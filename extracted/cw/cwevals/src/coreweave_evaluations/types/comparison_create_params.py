# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable, Optional
from typing_extensions import Required, TypedDict

__all__ = ["ComparisonCreateParams", "Comparison", "ComparisonMember"]


class ComparisonCreateParams(TypedDict, total=False):
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

    comparisons: Required[Iterable[Comparison]]


class ComparisonMember(TypedDict, total=False):
    case_id: Required[str]

    role: Optional[str]
    """Optional label for this case's role in the comparison.

    The service does not impose a vocabulary for roles.
    """


class Comparison(TypedDict, total=False):
    members: Required[Iterable[ComparisonMember]]

    attributes: Dict[str, object]
