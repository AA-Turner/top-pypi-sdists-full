# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal, TypeAlias

__all__ = ["EvaluationWidgetTypeEnum"]

EvaluationWidgetTypeEnum: TypeAlias = Literal[
    "bar", "histogram", "donut", "scatter", "metric", "table", "markdown", "heading", "timeseries"
]
