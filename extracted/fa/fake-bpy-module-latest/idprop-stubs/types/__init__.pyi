import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

class IDPropertyArray:
    """An array of values with a fixed type, supporting indexing and slicing."""

    typecode: typing.Literal["f", "d", "i", "b"]
    """ The type of the data in the array {'f': float (32-bit), 'd': double (64-bit), 'i': int, 'b': bool}. Both 'f' and 'd' use Python's `float` type but differ in storage precision."""

    def to_list(self) -> list[bool] | list[float] | list[int]:
        """Return the array as a list.

        :return: The array as a list.
        """

class IDPropertyGroup:
    """A dictionary-like group of ID properties, supporting key access, iteration, and membership testing."""

    name: str
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
        """Return a view of the items in the group, behaves like dictionary method items.

        :return: A view of the items.
        """

    def keys(self) -> IDPropertyGroupViewKeys:
        """Return a view of the keys in the group.

        :return: A view of the keys.
        """

    def pop(self, key: str, default: typing.Any) -> typing.Any:
        """Remove an item from the group, returning a Python representation.

        :param key: Name of item to remove.
        :param default: Value to return when key isnt found (optional, a `KeyError` is raised when omitted and the key is not found).
        :return: A Python representation of the removed item, or default.
        """

    def to_dict(self) -> dict[str, typing.Any]:
        """Return a purely Python version of the group.

        :return: A dictionary representation of the group.
        """

    def update(self, other: dict[str, typing.Any] | typing_extensions.Self) -> None:
        """Update key-value pairs from other, overwriting existing keys.

        :param other: Updates the values in the group with this.
        """

    def values(self) -> IDPropertyGroupViewValues:
        """Return the values associated with this group.

        :return: A view of the values.
        """

class IDPropertyGroupIterItems:
    """Iterator over `IDPropertyGroup` items (key/value pairs)."""

class IDPropertyGroupIterKeys:
    """Iterator over `IDPropertyGroup` keys."""

class IDPropertyGroupIterValues:
    """Iterator over `IDPropertyGroup` values."""

class IDPropertyGroupViewItems(collections.abc.Iterable[tuple[str, typing.Any]]):
    """A view of `IDPropertyGroup` items as key/value pairs (supports len(), in, iteration, and reversed())."""

class IDPropertyGroupViewKeys(collections.abc.Iterable[str]):
    """A view of `IDPropertyGroup` keys (supports len(), in, iteration, and reversed())."""

class IDPropertyGroupViewValues(collections.abc.Iterable[typing.Any]):
    """A view of `IDPropertyGroup` values (supports len(), in, iteration, and reversed())."""

class IDPropertyUIManager:
    """Manages the UI data of an ID property, see `bpy.types.bpy_struct.id_properties_ui`."""

    def as_dict(self) -> dict[str, typing.Any]:
        """Return a dictionary of the propertys RNA UI data. The fields in the
        returned dictionary and their types will depend on the propertys type.

                :return: The propertys UI data.
        """

    def clear(self) -> None:
        """Remove the RNA UI data from this IDProperty."""

    def update(
        self,
        *,
        subtype: bpy.stub_internal.rna_enums.PropertySubtypeItems = None,
        min: None | float | None = None,
        max: None | float | None = None,
        soft_min: None | float | None = None,
        soft_max: None | float | None = None,
        precision: None | int | None = None,
        step: None | float | None = None,
        default: typing.Any | None = None,
        id_type: bpy.stub_internal.rna_enums.IdTypeItems = None,
        items: None
        | collections.abc.Iterable[
            tuple[str, str, str]
            | tuple[str, str, str, int]
            | tuple[str, str, str, str | int, int]
            | None
        ]
        | None = None,
        description: None | str | None = None,
    ) -> None:
        """Update the RNA information of the IDProperty used for interaction and
        display in the user interface. The required types for many of the keyword
        arguments depend on the type of the property.

                :param subtype: Enumerator in `rna_enum_property_subtype_items`.
                :param min: Minimum value (int & float properties).
                :param max: Maximum value (int & float properties).
                :param soft_min: Soft minimum value (int & float properties).
                :param soft_max: Soft maximum value (int & float properties).
                :param precision: Number of digits to display after the decimal point
        (float properties).
                :param step: Step used when dragging the value (int & float properties).
                :param default: Default value, may be a sequence for array properties.
                :param id_type: Enumerator in `rna_enum_id_type_items` (ID properties).
                :param items: Enum items (int properties),
        see `bpy.props.EnumProperty` for the item format.
                :param description: Tooltip text.
        """

    def update_from(
        self,
        ui_manager_source: typing_extensions.Self,
        /,
    ) -> None:
        """Copy UI data from an IDProperty in the source group to a property in this group.
        If the source property has no UI data, the target UI data will be reset if it exists.

                :param ui_manager_source: The UI manager to copy from.
        """
