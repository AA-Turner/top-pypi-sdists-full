# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["PromptDeleteDefinitionsParams"]


class PromptDeleteDefinitionsParams(TypedDict, total=False):
    project_id: Optional[str]
    """Delete all prompt definitions for this project"""

    prompt_id: Optional[str]
    """Delete a specific prompt definition by ID"""
