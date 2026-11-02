from typing import Any

from typing_extensions import Unpack

from .._core.param import Param
from ._attributes import PlotAttributes, plot_attributes_mosaic


class PlotDefaults(PlotAttributes, total=False):
    """Default options for plots.

    Use the `plot_defaults()` function to set global defaults for plot options.
    """

    x_label: str | Param
    """A textual label to show on the axis or legend; if null, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.
    """

    fx_label: str | Param
    """
    A textual label to show on the axis or legend; if null, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.\n\nFor axes and legends only.
    """

    y_label: str | Param
    """A textual label to show on the axis or legend; if null, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.
    """

    fy_label: str | Param
    """
    A textual label to show on the axis or legend; if null, show no label. By default the scale label is inferred from channel definitions, possibly with an arrow (↑, →, ↓, or ←) to indicate the direction of increasing value.\n\nFor axes and legends only.
    """

    width: float | Param
    """The outer width of the plot in pixels, including margins. Defaults to 640.
    """

    height: float | Param
    """The outer height of the plot in pixels, including margins. The default depends on the plot's scales, and the plot's width if an aspectRatio is specified. For example, if the *y* scale is linear and there is no *fy* scale, it might be 396.
    """


def plot_defaults(**defaults: Unpack[PlotDefaults]) -> None:
    """Set global plot defaults.

    Note that this function should be called once at the outset (subsequent calls to it do not reset the defaults).

    Args:
       **defaults: Keyword args from `PlotDefaults`
    """
    global _plot_defaults
    _plot_defaults = defaults


def plot_defaults_as_camel() -> dict[str, Any]:
    global _plot_defaults
    return plot_attributes_mosaic(_builtin_plot_defaults | _plot_defaults)


_builtin_plot_defaults = PlotDefaults(width=700, height=450)

_plot_defaults = PlotDefaults()
