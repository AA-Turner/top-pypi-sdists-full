"""Strata-3 tests: method wiring — the right HTTP verb, URL, body, and query
reach the kernel, and the response parses into the aliased model. Representative
coverage across POST-with-body, GET-with-query, nested mount paths, optional
bodies, RootModel responses, path encoding, and the async client.
"""

from __future__ import annotations

import json
from typing import Annotated, Literal, Optional

import httpx
import pytest
import respx

from composio_client import AsyncComposio, Composio
from composio_client._base_client import _construct_response, _discriminated_variant, _literal_annotation
from composio_client.types.tool_router.session_config_history_response import (
    ItemConfigToolkitsRequireApproval,
    SessionConfigHistoryResponse,
)
from composio_client.types.tool_router.session_create_response import (
    ConfigToolkitsDisabled,
    ConfigToolkitsEnabled,
    ConfigToolkitsRequireApproval,
    ConfigToolsEnabled,
    ConfigToolsRequireApproval,
    ConfigToolsTags,
    SessionCreateResponse,
)
from composio_client.types.tool_router.session_execute_meta_response import SessionExecuteMetaBlockedResponse
from composio_client.types.tool_router.session_execute_response import (
    CurrentSessionExecuteInputRequiredResponseInputRequestsValue,
    SessionExecuteBlockedResponse,
    SessionExecuteInputRequiredResponse,
    SessionExecuteResponse,
    SessionExecuteResult,
)
from composio_client.types.tool_router.session_proxy_execute_response import (
    CurrentSessionProxyExecuteInputRequiredResponseInputRequestsValue,
    SessionProxyExecuteBlockedResponse,
    SessionProxyExecuteInputRequiredResponse,
    SessionProxyExecuteResponse,
    SessionProxyExecuteResult,
)

from .conftest import BASE_URL

_TR = f"{BASE_URL}/api/v3.1/tool_router/session"

# A response payload valid against the (strict) generated create/attach models.
_SESSION_PAYLOAD = {
    "session_id": "sess_1",
    "mcp": {"type": "http", "url": "https://mcp.example.com"},
    "tool_router_tools": [],
    "config": {"user_id": "u", "preload": {"tools": []}, "search": {}, "execute": {}},
    "config_version": 1,
}

_HOOKS = [
    {
        "type": "before_execute",
        "id": "policy",
        "applies_to": "all",
        "handler": {"type": "condition_check", "condition": "Sending external email", "action": "block"},
    },
    {
        "type": "after_execute",
        "id": "injection",
        "applies_to": {"toolkits": ["gmail"]},
        "handler": {"type": "prompt_injection_check", "action": "block"},
    },
]
_HOOK_WRITES = [
    ("create", (), {"user_id": "u"}, "post", _TR, 201),
    ("patch", ("sess_1",), {}, "patch", f"{_TR}/sess_1", 200),
]


@respx.mock
@pytest.mark.parametrize(("operation", "args", "kwargs", "method", "url", "status"), _HOOK_WRITES)
def test_session_writes_serialize_iterable_hooks(
    client: Composio, operation: str, args: tuple, kwargs: dict, method: str, url: str, status: int
) -> None:
    route = getattr(respx, method)(url).mock(return_value=httpx.Response(status, json=_SESSION_PAYLOAD))
    getattr(client.tool_router.session, operation)(*args, **kwargs, hooks=iter(_HOOKS))
    assert json.loads(route.calls.last.request.content)["hooks"] == _HOOKS


@respx.mock
@pytest.mark.parametrize(("operation", "args", "kwargs", "method", "url", "status"), _HOOK_WRITES)
async def test_async_session_writes_serialize_iterable_hooks(
    async_client: AsyncComposio, operation: str, args: tuple, kwargs: dict, method: str, url: str, status: int
) -> None:
    route = getattr(respx, method)(url).mock(return_value=httpx.Response(status, json=_SESSION_PAYLOAD))
    await getattr(async_client.tool_router.session, operation)(
        *args, **kwargs, hooks=(hook for hook in _HOOKS)
    )
    assert json.loads(route.calls.last.request.content)["hooks"] == _HOOKS


