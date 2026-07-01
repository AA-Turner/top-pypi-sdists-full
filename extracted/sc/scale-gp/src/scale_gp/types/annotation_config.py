# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["AnnotationConfig", "Component", "LlmPrompt", "LlmPromptVariable"]


class Component(BaseModel):
    data_loc: List[str]

    label: Optional[str] = None

    optional: Optional[bool] = None


class LlmPromptVariable(BaseModel):
    data_loc: List[str]

    name: str

    optional: Optional[bool] = None


class LlmPrompt(BaseModel):
    template: str

    variables: List[LlmPromptVariable]


class AnnotationConfig(BaseModel):
    annotation_config_type: Optional[Literal["generation", "flexible", "summarization", "multiturn", "translation"]] = (
        None
    )

    components: Optional[List[List[Component]]] = None

    direction: Optional[Literal["col", "row"]] = None

    llm_prompt: Optional[LlmPrompt] = None
