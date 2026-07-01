"""Standalone, environment-independent tools.

These can be used directly in any agent loop without an OpenReward
``Environment``:

    from openreward.tools import Backsearch, Backfetch

    bs = Backsearch(as_of="2025-12-01")
    result = await bs.run("recent ICML 2025 RL papers")

For use *inside* an environment, see
:class:`openreward.toolsets.BackSearchToolset`, which exposes the same
backdated search/fetch as ``web_search`` / ``web_fetch`` tools.
"""

from .web import (
    Backfetch,
    Backsearch,
    WebToolResult,
    clear_web_fetch_cache,
    run_fetch,
    run_search,
)

__all__ = [
    "Backfetch",
    "Backsearch",
    "WebToolResult",
    "clear_web_fetch_cache",
    "run_fetch",
    "run_search",
]
