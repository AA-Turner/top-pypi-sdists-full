from __future__ import annotations

import collections.abc
from typing import Any, Collection, Dict, Generic, Iterable, List, Sequence, Set, Tuple, TypeVar, Union, cast, overload

from typing_extensions import Annotated, get_args, get_origin

try:
    from types import UnionType
except ImportError:
    UnionType = Union

_NoneType = type(None)
_AnnotatedType = type(Annotated[int, ""])

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
B_co = TypeVar("B_co", covariant=True)
U = TypeVar("U")


def unwrap_annotated_if_needed(typ: Any):
    args = get_args(typ)
    if type(typ) is _AnnotatedType and hasattr(typ, "__metadata__"):  # pyright: ignore[reportUnnecessaryComparison]
        return args[0]
    return typ


def is_optional(typ: Any) -> bool:
    args = get_args(typ)
    return get_origin(typ) in (Union, UnionType) and len(args) == 2 and any(d is _NoneType for d in args)


def unwrap_optional_and_annotated_if_needed(typ: Any):
    typ = unwrap_annotated_if_needed(typ)
    if is_optional(typ):
        return next(m for m in get_args(typ) if m is not _NoneType)
    return typ


def is_namedtuple(value: Any) -> bool:
    """Infer whether value is a NamedTuple."""
    # From https://github.com/pola-rs/polars/blob/5f3e332fb2a653064f083b02949c527e0ec0afda/py-polars/polars/internals/construction.py#L78
    return all(hasattr(value, attr) for attr in ("_fields", "_field_defaults", "_replace"))


def flatten(v: Sequence[T | Sequence[T | Sequence[T]]]) -> List[T]:
    ret = []
    for x in v:
        if isinstance(x, collections.abc.Sequence) and not isinstance(x, (str, bytes, bytearray)):
            ret.extend(flatten(x))
        else:
            ret.append(x)
    return ret


@overload
def chunks(lst: List[T], n: int) -> Iterable[List[T]]:
    ...


@overload
def chunks(lst: Set[T], n: int) -> Iterable[Set[T]]:
    ...


@overload
def chunks(lst: Tuple[T, ...], n: int) -> Iterable[Tuple[T, ...]]:
    ...


@overload
def chunks(lst: Iterable[T], n: int) -> Iterable[Iterable[T]]:
    ...


def chunks(lst: Iterable[T], n: int) -> Iterable[Iterable[T]]:
    """Yield successive n-sized chunks from ``lst``, potentially lazily.

    Chunks are generated up-front if ``lst`` is a list, tuple, or set. In this case,
    the result will be an iterator of n-sized chunks of the underlying collection type.

    Otherwise, the chunks and the contents of each chunk are generated lazily,
    where at most one sample from ``lst`` is read in advance.

    Parameters
    ----------
    lst
        The collection
    n
        The chunk size. If <=0, then everything will be yielded back as one chunk.
    """
    if n <= 0:
        yield lst

    iterator = iter(lst)

    # Greedily loading the next sample to detect if we exhausted the iterable, so we don't yield an empty chunk at the end
    have_sample_to_yield = True
    try:
        next_sample = next(iterator)
    except StopIteration:
        have_sample_to_yield = False
        return

    def _get_chunk() -> Iterable[T]:
        """Get a chunk of size n from the generator, or raises StopIteration of the lst is empty"""
        nonlocal next_sample, have_sample_to_yield
        for _ in range(n):
            yield next_sample

            try:
                next_sample = next(iterator)
            except StopIteration:
                have_sample_to_yield = False
                break

    while have_sample_to_yield:
        chunk = _get_chunk()
        if isinstance(lst, (tuple, set, list)):
            # If the underlying collection is already allocated, then allocate the entire chunk at once
            # For backwards compatibility
            yield type(lst)(chunk)
        else:
            yield chunk


def ensure_tuple(x: T | Sequence[T] | Dict[Any, T] | None) -> Tuple[T, ...]:
    """Converts ``x`` into a tuple.
    * If ``x`` is `None`, then ``tuple()`` is returned.
    * If ``x`` is a tuple, then ``x`` is returned as-is.
    * If ``x`` is a list, then ``tuple(x)`` is returned.
    * If ``x`` is a dict, then ``tuple(v for v in x.values())`` is returned.
    Otherwise, a single element tuple of ``(x,)`` is returned.

    Parameters
    ----------
    x
        The input to convert into a tuple.

    Returns
    -------
    tuple
        A tuple of ``x``.
    """
    # From https://github.com/mosaicml/composer/blob/020ca02e3848ee8fb6b7fff0c8123f597b05be8a/composer/utils/iter_helpers.py#L40
    if x is None:
        return ()
    if isinstance(x, (str, bytes, bytearray)):
        return (cast(T, x),)
    if isinstance(x, collections.abc.Sequence):
        return tuple(x)
    if isinstance(x, dict):
        return tuple(x.values())
    return (x,)