@respx.mock
def test_session_create_posts_body(client: Composio) -> None:
    route = respx.post(_TR).mock(return_value=httpx.Response(201, json=_SESSION_PAYLOAD))
    result = client.tool_router.session.create({"user_id": "u@example.com"})
    assert result.session_id == "sess_1"
    request = route.calls.last.request
    assert request.method == "POST"
    assert request.read() == b'{"user_id":"u@example.com"}'


@respx.mock
def test_session_execute_posts_to_nested_path(client: Composio) -> None:
    route = respx.post(f"{_TR}/sess_1/execute").mock(
        return_value=httpx.Response(200, json={"data": {"result": 1}, "log_id": "log_9"})
    )
    result = client.tool_router.session.execute("sess_1", {"tool_slug": "GITHUB_X", "arguments": {}})
    assert result.log_id == "log_9"
    assert route.calls.last.request.read() == b'{"tool_slug":"GITHUB_X","arguments":{}}'


_INPUT_REQUIRED = {
    "result_type": "input_required",
    "input_requests": {
        "approval": {
            "type": "elicitation",
            "mode": "form",
            "message": "Approve?",
            "requested_schema": {"type": "object"},
        }
    },
    "request_state": "state_1",
}
_EXECUTE_BODY = {"tool_slug": "GITHUB_X", "arguments": {}}
_PROXY_BODY = {"endpoint": "/messages", "method": "GET", "toolkit_slug": "gmail"}


@respx.mock
@pytest.mark.parametrize(
    ("operation", "body", "response_class"),
    [
        ("execute", _EXECUTE_BODY, SessionExecuteBlockedResponse),
        (
            "execute_meta",
            {"slug": "COMPOSIO_SEARCH_TOOLS", "arguments": {}},
            SessionExecuteMetaBlockedResponse,
        ),
        ("proxy_execute", _PROXY_BODY, SessionProxyExecuteBlockedResponse),
    ],
)
def test_session_blocked_outcomes_expose_reason_and_hook_results(
    client: Composio, operation: str, body: dict, response_class: type
) -> None:
    payload = {
        "result_type": "blocked",
        "reason": {"type": "request_blocked", "hook_id": "policy"},
        "message": "Blocked by session policy",
        "hook_results": [
            {"id": "policy", "status": "evaluated", "outcome": "block"},
            {"id": "other", "status": "unavailable"},
        ],
    }
    respx.post(f"{_TR}/sess_1/{operation}").mock(return_value=httpx.Response(200, json=payload))
    result = getattr(client.tool_router.session, operation)("sess_1", body)
    assert type(result) is response_class
    assert result.reason.type == "request_blocked"
    assert result.reason.hook_id == "policy"
    assert result.hook_results[0].outcome == "block"
    assert result.hook_results[1].status == "unavailable"
    assert result.to_dict() == payload


@respx.mock
@pytest.mark.parametrize(
    ("payload", "result_type"),
    [
        ({"result_type": "completed", "data": {"ok": 1}, "error": None, "log_id": "log_1"}, "completed"),
        ({"result_type": "failed", "data": {}, "error": "boom", "log_id": "log_2"}, "failed"),
        # A server that predates the tag answers the legacy class too.
        ({"data": {"ok": 1}, "error": None, "log_id": "log_3"}, None),
    ],
)
def test_session_execute_answers_the_legacy_class_for_completed_failed_and_untagged(
    client: Composio, payload: dict[str, object], result_type: str | None
) -> None:
    respx.post(f"{_TR}/sess_1/execute").mock(return_value=httpx.Response(200, json=payload))
    result = client.tool_router.session.execute("sess_1", _EXECUTE_BODY)
    assert type(result) is SessionExecuteResponse
    assert result.result_type == result_type
    assert result.log_id == payload["log_id"]


