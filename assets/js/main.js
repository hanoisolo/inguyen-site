// Progressive enhancement only — the page is fully usable without this file.

(function () {
  'use strict';

  var header = document.querySelector('.site-header');

  function updateHeaderState() {
    if (header) {
      header.classList.toggle('is-scrolled', window.scrollY > 8);
    }
  }

  window.addEventListener('scroll', updateHeaderState, { passive: true });
  updateHeaderState();

  var yearEl = document.querySelector('[data-year]');
  if (yearEl) {
    yearEl.textContent = String(new Date().getFullYear());
  }

  var reduceMotionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (reduceMotionQuery.matches) {
    document.documentElement.classList.add('reduce-motion');
  }
})();
