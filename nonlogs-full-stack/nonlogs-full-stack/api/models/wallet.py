"""
Wallet Model - Stores user wallet information
"""

from app import db
from datetime import datetime
import uuid

class Wallet(db.Model):
    """Wallet model for cryptocurrency holdings"""
    
    __tablename__ = 'wallets'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Wallet information
    currency = db.Column(db.String(10), nullable=False, index=True)  # BTC, ETH, USD, etc.
    currency_name = db.Column(db.String(100))  # Bitcoin, Ethereum, US Dollar, etc.
    
    # Balances
    available_balance = db.Column(db.Float, default=0.0)
    locked_balance = db.Column(db.Float, default=0.0)  # Balance in pending trades
    total_balance = db.Column(db.Float, default=0.0)
    
    # Wallet address (for blockchain wallets)
    wallet_address = db.Column(db.String(255), unique=True)
    wallet_type = db.Column(db.String(20))  # 'fiat', 'crypto', 'stablecoin'
    
    # Value tracking
    current_price = db.Column(db.Float)  # Current market price
    total_value_usd = db.Column(db.Float, default=0.0)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_transaction = db.Column(db.DateTime)
    
    # Relationships
    transactions = db.relationship('Transaction', backref='wallet', lazy=True, cascade='all, delete-orphan')
    
    def update_balance(self, amount, is_locked=False):
        """Update wallet balance"""
        if is_locked:
            self.locked_balance += amount
        else:
            self.available_balance += amount
        
        self.total_balance = self.available_balance + self.locked_balance
        self.updated_at = datetime.utcnow()
    
    def update_value(self, current_price):
        """Update USD value of wallet"""
        self.current_price = current_price
        self.total_value_usd = self.total_balance * current_price
        self.updated_at = datetime.utcnow()
    
    def to_dict(self, include_sensitive=False):
        """Convert wallet to dictionary"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'currency': self.currency,
            'currency_name': self.currency_name,
            'available_balance': self.available_balance,
            'locked_balance': self.locked_balance,
            'total_balance': self.total_balance,
            'wallet_type': self.wallet_type,
            'current_price': self.current_price,
            'total_value_usd': self.total_value_usd,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'last_transaction': self.last_transaction.isoformat() if self.last_transaction else None,
        }
        
        if include_sensitive and self.wallet_address:
            data['wallet_address'] = self.wallet_address
        
        return data
    
    def __repr__(self):
        return f'<Wallet {self.currency}>'
