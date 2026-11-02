"""A Pydantic base for authored objects whose fields are their state.

The state of an object is its class plus the values of its fields. A dump names the class under
``polymorphic_type``, so a value validated as a base class comes back as the class it was dumped
from, through Temporal and in another process that loaded the class's module. Everything an
object needs that is not state is a ``PrivateAttr``: it is never saved.

A class is found again by its import path, among the modules already loaded: loading a value never
imports a module. ``check_importable`` tells early when a class could not be found again that way.
"""

from __future__ import annotations

import copy
import inspect
import sys
import warnings
from collections.abc import Iterator, Mapping, Sequence
from collections.abc import Set as AbstractSet
from pathlib import Path
from typing import Any, Self, TypeGuard

import pydantic
from pydantic import (
    BaseModel,
    ConfigDict,
    JsonValue,
    SerializerFunctionWrapHandler,
    ValidatorFunctionWrapHandler,
    model_serializer,
    model_validator,
)

POLYMORPHIC_TYPE = "polymorphic_type"

# A deprecation warning names the user's line, not a line in Pydantic or in this SDK.
_INTERNAL_PATHS = (str(Path(pydantic.__file__).parent), str(Path(__file__).parents[3]))


def warn_deprecated(message: str) -> None:
    warnings.warn(message, DeprecationWarning, skip_file_prefixes=_INTERNAL_PATHS)


def type_ref(cls: type, *, allow_local: bool = False) -> JsonValue:
    """Name a class so ``resolve`` finds it again, by import path and generic arguments.

    Raises ``TypeError`` for a class defined in a function, unless ``allow_local`` is set.
    """

    meta = getattr(cls, "__pydantic_generic_metadata__", None)
    if meta is not None and meta["origin"] is not None:
        return {
            "origin": type_ref(meta["origin"], allow_local=allow_local),
            "args": [type_ref(arg, allow_local=allow_local) for arg in meta["args"]],
        }
    if not isinstance(cls, type):
        raise TypeError(f"{cls!r} is not a class, so it cannot be found again by import")
    if not allow_local and "<locals>" in cls.__qualname__:
        raise TypeError(
            f"{_path(cls)} is defined inside a function, so it cannot be imported again; define it at module level"
        )
    return _path(cls)


def resolve(ref: object) -> type:
    """Find the class ``type_ref`` named, in a module that is already loaded.

    Raises ``ValueError`` for a name that does not lead to a class, or whose module is not loaded.
    """

    if isinstance(ref, Mapping):
        origin = resolve(ref.get("origin"))
        raw_args = ref.get("args")
        if not isinstance(raw_args, list) or not raw_args:
            raise ValueError(f"unknown {POLYMORPHIC_TYPE} {ref!r}: a generic needs its arguments")
        args = tuple(resolve(arg) for arg in raw_args)
        try:
            return origin[args if len(args) > 1 else args[0]]  # type: ignore[index]
        except TypeError as error:
            raise ValueError(f"unknown {POLYMORPHIC_TYPE} {ref!r}: {error}") from error
    if not isinstance(ref, str):
        raise ValueError(f"unknown {POLYMORPHIC_TYPE} {ref!r}")
    module, _, qualname = ref.partition(":")
    if not module or not qualname or "<locals>" in qualname:
        raise ValueError(f"unknown {POLYMORPHIC_TYPE} {ref!r}")
    found: object = sys.modules.get(module)
    if found is None:
        raise ValueError(
            f"unknown {POLYMORPHIC_TYPE} {ref!r}: module {module!r} is not loaded; "
            "import the class's module at module level, for example in the agent's module"
        )
    try:
        for part in qualname.split("."):
            # Static lookup: a module ``__getattr__`` or a descriptor never runs, so nothing is imported.
            found = inspect.getattr_static(found, part)
    except AttributeError as error:
        raise ValueError(f"unknown {POLYMORPHIC_TYPE} {ref!r}: {error}") from error
    if not isinstance(found, type):
        raise ValueError(f"unknown {POLYMORPHIC_TYPE} {ref!r}: it is not a class")
    return found


def check_importable(cls: type) -> None:
    """Raise ``TypeError`` unless the path ``type_ref`` gives for ``cls`` leads back to ``cls``.

    The class of a saved value is found only by its import path, so a class defined in a function, a
    class replaced by a later class of the same name, or a class its module does not expose fails
    here, before any value of it is saved.
    """

    ref = type_ref(cls)
    try:
        found = resolve(ref)
    except ValueError as error:
        raise TypeError(
            f"{_path(cls)} cannot be imported again by its path ({error}); define it at module level"
        ) from error
    if found is not cls:
        raise TypeError(
            f"{_path(cls)} is not the class its import path leads to: another class with the same name "
            "replaced it in its module; define each class once, at module level"
        )


def is_sequence(value: object) -> TypeGuard[Sequence[object]]:
    """Tell a container whose items keep their places, such as a list, tuple or deque, from text."""

    return isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray)


