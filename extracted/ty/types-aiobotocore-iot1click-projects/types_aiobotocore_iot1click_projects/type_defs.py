"""
Type annotations for iot1click-projects service type definitions.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_projects/type_defs/)

Usage::

    ```python
    from types_aiobotocore_iot1click_projects.type_defs import AssociateDeviceWithPlacementRequestRequestTypeDef

    data: AssociateDeviceWithPlacementRequestRequestTypeDef = ...
    ```

Copyright 2025 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Union

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
    "AssociateDeviceWithPlacementRequestRequestTypeDef",
    "CreatePlacementRequestRequestTypeDef",
    "CreateProjectRequestRequestTypeDef",
    "DeletePlacementRequestRequestTypeDef",
    "DeleteProjectRequestRequestTypeDef",
    "DescribePlacementRequestRequestTypeDef",
    "DescribePlacementResponseTypeDef",
    "DescribeProjectRequestRequestTypeDef",
    "DescribeProjectResponseTypeDef",
    "DeviceTemplateOutputTypeDef",
    "DeviceTemplateTypeDef",
    "DeviceTemplateUnionTypeDef",
    "DisassociateDeviceFromPlacementRequestRequestTypeDef",
    "GetDevicesInPlacementRequestRequestTypeDef",
    "GetDevicesInPlacementResponseTypeDef",
    "ListPlacementsRequestPaginateTypeDef",
    "ListPlacementsRequestRequestTypeDef",
    "ListPlacementsResponseTypeDef",
    "ListProjectsRequestPaginateTypeDef",
    "ListProjectsRequestRequestTypeDef",
    "ListProjectsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PlacementDescriptionTypeDef",
    "PlacementSummaryTypeDef",
    "PlacementTemplateOutputTypeDef",
    "PlacementTemplateTypeDef",
    "ProjectDescriptionTypeDef",
    "ProjectSummaryTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdatePlacementRequestRequestTypeDef",
    "UpdateProjectRequestRequestTypeDef",
)


class AssociateDeviceWithPlacementRequestRequestTypeDef(TypedDict):
    projectName: str
    placementName: str
    deviceId: str
    deviceTemplateName: str


class CreatePlacementRequestRequestTypeDef(TypedDict):
    placementName: str
    projectName: str
    attributes: NotRequired[Mapping[str, str]]


class DeletePlacementRequestRequestTypeDef(TypedDict):
    placementName: str
    projectName: str


class DeleteProjectRequestRequestTypeDef(TypedDict):
    projectName: str


class DescribePlacementRequestRequestTypeDef(TypedDict):
    placementName: str
    projectName: str


class PlacementDescriptionTypeDef(TypedDict):
    projectName: str
    placementName: str
    attributes: Dict[str, str]
    createdDate: datetime
    updatedDate: datetime


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DescribeProjectRequestRequestTypeDef(TypedDict):
    projectName: str


class DeviceTemplateOutputTypeDef(TypedDict):
    deviceType: NotRequired[str]
    callbackOverrides: NotRequired[Dict[str, str]]


class DeviceTemplateTypeDef(TypedDict):
    deviceType: NotRequired[str]
    callbackOverrides: NotRequired[Mapping[str, str]]


class DisassociateDeviceFromPlacementRequestRequestTypeDef(TypedDict):
    projectName: str
    placementName: str
    deviceTemplateName: str


class GetDevicesInPlacementRequestRequestTypeDef(TypedDict):
    projectName: str
    placementName: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListPlacementsRequestRequestTypeDef(TypedDict):
    projectName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class PlacementSummaryTypeDef(TypedDict):
    projectName: str
    placementName: str
    createdDate: datetime
    updatedDate: datetime


class ListProjectsRequestRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ProjectSummaryTypeDef(TypedDict):
    projectName: str
    createdDate: datetime
    updatedDate: datetime
    arn: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str


class TagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdatePlacementRequestRequestTypeDef(TypedDict):
    placementName: str
    projectName: str
    attributes: NotRequired[Mapping[str, str]]


class DescribePlacementResponseTypeDef(TypedDict):
    placement: PlacementDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetDevicesInPlacementResponseTypeDef(TypedDict):
    devices: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class PlacementTemplateOutputTypeDef(TypedDict):
    defaultAttributes: NotRequired[Dict[str, str]]
    deviceTemplates: NotRequired[Dict[str, DeviceTemplateOutputTypeDef]]


DeviceTemplateUnionTypeDef = Union[DeviceTemplateTypeDef, DeviceTemplateOutputTypeDef]


class ListPlacementsRequestPaginateTypeDef(TypedDict):
    projectName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProjectsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPlacementsResponseTypeDef(TypedDict):
    placements: List[PlacementSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListProjectsResponseTypeDef(TypedDict):
    projects: List[ProjectSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ProjectDescriptionTypeDef(TypedDict):
    projectName: str
    createdDate: datetime
    updatedDate: datetime
    arn: NotRequired[str]
    description: NotRequired[str]
    placementTemplate: NotRequired[PlacementTemplateOutputTypeDef]
    tags: NotRequired[Dict[str, str]]


class PlacementTemplateTypeDef(TypedDict):
    defaultAttributes: NotRequired[Mapping[str, str]]
    deviceTemplates: NotRequired[Mapping[str, DeviceTemplateUnionTypeDef]]


class DescribeProjectResponseTypeDef(TypedDict):
    project: ProjectDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateProjectRequestRequestTypeDef(TypedDict):
    projectName: str
    description: NotRequired[str]
    placementTemplate: NotRequired[PlacementTemplateTypeDef]
    tags: NotRequired[Mapping[str, str]]


class UpdateProjectRequestRequestTypeDef(TypedDict):
    projectName: str
    description: NotRequired[str]
    placementTemplate: NotRequired[PlacementTemplateTypeDef]
