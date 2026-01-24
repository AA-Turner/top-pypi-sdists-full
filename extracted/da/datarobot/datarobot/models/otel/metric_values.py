#
# Copyright 2025 DataRobot, Inc. and its affiliates.
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

from datetime import datetime
from typing import Any, Dict, List, Optional

import dateutil
import trafaret as t

from datarobot.models.api_object import APIObject
from datarobot.models.otel.metric_enums import MetricResolution

OtelMetricValueTrafaret = t.Dict({
    t.Key("otel_name"): t.String(),
    t.Key("samples"): t.Int(),
    t.Key("delta", optional=True): t.Or(t.Float(), t.Null()),
    t.Key("value", optional=True): t.Or(t.Float(), t.Null()),
    t.Key("buckets", optional=True): t.Or(t.List(t.Dict().allow_extra("*")), t.Null()),
    t.Key("display_name", optional=True): t.Or(t.String(), t.Null()),
    t.Key("aggregation", optional=True): t.Or(t.String(), t.Null()),
    t.Key("id", optional=True): t.Or(t.String(), t.Null()),
}).ignore_extra("*")


class OtelMetricBucketValue(APIObject):
    """OpenTelemetry metric bucket value.

    .. versionadded:: v3.9

    Attributes
    ----------
    otel_name: str
        The OTEL name of the metric.
    value: Optional[float]
        The metric value for the period.
    buckets: Optional[list[dict]
        Histogram bucket values.
    samples: int
        Number of metric values in the period.
    delta: Optional[float]
        Difference between value from previous period (if any).
    display_name: Optional[str]
        The display name of the metric.
    aggregation: Optional[str]
        The aggregation type of the metric.
    id: Optional[str]
        The ID of the metric configuration (if any).
    """

    _converter = OtelMetricValueTrafaret

    def __init__(
        self,
        otel_name: str,
        samples: int,
        value: Optional[float] = None,
        buckets: Optional[List[Dict[str, Any]]] = None,
        delta: Optional[float] = None,
        display_name: Optional[str] = None,
        aggregation: Optional[str] = None,
        id: Optional[str] = None,
    ) -> None:
        self.otel_name = otel_name
        self.value = value
        self.buckets = buckets
        self.display_name = display_name
        self.samples = samples
        self.delta = delta
        self.aggregation = aggregation
        self.id = id

    def __repr__(self) -> str:
        params = [
            self.display_name or self.otel_name,
            str(self.value),
        ]
        return f"{self.__class__.__name__}({', '.join(params)})"


class OtelMetricValue(APIObject):
    """OpenTelemetry metric value.

    .. versionadded:: v3.9

    Attributes
    ----------
    start_time: datetime
        Start time of the metric value period.
    end_time: datetime
        End time of the metric value period.
    values: List[OtelMetricBucketValue]
        List of metric bucket values.
    """

    _path = "otel/{}/{}/metrics/valuesOverTime/"
    _converter = t.Dict({
        t.Key("start_time"): t.String() >> dateutil.parser.parse,
        t.Key("end_time"): t.String() >> dateutil.parser.parse,
        t.Key("values"): t.List(OtelMetricValueTrafaret),
    }).ignore_extra("*")

    def __init__(
        self,
        start_time: datetime,
        end_time: datetime,
        values: List[OtelMetricBucketValue | dict[str, Any]],
    ) -> None:
        self.start_time = start_time
        self.end_time = end_time
        self.values = []
        for value in values:
            if isinstance(value, OtelMetricBucketValue):
                self.values.append(value)
            if isinstance(value, dict):
                self.values.append(OtelMetricBucketValue(**value))

    def __repr__(self) -> str:
        params = [
            f"start={self.start_time}",
            f"{len(self.values)} values",
        ]
        return f"{self.__class__.__name__}({', '.join(params)})"

    @classmethod
    def list(
        cls,
        entity_type: str,
        entity_id: str,
        resolution: MetricResolution,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> List[OtelMetricValue]:
        """List OpenTelemetry metric buckets with values.

        .. versionadded:: v3.9

        Parameters
        ----------
        entity_type: str
            The entity type of the reported metrics (e.g. deployment, or use_case).
        entity_id: str
            The entity ID of the reported metrics (e.g. `123456`).
        resolution: OtelMetricResolution
            Period for values of the metric list.
        start_time: Optional[datetime]
            Start time of the metric list.
        end_time: Optional[datetime]
            End time of the metric list.

        Returns
        -------
        info: List[OtelMetricValue]
        """
        path = cls._path.format(entity_type, entity_id)
        params: Dict[str, Any] = {
            "resolution": resolution,
        }
        if start_time:
            params["startTime"] = start_time.isoformat()
        if end_time:
            params["endTime"] = end_time.isoformat()

        data = cls._client.get(path, params=params).json()["data"]
        return [cls.from_server_data(d) for d in data]
