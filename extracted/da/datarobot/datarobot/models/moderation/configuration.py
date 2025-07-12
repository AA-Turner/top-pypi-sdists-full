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
The configuration object here applies to an individual guard.
Moderation for a model can involve multiple guards: models, NeMo guardrails, etc.

    name = dto.DtoField(t.String(max_length=MAX_GUARD_NAME_LENGTH))
    type = dto.DtoField(t.Enum(*GuardType.all()), auto_convert=True)
    description = dto.DtoField(t.String(max_length=MAX_GUARD_DESCRIPTION_LENGTH))
    created_at = dto.DtoField(RFC3339NoTZStringTrafaret(), auto_convert=True)
    creator_id = dto.DtoField(t.Or(MongoId(), t.Null()), auto_convert=True)
    # configurations are stored for a custom model (not a specific version)
    # or a playground ID
    # however, in prod, publishing the configs (to a model YAML file)
    # can be done only the latest model version (and creates a new one)
    entity_id = dto.DtoField(MongoId(), auto_convert=True)
    entity_type = dto.DtoField(t.Enum(*GuardEntityType.all()), auto_convert=True)
    deployment_id = dto.DtoFieldOptional(MongoId() | t.Null(), auto_convert=True, default=None)

"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set

import trafaret as t
from trafaret import String

from datarobot.enums import (
    GuardType,
    ModerationGuardEntityType,
    ModerationGuardLlmType,
    ModerationGuardOotbType,
    ModerationGuardStage,
)
from datarobot.models.api_object import APIObject
from datarobot.models.moderation.intervention import GuardInterventionForConfiguration
from datarobot.models.moderation.model_info import GuardModelInfo
from datarobot.models.moderation.nemo_info import GuardNemoInfo
from datarobot.models.moderation.utils import exclude_if
from datarobot.utils import parse_time
from datarobot.utils.pagination import unpaginate


