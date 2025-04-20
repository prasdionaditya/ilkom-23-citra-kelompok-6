// Fungsi untuk halaman index.html - Slider gambar
function setupSlider() {
    const sliderHandle = document.getElementById("sliderHandle");
    const beforeWrapper = document.querySelector(".img-before-wrapper");
    const container = document.querySelector(".split-image");

    if (!container) return;