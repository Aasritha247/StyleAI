# StyleAI+ – AI Powered Fashion Styling Advisor

An intelligent personal fashion assistant that analyzes facial photos, detects skin tone, and generates personalized styling recommendations using Google Gemini AI.

## Features
- Face detection & skin tone analysis
- AI-powered outfit recommendations
- Virtual wardrobe management
- Smart shopping assistant
- Style preference learning
- Weather & budget-aware suggestions
- Multilingual support (English, Hindi, Telugu)

## Tech Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python (Flask)
- AI: Google Gemini API
- Image Processing: OpenCV, Pillow, NumPy
- Storage: SQLite

## Setup Instructions

### Prerequisites
- Python 3.8+
- Google AI Studio API Key

### Installation

1. Install dependencies:
```bash
pip install flask opencv-python pillow numpy requests google-generativeai
```

2. Set your Gemini API key:
```bash
set GEMINI_API_KEY=your_api_key_here
```

3. Run the server:
```bash
python server.py
```

4. Open browser:
```
http://localhost:5000
```

## API Endpoints
- `POST /upload` - Upload face image
- `POST /analyze` - Analyze skin tone
- `POST /recommend` - Get AI styling recommendations
- `POST /wardrobe` - Manage virtual wardrobe
- `POST /feedback` - Submit style feedback

## Project Structure
```
StyleAI+/
├── server.py           # Main Flask server
├── skin_analyzer.py    # Skin tone detection
├── ai_stylist.py       # Gemini AI integration
├── database.py         # SQLite database
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── templates/
│   └── index.html
├── uploads/            # Temporary image storage
└── data/
    └── styleai.db      # SQLite database
```

## Security
- Images deleted after analysis
- No permanent face storage
- Temporary session-based processing
