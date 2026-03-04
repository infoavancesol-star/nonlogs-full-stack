"""
Trading Routes
Handles buy/sell orders and trading operations
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.user import User
from models.trade import Trade
from models.wallet import Wallet
from datetime import datetime

trading_bp = Blueprint('trading', __name__)

@trading_bp.route('/create-order', methods=['POST'])
@jwt_required()
def create_order():
    """Create a new trade order"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        required_fields = ['trade_type', 'from_currency', 'to_currency', 'from_amount', 'price_per_unit']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        trade_type = data.get('trade_type')
        if trade_type not in ['buy', 'sell']:
            return jsonify({'error': 'Invalid trade type'}), 400
        
        from_amount = float(data['from_amount'])
        price_per_unit = float(data['price_per_unit'])
        
        if from_amount <= 0 or price_per_unit <= 0:
            return jsonify({'error': 'Amount and price must be positive'}), 400
        
        # Calculate amounts and fees
        to_amount = from_amount * price_per_unit
        fee_percentage = float(data.get('fee_percentage', 0.1))
        fee_amount = to_amount * (fee_percentage / 100)
        
        # Create trade
        trade = Trade(
            user_id=user_id,
            trade_type=trade_type,
            from_currency=data['from_currency'],
            to_currency=data['to_currency'],
            from_amount=from_amount,
            to_amount=to_amount,
            price_per_unit=price_per_unit,
            fee_amount=fee_amount,
            fee_percentage=fee_percentage,
            status='pending',
            ip_hash=hash(request.remote_addr)
        )
        
        db.session.add(trade)
        db.session.commit()
        
        return jsonify({
            'message': 'Order created successfully',
            'trade': trade.to_dict()
        }), 201
    
    except ValueError:
        return jsonify({'error': 'Invalid input values'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@trading_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    """Get all trades for the authenticated user"""
    try:
        user_id = get_jwt_identity()
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status', None)
        
        query = Trade.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        trades = query.order_by(Trade.created_at.desc()).paginate(page=page, per_page=per_page)
        
        return jsonify({
            'trades': [t.to_dict() for t in trades.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': trades.total,
                'pages': trades.pages
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@trading_bp.route('/orders/<trade_id>', methods=['GET'])
@jwt_required()
def get_order(trade_id):
    """Get specific trade details"""
    try:
        user_id = get_jwt_identity()
        trade = Trade.query.filter_by(id=trade_id, user_id=user_id).first()
        
        if not trade:
            return jsonify({'error': 'Trade not found'}), 404
        
        return jsonify(trade.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@trading_bp.route('/orders/<trade_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_order(trade_id):
    """Cancel a pending trade"""
    try:
        user_id = get_jwt_identity()
        trade = Trade.query.filter_by(id=trade_id, user_id=user_id).first()
        
        if not trade:
            return jsonify({'error': 'Trade not found'}), 404
        
        if trade.status != 'pending':
            return jsonify({'error': 'Can only cancel pending trades'}), 400
        
        trade.status = 'cancelled'
        db.session.commit()
        
        return jsonify({
            'message': 'Order cancelled successfully',
            'trade': trade.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@trading_bp.route('/orders/<trade_id>/execute', methods=['POST'])
@jwt_required()
def execute_order(trade_id):
    """Execute a pending trade"""
    try:
        user_id = get_jwt_identity()
        trade = Trade.query.filter_by(id=trade_id, user_id=user_id).first()
        
        if not trade:
            return jsonify({'error': 'Trade not found'}), 404
        
        if trade.status != 'pending':
            return jsonify({'error': 'Can only execute pending trades'}), 400
        
        # Get user wallets
        from_wallet = Wallet.query.filter_by(user_id=user_id, currency=trade.from_currency).first()
        to_wallet = Wallet.query.filter_by(user_id=user_id, currency=trade.to_currency).first()
        
        if not from_wallet or not to_wallet:
            return jsonify({'error': 'Required wallets not found'}), 404
        
        # Check sufficient balance
        if from_wallet.available_balance < trade.from_amount:
            return jsonify({'error': 'Insufficient funds'}), 400
        
        # Execute trade
        from_wallet.update_balance(-trade.from_amount)
        to_wallet.update_balance(trade.to_amount - trade.fee_amount)
        
        trade.status = 'completed'
        trade.completed_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Order executed successfully',
            'trade': trade.to_dict(),
            'from_wallet': from_wallet.to_dict(),
            'to_wallet': to_wallet.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@trading_bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_statistics():
    """Get trading statistics for the user"""
    try:
        user_id = get_jwt_identity()
        
        all_trades = Trade.query.filter_by(user_id=user_id).all()
        completed_trades = Trade.query.filter_by(user_id=user_id, status='completed').all()
        
        total_trades = len(all_trades)
        completed_count = len(completed_trades)
        
        total_volume = sum(trade.from_amount for trade in completed_trades)
        total_fees = sum(trade.fee_amount for trade in completed_trades)
        
        return jsonify({
            'total_trades': total_trades,
            'completed_trades': completed_count,
            'pending_trades': total_trades - completed_count,
            'total_volume': total_volume,
            'total_fees': total_fees,
            'average_fee': total_fees / completed_count if completed_count > 0 else 0
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
