# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Masking of a connector run's output, so raw records never reach disk.

Every record value becomes a token that keeps the value's type and length and
a truncated hash of it -- `string_len-5_<hash>` -- so a schema can still be
inferred from masked output and the same value masks the same way on both
sides of a comparison: a field that differs between control and target still
reads as changed, and one that does not still reads as equal. A stream's
cursor is left readable when its declared type is an integer or a date and
its value is one, so a failing record can still be placed in the stream;
primary keys are masked.

The token shape is that of the airbyte-ci live tests, which hashed every
value in-container. The hash is an HMAC-SHA256 under a key that is made once
per run and thrown away after: both sides of a comparison and every command of
a run hash under the same key, so their tokens pair, and nobody holding the
artifacts can confirm a guess at a value by hashing it. The key is carried on
the `MaskPolicy` and never held by this module, so no caller can mask under a
key it did not choose; tokens from two runs do not match, by design.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import re
from collections.abc import Callable, Collection, Iterable, Mapping
from dataclasses import dataclass, field
from enum import Enum
from functools import partial
from typing import Any

from airbyte_protocol.models import (
    AirbyteMessage,
    AirbyteStateType,
    AirbyteStreamStatus,
    AirbyteStreamStatusReasonType,
    Change,
    EstimateType,
    FailureType,
    Level,
    OrchestratorType,
    Reason,
)
from airbyte_protocol.models import Type as AirbyteMessageType

from airbyte_ops_mcp.regression_tests.normalization import to_plain_dict
from airbyte_ops_mcp.regression_tests.regression.comparators import _normalized_value

FieldPath = tuple[str, ...]

# What a value becomes when only its length may be kept: a DEBUG log line, an
# error's stack trace, a stdout line that is not a protocol message, a line of
# the connector's stderr.
MASKED_TEXT_PREFIX = "masked_len-"

# Log levels whose message stays readable, on an exact match. Every other
# level keeps only its message's length: DEBUG and TRACE carry request and
# response bodies; ERROR and FATAL carry an exception's text, and the Python
# CDK's uncaught-exception hook writes the exception and the whole traceback
# into a FATAL message with no `stack_trace` field; a level the protocol does
# not name (`CRITICAL`) or spells differently (`debug`) is not let through on
# the strength of being unknown.
_READABLE_LOG_LEVELS = frozenset({"INFO", "WARN"})

# The message types this module knows. A stdout line whose `type` is anything
# else -- the CDK's `{"type": "DEBUG", ...}` lines among them -- is not a
# protocol message and keeps only its length (`mask_line`), so a type this
# module has no rule for cannot carry a value through.
_MESSAGE_TYPES = frozenset(
    {
        "RECORD",
        "STATE",
        "LOG",
        "TRACE",
        "CONTROL",
        "CATALOG",
        "SPEC",
        "CONNECTION_STATUS",
    }
)
# The types that carry no customer value and pass through unchanged.
_PASS_THROUGH_TYPES = frozenset({"CATALOG", "SPEC", "CONNECTION_STATUS"})


def _protocol_values(enum: type[Enum]) -> frozenset[str]:
    return frozenset(member.value for member in enum)


# The values the protocol names for a message's enum fields. A field holding
# anything else is not one of them and is masked, not let through as a label.
_LOG_LEVELS = _protocol_values(Level)
_FAILURE_TYPES = _protocol_values(FailureType)
_ESTIMATE_TYPES = _protocol_values(EstimateType)
_STREAM_STATUSES = _protocol_values(AirbyteStreamStatus)
_STREAM_STATUS_REASON_TYPES = _protocol_values(AirbyteStreamStatusReasonType)
_ORCHESTRATOR_TYPES = _protocol_values(OrchestratorType)
_RECORD_CHANGES = _protocol_values(Change)
_RECORD_CHANGE_REASONS = _protocol_values(Reason)
_STATE_TYPES = _protocol_values(AirbyteStateType)
# The field each state type keeps its state in.
_STATE_BODIES = {"STREAM": "stream", "GLOBAL": "global", "LEGACY": "data"}


def _generate_hash(value: Any, key: bytes) -> str:
    """The first 16 hex characters of HMAC-SHA256 over the value's text, under `key`."""
    return hmac.new(key, str(value).encode(), hashlib.sha256).hexdigest()[:16]


def mask_value(value: Any, *, key: bytes, normalize: bool = True) -> Any:
    """A value as a token that keeps its type and length and hides the rest.

    The token encodes the original type (`string`, `integer`, `number`,
    `boolean`, `array`, `object`), the length or size of the value, and a hash
    truncated for readability, so a schema can still be inferred from it. The
    hash is keyed with `key`, the run's secret: the same value gives the same
    token under one key and a different one under another.

    With `normalize` the value is first put in the form the record comparison
    compares it in (`_normalized_value`): a whole float as its int and every
    list sorted, at any depth, so `1` and `1.0`, and the same array in another
    order, give one token as they give one value to the comparison, and a
    masked run agrees with a raw one on them. Two differences remain: a
    boolean keeps its own token, so a top-level `True` against `1` is a diff
    masked and not raw, and a list that differs only in how often an item
    repeats is equal raw (DeepDiff ignores the count) and a diff masked. The
    state masking passes `normalize=False`: the final-state check compares
    states as written, so their tokens are too.

    `None` is returned as `None`: a null carries nothing to hide, and the
    record comparison tests a missing primary key with `is None`.
    """
    if value is None:
        return None
    if isinstance(value, bool):  # Must check bool before int (bool is subclass of int)
        return f"boolean_{_generate_hash(value, key)}"
    if normalize:
        value = _normalized_value(value)
    if isinstance(value, str):
        return f"string_len-{len(value)}_{_generate_hash(value, key)}"
    if isinstance(value, int):
        return f"integer_len-{len(str(value))}_{_generate_hash(value, key)}"
    if isinstance(value, float):
        return f"number_len-{len(str(value))}_{_generate_hash(value, key)}"
    if isinstance(value, list):
        return f"array_len-{len(value)}_{_generate_hash(json.dumps(value, sort_keys=True), key)}"
    if isinstance(value, dict):
        return f"object_len-{len(value.keys())}_{_generate_hash(json.dumps(value, sort_keys=True), key)}"
    # Fallback for unknown types
    return f"unknown_{_generate_hash(value, key)}"


