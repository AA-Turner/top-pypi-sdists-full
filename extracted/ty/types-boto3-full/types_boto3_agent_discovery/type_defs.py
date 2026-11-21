"""
Type annotations for agent-discovery service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_agent_discovery/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_agent_discovery.type_defs import DescriptorSourceUrlTypeDef

    data: DescriptorSourceUrlTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from datetime import datetime
from typing import Any

from .literals import ProvenanceRelationType, RecordTypeType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "DescriptorEntryPaginatorTypeDef",
    "DescriptorEntryTypeDef",
    "DescriptorSourceTypeDef",
    "DescriptorSourceUrlTypeDef",
    "IdentifierTypeDef",
    "PaginatorConfigTypeDef",
    "ProvenanceLinkTypeDef",
    "PublicRecordPaginatorTypeDef",
    "PublicRecordTypeDef",
    "ResponseMetadataTypeDef",
    "SearchPublicRecordsRequestPaginateTypeDef",
    "SearchPublicRecordsRequestTypeDef",
    "SearchPublicRecordsResponsePaginatorTypeDef",
    "SearchPublicRecordsResponseTypeDef",
    "TrustManifestTypeDef",
)


class DescriptorSourceUrlTypeDef(TypedDict):
    url: str


class IdentifierTypeDef(TypedDict):
    domain: NotRequired[str]
    uri: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ProvenanceLinkTypeDef(TypedDict):
    relation: ProvenanceRelationType
    sourceId: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class SearchPublicRecordsRequestTypeDef(TypedDict):
    searchQuery: NotRequired[str]
    filters: NotRequired[Mapping[str, Any]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class DescriptorSourceTypeDef(TypedDict):
    fromUrl: NotRequired[DescriptorSourceUrlTypeDef]


class SearchPublicRecordsRequestPaginateTypeDef(TypedDict):
    searchQuery: NotRequired[str]
    filters: NotRequired[Mapping[str, Any]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class TrustManifestTypeDef(TypedDict):
    contributor: str
    provenance: NotRequired[list[ProvenanceLinkTypeDef]]


class DescriptorEntryPaginatorTypeDef(TypedDict):
    data: NotRequired[str]
    version: NotRequired[str]
    source: NotRequired[DescriptorSourceTypeDef]
    additionalData: NotRequired[dict[str, dict[str, Any]]]


class DescriptorEntryTypeDef(TypedDict):
    data: NotRequired[str]
    version: NotRequired[str]
    source: NotRequired[DescriptorSourceTypeDef]
    additionalData: NotRequired[dict[str, dict[str, Any]]]


class PublicRecordPaginatorTypeDef(TypedDict):
    identifier: IdentifierTypeDef
    displayName: str
    recordType: RecordTypeType
    description: NotRequired[str]
    domain: NotRequired[str]
    descriptors: NotRequired[dict[str, DescriptorEntryPaginatorTypeDef]]
    trustManifests: NotRequired[list[TrustManifestTypeDef]]
    recordVersion: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]


class PublicRecordTypeDef(TypedDict):
    identifier: IdentifierTypeDef
    displayName: str
    recordType: RecordTypeType
    description: NotRequired[str]
    domain: NotRequired[str]
    descriptors: NotRequired[dict[str, DescriptorEntryTypeDef]]
    trustManifests: NotRequired[list[TrustManifestTypeDef]]
    recordVersion: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]


class SearchPublicRecordsResponsePaginatorTypeDef(TypedDict):
    records: list[PublicRecordPaginatorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class SearchPublicRecordsResponseTypeDef(TypedDict):
    records: list[PublicRecordTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
