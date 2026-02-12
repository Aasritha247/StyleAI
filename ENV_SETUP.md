# Environment Variables Setup for StyleAI+

## What is a .env file?
A `.env` file stores sensitive configuration data like API keys that shouldn't be shared publicly on GitHub.

## Quick Setup

### Step 1: Get Your Grok API Key
1. Go to [xAI Console](https://console.x.ai/)
2. Sign in or create an account
3. Navigate to API Keys section
4. Click "Create API Key"
5. Copy the generated API key

**Alternative: Use Gemini API**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

### Step 2: Create .env File
```bash
# Copy the example file
copy .env.example .env
```

### Step 3: Add Your API Key
Open `.env` file in any text editor and replace the placeholder:

**For Grok (Recommended):**
```env
XAI_API_KEY=xai-1234567890abcdefghijklmnopqrstuvwxyz
AI_PROVIDER=grok
```

**For Gemini:**
```env
GEMINI_API_KEY=AIzaSyC...paste_your_actual_key_here
AI_PROVIDER=gemini
```

### Step 4: Verify Setup
The `.env` file should look like this:

**For Grok:**
```env
# StyleAI+ Environment Variables

# Grok API Key (xAI)
XAI_API_KEY=xai-1234567890abcdefghijklmnopqrstuvwxyz

# AI Provider Selection
AI_PROVIDER=grok

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Upload Configuration
MAX_UPLOAD_SIZE=5242880
ALLOWED_EXTENSIONS=jpg,jpeg,png,webp

# Database (if needed later)
DATABASE_URL=sqlite:///styleai.db
```

**For Gemini:**
```env
# StyleAI+ Environment Variables

# Google AI Studio API Key (Gemini)
GEMINI_API_KEY=AIzaSyC1234567890abcdefghijklmnopqrstuvwxyz

# AI Provider Selection
AI_PROVIDER=gemini

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Upload Configuration
MAX_UPLOAD_SIZE=5242880
ALLOWED_EXTENSIONS=jpg,jpeg,png,webp

# Database (if needed later)
DATABASE_URL=sqlite:///styleai.db
```

## Important Notes

⚠️ **Security**
- NEVER commit `.env` file to GitHub
- NEVER share your API key publicly
- The `.env` file is already in `.gitignore` to prevent accidental commits

✅ **What to Share**
- Share `.env.example` (template without real keys)
- Share setup instructions
- Share this ENV_SETUP.md file

## Using the API Key in Code

The application will automatically load the `.env` file using `python-dotenv`:

```python
from dotenv import load_dotenv
import os

load_dotenv()

# For Grok
xai_api_key = os.getenv('XAI_API_KEY')

# For Gemini
gemini_api_key = os.getenv('GEMINI_API_KEY')

# Check which provider to use
ai_provider = os.getenv('AI_PROVIDER', 'grok')
```

## Troubleshooting

### "API key not found" error
- Make sure `.env` file exists in the root directory
- Check that `XAI_API_KEY` (for Grok) or `GEMINI_API_KEY` (for Gemini) is spelled correctly
- Verify there are no extra spaces around the `=` sign
- Make sure `python-dotenv` is installed: `pip install python-dotenv`

### "Invalid API key" error
- Verify your API key is correct
- For Grok: Check if the API key is active in [xAI Console](https://console.x.ai/)
- For Gemini: Check if the API key is active in Google AI Studio
- Make sure you copied the entire key (no truncation)

### "Rate limit exceeded" error
- Grok API has rate limits based on your plan
- Wait a few minutes before trying again
- Consider upgrading your xAI plan for higher limits

### File not loading
- Ensure `.env` is in the same directory as `server_simple.py`
- Check file encoding (should be UTF-8)
- Restart the server after creating/modifying `.env`

## Alternative: Environment Variables Without .env

If you don't want to use a `.env` file, you can set environment variables directly:

**Windows CMD:**
```cmd
set XAI_API_KEY=your_key_here
set AI_PROVIDER=grok
python server_simple.py
```

**Windows PowerShell:**
```powershell
$env:XAI_API_KEY="your_key_here"
$env:AI_PROVIDER="grok"
python server_simple.py
```

**Linux/Mac:**
```bash
export XAI_API_KEY=your_key_here
export AI_PROVIDER=grok
python server_simple.py
```

## For Deployment

When deploying to production (Heroku, Render, etc.), set environment variables in the platform's dashboard instead of using a `.env` file.

### Heroku Example:
```bash
heroku config:set XAI_API_KEY=your_key_here
heroku config:set AI_PROVIDER=grok
```

### Render Example:
Add environment variables in the Render dashboard under "Environment" section:
- `XAI_API_KEY` = your_key_here
- `AI_PROVIDER` = grok

## Grok API Resources

- [xAI Console](https://console.x.ai/) - Get API keys
- [xAI Documentation](https://docs.x.ai/) - API documentation
- [Grok API Pricing](https://x.ai/pricing) - Check pricing and limits

---

Need help? Check the [SETUP_GUIDE.md](SETUP_GUIDE.md) for complete installation instructions.
