from __future__ import annotations

import dataclasses
import datetime as dt
import importlib
import json
import math
from collections.abc import Callable
from decimal import Decimal
from enum import Enum
from typing import Any
from uuid import UUID

import jsonpickle
from jsonpickle.errors import ClassNotFoundError

from bitfab.payload_budget import MAX_COMPRESSIBLE_SPAN_CARRIER_BYTES

_MAX_COPY_BYTES = MAX_COMPRESSIBLE_SPAN_CARRIER_BYTES
_MAX_NODES = 1_000_000

Path = tuple[str, ...]
Walk = Callable[[Any, Any, Any], None]


class _NeedsCopy(Exception):
    pass


class _GiveUp(Exception):
    pass


class _Cycle(Exception):
    def __init__(self, target: Path) -> None:
        super().__init__(f"value refers back to {list(target)}")
        self.target = target


@dataclasses.dataclass(frozen=True)
class SpanType:
    name: str
    matches: Callable[[Any], bool]
    describe: Callable[[Any, Any, Walk], dict[str, Any] | None]
    rebuild: Callable[[Any, dict[str, Any]], Any]


def _require(condition: bool) -> None:
    if not condition:
        raise _NeedsCopy


def _describe_isoformat(value: Any, readable: Any, walk: Walk) -> None:
    _require(readable == value.isoformat())


def _describe_str(value: Any, readable: Any, walk: Walk) -> None:
    _require(readable == str(value))


def _describe_items(value: Any, readable: Any, walk: Walk) -> None:
    items = list(value)
    _require(isinstance(readable, list) and len(readable) == len(items))
    for index, item in enumerate(items):
        walk(item, readable[index], index)


def _describe_fields(value: Any, names: list[str], readable: Any, walk: Walk) -> None:
    _require(isinstance(readable, dict) and list(readable) == names)
    for name in names:
        walk(getattr(value, name), readable[name], name)


def _describe_namedtuple(value: Any, readable: Any, walk: Walk) -> dict[str, Any]:
    _describe_items(value, readable, walk)
    return {"class": _class_path(type(value))}


def _describe_bytes(value: Any, readable: Any, walk: Walk) -> dict[str, Any]:
    try:
        if readable == bytes(value).decode("utf-8"):
            return {"encoding": "utf-8"}
    except UnicodeDecodeError:
        pass
    _require(readable == value.hex())
    return {"encoding": "hex"}


def _describe_enum(value: Any, readable: Any, walk: Walk) -> dict[str, Any]:
    _require(type(value.value) in (str, int, bool) and readable == value.value)
    return {"class": _class_path(type(value))}


def _describe_model(value: Any, readable: Any, walk: Walk) -> dict[str, Any]:
    fields = type(value).model_fields
    _require(isinstance(readable, dict) and set(readable) <= set(fields))
    _describe_fields(value, list(readable), readable, walk)
    return {"class": _class_path(type(value))}


def _describe_dataclass(value: Any, readable: Any, walk: Walk) -> dict[str, Any]:
    names = [field.name for field in dataclasses.fields(value)]
    _describe_fields(value, names, readable, walk)
    return {"class": _class_path(type(value))}


def _bytes_from(built: str, params: dict[str, Any]) -> bytes:
    if params["encoding"] == "hex":
        return bytes.fromhex(built)
    return built.encode("utf-8")


def _is_model(value: Any) -> bool:
    return isinstance(getattr(type(value), "model_fields", None), dict)


def _is_dataclass_instance(value: Any) -> bool:
    return dataclasses.is_dataclass(value) and not isinstance(value, type)


