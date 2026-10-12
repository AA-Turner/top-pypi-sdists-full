from __future__ import annotations

import functools
import gzip
import logging
import os
import sys
import threading
import types
from contextvars import ContextVar
from datetime import date, datetime, time
from decimal import Decimal
from email.message import Message
from email.utils import collapse_rfc2231_value
from itertools import chain
from uuid import UUID
from typing import TYPE_CHECKING, Any, Dict, List, Tuple, TypedDict, TypeVar

import msgpack

from ._construction import CHECK as _CONSTRUCTION_CHECK
from ._construction import (
    _CPYTHON,
    _TPFLAGS_HEAPTYPE,
    _type_flags,
    may_run_user_code as _may_run_user_code,
    objects_under_construction as _objects_under_construction,
    placeholder as _construction_placeholder,
)

# The native encoder reads these two, and `_objects_under_construction`, from
# this module's globals.
from ._construction import (  # noqa: F401
    method_under_construction_repr as _method_under_construction_repr,
    under_construction_repr as _under_construction_repr,
)

logger = logging.getLogger("kolo")


if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse, StreamingHttpResponse


class UserCodeCallSite(TypedDict):
    # None when the calling frame has no source line (`f_lineno is None`).
    line_number: int | None
    call_frame_id: str


class _ValueReference:
    __slots__ = ("index",)

    def __init__(self, index: int):
        self.index = index


# Every msgpack extension code in Kolo traces. The native encoder
# (python/rust/src/utils/value_serializer.rs) and all readers (this module,
# dashboard/core/serialize.py, vscode/src/extension/msgpack.ts) must agree
# with this table; tests/test_extension_codes.py checks them. Claim a new code
# here, in RESERVED_EXTENSION_TYPES while its PR is open, before using it.
EXTENSION_TYPES = {
    0: "repr text",
    1: "datetime",
    2: "date",
    3: "time",
    4: "int outside 64 bits",
    5: "Decimal",
    6: "tuple",
    7: "set",
    8: "frozenset",
    9: "value-table reference",
    10: "str with lone surrogates",
    11: "shared list/dict reference",
    12: "value truncated by max_value_mb",
    127: "serialization error",
}
# Codes claimed by open PRs, so no other change reuses them.
RESERVED_EXTENSION_TYPES: dict[int, str] = {}

# A later occurrence of an exact list or dict already packed in the same root
# is written as this extension: the number of arrays and maps completed in the
# root's stream since the referenced one. It keeps DAG-shaped values (the same
# list referenced at many depths) linear instead of exponential. The rule is
# mirrored by the native encoder in python/rust/src/utils/value_serializer.rs.
SHARED_REFERENCE_EXTENSION_TYPE = 11
# Plain containers one root packs before identities are tracked.
SHARED_TRACKING_THRESHOLD = 1024
# Containers one root remembers at most (as natively), which bounds the
# tracking table's memory however many containers a value holds.
MAX_SHARED_CONTAINERS = 1 << 18
# A value whose encoding exceeded ``max_value_mb`` is replaced by this marker.
TRUNCATED_VALUE_EXTENSION_TYPE = 12
# How to raise the budget, appended to every truncation marker's text (as
# natively).
TRUNCATION_MARKER_HINT = "; raise max_value_mb in .kolo/config.toml or set it to false"
# A frame's weight when shared and value references are expanded: this much
# per value plus the length of each str/bytes. Readers keep shared references
# as markers past MAX_EXPANDED_WEIGHT, and refuse frames that stay heavier.
EXPANDED_VALUE_WEIGHT = 16
MAX_EXPANDED_WEIGHT = 1 << 30
# Longest type name a truncation marker repeats (as natively).
MAX_MARKER_TYPE_NAME_CHARS = 200
SHARED_VALUE_MARKER = "KoloSharedValue: repeats an earlier value, too large to expand"


class _SharedReferenceFound(ValueError):
    """Raised by the plain decoder so the frame is decoded again with the
    container numbering a shared reference needs."""


def user_code_call_site(
    call_frames: List[Tuple[types.FrameType, str]],
    frame_id: str,
) -> UserCodeCallSite | None:
    count = len(call_frames)
    if count == 0:
        return None

    call_frame, call_frame_id = call_frames[-1]

    # If `frame_id` is set in a `return` frame, we want to skip it
    if call_frame_id == frame_id:
        if count == 1:
            return None
        call_frame, call_frame_id = call_frames[-2]

    return {
        "call_frame_id": call_frame_id,
        "line_number": call_frame.f_lineno,
    }


Local = TypeVar("Local")


SERIALIZE_PATH = os.path.normpath("kolo/serialize.py")


# TODO: Make these threadlocals when we support multithreading
QUERYSET_PATCHED = False
IN_KOLO_PROFILER = False
_PACKERS = threading.local()
# msgpack 1.2 raised Packer's DEFAULT_RECURSE_LIMIT from 511.
_PACKER_RECURSE_LIMIT = 1024 if msgpack.version >= (1, 2) else 511


class DatabaseAccessBlocked(Exception):
    """Raised by Django's database layer while Kolo serializes a value.

    A `__repr__` (or `__str__`) can load a deferred field, an unloaded
    relation or a lazy object, and each of those runs a query. Kolo must never
    change what the traced program does, so the query is refused before a
    connection or cursor is touched and the value gets `_query_free_repr`.
    """


class _QueryGuard(threading.local):
    # Per thread: other threads keep querying while one serializes. The
    # native encoder keeps its own per-thread count instead (see
    # `_native_encode_in_progress`), which is far cheaper on the hot path.
    # A depth rather than a flag, so encodes that end out of order (greenlets
    # switching mid-repr) cannot leave it set.
    depth = 0


# `[found]` for the root being dumped: what `_objects_under_construction`
# found (None: not looked for yet). The stack below Kolo cannot change while
# one root is serialized, so one walk serves all its values. Each dump owns
# its list, and a context variable keeps greenlets that switch inside a
# `__repr__` from reading each other's.
_CONSTRUCTION: ContextVar = ContextVar("kolo_objects_under_construction", default=None)


try:
    # The same walk in native code, far cheaper on a deep stack; None when
    # it leaves the answer to `_objects_under_construction`.
    from kolo._kolo import _validated_objects_under_construction
except ImportError:  # pragma: no cover - PyPy and builds without the extension
    _validated_objects_under_construction = None


def _find_objects_under_construction():
    found = None
    if _validated_objects_under_construction is not None:
        found = _validated_objects_under_construction()
    if found is None:
        found = _objects_under_construction()
    return found


def _under_construction_ext(obj, lightweight=False):
    """The placeholder for an object whose constructor is still running (see
    `kolo._construction`), or None to serialize `obj` as usual."""
    if not _CONSTRUCTION_CHECK:
        return None
    kind = type(obj)
    # Spelled out for the usual case, a value of a builtin type: this runs
    # for every value the packer hands to the hook.
    if _CPYTHON and not _type_flags(kind) & _TPFLAGS_HEAPTYPE:
        if kind is not types.MethodType or not _may_run_user_code(type(obj.__self__)):
            return None
    memo = _CONSTRUCTION.get()
    if memo is None:
        found = _find_objects_under_construction()
    else:
        found = memo[0]
        if found is None:
            found = memo[0] = _find_objects_under_construction()
    if len(found) == 1:
        return None
    text = _construction_placeholder(found, obj, lightweight)
    if text is None:
        return None
    # A class name can hold lone surrogates; escape them rather than fail.
    return msgpack.ExtType(0, text.encode("utf-8", "backslashreplace"))


# Set once Django's database layer is patched, so the Python serializers cost
# nothing extra in processes that never use Django.
_QUERY_GUARD: _QueryGuard | None = None
# Concurrent first requests (or free-threaded builds) must patch Django once.
_PATCH_LOCK = threading.Lock()

