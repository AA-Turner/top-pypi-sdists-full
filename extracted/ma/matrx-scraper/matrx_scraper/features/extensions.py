"""
Optional extension functions for matrx-scraper.

The scraper package has no dependency on matrx_ai (or any AI library).
Apps that want AI-powered summarisation during scraping must call
``configure_extensions()`` at startup, passing callables that the scraper
can invoke without knowing anything about their internals.

Example (from the main aidream app or matrx_ai's web tool):

    from matrx_scraper.features.extensions import configure_extensions
    from matrx_ai.agent_runners.research import (
        scrape_research_condenser_agent_1,
        scrape_research_condenser_agent_2,
    )

    configure_extensions(
        condenser_1=scrape_research_condenser_agent_1,
        condenser_2=scrape_research_condenser_agent_2,
    )
"""

from __future__ import annotations

from typing import Any
from collections.abc import Awaitable, Callable

# Protocol: async (instructions, scraped_content, queries, search_results, ctx) -> result
# where result has a `.output: str` and `.success: bool` attribute.
CondenserFn = Callable[..., Awaitable[Any]]

_condenser_1: CondenserFn | None = None
_condenser_2: CondenserFn | None = None


def configure_extensions(
    *,
    condenser_1: CondenserFn | None = None,
    condenser_2: CondenserFn | None = None,
) -> None:
    """Register optional AI condenser functions.

    Call this once at application startup before any scraping takes place.
    Either or both condensers may be provided; unregistered slots remain None.
    """
    global _condenser_1, _condenser_2
    if condenser_1 is not None:
        _condenser_1 = condenser_1
    if condenser_2 is not None:
        _condenser_2 = condenser_2


def get_condenser_1() -> CondenserFn | None:
    return _condenser_1


def get_condenser_2() -> CondenserFn | None:
    return _condenser_2


def has_condenser() -> bool:
    """Return True if at least one condenser is available."""
    return _condenser_1 is not None or _condenser_2 is not None
