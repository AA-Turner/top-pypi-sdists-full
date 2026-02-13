import typing
import collections.abc
import typing_extensions
import numpy.typing as npt

class IDPropertyArray:
    typecode: typing.Any
    """ The type of the data in the array {'f': float, 'd': double, 'i': int, 'b': bool}."""

    def to_list(self) -> list[float] | list[int]:
        """Return the array as a list.

        :return: The array as a list.
        """

class IDPropertyGroup:
    name: typing.Any
    """ The name of this Group."""

    def clear(self) -> None:
        """Clear all members from this group."""

    def get(self, key: str, default: typing.Any | None = None) -> typing.Any:
        """Return the value for key, if it exists, else default.

        :param key: The key to look up.
        :param default: Value to return if key is not found.
        :return: The value for the key, or default if not found.
        """

    def items(self) -> IDPropertyGroupViewItems:
        """Iterate through the items in the dict; behaves like dictionary method items.

        :return: A view of the items.
        """

    def keys(self) -> IDPropertyGroupViewKeys:
        """Return the keys associated with this group.

        :return: The keys.
        """

    def pop(self, key: str, default: typing.Any | None = None) -> typing.Any:
        """Remove an item from the group, returning a Python representation.

        :param key: Name of item to remove.
        :param default: Value to return when key isnt found, otherwise raise an exception.
        :return: A Python representation of the removed item.
        """

    def to_dict(self) -> dict[str, typing.Any]:
        """Return a purely Python version of the group.

        :return: A dictionary representation of the group.
        """

    def update(self, other: dict[str, typing.Any] | typing_extensions.Self) -> None:
        """Update key-value pairs.

        :param other: Updates the values in the group with this.
        """

    def values(self) -> IDPropertyGroupViewValues:
        """Return the values associated with this group.

        :return: A view of the values.
        """

class IDPropertyGroupIterItems: ...
class IDPropertyGroupIterKeys: ...
class IDPropertyGroupIterValues: ...
class IDPropertyGroupViewItems(collections.abc.Iterable[tuple[str, typing.Any]]): ...
class IDPropertyGroupViewKeys(collections.abc.Iterable[str]): ...
class IDPropertyGroupViewValues(collections.abc.Iterable[typing.Any]): ...
