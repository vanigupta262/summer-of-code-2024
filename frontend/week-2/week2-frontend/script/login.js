document.addEventListener('DOMContentLoaded', function() {
  const loginForm = document.querySelector('#login form');
  const registerForm = document.querySelector('#register form');

  loginForm.addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('loginUserName').value;
    const password = document.getElementById('loginPassword').value;
    const role = document.getElementById('loginRole').value;

    if (email && password && role !== 'Select Role') {
      loginUser(email, password, role);
    } else {
      alert('Please fill in all fields.');
    }
  });

  registerForm.addEventListener('submit', function(event) {
    event.preventDefault();
    alert('Registration functionality not implemented.');
  });

  function loginUser(email, password, role) {
    fetch('http://167.71.236.10/api/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: email,
        password: password
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.token) {
        localStorage.setItem('authToken', data.token);
        localStorage.setItem('userRole', role);
        localStorage.setItem('username', email);
        if (role === 'admin') {
          window.location.href = '../templates/admin-dashboard.html';
        } else if (role === 'cashier') {
          window.location.href = '../templates/cashier-dashboard.html';
        }
      } else {
        alert('Login failed. Please check your credentials.');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred. Please try again.');
    });
  }
});
