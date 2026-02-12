"""Grok API Integration for AI-powered fashion recommendations"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class GrokAPI:
    """Interface for xAI's Grok API"""
    
    def __init__(self):
        self.api_key = os.getenv('XAI_API_KEY')
        self.base_url = "https://api.x.ai/v1"
        self.model = "grok-beta"  # or "grok-vision-beta" for image analysis
        
        if not self.api_key:
            print("Warning: XAI_API_KEY not found in environment variables")
    
    def generate_style_recommendations(self, skin_tone, undertone, gender, occasion, vibe, budget):
        """
        Generate personalized fashion recommendations using Grok
        """
        
        prompt = f"""You are a professional fashion stylist. Based on the following information, provide personalized fashion advice:

Skin Tone: {skin_tone}
Undertone: {undertone}
Gender: {gender}
Occasion: {occasion}
Style Vibe: {vibe}
Budget: {budget}

Please provide:
1. Why these colors work well for this skin tone and undertone
2. Specific outfit suggestions (be creative and detailed)
3. Accessory recommendations
4. Hairstyle suggestions
5. Styling tips

Keep the response natural, friendly, and practical. Focus on Indian fashion context and availability."""

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert fashion stylist with deep knowledge of color theory, skin tones, and Indian fashion trends."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "model": self.model,
                "stream": False,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'advice': result['choices'][0]['message']['content'],
                    'model': result.get('model', self.model)
                }
            else:
                return {
                    'success': False,
                    'error': f"API Error: {response.status_code}",
                    'details': response.text
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def analyze_image_with_grok(self, image_path):
        """
        Use Grok Vision to analyze uploaded image
        (Optional: for enhanced image analysis)
        """
        
        try:
            # Read image and convert to base64
            import base64
            with open(image_path, 'rb') as img_file:
                image_data = base64.b64encode(img_file.read()).decode('utf-8')
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analyze this person's skin tone, face shape, and provide fashion styling recommendations. Be specific about colors that would suit them."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                "model": "grok-vision-beta",
                "stream": False,
                "temperature": 0.5
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'analysis': result['choices'][0]['message']['content']
                }
            else:
                return {
                    'success': False,
                    'error': f"Vision API Error: {response.status_code}"
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_personalized_explanation(self, skin_tone, undertone, colors, occasion):
        """
        Generate a personalized explanation for why certain colors work
        """
        
        color_names = ', '.join([c['name'] for c in colors[:3]])
        
        prompt = f"""In 2-3 friendly sentences, explain why {color_names} colors are perfect for someone with {skin_tone} skin and {undertone} undertones for {occasion} occasions. Be warm and encouraging."""
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "model": self.model,
                "stream": False,
                "temperature": 0.8,
                "max_tokens": 150
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                # Fallback to default explanation
                return f'These {color_names} colors are specially chosen for your {skin_tone.lower()} skin tone with {undertone} undertones. Perfect for {occasion} occasions!'
                
        except Exception as e:
            print(f"Explanation generation error: {e}")
            return f'These {color_names} colors are specially chosen for your {skin_tone.lower()} skin tone with {undertone} undertones. Perfect for {occasion} occasions!'

# Test function
if __name__ == "__main__":
    grok = GrokAPI()
    
    # Test recommendation generation
    result = grok.generate_style_recommendations(
        skin_tone="Medium",
        undertone="warm",
        gender="female",
        occasion="party",
        vibe="elegant",
        budget="medium"
    )
    
    print("Grok API Test:")
    print(result)
