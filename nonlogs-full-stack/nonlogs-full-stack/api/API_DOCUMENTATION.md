# NonLogs Backend API Documentation

## Overview

NonLogs Backend is a Python Flask-based REST API for a privacy-focused cryptocurrency exchange platform. It provides authentication, wallet management, trading functionality, and market data.

## Features

- **User Authentication** - JWT-based authentication
- **Wallet Management** - Create and manage multiple wallets
- **Trading** - Execute crypto trades
- **Market Data** - Real-time cryptocurrency prices
- **Privacy-First** - No IP logging, no unnecessary data collection
- **Security** - Password hashing, JWT tokens, CORS support

## Technology Stack

- **Framework**: Flask 2.3.2
- **Database**: SQLAlchemy (SQLite/PostgreSQL)
- **Authentication**: JWT (JSON Web Tokens)
- **Security**: Werkzeug (password hashing)
- **CORS**: Flask-CORS

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- SQLite or PostgreSQL

### Setup

1. **Clone/Download Backend Files**
   ```bash
   cd nonlogs-backend
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize Database**
   ```bash
   python app.py
   # This will create the database and add sample data
   ```

6. **Run Server**
   ```bash
   python app.py
   ```

   Server will start at: `http://localhost:5000`

## API Endpoints

### Authentication

#### Register User
```
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123",
  "username": "myusername"
}

Response (201):
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "myusername",
    "created_at": "2024-03-04T20:45:00"
  }
}
```

#### Login User
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}

Response (200):
{
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "myusername",
    "created_at": "2024-03-04T20:45:00"
  }
}
```

#### Logout User
```
POST /api/auth/logout
Authorization: Bearer {access_token}

Response (200):
{
  "message": "Logout successful"
}
```

### User Profile

#### Get Profile
```
GET /api/user/profile
Authorization: Bearer {access_token}

Response (200):
{
  "id": 1,
  "email": "user@example.com",
  "username": "myusername",
  "created_at": "2024-03-04T20:45:00"
}
```

#### Update Profile
```
PUT /api/user/profile
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "username": "newusername"
}

Response (200):
{
  "message": "Profile updated",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "newusername",
    "created_at": "2024-03-04T20:45:00"
  }
}
```

### Wallets

#### Get All Wallets
```
GET /api/wallets
Authorization: Bearer {access_token}

Response (200):
{
  "wallets": [
    {
      "id": 1,
      "currency": "BTC",
      "balance": 0.5,
      "updated_at": "2024-03-04T20:45:00"
    },
    {
      "id": 2,
      "currency": "ETH",
      "balance": 5.0,
      "updated_at": "2024-03-04T20:45:00"
    }
  ]
}
```

#### Get Specific Wallet
```
GET /api/wallets/BTC
Authorization: Bearer {access_token}

Response (200):
{
  "id": 1,
  "currency": "BTC",
  "balance": 0.5,
  "updated_at": "2024-03-04T20:45:00"
}
```

#### Create New Wallet
```
POST /api/wallets
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "currency": "LTC",
  "balance": 0.0
}

Response (201):
{
  "message": "Wallet created",
  "wallet": {
    "id": 3,
    "currency": "LTC",
    "balance": 0.0,
    "updated_at": "2024-03-04T20:45:00"
  }
}
```

### Trading

#### Get All Trades
```
GET /api/trades
Authorization: Bearer {access_token}

Response (200):
{
  "trades": [
    {
      "id": 1,
      "from_currency": "USD",
      "to_currency": "BTC",
      "amount": 1000.0,
      "price": 45320.50,
      "total": 45320500.0,
      "status": "completed",
      "created_at": "2024-03-04T20:45:00"
    }
  ]
}
```

#### Create Trade
```
POST /api/trades
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "from_currency": "USD",
  "to_currency": "BTC",
  "amount": 1000.0,
  "price": 45320.50
}

Response (201):
{
  "message": "Trade executed",
  "trade": {
    "id": 1,
    "from_currency": "USD",
    "to_currency": "BTC",
    "amount": 1000.0,
    "price": 45320.50,
    "total": 45320500.0,
    "status": "completed",
    "created_at": "2024-03-04T20:45:00"
  }
}
```

#### Get Specific Trade
```
GET /api/trades/1
Authorization: Bearer {access_token}

Response (200):
{
  "id": 1,
  "from_currency": "USD",
  "to_currency": "BTC",
  "amount": 1000.0,
  "price": 45320.50,
  "total": 45320500.0,
  "status": "completed",
  "created_at": "2024-03-04T20:45:00"
}
```

### Market Data

#### Get All Prices
```
GET /api/market/prices

Response (200):
{
  "prices": [
    {
      "currency": "BTC",
      "price": 45320.50,
      "change_24h": 5.2,
      "market_cap": 890000000000,
      "volume_24h": 25000000000,
      "updated_at": "2024-03-04T20:45:00"
    },
    {
      "currency": "ETH",
      "price": 2580.75,
      "change_24h": 3.8,
      "market_cap": 310000000000,
      "volume_24h": 15000000000,
      "updated_at": "2024-03-04T20:45:00"
    }
  ]
}
```

#### Get Specific Price
```
GET /api/market/prices/BTC

