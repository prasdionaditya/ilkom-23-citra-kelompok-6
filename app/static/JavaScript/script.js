// Fungsi untuk halaman index.html - Slider gambar
function setupSlider() {
    const sliderHandle = document.getElementById("sliderHandle");
    const beforeWrapper = document.querySelector(".img-before-wrapper");
    const container = document.querySelector(".split-image");

    if (!container) return;

    container.addEventListener("mousemove", (e) => {
        const rect = container.getBoundingClientRect();
        let offset = e.clientX - rect.left;
        let percent = offset / container.offsetWidth * 100;
        beforeWrapper.style.width = percent + "%";
        sliderHandle.style.left = percent + "%";
    });
}

// Fungsi untuk halaman hsv.html dan grayscale.html
function setupImageProcessing() {
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-input');
    const uploadBtn = document.getElementById('upload-btn');
    const previewImage = document.getElementById('preview-image');
    const resultImage = document.getElementById('result-image');
    const processBtn = document.getElementById('process-btn');
    const saveBtn = document.getElementById('save-btn');

    if (!dropArea || !fileInput) return;

    let imageData = null;
    let currentPage = '';

    // Determine current page
    if (window.location.pathname.includes('hsv')) {
        currentPage = 'hsv';
    } else if (window.location.pathname.includes('grayscale')) { 
        currentPage = 'grayscale';
    }

    // Handle click on upload button
    if (uploadBtn) {
        uploadBtn.addEventListener('click', () => {
            fileInput.click();
        });
    }

    // Handle file selection
    if (fileInput) {
        fileInput.addEventListener('change', handleFile);
    }

    if (dropArea) {
        dropArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropArea.style.borderColor = '#ff9800';
        });
        
        dropArea.addEventListener('dragleave', () => {
            dropArea.style.borderColor = '#aaa';
        });
        
        dropArea.addEventListener('drop', (e) => {
            e.preventDefault();
            dropArea.style.borderColor = '#aaa';
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                handleFile();
            }
        });
    }

    // Process file
    function handleFile() {
        const file = fileInput.files[0];
        if (file && file.type.match('image.*')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imageData = e.target.result;
                previewImage.src = imageData;
                previewImage.style.display = 'block';
                processBtn.style.display = 'block';
            }
            reader.readAsDataURL(file);
        }
    }

    // Process image
    if (processBtn) {
        processBtn.addEventListener('click', async () => {
            if (!imageData) return;
            
            try {
                const operation = currentPage === 'hsv' ? 'rgb_to_hsv' : 'rgb_to_grayscale';
                
                const response = await fetch('/process', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        image: imageData,
                        operation: operation
                    }),
                });
                
                const result = await response.json();
                resultImage.src = result.processed_image;
                resultImage.style.display = 'block';
                saveBtn.style.display = 'block';
            } catch (error) {
                console.error('Error processing image:', error);
                alert('Terjadi kesalahan saat memproses gambar');
            }
        });
    }

    // Save the processed image
    if (saveBtn) {
        saveBtn.addEventListener('click', () => {
            if (resultImage.src) {
                const link = document.createElement('a');
                link.download = currentPage === 'hsv' ? 'hsv-image.png' : 'grayscale-image.png';
                link.href = resultImage.src;
                link.click();
            } else {
                alert('Belum ada gambar yang diproses');
            }
        });
    }
}

// Initialize appropriate functions based on page content
document.addEventListener('DOMContentLoaded', function() {
    setupSlider();
    setupImageProcessing();
});