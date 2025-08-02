"""
Type annotations for elastic-inference service type definitions.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastic_inference/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from types_aiobotocore_elastic_inference.type_defs import AcceleratorTypeOfferingTypeDef

    data: AcceleratorTypeOfferingTypeDef = ...
    ```
"""

from __future__ import annotations

import sys

from .literals import LocationTypeType

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import list as List
    from collections.abc import Mapping, Sequence
else:
    from typing import Dict, List, Mapping, Sequence
if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AcceleratorTypeOfferingTypeDef",
    "AcceleratorTypeTypeDef",
    "DescribeAcceleratorOfferingsRequestTypeDef",
    "DescribeAcceleratorOfferingsResponseTypeDef",
    "DescribeAcceleratorTypesResponseTypeDef",
    "DescribeAcceleratorsRequestPaginateTypeDef",
    "DescribeAcceleratorsRequestTypeDef",
    "DescribeAcceleratorsResponseTypeDef",
    "ElasticInferenceAcceleratorHealthTypeDef",
    "ElasticInferenceAcceleratorTypeDef",
    "FilterTypeDef",
    "KeyValuePairTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResultTypeDef",
    "MemoryInfoTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestTypeDef",
    "UntagResourceRequestTypeDef",
)

class AcceleratorTypeOfferingTypeDef(TypedDict):
    acceleratorType: NotRequired[str]
    locationType: NotRequired[LocationTypeType]
    location: NotRequired[str]

class KeyValuePairTypeDef(TypedDict):
    key: NotRequired[str]
    value: NotRequired[int]

class MemoryInfoTypeDef(TypedDict):
    sizeInMiB: NotRequired[int]

class DescribeAcceleratorOfferingsRequestTypeDef(TypedDict):
    locationType: LocationTypeType
    acceleratorTypes: NotRequired[Sequence[str]]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class FilterTypeDef(TypedDict):
    name: NotRequired[str]
    values: NotRequired[Sequence[str]]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ElasticInferenceAcceleratorHealthTypeDef(TypedDict):
    status: NotRequired[str]

class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str

class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class AcceleratorTypeTypeDef(TypedDict):
    acceleratorTypeName: NotRequired[str]
    memoryInfo: NotRequired[MemoryInfoTypeDef]
    throughputInfo: NotRequired[List[KeyValuePairTypeDef]]

class DescribeAcceleratorOfferingsResponseTypeDef(TypedDict):
    acceleratorTypeOfferings: List[AcceleratorTypeOfferingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResultTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAcceleratorsRequestTypeDef(TypedDict):
    acceleratorIds: NotRequired[Sequence[str]]
    filters: NotRequired[Sequence[FilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class DescribeAcceleratorsRequestPaginateTypeDef(TypedDict):
    acceleratorIds: NotRequired[Sequence[str]]
    filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ElasticInferenceAcceleratorTypeDef(TypedDict):
    acceleratorHealth: NotRequired[ElasticInferenceAcceleratorHealthTypeDef]
    acceleratorType: NotRequired[str]
    acceleratorId: NotRequired[str]
    availabilityZone: NotRequired[str]
    attachedResource: NotRequired[str]

class DescribeAcceleratorTypesResponseTypeDef(TypedDict):
    acceleratorTypes: List[AcceleratorTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeAcceleratorsResponseTypeDef(TypedDict):
    acceleratorSet: List[ElasticInferenceAcceleratorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
