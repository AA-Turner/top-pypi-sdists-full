"""Plain-dataclass replacement for the former pydantic-based ``Serializable`` base.

**Why this exists.** The runtime must eventually run on the sandboxed Sucuri
interpreter, which cannot load the native ``pydantic-core`` C-extension. abstra
only ever used a shallow slice of pydantic here — camelCase alias round-tripping,
one discriminated union, a single before-validator and datetime (de)serialization
— so we drop the dependency and back the same public API with stdlib dataclasses
plus a small, purpose-built serializer.

**Wire compatibility is a hard contract.** ``dump()``/``dump_json()`` output is
written to the DB and the queue and read back by cloud-api and other running
deployments, so the exact bytes must not change. This is frozen by
``entities/serializable_golden_test.py`` (both dict values and JSON field order).

**How subclasses work.** Every ``class X(Serializable)`` is auto-converted to
``@dataclass(kw_only=True)`` via ``__init_subclass__`` — ``kw_only`` because
required fields frequently follow defaulted ones and reordering fields would
change the wire order. Construction is keyword-based everywhere, so this is
transparent. The public API is kept identical to the old pydantic base so call
sites are unchanged: ``dump``, ``dump_json``, ``model_dump``, ``model_validate``,
``model_validate_json``, ``model_copy``.
"""

from __future__ import annotations

import dataclasses
import datetime
import json
import typing
from typing import Any, Dict, Type, TypeVar, cast, get_args, get_origin, get_type_hints

# typing_extensions (a transitive dep, always installed) re-exports
# dataclass_transform on every supported version; importing from `typing` would be
# invalid under the pyright target (3.10, where it doesn't exist yet).
from typing_extensions import dataclass_transform

from abstra_internals.utils.datetime import from_utc_iso_string, to_utc_iso_string

T = TypeVar("T", bound="Serializable")


def to_camel(snake: str) -> str:
    """snake_case -> lowerCamelCase (matches pydantic ``alias_generators.to_camel``
    for the simple identifiers used across the hierarchy)."""
    head, *tail = snake.split("_")
    return head + "".join(word.capitalize() for word in tail)


# --- before-validators (subset of pydantic's @field_validator(mode="before")) ---

_VALIDATES = "__abstra_validates__"


def field_validator(*fields: str, mode: str = "before"):
    """Register a before-validator for ``fields``. Mirrors the pydantic decorator
    shape (``@field_validator("x", mode="before")`` over a ``@classmethod``) so
    subclass code stays recognizable. The function runs during construction and
    its return value replaces the field."""
    if mode != "before":
        raise ValueError("Serializable only supports mode='before' validators")

    def decorator(fn):
        target = fn.__func__ if isinstance(fn, classmethod) else fn
        setattr(target, _VALIDATES, fields)
        return fn

    return decorator


# --- discriminated unions (subset of pydantic's Discriminator/Tag) ---

_UNION_DISCRIMINATORS: Dict[Any, Any] = {}


def register_discriminated_union(union, discriminator, mapping: Dict[str, type]):
    """Associate a ``Union[...]`` type with a callable that, given a raw value,
    returns the tag selecting one member of ``mapping`` (tag -> class). Used by
    ``from_dict`` to rebuild the correct concrete type."""
    _UNION_DISCRIMINATORS[union] = (discriminator, mapping)
    return union


@dataclass_transform(kw_only_default=True, field_specifiers=(dataclasses.field,))
class Serializable:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # init=False: we supply a custom __init__ (below) that is alias-tolerant and
        # coerces nested values — matching pydantic's populate_by_name + validation so
        # that constructing from a dumped (camelCase) dict via ``Model(**data)`` keeps
        # working (e.g. `ListTasksItem(**task.dump())`, `Execution(context=<jsonb dict>)`).
        # kw_only so required fields may follow defaulted (inherited) ones without a
        # definition-order constraint, and so the wire field order stays free.
        dataclasses.dataclass(kw_only=True, init=False)(cls)

    # ------------------------------------------------------------------ construct
    def __init__(self, **kwargs):
        cls = type(self)
        hints = _hints(cls)
        validators = _before_validators(cls)
        for f in dataclasses.fields(cast(Any, cls)):
            alias = to_camel(f.name)
            if alias in kwargs:  # populate_by_name: camelCase alias
                raw, provided = kwargs[alias], True
            elif f.name in kwargs:  # or the snake_case field name
                raw, provided = kwargs[f.name], True
            else:
                raw, provided = None, False
            if provided:
                # before-validator runs on the RAW input (pydantic mode="before"),
                # then the value is coerced to the field type.
                validator = validators.get(f.name)
                if validator is not None:
                    raw = validator(cls, raw)
                value = _coerce(hints.get(f.name, Any), raw)
            elif f.default is not dataclasses.MISSING:
                value = f.default  # defaults are not validated (pydantic parity)
            elif f.default_factory is not dataclasses.MISSING:
                value = f.default_factory()
            else:
                raise TypeError(
                    f"{cls.__name__} missing required keyword argument: {f.name!r}"
                )
            setattr(self, f.name, value)

    # ------------------------------------------------------------------ serialize
    def dump(self) -> dict:
        """Wire form: camelCase keys, JSON-safe values (datetime -> ISO string)."""
        return _serialize(self, by_alias=True, json_mode=True)

    def dump_json(self, indent: int = 4) -> str:
        return json.dumps(self.dump(), indent=indent, ensure_ascii=False)

    def model_dump(self) -> dict:
        """Python-mode dump with snake_case field names (datetime kept as objects),
        matching pydantic ``model_dump(by_alias=False)``."""
        return _serialize(self, by_alias=False, json_mode=False)

    def model_copy(self: T, update: Dict[str, Any] | None = None) -> T:
        data = {
            f.name: getattr(self, f.name) for f in dataclasses.fields(cast(Any, self))
        }
        data.update(update or {})
        return cast(T, type(self)(**data))

    # ------------------------------------------------------------------ deserialize
    @classmethod
    def model_validate(cls: Type[T], data: Any) -> T:
        return _build(cls, data)

    @classmethod
    def model_validate_json(cls: Type[T], data: str) -> T:
        return _build(cls, json.loads(data))

    # kept for symmetry with pydantic-style call sites
    from_dict = model_validate


