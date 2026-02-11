import os
import google.generativeai as genai
import json

class AIStylist:
    """AI-powered styling recommendations using Google Gemini"""
    
    def __init__(self):
        # Configure Gemini API
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
            print("Warning: GEMINI_API_KEY not set. Using fallback recommendations.")
    
    def generate_recommendations(self, skin_tone, undertone, gender='female', 
                                vibe='casual', weather='moderate', budget='medium', 
                                occasion='daily'):
        """Generate personalized styling recommendations"""
        
        if self.model:
            return self._generate_with_ai(skin_tone, undertone, gender, vibe, 
                                         weather, budget, occasion)
        else:
            return self._generate_fallback(skin_tone, undertone, gender, vibe)
    
    def _generate_with_ai(self, skin_tone, undertone, gender, vibe, 
                         weather, budget, occasion):
        """Generate recommendations using Gemini AI"""
        
        prompt = f"""You are an expert fashion stylist. Generate personalized styling advice.

User Profile:
- Skin Tone: {skin_tone}
- Undertone: {undertone}
- Gender: {gender}
- Desired Vibe: {vibe}
- Weather: {weather}
- Budget: {budget}
- Occasion: {occasion}

Provide recommendations in JSON format with these sections:
1. color_palette: Array of 5 colors that suit this skin tone (with hex codes)
2. outfits: Array of 3 complete outfit suggestions with items
3. accessories: Array of 5 accessory suggestions
4. hairstyle: 2 hairstyle suggestions
5. shopping_tips: 3 practical shopping tips for India
6. explanation: Why these recommendations suit the user

Keep it practical, India-friendly, and culturally appropriate. Use Indian fashion brands when possible.

Return ONLY valid JSON, no markdown formatting."""

        try:
            response = self.model.generate_content(prompt)
            
            # Parse JSON from response
            text = response.text.strip()
            if text.startswith('```json'):
                text = text[7:]
            if text.endswith('```'):
                text = text[:-3]
            
            recommendations = json.loads(text.strip())
            recommendations['success'] = True
            
            return recommendations
        
        except Exception as e:
            print(f"AI generation error: {e}")
            return self._generate_fallback(skin_tone, undertone, gender, vibe)
    
    def _generate_fallback(self, skin_tone, undertone, gender, vibe):
        """Fallback recommendations when AI is unavailable"""
        
        # Color recommendations based on skin tone and undertone
        color_palettes = {
            'Fair_warm': ['#E8B4A0', '#D4A574', '#8B4513', '#FF6B6B', '#FFD93D'],
            'Fair_cool': ['#B4C7E7', '#8E7CC3', '#E91E63', '#00BCD4', '#9C27B0'],
            'Fair_neutral': ['#FFB6C1', '#87CEEB', '#98D8C8', '#F7DC6F', '#E8DAEF'],
            'Medium_warm': ['#D4A574', '#CD853F', '#FF8C42', '#E74C3C', '#F39C12'],
            'Medium_cool': ['#5DADE2', '#AF7AC5', '#EC7063', '#48C9B0', '#5499C7'],
            'Medium_neutral': ['#F8B88B', '#FAD7A0', '#A9DFBF', '#D7BDE2', '#AED6F1'],
            'Olive_warm': ['#8B4513', '#CD853F', '#D35400', '#E67E22', '#F39C12'],
            'Olive_cool': ['#117A65', '#1F618D', '#7D3C98', '#C0392B', '#2874A6'],
            'Olive_neutral': ['#A04000', '#D68910', '#229954', '#5B2C6F', '#1A5490'],
            'Deep_warm': ['#FF6B35', '#F7931E', '#FFC300', '#E74C3C', '#D35400'],
            'Deep_cool': ['#8E44AD', '#2980B9', '#E91E63', '#16A085', '#2C3E50'],
            'Deep_neutral': ['#E74C3C', '#F39C12', '#27AE60', '#8E44AD', '#2980B9']
        }
        
        key = f"{skin_tone}_{undertone}"
        colors = color_palettes.get(key, color_palettes['Medium_neutral'])
        
        return {
            'success': True,
            'color_palette': [
                {'name': 'Primary', 'hex': colors[0]},
                {'name': 'Secondary', 'hex': colors[1]},
                {'name': 'Accent', 'hex': colors[2]},
                {'name': 'Neutral', 'hex': colors[3]},
                {'name': 'Pop', 'hex': colors[4]}
            ],
            'outfits': [
                {
                    'name': f'{vibe.capitalize()} Look 1',
                    'items': ['Kurta', 'Palazzo', 'Dupatta'],
                    'colors': [colors[0], colors[1], colors[3]]
                },
                {
                    'name': f'{vibe.capitalize()} Look 2',
                    'items': ['Top', 'Jeans', 'Jacket'],
                    'colors': [colors[2], colors[4], colors[1]]
                },
                {
                    'name': f'{vibe.capitalize()} Look 3',
                    'items': ['Dress', 'Belt', 'Shoes'],
                    'colors': [colors[0], colors[2], colors[3]]
                }
            ],
            'accessories': [
                'Statement earrings',
                'Layered necklace',
                'Woven handbag',
                'Sunglasses',
                'Ankle boots'
            ],
            'hairstyle': [
                'Soft waves with side part',
                'Sleek low bun with face-framing layers'
            ],
            'shopping_tips': [
                'Look for natural fabrics like cotton and linen for Indian weather',
                'Mix traditional and western pieces for versatile styling',
                'Invest in neutral basics and add color with accessories'
            ],
            'explanation': f'These recommendations complement your {skin_tone.lower()} skin tone with {undertone} undertones. The color palette enhances your natural beauty while the outfit suggestions match your {vibe} style preference.'
        }
    
    def mix_and_match(self, wardrobe_items, occasion='casual'):
        """Generate outfit combinations from wardrobe"""
        
        if not wardrobe_items or len(wardrobe_items) < 2:
            return {'error': 'Not enough items in wardrobe'}
        
        # Simple matching logic
        tops = [item for item in wardrobe_items if item.get('type') in ['top', 'shirt', 'kurta']]
        bottoms = [item for item in wardrobe_items if item.get('type') in ['bottom', 'jeans', 'skirt', 'palazzo']]
        
        if tops and bottoms:
            return {
                'success': True,
                'outfit': {
                    'top': tops[0],
                    'bottom': bottoms[0],
                    'occasion': occasion
                }
            }
        
        return {'error': 'Unable to create outfit combination'}
