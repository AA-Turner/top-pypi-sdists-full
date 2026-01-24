# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["EvaluatorListFamiliesResponse", "EvaluatorFamily"]


class EvaluatorFamily(BaseModel):
    family_name: str

    optional_input_fields: List[str]

    profile_config_schema: Optional[object] = None

    required_input_fields: List[str]


class EvaluatorListFamiliesResponse(BaseModel):
    evaluator_families: List[EvaluatorFamily]
