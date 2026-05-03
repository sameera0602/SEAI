import os
import random
import logging
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure Gemini API
GENAI_API_KEY = os.environ.get("GEMINI_API_KEY", "mock_key")
genai.configure(api_key=GENAI_API_KEY)

CLASSES = ['acne', 'carcinoma', 'eczema', 'keratosis', 'millia', 'rosacea']

def mock_predict(image_path):
    """Fallback prediction if real model is not available."""
    # Simulate processing delay
    import time
    time.sleep(1)
    return random.choice(CLASSES)

def get_llm_advice(disease_name):
    """Fetch patient-friendly explanation from Gemini LLM."""
    if GENAI_API_KEY == "mock_key":
        return f"Mock LLM Response: {disease_name} is a common skin condition. Please consult a dermatologist for personalized medical advice. Maintain good hygiene and avoid scratching."

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Act as a professional dermatologist. A patient's skin scan indicated a high probability of '{disease_name}'. Provide a brief, compassionate, and patient-friendly explanation of what this condition is, its common causes, and general lifestyle or treatment advice. Limit the response to 3 short paragraphs. Include a disclaimer that this is AI-generated and they should consult a doctor."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logging.error(f"LLM Error: {e}")
        return "An error occurred while generating advice. Please consult a healthcare professional."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # In a real scenario, we would load model.h5 and run prediction here.
    # We use mock_predict since the weights are missing from the repo.
    predicted_class = mock_predict(filepath)
    
    # Get GenAI insights
    llm_advice = get_llm_advice(predicted_class)

    return jsonify({
        'prediction': predicted_class,
        'advice': llm_advice
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