def get_unique_item(collection: Iterable[T], name: str | None = None) -> T:
    """Get the unique item from the collection, ignoring equal duplicates.

    Raises a ValueError if there is not a single, unique element."""
    unique_item_or_none = get_unique_item_if_exists(collection, name)
    if unique_item_or_none is None:
        in_name = f" in `{name}`" if name is not None else ""
        raise ValueError(f"There should be at least one item{in_name}")
    return unique_item_or_none


def get_unique_item_if_exists(iterable: Iterable[T], name: str | None = None) -> T | None:
    """Get the unique item from the collection, if any element exists inside the collection.

    Raises a ValueError if there are multiple unique elements. Returns None if the collection is empty.
    """
    item = ...
    in_name = f" in `{name}`" if name is not None else ""
    for x in iterable:
        if item is ...:
            item = x
        if x != item:
            raise ValueError(f"Multiple values{in_name} are not permitted. Found {x}, {item}")
    if item is ...:
        return None
    return item


class BidirectionalMap(Generic[T, U]):
    """
    Represents a bijection between two sets of elements, with fast lookup for each direction.
    Under the hood keeps two dictionaries, one from T-->U and another from U-->T
    Constructor enforces that the mapping is a bijection.
    """

    def __init__(self, value_pairs: Sequence[Tuple[T, U]]):
        """
        Takes a sequence of pairs (t,u) to build the mapping t_i <--> u_i. Must be a bijection.
        :param value_pairs:
        """
        super().__init__()
        self._t_to_u: Dict[T, U] = dict(value_pairs)
        self._u_to_t: Dict[U, T] = dict([(v, k) for (k, v) in value_pairs])
        if (len(value_pairs) != len(self._t_to_u)) or (len(value_pairs) != len(self._u_to_t)):
            raise ValueError("Mapping is not a bijection.")

    def get(self, t: T, default: U | None = None) -> U | None:
        return self._t_to_u.get(t, default)

    def contains(self, t: T) -> bool:
        return t in self._t_to_u

    def get_reverse(self, u: U, default: T | None = None) -> T | None:
        return self._u_to_t.get(u, default)

    def contains_reverse(self, u: U) -> bool:
        return u in self._u_to_t

    def insert(self, t: T, u: U):
        """
        Raises if either element already exists.
        """
        if self.contains(t):
            raise ValueError(f"Element {t} already exists in forward mapping.")
        if self.contains_reverse(u):
            raise ValueError(f"Element {t} already exists in reverse mapping.")

    def __len__(self):
        return len(self._t_to_u)

    @classmethod
    def empty(cls):
        return cls(())


class OrderedSet(Generic[T]):
    """
    A_co set of items, with O(1) contains checks, which always iterates in insertion order.
    """

    __slots__ = ("_items",)

    def __init__(self, items: Iterable[T] = ()) -> None:
        """
        Create a new ordered set containing `items`.
        """
        super().__init__()
        self._items: dict[T, None] = dict.fromkeys(items)

    def add(self, item: T) -> None:
        """Adds `item` to the set, if it is not already present."""
        self._items[item] = None

    def update(self, items: Iterable[T]) -> None:
        """Adds all items from `items` to the set, skipping those that are already present."""
        for item in items:
            self._items[item] = None

    def remove(self, item: T) -> None:
        """Removes `item` from the set, if it is present. Otherwise, raises a KeyError."""
        del self._items[item]

    def discard(self, item: T) -> None:
        """Removes `item` from the set, if it is present. Otherwise, does nothing."""
        self._items.pop(item, None)

    def __len__(self) -> int:
        """Returns the number of items in the set."""
        return len(self._items)

    def __iter__(self):
        """Iterates over the items in insertion order."""
        return iter(self._items)

    def __contains__(self, item: object) -> bool:
        """Returns whether the given item is in the set."""
        return item in self._items

    def __or__(self, __value: Iterable[B_co]) -> "OrderedSet[T | B_co]":
        """Creates a new set containing values from both the left and the right."""
        return OrderedSet(tuple(self._items) + tuple(__value))

    def __and__(self, __value: Iterable[T]) -> "OrderedSet[T]":
        """Creates a new set containing only values found in both the left and the right."""
        value_set = set(__value)
        return OrderedSet(item for item in self._items if item in value_set)

    def __sub__(self, __value: Iterable[Any]) -> OrderedSet[T]:
        right = FrozenOrderedSet(__value)
        return OrderedSet(item for item in self if item not in right)

    def __rsub__(self, __value: Iterable[T]) -> Collection[T]:
        if isinstance(__value, (set, frozenset)):
            return __value - set(self)
        raise NotImplementedError

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, (set, frozenset)):
            return frozenset(self._items) == __value
        if not isinstance(__value, (OrderedSet, FrozenOrderedSet)):
            return NotImplemented
        return self._items == __value._items  # pyright: ignore[reportPrivateUsage]

    def issubset(self, other: set[T] | frozenset[T] | OrderedSet[T] | FrozenOrderedSet[T]) -> bool:
        return all(item in other for item in self)

    def issuperset(self, other: Iterable[Any]) -> bool:
        return all(item in self for item in other)

    def isdisjoint(self, other: Iterable[Any]) -> bool:
        return all(item not in self for item in other)

    def freeze(self) -> FrozenOrderedSet[T]:
        return FrozenOrderedSet(self)

    def __repr__(self) -> str:
        return f"OrderedSet({repr(tuple(self._items))})"

    def pop(self) -> T:
        """Removes the item that was last inserted into the ordered set"""
        item, _ = self._items.popitem()
        return item

    def pop_left(self) -> T:
        """Removes the item that was first inserted into the ordered set"""
        item = next(iter(self._items))
        del self._items[item]
        return item

    def clear(self) -> None:
        self._items.clear()


