# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["PromptListDefinitionsParams"]


class PromptListDefinitionsParams(TypedDict, total=False):
    limit: int
    """Maximum number of records to return"""

    name: Optional[str]
    """Filter by exact prompt definition name"""

    name_startswith: Optional[str]
    """Filter by prompt definition name prefix"""

    offset: int
    """Number of records to skip"""

    project_id: Optional[str]
    """Filter by project ID"""

    project_name: Optional[str]
    """Filter by project name"""

    prompt_id: Optional[str]
    """Filter by specific prompt definition ID"""
