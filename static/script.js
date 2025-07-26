function confirmDelete() {
  if (window.confirm("Are you sure you want to delete your account? This action cannot be undone.")) {
    // If the user clicks "OK", send a request to the delete account endpoint
    deleteAccount();
  }
}

function deleteAccount() {
  // Send a POST request to the delete account endpoint using AJAX
  fetch('/delete-account', {
    method: 'DELETE'
  }).then(response => {
    if (response.ok) {
      // If the request is successful, show a success message
      alert("Your account has been deleted.");
      // Redirect the user to the home page
      window.location.href = '/';
    } else {
      // If the request fails, show an error message
      alert("An error occurred while deleting your account.");
    }
  }).catch(error => {
    // If the request fails, show an error message
    alert("An error occurred in deleting your account.");
  });
}
 const button = document.getElementById('toggle-form');
  const form = document.getElementById('my-form');

  button.addEventListener('click', () => {
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
  });




