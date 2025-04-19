from flask import Flask, render_template, request, jsonify, redirect, url_for
import cv2
import numpy as np
import os
from PIL import Image
import io
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def rgb_to_hsv(img):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    return hsv_img

def rgb_to_grayscale(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return gray_img

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
    else:
        result_img = image
        
    return img_array, result_img

def image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_str}"



if __name__ == '__main__':
    app.run(debug=True)