# 🚀 StudyMate Deployment Guide

**TripleMind Team - Hackathon Project**

This guide will help you deploy both **TripleMind MVP** and **StudyMate Advanced** solutions to Streamlit Cloud.

## 📋 **Deployment Overview**

We're deploying **TWO complete solutions**:

1. **🧠 TripleMind MVP** - Multi-model AI solution with citations
2. **🚀 StudyMate Advanced** - Enterprise-grade RAG system

## 🎯 **Deployment Options**

### **Option 1: Streamlit Cloud (Recommended for Hackathon)**

- **Free hosting** for hackathon projects
- **Easy deployment** with GitHub integration
- **Professional URLs** for demo purposes
- **Automatic updates** when you push to GitHub

### **Option 2: Local Deployment**

- **Full control** over the environment
- **All features** available
- **API keys** properly configured
- **Development and testing**

## 🚀 **Streamlit Cloud Deployment**

### **Step 1: Prepare Your Repository**

1. **Ensure your code is on GitHub**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Verify file structure**
   ```
   StudyMate_Hackathon/
   ├── deploy_triplemind.py          # TripleMind MVP deployment
   ├── StudyMate_Advanced/
   │   └── deploy_advanced.py        # StudyMate Advanced deployment
   ├── .streamlit/
   │   └── config.toml               # Streamlit configuration
   ├── requirements.txt               # Dependencies
   └── README.md                     # Project documentation
   ```

### **Step 2: Deploy to Streamlit Cloud**

1. **Visit [Streamlit Cloud](https://streamlit.io/cloud)**
2. **Sign in with GitHub**
3. **Click "New app"**
4. **Configure your app:**

#### **For TripleMind MVP:**
   - **Repository**: `yourusername/StudyMate_Hackathon`
   - **Branch**: `main`
   - **Main file path**: `deploy_triplemind.py`
   - **App URL**: `https://studymate-triplemind.streamlit.app`

#### **For StudyMate Advanced:**
   - **Repository**: `yourusername/StudyMate_Hackathon`
   - **Branch**: `main`
   - **Main file path**: `StudyMate_Advanced/deploy_advanced.py`
   - **App URL**: `https://studymate-advanced.streamlit.app`

### **Step 3: Configure Environment Variables**

In Streamlit Cloud, go to **Settings → Secrets** and add:

```toml
# For TripleMind MVP
GOOGLE_API_KEY = "your_google_api_key"
OPENROUTER_API_KEY = "your_openrouter_api_key"
HUGGINGFACE_API_TOKEN = "your_huggingface_token"

# For StudyMate Advanced
WATSONX_API_KEY = "your_ibm_watsonx_api_key"
WATSONX_PROJECT_ID = "your_project_id"
WATSONX_URL = "https://us-south.ml.cloud.ibm.com"

# Common settings
MAX_FILE_SIZE = "50"
MAX_CHUNK_SIZE = "1000"
CHUNK_OVERLAP = "200"
```

### **Step 4: Deploy and Test**

1. **Click "Deploy"**
2. **Wait for deployment to complete**
3. **Test your app with sample PDFs**
4. **Verify all features are working**

## 🔧 **Local Deployment**

### **Prerequisites**

- Python 3.8+
- All required packages installed
- API keys configured in `.env` files

### **Deploy TripleMind MVP**

```bash
# Navigate to project directory
cd StudyMate_Hackathon

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys

# Run TripleMind MVP
streamlit run deploy_triplemind.py
```

### **Deploy StudyMate Advanced**

```bash
# Navigate to StudyMate Advanced directory
cd StudyMate_Advanced

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your IBM Watsonx credentials

# Run StudyMate Advanced
streamlit run deploy_advanced.py
```

## 📊 **Deployment Verification**

### **TripleMind MVP Checklist**

- [ ] **Multi-Model AI**: All 3 AI models responding
- [ ] **Citation System**: Page references working
- [ ] **File Upload**: PDF processing successful
- [ ] **Question Handling**: Natural language Q&A working
- [ ] **Fallback Mechanisms**: Error handling functional

### **StudyMate Advanced Checklist**

- [ ] **RAG System**: Vector search operational
- [ ] **IBM Watsonx**: API integration working
- [ ] **FAISS**: Vector database functional
- [ ] **Performance**: <100ms search times
- [ ] **Multi-Document**: Multiple PDF support

## 🌐 **Public URLs for Hackathon**

After deployment, you'll have:

1. **🧠 TripleMind MVP**: `https://studymate-triplemind.streamlit.app`
2. **🚀 StudyMate Advanced**: `https://studymate-advanced.streamlit.app`

## 🎯 **Hackathon Demo Strategy**

### **Quick Demo (2 minutes)**
1. **Show TripleMind MVP**: Upload PDF, ask question
2. **Highlight Multi-Model**: Explain 3 AI models working together
3. **Demonstrate Citations**: Show source tracking

### **Advanced Demo (5 minutes)**
1. **Compare Both Solutions**: Show MVP vs Advanced
2. **Technical Deep Dive**: Explain RAG vs Multi-Model
3. **Performance Metrics**: Demonstrate speed and accuracy

### **Technical Q&A (3 minutes)**
1. **Architecture**: Explain dual solution approach
2. **Innovation**: Highlight TripleMind concept
3. **Scalability**: Show production readiness

## 🚨 **Troubleshooting**

### **Common Issues**

1. **Import Errors**: Check requirements.txt and dependencies
2. **API Errors**: Verify environment variables and API keys
3. **File Upload Issues**: Check file size limits and formats
4. **Performance Issues**: Monitor API rate limits

### **Solutions**

1. **Restart Deployment**: Sometimes fixes import issues
2. **Check Logs**: Streamlit Cloud provides detailed error logs
3. **Verify Secrets**: Ensure environment variables are set correctly
4. **Test Locally**: Debug issues in local environment first

## 📈 **Performance Optimization**

### **For Streamlit Cloud**

1. **Efficient Imports**: Only import what's needed
2. **Caching**: Use `@st.cache_data` for expensive operations
3. **Lazy Loading**: Load components only when needed
4. **Error Handling**: Graceful degradation for API failures

### **For Production**

1. **Rate Limiting**: Implement API call throttling
2. **Monitoring**: Track performance metrics
3. **Scaling**: Plan for increased usage
4. **Security**: Implement proper authentication

## 🎉 **Success Metrics**

### **Deployment Success**

- [ ] Both apps accessible via public URLs
- [ ] All features functional in cloud environment
- [ ] Performance meets hackathon requirements
- [ ] Professional appearance and branding

### **Hackathon Impact**

- [ ] **Innovation**: TripleMind concept clearly demonstrated
- [ ] **Technical Depth**: Both solutions showcase different approaches
- [ ] **Production Ready**: Apps can be used immediately
- [ ] **Documentation**: Clear setup and usage instructions

## 🏆 **TripleMind Team Achievement**

By successfully deploying both solutions, you demonstrate:

1. **🚀 Technical Versatility**: MVP + Advanced implementation
2. **🧠 Innovation**: Multi-model AI orchestration
3. **📚 Academic Focus**: Student-centric solutions
4. **⚡ Production Ready**: Deployable applications
5. **🎯 Hackathon Excellence**: Comprehensive project delivery

---

**🚀 Ready to Deploy? Follow this guide and showcase your TripleMind innovation to the world!**

**Built with ❤️ by TripleMind Team**
