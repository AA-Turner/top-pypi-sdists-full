"""Validation helpers for public AdCP union aliases."""

from __future__ import annotations

from functools import lru_cache
from typing import Any, TypeVar, overload

from pydantic import TypeAdapter

_T = TypeVar("_T")


@lru_cache(maxsize=128)
def _union_adapter(union: Any, _identity: int) -> TypeAdapter[Any]:
    # Python compares unions without considering arm order, although that order
    # can change Pydantic's coercion. Identity keeps distinct aliases separate;
    # the cache's strong reference to union prevents reuse of a cached ID.
    return TypeAdapter(union)


@overload
def validate_union(union: type[_T], payload: Any) -> _T: ...


@overload
def validate_union(union: Any, payload: Any) -> Any: ...


def validate_union(union: Any, payload: Any) -> Any:
    """Validate *payload* against a type or union, reusing its adapter.

    Pass an exported union alias such as ``WholesaleFeedEvent`` or
    ``VendorPricingOption``. Validation preserves the alias's discriminator
    and returns the selected model directly, without a ``RootModel`` wrapper.
    Invalid documents raise :class:`pydantic.ValidationError`.

    Adapters for hashable aliases are cached on first use in a bounded cache.
    An alias containing unhashable annotation metadata is also supported,
    using an uncached adapter.
    """
    try:
        hash(union)
    except TypeError:
        return TypeAdapter(union).validate_python(payload)
    return _union_adapter(union, id(union)).validate_python(payload)


__all__ = ["validate_union"]
