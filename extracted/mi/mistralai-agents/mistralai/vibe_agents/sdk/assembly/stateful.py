"""Run calls of authored stateful objects against the values one Session saved.

A Session (in-process) or a Workflow run keeps one ``StateMap``: the saved value of each stateful
object, by a key fixed at assembly. Each call rebuilds the object from the authored one and that
value, and saves the object's new value only when the call succeeds. Calls of one key run one at
a time.
"""

import asyncio
import contextvars
import copy as copy_module
import json
import math
import sys
import warnings
from collections.abc import Awaitable, Callable, Iterable, Iterator, Mapping
from dataclasses import dataclass, field
from typing import Any, cast

from pydantic import BaseModel, JsonValue, ValidationError, ValidationInfo
from pydantic_core import SchemaValidator, core_schema

from mistralai.vibe_agents.sdk.authoring import stateful

# Bounds on Hook state. A saved value travels in each activity's input and result, and all of them
# in the Continue-As-New input, where Temporal refuses a payload over 2 MB. That input also carries
# the conversation, so these limits alone do not keep it under 2 MB.
# TODO: offload large saved values to external storage and keep only a reference in the Workflow
# payloads, so these limits can go up.
MAX_VALUE_BYTES = 64 * 1024
MAX_TOTAL_BYTES = 256 * 1024

# JSON has no NaN or infinity, so a dump writes such a float as null, which restores as None or fails.
_NON_FINITE_HINT = "; a float that is NaN or infinite is saved as null"


class SavedStateTooLargeError(ValueError):
    """A stateful object's saved value, or a Session's saved values together, exceed their limit."""


class StateMap:
    """The saved values of one Session's stateful objects, and one lock per key."""

    def __init__(self, values: Mapping[str, JsonValue] | None = None) -> None:
        self._values: dict[str, JsonValue] = dict(values or {})
        self._sizes: dict[str, int] = {key: _json_size(value) for key, value in self._values.items()}
        self._locks: dict[str, asyncio.Lock] = {}

    def get(self, key: str) -> JsonValue | None:
        return self._values.get(key)

    def set(self, key: str, value: JsonValue) -> None:
        """Save ``value`` under ``key``.

        Raises ``SavedStateTooLargeError``, and keeps the previous value, when the value or all the
        saved values together would exceed their limit.
        """

        size = _json_size(value)
        if size > MAX_VALUE_BYTES:
            raise SavedStateTooLargeError(
                f"the saved value of {_class_name(key, value)} is {size} bytes, over the limit of "
                f"{MAX_VALUE_BYTES} bytes for one object; keep its fields small, and anything else in a PrivateAttr"
            )
        total = sum(other for name, other in self._sizes.items() if name != key) + size
        if total > MAX_TOTAL_BYTES:
            raise SavedStateTooLargeError(
                f"saving {_class_name(key, value)} would make the Session's saved values {total} bytes, over "
                f"the limit of {MAX_TOTAL_BYTES} bytes; keep Hook fields small, and anything else in a PrivateAttr"
            )
        self._values[key] = value
        self._sizes[key] = size

    def lock(self, key: str) -> asyncio.Lock:
        lock = self._locks.get(key)
        if lock is None:
            lock = self._locks[key] = asyncio.Lock()
        return lock

    def values(self) -> dict[str, JsonValue]:
        return dict(self._values)


def check_starting_values(objects: Iterable[stateful.StatefulModel]) -> None:
    """Raise ``SavedStateTooLargeError`` when the objects of one Session start over a size limit.

    Such a Session would fail every call that saves one of them.
    """

    values = StateMap()
    for index, value in enumerate(objects):
        values.set(str(index), snapshot(value))


def _json_size(value: JsonValue) -> int:
    return len(json.dumps(value, separators=(",", ":"), ensure_ascii=False).encode())


def _class_name(key: str, value: JsonValue) -> str:
    """Name the class a saved value was dumped from, or fall back to its key."""

    ref = value.get(stateful.POLYMORPHIC_TYPE) if isinstance(value, Mapping) else None
    return _ref_name(ref) if ref is not None else key


