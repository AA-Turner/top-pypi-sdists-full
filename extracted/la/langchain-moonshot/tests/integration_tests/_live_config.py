from __future__ import annotations

from langchain_core.rate_limiters import InMemoryRateLimiter

DEFAULT_API_BASE = "https://api.moonshot.cn/v1"
LIVE_MAX_RETRIES = 6
LIVE_RATE_LIMITER = InMemoryRateLimiter(
    requests_per_second=0.3,
    check_every_n_seconds=0.1,
    max_bucket_size=1,
)
