# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the masking of a connector run's output."""

from __future__ import annotations

import hashlib
import hmac
import json
import re

import pytest
from airbyte_protocol.models import (
    AirbyteMessage,
    AirbyteStream,
    ConfiguredAirbyteCatalog,
    ConfiguredAirbyteStream,
    DestinationSyncMode,
    SyncMode,
)

from airbyte_ops_mcp.regression_tests.masking import (
    MASKED_TEXT_PREFIX,
    MaskPolicy,
    StreamMaskInfo,
    mask_all_values,
    mask_input_state,
    mask_line,
    mask_message,
    mask_record_data,
    mask_state,
    mask_text,
    mask_text_line,
    mask_value,
    type_of_token,
    typed_record_from_tokens,
)
from airbyte_ops_mcp.regression_tests.regression.comparators import _extract_pk_tuple

pytestmark = pytest.mark.unit

TOKEN = re.compile(r"^(string|integer|number|array|object)_len-\d+_[0-9a-f]{16}$")

# A fixed key for the tests, never a real run's: tokens pair only under one
# key, so every expectation here is computed under this one. The other key
# stands in for another run.
KEY = bytes(range(32))
OTHER_KEY = bytes(range(32, 64))


# ---------------------------------------------------------------------------
# Tokens
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "value,prefix",
    [
        pytest.param("hello", "string_len-5_", id="string"),
        pytest.param(12345, "integer_len-5_", id="integer"),
        pytest.param(1.5, "number_len-3_", id="number"),
        pytest.param([1, 2, 3], "array_len-3_", id="array"),
        pytest.param({"a": 1, "b": 2}, "object_len-2_", id="object"),
    ],
)
def test_a_token_keeps_the_type_and_the_length(value, prefix) -> None:
    token = mask_value(value, key=KEY)

    assert token.startswith(prefix)
    assert TOKEN.match(token)


def test_booleans_are_their_own_type_not_integers() -> None:
    """`True` is an `int` to `isinstance`; it must not mask as one."""
    assert mask_value(True, key=KEY).startswith("boolean_")
    assert mask_value(False, key=KEY).startswith("boolean_")
    assert mask_value(1, key=KEY) != mask_value(True, key=KEY)


def test_a_null_stays_a_null() -> None:
    """The comparison tests a missing primary key with `is None`."""
    assert mask_value(None, key=KEY) is None
    assert mask_all_values({"a": None, "b": 1}, key=KEY) == {
        "a": None,
        "b": mask_value(1, key=KEY),
    }


@pytest.mark.parametrize(
    "token,typed",
    [
        pytest.param(mask_value("hello", key=KEY), "a", id="string"),
        pytest.param(mask_value(12, key=KEY), 0, id="integer"),
        pytest.param(mask_value(1.5, key=KEY), 0.1, id="number"),
        pytest.param(mask_value(True, key=KEY), True, id="boolean"),
        pytest.param(mask_value([1], key=KEY), [], id="array"),
        pytest.param(mask_value({"a": 1}, key=KEY), {}, id="object"),
        pytest.param(None, None, id="null-kept-as-is"),
        pytest.param(42, 42, id="readable-integer-as-is"),
        pytest.param("2026-01-01", "2026-01-01", id="readable-string-as-is"),
    ],
)
def test_a_token_reads_back_as_a_value_of_its_type(token, typed) -> None:
    assert type_of_token(token) == typed
    assert typed_record_from_tokens({"f": token}) == {"f": typed}


def test_the_same_value_masks_the_same_way_and_a_different_one_does_not() -> None:
    """Both sides of a comparison must agree, so a diff still reads as a diff."""
    assert mask_value("alice", key=KEY) == mask_value("alice", key=KEY)
    assert mask_value("alice", key=KEY) != mask_value("alicf", key=KEY)
    assert mask_value({"b": 1, "a": 2}, key=KEY) == mask_value(
        {"a": 2, "b": 1}, key=KEY
    )


def test_a_reordered_array_and_a_whole_float_mask_as_the_comparison_sees_them() -> None:
    """The record comparison calls `1` and `1.0`, and the same list in another
    order, one value; so do their tokens, or a masked run would report a
    difference a raw run does not."""
    assert mask_value([3, 1, 2], key=KEY) == mask_value([1, 2, 3], key=KEY)
    assert mask_value({"tags": [True, 2.0]}, key=KEY) == mask_value(
        {"tags": [2, 1]}, key=KEY
    )
    assert mask_value(1.0, key=KEY) == mask_value(1, key=KEY)
    assert mask_value(1.0, key=KEY).startswith("integer_len-1_")
    assert mask_value(1.5, key=KEY).startswith("number_len-3_")
    # A boolean keeps its own type: a field that turns into a number still
    # reads as a type change.
    assert mask_value(True, key=KEY) != mask_value(1, key=KEY)
    # The state masking takes values as written, as the final-state check does.
    assert mask_value(1.0, normalize=False, key=KEY).startswith("number_len-3_")
    assert mask_value([3, 1], normalize=False, key=KEY) != mask_value(
        [1, 3], normalize=False, key=KEY
    )


def test_the_hash_is_an_hmac_under_the_key_so_a_guess_cannot_be_confirmed_without_it() -> (
    None
):
    """A plain hash of a short value is matched by hashing the candidates; an
    HMAC under a secret key is not, and the key is what the two sides of a run
    share. The construction is pinned so nothing rebuilds it on the plain hash."""
    keyed = hmac.new(KEY, b"alice", hashlib.sha256).hexdigest()[:16]
    plain = hashlib.sha256(b"alice").hexdigest()[:16]

    assert mask_value("alice", key=KEY) == f"string_len-5_{keyed}"
    assert plain not in mask_value("alice", key=KEY)


@pytest.mark.parametrize(
    "value",
    [
        pytest.param("alice", id="string"),
        pytest.param(12345, id="integer"),
        pytest.param(1.5, id="number"),
        pytest.param(True, id="boolean"),
        pytest.param([1, 2, 3], id="array"),
        pytest.param({"a": 1}, id="object"),
    ],
)
def test_a_different_key_gives_a_different_token_for_the_same_value(value) -> None:
    """Two runs hash under two keys, so a token from one run matches nothing
    in another run's artifacts; the state tokens follow the same key."""
    assert mask_value(value, key=KEY) != mask_value(value, key=OTHER_KEY)
    assert mask_value(value, key=KEY, normalize=False) != mask_value(
        value, key=OTHER_KEY, normalize=False
    )


def test_masked_text_carries_only_its_length() -> None:
    assert mask_text("secret payload") == f"{MASKED_TEXT_PREFIX}14"


# ---------------------------------------------------------------------------
# MaskPolicy
# ---------------------------------------------------------------------------


def _catalog(*streams: dict) -> dict:
    return {"streams": list(streams)}


DATE_TIME = {"type": ["null", "string"], "format": "date-time"}


def _stream(name: str, **declared) -> dict:
    """A configured stream; `json_schema` is `{}` unless given, as the platform
    returns it for a stream whose schema is not stored."""
    configured = {
        key: declared.pop(key)
        for key in ("primary_key", "cursor_field")
        if key in declared
    }
    return {
        "stream": {"name": name, "json_schema": {}, **declared},
        "sync_mode": "incremental",
        "destination_sync_mode": "append",
        **configured,
    }


def _schema(**properties: dict) -> dict:
    return {"type": "object", "properties": properties}


@pytest.mark.parametrize(
    "cursor_schema,declared",
    [
        pytest.param(DATE_TIME, "string/date-time", id="date-time"),
        pytest.param({"type": "string", "format": "date"}, "string/date", id="date"),
        pytest.param({"type": "integer"}, "integer", id="integer"),
        pytest.param({"type": ["null", "integer"]}, "integer", id="nullable-integer"),
        pytest.param(
            {"type": "string", "airbyte_type": "timestamp_with_timezone"},
            "string/timestamp_with_timezone",
            id="airbyte-type-only",
        ),
        pytest.param(
            {"type": "string", "airbyte_type": "timestamp_without_timezone"},
            "string/timestamp_without_timezone",
            id="airbyte-type-naive",
        ),
        pytest.param(
            {"type": "string", "airbyte_type": "date"}, "string/date", id="airbyte-date"
        ),
        pytest.param(
            {"type": "number", "airbyte_type": "integer"},
            "number/integer",
            id="airbyte-integer",
        ),
    ],
)
def test_an_integer_or_date_cursor_stays_readable(cursor_schema, declared) -> None:
    policy = MaskPolicy.from_configured_catalog(
        _catalog(
            _stream(
                "users",
                default_cursor_field=["updated_at"],
                json_schema=_schema(id={"type": "integer"}, updated_at=cursor_schema),
            )
        ),
        key=KEY,
    )

    assert policy.readable("users") == {("updated_at",)}
    info = policy.streams["users"]
    assert info.cursor == ("updated_at",)
    assert info.readable is True
    assert info.declared == declared
    assert info.reason == f"readable ({declared})"
    assert policy.summary() == (1, 1)


