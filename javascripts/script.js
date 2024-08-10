const container = document.querySelector('.container');
const signupButton = document.querySelector('.signup-section header');
const loginButton = document.querySelector('.login-section header');

loginButton.addEventListener('click', () => {
    container.classList.add('active');
});

signupButton.addEventListener('click', () => {
    container.classList.remove('active');
});

function validateAndRedirect() {
    // Lấy giá trị từ ô nhập liệu
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    // Kiểm tra điều kiện (thay thế bằng điều kiện của bạn)
    if (username === "admin@gmail.com" && password === "admin") {
        // Nếu đúng, chuyển hướng
        window.location.href = 'main.html';
    } else {
        // Nếu sai, thông báo lỗi và chuyển về trang login
        alert("Tên đăng nhập hoặc mật khẩu không đúng.");
        window.location.href = 'index.html'; // Thay 'login.html' bằng đường dẫn tới trang login của bạn
    }
}