from typing import Generator

from colorfield.fields import ColorField
from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField


class ColorGradient(models.Model):
    """
    Utility class for color gradient support in report
    """

    title = models.CharField(max_length=128, default="")
    colors = ArrayField(ColorField(default="#FF0000"), default=list)

    def __str__(self) -> str:
        return self.title

    def get_gradient(self, color: str | None = None, color_size: int = -1) -> Generator:
        """
        Return the consecutive colors (gradient) given a color based on the closest distance

        Args:
            color: a hex color. Optional.
            color_size: The number of colors the list should return. Optional.

        Returns:
            A generator of colors bounds in size by the color_size parameters or the gradient defaults color palette size
        """

        def _hex2rgb(_color):
            _color = _color.replace("#", "")
            return tuple(int(_color[i : i + 2], 16) for i in (0, 2, 4))

        if color_size < 0:
            color_size = len(self.colors)

        index = 0
        if color:
            color_rgb = _hex2rgb(color)
            nearest_color = min(
                self.colors,
                key=lambda subject: sum((s - q) ** 2 for s, q in zip(_hex2rgb(subject), color_rgb, strict=False)),
            )

            index = self.colors.index(nearest_color)
        for i in range(color_size):
            yield self.colors[(index + i) % len(self.colors)]


class TransparencyMixin:
    def get_cell_formatting(self, request):
        return [
            {
                "column": None,
                "conditions": [
                    {
                        "condition": None,
                        "style": {"backgroundColor": f'rgba(255, 255, 255, {getattr(self, "TRANSPARENCY", 0.4)})'},
                    },
                ],
            }
        ]
