"""RingProgress component for displaying progress in a circular shape."""

from typing import Any, TypedDict

import reflex as rx

from reflex_enterprise.components.mantine.base import MantineCoreBase


class Section(TypedDict, total=False):
    """Props for a section in the RingProgress component."""

    color: str
    value: float
    tooltip: str


class RingProgress(MantineCoreBase):
    """Displays progress in a circular shape."""

    tag = "RingProgress"

    # Text displayed in the center of the ring
    label: rx.Var[Any]

    # Sets whether the edges of the progress circle are rounded
    round_caps: rx.Var[bool]

    # Ring sections data
    sections: rx.Var[list[Section]]

    # Width and height of the progress ring
    size: rx.Var[float | str]

    # Ring thickness
    thickness: rx.Var[float]

    # Ring color from theme.colors
    color: rx.Var[str | list[str]]

    # Color of the root element, specified as theme color or CSS color value
    root_color: rx.Var[str]


ring_progress = RingProgress.create
