(function () {
  var cards = document.querySelectorAll("[data-revista-pdf]");
  var iframe = document.getElementById("revista-iframe");
  var title = document.getElementById("revista-viewer-title");
  var openLink = document.getElementById("revista-open-link");
  var panel = document.getElementById("revista-viewer");
  if (!cards.length || !iframe || !title || !openLink) return;

  function activate(card) {
    cards.forEach(function (item) {
      var on = item === card;
      item.classList.toggle("is-active", on);
      item.setAttribute("aria-selected", on ? "true" : "false");
    });

    var pdf = card.getAttribute("data-revista-pdf");
    var label = card.getAttribute("data-revista-title") || "Ciencia INBA";
    iframe.src = pdf + "#toolbar=1&navpanes=0&view=FitH";
    iframe.setAttribute("title", "Visor de " + label);
    title.textContent = label;
    openLink.href = pdf;
    if (panel) panel.setAttribute("aria-labelledby", card.id);
  }

  cards.forEach(function (card) {
    card.addEventListener("click", function () {
      activate(card);
      if (panel) panel.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
})();
