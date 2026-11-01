"""Serialization utilities for Bitfab SDK.

This module provides serialization with type metadata preservation,
similar to superjson in JavaScript. Uses jsonpickle for handling
arbitrary Python objects including datetime, Decimal, UUID, sets,
custom classes, etc.
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import json
import math
import sys
from collections.abc import Iterable
from decimal import Decimal
from enum import Enum
from types import ModuleType
from typing import Any, TypedDict
from uuid import UUID

import jsonpickle

from bitfab.payload_budget import MAX_COMPRESSIBLE_SPAN_CARRIER_BYTES


class SerializedValue(TypedDict, total=False):
    """Serialized value with JSON data and optional type metadata.

    Attributes:
        json: The JSON-serializable data
        meta: Type metadata for reconstructing special types (only present if needed)
    """

    json: Any
    meta: Any


# Types jsonpickle handles well that json.dumps cannot natively serialize.
_JSONPICKLE_NATIVE_TYPES = (
    dt.datetime,
    dt.date,
    dt.time,
    UUID,
    Decimal,
    bytes,
    bytearray,
    set,
    frozenset,
)

# Module prefixes whose objects are expected to contain non-picklable runtime
# state (callbacks, thread locks, http clients, weak refs, etc.). We proactively
# convert these to plain dicts via `.model_dump()` / `asdict()` instead of
# letting jsonpickle walk their internals.
_FRAMEWORK_MODULE_PREFIXES: tuple[str, ...] = (
    "openai",
    "anthropic",
    "claude_agent_sdk",
    "httpx",
    "httpcore",
    "fastmcp",
    "mcp",
)


def _is_framework_object(value: Any) -> bool:
    """Return True if `value` appears to come from a known SDK/framework.

    Matches on the class's module name. Accepts both dotted children
    (`openai.types`) and underscore-suffixed sibling packages.
    """
    module = getattr(type(value), "__module__", "") or ""
    return any(
        module == prefix
        or module.startswith(prefix + ".")
        or module.startswith(prefix + "_")
        for prefix in _FRAMEWORK_MODULE_PREFIXES
    )


def to_json_safe(value: Any) -> Any:
    """Convert any value to JSON-serialisable primitives, never raising.

    Produces plain dicts/lists/scalars suitable for ``json.dumps``, recursing
    through ``model_dump()`` / ``dict()`` / dataclass / ``__dict__`` so no raw
    non-serialisable object (a Pydantic model class, a tool schema, an SDK
    client) survives into a span payload.

    This is the single shared "safe serialize" used by every framework
    integration (LangGraph, OpenAI tracing, Claude Agent SDK, the ``@span``
    decorator). Keeping the recurse-the-dump logic here, in one place, is what
    stops a new integration from reintroducing the "dump without recursing"
    bug - see ``tests/test_serialization_invariant.py``.
    """
    try:
        return _to_json_safe(value)
    except Exception:
        return f"<{type(value).__qualname__}>"


def encode_json(value: Any) -> str:
    """Encode a value exactly as it goes on the wire, raising if it cannot.

    The single encoder for request bodies and span payload attributes, so the
    string a caller validates is the same string that is sent and never has to
    be produced twice.
    """
    return json.dumps(value, separators=(",", ":"), allow_nan=False)


def to_json_safe_report(value: Any) -> tuple[Any, list[str]]:
    """Like :func:`to_json_safe`, but also report what could not be captured.

    Returns ``(safe, dropped)`` where ``dropped`` lists the type name behind
    every placeholder stub the walker had to emit: a cycle, a max-depth cut, an
    opaque object with no usable shape, or a failed item/attribute. An empty
    list means a faithful capture (a value reached via ``model_dump`` / ``dict``
    / dataclass / ``__class__`` shell records nothing, because that data is
    preserved). Callers use ``dropped`` to mark a span/trace as degraded rather
    than letting the loss go unrecorded.
    """
    dropped: list[str] = []
    try:
        return _to_json_safe(value, _dropped=dropped), dropped
    except Exception:
        name = type(value).__qualname__
        return f"<{name}>", [name]


def _to_json_safe(
    value: Any,
    _depth: int = 0,
    _seen: Any = None,
    _dropped: list[str] | None = None,
) -> Any:
    """Recursive worker for ``to_json_safe``. ``_seen`` tracks object ids on the
    current path so cyclic graphs collapse to a ``<cycle ...>`` marker instead
    of recursing until the depth cap.

    When ``_dropped`` is supplied, the type name behind every placeholder stub
    (cycle, max-depth cut, opaque object, failed item/attr) is appended to it so
    callers can mark a degraded capture. A faithfully captured value
    (``model_dump`` / ``dict`` / dataclass / ``__class__`` shell) records
    nothing."""
    if _seen is None:
        _seen = frozenset()

    # Prevent runaway recursion on pathologically nested structures.
    if _depth > _MAX_SAFE_DEPTH:
        if _dropped is not None:
            _dropped.append(type(value).__qualname__)
        return f"<{type(value).__qualname__}: max depth>"

    if value is None or isinstance(value, (str, int, float, bool)):
        return value

    # Enum before model_dump since Enums can inherit from Pydantic-ish things.
    if isinstance(value, Enum):
        try:
            return _to_json_safe(value.value, _depth + 1, _seen, _dropped)
        except Exception:
            return str(value)

    # Types that json.dumps can't handle but that stringify reasonably.
    if isinstance(value, (dt.datetime, dt.date, dt.time)):
        return value.isoformat()
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, (bytes, bytearray)):
        try:
            return value.decode("utf-8")
        except Exception:
            return value.hex()

    # Cycle detection for containers and objects that carry state.
    if isinstance(value, (dict, list, tuple, set, frozenset)) or hasattr(
        value, "__dict__"
    ):
        obj_id = id(value)
        if obj_id in _seen:
            if _dropped is not None:
                _dropped.append(type(value).__qualname__)
            return f"<cycle {type(value).__qualname__}>"
        _seen = _seen | {obj_id}

    if isinstance(value, dict):
        out: dict[str, Any] = {}
        for k, v in value.items():
            if type(k) is str:
                safe_key = k
            elif isinstance(k, str):
                safe_key = str.__str__(k)
            elif isinstance(k, float) and not math.isfinite(k):
                if _dropped is not None:
                    _dropped.append("non_finite_float")
                safe_key = f"<unserializable: non_finite_float_key: {k}>"
            else:
                key_type = type(k).__qualname__
                if _dropped is not None:
                    _dropped.append(key_type)
                try:
                    safe_key = str(k)
                except Exception:
                    safe_key = f"<unserializable: {key_type}_key>"

            base_key = safe_key
            suffix = 2
            while safe_key in out:
                safe_key = f"{base_key} #{suffix}"
                suffix += 1
            try:
                out[safe_key] = _to_json_safe(v, _depth + 1, _seen, _dropped)
            except Exception:
                if _dropped is not None:
                    _dropped.append(type(v).__qualname__)
                out[safe_key] = f"<{type(v).__qualname__}>"
        return out

    if isinstance(value, (list, tuple, set, frozenset)):
        out_list: list[Any] = []
        for item in value:
            try:
                out_list.append(_to_json_safe(item, _depth + 1, _seen, _dropped))
            except Exception:
                if _dropped is not None:
                    _dropped.append(type(item).__qualname__)
                out_list.append(f"<{type(item).__qualname__}>")
        return out_list

    # Pydantic v2
    model_dump = getattr(value, "model_dump", None)
    if callable(model_dump):
        try:
            return _to_json_safe(model_dump(mode="python"), _depth + 1, _seen, _dropped)
        except Exception:
            try:
                return _to_json_safe(model_dump(), _depth + 1, _seen, _dropped)
            except Exception:
                pass

    # Pydantic v1
    dict_method = getattr(value, "dict", None)
    if callable(dict_method):
        try:
            return _to_json_safe(dict_method(), _depth + 1, _seen, _dropped)
        except Exception:
            pass

    # Dataclass instance (not the class itself)
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        try:
            return _to_json_safe(dataclasses.asdict(value), _depth + 1, _seen, _dropped)
        except Exception:
            pass

    # Objects with a __dict__ - shallow expansion.
    if hasattr(value, "__dict__") and _depth < _SHALLOW_OBJECT_DEPTH:
        try:
            attrs: dict[str, Any] = {}
            for k, v in vars(value).items():
                if k.startswith("_"):
                    continue
                try:
                    attrs[k] = _to_json_safe(v, _depth + 1, _seen, _dropped)
                except Exception:
                    if _dropped is not None:
                        _dropped.append(type(v).__qualname__)
                    attrs[k] = f"<{type(v).__qualname__}>"
            class_name = type(value).__qualname__
            if attrs:
                return {"__class__": class_name, **attrs}
        except Exception:
            pass

    if _dropped is not None:
        _dropped.append(type(value).__qualname__)
    return f"<{type(value).__qualname__}>"


def _contains_framework_object(value: Any, _depth: int = 0) -> bool:
    """Return True if value or a nested child is a framework object."""
    if _depth > 8:
        return False
    if _is_framework_object(value):
        return True
    if isinstance(value, dict):
        return any(_contains_framework_object(v, _depth + 1) for v in value.values())
    if isinstance(value, (list, tuple, set, frozenset)):
        return any(_contains_framework_object(v, _depth + 1) for v in value)
    return False


# Cap on a single serialized value. jsonpickle can succeed on values like SDK
# client instances (OpenAI, etc.) and produce hundreds of KB to MB of useless
# internal state, so this is the cheap early-out that stops the walk before a
# pathological object is carried any further. It is deliberately the same number
# as the whole-span budget: one legitimately large value may use the entire
# budget, and enforce_payload_budget is what enforces the total once every field
# is in. Anything past it is replaced with a stub so the span still ships and
# the trace isn't dropped server-side.
_MAX_SERIALIZED_BYTES = MAX_COMPRESSIBLE_SPAN_CARRIER_BYTES
_MAX_SAFE_DEPTH = 16
_SHALLOW_OBJECT_DEPTH = 4
_DEFAULT_GETSTATE = getattr(object, "__getstate__", None)
_FLAT_SCALAR_TYPES = frozenset({int, float, bool, type(None)})
_MAX_SKIPPED_PER_BUDGET_BYTE = 3


def too_large_reason(budget: int) -> str:
    return f"too_large_over_{budget}_bytes"


def _loaded_attribute(module_name: str, name: str) -> Any:
    module = sys.modules.get(module_name)
    return getattr(module, name, None) if module is not None else None


def _has_jsonpickle_handler(kind: type) -> bool:
    return jsonpickle.handlers.registry.get(kind) is not None


def _pickles_with_default_state(kind: type) -> bool:
    return (
        kind.__reduce_ex__ is object.__reduce_ex__
        and getattr(kind, "__getstate__", None) is _DEFAULT_GETSTATE
        and kind.__getattribute__ is object.__getattribute__
        and not hasattr(kind, "__getattr__")
        and not _has_jsonpickle_handler(kind)
    )


def _pickles_as_plain_object(node: Any, kind: type) -> bool:
    return (
        not callable(node)
        and not isinstance(node, (ModuleType, BaseException))
        and isinstance(getattr(node, "__dict__", None), dict)
        and _pickles_with_default_state(kind)
        and kind.__reduce__ is object.__reduce__
        and not hasattr(kind, "__getnewargs_ex__")
        and not hasattr(kind, "__getnewargs__")
        and not hasattr(kind, "__slots__")
    )


def _pickles_as_model(kind: type, model_getstate: Any) -> bool:
    return (
        model_getstate is not None
        and getattr(kind, "__getstate__", None) is model_getstate
        and not _has_jsonpickle_handler(kind)
    )


def _pickles_as_exception(node: Any, kind: type) -> bool:
    return (
        isinstance(node, BaseException)
        and isinstance(getattr(node, "__dict__", None), dict)
        and _pickles_with_default_state(kind)
        and kind.__reduce__ is BaseException.__reduce__
    )


class _WalkTooLong(Exception):
    pass


def _flat_items_size(items: Any, room: int, check_types: bool = True) -> int | None:
    shortest = max(2 * len(items) - 1, 0)
    if shortest > room:
        return shortest
    if not check_types:
        return None
    kinds = set(map(type, items))
    if kinds <= _FLAT_SCALAR_TYPES:
        return shortest
    if kinds == {str}:
        return sum(map(len, items)) + 3 * len(items) - 1
    return None


def _ndarray_text_size(node: Any) -> int:
    if _has_jsonpickle_handler(type(node)):
        return 1
    if node.dtype.hasobject:
        return int(node.size)
    return int(node.nbytes) * 4 // 3


def exceeds_jsonpickle_budget(value: Any, budget: int) -> bool:
    total = 0
    skipped = 0
    seen: set[int] = set()
    ndarray = _loaded_attribute("numpy", "ndarray")
    model_getstate = getattr(
        _loaded_attribute("pydantic", "BaseModel"), "__getstate__", None
    )

    def visit_entries(entries: dict[Any, Any]) -> None:
        nonlocal total, skipped
        for key, item in entries.items():
            if total > budget:
                return
            if callable(item) or (isinstance(key, str) and key.startswith("py/")):
                skipped += 1
                if skipped > _MAX_SKIPPED_PER_BUDGET_BYTE * budget:
                    raise _WalkTooLong
                continue
            total += (len(key) if isinstance(key, str) else 0) + 3
            visit(item)

    def visit_items(items: Any) -> None:
        nonlocal total
        total += 2
        flat_size = _flat_items_size(items, budget - total)
        if flat_size is not None:
            total += flat_size
            return
        for index, item in enumerate(items):
            if total > budget:
                return
            if index:
                total += 1
            visit(item)

    def visit(node: Any) -> None:
        nonlocal total
        kind = type(node)
        if node is None or kind is bool:
            total += 4
        elif kind is str:
            total += len(node) + 2
        elif kind is int or kind is float:
            total += 1
        elif kind is bytes:
            total += len(node) * 4 // 3 + 2
        elif id(node) in seen:
            total += 1
        else:
            seen.add(id(node))
            if kind is dict:
                total += 2
                visit_entries(node)
            elif kind in (list, tuple, set, frozenset):
                visit_items(node)
            elif ndarray is not None and kind is ndarray:
                total += _ndarray_text_size(node)
            elif _pickles_as_exception(node, kind):
                total += 2
                visit_items(node.args)
                visit_entries(vars(node))
            elif _pickles_as_model(kind, model_getstate) or _pickles_as_plain_object(
                node, kind
            ):
                total += 2
                visit_entries(vars(node))
            else:
                total += 1

    try:
        visit(value)
    except Exception:
        return False
    return total > budget


def _readable_bytes_size(node: bytes | bytearray, remaining: int) -> int:
    """Lower bound on the text to_json_safe writes for bytes: the decoded
    UTF-8 when it decodes, else a hex string twice as long. Every UTF-8
    character takes at most four bytes, so len // 4 holds either way and
    answers without reading the bytes once it alone passes the budget."""
    floor = len(node) // 4
    if floor > remaining:
        return floor
    if node.isascii():
        return len(node)
    try:
        return len(node.decode("utf-8"))
    except UnicodeDecodeError:
        return 2 * len(node)


def exceeds_readable_budget(values: Iterable[Any], budget: int) -> bool:
    total = 0
    skipped = 0
    ancestors: set[int] = set()

    def visit(node: Any, depth: int) -> None:
        nonlocal total
        if depth > _MAX_SAFE_DEPTH:
            total += 2
        elif node is None or isinstance(node, bool):
            total += 4
        elif isinstance(node, str):
            total += len(node) + 2
        elif isinstance(node, (int, float, Enum)):
            total += 1
        elif isinstance(node, (dt.datetime, dt.date, dt.time, UUID, Decimal)):
            total += 2
        elif isinstance(node, (bytes, bytearray)):
            total += _readable_bytes_size(node, budget - total) + 2
        elif isinstance(node, (dict, list, tuple, set, frozenset)) or hasattr(
            node, "__dict__"
        ):
            if id(node) in ancestors:
                total += 2
                return
            ancestors.add(id(node))
            visit_shape(node, depth)
            ancestors.discard(id(node))
        else:
            total += 2

    def visit_shape(node: Any, depth: int) -> None:
        nonlocal total
        if isinstance(node, dict):
            total += 2
            visit_entries(node.items(), depth, skip_private=False)
        elif isinstance(node, (list, tuple, set, frozenset)):
            total += 2
            flat_size = _flat_items_size(
                node, budget - total, check_types=depth < _MAX_SAFE_DEPTH
            )
            if flat_size is not None:
                total += flat_size
                return
            for index, item in enumerate(node):
                if total > budget:
                    return
                if index:
                    total += 1
                visit(item, depth + 1)
        elif (
            callable(getattr(node, "model_dump", None))
            or callable(getattr(node, "dict", None))
            or (dataclasses.is_dataclass(node) and not isinstance(node, type))
        ):
            total += 1
        elif depth < _SHALLOW_OBJECT_DEPTH:
            total += 2
            visit_entries(vars(node).items(), depth, skip_private=True)
        else:
            total += 2

    def visit_entries(
        entries: Iterable[tuple[Any, Any]], depth: int, skip_private: bool
    ) -> None:
        nonlocal total, skipped
        for key, item in entries:
            if total > budget:
                return
            if skip_private and key.startswith("_"):
                skipped += 1
                if skipped > _MAX_SKIPPED_PER_BUDGET_BYTE * budget:
                    raise _WalkTooLong
                continue
            total += (len(key) if isinstance(key, str) else 0) + 3
            visit(item, depth + 1)

    try:
        for value in values:
            if total > budget:
                break
            visit(value, 0)
    except Exception:
        return False
    return total > budget


def _describe_value(value: Any) -> str:
    try:
        name = type(value).__qualname__
        if name and name != "object":
            return name
    except Exception:
        pass
    return type(value).__name__ if value is not None else "None"


def _unserializable_stub(value: Any, reason: str) -> SerializedValue:
    try:
        summary = f"<unserializable: {_describe_value(value)} ({reason})>"
    except Exception:
        summary = f"<unserializable ({reason})>"
    return {"json": summary}


def _safe_str(value: Any) -> str:
    """str() that never raises. Replaces calls to bare str(value) which can
    propagate exceptions from a user-defined __str__/__repr__."""
    try:
        return str(value)
    except Exception:
        return f"<{_describe_value(value)}: __str__ raised>"


def serialize_value(value: Any) -> SerializedValue:
    """Serialize a value using jsonpickle for type preservation.

    Handles arbitrary Python objects including:
    - datetime, date, time
    - Decimal, UUID
    - set, frozenset
    - bytes, bytearray
    - Custom classes
    - Pydantic models

    Guarantees:
    - Never raises. Pathological inputs (SDK clients, objects with
      poisoned __str__/__getattr__, cycles that defeat jsonpickle) return
      a stub string.
    - Never returns a payload larger than _MAX_SERIALIZED_BYTES; oversized
      inputs are replaced with a stub. Without this the wire-side
      json.dumps in http.py can produce a request that times out or gets
      rejected, leaving a trace with zero spans.

    Args:
        value: Any Python value to serialize

    Returns:
        SerializedValue with 'json' field containing the data.
        If type metadata is needed for reconstruction, includes 'meta' field.

    Example:
        >>> from datetime import datetime
        >>> result = serialize_value(datetime(2024, 1, 15, 10, 30))
        >>> result["json"]  # Contains the serialized datetime
        >>> result.get("meta")  # Contains type info if present
    """
    try:
        return _serialize_value_inner(value)
    except Exception:
        return _unserializable_stub(value, "serialize_value_unexpected_error")


def _serialize_value_inner(value: Any) -> SerializedValue:
    if value is None:
        return {"json": None}

    # For simple JSON-native types, no metadata needed
    if isinstance(value, (str, int, float, bool)):
        return {"json": value}

    if exceeds_jsonpickle_budget(value, _MAX_SERIALIZED_BYTES):
        return _unserializable_stub(value, too_large_reason(_MAX_SERIALIZED_BYTES))

    import json

    # For dicts and lists of simple types, try plain JSON first
    if isinstance(value, (dict, list)):
        try:
            # Check if it's already JSON-serializable without special types
            encoded = json.dumps(value)
            if len(encoded) > _MAX_SERIALIZED_BYTES:
                return _unserializable_stub(value, f"too_large_{len(encoded)}_bytes")
            return {"json": value}
        except (TypeError, ValueError):
            # Contains special types, use jsonpickle
            pass

    # Use jsonpickle for everything else
    try:
        # Encode with type information (unpicklable=True preserves type markers)
        encoded = jsonpickle.encode(value, unpicklable=True)
        if encoded is None:
            return _unserializable_stub(value, "jsonpickle_returned_none")
        if len(encoded) > _MAX_SERIALIZED_BYTES:
            return _unserializable_stub(value, f"too_large_{len(encoded)}_bytes")
        # Parse back to get the JSON structure
        parsed = json.loads(encoded)

        # Check if jsonpickle added type markers
        if _has_type_markers(parsed):
            # Return with metadata indicating jsonpickle encoding
            return {"json": parsed, "meta": {"encoding": "jsonpickle"}}
        else:
            # No special types, return plain JSON
            return {"json": parsed}
    except Exception:
        # Fallback: try basic serialization
        try:
            if hasattr(value, "model_dump"):  # Pydantic v2
                dumped = value.model_dump()
                if len(json.dumps(dumped, default=_safe_str)) > _MAX_SERIALIZED_BYTES:
                    return _unserializable_stub(value, "too_large_after_model_dump")
                return {"json": dumped}
            elif hasattr(value, "dict"):  # Pydantic v1
                dumped = value.dict()
                if len(json.dumps(dumped, default=_safe_str)) > _MAX_SERIALIZED_BYTES:
                    return _unserializable_stub(value, "too_large_after_dict")
                return {"json": dumped}
            else:
                return {"json": _safe_str(value)}
        except Exception:
            return {"json": _safe_str(value)}


def deserialize_value(serialized: SerializedValue) -> Any:
    """Deserialize a value that was serialized with serialize_value.

    Args:
        serialized: A SerializedValue dict with 'json' and optional 'meta'

    Returns:
        The reconstructed Python value
    """
    json_data = serialized.get("json")
    meta = serialized.get("meta")

    if not isinstance(meta, dict):
        return json_data

    if meta.get("encoding") == "jsonpickle":
        return _decode_jsonpickle(json_data)

    return json_data


def _decode_jsonpickle(json_data: Any) -> Any:
    return jsonpickle.decode(json.dumps(json_data))


def _has_type_markers(obj: Any) -> bool:
    """Check if a JSON structure contains jsonpickle type markers."""
    if isinstance(obj, dict):
        # Check for jsonpickle's type marker keys
        if any(k.startswith("py/") for k in obj):
            return True
        # Check nested values
        return any(_has_type_markers(v) for v in obj.values())
    elif isinstance(obj, list):
        return any(_has_type_markers(item) for item in obj)
    return False
