# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["EvaluationListParams"]


class EvaluationListParams(TypedDict, total=False):
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

    cursor: str
    """Cursor from the previous page's next_cursor. Omit for the first page."""

    limit: int

    name: str
    """Return only evaluations with exactly this name, including evaluation tables.

    Omit to list all evaluations in the scope.
    """
