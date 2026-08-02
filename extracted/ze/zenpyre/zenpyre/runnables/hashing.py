r"""Provide hashing utilities."""

from __future__ import annotations

__all__ = ["SerializableHasher"]


from coola.hashing import BaseHasher, HasherRegistry, get_default_registry, hash_string
from langchain_core.load import Serializable


class SerializableHasher(BaseHasher[Serializable]):
    r"""Hasher for LangChain ``Serializable`` objects.

    This hasher applies ``registry.hash`` to the object's ``to_json()``
    output (its LangChain-serialized form: class id plus constructor
    kwargs), so two ``Serializable`` instances with equal serialized
    content produce the same hash regardless of object identity. Using
    the supplied ``registry`` (rather than a fixed global one) means
    nested values within ``to_json()`` are hashed with whatever hashers
    ``registry`` has registered, so ``registry`` must have hashers
    registered for the primitive types ``to_json()`` can produce (at
    minimum ``dict``, ``list``, and ``str``) -- ``coola``'s
    ``get_default_registry()`` satisfies this out of the box; a bare,
    empty ``HasherRegistry()`` does not.

    Raises:
        TypeError: Raised by :meth:`hash` if ``data`` is not
            LangChain-serializable (``data.is_lc_serializable()`` is
            ``False``) and ``ignore_unhashable`` is ``False``. In that
            case ``to_json()`` would return a generic "not implemented"
            sentinel shared by every non-serializable instance, which
            would silently hash all such instances to the same value
            regardless of their actual content -- raising instead of
            doing that. If ``ignore_unhashable`` is ``True``, a
            deterministic placeholder hash is returned instead, mirroring
            how ``HasherRegistry.hash`` handles types with no registered
            hasher.

    Example:
        ```pycon
        >>> from langchain_core.messages import HumanMessage
        >>> from coola.hashing import get_default_registry
        >>> from zenpyre.runnables.hashing import SerializableHasher
        >>> registry = get_default_registry()
        >>> hasher = SerializableHasher()
        >>> hasher
        SerializableHasher()
        >>> message = HumanMessage(content="hello")
        >>> len(hasher.hash(message, registry=registry))
        64

        ```
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def hash(
        self,
        data: Serializable,
        registry: HasherRegistry,
        length: int = 64,
        ignore_unhashable: bool = False,
    ) -> str:
        r"""Compute a deterministic hash of a ``Serializable`` object.

        Args:
            data: The ``Serializable`` instance to hash.
            registry: The hasher registry used to hash the nested
                values found in ``data.to_json()``.
            length: The desired length of the returned hex string.
                Defaults to 64.
            ignore_unhashable: If ``True``, non-serializable ``data``
                (and nested values within ``data.to_json()`` for which
                ``registry`` has no registered hasher) are replaced by
                a deterministic placeholder hash instead of raising -
                also passed through to ``registry.hash``.

        Returns:
            A lowercase hexadecimal string of exactly ``length``
            characters.

        Raises:
            TypeError: If ``data.is_lc_serializable()`` is ``False``
                and ``ignore_unhashable`` is ``False``.
        """
        if not data.is_lc_serializable():
            if ignore_unhashable:
                return hash_string(f"<unhashable:{type(data)!r}>", length=length)
            msg = f"Cannot hash non-serializable object of type {type(data).__qualname__}"
            raise TypeError(msg)
        return registry.hash(data.to_json(), length=length, ignore_unhashable=ignore_unhashable)


get_default_registry().register(Serializable, SerializableHasher(), exist_ok=True)
