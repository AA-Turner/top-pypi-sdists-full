from datetime import datetime
from enum import StrEnum
from typing import Dict, List, Optional, TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

ActionOrder = int
AllocationId = str
AlpnPolicyValue = str
AuthenticateCognitoActionAuthenticationRequestParamName = str
AuthenticateCognitoActionAuthenticationRequestParamValue = str
AuthenticateCognitoActionScope = str
AuthenticateCognitoActionSessionCookieName = str
AuthenticateCognitoActionUserPoolArn = str
AuthenticateCognitoActionUserPoolClientId = str
AuthenticateCognitoActionUserPoolDomain = str
AuthenticateOidcActionAuthenticationRequestParamName = str
AuthenticateOidcActionAuthenticationRequestParamValue = str
AuthenticateOidcActionAuthorizationEndpoint = str
AuthenticateOidcActionClientId = str
AuthenticateOidcActionClientSecret = str
AuthenticateOidcActionIssuer = str
AuthenticateOidcActionScope = str
AuthenticateOidcActionSessionCookieName = str
AuthenticateOidcActionTokenEndpoint = str
AuthenticateOidcActionUseExistingClientSecret = bool
AuthenticateOidcActionUserInfoEndpoint = str
CanonicalHostedZoneId = str
CapacityUnits = int
CapacityUnitsDouble = float
CertificateArn = str
CipherName = str
CipherPriority = int
ConditionFieldName = str
CustomerOwnedIpv4Pool = str
DNSName = str
DecreaseRequestsRemaining = int
Default = bool
Description = str
EnforceSecurityGroupInboundRulesOnPrivateLinkTraffic = str
FixedResponseActionContentType = str
FixedResponseActionMessage = str
FixedResponseActionStatusCode = str
GrpcCode = str
HealthCheckEnabled = bool
HealthCheckIntervalSeconds = int
HealthCheckPort = str
HealthCheckThresholdCount = int
HealthCheckTimeoutSeconds = int
HttpCode = str
HttpHeaderConditionName = str
IPv6Address = str
IgnoreClientCertificateExpiry = bool
IpAddress = str
IpamPoolId = str
IsDefault = bool
ListenerArn = str
ListenerAttributeKey = str
ListenerAttributeValue = str
LoadBalancerArn = str
LoadBalancerAttributeKey = str
LoadBalancerAttributeValue = str
LoadBalancerName = str
Location = str
Marker = str
Max = str
Mode = str
Name = str
NumberOfCaCertificates = int
OutpostId = str
PageSize = int
Path = str
Policy = str
Port = int
PrivateIPv4Address = str
ProtocolVersion = str
RedirectActionHost = str
RedirectActionPath = str
RedirectActionPort = str
RedirectActionProtocol = str
RedirectActionQuery = str
ResetCapacityReservation = bool
ResourceArn = str
RuleArn = str
RulePriority = int
S3Bucket = str
S3Key = str
S3ObjectVersion = str
SecurityGroupId = str
SourceNatIpv6Prefix = str
SslPolicyName = str
SslProtocol = str
StateReason = str
String = str
StringValue = str
SubnetId = str
TagKey = str
TagValue = str
TargetGroupArn = str
TargetGroupAttributeKey = str
TargetGroupAttributeValue = str
TargetGroupName = str
TargetGroupStickinessDurationSeconds = int
TargetGroupStickinessEnabled = bool
TargetGroupWeight = int
TargetId = str
TrustStoreArn = str
TrustStoreAssociationResourceArn = str
TrustStoreName = str
VpcId = str
ZoneName = str


class ActionTypeEnum(StrEnum):
    forward = "forward"
    authenticate_oidc = "authenticate-oidc"
    authenticate_cognito = "authenticate-cognito"
    redirect = "redirect"
    fixed_response = "fixed-response"


class AdvertiseTrustStoreCaNamesEnum(StrEnum):
    on = "on"
    off = "off"


class AnomalyResultEnum(StrEnum):
    anomalous = "anomalous"
    normal = "normal"


class AuthenticateCognitoActionConditionalBehaviorEnum(StrEnum):
    deny = "deny"
    allow = "allow"
    authenticate = "authenticate"


class AuthenticateOidcActionConditionalBehaviorEnum(StrEnum):
    deny = "deny"
    allow = "allow"
    authenticate = "authenticate"


class CapacityReservationStateEnum(StrEnum):
    provisioned = "provisioned"
    pending = "pending"
    rebalancing = "rebalancing"
    failed = "failed"


class DescribeTargetHealthInputIncludeEnum(StrEnum):
    AnomalyDetection = "AnomalyDetection"
    All = "All"


class EnablePrefixForIpv6SourceNatEnum(StrEnum):
    on = "on"
    off = "off"


class EnforceSecurityGroupInboundRulesOnPrivateLinkTrafficEnum(StrEnum):
    on = "on"
    off = "off"


class IpAddressType(StrEnum):
    ipv4 = "ipv4"
    dualstack = "dualstack"
    dualstack_without_public_ipv4 = "dualstack-without-public-ipv4"


class LoadBalancerSchemeEnum(StrEnum):
    internet_facing = "internet-facing"
    internal = "internal"


class LoadBalancerStateEnum(StrEnum):
    active = "active"
    provisioning = "provisioning"
    active_impaired = "active_impaired"
    failed = "failed"


class LoadBalancerTypeEnum(StrEnum):
    application = "application"
    network = "network"
    gateway = "gateway"


class MitigationInEffectEnum(StrEnum):
    yes = "yes"
    no = "no"


class ProtocolEnum(StrEnum):
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    TCP = "TCP"
    TLS = "TLS"
    UDP = "UDP"
    TCP_UDP = "TCP_UDP"
    GENEVE = "GENEVE"


class RedirectActionStatusCodeEnum(StrEnum):
    HTTP_301 = "HTTP_301"
    HTTP_302 = "HTTP_302"


class RemoveIpamPoolEnum(StrEnum):
    ipv4 = "ipv4"


class RevocationType(StrEnum):
    CRL = "CRL"


class TargetAdministrativeOverrideReasonEnum(StrEnum):
    AdministrativeOverride_Unknown = "AdministrativeOverride.Unknown"
    AdministrativeOverride_NoOverride = "AdministrativeOverride.NoOverride"
    AdministrativeOverride_ZonalShiftActive = "AdministrativeOverride.ZonalShiftActive"
    AdministrativeOverride_ZonalShiftDelegatedToDns = (
        "AdministrativeOverride.ZonalShiftDelegatedToDns"
    )


class TargetAdministrativeOverrideStateEnum(StrEnum):
    unknown = "unknown"
    no_override = "no_override"
    zonal_shift_active = "zonal_shift_active"
    zonal_shift_delegated_to_dns = "zonal_shift_delegated_to_dns"


class TargetGroupIpAddressTypeEnum(StrEnum):
    ipv4 = "ipv4"
    ipv6 = "ipv6"


class TargetHealthReasonEnum(StrEnum):
    Elb_RegistrationInProgress = "Elb.RegistrationInProgress"
    Elb_InitialHealthChecking = "Elb.InitialHealthChecking"
    Target_ResponseCodeMismatch = "Target.ResponseCodeMismatch"
    Target_Timeout = "Target.Timeout"
    Target_FailedHealthChecks = "Target.FailedHealthChecks"
    Target_NotRegistered = "Target.NotRegistered"
    Target_NotInUse = "Target.NotInUse"
    Target_DeregistrationInProgress = "Target.DeregistrationInProgress"
    Target_InvalidState = "Target.InvalidState"
    Target_IpUnusable = "Target.IpUnusable"
    Target_HealthCheckDisabled = "Target.HealthCheckDisabled"
    Elb_InternalError = "Elb.InternalError"


class TargetHealthStateEnum(StrEnum):
    initial = "initial"
    healthy = "healthy"
    unhealthy = "unhealthy"
    unhealthy_draining = "unhealthy.draining"
    unused = "unused"
    draining = "draining"
    unavailable = "unavailable"


class TargetTypeEnum(StrEnum):
    instance = "instance"
    ip = "ip"
    lambda_ = "lambda"
    alb = "alb"


class TrustStoreAssociationStatusEnum(StrEnum):
    active = "active"
    removed = "removed"


class TrustStoreStatus(StrEnum):
    ACTIVE = "ACTIVE"
    CREATING = "CREATING"


class ALPNPolicyNotSupportedException(ServiceException):
    """The specified ALPN policy is not supported."""

    code: str = "ALPNPolicyNotFound"
    sender_fault: bool = True
    status_code: int = 400


class AllocationIdNotFoundException(ServiceException):
    """The specified allocation ID does not exist."""

    code: str = "AllocationIdNotFound"
    sender_fault: bool = True
    status_code: int = 400


class AvailabilityZoneNotSupportedException(ServiceException):
    """The specified Availability Zone is not supported."""

    code: str = "AvailabilityZoneNotSupported"
    sender_fault: bool = True
    status_code: int = 400


class CaCertificatesBundleNotFoundException(ServiceException):
    """The specified ca certificate bundle does not exist."""

    code: str = "CaCertificatesBundleNotFound"
    sender_fault: bool = True
    status_code: int = 400


class CapacityDecreaseRequestsLimitExceededException(ServiceException):
    """You've exceeded the daily capacity decrease limit for this reservation."""

    code: str = "CapacityDecreaseRequestLimitExceeded"
    sender_fault: bool = True
    status_code: int = 400


class CapacityReservationPendingException(ServiceException):
    """There is a pending capacity reservation."""

    code: str = "CapacityReservationPending"
    sender_fault: bool = True
    status_code: int = 400


class CapacityUnitsLimitExceededException(ServiceException):
    """You've exceeded the capacity units limit."""

    code: str = "CapacityUnitsLimitExceeded"
    sender_fault: bool = True
    status_code: int = 400


class CertificateNotFoundException(ServiceException):
    """The specified certificate does not exist."""

    code: str = "CertificateNotFound"
    sender_fault: bool = True
    status_code: int = 400


class DeleteAssociationSameAccountException(ServiceException):
    """The specified association can't be within the same account."""

    code: str = "DeleteAssociationSameAccount"
    sender_fault: bool = True
    status_code: int = 400


class DuplicateListenerException(ServiceException):
    """A listener with the specified port already exists."""

    code: str = "DuplicateListener"
    sender_fault: bool = True
    status_code: int = 400


class DuplicateLoadBalancerNameException(ServiceException):
    """A load balancer with the specified name already exists."""

    code: str = "DuplicateLoadBalancerName"
    sender_fault: bool = True
    status_code: int = 400


class DuplicateTagKeysException(ServiceException):
    """A tag key was specified more than once."""

    code: str = "DuplicateTagKeys"
    sender_fault: bool = True
    status_code: int = 400


class DuplicateTargetGroupNameException(ServiceException):
    """A target group with the specified name already exists."""

    code: str = "DuplicateTargetGroupName"
    sender_fault: bool = True
    status_code: int = 400


class DuplicateTrustStoreNameException(ServiceException):
    """A trust store with the specified name already exists."""

    code: str = "DuplicateTrustStoreName"
    sender_fault: bool = True
    status_code: int = 400


class HealthUnavailableException(ServiceException):
    """The health of the specified targets could not be retrieved due to an
    internal error.
    """

    code: str = "HealthUnavailable"
    sender_fault: bool = False
    status_code: int = 500


class IncompatibleProtocolsException(ServiceException):
    """The specified configuration is not valid with this protocol."""

    code: str = "IncompatibleProtocols"
    sender_fault: bool = True
    status_code: int = 400


class InsufficientCapacityException(ServiceException):
    """There is insufficient capacity to reserve."""

    code: str = "InsufficientCapacity"
    sender_fault: bool = False
    status_code: int = 500


class InvalidCaCertificatesBundleException(ServiceException):
    """The specified ca certificate bundle is in an invalid format, or corrupt."""

    code: str = "InvalidCaCertificatesBundle"
    sender_fault: bool = True
    status_code: int = 400


class InvalidConfigurationRequestException(ServiceException):
    """The requested configuration is not valid."""

    code: str = "InvalidConfigurationRequest"
    sender_fault: bool = True
    status_code: int = 400


class InvalidLoadBalancerActionException(ServiceException):
    """The requested action is not valid."""

    code: str = "InvalidLoadBalancerAction"
    sender_fault: bool = True
    status_code: int = 400


class InvalidRevocationContentException(ServiceException):
    """The provided revocation file is an invalid format, or uses an incorrect
    algorithm.
    """

    code: str = "InvalidRevocationContent"
    sender_fault: bool = True
    status_code: int = 400


class InvalidSchemeException(ServiceException):
    """The requested scheme is not valid."""

    code: str = "InvalidScheme"
    sender_fault: bool = True
    status_code: int = 400


class InvalidSecurityGroupException(ServiceException):
    """The specified security group does not exist."""

    code: str = "InvalidSecurityGroup"
    sender_fault: bool = True
    status_code: int = 400


class InvalidSubnetException(ServiceException):
    """The specified subnet is out of available addresses."""

    code: str = "InvalidSubnet"
    sender_fault: bool = True
    status_code: int = 400


class InvalidTargetException(ServiceException):
    """The specified target does not exist, is not in the same VPC as the
    target group, or has an unsupported instance type.
    """

    code: str = "InvalidTarget"
    sender_fault: bool = True
    status_code: int = 400


class ListenerNotFoundException(ServiceException):
    """The specified listener does not exist."""

    code: str = "ListenerNotFound"
    sender_fault: bool = True
    status_code: int = 400


class LoadBalancerNotFoundException(ServiceException):
    """The specified load balancer does not exist."""

    code: str = "LoadBalancerNotFound"
    sender_fault: bool = True
    status_code: int = 400


