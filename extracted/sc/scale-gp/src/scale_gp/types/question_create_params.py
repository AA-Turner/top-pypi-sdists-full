# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo
from .shared_params.categorical_choice import CategoricalChoice

__all__ = ["QuestionCreateParams", "FreeTextOptions", "FreeTextOptionsCharacterLimit", "NumberOptions", "RatingOptions"]


class QuestionCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    prompt: Required[str]

    title: Required[str]

    type: Required[Literal["categorical", "free_text", "rating", "number", "form", "timestamp"]]
    """The type of question"""

    allow_multi_timestamps: Annotated[bool, PropertyInfo(alias="allowMultiTimestamps")]
    """Whether to allow multiple media timestamps for timestamp questions."""

    choices: Iterable[CategoricalChoice]
    """List of choices for the question. Required for CATEGORICAL questions."""

    conditions: Iterable[Dict[str, object]]
    """Conditions for the question to be shown."""

    default: object
    """The default value for the question."""

    dropdown: bool
    """Whether the question is displayed as a dropdown in the UI."""

    form_schema: Dict[str, object]
    """The schema for the question."""

    free_text_options: Annotated[FreeTextOptions, PropertyInfo(alias="freeTextOptions")]
    """Options for free text questions."""

    multi: bool
    """Whether the question allows multiple answers.

    For categorical questions, this enables multi-select. For timestamp questions,
    this allows multiple timestamps.
    """

    number_options: Annotated[NumberOptions, PropertyInfo(alias="numberOptions")]
    """Options for number questions."""

    rating_options: Annotated[RatingOptions, PropertyInfo(alias="ratingOptions")]
    """Options for rating questions."""

    required: bool
    """
    [To be deprecated in favor of question set question_id_to_config] Whether the
    question is required.
    """


class FreeTextOptionsCharacterLimit(TypedDict, total=False):
    max: int
    """Maximum number of characters"""

    min: int
    """Minimum number of characters"""


class FreeTextOptions(TypedDict, total=False):
    """Options for free text questions."""

    character_limit: Required[Annotated[FreeTextOptionsCharacterLimit, PropertyInfo(alias="characterLimit")]]


class NumberOptions(TypedDict, total=False):
    """Options for number questions."""

    max: float
    """Maximum value for the number"""

    min: float
    """Minimum value for the number"""


class RatingOptions(TypedDict, total=False):
    """Options for rating questions."""

    max_label: Required[Annotated[str, PropertyInfo(alias="maxLabel")]]
    """Maximum value for the rating"""

    min_label: Required[Annotated[str, PropertyInfo(alias="minLabel")]]
    """Minimum value for the rating"""

    scale_steps: Required[Annotated[int, PropertyInfo(alias="scaleSteps")]]
    """Number of steps in the rating scale"""
