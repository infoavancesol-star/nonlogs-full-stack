# NonLogs - Full Stack Crypto Exchange Platform

A complete, production-ready cryptocurrency exchange platform with merged frontend and backend, optimized for Netlify deployment.

## 📁 Project Structure

```
nonlogs-full-stack/
├── public/                 # Frontend (Static HTML/JS)
│   ├── index.html         # Main application page
│   └── js/
│       └── main.js        # Frontend JavaScript
├── api/                   # Backend (Python Flask)
│   ├── app.py            # Main Flask application
│   ├── config.py         # Configuration
│   ├── requirements.txt   # Python dependencies
│   ├── models/           # Database models
│   │   ├── user.py
│   │   ├── trade.py
│   │   ├── transaction.py
│   │   └── wallet.py
│   └── routes/           # API endpoints
│       ├── auth.py
│       ├── market.py
│       ├── trading.py
│       ├── user.py
│       └── wallet.py
├── netlify/functions/     # Netlify serverless functions
│   └── api.py            # Lambda handler for backend
├── netlify.toml          # Netlify configuration
├── package.json          # Node.js configuration
├── .env.example          # Environment variables template
├── NETLIFY_DEPLOYMENT_GUIDE.md
├── deploy.sh             # Quick deployment script
└── README.md             # This file
```

## 🚀 Quick Start (Netlify Deployment)

### Option 1: One-Click Script (Recommended)

```bash
chmod +x deploy.sh
./deploy.sh
```

This script will:
- Initialize Git repository
- Install Netlify CLI
- Authenticate with Netlify
- Deploy your site
- Show deployment status

### Option 2: Manual Setup

1. **Install Prerequisites:**
   ```bash
   # Install Node.js from https://nodejs.org
   # Install Git from https://git-scm.com
   ```

2. **Initialize Git:**
   ```bash
   cd nonlogs-full-stack
   git init
   git add .
   git commit -m "Initial commit"
   ```

3. **Create GitHub Repository:**
   - Go to https://github.com/new
   - Create repository `nonlogs-full-stack`
   - Run:
     ```bash
     git remote add origin https://github.com/YOUR_USERNAME/nonlogs-full-stack.git
     git branch -M main
     git push -u origin main
     ```

4. **Deploy to Netlify:**
   - Go to https://app.netlify.com
   - Click "New site from Git"
   - Select GitHub and authorize
   - Choose your repository
   - Click "Deploy site"

5. **Add Environment Variables:**
   - Go to Site Settings → Build & Deploy → Environment
   - Add:
     - `SECRET_KEY` - Generate: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`
     - `JWT_SECRET_KEY` - Generate same way
     - `DATABASE_URL` - Your PostgreSQL connection string

## 🔧 Local Development

### Backend Setup

```bash
# Navigate to api directory
cd api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp ../.env.example .env
# Edit .env with your settings

# Initialize database
python3
>>> from app import create_app
>>> app = create_app()
>>> exit()

# Run Flask server
python app.py
# Server runs at http://localhost:5000
```

### Frontend Setup

```bash
# Navigate to public directory
cd public

# Simple HTTP server (Python 3)
python3 -m http.server 8000
# Or with Node.js:
npx http-server

# Open browser to http://localhost:8000
```

## 📚 API Documentation

### Base URL
- **Local:** `http://localhost:5000/api`
- **Production:** `https://yourdomain.netlify.app/api`

### Authentication Endpoints

#### Register User
```bash
POST /api/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password",
  "wallet_address": "0x123..."  # Optional
}

Response: 201 Created
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "wallet_address": "0x123...",
    "created_at": "2024-03-05T12:00:00"
  }
}
```

#### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "secure_password"
}

Response: 200 OK
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": { ... }
}
```

#### Get Profile
```bash
GET /api/auth/profile
Authorization: Bearer <access_token>

Response: 200 OK
{
  "user": { ... }
}
```

### Cryptocurrency Endpoints

#### Get All Cryptocurrencies
```bash
GET /api/cryptocurrencies

Response: 200 OK
{
  "cryptocurrencies": [
    {
      "id": 1,
      "symbol": "BTC",
      "name": "Bitcoin",
      "price": 45000.00,
      "change_24h": 2.5,
      "market_cap": 900000000000,
      "updated_at": "2024-03-05T12:00:00"
    },
    ...
  ]
}
```

#### Get Specific Cryptocurrency
```bash
GET /api/cryptocurrencies/BTC

Response: 200 OK
{
  "cryptocurrency": { ... }
}
```

### Trading Endpoints

#### Create Trade
```bash
POST /api/trades
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "crypto_from": "BTC",
  "crypto_to": "ETH",
  "amount": 0.5,
  "price": 45000,
  "trade_type": "BUY"
}

