from typing import List, TypedDict, Union, Literal, Required, Dict


CounterMetricValue = Union[int, float]
""" counter_metric_value. """



DistributionMetricValue = List[Union[int, float]]
""" distribution_metric_value. """



class EncodedSeriesArrayMetricValue(TypedDict, total=False):
    """ encoded_series_array_metric_value. """

    format: Required[Literal['array']]
    """ Required property """

    data: Required["_EncodedSeriesArrayMetricValueData"]
    """
    Aggregation type: anyOf

    Required property
    """



class EncodedSeriesBase64MetricValue(TypedDict, total=False):
    """ encoded_series_base64_metric_value. """

    format: Required[Literal['base64']]
    """ Required property """

    data: Required[str]
    """ Required property """



class EncodedSeriesZstdMetricValue(TypedDict, total=False):
    """ encoded_series_zstd_metric_value. """

    format: Required[Literal['zstd']]
    """ Required property """

    data: Required[str]
    """ Required property """



class GaugeMetricValue(TypedDict, total=False):
    """ gauge_metric_value. """

    min: Required[Union[int, float]]
    """ Required property """

    max: Required[Union[int, float]]
    """ Required property """

    sum: Required[Union[int, float]]
    """ Required property """

    count: Required[int]
    """ Required property """

    last: Required[Union[int, float]]
    """ Required property """



class GenericMetric(TypedDict, total=False):
    """ generic_metric. """

    version: Literal[2]
    use_case_id: Required[str]
    """ Required property """

    org_id: Required[int]
    """ Required property """

    project_id: Required[int]
    """ Required property """

    metric_id: Required[int]
    """ Required property """

    type: Required[str]
    """ Required property """

    timestamp: Required[int]
    """
    minimum: 0

    Required property
    """

    sentry_received_timestamp: Union[int, float]
    tags: Required[Dict[str, str]]
    """ Required property """

    value: Required["_GenericMetricValue"]
    """
    Aggregation type: anyOf
    Subtype: "EncodedSeriesArrayMetricValue", "EncodedSeriesBase64MetricValue", "EncodedSeriesZstdMetricValue", "CounterMetricValue", "SetMetricValue", "DistributionMetricValue", "GaugeMetricValue"

    Required property
    """

    retention_days: Required[int]
    """ Required property """

    mapping_meta: Required[Dict[str, Dict[str, str]]]
    """ Required property """

    aggregation_option: str
    sampling_weight: Union[int, float]
    """
    minimum: 1
    maximum: 18446744073709551615
    """



SetMetricValue = List[int]
""" set_metric_value. """



_EncodedSeriesArrayMetricValueData = Union[List[Union[int, float]], List[int]]
""" Aggregation type: anyOf """



_GenericMetricValue = Union["EncodedSeriesArrayMetricValue", "EncodedSeriesBase64MetricValue", "EncodedSeriesZstdMetricValue", "CounterMetricValue", "SetMetricValue", "DistributionMetricValue", "GaugeMetricValue"]
"""
Aggregation type: anyOf
Subtype: "EncodedSeriesArrayMetricValue", "EncodedSeriesBase64MetricValue", "EncodedSeriesZstdMetricValue", "CounterMetricValue", "SetMetricValue", "DistributionMetricValue", "GaugeMetricValue"
"""

