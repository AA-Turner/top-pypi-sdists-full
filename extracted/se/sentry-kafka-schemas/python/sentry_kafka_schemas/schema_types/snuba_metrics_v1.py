from typing import List, TypedDict, Union, Literal, Required, Dict


CounterMetricValue = Union[int, float]
""" counter_metric_value. """



DistributionMetricValue = List[Union[int, float]]
""" distribution_metric_value. """



class Metric(TypedDict, total=False):
    """ metric. """

    version: Literal[1]
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
    tags: Required[Dict[str, int]]
    """ Required property """

    value: Required["_MetricValue"]
    """
    Aggregation type: anyOf
    Subtype: "CounterMetricValue", "SetMetricValue", "DistributionMetricValue"

    Required property
    """

    retention_days: Required[int]
    """ Required property """

    mapping_meta: Required[Dict[str, Dict[str, str]]]
    """ Required property """



SetMetricValue = List[int]
""" set_metric_value. """



_MetricValue = Union["CounterMetricValue", "SetMetricValue", "DistributionMetricValue"]
"""
Aggregation type: anyOf
Subtype: "CounterMetricValue", "SetMetricValue", "DistributionMetricValue"
"""

