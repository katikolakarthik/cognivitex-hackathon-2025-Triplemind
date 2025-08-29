import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test Google Gemini API"""
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in .env file")
        return False
    
    print(f"✅ Gemini API Key found: {api_key[:20]}...")
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [{
            "parts": [{
                "text": "Hello, this is a test message."
            }]
        }]
    }
    
    try:
        response = requests.post(
            f"{url}?key={api_key}",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Google Gemini API is working!")
            return True
        else:
            print(f"❌ Gemini API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Gemini Connection Error: {e}")
        return False

def test_deepseek_api():
    """Test DeepSeek API via OpenRouter"""
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in .env file")
        return False
    
    print(f"✅ OpenRouter API Key found: {api_key[:20]}...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://studymate-ai.com",
        "X-Title": "StudyMate AI"
    }
    
    data = {
        "model": "deepseek/deepseek-chat-v3.1:free",
        "messages": [
            {"role": "user", "content": "Hello, this is a test message."}
        ]
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ DeepSeek API is working!")
            return True
        else:
            print(f"❌ DeepSeek API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ DeepSeek Connection Error: {e}")
        return False

def test_gpt_oss_api():
    """Test GPT-OSS-120B API via OpenRouter"""
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in .env file")
        return False
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://studymate-ai.com",
        "X-Title": "StudyMate AI"
    }
    
    data = {
        "model": "openai/gpt-oss-120b:free",
        "messages": [
            {"role": "user", "content": "Hello, this is a test message."}
        ]
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ GPT-OSS-120B API is working!")
            return True
        else:
            print(f"❌ GPT-OSS API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ GPT-OSS Connection Error: {e}")
        return False

def main():
    print("🧠 Testing TripleMind AI Models...")
    print("=" * 50)
    
    # Test all three models
    gemini_ok = test_gemini_api()
    print()
    
    deepseek_ok = test_deepseek_api()
    print()
    
    gpt_oss_ok = test_gpt_oss_api()
    print()
    
    # Summary
    print("=" * 50)
    print("🧠 TripleMind Test Results:")
    print(f"📚 Google Gemini: {'✅ Working' if gemini_ok else '❌ Failed'}")
    print(f"🌍 DeepSeek AI: {'✅ Working' if deepseek_ok else '❌ Failed'}")
    print(f"🤖 GPT-OSS-120B: {'✅ Working' if gpt_oss_ok else '❌ Failed'}")
    
    working_models = sum([gemini_ok, deepseek_ok, gpt_oss_ok])
    print(f"\n🎯 Total Working Models: {working_models}/3")
    
    if working_models == 3:
        print("🎉 All TripleMind models are ready!")
    elif working_models >= 2:
        print("👍 Most models are working!")
    else:
        print("⚠️ Some models need attention.")

if __name__ == "__main__":
    main()
