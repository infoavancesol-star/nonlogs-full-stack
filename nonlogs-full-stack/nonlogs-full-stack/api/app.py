"""
NonLogs Backend - Flask Application
Professional Python backend for the NonLogs crypto exchange website
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///nonlogs.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ==================== DATABASE MODELS ====================

class User(db.Model):
    """User model for registration and authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    wallet_address = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    trades = db.relationship('Trade', backref='user', lazy=True, cascade='all, delete-orphan')
    portfolio = db.relationship('Portfolio', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'wallet_address': self.wallet_address,
            'created_at': self.created_at.isoformat()
        }


class Trade(db.Model):
    """Trade model for storing trading history"""
    __tablename__ = 'trades'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    crypto_from = db.Column(db.String(10), nullable=False)
    crypto_to = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    trade_type = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default='COMPLETED')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        """Convert trade to dictionary"""
        return {
            'id': self.id,
            'crypto_from': self.crypto_from,
            'crypto_to': self.crypto_to,
            'amount': self.amount,
            'price': self.price,
            'total': self.total,
            'trade_type': self.trade_type,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }


class Portfolio(db.Model):
    """Portfolio model for tracking user crypto holdings"""
    __tablename__ = 'portfolio'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    crypto = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, default=0.0)
    average_price = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'crypto', name='unique_user_crypto'),)
    
    def to_dict(self):
        """Convert portfolio to dictionary"""
        return {
            'id': self.id,
            'crypto': self.crypto,
            'amount': self.amount,
            'average_price': self.average_price,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Cryptocurrency(db.Model):
    """Cryptocurrency model for storing crypto prices"""
    __tablename__ = 'cryptocurrencies'
    
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    change_24h = db.Column(db.Float, default=0.0)
    market_cap = db.Column(db.Float, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert cryptocurrency to dictionary"""
        return {
            'id': self.id,
            'symbol': self.symbol,
            'name': self.name,
            'price': self.price,
            'change_24h': self.change_24h,
            'market_cap': self.market_cap,
            'updated_at': self.updated_at.isoformat()
        }


# ==================== API ROUTES ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


# ==================== AUTHENTICATION ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        user = User(
            username=data['username'],
            email=data['email'],
            wallet_address=data.get('wallet_address', None)
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        logger.info(f'New user registered: {user.username}')
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        logger.error(f'Registration error: {str(e)}')
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing email or password'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        access_token = create_access_token(identity=user.id)
        
        logger.info(f'User logged in: {user.username}')
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        logger.error(f'Login error: {str(e)}')
        return jsonify({'error': 'Login failed'}), 500


@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
    
    except Exception as e:
        logger.error(f'Profile error: {str(e)}')
        return jsonify({'error': 'Failed to fetch profile'}), 500


# ==================== CRYPTOCURRENCIES ====================

@app.route('/api/cryptocurrencies', methods=['GET'])
def get_cryptocurrencies():
    """Get all cryptocurrencies"""
    try:
        cryptos = Cryptocurrency.query.all()
        return jsonify({
            'cryptocurrencies': [crypto.to_dict() for crypto in cryptos]
        }), 200
    
    except Exception as e:
        logger.error(f'Get cryptocurrencies error: {str(e)}')
        return jsonify({'error': 'Failed to fetch cryptocurrencies'}), 500


@app.route('/api/cryptocurrencies/<symbol>', methods=['GET'])
def get_cryptocurrency(symbol):
    """Get specific cryptocurrency"""
    try:
        crypto = Cryptocurrency.query.filter_by(symbol=symbol.upper()).first()
        
        if not crypto:
            return jsonify({'error': 'Cryptocurrency not found'}), 404
        
        return jsonify({'cryptocurrency': crypto.to_dict()}), 200
    
    except Exception as e:
        logger.error(f'Get cryptocurrency error: {str(e)}')
        return jsonify({'error': 'Failed to fetch cryptocurrency'}), 500


# ==================== TRADING ====================

@app.route('/api/trades', methods=['POST'])
@jwt_required()
def create_trade():
    """Create a new trade"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        required_fields = ['crypto_from', 'crypto_to', 'amount', 'price', 'trade_type']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        trade = Trade(
            user_id=user_id,
            crypto_from=data['crypto_from'].upper(),
            crypto_to=data['crypto_to'].upper(),
            amount=float(data['amount']),
            price=float(data['price']),
            total=float(data['amount']) * float(data['price']),
            trade_type=data['trade_type'].upper()
        )
        
        db.session.add(trade)
        db.session.commit()
        
        logger.info(f'Trade created: User {user_id}')
        
        return jsonify({
            'message': 'Trade created successfully',
            'trade': trade.to_dict()
        }), 201
    
    except Exception as e:
        logger.error(f'Create trade error: {str(e)}')
        db.session.rollback()
        return jsonify({'error': 'Failed to create trade'}), 500


@app.route('/api/trades', methods=['GET'])
@jwt_required()
def get_trades():
    """Get user's trading history"""
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        trades = Trade.query.filter_by(user_id=user_id).order_by(
            Trade.created_at.desc()
        ).paginate(page=page, per_page=per_page)
        
        return jsonify({
            'trades': [trade.to_dict() for trade in trades.items],
            'total': trades.total,
            'pages': trades.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        logger.error(f'Get trades error: {str(e)}')
        return jsonify({'error': 'Failed to fetch trades'}), 500


# ==================== PORTFOLIO ====================

@app.route('/api/portfolio', methods=['GET'])
@jwt_required()
def get_portfolio():
    """Get user's portfolio"""
    try:
        user_id = get_jwt_identity()
        portfolio = Portfolio.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'portfolio': [item.to_dict() for item in portfolio]
        }), 200
    
    except Exception as e:
        logger.error(f'Get portfolio error: {str(e)}')
        return jsonify({'error': 'Failed to fetch portfolio'}), 500


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'error': 'Unauthorized'}), 401


# ==================== INITIALIZATION ====================

def create_app():
    """Application factory"""
    with app.app_context():
        db.create_all()
        logger.info('Database initialized')
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
