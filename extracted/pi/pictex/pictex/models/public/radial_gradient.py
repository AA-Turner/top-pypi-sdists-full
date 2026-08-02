from dataclasses import dataclass
from typing import Sequence, Optional
import skia
from .paint_source import PaintSource
from .color import SolidColor

@dataclass
class RadialGradient(PaintSource):
    """
    Represents a radial gradient fill, smoothly transitioning between colors
    from a center point outward in a circular pattern.

    The gradient's center, radius, and color distribution are controlled by its
    parameters.

    Attributes:
        colors (Sequence[Union[SolidColor, str]]): A sequence of two or more colors
            that define the key colors of the gradient.
        stops (Optional[Sequence[float]]): A sequence of numbers between 0.0
            and 1.0 that specify the position of each color in the `colors`
            sequence. The length of `stops` must match the length of `colors`.
            If `None`, the colors are distributed evenly from center to edge.
            For example, for `colors` with 3 colors, `stops=[0.0, 0.5, 1.0]`
            would place the second color exactly halfway between center and edge.
        center (tuple[float, float]): A tuple `(x, y)` representing the
            center point of the radial gradient. Coordinates are relative to the
            object's bounding box, where (0.0, 0.0) is the top-left corner and
            (1.0, 1.0) is the bottom-right corner. Defaults to (0.5, 0.5) which
            is the center of the object.
        radius (float): The radius of the gradient circle, relative to the
            object's dimensions. A value of 0.5 means the radius extends halfway
            across the bounding box. Must be positive. Defaults to 0.5.

    Example:
        # A simple radial gradient from red (center) to blue (edge)
        ```python
        radial_gradient = RadialGradient(
            colors=['#FF0000', 'blue']
        )
        ```

        # A radial gradient centered at top-left corner
        ```python
        corner_gradient = RadialGradient(
            colors=['yellow', 'orange'],
            center=(0.0, 0.0),
            radius=0.7
        )
        ```

        # A radial gradient with custom color stops
        ```python
        multi_stop_gradient = RadialGradient(
            colors=[
                'magenta',
                'cyan',
                'yellow'
            ],
            stops=[0.0, 0.3, 1.0]  # 'cyan' positioned 30% from center
        )
        ```
    """
    colors: Sequence[SolidColor]
    stops: Optional[Sequence[float]] = None
    center: tuple[float, float] = (0.5, 0.5)
    radius: float = 0.5

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

        if self.radius <= 0 or self.radius > 1.0:
            raise ValueError("Radius must be between 0.0 and 1.0.")

        if self.stops is not None:
            if len(self.stops) != len(self.colors):
                raise ValueError(f"Length of 'stops' ({len(self.stops)}) must match length of 'colors' ({len(self.colors)}).")

            stops_list = list(self.stops)

            if not all(0.0 <= stop <= 1.0 for stop in stops_list):
                raise ValueError("All values in 'stops' must be between 0.0 and 1.0.")

            for i in range(len(stops_list) - 1):
                if stops_list[i] > stops_list[i + 1]:
                    raise ValueError(f"Values in 'stops' must be strictly increasing. Found {stops_list[i]} >= {stops_list[i + 1]} at positions {i} and {i + 1}.")

    def apply_to_paint(self, paint: skia.Paint, bounds: skia.Rect) -> None:
        """Creates a radial gradient shader and applies it to the paint."""
        if not self.colors:
            return

        skia_colors = [skia.Color(c.r, c.g, c.b, c.a) for c in self.colors]

        center_point = skia.Point(
            bounds.left() + self.center[0] * bounds.width(),
            bounds.top() + self.center[1] * bounds.height()
        )

        absolute_radius = self.radius * (bounds.width() + bounds.height()) / 2.0

        shader = skia.GradientShader.MakeRadial(
            center=center_point,
            radius=absolute_radius,
            colors=skia_colors,
            positions=self.stops if self.stops else []
        )
        paint.setShader(shader)
