"""
`seq eval replay`'s page: the console's own replay player, served on this machine to the one browser its link was
opened in.

In one sentence: a server on 127.0.0.1, at a port the system picks → its link carries a token that works once: it
hands that browser a cookie and is spent, so the link seen again opens nothing → every request after it needs that
cookie and must name this host as 127.0.0.1 or localhost (a page elsewhere cannot reach it through a name of its own)
→ `/` is the page, a few lines that mount the console's player (player/, its files as the console's site serves
them), `/assets/` those files and nothing else, `/api/` what the player asks for - the report, the details, an
episode's replay, its scene, its recording - read by this process (sources.py), whose key never reaches the page.
"""
from __future__ import annotations

import hmac
import html
import json
import pathlib
import re
import secrets
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlencode, urlsplit

from seq._replay_player.sources import Missing
from sequence_ai.errors import SequencesError

HERE = pathlib.Path(__file__).resolve().parent
PLAYER = HERE / "player"
COOKIE = "seq_replay"
TYPES = {".js": "text/javascript; charset=utf-8", ".mjs": "text/javascript; charset=utf-8",
         ".css": "text/css; charset=utf-8", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".woff": "font/woff",
         ".png": "image/png", ".webp": "image/webp", ".jpg": "image/jpeg", ".json": "application/json"}

CSP = ("default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' blob: data:; "
       "media-src 'self' blob:; connect-src 'self' blob: data:; font-src 'self' data:; worker-src 'self' blob:; "
       "object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'")
SPENT = ("This link was opened already: it works once. Open http://127.0.0.1:{port}/ in the browser it was opened in, "
         "or run `seq eval replay` again for a new one.")
REFUSED = "Open the link `seq eval replay` printed: this page opens only in the browser that link was opened in."
API = [
    (re.compile(r"/api/report"), "report", "application/json"),
    (re.compile(r"/api/details"), "details", "application/json"),
    (re.compile(r"/api/cameras"), "cameras", "application/json"),
    (re.compile(r"/api/replays/(\d+)"), "replay", "application/octet-stream"),
    (re.compile(r"/api/scenes/([0-9a-f]{64})"), "scene", "model/gltf-binary"),
    (re.compile(r"/api/videos/(\d+)\.mp4"), "video", "video/mp4"),
    (re.compile(r"/api/episodes/(\d+)/record"), "record", "application/octet-stream"),
]


def manifest() -> dict:
    """The player's files as tools/replay_player.py copied them: {entry, styles, files: {path: sha256}}."""
    return json.loads((PLAYER / "MANIFEST.json").read_text())


