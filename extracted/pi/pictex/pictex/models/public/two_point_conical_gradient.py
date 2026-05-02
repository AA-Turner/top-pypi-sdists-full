from dataclasses import dataclass
from typing import Sequence, Optional
import skia
from .paint_source import PaintSource
from .color import SolidColor

@dataclass
class TwoPointConicalGradient(PaintSource):
    """
    Represents a two-point conical gradient fill, smoothly transitioning between
    colors from one circle to another circle.

    This gradient creates a cone-like transition between two circles defined by
    their center points and radii. The gradient interpolates colors from the
    start circle to the end circle, creating sophisticated radial effects.

    Attributes:
        colors (Sequence[Color]): A sequence of two or more Color objects
            that define the key colors of the gradient.
        stops (Optional[Sequence[float]]): A sequence of numbers between 0.0
            and 1.0 that specify the position of each color in the `colors`
            sequence. The length of `stops` must match the length of `colors`.
            If `None`, the colors are distributed evenly from start to end circle.
            For example, for `colors` with 3 colors, `stops=[0.0, 0.5, 1.0]`
            would place the second color exactly halfway between the circles.
        start (tuple[float, float]): A tuple `(x, y)` representing the
            center point of the start circle. Coordinates are relative to the
            object's bounding box, where (0.0, 0.0) is the top-left corner and
            (1.0, 1.0) is the bottom-right corner. Defaults to (0.5, 0.5).
        start_radius (float): The radius of the start circle, relative to the
            object's dimensions. Must be non-negative. Defaults to 0.0.
        end (tuple[float, float]): A tuple `(x, y)` representing the
            center point of the end circle. Coordinates are relative to the
            object's bounding box. Defaults to (0.5, 0.5).
        end_radius (float): The radius of the end circle, relative to the
            object's dimensions. Must be non-negative. Defaults to 0.5.

    Example:
        # A simple conical gradient from center to edge
        ```python
        conical_gradient = TwoPointConicalGradient(
            colors=['yellow', 'orange', 'red']
        )
        ```

        # A spotlight effect with offset circles
        ```python
        spotlight = TwoPointConicalGradient(
            colors=['white', 'black'],
            start=(0.3, 0.3),
            start_radius=0.0,
            end=(0.5, 0.5),
            end_radius=0.7
        )
        ```

        # A custom conical gradient with multiple stops
        ```python
        custom_conical = TwoPointConicalGradient(
            colors=['cyan', 'blue', 'purple', 'magenta'],
            stops=[0.0, 0.3, 0.7, 1.0],
            start=(0.5, 0.5),
            start_radius=0.1,
            end=(0.5, 0.5),
            end_radius=0.8
        )
        ```

    Note:
        For the gradient to render correctly, the **start circle should be fully
        contained within the end circle**. If they only partially overlap or do
        not overlap at all, the area outside the gradient region may appear
        transparent or unexpectedly dark - this behavior follows Skia's
        conical gradient implementation.
    """
    colors: Sequence[SolidColor]
    stops: Optional[Sequence[float]] = None
    start: tuple[float, float] = (0.5, 0.5)
    start_radius: float = 0.0
    end: tuple[float, float] = (0.5, 0.5)
    end_radius: float = 0.5

    def __post_init__(self):
        self.colors = [
            SolidColor.from_str(c) if isinstance(c, str) else c
            for c in self.colors
        ]
        if not all(isinstance(c, SolidColor) for c in self.colors):
             raise TypeError("All items in 'colors' must be Color objects or valid color strings.")

        if len(self.colors) < 2:
            raise ValueError("At least 2 colors are required for a gradient.")

        if len(self.start) != 2:
            raise ValueError("start must be a tuple of 2 values (x, y).")
        if not all(0.0 <= v <= 1.0 for v in self.start):
            raise ValueError("start values must be between 0.0 and 1.0.")

        if len(self.end) != 2:
            raise ValueError("end must be a tuple of 2 values (x, y).")
        if not all(0.0 <= v <= 1.0 for v in self.end):
            raise ValueError("end values must be between 0.0 and 1.0.")

        if self.start_radius < 0 or self.start_radius > 1.0:
            raise ValueError("start_radius must be between 0.0 and 1.0.")

        if self.end_radius < 0 or self.end_radius > 1.0:
            raise ValueError("end_radius must be between 0.0 and 1.0.")

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
        """Creates a two-point conical gradient shader and applies it to the paint."""
        if not self.colors:
            return

        skia_colors = [skia.Color(c.r, c.g, c.b, c.a) for c in self.colors]

        start_point = skia.Point(
            bounds.left() + self.start[0] * bounds.width(),
            bounds.top() + self.start[1] * bounds.height()
        )

        end_point = skia.Point(
            bounds.left() + self.end[0] * bounds.width(),
            bounds.top() + self.end[1] * bounds.height()
        )

        absolute_start_radius = self.start_radius * (bounds.width() + bounds.height()) / 2.0
        absolute_end_radius = self.end_radius * (bounds.width() + bounds.height()) / 2.0

        shader = skia.GradientShader.MakeTwoPointConical(
            start=start_point,
            startRadius=absolute_start_radius,
            end=end_point,
            endRadius=absolute_end_radius,
            colors=skia_colors,
            positions=self.stops if self.stops else []
        )
        paint.setShader(shader)
