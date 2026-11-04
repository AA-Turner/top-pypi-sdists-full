"""Nested response fields arrive as models, through the client, at runtime.

The offline gates in `test_type_compatibility.py` compare annotation *strings*
against the frozen oracle. That is what makes a re-flattening to `Any` fail, but
it says nothing about `_construct_response`: the annotations could stay perfect
while the construction path regressed to handing back plain dicts, which is the
symptom issue #30 actually reported. These tests drive real client calls and
assert the runtime type.
"""

from __future__ import annotations

import json
from typing import Annotated, Any

import httpx
import pytest
import respx
from pydantic import BaseModel, ConfigDict

from composio_client import Composio, ProjectAuth
from composio_client._base_client import _ADAPTERS, _adapter, _construct_response
from composio_client.types.mcp.custom_create_response import Commands
from composio_client.types.tool_router.session_create_response import Config, Mcp
from composio_client.types.tool_router.session_toolkits_response import (
    Item,
    ItemConnectedAccount,
    ItemConnectedAccountAuthConfig,
    ItemMeta,
)

from .conftest import BASE_URL

_TR = f"{BASE_URL}/api/v3.1/tool_router/session"

_SESSION_PAYLOAD: dict[str, Any] = {
    "session_id": "sess_1",
    "mcp": {"type": "http", "url": "https://mcp.example.com"},
    "tool_router_tools": [],
    "config": {"user_id": "u", "preload": {"tools": []}, "search": {}, "execute": {}},
    "config_version": 1,
}

# Issue #30's second reproduction: nesting three deep, inside a list element.
_TOOLKITS_PAYLOAD: dict[str, Any] = {
    "current_page": 1,
    "total_items": 1,
    "total_pages": 1,
    "next_cursor": None,
    "items": [
        {
            "slug": "gmail",
            "name": "Gmail",
            "enabled": True,
            "is_no_auth": False,
            "composio_managed_auth_schemes": ["OAUTH2"],
            "meta": {"description": "d", "logo": "https://logo"},
            "connected_account": {
                "id": "ca_1",
                "status": "ACTIVE",
                "user_id": "u_1",
                "created_at": "2026-08-20T00:00:00Z",
                "auth_config": {"id": "ac_1", "auth_scheme": "OAUTH2", "is_composio_managed": True},
            },
        }
    ],
}

_MCP_PAYLOAD: dict[str, Any] = {
    "id": "mcp_1",
    "name": "n",
    "mcp_url": "https://x",
    "allowed_tools": ["A"],
    "auth_config_ids": ["ac_1"],
    "commands": {"claude": "c", "cursor": "cu", "windsurf": "w"},
}


@respx.mock
def test_nested_response_fields_construct_models(client: Composio) -> None:
    respx.post(_TR).mock(return_value=httpx.Response(201, json=_SESSION_PAYLOAD))
    result = client.tool_router.session.create({"user_id": "u@example.com"})

    assert isinstance(result.config, Config)
    assert result.config.user_id == "u"
    assert isinstance(result.mcp, Mcp)
    assert result.mcp.url == "https://mcp.example.com"


@respx.mock
def test_nested_models_inside_list_elements_are_addressable(client: Composio) -> None:
    """`ToolRouterSession.toolkits()` — the path issue #30 says no CI covered."""
    respx.get(f"{_TR}/sess_1/toolkits").mock(return_value=httpx.Response(200, json=_TOOLKITS_PAYLOAD))
    result = client.tool_router.session.toolkits("sess_1")
    item = result.items[0]

    assert isinstance(item, Item)
    assert item.slug == "gmail"
    assert isinstance(item.meta, ItemMeta)
    assert item.meta.logo == "https://logo"
    assert isinstance(item.connected_account, ItemConnectedAccount)
    assert isinstance(item.connected_account.auth_config, ItemConnectedAccountAuthConfig)
    assert item.connected_account.auth_config.id == "ac_1"


@respx.mock
def test_issue_30_mcp_custom_create_reproduction(client: Composio) -> None:
    respx.post(f"{BASE_URL}/api/v3.1/mcp/servers/custom").mock(
        return_value=httpx.Response(200, json=_MCP_PAYLOAD)
    )
    result = client.mcp.custom.create(allowed_tools=["A"], auth_config_ids=["ac_1"], name="n")

    assert isinstance(result.commands, Commands)
    assert result.commands.claude == "c"


