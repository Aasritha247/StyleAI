// StyleAI+ Frontend Application

let uploadedFilePath = null;
let analysisResult = null;
let currentLanguage = 'en';
let currentTheme = 'pink';
let currentGender = 'female';
let cameraStream = null;

// Translations
const translations = {
    en: {
        upload_title: "Upload Your Photo",
        upload_desc: "Let's discover your perfect style!",
        drag_drop: "Drag & drop your photo here",
        browse: "📁 Browse Files",
        camera: "📸 Use Camera",
        change_photo: "Change Photo",
        tell_us: "Tell us more about you",
        vibe: "What's your vibe?",
        occasion: "Occasion",
        budget: "Budget Range",
        analyze: "Analyze My Style ✨",
        analyzing: "Analyzing your beauty...",
        wait: "Creating your personalized style guide",
        your_palette: "Your Perfect Palette",
        colors: "Colors Made for You",
        outfits: "Outfit Inspirations",
        accessories: "Complete the Look",
        hairstyles: "Hairstyle Suggestions",
        why: "Why This Works for You",
        shop: "Shop Your Style",
        feedback_title: "Love these recommendations?",
        try_again: "Try Another Look"
    },
    hi: {
        upload_title: "अपनी फोटो अपलोड करें",
        upload_desc: "आइए आपकी परफेक्ट स्टाइल खोजें!",
        drag_drop: "यहाँ अपनी फोटो ड्रैग करें",
        browse: "📁 फाइल चुनें",
        camera: "📸 कैमरा उपयोग करें",
        change_photo: "फोटो बदलें",
        tell_us: "हमें अपने बारे में बताएं",
        vibe: "आपकी पसंद क्या है?",
        occasion: "अवसर",
        budget: "बजट रेंज",
        analyze: "मेरी स्टाइल का विश्लेषण करें ✨",
        analyzing: "आपकी सुंदरता का विश्लेषण...",
        wait: "आपकी व्यक्तिगत स्टाइल गाइड बना रहे हैं",
        your_palette: "आपका परफेक्ट पैलेट",
        colors: "आपके लिए रंग",
        outfits: "आउटफिट प्रेरणा",
        accessories: "लुक पूरा करें",
        hairstyles: "हेयरस्टाइल सुझाव",
        why: "यह आपके लिए क्यों काम करता है",
        shop: "अपनी स्टाइल खरीदें",
        feedback_title: "ये सिफारिशें पसंद हैं?",
        try_again: "एक और लुक आज़माएं"
    },
    te: {
        upload_title: "మీ ఫోటో అప్‌లోడ్ చేయండి",
        upload_desc: "మీ పర్ఫెక్ట్ స్టైల్ కనుగొందాం!",
        drag_drop: "మీ ఫోటోను ఇక్కడ డ్రాగ్ చేయండి",
        browse: "📁 ఫైల్స్ బ్రౌజ్ చేయండి",
        camera: "📸 కెమెరా ఉపయోగించండి",
        change_photo: "ఫోటో మార్చండి",
        tell_us: "మీ గురించి మాకు చెప్పండి",
        vibe: "మీ వైబ్ ఏమిటి?",
        occasion: "సందర్భం",
        budget: "బడ్జెట్ రేంజ్",
        analyze: "నా స్టైల్ విశ్లేషించండి ✨",
        analyzing: "మీ అందాన్ని విశ్లేషిస్తోంది...",
        wait: "మీ వ్యక్తిగత స్టైల్ గైడ్ సృష్టిస్తోంది",
        your_palette: "మీ పర్ఫెక్ట్ పాలెట్",
        colors: "మీ కోసం రంగులు",
        outfits: "దుస్తుల ప్రేరణలు",
        accessories: "లుక్ పూర్తి చేయండి",
        hairstyles: "హెయిర్‌స్టైల్ సూచనలు",
        why: "ఇది మీకు ఎందుకు పనిచేస్తుంది",
        shop: "మీ స్టైల్ షాప్ చేయండి",
        feedback_title: "ఈ సిఫార్సులు ఇష్టమా?",
        try_again: "మరొక లుక్ ప్రయత్నించండి"
    }
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
});