class ReplayServer:
    """The page's server, bound to 127.0.0.1 at a port the system picks; `url` is its one-time link."""

    def __init__(self, source, *, title: str, name: str = "replay", episode: int | None = None) -> None:
        self.source = source
        self.title = title
        self.name = name
        self.episode = episode
        self.files = manifest()
        self._link = secrets.token_urlsafe(18)
        self._cookie = secrets.token_urlsafe(32)
        self._spent = False
        self._lock = threading.Lock()
        self._scenes: dict[str, bytes] = {}
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), type("Handler", (_Handler,), {"app": self}))
        self.httpd.daemon_threads = True
        self.port = self.httpd.server_address[1]

    @property
    def url(self) -> str:
        q = {"t": self._link, **({"ep": str(self.episode)} if self.episode is not None else {})}
        return f"http://127.0.0.1:{self.port}/?{urlencode(q)}"

    def spend(self, token: str) -> bool:
        """The link's token, taken once."""
        with self._lock:
            if self._spent or not hmac.compare_digest(token.encode(), self._link.encode()):
                return False
            self._spent = True
            return True

    def admits(self, cookie_header: str | None) -> bool:
        for part in (cookie_header or "").split(";"):
            k, _, v = part.strip().partition("=")
            if k == COOKIE and hmac.compare_digest(v.encode(), self._cookie.encode()):
                return True
        return False

    def page(self) -> bytes:
        styles = "\n".join(f'<link rel="stylesheet" href="{html.escape(s)}">' for s in self.files["styles"])
        text = (HERE / "page.html").read_text(encoding="utf-8")
        for k, v in (("{{title}}", html.escape(self.title)), ("{{styles}}", styles),
                     ("{{entry}}", html.escape(self.files["entry"])), ("{{name}}", html.escape(self.name))):
            text = text.replace(k, v)
        return text.encode("utf-8")

    def answer(self, kind: str, arg: str | None) -> bytes:
        if kind == "scene":
            with self._lock:
                hit = self._scenes.get(arg)
            if hit is None:
                hit = self.source.scene(arg)
                with self._lock:
                    self._scenes[arg] = hit
            return hit
        call = getattr(self.source, kind)
        return call(int(arg)) if arg is not None else call()

    def serve(self) -> None:
        self.httpd.serve_forever()

    def close(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()


class _Handler(BaseHTTPRequestHandler):
    app: ReplayServer
    server_version = "seq-replay"
    sys_version = ""

    def log_message(self, format, *args):
        pass

    def _send(self, status: int, body: bytes, ctype: str, *, cache: str = "no-store", extra: dict | None = None):
        self.send_response(status)
        for k, v in {"Content-Type": ctype, "Content-Length": str(len(body)), "Cache-Control": cache,
                     "X-Content-Type-Options": "nosniff", "Referrer-Policy": "no-referrer",
                     "Cross-Origin-Resource-Policy": "same-origin", **(extra or {})}.items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _text(self, status: int, text: str):
        self._send(status, text.encode("utf-8"), "text/plain; charset=utf-8")

    def _error(self, status: int, text: str):
        self._send(status, json.dumps({"error": text}).encode("utf-8"), "application/json")

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        app = self.app
        if (self.headers.get("Host") or "").lower() not in (f"127.0.0.1:{app.port}", f"localhost:{app.port}"):
            return self._text(403, "Not this host.")
        u = urlsplit(self.path)
        if u.path == "/" and "t" in parse_qs(u.query):
            q = parse_qs(u.query)
            if not app.spend(q["t"][0]):
                return self._text(403, SPENT.format(port=app.port))
            rest = {k: v[0] for k, v in q.items() if k != "t"}
            return self._send(303, b"", "text/plain", extra={
                "Location": "/" + (f"?{urlencode(rest)}" if rest else ""),
                "Set-Cookie": f"{COOKIE}={app._cookie}; HttpOnly; SameSite=Strict; Path=/"})
        if not app.admits(self.headers.get("Cookie")):
            return self._text(403, REFUSED)
        try:
            if u.path == "/":
                return self._send(200, app.page(), "text/html; charset=utf-8", extra={"Content-Security-Policy": CSP})
            if u.path == "/page.js":
                return self._send(200, (HERE / "page.js").read_bytes(), TYPES[".js"])
            if u.path in app.files["files"]:
                path = PLAYER / u.path.lstrip("/")
                ctype = TYPES.get(path.suffix, "application/octet-stream")
                return self._send(200, path.read_bytes(), ctype, cache="private, max-age=86400")
            for pattern, kind, ctype in API:
                m = pattern.fullmatch(u.path)
                if m:
                    return self._send(200, app.answer(kind, m.group(1) if m.groups() else None), ctype)
            return self._error(404, "not found")
        except Missing as exc:
            return self._error(404, str(exc))
        except SequencesError as exc:
            status = exc.status if exc.status in (400, 401, 403, 404, 409, 410, 429) else 502
            return self._error(status, exc.message)
        except (BrokenPipeError, ConnectionResetError):
            return None
        except Exception as exc:
            print(f"seq eval replay: {u.path}: {type(exc).__name__}: {exc}", file=sys.stderr)
            return self._error(500, f"{type(exc).__name__}: {exc}")