Response: 201 Created
{
  "message": "Trade created successfully",
  "trade": { ... }
}
```

#### Get Trading History
```bash
GET /api/trades?page=1&per_page=20
Authorization: Bearer <access_token>

Response: 200 OK
{
  "trades": [...],
  "total": 50,
  "pages": 3,
  "current_page": 1
}
```

### Portfolio Endpoints

#### Get Portfolio
```bash
GET /api/portfolio
Authorization: Bearer <access_token>

Response: 200 OK
{
  "portfolio": [
    {
      "id": 1,
      "crypto": "BTC",
      "amount": 2.5,
      "average_price": 40000,
      "created_at": "2024-03-05T12:00:00",
      "updated_at": "2024-03-05T12:00:00"
    },
    ...
  ]
}
```

### Health Check
```bash
GET /api/health

Response: 200 OK
{
  "status": "healthy",
  "timestamp": "2024-03-05T12:00:00"
}
```

## 🗄️ Database

### Supported Databases

**Development:**
- SQLite (default, local file-based)

**Production (Recommended):**
- PostgreSQL (Heroku, AWS RDS, Railway, Supabase, Neon)
- MySQL

### Setup PostgreSQL

1. **Using Supabase (Free):**
   ```
   - Sign up: https://supabase.com
   - Create project
   - Copy JDBC connection string
   - Format: postgresql://postgres:PASSWORD@HOST:5432/postgres
   - Add as DATABASE_URL in Netlify
   ```

2. **Using Railway.app:**
   ```
   - Sign up: https://railway.app
   - Create new project → Provision PostgreSQL
   - Copy connection string
   - Add as DATABASE_URL in Netlify
   ```

3. **Update Connection String in Netlify:**
   - Site Settings → Build & Deploy → Environment
   - Add `DATABASE_URL` variable

### Database Models

- **User:** Authentication and user data
- **Trade:** Trading history
- **Portfolio:** User cryptocurrency holdings
- **Cryptocurrency:** Price data

## 🔐 Security

### Environment Variables (Never Commit!)
```env
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-key-here
DATABASE_URL=postgresql://user:pass@host/db
FLASK_ENV=production
DEBUG=False
```

### Generate Secure Keys
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### CORS Configuration
Update in `api/app.py`:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.netlify.app"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

## 🧪 Testing

### Test Health Endpoint
```bash
curl https://yourdomain.netlify.app/api/health
```

### Test Registration
```bash
curl -X POST https://yourdomain.netlify.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Test Login
```bash
curl -X POST https://yourdomain.netlify.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

## 📊 Monitoring

### Netlify Logs
```bash
netlify logs --function api
```

### View Deployment Status
- Go to https://app.netlify.com
- Select your site
- Check Deployment history and logs

## 🚨 Troubleshooting

### Issue: 500 Errors
1. Check Netlify function logs
2. Verify environment variables
3. Test database connection

### Issue: CORS Errors
1. Update `CORS` in `api/app.py`
2. Add domain to allowed origins
3. Clear browser cache

### Issue: Database Connection Failed
1. Verify `DATABASE_URL` format
2. Check database service is running
3. Confirm credentials

### Issue: Static Files Not Loading
1. Ensure files in `public/` directory
2. Check `netlify.toml` configuration
3. Clear browser cache

## 📖 Documentation

- [Netlify Deployment Guide](./NETLIFY_DEPLOYMENT_GUIDE.md) - Detailed deployment steps
- [API Documentation](./api/API_DOCUMENTATION.md) - Complete API reference
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Netlify Functions](https://docs.netlify.com/functions/overview/)

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Test locally
4. Commit and push
5. Create a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 🎯 Roadmap

- [ ] WebSocket support for real-time prices
- [ ] Advanced trading features
- [ ] User portfolio analytics
- [ ] Mobile app
- [ ] Market depth visualization
- [ ] Order book implementation

## 📞 Support

For issues and questions:
1. Check [Troubleshooting](#-troubleshooting)
2. Review [Netlify Deployment Guide](./NETLIFY_DEPLOYMENT_GUIDE.md)
3. Check API logs in Netlify Dashboard

## 🎉 Deployment Checklist

- [ ] Git repository initialized
- [ ] GitHub repository created
- [ ] Netlify account set up
- [ ] Environment variables configured
- [ ] Database connected
- [ ] Custom domain added (optional)
- [ ] SSL certificate enabled
- [ ] API endpoints tested
- [ ] Frontend loads correctly
- [ ] Authentication works
- [ ] Error monitoring set up

---

**Last Updated:** March 5, 2026
**Status:** Production Ready ✅
