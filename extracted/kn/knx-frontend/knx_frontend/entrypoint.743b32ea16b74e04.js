
function loadES5() {
  var el = document.createElement('script');
  el.src = '/knx_static/frontend_es5/entrypoint.32741f2ed4bd743d.js';
  document.body.appendChild(el);
}
if (/.*Version\/(?:11|12)(?:\.\d+)*.*Safari\//.test(navigator.userAgent)) {
    loadES5();
} else {
  try {
    new Function("import('/knx_static/frontend_latest/entrypoint.743b32ea16b74e04.js')")();
  } catch (err) {
    loadES5();
  }
}
  