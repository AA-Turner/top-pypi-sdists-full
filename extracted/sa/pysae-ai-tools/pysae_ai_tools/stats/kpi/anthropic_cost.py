"""Anthropic Admin API collector: organization API spend over a window.

Covers pay-per-use API costs only — Claude subscription seats do not appear
in the cost report and are passed separately (``--ai-seats-monthly-usd``).
"""

import httpx

from ...env.resolve import try_auto_resolve

COST_REPORT_URL = "https://api.anthropic.com/v1/organizations/cost_report"
ANTHROPIC_VERSION = "2023-06-01"


def api_cost_usd(since: str, until: str) -> float:
    """Total API cost in USD over ``[since, until)`` (YYYY-MM-DD bounds)."""
    admin_key = try_auto_resolve("ANTHROPIC_ADMIN_API_KEY")
    if not admin_key:
        raise RuntimeError(
            "ANTHROPIC_ADMIN_API_KEY not resolved — run `pysae-ai-tools env resolve ANTHROPIC_ADMIN_API_KEY`"
        )

    total = 0.0
    page: str | None = None
    with httpx.Client(
        headers={"x-api-key": admin_key, "anthropic-version": ANTHROPIC_VERSION},
        timeout=30,
    ) as anthropic:
        while True:
            params: dict[str, str] = {
                "starting_at": f"{since}T00:00:00Z",
                "ending_at": f"{until}T00:00:00Z",
                "limit": "31",
            }
            if page:
                params["page"] = page
            resp = anthropic.get(COST_REPORT_URL, params=params)
            resp.raise_for_status()
            payload = resp.json()
            for bucket in payload.get("data", []):
                for result in bucket.get("results", []):
                    total += float(result.get("amount") or 0)
            if not payload.get("has_more"):
                return round(total, 2)
            page = payload.get("next_page")
