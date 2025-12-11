const uploadZone = document.getElementById('uploadZone');
const fileInput = document.getElementById('fileInput');
const preview = document.getElementById('preview');
const previewImage = document.getElementById('previewImage');
const cancelBtn = document.getElementById('cancelBtn');
const uploadBtn = document.getElementById('uploadBtn');
const loading = document.getElementById('loading');
const success = document.getElementById('success');
const error = document.getElementById('error');
const errorText = document.getElementById('errorText');

let selectedFile = null;

fileInput.addEventListener('change', handleFileSelect);
cancelBtn.addEventListener('click', resetUpload);
uploadBtn.addEventListener('click', uploadPhoto);

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
        showError('Seleziona un file immagine valido');
        return;
    }

    if (file.size > 10 * 1024 * 1024) {
        showError('Il file è troppo grande. Massimo 10MB');
        return;
    }

    selectedFile = file;
    const reader = new FileReader();

    reader.onload = (e) => {
        previewImage.src = e.target.result;
        uploadZone.classList.add('hidden');
        preview.classList.remove('hidden');
    };

    reader.readAsDataURL(file);
}

function resetUpload() {
    selectedFile = null;
    fileInput.value = '';
    preview.classList.add('hidden');
    uploadZone.classList.remove('hidden');
    hideMessages();
}

async function uploadPhoto() {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('photo', selectedFile);

    preview.classList.add('hidden');
    loading.classList.remove('hidden');

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        loading.classList.add('hidden');

        if (response.ok) {
            success.classList.remove('hidden');
            setTimeout(() => {
                resetUpload();
            }, 3000);
        } else {
            showError(data.error || 'Errore durante il caricamento');
        }
    } catch (err) {
        loading.classList.add('hidden');
        showError('Errore di connessione. Riprova.');
        console.error('Upload error:', err);
    }
}

function showError(message) {
    errorText.textContent = message;
    error.classList.remove('hidden');
    setTimeout(() => {
        error.classList.add('hidden');
        resetUpload();
    }, 3000);
}

function hideMessages() {
    success.classList.add('hidden');
    error.classList.add('hidden');
}