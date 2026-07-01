# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, TypedDict

__all__ = ["TaggingInformationAll"]


class TaggingInformationAll(TypedDict, total=False):
    tags_to_apply: Dict[str, object]

    type: Literal["all"]
