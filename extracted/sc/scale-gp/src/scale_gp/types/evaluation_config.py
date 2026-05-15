# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .shared.auto_evaluation_parameters import AutoEvaluationParameters

__all__ = ["EvaluationConfig"]


class EvaluationConfig(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_identity_type: Literal["user", "service_account"]
    """The type of identity that created the entity."""

    created_by_user_id: str
    """The user who originally created the entity."""

    evaluation_type: Literal["studio", "llm_auto", "human", "llm_benchmark"]
    """Evaluation type"""

    question_set_id: str

    auto_evaluation_model: Optional[
        Literal[
            "gpt-4-32k-0613",
            "gpt-4-turbo-preview",
            "gpt-4-turbo-2024-04-09",
            "gpt-4o-2024-05-13",
            "gpt-4o",
            "gpt-4o-mini-2024-07-18",
            "gpt-4o-mini",
            "gpt-4.1",
            "gpt-4.1-mini",
            "gpt-4.1-nano",
            "gpt-5-nano",
            "gpt-5-mini",
            "gpt-5",
            "gpt-5.1",
            "gpt-5.2",
            "o1",
            "o1-mini",
            "o3",
            "o3-mini",
            "o3-mini-2025-01-31",
            "o4-mini",
            "gpt-oss-120b",
            "gpt-oss-20b",
            "llama-3-70b-instruct",
            "llama-3-1-70b-instruct",
            "llama-3-70b-instruct-bedrock",
        ]
    ] = None
    """The name of the model to be used for auto-evaluation"""

    auto_evaluation_parameters: Optional[AutoEvaluationParameters] = None
    """Execution parameters for auto-evaluation"""

    studio_project_id: Optional[str] = None
