"""CLI entry: start the ingest dashboard web server."""

from __future__ import annotations

import argparse
import logging
import sys
import threading
import time
import webbrowser


def configure_dashboard_logging() -> None:
    log = logging.getLogger("ingest_dashboard.api.errors")
    if log.handlers:
        return
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("%(levelname)s:     %(message)s"))
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    log.propagate = False


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="scrapy-ingest dashboard",
        description="Start the read-only scrapy-ingest web dashboard (FastAPI).",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Bind address (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8765,
        help="HTTP port (default: 8765)",
    )
    parser.add_argument("--db-url", help="Override DB_URL from Scrapy settings")
    parser.add_argument("--search-url", help="Override SEARCH_URL from Scrapy settings")
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload (development only)",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not open the dashboard URL in a browser",
    )
    args = parser.parse_args(argv)

    try:
        import uvicorn
    except ImportError:
        print(
            "scrapy-ingest dashboard requires optional dependencies.\n"
            'Install with: pip install "scrapy-ingest[dashboard]"',
            file=sys.stderr,
        )
        return 1

    return run_server(
        host=args.host,
        port=args.port,
        db_url=args.db_url,
        search_url=args.search_url,
        reload=args.reload,
        open_browser=not args.no_browser,
    )


def _browser_url(host: str, port: int) -> str:
    browse_host = host
    if host in ("0.0.0.0", "::"):
        browse_host = "127.0.0.1"
    return f"http://{browse_host}:{port}"


def _schedule_browser_open(url: str) -> None:
    def _open() -> None:
        time.sleep(0.85)
        try:
            webbrowser.open(url)
        except OSError:
            pass

    threading.Thread(target=_open, daemon=True).start()


def run_server(
    *,
    host: str = "127.0.0.1",
    port: int = 8765,
    db_url: str | None = None,
    search_url: str | None = None,
    reload: bool = False,
    open_browser: bool = True,
) -> int:
    import uvicorn

    from scrapy_ingest.exceptions import ConfigurationError, IngestError

    from .api.app import create_app

    try:
        app = create_app(db_url=db_url, search_url=search_url)
    except (ConfigurationError, IngestError, RuntimeError) as exc:
        print(f"scrapy-ingest dashboard: {exc}", file=sys.stderr)
        return 1
    url = f"http://{host}:{port}"
    browse_url = _browser_url(host, port)
    print(f"scrapy-ingest dashboard: {url}")
    print("Press Ctrl+C to stop.")
    configure_dashboard_logging()
    if open_browser and not reload:
        _schedule_browser_open(browse_url)
    uvicorn.run(app, host=host, port=port, reload=reload, log_level="info")
    return 0


if __name__ == "__main__":
    sys.exit(main())
