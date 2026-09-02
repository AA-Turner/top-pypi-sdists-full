"""
matrx_scraper.server — Standalone microservice entrypoint.

Usage:
    # As a module:
    python -m matrx_scraper.server

    # Programmatically:
    from matrx_scraper.server import create_app
    app = create_app()

Requires the ``server`` optional dependency group:
    pip install matrx-scraper[server]
"""

from matrx_scraper.server.app import create_app
from matrx_scraper.server.config import ServerConfig

__all__ = ["create_app", "ServerConfig"]
