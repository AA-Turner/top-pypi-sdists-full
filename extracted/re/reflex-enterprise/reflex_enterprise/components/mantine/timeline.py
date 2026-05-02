"""Timeline component for displaying content divided into sections."""

from typing import Literal

import reflex as rx
from reflex.components.component import Component

from reflex_enterprise.components.mantine.base import MantineCoreBase


class Timeline(MantineCoreBase):
    """Display content divided into sections."""

    tag = "Timeline"

    # Index of the active item, -1 by default
    active: rx.Var[int]

    # Timeline alignment
    align: rx.Var[Literal["right", "left"]]

    # Determines whether icon color should depend on background-color. If luminosity of the color prop is less than theme.luminosityThreshold, then theme.white will be used for text color, otherwise theme.black. Overrides theme.autoContrast.
    auto_contrast: rx.Var[bool]

    # Bullet size
    bullet_size: rx.Var[float | str]

    # Active color from theme.colors
    color: rx.Var[str]

    # Line width
    line_width: rx.Var[float | str]

    # Radius from theme.radius, or number to calculate border-radius in px
    radius: rx.Var[float | str]

    # Reverse active direction without changing items order
    reverse_active: rx.Var[bool]

    _valid_children = ["TimelineItem"]


class TimelineItem(MantineCoreBase):
    """Item component for Timeline."""

    tag = "Timeline.Item"

    # Custom bullet replacing the default one
    bullet: rx.Var[Component | str]

    # Active color from theme.colors
    color: rx.Var[str]

    # Line border style
    line_variant: rx.Var[Literal["solid", "dashed", "dotted"]]

    # Radius from theme.radius, or number to calculate border-radius in px
    radius: rx.Var[float | str]

    # Item title, rendered next to the bullet
    title: rx.Var[str | Component]


# Define the namespace
class TimelineNamespace(rx.ComponentNamespace):
    """Timeline components namespace."""

    __call__ = Timeline.create
    item = TimelineItem.create


timeline = TimelineNamespace()
