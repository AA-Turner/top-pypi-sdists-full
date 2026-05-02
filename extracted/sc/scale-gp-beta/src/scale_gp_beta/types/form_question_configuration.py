# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict

from .._models import BaseModel

__all__ = ["FormQuestionConfiguration"]


class FormQuestionConfiguration(BaseModel):
    form_schema: Dict[str, object]
    """The JSON schema of the desired form object"""