def mask_all_values(data: dict[str, Any], *, key: bytes) -> dict[str, Any]:
    """A record's data with every value masked under `key` and every key kept."""
    return {name: mask_value(value, key=key) for name, value in data.items()}


def mask_message_model(message: AirbyteMessage, *, key: bytes) -> AirbyteMessage:
    """A protocol message model with its RECORD data masked whole under `key`.

    Non-RECORD messages are returned unchanged.
    """
    if message.type != AirbyteMessageType.RECORD:
        return message

    if not message.record or not message.record.data:
        return message

    message_dict = message.dict()
    message_dict["record"]["data"] = mask_all_values(message.record.data, key=key)
    return AirbyteMessage.parse_obj(message_dict)


def mask_message_models(
    messages: list[AirbyteMessage], *, key: bytes
) -> list[AirbyteMessage]:
    """A list of protocol message models, each masked by `mask_message_model`."""
    return [mask_message_model(msg, key=key) for msg in messages]


def type_of_token(value: Any) -> Any:
    """A representative value of the type a token encodes.

    This is what schema inference runs on: `string_len-5_...` becomes `"a"`,
    `integer_len-2_...` becomes `0`, and so on. A value that is not a token --
    a `None` the mask kept, a readable cursor, any non-string -- is returned
    as it is, since it already has its own type.

    Based on airbyte-ci implementation:
    https://github.com/airbytehq/airbyte/blob/master/airbyte-ci/connectors/live-tests/src/live_tests/commons/models.py#L369-L390
    """
    if not isinstance(value, str):
        return value
    if value.startswith("string_"):
        return "a"
    if value.startswith("integer_"):
        return 0
    if value.startswith("number_"):
        return 0.1
    if value.startswith("boolean_"):
        return True
    if value.startswith("array_"):
        return []
    if value.startswith("object_"):
        return {}
    return value


def typed_record_from_tokens(
    masked_data: dict[str, Any],
) -> dict[str, Any]:
    """Masked record data as typed values, for schema inference."""
    return {key: type_of_token(value) for key, value in masked_data.items()}


def mask_text(text: str) -> str:
    """A token that says how long the text was and nothing else."""
    return f"{MASKED_TEXT_PREFIX}{len(text)}"


def _mask_free_text(value: Any) -> Any:
    """`mask_text` of a field that should hold text: a string as it is, and
    anything else -- a dict a connector logs as its message -- as its
    sorted-key JSON, so a body does not pass on the strength of its type. A
    null stays, as it carries nothing."""
    if value is None:
        return None
    if isinstance(value, str):
        return mask_text(value)
    return mask_text(json.dumps(value, sort_keys=True, default=str))


def _mask_analytics_value(value: Any) -> Any:
    """A TRACE ANALYTICS value: a count stays, anything else keeps its length.

    The CDK's counters (its request and cache-hit counts, which the HTTP
    metrics read off the masked output) are non-negative integers written as
    text; a value of any other shape is not one of them.
    """
    if isinstance(value, str) and value.isdigit():
        return value
    if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
        return value
    return _mask_free_text(value)


def _token(value: Any, key: bytes) -> Any:
    """A field the masking has no rule for, as a token under `key`, taken as
    written."""
    return mask_value(value, key=key, normalize=False)


def _kept(value: Any) -> Any:
    return value


def _keep_if(
    test: Callable[[Any], bool], mask: Callable[[Any], Any]
) -> Callable[[Any], Any]:
    """A rule that keeps a value `test` accepts and masks any other with `mask`."""

    def rule(value: Any) -> Any:
        return value if test(value) else mask(value)

    return rule


def _one_of(values: frozenset[str]) -> Callable[[Any], bool]:
    def test(value: Any) -> bool:
        return isinstance(value, str) and value in values

    return test


def _is_text(value: Any) -> bool:
    return isinstance(value, str)


def _is_text_or_null(value: Any) -> bool:
    return value is None or isinstance(value, str)


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_number_or_null(value: Any) -> bool:
    return value is None or _is_number(value)


def _is_integer_or_null(value: Any) -> bool:
    return value is None or (isinstance(value, int) and not isinstance(value, bool))


def _masked_fields(
    body: dict[str, Any],
    rules: Mapping[str, Callable[[Any], Any]],
    other: Callable[[Any], Any],
) -> dict[str, Any]:
    """`body` with each field passed through its rule, and every field without
    one through `other`: a field has to be named to be kept.

    A rule keeps a value by returning that very object, and the very same
    `body` comes back when every field was kept.
    """
    masked = {name: rules.get(name, other)(value) for name, value in body.items()}
    return body if all(masked[name] is body[name] for name in body) else masked


def _masked_items(items: list[Any], rule: Callable[[Any], Any]) -> list[Any]:
    """`items` passed through `rule`; the very same list when every item was kept."""
    masked = [rule(item) for item in items]
    return items if all(new is old for new, old in zip(masked, items)) else masked


def mask_text_line(line: bytes) -> bytes:
    """One line of free text, such as the connector's stderr, as its length only.

    Unlike `mask_line`, nothing is parsed and nothing is kept: a blank line
    becomes `masked_len-0` too. The line ending is kept, so a file written line
    by line keeps its line count, and a last line that had none still has
    none. A character cut short, as when the container is stopped mid-write,
    counts as one.
    """
    body = line.rstrip(b"\r\n")
    return mask_text(body.decode(errors="replace")).encode() + line[len(body) :]


