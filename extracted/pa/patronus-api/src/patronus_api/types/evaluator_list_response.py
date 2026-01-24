# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["EvaluatorListResponse", "Evaluator"]


class Evaluator(BaseModel):
    id: str

    aliases: List[str]

    description: Optional[str] = None

    evaluation_enabled: bool
    """Whether the evaluator is available for LLM Monitoring."""

    evaluation_run_enabled: bool
    """Whether the evaluator is available for Evaluation Runs."""

    evaluator_family: Optional[str] = None

    image_url: Optional[str] = None

    name: Optional[str] = None

    profile_required: bool
    """Whether a profile is required by the evaluator.

    Learn more about profiles [here](https://docs.patronus.ai/docs/profiles).
    """

    default_criteria: Optional[str] = None


class EvaluatorListResponse(BaseModel):
    evaluators: List[Evaluator]