function setupEventListeners() {
    // Gender selector with auto theme
    document.querySelectorAll('.gender-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.gender-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentGender = btn.dataset.gender;
            
            // Update upload emoji based on gender
            const uploadEmoji = document.getElementById('upload-emoji');
            if (currentGender === 'female') {
                uploadEmoji.textContent = '👗';
                setTheme('pink');
            } else if (currentGender === 'male') {
                uploadEmoji.textContent = '👔';
                setTheme('blue');
            } else {
                uploadEmoji.textContent = '✨';
                setTheme('purple');
            }
        });
    });
    
    // Theme selector
    document.querySelectorAll('.theme-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            setTheme(btn.dataset.theme);
        });
    });

    // Language selector
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentLanguage = btn.dataset.lang;
            updateTranslations();
        });
    });

    // File upload
    const fileInput = document.getElementById('file-input');
    const uploadArea = document.getElementById('upload-area');
    const browseBtn = document.getElementById('browse-btn');
    const cameraBtn = document.getElementById('camera-btn');

    browseBtn.addEventListener('click', () => fileInput.click());
    cameraBtn.addEventListener('click', openCamera);

    // Camera controls
    document.querySelector('.close-modal').addEventListener('click', closeCamera);
    document.getElementById('cancel-camera-btn').addEventListener('click', closeCamera);
    document.getElementById('capture-btn').addEventListener('click', capturePhoto);

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--primary)';
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = 'var(--secondary)';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--secondary)';
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            handleFileUpload(file);
        }
    });

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleFileUpload(file);
        }
    });

    // Change photo
    document.getElementById('change-photo').addEventListener('click', () => {
        document.getElementById('preview-container').style.display = 'none';
        document.getElementById('upload-area').style.display = 'block';
        document.getElementById('analyze-btn').disabled = true;
        uploadedFilePath = null;
    });

    // Analyze button
    document.getElementById('analyze-btn').addEventListener('click', analyzeImage);

    // Try again button
    document.getElementById('try-again-btn').addEventListener('click', () => {
        showSection('upload-section');
        document.getElementById('preview-container').style.display = 'none';
        document.getElementById('upload-area').style.display = 'block';
        document.getElementById('analyze-btn').disabled = true;
        uploadedFilePath = null;
    });

    // Feedback buttons
    document.querySelectorAll('.btn-feedback').forEach(btn => {
        btn.addEventListener('click', () => {
            const liked = btn.dataset.feedback === 'true';
            submitFeedback(liked);
        });
    });
}

function updateTranslations() {
    document.querySelectorAll('[data-translate]').forEach(el => {
        const key = el.dataset.translate;
        if (translations[currentLanguage][key]) {
            if (el.tagName === 'INPUT' || el.tagName === 'BUTTON') {
                el.value = translations[currentLanguage][key];
            } else {
                el.textContent = translations[currentLanguage][key];
            }
        }
    });
}

async function handleFileUpload(file) {
    const formData = new FormData();
    formData.append('image', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            uploadedFilePath = result.filepath;
            
            // Show preview
            const reader = new FileReader();
            reader.onload = (e) => {
                document.getElementById('preview-image').src = e.target.result;
                document.getElementById('upload-area').style.display = 'none';
                document.getElementById('preview-container').style.display = 'block';
                document.getElementById('analyze-btn').disabled = false;
            };
            reader.readAsDataURL(file);
        } else {
            alert('Upload failed: ' + result.error);
        }
    } catch (error) {
        alert('Upload error: ' + error.message);
    }
}

