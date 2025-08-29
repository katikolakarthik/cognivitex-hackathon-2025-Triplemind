"""
StudyMate - AI-Powered PDF-Based Q&A System for Students
Hackathon Project - TripleMind Team
"""

import streamlit as st
import os
import fitz  # PyMuPDF
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize session state
if 'pdf_texts' not in st.session_state:
    st.session_state.pdf_texts = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF using PyMuPDF"""
    try:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return None

def call_watsonx_api(prompt, context=""):
    """Call IBM Watsonx API for AI responses"""
    try:
        api_key = os.getenv('WATSONX_API_KEY')
        project_id = os.getenv('WATSONX_PROJECT_ID')
        url = os.getenv('WATSONX_URL')
        
        if not all([api_key, project_id, url]):
            return "❌ Watsonx API configuration incomplete"
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model_id': 'mixtral-8x7b-instruct-v0-q',
            'parameters': {
                'max_new_tokens': 1000,
                'temperature': 0.7,
                'top_p': 0.9,
                'top_k': 50
            },
            'project_id': project_id,
            'prompt': f"Context: {context}\n\nQuestion: {prompt}\n\nAnswer:"
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('results', [{}])[0].get('generated_text', 'No response generated')
        else:
            return f"❌ Watsonx API Error: {response.status_code}"
            
    except Exception as e:
        return f"❌ Error calling Watsonx API: {str(e)}"

def main():
    # Header
    st.markdown("""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; color: white; text-align: center;">
        <h1>🎓 StudyMate</h1>
        <h3>AI-Powered PDF-Based Q&A System for Students</h3>
        <p>Hackathon Project - TripleMind Team</p>
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
                        text = extract_text_from_pdf(pdf_file)
                        if text:
                            st.session_state.pdf_texts.append({
                                'filename': pdf_file.name,
                                'text': text[:1000] + "..." if len(text) > 1000 else text,
                                'full_text': text
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
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Ask Questions")
        
        # Question input
        question = st.text_input(
            "Ask a question:",
            placeholder="e.g., What are the main concepts in this material?",
            help="Ask any question about your uploaded documents"
        )
        
        if question and st.button("🚀 Get Answer", type="primary"):
            if not st.session_state.pdf_texts:
                st.warning("⚠️ Please upload and process PDF documents first!")
            else:
                with st.spinner("🤔 Thinking..."):
                    # Combine all document texts for context
                    context = "\n\n".join([f"Document: {doc['filename']}\n{doc['full_text']}" for doc in st.session_state.pdf_texts])
                    
                    # Get AI response
                    response = call_watsonx_api(question, context)
                    
                    if response:
                        # Add to chat history
                        st.session_state.chat_history.append({
                            'question': question,
                            'answer': response,
                            'timestamp': datetime.now().strftime("%H:%M")
                        })
                        
                        st.success("✅ Answer generated!")
                        st.experimental_rerun()
                    else:
                        st.error("❌ Failed to get answer. Please try again.")
        
        # Chat history
        if st.session_state.chat_history:
            st.subheader("📝 Conversation History")
            for i, chat in enumerate(reversed(st.session_state.chat_history)):
                with st.expander(f"Q: {chat['question'][:50]}... ({chat['timestamp']})"):
                    st.write(f"**Question:** {chat['question']}")
                    st.write(f"**Answer:** {chat['answer']}")
    
    with col2:
        st.header("📊 Project Info")
        
        # Hackathon Goals
        st.subheader("🎯 Hackathon Goals")
        st.write("✅ PDF Processing")
        st.write("✅ AI Q&A System") 
        st.write("✅ Student Interface")
        st.write("✅ Modern UI/UX")
        
        st.markdown("---")
        
        # Technology Stack
        st.subheader("🔧 Technology Stack")
        st.write("• Python + Streamlit")
        st.write("• PyMuPDF (PDF Processing)")
        st.write("• IBM Watsonx AI")
        st.write("• Modern Web Interface")
        
        st.markdown("---")
        
        # Statistics (when documents are uploaded)
        if st.session_state.pdf_texts:
            st.subheader("📈 Statistics")
            st.metric("Documents", len(st.session_state.pdf_texts))
            st.metric("Questions Asked", len(st.session_state.chat_history))
            st.metric("Total Text", f"{sum(len(doc['full_text']) for doc in st.session_state.pdf_texts):,} chars")
            st.markdown("---")
        
        # Project Description
        st.subheader("📚 About StudyMate")
        st.write("StudyMate is an AI-powered academic assistant that transforms how students interact with their study materials. Upload PDFs and ask questions in natural language!")
        
        # Features List
        st.subheader("🚀 Key Features")
        st.write("• **Multi-PDF Upload** - Handle multiple study materials")
        st.write("• **AI-Powered Q&A** - Get instant, contextual answers")
        st.write("• **Smart Processing** - Advanced text extraction and analysis")
        st.write("• **Student-Friendly** - Intuitive interface designed for learners")

if __name__ == "__main__":
    main()