def walk(value: object, path: str) -> Iterator[tuple[str, object]]:
    """Yield ``value`` and every value its fields and containers hold, at any depth, with its path.

    Raises ``TypeError`` for a value that holds itself, which saved state cannot.
    """

    yield path, value
    yield from _walk_items(value, path, frozenset())


def _walk_items(value: object, path: str, active: frozenset[int]) -> Iterator[tuple[str, object]]:
    if isinstance(value, BaseModel):
        items = [(f"{path}.{name}", getattr(value, name)) for name in type(value).model_fields]
    elif isinstance(value, Mapping):
        items = [(f"{path}[{key!r}]", item) for key, item in value.items()]
    elif is_sequence(value) or isinstance(value, AbstractSet):
        items = [(f"{path}[{index}]", item) for index, item in enumerate(value)]
    else:
        return
    if id(value) in active:
        raise TypeError(f"{path} refers back to an object that holds it; saved state cannot hold a cycle")
    for place, item in items:
        yield place, item
        yield from _walk_items(item, place, active | {id(value)})


def _path(cls: type) -> str:
    return f"{cls.__module__}:{cls.__qualname__}"


class StatefulModel(BaseModel):
    """An authored object whose fields are its state; anything else is a ``PrivateAttr``."""

    # The constructor takes field names, and a saved value names fields by their alias, which
    # restoring it expects. A default is validated, so ``timeout: float = 30`` holds the 30.0 that
    # restoring its saved value gives.
    model_config = ConfigDict(
        extra="forbid",
        polymorphic_serialization=True,
        validate_by_name=True,
        validate_by_alias=False,
        serialize_by_alias=True,
        validate_default=True,
    )

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        for name, field in cls.model_fields.items():
            if POLYMORPHIC_TYPE in (name, field.alias, field.serialization_alias):
                # A dump writes the class under this key, so a field there would replace or lose it.
                raise TypeError(
                    f"{cls.__qualname__} declares the field {name!r} under the key {POLYMORPHIC_TYPE!r}, "
                    "which names the class in its saved value: rename the field or its alias"
                )
        if (computed := next(iter(cls.model_computed_fields), None)) is not None:
            # A dump writes a computed field with the fields, and restoring the dump refuses it.
            raise TypeError(
                f"{cls.__qualname__} declares the computed field {computed!r}, which its saved value cannot "
                "hold: use a plain property instead"
            )

    def __deepcopy__(self, memo: dict[int, Any] | None = None) -> Self:
        """Copy the field values deeply, and share everything else, such as a client in a ``PrivateAttr``."""

        copied = copy.copy(self)
        if memo is not None:
            memo[id(self)] = copied
        for name in type(self).model_fields:
            try:
                copied.__dict__[name] = copy.deepcopy(self.__dict__[name], memo)
            except Exception as error:
                raise TypeError(f"{type(self).__qualname__} cannot copy its field {name!r}: {error}") from error
        return copied

    def __setattr__(self, name: str, value: Any) -> None:
        cls = type(self)
        if not name.startswith("__") and not hasattr(self, "__pydantic_fields_set__"):
            if name in cls.model_fields:
                raise AttributeError(
                    f"{cls.__qualname__} sets the field {name!r} before calling super().__init__(): "
                    f"call super().__init__() first, or pass the value as super().__init__({name}=...)"
                )
            if name in cls.__private_attributes__:
                raise AttributeError(
                    f"{cls.__qualname__} sets the private attribute {name!r} before calling "
                    "super().__init__(): call super().__init__() first"
                )
        if name.startswith("__") or _is_declared(cls, name):
            super().__setattr__(name, value)
            return
        self._set_undeclared(name, value)

    def _set_undeclared(self, name: str, value: Any) -> None:
        raise AttributeError(
            f"{type(self).__qualname__} has no attribute {name!r}; declare it as a field or a PrivateAttr"
        )

    @model_serializer(mode="wrap")
    def _write_polymorphic_type(self, handler: SerializerFunctionWrapHandler) -> Any:
        return {POLYMORPHIC_TYPE: type_ref(type(self)), **handler(self)}

    @model_validator(mode="wrap")
    @classmethod
    def _read_polymorphic_type(cls, data: Any, handler: ValidatorFunctionWrapHandler) -> Self:
        if not isinstance(data, Mapping) or POLYMORPHIC_TYPE not in data:
            return handler(data)
        fields = dict(data)
        ref = fields.pop(POLYMORPHIC_TYPE)
        if ref == type_ref(cls, allow_local=True):
            return handler(fields)
        target = resolve(ref)
        if not issubclass(target, cls):
            raise ValueError(
                f"{POLYMORPHIC_TYPE} {ref!r} names {target.__qualname__}, which is not a {cls.__qualname__}"
            )
        return target.model_validate(fields)


def _is_declared(cls: type[BaseModel], name: str) -> bool:
    return name in cls.model_fields or name in cls.__private_attributes__ or hasattr(cls, name)


__all__ = [
    "POLYMORPHIC_TYPE",
    "StatefulModel",
    "check_importable",
    "is_sequence",
    "resolve",
    "type_ref",
    "walk",
    "warn_deprecated",
]
