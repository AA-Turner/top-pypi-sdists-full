# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["EvaluationMetrics"]


class EvaluationMetrics(BaseModel):
    avg_labeling_time_per_test_case: float
    """Average time spent labeling per test case in seconds."""

    avg_num_test_cases_labeled_per_day: float
    """Average number of test cases labeled per day."""

    evaluation_id: str
    """The ID of the evaluation."""

    num_test_cases_approved: int
    """Number of test cases approved."""

    num_test_cases_fixed: int
    """Number of test cases fixed."""

    num_test_cases_flagged: int
    """Number of test cases flagged."""

    num_test_cases_labeled: int
    """Number of test cases labeled."""

    num_test_cases_unaudited: int
    """Number of test cases unaudited."""

    num_total_test_cases: int
    """Total number of test cases."""

    percentage_test_cases_approved: float
    """Percentage of test cases that were approved."""

    percentage_test_cases_fixed: float
    """Percentage of test cases that were fixed."""

    percentage_test_cases_unaudited: float
    """Percentage of test cases that were unaudited."""
