"""
Type annotations for route53profiles service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53profiles/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_route53profiles.type_defs import TagTypeDef

    data: TagTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime

from .literals import ProfileStatusType, ShareStatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AssociateProfileRequestTypeDef",
    "AssociateProfileResponseTypeDef",
    "AssociateResourceToProfileRequestTypeDef",
    "AssociateResourceToProfileResponseTypeDef",
    "CreateProfileRequestTypeDef",
    "CreateProfileResponseTypeDef",
    "DeleteProfileRequestTypeDef",
    "DeleteProfileResponseTypeDef",
    "DisassociateProfileRequestTypeDef",
    "DisassociateProfileResponseTypeDef",
    "DisassociateResourceFromProfileRequestTypeDef",
    "DisassociateResourceFromProfileResponseTypeDef",
    "GetProfileAssociationRequestTypeDef",
    "GetProfileAssociationResponseTypeDef",
    "GetProfileRequestTypeDef",
    "GetProfileResourceAssociationRequestTypeDef",
    "GetProfileResourceAssociationResponseTypeDef",
    "GetProfileResponseTypeDef",
    "ListProfileAssociationsRequestPaginateTypeDef",
    "ListProfileAssociationsRequestTypeDef",
    "ListProfileAssociationsResponseTypeDef",
    "ListProfileResourceAssociationsRequestPaginateTypeDef",
    "ListProfileResourceAssociationsRequestTypeDef",
    "ListProfileResourceAssociationsResponseTypeDef",
    "ListProfilesRequestPaginateTypeDef",
    "ListProfilesRequestTypeDef",
    "ListProfilesResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ProfileAssociationTypeDef",
    "ProfileResourceAssociationTypeDef",
    "ProfileSummaryTypeDef",
    "ProfileTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateProfileAssociationRequestTypeDef",
    "UpdateProfileAssociationResponseTypeDef",
    "UpdateProfileResourceAssociationRequestTypeDef",
    "UpdateProfileResourceAssociationResponseTypeDef",
)


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class ProfileAssociationTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    OwnerId: NotRequired[str]
    ProfileId: NotRequired[str]
    ResourceId: NotRequired[str]
    Status: NotRequired[ProfileStatusType]
    StatusMessage: NotRequired[str]
    CreationTime: NotRequired[datetime]
    ModificationTime: NotRequired[datetime]
    Priority: NotRequired[int]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AssociateResourceToProfileRequestTypeDef(TypedDict):
    ProfileId: str
    ResourceArn: str
    Name: str
    ResourceProperties: NotRequired[str]


class ProfileResourceAssociationTypeDef(TypedDict):
    Id: NotRequired[str]
    Name: NotRequired[str]
    OwnerId: NotRequired[str]
    ProfileId: NotRequired[str]
    ResourceArn: NotRequired[str]
    ResourceType: NotRequired[str]
    ResourceProperties: NotRequired[str]
    Status: NotRequired[ProfileStatusType]
    StatusMessage: NotRequired[str]
    CreationTime: NotRequired[datetime]
    ModificationTime: NotRequired[datetime]


class ProfileTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    OwnerId: NotRequired[str]
    Status: NotRequired[ProfileStatusType]
    StatusMessage: NotRequired[str]
    ShareStatus: NotRequired[ShareStatusType]
    CreationTime: NotRequired[datetime]
    ModificationTime: NotRequired[datetime]
    ClientToken: NotRequired[str]


class DeleteProfileRequestTypeDef(TypedDict):
    ProfileId: str


class DisassociateProfileRequestTypeDef(TypedDict):
    ProfileId: str
    ResourceId: str


class DisassociateResourceFromProfileRequestTypeDef(TypedDict):
    ProfileId: str
    ResourceArn: str


class GetProfileAssociationRequestTypeDef(TypedDict):
    ProfileAssociationId: str


class GetProfileRequestTypeDef(TypedDict):
    ProfileId: str


class GetProfileResourceAssociationRequestTypeDef(TypedDict):
    ProfileResourceAssociationId: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListProfileAssociationsRequestTypeDef(TypedDict):
    ResourceId: NotRequired[str]
    ProfileId: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListProfileResourceAssociationsRequestTypeDef(TypedDict):
    ProfileId: str
    ResourceType: NotRequired[str]
    ResourceArn: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListProfilesRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ProfileSummaryTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    ShareStatus: NotRequired[ShareStatusType]


class ListTagsForResourceRequestTypeDef(TypedDict):
    ResourceArn: str


class TagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]


class UntagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class UpdateProfileAssociationRequestTypeDef(TypedDict):
    ProfileAssociationId: str
    Name: NotRequired[str]
    Priority: NotRequired[int]


class UpdateProfileResourceAssociationRequestTypeDef(TypedDict):
    ProfileResourceAssociationId: str
    Name: NotRequired[str]
    ResourceProperties: NotRequired[str]


class AssociateProfileRequestTypeDef(TypedDict):
    ProfileId: str
    ResourceId: str
    Name: str
    Tags: NotRequired[Sequence[TagTypeDef]]
    Priority: NotRequired[int]


class CreateProfileRequestTypeDef(TypedDict):
    Name: str
    ClientToken: str
    Tags: NotRequired[Sequence[TagTypeDef]]


class AssociateProfileResponseTypeDef(TypedDict):
    ProfileAssociation: ProfileAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateProfileResponseTypeDef(TypedDict):
    ProfileAssociation: ProfileAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetProfileAssociationResponseTypeDef(TypedDict):
    ProfileAssociation: ProfileAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListProfileAssociationsResponseTypeDef(TypedDict):
    ProfileAssociations: list[ProfileAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateProfileAssociationResponseTypeDef(TypedDict):
    ProfileAssociation: ProfileAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateResourceToProfileResponseTypeDef(TypedDict):
    ProfileResourceAssociation: ProfileResourceAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateResourceFromProfileResponseTypeDef(TypedDict):
    ProfileResourceAssociation: ProfileResourceAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetProfileResourceAssociationResponseTypeDef(TypedDict):
    ProfileResourceAssociation: ProfileResourceAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListProfileResourceAssociationsResponseTypeDef(TypedDict):
    ProfileResourceAssociations: list[ProfileResourceAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateProfileResourceAssociationResponseTypeDef(TypedDict):
    ProfileResourceAssociation: ProfileResourceAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateProfileResponseTypeDef(TypedDict):
    Profile: ProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteProfileResponseTypeDef(TypedDict):
    Profile: ProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetProfileResponseTypeDef(TypedDict):
    Profile: ProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListProfileAssociationsRequestPaginateTypeDef(TypedDict):
    ResourceId: NotRequired[str]
    ProfileId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProfileResourceAssociationsRequestPaginateTypeDef(TypedDict):
    ProfileId: str
    ResourceType: NotRequired[str]
    ResourceArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProfilesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProfilesResponseTypeDef(TypedDict):
    ProfileSummaries: list[ProfileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
