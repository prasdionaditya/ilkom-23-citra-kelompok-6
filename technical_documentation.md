# Dokumentasi Teknis Proyek Konversi Warna & Deteksi Warna Dominan

## 1. Pendahuluan
Proyek ini bertujuan untuk melakukan konversi warna serta mendeteksi warna dominan dalam sebuah gambar. Dokumentasi ini menjelaskan arsitektur proyek, algoritma yang digunakan, dependensi, serta cara penggunaan.

## 2. Arsitektur Proyek
Proyek ini terdiri dari beberapa komponen utama:
- **Input Gambar**: Pengguna dapat mengunggah gambar.
- **Konversi Warna**: Mengubah warna gambar ke format lain (misalnya RGB ke HEX, RGB ke HSV, dll.).
- **Deteksi Warna Dominan**: Menggunakan algoritma clustering untuk menentukan warna dominan dalam gambar.
- **Output**: Menampilkan hasil konversi dan warna dominan kepada pengguna.

## 3. Teknologi yang Digunakan
- **Python** dengan pustaka OpenCV dan PIL untuk manipulasi gambar.
- **JavaScript** untuk tampilan antarmuka jika berbasis web.
- **Flask/Django** (jika menggunakan backend Python) untuk API.
- **React/Vanilla JS** (jika berbasis frontend) untuk tampilan.

## 4. Algoritma yang Digunakan
### a. Konversi Warna
Menggunakan rumus konversi warna seperti:
- **RGB ke HEX**: `HEX = '#{:02x}{:02x}{:02x}'.format(R, G, B)`
- **RGB ke HSV**: Menggunakan OpenCV: `cv2.cvtColor(image, cv2.COLOR_RGB2HSV)`

### b. Deteksi Warna Dominan
Menggunakan algoritma **K-Means Clustering**:
1. Gambar dikonversi menjadi array pixel.
2. K-Means diterapkan untuk mengelompokkan warna.
3. Warna dengan jumlah piksel terbesar dianggap sebagai warna dominan.

## 5. Instalasi dan Penggunaan
### a. Instalasi
Jika menggunakan Python:
```bash
pip install opencv-python numpy pillow
```

### b. Menjalankan Program
Jika berbasis Python:
```bash
python main.py
```
Jika berbasis web:
```bash
npm install
npm start
```

## 6. Contoh Hasil
Berikut adalah contoh hasil deteksi warna dominan dari sebuah gambar:
![Contoh Hasil](docs/images/contoh_hasil.png)

## 7. Kesimpulan
Proyek ini dapat digunakan untuk berbagai keperluan seperti desain grafis, analisis warna, dan lain sebagainya. Dokumentasi ini akan terus diperbarui seiring dengan pengembangan proyek.
