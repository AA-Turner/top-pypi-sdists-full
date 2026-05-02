# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel

__all__ = [
    "AutoEvaluationAgentTaskRequestWithItemLocator",
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


class DesignatedToApeAgentConfig(BaseModel):
    model: Optional[str] = None

    temperature: Optional[float] = None


class DesignatedToApeAgent(BaseModel):
    config: DesignatedToApeAgentConfig

    agent_name: Optional[Literal["APEAgent"]] = None


class DesignatedToIfAgentConfig(BaseModel):
    model: Optional[str] = None


class DesignatedToIfAgent(BaseModel):
    config: DesignatedToIfAgentConfig

    agent_name: Optional[Literal["IFAgent"]] = None


class DesignatedToTruthfulnessAgentConfig(BaseModel):
    model: Optional[str] = None


class DesignatedToTruthfulnessAgent(BaseModel):
    config: DesignatedToTruthfulnessAgentConfig

    agent_name: Optional[Literal["TruthfulnessAgent"]] = None


class DesignatedToBaseAgentConfig(BaseModel):
    model: Optional[str] = None


class DesignatedToBaseAgent(BaseModel):
    config: DesignatedToBaseAgentConfig

    agent_name: Optional[Literal["BaseAgent"]] = None


DesignatedTo: TypeAlias = Union[
    DesignatedToApeAgent, DesignatedToIfAgent, DesignatedToTruthfulnessAgent, DesignatedToBaseAgent
]


class AutoEvaluationAgentTaskRequestWithItemLocator(BaseModel):
    definition: str

    name: str

    output_rules: List[str]

    data_fields: Optional[List[str]] = None

    designated_to: Optional[DesignatedTo] = None

    output_type: Optional[Literal["text", "integer", "float", "boolean"]] = None

    output_values: Optional[List[Union[str, float, bool]]] = None

    rubric_id: Optional[str] = None

    rubric_version: Optional[int] = None