@pytest.mark.parametrize(
    "cursor_schema,declared",
    [
        pytest.param({"type": "string"}, "string", id="string"),
        pytest.param({"type": ["null", "string"]}, "string", id="nullable-string"),
        pytest.param({"type": "number"}, "number", id="number"),
        pytest.param({"type": "string", "format": "email"}, "string/email", id="email"),
        pytest.param({}, "unknown", id="undeclared"),
        # Every declared type must fit: a string in the list can be an email.
        pytest.param(
            {"type": ["integer", "string"]}, "integer|string", id="integer-or-string"
        ),
        pytest.param(
            {"type": ["null", "number", "integer"]},
            "number|integer",
            id="number-or-integer",
        ),
        pytest.param(
            {"type": "string", "airbyte_type": "integer"},
            "string/integer",
            id="string-said-integer",
        ),
        pytest.param({"format": "date-time"}, "unknown/date-time", id="format-only"),
    ],
)
def test_a_cursor_of_any_other_type_is_masked(cursor_schema, declared) -> None:
    policy = MaskPolicy.from_configured_catalog(
        _catalog(
            _stream(
                "users",
                default_cursor_field=["email"],
                json_schema=_schema(email=cursor_schema),
            )
        ),
        key=KEY,
    )

    assert policy.readable("users") == frozenset()
    info = policy.streams["users"]
    assert info.readable is False
    assert info.declared == declared
    assert info.reason == f"masked: type {declared}"
    assert policy.summary() == (0, 1)


def test_a_cursor_whose_schema_is_missing_is_masked_and_says_so() -> None:
    """The platform returns `{}` for a stream whose schema is not stored."""
    policy = MaskPolicy.from_configured_catalog(
        _catalog(_stream("users", default_cursor_field=["updated_at"])), key=KEY
    )

    assert policy.readable("users") == frozenset()
    assert policy.streams["users"] == StreamMaskInfo(
        cursor=("updated_at",),
        readable=False,
        declared=None,
        reason="masked: schema missing",
    )


def test_a_cursor_the_schema_does_not_declare_is_masked() -> None:
    policy = MaskPolicy.from_configured_catalog(
        _catalog(
            _stream(
                "users",
                default_cursor_field=["updated_at"],
                json_schema=_schema(id={"type": "integer"}),
            )
        ),
        key=KEY,
    )

    assert policy.readable("users") == frozenset()
    assert policy.streams["users"].reason == "masked: cursor not in schema"


def test_a_nested_cursor_path_is_resolved_through_the_schema() -> None:
    policy = MaskPolicy.from_configured_catalog(
        _catalog(
            _stream(
                "orders",
                default_cursor_field=["meta", "ts"],
                json_schema=_schema(meta=_schema(ts=DATE_TIME)),
            )
        ),
        key=KEY,
    )

    assert policy.readable("orders") == {("meta", "ts")}
    assert policy.streams["orders"].reason == "readable (string/date-time)"


def test_the_configured_cursor_is_used_when_the_source_defines_none() -> None:
    policy = MaskPolicy.from_configured_catalog(
        _catalog(
            _stream(
                "users",
                cursor_field=["ts"],
                json_schema=_schema(ts={"type": "integer"}),
            )
        ),
        key=KEY,
    )

    assert policy.readable("users") == {("ts",)}


@pytest.mark.parametrize(
    "source_defined_cursor,cursor",
    [
        pytest.param(False, ("ts",), id="user-picked"),
        pytest.param(True, ("updated_at",), id="source-defined"),
    ],
)
def test_the_configured_cursor_wins_over_the_default_unless_the_source_defines_it(
    source_defined_cursor: bool, cursor: tuple[str, ...]
) -> None:
    """`default_cursor_field` is a suggestion the user can override unless the
    source defines its cursor; the policy reads the one the connector will."""
    policy = MaskPolicy.from_configured_catalog(
        _catalog(
            _stream(
                "users",
                source_defined_cursor=source_defined_cursor,
                default_cursor_field=["updated_at"],
                cursor_field=["ts"],
                json_schema=_schema(ts={"type": "integer"}, updated_at=DATE_TIME),
            )
        ),
        key=KEY,
    )

    assert policy.streams["users"].cursor == cursor
    assert policy.readable("users") == {cursor}


def test_a_primary_key_is_never_readable() -> None:
    policy = MaskPolicy.from_configured_catalog(
        _catalog(
            _stream(
                "users",
                source_defined_primary_key=[["id"]],
                primary_key=[["email"]],
                default_cursor_field=["updated_at"],
                json_schema=_schema(
                    id={"type": "integer"},
                    email={"type": "string"},
                    updated_at=DATE_TIME,
                ),
            )
        ),
        key=KEY,
    )

    assert policy.readable("users") == {("updated_at",)}


def test_a_nested_primary_key_keeps_its_path_and_masks_its_leaf() -> None:
    """One token for the whole parent object would hide the key from the
    record comparison, which reads it by path: every record would count as
    missing its key and the stream's value diffs would be lost."""
    policy = MaskPolicy.from_configured_catalog(
        _catalog(
            _stream(
                "readings",
                source_defined_primary_key=[["parent", "id"], ["day"]],
                json_schema=_schema(
                    parent=_schema(id={"type": "integer"}, name={"type": "string"}),
                    day={"type": "string"},
                    value={"type": "integer"},
                ),
            )
        ),
        key=KEY,
    )
    assert policy.primary_key("readings") == {("parent", "id"), ("day",)}

    control = {"parent": {"id": 7, "name": "Alice"}, "day": "d1", "value": 1}
    target = {"parent": {"id": 7, "name": "Alice"}, "day": "d1", "value": 2}
    masked_control = mask_record_data(
        control, policy.readable("readings"), policy.primary_key("readings"), key=KEY
    )
    masked_target = mask_record_data(
        target, policy.readable("readings"), policy.primary_key("readings"), key=KEY
    )

    assert masked_control["parent"] == {
        "id": mask_value(7, key=KEY),
        "name": mask_value("Alice", key=KEY),
    }
    assert masked_control["day"] == mask_value("d1", key=KEY)
    pk_paths = [["parent", "id"], ["day"]]
    assert _extract_pk_tuple(masked_control, pk_paths) == (
        mask_value(7, key=KEY),
        mask_value("d1", key=KEY),
    )
    assert _extract_pk_tuple(masked_target, pk_paths) == _extract_pk_tuple(
        masked_control, pk_paths
    )
    assert masked_control["value"] != masked_target["value"]


def test_an_array_primary_key_is_hashed_in_its_own_order() -> None:
    """The comparison keys `[1, 2]` and `[2, 1]` apart, so their tokens are
    two keys too, not a false duplicate; the same arrays outside the key are
    sorted first and mask alike, as the field diff compares them."""
    first = {"pair": [1, 2], "tags": [1, 2], "id": 1}
    second = {"pair": [2, 1], "tags": [2, 1], "id": 1.0}
    pk_paths = [["pair"]]

    masked_first = mask_record_data(first, (), {("pair",), ("id",)}, key=KEY)
    masked_second = mask_record_data(second, (), {("pair",), ("id",)}, key=KEY)

    assert _extract_pk_tuple(masked_first, pk_paths) != _extract_pk_tuple(
        masked_second, pk_paths
    )
    assert _extract_pk_tuple(first, pk_paths) != _extract_pk_tuple(second, pk_paths)
    assert masked_first["tags"] == masked_second["tags"]
    # A scalar key still takes a whole float as its integer, as tuple
    # equality does on the raw values.
    assert masked_first["id"] == masked_second["id"]


def test_the_configured_primary_key_is_used_when_the_source_defines_none() -> None:
    policy = MaskPolicy.from_configured_catalog(
        _catalog(
            _stream("flat", primary_key=["id"]),
            _stream("nested", primary_key=[["parent", "id"]]),
            _stream("none"),
        ),
        key=KEY,
    )

    assert policy.primary_key("flat") == {("id",)}
    assert policy.primary_key("nested") == {("parent", "id")}
    assert policy.primary_key("none") == frozenset()
    assert policy.primary_key("unknown") == frozenset()


def test_a_primary_key_that_is_also_the_cursor_follows_the_cursor_rule() -> None:
    readable = MaskPolicy.from_configured_catalog(
        _catalog(
            _stream(
                "events",
                source_defined_primary_key=[["seq"]],
                default_cursor_field=["seq"],
                json_schema=_schema(seq={"type": "integer"}),
            )
        ),
        key=KEY,
    )
    masked = MaskPolicy.from_configured_catalog(
        _catalog(
            _stream(
                "events",
                source_defined_primary_key=[["key"]],
                default_cursor_field=["key"],
                json_schema=_schema(key={"type": "string"}),
            )
        ),
        key=KEY,
    )

    assert readable.readable("events") == {("seq",)}
    assert masked.readable("events") == frozenset()


