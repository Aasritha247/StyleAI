# StyleAI+ Setup Guide

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

## Installation Steps

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd StyleAI-Plus
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

**Option 1: Using .env file (Recommended)**
```bash
# Copy the example file
copy .env.example .env

# Edit .env file and add your actual Gemini API key
# Get your API key from: https://makersuite.google.com/app/apikey
```

Open `.env` file and replace `your_gemini_api_key_here` with your actual API key:
```
GEMINI_API_KEY=AIzaSyC...your_actual_key_here
```

**Option 2: Set environment variable directly in terminal**

**Windows (CMD):**
```cmd
set GEMINI_API_KEY=your_api_key_here
```

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

**Linux/Mac:**
```bash
export GEMINI_API_KEY=your_api_key_here
```

### 4. Run the Application
```bash
python server_simple.py
```

### 5. Open in Browser
Navigate to: `http://localhost:5000`

## Features
- 🎨 AI-powered skin tone analysis
- 👗 Personalized outfit recommendations
- 💎 Accessory and hairstyle suggestions
- 🛍️ Direct shopping links (Amazon, Flipkart, Myntra)
- 🌍 Multilingual support (English, Hindi, Telugu)
- 🎭 Gender-based themes
- 📸 Camera and file upload support

## Troubleshooting

### OpenCV Installation Issues
If you face issues with OpenCV:
```bash
pip install opencv-python-headless
```

### Port Already in Use
Change the port in `server_simple.py`:
```python
app.run(debug=True, host='127.0.0.1', port=5001)
```

## Project Structure
```
StyleAI+/
├── server_simple.py          # Main Flask server
├── skin_analyzer.py          # Skin tone detection
├── ai_stylist.py            # AI recommendations
├── shopping_api.py          # Shopping integration
├── database.py              # SQLite database
├── templates/
│   └── index.html           # Main UI
├── static/
│   ├── css/
│   │   └── style.css        # Styling
│   └── js/
│       └── app.js           # Frontend logic
└── requirements.txt         # Dependencies
```

## Contributing
Feel free to submit issues and pull requests!

## License
MIT License
