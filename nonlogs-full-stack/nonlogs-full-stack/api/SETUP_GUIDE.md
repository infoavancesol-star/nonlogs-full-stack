╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║         🚀 NONLOGS PYTHON BACKEND - SETUP & DEPLOYMENT GUIDE 🚀          ║
║                                                                            ║
║              Complete API for Privacy-First Crypto Exchange               ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝


📋 WHAT'S INCLUDED
===================

✅ app.py - Main Flask application
✅ requirements.txt - Python dependencies  
✅ .env.example - Environment configuration template
✅ API_DOCUMENTATION.md - Complete API reference
✅ This setup guide

Features:
✓ User authentication (JWT)
✓ Wallet management
✓ Trading functionality
✓ Market data
✓ Privacy-first design
✓ RESTful API


🎯 QUICK START (5 MINUTES)
==========================

STEP 1: Install Python
───────────────────────

Download: https://www.python.org/downloads/
Version: Python 3.8 or higher

Verify installation:
python --version


STEP 2: Create Virtual Environment
───────────────────────────────────

Open terminal/command prompt and run:

Windows:
python -m venv venv
venv\Scripts\activate

macOS/Linux:
python3 -m venv venv
source venv/bin/activate

You should see (venv) in your terminal


STEP 3: Install Dependencies
─────────────────────────────

pip install -r requirements.txt

Wait for all packages to install (takes 1-2 minutes)


STEP 4: Configure Environment
──────────────────────────────

Copy .env.example to .env:

Windows: copy .env.example .env
macOS/Linux: cp .env.example .env

Edit .env file (optional for development):
- Change JWT_SECRET_KEY to something random
- Leave DATABASE_URL as sqlite:///nonlogs.db for development


STEP 5: Run Server
──────────────────

python app.py

You should see:
  * Running on http://0.0.0.0:5000
  * Database initialized
  * Sample market data added

Server is now running! ✅


📍 ACCESSING THE API
====================

Base URL: http://localhost:5000

Test it:
curl http://localhost:5000/api/health

Response should be:
{
  "status": "healthy",
  "timestamp": "2024-03-04T20:45:00"
}


🔗 CONNECTING FRONTEND TO BACKEND
==================================

Update your HTML/JavaScript to point to backend:

const API_URL = 'http://localhost:5000/api';

