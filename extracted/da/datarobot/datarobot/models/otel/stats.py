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

import trafaret as t

from datarobot.models.api_object import APIObject
from datarobot.models.otel.utils import to_datetime_param
from datarobot.utils.pagination import unpaginate


class OtelStats(APIObject):
    """Otel statistics.

    .. versionadded:: v3.14

    Attributes
    ----------
    service_name: str
        The service name of the process.
    user_id: str
        The user ID.
    span_count: int
        The number of spans used by this entity.
    metric_count: int
        The number of metrics used by this entity.
    log_count: int
        The number of logs used by this entity.
    """

    _path = "otel/stats/"
    _converter = t.Dict({
        t.Key("service_name"): t.String(allow_blank=False),
        t.Key("user_id"): t.String(),
        t.Key("span_count"): t.Int(),
        t.Key("metric_count"): t.Int(),
        t.Key("log_count"): t.Int(),
    }).ignore_extra("*")

    def __init__(
        self,
        service_name: str,
        user_id: str = "",
        log_count: int = 0,
        metric_count: int = 0,
        span_count: int = 0,
    ):
        self.service_name = service_name
        self.user_id = user_id
        self.log_count = log_count
        self.metric_count = metric_count
        self.span_count = span_count

    def __repr__(self) -> str:
        counts = f"logs={self.log_count}, metrics={self.metric_count}, spans={self.span_count}"
        return f"OtelStats({self.service_name}, {counts})"

    @classmethod
    def list(
        cls,
        service_names: Optional[str | List[str]] = None,
        user_ids: Optional[str | List[str]] = None,
        start_time: Optional[datetime | date | str] = None,
        end_time: Optional[datetime | date | str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[OtelStats]:
        """List the Otel usage statistics.

        .. versionadded:: v3.14

        Parameters
        ----------
        service_names: Optional[str | List[str]]
            The service name or list of service names for the process.
        user_ids: Optional[str | List[str]]
            The user IDs to view. You must be administrator to use this field.
        start_time: Optional[datetime | date | str]
            The start time of the log list.
        end_time: Optional[datetime | date | str]
            The end time of the log list.
        offset: Optional[int]
            Offset for pagination.
        limit: Optional[int]
            Limit for pagination.

        Returns
        -------
        stats: List[OtelStats]
        """
        path = cls._path
        params: Dict[str, Any] = {}
        if service_names:
            params["serviceName"] = service_names
        if user_ids:
            params["userId"] = user_ids
        if start_time:
            params["startTime"] = to_datetime_param(start_time)
        if end_time:
            params["endTime"] = to_datetime_param(end_time)
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit

        if offset is None:
            data = unpaginate(path, params, cls._client)
        else:
            data = cls._client.get(path, params=params or None).json()["data"]
        return [cls.from_server_data(d) for d in data]
