"""
Utility functions for StudyMate
Hackathon Project - TripleMind Team
"""

import os
import requests
import json
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WatsonxClient:
    """Client for IBM Watsonx AI API"""
    
    def __init__(self):
        self.api_key = os.getenv('WATSONX_API_KEY')
        self.project_id = os.getenv('WATSONX_PROJECT_ID')
        self.url = os.getenv('WATSONX_URL')
        
        if not all([self.api_key, self.project_id, self.url]):
            raise ValueError("Watsonx API configuration incomplete. Please check your .env file.")
    
    def generate_response(self, prompt: str, context: str = "", max_tokens: int = 1000) -> Optional[str]:
        """
        Generate AI response using Watsonx API
        
        Args:
            prompt (str): User's question
            context (str): Context from PDF documents
            max_tokens (int): Maximum tokens for response
            
        Returns:
            Optional[str]: Generated response or None if failed
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model_id': 'mixtral-8x7b-instruct-v0-q',
                'parameters': {
                    'max_new_tokens': max_tokens,
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'top_k': 50
                },
                'project_id': self.project_id,
                'prompt': f"Context: {context}\n\nQuestion: {prompt}\n\nAnswer:"
            }
            
            response = requests.post(self.url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('results', [{}])[0].get('generated_text', 'No response generated')
            else:
                print(f"Watsonx API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error calling Watsonx API: {str(e)}")
            return None
    
    def test_connection(self) -> bool:
        """
        Test the connection to Watsonx API
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model_id': 'mixtral-8x7b-instruct-v0-q',
                'parameters': {
                    'max_new_tokens': 10,
                    'temperature': 0.1
                },
                'project_id': self.project_id,
                'prompt': "Test connection"
            }
            
            response = requests.post(self.url, headers=headers, json=data, timeout=10)
            return response.status_code == 200
            
        except Exception as e:
            print(f"Connection test failed: {str(e)}")
            return False

def validate_pdf_file(file_path: str) -> bool:
    """
    Validate if a file is a valid PDF
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        bool: True if valid PDF, False otherwise
    """
    try:
        if not file_path.lower().endswith('.pdf'):
            return False
        
        # Check if file exists and is readable
        if not os.path.exists(file_path) or not os.access(file_path, os.R_OK):
            return False
        
        # Check file size (max 900MB)
        file_size = os.path.getsize(file_path)
        if file_size > 900 * 1024 * 1024:  # 900MB
            return False
        
        return True
        
    except Exception:
        return False

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks for better processing
    
    Args:
        text (str): Input text to chunk
        chunk_size (int): Size of each chunk
        overlap (int): Overlap between chunks
        
    Returns:
        List[str]: List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # Try to break at sentence boundary
        if end < len(text):
            # Look for sentence endings
            for i in range(end, max(start, end - 100), -1):
                if text[i] in '.!?':
                    end = i + 1
                    break
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - overlap
        if start >= len(text):
            break
    
    return chunks

def extract_metadata_from_filename(filename: str) -> Dict[str, str]:
    """
    Extract metadata from filename
    
    Args:
        filename (str): Name of the file
        
    Returns:
        Dict[str, str]: Dictionary of metadata
    """
    metadata = {
        'filename': filename,
        'extension': '',
        'name_without_ext': '',
        'size_category': 'unknown'
    }
    
    if '.' in filename:
        name_parts = filename.rsplit('.', 1)
        metadata['name_without_ext'] = name_parts[0]
        metadata['extension'] = name_parts[1].lower()
    
    # Categorize by size
    if 'small' in filename.lower() or 'mini' in filename.lower():
        metadata['size_category'] = 'small'
    elif 'large' in filename.lower() or 'big' in filename.lower():
        metadata['size_category'] = 'large'
    else:
        metadata['size_category'] = 'medium'
    
    return metadata

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes (int): Size in bytes
        
    Returns:
        str: Formatted size string
    """
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe storage
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Sanitized filename
    """
    # Remove or replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    
    # Limit length
    if len(filename) > 100:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:95] + '.' + ext if ext else name[:100]
    
    return filename

def get_environment_info() -> Dict[str, str]:
    """
    Get information about the current environment
    
    Returns:
        Dict[str, str]: Environment information
    """
    return {
        'python_version': os.sys.version,
        'platform': os.sys.platform,
        'working_directory': os.getcwd(),
        'env_file_exists': os.path.exists('.env'),
        'watsonx_configured': bool(os.getenv('WATSONX_API_KEY')),
        'huggingface_configured': bool(os.getenv('HUGGINGFACE_API_TOKEN'))
    }
