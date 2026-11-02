"""
The parameters each side of an eval declares, all written the way @seq.infer's always were — keyword arguments with
defaults, typed int / float / bool / str, or list[float] (a list of numbers: a crop's corners):

    policy     @seq.infer   def infer(self, obs, *, replan_steps: int = 5)
    adapter    __init__     def __init__(self, *, image_size: int = 224)
    benchmark  __init__     def __init__(self, worlds, *, noise_std: float = 0.02)   (beside what init= hands it)
    eval       the eval loop's own: max_seconds (how long an episode may run on the robot's clock; the benchmark's
               max_seconds by default)

Registering a side sends its declarations (type and default); an eval sets any of them by `side.name`
(`--param adapter.image_size=128`), or by the bare name when only one side declares it, and sweeps any of them. The
platform checks each name and type before the eval starts and records, per arm, the value each ran with and where it
came from.
"""
from __future__ import annotations

import inspect
import types
import typing
from typing import Any

from sequence_base.contract import InferParam

SIDES = ("policy", "adapter", "benchmark", "eval")
TYPES = {"int": int, "float": float, "bool": bool, "str": str}

_UNIONS = (typing.Union, getattr(types, "UnionType", typing.Union))


class Range:
    """`Annotated[int, seq.Range(1, 10)]`: a parameter's bounds, inclusive (None: open on that side). The platform refuses
    a value outside them before it is used, saying the bounds."""

    def __init__(self, min: float | None = None, max: float | None = None) -> None:
        self.min, self.max = min, max


class OneOf:
    """`Annotated[str, seq.OneOf("fast", "careful")]`: the only values a parameter may take."""

    def __init__(self, *values: Any) -> None:
        self.values = list(values)


