#!/bin/bash

# NonLogs - Quick Deployment to Netlify
# This script automates the setup process

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   NonLogs - Quick Deploy to Netlify                           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if Node is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

echo "✓ Git and Node.js detected"
echo ""

# 1. Initialize Git
echo "📦 Step 1: Initializing Git repository..."
if [ ! -d .git ]; then
    git init
    echo "✓ Git initialized"
else
    echo "✓ Git repository already exists"
fi
echo ""

# 2. Add files
echo "📝 Step 2: Adding files to Git..."
git add .
git commit -m "NonLogs full stack - ready for Netlify deployment" || true
echo "✓ Files staged"
echo ""

# 3. Check if Netlify CLI is installed
echo "🔧 Step 3: Checking Netlify CLI..."
if ! command -v netlify &> /dev/null; then
    echo "📥 Installing Netlify CLI..."
    npm install -g netlify-cli
    echo "✓ Netlify CLI installed"
else
    echo "✓ Netlify CLI already installed"
fi
echo ""

# 4. Authenticate with Netlify
echo "🔐 Step 4: Authenticating with Netlify..."
echo "A browser window will open. Log in to your Netlify account."
echo "Press Enter to continue..."
read

netlify login
echo "✓ Authenticated with Netlify"
echo ""

# 5. Create netlify site
echo "🌐 Step 5: Creating Netlify site..."
netlify sites:create --name nonlogs-exchange
echo "✓ Netlify site created"
echo ""

# 6. Deploy
echo "🚀 Step 6: Deploying to Netlify..."
netlify deploy --prod \
  --dir=public \
  --functions=netlify/functions \
  --message="NonLogs Full Stack Deployment"
echo "✓ Deployed!"
echo ""

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   ✅ Deployment Complete!                                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Next Steps:"
echo "1. Open your site in the browser"
echo "2. Go to Netlify Dashboard → Site Settings → Environment"
echo "3. Add environment variables:"
echo "   - SECRET_KEY"
echo "   - JWT_SECRET_KEY"
echo "   - DATABASE_URL"
echo "4. Configure your database (PostgreSQL recommended)"
echo "5. Test your API endpoints"
echo ""
echo "🎯 Your site is live at:"
netlify info --json 2>/dev/null | grep -o '"name":"[^"]*' || echo "Check your Netlify dashboard"
echo ""
