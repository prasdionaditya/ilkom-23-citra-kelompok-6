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