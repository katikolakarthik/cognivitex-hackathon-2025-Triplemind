"""
StudyMate Advanced Test Script
Test the advanced RAG system components
Hackathon Project - TripleMind Team
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing module imports...")
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import fitz
        print("✅ PyMuPDF imported successfully")
    except ImportError as e:
        print(f"❌ PyMuPDF import failed: {e}")
        return False
    
    try:
        import sentence_transformers
        print("✅ SentenceTransformers imported successfully")
    except ImportError as e:
        print(f"❌ SentenceTransformers import failed: {e}")
        return False
    
    try:
        import faiss
        print("✅ FAISS imported successfully")
    except ImportError as e:
        print(f"❌ FAISS import failed: {e}")
        return False
    
    try:
        import numpy
        print("✅ NumPy imported successfully")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    try:
        import pandas
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    return True

def test_environment():
    """Test environment configuration"""
    print("\n🔧 Testing environment configuration...")
    
    required_vars = [
        'WATSONX_API_KEY',
        'WATSONX_PROJECT_ID', 
        'WATSONX_URL'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("💡 Please check your .env file")
        return False
    else:
        print("✅ All required environment variables found")
        return True

def test_custom_modules():
    """Test custom module imports"""
    print("\n📦 Testing custom modules...")
    
    try:
        from rag_engine import AdvancedRAGEngine
        print("✅ AdvancedRAGEngine imported successfully")
    except ImportError as e:
        print(f"❌ AdvancedRAGEngine import failed: {e}")
        return False
    
    try:
        from watsonx_client import WatsonxClient
        print("✅ WatsonxClient imported successfully")
    except ImportError as e:
        print(f"❌ WatsonxClient import failed: {e}")
        return False
    
    return True

def test_rag_engine_initialization():
    """Test RAG engine initialization"""
    print("\n🔍 Testing RAG engine initialization...")
    
    try:
        from rag_engine import AdvancedRAGEngine
        
        # Initialize RAG engine
        rag_engine = AdvancedRAGEngine()
        print("✅ RAG Engine initialized successfully")
        
        # Get statistics
        stats = rag_engine.get_statistics()
        print(f"📊 RAG Engine stats: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ RAG Engine initialization failed: {e}")
        return False

def test_watsonx_client():
    """Test Watsonx client initialization"""
    print("\n🧠 Testing Watsonx client...")
    
    try:
        from watsonx_client import WatsonxClient
        
        # Initialize client
        client = WatsonxClient()
        print("✅ Watsonx client initialized successfully")
        
        # Get model info
        model_info = client.get_model_info()
        print(f"📋 Model info: {model_info}")
        
        return True
        
    except Exception as e:
        print(f"❌ Watsonx client initialization failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 StudyMate Advanced - System Test")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Environment Configuration", test_environment),
        ("Custom Modules", test_custom_modules),
        ("RAG Engine", test_rag_engine_initialization),
        ("Watsonx Client", test_watsonx_client)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("💡 Run 'streamlit run app_advanced.py' to start the application.")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        print("💡 Make sure all dependencies are installed and environment is configured.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
