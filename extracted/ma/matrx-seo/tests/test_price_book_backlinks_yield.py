"""Backlinks row lists are billed per row RETURNED, so the book prices the observed
yield, not the cap (OPENSEO-TOOLS-SPEC §6.3; coordinator ruling 2026-09-28).

Figures are the provider's billed costs for these exact shapes in seo.provider_call.
"""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

from matrx_seo.providers.dataforseo.pricing import estimate

sys.path.insert(0, str(Path(__file__).parent))
from test_price_book_calibration_live import calibration_failures  # noqa: E402


def _bl(endpoint: str, *, limit: int | None = 1000, max_items: int | None = None) -> dict:
    task = {"target": "titaniumsuccess.com"}
    if limit is not None:
        task["limit"] = limit
    settings = {"tasks": [task], "endpoint": endpoint}
    if max_items is not None:
        settings["max_items"] = max_items
    return settings


def test_a_ten_thousand_item_backlinks_pull_is_not_priced_as_ten_full_pages() -> None:
    # Billed $0.103584 and $0.105816 (2 calls). The cap-priced book said $0.60.
    got = estimate("backlinks.core", _bl("/v3/backlinks/backlinks/live", max_items=10_000))
    assert got == Decimal("0.060000")


def test_list_endpoints_are_priced_at_their_observed_yield() -> None:
    # anchors billed 0.029148-0.031092 at limit 1000; the cap priced 0.06.
    assert estimate("backlinks.core", _bl("/v3/backlinks/anchors/live")) == Decimal("0.030984")
    assert estimate(
        "backlinks.core", _bl("/v3/backlinks/referring_domains/live")
    ) == Decimal("0.039372")
    # a small limit is still the cap
    assert estimate("backlinks.core", _bl("/v3/backlinks/anchors/live", limit=10)) == Decimal(
        "0.024360"
    )


def test_a_time_series_is_priced_per_period_not_as_one_row() -> None:
    got = estimate(
        "backlinks.pages_competitors_timeseries",
        _bl("/v3/backlinks/timeseries_summary/live", limit=None),
    )
    assert got == Decimal("0.027276")  # billed 0.027276 at 91 periods


def test_the_calibration_check_fails_a_book_that_is_off() -> None:
    rows = [
        {"operation": "backlinks.core", "settings": _bl("/v3/backlinks/anchors/live"),
         "reported": "0.012"},
    ]
    failures = calibration_failures(rows, Decimal("0.25"))
    assert failures and "backlinks.core" in failures[0]
    rows[0]["reported"] = "0.031"
    assert calibration_failures(rows, Decimal("0.25")) == []
