import os
from collections.abc import AsyncIterator
from contextlib import aclosing
from pathlib import Path

import pytest
import pytest_asyncio

from edison_client.clients.rest_client import RestClient
from edison_client.models.app import AuthType, Stage


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "live: tests that call the deployed API")
    config.addinivalue_line(
        "markers", "live_agent: tests exercising LLM/agent functionality (scheduled)"
    )


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Classify deployed clients before pytest applies its marker expression."""
    tests_dir = Path(__file__).parent
    for item in items:
        if not item.path.is_relative_to(tests_dir):
            continue
        if isinstance(item, pytest.Function) and {
            "admin_client",
            "pub_client",
        }.intersection(item.fixturenames):
            item.add_marker(pytest.mark.live)


@pytest_asyncio.fixture(loop_scope="function")
async def offline_client() -> AsyncIterator[RestClient]:
    """Use static auth and fail before networking if a request is not mocked."""
    async with aclosing(
        RestClient(
            stage=Stage.LOCAL,
            service_uri="unreachable://unit-test.invalid",
            auth_type=AuthType.JWT,
            jwt="test-token",
        )
    ) as client:
        yield client


@pytest_asyncio.fixture(name="admin_client", loop_scope="function")
async def fixture_admin_client() -> AsyncIterator[RestClient]:
    """Create a RestClient for testing; using a admin user key with full access."""
    async with aclosing(
        RestClient(stage=Stage.DEV, api_key=os.environ["PLAYWRIGHT_ADMIN_API_KEY"])
    ) as client:
        yield client


@pytest_asyncio.fixture(name="pub_client", loop_scope="function")
async def fixture_pub_client() -> AsyncIterator[RestClient]:
    """Create a RestClient for testing; using a public user key with limited access."""
    async with aclosing(
        RestClient(stage=Stage.DEV, api_key=os.environ["PLAYWRIGHT_PUBLIC_API_KEY"])
    ) as client:
        yield client
