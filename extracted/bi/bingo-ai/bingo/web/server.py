"""bingo/web/server.py — local web IDE (FastAPI + WebSocket).

Security model: the browser can read/write files and drive a pentest engine,
so this is treated as a local RCE surface. We bind loopback, mint a random
session token (see security.py), require it on every /api + /ws call, and lock
CORS to the launch origin. WSL2 needs 0.0.0.0 to be reachable from the Windows
browser; there the token is the only gate, so we warn.
"""
from __future__ import annotations

import socket
import threading
from pathlib import Path

from .security import SESSION_TOKEN, verify_token

_STATIC = Path(__file__).parent / "static"
_TEMPLATES = Path(__file__).parent / "templates"


def _is_wsl2() -> bool:
    try:
        with open("/proc/version") as f:
            return "microsoft" in f.read().lower()
    except Exception:
        return False


def _find_free_port(start: int = 17890) -> int:
    for p in range(start, start + 40):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(("127.0.0.1", p))
                return p
        except OSError:
            continue
    return start


def _serve_index(port: int, lang: str) -> str:
    """Read the SPA template and inject the session token + config as JSON.

    The token never touches disk; it lives only in this served page and the
    memory of the tab that loaded it.
    """
    import json

    html = (_TEMPLATES / "index.html").read_text(encoding="utf-8")
    boot = json.dumps({"token": SESSION_TOKEN, "port": port, "lang": lang})
    inject = f'<script>window.__BINGO__={boot};</script>'
    if "</head>" in html:
        return html.replace("</head>", inject + "\n</head>", 1)
    return inject + html


def _make_app(session):
    """Build the Starlette/FastAPI app for one WebSession."""
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse, PlainTextResponse
    from fastapi.staticfiles import StaticFiles

    from . import routes

    port = session.config_port  # set by start_web_server
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

    origin = f"http://127.0.0.1:{port}"

    @app.middleware("http")
    async def _guard(request: Request, call_next):
        path = request.url.path
        # Static assets and the index shell are public; everything else needs
        # the token (header, query, or cookie) and a same-origin referer.
        if path.startswith("/api"):
            tok = (request.headers.get("x-bingo-token")
                   or request.query_params.get("token"))
            if not verify_token(tok):
                return JSONResponse({"error": "unauthorized"}, status_code=401)
            ref = request.headers.get("origin") or ""
            if ref and not ref.startswith(origin):
                return JSONResponse({"error": "bad origin"}, status_code=403)
        return await call_next(request)

    if _STATIC.exists():
        app.mount("/static", StaticFiles(directory=str(_STATIC)), name="static")

    routes.register(app, session, port)
    return app


def start_web_server(session) -> int:
    """Start uvicorn in a daemon thread. Returns the bound port."""
    port = _find_free_port(17890)
    session.config_port = port
    wsl = _is_wsl2()
    host = "0.0.0.0" if wsl else "127.0.0.1"
    if wsl:
        print("  [!] WSL2 detected: binding 0.0.0.0 so the Windows browser "
              "can reach Bingo. The session token is the only gate — do not "
              "expose this port beyond your machine.")

    app = _make_app(session)

    def _run():
        import uvicorn
        uvicorn.run(app, host=host, port=port, log_level="error",
                    access_log=False)

    t = threading.Thread(target=_run, daemon=True, name="bingo-web")
    t.start()

    import time
    time.sleep(0.8)  # wait for bind
    return port
