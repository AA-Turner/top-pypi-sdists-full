# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["RuleUpdateResponse", "Rule", "RuleActionParameters"]


class RuleActionParameters(BaseModel):
    sampling_ratio: float
    """The ratio of requests sampled for tracing, from 0 to 1."""


class Rule(BaseModel):
    action: Literal["set_trace_settings"]

    action_parameters: RuleActionParameters

    description: str

    enabled: bool

    expression: str
    """A Rules language expression that selects requests."""


class RuleUpdateResponse(BaseModel):
    rules: List[Rule]
    """Trace rules in evaluation order."""
