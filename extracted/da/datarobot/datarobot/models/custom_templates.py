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

import json
from typing import Any, Dict, List, Optional

import trafaret as t

from datarobot.enums import ListCustomTemplatesSortQueryParams
from datarobot.models.api_object import APIObject
from datarobot.utils import _from_api_dict, to_api
from datarobot.utils.pagination import unpaginate


class DefaultEnvironment(APIObject):
    """
    Default execution environment.
    """

    _converter = t.Dict(
        {
            t.Key("environment_id"): t.String(),
            t.Key("environment_version_id"): t.String(),
        }
    ).ignore_extra("*")
    schema = _converter

    def __init__(self, environment_id: str, environment_version_id: str):
        self.environment_id = environment_id
        self.environment_version_id = environment_version_id

    def __repr__(self) -> str:
        return "{}(environment_id={}, environment_version_id={})".format(
            self.__class__.__name__, self.environment_id, self.environment_version_id
        )


class CustomMetricMetadata(APIObject):
    """
    Metadata for custom metrics.
    """

    _converter = t.Dict(
        {
            # NOTE: several values are really enums, but treated as strings for simplicity
            t.Key("units"): t.String(),
            t.Key("directionality"): t.String(),
            t.Key("type"): t.String(),
            t.Key("time_step"): t.String(),
            t.Key("is_model_specific"): t.Bool(),
            t.Key("template_metric_type", optional=True): t.Or(t.Null(), t.String()),
        }
    ).ignore_extra("*")
    schema = _converter

    def __init__(
        self,
        units: str,
        directionality: str,
        type: str,
        time_step: str,
        is_model_specific: bool,
        template_metric_type: Optional[str] = None,
    ):
        self.units = units
        self.directionality = directionality
        self.type = type
        self.time_step = time_step
        self.is_model_specific = is_model_specific
        self.template_metric_type = template_metric_type


class TemplateMetadata(APIObject):
    """
    Metadata for the custom templates.
    """

    _converter = t.Dict(
        {
            t.Key("readme", optional=True): t.Or(t.Null(), t.String()),
            t.Key("source", optional=True): t.Or(t.Null(), t.Dict().allow_extra("*")),
            t.Key("tags", optional=True): t.List(t.String()),
            t.Key("custom_metric_metadata", optional=True): t.Or(
                t.Null(), CustomMetricMetadata.schema
            ),
            t.Key("feature_flag", optional=True): t.Or(t.Null(), t.String()),
            t.Key("preview_image", optional=True): t.Or(t.Null(), t.String()),
        }
    ).ignore_extra("*")
    schema = _converter

    def __init__(
        self,
        readme: Optional[str] = None,
        source: Optional[str] = None,
        tags: Optional[List[str]] = None,
        feature_flag: Optional[str] = None,
        preview_image: Optional[str] = None,
    ):
        self.readme = readme
        self.source = source
        self.tags = tags
        self.feature_flag = feature_flag
        self.preview_image = preview_image


