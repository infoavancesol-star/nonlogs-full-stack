"""
Wallet Routes
Handles wallet management and balance operations
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.user import User
from models.wallet import Wallet
from models.transaction import Transaction
from datetime import datetime

wallet_bp = Blueprint('wallet', __name__)

@wallet_bp.route('/list', methods=['GET'])
@jwt_required()
def list_wallets():
    """Get all wallets for the authenticated user"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        wallets = Wallet.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'wallets': [wallet.to_dict() for wallet in wallets]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@wallet_bp.route('/<wallet_id>', methods=['GET'])
@jwt_required()
def get_wallet(wallet_id):
    """Get specific wallet details"""
    try:
        user_id = get_jwt_identity()
        wallet = Wallet.query.filter_by(id=wallet_id, user_id=user_id).first()
        
        if not wallet:
            return jsonify({'error': 'Wallet not found'}), 404
        
        return jsonify(wallet.to_dict(include_sensitive=True)), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@wallet_bp.route('/deposit', methods=['POST'])
@jwt_required()
def deposit():
    """Deposit funds to wallet"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        if not data or not data.get('wallet_id') or not data.get('amount'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        amount = float(data['amount'])
        
        if amount <= 0:
            return jsonify({'error': 'Amount must be positive'}), 400
        
        wallet = Wallet.query.filter_by(id=data['wallet_id'], user_id=user_id).first()
        
        if not wallet:
            return jsonify({'error': 'Wallet not found'}), 404
        
        # Update wallet balance
        wallet.update_balance(amount)
        
        # Create transaction record
        transaction = Transaction(
            user_id=user_id,
            wallet_id=wallet.id,
            transaction_type='deposit',
            amount=amount,
            currency=wallet.currency,
            description=f'Deposit to {wallet.currency} wallet',
            status='completed'
        )
        transaction.mark_completed()
        
        wallet.last_transaction = datetime.utcnow()
        
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'message': 'Deposit successful',
            'wallet': wallet.to_dict(),
            'transaction': transaction.to_dict()
        }), 200
    
    except ValueError:
        return jsonify({'error': 'Invalid amount'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@wallet_bp.route('/withdraw', methods=['POST'])
@jwt_required()
def withdraw():
    """Withdraw funds from wallet"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        if not data or not data.get('wallet_id') or not data.get('amount'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        amount = float(data['amount'])
        
        if amount <= 0:
            return jsonify({'error': 'Amount must be positive'}), 400
        
        wallet = Wallet.query.filter_by(id=data['wallet_id'], user_id=user_id).first()
        
        if not wallet:
            return jsonify({'error': 'Wallet not found'}), 404
        
        if wallet.available_balance < amount:
            return jsonify({'error': 'Insufficient funds'}), 400
        
        # Deduct from wallet
        wallet.update_balance(-amount)
        
        # Create transaction record
        transaction = Transaction(
            user_id=user_id,
            wallet_id=wallet.id,
            transaction_type='withdrawal',
            amount=amount,
            currency=wallet.currency,
            description=f'Withdrawal from {wallet.currency} wallet',
            status='pending'
        )
        
        wallet.last_transaction = datetime.utcnow()
        
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'message': 'Withdrawal initiated',
            'wallet': wallet.to_dict(),
            'transaction': transaction.to_dict()
        }), 200
    
    except ValueError:
        return jsonify({'error': 'Invalid amount'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@wallet_bp.route('/transfer', methods=['POST'])
@jwt_required()
def transfer():
    """Transfer funds between wallets"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        required_fields = ['from_wallet_id', 'to_wallet_id', 'amount']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        amount = float(data['amount'])
        
        if amount <= 0:
            return jsonify({'error': 'Amount must be positive'}), 400
        
        # Get wallets
        from_wallet = Wallet.query.filter_by(id=data['from_wallet_id'], user_id=user_id).first()
        to_wallet = Wallet.query.filter_by(id=data['to_wallet_id'], user_id=user_id).first()
        
        if not from_wallet or not to_wallet:
            return jsonify({'error': 'One or both wallets not found'}), 404
        
        if from_wallet.available_balance < amount:
            return jsonify({'error': 'Insufficient funds'}), 400
        
        # Perform transfer
        from_wallet.update_balance(-amount)
        to_wallet.update_balance(amount)
        
        # Create transaction records
        from_transaction = Transaction(
            user_id=user_id,
            wallet_id=from_wallet.id,
            transaction_type='transfer',
            amount=amount,
            currency=from_wallet.currency,
            description=f'Transfer to {to_wallet.currency} wallet',
            status='completed'
        )
        from_transaction.mark_completed()
        
        to_transaction = Transaction(
            user_id=user_id,
            wallet_id=to_wallet.id,
            transaction_type='transfer',
            amount=amount,
            currency=to_wallet.currency,
            description=f'Transfer from {from_wallet.currency} wallet',
            status='completed'
        )
        to_transaction.mark_completed()
        
        from_wallet.last_transaction = datetime.utcnow()
        to_wallet.last_transaction = datetime.utcnow()
        
        db.session.add_all([from_transaction, to_transaction])
        db.session.commit()
        
        return jsonify({
            'message': 'Transfer successful',
            'from_wallet': from_wallet.to_dict(),
            'to_wallet': to_wallet.to_dict(),
        }), 200
    
    except ValueError:
        return jsonify({'error': 'Invalid amount'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@wallet_bp.route('/transactions/<wallet_id>', methods=['GET'])
@jwt_required()
def get_wallet_transactions(wallet_id):
    """Get transaction history for a wallet"""
    try:
        user_id = get_jwt_identity()
        
        wallet = Wallet.query.filter_by(id=wallet_id, user_id=user_id).first()
        
        if not wallet:
            return jsonify({'error': 'Wallet not found'}), 404
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        transactions = Transaction.query.filter_by(wallet_id=wallet_id).order_by(
            Transaction.created_at.desc()
        ).paginate(page=page, per_page=per_page)
        
        return jsonify({
            'transactions': [t.to_dict() for t in transactions.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': transactions.total,
                'pages': transactions.pages
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
