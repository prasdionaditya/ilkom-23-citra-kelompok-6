# Ilkom-23 Citra Kelompok 6

## Deskripsi
Proyek ini adalah aplikasi berbasis web untuk **analisis citra** (image processing), mencakup fungsi seperti deteksi warna, konversi ke grayscale, analisis HSV, dan lainnya.

Dibangun menggunakan:
- **Python** (menggunakan framework seperti Flask/Django)
- **HTML**, **CSS**, **JavaScript** untuk frontend
- Struktur file statis dan template yang terorganisir.

## Struktur Folder
```
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── foto/
│   │   │   ├── background.jpg
│   │   │   ├── berwarna.jpg
│   │   │   ├── berwarnaaa.jpg
│   │   │   ├── detectone.jpg
│   │   │   ├── logo.png
│   │   │   ├── tool1.jpg
│   │   │   ├── tool2.jpg
│   │   │   └── tool3.jpg
│   │   ├── JavaScript/
│   │   │   └── script.js
│   │   └── uploads/         # Folder tambahan untuk upload file gambar
│   ├── templates/
│   │   ├── analisis.html
│   │   ├── deteksi_warna.html
│   │   ├── grayscale.html
│   │   ├── hsv.html
│   │   └── index.html
│   └── app.py
├── .gitignore
├── ACKNOWLEDGEMENTS.md
├── FAQ.md
├── FEATURES.md
├── GLOSSARY.md
├── INSTALLATION.md
├── project_plan.md          # Rencana proyek
├── README.md                 # Dokumentasi utama (ini file yang sedang kamu baca)
├── requirements.txt          # Daftar library Python yang diperlukan
├── Team.md                   # Daftar anggota tim
├── technical_documentation.md # Dokumentasi teknis
```