def keyword_params(fn: Any, where: str, error: type[Exception], *, kind: str = "parameter",
                   skip: frozenset[str] = frozenset(), skip_first: bool = False,
                   loose: bool = False) -> dict[str, InferParam]:
    """`fn`'s parameters after `self` that an eval may set, each with its type (the annotation, else its default's) and
    default: every one but the first positional when `skip_first` (the observation),
    the names in `skip` (what the platform itself passes), and *args / **kwargs. One without a default, passed only by
    position, or of another type is refused with `error`, naming `where` - but for `loose`, a class's own method left as
    it is written: there one with a default that is none of them (`generator=None`, a dict) keeps its default, set by
    nothing."""
    params = list(inspect.signature(fn).parameters.values())[1:]
    try:

        hints = typing.get_type_hints(fn, include_extras=True)
    except Exception:
        hints = {}
    positional = (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    first = next((p for p in params if p.kind in positional), None) if skip_first else None
    out: dict[str, InferParam] = {}
    for p in params:
        if p is first or p.name in skip or p.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue
        at = f"{where}: parameter {p.name!r}"
        if p.default is not inspect.Parameter.empty and loose and p.kind is inspect.Parameter.POSITIONAL_ONLY:
            continue
        if p.kind is inspect.Parameter.POSITIONAL_ONLY:
            raise error(f"{at} is positional-only; {_a(kind)} is passed by name")
        if p.default is inspect.Parameter.empty:
            raise error(f"{at} has no default; {_a(kind)} needs one (it may be left unset)")
        hint, marks = hints.get(p.name), ()
        if typing.get_origin(hint) is typing.Annotated:
            hint, marks = typing.get_args(hint)[0], tuple(hint.__metadata__)
        t = param_type(p.replace(annotation=hint) if hint is not None else p)
        if t is None:
            if loose:
                continue
            raise error(f"{at}: annotate it as int, float, bool, str or list[float] ({_a(kind)} is one of those)")
        default = p.default
        if default is not None:
            if t == "list":
                if not _numbers(default):
                    if loose:
                        continue
                    raise error(f"{at}: its default {default!r} is not a list of numbers")
                default = [float(v) for v in default]
            elif t == "float" and isinstance(default, int) and not isinstance(default, bool):
                default = float(default)
            elif type(default) is not TYPES[t]:
                if loose:
                    continue
                raise error(f"{at}: its default {default!r} is not a {t}")
        bounds: dict[str, Any] = {}
        for mark in marks:
            if isinstance(mark, Range):
                bounds.update({k: v for k, v in (("min", mark.min), ("max", mark.max)) if v is not None})
            elif isinstance(mark, OneOf):
                bounds["choices"] = mark.values
        try:
            out[p.name] = InferParam(type=t, default=default, **bounds)
        except ValueError as exc:
            raise error(f"{at}: {_first_error(exc)}") from None
    return out


def _first_error(exc: Exception) -> str:
    """A pydantic refusal in one line: its first error's message."""
    errors = getattr(exc, "errors", None)
    try:
        return str(errors()[0]["msg"]).removeprefix("Value error, ") if errors else str(exc)
    except Exception:
        return str(exc)


def _a(kind: str) -> str:
    return f"an {kind}" if kind[:1] in "aeiou" else f"a {kind}"


def param_type(p: inspect.Parameter) -> str | None:
    """int / float / bool / str from the annotation (`int`, `"int"`, `int | None`, `Optional[int]`), "list" from
    `list[float]` alone, else from the default's own type; None when it is none of those."""
    ann = p.annotation
    if ann is not inspect.Parameter.empty:
        if _list_of_floats(ann):
            return "list"
        text = ann if isinstance(ann, str) else getattr(ann, "__name__", None) or str(ann)
        text = text.strip().strip("'\"")
        if text.replace(" ", "") in ("list[float]", "list[float]|None", "Optional[list[float]]"):
            return "list"
        parts = {t.strip().strip("'\"") for t in text.replace("Optional[", "").replace("typing.", "").rstrip("]")
                 .split("|")}
        parts.discard("None")
        return parts.pop() if len(parts) == 1 and next(iter(parts)) in TYPES else None
    for kind, t in (("bool", bool), ("int", int), ("float", float), ("str", str)):
        if type(p.default) is t:
            return kind
    return None


def _list_of_floats(ann: Any) -> bool:
    """Whether an annotation is list[float], or list[float] | None."""
    if typing.get_origin(ann) in _UNIONS:
        args = [a for a in typing.get_args(ann) if a is not type(None)]
        ann = args[0] if len(args) == 1 else None
    return typing.get_origin(ann) is list and typing.get_args(ann) == (float,)


def _numbers(value: Any) -> bool:
    """Whether a value is a list or tuple of numbers (true / false none of them)."""
    return isinstance(value, (list, tuple)) and all(not isinstance(v, bool) and isinstance(v, (int, float))
                                                    for v in value)


def adapter_params(cls: type) -> dict[str, InferParam]:
    """The parameters an adapter's __init__ declares — `def __init__(self, *, image_size: int = 224)` — which an eval may
    set (`--param adapter.image_size=128`); the benchmark machine creates the adapter with them. {} for an adapter
    without an __init__ of its own."""
    from seq.errors import AdapterDefinitionError

    init = getattr(cls, "__init__", object.__init__)
    if init is object.__init__ or not inspect.isfunction(init):
        return {}
    return keyword_params(init, f"{cls.__name__}.__init__", AdapterDefinitionError, kind="adapter parameter")


def split(key: str) -> tuple[str | None, str]:
    """`adapter.image_size` → ("adapter", "image_size"); a bare `replan_steps` → (None, "replan_steps"). ValueError for a
    side that is not one of policy / adapter / benchmark / eval, or a name that is not a Python name."""
    side, dot, name = key.strip().rpartition(".")
    if not name.isidentifier() or (dot and side not in SIDES):
        raise ValueError(f"{key!r} is not NAME or SIDE.NAME, SIDE one of {', '.join(SIDES)} (e.g. replan_steps, "
                         "adapter.image_size, eval.max_seconds)")
    return (side or None), name