def _ref_name(ref: JsonValue) -> str:
    if isinstance(ref, Mapping):
        args = ref.get("args")
        names = ", ".join(_ref_name(arg) for arg in args) if isinstance(args, list) else ""
        return f"{_ref_name(ref.get('origin'))}[{names}]"
    return str(ref).rpartition(":")[2]


def snapshot(value: stateful.StatefulModel) -> JsonValue:
    """Dump a stateful object to its saved JSON value."""

    dumped: JsonValue = value.model_dump(mode="json", by_alias=True)
    return dumped


def check_rebuildable(value: stateful.StatefulModel) -> None:
    """Raise ``TypeError`` unless ``value`` is rebuilt with the same field values, the way each call rebuilds it.

    The rebuild runs no ``__init__`` of ``value``, so a class with its own ``__init__`` passes.
    """

    try:
        rebuilt = restore(value, snapshot(value))
    except ValidationError as error:
        raise TypeError(_restore_error(error)) from error
    except ValueError as error:
        raise TypeError(str(error)) from error
    for name in type(value).model_fields:
        authored_field, rebuilt_field = getattr(value, name), getattr(rebuilt, name)
        if not _same_value(authored_field, rebuilt_field):
            hint = _NON_FINITE_HINT if isinstance(authored_field, float) and not math.isfinite(authored_field) else ""
            raise TypeError(
                f"field {name!r} holds {_short(authored_field)} but is rebuilt as {_short(rebuilt_field)}{hint}"
            )


def _same_value(authored: object, rebuilt: object) -> bool:
    """Compare two values by type and content: a model by its fields, a container item by item."""

    if type(authored) is int and type(rebuilt) is float:
        # A float field set to an int without validation, such as ``self.timeout = 30``, is rebuilt
        # as the same number.
        return authored == rebuilt
    if type(authored) is not type(rebuilt):
        return False
    if isinstance(authored, BaseModel):
        return all(_same_value(getattr(authored, name), getattr(rebuilt, name)) for name in type(authored).model_fields)
    if isinstance(authored, Mapping) and isinstance(rebuilt, Mapping):
        return authored.keys() == rebuilt.keys() and all(_same_value(authored[key], rebuilt[key]) for key in authored)
    if stateful.is_sequence(authored) and stateful.is_sequence(rebuilt):
        return len(authored) == len(rebuilt) and all(map(_same_value, authored, rebuilt))
    return bool(authored == rebuilt)


def _short(value: object, limit: int = 200) -> str:
    text = repr(value)
    return text if len(text) <= limit else f"{text[:limit]}..."


def restore[T: stateful.StatefulModel](authored: T, value: JsonValue) -> T:
    """Return a copy of the authored object with the saved field values.

    The copy keeps the private attributes of the authored object, and building it runs no
    ``__init__``, ``model_post_init`` or private attribute default factory of it. A stateful object
    in its fields is plain data: validation builds it, as Pydantic does. Raises ``TypeError`` when
    the value was saved for another class.
    """

    if not isinstance(value, Mapping):
        raise TypeError(f"the saved value of {type(authored).__qualname__} is not an object")
    fields = dict(value)
    saved_type = fields.pop(stateful.POLYMORPHIC_TYPE, None)
    expected = stateful.type_ref(type(authored))
    if saved_type != expected:
        raise TypeError(f"the saved value is for {saved_type!r}, but the authored object is {expected!r}")
    return _copy_with(authored, fields)


def _copy_with[T: BaseModel](authored: T, fields: Mapping[str, JsonValue]) -> T:
    """Validate saved field values into a shallow copy of ``authored``, as one model validation.

    Field and model validators run once, on the saved values. A field the dump leaves out gets its
    default. The copy keeps the private attributes of ``authored`` and any other attribute it holds,
    such as a ``functools.cached_property`` value, and runs no ``__init__`` or ``model_post_init``.
    Returns the instance validation returns, which an "after" or "wrap" model validator may replace.
    """

    cls = type(authored)
    copy = authored.model_copy()
    kept = (copy.__pydantic_private__, {k: v for k, v in authored.__dict__.items() if k not in cls.model_fields})
    validator = _copy_validator(cls)
    if validator is None:
        by_name = {_field_name(cls, key): item for key, item in fields.items()}
        result = cls.__pydantic_validator__.validate_python(by_name, self_instance=copy)
        _give_back(result, *kept)
        return cast(T, result)
    token = _KEPT.set((copy, *kept))
    try:
        result = validator.validate_python(dict(fields), self_instance=copy)
    finally:
        _KEPT.reset(token)
    return cast(T, result)


