import json
import sys
import os
from pathlib import Path

# Add api directory to path
api_path = Path(__file__).parent.parent.parent / "api"
sys.path.insert(0, str(api_path))

# Set environment for Netlify
os.environ.setdefault('FLASK_ENV', 'production')
os.environ.setdefault('DEBUG', 'False')

# Import Flask app
from app import create_app

app = create_app()

def handler(event, context):
    """
    Netlify Functions handler for Flask backend
    Converts HTTP events to Flask requests and responses
    """
    
    # Extract request data
    path = event.get('path', '/')
    method = event.get('httpMethod', 'GET').upper()
    headers = event.get('headers', {}) or {}
    body = event.get('body', '')
    
    # Handle CORS preflight requests
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Max-Age': '86400'
            },
            'body': ''
        }
    
    try:
        # Prepare Flask test client request
        with app.test_client() as client:
            # Build the request
            kwargs = {
                'method': method,
                'headers': headers,
            }
            
            # Add body if present
            if body:
                if headers.get('content-type', '').startswith('application/json'):
                    kwargs['json'] = json.loads(body)
                else:
                    kwargs['data'] = body
            
            # Make the request
            response = client.open(path, **kwargs)
            
            # Extract response data
            status_code = response.status_code
            response_headers = {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            }
            
            # Add response headers from Flask
            for key, value in response.headers:
                if key.lower() not in ['content-length', 'content-encoding']:
                    response_headers[key] = value
            
            response_body = response.get_data(as_text=True)
            
            return {
                'statusCode': status_code,
                'headers': response_headers,
                'body': response_body
            }
    
    except json.JSONDecodeError as e:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Invalid JSON in request body'})
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': f'Internal server error: {str(e)}'})
        }
