"""Examples using the httpx compatible transport.

Run directly:
    uv run python -m examples.compatibility_httpx
"""

import asyncio
import sys

import httpx
from pyreqwest.client import ClientBuilder
from pyreqwest.compatibility.httpx import HttpxTransport, SyncHttpxTransport

from ._utils import httpbin_url, run_examples


async def example_httpx() -> None:
    """Example using httpx compatibility layer."""
    async with httpx.AsyncClient(transport=HttpxTransport()) as httpx_client:
        resp = await httpx_client.get(str(httpbin_url() / "get"), params={"q": "pyreqwest"})
        data = resp.json()
        print({"url": data["url"], "status": resp.status_code})


async def example_httpx_custom_client() -> None:
    """Example using httpx compatibility layer with a custom pyreqwest client."""
    async with (
        ClientBuilder().http1_only().build() as client,
        httpx.AsyncClient(transport=HttpxTransport(client)) as httpx_client,
    ):
        resp = await httpx_client.get(str(httpbin_url() / "get"), params={"q": "pyreqwest"})
        data = resp.json()
        print({"url": data["url"], "status": resp.status_code})


def example_httpx_sync() -> None:
    """Example using httpx compatibility layer in sync client."""
    with httpx.Client(transport=SyncHttpxTransport()) as httpx_client:
        resp = httpx_client.get(str(httpbin_url() / "get"), params={"q": "pyreqwest"})
        data = resp.json()
        print({"url": data["url"], "status": resp.status_code})


if __name__ == "__main__":
    asyncio.run(run_examples(sys.modules[__name__]))