@respx.mock
def test_session_execute_input_required_exposes_its_requests(client: Composio) -> None:
    respx.post(f"{_TR}/sess_1/execute").mock(return_value=httpx.Response(200, json=_INPUT_REQUIRED))
    result = client.tool_router.session.execute("sess_1", _EXECUTE_BODY)
    assert type(result) is SessionExecuteInputRequiredResponse
    assert result.result_type == "input_required"
    request = result.input_requests["approval"]
    assert type(request) is CurrentSessionExecuteInputRequiredResponseInputRequestsValue
    assert request.message == "Approve?"
    assert result.request_state == "state_1"


@respx.mock
@pytest.mark.parametrize(
    ("payload", "result_type"),
    [
        ({"result_type": "completed", "data": {}, "status": 200, "headers": {}}, "completed"),
        ({"data": {}, "status": 200, "headers": {}}, None),
    ],
)
def test_session_proxy_execute_answers_the_legacy_class_for_completed_and_untagged(
    client: Composio, payload: dict[str, object], result_type: str | None
) -> None:
    respx.post(f"{_TR}/sess_1/proxy_execute").mock(return_value=httpx.Response(200, json=payload))
    result = client.tool_router.session.proxy_execute("sess_1", _PROXY_BODY)
    assert type(result) is SessionProxyExecuteResponse
    assert result.result_type == result_type
    assert result.status == 200


@respx.mock
def test_session_proxy_execute_input_required_exposes_its_requests(client: Composio) -> None:
    respx.post(f"{_TR}/sess_1/proxy_execute").mock(return_value=httpx.Response(200, json=_INPUT_REQUIRED))
    result = client.tool_router.session.proxy_execute("sess_1", _PROXY_BODY)
    assert type(result) is SessionProxyExecuteInputRequiredResponse
    request = result.input_requests["approval"]
    assert type(request) is CurrentSessionProxyExecuteInputRequiredResponseInputRequestsValue
    assert request.requested_schema == {"type": "object"}
    assert result.request_state == "state_1"


@pytest.mark.parametrize(
    ("union", "payload", "variant"),
    [
        # Each payload fails validation against every member, so the class is
        # chosen by the tag alone -- or, with no tag, by the legacy member
        # standing first in the union.
        (SessionExecuteResult, {"result_type": "input_required"}, SessionExecuteInputRequiredResponse),
        (SessionExecuteResult, {"result_type": "blocked"}, SessionExecuteBlockedResponse),
        (SessionExecuteResult, {"result_type": "completed", "data": {}}, SessionExecuteResponse),
        (SessionExecuteResult, {"result_type": "failed", "error": "boom"}, SessionExecuteResponse),
        (SessionExecuteResult, {"data": {}}, SessionExecuteResponse),
        (
            SessionProxyExecuteResult,
            {"result_type": "input_required", "status": 200},
            SessionProxyExecuteInputRequiredResponse,
        ),
        (SessionProxyExecuteResult, {"result_type": "completed", "data": {}}, SessionProxyExecuteResponse),
        (SessionProxyExecuteResult, {"result_type": "blocked"}, SessionProxyExecuteBlockedResponse),
        (SessionProxyExecuteResult, {"data": {}}, SessionProxyExecuteResponse),
    ],
)
def test_a_malformed_execute_payload_is_still_the_class_its_tag_names(
    union: object, payload: dict[str, object], variant: type
) -> None:
    result = _construct_response(payload, union)
    assert type(result) is variant
    assert result.result_type == payload.get("result_type")
    assert result.to_dict() == payload


def test_the_legacy_execute_class_is_constructible_and_subclassable() -> None:
    """What the downstream SDK does with the name: call it, and inherit from it."""

    class Mine(SessionExecuteResponse):
        extra_field: str = "mine"

    built = SessionExecuteResponse(data={}, log_id="l")
    assert built.result_type is None
    assert Mine(data={"a": 1}, log_id="l").extra_field == "mine"
    assert issubclass(Mine, SessionExecuteResponse)


