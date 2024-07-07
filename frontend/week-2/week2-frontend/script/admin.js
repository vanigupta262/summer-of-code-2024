document.addEventListener('DOMContentLoaded', function() {
    let products = [
      { sku: 'SKU001', name: 'Product 1', category: 'Category 1', price: 100, quantity: 10 },
      { sku: 'SKU002', name: 'Product 2', category: 'Category 2', price: 200, quantity: 20 },
      // Add more dummy products as needed
    ];
  
    const productTable = document.getElementById('productTable');
    const searchInput = document.getElementById('searchInput');
    const filterCategory = document.getElementById('filterCategory');
    const productForm = document.getElementById('productForm');
    const productModalLabel = document.getElementById('productModalLabel');
    const addProductBtn = document.getElementById('addProductBtn');
    let editIndex = -1;
  
    // Load products into table
    function loadProducts(products) {
      productTable.innerHTML = '';
      products.forEach((product, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${product.sku}</td>
          <td>${product.name}</td>
          <td>${product.category}</td>
          <td>${product.price}</td>
          <td>${product.quantity}</td>
          <td>
            <button class="btn btn-sm btn-info" onclick="viewProduct(${index})">View</button>
            <button class="btn btn-sm btn-warning" onclick="editProduct(${index})">Edit</button>
            <button class="btn btn-sm btn-danger" onclick="deleteProduct(${index})">Delete</button>
          </td>
        `;
        productTable.appendChild(row);
      });
    }
  
    // Event listeners for search and filter
    searchInput.addEventListener('input', function() {
      const query = searchInput.value.toLowerCase();
      const filteredProducts = products.filter(product => 
        product.name.toLowerCase().includes(query) ||
        product.sku.toLowerCase().includes(query)
      );
      loadProducts(filteredProducts);
    });
  
    filterCategory.addEventListener('change', function() {
      const category = filterCategory.value;
      if (category === 'Filter by Category') {
        loadProducts(products);
      } else {
        const filteredProducts = products.filter(product => product.category === category);
        loadProducts(filteredProducts);
      }
    });
  
    // Clear form fields
    function clearForm() {
      productForm.reset();
      editIndex = -1;
      productModalLabel.textContent = 'Add Product';
    }
  
    // Submit product form
    productForm.addEventListener('submit', function(event) {
      event.preventDefault();
      const newProduct = {
        sku: document.getElementById('parentSku').value || `SKU${products.length + 1}`,
        name: document.getElementById('productName').value,
        category: document.getElementById('productCategory').value,
        price: document.getElementById('productPrice').value,
        quantity: document.getElementById('productQuantity').value,
      };
  
      if (editIndex > -1) {
        products[editIndex] = newProduct;
      } else {
        products.push(newProduct);
      }
  
      loadProducts(products);
      clearForm();
      document.getElementById('productModal').click(); // Close modal
    });
  
    // Add Product button click
    addProductBtn.addEventListener('click', clearForm);
  
    window.viewProduct = function(index) {
      alert(`Viewing product ${products[index].sku}`);
      // Implement view functionality
    }
  
    window.editProduct = function(index) {
      editIndex = index;
      const product = products[index];
      document.getElementById('productName').value = product.name;
      document.getElementById('productDescription').value = product.description || '';
      document.getElementById('productPrice').value = product.price;
      document.getElementById('productQuantity').value = product.quantity;
      document.getElementById('parentSku').value = product.sku;
      document.getElementById('productCategory').value = product.category;
      document.getElementById('productModalLabel').textContent = 'Edit Product';
      const productModal = new bootstrap.Modal(document.getElementById('productModal'));
      productModal.show();
    }
  
    window.deleteProduct = function(index) {
      const confirmed = confirm(`Are you sure you want to delete product ${products[index].sku}?`);
      if (confirmed) {
        products.splice(index, 1);
        loadProducts(products);
      }
    }
  
    // Initialize products
    loadProducts(products);
  });
  