document.addEventListener('DOMContentLoaded', function () {
  var hero = document.querySelector('.mo-hero');
  if (!hero) return;

  var slides = Array.prototype.slice.call(hero.querySelectorAll('.mo-slide'));
  var dots = Array.prototype.slice.call(hero.querySelectorAll('[data-mo-dot]'));
  var activeIndex = 0;

  function showSlide(index) {
    activeIndex = (index + slides.length) % slides.length;
    slides.forEach(function (slide, slideIndex) {
      slide.classList.toggle('is-active', slideIndex === activeIndex);
    });
    dots.forEach(function (dot, dotIndex) {
      dot.classList.toggle('is-active', dotIndex === activeIndex);
    });
  }

  hero.querySelector('[data-mo-prev]').addEventListener('click', function () { showSlide(activeIndex - 1); });
  hero.querySelector('[data-mo-next]').addEventListener('click', function () { showSlide(activeIndex + 1); });
  dots.forEach(function (dot) {
    dot.addEventListener('click', function () { showSlide(Number(dot.getAttribute('data-mo-dot'))); });
  });
});
