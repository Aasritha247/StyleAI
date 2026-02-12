# 🚀 Grok API Setup - Quick Summary

## What You Need

1. **Grok API Key** from [xAI Console](https://console.x.ai/)
2. **Python 3.8+** installed
3. **Internet connection**

## 3-Step Setup

### Step 1: Get API Key
```
1. Go to https://console.x.ai/
2. Sign up/Login
3. Create API Key
4. Copy the key (starts with "xai-")
```

### Step 2: Configure
```bash
# Run the setup script
setup_grok.bat

# OR manually:
copy .env.example .env
# Then edit .env and add your key
```

Your `.env` should look like:
```env
XAI_API_KEY=xai-1234567890abcdefghijklmnopqrstuvwxyz
AI_PROVIDER=grok
```

### Step 3: Run
```bash
# Install dependencies
pip install -r requirements.txt

# Start server
python server_simple.py

# Open browser
http://localhost:5000
```

## Files Created for Grok Integration

✅ `grok_api.py` - Grok API integration module
✅ `.env` - Your API keys (DO NOT commit to GitHub)
✅ `.env.example` - Template for sharing
✅ `ENV_SETUP.md` - Detailed setup guide
✅ `GROK_INTEGRATION.md` - Complete integration docs
✅ `setup_grok.bat` - Automated setup script
✅ `requirements.txt` - Updated with dependencies

## What Grok Does in Your App

🎨 **Personalized Explanations**
- Generates custom color recommendations
- Explains why colors work for your skin tone
- Adapts to occasion and style preferences

🤖 **AI-Powered Advice** (Optional Enhancement)
- Complete outfit suggestions
- Styling tips
- Trend insights

👁️ **Vision Analysis** (Optional)
- Advanced image analysis
- Face shape detection
- Style personality assessment

## Testing Grok Integration

1. Upload a photo
2. Select preferences (occasion, vibe, budget)
3. Click "Analyze My Style"
4. Check the explanation text - if it's natural and personalized, Grok is working!

## Fallback Behavior

If Grok API is not configured or fails:
- App still works perfectly
- Uses template-based explanations
- All features remain functional

## Cost & Limits

- **Free Tier**: Limited requests per month
- **Paid Plans**: Higher limits, faster responses
- Check [xAI Pricing](https://x.ai/pricing)

## Need Help?

📖 **Detailed Guides:**
- `ENV_SETUP.md` - Environment setup
- `GROK_INTEGRATION.md` - Full integration guide
- `SETUP_GUIDE.md` - General setup

🔗 **Resources:**
- [xAI Console](https://console.x.ai/)
- [xAI Documentation](https://docs.x.ai/)
- [GitHub Issues](https://github.com/Aasritha247/StyleAI/issues)

## Quick Troubleshooting

**"API key not found"**
→ Check `.env` file exists and has `XAI_API_KEY=your_key`

**"Invalid API key"**
→ Verify key in xAI Console, check for typos

**"Rate limit exceeded"**
→ Wait a few minutes or upgrade plan

**App works but no AI explanations**
→ Check console logs, verify `AI_PROVIDER=grok` in `.env`

## Alternative: Use Without Grok

Don't want to use Grok? No problem!
```env
# Leave XAI_API_KEY empty or remove it
AI_PROVIDER=none
```

The app will use built-in template recommendations.

---

**Ready to go!** Run `setup_grok.bat` or follow Step 2 above. 🎉
