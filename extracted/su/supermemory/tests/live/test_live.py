"""End-to-end checks against the real API.

Skipped unless SUPERMEMORY_LIVE_API_KEY is set; each run uses a throwaway
namespace that it deletes afterwards.

    SUPERMEMORY_LIVE_API_KEY=... uv run --group dev pytest tests/live -q
"""

import os
import time
import uuid
from collections.abc import Iterator

import pytest

import supermemory
from supermemory import AsyncSupermemory, Supermemory

API_KEY = os.environ.get("SUPERMEMORY_LIVE_API_KEY")
BASE_URL = os.environ.get("SUPERMEMORY_LIVE_BASE_URL")
pytestmark = pytest.mark.skipif(not API_KEY, reason="SUPERMEMORY_LIVE_API_KEY not set")


@pytest.fixture(scope="module")
def client() -> Supermemory:
    return Supermemory(api_key=API_KEY, base_url=BASE_URL)


@pytest.fixture(scope="module")
def namespace(client: Supermemory) -> Iterator[str]:
    name = f"sdk_python_test_{uuid.uuid4().hex[:10]}"
    yield name
    try:
        client.namespaces.delete(name)
    except supermemory.APIStatusError:
        pass


def test_add_get_search_list(client: Supermemory, namespace: str) -> None:
    added = client.add(namespace, content="The SDK test user's favorite color is teal.", id="favorite-color")
    assert added.id

    deadline = time.monotonic() + 90
    while True:
        document = client.documents.get(namespace, added.id)
        if document.system.status in ("done", "failed") or time.monotonic() > deadline:
            break
        time.sleep(3)
    assert document.system.status == "done", document.system.status

    results = client.search(namespace, query="What color does the user like?", limit=5).results
    assert results, "expected at least one search result"

    page = client.list(namespace, "documents", limit=10)
    assert any(d.id == added.id for d in page.documents or [])

    assert namespace in {ns.id for ns in client.namespaces.list()}


def test_profile_and_buckets(client: Supermemory, namespace: str) -> None:
    client.profile(namespace)
    client.profiles.get_buckets(namespace)


def test_errors(client: Supermemory, namespace: str) -> None:
    with pytest.raises(supermemory.NotFoundError) as exc:
        client.documents.get(namespace, "does-not-exist")
    assert exc.value.status_code == 404
    assert exc.value.response is not None

    with pytest.raises(supermemory.AuthenticationError):
        Supermemory(api_key="sm_invalid", base_url=BASE_URL).namespaces.list()


def test_raw_response_and_per_call_options(client: Supermemory, namespace: str) -> None:
    raw = client.with_raw_response.search(namespace, query="color", extra_headers={"X-Sdk-Test": "1"}, timeout=30)
    assert raw.status_code == 200
    assert isinstance(raw.parse().results, list)


async def test_async_client(namespace: str) -> None:
    async with AsyncSupermemory(api_key=API_KEY, base_url=BASE_URL) as client:
        response = await client.search(namespace, query="color")
        assert isinstance(response.results, list)
