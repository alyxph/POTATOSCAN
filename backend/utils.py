
import cv2
import numpy as np
import base64
from skimage.feature import graycomatrix, graycoprops

def to_base64(image):
    """Encodes a numpy image to base64 string"""
    _, buffer = cv2.imencode('.png', image)
    return base64.b64encode(buffer).decode('utf-8')

def extract_roi(gray_image, contour):
    """
    Extracts the Region of Interest (ROI) from a grayscale image based on a contour.
    
    Parameters:
    - gray_image: Gambar grayscale
    - contour: Contour yang sudah terdeteksi
    """
    # Ambil koordinat kotak (Bounding Box) dari contour
    x, y, w, h = cv2.boundingRect(contour)

    # POTONG GAMBAR (ROI Extraction)
    roi = gray_image[y:y+h, x:x+w]

    return roi, (x, y, w, h)

def preprocess_image(image_file, target_size=(128, 128)):
    """
    Reads an image, processes it, and returns both the ROI (for analysis)
    and a dictionary of base64 images for visualization.
    """
    steps = {}
    try:
        # 1. Read Image
        if hasattr(image_file, 'read'):
            image_file.seek(0)
            file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        elif isinstance(image_file, str):
            image = cv2.imread(image_file)
        else:
            image = image_file

        if image is None:
            raise ValueError("Could not read image")
            
        # steps['original'] = to_base64(image) 

        # 2. Resize
        resized_image = cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)
        steps['resized'] = to_base64(resized_image)
        
        # 3. Grayscale
        gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
        steps['grayscale'] = to_base64(gray_image)
        
        # 4. Blur
        blurred = cv2.GaussianBlur(gray_image, (15, 15), 0)
        steps['blur'] = to_base64(blurred)

      # 5. Threshold (Adaptive)
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        if thresh[0, 0] == 255:
            thresh = cv2.bitwise_not(thresh)
        
        # 6. Contours Detection
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Visualization Canvas
        contour_viz = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR) 
        
        roi = None
        main_cnt = None
        
        if contours:
            # --- LOGIKA 1: GAMBAR KONTUR (Hijau & Merah) ---
            # 1. Draw all contours in Green (0, 255, 0)
            cv2.drawContours(contour_viz, contours, -1, (0, 255, 0), 1)
            
            # 2. Get Largest Contour (Main Object)
            main_cnt = max(contours, key=cv2.contourArea)
            
            # 3. Draw Main Contour in Red (0, 0, 255)
            cv2.drawContours(contour_viz, [main_cnt], -1, (0, 0, 255), 2)
            
            # --- LOGIKA 2: EKSTRAK ROI (Terpisah) ---
             # Apply Masking (Background removal)
            mask = np.zeros_like(gray_image)
            cv2.drawContours(mask, [main_cnt], -1, 255, -1)
            masked_img = cv2.bitwise_and(gray_image, gray_image, mask=mask)
            
            roi, bbox = extract_roi(masked_img, main_cnt)
            
            # --- LOGIKA 3: GAMBAR BOUNDING BOX (Biru) ---
            # Menggunakan hasil dari fungsi extract_roi untuk visualisasi
            x, y, w, h = bbox
            cv2.rectangle(contour_viz, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
        else:
            roi = gray_image

        steps['contours'] = to_base64(contour_viz)
        steps['roi'] = to_base64(roi)
        
        # Return ROI, Contour (for shape features), and Visualization Steps
        return roi, main_cnt, steps

    except Exception as e:
        print(f"Error in preprocessing: {e}")
        return None, None, None

def extract_shape_features(contour):
    """
    Extracts geometric shape features from the contour.
    Returns: [Area, Perimeter, Circularity, Aspect Ratio]
    """
    if contour is None:
        return [0, 0, 0, 0]

    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)

    if perimeter > 0:
        circularity = (4 * np.pi * area) / (perimeter ** 2)
    else:
        circularity = 0

    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = float(w) / h if h > 0 else 0

    return [area, perimeter, circularity, aspect_ratio]

def extract_features(roi, contour):
    """
    Extracts BOTH Texture (GLCM) and Shape features.
    Total 9 Features: [Contrast, Homogeneity, Energy, Correlation, Dissimilarity, Area, Perimeter, Circularity, AspectRatio]
    """
    if roi is None:
        return None
        
    try:
        # 1. GLCM Features (5)
        # Normalize ROI to 256 levels if needed
        if roi.dtype != np.uint8:
            roi = (roi * 255).astype(np.uint8)

        img_normalized = ((roi / roi.max()) * 255).astype(np.uint8) if roi.max() > 0 else roi

        # Use 4 angles as per training script
        glcm = graycomatrix(img_normalized, distances=[1], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4], levels=256,
                            symmetric=True, normed=True)
                            
        contrast = graycoprops(glcm, 'contrast').mean()
        dissimilarity = graycoprops(glcm, 'dissimilarity').mean()
        homogeneity = graycoprops(glcm, 'homogeneity').mean()
        energy = graycoprops(glcm, 'energy').mean()
        correlation = graycoprops(glcm, 'correlation').mean()
        
        glcm_features = [contrast, homogeneity, energy, correlation, dissimilarity]
        
        # 2. Shape Features (4)
        shape_features = extract_shape_features(contour)
    
        
        glcm_features_corrected = [contrast, homogeneity, energy, correlation, dissimilarity]
        
        final_features = glcm_features_corrected + shape_features
        
        return np.array(final_features).reshape(1, -1)

    except Exception as e:
        print(f"Error in feature extraction: {e}")
        return None
