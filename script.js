document.addEventListener("DOMContentLoaded", function () {
  // Fetch the GIF URL from the backend
  fetchGifUrl().then(gifUrl => {
    // Set the src attribute of the second GIF img tag
    document.getElementById('gif2').src = gifUrl;
  });

  // Retrieve names from local storage and update input values
  for (let i = 1; i <= 10; i++) {
    const name = localStorage.getItem(`user${i}Name`);
    if (name) {
      document.getElementById(`user${i}Name`).value = name;
    }
  }

  const userIcons = document.querySelectorAll('.user-icon');

  userIcons.forEach(icon => {
    icon.addEventListener('click', () => {
      // Redirect to the user's webpage in the same tab
      const userPageUrl = icon.parentElement.dataset.userPageUrl;
      window.location.href = userPageUrl;
    });
  });

  // Update local storage when input values change
  document.querySelectorAll('.transparent-input').forEach(input => {
    input.addEventListener('change', function () {
      const userId = this.id.replace('Name', '');
      localStorage.setItem(`${userId}Name`, this.value);
    });
  });

  // Function to fetch GIF URL from the backend
  function fetchGifUrl() {
    // Replace 'backend_endpoint' with the actual endpoint URL to fetch the GIF URL
    return fetch('backend_endpoint')
      .then(response => response.json())
      .then(data => data.gifUrl)
      .catch(error => {
        console.error('Error fetching GIF URL:', error);
      });
  }
});