def test_a_stream_without_a_cursor_has_nothing_readable() -> None:
    policy = MaskPolicy.from_configured_catalog(
        _catalog(
            _stream(
                "events",
                source_defined_primary_key=[["id"]],
                json_schema=_schema(id={"type": "integer"}),
            )
        ),
        key=KEY,
    )

    assert policy.readable("events") == frozenset()
    assert policy.streams["events"] == StreamMaskInfo(
        cursor=None, readable=False, declared=None, reason="no cursor"
    )
    assert policy.summary() == (0, 0)


def test_a_name_shared_across_namespaces_is_readable_only_when_both_qualify() -> None:
    """Records are keyed by stream name, so one rule covers both namespaces."""
    both = MaskPolicy.from_configured_catalog(
        _catalog(
            _stream(
                "users",
                namespace="public",
                default_cursor_field=["updated_at"],
                json_schema=_schema(updated_at=DATE_TIME),
            ),
            _stream(
                "users",
                namespace="reporting",
                default_cursor_field=["modified"],
                json_schema=_schema(modified={"type": "integer"}),
            ),
        ),
        key=KEY,
    )
    one = MaskPolicy.from_configured_catalog(
        _catalog(
            _stream(
                "users",
                namespace="public",
                default_cursor_field=["updated_at"],
                json_schema=_schema(updated_at=DATE_TIME),
            ),
            _stream(
                "users",
                namespace="reporting",
                default_cursor_field=["updated_at"],
                json_schema=_schema(updated_at={"type": "string"}),
            ),
        ),
        key=KEY,
    )

    assert both.readable("users") == {("updated_at",), ("modified",)}
    assert both.streams["users"].readable is True
    assert one.readable("users") == frozenset()
    assert one.streams["users"].reason == (
        "masked: declarations differ across namespaces"
    )


def test_a_stream_unknown_to_the_policy_has_nothing_readable() -> None:
    policy = MaskPolicy.from_configured_catalog(_catalog(_stream("events")), key=KEY)

    assert policy.readable("not_in_the_catalog") == frozenset()
    assert policy.readable(None) == frozenset()
    assert MaskPolicy(key=KEY).readable("users") == frozenset()
    assert MaskPolicy(key=KEY).summary() == (0, 0)


def test_the_policy_accepts_the_protocol_model_as_well_as_a_dict() -> None:
    catalog = ConfiguredAirbyteCatalog(
        streams=[
            ConfiguredAirbyteStream(
                stream=AirbyteStream(
                    name="users",
                    json_schema=_schema(id={"type": "integer"}, updated_at=DATE_TIME),
                    supported_sync_modes=[SyncMode.incremental],
                    source_defined_primary_key=[["id"]],
                    default_cursor_field=["updated_at"],
                ),
                sync_mode=SyncMode.incremental,
                destination_sync_mode=DestinationSyncMode.append,
            )
        ]
    )

    assert MaskPolicy.from_configured_catalog(catalog, key=KEY).readable("users") == {
        ("updated_at",),
    }
    assert (
        MaskPolicy.from_configured_catalog(None, key=KEY).readable("users")
        == frozenset()
    )


def test_the_policy_carries_the_key_but_keeps_it_out_of_its_repr() -> None:
    """A policy that lands in a log line or a traceback must not show the
    run's key; it is given by keyword only, so no caller passes it by accident."""
    policy = MaskPolicy({"users": frozenset({("updated_at",)})}, key=KEY)

    assert policy.key == KEY
    assert "key=" not in repr(policy)
    assert repr(KEY) not in repr(policy)
    with pytest.raises(TypeError):
        MaskPolicy({"users": frozenset({("updated_at",)})}, {}, {}, KEY, key=KEY)  # type: ignore[misc]


def test_the_per_stream_info_serialises_for_the_run_payload() -> None:
    info = StreamMaskInfo(("meta", "ts"), True, "string/date-time", "readable (x)")

    assert info.to_dict() == {
        "cursor": ["meta", "ts"],
        "readable": True,
        "declared": "string/date-time",
        "reason": "readable (x)",
    }
    assert StreamMaskInfo(None, False, None, "no cursor").to_dict()["cursor"] is None


# ---------------------------------------------------------------------------
# Record data
# ---------------------------------------------------------------------------


def test_every_value_is_masked_except_the_readable_paths() -> None:
    data = {
        "id": 7,
        "updated_at": "2026-01-01T00:00:00Z",
        "name": "Alice",
        "age": 41,
        "active": True,
        "tags": ["a", "b"],
        "address": {"city": "Paris", "zip": "75001"},
        "nothing": None,
    }

    masked = mask_record_data(data, {("id",), ("updated_at",)}, key=KEY)

    assert masked["id"] == 7
    assert masked["updated_at"] == "2026-01-01T00:00:00Z"
    assert masked["name"] == mask_value("Alice", key=KEY)
    assert masked["age"].startswith("integer_len-2_")
    assert masked["active"].startswith("boolean_")
    assert masked["tags"].startswith("array_len-2_")
    assert masked["address"].startswith("object_len-2_")
    assert masked["nothing"] is None
    assert set(masked) == set(data)


def test_a_nested_readable_path_keeps_the_leaf_and_masks_its_siblings() -> None:
    data = {"location": {"id": 3, "name": "Berlin"}, "day": "2026-01-01", "qty": 2}

    masked = mask_record_data(data, {("location", "id"), ("day",)}, key=KEY)

    assert masked["location"]["id"] == 3
    assert masked["location"]["name"] == mask_value("Berlin", key=KEY)
    assert masked["day"] == "2026-01-01"
    assert masked["qty"] == mask_value(2, key=KEY)


def test_a_readable_path_through_a_non_object_masks_the_value_whole() -> None:
    masked = mask_record_data(
        {"location": "not an object"}, {("location", "id")}, key=KEY
    )

    assert masked["location"] == mask_value("not an object", key=KEY)


def test_a_readable_cursor_whose_value_is_an_object_is_masked() -> None:
    """A date cursor is a scalar; an object or a list under the cursor's name
    is data, not the cursor."""
    masked = mask_record_data(
        {"updated_at": {"$date": "2026-01-01"}, "ts": ["2026-01-01"]},
        [("updated_at",), ("ts",)],
        key=KEY,
    )

    assert masked == {
        "updated_at": mask_value({"$date": "2026-01-01"}, key=KEY),
        "ts": mask_value(["2026-01-01"], key=KEY),
    }


def test_the_input_record_is_left_untouched() -> None:
    data = {"id": 1, "name": "Alice", "address": {"city": "Paris"}}

    mask_record_data(data, {("id",)}, key=KEY)

    assert data == {"id": 1, "name": "Alice", "address": {"city": "Paris"}}


# ---------------------------------------------------------------------------
# Messages and lines
# ---------------------------------------------------------------------------

POLICY = MaskPolicy({"users": frozenset({("id",), ("updated_at",)})}, key=KEY)


def _line(payload: dict, ending: bytes = b"\n") -> bytes:
    return json.dumps(payload).encode() + ending


def _record(stream: str, data: dict) -> dict:
    return {
        "type": "RECORD",
        "record": {"stream": stream, "data": data, "emitted_at": 1_700_000_000_000},
    }


def test_a_record_line_is_masked_under_the_streams_policy() -> None:
    masked, kind = mask_line(
        _line(_record("users", {"id": 1, "updated_at": "2026-01-01", "name": "Alice"})),
        POLICY,
    )

    assert kind == "RECORD"
    assert masked.endswith(b"\n")
    payload = json.loads(masked)
    assert payload["record"]["stream"] == "users"
    assert payload["record"]["emitted_at"] == 1_700_000_000_000
    assert payload["record"]["data"] == {
        "id": 1,
        "updated_at": "2026-01-01",
        "name": mask_value("Alice", key=KEY),
    }
    assert b"Alice" not in masked


def test_a_record_of_an_unknown_stream_is_masked_whole() -> None:
    masked, _kind = mask_line(_line(_record("secrets", {"id": 1, "k": "v"})), POLICY)

    data = json.loads(masked)["record"]["data"]
    assert data == {"id": mask_value(1, key=KEY), "k": mask_value("v", key=KEY)}


def test_the_same_value_on_both_sides_masks_identically() -> None:
    control, _ = mask_line(_line(_record("users", {"id": 1, "name": "Alice"})), POLICY)
    target, _ = mask_line(_line(_record("users", {"id": 1, "name": "Alice"})), POLICY)
    changed, _ = mask_line(_line(_record("users", {"id": 1, "name": "Alicia"})), POLICY)

    assert control == target
    assert (
        json.loads(control)["record"]["data"]["name"]
        != (json.loads(changed)["record"]["data"]["name"])
    )


def test_a_debug_log_keeps_only_its_length_and_an_info_log_is_untouched() -> None:
    debug = _line(
        {"type": "LOG", "log": {"level": "DEBUG", "message": "GET /users -> {...}"}}
    )
    info = _line({"type": "LOG", "log": {"level": "INFO", "message": "Syncing users"}})

    masked_debug, kind = mask_line(debug, POLICY)
    masked_info, _ = mask_line(info, POLICY)

    assert kind == "LOG"
    assert json.loads(masked_debug)["log"] == {
        "level": "DEBUG",
        "message": f"{MASKED_TEXT_PREFIX}19",
    }
    assert masked_info == info


