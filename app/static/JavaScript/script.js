document.addEventListener('DOMContentLoaded', () => {
    setupSlider();
    setupImageProcessing();
});

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
    const dropArea          = document.getElementById('drop-area');
    const fileInput         = document.getElementById('file-input');
    const uploadBtn         = document.getElementById('upload-btn');
    const previewImage      = document.getElementById('preview-image');
    const resultImage       = document.getElementById('result-image');
    const processBtn        = document.getElementById('process-btn');
    const saveBtn           = document.getElementById('save-btn');
    const applyHsvBtn       = document.getElementById('apply-hsv');
    const hueSlider         = document.getElementById('hueSlider');
    const saturationSlider  = document.getElementById('saturationSlider');
    const valueSlider       = document.getElementById('valueSlider');
    const hueValue          = document.getElementById('hueValue');
    const saturationValue   = document.getElementById('saturationValue');
    const valueValue        = document.getElementById('valueValue');

    hueSlider.addEventListener('input', () => {
        hueValue.textContent = hueSlider.value;
    });

    saturationSlider.addEventListener('input', () => {
        saturationValue.textContent = saturationSlider.value;
    });

    valueSlider.addEventListener('input', () => {
        valueValue.textContent = valueSlider.value;
    });

    let imageData = null;

    // === Upload File ===
    uploadBtn.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', () => {
        handleFile(fileInput.files[0]);
    });

    // === Drag & Drop ===
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
            handleFile(e.dataTransfer.files[0]);
        }
    });

    // === File Preview Handler ===
    function handleFile(file) {
        if (file && file.type.match('image.*')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imageData = e.target.result;
                previewImage.src = imageData;
                previewImage.style.display = 'block';
                saveBtn.style.display = 'inline-block';
            };
            reader.readAsDataURL(file);
        }
    }

    // === Process Image ===
    applyHsvBtn.addEventListener('click', () => {
        if (!imageData) {
            alert('Silakan unggah gambar terlebih dahulu.');
            return;
        }

        const hue = parseInt(hueSlider.value);
        const saturation = parseInt(saturationSlider.value);
        const value = parseInt(valueSlider.value);

        fetch('/process', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                image: imageData,
                operation: 'adjust_hsv',
                hsv_values: { hue, saturation, value }
            })
        })
        .then(res => res.json())
        .then(data => {
            previewImage.src = data.processed_image;
        })
        .catch(error => console.error('Error:', error));
    });

    // === Save Image ===
    saveBtn.addEventListener('click', () => {
        if (previewImage.src) {
            const link = document.createElement('a');
            link.download = 'processed-image.png';
            link.href = previewImage.src;
            link.click();
        } else {
            alert('Belum ada gambar yang diproses');
        }
    });
}