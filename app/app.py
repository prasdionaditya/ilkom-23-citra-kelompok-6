from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import os
from PIL import Image
import io
import base64
from sklearn.cluster import KMeans  # Tambahkan import ini

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Konversi RGB ke HSV
def rgb_to_hsv(img):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    return hsv_img

# Konversi RGB ke Grayscale
def rgb_to_grayscale(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return gray_img

# Deteksi warna (merah, hijau, biru)
def detect_color(img, color_name):
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    if color_name == 'red':
        # Untuk mendeteksi merah, butuh dua rentang karena berada di ujung spektrum HSV
        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = mask1 | mask2
    elif color_name == 'green':
        lower = np.array([35, 100, 100])
        upper = np.array([85, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
    elif color_name == 'blue':
        lower = np.array([100, 150, 0])
        upper = np.array([140, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
    else:
        return img

    result = cv2.bitwise_and(img, img, mask=mask)
    return result

# TAMBAHKAN FUNGSI BARU INI - Deteksi warna dominan
def detect_dominant_colors(img, n_colors=5):
    # Reshape image untuk analisis clustering
    pixels = img.reshape(-1, 3)
    
    # Gunakan KMeans untuk menemukan warna dominan
    kmeans = KMeans(n_clusters=n_colors, random_state=42)
    kmeans.fit(pixels)
    
    # Ambil warna dari centroid
    colors = kmeans.cluster_centers_
    
    # Hitung persentase setiap warna
    labels = kmeans.labels_
    count_labels = np.bincount(labels)
    percentage = count_labels / len(labels) * 100
    
    # Buat hasil dengan hex code dan persentase
    result = []
    for i, color in enumerate(colors):
        # Konversi ke RGB 0-255
        rgb = np.round(color).astype(int)
        # Konversi ke hex
        hex_code = '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
        
        result.append({
            'rgb': rgb.tolist(),
            'hex': hex_code,
            'percentage': percentage[i]
        })
    
    # Urutkan berdasarkan persentase (dari yang terbesar)
    result = sorted(result, key=lambda x: x['percentage'], reverse=True)
    
    return result

# Proses gambar
def process_image(image_data, operation, color_name=None):
    try:
        image_data = image_data.split(',')[1]
        image = Image.open(io.BytesIO(base64.b64decode(image_data))).convert("RGB")
        img_array = np.array(image)

        if operation == 'rgb_to_hsv':
            processed = rgb_to_hsv(img_array)
            result_img = Image.fromarray(cv2.cvtColor(processed, cv2.COLOR_RGB2HSV))
        elif operation == 'rgb_to_grayscale':
            processed = rgb_to_grayscale(img_array)
            result_img = Image.fromarray(processed).convert('RGB')
        elif operation == 'detect_color' and color_name:
            processed = detect_color(img_array, color_name)
            result_img = Image.fromarray(processed)
        else:
            result_img = image

        return img_array, result_img
    except Exception as e:
        print(f"Error in processing image: {e}")
        return None, None

# Ubah ke base64
def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_str}"

# Route tampilan
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hsv')
def hsv():
    return render_template('hsv.html')

@app.route('/grayscale')
def grayscale():
    return render_template('grayscale.html')

@app.route('/deteksi_warna')
def deteksi_warna_page():
    return render_template('deteksi_warna.html')

# Route proses gambar
@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.get_json()
        image_data = data['image']
        operation = data['operation']
        color_name = data.get('color_name', None)

        print(f"Operasi: {operation}, Warna: {color_name}")

        original, processed = process_image(image_data, operation, color_name)

        if processed is None:
            return jsonify({'error': 'Gagal memproses gambar'}), 500

        processed_base64 = image_to_base64(processed)
        return jsonify({'processed_image': processed_base64})
    except Exception as e:
        print(f"Error in /process route: {e}")
        return jsonify({'error': 'Server error'}), 500

# TAMBAHKAN ROUTE BARU INI - Route untuk proses deteksi warna dominan
@app.route('/process_dominant_colors', methods=['POST'])
def process_dominant_colors():
    try:
        data = request.get_json()
        image_data = data['image']
        
        # Proses gambar untuk mendapatkan array numpy
        image_data = image_data.split(',')[1]
        image = Image.open(io.BytesIO(base64.b64decode(image_data))).convert("RGB")
        img_array = np.array(image)
        
        # Deteksi warna dominan
        dominant_colors = detect_dominant_colors(img_array)
        
        return jsonify({
            'dominant_colors': dominant_colors
        })
    except Exception as e:
        print(f"Error in /process_dominant_colors route: {e}")
        return jsonify({'error': 'Gagal memproses gambar'}), 500

# Jalankan app
if __name__ == '__main__':
    app.run(debug=True)
