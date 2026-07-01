# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, TypedDict

__all__ = ["TaskUpdateParams"]


class TaskUpdateParams(TypedDict, total=False):
    evaluation_id: Required[str]

    configuration: Required[Dict[str, object]]
    """Full replacement for the test criteria's configuration JSON.

    Only allowed when no contributor annotation tasks for this evaluation have been
    claimed or completed.
    """
