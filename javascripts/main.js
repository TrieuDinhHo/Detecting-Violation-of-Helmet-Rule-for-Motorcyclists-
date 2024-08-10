document.querySelectorAll('.redirect-login').forEach(item => {
    item.addEventListener('click', event => {
        event.preventDefault();
        window.location.href = "index.html"; // Đường dẫn đến trang index.html
    });
});
