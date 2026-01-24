#
# Copyright 2025 DataRobot, Inc. and its affiliates.
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

from datetime import datetime
from typing import Any, Dict, List, Optional

import trafaret as t

from datarobot.models.api_object import APIObject
from datarobot.utils import parse_time
from datarobot.utils.pagination import unpaginate


class OtelLogEntry(APIObject):
    """An Otel log entry.

    .. versionadded:: v3.9

    Attributes
    ----------
    level: Optional[str]
        Log level string of entry.
    message: str
        The log message.
    timestamp: datetime
        Actuals data export creation timestamp.
    """

    _path = "otel/{}/{}/logs/"
    _converter = t.Dict({
        t.Key("timestamp"): parse_time,
        t.Key("message", optional=True, default=""): t.Or(t.String(allow_blank=True), t.Null()),
        t.Key("level", optional=True, default=None): t.Or(t.Null(), t.String()),
        t.Key("stacktrace", optional=True, default=None): t.Or(t.Null(), t.String()),
        t.Key("span_id", optional=True, default=None): t.Or(t.Null(), t.String()),
        t.Key("trace_id", optional=True, default=None): t.Or(t.Null(), t.String()),
    }).ignore_extra("*")

    def __init__(
        self,
        timestamp: datetime,
        message: str = "",
        level: Optional[str] = None,
        stacktrace: Optional[str] = None,
        span_id: Optional[str] = None,
        trace_id: Optional[str] = None,
    ):
        self.timestamp = timestamp
        self.message = message
        self.level = level
        self.stacktrace = stacktrace
        self.span_id = span_id
        self.trace_id = trace_id

    def __repr__(self) -> str:
        time = str(self.timestamp.time())  # use truncated time, since most are on same day
        # use truncated/aligned formatting for easier viewing in a list
        return f"OtelLogEntry({time:15} - {self.level or '':8} - {self.message:40})"

    @classmethod
    def list(
        cls,
        entity_type: str,
        entity_id: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        level: Optional[str] = None,
        includes: Optional[str | List[str]] = None,
        excludes: Optional[str | List[str]] = None,
        span_id: Optional[str] = None,
        trace_id: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[OtelLogEntry]:
        """List the log entries associated with the specified entity type/id.

        .. versionadded:: v3.9

        Parameters
        ----------
        entity_type: str
            The entity type of the log entries (e.g. deployment or use_case).
        entity_id: str
            The entity ID of the log entries (e.g. `123456`).
        start_time: Optional[datetime]
            The start time of the log list.
        end_time: Optional[datetime]
            The end time of the log list.
        level: Optional[str]
            The minimum log level of the log entries.
        includes: Optional[str | List[str]]
            A string, or list of strings, which must be included in the log entry.
        excludes: Optional[str | List[str]]
            A string, or list of strings, which must NOT be included in the log entry.
        span_id: Optional[str]
            The span ID that (if provided) must be in the log entries.
        trace_id: Optional[str]
            The trace ID that (if provided) must be in the log entries.
        offset: Optional[int]
            Offset for pagination.
        limit: Optional[int]
            Limit for pagination.

        Returns
        -------
        logs: List[OtelLogEntry]
        """
        path = cls._path.format(entity_type, entity_id)
        params: Dict[str, Any] = {}
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        if level:
            params["level"] = level
        if includes:
            params["includes"] = includes
        if excludes:
            params["excludes"] = excludes
        if span_id:
            params["spanId"] = span_id
        if trace_id:
            params["traceId"] = trace_id
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit

        if offset is None:
            data = unpaginate(path, params, cls._client)
        else:
            data = cls._client.get(path, params=params if params else None).json()["data"]
        return [cls.from_server_data(d) for d in data]
