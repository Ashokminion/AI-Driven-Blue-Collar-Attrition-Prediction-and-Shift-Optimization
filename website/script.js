// ========================================
// SHIFTSYNC AI - MODERN ANIMATION ENGINE
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    initCursor();
    initStarfield();
    initGSAP();
});

// 1. CUSTOM CURSOR ENGINE
function initCursor() {
    const dot = document.getElementById('cursor-dot');
    const glow = document.getElementById('cursor-glow');

    let mouseX = 0, mouseY = 0;
    let dotX = 0, dotY = 0;
    let glowX = 0, glowY = 0;

    window.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    function animate() {
        // Smooth lag effect
        dotX += (mouseX - dotX) * 0.2;
        dotY += (mouseY - dotY) * 0.2;
        glowX += (mouseX - glowX) * 0.1;
        glowY += (mouseY - glowY) * 0.1;

        dot.style.left = `${dotX}px`;
        dot.style.top = `${dotY}px`;
        glow.style.left = `${glowX}px`;
        glow.style.top = `${glowY}px`;

        requestAnimationFrame(animate);
    }
    animate();

    // Hover Interaction
    document.querySelectorAll('a, button, .p-card, .f-card, .arch-node').forEach(el => {
        el.addEventListener('mouseenter', () => {
            gsap.to(dot, { scale: 4, duration: 0.3 });
            gsap.to(glow, { scale: 1.5, opacity: 0.6, duration: 0.3 });
        });
        el.addEventListener('mouseleave', () => {
            gsap.to(dot, { scale: 1, duration: 0.3 });
            gsap.to(glow, { scale: 1, opacity: 0.4, duration: 0.3 });
        });
    });
}

// 2. SUBTLE STARFIELD
function initStarfield() {
    const canvas = document.getElementById('star-canvas');
    const ctx = canvas.getContext('2d');
    let stars = [];

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        stars = [];
        for (let i = 0; i < 200; i++) {
            stars.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                size: Math.random() * 1.5,
                opacity: Math.random(),
                speed: Math.random() * 0.005
            });
        }
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        stars.forEach(star => {
            ctx.fillStyle = `rgba(14, 165, 233, ${star.opacity})`;
            ctx.beginPath();
            ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
            ctx.fill();
            star.opacity += star.speed;
            if (star.opacity > 1 || star.opacity < 0) star.speed *= -1;
        });
        requestAnimationFrame(draw);
    }

    window.addEventListener('resize', resize);
    resize();
    draw();
}

// 3. GSAP ANIMATIONS
function initGSAP() {
    gsap.registerPlugin(ScrollTrigger);

    // Hero Reveal
    const heroTl = gsap.timeline();
    heroTl.from(".hero-title", { y: 100, opacity: 0, duration: 1.2, ease: "power4.out" })
        .from(".wave-line", { scaleX: 0, duration: 0.8, ease: "power2.inOut" }, "-=0.8")
        .from(".hero-subtitle", { y: 30, opacity: 0, duration: 1 }, "-=0.6")
        .from(".hero-btns", { y: 30, opacity: 0, duration: 0.8 }, "-=0.6");

    // Stats Counter
    gsap.from(".stat-value", {
        scrollTrigger: {
            trigger: ".stats",
            start: "top 80%",
        },
        innerHTML: 0,
        duration: 2,
        snap: { innerHTML: 1 },
        stagger: 0.2,
        onUpdate: function () {
            this.targets().forEach(t => {
                const suffix = t.dataset.suffix || "";
                t.innerHTML = Math.ceil(t.innerHTML) + suffix;
            });
        }
    });

    // Reveal Sections
    document.querySelectorAll('section > .section-container, .p-card, .f-card, .arch-node').forEach(el => {
        gsap.from(el, {
            scrollTrigger: {
                trigger: el,
                start: "top 85%",
                toggleActions: "play none none none"
            },
            y: 50,
            opacity: 0,
            duration: 1,
            ease: "power2.out"
        });
    });

    // Architecture Lines
    gsap.from(".arch-line", {
        scrollTrigger: {
            trigger: ".arch-flow",
            start: "top 70%"
        },
        scaleX: 0,
        transformOrigin: "left",
        duration: 1.5,
        ease: "power2.inOut",
        stagger: 0.3
    });
}

// Navbar Scroll Effect
window.addEventListener('scroll', () => {
    const nav = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        nav.style.padding = "15px 50px";
        nav.style.background = "rgba(15, 23, 42, 0.9)";
    } else {
        nav.style.padding = "25px 50px";
        nav.style.background = "transparent";
    }
});
