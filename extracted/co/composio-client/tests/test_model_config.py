"""The generated models are lossless: validating a mapping and dumping it again
never drops a field the caller supplied.

This is the precondition for handing a plain-dict request body to the matching
generated model so pydantic applies the wire aliases. The relaxation itself is
applied by the generator (``packages/codegen``'s ``python-postgen``, unit-tested
in the ``codegen`` vitest project); everything here asserts the resulting
property on the committed generated output.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest
from pydantic import BaseModel, RootModel

from composio_client._generated import pydantic_gen as _g
from composio_client._models import SessionCreateBody, SessionProxyExecuteBody


def _variant(suffix: str) -> type[BaseModel]:
    """One ``custom_connection_data`` oneOf variant, by hey-api's name suffix."""

    model: type[BaseModel] = getattr(
        _g, f"PostV31ToolRouterSessionBySessionIdProxyExecuteCustomConnectionData{suffix}"
    )
    return model


# Every ``authScheme`` literal in the 11-variant ``custom_connection_data``
# oneOf, with the minimum ``val`` its variant requires, and the generated
# variant class the union must resolve to.
CONNECTION_VARIANTS = [
    ("OAUTH2", {"access_token": "t"}, _variant("")),
    ("DCR_OAUTH", {"client_id": "c", "access_token": "t"}, _variant("_")),
    ("API_KEY", {}, _variant("_2")),
    ("BASIC_WITH_JWT", {"username": "u", "password": "p"}, _variant("_3")),
    ("BASIC", {"username": "u"}, _variant("_4")),
    ("BEARER_TOKEN", {"token": "t"}, _variant("_5")),
    ("OAUTH1", {"oauth_token": "t", "oauth_token_secret": "s"}, _variant("_6")),
    ("NO_AUTH", {}, _variant("_7")),
    ("SERVICE_ACCOUNT", {"application_id": "a", "installation_id": "i", "private_key": "k"}, _variant("_8")),
    ("GOOGLE_SERVICE_ACCOUNT", {"credentials_json": "{}"}, _variant("_9")),
    ("S2S_OAUTH2", {"access_token": "t"}, _variant("_10")),
]
VARIANT_IDS = [scheme for scheme, _, _ in CONNECTION_VARIANTS]


def _round_trip(model: type[BaseModel], payload: dict[str, object]) -> dict[str, object]:
    """Validate then dump exactly the way the kernel serializes a body."""

    dumped = model.model_validate(payload).model_dump(mode="json", by_alias=True, exclude_unset=True)
    assert isinstance(dumped, dict)
    return dumped


# ---- losslessness of the body round-trip ----


def test_proxy_execute_body_round_trip_is_lossless() -> None:
    payload = {
        "endpoint": "/e",
        "method": "GET",
        "toolkit_slug": "gmail",
        "brand_new_field": "keep-me",
        "body": None,
        "custom_connection_data": {
            "authScheme": "OAUTH2",
            "toolkitSlug": "gmail",
            "val": {"access_token": "t", "unknown_val_key": "keep"},
        },
    }

    dumped = _round_trip(SessionProxyExecuteBody, payload)

    assert dumped == payload
    # `body` was explicitly set to None, so it stays as a JSON null...
    assert "body" in dumped
    # ...while a field that was never set is omitted entirely.
    assert "parameters" not in dumped


def test_unknown_top_level_key_is_preserved() -> None:
    dumped = _round_trip(
        SessionProxyExecuteBody,
        {"endpoint": "/e", "method": "GET", "toolkit_slug": "gmail", "brand_new_field": "keep-me"},
    )

    assert dumped["brand_new_field"] == "keep-me"


def test_unknown_nested_key_is_preserved() -> None:
    dumped = _round_trip(
        SessionProxyExecuteBody,
        {
            "endpoint": "/e",
            "method": "GET",
            "toolkit_slug": "gmail",
            "custom_connection_data": {
                "authScheme": "OAUTH2",
                "toolkitSlug": "gmail",
                "brand_new_wrapper_key": "keep-wrapper",
                "val": {"access_token": "t", "brand_new_val_key": "keep-val"},
            },
        },
    )

    connection = dumped["custom_connection_data"]
    assert isinstance(connection, dict)
    assert connection["brand_new_wrapper_key"] == "keep-wrapper"
    assert connection["val"]["brand_new_val_key"] == "keep-val"


