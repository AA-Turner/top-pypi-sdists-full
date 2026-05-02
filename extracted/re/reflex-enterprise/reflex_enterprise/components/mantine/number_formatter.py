"""NumberFormatter component for formatting numbers in a user-friendly way."""

from typing import Literal

import reflex as rx

from reflex_enterprise.components.mantine.base import MantineCoreBase


class NumberFormatter(MantineCoreBase):
    """Formats number input/output."""

    tag = "NumberFormatter"

    # If true, negative numbers are allowed.
    allow_negative: rx.Var[bool]

    # Limits the number of digits after the decimal separator.
    decimal_scale: rx.Var[int]

    # Character used as decimal separator.
    decimal_separator: rx.Var[str]

    # If true, the number will be padded with zeros to match the decimal scale.
    fixed_decimal_scale: rx.Var[bool]

    # Adds prefix to the formatted value, eg. '$ '.
    prefix: rx.Var[str]

    # Adds suffix to the formatted value, eg. ' %'.
    suffix: rx.Var[str]

    # Character used as thousand separator. Set to true to automatically determine the separator based on the user's locale.
    thousand_separator: rx.Var[str | bool]

    # Defines the thousand grouping style.
    thousands_group_style: rx.Var[Literal["none", "thousand", "lakh", "wan"]]

    # The value to be formatted.
    value: rx.Var[str | int | float]


number_formatter = NumberFormatter.create
