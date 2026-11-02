# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Required, TypedDict

__all__ = ["MetricReportParams", "Metric"]


class MetricReportParams(TypedDict, total=False):
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

    metrics: Required[Iterable[Metric]]


class Metric(TypedDict, total=False):
    name: Required[str]

    value: Required[object]
    """Metric value calculated by your application, in any JSON type.

    Send JSON null to remove this metric from this commit onward.
    """

    subject: Optional[str]
    """Model, checkpoint, or other entity the metric describes.

    Leading and trailing whitespace are not allowed. Omit or send null for a metric
    describing the whole evaluation.
    """
