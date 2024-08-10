document.querySelectorAll('.logout').forEach(item => {
    item.addEventListener('click', event => {
        event.preventDefault();
        window.location.href = "mainpage.html";
    });
});

document.getElementById('about-link').addEventListener('click', function() {
    closeAllModals();
    document.getElementById('about-modal').style.display = 'block';
});

document.getElementById('image-link').addEventListener('click', function(event) {
    event.preventDefault();
    closeAllModals();
    document.getElementById('image-modal').style.display = 'block';
});

document.getElementById('video-link').addEventListener('click', function(event) {
    event.preventDefault();
    closeAllModals();
    document.getElementById('video-modal').style.display = 'block';
});

document.getElementById('live-link').addEventListener('click', function(event) {
    event.preventDefault();
    closeAllModals();
    document.getElementById('live-modal').style.display = 'block';
});

document.querySelectorAll('.close').forEach(item => {
    item.addEventListener('click', event => {
        event.target.closest('.modal').style.display = 'none';
    });
});

window.addEventListener('click', function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
});

function closeAllModals() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.style.display = 'none';
    });
}
