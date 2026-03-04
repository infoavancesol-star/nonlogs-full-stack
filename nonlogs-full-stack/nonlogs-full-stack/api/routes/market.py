"""
Market Routes
Handles market data and price information
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta

market_bp = Blueprint('market', __name__)

# Mock market data (in production, connect to real price APIs)
MARKET_DATA = {
    'BTC': {'name': 'Bitcoin', 'price': 45320.50, 'change_24h': 5.2, 'change_7d': 8.1},
    'ETH': {'name': 'Ethereum', 'price': 2580.75, 'change_24h': 3.8, 'change_7d': 6.5},
    'XRP': {'name': 'Ripple', 'price': 0.58, 'change_24h': 2.1, 'change_7d': 1.3},
    'USD': {'name': 'US Dollar', 'price': 1.0, 'change_24h': 0.0, 'change_7d': 0.0},
    'EUR': {'name': 'Euro', 'price': 0.92, 'change_24h': -0.5, 'change_7d': 0.2},
}

@market_bp.route('/prices', methods=['GET'])
def get_prices():
    """Get current prices for all cryptocurrencies"""
    try:
        currencies = request.args.get('currencies', 'BTC,ETH,XRP,USD,EUR').split(',')
        
        prices = {}
        for currency in currencies:
            currency = currency.strip().upper()
            if currency in MARKET_DATA:
                data = MARKET_DATA[currency]
                prices[currency] = {
                    'name': data['name'],
                    'price': data['price'],
                    'change_24h': data['change_24h'],
                    'change_7d': data['change_7d'],
                    'timestamp': datetime.utcnow().isoformat()
                }
        
        return jsonify({
            'prices': prices,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@market_bp.route('/price/<currency>', methods=['GET'])
def get_price(currency):
    """Get price for specific currency"""
    try:
        currency = currency.upper()
        
        if currency not in MARKET_DATA:
            return jsonify({'error': f'Currency {currency} not found'}), 404
        
        data = MARKET_DATA[currency]
        
        return jsonify({
            'currency': currency,
            'name': data['name'],
            'price': data['price'],
            'change_24h': data['change_24h'],
            'change_7d': data['change_7d'],
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@market_bp.route('/market-cap', methods=['GET'])
def get_market_cap():
    """Get market cap information"""
    try:
        # Mock market cap data
        return jsonify({
            'total_market_cap': 2500000000000,  # $2.5 trillion
            'btc_dominance': 45.2,
            'eth_dominance': 18.5,
            'altcoin_market_cap': 1375000000000,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@market_bp.route('/trading-pairs', methods=['GET'])
def get_trading_pairs():
    """Get available trading pairs"""
    try:
        # Mock trading pairs
        pairs = [
            {'from': 'BTC', 'to': 'USD'},
            {'from': 'BTC', 'to': 'EUR'},
            {'from': 'ETH', 'to': 'USD'},
            {'from': 'ETH', 'to': 'EUR'},
            {'from': 'ETH', 'to': 'BTC'},
            {'from': 'XRP', 'to': 'USD'},
            {'from': 'XRP', 'to': 'BTC'},
            {'from': 'XRP', 'to': 'ETH'},
        ]
        
        return jsonify({
            'pairs': pairs,
            'total': len(pairs),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@market_bp.route('/24h-volume', methods=['GET'])
def get_24h_volume():
    """Get 24-hour trading volume"""
    try:
        # Mock 24h volume data
        return jsonify({
            'BTC': 28500000000,
            'ETH': 15200000000,
            'XRP': 3400000000,
            'total_volume_24h': 47100000000,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@market_bp.route('/chart/<currency>', methods=['GET'])
def get_chart_data(currency):
    """Get historical price data for chart"""
    try:
        currency = currency.upper()
        
        if currency not in MARKET_DATA:
            return jsonify({'error': f'Currency {currency} not found'}), 404
        
        # Generate mock historical data
        base_price = MARKET_DATA[currency]['price']
        chart_data = []
        
        for i in range(24):
            timestamp = datetime.utcnow() - timedelta(hours=24-i)
            # Add some variation to the price
            variation = (i * 0.5 - 6) / 100
            price = base_price * (1 + variation)
            
            chart_data.append({
                'timestamp': timestamp.isoformat(),
                'price': round(price, 2)
            })
        
        return jsonify({
            'currency': currency,
            'interval': '1h',
            'data': chart_data
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@market_bp.route('/supported-currencies', methods=['GET'])
def get_supported_currencies():
    """Get list of supported currencies"""
    try:
        currencies = []
        
        for code, data in MARKET_DATA.items():
            currencies.append({
                'code': code,
                'name': data['name'],
                'type': 'crypto' if code not in ['USD', 'EUR'] else 'fiat'
            })
        
        return jsonify({
            'currencies': currencies,
            'total': len(currencies)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
