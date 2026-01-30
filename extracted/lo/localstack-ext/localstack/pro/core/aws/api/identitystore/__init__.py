from datetime import datetime
from enum import StrEnum
from typing import TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

AttributePath = str
BooleanType = bool
ExceptionMessage = str
ExtensionName = str
ExternalIdIdentifier = str
ExternalIdIssuer = str
GroupDisplayName = str
IdentityStoreId = str
MaxResults = int
NextToken = str
RequestId = str
ResourceId = str
RetryAfterSeconds = int
SensitiveStringType = str
StringType = str
UserName = str


class AccessDeniedExceptionReason(StrEnum):
    KMS_ACCESS_DENIED = "KMS_ACCESS_DENIED"


class ConflictExceptionReason(StrEnum):
    UNIQUENESS_CONSTRAINT_VIOLATION = "UNIQUENESS_CONSTRAINT_VIOLATION"
    CONCURRENT_MODIFICATION = "CONCURRENT_MODIFICATION"


class ResourceNotFoundExceptionReason(StrEnum):
    KMS_KEY_NOT_FOUND = "KMS_KEY_NOT_FOUND"


class ResourceType(StrEnum):
    GROUP = "GROUP"
    USER = "USER"
    IDENTITY_STORE = "IDENTITY_STORE"
    GROUP_MEMBERSHIP = "GROUP_MEMBERSHIP"
    RESOURCE_POLICY = "RESOURCE_POLICY"


class ThrottlingExceptionReason(StrEnum):
    KMS_THROTTLING = "KMS_THROTTLING"


