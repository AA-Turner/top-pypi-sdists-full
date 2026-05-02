"""JsonInput component for displaying JSON data."""

from typing import Any, Dict, List, Literal

import reflex as rx
from reflex.components.component import Component
from reflex.vars.base import Var

from reflex_enterprise.components.mantine.base import (
    BaseMantineInput,
    MantineDescriptionProps,
    MantineErrorProps,
    MantineLabelProps,
)


class JsonInput(
    BaseMantineInput,
    MantineLabelProps,
    MantineDescriptionProps,
    MantineErrorProps,
):
    """Display json data."""

    tag = "JsonInput"

    # If true, textarea height grows with content, limited by max_rows
    autosize: Var[bool]

    # Default value for uncontrolled component
    default_value: Var[str]

    # Sets disabled attribute on the input element
    disabled: Var[bool]

    # If true, JSON is formatted on blur
    format_on_blur: Var[bool]

    # size prop added to the input element
    input_size: Var[str]

    # Controls order of the Input.Wrapper elements
    input_wrapper_order: Var[List[Literal["label", "description", "input", "error"]]]

    # Maximum rows for autosize textarea to grow
    max_rows: Var[int]

    # Minimum rows for autosize textarea
    min_rows: Var[int]

    # Determines whether the input should have cursor: pointer style, false by default
    pointer: Var[bool]

    # Placeholder
    placeholder: Var[str]

    # Input border-radius
    radius: Var[str | int]

    # Sets required on input element
    required: Var[bool]

    # Input size
    size: Var[str]

    # Error message shown when JSON is not valid
    validation_error: Var[str | Component]

    # Input value
    value: Var[str]

    # Determines whether required asterisk should be displayed near the label
    with_asterisk: Var[bool]

    # Determines whether the input should have red border and red text color when the error prop is set, true by default
    with_error_styles: Var[bool]

    # Props spread to the Input.Wrapper element
    wrapper_props: Var[Dict[str, Any]]

    # Called when value changes
    on_change: rx.EventHandler[rx.event.passthrough_event_spec(str)]


json_input = JsonInput.create