def _as_path(raw: Any) -> FieldPath | None:
    """A cursor declaration as a path: `["updated_at"]` or `["meta", "ts"]`."""
    if isinstance(raw, list) and raw and all(isinstance(p, str) for p in raw):
        return tuple(raw)
    return None


def _as_paths(raw: Any) -> frozenset[FieldPath]:
    """A primary-key declaration as paths: `[["id"]]`, `[["parent", "id"],
    ["date"]]` or the flat `["id"]`, as `normalize_primary_keys` reads them."""
    if not isinstance(raw, list):
        return frozenset()
    paths: set[FieldPath] = set()
    for part in raw:
        path = (part,) if isinstance(part, str) else _as_path(part)
        if path is not None:
            paths.add(path)
    return frozenset(paths)


# A cursor stays readable only when its declared type says it is an integer or
# a date: a string cursor can be an email or a name. Every declared type, `null`
# aside, must say so: `integer` does; a `string` does with a date format or a
# date `airbyte_type`; a `number` does with `airbyte_type: integer`, which is
# how a `number` property says integer. `["integer", "string"]` does not.
_READABLE_FORMATS = frozenset({"date", "date-time"})
_DATE_AIRBYTE_TYPES = frozenset(
    {"date", "timestamp_with_timezone", "timestamp_without_timezone"}
)


@dataclass(frozen=True)
class StreamMaskInfo:
    """What a masked run leaves readable on one stream, and why.

    `reason` is the sentence the report shows: `readable (<declared>)`,
    `masked: type <declared>`, `masked: schema missing`, `masked: cursor not
    in schema` or `no cursor`.
    """

    cursor: FieldPath | None
    readable: bool
    declared: str | None
    reason: str
    # The kinds of value a readable cursor keeps (`_fits_cursor`): `integer`,
    # `date`, or both for a union of the two. Empty when it is masked.
    kinds: frozenset[str] = frozenset()

    def to_dict(self) -> dict[str, Any]:
        """The JSON shape the run payload carries under `readable_fields`."""
        return {
            "cursor": list(self.cursor) if self.cursor else None,
            "readable": self.readable,
            "declared": self.declared,
            "reason": self.reason,
        }


def _schema_node(schema: Any, path: FieldPath) -> dict[str, Any] | None:
    """The schema of the property at `path`, descending through `properties`."""
    node = schema
    for part in path:
        if not isinstance(node, dict):
            return None
        properties = node.get("properties")
        if not isinstance(properties, dict) or part not in properties:
            return None
        node = properties[part]
    return node if isinstance(node, dict) else None


def _declared_type(node: dict[str, Any]) -> tuple[str, frozenset[str]]:
    """A property's declared type as text, and the kinds of value it may stay
    readable as -- empty when it must be masked."""
    raw = node.get("type")
    types = [
        t
        for t in (raw if isinstance(raw, list) else [raw])
        if isinstance(t, str) and t != "null"
    ]
    fmt = node.get("format")
    airbyte_type = node.get("airbyte_type")
    is_date = (isinstance(fmt, str) and fmt in _READABLE_FORMATS) or (
        isinstance(airbyte_type, str) and airbyte_type in _DATE_AIRBYTE_TYPES
    )
    kind_of = {
        "integer": "integer",
        "string": "date" if is_date else None,
        "number": "integer" if airbyte_type == "integer" else None,
    }
    kinds = [kind_of.get(t) for t in types]
    readable = bool(kinds) and all(kinds)
    declared = "|".join(types) or "unknown"
    for qualifier in (fmt, airbyte_type):
        if isinstance(qualifier, str):
            declared = f"{declared}/{qualifier}"
    return declared, frozenset(k for k in kinds if k) if readable else frozenset()


# Both kinds: what a readable path keeps when no schema typed it, as in a
# policy built by hand.
_CURSOR_KINDS = frozenset({"integer", "date"})

_DIGITS = re.compile(r"[0-9]+")
# An ISO 8601 date, or a date-time with an optional fraction and offset, as
# the whole value: `2026-01-01`, `2026-01-01T00:00:00Z`,
# `2026-01-01 00:00:00.123456+00:00`.
_ISO_DATE = re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}"
    r"(?:[T ][0-9]{2}:[0-9]{2}(?::[0-9]{2}(?:\.[0-9]+)?)?"
    r"(?:Z|[+-][0-9]{2}(?::?[0-9]{2})?)?)?"
)


def _fits_cursor(value: Any, kinds: Collection[str]) -> bool:
    """Whether a readable cursor's value is of a kind its schema declares.

    `integer` takes an integer, or a string of digits as a state often writes
    one; `date` takes a string that is wholly an ISO date or date-time. A
    boolean, a float, an object or a list is neither, and neither is a string
    with anything around the date: a connector emits a record whose cursor it
    cannot parse, so free text in a date field reaches here as it is.
    """
    if isinstance(value, bool):
        return False
    if "integer" in kinds and (
        isinstance(value, int)
        or (isinstance(value, str) and _DIGITS.fullmatch(value) is not None)
    ):
        return True
    return (
        "date" in kinds
        and isinstance(value, str)
        and _ISO_DATE.fullmatch(value) is not None
    )


