from __future__ import annotations

from argparse import ArgumentParser
import errno
from pathlib import Path
from socketserver import ThreadingMixIn
import sys
from wsgiref.simple_server import WSGIServer, make_server

from . import create_app
from packages.runtime_layout import default_cli_state_dir


class ThreadingWSGIServer(ThreadingMixIn, WSGIServer):
    daemon_threads = True


def main() -> int:
    parser = ArgumentParser(description="Run the Aegis API surface locally.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument(
        "--database",
        default=str(default_cli_state_dir() / "aegis.sqlite3"),
        help="SQLite database path for CLI session state.",
    )
    args = parser.parse_args()

    app = create_app(database_path=Path(args.database))
    try:
        with make_server(args.host, args.port, app, server_class=ThreadingWSGIServer) as server:
            print(f"Serving Aegis API on http://{args.host}:{args.port}")
            server.serve_forever()
    except OSError as exc:
        if exc.errno == errno.EADDRINUSE:
            print(
                f"Aegis API could not bind http://{args.host}:{args.port}; the address is already in use.",
                file=sys.stderr,
            )
            return 1
        raise
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