@respx.mock
def test_strict_validation_accepts_the_restored_annotations() -> None:
    """Strict mode is the only lever that surfaces an oracle-versus-wire gap.

    On the default path `_construct_response` catches `ValidationError` and
    falls through, so a restored annotation that disagreed with a real payload
    would present as the same silent dict issue #30 reports rather than as a
    rejection any suite would flag.
    """
    strict = Composio(auth=ProjectAuth("k"), base_url=BASE_URL, _strict_response_validation=True)
    respx.get(f"{_TR}/sess_1/toolkits").mock(return_value=httpx.Response(200, json=_TOOLKITS_PAYLOAD))
    result = strict.tool_router.session.toolkits("sess_1")

    assert isinstance(result.items[0], Item)
    assert result.items[0].connected_account.auth_config.id == "ac_1"
    strict.close()


def test_restored_annotations_coerce_only_where_the_oracle_declares_a_union() -> None:
    """The coercion asymmetry the restored annotations newly activate.

    A union field is validated (and so coerced) before the fallback walk; a
    required non-union field is constructed without validation, exactly as
    Stainless 1.43.0 did. Neither is incidental -- both are observable.
    """
    assert _construct_response(5, float | None) == 5.0
    assert _construct_response("7", int) == "7"


@respx.mock
def test_adapters_are_reused_across_items_and_calls(client: Composio) -> None:
    """Memoization has to hold on the path that motivated it.

    A field's annotation is one object on its ``FieldInfo`` and `get_args`
    hands back the cached `__args__`, so every item of a list response presents
    the same annotation objects. If that were not identity-stable the cache
    would miss per item and the memoization would be worthless.
    """
    payload = json.loads(json.dumps(_TOOLKITS_PAYLOAD))
    payload["items"] = [json.loads(json.dumps(payload["items"][0])) for _ in range(50)]
    respx.get(f"{_TR}/sess_1/toolkits").mock(return_value=httpx.Response(200, json=payload))

    client.tool_router.session.toolkits("sess_1")
    after_first = len(_ADAPTERS)
    client.tool_router.session.toolkits("sess_1")

    # 50 items through one response, then the whole response again: neither
    # adds an entry, and the total is per-annotation rather than per-value.
    assert 0 < after_first < 60
    assert len(_ADAPTERS) == after_first


def test_adapter_does_not_share_one_entry_between_reversed_unions() -> None:
    """Cache order must not decide which union member wins.

    Unions compare by member set, so `A | B` and `B | A`
    are equal and hash alike -- but pydantic's smart-union tiebreak reads them
    in order, and `extra="allow"` lets one payload satisfy both. Keyed on the
    annotation, whichever spelling arrived first would answer for both.
    """

    class A(BaseModel):
        model_config = ConfigDict(extra="allow")
        x: int

    class B(BaseModel):
        model_config = ConfigDict(extra="allow")
        x: int

    payload = {"x": 1}
    forward = _adapter(A | B).validate_python(payload)
    reverse = _adapter(B | A).validate_python(payload)

    assert type(forward) is A
    assert type(reverse) is B


def test_adapter_does_not_share_one_entry_between_same_named_classes() -> None:
    """Two distinct classes can share a module and a name, and so a ``repr``."""

    def make() -> type[BaseModel]:
        class Collision(BaseModel):
            model_config = ConfigDict(extra="allow")
            x: int

        return Collision

    first, second = make(), make()

    assert repr(first) == repr(second)
    assert type(_adapter(first | None).validate_python({"x": 1})) is first
    assert type(_adapter(second | None).validate_python({"x": 1})) is second


def test_adapter_memoizes_an_unhashable_annotation_too() -> None:
    """A dynamic `cast_to` through the raw escape hatch can reach this.

    `Annotated` metadata is part of the annotation's hash, so unhashable
    metadata makes the whole annotation unhashable while leaving it something
    pydantic builds a schema for. A `repr` key has no such requirement.
    """
    unhashable = Annotated[int, {"metadata": ["unhashable"]}]

    with pytest.raises(TypeError):
        hash(unhashable)

    assert _adapter(unhashable).validate_python(3) == 3
    assert _adapter(unhashable) is _adapter(unhashable)