SPAN_TYPES: list[SpanType] = [
    SpanType(
        "py:tuple",
        lambda value: type(value) is tuple,
        _describe_items,
        lambda built, _: tuple(built),
    ),
    SpanType(
        "py:set",
        lambda value: type(value) is set,
        _describe_items,
        lambda built, _: set(built),
    ),
    SpanType(
        "py:frozenset",
        lambda value: type(value) is frozenset,
        _describe_items,
        lambda built, _: frozenset(built),
    ),
    SpanType(
        "py:namedtuple",
        lambda value: isinstance(value, tuple) and hasattr(type(value), "_fields"),
        _describe_namedtuple,
        lambda built, params: _resolve_class(params["class"])._make(built),
    ),
    SpanType(
        "py:datetime",
        lambda value: type(value) is dt.datetime,
        _describe_isoformat,
        lambda built, _: dt.datetime.fromisoformat(built),
    ),
    SpanType(
        "py:date",
        lambda value: type(value) is dt.date,
        _describe_isoformat,
        lambda built, _: dt.date.fromisoformat(built),
    ),
    SpanType(
        "py:time",
        lambda value: type(value) is dt.time,
        _describe_isoformat,
        lambda built, _: dt.time.fromisoformat(built),
    ),
    SpanType(
        "py:uuid",
        lambda value: type(value) is UUID,
        _describe_str,
        lambda built, _: UUID(built),
    ),
    SpanType(
        "py:decimal",
        lambda value: type(value) is Decimal,
        _describe_str,
        lambda built, _: Decimal(built),
    ),
    SpanType(
        "py:bytes",
        lambda value: type(value) is bytes,
        _describe_bytes,
        _bytes_from,
    ),
    SpanType(
        "py:bytearray",
        lambda value: type(value) is bytearray,
        _describe_bytes,
        lambda built, params: bytearray(_bytes_from(built, params)),
    ),
    SpanType(
        "py:enum",
        lambda value: isinstance(value, Enum),
        _describe_enum,
        lambda built, params: _resolve_class(params["class"])(built),
    ),
    SpanType(
        "py:model",
        _is_model,
        _describe_model,
        lambda built, params: _resolve_class(params["class"]).model_validate(built),
    ),
    SpanType(
        "py:dataclass",
        _is_dataclass_instance,
        _describe_dataclass,
        lambda built, params: _resolve_class(params["class"])(**built),
    ),
]


def build_input_meta(
    args: list[Any], kwargs: dict[str, Any], readable_input: Any
) -> dict[str, Any] | None:
    meta: dict[str, Any] = {}
    if kwargs:
        meta["kwarg_names"] = list(kwargs)
    root = [*args, kwargs] if kwargs else list(args)
    meta.update(_value_meta(root, readable_input))
    return meta or None


def build_output_meta(value: Any, readable_output: Any) -> dict[str, Any] | None:
    return _value_meta(value, readable_output) or None


def restore_inputs(
    raw_input: Any, input_meta: Any
) -> tuple[list[Any], dict[str, Any]] | None:
    if not isinstance(input_meta, dict) or not isinstance(raw_input, list):
        return None
    try:
        root = _restore(raw_input, input_meta)
    except Exception:
        return None
    if not isinstance(root, list):
        return None
    args = list(root)
    kwargs: dict[str, Any] = {}
    if input_meta.get("kwarg_names"):
        if not args or not isinstance(args[-1], dict):
            return None
        kwargs = args.pop()
    return args, kwargs


def restore_output(raw_output: Any, output_meta: Any) -> Any:
    if not isinstance(output_meta, dict):
        return raw_output
    try:
        return _restore(raw_output, output_meta)
    except Exception:
        return raw_output


def _value_meta(value: Any, readable: Any) -> dict[str, Any]:
    recorder = _Recorder()
    try:
        recorder.walk(value, readable, ())
        meta = recorder.meta()
        if "v" in meta and not _restores_exactly(value, readable, meta, recorder.lossy):
            raise _GiveUp
    except Exception:
        copy = _encode(value)
        return {"copy": copy} if copy is not None else {}
    return meta


