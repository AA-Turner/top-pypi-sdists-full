"""
Entrypoint for running the scraper as a standalone service.

    python -m matrx_scraper.server
    # or
    python -m matrx_scraper.server --port 9000 --workers 2
"""

from __future__ import annotations

import argparse
import sys


def main() -> None:
    parser = argparse.ArgumentParser(description="Matrx Scraper standalone server")
    parser.add_argument("--host", default=None, help="Bind host (default: from env or 0.0.0.0)")
    parser.add_argument(
        "--port", type=int, default=None, help="Bind port (default: from env or 8000)"
    )
    parser.add_argument(
        "--workers", type=int, default=None, help="Uvicorn workers (default: from env or 1)"
    )
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    args = parser.parse_args()

    from matrx_scraper.server.config import ServerConfig

    config = ServerConfig.from_env()

    if args.host is not None:
        config.host = args.host
    if args.port is not None:
        config.port = args.port
    if args.workers is not None:
        config.workers = args.workers

    try:
        import uvicorn
    except ImportError:
        print(
            "uvicorn is required to run the standalone server.\n"
            "Install it with: pip install matrx-scraper[server]",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"[scraper-server] Starting on {config.host}:{config.port}", file=sys.stderr, flush=True)

    uvicorn.run(
        "matrx_scraper.server.app:create_app",
        factory=True,
        host=config.host,
        port=config.port,
        workers=config.workers,
        reload=args.reload,
        log_level=config.log_level,
    )


if __name__ == "__main__":
    main()
