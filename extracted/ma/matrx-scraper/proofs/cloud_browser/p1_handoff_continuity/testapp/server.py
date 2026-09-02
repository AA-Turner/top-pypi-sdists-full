"""Synthetic provider for Phase-0 proof P1.

NOT shipped code. This is a stand-in for a real site so that no proof ever touches a
third-party provider or a real account (PLAN.md forbids probing real providers).

Routes
------
GET  /                 index with links to every other route
GET  /state            sets a cookie + a localStorage value on load, shows both
GET  /login            login form; see "input provenance" below
POST /login            accepts the form, decides authenticated vs denied
GET  /auth             current auth state, read from the session cookie
GET  /popup            page with a target=_blank link and a window.open button
GET  /opened           the page a popup/new tab lands on
GET  /_reset           clears server-side session state (test convenience)

Input provenance — read this before trusting the login result
-------------------------------------------------------------
The login page counts, in the browser, the raw input events it receives before submit:

  * `keys`      keydown events on the credential fields
  * `gaps`      distinct inter-keystroke delays (ms, bucketed)
  * `moves`     mousemove events observed anywhere on the page
  * `path`      number of *distinct* pointer positions seen before the submit click

It refuses the login unless all four clear a floor. This distinguishes
`page.fill()` + `page.click()` (which sets a value with zero keydowns and clicks with a
single instantaneous pointer jump) from input injected at the X display via XTEST
(which produces a genuine key/pointer event stream inside the browser).

It is NOT a bot detector and must never be described as one. Playwright can defeat it
trivially with `keyboard.type(delay=...)` and stepped `mouse.move()`. Its only job in
this proof is to be a login that *cannot* be completed by the naive automated path, so
that "the human did this, not the agent" is an observable fact rather than an assertion.
"""

from __future__ import annotations

import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

# ---------------------------------------------------------------- server state

_LOCK = threading.Lock()
STATE: dict[str, object] = {
    "authenticated": False,
    "user": None,
    "last_attempt": None,  # dict: accepted + provenance counters + reason
    "attempts": [],
}

# Provenance floors. Chosen so page.fill()+page.click() cannot clear them and a
# human-paced xdotool sequence clears them comfortably.
MIN_KEYS = 8
MIN_GAPS = 2
MIN_MOVES = 5
MIN_PATH = 4

VALID_USER = "proof-user"
VALID_PASS = "proof-pass"

_STYLE = """
<style>
 body{font:15px/1.5 system-ui,sans-serif;margin:2rem;max-width:44rem}
 code,pre{background:#eee;padding:.15rem .35rem;border-radius:3px}
 .ok{color:#0a0;font-weight:700}.no{color:#c00;font-weight:700}
 input{font-size:16px;padding:.4rem;width:16rem;display:block;margin:.4rem 0}
 button{font-size:16px;padding:.5rem 1rem}
 a{display:inline-block;margin-right:1rem}
</style>
"""

INDEX = f"""<!doctype html><meta charset=utf-8><title>P1 synthetic provider</title>{_STYLE}
<h1>P1 synthetic provider</h1>
<p>Stand-in site for proof P1. No external network is used.</p>
<ul>
<li><a href="/state">/state</a> — sets cookie + localStorage</li>
<li><a href="/login">/login</a> — provenance-gated login form</li>
<li><a href="/auth">/auth</a> — current auth state</li>
<li><a href="/popup">/popup</a> — opens a new tab</li>
</ul>
"""

STATE_PAGE = f"""<!doctype html><meta charset=utf-8><title>state</title>{_STYLE}
<h1>state page</h1>
<p id=cookie></p><p id=ls></p>
<button id=writels>write localStorage marker</button>
<script>
document.cookie = "p1_visit=1; path=/; SameSite=Lax";
if(!localStorage.getItem("p1_agent_marker"))
  localStorage.setItem("p1_agent_marker","set-on-first-load");
document.getElementById("cookie").textContent = "document.cookie = " + document.cookie;
document.getElementById("ls").textContent =
  "localStorage.p1_agent_marker = " + localStorage.getItem("p1_agent_marker");
document.getElementById("writels").onclick = function(){{
  localStorage.setItem("p1_human_marker","written-by-display-input-"+Date.now());
  document.getElementById("ls").textContent =
    "localStorage.p1_human_marker = " + localStorage.getItem("p1_human_marker");
}};
</script>
"""

LOGIN_PAGE = f"""<!doctype html><meta charset=utf-8><title>login</title>{_STYLE}
<h1>login</h1>
<p>Credentials for this synthetic provider: <code>{VALID_USER}</code> /
<code>{VALID_PASS}</code></p>
<form method=POST action=/login id=f>
  <input name=username id=username placeholder=username autocomplete=off>
  <input name=password id=password placeholder=password type=password autocomplete=off>
  <input type=hidden name=provenance id=provenance>
  <button type=submit id=submit>Sign in</button>
</form>
<p id=live></p>
<script>
var keys=0, gaps={{}}, moves=0, seen={{}}, last=null;
function bump(e){{
  keys++;
  var now = performance.now();
  if(last!==null){{ var b = Math.round((now-last)/25); gaps[b]=1; }}
  last = now;
}}
document.getElementById("username").addEventListener("keydown", bump);
document.getElementById("password").addEventListener("keydown", bump);
document.addEventListener("mousemove", function(e){{
  moves++; seen[e.clientX+","+e.clientY]=1;
}});
setInterval(function(){{
  document.getElementById("live").textContent =
    "keys="+keys+" gaps="+Object.keys(gaps).length+
    " moves="+moves+" path="+Object.keys(seen).length;
}}, 200);
document.getElementById("f").addEventListener("submit", function(){{
  document.getElementById("provenance").value = JSON.stringify({{
    keys: keys, gaps: Object.keys(gaps).length,
    moves: moves, path: Object.keys(seen).length
  }});
}});
</script>
"""

