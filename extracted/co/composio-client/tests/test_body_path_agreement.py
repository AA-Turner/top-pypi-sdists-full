"""The two request-body routes must produce the same wire bytes.

``BodyParam = BaseModel | Mapping[str, Any]``: a caller may hand a resource
method a plain dict or the generated pydantic model for that endpoint. They are
two different code paths in the kernel —

* a dict goes through :func:`composio_client._aliasing.rename_to_wire_names`,
  which renames keys and copies every value through untouched;
* a model goes through ``model_dump(mode="json", by_alias=True,
  exclude_unset=True)``.

For one logical payload those two must be indistinguishable on the wire, and for
a while they were not: pydantic coerces at model *construction*, so
``expires_in: 3600`` came back out as ``3600.0`` and ``AnyUrl`` rewrote
``"https://Example.COM"`` into ``"https://example.com/"``. The kernel could not
repair either — the caller's value is already gone by the time ``_as_mapping``
sees the object — so the fix lives in the generated annotations
(``packages/codegen``'s ``python-postgen``: ``widenRequestNumbers``,
``plainFormatStrings``).

This module is the standing gate on that agreement. It is deliberately
*differential* rather than golden: it asserts the two routes match each other
for a corpus of payloads, so it keeps holding as the spec moves.
``test_wire_parity.py`` is what pins either route to the Stainless oracle's
absolute bytes.

JSON object key order is not part of the wire contract (the two routes order
keys differently: declaration order vs. the caller's insertion order), so the
comparison is over ``sort_keys=True`` renderings. It is *not* over parsed
objects: ``json.loads("3600") == json.loads("3600.0")`` is ``True`` in Python,
which is exactly the defect this test exists to catch.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any, NamedTuple

import httpx
import pytest
from pydantic import BaseModel

from composio_client import Composio, ProjectAuth
from composio_client._models import (
    SessionCreateBody,
    SessionExecuteBody,
    SessionLinkBody,
    SessionPatchBody,
    SessionProxyExecuteBody,
)

from .conftest import API_KEY, BASE_URL

SESSION_ID = "trs_agreement"


class Payload(NamedTuple):
    """One logical call, to be dispatched twice: as a dict and as a model."""

    id: str
    model: type[BaseModel]
    invoke: Callable[[Composio, Any], object]
    body: dict[str, Any]


def _CREATE(client: Composio, sent: Any) -> object:  # noqa: N802 - reads as a constant at the call sites
    return client.tool_router.session.create(sent)


def _PATCH(client: Composio, sent: Any) -> object:  # noqa: N802
    return client.tool_router.session.patch(SESSION_ID, sent)


def _EXECUTE(client: Composio, sent: Any) -> object:  # noqa: N802
    return client.tool_router.session.execute(SESSION_ID, sent)


def _LINK(client: Composio, sent: Any) -> object:  # noqa: N802
    return client.tool_router.session.link(SESSION_ID, sent)


def _PROXY(client: Composio, sent: Any) -> object:  # noqa: N802
    return client.tool_router.session.proxy_execute(SESSION_ID, sent)


def _ccd(val: dict[str, Any]) -> dict[str, Any]:
    return {
        "endpoint": "/messages",
        "method": "GET",
        "toolkit_slug": "gmail",
        "custom_connection_data": {
            "auth_scheme": "OAUTH2",
            "toolkit_slug": "gmail",
            "val": {"access_token": "tok", **val},
        },
    }


#: The corpus. Every entry names the value shape it defends.
PAYLOADS: list[Payload] = [
    # ---- numbers: a spec `number` must keep the caller's JSON type ----
    Payload("number-int", SessionProxyExecuteBody, _PROXY, _ccd({"expires_in": 3600})),
    Payload("number-float", SessionProxyExecuteBody, _PROXY, _ccd({"expires_in": 3599.5})),
    Payload("number-zero", SessionProxyExecuteBody, _PROXY, _ccd({"expires_in": 0})),
    Payload("number-string", SessionProxyExecuteBody, _PROXY, _ccd({"expires_in": "3600"})),
    # an integer past 2**53, which a float round-trip cannot represent exactly
    Payload("number-big-int", SessionProxyExecuteBody, _PROXY, _ccd({"expires_in": 9007199254740993})),
    # the same contract on a bare `number` on a different endpoint
    Payload(
        "number-workbench-threshold",
        SessionCreateBody,
        _CREATE,
        {"user_id": "u@example.com", "workbench": {"auto_offload_threshold": 20000}},
    ),
    # ---- URLs: `format: uri` must not be normalized ----
    Payload(
        "url-mixed-case-no-trailing-slash",
        SessionProxyExecuteBody,
        _PROXY,
        {
            "endpoint": "/upload",
            "method": "POST",
            "toolkit_slug": "gmail",
            "binary_body": {"url": "HTTPS://Example.COM", "content_type": "application/pdf"},
        },
    ),
    Payload(
        "url-authority-only",
        SessionLinkBody,
        _LINK,
        {"toolkit": "github", "callback_url": "https://example.com", "alias": "gh"},
    ),
    Payload(
        "url-uppercase-path-and-query",
        SessionLinkBody,
        _LINK,
        {"toolkit": "github", "callback_url": "https://Example.COM/CB?State=A%2Fb"},
    ),
    Payload(
        "url-experimental-override",
        SessionCreateBody,
        _CREATE,
        {"user_id": "u@example.com", "experimental": {"link_url_overwrite": "https://Connect.EXAMPLE.com"}},
    ),
    # ---- aliased fields: the spec's non-pythonic wire names ----
    Payload(
        "aliased-oauth2",
        SessionProxyExecuteBody,
        _PROXY,
        {
            "endpoint": "/messages",
            "method": "GET",
            "toolkit_slug": "gmail",
            "custom_connection_data": {
                "auth_scheme": "OAUTH2",
                "toolkit_slug": "gmail",
                "val": {
                    "access_token": "tok",
                    "your_domain": "acme.example.com",
                    "companydomain": "acme-corp",
                    "instance_endpoint": "https://acme.service-now.com",
                    "instance_name": "acme-prod",
                },
            },
        },
    ),
    Payload(
        "aliased-oauth1-redirect-url",
        SessionProxyExecuteBody,
        _PROXY,
        {
            "endpoint": "/1/members/me",
            "method": "GET",
            "toolkit_slug": "trello",
            "custom_connection_data": {
                "auth_scheme": "OAUTH1",
                "toolkit_slug": "trello",
                "val": {
                    "oauth_token": "ot_1",
                    "oauth_token_secret": "ots_1",
                    "redirect_url": "https://Example.COM/callback",
                },
            },
        },
    ),
    # ---- nulls: explicitly set to `None` is JSON null, never a dropped key ----
    Payload("null-top-level", SessionPatchBody, _PATCH, {"multi_account": None}),
    Payload(
        "null-nested",
        SessionPatchBody,
        _PATCH,
        {"manage_connections": {"enable": False, "callback_url": None}},
    ),
    # ---- unknown keys: a field this spec snapshot has not caught up with ----
    Payload(
        "unknown-key-top-level",
        SessionCreateBody,
        _CREATE,
        {"user_id": "u@example.com", "not_in_this_snapshot": {"a": 1}},
    ),
    Payload(
        "unknown-key-nested",
        SessionCreateBody,
        _CREATE,
        {"user_id": "u@example.com", "workbench": {"auto_offload_threshold": 20000, "future_flag": [1, 2]}},
    ),
    # ---- booleans and lists, so the corpus is not only numbers and URLs ----
    Payload(
        "bool-and-list",
        SessionExecuteBody,
        _EXECUTE,
        {
            "tool_slug": "GITHUB_GET_REPO",
            "arguments": {"owner": "composiohq", "repo": "composio", "page": 2},
            "enable_auto_workbench_offload": False,
        },
    ),
]


def _dispatch(payload: Payload, body: Any) -> str:
    """Drive one call and return its request body, rendered key-order-independently."""
    seen: list[bytes] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request.content)
        return httpx.Response(200, json={})

    client = Composio(
        auth=ProjectAuth(API_KEY),
        base_url=BASE_URL,
        max_retries=0,
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )
    try:
        payload.invoke(client, body)
    except Exception:  # noqa: BLE001 - the mock's `{}` never parses; only the request matters
        pass
    finally:
        client.close()

    assert len(seen) == 1, f"{payload.id}: expected exactly one request, got {len(seen)}"
    return json.dumps(json.loads(seen[0]), sort_keys=True)


@pytest.mark.parametrize("payload", PAYLOADS, ids=lambda payload: payload.id)
def test_dict_and_model_bodies_send_identical_wire_bytes(payload: Payload) -> None:
    as_dict = _dispatch(payload, payload.body)
    as_model = _dispatch(payload, payload.model.model_validate(payload.body))
    assert as_model == as_dict


@pytest.mark.parametrize("payload", PAYLOADS, ids=lambda payload: payload.id)
def test_dict_body_is_the_caller_payload_modulo_wire_names(payload: Payload) -> None:
    """Guard against a vacuous pass: the two routes could agree by *both* being
    wrong. The dict route is the one whose values are copied through by
    construction, so pinning it to the caller's literal — modulo the documented
    key renames — makes the agreement above meaningful."""
    sent = json.loads(_dispatch(payload, payload.body))
    assert _rekey(payload.body) == sent


#: The complete non-pythonic wire-name inventory of this surface, duplicated
#: from `test_wire_parity._WIRE_ALIASES` on purpose: if the two ever disagree,
#: one of them is describing a rename that is not happening.
_WIRE_ALIASES = {
    "auth_scheme": "authScheme",
    "toolkit_slug": "toolkitSlug",
    "your_domain": "your-domain",
    "companydomain": "COMPANYDOMAIN",
    "instance_endpoint": "instanceEndpoint",
    "instance_name": "instanceName",
    "redirect_url": "redirectUrl",
}

#: `toolkit_slug` is aliased on a `custom_connection_data` member but is a plain
#: field at the top level of a `proxy_execute` body, so the rekey is scoped.
_UNALIASED_AT_TOP_LEVEL = frozenset({"toolkit_slug"})


def _rekey(value: Any, *, top_level: bool = True) -> Any:
    if isinstance(value, dict):
        return {
            (key if top_level and key in _UNALIASED_AT_TOP_LEVEL else _WIRE_ALIASES.get(key, key)): _rekey(
                item, top_level=False
            )
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_rekey(item, top_level=False) for item in value]
    return value


def test_the_corpus_covers_every_value_shape_it_claims_to() -> None:
    """The corpus is the gate; an entry silently disappearing would weaken it."""
    ids = {payload.id for payload in PAYLOADS}
    assert len(ids) == len(PAYLOADS), "duplicate payload id"
    for shape in ("number-int", "number-float", "url-mixed-case-no-trailing-slash", "null-top-level"):
        assert shape in ids
    # every payload really does reach one of the annotation shapes under test
    rendered = json.dumps([payload.body for payload in PAYLOADS])
    assert "3600" in rendered and "3599.5" in rendered
    assert "HTTPS://Example.COM" in rendered
    assert "null" in rendered
