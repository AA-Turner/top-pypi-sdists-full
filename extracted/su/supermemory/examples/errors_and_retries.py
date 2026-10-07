"""Error handling, retries, and per-request options.

SUPERMEMORY_API_KEY=... uv run examples/errors_and_retries.py
"""

import supermemory
from supermemory import Supermemory

client = Supermemory(max_retries=4, timeout=20.0)

try:
    client.with_options(max_retries=0).documents.get("example_user", "does-not-exist")
except supermemory.NotFoundError as e:
    print("not found:", e.body)
except supermemory.RateLimitError as e:
    print("rate limited; retry after", e.response.headers.get("retry-after") if e.response else "?")
except supermemory.APIConnectionError:
    print("network problem")

raw = client.with_raw_response.search("example_user", query="anything", extra_headers={"X-Trace": "demo"})
print("request id:", raw.headers.get("x-request-id"))
print("results:", len(raw.parse().results))