def _stream_mask_info(
    stream: dict[str, Any], configured: dict[str, Any]
) -> StreamMaskInfo:
    """The rule for one configured stream, from its cursor and its schema."""
    # The cursor the connector reads: its own when it defines one, else the
    # one the user configured, with the source's default as the fallback.
    declared_cursor = _as_path(stream.get("default_cursor_field"))
    configured_cursor = _as_path(configured.get("cursor_field"))
    if stream.get("source_defined_cursor"):
        cursor = declared_cursor or configured_cursor
    else:
        cursor = configured_cursor or declared_cursor
    if cursor is None:
        return StreamMaskInfo(None, False, None, "no cursor")
    schema = stream.get("json_schema")
    if not isinstance(schema, dict) or not schema:
        return StreamMaskInfo(cursor, False, None, "masked: schema missing")
    node = _schema_node(schema, cursor)
    if node is None:
        return StreamMaskInfo(cursor, False, None, "masked: cursor not in schema")
    declared, kinds = _declared_type(node)
    if kinds:
        return StreamMaskInfo(cursor, True, declared, f"readable ({declared})", kinds)
    return StreamMaskInfo(cursor, False, declared, f"masked: type {declared}")


def _merge_namespaces(infos: list[StreamMaskInfo]) -> StreamMaskInfo:
    """One rule for a name that repeats across namespaces.

    Records are keyed by stream name, so every namespace's records mask under
    the same rule: readable only when every declaration qualifies, and masked
    (fail closed) when one does not.
    """
    first = infos[0]
    if all(info == first for info in infos):
        return first
    if all(info.readable for info in infos):
        declared = " / ".join(dict.fromkeys(info.declared or "" for info in infos))
        kinds = frozenset().union(*(info.kinds for info in infos))
        return StreamMaskInfo(
            first.cursor, True, declared, f"readable ({declared})", kinds
        )
    return StreamMaskInfo(
        first.cursor, False, None, "masked: declarations differ across namespaces"
    )


@dataclass(frozen=True)
class MaskPolicy:
    """Which fields a masked run leaves readable, per stream.

    Built from the configured catalog: a primary key is always masked, and a
    stream's cursor (the configured cursor field, or the source's own when it
    defines one) stays readable only when its declared type in the stream's
    JSON schema is an integer or a date -- see `_declared_type` -- and then
    only where its value is one (`cursor_fits`). A cursor the
    schema does not declare is masked. Streams are keyed by name, as the
    record comparison keys them; a name that repeats across namespaces is
    readable only when every declaration qualifies. A stream the policy does
    not know has nothing readable.

    The primary key's paths are kept too: a nested key's enclosing objects
    are masked field by field rather than as one token, so the key's token
    can be read out of the record as the record comparison reads it.

    The run's masking key travels on the policy, so every token a run writes
    -- records, state, a CONTROL message's config, the report's copy of the
    input state -- is hashed under the one key the run was given. It is
    keyword-only so no caller can pass it by accident, and left out of the
    repr so a logged or raised policy does not show it.
    """

    readable_fields: Mapping[str, frozenset[FieldPath]] = field(default_factory=dict)
    # Per stream, what stayed readable and why, for the report.
    streams: Mapping[str, StreamMaskInfo] = field(default_factory=dict)
    # Per stream, the primary key's paths (`source_defined_primary_key`, else
    # the configured `primary_key`), every namespace's together.
    primary_keys: Mapping[str, frozenset[FieldPath]] = field(default_factory=dict)
    key: bytes = field(kw_only=True, repr=False)

    @classmethod
    def from_configured_catalog(cls, catalog: Any, *, key: bytes) -> MaskPolicy:
        """The policy for a configured catalog, as a protocol model or a dict,
        masking under `key`."""
        plain = to_plain_dict(catalog) or {}
        declared: dict[str, list[StreamMaskInfo]] = {}
        cursors: dict[str, set[FieldPath]] = {}
        primary_keys: dict[str, set[FieldPath]] = {}
        for configured in plain.get("streams") or []:
            if not isinstance(configured, dict):
                continue
            stream = configured.get("stream")
            if not isinstance(stream, dict) or not isinstance(stream.get("name"), str):
                continue
            info = _stream_mask_info(stream, configured)
            declared.setdefault(stream["name"], []).append(info)
            if info.readable and info.cursor is not None:
                cursors.setdefault(stream["name"], set()).add(info.cursor)
            primary_keys.setdefault(stream["name"], set()).update(
                _as_paths(
                    stream.get("source_defined_primary_key")
                    or configured.get("primary_key")
                )
            )

        streams = {name: _merge_namespaces(infos) for name, infos in declared.items()}
        return cls(
            readable_fields={
                name: frozenset(cursors.get(name, ())) if info.readable else frozenset()
                for name, info in streams.items()
            },
            streams=streams,
            primary_keys={
                name: frozenset(paths) for name, paths in primary_keys.items() if paths
            },
            key=key,
        )

    def readable(self, stream: Any) -> frozenset[FieldPath]:
        """The field paths left readable on `stream`'s records."""
        if not isinstance(stream, str):
            return frozenset()
        return self.readable_fields.get(stream, frozenset())

    def primary_key(self, stream: Any) -> frozenset[FieldPath]:
        """The primary key's paths on `stream`'s records; empty without one."""
        if not isinstance(stream, str):
            return frozenset()
        return self.primary_keys.get(stream, frozenset())

    def summary(self) -> tuple[int, int]:
        """How many streams keep a readable cursor, out of those that have one."""
        with_cursor = [info for info in self.streams.values() if info.cursor]
        return sum(info.readable for info in with_cursor), len(with_cursor)

    def cursor_readable(self, stream: Any) -> bool:
        """Whether `stream`'s cursor stays readable, and with it its state."""
        return bool(self.readable(stream))

    def cursor_fits(self, stream: Any) -> Callable[[Any], bool]:
        """The test a value at `stream`'s readable cursor passes to stay
        readable, in its records and its state: `_fits_cursor` for the kinds
        its schema declares, or for both when no schema typed it."""
        info = self.streams.get(stream) if isinstance(stream, str) else None
        kinds = info.kinds if info is not None and info.readable else _CURSOR_KINDS
        return partial(_fits_cursor, kinds=kinds)

    def every_cursor_readable(self) -> bool:
        """Whether every stream the policy knows keeps a readable cursor.

        False when it knows none: a state that names no stream is masked
        unless there is a stream to vouch for it.
        """
        return bool(self.readable_fields) and all(self.readable_fields.values())


