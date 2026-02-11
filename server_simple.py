"""Simplified server without heavy dependencies"""
from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime
from shopping_api import ShoppingAPI

print("Starting StyleAI+ Simple Server...")

# Initialize shopping API
shopping_api = ShoppingAPI()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs('uploads', exist_ok=True)

@app.route('/')
def index():
    print("Index page requested")
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    print("Upload endpoint called")
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return jsonify({'success': True, 'filepath': filepath, 'filename': filename})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze_skin():
    print("Analyze endpoint called")
    try:
        data = request.json
        filepath = data.get('filepath')
        
        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'Invalid file path'}), 400
        
        # Simple image-based analysis using PIL
        from PIL import Image
        import hashlib
        
        # Open image
        img = Image.open(filepath)
        img = img.convert('RGB')
        
        # Get average color from center region (face area)
        width, height = img.size
        center_box = (
            width // 4, height // 4,
            3 * width // 4, 3 * height // 4
        )
        center_region = img.crop(center_box)
        
        # Calculate average RGB
        pixels = list(center_region.getdata())
        avg_r = sum(p[0] for p in pixels) // len(pixels)
        avg_g = sum(p[1] for p in pixels) // len(pixels)
        avg_b = sum(p[2] for p in pixels) // len(pixels)
        
        # Calculate brightness
        brightness = (avg_r + avg_g + avg_b) / 3
        
        # Classify skin tone based on brightness
        if brightness > 200:
            skin_tone = 'Fair'
        elif brightness > 160:
            skin_tone = 'Medium'
        elif brightness > 120:
            skin_tone = 'Olive'
        else:
            skin_tone = 'Deep'
        
        # Detect undertone based on color ratios
        red_ratio = avg_r / (avg_g + avg_b + 1)
        blue_ratio = avg_b / (avg_r + avg_g + 1)
        
        if red_ratio > 0.55:
            undertone = 'warm'
        elif blue_ratio > 0.35:
            undertone = 'cool'
        else:
            undertone = 'neutral'
        
        # Convert to hex
        hex_color = '#{:02x}{:02x}{:02x}'.format(avg_r, avg_g, avg_b)
        
        # Delete image after analysis
        try:
            os.remove(filepath)
        except:
            pass
        
        print(f"Analysis result: {skin_tone} skin with {undertone} undertone")
        
        return jsonify({
            'success': True,
            'skin_tone': skin_tone,
            'undertone': undertone,
            'rgb': [avg_r, avg_g, avg_b],
            'hex': hex_color
        })
        
    except Exception as e:
        print(f"Analysis error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    print("Recommend endpoint called")
    data = request.json
    occasion = data.get('occasion', 'daily')
    budget = data.get('budget', 'medium')
    skin_tone = data.get('skin_tone', 'Medium')
    undertone = data.get('undertone', 'warm')
    vibe = data.get('vibe', 'casual')
    
    # Personalized color palettes based on skin tone and undertone
    color_palettes = {
        'Fair_warm': [
            {'name': 'Peach', 'hex': '#FFDAB9'},
            {'name': 'Coral', 'hex': '#FF7F50'},
            {'name': 'Warm Brown', 'hex': '#8B4513'},
            {'name': 'Golden Yellow', 'hex': '#FFD700'},
            {'name': 'Rust Orange', 'hex': '#B7410E'}
        ],
        'Fair_cool': [
            {'name': 'Baby Pink', 'hex': '#F4C2C2'},
            {'name': 'Lavender', 'hex': '#E6E6FA'},
            {'name': 'Navy Blue', 'hex': '#000080'},
            {'name': 'Emerald Green', 'hex': '#50C878'},
            {'name': 'Royal Purple', 'hex': '#7851A9'}
        ],
        'Fair_neutral': [
            {'name': 'Soft Pink', 'hex': '#FFB6C1'},
            {'name': 'Sky Blue', 'hex': '#87CEEB'},
            {'name': 'Mint Green', 'hex': '#98FF98'},
            {'name': 'Lemon Yellow', 'hex': '#FFF44F'},
            {'name': 'Lilac', 'hex': '#C8A2C8'}
        ],
        'Medium_warm': [
            {'name': 'Terracotta', 'hex': '#E2725B'},
            {'name': 'Olive Green', 'hex': '#808000'},
            {'name': 'Burnt Orange', 'hex': '#CC5500'},
            {'name': 'Mustard Yellow', 'hex': '#FFDB58'},
            {'name': 'Warm Red', 'hex': '#DC143C'}
        ],
        'Medium_cool': [
            {'name': 'Teal', 'hex': '#008080'},
            {'name': 'Magenta', 'hex': '#FF00FF'},
            {'name': 'Cool Pink', 'hex': '#FF69B4'},
            {'name': 'Turquoise', 'hex': '#40E0D0'},
            {'name': 'Plum', 'hex': '#8E4585'}
        ],
        'Medium_neutral': [
            {'name': 'Rose Gold', 'hex': '#B76E79'},
            {'name': 'Sage Green', 'hex': '#9DC183'},
            {'name': 'Dusty Rose', 'hex': '#DCAE96'},
            {'name': 'Soft Coral', 'hex': '#F88379'},
            {'name': 'Periwinkle', 'hex': '#CCCCFF'}
        ],
        'Olive_warm': [
            {'name': 'Army Green', 'hex': '#4B5320'},
            {'name': 'Bronze', 'hex': '#CD7F32'},
            {'name': 'Camel', 'hex': '#C19A6B'},
            {'name': 'Burnt Sienna', 'hex': '#E97451'},
            {'name': 'Warm Beige', 'hex': '#D2B48C'}
        ],
        'Olive_cool': [
            {'name': 'Forest Green', 'hex': '#228B22'},
            {'name': 'Deep Purple', 'hex': '#673AB7'},
            {'name': 'Burgundy', 'hex': '#800020'},
            {'name': 'Slate Blue', 'hex': '#6A5ACD'},
            {'name': 'Charcoal', 'hex': '#36454F'}
        ],
        'Olive_neutral': [
            {'name': 'Khaki', 'hex': '#C3B091'},
            {'name': 'Moss Green', 'hex': '#8A9A5B'},
            {'name': 'Taupe', 'hex': '#483C32'},
            {'name': 'Mauve', 'hex': '#E0B0FF'},
            {'name': 'Steel Blue', 'hex': '#4682B4'}
        ],
        'Deep_warm': [
            {'name': 'Rich Gold', 'hex': '#FFD700'},
            {'name': 'Bright Orange', 'hex': '#FF8C00'},
            {'name': 'Crimson', 'hex': '#DC143C'},
            {'name': 'Amber', 'hex': '#FFBF00'},
            {'name': 'Copper', 'hex': '#B87333'}
        ],
        'Deep_cool': [
            {'name': 'Electric Blue', 'hex': '#7DF9FF'},
            {'name': 'Hot Pink', 'hex': '#FF69B4'},
            {'name': 'Violet', 'hex': '#8F00FF'},
            {'name': 'Cyan', 'hex': '#00FFFF'},
            {'name': 'Fuchsia', 'hex': '#FF00FF'}
        ],
        'Deep_neutral': [
            {'name': 'Ruby Red', 'hex': '#E0115F'},
            {'name': 'Sapphire Blue', 'hex': '#0F52BA'},
            {'name': 'Emerald', 'hex': '#50C878'},
            {'name': 'Amethyst', 'hex': '#9966CC'},
            {'name': 'Topaz', 'hex': '#FFC87C'}
        ]
    }
    
    # Get personalized color palette
    palette_key = f"{skin_tone}_{undertone}"
    color_palette = color_palettes.get(palette_key, color_palettes['Medium_neutral'])
    
    # Personalized accessories based on occasion and undertone
    accessories_by_occasion = {
        'wedding': {
            'warm': ['Gold Jhumkas', 'Kundan Necklace', 'Gold Bangles', 'Maang Tikka', 'Embroidered Clutch'],
            'cool': ['Silver Chandbalis', 'Diamond Necklace', 'Silver Bangles', 'Pearl Maang Tikka', 'Sequin Clutch'],
            'neutral': ['Rose Gold Earrings', 'Polki Necklace', 'Mixed Metal Bangles', 'Crystal Maang Tikka', 'Beaded Clutch']
        },
        'party': {
            'warm': ['Gold Hoops', 'Layered Gold Chain', 'Metallic Clutch', 'Gold Watch', 'Amber Ring'],
            'cool': ['Silver Studs', 'Platinum Chain', 'Sequin Bag', 'Silver Watch', 'Sapphire Ring'],
            'neutral': ['Rose Gold Danglers', 'Delicate Necklace', 'Satin Clutch', 'Minimalist Watch', 'Pearl Ring']
        },
        'work': {
            'warm': ['Small Gold Studs', 'Thin Gold Chain', 'Leather Tote', 'Classic Watch', 'Simple Ring'],
            'cool': ['Silver Studs', 'Silver Pendant', 'Black Tote', 'Steel Watch', 'Minimal Ring'],
            'neutral': ['Pearl Studs', 'Delicate Chain', 'Beige Tote', 'Leather Watch', 'Stackable Rings']
        },
        'gym': {
            'warm': ['Sports Watch', 'Gym Bag', 'Sweatband', 'Fitness Tracker', 'Water Bottle'],
            'cool': ['Fitness Watch', 'Duffle Bag', 'Headband', 'Activity Tracker', 'Insulated Bottle'],
            'neutral': ['Smart Watch', 'Backpack', 'Hair Ties', 'Step Counter', 'Shaker Bottle']
        },
        'beach': {
            'warm': ['Gold Anklet', 'Straw Hat', 'Woven Beach Bag', 'Tortoise Sunglasses', 'Shell Bracelet'],
            'cool': ['Silver Anklet', 'White Sun Hat', 'Canvas Tote', 'Blue Sunglasses', 'Turquoise Bracelet'],
            'neutral': ['Beaded Anklet', 'Floppy Hat', 'Mesh Beach Bag', 'Mirrored Sunglasses', 'Leather Bracelet']
        },
        'date': {
            'warm': ['Dainty Gold Necklace', 'Small Hoops', 'Crossbody Bag', 'Delicate Bracelet', 'Nude Heels'],
            'cool': ['Silver Pendant', 'Pearl Studs', 'Mini Bag', 'Silver Bracelet', 'Strappy Heels'],
            'neutral': ['Layered Necklace', 'Drop Earrings', 'Clutch Bag', 'Charm Bracelet', 'Block Heels']
        },
        'festival': {
            'warm': ['Oxidized Jhumkas', 'Coin Necklace', 'Potli Bag', 'Colorful Bangles', 'Embroidered Juttis'],
            'cool': ['Silver Chandbalis', 'Temple Jewelry', 'Mirror Work Bag', 'Silver Bangles', 'Mojaris'],
            'neutral': ['Tribal Earrings', 'Beaded Necklace', 'Ethnic Clutch', 'Thread Bangles', 'Kolhapuri Chappals']
        }
    }
    
    # Personalized hairstyles based on occasion and face shape (inferred from skin tone)
    hairstyles_by_occasion = {
        'wedding': {
            'Fair': ['Elegant Low Bun with Flowers', 'Side-swept Curls with Maang Tikka'],
            'Medium': ['Braided Crown with Gajra', 'Soft Waves with Hair Accessories'],
            'Olive': ['Sleek High Bun with Jewelry', 'Half-up Half-down with Curls'],
            'Deep': ['Voluminous Curls with Side Part', 'Twisted Updo with Statement Pins']
        },
        'party': {
            'Fair': ['Beachy Waves', 'High Ponytail with Volume'],
            'Medium': ['Sleek Straight Hair', 'Messy Bun with Face-framing Layers'],
            'Olive': ['Bouncy Curls', 'Side-swept Waves'],
            'Deep': ['Defined Curls', 'Slicked Back Bun']
        },
        'work': {
            'Fair': ['Low Ponytail', 'Simple Straight Blowout'],
            'Medium': ['Professional Low Bun', 'Neat Middle Part'],
            'Olive': ['Sleek Ponytail', 'Tucked Behind Ears'],
            'Deep': ['Polished Bun', 'Natural Texture with Headband']
        },
        'gym': {
            'Fair': ['High Ponytail', 'Dutch Braids'],
            'Medium': ['Top Knot', 'Braided Ponytail'],
            'Olive': ['Sleek Bun', 'Double French Braids'],
            'Deep': ['Puff with Ponytail', 'Cornrows']
        },
        'beach': {
            'Fair': ['Loose Beach Waves', 'Messy Braid'],
            'Medium': ['Natural Texture', 'Low Pigtails'],
            'Olive': ['Wet Look Slick Back', 'Fishtail Braid'],
            'Deep': ['Protective Style with Scarf', 'Box Braids']
        },
        'date': {
            'Fair': ['Soft Romantic Curls', 'Half-up with Loose Waves'],
            'Medium': ['Voluminous Blowout', 'Low Side Braid'],
            'Olive': ['Sleek and Straight', 'Textured Ponytail'],
            'Deep': ['Defined Curls with Side Part', 'Elegant Low Ponytail']
        }
    }
    
    # Get personalized accessories and hairstyles
    accessories = accessories_by_occasion.get(occasion, {}).get(undertone, 
        ['Statement Earrings', 'Crossbody Bag', 'Sunglasses', 'Watch', 'Scarf'])
    
    hairstyles = hairstyles_by_occasion.get(occasion, {}).get(skin_tone,
        ['Soft Waves', 'Low Bun'])
    
    # Occasion-specific recommendations
    occasion_outfits = {
        'wedding': [
            {'name': 'Traditional Elegance', 'items': ['Silk Saree', 'Blouse', 'Jewelry Set'], 'colors': ['#D4AF37', '#8B0000', '#FFD700']},
            {'name': 'Indo-Western Fusion', 'items': ['Lehenga', 'Crop Top', 'Dupatta'], 'colors': ['#FF1493', '#FFD700', '#FFF']},
        ],
        'party': [
            {'name': 'Glamorous Night', 'items': ['Sequin Dress', 'Heels', 'Clutch'], 'colors': ['#000000', '#FFD700', '#C0C0C0']},
            {'name': 'Chic Party Look', 'items': ['Jumpsuit', 'Statement Earrings', 'Heels'], 'colors': ['#8B008B', '#FF69B4', '#000']},
        ],
        'work': [
            {'name': 'Professional Chic', 'items': ['Blazer', 'Trousers', 'Pumps'], 'colors': ['#2C3E50', '#FFFFFF', '#000000']},
            {'name': 'Smart Casual', 'items': ['Shirt', 'Pencil Skirt', 'Loafers'], 'colors': ['#4A90E2', '#2C3E50', '#8B4513']},
        ],
        'gym': [
            {'name': 'Workout Ready', 'items': ['Sports Bra', 'Leggings', 'Sneakers'], 'colors': ['#FF6B6B', '#000000', '#FFFFFF']},
            {'name': 'Active Wear', 'items': ['Tank Top', 'Shorts', 'Running Shoes'], 'colors': ['#4ECDC4', '#2C3E50', '#95E1D3']},
        ],
        'beach': [
            {'name': 'Beach Vibes', 'items': ['Swimsuit', 'Cover-up', 'Sandals'], 'colors': ['#FF6B9D', '#FFFFFF', '#FFD93D']},
            {'name': 'Tropical Style', 'items': ['Bikini', 'Sarong', 'Sun Hat'], 'colors': ['#06D6A0', '#FFE66D', '#FFFFFF']},
        ],
    }
    
    outfits = occasion_outfits.get(occasion, [
        {'name': 'Casual Look', 'items': ['Floral Top', 'Denim Jeans', 'White Sneakers'], 'colors': ['#FF6B6B', '#4D96FF', '#FFFFFF']},
        {'name': 'Everyday Chic', 'items': ['T-shirt', 'Palazzo', 'Flats'], 'colors': ['#FFD93D', '#2C3E50', '#8B4513']},
    ])
    
    # Get shopping products for each platform separately
    amazon_products = shopping_api.search_products(
        query='fashion',
        occasion=occasion,
        budget=budget,
        limit=4,
        platform='amazon'
    )
    
    flipkart_products = shopping_api.search_products(
        query='fashion',
        occasion=occasion,
        budget=budget,
        limit=4,
        platform='flipkart'
    )
    
    myntra_products = shopping_api.search_products(
        query='fashion',
        occasion=occasion,
        budget=budget,
        limit=4,
        platform='myntra'
    )
    
    return jsonify({
        'success': True,
        'color_palette': color_palette,
        'outfits': outfits,
        'accessories': accessories,
        'hairstyle': hairstyles,
        'shopping': {
            'amazon': amazon_products,
            'flipkart': flipkart_products,
            'myntra': myntra_products
        },
        'explanation': f'These {", ".join([c["name"] for c in color_palette[:3]])} colors are specially chosen for your {skin_tone.lower()} skin tone with {undertone} undertones. Perfect for {occasion} occasions with a {vibe} vibe!'
    })

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    print("Feedback endpoint called")
    return jsonify({'success': True, 'message': 'Feedback saved'})

@app.route('/wardrobe', methods=['POST'])
def manage_wardrobe():
    print("Wardrobe endpoint called")
    return jsonify({'success': True, 'items': []})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("StyleAI+ Server Running!")
    print("Open your browser at: http://localhost:5000")
    print("="*60 + "\n")
    app.run(debug=True, host='127.0.0.1', port=5000)
