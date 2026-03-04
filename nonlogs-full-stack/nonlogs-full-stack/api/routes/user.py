"""
User Routes
Handles user profile and account management
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.user import User
from datetime import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict(include_sensitive=True)), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'phone' in data:
            user.phone = data['phone']
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict(include_sensitive=True)
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/account-info', methods=['GET'])
@jwt_required()
def get_account_info():
    """Get detailed account information"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'account_tier': user.account_tier,
            'is_verified': user.is_verified,
            'two_factor_enabled': user.two_factor_enabled,
            'created_at': user.created_at.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'account_age_days': (datetime.utcnow() - user.created_at).days
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/deactivate', methods=['POST'])
@jwt_required()
def deactivate_account():
    """Deactivate user account"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Require password confirmation
        data = request.get_json()
        if not data or not data.get('password'):
            return jsonify({'error': 'Password required for account deactivation'}), 400
        
        if not user.check_password(data['password']):
            return jsonify({'error': 'Incorrect password'}), 401
        
        # Deactivate account
        user.is_active = False
        db.session.commit()
        
        return jsonify({
            'message': 'Account deactivated successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/upgrade-tier', methods=['POST'])
@jwt_required()
def upgrade_tier():
    """Upgrade account tier"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        new_tier = data.get('tier')
        
        valid_tiers = ['free', 'pro', 'premium']
        if new_tier not in valid_tiers:
            return jsonify({'error': 'Invalid tier'}), 400
        
        user.account_tier = new_tier
        db.session.commit()
        
        return jsonify({
            'message': f'Account upgraded to {new_tier}',
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/enable-2fa', methods=['POST'])
@jwt_required()
def enable_2fa():
    """Enable two-factor authentication"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Generate 2FA secret (in real implementation, use TOTP library)
        import secrets
        secret = secrets.token_urlsafe(32)
        
        user.two_factor_enabled = True
        user.two_factor_secret = secret
        db.session.commit()
        
        return jsonify({
            'message': '2FA enabled',
            'secret': secret,
            'note': 'Save this secret in your authenticator app'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/disable-2fa', methods=['POST'])
@jwt_required()
def disable_2fa():
    """Disable two-factor authentication"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.two_factor_enabled = False
        user.two_factor_secret = None
        db.session.commit()
        
        return jsonify({
            'message': '2FA disabled successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
