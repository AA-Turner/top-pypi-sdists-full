"""Run config and array values as plain JSON (SDK reliability plan (c)).

Config is stored as JSONB; non-JSON values used to become one ``repr()`` string
(a Namespace, a dataclass, a ``DictConfig``, ``"np.float32(0.1)"``).
:func:`to_config` turns them into the dict a person meant, before any request.

OmegaConf is read via :mod:`probe.sdk.values.omegaconf_read`: interpolations
that would reveal a secret keep their ``${...}`` text, the rest resolve (#2032:
security over W&B parity, where ``wandb.config`` resolves everything).

Stdlib only: numpy, torch, omegaconf and pydantic values are recognised by
shape and class module name, never imported, so ``import probe`` loads none.
"""

from __future__ import annotations

import dataclasses
import datetime as _dt
import enum
import math
import os
import sys
import types
from collections.abc import Mapping
from typing import Any

from .. import errors
from . import omegaconf_read
from ...foundation.safe_warn import safe_warn

#: Arrays up to this many elements become lists; bigger ones a one-line summary.
MAX_ARRAY_ELEMENTS = 1_024

#: Deeper nesting stays ``repr()``: a guard no real config reaches.
_MAX_DEPTH = 64

#: Returned by :func:`array_scalar` for "not a numpy / torch value".
NOT_AN_ARRAY: Any = object()


def _module(value: Any) -> str:
    return getattr(type(value), "__module__", "") or ""


#: Packages whose values are arrays read by shape. jax arrays live in ``jaxlib``;
#: ``ml_dtypes`` holds jax's bfloat16/float8 scalars. Without them a size-1 jax
#: vector reached the step record as its repr (``float()`` refuses ndim > 0).
_ARRAY_PACKAGES = ("numpy", "torch", "jax", "jaxlib", "ml_dtypes")
_ARRAY_PREFIXES = tuple(f"{name}." for name in _ARRAY_PACKAGES)


def _is_array_like(value: Any) -> bool:
    """A numpy / jax value or a torch tensor, by module name alone."""
    module = _module(value)
    # Exact package names: `torchvision` / `torchmetrics` objects are not tensors.
    ours = module in _ARRAY_PACKAGES or module.startswith(_ARRAY_PREFIXES)
    return ours and hasattr(value, "item")


def _size(value: Any) -> int | None:
    size = getattr(value, "size", None)
    if callable(size):  # torch: .size() is the SHAPE; numel() is the count
        numel = getattr(value, "numel", None)
        return int(numel()) if callable(numel) else None
    return int(size) if isinstance(size, int) else None


def array_scalar(value: Any) -> Any:
    """A numpy value or torch tensor as a Python number for ``Run.log``.

    One element -> its float via ``.item()`` (no numpy >= 1.25 ``float(array)``
    warning). Several elements -> None: the caller keeps it as a step attribute
    instead of a RuntimeError in the loop. Not an array -> :data:`NOT_AN_ARRAY`."""
    if not _is_array_like(value):
        return NOT_AN_ARRAY
    try:
        if _size(value) != 1:
            return None
        item = value.item()
    except Exception:  # noqa: BLE001 -- a broken tensor is not a metric
        return None
    if isinstance(item, bool):
        return float(item)
    if isinstance(item, (int, float)):
        return float(item)
    return None  # complex, str, datetime64...


def scalar(value: Any) -> Any:
    """A 0-d numpy value or tensor as its Python scalar, else :data:`NOT_AN_ARRAY`.
    Used by ``unstorable.normalize_json`` so request bodies carry numbers, not reprs."""
    if not _is_array_like(value) or getattr(value, "ndim", None) != 0:
        return NOT_AN_ARRAY
    try:
        return value.item()
    except Exception:  # noqa: BLE001
        return NOT_AN_ARRAY


def _is_namespace(value: Any) -> bool:
    """An ``argparse.Namespace`` (incl. jsonargparse's) or ``types.SimpleNamespace``.
    argparse is not imported: unloaded means no Namespace exists."""
    if isinstance(value, types.SimpleNamespace):
        return True
    argparse = sys.modules.get("argparse")
    return argparse is not None and isinstance(value, argparse.Namespace)


def _as_mapping(value: Any) -> Mapping | None:
    """``value`` as a mapping if it is a config shape, else None (OmegaConf is walked by :func:`to_plain`)."""
    if isinstance(value, Mapping):
        return value
    if _is_namespace(value):
        return vars(value)
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        # `repr=False` marks a secret or big tensor: left out here too.
        return {
            field.name: getattr(value, field.name)
            for field in dataclasses.fields(value)
            if field.repr
        }
    if getattr(type(value), "__pydantic_root_model__", False):  # RootModel[dict]: its dict
        root = getattr(value, "root", None)
        return root if isinstance(root, Mapping) else None
    fields = getattr(type(value), "model_fields", None)  # pydantic v2
    if fields is None:
        fields = getattr(type(value), "__fields__", None)  # pydantic v1
    shown = getattr(value, "__repr_args__", None)
    if isinstance(fields, dict) and callable(shown):
        # Fields the repr() shows; `Field(repr=False)` ones are left out like a dataclass's.
        try:
            return {name: child for name, child in shown() if isinstance(name, str)}
        except Exception:  # noqa: BLE001
            return None
    return None


