"""Base class for AG Grid resource objects with JS expression handling."""

import typing
from typing import Any, Callable

from reflex.components.props import PropsBase
from reflex.utils import console
from reflex.utils.format import to_camel_case, to_snake_case
from reflex.utils.types import typehint_issubclass
from reflex.vars import FunctionVar

from ..resource import value_func_factory

# JS expression type for properties that can contain JavaScript code
JS_EXPRESSION = FunctionVar | str | dict | Callable


class AgGridResourceBase(PropsBase):
    """Base class for AG Grid resource objects with JS expression handling."""

    def __init__(self, **kwargs):
        """Initialize with camelCase to snake_case conversion for kwargs.

        Args:
            **kwargs: The field values to set.
        """
        # Convert camelCase kwargs to snake_case for compatibility with JS libraries
        field_names = self.get_fields()
        converted_kwargs = {}

        for key, value in kwargs.items():
            # Try exact match first
            if key in field_names:
                converted_kwargs[key] = value
            else:
                # Try converting camelCase to snake_case
                snake_key = to_snake_case(key)
                if snake_key in field_names:
                    converted_kwargs[snake_key] = value
                else:
                    # Keep as-is for unknown fields
                    converted_kwargs[key] = value

        super().__init__(**converted_kwargs)

    @classmethod
    def get_js_expressions(cls, camel_case: bool = False) -> dict[str, Any]:
        """Get the list of fields that are JS expressions.

        Args:
            camel_case: If True, convert field names to camelCase.

        Returns:
            Dictionary mapping field names to their types for JS expression fields.
        """
        return {
            to_camel_case(key) if camel_case else key: value.type_
            for key, value in cls.get_fields().items()
            if typehint_issubclass(JS_EXPRESSION, value.type_)
        }

    def _process_js_expressions(self, return_dict: dict) -> dict:
        """Process JS expressions in the dictionary.

        Args:
            return_dict: Dictionary to process JS expressions in.

        Returns:
            Dictionary with processed JS expressions.
        """
        for key, exp_types in self.get_js_expressions(camel_case=True).items():
            js_types = (
                _js_types if (_js_types := typing.get_args(exp_types)) else (exp_types,)
            )
            if key in return_dict:
                if isinstance(return_dict[key], dict):
                    return_dict[key] = value_func_factory(
                        return_dict[key]["function"],
                        self._known_components  # pyright: ignore [reportAttributeAccessIssue]
                        if hasattr(self, "_known_components")
                        else [],
                    )
                elif isinstance(return_dict[key], str):
                    return_dict[key] = value_func_factory(
                        return_dict[key],
                        self._known_components  # pyright: ignore [reportAttributeAccessIssue]
                        if hasattr(self, "_known_components")
                        else [],
                    )
                elif not isinstance(return_dict[key], js_types):
                    console.warn(
                        f"Unexpected type for JS expression in {key}: {type(return_dict[key])}. "
                        f"Expected one of: {js_types}."
                    )
        return return_dict

    def dict(self, *args, **kwargs) -> dict[str, Any]:
        """Override dict method to exclude None values and handle JS expressions.

        Args:
            *args: Arguments passed to parent dict method.
            **kwargs: Keyword arguments passed to parent dict method.

        Returns:
            Dictionary representation with processed JS expressions.
        """
        kwargs.setdefault("exclude_none", True)
        return_dict = super().dict(*args, **kwargs)

        # Process JS expressions
        return_dict = self._process_js_expressions(return_dict)

        return return_dict


class AgGridParamsBase(AgGridResourceBase):
    """Base class for AG Grid parameter classes with auto-naming conventions."""

    @classmethod
    def get_prop_name(cls) -> str:
        """Get the snake_case prop name from the class name.

        Example: DetailCellRendererParams -> detail_cell_renderer_params

        Returns:
            The snake_case property name.
        """
        return to_snake_case(cls.__name__)

    @classmethod
    def get_formatter_function_name(cls) -> str:
        """Get the JavaScript formatter function name from the class name.

        Example: DetailCellRendererParams -> formatDetailCellRendererParams

        Returns:
            The JavaScript formatter function name.
        """
        return f"format{cls.__name__}"
