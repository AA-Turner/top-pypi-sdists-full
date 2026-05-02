# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from .._utils import PropertyInfo
from .form_question import FormQuestion
from .number_question import NumberQuestion
from .rating_question import RatingQuestion
from .free_text_question import FreeTextQuestion
from .timestamp_question import TimestampQuestion
from .categorical_question import CategoricalQuestion

__all__ = ["Question"]

Question: TypeAlias = Annotated[
    Union[CategoricalQuestion, RatingQuestion, NumberQuestion, FreeTextQuestion, FormQuestion, TimestampQuestion],
    PropertyInfo(discriminator="question_type"),
]
