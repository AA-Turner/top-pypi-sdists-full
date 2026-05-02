"""SemiCircleProgress component for Reflex."""

from typing import Literal

from reflex.components.component import Component  # noqa: F401
from reflex.vars.base import Var

from reflex_enterprise.components.mantine.base import MantineLabelProps


class SemiCircleProgress(MantineLabelProps):
    """Display semi circle progress bar."""

    tag = "SemiCircleProgress"

    # Progress value from 0 to 100
    value: Var[int]

    # Key of theme.colors or any valid CSS color value, by default the value is determined based on the color scheme value
    empty_segment_color: Var[str]

    # Key of theme.colors or any valid CSS color value, theme.primaryColor by default
    filled_segment_color: Var[str]

    # Direction from which the circle is filled, 'left-to-right' by default
    fill_direction: Var[Literal["right-to-left", "left-to-right"]]

    # Label position
    label_position: Var[Literal["center", "bottom"]]

    # Orientation of the circle, 'up' by default
    orientation: Var[Literal["up", "down"]]

    # Diameter of the svg in px, 200 by default
    size: Var[str | float]

    # Circle thickness in px, 12 by default
    thickness: Var[float]

    # Transition duration of filled section styles changes in ms, 0 by default
    transition_duration: Var[int]


semi_circle_progress = SemiCircleProgress.create
