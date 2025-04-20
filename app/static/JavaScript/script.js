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
  
  // Fungsi untuk halaman hsv.html, grayscale.html, dan deteksi_warna.html
  function setupImageProcessing() {
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-input');
    const uploadBtn = document.getElementById('upload-btn');
    const previewImage = document.getElementById('preview-image');
    const resultImage = document.getElementById('result-image');
    const processBtn = document.getElementById('process-btn');
    const saveBtn = document.getElementById('save-btn');
    const resultContainer = document.getElementById('result-container');
    
    if (!dropArea || !fileInput) return;
    
    let imageData = null;
    let currentPage = '';
    
    // Determine current page
    if (window.location.pathname.includes('hsv')) {
      currentPage = 'hsv';
    } else if (window.location.pathname.includes('grayscale')) {
      currentPage = 'grayscale';
    } else if (window.location.pathname.includes('deteksi_warna')) {
      currentPage = 'deteksi_warna';
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
          
          // Update drop area message
          const dropAreaText = dropArea.querySelector('p');
          if (dropAreaText) {
            dropAreaText.style.display = 'none';
          }
        }
        reader.readAsDataURL(file);
      }
    }
    
    // Process image
    if (processBtn) {
      processBtn.addEventListener('click', async () => {
        if (!imageData) return;
        
        try {
          let endpoint;
          let operation;
          let requestBody = { image: imageData };
          
          if (currentPage === 'hsv') {
            endpoint = '/process';
            requestBody.operation = 'rgb_to_hsv';
          } else if (currentPage === 'grayscale') {
            endpoint = '/process';
            requestBody.operation = 'rgb_to_grayscale';
          } else if (currentPage === 'deteksi_warna') {
            endpoint = '/detect_colors';
            // Bisa tambahkan parameter jumlah warna jika ingin kustom
            requestBody.num_colors = 5;
          }
          
          processBtn.disabled = true;
          processBtn.textContent = 'Memproses...';
          
          const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody),
          });
          
          const result = await response.json();
          
          if (currentPage === 'deteksi_warna') {
            // Handle color detection results
            displayDominantColors(result.dominant_colors);
          } else {
            // Handle HSV and grayscale results
            resultImage.src = result.processed_image;
            resultImage.style.display = 'block';
          }
          
          saveBtn.style.display = 'block';
          processBtn.disabled = false;
          processBtn.textContent = currentPage === 'deteksi_warna' ? 'Deteksi Warna' : 'Proses Gambar';
        } catch (error) {
          console.error('Error processing image:', error);
          alert('Terjadi kesalahan saat memproses gambar');
          processBtn.disabled = false;
          processBtn.textContent = currentPage === 'deteksi_warna' ? 'Deteksi Warna' : 'Proses Gambar';
        }
      });
    }
    
    // Display dominant colors
    function displayDominantColors(colors) {
      if (!resultContainer) return;
      
      // Clear previous results
      resultContainer.innerHTML = '';
      
      // Create a container for the original image
      if (currentPage === 'deteksi_warna') {
        const imgContainer = document.createElement('div');
        imgContainer.style.marginBottom = '15px';
        
        const originalImg = document.createElement('img');
        originalImg.src = imageData;
        originalImg.style.maxWidth = '100%';
        originalImg.style.maxHeight = '120px';
        originalImg.style.borderRadius = '5px';
        originalImg.style.marginBottom = '10px';
        
        resultContainer.appendChild(imgContainer);
      }
      
      // Check if there are any colors detected
      if (colors.length === 0) {
        const noColors = document.createElement('div');
        noColors.textContent = 'Tidak ada warna dominan yang terdeteksi';
        noColors.style.color = '#333';
        resultContainer.appendChild(noColors);
        return;
      }
      
      // Create scrollable container for colors
      const colorsContainer = document.createElement('div');
      colorsContainer.style.maxHeight = '180px';
      colorsContainer.style.overflowY = 'auto';
      colorsContainer.style.width = '100%';
      
      // Create elements for each color
      colors.forEach(color => {
        const colorBox = document.createElement('div');
        colorBox.className = 'color-box';
        colorBox.style.display = 'flex';
        colorBox.style.alignItems = 'center';
        colorBox.style.marginBottom = '8px';
        colorBox.style.backgroundColor = 'rgba(255, 255, 255, 0.9)';
        colorBox.style.borderRadius = '5px';
        colorBox.style.padding = '8px';
        
        const colorSwatch = document.createElement('div');
        colorSwatch.style.width = '30px';
        colorSwatch.style.height = '30px';
        colorSwatch.style.backgroundColor = color.hex;
        colorSwatch.style.borderRadius = '4px';
        colorSwatch.style.marginRight = '10px';
        colorSwatch.style.border = '1px solid #ddd';
        
        const colorInfo = document.createElement('div');
        colorInfo.style.color = '#333';
        colorInfo.style.fontSize = '14px';
        colorInfo.innerHTML = `
          <div style="font-weight: bold;">${color.hex}</div>
          <div>RGB: ${color.rgb.join(', ')}</div>
          <div>${color.percentage}%</div>
        `;
        
        colorBox.appendChild(colorSwatch);
        colorBox.appendChild(colorInfo);
        colorsContainer.appendChild(colorBox);
      });
      
      resultContainer.appendChild(colorsContainer);
    }
    
    // Save the processed image or color results
    if (saveBtn) {
      saveBtn.addEventListener('click', () => {
        if (currentPage === 'deteksi_warna') {
          if (typeof html2canvas !== 'undefined') {
            // Use html2canvas to save the color detection results
            html2canvas(resultContainer).then(canvas => {
              const link = document.createElement('a');
              link.download = 'warna-dominan.png';
              link.href = canvas.toDataURL('image/png');
              link.click();
            });
          } else {
            alert('Fitur simpan hasil memerlukan html2canvas. Pastikan library sudah dimuat.');
          }
        } else if (resultImage && resultImage.src) {
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