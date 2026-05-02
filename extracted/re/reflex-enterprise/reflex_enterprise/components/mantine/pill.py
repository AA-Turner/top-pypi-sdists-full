"""Pill component for displaying labels with optional remove button."""

from typing import Any, Literal

import reflex as rx
from reflex.vars.base import Var

from reflex_enterprise.components.mantine.base import MantineCoreBase


class Pill(MantineCoreBase):
    """Displays label with optional remove button."""

    tag = "Pill"

    # Controls component size; `'sm'` by default
    size: Var[Literal["xs", "sm", "md", "lg", "xl"]]

    # Determines whether the remove button should be displayed.
    with_remove_button: Var[bool]

    # Props passed down to the remove button. Ignored if with_remove_button is false.
    remove_button_props: Var[dict[str, Any]]

    # Key of theme.radius or any valid CSS value to set border-radius, numbers are converted to rem, 0 corresponds to 0px radius. Defaults to theme default radius for the component size.
    radius: Var[str | int]

    # Disabled state.
    disabled: Var[bool]

    # Controls appearance based on theme.color value, supports any color key of theme.colors.
    variant: Var[str]

    # Called when the remove button is clicked.
    on_remove: rx.EventHandler[lambda: []]


class PillGroup(MantineCoreBase):
    """Manages spacing between Pills."""

    tag = "Pill.Group"

    # Controls size of Pills within the group. Affects font-size and padding.
    size: Var[Literal["xs", "sm", "md", "lg", "xl"]]

    # Controls gap between pills. Defaults to `theme.spacing.xs`.
    gap: Var[str | int]

    # Disabled state.
    disabled: Var[bool]


# Namespace for Pill components
class PillNamespace(rx.ComponentNamespace):
    """Namespace for Pill components."""

    __call__ = staticmethod(Pill.create)
    group = staticmethod(PillGroup.create)


pill = PillNamespace()