def test_literal_annotation_sees_through_optional_and_annotated() -> None:
    tag = Literal["completed", "failed"]
    assert _literal_annotation(tag) == tag
    # Both spellings: `Optional[...]` is a `typing.Union`, `X | None` a `types.UnionType`.
    assert _literal_annotation(Optional[tag]) == tag  # noqa: UP045
    assert _literal_annotation(tag | None) == tag
    assert _literal_annotation(Annotated[Optional[tag], "meta"]) == tag  # noqa: UP045
    # A real two-member union is not a tag and is left alone.
    assert _literal_annotation(tag | int) == tag | int
    assert _literal_annotation(str | None) is str


def test_an_optional_tag_selects_its_variant_and_an_absent_one_selects_none() -> None:
    assert _discriminated_variant(SessionExecuteResult, {"result_type": "failed"}) is SessionExecuteResponse
    assert (
        _discriminated_variant(SessionExecuteResult, {"result_type": "input_required"})
        is SessionExecuteInputRequiredResponse
    )
    assert _discriminated_variant(SessionExecuteResult, {"data": {}}) is None
    assert _discriminated_variant(SessionExecuteResult, {"result_type": None}) is None


def _session_with(**config: object) -> dict[str, object]:
    return {**_SESSION_PAYLOAD, "config": {**_SESSION_PAYLOAD["config"], **config}}


@pytest.mark.parametrize(
    ("toolkits", "variant"),
    [
        ({"require_approval": ["github"]}, ConfigToolkitsRequireApproval),
        ({"enabled": ["github"]}, ConfigToolkitsEnabled),
        # A captured variant that also carries the optional field stays itself.
        ({"enabled": ["github"], "require_approval": ["github"]}, ConfigToolkitsEnabled),
        ({"disabled": ["slack"], "require_approval": ["github"]}, ConfigToolkitsDisabled),
    ],
)
def test_session_config_toolkits_construct_the_variant_their_fields_name(
    toolkits: dict[str, list[str]], variant: type
) -> None:
    session = _construct_response(_session_with(toolkits=toolkits), SessionCreateResponse)
    assert type(session.config.toolkits) is variant
    assert session.config.toolkits.to_dict() == toolkits
    assert session.config.toolkits.require_approval == toolkits.get("require_approval")


def test_an_approval_only_toolkits_payload_has_no_enabled_attribute_to_mislead() -> None:
    """The defect: this payload was a `ConfigToolkitsEnabled` with no `enabled`."""
    session = _construct_response(
        _session_with(toolkits={"require_approval": ["github"]}), SessionCreateResponse
    )
    assert session.config.toolkits.require_approval == ["github"]
    assert not isinstance(session.config.toolkits, ConfigToolkitsEnabled)
    assert not hasattr(session.config.toolkits, "enabled")


def test_session_config_tools_values_construct_the_variant_their_fields_name() -> None:
    tools = {
        "github": {"require_approval": ["GITHUB_DELETE_A_REPOSITORY"]},
        "gmail": {"enabled": ["GMAIL_SEND_EMAIL"]},
        "slack": {"tags": {"enabled": ["readOnlyHint"]}, "require_approval": ["SLACK_X"]},
    }
    session = _construct_response(_session_with(tools=tools), SessionCreateResponse)
    assert {slug: type(value) for slug, value in session.config.tools.items()} == {
        "github": ConfigToolsRequireApproval,
        "gmail": ConfigToolsEnabled,
        "slack": ConfigToolsTags,
    }
    assert session.config.tools["github"].require_approval == ["GITHUB_DELETE_A_REPOSITORY"]


def test_config_history_items_construct_the_approval_only_variant() -> None:
    item = {
        "config": {**_SESSION_PAYLOAD["config"], "toolkits": {"require_approval": ["github"]}},
        "created_at": "2026-10-07T00:00:00Z",
        "is_current": True,
        "version": 1,
    }
    history = _construct_response(
        {"items": [item], "total_pages": 1, "current_page": 1, "total_items": 1},
        SessionConfigHistoryResponse,
    )
    assert type(history.items[0].config.toolkits) is ItemConfigToolkitsRequireApproval


