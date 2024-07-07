document.addEventListener('DOMContentLoaded', function() {
    const role = localStorage.getItem('userRole');
    const username = localStorage.getItem('username');
  
    if (role && username) {
      if (role === 'admin') {
        document.getElementById('adminName').textContent = username;
      } else if (role === 'cashier') {
        document.getElementById('cashierName').textContent = username;
      }
    }
  
    document.getElementById('logout').addEventListener('click', function() {
      localStorage.clear();
      window.location.href = 'index.html';
    });
  });
  