async function analyzeImage() {
    showSection('loading-section');

    try {
        // Step 1: Analyze skin tone
        const analyzeResponse = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filepath: uploadedFilePath })
        });

        analysisResult = await analyzeResponse.json();

        if (!analysisResult.success) {
            alert('Analysis failed: ' + analysisResult.error);
            showSection('upload-section');
            return;
        }

        // Step 2: Get recommendations
        const vibe = document.getElementById('vibe-select').value;
        const occasion = document.getElementById('occasion-select').value;
        const budget = document.getElementById('budget-select').value;

        const recommendResponse = await fetch('/recommend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                skin_tone: analysisResult.skin_tone,
                undertone: analysisResult.undertone,
                gender: currentGender,
                vibe: vibe,
                occasion: occasion,
                budget: budget,
                user_id: 'guest'
            })
        });

        const recommendations = await recommendResponse.json();

        if (recommendations.success) {
            displayResults(analysisResult, recommendations);
            showSection('results-section');
        } else {
            alert('Recommendation failed');
            showSection('upload-section');
        }

    } catch (error) {
        alert('Error: ' + error.message);
        showSection('upload-section');
    }
}

function displayResults(analysis, recommendations) {
    // Skin tone result
    document.getElementById('skin-tone-result').textContent = 
        `${analysis.skin_tone} skin with ${analysis.undertone} undertones`;

    // Color palette
    const colorPalette = document.getElementById('color-palette');
    colorPalette.innerHTML = '';
    
    if (recommendations.color_palette) {
        recommendations.color_palette.forEach(color => {
            const colorItem = document.createElement('div');
            colorItem.className = 'color-item';
            colorItem.innerHTML = `
                <div class="color-swatch" style="background-color: ${color.hex || color}"></div>
                <p>${color.name || 'Color'}</p>
            `;
            colorPalette.appendChild(colorItem);
        });
    }

    // Outfits
    const outfitsGrid = document.getElementById('outfits-grid');
    outfitsGrid.innerHTML = '';
    
    if (recommendations.outfits) {
        recommendations.outfits.forEach(outfit => {
            const outfitItem = document.createElement('div');
            outfitItem.className = 'outfit-item';
            
            const itemsList = outfit.items ? outfit.items.map(item => `<li>${item}</li>`).join('') : '';
            const colorSwatches = outfit.colors ? outfit.colors.map(color => 
                `<div class="outfit-color" style="background-color: ${color}"></div>`
            ).join('') : '';
            
            outfitItem.innerHTML = `
                <h4>${outfit.name}</h4>
                <ul class="outfit-items">${itemsList}</ul>
                <div class="outfit-colors">${colorSwatches}</div>
            `;
            outfitsGrid.appendChild(outfitItem);
        });
    }

    // Accessories
    const accessoriesList = document.getElementById('accessories-list');
    accessoriesList.innerHTML = '';
    
    if (recommendations.accessories) {
        recommendations.accessories.forEach(accessory => {
            const item = document.createElement('div');
            item.className = 'accessory-item';
            item.textContent = accessory;
            accessoriesList.appendChild(item);
        });
    }

    // Hairstyles
    const hairstyleList = document.getElementById('hairstyle-list');
    hairstyleList.innerHTML = '';
    
    if (recommendations.hairstyle) {
        recommendations.hairstyle.forEach(style => {
            const item = document.createElement('div');
            item.className = 'hairstyle-item';
            item.textContent = style;
            hairstyleList.appendChild(item);
        });
    }

    // Explanation
    document.getElementById('explanation-text').textContent = 
        recommendations.explanation || 'These recommendations are personalized for you!';

    // Shopping (real products by platform)
    if (recommendations.shopping) {
        displayShoppingByPlatform(recommendations.shopping);
    } else {
        displayShoppingByPlatform();
    }
}

