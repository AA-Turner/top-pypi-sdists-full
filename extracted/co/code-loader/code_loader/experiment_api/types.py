
from dataclasses import dataclass
from typing import Dict, Union


MetricValue = Union[str, float]
Metrics = Dict[str, MetricValue]

@dataclass
class NumericMetricValue:
    value: float
    type: str = "number"

@dataclass
class StringMetricValue:
    value: str
    type: str = "string"

@dataclass
class ImageMetricValue:
    value: str
    type: str = "image"

ApiMetricValue = Union[NumericMetricValue, StringMetricValue, ImageMetricValue]
ApiMetrics = Dict[str, ApiMetricValue]
