"""The raw HTTP escape hatch: ``client.get`` / ``.post`` / ``.put`` / ``.patch``
/ ``.delete``.

Four operations downstream calls have no typed method on the pinned Stainless
surface — the three ``webhook_subscriptions`` operations and
``tool_router.session.delete`` — so this is the only surface a consumer has for
them, and the only one the live parity harness can run them on.

What these pin is that the escape hatch is the *same* kernel the generated
surface uses, reached a different way: the same credential header, the same
query encoding, the same error hierarchy, the same deprecation notice, the same
retry policy. An escape hatch with a contract of its own would be a second
client hiding inside the first.

The one deliberate difference from the generated surface is the body: a raw
call sends the caller's mapping verbatim, with no request model to rename
``auth_scheme`` into ``authScheme``. That is what "raw" has to mean — the
caller named a path the client has no model for.
"""

from __future__ import annotations

import json
import warnings
from typing import Any

import httpx
import pytest
import respx
from pydantic import BaseModel

from composio_client import (
    AsyncComposio,
    Composio,
    ComposioDeprecationWarning,
    NotFoundError,
    RequestOptions,
    _base_client,
)

from .conftest import API_KEY, BASE_URL

RAW_PATH = "/api/v3.1/webhook_subscriptions"


class Named(BaseModel):
    name: str


@pytest.fixture
def recorded_delays(monkeypatch: pytest.MonkeyPatch) -> list[float]:
    """Replace the kernel sleep seams so the retry test does not sleep."""
    delays: list[float] = []

    def record(seconds: float) -> None:
        delays.append(seconds)

    monkeypatch.setattr(_base_client, "_sleep", record)
    return delays


# ---- the five verbs reach the wire ----


@pytest.mark.parametrize(
    ("verb", "method"),
    [("get", "GET"), ("post", "POST"), ("put", "PUT"), ("patch", "PATCH"), ("delete", "DELETE")],
)
@respx.mock
def test_each_verb_dispatches_its_own_method(client: Composio, verb: str, method: str) -> None:
    route = respx.request(method, f"{BASE_URL}{RAW_PATH}").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )

    assert getattr(client, verb)(RAW_PATH) == {"ok": True}

    assert route.called
    assert route.calls.last.request.method == method


@pytest.mark.parametrize(
    ("verb", "method"),
    [("get", "GET"), ("post", "POST"), ("put", "PUT"), ("patch", "PATCH"), ("delete", "DELETE")],
)
async def test_each_async_verb_dispatches_its_own_method(
    async_client: AsyncComposio, verb: str, method: str
) -> None:
    with respx.mock:
        route = respx.request(method, f"{BASE_URL}{RAW_PATH}").mock(
            return_value=httpx.Response(200, json={"ok": True})
        )

        assert await getattr(async_client, verb)(RAW_PATH) == {"ok": True}

        assert route.called
        assert route.calls.last.request.method == method


# ---- it is the same kernel, not a second one ----


@respx.mock
def test_a_raw_call_carries_the_api_key_like_a_generated_one(client: Composio) -> None:
    route = respx.get(f"{BASE_URL}{RAW_PATH}").mock(return_value=httpx.Response(200, json={}))

    client.get(RAW_PATH)

    assert route.calls.last.request.headers["x-api-key"] == API_KEY


@respx.mock
def test_query_goes_through_the_kernels_own_encoder(client: Composio) -> None:
    """Arrays comma-joined, ``None`` dropped, nested mappings expanded — the
    escape hatch must not hand its query to httpx raw."""
    route = respx.get(f"{BASE_URL}{RAW_PATH}").mock(return_value=httpx.Response(200, json={}))

    client.get(RAW_PATH, query={"tags": ["a", "b"], "skip": None, "page": {"size": 5}})

    url = route.calls.last.request.url
    assert dict(url.params) == {"tags": "a,b", "page[size]": "5"}


@respx.mock
def test_an_error_status_raises_the_same_exception_a_typed_call_would(client: Composio) -> None:
    respx.get(f"{BASE_URL}{RAW_PATH}").mock(
        return_value=httpx.Response(404, json={"error": {"message": "gone"}})
    )

    with pytest.raises(NotFoundError):
        client.get(RAW_PATH)


