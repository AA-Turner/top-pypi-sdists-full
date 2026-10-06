"""Check before buying again — the reuse windows every paid provider shares.

Each provider operation declares a reuse FAMILY (``SeoProviderOperation.reuse_family``).
How long a completed run of that family is reused is a Feature Knob,
``seo.reuse_hours.<family>``, overridable per organization and per person (the
host injects that ladder through :func:`matrx_seo.knobs.set_scoped_knob_resolver`).
An operation with no family keeps no reuse window (free first-party reads whose
identity is their date range). A caller may only NARROW a window, via
``CollectionRequest.require_fresh_within_seconds``.

No constant stands in for a knob: a missing row raises ``KnobNotRegisteredError``.
"""

from __future__ import annotations

from .knobs import scoped_int_knob

REUSE_KNOB_FEATURE = "seo"

#: Every reuse family a provider operation may declare. Each one is a knob row.
REUSE_FAMILIES: tuple[str, ...] = (
    "backlinks",
    "keyword_metrics",
    "serp",
    "onpage",
    "reference",
    "web_search",
    "default",
)


def reuse_knob_key(family: str) -> str:
    if family not in REUSE_FAMILIES:
        raise ValueError(f"unknown SEO reuse family {family!r}; known: {', '.join(REUSE_FAMILIES)}")
    return f"reuse_hours.{family}"


async def reuse_window_seconds(
    family: str | None, organization_id: str | None, user_id: str | None
) -> int:
    """The reuse window for ``family`` as this organization and person see it.
    ``None`` family → 0 (the operation keeps no reuse window)."""
    if family is None:
        return 0
    hours = await scoped_int_knob(
        REUSE_KNOB_FEATURE, reuse_knob_key(family), organization_id, user_id
    )
    return max(int(hours), 0) * 3600


def narrowed(window_seconds: int, require_fresh_within_seconds: int | None) -> int:
    """A caller's freshness requirement narrows the window; it never widens it."""
    if require_fresh_within_seconds is None:
        return window_seconds
    return min(window_seconds, max(int(require_fresh_within_seconds), 0))


__all__ = [
    "REUSE_FAMILIES",
    "REUSE_KNOB_FEATURE",
    "narrowed",
    "reuse_knob_key",
    "reuse_window_seconds",
]
