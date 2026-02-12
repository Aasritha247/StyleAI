# Grok API Integration Guide

## Overview
StyleAI+ now supports xAI's Grok API for enhanced AI-powered fashion recommendations. Grok provides more natural, conversational, and personalized styling advice.

## Why Grok?
- **Advanced Language Understanding**: Better context awareness for fashion advice
- **Real-time Knowledge**: Up-to-date fashion trends and recommendations
- **Natural Conversations**: More human-like styling suggestions
- **Vision Capabilities**: Optional image analysis with Grok Vision

## Quick Start

### 1. Get Grok API Key
1. Visit [xAI Console](https://console.x.ai/)
2. Sign up or log in
3. Navigate to "API Keys"
4. Create a new API key
5. Copy the key (starts with `xai-`)

### 2. Configure Environment
Edit your `.env` file:
```env
XAI_API_KEY=xai-your-actual-key-here
AI_PROVIDER=grok
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python server_simple.py
```

## Features Powered by Grok

### 1. Personalized Explanations
Grok generates custom explanations for why certain colors and styles work for each user:
- Considers skin tone and undertone
- Adapts to occasion and vibe
- Provides warm, encouraging advice

### 2. Enhanced Recommendations (Optional)
You can extend the integration to get:
- Complete outfit suggestions
- Styling tips and tricks
- Seasonal recommendations
- Trend insights

### 3. Vision Analysis (Optional)
Use Grok Vision for advanced image analysis:
- Face shape detection
- Color harmony analysis
- Style personality assessment

## API Usage

### Basic Text Generation
```python
from grok_api import GrokAPI

grok = GrokAPI()

result = grok.generate_style_recommendations(
    skin_tone="Medium",
    undertone="warm",
    gender="female",
    occasion="party",
    vibe="elegant",
    budget="medium"
)

print(result['advice'])
```

### Personalized Explanation
```python
explanation = grok.get_personalized_explanation(
    skin_tone="Fair",
    undertone="cool",
    colors=[
        {'name': 'Lavender', 'hex': '#E6E6FA'},
        {'name': 'Navy Blue', 'hex': '#000080'}
    ],
    occasion="work"
)
```

### Vision Analysis (Optional)
```python
result = grok.analyze_image_with_grok('path/to/image.jpg')
print(result['analysis'])
```

## Configuration Options

### Environment Variables
```env
# Required
XAI_API_KEY=xai-your-key-here

# Optional
AI_PROVIDER=grok              # or 'gemini' for Google AI
GROK_MODEL=grok-beta          # or 'grok-vision-beta'
GROK_TEMPERATURE=0.7          # 0.0 to 1.0 (creativity level)
GROK_MAX_TOKENS=500           # Response length limit
```

### Model Selection
- `grok-beta`: Standard text generation (recommended)
- `grok-vision-beta`: Image analysis capabilities

## Rate Limits & Pricing

### Free Tier
- Limited requests per month
- Standard response times
- Basic features

### Paid Plans
- Higher rate limits
- Faster responses
- Priority access
- Vision API access

Check [xAI Pricing](https://x.ai/pricing) for current rates.

## Error Handling

The integration includes automatic fallbacks:

```python
# If Grok API fails, uses default explanations
if grok_api and ai_provider == 'grok':
    try:
        explanation = grok_api.get_personalized_explanation(...)
    except Exception as e:
        # Falls back to template-based explanation
        explanation = default_explanation
```

## Troubleshooting

### "API key not found"
- Check `.env` file exists
- Verify `XAI_API_KEY` is set correctly
- Restart the server after editing `.env`

### "Rate limit exceeded"
- Wait a few minutes
- Check your xAI dashboard for usage
- Consider upgrading your plan

### "Invalid API key"
- Verify key is active in xAI Console
- Check for typos or extra spaces
- Regenerate key if needed

### "Connection timeout"
- Check internet connection
- Verify xAI API status
- Increase timeout in `grok_api.py`

## Advanced Usage

### Custom Prompts
Modify `grok_api.py` to customize prompts:

```python
prompt = f"""You are a fashion expert specializing in {specialty}.
Based on: {user_data}
Provide: {requirements}
Style: {tone}"""
```

### Streaming Responses
Enable streaming for real-time responses:

```python
payload = {
    "stream": True,  # Enable streaming
    "messages": messages
}
```

### Temperature Control
Adjust creativity level:
- `0.0-0.3`: Conservative, factual
- `0.4-0.7`: Balanced (recommended)
- `0.8-1.0`: Creative, varied

## Comparison: Grok vs Gemini

| Feature | Grok | Gemini |
|---------|------|--------|
| Fashion Knowledge | Excellent | Good |
| Response Speed | Fast | Very Fast |
| Cost | Moderate | Free tier available |
| Vision API | Yes | Yes |
| Indian Context | Good | Excellent |
| Customization | High | Medium |

## Best Practices

1. **Cache Responses**: Store common recommendations to reduce API calls
2. **Batch Requests**: Combine multiple queries when possible
3. **Error Handling**: Always have fallback content
4. **Rate Limiting**: Implement client-side throttling
5. **User Privacy**: Don't send sensitive data to API

## Future Enhancements

Planned features:
- [ ] Full outfit generation with Grok
- [ ] Style evolution tracking
- [ ] Trend prediction
- [ ] Virtual try-on suggestions
- [ ] Wardrobe analysis with Vision API

## Support

- **xAI Documentation**: https://docs.x.ai/
- **xAI Console**: https://console.x.ai/
- **Community**: https://x.ai/community
- **Issues**: Report bugs in GitHub Issues

## License
This integration follows xAI's Terms of Service and API usage guidelines.

---

**Note**: Grok API is optional. The application works without it using template-based recommendations.