# Lazy-loaded Django QuerySet (to avoid importing Django at module load time)
# This dramatically speeds up subprocess startup for emit --auto
_QuerySet = None
_QuerySet_checked = False


def _get_queryset_class():
    """Lazily import Django QuerySet, caching the result."""
    global _QuerySet, _QuerySet_checked
    if not _QuerySet_checked:
        try:
            from django.db.models import QuerySet

            _QuerySet = QuerySet
        except ImportError:
            _QuerySet = None
        _QuerySet_checked = True
    return _QuerySet


def monkeypatch_queryset_repr():
    if QUERYSET_PATCHED:
        return
    with _PATCH_LOCK:
        _monkeypatch_queryset_repr()


def _monkeypatch_queryset_repr():
    global QUERYSET_PATCHED
    if QUERYSET_PATCHED:
        return

    try:
        from django.db.models import QuerySet
    except ImportError:  # pragma: no cover
        QUERYSET_PATCHED = True
        return

    old_repr = QuerySet.__repr__

    @functools.wraps(old_repr)
    def new_repr(queryset):
        if getattr(queryset, "_result_cache", None) is None and IN_KOLO_PROFILER:
            return f"Unevaluated queryset for: {queryset.model}"
        return old_repr(queryset)

    QuerySet.__repr__ = new_repr  # type: ignore
    _install_query_guard()
    QUERYSET_PATCHED = True


REPR_EXTENSION = 0
# A str with lone surrogates, as `str.encode("utf-8", "surrogatepass")`.
SURROGATE_STR_EXTENSION = 10
# What the careful pass records (as repr text) for a container that is
# already being packed further up, as Python's repr marks a recursive
# reference.
_SEQUENCE_CYCLE_MARKERS = {6: b"(...)", 7: b"set(...)", 8: b"frozenset(...)"}
_LIST_CYCLE_MARKER = b"[...]"
_DICT_CYCLE_MARKER = b"{...}"


def _cycle_marker(marker: bytes) -> msgpack.ExtType:
    """The careful pass's repr marker for a container met again inside
    itself. Counted, so the careful pass shares only containers whose
    encoding holds no marker (and so does not depend on what encloses it)."""
    _CAREFUL.markers = getattr(_CAREFUL, "markers", 0) + 1
    return msgpack.ExtType(REPR_EXTENSION, marker)


# msgpack's own messages.
_RECURSION_LIMIT_MESSAGE = "recursion limit exceeded."
# msgpack's pure-Python packer (PyPy, Pyodide, MSGPACK_PUREPYTHON) drops the period.
_FALLBACK_RECURSION_LIMIT_MESSAGE = "recursion limit exceeded"
_RELEASED_MEMORYVIEW_MESSAGE = "operation forbidden on released memoryview object"
_CAREFUL_VALUE_ERROR_MESSAGES = (
    _RECURSION_LIMIT_MESSAGE,
    _FALLBACK_RECURSION_LIMIT_MESSAGE,
    _RELEASED_MEMORYVIEW_MESSAGE,
)
# msgpack 1.2 raised Packer's DEFAULT_RECURSE_LIMIT from 511.
_RECURSE_LIMIT = 1024 if msgpack.version >= (1, 2) else 511

# `active` is None during the usual pass, and during the careful pass the
# identities of the containers being packed (see `_dump_root`).
_CAREFUL = threading.local()


