"""Simple request sending without needing to create a client.

Run directly:
    uv run python -m examples.simple
"""

import asyncio
import sys

from ._utils import httpbin_url, run_examples


async def example_simple_async_get() -> None:
    """Simple async GET request."""
    from pyreqwest.simple.request import pyreqwest_get

    resp = await pyreqwest_get(httpbin_url() / "get").send()
    print({"status": resp.status})


def example_simple_sync_get() -> None:
    """Simple sync GET request."""
    from pyreqwest.simple.sync_request import pyreqwest_get

    resp = pyreqwest_get(httpbin_url() / "get").send()
    print({"status": resp.status})


if __name__ == "__main__":
    asyncio.run(run_examples(sys.modules[__name__]))
