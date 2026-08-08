document.addEventListener('DOMContentLoaded', function () {
  var items = Array.prototype.slice.call(document.querySelectorAll('.nav-item.has-children'));
  if (!items.length) return;

  function closeAll() {
    items.forEach(function (item) {
      item.classList.remove('is-open');
      item.querySelector('a').setAttribute('aria-expanded', 'false');
    });
  }

  items.forEach(function (item) {
    var trigger = item.querySelector('a');
    trigger.addEventListener('click', function (event) {
      event.preventDefault();
      var wasOpen = item.classList.contains('is-open');
      closeAll();
      if (!wasOpen) {
        item.classList.add('is-open');
        trigger.setAttribute('aria-expanded', 'true');
      }
    });
  });

  document.addEventListener('click', function (event) {
    var clickedInsideMenu = items.some(function (item) { return item.contains(event.target); });
    if (!clickedInsideMenu) closeAll();
  });

  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') closeAll();
  });
});
