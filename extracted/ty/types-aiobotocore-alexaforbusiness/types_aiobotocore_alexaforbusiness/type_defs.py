"""
Type annotations for alexaforbusiness service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/type_defs/)

Usage::

    ```python
    from types_aiobotocore_alexaforbusiness.type_defs import AddressBookDataTypeDef

    data: AddressBookDataTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    BusinessReportFailureCodeType,
    BusinessReportFormatType,
    BusinessReportIntervalType,
    BusinessReportStatusType,
    CommsProtocolType,
    ConferenceProviderTypeType,
    ConnectionStatusType,
    DeviceEventTypeType,
    DeviceStatusDetailCodeType,
    DeviceStatusType,
    DistanceUnitType,
    EnablementTypeFilterType,
    EnablementTypeType,
    EndOfMeetingReminderTypeType,
    EnrollmentStatusType,
    FeatureType,
    NetworkSecurityTypeType,
    PhoneNumberTypeType,
    RequirePinType,
    SkillTypeFilterType,
    SkillTypeType,
    SortValueType,
    TemperatureUnitType,
    WakeWordType,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AddressBookDataTypeDef",
    "AddressBookTypeDef",
    "ApproveSkillRequestRequestTypeDef",
    "AssociateContactWithAddressBookRequestRequestTypeDef",
    "AssociateDeviceWithNetworkProfileRequestRequestTypeDef",
    "AssociateDeviceWithRoomRequestRequestTypeDef",
    "AssociateSkillGroupWithRoomRequestRequestTypeDef",
    "AssociateSkillWithSkillGroupRequestRequestTypeDef",
    "AssociateSkillWithUsersRequestRequestTypeDef",
    "AudioTypeDef",
    "BusinessReportContentRangeTypeDef",
    "BusinessReportRecurrenceTypeDef",
    "BusinessReportS3LocationTypeDef",
    "CategoryTypeDef",
    "ConferencePreferenceTypeDef",
    "IPDialInTypeDef",
    "MeetingSettingTypeDef",
    "PSTNDialInTypeDef",
    "PhoneNumberTypeDef",
    "SipAddressTypeDef",
    "SsmlTypeDef",
    "TextTypeDef",
    "TagTypeDef",
    "ResponseMetadataTypeDef",
    "CreateEndOfMeetingReminderTypeDef",
    "CreateInstantBookingTypeDef",
    "CreateProactiveJoinTypeDef",
    "CreateRequireCheckInTypeDef",
    "DeleteAddressBookRequestRequestTypeDef",
    "DeleteBusinessReportScheduleRequestRequestTypeDef",
    "DeleteConferenceProviderRequestRequestTypeDef",
    "DeleteContactRequestRequestTypeDef",
    "DeleteDeviceRequestRequestTypeDef",
    "DeleteDeviceUsageDataRequestRequestTypeDef",
    "DeleteGatewayGroupRequestRequestTypeDef",
    "DeleteNetworkProfileRequestRequestTypeDef",
    "DeleteProfileRequestRequestTypeDef",
    "DeleteRoomRequestRequestTypeDef",
    "DeleteRoomSkillParameterRequestRequestTypeDef",
    "DeleteSkillAuthorizationRequestRequestTypeDef",
    "DeleteSkillGroupRequestRequestTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DeveloperInfoTypeDef",
    "DeviceEventTypeDef",
    "DeviceNetworkProfileInfoTypeDef",
    "DeviceStatusDetailTypeDef",
    "DisassociateContactFromAddressBookRequestRequestTypeDef",
    "DisassociateDeviceFromRoomRequestRequestTypeDef",
    "DisassociateSkillFromSkillGroupRequestRequestTypeDef",
    "DisassociateSkillFromUsersRequestRequestTypeDef",
    "DisassociateSkillGroupFromRoomRequestRequestTypeDef",
    "EndOfMeetingReminderTypeDef",
    "FilterTypeDef",
    "ForgetSmartHomeAppliancesRequestRequestTypeDef",
    "GatewayGroupSummaryTypeDef",
    "GatewayGroupTypeDef",
    "GatewaySummaryTypeDef",
    "GatewayTypeDef",
    "GetAddressBookRequestRequestTypeDef",
    "GetConferenceProviderRequestRequestTypeDef",
    "GetContactRequestRequestTypeDef",
    "GetDeviceRequestRequestTypeDef",
    "GetGatewayGroupRequestRequestTypeDef",
    "GetGatewayRequestRequestTypeDef",
    "GetNetworkProfileRequestRequestTypeDef",
    "NetworkProfileTypeDef",
    "GetProfileRequestRequestTypeDef",
    "GetRoomRequestRequestTypeDef",
    "RoomTypeDef",
    "GetRoomSkillParameterRequestRequestTypeDef",
    "RoomSkillParameterTypeDef",
    "GetSkillGroupRequestRequestTypeDef",
    "SkillGroupTypeDef",
    "InstantBookingTypeDef",
    "PaginatorConfigTypeDef",
    "ListBusinessReportSchedulesRequestRequestTypeDef",
    "ListConferenceProvidersRequestRequestTypeDef",
    "ListDeviceEventsRequestRequestTypeDef",
    "ListGatewayGroupsRequestRequestTypeDef",
    "ListGatewaysRequestRequestTypeDef",
    "ListSkillsRequestRequestTypeDef",
    "SkillSummaryTypeDef",
    "ListSkillsStoreCategoriesRequestRequestTypeDef",
    "ListSkillsStoreSkillsByCategoryRequestRequestTypeDef",
    "ListSmartHomeAppliancesRequestRequestTypeDef",
    "SmartHomeApplianceTypeDef",
    "ListTagsRequestRequestTypeDef",
    "ProactiveJoinTypeDef",
    "RequireCheckInTypeDef",
    "NetworkProfileDataTypeDef",
    "ProfileDataTypeDef",
    "PutInvitationConfigurationRequestRequestTypeDef",
    "PutSkillAuthorizationRequestRequestTypeDef",
    "RejectSkillRequestRequestTypeDef",
    "ResolveRoomRequestRequestTypeDef",
    "RevokeInvitationRequestRequestTypeDef",
    "RoomDataTypeDef",
    "SortTypeDef",
    "SkillGroupDataTypeDef",
    "UserDataTypeDef",
    "SendInvitationRequestRequestTypeDef",
    "StartDeviceSyncRequestRequestTypeDef",
    "StartSmartHomeApplianceDiscoveryRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAddressBookRequestRequestTypeDef",
    "UpdateDeviceRequestRequestTypeDef",
    "UpdateEndOfMeetingReminderTypeDef",
    "UpdateGatewayGroupRequestRequestTypeDef",
    "UpdateGatewayRequestRequestTypeDef",
    "UpdateInstantBookingTypeDef",
    "UpdateProactiveJoinTypeDef",
    "UpdateRequireCheckInTypeDef",
    "UpdateNetworkProfileRequestRequestTypeDef",
    "UpdateRoomRequestRequestTypeDef",
    "UpdateSkillGroupRequestRequestTypeDef",
    "UpdateBusinessReportScheduleRequestRequestTypeDef",
    "BusinessReportTypeDef",
    "PutConferencePreferenceRequestRequestTypeDef",
    "ConferenceProviderTypeDef",
    "UpdateConferenceProviderRequestRequestTypeDef",
    "ContactDataTypeDef",
    "ContactTypeDef",
    "UpdateContactRequestRequestTypeDef",
    "ContentTypeDef",
    "CreateAddressBookRequestRequestTypeDef",
    "CreateBusinessReportScheduleRequestRequestTypeDef",
    "CreateConferenceProviderRequestRequestTypeDef",
    "CreateContactRequestRequestTypeDef",
    "CreateGatewayGroupRequestRequestTypeDef",
    "CreateNetworkProfileRequestRequestTypeDef",
    "CreateRoomRequestRequestTypeDef",
    "CreateSkillGroupRequestRequestTypeDef",
    "CreateUserRequestRequestTypeDef",
    "RegisterAVSDeviceRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateAddressBookResponseTypeDef",
    "CreateBusinessReportScheduleResponseTypeDef",
    "CreateConferenceProviderResponseTypeDef",
    "CreateContactResponseTypeDef",
    "CreateGatewayGroupResponseTypeDef",
    "CreateNetworkProfileResponseTypeDef",
    "CreateProfileResponseTypeDef",
    "CreateRoomResponseTypeDef",
    "CreateSkillGroupResponseTypeDef",
    "CreateUserResponseTypeDef",
    "GetAddressBookResponseTypeDef",
    "GetConferencePreferenceResponseTypeDef",
    "GetInvitationConfigurationResponseTypeDef",
    "ListSkillsStoreCategoriesResponseTypeDef",
    "ListTagsResponseTypeDef",
    "RegisterAVSDeviceResponseTypeDef",
    "SearchAddressBooksResponseTypeDef",
    "SendAnnouncementResponseTypeDef",
    "CreateMeetingRoomConfigurationTypeDef",
    "SkillDetailsTypeDef",
    "ListDeviceEventsResponseTypeDef",
    "DeviceStatusInfoTypeDef",
    "ListGatewayGroupsResponseTypeDef",
    "GetGatewayGroupResponseTypeDef",
    "ListGatewaysResponseTypeDef",
    "GetGatewayResponseTypeDef",
    "GetNetworkProfileResponseTypeDef",
    "GetRoomResponseTypeDef",
    "GetRoomSkillParameterResponseTypeDef",
    "PutRoomSkillParameterRequestRequestTypeDef",
    "ResolveRoomResponseTypeDef",
    "GetSkillGroupResponseTypeDef",
    "ListBusinessReportSchedulesRequestListBusinessReportSchedulesPaginateTypeDef",
    "ListConferenceProvidersRequestListConferenceProvidersPaginateTypeDef",
    "ListDeviceEventsRequestListDeviceEventsPaginateTypeDef",
    "ListSkillsRequestListSkillsPaginateTypeDef",
    "ListSkillsStoreCategoriesRequestListSkillsStoreCategoriesPaginateTypeDef",
    "ListSkillsStoreSkillsByCategoryRequestListSkillsStoreSkillsByCategoryPaginateTypeDef",
    "ListSmartHomeAppliancesRequestListSmartHomeAppliancesPaginateTypeDef",
    "ListTagsRequestListTagsPaginateTypeDef",
    "ListSkillsResponseTypeDef",
    "ListSmartHomeAppliancesResponseTypeDef",
    "MeetingRoomConfigurationTypeDef",
    "SearchNetworkProfilesResponseTypeDef",
    "SearchProfilesResponseTypeDef",
    "SearchRoomsResponseTypeDef",
    "SearchAddressBooksRequestRequestTypeDef",
    "SearchContactsRequestRequestTypeDef",
    "SearchDevicesRequestRequestTypeDef",
    "SearchDevicesRequestSearchDevicesPaginateTypeDef",
    "SearchNetworkProfilesRequestRequestTypeDef",
    "SearchProfilesRequestRequestTypeDef",
    "SearchProfilesRequestSearchProfilesPaginateTypeDef",
    "SearchRoomsRequestRequestTypeDef",
    "SearchRoomsRequestSearchRoomsPaginateTypeDef",
    "SearchSkillGroupsRequestRequestTypeDef",
    "SearchSkillGroupsRequestSearchSkillGroupsPaginateTypeDef",
    "SearchUsersRequestRequestTypeDef",
    "SearchUsersRequestSearchUsersPaginateTypeDef",
    "SearchSkillGroupsResponseTypeDef",
    "SearchUsersResponseTypeDef",
    "UpdateMeetingRoomConfigurationTypeDef",
    "BusinessReportScheduleTypeDef",
    "GetConferenceProviderResponseTypeDef",
    "ListConferenceProvidersResponseTypeDef",
    "SearchContactsResponseTypeDef",
    "GetContactResponseTypeDef",
    "SendAnnouncementRequestRequestTypeDef",
    "CreateProfileRequestRequestTypeDef",
    "SkillsStoreSkillTypeDef",
    "DeviceDataTypeDef",
    "DeviceTypeDef",
    "ProfileTypeDef",
    "UpdateProfileRequestRequestTypeDef",
    "ListBusinessReportSchedulesResponseTypeDef",
    "ListSkillsStoreSkillsByCategoryResponseTypeDef",
    "SearchDevicesResponseTypeDef",
    "GetDeviceResponseTypeDef",
    "GetProfileResponseTypeDef",
)

AddressBookDataTypeDef = TypedDict(
    "AddressBookDataTypeDef",
    {
        "AddressBookArn": NotRequired[str],
        "Name": NotRequired[str],
        "Description": NotRequired[str],
    },
)
AddressBookTypeDef = TypedDict(
    "AddressBookTypeDef",
    {
        "AddressBookArn": NotRequired[str],
        "Name": NotRequired[str],
        "Description": NotRequired[str],
    },
)
ApproveSkillRequestRequestTypeDef = TypedDict(
    "ApproveSkillRequestRequestTypeDef",
    {
        "SkillId": str,
    },
)
AssociateContactWithAddressBookRequestRequestTypeDef = TypedDict(
    "AssociateContactWithAddressBookRequestRequestTypeDef",
    {
        "ContactArn": str,
        "AddressBookArn": str,
    },
)
AssociateDeviceWithNetworkProfileRequestRequestTypeDef = TypedDict(
    "AssociateDeviceWithNetworkProfileRequestRequestTypeDef",
    {
        "DeviceArn": str,
        "NetworkProfileArn": str,
    },
)
AssociateDeviceWithRoomRequestRequestTypeDef = TypedDict(
    "AssociateDeviceWithRoomRequestRequestTypeDef",
    {
        "DeviceArn": NotRequired[str],
        "RoomArn": NotRequired[str],
    },
)
AssociateSkillGroupWithRoomRequestRequestTypeDef = TypedDict(
    "AssociateSkillGroupWithRoomRequestRequestTypeDef",
    {
        "SkillGroupArn": NotRequired[str],
        "RoomArn": NotRequired[str],
    },
)
AssociateSkillWithSkillGroupRequestRequestTypeDef = TypedDict(
    "AssociateSkillWithSkillGroupRequestRequestTypeDef",
    {
        "SkillId": str,
        "SkillGroupArn": NotRequired[str],
    },
)
AssociateSkillWithUsersRequestRequestTypeDef = TypedDict(
    "AssociateSkillWithUsersRequestRequestTypeDef",
    {
        "SkillId": str,
    },
)
AudioTypeDef = TypedDict(
    "AudioTypeDef",
    {
        "Locale": Literal["en-US"],
        "Location": str,
    },
)
BusinessReportContentRangeTypeDef = TypedDict(
    "BusinessReportContentRangeTypeDef",
    {
        "Interval": BusinessReportIntervalType,
    },
)
BusinessReportRecurrenceTypeDef = TypedDict(
    "BusinessReportRecurrenceTypeDef",
    {
        "StartDate": NotRequired[str],
    },
)
BusinessReportS3LocationTypeDef = TypedDict(
    "BusinessReportS3LocationTypeDef",
    {
        "Path": NotRequired[str],
        "BucketName": NotRequired[str],
    },
)
CategoryTypeDef = TypedDict(
    "CategoryTypeDef",
    {
        "CategoryId": NotRequired[int],
        "CategoryName": NotRequired[str],
    },
)
ConferencePreferenceTypeDef = TypedDict(
    "ConferencePreferenceTypeDef",
    {
        "DefaultConferenceProviderArn": NotRequired[str],
    },
)
IPDialInTypeDef = TypedDict(
    "IPDialInTypeDef",
    {
        "Endpoint": str,
        "CommsProtocol": CommsProtocolType,
    },
)
MeetingSettingTypeDef = TypedDict(
    "MeetingSettingTypeDef",
    {
        "RequirePin": RequirePinType,
    },
)
PSTNDialInTypeDef = TypedDict(
    "PSTNDialInTypeDef",
    {
        "CountryCode": str,
        "PhoneNumber": str,
        "OneClickIdDelay": str,
        "OneClickPinDelay": str,
    },
)
PhoneNumberTypeDef = TypedDict(
    "PhoneNumberTypeDef",
    {
        "Number": str,
        "Type": PhoneNumberTypeType,
    },
)
SipAddressTypeDef = TypedDict(
    "SipAddressTypeDef",
    {
        "Uri": str,
        "Type": Literal["WORK"],
    },
)
SsmlTypeDef = TypedDict(
    "SsmlTypeDef",
    {
        "Locale": Literal["en-US"],
        "Value": str,
    },
)
TextTypeDef = TypedDict(
    "TextTypeDef",
    {
        "Locale": Literal["en-US"],
        "Value": str,
    },
)
TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
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
CreateEndOfMeetingReminderTypeDef = TypedDict(
    "CreateEndOfMeetingReminderTypeDef",
    {
        "ReminderAtMinutes": Sequence[int],
        "ReminderType": EndOfMeetingReminderTypeType,
        "Enabled": bool,
    },
)
CreateInstantBookingTypeDef = TypedDict(
    "CreateInstantBookingTypeDef",
    {
        "DurationInMinutes": int,
        "Enabled": bool,
    },
)
CreateProactiveJoinTypeDef = TypedDict(
    "CreateProactiveJoinTypeDef",
    {
        "EnabledByMotion": bool,
    },
)
CreateRequireCheckInTypeDef = TypedDict(
    "CreateRequireCheckInTypeDef",
    {
        "ReleaseAfterMinutes": int,
        "Enabled": bool,
    },
)
DeleteAddressBookRequestRequestTypeDef = TypedDict(
    "DeleteAddressBookRequestRequestTypeDef",
    {
        "AddressBookArn": str,
    },
)
DeleteBusinessReportScheduleRequestRequestTypeDef = TypedDict(
    "DeleteBusinessReportScheduleRequestRequestTypeDef",
    {
        "ScheduleArn": str,
    },
)
DeleteConferenceProviderRequestRequestTypeDef = TypedDict(
    "DeleteConferenceProviderRequestRequestTypeDef",
    {
        "ConferenceProviderArn": str,
    },
)
DeleteContactRequestRequestTypeDef = TypedDict(
    "DeleteContactRequestRequestTypeDef",
    {
        "ContactArn": str,
    },
)
DeleteDeviceRequestRequestTypeDef = TypedDict(
    "DeleteDeviceRequestRequestTypeDef",
    {
        "DeviceArn": str,
    },
)
DeleteDeviceUsageDataRequestRequestTypeDef = TypedDict(
    "DeleteDeviceUsageDataRequestRequestTypeDef",
    {
        "DeviceArn": str,
        "DeviceUsageType": Literal["VOICE"],
    },
)
DeleteGatewayGroupRequestRequestTypeDef = TypedDict(
    "DeleteGatewayGroupRequestRequestTypeDef",
    {
        "GatewayGroupArn": str,
    },
)
DeleteNetworkProfileRequestRequestTypeDef = TypedDict(
    "DeleteNetworkProfileRequestRequestTypeDef",
    {
        "NetworkProfileArn": str,
    },
)
DeleteProfileRequestRequestTypeDef = TypedDict(
    "DeleteProfileRequestRequestTypeDef",
    {
        "ProfileArn": NotRequired[str],
    },
)
DeleteRoomRequestRequestTypeDef = TypedDict(
    "DeleteRoomRequestRequestTypeDef",
    {
        "RoomArn": NotRequired[str],
    },
)
DeleteRoomSkillParameterRequestRequestTypeDef = TypedDict(
    "DeleteRoomSkillParameterRequestRequestTypeDef",
    {
        "SkillId": str,
        "ParameterKey": str,
        "RoomArn": NotRequired[str],
    },
)
DeleteSkillAuthorizationRequestRequestTypeDef = TypedDict(
    "DeleteSkillAuthorizationRequestRequestTypeDef",
    {
        "SkillId": str,
        "RoomArn": NotRequired[str],
    },
)
DeleteSkillGroupRequestRequestTypeDef = TypedDict(
    "DeleteSkillGroupRequestRequestTypeDef",
    {
        "SkillGroupArn": NotRequired[str],
    },
)
DeleteUserRequestRequestTypeDef = TypedDict(
    "DeleteUserRequestRequestTypeDef",
    {
        "EnrollmentId": str,
        "UserArn": NotRequired[str],
    },
)
DeveloperInfoTypeDef = TypedDict(
    "DeveloperInfoTypeDef",
    {
        "DeveloperName": NotRequired[str],
        "PrivacyPolicy": NotRequired[str],
        "Email": NotRequired[str],
        "Url": NotRequired[str],
    },
)
DeviceEventTypeDef = TypedDict(
    "DeviceEventTypeDef",
    {
        "Type": NotRequired[DeviceEventTypeType],
        "Value": NotRequired[str],
        "Timestamp": NotRequired[datetime],
    },
)
DeviceNetworkProfileInfoTypeDef = TypedDict(
    "DeviceNetworkProfileInfoTypeDef",
    {
        "NetworkProfileArn": NotRequired[str],
        "CertificateArn": NotRequired[str],
        "CertificateExpirationTime": NotRequired[datetime],
    },
)
DeviceStatusDetailTypeDef = TypedDict(
    "DeviceStatusDetailTypeDef",
    {
        "Feature": NotRequired[FeatureType],
        "Code": NotRequired[DeviceStatusDetailCodeType],
    },
)
DisassociateContactFromAddressBookRequestRequestTypeDef = TypedDict(
    "DisassociateContactFromAddressBookRequestRequestTypeDef",
    {
        "ContactArn": str,
        "AddressBookArn": str,
    },
)
DisassociateDeviceFromRoomRequestRequestTypeDef = TypedDict(
    "DisassociateDeviceFromRoomRequestRequestTypeDef",
    {
        "DeviceArn": NotRequired[str],
    },
)
DisassociateSkillFromSkillGroupRequestRequestTypeDef = TypedDict(
    "DisassociateSkillFromSkillGroupRequestRequestTypeDef",
    {
        "SkillId": str,
        "SkillGroupArn": NotRequired[str],
    },
)
DisassociateSkillFromUsersRequestRequestTypeDef = TypedDict(
    "DisassociateSkillFromUsersRequestRequestTypeDef",
    {
        "SkillId": str,
    },
)
DisassociateSkillGroupFromRoomRequestRequestTypeDef = TypedDict(
    "DisassociateSkillGroupFromRoomRequestRequestTypeDef",
    {
        "SkillGroupArn": NotRequired[str],
        "RoomArn": NotRequired[str],
    },
)
EndOfMeetingReminderTypeDef = TypedDict(
    "EndOfMeetingReminderTypeDef",
    {
        "ReminderAtMinutes": NotRequired[List[int]],
        "ReminderType": NotRequired[EndOfMeetingReminderTypeType],
        "Enabled": NotRequired[bool],
    },
)
FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Key": str,
        "Values": Sequence[str],
    },
)
ForgetSmartHomeAppliancesRequestRequestTypeDef = TypedDict(
    "ForgetSmartHomeAppliancesRequestRequestTypeDef",
    {
        "RoomArn": str,
    },
)
GatewayGroupSummaryTypeDef = TypedDict(
    "GatewayGroupSummaryTypeDef",
    {
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "Description": NotRequired[str],
    },
)
GatewayGroupTypeDef = TypedDict(
    "GatewayGroupTypeDef",
    {
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "Description": NotRequired[str],
    },
)
GatewaySummaryTypeDef = TypedDict(
    "GatewaySummaryTypeDef",
    {
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "GatewayGroupArn": NotRequired[str],
        "SoftwareVersion": NotRequired[str],
    },
)
GatewayTypeDef = TypedDict(
    "GatewayTypeDef",
    {
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "GatewayGroupArn": NotRequired[str],
        "SoftwareVersion": NotRequired[str],
    },
)
GetAddressBookRequestRequestTypeDef = TypedDict(
    "GetAddressBookRequestRequestTypeDef",
    {
        "AddressBookArn": str,
    },
)
GetConferenceProviderRequestRequestTypeDef = TypedDict(
    "GetConferenceProviderRequestRequestTypeDef",
    {
        "ConferenceProviderArn": str,
    },
)
GetContactRequestRequestTypeDef = TypedDict(
    "GetContactRequestRequestTypeDef",
    {
        "ContactArn": str,
    },
)
GetDeviceRequestRequestTypeDef = TypedDict(
    "GetDeviceRequestRequestTypeDef",
    {
        "DeviceArn": NotRequired[str],
    },
)
GetGatewayGroupRequestRequestTypeDef = TypedDict(
    "GetGatewayGroupRequestRequestTypeDef",
    {
        "GatewayGroupArn": str,
    },
)
GetGatewayRequestRequestTypeDef = TypedDict(
    "GetGatewayRequestRequestTypeDef",
    {
        "GatewayArn": str,
    },
)
GetNetworkProfileRequestRequestTypeDef = TypedDict(
    "GetNetworkProfileRequestRequestTypeDef",
    {
        "NetworkProfileArn": str,
    },
)
NetworkProfileTypeDef = TypedDict(
    "NetworkProfileTypeDef",
    {
        "NetworkProfileArn": NotRequired[str],
        "NetworkProfileName": NotRequired[str],
        "Description": NotRequired[str],
        "Ssid": NotRequired[str],
        "SecurityType": NotRequired[NetworkSecurityTypeType],
        "EapMethod": NotRequired[Literal["EAP_TLS"]],
        "CurrentPassword": NotRequired[str],
        "NextPassword": NotRequired[str],
        "CertificateAuthorityArn": NotRequired[str],
        "TrustAnchors": NotRequired[List[str]],
    },
)
GetProfileRequestRequestTypeDef = TypedDict(
    "GetProfileRequestRequestTypeDef",
    {
        "ProfileArn": NotRequired[str],
    },
)
GetRoomRequestRequestTypeDef = TypedDict(
    "GetRoomRequestRequestTypeDef",
    {
        "RoomArn": NotRequired[str],
    },
)
RoomTypeDef = TypedDict(
    "RoomTypeDef",
    {
        "RoomArn": NotRequired[str],
        "RoomName": NotRequired[str],
        "Description": NotRequired[str],
        "ProviderCalendarId": NotRequired[str],
        "ProfileArn": NotRequired[str],
    },
)
GetRoomSkillParameterRequestRequestTypeDef = TypedDict(
    "GetRoomSkillParameterRequestRequestTypeDef",
    {
        "SkillId": str,
        "ParameterKey": str,
        "RoomArn": NotRequired[str],
    },
)
RoomSkillParameterTypeDef = TypedDict(
    "RoomSkillParameterTypeDef",
    {
        "ParameterKey": str,
        "ParameterValue": str,
    },
)
GetSkillGroupRequestRequestTypeDef = TypedDict(
    "GetSkillGroupRequestRequestTypeDef",
    {
        "SkillGroupArn": NotRequired[str],
    },
)
SkillGroupTypeDef = TypedDict(
    "SkillGroupTypeDef",
    {
        "SkillGroupArn": NotRequired[str],
        "SkillGroupName": NotRequired[str],
        "Description": NotRequired[str],
    },
)
InstantBookingTypeDef = TypedDict(
    "InstantBookingTypeDef",
    {
        "DurationInMinutes": NotRequired[int],
        "Enabled": NotRequired[bool],
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
ListBusinessReportSchedulesRequestRequestTypeDef = TypedDict(
    "ListBusinessReportSchedulesRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
ListConferenceProvidersRequestRequestTypeDef = TypedDict(
    "ListConferenceProvidersRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
ListDeviceEventsRequestRequestTypeDef = TypedDict(
    "ListDeviceEventsRequestRequestTypeDef",
    {
        "DeviceArn": str,
        "EventType": NotRequired[DeviceEventTypeType],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
ListGatewayGroupsRequestRequestTypeDef = TypedDict(
    "ListGatewayGroupsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
ListGatewaysRequestRequestTypeDef = TypedDict(
    "ListGatewaysRequestRequestTypeDef",
    {
        "GatewayGroupArn": NotRequired[str],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
ListSkillsRequestRequestTypeDef = TypedDict(
    "ListSkillsRequestRequestTypeDef",
    {
        "SkillGroupArn": NotRequired[str],
        "EnablementType": NotRequired[EnablementTypeFilterType],
        "SkillType": NotRequired[SkillTypeFilterType],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
SkillSummaryTypeDef = TypedDict(
    "SkillSummaryTypeDef",
    {
        "SkillId": NotRequired[str],
        "SkillName": NotRequired[str],
        "SupportsLinking": NotRequired[bool],
        "EnablementType": NotRequired[EnablementTypeType],
        "SkillType": NotRequired[SkillTypeType],
    },
)
ListSkillsStoreCategoriesRequestRequestTypeDef = TypedDict(
    "ListSkillsStoreCategoriesRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
ListSkillsStoreSkillsByCategoryRequestRequestTypeDef = TypedDict(
    "ListSkillsStoreSkillsByCategoryRequestRequestTypeDef",
    {
        "CategoryId": int,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
ListSmartHomeAppliancesRequestRequestTypeDef = TypedDict(
    "ListSmartHomeAppliancesRequestRequestTypeDef",
    {
        "RoomArn": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
SmartHomeApplianceTypeDef = TypedDict(
    "SmartHomeApplianceTypeDef",
    {
        "FriendlyName": NotRequired[str],
        "Description": NotRequired[str],
        "ManufacturerName": NotRequired[str],
    },
)
ListTagsRequestRequestTypeDef = TypedDict(
    "ListTagsRequestRequestTypeDef",
    {
        "Arn": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
ProactiveJoinTypeDef = TypedDict(
    "ProactiveJoinTypeDef",
    {
        "EnabledByMotion": NotRequired[bool],
    },
)
RequireCheckInTypeDef = TypedDict(
    "RequireCheckInTypeDef",
    {
        "ReleaseAfterMinutes": NotRequired[int],
        "Enabled": NotRequired[bool],
    },
)
NetworkProfileDataTypeDef = TypedDict(
    "NetworkProfileDataTypeDef",
    {
        "NetworkProfileArn": NotRequired[str],
        "NetworkProfileName": NotRequired[str],
        "Description": NotRequired[str],
        "Ssid": NotRequired[str],
        "SecurityType": NotRequired[NetworkSecurityTypeType],
        "EapMethod": NotRequired[Literal["EAP_TLS"]],
        "CertificateAuthorityArn": NotRequired[str],
    },
)
ProfileDataTypeDef = TypedDict(
    "ProfileDataTypeDef",
    {
        "ProfileArn": NotRequired[str],
        "ProfileName": NotRequired[str],
        "IsDefault": NotRequired[bool],
        "Address": NotRequired[str],
        "Timezone": NotRequired[str],
        "DistanceUnit": NotRequired[DistanceUnitType],
        "TemperatureUnit": NotRequired[TemperatureUnitType],
        "WakeWord": NotRequired[WakeWordType],
        "Locale": NotRequired[str],
    },
)
PutInvitationConfigurationRequestRequestTypeDef = TypedDict(
    "PutInvitationConfigurationRequestRequestTypeDef",
    {
        "OrganizationName": str,
        "ContactEmail": NotRequired[str],
        "PrivateSkillIds": NotRequired[Sequence[str]],
    },
)
PutSkillAuthorizationRequestRequestTypeDef = TypedDict(
    "PutSkillAuthorizationRequestRequestTypeDef",
    {
        "AuthorizationResult": Mapping[str, str],
        "SkillId": str,
        "RoomArn": NotRequired[str],
    },
)
RejectSkillRequestRequestTypeDef = TypedDict(
    "RejectSkillRequestRequestTypeDef",
    {
        "SkillId": str,
    },
)
ResolveRoomRequestRequestTypeDef = TypedDict(
    "ResolveRoomRequestRequestTypeDef",
    {
        "UserId": str,
        "SkillId": str,
    },
)
RevokeInvitationRequestRequestTypeDef = TypedDict(
    "RevokeInvitationRequestRequestTypeDef",
    {
        "UserArn": NotRequired[str],
        "EnrollmentId": NotRequired[str],
    },
)
RoomDataTypeDef = TypedDict(
    "RoomDataTypeDef",
    {
        "RoomArn": NotRequired[str],
        "RoomName": NotRequired[str],
        "Description": NotRequired[str],
        "ProviderCalendarId": NotRequired[str],
        "ProfileArn": NotRequired[str],
        "ProfileName": NotRequired[str],
    },
)
SortTypeDef = TypedDict(
    "SortTypeDef",
    {
        "Key": str,
        "Value": SortValueType,
    },
)
SkillGroupDataTypeDef = TypedDict(
    "SkillGroupDataTypeDef",
    {
        "SkillGroupArn": NotRequired[str],
        "SkillGroupName": NotRequired[str],
        "Description": NotRequired[str],
    },
)
UserDataTypeDef = TypedDict(
    "UserDataTypeDef",
    {
        "UserArn": NotRequired[str],
        "FirstName": NotRequired[str],
        "LastName": NotRequired[str],
        "Email": NotRequired[str],
        "EnrollmentStatus": NotRequired[EnrollmentStatusType],
        "EnrollmentId": NotRequired[str],
    },
)
SendInvitationRequestRequestTypeDef = TypedDict(
    "SendInvitationRequestRequestTypeDef",
    {
        "UserArn": NotRequired[str],
    },
)
StartDeviceSyncRequestRequestTypeDef = TypedDict(
    "StartDeviceSyncRequestRequestTypeDef",
    {
        "Features": Sequence[FeatureType],
        "RoomArn": NotRequired[str],
        "DeviceArn": NotRequired[str],
    },
)
StartSmartHomeApplianceDiscoveryRequestRequestTypeDef = TypedDict(
    "StartSmartHomeApplianceDiscoveryRequestRequestTypeDef",
    {
        "RoomArn": str,
    },
)
UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "Arn": str,
        "TagKeys": Sequence[str],
    },
)
UpdateAddressBookRequestRequestTypeDef = TypedDict(
    "UpdateAddressBookRequestRequestTypeDef",
    {
        "AddressBookArn": str,
        "Name": NotRequired[str],
        "Description": NotRequired[str],
    },
)
UpdateDeviceRequestRequestTypeDef = TypedDict(
    "UpdateDeviceRequestRequestTypeDef",
    {
        "DeviceArn": NotRequired[str],
        "DeviceName": NotRequired[str],
    },
)
UpdateEndOfMeetingReminderTypeDef = TypedDict(
    "UpdateEndOfMeetingReminderTypeDef",
    {
        "ReminderAtMinutes": NotRequired[Sequence[int]],
        "ReminderType": NotRequired[EndOfMeetingReminderTypeType],
        "Enabled": NotRequired[bool],
    },
)
UpdateGatewayGroupRequestRequestTypeDef = TypedDict(
    "UpdateGatewayGroupRequestRequestTypeDef",
    {
        "GatewayGroupArn": str,
        "Name": NotRequired[str],
        "Description": NotRequired[str],
    },
)
UpdateGatewayRequestRequestTypeDef = TypedDict(
    "UpdateGatewayRequestRequestTypeDef",
    {
        "GatewayArn": str,
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "SoftwareVersion": NotRequired[str],
    },
)
UpdateInstantBookingTypeDef = TypedDict(
    "UpdateInstantBookingTypeDef",
    {
        "DurationInMinutes": NotRequired[int],
        "Enabled": NotRequired[bool],
    },
)
UpdateProactiveJoinTypeDef = TypedDict(
    "UpdateProactiveJoinTypeDef",
    {
        "EnabledByMotion": bool,
    },
)
UpdateRequireCheckInTypeDef = TypedDict(
    "UpdateRequireCheckInTypeDef",
    {
        "ReleaseAfterMinutes": NotRequired[int],
        "Enabled": NotRequired[bool],
    },
)
UpdateNetworkProfileRequestRequestTypeDef = TypedDict(
    "UpdateNetworkProfileRequestRequestTypeDef",
    {
        "NetworkProfileArn": str,
        "NetworkProfileName": NotRequired[str],
        "Description": NotRequired[str],
        "CurrentPassword": NotRequired[str],
        "NextPassword": NotRequired[str],
        "CertificateAuthorityArn": NotRequired[str],
        "TrustAnchors": NotRequired[Sequence[str]],
    },
)
UpdateRoomRequestRequestTypeDef = TypedDict(
    "UpdateRoomRequestRequestTypeDef",
    {
        "RoomArn": NotRequired[str],
        "RoomName": NotRequired[str],
        "Description": NotRequired[str],
        "ProviderCalendarId": NotRequired[str],
        "ProfileArn": NotRequired[str],
    },
)
UpdateSkillGroupRequestRequestTypeDef = TypedDict(
    "UpdateSkillGroupRequestRequestTypeDef",
    {
        "SkillGroupArn": NotRequired[str],
        "SkillGroupName": NotRequired[str],
        "Description": NotRequired[str],
    },
)
UpdateBusinessReportScheduleRequestRequestTypeDef = TypedDict(
    "UpdateBusinessReportScheduleRequestRequestTypeDef",
    {
        "ScheduleArn": str,
        "S3BucketName": NotRequired[str],
        "S3KeyPrefix": NotRequired[str],
        "Format": NotRequired[BusinessReportFormatType],
        "ScheduleName": NotRequired[str],
        "Recurrence": NotRequired[BusinessReportRecurrenceTypeDef],
    },
)
BusinessReportTypeDef = TypedDict(
    "BusinessReportTypeDef",
    {
        "Status": NotRequired[BusinessReportStatusType],
        "FailureCode": NotRequired[BusinessReportFailureCodeType],
        "S3Location": NotRequired[BusinessReportS3LocationTypeDef],
        "DeliveryTime": NotRequired[datetime],
        "DownloadUrl": NotRequired[str],
    },
)
PutConferencePreferenceRequestRequestTypeDef = TypedDict(
    "PutConferencePreferenceRequestRequestTypeDef",
    {
        "ConferencePreference": ConferencePreferenceTypeDef,
    },
)
ConferenceProviderTypeDef = TypedDict(
    "ConferenceProviderTypeDef",
    {
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "Type": NotRequired[ConferenceProviderTypeType],
        "IPDialIn": NotRequired[IPDialInTypeDef],
        "PSTNDialIn": NotRequired[PSTNDialInTypeDef],
        "MeetingSetting": NotRequired[MeetingSettingTypeDef],
    },
)
UpdateConferenceProviderRequestRequestTypeDef = TypedDict(
    "UpdateConferenceProviderRequestRequestTypeDef",
    {
        "ConferenceProviderArn": str,
        "ConferenceProviderType": ConferenceProviderTypeType,
        "MeetingSetting": MeetingSettingTypeDef,
        "IPDialIn": NotRequired[IPDialInTypeDef],
        "PSTNDialIn": NotRequired[PSTNDialInTypeDef],
    },
)
ContactDataTypeDef = TypedDict(
    "ContactDataTypeDef",
    {
        "ContactArn": NotRequired[str],
        "DisplayName": NotRequired[str],
        "FirstName": NotRequired[str],
        "LastName": NotRequired[str],
        "PhoneNumber": NotRequired[str],
        "PhoneNumbers": NotRequired[List[PhoneNumberTypeDef]],
        "SipAddresses": NotRequired[List[SipAddressTypeDef]],
    },
)
ContactTypeDef = TypedDict(
    "ContactTypeDef",
    {
        "ContactArn": NotRequired[str],
        "DisplayName": NotRequired[str],
        "FirstName": NotRequired[str],
        "LastName": NotRequired[str],
        "PhoneNumber": NotRequired[str],
        "PhoneNumbers": NotRequired[List[PhoneNumberTypeDef]],
        "SipAddresses": NotRequired[List[SipAddressTypeDef]],
    },
)
UpdateContactRequestRequestTypeDef = TypedDict(
    "UpdateContactRequestRequestTypeDef",
    {
        "ContactArn": str,
        "DisplayName": NotRequired[str],
        "FirstName": NotRequired[str],
        "LastName": NotRequired[str],
        "PhoneNumber": NotRequired[str],
        "PhoneNumbers": NotRequired[Sequence[PhoneNumberTypeDef]],
        "SipAddresses": NotRequired[Sequence[SipAddressTypeDef]],
    },
)
ContentTypeDef = TypedDict(
    "ContentTypeDef",
    {
        "TextList": NotRequired[Sequence[TextTypeDef]],
        "SsmlList": NotRequired[Sequence[SsmlTypeDef]],
        "AudioList": NotRequired[Sequence[AudioTypeDef]],
    },
)
CreateAddressBookRequestRequestTypeDef = TypedDict(
    "CreateAddressBookRequestRequestTypeDef",
    {
        "Name": str,
        "Description": NotRequired[str],
        "ClientRequestToken": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)
CreateBusinessReportScheduleRequestRequestTypeDef = TypedDict(
    "CreateBusinessReportScheduleRequestRequestTypeDef",
    {
        "Format": BusinessReportFormatType,
        "ContentRange": BusinessReportContentRangeTypeDef,
        "ScheduleName": NotRequired[str],
        "S3BucketName": NotRequired[str],
        "S3KeyPrefix": NotRequired[str],
        "Recurrence": NotRequired[BusinessReportRecurrenceTypeDef],
        "ClientRequestToken": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)
CreateConferenceProviderRequestRequestTypeDef = TypedDict(
    "CreateConferenceProviderRequestRequestTypeDef",
    {
        "ConferenceProviderName": str,
        "ConferenceProviderType": ConferenceProviderTypeType,
        "MeetingSetting": MeetingSettingTypeDef,
        "IPDialIn": NotRequired[IPDialInTypeDef],
        "PSTNDialIn": NotRequired[PSTNDialInTypeDef],
        "ClientRequestToken": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)
CreateContactRequestRequestTypeDef = TypedDict(
    "CreateContactRequestRequestTypeDef",
    {
        "FirstName": str,
        "DisplayName": NotRequired[str],
        "LastName": NotRequired[str],
        "PhoneNumber": NotRequired[str],
        "PhoneNumbers": NotRequired[Sequence[PhoneNumberTypeDef]],
        "SipAddresses": NotRequired[Sequence[SipAddressTypeDef]],
        "ClientRequestToken": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)
CreateGatewayGroupRequestRequestTypeDef = TypedDict(
    "CreateGatewayGroupRequestRequestTypeDef",
    {
        "Name": str,
        "ClientRequestToken": str,
        "Description": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)
CreateNetworkProfileRequestRequestTypeDef = TypedDict(
    "CreateNetworkProfileRequestRequestTypeDef",
    {
        "NetworkProfileName": str,
        "Ssid": str,
        "SecurityType": NetworkSecurityTypeType,
        "ClientRequestToken": str,
        "Description": NotRequired[str],
        "EapMethod": NotRequired[Literal["EAP_TLS"]],
        "CurrentPassword": NotRequired[str],
        "NextPassword": NotRequired[str],
        "CertificateAuthorityArn": NotRequired[str],
        "TrustAnchors": NotRequired[Sequence[str]],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)
CreateRoomRequestRequestTypeDef = TypedDict(
    "CreateRoomRequestRequestTypeDef",
    {
        "RoomName": str,
        "Description": NotRequired[str],
        "ProfileArn": NotRequired[str],
        "ProviderCalendarId": NotRequired[str],
        "ClientRequestToken": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)
CreateSkillGroupRequestRequestTypeDef = TypedDict(
    "CreateSkillGroupRequestRequestTypeDef",
    {
        "SkillGroupName": str,
        "Description": NotRequired[str],
        "ClientRequestToken": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)
CreateUserRequestRequestTypeDef = TypedDict(
    "CreateUserRequestRequestTypeDef",
    {
        "UserId": str,
        "FirstName": NotRequired[str],
        "LastName": NotRequired[str],
        "Email": NotRequired[str],
        "ClientRequestToken": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)
RegisterAVSDeviceRequestRequestTypeDef = TypedDict(
    "RegisterAVSDeviceRequestRequestTypeDef",
    {
        "ClientId": str,
        "UserCode": str,
        "ProductId": str,
        "AmazonId": str,
        "DeviceSerialNumber": NotRequired[str],
        "RoomArn": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)
TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "Arn": str,
        "Tags": Sequence[TagTypeDef],
    },
)
CreateAddressBookResponseTypeDef = TypedDict(
    "CreateAddressBookResponseTypeDef",
    {
        "AddressBookArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateBusinessReportScheduleResponseTypeDef = TypedDict(
    "CreateBusinessReportScheduleResponseTypeDef",
    {
        "ScheduleArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateConferenceProviderResponseTypeDef = TypedDict(
    "CreateConferenceProviderResponseTypeDef",
    {
        "ConferenceProviderArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateContactResponseTypeDef = TypedDict(
    "CreateContactResponseTypeDef",
    {
        "ContactArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateGatewayGroupResponseTypeDef = TypedDict(
    "CreateGatewayGroupResponseTypeDef",
    {
        "GatewayGroupArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateNetworkProfileResponseTypeDef = TypedDict(
    "CreateNetworkProfileResponseTypeDef",
    {
        "NetworkProfileArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateProfileResponseTypeDef = TypedDict(
    "CreateProfileResponseTypeDef",
    {
        "ProfileArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateRoomResponseTypeDef = TypedDict(
    "CreateRoomResponseTypeDef",
    {
        "RoomArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateSkillGroupResponseTypeDef = TypedDict(
    "CreateSkillGroupResponseTypeDef",
    {
        "SkillGroupArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateUserResponseTypeDef = TypedDict(
    "CreateUserResponseTypeDef",
    {
        "UserArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetAddressBookResponseTypeDef = TypedDict(
    "GetAddressBookResponseTypeDef",
    {
        "AddressBook": AddressBookTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetConferencePreferenceResponseTypeDef = TypedDict(
    "GetConferencePreferenceResponseTypeDef",
    {
        "Preference": ConferencePreferenceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetInvitationConfigurationResponseTypeDef = TypedDict(
    "GetInvitationConfigurationResponseTypeDef",
    {
        "OrganizationName": str,
        "ContactEmail": str,
        "PrivateSkillIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListSkillsStoreCategoriesResponseTypeDef = TypedDict(
    "ListSkillsStoreCategoriesResponseTypeDef",
    {
        "CategoryList": List[CategoryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ListTagsResponseTypeDef = TypedDict(
    "ListTagsResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
RegisterAVSDeviceResponseTypeDef = TypedDict(
    "RegisterAVSDeviceResponseTypeDef",
    {
        "DeviceArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
SearchAddressBooksResponseTypeDef = TypedDict(
    "SearchAddressBooksResponseTypeDef",
    {
        "AddressBooks": List[AddressBookDataTypeDef],
        "TotalCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
SendAnnouncementResponseTypeDef = TypedDict(
    "SendAnnouncementResponseTypeDef",
    {
        "AnnouncementArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateMeetingRoomConfigurationTypeDef = TypedDict(
    "CreateMeetingRoomConfigurationTypeDef",
    {
        "RoomUtilizationMetricsEnabled": NotRequired[bool],
        "EndOfMeetingReminder": NotRequired[CreateEndOfMeetingReminderTypeDef],
        "InstantBooking": NotRequired[CreateInstantBookingTypeDef],
        "RequireCheckIn": NotRequired[CreateRequireCheckInTypeDef],
        "ProactiveJoin": NotRequired[CreateProactiveJoinTypeDef],
    },
)
SkillDetailsTypeDef = TypedDict(
    "SkillDetailsTypeDef",
    {
        "ProductDescription": NotRequired[str],
        "InvocationPhrase": NotRequired[str],
        "ReleaseDate": NotRequired[str],
        "EndUserLicenseAgreement": NotRequired[str],
        "GenericKeywords": NotRequired[List[str]],
        "BulletPoints": NotRequired[List[str]],
        "NewInThisVersionBulletPoints": NotRequired[List[str]],
        "SkillTypes": NotRequired[List[str]],
        "Reviews": NotRequired[Dict[str, str]],
        "DeveloperInfo": NotRequired[DeveloperInfoTypeDef],
    },
)
ListDeviceEventsResponseTypeDef = TypedDict(
    "ListDeviceEventsResponseTypeDef",
    {
        "DeviceEvents": List[DeviceEventTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
DeviceStatusInfoTypeDef = TypedDict(
    "DeviceStatusInfoTypeDef",
    {
        "DeviceStatusDetails": NotRequired[List[DeviceStatusDetailTypeDef]],
        "ConnectionStatus": NotRequired[ConnectionStatusType],
        "ConnectionStatusUpdatedTime": NotRequired[datetime],
    },
)
ListGatewayGroupsResponseTypeDef = TypedDict(
    "ListGatewayGroupsResponseTypeDef",
    {
        "GatewayGroups": List[GatewayGroupSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
GetGatewayGroupResponseTypeDef = TypedDict(
    "GetGatewayGroupResponseTypeDef",
    {
        "GatewayGroup": GatewayGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListGatewaysResponseTypeDef = TypedDict(
    "ListGatewaysResponseTypeDef",
    {
        "Gateways": List[GatewaySummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
GetGatewayResponseTypeDef = TypedDict(
    "GetGatewayResponseTypeDef",
    {
        "Gateway": GatewayTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetNetworkProfileResponseTypeDef = TypedDict(
    "GetNetworkProfileResponseTypeDef",
    {
        "NetworkProfile": NetworkProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetRoomResponseTypeDef = TypedDict(
    "GetRoomResponseTypeDef",
    {
        "Room": RoomTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetRoomSkillParameterResponseTypeDef = TypedDict(
    "GetRoomSkillParameterResponseTypeDef",
    {
        "RoomSkillParameter": RoomSkillParameterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PutRoomSkillParameterRequestRequestTypeDef = TypedDict(
    "PutRoomSkillParameterRequestRequestTypeDef",
    {
        "SkillId": str,
        "RoomSkillParameter": RoomSkillParameterTypeDef,
        "RoomArn": NotRequired[str],
    },
)
ResolveRoomResponseTypeDef = TypedDict(
    "ResolveRoomResponseTypeDef",
    {
        "RoomArn": str,
        "RoomName": str,
        "RoomSkillParameters": List[RoomSkillParameterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSkillGroupResponseTypeDef = TypedDict(
    "GetSkillGroupResponseTypeDef",
    {
        "SkillGroup": SkillGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListBusinessReportSchedulesRequestListBusinessReportSchedulesPaginateTypeDef = TypedDict(
    "ListBusinessReportSchedulesRequestListBusinessReportSchedulesPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListConferenceProvidersRequestListConferenceProvidersPaginateTypeDef = TypedDict(
    "ListConferenceProvidersRequestListConferenceProvidersPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListDeviceEventsRequestListDeviceEventsPaginateTypeDef = TypedDict(
    "ListDeviceEventsRequestListDeviceEventsPaginateTypeDef",
    {
        "DeviceArn": str,
        "EventType": NotRequired[DeviceEventTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListSkillsRequestListSkillsPaginateTypeDef = TypedDict(
    "ListSkillsRequestListSkillsPaginateTypeDef",
    {
        "SkillGroupArn": NotRequired[str],
        "EnablementType": NotRequired[EnablementTypeFilterType],
        "SkillType": NotRequired[SkillTypeFilterType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListSkillsStoreCategoriesRequestListSkillsStoreCategoriesPaginateTypeDef = TypedDict(
    "ListSkillsStoreCategoriesRequestListSkillsStoreCategoriesPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListSkillsStoreSkillsByCategoryRequestListSkillsStoreSkillsByCategoryPaginateTypeDef = TypedDict(
    "ListSkillsStoreSkillsByCategoryRequestListSkillsStoreSkillsByCategoryPaginateTypeDef",
    {
        "CategoryId": int,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListSmartHomeAppliancesRequestListSmartHomeAppliancesPaginateTypeDef = TypedDict(
    "ListSmartHomeAppliancesRequestListSmartHomeAppliancesPaginateTypeDef",
    {
        "RoomArn": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListTagsRequestListTagsPaginateTypeDef = TypedDict(
    "ListTagsRequestListTagsPaginateTypeDef",
    {
        "Arn": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListSkillsResponseTypeDef = TypedDict(
    "ListSkillsResponseTypeDef",
    {
        "SkillSummaries": List[SkillSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ListSmartHomeAppliancesResponseTypeDef = TypedDict(
    "ListSmartHomeAppliancesResponseTypeDef",
    {
        "SmartHomeAppliances": List[SmartHomeApplianceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
MeetingRoomConfigurationTypeDef = TypedDict(
    "MeetingRoomConfigurationTypeDef",
    {
        "RoomUtilizationMetricsEnabled": NotRequired[bool],
        "EndOfMeetingReminder": NotRequired[EndOfMeetingReminderTypeDef],
        "InstantBooking": NotRequired[InstantBookingTypeDef],
        "RequireCheckIn": NotRequired[RequireCheckInTypeDef],
        "ProactiveJoin": NotRequired[ProactiveJoinTypeDef],
    },
)
SearchNetworkProfilesResponseTypeDef = TypedDict(
    "SearchNetworkProfilesResponseTypeDef",
    {
        "NetworkProfiles": List[NetworkProfileDataTypeDef],
        "TotalCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
SearchProfilesResponseTypeDef = TypedDict(
    "SearchProfilesResponseTypeDef",
    {
        "Profiles": List[ProfileDataTypeDef],
        "TotalCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
SearchRoomsResponseTypeDef = TypedDict(
    "SearchRoomsResponseTypeDef",
    {
        "Rooms": List[RoomDataTypeDef],
        "TotalCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
SearchAddressBooksRequestRequestTypeDef = TypedDict(
    "SearchAddressBooksRequestRequestTypeDef",
    {
        "Filters": NotRequired[Sequence[FilterTypeDef]],
        "SortCriteria": NotRequired[Sequence[SortTypeDef]],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
SearchContactsRequestRequestTypeDef = TypedDict(
    "SearchContactsRequestRequestTypeDef",
    {
        "Filters": NotRequired[Sequence[FilterTypeDef]],
        "SortCriteria": NotRequired[Sequence[SortTypeDef]],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)
SearchDevicesRequestRequestTypeDef = TypedDict(
    "SearchDevicesRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "Filters": NotRequired[Sequence[FilterTypeDef]],
        "SortCriteria": NotRequired[Sequence[SortTypeDef]],
    },
)
SearchDevicesRequestSearchDevicesPaginateTypeDef = TypedDict(
    "SearchDevicesRequestSearchDevicesPaginateTypeDef",
    {
        "Filters": NotRequired[Sequence[FilterTypeDef]],
        "SortCriteria": NotRequired[Sequence[SortTypeDef]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
SearchNetworkProfilesRequestRequestTypeDef = TypedDict(
    "SearchNetworkProfilesRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "Filters": NotRequired[Sequence[FilterTypeDef]],
        "SortCriteria": NotRequired[Sequence[SortTypeDef]],
    },
)
SearchProfilesRequestRequestTypeDef = TypedDict(
    "SearchProfilesRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "Filters": NotRequired[Sequence[FilterTypeDef]],
        "SortCriteria": NotRequired[Sequence[SortTypeDef]],
    },
)
SearchProfilesRequestSearchProfilesPaginateTypeDef = TypedDict(
    "SearchProfilesRequestSearchProfilesPaginateTypeDef",
    {
        "Filters": NotRequired[Sequence[FilterTypeDef]],
        "SortCriteria": NotRequired[Sequence[SortTypeDef]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
SearchRoomsRequestRequestTypeDef = TypedDict(
    "SearchRoomsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "Filters": NotRequired[Sequence[FilterTypeDef]],
        "SortCriteria": NotRequired[Sequence[SortTypeDef]],
    },
)
SearchRoomsRequestSearchRoomsPaginateTypeDef = TypedDict(
    "SearchRoomsRequestSearchRoomsPaginateTypeDef",
    {
        "Filters": NotRequired[Sequence[FilterTypeDef]],
        "SortCriteria": NotRequired[Sequence[SortTypeDef]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
SearchSkillGroupsRequestRequestTypeDef = TypedDict(
    "SearchSkillGroupsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "Filters": NotRequired[Sequence[FilterTypeDef]],
        "SortCriteria": NotRequired[Sequence[SortTypeDef]],
    },
)
SearchSkillGroupsRequestSearchSkillGroupsPaginateTypeDef = TypedDict(
    "SearchSkillGroupsRequestSearchSkillGroupsPaginateTypeDef",
    {
        "Filters": NotRequired[Sequence[FilterTypeDef]],
        "SortCriteria": NotRequired[Sequence[SortTypeDef]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
SearchUsersRequestRequestTypeDef = TypedDict(
    "SearchUsersRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "Filters": NotRequired[Sequence[FilterTypeDef]],
        "SortCriteria": NotRequired[Sequence[SortTypeDef]],
    },
)
SearchUsersRequestSearchUsersPaginateTypeDef = TypedDict(
    "SearchUsersRequestSearchUsersPaginateTypeDef",
    {
        "Filters": NotRequired[Sequence[FilterTypeDef]],
        "SortCriteria": NotRequired[Sequence[SortTypeDef]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
SearchSkillGroupsResponseTypeDef = TypedDict(
    "SearchSkillGroupsResponseTypeDef",
    {
        "SkillGroups": List[SkillGroupDataTypeDef],
        "TotalCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
SearchUsersResponseTypeDef = TypedDict(
    "SearchUsersResponseTypeDef",
    {
        "Users": List[UserDataTypeDef],
        "TotalCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
UpdateMeetingRoomConfigurationTypeDef = TypedDict(
    "UpdateMeetingRoomConfigurationTypeDef",
    {
        "RoomUtilizationMetricsEnabled": NotRequired[bool],
        "EndOfMeetingReminder": NotRequired[UpdateEndOfMeetingReminderTypeDef],
        "InstantBooking": NotRequired[UpdateInstantBookingTypeDef],
        "RequireCheckIn": NotRequired[UpdateRequireCheckInTypeDef],
        "ProactiveJoin": NotRequired[UpdateProactiveJoinTypeDef],
    },
)
BusinessReportScheduleTypeDef = TypedDict(
    "BusinessReportScheduleTypeDef",
    {
        "ScheduleArn": NotRequired[str],
        "ScheduleName": NotRequired[str],
        "S3BucketName": NotRequired[str],
        "S3KeyPrefix": NotRequired[str],
        "Format": NotRequired[BusinessReportFormatType],
        "ContentRange": NotRequired[BusinessReportContentRangeTypeDef],
        "Recurrence": NotRequired[BusinessReportRecurrenceTypeDef],
        "LastBusinessReport": NotRequired[BusinessReportTypeDef],
    },
)
GetConferenceProviderResponseTypeDef = TypedDict(
    "GetConferenceProviderResponseTypeDef",
    {
        "ConferenceProvider": ConferenceProviderTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListConferenceProvidersResponseTypeDef = TypedDict(
    "ListConferenceProvidersResponseTypeDef",
    {
        "ConferenceProviders": List[ConferenceProviderTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
SearchContactsResponseTypeDef = TypedDict(
    "SearchContactsResponseTypeDef",
    {
        "Contacts": List[ContactDataTypeDef],
        "TotalCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
GetContactResponseTypeDef = TypedDict(
    "GetContactResponseTypeDef",
    {
        "Contact": ContactTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
SendAnnouncementRequestRequestTypeDef = TypedDict(
    "SendAnnouncementRequestRequestTypeDef",
    {
        "RoomFilters": Sequence[FilterTypeDef],
        "Content": ContentTypeDef,
        "ClientRequestToken": str,
        "TimeToLiveInSeconds": NotRequired[int],
    },
)
CreateProfileRequestRequestTypeDef = TypedDict(
    "CreateProfileRequestRequestTypeDef",
    {
        "ProfileName": str,
        "Timezone": str,
        "Address": str,
        "DistanceUnit": DistanceUnitType,
        "TemperatureUnit": TemperatureUnitType,
        "WakeWord": WakeWordType,
        "Locale": NotRequired[str],
        "ClientRequestToken": NotRequired[str],
        "SetupModeDisabled": NotRequired[bool],
        "MaxVolumeLimit": NotRequired[int],
        "PSTNEnabled": NotRequired[bool],
        "DataRetentionOptIn": NotRequired[bool],
        "MeetingRoomConfiguration": NotRequired[CreateMeetingRoomConfigurationTypeDef],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)
SkillsStoreSkillTypeDef = TypedDict(
    "SkillsStoreSkillTypeDef",
    {
        "SkillId": NotRequired[str],
        "SkillName": NotRequired[str],
        "ShortDescription": NotRequired[str],
        "IconUrl": NotRequired[str],
        "SampleUtterances": NotRequired[List[str]],
        "SkillDetails": NotRequired[SkillDetailsTypeDef],
        "SupportsLinking": NotRequired[bool],
    },
)
DeviceDataTypeDef = TypedDict(
    "DeviceDataTypeDef",
    {
        "DeviceArn": NotRequired[str],
        "DeviceSerialNumber": NotRequired[str],
        "DeviceType": NotRequired[str],
        "DeviceName": NotRequired[str],
        "SoftwareVersion": NotRequired[str],
        "MacAddress": NotRequired[str],
        "DeviceStatus": NotRequired[DeviceStatusType],
        "NetworkProfileArn": NotRequired[str],
        "NetworkProfileName": NotRequired[str],
        "RoomArn": NotRequired[str],
        "RoomName": NotRequired[str],
        "DeviceStatusInfo": NotRequired[DeviceStatusInfoTypeDef],
        "CreatedTime": NotRequired[datetime],
    },
)
DeviceTypeDef = TypedDict(
    "DeviceTypeDef",
    {
        "DeviceArn": NotRequired[str],
        "DeviceSerialNumber": NotRequired[str],
        "DeviceType": NotRequired[str],
        "DeviceName": NotRequired[str],
        "SoftwareVersion": NotRequired[str],
        "MacAddress": NotRequired[str],
        "RoomArn": NotRequired[str],
        "DeviceStatus": NotRequired[DeviceStatusType],
        "DeviceStatusInfo": NotRequired[DeviceStatusInfoTypeDef],
        "NetworkProfileInfo": NotRequired[DeviceNetworkProfileInfoTypeDef],
    },
)
ProfileTypeDef = TypedDict(
    "ProfileTypeDef",
    {
        "ProfileArn": NotRequired[str],
        "ProfileName": NotRequired[str],
        "IsDefault": NotRequired[bool],
        "Address": NotRequired[str],
        "Timezone": NotRequired[str],
        "DistanceUnit": NotRequired[DistanceUnitType],
        "TemperatureUnit": NotRequired[TemperatureUnitType],
        "WakeWord": NotRequired[WakeWordType],
        "Locale": NotRequired[str],
        "SetupModeDisabled": NotRequired[bool],
        "MaxVolumeLimit": NotRequired[int],
        "PSTNEnabled": NotRequired[bool],
        "DataRetentionOptIn": NotRequired[bool],
        "AddressBookArn": NotRequired[str],
        "MeetingRoomConfiguration": NotRequired[MeetingRoomConfigurationTypeDef],
    },
)
UpdateProfileRequestRequestTypeDef = TypedDict(
    "UpdateProfileRequestRequestTypeDef",
    {
        "ProfileArn": NotRequired[str],
        "ProfileName": NotRequired[str],
        "IsDefault": NotRequired[bool],
        "Timezone": NotRequired[str],
        "Address": NotRequired[str],
        "DistanceUnit": NotRequired[DistanceUnitType],
        "TemperatureUnit": NotRequired[TemperatureUnitType],
        "WakeWord": NotRequired[WakeWordType],
        "Locale": NotRequired[str],
        "SetupModeDisabled": NotRequired[bool],
        "MaxVolumeLimit": NotRequired[int],
        "PSTNEnabled": NotRequired[bool],
        "DataRetentionOptIn": NotRequired[bool],
        "MeetingRoomConfiguration": NotRequired[UpdateMeetingRoomConfigurationTypeDef],
    },
)
ListBusinessReportSchedulesResponseTypeDef = TypedDict(
    "ListBusinessReportSchedulesResponseTypeDef",
    {
        "BusinessReportSchedules": List[BusinessReportScheduleTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ListSkillsStoreSkillsByCategoryResponseTypeDef = TypedDict(
    "ListSkillsStoreSkillsByCategoryResponseTypeDef",
    {
        "SkillsStoreSkills": List[SkillsStoreSkillTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
SearchDevicesResponseTypeDef = TypedDict(
    "SearchDevicesResponseTypeDef",
    {
        "Devices": List[DeviceDataTypeDef],
        "TotalCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
GetDeviceResponseTypeDef = TypedDict(
    "GetDeviceResponseTypeDef",
    {
        "Device": DeviceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetProfileResponseTypeDef = TypedDict(
    "GetProfileResponseTypeDef",
    {
        "Profile": ProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