def _has_path_below(path: FieldPath, paths: Collection[FieldPath]) -> bool:
    depth = len(path)
    return any(len(other) > depth and other[:depth] == path for other in paths)


def _mask_fields(
    data: dict[str, Any],
    readable: Collection[FieldPath],
    primary_key: Collection[FieldPath],
    shaped: Collection[FieldPath],
    prefix: FieldPath,
    fits: Callable[[Any], bool],
    key: bytes,
) -> dict[str, Any]:
    masked: dict[str, Any] = {}
    for name, value in data.items():
        path = (*prefix, name)
        if path in readable and fits(value):
            # Only a value of the cursor's declared kind: free text in a date
            # field, an object or a list under its name is masked like any
            # other value.
            masked[name] = value
        elif isinstance(value, dict) and _has_path_below(path, shaped):
            masked[name] = _mask_fields(
                value, readable, primary_key, shaped, path, fits, key
            )
        elif path in primary_key and isinstance(value, (dict, list)):
            # The comparison keys records on a container's sorted-key JSON,
            # its lists in their own order: `[1, 2]` and `[2, 1]` are two
            # keys, so their tokens must be two as well.
            masked[name] = mask_value(value, key=key, normalize=False)
        else:
            masked[name] = mask_value(value, key=key)
    return masked


def mask_record_data(
    data: dict[str, Any],
    readable: Iterable[FieldPath] = (),
    primary_key: Iterable[FieldPath] = (),
    *,
    key: bytes,
    fits: Callable[[Any], bool] | None = None,
) -> dict[str, Any]:
    """A record's `data` with every value tokenised under `key` except the
    readable paths, where a value stays only when `fits` accepts it (the
    stream's `MaskPolicy.cursor_fits`; by default an integer or an ISO date).

    A nested object is masked as one token unless a readable path or a
    primary-key path runs through it, in which case the masking descends so
    the readable leaf is kept, the key's leaf is its own token and their
    siblings are masked. The key is masked either way; descending is what
    lets the record comparison still find it: `_extract_pk_tuple` reads the
    key's path, and one token for the whole parent object would read as a
    record missing its key. A key that is an array or an object is hashed as
    the comparison keys it, lists in their own order; every other array is
    sorted first, as the field diff compares it.
    """
    readable = frozenset(readable)
    primary_key = frozenset(primary_key)
    if fits is None:
        fits = partial(_fits_cursor, kinds=_CURSOR_KINDS)
    return _mask_fields(
        data, readable, primary_key, readable | primary_key, (), fits, key
    )


# A state key the connector owns rather than the cursor: the full-refresh
# sentinels (`__ab_no_cursor_state_message`, `__ab_full_refresh_sync_complete`)
# say how the stream ended, not where it stopped. They are booleans, which
# stay, and the comparison reads only the key and the `true`; any other value
# under such a key is masked like the rest of the state.
_STATE_SENTINEL_PREFIX = "__ab_"


def _mask_state_leaves(value: Any, key: bytes) -> Any:
    """A state blob with every scalar leaf tokenised under `key` and its shape
    kept.

    Keys, booleans and nulls stay as they are, so the final-state comparison
    still sees the shape it compares and the full-refresh sentinels it reads,
    which are booleans. Values are tokenised as written (`normalize=False`):
    that comparison takes `1` and `1.0` as a type change, so their tokens
    must differ too.
    """
    if isinstance(value, dict):
        return {name: _mask_state_leaves(item, key) for name, item in value.items()}
    if isinstance(value, list):
        return [_mask_state_leaves(item, key) for item in value]
    if isinstance(value, bool) or value is None:
        return value
    return mask_value(value, key=key, normalize=False)


# Keys of a stream's state that hold another stream's values: the partition a
# per-partition cursor belongs to is a parent record's key, and the parent
# state is the parent stream's cursor. Both are masked even where the stream's
# own cursor stays readable.
_PARTITION_KEYS = frozenset({"partition", "parent_state"})


def _mask_readable_stream_state(
    value: Any, cursor_keys: Collection[str], fits: Callable[[Any], bool], key: bytes
) -> Any:
    """A readable-cursor stream's state with only its cursor readable.

    A scalar stays as it is when its key is the cursor's own (the last
    element of the cursor path, wherever it sits: at the top of the state or
    under `cursor` in a per-partition entry) and `fits` accepts it, as the
    stream's records are held to the same test (`MaskPolicy.cursor_fits`),
    or when it is a boolean or a null. Everything
    under `partition`, `parent_state` or a `__ab_*` sentinel key is masked
    leaf by leaf, and every other scalar is a token under `key`: a state key
    the policy did not vouch for carries nothing readable, whatever it is
    called. Dict keys are kept as they are,
    so a state keyed by a partition value shows that value as a key (a known
    limitation, recorded in the docs).

    Returns the very same object when nothing in it needed masking.
    """
    if isinstance(value, dict):
        masked: dict[Any, Any] = {}
        for name, item in value.items():
            if name in _PARTITION_KEYS or (
                isinstance(name, str) and name.startswith(_STATE_SENTINEL_PREFIX)
            ):
                masked[name] = _mask_state_leaves(item, key)
            elif isinstance(item, (dict, list)):
                masked[name] = _mask_readable_stream_state(item, cursor_keys, fits, key)
            elif isinstance(item, bool) or item is None:
                masked[name] = item
            elif name in cursor_keys and fits(item):
                # Matched by name at any depth, so a value that is not of the
                # cursor's declared kind is not taken for the cursor.
                masked[name] = item
            else:
                masked[name] = mask_value(item, key=key, normalize=False)
        return value if all(masked[name] is value[name] for name in value) else masked
    if isinstance(value, list):
        masked_items = [
            _mask_readable_stream_state(item, cursor_keys, fits, key)
            if isinstance(item, (dict, list))
            else _mask_state_leaves(item, key)
            for item in value
        ]
        if all(masked is item for masked, item in zip(masked_items, value)):
            return value
        return masked_items
    return value


