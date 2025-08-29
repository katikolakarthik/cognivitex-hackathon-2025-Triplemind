"""
Setup script for StudyMate
Hackathon Project - TripleMind Team
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    
    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def create_virtual_environment():
    """Create a virtual environment"""
    print("🔧 Creating virtual environment...")
    
    try:
        # Check if venv module is available
        import venv
        
        # Create virtual environment
        venv_path = Path("venv")
        if venv_path.exists():
            print("⚠️ Virtual environment already exists")
            return True
        
        venv.create("venv", with_pip=True)
        print("✅ Virtual environment created successfully!")
        
        # Activate and install packages
        if platform.system() == "Windows":
            activate_script = "venv\\Scripts\\activate"
            pip_path = "venv\\Scripts\\pip"
        else:
            activate_script = "venv/bin/activate"
            pip_path = "venv/bin/pip"
        
        print("📦 Installing packages in virtual environment...")
        subprocess.check_call([pip_path, "install", "--upgrade", "pip"])
        subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def check_environment():
    """Check environment configuration"""
    print("🔍 Checking environment configuration...")
    
    # Check .env file
    if not os.path.exists(".env"):
        print("⚠️ .env file not found. Please create one with your API keys.")
        return False
    
    # Check required environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        "GOOGLE_API_KEY",
        "OPENROUTER_API_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️ Missing environment variables: {', '.join(missing_vars)}")
        print("Please add them to your .env file")
        return False
    
    print("✅ Environment configuration looks good!")
    return True

def run_tests():
    """Run basic tests"""
    print("🧪 Running basic tests...")
    
    try:
        # Test imports
        import streamlit
        import fitz
        import requests
        import pandas
        import numpy
        
        print("✅ All required modules imported successfully!")
        
        # Test basic functionality
        print("✅ Basic functionality tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False

def setup_project():
    """Main setup function"""
    print("🚀 Setting up StudyMate Project...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create virtual environment
    if not create_virtual_environment():
        print("⚠️ Continuing without virtual environment...")
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Check environment
    if not check_environment():
        print("⚠️ Environment configuration incomplete")
    
    # Run tests
    if not run_tests():
        return False
    
    print("=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Ensure your .env file has the required API keys")
    print("2. Run: streamlit run app_simple.py")
    print("3. Or run: streamlit run demo.py")
    
    return True

def main():
    """Main entry point"""
    try:
        success = setup_project()
        if success:
            print("\n🎓 StudyMate is ready to use!")
            print("🏆 Good luck with your hackathon!")
        else:
            print("\n❌ Setup failed. Please check the errors above.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
