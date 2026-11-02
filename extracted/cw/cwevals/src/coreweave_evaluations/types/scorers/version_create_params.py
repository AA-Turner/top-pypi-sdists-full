# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["VersionCreateParams"]


class VersionCreateParams(TypedDict, total=False):
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

    allowed_target_kinds: Required[List[Literal["case", "comparison", "trajectory"]]]
    """
    Kinds of resource this scorer version can score: individual cases, comparisons,
    or trajectories.
    """

    name: Required[str]
    """Name of this scoring specification, such as accuracy or relevance.

    Leading and trailing whitespace are not allowed.
    """

    value_type: Required[Literal["null", "boolean", "integer", "number", "string", "json"]]
    """JSON type that every score recorded with this scorer version must use."""

    description: Optional[str]
    """Human-readable explanation of what this scorer version measures."""
