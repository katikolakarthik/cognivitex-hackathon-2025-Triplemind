# StudyMate Advanced: AI-Powered PDF-Based Q&A System with Advanced RAG

## 🎓 Project Overview

StudyMate Advanced is a cutting-edge AI-powered academic assistant that implements **Retrieval-Augmented Generation (RAG)** to enable students to interact with their study materials through natural language questions. This advanced version features a complete RAG pipeline with semantic search, intelligent text chunking, and IBM Watsonx integration.

## 🚀 Advanced Features

### Core RAG Pipeline
- **🔍 Advanced Semantic Search**: Uses FAISS + SentenceTransformers for intelligent document retrieval
- **🔪 Intelligent Text Chunking**: 500-word chunks with 100-word overlap for context preservation
- **🧠 IBM Watsonx Integration**: Powered by Mixtral-8x7B-Instruct model for accurate responses
- **📊 Vector Database**: FAISS index for fast similarity search and retrieval

### Technical Architecture
- **Input Layer**: PDF upload and text extraction using PyMuPDF
- **Processing Layer**: Intelligent chunking with metadata preservation
- **Embedding Layer**: SentenceTransformers for semantic vector generation
- **Search Layer**: FAISS for fast similarity search
- **Generation Layer**: IBM Watsonx LLM for context-aware responses
- **UI Layer**: Modern Streamlit interface with real-time feedback

## 🛠️ Technology Stack

- **Python 3.8+** - Core programming language
- **Streamlit** - Modern web application framework
- **PyMuPDF** - Advanced PDF processing and text extraction
- **SentenceTransformers** - State-of-the-art text embeddings
- **FAISS** - Facebook AI Similarity Search for vector operations
- **IBM Watsonx** - Enterprise-grade LLM with Mixtral-8x7B-Instruct
- **NumPy & Pandas** - Data processing and manipulation

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- IBM Watsonx account and API credentials
- HuggingFace account (for embedding models)

### Setup Instructions

1. **Clone and navigate to the advanced folder**
   ```bash
   cd StudyMate_Advanced
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys
   ```

5. **Run the advanced application**
   ```bash
   streamlit run app_advanced.py
   ```

## 🔧 Configuration

### Environment Variables
Create a `.env` file with the following variables:

```env
# IBM Watsonx API Configuration
WATSONX_API_KEY=your_ibm_watsonx_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# HuggingFace (for embeddings)
HUGGINGFACE_API_TOKEN=your_huggingface_token_here

# Application Settings
MAX_FILE_SIZE=900  # MB
MAX_CHUNK_SIZE=500  # words per chunk
CHUNK_OVERLAP=100   # words overlap between chunks
EMBEDDING_MODEL=all-MiniLM-L6-v2
LLM_MODEL=mixtral-8x7b-instruct-v01
MAX_TOKENS=300
TEMPERATURE=0.5
```

### Getting API Keys

#### IBM Watsonx
1. Visit [IBM Watsonx](https://www.ibm.com/products/watsonx-ai)
2. Create an account and get your API key
3. Note your project ID from the Watsonx dashboard

#### HuggingFace
1. Visit [HuggingFace](https://huggingface.co/)
2. Create an account and get your API token
3. Used for downloading embedding models

## 📖 Usage

### Basic Workflow
1. **Upload PDFs** - Drag and drop multiple academic PDFs
2. **Process Documents** - Click "Process with Advanced RAG" to build the semantic index
3. **Ask Questions** - Type natural language questions about your documents
4. **Get Answers** - Receive AI-generated responses with source citations
5. **Review Sources** - Examine the retrieved context chunks for verification

### Advanced Features
- **Semantic Search**: Questions are matched to relevant document chunks using AI embeddings
- **Context Preservation**: 100-word overlap ensures no context is lost between chunks
- **Source Tracing**: Every answer includes references to specific document chunks
- **Chat History**: Complete Q&A session tracking with export functionality

## 🔍 How It Works

### 1. Document Processing
- PDFs are uploaded and processed using PyMuPDF
- Text is extracted and cleaned for optimal processing
- Content is split into intelligent chunks with metadata

### 2. Embedding Generation
- Each text chunk is converted to a semantic vector using SentenceTransformers
- The all-MiniLM-L6-v2 model generates 384-dimensional embeddings
- Vectors are optimized for semantic similarity tasks

### 3. Vector Indexing
- FAISS builds a fast similarity search index
- L2 distance metric ensures accurate similarity calculations
- Index supports real-time query processing

### 4. Semantic Retrieval
- User questions are embedded using the same model
- FAISS returns top-k most similar chunks
- Similarity scores indicate relevance confidence

### 5. AI Generation
- Retrieved chunks provide context for the LLM
- IBM Watsonx generates context-aware responses
- Mixtral-8x7B-Instruct ensures factual accuracy

## 📊 Performance Metrics

- **Chunk Size**: 500 words optimal for academic content
- **Overlap**: 100 words preserves context continuity
- **Embedding Dimension**: 384D vectors for semantic search
- **Search Speed**: FAISS provides sub-second retrieval
- **Response Quality**: Context-grounded answers with citations

## 🧪 Testing

### Connection Testing
- **RAG Engine Test**: Verifies FAISS and embedding model initialization
- **Watsonx Test**: Validates IBM API connectivity
- **Document Processing Test**: Ensures PDF extraction and chunking

### Sample Questions
Test the system with academic questions like:
- "What is machine learning?"
- "Explain neural networks"
- "What are the key concepts in this chapter?"
- "Summarize the main points about..."

## 🚀 Future Enhancements

- **Multi-modal Support**: Image and table extraction from PDFs
- **Advanced Chunking**: Sentence-aware and paragraph-aware splitting
- **Hybrid Search**: Combine semantic and keyword-based retrieval
- **Confidence Scoring**: Reliability metrics for generated answers
- **Batch Processing**: Handle large document collections efficiently

## 🏆 Hackathon Features

This advanced version demonstrates:
- ✅ **Complete RAG Pipeline** - From PDF to AI response
- ✅ **Semantic Search** - FAISS + SentenceTransformers integration
- ✅ **Enterprise LLM** - IBM Watsonx with Mixtral-8x7B-Instruct
- ✅ **Intelligent Chunking** - Context-preserving text segmentation
- ✅ **Modern UI** - Streamlit with advanced styling and features
- ✅ **Source Verification** - Complete traceability of AI responses

## 📁 Project Structure

```
StudyMate_Advanced/
├── app_advanced.py          # Main Streamlit application
├── rag_engine.py            # Advanced RAG engine with FAISS
├── watsonx_client.py        # IBM Watsonx integration
├── requirements.txt          # Python dependencies
├── .env.example             # Environment configuration template
└── README.md                # This file
```

## 🤝 Team

**TripleMind Team** - Hackathon Project
- Advanced RAG implementation
- Semantic search and retrieval
- IBM Watsonx integration
- Modern Streamlit interface

## 📄 License

This project is developed for educational and hackathon purposes.

---

**🎯 Ready to experience the future of AI-powered studying? Run `streamlit run app_advanced.py` and start exploring your documents with advanced RAG technology!**
