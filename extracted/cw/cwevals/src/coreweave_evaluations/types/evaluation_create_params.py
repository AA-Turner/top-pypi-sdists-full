# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = ["EvaluationCreateParams", "Source", "SourceFixedEvaluationSource", "SourceLiveEvaluationSource"]


class EvaluationCreateParams(TypedDict, total=False):
    namespace: str
    """Namespace that assigned the scope reference."""

    scope_id: str
    """Project reference assigned by the namespace.

    For wandb, use the internal W&B project ID, not the project name or
    entity/project path.

    Percent-encode reserved characters so the reference occupies one URL path
    segment. Only printable ASCII is accepted. References are compared exactly,
    without parsing.
    """

    name: Required[str]

    primary_target_kind: Required[Literal["case", "trajectory"]]
    """Whether this evaluation reads individual cases or trajectories from its source."""

    source: Required[Source]

    attributes: Dict[str, object]


class SourceFixedEvaluationSource(TypedDict, total=False):
    dataset_version_id: Required[str]

    kind: Required[Literal["fixed"]]


class SourceLiveEvaluationSource(TypedDict, total=False):
    dataset_id: Required[str]

    kind: Required[Literal["live"]]


Source: TypeAlias = Union[SourceFixedEvaluationSource, SourceLiveEvaluationSource]
