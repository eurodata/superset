const observer = new MutationObserver(() => {
  const charts = document.querySelectorAll('[data-test-chart-id]');
  if (charts.length > 0) {
    charts.forEach(chart => {
      if (chart.querySelector('.info-icon')) return;

      const sliceId = chart.getAttribute('data-test-chart-id');
      const headerControls = chart.querySelector('.header-controls');

      const icon = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      icon.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
      icon.setAttribute('width', '24');
      icon.setAttribute('height', '24');
      icon.setAttribute('viewBox', '0 0 24 24');
      icon.classList.add('info-icon');
      icon.style.cursor = 'pointer';

      icon.innerHTML = `
        <path d="M13,16h2v2H9V16h2V12H10V10h3ZM12,8.25A1.25,1.25,0,1,0,10.75,7,
        1.25,1.25,0,0,0,12,8.25ZM22,12A10,10,0,1,1,12,2,10,10,0,0,1,22,12Zm-2,
        0a8,8,0,1,0-8,8A8.0091,8.0091,0,0,0,20,12Z"/>
      `;

      icon.addEventListener('click', () => {
        const link = `/explore/?slice_id=${sliceId}`;
        window.open(link, '_blank');
      });

      headerControls.appendChild(icon);
    });
  }
});

// Start observing
observer.observe(document.body, { childList: true, subtree: true });

