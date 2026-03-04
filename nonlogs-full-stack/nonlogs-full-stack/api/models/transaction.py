"""
Transaction Model - Stores transaction history
"""

from app import db
from datetime import datetime
import uuid

class Transaction(db.Model):
    """Transaction model for wallet deposits/withdrawals"""
    
    __tablename__ = 'transactions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    wallet_id = db.Column(db.String(36), db.ForeignKey('wallets.id'), nullable=False, index=True)
    
    # Transaction details
    transaction_type = db.Column(db.String(20), nullable=False)  # 'deposit', 'withdrawal', 'trade', 'transfer'
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    
    # Transaction information
    description = db.Column(db.Text)
    transaction_hash = db.Column(db.String(255), unique=True)  # For blockchain transactions
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed, cancelled
    
    # Addresses (for external transactions)
    from_address = db.Column(db.String(255))
    to_address = db.Column(db.String(255))
    
    # Fees
    fee_amount = db.Column(db.Float, default=0.0)
    
    # Confirmations (for blockchain)
    confirmations = db.Column(db.Integer, default=0)
    required_confirmations = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    completed_at = db.Column(db.DateTime)
    
    # Network information
    network = db.Column(db.String(50))  # 'bitcoin', 'ethereum', 'polygon', etc.
    gas_price = db.Column(db.Float)
    gas_used = db.Column(db.Float)
    
    def mark_completed(self):
        """Mark transaction as completed"""
        self.status = 'completed'
        self.completed_at = datetime.utcnow()
    
    def mark_failed(self):
        """Mark transaction as failed"""
        self.status = 'failed'
        self.completed_at = datetime.utcnow()
    
    def to_dict(self, include_sensitive=False):
        """Convert transaction to dictionary"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'wallet_id': self.wallet_id,
            'transaction_type': self.transaction_type,
            'amount': self.amount,
            'currency': self.currency,
            'description': self.description,
            'status': self.status,
            'fee_amount': self.fee_amount,
            'confirmations': self.confirmations,
            'required_confirmations': self.required_confirmations,
            'network': self.network,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }
        
        if include_sensitive:
            data['transaction_hash'] = self.transaction_hash
            data['from_address'] = self.from_address
            data['to_address'] = self.to_address
            data['gas_price'] = self.gas_price
            data['gas_used'] = self.gas_used
        
        return data
    
    def __repr__(self):
        return f'<Transaction {self.id}>'
