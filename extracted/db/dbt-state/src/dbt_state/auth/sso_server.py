from __future__ import annotations

import sys
import typing as t
from http.server import BaseHTTPRequestHandler, HTTPServer
from queue import Queue
from types import TracebackType
from urllib.parse import parse_qs, urlparse

if t.TYPE_CHECKING:
    if sys.version_info >= (3, 11):
        from typing import Self
    else:
        from typing_extensions import Self

LOGO = "https://auth.state.dbt.com/assets/logo-dbt-state.svg"
WARN_IMG = "https://auth.state.dbt.com/assets/warning-outline.svg"
LOCAL_OAUTH_PORT = 29525
""" The string "sql" in base 32"""


class SsoHttpServer(HTTPServer):
    allow_reuse_address = True

    def __init__(self) -> None:
        self.queue: Queue[str] = Queue()
        super().__init__(("", LOCAL_OAUTH_PORT), SsoHttpRequestHandler)
        self.timeout = 300

    def stop(self) -> None:
        """Best-effort stop: close the listening socket to unblock handle_request."""
        try:
            self.server_close()
        except Exception:
            pass

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: t.Optional[type[BaseException]],
        exc_val: t.Optional[BaseException],
        exc_tb: t.Optional[TracebackType],
    ) -> None:
        self.stop()


class SsoHttpRequestHandler(BaseHTTPRequestHandler):
    server: SsoHttpServer

    @staticmethod
    def _html(title: str, message: str) -> str:
        return str(f"""<!doctype html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="icon" href="https://auth.state.dbt.com/assets/favicon.ico" sizes="any" type="image/svg+xml" />
    <title>dbt State - Login</title>
    <style>
      * {{
        box-sizing: border-box;
      }}
      html, body {{
        margin: 0;
        padding: 0;
        min-height: 100vh;
        background: #0b0b0c;
        color: #f5f5f5;
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        -webkit-font-smoothing: antialiased;
      }}
      .page {{
        min-height: 100vh;
        display: flex;
        justify-content: center;
        padding: 84px 24px 24px;
      }}
      .container {{
        width: 100%;
        max-width: 520px;
        margin-left: auto;
        margin-right: auto;
      }}
      .brand {{
        margin-bottom: 44px;
      }}
      .brand svg {{
        height: 32px;
        width: auto;
        display: block;
      }}
      h1 {{
        font-size: 32px;
        line-height: 1.2;
        font-weight: 700;
        margin: 0 0 10px;
        letter-spacing: -0.01em;
      }}
      .subtitle {{
        font-size: 15px;
        color: #b8b8bd;
        margin: 0 0 30px;
      }}
      .card {{
        border: 1px solid #2a2a2e;
        border-radius: 11px;
        background: #141416;
        padding: 26px;
      }}
      .card-title {{
        font-size: 16px;
        font-weight: 600;
        margin: 0 0 16px;
        text-align: center;
      }}
      .btn {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        width: 100%;
        padding: 12px 18px;
        border-radius: 7px;
        font-size: 14.5px;
        font-weight: 600;
        text-decoration: none;
        transition: background 0.15s ease, border-color 0.15s ease;
        border: 1px solid transparent;
        cursor: pointer;
      }}
      .btn-primary {{
        background: #5b4cf5;
        color: #ffffff;
      }}
      .btn-primary:hover {{
        background: #4a3ce8;
      }}
      .btn-secondary {{
        background: transparent;
        color: #e4e4e8;
        border-color: #3a3a3f;
        margin-top: 10px;
      }}
      .btn-secondary:hover {{
        border-color: #5a5a60;
        background: #1b1b1e;
      }}
      .chev {{
        font-size: 17px;
        line-height: 1;
      }}
      .helper {{
        text-align: center;
        font-size: 12.5px;
        color: #8a8a90;
        margin: 14px 0 0;
      }}
      .error {{
        color: #f5f5f5;
        position: relative;
        background-color: #4b1f03;
        border: 1px solid #773501;
        border-radius: 0.375rem;
        padding: 0.5rem 0.5rem 0.5rem 2.25rem;
        font-size: 14px;
      }}
      .error img {{
        position: absolute;
        left: 0.5rem;
        top: 0.5rem;
        width: 1.1rem;
        height: 1.1rem;
      }}
    </style>
  </head>
  <body>
    <div class="page">
        <div class="container">
            <div class="brand"><img alt="dbt State" src="{LOGO}" height="24" style="height: 24px;" /></div>
            <h1>{title}</h1>
            <div>{message}</div>
        </div>
    </div>
  </body>
</html>
""")

    @staticmethod
    def success_html() -> str:
        return SsoHttpRequestHandler._html(
            title="You&rsquo;re signed in",
            message="<p class='subtitle'>Head back to your terminal to keep going.</p><button class='btn btn-primary' onclick='window.close()'>Close and return to terminal</button>",
        )

    @staticmethod
    def error_html(message: str) -> str:
        return SsoHttpRequestHandler._html(
            title="Sign-in failed",
            message=f"<p class='subtitle'>Something went wrong while completing authentication.</p><p class='error'><img src='{WARN_IMG}' alt='' />{message}</p><button class='btn btn-secondary' onclick='window.close()'>Close and return to terminal</button>",
        )

    def log_message(self, format: str, *args: t.Any) -> None:
        pass

    def do_GET(self) -> None:
        self.server.queue.put(self.path)

        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)

        if "error" in query:
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.send_header("Connection", "close")
            self.end_headers()
            message = query["error"][0]
            if query.get("error_description"):
                message = message + ": " + query["error_description"][0]
            self.wfile.write(self.error_html(message).encode("utf-8"))
            self.close_connection = True
            return

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(self.success_html().encode("utf-8"))
        self.close_connection = True
