"""
StudyMate Advanced RAG Engine
Advanced Retrieval-Augmented Generation with FAISS and SentenceTransformers
Hackathon Project - TripleMind Team
"""

import os
import fitz  # PyMuPDF
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from sentence_transformers import SentenceTransformer
import faiss
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AdvancedRAGEngine:
    """Advanced RAG Engine with semantic search and intelligent chunking"""
    
    def __init__(self):
        """Initialize the RAG engine with embedding model and FAISS index"""
        self.chunk_size = int(os.getenv('MAX_CHUNK_SIZE', 500))
        self.chunk_overlap = int(os.getenv('CHUNK_OVERLAP', 100))
        self.embedding_model_name = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
        
        # Initialize embedding model
        print(f"🔄 Loading embedding model: {self.embedding_model_name}")
        self.embedding_model = SentenceTransformer(self.embedding_model_name)
        self.embedding_dimension = self.embedding_model.get_sentence_embedding_dimension()
        
        # Initialize FAISS index
        self.index = faiss.IndexFlatL2(self.embedding_dimension)
        self.chunks = []
        self.chunk_metadata = []
        self.document_mapping = {}
        
        print(f"✅ RAG Engine initialized with {self.embedding_dimension}D embeddings")
    
    def extract_text_from_pdf(self, pdf_file, filename: str) -> str:
        """Extract clean text from PDF using PyMuPDF"""
        try:
            doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
            text = ""
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                page_text = page.get_text()
                
                # Clean and normalize text
                page_text = self._clean_text(page_text)
                text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
            
            doc.close()
            print(f"📄 Extracted {len(text)} characters from {filename}")
            return text
            
        except Exception as e:
            print(f"❌ Error extracting text from {filename}: {str(e)}")
            return ""
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Remove common PDF artifacts
        text = text.replace('\x00', '')  # Null characters
        text = text.replace('\uf0b7', '•')  # Bullet points
        
        # Normalize line breaks
        text = text.replace('\n', ' ')
        text = text.replace('\r', ' ')
        
        return text.strip()
    
    def create_intelligent_chunks(self, text: str, filename: str) -> List[Dict]:
        """Create intelligent text chunks with metadata"""
        chunks = []
        words = text.split()
        
        if len(words) <= self.chunk_size:
            # Single chunk for short texts
            chunk = {
                'text': text,
                'filename': filename,
                'chunk_id': 0,
                'page_start': 1,
                'page_end': 1,
                'word_count': len(words)
            }
            chunks.append(chunk)
            return chunks
        
        # Create overlapping chunks
        start = 0
        chunk_id = 0
        
        while start < len(words):
            end = start + self.chunk_size
            
            # Try to break at sentence boundary
            if end < len(words):
                # Look for sentence endings within the last 50 words
                for i in range(end, max(start, end - 50), -1):
                    if i < len(words) and words[i].endswith(('.', '!', '?')):
                        end = i + 1
                        break
            
            # Extract chunk text
            chunk_words = words[start:end]
            chunk_text = ' '.join(chunk_words)
            
            # Create chunk with metadata
            chunk = {
                'text': chunk_text,
                'filename': filename,
                'chunk_id': chunk_id,
                'page_start': 1,  # Simplified for now
                'page_end': 1,    # Could be enhanced with actual page mapping
                'word_count': len(chunk_words),
                'start_word': start,
                'end_word': end
            }
            
            chunks.append(chunk)
            chunk_id += 1
            
            # Move start position with overlap
            start = end - self.chunk_overlap
            if start >= len(words):
                break
        
        print(f"🔪 Created {len(chunks)} chunks from {filename}")
        return chunks
    
    def generate_embeddings(self, chunks: List[Dict]) -> np.ndarray:
        """Generate embeddings for all text chunks"""
        texts = [chunk['text'] for chunk in chunks]
        
        print(f"🧠 Generating embeddings for {len(texts)} chunks...")
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
        
        print(f"✅ Generated {embeddings.shape[0]} embeddings of dimension {embeddings.shape[1]}")
        return embeddings
    
    def build_faiss_index(self, embeddings: np.ndarray, chunks: List[Dict]):
        """Build FAISS index for fast similarity search"""
        # Clear existing index
        self.index = faiss.IndexFlatL2(self.embedding_dimension)
        
        # Add embeddings to index
        self.index.add(embeddings.astype('float32'))
        
        # Store chunks and metadata
        self.chunks = chunks
        self.chunk_metadata = chunks
        
        print(f"🔍 FAISS index built with {self.index.ntotal} vectors")
    
    def semantic_search(self, query: str, top_k: int = 3) -> List[Tuple[Dict, float]]:
        """Perform semantic search using FAISS"""
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])
        
        # Search in FAISS index
        distances, indices = self.index.search(
            query_embedding.astype('float32'), 
            min(top_k, len(self.chunks))
        )
        
        # Return results with metadata and similarity scores
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.chunks):
                # Convert distance to similarity score (0-1, higher is better)
                similarity_score = 1 / (1 + distance)
                
                result = {
                    'chunk': self.chunks[idx],
                    'similarity_score': similarity_score,
                    'distance': float(distance)
                }
                results.append(result)
        
        # Sort by similarity score (highest first)
        results.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        print(f"🔍 Semantic search returned {len(results)} results")
        return results
    
    def process_documents(self, uploaded_files: List) -> bool:
        """Process multiple PDF documents and build search index"""
        try:
            all_chunks = []
            
            for uploaded_file in uploaded_files:
                filename = uploaded_file.name
                print(f"📚 Processing document: {filename}")
                
                # Extract text
                text = self.extract_text_from_pdf(uploaded_file, filename)
                if not text:
                    continue
                
                # Create chunks
                chunks = self.create_intelligent_chunks(text, filename)
                all_chunks.extend(chunks)
                
                # Store document mapping
                self.document_mapping[filename] = {
                    'total_chunks': len(chunks),
                    'total_words': len(text.split()),
                    'file_size': uploaded_file.size
                }
            
            if not all_chunks:
                print("❌ No valid chunks created from documents")
                return False
            
            # Generate embeddings
            embeddings = self.generate_embeddings(all_chunks)
            
            # Build FAISS index
            self.build_faiss_index(embeddings, all_chunks)
            
            print(f"✅ Successfully processed {len(uploaded_files)} documents")
            print(f"📊 Total chunks: {len(all_chunks)}")
            print(f"🔍 FAISS index ready for semantic search")
            
            return True
            
        except Exception as e:
            print(f"❌ Error processing documents: {str(e)}")
            return False
    
    def get_context_for_query(self, query: str, top_k: int = 3) -> str:
        """Get relevant context chunks for a query"""
        search_results = self.semantic_search(query, top_k)
        
        if not search_results:
            return "No relevant context found."
        
        context_parts = []
        for i, result in enumerate(search_results):
            chunk = result['chunk']
            similarity = result['similarity_score']
            
            context_part = f"Context {i+1} (Similarity: {similarity:.3f}):\n"
            context_part += f"Source: {chunk['filename']}, Chunk {chunk['chunk_id']}\n"
            context_part += f"Text: {chunk['text'][:300]}...\n"
            context_part += "-" * 50 + "\n"
            
            context_parts.append(context_part)
        
        return "\n".join(context_parts)
    
    def get_statistics(self) -> Dict:
        """Get statistics about the current RAG system"""
        return {
            'total_chunks': len(self.chunks),
            'total_documents': len(self.document_mapping),
            'embedding_dimension': self.embedding_dimension,
            'faiss_index_size': self.index.ntotal if hasattr(self.index, 'ntotal') else 0,
            'chunk_size': self.chunk_size,
            'chunk_overlap': self.chunk_overlap,
            'documents': self.document_mapping
        }
