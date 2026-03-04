# NonLogs Backend - Python Flask API

Professional Python backend for the NonLogs crypto exchange website.

## 📋 Overview

A complete RESTful API backend built with Flask for the NonLogs privacy-first cryptocurrency exchange platform.

### Features

✅ User authentication with JWT
✅ User registration and login
✅ Trading history tracking
✅ Portfolio management
✅ Cryptocurrency data management
✅ Database persistence (SQLAlchemy ORM)
✅ CORS support for frontend integration
✅ Comprehensive error handling
✅ Logging and monitoring
✅ Production-ready code

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone or download the project**
```bash
cd nonlogs-backend
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create .env file**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize database**
```bash
python manage.py init
python manage.py seed
```

6. **Run the server**
```bash
python app.py
```

Server runs at: `http://localhost:5000`

---

## 📦 Project Structure

```
nonlogs-backend/
├── app.py                 # Main Flask application
├── config.py             # Configuration management
├── manage.py             # Database management CLI
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
├── README.md            # This file
├── nonlogs.db           # SQLite database (created after init)
└── logs/                # Application logs
```

---

## 🔑 API Endpoints

### Health Check

**GET** `/api/health`
```bash
curl http://localhost:5000/api/health
```
Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-03-04T20:00:00"
}
```

---

### Authentication

#### Register
**POST** `/api/auth/register`
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password",
    "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f42838"
  }'
```

#### Login
**POST** `/api/auth/login`
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "secure_password"
  }'
```
Response includes JWT token:
```json
{
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

#### Get Profile
**GET** `/api/auth/profile`
```bash
curl http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

### Cryptocurrencies

#### Get All Cryptocurrencies
**GET** `/api/cryptocurrencies`
```bash
curl http://localhost:5000/api/cryptocurrencies
```

#### Get Specific Cryptocurrency
**GET** `/api/cryptocurrencies/<symbol>`
```bash
curl http://localhost:5000/api/cryptocurrencies/BTC
```

---

### Trading

#### Create Trade
**POST** `/api/trades`
```bash
curl -X POST http://localhost:5000/api/trades \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "crypto_from": "BTC",
    "crypto_to": "ETH",
    "amount": 0.5,
    "price": 45320.50,
    "trade_type": "BUY"
  }'
```

#### Get Trading History
**GET** `/api/trades`
```bash
curl http://localhost:5000/api/trades \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Get Specific Trade
**GET** `/api/trades/<trade_id>`
```bash
curl http://localhost:5000/api/trades/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

### Portfolio

#### Get Portfolio
**GET** `/api/portfolio`
```bash
curl http://localhost:5000/api/portfolio \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Get Portfolio Item
**GET** `/api/portfolio/<crypto>`
```bash
curl http://localhost:5000/api/portfolio/BTC \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🗄️ Database Models

### User
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email
- `password_hash`: Hashed password
- `wallet_address`: Crypto wallet (optional)
- `created_at`: Creation timestamp
- `is_active`: Account status

### Trade
- `id`: Primary key
- `user_id`: Foreign key to User
- `crypto_from`: Source cryptocurrency
- `crypto_to`: Target cryptocurrency
- `amount`: Trade amount
- `price`: Price per unit
- `total`: Total transaction value
- `trade_type`: BUY or SELL
- `status`: Trade status
- `created_at`: Creation timestamp

### Portfolio
- `id`: Primary key
- `user_id`: Foreign key to User
- `crypto`: Cryptocurrency symbol
- `amount`: Holdings amount
- `average_price`: Average purchase price
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Cryptocurrency
- `id`: Primary key
- `symbol`: Cryptocurrency symbol (e.g., BTC)
- `name`: Full name
- `price`: Current price
- `change_24h`: 24-hour change percentage
- `market_cap`: Market capitalization
- `updated_at`: Last update timestamp

---

## 🔐 Authentication

Uses JWT (JSON Web Tokens) for secure authentication.

1. **Register** → Get credentials
2. **Login** → Receive JWT token
3. **Include token** in Authorization header: `Bearer YOUR_TOKEN`

Tokens expire after 30 days (configurable).

---

## 📊 Database Management

### Initialize Database
```bash
python manage.py init
```

### Seed Sample Data
```bash
python manage.py seed
```

### Show Statistics
```bash
python manage.py stats
```

### Reset Database
```bash
python manage.py reset
```

---

## ⚙️ Configuration

Edit `.env` file for configuration:

```
FLASK_ENV=development          # development, production, testing
FLASK_DEBUG=True               # Enable/disable debug mode
SECRET_KEY=your-secret-key     # Change in production!
DATABASE_URL=sqlite:///nonlogs.db
JWT_SECRET_KEY=your-jwt-key    # Change in production!
SERVER_HOST=0.0.0.0
SERVER_PORT=5000
LOG_LEVEL=INFO
```

### Database Options

**SQLite** (default - local development):
```
DATABASE_URL=sqlite:///nonlogs.db
```

**PostgreSQL** (production recommended):
```
DATABASE_URL=postgresql://user:password@localhost:5432/nonlogs_db
```

**MySQL**:
```
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/nonlogs_db
```

---

## 🐳 Docker Deployment

### Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Build and Run
```bash
docker build -t nonlogs-backend .
docker run -p 5000:5000 nonlogs-backend
```

---

## 🚀 Production Deployment

### Gunicorn
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name api.nonlogs.io;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Environment Setup
```bash
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key
export DATABASE_URL=postgresql://user:password@host/db
export JWT_SECRET_KEY=your-production-jwt-key
```

---

## 🧪 Testing

### Run Tests (if configured)
```bash
python -m pytest
```

### Manual Testing with cURL
See API Endpoints section above for cURL examples.

### Testing with Postman
1. Import API endpoints
2. Create environment with BASE_URL and token
3. Test each endpoint

---

## 📝 Logging

Logs are configured in `config.py` and stored in `logs/nonlogs.log`.

### Log Levels
- `DEBUG`: Detailed information
- `INFO`: General information
- `WARNING`: Warning messages
- `ERROR`: Error messages
- `CRITICAL`: Critical errors

---

## 🛡️ Security Best Practices

✅ **Change default secrets** in production
✅ **Use HTTPS** in production
✅ **Hash passwords** with werkzeug.security
✅ **Validate inputs** on all endpoints
✅ **Use JWT** for authentication
✅ **Set CORS** properly for your domain
✅ **Use environment variables** for secrets
✅ **Enable logging** for monitoring
✅ **Regular backups** of database
✅ **Update dependencies** regularly

---

## 🐛 Troubleshooting

### Database Lock Error
```
database is locked
```
Solution: Close other connections, restart app

### JWT Token Invalid
```
Unauthorized
```
Solution: Include valid token in Authorization header

### CORS Error
```
CORS policy: No 'Access-Control-Allow-Origin'
```
Solution: Check CORS configuration, verify frontend URL

### Port Already in Use
```
Address already in use
```
Solution: Change port in .env or kill process on port 5000

---

## 📚 Additional Resources

- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy ORM: https://docs.sqlalchemy.org/
- Flask-JWT-Extended: https://flask-jwt-extended.readthedocs.io/
- Flask-CORS: https://flask-cors.readthedocs.io/

---

## 📞 Support

For issues or questions:
1. Check troubleshooting section
2. Review logs in `logs/nonlogs.log`
3. Check Flask documentation
4. Open an issue on GitHub

---

## 📄 License

This project is licensed under the MIT License.

---

**Last Updated**: March 2024
**Version**: 1.0.0
