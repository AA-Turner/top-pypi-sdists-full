from dataclasses import dataclass
from typing import Sequence, Optional
import skia
from .paint_source import PaintSource
from .color import SolidColor

@dataclass
class SweepGradient(PaintSource):
    """
    Represents a sweep (conical/angular) gradient fill, smoothly transitioning
    between colors in a circular sweep around a center point.

    The gradient sweeps around the center point in a full 360-degree circle,
    creating a conical color distribution. This is useful for creating
    color wheels, radial UI elements, and angular effects.

    Attributes:
        colors (Sequence[Union[SolidColor, str]]): A sequence of two or more colors
            that define the key colors of the gradient.
        stops (Optional[Sequence[float]]): A sequence of numbers between 0.0
            and 1.0 that specify the position of each color in the `colors`
            sequence. The length of `stops` must match the length of `colors`.
            If `None`, the colors are distributed evenly around the full circle.
            For example, for `colors` with 3 colors, `stops=[0.0, 0.5, 1.0]`
            would place the second color exactly halfway around the circle.
        center (tuple[float, float]): A tuple `(x, y)` representing the
            center point of the sweep gradient. Coordinates are relative to the
            object's bounding box, where (0.0, 0.0) is the top-left corner and
            (1.0, 1.0) is the bottom-right corner. Defaults to (0.5, 0.5) which
            is the center of the object.

    Example:
        # A simple full-circle sweep gradient
        ```python
        sweep_gradient = SweepGradient(
            colors=['#FF0000', '#00FF00', '#0000FF', '#FF0000']
        )
        ```

        # A color wheel with custom stops
        ```python
        color_wheel = SweepGradient(
            colors=['red', 'yellow', 'green', 'cyan', 'blue', 'magenta', 'red'],
            stops=[0.0, 0.16, 0.33, 0.5, 0.66, 0.83, 1.0]
        )
        ```
    """
    colors: Sequence[SolidColor]
    stops: Optional[Sequence[float]] = None
    center: tuple[float, float] = (0.5, 0.5)

    def __post_init__(self):
        self.colors = [
            SolidColor.from_str(c) if isinstance(c, str) else c
            for c in self.colors
        ]
        if not all(isinstance(c, SolidColor) for c in self.colors):
             raise TypeError("All items in 'colors' must be Color objects or valid color strings.")

        if len(self.colors) < 2:
            raise ValueError("At least 2 colors are required for a gradient.")

        if len(self.center) != 2:
            raise ValueError("center must be a tuple of 2 values (x, y).")
        if not all(0.0 <= v <= 1.0 for v in self.center):
            raise ValueError("center values must be between 0.0 and 1.0.")

        if self.stops is not None:
            if len(self.stops) != len(self.colors):
                raise ValueError(f"Length of 'stops' ({len(self.stops)}) must match length of 'colors' ({len(self.colors)}).")

            stops_list = list(self.stops)

            if not all(0.0 <= stop <= 1.0 for stop in stops_list):
                raise ValueError("All values in 'stops' must be between 0.0 and 1.0.")

            for i in range(len(stops_list) - 1):
                if stops_list[i] >= stops_list[i + 1]:
                    raise ValueError(f"Values in 'stops' must be strictly increasing. Found {stops_list[i]} >= {stops_list[i + 1]} at positions {i} and {i + 1}.")

    def apply_to_paint(self, paint: skia.Paint, bounds: skia.Rect) -> None:
        """Creates a sweep gradient shader and applies it to the paint."""
        if not self.colors:
            return

        skia_colors = [skia.Color(c.r, c.g, c.b, c.a) for c in self.colors]

        center_x = bounds.left() + self.center[0] * bounds.width()
        center_y = bounds.top() + self.center[1] * bounds.height()

        shader = skia.GradientShader.MakeSweep(
            cx=center_x,
            cy=center_y,
            colors=skia_colors,
            positions=self.stops if self.stops else []
        )
        paint.setShader(shader)
