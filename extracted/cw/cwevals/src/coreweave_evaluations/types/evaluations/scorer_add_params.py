# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

__all__ = ["ScorerAddParams", "Scorer"]


class ScorerAddParams(TypedDict, total=False):
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

    scorers: Required[Iterable[Scorer]]
    """Scorer versions to add.

    Each Scorer ID must be unique. An already registered Scorer changes to the
    supplied version, which must keep its registered name and value type.
    """


class Scorer(TypedDict, total=False):
    scorer_id: Required[str]

    version_id: Required[str]
