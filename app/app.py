from flask import Flask, render_template, request, jsonify, redirect, url_for
import cv2
import numpy as np
import os
from PIL import Image
import base64
import io
from sklearn.cluster import KMeans
from collections import Counter

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def rgb_to_hsv(img):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    return hsv_img

def rgb_to_grayscale(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return gray_img

def detect_dominant_colors_improved(img, num_colors=5):
    """
    Deteksi warna dominan menggunakan metode quantisasi warna yang lebih akurat
    """
    # Resize image untuk mempercepat proses
    h, w = img.shape[:2]
    if max(h, w) > 600:  # Resize hanya jika lebih besar dari 600px
        scale = 600 / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)))
    
    # Konversi ke format yang diterima oleh PIL
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Pastikan gambar dalam RGB
    pil_img = Image.fromarray(img_rgb)
    
    try:
        # Quantisasi warna menggunakan metode PIL
        pil_img = pil_img.quantize(colors=num_colors, method=2)  # method=2 adalah median cut
        
        # Dapatkan palette warna
        palette = pil_img.getpalette()
        color_counts = Counter(pil_img.getdata())
        total_pixels = pil_img.width * pil_img.height
        
        # Format hasil
        color_info = []
        for color_idx, count in color_counts.most_common(num_colors):
            r = palette[color_idx*3]
            g = palette[color_idx*3+1]
            b = palette[color_idx*3+2]
            
            percentage = count / total_pixels * 100
            hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
            
            color_info.append({
                'rgb': [r, g, b],
                'hex': hex_color,
                'percentage': round(percentage, 2)
            })
    except Exception as e:
        print(f"Error in PIL quantize: {e}")
        return detect_dominant_colors_kmeans(img, num_colors)
    
    return color_info

def detect_dominant_colors_kmeans(img, num_colors=5):
    """
    Deteksi warna dominan menggunakan K-means dengan perbaikan
    """
    # Resize image untuk mempercepat proses
    h, w = img.shape[:2]
    if w > 600:  # Resize hanya jika lebih besar dari 600px
        ratio = 600 / w
        img = cv2.resize(img, (600, int(h * ratio)))
    
    # Pastikan gambar dalam format RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Konversi ke ruang warna LAB yang lebih perceptual
    lab_image = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    
    # Reshape image untuk analisis
    pixels = lab_image.reshape(-1, 3)
    
    # Gunakan K-means dengan inisialisasi yang lebih baik
    kmeans = KMeans(n_clusters=num_colors, n_init=10, init='k-means++')
    kmeans.fit(pixels)
    
    # Dapatkan pusat cluster
    centers = kmeans.cluster_centers_
    
    # Konversi pusat cluster kembali ke RGB
    centers_rgb = []
    for center in centers:
        # Pastikan kita membulatkan nilai center
        lab_color = np.uint8(np.round([[center]]))  # Pembulatan center sebelum konversi
        rgb_color = cv2.cvtColor(lab_color, cv2.COLOR_LAB2RGB)[0][0]
        centers_rgb.append(rgb_color)
    
    # Hitung persentase tiap warna
    labels = kmeans.labels_
    count = Counter(labels)
    
    total_pixels = len(labels)
    color_info = []
    
    for i, rgb in enumerate(centers_rgb):
        # Konversi ke int
        color = [int(c) for c in rgb]
        count_percent = count[i] / total_pixels * 100
        
        # Format ke RGB dan hex
        hex_color = '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])
        
        color_info.append({
            'rgb': color,
            'hex': hex_color,
            'percentage': round(count_percent, 2)
        })
    
    # Urutkan berdasarkan persentase
    color_info = sorted(color_info, key=lambda x: x['percentage'], reverse=True)
    
    return color_info

def is_grayscale_image(img):
    """
    Deteksi apakah gambar adalah grayscale/hitam-putih
    """
    # Hitung perbedaan antar channel warna
    diff_r_g = np.abs(img[:,:,0] - img[:,:,1])
    diff_r_b = np.abs(img[:,:,0] - img[:,:,2])
    diff_g_b = np.abs(img[:,:,1] - img[:,:,2])
    
    # Jika perbedaan minimal, gambar kemungkinan grayscale
    threshold = 15  # Toleransi untuk kompresi artifak
    is_gray = (
        np.mean(diff_r_g) < threshold and 
        np.mean(diff_r_b) < threshold and 
        np.mean(diff_g_b) < threshold
    )
    
    return is_gray

def detect_dominant_colors(img, num_colors=5):
    """
    Fungsi utama untuk deteksi warna dominan dengan
    penanganan khusus untuk gambar hitam-putih
    """
    # Cek apakah gambar grayscale/hitam-putih
    if is_grayscale_image(img):
        # Konversi ke grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        
        # Gunakan histogram untuk mendapatkan distribusi warna grayscale
        hist = cv2.calcHist([gray], [0], None, [num_colors], [0, 256])
        
        # Dapatkan rentang nilai per bin
        bin_width = 256 // num_colors
        
        color_info = []
        total_pixels = gray.size
        
        for i in range(num_colors):
            bin_count = hist[i][0]
            if bin_count > 0:
                # Nilai tengah bin sebagai warna representatif
                gray_val = int(i * bin_width + bin_width/2)
                percentage = (bin_count / total_pixels) * 100
                
                color_info.append({
                    'rgb': [gray_val, gray_val, gray_val],
                    'hex': '#{:02x}{:02x}{:02x}'.format(gray_val, gray_val, gray_val),
                    'percentage': round(percentage, 2)
                })
        
        # Urutkan berdasarkan persentase
        return sorted(color_info, key=lambda x: x['percentage'], reverse=True)
    
    # Untuk gambar berwarna, gunakan metode quantisasi yang lebih baik
    return detect_dominant_colors_improved(img, num_colors)

def process_image(image_data, operation):
    image_data = image_data.split(',')[1]
    image = Image.open(io.BytesIO(base64.b64decode(image_data)))
    img_array = np.array(image)
    
    if operation == 'rgb_to_hsv':
        processed = rgb_to_hsv(img_array)
        result_img = Image.fromarray(processed.astype('uint8'))
    elif operation == 'rgb_to_grayscale':
        processed = rgb_to_grayscale(img_array)
        result_img = Image.fromarray(processed).convert('RGB')
    elif operation == 'detect_colors':
        # Untuk deteksi warna, tidak perlu mengubah gambar
        dominant_colors = detect_dominant_colors(img_array)
        return img_array, image, dominant_colors
    else:
        result_img = image
    
    return img_array, result_img

def image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_str}"

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
def deteksi_warna():
    return render_template('deteksi_warna.html')

@app.route('/process', methods=['POST'])
def process():
    image_data = request.json['image']
    operation = request.json['operation']
    
    original, processed = process_image(image_data, operation)
    processed_base64 = image_to_base64(processed)
    
    response = {
        'processed_image': processed_base64,
    }
    
    return jsonify(response)

@app.route('/detect_colors', methods=['POST'])
def detect_colors():
    image_data = request.json['image']
    num_colors = request.json.get('num_colors', 5)  # Default 5 warna
    
    _, original_img, dominant_colors = process_image(image_data, 'detect_colors')
    processed_base64 = image_to_base64(original_img)
    
    response = {
        'processed_image': processed_base64,
        'dominant_colors': dominant_colors
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
