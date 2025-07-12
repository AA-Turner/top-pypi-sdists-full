#
# Copyright 2024-2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.

"""
"Overall" configuration for a model is not specific to a particular moderation guard.
Typically these are pushed, along with guard configurations, to a new custom model version.

Settings are:

    timeout_sec: the maximum time in seconds allowed for moderation
    timeout_action: what do to if moderation times out: block or continue
    entity_id: the object (such as custom model version) this config applies to
    entity_type: the type of the related entity
    updated_at: the time this configuration was updated (not manually settable)
    updater_id: the ID of the user making the update (not manually settable)
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Set

import trafaret as t

from datarobot import errors
from datarobot.enums import ModerationGuardEntityType, ModerationTimeoutActionType
from datarobot.models.api_object import APIObject
from datarobot.utils.pagination import unpaginate

OVERALL_MODERATION_DEFAULT_TIMEOUT_SEC = 60


class OverallModerationConfig(APIObject):
    """Details of overall moderation configuration for a model."""

    _path = "overallModerationConfiguration/"

    _converter = t.Dict(
        {
            t.Key("timeout_sec"): t.Int(),
            t.Key("timeout_action"): t.Enum(*[e.value for e in ModerationTimeoutActionType]),
            t.Key("entity_id"): t.String(),
            t.Key("entity_type"): t.Enum(*[e.value for e in ModerationGuardEntityType]),
            t.Key("updated_at", optional=True): t.String(),
            t.Key("updater_id", optional=True): t.String(),
        }
    ).ignore_extra("*")

    schema = _converter

    def __init__(self, **kwargs: Any) -> None:
        self._set_values(**kwargs)

    def __repr__(self) -> str:
        return "Overall moderation configuration; see details"

    def _set_values(
        self: OverallModerationConfig,
        timeout_sec: int,
        timeout_action: ModerationTimeoutActionType,
        entity_id: str,
        entity_type: ModerationGuardEntityType,
        updated_at: str = "",
        updater_id: str = "",
    ) -> None:
        """
        Initialize an overall configuration object based on values from init or server data.
        """
        self.timeout_sec = timeout_sec
        self.timeout_action = ModerationTimeoutActionType(timeout_action)
        self.entity_id = entity_id
        self.entity_type = ModerationGuardEntityType(entity_type)
        self.updated_at = updated_at
        self.updater_id = updater_id

    def to_dict(self: OverallModerationConfig) -> Dict[str, str | int]:
        return {
            "timeoutSec": self.timeout_sec,
            "timeoutAction": self.timeout_action,
            "entityId": self.entity_id,
            "entityType": self.entity_type,
            "updatedAt": self.updated_at,
            "updaterId": self.updater_id,
        }

    @classmethod
    def _template_path(cls, template_id: str) -> str:
        return f"{cls._path}{template_id}/"

    def _update_values(
        self: OverallModerationConfig, new_response: OverallModerationConfig
    ) -> None:
        # called by update() and refresh()
        fields: Set[str] = self._fields()  # type: ignore[no-untyped-call]
        for attr in fields:
            new_value = getattr(new_response, attr)
            setattr(self, attr, new_value)

    @classmethod
    def find(
        cls, entity_id: str, entity_type: ModerationGuardEntityType
    ) -> Optional[OverallModerationConfig]:
        """Find overall configuration by entity ID and entity type.
        Each entity (such as a customModelVersion) may have at most 1 overall moderation configuration.

        .. versionadded:: v3.6

        Parameters
        ----------
        entity_id: str
            ID of the entity
        entity_type: str
            Type of the entity

        Returns
        -------
        Optional[OverallModerationConfig]
            an OverallModerationConfig or None

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        data = unpaginate(
            cls._path,
            {"entityId": entity_id, "entityType": entity_type.value},
            cls._client,
        )
        result = next(data, None)
        if not result:
            return None
        return cls.from_server_data(result)

    @classmethod
    def locate(
        cls, entity_id: str, entity_type: ModerationGuardEntityType
    ) -> OverallModerationConfig:
        """Find overall configuration by entity ID and entity type.
        This version of find() expects the object to exist. Its return type is not optional.

        .. versionadded:: v3.6

        Parameters
        ----------
        entity_id: str
            ID of the entity
        entity_type: str
            Type of the entity

        Returns
        -------
        List[OverallModerationConfig]
            a list of OverallModerationConfig

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        data = unpaginate(
            cls._path,
            {"entityId": entity_id, "entityType": entity_type.value},
            cls._client,
        )
        result = next(data, None)
        if not result:
            raise errors.ClientError(status_code=404, exc_message="Not found")
        return cls.from_server_data(result)

    @classmethod
    def create(
        cls,
        timeout_sec: int,
        timeout_action: ModerationTimeoutActionType,
        entity_id: str,
        entity_type: ModerationGuardEntityType,
    ) -> OverallModerationConfig:
        """Create an OverallModerationConfig.

        .. versionadded:: v3.6

        Parameters
        ----------
        timeout_sec: int
            how long to wait for all moderation tasks in a phase to complete.
        timeout_action: ModerationTimeoutActionType
            what to do if moderation times out.
        entity_id: str
            entity, such as customModelVersion, that this configuration applies to.
        entity_type: ModerationGuardEntityType
            type of the entity defined by entity_id

        Returns
        -------
        OverallModerationConfig
            created OverallModerationConfig

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        payload = {
            "timeoutSec": timeout_sec,
            "timeoutAction": timeout_action.value,
            "entityId": entity_id,
            "entityType": entity_type.value,
        }

        response = cls._client.patch(
            cls._path,
            data=payload,
        )
        return cls.from_server_data(response.json())

    def update(
        self: OverallModerationConfig,
        timeout_sec: int,
        timeout_action: ModerationTimeoutActionType,
        entity_id: str,
        entity_type: ModerationGuardEntityType,
    ) -> None:
        """Update an OverallModerationConfig.

        .. versionadded:: v3.6

        Parameters
        ----------
        timeout_sec: int
            how long to wait for all moderation tasks in a phase to complete.
        timeout_action: ModerationTimeoutActionType
            what to do if moderation times out.
        entity_id: str
            entity, such as customModelVersion, that this configuration applies to.
        entity_type: ModerationGuardEntityType
            type of the entity defined by entity_id

        Returns
        -------
        OverallModerationConfig
            created OverallModerationConfig

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """

        payload = {
            "timeoutSec": timeout_sec,
            "timeoutAction": timeout_action.value,
            "entityId": entity_id,
            "entityType": entity_type.value,
        }

        response = self._client.patch(
            self._path,
            data=payload,
        )
        new_version = self.from_server_data(response.json())
        self._update_values(new_version)

    def refresh(self: OverallModerationConfig) -> None:
        """Update OverallModerationConfig with the latest data from server.

        .. versionadded:: v3.6

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """

        new_object = self.locate(self.entity_id, self.entity_type)
        self._update_values(new_object)
