# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["ExperimentCreateParams"]


class ExperimentCreateParams(TypedDict, total=False):
    name: Required[str]

    project_id: Required[str]

    metadata: Optional[object]

    tags: object
    """Tags are key-value pairs used to label resources"""
