
function loadES5() {
  var el = document.createElement('script');
  el.src = '/insteon_static/frontend_es5/entrypoint-3be169ad.js';
  document.body.appendChild(el);
}
if (/.*Version\/(?:11|12)(?:\.\d+)*.*Safari\//.test(navigator.userAgent)) {
    loadES5();
} else {
  try {
    new Function("import('/insteon_static/frontend_latest/entrypoint-6d69817a.js')")();
  } catch (err) {
    loadES5();
  }
}
  