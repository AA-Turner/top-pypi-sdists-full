# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = ["RuleUpdateParams", "Rule", "RuleActionParameters"]


class RuleUpdateParams(TypedDict, total=False):
    zone_id: Required[str]
    """Specify the zone ID."""

    rules: Required[Iterable[Rule]]
    """Trace rules in evaluation order."""


class RuleActionParameters(TypedDict, total=False):
    sampling_ratio: Required[float]
    """The ratio of requests sampled for tracing, from 0 to 1."""


class Rule(TypedDict, total=False):
    action: Required[Literal["set_trace_settings"]]

    action_parameters: Required[RuleActionParameters]

    description: Required[str]

    enabled: Required[bool]

    expression: Required[str]
    """A Rules language expression that selects requests."""