def test_a_trace_level_log_is_as_verbose_as_debug_and_masked_the_same() -> None:
    masked, _ = mask_line(
        _line({"type": "LOG", "log": {"level": "TRACE", "message": "body"}}), POLICY
    )

    assert json.loads(masked)["log"]["message"] == f"{MASKED_TEXT_PREFIX}4"


def test_a_stack_trace_on_a_log_of_any_level_keeps_only_its_length() -> None:
    masked, _ = mask_line(
        _line(
            {
                "type": "LOG",
                "log": {
                    "level": "WARN",
                    "message": "boom",
                    "stack_trace": "Traceback: KeyError('alice')",
                },
            }
        ),
        POLICY,
    )

    assert json.loads(masked)["log"] == {
        "level": "WARN",
        "message": "boom",
        "stack_trace": mask_text("Traceback: KeyError('alice')"),
    }


# What the Python CDK's uncaught-exception hook writes: the exception text and
# the whole traceback in the message, and no `stack_trace` field.
FATAL_MESSAGE = (
    "Traceback (most recent call last):\n"
    '  File "main.py", line 3, in <module>\n'
    "KeyError: 'alice@example.com'"
)


@pytest.mark.parametrize("level", ["ERROR", "FATAL"])
def test_an_error_or_fatal_log_keeps_only_its_length(level: str) -> None:
    masked, kind = mask_line(
        _line({"type": "LOG", "log": {"level": level, "message": FATAL_MESSAGE}}),
        POLICY,
    )

    assert kind == "LOG"
    assert b"alice" not in masked
    assert json.loads(masked)["log"] == {
        "level": level,
        "message": mask_text(FATAL_MESSAGE),
    }


@pytest.mark.parametrize("level", ["debug", "info", "CRITICAL", "NOTICE", None])
def test_a_log_level_outside_info_and_warn_keeps_only_its_length(level) -> None:
    """The readable levels are an exact match: a level the protocol does not
    name, or spells differently, is not let through for being unknown."""
    log = {"level": level, "message": "x alice@example.com"}
    masked, kind = mask_line(_line({"type": "LOG", "log": log}), POLICY)

    assert kind == "LOG"
    assert b"alice" not in masked
    assert json.loads(masked)["log"]["message"] == mask_text("x alice@example.com")


def test_a_log_message_that_is_not_text_keeps_only_its_length() -> None:
    """A connector that logs a dict as its message logs a body."""
    message = {"body": {"email": "alice@example.com"}, "status": 200}
    masked, _ = mask_line(
        _line({"type": "LOG", "log": {"level": "INFO", "message": message}}), POLICY
    )

    assert b"alice" not in masked
    assert json.loads(masked)["log"]["message"] == mask_text(
        json.dumps(message, sort_keys=True)
    )


def _trace(kind: str, **fields: object) -> dict:
    return {"type": "TRACE", "trace": {"type": kind, "emitted_at": 1.0, **fields}}


def test_a_trace_analytics_value_keeps_only_its_length_unless_it_is_a_count() -> None:
    """The CDK's counters are what the HTTP metrics read off the masked
    output, so a count stays; a value of any other shape does not."""
    text = _line(_trace("ANALYTICS", analytics={"type": "x", "value": "alice"}))
    count = _line(_trace("ANALYTICS", analytics={"type": "hits", "value": "42"}))

    masked, kind = mask_line(text, POLICY)

    assert kind == "TRACE"
    assert b"alice" not in masked
    assert json.loads(masked)["trace"]["analytics"] == {
        "type": "x",
        "value": mask_text("alice"),
    }
    assert mask_line(count, POLICY) == (count, "TRACE")


def test_an_estimate_or_stream_status_trace_passes_through() -> None:
    estimate = _line(_trace("ESTIMATE", estimate={"name": "users", "type": "STREAM"}))
    status = _line(
        _trace("STREAM_STATUS", stream_status={"stream_descriptor": {"name": "users"}})
    )

    assert mask_line(estimate, POLICY) == (estimate, "TRACE")
    assert mask_line(status, POLICY) == (status, "TRACE")


def test_a_warn_log_is_as_readable_as_an_info_log() -> None:
    line = _line({"type": "LOG", "log": {"level": "WARN", "message": "slow page"}})

    assert mask_line(line, POLICY) == (line, "LOG")


def test_a_trace_error_keeps_its_message_but_not_its_internals() -> None:
    masked, kind = mask_line(
        _line(
            {
                "type": "TRACE",
                "trace": {
                    "type": "ERROR",
                    "emitted_at": 1.0,
                    "error": {
                        "message": "Something went wrong",
                        "internal_message": "KeyError: 'alice@example.com'",
                        "stack_trace": "Traceback (most recent call last) ...",
                        "failure_type": "system_error",
                    },
                },
            }
        ),
        POLICY,
    )

    assert kind == "TRACE"
    error = json.loads(masked)["trace"]["error"]
    assert error["message"] == "Something went wrong"
    assert error["failure_type"] == "system_error"
    assert error["internal_message"] == mask_text("KeyError: 'alice@example.com'")
    assert error["stack_trace"] == mask_text("Traceback (most recent call last) ...")


def test_a_control_messages_connector_config_is_masked_whole() -> None:
    masked, kind = mask_line(
        _line(
            {
                "type": "CONTROL",
                "control": {
                    "type": "CONNECTOR_CONFIG",
                    "emitted_at": 1.0,
                    "connectorConfig": {
                        "config": {"api_key": "sk-live", "start_date": "2024-01-01"}
                    },
                },
            }
        ),
        POLICY,
    )

    assert kind == "CONTROL"
    config = json.loads(masked)["control"]["connectorConfig"]["config"]
    assert config == {
        "api_key": mask_value("sk-live", key=KEY),
        "start_date": mask_value("2024-01-01", key=KEY),
    }


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param(
            {
                "type": "STATE",
                "state": {
                    "type": "STREAM",
                    "stream": {
                        "stream_descriptor": {"name": "users"},
                        "stream_state": {"updated_at": "2026-01-01"},
                    },
                },
            },
            id="state",
        ),
        pytest.param(
            {"type": "CATALOG", "catalog": {"streams": [{"name": "users"}]}},
            id="catalog",
        ),
        pytest.param(
            {"type": "SPEC", "spec": {"connectionSpecification": {"type": "object"}}},
            id="spec",
        ),
        pytest.param(
            {
                "type": "CONNECTION_STATUS",
                "connectionStatus": {"status": "FAILED", "message": "401"},
            },
            id="connection-status",
        ),
        pytest.param(
            {
                "type": "TRACE",
                "trace": {
                    "type": "STREAM_STATUS",
                    "emitted_at": 1.0,
                    "stream_status": {
                        "stream_descriptor": {"name": "users"},
                        "status": "COMPLETE",
                    },
                },
            },
            id="stream-status",
        ),
        pytest.param(
            _trace(
                "STREAM_STATUS",
                stream_status={
                    "stream_descriptor": {"name": "users", "namespace": "public"},
                    "status": "INCOMPLETE",
                    "reasons": [
                        {"type": "RATE_LIMITED", "rate_limited": {"quota_reset": 10}}
                    ],
                },
            ),
            id="stream-status-rate-limited",
        ),
        pytest.param(
            _trace(
                "ESTIMATE",
                estimate={
                    "name": "users",
                    "namespace": None,
                    "type": "STREAM",
                    "row_estimate": 10,
                    "byte_estimate": 2048,
                },
            ),
            id="estimate",
        ),
        pytest.param(
            _trace(
                "ERROR",
                error={
                    "message": "Something went wrong",
                    "failure_type": "system_error",
                    "stream_descriptor": {"name": "users"},
                },
            ),
            id="error-without-internals",
        ),
        pytest.param(
            {
                "type": "LOG",
                "log": {
                    "level": "INFO",
                    "message": "Syncing users",
                    "stack_trace": None,
                },
            },
            id="info-log",
        ),
    ],
)
def test_messages_that_carry_no_record_data_are_returned_byte_for_byte(
    payload: dict,
) -> None:
    line = _line(payload)

    masked, kind = mask_line(line, POLICY)

    assert masked == line
    assert kind == payload["type"]
    assert mask_message(payload, POLICY) is payload


def test_a_line_that_is_not_a_message_keeps_only_its_length() -> None:
    masked, kind = mask_line(b"Traceback: alice@example.com\n", POLICY)

    assert kind is None
    assert masked == f"{MASKED_TEXT_PREFIX}28\n".encode()


def test_a_json_line_that_is_not_a_message_keeps_only_its_length() -> None:
    masked, kind = mask_line(b'["alice", "bob"]\n', POLICY)

    assert kind is None
    assert masked == f"{MASKED_TEXT_PREFIX}16\n".encode()


