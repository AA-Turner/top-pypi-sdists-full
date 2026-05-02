# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["TaskUpdateParams"]


class TaskUpdateParams(TypedDict, total=False):
    evaluation_id: Required[str]

    assigned_to: str
    """The ID of the user that the task is assigned to."""
