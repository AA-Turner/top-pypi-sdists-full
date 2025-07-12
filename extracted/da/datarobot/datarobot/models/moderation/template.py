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
from __future__ import annotations

from typing import Any, Dict, List, Optional, Set

import trafaret as t

from datarobot._compat import String
from datarobot.enums import (
    GuardType,
    ModerationGuardLlmType,
    ModerationGuardOotbType,
    ModerationGuardStage,
)
from datarobot.models.api_object import APIObject
from datarobot.models.moderation.intervention import GuardInterventionForTemplate
from datarobot.models.moderation.model_info import GuardModelInfo
from datarobot.models.moderation.nemo_info import GuardNemoInfo
from datarobot.models.moderation.utils import exclude_if
from datarobot.utils import parse_time
from datarobot.utils.pagination import unpaginate


class ModerationTemplate(APIObject):
    """A DataRobot Moderation Template.

    .. versionadded:: v3.6

    Attributes
    ----------
    id: str
        ID of the Template
    name: str
        Template name
    """

    _path = "guardTemplates/"

    _converter = t.Dict(
        {
            t.Key("id"): String(),
            t.Key("name"): String(),
            t.Key("description"): String(),
            t.Key("type"): t.Enum(*[e.value for e in GuardType]),
            t.Key("ootb_type", optional=True): t.Enum(*[e.value for e in ModerationGuardOotbType]),
            t.Key("llm_type", optional=True): t.Enum(*[e.value for e in ModerationGuardLlmType]),
            t.Key("allowed_stages"): t.List(t.Enum(*[e.value for e in ModerationGuardStage])),
            t.Key("created_at", optional=True): t.Or(parse_time, t.Null),
            t.Key("creator_id", optional=True): String(allow_blank=True),
            t.Key("org_id", optional=True): String(allow_blank=True),
            t.Key("intervention", optional=True): GuardInterventionForTemplate.schema,
            t.Key("model_info", optional=True): GuardModelInfo.schema,
            t.Key("nemo_info", optional=True): GuardNemoInfo.schema,
        }
    ).ignore_extra("*")

    schema = _converter

    def __init__(
        self: ModerationTemplate,
        id: str,
        name: str,
        type: GuardType,
        description: str,
        created_at: str,
        allowed_stages: list[ModerationGuardStage],
        ootb_type: Optional[str] = None,
        llm_type: Optional[str] = None,
        creator_id: Optional[str] = None,
        org_id: Optional[str] = None,
        intervention: Optional[GuardInterventionForTemplate | Dict[str, Any]] = None,
        model_info: Optional[GuardModelInfo | Dict[str, Any]] = None,
        nemo_info: Optional[GuardNemoInfo | Dict[str, Any]] = None,
    ) -> None:
        self.id = id
        self.name = name
        self.type = GuardType(type)
        self.description = description
        self.created_at = created_at
        self.allowed_stages = [ModerationGuardStage(x) for x in allowed_stages]
        self.creator_id = creator_id
        self.org_id = org_id
        self.nemo_info = nemo_info
        self.ootb_type = None
        if ootb_type:
            self.ootb_type = ModerationGuardOotbType(ootb_type)
        self.llm_type = None
        if llm_type:
            self.llm_type = ModerationGuardLlmType(llm_type)
        # the following may arrive as objects or as dicts
        if intervention is None:
            self.intervention = None
        else:
            self.intervention = GuardInterventionForTemplate.ensure_object(intervention)
        if model_info is None:
            self.model_info = None
        else:
            self.model_info = GuardModelInfo.ensure_object(model_info)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name or self.id!r})"

    def _update_values(self: ModerationTemplate, new_response: ModerationTemplate) -> None:
        # called by update() and refresh()
        fields: Set[str] = self._fields()  # type: ignore[no-untyped-call]
        for attr in fields:
            new_value = getattr(new_response, attr)
            setattr(self, attr, new_value)

    @classmethod
    def _template_path(cls, template_id: str) -> str:
        return f"{cls._path}{template_id}/"

    @classmethod
    def get(cls, template_id: str) -> ModerationTemplate:
        """Get Template by id.

        .. versionadded:: v3.6

        Parameters
        ----------
        template_id: str
            ID of the Template

        Returns
        -------
        ModerationTemplate
            retrieved Template

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        path = cls._template_path(template_id)
        return cls.from_location(path)

    @classmethod
    def list(cls) -> List[ModerationTemplate]:
        """List Templates.

        .. versionadded:: v3.6

        Parameters
        ----------
        none yet

        Returns
        -------
        List[ModerationTemplate]
            a list of Templates

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        data = unpaginate(
            cls._path,
            {},
            cls._client,
        )
        return [cls.from_server_data(item) for item in data]

    @classmethod
    def find(cls, name: str) -> Optional[ModerationTemplate]:
        """Find Template by name.

        .. versionadded:: v3.6

        Parameters
        ----------
        name: str
            name of the Template

        Returns
        -------
        List[ModerationTemplate]
            a list of Templates

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        data = unpaginate(
            cls._path,
            {"name": name},
            cls._client,
        )
        kv_data = next(data, None)
        if not kv_data:
            return None
        return cls.from_server_data(kv_data)

    @classmethod
    def create(
        cls,
        name: str,
        description: str,
        type: GuardType,
        allowed_stages: List[ModerationGuardStage],
        intervention: Optional[GuardInterventionForTemplate] = None,
        ootb_type: Optional[ModerationGuardOotbType] = None,
        llm_type: Optional[ModerationGuardLlmType] = None,
        model_info: Optional[GuardModelInfo] = None,
        nemo_info: Optional[GuardNemoInfo] = None,
    ) -> ModerationTemplate:
        """Create a Template.

        .. versionadded:: v3.6

        Parameters
        ----------
        name: str
            name of the template.
        description: str
            description of the template.
        type: GuardType
            type of the template.
        allowed_stages: List[ModerationGuardStage]
            the stages of moderation this guard is allowed to be used
        ootb_type: ModerationGuardOotbType
            for guards of type "ootb", the specific "Out of the Box" metric type.
        llm_type:
            the backing LLM this guard uses.
        nemo_info
            additional configuration for NeMo Guardrails guards.
        model_info
            additional configuration for guards using a deployed model.
        intervention
            the assessment conditions, and action the guard should take if conditions are met.

        Returns
        -------
        ModerationTemplate
            created Template

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        payload = {
            "name": name,
            "type": type.value,
            "description": description,
            "allowedStages": allowed_stages,
            "ootbType": ootb_type,
            "llmType": llm_type,
            "intervention": intervention,
            "parameters": [],  # required but deprecated
        }
        if intervention:
            payload["intervention"] = intervention
        if model_info:
            payload["modelInfo"] = model_info
        if nemo_info:
            payload["nemoInfo"] = model_info

        response = cls._client.post(
            cls._path,
            data=payload,
        )

        # todo: POST response should include entire object, but only returns ID.
        # todo: re-fetch until that's fixed, then use cls.from_server_data(response.json())
        return cls.get(response.json()["id"])

    def update(
        self: ModerationTemplate,
        name: Optional[str] = None,
        description: Optional[str] = None,
        type: Optional[GuardType] = None,
        allowed_stages: Optional[List[ModerationGuardStage]] = None,
        intervention: Optional[GuardInterventionForTemplate] = None,
        ootb_type: Optional[ModerationGuardOotbType] = None,
        llm_type: Optional[ModerationGuardLlmType] = None,
        model_info: Optional[GuardModelInfo] = None,
        nemo_info: Optional[GuardNemoInfo] = None,
    ) -> None:
        """Update Template. All fields are optional, and omitted fields are left unchanged.

        .. versionadded:: v3.6

        Parameters
        ----------
        name: str
            name of the template.
        description: str
            description of the template.
        type: GuardType
            type of the template.
        allowed_stages: List[ModerationGuardStage]
            the stages of moderation this guard is allowed to be used
        ootb_type: ModerationGuardOotbType
            for guards of type "ootb", the specific "Out of the Box" metric type.
        llm_type:
            the backing LLM this guard uses.
        nemo_info
            additional configuration for NeMo Guardrails guards.
        model_info
            additional configuration for guards using a deployed model.
        intervention
            the assessment conditions, and action the guard should take if conditions are met.

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
        payload.update(exclude_if("type", type))
        payload.update(exclude_if("ootb_type", ootb_type))
        payload.update(exclude_if("llm_type", llm_type))
        if allowed_stages is not None:
            payload.update({"allowedStages": [x.value for x in self.allowed_stages]})
        if nemo_info is not None:
            payload.update({"nemoInfo": nemo_info.to_dict()})
        if model_info is not None:
            payload.update({"nemoInfo": model_info.to_dict()})
        if intervention is not None:
            payload.update({"intervention": intervention.to_dict()})

        response = self._client.patch(self._template_path(self.id), data=payload)
        data = response.json()
        new_version = self.from_server_data(data)
        self._update_values(new_version)

    def refresh(self: ModerationTemplate) -> None:
        """Update Template with the latest data from server.

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

    def delete(self: ModerationTemplate) -> None:
        """Delete Template.

        .. versionadded:: v3.6

        Raises
        ------
        datarobot.errors.ClientError
            If the server responded with 4xx status.
        datarobot.errors.ServerError
            If the server responded with 5xx status.
        """
        path = self._template_path(self.id)
        self._client.delete(path)