def test_a_json_object_whose_type_is_not_a_protocol_message_keeps_only_its_length() -> (
    None
):
    """The CDK writes `{"type": "DEBUG", ...}` lines to stdout; a type this
    module has no rule for is not let through on the strength of its shape."""
    line = _line({"type": "DEBUG", "data": {"email": "alice@example.com"}})

    masked, kind = mask_line(line, POLICY)

    assert kind is None
    assert masked == mask_text(line[:-1].decode()).encode() + b"\n"


@pytest.mark.parametrize(
    "kind",
    [
        pytest.param(["null", "string"], id="list"),
        pytest.param({"a": 1}, id="object"),
        pytest.param(7, id="number"),
    ],
)
def test_a_json_object_whose_type_is_not_text_keeps_only_its_length(kind) -> None:
    """A `type` that is a list or an object names no protocol type; it is
    masked like any other line that is not a message, not a crash that stops
    the read."""
    line = _line({"type": kind, "data": {"email": "alice@example.com"}})

    masked, message_kind = mask_line(line, POLICY)

    assert message_kind is None
    assert masked == mask_text(line[:-1].decode()).encode() + b"\n"


@pytest.mark.parametrize(
    "level",
    [
        pytest.param(["INFO"], id="list"),
        pytest.param({"name": "INFO"}, id="object"),
    ],
)
def test_a_log_whose_level_is_not_text_keeps_only_its_length(level) -> None:
    log = {"level": level, "message": "x alice@example.com"}

    masked, kind = mask_line(_line({"type": "LOG", "log": log}), POLICY)

    assert kind == "LOG"
    assert b"alice" not in masked
    assert json.loads(masked)["log"]["message"] == mask_text("x alice@example.com")


def test_mask_message_refuses_a_type_it_has_no_rule_for() -> None:
    with pytest.raises(ValueError, match="not a protocol message type"):
        mask_message({"type": "DEBUG", "data": {}}, POLICY)


def test_blank_lines_and_undecodable_bytes_do_not_break_the_pass() -> None:
    assert mask_line(b"\n", POLICY) == (b"\n", None)
    assert mask_line(b"", POLICY) == (b"", None)

    masked, kind = mask_line(b"\xff\xfe raw bytes\n", POLICY)

    assert kind is None
    assert masked.startswith(MASKED_TEXT_PREFIX.encode())


def test_the_line_ending_is_preserved_either_way() -> None:
    record = _record("users", {"id": 1, "name": "Alice"})

    with_newline, _ = mask_line(_line(record), POLICY)
    without_newline, _ = mask_line(_line(record, ending=b""), POLICY)
    crlf, _ = mask_line(_line(record, ending=b"\r\n"), POLICY)

    assert with_newline.endswith(b"\n")
    assert not without_newline.endswith(b"\n")
    assert crlf.endswith(b"\r\n")
    assert json.loads(with_newline) == json.loads(without_newline) == json.loads(crlf)


def test_a_stderr_line_keeps_only_its_length_and_its_ending() -> None:
    assert mask_text_line(b"KeyError: 'alice@example.com'\n") == b"masked_len-29\n"
    assert mask_text_line(b'{"type": "LOG"}\r\n') == b"masked_len-15\r\n"
    assert mask_text_line(b"\n") == b"masked_len-0\n"
    assert mask_text_line(b"no newline") == b"masked_len-10"


def test_a_stderr_line_cut_mid_character_counts_the_cut_character_as_one() -> None:
    """`h\xc3\xa9llo ` is six characters; `\xe2\x82` is two thirds of a `\u20ac`."""
    assert mask_text_line(b"h\xc3\xa9llo \xe2\x82") == b"masked_len-7"


def test_a_record_without_a_data_object_passes_through() -> None:
    line = _line({"type": "RECORD", "record": {"stream": "users", "data": None}})

    assert mask_line(line, POLICY) == (line, "RECORD")


# ---------------------------------------------------------------------------
# Fields without a rule: every message type keeps only what it is known to carry
# ---------------------------------------------------------------------------

SECRET = "alice@example.com"


def _control(**control: object) -> dict:
    return {
        "type": "CONTROL",
        "control": {"type": "CONNECTOR_CONFIG", "emitted_at": 1.0, **control},
    }


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param(
            {"type": "RECORD", "record": {"stream": "users", "data": SECRET}},
            id="record-data-text",
        ),
        pytest.param(
            {"type": "RECORD", "record": {"stream": "users", "data": [SECRET]}},
            id="record-data-list",
        ),
        pytest.param({"type": "RECORD", "record": SECRET}, id="record-not-an-object"),
        pytest.param(
            {"type": "RECORD", "record": {"stream": "users", "data": {}, "x": SECRET}},
            id="record-unknown-field",
        ),
        pytest.param(
            {"type": "RECORD", "record": {"stream": "users", "data": {}}, "x": SECRET},
            id="message-unknown-field",
        ),
        pytest.param(
            {
                "type": "RECORD",
                "record": {
                    "stream": "users",
                    "data": {},
                    "meta": {
                        "changes": [{"field": "a", "reason": SECRET}],
                        "x": SECRET,
                    },
                },
            },
            id="record-meta",
        ),
        pytest.param(
            _control(connectorConfig={"config": json.dumps({"api_key": SECRET})}),
            id="control-config-text",
        ),
        pytest.param(
            _control(connectorConfig={"api_key": SECRET}), id="control-no-config"
        ),
        pytest.param(
            _control(connectorConfig={"config": {}, "x": SECRET}),
            id="control-config-extra",
        ),
        pytest.param(_control(x=SECRET), id="control-extra"),
        pytest.param(
            {"type": "CONTROL", "control": SECRET}, id="control-not-an-object"
        ),
        pytest.param(
            {
                "type": "LOG",
                "log": {"level": "INFO", "message": "ok", "x": {"e": SECRET}},
            },
            id="log-extra",
        ),
        pytest.param({"type": "LOG", "log": SECRET}, id="log-not-an-object"),
        pytest.param(
            {"type": "LOG", "log": {"level": SECRET, "message": "ok"}},
            id="log-unknown-level",
        ),
        pytest.param(
            _trace("ERROR", error={"message": "boom", "request_body": SECRET}),
            id="error-extra",
        ),
        pytest.param(_trace("ERROR", error=SECRET), id="error-not-an-object"),
        pytest.param(_trace("WHATEVER", payload=SECRET), id="unknown-trace-type"),
        pytest.param(_trace(SECRET), id="trace-type-is-a-value"),
        pytest.param(
            _trace(
                "STREAM_STATUS",
                stream_status={
                    "stream_descriptor": {"name": "users", "x": SECRET},
                    "status": "RUNNING",
                    "note": SECRET,
                },
            ),
            id="stream-status-extra",
        ),
        pytest.param(
            _trace(
                "STREAM_STATUS",
                stream_status={
                    "stream_descriptor": {"name": "users"},
                    "status": "RUNNING",
                    "reasons": [{"type": "RATE_LIMITED", "x": SECRET}],
                },
            ),
            id="stream-status-reason-extra",
        ),
        pytest.param(
            _trace("ANALYTICS", analytics={"type": "hits", "value": "3", "x": SECRET}),
            id="analytics-extra",
        ),
        pytest.param(
            _trace(
                "ESTIMATE", estimate={"name": "users", "type": "STREAM", "x": SECRET}
            ),
            id="estimate-extra",
        ),
        pytest.param(
            _trace("ERROR", error={"message": "boom"}, analytics={"x": SECRET}),
            id="another-types-body",
        ),
    ],
)
def test_a_field_the_masking_has_no_rule_for_is_masked(payload: dict) -> None:
    """A message type keeps only the fields the protocol gives it, in the
    shape the protocol gives them: a field it has no rule for, and a body of
    the wrong shape, cannot carry a value through."""
    masked, kind = mask_line(_line(payload), POLICY)

    assert kind == payload["type"]
    assert SECRET.encode() not in masked


def test_a_masked_record_keeps_its_protocol_fields_and_still_parses() -> None:
    """The fields the comparison and the message counts read stay, so the
    masked line is still a record; a file's URL and path are tokens and its
    byte count stays."""
    payload = {
        "type": "RECORD",
        "record": {
            "stream": "users",
            "namespace": "public",
            "emitted_at": 1_700_000_000_000,
            "data": {"id": 1, "email": SECRET},
            "meta": {
                "changes": [
                    {
                        "field": "email",
                        "change": "TRUNCATED",
                        "reason": "SOURCE_FIELD_SIZE_LIMITATION",
                    }
                ]
            },
            "file_reference": {
                "staging_file_url": "s3://bucket/alice/report.pdf",
                "source_file_relative_path": "alice/report.pdf",
                "file_size_bytes": 2048,
            },
        },
    }

    masked, _ = mask_line(_line(payload), POLICY)

    record = json.loads(masked)["record"]
    assert {name: record[name] for name in ("stream", "namespace", "emitted_at")} == {
        "stream": "users",
        "namespace": "public",
        "emitted_at": 1_700_000_000_000,
    }
    assert record["data"] == {"id": 1, "email": mask_value(SECRET, key=KEY)}
    assert record["meta"] == payload["record"]["meta"]
    assert record["file_reference"] == {
        "staging_file_url": mask_value("s3://bucket/alice/report.pdf", key=KEY),
        "source_file_relative_path": mask_value("alice/report.pdf", key=KEY),
        "file_size_bytes": 2048,
    }
    assert b"alice" not in masked
    assert AirbyteMessage.parse_raw(masked).record.stream == "users"


