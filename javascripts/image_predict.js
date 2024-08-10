// Image Modal specific code
document.querySelector('#image-drop-area').addEventListener('click', () => {
    document.getElementById('ImageInput').click();
});

document.getElementById('ImageInput').addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            displayImage('#image-input', e.target.result);
        };
        reader.readAsDataURL(file);
    }
});

document.querySelectorAll('#image-modal .yolo-checkbox').forEach((checkbox) => {
    checkbox.addEventListener('click', () => {
        const checkedBoxes = getCheckedCheckboxes('#image-modal .yolo-checkbox');
        console.log('Checked checkboxes:', checkedBoxes);
    });
});

function predictImage() {
    const checkedBoxes = getCheckedCheckboxes('#image-modal .yolo-checkbox');

    const fileInput = document.getElementById('ImageInput');
    const file = fileInput.files[0];

    const modelName = checkedBoxes.length > 0 ? checkedBoxes[0] : 'yolo-v8n-version1';

    const formData = new FormData();
    if (file) {
        formData.append('file', file);
    }
    formData.append('model_name', modelName);

    sendAjaxRequestImage('http://127.0.0.1:3000/image', formData);
}


// document.querySelector('.btn').addEventListener('click', predict);


// Function to get values of checked checkboxes
function getCheckedCheckboxes(selector) {
    return Array.from(document.querySelectorAll(selector + ':checked')).map(cb => cb.value);
}

// Function to send AJAX request
function sendAjaxRequestImage(url, formData) {
    $.ajax({
        url: url,
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: (result_dir) => {
            console.log('File saved at:', result_dir);
            // test_dir = './sample_image/output/file_20240803_164638_50098.jpg'
            displayImage('#image-output', result_dir);
            
        },
    });
}

// Function to display an image in the specified container
function displayImage(containerSelector, src) {
    const container = document.querySelector(containerSelector);
    const img = document.createElement('img');
    img.src = src;
    container.innerHTML = '';
    container.appendChild(img);
}
