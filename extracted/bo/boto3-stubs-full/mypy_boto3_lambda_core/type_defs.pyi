"""
Type annotations for lambda-core service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_lambda_core.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    NetworkConnectorLastUpdateStatusReasonCodeType,
    NetworkConnectorLastUpdateStatusType,
    NetworkConnectorStateReasonCodeType,
    NetworkConnectorStateType,
    NetworkProtocolType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "CreateNetworkConnectorRequestTypeDef",
    "CreateNetworkConnectorResponseTypeDef",
    "DeleteNetworkConnectorRequestTypeDef",
    "DeleteNetworkConnectorResponseTypeDef",
    "GetNetworkConnectorRequestTypeDef",
    "GetNetworkConnectorResponseTypeDef",
    "ListNetworkConnectorsRequestPaginateTypeDef",
    "ListNetworkConnectorsRequestTypeDef",
    "ListNetworkConnectorsResponseTypeDef",
    "NetworkConnectorConfigurationOutputTypeDef",
    "NetworkConnectorConfigurationTypeDef",
    "NetworkConnectorConfigurationUnionTypeDef",
    "NetworkConnectorSummaryTypeDef",
    "NetworkConnectorVpcEgressConfigurationOutputTypeDef",
    "NetworkConnectorVpcEgressConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "UpdateNetworkConnectorRequestTypeDef",
    "UpdateNetworkConnectorResponseTypeDef",
)

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DeleteNetworkConnectorRequestTypeDef(TypedDict):
    Identifier: str

class GetNetworkConnectorRequestTypeDef(TypedDict):
    Identifier: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListNetworkConnectorsRequestTypeDef(TypedDict):
    State: NotRequired[NetworkConnectorStateType]
    Marker: NotRequired[str]
    MaxItems: NotRequired[int]

NetworkConnectorSummaryTypeDef = TypedDict(
    "NetworkConnectorSummaryTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Id": str,
        "Type": Literal["VPC_EGRESS"],
        "State": NotRequired[NetworkConnectorStateType],
        "LastModified": NotRequired[datetime],
    },
)

class NetworkConnectorVpcEgressConfigurationOutputTypeDef(TypedDict):
    SubnetIds: NotRequired[list[str]]
    SecurityGroupIds: NotRequired[list[str]]
    NetworkProtocol: NotRequired[NetworkProtocolType]
    AssociatedComputeResourceTypes: NotRequired[list[Literal["MicroVm"]]]

class NetworkConnectorVpcEgressConfigurationTypeDef(TypedDict):
    SubnetIds: NotRequired[Sequence[str]]
    SecurityGroupIds: NotRequired[Sequence[str]]
    NetworkProtocol: NotRequired[NetworkProtocolType]
    AssociatedComputeResourceTypes: NotRequired[Sequence[Literal["MicroVm"]]]

class ListNetworkConnectorsRequestPaginateTypeDef(TypedDict):
    State: NotRequired[NetworkConnectorStateType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListNetworkConnectorsResponseTypeDef(TypedDict):
    NetworkConnectors: list[NetworkConnectorSummaryTypeDef]
    NextMarker: str
    ResponseMetadata: ResponseMetadataTypeDef

class NetworkConnectorConfigurationOutputTypeDef(TypedDict):
    VpcEgressConfiguration: NotRequired[NetworkConnectorVpcEgressConfigurationOutputTypeDef]

class NetworkConnectorConfigurationTypeDef(TypedDict):
    VpcEgressConfiguration: NotRequired[NetworkConnectorVpcEgressConfigurationTypeDef]

class CreateNetworkConnectorResponseTypeDef(TypedDict):
    Arn: str
    Name: str
    Id: str
    Configuration: NetworkConnectorConfigurationOutputTypeDef
    OperatorRole: str
    State: NetworkConnectorStateType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteNetworkConnectorResponseTypeDef(TypedDict):
    Arn: str
    Name: str
    Id: str
    Configuration: NetworkConnectorConfigurationOutputTypeDef
    OperatorRole: str
    State: NetworkConnectorStateType
    ResponseMetadata: ResponseMetadataTypeDef

class GetNetworkConnectorResponseTypeDef(TypedDict):
    Arn: str
    Name: str
    Id: str
    Version: int
    Configuration: NetworkConnectorConfigurationOutputTypeDef
    OperatorRole: str
    State: NetworkConnectorStateType
    StateReason: str
    StateReasonCode: NetworkConnectorStateReasonCodeType
    LastUpdateStatus: NetworkConnectorLastUpdateStatusType
    LastUpdateStatusReason: str
    LastUpdateStatusReasonCode: NetworkConnectorLastUpdateStatusReasonCodeType
    LastModified: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateNetworkConnectorResponseTypeDef(TypedDict):
    Arn: str
    Name: str
    Id: str
    OperatorRole: str
    Configuration: NetworkConnectorConfigurationOutputTypeDef
    State: NetworkConnectorStateType
    LastUpdateStatus: NetworkConnectorLastUpdateStatusType
    LastUpdateStatusReason: str
    LastModified: datetime
    ResponseMetadata: ResponseMetadataTypeDef

NetworkConnectorConfigurationUnionTypeDef = Union[
    NetworkConnectorConfigurationTypeDef, NetworkConnectorConfigurationOutputTypeDef
]

class CreateNetworkConnectorRequestTypeDef(TypedDict):
    Name: str
    Configuration: NetworkConnectorConfigurationUnionTypeDef
    OperatorRole: NotRequired[str]
    ClientToken: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]

class UpdateNetworkConnectorRequestTypeDef(TypedDict):
    Identifier: str
    Configuration: NotRequired[NetworkConnectorConfigurationUnionTypeDef]
    OperatorRole: NotRequired[str]
    ClientToken: NotRequired[str]
