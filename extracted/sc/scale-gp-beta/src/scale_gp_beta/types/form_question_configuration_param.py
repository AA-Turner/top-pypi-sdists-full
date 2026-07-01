# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, TypedDict

__all__ = ["FormQuestionConfigurationParam"]


class FormQuestionConfigurationParam(TypedDict, total=False):
    form_schema: Required[Dict[str, object]]
    """The JSON schema of the desired form object"""
