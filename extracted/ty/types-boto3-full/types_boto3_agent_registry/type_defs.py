"""
Type annotations for agent-registry service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_agent_registry/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_agent_registry.type_defs import BatchGetDiscoverableRegistryRecordErrorTypeDef

    data: BatchGetDiscoverableRegistryRecordErrorTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any

from .literals import (
    BatchGetDiscoverableRegistryRecordErrorCodeType,
    RecordTypeType,
    RegistryRecordFilterNameType,
    RegistryRecordStatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "A2aAgentCardDescriptorTypeDef",
    "AgUiDescriptorTypeDef",
    "AgentSkillsAdditionalDataTypeDef",
    "AgentSkillsDefinitionDescriptorTypeDef",
    "AgentSkillsMdDescriptorTypeDef",
    "BatchGetDiscoverableRegistryRecordErrorTypeDef",
    "BatchGetDiscoverableRegistryRecordRequestTypeDef",
    "BatchGetDiscoverableRegistryRecordResponseTypeDef",
    "CustomDescriptorTypeDef",
    "DescriptorSourceFromUrlTypeDef",
    "DescriptorSourceTypeDef",
    "DescriptorsTypeDef",
    "DiscoverableRegistryRecordSummaryTypeDef",
    "HttpDescriptorTypeDef",
    "ListDiscoverableRegistryRecordsRequestPaginateTypeDef",
    "ListDiscoverableRegistryRecordsRequestTypeDef",
    "ListDiscoverableRegistryRecordsResponseTypeDef",
    "McpServerAdditionalDataTypeDef",
    "McpServerDescriptorTypeDef",
    "McpToolsDescriptorTypeDef",
    "PaginatorConfigTypeDef",
    "RegistryRecordFilterTypeDef",
    "RegistryRecordSummaryTypeDef",
    "RegistryRecordsEntryTypeDef",
    "ResponseMetadataTypeDef",
    "SearchDiscoverableRegistryRecordsRequestTypeDef",
    "SearchDiscoverableRegistryRecordsResponseTypeDef",
)


class BatchGetDiscoverableRegistryRecordErrorTypeDef(TypedDict):
    registryId: str
    recordId: str
    errorCode: BatchGetDiscoverableRegistryRecordErrorCodeType
    message: NotRequired[str]


class RegistryRecordsEntryTypeDef(TypedDict):
    registryId: str
    recordIds: Sequence[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CustomDescriptorTypeDef(TypedDict):
    data: NotRequired[str]


class DescriptorSourceFromUrlTypeDef(TypedDict):
    url: str


class DiscoverableRegistryRecordSummaryTypeDef(TypedDict):
    registryArn: str
    recordArn: str
    recordId: str
    name: str
    recordType: RecordTypeType
    recordVersion: str
    status: RegistryRecordStatusType
    createdAt: datetime
    updatedAt: datetime
    description: NotRequired[str]
    displayName: NotRequired[str]
    descriptorTypes: NotRequired[list[str]]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class RegistryRecordFilterTypeDef(TypedDict):
    name: RegistryRecordFilterNameType
    values: Sequence[str]


class McpToolsDescriptorTypeDef(TypedDict):
    data: NotRequired[str]
    dataSchemaVersion: NotRequired[str]


class SearchDiscoverableRegistryRecordsRequestTypeDef(TypedDict):
    searchQuery: str
    registryIds: Sequence[str]
    maxResults: NotRequired[int]
    filters: NotRequired[Mapping[str, Any]]


class BatchGetDiscoverableRegistryRecordRequestTypeDef(TypedDict):
    entries: Sequence[RegistryRecordsEntryTypeDef]


class DescriptorSourceTypeDef(TypedDict):
    fromUrl: NotRequired[DescriptorSourceFromUrlTypeDef]


class ListDiscoverableRegistryRecordsResponseTypeDef(TypedDict):
    registryRecords: list[DiscoverableRegistryRecordSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListDiscoverableRegistryRecordsRequestPaginateTypeDef(TypedDict):
    registryId: str
    filters: NotRequired[Sequence[RegistryRecordFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDiscoverableRegistryRecordsRequestTypeDef(TypedDict):
    registryId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    filters: NotRequired[Sequence[RegistryRecordFilterTypeDef]]


class McpServerAdditionalDataTypeDef(TypedDict):
    tools: NotRequired[McpToolsDescriptorTypeDef]


class A2aAgentCardDescriptorTypeDef(TypedDict):
    data: NotRequired[str]
    dataSchemaVersion: NotRequired[str]
    source: NotRequired[DescriptorSourceTypeDef]


class AgUiDescriptorTypeDef(TypedDict):
    source: NotRequired[DescriptorSourceTypeDef]


class AgentSkillsMdDescriptorTypeDef(TypedDict):
    data: NotRequired[str]
    dataSchemaVersion: NotRequired[str]
    source: NotRequired[DescriptorSourceTypeDef]


class HttpDescriptorTypeDef(TypedDict):
    source: NotRequired[DescriptorSourceTypeDef]


class McpServerDescriptorTypeDef(TypedDict):
    data: NotRequired[str]
    dataSchemaVersion: NotRequired[str]
    additionalData: NotRequired[McpServerAdditionalDataTypeDef]
    source: NotRequired[DescriptorSourceTypeDef]


class AgentSkillsAdditionalDataTypeDef(TypedDict):
    skillMd: NotRequired[AgentSkillsMdDescriptorTypeDef]


class AgentSkillsDefinitionDescriptorTypeDef(TypedDict):
    data: NotRequired[str]
    dataSchemaVersion: NotRequired[str]
    additionalData: NotRequired[AgentSkillsAdditionalDataTypeDef]


class DescriptorsTypeDef(TypedDict):
    mcpServer: NotRequired[McpServerDescriptorTypeDef]
    a2aAgentCard: NotRequired[A2aAgentCardDescriptorTypeDef]
    agentSkillsDefinition: NotRequired[AgentSkillsDefinitionDescriptorTypeDef]
    custom: NotRequired[CustomDescriptorTypeDef]
    http: NotRequired[HttpDescriptorTypeDef]
    agui: NotRequired[AgUiDescriptorTypeDef]


class RegistryRecordSummaryTypeDef(TypedDict):
    registryArn: str
    recordArn: str
    recordId: str
    name: str
    recordType: RecordTypeType
    descriptors: DescriptorsTypeDef
    recordVersion: str
    status: RegistryRecordStatusType
    createdAt: datetime
    updatedAt: datetime
    description: NotRequired[str]
    displayName: NotRequired[str]


class BatchGetDiscoverableRegistryRecordResponseTypeDef(TypedDict):
    registryRecords: list[RegistryRecordSummaryTypeDef]
    errors: list[BatchGetDiscoverableRegistryRecordErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class SearchDiscoverableRegistryRecordsResponseTypeDef(TypedDict):
    registryRecords: list[RegistryRecordSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