class ModerationConfiguration(APIObject):
    """Details of overall moderation configuration for a model."""

    _path = "guardConfigurations/"

    @classmethod
    def _config_path(cls, config_id: str) -> str:
        return f"{cls._path}{config_id}/"

    _converter = t.Dict(
        {
            t.Key("id"): String(),
            t.Key("name"): String(),
            t.Key("description"): String(),
            t.Key("type"): t.Enum(*[e.value for e in GuardType]),
            t.Key("entity_id"): t.String(),
            t.Key("entity_type"): t.Enum(*[e.value for e in ModerationGuardEntityType]),
            t.Key("ootb_type", optional=True): t.Enum(*[e.value for e in ModerationGuardOotbType]),
            t.Key("llm_type", optional=True): t.Enum(*[e.value for e in ModerationGuardLlmType]),
            t.Key("deployment_id", optional=True): String(allow_blank=True),
            t.Key("created_at", optional=True): t.Or(parse_time, t.Null),
            t.Key("creator_id", optional=True): String(allow_blank=True),
            t.Key("org_id", optional=True): String(allow_blank=True),
            t.Key("intervention", optional=True): GuardInterventionForConfiguration.schema,
            t.Key("model_info", optional=True): GuardModelInfo.schema,
            t.Key("nemo_info", optional=True): GuardNemoInfo.schema,
            # below are part of configuration, but not from a template
            t.Key("stages"): t.List(t.Enum(*[e.value for e in ModerationGuardStage])),
            t.Key("is_valid", optional=True): t.Bool(),
            t.Key("error_message", optional=True): String(),
            t.Key("openai_api_key", optional=True): String(),
            t.Key("openai_api_base", optional=True): String(),
            t.Key("openai_deployment_id", optional=True): String(),
            t.Key("openai_credential", optional=True): String(),
        }
    ).ignore_extra("*")

    schema = _converter

    def __init__(
        self: ModerationConfiguration,
        id: str,
        name: str,
        type: GuardType,
        description: str,
        created_at: str,
        entity_id: str,
        entity_type: ModerationGuardEntityType,
        stages: list[ModerationGuardStage],
        ootb_type: Optional[str] = None,
        llm_type: Optional[str] = None,
        deployment_id: Optional[str] = None,
        creator_id: Optional[str] = None,
        org_id: Optional[str] = None,
        intervention: Optional[GuardInterventionForConfiguration | Dict[str, Any]] = None,
        model_info: Optional[GuardModelInfo | Dict[str, Any]] = None,
        nemo_info: Optional[GuardNemoInfo | Dict[str, Any]] = None,
        is_valid: Optional[bool] = True,
        error_message: Optional[str] = "",
        openai_api_key: Optional[str] = "",
        openai_api_base: Optional[str] = "",
        openai_deployment_id: Optional[str] = "",
        openai_credential: Optional[str] = "",
    ) -> None:
        self.id = id
        self.name = name
        self.type = GuardType(type)
        self.description = description
        self.created_at = created_at
        self.entity_id = entity_id
        self.entity_type = ModerationGuardEntityType(entity_type)
        self.stages = [ModerationGuardStage(x) for x in stages]
        self.creator_id = creator_id
        self.org_id = org_id
        self.nemo_info = nemo_info
        self.ootb_type = None
        if ootb_type:
            self.ootb_type = ModerationGuardOotbType(ootb_type)
        self.llm_type = None
        if llm_type:
            self.llm_type = ModerationGuardLlmType(llm_type)
        self.deployment_id = None
        if deployment_id:
            self.deployment_id = deployment_id
        # the following may arrive as objects or as dicts
        if intervention is None:
            self.intervention = None
        else:
            self.intervention = GuardInterventionForConfiguration.ensure_object(intervention)
        if model_info is None:
            self.model_info = None
        else:
            self.model_info = GuardModelInfo.ensure_object(model_info)
        self.is_valid = is_valid
        self.error_message = error_message
        self.openai_api_key = openai_api_key
        self.openai_api_base = openai_api_base
        self.openai_deployment_id = openai_deployment_id
        self.openai_credential = openai_credential

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name or self.id!r})"

    def _update_values(
        self: ModerationConfiguration, new_response: ModerationConfiguration
    ) -> None:
        # called by update() and refresh()
        fields: Set[str] = self._fields()  # type: ignore[no-untyped-call]
        for attr in fields:
            new_value = getattr(new_response, attr)
            setattr(self, attr, new_value)

    @classmethod
    def get(cls, config_id: str) -> ModerationConfiguration:
        """Get a guard configuration by ID.

        .. versionadded:: v3.6

        Parameters
        ----------
        config_id: str
            ID of the configuration

        Returns
        -------
        ModerationConfiguration
            retrieved configuration

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        path = cls._config_path(config_id)
        return cls.from_location(path)

    @classmethod
    def list(
        cls, entity_id: str, entity_type: ModerationGuardEntityType
    ) -> List[ModerationConfiguration]:
        """List Guard Configurations.

        .. versionadded:: v3.6

        Parameters
        ----------
        entity_id: str
            ID of the entity
        entity_type: ModerationGuardEntityType
            Type of the entity

        Returns
        -------
        List[ModerationConfiguration]
            a list of configurations

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
        return [cls.from_server_data(item) for item in data]

    @classmethod
    def create(
        cls,
        template_id: str,
        name: str,
        description: str,
        stages: List[ModerationGuardStage],
        entity_id: str,
        entity_type: ModerationGuardEntityType,
        intervention: Optional[GuardInterventionForConfiguration] = None,
        llm_type: Optional[ModerationGuardLlmType] = None,
        deployment_id: Optional[str] = None,
        model_info: Optional[GuardModelInfo] = None,
        nemo_info: Optional[GuardNemoInfo] = None,
        openai_api_key: Optional[str] = "",
        openai_api_base: Optional[str] = "",
        openai_deployment_id: Optional[str] = "",
        openai_credential: Optional[str] = "",
    ) -> ModerationConfiguration:
        """Create a configuration. This is not a full create from scratch; it's based on a template.

        .. versionadded:: v3.6

        Parameters
        ----------
        template_id: str
            ID of the template to base this configuration on.
        name: str
            name of the configuration.
        description: str
            description of the configuration.
        stages: List[ModerationGuardStage]
            the stages of moderation where this guard is active
        entity_id:
            ID of the custom model version or playground this configuration applies to.
        entity_type: ModerationGuardEntityType
            Type of the associated entity_id
        llm_type:
            the backing LLM this guard uses.
        nemo_info
            additional configuration for NeMo Guardrails guards.
        model_info
            additional configuration for guards using a deployed model.
        intervention
            the assessment conditions, and action the guard should take if conditions are met.
        openai_api_key: str
            Token to use for OpenAI. Deprecated; use openai_credential instead.
        openai_api_base:
            Base of the OpenAI connection
        openai_deployment_id
            ID of the OpenAI deployment
        openai_credential
            ID of the credential defined in DataRobot for OpenAI.

        Returns
        -------
        ModerationConfiguration
            created ModerationConfiguration

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        # start with required fields, then optional
        payload = {
            "templateId": template_id,
            "name": name,
            "description": description,
            "stages": stages,  # enum, but the framework converts back/forth to string
            "llmType": llm_type,
            "entityId": entity_id,
            "entityType": entity_type.value,
        }
        # omit the following fields if they're empty
        payload.update(exclude_if("deployment_id", deployment_id))
        payload.update(exclude_if("openai_api_key", openai_api_key))
        payload.update(exclude_if("openai_api_base", openai_api_base))
        payload.update(exclude_if("openai_deployment_id", openai_deployment_id))
        payload.update(exclude_if("openai_credential", openai_credential))
        payload.update(exclude_if("intervention", intervention))
        payload.update(exclude_if("model_info", model_info))
        payload.update(exclude_if("nemo_info", nemo_info))

        response = cls._client.post(
            cls._path,
            data=payload,
        )
        # todo: POST response should include entire object, but only returns ID.
        # template has the same issue.
        # todo: re-fetch until that's fixed, then use cls.from_server_data(response.json())
        return cls.get(response.json()["id"])

    def update(
        self: ModerationConfiguration,
        name: Optional[str] = None,
        description: Optional[str] = None,
        intervention: Optional[GuardInterventionForConfiguration] = None,
        llm_type: Optional[ModerationGuardLlmType] = None,
        deployment_id: Optional[str] = None,
        model_info: Optional[GuardModelInfo] = None,
        nemo_info: Optional[GuardNemoInfo] = None,
        openai_api_key: Optional[str] = "",
        openai_api_base: Optional[str] = "",
        openai_deployment_id: Optional[str] = "",
        openai_credential: Optional[str] = "",
    ) -> None:
        """Update configuration. All fields are optional, and omitted fields are left unchanged.

        entity_id, entity_type, and stages cannot be modified for a guard configuration,.

        .. versionadded:: v3.6

        Parameters
        ----------
        name: str
            name of the configuration.
        description: str
            description of the configuration.
        llm_type:
            the backing LLM this guard uses.
        nemo_info
            additional configuration for NeMo Guardrails guards.
        model_info
            additional configuration for guards using a deployed model.
        intervention
            the assessment conditions, and action the guard should take if conditions are met.
        openai_api_key: str
            Token to use for OpenAI. Deprecated; use openai_credential instead.
        openai_api_base:
            Base of the OpenAI connection
        openai_deployment_id
            ID of the OpenAI deployment
        openai_credential
            ID of the credential defined in DataRobot for OpenAI.

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        payload = {}
        payload.update(exclude_if("name", name))
        payload.update(exclude_if("description", description))
        payload.update(exclude_if("llm_type", llm_type))
        payload.update(exclude_if("deployment_id", deployment_id))
        payload.update(exclude_if("openai_api_key", openai_api_key))
        payload.update(exclude_if("openai_api_base", openai_api_base))
        payload.update(exclude_if("openai_deployment_id", openai_deployment_id))
        payload.update(exclude_if("openai_credential", openai_credential))
        payload.update(exclude_if("intervention", intervention))
        payload.update(exclude_if("model_info", model_info))
        payload.update(exclude_if("nemo_info", nemo_info))

        response = self._client.patch(self._config_path(self.id), data=payload)
        data = response.json()
        new_version = self.from_server_data(data)
        self._update_values(new_version)

    def refresh(self: ModerationConfiguration) -> None:
        """Update OverallModerationConfig with the latest data from server.

        .. versionadded:: v3.6

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """

        new_object = self.get(self.id)
        self._update_values(new_object)

    def delete(self: ModerationConfiguration) -> None:
        """Delete configuration.

        .. versionadded:: v3.6

        Raises
        ------
        datarobot.errors.ClientError
            If the server responded with 4xx status.
        datarobot.errors.ServerError
            If the server responded with 5xx status.
        """
        path = self._config_path(self.id)
        self._client.delete(path)
