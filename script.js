function toggleMenu() {
  const menu = document.querySelector(".menu-links");
  const icon = document.querySelector(".hamburger-icon");
  menu.classList.toggle("open");
  icon.classList.toggle("open");
}

// Setup GSAP ScrollTrigger bidirectional animations
function getFrom(type, dir) {
  if (type.includes('left')) return { x: dir === 'down' ? -20 : 20, y: 0, opacity: 0 };
  if (type.includes('right')) return { x: dir === 'down' ? 20 : -20, y: 0, opacity: 0 };
  if (type.includes('zoom')) return { scale: 0.96, opacity: 0 };
  return { y: dir === 'down' ? 20 : -20, x: 0, opacity: 0 };
}
function getOut(type, dir) {
  if (type.includes('left')) return { x: dir === 'down' ? -20 : 20, opacity: 0 };
  if (type.includes('right')) return { x: dir === 'down' ? 20 : -20, opacity: 0 };
  if (type.includes('zoom')) return { scale: 0.98, opacity: 0 };
  return { y: dir === 'down' ? -20 : 20, opacity: 0 };
}

function setupScrollAnimations() {
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const elems = document.querySelectorAll('[data-aos]');

  if (prefersReduced || typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') {
    elems.forEach(el => { el.style.opacity = 1; el.style.transform = 'none'; });
    return;
  }

  gsap.registerPlugin(ScrollTrigger);

  elems.forEach(el => {
    const type = (el.dataset.aos || 'fade-up').toLowerCase();
    const delay = Number(el.dataset.aosDelay || el.dataset.aosDelay) || 0;

    // start hidden
    gsap.set(el, { opacity: 0, force3D: true });

    const enterAnim = (dir) => {
      gsap.killTweensOf(el);
      const from = getFrom(type, dir);
      gsap.fromTo(el, from, { x: 0, y: 0, scale: 1, opacity: 1, duration: 0.7, ease: 'power3.out', delay: delay / 1000, overwrite: true });
    };

    const leaveAnim = (dir) => {
      gsap.killTweensOf(el);
      const out = getOut(type, dir);
      gsap.to(el, { ...out, duration: 0.5, ease: 'power3.in', overwrite: true });
    };

    ScrollTrigger.create({
      trigger: el,
      start: 'top 85%',
      end: 'bottom 15%',
      onEnter: () => enterAnim('down'),
      onEnterBack: () => enterAnim('up'),
      onLeave: () => leaveAnim('down'),
      onLeaveBack: () => leaveAnim('up'),
    });

    // If element is already visible on load, play entrance animation
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight && rect.bottom > 0) {
      enterAnim('down');
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  setupScrollAnimations();
  updateProgress();
  onScrollParallax();
  setupScrollspy();
  setupProjectSlider();
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

// Scrollspy for navigation
function setupScrollspy() {
    const sections = document.querySelectorAll("section[id]");
    const navLinks = document.querySelectorAll("#desktop-nav .nav-button, #hamburger-nav .nav-button");

    if (!sections.length || !navLinks.length) return;

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute("id");
                navLinks.forEach(link => {
                    link.classList.remove("active");
                });
                const activeLinks = document.querySelectorAll(`a.nav-button[href="#${id}"]`);
                activeLinks.forEach(link => link.classList.add('active'));
            }
        });
    }, { rootMargin: "-30% 0px -70% 0px" });

    sections.forEach(section => {
        observer.observe(section);
    });
}

window.addEventListener('load', () => {
  if (window.location.hash) {
    const element = document.querySelector(window.location.hash);
    if (element) {
      // The timeout gives the browser a moment to finish layout
      setTimeout(() => {
        element.scrollIntoView({ behavior: 'smooth' });
      }, 100); 
    }
  }
});

// Project Slider Logic (Manual Wheel + Infinite Loop)
function setupProjectSlider() {
  const sliders = document.querySelectorAll('.project-slider-container');
  
  if (sliders.length === 0) return;

  sliders.forEach(slider => {
    let isHovered = false;
    const scrollSpeed = 1; // Auto-scroll speed

    // 1. Handle Mouse Wheel -> Horizontal Scroll
    slider.addEventListener('wheel', (e) => {
      e.preventDefault(); // Stop page scroll
      slider.scrollLeft += e.deltaY; // Scroll horizontally
      checkInfiniteLoop(); // Check bounds immediately for smooth feel
    }, { passive: false });

    // 2. Pause auto-scroll on hover
    slider.addEventListener('mouseenter', () => isHovered = true);
    slider.addEventListener('mouseleave', () => isHovered = false);

    // 3. Infinite Loop & Auto-scroll
    function loop() {
      if (!isHovered) {
        slider.scrollLeft += scrollSpeed;
      }
      checkInfiniteLoop();
      requestAnimationFrame(loop);
    }

    function checkInfiniteLoop() {
      // We have 2 identical sets of projects.
      // When we scroll past the first set (half width), reset to 0.
      const maxScroll = slider.scrollWidth / 2;
      
      if (slider.scrollLeft >= maxScroll) {
        slider.scrollLeft -= maxScroll;
      } else if (slider.scrollLeft <= 0) {
        slider.scrollLeft += maxScroll;
      }
    }

    // Start the loop
    requestAnimationFrame(loop);
  });
}
