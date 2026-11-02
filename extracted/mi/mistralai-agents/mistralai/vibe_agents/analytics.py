"""The request header that keeps an Agents SDK caller out of the control plane's product analytics.

The control plane still emits its events for these requests, flagged, so analysts filter test and CI
traffic out instead of guessing it from names or creators.
"""

EXCLUDE_FROM_ANALYTICS_HEADER = "X-Mistral-Exclude-From-Analytics"


def excluded_from_analytics(header_value: str | None) -> bool:
    """Return whether a request asked to be left out of product analytics."""
    return header_value is not None and header_value.strip().lower() == "true"


__all__ = ["EXCLUDE_FROM_ANALYTICS_HEADER", "excluded_from_analytics"]
