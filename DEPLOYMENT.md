# 🚀 Deployment Guide - Multiple Free Options

## Option 1: Streamlit Community Cloud (EASIEST - RECOMMENDED)

### Steps:
1. **Push your code to GitHub** (make sure it's public)
2. **Go to [share.streamlit.io](https://share.streamlit.io)**
3. **Sign in with GitHub**
4. **Click "Deploy an app"**
5. **Select your repository: `BRoliix/DoofenshmirtzEvil`**
6. **Set Main file path: `main.py`**
7. **Click "Deploy!"**

### Requirements:
- Uses `requirements_streamlit.txt` (already created)
- Automatically detects Python version from `runtime.txt`
- No additional configuration needed

---

## Option 2: Render (FLEXIBLE ALTERNATIVE)

### Steps:
1. **Push code to GitHub**
2. **Go to [render.com](https://render.com)**
3. **Sign up/Login with GitHub**
4. **Click "New +"** → **"Web Service"**
5. **Connect your `DoofenshmirtzEvil` repository**
6. **Settings:**
   - **Name:** `phishing-simulator`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run main.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`
7. **Click "Create Web Service"**

### Features:
- 750 hours/month free
- Custom domains
- Environment variables
- Database options

---

## Option 3: Heroku (CLASSIC CHOICE)

### Steps:
1. **Install Heroku CLI**
2. **Login:** `heroku login`
3. **Create app:** `heroku create your-app-name`
4. **Deploy:** 
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### Uses:
- `Procfile` (already created)
- `requirements.txt` (already created)
- `runtime.txt` (already created)

---

## Option 4: Hugging Face Spaces (AI-FOCUSED)

### Steps:
1. **Go to [huggingface.co/spaces](https://huggingface.co/spaces)**
2. **Create new Space**
3. **Select Streamlit SDK**
4. **Upload your files or connect GitHub**
5. **Auto-deploys from `app.py` or `main.py`**

---

## 🎯 RECOMMENDED: Streamlit Community Cloud

**Why?** 
- ✅ Built specifically for Streamlit apps
- ✅ Completely free forever
- ✅ Easy GitHub integration
- ✅ Perfect for your use case
- ✅ No configuration headaches

**Just push to GitHub and deploy in 2 minutes!**