"""token_provider / from_token_file: per-request credential resolution.

K8s rewrites projected ServiceAccount token files ~every 50 min; these
tests pin that a provider-constructed client presents the *current*
credential on every request, not the one seen at construction.
"""

from __future__ import annotations

from itertools import count
from typing import TYPE_CHECKING, Any

import httpx
import pytest
import respx

from conftest import TEST_BASE_URL
from hogland import AsyncHogbox, AsyncHogland, BoxView, ConfigurationError, Hogbox, Hogland

if TYPE_CHECKING:
    from pathlib import Path

# One stdout frame then the closing exit frame, in the wire shape hogplane
# emits (see _sse.py). Used to drive the streaming-exec path end to end.
_SSE_BODY = 'event: stdout\ndata: hi\n\nevent: exit\ndata: {"code": 0, "duration_ms": 1}\n\n'


def _stub_get(box_view_json: dict[str, Any], box_id: str = "hb-tp") -> respx.Route:
    return respx.get(f"{TEST_BASE_URL}/v1/hogboxes/{box_id}").mock(
        return_value=httpx.Response(200, json={**box_view_json, "id": box_id}),
    )


def _stub_stream(box_id: str = "hb-tp") -> respx.Route:
    return respx.post(f"{TEST_BASE_URL}/v1/hogboxes/{box_id}/exec/stream").mock(
        return_value=httpx.Response(
            200,
            headers={"content-type": "text/event-stream"},
            text=_SSE_BODY,
        ),
    )


def _auth_headers(route: respx.Route) -> list[str]:
    return [call.request.headers["Authorization"] for call in route.calls]


@respx.mock
def test_provider_called_per_request(box_view_json: dict[str, Any]) -> None:
    route = _stub_get(box_view_json)
    counter = count(1)
    client = Hogland(token_provider=lambda: f"jwt-{next(counter)}", base_url=TEST_BASE_URL)
    client.get("hb-tp")
    client.get("hb-tp")
    assert _auth_headers(route) == ["Bearer jwt-1", "Bearer jwt-2"]


# conftest sets $HOG_TOKEN=test-token, so both cases also prove the env
# fallback does not preempt the provider.
@pytest.mark.parametrize(
    "static_token",
    [None, "static-should-lose"],
    ids=["env-only", "explicit-token-kwarg"],
)
@respx.mock
def test_provider_wins_over_static_token(
    box_view_json: dict[str, Any],
    static_token: str | None,
) -> None:
    route = _stub_get(box_view_json)
    client = Hogland(
        token=static_token,
        token_provider=lambda: "provider-token",
        base_url=TEST_BASE_URL,
    )
    client.get("hb-tp")
    assert _auth_headers(route) == ["Bearer provider-token"]


def test_provider_needs_no_token_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("HOG_TOKEN", raising=False)
    client = Hogland(token_provider=lambda: "jwt", base_url=TEST_BASE_URL)
    assert client.token == "jwt"


def test_token_property_reads_provider_fresh() -> None:
    counter = count(1)
    client = Hogland(token_provider=lambda: f"jwt-{next(counter)}", base_url=TEST_BASE_URL)
    assert client.token == "jwt-1"
    assert client.token == "jwt-2"


@respx.mock
def test_from_token_file_rereads_rotated_file(
    box_view_json: dict[str, Any],
    tmp_path: Path,
) -> None:
    token_file = tmp_path / "token"
    token_file.write_text("first-jwt\n")
    route = _stub_get(box_view_json)
    client = Hogland.from_token_file(token_file, base_url=TEST_BASE_URL)
    client.get("hb-tp")
    token_file.write_text("rotated-jwt\n")
    client.get("hb-tp")
    assert _auth_headers(route) == ["Bearer first-jwt", "Bearer rotated-jwt"]


@pytest.mark.parametrize("cls", [Hogland, AsyncHogland])
def test_from_token_file_missing_file_fails_at_construction(
    cls: type[Hogland | AsyncHogland],
    tmp_path: Path,
) -> None:
    with pytest.raises(ConfigurationError, match="token file not found"):
        cls.from_token_file(tmp_path / "does-not-exist")


@pytest.mark.asyncio
@respx.mock
async def test_async_provider_called_per_request(box_view_json: dict[str, Any]) -> None:
    route = _stub_get(box_view_json)
    counter = count(1)
    async with AsyncHogland(
        token_provider=lambda: f"jwt-{next(counter)}",
        base_url=TEST_BASE_URL,
    ) as client:
        await client.get("hb-tp")
        await client.get("hb-tp")
    assert _auth_headers(route) == ["Bearer jwt-1", "Bearer jwt-2"]


@pytest.mark.asyncio
@respx.mock
async def test_async_from_token_file_rereads_rotated_file(
    box_view_json: dict[str, Any],
    tmp_path: Path,
) -> None:
    token_file = tmp_path / "token"
    token_file.write_text("first-jwt\n")
    route = _stub_get(box_view_json)
    async with AsyncHogland.from_token_file(token_file, base_url=TEST_BASE_URL) as client:
        await client.get("hb-tp")
        token_file.write_text("rotated-jwt\n")
        await client.get("hb-tp")
    assert _auth_headers(route) == ["Bearer first-jwt", "Bearer rotated-jwt"]


@respx.mock
def test_provider_called_on_streaming_exec(box_view_json: dict[str, Any]) -> None:
    # The streaming path builds its request through httpx-sse's
    # connect_sse, a different entry point from the unary POST. Pin that
    # _BearerAuth still runs the provider there.
    route = _stub_stream()
    counter = count(1)
    client = Hogland(token_provider=lambda: f"jwt-{next(counter)}", base_url=TEST_BASE_URL)
    box = Hogbox(BoxView.model_validate({**box_view_json, "id": "hb-tp"}), client)
    kinds = [event.kind for event in box.exec_stream(["echo", "hi"])]
    assert kinds == ["stdout", "exit"]
    assert _auth_headers(route) == ["Bearer jwt-1"]


@pytest.mark.asyncio
@respx.mock
async def test_async_provider_called_on_streaming_exec(box_view_json: dict[str, Any]) -> None:
    route = _stub_stream()
    counter = count(1)
    async with AsyncHogland(
        token_provider=lambda: f"jwt-{next(counter)}",
        base_url=TEST_BASE_URL,
    ) as client:
        box = AsyncHogbox(BoxView.model_validate({**box_view_json, "id": "hb-tp"}), client)
        kinds = [event.kind async for event in box.exec_stream(["echo", "hi"])]
    assert kinds == ["stdout", "exit"]
    assert _auth_headers(route) == ["Bearer jwt-1"]


@respx.mock
def test_from_token_file_read_error_wrapped(
    box_view_json: dict[str, Any],
    tmp_path: Path,
) -> None:
    # A per-request read can race the kubelet's atomic token swap and hit
    # a transient OSError. It must surface as ConfigurationError, not leak
    # a raw OSError out of the auth hook. Deleting the file mid-flight
    # reproduces the failing read.
    token_file = tmp_path / "token"
    token_file.write_text("jwt\n")
    _stub_get(box_view_json)
    client = Hogland.from_token_file(token_file, base_url=TEST_BASE_URL)
    token_file.unlink()
    with pytest.raises(ConfigurationError, match="failed to read token file"):
        client.get("hb-tp")
