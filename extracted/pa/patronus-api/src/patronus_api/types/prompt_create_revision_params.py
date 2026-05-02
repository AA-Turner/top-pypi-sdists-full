# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["PromptCreateRevisionParams"]


class PromptCreateRevisionParams(TypedDict, total=False):
    body: Required[str]

    create_only_if_not_exists: bool
    """
    If true, creation will fail if a prompt with the same name already exists in the
    project. Only applies when creating a new prompt (not providing prompt_id).
    """

    metadata: Optional[object]
    """Optional JSON metadata to associate with this revision"""

    project_id: Optional[str]

    project_name: Optional[str]

    prompt_description: Optional[str]

    prompt_id: Optional[str]

    prompt_name: Optional[str]