def _restores_exactly(
    value: Any, readable: Any, meta: dict[str, Any], lossy: list[Path]
) -> bool:
    try:
        restored = _restore(
            json.loads(json.dumps(readable)), json.loads(json.dumps(meta))
        )
        return _exact(value, restored, (), set(lossy), {}, {})
    except Exception:
        return False


class _Recorder:
    def __init__(self) -> None:
        self.values: dict[Path, list[Any]] = {}
        self.same: list[tuple[Path, Path]] = []
        self.copies: dict[Path, Any] = {}
        self.seen: dict[int, Path] = {}
        self.dropped: list[Path] = []
        self.lossy: list[Path] = []
        self.nodes = 0

    def meta(self) -> dict[str, Any]:
        meta: dict[str, Any] = {}
        if self.values:
            meta["values"] = _values_tree(self.values)
        if self.same:
            meta["referentialEqualities"] = _equalities_record(self.same)
        if meta:
            meta["v"] = 1
        if (
            self.copies
            and len(json.dumps(list(self.copies.values()))) > _MAX_COPY_BYTES
        ):
            self.lossy.extend(self.copies)
        elif () in self.copies:
            meta["copy"] = self.copies[()]
        elif self.copies:
            meta["copies"] = {
                _stringify_path(path): copy for path, copy in self.copies.items()
            }
        return meta

    def walk(self, value: Any, readable: Any, path: Path) -> None:
        self.nodes += 1
        if self.nodes > _MAX_NODES:
            raise _GiveUp
        marks = (len(self.values), len(self.same), len(self.copies), len(self.lossy))
        if _tracks_identity(value):
            first = self.seen.get(id(value))
            if first is not None and not self._dropped(first):
                if path[: len(first)] == first:
                    raise _Cycle(first)
                self.same.append((path, first))
                return
            self.seen[id(value)] = path
        try:
            self._annotate(value, readable, path)
        except _GiveUp:
            raise
        except _Cycle as cycle:
            if cycle.target != path:
                raise
            self._copy_here(value, path, marks)
        except Exception:
            self._copy_here(value, path, marks)

    def _copy_here(self, value: Any, path: Path, marks: tuple[int, ...]) -> None:
        self._drop_after(marks)
        self.dropped.append(path)
        copy = _encode(value)
        if copy is None:
            self.lossy.append(path)
        else:
            self.copies[path] = copy

    def _drop_after(self, marks: tuple[int, ...]) -> None:
        values_size, same_size, copies_size, lossy_size = marks
        for key in list(self.values)[values_size:]:
            del self.values[key]
        del self.same[same_size:]
        for key in list(self.copies)[copies_size:]:
            del self.copies[key]
        del self.lossy[lossy_size:]

    def _dropped(self, path: Path) -> bool:
        return any(path[: len(prefix)] == prefix for prefix in self.dropped)

    def _annotate(self, value: Any, readable: Any, path: Path) -> None:
        kind = type(value)
        if value is None or kind in (bool, int, str):
            _require(type(readable) is kind and readable == value)
            return
        if kind is float:
            _require(math.isfinite(value) and readable == value)
            return
        if kind is list:
            _describe_items(value, readable, self._child_walker(path))
            return
        if kind is dict:
            _require(all(type(key) is str for key in value))
            _require(isinstance(readable, dict) and list(readable) == list(value))
            for key, item in value.items():
                self.walk(item, readable[key], (*path, key))
            return
        span_type = next((entry for entry in SPAN_TYPES if entry.matches(value)), None)
        if span_type is None:
            raise _NeedsCopy
        params = span_type.describe(value, readable, self._child_walker(path))
        self.values[path] = ["custom", span_type.name] + ([params] if params else [])

    def _child_walker(self, path: Path) -> Walk:
        def walk(child: Any, readable: Any, key: Any) -> None:
            self.walk(child, readable, (*path, str(key)))

        return walk


def _tracks_identity(value: Any) -> bool:
    if isinstance(value, (dict, list, set, bytearray)):
        return True
    return (
        hasattr(value, "__dict__")
        and not isinstance(value, (type, Enum))
        and not callable(value)
    )


