"""
Base entity mixin providing common functionality for all entity types.

This module provides BaseEntityMixin, a generic mixin class that adds:
- Pretty-printed __repr__ showing all fields in multi-line format
- JSON serialization via __str__, to_json(), and to_dict()
- Smart formatting of various Python types (UUIDs, Enums, nested objects, etc.)

This mixin is designed to work with classes decorated with @functional.
"""

import json
from typing import Any, Optional


class BaseEntityMixin:
    """
    Base mixin providing common functionality for entity types.

    Provides:
    - __repr__: Multi-line Python representation showing all fields
    - __str__: Pretty JSON representation for printing
    - to_json(): Convert to JSON string
    - to_dict(): Convert to Python dictionary

    This mixin works with @functional decorated classes and regular classes.
    """

    def __repr__(self) -> str:
        """
        Returns a multi-line string representation of the object.
        Shows all instance attributes in a readable format.

        Returns:
            str: Multi-line string representation
        """
        try:
            class_name = self.__class__.__name__
            attrs = self._collect_repr_attributes()
            return self._build_repr_string(class_name, attrs)
        except Exception as e:
            return f"{self.__class__.__name__}(error_in_repr: {str(e)})"

    def _collect_repr_attributes(self) -> list[str]:
        """
        Collect and format all instance attributes for __repr__.

        Returns:
            list[str]: List of formatted attribute strings
        """
        attrs = []
        for attr_name in dir(self):
            if self._should_skip_attribute(attr_name):
                continue

            try:
                value = getattr(self, attr_name)
                clean_name = attr_name.lstrip("_")
                formatted_value = self._format_value(value)
                attrs.append(f"  {clean_name}={formatted_value}")
            except Exception:  # noqa
                continue

        return attrs

    def _should_skip_attribute(self, attr_name: str) -> bool:
        """
        Determine if an attribute should be skipped in __repr__.

        Parameters:
            attr_name: The attribute name to check

        Returns:
            bool: True if the attribute should be skipped
        """
        # Skip magic methods
        if attr_name.startswith("__"):
            return True

        # Skip property names without underscore (property accessors)
        if not attr_name.startswith("_"):
            return True

        # Check if it's a method by inspecting the class, not the instance
        # This avoids triggering property getters
        try:
            class_attr = getattr(self.__class__, attr_name, None)
            if callable(class_attr) and not isinstance(class_attr, property):
                return True
        except Exception:  # noqa
            pass

        return False

    def _build_repr_string(self, class_name: str, attrs: list[str]) -> str:
        """
        Build the final __repr__ string from class name and attributes.

        Parameters:
            class_name: Name of the class
            attrs: List of formatted attribute strings

        Returns:
            str: Formatted __repr__ string
        """
        if attrs:
            attrs_str = ",\n".join(attrs)
            return f"{class_name}(\n{attrs_str}\n)"

        # Fallback to simple representation
        if hasattr(self, "_id") and hasattr(self, "_name"):
            return f"{class_name}(id={self._id}, name='{self._name}')"
        elif hasattr(self, "_id"):
            return f"{class_name}(id={self._id})"
        else:
            return f"{class_name}()"

    def __str__(self) -> str:
        """
        Returns a pretty JSON representation of the object.
        Used when printing the object with print().

        Returns:
            str: Pretty JSON string representation
        """
        try:
            return self.to_json(indent=2)
        except Exception as e:
            # Fallback to simple JSON on error
            return json.dumps(
                {
                    "class": self.__class__.__name__,
                    "error": f"Error generating JSON representation: {str(e)}",
                },
                indent=2,
            )

    def to_json(self, indent: Optional[int] = None) -> str:
        """
        Converts the object to a JSON string representation.

        Parameters:
            indent (int, optional): Number of spaces for indentation.
                                   None for compact JSON.

        Returns:
            str: JSON string representation of the object
        """
        return json.dumps(self.to_dict(), indent=indent, default=str)

    def to_dict(self) -> dict:
        """
        Converts the object to a dictionary representation suitable for JSON serialization.

        Returns:
            dict: Dictionary representation of the object
        """
        result = {}

        # Iterate through all attributes
        for attr_name in dir(self):
            # Skip magic methods
            if attr_name.startswith("__"):
                continue

            # Skip property accessors (without underscore)
            if not attr_name.startswith("_"):
                continue

            # Check if it's a method by inspecting the class, not the instance
            # This avoids triggering property getters that may raise exceptions
            try:
                class_attr = getattr(self.__class__, attr_name, None)
                if callable(class_attr) and not isinstance(class_attr, property):
                    continue
            except Exception:  # noqa
                pass

            try:
                # Get the actual attribute value
                value = getattr(self, attr_name)

                # Format the attribute name (remove leading underscore)
                clean_name = attr_name.lstrip("_")

                # Convert value to JSON-serializable format
                result[clean_name] = self._to_json_value(value)

            except Exception:  # noqa
                # Skip attributes that can't be accessed
                continue

        return result

    def _to_json_value(self, value: Any) -> Any:
        """
        Convert a value to a JSON-serializable format.

        Parameters:
            value: The value to convert

        Returns:
            JSON-serializable value
        """
        # Handle None
        if value is None:
            return None

        # Handle strings, numbers, booleans
        if isinstance(value, (str, int, float, bool)):
            return value

        # Handle UUIDs
        if hasattr(value, "hex"):
            return str(value)

        # Handle Enums
        if hasattr(value, "value") and hasattr(value, "name"):
            return value.value

        # Handle lists
        if isinstance(value, list):
            return [self._to_json_value(item) for item in value]

        # Handle dicts
        if isinstance(value, dict):
            return {k: self._to_json_value(v) for k, v in value.items()}

        # Handle @functional objects or other objects with annotations
        if self._is_functional_object(value):
            return self._functional_object_to_dict(value)

        # Default: convert to string
        return str(value)

    def _functional_object_to_dict(self, obj: Any) -> dict:
        """
        Convert a @functional decorated object to a dictionary.

        Parameters:
            obj: The object to convert

        Returns:
            dict: Dictionary representation
        """
        result = {}

        if hasattr(obj.__class__, "__annotations__"):
            for attr_name in obj.__class__.__annotations__.keys():
                try:
                    attr_value = getattr(obj, attr_name, None)
                    if attr_value is not None:
                        result[attr_name] = self._to_json_value(attr_value)
                except Exception:  # noqa
                    continue

        return result

    def _format_value(self, value: Any, depth: int = 0, max_depth: int = 4) -> str:
        """
        Format a value for display in __repr__.

        Parameters:
            value: The value to format
            depth: Current recursion depth (for nested objects)
            max_depth: Maximum recursion depth to prevent infinite loops

        Returns:
            str: Formatted string representation of the value
        """
        if value is None:
            return "None"

        # Handle primitive types
        primitive_result = self._format_primitive_value(value)
        if primitive_result is not None:
            return primitive_result

        # Handle collection types
        collection_result = self._format_collection_value(value, depth, max_depth)
        if collection_result is not None:
            return collection_result

        # Handle objects
        return self._format_object_value(value, depth, max_depth)

    @staticmethod
    def _format_primitive_value(value: Any) -> Optional[str]:
        """
        Format primitive values (strings, UUIDs, Enums).

        Parameters:
            value: The value to format

        Returns:
            str or None: Formatted string if primitive, None otherwise
        """
        # Handle strings
        if isinstance(value, str):
            if len(value) > 100:
                return f"'{value[:97]}...'"
            return f"'{value}'"

        # Handle UUIDs (but exclude numeric types that also have .hex() method)
        if hasattr(value, "hex") and not isinstance(value, (int, float, bool)):
            return f"'{str(value)}'"

        # Handle Enums
        if hasattr(value, "value") and hasattr(value, "name"):
            return f"{value.__class__.__name__}.{value.name}"

        return None

    def _format_collection_value(
        self, value: Any, depth: int, max_depth: int
    ) -> Optional[str]:
        """
        Format collection values (lists, dicts).

        Parameters:
            value: The value to format
            depth: Current recursion depth
            max_depth: Maximum recursion depth

        Returns:
            str or None: Formatted string if collection, None otherwise
        """
        # Handle lists
        if isinstance(value, list):
            return self._format_list_value(value, depth, max_depth)

        # Handle dicts
        if isinstance(value, dict):
            return self._format_dict_value(value, depth, max_depth)

        return None

    def _format_list_value(self, value: list, depth: int, max_depth: int) -> str:
        """
        Format a list value.

        Parameters:
            value: The list to format
            depth: Current recursion depth
            max_depth: Maximum recursion depth

        Returns:
            str: Formatted list string
        """
        if len(value) == 0:
            return "[]"

        if len(value) <= 3:
            formatted_items = [
                self._format_value(item, depth + 1, max_depth) for item in value
            ]
            return f"[{', '.join(formatted_items)}]"

        # For long lists, show first 2 and count
        formatted_items = [
            self._format_value(item, depth + 1, max_depth) for item in value[:2]
        ]
        return f"[{', '.join(formatted_items)}, ... +{len(value)-2} more]"

    def _format_dict_value(self, value: dict, depth: int, max_depth: int) -> str:
        """
        Format a dict value.

        Parameters:
            value: The dict to format
            depth: Current recursion depth
            max_depth: Maximum recursion depth

        Returns:
            str: Formatted dict string
        """
        if len(value) == 0:
            return "{}"

        if len(value) <= 3:
            items = [
                f"'{k}': {self._format_value(v, depth + 1, max_depth)}"
                for k, v in value.items()
            ]
            return f"{{{', '.join(items)}}}"

        # For large dicts, show count
        return f"{{...}} ({len(value)} keys)"

    def _format_object_value(self, value: Any, depth: int, max_depth: int) -> str:
        """
        Format object values (@functional decorated or other objects).

        Parameters:
            value: The object to format
            depth: Current recursion depth
            max_depth: Maximum recursion depth

        Returns:
            str: Formatted object string
        """
        # Check if depth limit reached
        if depth >= max_depth:
            return f"{value.__class__.__name__}(...)"

        # Try to format as @functional object
        if self._is_functional_object(value):
            return self._format_functional_object(value, depth, max_depth)

        # Default: convert to string
        return str(value)

    @staticmethod
    def _is_functional_object(obj: Any) -> bool:
        """
        Check if an object is decorated with @functional or has annotations.

        Parameters:
            obj: Object to check

        Returns:
            bool: True if object appears to be a @functional decorated class
        """
        # Objects with @functional have class annotations
        # Check that __annotations__ exists AND is not empty
        return (
            hasattr(obj.__class__, "__annotations__")
            and bool(
                obj.__class__.__annotations__
            )  # Ensure annotations dict is not empty
            and not isinstance(obj, (str, int, float, bool, list, dict, tuple, set))
            and not hasattr(obj, "hex")  # Not a UUID
        )

    def _format_functional_object(self, obj: Any, depth: int, max_depth: int) -> str:
        """
        Format a @functional decorated object showing its attributes.

        Parameters:
            obj: The object to format
            depth: Current recursion depth
            max_depth: Maximum recursion depth

        Returns:
            str: Formatted string representation
        """
        class_name = obj.__class__.__name__

        # Get all non-None attributes
        attrs = []
        if hasattr(obj.__class__, "__annotations__"):
            for attr_name in obj.__class__.__annotations__.keys():
                try:
                    attr_value = getattr(obj, attr_name, None)
                    if attr_value is not None:
                        formatted = self._format_value(attr_value, depth + 1, max_depth)
                        attrs.append(f"{attr_name}={formatted}")
                except Exception:  # noqa
                    continue

        if attrs:
            # Show up to 3 attributes inline, then abbreviate
            if len(attrs) <= 3:
                return f"{class_name}({', '.join(attrs)})"
            else:
                # For many attributes, show first 2 and indicate more
                first_attrs = ", ".join(attrs[:2])
                return f"{class_name}({first_attrs}, ... +{len(attrs)-2} more)"
        else:
            return f"{class_name}()"

    def _isclass(self, obj: Any, cls: type) -> bool:  # noqa
        """
        Check if an object is an instance of a class.
        Works with @functional decorated classes.

        Parameters:
            obj: Object to check
            cls: Class to check against

        Returns:
            bool: True if obj is an instance of cls
        """
        try:
            return isinstance(obj, cls)
        except TypeError:
            # For @functional classes, isinstance doesn't work
            # Compare by instantiating and comparing class types
            try:
                return obj.__class__ == cls().__class__
            except Exception:  # noqa
                return False
