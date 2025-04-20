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

---

