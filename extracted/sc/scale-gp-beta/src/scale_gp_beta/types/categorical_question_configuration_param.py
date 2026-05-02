# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["CategoricalQuestionConfigurationParam"]


class CategoricalQuestionConfigurationParam(TypedDict, total=False):
    choices: Required[SequenceNotStr[str]]
    """Categorical answer choices (must contain at least one entry)"""

    dropdown: bool
    """Whether the question is displayed as a dropdown in the UI."""

    multi: bool
    """Whether the question allows multiple answers."""
