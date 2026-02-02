import types
from collections.abc import Callable
from typing import (  # type: ignore
    Generic,
    Protocol,
    TypeVar,
    _GenericAlias,  # type: ignore
    _SpecialGenericAlias,  # type: ignore
)

from theutilitybelt.collections.queue import Queue

TypingGenericAlias = (_GenericAlias, _SpecialGenericAlias, types.GenericAlias)
GenericDefinitionClasses = (Generic, Protocol)


class _GenericTypeMapMeta(type):
    """
    Metaclass for GenericTypeMap that implements caching of instances.
    """

    _cache = {}

    def __call__(cls, mapped_type: type):
        if mapped_type in cls._cache:
            return cls._cache[mapped_type]
        instance = super().__call__(mapped_type)  # Create a new instance
        cls._cache[mapped_type] = instance  # Cache the new instance
        return instance


class GenericTypeMap(metaclass=_GenericTypeMapMeta):
    """
    A class that represents a mapping between generic types and their implementations.

    This class allows you to define a mapping between generic types and their corresponding
    implementations. It provides methods to access and modify the mapping.

    Example:
        ```python
        class Node(Generic[T]):
            pass

        class IntNode(Node[int]):
            pass

        mapping = GenericTypeMap(Node)

        mapping["T"] # Returns int
        mapping[T] # Returns int
        ```
    """

    def __init__(self, cls: type):
        self._inner_map: dict[str, TypeVar | type] = {}

        mapping = self._build_map(cls)

        for k, v in mapping.items():
            self._inner_map[self._lookup_key(k)] = v

    @classmethod
    def _get_generic_definitions(cls, type_cls: type):
        queue = Queue()
        queue.put(type_cls)
        aliases = []

        if root_origin := (getattr(type_cls, "__origin__", None)):
            queue.put(root_origin)

        while not queue.is_empty():
            type_check = queue.get()
            if getattr(type_check, "__origin__", None) in GenericDefinitionClasses:
                aliases.append(type_check)

            for base in getattr(type_check, "__orig_bases__", ()):
                queue.put(base)
                if orig := getattr(base, "__origin__", None):
                    queue.put(orig)

        return aliases

    @classmethod
    def _get_generic_implementations(cls, type_cls: type):
        queue = Queue()
        queue.put(type_cls)
        if orig := getattr(type_cls, "__origin__", None):
            queue.put(orig)

        aliases = []
        while not queue.is_empty():
            type_check = queue.get()
            if (
                type(type_check) is _GenericAlias
                and getattr(type_check, "__origin__", None)
                not in GenericDefinitionClasses
            ):
                aliases.append(type_check)

            for base in getattr(type_check, "__orig_bases__", ()):
                queue.put(base)
                if base_orig := getattr(base, "__origin__", None):
                    queue.put(base_orig)

        return aliases

    @classmethod
    def _close_off_possible_type_aliases(cls, mapping: dict[str, TypeVar | type]):
        found_link = False

        for k, v in mapping.items():
            if isinstance(v, TypeVar) and v is not k:
                if v in mapping and mapping[v] is not v:
                    mapping[k] = mapping[v]
                    found_link = True

        if found_link:
            cls._close_off_possible_type_aliases(mapping)

    @classmethod
    def _build_map(cls, type_cls: type) -> dict[str, TypeVar | type]:
        generic_definitions = cls._get_generic_definitions(type_cls)

        generic_implementations = cls._get_generic_implementations(type_cls)

        generic_definitions.reverse()
        generic_implementations.reverse()

        mapping = {}

        for idx, definition in enumerate(generic_definitions):
            additions = dict(zip(definition.__args__, definition.__args__))
            mapping = {**mapping, **additions}

        reduced_generic_definitions = generic_definitions[
            : len(generic_implementations)
        ]

        for idx, definition in enumerate(reduced_generic_definitions):
            implementation = generic_implementations[idx]
            additions = dict(zip(definition.__args__, implementation.__args__))
            mapping = {**mapping, **additions}

        cls._close_off_possible_type_aliases(mapping)

        return mapping

    @classmethod
    def _lookup_key(cls, key: TypeVar | str) -> str:
        if isinstance(key, TypeVar):
            return key.__name__
        return key

    def is_generic_mapping_open(self) -> bool:
        for k, v in self._inner_map.items():
            if isinstance(v, TypeVar):
                return True
        return False

    def is_generic_mapping_closed(self) -> bool:
        return not self.is_generic_mapping_open()

    def __getitem__(self, key: TypeVar | str):
        return self._inner_map[self._lookup_key(key)]

    def __setitem__(self, key: TypeVar | str, value: type | TypeVar):
        raise ValueError("Cannot set items in a GenericTypeMap")

    def values(self):
        return self._inner_map.values()

    def get(self, key: TypeVar | str, default=None):
        return self._inner_map.get(self._lookup_key(key), default)

    def items(self):
        return self._inner_map.items()

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, GenericTypeMap):
            return False
        return self._inner_map == __value._inner_map

    def __repr__(self) -> str:
        return f"GenericTypeMap({self._inner_map})"


