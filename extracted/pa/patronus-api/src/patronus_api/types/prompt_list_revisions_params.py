# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["PromptListRevisionsParams"]


class PromptListRevisionsParams(TypedDict, total=False):
    label: Optional[str]
    """Filter by revisions that have this label"""

    latest_revision_only: bool
    """Only return the latest revision for each prompt"""

    limit: int
    """Maximum number of records to return"""

    normalized_body_sha256: Optional[str]
    """
    Filter by SHA-256 hash prefix of prompt body with whitespace stripped from start
    and end
    """

    offset: int
    """Number of records to skip"""

    project_id: Optional[str]
    """Filter by project ID"""

    project_name: Optional[str]
    """Filter by project name"""

    prompt_id: Optional[str]
    """Filter by prompt definition ID"""

    prompt_name: Optional[str]
    """Filter by prompt definition name"""

    prompt_name_startswith: Optional[str]
    """Filter by prompt definition name prefix"""

    revision: Optional[int]
    """Filter by revision number"""

    revision_id: Optional[str]
    """Filter by specific revision ID"""
