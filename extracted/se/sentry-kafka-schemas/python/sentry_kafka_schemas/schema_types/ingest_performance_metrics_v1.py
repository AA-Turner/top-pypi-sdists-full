from typing import Required, Union, TypedDict, Literal, List, Dict


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



class IngestMetric(TypedDict, total=False):
    """ ingest_metric. """

    org_id: Required[int]
    """
    The organization for which this metric is being sent.

    minimum: 0
    maximum: 18446744073709551615

    Required property
    """

    project_id: Required[int]
    """
    The project for which this metric is being sent.

    minimum: 0
    maximum: 18446744073709551615

    Required property
    """

    name: Required[str]
    """
    The metric name. Relay sometimes calls this an MRI and makes assumptions about its string shape, and those assumptions also exist in certain queries. The rest of the ingestion pipeline treats it as an opaque string.

    Required property
    """

    type: Required["_IngestMetricType"]
    """
    The metric type. [c]ounter, [d]istribution, [s]et. Relay additionally defines Gauge, but that metric type is completely unsupported downstream.

    Required property
    """

    timestamp: Required[int]
    """
    The timestamp at which this metric was being sent. Relay will round this down to the next 10-second interval.

    minimum: 0
    maximum: 18446744073709551615

    Required property
    """

    tags: Required[Dict[str, str]]
    """ Required property """

    value: Required["_IngestMetricValue"]
    """
    Aggregation type: anyOf
    Subtype: "EncodedSeriesArrayMetricValue", "EncodedSeriesBase64MetricValue", "EncodedSeriesZstdMetricValue", "CounterMetricValue", "SetMetricValue", "DistributionMetricValue", "GaugeMetricValue"

    Required property
    """

    retention_days: Required[int]
    """
    minimum: 0
    maximum: 65535

    Required property
    """

    received_at: int
    """
    The oldest timestamp of the first metric that was received in this bucket by the outermost internal Relay.

    minimum: 0
    maximum: 18446744073709551615
    """

    sampling_weight: Union[int, float]
    """
    minimum: 1
    maximum: 18446744073709551615
    """



SetMetricValue = List["_SetMetricValueItem"]
""" set_metric_value. """



_EncodedSeriesArrayMetricValueData = Union[List[Union[int, float]], List[int]]
""" Aggregation type: anyOf """



_IngestMetricType = Union[Literal['c'], Literal['d'], Literal['s'], Literal['g']]
""" The metric type. [c]ounter, [d]istribution, [s]et. Relay additionally defines Gauge, but that metric type is completely unsupported downstream. """
_INGESTMETRICTYPE_C: Literal['c'] = "c"
"""The values for the 'The metric type. [c]ounter, [d]istribution, [s]et. Relay additionally defines Gauge, but that metric type is completely unsupported downstream' enum"""
_INGESTMETRICTYPE_D: Literal['d'] = "d"
"""The values for the 'The metric type. [c]ounter, [d]istribution, [s]et. Relay additionally defines Gauge, but that metric type is completely unsupported downstream' enum"""
_INGESTMETRICTYPE_S: Literal['s'] = "s"
"""The values for the 'The metric type. [c]ounter, [d]istribution, [s]et. Relay additionally defines Gauge, but that metric type is completely unsupported downstream' enum"""
_INGESTMETRICTYPE_G: Literal['g'] = "g"
"""The values for the 'The metric type. [c]ounter, [d]istribution, [s]et. Relay additionally defines Gauge, but that metric type is completely unsupported downstream' enum"""



_IngestMetricValue = Union["EncodedSeriesArrayMetricValue", "EncodedSeriesBase64MetricValue", "EncodedSeriesZstdMetricValue", "CounterMetricValue", "SetMetricValue", "DistributionMetricValue", "GaugeMetricValue"]
"""
Aggregation type: anyOf
Subtype: "EncodedSeriesArrayMetricValue", "EncodedSeriesBase64MetricValue", "EncodedSeriesZstdMetricValue", "CounterMetricValue", "SetMetricValue", "DistributionMetricValue", "GaugeMetricValue"
"""



_SetMetricValueItem = int
"""
minimum: 0
maximum: 4294967295
"""

