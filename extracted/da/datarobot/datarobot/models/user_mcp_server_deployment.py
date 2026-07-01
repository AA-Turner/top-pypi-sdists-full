#
# Copyright 2024-2026 DataRobot, Inc. and its affiliates.
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

from enum import auto
from typing import List

import trafaret as t

from datarobot.models.api_object import APIObject
from datarobot.models.enums import EnumAPIRepresentationConverter
from datarobot.utils.pagination import unpaginate

ROOT_RESTFUL_PATH = "userMCPServerDeployments"

DEFAULT_BATCH_SIZE = 100


class TypeOfToolInUserMCPServerDeployment(EnumAPIRepresentationConverter):
    """Supported types of tools in one user MCP server deployment

    USER_TOOL
        A tool created as an MCP tool decorated Python function within the user MCP server.
    BUILT_IN_TOOL
        A DataRobot Predictive AI tool or wrapper tool of external service (e.g., GitHub).
    USER_TOOL_DEPLOYMENT
        A tool created as a custom inference model.
    """

    USER_TOOL = auto()
    BUILT_IN_TOOL = auto()
    USER_TOOL_DEPLOYMENT = auto()


class TypeOfPromptInUserMCPServerDeployment(EnumAPIRepresentationConverter):
    """Supported types of prompts in one user MCP server deployment

    USER_PROMPT_TEMPLATE
        A prompt template created as an MCP prompt decorated function within the user MCP server.
    USER_PROMPT_TEMPLATE_VERSION
        A prompt template created and registered in DataRobot.
    """

    USER_PROMPT_TEMPLATE = auto()
    USER_PROMPT_TEMPLATE_VERSION = auto()


class TypeOfResourceInUserMCPServerDeployment(EnumAPIRepresentationConverter):
    """Supported types of resources in one user MCP server deployment

    USER_RESOURCE
        A resource created as an MCP resource decorated function within the user MCP server.
    """

    USER_RESOURCE = auto()


class ToolInUserMCPServerDeployment(APIObject):
    """A tool registered in one MCP server deployment. It is used to:
    - Create one tool and register it in one MCP server deployment.
    - List tools registered in one MCP server deployment.

    Attributes
    ----------
    id: str
        The identifier of tool.
    name: str
        The tool name.
    type: str
        The tool type. It is a camelCase string representation of TypeOfToolInUserMCPServerDeployment.
    created_at: str
        Datetime when the tool is created.
        It is formatted as RFC3339 UTC, e.g., 2026-02-24T19:12:48.285320Z.
    user_id: bool
        The identifier of user who created the tool.
    user_name: str
        The name of user who created the tool.
    mcp_server_deployment_id: str
        The identifier of MCP server deployment (custom model deployment) under which the tool
        is registered.
    """

    _url_template = ROOT_RESTFUL_PATH + "/{mcp_server_deployment_id}/tools/"

    _converter = t.Dict({
        t.Key("id"): t.String(),
        t.Key("name"): t.String(),
        t.Key("type"): t.Enum(*[el.to_api_representation() for el in TypeOfToolInUserMCPServerDeployment]),
        t.Key("created_at"): t.String(),
        t.Key("user_id"): t.String(),
        t.Key("user_name"): t.String(),
        t.Key("mcp_server_deployment_id"): t.String(),
    }).ignore_extra("*")

    schema = _converter

    def __init__(
        self,
        id: str,
        name: str,
        type: str,
        created_at: str,
        user_id: str,
        user_name: str,
        mcp_server_deployment_id: str,
    ) -> None:
        self.id = id
        self.name = name
        self.type: TypeOfToolInUserMCPServerDeployment = TypeOfToolInUserMCPServerDeployment.from_api_representation(
            type
        )
        self.created_at = created_at
        self.user_id = user_id
        self.user_name = user_name
        self.mcp_server_deployment_id = mcp_server_deployment_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name: {self.name!r}, type: {self.type!r})"

    @classmethod
    def create(
        cls,
        mcp_server_deployment_id: str,
        name: str,
        type: TypeOfToolInUserMCPServerDeployment,
    ) -> "ToolInUserMCPServerDeployment":
        """Create a new MCP tool and return it.

        Parameters
        ----------
        mcp_server_deployment_id: str
            The identifier of MCP server deployment (custom model deployment) under which the tool
            is registered.
        name: str
            The tool name.
        type: TypeOfToolInUserMCPServerDeployment
            The tool type.

        Returns
        -------
        ToolInUserMCPServerDeployment
            The created MCP tool.
        """

        url_path = cls._url_template.format(mcp_server_deployment_id=mcp_server_deployment_id)
        request_payload = {
            "name": name,
            "type": type.to_api_representation(),
        }

        data = cls._client.post(
            url_path,
            json=request_payload,
        ).json()

        return cls.from_server_data(data)

    @classmethod
    def list(
        cls,
        mcp_server_deployment_id: str,
        offset: int = 0,
        limit: int = 10,
    ) -> List["ToolInUserMCPServerDeployment"]:
        """Get a list of MCP tools.

        Parameters
        ----------
        mcp_server_deployment_id: str
            The identifier of MCP server deployment (custom model deployment) under which the tool
            is registered.
        offset: int
            The offset of the query.
        limit: int
            The limit of returned MCP tool.

        Returns
        -------
        List[ToolInUserMCPServerDeployment]
            A list of MCP tools.
        """
        query_params = {"offset": offset, "limit": limit}
        url_path = cls._url_template.format(mcp_server_deployment_id=mcp_server_deployment_id)
        list_of_resources = (
            unpaginate(url_path, {"offset": offset, "limit": DEFAULT_BATCH_SIZE}, cls._client)
            if limit == 0
            else cls._client.get(url_path, params=query_params).json()["data"]
        )

        return [cls.from_server_data(resource) for resource in list_of_resources]

    def delete(self) -> None:
        """Delete a MCP tool."""
        url_path = self._url_template.format(mcp_server_deployment_id=self.mcp_server_deployment_id) + f"{self.id}/"
        self._client.delete(url_path)


