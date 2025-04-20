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