def _install_query_guard():
    global _QUERY_GUARD
    if _QUERY_GUARD is not None:
        return
    from django.db import transaction
    from django.db.backends.base.base import BaseDatabaseWrapper
    from django.db.backends.utils import CursorDebugWrapper, CursorWrapper

    try:
        from ._kolo import _native_encode_in_progress
    except ImportError:  # pragma: no cover

        def _native_encode_in_progress():
            return False

    guard = _QueryGuard()

    def guarded(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            if guard.depth or _native_encode_in_progress():
                raise DatabaseAccessBlocked(
                    f"Kolo blocked {function.__qualname__}() while serializing"
                )
            return function(*args, **kwargs)

        return wrapper

    # Refuse at the entry points, before any state changes: every query
    # creates a cursor (`_cursor`) or runs on a held one, and the other
    # connection methods here reach the driver without a cursor (or, for
    # `savepoint`, count the savepoint first). Entering `atomic()` or
    # `mark_for_rollback_on_error()` would let the refusal mark the program's
    # own transaction for rollback on its way out.
    for owner, names in (
        (
            BaseDatabaseWrapper,
            (
                "_cursor",
                "connect",
                "commit",
                "rollback",
                "set_autocommit",
                "savepoint",
                "close",
            ),
        ),
        # Ahead of `debug_sql`, which logs even a refused query.
        (CursorWrapper, ("execute", "executemany", "callproc")),
        (CursorDebugWrapper, ("execute", "executemany")),
        (transaction.Atomic, ("__enter__",)),
    ):
        for name in names:
            setattr(owner, name, guarded(getattr(owner, name)))
    transaction.mark_for_rollback_on_error = guarded(
        transaction.mark_for_rollback_on_error
    )
    _QUERY_GUARD = guard


def _plain_value_repr(value) -> str:
    # A primary key can be any object, even a lazy one that queries.
    cls = type(value)
    if value is None or cls is int or cls is str or cls is UUID:
        return repr(value)
    return f"<{cls.__qualname__}>"


_SKIPPED = "Kolo skipped repr to avoid a database query"


def _query_free_repr(obj) -> str:
    """Describe `obj` from its type and loaded state alone: the fallback
    when its `repr()` tried to use the database."""
    from django.db.models import Model

    cls = type(obj)
    if issubclass(cls, Model):
        try:
            description = _describe_instance(cls._meta, obj.__dict__)
        except Exception:
            # Only a model overriding `__dict__` or `_meta` gets here.
            pass
        else:
            return f"<{cls.__name__} {description}: {_SKIPPED}>"
    return f"<{cls.__module__}.{cls.__qualname__} object: {_SKIPPED}>"


def _describe_instance(meta, loaded) -> str:
    if getattr(meta, "is_composite_pk", False):
        parts = [
            _plain_value_repr(loaded.get(field.attname)) for field in meta.pk.fields
        ]
        pk = f"({', '.join(parts)})"
    else:
        pk = _plain_value_repr(loaded.get(meta.pk.attname))
    # `Model.get_deferred_fields()`, without calling a method a model may override.
    deferred = sorted(
        field.attname for field in meta.concrete_fields if field.attname not in loaded
    )
    if deferred:
        return f"pk={pk} deferred=[{', '.join(deferred)}]"
    return f"pk={pk}"


def msgpack_encode_hook(obj):
    try:
        skipped = _under_construction_ext(obj)
        if skipped is not None:
            return skipped

        if isinstance(obj, tuple):
            code = 6
        elif isinstance(obj, set):
            code = 7
        elif isinstance(obj, frozenset):
            code = 8
        else:
            code = 0
        if code:
            active = getattr(_CAREFUL, "active", None)
            if active is None:
                return msgpack.ExtType(code, _dump_msgpack(list(obj)))
            if id(obj) in active:
                return _cycle_marker(_SEQUENCE_CYCLE_MARKERS[code])
            active.append(id(obj))
            try:
                return msgpack.ExtType(code, _dump_msgpack_carefully(list(obj)))
            finally:
                active.pop()

        if isinstance(obj, dict):
            active = getattr(_CAREFUL, "active", None)
            if active is not None and id(obj) in active:
                return _cycle_marker(_DICT_CYCLE_MARKER)
            return dict(obj)

        if isinstance(obj, datetime):
            return msgpack.ExtType(1, obj.isoformat().encode("utf-8"))

        if isinstance(obj, date):
            return msgpack.ExtType(2, obj.isoformat().encode("utf-8"))

        if isinstance(obj, time):
            return msgpack.ExtType(3, obj.isoformat().encode("utf-8"))

        if isinstance(obj, int):
            num_bytes = (obj.bit_length() + 7) // 8 + 1
            return msgpack.ExtType(4, obj.to_bytes(num_bytes, "big", signed=True))

        if isinstance(obj, Decimal):
            return msgpack.ExtType(5, str(obj).encode("utf-8"))

        # Check for Django QuerySet (lazy import to avoid loading Django at module load)
        QuerySet = _get_queryset_class()
        if QuerySet is not None and isinstance(obj, QuerySet):
            if obj._result_cache is None:
                data = f"Unevaluated queryset for: {obj.model}".encode("utf-8")
                return msgpack.ExtType(0, data)

        return msgpack.ExtType(0, _root_repr(obj).encode("utf-8"))
    except DatabaseAccessBlocked:
        return msgpack.ExtType(0, _query_free_repr(obj).encode("utf-8"))
    except Exception as error:
        if getattr(_CAREFUL, "active", None) is None and _needs_careful(error):
            # Left to the careful pass, which records it instead.
            raise
        path = f"{obj.__module__}.{type(obj).__qualname__}"
        # A type name can hold lone surrogates; escape them rather than fail.
        return msgpack.ExtType(127, path.encode("utf-8", "backslashreplace"))


def msgpack_decode_hook(code, data):
    if code == 0:
        return data.decode("utf-8")
    if code == 1:
        return datetime.fromisoformat(data.decode("utf-8"))
    if code == 2:
        return date.fromisoformat(data.decode("utf-8"))
    if code == 3:
        return time.fromisoformat(data.decode("utf-8"))
    if code == 4:
        return int.from_bytes(data, "big", signed=True)
    if code == 5:
        return Decimal(data.decode("utf-8"))
    if code == 6 or code == 7 or code == 8:
        return _decode_sequence(code, data)
    if code == 9:
        if len(data) != 4:
            raise ValueError("Invalid Kolo value reference")
        _DECODING.value_references = True
        return _ValueReference(int.from_bytes(data, "big"))
    if code == SHARED_REFERENCE_EXTENSION_TYPE:
        raise _SharedReferenceFound("Kolo shared reference outside a frame value")
    if code == TRUNCATED_VALUE_EXTENSION_TYPE:
        return f"KoloTruncatedValue: {data.decode('utf-8')}"
    if code == SURROGATE_STR_EXTENSION:
        return data.decode("utf-8", "surrogatepass")
    if code == 127:
        data = data.decode("utf-8")
        return f"KoloSerializationError: {data}"
    raise ValueError(f"Unknown msgpack extension. Code: {code}")


def _pack_with_msgpack(name: str, default, data, careful=False, share=False):
    stack_name = f"{name}_packers"
    depth_name = f"{name}_depth"
    packers = getattr(_PACKERS, stack_name, None)
    if packers is None:
        packers = []
        setattr(_PACKERS, stack_name, packers)

    depth = getattr(_PACKERS, depth_name, 0)
    if depth == len(packers):
        packers.append(
            msgpack.Packer(default=default, strict_types=True, autoreset=True)
        )

    setattr(_PACKERS, depth_name, depth + 1)
    try:
        if careful:
            return _pack_careful(data, packers[depth], default, share)
        return packers[depth].pack(data)
    finally:
        setattr(_PACKERS, depth_name, depth)


def _needs_careful(error):
    """Whether a value that failed to pack with `error` is packed again by the
    careful pass, which records it instead: a cycle (which ends in msgpack's
    nesting limit or a RecursionError), a str with lone surrogates, or a
    released memoryview. Exact types only, so deciding runs no user code."""
    kind = type(error)
    if kind is RecursionError:
        return True
    if kind is ValueError:
        args = error.args
        return (
            len(args) == 1
            and type(args[0]) is str
            and args[0] in _CAREFUL_VALUE_ERROR_MESSAGES
        )
    if kind is UnicodeEncodeError:
        reason = error.reason
        return type(reason) is str and reason == "surrogates not allowed"
    return False


def _is_released_memoryview_error(error):
    args = error.args
    return (
        type(error) is ValueError
        and len(args) == 1
        and type(args[0]) is str
        and args[0] == _RELEASED_MEMORYVIEW_MESSAGE
    )


# Compared by identity: hashing a type can run its metaclass's `__hash__`.
_PACKED_WITHOUT_DEFAULT = (
    type(None),
    bool,
    int,
    float,
    bytes,
    bytearray,
    msgpack.ExtType,
    msgpack.Timestamp,
)
_DONE: Any = object()


def _pack_careful(value, packer, default, share):
    """`packer.pack(value)`, except that a list or dict already being packed
    further up is recorded as a cycle marker, a str with lone surrogates as a
    `SURROGATE_STR_EXTENSION`, and a released memoryview as its repr.

    Mirrors msgpack's Packer (and its nesting limit) for the containers it
    walks itself, without recursing, and leaves leaves to `packer`. Lists and
    dicts are packed as they were when packing them started, as the native
    encoder packs them. Repeated lists and dicts become shared references
    under the same rule as `_SharedValueEncoder` (with a table of its own),
    so a shared value stays as compact as in the first pass, except that a
    container whose encoding holds a cycle marker is never shared: packed
    again elsewhere it would mark different containers. Only a root
    shares (``share``): tuple and set payloads never hold shared references.
    """
    active = _CAREFUL.active
    base = len(active)
    parts = []
    entered = 0
    completed = 0
    numbers: dict[int, int] | None = None
    # Keeps remembered containers alive so their ids are not reused.
    pins: list = []
    # Each entry: the values left to pack, the nesting limit they are packed
    # at, the container finishing them completes (with whether it may be
    # remembered) or None, and whether those values may be shared.
    stack: list = [(iter((value,)), _RECURSE_LIMIT, None, share)]
    try:
        while stack:
            values, limit, container, shareable = stack[-1]
            item = next(values, _DONE)
            if item is _DONE:
                stack.pop()
                if container is not None:
                    active.pop()
                    if numbers is not None:
                        obj, remember, markers = container
                        # A container holding a cycle marker is encoded
                        # relative to what encloses it: not shared.
                        if (
                            remember
                            and markers == getattr(_CAREFUL, "markers", 0)
                            and len(obj) >= 2
                            and len(numbers) < MAX_SHARED_CONTAINERS
                        ):
                            numbers[id(obj)] = completed
                            pins.append(obj)
                        completed += 1
                continue
            if limit < 0:
                raise ValueError(_RECURSION_LIMIT_MESSAGE)
            limit -= 1
            kind = type(item)
            if kind is list or kind is dict:
                if shareable:
                    if numbers is None:
                        entered += 1
                        if entered >= SHARED_TRACKING_THRESHOLD:
                            numbers = {}
                    else:
                        number = numbers.get(id(item))
                        if number is not None and completed - 1 - number <= 0xFFFFFFFF:
                            distance = (completed - 1 - number).to_bytes(4, "big")
                            parts.append(
                                packer.pack(
                                    msgpack.ExtType(
                                        SHARED_REFERENCE_EXTENSION_TYPE, distance
                                    )
                                )
                            )
                            continue
                if id(item) in active:
                    marker = _LIST_CYCLE_MARKER if kind is list else _DICT_CYCLE_MARKER
                    parts.append(packer.pack(_cycle_marker(marker)))
                    continue
                source = item
                remember = shareable
            elif kind is str:
                try:
                    parts.append(packer.pack(item))
                except UnicodeEncodeError:
                    data = item.encode("utf-8", "surrogatepass")
                    parts.append(
                        packer.pack(msgpack.ExtType(SURROGATE_STR_EXTENSION, data))
                    )
                continue
            elif kind is memoryview:
                try:
                    parts.append(packer.pack(item))
                except ValueError as error:
                    if not _is_released_memoryview_error(error):
                        raise
                    text = _root_repr(item).encode("utf-8")
                    parts.append(packer.pack(msgpack.ExtType(REPR_EXTENSION, text)))
                continue
            elif any(kind is packed for packed in _PACKED_WITHOUT_DEFAULT):
                parts.append(packer.pack(item))
                continue
            else:
                # As msgpack does: `o = default(o)`, then pack `o` itself.
                source = item
                item = default(item)
                if type(item) is not dict:
                    parts.append(packer.pack(item))
                    continue
                # `dict(obj)` for a dict subclass stands for `obj`. It counts
                # as completed but, like everything in it, is never shared.
                remember = False
            active.append(id(source))
            completes = (item, remember, getattr(_CAREFUL, "markers", 0))
            if type(item) is list:
                items = list(item)
                parts.append(packer.pack_array_header(len(items)))
                stack.append((iter(items), limit, completes, remember))
            else:
                entries = list(item.items())
                parts.append(packer.pack_map_header(len(entries)))
                stack.append((chain.from_iterable(entries), limit, completes, remember))
    finally:
        del active[base:]
    return b"".join(parts)


def _dump_root(dump, dump_carefully, data):
    """`dump(data)`, then for a value it fails on as `_needs_careful` decides,
    `dump_carefully(data)` instead. Only such values pay for the second pass;
    the native encoder makes the same two passes."""
    saved = getattr(_CAREFUL, "active", None)
    saved_reprs = getattr(_CAREFUL, "reprs", None)
    _CAREFUL.active = None
    # A memo opened by the caller (dump_frame_msgpack) spans its dumps.
    _CAREFUL.reprs = {} if saved_reprs is None else saved_reprs
    try:
        try:
            return dump(data)
        except Exception as error:
            # The careful pass shares repeated containers too, so a shared
            # value is not expanded there either.
            if not _needs_careful(error):
                raise
        _CAREFUL.active = []
        return dump_carefully(data, True)
    finally:
        _CAREFUL.active = saved
        _CAREFUL.reprs = saved_reprs


# As `REPR_MEMO_CAPACITY` in value_serializer.rs.
_REPR_MEMO_CAPACITY = 1024


def _root_repr(obj):
    """`repr(obj)`, run at most once per object in one root `dump_msgpack`, so
    the careful pass reuses the first pass's reprs as the native encoder's
    memo does. Memoized objects stay referenced, so ids cannot be reused."""
    reprs = getattr(_CAREFUL, "reprs", None)
    if reprs is None:
        return repr(obj)
    hit = reprs.get(id(obj))
    if hit is not None:
        return hit[1]
    text = repr(obj)
    if type(text) is str and len(reprs) < _REPR_MEMO_CAPACITY:
        reprs[id(obj)] = (obj, text)
    return text


def _dump_msgpack(data):
    return _pack_with_msgpack("default", msgpack_encode_hook, data)


def _dump_msgpack_carefully(data, share=False):
    return _pack_with_msgpack("default", msgpack_encode_hook, data, True, share)


def dump_msgpack(data, may_share=None):
    """``may_share`` is ``_may_share(data)`` when the caller already has it."""
    global IN_KOLO_PROFILER
    IN_KOLO_PROFILER = True
    guard = _QUERY_GUARD
    if guard is not None:
        guard.depth += 1
    construction = _CONSTRUCTION.set([None])
    try:
        if may_share is None:
            may_share = _may_share(data)
        if may_share and _replay_shared_reference_rule(data):
            return _dump_root(
                _SharedValueEncoder(msgpack_encode_hook).encode,
                _dump_msgpack_carefully,
                data,
            )
        return _dump_root(_dump_msgpack, _dump_msgpack_carefully, data)
    finally:
        IN_KOLO_PROFILER = False
        if guard is not None:
            guard.depth -= 1
        try:
            _CONSTRUCTION.reset(construction)
        except ValueError:  # pragma: no cover - ended in another context
            _CONSTRUCTION.set(None)


def msgpack_encode_hook_lightweight_repr(obj):
    try:
        return _lightweight_repr_ext(obj)
    except DatabaseAccessBlocked:
        # `obj.__class__` can still evaluate a lazy object.
        return msgpack.ExtType(0, _query_free_repr(obj).encode("utf-8"))


def _lightweight_repr_ext(obj):
    skipped = _under_construction_ext(obj, True)
    if skipped is not None:
        return skipped

    if isinstance(obj, tuple):
        code = 6
    elif isinstance(obj, set):
        code = 7
    elif isinstance(obj, frozenset):
        code = 8
    else:
        code = 0
    if code:
        active = getattr(_CAREFUL, "active", None)
        if active is None:
            return msgpack.ExtType(code, _dump_lightweight(list(obj)))
        if id(obj) in active:
            return _cycle_marker(_SEQUENCE_CYCLE_MARKERS[code])
        active.append(id(obj))
        try:
            return msgpack.ExtType(code, _dump_lightweight_carefully(list(obj)))
        finally:
            active.pop()

    if isinstance(obj, dict):
        active = getattr(_CAREFUL, "active", None)
        if active is not None and id(obj) in active:
            return _cycle_marker(_DICT_CYCLE_MARKER)
        return dict(obj)

    if isinstance(obj, datetime):
        return msgpack.ExtType(1, obj.isoformat().encode("utf-8"))

    if isinstance(obj, date):
        return msgpack.ExtType(2, obj.isoformat().encode("utf-8"))

    if isinstance(obj, time):
        return msgpack.ExtType(3, obj.isoformat().encode("utf-8"))

    if isinstance(obj, int):
        num_bytes = (obj.bit_length() + 7) // 8 + 1
        return msgpack.ExtType(4, obj.to_bytes(num_bytes, "big", signed=True))

    if isinstance(obj, Decimal):
        return msgpack.ExtType(5, str(obj).encode("utf-8"))

    return msgpack.ExtType(
        0, f"<{obj.__class__.__qualname__} object {id(obj)}>".encode("utf-8")
    )


def _dump_lightweight(data):
    return _pack_with_msgpack("lightweight", msgpack_encode_hook_lightweight_repr, data)


def _dump_lightweight_carefully(data, share=False):
    return _pack_with_msgpack(
        "lightweight", msgpack_encode_hook_lightweight_repr, data, True, share
    )


def dump_msgpack_lightweight_repr(data, may_share=None):
    guard = _QUERY_GUARD
    if guard is not None:
        guard.depth += 1
    construction = _CONSTRUCTION.set([None])
    try:
        if may_share is None:
            may_share = _may_share(data)
        if may_share and _replay_shared_reference_rule(data):
            return _dump_root(
                _SharedValueEncoder(msgpack_encode_hook_lightweight_repr).encode,
                _dump_lightweight_carefully,
                data,
            )
        return _dump_root(_dump_lightweight, _dump_lightweight_carefully, data)
    finally:
        if guard is not None:
            guard.depth -= 1
        try:
            _CONSTRUCTION.reset(construction)
        except ValueError:  # pragma: no cover - ended in another context
            _CONSTRUCTION.set(None)


_PLAIN_CONTAINER_TYPE_IDS = frozenset({id(list), id(dict)})

try:
    # The same count natively, so the Python backends pay almost nothing per
    # frame for values too small to start tracking.
    from kolo._kolo import _count_plain_containers
except ImportError:  # pragma: no cover - PyPy and builds without the extension
    _count_plain_containers = None


def _may_share(root) -> bool:
    """Whether ``root`` reaches ``SHARED_TRACKING_THRESHOLD`` exact lists and
    dicts (counting repeats), so that tracking, and so a reference, can start.
    """
    if type(root) is not list and type(root) is not dict:
        return False
    if _count_plain_containers is not None:
        return (
            _count_plain_containers(root, SHARED_TRACKING_THRESHOLD)
            >= SHARED_TRACKING_THRESHOLD
        )
    # Counting needs no order or identities, and C-level type scans skip
    # containers without nested ones.
    pending: list[Any] = [root]
    entered = 0
    while pending:
        node = pending.pop()
        entered += 1
        if entered >= SHARED_TRACKING_THRESHOLD:
            return True
        children = node if type(node) is list else node.values()
        # Type identities, so no user-defined type is hashed or compared.
        if not _PLAIN_CONTAINER_TYPE_IDS.isdisjoint(map(id, map(type, children))):
            for child in children:
                if type(child) is list or type(child) is dict:
                    pending.append(child)
                    # Every pending container counts once popped.
                    if entered + len(pending) >= SHARED_TRACKING_THRESHOLD:
                        return True
    return False


def _replay_shared_reference_rule(root) -> bool:
    """Whether the first pass over ``root`` writes a shared reference anywhere.
    A list or dict already open further up (a cycle, which fails the first
    pass either way) is not followed again. Picks the first pass's encoder:
    when this returns False, msgpack's own packer writes the same bytes as
    the native encoder."""
    entered = 0
    remembered: set[int] | None = None
    open_ids: set[int] = set()
    stack: list = []
    container: Any = root
    while True:
        if container is not None:
            identity = id(container)
            if remembered is None:
                entered += 1
                if entered >= SHARED_TRACKING_THRESHOLD:
                    remembered = set()
            elif identity in remembered:
                return True
            if identity not in open_ids:
                open_ids.add(identity)
                items = container if type(container) is list else container.values()
                stack.append((container, iter(items)))
            container = None
        if not stack:
            return False
        current, items = stack[-1]
        for item in items:
            if type(item) is list or type(item) is dict:
                container = item
                break
        else:
            stack.pop()
            open_ids.discard(id(current))
            if (
                remembered is not None
                and len(current) >= 2
                and len(remembered) < MAX_SHARED_CONTAINERS
            ):
                remembered.add(id(current))


_NATIVE_LEAF_TYPES = frozenset(
    {
        type(None),
        bool,
        int,
        float,
        str,
        bytes,
        bytearray,
        memoryview,
        msgpack.ExtType,
        msgpack.Timestamp,
    }
)


class _SharedValueEncoder:
    """``Packer(default=hook, strict_types=True).pack`` with shared references.

    Only used for values whose first pass writes a shared reference (see
    ``_replay_shared_reference_rule``). Like the native encoder it packs each
    list and dict as it was when packing it started.
    """

    def __init__(self, default):
        self.default = default
        self.leaf_packer = msgpack.Packer(
            default=default, strict_types=True, autoreset=True
        )
        self.out = bytearray()
        self.entered = 0
        self.completed = 0
        self.numbers: dict[int, int] | None = None
        # Keeps remembered containers alive so their ids are not reused.
        self.pins: list = []

    def encode(self, data) -> bytes:
        # An explicit work stack, so nesting is bounded by msgpack's limit as
        # with its own packer, not by Python's recursion limit. Each entry is
        # a value to pack (with its nest limit and whether it may be shared)
        # or, with nest limit None, a container to complete.
        stack: list = [(data, _PACKER_RECURSE_LIMIT, True)]
        while stack:
            obj, nest_limit, shareable = stack.pop()
            if nest_limit is None:
                self.complete(obj, shareable)
            else:
                self.pack(obj, nest_limit, shareable, stack)
        return bytes(self.out)

    def pack(self, obj, nest_limit, shareable, stack):
        if nest_limit < 0:
            raise ValueError("recursion limit exceeded.")
        nest_limit -= 1
        obj_type = type(obj)
        if obj_type is not list and obj_type is not dict:
            if obj_type in _NATIVE_LEAF_TYPES:
                self.out += self.leaf_packer.pack(obj)
                return
            obj = self.default(obj)
            if type(obj) is not dict:
                # The hooks only return an ExtType or a dict.
                self.out += self.leaf_packer.pack(obj)
                return
            shareable = False

        if shareable:
            if self.numbers is None:
                self.entered += 1
                if self.entered >= SHARED_TRACKING_THRESHOLD:
                    self.numbers = {}
            else:
                number = self.numbers.get(id(obj))
                if number is not None and self.completed - 1 - number <= 0xFFFFFFFF:
                    distance = self.completed - 1 - number
                    self.out += self.leaf_packer.pack(
                        msgpack.ExtType(
                            SHARED_REFERENCE_EXTENSION_TYPE, distance.to_bytes(4, "big")
                        )
                    )
                    return
        stack.append((obj, None, shareable))
        if type(obj) is list:
            items = list(obj)
            self.out += self.leaf_packer.pack_array_header(len(items))
            for item in reversed(items):
                stack.append((item, nest_limit, shareable))
        else:
            entries = list(obj.items())
            self.out += self.leaf_packer.pack_map_header(len(entries))
            for key, value in reversed(entries):
                stack.append((value, nest_limit, shareable))
                stack.append((key, nest_limit, shareable))

    def complete(self, obj, shareable):
        if self.numbers is not None:
            if (
                shareable
                and len(obj) >= 2
                and len(self.numbers) < MAX_SHARED_CONTAINERS
            ):
                self.numbers[id(obj)] = self.completed
                self.pins.append(obj)
            self.completed += 1


_TYPE_MRO = vars(type)["__mro__"].__get__
_TYPE_DICT = vars(type)["__dict__"].__get__


def _type_defines(cls, name: str) -> bool:
    """Whether ``cls`` fills the type slot behind ``name``, as ``PyIter_Check``
    and ``PyAIter_Check`` read it: a class on the MRO defines the name (even
    as ``None``). Read through ``type``'s own descriptors, so that no
    metaclass attribute, hook or property runs."""
    for klass in _TYPE_MRO(cls):
        if name in _TYPE_DICT(klass):
            return True
    return False


_COMPREHENSIONS = frozenset(("<genexpr>", "<listcomp>", "<setcomp>", "<dictcomp>"))

# Whether the interpreter passes a generator expression its iterable rather
# than an iterator (see ``hide_implicit_iterable``). Callers on the per-event
# path test this instead of paying for a call on older versions.
IMPLICIT_ITERABLE_IS_RAW = sys.version_info >= (3, 15)


def hide_implicit_iterable(frame, frame_locals: Dict[str, Any]) -> None:
    """Record the iterable a generator expression was called with by identity.

    Up to CPython 3.14 the caller of a generator expression (or of a
    comprehension that is not inlined) runs ``iter()`` and passes the iterator
    as the implicit ``.0`` argument, recorded as ``<list_iterator object at
    0x...>``. From 3.15 the caller passes the iterable itself, so ``.0`` holds
    the whole collection for the life of the frame: recorded like any other
    local, a generator expression over ``n`` items would write all ``n`` of
    them at its call, return, and every yield and resume. ``.0`` is not a name
    the program wrote, so on 3.15 a value that is not already an iterator is
    recorded as ``object.__repr__`` shows it: its type and address, as on
    earlier versions.

    Only call this when ``IMPLICIT_ITERABLE_IS_RAW``. ``frame_locals`` is a
    copy Kolo owns and is changed in place. Mirrors
    ``hide_implicit_iterable`` in the Rust frame writer.
    """
    if ".0" not in frame_locals:
        return
    # Only the compiler's implicit argument: a ".0" key in the namespace
    # given to exec(), or a parameter of a function built from an AST, is the
    # program's own.
    code = frame.f_code
    if code.co_varnames[:1] != (".0",) or code.co_name not in _COMPREHENSIONS:
        return
    iterable = frame_locals[".0"]
    cls = type(iterable)
    if _type_defines(cls, "__next__"):
        return
    # An async iterator that can also be iterated synchronously (``__iter__``
    # or the sequence protocol) may be the collection a synchronous generator
    # expression iterates: only one that cannot be is kept.
    if (
        _type_defines(cls, "__anext__")
        and not _type_defines(cls, "__iter__")
        and not _type_defines(cls, "__getitem__")
    ):
        return
    frame_locals[".0"] = object.__repr__(iterable)


def truncation_marker(value, max_value_bytes: int) -> msgpack.ExtType:
    """What the native frame writer records for a value over ``max_value_mb``."""
    # As natively, a type whose name cannot be read still gets a marker. A
    # metaclass may compute the name: keep the query guard on meanwhile, as
    # the native encoder does.
    guard = _QUERY_GUARD
    if guard is not None:
        guard.depth += 1
    try:
        qualname = type(value).__qualname__
    except Exception:  # noqa: BLE001
        qualname = "object"
    finally:
        if guard is not None:
            guard.depth -= 1
    if not isinstance(qualname, str):
        qualname = "object"
    # An exact str (a str subclass's overrides never run), with lone
    # surrogates escaped, as natively.
    qualname = str.__getitem__(qualname, slice(0, MAX_MARKER_TYPE_NAME_CHARS))
    text = f"{qualname} exceeded max_value_mb ({max_value_bytes} bytes){TRUNCATION_MARKER_HINT}"
    return msgpack.ExtType(
        TRUNCATED_VALUE_EXTENSION_TYPE, text.encode("utf-8", "backslashreplace")
    )


_FRAME_ENVELOPE_KEYS = frozenset(
    {
        "path",
        "co_name",
        "qualname",
        "event",
        "frame_id",
        "timestamp",
        "type",
        "user_code_call_site",
    }
)
# Plugin frames also carry a subtype. Mirrored by ENVELOPE_KEYS in
# value_serializer.rs.
_ENVELOPE_KEYS = _FRAME_ENVELOPE_KEYS | {"subtype"}


def _size_in_tuple_payload(dump, value) -> int:
    """Bytes ``value`` takes inside a tuple payload, which never holds shared
    references (so it can be larger than ``dump(value)``), as the native
    writer budgets an assignment's value."""
    payload = msgpack.unpackb(dump((value,)), ext_hook=lambda code, data: data)
    # Minus the one-item array header.
    return len(payload) - 1


def dump_frame_msgpack(dump, frame_data, max_value_bytes: int | None) -> bytes:
    """``dump(frame_data)`` with each value over ``max_value_bytes`` replaced
    by a truncation marker, as the native writers record it: a value whose
    own encoding is larger than the budget becomes a marker, and an oversized
    ``locals`` dict is capped per variable instead. Plugin frames (any other
    ``type``) are capped per value once the frame as a whole is over budget,
    as the native plugin processor does.
    """
    # Checked once per frame: the dump and the cap below both need it.
    may_share = _may_share(frame_data)
    if max_value_bytes is None:
        return dump(frame_data, may_share=may_share)
    # Every dump of this frame, as natively every root of one event, shares
    # one repr memo: a `__repr__` that answers differently on each call
    # cannot make a value measure small and then be recorded large.
    saved_reprs = getattr(_CAREFUL, "reprs", None)
    memo = {} if saved_reprs is None else saved_reprs
    _CAREFUL.reprs = memo
    try:
        return _dump_frame_capped(dump, frame_data, max_value_bytes, may_share)
    finally:
        _CAREFUL.reprs = saved_reprs
        if saved_reprs is None and memo:
            # Releasing memoized objects can run their finalizers: keep the
            # query guard on meanwhile, as the native encoder does.
            guard = _QUERY_GUARD
            if guard is not None:
                guard.depth += 1
            try:
                memo.clear()
            finally:
                if guard is not None:
                    guard.depth -= 1


def _dump_frame_capped(dump, frame_data, max_value_bytes, may_share):
    data = dump(frame_data, may_share=may_share)
    # Each value is its own root natively. Here the whole frame is one, so a
    # shared reference can make a value smaller than it is on its own.
    if len(data) <= max_value_bytes and not may_share:
        return data
    is_frame = frame_data.get("type") == "frame"
    if not is_frame and len(data) <= max_value_bytes:
        # Natively a plugin frame is one root, so it fits as it is.
        return data
    capped = dict(frame_data)
    for key, value in frame_data.items():
        # A frame's (or plugin frame's) envelope is never capped: readers
        # pair and dispatch frames by it.
        if (type(key) is str and key in _ENVELOPE_KEYS) or len(
            dump(value)
        ) <= max_value_bytes:
            continue
        if not is_frame:
            capped[key] = truncation_marker(value, max_value_bytes)
        elif key == "assign" and type(value) is tuple and len(value) == 2:
            name, assigned = value
            if _size_in_tuple_payload(dump, assigned) > max_value_bytes:
                capped[key] = (name, truncation_marker(assigned, max_value_bytes))
        elif key == "locals" and type(value) is dict:
            capped[key] = {
                name: (
                    local
                    if len(dump(local)) <= max_value_bytes
                    else truncation_marker(local, max_value_bytes)
                )
                for name, local in value.items()
            }
        else:
            capped[key] = truncation_marker(value, max_value_bytes)
    return dump(capped)


class _HashableDict(dict):
    """A decoded map where Python needs a hashable value (a set element or a
    dict key): Kolo records a hashable dict subclass as a plain map."""

    __hash__ = object.__hash__  # type: ignore[assignment]


class _HashableSet(set):
    __hash__ = object.__hash__  # type: ignore[assignment]

    def __repr__(self):
        return repr(set(self))


class _HashableTuple(tuple):
    __hash__ = object.__hash__


def _hashable(value):
    kind = type(value)
    if kind is dict:
        return _HashableDict(value)
    if kind is set:
        return _HashableSet(value)
    if kind is tuple:
        return _HashableTuple(value)
    return value


def _sequence(code, items):
    if code == 6:
        return tuple(items)
    kind = set if code == 7 else frozenset
    try:
        return kind(items)
    except TypeError:
        return kind(_hashable(item) for item in items)


def _dict_from_pairs(pairs):
    try:
        return dict(pairs)
    except TypeError:
        return {_hashable(key): value for key, value in pairs}


def _dict_from_flat_items(items):
    """``_dict_from_pairs`` over ``[key, value, key, value, ...]``, without
    materializing the pairs: a huge dict costs no copies on top of ``items``."""
    try:
        pairs = iter(items)
        return dict(zip(pairs, pairs))
    except TypeError:
        pairs = iter(items)
        return {_hashable(key): value for key, value in zip(pairs, pairs)}


def _unpack(data):
    try:
        return msgpack.unpackb(data, strict_map_key=False, ext_hook=msgpack_decode_hook)
    except TypeError:
        # A map key that decoded unhashable.
        return msgpack.unpackb(
            data,
            strict_map_key=False,
            ext_hook=msgpack_decode_hook,
            object_pairs_hook=_dict_from_pairs,
        )


def _raw_ext_hook(code, data):
    if code == SURROGATE_STR_EXTENSION:
        return data.decode("utf-8", "surrogatepass")
    return msgpack.ExtType(code, data)


def load_msgpack_raw(data):
    """`msgpack.unpackb` without Kolo's extension hook (extensions other than
    a str with lone surrogates stay `msgpack.ExtType`), for reading a frame's
    fields, including frames whose map keys decode unhashable."""
    try:
        return msgpack.unpackb(data, strict_map_key=False, ext_hook=_raw_ext_hook)
    except TypeError:
        return msgpack.unpackb(
            data,
            strict_map_key=False,
            ext_hook=_raw_ext_hook,
            object_pairs_hook=_dict_from_pairs,
        )


def escape_surrogates(text: str) -> str:
    """`text` with lone surrogates written as `\\udxxx` escapes, for names,
    paths and database columns that need valid UTF-8."""
    return text.encode("utf-8", "backslashreplace").decode("utf-8")


class _DeferredSequence:
    __slots__ = ("code", "data")

    def __init__(self, code, data):
        self.code = code
        self.data = data


# Each nested tuple/set/frozenset payload re-enters msgpack's unpacker, which
# keeps about 40 KiB on the C stack, so deep nesting crashed the reader with a
# C stack overflow. Payloads nested deeper than this are decoded by
# `_materialize` instead, without recursing.
_EAGER_SEQUENCE_DEPTH = 4
_DECODING = threading.local()


def _decode_sequence(code, data):
    depth = getattr(_DECODING, "depth", 0)
    if depth >= _EAGER_SEQUENCE_DEPTH:
        _DECODING.deferred = True
        return _DeferredSequence(code, data)
    _DECODING.depth = depth + 1
    try:
        items = _unpack(data)
    finally:
        _DECODING.depth = depth
    return _sequence(code, items)


def load_msgpack_value(data):
    """Decode one value. Shared references are only valid in trace frames,
    which ``load_frame`` decodes; anywhere else they fail."""
    outer_deferred = getattr(_DECODING, "deferred", False)
    _DECODING.deferred = False
    try:
        value = _unpack(data)
        if _DECODING.deferred:
            value = _materialize(value, None)
        return value
    finally:
        _DECODING.deferred = outer_deferred


def _referenced(reference, table):
    try:
        return table[reference.index]
    except (IndexError, KeyError) as exc:
        raise ValueError(f"Invalid Kolo value reference: {reference.index}") from exc


_LIST = 1
_DICT = 2
_NOTHING = object()


def _materialize(value, table):
    """`value` with its deferred sequences decoded and, given a `table`, its
    value references resolved; rebuilt without recursing, however deep."""
    stack: list = []
    while True:
        kind = type(value)
        result = _NOTHING
        if kind is _DeferredSequence:
            depth = getattr(_DECODING, "depth", 0)
            # Nested sequences come back deferred too.
            _DECODING.depth = _EAGER_SEQUENCE_DEPTH
            try:
                items = _unpack(value.data)
            finally:
                _DECODING.depth = depth
            stack.append((value.code, iter(items), []))
        elif kind is list:
            stack.append((_LIST, iter(value), []))
        elif kind is dict or kind is _HashableDict:
            stack.append((_DICT, chain.from_iterable(value.items()), []))
        elif kind is tuple or kind is _HashableTuple:
            stack.append((6, iter(value), []))
        elif kind is set or kind is _HashableSet:
            stack.append((7, iter(value), []))
        elif kind is frozenset:
            stack.append((8, iter(value), []))
        elif kind is _ValueReference and table is not None:
            result = _referenced(value, table)
        else:
            result = value
        while stack:
            code, items, built = stack[-1]
            if result is not _NOTHING:
                built.append(result)
            value = next(items, _NOTHING)
            if value is not _NOTHING:
                break
            stack.pop()
            if code == _LIST:
                result = built
            elif code == _DICT:
                result = _dict_from_pairs(list(zip(built[::2], built[1::2])))
            else:
                result = _sequence(code, built)
        else:
            return result


def _load_with_shared_references(data):
    completed = []
    # Containers handed out for a reference (kept alive by `completed`).
    referenced = set()

    def track(container):
        completed.append(container)
        return container

    def ext_hook(code, payload):
        if code != SHARED_REFERENCE_EXTENSION_TYPE:
            return msgpack_decode_hook(code, payload)
        # Only containers completed earlier can be referenced, so there are no
        # self or forward references.
        index = len(completed) - 1 - _shared_reference_distance(payload)
        if index < 0:
            raise ValueError("Invalid Kolo shared reference")
        referenced.add(id(completed[index]))
        return completed[index]

    def track_map(pairs):
        # Kolo never writes a reference as a map key (as the VS Code reader
        # enforces too).
        for key, _ in pairs:
            if id(key) in referenced and (type(key) is list or type(key) is dict):
                raise ValueError("Invalid Kolo shared reference as a map key")
        return track(_dict_from_pairs(pairs))

    # Maps complete through `object_pairs_hook`, in the same order, so a key
    # that decodes unhashable still decodes (see `_dict_from_pairs`).
    return msgpack.unpackb(
        data,
        strict_map_key=False,
        ext_hook=ext_hook,
        list_hook=track,
        object_pairs_hook=track_map,
    )


def _shared_reference_distance(payload):
    if len(payload) != 4:
        raise ValueError("Invalid Kolo shared reference")
    return int.from_bytes(payload, "big")


def _shared_reference_marker_hook(code, payload):
    if code != SHARED_REFERENCE_EXTENSION_TYPE:
        return msgpack_decode_hook(code, payload)
    _shared_reference_distance(payload)
    return SHARED_VALUE_MARKER


def load_frame(data, value_table, max_expanded_weight=MAX_EXPANDED_WEIGHT):
    """Decode one trace frame and resolve its references.

    References let a few bytes stand for a large value: a shared reference
    repeats a container and a value reference a string of up to 16 MB.
    Everything that walks a decoded frame (repr, pprint, ==, JSON) pays for
    the expanded value, which for a DAG or a crafted trace is exponential. So
    a frame is weighed as expanded (``EXPANDED_VALUE_WEIGHT`` per value plus
    the length of each str/bytes, counting shared values wherever they
    appear). Past ``max_expanded_weight`` its shared references stay
    ``SHARED_VALUE_MARKER``; if it is still too heavy, decoding fails.
    """
    outer_deferred = getattr(_DECODING, "deferred", False)
    _DECODING.deferred = False
    _DECODING.value_references = False
    try:
        try:
            value = _unpack(data)
            shared = False
        except _SharedReferenceFound:
            _DECODING.deferred = False
            value = _load_with_shared_references(data)
            shared = True
        if not shared and not _DECODING.value_references and not _DECODING.deferred:
            # Without references a frame decodes to fresh objects no larger
            # than its bytes, and there is nothing to resolve. Deferred deep
            # payloads (which may hold value references) decode in `_resolve`.
            return value
        value, weight = _resolve(value, value_table, {}, max_expanded_weight)
        if weight <= max_expanded_weight:
            return value
        if shared:
            value = _unpack_with_hook(data, _shared_reference_marker_hook)
            value, weight = _resolve(value, value_table, {}, max_expanded_weight)
            if weight <= max_expanded_weight:
                return value
        raise ValueError(
            f"Kolo frame expands past {max_expanded_weight} (weight of its values)"
        )
    finally:
        _DECODING.deferred = outer_deferred


def _unpack_with_hook(data, ext_hook):
    try:
        return msgpack.unpackb(data, strict_map_key=False, ext_hook=ext_hook)
    except TypeError:
        return msgpack.unpackb(
            data,
            strict_map_key=False,
            ext_hook=ext_hook,
            object_pairs_hook=_dict_from_pairs,
        )


def _resolve(value, table, resolved, limit):
    """Resolve value references in ``value``, returning it with its expanded
    weight (capped just past ``limit``). Each container resolves once, so the
    result stays shared and the walk linear in the decoded (not expanded)
    size. An explicit stack keeps nesting from hitting the recursion limit.
    """
    leaf = _resolve_leaf(value, table)
    if leaf is not None:
        return leaf
    # Each entry: the container, an iterator over its items (keys and values
    # alternating for a dict), its resolved items so far, and its weight.
    stack: list[list[Any]] = [
        [value, _container_items(value), [], EXPANDED_VALUE_WEIGHT]
    ]
    while True:
        entry = stack[-1]
        for item in entry[1]:
            hit = _resolve_leaf(item, table) or resolved.get(id(item))
            if hit is None:
                stack.append([item, _container_items(item), [], EXPANDED_VALUE_WEIGHT])
                break
            entry[2].append(hit[0])
            entry[3] = min(entry[3] + hit[1], limit + 1)
        else:
            stack.pop()
            container, _, items, weight = entry
            done = (_rebuild(container, items), weight)
            # Keyed by identity, so the entry keeps `container` alive: a
            # container decoded from a deferred payload is otherwise freed
            # once resolved, and a later one could reuse its id.
            resolved[id(container)] = (*done, container)
            if not stack:
                return done
            stack[-1][2].append(done[0])
            stack[-1][3] = min(stack[-1][3] + weight, limit + 1)


def _container_items(container):
    if type(container) is _DeferredSequence:
        # A payload nested too deep to decode eagerly (see `_decode_sequence`);
        # payloads hold no shared references, so it is decoded once here.
        depth = getattr(_DECODING, "depth", 0)
        _DECODING.depth = _EAGER_SEQUENCE_DEPTH
        try:
            return iter(_unpack(container.data))
        finally:
            _DECODING.depth = depth
    if isinstance(container, dict):
        return iter([part for pair in container.items() for part in pair])
    return iter(container)


def _rebuild(container, items):
    kind = type(container)
    if kind is _DeferredSequence:
        return _sequence(container.code, items)
    if isinstance(container, dict):
        rebuilt = _dict_from_flat_items(items)
        return _HashableDict(rebuilt) if kind is _HashableDict else rebuilt
    if isinstance(container, list):
        return items
    if isinstance(container, tuple):
        return _HashableTuple(items) if kind is _HashableTuple else tuple(items)
    if isinstance(container, set):
        rebuilt_set = _sequence(7, items)
        return _HashableSet(rebuilt_set) if kind is _HashableSet else rebuilt_set
    return _sequence(8, items)


# Conservative rendered sizes for the expanded weight: repr and JSON escape
# a quote or backslash as two characters, a control or non-ASCII character
# as up to twelve (`\\UXXXXXXXX`, its backslash escaped again in JSON), and
# a non-ASCII character takes up to four UTF-8 bytes.
_RENDERED_DATE_TIME_WEIGHT = 128


def _text_weight(text):
    if text.isascii() and text.isprintable():
        return 2 * len(text)
    # Up to `\\U000e0001` per code point in a repr, its backslash escaped
    # again in JSON.
    return 12 * len(text)


def _resolve_leaf(value, table):
    """``(value, weight)`` for anything but a container, with value
    references resolved; ``None`` for a container."""
    if isinstance(value, _ValueReference):
        try:
            value = table[value.index]
        except (IndexError, KeyError) as exc:
            raise ValueError(f"Invalid Kolo value reference: {value.index}") from exc
    if isinstance(value, str):
        return value, EXPANDED_VALUE_WEIGHT + _text_weight(value)
    if isinstance(value, bytes):
        # `\\xNN` in a repr, escaped again in JSON.
        return value, EXPANDED_VALUE_WEIGHT + 6 * len(value)
    if isinstance(value, int):
        # Rendered in decimal: at most one digit per 3.3 bits, plus a sign.
        return value, EXPANDED_VALUE_WEIGHT + value.bit_length() // 3 + 2
    if isinstance(value, (datetime, date, time)):
        # A repr with its constructor name and time zone.
        return value, EXPANDED_VALUE_WEIGHT + _RENDERED_DATE_TIME_WEIGHT
    if isinstance(value, Decimal):
        # Its text holds every coefficient digit; `as_tuple()` would make a
        # tuple of them, eight bytes or more per digit.
        return value, EXPANDED_VALUE_WEIGHT + len(str(value)) + 32
    if isinstance(value, float):
        # Up to 24 characters, as `-1.7976931348623157e+308`.
        return value, EXPANDED_VALUE_WEIGHT + 24
    if isinstance(value, (dict, list, tuple, set, frozenset, _DeferredSequence)):
        return None
    return value, EXPANDED_VALUE_WEIGHT


def load_msgpack(data):
    return load_msgpack_value(data)


def decode_header_value(bytes_or_str: bytes | str) -> str:
    """
    Convert a bytes header value to text.

    Valid header values are expected to be ascii in modern times, but
    ISO-8859-1 (latin1) has historically been allowed.

    https://datatracker.ietf.org/doc/html/rfc7230#section-3.2.4
    """
    if isinstance(bytes_or_str, bytes):
        return bytes_or_str.decode("latin1")
    return bytes_or_str


def frame_path(frame: types.FrameType) -> str:
    path = frame.f_code.co_filename
    try:
        relative_path = os.path.relpath(path)
    except ValueError:  # pragma: no cover
        relative_path = path
    return f"{relative_path}:{frame.f_lineno}"


class FramePathCache:
    """Format frame paths relative to the directory where tracing started.

    Code objects are held strongly for the lifetime of a tracing session.  Besides
    making the cache safe from ``id`` reuse, this turns path normalization from a
    per-event filesystem operation into a once-per-code-object operation.
    """

    def __init__(self) -> None:
        self.root = os.getcwd()
        self._paths: dict[int, tuple[types.CodeType, str]] = {}

    def format(self, frame: types.FrameType) -> str:
        return self.format_code(frame.f_code, frame.f_lineno)

    def format_code(self, code: types.CodeType, lineno: int | None) -> str:
        code_id = id(code)
        try:
            relative_path = self._paths[code_id][1]
        except KeyError:
            path = code.co_filename
            if os.path.isabs(path):
                try:
                    relative_path = os.path.relpath(path, self.root)
                except ValueError:  # pragma: no cover
                    relative_path = path
            else:
                relative_path = os.path.normpath(path)
            self._paths[code_id] = (code, relative_path)
        return f"{relative_path}:{lineno}"


def decode_body(body: Any, request_headers: Dict[str, str]) -> Any:
    """Convert a request body into a json-serializable form."""
    if isinstance(body, bytes):
        content_type = request_headers.get("Content-Type", "")
        m = Message()
        m["content-type"] = content_type
        charset = collapse_rfc2231_value(m.get_param("charset", "utf-8"))
        try:
            return body.decode(charset)
        except (UnicodeDecodeError, LookupError):
            return "<Binary request body>"
    return body


def get_content(response: HttpResponse | StreamingHttpResponse) -> str:
    if response.streaming:
        return "<Streaming Response>"

    if TYPE_CHECKING:
        assert isinstance(response, HttpResponse)
    content_encoding = response.get("Content-Encoding")
    if content_encoding == "gzip":
        content = gzip.decompress(response.content)
    else:
        content = response.content
    try:
        return content.decode(response.charset)
    except (UnicodeDecodeError, LookupError):
        return f"<Response with invalid charset ({response.charset})>"


def get_request_body(request: "HttpRequest") -> str:
    from django.http.request import RawPostDataException

    try:
        return request.body.decode("utf-8")
    except UnicodeDecodeError:  # pragma: no cover
        return "<Binary request body>"
    except RawPostDataException:
        return "<Request data already read>"
