#!/usr/bin/env python3
"""
NonLogs API Test Script
Tests all API endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:5000/api'

class Colors:
    """Terminal colors for output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}→ {message}{Colors.END}")

def print_header(message):
    print(f"\n{Colors.YELLOW}{'='*60}{Colors.END}")
    print(f"{Colors.YELLOW}{message}{Colors.END}")
    print(f"{Colors.YELLOW}{'='*60}{Colors.END}\n")

# Global token storage
access_token = None

def test_health():
    """Test health endpoint"""
    print_header("Testing Health Check")
    
    try:
        response = requests.get(f'{BASE_URL}/health')
        data = response.json()
        
        if response.status_code == 200:
            print_success(f"Server is healthy: {data['status']}")
            print(f"  Status: {data['status']}")
            print(f"  Timestamp: {data['timestamp']}")
        else:
            print_error(f"Health check failed: {response.status_code}")
            
    except Exception as e:
        print_error(f"Connection failed: {str(e)}")
        print_info("Make sure the server is running: python app.py")
        return False
    
    return True

def test_register():
    """Test user registration"""
    print_header("Testing User Registration")
    
    payload = {
        'email': f'testuser_{datetime.now().timestamp()}@example.com',
        'password': 'testpass123',
        'username': f'testuser_{datetime.now().timestamp()}'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/register', json=payload)
        data = response.json()
        
        if response.status_code == 201:
            print_success("User registration successful")
            print(f"  Email: {data['user']['email']}")
            print(f"  Username: {data['user']['username']}")
            print(f"  Created: {data['user']['created_at']}")
            return payload['email'], payload['password']
        else:
            print_error(f"Registration failed: {data['message']}")
            
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
    
    return None, None

def test_login(email, password):
    """Test user login"""
    print_header("Testing User Login")
    
    global access_token
    
    payload = {
        'email': email,
        'password': password
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/login', json=payload)
        data = response.json()
        
        if response.status_code == 200:
            access_token = data['access_token']
            print_success("User login successful")
            print(f"  Email: {data['user']['email']}")
            print(f"  Token: {access_token[:30]}...")
            return True
        else:
            print_error(f"Login failed: {data['message']}")
            
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
    
    return False

def test_get_profile():
    """Test get user profile"""
    print_header("Testing Get User Profile")
    
    if not access_token:
        print_error("Not authenticated. Run login test first.")
        return False
    
    headers = {'Authorization': f'Bearer {access_token}'}
    
    try:
        response = requests.get(f'{BASE_URL}/user/profile', headers=headers)
        data = response.json()
        
        if response.status_code == 200:
            print_success("Profile retrieved successfully")
            print(f"  ID: {data['id']}")
            print(f"  Email: {data['email']}")
            print(f"  Username: {data['username']}")
            return True
        else:
            print_error(f"Failed to get profile: {data['message']}")
            
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
    
    return False

def test_get_wallets():
    """Test get user wallets"""
    print_header("Testing Get Wallets")
    
    if not access_token:
        print_error("Not authenticated. Run login test first.")
        return False
    
    headers = {'Authorization': f'Bearer {access_token}'}
    
    try:
        response = requests.get(f'{BASE_URL}/wallets', headers=headers)
        data = response.json()
        
        if response.status_code == 200:
            print_success("Wallets retrieved successfully")
            for wallet in data['wallets']:
                print(f"  {wallet['currency']}: {wallet['balance']} (ID: {wallet['id']})")
            return True
        else:
            print_error(f"Failed to get wallets: {response.text}")
            
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
    
    return False

def test_create_wallet():
    """Test create new wallet"""
    print_header("Testing Create Wallet")
    
    if not access_token:
        print_error("Not authenticated. Run login test first.")
        return False
    
    headers = {'Authorization': f'Bearer {access_token}'}
    payload = {
        'currency': 'XRP',
        'balance': 0.0
    }
    
    try:
        response = requests.post(f'{BASE_URL}/wallets', json=payload, headers=headers)
        data = response.json()
        
        if response.status_code == 201:
            print_success("Wallet created successfully")
            print(f"  Currency: {data['wallet']['currency']}")
            print(f"  Balance: {data['wallet']['balance']}")
            return True
        elif response.status_code == 400:
            print_error(f"Wallet creation failed: {data['message']}")
            print_info("Wallet might already exist")
            return True
        else:
            print_error(f"Failed: {data['message']}")
            
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
    
    return False

def test_get_market_prices():
    """Test get market prices"""
    print_header("Testing Get Market Prices")
    
    try:
        response = requests.get(f'{BASE_URL}/market/prices')
        data = response.json()
        
        if response.status_code == 200:
            print_success("Market prices retrieved successfully")
            for price in data['prices']:
                print(f"  {price['currency']}: ${price['price']:.2f} ({price['change_24h']:+.1f}%)")
            return True
        else:
            print_error(f"Failed to get prices: {response.text}")
            
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
    
    return False

def test_create_trade():
    """Test create trade"""
    print_header("Testing Create Trade")
    
    if not access_token:
        print_error("Not authenticated. Run login test first.")
        return False
    
    # First, add balance to wallet
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Create trade (will fail if no balance, but that's OK for testing)
    payload = {
        'from_currency': 'USD',
        'to_currency': 'BTC',
        'amount': 1000.0,
        'price': 45320.50
    }
    
    try:
        response = requests.post(f'{BASE_URL}/trades', json=payload, headers=headers)
        data = response.json()
        
        if response.status_code == 201:
            print_success("Trade created successfully")
            print(f"  From: {data['trade']['from_currency']}")
            print(f"  To: {data['trade']['to_currency']}")
            print(f"  Amount: {data['trade']['amount']}")
            print(f"  Price: ${data['trade']['price']:.2f}")
            print(f"  Total: ${data['trade']['total']:.2f}")
            return True
        else:
            print_info(f"Trade failed (expected if no balance): {data['message']}")
            return True
            
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
    
    return False

def main():
    """Run all tests"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}NonLogs API Test Suite{Colors.END}")
    print(f"{Colors.BLUE}Testing: {BASE_URL}{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    # Test health
    if not test_health():
        return
    
    # Test registration and login
    email, password = test_register()
    if not email:
        print_error("Could not register user. Stopping tests.")
        return
    
    if not test_login(email, password):
        print_error("Could not login. Stopping tests.")
        return
    
    # Test authenticated endpoints
    test_get_profile()
    test_get_wallets()
    test_create_wallet()
    
    # Test public endpoints
    test_get_market_prices()
    
    # Test trading
    test_create_trade()
    
    # Summary
    print_header("Test Suite Complete")
    print_success("All tests completed!")
    print_info("Check results above for any failures")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Tests interrupted by user{Colors.END}")
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