def get_generic_bases(cls: type, filter: Callable[[type], bool] = lambda t: True):
    queue = Queue()
    queue.put(cls)
    items = []
    while not queue.is_empty():
        t = queue.get()

        for sub in getattr(t, "__orig_bases__", ()):
            queue.put(sub)
            if orig := getattr(sub, "__origin__", None):
                queue.put(orig)

            if filter(sub):
                items.append(sub)

    return items


def is_generic_type(tp: type):
    """Test if the given type is a generic type. This includes Generic itself, but
    excludes special typing constructs such as Union, Tuple, Callable, ClassVar.
    Example:

        is_generic_type(int) == False
        is_generic_type(Union[int, str]) == False
        is_generic_type(Union[int, T]) == False
        is_generic_type(ClassVar[List[int]]) == False
        is_generic_type(Callable[..., T]) == False

        is_generic_type(Generic) == True
        is_generic_type(Generic[T]) == True
        is_generic_type(Iterable[int]) == True
        is_generic_type(Mapping) == True
        is_generic_type(MutableMapping[T, List[int]]) == True
        is_generic_type(Sequence[Union[str, bytes]]) == True
    """

    return (
        isinstance(tp, type)
        and issubclass(tp, Generic)
        or isinstance(tp, TypingGenericAlias)
    )


def get_generic_type_args(type: type):
    queue = Queue()
    queue.put(type)

    while not queue.is_empty():
        type_check = queue.get()
        if origin_type := getattr(type_check, "__origin__", None):
            queue.put(origin_type)
            if origin_type in GenericDefinitionClasses:
                return type_check.__args__

        for base in getattr(type_check, "__orig_bases__", ()):
            queue.put(base)
            if base_origin := getattr(base, "__origin__", None):
                queue.put(base_origin)
    return ()


def try_to_map_generic_args_to_open_type(
    open_type: _GenericAlias, closed_type: type
) -> type:
    open_mapping = GenericTypeMap(open_type)
    closed_mapping = GenericTypeMap(closed_type)

    if open_mapping.is_generic_mapping_closed():
        return open_type

    output_args = []

    generic_args = get_generic_type_args(open_type)

    for a in generic_args:
        if from_closed := closed_mapping.get(a):
            output_args.append(from_closed)
            continue

        if from_open := open_mapping.get(a):
            if linked_to_open := closed_mapping.get(from_open):  # type: ignore
                output_args.append(linked_to_open)
                continue

        output_args.append(a)

    return open_type[tuple(output_args)]


def get_generic_type(obj):
    """Get the generic type of an object if possible, or runtime class otherwise.
    Examples::
        class Node(Generic[T]):
            ...
        type(Node[int]()) == Node
        get_generic_type(Node[int]()) == Node[int]
        get_generic_type(Node[T]()) == Node[T]
        get_generic_type(1) == int
    """

    gen_type = getattr(obj, "__orig_class__", None)
    return gen_type if gen_type is not None else type(obj)
