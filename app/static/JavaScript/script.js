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