def _stream_name(entry: dict[str, Any]) -> Any:
    descriptor = entry.get("stream_descriptor")
    return descriptor.get("name") if isinstance(descriptor, dict) else None


def _mask_descriptor(descriptor: Any, mask: Callable[[Any], Any]) -> Any:
    """A stream descriptor: its name and namespace stay, anything else is masked."""
    if not isinstance(descriptor, dict):
        return mask(descriptor)
    return _masked_fields(
        descriptor,
        {
            "name": _keep_if(_is_text, mask),
            "namespace": _keep_if(_is_text_or_null, mask),
        },
        mask,
    )


def _mask_stream_state(entry: Any, policy: MaskPolicy) -> Any:
    """One `AirbyteStreamState` with its `stream_state` masked leaf by leaf,
    or, when its stream keeps a readable cursor, with everything but that
    cursor masked (`_mask_readable_stream_state`). Its descriptor keeps the
    stream's name and namespace; any other field is a token, and so is an
    entry that is not an object. The same object comes back when nothing in
    it needed masking."""
    token = partial(_token, key=policy.key)
    if not isinstance(entry, dict):
        return token(entry)
    name = _stream_name(entry)

    def stream_state(state: Any) -> Any:
        if policy.cursor_readable(name):
            cursor_keys = {path[-1] for path in policy.readable(name)}
            return _mask_readable_stream_state(
                state, cursor_keys, policy.cursor_fits(name), policy.key
            )
        return _mask_state_leaves(state, policy.key)

    return _masked_fields(
        entry,
        {
            "stream_descriptor": partial(_mask_descriptor, mask=token),
            "stream_state": stream_state,
        },
        token,
    )


def _mask_global_state(global_state: Any, policy: MaskPolicy) -> Any:
    """A GLOBAL state's body, masked entry by entry; see `mask_state`."""
    token = partial(_token, key=policy.key)
    if not isinstance(global_state, dict):
        return token(global_state)
    entries = global_state.get("stream_states")
    entry_list = entries if isinstance(entries, list) else []
    # The shared state names no stream, so the policy decides it through the
    # entries: readable only when every entry's stream keeps a readable
    # cursor, and with no entry to vouch for it, masked.
    shared_readable = bool(entry_list) and all(
        isinstance(entry, dict) and policy.cursor_readable(_stream_name(entry))
        for entry in entry_list
    )

    def stream_states(value: Any) -> Any:
        if not isinstance(value, list):
            return token(value)
        return _masked_items(value, partial(_mask_stream_state, policy=policy))

    return _masked_fields(
        global_state,
        {
            "stream_states": stream_states,
            "shared_state": _kept
            if shared_readable
            else partial(_mask_state_leaves, key=policy.key),
        },
        token,
    )


def _mask_state_stats(stats: Any, key: bytes) -> Any:
    """`sourceStats` or `destinationStats`: the counts stay, anything else is a token."""
    token = partial(_token, key=key)
    if not isinstance(stats, dict):
        return token(stats)
    count = _keep_if(_is_number_or_null, token)
    return _masked_fields(
        stats, {"recordCount": count, "rejectedRecordCount": count}, token
    )


def _state_body(state: dict[str, Any]) -> str | None:
    """The field that holds a state message's state, by its `type`; a state
    with no `type` is read by the one it carries."""
    kind = state.get("type")
    if kind is None:
        return next(
            (name for name in ("stream", "global", "data") if name in state), None
        )
    return _STATE_BODIES.get(kind) if isinstance(kind, str) else None


def mask_state(state: dict[str, Any], policy: MaskPolicy) -> dict[str, Any]:
    """An `AirbyteStateMessage` payload with the masked-cursor streams' state
    tokenised.

    A STREAM state is masked when its stream's cursor is masked or the stream
    is unknown to the policy; a readable-cursor stream keeps only its cursor
    readable in its state, with its `partition` values and `parent_state`
    (a parent record's key and the parent stream's cursor) and every other
    scalar tokenised and its keys kept. A GLOBAL state is masked entry by
    entry, and its `shared_state` unless every entry's stream keeps a
    readable cursor -- so with no entry to vouch for it, it is masked. A
    LEGACY blob names no stream, so it is masked unless every stream the
    policy knows keeps a readable cursor, and the legacy `data` copy beside a
    STREAM or GLOBAL state is masked leaf by leaf. The counts in `sourceStats`
    and `destinationStats` are kept.

    Fails closed on any other shape: a field the state's type does not carry
    (a `global` beside a STREAM state, say), a body that is not an object, and
    every field of a state whose `type` the protocol does not name, become
    tokens.

    Returns the very same object when nothing in it needed masking.
    """
    key = policy.key
    token = partial(_token, key=key)
    rules: dict[str, Callable[[Any], Any]] = {
        "type": _keep_if(_one_of(_STATE_TYPES), token),
        "sourceStats": partial(_mask_state_stats, key=key),
        "destinationStats": partial(_mask_state_stats, key=key),
    }
    body = _state_body(state)
    if body in ("stream", "global"):
        # The Java CDK writes a legacy copy of every stream's cursor in `data`
        # beside a STREAM or GLOBAL state. Nothing reads that copy back, so it
        # is masked leaf by leaf whatever the cursors, and stays the object
        # the protocol model needs to parse the message at all.
        rules["data"] = partial(_mask_state_leaves, key=key)
    if body == "stream":
        rules["stream"] = partial(_mask_stream_state, policy=policy)
    elif body == "global":
        rules["global"] = partial(_mask_global_state, policy=policy)
    elif body == "data":
        rules["data"] = (
            _kept
            if policy.every_cursor_readable()
            else partial(_mask_state_leaves, key=key)
        )
    return _masked_fields(state, rules, token)


