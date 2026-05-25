# Deployment Guide for House Price Prediction Model

This guide covers deploying your Flask application to various free platforms.

---

## 🚀 Option 1: Deploy to Render (Easiest & Recommended)

### Prerequisites
- GitHub account (free)
- Render account (free)
- Your project pushed to GitHub

### Step 1: Push to GitHub

```bash
# Initialize git (if not already done)
cd /workspaces/codespaces-blank/house_price_prediction
git init
git add .
git commit -m "Initial commit: House price prediction model"

# Add your GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/house-price-prediction.git
git branch -M main
git push -u origin main
```

### Step 2: Create Render Account
1. Go to https://render.com
2. Click "Sign up"
3. Sign up with GitHub (recommended for easy integration)

### Step 3: Deploy on Render

1. **In Render Dashboard:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `house-price-prediction` repo

2. **Configure the Service:**
   - **Name**: `house-price-prediction`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
   
3. **Environment Variables:**
   - Add `PYTHONUNBUFFERED=true` (helps with logging)

4. **Plan**: Select "Free"

5. Click "Create Web Service"

### Step 4: Monitor Deployment
- Render will automatically build and deploy
- Wait for "Live" status (usually 2-5 minutes)
- Your app URL will be: `https://house-price-prediction.onrender.com`

### Testing Your Deployment
```bash
# Health check
curl https://your-app-url.onrender.com/health

# Make a prediction
curl -X POST https://your-app-url.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [8.3252, 41.0, 6.984127, 1.023810, 322.0, 2.555556, 37.88, -122.23]}'
```

⚠️ **Note**: Free tier on Render goes to sleep after 15 minutes of inactivity. The first request will take ~30 seconds to wake up. Upgrade to paid plan to avoid this.

---

## 🐳 Option 2: Deploy to Railway

### Prerequisites
- GitHub account
- Railway account (free)

### Steps

1. **Create Railway Account**: https://railway.app
2. **Connect GitHub**: Link your GitHub account
3. **Create New Project**: Click "New Project"
4. **Deploy from GitHub**:
   - Select your `house-price-prediction` repo
   - Railway will auto-detect it's a Python project
5. **Set Start Command**:
   - In Railway dashboard, go to Variables
   - Add environment variable: `RAILWAY_START_CMD=gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
6. **Deploy**: Click "Deploy"

Your app will be live at a Railway-generated URL.

---

## ☁️ Option 3: Deploy to Google Cloud Run

### Prerequisites
- Google Cloud Account (free tier available)
- Google Cloud CLI installed
- Docker (for local testing)

### Steps

1. **Create Google Cloud Project**:
   ```bash
   gcloud projects create house-price-prediction
   gcloud config set project house-price-prediction
   ```

2. **Enable Cloud Run API**:
   ```bash
   gcloud services enable run.googleapis.com
   ```

3. **Build and Deploy**:
   ```bash
   gcloud run deploy house-price-prediction \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

4. Your app URL will be provided after deployment completes.

---

## 🎯 Option 4: Deploy to PythonAnywhere

### Steps

1. Go to https://www.pythonanywhere.com
2. Sign up for free account
3. Upload your files via "Files" section
4. Create a new web app:
   - Click "Web" → "Add a new web app"
   - Choose "Flask"
   - Choose Python 3.12
5. Configure WSGI file (will be auto-created)
6. Your app will be live at `https://yourusername.pythonanywhere.com`

---

## 🐳 Option 5: Deploy with Docker Locally

### Test Locally with Docker

```bash
# Build image
docker build -t house-price-prediction .

# Run container
docker run -p 5000:5000 house-price-prediction

# Test
curl http://localhost:5000/health
```

---

## 📋 Deployment Comparison

| Platform | Free Tier | Sleep Issue | Setup Time | Best For |
|----------|-----------|-------------|-----------|----------|
| **Render** | Yes (paid option better) | Yes (15 min) | 5 min | Quick demos |
| **Railway** | $5/month credit | No | 5 min | Small projects |
| **Google Cloud Run** | 2M requests/month | No | 10 min | Production |
| **PythonAnywhere** | Limited | No | 5 min | Beginners |

---

## 🔧 Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'sklearn'"
**Solution**: Ensure `requirements.txt` is in root directory and includes scikit-learn.

### Issue: Model not found error
**Solution**: The models are built at runtime. First deployment will take longer as it trains the model.

### Issue: Port conflicts
**Solution**: Don't hardcode port 5000. Use environment variable `$PORT` (Render/Railway do this automatically).

### Issue: Timeout during deployment
**Solution**: 
- Increase deployment timeout in platform settings
- Consider pre-training model locally and committing pickled files (add to .gitignore if large)

---

## 📈 Next Steps After Deployment

1. **Monitor Performance**: Check logs in your platform's dashboard
2. **Add Custom Domain**: Most platforms allow free custom domains
3. **Set Up Auto-Deploys**: Enable auto-deployment from GitHub (usually default)
4. **Add HTTPS**: All major platforms provide free SSL certificates
5. **Scale Up**: Upgrade to paid tier when ready for production

---

## 🎓 Additional Resources

- **Render Docs**: https://render.com/docs
- **Railway Docs**: https://docs.railway.app
- **Google Cloud Run**: https://cloud.google.com/run/docs
- **Flask Deployment**: https://flask.palletsprojects.com/deployment/

---

## ✅ Recommended Setup for Production

For the best free experience:
1. **Use Google Cloud Run** - Most generous free tier (2M requests/month)
2. **Enable auto-scaling** - Handles traffic spikes automatically
3. **Add monitoring** - Use built-in logs and metrics
4. **Set up alerts** - Get notified of errors

```bash
# Deploy to Google Cloud Run
gcloud run deploy house-price-prediction \
  --source . \
  --platform managed \
  --region us-central1 \
  --memory 1Gi \
  --allow-unauthenticated
```

That's it! Your model is now live. 🎉
