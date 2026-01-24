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
from datarobot.models.otel.metric_enums import MetricAggregation
from datarobot.utils import to_api
from datarobot.utils.pagination import unpaginate


class OtelMetricConfig(APIObject):
    """OpenTelemetry metric configuration.

    .. versionadded:: v3.9

    Attributes
    ----------
    otelName: str
        Name of the OpenTelemetry reported metric.
    id: Optional[str]
        ID of the metric configuration. This is optional to allow setting list.
    displayName: Optional[str]
        Name to display for the reported metric.
    aggregation: Optional[str|MetricAggregation]
        Aggregation type to use for the reported metric.
    enabled: Optional[bool]
        Whether the reported metric is shown in displays.
    """

    _path = "otel/{}/{}/metrics/configs/"
    _converter = t.Dict({
        t.Key("otel_name"): t.String(),
        t.Key("id", optional=True): t.Or(t.String(), t.Null()),
        t.Key("display_name", optional=True): t.Or(t.String(), t.Null()),
        t.Key("aggregation", optional=True): t.Or(t.Enum(*[e.value for e in MetricAggregation]), t.String(), t.Null()),
        t.Key("enabled", optional=True): t.Or(t.Bool(), t.Null()),
    }).ignore_extra("*")

    def __init__(
        self,
        otel_name: str,
        id: Optional[str] = None,
        display_name: Optional[str] = None,
        aggregation: Optional[str | MetricAggregation] = None,
        enabled: Optional[bool] = None,
        # NOTE: fields below are not provided by server, but tracked for object operations
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
    ) -> None:
        self.id = id
        self.otel_name = otel_name
        self.display_name = display_name
        self.aggregation = aggregation
        self.enabled = enabled
        self.entity_type = entity_type
        self.entity_id = entity_id

    def __repr__(self) -> str:
        name = self.display_name
        if not name:
            name = self.otel_name
            if self.aggregation:
                name += f" ({self.aggregation})"
        return f"OtelMetricConfig({name}, {self.id})"

    @classmethod
    def from_server_data_with_entity(
        cls,
        data: Dict[str, Any],
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
    ) -> OtelMetricConfig:
        config = cls.from_server_data(data)
        config.entity_type = entity_type
        config.entity_id = entity_id
        return config

    @classmethod
    def create(
        cls,
        entity_type: str,
        entity_id: str,
        otel_name: str,
        display_name: Optional[str] = None,
        aggregation: Optional[str] = None,
        enabled: Optional[bool] = None,
    ) -> OtelMetricConfig:
        """Create a new OpenTelemetry metric configuration.

        .. versionadded:: v3.9

        Parameters
        ----------
        entity_type: str
            The entity type of the log entries (e.g. deployment, or use_case)
        entity_id: str
            The entity id of the log entries (e.g. `123456`)
        otel_name: str
            Name of the reported metric.
        display_name: Optional[str]
            Name to display for the reported metric.
        aggregation: Optional[str]
            Aggregation type to use for the reported metric.
        enabled: Optional[bool]
            Whether the reported metric is shown in displays.
        """
        body: Dict[str, Any] = {
            "otelName": otel_name,
        }
        if display_name:
            body["displayName"] = display_name
        if aggregation:
            body["aggregation"] = str(aggregation)
        if enabled is not None:
            body["enabled"] = enabled
        url = cls._path.format(entity_type, entity_id)
        response = cls._client.post(url, json=body)
        return cls.from_server_data_with_entity(response.json(), entity_type, entity_id)

    @classmethod
    def set_list(
        cls,
        entity_type: str,
        entity_id: str,
        configs: List[OtelMetricConfig | Dict[str, Any]],
    ) -> List[OtelMetricConfig]:
        """Set a list of OpenTelemetry metric configurations.

        .. versionadded:: v3.9

        Parameters
        ----------
        entity_type: str
            The entity type of the log entries (e.g. deployment, or use_case)
        entity_id: str
            The entity id of the log entries (e.g. `123456`)
        configs: List[OtelMetricConfig]
            Ordered list of OpenTelemetry metric configurations.
        """
        items: List[Dict[str, Any]] = []
        for config in configs:
            item: Dict[str, Any] = {}
            if isinstance(config, dict):
                item = config
            elif isinstance(config, APIObject):
                data = to_api(config)
                if isinstance(data, dict):
                    item = data
                else:
                    continue
            item.pop("id", None)
            item.pop("entityId", None)
            item.pop("entityType", None)
            items.append(item)

        url = cls._path.format(entity_type, entity_id)
        cls._client.put(url, json={"values": items})

        return cls.list(entity_type, entity_id)

    @classmethod
    def list(
        cls,
        entity_type: str,
        entity_id: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[OtelMetricConfig]:
        """List OpenTelemetry metric configurations.

        .. versionadded:: v3.9

        Parameters
        ----------
        entity_type: str
            The entity type of the log entries (e.g. deployment, or use_case)
        entity_id: str
            The entity id of the log entries (e.g. `123456`)
        offset: Optional[int]
            Offset for pagination.
        limit: Optional[int]
            Limit for pagination.

        Returns
        -------
        info: List[OtelMetricConfig]
        """
        path = cls._path.format(entity_type, entity_id)
        params: Dict[str, Any] = {}
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit

        if offset is None:
            data = unpaginate(path, params, cls._client)
        else:
            response = cls._client.get(path, params=params if params else None)
            data = response.json()["data"]

        return [cls.from_server_data_with_entity(d, entity_type, entity_id) for d in data]

    @classmethod
    def get(
        cls,
        entity_type: str,
        entity_id: str,
        config_id: str,
    ) -> OtelMetricConfig:
        """Get an OpenTelemetry metric configuration by ID.

        .. versionadded:: v3.9

        Parameters
        ----------
        entity_type: str
            The entity type of the log entries (e.g. deployment, or use_case)
        entity_id: str
            The entity id of the log entries (e.g. `123456`)
        config_id: str
            ID of the OpenTelemetry metric configuration.

        Returns
        -------
        config : OtelMetricConfig
        """
        url = cls._path.format(entity_type, entity_id) + config_id + "/"
        response = cls._client.get(url)
        return cls.from_server_data_with_entity(response.json(), entity_type, entity_id)

    def update(
        self,
        otel_name: Optional[str] = None,
        display_name: Optional[str] = None,
        aggregation: Optional[str | MetricAggregation] = None,
        enabled: Optional[bool] = None,
    ) -> None:
        """Update an OpenTelemetry metric configuration.

        .. versionadded:: v3.9

        Parameters
        ----------
        otel_name: Optional[str]
            Name of the reported metric.
        display_name: Optional[str]
            Name to display for the reported metric.
        aggregation: Optional[str]
            Aggregation type to use for the reported metric.
        enabled: Optional[bool]
            Whether the reported metric is shown in displays.
        """
        body: Dict[str, Any] = {}
        if otel_name:
            body["otelName"] = otel_name
        if display_name is not None:
            body["displayName"] = display_name
        if aggregation is not None:
            body["aggregation"] = str(aggregation)
        if enabled is not None:
            body["enabled"] = enabled

        if not self.id:
            raise ValueError("Cannot update a metric configuration without an ID")

        url = self._path.format(self.entity_type, self.entity_id) + self.id + "/"
        response = self._client.patch(url, json=body)

        # the response comes with the latest data, so update all the fields
        data = response.json()
        self.otel_name = data.get("otelName")
        self.display_name = data.get("displayName")
        self.aggregation = data.get("aggregation")
        self.enabled = data.get("enabled")

    def delete(self) -> None:
        """
        Delete this OpenTelemetry metric configuration.

        .. versionadded:: v3.9

        Returns
        -------
        None
        """

        if not self.id:
            raise ValueError("Cannot delete a metric configuration without an ID")

        url = self._path.format(self.entity_type, self.entity_id) + self.id + "/"
        self._client.delete(url)