function displayShoppingByPlatform(shopping) {
    // Display Amazon products
    const amazonGrid = document.getElementById('amazon-grid');
    amazonGrid.innerHTML = '';
    const amazonProducts = shopping?.amazon || [];
    
    if (amazonProducts.length > 0) {
        amazonProducts.forEach(item => {
            amazonGrid.appendChild(createProductCard(item));
        });
    } else {
        amazonGrid.innerHTML = '<p>Loading products...</p>';
    }
    
    // Display Flipkart products
    const flipkartGrid = document.getElementById('flipkart-grid');
    flipkartGrid.innerHTML = '';
    const flipkartProducts = shopping?.flipkart || [];
    
    if (flipkartProducts.length > 0) {
        flipkartProducts.forEach(item => {
            flipkartGrid.appendChild(createProductCard(item));
        });
    } else {
        flipkartGrid.innerHTML = '<p>Loading products...</p>';
    }
    
    // Display Myntra products
    const myntraGrid = document.getElementById('myntra-grid');
    myntraGrid.innerHTML = '';
    const myntraProducts = shopping?.myntra || [];
    
    if (myntraProducts.length > 0) {
        myntraProducts.forEach(item => {
            myntraGrid.appendChild(createProductCard(item));
        });
    } else {
        myntraGrid.innerHTML = '<p>Loading products...</p>';
    }
}

function createProductCard(item) {
    const shopItem = document.createElement('div');
    shopItem.className = 'shop-item';
    
    // Ensure URL is properly formatted
    let productUrl = item.url || '#';
    
    // If URL doesn't start with http, add the base URL
    if (!productUrl.startsWith('http')) {
        if (item.platform === 'Amazon') {
            productUrl = `https://www.amazon.in/s?k=${encodeURIComponent(item.name)}`;
        } else if (item.platform === 'Flipkart') {
            productUrl = `https://www.flipkart.com/search?q=${encodeURIComponent(item.name)}`;
        } else if (item.platform === 'Myntra') {
            productUrl = `https://www.myntra.com/${encodeURIComponent(item.name.toLowerCase().replace(/\s+/g, '-'))}`;
        }
    }
    
    shopItem.innerHTML = `
        <h4>${item.name}</h4>
        <div class="price">₹${item.price.toLocaleString()}</div>
        ${item.rating ? `<div class="rating">⭐ ${item.rating} (${item.reviews} reviews)</div>` : ''}
        <a href="${productUrl}" target="_blank" rel="noopener noreferrer" class="shop-btn ${item.platform.toLowerCase()}">
            Shop on ${item.platform}
        </a>
    `;
    return shopItem;
}

async function submitFeedback(liked) {
    try {
        await fetch('/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: 'guest',
                recommendation_id: 1,
                liked: liked
            })
        });

        alert(liked ? '💖 Thank you! We\'re glad you loved it!' : '🤔 Thanks for feedback! We\'ll improve.');
    } catch (error) {
        console.error('Feedback error:', error);
    }
}

function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(sectionId).classList.add('active');
}

// Theme setter function
function setTheme(theme) {
    currentTheme = theme;
    document.body.setAttribute('data-theme', theme);
    
    // Update active theme button
    document.querySelectorAll('.theme-btn').forEach(b => b.classList.remove('active'));
    document.querySelector(`[data-theme="${theme}"]`).classList.add('active');
}

// Camera functions
async function openCamera() {
    const modal = document.getElementById('camera-modal');
    const video = document.getElementById('camera-video');
    
    try {
        cameraStream = await navigator.mediaDevices.getUserMedia({ 
            video: { facingMode: 'user' },
            audio: false 
        });
        video.srcObject = cameraStream;
        modal.classList.add('active');
    } catch (error) {
        alert('Camera access denied or not available: ' + error.message);
    }
}

function closeCamera() {
    const modal = document.getElementById('camera-modal');
    const video = document.getElementById('camera-video');
    
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
    }
    
    video.srcObject = null;
    modal.classList.remove('active');
}

function capturePhoto() {
    const video = document.getElementById('camera-video');
    const canvas = document.getElementById('camera-canvas');
    const context = canvas.getContext('2d');
    
    // Set canvas size to video size
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Draw video frame to canvas
    context.drawImage(video, 0, 0);
    
    // Convert to blob and upload
    canvas.toBlob(async (blob) => {
        const file = new File([blob], 'camera-photo.jpg', { type: 'image/jpeg' });
        await handleFileUpload(file);
        closeCamera();
    }, 'image/jpeg', 0.95);
}
