"""
StudyMate Advanced IBM Watsonx Client
Integration with IBM Watsonx AI for LLM responses
Hackathon Project - TripleMind Team
"""

import os
import requests
import json
import time
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WatsonxClient:
    """Client for IBM Watsonx AI API with IBM Granite models"""
    
    def __init__(self):
        """Initialize Watsonx client with API credentials"""
        self.api_key = os.getenv('WATSONX_API_KEY')
        self.project_id = os.getenv('WATSONX_PROJECT_ID')
        self.url = os.getenv('WATSONX_URL')
        
        # Model configuration
        self.model_id = os.getenv('LLM_MODEL', 'ibm/granite-3-3-8b-instruct')
        self.max_tokens = int(os.getenv('MAX_TOKENS', 300))
        self.temperature = float(os.getenv('TEMPERATURE', 0.5))
        
        # Rate limiting configuration
        self.max_retries = 3
        self.retry_delay = 2  # seconds
        
        # Validate configuration
        if not all([self.api_key, self.project_id, self.url]):
            raise ValueError("Watsonx API configuration incomplete. Please check your .env file")
    
    def _get_auth_token(self) -> str:
        """Get IBM Cloud authentication token"""
        auth_url = "https://iam.cloud.ibm.com/identity/token"
        auth_data = {
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": self.api_key
        }
        
        response = requests.post(auth_url, data=auth_data)
        response.raise_for_status()
        
        return response.json()["access_token"]
    
    def generate_response(self, prompt: str, context: str = "") -> Dict[str, Any]:
        """Generate response using IBM Watsonx AI with rate limiting protection"""
        for attempt in range(self.max_retries):
            try:
                # Get authentication token
                token = self._get_auth_token()
                
                # Prepare the full prompt with context
                if context:
                    full_prompt = f"Context: {context}\n\nQuestion: {prompt}\n\nAnswer:"
                else:
                    full_prompt = f"Question: {prompt}\n\nAnswer:"
                
                # API endpoint
                api_url = f"{self.url}/ml/v1/text/generation?version=2024-11-19"
                
                # Request headers
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
                
                # Request body
                payload = {
                    "model_id": self.model_id,
                    "input": full_prompt,
                    "parameters": {
                        "max_new_tokens": self.max_tokens,
                        "temperature": self.temperature,
                        "top_p": 0.9,
                        "repetition_penalty": 1.1
                    },
                    "project_id": self.project_id
                }
                
                # Make API request
                response = requests.post(api_url, headers=headers, json=payload)
                
                # Handle rate limiting
                if response.status_code == 429:
                    if attempt < self.max_retries - 1:
                        wait_time = self.retry_delay * (2 ** attempt)  # Exponential backoff
                        print(f"⚠️ Rate limited (429). Waiting {wait_time} seconds before retry {attempt + 1}/{self.max_retries}")
                        time.sleep(wait_time)
                        continue
                    else:
                        return {
                            "success": False,
                            "error": "Rate limit exceeded. Please wait a few minutes before trying again.",
                            "raw_response": None
                        }
                
                response.raise_for_status()
                result = response.json()
                
                # Extract the generated text
                if "results" in result and len(result["results"]) > 0:
                    generated_text = result["results"][0].get("generated_text", "")
                    return {
                        "success": True,
                        "response": generated_text,
                        "model": self.model_id,
                        "tokens_used": result.get("usage", {}).get("total_tokens", 0),
                        "raw_response": result
                    }
                else:
                    return {
                        "success": False,
                        "error": "No response generated",
                        "raw_response": result
                    }
                    
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    if attempt < self.max_retries - 1:
                        wait_time = self.retry_delay * (2 ** attempt)
                        print(f"⚠️ Rate limited (429). Waiting {wait_time} seconds before retry {attempt + 1}/{self.max_retries}")
                        time.sleep(wait_time)
                        continue
                    else:
                        return {
                            "success": False,
                            "error": "Rate limit exceeded. Please wait a few minutes before trying again.",
                            "raw_response": None
                        }
                else:
                    return {
                        "success": False,
                        "error": f"HTTP Error {e.response.status_code}: {e.response.text}",
                        "raw_response": None
                    }
            except requests.exceptions.RequestException as e:
                return {
                    "success": False,
                    "error": f"API request failed: {str(e)}",
                    "raw_response": None
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Unexpected error: {str(e)}",
                    "raw_response": None
                }
        
        return {
            "success": False,
            "error": "Max retries exceeded",
            "raw_response": None
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """Test the Watsonx connection and model availability"""
        try:
            # Simple test prompt
            test_prompt = "Hello, this is a test. Please respond with 'Connection successful!'"
            result = self.generate_response(test_prompt)
            
            if result["success"]:
                return {
                    "status": "success",
                    "message": "Watsonx connection and model working correctly",
                    "model": self.model_id,
                    "response": result["response"]
                }
            else:
                return {
                    "status": "error",
                    "message": f"Model test failed: {result.get('error', 'Unknown error')}",
                    "model": self.model_id
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Connection test failed: {str(e)}",
                "model": self.model_id
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the configured model"""
        return {
            "model_id": self.model_id,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "api_url": self.url,
            "project_id": self.project_id
        }
    
    def update_parameters(self, max_tokens: Optional[int] = None, temperature: Optional[float] = None):
        """Update generation parameters"""
        if max_tokens is not None:
            self.max_tokens = max_tokens
            print(f"📝 Updated max_tokens to: {max_tokens}")
        
        if temperature is not None:
            self.temperature = temperature
            print(f"🌡️ Updated temperature to: {temperature}")
