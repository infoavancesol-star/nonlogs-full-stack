# 🚀 NonLogs - Complete Deployment Guide for Netlify

## Overview
This guide walks you through deploying your merged NonLogs application (Frontend + Backend) to Netlify.

---

## 📋 Prerequisites

1. **GitHub Account** - Required for CI/CD integration
2. **Netlify Account** - Create at https://app.netlify.com/signup
3. **Git installed locally** - https://git-scm.com/downloads
4. **Basic command line knowledge**

---

## 🔧 Step 1: Prepare Your Project

### 1.1 Initialize Git Repository
```bash
cd nonlogs-full-stack
git init
git add .
git commit -m "Initial commit: Frontend and Backend merged"
```

### 1.2 Create GitHub Repository
1. Go to https://github.com/new
2. Name it: `nonlogs-full-stack`
3. Add description: "NonLogs Crypto Exchange - Full Stack App"
4. Choose "Public" or "Private"
5. Click "Create Repository"

### 1.3 Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/nonlogs-full-stack.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

---

## 🚀 Step 2: Deploy to Netlify

### Option A: Automatic Deployment (Recommended)

#### 2.1 Connect GitHub to Netlify
1. Go to https://app.netlify.com
2. Click **"New site from Git"**
3. Click **"GitHub"**
4. Authorize Netlify to access your GitHub account
5. Select your `nonlogs-full-stack` repository
6. Click **"Deploy site"**

#### 2.2 Configure Build Settings
Netlify should auto-detect settings. If not, set:
- **Build command:** `npm run build`
- **Publish directory:** `public`
- **Functions directory:** `netlify/functions`

#### 2.3 Add Environment Variables
1. In Netlify Dashboard, go to **Site Settings** → **Build & Deploy** → **Environment**
2. Click **"Edit Variables"**
3. Add the following:

```
SECRET_KEY = your-super-secret-key-123456789
JWT_SECRET_KEY = your-jwt-secret-key-987654321
FLASK_ENV = production
DEBUG = False
DATABASE_URL = postgresql://user:password@host:5432/dbname
```

**Important:** Generate secure secret keys:
```bash
# On Linux/Mac
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

### Option B: Manual Deployment with Netlify CLI

#### 2.1 Install Netlify CLI
```bash
npm install -g netlify-cli
```

#### 2.2 Authenticate with Netlify
```bash
netlify login
```

#### 2.3 Deploy
```bash
cd nonlogs-full-stack
netlify deploy --prod
```

---

## 🗄️ Step 3: Database Setup

### Important: Choose Your Database

**For Production (Recommended):**
Use PostgreSQL on a service like:
- Heroku Postgres
- AWS RDS
- Railway.app
- Neon
- Supabase

**Steps:**
1. Sign up for a database service
2. Create a new PostgreSQL database
3. Copy the connection string
4. Add to Netlify environment variables as `DATABASE_URL`
5. Update the SQLAlchemy URI in your app

**For Development:**
SQLite is fine, but **NOT for production**.

### Example: Using Supabase (Free)
1. Go to https://supabase.com
2. Sign up with GitHub
3. Create a new project
4. Go to **Settings** → **Database** → copy JDBC connection string
5. Format: `postgresql://postgres:PASSWORD@HOST:5432/postgres`
6. Add to Netlify environment variables

---

## 🔐 Step 4: Security Configuration

### 4.1 CORS Settings
Update your backend to accept your Netlify domain:

In `api/app.py`, update CORS:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.netlify.app"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

### 4.2 Environment Variables
- **Never** commit `.env` file
- Always use Netlify's environment variables dashboard
- Rotate keys regularly

### 4.3 API Key Best Practices
- Use `python3 -c "import secrets; print(secrets.token_urlsafe(32))"` to generate keys
- Store all keys in Netlify's dashboard
- Don't share your keys

---

## 🧪 Step 5: Testing Your Deployment

### Test the Frontend
```
https://yourdomain.netlify.app
```

### Test the API Health Check
```
https://yourdomain.netlify.app/api/health
```

### Test Authentication (Register)
```bash
curl -X POST https://yourdomain.netlify.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Check Netlify Logs
1. Go to **Site Settings** → **Functions** in Netlify Dashboard
2. Click **View function logs**
3. Check for any errors

---

## 📱 Custom Domain Setup

1. In Netlify Dashboard: **Site Settings** → **Domain Management**
2. Click **Add Custom Domain**
3. Enter your domain (e.g., nonlogs.com)
4. Follow DNS setup instructions for your domain provider
5. Wait 24-48 hours for DNS propagation

---

## 🆘 Troubleshooting

### Issue: Functions returning 500 errors
- Check Netlify function logs
- Verify environment variables are set
- Ensure database connection is working

### Issue: CORS errors
- Update CORS settings in `api/app.py`
- Add Netlify domain to allowed origins
- Clear browser cache

### Issue: Database connection fails
- Verify DATABASE_URL format
- Check database service is running
- Confirm credentials in environment variables

### Issue: Static files not loading
- Ensure frontend files are in `public/` directory
- Check `netlify.toml` redirects are correct

---

## 📊 Monitoring & Logs

### View Logs
1. **Netlify Dashboard** → **Functions** → **View logs**
2. **Terminal:** `netlify logs --function api`

### Set up Alerts
1. **Site Settings** → **Build & Deploy** → **Deploy Notifications**
2. Add email or Slack notifications

---

## 🎯 Production Checklist

- [ ] Environment variables set in Netlify
- [ ] Database configured and connected
- [ ] CORS updated with production domain
- [ ] Custom domain configured
- [ ] SSL certificate installed (automatic with Netlify)
- [ ] API endpoints tested
- [ ] Frontend loads correctly
- [ ] Authentication working
- [ ] Error logs reviewed
- [ ] Backup strategy for database

---

## 📞 Support & Resources

- **Netlify Docs:** https://docs.netlify.com/
- **Flask Docs:** https://flask.palletsprojects.com/
- **Netlify Functions:** https://docs.netlify.com/functions/overview/
- **Common Issues:** https://docs.netlify.com/functions/troubleshooting/tips/

---

## 🎉 You're Deployed!

Your NonLogs application is now live on Netlify!

- **Frontend URL:** `https://yourdomain.netlify.app`
- **API Base URL:** `https://yourdomain.netlify.app/api`

---

## Next Steps

1. **Monitor Performance:** Check Netlify Analytics
2. **Scale Database:** Upgrade if needed
3. **Add Features:** Deploy updates via git push
4. **Backup Data:** Set up database backups
5. **Security:** Implement rate limiting and API keys

---

**Last Updated:** March 5, 2026
