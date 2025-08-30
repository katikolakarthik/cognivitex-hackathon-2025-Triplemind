#!/usr/bin/env python3
"""
StudyMate Quick Deployment Script
TripleMind Team - Hackathon Project

Choose and deploy your preferred solution:
1. TripleMind MVP (Multi-Model AI)
2. StudyMate Advanced (RAG System)
"""

import streamlit as st
import subprocess
import sys
import os
from pathlib import Path

def main():
    """Main deployment selection interface"""
    
    st.set_page_config(
        page_title="StudyMate Deployment - TripleMind Team",
        page_icon="🚀",
        layout="wide"
    )
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0;">🚀 StudyMate Deployment</h1>
        <p style="color: white; font-size: 1.2rem; margin: 0.5rem 0;">Choose Your Solution - TripleMind Team</p>
        <p style="color: white; margin: 0;"><strong>Hackathon Project - Ready to Deploy!</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Solution Selection
    st.header("🎯 **Choose Your Deployment Solution**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🧠 **TripleMind MVP**
        
        **Multi-Model AI Solution**
        - 3 AI models working together
        - Citation system with page references
        - Production-ready interface
        - Cost-optimized API usage
        
        **Best for:**
        - Immediate deployment
        - Multi-model AI showcase
        - Academic integrity focus
        """)
        
        if st.button("🚀 Deploy TripleMind MVP", type="primary", use_container_width=True):
            deploy_triplemind()
    
    with col2:
        st.markdown("""
        ### 🚀 **StudyMate Advanced**
        
        **Enterprise-Grade RAG System**
        - Advanced vector search (FAISS)
        - IBM Watsonx integration
        - Semantic embeddings
        - Sub-100ms performance
        
        **Best for:**
        - Cutting-edge technology
        - Enterprise applications
        - Research and development
        """)
        
        if st.button("🚀 Deploy StudyMate Advanced", type="primary", use_container_width=True):
            deploy_advanced()
    
    st.markdown("---")
    
    # Deployment Information
    st.header("📋 **Deployment Information**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🌐 **Streamlit Cloud URLs**
        
        After deployment, your apps will be available at:
        
        **TripleMind MVP:**
        `https://studymate-triplemind.streamlit.app`
        
        **StudyMate Advanced:**
        `https://studymate-advanced.streamlit.app`
        
        ### 🔧 **Requirements**
        
        - GitHub repository connected
        - API keys configured
        - Dependencies installed
        """)
    
    with col2:
        st.markdown("""
        ### 📊 **What You'll Get**
        
        **Professional Apps:**
        - Live, accessible URLs
        - Automatic updates
        - Professional branding
        - Hackathon-ready demos
        
        **Technical Benefits:**
        - Production deployment
        - Performance monitoring
        - Error logging
        - Scalable hosting
        """)
    
    # Quick Start Guide
    st.markdown("---")
    st.header("⚡ **Quick Start Guide**")
    
    with st.expander("🚀 **Deploy to Streamlit Cloud (Recommended)**"):
        st.markdown("""
        1. **Visit [Streamlit Cloud](https://streamlit.io/cloud)**
        2. **Sign in with GitHub**
        3. **Click 'New app'**
        4. **Select your repository: `yourusername/StudyMate_Hackathon`**
        5. **Choose main file:**
           - TripleMind MVP: `deploy_triplemind.py`
           - StudyMate Advanced: `StudyMate_Advanced/deploy_advanced.py`
        6. **Configure environment variables in Settings → Secrets**
        7. **Click Deploy!**
        """)
    
    with st.expander("🔧 **Local Deployment**"):
        st.markdown("""
        **For TripleMind MVP:**
        ```bash
        streamlit run deploy_triplemind.py
        ```
        
        **For StudyMate Advanced:**
        ```bash
        cd StudyMate_Advanced
        streamlit run deploy_advanced.py
        ```
        """)
    
    with st.expander("🔑 **Environment Variables**"):
        st.markdown("""
        **TripleMind MVP:**
        ```env
        GOOGLE_API_KEY=your_key
        OPENROUTER_API_KEY=your_key
        HUGGINGFACE_API_TOKEN=your_token
        ```
        
        **StudyMate Advanced:**
        ```env
        WATSONX_API_KEY=your_key
        WATSONX_PROJECT_ID=your_id
        WATSONX_URL=https://us-south.ml.cloud.ibm.com
        ```
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: #f0f2f6; border-radius: 10px;">
        <p><strong>🚀 StudyMate Deployment</strong> - Ready to showcase your TripleMind innovation!</p>
        <p>🏆 <strong>Hackathon Project</strong> - Built by TripleMind Team</p>
    </div>
    """, unsafe_allow_html=True)

def deploy_triplemind():
    """Deploy TripleMind MVP solution"""
    st.success("🧠 **Deploying TripleMind MVP...**")
    
    st.info("""
    **Next Steps:**
    
    1. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**
    2. **Create new app with these settings:**
       - Repository: `yourusername/StudyMate_Hackathon`
       - Branch: `main`
       - Main file path: `deploy_triplemind.py`
    
    3. **Configure environment variables in Settings → Secrets:**
       ```toml
       GOOGLE_API_KEY = "your_google_api_key"
       OPENROUTER_API_KEY = "your_openrouter_api_key"
       HUGGINGFACE_API_TOKEN = "your_huggingface_token"
       ```
    
    4. **Click Deploy!**
    
    Your TripleMind MVP will be available at: `https://studymate-triplemind.streamlit.app`
    """)

def deploy_advanced():
    """Deploy StudyMate Advanced solution"""
    st.success("🚀 **Deploying StudyMate Advanced...**")
    
    st.info("""
    **Next Steps:**
    
    1. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**
    2. **Create new app with these settings:**
       - Repository: `yourusername/StudyMate_Hackathon`
       - Branch: `main`
       - Main file path: `StudyMate_Advanced/deploy_advanced.py`
    
    3. **Configure environment variables in Settings → Secrets:**
       ```toml
       WATSONX_API_KEY = "your_ibm_watsonx_api_key"
       WATSONX_PROJECT_ID = "your_project_id"
       WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
       ```
    
    4. **Click Deploy!**
    
    Your StudyMate Advanced will be available at: `https://studymate-advanced.streamlit.app`
    """)

if __name__ == "__main__":
    main()
