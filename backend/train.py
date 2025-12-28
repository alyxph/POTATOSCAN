
import os
import cv2
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import glob

# Import functions from our existing utils
from utils import preprocess_image, extract_features

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, 'dataset')
MODEL_PATH = os.path.join(BASE_DIR, 'model_terbaik_Random_Forest.pkl')

def load_dataset():
    features = []
    labels = []
    
    classes = ['Fresh', 'Busuk']
    
    print("Mulai memproses dataset gambar asli...")
    
    for label in classes:
        path = os.path.join(DATASET_PATH, label)
        if not os.path.isdir(path):
            print(f"Folder tidak ditemukan: {path}. Silakan buat folder dan isi dengan gambar.")
            continue
            
        print(f"Memproses kelas: {label}")
        # Support common image formats
        images = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
            images.extend(glob.glob(os.path.join(path, ext)))
            
        if not images:
            print(f"  Tidak ada gambar di {path}")
            continue
            
        count = 0
        for img_path in images:
            try:
                # 1. Preprocess (Input is file path string)
                roi, _ = preprocess_image(img_path)
                
                if roi is None:
                    continue
                    
                # 2. Extract Features
                feat = extract_features(roi)
                
                if feat is not None:
                    features.append(feat[0]) # Flatten
                    labels.append(label)
                    count += 1
                    
            except Exception as e:
                print(f"  Gagal memproses {img_path}: {e}")
        
        print(f"  Berhasil memproses {count} gambar untuk {label}")

    return np.array(features), np.array(labels)

def train_model():
    X, y = load_dataset()
    
    if len(X) == 0:
        print("Error: Tidak ada data untuk dilatih. Pastikan Anda sudah memasukkan foto kentang ke folder 'dataset/Fresh' dan 'dataset/Busuk'.")
        return

    print(f"\nTotal Data: {len(X)}")
    print("Membagi data training (80%) dan testing (20%)...")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Melatih Random Forest...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    print("Evaluasi Model:")
    y_pred = model.predict(X_test)
    print(f"Akurasi: {accuracy_score(y_test, y_pred) * 100:.2f}%")
    print("\nLaporan Klasifikasi:")
    print(classification_report(y_test, y_pred))
    
    # Save the model
    joblib.dump(model, MODEL_PATH)
    print(f"\nModel berhasil disimpan ke: {MODEL_PATH}")
    print("Sekarang aplikasi backend akan menggunakan otak dari gambar asli Anda!")

if __name__ == "__main__":
    train_model()
