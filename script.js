function toggleMenu() {
  const menu = document.querySelector(".menu-links");
  const icon = document.querySelector(".hamburger-icon");
  menu.classList.toggle("open");
  icon.classList.toggle("open");
}

// Initialize AOS unless user prefers reduced motion
document.addEventListener('DOMContentLoaded', () => {
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches && typeof AOS !== 'undefined') {
    AOS.init({
      duration: 700,
      easing: 'ease-out-cubic',
      once: true,
      mirror: false,
    });
  }
  updateProgress();
  onScrollParallax();
});

// Scroll progress bar
const progressBar = document.getElementById('scroll-progress');
function updateProgress() {
  const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
  const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  const percent = docHeight ? (scrollTop / docHeight) * 100 : 0;
  if (progressBar) progressBar.style.width = percent + '%';
}
window.addEventListener('scroll', updateProgress, { passive: true });
window.addEventListener('resize', updateProgress);

// Lightweight parallax for elements with data-speed
const parallaxEls = document.querySelectorAll('[data-speed]');
let ticking = false;
function onScrollParallax() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  parallaxEls.forEach(el => {
    const speed = parseFloat(el.dataset.speed) || 0.06;
    const rect = el.getBoundingClientRect();
    const center = rect.top + rect.height / 2 - window.innerHeight / 2;
    el.style.transform = `translateY(${ -center * speed }px)`;
  });
}
window.addEventListener('scroll', function() {
  if (!ticking) {
    window.requestAnimationFrame(function() {
      onScrollParallax();
      ticking = false;
    });
    ticking = true;
  }
}, { passive: true });
