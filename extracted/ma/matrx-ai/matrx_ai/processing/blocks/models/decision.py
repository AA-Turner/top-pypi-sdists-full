"""Decision block data models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class DecisionOption(BaseModel):
    """A single selectable option within a decision block."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: str
    label: str
    text: str


class DecisionBlockData(BaseModel):
    """
    Parsed data for an inline decision block.

    Mirrors the TypeScript InlineDecision interface exactly:
        { id, prompt, options: InlineDecisionOption[] }

    The frontend uses this to render option pills. When the user picks one,
    the raw XML is replaced with the chosen option's prose text.
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: str
    prompt: str
    options: list[DecisionOption]
