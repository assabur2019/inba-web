document.addEventListener('DOMContentLoaded', function () {
  var input = document.getElementById('news-search-input');
  var grid = document.getElementById('news-grid');
  if (!input || !grid) return;

  var cards = Array.prototype.slice.call(grid.querySelectorAll('.news-card'));
  var emptyMessage = document.getElementById('news-search-empty');

  function normalize(text) {
    return text.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  }

  input.addEventListener('input', function () {
    var query = normalize(input.value.trim().toLowerCase());
    var visibleCount = 0;

    cards.forEach(function (card) {
      var haystack = normalize(card.getAttribute('data-search-text'));
      var matches = haystack.indexOf(query) !== -1;
      card.hidden = !matches;
      if (matches) visibleCount += 1;
    });

    if (emptyMessage) emptyMessage.hidden = visibleCount !== 0;
  });
});
