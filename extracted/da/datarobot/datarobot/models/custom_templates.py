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

from io import BytesIO
import json
import os
from typing import Any, Dict, List, Optional
from zipfile import ZipFile

import trafaret as t

from datarobot.enums import ListCustomTemplatesSortQueryParams
from datarobot.models.api_object import APIObject
from datarobot.utils import from_api, to_api
from datarobot.utils.pagination import unpaginate


def file_content(file: str) -> bytes:
    """
    Converts a file/directory name (or byte string) to a byte string.

    When 'file' is a directory, the content is a ZIP of the directory.
    When 'file' is a file, the content is the file contents and should be a ZIP file (but not checked).
    Otherwise, the content is the encoded [assumed] string.
    """
    if os.path.isdir(file):
        temp_file = BytesIO()
        with ZipFile(temp_file, "w") as zipf:
            for dir_path, _, files in os.walk(file):
                for f in files:
                    fn = os.path.join(dir_path, f)
                    archive_path = os.path.relpath(fn, file)
                    zipf.write(fn, arcname=archive_path)
        content = temp_file.getvalue()
    elif os.path.isfile(file):
        with open(file, "rb") as fp:
            content = fp.read()
    else:
        content = bytes(file.encode("utf-8"))

    return content


def to_json_str(obj: Any) -> str:
    """
    Converts a Python object to a JSON string.

    This avoids redundant logic to convert APIObject|str|Any to a json encoded string.
    """
    if isinstance(obj, APIObject):
        api_obj = to_api(obj)
    elif isinstance(obj, str):
        api_obj = json.loads(obj)
    else:
        api_obj = obj
    return json.dumps(api_obj)


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
        custom_metric_metadata: Optional[CustomMetricMetadata] = None,
    ):
        self.readme = readme
        self.source = source
        self.tags = tags
        self.feature_flag = feature_flag
        self.preview_image = preview_image
        self.custom_metric_metadata = custom_metric_metadata


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
            t.Key("is_hidden", optional=True, default=None): t.Or(t.Bool(), t.Null()),
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
        is_hidden: bool,
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
        self.is_hidden = is_hidden

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, name={self.name!r})"

    @classmethod
    def create(
        cls,
        name: str,
        description: str,
        template_type: str,
        template_sub_type: str,
        template_metadata: TemplateMetadata | dict[str, Any] | str,
        default_environment: DefaultEnvironment | dict[str, Any] | str,
        file: str,
        default_resource_bundle_id: Optional[str] = None,
        enabled: Optional[bool] = None,
        is_hidden: Optional[bool] = None,
    ) -> CustomTemplate:
        """
        Create the custom template.

        .. versionadded:: v3.9

        Parameters
        ----------
        name: str
            The template name.
        description: str
            A description of the template.
        template_type: str
            The template type.
        template_sub_type: str
            The template sub-type.
        template_metadata: TemplateMetadata|dict[str, Any]|str
            The metadata associated with the template, provided as TemplateMetadata or a JSON-encoded string.
        default_environment: DefaultEnvironment|dict[str, Any]|str
            The default environment associated with the template, provided as DefaultEnvironment or a JSON-encoded
            string.
        file: str
            The path to the template directory or file, or the contents of the template.
        default_resource_bundle_id: Optional[str]
            The default resource bundle ID.
        enabled: Optional[bool]
            Whether the template is enabled (default is true).
        is_hidden: Optional[bool]
            Whether the template is hidden (default is false).

        Examples
        --------
        .. code-block:: python

            from datarobot import CustomTemplate
            from datarobot.models.custom_templates import DefaultEnvironment
            def_env = DefaultEnvironment(
                environment_id='679d47c8ce1ecd17326f3fdf',
                environment_version_id='679d47c8ce1ecd17326f3fe3',
            )
            template = template.create(
                name="My new template",
                default_environment=def_env,
                description='Updated template with environment v17',
            )
        """

        body = {}
        body["name"] = name
        body["description"] = description
        if default_resource_bundle_id:
            body["defaultResourceBundleId"] = default_resource_bundle_id
        body["templateType"] = template_type
        body["templateSubType"] = template_sub_type
        body["templateMetadata"] = to_json_str(template_metadata)
        body["defaultEnvironment"] = to_json_str(default_environment)
        if enabled is not None:
            body["enabled"] = str(enabled).lower()
        if is_hidden is not None:
            body["isHidden"] = str(is_hidden).lower()

        url = f"{cls._path}/"
        response = cls._client.build_request_with_file(
            method="POST",
            url=url,
            form_data=body,
            fname="template-content",
            content=file_content(file),
        )

        # the create response only has the customTemplateId, so use that to fetch the object
        template_id = response.json().get("customTemplateId")
        return CustomTemplate.get(template_id)

    @classmethod
    def list(
        cls,
        search: Optional[str] = None,
        order_by: Optional[ListCustomTemplatesSortQueryParams] = None,
        tag: Optional[str] = None,
        template_type: Optional[str] = None,
        template_sub_type: Optional[str] = None,
        publisher: Optional[str] = None,
        category: Optional[str] = None,
        show_hidden: Optional[bool] = None,
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
        publisher: Optional[str]
            Only return custom templates with this publisher.
        category: Optional[str]
            Only return custom templates with this category (use case).
        show_hidden: Optional[bool]
            Whether the template is hidden (default is false).
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
        if publisher:
            params["publisher"] = publisher
        if category:
            params["category"] = category
        if show_hidden is not None:
            params["showHidden"] = show_hidden
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
        file: Optional[str] = None,
        enabled: Optional[bool] = None,
        is_hidden: Optional[bool] = None,
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
        file: str
            The path to the template directory or file, or the contents of the template.
        enabled: Optional[bool]
            Whether the template is enabled (default is true).
        is_hidden: Optional[bool]
            Whether the template is hidden (default is false).

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
                _template_meta_obj = from_api(api_obj)  # type: ignore[arg-type]
                template_metadata = json.dumps(api_obj)
            else:
                _template_meta_obj = from_api(json.loads(template_metadata))
            body["templateMetadata"] = template_metadata
        if default_environment:
            if isinstance(default_environment, DefaultEnvironment):
                api_obj = to_api(default_environment)
                _default_env_obj = from_api(api_obj)  # type: ignore[arg-type]
                default_environment = json.dumps(api_obj)
            else:
                _default_env_obj = from_api(json.loads(default_environment))
            body["defaultEnvironment"] = default_environment
        if enabled is not None:
            body["enabled"] = str(enabled).lower()
        if is_hidden is not None:
            body["isHidden"] = str(is_hidden).lower()

        if not body and not file:
            raise ValueError("Nothing to update")

        url = f"{self._path}{self.id}/"
        items = None
        if not file:
            self._client.patch(url, data=body)
        else:
            response = self._client.build_request_with_file(
                method="PATCH",
                url=url,
                form_data=body,
                fname="template-content",
                content=file_content(file),
            )
            updated = self.from_server_data(response.json())
            items = updated.items

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
        if enabled is not None:
            self.enabled = enabled
        if is_hidden is not None:
            self.is_hidden = is_hidden
        if items is not None:
            self.items = items

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

    def download_content(
        self, index: Optional[int] = None, filename: Optional[str] = None
    ) -> Optional[bytes]:
        """
        Retrieve the file content for the given item.

        The item can be identified by filename or index in the array of items.

        .. versionadded:: v3.9

        Parameters
        ----------
        filename: Optional[str]
            The file name to retrieve.
        index: Optional[int]
            Index of the item to retrieve.

        Returns
        -------
        Bytes content of the file.
        """
        item = None
        if index is not None:
            if index > len(self.items):
                raise ValueError(
                    f"Index out of range -- only {len(self.items)} items are available"
                )
            item = self.items[index]
        elif filename is not None:
            item = next((i for i in self.items if i.get("name") == filename), None)
            if not item:
                names = [str(_item.get("name")) for _item in self.items]
                raise ValueError(f"File {filename} not found in: {', '.join(names)}")
        elif len(self.items) == 1:
            item = self.items[0]
        else:
            raise ValueError("Item must be specified by index or filename")

        url = f"{self._path}{self.id}/files/{item.get('id')}/"
        resp = self._client.get(url)
        return str(resp.json().get("content")).encode("utf-8") if resp.ok else None
