# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Union
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel

__all__ = ["EvaluationCreateResponse", "Source", "SourceFixedEvaluationSource", "SourceLiveEvaluationSource"]


class SourceFixedEvaluationSource(BaseModel):
    dataset_version_id: str

    kind: Literal["fixed"]


class SourceLiveEvaluationSource(BaseModel):
    dataset_id: str

    kind: Literal["live"]


Source: TypeAlias = Annotated[
    Union[SourceFixedEvaluationSource, SourceLiveEvaluationSource], PropertyInfo(discriminator="kind")
]


class EvaluationCreateResponse(BaseModel):
    attributes: Dict[str, object]

    evaluation_id: str

    name: str

    namespace: Literal["wandb"]
    """Namespace that assigned the scope reference."""

    primary_target_kind: Literal["case", "trajectory"]

    scope_ref: str

    source: Source
