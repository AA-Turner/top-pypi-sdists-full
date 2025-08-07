"""
This file contains useful schemas for page.extract.
Defined here so that they can be directly imported in generated main.py
"""

from pydantic import BaseModel


class FormVerification(BaseModel):
    # For LLM verification on filled form
    # It uses page.extract to output the following information, given expected_form_data, page snapshot, and screenshot
    form_match_expected: bool
    reason: str
