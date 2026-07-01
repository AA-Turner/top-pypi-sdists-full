# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["EvaluationDatasetGenerationJob"]


class EvaluationDatasetGenerationJob(BaseModel):
    created_at: datetime
    """The timestamp at which the upload job started."""

    generation_job_id: str
    """ID of the async job associated with this evaluation dataset generation"""

    status: Literal["Pending", "Running", "Completed", "Failed", "Canceled"]
    """Status of the async job"""

    updated_at: datetime
    """The timestamp at which the upload job was last updated."""

    failure_reason: Optional[str] = None
    """Reason for the job's failure, if applicable"""

    num_completed_test_cases: Optional[int] = None
    """Number of test cases that have been generated"""

    num_test_cases: Optional[int] = None
    """Optional number of test cases input to the job"""

    total_chunk_count: Optional[int] = None
    """Number of chunks in the knowledge base"""
