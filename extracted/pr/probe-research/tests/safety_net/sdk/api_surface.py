"""Public SDK objects as data: kind, signature and members, with no module path in them.

Annotations render by bare name and addresses are dropped, so a pure move changes nothing.
"""

from __future__ import annotations

import enum
import functools
import inspect
import re
import types
from typing import Any

_DOTTED = re.compile(r"\b(?:[A-Za-z_]\w*\.)+(?=[A-Za-z_]\w*)")
_ADDRESS = re.compile(r" at 0x[0-9a-fA-F]+")
_CLASS_REPR = re.compile(r"<class '([\w.]+)'>")
#: Dunders a caller relies on (`with probe.init(...)`, `for x in ...`); others are internals.
PROTOCOL_DUNDERS = frozenset(
    {
        "__call__", "__enter__", "__exit__", "__aenter__", "__aexit__", "__iter__", "__next__",
        "__len__", "__getitem__", "__setitem__", "__contains__", "__bool__", "__getattr__",
    }
)
#: Values that differ per build: their type is pinned, never the value.
_VARYING = frozenset({"__version__"})
_LITERALS = (str, int, float, bool, type(None))


def _bare(text: str) -> str:
    text = _ADDRESS.sub("", text)
    text = _CLASS_REPR.sub(lambda m: m.group(1).rsplit(".", 1)[-1], text)
    return _DOTTED.sub("", text)


def annotation_text(annotation: Any) -> str:
    if annotation is inspect.Parameter.empty:
        return ""
    if isinstance(annotation, str):
        return _bare(annotation)
    if isinstance(annotation, type):
        return annotation.__qualname__
    return _bare(repr(annotation))


def default_text(value: Any) -> str:
    if isinstance(value, (set, frozenset)):  # hash order varies per process
        inner = ", ".join(sorted(default_text(v) for v in value))
        return f"{type(value).__name__}({{{inner}}})"
    if isinstance(value, enum.Enum):
        return f"{type(value).__qualname__}.{value.name}"
    if isinstance(value, (types.FunctionType, type)):
        return value.__qualname__
    return _bare(repr(value))


def _param(param: inspect.Parameter) -> str:
    prefix = {param.VAR_POSITIONAL: "*", param.VAR_KEYWORD: "**"}.get(param.kind, "")
    text = prefix + param.name
    annotation = annotation_text(param.annotation)
    if annotation:
        text += f": {annotation}"
    if param.default is not param.empty:
        text += (" = " if annotation else "=") + default_text(param.default)
    return text


def signature_text(obj: Any) -> str | None:
    """`(a: int, *, b: str = 'x') -> None` with bare annotation names, or None."""
    try:
        sig = inspect.signature(obj)
    except (TypeError, ValueError):
        return None
    parts: list[str] = []
    params = list(sig.parameters.values())
    for i, param in enumerate(params):
        if param.kind == param.KEYWORD_ONLY and not any(
            p.kind in (p.VAR_POSITIONAL, p.KEYWORD_ONLY) for p in params[:i]
        ):
            parts.append("*")
        parts.append(_param(param))
        if param.kind == param.POSITIONAL_ONLY and (
            i + 1 == len(params) or params[i + 1].kind != param.POSITIONAL_ONLY
        ):
            parts.append("/")
    returns = annotation_text(sig.return_annotation)
    return f"({', '.join(parts)})" + (f" -> {returns}" if returns else "")


def _ours(cls: type) -> bool:
    return (getattr(cls, "__module__", "") or "").split(".")[0] == "probe"


def _member(raw: Any) -> str:
    if isinstance(raw, staticmethod):
        return f"staticmethod {signature_text(raw.__func__)}"
    if isinstance(raw, classmethod):
        return f"classmethod {signature_text(raw.__func__)}"
    if isinstance(raw, property):
        returns = annotation_text(inspect.signature(raw.fget).return_annotation) if raw.fget else ""
        settable = " settable" if raw.fset is not None else ""
        return f"property{settable}" + (f" -> {returns}" if returns else "")
    if isinstance(raw, functools.cached_property):
        return "cached_property"
    if isinstance(raw, type):
        return "class"
    if inspect.isfunction(raw) or inspect.ismethoddescriptor(raw) or callable(raw):
        return f"method {signature_text(raw)}"
    return f"attribute: {type(raw).__name__}"


def class_members(cls: type) -> dict[str, str]:
    """Public members defined by Probe's own classes in the MRO (first definition wins)."""
    members: dict[str, str] = {}
    for owner in cls.__mro__:
        if not _ours(owner):
            continue
        for name, raw in vars(owner).items():
            if name in members or (name.startswith("_") and name not in PROTOCOL_DUNDERS):
                continue
            if issubclass(cls, enum.Enum) and isinstance(raw, cls):
                continue  # enum members are listed with their values
            members[name] = _member(raw)
    return dict(sorted(members.items()))


def _constructor(cls: type) -> str | None:
    for owner in cls.__mro__:
        if any(n in vars(owner) for n in ("__init__", "__new__", "__signature__")):
            return signature_text(cls) if _ours(owner) else None
    return None


def describe(obj: Any, name: str = "") -> dict:
    """What a caller of `obj` depends on, as plain data."""
    if isinstance(obj, type):
        entry: dict[str, Any] = {
            "kind": "class",
            "bases": [b.__qualname__ for b in obj.__bases__],
            "members": class_members(obj),
        }
        if issubclass(obj, enum.Enum):
            entry["enum"] = {m.name: m.value if isinstance(m.value, _LITERALS) else repr(m.value) for m in obj}
        else:
            signature = _constructor(obj)
            if signature is not None:
                entry["signature"] = signature
        return entry
    if isinstance(obj, types.ModuleType):
        return {"kind": "module", "names": module_names(obj)}
    if inspect.isroutine(obj):
        return {"kind": "function", "signature": signature_text(obj)}
    entry = {"kind": "constant", "type": type(obj).__name__}
    if isinstance(obj, _LITERALS) and name not in _VARYING:
        entry["value"] = obj
    return entry


def module_names(module: types.ModuleType) -> dict[str, str]:
    """A public module's own classes and functions, by name and kind."""
    names = getattr(module, "__all__", None) or [n for n in vars(module) if not n.startswith("_")]
    found: dict[str, str] = {}
    for name in names:
        value = getattr(module, name, None)
        if not (isinstance(value, type) or inspect.isroutine(value)) or not _ours(value):
            continue  # imported helpers (typing, stdlib) are not this module's surface
        if isinstance(value, type):
            found[name] = "class " + ", ".join(b.__qualname__ for b in value.__bases__)
        elif inspect.isroutine(value):
            found[name] = f"function {signature_text(value)}"
    return dict(sorted(found.items()))