class PromptInUserMCPServerDeployment(APIObject):
    """A prompt registered in one MCP server deployment. It is used to:
    - Create one prompt and register it in one MCP server deployment.
    - List tools registered in one MCP server deployment.

    Attributes
    ----------
    id: str
        The identifier of prompt.
    name: str
        The prompt name.
    type: str
        The prompt type. It is a camelCase string representation of TypeOfPromptInUserMCPServerDeployment.
    created_at: str
        Datetime when the prompt is created.
        It is formatted as RFC3339 UTC, e.g., 2026-02-24T19:12:48.285320Z.
    user_id: bool
        The identifier of user who created the prompt.
    user_name: str
        The name of user who created the prompt.
    mcp_server_deployment_id: str
        The identifier of MCP server deployment (custom model deployment) under which the prompt
        is registered.
    """

    _url_template = ROOT_RESTFUL_PATH + "/{mcp_server_deployment_id}/prompts/"

    _converter = t.Dict({
        t.Key("id"): t.String(),
        t.Key("name"): t.String(),
        t.Key("type"): t.Enum(*[el.to_api_representation() for el in TypeOfPromptInUserMCPServerDeployment]),
        t.Key("created_at"): t.String(),
        t.Key("user_id"): t.String(),
        t.Key("user_name"): t.String(),
        t.Key("mcp_server_deployment_id"): t.String(),
    }).ignore_extra("*")

    schema = _converter

    def __init__(
        self,
        id: str,
        name: str,
        type: str,
        created_at: str,
        user_id: str,
        user_name: str,
        mcp_server_deployment_id: str,
    ) -> None:
        self.id = id
        self.name = name
        self.type: TypeOfPromptInUserMCPServerDeployment = (
            TypeOfPromptInUserMCPServerDeployment.from_api_representation(type)
        )
        self.created_at = created_at
        self.user_id = user_id
        self.user_name = user_name
        self.mcp_server_deployment_id = mcp_server_deployment_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name: {self.name!r}, type: {self.type!r})"

    @classmethod
    def create(
        cls,
        mcp_server_deployment_id: str,
        name: str,
        type: TypeOfPromptInUserMCPServerDeployment,
    ) -> "PromptInUserMCPServerDeployment":
        """Create a new MCP prompt and return it.

        Parameters
        ----------
        mcp_server_deployment_id: str
            The identifier of MCP server deployment (custom model deployment) under which the prompt
            is registered.
        name: str
            The prompt name.
        type: TypeOfPromptInUserMCPServerDeployment
            The prompt type.

        Returns
        -------
        PromptInUserMCPServerDeployment
            The created MCP prompt.
        """

        url_path = cls._url_template.format(mcp_server_deployment_id=mcp_server_deployment_id)
        request_payload = {
            "name": name,
            "type": type.to_api_representation(),
        }

        data = cls._client.post(
            url_path,
            json=request_payload,
        ).json()

        return cls.from_server_data(data)

    @classmethod
    def list(
        cls,
        mcp_server_deployment_id: str,
        offset: int = 0,
        limit: int = 10,
    ) -> List["PromptInUserMCPServerDeployment"]:
        """Get a list of MCP prompts.

        Parameters
        ----------
        mcp_server_deployment_id: str
            The identifier of MCP server deployment (custom model deployment) under which the prompt
            is registered.
        offset: int
            The offset of the query.
        limit: int
            The limit of returned MCP prompt.

        Returns
        -------
        List[PromptInUserMCPServerDeployment]
            A list of MCP prompts.
        """
        query_params = {"offset": offset, "limit": limit}
        url_path = cls._url_template.format(mcp_server_deployment_id=mcp_server_deployment_id)
        list_of_resources = (
            unpaginate(url_path, {"offset": offset, "limit": DEFAULT_BATCH_SIZE}, cls._client)
            if limit == 0
            else cls._client.get(url_path, params=query_params).json()["data"]
        )

        return [cls.from_server_data(resource) for resource in list_of_resources]

    def delete(self) -> None:
        """Delete a MCP prompt."""
        url_path = self._url_template.format(mcp_server_deployment_id=self.mcp_server_deployment_id) + f"{self.id}/"
        self._client.delete(url_path)


