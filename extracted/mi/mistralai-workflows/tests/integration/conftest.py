import os
from typing import Generator

import httpx
import pytest


@pytest.fixture(autouse=True)
def setup_test_config() -> Generator[None, None, None]:
    # Override the autouse fixture from workflow_sdk/tests/conftest.py, which sets
    # config.worker.deployment_name = "test-task-queue" for unit tests. Integration
    # tests run against a real server, so the config must reflect the actual env vars
    # (DEPLOYMENT_NAME=example-dev-worker) rather than the unit-test sentinel value.
    yield


@pytest.fixture
def server_url():
    return os.getenv("SERVER_URL", "http://localhost:7444")


@pytest.fixture
def api_client(server_url) -> httpx.AsyncClient:
    api_key = os.getenv("MISTRAL_API_KEY")

    return httpx.AsyncClient(
        base_url=server_url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        timeout=120.0,
    )
