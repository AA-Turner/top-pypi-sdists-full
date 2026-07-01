# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel
from .evaluation_dataset_generation_job import EvaluationDatasetGenerationJob

__all__ = ["EvaluationDatasetGenerationJobsList"]


class EvaluationDatasetGenerationJobsList(BaseModel):
    generation_jobs: List[EvaluationDatasetGenerationJob]
    """List of evaluation dataset generation jobs."""
