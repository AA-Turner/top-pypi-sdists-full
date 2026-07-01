# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .form_question_configuration_param import FormQuestionConfigurationParam
from .number_question_configuration_param import NumberQuestionConfigurationParam
from .rating_question_configuration_param import RatingQuestionConfigurationParam
from .free_text_question_configuration_param import FreeTextQuestionConfigurationParam
from .timestamp_question_configuration_param import TimestampQuestionConfigurationParam
from .categorical_question_configuration_param import CategoricalQuestionConfigurationParam

__all__ = [
    "QuestionCreateParams",
    "Question",
    "QuestionCategoricalQuestionRequest",
    "QuestionRatingQuestionRequest",
    "QuestionNumberQuestionRequest",
    "QuestionFreeTextQuestionRequest",
    "QuestionFormQuestionRequest",
    "QuestionTimestampQuestionRequest",
]


class QuestionCreateParams(TypedDict, total=False):
    question: Required[Question]


class QuestionCategoricalQuestionRequest(TypedDict, total=False):
    configuration: Required[CategoricalQuestionConfigurationParam]

    name: Required[str]

    prompt: Required[str]
    """user-facing question prompt"""

    conditions: Iterable[Dict[str, object]]
    """Conditions for the question to be shown"""

    question_type: Literal["categorical"]


class QuestionRatingQuestionRequest(TypedDict, total=False):
    configuration: Required[RatingQuestionConfigurationParam]

    name: Required[str]

    prompt: Required[str]
    """user-facing question prompt"""

    conditions: Iterable[Dict[str, object]]
    """Conditions for the question to be shown"""

    question_type: Literal["rating"]


class QuestionNumberQuestionRequest(TypedDict, total=False):
    name: Required[str]

    prompt: Required[str]
    """user-facing question prompt"""

    conditions: Iterable[Dict[str, object]]
    """Conditions for the question to be shown"""

    configuration: NumberQuestionConfigurationParam

    question_type: Literal["number"]


class QuestionFreeTextQuestionRequest(TypedDict, total=False):
    name: Required[str]

    prompt: Required[str]
    """user-facing question prompt"""

    conditions: Iterable[Dict[str, object]]
    """Conditions for the question to be shown"""

    configuration: FreeTextQuestionConfigurationParam

    question_type: Literal["free_text"]


class QuestionFormQuestionRequest(TypedDict, total=False):
    configuration: Required[FormQuestionConfigurationParam]

    name: Required[str]

    prompt: Required[str]
    """user-facing question prompt"""

    conditions: Iterable[Dict[str, object]]
    """Conditions for the question to be shown"""

    question_type: Literal["form"]


class QuestionTimestampQuestionRequest(TypedDict, total=False):
    name: Required[str]

    prompt: Required[str]
    """user-facing question prompt"""

    conditions: Iterable[Dict[str, object]]
    """Conditions for the question to be shown"""

    configuration: TimestampQuestionConfigurationParam

    question_type: Literal["timestamp"]


Question: TypeAlias = Union[
    QuestionCategoricalQuestionRequest,
    QuestionRatingQuestionRequest,
    QuestionNumberQuestionRequest,
    QuestionFreeTextQuestionRequest,
    QuestionFormQuestionRequest,
    QuestionTimestampQuestionRequest,
]
