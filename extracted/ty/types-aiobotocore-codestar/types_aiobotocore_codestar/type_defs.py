"""
Type annotations for codestar service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/type_defs/)

Usage::

    ```python
    from types_aiobotocore_codestar.type_defs import AssociateTeamMemberRequestRequestTypeDef

    data: AssociateTeamMemberRequestRequestTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AssociateTeamMemberRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CodeCommitCodeDestinationTypeDef",
    "GitHubCodeDestinationTypeDef",
    "S3LocationTypeDef",
    "CreateUserProfileRequestRequestTypeDef",
    "DeleteProjectRequestRequestTypeDef",
    "DeleteUserProfileRequestRequestTypeDef",
    "DescribeProjectRequestRequestTypeDef",
    "ProjectStatusTypeDef",
    "DescribeUserProfileRequestRequestTypeDef",
    "DisassociateTeamMemberRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListProjectsRequestRequestTypeDef",
    "ProjectSummaryTypeDef",
    "ListResourcesRequestRequestTypeDef",
    "ResourceTypeDef",
    "ListTagsForProjectRequestRequestTypeDef",
    "ListTeamMembersRequestRequestTypeDef",
    "TeamMemberTypeDef",
    "ListUserProfilesRequestRequestTypeDef",
    "UserProfileSummaryTypeDef",
    "TagProjectRequestRequestTypeDef",
    "UntagProjectRequestRequestTypeDef",
    "UpdateProjectRequestRequestTypeDef",
    "UpdateTeamMemberRequestRequestTypeDef",
    "UpdateUserProfileRequestRequestTypeDef",
    "AssociateTeamMemberResultTypeDef",
    "CreateProjectResultTypeDef",
    "CreateUserProfileResultTypeDef",
    "DeleteProjectResultTypeDef",
    "DeleteUserProfileResultTypeDef",
    "DescribeUserProfileResultTypeDef",
    "ListTagsForProjectResultTypeDef",
    "TagProjectResultTypeDef",
    "UpdateTeamMemberResultTypeDef",
    "UpdateUserProfileResultTypeDef",
    "CodeDestinationTypeDef",
    "CodeSourceTypeDef",
    "ToolchainSourceTypeDef",
    "DescribeProjectResultTypeDef",
    "ListProjectsRequestListProjectsPaginateTypeDef",
    "ListResourcesRequestListResourcesPaginateTypeDef",
    "ListTeamMembersRequestListTeamMembersPaginateTypeDef",
    "ListUserProfilesRequestListUserProfilesPaginateTypeDef",
    "ListProjectsResultTypeDef",
    "ListResourcesResultTypeDef",
    "ListTeamMembersResultTypeDef",
    "ListUserProfilesResultTypeDef",
    "CodeTypeDef",
    "ToolchainTypeDef",
    "CreateProjectRequestRequestTypeDef",
)

AssociateTeamMemberRequestRequestTypeDef = TypedDict(
    "AssociateTeamMemberRequestRequestTypeDef",
    {
        "projectId": str,
        "userArn": str,
        "projectRole": str,
        "clientRequestToken": NotRequired[str],
        "remoteAccessAllowed": NotRequired[bool],
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
CodeCommitCodeDestinationTypeDef = TypedDict(
    "CodeCommitCodeDestinationTypeDef",
    {
        "name": str,
    },
)
GitHubCodeDestinationTypeDef = TypedDict(
    "GitHubCodeDestinationTypeDef",
    {
        "name": str,
        "type": str,
        "owner": str,
        "privateRepository": bool,
        "issuesEnabled": bool,
        "token": str,
        "description": NotRequired[str],
    },
)
S3LocationTypeDef = TypedDict(
    "S3LocationTypeDef",
    {
        "bucketName": NotRequired[str],
        "bucketKey": NotRequired[str],
    },
)
CreateUserProfileRequestRequestTypeDef = TypedDict(
    "CreateUserProfileRequestRequestTypeDef",
    {
        "userArn": str,
        "displayName": str,
        "emailAddress": str,
        "sshPublicKey": NotRequired[str],
    },
)
DeleteProjectRequestRequestTypeDef = TypedDict(
    "DeleteProjectRequestRequestTypeDef",
    {
        "id": str,
        "clientRequestToken": NotRequired[str],
        "deleteStack": NotRequired[bool],
    },
)
DeleteUserProfileRequestRequestTypeDef = TypedDict(
    "DeleteUserProfileRequestRequestTypeDef",
    {
        "userArn": str,
    },
)
DescribeProjectRequestRequestTypeDef = TypedDict(
    "DescribeProjectRequestRequestTypeDef",
    {
        "id": str,
    },
)
ProjectStatusTypeDef = TypedDict(
    "ProjectStatusTypeDef",
    {
        "state": str,
        "reason": NotRequired[str],
    },
)
DescribeUserProfileRequestRequestTypeDef = TypedDict(
    "DescribeUserProfileRequestRequestTypeDef",
    {
        "userArn": str,
    },
)
DisassociateTeamMemberRequestRequestTypeDef = TypedDict(
    "DisassociateTeamMemberRequestRequestTypeDef",
    {
        "projectId": str,
        "userArn": str,
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
ListProjectsRequestRequestTypeDef = TypedDict(
    "ListProjectsRequestRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
ProjectSummaryTypeDef = TypedDict(
    "ProjectSummaryTypeDef",
    {
        "projectId": NotRequired[str],
        "projectArn": NotRequired[str],
    },
)
ListResourcesRequestRequestTypeDef = TypedDict(
    "ListResourcesRequestRequestTypeDef",
    {
        "projectId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "id": str,
    },
)
ListTagsForProjectRequestRequestTypeDef = TypedDict(
    "ListTagsForProjectRequestRequestTypeDef",
    {
        "id": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
ListTeamMembersRequestRequestTypeDef = TypedDict(
    "ListTeamMembersRequestRequestTypeDef",
    {
        "projectId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
TeamMemberTypeDef = TypedDict(
    "TeamMemberTypeDef",
    {
        "userArn": str,
        "projectRole": str,
        "remoteAccessAllowed": NotRequired[bool],
    },
)
ListUserProfilesRequestRequestTypeDef = TypedDict(
    "ListUserProfilesRequestRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
UserProfileSummaryTypeDef = TypedDict(
    "UserProfileSummaryTypeDef",
    {
        "userArn": NotRequired[str],
        "displayName": NotRequired[str],
        "emailAddress": NotRequired[str],
        "sshPublicKey": NotRequired[str],
    },
)
TagProjectRequestRequestTypeDef = TypedDict(
    "TagProjectRequestRequestTypeDef",
    {
        "id": str,
        "tags": Mapping[str, str],
    },
)
UntagProjectRequestRequestTypeDef = TypedDict(
    "UntagProjectRequestRequestTypeDef",
    {
        "id": str,
        "tags": Sequence[str],
    },
)
UpdateProjectRequestRequestTypeDef = TypedDict(
    "UpdateProjectRequestRequestTypeDef",
    {
        "id": str,
        "name": NotRequired[str],
        "description": NotRequired[str],
    },
)
UpdateTeamMemberRequestRequestTypeDef = TypedDict(
    "UpdateTeamMemberRequestRequestTypeDef",
    {
        "projectId": str,
        "userArn": str,
        "projectRole": NotRequired[str],
        "remoteAccessAllowed": NotRequired[bool],
    },
)
UpdateUserProfileRequestRequestTypeDef = TypedDict(
    "UpdateUserProfileRequestRequestTypeDef",
    {
        "userArn": str,
        "displayName": NotRequired[str],
        "emailAddress": NotRequired[str],
        "sshPublicKey": NotRequired[str],
    },
)
AssociateTeamMemberResultTypeDef = TypedDict(
    "AssociateTeamMemberResultTypeDef",
    {
        "clientRequestToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateProjectResultTypeDef = TypedDict(
    "CreateProjectResultTypeDef",
    {
        "id": str,
        "arn": str,
        "clientRequestToken": str,
        "projectTemplateId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateUserProfileResultTypeDef = TypedDict(
    "CreateUserProfileResultTypeDef",
    {
        "userArn": str,
        "displayName": str,
        "emailAddress": str,
        "sshPublicKey": str,
        "createdTimestamp": datetime,
        "lastModifiedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteProjectResultTypeDef = TypedDict(
    "DeleteProjectResultTypeDef",
    {
        "stackId": str,
        "projectArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteUserProfileResultTypeDef = TypedDict(
    "DeleteUserProfileResultTypeDef",
    {
        "userArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeUserProfileResultTypeDef = TypedDict(
    "DescribeUserProfileResultTypeDef",
    {
        "userArn": str,
        "displayName": str,
        "emailAddress": str,
        "sshPublicKey": str,
        "createdTimestamp": datetime,
        "lastModifiedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListTagsForProjectResultTypeDef = TypedDict(
    "ListTagsForProjectResultTypeDef",
    {
        "tags": Dict[str, str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
TagProjectResultTypeDef = TypedDict(
    "TagProjectResultTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateTeamMemberResultTypeDef = TypedDict(
    "UpdateTeamMemberResultTypeDef",
    {
        "userArn": str,
        "projectRole": str,
        "remoteAccessAllowed": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateUserProfileResultTypeDef = TypedDict(
    "UpdateUserProfileResultTypeDef",
    {
        "userArn": str,
        "displayName": str,
        "emailAddress": str,
        "sshPublicKey": str,
        "createdTimestamp": datetime,
        "lastModifiedTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CodeDestinationTypeDef = TypedDict(
    "CodeDestinationTypeDef",
    {
        "codeCommit": NotRequired[CodeCommitCodeDestinationTypeDef],
        "gitHub": NotRequired[GitHubCodeDestinationTypeDef],
    },
)
CodeSourceTypeDef = TypedDict(
    "CodeSourceTypeDef",
    {
        "s3": S3LocationTypeDef,
    },
)
ToolchainSourceTypeDef = TypedDict(
    "ToolchainSourceTypeDef",
    {
        "s3": S3LocationTypeDef,
    },
)
DescribeProjectResultTypeDef = TypedDict(
    "DescribeProjectResultTypeDef",
    {
        "name": str,
        "id": str,
        "arn": str,
        "description": str,
        "clientRequestToken": str,
        "createdTimeStamp": datetime,
        "stackId": str,
        "projectTemplateId": str,
        "status": ProjectStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListProjectsRequestListProjectsPaginateTypeDef = TypedDict(
    "ListProjectsRequestListProjectsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListResourcesRequestListResourcesPaginateTypeDef = TypedDict(
    "ListResourcesRequestListResourcesPaginateTypeDef",
    {
        "projectId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListTeamMembersRequestListTeamMembersPaginateTypeDef = TypedDict(
    "ListTeamMembersRequestListTeamMembersPaginateTypeDef",
    {
        "projectId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListUserProfilesRequestListUserProfilesPaginateTypeDef = TypedDict(
    "ListUserProfilesRequestListUserProfilesPaginateTypeDef",
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
ListResourcesResultTypeDef = TypedDict(
    "ListResourcesResultTypeDef",
    {
        "resources": List[ResourceTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListTeamMembersResultTypeDef = TypedDict(
    "ListTeamMembersResultTypeDef",
    {
        "teamMembers": List[TeamMemberTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListUserProfilesResultTypeDef = TypedDict(
    "ListUserProfilesResultTypeDef",
    {
        "userProfiles": List[UserProfileSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CodeTypeDef = TypedDict(
    "CodeTypeDef",
    {
        "source": CodeSourceTypeDef,
        "destination": CodeDestinationTypeDef,
    },
)
ToolchainTypeDef = TypedDict(
    "ToolchainTypeDef",
    {
        "source": ToolchainSourceTypeDef,
        "roleArn": NotRequired[str],
        "stackParameters": NotRequired[Mapping[str, str]],
    },
)
CreateProjectRequestRequestTypeDef = TypedDict(
    "CreateProjectRequestRequestTypeDef",
    {
        "name": str,
        "id": str,
        "description": NotRequired[str],
        "clientRequestToken": NotRequired[str],
        "sourceCode": NotRequired[Sequence[CodeTypeDef]],
        "toolchain": NotRequired[ToolchainTypeDef],
        "tags": NotRequired[Mapping[str, str]],
    },
)
