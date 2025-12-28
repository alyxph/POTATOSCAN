
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import preprocess_image, extract_features
from model import predict_potato
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route('/classify', methods=['POST'])
def classify_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    
    # Preprocess Image
    roi, contour, steps = preprocess_image(file)
    
    if roi is None:
        return jsonify({'error': 'Failed to process image'}), 400

    # Extract Features (GLCM + Shape)
    features = extract_features(roi, contour)
    
    if features is None:
        return jsonify({'error': 'Failed to extract features'}), 400
        
    print("Extracted Features:", features) # Debugging output

    # Predict
    label, confidence = predict_potato(features)
    
    # Prepare result
    # We convert features to list for JSON serialization
    feature_list = features.flatten().tolist()
    
    # Map feature names based on utils.py order:
    # [Contrast, Homogeneity, Energy, Correlation, Dissimilarity, Area, Perimeter, Circularity, AspectRatio]
    feature_dict = {
        'Contrast': feature_list[0],
        'Homogeneity': feature_list[1],
        'Energy': feature_list[2],
        'Correlation': feature_list[3],
        'Dissimilarity': feature_list[4],
        'Area': feature_list[5],
        'Perimeter': feature_list[6],
        'Circularity': feature_list[7],
        'AspectRatio': feature_list[8]
    }
    
    return jsonify({
        'class': label,
        'confidence': float(confidence),
        'features': feature_dict,
        'steps': steps
    })

if __name__ == '__main__':
    app.run(debug=True)
