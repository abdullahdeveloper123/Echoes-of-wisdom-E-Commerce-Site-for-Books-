  // Theme Toggle Functionality
    function toggleTheme() {
      const body = document.body;
      const themeIcon = document.getElementById('theme-icon');
      const mobileThemeIcon = document.getElementById('mobile-theme-icon');

      if (body.getAttribute('data-theme') === 'light') {
        body.setAttribute('data-theme', 'dark');
        themeIcon.className = 'fas fa-moon';
        mobileThemeIcon.className = 'fas fa-moon';
        localStorage.setItem('theme', 'dark');
      } else {
        body.setAttribute('data-theme', 'light');
        themeIcon.className = 'fas fa-sun';
        mobileThemeIcon.className = 'fas fa-sun';
        localStorage.setItem('theme', 'light');
      }
    }

    // Load saved theme
    document.addEventListener('DOMContentLoaded', function () {
      const savedTheme = localStorage.getItem('theme') || 'light';
      const body = document.body;
      const themeIcon = document.getElementById('theme-icon');
      const mobileThemeIcon = document.getElementById('mobile-theme-icon');

      body.setAttribute('data-theme', savedTheme);
      if (savedTheme === 'dark') {
        themeIcon.className = 'fas fa-moon';
        mobileThemeIcon.className = 'fas fa-moon';
      }
    });

    // Mobile Navigation Toggle
    function toggleMobileNav() {
      const hamburger = document.querySelector('.nav-hamburger');
      const sidebar = document.getElementById('mobile-sidebar');

      hamburger.classList.toggle('active');
      sidebar.classList.toggle('active');
    }

    // Close mobile nav when clicking outside
    document.addEventListener('click', function (event) {
      const sidebar = document.getElementById('mobile-sidebar');
      const hamburger = document.querySelector('.nav-hamburger');

      if (!sidebar.contains(event.target) && !hamburger.contains(event.target)) {
        sidebar.classList.remove('active');
        hamburger.classList.remove('active');
      }
    });

    // Carousel Functionality
    let currentSlideIndex = 0;
    const slides = document.querySelectorAll('.carousel-slide');
    const dots = document.querySelectorAll('.carousel-dot');
    const track = document.getElementById('carousel-track');

    function showSlide(index) {
      currentSlideIndex = index;
      track.style.transform = `translateX(-${index * 100}%)`;

      dots.forEach((dot, i) => {
        dot.classList.toggle('active', i === index);
      });
    }

    function nextSlide() {
      currentSlideIndex = (currentSlideIndex + 1) % slides.length;
      showSlide(currentSlideIndex);
    }

    function previousSlide() {
      currentSlideIndex = (currentSlideIndex - 1 + slides.length) % slides.length;
      showSlide(currentSlideIndex);
    }

    function currentSlide(index) {
      showSlide(index - 1);
    }

    // Auto-play carousel
    setInterval(nextSlide, 5000);

    // Search Functionality
    function search() {
      fetch('http://127.0.0.1:8000/search/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 'query': document.getElementById('search_input').value })
      })
        .then(response => response.json())
        .then(data => {
          let quotes_collection = document.getElementById('quotes-collection')
          quotes_collection.innerHTML = ''

          for (let i = 0; i < data.length; i++) {
            let a = document.createElement('a')
            a.classList.add('quote-card')
            a.setAttribute('href', `http://127.0.0.1:8000/details/${data[i].id}`)

            let quoteContent = document.createElement('div')
            quoteContent.classList.add('quote-content')
            quoteContent.textContent = data[i].name

            let authorName = document.createElement('div')
            authorName.classList.add('author_name')
            authorName.textContent = "— " + data[i].author

            a.appendChild(quoteContent)
            a.appendChild(authorName)
            quotes_collection.appendChild(a)
          }
        })
        .catch(error => console.error("Error:", error))
    }

    // Add enter key support for search
    document.getElementById('search_input').addEventListener('keypress', function (event) {
      if (event.key === 'Enter') {
        search();
      }
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      });
    });

    // Add loading animation for search
    function search() {
      const searchButton = document.querySelector('.search-button');
      const originalText = searchButton.innerHTML;

      searchButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Searching...';
      searchButton.disabled = true;

      fetch('http://127.0.0.1:8000/main/search/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 'query': document.getElementById('search_input').value })
      })
        .then(response => response.json())
        .then(data => {
          let quotes_collection = document.getElementById('quotes-collection')
          quotes_collection.innerHTML = ''

          for (let i = 0; i < data.length; i++) {
            let a = document.createElement('a')
            a.classList.add('quote-card')
            a.setAttribute('href', `http://127.0.0.1:8000/main/details/${data[i].id}`)

            let quoteContent = document.createElement('div')
            quoteContent.classList.add('quote-content')
            quoteContent.textContent = data[i].name

            let authorName = document.createElement('div')
            authorName.classList.add('author_name')
            authorName.textContent = "— " + data[i].author

            a.appendChild(quoteContent)
            a.appendChild(authorName)
            quotes_collection.appendChild(a)
          }
        })
        .catch(error => console.error("Error:", error))
        .finally(() => {
          searchButton.innerHTML = originalText;
          searchButton.disabled = false;
        });
    }