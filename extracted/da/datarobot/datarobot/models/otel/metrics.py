#
# Copyright 2026 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, List, Optional

from datarobot.models.api_object import APIObject
from datarobot.models.otel.metric_summary import OtelMetricSummary
from datarobot.models.otel.utils import to_datetime_param


class OtelMetrics(APIObject):
    """General ``OTel`` metric wrapper class.

    .. versionadded:: v3.13
    """

    _path = "otel/{}/{}/metrics/"

    @classmethod
    def list(
        cls,
        entity_type: str,
        entity_id: str,
        search: Optional[str] = None,
        metric_type: Optional[str] = None,
    ) -> List[OtelMetricSummary]:
        """Returns a list of available OpenTelemetry metric information.

        .. versionadded:: v3.13

        Parameters
        ----------
        entity_type: str
            The entity type of the reported metrics (e.g., deployment or ``use_case``).
        entity_id: str
            The entity ID of the reported metrics (e.g., `123456`).
        search: Optional[str]
            Only return metrics whose name contains this case-sensitive value.
        metric_type: Optional[str]
            Only return metrics whose type matches this value (e.g., counter, gauge, histogram).

        Returns
        -------
        summary: List[OtelMetricSummary]
        """
        return OtelMetricSummary.list(entity_type, entity_id, search, metric_type)

    @classmethod
    def delete(
        cls,
        entity_type: str,
        entity_id: str,
        start_time: Optional[datetime | date | str] = None,
        end_time: Optional[datetime | date | str] = None,
    ) -> None:
        """Deletes the ``OTel`` metrics associated with the specified entity type/ID.

        .. versionadded:: v3.13

        Parameters
        ----------
        entity_type: str
            The entity type of the metrics (e.g., deployment or ``use_case``).
        entity_id: str
            The entity ID of the metrics (e.g., `123456`).
        start_time: Optional[datetime | date | str]
            The start time of the metrics to delete.
        end_time: Optional[datetime | date | str]
            The end time of the metrics to delete.

        Returns
        -------
        None
        """
        path = cls._path.format(entity_type, entity_id)
        params: Dict[str, Any] = {}
        if start_time:
            params["startTime"] = to_datetime_param(start_time)
        if end_time:
            params["endTime"] = to_datetime_param(end_time)

        cls._client.delete(path, params=params or None)
