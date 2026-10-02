"""Contain configurations."""

from __future__ import annotations

__all__ = ["MISSING", "BaseConfig"]

from abc import ABC, abstractmethod
from typing import Any

from coola.hashing import hash_object
from coola.recursive import recursive_apply

MISSING = object()


class BaseConfig(ABC):
    """Define the interface shared by all configuration classes.

    Concrete subclasses only need to implement :meth:`to_kwargs` and
    :meth:`get_value`; :meth:`cache_key` is derived from
    :meth:`to_kwargs` automatically.

    Example:
        ```pycon
        >>> from zenpyre.utils.config import BaseConfig, MISSING
        >>> class ChatModelConfig(BaseConfig):
        ...     def __init__(self, model: str, temperature: float | None = None):
        ...         self.model = model
        ...         self.temperature = temperature
        ...     def get_value(self, name: str, default: Any = MISSING) -> Any:
        ...         kwargs = self.to_kwargs()
        ...         if name in kwargs:
        ...             return kwargs[name]
        ...         if default is not MISSING:
        ...             return default
        ...         raise KeyError(name)
        ...     def to_kwargs(self) -> dict:
        ...         return {"model": self.model, "temperature": self.temperature}
        ...
        >>> cfg = ChatModelConfig(model="gpt-4", temperature=0.2)
        >>> isinstance(cfg, BaseConfig)
        True

        ```
    """

    @abstractmethod
    def get_value(self, name: str, default: Any = MISSING) -> Any:
        """Get the value of a configuration field by name.

        Args:
            name: The name of the field to look up.
            default: The value to return if ``name`` is not present.
                If omitted, a missing ``name`` raises ``KeyError``
                instead. Since ``None`` is a valid field value,
                omitting ``default`` is the only way to distinguish
                "not present" from "present but set to ``None``" —
                passing ``default=None`` explicitly means a missing
                field silently returns ``None`` instead of raising.

        Returns:
            The value associated with ``name``, or ``default`` if not
                present and ``default`` was given.

        Raises:
            KeyError: If ``name`` is not present in this config and no
                ``default`` was given.

        Example:
            ```pycon
            >>> from zenpyre.utils.config import BaseConfig, MISSING
            >>> class ChatModelConfig(BaseConfig):
            ...     def __init__(self, model: str, temperature: float | None = None):
            ...         self.model = model
            ...         self.temperature = temperature
            ...     def get_value(self, name: str, default: Any = MISSING) -> Any:
            ...         kwargs = self.to_kwargs()
            ...         if name in kwargs:
            ...             return kwargs[name]
            ...         if default is not MISSING:
            ...             return default
            ...         raise KeyError(name)
            ...     def to_kwargs(self) -> dict:
            ...         return {"model": self.model, "temperature": self.temperature}
            ...
            >>> cfg = ChatModelConfig(model="gpt-4", temperature=0.2)
            >>> cfg.get_value("model")
            'gpt-4'
            >>> cfg.get_value("missing_key", default=42)
            42

            ```
        """

    @abstractmethod
    def to_kwargs(self) -> dict[str, Any]:
        """Return the configuration as a flat dict of keyword arguments.

        This is the single source of truth for the configuration's
        content: it is used both to construct/invoke the chat model
        and, via :meth:`cache_key`, to derive a stable hash. Any field
        that should affect caching or equality must be included here.

        Returns:
            A dict of keyword arguments representing this
                configuration.

        Example:
            ```pycon
            >>> from zenpyre.utils.config import BaseConfig, MISSING
            >>> class ChatModelConfig(BaseConfig):
            ...     def __init__(self, model: str, temperature: float | None = None):
            ...         self.model = model
            ...         self.temperature = temperature
            ...     def get_value(self, name: str, default: Any = MISSING) -> Any:
            ...         kwargs = self.to_kwargs()
            ...         if name in kwargs:
            ...             return kwargs[name]
            ...         if default is not MISSING:
            ...             return default
            ...         raise KeyError(name)
            ...     def to_kwargs(self) -> dict:
            ...         return {"model": self.model, "temperature": self.temperature}
            ...
            >>> cfg = ChatModelConfig(model="gpt-4", temperature=0.2)
            >>> cfg.to_kwargs()
            {'model': 'gpt-4', 'temperature': 0.2}

            ```
        """

    def cache_key(self, length: int = 64) -> str:
        """Return a stable hash string derived from the current
        configuration.

        Walks the ``to_kwargs()`` output and replaces any nested
        :class:`BaseConfig` instance with its own ``cache_key()`` string,
        then hashes the result via :func:`coola.hashing.hash_object`. The
        substitution step means two structurally-equal-but-distinct nested
        configs (e.g. two separately constructed ``ChatModelConfig``
        objects with the same fields) yield the same key, since the nested
        config contributes its content rather than its object identity.

        :func:`hash_object` canonicalizes its input (e.g. via sorted keys)
        before hashing, so two configs with identical (post-substitution)
        ``to_kwargs()`` output always produce the same hash regardless of
        field ordering.

        Note that this only covers whatever ``to_kwargs()`` returns. A
        subclass that adds a field must also include it in ``to_kwargs()``
        for it to affect the cache key.

        Useful for cache keys, output filenames, or detecting
        configuration changes between runs without comparing each field
        manually.

        Args:
            length: The desired length of the returned hash string.

        Returns:
            A stable hash string, ``length`` characters long.

        Example:
            ```pycon
            >>> from zenpyre.utils.config import BaseConfig, MISSING
            >>> class ChatModelConfig(BaseConfig):
            ...     def __init__(self, model: str, temperature: float | None = None):
            ...         self.model = model
            ...         self.temperature = temperature
            ...     def get_value(self, name: str, default: Any = MISSING) -> Any:
            ...         kwargs = self.to_kwargs()
            ...         if name in kwargs:
            ...             return kwargs[name]
            ...         if default is not MISSING:
            ...             return default
            ...         raise KeyError(name)
            ...     def to_kwargs(self) -> dict:
            ...         return {"model": self.model, "temperature": self.temperature}
            ...
            >>> cfg = ChatModelConfig(model="gpt-4", temperature=0.2)
            >>> key = cfg.cache_key()
            >>> len(key)
            64
            >>> cfg.cache_key() == cfg.cache_key()
            True

            ```
        """
        resolved_kwargs = recursive_apply(
            self.to_kwargs(), lambda x: x.cache_key() if isinstance(x, BaseConfig) else x
        )
        return hash_object(resolved_kwargs, length=length)
