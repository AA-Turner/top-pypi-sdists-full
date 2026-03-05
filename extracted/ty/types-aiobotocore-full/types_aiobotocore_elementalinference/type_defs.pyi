"""
Type annotations for elementalinference service type definitions.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elementalinference/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_aiobotocore_elementalinference.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from typing import Any, Union

from .literals import FeedStatusType, OutputStatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AssociateFeedRequestTypeDef",
    "AssociateFeedResponseTypeDef",
    "ClippingConfigTypeDef",
    "CreateFeedRequestTypeDef",
    "CreateFeedResponseTypeDef",
    "CreateOutputTypeDef",
    "DeleteFeedRequestTypeDef",
    "DeleteFeedResponseTypeDef",
    "DisassociateFeedRequestTypeDef",
    "DisassociateFeedResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "FeedAssociationTypeDef",
    "FeedSummaryTypeDef",
    "GetFeedRequestTypeDef",
    "GetFeedRequestWaitTypeDef",
    "GetFeedResponseTypeDef",
    "GetOutputTypeDef",
    "ListFeedsRequestPaginateTypeDef",
    "ListFeedsRequestTypeDef",
    "ListFeedsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "OutputConfigOutputTypeDef",
    "OutputConfigTypeDef",
    "OutputConfigUnionTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateFeedRequestTypeDef",
    "UpdateFeedResponseTypeDef",
    "UpdateOutputTypeDef",
    "WaiterConfigTypeDef",
)

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class ClippingConfigTypeDef(TypedDict):
    callbackMetadata: NotRequired[str]

class FeedAssociationTypeDef(TypedDict):
    associatedResourceName: str

DeleteFeedRequestTypeDef = TypedDict(
    "DeleteFeedRequestTypeDef",
    {
        "id": str,
    },
)
DisassociateFeedRequestTypeDef = TypedDict(
    "DisassociateFeedRequestTypeDef",
    {
        "id": str,
        "associatedResourceName": str,
        "dryRun": NotRequired[bool],
    },
)
GetFeedRequestTypeDef = TypedDict(
    "GetFeedRequestTypeDef",
    {
        "id": str,
    },
)

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListFeedsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str

class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

AssociateFeedResponseTypeDef = TypedDict(
    "AssociateFeedResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteFeedResponseTypeDef = TypedDict(
    "DeleteFeedResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "status": FeedStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DisassociateFeedResponseTypeDef = TypedDict(
    "DisassociateFeedResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class OutputConfigOutputTypeDef(TypedDict):
    cropping: NotRequired[dict[str, Any]]
    clipping: NotRequired[ClippingConfigTypeDef]

class OutputConfigTypeDef(TypedDict):
    cropping: NotRequired[Mapping[str, Any]]
    clipping: NotRequired[ClippingConfigTypeDef]

FeedSummaryTypeDef = TypedDict(
    "FeedSummaryTypeDef",
    {
        "arn": str,
        "id": str,
        "name": str,
        "status": FeedStatusType,
        "association": NotRequired[FeedAssociationTypeDef],
    },
)
GetFeedRequestWaitTypeDef = TypedDict(
    "GetFeedRequestWaitTypeDef",
    {
        "id": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)

class ListFeedsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetOutputTypeDef(TypedDict):
    name: str
    outputConfig: OutputConfigOutputTypeDef
    status: OutputStatusType
    description: NotRequired[str]
    fromAssociation: NotRequired[bool]

OutputConfigUnionTypeDef = Union[OutputConfigTypeDef, OutputConfigOutputTypeDef]

class ListFeedsResponseTypeDef(TypedDict):
    feeds: list[FeedSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

CreateFeedResponseTypeDef = TypedDict(
    "CreateFeedResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "id": str,
        "dataEndpoints": list[str],
        "outputs": list[GetOutputTypeDef],
        "status": FeedStatusType,
        "association": FeedAssociationTypeDef,
        "tags": dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetFeedResponseTypeDef = TypedDict(
    "GetFeedResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "id": str,
        "dataEndpoints": list[str],
        "outputs": list[GetOutputTypeDef],
        "status": FeedStatusType,
        "association": FeedAssociationTypeDef,
        "tags": dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateFeedResponseTypeDef = TypedDict(
    "UpdateFeedResponseTypeDef",
    {
        "arn": str,
        "name": str,
        "id": str,
        "dataEndpoints": list[str],
        "outputs": list[GetOutputTypeDef],
        "status": FeedStatusType,
        "association": FeedAssociationTypeDef,
        "tags": dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateOutputTypeDef(TypedDict):
    name: str
    outputConfig: OutputConfigUnionTypeDef
    status: OutputStatusType
    description: NotRequired[str]

class UpdateOutputTypeDef(TypedDict):
    name: str
    outputConfig: OutputConfigUnionTypeDef
    status: OutputStatusType
    description: NotRequired[str]
    fromAssociation: NotRequired[bool]

AssociateFeedRequestTypeDef = TypedDict(
    "AssociateFeedRequestTypeDef",
    {
        "id": str,
        "associatedResourceName": str,
        "outputs": Sequence[CreateOutputTypeDef],
        "dryRun": NotRequired[bool],
    },
)

class CreateFeedRequestTypeDef(TypedDict):
    name: str
    outputs: Sequence[CreateOutputTypeDef]
    tags: NotRequired[Mapping[str, str]]

UpdateFeedRequestTypeDef = TypedDict(
    "UpdateFeedRequestTypeDef",
    {
        "name": str,
        "id": str,
        "outputs": Sequence[UpdateOutputTypeDef],
    },
)
