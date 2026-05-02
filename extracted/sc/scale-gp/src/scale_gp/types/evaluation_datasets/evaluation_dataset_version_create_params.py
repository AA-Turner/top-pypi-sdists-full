# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["EvaluationDatasetVersionCreateParams"]


class EvaluationDatasetVersionCreateParams(TypedDict, total=False):
    account_id: str
    """The ID of the account that owns the given entity."""

    draft: bool
    """Boolean to check whether or not the evaluation dataset is in draft mode"""

    published_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
    """
    The date and time that all test case results for the evaluation were completed
    for the evaluation in ISO format.
    """
