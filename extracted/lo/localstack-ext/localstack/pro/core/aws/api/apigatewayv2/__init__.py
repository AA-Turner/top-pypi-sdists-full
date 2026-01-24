from collections.abc import Iterable
from datetime import datetime
from enum import StrEnum
from typing import IO, TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

Arn = str
Id = str
IntegerWithLengthBetween0And3600 = int
IntegerWithLengthBetween50And30000 = int
IntegerWithLengthBetweenMinus1And86400 = int
NextToken = str
RoutingRulePriority = int
MaxResults = int
SelectionExpression = str
SelectionKey = str
StringWithLengthBetween0And1024 = str
StringWithLengthBetween0And2048 = str
StringWithLengthBetween0And32K = str
StringWithLengthBetween1And1024 = str
StringWithLengthBetween1And128 = str
StringWithLengthBetween1And1600 = str
StringWithLengthBetween1And256 = str
StringWithLengthBetween1And512 = str
StringWithLengthBetween1And64 = str
UriWithLengthBetween1And2048 = str
_boolean = bool
_double = float
_integer = int
_string = str
_stringMin0Max1024 = str
_stringMin0Max1092 = str
_stringMin0Max255 = str
_stringMin10Max2048 = str
_stringMin10Max30PatternAZ09 = str
_stringMin1Max1024 = str
_stringMin1Max128 = str
_stringMin1Max16 = str
_stringMin1Max20 = str
_stringMin1Max2048 = str
_stringMin1Max255 = str
_stringMin1Max256 = str
_stringMin1Max307200 = str
_stringMin1Max32768 = str
_stringMin1Max4096 = str
_stringMin1Max50 = str
_stringMin1Max64 = str
_stringMin20Max2048 = str
_stringMin3Max255 = str
_stringMin3Max256 = str


class AuthorizationType(StrEnum):
    NONE = "NONE"
    AWS_IAM = "AWS_IAM"
    CUSTOM = "CUSTOM"
    JWT = "JWT"


class AuthorizerType(StrEnum):
    REQUEST = "REQUEST"
    JWT = "JWT"


class ConnectionType(StrEnum):
    INTERNET = "INTERNET"
    VPC_LINK = "VPC_LINK"


class ContentHandlingStrategy(StrEnum):
    CONVERT_TO_BINARY = "CONVERT_TO_BINARY"
    CONVERT_TO_TEXT = "CONVERT_TO_TEXT"


class DeploymentStatus(StrEnum):
    PENDING = "PENDING"
    FAILED = "FAILED"
    DEPLOYED = "DEPLOYED"


class DomainNameStatus(StrEnum):
    AVAILABLE = "AVAILABLE"
    UPDATING = "UPDATING"
    PENDING_CERTIFICATE_REIMPORT = "PENDING_CERTIFICATE_REIMPORT"
    PENDING_OWNERSHIP_VERIFICATION = "PENDING_OWNERSHIP_VERIFICATION"


class EndpointType(StrEnum):
    REGIONAL = "REGIONAL"
    EDGE = "EDGE"


class IntegrationType(StrEnum):
    AWS = "AWS"
    HTTP = "HTTP"
    MOCK = "MOCK"
    HTTP_PROXY = "HTTP_PROXY"
    AWS_PROXY = "AWS_PROXY"


class IpAddressType(StrEnum):
    ipv4 = "ipv4"
    dualstack = "dualstack"


class LoggingLevel(StrEnum):
    ERROR = "ERROR"
    INFO = "INFO"
    OFF = "OFF"


class PassthroughBehavior(StrEnum):
    WHEN_NO_MATCH = "WHEN_NO_MATCH"
    NEVER = "NEVER"
    WHEN_NO_TEMPLATES = "WHEN_NO_TEMPLATES"


class PreviewStatus(StrEnum):
    PREVIEW_IN_PROGRESS = "PREVIEW_IN_PROGRESS"
    PREVIEW_FAILED = "PREVIEW_FAILED"
    PREVIEW_READY = "PREVIEW_READY"


class ProtocolType(StrEnum):
    WEBSOCKET = "WEBSOCKET"
    HTTP = "HTTP"


class PublishStatus(StrEnum):
    PUBLISHED = "PUBLISHED"
    PUBLISH_IN_PROGRESS = "PUBLISH_IN_PROGRESS"
    PUBLISH_FAILED = "PUBLISH_FAILED"
    DISABLED = "DISABLED"


class RoutingMode(StrEnum):
    API_MAPPING_ONLY = "API_MAPPING_ONLY"
    ROUTING_RULE_ONLY = "ROUTING_RULE_ONLY"
    ROUTING_RULE_THEN_API_MAPPING = "ROUTING_RULE_THEN_API_MAPPING"


class SecurityPolicy(StrEnum):
    TLS_1_0 = "TLS_1_0"
    TLS_1_2 = "TLS_1_2"


class Status(StrEnum):
    AVAILABLE = "AVAILABLE"
    IN_PROGRESS = "IN_PROGRESS"
    FAILED = "FAILED"


