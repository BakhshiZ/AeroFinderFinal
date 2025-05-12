from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import os
import json
from dotenv import load_dotenv
import requests
from flask_cors import CORS
from amadeus_api import search_flights, get_airport_autocomplete

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Get Gemini API key
GEMINI_API_KEY = "AIzaSyBPX4Oqn4oW7tblB_IM62Ay5pN-TAf-QgM"
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found in .env file")

# Firebase setup
firebase_admin_config_json = {
  "type": "service_account",
  "project_id": "aerofinder-d6590",
  "private_key_id": "229860e3e0c28868dc22fe6577afac9b8ca32e0f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCXbpJGiYg2OtBs\no7h4Q8tqJuGmUIueTcuN0U8ZWYIYxJ/k1fqh918n1HLZlfBZVSmLKz5dxkJG/0N5\nPtn4Ok4FUXcm5tmeWMSO5/mmf6tJ1fyqaRl90sgXJoSFOY5r1Spr7m64/UEEH6r+\nc8D95ZcilB64JHb5okQR8rFWiA8OQF9XPZV/wgU0S4jp7W38T03TG1ytH6/qIPGo\nM4TOc2k9rm0XQ3Wd/nMZd93TUdvhe+mo1+hAFWgfocjFof5IOnVSHyE2Hi8c3FaD\nS4Ybqr4mBVl+YThsBst1RtNcn4coym+V/jFuL2S5iXw2WROo7d5gvbTeqE+0bhXY\nlmdu8ZPlAgMBAAECggEAD8vwhVwucd3DxTl08lK8IvgoXNWVIu/hlospka7lI9lL\nBq+NpByud/SxAGKkPmVkXoilyll2q3pQWxMD4OGQJvzfDZdSRzLiWjf3sncp8ptY\nbpxlFNuKlOOnOlCNO1FyyeyG71Q31orJJx8DGFk9YVWLONFQ+eyD5k1nU2wBCg7i\n3CFMndlKOlAdSdR/T0o/sVCbpOlvCdacNP8wCZVAXiuX7O9nc1+gggfL5RbE3JuV\njLhaSx3uIpELN6IA62ybqR6y2qSKRlPzC4Q02+UanTMiX1Y0SE94JkTUez511GuO\nd+MP5iG9GiMWQvVkQ56HzEw0GCxheHNTQ9tyGoh8EQKBgQDRGG0gk5l9NSz8mok5\ne/GxSlBBIFuSFU5YQwJwMda9iM2JX3/yko4FxVFCteAh6LuTenS63h65LHLCLXvd\nKq5lXj/NLHpg8A1/8kWU+4BryzZWCPe0gAA+x58n+3O5Oa+rcwAPgOHQFowKUgGq\npqASGCgNQuYsn8ho4OoFBuxq7QKBgQC5Zr6avMrk/XCupnYnvYNNM9XzJRM0WE8W\nQVKEwKlne5ZjEiCgNGvE++qewGdDGpEvqBJxbF2AN6WpuLM0lw79Qi1nfy/gHdvM\nm2x+GzSBtm4LUspYq9VnL5fzkqO5AZHZS7ueHAyfJRumIKSA189weOPT0XAuUh9e\nBjtkcquV2QKBgCTY1hpAiHLdFRFqtjXwFpZ0jxH6/sgOgyDgpiRZVAtQeU/1CVoY\n43g23mwQGvA+0BdcJAfuLqHZKFv5ofNGmzb31ex1IxfEFczvR73KWEYmqGue5u/j\nAqgNi4mDMVB5zvA6ss8ImkKORp1m+C43cMvff+deW6uPeMSqpfK+1pi9AoGBAJOR\n2DzJ8KT7pWkeTgWrrosQq0bxR6vubmTEca4Au9YGZNlOYHGjx/Pun/zkIE0lJFLO\ncH+fRXz8zfuda+Z8Jg4nUoSCk9TLb1wYie6GMPDeCBEzQKP7gcyz8TqKiY6EVVak\nFR3wLYuuuactbEKxhAd98blzhtsXuqfYRgXZ0AFhAoGBAKv6hx/t7kQf6eobukjC\nM79IDv9/K2whgfKwFgX+wAkeu3lNFw6yNdh3mpUTkPkn32V711mcjdE/7JzEm3hT\n9DeK4BxjGjZJ/8KzC0fkYUMIBV0ZCp+8sAnFUGtd9a2PNTtmvCgxtmWlSOFScJeR\n1Og+O02oBZbsrDZjNnj6EW9r\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@aerofinder-d6590.iam.gserviceaccount.com",
  "client_id": "109561751343817721336",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40aerofinder-d6590.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

if firebase_admin_config_json:
    try:
        firebase_admin_config = json.loads(firebase_admin_config_json)
        cred = credentials.Certificate(firebase_admin_config)
        firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK initialized successfully using environment variable.")
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from PRIV_KEY environment variable.")
        print("Please ensure the content of PRIV_KEY is valid JSON.")
    except Exception as e:
        print(f"Error initializing Firebase Admin SDK: {e}")
else:
    print("Error: PRIV_KEY environment variable not set.")
    print("Please set the PRIV_KEY environment variable in your .env file with the contents of your service account key JSON file.")

@app.route('/')
def index():
    return "Welcome to AeroFinder Backend!"

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages using Gemini API."""
    if not GEMINI_API_KEY:
        return jsonify({'error': 'API key not configured'}), 500

    try:
        data = request.get_json()
        user_message = data.get('message')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Prepare the API request - Using gemini-1.5-flash model
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        # System prompt defining the AI's role and capabilities
        system_prompt = """You are AeroBot, an AI assistant specialized in helping people with flight and air travel related questions. You are knowledgeable about:
- Flight bookings and reservations
- Airlines and their policies
- Airports and routes
- Travel requirements (visas, passports)
- Baggage policies
- Flight prices and trends
- Travel tips for flying

Keep responses concise and helpful. If a question is not about flights or air travel, politely explain you can only help with flight-related queries."""
        
        # Separate system prompt and user message in the payload
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": system_prompt}]
                },
                {
                    "role": "user",
                    "parts": [{"text": user_message}]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.8,
                "maxOutputTokens": 2048,
            }
        }

        # Make the API request
        response = requests.post(url, headers=headers, json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()
            
            # Extract the generated text from the response
            if 'candidates' in response_data:
                bot_response = response_data['candidates'][0]['content']['parts'][0]['text'].strip()
            else:
                bot_response = "I understand. How can I help you with your travel plans?"
            
            return jsonify({"response": bot_response})
        else:
            print(f"API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return jsonify({
                "error": f"API Error: {response.status_code}. Please try again."
            }), 500
    
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            "error": "An error occurred while processing your request"
        }), 500

@app.route('/api/auth/token', methods=['POST'])
def get_token():
    """
    Endpoint for getting Amadeus API access token
    """
    try:
        # Get credentials from environment variables
        client_id = os.getenv('AMADEUS_API_KEY')
        client_secret = os.getenv('AMADEUS_API_SECRET')

        if not client_id or not client_secret:
            return jsonify({
                'status': 'error',
                'message': 'API credentials not configured'
            }), 500

        # Make request to Amadeus token endpoint
        response = requests.post(
            'https://test.api.amadeus.com/v1/security/oauth2/token',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={
                'grant_type': 'client_credentials',
                'client_id': client_id,
                'client_secret': client_secret
            }
        )

        if response.status_code != 200:
            return jsonify({
                'status': 'error',
                'message': 'Failed to get access token from Amadeus'
            }), 500

        data = response.json()
        return jsonify({
            'status': 'success',
            'access_token': data['access_token'],
            'expires_in': data['expires_in']
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/flights/search', methods=['POST'])
def search_flights_route():
    """
    Endpoint for searching flights
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['originLocationCode', 'destinationLocationCode', 'departureDate']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'status': 'error',
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Get optional fields
        return_date = data.get('returnDate')
        adults = int(data.get('adults', 1))
        travel_class = data.get('travelClass', 'ECONOMY')
        filters = data.get('filters')
        
        # Search flights
        result = search_flights(
            origin=data['originLocationCode'],
            destination=data['destinationLocationCode'],
            departure_date=data['departureDate'],
            return_date=return_date,
            adults=adults,
            travel_class=travel_class,
            filters=filters
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/airports/search', methods=['GET'])
def search_airports_route():
    """
    Endpoint for searching airports
    """
    try:
        keyword = request.args.get('keyword')
        if not keyword:
            return jsonify({
                'status': 'error',
                'message': 'Missing required parameter: keyword'
            }), 400
        
        result = get_airport_autocomplete(keyword)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 
