/* ==========================================================================
   EcoBuilders — shared site script
   Loaded by every page. Handles: theme toggle, mobile nav, phone reveal,
   and the project gallery.

   Note: the initial theme is set by a small inline script in <head> so the
   correct colours paint before first render. This file only handles the
   click-to-switch behaviour.
   ========================================================================== */
(function () {
  'use strict';

  var root = document.documentElement;

  /* ---------------------------------------------------------------- theme */
  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    try { localStorage.setItem('eb-theme', theme); } catch (e) {}

    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', theme === 'dark' ? '#121A16' : '#F4F6F4');

    document.querySelectorAll('.theme-toggle').forEach(function (btn) {
      btn.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
      btn.setAttribute('aria-pressed', theme === 'dark' ? 'true' : 'false');
    });
  }

  document.querySelectorAll('.theme-toggle').forEach(function (btn) {
    btn.addEventListener('click', function () {
      applyTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
    });
  });

  applyTheme(root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light');

  /* Follow the OS setting until the visitor makes their own choice. */
  var mq = window.matchMedia('(prefers-color-scheme: dark)');
  var onSchemeChange = function (e) {
    var stored = null;
    try { stored = localStorage.getItem('eb-theme'); } catch (err) {}
    if (!stored) root.setAttribute('data-theme', e.matches ? 'dark' : 'light');
  };
  if (mq.addEventListener) mq.addEventListener('change', onSchemeChange);
  else if (mq.addListener) mq.addListener(onSchemeChange);

  /* ------------------------------------------------------------ mobile nav */
  var navToggle = document.querySelector('.nav-toggle');
  var navLinks = document.querySelector('.nav-links');

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', function () {
      var isOpen = navLinks.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', String(isOpen));
      document.body.classList.toggle('menu-open', isOpen);
    });

    navLinks.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        navLinks.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
        document.body.classList.remove('menu-open');
      });
    });
  }

  /* ---------------------------------------------------------- phone reveal */
  document.querySelectorAll('.phone-reveal').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var link = document.createElement('a');
      link.href = 'tel:5625071350';
      link.textContent = '(562) 507-1350';
      link.className = 'phone-reveal revealed';
      btn.parentNode.replaceChild(link, btn);
    });
  });

  /* --------------------------------------------------------------- gallery */
  var modal = document.getElementById('galleryModal');
  if (!modal) return;

  var backdrop  = modal.querySelector('.gallery-backdrop');
  var panel     = modal.querySelector('.gallery-panel');
  var mainImg   = document.getElementById('galleryMainImg');
  var thumbsBox = document.getElementById('galleryThumbs');
  var titleEl   = document.getElementById('galleryTitle');
  var descEl    = document.getElementById('galleryDesc');
  var closeBtn  = modal.querySelector('.gallery-close');
  var prevBtn   = modal.querySelector('.gallery-nav.prev');
  var nextBtn   = modal.querySelector('.gallery-nav.next');

  var images = [];       // [{src, caption}]
  var index = 0;
  var lastFocus = null;
  var closeTimer = null;

  function normalise(raw) {
    return raw.map(function (item) {
      return typeof item === 'string' ? { src: item, caption: '' } : item;
    });
  }

  function render() {
    var item = images[index] || { src: '', caption: '' };
    mainImg.src = item.src;
    mainImg.alt = item.caption || titleEl.textContent || '';
    descEl.textContent = item.caption || descEl.dataset.fallback || '';

    thumbsBox.querySelectorAll('.gallery-thumb').forEach(function (t, i) {
      t.classList.toggle('active', i === index);
      if (i === index) t.setAttribute('aria-current', 'true');
      else t.removeAttribute('aria-current');
    });

    var multiple = images.length > 1;
    prevBtn.hidden = !multiple;
    nextBtn.hidden = !multiple;
    thumbsBox.hidden = !multiple;

    // preload neighbours so arrowing through feels instant
    [index + 1, index - 1].forEach(function (i) {
      var n = images[(i + images.length) % images.length];
      if (n) { var pre = new Image(); pre.src = n.src; }
    });
  }

  function step(delta) {
    if (!images.length) return;
    index = (index + delta + images.length) % images.length;
    render();
  }

  function open(trigger) {
    var raw;
    try { raw = JSON.parse(trigger.dataset.images || '[]'); }
    catch (e) { raw = []; }
    if (!raw.length) return;

    if (closeTimer) { clearTimeout(closeTimer); closeTimer = null; }

    lastFocus = trigger;
    images = normalise(raw);
    index = 0;

    var item = trigger.closest('.project-item');
    var title = trigger.dataset.title || (item && item.querySelector('h4') ? item.querySelector('h4').textContent : '');
    var desc  = trigger.dataset.specs || (item && item.querySelector('.specs') ? item.querySelector('.specs').textContent : '');

    titleEl.textContent = title;
    descEl.dataset.fallback = desc;
    descEl.textContent = desc;

    thumbsBox.innerHTML = '';
    images.forEach(function (img, i) {
      var t = document.createElement('img');
      t.src = img.src;
      t.alt = '';
      t.className = 'gallery-thumb' + (i === 0 ? ' active' : '');
      t.addEventListener('click', function () { index = i; render(); });
      thumbsBox.appendChild(t);
    });

    render();

    modal.hidden = false;
    document.body.classList.add('gallery-open');
    panel.classList.remove('animate-out');
    panel.classList.add(window.matchMedia('(max-width: 768px)').matches ? 'animate-in-mobile' : 'animate-in');
    closeBtn.focus();
  }

  function close() {
    panel.classList.remove('animate-in', 'animate-in-mobile');
    panel.classList.add('animate-out');

    closeTimer = setTimeout(function () {
      modal.hidden = true;
      document.body.classList.remove('gallery-open');
      panel.classList.remove('animate-out');
      mainImg.removeAttribute('src');
      images = [];
      closeTimer = null;
      if (lastFocus) { lastFocus.focus(); lastFocus = null; }
    }, 200);
  }

  document.querySelectorAll('.project-thumb').forEach(function (thumb) {
    thumb.addEventListener('click', function () { open(thumb); });
  });

  closeBtn.addEventListener('click', close);
  backdrop.addEventListener('click', close);
  prevBtn.addEventListener('click', function () { step(-1); });
  nextBtn.addEventListener('click', function () { step(1); });

  document.addEventListener('keydown', function (e) {
    if (modal.hidden) return;
    if (e.key === 'Escape')     { close(); }
    if (e.key === 'ArrowLeft')  { step(-1); }
    if (e.key === 'ArrowRight') { step(1); }
    if (e.key === 'Tab') {
      // keep focus inside the dialog
      var focusable = modal.querySelectorAll('button:not([hidden]), img.gallery-thumb');
      if (!focusable.length) return;
      var first = focusable[0], last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });

  var touchX = 0;
  mainImg.addEventListener('touchstart', function (e) {
    touchX = e.changedTouches[0].screenX;
  }, { passive: true });

  mainImg.addEventListener('touchend', function (e) {
    var diff = e.changedTouches[0].screenX - touchX;
    if (Math.abs(diff) > 50) step(diff > 0 ? -1 : 1);
  }, { passive: true });
})();