def mask_input_state(state: Any, policy: MaskPolicy) -> Any:
    """A state file's content masked as `mask_state` masks a message.

    The file holds a list of state message payloads, as the platform stores
    them and `--state-path` seeds them, or one payload; a bare object that is
    none of those is the pre-protocol legacy blob and is masked whole unless
    every known stream keeps a readable cursor. Anything else -- an entry
    that is not an object, a file that holds neither -- is masked leaf by
    leaf.
    """
    if isinstance(state, list):
        return [
            mask_state(entry, policy)
            if isinstance(entry, dict)
            else _mask_state_leaves(entry, policy.key)
            for entry in state
        ]
    if not isinstance(state, dict):
        return _mask_state_leaves(state, policy.key)
    if any(name in state for name in ("type", "stream", "global", "data")):
        return mask_state(state, policy)
    if policy.every_cursor_readable():
        return state
    return _mask_state_leaves(state, policy.key)


def _mask_record(record: Any, policy: MaskPolicy) -> Any:
    """A RECORD's body, with `data` masked under the stream's rule and every
    field the protocol does not give a record turned into a token.

    `stream`, `namespace` and `emitted_at` stay when they have the protocol's
    type. `data` that is not an object is one token, as is a `record` that is
    not one. `meta` keeps only the field paths of its `changes` and the change
    and reason the protocol names. A `file_reference` keeps its byte count; its
    URL and path, which can name a customer's file, are tokens.
    """
    key = policy.key
    token = partial(_token, key=key)
    if not isinstance(record, dict):
        return token(record)
    stream = record.get("stream")

    def data(value: Any) -> Any:
        if not isinstance(value, dict):
            return mask_value(value, key=key)
        return mask_record_data(
            value,
            policy.readable(stream),
            policy.primary_key(stream),
            key=key,
            fits=policy.cursor_fits(stream),
        )

    def change(value: Any) -> Any:
        if not isinstance(value, dict):
            return token(value)
        return _masked_fields(
            value,
            {
                "field": _keep_if(_is_text, token),
                "change": _keep_if(_one_of(_RECORD_CHANGES), token),
                "reason": _keep_if(_one_of(_RECORD_CHANGE_REASONS), token),
            },
            token,
        )

    def changes(value: Any) -> Any:
        return _masked_items(value, change) if isinstance(value, list) else token(value)

    def meta(value: Any) -> Any:
        if not isinstance(value, dict):
            return token(value)
        return _masked_fields(value, {"changes": changes}, token)

    def file_reference(value: Any) -> Any:
        if not isinstance(value, dict):
            return token(value)
        return _masked_fields(
            value, {"file_size_bytes": _keep_if(_is_integer_or_null, token)}, token
        )

    return _masked_fields(
        record,
        {
            "stream": _keep_if(_is_text, token),
            "namespace": _keep_if(_is_text_or_null, token),
            "emitted_at": _keep_if(_is_number, token),
            "data": data,
            "meta": meta,
            "file_reference": file_reference,
        },
        token,
    )


def _mask_log(log: Any) -> Any:
    """A LOG's body: `level` stays when the protocol names it, `message` only at
    INFO or WARN and only when it is text, and every other field -- a stack
    trace, a field the protocol does not give a log -- keeps only its length,
    as does a body that is not an object."""
    if not isinstance(log, dict):
        return _mask_free_text(log)
    level = log.get("level")
    readable = isinstance(level, str) and level in _READABLE_LOG_LEVELS
    return _masked_fields(
        log,
        {
            "level": _keep_if(_one_of(_LOG_LEVELS), _mask_free_text),
            "message": _keep_if(_is_text, _mask_free_text)
            if readable
            else _mask_free_text,
        },
        _mask_free_text,
    )


def _mask_trace_body(body: Any, rules: Mapping[str, Callable[[Any], Any]]) -> Any:
    """One trace type's body: its known fields by `rules`, every other field,
    and a body that is not an object, as its length."""
    if not isinstance(body, dict):
        return _mask_free_text(body)
    return _masked_fields(body, rules, _mask_free_text)


_TEXT = _keep_if(_is_text, _mask_free_text)
_DESCRIPTOR = partial(_mask_descriptor, mask=_mask_free_text)


def _mask_status_reason(reason: Any) -> Any:
    return _mask_trace_body(
        reason,
        {
            "type": _keep_if(_one_of(_STREAM_STATUS_REASON_TYPES), _mask_free_text),
            "rate_limited": partial(
                _mask_trace_body,
                rules={"quota_reset": _keep_if(_is_integer_or_null, _mask_free_text)},
            ),
        },
    )


def _mask_status_reasons(reasons: Any) -> Any:
    if not isinstance(reasons, list):
        return _mask_free_text(reasons)
    return _masked_items(reasons, _mask_status_reason)