# The copy being validated, with the private attributes and other attributes it keeps.
_KEPT: contextvars.ContextVar[tuple[BaseModel, dict[str, Any] | None, dict[str, Any]] | None] = contextvars.ContextVar(
    "kept_attributes", default=None
)


def _put_kept_back(instance: BaseModel, _info: ValidationInfo) -> BaseModel:
    """Give the validated copy back what validation reset, before the model's own validators run."""

    kept = _KEPT.get()
    if kept is not None and kept[0] is instance:
        _give_back(instance, kept[1], kept[2])
    return instance


def _give_back(instance: BaseModel, private: dict[str, Any] | None, others: dict[str, Any]) -> None:
    object.__setattr__(instance, "__pydantic_private__", private)
    instance.__dict__.update(others)


def _copy_validator(cls: type[BaseModel]) -> SchemaValidator | None:
    """Return the validator of ``cls`` without its ``__init__`` and ``model_post_init``, for ``_copy_with``.

    Builds it once per class from the class's Pydantic core schema, which is not a public API. When
    the installed Pydantic builds no such validator, warns once and returns ``None``: the copy then
    takes Pydantic's public validation, which runs ``model_post_init`` and private attribute default
    factories, and runs model validators before the private attributes are given back.
    """

    if "__stateful_copy_validator__" in cls.__dict__:
        return cast("SchemaValidator | None", cls.__dict__["__stateful_copy_validator__"])
    try:
        validator: SchemaValidator | None = _build_copy_validator(cls)
    except Exception as error:  # noqa: BLE001 - any change in Pydantic's internals takes the public path
        validator = None
        warnings.warn(
            f"{cls.__qualname__} is copied for each call through Pydantic's public validation, since the "
            f"installed Pydantic cannot build the copy validator ({error!r}): each call runs its "
            "model_post_init and private attribute default factories",
            RuntimeWarning,
            stacklevel=2,
        )
    # Kept on the class itself, so the class can still be garbage-collected.
    setattr(cls, "__stateful_copy_validator__", validator)
    return validator


def _build_copy_validator(cls: type[BaseModel]) -> SchemaValidator:
    """Build the validator of ``cls`` without its ``model_post_init``.

    ``_copy_with`` validates into an existing instance, which already skips ``__init__``. It takes
    fields by their alias, as a dump names them.

    Only the outer model changes: a model of the same class nested in its fields validates as usual.
    """

    schema = copy_module.deepcopy(cls.__pydantic_core_schema__)
    definitions = schema["definitions"] if schema["type"] == "definitions" else None
    top = schema["schema"] if definitions is not None else schema
    if top["type"] == "definition-ref" and definitions is not None:
        missing: dict[str, Any] = {}
        top = copy_module.deepcopy(
            next((item for item in definitions if item.get("ref") == top["schema_ref"]), missing)
        )
        top.pop("ref", None)
    parent: dict[str, Any] | None = None
    model: dict[str, Any] = cast("dict[str, Any]", top)
    while model.get("type") != "model":
        if not isinstance(model.get("schema"), dict):
            raise TypeError(f"{cls.__qualname__} has a Pydantic core schema without a model, so it cannot be rebuilt")
        parent, model = model, model["schema"]
    model.pop("post_init", None)
    # A saved value names fields by their alias. Set in the schema, since a "wrap" model validator
    # would not pass on the by_alias and by_name of the call.
    model["config"] = {**model.get("config", {}), "validate_by_alias": True, "validate_by_name": False}
    wrapped = core_schema.with_info_after_validator_function(_put_kept_back, cast("core_schema.CoreSchema", model))
    if parent is None:
        top = wrapped
    else:
        parent["schema"] = wrapped
    if definitions is not None:
        top = core_schema.definitions_schema(cast("core_schema.CoreSchema", top), definitions)
    # Without _use_prebuilt=False, pydantic-core would reuse the class's own validator for the model.
    return SchemaValidator(cast("core_schema.CoreSchema", top), model.get("config"), _use_prebuilt=False)


