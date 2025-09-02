
function loadES5() {
  var el = document.createElement('script');
  el.src = '/dynalite_static/frontend_es5/entrypoint-e859e4b8.js';
  document.body.appendChild(el);
}
if (/.*Version\/(?:11|12)(?:\.\d+)*.*Safari\//.test(navigator.userAgent)) {
    loadES5();
} else {
  try {
    new Function("import('/dynalite_static/frontend_latest/entrypoint-94572d1e.js')")();
  } catch (err) {
    loadES5();
  }
}
  