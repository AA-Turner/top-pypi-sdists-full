# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .shared_params.auto_evaluation_parameters import AutoEvaluationParameters

__all__ = ["EvaluationConfigCreateParams", "AutoEvalEvaluationConfigRequest", "ManualEvaluationConfigRequest"]


class AutoEvalEvaluationConfigRequest(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    question_set_id: Required[str]

    auto_evaluation_model: Literal[
        "llama-3-1-70b-instruct",
        "gpt-4-turbo-2024-04-09",
        "llama-3-70b-instruct-bedrock",
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4.1",
        "gpt-4.1-mini",
        "gpt-4.1-nano",
        "o1",
        "o3",
        "o3-mini",
        "o4-mini",
    ]
    """The name of the model to be used for auto-evaluation"""

    auto_evaluation_parameters: AutoEvaluationParameters
    """Execution parameters for auto-evaluation"""

    evaluation_type: Literal["llm_auto", "llm_benchmark"]
    """Evaluation type"""

    studio_project_id: str


class ManualEvaluationConfigRequest(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    question_set_id: Required[str]

    auto_evaluation_model: None
    """The name of the model to be used for auto-evaluation.

    Not applicable for manual evaluations.
    """

    auto_evaluation_parameters: AutoEvaluationParameters
    """Execution parameters for auto-evaluation"""

    evaluation_type: Literal["studio", "human"]
    """Evaluation type"""

    studio_project_id: str


EvaluationConfigCreateParams: TypeAlias = Union[AutoEvalEvaluationConfigRequest, ManualEvaluationConfigRequest]
