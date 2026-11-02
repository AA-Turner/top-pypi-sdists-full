# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel

__all__ = [
    "EvaluationListResponse",
    "Evaluation",
    "EvaluationSource",
    "EvaluationSourceFixedEvaluationSource",
    "EvaluationSourceLiveEvaluationSource",
]


class EvaluationSourceFixedEvaluationSource(BaseModel):
    dataset_version_id: str

    kind: Literal["fixed"]


class EvaluationSourceLiveEvaluationSource(BaseModel):
    dataset_id: str

    kind: Literal["live"]


EvaluationSource: TypeAlias = Annotated[
    Union[EvaluationSourceFixedEvaluationSource, EvaluationSourceLiveEvaluationSource],
    PropertyInfo(discriminator="kind"),
]


class Evaluation(BaseModel):
    attributes: Dict[str, object]

    evaluation_id: str

    name: str

    namespace: Literal["wandb"]
    """Namespace that assigned the scope reference."""

    primary_target_kind: Literal["case", "trajectory"]

    scope_ref: str

    source: EvaluationSource


class EvaluationListResponse(BaseModel):
    evaluations: List[Evaluation]

    next_cursor: Optional[str] = None
