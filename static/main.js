// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            if (mobileMenu.classList.contains('max-h-0')) {
                mobileMenu.classList.remove('max-h-0');
                mobileMenu.classList.add('max-h-96');
            } else {
                mobileMenu.classList.remove('max-h-96');
                mobileMenu.classList.add('max-h-0');
            }
        });
    }
});

// Add any additional JavaScript that should be available site-wide here
