"""
Type annotations for nimble service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/type_defs/)

Usage::

    ```python
    from types_aiobotocore_nimble.type_defs import AcceptEulasRequestRequestTypeDef

    data: AcceptEulasRequestRequestTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AutomaticTerminationModeType,
    LaunchProfilePlatformType,
    LaunchProfileStateType,
    LaunchProfileStatusCodeType,
    LaunchProfileValidationStateType,
    LaunchProfileValidationStatusCodeType,
    LaunchProfileValidationTypeType,
    SessionBackupModeType,
    SessionPersistenceModeType,
    StreamingClipboardModeType,
    StreamingImageStateType,
    StreamingImageStatusCodeType,
    StreamingInstanceTypeType,
    StreamingSessionStateType,
    StreamingSessionStatusCodeType,
    StreamingSessionStreamStateType,
    StreamingSessionStreamStatusCodeType,
    StudioComponentInitializationScriptRunContextType,
    StudioComponentStateType,
    StudioComponentStatusCodeType,
    StudioComponentSubtypeType,
    StudioComponentTypeType,
    StudioEncryptionConfigurationKeyTypeType,
    StudioStateType,
    StudioStatusCodeType,
    VolumeRetentionModeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AcceptEulasRequestRequestTypeDef",
    "EulaAcceptanceTypeDef",
    "ResponseMetadataTypeDef",
    "ActiveDirectoryComputerAttributeTypeDef",
    "ComputeFarmConfigurationTypeDef",
    "CreateStreamingImageRequestRequestTypeDef",
    "CreateStreamingSessionRequestRequestTypeDef",
    "CreateStreamingSessionStreamRequestRequestTypeDef",
    "StreamingSessionStreamTypeDef",
    "ScriptParameterKeyValueTypeDef",
    "StudioComponentInitializationScriptTypeDef",
    "StudioEncryptionConfigurationTypeDef",
    "DeleteLaunchProfileMemberRequestRequestTypeDef",
    "DeleteLaunchProfileRequestRequestTypeDef",
    "DeleteStreamingImageRequestRequestTypeDef",
    "DeleteStreamingSessionRequestRequestTypeDef",
    "DeleteStudioComponentRequestRequestTypeDef",
    "DeleteStudioMemberRequestRequestTypeDef",
    "DeleteStudioRequestRequestTypeDef",
    "EulaTypeDef",
    "GetEulaRequestRequestTypeDef",
    "GetLaunchProfileDetailsRequestRequestTypeDef",
    "StudioComponentSummaryTypeDef",
    "GetLaunchProfileInitializationRequestRequestTypeDef",
    "GetLaunchProfileMemberRequestRequestTypeDef",
    "LaunchProfileMembershipTypeDef",
    "WaiterConfigTypeDef",
    "GetLaunchProfileRequestRequestTypeDef",
    "GetStreamingImageRequestRequestTypeDef",
    "GetStreamingSessionBackupRequestRequestTypeDef",
    "StreamingSessionBackupTypeDef",
    "GetStreamingSessionRequestRequestTypeDef",
    "GetStreamingSessionStreamRequestRequestTypeDef",
    "GetStudioComponentRequestRequestTypeDef",
    "GetStudioMemberRequestRequestTypeDef",
    "StudioMembershipTypeDef",
    "GetStudioRequestRequestTypeDef",
    "LaunchProfileInitializationScriptTypeDef",
    "ValidationResultTypeDef",
    "LicenseServiceConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "ListEulaAcceptancesRequestRequestTypeDef",
    "ListEulasRequestRequestTypeDef",
    "ListLaunchProfileMembersRequestRequestTypeDef",
    "ListLaunchProfilesRequestRequestTypeDef",
    "ListStreamingImagesRequestRequestTypeDef",
    "ListStreamingSessionBackupsRequestRequestTypeDef",
    "ListStreamingSessionsRequestRequestTypeDef",
    "ListStudioComponentsRequestRequestTypeDef",
    "ListStudioMembersRequestRequestTypeDef",
    "ListStudiosRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "NewLaunchProfileMemberTypeDef",
    "NewStudioMemberTypeDef",
    "SharedFileSystemConfigurationTypeDef",
    "StartStreamingSessionRequestRequestTypeDef",
    "StartStudioSSOConfigurationRepairRequestRequestTypeDef",
    "StopStreamingSessionRequestRequestTypeDef",
    "StreamConfigurationSessionBackupTypeDef",
    "VolumeConfigurationTypeDef",
    "StreamingSessionStorageRootTypeDef",
    "StreamingImageEncryptionConfigurationTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateLaunchProfileMemberRequestRequestTypeDef",
    "UpdateStreamingImageRequestRequestTypeDef",
    "UpdateStudioRequestRequestTypeDef",
    "AcceptEulasResponseTypeDef",
    "ListEulaAcceptancesResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ActiveDirectoryConfigurationOutputTypeDef",
    "ActiveDirectoryConfigurationTypeDef",
    "LaunchProfileInitializationActiveDirectoryTypeDef",
    "CreateStreamingSessionStreamResponseTypeDef",
    "GetStreamingSessionStreamResponseTypeDef",
    "CreateStudioRequestRequestTypeDef",
    "StudioTypeDef",
    "GetEulaResponseTypeDef",
    "ListEulasResponseTypeDef",
    "GetLaunchProfileMemberResponseTypeDef",
    "ListLaunchProfileMembersResponseTypeDef",
    "UpdateLaunchProfileMemberResponseTypeDef",
    "GetLaunchProfileRequestLaunchProfileDeletedWaitTypeDef",
    "GetLaunchProfileRequestLaunchProfileReadyWaitTypeDef",
    "GetStreamingImageRequestStreamingImageDeletedWaitTypeDef",
    "GetStreamingImageRequestStreamingImageReadyWaitTypeDef",
    "GetStreamingSessionRequestStreamingSessionDeletedWaitTypeDef",
    "GetStreamingSessionRequestStreamingSessionReadyWaitTypeDef",
    "GetStreamingSessionRequestStreamingSessionStoppedWaitTypeDef",
    "GetStreamingSessionStreamRequestStreamingSessionStreamReadyWaitTypeDef",
    "GetStudioComponentRequestStudioComponentDeletedWaitTypeDef",
    "GetStudioComponentRequestStudioComponentReadyWaitTypeDef",
    "GetStudioRequestStudioDeletedWaitTypeDef",
    "GetStudioRequestStudioReadyWaitTypeDef",
    "GetStreamingSessionBackupResponseTypeDef",
    "ListStreamingSessionBackupsResponseTypeDef",
    "GetStudioMemberResponseTypeDef",
    "ListStudioMembersResponseTypeDef",
    "ListEulaAcceptancesRequestListEulaAcceptancesPaginateTypeDef",
    "ListEulasRequestListEulasPaginateTypeDef",
    "ListLaunchProfileMembersRequestListLaunchProfileMembersPaginateTypeDef",
    "ListLaunchProfilesRequestListLaunchProfilesPaginateTypeDef",
    "ListStreamingImagesRequestListStreamingImagesPaginateTypeDef",
    "ListStreamingSessionBackupsRequestListStreamingSessionBackupsPaginateTypeDef",
    "ListStreamingSessionsRequestListStreamingSessionsPaginateTypeDef",
    "ListStudioComponentsRequestListStudioComponentsPaginateTypeDef",
    "ListStudioMembersRequestListStudioMembersPaginateTypeDef",
    "ListStudiosRequestListStudiosPaginateTypeDef",
    "PutLaunchProfileMembersRequestRequestTypeDef",
    "PutStudioMembersRequestRequestTypeDef",
    "StreamingSessionTypeDef",
    "StreamConfigurationSessionStorageOutputTypeDef",
    "StreamConfigurationSessionStorageTypeDef",
    "StreamingImageTypeDef",
    "StudioComponentConfigurationOutputTypeDef",
    "ActiveDirectoryConfigurationUnionTypeDef",
    "LaunchProfileInitializationTypeDef",
    "CreateStudioResponseTypeDef",
    "DeleteStudioResponseTypeDef",
    "GetStudioResponseTypeDef",
    "ListStudiosResponseTypeDef",
    "StartStudioSSOConfigurationRepairResponseTypeDef",
    "UpdateStudioResponseTypeDef",
    "CreateStreamingSessionResponseTypeDef",
    "DeleteStreamingSessionResponseTypeDef",
    "GetStreamingSessionResponseTypeDef",
    "ListStreamingSessionsResponseTypeDef",
    "StartStreamingSessionResponseTypeDef",
    "StopStreamingSessionResponseTypeDef",
    "StreamConfigurationTypeDef",
    "StreamConfigurationSessionStorageUnionTypeDef",
    "CreateStreamingImageResponseTypeDef",
    "DeleteStreamingImageResponseTypeDef",
    "GetStreamingImageResponseTypeDef",
    "ListStreamingImagesResponseTypeDef",
    "UpdateStreamingImageResponseTypeDef",
    "StudioComponentTypeDef",
    "StudioComponentConfigurationTypeDef",
    "GetLaunchProfileInitializationResponseTypeDef",
    "LaunchProfileTypeDef",
    "StreamConfigurationCreateTypeDef",
    "CreateStudioComponentResponseTypeDef",
    "DeleteStudioComponentResponseTypeDef",
    "GetStudioComponentResponseTypeDef",
    "ListStudioComponentsResponseTypeDef",
    "UpdateStudioComponentResponseTypeDef",
    "CreateStudioComponentRequestRequestTypeDef",
    "UpdateStudioComponentRequestRequestTypeDef",
    "CreateLaunchProfileResponseTypeDef",
    "DeleteLaunchProfileResponseTypeDef",
    "GetLaunchProfileDetailsResponseTypeDef",
    "GetLaunchProfileResponseTypeDef",
    "ListLaunchProfilesResponseTypeDef",
    "UpdateLaunchProfileResponseTypeDef",
    "CreateLaunchProfileRequestRequestTypeDef",
    "UpdateLaunchProfileRequestRequestTypeDef",
)

AcceptEulasRequestRequestTypeDef = TypedDict(
    "AcceptEulasRequestRequestTypeDef",
    {
        "studioId": str,
        "clientToken": NotRequired[str],
        "eulaIds": NotRequired[Sequence[str]],
    },
)
EulaAcceptanceTypeDef = TypedDict(
    "EulaAcceptanceTypeDef",
    {
        "acceptedAt": NotRequired[datetime],
        "acceptedBy": NotRequired[str],
        "accepteeId": NotRequired[str],
        "eulaAcceptanceId": NotRequired[str],
        "eulaId": NotRequired[str],
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
ActiveDirectoryComputerAttributeTypeDef = TypedDict(
    "ActiveDirectoryComputerAttributeTypeDef",
    {
        "name": NotRequired[str],
        "value": NotRequired[str],
    },
)
ComputeFarmConfigurationTypeDef = TypedDict(
    "ComputeFarmConfigurationTypeDef",
    {
        "activeDirectoryUser": NotRequired[str],
        "endpoint": NotRequired[str],
    },
)
CreateStreamingImageRequestRequestTypeDef = TypedDict(
    "CreateStreamingImageRequestRequestTypeDef",
    {
        "ec2ImageId": str,
        "name": str,
        "studioId": str,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
CreateStreamingSessionRequestRequestTypeDef = TypedDict(
    "CreateStreamingSessionRequestRequestTypeDef",
    {
        "launchProfileId": str,
        "studioId": str,
        "clientToken": NotRequired[str],
        "ec2InstanceType": NotRequired[StreamingInstanceTypeType],
        "ownedBy": NotRequired[str],
        "streamingImageId": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
CreateStreamingSessionStreamRequestRequestTypeDef = TypedDict(
    "CreateStreamingSessionStreamRequestRequestTypeDef",
    {
        "sessionId": str,
        "studioId": str,
        "clientToken": NotRequired[str],
        "expirationInSeconds": NotRequired[int],
    },
)
StreamingSessionStreamTypeDef = TypedDict(
    "StreamingSessionStreamTypeDef",
    {
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "expiresAt": NotRequired[datetime],
        "ownedBy": NotRequired[str],
        "state": NotRequired[StreamingSessionStreamStateType],
        "statusCode": NotRequired[StreamingSessionStreamStatusCodeType],
        "streamId": NotRequired[str],
        "url": NotRequired[str],
    },
)
ScriptParameterKeyValueTypeDef = TypedDict(
    "ScriptParameterKeyValueTypeDef",
    {
        "key": NotRequired[str],
        "value": NotRequired[str],
    },
)
StudioComponentInitializationScriptTypeDef = TypedDict(
    "StudioComponentInitializationScriptTypeDef",
    {
        "launchProfileProtocolVersion": NotRequired[str],
        "platform": NotRequired[LaunchProfilePlatformType],
        "runContext": NotRequired[StudioComponentInitializationScriptRunContextType],
        "script": NotRequired[str],
    },
)
StudioEncryptionConfigurationTypeDef = TypedDict(
    "StudioEncryptionConfigurationTypeDef",
    {
        "keyType": StudioEncryptionConfigurationKeyTypeType,
        "keyArn": NotRequired[str],
    },
)
DeleteLaunchProfileMemberRequestRequestTypeDef = TypedDict(
    "DeleteLaunchProfileMemberRequestRequestTypeDef",
    {
        "launchProfileId": str,
        "principalId": str,
        "studioId": str,
        "clientToken": NotRequired[str],
    },
)
DeleteLaunchProfileRequestRequestTypeDef = TypedDict(
    "DeleteLaunchProfileRequestRequestTypeDef",
    {
        "launchProfileId": str,
        "studioId": str,
        "clientToken": NotRequired[str],
    },
)
DeleteStreamingImageRequestRequestTypeDef = TypedDict(
    "DeleteStreamingImageRequestRequestTypeDef",
    {
        "streamingImageId": str,
        "studioId": str,
        "clientToken": NotRequired[str],
    },
)
DeleteStreamingSessionRequestRequestTypeDef = TypedDict(
    "DeleteStreamingSessionRequestRequestTypeDef",
    {
        "sessionId": str,
        "studioId": str,
        "clientToken": NotRequired[str],
    },
)
DeleteStudioComponentRequestRequestTypeDef = TypedDict(
    "DeleteStudioComponentRequestRequestTypeDef",
    {
        "studioComponentId": str,
        "studioId": str,
        "clientToken": NotRequired[str],
    },
)
DeleteStudioMemberRequestRequestTypeDef = TypedDict(
    "DeleteStudioMemberRequestRequestTypeDef",
    {
        "principalId": str,
        "studioId": str,
        "clientToken": NotRequired[str],
    },
)
DeleteStudioRequestRequestTypeDef = TypedDict(
    "DeleteStudioRequestRequestTypeDef",
    {
        "studioId": str,
        "clientToken": NotRequired[str],
    },
)
EulaTypeDef = TypedDict(
    "EulaTypeDef",
    {
        "content": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "eulaId": NotRequired[str],
        "name": NotRequired[str],
        "updatedAt": NotRequired[datetime],
    },
)
GetEulaRequestRequestTypeDef = TypedDict(
    "GetEulaRequestRequestTypeDef",
    {
        "eulaId": str,
    },
)
GetLaunchProfileDetailsRequestRequestTypeDef = TypedDict(
    "GetLaunchProfileDetailsRequestRequestTypeDef",
    {
        "launchProfileId": str,
        "studioId": str,
    },
)
StudioComponentSummaryTypeDef = TypedDict(
    "StudioComponentSummaryTypeDef",
    {
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "description": NotRequired[str],
        "name": NotRequired[str],
        "studioComponentId": NotRequired[str],
        "subtype": NotRequired[StudioComponentSubtypeType],
        "type": NotRequired[StudioComponentTypeType],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
    },
)
GetLaunchProfileInitializationRequestRequestTypeDef = TypedDict(
    "GetLaunchProfileInitializationRequestRequestTypeDef",
    {
        "launchProfileId": str,
        "launchProfileProtocolVersions": Sequence[str],
        "launchPurpose": str,
        "platform": str,
        "studioId": str,
    },
)
GetLaunchProfileMemberRequestRequestTypeDef = TypedDict(
    "GetLaunchProfileMemberRequestRequestTypeDef",
    {
        "launchProfileId": str,
        "principalId": str,
        "studioId": str,
    },
)
LaunchProfileMembershipTypeDef = TypedDict(
    "LaunchProfileMembershipTypeDef",
    {
        "identityStoreId": NotRequired[str],
        "persona": NotRequired[Literal["USER"]],
        "principalId": NotRequired[str],
        "sid": NotRequired[str],
    },
)
WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": NotRequired[int],
        "MaxAttempts": NotRequired[int],
    },
)
GetLaunchProfileRequestRequestTypeDef = TypedDict(
    "GetLaunchProfileRequestRequestTypeDef",
    {
        "launchProfileId": str,
        "studioId": str,
    },
)
GetStreamingImageRequestRequestTypeDef = TypedDict(
    "GetStreamingImageRequestRequestTypeDef",
    {
        "streamingImageId": str,
        "studioId": str,
    },
)
GetStreamingSessionBackupRequestRequestTypeDef = TypedDict(
    "GetStreamingSessionBackupRequestRequestTypeDef",
    {
        "backupId": str,
        "studioId": str,
    },
)
StreamingSessionBackupTypeDef = TypedDict(
    "StreamingSessionBackupTypeDef",
    {
        "arn": NotRequired[str],
        "backupId": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "launchProfileId": NotRequired[str],
        "ownedBy": NotRequired[str],
        "sessionId": NotRequired[str],
        "state": NotRequired[StreamingSessionStateType],
        "statusCode": NotRequired[StreamingSessionStatusCodeType],
        "statusMessage": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
    },
)
GetStreamingSessionRequestRequestTypeDef = TypedDict(
    "GetStreamingSessionRequestRequestTypeDef",
    {
        "sessionId": str,
        "studioId": str,
    },
)
GetStreamingSessionStreamRequestRequestTypeDef = TypedDict(
    "GetStreamingSessionStreamRequestRequestTypeDef",
    {
        "sessionId": str,
        "streamId": str,
        "studioId": str,
    },
)
GetStudioComponentRequestRequestTypeDef = TypedDict(
    "GetStudioComponentRequestRequestTypeDef",
    {
        "studioComponentId": str,
        "studioId": str,
    },
)
GetStudioMemberRequestRequestTypeDef = TypedDict(
    "GetStudioMemberRequestRequestTypeDef",
    {
        "principalId": str,
        "studioId": str,
    },
)
StudioMembershipTypeDef = TypedDict(
    "StudioMembershipTypeDef",
    {
        "identityStoreId": NotRequired[str],
        "persona": NotRequired[Literal["ADMINISTRATOR"]],
        "principalId": NotRequired[str],
        "sid": NotRequired[str],
    },
)
GetStudioRequestRequestTypeDef = TypedDict(
    "GetStudioRequestRequestTypeDef",
    {
        "studioId": str,
    },
)
LaunchProfileInitializationScriptTypeDef = TypedDict(
    "LaunchProfileInitializationScriptTypeDef",
    {
        "runtimeRoleArn": NotRequired[str],
        "script": NotRequired[str],
        "secureInitializationRoleArn": NotRequired[str],
        "studioComponentId": NotRequired[str],
        "studioComponentName": NotRequired[str],
    },
)
ValidationResultTypeDef = TypedDict(
    "ValidationResultTypeDef",
    {
        "state": LaunchProfileValidationStateType,
        "statusCode": LaunchProfileValidationStatusCodeType,
        "statusMessage": str,
        "type": LaunchProfileValidationTypeType,
    },
)
LicenseServiceConfigurationTypeDef = TypedDict(
    "LicenseServiceConfigurationTypeDef",
    {
        "endpoint": NotRequired[str],
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
ListEulaAcceptancesRequestRequestTypeDef = TypedDict(
    "ListEulaAcceptancesRequestRequestTypeDef",
    {
        "studioId": str,
        "eulaIds": NotRequired[Sequence[str]],
        "nextToken": NotRequired[str],
    },
)
ListEulasRequestRequestTypeDef = TypedDict(
    "ListEulasRequestRequestTypeDef",
    {
        "eulaIds": NotRequired[Sequence[str]],
        "nextToken": NotRequired[str],
    },
)
ListLaunchProfileMembersRequestRequestTypeDef = TypedDict(
    "ListLaunchProfileMembersRequestRequestTypeDef",
    {
        "launchProfileId": str,
        "studioId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListLaunchProfilesRequestRequestTypeDef = TypedDict(
    "ListLaunchProfilesRequestRequestTypeDef",
    {
        "studioId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "principalId": NotRequired[str],
        "states": NotRequired[Sequence[LaunchProfileStateType]],
    },
)
ListStreamingImagesRequestRequestTypeDef = TypedDict(
    "ListStreamingImagesRequestRequestTypeDef",
    {
        "studioId": str,
        "nextToken": NotRequired[str],
        "owner": NotRequired[str],
    },
)
ListStreamingSessionBackupsRequestRequestTypeDef = TypedDict(
    "ListStreamingSessionBackupsRequestRequestTypeDef",
    {
        "studioId": str,
        "nextToken": NotRequired[str],
        "ownedBy": NotRequired[str],
    },
)
ListStreamingSessionsRequestRequestTypeDef = TypedDict(
    "ListStreamingSessionsRequestRequestTypeDef",
    {
        "studioId": str,
        "createdBy": NotRequired[str],
        "nextToken": NotRequired[str],
        "ownedBy": NotRequired[str],
        "sessionIds": NotRequired[str],
    },
)
ListStudioComponentsRequestRequestTypeDef = TypedDict(
    "ListStudioComponentsRequestRequestTypeDef",
    {
        "studioId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "states": NotRequired[Sequence[StudioComponentStateType]],
        "types": NotRequired[Sequence[StudioComponentTypeType]],
    },
)
ListStudioMembersRequestRequestTypeDef = TypedDict(
    "ListStudioMembersRequestRequestTypeDef",
    {
        "studioId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListStudiosRequestRequestTypeDef = TypedDict(
    "ListStudiosRequestRequestTypeDef",
    {
        "nextToken": NotRequired[str],
    },
)
ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)
NewLaunchProfileMemberTypeDef = TypedDict(
    "NewLaunchProfileMemberTypeDef",
    {
        "persona": Literal["USER"],
        "principalId": str,
    },
)
NewStudioMemberTypeDef = TypedDict(
    "NewStudioMemberTypeDef",
    {
        "persona": Literal["ADMINISTRATOR"],
        "principalId": str,
    },
)
SharedFileSystemConfigurationTypeDef = TypedDict(
    "SharedFileSystemConfigurationTypeDef",
    {
        "endpoint": NotRequired[str],
        "fileSystemId": NotRequired[str],
        "linuxMountPoint": NotRequired[str],
        "shareName": NotRequired[str],
        "windowsMountDrive": NotRequired[str],
    },
)
StartStreamingSessionRequestRequestTypeDef = TypedDict(
    "StartStreamingSessionRequestRequestTypeDef",
    {
        "sessionId": str,
        "studioId": str,
        "backupId": NotRequired[str],
        "clientToken": NotRequired[str],
    },
)
StartStudioSSOConfigurationRepairRequestRequestTypeDef = TypedDict(
    "StartStudioSSOConfigurationRepairRequestRequestTypeDef",
    {
        "studioId": str,
        "clientToken": NotRequired[str],
    },
)
StopStreamingSessionRequestRequestTypeDef = TypedDict(
    "StopStreamingSessionRequestRequestTypeDef",
    {
        "sessionId": str,
        "studioId": str,
        "clientToken": NotRequired[str],
        "volumeRetentionMode": NotRequired[VolumeRetentionModeType],
    },
)
StreamConfigurationSessionBackupTypeDef = TypedDict(
    "StreamConfigurationSessionBackupTypeDef",
    {
        "maxBackupsToRetain": NotRequired[int],
        "mode": NotRequired[SessionBackupModeType],
    },
)
VolumeConfigurationTypeDef = TypedDict(
    "VolumeConfigurationTypeDef",
    {
        "iops": NotRequired[int],
        "size": NotRequired[int],
        "throughput": NotRequired[int],
    },
)
StreamingSessionStorageRootTypeDef = TypedDict(
    "StreamingSessionStorageRootTypeDef",
    {
        "linux": NotRequired[str],
        "windows": NotRequired[str],
    },
)
StreamingImageEncryptionConfigurationTypeDef = TypedDict(
    "StreamingImageEncryptionConfigurationTypeDef",
    {
        "keyType": Literal["CUSTOMER_MANAGED_KEY"],
        "keyArn": NotRequired[str],
    },
)
TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": NotRequired[Mapping[str, str]],
    },
)
UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)
UpdateLaunchProfileMemberRequestRequestTypeDef = TypedDict(
    "UpdateLaunchProfileMemberRequestRequestTypeDef",
    {
        "launchProfileId": str,
        "persona": Literal["USER"],
        "principalId": str,
        "studioId": str,
        "clientToken": NotRequired[str],
    },
)
UpdateStreamingImageRequestRequestTypeDef = TypedDict(
    "UpdateStreamingImageRequestRequestTypeDef",
    {
        "streamingImageId": str,
        "studioId": str,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "name": NotRequired[str],
    },
)
UpdateStudioRequestRequestTypeDef = TypedDict(
    "UpdateStudioRequestRequestTypeDef",
    {
        "studioId": str,
        "adminRoleArn": NotRequired[str],
        "clientToken": NotRequired[str],
        "displayName": NotRequired[str],
        "userRoleArn": NotRequired[str],
    },
)
AcceptEulasResponseTypeDef = TypedDict(
    "AcceptEulasResponseTypeDef",
    {
        "eulaAcceptances": List[EulaAcceptanceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListEulaAcceptancesResponseTypeDef = TypedDict(
    "ListEulaAcceptancesResponseTypeDef",
    {
        "eulaAcceptances": List[EulaAcceptanceTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ActiveDirectoryConfigurationOutputTypeDef = TypedDict(
    "ActiveDirectoryConfigurationOutputTypeDef",
    {
        "computerAttributes": NotRequired[List[ActiveDirectoryComputerAttributeTypeDef]],
        "directoryId": NotRequired[str],
        "organizationalUnitDistinguishedName": NotRequired[str],
    },
)
ActiveDirectoryConfigurationTypeDef = TypedDict(
    "ActiveDirectoryConfigurationTypeDef",
    {
        "computerAttributes": NotRequired[Sequence[ActiveDirectoryComputerAttributeTypeDef]],
        "directoryId": NotRequired[str],
        "organizationalUnitDistinguishedName": NotRequired[str],
    },
)
LaunchProfileInitializationActiveDirectoryTypeDef = TypedDict(
    "LaunchProfileInitializationActiveDirectoryTypeDef",
    {
        "computerAttributes": NotRequired[List[ActiveDirectoryComputerAttributeTypeDef]],
        "directoryId": NotRequired[str],
        "directoryName": NotRequired[str],
        "dnsIpAddresses": NotRequired[List[str]],
        "organizationalUnitDistinguishedName": NotRequired[str],
        "studioComponentId": NotRequired[str],
        "studioComponentName": NotRequired[str],
    },
)
CreateStreamingSessionStreamResponseTypeDef = TypedDict(
    "CreateStreamingSessionStreamResponseTypeDef",
    {
        "stream": StreamingSessionStreamTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetStreamingSessionStreamResponseTypeDef = TypedDict(
    "GetStreamingSessionStreamResponseTypeDef",
    {
        "stream": StreamingSessionStreamTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateStudioRequestRequestTypeDef = TypedDict(
    "CreateStudioRequestRequestTypeDef",
    {
        "adminRoleArn": str,
        "displayName": str,
        "studioName": str,
        "userRoleArn": str,
        "clientToken": NotRequired[str],
        "studioEncryptionConfiguration": NotRequired[StudioEncryptionConfigurationTypeDef],
        "tags": NotRequired[Mapping[str, str]],
    },
)
StudioTypeDef = TypedDict(
    "StudioTypeDef",
    {
        "adminRoleArn": NotRequired[str],
        "arn": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "displayName": NotRequired[str],
        "homeRegion": NotRequired[str],
        "ssoClientId": NotRequired[str],
        "state": NotRequired[StudioStateType],
        "statusCode": NotRequired[StudioStatusCodeType],
        "statusMessage": NotRequired[str],
        "studioEncryptionConfiguration": NotRequired[StudioEncryptionConfigurationTypeDef],
        "studioId": NotRequired[str],
        "studioName": NotRequired[str],
        "studioUrl": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
        "updatedAt": NotRequired[datetime],
        "userRoleArn": NotRequired[str],
    },
)
GetEulaResponseTypeDef = TypedDict(
    "GetEulaResponseTypeDef",
    {
        "eula": EulaTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListEulasResponseTypeDef = TypedDict(
    "ListEulasResponseTypeDef",
    {
        "eulas": List[EulaTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetLaunchProfileMemberResponseTypeDef = TypedDict(
    "GetLaunchProfileMemberResponseTypeDef",
    {
        "member": LaunchProfileMembershipTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListLaunchProfileMembersResponseTypeDef = TypedDict(
    "ListLaunchProfileMembersResponseTypeDef",
    {
        "members": List[LaunchProfileMembershipTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateLaunchProfileMemberResponseTypeDef = TypedDict(
    "UpdateLaunchProfileMemberResponseTypeDef",
    {
        "member": LaunchProfileMembershipTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetLaunchProfileRequestLaunchProfileDeletedWaitTypeDef = TypedDict(
    "GetLaunchProfileRequestLaunchProfileDeletedWaitTypeDef",
    {
        "launchProfileId": str,
        "studioId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
GetLaunchProfileRequestLaunchProfileReadyWaitTypeDef = TypedDict(
    "GetLaunchProfileRequestLaunchProfileReadyWaitTypeDef",
    {
        "launchProfileId": str,
        "studioId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
GetStreamingImageRequestStreamingImageDeletedWaitTypeDef = TypedDict(
    "GetStreamingImageRequestStreamingImageDeletedWaitTypeDef",
    {
        "streamingImageId": str,
        "studioId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
GetStreamingImageRequestStreamingImageReadyWaitTypeDef = TypedDict(
    "GetStreamingImageRequestStreamingImageReadyWaitTypeDef",
    {
        "streamingImageId": str,
        "studioId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
GetStreamingSessionRequestStreamingSessionDeletedWaitTypeDef = TypedDict(
    "GetStreamingSessionRequestStreamingSessionDeletedWaitTypeDef",
    {
        "sessionId": str,
        "studioId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
GetStreamingSessionRequestStreamingSessionReadyWaitTypeDef = TypedDict(
    "GetStreamingSessionRequestStreamingSessionReadyWaitTypeDef",
    {
        "sessionId": str,
        "studioId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
GetStreamingSessionRequestStreamingSessionStoppedWaitTypeDef = TypedDict(
    "GetStreamingSessionRequestStreamingSessionStoppedWaitTypeDef",
    {
        "sessionId": str,
        "studioId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
GetStreamingSessionStreamRequestStreamingSessionStreamReadyWaitTypeDef = TypedDict(
    "GetStreamingSessionStreamRequestStreamingSessionStreamReadyWaitTypeDef",
    {
        "sessionId": str,
        "streamId": str,
        "studioId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
GetStudioComponentRequestStudioComponentDeletedWaitTypeDef = TypedDict(
    "GetStudioComponentRequestStudioComponentDeletedWaitTypeDef",
    {
        "studioComponentId": str,
        "studioId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
GetStudioComponentRequestStudioComponentReadyWaitTypeDef = TypedDict(
    "GetStudioComponentRequestStudioComponentReadyWaitTypeDef",
    {
        "studioComponentId": str,
        "studioId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
GetStudioRequestStudioDeletedWaitTypeDef = TypedDict(
    "GetStudioRequestStudioDeletedWaitTypeDef",
    {
        "studioId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
GetStudioRequestStudioReadyWaitTypeDef = TypedDict(
    "GetStudioRequestStudioReadyWaitTypeDef",
    {
        "studioId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
GetStreamingSessionBackupResponseTypeDef = TypedDict(
    "GetStreamingSessionBackupResponseTypeDef",
    {
        "streamingSessionBackup": StreamingSessionBackupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListStreamingSessionBackupsResponseTypeDef = TypedDict(
    "ListStreamingSessionBackupsResponseTypeDef",
    {
        "nextToken": str,
        "streamingSessionBackups": List[StreamingSessionBackupTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetStudioMemberResponseTypeDef = TypedDict(
    "GetStudioMemberResponseTypeDef",
    {
        "member": StudioMembershipTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListStudioMembersResponseTypeDef = TypedDict(
    "ListStudioMembersResponseTypeDef",
    {
        "members": List[StudioMembershipTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListEulaAcceptancesRequestListEulaAcceptancesPaginateTypeDef = TypedDict(
    "ListEulaAcceptancesRequestListEulaAcceptancesPaginateTypeDef",
    {
        "studioId": str,
        "eulaIds": NotRequired[Sequence[str]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListEulasRequestListEulasPaginateTypeDef = TypedDict(
    "ListEulasRequestListEulasPaginateTypeDef",
    {
        "eulaIds": NotRequired[Sequence[str]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListLaunchProfileMembersRequestListLaunchProfileMembersPaginateTypeDef = TypedDict(
    "ListLaunchProfileMembersRequestListLaunchProfileMembersPaginateTypeDef",
    {
        "launchProfileId": str,
        "studioId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListLaunchProfilesRequestListLaunchProfilesPaginateTypeDef = TypedDict(
    "ListLaunchProfilesRequestListLaunchProfilesPaginateTypeDef",
    {
        "studioId": str,
        "principalId": NotRequired[str],
        "states": NotRequired[Sequence[LaunchProfileStateType]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListStreamingImagesRequestListStreamingImagesPaginateTypeDef = TypedDict(
    "ListStreamingImagesRequestListStreamingImagesPaginateTypeDef",
    {
        "studioId": str,
        "owner": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListStreamingSessionBackupsRequestListStreamingSessionBackupsPaginateTypeDef = TypedDict(
    "ListStreamingSessionBackupsRequestListStreamingSessionBackupsPaginateTypeDef",
    {
        "studioId": str,
        "ownedBy": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListStreamingSessionsRequestListStreamingSessionsPaginateTypeDef = TypedDict(
    "ListStreamingSessionsRequestListStreamingSessionsPaginateTypeDef",
    {
        "studioId": str,
        "createdBy": NotRequired[str],
        "ownedBy": NotRequired[str],
        "sessionIds": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListStudioComponentsRequestListStudioComponentsPaginateTypeDef = TypedDict(
    "ListStudioComponentsRequestListStudioComponentsPaginateTypeDef",
    {
        "studioId": str,
        "states": NotRequired[Sequence[StudioComponentStateType]],
        "types": NotRequired[Sequence[StudioComponentTypeType]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListStudioMembersRequestListStudioMembersPaginateTypeDef = TypedDict(
    "ListStudioMembersRequestListStudioMembersPaginateTypeDef",
    {
        "studioId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListStudiosRequestListStudiosPaginateTypeDef = TypedDict(
    "ListStudiosRequestListStudiosPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
PutLaunchProfileMembersRequestRequestTypeDef = TypedDict(
    "PutLaunchProfileMembersRequestRequestTypeDef",
    {
        "identityStoreId": str,
        "launchProfileId": str,
        "members": Sequence[NewLaunchProfileMemberTypeDef],
        "studioId": str,
        "clientToken": NotRequired[str],
    },
)
PutStudioMembersRequestRequestTypeDef = TypedDict(
    "PutStudioMembersRequestRequestTypeDef",
    {
        "identityStoreId": str,
        "members": Sequence[NewStudioMemberTypeDef],
        "studioId": str,
        "clientToken": NotRequired[str],
    },
)
StreamingSessionTypeDef = TypedDict(
    "StreamingSessionTypeDef",
    {
        "arn": NotRequired[str],
        "automaticTerminationMode": NotRequired[AutomaticTerminationModeType],
        "backupMode": NotRequired[SessionBackupModeType],
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "ec2InstanceType": NotRequired[str],
        "launchProfileId": NotRequired[str],
        "maxBackupsToRetain": NotRequired[int],
        "ownedBy": NotRequired[str],
        "sessionId": NotRequired[str],
        "sessionPersistenceMode": NotRequired[SessionPersistenceModeType],
        "startedAt": NotRequired[datetime],
        "startedBy": NotRequired[str],
        "startedFromBackupId": NotRequired[str],
        "state": NotRequired[StreamingSessionStateType],
        "statusCode": NotRequired[StreamingSessionStatusCodeType],
        "statusMessage": NotRequired[str],
        "stopAt": NotRequired[datetime],
        "stoppedAt": NotRequired[datetime],
        "stoppedBy": NotRequired[str],
        "streamingImageId": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
        "terminateAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
        "volumeConfiguration": NotRequired[VolumeConfigurationTypeDef],
        "volumeRetentionMode": NotRequired[VolumeRetentionModeType],
    },
)
StreamConfigurationSessionStorageOutputTypeDef = TypedDict(
    "StreamConfigurationSessionStorageOutputTypeDef",
    {
        "mode": List[Literal["UPLOAD"]],
        "root": NotRequired[StreamingSessionStorageRootTypeDef],
    },
)
StreamConfigurationSessionStorageTypeDef = TypedDict(
    "StreamConfigurationSessionStorageTypeDef",
    {
        "mode": Sequence[Literal["UPLOAD"]],
        "root": NotRequired[StreamingSessionStorageRootTypeDef],
    },
)
StreamingImageTypeDef = TypedDict(
    "StreamingImageTypeDef",
    {
        "arn": NotRequired[str],
        "description": NotRequired[str],
        "ec2ImageId": NotRequired[str],
        "encryptionConfiguration": NotRequired[StreamingImageEncryptionConfigurationTypeDef],
        "eulaIds": NotRequired[List[str]],
        "name": NotRequired[str],
        "owner": NotRequired[str],
        "platform": NotRequired[str],
        "state": NotRequired[StreamingImageStateType],
        "statusCode": NotRequired[StreamingImageStatusCodeType],
        "statusMessage": NotRequired[str],
        "streamingImageId": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
    },
)
StudioComponentConfigurationOutputTypeDef = TypedDict(
    "StudioComponentConfigurationOutputTypeDef",
    {
        "activeDirectoryConfiguration": NotRequired[ActiveDirectoryConfigurationOutputTypeDef],
        "computeFarmConfiguration": NotRequired[ComputeFarmConfigurationTypeDef],
        "licenseServiceConfiguration": NotRequired[LicenseServiceConfigurationTypeDef],
        "sharedFileSystemConfiguration": NotRequired[SharedFileSystemConfigurationTypeDef],
    },
)
ActiveDirectoryConfigurationUnionTypeDef = Union[
    ActiveDirectoryConfigurationTypeDef, ActiveDirectoryConfigurationOutputTypeDef
]
LaunchProfileInitializationTypeDef = TypedDict(
    "LaunchProfileInitializationTypeDef",
    {
        "activeDirectory": NotRequired[LaunchProfileInitializationActiveDirectoryTypeDef],
        "ec2SecurityGroupIds": NotRequired[List[str]],
        "launchProfileId": NotRequired[str],
        "launchProfileProtocolVersion": NotRequired[str],
        "launchPurpose": NotRequired[str],
        "name": NotRequired[str],
        "platform": NotRequired[LaunchProfilePlatformType],
        "systemInitializationScripts": NotRequired[List[LaunchProfileInitializationScriptTypeDef]],
        "userInitializationScripts": NotRequired[List[LaunchProfileInitializationScriptTypeDef]],
    },
)
CreateStudioResponseTypeDef = TypedDict(
    "CreateStudioResponseTypeDef",
    {
        "studio": StudioTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteStudioResponseTypeDef = TypedDict(
    "DeleteStudioResponseTypeDef",
    {
        "studio": StudioTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetStudioResponseTypeDef = TypedDict(
    "GetStudioResponseTypeDef",
    {
        "studio": StudioTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListStudiosResponseTypeDef = TypedDict(
    "ListStudiosResponseTypeDef",
    {
        "nextToken": str,
        "studios": List[StudioTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartStudioSSOConfigurationRepairResponseTypeDef = TypedDict(
    "StartStudioSSOConfigurationRepairResponseTypeDef",
    {
        "studio": StudioTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateStudioResponseTypeDef = TypedDict(
    "UpdateStudioResponseTypeDef",
    {
        "studio": StudioTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateStreamingSessionResponseTypeDef = TypedDict(
    "CreateStreamingSessionResponseTypeDef",
    {
        "session": StreamingSessionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteStreamingSessionResponseTypeDef = TypedDict(
    "DeleteStreamingSessionResponseTypeDef",
    {
        "session": StreamingSessionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetStreamingSessionResponseTypeDef = TypedDict(
    "GetStreamingSessionResponseTypeDef",
    {
        "session": StreamingSessionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListStreamingSessionsResponseTypeDef = TypedDict(
    "ListStreamingSessionsResponseTypeDef",
    {
        "nextToken": str,
        "sessions": List[StreamingSessionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartStreamingSessionResponseTypeDef = TypedDict(
    "StartStreamingSessionResponseTypeDef",
    {
        "session": StreamingSessionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StopStreamingSessionResponseTypeDef = TypedDict(
    "StopStreamingSessionResponseTypeDef",
    {
        "session": StreamingSessionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StreamConfigurationTypeDef = TypedDict(
    "StreamConfigurationTypeDef",
    {
        "clipboardMode": StreamingClipboardModeType,
        "ec2InstanceTypes": List[StreamingInstanceTypeType],
        "streamingImageIds": List[str],
        "automaticTerminationMode": NotRequired[AutomaticTerminationModeType],
        "maxSessionLengthInMinutes": NotRequired[int],
        "maxStoppedSessionLengthInMinutes": NotRequired[int],
        "sessionBackup": NotRequired[StreamConfigurationSessionBackupTypeDef],
        "sessionPersistenceMode": NotRequired[SessionPersistenceModeType],
        "sessionStorage": NotRequired[StreamConfigurationSessionStorageOutputTypeDef],
        "volumeConfiguration": NotRequired[VolumeConfigurationTypeDef],
    },
)
StreamConfigurationSessionStorageUnionTypeDef = Union[
    StreamConfigurationSessionStorageTypeDef, StreamConfigurationSessionStorageOutputTypeDef
]
CreateStreamingImageResponseTypeDef = TypedDict(
    "CreateStreamingImageResponseTypeDef",
    {
        "streamingImage": StreamingImageTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteStreamingImageResponseTypeDef = TypedDict(
    "DeleteStreamingImageResponseTypeDef",
    {
        "streamingImage": StreamingImageTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetStreamingImageResponseTypeDef = TypedDict(
    "GetStreamingImageResponseTypeDef",
    {
        "streamingImage": StreamingImageTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListStreamingImagesResponseTypeDef = TypedDict(
    "ListStreamingImagesResponseTypeDef",
    {
        "nextToken": str,
        "streamingImages": List[StreamingImageTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateStreamingImageResponseTypeDef = TypedDict(
    "UpdateStreamingImageResponseTypeDef",
    {
        "streamingImage": StreamingImageTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StudioComponentTypeDef = TypedDict(
    "StudioComponentTypeDef",
    {
        "arn": NotRequired[str],
        "configuration": NotRequired[StudioComponentConfigurationOutputTypeDef],
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "description": NotRequired[str],
        "ec2SecurityGroupIds": NotRequired[List[str]],
        "initializationScripts": NotRequired[List[StudioComponentInitializationScriptTypeDef]],
        "name": NotRequired[str],
        "runtimeRoleArn": NotRequired[str],
        "scriptParameters": NotRequired[List[ScriptParameterKeyValueTypeDef]],
        "secureInitializationRoleArn": NotRequired[str],
        "state": NotRequired[StudioComponentStateType],
        "statusCode": NotRequired[StudioComponentStatusCodeType],
        "statusMessage": NotRequired[str],
        "studioComponentId": NotRequired[str],
        "subtype": NotRequired[StudioComponentSubtypeType],
        "tags": NotRequired[Dict[str, str]],
        "type": NotRequired[StudioComponentTypeType],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
    },
)
StudioComponentConfigurationTypeDef = TypedDict(
    "StudioComponentConfigurationTypeDef",
    {
        "activeDirectoryConfiguration": NotRequired[ActiveDirectoryConfigurationUnionTypeDef],
        "computeFarmConfiguration": NotRequired[ComputeFarmConfigurationTypeDef],
        "licenseServiceConfiguration": NotRequired[LicenseServiceConfigurationTypeDef],
        "sharedFileSystemConfiguration": NotRequired[SharedFileSystemConfigurationTypeDef],
    },
)
GetLaunchProfileInitializationResponseTypeDef = TypedDict(
    "GetLaunchProfileInitializationResponseTypeDef",
    {
        "launchProfileInitialization": LaunchProfileInitializationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
LaunchProfileTypeDef = TypedDict(
    "LaunchProfileTypeDef",
    {
        "arn": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "description": NotRequired[str],
        "ec2SubnetIds": NotRequired[List[str]],
        "launchProfileId": NotRequired[str],
        "launchProfileProtocolVersions": NotRequired[List[str]],
        "name": NotRequired[str],
        "state": NotRequired[LaunchProfileStateType],
        "statusCode": NotRequired[LaunchProfileStatusCodeType],
        "statusMessage": NotRequired[str],
        "streamConfiguration": NotRequired[StreamConfigurationTypeDef],
        "studioComponentIds": NotRequired[List[str]],
        "tags": NotRequired[Dict[str, str]],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
        "validationResults": NotRequired[List[ValidationResultTypeDef]],
    },
)
StreamConfigurationCreateTypeDef = TypedDict(
    "StreamConfigurationCreateTypeDef",
    {
        "clipboardMode": StreamingClipboardModeType,
        "ec2InstanceTypes": Sequence[StreamingInstanceTypeType],
        "streamingImageIds": Sequence[str],
        "automaticTerminationMode": NotRequired[AutomaticTerminationModeType],
        "maxSessionLengthInMinutes": NotRequired[int],
        "maxStoppedSessionLengthInMinutes": NotRequired[int],
        "sessionBackup": NotRequired[StreamConfigurationSessionBackupTypeDef],
        "sessionPersistenceMode": NotRequired[SessionPersistenceModeType],
        "sessionStorage": NotRequired[StreamConfigurationSessionStorageUnionTypeDef],
        "volumeConfiguration": NotRequired[VolumeConfigurationTypeDef],
    },
)
CreateStudioComponentResponseTypeDef = TypedDict(
    "CreateStudioComponentResponseTypeDef",
    {
        "studioComponent": StudioComponentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteStudioComponentResponseTypeDef = TypedDict(
    "DeleteStudioComponentResponseTypeDef",
    {
        "studioComponent": StudioComponentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetStudioComponentResponseTypeDef = TypedDict(
    "GetStudioComponentResponseTypeDef",
    {
        "studioComponent": StudioComponentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListStudioComponentsResponseTypeDef = TypedDict(
    "ListStudioComponentsResponseTypeDef",
    {
        "nextToken": str,
        "studioComponents": List[StudioComponentTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateStudioComponentResponseTypeDef = TypedDict(
    "UpdateStudioComponentResponseTypeDef",
    {
        "studioComponent": StudioComponentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateStudioComponentRequestRequestTypeDef = TypedDict(
    "CreateStudioComponentRequestRequestTypeDef",
    {
        "name": str,
        "studioId": str,
        "type": StudioComponentTypeType,
        "clientToken": NotRequired[str],
        "configuration": NotRequired[StudioComponentConfigurationTypeDef],
        "description": NotRequired[str],
        "ec2SecurityGroupIds": NotRequired[Sequence[str]],
        "initializationScripts": NotRequired[Sequence[StudioComponentInitializationScriptTypeDef]],
        "runtimeRoleArn": NotRequired[str],
        "scriptParameters": NotRequired[Sequence[ScriptParameterKeyValueTypeDef]],
        "secureInitializationRoleArn": NotRequired[str],
        "subtype": NotRequired[StudioComponentSubtypeType],
        "tags": NotRequired[Mapping[str, str]],
    },
)
UpdateStudioComponentRequestRequestTypeDef = TypedDict(
    "UpdateStudioComponentRequestRequestTypeDef",
    {
        "studioComponentId": str,
        "studioId": str,
        "clientToken": NotRequired[str],
        "configuration": NotRequired[StudioComponentConfigurationTypeDef],
        "description": NotRequired[str],
        "ec2SecurityGroupIds": NotRequired[Sequence[str]],
        "initializationScripts": NotRequired[Sequence[StudioComponentInitializationScriptTypeDef]],
        "name": NotRequired[str],
        "runtimeRoleArn": NotRequired[str],
        "scriptParameters": NotRequired[Sequence[ScriptParameterKeyValueTypeDef]],
        "secureInitializationRoleArn": NotRequired[str],
        "subtype": NotRequired[StudioComponentSubtypeType],
        "type": NotRequired[StudioComponentTypeType],
    },
)
CreateLaunchProfileResponseTypeDef = TypedDict(
    "CreateLaunchProfileResponseTypeDef",
    {
        "launchProfile": LaunchProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteLaunchProfileResponseTypeDef = TypedDict(
    "DeleteLaunchProfileResponseTypeDef",
    {
        "launchProfile": LaunchProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetLaunchProfileDetailsResponseTypeDef = TypedDict(
    "GetLaunchProfileDetailsResponseTypeDef",
    {
        "launchProfile": LaunchProfileTypeDef,
        "streamingImages": List[StreamingImageTypeDef],
        "studioComponentSummaries": List[StudioComponentSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetLaunchProfileResponseTypeDef = TypedDict(
    "GetLaunchProfileResponseTypeDef",
    {
        "launchProfile": LaunchProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListLaunchProfilesResponseTypeDef = TypedDict(
    "ListLaunchProfilesResponseTypeDef",
    {
        "launchProfiles": List[LaunchProfileTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateLaunchProfileResponseTypeDef = TypedDict(
    "UpdateLaunchProfileResponseTypeDef",
    {
        "launchProfile": LaunchProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateLaunchProfileRequestRequestTypeDef = TypedDict(
    "CreateLaunchProfileRequestRequestTypeDef",
    {
        "ec2SubnetIds": Sequence[str],
        "launchProfileProtocolVersions": Sequence[str],
        "name": str,
        "streamConfiguration": StreamConfigurationCreateTypeDef,
        "studioComponentIds": Sequence[str],
        "studioId": str,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
UpdateLaunchProfileRequestRequestTypeDef = TypedDict(
    "UpdateLaunchProfileRequestRequestTypeDef",
    {
        "launchProfileId": str,
        "studioId": str,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "launchProfileProtocolVersions": NotRequired[Sequence[str]],
        "name": NotRequired[str],
        "streamConfiguration": NotRequired[StreamConfigurationCreateTypeDef],
        "studioComponentIds": NotRequired[Sequence[str]],
    },
)