class OperationNotPermittedException(ServiceException):
    """This operation is not allowed."""

    code: str = "OperationNotPermitted"
    sender_fault: bool = True
    status_code: int = 400


class PriorRequestNotCompleteException(ServiceException):
    """This operation is not allowed while a prior request has not been
    completed.
    """

    code: str = "PriorRequestNotComplete"
    sender_fault: bool = True
    status_code: int = 429


class PriorityInUseException(ServiceException):
    """The specified priority is in use."""

    code: str = "PriorityInUse"
    sender_fault: bool = True
    status_code: int = 400


class ResourceInUseException(ServiceException):
    """A specified resource is in use."""

    code: str = "ResourceInUse"
    sender_fault: bool = True
    status_code: int = 400


class ResourceNotFoundException(ServiceException):
    """The specified resource does not exist."""

    code: str = "ResourceNotFound"
    sender_fault: bool = True
    status_code: int = 400


class RevocationContentNotFoundException(ServiceException):
    """The specified revocation file does not exist."""

    code: str = "RevocationContentNotFound"
    sender_fault: bool = True
    status_code: int = 400


class RevocationIdNotFoundException(ServiceException):
    """The specified revocation ID does not exist."""

    code: str = "RevocationIdNotFound"
    sender_fault: bool = True
    status_code: int = 400


class RuleNotFoundException(ServiceException):
    """The specified rule does not exist."""

    code: str = "RuleNotFound"
    sender_fault: bool = True
    status_code: int = 400


class SSLPolicyNotFoundException(ServiceException):
    """The specified SSL policy does not exist."""

    code: str = "SSLPolicyNotFound"
    sender_fault: bool = True
    status_code: int = 400


class SubnetNotFoundException(ServiceException):
    """The specified subnet does not exist."""

    code: str = "SubnetNotFound"
    sender_fault: bool = True
    status_code: int = 400


class TargetGroupAssociationLimitException(ServiceException):
    """You've reached the limit on the number of load balancers per target
    group.
    """

    code: str = "TargetGroupAssociationLimit"
    sender_fault: bool = True
    status_code: int = 400


class TargetGroupNotFoundException(ServiceException):
    """The specified target group does not exist."""

    code: str = "TargetGroupNotFound"
    sender_fault: bool = True
    status_code: int = 400


class TooManyActionsException(ServiceException):
    """You've reached the limit on the number of actions per rule."""

    code: str = "TooManyActions"
    sender_fault: bool = True
    status_code: int = 400


class TooManyCertificatesException(ServiceException):
    """You've reached the limit on the number of certificates per load
    balancer.
    """

    code: str = "TooManyCertificates"
    sender_fault: bool = True
    status_code: int = 400


class TooManyListenersException(ServiceException):
    """You've reached the limit on the number of listeners per load balancer."""

    code: str = "TooManyListeners"
    sender_fault: bool = True
    status_code: int = 400


class TooManyLoadBalancersException(ServiceException):
    """You've reached the limit on the number of load balancers for your Amazon
    Web Services account.
    """

    code: str = "TooManyLoadBalancers"
    sender_fault: bool = True
    status_code: int = 400


class TooManyRegistrationsForTargetIdException(ServiceException):
    """You've reached the limit on the number of times a target can be
    registered with a load balancer.
    """

    code: str = "TooManyRegistrationsForTargetId"
    sender_fault: bool = True
    status_code: int = 400


class TooManyRulesException(ServiceException):
    """You've reached the limit on the number of rules per load balancer."""

    code: str = "TooManyRules"
    sender_fault: bool = True
    status_code: int = 400


class TooManyTagsException(ServiceException):
    """You've reached the limit on the number of tags for this resource."""

    code: str = "TooManyTags"
    sender_fault: bool = True
    status_code: int = 400


class TooManyTargetGroupsException(ServiceException):
    """You've reached the limit on the number of target groups for your Amazon
    Web Services account.
    """

    code: str = "TooManyTargetGroups"
    sender_fault: bool = True
    status_code: int = 400


class TooManyTargetsException(ServiceException):
    """You've reached the limit on the number of targets."""

    code: str = "TooManyTargets"
    sender_fault: bool = True
    status_code: int = 400


class TooManyTrustStoreRevocationEntriesException(ServiceException):
    """The specified trust store has too many revocation entries."""

    code: str = "TooManyTrustStoreRevocationEntries"
    sender_fault: bool = True
    status_code: int = 400


class TooManyTrustStoresException(ServiceException):
    """You've reached the limit on the number of trust stores for your Amazon
    Web Services account.
    """

    code: str = "TooManyTrustStores"
    sender_fault: bool = True
    status_code: int = 400


class TooManyUniqueTargetGroupsPerLoadBalancerException(ServiceException):
    """You've reached the limit on the number of unique target groups per load
    balancer across all listeners. If a target group is used by multiple
    actions for a load balancer, it is counted as only one use.
    """

    code: str = "TooManyUniqueTargetGroupsPerLoadBalancer"
    sender_fault: bool = True
    status_code: int = 400


class TrustStoreAssociationNotFoundException(ServiceException):
    """The specified association does not exist."""

    code: str = "AssociationNotFound"
    sender_fault: bool = True
    status_code: int = 400


class TrustStoreInUseException(ServiceException):
    """The specified trust store is currently in use."""

    code: str = "TrustStoreInUse"
    sender_fault: bool = True
    status_code: int = 400


class TrustStoreNotFoundException(ServiceException):
    """The specified trust store does not exist."""

    code: str = "TrustStoreNotFound"
    sender_fault: bool = True
    status_code: int = 400


class TrustStoreNotReadyException(ServiceException):
    """The specified trust store is not active."""

    code: str = "TrustStoreNotReady"
    sender_fault: bool = True
    status_code: int = 400


class UnsupportedProtocolException(ServiceException):
    """The specified protocol is not supported."""

    code: str = "UnsupportedProtocol"
    sender_fault: bool = True
    status_code: int = 400


class TargetGroupStickinessConfig(TypedDict, total=False):
    """Information about the target group stickiness for a rule."""

    Enabled: Optional[TargetGroupStickinessEnabled]
    DurationSeconds: Optional[TargetGroupStickinessDurationSeconds]


class TargetGroupTuple(TypedDict, total=False):
    """Information about how traffic will be distributed between multiple
    target groups in a forward rule.
    """

    TargetGroupArn: Optional[TargetGroupArn]
    Weight: Optional[TargetGroupWeight]


TargetGroupList = List[TargetGroupTuple]


class ForwardActionConfig(TypedDict, total=False):
    """Information about a forward action."""

    TargetGroups: Optional[TargetGroupList]
    TargetGroupStickinessConfig: Optional[TargetGroupStickinessConfig]


class FixedResponseActionConfig(TypedDict, total=False):
    """Information about an action that returns a custom HTTP response."""

    MessageBody: Optional[FixedResponseActionMessage]
    StatusCode: FixedResponseActionStatusCode
    ContentType: Optional[FixedResponseActionContentType]


class RedirectActionConfig(TypedDict, total=False):
    """Information about a redirect action.

    A URI consists of the following components:
    protocol://hostname:port/path?query. You must modify at least one of the
    following components to avoid a redirect loop: protocol, hostname, port,
    or path. Any components that you do not modify retain their original
    values.

    You can reuse URI components using the following reserved keywords:

    -  #{protocol}

    -  #{host}

    -  #{port}

    -  #{path} (the leading "/" is removed)

    -  #{query}

    For example, you can change the path to "/new/#{path}", the hostname to
    "example.#{host}", or the query to "#{query}&value=xyz".
    """

    Protocol: Optional[RedirectActionProtocol]
    Port: Optional[RedirectActionPort]
    Host: Optional[RedirectActionHost]
    Path: Optional[RedirectActionPath]
    Query: Optional[RedirectActionQuery]
    StatusCode: RedirectActionStatusCodeEnum


AuthenticateCognitoActionAuthenticationRequestExtraParams = Dict[
    AuthenticateCognitoActionAuthenticationRequestParamName,
    AuthenticateCognitoActionAuthenticationRequestParamValue,
]
AuthenticateCognitoActionSessionTimeout = int


class AuthenticateCognitoActionConfig(TypedDict, total=False):
    """Request parameters to use when integrating with Amazon Cognito to
    authenticate users.
    """

    UserPoolArn: AuthenticateCognitoActionUserPoolArn
    UserPoolClientId: AuthenticateCognitoActionUserPoolClientId
    UserPoolDomain: AuthenticateCognitoActionUserPoolDomain
    SessionCookieName: Optional[AuthenticateCognitoActionSessionCookieName]
    Scope: Optional[AuthenticateCognitoActionScope]
    SessionTimeout: Optional[AuthenticateCognitoActionSessionTimeout]
    AuthenticationRequestExtraParams: Optional[
        AuthenticateCognitoActionAuthenticationRequestExtraParams
    ]
    OnUnauthenticatedRequest: Optional[AuthenticateCognitoActionConditionalBehaviorEnum]


AuthenticateOidcActionAuthenticationRequestExtraParams = Dict[
    AuthenticateOidcActionAuthenticationRequestParamName,
    AuthenticateOidcActionAuthenticationRequestParamValue,
]
AuthenticateOidcActionSessionTimeout = int


class AuthenticateOidcActionConfig(TypedDict, total=False):
    """Request parameters when using an identity provider (IdP) that is
    compliant with OpenID Connect (OIDC) to authenticate users.
    """

    Issuer: AuthenticateOidcActionIssuer
    AuthorizationEndpoint: AuthenticateOidcActionAuthorizationEndpoint
    TokenEndpoint: AuthenticateOidcActionTokenEndpoint
    UserInfoEndpoint: AuthenticateOidcActionUserInfoEndpoint
    ClientId: AuthenticateOidcActionClientId
    ClientSecret: Optional[AuthenticateOidcActionClientSecret]
    SessionCookieName: Optional[AuthenticateOidcActionSessionCookieName]
    Scope: Optional[AuthenticateOidcActionScope]
    SessionTimeout: Optional[AuthenticateOidcActionSessionTimeout]
    AuthenticationRequestExtraParams: Optional[
        AuthenticateOidcActionAuthenticationRequestExtraParams
    ]
    OnUnauthenticatedRequest: Optional[AuthenticateOidcActionConditionalBehaviorEnum]
    UseExistingClientSecret: Optional[AuthenticateOidcActionUseExistingClientSecret]


class Action(TypedDict, total=False):
    """Information about an action.

    Each rule must include exactly one of the following types of actions:
    ``forward``, ``fixed-response``, or ``redirect``, and it must be the
    last action to be performed.
    """

    Type: ActionTypeEnum
    TargetGroupArn: Optional[TargetGroupArn]
    AuthenticateOidcConfig: Optional[AuthenticateOidcActionConfig]
    AuthenticateCognitoConfig: Optional[AuthenticateCognitoActionConfig]
    Order: Optional[ActionOrder]
    RedirectConfig: Optional[RedirectActionConfig]
    FixedResponseConfig: Optional[FixedResponseActionConfig]
    ForwardConfig: Optional[ForwardActionConfig]


Actions = List[Action]


class Certificate(TypedDict, total=False):
    """Information about an SSL server certificate."""

    CertificateArn: Optional[CertificateArn]
    IsDefault: Optional[Default]


CertificateList = List[Certificate]


class AddListenerCertificatesInput(ServiceRequest):
    ListenerArn: ListenerArn
    Certificates: CertificateList


class AddListenerCertificatesOutput(TypedDict, total=False):
    Certificates: Optional[CertificateList]


class Tag(TypedDict, total=False):
    """Information about a tag."""

    Key: TagKey
    Value: Optional[TagValue]


TagList = List[Tag]
ResourceArns = List[ResourceArn]


class AddTagsInput(ServiceRequest):
    ResourceArns: ResourceArns
    Tags: TagList


class AddTagsOutput(TypedDict, total=False):
    pass


class RevocationContent(TypedDict, total=False):
    """Information about a revocation file."""

    S3Bucket: Optional[S3Bucket]
    S3Key: Optional[S3Key]
    S3ObjectVersion: Optional[S3ObjectVersion]
    RevocationType: Optional[RevocationType]


RevocationContents = List[RevocationContent]


class AddTrustStoreRevocationsInput(ServiceRequest):
    TrustStoreArn: TrustStoreArn
    RevocationContents: Optional[RevocationContents]


NumberOfRevokedEntries = int
RevocationId = int


class TrustStoreRevocation(TypedDict, total=False):
    """Information about a revocation file in use by a trust store."""

    TrustStoreArn: Optional[TrustStoreArn]
    RevocationId: Optional[RevocationId]
    RevocationType: Optional[RevocationType]
    NumberOfRevokedEntries: Optional[NumberOfRevokedEntries]


TrustStoreRevocations = List[TrustStoreRevocation]


class AddTrustStoreRevocationsOutput(TypedDict, total=False):
    TrustStoreRevocations: Optional[TrustStoreRevocations]


class AdministrativeOverride(TypedDict, total=False):
    """Information about the override status applied to a target."""

    State: Optional[TargetAdministrativeOverrideStateEnum]
    Reason: Optional[TargetAdministrativeOverrideReasonEnum]
    Description: Optional[Description]


AlpnPolicyName = List[AlpnPolicyValue]


class AnomalyDetection(TypedDict, total=False):
    """Information about anomaly detection and mitigation."""

    Result: Optional[AnomalyResultEnum]
    MitigationInEffect: Optional[MitigationInEffectEnum]


SourceNatIpv6Prefixes = List[SourceNatIpv6Prefix]


