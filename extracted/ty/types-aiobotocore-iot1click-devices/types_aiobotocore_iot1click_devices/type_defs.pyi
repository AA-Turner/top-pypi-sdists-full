"""
Type annotations for iot1click-devices service type definitions.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/type_defs/)

Usage::

    ```python
    from types_aiobotocore_iot1click_devices.type_defs import ClaimDevicesByClaimCodeRequestRequestTypeDef

    data: ClaimDevicesByClaimCodeRequestRequestTypeDef = ...
    ```

Copyright 2025 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Any, Union

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
    "ClaimDevicesByClaimCodeRequestRequestTypeDef",
    "ClaimDevicesByClaimCodeResponseTypeDef",
    "DescribeDeviceRequestRequestTypeDef",
    "DescribeDeviceResponseTypeDef",
    "DeviceDescriptionTypeDef",
    "DeviceEventTypeDef",
    "DeviceMethodTypeDef",
    "DeviceTypeDef",
    "EmptyResponseMetadataTypeDef",
    "FinalizeDeviceClaimRequestRequestTypeDef",
    "FinalizeDeviceClaimResponseTypeDef",
    "GetDeviceMethodsRequestRequestTypeDef",
    "GetDeviceMethodsResponseTypeDef",
    "InitiateDeviceClaimRequestRequestTypeDef",
    "InitiateDeviceClaimResponseTypeDef",
    "InvokeDeviceMethodRequestRequestTypeDef",
    "InvokeDeviceMethodResponseTypeDef",
    "ListDeviceEventsRequestPaginateTypeDef",
    "ListDeviceEventsRequestRequestTypeDef",
    "ListDeviceEventsResponseTypeDef",
    "ListDevicesRequestPaginateTypeDef",
    "ListDevicesRequestRequestTypeDef",
    "ListDevicesResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimestampTypeDef",
    "UnclaimDeviceRequestRequestTypeDef",
    "UnclaimDeviceResponseTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDeviceStateRequestRequestTypeDef",
)

class ClaimDevicesByClaimCodeRequestRequestTypeDef(TypedDict):
    ClaimCode: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DescribeDeviceRequestRequestTypeDef(TypedDict):
    DeviceId: str

DeviceDescriptionTypeDef = TypedDict(
    "DeviceDescriptionTypeDef",
    {
        "Arn": NotRequired[str],
        "Attributes": NotRequired[Dict[str, str]],
        "DeviceId": NotRequired[str],
        "Enabled": NotRequired[bool],
        "RemainingLife": NotRequired[float],
        "Type": NotRequired[str],
        "Tags": NotRequired[Dict[str, str]],
    },
)
DeviceTypeDef = TypedDict(
    "DeviceTypeDef",
    {
        "Attributes": NotRequired[Dict[str, Any]],
        "DeviceId": NotRequired[str],
        "Type": NotRequired[str],
    },
)

class DeviceMethodTypeDef(TypedDict):
    DeviceType: NotRequired[str]
    MethodName: NotRequired[str]

class FinalizeDeviceClaimRequestRequestTypeDef(TypedDict):
    DeviceId: str
    Tags: NotRequired[Mapping[str, str]]

class GetDeviceMethodsRequestRequestTypeDef(TypedDict):
    DeviceId: str

class InitiateDeviceClaimRequestRequestTypeDef(TypedDict):
    DeviceId: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

TimestampTypeDef = Union[datetime, str]

class ListDevicesRequestRequestTypeDef(TypedDict):
    DeviceType: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str

class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]

class UnclaimDeviceRequestRequestTypeDef(TypedDict):
    DeviceId: str

class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class UpdateDeviceStateRequestRequestTypeDef(TypedDict):
    DeviceId: str
    Enabled: NotRequired[bool]

class ClaimDevicesByClaimCodeResponseTypeDef(TypedDict):
    ClaimCode: str
    Total: int
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class FinalizeDeviceClaimResponseTypeDef(TypedDict):
    State: str
    ResponseMetadata: ResponseMetadataTypeDef

class InitiateDeviceClaimResponseTypeDef(TypedDict):
    State: str
    ResponseMetadata: ResponseMetadataTypeDef

class InvokeDeviceMethodResponseTypeDef(TypedDict):
    DeviceMethodResponse: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class UnclaimDeviceResponseTypeDef(TypedDict):
    State: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeDeviceResponseTypeDef(TypedDict):
    DeviceDescription: DeviceDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListDevicesResponseTypeDef(TypedDict):
    Devices: List[DeviceDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DeviceEventTypeDef(TypedDict):
    Device: NotRequired[DeviceTypeDef]
    StdEvent: NotRequired[str]

class GetDeviceMethodsResponseTypeDef(TypedDict):
    DeviceMethods: List[DeviceMethodTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class InvokeDeviceMethodRequestRequestTypeDef(TypedDict):
    DeviceId: str
    DeviceMethod: NotRequired[DeviceMethodTypeDef]
    DeviceMethodParameters: NotRequired[str]

class ListDevicesRequestPaginateTypeDef(TypedDict):
    DeviceType: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDeviceEventsRequestPaginateTypeDef(TypedDict):
    DeviceId: str
    FromTimeStamp: TimestampTypeDef
    ToTimeStamp: TimestampTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDeviceEventsRequestRequestTypeDef(TypedDict):
    DeviceId: str
    FromTimeStamp: TimestampTypeDef
    ToTimeStamp: TimestampTypeDef
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListDeviceEventsResponseTypeDef(TypedDict):
    Events: List[DeviceEventTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
