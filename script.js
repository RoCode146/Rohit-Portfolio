// 🔁 Scroll Reveal for .reveal elements
window.addEventListener('scroll', () => {
    const reveals = document.querySelectorAll('.reveal');
    for (let i = 0; i < reveals.length; i++) {
      const windowHeight = window.innerHeight;
      const revealTop = reveals[i].getBoundingClientRect().top;
      const revealPoint = 100;
  
      if (revealTop < windowHeight - revealPoint) {
        reveals[i].classList.add('active');
      }
    }
  });
  
  // ✍️ Typewriter Effect for Hero Title
  const heroTitle = document.querySelector('.hero h1');
  if (heroTitle) {
    const text = heroTitle.textContent;
    heroTitle.textContent = '';
    let i = 0;
    function typeWriter() {
      if (i < text.length) {
        heroTitle.textContent += text.charAt(i);
        i++;
        setTimeout(typeWriter, 50);
      }
    }
    setTimeout(typeWriter, 500);
  }
  
  // 🧭 Active Nav Link on Scroll
  const sections = document.querySelectorAll("section");
  const navLinks = document.querySelectorAll("nav ul li a");
  
  window.addEventListener("scroll", () => {
    let current = "";
    sections.forEach(section => {
      const sectionTop = section.offsetTop;
      if (scrollY >= sectionTop - 100) {
        current = section.getAttribute("id");
      }
    });
    navLinks.forEach(link => {
      link.classList.remove("active");
      if (link.getAttribute("href") === `#${current}`) {
        link.classList.add("active");
      }
    });
  });
  
  // 📊 Scroll Progress Bar
  const scrollBar = document.createElement('div');
  scrollBar.id = 'scroll-progress';
  scrollBar.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    height: 4px;
    background: #ffee58;
    width: 0;
    z-index: 9999;
  `;
  document.body.appendChild(scrollBar);
  
  window.addEventListener('scroll', () => {
    const totalHeight = document.body.scrollHeight - window.innerHeight;
    const progress = (window.scrollY / totalHeight) * 100;
    scrollBar.style.width = `${progress}%`;
  });
  
  // ⬆️ Back to Top Button
  const backToTop = document.createElement('div');
  backToTop.className = 'back-to-top';
  backToTop.innerHTML = '⬆️';
  document.body.appendChild(backToTop);
  
  backToTop.style.cssText = `
    position: fixed;
    bottom: 30px;
    right: 30px;
    background: #ffee58;
    padding: 10px 12px;
    border-radius: 50%;
    cursor: pointer;
    display: none;
    font-size: 1.2rem;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    z-index: 999;
  `;
  
  window.addEventListener('scroll', () => {
    backToTop.style.display = window.scrollY > 500 ? 'block' : 'none';
  });
  
  backToTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
  