@respx.mock
def test_a_deprecation_notice_on_a_raw_call_still_warns(client: Composio) -> None:
    respx.get(f"{BASE_URL}{RAW_PATH}").mock(
        return_value=httpx.Response(200, json={}, headers={"deprecation": "true"})
    )

    with pytest.warns(ComposioDeprecationWarning):
        client.get(RAW_PATH)


@respx.mock
def test_the_warning_points_at_the_callers_own_line(client: Composio) -> None:
    """``_note_deprecation`` counts frames, and the escape hatch adds one if it
    delegates. ``client.get(...)`` must sit exactly where a generated resource
    method sits: one frame below the caller."""
    respx.get(f"{BASE_URL}{RAW_PATH}").mock(
        return_value=httpx.Response(200, json={}, headers={"deprecation": "true"})
    )

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        client.get(RAW_PATH)

    notice = next(item for item in caught if issubclass(item.category, ComposioDeprecationWarning))
    assert notice.filename == __file__


@respx.mock
def test_a_raw_call_retries_on_the_same_policy(client: Composio, recorded_delays: list[float]) -> None:
    route = respx.get(f"{BASE_URL}{RAW_PATH}").mock(
        side_effect=[httpx.Response(429), httpx.Response(200, json={"ok": True})]
    )

    assert client.get(RAW_PATH) == {"ok": True}

    assert route.call_count == 2
    assert len(recorded_delays) == 1


# ---- cast_to ----


@respx.mock
def test_cast_to_validates_into_the_named_model(client: Composio) -> None:
    """The Stainless-shaped call. ``cast_to`` is required there and optional
    here, so a call written against the oracle keeps working."""
    respx.get(f"{BASE_URL}{RAW_PATH}").mock(return_value=httpx.Response(200, json={"name": "n"}))

    result = client.get(RAW_PATH, cast_to=Named)

    assert isinstance(result, Named)
    assert result.name == "n"


@respx.mock
def test_without_cast_to_the_decoded_json_comes_back_unvalidated(client: Composio) -> None:
    """No model means no model: a payload no generated schema describes is
    still returned, which is the point of reaching a path the client has none
    for."""
    payload = {"items": [{"unmodelled": 1}], "extra": None}
    respx.get(f"{BASE_URL}{RAW_PATH}").mock(return_value=httpx.Response(200, json=payload))

    assert client.get(RAW_PATH) == payload


# ---- the body is verbatim ----


@respx.mock
def test_a_raw_body_is_sent_without_any_alias_renaming(client: Composio) -> None:
    """``auth_scheme`` reaches the wire as ``authScheme`` through the generated
    surface, because that endpoint has a request model. A raw path has none,
    so the caller's own keys go out."""
    route = respx.post(f"{BASE_URL}{RAW_PATH}").mock(return_value=httpx.Response(200, json={}))

    client.post(RAW_PATH, body={"auth_scheme": "OAUTH2", "your_domain": "d"})

    sent: Any = json.loads(route.calls.last.request.content)
    assert sent == {"auth_scheme": "OAUTH2", "your_domain": "d"}


@respx.mock
def test_a_get_declares_no_content_type(client: Composio) -> None:
    """The verb with no ``body`` parameter must not invent an empty one."""
    route = respx.get(f"{BASE_URL}{RAW_PATH}").mock(return_value=httpx.Response(200, json={}))

    client.get(RAW_PATH)

    assert "content-type" not in route.calls.last.request.headers


# ---- request options ----


@respx.mock
def test_request_options_reach_a_raw_call(client: Composio) -> None:
    route = respx.get(f"{BASE_URL}{RAW_PATH}").mock(return_value=httpx.Response(200, json={}))

    client.get(RAW_PATH, options=RequestOptions(headers={"x-trace": "t"}, query={"limit": 5}))

    request = route.calls.last.request
    assert request.headers["x-trace"] == "t"
    assert dict(request.url.params) == {"limit": "5"}