class LoadBalancerAddress(TypedDict, total=False):
    """Information about a static IP address for a load balancer."""

    IpAddress: Optional[IpAddress]
    AllocationId: Optional[AllocationId]
    PrivateIPv4Address: Optional[PrivateIPv4Address]
    IPv6Address: Optional[IPv6Address]


LoadBalancerAddresses = List[LoadBalancerAddress]


class AvailabilityZone(TypedDict, total=False):
    """Information about an Availability Zone."""

    ZoneName: Optional[ZoneName]
    SubnetId: Optional[SubnetId]
    OutpostId: Optional[OutpostId]
    LoadBalancerAddresses: Optional[LoadBalancerAddresses]
    SourceNatIpv6Prefixes: Optional[SourceNatIpv6Prefixes]


AvailabilityZones = List[AvailabilityZone]


class CapacityReservationStatus(TypedDict, total=False):
    """The status of a capacity reservation."""

    Code: Optional[CapacityReservationStateEnum]
    Reason: Optional[StateReason]


class Cipher(TypedDict, total=False):
    """Information about a cipher used in a policy."""

    Name: Optional[CipherName]
    Priority: Optional[CipherPriority]


Ciphers = List[Cipher]


class MutualAuthenticationAttributes(TypedDict, total=False):
    """Information about the mutual authentication attributes of a listener."""

    Mode: Optional[Mode]
    TrustStoreArn: Optional[TrustStoreArn]
    IgnoreClientCertificateExpiry: Optional[IgnoreClientCertificateExpiry]
    TrustStoreAssociationStatus: Optional[TrustStoreAssociationStatusEnum]
    AdvertiseTrustStoreCaNames: Optional[AdvertiseTrustStoreCaNamesEnum]


class CreateListenerInput(ServiceRequest):
    LoadBalancerArn: LoadBalancerArn
    Protocol: Optional[ProtocolEnum]
    Port: Optional[Port]
    SslPolicy: Optional[SslPolicyName]
    Certificates: Optional[CertificateList]
    DefaultActions: Actions
    AlpnPolicy: Optional[AlpnPolicyName]
    Tags: Optional[TagList]
    MutualAuthentication: Optional[MutualAuthenticationAttributes]


class Listener(TypedDict, total=False):
    """Information about a listener."""

    ListenerArn: Optional[ListenerArn]
    LoadBalancerArn: Optional[LoadBalancerArn]
    Port: Optional[Port]
    Protocol: Optional[ProtocolEnum]
    Certificates: Optional[CertificateList]
    SslPolicy: Optional[SslPolicyName]
    DefaultActions: Optional[Actions]
    AlpnPolicy: Optional[AlpnPolicyName]
    MutualAuthentication: Optional[MutualAuthenticationAttributes]


Listeners = List[Listener]


class CreateListenerOutput(TypedDict, total=False):
    Listeners: Optional[Listeners]


class IpamPools(TypedDict, total=False):
    """An IPAM pool is a collection of IP address CIDRs. IPAM pools enable you
    to organize your IP addresses according to your routing and security
    needs.
    """

    Ipv4IpamPoolId: Optional[IpamPoolId]


SecurityGroups = List[SecurityGroupId]


class SubnetMapping(TypedDict, total=False):
    """Information about a subnet mapping."""

    SubnetId: Optional[SubnetId]
    AllocationId: Optional[AllocationId]
    PrivateIPv4Address: Optional[PrivateIPv4Address]
    IPv6Address: Optional[IPv6Address]
    SourceNatIpv6Prefix: Optional[SourceNatIpv6Prefix]


SubnetMappings = List[SubnetMapping]
Subnets = List[SubnetId]


class CreateLoadBalancerInput(ServiceRequest):
    Name: LoadBalancerName
    Subnets: Optional[Subnets]
    SubnetMappings: Optional[SubnetMappings]
    SecurityGroups: Optional[SecurityGroups]
    Scheme: Optional[LoadBalancerSchemeEnum]
    Tags: Optional[TagList]
    Type: Optional[LoadBalancerTypeEnum]
    IpAddressType: Optional[IpAddressType]
    CustomerOwnedIpv4Pool: Optional[CustomerOwnedIpv4Pool]
    EnablePrefixForIpv6SourceNat: Optional[EnablePrefixForIpv6SourceNatEnum]
    IpamPools: Optional[IpamPools]


class LoadBalancerState(TypedDict, total=False):
    """Information about the state of the load balancer."""

    Code: Optional[LoadBalancerStateEnum]
    Reason: Optional[StateReason]


CreatedTime = datetime


class LoadBalancer(TypedDict, total=False):
    """Information about a load balancer."""

    LoadBalancerArn: Optional[LoadBalancerArn]
    DNSName: Optional[DNSName]
    CanonicalHostedZoneId: Optional[CanonicalHostedZoneId]
    CreatedTime: Optional[CreatedTime]
    LoadBalancerName: Optional[LoadBalancerName]
    Scheme: Optional[LoadBalancerSchemeEnum]
    VpcId: Optional[VpcId]
    State: Optional[LoadBalancerState]
    Type: Optional[LoadBalancerTypeEnum]
    AvailabilityZones: Optional[AvailabilityZones]
    SecurityGroups: Optional[SecurityGroups]
    IpAddressType: Optional[IpAddressType]
    CustomerOwnedIpv4Pool: Optional[CustomerOwnedIpv4Pool]
    EnforceSecurityGroupInboundRulesOnPrivateLinkTraffic: Optional[
        EnforceSecurityGroupInboundRulesOnPrivateLinkTraffic
    ]
    EnablePrefixForIpv6SourceNat: Optional[EnablePrefixForIpv6SourceNatEnum]
    IpamPools: Optional[IpamPools]


LoadBalancers = List[LoadBalancer]


class CreateLoadBalancerOutput(TypedDict, total=False):
    LoadBalancers: Optional[LoadBalancers]


ListOfString = List[StringValue]


class SourceIpConditionConfig(TypedDict, total=False):
    """Information about a source IP condition.

    You can use this condition to route based on the IP address of the
    source that connects to the load balancer. If a client is behind a
    proxy, this is the IP address of the proxy not the IP address of the
    client.
    """

    Values: Optional[ListOfString]


class HttpRequestMethodConditionConfig(TypedDict, total=False):
    """Information about an HTTP method condition.

    HTTP defines a set of request methods, also referred to as HTTP verbs.
    For more information, see the `HTTP Method
    Registry <https://www.iana.org/assignments/http-methods/http-methods.xhtml>`__.
    You can also define custom HTTP methods.
    """

    Values: Optional[ListOfString]


class QueryStringKeyValuePair(TypedDict, total=False):
    """Information about a key/value pair."""

    Key: Optional[StringValue]
    Value: Optional[StringValue]


QueryStringKeyValuePairList = List[QueryStringKeyValuePair]


class QueryStringConditionConfig(TypedDict, total=False):
    """Information about a query string condition.

    The query string component of a URI starts after the first '?' character
    and is terminated by either a '#' character or the end of the URI. A
    typical query string contains key/value pairs separated by '&'
    characters. The allowed characters are specified by RFC 3986. Any
    character can be percentage encoded.
    """

    Values: Optional[QueryStringKeyValuePairList]


class HttpHeaderConditionConfig(TypedDict, total=False):
    """Information about an HTTP header condition.

    There is a set of standard HTTP header fields. You can also define
    custom HTTP header fields.
    """

    HttpHeaderName: Optional[HttpHeaderConditionName]
    Values: Optional[ListOfString]


class PathPatternConditionConfig(TypedDict, total=False):
    """Information about a path pattern condition."""

    Values: Optional[ListOfString]


class HostHeaderConditionConfig(TypedDict, total=False):
    """Information about a host header condition."""

    Values: Optional[ListOfString]


class RuleCondition(TypedDict, total=False):
    """Information about a condition for a rule.

    Each rule can optionally include up to one of each of the following
    conditions: ``http-request-method``, ``host-header``, ``path-pattern``,
    and ``source-ip``. Each rule can also optionally include one or more of
    each of the following conditions: ``http-header`` and ``query-string``.
    Note that the value for a condition can't be empty.

    For more information, see `Quotas for your Application Load
    Balancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-limits.html>`__.
    """

    Field: Optional[ConditionFieldName]
    Values: Optional[ListOfString]
    HostHeaderConfig: Optional[HostHeaderConditionConfig]
    PathPatternConfig: Optional[PathPatternConditionConfig]
    HttpHeaderConfig: Optional[HttpHeaderConditionConfig]
    QueryStringConfig: Optional[QueryStringConditionConfig]
    HttpRequestMethodConfig: Optional[HttpRequestMethodConditionConfig]
    SourceIpConfig: Optional[SourceIpConditionConfig]


RuleConditionList = List[RuleCondition]


class CreateRuleInput(ServiceRequest):
    ListenerArn: ListenerArn
    Conditions: RuleConditionList
    Priority: RulePriority
    Actions: Actions
    Tags: Optional[TagList]


class Rule(TypedDict, total=False):
    """Information about a rule."""

    RuleArn: Optional[RuleArn]
    Priority: Optional[String]
    Conditions: Optional[RuleConditionList]
    Actions: Optional[Actions]
    IsDefault: Optional[IsDefault]


Rules = List[Rule]


class CreateRuleOutput(TypedDict, total=False):
    Rules: Optional[Rules]


class Matcher(TypedDict, total=False):
    """The codes to use when checking for a successful response from a target.
    If the protocol version is gRPC, these are gRPC codes. Otherwise, these
    are HTTP codes.
    """

    HttpCode: Optional[HttpCode]
    GrpcCode: Optional[GrpcCode]


class CreateTargetGroupInput(ServiceRequest):
    Name: TargetGroupName
    Protocol: Optional[ProtocolEnum]
    ProtocolVersion: Optional[ProtocolVersion]
    Port: Optional[Port]
    VpcId: Optional[VpcId]
    HealthCheckProtocol: Optional[ProtocolEnum]
    HealthCheckPort: Optional[HealthCheckPort]
    HealthCheckEnabled: Optional[HealthCheckEnabled]
    HealthCheckPath: Optional[Path]
    HealthCheckIntervalSeconds: Optional[HealthCheckIntervalSeconds]
    HealthCheckTimeoutSeconds: Optional[HealthCheckTimeoutSeconds]
    HealthyThresholdCount: Optional[HealthCheckThresholdCount]
    UnhealthyThresholdCount: Optional[HealthCheckThresholdCount]
    Matcher: Optional[Matcher]
    TargetType: Optional[TargetTypeEnum]
    Tags: Optional[TagList]
    IpAddressType: Optional[TargetGroupIpAddressTypeEnum]


LoadBalancerArns = List[LoadBalancerArn]


class TargetGroup(TypedDict, total=False):
    """Information about a target group."""

    TargetGroupArn: Optional[TargetGroupArn]
    TargetGroupName: Optional[TargetGroupName]
    Protocol: Optional[ProtocolEnum]
    Port: Optional[Port]
    VpcId: Optional[VpcId]
    HealthCheckProtocol: Optional[ProtocolEnum]
    HealthCheckPort: Optional[HealthCheckPort]
    HealthCheckEnabled: Optional[HealthCheckEnabled]
    HealthCheckIntervalSeconds: Optional[HealthCheckIntervalSeconds]
    HealthCheckTimeoutSeconds: Optional[HealthCheckTimeoutSeconds]
    HealthyThresholdCount: Optional[HealthCheckThresholdCount]
    UnhealthyThresholdCount: Optional[HealthCheckThresholdCount]
    HealthCheckPath: Optional[Path]
    Matcher: Optional[Matcher]
    LoadBalancerArns: Optional[LoadBalancerArns]
    TargetType: Optional[TargetTypeEnum]
    ProtocolVersion: Optional[ProtocolVersion]
    IpAddressType: Optional[TargetGroupIpAddressTypeEnum]


TargetGroups = List[TargetGroup]


class CreateTargetGroupOutput(TypedDict, total=False):
    TargetGroups: Optional[TargetGroups]


class CreateTrustStoreInput(ServiceRequest):
    Name: TrustStoreName
    CaCertificatesBundleS3Bucket: S3Bucket
    CaCertificatesBundleS3Key: S3Key
    CaCertificatesBundleS3ObjectVersion: Optional[S3ObjectVersion]
    Tags: Optional[TagList]


TotalRevokedEntries = int


class TrustStore(TypedDict, total=False):
    """Information about a trust store."""

    Name: Optional[TrustStoreName]
    TrustStoreArn: Optional[TrustStoreArn]
    Status: Optional[TrustStoreStatus]
    NumberOfCaCertificates: Optional[NumberOfCaCertificates]
    TotalRevokedEntries: Optional[TotalRevokedEntries]


TrustStores = List[TrustStore]


class CreateTrustStoreOutput(TypedDict, total=False):
    TrustStores: Optional[TrustStores]


class DeleteListenerInput(ServiceRequest):
    ListenerArn: ListenerArn


class DeleteListenerOutput(TypedDict, total=False):
    pass


class DeleteLoadBalancerInput(ServiceRequest):
    LoadBalancerArn: LoadBalancerArn


class DeleteLoadBalancerOutput(TypedDict, total=False):
    pass


class DeleteRuleInput(ServiceRequest):
    RuleArn: RuleArn


class DeleteRuleOutput(TypedDict, total=False):
    pass


class DeleteSharedTrustStoreAssociationInput(ServiceRequest):
    TrustStoreArn: TrustStoreArn
    ResourceArn: ResourceArn


class DeleteSharedTrustStoreAssociationOutput(TypedDict, total=False):
    pass


class DeleteTargetGroupInput(ServiceRequest):
    TargetGroupArn: TargetGroupArn


class DeleteTargetGroupOutput(TypedDict, total=False):
    pass


class DeleteTrustStoreInput(ServiceRequest):
    TrustStoreArn: TrustStoreArn


