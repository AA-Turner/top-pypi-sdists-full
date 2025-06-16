from typing import Any, Iterator, Literal, Tuple

from msgspec import UNSET, Struct


_getattribute = object.__getattribute__


class DictStruct(Struct, dict=True):  # type: ignore [call-arg]
    """
    A base class that extends the :class:`msgspec.Struct` class to be compatible with the standard python dictionary API.

    Allows iteration over the fields of a struct and provides a dictionary-like interface for retrieving values by field name.

    Note:
        Attempting to access an attribute that is set to :obj:`~msgspec.UNSET` will raise an :class:`AttributeError`
        when accessed as an attribute, or a :class:`KeyError` when accessed using dictionary-style access. This behavior
        indicates that the attribute/key is not present on the DictStruct object.

    Example:
        >>> class MyStruct(DictStruct):
        ...     field1: str
        ...     field2: int
        ...     field3: int = UNSET
        >>> s = MyStruct(field1="value", field2=42)
        >>> list(s.keys())
        ['field1', 'field2']
        >>> s['field1']
        'value'
        >>> s.field3
        Traceback (most recent call last):
            ...
        AttributeError: "'MyStruct' object has no attribute 'field3'"
        >>> s['field3']
        Traceback (most recent call last):
            ...
        KeyError: ('field3', MyStruct(field1='value'))
    """

    def __bool__(self) -> Literal[True]:
        """Unlike a dictionary, a Struct will always exist.

        Example:
            >>> class MyStruct(DictStruct):
            ...     pass
            >>> bool(MyStruct())
            True
        """
        return True

    def __contains__(self, key: str) -> bool:
        """
        Check if a key is in the struct.

        Args:
            key: The key to check.

        Returns:
            True if the key is present and not :obj:`~msgspec.UNSET`, False otherwise.

        Example:
            >>> class MyStruct(DictStruct):
            ...     field1: str
            >>> s = MyStruct(field1="value")
            >>> 'field1' in s
            True
            >>> 'field2' in s
            False
        """
        return key in self.__struct_fields__ and getattr(self, key, UNSET) is not UNSET

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get the value associated with a key, or a default value if the key is not present.

        Args:
            key: The key to look up.
            default (optional): The value to return if the key is not present.

        Example:
            >>> class MyStruct(DictStruct):
            ...     field1: str
            >>> s = MyStruct(field1="value")
            >>> s.get('field1')
            'value'
            >>> s.get('field2', 'default')
            'default'
        """
        return getattr(self, key, default)

    def __getitem__(self, attr: str) -> Any:
        """
        Lookup an attribute value via dictionary-style access.

        Args:
            attr: The name of the attribute to access.

        Raises:
            KeyError: If the provided key is not a member of the struct.

        Example:
            >>> class MyStruct(DictStruct):
            ...     field1: str
            >>> s = MyStruct(field1="value")
            >>> s['field1']
            'value'
            >>> s['field2']
            Traceback (most recent call last):
                ...
            KeyError: ('field2', MyStruct(field1='value'))
        """
        try:
            return getattr(self, attr)
        except AttributeError as e:
            raise KeyError(attr, self) from e.__cause__

    def __getattribute__(self, attr: str) -> Any:
        """
        Get the value of an attribute, raising AttributeError if the value is :obj:`~msgspec.UNSET`.

        Args:
            attr: The name of the attribute to fetch.

        Raises:
            AttributeError: If the attribute is not found or is considered unset (:obj:`~msgspec.UNSET`).

        Example:
            >>> class MyStruct(DictStruct):
            ...     field1: str = UNSET
            >>> s = MyStruct()
            >>> s.field1
            Traceback (most recent call last):
                ...
            AttributeError: "'MyStruct' object has no attribute 'field1'"

        See Also:
            :meth:`__getitem__` for dictionary-style access.
        """
        value = _getattribute(self, attr)
        if value is UNSET:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{attr}'"
            )
        return value

    def __setitem__(self, attr: str, value: Any) -> None:
        """
        Set the value of an attribute, raising AttributeError if the instance's type is frozen.

        Args:
            attr: The name of the item to set.
            value: The value to set.

        Raises:
            AttributeError: If the type of the instance was initialized with `frozen=True`.

        Example:
            >>> class MyStruct(DictStruct):
            ...     field1: str
            >>> s = MyStruct("some value")
            >>> s["field1"] = "new value"
            >>> # Now let's try with a frozen struct
            >>> class MyFrozenStruct(DictStruct, frozen=True):
            ...     field1: str
            >>> s = MyFrozenStruct("some value")
            >>> s["field1"] = "new value"
            Traceback (most recent call last):
                ...
            AttributeError: "immutable type: 'MyFrozenStruct'"
        """
        try:
            setattr(self, attr, value)
        except AttributeError as e:
            raise TypeError(*e.args) from e.__cause__

    def __iter__(self) -> Iterator[str]:
        """
        Iterate through the keys of the Struct.

        Yields:
            Struct key.

        Example:
            >>> class MyStruct(DictStruct):
            ...     field1: str
            ...     field2: int
            >>> s = MyStruct(field1="value", field2=42)
            >>> list(iter(s))
            ['field1', 'field2']
        """
        for field in self.__struct_fields__:
            value = getattr(self, field, UNSET)
            if value is not UNSET:
                yield field

    def __len__(self) -> int:  # sourcery skip: identity-comprehension
        """
        The number of keys in the Struct.

        Example:
            >>> class MyStruct(DictStruct):
            ...     field1: str
            ...     field2: int
            >>> s = MyStruct(field1="value", field2=42)
            >>> len(s)
            2
        """
        return len([key for key in self])

    def keys(self) -> Iterator[str]:
        """
        Returns an iterator over the field names of the struct.

        Example:
            >>> class MyStruct(DictStruct):
            ...     field1: str
            ...     field2: int
            >>> s = MyStruct(field1="value", field2=42)
            >>> list(s.keys())
            ['field1', 'field2']
        """
        yield from self

    def items(self) -> Iterator[Tuple[str, Any]]:
        """
        Returns an iterator over the struct's field name and value pairs.

        Example:
            >>> class MyStruct(DictStruct):
            ...     field1: str
            ...     field2: int
            >>> s = MyStruct(field1="value", field2=42)
            >>> list(s.items())
            [('field1', 'value'), ('field2', 42)]
        """
        for key in self.__struct_fields__:
            value = getattr(self, key, UNSET)
            if value is not UNSET:
                yield key, value

    def values(self) -> Iterator[Any]:
        """
        Returns an iterator over the struct's field values.

        Example:
            >>> class MyStruct(DictStruct):
            ...     field1: str
            ...     field2: int
            >>> s = MyStruct(field1="value", field2=42)
            >>> list(s.values())
            ['value', 42]
        """
        for key in self.__struct_fields__:
            value = getattr(self, key, UNSET)
            if value is not UNSET:
                yield value

    def __hash__(self) -> int:
        """
        A frozen Struct is hashable but only if the fields are all hashable as well.

        This modified hash function attempts to hash the fields directly and converts any list fields to tuples if a `TypeError` is raised.

        Raises:
            TypeError: If the struct is not frozen.

        Example:
            >>> class MyStruct(DictStruct, frozen=True):
            ...     field1: str
            ...     field2: list
            >>> s = MyStruct(field1="value", field2=[1, 2, 3])
            >>> hash(s)
            123456789  # Example output, actual value will vary
        """
        if not self.__struct_config__.frozen:
            raise TypeError(f"unhashable type: '{type(self).__name__}'")
        if cached_hash := self.__dict__.get("__hash__"):
            return cached_hash
        fields = (
            _getattribute(self, field_name)
            for field_name in self.__struct_fields__
        )
        try:
            # Skip if-checks, just try it
            try:
                self.__dict__["__hash__"] = hash(fields)
            except TypeError:  # unhashable type: 'list'
                self.__dict__["__hash__"] = hash(
                    tuple(f) if isinstance(f, list) else f for f in fields
                )
        except Exception as e:
            e.args = *e.args, "recursed in hash fn"
        return self.__dict__["__hash__"]
    
