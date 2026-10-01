
function loadES5() {
  var el = document.createElement('script');
  el.src = '/knx_static/frontend_es5/entrypoint.fa5c0f5a710836e1.js';
  document.body.appendChild(el);
}
if (/.*Version\/(?:11|12)(?:\.\d+)*.*Safari\//.test(navigator.userAgent)) {
    loadES5();
} else {
  try {
    new Function("import('/knx_static/frontend_latest/entrypoint.400dc91644cf14f4.js')")();
  } catch (err) {
    loadES5();
  }
}
  