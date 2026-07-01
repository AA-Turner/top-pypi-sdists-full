# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["FreeTextQuestionConfigurationParam"]


class FreeTextQuestionConfigurationParam(TypedDict, total=False):
    max_length: int
    """Maximum characters allowed"""

    min_length: int
    """Minimum characters required"""
