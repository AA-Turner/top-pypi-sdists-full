import os
from contextlib import aclosing

import pytest_asyncio

from edison_client.clients.rest_client import RestClient
from edison_client.models.app import Stage


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "live: tests that hit real deployed agents",
    )
    config.addinivalue_line(
        "markers",
        "live_agent: tests exercising LLM/agent functionality (scheduled)",
    )


ADMIN_API_KEY = os.environ.get("PLAYWRIGHT_ADMIN_API_KEY", "")
PUBLIC_API_KEY = os.environ.get("PLAYWRIGHT_PUBLIC_API_KEY", "")


@pytest_asyncio.fixture(name="admin_client")
async def fixture_admin_client():
    """Create a RestClient for testing; using a admin user key with full access."""
    async with aclosing(RestClient(stage=Stage.DEV, api_key=ADMIN_API_KEY)) as client:
        yield client


@pytest_asyncio.fixture(name="pub_client")
async def fixture_pub_client():
    """Create a RestClient for testing; using a public user key with limited access."""
    async with aclosing(RestClient(stage=Stage.DEV, api_key=PUBLIC_API_KEY)) as client:
        yield client
