document.addEventListener('DOMContentLoaded', function () {
  var carousel = document.querySelector('.home-carousel');
  if (!carousel) return;

  var slides = Array.prototype.slice.call(carousel.querySelectorAll('.home-hero'));
  var dots = Array.prototype.slice.call(carousel.querySelectorAll('[data-carousel-dot]'));
  var activeIndex = 0;
  var intervalId;

  function showSlide(index) {
    activeIndex = (index + slides.length) % slides.length;
    slides.forEach(function (slide, slideIndex) {
      var isActive = slideIndex === activeIndex;
      slide.classList.toggle('is-active', isActive);
      slide.setAttribute('aria-hidden', String(!isActive));
    });
    dots.forEach(function (dot, dotIndex) {
      var isActive = dotIndex === activeIndex;
      dot.classList.toggle('is-active', isActive);
      dot.setAttribute('aria-selected', String(isActive));
    });
  }

  function restartAutoplay() {
    window.clearInterval(intervalId);
    intervalId = window.setInterval(function () { showSlide(activeIndex + 1); }, 7000);
  }

  carousel.querySelector('[data-carousel-prev]').addEventListener('click', function () {
    showSlide(activeIndex - 1);
    restartAutoplay();
  });
  carousel.querySelector('[data-carousel-next]').addEventListener('click', function () {
    showSlide(activeIndex + 1);
    restartAutoplay();
  });
  dots.forEach(function (dot) {
    dot.addEventListener('click', function () {
      showSlide(Number(dot.getAttribute('data-carousel-dot')));
      restartAutoplay();
    });
  });

  slides.forEach(function (slide) {
    slide.addEventListener('click', function (event) {
      if (event.target.closest('a, button')) return;
      var url = slide.getAttribute('data-slide-url');
      if (!url) return;
      if (slide.getAttribute('data-slide-external') === 'true') {
        window.open(url, '_blank', 'noopener');
        return;
      }
      window.location.href = url;
    });
  });

  restartAutoplay();
});