@respx.mock
def test_session_create_returns_and_sends_the_approval_only_variants(client: Composio) -> None:
    route = respx.post(_TR).mock(
        return_value=httpx.Response(201, json=_session_with(toolkits={"require_approval": ["github"]}))
    )
    result = client.tool_router.session.create(
        user_id="u",
        toolkits={"require_approval": ["github"]},
        tools={"github": {"require_approval": ["GITHUB_DELETE_A_REPOSITORY"]}},
    )
    assert type(result.config.toolkits) is ConfigToolkitsRequireApproval
    assert json.loads(route.calls.last.request.read()) == {
        "user_id": "u",
        "toolkits": {"require_approval": ["github"]},
        "tools": {"github": {"require_approval": ["GITHUB_DELETE_A_REPOSITORY"]}},
    }


@respx.mock
def test_session_patch_sends_the_approval_only_variants(client: Composio) -> None:
    route = respx.patch(f"{_TR}/sess_1").mock(return_value=httpx.Response(200, json=_SESSION_PAYLOAD))
    client.tool_router.session.patch("sess_1", toolkits={"require_approval": ["github"]})
    assert json.loads(route.calls.last.request.read()) == {"toolkits": {"require_approval": ["github"]}}


@respx.mock
def test_session_config_history_serializes_query_and_exposes_stainless_fields(client: Composio) -> None:
    body = {"items": [], "total_pages": 1, "current_page": 1, "total_items": 0}
    route = respx.get(f"{_TR}/sess_1/config_history").mock(return_value=httpx.Response(200, json=body))
    result = client.tool_router.session.config_history("sess_1", query={"cursor": "c1", "limit": 25})
    assert result.total_items == 0
    params = route.calls.last.request.url.params
    assert params.get("cursor") == "c1"
    assert params.get("limit") == "25"


@respx.mock
def test_session_attach_sends_empty_body_when_omitted(client: Composio) -> None:
    route = respx.post(f"{_TR}/sess_1/attach").mock(return_value=httpx.Response(200, json=_SESSION_PAYLOAD))
    client.tool_router.session.attach("sess_1")
    assert route.calls.last.request.read() == b"{}"


@respx.mock
def test_files_list_uses_nested_mount_path(client: Composio) -> None:
    route = respx.get(f"{_TR}/sess_1/mounts/mount_1/items").mock(
        return_value=httpx.Response(200, json={"items": []})
    )
    result = client.tool_router.session.files.list("sess_1", "mount_1")
    assert result.items == []
    assert route.calls.last.request.url.path == "/api/v3.1/tool_router/session/sess_1/mounts/mount_1/items"


@respx.mock
def test_files_delete_sends_the_body(client: Composio) -> None:
    route = respx.post(f"{_TR}/sess_1/mounts/mount_1/delete").mock(
        return_value=httpx.Response(
            200, json={"mount_relative_path": "/f.txt", "sandbox_mount_prefix": "/mnt"}
        )
    )
    result = client.tool_router.session.files.delete("sess_1", "mount_1", {"mount_relative_path": "/f.txt"})
    assert result.mount_relative_path == "/f.txt"
    assert route.calls.last.request.read() == b'{"mount_relative_path":"/f.txt"}'


@pytest.mark.parametrize("method", ["delete", "create_download_url", "create_upload_url"])
def test_the_mount_write_methods_require_a_body(client: Composio, method: str) -> None:
    """The spec requires ``mount_relative_path`` on all three, and so does the
    Stainless Python client this package succeeds — ``mount_relative_path: str``
    with no ``Omit`` default, on all three. The handwritten MVP defaulted the
    body to ``{}`` on this one family, which made an unsatisfiable request easy
    to write by accident; generation from the shared plan restores the oracle's
    shape.

    The wire-parity corpus cannot cover this: every one of its mount cases
    passes an explicit body, and it structurally could not record the
    omitted-body call because the oracle refuses to make it.
    """
    with pytest.raises(TypeError):
        getattr(client.tool_router.session.files, method)("sess_1", "mount_1")


