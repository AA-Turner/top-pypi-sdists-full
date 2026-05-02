"""PillsInput component for Mantine."""

from typing import Any, Literal

import reflex as rx
from reflex.vars.base import Var

from reflex_enterprise.components.mantine.base import MantineCoreBase

LiteralPillsInputSize = Literal["xs", "sm", "md", "lg", "xl"]
LiteralPillsInputFieldType = Literal["input", "pills", "cursor"]


class PillsInput(MantineCoreBase):
    """Displays pills in an input field."""

    tag = "PillsInput"

    # Controls input size.
    size: Var[LiteralPillsInputSize]

    # If set, the input is disabled.
    disabled: Var[bool]

    # Displays error message after input.
    error: Var[str]

    # Controls input appearance, defaults to default.
    variant: Var[str]

    # Reference to the input field.
    field_ref: Var[Any]


class PillsInputField(MantineCoreBase):
    """Renders input section."""

    tag = "PillsInput.Field"

    # Determines the type of the field.
    type: Var[LiteralPillsInputFieldType]

    # Show placeholder when field is empty.
    placeholder: Var[str]

    # If set, the input is disabled.
    disabled: Var[bool]


class PillsInputNamespace(rx.ComponentNamespace):
    """Namespace for PillsInput components."""

    __call__ = staticmethod(PillsInput.create)
    field = staticmethod(PillsInputField.create)


pills_input = PillsInputNamespace()