// Example: Login
fetch(`${API_URL}/auth/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
})
.then(res => res.json())
.then(data => {
  console.log('Token:', data.access_token);
  // Store token in localStorage
  localStorage.setItem('token', data.access_token);
});


📚 COMMON API CALLS
===================

1. REGISTER USER
────────────────

POST http://localhost:5000/api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepass123",
  "username": "myuser"
}


2. LOGIN USER
─────────────

POST http://localhost:5000/api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepass123"
}

Response includes access_token!


3. GET USER PROFILE
────────────────────

GET http://localhost:5000/api/user/profile
Authorization: Bearer {access_token}


4. GET WALLETS
───────────────

GET http://localhost:5000/api/wallets
Authorization: Bearer {access_token}


5. CREATE TRADE
────────────────

POST http://localhost:5000/api/trades
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "from_currency": "USD",
  "to_currency": "BTC",
  "amount": 1000.0,
  "price": 45320.50
}


6. GET MARKET PRICES
──────────────────────

GET http://localhost:5000/api/market/prices

No authentication needed!


📖 FULL API DOCUMENTATION
=========================

See API_DOCUMENTATION.md for:
- All endpoints
- Request/response formats
- Authentication details
- Database schema
- Error handling
- Testing examples


🚀 PRODUCTION DEPLOYMENT
========================

OPTION 1: Using Gunicorn
────────────────────────

1. Install Gunicorn:
   pip install gunicorn

2. Run with Gunicorn:
   gunicorn -w 4 -b 0.0.0.0:5000 app:app

   Parameters:
   -w 4 = 4 worker processes
   -b 0.0.0.0:5000 = bind to all interfaces on port 5000


OPTION 2: Using Heroku
──────────────────────

1. Create Procfile:
   web: gunicorn app:app

2. Deploy:
   heroku login
   heroku create nonlogs-api
   git push heroku main


OPTION 3: Using Docker
──────────────────────

1. Create Dockerfile:
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

2. Build:
   docker build -t nonlogs-api .

3. Run:
   docker run -p 5000:5000 nonlogs-api


DATABASE SETUP
==============

For Development:
────────────────
- SQLite (default in .env)
- Database file: nonlogs.db
- No setup needed, creates automatically


For Production (PostgreSQL):
────────────────────────────

1. Install PostgreSQL

2. Create database:
   createdb nonlogs

3. Update .env:
   DATABASE_URL=postgresql://user:password@localhost/nonlogs

4. Restart server:
   python app.py


🔐 SECURITY SETUP
=================

IMPORTANT FOR PRODUCTION:

1. Change JWT_SECRET_KEY
   Generate random key:
   python -c "import secrets; print(secrets.token_hex(32))"
   
   Add to .env:
   JWT_SECRET_KEY=your_generated_key

2. Set Flask Environment
   FLASK_ENV=production

3. Use HTTPS
   Configure reverse proxy (nginx)

4. Add Rate Limiting
   pip install Flask-Limiter
   
5. Add CORS Whitelist
   CORS_ORIGINS=https://yourdomain.com

6. Use Environment Variables
   Don't hardcode secrets!


⚙️ CONFIGURATION
================

Edit .env to customize:

FLASK_ENV=development
├─ development = Debug mode ON
└─ production = Debug mode OFF

FLASK_PORT=5000
└─ Change to different port if needed

DATABASE_URL=sqlite:///nonlogs.db
├─ SQLite: sqlite:///nonlogs.db
└─ PostgreSQL: postgresql://user:pass@host/dbname

JWT_SECRET_KEY=your-secret-key
└─ Change this! Use 32+ character random string

CORS_ORIGINS=http://localhost:3000
└─ Add your frontend domain(s)


🐛 TROUBLESHOOTING
===================

Problem: "Module not found"
Solution:
- Activate virtual environment: source venv/bin/activate
- Install requirements: pip install -r requirements.txt

Problem: "Address already in use"
Solution:
- Change port in .env: FLASK_PORT=5001
- Or kill process on port 5000

Problem: "Database locked"
Solution:
- Delete nonlogs.db
- Restart server

Problem: "CORS error from frontend"
Solution:
- Add frontend URL to .env: CORS_ORIGINS=https://yoursite.com
- Restart server

Problem: "JWT token invalid"
Solution:
- Check header format: Authorization: Bearer {token}
- Token must be from same server
- Check token hasn't expired (24 hours)


📊 DATABASE MANAGEMENT
======================

View SQLite Database:
────────────────────

Install SQLite browser: https://sqlitebrowser.org/

Or use command line:
sqlite3 nonlogs.db
.tables        # Show tables
SELECT * FROM user;  # Show users
.exit          # Exit


Reset Database:
───────────────

rm nonlogs.db
python app.py
# Creates fresh database


Backup Database:
────────────────

cp nonlogs.db nonlogs_backup.db


🧪 TESTING THE API
===================

Using Postman (Recommended):
────────────────────────────

1. Download Postman: https://www.postman.com/
2. Create new request
3. Set URL: http://localhost:5000/api/auth/login
4. Set method: POST
5. Set body (JSON):
   {
     "email": "test@example.com",
     "password": "test123"
   }
6. Click Send

Response includes access_token!


Using cURL:
───────────

curl -X POST http://localhost:5000/api/health

curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email":"test@example.com",
    "password":"test123",
    "username":"testuser"
  }'


Using Python:
──────────────

import requests

url = 'http://localhost:5000/api/auth/login'
data = {
    'email': 'test@example.com',
    'password': 'test123'
}

response = requests.post(url, json=data)
print(response.json())


📱 INTEGRATING WITH FRONTEND
=============================

JavaScript Example:

const API_URL = 'http://localhost:5000/api';
let authToken = null;

// Register
async function register(email, password, username) {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, username })
  });
  return await response.json();
}

// Login
async function login(email, password) {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  const data = await response.json();
  authToken = data.access_token;
  localStorage.setItem('token', authToken);
  return data;
}

// Get Wallets
async function getWallets() {
  const response = await fetch(`${API_URL}/wallets`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${authToken}`,
      'Content-Type': 'application/json'
    }
  });
  return await response.json();
}

// Get Market Prices
async function getPrices() {
  const response = await fetch(`${API_URL}/market/prices`);
  return await response.json();
}


🆚 FRONTEND VS BACKEND
=======================

Frontend (HTML/CSS/JS):
- User Interface
- Client-side logic
- Runs in browser

Backend (Python/Flask):
- Data storage
- Authentication
- Business logic
- API endpoints
- Security

Both together:
- Frontend calls backend API
- Backend returns data
- Frontend displays data


📈 SCALING UP
=============

When you grow:

1. Add caching (Redis)
2. Add message queue (Celery)
3. Add search index (Elasticsearch)
4. Add CDN for static files
5. Load balancing (nginx)
6. Database replication
7. Monitoring & alerting


═════════════════════════════════════════════════════════════════════════════

                        READY TO GET STARTED? 🚀

1. Create virtual environment
2. Install requirements
3. Configure .env
4. Run: python app.py
5. Test: http://localhost:5000/api/health

Your API backend is now running!

═════════════════════════════════════════════════════════════════════════════

For detailed API reference, see: API_DOCUMENTATION.md

═════════════════════════════════════════════════════════════════════════════
