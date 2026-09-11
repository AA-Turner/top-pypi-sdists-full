"""Bases shared by every entity and collection."""

from __future__ import annotations

# Python internals
from dataclasses import asdict, fields as dataclass_fields
from typing import Any, ClassVar, Generic, TypeVar, cast

# Current package
from dlthub_sdk._glue.context import M, _Ctx
from dlthub_sdk._glue.enums import EntityKind
from dlthub_sdk.errors import UnboundEntity

E = TypeVar("E", bound="Entity[Any]")

#: Entity subclasses already checked by _validate_class.
_validated: set[type] = set()


class Entity(Generic[M]):
    """Base for value objects.

    Subclasses declare ``@dataclass(frozen=True, repr=False)``, set ``_identity``
    and ``_kind``, and must not use ``slots=True``; :meth:`_validate_class`
    enforces all three. ``M`` is the transport mode, carried so navigation stays
    in one mode.

    ``_ctx`` is annotated here but is not a dataclass field, so it stays out of
    ``fields()``, ``asdict()``, equality and every derived schema.
    """

    _ctx: _Ctx[M]

    #: Fields that identify the entity, rendered by ``__repr__``.
    _identity: ClassVar[tuple[str, ...]] = ()

    #: What this entity is, declared by every subclass.
    _kind: ClassVar[EntityKind | None] = None

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Reject a subclass that left ``_identity`` or ``_kind`` unset.

        Args:
            **kwargs: Forwarded to ``super()``.

        Raises:
            TypeError: ``_identity`` is empty or ``_kind`` is unset.
        """
        super().__init_subclass__(**kwargs)
        # Runs before @dataclass, so fields are not visible yet — see _validate_class.
        if not cls._identity:
            raise TypeError(
                f"{cls.__name__} must set a non-empty _identity naming the fields "
                "its repr shows"
            )
        if cls._kind is None:
            raise TypeError(f"{cls.__name__} must set _kind to an EntityKind")

    @classmethod
    def _validate_class(cls) -> None:
        """Check the conventions @dataclass hides until it has run.

        Raises:
            TypeError: The subclass is not a frozen dataclass, shadows the base
                repr, uses slots, or names an unknown field in ``_identity``.
        """
        params = getattr(cls, "__dataclass_params__", None)
        if params is None:
            raise TypeError(f"{cls.__name__} must be a dataclass")
        if not params.frozen:
            raise TypeError(f"{cls.__name__} must be frozen=True")
        if cls.__repr__ is not Entity.__repr__:
            raise TypeError(
                f"{cls.__name__} must be declared repr=False; the generated repr "
                "shadows the identity repr and prints every field"
            )
        if "__slots__" in cls.__dict__:
            raise TypeError(f"{cls.__name__} must not use slots=True; _ctx has no slot")
        known = {f.name for f in dataclass_fields(cast(Any, cls))}
        unknown = [name for name in cls._identity if name not in known]
        if unknown:
            raise TypeError(f"{cls.__name__}._identity names unknown fields: {unknown}")

    def __getattr__(self, name: str) -> Any:
        # Reached only when normal lookup fails, i.e. _ctx was never bound.
        if name == "_ctx":
            raise UnboundEntity(
                f"{type(self).__name__} was constructed directly; obtain it from "
                "the SDK so it carries a context"
            )
        raise AttributeError(name)

    @classmethod
    def _bind(cls: type[E], ctx: _Ctx[Any], obj: E) -> E:
        if cls not in _validated:
            cls._validate_class()
            _validated.add(cls)
        object.__setattr__(obj, "_ctx", ctx)
        return obj

    def to_dict(self) -> dict[str, Any]:
        """Return the entity's fields as a plain dict, without the context.

        Values keep their Python types, so this is not JSON-ready.

        Returns:
            One key per dataclass field.
        """
        return asdict(cast(Any, self))

    def __repr__(self) -> str:
        shown = " ".join(f"{name}={getattr(self, name)!r}" for name in self._identity)
        return f"<{self._kind} {shown}>" if shown else f"<{self._kind}>"


class Namespace(Generic[M]):
    """Base for the context-holding objects a caller navigates through.

    Holds ``_ctx`` openly; a namespace is never serialized.
    """

    def __init__(self, ctx: _Ctx[M]) -> None:
        self._ctx: _Ctx[M] = ctx

    def _repr_label(self) -> str:
        return type(self).__name__

    def __repr__(self) -> str:
        parts = [self._repr_label(), "async" if self._ctx.is_async else "sync"]
        scope = self._ctx.scope_repr()
        parts.append(scope if scope else "unscoped")
        return f"<{' '.join(parts)}>"


class Collection(Namespace[M]):
    """A namespace over one kind of entity, named by ``_entity``.

    The entity carries the kind, so a collection cannot disagree with what it
    contains.
    """

    #: What this collection contains.
    _entity: ClassVar[type[Entity[Any]]]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Reject a collection that never said what it contains.

        Args:
            **kwargs: Forwarded to ``super()``.

        Raises:
            TypeError: ``_entity`` was left unset.
        """
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "_entity"):
            raise TypeError(f"{cls.__name__} must set _entity to an Entity subclass")

    @property
    def _kind(self) -> EntityKind | None:
        return self._entity._kind

    def _repr_label(self) -> str:
        return f"{self._kind}s"
