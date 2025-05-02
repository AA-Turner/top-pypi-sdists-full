"""
Type annotations for mobile service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mobile/type_defs/)

Usage::

    ```python
    from types_aiobotocore_mobile.type_defs import BlobTypeDef

    data: BlobTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Union

from aiobotocore.response import StreamingBody

from .literals import PlatformType, ProjectStateType

if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "BlobTypeDef",
    "BundleDetailsTypeDef",
    "ResponseMetadataTypeDef",
    "DeleteProjectRequestRequestTypeDef",
    "ResourceTypeDef",
    "DescribeBundleRequestRequestTypeDef",
    "DescribeProjectRequestRequestTypeDef",
    "ExportBundleRequestRequestTypeDef",
    "ExportProjectRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListBundlesRequestRequestTypeDef",
    "ListProjectsRequestRequestTypeDef",
    "ProjectSummaryTypeDef",
    "CreateProjectRequestRequestTypeDef",
    "UpdateProjectRequestRequestTypeDef",
    "DescribeBundleResultTypeDef",
    "ExportBundleResultTypeDef",
    "ExportProjectResultTypeDef",
    "ListBundlesResultTypeDef",
    "DeleteProjectResultTypeDef",
    "ProjectDetailsTypeDef",
    "ListBundlesRequestListBundlesPaginateTypeDef",
    "ListProjectsRequestListProjectsPaginateTypeDef",
    "ListProjectsResultTypeDef",
    "CreateProjectResultTypeDef",
    "DescribeProjectResultTypeDef",
    "UpdateProjectResultTypeDef",
)

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
BundleDetailsTypeDef = TypedDict(
    "BundleDetailsTypeDef",
    {
        "bundleId": NotRequired[str],
        "title": NotRequired[str],
        "version": NotRequired[str],
        "description": NotRequired[str],
        "iconUrl": NotRequired[str],
        "availablePlatforms": NotRequired[List[PlatformType]],
    },
)
ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
        "HostId": NotRequired[str],
    },
)
DeleteProjectRequestRequestTypeDef = TypedDict(
    "DeleteProjectRequestRequestTypeDef",
    {
        "projectId": str,
    },
)
ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "type": NotRequired[str],
        "name": NotRequired[str],
        "arn": NotRequired[str],
        "feature": NotRequired[str],
        "attributes": NotRequired[Dict[str, str]],
    },
)
DescribeBundleRequestRequestTypeDef = TypedDict(
    "DescribeBundleRequestRequestTypeDef",
    {
        "bundleId": str,
    },
)
DescribeProjectRequestRequestTypeDef = TypedDict(
    "DescribeProjectRequestRequestTypeDef",
    {
        "projectId": str,
        "syncFromResources": NotRequired[bool],
    },
)
ExportBundleRequestRequestTypeDef = TypedDict(
    "ExportBundleRequestRequestTypeDef",
    {
        "bundleId": str,
        "projectId": NotRequired[str],
        "platform": NotRequired[PlatformType],
    },
)
ExportProjectRequestRequestTypeDef = TypedDict(
    "ExportProjectRequestRequestTypeDef",
    {
        "projectId": str,
    },
)
PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": NotRequired[int],
        "PageSize": NotRequired[int],
        "StartingToken": NotRequired[str],
    },
)
ListBundlesRequestRequestTypeDef = TypedDict(
    "ListBundlesRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListProjectsRequestRequestTypeDef = TypedDict(
    "ListProjectsRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ProjectSummaryTypeDef = TypedDict(
    "ProjectSummaryTypeDef",
    {
        "name": NotRequired[str],
        "projectId": NotRequired[str],
    },
)
CreateProjectRequestRequestTypeDef = TypedDict(
    "CreateProjectRequestRequestTypeDef",
    {
        "name": NotRequired[str],
        "region": NotRequired[str],
        "contents": NotRequired[BlobTypeDef],
        "snapshotId": NotRequired[str],
    },
)
UpdateProjectRequestRequestTypeDef = TypedDict(
    "UpdateProjectRequestRequestTypeDef",
    {
        "projectId": str,
        "contents": NotRequired[BlobTypeDef],
    },
)
DescribeBundleResultTypeDef = TypedDict(
    "DescribeBundleResultTypeDef",
    {
        "details": BundleDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ExportBundleResultTypeDef = TypedDict(
    "ExportBundleResultTypeDef",
    {
        "downloadUrl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ExportProjectResultTypeDef = TypedDict(
    "ExportProjectResultTypeDef",
    {
        "downloadUrl": str,
        "shareUrl": str,
        "snapshotId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListBundlesResultTypeDef = TypedDict(
    "ListBundlesResultTypeDef",
    {
        "bundleList": List[BundleDetailsTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteProjectResultTypeDef = TypedDict(
    "DeleteProjectResultTypeDef",
    {
        "deletedResources": List[ResourceTypeDef],
        "orphanedResources": List[ResourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ProjectDetailsTypeDef = TypedDict(
    "ProjectDetailsTypeDef",
    {
        "name": NotRequired[str],
        "projectId": NotRequired[str],
        "region": NotRequired[str],
        "state": NotRequired[ProjectStateType],
        "createdDate": NotRequired[datetime],
        "lastUpdatedDate": NotRequired[datetime],
        "consoleUrl": NotRequired[str],
        "resources": NotRequired[List[ResourceTypeDef]],
    },
)
ListBundlesRequestListBundlesPaginateTypeDef = TypedDict(
    "ListBundlesRequestListBundlesPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListProjectsRequestListProjectsPaginateTypeDef = TypedDict(
    "ListProjectsRequestListProjectsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListProjectsResultTypeDef = TypedDict(
    "ListProjectsResultTypeDef",
    {
        "projects": List[ProjectSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateProjectResultTypeDef = TypedDict(
    "CreateProjectResultTypeDef",
    {
        "details": ProjectDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeProjectResultTypeDef = TypedDict(
    "DescribeProjectResultTypeDef",
    {
        "details": ProjectDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateProjectResultTypeDef = TypedDict(
    "UpdateProjectResultTypeDef",
    {
        "details": ProjectDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
