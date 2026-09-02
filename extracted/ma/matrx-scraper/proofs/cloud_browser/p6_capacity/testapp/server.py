"""Synthetic site for the P6 capacity benchmark. Phase-0 proof harness (NOT shipped code).

Why a local synthetic site and not a real one: PLAN.md Phase 0 forbids probing real
providers, and a capacity benchmark whose page weight changes when someone else deploys
a site is not reproducible. Every byte served here is fixed by this file, so two hosts
measured a month apart are measured against the same work.

Routes
------
GET  /health          liveness for the harness
GET  /login           login form (synthetic; no real credentials anywhere)
POST /login           sets the session cookie -> the profile is now "authenticated"
GET  /idle            authenticated page that then does nothing (workload 1)
GET  /form            small form page; POST /form echoes a result (workload 2)
GET  /heavy           deliberately heavy modern-app page (workload 3)

Weight of /heavy is controlled by P6_HEAVY_ROWS (default 1500 DOM rows) plus a
requestAnimationFrame loop, a periodic re-render, and a web-worker-free JSON churn --
enough to make a Chromium renderer genuinely busy without needing the network.
"""

from __future__ import annotations

import argparse
import http.server
import json
import os
import socketserver
import threading
import time
from urllib.parse import parse_qs, urlparse

HEAVY_ROWS = int(os.environ.get("P6_HEAVY_ROWS", "1500"))
SESSION_COOKIE = "p6session"
SESSION_VALUE = "authenticated-synthetic"

_PAGE_HEAD = """<!doctype html><html><head><meta charset="utf-8">
<title>{title}</title><style>
body{{font:14px system-ui;margin:0;padding:12px;background:#111;color:#eee}}
.row{{display:flex;gap:8px;padding:2px 4px;border-bottom:1px solid #222}}
.cell{{flex:1;overflow:hidden;white-space:nowrap}}
#box{{width:120px;height:120px;background:linear-gradient(45deg,#3af,#f3a);border-radius:12px}}
</style></head><body>"""


def _page(title: str, body: str) -> bytes:
    return (_PAGE_HEAD.format(title=title) + body + "</body></html>").encode()


LOGIN_PAGE = _page(
    "p6 login",
    """<h1>Synthetic login</h1>
<form method="post" action="/login">
<input id="u" name="u" value=""><input id="p" name="p" type="password" value="">
<button id="submit" type="submit">Sign in</button></form>""",
)

IDLE_PAGE = _page(
    "p6 idle",
    """<h1 id="state">idle-authenticated</h1>
<p id="stamp"></p>
<script>
 localStorage.setItem('p6','authenticated');
 document.getElementById('stamp').textContent = new Date().toISOString();
</script>""",
)

FORM_PAGE = _page(
    "p6 form",
    """<h1>Form</h1>
<form method="post" action="/form">
<input id="name" name="name"><input id="qty" name="qty" value="1">
<button id="go" type="submit">Submit</button></form>""",
)

_HEAVY_BODY = """<h1>Heavy app</h1><div id="box"></div>
<button id="churn">churn</button><span id="count">0</span>
<div id="grid"></div>
<script>
const ROWS = __P6_ROWS__;
const grid = document.getElementById('grid');
function render(seed) {
  const frag = document.createDocumentFragment();
  for (let i = 0; i < ROWS; i++) {
    const row = document.createElement('div'); row.className = 'row';
    for (let c = 0; c < 4; c++) {
      const cell = document.createElement('div'); cell.className = 'cell';
      cell.textContent = 'r' + i + 'c' + c + ':' + ((i * 31 + c * 7 + seed) % 9973);
      row.appendChild(cell);
    }
    frag.appendChild(row);
  }
  grid.replaceChildren(frag);
}
render(0);
let n = 0, deg = 0;
const box = document.getElementById('box');
function frame() { deg = (deg + 3) % 360; box.style.transform = 'rotate(' + deg + 'deg)';
  requestAnimationFrame(frame); }
requestAnimationFrame(frame);
setInterval(function () { render(++n); }, 1000);
document.getElementById('churn').addEventListener('click', function () {
  const t0 = performance.now();
  let acc = 0;
  const data = [];
  for (let i = 0; i < 20000; i++) data.push({ i: i, s: 'x' + i, v: Math.sin(i) });
  for (const d of data) acc += d.v;
  JSON.parse(JSON.stringify(data.slice(0, 4000)));
  render(++n);
  document.getElementById('count').textContent = String(Math.round(performance.now() - t0));
  window.__p6_last_churn = acc;
});
</script>"""

HEAVY_PAGE = _page("p6 heavy", _HEAVY_BODY.replace("__P6_ROWS__", str(HEAVY_ROWS)))


class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):  # silence: the harness owns stdout
        return

    def _send(
        self,
        body: bytes,
        status: int = 200,
        cookie: str | None = None,
        content_type: str = "text/html; charset=utf-8",
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802
        path = urlparse(self.path).path
        if path == "/health":
            self._send(
                json.dumps({"ok": True, "t": time.time()}).encode(), content_type="application/json"
            )
        elif path == "/login":
            self._send(LOGIN_PAGE)
        elif path == "/idle":
            self._send(IDLE_PAGE)
        elif path == "/form":
            self._send(FORM_PAGE)
        elif path == "/heavy":
            self._send(HEAVY_PAGE)
        else:
            self._send(_page("p6", '<a href="/idle">idle</a> <a href="/heavy">heavy</a>'), 404)

    def do_POST(self):  # noqa: N802
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length).decode() if length else ""
        fields = parse_qs(raw)
        if path == "/login":
            cookie = f"{SESSION_COOKIE}={SESSION_VALUE}; Path=/; SameSite=Lax"
            self._send(_page("p6 auth", '<h1 id="state">authenticated</h1>'), cookie=cookie)
        elif path == "/form":
            name = (fields.get("name") or [""])[0]
            qty = (fields.get("qty") or ["0"])[0]
            self._send(_page("p6 result", f'<h1 id="result">ok:{name}:{qty}</h1>'))
        else:
            self._send(_page("p6", "no"), 404)


class Server(socketserver.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True


def serve(port: int) -> tuple[Server, threading.Thread]:
    httpd = Server(("127.0.0.1", port), Handler)
    thread = threading.Thread(target=httpd.serve_forever, name="p6-testapp", daemon=True)
    thread.start()
    return httpd, thread


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8642)
    args = ap.parse_args()
    srv, _ = serve(args.port)
    print(f"p6 testapp on http://127.0.0.1:{args.port} (heavy rows={HEAVY_ROWS})", flush=True)
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        srv.shutdown()