def test_a_record_whose_data_is_not_an_object_is_one_token() -> None:
    for data in (SECRET, [SECRET, "bob"]):
        masked, kind = mask_line(
            _line({"type": "RECORD", "record": {"stream": "users", "data": data}}),
            POLICY,
        )

        assert kind == "RECORD"
        assert json.loads(masked)["record"]["data"] == mask_value(data, key=KEY)


def test_a_control_message_keeps_only_its_type_and_timestamp() -> None:
    """A connector config that is not an object -- a JSON string of one, say
    -- is one token, as is any other field: a CONTROL message carries
    credentials."""
    as_text = json.dumps({"api_key": "sk-live-123"})
    masked, _ = mask_line(
        _line(_control(connectorConfig={"config": as_text}, debug="sk-live-123")),
        POLICY,
    )

    assert json.loads(masked)["control"] == {
        "type": "CONNECTOR_CONFIG",
        "emitted_at": 1.0,
        "connectorConfig": mask_value({"config": as_text}, key=KEY, normalize=False),
        "debug": mask_value("sk-live-123", key=KEY),
    }
    assert b"sk-live-123" not in masked


def test_a_log_keeps_only_its_level_and_a_readable_message() -> None:
    context = {"email": SECRET}
    masked, _ = mask_line(
        _line(
            {"type": "LOG", "log": {"level": "INFO", "message": "ok", "ctx": context}}
        ),
        POLICY,
    )
    not_an_object, _ = mask_line(_line({"type": "LOG", "log": SECRET}), POLICY)

    assert json.loads(masked)["log"] == {
        "level": "INFO",
        "message": "ok",
        "ctx": mask_text(json.dumps(context, sort_keys=True)),
    }
    assert json.loads(not_an_object)["log"] == mask_text(SECRET)


def test_a_trace_keeps_only_the_fields_its_type_carries() -> None:
    error, _ = mask_line(
        _line(
            _trace(
                "ERROR",
                error={
                    "message": "boom",
                    "failure_type": "config_error",
                    "stream_descriptor": {"name": "users", "namespace": None},
                    "request_body": SECRET,
                },
            )
        ),
        POLICY,
    )
    unknown, _ = mask_line(_line(_trace("WHATEVER", payload=SECRET)), POLICY)
    status, _ = mask_line(
        _line(
            _trace(
                "STREAM_STATUS",
                stream_status={
                    "stream_descriptor": {"name": "users"},
                    "status": "RUNNING",
                    "note": SECRET,
                },
            )
        ),
        POLICY,
    )

    assert json.loads(error)["trace"]["error"] == {
        "message": "boom",
        "failure_type": "config_error",
        "stream_descriptor": {"name": "users", "namespace": None},
        "request_body": mask_text(SECRET),
    }
    assert json.loads(unknown)["trace"] == {
        "type": mask_text("WHATEVER"),
        "emitted_at": 1.0,
        "payload": mask_text(SECRET),
    }
    assert json.loads(status)["trace"]["stream_status"] == {
        "stream_descriptor": {"name": "users"},
        "status": "RUNNING",
        "note": mask_text(SECRET),
    }


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

# `users` keeps a readable cursor; `secrets` is known with none; `unknown` is
# not in the policy at all.
STATE_POLICY = MaskPolicy(
    {"users": frozenset({("updated_at",)}), "secrets": frozenset()}, key=KEY
)


def _stream_state(name: str, state: dict, **extra) -> dict:
    return {
        "type": "STATE",
        "state": {
            "type": "STREAM",
            "stream": {"stream_descriptor": {"name": name}, "stream_state": state},
            **extra,
        },
    }


def test_the_state_of_a_masked_cursor_stream_is_tokenised_leaf_by_leaf() -> None:
    payload = _stream_state(
        "secrets",
        {
            "token": "sk-live-abc",
            "page": 3,
            "ratio": 0.5,
            "done": True,
            "nothing": None,
            "partitions": [{"parent": "acct-1", "cursor": "2026-01-01"}],
            "__ab_full_refresh_sync_complete": True,
            "__ab_rfr_cursor": "keep-me",
        },
        sourceStats={"recordCount": 12.0},
        destinationStats={"recordCount": 12.0},
    )

    masked = mask_message(payload, STATE_POLICY)

    assert masked is not payload
    state = masked["state"]
    assert state["sourceStats"] == {"recordCount": 12.0}
    assert state["destinationStats"] == {"recordCount": 12.0}
    assert state["stream"]["stream_descriptor"] == {"name": "secrets"}
    assert state["stream"]["stream_state"] == {
        "token": mask_value("sk-live-abc", key=KEY),
        "page": mask_value(3, key=KEY),
        "ratio": mask_value(0.5, key=KEY),
        "done": True,
        "nothing": None,
        "partitions": [
            {
                "parent": mask_value("acct-1", key=KEY),
                "cursor": mask_value("2026-01-01", key=KEY),
            }
        ],
        "__ab_full_refresh_sync_complete": True,
        "__ab_rfr_cursor": mask_value("keep-me", key=KEY, normalize=False),
    }
    assert "sk-live-abc" not in json.dumps(masked)


def test_the_state_of_a_readable_cursor_stream_is_the_same_object() -> None:
    """Nothing to mask -- the cursor, a boolean, a sentinel -- means the
    original bytes of the line are kept."""
    payload = _stream_state(
        "users",
        {
            "updated_at": "2026-01-01",
            "done": True,
            "__ab_full_refresh_sync_complete": True,
        },
    )

    assert mask_message(payload, STATE_POLICY) is payload


def test_a_readable_cursor_streams_partitions_and_parent_state_are_masked() -> None:
    """The partition is a parent record's key and the parent state the parent
    stream's cursor; neither is the readable cursor, which stays."""
    payload = _stream_state(
        "users",
        {
            "states": [
                {
                    "partition": {"account_id": 42, "region": "eu"},
                    "cursor": {"updated_at": "2026-01-01"},
                }
            ],
            "parent_state": {"accounts": {"updated_at": "2026-01-02"}},
            "use_global_cursor": False,
            "lookback_window": 0,
        },
    )

    masked = mask_state(payload["state"], STATE_POLICY)

    assert masked["stream"]["stream_state"] == {
        "states": [
            {
                "partition": {
                    "account_id": mask_value(42, key=KEY),
                    "region": mask_value("eu", key=KEY),
                },
                "cursor": {"updated_at": "2026-01-01"},
            }
        ],
        "parent_state": {"accounts": {"updated_at": mask_value("2026-01-02", key=KEY)}},
        "use_global_cursor": False,
        "lookback_window": mask_value(0, normalize=False, key=KEY),
    }


def test_a_readable_cursor_streams_state_keeps_only_its_cursor() -> None:
    """A key the policy did not vouch for carries nothing readable, whatever
    it is called; the cursor's own key stays wherever it sits, and so do
    booleans, nulls and the sentinels."""
    payload = _stream_state(
        "users",
        {
            "updated_at": "2026-01-03",
            "states": [
                {
                    "partition": {"parent_id": "p-1"},
                    "cursor": {"updated_at": "2026-01-01"},
                }
            ],
            "extra_key": "sk-live",
            "slices": ["eu", 7],
            "use_global_cursor": False,
            "last_error": None,
            "__ab_full_refresh_sync_complete": True,
        },
    )

    masked = mask_state(payload["state"], STATE_POLICY)

    assert masked["stream"]["stream_state"] == {
        "updated_at": "2026-01-03",
        "states": [
            {
                "partition": {"parent_id": mask_value("p-1", key=KEY)},
                "cursor": {"updated_at": "2026-01-01"},
            }
        ],
        "extra_key": mask_value("sk-live", key=KEY),
        "slices": [mask_value("eu", key=KEY), mask_value(7, key=KEY)],
        "use_global_cursor": False,
        "last_error": None,
        "__ab_full_refresh_sync_complete": True,
    }


