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

from typing import Any, Dict, List, Optional

import trafaret as t

from datarobot.models.api_object import APIObject


class OtelMetricSummary(APIObject):
    """Reported OpenTelemetry metric summary information.

    .. versionadded:: v3.9

    Attributes
    ----------
    otelName: str
        Name of the reported metric.
    description: Optional[str]
        Description of the reported metric.
    metricType: Optional[str]
        Reported metric type (e.g. counter, gauge, histogram).
    units: Optional[str]
        Units of the reported metric.
    """

    _path = "otel/{}/{}/metrics/summary/"
    _converter = t.Dict({
        t.Key("otel_name"): t.String(),
        t.Key("description", optional=True): t.Or(t.String(), t.Null()),
        t.Key("metric_type", optional=True): t.Or(t.String(), t.Null()),
        t.Key("units", optional=True): t.Or(t.String(), t.Null()),
    }).ignore_extra("*")

    def __init__(
        self,
        otel_name: str,
        description: Optional[str] = None,
        metric_type: Optional[str] = None,
        units: Optional[str] = None,
    ) -> None:
        self.otel_name = otel_name
        self.description = description
        self.metric_type = metric_type
        self.units = units

    def __repr__(self) -> str:
        params = [self.otel_name]
        if self.units:
            params.append(f"units={self.units}")
        if self.metric_type:
            params.append(f"type={self.metric_type}")
        if self.description:
            params.append(f"description='{self.description}'")
        return f"OtelMetricSummary({','.join(params)})"

    @classmethod
    def list(
        cls,
        entity_type: str,
        entity_id: str,
        search: Optional[str] = None,
        metric_type: Optional[str] = None,
    ) -> List[OtelMetricSummary]:
        """List OpenTelemetry metric summary information.

        .. versionadded:: v3.9

        Parameters
        ----------
        entity_type: str
            The entity type of the reported metrics (e.g. deployment, or use_case).
        entity_id: str
            The entity ID of the reported metrics (e.g. `123456`).
        search: Optional[str]
            Only return metrics whose name contains this case-sensitive value.
        metric_type: Optional[str]
            Only return metrics whose type matches this value (e.g. counter, gauge, histogram).

        Returns
        -------
        summary: List[OtelMetricSummary]
        """
        path = cls._path.format(entity_type, entity_id)
        params: Dict[str, Any] = {}
        if search:
            params["search"] = search
        if metric_type:
            params["metricType"] = metric_type

        data = cls._client.get(path, params=params if params else None).json()["data"]
        return [cls.from_server_data(d) for d in data]