def _field_name(cls: type[BaseModel], key: str) -> str:
    """Name the field a dump wrote under ``key``: its name, or its alias for a model that dumps by alias."""

    if key in cls.model_fields:
        return key
    for name, info in cls.model_fields.items():
        if key in (info.serialization_alias, info.alias):
            return name
    return key


@dataclass(frozen=True, slots=True)
class StatefulRow[T: stateful.StatefulModel]:
    """One authored stateful object, with the key and initial value fixed at assembly.

    An object without fields has nothing to save, so it is never dumped or rebuilt: every call runs
    on the authored object, and calls stay parallel.
    """

    key: str
    authored: T
    initial: JsonValue = field(init=False)
    # The modules a restarted process loads again, so the only ones a saved value may name classes of.
    loaded: frozenset[str] = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "initial", snapshot(self.authored) if self.has_state else None)
        object.__setattr__(self, "loaded", frozenset(sys.modules) if self.has_state else frozenset())

    @property
    def has_state(self) -> bool:
        return bool(type(self.authored).model_fields)

    async def call[R](self, values: StateMap, run: Callable[[T], Awaitable[R]]) -> R:
        """Run one call on a rebuilt object, and save its value when the call returns and the value restores."""

        if not self.has_state:
            return await run(self.authored)
        async with values.lock(self.key):
            saved = values.get(self.key)
            # A copy, so a call that changes a value in place and then fails leaves the saved value as it was.
            current = restore(self.authored, copy_module.deepcopy(saved if saved is not None else self.initial))
            result = await run(current)
            new = snapshot(current)
            self._check_restorable(current, new)
            values.set(self.key, new)
            return result

    def _check_restorable(self, current: T, value: JsonValue) -> None:
        """Raise ``ValueError`` unless ``value``, the dump of ``current``, restores here and in a restarted process."""

        for module in _named_modules(current):
            if module not in self.loaded:
                raise ValueError(
                    f"the new value of {type(self.authored).__qualname__} names a class of module {module!r}, "
                    "which was not loaded when the agent was assembled; import it at module level"
                )
        try:
            restore(self.authored, copy_module.deepcopy(value))
        except ValidationError as error:
            raise ValueError(
                f"the new value of {type(self.authored).__qualname__} cannot be restored, {_restore_error(error)}"
            ) from error


def _restore_error(error: ValidationError) -> str:
    """Name the first reason a saved value does not restore, and the field it is at."""

    first = error.errors()[0]
    place = ".".join(str(part) for part in first["loc"])
    nan = first["type"] == "float_type" and first["input"] is None
    where = f"at {place!r}: " if place else ""
    return where + first["msg"] + (_NON_FINITE_HINT if nan else "")


def _named_modules(value: stateful.StatefulModel) -> Iterator[str]:
    """Yield the module of each class ``type_ref`` names for ``value`` and each stateful object it holds."""

    for _, item in stateful.walk(value, type(value).__qualname__):
        if isinstance(item, stateful.StatefulModel):
            yield from _ref_modules(stateful.type_ref(type(item)))


def _ref_modules(ref: JsonValue) -> Iterator[str]:
    if isinstance(ref, Mapping):
        yield from _ref_modules(ref.get("origin"))
        args = ref.get("args")
        for arg in args if isinstance(args, list) else ():
            yield from _ref_modules(arg)
    elif isinstance(ref, str):
        yield ref.partition(":")[0]


__all__ = [
    "MAX_TOTAL_BYTES",
    "MAX_VALUE_BYTES",
    "SavedStateTooLargeError",
    "StateMap",
    "StatefulRow",
    "check_rebuildable",
    "check_starting_values",
    "restore",
    "snapshot",
]