class ResourceInUserMCPServerDeployment(APIObject):
    """A resource registered in one MCP server deployment. It is used to:
    - Create one resource and register it in one MCP server deployment.
    - List tools registered in one MCP server deployment.

    Attributes
    ----------
    id: str
        The identifier of resource.
    name: str
        The resource name.
    type: str
        The resource type. It is a camelCase string representation of TypeOfResourceInUserMCPServerDeployment.
    uri: str
        The resource URI.
    created_at: str
        Datetime when the resource is created.
        It is formatted as RFC3339 UTC, e.g., 2026-02-24T19:12:48.285320Z.
    user_id: bool
        The identifier of user who created the resource.
    user_name: str
        The name of user who created the resource.
    mcp_server_deployment_id: str
        The identifier of MCP server deployment (custom model deployment) under which the resource
        is registered.
    """

    _url_template = ROOT_RESTFUL_PATH + "/{mcp_server_deployment_id}/resources/"

    _converter = t.Dict({
        t.Key("id"): t.String(),
        t.Key("name"): t.String(),
        t.Key("uri"): t.String(),
        t.Key("type"): t.Enum(*[el.to_api_representation() for el in TypeOfResourceInUserMCPServerDeployment]),
        t.Key("created_at"): t.String(),
        t.Key("user_id"): t.String(),
        t.Key("user_name"): t.String(),
        t.Key("mcp_server_deployment_id"): t.String(),
    }).ignore_extra("*")

    schema = _converter

    def __init__(
        self,
        id: str,
        name: str,
        type: str,
        uri: str,
        created_at: str,
        user_id: str,
        user_name: str,
        mcp_server_deployment_id: str,
    ) -> None:
        self.id = id
        self.name = name
        self.type: TypeOfResourceInUserMCPServerDeployment = (
            TypeOfResourceInUserMCPServerDeployment.from_api_representation(type)
        )
        self.uri = uri
        self.created_at = created_at
        self.user_id = user_id
        self.user_name = user_name
        self.mcp_server_deployment_id = mcp_server_deployment_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name: {self.name!r}, type: {self.type!r})"

    @classmethod
    def create(
        cls,
        mcp_server_deployment_id: str,
        name: str,
        type: TypeOfResourceInUserMCPServerDeployment,
        uri: str,
    ) -> "ResourceInUserMCPServerDeployment":
        """Create a new MCP resource and return it.

        Parameters
        ----------
        mcp_server_deployment_id: str
            The identifier of MCP server deployment (custom model deployment) under which the resource
            is registered.
        name: str
            The resource name.
        type: TypeOfResourceInUserMCPServerDeployment
            The resource type.
        uri: str
            The resource URI.

        Returns
        -------
        ResourceInUserMCPServerDeployment
            The created MCP resource.
        """

        url_path = cls._url_template.format(mcp_server_deployment_id=mcp_server_deployment_id)
        request_payload = {
            "name": name,
            "type": type.to_api_representation(),
            "uri": uri,
        }

        data = cls._client.post(
            url_path,
            json=request_payload,
        ).json()

        return cls.from_server_data(data)

    @classmethod
    def list(
        cls,
        mcp_server_deployment_id: str,
        offset: int = 0,
        limit: int = 10,
    ) -> List["ResourceInUserMCPServerDeployment"]:
        """Get a list of MCP resources.

        Parameters
        ----------
        mcp_server_deployment_id: str
            The identifier of MCP server deployment (custom model deployment) under which the resource
            is registered.
        offset: int
            The offset of the query.
        limit: int
            The limit of returned MCP resource.

        Returns
        -------
        List[ResourceInUserMCPServerDeployment]
            A list of MCP resources.
        """
        query_params = {"offset": offset, "limit": limit}
        url_path = cls._url_template.format(mcp_server_deployment_id=mcp_server_deployment_id)
        list_of_resources = (
            unpaginate(url_path, {"offset": offset, "limit": DEFAULT_BATCH_SIZE}, cls._client)
            if limit == 0
            else cls._client.get(url_path, params=query_params).json()["data"]
        )

        return [cls.from_server_data(resource) for resource in list_of_resources]

    def delete(self) -> None:
        """Delete a MCP resource."""
        url_path = self._url_template.format(mcp_server_deployment_id=self.mcp_server_deployment_id) + f"{self.id}/"
        self._client.delete(url_path)
