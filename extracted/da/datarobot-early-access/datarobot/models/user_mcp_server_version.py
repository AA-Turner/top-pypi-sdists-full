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

ROOT_RESTFUL_PATH = "userMCPServerVersions"


DEFAULT_BATCH_SIZE = 100


class TypeOfToolInUserMCPServerVersion(EnumAPIRepresentationConverter):
    """Supported types of tools associated with one user MCP server version

    USER_TOOL
        A tool created as a mcp tool decorated python function within the user MCP server.
    BUILT_IN_TOOL
        A DataRobot Predictive AI tool or wrapper tool of external service (e.g., github).
    """

    USER_TOOL = auto()
    BUILT_IN_TOOL = auto()


class TypeOfPromptInUserMCPServerVersion(EnumAPIRepresentationConverter):
    """Supported types of prompts associated with one user MCP server version

    USER_PROMPT_TEMPLATE
        A prompt template created as a mcp prompt decorated function within the user MCP server.
    """

    USER_PROMPT_TEMPLATE = auto()


class TypeOfResourceInUserMCPServerVersion(EnumAPIRepresentationConverter):
    """Supported types of resources associated with one user MCP server version

    USER_RESOURCE
        A resource created as a mcp resource decorated function within the user MCP server.
    """

    USER_RESOURCE = auto()


class ToolInUserMCPServerVersion(APIObject):
    """A tool registered in one MCP server version. It is used to:
    - List tools registered in one MCP server version.

    Attributes
    ----------
    id: str
        The identifier of tool.
    name: str
        The tool name.
    type: str
        The tool type. It is a camelized string representation of TypeOfToolInUserMCPServerVersion
    created_at: str
        Datetime when the tool is created.
        It is formatted as RFC3339 UTC, e.g. 2026-02-24T19:12:48.285320Z
    user_id: bool
        The identifier of user who created the tool.
    user_name: str
        The name of user who created the tool.
    mcp_server_version_id: str
        The identifier of MCP server version (custom model version) under which the tool
        is registered.
    """

    _url_template = ROOT_RESTFUL_PATH + "/{mcp_server_version_id}/tools/"

    _converter = t.Dict({
        t.Key("id"): t.String(),
        t.Key("name"): t.String(),
        t.Key("type"): t.Enum(*[el.to_api_representation() for el in TypeOfToolInUserMCPServerVersion]),
        t.Key("created_at"): t.String(),
        t.Key("user_id"): t.String(),
        t.Key("user_name"): t.String(),
        t.Key("mcp_server_version_id"): t.String(),
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
        mcp_server_version_id: str,
    ) -> None:
        self.id = id
        self.name = name
        self.type: TypeOfToolInUserMCPServerVersion = TypeOfToolInUserMCPServerVersion.from_api_representation(type)
        self.created_at = created_at
        self.user_id = user_id
        self.user_name = user_name
        self.mcp_server_version_id = mcp_server_version_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name: {self.name!r}, type: {self.type!r})"

    @classmethod
    def list(
        cls,
        mcp_server_version_id: str,
        offset: int = 0,
        limit: int = 10,
    ) -> List["ToolInUserMCPServerVersion"]:
        """Get a list of MCP tools.

        Parameters
        ----------
        mcp_server_version_id: str
            The identifier of MCP server version (custom model version) under which the tool
            is registered.
        offset: int
            The offset of the query.
        limit: int
            The limit of returned MCP tool.

        Returns
        -------
        List[ToolInUserMCPServerVersion]
            A list of MCP tools.
        """
        query_params = {"offset": offset, "limit": limit}
        url_path = cls._url_template.format(mcp_server_version_id=mcp_server_version_id)
        list_of_resources = (
            unpaginate(url_path, {"offset": offset, "limit": DEFAULT_BATCH_SIZE}, cls._client)
            if limit == 0
            else cls._client.get(url_path, params=query_params).json()["data"]
        )

        return [cls.from_server_data(resource) for resource in list_of_resources]


