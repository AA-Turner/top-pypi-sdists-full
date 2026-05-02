"""Utility functions for AG Grid components."""

from typing import Any

import reflex as rx
from reflex.vars.base import Var

from .resources.base import AgGridParamsBase


def format_parameter_prop(
    props: dict[str, Any],
    param_class: type[AgGridParamsBase],
) -> None:
    """Format parameter props using class naming conventions.

    Args:
        props: The props dictionary to modify
        param_class: The parameter class with auto-naming methods
    """
    prop_name = param_class.get_prop_name()
    formatter_function_name = param_class.get_formatter_function_name()

    if (param_value := props.get(prop_name)) is not None:
        if isinstance(param_value, dict):
            # Static dict: process with parameter class
            props[prop_name] = param_class(**param_value).dict()
        elif isinstance(param_value, Var):
            # Var: call JavaScript formatter at runtime
            props[prop_name] = rx.vars.function.FunctionStringVar.create(
                formatter_function_name
            ).call(param_value)
