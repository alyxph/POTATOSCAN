
import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = 'model_terbaik_Random_Forest.pkl'

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
    # Features: [Contrast, Dissimilarity, Homogeneity, Energy, Correlation]
    
    # Fresh samples (High contrast, low homogeneity)
    X_fresh = [
        [407.36, 12.05, 0.13, 0.015, 0.91],
        [400.00, 11.50, 0.14, 0.016, 0.90],
        [415.00, 12.50, 0.12, 0.014, 0.92]
    ]
    
    # Rotten (Busuk) samples (Lower contrast, higher homogeneity)
    X_rotten = [
        [230.70, 7.64, 0.29, 0.028, 0.94],
        [240.00, 8.00, 0.28, 0.027, 0.93],
        [220.00, 7.20, 0.30, 0.029, 0.95]
    ]
    
    X = np.array(X_fresh + X_rotten)
    # 0 = Fresh, 1 = Rotten
    y = np.array(['Fresh'] * 3 + ['Busuk'] * 3)
    
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