class UserStatus(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class ValidationExceptionReason(StrEnum):
    KMS_INVALID_ARN = "KMS_INVALID_ARN"
    KMS_INVALID_KEY_USAGE = "KMS_INVALID_KEY_USAGE"
    KMS_INVALID_STATE = "KMS_INVALID_STATE"
    KMS_DISABLED = "KMS_DISABLED"


class AccessDeniedException(ServiceException):
    """You do not have sufficient access to perform this action."""

    code: str = "AccessDeniedException"
    sender_fault: bool = False
    status_code: int = 400
    RequestId: RequestId | None
    Reason: AccessDeniedExceptionReason | None


class ConflictException(ServiceException):
    """This request cannot be completed for one of the following reasons:

    -  Performing the requested operation would violate an existing
       uniqueness claim in the identity store. Resolve the conflict before
       retrying this request.

    -  The requested resource was being concurrently modified by another
       request.
    """

    code: str = "ConflictException"
    sender_fault: bool = False
    status_code: int = 400
    RequestId: RequestId | None
    Reason: ConflictExceptionReason | None


class InternalServerException(ServiceException):
    """The request processing has failed because of an unknown error, exception
    or failure with an internal server.
    """

    code: str = "InternalServerException"
    sender_fault: bool = False
    status_code: int = 400
    RequestId: RequestId | None
    RetryAfterSeconds: RetryAfterSeconds | None


class ResourceNotFoundException(ServiceException):
    """Indicates that a requested resource is not found."""

    code: str = "ResourceNotFoundException"
    sender_fault: bool = False
    status_code: int = 400
    ResourceType: ResourceType | None
    ResourceId: ResourceId | None
    Reason: ResourceNotFoundExceptionReason | None
    RequestId: RequestId | None


class ServiceQuotaExceededException(ServiceException):
    """The request would cause the number of users or groups in the identity
    store to exceed the maximum allowed.
    """

    code: str = "ServiceQuotaExceededException"
    sender_fault: bool = False
    status_code: int = 400
    RequestId: RequestId | None


class ThrottlingException(ServiceException):
    """Indicates that the principal has crossed the throttling limits of the
    API operations.
    """

    code: str = "ThrottlingException"
    sender_fault: bool = False
    status_code: int = 400
    RequestId: RequestId | None
    RetryAfterSeconds: RetryAfterSeconds | None
    Reason: ThrottlingExceptionReason | None


class ValidationException(ServiceException):
    """The request failed because it contains a syntax error."""

    code: str = "ValidationException"
    sender_fault: bool = False
    status_code: int = 400
    RequestId: RequestId | None
    Reason: ValidationExceptionReason | None


class Address(TypedDict, total=False):
    """The address associated with the specified user."""

    StreetAddress: SensitiveStringType | None
    Locality: SensitiveStringType | None
    Region: SensitiveStringType | None
    PostalCode: SensitiveStringType | None
    Country: SensitiveStringType | None
    Formatted: SensitiveStringType | None
    Type: SensitiveStringType | None
    Primary: BooleanType | None


Addresses = list[Address]


class AttributeValue(TypedDict, total=False):
    """The value of the attribute. This is a ``Document`` type. This type is
    not supported by Java V1, Go V1, and older versions of the CLI.
    """

    pass


class UniqueAttribute(TypedDict, total=False):
    """An entity attribute that's unique to a specific entity."""

    AttributePath: AttributePath
    AttributeValue: AttributeValue


class ExternalId(TypedDict, total=False):
    """The identifier issued to this resource by an external identity provider."""

    Issuer: ExternalIdIssuer
    Id: ExternalIdIdentifier


class AlternateIdentifier(TypedDict, total=False):
    """A unique identifier for a user or group that is not the primary
    identifier. This value can be an identifier from an external identity
    provider (IdP) that is associated with the user, the group, or a unique
    attribute.
    """

    ExternalId: ExternalId | None
    UniqueAttribute: UniqueAttribute | None


class AttributeOperation(TypedDict, total=False):
    """An operation that applies to the requested group. This operation might
    add, replace, or remove an attribute.
    """

    AttributePath: AttributePath
    AttributeValue: AttributeValue | None


AttributeOperations = list[AttributeOperation]


class MemberId(TypedDict, total=False):
    """An object containing the identifier of a group member."""

    UserId: ResourceId | None


class CreateGroupMembershipRequest(ServiceRequest):
    IdentityStoreId: IdentityStoreId
    GroupId: ResourceId
    MemberId: MemberId


class CreateGroupMembershipResponse(TypedDict, total=False):
    MembershipId: ResourceId
    IdentityStoreId: IdentityStoreId


class CreateGroupRequest(ServiceRequest):
    IdentityStoreId: IdentityStoreId
    DisplayName: GroupDisplayName | None
    Description: SensitiveStringType | None


class CreateGroupResponse(TypedDict, total=False):
    GroupId: ResourceId
    IdentityStoreId: IdentityStoreId


Extensions = dict[ExtensionName, AttributeValue]


class Role(TypedDict, total=False):
    """The role associated with the user."""

    Value: SensitiveStringType | None
    Type: SensitiveStringType | None
    Primary: BooleanType | None


Roles = list[Role]


class Photo(TypedDict, total=False):
    """Contains information about a user's photo. Users can have up to 3
    photos, with one designated as primary. Supports common image formats,
    including jpg, jpeg, png, and gif.
    """

    Value: SensitiveStringType
    Type: SensitiveStringType | None
    Display: SensitiveStringType | None
    Primary: BooleanType | None


Photos = list[Photo]


class PhoneNumber(TypedDict, total=False):
    """The phone number associated with the user."""

    Value: SensitiveStringType | None
    Type: SensitiveStringType | None
    Primary: BooleanType | None


PhoneNumbers = list[PhoneNumber]


class Email(TypedDict, total=False):
    """The email address associated with the user."""

    Value: SensitiveStringType | None
    Type: SensitiveStringType | None
    Primary: BooleanType | None


Emails = list[Email]


class Name(TypedDict, total=False):
    """The full name of the user."""

    Formatted: SensitiveStringType | None
    FamilyName: SensitiveStringType | None
    GivenName: SensitiveStringType | None
    MiddleName: SensitiveStringType | None
    HonorificPrefix: SensitiveStringType | None
    HonorificSuffix: SensitiveStringType | None


class CreateUserRequest(ServiceRequest):
    IdentityStoreId: IdentityStoreId
    UserName: UserName | None
    Name: Name | None
    DisplayName: SensitiveStringType | None
    NickName: SensitiveStringType | None
    ProfileUrl: SensitiveStringType | None
    Emails: Emails | None
    Addresses: Addresses | None
    PhoneNumbers: PhoneNumbers | None
    UserType: SensitiveStringType | None
    Title: SensitiveStringType | None
    PreferredLanguage: SensitiveStringType | None
    Locale: SensitiveStringType | None
    Timezone: SensitiveStringType | None
    Photos: Photos | None
    Website: SensitiveStringType | None
    Birthdate: SensitiveStringType | None
    Roles: Roles | None
    Extensions: Extensions | None


class CreateUserResponse(TypedDict, total=False):
    IdentityStoreId: IdentityStoreId
    UserId: ResourceId


DateType = datetime


class DeleteGroupMembershipRequest(ServiceRequest):
    IdentityStoreId: IdentityStoreId
    MembershipId: ResourceId


class DeleteGroupMembershipResponse(TypedDict, total=False):
    pass


class DeleteGroupRequest(ServiceRequest):
    IdentityStoreId: IdentityStoreId
    GroupId: ResourceId


class DeleteGroupResponse(TypedDict, total=False):
    pass


class DeleteUserRequest(ServiceRequest):
    IdentityStoreId: IdentityStoreId
    UserId: ResourceId


class DeleteUserResponse(TypedDict, total=False):
    pass


class DescribeGroupMembershipRequest(ServiceRequest):
    IdentityStoreId: IdentityStoreId
    MembershipId: ResourceId


class DescribeGroupMembershipResponse(TypedDict, total=False):
    IdentityStoreId: IdentityStoreId
    MembershipId: ResourceId
    GroupId: ResourceId
    MemberId: MemberId
    CreatedAt: DateType | None
    UpdatedAt: DateType | None
    CreatedBy: StringType | None
    UpdatedBy: StringType | None


class DescribeGroupRequest(ServiceRequest):
    IdentityStoreId: IdentityStoreId
    GroupId: ResourceId


ExternalIds = list[ExternalId]


class DescribeGroupResponse(TypedDict, total=False):
    GroupId: ResourceId
    DisplayName: GroupDisplayName | None
    ExternalIds: ExternalIds | None
    Description: SensitiveStringType | None
    CreatedAt: DateType | None
    UpdatedAt: DateType | None
    CreatedBy: StringType | None
    UpdatedBy: StringType | None
    IdentityStoreId: IdentityStoreId


ExtensionNames = list[ExtensionName]


class DescribeUserRequest(ServiceRequest):
    IdentityStoreId: IdentityStoreId
    UserId: ResourceId
    Extensions: ExtensionNames | None


class DescribeUserResponse(TypedDict, total=False):
    IdentityStoreId: IdentityStoreId
    UserId: ResourceId
    UserName: UserName | None
    ExternalIds: ExternalIds | None
    Name: Name | None
    DisplayName: SensitiveStringType | None
    NickName: SensitiveStringType | None
    ProfileUrl: SensitiveStringType | None
    Emails: Emails | None
    Addresses: Addresses | None
    PhoneNumbers: PhoneNumbers | None
    UserType: SensitiveStringType | None
    Title: SensitiveStringType | None
    PreferredLanguage: SensitiveStringType | None
    Locale: SensitiveStringType | None
    Timezone: SensitiveStringType | None
    UserStatus: UserStatus | None
    Photos: Photos | None
    Website: SensitiveStringType | None
    Birthdate: SensitiveStringType | None
    Roles: Roles | None
    CreatedAt: DateType | None
    CreatedBy: StringType | None
    UpdatedAt: DateType | None
    UpdatedBy: StringType | None
    Extensions: Extensions | None


class Filter(TypedDict, total=False):
    """A query filter used by ``ListUsers`` and ``ListGroups``. This filter
    object provides the attribute name and attribute value to search users
    or groups.
    """

    AttributePath: AttributePath
    AttributeValue: SensitiveStringType


Filters = list[Filter]


class GetGroupIdRequest(ServiceRequest):
    IdentityStoreId: IdentityStoreId
    AlternateIdentifier: AlternateIdentifier


class GetGroupIdResponse(TypedDict, total=False):
    GroupId: ResourceId
    IdentityStoreId: IdentityStoreId


class GetGroupMembershipIdRequest(ServiceRequest):
    IdentityStoreId: IdentityStoreId
    GroupId: ResourceId
    MemberId: MemberId


class GetGroupMembershipIdResponse(TypedDict, total=False):
    MembershipId: ResourceId
    IdentityStoreId: IdentityStoreId


class GetUserIdRequest(ServiceRequest):
    IdentityStoreId: IdentityStoreId
    AlternateIdentifier: AlternateIdentifier


class GetUserIdResponse(TypedDict, total=False):
    IdentityStoreId: IdentityStoreId
    UserId: ResourceId


class Group(TypedDict, total=False):
    """A group object that contains the metadata and attributes for a specified
    group.
    """

    GroupId: ResourceId
    DisplayName: GroupDisplayName | None
    ExternalIds: ExternalIds | None
    Description: SensitiveStringType | None
    CreatedAt: DateType | None
    UpdatedAt: DateType | None
    CreatedBy: StringType | None
    UpdatedBy: StringType | None
    IdentityStoreId: IdentityStoreId


GroupIds = list[ResourceId]


class GroupMembership(TypedDict, total=False):
    """Contains the identifiers for a group, a group member, and a
    ``GroupMembership`` object in the identity store.
    """

    IdentityStoreId: IdentityStoreId
    MembershipId: ResourceId | None
    GroupId: ResourceId | None
    MemberId: MemberId | None
    CreatedAt: DateType | None
    UpdatedAt: DateType | None
    CreatedBy: StringType | None
    UpdatedBy: StringType | None


class GroupMembershipExistenceResult(TypedDict, total=False):
    """Indicates whether a resource is a member of a group in the identity
    store.
    """

    GroupId: ResourceId | None
    MemberId: MemberId | None
    MembershipExists: BooleanType | None


GroupMembershipExistenceResults = list[GroupMembershipExistenceResult]
GroupMemberships = list[GroupMembership]
Groups = list[Group]


class IsMemberInGroupsRequest(ServiceRequest):
    IdentityStoreId: IdentityStoreId
    MemberId: MemberId
    GroupIds: GroupIds


class IsMemberInGroupsResponse(TypedDict, total=False):
    Results: GroupMembershipExistenceResults


class ListGroupMembershipsForMemberRequest(ServiceRequest):
    IdentityStoreId: IdentityStoreId
    MemberId: MemberId
    MaxResults: MaxResults | None
    NextToken: NextToken | None


class ListGroupMembershipsForMemberResponse(TypedDict, total=False):
    GroupMemberships: GroupMemberships
    NextToken: NextToken | None


class ListGroupMembershipsRequest(ServiceRequest):
    IdentityStoreId: IdentityStoreId
    GroupId: ResourceId
    MaxResults: MaxResults | None
    NextToken: NextToken | None


class ListGroupMembershipsResponse(TypedDict, total=False):
    GroupMemberships: GroupMemberships
    NextToken: NextToken | None


class ListGroupsRequest(ServiceRequest):
    IdentityStoreId: IdentityStoreId
    MaxResults: MaxResults | None
    NextToken: NextToken | None
    Filters: Filters | None


class ListGroupsResponse(TypedDict, total=False):
    Groups: Groups
    NextToken: NextToken | None


class ListUsersRequest(ServiceRequest):
    IdentityStoreId: IdentityStoreId
    Extensions: ExtensionNames | None
    MaxResults: MaxResults | None
    NextToken: NextToken | None
    Filters: Filters | None


class User(TypedDict, total=False):
    """A user object that contains the metadata and attributes for a specified
    user.
    """

    IdentityStoreId: IdentityStoreId
    UserId: ResourceId
    UserName: UserName | None
    ExternalIds: ExternalIds | None
    Name: Name | None
    DisplayName: SensitiveStringType | None
    NickName: SensitiveStringType | None
    ProfileUrl: SensitiveStringType | None
    Emails: Emails | None
    Addresses: Addresses | None
    PhoneNumbers: PhoneNumbers | None
    UserType: SensitiveStringType | None
    Title: SensitiveStringType | None
    PreferredLanguage: SensitiveStringType | None
    Locale: SensitiveStringType | None
    Timezone: SensitiveStringType | None
    UserStatus: UserStatus | None
    Photos: Photos | None
    Website: SensitiveStringType | None
    Birthdate: SensitiveStringType | None
    Roles: Roles | None
    CreatedAt: DateType | None
    CreatedBy: StringType | None
    UpdatedAt: DateType | None
    UpdatedBy: StringType | None
    Extensions: Extensions | None


Users = list[User]


class ListUsersResponse(TypedDict, total=False):
    Users: Users
    NextToken: NextToken | None


class UpdateGroupRequest(ServiceRequest):
    IdentityStoreId: IdentityStoreId
    GroupId: ResourceId
    Operations: AttributeOperations


class UpdateGroupResponse(TypedDict, total=False):
    pass


class UpdateUserRequest(ServiceRequest):
    IdentityStoreId: IdentityStoreId
    UserId: ResourceId
    Operations: AttributeOperations


class UpdateUserResponse(TypedDict, total=False):
    pass


class IdentitystoreApi:
    service: str = "identitystore"
    version: str = "2020-06-15"

    @handler("CreateGroup")
    def create_group(
        self,
        context: RequestContext,
        identity_store_id: IdentityStoreId,
        display_name: GroupDisplayName | None = None,
        description: SensitiveStringType | None = None,
        **kwargs,
    ) -> CreateGroupResponse:
        """Creates a group within the specified identity store.

        :param identity_store_id: The globally unique identifier for the identity store.
        :param display_name: A string containing the name of the group.
        :param description: A string containing the description of the group.
        :returns: CreateGroupResponse
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ValidationException:
        :raises ServiceQuotaExceededException:
        """
        raise NotImplementedError

    @handler("CreateGroupMembership")
    def create_group_membership(
        self,
        context: RequestContext,
        identity_store_id: IdentityStoreId,
        group_id: ResourceId,
        member_id: MemberId,
        **kwargs,
    ) -> CreateGroupMembershipResponse:
        """Creates a relationship between a member and a group. The following
        identifiers must be specified: ``GroupId``, ``IdentityStoreId``, and
        ``MemberId``.

        :param identity_store_id: The globally unique identifier for the identity store.
        :param group_id: The identifier for a group in the identity store.
        :param member_id: An object that contains the identifier of a group member.
        :returns: CreateGroupMembershipResponse
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ValidationException:
        :raises ServiceQuotaExceededException:
        """
        raise NotImplementedError

    @handler("CreateUser")
    def create_user(
        self,
        context: RequestContext,
        identity_store_id: IdentityStoreId,
        user_name: UserName | None = None,
        name: Name | None = None,
        display_name: SensitiveStringType | None = None,
        nick_name: SensitiveStringType | None = None,
        profile_url: SensitiveStringType | None = None,
        emails: Emails | None = None,
        addresses: Addresses | None = None,
        phone_numbers: PhoneNumbers | None = None,
        user_type: SensitiveStringType | None = None,
        title: SensitiveStringType | None = None,
        preferred_language: SensitiveStringType | None = None,
        locale: SensitiveStringType | None = None,
        timezone: SensitiveStringType | None = None,
        photos: Photos | None = None,
        website: SensitiveStringType | None = None,
        birthdate: SensitiveStringType | None = None,
        roles: Roles | None = None,
        extensions: Extensions | None = None,
        **kwargs,
    ) -> CreateUserResponse:
        """Creates a user within the specified identity store.

        :param identity_store_id: The globally unique identifier for the identity store.
        :param user_name: A unique string used to identify the user.
        :param name: An object containing the name of the user.
        :param display_name: A string containing the name of the user.
        :param nick_name: A string containing an alternate name for the user.
        :param profile_url: A string containing a URL that might be associated with the user.
        :param emails: A list of ``Email`` objects containing email addresses associated with
        the user.
        :param addresses: A list of ``Address`` objects containing addresses associated with the
        user.
        :param phone_numbers: A list of ``PhoneNumber`` objects containing phone numbers associated
        with the user.
        :param user_type: A string indicating the type of user.
        :param title: A string containing the title of the user.
        :param preferred_language: A string containing the preferred language of the user.
        :param locale: A string containing the geographical region or location of the user.
        :param timezone: A string containing the time zone of the user.
        :param photos: A list of photos associated with the user.
        :param website: The user's personal website or blog URL.
        :param birthdate: The user's birthdate in YYYY-MM-DD format.
        :param roles: A list of ``Role`` objects containing roles associated with the user.
        :param extensions: A map with additional attribute extensions for the user.
        :returns: CreateUserResponse
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ValidationException:
        :raises ServiceQuotaExceededException:
        """
        raise NotImplementedError

    @handler("DeleteGroup")
    def delete_group(
        self,
        context: RequestContext,
        identity_store_id: IdentityStoreId,
        group_id: ResourceId,
        **kwargs,
    ) -> DeleteGroupResponse:
        """Delete a group within an identity store given ``GroupId``.

        :param identity_store_id: The globally unique identifier for the identity store.
        :param group_id: The identifier for a group in the identity store.
        :returns: DeleteGroupResponse
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("DeleteGroupMembership")
    def delete_group_membership(
        self,
        context: RequestContext,
        identity_store_id: IdentityStoreId,
        membership_id: ResourceId,
        **kwargs,
    ) -> DeleteGroupMembershipResponse:
        """Delete a membership within a group given ``MembershipId``.

        :param identity_store_id: The globally unique identifier for the identity store.
        :param membership_id: The identifier for a ``GroupMembership`` in an identity store.
        :returns: DeleteGroupMembershipResponse
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("DeleteUser")
    def delete_user(
        self,
        context: RequestContext,
        identity_store_id: IdentityStoreId,
        user_id: ResourceId,
        **kwargs,
    ) -> DeleteUserResponse:
        """Deletes a user within an identity store given ``UserId``.

        :param identity_store_id: The globally unique identifier for the identity store.
        :param user_id: The identifier for a user in the identity store.
        :returns: DeleteUserResponse
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("DescribeGroup")
    def describe_group(
        self,
        context: RequestContext,
        identity_store_id: IdentityStoreId,
        group_id: ResourceId,
        **kwargs,
    ) -> DescribeGroupResponse:
        """Retrieves the group metadata and attributes from ``GroupId`` in an
        identity store.

        If you have access to a member account, you can use this API operation
        from the member account. For more information, see `Limiting access to
        the identity store from member
        accounts <https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-accounts.html#limiting-access-from-member-accounts>`__
        in the *IAM Identity Center User Guide*.

        :param identity_store_id: The globally unique identifier for the identity store, such as
        ``d-1234567890``.
        :param group_id: The identifier for a group in the identity store.
        :returns: DescribeGroupResponse
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("DescribeGroupMembership")
    def describe_group_membership(
        self,
        context: RequestContext,
        identity_store_id: IdentityStoreId,
        membership_id: ResourceId,
        **kwargs,
    ) -> DescribeGroupMembershipResponse:
        """Retrieves membership metadata and attributes from ``MembershipId`` in an
        identity store.

        If you have access to a member account, you can use this API operation
        from the member account. For more information, see `Limiting access to
        the identity store from member
        accounts <https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-accounts.html#limiting-access-from-member-accounts>`__
        in the *IAM Identity Center User Guide*.

        :param identity_store_id: The globally unique identifier for the identity store.
        :param membership_id: The identifier for a ``GroupMembership`` in an identity store.
        :returns: DescribeGroupMembershipResponse
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("DescribeUser")
    def describe_user(
        self,
        context: RequestContext,
        identity_store_id: IdentityStoreId,
        user_id: ResourceId,
        extensions: ExtensionNames | None = None,
        **kwargs,
    ) -> DescribeUserResponse:
        """Retrieves the user metadata and attributes from the ``UserId`` in an
        identity store.

        If you have access to a member account, you can use this API operation
        from the member account. For more information, see `Limiting access to
        the identity store from member
        accounts <https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-accounts.html#limiting-access-from-member-accounts>`__
        in the *IAM Identity Center User Guide*.

        :param identity_store_id: The globally unique identifier for the identity store, such as
        ``d-1234567890``.
        :param user_id: The identifier for a user in the identity store.
        :param extensions: A collection of extension names indicating what extensions the service
        should retrieve alongside other user attributes.
        :returns: DescribeUserResponse
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("GetGroupId")
    def get_group_id(
        self,
        context: RequestContext,
        identity_store_id: IdentityStoreId,
        alternate_identifier: AlternateIdentifier,
        **kwargs,
    ) -> GetGroupIdResponse:
        """Retrieves ``GroupId`` in an identity store.

        If you have access to a member account, you can use this API operation
        from the member account. For more information, see `Limiting access to
        the identity store from member
        accounts <https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-accounts.html#limiting-access-from-member-accounts>`__
        in the *IAM Identity Center User Guide*.

        :param identity_store_id: The globally unique identifier for the identity store.
        :param alternate_identifier: A unique identifier for a user or group that is not the primary
        identifier.
        :returns: GetGroupIdResponse
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("GetGroupMembershipId")
    def get_group_membership_id(
        self,
        context: RequestContext,
        identity_store_id: IdentityStoreId,
        group_id: ResourceId,
        member_id: MemberId,
        **kwargs,
    ) -> GetGroupMembershipIdResponse:
        """Retrieves the ``MembershipId`` in an identity store.

        If you have access to a member account, you can use this API operation
        from the member account. For more information, see `Limiting access to
        the identity store from member
        accounts <https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-accounts.html#limiting-access-from-member-accounts>`__
        in the *IAM Identity Center User Guide*.

        :param identity_store_id: The globally unique identifier for the identity store.
        :param group_id: The identifier for a group in the identity store.
        :param member_id: An object that contains the identifier of a group member.
        :returns: GetGroupMembershipIdResponse
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("GetUserId")
    def get_user_id(
        self,
        context: RequestContext,
        identity_store_id: IdentityStoreId,
        alternate_identifier: AlternateIdentifier,
        **kwargs,
    ) -> GetUserIdResponse:
        """Retrieves the ``UserId`` in an identity store.

        If you have access to a member account, you can use this API operation
        from the member account. For more information, see `Limiting access to
        the identity store from member
        accounts <https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-accounts.html#limiting-access-from-member-accounts>`__
        in the *IAM Identity Center User Guide*.

        :param identity_store_id: The globally unique identifier for the identity store.
        :param alternate_identifier: A unique identifier for a user or group that is not the primary
        identifier.
        :returns: GetUserIdResponse
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("IsMemberInGroups")
    def is_member_in_groups(
        self,
        context: RequestContext,
        identity_store_id: IdentityStoreId,
        member_id: MemberId,
        group_ids: GroupIds,
        **kwargs,
    ) -> IsMemberInGroupsResponse:
        """Checks the user's membership in all requested groups and returns if the
        member exists in all queried groups.

        If you have access to a member account, you can use this API operation
        from the member account. For more information, see `Limiting access to
        the identity store from member
        accounts <https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-accounts.html#limiting-access-from-member-accounts>`__
        in the *IAM Identity Center User Guide*.

        :param identity_store_id: The globally unique identifier for the identity store.
        :param member_id: An object containing the identifier of a group member.
        :param group_ids: A list of identifiers for groups in the identity store.
        :returns: IsMemberInGroupsResponse
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("ListGroupMemberships")
    def list_group_memberships(
        self,
        context: RequestContext,
        identity_store_id: IdentityStoreId,
        group_id: ResourceId,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListGroupMembershipsResponse:
        """For the specified group in the specified identity store, returns the
        list of all ``GroupMembership`` objects and returns results in paginated
        form.

        If you have access to a member account, you can use this API operation
        from the member account. For more information, see `Limiting access to
        the identity store from member
        accounts <https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-accounts.html#limiting-access-from-member-accounts>`__
        in the *IAM Identity Center User Guide*.

        :param identity_store_id: The globally unique identifier for the identity store.
        :param group_id: The identifier for a group in the identity store.
        :param max_results: The maximum number of results to be returned per request.
        :param next_token: The pagination token used for the ``ListUsers``, ``ListGroups`` and
        ``ListGroupMemberships`` API operations.
        :returns: ListGroupMembershipsResponse
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("ListGroupMembershipsForMember")
    def list_group_memberships_for_member(
        self,
        context: RequestContext,
        identity_store_id: IdentityStoreId,
        member_id: MemberId,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListGroupMembershipsForMemberResponse:
        """For the specified member in the specified identity store, returns the
        list of all ``GroupMembership`` objects and returns results in paginated
        form.

        If you have access to a member account, you can use this API operation
        from the member account. For more information, see `Limiting access to
        the identity store from member
        accounts <https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-accounts.html#limiting-access-from-member-accounts>`__
        in the *IAM Identity Center User Guide*.

        :param identity_store_id: The globally unique identifier for the identity store.
        :param member_id: An object that contains the identifier of a group member.
        :param max_results: The maximum number of results to be returned per request.
        :param next_token: The pagination token used for the ``ListUsers``, ``ListGroups``, and
        ``ListGroupMemberships`` API operations.
        :returns: ListGroupMembershipsForMemberResponse
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("ListGroups")
    def list_groups(
        self,
        context: RequestContext,
        identity_store_id: IdentityStoreId,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        filters: Filters | None = None,
        **kwargs,
    ) -> ListGroupsResponse:
        """Lists all groups in the identity store. Returns a paginated list of
        complete ``Group`` objects. Filtering for a ``Group`` by the
        ``DisplayName`` attribute is deprecated. Instead, use the ``GetGroupId``
        API action.

        If you have access to a member account, you can use this API operation
        from the member account. For more information, see `Limiting access to
        the identity store from member
        accounts <https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-accounts.html#limiting-access-from-member-accounts>`__
        in the *IAM Identity Center User Guide*.

        :param identity_store_id: The globally unique identifier for the identity store, such as
        ``d-1234567890``.
        :param max_results: The maximum number of results to be returned per request.
        :param next_token: The pagination token used for the ``ListUsers`` and ``ListGroups`` API
        operations.
        :param filters: A list of ``Filter`` objects, which is used in the ``ListUsers`` and
        ``ListGroups`` requests.
        :returns: ListGroupsResponse
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("ListUsers")
    def list_users(
        self,
        context: RequestContext,
        identity_store_id: IdentityStoreId,
        extensions: ExtensionNames | None = None,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        filters: Filters | None = None,
        **kwargs,
    ) -> ListUsersResponse:
        """Lists all users in the identity store. Returns a paginated list of
        complete ``User`` objects. Filtering for a ``User`` by the ``UserName``
        attribute is deprecated. Instead, use the ``GetUserId`` API action.

        If you have access to a member account, you can use this API operation
        from the member account. For more information, see `Limiting access to
        the identity store from member
        accounts <https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-accounts.html#limiting-access-from-member-accounts>`__
        in the *IAM Identity Center User Guide*.

        :param identity_store_id: The globally unique identifier for the identity store, such as
        ``d-1234567890``.
        :param extensions: A collection of extension names indicating what extensions the service
        should retrieve alongside other user attributes.
        :param max_results: The maximum number of results to be returned per request.
        :param next_token: The pagination token used for the ``ListUsers`` and ``ListGroups`` API
        operations.
        :param filters: A list of ``Filter`` objects, which is used in the ``ListUsers`` and
        ``ListGroups`` requests.
        :returns: ListUsersResponse
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("UpdateGroup")
    def update_group(
        self,
        context: RequestContext,
        identity_store_id: IdentityStoreId,
        group_id: ResourceId,
        operations: AttributeOperations,
        **kwargs,
    ) -> UpdateGroupResponse:
        """Updates the specified group metadata and attributes in the specified
        identity store.

        :param identity_store_id: The globally unique identifier for the identity store.
        :param group_id: The identifier for a group in the identity store.
        :param operations: A list of ``AttributeOperation`` objects to apply to the requested
        group.
        :returns: UpdateGroupResponse
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ValidationException:
        :raises ServiceQuotaExceededException:
        """
        raise NotImplementedError

    @handler("UpdateUser")
    def update_user(
        self,
        context: RequestContext,
        identity_store_id: IdentityStoreId,
        user_id: ResourceId,
        operations: AttributeOperations,
        **kwargs,
    ) -> UpdateUserResponse:
        """Updates the specified user metadata and attributes in the specified
        identity store.

        :param identity_store_id: The globally unique identifier for the identity store.
        :param user_id: The identifier for a user in the identity store.
        :param operations: A list of ``AttributeOperation`` objects to apply to the requested user.
        :returns: UpdateUserResponse
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ValidationException:
        :raises ServiceQuotaExceededException:
        """
        raise NotImplementedError
