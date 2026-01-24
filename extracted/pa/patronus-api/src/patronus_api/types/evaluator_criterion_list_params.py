# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["EvaluatorCriterionListParams"]


class EvaluatorCriterionListParams(TypedDict, total=False):
    enabled: Optional[bool]

    evaluator_family: Optional[str]

    get_last_revision: bool

    is_patronus_managed: Optional[bool]

    limit: int

    name: Optional[str]

    offset: int

    public_id: Optional[str]

    revision: Optional[int]
