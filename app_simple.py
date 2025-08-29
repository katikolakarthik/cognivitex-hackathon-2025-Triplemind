"""
StudyMate: AI-Powered PDF-Based Q&A System for Students
Simplified Working Version - Uses Google Gemini API
"""

import streamlit as st
import os
import fitz  # PyMuPDF
import requests
import json
from datetime import datetime
import tempfile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="StudyMate - AI Academic Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling and tight layout
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .info-box {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    
    /* Remove unwanted spacing */
    .stExpander {
        margin: 0.5rem 0;
    }
    
    .stButton > button {
        margin: 0.25rem 0;
    }
    
    /* Tight layout for sources */
    .sources-section {
        margin: 0.5rem 0;
        padding: 0.5rem;
    }
    
    /* Optimize column spacing */
    .row-widget.stHorizontal {
        gap: 1rem;
    }
    
    /* Right column styling for proper alignment */
    .right-column {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 10px;
        padding: 1rem;
        border-left: 2px solid #667eea;
    }
    
    /* Ensure proper column spacing */
    .stColumns {
        gap: 2rem;
    }
    
    /* Right column content styling */
    .project-info {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'pdf_texts' not in st.session_state:
    st.session_state.pdf_texts = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF using PyMuPDF with page-level extraction"""
    try:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        pages_data = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            if text.strip():  # Only add non-empty pages
                pages_data.append({
                    'page': page_num + 1,
                    'text': text.strip()
                })
        
        doc.close()
        return pages_data
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return None

def create_chunks_with_metadata(pages_data, chunk_size=1000, overlap=200):
    """Create text chunks with metadata for citations"""
    chunks = []
    
    for page_data in pages_data:
        page_num = page_data['page']
        text = page_data['text']
        doc_name = page_data.get('filename', 'Unknown')
        
        # Split text into chunks
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]
            
            # Add overlap for better context
            if start > 0:
                chunk_text = text[start-overlap:end]
            
            chunks.append({
                'doc': doc_name,
                'page': page_num,
                'text': chunk_text.strip(),
                'start_pos': start
            })
            
            start = end - overlap
            if start >= len(text):
                break
    
    return chunks

def parse_citations(response_text):
    """Parse citations from AI response text"""
    import re
    
    # Pattern to match [DocName p.X] citations
    citation_pattern = r'\[([^\]]+)\s+p\.(\d+)\]'
    citations = []
    
    # Find all citations in the response
    matches = re.finditer(citation_pattern, response_text)
    for match in matches:
        doc_name = match.group(1).strip()
        page_num = int(match.group(2))
        
        # Check if this citation already exists
        existing = next((c for c in citations if c['doc'] == doc_name and c['page'] == page_num), None)
        if not existing:
            citations.append({
                'doc': doc_name,
                'page': page_num,
                'count': 1
            })
        else:
            existing['count'] += 1
    
    return citations

def call_gemini_api(prompt, context_chunks, filename=""):
    """Call Google Gemini API with citations enforcement"""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        st.error("Google API key not found. Please check your .env file.")
        return None
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    if context_chunks:
        # Build context with citations format
        context_lines = []
        for chunk in context_chunks:
            doc_name = chunk['doc'] or filename
            page_num = chunk['page']
            snippet = chunk['text'][:500]  # Trim to 500 chars
            context_lines.append(f"[{doc_name} p.{page_num}] {snippet}")
        
        context_text = "\n\n".join(context_lines)
        
        full_prompt = f"""Context from PDF documents:
{context_text}

Question: {prompt}

IMPORTANT: You MUST include inline citations in your answer using the format [DocName p.X] where X is the page number.

Rules for citations:
1. Every factual statement must be cited with [DocName p.X]
2. Use the exact document names and page numbers from the context
3. Place citations immediately after the relevant information
4. If you reference multiple sources, cite each one appropriately

Example citation format: "The main concept discussed here [DocName p.5] explains that..."

Please provide a simple, clean response with proper citations:
- Write in simple, clear sentences
- Include [DocName p.X] citations for all facts
- No bullet points or complex formatting
- Natural conversation style
- Easy to read line by line

Answer based on the provided context from the PDF documents."""
    else:
        full_prompt = f"""Question: {prompt}

Please provide a simple, clean response in plain text format:
- Write in simple, clear sentences
- No bullet points, no special formatting
- No emojis or symbols
- Just plain text like ChatGPT
- Easy to read line by line
- Natural conversation style"""

    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [{
            "parts": [{
                "text": full_prompt
            }]
        }]
    }
    
    try:
        response = requests.post(
            f"{url}?key={api_key}",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return "Sorry, I couldn't generate a response. Please try again."
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        st.error(f"Error calling Gemini API: {str(e)}")
        return None

def call_openrouter_api(prompt):
    """Call OpenRouter API for global knowledge using DeepSeek model"""
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        st.error("❌ OpenRouter API key not found. Please check your .env file.")
        return None
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://studymate-hackathon.com",
        "X-Title": "StudyMate - AI-Powered PDF Q&A System"
    }
    
    data = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful AI assistant. Provide clear, accurate answers in simple, conversational language. No bullet points or complex formatting - just clean, easy-to-read text like ChatGPT."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)

        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            else:
                st.error(f"❌ OpenRouter API returned empty response: {result}")
                return None
        else:
            # Surface common OpenRouter privacy/model errors clearly
            try:
                err_json = response.json()
            except Exception:
                err_json = response.text
            st.error(
                "❌ OpenRouter API error. If you see 'No endpoints found matching your data policy', either switch to a non-free model or enable Prompt Training at https://openrouter.ai/settings/privacy.\n"
                f"Status {response.status_code}: {err_json}"
            )
            return None

    except Exception as e:
        st.error(f"❌ Error calling OpenRouter API: {str(e)}")
        return None

def call_gpt_oss_api(prompt):
    """Call OpenRouter API for GPT-OSS-120B model (high-reasoning capabilities)"""
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not api_key:
        st.error("❌ OpenRouter API key not found. Please check your .env file.")
        return None
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://studymate-ai.com",
        "X-Title": "StudyMate AI"
    }
    
    data = {
        "model": "qwen/qwen-2.5-72b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert academic assistant with high reasoning capabilities. Provide detailed, well-structured answers with logical flow and clear explanations."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)

        if response.status_code == 200:
            result = response.json()
            if result.get('choices') and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            else:
                st.error(f"❌ OpenRouter (Qwen) API returned empty response: {result}")
                return None
        else:
            try:
                err_json = response.json()
            except Exception:
                err_json = response.text
            st.error(
                "❌ Model unavailable under current data policy. Consider enabling Prompt Training at https://openrouter.ai/settings/privacy or switch to another model (e.g., meta-llama/llama-3.1-70b-instruct).\n"
                f"Status {response.status_code}: {err_json}"
            )
            return None

    except Exception as e:
        st.error(f"❌ Error calling OpenRouter API: {str(e)}")
        return None

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🧠 StudyMate TripleMind</h1>
        <h3>AI-Powered PDF-Based Q&A System with Triple AI Models</h3>
        <p>📚 PDF-Specific (Gemini) + 🌍 Global Knowledge (DeepSeek) + 🤖 High Reasoning (GPT-OSS-120B)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📚 Document Management")
        
        # File upload
        uploaded_files = st.file_uploader(
            "Upload PDF Documents",
            type=['pdf'],
            accept_multiple_files=True,
            help="Upload one or more PDF files to analyze"
        )
        
        if uploaded_files:
            st.success(f"📄 {len(uploaded_files)} PDF(s) uploaded successfully!")
            
            # Process PDFs
            if st.button("🔍 Process Documents", type="primary"):
                with st.spinner("Processing PDFs..."):
                    st.session_state.pdf_texts = []
                    for pdf_file in uploaded_files:
                        pages_data = extract_text_from_pdf(pdf_file)
                        if pages_data:
                            # Combine all pages for display
                            full_text = "\n\n".join([f"Page {p['page']}: {p['text']}" for p in pages_data])
                            display_text = full_text[:1000] + "..." if len(full_text) > 1000 else full_text
                            
                            st.session_state.pdf_texts.append({
                                'filename': pdf_file.name,
                                'pages_data': pages_data,
                                'text': display_text,
                                'full_text': full_text
                            })
                    
                    if st.session_state.pdf_texts:
                        st.success(f"✅ {len(st.session_state.pdf_texts)} document(s) processed!")
                    else:
                        st.error("❌ Failed to process PDFs")
        
        # Document info
        if st.session_state.pdf_texts:
            st.subheader("📋 Processed Documents")
            for doc in st.session_state.pdf_texts:
                st.info(f"📄 {doc['filename']}")
                st.caption(f"Text length: {len(doc['full_text'])} characters")
        
        # Clear data
        if st.button("🗑️ Clear All Data"):
            st.session_state.pdf_texts = []
            st.session_state.chat_history = []
            st.experimental_rerun()
        
        # Sources Overview
        if st.session_state.chat_history:
            st.markdown("---")
            st.subheader("📚 Recent Sources")
            all_citations = []
            for chat in st.session_state.chat_history:
                if 'citations' in chat and chat['citations']:
                    all_citations.extend(chat['citations'])
            
            # Group citations by document
            if all_citations:
                doc_citations = {}
                for citation in all_citations:
                    key = (citation['doc'], citation['page'])
                    if key not in doc_citations:
                        doc_citations[key] = citation
                    else:
                        doc_citations[key]['count'] += citation['count']
                
                # Display unique citations
                for (doc_name, page_num), citation in doc_citations.items():
                    st.write(f"📄 **{doc_name}** - Page {page_num}")
                    if citation['count'] > 1:
                        st.caption(f"Referenced {citation['count']} times")
                    st.markdown("---")
    
    # Main content area - optimized layout with proper right-side alignment
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        st.header("💬 Ask Questions")
        
        # Question input
        question = st.text_input(
            "Ask a question:",
            placeholder="e.g., What are the main concepts in this material?",
            help="Ask any question - get both PDF-specific and global knowledge answers!"
        )
        
        # TripleMind Model Selection
        st.subheader("🧠 TripleMind AI Models")
        
        # Model selection checkboxes
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            pdf_only = st.checkbox("📚 PDF Only (Gemini)", value=False, help="Get answer only from uploaded documents using Google Gemini")
        with col2:
            deepseek_only = st.checkbox("🌍 DeepSeek Only", value=False, help="Get answer only from DeepSeek AI (general knowledge)")
        with col3:
            gpt_oss_only = st.checkbox("🤖 GPT-OSS Only", value=False, help="Get answer only from GPT-OSS-120B (high reasoning)")
        
        # TripleMind combination options
        st.markdown("**🎯 TripleMind Combinations:**")
        triple_col1, triple_col2, triple_col3 = st.columns([1, 1, 1])
        with triple_col1:
            gemini_deepseek = st.checkbox("📚+🌍 Gemini + DeepSeek", value=False, help="PDF-specific + Global knowledge")
        with triple_col2:
            gemini_gptoss = st.checkbox("📚+🤖 Gemini + GPT-OSS", value=False, help="PDF-specific + High reasoning")
        with triple_col3:
            all_three = st.checkbox("🧠 All Three Minds", value=False, help="Complete TripleMind: PDF + Global + Reasoning")
        
        # Ensure only one option is selected
        selected_options = [pdf_only, deepseek_only, gpt_oss_only, gemini_deepseek, gemini_gptoss, all_three]
        if sum(selected_options) > 1:
            st.warning("⚠️ Please select only one option")
            return
        elif sum(selected_options) == 0:
            # Default to PDF-only to avoid OpenRouter errors when user has no credits
            pdf_only = True
        
        if question and st.button("🚀 Get Answer", type="primary"):
            with st.spinner("🤔 Thinking..."):
                # Initialize response variables
                pdf_response = None
                global_response = None
                citations = []
                
                # Initialize response variables
                pdf_response = None
                deepseek_response = None
                gpt_oss_response = None
                citations = []
                
                # 1. Get PDF-specific answer from Gemini (if requested)
                if pdf_only or gemini_deepseek or gemini_gptoss or all_three:
                    if st.session_state.pdf_texts:
                        # Create chunks with metadata for citations
                        all_chunks = []
                        for doc in st.session_state.pdf_texts:
                            if 'pages_data' in doc:
                                chunks = create_chunks_with_metadata(doc['pages_data'])
                                for chunk in chunks:
                                    chunk['doc'] = doc['filename']
                                all_chunks.extend(chunks)
                        
                        # Get PDF-specific response with citations
                        pdf_response = call_gemini_api(question, all_chunks)
                        if pdf_response:
                            citations = parse_citations(pdf_response)
                    else:
                        st.warning("⚠️ No PDFs uploaded. Please upload documents first for PDF-specific answers.")
                        if pdf_only:
                            return
                
                # 2. Get global knowledge answer from DeepSeek (if requested)
                if deepseek_only or gemini_deepseek or all_three:
                    deepseek_response = call_openrouter_api(question)
                    if deepseek_response:
                        st.success("✅ DeepSeek AI response received!")
                    else:
                        st.error("❌ DeepSeek AI response failed!")
                
                # 3. Get high-reasoning answer from GPT-OSS-120B (if requested)
                if gpt_oss_only or gemini_gptoss or all_three:
                    gpt_oss_response = call_gpt_oss_api(question)
                    if gpt_oss_response:
                        st.success("✅ GPT-OSS-120B response received!")
                    else:
                        st.error("❌ GPT-OSS-120B response failed!")
                
                # 4. Combine responses and add to chat history
                if pdf_response or deepseek_response or gpt_oss_response:
                    # Create combined response based on user choice
                    combined_response = ""
                    response_type = []
                    
                    if pdf_response:
                        combined_response += f"📚 **PDF-Specific Answer (Gemini):**\n{pdf_response}\n\n"
                        response_type.append("PDF")
                    
                    if deepseek_response:
                        combined_response += f"🌍 **Global Knowledge (DeepSeek):**\n{deepseek_response}\n\n"
                        response_type.append("DeepSeek")
                    
                    if gpt_oss_response:
                        combined_response += f"🤖 **High Reasoning (GPT-OSS-120B):**\n{gpt_oss_response}\n\n"
                        response_type.append("GPT-OSS")
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        'question': question,
                        'answer': combined_response,
                        'citations': citations,
                        'response_type': response_type,
                        'timestamp': datetime.now().strftime("%H:%M")
                    })
                    
                    # Show success message based on response type
                    if len(response_type) == 3:
                        st.success("🧠 **TripleMind Complete:** PDF + Global + Reasoning!")
                    elif len(response_type) == 2:
                        st.success(f"🎯 **Dual Response:** {' + '.join(response_type)}")
                    elif "PDF" in response_type:
                        st.success("✅ PDF-specific answer generated with citations!")
                    elif "DeepSeek" in response_type:
                        st.success("✅ DeepSeek AI answer generated!")
                    elif "GPT-OSS" in response_type:
                        st.success("✅ GPT-OSS-120B answer generated!")
                    
                    st.experimental_rerun()
                else:
                    # Better error handling for different scenarios
                    if gpt_oss_only and not gpt_oss_response:
                        st.error("❌ Failed to get GPT-OSS-120B response. Please check your OpenRouter API key and try again.")
                    elif deepseek_only and not deepseek_response:
                        st.error("❌ Failed to get DeepSeek AI response. Please check your OpenRouter API key and try again.")
                    elif pdf_only and not pdf_response:
                        st.error("❌ Failed to get PDF-specific response. Please check your Google API key and try again.")
                    else:
                        st.error("❌ Failed to get answers. Please try again.")
        
        # Chat history
        if st.session_state.chat_history:
            st.subheader("📝 Conversation History")
            for i, chat in enumerate(reversed(st.session_state.chat_history)):
                with st.expander(f"Q: {chat['question'][:50]}... ({chat['timestamp']})"):
                    st.write(f"**Question:** {chat['question']}")
                    
                    # Display combined answer
                    st.markdown(chat['answer'])
                    
                    # Show response type indicators
                    if 'response_type' in chat:
                        response_types = chat['response_type']
                        if len(response_types) == 3:
                            st.success("🧠 **TripleMind Complete:** PDF + Global + Reasoning")
                        elif len(response_types) == 2:
                            st.success(f"🎯 **Dual Response:** {' + '.join(response_types)}")
                        elif "PDF" in response_types:
                            st.info("📚 **PDF Response:** Based on uploaded documents (Gemini)")
                        elif "DeepSeek" in response_types:
                            st.info("🌍 **DeepSeek Response:** AI-powered general knowledge")
                        elif "GPT-OSS" in response_types:
                            st.info("🤖 **GPT-OSS Response:** High-reasoning capabilities")
                    
                    # Display sources if citations exist
                    if 'citations' in chat and chat['citations']:
                        st.markdown("---")
                        st.subheader("📚 PDF Sources")
                        for citation in chat['citations']:
                            doc_name = citation['doc']
                            page_num = citation['page']
                            count = citation['count']
                            
                            # Display citation info
                            st.write(f"📄 **{doc_name}** - Page {page_num}")
                            if count > 1:
                                st.caption(f"Referenced {count} times")
                            
                            # View page button
                            if st.button(f"View Page {page_num}", key=f"view_{doc_name}_{page_num}_{i}"):
                                st.info(f"📖 Showing content from {doc_name} - Page {page_num}")
                                # Find and display the page content
                                for doc in st.session_state.pdf_texts:
                                    if doc['filename'] == doc_name:
                                        for page_data in doc['pages_data']:
                                            if page_data['page'] == page_num:
                                                st.text_area(f"Page {page_num} Content:", page_data['text'], height=200)
                                                break
                                        break
    
    with right_col:
        # Apply right column styling
        st.markdown('<div class="right-column">', unsafe_allow_html=True)
        
        st.header("📊 Project Info")
        
        # Hackathon Goals
        with st.container():
            st.subheader("🎯 Hackathon Goals")
            st.write("✅ PDF Processing")
            st.write("✅ AI Q&A System") 
            st.write("✅ Student Interface")
            st.write("✅ Modern UI/UX")
        
        st.markdown("---")
        
        # Technology Stack
        with st.container():
            st.subheader("🔧 Technology Stack")
            st.write("• Python + Streamlit")
            st.write("• PyMuPDF (PDF Processing)")
            st.write("• 🧠 **TripleMind AI Models:**")
            st.write("  - 📚 Google Gemini AI (PDF-specific)")
            st.write("  - 🌍 DeepSeek AI (Global knowledge)")
            st.write("  - 🤖 GPT-OSS-120B (High reasoning)")
            st.write("• OpenRouter API Integration")
            st.write("• Modern Web Interface")
        
        st.markdown("---")
        
        # Statistics (when documents are uploaded)
        if st.session_state.pdf_texts:
            with st.container():
                st.subheader("📈 Statistics")
                st.metric("Documents", len(st.session_state.pdf_texts))
                st.metric("Questions Asked", len(st.session_state.chat_history))
                st.metric("Total Text", f"{sum(len(doc['full_text']) for doc in st.session_state.pdf_texts):,} chars")
            st.markdown("---")
        
        # Project Description
        with st.container():
            st.subheader("📚 About StudyMate")
            st.write("StudyMate is an AI-powered academic assistant that transforms how students interact with their study materials. Upload PDFs and ask questions in natural language!")
        
        # Features List
        with st.container():
            st.subheader("🚀 Key Features")
            st.write("• **Multi-PDF Upload** - Handle multiple study materials")
            st.write("• **AI-Powered Q&A** - Get instant, contextual answers")
            st.write("• **Smart Processing** - Advanced text extraction and analysis")
            st.write("• **Student-Friendly** - Intuitive interface designed for learners")
        
        # Close right column styling
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
