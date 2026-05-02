# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["AnnotationConfigParam", "Component", "LlmPrompt", "LlmPromptVariable"]


class Component(TypedDict, total=False):
    data_loc: Required[SequenceNotStr[str]]

    label: str

    optional: bool


class LlmPromptVariable(TypedDict, total=False):
    data_loc: Required[SequenceNotStr[str]]

    name: Required[str]

    optional: bool


class LlmPrompt(TypedDict, total=False):
    template: Required[str]

    variables: Required[Iterable[LlmPromptVariable]]


class AnnotationConfigParam(TypedDict, total=False):
    annotation_config_type: Literal["generation", "flexible", "summarization", "multiturn", "translation"]

    components: Iterable[Iterable[Component]]

    direction: Literal["col", "row"]

    llm_prompt: LlmPrompt
