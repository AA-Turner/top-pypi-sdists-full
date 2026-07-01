# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["ContributorMetrics"]


class ContributorMetrics(BaseModel):
    annotated_by_user_id: str
    """The ID of the user who annotated the test case."""

    evaluation_id: str
    """The ID of the evaluation."""

    num_test_cases_fixed: int
    """Number of test cases that were fixed."""

    percentage_test_cases_fixed: float
    """Percentage of test cases done by this contributor that were fixed."""

    total_num_test_cases_labeled: int
    """Total number of test cases labeled."""

    avg_time_spent_labeling_sec: Optional[float] = None
    """Average time spent labeling per test case in seconds."""

    total_time_spent_labeling_sec: Optional[int] = None
    """Total time spent labeling in seconds."""
