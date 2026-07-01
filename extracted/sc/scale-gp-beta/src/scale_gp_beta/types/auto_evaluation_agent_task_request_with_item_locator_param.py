# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .._types import SequenceNotStr

__all__ = [
    "AutoEvaluationAgentTaskRequestWithItemLocatorParam",
    "DesignatedTo",
    "DesignatedToApeAgent",
    "DesignatedToApeAgentConfig",
    "DesignatedToIfAgent",
    "DesignatedToIfAgentConfig",
    "DesignatedToTruthfulnessAgent",
    "DesignatedToTruthfulnessAgentConfig",
    "DesignatedToBaseAgent",
    "DesignatedToBaseAgentConfig",
]


class DesignatedToApeAgentConfig(TypedDict, total=False):
    model: str

    temperature: float


class DesignatedToApeAgent(TypedDict, total=False):
    config: Required[DesignatedToApeAgentConfig]

    agent_name: Literal["APEAgent"]


class DesignatedToIfAgentConfig(TypedDict, total=False):
    model: str


class DesignatedToIfAgent(TypedDict, total=False):
    config: Required[DesignatedToIfAgentConfig]

    agent_name: Literal["IFAgent"]


class DesignatedToTruthfulnessAgentConfig(TypedDict, total=False):
    model: str


class DesignatedToTruthfulnessAgent(TypedDict, total=False):
    config: Required[DesignatedToTruthfulnessAgentConfig]

    agent_name: Literal["TruthfulnessAgent"]


class DesignatedToBaseAgentConfig(TypedDict, total=False):
    model: str


class DesignatedToBaseAgent(TypedDict, total=False):
    config: Required[DesignatedToBaseAgentConfig]

    agent_name: Literal["BaseAgent"]


DesignatedTo: TypeAlias = Union[
    DesignatedToApeAgent, DesignatedToIfAgent, DesignatedToTruthfulnessAgent, DesignatedToBaseAgent
]


class AutoEvaluationAgentTaskRequestWithItemLocatorParam(TypedDict, total=False):
    definition: Required[str]

    name: Required[str]

    output_rules: Required[SequenceNotStr[str]]

    data_fields: SequenceNotStr[str]

    designated_to: DesignatedTo

    output_type: Literal["text", "integer", "float", "boolean"]

    output_values: SequenceNotStr[Union[str, float, bool]]

    rubric_id: str

    rubric_version: int
