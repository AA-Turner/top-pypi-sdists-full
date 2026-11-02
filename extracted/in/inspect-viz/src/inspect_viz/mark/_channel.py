from typing import Literal, Optional, Sequence, TypeAlias, TypedDict

from inspect_viz._core.types import Interval

from ..transform._transform import Transform

ChannelName: TypeAlias = Literal[
    "ariaLabel",
    "fill",
    "fillOpacity",
    "fontSize",
    "fx",
    "fy",
    "geometry",
    "height",
    "href",
    "length",
    "opacity",
    "path",
    "r",
    "rotate",
    "src",
    "stroke",
    "strokeOpacity",
    "strokeWidth",
    "symbol",
    "text",
    "title",
    "weight",
    "width",
    "x",
    "x1",
    "x2",
    "y",
    "y1",
    "y2",
    "z",
]
"""Known channel names."""


Channel: TypeAlias = (
    str | Transform | Sequence[int | float | bool | str] | int | float | bool | None
)
"""Data channel for visualization.

Data channels can be either:
  - a field name, to extract the corresponding value from the source data
  - a channel transform  (aggregation or SQL expression)
  - a sequence of values, typically of the same length as the source data
  - a constant number or boolean
  - None to represent no value.
"""


class ChannelWithScale(TypedDict):
    """Channel with label and scale to override the scale that would normally be associated with the channel."""

    value: Channel
    label: Optional[str]
    scale: Optional[
        (
            Literal[
                "x",
                "y",
                "fx",
                "fy",
                "r",
                "color",
                "opacity",
                "symbol",
                "length",
                "auto",
            ]
            | bool
        )
    ]


ChannelSpec: TypeAlias = Channel | ChannelWithScale
"""Data channel spec for visualization.

Data channel specs can be either:
  - a field name, to extract the corresponding value from the source data
  - a channel transform  (aggregation or SQL expression)
  - a sequence of values, typically of the same length as the source data
  - a constant number or boolean
  - None to represent no value.
  - a data channel with an associated scale to override the scale that would normally be associated with the channel.
"""


class ChannelWithInterval(TypedDict):
    """Channel with associated interval."""

    value: Channel
    interval: Interval


ChannelIntervalSpec: TypeAlias = ChannelSpec | ChannelWithInterval
"""In some contexts, when specifying a mark channel’s value, you can provide a
{value, interval} object to specify an associated interval."""


class ChannelWithOrder(TypedDict, total=False):
    """Channel with order option"""

    value: Channel
    """The channel value to use for ordering."""

    order: Literal["ascending", "descending"]
    """The order in which to sort the values. Defaults to "ascending"."""


class ChannelDomainValueSpec(TypedDict, total=False):
    """Channel domain value spec."""

    value: str | None
    """The value to use for sorting"""

    order: Literal["ascending", "descending"] | None
    """The order in which to sort the values. Defaults to "ascending"."""

    reduce: str | None
    """The reduction function to use for sorting. Defaults to None, which means no reduction is applied. See https://observablehq.com/plot/transforms/group#group-options for the list of named reducers """

    reverse: bool | None
    """Whether to reverse the order of the values. Defaults to False."""

    limit: float | None
    """The maximum number of values to include in the domain. Defaults to None, which means no limit is applied."""


class ChannelDomainSort(TypedDict, total=False):
    """Channel domain sort spec."""

    x: ChannelDomainValueSpec | str | None
    """Sorting specification for the x-axis."""

    y: ChannelDomainValueSpec | str | None
    """Sorting specification for the y-axis."""

    color: ChannelDomainValueSpec | str | None
    """Sorting specification for the color channel."""

    fx: ChannelDomainValueSpec | str | None
    """Sorting specification for the fx channel."""

    fy: ChannelDomainValueSpec | str | None
    """Sorting specification for the fy channel."""

    r: ChannelDomainValueSpec | str | None
    """Sorting specification for the r channel."""

    length: ChannelDomainValueSpec | str | None
    """Sorting specification for the length channel."""

    opacity: ChannelDomainValueSpec | str | None
    """Sorting specification for the opacity channel."""

    symbol: ChannelDomainValueSpec | str | None
    """Sorting specification for the symbol channel."""

    reverse: bool | None
    """Whether to reverse the order of the values. Defaults to False."""


SortOrder: TypeAlias = Channel | ChannelWithOrder | ChannelDomainSort
"""Sort order for a plot mark's index.

  - a channel value definition for sorting given values (ascending)
  - a {value, order} object for sorting given values
"""
