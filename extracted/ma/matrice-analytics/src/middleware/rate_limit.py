"""Simple in-memory rate limiter.

For production, use Redis-backed rate limiting (e.g., slowapi, fastapi-limiter).

Usage with FastAPI:
    limiter = RateLimiter(max_requests=100, window_seconds=60)

    @app.get("/api/data")
    async def get_data(request: Request):
        if not limiter.check(request.client.host):
            raise HTTPException(429, "Rate limit exceeded")
        ...
"""

import time
from collections import defaultdict
from threading import Lock


class RateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = window_seconds
        self._hits: dict[str, list[float]] = defaultdict(list)
        self._lock = Lock()

    def check(self, key: str) -> bool:
        """Returns True if request is allowed, False if rate limited."""
        now = time.time()
        with self._lock:
            # Remove expired entries
            self._hits[key] = [t for t in self._hits[key] if now - t < self.window]
            if len(self._hits[key]) >= self.max_requests:
                return False
            self._hits[key].append(now)
            return True