class DeleteTrustStoreOutput(TypedDict, total=False):
    pass


class TargetDescription(TypedDict, total=False):
    """Information about a target."""

    Id: TargetId
    Port: Optional[Port]
    AvailabilityZone: Optional[ZoneName]


TargetDescriptions = List[TargetDescription]


class DeregisterTargetsInput(ServiceRequest):
    TargetGroupArn: TargetGroupArn
    Targets: TargetDescriptions


class DeregisterTargetsOutput(TypedDict, total=False):
    pass


class DescribeAccountLimitsInput(ServiceRequest):
    Marker: Optional[Marker]
    PageSize: Optional[PageSize]


class Limit(TypedDict, total=False):
    """Information about an Elastic Load Balancing resource limit for your
    Amazon Web Services account.

    For more information, see the following:

    -  `Quotas for your Application Load
       Balancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-limits.html>`__

    -  `Quotas for your Network Load
       Balancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-limits.html>`__

    -  `Quotas for your Gateway Load
       Balancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/quotas-limits.html>`__
    """

    Name: Optional[Name]
    Max: Optional[Max]


Limits = List[Limit]


class DescribeAccountLimitsOutput(TypedDict, total=False):
    Limits: Optional[Limits]
    NextMarker: Optional[Marker]


class DescribeCapacityReservationInput(ServiceRequest):
    LoadBalancerArn: LoadBalancerArn


class ZonalCapacityReservationState(TypedDict, total=False):
    """The capacity reservation status for each availability zone."""

    State: Optional[CapacityReservationStatus]
    AvailabilityZone: Optional[ZoneName]
    EffectiveCapacityUnits: Optional[CapacityUnitsDouble]


ZonalCapacityReservationStates = List[ZonalCapacityReservationState]


class MinimumLoadBalancerCapacity(TypedDict, total=False):
    """The minimum capacity for a load balancer."""

    CapacityUnits: Optional[CapacityUnits]


LastModifiedTime = datetime


class DescribeCapacityReservationOutput(TypedDict, total=False):
    LastModifiedTime: Optional[LastModifiedTime]
    DecreaseRequestsRemaining: Optional[DecreaseRequestsRemaining]
    MinimumLoadBalancerCapacity: Optional[MinimumLoadBalancerCapacity]
    CapacityReservationState: Optional[ZonalCapacityReservationStates]


class DescribeListenerAttributesInput(ServiceRequest):
    ListenerArn: ListenerArn


class ListenerAttribute(TypedDict, total=False):
    """Information about a listener attribute."""

    Key: Optional[ListenerAttributeKey]
    Value: Optional[ListenerAttributeValue]


ListenerAttributes = List[ListenerAttribute]


class DescribeListenerAttributesOutput(TypedDict, total=False):
    Attributes: Optional[ListenerAttributes]


class DescribeListenerCertificatesInput(ServiceRequest):
    ListenerArn: ListenerArn
    Marker: Optional[Marker]
    PageSize: Optional[PageSize]


class DescribeListenerCertificatesOutput(TypedDict, total=False):
    Certificates: Optional[CertificateList]
    NextMarker: Optional[Marker]


ListenerArns = List[ListenerArn]


class DescribeListenersInput(ServiceRequest):
    LoadBalancerArn: Optional[LoadBalancerArn]
    ListenerArns: Optional[ListenerArns]
    Marker: Optional[Marker]
    PageSize: Optional[PageSize]


class DescribeListenersOutput(TypedDict, total=False):
    Listeners: Optional[Listeners]
    NextMarker: Optional[Marker]


class DescribeLoadBalancerAttributesInput(ServiceRequest):
    LoadBalancerArn: LoadBalancerArn


class LoadBalancerAttribute(TypedDict, total=False):
    """Information about a load balancer attribute."""

    Key: Optional[LoadBalancerAttributeKey]
    Value: Optional[LoadBalancerAttributeValue]


LoadBalancerAttributes = List[LoadBalancerAttribute]


class DescribeLoadBalancerAttributesOutput(TypedDict, total=False):
    Attributes: Optional[LoadBalancerAttributes]


LoadBalancerNames = List[LoadBalancerName]


class DescribeLoadBalancersInput(ServiceRequest):
    LoadBalancerArns: Optional[LoadBalancerArns]
    Names: Optional[LoadBalancerNames]
    Marker: Optional[Marker]
    PageSize: Optional[PageSize]


class DescribeLoadBalancersOutput(TypedDict, total=False):
    LoadBalancers: Optional[LoadBalancers]
    NextMarker: Optional[Marker]


RuleArns = List[RuleArn]


class DescribeRulesInput(ServiceRequest):
    ListenerArn: Optional[ListenerArn]
    RuleArns: Optional[RuleArns]
    Marker: Optional[Marker]
    PageSize: Optional[PageSize]


class DescribeRulesOutput(TypedDict, total=False):
    Rules: Optional[Rules]
    NextMarker: Optional[Marker]


SslPolicyNames = List[SslPolicyName]


class DescribeSSLPoliciesInput(ServiceRequest):
    Names: Optional[SslPolicyNames]
    Marker: Optional[Marker]
    PageSize: Optional[PageSize]
    LoadBalancerType: Optional[LoadBalancerTypeEnum]


SslProtocols = List[SslProtocol]


class SslPolicy(TypedDict, total=False):
    """Information about a policy used for SSL negotiation."""

    SslProtocols: Optional[SslProtocols]
    Ciphers: Optional[Ciphers]
    Name: Optional[SslPolicyName]
    SupportedLoadBalancerTypes: Optional[ListOfString]


SslPolicies = List[SslPolicy]


class DescribeSSLPoliciesOutput(TypedDict, total=False):
    SslPolicies: Optional[SslPolicies]
    NextMarker: Optional[Marker]


class DescribeTagsInput(ServiceRequest):
    ResourceArns: ResourceArns


class TagDescription(TypedDict, total=False):
    """The tags associated with a resource."""

    ResourceArn: Optional[ResourceArn]
    Tags: Optional[TagList]


TagDescriptions = List[TagDescription]


class DescribeTagsOutput(TypedDict, total=False):
    TagDescriptions: Optional[TagDescriptions]


class DescribeTargetGroupAttributesInput(ServiceRequest):
    TargetGroupArn: TargetGroupArn


class TargetGroupAttribute(TypedDict, total=False):
    """Information about a target group attribute."""

    Key: Optional[TargetGroupAttributeKey]
    Value: Optional[TargetGroupAttributeValue]


TargetGroupAttributes = List[TargetGroupAttribute]


class DescribeTargetGroupAttributesOutput(TypedDict, total=False):
    Attributes: Optional[TargetGroupAttributes]


TargetGroupNames = List[TargetGroupName]
TargetGroupArns = List[TargetGroupArn]


class DescribeTargetGroupsInput(ServiceRequest):
    LoadBalancerArn: Optional[LoadBalancerArn]
    TargetGroupArns: Optional[TargetGroupArns]
    Names: Optional[TargetGroupNames]
    Marker: Optional[Marker]
    PageSize: Optional[PageSize]


class DescribeTargetGroupsOutput(TypedDict, total=False):
    TargetGroups: Optional[TargetGroups]
    NextMarker: Optional[Marker]


ListOfDescribeTargetHealthIncludeOptions = List[DescribeTargetHealthInputIncludeEnum]


class DescribeTargetHealthInput(ServiceRequest):
    TargetGroupArn: TargetGroupArn
    Targets: Optional[TargetDescriptions]
    Include: Optional[ListOfDescribeTargetHealthIncludeOptions]


class TargetHealth(TypedDict, total=False):
    """Information about the current health of a target."""

    State: Optional[TargetHealthStateEnum]
    Reason: Optional[TargetHealthReasonEnum]
    Description: Optional[Description]


class TargetHealthDescription(TypedDict, total=False):
    """Information about the health of a target."""

    Target: Optional[TargetDescription]
    HealthCheckPort: Optional[HealthCheckPort]
    TargetHealth: Optional[TargetHealth]
    AnomalyDetection: Optional[AnomalyDetection]
    AdministrativeOverride: Optional[AdministrativeOverride]


TargetHealthDescriptions = List[TargetHealthDescription]


class DescribeTargetHealthOutput(TypedDict, total=False):
    TargetHealthDescriptions: Optional[TargetHealthDescriptions]


class DescribeTrustStoreAssociationsInput(ServiceRequest):
    TrustStoreArn: TrustStoreArn
    Marker: Optional[Marker]
    PageSize: Optional[PageSize]


class TrustStoreAssociation(TypedDict, total=False):
    """Information about the resources a trust store is associated with."""

    ResourceArn: Optional[TrustStoreAssociationResourceArn]


TrustStoreAssociations = List[TrustStoreAssociation]


class DescribeTrustStoreAssociationsOutput(TypedDict, total=False):
    TrustStoreAssociations: Optional[TrustStoreAssociations]
    NextMarker: Optional[Marker]


class DescribeTrustStoreRevocation(TypedDict, total=False):
    """Information about the revocations used by a trust store."""

    TrustStoreArn: Optional[TrustStoreArn]
    RevocationId: Optional[RevocationId]
    RevocationType: Optional[RevocationType]
    NumberOfRevokedEntries: Optional[NumberOfRevokedEntries]


DescribeTrustStoreRevocationResponse = List[DescribeTrustStoreRevocation]
RevocationIds = List[RevocationId]


class DescribeTrustStoreRevocationsInput(ServiceRequest):
    TrustStoreArn: TrustStoreArn
    RevocationIds: Optional[RevocationIds]
    Marker: Optional[Marker]
    PageSize: Optional[PageSize]


class DescribeTrustStoreRevocationsOutput(TypedDict, total=False):
    TrustStoreRevocations: Optional[DescribeTrustStoreRevocationResponse]
    NextMarker: Optional[Marker]


TrustStoreNames = List[TrustStoreName]
TrustStoreArns = List[TrustStoreArn]


class DescribeTrustStoresInput(ServiceRequest):
    TrustStoreArns: Optional[TrustStoreArns]
    Names: Optional[TrustStoreNames]
    Marker: Optional[Marker]
    PageSize: Optional[PageSize]


class DescribeTrustStoresOutput(TypedDict, total=False):
    TrustStores: Optional[TrustStores]
    NextMarker: Optional[Marker]


class GetResourcePolicyInput(ServiceRequest):
    ResourceArn: ResourceArn


class GetResourcePolicyOutput(TypedDict, total=False):
    Policy: Optional[Policy]


class GetTrustStoreCaCertificatesBundleInput(ServiceRequest):
    TrustStoreArn: TrustStoreArn


class GetTrustStoreCaCertificatesBundleOutput(TypedDict, total=False):
    Location: Optional[Location]


class GetTrustStoreRevocationContentInput(ServiceRequest):
    TrustStoreArn: TrustStoreArn
    RevocationId: RevocationId


class GetTrustStoreRevocationContentOutput(TypedDict, total=False):
    Location: Optional[Location]


class ModifyCapacityReservationInput(ServiceRequest):
    LoadBalancerArn: LoadBalancerArn
    MinimumLoadBalancerCapacity: Optional[MinimumLoadBalancerCapacity]
    ResetCapacityReservation: Optional[ResetCapacityReservation]


class ModifyCapacityReservationOutput(TypedDict, total=False):
    LastModifiedTime: Optional[LastModifiedTime]
    DecreaseRequestsRemaining: Optional[DecreaseRequestsRemaining]
    MinimumLoadBalancerCapacity: Optional[MinimumLoadBalancerCapacity]
    CapacityReservationState: Optional[ZonalCapacityReservationStates]


RemoveIpamPools = List[RemoveIpamPoolEnum]


class ModifyIpPoolsInput(ServiceRequest):
    LoadBalancerArn: LoadBalancerArn
    IpamPools: Optional[IpamPools]
    RemoveIpamPools: Optional[RemoveIpamPools]


class ModifyIpPoolsOutput(TypedDict, total=False):
    IpamPools: Optional[IpamPools]


class ModifyListenerAttributesInput(ServiceRequest):
    ListenerArn: ListenerArn
    Attributes: ListenerAttributes


class ModifyListenerAttributesOutput(TypedDict, total=False):
    Attributes: Optional[ListenerAttributes]


class ModifyListenerInput(ServiceRequest):
    ListenerArn: ListenerArn
    Port: Optional[Port]
    Protocol: Optional[ProtocolEnum]
    SslPolicy: Optional[SslPolicyName]
    Certificates: Optional[CertificateList]
    DefaultActions: Optional[Actions]
    AlpnPolicy: Optional[AlpnPolicyName]
    MutualAuthentication: Optional[MutualAuthenticationAttributes]


class ModifyListenerOutput(TypedDict, total=False):
    Listeners: Optional[Listeners]


class ModifyLoadBalancerAttributesInput(ServiceRequest):
    LoadBalancerArn: LoadBalancerArn
    Attributes: LoadBalancerAttributes


class ModifyLoadBalancerAttributesOutput(TypedDict, total=False):
    Attributes: Optional[LoadBalancerAttributes]


class ModifyRuleInput(ServiceRequest):
    RuleArn: RuleArn
    Conditions: Optional[RuleConditionList]
    Actions: Optional[Actions]


class ModifyRuleOutput(TypedDict, total=False):
    Rules: Optional[Rules]


class ModifyTargetGroupAttributesInput(ServiceRequest):
    TargetGroupArn: TargetGroupArn
    Attributes: TargetGroupAttributes


class ModifyTargetGroupAttributesOutput(TypedDict, total=False):
    Attributes: Optional[TargetGroupAttributes]


