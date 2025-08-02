"""
Type annotations for alexaforbusiness service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_alexaforbusiness.client import AlexaForBusinessClient

    session = get_session()
    async with session.create_client("alexaforbusiness") as client:
        client: AlexaForBusinessClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    BusinessReportFormatType,
    ConferenceProviderTypeType,
    DeviceEventTypeType,
    DistanceUnitType,
    EnablementTypeFilterType,
    FeatureType,
    NetworkSecurityTypeType,
    SkillTypeFilterType,
    TemperatureUnitType,
    WakeWordType,
)
from .paginator import (
    ListBusinessReportSchedulesPaginator,
    ListConferenceProvidersPaginator,
    ListDeviceEventsPaginator,
    ListSkillsPaginator,
    ListSkillsStoreCategoriesPaginator,
    ListSkillsStoreSkillsByCategoryPaginator,
    ListSmartHomeAppliancesPaginator,
    ListTagsPaginator,
    SearchDevicesPaginator,
    SearchProfilesPaginator,
    SearchRoomsPaginator,
    SearchSkillGroupsPaginator,
    SearchUsersPaginator,
)
from .type_defs import (
    BusinessReportContentRangeTypeDef,
    BusinessReportRecurrenceTypeDef,
    ConferencePreferenceTypeDef,
    ContentTypeDef,
    CreateAddressBookResponseTypeDef,
    CreateBusinessReportScheduleResponseTypeDef,
    CreateConferenceProviderResponseTypeDef,
    CreateContactResponseTypeDef,
    CreateGatewayGroupResponseTypeDef,
    CreateMeetingRoomConfigurationTypeDef,
    CreateNetworkProfileResponseTypeDef,
    CreateProfileResponseTypeDef,
    CreateRoomResponseTypeDef,
    CreateSkillGroupResponseTypeDef,
    CreateUserResponseTypeDef,
    FilterTypeDef,
    GetAddressBookResponseTypeDef,
    GetConferencePreferenceResponseTypeDef,
    GetConferenceProviderResponseTypeDef,
    GetContactResponseTypeDef,
    GetDeviceResponseTypeDef,
    GetGatewayGroupResponseTypeDef,
    GetGatewayResponseTypeDef,
    GetInvitationConfigurationResponseTypeDef,
    GetNetworkProfileResponseTypeDef,
    GetProfileResponseTypeDef,
    GetRoomResponseTypeDef,
    GetRoomSkillParameterResponseTypeDef,
    GetSkillGroupResponseTypeDef,
    IPDialInTypeDef,
    ListBusinessReportSchedulesResponseTypeDef,
    ListConferenceProvidersResponseTypeDef,
    ListDeviceEventsResponseTypeDef,
    ListGatewayGroupsResponseTypeDef,
    ListGatewaysResponseTypeDef,
    ListSkillsResponseTypeDef,
    ListSkillsStoreCategoriesResponseTypeDef,
    ListSkillsStoreSkillsByCategoryResponseTypeDef,
    ListSmartHomeAppliancesResponseTypeDef,
    ListTagsResponseTypeDef,
    MeetingSettingTypeDef,
    PhoneNumberTypeDef,
    PSTNDialInTypeDef,
    RegisterAVSDeviceResponseTypeDef,
    ResolveRoomResponseTypeDef,
    RoomSkillParameterTypeDef,
    SearchAddressBooksResponseTypeDef,
    SearchContactsResponseTypeDef,
    SearchDevicesResponseTypeDef,
    SearchNetworkProfilesResponseTypeDef,
    SearchProfilesResponseTypeDef,
    SearchRoomsResponseTypeDef,
    SearchSkillGroupsResponseTypeDef,
    SearchUsersResponseTypeDef,
    SendAnnouncementResponseTypeDef,
    SipAddressTypeDef,
    SortTypeDef,
    TagTypeDef,
    UpdateMeetingRoomConfigurationTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("AlexaForBusinessClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AlreadyExistsException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    DeviceNotRegisteredException: Type[BotocoreClientError]
    InvalidCertificateAuthorityException: Type[BotocoreClientError]
    InvalidDeviceException: Type[BotocoreClientError]
    InvalidSecretsManagerResourceException: Type[BotocoreClientError]
    InvalidServiceLinkedRoleStateException: Type[BotocoreClientError]
    InvalidUserStatusException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NameInUseException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ResourceAssociatedException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    SkillNotLinkedException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]


class AlexaForBusinessClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AlexaForBusinessClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#exceptions)
        """

    async def approve_skill(self, *, SkillId: str) -> Dict[str, Any]:
        """
        Associates a skill with the organization under the customer's AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.approve_skill)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#approve_skill)
        """

    async def associate_contact_with_address_book(
        self, *, ContactArn: str, AddressBookArn: str
    ) -> Dict[str, Any]:
        """
        Associates a contact with a given address book.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.associate_contact_with_address_book)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#associate_contact_with_address_book)
        """

    async def associate_device_with_network_profile(
        self, *, DeviceArn: str, NetworkProfileArn: str
    ) -> Dict[str, Any]:
        """
        Associates a device with the specified network profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.associate_device_with_network_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#associate_device_with_network_profile)
        """

    async def associate_device_with_room(
        self, *, DeviceArn: str = ..., RoomArn: str = ...
    ) -> Dict[str, Any]:
        """
        Associates a device with a given room.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.associate_device_with_room)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#associate_device_with_room)
        """

    async def associate_skill_group_with_room(
        self, *, SkillGroupArn: str = ..., RoomArn: str = ...
    ) -> Dict[str, Any]:
        """
        Associates a skill group with a given room.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.associate_skill_group_with_room)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#associate_skill_group_with_room)
        """

    async def associate_skill_with_skill_group(
        self, *, SkillId: str, SkillGroupArn: str = ...
    ) -> Dict[str, Any]:
        """
        Associates a skill with a skill group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.associate_skill_with_skill_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#associate_skill_with_skill_group)
        """

    async def associate_skill_with_users(self, *, SkillId: str) -> Dict[str, Any]:
        """
        Makes a private skill available for enrolled users to enable on their devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.associate_skill_with_users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#associate_skill_with_users)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#close)
        """

    async def create_address_book(
        self,
        *,
        Name: str,
        Description: str = ...,
        ClientRequestToken: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateAddressBookResponseTypeDef:
        """
        Creates an address book with the specified details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.create_address_book)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#create_address_book)
        """

    async def create_business_report_schedule(
        self,
        *,
        Format: BusinessReportFormatType,
        ContentRange: BusinessReportContentRangeTypeDef,
        ScheduleName: str = ...,
        S3BucketName: str = ...,
        S3KeyPrefix: str = ...,
        Recurrence: BusinessReportRecurrenceTypeDef = ...,
        ClientRequestToken: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateBusinessReportScheduleResponseTypeDef:
        """
        Creates a recurring schedule for usage reports to deliver to the specified S3
        location with a specified daily or weekly
        interval.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.create_business_report_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#create_business_report_schedule)
        """

    async def create_conference_provider(
        self,
        *,
        ConferenceProviderName: str,
        ConferenceProviderType: ConferenceProviderTypeType,
        MeetingSetting: MeetingSettingTypeDef,
        IPDialIn: IPDialInTypeDef = ...,
        PSTNDialIn: PSTNDialInTypeDef = ...,
        ClientRequestToken: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateConferenceProviderResponseTypeDef:
        """
        Adds a new conference provider under the user's AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.create_conference_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#create_conference_provider)
        """

    async def create_contact(
        self,
        *,
        FirstName: str,
        DisplayName: str = ...,
        LastName: str = ...,
        PhoneNumber: str = ...,
        PhoneNumbers: Sequence[PhoneNumberTypeDef] = ...,
        SipAddresses: Sequence[SipAddressTypeDef] = ...,
        ClientRequestToken: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateContactResponseTypeDef:
        """
        Creates a contact with the specified details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.create_contact)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#create_contact)
        """

    async def create_gateway_group(
        self,
        *,
        Name: str,
        ClientRequestToken: str,
        Description: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateGatewayGroupResponseTypeDef:
        """
        Creates a gateway group with the specified details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.create_gateway_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#create_gateway_group)
        """

    async def create_network_profile(
        self,
        *,
        NetworkProfileName: str,
        Ssid: str,
        SecurityType: NetworkSecurityTypeType,
        ClientRequestToken: str,
        Description: str = ...,
        EapMethod: Literal["EAP_TLS"] = ...,
        CurrentPassword: str = ...,
        NextPassword: str = ...,
        CertificateAuthorityArn: str = ...,
        TrustAnchors: Sequence[str] = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateNetworkProfileResponseTypeDef:
        """
        Creates a network profile with the specified details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.create_network_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#create_network_profile)
        """

    async def create_profile(
        self,
        *,
        ProfileName: str,
        Timezone: str,
        Address: str,
        DistanceUnit: DistanceUnitType,
        TemperatureUnit: TemperatureUnitType,
        WakeWord: WakeWordType,
        Locale: str = ...,
        ClientRequestToken: str = ...,
        SetupModeDisabled: bool = ...,
        MaxVolumeLimit: int = ...,
        PSTNEnabled: bool = ...,
        DataRetentionOptIn: bool = ...,
        MeetingRoomConfiguration: CreateMeetingRoomConfigurationTypeDef = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateProfileResponseTypeDef:
        """
        Creates a new room profile with the specified details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.create_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#create_profile)
        """

    async def create_room(
        self,
        *,
        RoomName: str,
        Description: str = ...,
        ProfileArn: str = ...,
        ProviderCalendarId: str = ...,
        ClientRequestToken: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateRoomResponseTypeDef:
        """
        Creates a room with the specified details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.create_room)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#create_room)
        """

    async def create_skill_group(
        self,
        *,
        SkillGroupName: str,
        Description: str = ...,
        ClientRequestToken: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateSkillGroupResponseTypeDef:
        """
        Creates a skill group with a specified name and description.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.create_skill_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#create_skill_group)
        """

    async def create_user(
        self,
        *,
        UserId: str,
        FirstName: str = ...,
        LastName: str = ...,
        Email: str = ...,
        ClientRequestToken: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateUserResponseTypeDef:
        """
        Creates a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.create_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#create_user)
        """

    async def delete_address_book(self, *, AddressBookArn: str) -> Dict[str, Any]:
        """
        Deletes an address book by the address book ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_address_book)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#delete_address_book)
        """

    async def delete_business_report_schedule(self, *, ScheduleArn: str) -> Dict[str, Any]:
        """
        Deletes the recurring report delivery schedule with the specified schedule ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_business_report_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#delete_business_report_schedule)
        """

    async def delete_conference_provider(self, *, ConferenceProviderArn: str) -> Dict[str, Any]:
        """
        Deletes a conference provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_conference_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#delete_conference_provider)
        """

    async def delete_contact(self, *, ContactArn: str) -> Dict[str, Any]:
        """
        Deletes a contact by the contact ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_contact)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#delete_contact)
        """

    async def delete_device(self, *, DeviceArn: str) -> Dict[str, Any]:
        """
        Removes a device from Alexa For Business.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#delete_device)
        """

    async def delete_device_usage_data(
        self, *, DeviceArn: str, DeviceUsageType: Literal["VOICE"]
    ) -> Dict[str, Any]:
        """
        When this action is called for a specified shared device, it allows authorized
        users to delete the device's entire previous history of voice input data and
        associated response
        data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_device_usage_data)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#delete_device_usage_data)
        """

    async def delete_gateway_group(self, *, GatewayGroupArn: str) -> Dict[str, Any]:
        """
        Deletes a gateway group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_gateway_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#delete_gateway_group)
        """

    async def delete_network_profile(self, *, NetworkProfileArn: str) -> Dict[str, Any]:
        """
        Deletes a network profile by the network profile ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_network_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#delete_network_profile)
        """

    async def delete_profile(self, *, ProfileArn: str = ...) -> Dict[str, Any]:
        """
        Deletes a room profile by the profile ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#delete_profile)
        """

    async def delete_room(self, *, RoomArn: str = ...) -> Dict[str, Any]:
        """
        Deletes a room by the room ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_room)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#delete_room)
        """

    async def delete_room_skill_parameter(
        self, *, SkillId: str, ParameterKey: str, RoomArn: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes room skill parameter details by room, skill, and parameter key ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_room_skill_parameter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#delete_room_skill_parameter)
        """

    async def delete_skill_authorization(
        self, *, SkillId: str, RoomArn: str = ...
    ) -> Dict[str, Any]:
        """
        Unlinks a third-party account from a skill.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_skill_authorization)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#delete_skill_authorization)
        """

    async def delete_skill_group(self, *, SkillGroupArn: str = ...) -> Dict[str, Any]:
        """
        Deletes a skill group by skill group ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_skill_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#delete_skill_group)
        """

    async def delete_user(self, *, EnrollmentId: str, UserArn: str = ...) -> Dict[str, Any]:
        """
        Deletes a specified user by user ARN and enrollment ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.delete_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#delete_user)
        """

    async def disassociate_contact_from_address_book(
        self, *, ContactArn: str, AddressBookArn: str
    ) -> Dict[str, Any]:
        """
        Disassociates a contact from a given address book.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.disassociate_contact_from_address_book)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#disassociate_contact_from_address_book)
        """

    async def disassociate_device_from_room(self, *, DeviceArn: str = ...) -> Dict[str, Any]:
        """
        Disassociates a device from its current room.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.disassociate_device_from_room)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#disassociate_device_from_room)
        """

    async def disassociate_skill_from_skill_group(
        self, *, SkillId: str, SkillGroupArn: str = ...
    ) -> Dict[str, Any]:
        """
        Disassociates a skill from a skill group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.disassociate_skill_from_skill_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#disassociate_skill_from_skill_group)
        """

    async def disassociate_skill_from_users(self, *, SkillId: str) -> Dict[str, Any]:
        """
        Makes a private skill unavailable for enrolled users and prevents them from
        enabling it on their
        devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.disassociate_skill_from_users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#disassociate_skill_from_users)
        """

    async def disassociate_skill_group_from_room(
        self, *, SkillGroupArn: str = ..., RoomArn: str = ...
    ) -> Dict[str, Any]:
        """
        Disassociates a skill group from a specified room.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.disassociate_skill_group_from_room)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#disassociate_skill_group_from_room)
        """

    async def forget_smart_home_appliances(self, *, RoomArn: str) -> Dict[str, Any]:
        """
        Forgets smart home appliances associated to a room.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.forget_smart_home_appliances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#forget_smart_home_appliances)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#generate_presigned_url)
        """

    async def get_address_book(self, *, AddressBookArn: str) -> GetAddressBookResponseTypeDef:
        """
        Gets address the book details by the address book ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_address_book)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_address_book)
        """

    async def get_conference_preference(self) -> GetConferencePreferenceResponseTypeDef:
        """
        Retrieves the existing conference preferences.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_conference_preference)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_conference_preference)
        """

    async def get_conference_provider(
        self, *, ConferenceProviderArn: str
    ) -> GetConferenceProviderResponseTypeDef:
        """
        Gets details about a specific conference provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_conference_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_conference_provider)
        """

    async def get_contact(self, *, ContactArn: str) -> GetContactResponseTypeDef:
        """
        Gets the contact details by the contact ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_contact)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_contact)
        """

    async def get_device(self, *, DeviceArn: str = ...) -> GetDeviceResponseTypeDef:
        """
        Gets the details of a device by device ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_device)
        """

    async def get_gateway(self, *, GatewayArn: str) -> GetGatewayResponseTypeDef:
        """
        Retrieves the details of a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_gateway)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_gateway)
        """

    async def get_gateway_group(self, *, GatewayGroupArn: str) -> GetGatewayGroupResponseTypeDef:
        """
        Retrieves the details of a gateway group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_gateway_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_gateway_group)
        """

    async def get_invitation_configuration(self) -> GetInvitationConfigurationResponseTypeDef:
        """
        Retrieves the configured values for the user enrollment invitation email
        template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_invitation_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_invitation_configuration)
        """

    async def get_network_profile(
        self, *, NetworkProfileArn: str
    ) -> GetNetworkProfileResponseTypeDef:
        """
        Gets the network profile details by the network profile ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_network_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_network_profile)
        """

    async def get_profile(self, *, ProfileArn: str = ...) -> GetProfileResponseTypeDef:
        """
        Gets the details of a room profile by profile ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_profile)
        """

    async def get_room(self, *, RoomArn: str = ...) -> GetRoomResponseTypeDef:
        """
        Gets room details by room ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_room)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_room)
        """

    async def get_room_skill_parameter(
        self, *, SkillId: str, ParameterKey: str, RoomArn: str = ...
    ) -> GetRoomSkillParameterResponseTypeDef:
        """
        Gets room skill parameter details by room, skill, and parameter key ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_room_skill_parameter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_room_skill_parameter)
        """

    async def get_skill_group(self, *, SkillGroupArn: str = ...) -> GetSkillGroupResponseTypeDef:
        """
        Gets skill group details by skill group ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_skill_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_skill_group)
        """

    async def list_business_report_schedules(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListBusinessReportSchedulesResponseTypeDef:
        """
        Lists the details of the schedules that a user configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.list_business_report_schedules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#list_business_report_schedules)
        """

    async def list_conference_providers(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListConferenceProvidersResponseTypeDef:
        """
        Lists conference providers under a specific AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.list_conference_providers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#list_conference_providers)
        """

    async def list_device_events(
        self,
        *,
        DeviceArn: str,
        EventType: DeviceEventTypeType = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListDeviceEventsResponseTypeDef:
        """
        Lists the device event history, including device connection status, for up to
        30
        days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.list_device_events)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#list_device_events)
        """

    async def list_gateway_groups(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListGatewayGroupsResponseTypeDef:
        """
        Retrieves a list of gateway group summaries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.list_gateway_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#list_gateway_groups)
        """

    async def list_gateways(
        self, *, GatewayGroupArn: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> ListGatewaysResponseTypeDef:
        """
        Retrieves a list of gateway summaries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.list_gateways)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#list_gateways)
        """

    async def list_skills(
        self,
        *,
        SkillGroupArn: str = ...,
        EnablementType: EnablementTypeFilterType = ...,
        SkillType: SkillTypeFilterType = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListSkillsResponseTypeDef:
        """
        Lists all enabled skills in a specific skill group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.list_skills)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#list_skills)
        """

    async def list_skills_store_categories(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListSkillsStoreCategoriesResponseTypeDef:
        """
        Lists all categories in the Alexa skill store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.list_skills_store_categories)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#list_skills_store_categories)
        """

    async def list_skills_store_skills_by_category(
        self, *, CategoryId: int, NextToken: str = ..., MaxResults: int = ...
    ) -> ListSkillsStoreSkillsByCategoryResponseTypeDef:
        """
        Lists all skills in the Alexa skill store by category.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.list_skills_store_skills_by_category)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#list_skills_store_skills_by_category)
        """

    async def list_smart_home_appliances(
        self, *, RoomArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListSmartHomeAppliancesResponseTypeDef:
        """
        Lists all of the smart home appliances associated with a room.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.list_smart_home_appliances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#list_smart_home_appliances)
        """

    async def list_tags(
        self, *, Arn: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListTagsResponseTypeDef:
        """
        Lists all tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.list_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#list_tags)
        """

    async def put_conference_preference(
        self, *, ConferencePreference: ConferencePreferenceTypeDef
    ) -> Dict[str, Any]:
        """
        Sets the conference preferences on a specific conference provider at the
        account
        level.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.put_conference_preference)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#put_conference_preference)
        """

    async def put_invitation_configuration(
        self,
        *,
        OrganizationName: str,
        ContactEmail: str = ...,
        PrivateSkillIds: Sequence[str] = ...,
    ) -> Dict[str, Any]:
        """
        Configures the email template for the user enrollment invitation with the
        specified
        attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.put_invitation_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#put_invitation_configuration)
        """

    async def put_room_skill_parameter(
        self, *, SkillId: str, RoomSkillParameter: RoomSkillParameterTypeDef, RoomArn: str = ...
    ) -> Dict[str, Any]:
        """
        Updates room skill parameter details by room, skill, and parameter key ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.put_room_skill_parameter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#put_room_skill_parameter)
        """

    async def put_skill_authorization(
        self, *, AuthorizationResult: Mapping[str, str], SkillId: str, RoomArn: str = ...
    ) -> Dict[str, Any]:
        """
        Links a user's account to a third-party skill provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.put_skill_authorization)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#put_skill_authorization)
        """

    async def register_avs_device(
        self,
        *,
        ClientId: str,
        UserCode: str,
        ProductId: str,
        AmazonId: str,
        DeviceSerialNumber: str = ...,
        RoomArn: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> RegisterAVSDeviceResponseTypeDef:
        """
        Registers an Alexa-enabled device built by an Original Equipment Manufacturer
        (OEM) using Alexa Voice Service
        (AVS).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.register_avs_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#register_avs_device)
        """

    async def reject_skill(self, *, SkillId: str) -> Dict[str, Any]:
        """
        Disassociates a skill from the organization under a user's AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.reject_skill)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#reject_skill)
        """

    async def resolve_room(self, *, UserId: str, SkillId: str) -> ResolveRoomResponseTypeDef:
        """
        Determines the details for the room from which a skill request was invoked.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.resolve_room)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#resolve_room)
        """

    async def revoke_invitation(
        self, *, UserArn: str = ..., EnrollmentId: str = ...
    ) -> Dict[str, Any]:
        """
        Revokes an invitation and invalidates the enrollment URL.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.revoke_invitation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#revoke_invitation)
        """

    async def search_address_books(
        self,
        *,
        Filters: Sequence[FilterTypeDef] = ...,
        SortCriteria: Sequence[SortTypeDef] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> SearchAddressBooksResponseTypeDef:
        """
        Searches address books and lists the ones that meet a set of filter and sort
        criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.search_address_books)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#search_address_books)
        """

    async def search_contacts(
        self,
        *,
        Filters: Sequence[FilterTypeDef] = ...,
        SortCriteria: Sequence[SortTypeDef] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> SearchContactsResponseTypeDef:
        """
        Searches contacts and lists the ones that meet a set of filter and sort
        criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.search_contacts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#search_contacts)
        """

    async def search_devices(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        SortCriteria: Sequence[SortTypeDef] = ...,
    ) -> SearchDevicesResponseTypeDef:
        """
        Searches devices and lists the ones that meet a set of filter criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.search_devices)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#search_devices)
        """

    async def search_network_profiles(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        SortCriteria: Sequence[SortTypeDef] = ...,
    ) -> SearchNetworkProfilesResponseTypeDef:
        """
        Searches network profiles and lists the ones that meet a set of filter and sort
        criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.search_network_profiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#search_network_profiles)
        """

    async def search_profiles(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        SortCriteria: Sequence[SortTypeDef] = ...,
    ) -> SearchProfilesResponseTypeDef:
        """
        Searches room profiles and lists the ones that meet a set of filter criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.search_profiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#search_profiles)
        """

    async def search_rooms(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        SortCriteria: Sequence[SortTypeDef] = ...,
    ) -> SearchRoomsResponseTypeDef:
        """
        Searches rooms and lists the ones that meet a set of filter and sort criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.search_rooms)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#search_rooms)
        """

    async def search_skill_groups(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        SortCriteria: Sequence[SortTypeDef] = ...,
    ) -> SearchSkillGroupsResponseTypeDef:
        """
        Searches skill groups and lists the ones that meet a set of filter and sort
        criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.search_skill_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#search_skill_groups)
        """

    async def search_users(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        SortCriteria: Sequence[SortTypeDef] = ...,
    ) -> SearchUsersResponseTypeDef:
        """
        Searches users and lists the ones that meet a set of filter and sort criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.search_users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#search_users)
        """

    async def send_announcement(
        self,
        *,
        RoomFilters: Sequence[FilterTypeDef],
        Content: ContentTypeDef,
        ClientRequestToken: str,
        TimeToLiveInSeconds: int = ...,
    ) -> SendAnnouncementResponseTypeDef:
        """
        Triggers an asynchronous flow to send text, SSML, or audio announcements to
        rooms that are identified by a search or
        filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.send_announcement)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#send_announcement)
        """

    async def send_invitation(self, *, UserArn: str = ...) -> Dict[str, Any]:
        """
        Sends an enrollment invitation email with a URL to a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.send_invitation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#send_invitation)
        """

    async def start_device_sync(
        self, *, Features: Sequence[FeatureType], RoomArn: str = ..., DeviceArn: str = ...
    ) -> Dict[str, Any]:
        """
        Resets a device and its account to the known default settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.start_device_sync)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#start_device_sync)
        """

    async def start_smart_home_appliance_discovery(self, *, RoomArn: str) -> Dict[str, Any]:
        """
        Initiates the discovery of any smart home appliances associated with the room.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.start_smart_home_appliance_discovery)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#start_smart_home_appliance_discovery)
        """

    async def tag_resource(self, *, Arn: str, Tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Adds metadata tags to a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#tag_resource)
        """

    async def untag_resource(self, *, Arn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes metadata tags from a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#untag_resource)
        """

    async def update_address_book(
        self, *, AddressBookArn: str, Name: str = ..., Description: str = ...
    ) -> Dict[str, Any]:
        """
        Updates address book details by the address book ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.update_address_book)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#update_address_book)
        """

    async def update_business_report_schedule(
        self,
        *,
        ScheduleArn: str,
        S3BucketName: str = ...,
        S3KeyPrefix: str = ...,
        Format: BusinessReportFormatType = ...,
        ScheduleName: str = ...,
        Recurrence: BusinessReportRecurrenceTypeDef = ...,
    ) -> Dict[str, Any]:
        """
        Updates the configuration of the report delivery schedule with the specified
        schedule
        ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.update_business_report_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#update_business_report_schedule)
        """

    async def update_conference_provider(
        self,
        *,
        ConferenceProviderArn: str,
        ConferenceProviderType: ConferenceProviderTypeType,
        MeetingSetting: MeetingSettingTypeDef,
        IPDialIn: IPDialInTypeDef = ...,
        PSTNDialIn: PSTNDialInTypeDef = ...,
    ) -> Dict[str, Any]:
        """
        Updates an existing conference provider's settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.update_conference_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#update_conference_provider)
        """

    async def update_contact(
        self,
        *,
        ContactArn: str,
        DisplayName: str = ...,
        FirstName: str = ...,
        LastName: str = ...,
        PhoneNumber: str = ...,
        PhoneNumbers: Sequence[PhoneNumberTypeDef] = ...,
        SipAddresses: Sequence[SipAddressTypeDef] = ...,
    ) -> Dict[str, Any]:
        """
        Updates the contact details by the contact ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.update_contact)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#update_contact)
        """

    async def update_device(self, *, DeviceArn: str = ..., DeviceName: str = ...) -> Dict[str, Any]:
        """
        Updates the device name by device ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.update_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#update_device)
        """

    async def update_gateway(
        self,
        *,
        GatewayArn: str,
        Name: str = ...,
        Description: str = ...,
        SoftwareVersion: str = ...,
    ) -> Dict[str, Any]:
        """
        Updates the details of a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.update_gateway)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#update_gateway)
        """

    async def update_gateway_group(
        self, *, GatewayGroupArn: str, Name: str = ..., Description: str = ...
    ) -> Dict[str, Any]:
        """
        Updates the details of a gateway group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.update_gateway_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#update_gateway_group)
        """

    async def update_network_profile(
        self,
        *,
        NetworkProfileArn: str,
        NetworkProfileName: str = ...,
        Description: str = ...,
        CurrentPassword: str = ...,
        NextPassword: str = ...,
        CertificateAuthorityArn: str = ...,
        TrustAnchors: Sequence[str] = ...,
    ) -> Dict[str, Any]:
        """
        Updates a network profile by the network profile ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.update_network_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#update_network_profile)
        """

    async def update_profile(
        self,
        *,
        ProfileArn: str = ...,
        ProfileName: str = ...,
        IsDefault: bool = ...,
        Timezone: str = ...,
        Address: str = ...,
        DistanceUnit: DistanceUnitType = ...,
        TemperatureUnit: TemperatureUnitType = ...,
        WakeWord: WakeWordType = ...,
        Locale: str = ...,
        SetupModeDisabled: bool = ...,
        MaxVolumeLimit: int = ...,
        PSTNEnabled: bool = ...,
        DataRetentionOptIn: bool = ...,
        MeetingRoomConfiguration: UpdateMeetingRoomConfigurationTypeDef = ...,
    ) -> Dict[str, Any]:
        """
        Updates an existing room profile by room profile ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.update_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#update_profile)
        """

    async def update_room(
        self,
        *,
        RoomArn: str = ...,
        RoomName: str = ...,
        Description: str = ...,
        ProviderCalendarId: str = ...,
        ProfileArn: str = ...,
    ) -> Dict[str, Any]:
        """
        Updates room details by room ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.update_room)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#update_room)
        """

    async def update_skill_group(
        self, *, SkillGroupArn: str = ..., SkillGroupName: str = ..., Description: str = ...
    ) -> Dict[str, Any]:
        """
        Updates skill group details by skill group ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.update_skill_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#update_skill_group)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_business_report_schedules"]
    ) -> ListBusinessReportSchedulesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_conference_providers"]
    ) -> ListConferenceProvidersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_device_events"]
    ) -> ListDeviceEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_skills"]) -> ListSkillsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_skills_store_categories"]
    ) -> ListSkillsStoreCategoriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_skills_store_skills_by_category"]
    ) -> ListSkillsStoreSkillsByCategoryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_smart_home_appliances"]
    ) -> ListSmartHomeAppliancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tags"]) -> ListTagsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_devices"]) -> SearchDevicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_profiles"]) -> SearchProfilesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_rooms"]) -> SearchRoomsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_skill_groups"]
    ) -> SearchSkillGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_users"]) -> SearchUsersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/#get_paginator)
        """

    async def __aenter__(self) -> "AlexaForBusinessClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/alexaforbusiness.html#AlexaForBusiness.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_alexaforbusiness/client/)
        """
