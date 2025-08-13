"""
This file contains useful schemas for page.extract.
Defined here so that they can be directly imported in generated main.py
"""

from typing import List
from pydantic import BaseModel, Field


class FormVerification(BaseModel):
    """
    For LLM verification on filled form.
    """

    reason: str = Field(description="The reason for the verification result.")
    # Added this field to help the LLM reason about the verification result.
    non_matching_fields: List[str] = Field(
        description="The fields in the snapshot that do not match the expected form data values after normalization."
    )
    form_match_expected: bool = Field(
        description="Whether the form values match the expected form data values after normalization. Must be consistent with the reason."
    )