def _class_path(kind: type) -> str:
    _require("<locals>" not in kind.__qualname__)
    return f"{kind.__module__}:{kind.__qualname__}"


def _resolve_class(path: str) -> Any:
    module_name, _, qualname = path.partition(":")
    resolved: Any = importlib.import_module(module_name)
    for part in qualname.split("."):
        resolved = getattr(resolved, part)
    return resolved


def _stringify_path(path: Path) -> str:
    return ".".join(
        segment.replace("\\", "\\\\").replace(".", "\\.")
        if "." in segment or "\\" in segment
        else segment
        for segment in path
    )


def _parse_path(text: str) -> Path:
    if "\\" not in text:
        return tuple(text.split("."))
    segments: list[str] = []
    segment = ""
    index = 0
    while index < len(text):
        char = text[index]
        if char == "\\":
            escaped = text[index + 1 : index + 2]
            if escaped not in ("\\", "."):
                raise ValueError(f"invalid path {text!r}")
            segment += escaped
            index += 2
            continue
        if char == ".":
            segments.append(segment)
            segment = ""
        else:
            segment += char
        index += 1
    segments.append(segment)
    return tuple(segments)


def _values_tree(annotations: dict[Path, list[Any]]) -> Any:
    root: dict[Any, Any] = {}
    for path in annotations:
        node = root
        for segment in path:
            node = node.setdefault(segment, {})
        node[None] = path

    def collect(
        node: dict[Any, Any], prefix: Path, out: dict[str, Any]
    ) -> dict[str, Any]:
        for segment, child in node.items():
            if segment is None:
                continue
            relative = (*prefix, segment)
            if None in child:
                out[_stringify_path(relative)] = tree_for(child)
            else:
                collect(child, relative, out)
        return out

    def tree_for(node: dict[Any, Any]) -> list[Any]:
        kids = collect(node, (), {})
        annotation = annotations[node[None]]
        return [annotation, kids] if kids else [annotation]

    return tree_for(root) if None in root else collect(root, (), {})


def _flatten_values(tree: Any, origin: Path, out: dict[Path, Any]) -> dict[Path, Any]:
    if isinstance(tree, dict):
        for key, child in tree.items():
            _flatten_values(child, (*origin, *_parse_path(key)), out)
    elif isinstance(tree, list) and tree:
        if len(tree) > 1 and isinstance(tree[1], dict):
            _flatten_values(tree[1], origin, out)
        out[origin] = tree[0]
    return out


def _equalities_record(same: list[tuple[Path, Path]]) -> dict[str, list[str]]:
    record: dict[str, list[str]] = {}
    for path, first in same:
        record.setdefault(_stringify_path(first), []).append(_stringify_path(path))
    return record


def _parse_equalities(annotations: Any) -> dict[Path, Path]:
    if isinstance(annotations, list):
        annotations = annotations[1] if len(annotations) > 1 else {}
    if not isinstance(annotations, dict):
        return {}
    return {
        _parse_path(path): _parse_path(first)
        for first, paths in annotations.items()
        if isinstance(paths, list)
        for path in paths
        if isinstance(path, str)
    }


@dataclasses.dataclass
class _PathTrie:
    children: dict[str, _PathTrie] = dataclasses.field(default_factory=dict)
    annotation: Any = None
    copy: list[Any] | None = None
    same: Path | None = None
    store: Path | None = None


def _restore_trie(meta: dict[str, Any]) -> _PathTrie:
    root = _PathTrie()

    def insert(path: Path) -> _PathTrie:
        node = root
        for segment in path:
            node = node.children.setdefault(segment, _PathTrie())
        return node

    for path, annotation in _flatten_values(meta.get("values"), (), {}).items():
        insert(path).annotation = annotation
    for path, target in _parse_equalities(meta.get("referentialEqualities")).items():
        insert(path).same = target
        insert(target).store = target
    raw_copies = meta.get("copies")
    if isinstance(raw_copies, dict):
        for path, copy in raw_copies.items():
            insert(_parse_path(path)).copy = [copy]
    return root


