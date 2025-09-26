// Common JavaScript functionality
document.addEventListener('DOMContentLoaded', function () {
    // Add loading animation
    document.body.classList.add('loaded');

    // Highlight active menu item
    const currentPath = window.location.pathname;
    const menuItems = document.querySelectorAll('.menu a');

    menuItems.forEach(item => {
        const href = item.getAttribute('href');
        if (
            (currentPath === '/' && href === './') ||
            (currentPath === '/resume' && href === './resume') ||
            (currentPath.includes('publications') && href === './publications') ||
            (currentPath.includes('projects') && href === './projects') ||
            (currentPath.includes('blogs') && href === './blogs') ||
            (currentPath.includes('awards') && href === './awards')
        ) {
            item.classList.add('active');
        }
    });

    // Smooth scrolling for internal links
    const internalLinks = document.querySelectorAll('a[href^="#"]');
    internalLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add scroll to top button
    const scrollToTopButton = document.createElement('button');
    scrollToTopButton.innerHTML = '↑';
    scrollToTopButton.className = 'scroll-to-top';
    scrollToTopButton.setAttribute('aria-label', 'Scroll to top');
    document.body.appendChild(scrollToTopButton);

    // Show/hide scroll to top button
    window.addEventListener('scroll', function () {
        if (window.pageYOffset > 300) {
            scrollToTopButton.classList.add('show');
        } else {
            scrollToTopButton.classList.remove('show');
        }
    });

    // Scroll to top functionality
    scrollToTopButton.addEventListener('click', function () {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Add loading states for images
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('load', function () {
            this.classList.add('loaded');
        });

        // If image is already cached and loaded
        if (img.complete) {
            img.classList.add('loaded');
        }
    });

    // Lazy loading for images (if supported)
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        imageObserver.unobserve(img);
                    }
                }
            });
        });

        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(img => imageObserver.observe(img));
    }

    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('.btn-download-cv, .social-link');
    buttons.forEach(button => {
        button.addEventListener('click', function (e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                transform: scale(0);
                animation: ripple 0.6s linear;
                pointer-events: none;
            `;

            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
});

// Add CSS for ripple animation
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
    
    img {
        transition: opacity 0.3s ease;
        opacity: 0;
    }
    
    img.loaded {
        opacity: 1;
    }
`;
document.head.appendChild(style);