class FrozenOrderedSet(Generic[T_co]):
    """
    Frozen version of `OrderedSet[T_co]`, which can be used as a key in maps and sets.
    """

    __slots__ = ("_items", "_items_frozenset")

    def __init__(self, items: Iterable[T_co] = ()) -> None:
        super().__init__()
        if isinstance(items, FrozenOrderedSet):
            self._items: dict[T_co, None] = items._items
            self._items_frozenset = items._items_frozenset
        else:
            self._items = dict.fromkeys(items)
            self._items_frozenset = frozenset(self._items)

    def __len__(self) -> int:
        """Returns the number of items in the set."""
        return len(self._items)

    def __iter__(self):
        """Iterates over the items in insertion order."""
        return iter(self._items)

    def __contains__(self, item: object) -> bool:
        """Returns whether the given item is in the set."""
        return item in self._items

    def __or__(self, __value: Iterable[B_co]) -> "FrozenOrderedSet[T_co | B_co]":
        """Creates a new set containing values from both the left and the right."""
        return FrozenOrderedSet((*self._items, *__value))

    def __and__(self, __value: Iterable[T_co]) -> "FrozenOrderedSet[T_co]":
        """Creates a new set containing only values found in both the left and the right."""
        other_frozenset = frozenset(__value)
        return FrozenOrderedSet(item for item in self._items if item in other_frozenset)

    def __sub__(self, __value: Iterable[Any]) -> FrozenOrderedSet[T_co]:
        right = frozenset(__value)
        return FrozenOrderedSet(item for item in self if item not in right)

    def __rsub__(self, __value: Iterable[B_co]) -> FrozenOrderedSet[T_co | B_co]:
        return FrozenOrderedSet(x for x in __value if x not in self._items_frozenset)

    def __ror__(self, __value: Iterable[B_co]) -> FrozenOrderedSet[T_co | B_co]:
        return FrozenOrderedSet((*__value, *self._items))

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, FrozenOrderedSet):
            return self._items_frozenset == __value._items_frozenset
        if isinstance(__value, (set, frozenset)):
            return self._items_frozenset == __value
        if isinstance(__value, OrderedSet):
            return self._items_frozenset == frozenset(__value)
        return NotImplemented

    def issubset(
        self,
        other: set[T_co | B_co] | frozenset[T_co | B_co] | OrderedSet[T_co | B_co] | FrozenOrderedSet[T_co | B_co],
    ) -> bool:
        return all(item in other for item in self)

    def issuperset(self, other: Iterable[Any]) -> bool:
        return all(item in self._items_frozenset for item in other)

    def isdisjoint(self, other: Iterable[Any]) -> bool:
        return all(item not in self._items_frozenset for item in other)

    def __hash__(self) -> int:
        return hash(self._items_frozenset)

    def __repr__(self) -> str:
        return f"FrozenOrderedSet({repr(tuple(self._items))})"


def unwrap_optional(x: T | None) -> T:
    if x is None:
        raise ValueError("Value is None")
    return x