def _float(value: float) -> Any:
    if math.isfinite(value):
        return value
    if math.isnan(value):
        return "NaN"
    return "Infinity" if value > 0 else "-Infinity"


def to_plain(value: Any, *, _depth: int = 0, _seen: frozenset[int] = frozenset(), _reader: Any = None) -> Any:
    """A JSON-safe copy of ``value``. Non-finite floats become ``"NaN"`` /
    ``"Infinity"`` / ``"-Infinity"``; anything unrecognised becomes its ``repr()``. Never raises."""
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        return _float(value)
    if _depth >= _MAX_DEPTH or id(value) in _seen:
        return _safe_repr(value)
    seen = _seen | {id(value)}
    reader = _reader
    if omegaconf_read.is_omegaconf(value):
        reader = omegaconf_read.Reader() if reader is None else reader
        try:
            items = reader.items(value)
        except Exception:  # noqa: BLE001 -- a node that cannot even be listed
            return _safe_repr(value)
        children = [(key, to_plain(child, _depth=_depth + 1, _seen=seen, _reader=reader)) for key, child in items]
        if hasattr(value, "keys"):
            return _keyed(children)
        return [child for _, child in children]
    if isinstance(value, enum.Enum):
        return to_plain(value.value, _depth=_depth + 1, _seen=seen, _reader=reader)
    if isinstance(value, (_dt.datetime, _dt.date, _dt.time)):
        return value.isoformat()
    if isinstance(value, os.PathLike):
        path = os.fspath(value)
        return path if isinstance(path, str) else _safe_repr(value)
    if _is_array_like(value):
        return _array(value, _depth=_depth, _seen=seen)
    mapping = _as_mapping(value)
    if mapping is not None:
        return _keyed(
            [(key, to_plain(child, _depth=_depth + 1, _seen=seen, _reader=reader)) for key, child in _items(mapping)]
        )
    if isinstance(value, (list, tuple)):
        return [to_plain(child, _depth=_depth + 1, _seen=seen, _reader=reader) for child in value]
    if isinstance(value, (set, frozenset)):
        items = [to_plain(child, _depth=_depth + 1, _seen=seen, _reader=reader) for child in value]
        try:
            return sorted(items)
        except TypeError:
            return items
    return _safe_repr(value)


def _keyed(children: list) -> dict[str, Any]:
    """``{str(key): value}``; warns when two keys collapse to one string (later wins)."""
    out: dict[str, Any] = {}
    for key, value in children:
        name = str(key)
        if name in out:
            safe_warn.warn(
                f"probe: config keys {key!r} and another both become {name!r} in JSON; "
                "kept the later one.",
                stacklevel=4,
            )
        out[name] = value
    return out


def _items(mapping: Mapping) -> list:
    try:
        return list(mapping.items())
    except Exception:  # noqa: BLE001
        return []


def _array(value: Any, *, _depth: int, _seen: frozenset[int]) -> Any:
    try:
        size = _size(value)
        if size is not None and size <= MAX_ARRAY_ELEMENTS:
            detach = getattr(value, "detach", None)
            if callable(detach):  # torch
                value = detach().cpu()
            return to_plain(value.tolist(), _depth=_depth + 1, _seen=_seen)
        shape = tuple(getattr(value, "shape", ()) or ())
        return f"<{type(value).__name__} shape={shape} dtype={getattr(value, 'dtype', '?')}>"
    except Exception:  # noqa: BLE001
        return _safe_repr(value)


def _safe_repr(value: Any) -> str:
    try:
        return repr(value)
    except Exception:  # noqa: BLE001
        return f"<unrepresentable {type(value).__name__}>"


def to_config(value: Any) -> dict[str, Any]:
    """A run config as a plain JSON object.

    Top level must be a ``Mapping`` (a Hydra ``DictConfig`` included), an
    ``argparse.Namespace``, a dataclass instance or a pydantic model; anything
    else raises ``ValidationError`` before any request."""
    if omegaconf_read.is_omegaconf(value) and hasattr(value, "keys"):
        plain = to_plain(value)
        return plain if isinstance(plain, dict) else {}
    mapping = _as_mapping(value)
    if mapping is None:
        raise errors.ValidationError(
            f"config must be a mapping (a dict, a DictConfig, an argparse.Namespace, "
            f"a dataclass or a pydantic model), got {type(value).__name__}"
        )
    plain = to_plain(mapping)
    return plain if isinstance(plain, dict) else {}
