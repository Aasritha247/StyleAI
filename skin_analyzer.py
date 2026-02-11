import cv2
import numpy as np
from PIL import Image

class SkinAnalyzer:
    """Analyzes facial images to detect skin tone and undertone"""
    
    def __init__(self):
        # Load face detection cascade
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
    
    def analyze(self, image_path):
        """Main analysis function"""
        try:
            # Read image
            img = cv2.imread(image_path)
            if img is None:
                return {'error': 'Could not read image'}
            
            # Detect face
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) == 0:
                return {'error': 'No face detected'}
            
            # Get largest face
            x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
            
            # Extract face region
            face_roi = img[y:y+h, x:x+w]
            
            # Extract skin region (cheek area)
            skin_region = self._extract_skin_region(face_roi)
            
            # Calculate average color
            avg_color = self._calculate_average_color(skin_region)
            
            # Classify skin tone
            skin_tone = self._classify_skin_tone(avg_color)
            
            # Detect undertone
            undertone = self._detect_undertone(avg_color)
            
            return {
                'success': True,
                'skin_tone': skin_tone,
                'undertone': undertone,
                'rgb': avg_color.tolist(),
                'hex': self._rgb_to_hex(avg_color)
            }
        
        except Exception as e:
            return {'error': str(e)}
    
    def _extract_skin_region(self, face_roi):
        """Extract skin region from face (cheek area)"""
        h, w = face_roi.shape[:2]
        
        # Define cheek regions (avoid eyes, nose, mouth)
        cheek_left = face_roi[int(h*0.4):int(h*0.7), int(w*0.1):int(w*0.35)]
        cheek_right = face_roi[int(h*0.4):int(h*0.7), int(w*0.65):int(w*0.9)]
        
        # Combine cheeks
        skin_region = np.vstack([cheek_left, cheek_right])
        
        return skin_region
    
    def _calculate_average_color(self, region):
        """Calculate average RGB color"""
        # Convert BGR to RGB
        region_rgb = cv2.cvtColor(region, cv2.COLOR_BGR2RGB)
        
        # Calculate mean
        avg_color = np.mean(region_rgb.reshape(-1, 3), axis=0)
        
        return avg_color.astype(int)
    
    def _classify_skin_tone(self, rgb):
        """Classify skin tone into categories"""
        # Calculate brightness
        brightness = (rgb[0] + rgb[1] + rgb[2]) / 3
        
        if brightness > 200:
            return 'Fair'
        elif brightness > 160:
            return 'Medium'
        elif brightness > 120:
            return 'Olive'
        else:
            return 'Deep'
    
    def _detect_undertone(self, rgb):
        """Detect warm/cool/neutral undertone"""
        r, g, b = rgb
        
        # Calculate ratios
        red_ratio = r / (g + b + 1)
        blue_ratio = b / (r + g + 1)
        
        if red_ratio > 0.55:
            return 'warm'
        elif blue_ratio > 0.35:
            return 'cool'
        else:
            return 'neutral'
    
    def _rgb_to_hex(self, rgb):
        """Convert RGB to hex color"""
        return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