def test_unknown_key_is_preserved_where_the_spec_said_additional_properties_false() -> None:
    """``additionalProperties: false`` used to compile to ``extra="forbid"``,
    which rejected the payload outright."""

    dumped = _round_trip(
        SessionCreateBody,
        {"user_id": "u", "toolkits": {"enable": ["gmail"], "brand_new_key": "keep-me"}},
    )

    toolkits = dumped["toolkits"]
    assert isinstance(toolkits, dict)
    assert toolkits == {"enable": ["gmail"], "brand_new_key": "keep-me"}


def test_explicit_none_is_kept_and_unset_fields_are_omitted() -> None:
    dumped = _round_trip(
        SessionProxyExecuteBody,
        {"endpoint": "/e", "method": "GET", "toolkit_slug": "gmail", "body": None},
    )

    assert dumped["body"] is None
    assert set(dumped) == {"endpoint", "method", "toolkit_slug", "body"}


# ---- wire aliases ----


def test_wire_aliases_are_applied_on_dump() -> None:
    dumped = _round_trip(
        SessionProxyExecuteBody,
        {
            "endpoint": "/e",
            "method": "GET",
            "toolkit_slug": "gmail",
            "custom_connection_data": {
                "auth_scheme": "OAUTH2",
                "toolkit_slug": "gmail",
                "val": {"access_token": "t", "your_domain": "acme.example.com"},
            },
        },
    )

    connection = dumped["custom_connection_data"]
    assert isinstance(connection, dict)
    # `populate_by_name` accepted the snake_case Python names on input, and
    # `by_alias` restored the wire spelling on output.
    assert connection["authScheme"] == "OAUTH2"
    assert connection["toolkitSlug"] == "gmail"
    assert connection["val"]["your-domain"] == "acme.example.com"
    assert "auth_scheme" not in connection
    assert "your_domain" not in connection["val"]


def test_wire_aliases_are_accepted_on_input() -> None:
    dumped = _round_trip(
        SessionProxyExecuteBody,
        {
            "endpoint": "/e",
            "method": "GET",
            "toolkit_slug": "gmail",
            "custom_connection_data": {
                "authScheme": "OAUTH2",
                "toolkitSlug": "gmail",
                "val": {"access_token": "t", "your-domain": "acme.example.com"},
            },
        },
    )

    connection = dumped["custom_connection_data"]
    assert isinstance(connection, dict)
    assert connection["val"]["your-domain"] == "acme.example.com"


# ---- union resolution is still discriminated by `authScheme` ----


@pytest.mark.parametrize(("scheme", "val", "expected"), CONNECTION_VARIANTS, ids=VARIANT_IDS)
def test_connection_data_variant_resolution(
    scheme: str, val: dict[str, str], expected: type[BaseModel]
) -> None:
    """``extra="allow"`` widens what each variant accepts, so a payload could in
    principle match a sibling variant. The single-member ``authScheme`` enum
    keeps every variant disjoint; assert that for all 11."""

    body = SessionProxyExecuteBody.model_validate(
        {
            "endpoint": "/e",
            "method": "GET",
            "toolkit_slug": "gmail",
            "custom_connection_data": {"authScheme": scheme, "toolkitSlug": "gmail", "val": val},
        }
    )

    assert type(body.custom_connection_data) is expected


