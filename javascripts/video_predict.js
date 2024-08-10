// Video Modal specific code
document.querySelector('#video-drop-area').addEventListener('click', () => {
    document.getElementById('VideoInput').click();
});

document.getElementById('VideoInput').addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            displayVideo('#video-input', e.target.result);
        };
        reader.readAsDataURL(file);
    }
});

document.querySelectorAll('#video-modal .yolo-checkbox').forEach((checkbox) => {
    checkbox.addEventListener('click', () => {
        const checkedBoxes = getCheckedCheckboxes('#video-modal .yolo-checkbox');
        console.log('Checked checkboxes:', checkedBoxes);
    });
});

function predictVideo() {
    const checkedBoxes = getCheckedCheckboxes('#video-modal .yolo-checkbox');

    const fileInput = document.getElementById('VideoInput');
    const file = fileInput.files[0];

    const modelName = checkedBoxes.length > 0 ? checkedBoxes[0] : 'yolo-v8n-version1';

    const formData = new FormData();
    if (file) {
        formData.append('file', file);
    }
    formData.append('model_name', modelName);

    sendAjaxRequestVideo('http://127.0.0.1:3000/video', formData);
}

// Function to get values of checked checkboxes
function getCheckedCheckboxes(selector) {
    return Array.from(document.querySelectorAll(selector + ':checked')).map(cb => cb.value);
}

// Function to send AJAX request
function sendAjaxRequestVideo(url, formData) {
    $.ajax({
        url: url,
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: (result_dir) => {
            console.log('File saved at:', result_dir);
            displayVideo('#video-output', result_dir);
            
        },
    });
}

// Function to display the video in the specified element
function displayVideo(selector, src) {
    const container = document.querySelector(selector);
    container.innerHTML = ''; // Clear any existing content
    const video = document.createElement('video');
    video.src = src;
    video.controls = true; // Add video controls like play, pause, etc.
    video.style.width = '100%'; // Make the video responsive
    container.appendChild(video);
}
