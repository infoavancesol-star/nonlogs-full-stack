"""
Trade Model - Stores trading information
"""

from app import db
from datetime import datetime
import uuid

class Trade(db.Model):
    """Trade model for buy/sell orders"""
    
    __tablename__ = 'trades'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Trade details
    trade_type = db.Column(db.String(10), nullable=False)  # 'buy' or 'sell'
    from_currency = db.Column(db.String(10), nullable=False)  # BTC, ETH, etc.
    to_currency = db.Column(db.String(10), nullable=False)  # USD, EUR, etc.
    
    # Amount and price
    from_amount = db.Column(db.Float, nullable=False)
    to_amount = db.Column(db.Float, nullable=False)
    price_per_unit = db.Column(db.Float, nullable=False)
    
    # Fees
    fee_amount = db.Column(db.Float, default=0.0)
    fee_percentage = db.Column(db.Float, default=0.1)  # 0.1% default
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, completed, cancelled, failed
    
    # Trading information
    market_price = db.Column(db.Float)
    price_impact = db.Column(db.Float)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    completed_at = db.Column(db.DateTime)
    
    # IP Address (anonymized)
    ip_hash = db.Column(db.String(255))
    
    def calculate_total(self):
        """Calculate total including fees"""
        if self.trade_type == 'buy':
            return self.to_amount + self.fee_amount
        else:
            return self.to_amount - self.fee_amount
    
    def to_dict(self):
        """Convert trade to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'trade_type': self.trade_type,
            'from_currency': self.from_currency,
            'to_currency': self.to_currency,
            'from_amount': self.from_amount,
            'to_amount': self.to_amount,
            'price_per_unit': self.price_per_unit,
            'fee_amount': self.fee_amount,
            'fee_percentage': self.fee_percentage,
            'status': self.status,
            'market_price': self.market_price,
            'price_impact': self.price_impact,
            'total': self.calculate_total(),
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }
    
    def __repr__(self):
        return f'<Trade {self.id}>'