def test_a_value_under_the_cursors_name_stays_only_when_it_reads_as_a_cursor() -> None:
    """The cursor is matched by its key name at any depth, so a value there
    that is no integer or date is not taken for it and becomes a token."""
    policy = MaskPolicy(
        {"users": frozenset({("updated_at",)}), "events": frozenset({("seq",)})},
        key=KEY,
    )
    dated = _stream_state(
        "users",
        {
            "updated_at": "2026-01-03",
            "children": [{"updated_at": "alice@example.com"}],
            "cursor": {"updated_at": "2026-01-01T00:00:00Z"},
        },
    )
    counted = _stream_state(
        "events",
        {"seq": 100, "children": [{"seq": "carol@example.com"}], "last": {"seq": "17"}},
    )

    masked_dated = mask_state(dated["state"], policy)["stream"]["stream_state"]
    masked_counted = mask_state(counted["state"], policy)["stream"]["stream_state"]

    assert masked_dated == {
        "updated_at": "2026-01-03",
        "children": [
            {"updated_at": mask_value("alice@example.com", key=KEY, normalize=False)}
        ],
        "cursor": {"updated_at": "2026-01-01T00:00:00Z"},
    }
    assert masked_counted == {
        "seq": 100,
        "children": [
            {"seq": mask_value("carol@example.com", key=KEY, normalize=False)}
        ],
        "last": {"seq": "17"},
    }


UNION = {"type": ["null", "integer", "string"], "format": "date-time"}


@pytest.mark.parametrize(
    "cursor_schema,value,readable",
    [
        pytest.param(DATE_TIME, "2026-01-01T00:00:00Z", True, id="date-time"),
        pytest.param(
            DATE_TIME, "2026-01-01 00:00:00.123456+00:00", True, id="space-and-offset"
        ),
        pytest.param(DATE_TIME, "2026-01-01", True, id="date-in-a-date-time"),
        pytest.param(DATE_TIME, "john@doe.com", False, id="email-in-a-date-time"),
        pytest.param(
            DATE_TIME, "2026-01-01 john@doe.com", False, id="text-after-a-date"
        ),
        pytest.param(DATE_TIME, 1_767_225_600, False, id="integer-in-a-date-time"),
        pytest.param({"type": "integer"}, 42, True, id="integer"),
        pytest.param({"type": "integer"}, "42", True, id="digits-in-an-integer"),
        pytest.param({"type": "integer"}, "+44 20 7946 0958", False, id="phone"),
        pytest.param({"type": "integer"}, 4.5, False, id="float-in-an-integer"),
        pytest.param({"type": "integer"}, True, False, id="boolean-in-an-integer"),
        pytest.param({"type": "integer"}, "2026-01-01", False, id="date-in-an-integer"),
        pytest.param(
            {"type": "number", "airbyte_type": "integer"},
            42,
            True,
            id="airbyte-integer",
        ),
        pytest.param(UNION, "2026-01-01", True, id="union-takes-a-date"),
        pytest.param(UNION, 42, True, id="union-takes-an-integer"),
        pytest.param(UNION, "john@doe.com", False, id="union-masks-text"),
    ],
)
def test_a_readable_cursor_keeps_only_a_value_of_its_declared_type(
    cursor_schema: dict, value: object, readable: bool
) -> None:
    """The CDK emits a record whose cursor it cannot parse, so the schema's
    word is not enough: a value stays only when it is of the kind the schema
    declares, in the records and in the state alike. A boolean is kept in the
    state, as every boolean there is."""
    policy = MaskPolicy.from_configured_catalog(
        _catalog(
            _stream(
                "users",
                json_schema=_schema(updated_at=cursor_schema),
                default_cursor_field=["updated_at"],
            )
        ),
        key=KEY,
    )

    record, _kind = mask_line(_line(_record("users", {"updated_at": value})), policy)
    state = mask_state(_stream_state("users", {"updated_at": value})["state"], policy)

    masked_record = json.loads(record)["record"]["data"]["updated_at"]
    masked_state = state["stream"]["stream_state"]["updated_at"]
    assert masked_record == (value if readable else mask_value(value, key=KEY))
    if isinstance(value, bool):
        assert masked_state is value
    else:
        assert masked_state == (
            value if readable else mask_value(value, key=KEY, normalize=False)
        )


def test_a_sentinel_keeps_its_value_only_when_it_is_a_boolean_or_null() -> None:
    """The full-refresh sentinels are booleans, and the comparison reads only
    the key and the `true`; anything else under an `__ab_*` key is masked, on
    a masked-cursor and a readable-cursor stream alike."""
    sentinels = {
        "__ab_no_cursor_state_message": True,
        "__ab_none": None,
        "__ab_custom": {"last_email": "alice@example.com", "done": False},
    }
    expected = {
        "__ab_no_cursor_state_message": True,
        "__ab_none": None,
        "__ab_custom": {
            "last_email": mask_value("alice@example.com", key=KEY, normalize=False),
            "done": False,
        },
    }

    for stream in ("secrets", "users"):
        payload = _stream_state(stream, sentinels)

        masked = mask_state(payload["state"], STATE_POLICY)

        assert masked["stream"]["stream_state"] == expected
    kept = _stream_state("users", {"__ab_no_cursor_state_message": True})
    assert mask_state(kept["state"], STATE_POLICY) is kept["state"]


def test_a_state_keyed_by_a_partition_value_shows_the_value_as_a_key() -> None:
    """Known limitation, recorded rather than fixed: keys are never masked."""
    payload = _stream_state("users", {"p-1": {"updated_at": "2026-01-01"}})

    masked = mask_state(payload["state"], STATE_POLICY)

    assert masked is payload["state"]
    assert list(masked["stream"]["stream_state"]) == ["p-1"]


def test_state_tokens_are_taken_as_written() -> None:
    """The final-state check takes `1` against `1.0` as a type change, so
    their state tokens must differ, as the record tokens would not."""
    payload = _stream_state("secrets", {"cursor": 1.0})

    masked = mask_state(payload["state"], STATE_POLICY)

    assert masked["stream"]["stream_state"]["cursor"].startswith("number_len-3_")


def test_the_state_of_a_stream_unknown_to_the_policy_is_masked() -> None:
    payload = _stream_state("unknown", {"cursor": "secret"})

    masked = mask_message(payload, STATE_POLICY)

    assert masked["state"]["stream"]["stream_state"] == {
        "cursor": mask_value("secret", key=KEY)
    }


def test_a_state_line_is_rewritten_only_when_its_stream_is_masked() -> None:
    masked_line = _line(_stream_state("secrets", {"token": "sk-live"}))
    kept_line = _line(_stream_state("users", {"updated_at": "2026-01-01"}))

    masked, kind = mask_line(masked_line, STATE_POLICY)
    kept, _ = mask_line(kept_line, STATE_POLICY)

    assert kind == "STATE"
    assert b"sk-live" not in masked
    assert kept == kept_line


def _global_state(*entries: tuple[str, dict], shared: dict | None = None) -> dict:
    payload = {
        "type": "GLOBAL",
        "global": {
            "stream_states": [
                {"stream_descriptor": {"name": name}, "stream_state": state}
                for name, state in entries
            ]
        },
    }
    if shared is not None:
        payload["global"]["shared_state"] = shared
    return payload


def test_a_global_state_is_masked_entry_by_entry_and_its_shared_state_with_them() -> (
    None
):
    state = _global_state(
        ("users", {"updated_at": "2026-01-01"}),
        ("secrets", {"token": "sk-live"}),
        shared={"lsn": 12345, "__ab_marker": "x"},
    )

    masked = mask_state(state, STATE_POLICY)

    entries = masked["global"]["stream_states"]
    assert entries[0]["stream_state"] == {"updated_at": "2026-01-01"}
    assert entries[1]["stream_state"] == {"token": mask_value("sk-live", key=KEY)}
    assert masked["global"]["shared_state"] == {
        "lsn": mask_value(12345, key=KEY),
        "__ab_marker": mask_value("x", key=KEY, normalize=False),
    }


def test_a_global_state_whose_streams_all_keep_their_cursor_is_untouched() -> None:
    state = _global_state(("users", {"updated_at": "2026-01-01"}), shared={"lsn": 1})

    assert mask_state(state, STATE_POLICY) is state


def test_a_global_state_without_entries_masks_its_shared_state() -> None:
    state = {"type": "GLOBAL", "global": {"shared_state": {"lsn": 1}}}

    assert mask_state(state, STATE_POLICY)["global"]["shared_state"] == {
        "lsn": mask_value(1, key=KEY)
    }


def test_a_global_state_with_an_empty_entry_list_masks_its_shared_state() -> None:
    state = {
        "type": "GLOBAL",
        "global": {"stream_states": [], "shared_state": {"lsn": 1}},
    }

    masked = mask_state(state, STATE_POLICY)

    assert masked["global"] == {
        "stream_states": [],
        "shared_state": {"lsn": mask_value(1, key=KEY)},
    }


def test_a_global_states_shared_state_follows_the_policy_not_what_changed() -> None:
    """A readable stream's entry changes when its partitions are masked; that
    is no reason to mask the shared state the policy keeps readable."""
    state = _global_state(
        (
            "users",
            {
                "states": [
                    {
                        "partition": {"account_id": 42},
                        "cursor": {"updated_at": "2026-01-01"},
                    }
                ]
            },
        ),
        shared={"lsn": 1},
    )

    masked = mask_state(state, STATE_POLICY)

    [entry] = masked["global"]["stream_states"]
    assert entry["stream_state"]["states"][0]["partition"] == {
        "account_id": mask_value(42, key=KEY)
    }
    assert masked["global"]["shared_state"] == {"lsn": 1}


