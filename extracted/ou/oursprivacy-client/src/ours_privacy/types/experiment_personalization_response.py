# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ExperimentPersonalizationResponse", "Personalization"]


class Personalization(BaseModel):
    assigned_at: float

    experiment_id: str

    variant_id: str

    experiment_key: Optional[str] = None

    experiment_name: Optional[str] = None

    variant_name: Optional[str] = None


class ExperimentPersonalizationResponse(BaseModel):
    properties: Dict[str, Union[str, float, bool, int, None]]
    """
    The visitor traits accumulated by your personalization property rules, keyed by
    property key. Values are always scalars — a string, number, or boolean, or null
    when the captured field was itself empty. Empty for a visitor who has not
    matched any rule yet. These same values are delivered to the visitor's browser
    and are readable by anyone who knows the visitor_id, so never accumulate
    secrets, credentials, PHI, or confidential data into a property.
    """

    success: Literal[True]

    personalizations: Optional[List[Personalization]] = None
    """Deprecated legacy personalization assignments.

    Current API responses omit this field; use properties for accumulated
    personalization traits. Retained in the SDK for callers using older responses.
    """