class PromptInUserMCPServerVersion(APIObject):
    """A prompt registered in one MCP server version. It is used to:
    - List prompts registered in one MCP server version.

    Attributes
    ----------
    id: str
        The identifier of prompt.
    name: str
        The prompt name.
    type: str
        The prompt type. It is a camelized string representation of TypeOfPromptInUserMCPServerVersion.
    created_at: str
        Datetime when the prompt is created.
        It is formatted as RFC3339 UTC, e.g. 2026-02-24T19:12:48.285320Z
    user_id: bool
        The identifier of user who created the prompt.
    user_name: str
        The name of user who created the prompt.
    mcp_server_version_id: str
        The identifier of MCP server version (custom model version) under which the prompt
        is registered.
    """

    _url_template = ROOT_RESTFUL_PATH + "/{mcp_server_version_id}/prompts/"

    _converter = t.Dict({
        t.Key("id"): t.String(),
        t.Key("name"): t.String(),
        t.Key("type"): t.Enum(*[el.to_api_representation() for el in TypeOfPromptInUserMCPServerVersion]),
        t.Key("created_at"): t.String(),
        t.Key("user_id"): t.String(),
        t.Key("user_name"): t.String(),
        t.Key("mcp_server_version_id"): t.String(),
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
        mcp_server_version_id: str,
    ) -> None:
        self.id = id
        self.name = name
        self.type: TypeOfPromptInUserMCPServerVersion = TypeOfPromptInUserMCPServerVersion.from_api_representation(type)
        self.created_at = created_at
        self.user_id = user_id
        self.user_name = user_name
        self.mcp_server_version_id = mcp_server_version_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name: {self.name!r}, type: {self.type!r})"

    @classmethod
    def list(
        cls,
        mcp_server_version_id: str,
        offset: int = 0,
        limit: int = 10,
    ) -> List["PromptInUserMCPServerVersion"]:
        """Get a list of MCP prompts.

        Parameters
        ----------
        mcp_server_version_id: str
            The identifier of MCP server version (custom model version) under which the prompt
            is registered.
        offset: int
            The offset of the query.
        limit: int
            The limit of returned MCP prompt.

        Returns
        -------
        List[PromptInUserMCPServerVersion]
            A list of MCP prompts.
        """
        query_params = {"offset": offset, "limit": limit}
        url_path = cls._url_template.format(mcp_server_version_id=mcp_server_version_id)
        list_of_resources = (
            unpaginate(url_path, {"offset": offset, "limit": DEFAULT_BATCH_SIZE}, cls._client)
            if limit == 0
            else cls._client.get(url_path, params=query_params).json()["data"]
        )

        return [cls.from_server_data(resource) for resource in list_of_resources]


class ResourceInUserMCPServerVersion(APIObject):
    """A resource registered in one MCP server version. It is used to:
    - List resources registered in one MCP server version.

    Attributes
    ----------
    id: str
        The identifier of resource.
    name: str
        The resource name.
    type: str
        The resource type. It is a camelized string representation of TypeOfResourceInUserMCPServerVersion.
    uri: str
        The resource URI.
    created_at: str
        Datetime when the resource is created.
        It is formatted as RFC3339 UTC, e.g. 2026-02-24T19:12:48.285320Z
    user_id: bool
        The identifier of user who created the resource.
    user_name: str
        The name of user who created the resource.
    mcp_server_version_id: str
        The identifier of MCP server version (custom model version) under which the resource
        is registered.
    """

    _url_template = ROOT_RESTFUL_PATH + "/{mcp_server_version_id}/resources/"

    _converter = t.Dict({
        t.Key("id"): t.String(),
        t.Key("name"): t.String(),
        t.Key("uri"): t.String(),
        t.Key("type"): t.Enum(*[el.to_api_representation() for el in TypeOfResourceInUserMCPServerVersion]),
        t.Key("created_at"): t.String(),
        t.Key("user_id"): t.String(),
        t.Key("user_name"): t.String(),
        t.Key("mcp_server_version_id"): t.String(),
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
        mcp_server_version_id: str,
    ) -> None:
        self.id = id
        self.name = name
        self.type: TypeOfResourceInUserMCPServerVersion = TypeOfResourceInUserMCPServerVersion.from_api_representation(
            type
        )
        self.uri = uri
        self.created_at = created_at
        self.user_id = user_id
        self.user_name = user_name
        self.mcp_server_version_id = mcp_server_version_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name: {self.name!r}, type: {self.type!r})"

    @classmethod
    def list(
        cls,
        mcp_server_version_id: str,
        offset: int = 0,
        limit: int = 10,
    ) -> List["ResourceInUserMCPServerVersion"]:
        """Get a list of MCP resources.

        Parameters
        ----------
        mcp_server_version_id: str
            The identifier of MCP server version (custom model version) under which the resource
            is registered.
        offset: int
            The offset of the query.
        limit: int
            The limit of returned MCP resource.

        Returns
        -------
        List[ResourceInUserMCPServerVersion]
            A list of MCP resources.
        """
        query_params = {"offset": offset, "limit": limit}
        url_path = cls._url_template.format(mcp_server_version_id=mcp_server_version_id)
        list_of_resources = (
            unpaginate(url_path, {"offset": offset, "limit": DEFAULT_BATCH_SIZE}, cls._client)
            if limit == 0
            else cls._client.get(url_path, params=query_params).json()["data"]
        )

        return [cls.from_server_data(resource) for resource in list_of_resources]