POPUP_PAGE = f"""<!doctype html><meta charset=utf-8><title>popup launcher</title>{_STYLE}
<h1>popup launcher</h1>
<p><a id=newtab href="/opened?via=target_blank" target="_blank"
      style="font-size:22px;padding:1rem;border:2px solid #333">OPEN IN NEW TAB</a></p>
<button id=win style="margin-top:1rem">window.open()</button>
<script>
document.getElementById("win").onclick=function(){{
  window.open("/opened?via=window_open","_blank");
}};
</script>
"""

OPENED_PAGE = f"""<!doctype html><meta charset=utf-8><title>opened-tab</title>{_STYLE}
<h1 id=h>opened tab</h1>
<p id=via></p>
<script>
var q = new URLSearchParams(location.search);
document.getElementById("via").textContent = "opened via: " + (q.get("via")||"unknown");
localStorage.setItem("p1_opened_tab","yes");
window.__p1_opened_tab_marker = "drivable";
</script>
"""


def _auth_page() -> str:
    with _LOCK:
        authed = bool(STATE["authenticated"])
        user = STATE["user"]
        last = STATE["last_attempt"]
    badge = (
        f"<p class=ok id=status>AUTHENTICATED as {user}</p>"
        if authed
        else "<p class=no id=status>NOT AUTHENTICATED</p>"
    )
    return (
        f"<!doctype html><meta charset=utf-8><title>auth</title>{_STYLE}"
        f"<h1>auth state</h1>{badge}"
        f"<pre id=last>{json.dumps(last, indent=2)}</pre>"
    )


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):  # keep the harness log readable
        pass

    def _send(self, body: str, code: int = 200, cookies: list[str] | None = None):
        raw = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        for c in cookies or []:
            self.send_header("Set-Cookie", c)
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            self._send(INDEX)
        elif path == "/state":
            self._send(STATE_PAGE, cookies=["p1_server_cookie=from-server; Path=/"])
        elif path == "/login":
            self._send(LOGIN_PAGE)
        elif path == "/auth":
            self._send(_auth_page())
        elif path == "/popup":
            self._send(POPUP_PAGE)
        elif path == "/opened":
            self._send(OPENED_PAGE)
        elif path == "/_state.json":
            with _LOCK:
                body = json.dumps(STATE)
            raw = body.encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
        elif path == "/_reset":
            with _LOCK:
                STATE.update(authenticated=False, user=None, last_attempt=None)
                STATE["attempts"] = []
            self._send("<p>reset</p>")
        else:
            self._send("<h1>404</h1>", 404)

    def do_POST(self):
        if urlparse(self.path).path != "/login":
            self._send("<h1>404</h1>", 404)
            return
        n = int(self.headers.get("Content-Length", 0))
        form = parse_qs(self.rfile.read(n).decode())
        user = (form.get("username") or [""])[0]
        pwd = (form.get("password") or [""])[0]
        try:
            prov = json.loads((form.get("provenance") or ["{}"])[0] or "{}")
        except json.JSONDecodeError:
            prov = {}

        counters = {k: int(prov.get(k, 0) or 0) for k in ("keys", "gaps", "moves", "path")}
        creds_ok = user == VALID_USER and pwd == VALID_PASS
        prov_ok = (
            counters["keys"] >= MIN_KEYS
            and counters["gaps"] >= MIN_GAPS
            and counters["moves"] >= MIN_MOVES
            and counters["path"] >= MIN_PATH
        )
        if not creds_ok:
            reason = "bad_credentials"
        elif not prov_ok:
            reason = "insufficient_input_provenance"
        else:
            reason = "accepted"

        record = {
            "accepted": creds_ok and prov_ok,
            "reason": reason,
            "provenance": counters,
            "floors": {
                "keys": MIN_KEYS,
                "gaps": MIN_GAPS,
                "moves": MIN_MOVES,
                "path": MIN_PATH,
            },
        }
        with _LOCK:
            STATE["last_attempt"] = record
            STATE["attempts"].append(record)  # type: ignore[union-attr]
            if record["accepted"]:
                STATE["authenticated"] = True
                STATE["user"] = user

        cookies = (
            [f"p1_session=session-for-{user}; Path=/; SameSite=Lax"] if record["accepted"] else []
        )
        self._send(_auth_page(), cookies=cookies)


def main() -> None:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8901
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"P1 synthetic provider on http://127.0.0.1:{port}", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
