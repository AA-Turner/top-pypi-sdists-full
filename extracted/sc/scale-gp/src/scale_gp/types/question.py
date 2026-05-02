# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .shared.categorical_choice import CategoricalChoice

__all__ = ["Question", "FreeTextOptions", "FreeTextOptionsCharacterLimit", "NumberOptions", "RatingOptions"]


class FreeTextOptionsCharacterLimit(BaseModel):
    max: Optional[int] = None
    """Maximum number of characters"""

    min: Optional[int] = None
    """Minimum number of characters"""


class FreeTextOptions(BaseModel):
    """Options for free text questions."""

    character_limit: FreeTextOptionsCharacterLimit = FieldInfo(alias="characterLimit")


class NumberOptions(BaseModel):
    """Options for number questions."""

    max: Optional[float] = None
    """Maximum value for the number"""

    min: Optional[float] = None
    """Minimum value for the number"""


class RatingOptions(BaseModel):
    """Options for rating questions."""

    max_label: str = FieldInfo(alias="maxLabel")
    """Maximum value for the rating"""

    min_label: str = FieldInfo(alias="minLabel")
    """Minimum value for the rating"""

    scale_steps: int = FieldInfo(alias="scaleSteps")
    """Number of steps in the rating scale"""


class Question(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_identity_type: Literal["user", "service_account"]
    """The type of identity that created the entity."""

    created_by_user_id: str
    """The user who originally created the entity."""

    prompt: str

    title: str

    type: Literal["categorical", "free_text", "rating", "number", "form", "timestamp"]
    """The type of question"""

    choices: Optional[List[CategoricalChoice]] = None
    """List of choices for the question. Required for CATEGORICAL questions."""

    conditions: Optional[List[Dict[str, object]]] = None
    """Conditions for the question to be shown."""

    default: Optional[object] = None
    """The default value for the question."""

    dropdown: Optional[bool] = None
    """Whether the question is displayed as a dropdown in the UI."""

    form_schema: Optional[Dict[str, object]] = None
    """The schema for the question."""

    free_text_options: Optional[FreeTextOptions] = FieldInfo(alias="freeTextOptions", default=None)
    """Options for free text questions."""

    multi: Optional[bool] = None
    """Whether the question allows multiple answers."""

    number_options: Optional[NumberOptions] = FieldInfo(alias="numberOptions", default=None)
    """Options for number questions."""

    rating_options: Optional[RatingOptions] = FieldInfo(alias="ratingOptions", default=None)
    """Options for rating questions."""

    required: Optional[bool] = None
    """
    [To be deprecated in favor of question set question_id_to_config] Whether the
    question is required.
    """
