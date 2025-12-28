
import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model_terbaik_Random_Forest.pkl')

def load_or_train_model():
    """
    Loads the trained model if it exists.
    If not, trains a simple fallback model using sample data points observed in the notebook.
    This ensures the backend works even without the original .pkl file.
    """
    if os.path.exists(MODEL_PATH):
        print(f"Loading existing model from {MODEL_PATH}")
        try:
            model = joblib.load(MODEL_PATH)
            return model
        except Exception as e:
            print(f"Error loading model: {e}. Retraining fallback model.")
    
    print("Model file not found or invalid. Training fallback model...")
    
    # Synthetic data based on notebook values
    # Features: [Contrast, Homogeneity, Energy, Correlation, Dissimilarity, Area, Perimeter, Circularity, AspectRatio]
    
    # Fresh samples (Based on user input: Low Contrast, High Homogeneity, Smooth)
    X_fresh = [
        [74.09, 0.456, 0.103, 0.958, 3.89, 6769.5, 316.8, 0.847, 1.30],
        [70.00, 0.460, 0.105, 0.960, 3.50, 6800.0, 320.0, 0.850, 1.25],
        [80.00, 0.440, 0.100, 0.950, 4.20, 6600.0, 310.0, 0.840, 1.35],
        [65.00, 0.470, 0.110, 0.965, 3.20, 6900.0, 315.0, 0.860, 1.28]
    ]
    
    # Rotten (Busuk) samples (High Contrast, Low Homogeneity, Rough/Spotted)
    X_rotten = [
        [230.70, 0.29, 0.028, 0.94, 7.64, 4000, 250, 0.6, 1.2],
        [400.00, 0.14, 0.016, 0.90, 11.50, 5100, 310, 0.55, 1.05],
        [350.00, 0.20, 0.020, 0.92, 9.50, 4500, 280, 0.58, 1.15],
        [250.00, 0.25, 0.025, 0.93, 8.00, 4200, 260, 0.62, 1.10]
    ]
    
    X = np.array(X_fresh + X_rotten)
    # 0 = Fresh, 1 = Rotten
    y = np.array(['Fresh'] * 4 + ['Busuk'] * 4)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Save it so we don't retrain every time
    joblib.dump(model, MODEL_PATH)
    print("Fallback model trained and saved.")
    
    return model

# Global model instance
model = load_or_train_model()

def predict_potato(features):
    """
    Predicts class from features.
    """
    prediction = model.predict(features)
    probabilities = model.predict_proba(features)
    
    # Get max probability as confidence
    confidence = np.max(probabilities)
    
    # Ensure result is standard python type for JSON serialization (Fix int64 error)
    label = prediction[0]
    
    # If label is numpy type (like numpy.str_ or numpy.int64), convert it
    if hasattr(label, 'item'):
        label = label.item()
    
    # Just in case it's numeric 0 or 1, map it (optional safety)
    # But usually model.predict returns the class labels we trained with
    
    return label, confidence
