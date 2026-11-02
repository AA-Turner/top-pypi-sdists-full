# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = ["ScoreCreateParams", "Score", "ScoreTarget"]


class ScoreCreateParams(TypedDict, total=False):
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

    scores: Required[Iterable[Score]]


class ScoreTarget(TypedDict, total=False):
    id: Required[str]
    """ID of the published case, comparison, or trajectory selected by kind."""

    kind: Required[Literal["case", "comparison", "trajectory"]]
    """Kind of resource being scored."""


class Score(TypedDict, total=False):
    scorer_id: Required[str]

    scorer_version_id: Required[str]

    target: Required[ScoreTarget]

    value: Required[object]
    """Score calculated by your application.

    Its JSON type must match the referenced scorer version's value_type.
    """

    attributes: Dict[str, object]
