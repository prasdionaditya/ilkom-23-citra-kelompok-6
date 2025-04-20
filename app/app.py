from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import os
from PIL import Image
import io
import base64

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
        lower = np.array([0, 120, 70])
        upper = np.array([10, 255, 255])
    elif color_name == 'green':
        lower = np.array([35, 100, 100])
        upper = np.array([85, 255, 255])
    elif color_name == 'blue':
        lower = np.array([100, 150, 0])
        upper = np.array([140, 255, 255])
    else:
        return img  # jika tidak ada warna yang cocok, kembalikan gambar asli

    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)
    return result

# Proses gambar sesuai operasi
def process_image(image_data, operation, color_name=None):
    image_data = image_data.split(',')[1]
    image = Image.open(io.BytesIO(base64.b64decode(image_data)))
    img_array = np.array(image)

    if operation == 'rgb_to_hsv':
        processed = rgb_to_hsv(img_array)
        result_img = Image.fromarray(processed.astype('uint8'))
    elif operation == 'rgb_to_grayscale':
        processed = rgb_to_grayscale(img_array)
        result_img = Image.fromarray(processed).convert('RGB')
    elif operation == 'detect_color' and color_name:
        processed = detect_color(img_array, color_name)
        result_img = Image.fromarray(processed)
    else:
        result_img = image

    return img_array, result_img

# Konversi gambar ke base64
def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_str}"

# Route utama
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

# Route untuk memproses gambar
@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    image_data = data['image']
    operation = data['operation']
    color_name = data.get('color_name', None)

    original, processed = process_image(image_data, operation, color_name)
    processed_base64 = image_to_base64(processed)

    return jsonify({'processed_image': processed_base64})

if __name__ == '__main__':
    app.run(debug=True)
