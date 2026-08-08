document.addEventListener('DOMContentLoaded', function () {
  if (window.POPUP_COMUNICADOS_ENABLED === false) return;

  var popup = document.getElementById('popup-comunicado');
  if (!popup) return;

  var comunicadoId = popup.getAttribute('data-comunicado-id');
  var skipKey = 'inba-ocultar-popup-en-comunicado';

  if (sessionStorage.getItem(skipKey) === comunicadoId && window.location.pathname.endsWith(comunicadoId)) {
    sessionStorage.removeItem(skipKey);
    return;
  }

  function closePopup() {
    popup.hidden = true;
    document.body.classList.remove('popup-open');
  }

  popup.hidden = false;
  document.body.classList.add('popup-open');

  popup.querySelectorAll('[data-popup-close]').forEach(function (btn) {
    btn.addEventListener('click', closePopup);
  });
  popup.querySelectorAll('.popup-image-link').forEach(function (link) {
    link.addEventListener('click', closePopup);
  });
  popup.querySelectorAll('.popup-cta').forEach(function (link) {
    link.addEventListener('click', function () {
      sessionStorage.setItem(skipKey, comunicadoId);
      closePopup();
    });
  });
  popup.addEventListener('click', function (event) {
    if (event.target === popup) closePopup();
  });
  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && !popup.hidden) closePopup();
  });
});