## Penjelasan Folder dan File
- **app/static/**: Menyimpan file statis seperti CSS, JavaScript, gambar, dan folder upload file.
- **app/templates/**: Menyimpan file HTML untuk halaman-halaman web.
- **app/app.py**: File Python utama untuk mengatur server dan routing.
- **uploads/**: Folder untuk menyimpan file yang diupload oleh pengguna.
- **requirements.txt**: Berisi daftar dependensi Python yang harus di-install.
- **project_plan.md**: Rencana pengembangan proyek.
- **Team.md**: Berisi informasi anggota tim.
- **technical_documentation.md**: Menjelaskan teknis aplikasi, API, atau alur data.
- **README.md**: Dokumentasi utama proyek.
- **ACKNOWLEDGEMENTS.md, FAQ.md, FEATURES.md, GLOSSARY.md, INSTALLATION.md**: Dokumentasi tambahan untuk melengkapi informasi proyek.

## Cara Menjalankan
1. Pastikan Python sudah terinstal di sistem.
2. Install dependencies dengan perintah:
    ```bash
    pip install -r requirements.txt
    ```
3. Jalankan server:
    ```bash
    python app.py
    ```
4. Buka browser dan akses:
    ```
    http://localhost:5000/
    ```
   (atau sesuai port yang digunakan)

## Catatan
- Semua file statis seperti gambar, CSS, dan JavaScript harus dipanggil menggunakan `url_for('static', filename='...')` (jika menggunakan Flask).
- Pastikan folder `uploads/` memiliki izin tulis (writable) untuk bisa menyimpan file upload.

# FAQ


# FAQ (Frequently Asked Questions) - Deteksi Warna


## 1. Apa itu Deteksi Warna?
**Deteksi Warna** adalah aplikasi yang memungkinkan pengguna untuk mendeteksi warna dominan dalam gambar. Pengguna dapat mengunggah gambar, dan aplikasi akan menampilkan warna dominan dalam format   Grayscale ke RGB

---

## 2. Apa saja format gambar yang didukung?
Saat ini, aplikasi ini mendukung format gambar berikut:
- JPEG
- PNG
- BMP

## 3. Bagaimana cara menggunakan website deteksi warna ini?
Setelah aplikasi berjalan di localhost, ikuti langkah-langkah berikut:
1. **Unggah Gambar**: Pilih gambar yang ingin kamu deteksi warnanya.
2. **Deteksi Warna**: Aplikasi akan memproses gambar dan menampilkan warna dominan dalam format RGB, HEX, dan HSV.
3. **Konversi Warna**: Kamu dapat mengonversi warna yang terdeteksi dari RGB ke HEX atau sebaliknya.

---

## 4. Apakah ada batasan ukuran gambar?
Meskipun aplikasi dapat mendeteksi warna dari gambar dengan ukuran besar, kami sarankan untuk mengunggah gambar dengan ukuran kurang dari 10 MB untuk kinerja yang optimal.

---

## 5. Bagaimana cara berkontribusi pada proyek ini?
Kami menyambut baik kontribusi dari kamu! Untuk informasi lebih lanjut tentang cara berkontribusi, silakan baca panduan kontribusi di [CONTRIBUTING.md](CONTRIBUTING.md).

# FEATURES

# Fitur-Fitur - Proyek Deteksi Warna

Berikut ini adalah fitur-fitur yang tersedia dalam proyek deteksi warna:

## Fitur Utama

- 📷 **Deteksi Warna Dominan dari Gambar**
  - Upload gambar dari komputer.
  - Klik pada gambar untuk mendeteksi warna.

- 🎨 **Konversi Nilai Warna Grayscale ke RGB**
  - Grayscale ke RGB

 - 🎨 **Konversi Warna Gambar ke HSV**
  -  Gambar ke HSV
 
  - 🎨 **Deteksi Warna Dominan**
  - Deteksi Warna Dominan
 
- 📄 **Export Data**
  - Menyimpan hasil deteksi warna ke dalam file `.csv`.

# GLOSSARY

# Glossary - Deteksi Warna/DetecTone

Daftar istilah teknis yang digunakan dalam proyek **Deteksi Warna**.

---

## 🧩 Daftar Istilah

### 1. Deteksi Warna
Proses identifikasi warna dominan atau spesifik dari sebuah gambar atau citra digital.

### 2. Grayscale
Transformasi gambar berwarna menjadi gambar hitam putih, di mana setiap piksel hanya menyimpan informasi intensitas cahaya (tanpa warna).

### 3. Warna Dominan
Warna yang paling sering muncul dalam sebuah gambar.

### 4. RGB (Red, Green, Blue)
Model warna digital yang menggunakan kombinasi cahaya merah, hijau, dan biru untuk merepresentasikan warna.

### 5. Histogram Warna
Grafik distribusi intensitas warna dalam gambar.

### 6. Palette
Sekumpulan warna yang digunakan bersama-sama untuk desain atau analisis.

### 7. Konversi Warna
Proses mengubah representasi warna suatu gambar ke model atau skala warna lain (contoh: dari RGB ke Grayscale).

### 8. Machine Learning
Cabang dari kecerdasan buatan (AI) yang memungkinkan sistem belajar dari data untuk meningkatkan performa dalam tugas tertentu, seperti analisis warna.

### 9. API (Application Programming Interface)
Sekumpulan definisi dan protokol yang memungkinkan dua aplikasi berkomunikasi satu sama lain.

### 10. Deployment
Proses pengiriman aplikasi dari lingkungan pengembangan ke produksi sehingga bisa diakses oleh pengguna.

### 11. Python 
Python adalah bahasa pemrograman tingkat tinggi yang dinamis dan terstruktur yang sangat populer di berbagai bidang, seperti pengembangan web, analisis data, kecerdasan buatan (AI), pembelajaran mesin (machine learning), dan banyak lagi.

### 12. HSV
HSV (Hue, Saturation, Value) adalah model warna yang sering digunakan dalam pengolahan citra dan grafik komputer. Model ini menggambarkan warna berdasarkan tiga parameter utama:

Hue (H):

Merupakan warna dasar atau jenis warna, yang diukur dalam derajat dari 0 hingga 360.

0° adalah merah, 120° adalah hijau, 240° adalah biru, dan 360° kembali ke merah.

Hue memberikan identitas utama warna, misalnya apakah itu merah, biru, kuning, dll.

Saturation (S):

Mengukur seberapa "murni" warna tersebut. Saturasi berkisar dari 0 hingga 100%.

Saturasi 0% berarti warna tersebut akan menjadi abu-abu (tidak ada warna asli), sedangkan 100% menunjukkan warna yang paling murni (penuh warna).

Value (V):

Mengukur seberapa terang atau gelap warna tersebut, dengan rentang 0 hingga 100%.

Value 0% berarti warna tersebut sepenuhnya gelap (hitam), dan value 100% berarti warna tersebut sepenuhnya terang.

### 13. Citra Digital
Gambar yang disimpan dalam format digital, terdiri dari piksel-piksel yang mewakili informasi warna atau intensitas cahaya.

### 14. Segmentasi Citra
Proses membagi gambar menjadi beberapa bagian atau segmen berdasarkan karakteristik tertentu, seperti warna atau tekstur, untuk memudahkan analisis lebih lanjut.

### 15. Filter
Proses penerapan operasi matematika pada gambar untuk memperbaiki atau memodifikasi karakteristik gambar, seperti mengurangi noise atau menonjolkan fitur tertentu.

### 16. Piksel
Elemen terkecil dalam sebuah gambar digital yang mewakili nilai warna atau intensitas cahaya.

### 17. Color Space
Sistem koordinat yang digunakan untuk mewakili warna dalam berbagai model warna, seperti RGB, HSV, CMYK, dll.

### 18. Noise
Gangguan atau ketidakteraturan dalam citra yang biasanya disebabkan oleh kesalahan dalam proses pengambilan gambar atau pengolahan citra.

### 19. Kecerahan (Brightness)
Ukuran seberapa terang atau gelap gambar secara keseluruhan. Dalam model HSV, ini diwakili oleh parameter **Value**.

### 21. Redundansi Warna
Ketika dua atau lebih warna yang sangat mirip atau serupa mendominasi dalam gambar, sehingga sulit membedakan satu sama lain dalam analisis.

### 22. Color Mapping
Proses pemetaan warna tertentu pada piksel-piksel dalam gambar untuk tujuan visualisasi atau pemrosesan lebih lanjut.

### 23. Image Thresholding
Metode untuk memisahkan objek dari latar belakang dalam gambar berdasarkan nilai piksel yang ditentukan oleh threshold.

### 24. Color Calibration
Proses penyesuaian warna pada citra digital agar sesuai dengan representasi warna yang sebenarnya, dengan mengoreksi pengaruh perangkat seperti kamera atau monitor.

### 25. Saturation Adjustment
Proses mengubah seberapa kuat atau pudar warna dalam gambar, sering digunakan dalam pengeditan gambar dan analisis warna.

### 26. Binarisasi
Proses mengonversi gambar menjadi dua warna (hitam dan putih) berdasarkan nilai intensitas atau threshold, digunakan dalam banyak aplikasi pengolahan citra, seperti deteksi objek.

---

Dengan tambahan ini, glossary untuk **Deteksi Warna** menjadi lebih komprehensif dan dapat mencakup berbagai aspek yang terlibat dalam proyek ini. Jika ada istilah lain yang ingin ditambahkan, beri tahu saya!
---

# INSTALLATION

# Panduan Instalasi dan Pengaturan Proyek Deteksi Warna

Panduan ini memberikan langkah-langkah rinci untuk menginstal dan menyiapkan **Proyek Deteksi Warna** di komputer lokal. Ikuti instruksi di bawah ini untuk memulai.

## Persyaratan Sistem

Sebelum memulai, pastikan sistem kamu memiliki perangkat lunak berikut:

- **Node.js** versi 14.0.0 atau lebih tinggi (untuk menjalankan server dan aplikasi backend).
- **npm** (Node Package Manager, terinstal otomatis bersama Node.js).
- **Git** (untuk meng-clone repository dari GitHub).
- **Editor Teks** seperti **Visual Studio Code** (untuk memodifikasi kode jika diperlukan).

### Instalasi Node.js
- Kunjungi [situs resmi Node.js](https://nodejs.org/) dan unduh versi terbaru yang stabil.
- Ikuti petunjuk instalasi untuk sistem operasi kamu (Windows, macOS, atau Linux).

### Instalasi Git
- Kunjungi [situs resmi Git](https://git-scm.com/) dan ikuti panduan untuk menginstal Git sesuai dengan sistem operasi kamu.

---

## Langkah-langkah Instalasi

### 1. Clone Repository

Langkah pertama adalah meng-clone repository **Deteksi Warna** dari GitHub ke komputer lokal kamu:

1. Buka terminal atau command prompt.
2. Jalankan perintah berikut untuk meng-clone repository:
   ```bash
   git clone https://github.com/prasdionaditya/ilkom-23-citra-kelompok-6.git
   cd deteksi-warna
