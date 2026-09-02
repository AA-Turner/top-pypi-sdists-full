"""P3 synthetic provider — a local-only stand-in for a real logged-in website.

PHASE-0 PROOF HARNESS. NOT SHIPPED CODE.

PLAN.md forbids using real providers for proofs. This app establishes exactly the
four kinds of browser state a Cloud Browser checkpoint must carry:

  1. an httpOnly session cookie  (server decides "authenticated")
  2. a localStorage value
  3. an IndexedDB record
  4. history (visiting pages)

It binds to 127.0.0.1 only and talks to nothing external.

The listen port is PINNED because localStorage/IndexedDB origins include the port;
a restore on a different port would look like a different site and the proof would
be meaningless (cookies would still match, since cookies ignore port — which is
itself worth knowing).
"""

from __future__ import annotations

import json
import secrets
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

PORT = 8731
SESSIONS: dict[str, str] = {}

PAGE = """<!doctype html>
<html><head><meta charset="utf-8"><title>P3 Synthetic Provider</title></head>
<body>
<h1>P3 Synthetic Provider</h1>
<div id="authstate">checking...</div>
<div id="lsstate">ls: ?</div>
<div id="idbstate">idb: ?</div>
<form method="POST" action="/api/login">
  <input name="user" value="p3-user" id="user">
  <button type="submit" id="loginbtn">Log in</button>
</form>
<script>
const DB_NAME = 'p3db', STORE = 'kv';

function openDb() {
  return new Promise((res, rej) => {
    const r = indexedDB.open(DB_NAME, 1);
    r.onupgradeneeded = () => r.result.createObjectStore(STORE, {keyPath: 'k'});
    r.onsuccess = () => res(r.result);
    r.onerror = () => rej(r.error);
  });
}
async function idbPut(k, v) {
  const db = await openDb();
  await new Promise((res, rej) => {
    const tx = db.transaction(STORE, 'readwrite');
    tx.objectStore(STORE).put({k, v});
    tx.oncomplete = res; tx.onerror = () => rej(tx.error);
  });
  db.close();
}
async function idbGet(k) {
  const db = await openDb();
  const out = await new Promise((res, rej) => {
    const tx = db.transaction(STORE, 'readonly');
    const rq = tx.objectStore(STORE).get(k);
    rq.onsuccess = () => res(rq.result ? rq.result.v : null);
    rq.onerror = () => rej(rq.error);
  });
  db.close();
  return out;
}
window.p3 = {idbPut, idbGet};

async function refresh() {
  const r = await fetch('/api/whoami', {credentials: 'same-origin'});
  const j = await r.json();
  document.getElementById('authstate').textContent =
    j.authenticated ? ('AUTHENTICATED as ' + j.user) : 'ANONYMOUS';
  document.getElementById('authstate').dataset.auth = j.authenticated ? '1' : '0';
  document.getElementById('lsstate').textContent =
    'ls: ' + (localStorage.getItem('p3_pref') || 'MISSING');
  let idbv = 'MISSING';
  try { idbv = (await idbGet('p3_record')) || 'MISSING'; } catch (e) { idbv = 'ERR:' + e; }
  document.getElementById('idbstate').textContent = 'idb: ' + idbv;
  document.getElementById('idbstate').dataset.v = idbv;
}
refresh();
</script>
</body></html>
"""


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *_args):  # keep the proof output clean
        pass

    def _cookies(self) -> dict[str, str]:
        raw = self.headers.get("Cookie", "")
        out = {}
        for part in raw.split(";"):
            if "=" in part:
                k, v = part.split("=", 1)
                out[k.strip()] = v.strip()
        return out

    def _send(self, code: int, body: bytes, ctype: str, extra: list[tuple[str, str]] = ()):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        for k, v in extra:
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/page2", "/page3"):
            self._send(200, PAGE.encode(), "text/html; charset=utf-8")
        elif path == "/api/whoami":
            tok = self._cookies().get("p3_session")
            user = SESSIONS.get(tok or "")
            body = json.dumps({"authenticated": bool(user), "user": user}).encode()
            self._send(200, body, "application/json")
        else:
            self._send(404, b"nope", "text/plain")

    def do_POST(self):
        if urlparse(self.path).path != "/api/login":
            self._send(404, b"nope", "text/plain")
            return
        n = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(n).decode()
        user = "p3-user"
        for part in raw.split("&"):
            if part.startswith("user="):
                user = part[5:] or user
        tok = secrets.token_urlsafe(24)
        SESSIONS[tok] = user
        # Max-Age set deliberately: a pure session cookie is never written to disk by
        # Chromium, so it could not survive a checkpoint. Real providers use
        # persistent cookies for "stay signed in", which is the case under test.
        cookie = f"p3_session={tok}; Path=/; Max-Age=86400; HttpOnly; SameSite=Lax"
        self._send(303, b"", "text/plain", [("Location", "/"), ("Set-Cookie", cookie)])


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"P3 synthetic provider on http://127.0.0.1:{port}", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
