# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["Dashboard", "Visualization", "VisualizationMetadata"]


class VisualizationMetadata(BaseModel):
    is_variant_specific_metric: Optional[bool] = None

    label_color_map: Optional[Dict[str, str]] = None

    label_title_map: Optional[Dict[str, str]] = None


class Visualization(BaseModel):
    id: str

    metric_id: Literal[
        "total_requests",
        "total_errors",
        "total_tokens",
        "average_latency",
        "p95_latency",
        "error_rate",
        "average_users",
        "aggregated_tokens",
        "feedback",
        "execution_input_response_tokens",
        "execution_average_latency_per_variant",
        "execution_error_rate",
        "execution_latency_percentile",
        "execution_average_latency_per_node",
    ]

    title: str

    type: Literal["scalar", "bar", "stacked_bar", "line"]

    metadata: Optional[VisualizationMetadata] = None


class Dashboard(BaseModel):
    id: str

    title: str

    visualizations: List[Visualization]
