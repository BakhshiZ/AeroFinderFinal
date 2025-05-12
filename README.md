# AeroFinder - Flight Search and Booking Platform

AeroFinder is a modern web application for searching and booking flights, featuring an AI-powered chatbot assistant. The platform combines flight search capabilities with intelligent travel assistance to provide a comprehensive travel planning experience.

## Core Features

- **AI Travel Assistant (AeroBot)**
  - Powered by Google's Gemini API
  - Specialized in flight and travel-related queries
  - Real-time chat interface

- **Flight Search**
  - Advanced filtering options
  - Real-time pricing
  - Multi-city support
  - Amadeus API integration

- **User Features**
  - User authentication via Firebase
  - Flight bookmarking
  - Personalized dashboard
  - Search history

- **Responsive Design**
  - Mobile-first approach
  - Cross-browser compatibility
  - Modern UI/UX

## Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript/jQuery
- Firebase Authentication
- Font Awesome Icons

### Backend
- Python Flask
- Firebase Admin SDK
- Google Gemini API
- Amadeus Travel API
- CORS support

## Project Structure

```
AeroFinder/
├── frontend/
│   ├── css/
│   │   ├── main.css
│   │   ├── content.css
│   │   ├── auth.css
│   │   └── chatbot.css
│   ├── js/
│   │   ├── auth.js
│   │   ├── chatbot.js
│   │   └── main.js
│   ├── chatbot.html
│   ├── contact.html
│   ├── about.html
│   ├── login.html
│   └── register.html
└── backend/
    ├── app.py
    ├── amadeus_api.py
    └── requirements.txt
```

## Setup Instructions

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables in `.env`:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   AMADEUS_API_KEY=your_amadeus_api_key
   AMADEUS_API_SECRET=your_amadeus_secret
   PRIV_KEY=your_firebase_admin_sdk_json
   ```

4. Start the Flask server:
   ```bash
   python app.py
   ```
   Server will run on http://localhost:5000

### Frontend Setup

1. Configure Firebase:
   - Update Firebase configuration in `js/auth.js`
   - Enable Authentication in Firebase Console
   - Set up Firestore rules

2. Serve the frontend:
   - Use any local server (e.g., Live Server in VS Code)
   - Access via http://localhost:8000

## API Endpoints

### Chat API
- `POST /api/chat`
  - Handles AI assistant interactions
  - Uses Gemini API for responses

### Flight Search
- `POST /api/flights/search`
  - Search flights with filters
  - Integrates with Amadeus API

### Authentication
- `POST /api/auth/token`
  - Manages Amadeus API authentication
  - Handles user sessions

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Development Notes

- The AI assistant uses Gemini 1.5 Flash model for faster responses
- CORS is enabled for local development
- Firebase is used for both authentication and data storage
- Amadeus API is used in test mode

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is created for educational purposes as part of a school project.

## Deployment

### GitHub Setup

1. Create a new GitHub repository
2. Add your project files:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin your-repository-url
   git push -u origin main
   ```

3. Set up GitHub Secrets:
   - Go to your repository Settings > Secrets and Variables > Actions
   - Add the following secrets:
     ```
     GEMINI_API_KEY=your_gemini_api_key
     AMADEUS_API_KEY=your_amadeus_api_key
     AMADEUS_API_SECRET=your_amadeus_secret
     FIREBASE_ADMIN_SDK=your_entire_firebase_admin_sdk_json
     ```

### Frontend Deployment (GitHub Pages)

1. In your repository settings, enable GitHub Pages
2. Select the branch to deploy (usually `main`)
3. Set the folder to `/frontend`
4. Your site will be available at `https://your-username.github.io/repository-name`

### Backend Deployment Options

1. **Heroku (Free Tier Discontinued)**:
   - Create a new Heroku app
   - Connect your GitHub repository
   - Add your environment variables in Heroku Settings
   - Deploy the backend folder

2. **Railway.app (Recommended)**:
   - Create a new project
   - Connect your GitHub repository
   - Add environment variables
   - Set the build command: `pip install -r requirements.txt`
   - Set the start command: `python app.py`

3. **Render.com (Alternative)**:
   - Create a new Web Service
   - Connect your GitHub repository
   - Add environment variables
   - Set build command and start command

### Post-Deployment Setup

1. Update API endpoints in frontend code:
   ```javascript
   // In chatbot.js, update the API URL:
   const API_URL = 'https://your-backend-url.com/api/chat';
   ```

2. Update CORS settings in backend:
   ```python
   # In app.py, update CORS settings:
   CORS(app, origins=['https://your-username.github.io'])
   ```

3. Update Firebase configuration:
   - Add your deployed domain to Firebase Console > Authentication > Settings > Authorized Domains

### Important Security Notes

1. Never commit sensitive data:
   ```gitignore
   # .gitignore
   .env
   **/serviceAccountKey.json
   **/*.pem
   ```

2. Keep your API keys secure:
   - Use environment variables
   - Don't expose keys in frontend code
   - Use backend proxy for API calls

3. Firebase Security:
   - Set up proper Firestore rules
   - Configure Authentication providers
   - Restrict API access in Google Cloud Console 