# note, program belum sepenuhnya selesai
# tujuan ini dibentuk untuk keperluan pengembangan program

from flask import Flask, render_template, request, jsonify, url_for, redirect
import cv2
import numpy as np
import os
from PIL import Image
import io
import base64
from sklearn.cluster import KMeans
import matplotlib.colors as mcolors

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def rgb_to_hsv(img):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    return hsv_img

def rgb_to_grayscale(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return gray_img

def get_dominant_colors(img, num_colors=5):

    pixels = img.reshape(-1, 3)
    
    clt = KMeans(n_clusters=num_colors)
    clt.fit(pixels)
    
    colors = clt.cluster_centers_
    
    colors = colors.astype(int)
    
    hex_colors = ['#%02x%02x%02x' % (r, g, b) for r, g, b in colors]
    
    labels = clt.labels_
    count_labels = np.bincount(labels)
    percentages = count_labels / len(labels) * 100
    
  
    color_info = sorted(
        zip(hex_colors, percentages),
        key=lambda x: x[1],
        reverse=True
    )
    
    return color_info

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
    
    elif operation == 'dominant_colors':
        
        color_info = get_dominant_colors(img_array)
       
        result_img = image
        return img_array, result_img, color_info
    
    return img_array, result_img, None

def image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_str}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
   
    image_data = request.json['image']
    operation = request.json['operation']
    
    original, processed, color_info = process_image(image_data, operation)
    
    processed_base64 = image_to_base64(processed)
    
    response = {
        'processed_image': processed_base64,
    }
    
    if operation == 'dominant_colors' and color_info:
        response['colors'] = color_info
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
