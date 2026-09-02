"""Crawl recipes — pre-baked handlers for known sites.

A *recipe* is a host-pattern + a list of actions to apply when visiting any
URL on that host. Use cases: dismiss cookie banners, click "I'm over 18"
gates, scroll to trigger lazy-loaded content, hide sticky chat widgets,
wait for SPA hydration.

The crawler picks the most-specific matching recipe (longest host suffix
wins) and runs the action list against the Playwright `page` object before
parsing. With render_mode=http_only, recipes are no-ops — they only have
teeth when a browser is in the loop.

Standalone — no sibling matrx imports. Recipes are pure data; the runtime
that interprets them lives in the host (so we can swap engines later
without touching the registry).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Protocol
from urllib.parse import urlparse


ActionType = Literal[
    "click",  # selector
    "wait_for",  # selector, timeout_ms
    "scroll_to_bottom",  # steps, delay_ms
    "scroll_by",  # px
    "remove",  # selector — set display:none on every match
    "set_value",  # selector + value (e.g. age-gate inputs)
    "press",  # key (Escape, Enter)
    "evaluate",  # script (raw JS string)
    "sleep",  # ms
]


@dataclass
class RecipeAction:
    type: ActionType
    selector: str | None = None
    value: str | None = None
    key: str | None = None
    script: str | None = None
    timeout_ms: int | None = None
    steps: int | None = None
    delay_ms: int | None = None
    px: int | None = None
    ms: int | None = None

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> RecipeAction:
        return cls(
            type=d.get("type"),  # type: ignore[arg-type]
            selector=d.get("selector"),
            value=d.get("value"),
            key=d.get("key"),
            script=d.get("script"),
            timeout_ms=d.get("timeout_ms"),
            steps=d.get("steps"),
            delay_ms=d.get("delay_ms"),
            px=d.get("px"),
            ms=d.get("ms"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}


@dataclass
class CrawlRecipe:
    name: str
    host_pattern: str  # exact host or ".suffix" form (most specific wins)
    actions: list[RecipeAction] = field(default_factory=list)
    enabled: bool = True
    description: str | None = None

    def matches(self, host: str) -> bool:
        if not self.enabled:
            return False
        host = host.lower()
        pat = self.host_pattern.lower().strip()
        if pat == host:
            return True
        if pat.startswith(".") and host.endswith(pat):
            return True
        return False


class RecipeBackend(Protocol):
    """Pluggable recipe registry. The host (aidream) provides the Postgres
    implementation; tests / standalone callers can plug an in-memory list.
    """

    async def find_for_url(self, url: str) -> CrawlRecipe | None: ...


class StaticRecipeBackend:
    """Default in-memory backend. Useful for tests and local dev."""

    def __init__(self, recipes: list[CrawlRecipe]) -> None:
        self.recipes = recipes

    async def find_for_url(self, url: str) -> CrawlRecipe | None:
        host = urlparse(url).netloc.lower()
        if not host:
            return None
        # Exact host match wins; otherwise longest .suffix match.
        candidates = [r for r in self.recipes if r.matches(host)]
        if not candidates:
            return None
        candidates.sort(
            key=lambda r: (
                0 if r.host_pattern.lower() == host else 1,
                -len(r.host_pattern),
            )
        )
        return candidates[0]


# Reference recipes — start small. Hosts can extend via the DB-backed backend.
DEFAULT_RECIPES: list[CrawlRecipe] = [
    # Generic OneTrust cookie banner — common across many WordPress / agency sites.
    CrawlRecipe(
        name="onetrust-cookie-accept",
        host_pattern=".onetrust.com",
        description="Dismisses the OneTrust cookie consent banner.",
        actions=[
            RecipeAction(type="click", selector="#onetrust-accept-btn-handler", timeout_ms=3000),
        ],
    ),
]


__all__ = [
    "ActionType",
    "RecipeAction",
    "CrawlRecipe",
    "RecipeBackend",
    "StaticRecipeBackend",
    "DEFAULT_RECIPES",
]
