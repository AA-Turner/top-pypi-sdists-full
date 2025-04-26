#
# Copyright 2024 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from datetime import datetime
from typing import Any, Dict, Optional

import trafaret as t

from datarobot._compat import String
from datarobot.mlops.enums import EventStatusType, RemoteEventType
from datarobot.models.api_object import APIObject
from datarobot.utils import datetime_to_string

EVENT_MESSAGE_MAX_LENGTH = 16384
PE_LABEL_MAX_LENGTH = 512
MAX_GUARD_NAME_LENGTH = 512


class MLOpsEvent(APIObject):
    """
    An MLOps Event Object: An object representing an important MLOps activity that
    happened.  For example, health, service issues with the DataRobot deployment
    or a prediction environment or a particular phase in a long operation (like
    creation of deployment or processing training data) is completed or errored.

    This class allows the client to report such event to the DataRobot service.

    Notes
    -----
        DataRobot backend support lots of events and all these events are categorized
        into different categories.  This class does not yet support *ALL* events, but
        we will gradually add support for them

        Supported Event Categories:
            - moderation
    """

    _path = "remoteEvents/"

    _moderation_data = t.Dict(
        {
            t.Key("guard_name", optional=True): String(
                max_length=MAX_GUARD_NAME_LENGTH, allow_blank=True
            ),
            t.Key("metric_name", optional=True): String(
                max_length=MAX_GUARD_NAME_LENGTH, allow_blank=True
            ),
        }
    ).allow_extra("*")

    _converter = t.Dict(
        {
            t.Key("id"): String(),
            t.Key("title", optional=True): String(max_length=PE_LABEL_MAX_LENGTH),
            t.Key("status_type", optional=True): t.Enum(*[e.value for e in EventStatusType]),
            t.Key("type"): t.Enum(*[e.value for e in RemoteEventType]),
            t.Key("timestamp"): String(),
            t.Key("message", optional=True): String(max_length=EVENT_MESSAGE_MAX_LENGTH),
            t.Key("moderation_data", optional=True): _moderation_data,
        }
    ).allow_extra("*")

    def __init__(
        self,
        id: str,
        type: RemoteEventType,
        status_type: EventStatusType,
        timestamp: Optional[str] = None,
        title: Optional[str] = None,
        message: Optional[str] = None,
        moderation_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.id = id
        self.type = type
        self.title = title
        self.message = message
        self.moderation_data = moderation_data
        self.timestamp = timestamp
        self.status_type = status_type

    @classmethod
    def report_moderation_event(
        cls,
        event_type: str,
        timestamp: Optional[str] = None,
        title: Optional[str] = None,
        message: Optional[str] = None,
        deployment_id: Optional[str] = None,
        org_id: Optional[str] = None,
        guard_name: Optional[str] = None,
        metric_name: Optional[str] = None,
    ) -> None:
        """
        Reports a moderation event

        Parameters
        ----------
        event_type : str
            The type of the moderation event.
        timestamp : Optional[str]
            The timestamp of the event, datetime, or string in RFC3339 format. If the datetime provided
            does not have a timezone, DataRobot assumes it is UTC.
        title : Optional[str]
            The title of the moderation event.
        message : Optional[str]
            A description of the moderation event.
        deployment_id : Optional[str]
            The ID of the deployment associated with the event.
        org_id : Optional[str]
            The ID of the organization associated with the event.
        guard_name : Optional[str]
            The name or label of the guard.
        metric_name : Optional[str]
            The name or label of the metric.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If event_type is not one of the moderation event types.
            If fails to create the event.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.mlops.events import MLOpsEvent
            >>> MLOpsEvent.report_moderation_event(
            ...     event_type="moderationMetricCreationError",
            ...     title="Failed to create moderation metric",
            ...     message="Maximum number of custom metrics reached",
            ...     deployment_id="5c939e08962d741e34f609f0",
            ...     metric_name="Blocked Prompts",
            ... )
        """
        if event_type not in RemoteEventType.moderation_event_types():
            raise ValueError(
                f"Invalid moderation event type {event_type}, supported events are: "
                f"{RemoteEventType.moderation_event_types()}"
            )

        _timestamp = timestamp
        if _timestamp is None:
            _timestamp = datetime_to_string(datetime.utcnow())

        payload = {
            "title": title,
            "message": message,
            "timestamp": _timestamp,
            "deploymentId": str(deployment_id),
            "eventType": event_type,
            "moderationData": {
                "guardName": guard_name if guard_name else "",
                "metricName": metric_name if metric_name else "",
            },
            "orgId": org_id,
        }

        try:
            cls._client.post(cls._path, data=payload)
        except Exception as ex:
            raise Exception(f"Failed to create moderation event: {ex}")
