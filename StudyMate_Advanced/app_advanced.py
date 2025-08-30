"""
StudyMate Advanced: AI-Powered PDF-Based Q&A System with Advanced RAG
Advanced Retrieval-Augmented Generation with FAISS, SentenceTransformers, and IBM Watsonx
Hackathon Project - TripleMind Team
"""

import streamlit as st
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Import our custom modules
from rag_engine import AdvancedRAGEngine
from watsonx_client import WatsonxClient

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="StudyMate Advanced - AI Academic Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .info-box {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .rag-stats {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .chunk-display {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'rag_engine' not in st.session_state:
    st.session_state.rag_engine = None
if 'watsonx_client' not in st.session_state:
    st.session_state.watsonx_client = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'documents_processed' not in st.session_state:
    st.session_state.documents_processed = False

def initialize_components():
    """Initialize RAG engine and Watsonx client"""
    try:
        if st.session_state.rag_engine is None:
            with st.spinner("🔄 Initializing Advanced RAG Engine..."):
                st.session_state.rag_engine = AdvancedRAGEngine()
            st.success("✅ RAG Engine initialized successfully!")
        
        if st.session_state.watsonx_client is None:
            with st.spinner("🔄 Initializing IBM Watsonx Client..."):
                st.session_state.watsonx_client = WatsonxClient()
            st.success("✅ Watsonx Client initialized successfully!")
            
    except Exception as e:
        st.error(f"❌ Error initializing components: {str(e)}")
        return False
    
    return True

def process_documents(uploaded_files):
    """Process uploaded PDF documents using the RAG engine"""
    if not st.session_state.rag_engine:
        st.error("❌ RAG Engine not initialized")
        return False
    
    try:
        with st.spinner("🔄 Processing documents with advanced RAG pipeline..."):
            success = st.session_state.rag_engine.process_documents(uploaded_files)
            
            if success:
                st.session_state.documents_processed = True
                st.success(f"✅ Successfully processed {len(uploaded_files)} document(s)")
                return True
            else:
                st.error("❌ Failed to process documents")
                return False
                
    except Exception as e:
        st.error(f"❌ Error processing documents: {str(e)}")
        return False

def generate_answer(question: str):
    """Generate answer using RAG pipeline and Watsonx"""
    if not st.session_state.rag_engine or not st.session_state.watsonx_client:
        st.error("❌ Components not initialized")
        return None, None
    
    try:
        # Get relevant context using semantic search
        with st.spinner("🔍 Performing semantic search..."):
            search_results = st.session_state.rag_engine.semantic_search(question, top_k=3)
        
        if not search_results:
            st.warning("⚠️ No relevant context found for your question")
            return None, None
        
        # Prepare context for LLM
        context_parts = []
        for i, result in enumerate(search_results):
            chunk = result['chunk']
            similarity = result['similarity_score']
            
            context_part = f"Context {i+1} (Similarity: {similarity:.3f}):\n"
            context_part += f"Source: {chunk['filename']}, Chunk {chunk['chunk_id']}\n"
            context_part += f"Text: {chunk['text']}\n"
            context_part += "-" * 50 + "\n"
            
            context_parts.append(context_part)
        
        context = "\n".join(context_parts)
        
        # Generate answer using Watsonx
        with st.spinner("🧠 Generating AI response with IBM Watsonx..."):
            result = st.session_state.watsonx_client.generate_response(question, context)
        
        if result and result.get('success'):
            return result['response'], search_results
        else:
            error_msg = result.get('error', 'Unknown error') if result else 'No response'
            st.error(f"❌ Failed to generate answer from Watsonx: {error_msg}")
            return None, None
            
    except Exception as e:
        st.error(f"❌ Error generating answer: {str(e)}")
        return None, None

