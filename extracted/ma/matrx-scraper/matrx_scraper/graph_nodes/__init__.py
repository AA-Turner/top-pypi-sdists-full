"""matrx-scraper → matrx-graph integration: scraper entry points as typed actions.

This submodule is the **only** place inside matrx-scraper that imports
``matrx-graph``. It is opt-in via the ``[graph]`` extra::

    pip install matrx-scraper[graph]

Import this module from a host (e.g. aidream) at startup to register all
scraper actions with matrx-graph's default registry::

    from matrx_scraper.graph_nodes import register_with_graph
    register_with_graph()

Actions registered:

- ``scraper.scrape``       — one URL → structured page
- ``scraper.scrape_many``  — parallel scrape of N URLs with bounded concurrency
- ``scraper.crawl_site``   — BFS crawl of a site, capped at max_pages
- ``media.stock_image.search`` — Unsplash search for real stock photos
"""

from __future__ import annotations

_registered = False


def register_with_graph() -> None:
    """Import the action modules so their ``@action`` decorators fire.

    Idempotent — safe to call multiple times.
    """
    global _registered
    if _registered:
        return

    from matrx_scraper.graph_nodes import (  # noqa: F401 — imported for side effects
        scrape_actions,
        stock_image_actions,
    )

    _registered = True


__all__ = ["register_with_graph"]
