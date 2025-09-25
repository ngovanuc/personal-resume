// Toggle hamburger menu
function toggleMenu() {
    const hamburger = document.querySelector('.hamburger');
    const menuItems = document.querySelector('.menu-items');

    hamburger.classList.toggle('active');
    menuItems.classList.toggle('active');
}

// Close menu when clicking on a menu item (for mobile)
document.addEventListener('DOMContentLoaded', function () {
    const menuLinks = document.querySelectorAll('.menu-items a');
    const hamburger = document.querySelector('.hamburger');
    const menuItems = document.querySelector('.menu-items');

    menuLinks.forEach(link => {
        link.addEventListener('click', function () {
            // Close mobile menu when a link is clicked
            if (window.innerWidth <= 768) {
                hamburger.classList.remove('active');
                menuItems.classList.remove('active');
            }
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', function (event) {
        const menu = document.querySelector('.menu');

        if (!menu.contains(event.target) && menuItems.classList.contains('active')) {
            hamburger.classList.remove('active');
            menuItems.classList.remove('active');
        }
    });

    // Handle window resize
    window.addEventListener('resize', function () {
        if (window.innerWidth > 768) {
            hamburger.classList.remove('active');
            menuItems.classList.remove('active');
        }
    });

    // Add smooth scroll effect for better UX
    menuLinks.forEach(link => {
        link.addEventListener('mouseenter', function () {
            this.style.transform = 'translateY(-2px) scale(1.05)';
        });

        link.addEventListener('mouseleave', function () {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
});

// Add loading animation
window.addEventListener('load', function () {
    const menuItems = document.querySelector('.menu-items');
    const menuChildren = menuItems.children;

    // Animate menu items one by one
    Array.from(menuChildren).forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(20px)';

        setTimeout(() => {
            item.style.transition = 'all 0.5s ease';
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
        }, index * 100);
    });
});