from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import os
from PIL import Image
import io
import base64
import logging

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

logging.basicConfig(level=logging.INFO)

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
        lower1 = np.array([0, 120, 70])
        upper1 = np.array([10, 255, 255])
        lower2 = np.array([170, 120, 70])
        upper2 = np.array([180, 255, 255])
        mask1 = cv2.inRange(hsv, lower1, upper1)
        mask2 = cv2.inRange(hsv, lower2, upper2)
        mask = cv2.bitwise_or(mask1, mask2)
    elif color_name == 'green':
        lower = np.array([35, 100, 100])
        upper = np.array([85, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
    elif color_name == 'blue':
        lower = np.array([100, 150, 0])
        upper = np.array([140, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
    else:
        return img  # Jika tidak cocok, kembalikan gambar asli

    result = cv2.bitwise_and(img, img, mask=mask)
    return result

def adjust_hsv(img, hsv_values):
    hue = hsv_values.get('hue', 0)
    saturation = hsv_values.get('saturation', 0)
    value = hsv_values.get('value', 0)

    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(hsv_img)

    h = np.clip(h + hue, 0, 180).astype(np.uint8)
    s = np.clip(s + saturation, 0, 255).astype(np.uint8)
    v = np.clip(v + value, 0, 255).astype(np.uint8)

    adjusted_hsv = cv2.merge([h, s, v])
    adjusted_img = cv2.cvtColor(adjusted_hsv, cv2.COLOR_HSV2RGB)
    return adjusted_img

def process_image(image_data, operation, hsv_values=None, color_name=None):
    if ',' not in image_data:
        raise ValueError("Invalid image data format. Expected Base64 string with a comma.")

    try:
        image_data = image_data.split(',')[1]
        image = Image.open(io.BytesIO(base64.b64decode(image_data))).convert("RGB")
        img_array = np.array(image)
    except Exception as e:
        raise ValueError(f"Failed to decode image: {e}")

    if operation == 'adjust_hsv' and hsv_values:
        processed = adjust_hsv(img_array, hsv_values)
        result_img = Image.fromarray(processed)
    elif operation == 'rgb_to_grayscale':
        processed = rgb_to_grayscale(img_array)
        result_img = Image.fromarray(processed).convert('RGB')
    elif operation == 'detect_color' and color_name:
        processed = detect_color(img_array, color_name)
        result_img = Image.fromarray(processed)
    else:
        result_img = image  # fallback ke original image

    return img_array, result_img

def image_to_base64(image):
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
def deteksi_warna_page():
    return render_template('deteksi_warna.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data received'}), 400

    image_data = data.get('image')
    if not image_data:
        return jsonify({'error': 'No image data provided'}), 400

    operation = data.get('operation')
    color_name = data.get('color_name')
    hsv_values = data.get('hsv_values')

    try:
        original, processed = process_image(image_data, operation, hsv_values, color_name)
        processed_base64 = image_to_base64(processed)
        return jsonify({'processed_image': processed_base64})
    except Exception as e:
        logging.exception("Error while processing image:")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)  # Ubah ke False saat produksi