"""Offline `platform.feature_knob` values for feature "seo" (tests import this, never conftest)."""

from __future__ import annotations

SEO_KNOB_VALUES: dict[str, dict[str, object]] = {
    "seo": {
        "max_per_request_cost_usd": 0.25,
        "unpriced_run_assumed_cost_usd": 0.01,
        "org_provider_monthly_ceiling_usd": 50,
        "global_provider_monthly_ceiling_usd": 750,
        "caller_daily_ceiling_usd": 1,
        "global_daily_ceiling_usd": 50,
        "inline_payload_max_bytes": 32768,
        # Reuse windows (hours) per operation family — matrx_seo.reuse; the
        # values the hard-coded TTLs had before they became knobs.
        "reuse_hours.backlinks": 720,
        "reuse_hours.keyword_metrics": 720,
        "reuse_hours.serp": 24,
        "reuse_hours.onpage": 24,
        "reuse_hours.reference": 720,
        "reuse_hours.web_search": 168,
        "reuse_hours.default": 168,
    },
}
