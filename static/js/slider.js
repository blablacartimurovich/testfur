document.addEventListener('DOMContentLoaded', function () {
    const slider = document.getElementById('heroSlider');
    if (!slider) return;

    const slides = slider.querySelectorAll('.slide');
    const prevBtn = document.getElementById('prevSlide');
    const nextBtn = document.getElementById('nextSlide');
    const dotsContainer = document.getElementById('sliderDots');

    let currentIndex = 0;
    let interval;

    function createDots() {
        slides.forEach((_, index) => {
            const dot = document.createElement('button');
            dot.classList.add('dot');
            if (index === 0) dot.classList.add('active');

            dot.addEventListener('click', () => {
                goToSlide(index);
                resetAutoplay();
            });

            dotsContainer.appendChild(dot);
        });
    }

    function updateSlider() {
        slides.forEach((slide, index) => {
            slide.classList.toggle('active', index === currentIndex);
        });

        const dots = dotsContainer.querySelectorAll('.dot');
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === currentIndex);
        });
    }

    function goToSlide(index) {
        currentIndex = index;
        if (currentIndex < 0) currentIndex = slides.length - 1;
        if (currentIndex >= slides.length) currentIndex = 0;
        updateSlider();
    }

    function nextSlide() {
        goToSlide(currentIndex + 1);
    }

    function prevSlideFunc() {
        goToSlide(currentIndex - 1);
    }

    function startAutoplay() {
        interval = setInterval(nextSlide, 5000);
    }

    function resetAutoplay() {
        clearInterval(interval);
        startAutoplay();
    }

    nextBtn.addEventListener('click', () => {
        nextSlide();
        resetAutoplay();
    });

    prevBtn.addEventListener('click', () => {
        prevSlideFunc();
        resetAutoplay();
    });

    createDots();
    updateSlider();
    startAutoplay();
});