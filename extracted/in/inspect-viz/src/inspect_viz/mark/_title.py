from typing import Any, cast

from ._mark import Mark
from ._text import text_styles_config
from ._types import TextStyles


class Title(Mark):
    """Plot title mark."""

    def __init__(self, title: str, margin_top: int, styles: TextStyles) -> None:
        config: dict[str, Any] = dict(
            text=[title],
            dy=-margin_top,
            frameAnchor="top",
        ) | text_styles_config(styles)

        super().__init__("text", config, {"facet": "super"})

    @property
    def margin_top(self) -> int:
        return -(cast(int, self.config.get("dy", 0)))

    @margin_top.setter
    def margin_top(self, margin_top: int) -> None:
        self.config["dy"] = -margin_top


def title(
    title: str,
    margin_top: int = 15,
    font_size: float | None = 16,
    font_family: str | None = None,
    font_weight: float | None = None,
) -> Title:
    """Create a plot title mark.

    Adds a title at the top of the plot frame.

    Args:
       title: Title text.
       margin_top: Top margin fot title (defaults to 10 pixels). You may need to increase this if there are facet labels on the x-axis that the title needs to be placed above.
       font_size: The font size in pixels (defaults to 14)
       font_family: The font-family (defaults to the plot's font family, which is typically *system-ui*")
       font_weight: The font weight (defaults to the plot's font weight, which is typically 400."
    """
    # create styles
    styles = TextStyles()
    if font_size is not None:
        styles["font_size"] = font_size
    if font_family is not None:
        styles["font_family"] = font_family
    if font_weight is not None:
        styles["font_weight"] = font_weight

    # create mark
    return Title(
        title=title,
        margin_top=margin_top,
        styles=styles,
    )
