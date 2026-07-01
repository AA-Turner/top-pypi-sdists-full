#
# Copyright 2026 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc. Confidential.
#
# This is unpublished proprietary source code of DataRobot, Inc.
# and its affiliates.
#
# The copyright notice above does not evidence any actual or intended
# publication of such source code.
from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, List, Optional

import dateutil
import trafaret as t

from datarobot.models.api_object import APIObject
from datarobot.models.otel.utils import to_datetime_param

OtelMetricAggValueTrafaret = t.Dict({
    t.Key("otel_name"): t.String(),
    t.Key("aggregation", optional=True): t.Or(t.String(), t.Null()),
    t.Key("display_name", optional=True): t.Or(t.String(), t.Null()),
    t.Key("unit", optional=True): t.Or(t.String(), t.Null()),
    t.Key("aggregated_value", optional=True): t.Or(t.Float(), t.Null()),
    t.Key("current_value", optional=True): t.Or(t.Float(), t.Null()),
    t.Key("buckets", optional=True): t.Or(t.List(t.Dict().allow_extra("*")), t.Null()),
}).ignore_extra("*")


class OtelMetricAggValue(APIObject):
    """OpenTelemetry single metric aggregated value.

    .. versionadded:: v3.12

    Attributes
    ----------
    otel_name: str
      The OTel key of the metric.
    aggregation: Optional[str]
      The aggregation method used for metric display.
    display_name: Optional[str]
      The display name of the metric.
    unit: Optional[str]
      The unit of measurement for the metric.
    aggregated_value: Optional[float]
      The aggregated metric value over the period.
    current_value: Optional[float]
      The current metric value at request time.
    buckets: Optional[List[Dict[str, Any]]]
      The histogram bucket values.
    """

    _converter = OtelMetricAggValueTrafaret

    def __init__(
        self,
        otel_name: str,
        aggregation: Optional[str] = None,
        display_name: Optional[str] = None,
        unit: Optional[str] = None,
        aggregated_value: Optional[float] = None,
        current_value: Optional[float] = None,
        buckets: Optional[List[Dict[str, Any]]] = None,
    ):
        self.otel_name = otel_name
        self.aggregation = aggregation
        self.display_name = display_name
        self.unit = unit
        self.aggregated_value = aggregated_value
        self.current_value = current_value
        self.buckets = buckets

    def __repr__(self) -> str:
        name = self.display_name or self.otel_name
        if self.aggregation == "histogram":
            bucket_len = len(self.buckets) if self.buckets else 0
            value = f"{bucket_len} buckets"
        else:
            value = str(self.aggregated_value)
        return f"{self.__class__.__name__}({name}, {value})"


class OtelMetricAggregatedValues(APIObject):
    """OpenTelemetry aggregated metric values for configured metrics.

    .. versionadded:: v3.12

    Attributes
    ----------
    metric_aggregations: List[OtelMetricAggValue]
      description: A list of OTel metric value periods.
    start_time: Optional[datetime]
      description: The start time of the metric value period.
    end_time: Optional[datetime]
      description: The end time of the metric value period.
    """

    _path = "otel/{}/{}/metrics/values/"
    _converter = t.Dict({
        t.Key("metric_aggregations"): t.List(OtelMetricAggValueTrafaret),
        t.Key("start_time"): t.String() >> dateutil.parser.parse,
        t.Key("end_time"): t.String() >> dateutil.parser.parse,
    }).ignore_extra("*")

    def __init__(
        self,
        metric_aggregations: List[OtelMetricAggValue | Dict[str, Any]],
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ):
        self.start_time = start_time
        self.end_time = end_time
        self.metric_aggregations = []
        for ma in metric_aggregations:
            if isinstance(ma, OtelMetricAggValue):
                self.metric_aggregations.append(ma)
            if isinstance(ma, dict):
                self.metric_aggregations.append(OtelMetricAggValue(**ma))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({len(self.metric_aggregations)} metrics)"

    @classmethod
    def get(
        cls,
        entity_type: str,
        entity_id: str,
        start_time: Optional[datetime | date | str] = None,
        end_time: Optional[datetime | date | str] = None,
        histogram_buckets: bool = False,
    ) -> OtelMetricAggregatedValues:
        """Get the OpenTelemetry metric aggregated value for configured metrics.

        .. versionadded:: v3.12

        Parameters
        ----------
        entity_type: str
            Type of the entity to which the metric belongs.
        entity_id: str
            ID of the entity to which the metric belongs.
        start_time: Optional[datetime | date | str]
            The start time of the metric list.
        end_time: Optional[datetime | date | str]
            The end time of the metric list.
        histogram_buckets: bool
            Return histograms as buckets instead of percentile values, default is False.

        Returns
        -------
        info: OtelMetricAggregatedValues
        """
        path = cls._path.format(entity_type, entity_id)
        params = {
            'histogramBuckets': str(histogram_buckets).lower(),
        }
        if start_time:
            params['startTime'] = to_datetime_param(start_time)
        if end_time:
            params['endTime'] = to_datetime_param(end_time)

        data = cls._client.get(path, params=params).json()
        return cls.from_server_data(data)
