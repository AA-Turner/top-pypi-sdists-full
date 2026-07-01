# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["TranslationAnnotationConfigParam", "LlmPrompt", "LlmPromptVariable"]


class LlmPromptVariable(TypedDict, total=False):
    data_loc: Required[SequenceNotStr[str]]

    name: Required[str]

    optional: bool


class LlmPrompt(TypedDict, total=False):
    template: Required[str]

    variables: Required[Iterable[LlmPromptVariable]]


class TranslationAnnotationConfigParam(TypedDict, total=False):
    original_text_loc: Required[SequenceNotStr[str]]

    translation_loc: Required[SequenceNotStr[str]]

    expected_translation_loc: SequenceNotStr[str]

    language_loc: SequenceNotStr[str]

    llm_prompt: LlmPrompt