class ModifyTargetGroupInput(ServiceRequest):
    TargetGroupArn: TargetGroupArn
    HealthCheckProtocol: Optional[ProtocolEnum]
    HealthCheckPort: Optional[HealthCheckPort]
    HealthCheckPath: Optional[Path]
    HealthCheckEnabled: Optional[HealthCheckEnabled]
    HealthCheckIntervalSeconds: Optional[HealthCheckIntervalSeconds]
    HealthCheckTimeoutSeconds: Optional[HealthCheckTimeoutSeconds]
    HealthyThresholdCount: Optional[HealthCheckThresholdCount]
    UnhealthyThresholdCount: Optional[HealthCheckThresholdCount]
    Matcher: Optional[Matcher]


class ModifyTargetGroupOutput(TypedDict, total=False):
    TargetGroups: Optional[TargetGroups]


class ModifyTrustStoreInput(ServiceRequest):
    TrustStoreArn: TrustStoreArn
    CaCertificatesBundleS3Bucket: S3Bucket
    CaCertificatesBundleS3Key: S3Key
    CaCertificatesBundleS3ObjectVersion: Optional[S3ObjectVersion]


class ModifyTrustStoreOutput(TypedDict, total=False):
    TrustStores: Optional[TrustStores]


class RegisterTargetsInput(ServiceRequest):
    TargetGroupArn: TargetGroupArn
    Targets: TargetDescriptions


class RegisterTargetsOutput(TypedDict, total=False):
    pass


class RemoveListenerCertificatesInput(ServiceRequest):
    ListenerArn: ListenerArn
    Certificates: CertificateList


class RemoveListenerCertificatesOutput(TypedDict, total=False):
    pass


TagKeys = List[TagKey]


class RemoveTagsInput(ServiceRequest):
    ResourceArns: ResourceArns
    TagKeys: TagKeys


class RemoveTagsOutput(TypedDict, total=False):
    pass


class RemoveTrustStoreRevocationsInput(ServiceRequest):
    TrustStoreArn: TrustStoreArn
    RevocationIds: RevocationIds


class RemoveTrustStoreRevocationsOutput(TypedDict, total=False):
    pass


class RulePriorityPair(TypedDict, total=False):
    """Information about the priorities for the rules for a listener."""

    RuleArn: Optional[RuleArn]
    Priority: Optional[RulePriority]


RulePriorityList = List[RulePriorityPair]


class SetIpAddressTypeInput(ServiceRequest):
    LoadBalancerArn: LoadBalancerArn
    IpAddressType: IpAddressType


class SetIpAddressTypeOutput(TypedDict, total=False):
    IpAddressType: Optional[IpAddressType]


class SetRulePrioritiesInput(ServiceRequest):
    RulePriorities: RulePriorityList


class SetRulePrioritiesOutput(TypedDict, total=False):
    Rules: Optional[Rules]


class SetSecurityGroupsInput(ServiceRequest):
    LoadBalancerArn: LoadBalancerArn
    SecurityGroups: SecurityGroups
    EnforceSecurityGroupInboundRulesOnPrivateLinkTraffic: Optional[
        EnforceSecurityGroupInboundRulesOnPrivateLinkTrafficEnum
    ]


class SetSecurityGroupsOutput(TypedDict, total=False):
    SecurityGroupIds: Optional[SecurityGroups]
    EnforceSecurityGroupInboundRulesOnPrivateLinkTraffic: Optional[
        EnforceSecurityGroupInboundRulesOnPrivateLinkTrafficEnum
    ]


class SetSubnetsInput(ServiceRequest):
    LoadBalancerArn: LoadBalancerArn
    Subnets: Optional[Subnets]
    SubnetMappings: Optional[SubnetMappings]
    IpAddressType: Optional[IpAddressType]
    EnablePrefixForIpv6SourceNat: Optional[EnablePrefixForIpv6SourceNatEnum]


class SetSubnetsOutput(TypedDict, total=False):
    AvailabilityZones: Optional[AvailabilityZones]
    IpAddressType: Optional[IpAddressType]
    EnablePrefixForIpv6SourceNat: Optional[EnablePrefixForIpv6SourceNatEnum]


