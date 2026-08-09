(function () {
  const modal = document.getElementById('galleryModal');
  if (!modal) return;

  const backdrop = modal.querySelector('.gallery-backdrop');
  const panel = modal.querySelector('.gallery-panel');
  const mainImg = document.getElementById('galleryMainImg');
  const thumbsContainer = document.getElementById('galleryThumbs');
  const titleEl = document.getElementById('galleryTitle');
  const descEl = document.getElementById('galleryDesc');
  const closeBtn = modal.querySelector('.gallery-close');
  const prevBtn = modal.querySelector('.gallery-nav.prev');
  const nextBtn = modal.querySelector('.gallery-nav.next');

  let currentImages = [];
  let currentIndex = 0;
  let currentTitle = '';
  let currentDesc = '';
  let isMobile = window.matchMedia('(max-width: 768px)').matches;

  // Update mobile detection on resize
  window.addEventListener('resize', () => {
    isMobile = window.matchMedia('(max-width: 768px)').matches;
  });

  function openGallery(thumbEl, images, title, desc) {
    currentImages = images;
    currentIndex = 0;
    currentTitle = title;
    currentDesc = desc;

    titleEl.textContent = title;
    descEl.textContent = desc;

    // Build thumbs
    thumbsContainer.innerHTML = '';
    images.forEach((src, i) => {
      const t = document.createElement('img');
      t.src = src;
      t.alt = '';
      t.className = 'gallery-thumb' + (i === 0 ? ' active' : '');
      t.addEventListener('click', () => {
        currentIndex = i;
        updateMain();
      });
      thumbsContainer.appendChild(t);
    });

    updateMain();

    // Show modal
    modal.hidden = false;
    document.body.classList.add('gallery-open');

    // Desktop: try simple scale-from-center feel (exact position zoom is complex; we use a polished fade+scale)
    if (!isMobile) {
      panel.classList.add('animate-in');
    } else {
      panel.classList.add('animate-in-mobile');
    }

    // Focus management
    closeBtn.focus();
  }

  function updateMain() {
    mainImg.src = currentImages[currentIndex];
    mainImg.alt = currentTitle;
    // Update active thumb
    thumbsContainer.querySelectorAll('.gallery-thumb').forEach((t, i) => {
      t.classList.toggle('active', i === currentIndex);
    });
  }

  function closeGallery() {
    panel.classList.remove('animate-in', 'animate-in-mobile');
    panel.classList.add('animate-out');

    setTimeout(() => {
      modal.hidden = true;
      document.body.classList.remove('gallery-open');
      panel.classList.remove('animate-out');
      currentImages = [];
    }, 250);
  }

  // Event: click on any project thumb
  document.querySelectorAll('.project-thumb').forEach(thumb => {
    thumb.addEventListener('click', () => {
      const images = JSON.parse(thumb.dataset.images || '[]');
      if (!images.length) return;

      const item = thumb.closest('.project-item');
      const title = item.querySelector('h3')?.textContent || '';
      const desc = item.querySelector('p')?.textContent || '';

      openGallery(thumb, images, title, desc);
    });
  });

  // Close actions
  closeBtn.addEventListener('click', closeGallery);
  backdrop.addEventListener('click', closeGallery);

  document.addEventListener('keydown', (e) => {
    if (modal.hidden) return;
    if (e.key === 'Escape') closeGallery();
    if (e.key === 'ArrowLeft') {
      currentIndex = (currentIndex - 1 + currentImages.length) % currentImages.length;
      updateMain();
    }
    if (e.key === 'ArrowRight') {
      currentIndex = (currentIndex + 1) % currentImages.length;
      updateMain();
    }
  });

  // Nav buttons
  prevBtn.addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + currentImages.length) % currentImages.length;
    updateMain();
  });
  nextBtn.addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % currentImages.length;
    updateMain();
  });

  // Simple swipe for mobile
  let touchStartX = 0;
  mainImg.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
  }, { passive: true });

  mainImg.addEventListener('touchend', (e) => {
    const diff = e.changedTouches[0].screenX - touchStartX;
    if (Math.abs(diff) > 50) {
      if (diff > 0) {
        currentIndex = (currentIndex - 1 + currentImages.length) % currentImages.length;
      } else {
        currentIndex = (currentIndex + 1) % currentImages.length;
      }
      updateMain();
    }
  }, { passive: true });
})();
