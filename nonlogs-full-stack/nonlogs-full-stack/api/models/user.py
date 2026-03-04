"""
User Model - Stores user account information
"""

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

class User(db.Model):
    """User model for authentication and account management"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # User info
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    phone = db.Column(db.String(20))
    
    # Account status
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(255), unique=True)
    
    # Privacy settings
    two_factor_enabled = db.Column(db.Boolean, default=False)
    two_factor_secret = db.Column(db.String(255))
    
    # Account info
    account_tier = db.Column(db.String(50), default='free')  # free, pro, premium
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # IP logging (privacy-respecting)
    registered_ip = db.Column(db.String(45))  # IPv4 or IPv6
    
    # Relationships
    trades = db.relationship('Trade', backref='user', lazy=True, cascade='all, delete-orphan')
    wallets = db.relationship('Wallet', backref='user', lazy=True, cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_sensitive=False):
        """Convert user to dictionary"""
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'account_tier': self.account_tier,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
        }
        
        if include_sensitive:
            data['phone'] = self.phone
            data['two_factor_enabled'] = self.two_factor_enabled
        
        return data
    
    def __repr__(self):
        return f'<User {self.username}>'