class CustomTemplate(APIObject):
    """
    Template for custom activity (e.g. custom-metrics, applications).
    """

    _path = "customTemplates/"

    _converter = t.Dict(
        {
            t.Key("default_environment"): DefaultEnvironment.schema,
            t.Key("default_resource_bundle_id", optional=True, default=None): t.Or(
                t.Null(), t.String()
            ),
            t.Key("description"): t.String(),
            t.Key("enabled"): t.Bool(),
            t.Key("id"): t.String(),
            t.Key("items"): t.List(t.Dict().allow_extra("*")),
            t.Key("name"): t.String(),
            t.Key("template_metadata"): TemplateMetadata.schema,
            t.Key("template_sub_type"): t.String(),
            t.Key("template_type"): t.String(),
        }
    ).ignore_extra("*")

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        template_metadata: Dict[str, Any],
        default_environment: Dict[str, Any],
        default_resource_bundle_id: Optional[str],
        items: List[Dict[str, Any]],
        template_type: str,
        template_sub_type: str,
        enabled: bool,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.template_metadata = template_metadata
        self.default_environment = default_environment
        self.default_resource_bundle_id = default_resource_bundle_id
        self.items = items
        self.template_type = template_type
        self.template_sub_type = template_sub_type
        self.enabled = enabled

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, name={self.name!r})"

    @classmethod
    def list(
        cls,
        search: Optional[str] = None,
        order_by: Optional[ListCustomTemplatesSortQueryParams] = None,
        tag: Optional[str] = None,
        template_type: Optional[str] = None,
        template_sub_type: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[CustomTemplate]:
        """List all custom templates.

        .. versionadded:: v3.7

        Parameters
        ----------
        search: Optional[str]
            Search string.
        order_by: Optional[ListCustomTemplatesSortQueryParams]
            Ordering field.
        tag: Optional[str]
            Tag associated with the template.
        template_type: Optional[str]
            Type of the template.
        template_type: Optional[str]
            Sub-type of the template.
        offset: Optional[int]
            Offset for pagination.
        limit: Optional[int]
            Limit for pagination.

        Returns
        -------
        templates: List[CustomTemplate]
        """
        params: Dict[str, Any] = {}
        if search:
            params["search"] = search
        if order_by:
            params["orderBy"] = order_by
        if tag:
            params["tag"] = tag
        if template_type:
            params["templateType"] = template_type
        if template_sub_type:
            params["templateSubType"] = template_sub_type
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit

        if offset is None:
            data = unpaginate(cls._path, params, cls._client)
        else:
            data = cls._client.get(cls._path, params=params if params else None).json()["data"]
        return [cls.from_server_data(d) for d in data]

    @classmethod
    def get(cls, template_id: str) -> CustomTemplate:
        """Get a custom template by ID.

        .. versionadded:: v3.7

        Parameters
        ----------
        template_id: str
            ID of the template.

        Returns
        -------
        template : CustomTemplate
        """
        response = cls._client.get(f"{cls._path}{template_id}/")
        return cls.from_server_data(response.json())

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        default_resource_bundle_id: Optional[str] = None,
        template_type: Optional[str] = None,
        template_sub_type: Optional[str] = None,
        template_metadata: Optional[TemplateMetadata | str] = None,
        default_environment: Optional[DefaultEnvironment | str] = None,
    ) -> None:
        """
        Update the custom template.

        .. versionadded:: v3.7

        Parameters
        ----------
        name: Optional[str]
            The template name.
        description: Optional[str]
            A description of the template.
        default_resource_bundle_id: Optional[str]
            The default resource bundle ID.
        template_type: Optional[str]
            The template type.
        template_sub_type: Optional[str]
            The template sub-type.
        template_metadata: Optional[TemplateMetadata|str]
            The metadata associated with the template, provided as TemplateMetadata or a JSON encoded string.
        default_environment: Optional[DefaultEnvironment|str]
            The default environment associated with the template, provided as DefaultEnvironment or a JSON encoded
            string.

        Examples
        --------
        .. code-block:: python

            from datarobot import CustomTemplate
            from datarobot.models.custom_templates import DefaultEnvironment
            new_env = DefaultEnvironment(
                environment_id='679d47c8ce1ecd17326f3fdf',
                environment_version_id='679d47c8ce1ecd17326f3fe3',
            )
            template = CustomTemplate.get(template_id='5c939e08962d741e34f609f0')
            template.update(default_environment=new_env, description='Updated template with environment v17')
        """

        _default_env_obj: Any = None
        _template_meta_obj: Any = None
        body = {}
        if name:
            body["name"] = name
        if description:
            body["description"] = description
        if default_resource_bundle_id:
            body["defaultResourceBundleId"] = default_resource_bundle_id
        if template_type:
            body["templateType"] = template_type
        if template_sub_type:
            body["templateSubType"] = template_sub_type
        if template_metadata:
            if isinstance(template_metadata, TemplateMetadata):
                api_obj = to_api(template_metadata)
                _template_meta_obj = _from_api_dict(api_obj)  # type: ignore[arg-type]
                template_metadata = json.dumps(api_obj)
            else:
                _template_meta_obj = _from_api_dict(json.loads(template_metadata))
            body["templateMetadata"] = template_metadata
        if default_environment:
            if isinstance(default_environment, DefaultEnvironment):
                api_obj = to_api(default_environment)
                _default_env_obj = _from_api_dict(api_obj)  # type: ignore[arg-type]
                default_environment = json.dumps(api_obj)
            else:
                _default_env_obj = _from_api_dict(json.loads(default_environment))
            body["defaultEnvironment"] = default_environment
        if not body:
            raise ValueError("Nothing to update")

        url = f"{self._path}{self.id}/"
        self._client.patch(url, data=body)

        # update the local data
        if name:
            self.name = name
        if description:
            self.description = description
        if default_resource_bundle_id:
            self.default_resource_bundle_id = default_resource_bundle_id
        if template_type:
            self.template_type = template_type
        if template_sub_type:
            self.template_sub_type = template_sub_type
        if _template_meta_obj:
            self.template_metadata = _template_meta_obj
        if _default_env_obj:
            self.default_environment = _default_env_obj

    def delete(self) -> None:
        """
        Delete this custom template.

        .. versionadded:: v3.7

        Returns
        -------
        None
        """

        url = f"{self._path}{self.id}/"
        self._client.delete(url)
