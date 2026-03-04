// NonLogs Website - Main JavaScript

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// Button handlers
function handleLogin() {
    console.log('Login clicked');
    alert('Login functionality would go here');
}

function handleRegister() {
    console.log('Register clicked');
    alert('Register functionality would go here');
}

function handleStartTrading() {
    console.log('Start Trading clicked');
    alert('Start Trading functionality would go here');
}

function handleViewPolicy() {
    console.log('View Data Policy clicked');
    alert('View Data Policy functionality would go here');
}

function handleCreateAccount() {
    console.log('Create Account clicked');
    alert('Create Account functionality would go here');
}

function handleLearnMore() {
    console.log('Learn More clicked');
    alert('Learn More functionality would go here');
}

// Language switching
function switchLanguage(lang) {
    console.log('Language switched to:', lang);
    // Language switching logic would go here
    // This is a placeholder for localization functionality
}

// Nav transparency on scroll
const nav = document.querySelector('nav');
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        nav.style.borderBottomColor = 'rgba(45, 55, 72, 0.8)';
    } else {
        nav.style.borderBottomColor = 'rgb(45, 55, 72)';
    }
});

// Intersection Observer for animations on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all feature cards
document.querySelectorAll('.feature-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
});

// Console welcome message
console.log('%c🔒 Welcome to NonLogs - Privacy First Exchange', 'font-size: 20px; color: #00d4ff; font-weight: bold;');
console.log('%cBuilt with security, privacy, and performance in mind.', 'font-size: 14px; color: #a0aec0;');