def _restore(readable: Any, meta: dict[str, Any]) -> Any:
    if "copy" in meta:
        return _decode_or_keep(meta["copy"], readable)
    trie = _restore_trie(meta)
    if not trie.children and trie.annotation is None:
        return readable
    built: dict[Path, Any] = {}

    def build(node: Any, trie_node: _PathTrie | None) -> Any:
        if trie_node is None:
            return node
        if trie_node.copy is not None:
            result = _decode_or_keep(trie_node.copy[0], node)
        elif trie_node.same is not None:
            result = built.get(trie_node.same, node)
        else:
            children = trie_node.children
            if not children:
                rebuilt: Any = node
            elif isinstance(node, list):
                rebuilt = [
                    build(item, children.get(str(index)))
                    for index, item in enumerate(node)
                ]
            elif isinstance(node, dict):
                rebuilt = {
                    key: build(item, children.get(key)) for key, item in node.items()
                }
            else:
                rebuilt = node
            result = (
                rebuilt
                if trie_node.annotation is None
                else _apply_or_keep(trie_node.annotation, rebuilt)
            )
        if trie_node.store is not None:
            built[trie_node.store] = result
        return result

    return build(readable, trie)


_SPAN_TYPES_BY_NAME = {span_type.name: span_type for span_type in SPAN_TYPES}


def _apply_or_keep(annotation: Any, built: Any) -> Any:
    try:
        _, name, *rest = annotation
        params = rest[0] if rest else {}
        return _SPAN_TYPES_BY_NAME[name].rebuild(built, params)
    except (Exception, ClassNotFoundError):
        return built


def _encode(value: Any) -> Any:
    try:
        encoded = jsonpickle.encode(value, unpicklable=True, keys=True)
    except Exception:
        return None
    if encoded is None or len(encoded) > _MAX_COPY_BYTES:
        return None
    return json.loads(encoded)


def _decode_or_keep(copy: Any, readable: Any) -> Any:
    try:
        return jsonpickle.decode(json.dumps(copy), keys=True, on_missing="error")
    except (Exception, ClassNotFoundError):
        return readable


def _exact(
    a: Any,
    b: Any,
    path: Path,
    lossy: set[Path],
    forward: dict[int, int],
    backward: dict[int, int],
) -> bool:
    if lossy and path in lossy:
        return True
    if type(a) is not type(b):
        return False
    if _tracks_identity(a):
        if forward.get(id(a), id(b)) != id(b) or backward.get(id(b), id(a)) != id(a):
            return False
        if id(a) in forward:
            return True
        forward[id(a)] = id(b)
        backward[id(b)] = id(a)
    if isinstance(a, float):
        return a == b or (math.isnan(a) and math.isnan(b))
    if isinstance(a, dict):
        return list(a) == list(b) and all(
            _exact(a[key], b[key], _child(path, key, lossy), lossy, forward, backward)
            for key in a
        )
    if isinstance(a, (list, tuple)):
        return len(a) == len(b) and all(
            _exact(x, y, _child(path, index, lossy), lossy, forward, backward)
            for index, (x, y) in enumerate(zip(a, b))
        )
    try:
        if isinstance(a, (set, frozenset)):
            return bool(a == b)
        if hasattr(a, "__dict__") and not isinstance(a, (type, Enum)):
            if not _exact(vars(a), vars(b), path, lossy, forward, backward):
                return False
            return type(a).__eq__ is object.__eq__ or bool(a == b)
        return bool(a == b) and repr(a) == repr(b)
    except Exception:
        return False


def _child(path: Path, segment: Any, lossy: set[Path]) -> Path:
    return (*path, str(segment)) if lossy else path
