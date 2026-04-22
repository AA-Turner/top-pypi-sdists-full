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
from datarobot.models.otel.metric_enums import MetricResolution
from datarobot.models.otel.utils import to_datetime_param

OtelSingleMetricTimeBucketTrafaret = t.Dict({
    t.Key("start_time"): t.String() >> dateutil.parser.parse,
    t.Key("end_time"): t.String() >> dateutil.parser.parse,
    t.Key("samples"): t.Int(),
    t.Key("delta", optional=True): t.Or(t.Float(), t.Null()),
    t.Key("value", optional=True): t.Or(t.Float(), t.Null()),
    t.Key("buckets", optional=True): t.Or(t.List(t.Dict().allow_extra("*")), t.Null()),
}).ignore_extra("*")


class OtelSingleMetricTimeBucket(APIObject):
    """OpenTelemetry single metric bucket value.

    .. versionadded:: v3.12

    Attributes
    ----------
    start_time: datetime
        Start time of the metric value period.
    end_time: datetime
        End time of the metric value period.
    samples: int
        Number of metric values in the period.
    value: Optional[float]
        The metric value for the period.
    delta: Optional[float]
        Difference between value from previous period (if any).
    buckets: Optional[list[dict[str, Any]]]
        Histogram bucket values.
    """

    _converter = OtelSingleMetricTimeBucketTrafaret

    def __init__(
        self,
        start_time: datetime,
        end_time: datetime,
        samples: int,
        value: Optional[float] = None,
        delta: Optional[float] = None,
        buckets: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        self.start_time = start_time
        self.end_time = end_time
        self.samples = samples
        self.value = value
        self.delta = delta
        self.buckets = buckets

    def __repr__(self) -> str:
        bucket_len = len(self.buckets) if self.buckets else 0
        value = str(self.value) if self.value is not None else f"{bucket_len} buckets"
        params = [self.start_time.isoformat(), value]
        return f"{self.__class__.__name__}({', '.join(params)})"


class OtelSingleMetricValue(APIObject):
    """OpenTelemetry single metric value.

    .. versionadded:: v3.12

    Attributes
    ----------
    otel_name:
        The OTel metric name.
    time_buckets: List[OtelSingleMetricTimeBucket]
        List of single metric time bucket values.
    display_name: Optional[str]
        The display name of the metric.
    aggregation: Optional[str]
        The aggregation of the metric.
    id: Optional[str]
        The ID of the metric configuration.
    unit: Optional[str]
        The reported unit of the metric.
    """

    _path = "otel/{}/{}/metrics/valueOverTime/"
    _converter = t.Dict({
        t.Key("otel_name"): t.String(),
        t.Key("time_buckets"): t.List(OtelSingleMetricTimeBucketTrafaret),
        t.Key("display_name", optional=True): t.Or(t.String(), t.Null()),
        t.Key("aggregation", optional=True): t.Or(t.String(), t.Null()),
        t.Key("id", optional=True): t.Or(t.String(), t.Null()),
        t.Key("unit", optional=True): t.Or(t.String(), t.Null()),
    }).ignore_extra("*")

    def __init__(
        self,
        otel_name: str,
        time_buckets: List[OtelSingleMetricTimeBucket | dict[str, Any]],
        display_name: Optional[str] = None,
        aggregation: Optional[str] = None,
        id: Optional[str] = None,
        unit: Optional[str] = None,
    ) -> None:
        self.otel_name = otel_name
        self.display_name = display_name
        self.aggregation = aggregation
        self.id = id
        self.unit = unit
        self.time_buckets = []
        for tb in time_buckets:
            if isinstance(tb, OtelSingleMetricTimeBucket):
                self.time_buckets.append(tb)
            if isinstance(tb, dict):
                self.time_buckets.append(OtelSingleMetricTimeBucket(**tb))

    def __repr__(self) -> str:
        params = [
            self.otel_name,
            f"{len(self.time_buckets)} time buckets",
        ]
        return f"{self.__class__.__name__}({', '.join(params)})"

    @classmethod
    def get(
        cls,
        entity_type: str,
        entity_id: str,
        otel_name: str,
        aggregation: str,
        resolution: Optional[MetricResolution] = None,
        start_time: Optional[datetime | date | str] = None,
        end_time: Optional[datetime | date | str] = None,
        percentile: Optional[float] = None,
    ) -> OtelSingleMetricValue:
        """List OpenTelemetry metric with time-bucket values.

        .. versionadded:: v3.12

        Parameters
        ----------
        entity_type: str
            The entity type of the reported metrics (e.g., deployment, or use_case).
        entity_id: str
            The entity ID of the reported metrics (e.g., `123456`).
        otel_name: str
            The OTel metric name.
        aggregation: str
            The aggregation to use for getting metric data.
        resolution: Optional[OtelMetricResolution]
            Period for values of the metric list, server defaults to PT1H.
        start_time: Optional[datetime | date | str]
            Start time of the metric list.
        end_time: Optional[datetime | date | str]
            End time of the metric list.
        percentile: Optional[float]
            Percentile of the metric values used with `percentiles` aggregation, between 0 and 1.

        Returns
        -------
        info: OtelSingleMetricValue
        """
        path = cls._path.format(entity_type, entity_id)
        params: Dict[str, Any] = {
            "otelName": otel_name,
            "aggregation": aggregation,
        }
        if resolution:
            params["resolution"] = resolution
        if start_time:
            params["startTime"] = to_datetime_param(start_time)
        if end_time:
            params["endTime"] = to_datetime_param(end_time)
        if percentile is not None:
            params["percentile"] = percentile

        data = cls._client.get(path, params=params).json()
        return cls.from_server_data(data)