class TryItState(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class VpcLinkStatus(StrEnum):
    PENDING = "PENDING"
    AVAILABLE = "AVAILABLE"
    DELETING = "DELETING"
    FAILED = "FAILED"
    INACTIVE = "INACTIVE"


class VpcLinkVersion(StrEnum):
    V2 = "V2"


class AccessDeniedException(ServiceException):
    code: str = "AccessDeniedException"
    sender_fault: bool = False
    status_code: int = 403


class BadRequestException(ServiceException):
    """The request is not valid, for example, the input is incomplete or
    incorrect. See the accompanying error message for details.
    """

    code: str = "BadRequestException"
    sender_fault: bool = False
    status_code: int = 400


class ConflictException(ServiceException):
    """The requested operation would cause a conflict with the current state of
    a service resource associated with the request. Resolve the conflict
    before retrying this request. See the accompanying error message for
    details.
    """

    code: str = "ConflictException"
    sender_fault: bool = False
    status_code: int = 409


class NotFoundException(ServiceException):
    """The resource specified in the request was not found. See the message
    field for more information.
    """

    code: str = "NotFoundException"
    sender_fault: bool = False
    status_code: int = 404
    ResourceType: _string | None


class TooManyRequestsException(ServiceException):
    """A limit has been exceeded. See the accompanying error message for
    details.
    """

    code: str = "TooManyRequestsException"
    sender_fault: bool = False
    status_code: int = 429
    LimitType: _string | None


class ACMManaged(TypedDict, total=False):
    """Represents a domain name and certificate for a portal."""

    CertificateArn: _stringMin10Max2048
    DomainName: _stringMin3Max256


class AccessDeniedExceptionResponseContent(TypedDict, total=False):
    """The error message."""

    Message: _string | None


class AccessLogSettings(TypedDict, total=False):
    """Settings for logging access in a stage."""

    DestinationArn: Arn | None
    Format: StringWithLengthBetween1And1024 | None


_listOf__string = list[_string]
Tags = dict[_string, StringWithLengthBetween1And1600]
_timestampIso8601 = datetime
CorsHeaderList = list[_string]
CorsOriginList = list[_string]
CorsMethodList = list[StringWithLengthBetween1And64]


class Cors(TypedDict, total=False):
    """Represents a CORS configuration. Supported only for HTTP APIs. See
    `Configuring
    CORS <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-cors.html>`__
    for more information.
    """

    AllowCredentials: _boolean | None
    AllowHeaders: CorsHeaderList | None
    AllowMethods: CorsMethodList | None
    AllowOrigins: CorsOriginList | None
    ExposeHeaders: CorsHeaderList | None
    MaxAge: IntegerWithLengthBetweenMinus1And86400 | None


class Api(TypedDict, total=False):
    """Represents an API."""

    ApiEndpoint: _string | None
    ApiGatewayManaged: _boolean | None
    ApiId: Id | None
    ApiKeySelectionExpression: SelectionExpression | None
    CorsConfiguration: Cors | None
    CreatedDate: _timestampIso8601 | None
    Description: StringWithLengthBetween0And1024 | None
    DisableSchemaValidation: _boolean | None
    DisableExecuteApiEndpoint: _boolean | None
    ImportInfo: _listOf__string | None
    IpAddressType: IpAddressType | None
    Name: StringWithLengthBetween1And128
    ProtocolType: ProtocolType
    RouteSelectionExpression: SelectionExpression
    Tags: Tags | None
    Version: StringWithLengthBetween1And64 | None
    Warnings: _listOf__string | None


class ApiMapping(TypedDict, total=False):
    """Represents an API mapping."""

    ApiId: Id
    ApiMappingId: Id | None
    ApiMappingKey: SelectionKey | None
    Stage: StringWithLengthBetween1And128


_listOfApiMapping = list[ApiMapping]


class ApiMappings(TypedDict, total=False):
    """Represents a collection of ApiMappings resources."""

    Items: _listOfApiMapping | None
    NextToken: NextToken | None


_listOfApi = list[Api]


class Apis(TypedDict, total=False):
    """Represents a collection of APIs."""

    Items: _listOfApi | None
    NextToken: NextToken | None


class None_(TypedDict, total=False):
    """The none option."""

    pass


class CognitoConfig(TypedDict, total=False):
    """The configuration for using Amazon Cognito user pools to control access
    to your portal.
    """

    AppClientId: _stringMin1Max256
    UserPoolArn: _stringMin20Max2048
    UserPoolDomain: _stringMin20Max2048


Authorization = TypedDict(
    "Authorization",
    {
        "CognitoConfig": CognitoConfig | None,
        "None": None_ | None,
    },
    total=False,
)
AuthorizationScopes = list[StringWithLengthBetween1And64]


class JWTConfiguration(TypedDict, total=False):
    """Represents the configuration of a JWT authorizer. Required for the JWT
    authorizer type. Supported only for HTTP APIs.
    """

    Audience: _listOf__string | None
    Issuer: UriWithLengthBetween1And2048 | None


IdentitySourceList = list[_string]


class Authorizer(TypedDict, total=False):
    """Represents an authorizer."""

    AuthorizerCredentialsArn: Arn | None
    AuthorizerId: Id | None
    AuthorizerPayloadFormatVersion: StringWithLengthBetween1And64 | None
    AuthorizerResultTtlInSeconds: IntegerWithLengthBetween0And3600 | None
    AuthorizerType: AuthorizerType | None
    AuthorizerUri: UriWithLengthBetween1And2048 | None
    EnableSimpleResponses: _boolean | None
    IdentitySource: IdentitySourceList | None
    IdentityValidationExpression: StringWithLengthBetween0And1024 | None
    JwtConfiguration: JWTConfiguration | None
    Name: StringWithLengthBetween1And128


_listOfAuthorizer = list[Authorizer]


class Authorizers(TypedDict, total=False):
    """Represents a collection of authorizers."""

    Items: _listOfAuthorizer | None
    NextToken: NextToken | None


class BadRequestExceptionResponseContent(TypedDict, total=False):
    """The response content for bad request exception."""

    Message: _string | None


class ConflictExceptionResponseContent(TypedDict, total=False):
    """The resource identifier."""

    Message: _string | None


class CreateApiInput(TypedDict, total=False):
    """Represents the input parameters for a CreateApi request."""

    ApiKeySelectionExpression: SelectionExpression | None
    CorsConfiguration: Cors | None
    CredentialsArn: Arn | None
    Description: StringWithLengthBetween0And1024 | None
    DisableSchemaValidation: _boolean | None
    DisableExecuteApiEndpoint: _boolean | None
    Name: StringWithLengthBetween1And128
    ProtocolType: ProtocolType
    RouteKey: SelectionKey | None
    RouteSelectionExpression: SelectionExpression | None
    Tags: Tags | None
    Target: UriWithLengthBetween1And2048 | None
    Version: StringWithLengthBetween1And64 | None


class CreateApiMappingInput(TypedDict, total=False):
    """Represents the input parameters for a CreateApiMapping request."""

    ApiId: Id
    ApiMappingKey: SelectionKey | None
    Stage: StringWithLengthBetween1And128


class CreateApiMappingRequest(ServiceRequest):
    """Creates a new ApiMapping resource to represent an API mapping."""

    ApiId: Id
    ApiMappingKey: SelectionKey | None
    DomainName: _string
    Stage: StringWithLengthBetween1And128


class CreateApiMappingResponse(TypedDict, total=False):
    ApiId: Id | None
    ApiMappingId: Id | None
    ApiMappingKey: SelectionKey | None
    Stage: StringWithLengthBetween1And128 | None


class CreateApiRequest(ServiceRequest):
    """Creates a new Api resource to represent an API."""

    ApiKeySelectionExpression: SelectionExpression | None
    CorsConfiguration: Cors | None
    CredentialsArn: Arn | None
    Description: StringWithLengthBetween0And1024 | None
    DisableSchemaValidation: _boolean | None
    DisableExecuteApiEndpoint: _boolean | None
    IpAddressType: IpAddressType | None
    Name: StringWithLengthBetween1And128
    ProtocolType: ProtocolType
    RouteKey: SelectionKey | None
    RouteSelectionExpression: SelectionExpression | None
    Tags: Tags | None
    Target: UriWithLengthBetween1And2048 | None
    Version: StringWithLengthBetween1And64 | None


class CreateApiResponse(TypedDict, total=False):
    ApiEndpoint: _string | None
    ApiGatewayManaged: _boolean | None
    ApiId: Id | None
    ApiKeySelectionExpression: SelectionExpression | None
    CorsConfiguration: Cors | None
    CreatedDate: _timestampIso8601 | None
    Description: StringWithLengthBetween0And1024 | None
    DisableSchemaValidation: _boolean | None
    DisableExecuteApiEndpoint: _boolean | None
    ImportInfo: _listOf__string | None
    IpAddressType: IpAddressType | None
    Name: StringWithLengthBetween1And128 | None
    ProtocolType: ProtocolType | None
    RouteSelectionExpression: SelectionExpression | None
    Tags: Tags | None
    Version: StringWithLengthBetween1And64 | None
    Warnings: _listOf__string | None


class CreateAuthorizerInput(TypedDict, total=False):
    """Represents the input parameters for a CreateAuthorizer request."""

    AuthorizerCredentialsArn: Arn | None
    AuthorizerPayloadFormatVersion: StringWithLengthBetween1And64 | None
    AuthorizerResultTtlInSeconds: IntegerWithLengthBetween0And3600 | None
    AuthorizerType: AuthorizerType
    AuthorizerUri: UriWithLengthBetween1And2048 | None
    EnableSimpleResponses: _boolean | None
    IdentitySource: IdentitySourceList
    IdentityValidationExpression: StringWithLengthBetween0And1024 | None
    JwtConfiguration: JWTConfiguration | None
    Name: StringWithLengthBetween1And128


class CreateAuthorizerRequest(ServiceRequest):
    """Creates a new Authorizer resource to represent an authorizer."""

    ApiId: _string
    AuthorizerCredentialsArn: Arn | None
    AuthorizerPayloadFormatVersion: StringWithLengthBetween1And64 | None
    AuthorizerResultTtlInSeconds: IntegerWithLengthBetween0And3600 | None
    AuthorizerType: AuthorizerType
    AuthorizerUri: UriWithLengthBetween1And2048 | None
    EnableSimpleResponses: _boolean | None
    IdentitySource: IdentitySourceList
    IdentityValidationExpression: StringWithLengthBetween0And1024 | None
    JwtConfiguration: JWTConfiguration | None
    Name: StringWithLengthBetween1And128


class CreateAuthorizerResponse(TypedDict, total=False):
    AuthorizerCredentialsArn: Arn | None
    AuthorizerId: Id | None
    AuthorizerPayloadFormatVersion: StringWithLengthBetween1And64 | None
    AuthorizerResultTtlInSeconds: IntegerWithLengthBetween0And3600 | None
    AuthorizerType: AuthorizerType | None
    AuthorizerUri: UriWithLengthBetween1And2048 | None
    EnableSimpleResponses: _boolean | None
    IdentitySource: IdentitySourceList | None
    IdentityValidationExpression: StringWithLengthBetween0And1024 | None
    JwtConfiguration: JWTConfiguration | None
    Name: StringWithLengthBetween1And128 | None


class CreateDeploymentInput(TypedDict, total=False):
    """Represents the input parameters for a CreateDeployment request."""

    Description: StringWithLengthBetween0And1024 | None
    StageName: StringWithLengthBetween1And128 | None


class CreateDeploymentRequest(ServiceRequest):
    """Creates a new Deployment resource to represent a deployment."""

    ApiId: _string
    Description: StringWithLengthBetween0And1024 | None
    StageName: StringWithLengthBetween1And128 | None


class CreateDeploymentResponse(TypedDict, total=False):
    AutoDeployed: _boolean | None
    CreatedDate: _timestampIso8601 | None
    DeploymentId: Id | None
    DeploymentStatus: DeploymentStatus | None
    DeploymentStatusMessage: _string | None
    Description: StringWithLengthBetween0And1024 | None


class MutualTlsAuthenticationInput(TypedDict, total=False):
    TruststoreUri: UriWithLengthBetween1And2048 | None
    TruststoreVersion: StringWithLengthBetween1And64 | None


class DomainNameConfiguration(TypedDict, total=False):
    """The domain name configuration."""

    ApiGatewayDomainName: _string | None
    CertificateArn: Arn | None
    CertificateName: StringWithLengthBetween1And128 | None
    CertificateUploadDate: _timestampIso8601 | None
    DomainNameStatus: DomainNameStatus | None
    DomainNameStatusMessage: _string | None
    EndpointType: EndpointType | None
    HostedZoneId: _string | None
    IpAddressType: IpAddressType | None
    SecurityPolicy: SecurityPolicy | None
    OwnershipVerificationCertificateArn: Arn | None


DomainNameConfigurations = list[DomainNameConfiguration]


class CreateDomainNameInput(TypedDict, total=False):
    """Represents the input parameters for a CreateDomainName request."""

    DomainName: StringWithLengthBetween1And512
    DomainNameConfigurations: DomainNameConfigurations | None
    MutualTlsAuthentication: MutualTlsAuthenticationInput | None
    RoutingMode: RoutingMode | None
    Tags: Tags | None


class CreateDomainNameRequest(ServiceRequest):
    """Creates a new DomainName resource to represent a domain name."""

    DomainName: StringWithLengthBetween1And512
    DomainNameConfigurations: DomainNameConfigurations | None
    MutualTlsAuthentication: MutualTlsAuthenticationInput | None
    RoutingMode: RoutingMode | None
    Tags: Tags | None


class MutualTlsAuthentication(TypedDict, total=False):
    TruststoreUri: UriWithLengthBetween1And2048 | None
    TruststoreVersion: StringWithLengthBetween1And64 | None
    TruststoreWarnings: _listOf__string | None


class CreateDomainNameResponse(TypedDict, total=False):
    ApiMappingSelectionExpression: SelectionExpression | None
    DomainName: StringWithLengthBetween1And512 | None
    DomainNameArn: Arn | None
    DomainNameConfigurations: DomainNameConfigurations | None
    MutualTlsAuthentication: MutualTlsAuthentication | None
    RoutingMode: RoutingMode | None
    Tags: Tags | None


class TlsConfigInput(TypedDict, total=False):
    """The TLS configuration for a private integration. If you specify a TLS
    configuration, private integration traffic uses the HTTPS protocol.
    Supported only for HTTP APIs.
    """

    ServerNameToVerify: StringWithLengthBetween1And512 | None


IntegrationParameters = dict[_string, StringWithLengthBetween1And512]
ResponseParameters = dict[_string, IntegrationParameters]
TemplateMap = dict[_string, StringWithLengthBetween0And32K]


class CreateIntegrationInput(TypedDict, total=False):
    """Represents the input parameters for a CreateIntegration request."""

    ConnectionId: StringWithLengthBetween1And1024 | None
    ConnectionType: ConnectionType | None
    ContentHandlingStrategy: ContentHandlingStrategy | None
    CredentialsArn: Arn | None
    Description: StringWithLengthBetween0And1024 | None
    IntegrationMethod: StringWithLengthBetween1And64 | None
    IntegrationSubtype: StringWithLengthBetween1And128 | None
    IntegrationType: IntegrationType
    IntegrationUri: UriWithLengthBetween1And2048 | None
    PassthroughBehavior: PassthroughBehavior | None
    PayloadFormatVersion: StringWithLengthBetween1And64 | None
    RequestParameters: IntegrationParameters | None
    RequestTemplates: TemplateMap | None
    ResponseParameters: ResponseParameters | None
    TemplateSelectionExpression: SelectionExpression | None
    TimeoutInMillis: IntegerWithLengthBetween50And30000 | None
    TlsConfig: TlsConfigInput | None


class CreateIntegrationRequest(ServiceRequest):
    """Creates a new Integration resource to represent an integration."""

    ApiId: _string
    ConnectionId: StringWithLengthBetween1And1024 | None
    ConnectionType: ConnectionType | None
    ContentHandlingStrategy: ContentHandlingStrategy | None
    CredentialsArn: Arn | None
    Description: StringWithLengthBetween0And1024 | None
    IntegrationMethod: StringWithLengthBetween1And64 | None
    IntegrationSubtype: StringWithLengthBetween1And128 | None
    IntegrationType: IntegrationType
    IntegrationUri: UriWithLengthBetween1And2048 | None
    PassthroughBehavior: PassthroughBehavior | None
    PayloadFormatVersion: StringWithLengthBetween1And64 | None
    RequestParameters: IntegrationParameters | None
    RequestTemplates: TemplateMap | None
    ResponseParameters: ResponseParameters | None
    TemplateSelectionExpression: SelectionExpression | None
    TimeoutInMillis: IntegerWithLengthBetween50And30000 | None
    TlsConfig: TlsConfigInput | None


class TlsConfig(TypedDict, total=False):
    """The TLS configuration for a private integration. If you specify a TLS
    configuration, private integration traffic uses the HTTPS protocol.
    Supported only for HTTP APIs.
    """

    ServerNameToVerify: StringWithLengthBetween1And512 | None


class CreateIntegrationResult(TypedDict, total=False):
    ApiGatewayManaged: _boolean | None
    ConnectionId: StringWithLengthBetween1And1024 | None
    ConnectionType: ConnectionType | None
    ContentHandlingStrategy: ContentHandlingStrategy | None
    CredentialsArn: Arn | None
    Description: StringWithLengthBetween0And1024 | None
    IntegrationId: Id | None
    IntegrationMethod: StringWithLengthBetween1And64 | None
    IntegrationResponseSelectionExpression: SelectionExpression | None
    IntegrationSubtype: StringWithLengthBetween1And128 | None
    IntegrationType: IntegrationType | None
    IntegrationUri: UriWithLengthBetween1And2048 | None
    PassthroughBehavior: PassthroughBehavior | None
    PayloadFormatVersion: StringWithLengthBetween1And64 | None
    RequestParameters: IntegrationParameters | None
    RequestTemplates: TemplateMap | None
    ResponseParameters: ResponseParameters | None
    TemplateSelectionExpression: SelectionExpression | None
    TimeoutInMillis: IntegerWithLengthBetween50And30000 | None
    TlsConfig: TlsConfig | None


class CreateIntegrationResponseInput(TypedDict, total=False):
    """Represents the input parameters for a CreateIntegrationResponse request."""

    ContentHandlingStrategy: ContentHandlingStrategy | None
    IntegrationResponseKey: SelectionKey
    ResponseParameters: IntegrationParameters | None
    ResponseTemplates: TemplateMap | None
    TemplateSelectionExpression: SelectionExpression | None


class CreateIntegrationResponseRequest(ServiceRequest):
    """Creates a new IntegrationResponse resource to represent an integration
    response.
    """

    ApiId: _string
    ContentHandlingStrategy: ContentHandlingStrategy | None
    IntegrationId: _string
    IntegrationResponseKey: SelectionKey
    ResponseParameters: IntegrationParameters | None
    ResponseTemplates: TemplateMap | None
    TemplateSelectionExpression: SelectionExpression | None


class CreateIntegrationResponseResponse(TypedDict, total=False):
    ContentHandlingStrategy: ContentHandlingStrategy | None
    IntegrationResponseId: Id | None
    IntegrationResponseKey: SelectionKey | None
    ResponseParameters: IntegrationParameters | None
    ResponseTemplates: TemplateMap | None
    TemplateSelectionExpression: SelectionExpression | None


class CreateModelInput(TypedDict, total=False):
    """Represents the input parameters for a CreateModel request."""

    ContentType: StringWithLengthBetween1And256 | None
    Description: StringWithLengthBetween0And1024 | None
    Name: StringWithLengthBetween1And128
    Schema: StringWithLengthBetween0And32K


class CreateModelRequest(ServiceRequest):
    """Creates a new Model."""

    ApiId: _string
    ContentType: StringWithLengthBetween1And256 | None
    Description: StringWithLengthBetween0And1024 | None
    Name: StringWithLengthBetween1And128
    Schema: StringWithLengthBetween0And32K


class CreateModelResponse(TypedDict, total=False):
    ContentType: StringWithLengthBetween1And256 | None
    Description: StringWithLengthBetween0And1024 | None
    ModelId: Id | None
    Name: StringWithLengthBetween1And128 | None
    Schema: StringWithLengthBetween0And32K | None


class CreatePortalProductRequest(ServiceRequest):
    """The request body for the post operation."""

    Description: _stringMin0Max1024 | None
    DisplayName: _stringMin1Max255
    Tags: Tags | None


class CreatePortalProductRequestContent(TypedDict, total=False):
    """Creates a portal product."""

    Description: _stringMin0Max1024 | None
    DisplayName: _stringMin1Max255
    Tags: Tags | None


_listOf__stringMin20Max2048 = list[_stringMin20Max2048]


class Section(TypedDict, total=False):
    """Contains the section name and list of product REST endpoints for a
    product.
    """

    ProductRestEndpointPageArns: _listOf__stringMin20Max2048
    SectionName: _string


_listOfSection = list[Section]


class DisplayOrder(TypedDict, total=False):
    """The display order."""

    Contents: _listOfSection | None
    OverviewPageArn: _stringMin20Max2048 | None
    ProductPageArns: _listOf__stringMin20Max2048 | None


class CreatePortalProductResponse(TypedDict, total=False):
    Description: _stringMin0Max1024 | None
    DisplayName: _stringMin1Max255 | None
    DisplayOrder: DisplayOrder | None
    LastModified: _timestampIso8601 | None
    PortalProductArn: _stringMin20Max2048 | None
    PortalProductId: _stringMin10Max30PatternAZ09 | None
    Tags: Tags | None


class CreatePortalProductResponseContent(TypedDict, total=False):
    """Creates a portal product."""

    Description: _stringMin0Max1024 | None
    DisplayName: _stringMin1Max255
    DisplayOrder: DisplayOrder | None
    LastModified: _timestampIso8601
    PortalProductArn: _stringMin20Max2048
    PortalProductId: _stringMin10Max30PatternAZ09
    Tags: Tags | None


class CustomColors(TypedDict, total=False):
    """Represents custom colors for a published portal."""

    AccentColor: _stringMin1Max16
    BackgroundColor: _stringMin1Max16
    ErrorValidationColor: _stringMin1Max16
    HeaderColor: _stringMin1Max16
    NavigationColor: _stringMin1Max16
    TextColor: _stringMin1Max16


class PortalTheme(TypedDict, total=False):
    """Defines the theme for a portal."""

    CustomColors: CustomColors
    LogoLastUploaded: _timestampIso8601 | None


class PortalContent(TypedDict, total=False):
    """Contains the content that is visible to portal consumers including the
    themes, display names, and description.
    """

    Description: _stringMin0Max1024 | None
    DisplayName: _stringMin3Max255
    Theme: PortalTheme


EndpointConfigurationRequest = TypedDict(
    "EndpointConfigurationRequest",
    {
        "AcmManaged": ACMManaged | None,
        "None": None_ | None,
    },
    total=False,
)


class CreatePortalRequest(ServiceRequest):
    """The request body for the post operation."""

    Authorization: Authorization
    EndpointConfiguration: EndpointConfigurationRequest
    IncludedPortalProductArns: _listOf__stringMin20Max2048 | None
    LogoUri: _stringMin0Max1092 | None
    PortalContent: PortalContent
    RumAppMonitorName: _stringMin0Max255 | None
    Tags: Tags | None


class CreatePortalRequestContent(TypedDict, total=False):
    """Creates a portal."""

    Authorization: Authorization
    EndpointConfiguration: EndpointConfigurationRequest
    IncludedPortalProductArns: _listOf__stringMin20Max2048 | None
    LogoUri: _stringMin0Max1092 | None
    PortalContent: PortalContent
    RumAppMonitorName: _stringMin0Max255 | None
    Tags: Tags | None


class StatusException(TypedDict, total=False):
    """Represents a StatusException."""

    Exception: _stringMin1Max256 | None
    Message: _stringMin1Max2048 | None


class EndpointConfigurationResponse(TypedDict, total=False):
    """Represents an endpoint configuration."""

    CertificateArn: _stringMin10Max2048 | None
    DomainName: _stringMin3Max256 | None
    PortalDefaultDomainName: _stringMin3Max256
    PortalDomainHostedZoneId: _stringMin1Max64


class CreatePortalResponse(TypedDict, total=False):
    Authorization: Authorization | None
    EndpointConfiguration: EndpointConfigurationResponse | None
    IncludedPortalProductArns: _listOf__stringMin20Max2048 | None
    LastModified: _timestampIso8601 | None
    LastPublished: _timestampIso8601 | None
    LastPublishedDescription: _stringMin0Max1024 | None
    PortalArn: _stringMin20Max2048 | None
    PortalContent: PortalContent | None
    PortalId: _stringMin10Max30PatternAZ09 | None
    PublishStatus: PublishStatus | None
    RumAppMonitorName: _stringMin0Max255 | None
    StatusException: StatusException | None
    Tags: Tags | None


class CreatePortalResponseContent(TypedDict, total=False):
    """Creates a portal."""

    Authorization: Authorization
    EndpointConfiguration: EndpointConfigurationResponse
    IncludedPortalProductArns: _listOf__stringMin20Max2048
    LastModified: _timestampIso8601
    LastPublished: _timestampIso8601 | None
    LastPublishedDescription: _stringMin0Max1024 | None
    PortalArn: _stringMin20Max2048
    PortalContent: PortalContent
    PortalId: _stringMin10Max30PatternAZ09
    PublishStatus: PublishStatus | None
    RumAppMonitorName: _stringMin0Max255 | None
    StatusException: StatusException | None
    Tags: Tags | None


class DisplayContent(TypedDict, total=False):
    """The content of the product page."""

    Body: _stringMin1Max32768
    Title: _stringMin1Max255


class CreateProductPageRequest(ServiceRequest):
    """The request body for the post operation."""

    DisplayContent: DisplayContent
    PortalProductId: _string


class CreateProductPageRequestContent(TypedDict, total=False):
    """Creates a product page."""

    DisplayContent: DisplayContent


class CreateProductPageResponse(TypedDict, total=False):
    DisplayContent: DisplayContent | None
    LastModified: _timestampIso8601 | None
    ProductPageArn: _stringMin20Max2048 | None
    ProductPageId: _stringMin10Max30PatternAZ09 | None


class CreateProductPageResponseContent(TypedDict, total=False):
    """Creates a product page."""

    DisplayContent: DisplayContent | None
    LastModified: _timestampIso8601
    ProductPageArn: _stringMin20Max2048
    ProductPageId: _stringMin10Max30PatternAZ09


class IdentifierParts(TypedDict, total=False):
    """The identifier parts of a product REST endpoint."""

    Method: _stringMin1Max20
    Path: _stringMin1Max4096
    RestApiId: _stringMin1Max50
    Stage: _stringMin1Max128


class RestEndpointIdentifier(TypedDict, total=False):
    """The REST API endpoint identifier."""

    IdentifierParts: IdentifierParts | None


class DisplayContentOverrides(TypedDict, total=False):
    """Contains any values that override the default configuration generated
    from API Gateway.
    """

    Body: _stringMin1Max32768 | None
    Endpoint: _stringMin1Max1024 | None
    OperationName: _stringMin1Max255 | None


EndpointDisplayContent = TypedDict(
    "EndpointDisplayContent",
    {
        "None": None_ | None,
        "Overrides": DisplayContentOverrides | None,
    },
    total=False,
)


class CreateProductRestEndpointPageRequest(ServiceRequest):
    """The request body for the post operation."""

    DisplayContent: EndpointDisplayContent | None
    PortalProductId: _string
    RestEndpointIdentifier: RestEndpointIdentifier
    TryItState: TryItState | None


class CreateProductRestEndpointPageRequestContent(TypedDict, total=False):
    """Creates a product REST endpoint page."""

    DisplayContent: EndpointDisplayContent | None
    RestEndpointIdentifier: RestEndpointIdentifier
    TryItState: TryItState | None


class EndpointDisplayContentResponse(TypedDict, total=False):
    """The product REST endpoint page."""

    Body: _stringMin1Max32768 | None
    Endpoint: _stringMin1Max1024
    OperationName: _stringMin1Max255 | None


class CreateProductRestEndpointPageResponse(TypedDict, total=False):
    DisplayContent: EndpointDisplayContentResponse | None
    LastModified: _timestampIso8601 | None
    ProductRestEndpointPageArn: _stringMin20Max2048 | None
    ProductRestEndpointPageId: _stringMin10Max30PatternAZ09 | None
    RestEndpointIdentifier: RestEndpointIdentifier | None
    Status: Status | None
    StatusException: StatusException | None
    TryItState: TryItState | None


class CreateProductRestEndpointPageResponseContent(TypedDict, total=False):
    """Creates a product REST endpoint page."""

    DisplayContent: EndpointDisplayContentResponse
    LastModified: _timestampIso8601
    ProductRestEndpointPageArn: _stringMin20Max2048
    ProductRestEndpointPageId: _stringMin10Max30PatternAZ09
    RestEndpointIdentifier: RestEndpointIdentifier
    Status: Status
    StatusException: StatusException | None
    TryItState: TryItState


class ParameterConstraints(TypedDict, total=False):
    """Validation constraints imposed on parameters of a request (path, query
    string, headers).
    """

    Required: _boolean | None


RouteParameters = dict[_string, ParameterConstraints]
RouteModels = dict[_string, StringWithLengthBetween1And128]


class CreateRouteInput(TypedDict, total=False):
    """Represents the input parameters for a CreateRoute request."""

    ApiKeyRequired: _boolean | None
    AuthorizationScopes: AuthorizationScopes | None
    AuthorizationType: AuthorizationType | None
    AuthorizerId: Id | None
    ModelSelectionExpression: SelectionExpression | None
    OperationName: StringWithLengthBetween1And64 | None
    RequestModels: RouteModels | None
    RequestParameters: RouteParameters | None
    RouteKey: SelectionKey
    RouteResponseSelectionExpression: SelectionExpression | None
    Target: StringWithLengthBetween1And128 | None


class CreateRouteRequest(ServiceRequest):
    """Creates a new Route resource to represent a route."""

    ApiId: _string
    ApiKeyRequired: _boolean | None
    AuthorizationScopes: AuthorizationScopes | None
    AuthorizationType: AuthorizationType | None
    AuthorizerId: Id | None
    ModelSelectionExpression: SelectionExpression | None
    OperationName: StringWithLengthBetween1And64 | None
    RequestModels: RouteModels | None
    RequestParameters: RouteParameters | None
    RouteKey: SelectionKey
    RouteResponseSelectionExpression: SelectionExpression | None
    Target: StringWithLengthBetween1And128 | None


class CreateRouteResult(TypedDict, total=False):
    ApiGatewayManaged: _boolean | None
    ApiKeyRequired: _boolean | None
    AuthorizationScopes: AuthorizationScopes | None
    AuthorizationType: AuthorizationType | None
    AuthorizerId: Id | None
    ModelSelectionExpression: SelectionExpression | None
    OperationName: StringWithLengthBetween1And64 | None
    RequestModels: RouteModels | None
    RequestParameters: RouteParameters | None
    RouteId: Id | None
    RouteKey: SelectionKey | None
    RouteResponseSelectionExpression: SelectionExpression | None
    Target: StringWithLengthBetween1And128 | None


class CreateRouteResponseInput(TypedDict, total=False):
    """Represents the input parameters for an CreateRouteResponse request."""

    ModelSelectionExpression: SelectionExpression | None
    ResponseModels: RouteModels | None
    ResponseParameters: RouteParameters | None
    RouteResponseKey: SelectionKey


class CreateRouteResponseRequest(ServiceRequest):
    """Creates a new RouteResponse resource to represent a route response."""

    ApiId: _string
    ModelSelectionExpression: SelectionExpression | None
    ResponseModels: RouteModels | None
    ResponseParameters: RouteParameters | None
    RouteId: _string
    RouteResponseKey: SelectionKey


class CreateRouteResponseResponse(TypedDict, total=False):
    ModelSelectionExpression: SelectionExpression | None
    ResponseModels: RouteModels | None
    ResponseParameters: RouteParameters | None
    RouteResponseId: Id | None
    RouteResponseKey: SelectionKey | None


class RoutingRuleMatchHeaderValue(TypedDict, total=False):
    """Represents a MatchHeaderValue."""

    Header: SelectionKey
    ValueGlob: SelectionExpression


_listOfRoutingRuleMatchHeaderValue = list[RoutingRuleMatchHeaderValue]


class RoutingRuleMatchHeaders(TypedDict, total=False):
    """Represents a MatchHeaders condition."""

    AnyOf: _listOfRoutingRuleMatchHeaderValue


_listOfSelectionKey = list[SelectionKey]


class RoutingRuleMatchBasePaths(TypedDict, total=False):
    """Represents a MatchBasePaths condition."""

    AnyOf: _listOfSelectionKey


class RoutingRuleCondition(TypedDict, total=False):
    """Represents a routing rule condition."""

    MatchBasePaths: RoutingRuleMatchBasePaths | None
    MatchHeaders: RoutingRuleMatchHeaders | None


_listOfRoutingRuleCondition = list[RoutingRuleCondition]


class RoutingRuleActionInvokeApi(TypedDict, total=False):
    """Represents an InvokeApi action."""

    ApiId: Id
    Stage: StringWithLengthBetween1And128
    StripBasePath: _boolean | None


class RoutingRuleAction(TypedDict, total=False):
    """The routing rule action."""

    InvokeApi: RoutingRuleActionInvokeApi


_listOfRoutingRuleAction = list[RoutingRuleAction]


class CreateRoutingRuleRequest(ServiceRequest):
    Actions: _listOfRoutingRuleAction
    Conditions: _listOfRoutingRuleCondition
    DomainName: _string
    DomainNameId: _string | None
    Priority: RoutingRulePriority


class CreateRoutingRuleResponse(TypedDict, total=False):
    Actions: _listOfRoutingRuleAction | None
    Conditions: _listOfRoutingRuleCondition | None
    Priority: RoutingRulePriority | None
    RoutingRuleArn: Arn | None
    RoutingRuleId: Id | None


StageVariablesMap = dict[_string, StringWithLengthBetween0And2048]


class RouteSettings(TypedDict, total=False):
    """Represents a collection of route settings."""

    DataTraceEnabled: _boolean | None
    DetailedMetricsEnabled: _boolean | None
    LoggingLevel: LoggingLevel | None
    ThrottlingBurstLimit: _integer | None
    ThrottlingRateLimit: _double | None


RouteSettingsMap = dict[_string, RouteSettings]


class CreateStageInput(TypedDict, total=False):
    """Represents the input parameters for a CreateStage request."""

    AccessLogSettings: AccessLogSettings | None
    AutoDeploy: _boolean | None
    ClientCertificateId: Id | None
    DefaultRouteSettings: RouteSettings | None
    DeploymentId: Id | None
    Description: StringWithLengthBetween0And1024 | None
    RouteSettings: RouteSettingsMap | None
    StageName: StringWithLengthBetween1And128
    StageVariables: StageVariablesMap | None
    Tags: Tags | None


class CreateStageRequest(ServiceRequest):
    """Creates a new Stage resource to represent a stage."""

    AccessLogSettings: AccessLogSettings | None
    ApiId: _string
    AutoDeploy: _boolean | None
    ClientCertificateId: Id | None
    DefaultRouteSettings: RouteSettings | None
    DeploymentId: Id | None
    Description: StringWithLengthBetween0And1024 | None
    RouteSettings: RouteSettingsMap | None
    StageName: StringWithLengthBetween1And128
    StageVariables: StageVariablesMap | None
    Tags: Tags | None


class CreateStageResponse(TypedDict, total=False):
    AccessLogSettings: AccessLogSettings | None
    ApiGatewayManaged: _boolean | None
    AutoDeploy: _boolean | None
    ClientCertificateId: Id | None
    CreatedDate: _timestampIso8601 | None
    DefaultRouteSettings: RouteSettings | None
    DeploymentId: Id | None
    Description: StringWithLengthBetween0And1024 | None
    LastDeploymentStatusMessage: _string | None
    LastUpdatedDate: _timestampIso8601 | None
    RouteSettings: RouteSettingsMap | None
    StageName: StringWithLengthBetween1And128 | None
    StageVariables: StageVariablesMap | None
    Tags: Tags | None


SubnetIdList = list[_string]
SecurityGroupIdList = list[_string]


class CreateVpcLinkInput(TypedDict, total=False):
    """Represents the input parameters for a CreateVpcLink request."""

    Name: StringWithLengthBetween1And128
    SecurityGroupIds: SecurityGroupIdList | None
    SubnetIds: SubnetIdList
    Tags: Tags | None


class CreateVpcLinkRequest(ServiceRequest):
    """Creates a VPC link"""

    Name: StringWithLengthBetween1And128
    SecurityGroupIds: SecurityGroupIdList | None
    SubnetIds: SubnetIdList
    Tags: Tags | None


class CreateVpcLinkResponse(TypedDict, total=False):
    CreatedDate: _timestampIso8601 | None
    Name: StringWithLengthBetween1And128 | None
    SecurityGroupIds: SecurityGroupIdList | None
    SubnetIds: SubnetIdList | None
    Tags: Tags | None
    VpcLinkId: Id | None
    VpcLinkStatus: VpcLinkStatus | None
    VpcLinkStatusMessage: StringWithLengthBetween0And1024 | None
    VpcLinkVersion: VpcLinkVersion | None


class DeleteAccessLogSettingsRequest(ServiceRequest):
    ApiId: _string
    StageName: _string


class DeleteApiMappingRequest(ServiceRequest):
    ApiMappingId: _string
    DomainName: _string


class DeleteApiRequest(ServiceRequest):
    ApiId: _string


class DeleteAuthorizerRequest(ServiceRequest):
    ApiId: _string
    AuthorizerId: _string


class DeleteCorsConfigurationRequest(ServiceRequest):
    ApiId: _string


class DeleteDeploymentRequest(ServiceRequest):
    ApiId: _string
    DeploymentId: _string


class DeleteDomainNameRequest(ServiceRequest):
    DomainName: _string


class DeleteIntegrationRequest(ServiceRequest):
    ApiId: _string
    IntegrationId: _string


class DeleteIntegrationResponseRequest(ServiceRequest):
    ApiId: _string
    IntegrationId: _string
    IntegrationResponseId: _string


class DeleteModelRequest(ServiceRequest):
    ApiId: _string
    ModelId: _string


class DeletePortalProductRequest(ServiceRequest):
    PortalProductId: _string


class DeletePortalProductSharingPolicyRequest(ServiceRequest):
    PortalProductId: _string


class DeletePortalRequest(ServiceRequest):
    PortalId: _string


class DeleteProductPageRequest(ServiceRequest):
    PortalProductId: _string
    ProductPageId: _string


class DeleteProductRestEndpointPageRequest(ServiceRequest):
    PortalProductId: _string
    ProductRestEndpointPageId: _string


class DeleteRouteRequest(ServiceRequest):
    ApiId: _string
    RouteId: _string


class DeleteRouteRequestParameterRequest(ServiceRequest):
    ApiId: _string
    RequestParameterKey: _string
    RouteId: _string


class DeleteRouteResponseRequest(ServiceRequest):
    ApiId: _string
    RouteId: _string
    RouteResponseId: _string


class DeleteRouteSettingsRequest(ServiceRequest):
    ApiId: _string
    RouteKey: _string
    StageName: _string


class DeleteRoutingRuleRequest(ServiceRequest):
    DomainName: _string
    DomainNameId: _string | None
    RoutingRuleId: _string


class DeleteStageRequest(ServiceRequest):
    ApiId: _string
    StageName: _string


class DeleteVpcLinkRequest(ServiceRequest):
    VpcLinkId: _string


class DeleteVpcLinkResponse(TypedDict, total=False):
    pass


class Deployment(TypedDict, total=False):
    """An immutable representation of an API that can be called by users. A
    Deployment must be associated with a Stage for it to be callable over
    the internet.
    """

    AutoDeployed: _boolean | None
    CreatedDate: _timestampIso8601 | None
    DeploymentId: Id | None
    DeploymentStatus: DeploymentStatus | None
    DeploymentStatusMessage: _string | None
    Description: StringWithLengthBetween0And1024 | None


_listOfDeployment = list[Deployment]


class Deployments(TypedDict, total=False):
    """A collection resource that contains zero or more references to your
    existing deployments, and links that guide you on how to interact with
    your collection. The collection offers a paginated view of the contained
    deployments.
    """

    Items: _listOfDeployment | None
    NextToken: NextToken | None


class DisablePortalRequest(ServiceRequest):
    PortalId: _string


class DomainName(TypedDict, total=False):
    """Represents a domain name."""

    ApiMappingSelectionExpression: SelectionExpression | None
    DomainName: StringWithLengthBetween1And512
    DomainNameArn: Arn | None
    DomainNameConfigurations: DomainNameConfigurations | None
    MutualTlsAuthentication: MutualTlsAuthentication | None
    RoutingMode: RoutingMode | None
    Tags: Tags | None


_listOfDomainName = list[DomainName]


class DomainNames(TypedDict, total=False):
    """Represents a collection of domain names."""

    Items: _listOfDomainName | None
    NextToken: NextToken | None


class ExportApiRequest(ServiceRequest):
    ApiId: _string
    ExportVersion: _string | None
    IncludeExtensions: _boolean | None
    OutputType: _string
    Specification: _string
    StageName: _string | None


ExportedApi = bytes


class ExportApiResponse(TypedDict, total=False):
    body: ExportedApi | IO[ExportedApi] | Iterable[ExportedApi] | None


class ResetAuthorizersCacheRequest(ServiceRequest):
    ApiId: _string
    StageName: _string


class GetApiMappingRequest(ServiceRequest):
    ApiMappingId: _string
    DomainName: _string


class GetApiMappingResponse(TypedDict, total=False):
    ApiId: Id | None
    ApiMappingId: Id | None
    ApiMappingKey: SelectionKey | None
    Stage: StringWithLengthBetween1And128 | None


class GetApiMappingsRequest(ServiceRequest):
    DomainName: _string
    MaxResults: _string | None
    NextToken: _string | None


class GetApiMappingsResponse(TypedDict, total=False):
    Items: _listOfApiMapping | None
    NextToken: NextToken | None


class GetApiRequest(ServiceRequest):
    ApiId: _string


class GetApiResponse(TypedDict, total=False):
    ApiEndpoint: _string | None
    ApiGatewayManaged: _boolean | None
    ApiId: Id | None
    ApiKeySelectionExpression: SelectionExpression | None
    CorsConfiguration: Cors | None
    CreatedDate: _timestampIso8601 | None
    Description: StringWithLengthBetween0And1024 | None
    DisableSchemaValidation: _boolean | None
    DisableExecuteApiEndpoint: _boolean | None
    ImportInfo: _listOf__string | None
    IpAddressType: IpAddressType | None
    Name: StringWithLengthBetween1And128 | None
    ProtocolType: ProtocolType | None
    RouteSelectionExpression: SelectionExpression | None
    Tags: Tags | None
    Version: StringWithLengthBetween1And64 | None
    Warnings: _listOf__string | None


class GetApisRequest(ServiceRequest):
    MaxResults: _string | None
    NextToken: _string | None


class GetApisResponse(TypedDict, total=False):
    Items: _listOfApi | None
    NextToken: NextToken | None


class GetAuthorizerRequest(ServiceRequest):
    ApiId: _string
    AuthorizerId: _string


class GetAuthorizerResponse(TypedDict, total=False):
    AuthorizerCredentialsArn: Arn | None
    AuthorizerId: Id | None
    AuthorizerPayloadFormatVersion: StringWithLengthBetween1And64 | None
    AuthorizerResultTtlInSeconds: IntegerWithLengthBetween0And3600 | None
    AuthorizerType: AuthorizerType | None
    AuthorizerUri: UriWithLengthBetween1And2048 | None
    EnableSimpleResponses: _boolean | None
    IdentitySource: IdentitySourceList | None
    IdentityValidationExpression: StringWithLengthBetween0And1024 | None
    JwtConfiguration: JWTConfiguration | None
    Name: StringWithLengthBetween1And128 | None


class GetAuthorizersRequest(ServiceRequest):
    ApiId: _string
    MaxResults: _string | None
    NextToken: _string | None


class GetAuthorizersResponse(TypedDict, total=False):
    Items: _listOfAuthorizer | None
    NextToken: NextToken | None


class GetDeploymentRequest(ServiceRequest):
    ApiId: _string
    DeploymentId: _string


class GetDeploymentResponse(TypedDict, total=False):
    AutoDeployed: _boolean | None
    CreatedDate: _timestampIso8601 | None
    DeploymentId: Id | None
    DeploymentStatus: DeploymentStatus | None
    DeploymentStatusMessage: _string | None
    Description: StringWithLengthBetween0And1024 | None


class GetDeploymentsRequest(ServiceRequest):
    ApiId: _string
    MaxResults: _string | None
    NextToken: _string | None


class GetDeploymentsResponse(TypedDict, total=False):
    Items: _listOfDeployment | None
    NextToken: NextToken | None


class GetDomainNameRequest(ServiceRequest):
    DomainName: _string


class GetDomainNameResponse(TypedDict, total=False):
    ApiMappingSelectionExpression: SelectionExpression | None
    DomainName: StringWithLengthBetween1And512 | None
    DomainNameArn: Arn | None
    DomainNameConfigurations: DomainNameConfigurations | None
    MutualTlsAuthentication: MutualTlsAuthentication | None
    RoutingMode: RoutingMode | None
    Tags: Tags | None


class GetDomainNamesRequest(ServiceRequest):
    MaxResults: _string | None
    NextToken: _string | None


class GetDomainNamesResponse(TypedDict, total=False):
    Items: _listOfDomainName | None
    NextToken: NextToken | None


class GetIntegrationRequest(ServiceRequest):
    ApiId: _string
    IntegrationId: _string


class GetIntegrationResult(TypedDict, total=False):
    ApiGatewayManaged: _boolean | None
    ConnectionId: StringWithLengthBetween1And1024 | None
    ConnectionType: ConnectionType | None
    ContentHandlingStrategy: ContentHandlingStrategy | None
    CredentialsArn: Arn | None
    Description: StringWithLengthBetween0And1024 | None
    IntegrationId: Id | None
    IntegrationMethod: StringWithLengthBetween1And64 | None
    IntegrationResponseSelectionExpression: SelectionExpression | None
    IntegrationSubtype: StringWithLengthBetween1And128 | None
    IntegrationType: IntegrationType | None
    IntegrationUri: UriWithLengthBetween1And2048 | None
    PassthroughBehavior: PassthroughBehavior | None
    PayloadFormatVersion: StringWithLengthBetween1And64 | None
    RequestParameters: IntegrationParameters | None
    RequestTemplates: TemplateMap | None
    ResponseParameters: ResponseParameters | None
    TemplateSelectionExpression: SelectionExpression | None
    TimeoutInMillis: IntegerWithLengthBetween50And30000 | None
    TlsConfig: TlsConfig | None


class GetIntegrationResponseRequest(ServiceRequest):
    ApiId: _string
    IntegrationId: _string
    IntegrationResponseId: _string


class GetIntegrationResponseResponse(TypedDict, total=False):
    ContentHandlingStrategy: ContentHandlingStrategy | None
    IntegrationResponseId: Id | None
    IntegrationResponseKey: SelectionKey | None
    ResponseParameters: IntegrationParameters | None
    ResponseTemplates: TemplateMap | None
    TemplateSelectionExpression: SelectionExpression | None


class GetIntegrationResponsesRequest(ServiceRequest):
    ApiId: _string
    IntegrationId: _string
    MaxResults: _string | None
    NextToken: _string | None


class IntegrationResponse(TypedDict, total=False):
    """Represents an integration response."""

    ContentHandlingStrategy: ContentHandlingStrategy | None
    IntegrationResponseId: Id | None
    IntegrationResponseKey: SelectionKey
    ResponseParameters: IntegrationParameters | None
    ResponseTemplates: TemplateMap | None
    TemplateSelectionExpression: SelectionExpression | None


_listOfIntegrationResponse = list[IntegrationResponse]


class GetIntegrationResponsesResponse(TypedDict, total=False):
    Items: _listOfIntegrationResponse | None
    NextToken: NextToken | None


class GetIntegrationsRequest(ServiceRequest):
    ApiId: _string
    MaxResults: _string | None
    NextToken: _string | None


class Integration(TypedDict, total=False):
    """Represents an integration."""

    ApiGatewayManaged: _boolean | None
    ConnectionId: StringWithLengthBetween1And1024 | None
    ConnectionType: ConnectionType | None
    ContentHandlingStrategy: ContentHandlingStrategy | None
    CredentialsArn: Arn | None
    Description: StringWithLengthBetween0And1024 | None
    IntegrationId: Id | None
    IntegrationMethod: StringWithLengthBetween1And64 | None
    IntegrationResponseSelectionExpression: SelectionExpression | None
    IntegrationSubtype: StringWithLengthBetween1And128 | None
    IntegrationType: IntegrationType | None
    IntegrationUri: UriWithLengthBetween1And2048 | None
    PassthroughBehavior: PassthroughBehavior | None
    PayloadFormatVersion: StringWithLengthBetween1And64 | None
    RequestParameters: IntegrationParameters | None
    RequestTemplates: TemplateMap | None
    ResponseParameters: ResponseParameters | None
    TemplateSelectionExpression: SelectionExpression | None
    TimeoutInMillis: IntegerWithLengthBetween50And30000 | None
    TlsConfig: TlsConfig | None


_listOfIntegration = list[Integration]


class GetIntegrationsResponse(TypedDict, total=False):
    Items: _listOfIntegration | None
    NextToken: NextToken | None


class GetModelRequest(ServiceRequest):
    ApiId: _string
    ModelId: _string


class GetModelResponse(TypedDict, total=False):
    ContentType: StringWithLengthBetween1And256 | None
    Description: StringWithLengthBetween0And1024 | None
    ModelId: Id | None
    Name: StringWithLengthBetween1And128 | None
    Schema: StringWithLengthBetween0And32K | None


class GetModelTemplateRequest(ServiceRequest):
    ApiId: _string
    ModelId: _string


class GetModelTemplateResponse(TypedDict, total=False):
    Value: _string | None


class GetModelsRequest(ServiceRequest):
    ApiId: _string
    MaxResults: _string | None
    NextToken: _string | None


class Model(TypedDict, total=False):
    """Represents a data model for an API. Supported only for WebSocket APIs.
    See `Create Models and Mapping Templates for Request and Response
    Mappings <https://docs.aws.amazon.com/apigateway/latest/developerguide/models-mappings.html>`__.
    """

    ContentType: StringWithLengthBetween1And256 | None
    Description: StringWithLengthBetween0And1024 | None
    ModelId: Id | None
    Name: StringWithLengthBetween1And128
    Schema: StringWithLengthBetween0And32K | None


_listOfModel = list[Model]


class GetModelsResponse(TypedDict, total=False):
    Items: _listOfModel | None
    NextToken: NextToken | None


class GetPortalProductRequest(ServiceRequest):
    PortalProductId: _string
    ResourceOwnerAccountId: _string | None


class GetPortalProductResponse(TypedDict, total=False):
    Description: _stringMin0Max1024 | None
    DisplayName: _stringMin1Max255 | None
    DisplayOrder: DisplayOrder | None
    LastModified: _timestampIso8601 | None
    PortalProductArn: _stringMin20Max2048 | None
    PortalProductId: _stringMin10Max30PatternAZ09 | None
    Tags: Tags | None


class GetPortalProductResponseContent(TypedDict, total=False):
    """Gets a portal product."""

    Description: _stringMin0Max1024
    DisplayName: _stringMin1Max255
    DisplayOrder: DisplayOrder
    LastModified: _timestampIso8601
    PortalProductArn: _stringMin20Max2048
    PortalProductId: _stringMin10Max30PatternAZ09
    Tags: Tags | None


class GetPortalProductSharingPolicyRequest(ServiceRequest):
    PortalProductId: _string


class GetPortalProductSharingPolicyResponse(TypedDict, total=False):
    PolicyDocument: _stringMin1Max307200 | None
    PortalProductId: _stringMin10Max30PatternAZ09 | None


class GetPortalProductSharingPolicyResponseContent(TypedDict, total=False):
    """Gets a product sharing policy."""

    PolicyDocument: _stringMin1Max307200
    PortalProductId: _stringMin10Max30PatternAZ09


class GetPortalRequest(ServiceRequest):
    PortalId: _string


class Preview(TypedDict, total=False):
    """Contains the preview status and preview URL."""

    PreviewStatus: PreviewStatus
    PreviewUrl: _string | None
    StatusException: StatusException | None


class GetPortalResponse(TypedDict, total=False):
    Authorization: Authorization | None
    EndpointConfiguration: EndpointConfigurationResponse | None
    IncludedPortalProductArns: _listOf__stringMin20Max2048 | None
    LastModified: _timestampIso8601 | None
    LastPublished: _timestampIso8601 | None
    LastPublishedDescription: _stringMin0Max1024 | None
    PortalArn: _stringMin20Max2048 | None
    PortalContent: PortalContent | None
    PortalId: _stringMin10Max30PatternAZ09 | None
    Preview: Preview | None
    PublishStatus: PublishStatus | None
    RumAppMonitorName: _stringMin0Max255 | None
    StatusException: StatusException | None
    Tags: Tags | None


class GetPortalResponseContent(TypedDict, total=False):
    """Gets a portal."""

    Authorization: Authorization
    EndpointConfiguration: EndpointConfigurationResponse
    IncludedPortalProductArns: _listOf__stringMin20Max2048
    LastModified: _timestampIso8601
    LastPublished: _timestampIso8601 | None
    LastPublishedDescription: _stringMin0Max1024 | None
    PortalArn: _stringMin20Max2048
    PortalContent: PortalContent
    PortalId: _stringMin10Max30PatternAZ09
    Preview: Preview | None
    PublishStatus: PublishStatus | None
    RumAppMonitorName: _stringMin0Max255 | None
    StatusException: StatusException | None
    Tags: Tags | None


class GetProductPageRequest(ServiceRequest):
    PortalProductId: _string
    ProductPageId: _string
    ResourceOwnerAccountId: _string | None


class GetProductPageResponse(TypedDict, total=False):
    DisplayContent: DisplayContent | None
    LastModified: _timestampIso8601 | None
    ProductPageArn: _stringMin20Max2048 | None
    ProductPageId: _stringMin10Max30PatternAZ09 | None


class GetProductPageResponseContent(TypedDict, total=False):
    """Gets a product page."""

    DisplayContent: DisplayContent
    LastModified: _timestampIso8601
    ProductPageArn: _stringMin20Max2048
    ProductPageId: _stringMin10Max30PatternAZ09


class GetProductRestEndpointPageRequest(ServiceRequest):
    IncludeRawDisplayContent: _string | None
    PortalProductId: _string
    ProductRestEndpointPageId: _string
    ResourceOwnerAccountId: _string | None


class GetProductRestEndpointPageResponse(TypedDict, total=False):
    DisplayContent: EndpointDisplayContentResponse | None
    LastModified: _timestampIso8601 | None
    ProductRestEndpointPageArn: _stringMin20Max2048 | None
    ProductRestEndpointPageId: _stringMin10Max30PatternAZ09 | None
    RawDisplayContent: _string | None
    RestEndpointIdentifier: RestEndpointIdentifier | None
    Status: Status | None
    StatusException: StatusException | None
    TryItState: TryItState | None


class GetProductRestEndpointPageResponseContent(TypedDict, total=False):
    """Gets a product REST endpoint page."""

    DisplayContent: EndpointDisplayContentResponse
    LastModified: _timestampIso8601
    ProductRestEndpointPageArn: _stringMin20Max2048
    ProductRestEndpointPageId: _stringMin10Max30PatternAZ09
    RawDisplayContent: _string | None
    RestEndpointIdentifier: RestEndpointIdentifier
    Status: Status
    StatusException: StatusException | None
    TryItState: TryItState


class GetRouteRequest(ServiceRequest):
    ApiId: _string
    RouteId: _string


class GetRouteResult(TypedDict, total=False):
    ApiGatewayManaged: _boolean | None
    ApiKeyRequired: _boolean | None
    AuthorizationScopes: AuthorizationScopes | None
    AuthorizationType: AuthorizationType | None
    AuthorizerId: Id | None
    ModelSelectionExpression: SelectionExpression | None
    OperationName: StringWithLengthBetween1And64 | None
    RequestModels: RouteModels | None
    RequestParameters: RouteParameters | None
    RouteId: Id | None
    RouteKey: SelectionKey | None
    RouteResponseSelectionExpression: SelectionExpression | None
    Target: StringWithLengthBetween1And128 | None


class GetRouteResponseRequest(ServiceRequest):
    ApiId: _string
    RouteId: _string
    RouteResponseId: _string


class GetRouteResponseResponse(TypedDict, total=False):
    ModelSelectionExpression: SelectionExpression | None
    ResponseModels: RouteModels | None
    ResponseParameters: RouteParameters | None
    RouteResponseId: Id | None
    RouteResponseKey: SelectionKey | None


class GetRouteResponsesRequest(ServiceRequest):
    ApiId: _string
    MaxResults: _string | None
    NextToken: _string | None
    RouteId: _string


class RouteResponse(TypedDict, total=False):
    """Represents a route response."""

    ModelSelectionExpression: SelectionExpression | None
    ResponseModels: RouteModels | None
    ResponseParameters: RouteParameters | None
    RouteResponseId: Id | None
    RouteResponseKey: SelectionKey


_listOfRouteResponse = list[RouteResponse]


class GetRouteResponsesResponse(TypedDict, total=False):
    Items: _listOfRouteResponse | None
    NextToken: NextToken | None


class GetRoutesRequest(ServiceRequest):
    ApiId: _string
    MaxResults: _string | None
    NextToken: _string | None


class ListRoutingRulesRequest(ServiceRequest):
    DomainName: _string
    DomainNameId: _string | None
    MaxResults: MaxResults | None
    NextToken: _string | None


class RoutingRule(TypedDict, total=False):
    """Represents a routing rule."""

    Actions: _listOfRoutingRuleAction | None
    Conditions: _listOfRoutingRuleCondition | None
    Priority: RoutingRulePriority | None
    RoutingRuleArn: Arn | None
    RoutingRuleId: Id | None


_listOfRoutingRule = list[RoutingRule]


class ListRoutingRulesResponse(TypedDict, total=False):
    NextToken: NextToken | None
    RoutingRules: _listOfRoutingRule | None


class Route(TypedDict, total=False):
    """Represents a route."""

    ApiGatewayManaged: _boolean | None
    ApiKeyRequired: _boolean | None
    AuthorizationScopes: AuthorizationScopes | None
    AuthorizationType: AuthorizationType | None
    AuthorizerId: Id | None
    ModelSelectionExpression: SelectionExpression | None
    OperationName: StringWithLengthBetween1And64 | None
    RequestModels: RouteModels | None
    RequestParameters: RouteParameters | None
    RouteId: Id | None
    RouteKey: SelectionKey
    RouteResponseSelectionExpression: SelectionExpression | None
    Target: StringWithLengthBetween1And128 | None


_listOfRoute = list[Route]


class GetRoutesResponse(TypedDict, total=False):
    Items: _listOfRoute | None
    NextToken: NextToken | None


class GetRoutingRuleRequest(ServiceRequest):
    DomainName: _string
    DomainNameId: _string | None
    RoutingRuleId: _string


class GetRoutingRuleResponse(TypedDict, total=False):
    Actions: _listOfRoutingRuleAction | None
    Conditions: _listOfRoutingRuleCondition | None
    Priority: RoutingRulePriority | None
    RoutingRuleArn: Arn | None
    RoutingRuleId: Id | None


class GetStageRequest(ServiceRequest):
    ApiId: _string
    StageName: _string


class GetStageResponse(TypedDict, total=False):
    AccessLogSettings: AccessLogSettings | None
    ApiGatewayManaged: _boolean | None
    AutoDeploy: _boolean | None
    ClientCertificateId: Id | None
    CreatedDate: _timestampIso8601 | None
    DefaultRouteSettings: RouteSettings | None
    DeploymentId: Id | None
    Description: StringWithLengthBetween0And1024 | None
    LastDeploymentStatusMessage: _string | None
    LastUpdatedDate: _timestampIso8601 | None
    RouteSettings: RouteSettingsMap | None
    StageName: StringWithLengthBetween1And128 | None
    StageVariables: StageVariablesMap | None
    Tags: Tags | None


class GetStagesRequest(ServiceRequest):
    ApiId: _string
    MaxResults: _string | None
    NextToken: _string | None


class Stage(TypedDict, total=False):
    """Represents an API stage."""

    AccessLogSettings: AccessLogSettings | None
    ApiGatewayManaged: _boolean | None
    AutoDeploy: _boolean | None
    ClientCertificateId: Id | None
    CreatedDate: _timestampIso8601 | None
    DefaultRouteSettings: RouteSettings | None
    DeploymentId: Id | None
    Description: StringWithLengthBetween0And1024 | None
    LastDeploymentStatusMessage: _string | None
    LastUpdatedDate: _timestampIso8601 | None
    RouteSettings: RouteSettingsMap | None
    StageName: StringWithLengthBetween1And128
    StageVariables: StageVariablesMap | None
    Tags: Tags | None


_listOfStage = list[Stage]


class GetStagesResponse(TypedDict, total=False):
    Items: _listOfStage | None
    NextToken: NextToken | None


class GetTagsRequest(ServiceRequest):
    ResourceArn: _string


class GetTagsResponse(TypedDict, total=False):
    Tags: Tags | None


class GetVpcLinkRequest(ServiceRequest):
    VpcLinkId: _string


class GetVpcLinkResponse(TypedDict, total=False):
    CreatedDate: _timestampIso8601 | None
    Name: StringWithLengthBetween1And128 | None
    SecurityGroupIds: SecurityGroupIdList | None
    SubnetIds: SubnetIdList | None
    Tags: Tags | None
    VpcLinkId: Id | None
    VpcLinkStatus: VpcLinkStatus | None
    VpcLinkStatusMessage: StringWithLengthBetween0And1024 | None
    VpcLinkVersion: VpcLinkVersion | None


class GetVpcLinksRequest(ServiceRequest):
    MaxResults: _string | None
    NextToken: _string | None


class VpcLink(TypedDict, total=False):
    """Represents a VPC link."""

    CreatedDate: _timestampIso8601 | None
    Name: StringWithLengthBetween1And128
    SecurityGroupIds: SecurityGroupIdList
    SubnetIds: SubnetIdList
    Tags: Tags | None
    VpcLinkId: Id
    VpcLinkStatus: VpcLinkStatus | None
    VpcLinkStatusMessage: StringWithLengthBetween0And1024 | None
    VpcLinkVersion: VpcLinkVersion | None


_listOfVpcLink = list[VpcLink]


class GetVpcLinksResponse(TypedDict, total=False):
    Items: _listOfVpcLink | None
    NextToken: NextToken | None


class ImportApiInput(TypedDict, total=False):
    """Represents the input to ImportAPI. Supported only for HTTP APIs."""

    Body: _string


class ImportApiRequest(ServiceRequest):
    Basepath: _string | None
    Body: _string
    FailOnWarnings: _boolean | None


class ImportApiResponse(TypedDict, total=False):
    ApiEndpoint: _string | None
    ApiGatewayManaged: _boolean | None
    ApiId: Id | None
    ApiKeySelectionExpression: SelectionExpression | None
    CorsConfiguration: Cors | None
    CreatedDate: _timestampIso8601 | None
    Description: StringWithLengthBetween0And1024 | None
    DisableSchemaValidation: _boolean | None
    DisableExecuteApiEndpoint: _boolean | None
    ImportInfo: _listOf__string | None
    IpAddressType: IpAddressType | None
    Name: StringWithLengthBetween1And128 | None
    ProtocolType: ProtocolType | None
    RouteSelectionExpression: SelectionExpression | None
    Tags: Tags | None
    Version: StringWithLengthBetween1And64 | None
    Warnings: _listOf__string | None


class IntegrationResponses(TypedDict, total=False):
    """Represents a collection of integration responses."""

    Items: _listOfIntegrationResponse | None
    NextToken: NextToken | None


class Integrations(TypedDict, total=False):
    """Represents a collection of integrations."""

    Items: _listOfIntegration | None
    NextToken: NextToken | None


class LimitExceededException(TypedDict, total=False):
    """A limit has been exceeded. See the accompanying error message for
    details.
    """

    LimitType: _string | None
    Message: _string | None


class LimitExceededExceptionResponseContent(TypedDict, total=False):
    """The response content for limit exceeded exception."""

    LimitType: _string | None
    Message: _string | None


class ListPortalProductsRequest(ServiceRequest):
    MaxResults: _string | None
    NextToken: _string | None
    ResourceOwner: _string | None


class PortalProductSummary(TypedDict, total=False):
    """Represents a portal product."""

    Description: _stringMin0Max1024
    DisplayName: _stringMin1Max255
    LastModified: _timestampIso8601
    PortalProductArn: _stringMin20Max2048
    PortalProductId: _stringMin10Max30PatternAZ09
    Tags: Tags | None


_listOfPortalProductSummary = list[PortalProductSummary]


class ListPortalProductsResponse(TypedDict, total=False):
    Items: _listOfPortalProductSummary | None
    NextToken: _stringMin1Max2048 | None


class ListPortalProductsResponseContent(TypedDict, total=False):
    """Lists portal products."""

    Items: _listOfPortalProductSummary | None
    NextToken: _stringMin1Max2048 | None


class ListPortalsRequest(ServiceRequest):
    MaxResults: _string | None
    NextToken: _string | None


class PortalSummary(TypedDict, total=False):
    """Represents a portal summary."""

    Authorization: Authorization
    EndpointConfiguration: EndpointConfigurationResponse
    IncludedPortalProductArns: _listOf__stringMin20Max2048
    LastModified: _timestampIso8601
    LastPublished: _timestampIso8601 | None
    LastPublishedDescription: _stringMin0Max1024 | None
    PortalArn: _stringMin20Max2048
    PortalContent: PortalContent
    PortalId: _stringMin10Max30PatternAZ09
    Preview: Preview | None
    PublishStatus: PublishStatus | None
    RumAppMonitorName: _stringMin0Max255 | None
    StatusException: StatusException | None
    Tags: Tags | None


_listOfPortalSummary = list[PortalSummary]


class ListPortalsResponse(TypedDict, total=False):
    Items: _listOfPortalSummary | None
    NextToken: _stringMin1Max2048 | None


class ListPortalsResponseContent(TypedDict, total=False):
    """Lists portals."""

    Items: _listOfPortalSummary | None
    NextToken: _stringMin1Max2048 | None


class ListProductPagesRequest(ServiceRequest):
    MaxResults: _string | None
    NextToken: _string | None
    PortalProductId: _string
    ResourceOwnerAccountId: _string | None


class ProductPageSummaryNoBody(TypedDict, total=False):
    """Represents a product page summary without listing any page content."""

    LastModified: _timestampIso8601
    PageTitle: _stringMin1Max255
    ProductPageArn: _stringMin20Max2048
    ProductPageId: _stringMin10Max30PatternAZ09


_listOfProductPageSummaryNoBody = list[ProductPageSummaryNoBody]


class ListProductPagesResponse(TypedDict, total=False):
    Items: _listOfProductPageSummaryNoBody | None
    NextToken: _stringMin1Max2048 | None


class ListProductPagesResponseContent(TypedDict, total=False):
    """Lists product pages."""

    Items: _listOfProductPageSummaryNoBody
    NextToken: _stringMin1Max2048 | None


class ListProductRestEndpointPagesRequest(ServiceRequest):
    MaxResults: _string | None
    NextToken: _string | None
    PortalProductId: _string
    ResourceOwnerAccountId: _string | None


class ProductRestEndpointPageSummaryNoBody(TypedDict, total=False):
    """A summary of a product REST endpoint page, without providing the page
    content.
    """

    Endpoint: _stringMin1Max1024
    LastModified: _timestampIso8601
    OperationName: _stringMin1Max255 | None
    ProductRestEndpointPageArn: _stringMin20Max2048
    ProductRestEndpointPageId: _stringMin10Max30PatternAZ09
    RestEndpointIdentifier: RestEndpointIdentifier
    Status: Status
    StatusException: StatusException | None
    TryItState: TryItState


_listOfProductRestEndpointPageSummaryNoBody = list[ProductRestEndpointPageSummaryNoBody]


class ListProductRestEndpointPagesResponse(TypedDict, total=False):
    Items: _listOfProductRestEndpointPageSummaryNoBody | None
    NextToken: _string | None


class ListProductRestEndpointPagesResponseContent(TypedDict, total=False):
    """Lists the product rest endpoint pages in a portal product."""

    Items: _listOfProductRestEndpointPageSummaryNoBody
    NextToken: _string | None


class Models(TypedDict, total=False):
    """Represents a collection of data models. See `Create Models and Mapping
    Templates for Request and Response
    Mappings <https://docs.aws.amazon.com/apigateway/latest/developerguide/models-mappings.html>`__.
    """

    Items: _listOfModel | None
    NextToken: NextToken | None


class NotFoundExceptionResponseContent(TypedDict, total=False):
    """The response content for not found exception."""

    Message: _string | None
    ResourceType: _string | None


class PreviewPortalRequest(ServiceRequest):
    PortalId: _string


class PreviewPortalResponse(TypedDict, total=False):
    pass


class PublishPortalRequest(ServiceRequest):
    """The request body for the post operation."""

    Description: _stringMin0Max1024 | None
    PortalId: _string


class PublishPortalRequestContent(TypedDict, total=False):
    """Publish a portal."""

    Description: _stringMin0Max1024 | None


class PublishPortalResponse(TypedDict, total=False):
    pass


class PutPortalProductSharingPolicyRequest(ServiceRequest):
    """The request body for the put operation."""

    PolicyDocument: _stringMin1Max307200
    PortalProductId: _string


class PutPortalProductSharingPolicyRequestContent(TypedDict, total=False):
    """The request content."""

    PolicyDocument: _stringMin1Max307200


class PutPortalProductSharingPolicyResponse(TypedDict, total=False):
    pass


class PutRoutingRuleRequest(ServiceRequest):
    Actions: _listOfRoutingRuleAction
    Conditions: _listOfRoutingRuleCondition
    DomainName: _string
    DomainNameId: _string | None
    Priority: RoutingRulePriority
    RoutingRuleId: _string


class PutRoutingRuleResponse(TypedDict, total=False):
    Actions: _listOfRoutingRuleAction | None
    Conditions: _listOfRoutingRuleCondition | None
    Priority: RoutingRulePriority | None
    RoutingRuleArn: Arn | None
    RoutingRuleId: Id | None


class ReimportApiInput(TypedDict, total=False):
    """Overwrites the configuration of an existing API using the provided
    definition. Supported only for HTTP APIs.
    """

    Body: _string


class ReimportApiRequest(ServiceRequest):
    ApiId: _string
    Basepath: _string | None
    Body: _string
    FailOnWarnings: _boolean | None


class ReimportApiResponse(TypedDict, total=False):
    ApiEndpoint: _string | None
    ApiGatewayManaged: _boolean | None
    ApiId: Id | None
    ApiKeySelectionExpression: SelectionExpression | None
    CorsConfiguration: Cors | None
    CreatedDate: _timestampIso8601 | None
    Description: StringWithLengthBetween0And1024 | None
    DisableSchemaValidation: _boolean | None
    DisableExecuteApiEndpoint: _boolean | None
    ImportInfo: _listOf__string | None
    IpAddressType: IpAddressType | None
    Name: StringWithLengthBetween1And128 | None
    ProtocolType: ProtocolType | None
    RouteSelectionExpression: SelectionExpression | None
    Tags: Tags | None
    Version: StringWithLengthBetween1And64 | None
    Warnings: _listOf__string | None


class RouteResponses(TypedDict, total=False):
    """Represents a collection of route responses."""

    Items: _listOfRouteResponse | None
    NextToken: NextToken | None


class Routes(TypedDict, total=False):
    """Represents a collection of routes."""

    Items: _listOfRoute | None
    NextToken: NextToken | None


class RoutingRuleInput(TypedDict, total=False):
    Actions: _listOfRoutingRuleAction
    Conditions: _listOfRoutingRuleCondition
    Priority: RoutingRulePriority


class RoutingRules(TypedDict, total=False):
    """A collection of routing rules."""

    NextToken: NextToken | None
    RoutingRules: _listOfRoutingRule | None


class Stages(TypedDict, total=False):
    """A collection of Stage resources that are associated with the ApiKey
    resource.
    """

    Items: _listOfStage | None
    NextToken: NextToken | None


class TagResourceInput(TypedDict, total=False):
    """Represents the input parameters for a TagResource request."""

    Tags: Tags | None


class TagResourceRequest(ServiceRequest):
    """Creates a new Tag resource to represent a tag."""

    ResourceArn: _string
    Tags: Tags | None


class TagResourceResponse(TypedDict, total=False):
    pass


class Template(TypedDict, total=False):
    """Represents a template."""

    Value: _string | None


class UntagResourceRequest(ServiceRequest):
    ResourceArn: _string
    TagKeys: _listOf__string


class UpdateApiInput(TypedDict, total=False):
    """Represents the input parameters for an UpdateApi request."""

    ApiKeySelectionExpression: SelectionExpression | None
    CorsConfiguration: Cors | None
    CredentialsArn: Arn | None
    Description: StringWithLengthBetween0And1024 | None
    DisableExecuteApiEndpoint: _boolean | None
    DisableSchemaValidation: _boolean | None
    IpAddressType: IpAddressType | None
    Name: StringWithLengthBetween1And128 | None
    RouteKey: SelectionKey | None
    RouteSelectionExpression: SelectionExpression | None
    Target: UriWithLengthBetween1And2048 | None
    Version: StringWithLengthBetween1And64 | None


class UpdateApiMappingInput(TypedDict, total=False):
    """Represents the input parameters for an UpdateApiMapping request."""

    ApiId: Id | None
    ApiMappingKey: SelectionKey | None
    Stage: StringWithLengthBetween1And128 | None


class UpdateApiMappingRequest(ServiceRequest):
    """Updates an ApiMapping."""

    ApiId: Id
    ApiMappingId: _string
    ApiMappingKey: SelectionKey | None
    DomainName: _string
    Stage: StringWithLengthBetween1And128 | None


class UpdateApiMappingResponse(TypedDict, total=False):
    ApiId: Id | None
    ApiMappingId: Id | None
    ApiMappingKey: SelectionKey | None
    Stage: StringWithLengthBetween1And128 | None


class UpdateApiRequest(ServiceRequest):
    """Updates an Api."""

    ApiId: _string
    ApiKeySelectionExpression: SelectionExpression | None
    CorsConfiguration: Cors | None
    CredentialsArn: Arn | None
    Description: StringWithLengthBetween0And1024 | None
    DisableSchemaValidation: _boolean | None
    DisableExecuteApiEndpoint: _boolean | None
    IpAddressType: IpAddressType | None
    Name: StringWithLengthBetween1And128 | None
    RouteKey: SelectionKey | None
    RouteSelectionExpression: SelectionExpression | None
    Target: UriWithLengthBetween1And2048 | None
    Version: StringWithLengthBetween1And64 | None


class UpdateApiResponse(TypedDict, total=False):
    ApiEndpoint: _string | None
    ApiGatewayManaged: _boolean | None
    ApiId: Id | None
    ApiKeySelectionExpression: SelectionExpression | None
    CorsConfiguration: Cors | None
    CreatedDate: _timestampIso8601 | None
    Description: StringWithLengthBetween0And1024 | None
    DisableSchemaValidation: _boolean | None
    DisableExecuteApiEndpoint: _boolean | None
    ImportInfo: _listOf__string | None
    IpAddressType: IpAddressType | None
    Name: StringWithLengthBetween1And128 | None
    ProtocolType: ProtocolType | None
    RouteSelectionExpression: SelectionExpression | None
    Tags: Tags | None
    Version: StringWithLengthBetween1And64 | None
    Warnings: _listOf__string | None


class UpdateAuthorizerInput(TypedDict, total=False):
    """The input parameters for an UpdateAuthorizer request."""

    AuthorizerCredentialsArn: Arn | None
    AuthorizerPayloadFormatVersion: StringWithLengthBetween1And64 | None
    AuthorizerResultTtlInSeconds: IntegerWithLengthBetween0And3600 | None
    AuthorizerType: AuthorizerType | None
    AuthorizerUri: UriWithLengthBetween1And2048 | None
    EnableSimpleResponses: _boolean | None
    IdentitySource: IdentitySourceList | None
    IdentityValidationExpression: StringWithLengthBetween0And1024 | None
    JwtConfiguration: JWTConfiguration | None
    Name: StringWithLengthBetween1And128 | None


class UpdateAuthorizerRequest(ServiceRequest):
    """Updates an Authorizer."""

    ApiId: _string
    AuthorizerCredentialsArn: Arn | None
    AuthorizerId: _string
    AuthorizerPayloadFormatVersion: StringWithLengthBetween1And64 | None
    AuthorizerResultTtlInSeconds: IntegerWithLengthBetween0And3600 | None
    AuthorizerType: AuthorizerType | None
    AuthorizerUri: UriWithLengthBetween1And2048 | None
    EnableSimpleResponses: _boolean | None
    IdentitySource: IdentitySourceList | None
    IdentityValidationExpression: StringWithLengthBetween0And1024 | None
    JwtConfiguration: JWTConfiguration | None
    Name: StringWithLengthBetween1And128 | None


class UpdateAuthorizerResponse(TypedDict, total=False):
    AuthorizerCredentialsArn: Arn | None
    AuthorizerId: Id | None
    AuthorizerPayloadFormatVersion: StringWithLengthBetween1And64 | None
    AuthorizerResultTtlInSeconds: IntegerWithLengthBetween0And3600 | None
    AuthorizerType: AuthorizerType | None
    AuthorizerUri: UriWithLengthBetween1And2048 | None
    EnableSimpleResponses: _boolean | None
    IdentitySource: IdentitySourceList | None
    IdentityValidationExpression: StringWithLengthBetween0And1024 | None
    JwtConfiguration: JWTConfiguration | None
    Name: StringWithLengthBetween1And128 | None


class UpdateDeploymentInput(TypedDict, total=False):
    """Represents the input parameters for an UpdateDeployment request."""

    Description: StringWithLengthBetween0And1024 | None


class UpdateDeploymentRequest(ServiceRequest):
    """Updates a Deployment."""

    ApiId: _string
    DeploymentId: _string
    Description: StringWithLengthBetween0And1024 | None


class UpdateDeploymentResponse(TypedDict, total=False):
    AutoDeployed: _boolean | None
    CreatedDate: _timestampIso8601 | None
    DeploymentId: Id | None
    DeploymentStatus: DeploymentStatus | None
    DeploymentStatusMessage: _string | None
    Description: StringWithLengthBetween0And1024 | None


class UpdateDomainNameInput(TypedDict, total=False):
    """Represents the input parameters for an UpdateDomainName request."""

    DomainNameConfigurations: DomainNameConfigurations | None
    MutualTlsAuthentication: MutualTlsAuthenticationInput | None
    RoutingMode: RoutingMode | None


class UpdateDomainNameRequest(ServiceRequest):
    """Updates a DomainName."""

    DomainName: _string
    DomainNameConfigurations: DomainNameConfigurations | None
    MutualTlsAuthentication: MutualTlsAuthenticationInput | None
    RoutingMode: RoutingMode | None


class UpdateDomainNameResponse(TypedDict, total=False):
    ApiMappingSelectionExpression: SelectionExpression | None
    DomainName: StringWithLengthBetween1And512 | None
    DomainNameArn: Arn | None
    DomainNameConfigurations: DomainNameConfigurations | None
    MutualTlsAuthentication: MutualTlsAuthentication | None
    RoutingMode: RoutingMode | None
    Tags: Tags | None


class UpdateIntegrationInput(TypedDict, total=False):
    """Represents the input parameters for an UpdateIntegration request."""

    ConnectionId: StringWithLengthBetween1And1024 | None
    ConnectionType: ConnectionType | None
    ContentHandlingStrategy: ContentHandlingStrategy | None
    CredentialsArn: Arn | None
    Description: StringWithLengthBetween0And1024 | None
    IntegrationMethod: StringWithLengthBetween1And64 | None
    IntegrationSubtype: StringWithLengthBetween1And128 | None
    IntegrationType: IntegrationType | None
    IntegrationUri: UriWithLengthBetween1And2048 | None
    PassthroughBehavior: PassthroughBehavior | None
    PayloadFormatVersion: StringWithLengthBetween1And64 | None
    RequestParameters: IntegrationParameters | None
    RequestTemplates: TemplateMap | None
    ResponseParameters: ResponseParameters | None
    TemplateSelectionExpression: SelectionExpression | None
    TimeoutInMillis: IntegerWithLengthBetween50And30000 | None
    TlsConfig: TlsConfigInput | None


class UpdateIntegrationRequest(ServiceRequest):
    """Updates an Integration."""

    ApiId: _string
    ConnectionId: StringWithLengthBetween1And1024 | None
    ConnectionType: ConnectionType | None
    ContentHandlingStrategy: ContentHandlingStrategy | None
    CredentialsArn: Arn | None
    Description: StringWithLengthBetween0And1024 | None
    IntegrationId: _string
    IntegrationMethod: StringWithLengthBetween1And64 | None
    IntegrationSubtype: StringWithLengthBetween1And128 | None
    IntegrationType: IntegrationType | None
    IntegrationUri: UriWithLengthBetween1And2048 | None
    PassthroughBehavior: PassthroughBehavior | None
    PayloadFormatVersion: StringWithLengthBetween1And64 | None
    RequestParameters: IntegrationParameters | None
    RequestTemplates: TemplateMap | None
    ResponseParameters: ResponseParameters | None
    TemplateSelectionExpression: SelectionExpression | None
    TimeoutInMillis: IntegerWithLengthBetween50And30000 | None
    TlsConfig: TlsConfigInput | None


class UpdateIntegrationResult(TypedDict, total=False):
    ApiGatewayManaged: _boolean | None
    ConnectionId: StringWithLengthBetween1And1024 | None
    ConnectionType: ConnectionType | None
    ContentHandlingStrategy: ContentHandlingStrategy | None
    CredentialsArn: Arn | None
    Description: StringWithLengthBetween0And1024 | None
    IntegrationId: Id | None
    IntegrationMethod: StringWithLengthBetween1And64 | None
    IntegrationResponseSelectionExpression: SelectionExpression | None
    IntegrationSubtype: StringWithLengthBetween1And128 | None
    IntegrationType: IntegrationType | None
    IntegrationUri: UriWithLengthBetween1And2048 | None
    PassthroughBehavior: PassthroughBehavior | None
    PayloadFormatVersion: StringWithLengthBetween1And64 | None
    RequestParameters: IntegrationParameters | None
    RequestTemplates: TemplateMap | None
    ResponseParameters: ResponseParameters | None
    TemplateSelectionExpression: SelectionExpression | None
    TimeoutInMillis: IntegerWithLengthBetween50And30000 | None
    TlsConfig: TlsConfig | None


class UpdateIntegrationResponseInput(TypedDict, total=False):
    """Represents the input parameters for an UpdateIntegrationResponse
    request.
    """

    ContentHandlingStrategy: ContentHandlingStrategy | None
    IntegrationResponseKey: SelectionKey | None
    ResponseParameters: IntegrationParameters | None
    ResponseTemplates: TemplateMap | None
    TemplateSelectionExpression: SelectionExpression | None


class UpdateIntegrationResponseRequest(ServiceRequest):
    """Updates an IntegrationResponses."""

    ApiId: _string
    ContentHandlingStrategy: ContentHandlingStrategy | None
    IntegrationId: _string
    IntegrationResponseId: _string
    IntegrationResponseKey: SelectionKey | None
    ResponseParameters: IntegrationParameters | None
    ResponseTemplates: TemplateMap | None
    TemplateSelectionExpression: SelectionExpression | None


class UpdateIntegrationResponseResponse(TypedDict, total=False):
    ContentHandlingStrategy: ContentHandlingStrategy | None
    IntegrationResponseId: Id | None
    IntegrationResponseKey: SelectionKey | None
    ResponseParameters: IntegrationParameters | None
    ResponseTemplates: TemplateMap | None
    TemplateSelectionExpression: SelectionExpression | None


class UpdateModelInput(TypedDict, total=False):
    """Represents the input parameters for an UpdateModel request. Supported
    only for WebSocket APIs.
    """

    ContentType: StringWithLengthBetween1And256 | None
    Description: StringWithLengthBetween0And1024 | None
    Name: StringWithLengthBetween1And128 | None
    Schema: StringWithLengthBetween0And32K | None


class UpdateModelRequest(ServiceRequest):
    """Updates a Model."""

    ApiId: _string
    ContentType: StringWithLengthBetween1And256 | None
    Description: StringWithLengthBetween0And1024 | None
    ModelId: _string
    Name: StringWithLengthBetween1And128 | None
    Schema: StringWithLengthBetween0And32K | None


class UpdateModelResponse(TypedDict, total=False):
    ContentType: StringWithLengthBetween1And256 | None
    Description: StringWithLengthBetween0And1024 | None
    ModelId: Id | None
    Name: StringWithLengthBetween1And128 | None
    Schema: StringWithLengthBetween0And32K | None


class UpdatePortalProductRequest(ServiceRequest):
    """The request body for the patch operation."""

    Description: _stringMin0Max1024 | None
    DisplayName: _stringMin1Max255 | None
    DisplayOrder: DisplayOrder | None
    PortalProductId: _string


class UpdatePortalProductRequestContent(TypedDict, total=False):
    """Updates a portal product."""

    Description: _stringMin0Max1024 | None
    DisplayName: _stringMin1Max255 | None
    DisplayOrder: DisplayOrder | None


class UpdatePortalProductResponse(TypedDict, total=False):
    Description: _stringMin0Max1024 | None
    DisplayName: _stringMin1Max255 | None
    DisplayOrder: DisplayOrder | None
    LastModified: _timestampIso8601 | None
    PortalProductArn: _stringMin20Max2048 | None
    PortalProductId: _stringMin10Max30PatternAZ09 | None
    Tags: Tags | None


class UpdatePortalProductResponseContent(TypedDict, total=False):
    """Updates a portal product."""

    Description: _stringMin0Max1024 | None
    DisplayName: _stringMin1Max255
    DisplayOrder: DisplayOrder | None
    LastModified: _timestampIso8601
    PortalProductArn: _stringMin20Max2048
    PortalProductId: _stringMin10Max30PatternAZ09
    Tags: Tags | None


class UpdatePortalRequest(ServiceRequest):
    """The request body for the patch operation."""

    Authorization: Authorization | None
    EndpointConfiguration: EndpointConfigurationRequest | None
    IncludedPortalProductArns: _listOf__stringMin20Max2048 | None
    LogoUri: _stringMin0Max1092 | None
    PortalContent: PortalContent | None
    PortalId: _string
    RumAppMonitorName: _stringMin0Max255 | None


class UpdatePortalRequestContent(TypedDict, total=False):
    """Updates a portal."""

    Authorization: Authorization | None
    EndpointConfiguration: EndpointConfigurationRequest | None
    IncludedPortalProductArns: _listOf__stringMin20Max2048 | None
    LogoUri: _stringMin0Max1092 | None
    PortalContent: PortalContent | None
    RumAppMonitorName: _stringMin0Max255 | None


class UpdatePortalResponse(TypedDict, total=False):
    Authorization: Authorization | None
    EndpointConfiguration: EndpointConfigurationResponse | None
    IncludedPortalProductArns: _listOf__stringMin20Max2048 | None
    LastModified: _timestampIso8601 | None
    LastPublished: _timestampIso8601 | None
    LastPublishedDescription: _stringMin0Max1024 | None
    PortalArn: _stringMin20Max2048 | None
    PortalContent: PortalContent | None
    PortalId: _stringMin10Max30PatternAZ09 | None
    Preview: Preview | None
    PublishStatus: PublishStatus | None
    RumAppMonitorName: _stringMin0Max255 | None
    StatusException: StatusException | None
    Tags: Tags | None


class UpdatePortalResponseContent(TypedDict, total=False):
    """Updates a portal."""

    Authorization: Authorization
    EndpointConfiguration: EndpointConfigurationResponse
    IncludedPortalProductArns: _listOf__stringMin20Max2048
    LastModified: _timestampIso8601
    LastPublished: _timestampIso8601 | None
    LastPublishedDescription: _stringMin0Max1024 | None
    PortalArn: _stringMin20Max2048
    PortalContent: PortalContent
    PortalId: _stringMin10Max30PatternAZ09
    Preview: Preview | None
    PublishStatus: PublishStatus | None
    RumAppMonitorName: _stringMin0Max255 | None
    StatusException: StatusException | None
    Tags: Tags | None


class UpdateProductPageRequest(ServiceRequest):
    """The request body for the patch operation."""

    DisplayContent: DisplayContent | None
    PortalProductId: _string
    ProductPageId: _string


class UpdateProductPageRequestContent(TypedDict, total=False):
    """Update a product page."""

    DisplayContent: DisplayContent | None


class UpdateProductPageResponse(TypedDict, total=False):
    DisplayContent: DisplayContent | None
    LastModified: _timestampIso8601 | None
    ProductPageArn: _stringMin20Max2048 | None
    ProductPageId: _stringMin10Max30PatternAZ09 | None


class UpdateProductPageResponseContent(TypedDict, total=False):
    """Updates a product page."""

    DisplayContent: DisplayContent | None
    LastModified: _timestampIso8601
    ProductPageArn: _stringMin20Max2048
    ProductPageId: _stringMin10Max30PatternAZ09


class UpdateProductRestEndpointPageRequest(ServiceRequest):
    """The request body for the patch operation."""

    DisplayContent: EndpointDisplayContent | None
    PortalProductId: _string
    ProductRestEndpointPageId: _string
    TryItState: TryItState | None


class UpdateProductRestEndpointPageRequestContent(TypedDict, total=False):
    """Updates a product REST endpoint page."""

    DisplayContent: EndpointDisplayContent | None
    TryItState: TryItState | None


class UpdateProductRestEndpointPageResponse(TypedDict, total=False):
    DisplayContent: EndpointDisplayContentResponse | None
    LastModified: _timestampIso8601 | None
    ProductRestEndpointPageArn: _stringMin20Max2048 | None
    ProductRestEndpointPageId: _stringMin10Max30PatternAZ09 | None
    RestEndpointIdentifier: RestEndpointIdentifier | None
    Status: Status | None
    StatusException: StatusException | None
    TryItState: TryItState | None


class UpdateProductRestEndpointPageResponseContent(TypedDict, total=False):
    """Update a product REST endpoint page."""

    DisplayContent: EndpointDisplayContentResponse
    LastModified: _timestampIso8601
    ProductRestEndpointPageArn: _stringMin20Max2048
    ProductRestEndpointPageId: _stringMin10Max30PatternAZ09
    RestEndpointIdentifier: RestEndpointIdentifier
    Status: Status
    StatusException: StatusException | None
    TryItState: TryItState


class UpdateRouteInput(TypedDict, total=False):
    """Represents the input parameters for an UpdateRoute request."""

    ApiKeyRequired: _boolean | None
    AuthorizationScopes: AuthorizationScopes | None
    AuthorizationType: AuthorizationType | None
    AuthorizerId: Id | None
    ModelSelectionExpression: SelectionExpression | None
    OperationName: StringWithLengthBetween1And64 | None
    RequestModels: RouteModels | None
    RequestParameters: RouteParameters | None
    RouteKey: SelectionKey | None
    RouteResponseSelectionExpression: SelectionExpression | None
    Target: StringWithLengthBetween1And128 | None


class UpdateRouteRequest(ServiceRequest):
    """Updates a Route."""

    ApiId: _string
    ApiKeyRequired: _boolean | None
    AuthorizationScopes: AuthorizationScopes | None
    AuthorizationType: AuthorizationType | None
    AuthorizerId: Id | None
    ModelSelectionExpression: SelectionExpression | None
    OperationName: StringWithLengthBetween1And64 | None
    RequestModels: RouteModels | None
    RequestParameters: RouteParameters | None
    RouteId: _string
    RouteKey: SelectionKey | None
    RouteResponseSelectionExpression: SelectionExpression | None
    Target: StringWithLengthBetween1And128 | None


class UpdateRouteResult(TypedDict, total=False):
    ApiGatewayManaged: _boolean | None
    ApiKeyRequired: _boolean | None
    AuthorizationScopes: AuthorizationScopes | None
    AuthorizationType: AuthorizationType | None
    AuthorizerId: Id | None
    ModelSelectionExpression: SelectionExpression | None
    OperationName: StringWithLengthBetween1And64 | None
    RequestModels: RouteModels | None
    RequestParameters: RouteParameters | None
    RouteId: Id | None
    RouteKey: SelectionKey | None
    RouteResponseSelectionExpression: SelectionExpression | None
    Target: StringWithLengthBetween1And128 | None


class UpdateRouteResponseInput(TypedDict, total=False):
    """Represents the input parameters for an UpdateRouteResponse request."""

    ModelSelectionExpression: SelectionExpression | None
    ResponseModels: RouteModels | None
    ResponseParameters: RouteParameters | None
    RouteResponseKey: SelectionKey | None


class UpdateRouteResponseRequest(ServiceRequest):
    """Updates a RouteResponse."""

    ApiId: _string
    ModelSelectionExpression: SelectionExpression | None
    ResponseModels: RouteModels | None
    ResponseParameters: RouteParameters | None
    RouteId: _string
    RouteResponseId: _string
    RouteResponseKey: SelectionKey | None


class UpdateRouteResponseResponse(TypedDict, total=False):
    ModelSelectionExpression: SelectionExpression | None
    ResponseModels: RouteModels | None
    ResponseParameters: RouteParameters | None
    RouteResponseId: Id | None
    RouteResponseKey: SelectionKey | None


class UpdateStageInput(TypedDict, total=False):
    """Represents the input parameters for an UpdateStage request."""

    AccessLogSettings: AccessLogSettings | None
    AutoDeploy: _boolean | None
    ClientCertificateId: Id | None
    DefaultRouteSettings: RouteSettings | None
    DeploymentId: Id | None
    Description: StringWithLengthBetween0And1024 | None
    RouteSettings: RouteSettingsMap | None
    StageVariables: StageVariablesMap | None


class UpdateStageRequest(ServiceRequest):
    """Updates a Stage."""

    AccessLogSettings: AccessLogSettings | None
    ApiId: _string
    AutoDeploy: _boolean | None
    ClientCertificateId: Id | None
    DefaultRouteSettings: RouteSettings | None
    DeploymentId: Id | None
    Description: StringWithLengthBetween0And1024 | None
    RouteSettings: RouteSettingsMap | None
    StageName: _string
    StageVariables: StageVariablesMap | None


class UpdateStageResponse(TypedDict, total=False):
    AccessLogSettings: AccessLogSettings | None
    ApiGatewayManaged: _boolean | None
    AutoDeploy: _boolean | None
    ClientCertificateId: Id | None
    CreatedDate: _timestampIso8601 | None
    DefaultRouteSettings: RouteSettings | None
    DeploymentId: Id | None
    Description: StringWithLengthBetween0And1024 | None
    LastDeploymentStatusMessage: _string | None
    LastUpdatedDate: _timestampIso8601 | None
    RouteSettings: RouteSettingsMap | None
    StageName: StringWithLengthBetween1And128 | None
    StageVariables: StageVariablesMap | None
    Tags: Tags | None


class UpdateVpcLinkInput(TypedDict, total=False):
    """Represents the input parameters for an UpdateVpcLink request."""

    Name: StringWithLengthBetween1And128 | None


class UpdateVpcLinkRequest(ServiceRequest):
    """Updates a VPC link."""

    Name: StringWithLengthBetween1And128 | None
    VpcLinkId: _string


class UpdateVpcLinkResponse(TypedDict, total=False):
    CreatedDate: _timestampIso8601 | None
    Name: StringWithLengthBetween1And128 | None
    SecurityGroupIds: SecurityGroupIdList | None
    SubnetIds: SubnetIdList | None
    Tags: Tags | None
    VpcLinkId: Id | None
    VpcLinkStatus: VpcLinkStatus | None
    VpcLinkStatusMessage: StringWithLengthBetween0And1024 | None
    VpcLinkVersion: VpcLinkVersion | None


class VpcLinks(TypedDict, total=False):
    """Represents a collection of VPCLinks."""

    Items: _listOfVpcLink | None
    NextToken: NextToken | None


_long = int
_timestampUnix = datetime


class Apigatewayv2Api:
    service: str = "apigatewayv2"
    version: str = "2018-11-29"

    @handler("CreateApi")
    def create_api(
        self,
        context: RequestContext,
        protocol_type: ProtocolType,
        name: StringWithLengthBetween1And128,
        api_key_selection_expression: SelectionExpression | None = None,
        cors_configuration: Cors | None = None,
        credentials_arn: Arn | None = None,
        description: StringWithLengthBetween0And1024 | None = None,
        disable_schema_validation: _boolean | None = None,
        disable_execute_api_endpoint: _boolean | None = None,
        ip_address_type: IpAddressType | None = None,
        route_key: SelectionKey | None = None,
        route_selection_expression: SelectionExpression | None = None,
        tags: Tags | None = None,
        target: UriWithLengthBetween1And2048 | None = None,
        version: StringWithLengthBetween1And64 | None = None,
        **kwargs,
    ) -> CreateApiResponse:
        """Creates an Api resource.

        :param protocol_type: The API protocol.
        :param name: The name of the API.
        :param api_key_selection_expression: An API key selection expression.
        :param cors_configuration: A CORS configuration.
        :param credentials_arn: This property is part of quick create.
        :param description: The description of the API.
        :param disable_schema_validation: Avoid validating models when creating a deployment.
        :param disable_execute_api_endpoint: Specifies whether clients can invoke your API by using the default
        execute-api endpoint.
        :param ip_address_type: The IP address types that can invoke the API.
        :param route_key: This property is part of quick create.
        :param route_selection_expression: The route selection expression for the API.
        :param tags: The collection of tags.
        :param target: This property is part of quick create.
        :param version: A version identifier for the API.
        :returns: CreateApiResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("CreateApiMapping")
    def create_api_mapping(
        self,
        context: RequestContext,
        domain_name: _string,
        stage: StringWithLengthBetween1And128,
        api_id: Id,
        api_mapping_key: SelectionKey | None = None,
        **kwargs,
    ) -> CreateApiMappingResponse:
        """Creates an API mapping.

        :param domain_name: The domain name.
        :param stage: The API stage.
        :param api_id: The API identifier.
        :param api_mapping_key: The API mapping key.
        :returns: CreateApiMappingResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("CreateAuthorizer")
    def create_authorizer(
        self,
        context: RequestContext,
        api_id: _string,
        authorizer_type: AuthorizerType,
        identity_source: IdentitySourceList,
        name: StringWithLengthBetween1And128,
        authorizer_credentials_arn: Arn | None = None,
        authorizer_payload_format_version: StringWithLengthBetween1And64 | None = None,
        authorizer_result_ttl_in_seconds: IntegerWithLengthBetween0And3600 | None = None,
        authorizer_uri: UriWithLengthBetween1And2048 | None = None,
        enable_simple_responses: _boolean | None = None,
        identity_validation_expression: StringWithLengthBetween0And1024 | None = None,
        jwt_configuration: JWTConfiguration | None = None,
        **kwargs,
    ) -> CreateAuthorizerResponse:
        """Creates an Authorizer for an API.

        :param api_id: The API identifier.
        :param authorizer_type: The authorizer type.
        :param identity_source: The identity source for which authorization is requested.
        :param name: The name of the authorizer.
        :param authorizer_credentials_arn: Specifies the required credentials as an IAM role for API Gateway to
        invoke the authorizer.
        :param authorizer_payload_format_version: Specifies the format of the payload sent to an HTTP API Lambda
        authorizer.
        :param authorizer_result_ttl_in_seconds: The time to live (TTL) for cached authorizer results, in seconds.
        :param authorizer_uri: The authorizer's Uniform Resource Identifier (URI).
        :param enable_simple_responses: Specifies whether a Lambda authorizer returns a response in a simple
        format.
        :param identity_validation_expression: This parameter is not used.
        :param jwt_configuration: Represents the configuration of a JWT authorizer.
        :returns: CreateAuthorizerResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("CreateDeployment")
    def create_deployment(
        self,
        context: RequestContext,
        api_id: _string,
        description: StringWithLengthBetween0And1024 | None = None,
        stage_name: StringWithLengthBetween1And128 | None = None,
        **kwargs,
    ) -> CreateDeploymentResponse:
        """Creates a Deployment for an API.

        :param api_id: The API identifier.
        :param description: The description for the deployment resource.
        :param stage_name: The name of the Stage resource for the Deployment resource to create.
        :returns: CreateDeploymentResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("CreateDomainName")
    def create_domain_name(
        self,
        context: RequestContext,
        domain_name: StringWithLengthBetween1And512,
        domain_name_configurations: DomainNameConfigurations | None = None,
        mutual_tls_authentication: MutualTlsAuthenticationInput | None = None,
        routing_mode: RoutingMode | None = None,
        tags: Tags | None = None,
        **kwargs,
    ) -> CreateDomainNameResponse:
        """Creates a domain name.

        :param domain_name: The domain name.
        :param domain_name_configurations: The domain name configurations.
        :param mutual_tls_authentication: The mutual TLS authentication configuration for a custom domain name.
        :param routing_mode: The routing mode.
        :param tags: The collection of tags associated with a domain name.
        :returns: CreateDomainNameResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("CreateIntegration")
    def create_integration(
        self,
        context: RequestContext,
        api_id: _string,
        integration_type: IntegrationType,
        connection_id: StringWithLengthBetween1And1024 | None = None,
        connection_type: ConnectionType | None = None,
        content_handling_strategy: ContentHandlingStrategy | None = None,
        credentials_arn: Arn | None = None,
        description: StringWithLengthBetween0And1024 | None = None,
        integration_method: StringWithLengthBetween1And64 | None = None,
        integration_subtype: StringWithLengthBetween1And128 | None = None,
        integration_uri: UriWithLengthBetween1And2048 | None = None,
        passthrough_behavior: PassthroughBehavior | None = None,
        payload_format_version: StringWithLengthBetween1And64 | None = None,
        request_parameters: IntegrationParameters | None = None,
        request_templates: TemplateMap | None = None,
        response_parameters: ResponseParameters | None = None,
        template_selection_expression: SelectionExpression | None = None,
        timeout_in_millis: IntegerWithLengthBetween50And30000 | None = None,
        tls_config: TlsConfigInput | None = None,
        **kwargs,
    ) -> CreateIntegrationResult:
        """Creates an Integration.

        :param api_id: The API identifier.
        :param integration_type: The integration type of an integration.
        :param connection_id: The ID of the VPC link for a private integration.
        :param connection_type: The type of the network connection to the integration endpoint.
        :param content_handling_strategy: Supported only for WebSocket APIs.
        :param credentials_arn: Specifies the credentials required for the integration, if any.
        :param description: The description of the integration.
        :param integration_method: Specifies the integration's HTTP method type.
        :param integration_subtype: Supported only for HTTP API AWS_PROXY integrations.
        :param integration_uri: For a Lambda integration, specify the URI of a Lambda function.
        :param passthrough_behavior: Specifies the pass-through behavior for incoming requests based on the
        Content-Type header in the request, and the available mapping templates
        specified as the requestTemplates property on the Integration resource.
        :param payload_format_version: Specifies the format of the payload sent to an integration.
        :param request_parameters: For WebSocket APIs, a key-value map specifying request parameters that
        are passed from the method request to the backend.
        :param request_templates: Represents a map of Velocity templates that are applied on the request
        payload based on the value of the Content-Type header sent by the
        client.
        :param response_parameters: Supported only for HTTP APIs.
        :param template_selection_expression: The template selection expression for the integration.
        :param timeout_in_millis: Custom timeout between 50 and 29,000 milliseconds for WebSocket APIs and
        between 50 and 30,000 milliseconds for HTTP APIs.
        :param tls_config: The TLS configuration for a private integration.
        :returns: CreateIntegrationResult
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("CreateIntegrationResponse")
    def create_integration_response(
        self,
        context: RequestContext,
        api_id: _string,
        integration_id: _string,
        integration_response_key: SelectionKey,
        content_handling_strategy: ContentHandlingStrategy | None = None,
        response_parameters: IntegrationParameters | None = None,
        response_templates: TemplateMap | None = None,
        template_selection_expression: SelectionExpression | None = None,
        **kwargs,
    ) -> CreateIntegrationResponseResponse:
        """Creates an IntegrationResponses.

        :param api_id: The API identifier.
        :param integration_id: The integration ID.
        :param integration_response_key: The integration response key.
        :param content_handling_strategy: Specifies how to handle response payload content type conversions.
        :param response_parameters: A key-value map specifying response parameters that are passed to the
        method response from the backend.
        :param response_templates: The collection of response templates for the integration response as a
        string-to-string map of key-value pairs.
        :param template_selection_expression: The template selection expression for the integration response.
        :returns: CreateIntegrationResponseResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("CreateModel")
    def create_model(
        self,
        context: RequestContext,
        api_id: _string,
        schema: StringWithLengthBetween0And32K,
        name: StringWithLengthBetween1And128,
        content_type: StringWithLengthBetween1And256 | None = None,
        description: StringWithLengthBetween0And1024 | None = None,
        **kwargs,
    ) -> CreateModelResponse:
        """Creates a Model for an API.

        :param api_id: The API identifier.
        :param schema: The schema for the model.
        :param name: The name of the model.
        :param content_type: The content-type for the model, for example, "application/json".
        :param description: The description of the model.
        :returns: CreateModelResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("CreatePortal")
    def create_portal(
        self,
        context: RequestContext,
        authorization: Authorization,
        portal_content: PortalContent,
        endpoint_configuration: EndpointConfigurationRequest,
        included_portal_product_arns: _listOf__stringMin20Max2048 | None = None,
        logo_uri: _stringMin0Max1092 | None = None,
        rum_app_monitor_name: _stringMin0Max255 | None = None,
        tags: Tags | None = None,
        **kwargs,
    ) -> CreatePortalResponse:
        """Creates a portal.

        :param authorization: The authentication configuration for the portal.
        :param portal_content: The content of the portal.
        :param endpoint_configuration: The domain configuration for the portal.
        :param included_portal_product_arns: The ARNs of the portal products included in the portal.
        :param logo_uri: The URI for the portal logo image that is displayed in the portal
        header.
        :param rum_app_monitor_name: The name of the Amazon CloudWatch RUM app monitor for the portal.
        :param tags: The collection of tags.
        :returns: CreatePortalResponse
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("CreatePortalProduct")
    def create_portal_product(
        self,
        context: RequestContext,
        display_name: _stringMin1Max255,
        description: _stringMin0Max1024 | None = None,
        tags: Tags | None = None,
        **kwargs,
    ) -> CreatePortalProductResponse:
        """Creates a new portal product.

        :param display_name: The name of the portal product as it appears in a published portal.
        :param description: A description of the portal product.
        :param tags: The collection of tags.
        :returns: CreatePortalProductResponse
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("CreateProductPage")
    def create_product_page(
        self,
        context: RequestContext,
        portal_product_id: _string,
        display_content: DisplayContent,
        **kwargs,
    ) -> CreateProductPageResponse:
        """Creates a new product page for a portal product.

        :param portal_product_id: The portal product identifier.
        :param display_content: The content of the product page.
        :returns: CreateProductPageResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("CreateProductRestEndpointPage")
    def create_product_rest_endpoint_page(
        self,
        context: RequestContext,
        portal_product_id: _string,
        rest_endpoint_identifier: RestEndpointIdentifier,
        display_content: EndpointDisplayContent | None = None,
        try_it_state: TryItState | None = None,
        **kwargs,
    ) -> CreateProductRestEndpointPageResponse:
        """Creates a product REST endpoint page for a portal product.

        :param portal_product_id: The portal product identifier.
        :param rest_endpoint_identifier: The REST endpoint identifier.
        :param display_content: The content of the product REST endpoint page.
        :param try_it_state: The try it state of the product REST endpoint page.
        :returns: CreateProductRestEndpointPageResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("CreateRoute")
    def create_route(
        self,
        context: RequestContext,
        api_id: _string,
        route_key: SelectionKey,
        api_key_required: _boolean | None = None,
        authorization_scopes: AuthorizationScopes | None = None,
        authorization_type: AuthorizationType | None = None,
        authorizer_id: Id | None = None,
        model_selection_expression: SelectionExpression | None = None,
        operation_name: StringWithLengthBetween1And64 | None = None,
        request_models: RouteModels | None = None,
        request_parameters: RouteParameters | None = None,
        route_response_selection_expression: SelectionExpression | None = None,
        target: StringWithLengthBetween1And128 | None = None,
        **kwargs,
    ) -> CreateRouteResult:
        """Creates a Route for an API.

        :param api_id: The API identifier.
        :param route_key: The route key for the route.
        :param api_key_required: Specifies whether an API key is required for the route.
        :param authorization_scopes: The authorization scopes supported by this route.
        :param authorization_type: The authorization type for the route.
        :param authorizer_id: The identifier of the Authorizer resource to be associated with this
        route.
        :param model_selection_expression: The model selection expression for the route.
        :param operation_name: The operation name for the route.
        :param request_models: The request models for the route.
        :param request_parameters: The request parameters for the route.
        :param route_response_selection_expression: The route response selection expression for the route.
        :param target: The target for the route.
        :returns: CreateRouteResult
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("CreateRouteResponse")
    def create_route_response(
        self,
        context: RequestContext,
        api_id: _string,
        route_id: _string,
        route_response_key: SelectionKey,
        model_selection_expression: SelectionExpression | None = None,
        response_models: RouteModels | None = None,
        response_parameters: RouteParameters | None = None,
        **kwargs,
    ) -> CreateRouteResponseResponse:
        """Creates a RouteResponse for a Route.

        :param api_id: The API identifier.
        :param route_id: The route ID.
        :param route_response_key: The route response key.
        :param model_selection_expression: The model selection expression for the route response.
        :param response_models: The response models for the route response.
        :param response_parameters: The route response parameters.
        :returns: CreateRouteResponseResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("CreateRoutingRule")
    def create_routing_rule(
        self,
        context: RequestContext,
        domain_name: _string,
        actions: _listOfRoutingRuleAction,
        priority: RoutingRulePriority,
        conditions: _listOfRoutingRuleCondition,
        domain_name_id: _string | None = None,
        **kwargs,
    ) -> CreateRoutingRuleResponse:
        """Creates a RoutingRule.

        :param domain_name: The domain name.
        :param actions: Represents a routing rule action.
        :param priority: Represents the priority of the routing rule.
        :param conditions: Represents a condition.
        :param domain_name_id: The domain name ID.
        :returns: CreateRoutingRuleResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("CreateStage")
    def create_stage(
        self,
        context: RequestContext,
        api_id: _string,
        stage_name: StringWithLengthBetween1And128,
        access_log_settings: AccessLogSettings | None = None,
        auto_deploy: _boolean | None = None,
        client_certificate_id: Id | None = None,
        default_route_settings: RouteSettings | None = None,
        deployment_id: Id | None = None,
        description: StringWithLengthBetween0And1024 | None = None,
        route_settings: RouteSettingsMap | None = None,
        stage_variables: StageVariablesMap | None = None,
        tags: Tags | None = None,
        **kwargs,
    ) -> CreateStageResponse:
        """Creates a Stage for an API.

        :param api_id: The API identifier.
        :param stage_name: The name of the stage.
        :param access_log_settings: Settings for logging access in this stage.
        :param auto_deploy: Specifies whether updates to an API automatically trigger a new
        deployment.
        :param client_certificate_id: The identifier of a client certificate for a Stage.
        :param default_route_settings: The default route settings for the stage.
        :param deployment_id: The deployment identifier of the API stage.
        :param description: The description for the API stage.
        :param route_settings: Route settings for the stage, by routeKey.
        :param stage_variables: A map that defines the stage variables for a Stage.
        :param tags: The collection of tags.
        :returns: CreateStageResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("CreateVpcLink")
    def create_vpc_link(
        self,
        context: RequestContext,
        subnet_ids: SubnetIdList,
        name: StringWithLengthBetween1And128,
        security_group_ids: SecurityGroupIdList | None = None,
        tags: Tags | None = None,
        **kwargs,
    ) -> CreateVpcLinkResponse:
        """Creates a VPC link.

        :param subnet_ids: A list of subnet IDs to include in the VPC link.
        :param name: The name of the VPC link.
        :param security_group_ids: A list of security group IDs for the VPC link.
        :param tags: A list of tags.
        :returns: CreateVpcLinkResponse
        :raises BadRequestException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteAccessLogSettings")
    def delete_access_log_settings(
        self, context: RequestContext, stage_name: _string, api_id: _string, **kwargs
    ) -> None:
        """Deletes the AccessLogSettings for a Stage. To disable access logging for
        a Stage, delete its AccessLogSettings.

        :param stage_name: The stage name.
        :param api_id: The API identifier.
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteApi")
    def delete_api(self, context: RequestContext, api_id: _string, **kwargs) -> None:
        """Deletes an Api resource.

        :param api_id: The API identifier.
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteApiMapping")
    def delete_api_mapping(
        self, context: RequestContext, api_mapping_id: _string, domain_name: _string, **kwargs
    ) -> None:
        """Deletes an API mapping.

        :param api_mapping_id: The API mapping identifier.
        :param domain_name: The domain name.
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("DeleteAuthorizer")
    def delete_authorizer(
        self, context: RequestContext, authorizer_id: _string, api_id: _string, **kwargs
    ) -> None:
        """Deletes an Authorizer.

        :param authorizer_id: The authorizer identifier.
        :param api_id: The API identifier.
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteCorsConfiguration")
    def delete_cors_configuration(self, context: RequestContext, api_id: _string, **kwargs) -> None:
        """Deletes a CORS configuration.

        :param api_id: The API identifier.
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteDeployment")
    def delete_deployment(
        self, context: RequestContext, api_id: _string, deployment_id: _string, **kwargs
    ) -> None:
        """Deletes a Deployment.

        :param api_id: The API identifier.
        :param deployment_id: The deployment ID.
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteDomainName")
    def delete_domain_name(self, context: RequestContext, domain_name: _string, **kwargs) -> None:
        """Deletes a domain name.

        :param domain_name: The domain name.
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteIntegration")
    def delete_integration(
        self, context: RequestContext, api_id: _string, integration_id: _string, **kwargs
    ) -> None:
        """Deletes an Integration.

        :param api_id: The API identifier.
        :param integration_id: The integration ID.
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteIntegrationResponse")
    def delete_integration_response(
        self,
        context: RequestContext,
        api_id: _string,
        integration_response_id: _string,
        integration_id: _string,
        **kwargs,
    ) -> None:
        """Deletes an IntegrationResponses.

        :param api_id: The API identifier.
        :param integration_response_id: The integration response ID.
        :param integration_id: The integration ID.
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteModel")
    def delete_model(
        self, context: RequestContext, model_id: _string, api_id: _string, **kwargs
    ) -> None:
        """Deletes a Model.

        :param model_id: The model ID.
        :param api_id: The API identifier.
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeletePortal")
    def delete_portal(self, context: RequestContext, portal_id: _string, **kwargs) -> None:
        """Deletes a portal.

        :param portal_id: The portal identifier.
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("DeletePortalProduct")
    def delete_portal_product(
        self, context: RequestContext, portal_product_id: _string, **kwargs
    ) -> None:
        """Deletes a portal product.

        :param portal_product_id: The portal product identifier.
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("DeletePortalProductSharingPolicy")
    def delete_portal_product_sharing_policy(
        self, context: RequestContext, portal_product_id: _string, **kwargs
    ) -> None:
        """Deletes the sharing policy for a portal product.

        :param portal_product_id: The portal product identifier.
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("DeleteProductPage")
    def delete_product_page(
        self,
        context: RequestContext,
        portal_product_id: _string,
        product_page_id: _string,
        **kwargs,
    ) -> None:
        """Deletes a product page of a portal product.

        :param portal_product_id: The portal product identifier.
        :param product_page_id: The portal product identifier.
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("DeleteProductRestEndpointPage")
    def delete_product_rest_endpoint_page(
        self,
        context: RequestContext,
        product_rest_endpoint_page_id: _string,
        portal_product_id: _string,
        **kwargs,
    ) -> None:
        """Deletes a product REST endpoint page.

        :param product_rest_endpoint_page_id: The product REST endpoint identifier.
        :param portal_product_id: The portal product identifier.
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("DeleteRoute")
    def delete_route(
        self, context: RequestContext, api_id: _string, route_id: _string, **kwargs
    ) -> None:
        """Deletes a Route.

        :param api_id: The API identifier.
        :param route_id: The route ID.
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteRouteRequestParameter")
    def delete_route_request_parameter(
        self,
        context: RequestContext,
        request_parameter_key: _string,
        api_id: _string,
        route_id: _string,
        **kwargs,
    ) -> None:
        """Deletes a route request parameter. Supported only for WebSocket APIs.

        :param request_parameter_key: The route request parameter key.
        :param api_id: The API identifier.
        :param route_id: The route ID.
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteRouteResponse")
    def delete_route_response(
        self,
        context: RequestContext,
        route_response_id: _string,
        api_id: _string,
        route_id: _string,
        **kwargs,
    ) -> None:
        """Deletes a RouteResponse.

        :param route_response_id: The route response ID.
        :param api_id: The API identifier.
        :param route_id: The route ID.
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteRouteSettings")
    def delete_route_settings(
        self,
        context: RequestContext,
        stage_name: _string,
        route_key: _string,
        api_id: _string,
        **kwargs,
    ) -> None:
        """Deletes the RouteSettings for a stage.

        :param stage_name: The stage name.
        :param route_key: The route key.
        :param api_id: The API identifier.
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteRoutingRule")
    def delete_routing_rule(
        self,
        context: RequestContext,
        routing_rule_id: _string,
        domain_name: _string,
        domain_name_id: _string | None = None,
        **kwargs,
    ) -> None:
        """Deletes a routing rule.

        :param routing_rule_id: The routing rule ID.
        :param domain_name: The domain name.
        :param domain_name_id: The domain name ID.
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("DeleteStage")
    def delete_stage(
        self, context: RequestContext, stage_name: _string, api_id: _string, **kwargs
    ) -> None:
        """Deletes a Stage.

        :param stage_name: The stage name.
        :param api_id: The API identifier.
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteVpcLink")
    def delete_vpc_link(
        self, context: RequestContext, vpc_link_id: _string, **kwargs
    ) -> DeleteVpcLinkResponse:
        """Deletes a VPC link.

        :param vpc_link_id: The ID of the VPC link.
        :returns: DeleteVpcLinkResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("ExportApi")
    def export_api(
        self,
        context: RequestContext,
        specification: _string,
        output_type: _string,
        api_id: _string,
        export_version: _string | None = None,
        include_extensions: _boolean | None = None,
        stage_name: _string | None = None,
        **kwargs,
    ) -> ExportApiResponse:
        """

        :param specification: The version of the API specification to use.
        :param output_type: The output type of the exported definition file.
        :param api_id: The API identifier.
        :param export_version: The version of the API Gateway export algorithm.
        :param include_extensions: Specifies whether to include `API Gateway
        extensions <https://docs.
        :param stage_name: The name of the API stage to export.
        :returns: ExportApiResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("DisablePortal")
    def disable_portal(self, context: RequestContext, portal_id: _string, **kwargs) -> None:
        """Deletes the publication of a portal portal.

        :param portal_id: The portal identifier.
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("ResetAuthorizersCache")
    def reset_authorizers_cache(
        self, context: RequestContext, stage_name: _string, api_id: _string, **kwargs
    ) -> None:
        """Resets all authorizer cache entries on a stage. Supported only for HTTP
        APIs.

        :param stage_name: The stage name.
        :param api_id: The API identifier.
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetApi")
    def get_api(self, context: RequestContext, api_id: _string, **kwargs) -> GetApiResponse:
        """Gets an Api resource.

        :param api_id: The API identifier.
        :returns: GetApiResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetApiMapping")
    def get_api_mapping(
        self, context: RequestContext, api_mapping_id: _string, domain_name: _string, **kwargs
    ) -> GetApiMappingResponse:
        """Gets an API mapping.

        :param api_mapping_id: The API mapping identifier.
        :param domain_name: The domain name.
        :returns: GetApiMappingResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetApiMappings")
    def get_api_mappings(
        self,
        context: RequestContext,
        domain_name: _string,
        max_results: _string | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> GetApiMappingsResponse:
        """Gets API mappings.

        :param domain_name: The domain name.
        :param max_results: The maximum number of elements to be returned for this resource.
        :param next_token: The next page of elements from this collection.
        :returns: GetApiMappingsResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetApis")
    def get_apis(
        self,
        context: RequestContext,
        max_results: _string | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> GetApisResponse:
        """Gets a collection of Api resources.

        :param max_results: The maximum number of elements to be returned for this resource.
        :param next_token: The next page of elements from this collection.
        :returns: GetApisResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetAuthorizer")
    def get_authorizer(
        self, context: RequestContext, authorizer_id: _string, api_id: _string, **kwargs
    ) -> GetAuthorizerResponse:
        """Gets an Authorizer.

        :param authorizer_id: The authorizer identifier.
        :param api_id: The API identifier.
        :returns: GetAuthorizerResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetAuthorizers")
    def get_authorizers(
        self,
        context: RequestContext,
        api_id: _string,
        max_results: _string | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> GetAuthorizersResponse:
        """Gets the Authorizers for an API.

        :param api_id: The API identifier.
        :param max_results: The maximum number of elements to be returned for this resource.
        :param next_token: The next page of elements from this collection.
        :returns: GetAuthorizersResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetDeployment")
    def get_deployment(
        self, context: RequestContext, api_id: _string, deployment_id: _string, **kwargs
    ) -> GetDeploymentResponse:
        """Gets a Deployment.

        :param api_id: The API identifier.
        :param deployment_id: The deployment ID.
        :returns: GetDeploymentResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetDeployments")
    def get_deployments(
        self,
        context: RequestContext,
        api_id: _string,
        max_results: _string | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> GetDeploymentsResponse:
        """Gets the Deployments for an API.

        :param api_id: The API identifier.
        :param max_results: The maximum number of elements to be returned for this resource.
        :param next_token: The next page of elements from this collection.
        :returns: GetDeploymentsResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetDomainName")
    def get_domain_name(
        self, context: RequestContext, domain_name: _string, **kwargs
    ) -> GetDomainNameResponse:
        """Gets a domain name.

        :param domain_name: The domain name.
        :returns: GetDomainNameResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetDomainNames")
    def get_domain_names(
        self,
        context: RequestContext,
        max_results: _string | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> GetDomainNamesResponse:
        """Gets the domain names for an AWS account.

        :param max_results: The maximum number of elements to be returned for this resource.
        :param next_token: The next page of elements from this collection.
        :returns: GetDomainNamesResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetIntegration")
    def get_integration(
        self, context: RequestContext, api_id: _string, integration_id: _string, **kwargs
    ) -> GetIntegrationResult:
        """Gets an Integration.

        :param api_id: The API identifier.
        :param integration_id: The integration ID.
        :returns: GetIntegrationResult
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetIntegrationResponse")
    def get_integration_response(
        self,
        context: RequestContext,
        api_id: _string,
        integration_response_id: _string,
        integration_id: _string,
        **kwargs,
    ) -> GetIntegrationResponseResponse:
        """Gets an IntegrationResponses.

        :param api_id: The API identifier.
        :param integration_response_id: The integration response ID.
        :param integration_id: The integration ID.
        :returns: GetIntegrationResponseResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetIntegrationResponses")
    def get_integration_responses(
        self,
        context: RequestContext,
        integration_id: _string,
        api_id: _string,
        max_results: _string | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> GetIntegrationResponsesResponse:
        """Gets the IntegrationResponses for an Integration.

        :param integration_id: The integration ID.
        :param api_id: The API identifier.
        :param max_results: The maximum number of elements to be returned for this resource.
        :param next_token: The next page of elements from this collection.
        :returns: GetIntegrationResponsesResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetIntegrations")
    def get_integrations(
        self,
        context: RequestContext,
        api_id: _string,
        max_results: _string | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> GetIntegrationsResponse:
        """Gets the Integrations for an API.

        :param api_id: The API identifier.
        :param max_results: The maximum number of elements to be returned for this resource.
        :param next_token: The next page of elements from this collection.
        :returns: GetIntegrationsResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetModel")
    def get_model(
        self, context: RequestContext, model_id: _string, api_id: _string, **kwargs
    ) -> GetModelResponse:
        """Gets a Model.

        :param model_id: The model ID.
        :param api_id: The API identifier.
        :returns: GetModelResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetModelTemplate")
    def get_model_template(
        self, context: RequestContext, model_id: _string, api_id: _string, **kwargs
    ) -> GetModelTemplateResponse:
        """Gets a model template.

        :param model_id: The model ID.
        :param api_id: The API identifier.
        :returns: GetModelTemplateResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetModels")
    def get_models(
        self,
        context: RequestContext,
        api_id: _string,
        max_results: _string | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> GetModelsResponse:
        """Gets the Models for an API.

        :param api_id: The API identifier.
        :param max_results: The maximum number of elements to be returned for this resource.
        :param next_token: The next page of elements from this collection.
        :returns: GetModelsResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetPortal")
    def get_portal(
        self, context: RequestContext, portal_id: _string, **kwargs
    ) -> GetPortalResponse:
        """Gets a portal.

        :param portal_id: The portal identifier.
        :returns: GetPortalResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("GetPortalProduct")
    def get_portal_product(
        self,
        context: RequestContext,
        portal_product_id: _string,
        resource_owner_account_id: _string | None = None,
        **kwargs,
    ) -> GetPortalProductResponse:
        """Gets a portal product.

        :param portal_product_id: The portal product identifier.
        :param resource_owner_account_id: The account ID of the resource owner of the portal product.
        :returns: GetPortalProductResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("GetPortalProductSharingPolicy")
    def get_portal_product_sharing_policy(
        self, context: RequestContext, portal_product_id: _string, **kwargs
    ) -> GetPortalProductSharingPolicyResponse:
        """Gets the sharing policy for a portal product.

        :param portal_product_id: The portal product identifier.
        :returns: GetPortalProductSharingPolicyResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("GetProductPage")
    def get_product_page(
        self,
        context: RequestContext,
        portal_product_id: _string,
        product_page_id: _string,
        resource_owner_account_id: _string | None = None,
        **kwargs,
    ) -> GetProductPageResponse:
        """Gets a product page of a portal product.

        :param portal_product_id: The portal product identifier.
        :param product_page_id: The portal product identifier.
        :param resource_owner_account_id: The account ID of the resource owner of the portal product.
        :returns: GetProductPageResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("GetProductRestEndpointPage")
    def get_product_rest_endpoint_page(
        self,
        context: RequestContext,
        portal_product_id: _string,
        product_rest_endpoint_page_id: _string,
        include_raw_display_content: _string | None = None,
        resource_owner_account_id: _string | None = None,
        **kwargs,
    ) -> GetProductRestEndpointPageResponse:
        """Gets a product REST endpoint page.

        :param portal_product_id: The portal product identifier.
        :param product_rest_endpoint_page_id: The product REST endpoint identifier.
        :param include_raw_display_content: The query parameter to include raw display content.
        :param resource_owner_account_id: The account ID of the resource owner of the portal product.
        :returns: GetProductRestEndpointPageResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("GetRoute")
    def get_route(
        self, context: RequestContext, api_id: _string, route_id: _string, **kwargs
    ) -> GetRouteResult:
        """Gets a Route.

        :param api_id: The API identifier.
        :param route_id: The route ID.
        :returns: GetRouteResult
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetRouteResponse")
    def get_route_response(
        self,
        context: RequestContext,
        route_response_id: _string,
        api_id: _string,
        route_id: _string,
        **kwargs,
    ) -> GetRouteResponseResponse:
        """Gets a RouteResponse.

        :param route_response_id: The route response ID.
        :param api_id: The API identifier.
        :param route_id: The route ID.
        :returns: GetRouteResponseResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetRouteResponses")
    def get_route_responses(
        self,
        context: RequestContext,
        route_id: _string,
        api_id: _string,
        max_results: _string | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> GetRouteResponsesResponse:
        """Gets the RouteResponses for a Route.

        :param route_id: The route ID.
        :param api_id: The API identifier.
        :param max_results: The maximum number of elements to be returned for this resource.
        :param next_token: The next page of elements from this collection.
        :returns: GetRouteResponsesResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetRoutes")
    def get_routes(
        self,
        context: RequestContext,
        api_id: _string,
        max_results: _string | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> GetRoutesResponse:
        """Gets the Routes for an API.

        :param api_id: The API identifier.
        :param max_results: The maximum number of elements to be returned for this resource.
        :param next_token: The next page of elements from this collection.
        :returns: GetRoutesResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetRoutingRule")
    def get_routing_rule(
        self,
        context: RequestContext,
        routing_rule_id: _string,
        domain_name: _string,
        domain_name_id: _string | None = None,
        **kwargs,
    ) -> GetRoutingRuleResponse:
        """Gets a routing rule.

        :param routing_rule_id: The routing rule ID.
        :param domain_name: The domain name.
        :param domain_name_id: The domain name ID.
        :returns: GetRoutingRuleResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("ListRoutingRules")
    def list_routing_rules(
        self,
        context: RequestContext,
        domain_name: _string,
        domain_name_id: _string | None = None,
        max_results: MaxResults | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> ListRoutingRulesResponse:
        """Lists routing rules.

        :param domain_name: The domain name.
        :param domain_name_id: The domain name ID.
        :param max_results: The maximum number of elements to be returned for this resource.
        :param next_token: The next page of elements from this collection.
        :returns: ListRoutingRulesResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetStage")
    def get_stage(
        self, context: RequestContext, stage_name: _string, api_id: _string, **kwargs
    ) -> GetStageResponse:
        """Gets a Stage.

        :param stage_name: The stage name.
        :param api_id: The API identifier.
        :returns: GetStageResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetStages")
    def get_stages(
        self,
        context: RequestContext,
        api_id: _string,
        max_results: _string | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> GetStagesResponse:
        """Gets the Stages for an API.

        :param api_id: The API identifier.
        :param max_results: The maximum number of elements to be returned for this resource.
        :param next_token: The next page of elements from this collection.
        :returns: GetStagesResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetTags")
    def get_tags(self, context: RequestContext, resource_arn: _string, **kwargs) -> GetTagsResponse:
        """Gets a collection of Tag resources.

        :param resource_arn: The resource ARN for the tag.
        :returns: GetTagsResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("GetVpcLink")
    def get_vpc_link(
        self, context: RequestContext, vpc_link_id: _string, **kwargs
    ) -> GetVpcLinkResponse:
        """Gets a VPC link.

        :param vpc_link_id: The ID of the VPC link.
        :returns: GetVpcLinkResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetVpcLinks")
    def get_vpc_links(
        self,
        context: RequestContext,
        max_results: _string | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> GetVpcLinksResponse:
        """Gets a collection of VPC links.

        :param max_results: The maximum number of elements to be returned for this resource.
        :param next_token: The next page of elements from this collection.
        :returns: GetVpcLinksResponse
        :raises BadRequestException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("ImportApi")
    def import_api(
        self,
        context: RequestContext,
        body: _string,
        basepath: _string | None = None,
        fail_on_warnings: _boolean | None = None,
        **kwargs,
    ) -> ImportApiResponse:
        """Imports an API.

        :param body: The OpenAPI definition.
        :param basepath: Specifies how to interpret the base path of the API during import.
        :param fail_on_warnings: Specifies whether to rollback the API creation when a warning is
        encountered.
        :returns: ImportApiResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("ListPortalProducts")
    def list_portal_products(
        self,
        context: RequestContext,
        max_results: _string | None = None,
        next_token: _string | None = None,
        resource_owner: _string | None = None,
        **kwargs,
    ) -> ListPortalProductsResponse:
        """Lists portal products.

        :param max_results: The maximum number of elements to be returned for this resource.
        :param next_token: The next page of elements from this collection.
        :param resource_owner: The resource owner of the portal product.
        :returns: ListPortalProductsResponse
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("ListPortals")
    def list_portals(
        self,
        context: RequestContext,
        max_results: _string | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> ListPortalsResponse:
        """Lists portals.

        :param max_results: The maximum number of elements to be returned for this resource.
        :param next_token: The next page of elements from this collection.
        :returns: ListPortalsResponse
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("ListProductPages")
    def list_product_pages(
        self,
        context: RequestContext,
        portal_product_id: _string,
        max_results: _string | None = None,
        next_token: _string | None = None,
        resource_owner_account_id: _string | None = None,
        **kwargs,
    ) -> ListProductPagesResponse:
        """Lists the product pages for a portal product.

        :param portal_product_id: The portal product identifier.
        :param max_results: The maximum number of elements to be returned for this resource.
        :param next_token: The next page of elements from this collection.
        :param resource_owner_account_id: The account ID of the resource owner of the portal product.
        :returns: ListProductPagesResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("ListProductRestEndpointPages")
    def list_product_rest_endpoint_pages(
        self,
        context: RequestContext,
        portal_product_id: _string,
        max_results: _string | None = None,
        next_token: _string | None = None,
        resource_owner_account_id: _string | None = None,
        **kwargs,
    ) -> ListProductRestEndpointPagesResponse:
        """Lists the product REST endpoint pages of a portal product.

        :param portal_product_id: The portal product identifier.
        :param max_results: The maximum number of elements to be returned for this resource.
        :param next_token: The next page of elements from this collection.
        :param resource_owner_account_id: The account ID of the resource owner of the portal product.
        :returns: ListProductRestEndpointPagesResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("PreviewPortal")
    def preview_portal(
        self, context: RequestContext, portal_id: _string, **kwargs
    ) -> PreviewPortalResponse:
        """Creates a portal preview.

        :param portal_id: The portal identifier.
        :returns: PreviewPortalResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("PublishPortal")
    def publish_portal(
        self,
        context: RequestContext,
        portal_id: _string,
        description: _stringMin0Max1024 | None = None,
        **kwargs,
    ) -> PublishPortalResponse:
        """Publishes a portal.

        :param portal_id: The portal identifier.
        :param description: The description of the portal.
        :returns: PublishPortalResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("PutPortalProductSharingPolicy")
    def put_portal_product_sharing_policy(
        self,
        context: RequestContext,
        portal_product_id: _string,
        policy_document: _stringMin1Max307200,
        **kwargs,
    ) -> PutPortalProductSharingPolicyResponse:
        """Updates the sharing policy for a portal product.

        :param portal_product_id: The portal product identifier.
        :param policy_document: The product sharing policy.
        :returns: PutPortalProductSharingPolicyResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("PutRoutingRule")
    def put_routing_rule(
        self,
        context: RequestContext,
        routing_rule_id: _string,
        domain_name: _string,
        actions: _listOfRoutingRuleAction,
        priority: RoutingRulePriority,
        conditions: _listOfRoutingRuleCondition,
        domain_name_id: _string | None = None,
        **kwargs,
    ) -> PutRoutingRuleResponse:
        """Updates a routing rule.

        :param routing_rule_id: The routing rule ID.
        :param domain_name: The domain name.
        :param actions: The routing rule action.
        :param priority: The routing rule priority.
        :param conditions: The routing rule condition.
        :param domain_name_id: The domain name ID.
        :returns: PutRoutingRuleResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("ReimportApi")
    def reimport_api(
        self,
        context: RequestContext,
        api_id: _string,
        body: _string,
        basepath: _string | None = None,
        fail_on_warnings: _boolean | None = None,
        **kwargs,
    ) -> ReimportApiResponse:
        """Puts an Api resource.

        :param api_id: The API identifier.
        :param body: The OpenAPI definition.
        :param basepath: Specifies how to interpret the base path of the API during import.
        :param fail_on_warnings: Specifies whether to rollback the API creation when a warning is
        encountered.
        :returns: ReimportApiResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("TagResource")
    def tag_resource(
        self, context: RequestContext, resource_arn: _string, tags: Tags | None = None, **kwargs
    ) -> TagResourceResponse:
        """Creates a new Tag resource to represent a tag.

        :param resource_arn: The resource ARN for the tag.
        :param tags: The collection of tags.
        :returns: TagResourceResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("UntagResource")
    def untag_resource(
        self, context: RequestContext, resource_arn: _string, tag_keys: _listOf__string, **kwargs
    ) -> None:
        """Deletes a Tag.

        :param resource_arn: The resource ARN for the tag.
        :param tag_keys: The Tag keys to delete.
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("UpdateApi")
    def update_api(
        self,
        context: RequestContext,
        api_id: _string,
        api_key_selection_expression: SelectionExpression | None = None,
        cors_configuration: Cors | None = None,
        credentials_arn: Arn | None = None,
        description: StringWithLengthBetween0And1024 | None = None,
        disable_schema_validation: _boolean | None = None,
        disable_execute_api_endpoint: _boolean | None = None,
        ip_address_type: IpAddressType | None = None,
        name: StringWithLengthBetween1And128 | None = None,
        route_key: SelectionKey | None = None,
        route_selection_expression: SelectionExpression | None = None,
        target: UriWithLengthBetween1And2048 | None = None,
        version: StringWithLengthBetween1And64 | None = None,
        **kwargs,
    ) -> UpdateApiResponse:
        """Updates an Api resource.

        :param api_id: The API identifier.
        :param api_key_selection_expression: An API key selection expression.
        :param cors_configuration: A CORS configuration.
        :param credentials_arn: This property is part of quick create.
        :param description: The description of the API.
        :param disable_schema_validation: Avoid validating models when creating a deployment.
        :param disable_execute_api_endpoint: Specifies whether clients can invoke your API by using the default
        execute-api endpoint.
        :param ip_address_type: The IP address types that can invoke your API or domain name.
        :param name: The name of the API.
        :param route_key: This property is part of quick create.
        :param route_selection_expression: The route selection expression for the API.
        :param target: This property is part of quick create.
        :param version: A version identifier for the API.
        :returns: UpdateApiResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("UpdateApiMapping")
    def update_api_mapping(
        self,
        context: RequestContext,
        api_mapping_id: _string,
        api_id: Id,
        domain_name: _string,
        api_mapping_key: SelectionKey | None = None,
        stage: StringWithLengthBetween1And128 | None = None,
        **kwargs,
    ) -> UpdateApiMappingResponse:
        """The API mapping.

        :param api_mapping_id: The API mapping identifier.
        :param api_id: The API identifier.
        :param domain_name: The domain name.
        :param api_mapping_key: The API mapping key.
        :param stage: The API stage.
        :returns: UpdateApiMappingResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("UpdateAuthorizer")
    def update_authorizer(
        self,
        context: RequestContext,
        authorizer_id: _string,
        api_id: _string,
        authorizer_credentials_arn: Arn | None = None,
        authorizer_payload_format_version: StringWithLengthBetween1And64 | None = None,
        authorizer_result_ttl_in_seconds: IntegerWithLengthBetween0And3600 | None = None,
        authorizer_type: AuthorizerType | None = None,
        authorizer_uri: UriWithLengthBetween1And2048 | None = None,
        enable_simple_responses: _boolean | None = None,
        identity_source: IdentitySourceList | None = None,
        identity_validation_expression: StringWithLengthBetween0And1024 | None = None,
        jwt_configuration: JWTConfiguration | None = None,
        name: StringWithLengthBetween1And128 | None = None,
        **kwargs,
    ) -> UpdateAuthorizerResponse:
        """Updates an Authorizer.

        :param authorizer_id: The authorizer identifier.
        :param api_id: The API identifier.
        :param authorizer_credentials_arn: Specifies the required credentials as an IAM role for API Gateway to
        invoke the authorizer.
        :param authorizer_payload_format_version: Specifies the format of the payload sent to an HTTP API Lambda
        authorizer.
        :param authorizer_result_ttl_in_seconds: The time to live (TTL) for cached authorizer results, in seconds.
        :param authorizer_type: The authorizer type.
        :param authorizer_uri: The authorizer's Uniform Resource Identifier (URI).
        :param enable_simple_responses: Specifies whether a Lambda authorizer returns a response in a simple
        format.
        :param identity_source: The identity source for which authorization is requested.
        :param identity_validation_expression: This parameter is not used.
        :param jwt_configuration: Represents the configuration of a JWT authorizer.
        :param name: The name of the authorizer.
        :returns: UpdateAuthorizerResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("UpdateDeployment")
    def update_deployment(
        self,
        context: RequestContext,
        api_id: _string,
        deployment_id: _string,
        description: StringWithLengthBetween0And1024 | None = None,
        **kwargs,
    ) -> UpdateDeploymentResponse:
        """Updates a Deployment.

        :param api_id: The API identifier.
        :param deployment_id: The deployment ID.
        :param description: The description for the deployment resource.
        :returns: UpdateDeploymentResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("UpdateDomainName")
    def update_domain_name(
        self,
        context: RequestContext,
        domain_name: _string,
        domain_name_configurations: DomainNameConfigurations | None = None,
        mutual_tls_authentication: MutualTlsAuthenticationInput | None = None,
        routing_mode: RoutingMode | None = None,
        **kwargs,
    ) -> UpdateDomainNameResponse:
        """Updates a domain name.

        :param domain_name: The domain name.
        :param domain_name_configurations: The domain name configurations.
        :param mutual_tls_authentication: The mutual TLS authentication configuration for a custom domain name.
        :param routing_mode: The routing mode.
        :returns: UpdateDomainNameResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("UpdateIntegration")
    def update_integration(
        self,
        context: RequestContext,
        api_id: _string,
        integration_id: _string,
        connection_id: StringWithLengthBetween1And1024 | None = None,
        connection_type: ConnectionType | None = None,
        content_handling_strategy: ContentHandlingStrategy | None = None,
        credentials_arn: Arn | None = None,
        description: StringWithLengthBetween0And1024 | None = None,
        integration_method: StringWithLengthBetween1And64 | None = None,
        integration_subtype: StringWithLengthBetween1And128 | None = None,
        integration_type: IntegrationType | None = None,
        integration_uri: UriWithLengthBetween1And2048 | None = None,
        passthrough_behavior: PassthroughBehavior | None = None,
        payload_format_version: StringWithLengthBetween1And64 | None = None,
        request_parameters: IntegrationParameters | None = None,
        request_templates: TemplateMap | None = None,
        response_parameters: ResponseParameters | None = None,
        template_selection_expression: SelectionExpression | None = None,
        timeout_in_millis: IntegerWithLengthBetween50And30000 | None = None,
        tls_config: TlsConfigInput | None = None,
        **kwargs,
    ) -> UpdateIntegrationResult:
        """Updates an Integration.

        :param api_id: The API identifier.
        :param integration_id: The integration ID.
        :param connection_id: The ID of the VPC link for a private integration.
        :param connection_type: The type of the network connection to the integration endpoint.
        :param content_handling_strategy: Supported only for WebSocket APIs.
        :param credentials_arn: Specifies the credentials required for the integration, if any.
        :param description: The description of the integration.
        :param integration_method: Specifies the integration's HTTP method type.
        :param integration_subtype: Supported only for HTTP API AWS_PROXY integrations.
        :param integration_type: The integration type of an integration.
        :param integration_uri: For a Lambda integration, specify the URI of a Lambda function.
        :param passthrough_behavior: Specifies the pass-through behavior for incoming requests based on the
        Content-Type header in the request, and the available mapping templates
        specified as the requestTemplates property on the Integration resource.
        :param payload_format_version: Specifies the format of the payload sent to an integration.
        :param request_parameters: For WebSocket APIs, a key-value map specifying request parameters that
        are passed from the method request to the backend.
        :param request_templates: Represents a map of Velocity templates that are applied on the request
        payload based on the value of the Content-Type header sent by the
        client.
        :param response_parameters: Supported only for HTTP APIs.
        :param template_selection_expression: The template selection expression for the integration.
        :param timeout_in_millis: Custom timeout between 50 and 29,000 milliseconds for WebSocket APIs and
        between 50 and 30,000 milliseconds for HTTP APIs.
        :param tls_config: The TLS configuration for a private integration.
        :returns: UpdateIntegrationResult
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("UpdateIntegrationResponse")
    def update_integration_response(
        self,
        context: RequestContext,
        api_id: _string,
        integration_response_id: _string,
        integration_id: _string,
        content_handling_strategy: ContentHandlingStrategy | None = None,
        integration_response_key: SelectionKey | None = None,
        response_parameters: IntegrationParameters | None = None,
        response_templates: TemplateMap | None = None,
        template_selection_expression: SelectionExpression | None = None,
        **kwargs,
    ) -> UpdateIntegrationResponseResponse:
        """Updates an IntegrationResponses.

        :param api_id: The API identifier.
        :param integration_response_id: The integration response ID.
        :param integration_id: The integration ID.
        :param content_handling_strategy: Supported only for WebSocket APIs.
        :param integration_response_key: The integration response key.
        :param response_parameters: A key-value map specifying response parameters that are passed to the
        method response from the backend.
        :param response_templates: The collection of response templates for the integration response as a
        string-to-string map of key-value pairs.
        :param template_selection_expression: The template selection expression for the integration response.
        :returns: UpdateIntegrationResponseResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("UpdateModel")
    def update_model(
        self,
        context: RequestContext,
        model_id: _string,
        api_id: _string,
        content_type: StringWithLengthBetween1And256 | None = None,
        description: StringWithLengthBetween0And1024 | None = None,
        name: StringWithLengthBetween1And128 | None = None,
        schema: StringWithLengthBetween0And32K | None = None,
        **kwargs,
    ) -> UpdateModelResponse:
        """Updates a Model.

        :param model_id: The model ID.
        :param api_id: The API identifier.
        :param content_type: The content-type for the model, for example, "application/json".
        :param description: The description of the model.
        :param name: The name of the model.
        :param schema: The schema for the model.
        :returns: UpdateModelResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("UpdatePortal")
    def update_portal(
        self,
        context: RequestContext,
        portal_id: _string,
        authorization: Authorization | None = None,
        endpoint_configuration: EndpointConfigurationRequest | None = None,
        included_portal_product_arns: _listOf__stringMin20Max2048 | None = None,
        logo_uri: _stringMin0Max1092 | None = None,
        portal_content: PortalContent | None = None,
        rum_app_monitor_name: _stringMin0Max255 | None = None,
        **kwargs,
    ) -> UpdatePortalResponse:
        """Updates a portal.

        :param portal_id: The portal identifier.
        :param authorization: The authorization of the portal.
        :param endpoint_configuration: Represents an endpoint configuration.
        :param included_portal_product_arns: The ARNs of the portal products included in the portal.
        :param logo_uri: The logo URI.
        :param portal_content: Contains the content that is visible to portal consumers including the
        themes, display names, and description.
        :param rum_app_monitor_name: The CloudWatch RUM app monitor name.
        :returns: UpdatePortalResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("UpdatePortalProduct")
    def update_portal_product(
        self,
        context: RequestContext,
        portal_product_id: _string,
        description: _stringMin0Max1024 | None = None,
        display_name: _stringMin1Max255 | None = None,
        display_order: DisplayOrder | None = None,
        **kwargs,
    ) -> UpdatePortalProductResponse:
        """Updates the portal product.

        :param portal_product_id: The portal product identifier.
        :param description: The description.
        :param display_name: The displayName.
        :param display_order: The display order.
        :returns: UpdatePortalProductResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("UpdateProductPage")
    def update_product_page(
        self,
        context: RequestContext,
        portal_product_id: _string,
        product_page_id: _string,
        display_content: DisplayContent | None = None,
        **kwargs,
    ) -> UpdateProductPageResponse:
        """Updates a product page of a portal product.

        :param portal_product_id: The portal product identifier.
        :param product_page_id: The portal product identifier.
        :param display_content: The content of the product page.
        :returns: UpdateProductPageResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("UpdateProductRestEndpointPage")
    def update_product_rest_endpoint_page(
        self,
        context: RequestContext,
        product_rest_endpoint_page_id: _string,
        portal_product_id: _string,
        display_content: EndpointDisplayContent | None = None,
        try_it_state: TryItState | None = None,
        **kwargs,
    ) -> UpdateProductRestEndpointPageResponse:
        """Updates a product REST endpoint page.

        :param product_rest_endpoint_page_id: The product REST endpoint identifier.
        :param portal_product_id: The portal product identifier.
        :param display_content: The display content.
        :param try_it_state: The try it state of a product REST endpoint page.
        :returns: UpdateProductRestEndpointPageResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("UpdateRoute")
    def update_route(
        self,
        context: RequestContext,
        api_id: _string,
        route_id: _string,
        api_key_required: _boolean | None = None,
        authorization_scopes: AuthorizationScopes | None = None,
        authorization_type: AuthorizationType | None = None,
        authorizer_id: Id | None = None,
        model_selection_expression: SelectionExpression | None = None,
        operation_name: StringWithLengthBetween1And64 | None = None,
        request_models: RouteModels | None = None,
        request_parameters: RouteParameters | None = None,
        route_key: SelectionKey | None = None,
        route_response_selection_expression: SelectionExpression | None = None,
        target: StringWithLengthBetween1And128 | None = None,
        **kwargs,
    ) -> UpdateRouteResult:
        """Updates a Route.

        :param api_id: The API identifier.
        :param route_id: The route ID.
        :param api_key_required: Specifies whether an API key is required for the route.
        :param authorization_scopes: The authorization scopes supported by this route.
        :param authorization_type: The authorization type for the route.
        :param authorizer_id: The identifier of the Authorizer resource to be associated with this
        route.
        :param model_selection_expression: The model selection expression for the route.
        :param operation_name: The operation name for the route.
        :param request_models: The request models for the route.
        :param request_parameters: The request parameters for the route.
        :param route_key: The route key for the route.
        :param route_response_selection_expression: The route response selection expression for the route.
        :param target: The target for the route.
        :returns: UpdateRouteResult
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("UpdateRouteResponse")
    def update_route_response(
        self,
        context: RequestContext,
        route_response_id: _string,
        api_id: _string,
        route_id: _string,
        model_selection_expression: SelectionExpression | None = None,
        response_models: RouteModels | None = None,
        response_parameters: RouteParameters | None = None,
        route_response_key: SelectionKey | None = None,
        **kwargs,
    ) -> UpdateRouteResponseResponse:
        """Updates a RouteResponse.

        :param route_response_id: The route response ID.
        :param api_id: The API identifier.
        :param route_id: The route ID.
        :param model_selection_expression: The model selection expression for the route response.
        :param response_models: The response models for the route response.
        :param response_parameters: The route response parameters.
        :param route_response_key: The route response key.
        :returns: UpdateRouteResponseResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("UpdateStage")
    def update_stage(
        self,
        context: RequestContext,
        stage_name: _string,
        api_id: _string,
        access_log_settings: AccessLogSettings | None = None,
        auto_deploy: _boolean | None = None,
        client_certificate_id: Id | None = None,
        default_route_settings: RouteSettings | None = None,
        deployment_id: Id | None = None,
        description: StringWithLengthBetween0And1024 | None = None,
        route_settings: RouteSettingsMap | None = None,
        stage_variables: StageVariablesMap | None = None,
        **kwargs,
    ) -> UpdateStageResponse:
        """Updates a Stage.

        :param stage_name: The stage name.
        :param api_id: The API identifier.
        :param access_log_settings: Settings for logging access in this stage.
        :param auto_deploy: Specifies whether updates to an API automatically trigger a new
        deployment.
        :param client_certificate_id: The identifier of a client certificate for a Stage.
        :param default_route_settings: The default route settings for the stage.
        :param deployment_id: The deployment identifier for the API stage.
        :param description: The description for the API stage.
        :param route_settings: Route settings for the stage.
        :param stage_variables: A map that defines the stage variables for a Stage.
        :returns: UpdateStageResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("UpdateVpcLink")
    def update_vpc_link(
        self,
        context: RequestContext,
        vpc_link_id: _string,
        name: StringWithLengthBetween1And128 | None = None,
        **kwargs,
    ) -> UpdateVpcLinkResponse:
        """Updates a VPC link.

        :param vpc_link_id: The ID of the VPC link.
        :param name: The name of the VPC link.
        :returns: UpdateVpcLinkResponse
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        """
        raise NotImplementedError
