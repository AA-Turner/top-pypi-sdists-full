/* GhostPC — Shared JS utilities */

/**
 * WebSocket wrapper with auto-reconnect.
 * Mirrors the existing viewer chat pattern from mjpeg_server.py.
 */
class GhostWS {
  constructor(url, { onMessage, onOpen, onClose, reconnectMs = 3000 } = {}) {
    this.url = url;
    this.onMessage = onMessage || (() => {});
    this.onOpen = onOpen || (() => {});
    this.onClose = onClose || (() => {});
    this.reconnectMs = reconnectMs;
    this._ws = null;
    this._closed = false;
    this.connect();
  }

  connect() {
    if (this._closed) return;
    this._ws = new WebSocket(this.url);

    this._ws.onopen = () => this.onOpen();

    this._ws.onmessage = (ev) => {
      try {
        const data = JSON.parse(ev.data);
        this.onMessage(data);
      } catch {
        this.onMessage(ev.data);
      }
    };

    this._ws.onclose = () => {
      this.onClose();
      if (!this._closed) {
        setTimeout(() => this.connect(), this.reconnectMs);
      }
    };

    this._ws.onerror = () => {};
  }

  send(data) {
    if (this._ws && this._ws.readyState === WebSocket.OPEN) {
      this._ws.send(typeof data === 'string' ? data : JSON.stringify(data));
    }
  }

  close() {
    this._closed = true;
    if (this._ws) this._ws.close();
  }

  get connected() {
    return this._ws && this._ws.readyState === WebSocket.OPEN;
  }
}

/**
 * Fetch wrapper with JSON handling and error toasts.
 */
async function api(url, opts = {}) {
  const defaults = {
    headers: { 'Content-Type': 'application/json' },
  };
  if (opts.body && typeof opts.body === 'object') {
    opts.body = JSON.stringify(opts.body);
  }
  const merged = { ...defaults, ...opts, headers: { ...defaults.headers, ...(opts.headers || {}) } };

  try {
    const res = await fetch(url, merged);
    const text = await res.text();
    let json;
    try { json = JSON.parse(text); } catch { json = null; }

    if (!res.ok) {
      const msg = (json && json.error) || text || `HTTP ${res.status}`;
      toast(msg, 'error');
      return { ok: false, status: res.status, error: msg, data: json };
    }
    return { ok: true, status: res.status, data: json || text };
  } catch (err) {
    toast(`Network error: ${err.message}`, 'error');
    return { ok: false, status: 0, error: err.message, data: null };
  }
}

/**
 * Toast notification system.
 */
let _toastContainer = null;

function _ensureToastContainer() {
  if (_toastContainer) return _toastContainer;
  _toastContainer = document.createElement('div');
  _toastContainer.className = 'toast-container';
  document.body.appendChild(_toastContainer);
  return _toastContainer;
}

function toast(message, level = 'info', durationMs = 4000) {
  const container = _ensureToastContainer();
  const el = document.createElement('div');
  el.className = `toast ${level}`;
  el.textContent = message;
  container.appendChild(el);

  if (durationMs > 0) {
    setTimeout(() => {
      el.classList.add('removing');
      el.addEventListener('animationend', () => el.remove());
    }, durationMs);
  }
  return el;
}