@pytest.mark.parametrize(("scheme", "val", "expected"), CONNECTION_VARIANTS, ids=VARIANT_IDS)
def test_connection_data_variant_resolution_with_unknown_keys(
    scheme: str, val: dict[str, str], expected: type[BaseModel]
) -> None:
    """Unknown keys must not tip a payload into a different variant either."""

    body = SessionProxyExecuteBody.model_validate(
        {
            "endpoint": "/e",
            "method": "GET",
            "toolkit_slug": "gmail",
            "custom_connection_data": {
                "authScheme": scheme,
                "toolkitSlug": "gmail",
                "brand_new_wrapper_key": "keep",
                "val": {**val, "brand_new_val_key": "keep"},
            },
        }
    )

    assert type(body.custom_connection_data) is expected
    dumped = body.model_dump(mode="json", by_alias=True, exclude_unset=True)
    connection = dumped["custom_connection_data"]
    assert connection["brand_new_wrapper_key"] == "keep"
    assert connection["val"]["brand_new_val_key"] == "keep"


# ---- the invariant, over the whole generated module ----


def test_every_generated_basemodel_is_relaxed() -> None:
    checked = 0
    for name, obj in vars(_g).items():
        if not (isinstance(obj, type) and issubclass(obj, BaseModel)) or issubclass(obj, RootModel):
            continue
        if obj is BaseModel:
            continue
        assert obj.model_config.get("extra") == "allow", name
        assert obj.model_config.get("populate_by_name") is True, name
        checked += 1
    assert checked > 200


def test_root_models_do_not_set_extra() -> None:
    """Pydantic raises ``PydanticUserError`` for ``model_config["extra"]`` on a
    ``RootModel``; the fixer has to leave them alone (importing this module at
    all is most of the proof)."""

    root_models = [
        obj
        for obj in vars(_g).values()
        if isinstance(obj, type) and issubclass(obj, RootModel) and obj is not RootModel
    ]

    assert len(root_models) == 16
    for model in root_models:
        assert "extra" not in model.model_config


# ---- the committed module, at full-spec width ----
#
# The repairs themselves are the generator's now (`packages/codegen`'s
# `python-postgen` suite). What is still a *Python* claim is what the committed
# module says, which is what these two read.


def _classes_declaring_a_field_twice(tree: ast.Module) -> dict[str, list[str]]:
    """Every class in ``tree`` that annotates one field name more than once."""
    duplicates: dict[str, list[str]] = {}
    for cls in tree.body:
        if not isinstance(cls, ast.ClassDef):
            continue
        names = [
            node.target.id
            for node in cls.body
            if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)
        ]
        repeated = sorted({name for name in names if names.count(name) > 1})
        if repeated:
            duplicates[cls.name] = repeated
    return duplicates


def test_no_generated_class_declares_a_field_name_twice() -> None:
    """The guard `_LEGACY_PROPERTY_NAMES` exists for.

    hey-api's Python name normalizer can map a camelCase wire alias onto the
    same field name as its snake_case sibling, and a duplicate `AnnAssign`
    is *silent*: the later one simply wins and the earlier field is gone. The
    rename table disambiguates the five collisions the spec produces, and this
    asserts there is no sixth.
    """
    tree = ast.parse(Path(_g.__file__).read_text())

    assert _classes_declaring_a_field_twice(tree) == {}


def test_a_legacy_alias_outside_tool_router_round_trips_through_its_wire_name() -> None:
    """The rename is a *Python* name change only — the wire alias survives.

    `PostV31InternalTriggerLogsDataMeta` is a trigger-log response model, well
    outside the `tool_router` surface the rename table was derived from, and it
    carries two of the five renamed aliases.
    """
    payload = {
        "id": "log_1",
        "type": "trigger",
        "createdAt": "2026-08-07T00:00:00Z",
        "updatedAt": "2026-08-07T00:00:01Z",
        "provider": "github",
        "clientId": "client_1",
        "connectionId": "conn_1",
        "triggerName": "GITHUB_STAR_ADDED",
    }

    model = _g.PostV31InternalTriggerLogsDataMeta.model_validate(payload)

    assert model.deprecated_updated_at == "2026-08-07T00:00:01Z"
    assert model.deprecated_trigger_name == "GITHUB_STAR_ADDED"
    assert model.model_dump(by_alias=True, exclude_unset=True) == payload
