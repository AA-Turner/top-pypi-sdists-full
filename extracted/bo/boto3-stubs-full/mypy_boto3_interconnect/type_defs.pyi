"""
Type annotations for interconnect service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_interconnect/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_interconnect.type_defs import AttachPointTypeDef

    data: AttachPointTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence

from .literals import ConnectionStateType, EnvironmentStateType, RemoteAccountIdentifierTypeType

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AcceptConnectionProposalRequestTypeDef",
    "AcceptConnectionProposalResponseTypeDef",
    "AttachPointDescriptorTypeDef",
    "AttachPointTypeDef",
    "BandwidthsTypeDef",
    "ConnectionSummaryTypeDef",
    "ConnectionTypeDef",
    "CreateConnectionRequestTypeDef",
    "CreateConnectionResponseTypeDef",
    "DeleteConnectionRequestTypeDef",
    "DeleteConnectionResponseTypeDef",
    "DescribeConnectionProposalRequestTypeDef",
    "DescribeConnectionProposalResponseTypeDef",
    "EnvironmentTypeDef",
    "GetConnectionRequestTypeDef",
    "GetConnectionRequestWaitExtraTypeDef",
    "GetConnectionRequestWaitTypeDef",
    "GetConnectionResponseTypeDef",
    "GetEnvironmentRequestTypeDef",
    "GetEnvironmentResponseTypeDef",
    "ListAttachPointsRequestPaginateTypeDef",
    "ListAttachPointsRequestTypeDef",
    "ListAttachPointsResponseTypeDef",
    "ListConnectionsRequestPaginateTypeDef",
    "ListConnectionsRequestTypeDef",
    "ListConnectionsResponseTypeDef",
    "ListEnvironmentsRequestPaginateTypeDef",
    "ListEnvironmentsRequestTypeDef",
    "ListEnvironmentsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ProviderTypeDef",
    "RemoteAccountIdentifierTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateConnectionRequestTypeDef",
    "UpdateConnectionResponseTypeDef",
    "WaiterConfigTypeDef",
)

class AttachPointTypeDef(TypedDict):
    directConnectGateway: NotRequired[str]
    arn: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

AttachPointDescriptorTypeDef = TypedDict(
    "AttachPointDescriptorTypeDef",
    {
        "type": Literal["DirectConnectGateway"],
        "identifier": str,
        "name": str,
    },
)

class BandwidthsTypeDef(TypedDict):
    available: NotRequired[list[str]]
    supported: NotRequired[list[str]]

class ProviderTypeDef(TypedDict):
    cloudServiceProvider: NotRequired[str]
    lastMileProvider: NotRequired[str]

class RemoteAccountIdentifierTypeDef(TypedDict):
    identifier: NotRequired[str]

class DeleteConnectionRequestTypeDef(TypedDict):
    identifier: str
    clientToken: NotRequired[str]

class DescribeConnectionProposalRequestTypeDef(TypedDict):
    activationKey: str

class GetConnectionRequestTypeDef(TypedDict):
    identifier: str

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

GetEnvironmentRequestTypeDef = TypedDict(
    "GetEnvironmentRequestTypeDef",
    {
        "id": str,
    },
)

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAttachPointsRequestTypeDef(TypedDict):
    environmentId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListTagsForResourceRequestTypeDef(TypedDict):
    arn: str

class TagResourceRequestTypeDef(TypedDict):
    arn: str
    tags: Mapping[str, str]

class UntagResourceRequestTypeDef(TypedDict):
    arn: str
    tagKeys: Sequence[str]

class UpdateConnectionRequestTypeDef(TypedDict):
    identifier: str
    description: NotRequired[str]
    bandwidth: NotRequired[str]
    clientToken: NotRequired[str]

class AcceptConnectionProposalRequestTypeDef(TypedDict):
    attachPoint: AttachPointTypeDef
    activationKey: str
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListAttachPointsResponseTypeDef(TypedDict):
    attachPoints: list[AttachPointDescriptorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

ConnectionSummaryTypeDef = TypedDict(
    "ConnectionSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "description": str,
        "bandwidth": str,
        "attachPoint": AttachPointTypeDef,
        "environmentId": str,
        "provider": ProviderTypeDef,
        "location": str,
        "type": str,
        "state": ConnectionStateType,
        "sharedId": str,
        "billingTier": NotRequired[int],
    },
)
ConnectionTypeDef = TypedDict(
    "ConnectionTypeDef",
    {
        "id": str,
        "arn": str,
        "description": str,
        "bandwidth": str,
        "attachPoint": AttachPointTypeDef,
        "environmentId": str,
        "provider": ProviderTypeDef,
        "location": str,
        "type": str,
        "state": ConnectionStateType,
        "sharedId": str,
        "ownerAccount": str,
        "activationKey": str,
        "billingTier": NotRequired[int],
        "tags": NotRequired[dict[str, str]],
    },
)

class DescribeConnectionProposalResponseTypeDef(TypedDict):
    bandwidth: str
    environmentId: str
    provider: ProviderTypeDef
    location: str
    ResponseMetadata: ResponseMetadataTypeDef

EnvironmentTypeDef = TypedDict(
    "EnvironmentTypeDef",
    {
        "provider": ProviderTypeDef,
        "location": str,
        "environmentId": str,
        "state": EnvironmentStateType,
        "bandwidths": BandwidthsTypeDef,
        "type": str,
        "activationPageUrl": NotRequired[str],
        "remoteIdentifierType": NotRequired[RemoteAccountIdentifierTypeType],
    },
)

class ListConnectionsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    state: NotRequired[ConnectionStateType]
    environmentId: NotRequired[str]
    provider: NotRequired[ProviderTypeDef]
    attachPoint: NotRequired[AttachPointTypeDef]

class ListEnvironmentsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    provider: NotRequired[ProviderTypeDef]
    location: NotRequired[str]

class CreateConnectionRequestTypeDef(TypedDict):
    bandwidth: str
    attachPoint: AttachPointTypeDef
    environmentId: str
    description: NotRequired[str]
    remoteAccount: NotRequired[RemoteAccountIdentifierTypeDef]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]

class GetConnectionRequestWaitExtraTypeDef(TypedDict):
    identifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetConnectionRequestWaitTypeDef(TypedDict):
    identifier: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class ListAttachPointsRequestPaginateTypeDef(TypedDict):
    environmentId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListConnectionsRequestPaginateTypeDef(TypedDict):
    state: NotRequired[ConnectionStateType]
    environmentId: NotRequired[str]
    provider: NotRequired[ProviderTypeDef]
    attachPoint: NotRequired[AttachPointTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEnvironmentsRequestPaginateTypeDef(TypedDict):
    provider: NotRequired[ProviderTypeDef]
    location: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListConnectionsResponseTypeDef(TypedDict):
    connections: list[ConnectionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class AcceptConnectionProposalResponseTypeDef(TypedDict):
    connection: ConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateConnectionResponseTypeDef(TypedDict):
    connection: ConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteConnectionResponseTypeDef(TypedDict):
    connection: ConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetConnectionResponseTypeDef(TypedDict):
    connection: ConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateConnectionResponseTypeDef(TypedDict):
    connection: ConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetEnvironmentResponseTypeDef(TypedDict):
    environment: EnvironmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListEnvironmentsResponseTypeDef(TypedDict):
    environments: list[EnvironmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
