"""Contain configurations."""

from __future__ import annotations

__all__ = ["ExtraFieldsConfig"]

import dataclasses
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import TYPE_CHECKING, Any

from zenpyre.utils.config.base import MISSING, BaseConfig

if TYPE_CHECKING:
    from typing import Self


@dataclass(frozen=True, kw_only=True)
class ExtraFieldsConfig(BaseConfig):
    """Base for configs that merge arbitrary keyword arguments ("extra")
    into :meth:`to_kwargs`, alongside whatever typed fields a subclass
    declares.

    Subclasses just need to be frozen dataclasses with their own typed
    fields; :meth:`to_kwargs`, :meth:`from_kwargs`, the extra/field-name
    collision check, and ``__hash__`` are all inherited from here and
    work automatically via introspection (:func:`dataclasses.fields`) —
    no per-subclass overriding required.

    ``extra`` is declared keyword-only (``kw_only=True`` on this class)
    specifically so that subclasses are free to add non-defaulted,
    positional-or-keyword fields of their own without hitting
    dataclass's "non-default argument follows default argument" error,
    which would otherwise apply because ``extra`` (with its default)
    is defined here in the base class.

    Attributes:
        extra: Additional keyword arguments merged into
            :meth:`to_kwargs`. Must not contain a key that collides
            with any of this config's own field names (including ones
            declared by a subclass).
    """

    extra: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        reserved = self._get_reserved_fields()
        collisions = reserved & self.extra.keys()
        if collisions:
            msg = (
                f"'extra' must not contain any of this config's own field names "
                f"{sorted(reserved)}; got overlapping key(s) {sorted(collisions)} "
                f"in extra={dict(self.extra)!r}."
            )
            raise ValueError(msg)
        # Wrap `extra` in a read-only view so mutating it after
        # construction raises, matching the `frozen=True` contract
        # (which otherwise only prevents reassigning the attribute
        # itself, not mutating the dict it points to).
        object.__setattr__(self, "extra", MappingProxyType(dict(self.extra)))

    def get_value(self, name: str, default: Any = MISSING) -> Any:
        """Get the value of a dataclass field (or ``extra`` entry) by
        name.

        Checks this config's own dataclass fields first (via ``getattr``,
        without needing to build the full :meth:`to_kwargs` dict just for
        a single lookup), then falls back to ``extra`` for keys that only
        live there.

        Args:
            name: The name of the field (or ``extra`` key) to look up.
            default: The value to return if ``name`` is not present.
                If omitted, a missing ``name`` raises ``KeyError``
                instead. Since ``None`` is a valid field value, omitting
                ``default`` is the only way to distinguish "not present"
                from "present but set to ``None``" — passing
                ``default=None`` explicitly means a missing field
                silently returns ``None`` instead of raising.

        Returns:
            The value associated with ``name``, or ``default`` if not
                present and ``default`` was given.

        Raises:
            KeyError: If ``name`` is not present in this config and no
                ``default`` was given.
        """
        if name != "extra" and name in self._get_reserved_fields():
            return getattr(self, name)
        if name in self.extra:
            return self.extra[name]
        if default is not MISSING:
            return default
        available = sorted({*self._get_reserved_fields(), *self.extra})
        msg = f"{name!r} not found in config {type(self).__name__}; available keys: {available}."
        raise KeyError(msg)

    def to_kwargs(self) -> dict[str, Any]:
        """Return every dataclass field (including ones declared by a
        subclass) merged with ``extra``, as a flat dict.

        Fields are collected via introspection
        (:func:`dataclasses.fields`) rather than hardcoded by name, so
        a subclass that adds a new typed field gets it included here
        automatically, with no need to override this method.

        Returns:
            A dict of keyword arguments representing this
                configuration.
        """
        kwargs = {
            f.name: getattr(self, f.name) for f in dataclasses.fields(self) if f.name != "extra"
        }
        kwargs.update(self.extra)
        return kwargs

    @classmethod
    def from_kwargs(cls, **kwargs: Any) -> Self:
        """Construct a config from arbitrary keyword arguments, routing
        each one to a real field if it matches one, or to ``extra``
        otherwise.

        A convenience alternative to the regular constructor's
        ``extra={...}`` dict, letting callers pass extra fields
        directly as keyword arguments instead of building the dict
        themselves. Which keys count as "real fields" is determined by
        introspection (:func:`dataclasses.fields`) on ``cls``, so this
        works automatically for any subclass without needing its own
        override — including subclasses that add their own typed
        fields.

        Args:
            **kwargs: Keyword arguments to route: keys matching one of
                this class's own dataclass field names (other than
                ``extra``) are passed through as that field's value;
                any remaining keys are collected into ``extra``.

        Returns:
            A new instance of ``cls``.

        Raises:
            ValueError: If, after routing, a key intended for ``extra``
                collides with one of this config's own field names —
                this can't actually happen through normal use of this
                method (a key either matches a field name and is routed
                there, or it doesn't and goes to ``extra``, so a
                collision would require the field-name set to change
                between routing and construction). Documented for
                completeness rather than as a realistic failure mode.
        """
        reserved = cls._get_reserved_fields()
        no_extra = {key: value for key, value in kwargs.items() if key in reserved}
        extra = {key: value for key, value in kwargs.items() if key not in reserved}
        return cls(**no_extra, extra=extra)

    @classmethod
    def _get_reserved_fields(cls) -> set[str]:
        # dataclasses.fields() accepts either a dataclass instance or a
        # dataclass type, so this works called either via an instance
        # (self._get_reserved_fields(), as in __post_init__) or via the
        # class itself (cls._get_reserved_fields(), as in from_kwargs).
        # It must be a classmethod (not a plain instance method) for
        # the latter call site to work at all.
        return {f.name for f in dataclasses.fields(cls) if f.name != "extra"}

    def __hash__(self) -> int:
        # The auto-generated dataclass __hash__ would hash `extra`
        # (and any nested BaseConfig field, unless it's independently
        # hashable) directly, which fails for an unhashable
        # dict/MappingProxyType. Hashing the (string) cache key
        # sidesteps that while keeping equal configs hash-equal.
        return hash(self.cache_key())