@pytest.mark.parametrize(
    "policy,masked",
    [
        pytest.param(STATE_POLICY, True, id="one-stream-masked"),
        pytest.param(MaskPolicy(key=KEY), True, id="no-stream-known"),
        pytest.param(
            MaskPolicy({"users": frozenset({("updated_at",)})}, key=KEY),
            False,
            id="every-cursor-readable",
        ),
    ],
)
def test_a_legacy_state_is_masked_unless_every_cursor_is_readable(
    policy: MaskPolicy, masked: bool
) -> None:
    state = {"data": {"users": {"updated_at": "2026-01-01"}, "secrets": {"t": "k"}}}

    result = mask_state(state, policy)

    if masked:
        assert result["data"] == {
            "users": {"updated_at": mask_value("2026-01-01", key=KEY)},
            "secrets": {"t": mask_value("k", key=KEY)},
        }
    else:
        assert result is state


@pytest.mark.parametrize(
    "state",
    [
        pytest.param({"type": "STREAM", "stream": SECRET}, id="stream-not-an-object"),
        pytest.param(
            {
                "type": "STREAM",
                "stream": {"stream_descriptor": {"name": "users"}},
                "data": {"token": SECRET},
            },
            id="data-beside-a-stream-state",
        ),
        pytest.param(
            {
                "type": "STREAM",
                "stream": {"stream_descriptor": {"name": "users", "x": SECRET}},
            },
            id="descriptor-extra",
        ),
        pytest.param(
            {
                "type": "STREAM",
                "stream": {"stream_descriptor": {"name": "users"}, "x": SECRET},
            },
            id="stream-entry-extra",
        ),
        pytest.param({"type": "GLOBAL", "global": SECRET}, id="global-not-an-object"),
        pytest.param(
            {"type": "GLOBAL", "global": {"stream_states": [SECRET]}},
            id="global-entry-not-an-object",
        ),
        pytest.param(
            {"type": "GLOBAL", "global": {"stream_states": [], "x": SECRET}},
            id="global-extra",
        ),
        pytest.param(
            {"global": {"stream_states": [], "shared_state": {"lsn": SECRET}}},
            id="global-without-a-type",
        ),
        pytest.param({"type": "WHATEVER", "payload": SECRET}, id="unknown-state-type"),
        pytest.param(
            {
                "type": "LEGACY",
                "data": {},
                "sourceStats": {"recordCount": 1, "x": SECRET},
            },
            id="stats-extra",
        ),
        pytest.param(
            {"type": "LEGACY", "data": {}, "x": SECRET}, id="state-unknown-field"
        ),
    ],
)
def test_a_state_of_an_unexpected_shape_fails_closed(state: dict) -> None:
    """A state field the state's type does not carry, a body that is not an
    object and every field of a state type the protocol does not name are
    tokens, on the readable-cursor stream too."""
    masked, kind = mask_line(_line({"type": "STATE", "state": state}), STATE_POLICY)

    assert kind == "STATE"
    assert SECRET.encode() not in masked


def test_a_legacy_copy_beside_a_stream_state_is_masked_and_the_rest_stays() -> None:
    state = {
        "type": "STREAM",
        "stream": {
            "stream_descriptor": {"name": "users"},
            "stream_state": {"updated_at": "2026-01-01"},
        },
        "data": {"token": SECRET, "cdc": False},
        "sourceStats": {"recordCount": 3.0},
    }

    masked = mask_state(state, STATE_POLICY)

    assert masked == {
        **state,
        "data": {"token": mask_value(SECRET, key=KEY, normalize=False), "cdc": False},
    }


# The Java CDK's legacy `DbState`, which it writes in `data` beside every STREAM
# and GLOBAL state: every stream's cursor, the masked-cursor stream's among them.
_DB_STATE_STREAMS = [
    {
        "stream_name": "secrets",
        "stream_namespace": "public",
        "cursor_field": ["ref"],
        "cursor": SECRET,
        "cursor_record_count": 1,
    },
    {
        "stream_name": "users",
        "stream_namespace": "public",
        "cursor_field": ["updated_at"],
        "cursor": "2026-01-01",
        "cursor_record_count": 1,
    },
]


@pytest.mark.parametrize(
    "state",
    [
        pytest.param(
            {
                "type": "STREAM",
                "stream": {
                    "stream_descriptor": {"name": "users", "namespace": "public"},
                    "stream_state": {"updated_at": "2026-01-01"},
                },
                "data": {"cdc": False, "streams": _DB_STATE_STREAMS},
            },
            id="stream-plus-data",
        ),
        pytest.param(
            {
                "type": "GLOBAL",
                "global": {
                    "shared_state": {"lsn": 42},
                    "stream_states": [
                        {
                            "stream_descriptor": {"name": "users"},
                            "stream_state": {"updated_at": "2026-01-01"},
                        }
                    ],
                },
                "data": {
                    "cdc": True,
                    "cdc_state": {"state": {"lsn": 42}},
                    "streams": _DB_STATE_STREAMS,
                },
            },
            id="global-plus-data",
        ),
    ],
)
def test_a_java_cdk_legacy_copy_is_masked_and_the_message_still_parses(
    state: dict,
) -> None:
    """A token in place of the copy would hide it too, but the protocol model
    reads `data` as an object and would reject the message, and the run would
    then drop every state it emitted."""
    body = "stream" if state["type"] == "STREAM" else "global"

    masked, kind = mask_line(_line({"type": "STATE", "state": state}), STATE_POLICY)
    masked_file = json.dumps(mask_input_state([state], STATE_POLICY))

    assert kind == "STATE"
    assert SECRET.encode() not in masked
    assert SECRET not in masked_file
    payload = json.loads(masked)
    assert payload["state"][body] == mask_state(state, STATE_POLICY)[body]
    assert payload["state"]["data"]["cdc"] is state["data"]["cdc"]
    assert AirbyteMessage.model_validate_json(masked).state.data is not None


def test_a_state_message_without_a_state_object_passes_through() -> None:
    payload = {"type": "STATE", "state": None}

    assert mask_message(payload, STATE_POLICY) is payload


def test_an_input_state_file_is_masked_in_every_shape_it_is_stored_in() -> None:
    messages = [
        {
            "type": "STREAM",
            "stream": {
                "stream_descriptor": {"name": "users"},
                "stream_state": {"updated_at": "2026-01-01"},
            },
        },
        {
            "type": "STREAM",
            "stream": {
                "stream_descriptor": {"name": "secrets"},
                "stream_state": {"token": "sk-live"},
            },
        },
        "not a message",
    ]
    single = messages[1]
    legacy = {"users": {"updated_at": "2026-01-01"}, "secrets": {"token": "sk-live"}}

    masked_list = mask_input_state(messages, STATE_POLICY)
    masked_single = mask_input_state(single, STATE_POLICY)
    masked_legacy = mask_input_state(legacy, STATE_POLICY)

    assert masked_list[0] is messages[0]
    assert masked_list[1]["stream"]["stream_state"] == {
        "token": mask_value("sk-live", key=KEY)
    }
    assert masked_list[2] == mask_value("not a message", key=KEY, normalize=False)
    assert masked_single["stream"]["stream_state"] == {
        "token": mask_value("sk-live", key=KEY)
    }
    assert masked_legacy == {
        "users": {"updated_at": mask_value("2026-01-01", key=KEY)},
        "secrets": {"token": mask_value("sk-live", key=KEY)},
    }
    assert mask_input_state("garbage", STATE_POLICY) == mask_value(
        "garbage", key=KEY, normalize=False
    )


def test_records_and_the_input_state_are_masked_under_the_policys_own_key() -> None:
    """Every token of a run is hashed under the key its policy carries, the
    report's copy of the input state included, so the state's tokens are the
    ones the records carry and none of another run's."""
    other = MaskPolicy(STATE_POLICY.readable_fields, key=OTHER_KEY)
    line = _line(_record("secrets", {"token": "sk-live"}))
    state = {"users": {"updated_at": "2026-01-01"}, "secrets": {"token": "sk-live"}}

    under_key, _ = mask_line(line, STATE_POLICY)
    under_other, _ = mask_line(line, other)

    assert json.loads(under_key)["record"]["data"] == {
        "token": mask_value("sk-live", key=KEY)
    }
    assert json.loads(under_other)["record"]["data"] == {
        "token": mask_value("sk-live", key=OTHER_KEY)
    }
    assert mask_input_state(state, STATE_POLICY)["secrets"] == {
        "token": mask_value("sk-live", key=KEY, normalize=False)
    }
    assert mask_input_state(state, other)["secrets"] == {
        "token": mask_value("sk-live", key=OTHER_KEY, normalize=False)
    }
