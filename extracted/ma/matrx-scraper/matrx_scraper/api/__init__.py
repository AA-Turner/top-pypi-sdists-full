"""
matrx_scraper.api — FastAPI routers for the scraper package.

These routers depend on ``matrx-connect`` (optional dep) and are
dormant when matrx-scraper is used as a library. They activate when:

  1. Imported by a host app (aidream) and mounted on its FastAPI instance, OR
  2. Used by ``matrx_scraper.server`` to create a standalone microservice.

All imports are from ``matrx_connect`` — never from ``aidream``.

Routers:

  * ``scrape_router``   — streaming quick-scrape, search, search-and-scrape
  * ``ext_router``      — batch scrape, content save, retry queue, domain config
  * ``browser_router``  — stateful Playwright sessions for AI agents (navigate,
                          click, fill, type, screenshot, etc.)
  * ``preview_router``  — quick site preview (robots + SEO audit + screenshot)
  * ``crawl_router``    — direct canonical start/bootstrap/cancel commands
"""

from matrx_scraper.api.scrape_router import router as scrape_router
from matrx_scraper.api.ext_router import router as ext_router
from matrx_scraper.api.browser_router import router as browser_router
from matrx_scraper.api.preview_router import router as preview_router
from matrx_scraper.api.crawl_router import router as crawl_router

__all__ = [
    "scrape_router",
    "ext_router",
    "browser_router",
    "preview_router",
    "crawl_router",
]