class Elbv2Api:
    service = "elbv2"
    version = "2015-12-01"

    @handler("AddListenerCertificates")
    def add_listener_certificates(
        self,
        context: RequestContext,
        listener_arn: ListenerArn,
        certificates: CertificateList,
        **kwargs,
    ) -> AddListenerCertificatesOutput:
        """Adds the specified SSL server certificate to the certificate list for
        the specified HTTPS or TLS listener.

        If the certificate in already in the certificate list, the call is
        successful but the certificate is not added again.

        For more information, see `HTTPS
        listeners <https://docs.aws.amazon.com/elasticloadbalancing/latest/application/create-https-listener.html>`__
        in the *Application Load Balancers Guide* or `TLS
        listeners <https://docs.aws.amazon.com/elasticloadbalancing/latest/network/create-tls-listener.html>`__
        in the *Network Load Balancers Guide*.

        :param listener_arn: The Amazon Resource Name (ARN) of the listener.
        :param certificates: The certificate to add.
        :returns: AddListenerCertificatesOutput
        :raises ListenerNotFoundException:
        :raises TooManyCertificatesException:
        :raises CertificateNotFoundException:
        """
        raise NotImplementedError

    @handler("AddTags")
    def add_tags(
        self, context: RequestContext, resource_arns: ResourceArns, tags: TagList, **kwargs
    ) -> AddTagsOutput:
        """Adds the specified tags to the specified Elastic Load Balancing
        resource. You can tag your Application Load Balancers, Network Load
        Balancers, Gateway Load Balancers, target groups, trust stores,
        listeners, and rules.

        Each tag consists of a key and an optional value. If a resource already
        has a tag with the same key, ``AddTags`` updates its value.

        :param resource_arns: The Amazon Resource Name (ARN) of the resource.
        :param tags: The tags.
        :returns: AddTagsOutput
        :raises DuplicateTagKeysException:
        :raises TooManyTagsException:
        :raises LoadBalancerNotFoundException:
        :raises TargetGroupNotFoundException:
        :raises ListenerNotFoundException:
        :raises RuleNotFoundException:
        :raises TrustStoreNotFoundException:
        """
        raise NotImplementedError

    @handler("AddTrustStoreRevocations")
    def add_trust_store_revocations(
        self,
        context: RequestContext,
        trust_store_arn: TrustStoreArn,
        revocation_contents: RevocationContents = None,
        **kwargs,
    ) -> AddTrustStoreRevocationsOutput:
        """Adds the specified revocation file to the specified trust store.

        :param trust_store_arn: The Amazon Resource Name (ARN) of the trust store.
        :param revocation_contents: The revocation file to add.
        :returns: AddTrustStoreRevocationsOutput
        :raises TrustStoreNotFoundException:
        :raises InvalidRevocationContentException:
        :raises TooManyTrustStoreRevocationEntriesException:
        :raises RevocationContentNotFoundException:
        """
        raise NotImplementedError

    @handler("CreateListener")
    def create_listener(
        self,
        context: RequestContext,
        load_balancer_arn: LoadBalancerArn,
        default_actions: Actions,
        protocol: ProtocolEnum = None,
        port: Port = None,
        ssl_policy: SslPolicyName = None,
        certificates: CertificateList = None,
        alpn_policy: AlpnPolicyName = None,
        tags: TagList = None,
        mutual_authentication: MutualAuthenticationAttributes = None,
        **kwargs,
    ) -> CreateListenerOutput:
        """Creates a listener for the specified Application Load Balancer, Network
        Load Balancer, or Gateway Load Balancer.

        For more information, see the following:

        -  `Listeners for your Application Load
           Balancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html>`__

        -  `Listeners for your Network Load
           Balancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-listeners.html>`__

        -  `Listeners for your Gateway Load
           Balancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/gateway-listeners.html>`__

        This operation is idempotent, which means that it completes at most one
        time. If you attempt to create multiple listeners with the same
        settings, each call succeeds.

        :param load_balancer_arn: The Amazon Resource Name (ARN) of the load balancer.
        :param default_actions: The actions for the default rule.
        :param protocol: The protocol for connections from clients to the load balancer.
        :param port: The port on which the load balancer is listening.
        :param ssl_policy: [HTTPS and TLS listeners] The security policy that defines which
        protocols and ciphers are supported.
        :param certificates: [HTTPS and TLS listeners] The default certificate for the listener.
        :param alpn_policy: [TLS listeners] The name of the Application-Layer Protocol Negotiation
        (ALPN) policy.
        :param tags: The tags to assign to the listener.
        :param mutual_authentication: The mutual authentication configuration information.
        :returns: CreateListenerOutput
        :raises DuplicateListenerException:
        :raises TooManyListenersException:
        :raises TooManyCertificatesException:
        :raises LoadBalancerNotFoundException:
        :raises TargetGroupNotFoundException:
        :raises TargetGroupAssociationLimitException:
        :raises InvalidConfigurationRequestException:
        :raises IncompatibleProtocolsException:
        :raises SSLPolicyNotFoundException:
        :raises CertificateNotFoundException:
        :raises UnsupportedProtocolException:
        :raises TooManyRegistrationsForTargetIdException:
        :raises TooManyTargetsException:
        :raises TooManyActionsException:
        :raises InvalidLoadBalancerActionException:
        :raises TooManyUniqueTargetGroupsPerLoadBalancerException:
        :raises ALPNPolicyNotSupportedException:
        :raises TooManyTagsException:
        :raises TrustStoreNotFoundException:
        :raises TrustStoreNotReadyException:
        """
        raise NotImplementedError

    @handler("CreateLoadBalancer", expand=False)
    def create_load_balancer(
        self, context: RequestContext, request: CreateLoadBalancerInput, **kwargs
    ) -> CreateLoadBalancerOutput:
        """Creates an Application Load Balancer, Network Load Balancer, or Gateway
        Load Balancer.

        For more information, see the following:

        -  `Application Load
           Balancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html>`__

        -  `Network Load
           Balancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/network/network-load-balancers.html>`__

        -  `Gateway Load
           Balancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/gateway-load-balancers.html>`__

        This operation is idempotent, which means that it completes at most one
        time. If you attempt to create multiple load balancers with the same
        settings, each call succeeds.

        :param name: The name of the load balancer.
        :param subnets: The IDs of the subnets.
        :param subnet_mappings: The IDs of the subnets.
        :param security_groups: [Application Load Balancers and Network Load Balancers] The IDs of the
        security groups for the load balancer.
        :param scheme: The nodes of an Internet-facing load balancer have public IP addresses.
        :param tags: The tags to assign to the load balancer.
        :param type: The type of load balancer.
        :param ip_address_type: The IP address type.
        :param customer_owned_ipv4_pool: [Application Load Balancers on Outposts] The ID of the customer-owned
        address pool (CoIP pool).
        :param enable_prefix_for_ipv6_source_nat: [Network Load Balancers with UDP listeners] Indicates whether to use an
        IPv6 prefix from each subnet for source NAT.
        :param ipam_pools: [Application Load Balancers] The IPAM pools to use with the load
        balancer.
        :returns: CreateLoadBalancerOutput
        :raises DuplicateLoadBalancerNameException:
        :raises TooManyLoadBalancersException:
        :raises InvalidConfigurationRequestException:
        :raises SubnetNotFoundException:
        :raises InvalidSubnetException:
        :raises InvalidSecurityGroupException:
        :raises InvalidSchemeException:
        :raises TooManyTagsException:
        :raises DuplicateTagKeysException:
        :raises ResourceInUseException:
        :raises AllocationIdNotFoundException:
        :raises AvailabilityZoneNotSupportedException:
        :raises OperationNotPermittedException:
        """
        raise NotImplementedError

    @handler("CreateRule")
    def create_rule(
        self,
        context: RequestContext,
        listener_arn: ListenerArn,
        conditions: RuleConditionList,
        priority: RulePriority,
        actions: Actions,
        tags: TagList = None,
        **kwargs,
    ) -> CreateRuleOutput:
        """Creates a rule for the specified listener. The listener must be
        associated with an Application Load Balancer.

        Each rule consists of a priority, one or more actions, and one or more
        conditions. Rules are evaluated in priority order, from the lowest value
        to the highest value. When the conditions for a rule are met, its
        actions are performed. If the conditions for no rules are met, the
        actions for the default rule are performed. For more information, see
        `Listener
        rules <https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#listener-rules>`__
        in the *Application Load Balancers Guide*.

        :param listener_arn: The Amazon Resource Name (ARN) of the listener.
        :param conditions: The conditions.
        :param priority: The rule priority.
        :param actions: The actions.
        :param tags: The tags to assign to the rule.
        :returns: CreateRuleOutput
        :raises PriorityInUseException:
        :raises TooManyTargetGroupsException:
        :raises TooManyRulesException:
        :raises TargetGroupAssociationLimitException:
        :raises IncompatibleProtocolsException:
        :raises ListenerNotFoundException:
        :raises TargetGroupNotFoundException:
        :raises InvalidConfigurationRequestException:
        :raises TooManyRegistrationsForTargetIdException:
        :raises TooManyTargetsException:
        :raises UnsupportedProtocolException:
        :raises TooManyActionsException:
        :raises InvalidLoadBalancerActionException:
        :raises TooManyUniqueTargetGroupsPerLoadBalancerException:
        :raises TooManyTagsException:
        """
        raise NotImplementedError

    @handler("CreateTargetGroup")
    def create_target_group(
        self,
        context: RequestContext,
        name: TargetGroupName,
        protocol: ProtocolEnum = None,
        protocol_version: ProtocolVersion = None,
        port: Port = None,
        vpc_id: VpcId = None,
        health_check_protocol: ProtocolEnum = None,
        health_check_port: HealthCheckPort = None,
        health_check_enabled: HealthCheckEnabled = None,
        health_check_path: Path = None,
        health_check_interval_seconds: HealthCheckIntervalSeconds = None,
        health_check_timeout_seconds: HealthCheckTimeoutSeconds = None,
        healthy_threshold_count: HealthCheckThresholdCount = None,
        unhealthy_threshold_count: HealthCheckThresholdCount = None,
        matcher: Matcher = None,
        target_type: TargetTypeEnum = None,
        tags: TagList = None,
        ip_address_type: TargetGroupIpAddressTypeEnum = None,
        **kwargs,
    ) -> CreateTargetGroupOutput:
        """Creates a target group.

        For more information, see the following:

        -  `Target groups for your Application Load
           Balancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-target-groups.html>`__

        -  `Target groups for your Network Load
           Balancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-target-groups.html>`__

        -  `Target groups for your Gateway Load
           Balancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/target-groups.html>`__

        This operation is idempotent, which means that it completes at most one
        time. If you attempt to create multiple target groups with the same
        settings, each call succeeds.

        :param name: The name of the target group.
        :param protocol: The protocol to use for routing traffic to the targets.
        :param protocol_version: [HTTP/HTTPS protocol] The protocol version.
        :param port: The port on which the targets receive traffic.
        :param vpc_id: The identifier of the virtual private cloud (VPC).
        :param health_check_protocol: The protocol the load balancer uses when performing health checks on
        targets.
        :param health_check_port: The port the load balancer uses when performing health checks on
        targets.
        :param health_check_enabled: Indicates whether health checks are enabled.
        :param health_check_path: [HTTP/HTTPS health checks] The destination for health checks on the
        targets.
        :param health_check_interval_seconds: The approximate amount of time, in seconds, between health checks of an
        individual target.
        :param health_check_timeout_seconds: The amount of time, in seconds, during which no response from a target
        means a failed health check.
        :param healthy_threshold_count: The number of consecutive health check successes required before
        considering a target healthy.
        :param unhealthy_threshold_count: The number of consecutive health check failures required before
        considering a target unhealthy.
        :param matcher: [HTTP/HTTPS health checks] The HTTP or gRPC codes to use when checking
        for a successful response from a target.
        :param target_type: The type of target that you must specify when registering targets with
        this target group.
        :param tags: The tags to assign to the target group.
        :param ip_address_type: The IP address type.
        :returns: CreateTargetGroupOutput
        :raises DuplicateTargetGroupNameException:
        :raises TooManyTargetGroupsException:
        :raises InvalidConfigurationRequestException:
        :raises TooManyTagsException:
        """
        raise NotImplementedError

    @handler("CreateTrustStore")
    def create_trust_store(
        self,
        context: RequestContext,
        name: TrustStoreName,
        ca_certificates_bundle_s3_bucket: S3Bucket,
        ca_certificates_bundle_s3_key: S3Key,
        ca_certificates_bundle_s3_object_version: S3ObjectVersion = None,
        tags: TagList = None,
        **kwargs,
    ) -> CreateTrustStoreOutput:
        """Creates a trust store.

        :param name: The name of the trust store.
        :param ca_certificates_bundle_s3_bucket: The Amazon S3 bucket for the ca certificates bundle.
        :param ca_certificates_bundle_s3_key: The Amazon S3 path for the ca certificates bundle.
        :param ca_certificates_bundle_s3_object_version: The Amazon S3 object version for the ca certificates bundle.
        :param tags: The tags to assign to the trust store.
        :returns: CreateTrustStoreOutput
        :raises DuplicateTrustStoreNameException:
        :raises TooManyTrustStoresException:
        :raises InvalidCaCertificatesBundleException:
        :raises CaCertificatesBundleNotFoundException:
        :raises TooManyTagsException:
        :raises DuplicateTagKeysException:
        """
        raise NotImplementedError

    @handler("DeleteListener")
    def delete_listener(
        self, context: RequestContext, listener_arn: ListenerArn, **kwargs
    ) -> DeleteListenerOutput:
        """Deletes the specified listener.

        Alternatively, your listener is deleted when you delete the load
        balancer to which it is attached.

        :param listener_arn: The Amazon Resource Name (ARN) of the listener.
        :returns: DeleteListenerOutput
        :raises ListenerNotFoundException:
        :raises ResourceInUseException:
        """
        raise NotImplementedError

    @handler("DeleteLoadBalancer")
    def delete_load_balancer(
        self, context: RequestContext, load_balancer_arn: LoadBalancerArn, **kwargs
    ) -> DeleteLoadBalancerOutput:
        """Deletes the specified Application Load Balancer, Network Load Balancer,
        or Gateway Load Balancer. Deleting a load balancer also deletes its
        listeners.

        You can't delete a load balancer if deletion protection is enabled. If
        the load balancer does not exist or has already been deleted, the call
        succeeds.

        Deleting a load balancer does not affect its registered targets. For
        example, your EC2 instances continue to run and are still registered to
        their target groups. If you no longer need these EC2 instances, you can
        stop or terminate them.

        :param load_balancer_arn: The Amazon Resource Name (ARN) of the load balancer.
        :returns: DeleteLoadBalancerOutput
        :raises LoadBalancerNotFoundException:
        :raises OperationNotPermittedException:
        :raises ResourceInUseException:
        """
        raise NotImplementedError

    @handler("DeleteRule")
    def delete_rule(self, context: RequestContext, rule_arn: RuleArn, **kwargs) -> DeleteRuleOutput:
        """Deletes the specified rule.

        You can't delete the default rule.

        :param rule_arn: The Amazon Resource Name (ARN) of the rule.
        :returns: DeleteRuleOutput
        :raises RuleNotFoundException:
        :raises OperationNotPermittedException:
        """
        raise NotImplementedError

    @handler("DeleteSharedTrustStoreAssociation")
    def delete_shared_trust_store_association(
        self,
        context: RequestContext,
        trust_store_arn: TrustStoreArn,
        resource_arn: ResourceArn,
        **kwargs,
    ) -> DeleteSharedTrustStoreAssociationOutput:
        """Deletes a shared trust store association.

        :param trust_store_arn: The Amazon Resource Name (ARN) of the trust store.
        :param resource_arn: The Amazon Resource Name (ARN) of the resource.
        :returns: DeleteSharedTrustStoreAssociationOutput
        :raises TrustStoreNotFoundException:
        :raises DeleteAssociationSameAccountException:
        :raises TrustStoreAssociationNotFoundException:
        """
        raise NotImplementedError

    @handler("DeleteTargetGroup")
    def delete_target_group(
        self, context: RequestContext, target_group_arn: TargetGroupArn, **kwargs
    ) -> DeleteTargetGroupOutput:
        """Deletes the specified target group.

        You can delete a target group if it is not referenced by any actions.
        Deleting a target group also deletes any associated health checks.
        Deleting a target group does not affect its registered targets. For
        example, any EC2 instances continue to run until you stop or terminate
        them.

        :param target_group_arn: The Amazon Resource Name (ARN) of the target group.
        :returns: DeleteTargetGroupOutput
        :raises ResourceInUseException:
        """
        raise NotImplementedError

    @handler("DeleteTrustStore")
    def delete_trust_store(
        self, context: RequestContext, trust_store_arn: TrustStoreArn, **kwargs
    ) -> DeleteTrustStoreOutput:
        """Deletes a trust store.

        :param trust_store_arn: The Amazon Resource Name (ARN) of the trust store.
        :returns: DeleteTrustStoreOutput
        :raises TrustStoreNotFoundException:
        :raises TrustStoreInUseException:
        """
        raise NotImplementedError

    @handler("DeregisterTargets")
    def deregister_targets(
        self,
        context: RequestContext,
        target_group_arn: TargetGroupArn,
        targets: TargetDescriptions,
        **kwargs,
    ) -> DeregisterTargetsOutput:
        """Deregisters the specified targets from the specified target group. After
        the targets are deregistered, they no longer receive traffic from the
        load balancer.

        The load balancer stops sending requests to targets that are
        deregistering, but uses connection draining to ensure that in-flight
        traffic completes on the existing connections. This deregistration delay
        is configured by default but can be updated for each target group.

        For more information, see the following:

        -  `Deregistration
           delay <https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-target-groups.html#deregistration-delay>`__
           in the *Application Load Balancers User Guide*

        -  `Deregistration
           delay <https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-target-groups.html#deregistration-delay>`__
           in the *Network Load Balancers User Guide*

        -  `Deregistration
           delay <https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/target-groups.html#deregistration-delay>`__
           in the *Gateway Load Balancers User Guide*

        Note: If the specified target does not exist, the action returns
        successfully.

        :param target_group_arn: The Amazon Resource Name (ARN) of the target group.
        :param targets: The targets.
        :returns: DeregisterTargetsOutput
        :raises TargetGroupNotFoundException:
        :raises InvalidTargetException:
        """
        raise NotImplementedError

    @handler("DescribeAccountLimits")
    def describe_account_limits(
        self, context: RequestContext, marker: Marker = None, page_size: PageSize = None, **kwargs
    ) -> DescribeAccountLimitsOutput:
        """Describes the current Elastic Load Balancing resource limits for your
        Amazon Web Services account.

        For more information, see the following:

        -  `Quotas for your Application Load
           Balancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-limits.html>`__

        -  `Quotas for your Network Load
           Balancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-limits.html>`__

        -  `Quotas for your Gateway Load
           Balancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/quotas-limits.html>`__

        :param marker: The marker for the next set of results.
        :param page_size: The maximum number of results to return with this call.
        :returns: DescribeAccountLimitsOutput
        """
        raise NotImplementedError

    @handler("DescribeCapacityReservation")
    def describe_capacity_reservation(
        self, context: RequestContext, load_balancer_arn: LoadBalancerArn, **kwargs
    ) -> DescribeCapacityReservationOutput:
        """Describes the capacity reservation status for the specified load
        balancer.

        :param load_balancer_arn: The Amazon Resource Name (ARN) of the load balancer.
        :returns: DescribeCapacityReservationOutput
        :raises LoadBalancerNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeListenerAttributes")
    def describe_listener_attributes(
        self, context: RequestContext, listener_arn: ListenerArn, **kwargs
    ) -> DescribeListenerAttributesOutput:
        """Describes the attributes for the specified listener.

        :param listener_arn: The Amazon Resource Name (ARN) of the listener.
        :returns: DescribeListenerAttributesOutput
        :raises ListenerNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeListenerCertificates")
    def describe_listener_certificates(
        self,
        context: RequestContext,
        listener_arn: ListenerArn,
        marker: Marker = None,
        page_size: PageSize = None,
        **kwargs,
    ) -> DescribeListenerCertificatesOutput:
        """Describes the default certificate and the certificate list for the
        specified HTTPS or TLS listener.

        If the default certificate is also in the certificate list, it appears
        twice in the results (once with ``IsDefault`` set to true and once with
        ``IsDefault`` set to false).

        For more information, see `SSL
        certificates <https://docs.aws.amazon.com/elasticloadbalancing/latest/application/create-https-listener.html#https-listener-certificates>`__
        in the *Application Load Balancers Guide* or `Server
        certificates <https://docs.aws.amazon.com/elasticloadbalancing/latest/network/create-tls-listener.html#tls-listener-certificate>`__
        in the *Network Load Balancers Guide*.

        :param listener_arn: The Amazon Resource Names (ARN) of the listener.
        :param marker: The marker for the next set of results.
        :param page_size: The maximum number of results to return with this call.
        :returns: DescribeListenerCertificatesOutput
        :raises ListenerNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeListeners")
    def describe_listeners(
        self,
        context: RequestContext,
        load_balancer_arn: LoadBalancerArn = None,
        listener_arns: ListenerArns = None,
        marker: Marker = None,
        page_size: PageSize = None,
        **kwargs,
    ) -> DescribeListenersOutput:
        """Describes the specified listeners or the listeners for the specified
        Application Load Balancer, Network Load Balancer, or Gateway Load
        Balancer. You must specify either a load balancer or one or more
        listeners.

        :param load_balancer_arn: The Amazon Resource Name (ARN) of the load balancer.
        :param listener_arns: The Amazon Resource Names (ARN) of the listeners.
        :param marker: The marker for the next set of results.
        :param page_size: The maximum number of results to return with this call.
        :returns: DescribeListenersOutput
        :raises ListenerNotFoundException:
        :raises LoadBalancerNotFoundException:
        :raises UnsupportedProtocolException:
        """
        raise NotImplementedError

    @handler("DescribeLoadBalancerAttributes")
    def describe_load_balancer_attributes(
        self, context: RequestContext, load_balancer_arn: LoadBalancerArn, **kwargs
    ) -> DescribeLoadBalancerAttributesOutput:
        """Describes the attributes for the specified Application Load Balancer,
        Network Load Balancer, or Gateway Load Balancer.

        For more information, see the following:

        -  `Load balancer
           attributes <https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html#load-balancer-attributes>`__
           in the *Application Load Balancers Guide*

        -  `Load balancer
           attributes <https://docs.aws.amazon.com/elasticloadbalancing/latest/network/network-load-balancers.html#load-balancer-attributes>`__
           in the *Network Load Balancers Guide*

        -  `Load balancer
           attributes <https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/gateway-load-balancers.html#load-balancer-attributes>`__
           in the *Gateway Load Balancers Guide*

        :param load_balancer_arn: The Amazon Resource Name (ARN) of the load balancer.
        :returns: DescribeLoadBalancerAttributesOutput
        :raises LoadBalancerNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeLoadBalancers")
    def describe_load_balancers(
        self,
        context: RequestContext,
        load_balancer_arns: LoadBalancerArns = None,
        names: LoadBalancerNames = None,
        marker: Marker = None,
        page_size: PageSize = None,
        **kwargs,
    ) -> DescribeLoadBalancersOutput:
        """Describes the specified load balancers or all of your load balancers.

        :param load_balancer_arns: The Amazon Resource Names (ARN) of the load balancers.
        :param names: The names of the load balancers.
        :param marker: The marker for the next set of results.
        :param page_size: The maximum number of results to return with this call.
        :returns: DescribeLoadBalancersOutput
        :raises LoadBalancerNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeRules")
    def describe_rules(
        self,
        context: RequestContext,
        listener_arn: ListenerArn = None,
        rule_arns: RuleArns = None,
        marker: Marker = None,
        page_size: PageSize = None,
        **kwargs,
    ) -> DescribeRulesOutput:
        """Describes the specified rules or the rules for the specified listener.
        You must specify either a listener or one or more rules.

        :param listener_arn: The Amazon Resource Name (ARN) of the listener.
        :param rule_arns: The Amazon Resource Names (ARN) of the rules.
        :param marker: The marker for the next set of results.
        :param page_size: The maximum number of results to return with this call.
        :returns: DescribeRulesOutput
        :raises ListenerNotFoundException:
        :raises RuleNotFoundException:
        :raises UnsupportedProtocolException:
        """
        raise NotImplementedError

    @handler("DescribeSSLPolicies")
    def describe_ssl_policies(
        self,
        context: RequestContext,
        names: SslPolicyNames = None,
        marker: Marker = None,
        page_size: PageSize = None,
        load_balancer_type: LoadBalancerTypeEnum = None,
        **kwargs,
    ) -> DescribeSSLPoliciesOutput:
        """Describes the specified policies or all policies used for SSL
        negotiation.

        For more information, see `Security
        policies <https://docs.aws.amazon.com/elasticloadbalancing/latest/application/create-https-listener.html#describe-ssl-policies>`__
        in the *Application Load Balancers Guide* or `Security
        policies <https://docs.aws.amazon.com/elasticloadbalancing/latest/network/create-tls-listener.html#describe-ssl-policies>`__
        in the *Network Load Balancers Guide*.

        :param names: The names of the policies.
        :param marker: The marker for the next set of results.
        :param page_size: The maximum number of results to return with this call.
        :param load_balancer_type: The type of load balancer.
        :returns: DescribeSSLPoliciesOutput
        :raises SSLPolicyNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeTags")
    def describe_tags(
        self, context: RequestContext, resource_arns: ResourceArns, **kwargs
    ) -> DescribeTagsOutput:
        """Describes the tags for the specified Elastic Load Balancing resources.
        You can describe the tags for one or more Application Load Balancers,
        Network Load Balancers, Gateway Load Balancers, target groups,
        listeners, or rules.

        :param resource_arns: The Amazon Resource Names (ARN) of the resources.
        :returns: DescribeTagsOutput
        :raises LoadBalancerNotFoundException:
        :raises TargetGroupNotFoundException:
        :raises ListenerNotFoundException:
        :raises RuleNotFoundException:
        :raises TrustStoreNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeTargetGroupAttributes")
    def describe_target_group_attributes(
        self, context: RequestContext, target_group_arn: TargetGroupArn, **kwargs
    ) -> DescribeTargetGroupAttributesOutput:
        """Describes the attributes for the specified target group.

        For more information, see the following:

        -  `Target group
           attributes <https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-target-groups.html#target-group-attributes>`__
           in the *Application Load Balancers Guide*

        -  `Target group
           attributes <https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-target-groups.html#target-group-attributes>`__
           in the *Network Load Balancers Guide*

        -  `Target group
           attributes <https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/target-groups.html#target-group-attributes>`__
           in the *Gateway Load Balancers Guide*

        :param target_group_arn: The Amazon Resource Name (ARN) of the target group.
        :returns: DescribeTargetGroupAttributesOutput
        :raises TargetGroupNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeTargetGroups")
    def describe_target_groups(
        self,
        context: RequestContext,
        load_balancer_arn: LoadBalancerArn = None,
        target_group_arns: TargetGroupArns = None,
        names: TargetGroupNames = None,
        marker: Marker = None,
        page_size: PageSize = None,
        **kwargs,
    ) -> DescribeTargetGroupsOutput:
        """Describes the specified target groups or all of your target groups. By
        default, all target groups are described. Alternatively, you can specify
        one of the following to filter the results: the ARN of the load
        balancer, the names of one or more target groups, or the ARNs of one or
        more target groups.

        :param load_balancer_arn: The Amazon Resource Name (ARN) of the load balancer.
        :param target_group_arns: The Amazon Resource Names (ARN) of the target groups.
        :param names: The names of the target groups.
        :param marker: The marker for the next set of results.
        :param page_size: The maximum number of results to return with this call.
        :returns: DescribeTargetGroupsOutput
        :raises LoadBalancerNotFoundException:
        :raises TargetGroupNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeTargetHealth")
    def describe_target_health(
        self,
        context: RequestContext,
        target_group_arn: TargetGroupArn,
        targets: TargetDescriptions = None,
        include: ListOfDescribeTargetHealthIncludeOptions = None,
        **kwargs,
    ) -> DescribeTargetHealthOutput:
        """Describes the health of the specified targets or all of your targets.

        :param target_group_arn: The Amazon Resource Name (ARN) of the target group.
        :param targets: The targets.
        :param include: Used to include anomaly detection information.
        :returns: DescribeTargetHealthOutput
        :raises InvalidTargetException:
        :raises TargetGroupNotFoundException:
        :raises HealthUnavailableException:
        """
        raise NotImplementedError

    @handler("DescribeTrustStoreAssociations")
    def describe_trust_store_associations(
        self,
        context: RequestContext,
        trust_store_arn: TrustStoreArn,
        marker: Marker = None,
        page_size: PageSize = None,
        **kwargs,
    ) -> DescribeTrustStoreAssociationsOutput:
        """Describes all resources associated with the specified trust store.

        :param trust_store_arn: The Amazon Resource Name (ARN) of the trust store.
        :param marker: The marker for the next set of results.
        :param page_size: The maximum number of results to return with this call.
        :returns: DescribeTrustStoreAssociationsOutput
        :raises TrustStoreNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeTrustStoreRevocations")
    def describe_trust_store_revocations(
        self,
        context: RequestContext,
        trust_store_arn: TrustStoreArn,
        revocation_ids: RevocationIds = None,
        marker: Marker = None,
        page_size: PageSize = None,
        **kwargs,
    ) -> DescribeTrustStoreRevocationsOutput:
        """Describes the revocation files in use by the specified trust store or
        revocation files.

        :param trust_store_arn: The Amazon Resource Name (ARN) of the trust store.
        :param revocation_ids: The revocation IDs of the revocation files you want to describe.
        :param marker: The marker for the next set of results.
        :param page_size: The maximum number of results to return with this call.
        :returns: DescribeTrustStoreRevocationsOutput
        :raises TrustStoreNotFoundException:
        :raises RevocationIdNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeTrustStores")
    def describe_trust_stores(
        self,
        context: RequestContext,
        trust_store_arns: TrustStoreArns = None,
        names: TrustStoreNames = None,
        marker: Marker = None,
        page_size: PageSize = None,
        **kwargs,
    ) -> DescribeTrustStoresOutput:
        """Describes all trust stores for the specified account.

        :param trust_store_arns: The Amazon Resource Name (ARN) of the trust store.
        :param names: The names of the trust stores.
        :param marker: The marker for the next set of results.
        :param page_size: The maximum number of results to return with this call.
        :returns: DescribeTrustStoresOutput
        :raises TrustStoreNotFoundException:
        """
        raise NotImplementedError

    @handler("GetResourcePolicy")
    def get_resource_policy(
        self, context: RequestContext, resource_arn: ResourceArn, **kwargs
    ) -> GetResourcePolicyOutput:
        """Retrieves the resource policy for a specified resource.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource.
        :returns: GetResourcePolicyOutput
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("GetTrustStoreCaCertificatesBundle")
    def get_trust_store_ca_certificates_bundle(
        self, context: RequestContext, trust_store_arn: TrustStoreArn, **kwargs
    ) -> GetTrustStoreCaCertificatesBundleOutput:
        """Retrieves the ca certificate bundle.

        This action returns a pre-signed S3 URI which is active for ten minutes.

        :param trust_store_arn: The Amazon Resource Name (ARN) of the trust store.
        :returns: GetTrustStoreCaCertificatesBundleOutput
        :raises TrustStoreNotFoundException:
        """
        raise NotImplementedError

    @handler("GetTrustStoreRevocationContent")
    def get_trust_store_revocation_content(
        self,
        context: RequestContext,
        trust_store_arn: TrustStoreArn,
        revocation_id: RevocationId,
        **kwargs,
    ) -> GetTrustStoreRevocationContentOutput:
        """Retrieves the specified revocation file.

        This action returns a pre-signed S3 URI which is active for ten minutes.

        :param trust_store_arn: The Amazon Resource Name (ARN) of the trust store.
        :param revocation_id: The revocation ID of the revocation file.
        :returns: GetTrustStoreRevocationContentOutput
        :raises TrustStoreNotFoundException:
        :raises RevocationIdNotFoundException:
        """
        raise NotImplementedError

    @handler("ModifyCapacityReservation")
    def modify_capacity_reservation(
        self,
        context: RequestContext,
        load_balancer_arn: LoadBalancerArn,
        minimum_load_balancer_capacity: MinimumLoadBalancerCapacity = None,
        reset_capacity_reservation: ResetCapacityReservation = None,
        **kwargs,
    ) -> ModifyCapacityReservationOutput:
        """Modifies the capacity reservation of the specified load balancer.

        When modifying capacity reservation, you must include at least one
        ``MinimumLoadBalancerCapacity`` or ``ResetCapacityReservation``.

        :param load_balancer_arn: The Amazon Resource Name (ARN) of the load balancer.
        :param minimum_load_balancer_capacity: The minimum load balancer capacity reserved.
        :param reset_capacity_reservation: Resets the capacity reservation.
        :returns: ModifyCapacityReservationOutput
        :raises LoadBalancerNotFoundException:
        :raises InvalidConfigurationRequestException:
        :raises CapacityUnitsLimitExceededException:
        :raises CapacityReservationPendingException:
        :raises InsufficientCapacityException:
        :raises CapacityDecreaseRequestsLimitExceededException:
        :raises PriorRequestNotCompleteException:
        :raises OperationNotPermittedException:
        """
        raise NotImplementedError

    @handler("ModifyIpPools")
    def modify_ip_pools(
        self,
        context: RequestContext,
        load_balancer_arn: LoadBalancerArn,
        ipam_pools: IpamPools = None,
        remove_ipam_pools: RemoveIpamPools = None,
        **kwargs,
    ) -> ModifyIpPoolsOutput:
        """[Application Load Balancers] Modify the IP pool associated to a load
        balancer.

        :param load_balancer_arn: The Amazon Resource Name (ARN) of the load balancer.
        :param ipam_pools: The IPAM pools to be modified.
        :param remove_ipam_pools: Remove the IP pools in use by the load balancer.
        :returns: ModifyIpPoolsOutput
        :raises LoadBalancerNotFoundException:
        """
        raise NotImplementedError

    @handler("ModifyListener")
    def modify_listener(
        self,
        context: RequestContext,
        listener_arn: ListenerArn,
        port: Port = None,
        protocol: ProtocolEnum = None,
        ssl_policy: SslPolicyName = None,
        certificates: CertificateList = None,
        default_actions: Actions = None,
        alpn_policy: AlpnPolicyName = None,
        mutual_authentication: MutualAuthenticationAttributes = None,
        **kwargs,
    ) -> ModifyListenerOutput:
        """Replaces the specified properties of the specified listener. Any
        properties that you do not specify remain unchanged.

        Changing the protocol from HTTPS to HTTP, or from TLS to TCP, removes
        the security policy and default certificate properties. If you change
        the protocol from HTTP to HTTPS, or from TCP to TLS, you must add the
        security policy and default certificate properties.

        To add an item to a list, remove an item from a list, or update an item
        in a list, you must provide the entire list. For example, to add an
        action, specify a list with the current actions plus the new action.

        :param listener_arn: The Amazon Resource Name (ARN) of the listener.
        :param port: The port for connections from clients to the load balancer.
        :param protocol: The protocol for connections from clients to the load balancer.
        :param ssl_policy: [HTTPS and TLS listeners] The security policy that defines which
        protocols and ciphers are supported.
        :param certificates: [HTTPS and TLS listeners] The default certificate for the listener.
        :param default_actions: The actions for the default rule.
        :param alpn_policy: [TLS listeners] The name of the Application-Layer Protocol Negotiation
        (ALPN) policy.
        :param mutual_authentication: The mutual authentication configuration information.
        :returns: ModifyListenerOutput
        :raises DuplicateListenerException:
        :raises TooManyListenersException:
        :raises TooManyCertificatesException:
        :raises ListenerNotFoundException:
        :raises TargetGroupNotFoundException:
        :raises TargetGroupAssociationLimitException:
        :raises IncompatibleProtocolsException:
        :raises SSLPolicyNotFoundException:
        :raises CertificateNotFoundException:
        :raises InvalidConfigurationRequestException:
        :raises UnsupportedProtocolException:
        :raises TooManyRegistrationsForTargetIdException:
        :raises TooManyTargetsException:
        :raises TooManyActionsException:
        :raises InvalidLoadBalancerActionException:
        :raises TooManyUniqueTargetGroupsPerLoadBalancerException:
        :raises ALPNPolicyNotSupportedException:
        :raises TrustStoreNotFoundException:
        :raises TrustStoreNotReadyException:
        """
        raise NotImplementedError

    @handler("ModifyListenerAttributes")
    def modify_listener_attributes(
        self,
        context: RequestContext,
        listener_arn: ListenerArn,
        attributes: ListenerAttributes,
        **kwargs,
    ) -> ModifyListenerAttributesOutput:
        """Modifies the specified attributes of the specified listener.

        :param listener_arn: The Amazon Resource Name (ARN) of the listener.
        :param attributes: The listener attributes.
        :returns: ModifyListenerAttributesOutput
        :raises ListenerNotFoundException:
        :raises InvalidConfigurationRequestException:
        """
        raise NotImplementedError

    @handler("ModifyLoadBalancerAttributes")
    def modify_load_balancer_attributes(
        self,
        context: RequestContext,
        load_balancer_arn: LoadBalancerArn,
        attributes: LoadBalancerAttributes,
        **kwargs,
    ) -> ModifyLoadBalancerAttributesOutput:
        """Modifies the specified attributes of the specified Application Load
        Balancer, Network Load Balancer, or Gateway Load Balancer.

        If any of the specified attributes can't be modified as requested, the
        call fails. Any existing attributes that you do not modify retain their
        current values.

        :param load_balancer_arn: The Amazon Resource Name (ARN) of the load balancer.
        :param attributes: The load balancer attributes.
        :returns: ModifyLoadBalancerAttributesOutput
        :raises LoadBalancerNotFoundException:
        :raises InvalidConfigurationRequestException:
        """
        raise NotImplementedError

    @handler("ModifyRule")
    def modify_rule(
        self,
        context: RequestContext,
        rule_arn: RuleArn,
        conditions: RuleConditionList = None,
        actions: Actions = None,
        **kwargs,
    ) -> ModifyRuleOutput:
        """Replaces the specified properties of the specified rule. Any properties
        that you do not specify are unchanged.

        To add an item to a list, remove an item from a list, or update an item
        in a list, you must provide the entire list. For example, to add an
        action, specify a list with the current actions plus the new action.

        :param rule_arn: The Amazon Resource Name (ARN) of the rule.
        :param conditions: The conditions.
        :param actions: The actions.
        :returns: ModifyRuleOutput
        :raises TargetGroupAssociationLimitException:
        :raises IncompatibleProtocolsException:
        :raises RuleNotFoundException:
        :raises OperationNotPermittedException:
        :raises TooManyRegistrationsForTargetIdException:
        :raises TooManyTargetsException:
        :raises TargetGroupNotFoundException:
        :raises UnsupportedProtocolException:
        :raises TooManyActionsException:
        :raises InvalidLoadBalancerActionException:
        :raises TooManyUniqueTargetGroupsPerLoadBalancerException:
        """
        raise NotImplementedError

    @handler("ModifyTargetGroup")
    def modify_target_group(
        self,
        context: RequestContext,
        target_group_arn: TargetGroupArn,
        health_check_protocol: ProtocolEnum = None,
        health_check_port: HealthCheckPort = None,
        health_check_path: Path = None,
        health_check_enabled: HealthCheckEnabled = None,
        health_check_interval_seconds: HealthCheckIntervalSeconds = None,
        health_check_timeout_seconds: HealthCheckTimeoutSeconds = None,
        healthy_threshold_count: HealthCheckThresholdCount = None,
        unhealthy_threshold_count: HealthCheckThresholdCount = None,
        matcher: Matcher = None,
        **kwargs,
    ) -> ModifyTargetGroupOutput:
        """Modifies the health checks used when evaluating the health state of the
        targets in the specified target group.

        :param target_group_arn: The Amazon Resource Name (ARN) of the target group.
        :param health_check_protocol: The protocol the load balancer uses when performing health checks on
        targets.
        :param health_check_port: The port the load balancer uses when performing health checks on
        targets.
        :param health_check_path: [HTTP/HTTPS health checks] The destination for health checks on the
        targets.
        :param health_check_enabled: Indicates whether health checks are enabled.
        :param health_check_interval_seconds: The approximate amount of time, in seconds, between health checks of an
        individual target.
        :param health_check_timeout_seconds: [HTTP/HTTPS health checks] The amount of time, in seconds, during which
        no response means a failed health check.
        :param healthy_threshold_count: The number of consecutive health checks successes required before
        considering an unhealthy target healthy.
        :param unhealthy_threshold_count: The number of consecutive health check failures required before
        considering the target unhealthy.
        :param matcher: [HTTP/HTTPS health checks] The HTTP or gRPC codes to use when checking
        for a successful response from a target.
        :returns: ModifyTargetGroupOutput
        :raises TargetGroupNotFoundException:
        :raises InvalidConfigurationRequestException:
        """
        raise NotImplementedError

    @handler("ModifyTargetGroupAttributes")
    def modify_target_group_attributes(
        self,
        context: RequestContext,
        target_group_arn: TargetGroupArn,
        attributes: TargetGroupAttributes,
        **kwargs,
    ) -> ModifyTargetGroupAttributesOutput:
        """Modifies the specified attributes of the specified target group.

        :param target_group_arn: The Amazon Resource Name (ARN) of the target group.
        :param attributes: The target group attributes.
        :returns: ModifyTargetGroupAttributesOutput
        :raises TargetGroupNotFoundException:
        :raises InvalidConfigurationRequestException:
        """
        raise NotImplementedError

    @handler("ModifyTrustStore")
    def modify_trust_store(
        self,
        context: RequestContext,
        trust_store_arn: TrustStoreArn,
        ca_certificates_bundle_s3_bucket: S3Bucket,
        ca_certificates_bundle_s3_key: S3Key,
        ca_certificates_bundle_s3_object_version: S3ObjectVersion = None,
        **kwargs,
    ) -> ModifyTrustStoreOutput:
        """Update the ca certificate bundle for the specified trust store.

        :param trust_store_arn: The Amazon Resource Name (ARN) of the trust store.
        :param ca_certificates_bundle_s3_bucket: The Amazon S3 bucket for the ca certificates bundle.
        :param ca_certificates_bundle_s3_key: The Amazon S3 path for the ca certificates bundle.
        :param ca_certificates_bundle_s3_object_version: The Amazon S3 object version for the ca certificates bundle.
        :returns: ModifyTrustStoreOutput
        :raises TrustStoreNotFoundException:
        :raises InvalidCaCertificatesBundleException:
        :raises CaCertificatesBundleNotFoundException:
        """
        raise NotImplementedError

    @handler("RegisterTargets")
    def register_targets(
        self,
        context: RequestContext,
        target_group_arn: TargetGroupArn,
        targets: TargetDescriptions,
        **kwargs,
    ) -> RegisterTargetsOutput:
        """Registers the specified targets with the specified target group.

        If the target is an EC2 instance, it must be in the ``running`` state
        when you register it.

        By default, the load balancer routes requests to registered targets
        using the protocol and port for the target group. Alternatively, you can
        override the port for a target when you register it. You can register
        each EC2 instance or IP address with the same target group multiple
        times using different ports.

        With a Network Load Balancer, you can't register instances by instance
        ID if they have the following instance types: C1, CC1, CC2, CG1, CG2,
        CR1, CS1, G1, G2, HI1, HS1, M1, M2, M3, and T1. You can register
        instances of these types by IP address.

        :param target_group_arn: The Amazon Resource Name (ARN) of the target group.
        :param targets: The targets.
        :returns: RegisterTargetsOutput
        :raises TargetGroupNotFoundException:
        :raises TooManyTargetsException:
        :raises InvalidTargetException:
        :raises TooManyRegistrationsForTargetIdException:
        """
        raise NotImplementedError

    @handler("RemoveListenerCertificates")
    def remove_listener_certificates(
        self,
        context: RequestContext,
        listener_arn: ListenerArn,
        certificates: CertificateList,
        **kwargs,
    ) -> RemoveListenerCertificatesOutput:
        """Removes the specified certificate from the certificate list for the
        specified HTTPS or TLS listener.

        :param listener_arn: The Amazon Resource Name (ARN) of the listener.
        :param certificates: The certificate to remove.
        :returns: RemoveListenerCertificatesOutput
        :raises ListenerNotFoundException:
        :raises OperationNotPermittedException:
        """
        raise NotImplementedError

    @handler("RemoveTags")
    def remove_tags(
        self, context: RequestContext, resource_arns: ResourceArns, tag_keys: TagKeys, **kwargs
    ) -> RemoveTagsOutput:
        """Removes the specified tags from the specified Elastic Load Balancing
        resources. You can remove the tags for one or more Application Load
        Balancers, Network Load Balancers, Gateway Load Balancers, target
        groups, listeners, or rules.

        :param resource_arns: The Amazon Resource Name (ARN) of the resource.
        :param tag_keys: The tag keys for the tags to remove.
        :returns: RemoveTagsOutput
        :raises LoadBalancerNotFoundException:
        :raises TargetGroupNotFoundException:
        :raises ListenerNotFoundException:
        :raises RuleNotFoundException:
        :raises TooManyTagsException:
        :raises TrustStoreNotFoundException:
        """
        raise NotImplementedError

    @handler("RemoveTrustStoreRevocations")
    def remove_trust_store_revocations(
        self,
        context: RequestContext,
        trust_store_arn: TrustStoreArn,
        revocation_ids: RevocationIds,
        **kwargs,
    ) -> RemoveTrustStoreRevocationsOutput:
        """Removes the specified revocation file from the specified trust store.

        :param trust_store_arn: The Amazon Resource Name (ARN) of the trust store.
        :param revocation_ids: The revocation IDs of the revocation files you want to remove.
        :returns: RemoveTrustStoreRevocationsOutput
        :raises TrustStoreNotFoundException:
        :raises RevocationIdNotFoundException:
        """
        raise NotImplementedError

    @handler("SetIpAddressType")
    def set_ip_address_type(
        self,
        context: RequestContext,
        load_balancer_arn: LoadBalancerArn,
        ip_address_type: IpAddressType,
        **kwargs,
    ) -> SetIpAddressTypeOutput:
        """Sets the type of IP addresses used by the subnets of the specified load
        balancer.

        :param load_balancer_arn: The Amazon Resource Name (ARN) of the load balancer.
        :param ip_address_type: The IP address type.
        :returns: SetIpAddressTypeOutput
        :raises LoadBalancerNotFoundException:
        :raises InvalidConfigurationRequestException:
        :raises InvalidSubnetException:
        """
        raise NotImplementedError

    @handler("SetRulePriorities")
    def set_rule_priorities(
        self, context: RequestContext, rule_priorities: RulePriorityList, **kwargs
    ) -> SetRulePrioritiesOutput:
        """Sets the priorities of the specified rules.

        You can reorder the rules as long as there are no priority conflicts in
        the new order. Any existing rules that you do not specify retain their
        current priority.

        :param rule_priorities: The rule priorities.
        :returns: SetRulePrioritiesOutput
        :raises RuleNotFoundException:
        :raises PriorityInUseException:
        :raises OperationNotPermittedException:
        """
        raise NotImplementedError

    @handler("SetSecurityGroups")
    def set_security_groups(
        self,
        context: RequestContext,
        load_balancer_arn: LoadBalancerArn,
        security_groups: SecurityGroups,
        enforce_security_group_inbound_rules_on_private_link_traffic: EnforceSecurityGroupInboundRulesOnPrivateLinkTrafficEnum = None,
        **kwargs,
    ) -> SetSecurityGroupsOutput:
        """Associates the specified security groups with the specified Application
        Load Balancer or Network Load Balancer. The specified security groups
        override the previously associated security groups.

        You can't perform this operation on a Network Load Balancer unless you
        specified a security group for the load balancer when you created it.

        You can't associate a security group with a Gateway Load Balancer.

        :param load_balancer_arn: The Amazon Resource Name (ARN) of the load balancer.
        :param security_groups: The IDs of the security groups.
        :param enforce_security_group_inbound_rules_on_private_link_traffic: Indicates whether to evaluate inbound security group rules for traffic
        sent to a Network Load Balancer through Amazon Web Services PrivateLink.
        :returns: SetSecurityGroupsOutput
        :raises LoadBalancerNotFoundException:
        :raises InvalidConfigurationRequestException:
        :raises InvalidSecurityGroupException:
        """
        raise NotImplementedError

    @handler("SetSubnets")
    def set_subnets(
        self,
        context: RequestContext,
        load_balancer_arn: LoadBalancerArn,
        subnets: Subnets = None,
        subnet_mappings: SubnetMappings = None,
        ip_address_type: IpAddressType = None,
        enable_prefix_for_ipv6_source_nat: EnablePrefixForIpv6SourceNatEnum = None,
        **kwargs,
    ) -> SetSubnetsOutput:
        """Enables the Availability Zones for the specified public subnets for the
        specified Application Load Balancer, Network Load Balancer or Gateway
        Load Balancer. The specified subnets replace the previously enabled
        subnets.

        When you specify subnets for a Network Load Balancer, or Gateway Load
        Balancer you must include all subnets that were enabled previously, with
        their existing configurations, plus any additional subnets.

        :param load_balancer_arn: The Amazon Resource Name (ARN) of the load balancer.
        :param subnets: The IDs of the public subnets.
        :param subnet_mappings: The IDs of the public subnets.
        :param ip_address_type: The IP address type.
        :param enable_prefix_for_ipv6_source_nat: [Network Load Balancers with UDP listeners] Indicates whether to use an
        IPv6 prefix from each subnet for source NAT.
        :returns: SetSubnetsOutput
        :raises LoadBalancerNotFoundException:
        :raises InvalidConfigurationRequestException:
        :raises SubnetNotFoundException:
        :raises InvalidSubnetException:
        :raises AllocationIdNotFoundException:
        :raises AvailabilityZoneNotSupportedException:
        :raises CapacityReservationPendingException:
        """
        raise NotImplementedError
