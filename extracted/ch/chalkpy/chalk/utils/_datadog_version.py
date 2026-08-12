from functools import lru_cache
from typing import Any


@lru_cache(maxsize=1)
def get_datadog_statsd() -> Any | None:
    """Return the optional StatsD client, importing and caching it on first use."""
    try:
        from datadog.dogstatsd.base import statsd

        return statsd
    except ImportError:
        return None