@respx.mock
def test_proxy_execute_dict_body_is_aliased_by_its_request_model(client: Composio) -> None:
    """`session.proxy_execute` is the only method on this surface whose body has
    aliased fields; a dict body must reach the wire in the spec's spelling."""
    route = respx.post(f"{_TR}/sess_1/proxy_execute").mock(
        return_value=httpx.Response(200, json={"data": {}, "status": 200, "headers": {}})
    )
    client.tool_router.session.proxy_execute(
        "sess_1",
        {
            "endpoint": "/messages",
            "method": "GET",
            "toolkit_slug": "gmail",
            "custom_connection_data": {
                "auth_scheme": "OAUTH2",
                "toolkit_slug": "gmail",
                "val": {"access_token": "t", "your_domain": "acme.example.com"},
            },
        },
    )
    sent = json.loads(route.calls.last.request.read())
    connection = sent["custom_connection_data"]
    assert connection["authScheme"] == "OAUTH2"
    assert connection["toolkitSlug"] == "gmail"
    assert connection["val"]["your-domain"] == "acme.example.com"
    # unaliased fields keep their spelling
    assert sent["toolkit_slug"] == "gmail"


@respx.mock
def test_proxy_execute_aliases_resolve_per_variant_not_across_the_union(
    client: Composio,
) -> None:
    """Pinned divergence from Stainless, deliberate.

    ``custom_connection_data`` is an 11-member ``oneOf`` discriminated by
    ``authScheme``, and ``redirect_url``/``redirectUrl`` is declared on the
    OAUTH1 member only. We resolve the member first and rename against *its*
    fields, so ``redirect_url`` inside an OAUTH2 connection is not a known
    field and is forwarded verbatim (``extra='allow'``).

    Stainless renames it anyway: ``maybe_transform`` walks the whole union's
    unchecked TypedDicts and applies any alias it finds a key for, without
    discriminating, so it emits ``redirectUrl`` on a connection whose schema
    does not define the field. Matching that would mean contradicting the spec
    to reproduce a quirk, and it is only reachable with a body the spec already
    rejects — so we keep per-variant resolution and pin the difference here.
    """
    route = respx.post(f"{_TR}/sess_1/proxy_execute").mock(
        return_value=httpx.Response(200, json={"data": {}, "status": 200, "headers": {}})
    )
    client.tool_router.session.proxy_execute(
        "sess_1",
        {
            "endpoint": "/messages",
            "method": "GET",
            "toolkit_slug": "gmail",
            "custom_connection_data": {
                "auth_scheme": "OAUTH2",
                "toolkit_slug": "gmail",
                # OAUTH1-only field, so unknown to the resolved OAUTH2 member
                "val": {"access_token": "t", "redirect_url": "https://example.com/cb"},
            },
        },
    )
    val = json.loads(route.calls.last.request.read())["custom_connection_data"]["val"]
    assert val["redirect_url"] == "https://example.com/cb"
    assert "redirectUrl" not in val
    # the members the variant *does* declare are still renamed
    assert json.loads(route.calls.last.request.read())["custom_connection_data"]["authScheme"] == "OAUTH2"


@respx.mock
def test_path_params_are_percent_encoded(client: Composio) -> None:
    body = {"items": [], "total_pages": 1, "current_page": 1, "total_items": 0}
    route = respx.get(url__regex=rf"{_TR}/.+/config_history").mock(
        return_value=httpx.Response(200, json=body)
    )
    client.tool_router.session.config_history("a b/c")
    # space and slash both percent-encoded into a single path segment
    assert "a%20b%2Fc" in str(route.calls.last.request.url)


@respx.mock
async def test_async_execute(async_client: AsyncComposio) -> None:
    route = respx.post(f"{_TR}/sess_1/execute").mock(
        return_value=httpx.Response(200, json={"data": {}, "log_id": "log_async"})
    )
    result = await async_client.tool_router.session.execute("sess_1", {"tool_slug": "X", "arguments": {}})
    assert result.log_id == "log_async"
    assert route.calls.last.request.method == "POST"
    await async_client.aclose()