# ---------------------------------------------------------------------- internals


_VALIDATORS_CACHE: Dict[type, Dict[str, Any]] = {}


def _before_validators(cls) -> Dict[str, Any]:
    cached = _VALIDATORS_CACHE.get(cls)
    if cached is not None:
        return cached
    validators: Dict[str, Any] = {}
    for klass in reversed(cls.__mro__):
        for attr in vars(klass).values():
            target = attr.__func__ if isinstance(attr, classmethod) else attr
            fields = getattr(target, _VALIDATES, None)
            if fields:
                for field_name in fields:
                    validators[field_name] = target
    _VALIDATORS_CACHE[cls] = validators
    return validators


def _serialize(value, *, by_alias: bool, json_mode: bool) -> Any:
    if isinstance(value, Serializable):
        out = {}
        for f in dataclasses.fields(cast(Any, value)):
            if f.metadata.get("exclude"):
                continue
            key = to_camel(f.name) if by_alias else f.name
            out[key] = _serialize(
                getattr(value, f.name), by_alias=by_alias, json_mode=json_mode
            )
        return out
    if isinstance(value, datetime.datetime):
        return to_utc_iso_string(value) if json_mode else value
    if isinstance(value, (list, tuple)):
        return [_serialize(v, by_alias=by_alias, json_mode=json_mode) for v in value]
    if isinstance(value, dict):
        return {
            k: _serialize(v, by_alias=by_alias, json_mode=json_mode)
            for k, v in value.items()
        }
    return value


_HINTS_CACHE: Dict[type, Dict[str, Any]] = {}


def _hints(cls) -> Dict[str, Any]:
    cached = _HINTS_CACHE.get(cls)
    if cached is None:
        cached = get_type_hints(cls)
        _HINTS_CACHE[cls] = cached
    return cached


def _build(cls: Type[T], data: Any) -> T:
    if isinstance(data, cls):
        return data
    if not isinstance(data, dict):
        raise TypeError(
            f"{cls.__name__}.model_validate expects a dict, got {type(data)}"
        )
    # The constructor is alias-tolerant and coerces nested values, so this is just it.
    return cls(**data)


def _parse_datetime(value):
    """Tolerant ISO-8601 parse (pydantic accepted many forms; the strict
    ``from_utc_iso_string`` only accepts ``.%fZ``). Serialization is unchanged
    (always ``to_utc_iso_string``), so this only widens what we can READ — e.g.
    ``+00:00`` offsets or missing microseconds from peers / hand-migrated rows."""
    if isinstance(value, datetime.datetime):
        return value
    if not isinstance(value, str):
        raise TypeError(f"expected datetime or ISO string, got {type(value).__name__}")
    try:
        normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
        return datetime.datetime.fromisoformat(normalized)
    except ValueError:
        return from_utc_iso_string(value)  # last resort (raises if truly invalid)


def _coerce(hint, value):
    if hint is Any:
        return value

    if isinstance(hint, TypeVar):
        return _coerce(hint.__bound__ or Any, value)

    # discriminated union (e.g. ClientContext) — pick the concrete member.
    disc = _UNION_DISCRIMINATORS.get(hint)
    if disc is not None:
        if value is None:
            raise ValueError(f"{getattr(hint, '__name__', hint)} is required, got None")
        discriminator, mapping = disc
        tag = discriminator(value)
        member = mapping.get(tag)
        if member is None:
            # No member matches — an unreconstructable value (e.g. a stale row after
            # a context-model change). Raise so callers can skip it, matching the old
            # pydantic ValidationError behavior.
            raise ValueError(
                f"cannot reconstruct {getattr(hint, '__name__', hint)}: "
                f"no member for discriminator tag {tag!r}"
            )
        return _build(member, value)

    origin = get_origin(hint)

    if origin is typing.Union:
        args = get_args(hint)
        if value is None:
            if type(None) in args:
                return None
            raise ValueError(f"None is not valid for {hint}")
        non_none = [a for a in args if a is not type(None)]
        if len(non_none) == 1:
            return _coerce(non_none[0], value)
        return value  # ambiguous plain union: best-effort (none in this hierarchy)

    # Past this point None is only valid for Optional/Union (handled above) or Any.
    if value is None:
        raise ValueError(f"None is not valid for required field of type {hint}")

    if origin in (list, tuple):
        if not isinstance(value, (list, tuple)) or isinstance(value, (str, bytes)):
            raise TypeError(f"expected a list for {hint}, got {type(value).__name__}")
        (elem,) = get_args(hint) or (Any,)
        return [_coerce(elem, v) for v in value]

    if origin is dict:
        return value

    if origin is typing.Literal:
        if value not in get_args(hint):
            raise ValueError(f"{value!r} is not a valid {hint}")
        return value

    if isinstance(hint, type):
        if issubclass(hint, Serializable):
            return _build(hint, value)
        if issubclass(hint, datetime.datetime):
            return _parse_datetime(value)

    return value