def main():
    """Main application function"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎓 StudyMate Advanced</h1>
        <h3>AI-Powered PDF-Based Q&A System with Advanced RAG</h3>
        <p>Advanced Retrieval-Augmented Generation with FAISS, SentenceTransformers, and IBM Watsonx</p>
        <p><strong>Hackathon Project - TripleMind Team</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize components
    if not initialize_components():
        st.error("❌ Failed to initialize system components. Please check your configuration.")
        return
    
    # Sidebar
    with st.sidebar:
        st.header("📚 Document Management")
        
        # File upload
        uploaded_files = st.file_uploader(
            "Upload PDF Documents",
            type=['pdf'],
            accept_multiple_files=True,
            help="Upload one or more PDF files for advanced RAG processing"
        )
        
        if uploaded_files:
            st.success(f"📄 {len(uploaded_files)} PDF(s) uploaded!")
            
            # Process documents button
            if st.button("🔍 Process with Advanced RAG", type="primary"):
                if process_documents(uploaded_files):
                    st.rerun()
        
        # System status
        st.header("🔧 System Status")
        
        if st.session_state.rag_engine:
            stats = st.session_state.rag_engine.get_statistics()
            
            # Professional metrics display
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📊 Total Chunks", stats['total_chunks'])
                st.metric("📚 Documents", stats['total_documents'])
            with col2:
                st.metric("🧠 Embedding Dim", stats['embedding_dimension'])
                st.metric("🔍 FAISS Index", "Ready" if stats['faiss_index_size'] > 0 else "Building")
            
            # Advanced RAG Status
            if stats['total_chunks'] > 0:
                st.success("✅ Advanced RAG Pipeline: ACTIVE")
                st.info(f"🎯 Processing: {stats['chunk_size']} words per chunk, {stats['chunk_overlap']} overlap")
            else:
                st.warning("⚠️ RAG Pipeline: Waiting for documents")
        
        if st.session_state.watsonx_client:
            model_info = st.session_state.watsonx_client.get_model_info()
            
            # AI Model Status
            st.header("🤖 AI Model Status")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("🧠 LLM Model", model_info['model_id'].split('/')[-1])
                st.metric("🔥 Max Tokens", model_info['max_tokens'])
            with col2:
                st.metric("🌡️ Temperature", model_info['temperature'])
                st.metric("🔗 API Status", "Connected")
            
            st.success("✅ IBM Watsonx AI: Ready for Generation")
        
        # Test connections
        st.header("🧪 Test Connections")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Test RAG"):
                if st.session_state.rag_engine:
                    st.success("✅ RAG Engine: Ready")
                else:
                    st.error("❌ RAG Engine: Not Ready")
        
        with col2:
            if st.button("Test Watsonx"):
                if st.session_state.watsonx_client:
                    if st.session_state.watsonx_client.test_connection():
                        st.success("✅ Watsonx: Connected")
                    else:
                        st.error("❌ Watsonx: Connection Failed")
                else:
                    st.error("❌ Watsonx: Not Ready")
    
    # Main content area
    if not st.session_state.documents_processed:
        st.info("📚 Please upload and process PDF documents to start using the advanced RAG system.")
        
        # Show features
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h4>🔍 Advanced Semantic Search</h4>
                <p>Uses FAISS + SentenceTransformers for intelligent document retrieval</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <h4>🧠 IBM Watsonx Integration</h4>
                <p>Powered by Mixtral-8x7B-Instruct model for accurate responses</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h4>🔪 Intelligent Text Chunking</h4>
                <p>500-word chunks with 100-word overlap for context preservation</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <h4>📊 Advanced RAG Pipeline</h4>
                <p>Complete pipeline from PDF to semantic search to AI generation</p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # RAG system is ready
        st.success("🎯 Advanced RAG System Ready! You can now ask questions.")
        
        # Question input
        st.header("❓ Ask Your Question")
        question = st.text_input(
            "Enter your question about the uploaded documents:",
            placeholder="e.g., What is machine learning? Explain neural networks..."
        )
        
        if st.button("🚀 Generate Answer", type="primary") and question:
            answer, search_results = generate_answer(question)
            
            if answer and search_results:
                # Display answer
                st.header("🤖 AI-Generated Answer")
                st.markdown(f"**Question:** {question}")
                st.markdown(f"**Answer:** {answer}")
                
                # Display source chunks
                st.header("📚 Source Context (Retrieved Chunks)")
                for i, result in enumerate(search_results):
                    chunk = result['chunk']
                    similarity = result['similarity_score']
                    
                    with st.expander(f"Context {i+1} - {chunk['filename']} (Similarity: {similarity:.3f})"):
                        st.markdown(f"**Source:** {chunk['filename']}, Chunk {chunk['chunk_id']}")
                        st.markdown(f"**Word Count:** {chunk['word_count']}")
                        st.markdown(f"**Text:**")
                        # Display text content directly without HTML wrapping
                        st.text_area(
                            label="Chunk Content",
                            value=chunk['text'],
                            height=200,
                            disabled=True,
                            key=f"chunk_{i}"
                        )
                
                # Add to chat history
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                chat_entry = {
                    'timestamp': timestamp,
                    'question': question,
                    'answer': answer,
                    'sources': [r['chunk']['filename'] for r in search_results]
                }
                st.session_state.chat_history.append(chat_entry)
                
                st.success("✅ Answer generated and added to chat history!")
            elif "rate limit" in str(answer).lower():
                st.error("🚫 Rate limit exceeded. Please wait a few minutes before trying again.")
                st.info("💡 **What happened:** IBM Watsonx has API rate limits to prevent abuse.")
                st.info("⏰ **Solution:** Wait 2-3 minutes and try again, or ask fewer questions in a short time.")
            else:
                st.error("❌ Failed to generate answer. Please try again.")
        
        # Chat history
        if st.session_state.chat_history:
            st.header("💬 Chat History")
            
            for i, entry in enumerate(reversed(st.session_state.chat_history)):
                with st.expander(f"Q&A {len(st.session_state.chat_history) - i} - {entry['timestamp']}"):
                    st.markdown(f"**Question:** {entry['question']}")
                    st.markdown(f"**Answer:** {entry['answer']}")
                    st.markdown(f"**Sources:** {', '.join(entry['sources'])}")
            
            # Download chat history
            if st.button("📥 Download Chat History"):
                chat_text = ""
                for entry in st.session_state.chat_history:
                    chat_text += f"Timestamp: {entry['timestamp']}\n"
                    chat_text += f"Question: {entry['question']}\n"
                    chat_text += f"Answer: {entry['answer']}\n"
                    chat_text += f"Sources: {', '.join(entry['sources'])}\n"
                    chat_text += "-" * 50 + "\n\n"
                
                st.download_button(
                    label="💾 Download as TXT",
                    data=chat_text,
                    file_name=f"studymate_chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )

if __name__ == "__main__":
    main()