# Per trace type, the field its body sits in and what of it stays. Every
# field not named keeps only its length: an error's `internal_message` and
# `stack_trace` among them.
_TRACE_BODY_RULES: Mapping[str, tuple[str, Mapping[str, Callable[[Any], Any]]]] = {
    "ERROR": (
        "error",
        {
            "message": _TEXT,
            "failure_type": _keep_if(_one_of(_FAILURE_TYPES), _mask_free_text),
            "stream_descriptor": _DESCRIPTOR,
        },
    ),
    "ANALYTICS": ("analytics", {"type": _TEXT, "value": _mask_analytics_value}),
    "ESTIMATE": (
        "estimate",
        {
            "name": _TEXT,
            "namespace": _keep_if(_is_text_or_null, _mask_free_text),
            "type": _keep_if(_one_of(_ESTIMATE_TYPES), _mask_free_text),
            "row_estimate": _keep_if(_is_integer_or_null, _mask_free_text),
            "byte_estimate": _keep_if(_is_integer_or_null, _mask_free_text),
        },
    ),
    "STREAM_STATUS": (
        "stream_status",
        {
            "stream_descriptor": _DESCRIPTOR,
            "status": _keep_if(_one_of(_STREAM_STATUSES), _mask_free_text),
            "reasons": _mask_status_reasons,
        },
    ),
}


def _mask_trace(trace: Any) -> Any:
    """A TRACE's body: `type` and `emitted_at` stay, and the body of a trace
    type this module knows keeps only the fields it names
    (`_TRACE_BODY_RULES`). Every other field keeps only its length, so a
    trace type it does not know keeps nothing but its timestamp."""
    if not isinstance(trace, dict):
        return _mask_free_text(trace)
    rules: dict[str, Callable[[Any], Any]] = {
        "type": _keep_if(_one_of(frozenset(_TRACE_BODY_RULES)), _mask_free_text),
        "emitted_at": _keep_if(_is_number, _mask_free_text),
    }
    kind = trace.get("type")
    if isinstance(kind, str) and kind in _TRACE_BODY_RULES:
        field_name, body_rules = _TRACE_BODY_RULES[kind]
        rules[field_name] = partial(_mask_trace_body, rules=body_rules)
    return _masked_fields(trace, rules, _mask_free_text)


def _mask_control(control: Any, key: bytes) -> Any:
    """A CONTROL's body: `type` and `emitted_at` stay, a connector config's
    `config` object has every value masked, and anything else -- a config
    that is not an object, a field the protocol does not give the message --
    is one token."""
    token = partial(_token, key=key)
    if not isinstance(control, dict):
        return token(control)

    def connector_config(value: Any) -> Any:
        if not isinstance(value, dict) or not isinstance(value.get("config"), dict):
            return token(value)
        return _masked_fields(
            value, {"config": partial(mask_all_values, key=key)}, token
        )

    return _masked_fields(
        control,
        {
            "type": _keep_if(_one_of(_ORCHESTRATOR_TYPES), token),
            "emitted_at": _keep_if(_is_number, token),
            "connectorConfig": connector_config,
        },
        token,
    )


def mask_message(payload: dict[str, Any], policy: MaskPolicy) -> dict[str, Any]:
    """A parsed protocol message with every field it has no rule for masked.

    Each message type keeps only the fields the protocol gives it, and only
    in the shape the protocol gives them; anything else fails closed. RECORD
    data is masked under `policy` (see `_mask_record`), and so is the STATE of
    a stream whose cursor is masked (see `mask_state`). A LOG keeps its
    message only at INFO or WARN level, spelled exactly so, and only when it
    is text (see `_mask_log`). A TRACE keeps only the fields of its type: an
    error its `message`, failure type and stream, not its `internal_message`
    or `stack_trace`; an ANALYTICS value only when it is a count (see
    `_mask_trace`). A CONTROL message's connector config is masked whole (see
    `_mask_control`). A field beside the message's body is a token. CATALOG,
    SPEC and CONNECTION_STATUS pass through unchanged. Any other `type` is not
    a protocol message and raises `ValueError`; `mask_line` masks such a line
    to its length before it gets here.

    Returns the very same object when nothing in it needed masking, so a
    caller can keep the original bytes of a line it did not touch.
    """
    kind = payload.get("type")
    if not isinstance(kind, str) or kind not in _MESSAGE_TYPES:
        raise ValueError(f"not a protocol message type: {kind!r}")
    if kind in _PASS_THROUGH_TYPES:
        return payload

    key = policy.key
    token = partial(_token, key=key)

    def state(value: Any) -> Any:
        return mask_state(value, policy) if isinstance(value, dict) else token(value)

    body_rules: dict[str, tuple[str, Callable[[Any], Any]]] = {
        "RECORD": ("record", partial(_mask_record, policy=policy)),
        "LOG": ("log", _mask_log),
        "TRACE": ("trace", _mask_trace),
        "STATE": ("state", state),
        "CONTROL": ("control", partial(_mask_control, key=key)),
    }
    body, rule = body_rules[kind]
    return _masked_fields(payload, {"type": _kept, body: rule}, token)


def mask_line(line: bytes, policy: MaskPolicy) -> tuple[bytes, str | None]:
    """One line of a connector's stdout, masked, and the message type it held.

    A protocol message is masked by `mask_message` and re-serialised only when
    it changed; a line that is not a protocol message -- not JSON, not an
    object, or an object whose `type` is none of the protocol's
    (`_MESSAGE_TYPES`) -- keeps only its length. A blank line stays blank.
    Whether the line ended in a newline is preserved, so a caller streaming
    lines to a file can write what comes back as-is.

    The type is `None` for a line that was not a message, so a caller that
    needs to count records does not parse the line a second time.
    """
    body = line.rstrip(b"\r\n")
    ending = line[len(body) :]
    if not body.strip():
        return line, None

    try:
        payload = json.loads(body)
    except ValueError:
        payload = None
    # A `type` that is not text (a list, an object) is no protocol type, and
    # would not hash for the set lookup either.
    kind = payload.get("type") if isinstance(payload, dict) else None
    if (
        not isinstance(payload, dict)
        or not isinstance(kind, str)
        or kind not in _MESSAGE_TYPES
    ):
        return mask_text(body.decode(errors="replace")).encode() + ending, None

    masked = mask_message(payload, policy)
    if masked is payload:
        return line, kind
    return json.dumps(masked).encode() + ending, kind