Response (200):
{
  "currency": "BTC",
  "price": 45320.50,
  "change_24h": 5.2,
  "market_cap": 890000000000,
  "volume_24h": 25000000000,
  "updated_at": "2024-03-04T20:45:00"
}
```

#### Update Price (Admin)
```
POST /api/market/prices
Content-Type: application/json

{
  "currency": "BTC",
  "price": 46000.00,
  "change_24h": 6.5,
  "market_cap": 900000000000,
  "volume_24h": 26000000000
}

Response (200):
{
  "message": "Price updated",
  "data": {
    "currency": "BTC",
    "price": 46000.00,
    "change_24h": 6.5,
    "market_cap": 900000000000,
    "volume_24h": 26000000000,
    "updated_at": "2024-03-04T20:45:00"
  }
}
```

### Health Check

#### Server Health
```
GET /api/health

Response (200):
{
  "status": "healthy",
  "timestamp": "2024-03-04T20:45:00"
}
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### How to Use JWT:

1. **Register** - POST `/api/auth/register`
2. **Login** - POST `/api/auth/login` → Get `access_token`
3. **Use Token** - Add to all protected requests:
   ```
   Authorization: Bearer {access_token}
   ```

### Token Format:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3ODAwMDAwMCwianRpIjoiYWJjZGVmIn0.xxx
```

## Error Responses

### Standard Error Format:
```json
{
  "message": "Error description"
}
```

### HTTP Status Codes:
- `200` - OK
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `500` - Internal Server Error

### Example Error Response:
```json
{
  "message": "Invalid email or password"
}
```

## Database Models

### User
```python
- id (Integer, Primary Key)
- email (String, Unique)
- password_hash (String)
- username (String)
- created_at (DateTime)
- last_login (DateTime)
- is_active (Boolean)
- wallets (Relationship)
- trades (Relationship)
```

### Wallet
```python
- id (Integer, Primary Key)
- user_id (Integer, Foreign Key)
- currency (String)
- balance (Float)
- created_at (DateTime)
- updated_at (DateTime)
```

### Trade
```python
- id (Integer, Primary Key)
- user_id (Integer, Foreign Key)
- from_currency (String)
- to_currency (String)
- amount (Float)
- price (Float)
- total (Float)
- status (String)
- created_at (DateTime)
```

### MarketData
```python
- id (Integer, Primary Key)
- currency (String, Unique)
- price (Float)
- change_24h (Float)
- market_cap (Float)
- volume_24h (Float)
- updated_at (DateTime)
```

## Configuration

### Environment Variables (.env)

```
FLASK_ENV=development          # development or production
FLASK_HOST=0.0.0.0            # Host to bind to
FLASK_PORT=5000               # Port to run on
DATABASE_URL=sqlite:///nonlogs.db  # Database connection string
JWT_SECRET_KEY=your-secret-key    # Secret key for JWT signing
CORS_ORIGINS=http://localhost:3000  # Allowed CORS origins
```

## Deployment

### Using Gunicorn (Production)

```bash
pip install gunicorn

gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t nonlogs-backend .
docker run -p 5000:5000 nonlogs-backend
```

## Security Best Practices

1. **Change JWT Secret Key** - Set a strong random key in .env
2. **Use HTTPS** - Always use HTTPS in production
3. **Secure Database** - Use strong passwords for database
4. **Rate Limiting** - Implement rate limiting in production
5. **Input Validation** - All inputs are validated
6. **Password Hashing** - Passwords are hashed with Werkzeug
7. **CORS Configuration** - Configure allowed origins

## Testing

Example using curl:

```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "username": "testuser"
  }'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'

# Get Wallets (replace TOKEN with actual token)
curl -X GET http://localhost:5000/api/wallets \
  -H "Authorization: Bearer TOKEN"

# Get Market Prices
curl -X GET http://localhost:5000/api/market/prices
```

## Troubleshooting

### Issue: ModuleNotFoundError
**Solution**: Activate virtual environment and install requirements
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Database Locked
**Solution**: Delete `nonlogs.db` and restart
```bash
rm nonlogs.db
python app.py
```

### Issue: Port Already in Use
**Solution**: Change port in .env or use different port
```bash
FLASK_PORT=5001
```

### Issue: JWT Token Invalid
**Solution**: Make sure token is in header correctly
```
Authorization: Bearer {token}
```

## Contributing

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## License

MIT License - See LICENSE file

## Support

For issues and questions, please open an issue on the repository.

## Roadmap

- [ ] WebSocket support for real-time updates
- [ ] Advanced order types (limit, stop-loss)
- [ ] 2FA authentication
- [ ] Email notifications
- [ ] Admin dashboard
- [ ] Advanced analytics
- [ ] Mobile app API
