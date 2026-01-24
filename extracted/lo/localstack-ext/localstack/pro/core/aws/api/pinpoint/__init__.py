from datetime import datetime
from enum import StrEnum
from typing import TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

_boolean = bool
_double = float
_integer = int
_string = str


class Action(StrEnum):
    OPEN_APP = "OPEN_APP"
    DEEP_LINK = "DEEP_LINK"
    URL = "URL"


class Alignment(StrEnum):
    LEFT = "LEFT"
    CENTER = "CENTER"
    RIGHT = "RIGHT"


class AttributeType(StrEnum):
    INCLUSIVE = "INCLUSIVE"
    EXCLUSIVE = "EXCLUSIVE"
    CONTAINS = "CONTAINS"
    BEFORE = "BEFORE"
    AFTER = "AFTER"
    ON = "ON"
    BETWEEN = "BETWEEN"


class ButtonAction(StrEnum):
    LINK = "LINK"
    DEEP_LINK = "DEEP_LINK"
    CLOSE = "CLOSE"


class CampaignStatus(StrEnum):
    SCHEDULED = "SCHEDULED"
    EXECUTING = "EXECUTING"
    PENDING_NEXT_RUN = "PENDING_NEXT_RUN"
    COMPLETED = "COMPLETED"
    PAUSED = "PAUSED"
    DELETED = "DELETED"
    INVALID = "INVALID"


class ChannelType(StrEnum):
    PUSH = "PUSH"
    GCM = "GCM"
    APNS = "APNS"
    APNS_SANDBOX = "APNS_SANDBOX"
    APNS_VOIP = "APNS_VOIP"
    APNS_VOIP_SANDBOX = "APNS_VOIP_SANDBOX"
    ADM = "ADM"
    SMS = "SMS"
    VOICE = "VOICE"
    EMAIL = "EMAIL"
    BAIDU = "BAIDU"
    CUSTOM = "CUSTOM"
    IN_APP = "IN_APP"


class DeliveryStatus(StrEnum):
    SUCCESSFUL = "SUCCESSFUL"
    THROTTLED = "THROTTLED"
    TEMPORARY_FAILURE = "TEMPORARY_FAILURE"
    PERMANENT_FAILURE = "PERMANENT_FAILURE"
    UNKNOWN_FAILURE = "UNKNOWN_FAILURE"
    OPT_OUT = "OPT_OUT"
    DUPLICATE = "DUPLICATE"


class DimensionType(StrEnum):
    INCLUSIVE = "INCLUSIVE"
    EXCLUSIVE = "EXCLUSIVE"


class Duration(StrEnum):
    HR_24 = "HR_24"
    DAY_7 = "DAY_7"
    DAY_14 = "DAY_14"
    DAY_30 = "DAY_30"


class FilterType(StrEnum):
    SYSTEM = "SYSTEM"
    ENDPOINT = "ENDPOINT"


class Format(StrEnum):
    CSV = "CSV"
    JSON = "JSON"


class Frequency(StrEnum):
    ONCE = "ONCE"
    HOURLY = "HOURLY"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    EVENT = "EVENT"
    IN_APP_EVENT = "IN_APP_EVENT"


class Include(StrEnum):
    ALL = "ALL"
    ANY = "ANY"
    NONE = "NONE"


class JobStatus(StrEnum):
    CREATED = "CREATED"
    PREPARING_FOR_INITIALIZATION = "PREPARING_FOR_INITIALIZATION"
    INITIALIZING = "INITIALIZING"
    PROCESSING = "PROCESSING"
    PENDING_JOB = "PENDING_JOB"
    COMPLETING = "COMPLETING"
    COMPLETED = "COMPLETED"
    FAILING = "FAILING"
    FAILED = "FAILED"


class JourneyRunStatus(StrEnum):
    SCHEDULED = "SCHEDULED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Layout(StrEnum):
    BOTTOM_BANNER = "BOTTOM_BANNER"
    TOP_BANNER = "TOP_BANNER"
    OVERLAYS = "OVERLAYS"
    MOBILE_FEED = "MOBILE_FEED"
    MIDDLE_BANNER = "MIDDLE_BANNER"
    CAROUSEL = "CAROUSEL"


class MessageType(StrEnum):
    TRANSACTIONAL = "TRANSACTIONAL"
    PROMOTIONAL = "PROMOTIONAL"


class Mode(StrEnum):
    DELIVERY = "DELIVERY"
    FILTER = "FILTER"


class Operator(StrEnum):
    ALL = "ALL"
    ANY = "ANY"


class RecencyType(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class SegmentType(StrEnum):
    DIMENSIONAL = "DIMENSIONAL"
    IMPORT = "IMPORT"


class SourceType(StrEnum):
    ALL = "ALL"
    ANY = "ANY"
    NONE = "NONE"


class State(StrEnum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    CLOSED = "CLOSED"
    PAUSED = "PAUSED"


class TemplateType(StrEnum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    VOICE = "VOICE"
    PUSH = "PUSH"
    INAPP = "INAPP"


class Type(StrEnum):
    ALL = "ALL"
    ANY = "ANY"
    NONE = "NONE"


class _EndpointTypesElement(StrEnum):
    PUSH = "PUSH"
    GCM = "GCM"
    APNS = "APNS"
    APNS_SANDBOX = "APNS_SANDBOX"
    APNS_VOIP = "APNS_VOIP"
    APNS_VOIP_SANDBOX = "APNS_VOIP_SANDBOX"
    ADM = "ADM"
    SMS = "SMS"
    VOICE = "VOICE"
    EMAIL = "EMAIL"
    BAIDU = "BAIDU"
    CUSTOM = "CUSTOM"
    IN_APP = "IN_APP"


class _TimezoneEstimationMethodsElement(StrEnum):
    PHONE_NUMBER = "PHONE_NUMBER"
    POSTAL_CODE = "POSTAL_CODE"


class DayOfWeek(StrEnum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"


class BadRequestException(ServiceException):
    """Provides information about an API request or response."""

    code: str = "BadRequestException"
    sender_fault: bool = False
    status_code: int = 400
    RequestID: _string | None


class ConflictException(ServiceException):
    """Provides information about an API request or response."""

    code: str = "ConflictException"
    sender_fault: bool = False
    status_code: int = 409
    RequestID: _string | None


class ForbiddenException(ServiceException):
    """Provides information about an API request or response."""

    code: str = "ForbiddenException"
    sender_fault: bool = False
    status_code: int = 403
    RequestID: _string | None


class InternalServerErrorException(ServiceException):
    """Provides information about an API request or response."""

    code: str = "InternalServerErrorException"
    sender_fault: bool = False
    status_code: int = 500
    RequestID: _string | None


class MethodNotAllowedException(ServiceException):
    """Provides information about an API request or response."""

    code: str = "MethodNotAllowedException"
    sender_fault: bool = False
    status_code: int = 405
    RequestID: _string | None


class NotFoundException(ServiceException):
    """Provides information about an API request or response."""

    code: str = "NotFoundException"
    sender_fault: bool = False
    status_code: int = 404
    RequestID: _string | None


class PayloadTooLargeException(ServiceException):
    """Provides information about an API request or response."""

    code: str = "PayloadTooLargeException"
    sender_fault: bool = False
    status_code: int = 413
    RequestID: _string | None


class TooManyRequestsException(ServiceException):
    """Provides information about an API request or response."""

    code: str = "TooManyRequestsException"
    sender_fault: bool = False
    status_code: int = 429
    RequestID: _string | None


class ADMChannelRequest(TypedDict, total=False):
    """Specifies the status and settings of the ADM (Amazon Device Messaging)
    channel for an application.
    """

    ClientId: _string
    ClientSecret: _string
    Enabled: _boolean | None


class ADMChannelResponse(TypedDict, total=False):
    """Provides information about the status and settings of the ADM (Amazon
    Device Messaging) channel for an application.
    """

    ApplicationId: _string | None
    CreationDate: _string | None
    Enabled: _boolean | None
    HasCredential: _boolean | None
    Id: _string | None
    IsArchived: _boolean | None
    LastModifiedBy: _string | None
    LastModifiedDate: _string | None
    Platform: _string
    Version: _integer | None


ListOf__string = list[_string]
MapOfListOf__string = dict[_string, ListOf__string]
MapOf__string = dict[_string, _string]


class ADMMessage(TypedDict, total=False):
    """Specifies the settings for a one-time message that's sent directly to an
    endpoint through the ADM (Amazon Device Messaging) channel.
    """

    Action: Action | None
    Body: _string | None
    ConsolidationKey: _string | None
    Data: MapOf__string | None
    ExpiresAfter: _string | None
    IconReference: _string | None
    ImageIconUrl: _string | None
    ImageUrl: _string | None
    MD5: _string | None
    RawContent: _string | None
    SilentPush: _boolean | None
    SmallImageIconUrl: _string | None
    Sound: _string | None
    Substitutions: MapOfListOf__string | None
    Title: _string | None
    Url: _string | None


class APNSChannelRequest(TypedDict, total=False):
    """Specifies the status and settings of the APNs (Apple Push Notification
    service) channel for an application.
    """

    BundleId: _string | None
    Certificate: _string | None
    DefaultAuthenticationMethod: _string | None
    Enabled: _boolean | None
    PrivateKey: _string | None
    TeamId: _string | None
    TokenKey: _string | None
    TokenKeyId: _string | None


class APNSChannelResponse(TypedDict, total=False):
    """Provides information about the status and settings of the APNs (Apple
    Push Notification service) channel for an application.
    """

    ApplicationId: _string | None
    CreationDate: _string | None
    DefaultAuthenticationMethod: _string | None
    Enabled: _boolean | None
    HasCredential: _boolean | None
    HasTokenKey: _boolean | None
    Id: _string | None
    IsArchived: _boolean | None
    LastModifiedBy: _string | None
    LastModifiedDate: _string | None
    Platform: _string
    Version: _integer | None


class APNSMessage(TypedDict, total=False):
    """Specifies the settings for a one-time message that's sent directly to an
    endpoint through the APNs (Apple Push Notification service) channel.
    """

    APNSPushType: _string | None
    Action: Action | None
    Badge: _integer | None
    Body: _string | None
    Category: _string | None
    CollapseId: _string | None
    Data: MapOf__string | None
    MediaUrl: _string | None
    PreferredAuthenticationMethod: _string | None
    Priority: _string | None
    RawContent: _string | None
    SilentPush: _boolean | None
    Sound: _string | None
    Substitutions: MapOfListOf__string | None
    ThreadId: _string | None
    TimeToLive: _integer | None
    Title: _string | None
    Url: _string | None


class APNSPushNotificationTemplate(TypedDict, total=False):
    """Specifies channel-specific content and settings for a message template
    that can be used in push notifications that are sent through the APNs
    (Apple Push Notification service) channel.
    """

    Action: Action | None
    Body: _string | None
    MediaUrl: _string | None
    RawContent: _string | None
    Sound: _string | None
    Title: _string | None
    Url: _string | None


class APNSSandboxChannelRequest(TypedDict, total=False):
    """Specifies the status and settings of the APNs (Apple Push Notification
    service) sandbox channel for an application.
    """

    BundleId: _string | None
    Certificate: _string | None
    DefaultAuthenticationMethod: _string | None
    Enabled: _boolean | None
    PrivateKey: _string | None
    TeamId: _string | None
    TokenKey: _string | None
    TokenKeyId: _string | None


class APNSSandboxChannelResponse(TypedDict, total=False):
    """Provides information about the status and settings of the APNs (Apple
    Push Notification service) sandbox channel for an application.
    """

    ApplicationId: _string | None
    CreationDate: _string | None
    DefaultAuthenticationMethod: _string | None
    Enabled: _boolean | None
    HasCredential: _boolean | None
    HasTokenKey: _boolean | None
    Id: _string | None
    IsArchived: _boolean | None
    LastModifiedBy: _string | None
    LastModifiedDate: _string | None
    Platform: _string
    Version: _integer | None


class APNSVoipChannelRequest(TypedDict, total=False):
    """Specifies the status and settings of the APNs (Apple Push Notification
    service) VoIP channel for an application.
    """

    BundleId: _string | None
    Certificate: _string | None
    DefaultAuthenticationMethod: _string | None
    Enabled: _boolean | None
    PrivateKey: _string | None
    TeamId: _string | None
    TokenKey: _string | None
    TokenKeyId: _string | None


class APNSVoipChannelResponse(TypedDict, total=False):
    """Provides information about the status and settings of the APNs (Apple
    Push Notification service) VoIP channel for an application.
    """

    ApplicationId: _string | None
    CreationDate: _string | None
    DefaultAuthenticationMethod: _string | None
    Enabled: _boolean | None
    HasCredential: _boolean | None
    HasTokenKey: _boolean | None
    Id: _string | None
    IsArchived: _boolean | None
    LastModifiedBy: _string | None
    LastModifiedDate: _string | None
    Platform: _string
    Version: _integer | None


class APNSVoipSandboxChannelRequest(TypedDict, total=False):
    """Specifies the status and settings of the APNs (Apple Push Notification
    service) VoIP sandbox channel for an application.
    """

    BundleId: _string | None
    Certificate: _string | None
    DefaultAuthenticationMethod: _string | None
    Enabled: _boolean | None
    PrivateKey: _string | None
    TeamId: _string | None
    TokenKey: _string | None
    TokenKeyId: _string | None


class APNSVoipSandboxChannelResponse(TypedDict, total=False):
    """Provides information about the status and settings of the APNs (Apple
    Push Notification service) VoIP sandbox channel for an application.
    """

    ApplicationId: _string | None
    CreationDate: _string | None
    DefaultAuthenticationMethod: _string | None
    Enabled: _boolean | None
    HasCredential: _boolean | None
    HasTokenKey: _boolean | None
    Id: _string | None
    IsArchived: _boolean | None
    LastModifiedBy: _string | None
    LastModifiedDate: _string | None
    Platform: _string
    Version: _integer | None


class ActivityResponse(TypedDict, total=False):
    """Provides information about an activity that was performed by a campaign."""

    ApplicationId: _string
    CampaignId: _string
    End: _string | None
    Id: _string
    Result: _string | None
    ScheduledStart: _string | None
    Start: _string | None
    State: _string | None
    SuccessfulEndpointCount: _integer | None
    TimezonesCompletedCount: _integer | None
    TimezonesTotalCount: _integer | None
    TotalEndpointCount: _integer | None
    TreatmentId: _string | None
    ExecutionMetrics: MapOf__string | None


ListOfActivityResponse = list[ActivityResponse]


class ActivitiesResponse(TypedDict, total=False):
    """Provides information about the activities that were performed by a
    campaign.
    """

    Item: ListOfActivityResponse
    NextToken: _string | None


class ContactCenterActivity(TypedDict, total=False):
    NextActivity: _string | None


class WaitTime(TypedDict, total=False):
    """Specifies a duration or a date and time that indicates when Amazon
    Pinpoint determines whether an activity's conditions have been met or an
    activity moves participants to the next activity in a journey.
    """

    WaitFor: _string | None
    WaitUntil: _string | None


class WaitActivity(TypedDict, total=False):
    """Specifies the settings for a wait activity in a journey. This type of
    activity waits for a certain amount of time or until a specific date and
    time before moving participants to the next activity in a journey.
    """

    NextActivity: _string | None
    WaitTime: WaitTime | None


class JourneySMSMessage(TypedDict, total=False):
    """Specifies the sender ID and message type for an SMS message that's sent
    to participants in a journey.
    """

    MessageType: MessageType | None
    OriginationNumber: _string | None
    SenderId: _string | None
    EntityId: _string | None
    TemplateId: _string | None


class SMSMessageActivity(TypedDict, total=False):
    """Specifies the settings for an SMS activity in a journey. This type of
    activity sends a text message to participants.
    """

    MessageConfig: JourneySMSMessage | None
    NextActivity: _string | None
    TemplateName: _string | None
    TemplateVersion: _string | None


class RandomSplitEntry(TypedDict, total=False):
    """Specifies the settings for a path in a random split activity in a
    journey.
    """

    NextActivity: _string | None
    Percentage: _integer | None


ListOfRandomSplitEntry = list[RandomSplitEntry]


class RandomSplitActivity(TypedDict, total=False):
    """Specifies the settings for a random split activity in a journey. This
    type of activity randomly sends specified percentages of participants
    down one of as many as five paths in a journey, based on conditions that
    you specify.
    """

    Branches: ListOfRandomSplitEntry | None


class JourneyPushMessage(TypedDict, total=False):
    """Specifies the message configuration for a push notification that's sent
    to participants in a journey.
    """

    TimeToLive: _string | None


class PushMessageActivity(TypedDict, total=False):
    """Specifies the settings for a push notification activity in a journey.
    This type of activity sends a push notification to participants.
    """

    MessageConfig: JourneyPushMessage | None
    NextActivity: _string | None
    TemplateName: _string | None
    TemplateVersion: _string | None


class AttributeDimension(TypedDict, total=False):
    """Specifies attribute-based criteria for including or excluding endpoints
    from a segment.
    """

    AttributeType: AttributeType | None
    Values: ListOf__string


MapOfAttributeDimension = dict[_string, AttributeDimension]


class MetricDimension(TypedDict, total=False):
    """Specifies metric-based criteria for including or excluding endpoints
    from a segment. These criteria derive from custom metrics that you
    define for endpoints.
    """

    ComparisonOperator: _string
    Value: _double


MapOfMetricDimension = dict[_string, MetricDimension]


class GPSCoordinates(TypedDict, total=False):
    """Specifies the GPS coordinates of a location."""

    Latitude: _double
    Longitude: _double


class GPSPointDimension(TypedDict, total=False):
    """Specifies GPS-based criteria for including or excluding endpoints from a
    segment.
    """

    Coordinates: GPSCoordinates
    RangeInKilometers: _double | None


class SetDimension(TypedDict, total=False):
    """Specifies the dimension type and values for a segment dimension."""

    DimensionType: DimensionType | None
    Values: ListOf__string


class SegmentLocation(TypedDict, total=False):
    """Specifies geographical dimension settings for a segment."""

    Country: SetDimension | None
    GPSPoint: GPSPointDimension | None


class SegmentDemographics(TypedDict, total=False):
    """Specifies demographic-based dimension settings for including or
    excluding endpoints from a segment. These settings derive from
    characteristics of endpoint devices, such as platform, make, and model.
    """

    AppVersion: SetDimension | None
    Channel: SetDimension | None
    DeviceType: SetDimension | None
    Make: SetDimension | None
    Model: SetDimension | None
    Platform: SetDimension | None


class RecencyDimension(TypedDict, total=False):
    """Specifies criteria for including or excluding endpoints from a segment
    based on how recently an endpoint was active.
    """

    Duration: Duration
    RecencyType: RecencyType


class SegmentBehaviors(TypedDict, total=False):
    """Specifies dimension settings for including or excluding endpoints from a
    segment based on how recently an endpoint was active.
    """

    Recency: RecencyDimension | None


class SegmentDimensions(TypedDict, total=False):
    """Specifies the dimension settings for a segment."""

    Attributes: MapOfAttributeDimension | None
    Behavior: SegmentBehaviors | None
    Demographic: SegmentDemographics | None
    Location: SegmentLocation | None
    Metrics: MapOfMetricDimension | None
    UserAttributes: MapOfAttributeDimension | None


class SegmentCondition(TypedDict, total=False):
    """Specifies a segment to associate with an activity in a journey."""

    SegmentId: _string


class EventDimensions(TypedDict, total=False):
    """Specifies the dimensions for an event filter that determines when a
    campaign is sent or a journey activity is performed.
    """

    Attributes: MapOfAttributeDimension | None
    EventType: SetDimension | None
    Metrics: MapOfMetricDimension | None


class EventCondition(TypedDict, total=False):
    """Specifies the conditions to evaluate for an event that applies to an
    activity in a journey.
    """

    Dimensions: EventDimensions | None
    MessageActivity: _string | None


class SimpleCondition(TypedDict, total=False):
    """Specifies a condition to evaluate for an activity in a journey."""

    EventCondition: EventCondition | None
    SegmentCondition: SegmentCondition | None
    SegmentDimensions: SegmentDimensions | None


class MultiConditionalBranch(TypedDict, total=False):
    """Specifies a condition to evaluate for an activity path in a journey."""

    Condition: SimpleCondition | None
    NextActivity: _string | None


ListOfMultiConditionalBranch = list[MultiConditionalBranch]


class MultiConditionalSplitActivity(TypedDict, total=False):
    """Specifies the settings for a multivariate split activity in a journey.
    This type of activity sends participants down one of as many as five
    paths (including a default *Else* path) in a journey, based on
    conditions that you specify.

    To create multivariate split activities that send participants down
    different paths based on push notification events (such as Open or
    Received events), your mobile app has to specify the User ID and
    Endpoint ID values. For more information, see `Integrating Amazon
    Pinpoint with your
    application <https://docs.aws.amazon.com/pinpoint/latest/developerguide/integrate.html>`__
    in the *Amazon Pinpoint Developer Guide*.
    """

    Branches: ListOfMultiConditionalBranch | None
    DefaultActivity: _string | None
    EvaluationWaitTime: WaitTime | None


class HoldoutActivity(TypedDict, total=False):
    """Specifies the settings for a holdout activity in a journey. This type of
    activity stops a journey for a specified percentage of participants.
    """

    NextActivity: _string | None
    Percentage: _integer


class JourneyEmailMessage(TypedDict, total=False):
    """Specifies the "From" address for an email message that's sent to
    participants in a journey.
    """

    FromAddress: _string | None


class EmailMessageActivity(TypedDict, total=False):
    """Specifies the settings for an email activity in a journey. This type of
    activity sends an email message to participants.
    """

    MessageConfig: JourneyEmailMessage | None
    NextActivity: _string | None
    TemplateName: _string | None
    TemplateVersion: _string | None


ListOfSimpleCondition = list[SimpleCondition]


class Condition(TypedDict, total=False):
    """Specifies the conditions to evaluate for an activity in a journey, and
    how to evaluate those conditions.
    """

    Conditions: ListOfSimpleCondition | None
    Operator: Operator | None


class ConditionalSplitActivity(TypedDict, total=False):
    """Specifies the settings for a yes/no split activity in a journey. This
    type of activity sends participants down one of two paths in a journey,
    based on conditions that you specify.

    To create yes/no split activities that send participants down different
    paths based on push notification events (such as Open or Received
    events), your mobile app has to specify the User ID and Endpoint ID
    values. For more information, see `Integrating Amazon Pinpoint with your
    application <https://docs.aws.amazon.com/pinpoint/latest/developerguide/integrate.html>`__
    in the *Amazon Pinpoint Developer Guide*.
    """

    Condition: Condition | None
    EvaluationWaitTime: WaitTime | None
    FalseActivity: _string | None
    TrueActivity: _string | None


class JourneyCustomMessage(TypedDict, total=False):
    """Specifies the message content for a custom channel message that's sent
    to participants in a journey.
    """

    Data: _string | None


ListOf__EndpointTypesElement = list[_EndpointTypesElement]


class CustomMessageActivity(TypedDict, total=False):
    """The settings for a custom message activity. This type of activity calls
    an AWS Lambda function or web hook that sends messages to participants.
    """

    DeliveryUri: _string | None
    EndpointTypes: ListOf__EndpointTypesElement | None
    MessageConfig: JourneyCustomMessage | None
    NextActivity: _string | None
    TemplateName: _string | None
    TemplateVersion: _string | None


class Activity(TypedDict, total=False):
    """Specifies the configuration and other settings for an activity in a
    journey.
    """

    CUSTOM: CustomMessageActivity | None
    ConditionalSplit: ConditionalSplitActivity | None
    Description: _string | None
    EMAIL: EmailMessageActivity | None
    Holdout: HoldoutActivity | None
    MultiCondition: MultiConditionalSplitActivity | None
    PUSH: PushMessageActivity | None
    RandomSplit: RandomSplitActivity | None
    SMS: SMSMessageActivity | None
    Wait: WaitActivity | None
    ContactCenter: ContactCenterActivity | None


class AddressConfiguration(TypedDict, total=False):
    """Specifies address-based configuration settings for a message that's sent
    directly to an endpoint.
    """

    BodyOverride: _string | None
    ChannelType: ChannelType | None
    Context: MapOf__string | None
    RawContent: _string | None
    Substitutions: MapOfListOf__string | None
    TitleOverride: _string | None


class AndroidPushNotificationTemplate(TypedDict, total=False):
    """Specifies channel-specific content and settings for a message template
    that can be used in push notifications that are sent through the ADM
    (Amazon Device Messaging), Baidu (Baidu Cloud Push), or GCM (Firebase
    Cloud Messaging, formerly Google Cloud Messaging) channel.
    """

    Action: Action | None
    Body: _string | None
    ImageIconUrl: _string | None
    ImageUrl: _string | None
    RawContent: _string | None
    SmallImageIconUrl: _string | None
    Sound: _string | None
    Title: _string | None
    Url: _string | None


_timestampIso8601 = datetime


class ResultRowValue(TypedDict, total=False):
    """Provides a single value and metadata about that value as part of an
    array of query results for a standard metric that applies to an
    application, campaign, or journey.
    """

    Key: _string
    Type: _string
    Value: _string


ListOfResultRowValue = list[ResultRowValue]


class ResultRow(TypedDict, total=False):
    """Provides the results of a query that retrieved the data for a standard
    metric that applies to an application, campaign, or journey.
    """

    GroupedBys: ListOfResultRowValue
    Values: ListOfResultRowValue


ListOfResultRow = list[ResultRow]


class BaseKpiResult(TypedDict, total=False):
    """Provides the results of a query that retrieved the data for a standard
    metric that applies to an application, campaign, or journey.
    """

    Rows: ListOfResultRow


class ApplicationDateRangeKpiResponse(TypedDict, total=False):
    """Provides the results of a query that retrieved the data for a standard
    metric that applies to an application, and provides information about
    that query.
    """

    ApplicationId: _string
    EndTime: _timestampIso8601
    KpiName: _string
    KpiResult: BaseKpiResult
    NextToken: _string | None
    StartTime: _timestampIso8601


class ApplicationResponse(TypedDict, total=False):
    """Provides information about an application."""

    Arn: _string
    Id: _string
    Name: _string
    tags: MapOf__string | None
    CreationDate: _string | None


class JourneyTimeframeCap(TypedDict, total=False):
    """The number of messages that can be sent to an endpoint during the
    specified timeframe for all journeys.
    """

    Cap: _integer | None
    Days: _integer | None


class ApplicationSettingsJourneyLimits(TypedDict, total=False):
    """The default sending limits for journeys in the application. To override
    these limits and define custom limits for a specific journey, use the
    Journey resource.
    """

    DailyCap: _integer | None
    TimeframeCap: JourneyTimeframeCap | None
    TotalCap: _integer | None


class QuietTime(TypedDict, total=False):
    """Specifies the start and end times that define a time range when messages
    aren't sent to endpoints.
    """

    End: _string | None
    Start: _string | None


class CampaignLimits(TypedDict, total=False):
    """For a campaign, specifies limits on the messages that the campaign can
    send. For an application, specifies the default limits for messages that
    campaigns in the application can send.
    """

    Daily: _integer | None
    MaximumDuration: _integer | None
    MessagesPerSecond: _integer | None
    Total: _integer | None
    Session: _integer | None


class CampaignHook(TypedDict, total=False):
    """Specifies settings for invoking an AWS Lambda function that customizes a
    segment for a campaign.
    """

    LambdaFunctionName: _string | None
    Mode: Mode | None
    WebUrl: _string | None


class ApplicationSettingsResource(TypedDict, total=False):
    """Provides information about an application, including the default
    settings for an application.
    """

    ApplicationId: _string
    CampaignHook: CampaignHook | None
    LastModifiedDate: _string | None
    Limits: CampaignLimits | None
    QuietTime: QuietTime | None
    JourneyLimits: ApplicationSettingsJourneyLimits | None


ListOfApplicationResponse = list[ApplicationResponse]


class ApplicationsResponse(TypedDict, total=False):
    """Provides information about all of your applications."""

    Item: ListOfApplicationResponse | None
    NextToken: _string | None


class AttributesResource(TypedDict, total=False):
    """Provides information about the type and the names of attributes that
    were removed from all the endpoints that are associated with an
    application.
    """

    ApplicationId: _string
    AttributeType: _string
    Attributes: ListOf__string | None


class BaiduChannelRequest(TypedDict, total=False):
    """Specifies the status and settings of the Baidu (Baidu Cloud Push)
    channel for an application.
    """

    ApiKey: _string
    Enabled: _boolean | None
    SecretKey: _string


class BaiduChannelResponse(TypedDict, total=False):
    """Provides information about the status and settings of the Baidu (Baidu
    Cloud Push) channel for an application.
    """

    ApplicationId: _string | None
    CreationDate: _string | None
    Credential: _string
    Enabled: _boolean | None
    HasCredential: _boolean | None
    Id: _string | None
    IsArchived: _boolean | None
    LastModifiedBy: _string | None
    LastModifiedDate: _string | None
    Platform: _string
    Version: _integer | None


class BaiduMessage(TypedDict, total=False):
    """Specifies the settings for a one-time message that's sent directly to an
    endpoint through the Baidu (Baidu Cloud Push) channel.
    """

    Action: Action | None
    Body: _string | None
    Data: MapOf__string | None
    IconReference: _string | None
    ImageIconUrl: _string | None
    ImageUrl: _string | None
    RawContent: _string | None
    SilentPush: _boolean | None
    SmallImageIconUrl: _string | None
    Sound: _string | None
    Substitutions: MapOfListOf__string | None
    TimeToLive: _integer | None
    Title: _string | None
    Url: _string | None


class CampaignCustomMessage(TypedDict, total=False):
    """Specifies the contents of a message that's sent through a custom channel
    to recipients of a campaign.
    """

    Data: _string | None


class CampaignDateRangeKpiResponse(TypedDict, total=False):
    """Provides the results of a query that retrieved the data for a standard
    metric that applies to a campaign, and provides information about that
    query.
    """

    ApplicationId: _string
    CampaignId: _string
    EndTime: _timestampIso8601
    KpiName: _string
    KpiResult: BaseKpiResult
    NextToken: _string | None
    StartTime: _timestampIso8601


class MessageHeader(TypedDict, total=False):
    """Contains the name and value pair of an email header to add to your
    email. You can have up to 15 MessageHeaders. A header can contain
    information such as the sender, receiver, route, or timestamp.
    """

    Name: _string | None
    Value: _string | None


ListOfMessageHeader = list[MessageHeader]


class CampaignEmailMessage(TypedDict, total=False):
    """Specifies the content and "From" address for an email message that's
    sent to recipients of a campaign.
    """

    Body: _string | None
    FromAddress: _string | None
    Headers: ListOfMessageHeader | None
    HtmlBody: _string | None
    Title: _string | None


class CampaignEventFilter(TypedDict, total=False):
    """Specifies the settings for events that cause a campaign to be sent."""

    Dimensions: EventDimensions
    FilterType: FilterType


class OverrideButtonConfiguration(TypedDict, total=False):
    """Override button configuration."""

    ButtonAction: ButtonAction
    Link: _string | None


class DefaultButtonConfiguration(TypedDict, total=False):
    """Default button configuration."""

    BackgroundColor: _string | None
    BorderRadius: _integer | None
    ButtonAction: ButtonAction
    Link: _string | None
    Text: _string
    TextColor: _string | None


class InAppMessageButton(TypedDict, total=False):
    """Button Config for an in-app message."""

    Android: OverrideButtonConfiguration | None
    DefaultConfig: DefaultButtonConfiguration | None
    IOS: OverrideButtonConfiguration | None
    Web: OverrideButtonConfiguration | None


class InAppMessageHeaderConfig(TypedDict, total=False):
    """Text config for Message Header."""

    Alignment: Alignment
    Header: _string
    TextColor: _string


class InAppMessageBodyConfig(TypedDict, total=False):
    """Text config for Message Body."""

    Alignment: Alignment
    Body: _string
    TextColor: _string


class InAppMessageContent(TypedDict, total=False):
    """The configuration for the message content."""

    BackgroundColor: _string | None
    BodyConfig: InAppMessageBodyConfig | None
    HeaderConfig: InAppMessageHeaderConfig | None
    ImageUrl: _string | None
    PrimaryBtn: InAppMessageButton | None
    SecondaryBtn: InAppMessageButton | None


ListOfInAppMessageContent = list[InAppMessageContent]


class CampaignInAppMessage(TypedDict, total=False):
    """In-app message configuration."""

    Body: _string | None
    Content: ListOfInAppMessageContent | None
    CustomConfig: MapOf__string | None
    Layout: Layout | None


class Template(TypedDict, total=False):
    """Specifies the name and version of the message template to use for the
    message.
    """

    Name: _string | None
    Version: _string | None


class TemplateConfiguration(TypedDict, total=False):
    """Specifies the message template to use for the message, for each type of
    channel.
    """

    EmailTemplate: Template | None
    PushTemplate: Template | None
    SMSTemplate: Template | None
    VoiceTemplate: Template | None
    InAppTemplate: Template | None


class CampaignState(TypedDict, total=False):
    """Provides information about the status of a campaign."""

    CampaignStatus: CampaignStatus | None


class Schedule(TypedDict, total=False):
    """Specifies the schedule settings for a campaign."""

    EndTime: _string | None
    EventFilter: CampaignEventFilter | None
    Frequency: Frequency | None
    IsLocalTime: _boolean | None
    QuietTime: QuietTime | None
    StartTime: _string
    Timezone: _string | None


class CampaignSmsMessage(TypedDict, total=False):
    """Specifies the content and settings for an SMS message that's sent to
    recipients of a campaign.
    """

    Body: _string | None
    MessageType: MessageType | None
    OriginationNumber: _string | None
    SenderId: _string | None
    EntityId: _string | None
    TemplateId: _string | None


class Message(TypedDict, total=False):
    """Specifies the content and settings for a push notification that's sent
    to recipients of a campaign.
    """

    Action: Action | None
    Body: _string | None
    ImageIconUrl: _string | None
    ImageSmallIconUrl: _string | None
    ImageUrl: _string | None
    JsonBody: _string | None
    MediaUrl: _string | None
    RawContent: _string | None
    SilentPush: _boolean | None
    TimeToLive: _integer | None
    Title: _string | None
    Url: _string | None


class MessageConfiguration(TypedDict, total=False):
    """Specifies the message configuration settings for a campaign."""

    ADMMessage: Message | None
    APNSMessage: Message | None
    BaiduMessage: Message | None
    CustomMessage: CampaignCustomMessage | None
    DefaultMessage: Message | None
    EmailMessage: CampaignEmailMessage | None
    GCMMessage: Message | None
    SMSMessage: CampaignSmsMessage | None
    InAppMessage: CampaignInAppMessage | None


class CustomDeliveryConfiguration(TypedDict, total=False):
    """Specifies the delivery configuration settings for sending a campaign or
    campaign treatment through a custom channel. This object is required if
    you use the CampaignCustomMessage object to define the message to send
    for the campaign or campaign treatment.
    """

    DeliveryUri: _string
    EndpointTypes: ListOf__EndpointTypesElement | None


class TreatmentResource(TypedDict, total=False):
    """Specifies the settings for a campaign treatment. A *treatment* is a
    variation of a campaign that's used for A/B testing of a campaign.
    """

    CustomDeliveryConfiguration: CustomDeliveryConfiguration | None
    Id: _string
    MessageConfiguration: MessageConfiguration | None
    Schedule: Schedule | None
    SizePercent: _integer
    State: CampaignState | None
    TemplateConfiguration: TemplateConfiguration | None
    TreatmentDescription: _string | None
    TreatmentName: _string | None


ListOfTreatmentResource = list[TreatmentResource]


class CampaignResponse(TypedDict, total=False):
    """Provides information about the status, configuration, and other settings
    for a campaign.
    """

    AdditionalTreatments: ListOfTreatmentResource | None
    ApplicationId: _string
    Arn: _string
    CreationDate: _string
    CustomDeliveryConfiguration: CustomDeliveryConfiguration | None
    DefaultState: CampaignState | None
    Description: _string | None
    HoldoutPercent: _integer | None
    Hook: CampaignHook | None
    Id: _string
    IsPaused: _boolean | None
    LastModifiedDate: _string
    Limits: CampaignLimits | None
    MessageConfiguration: MessageConfiguration | None
    Name: _string | None
    Schedule: Schedule | None
    SegmentId: _string
    SegmentVersion: _integer
    State: CampaignState | None
    tags: MapOf__string | None
    TemplateConfiguration: TemplateConfiguration | None
    TreatmentDescription: _string | None
    TreatmentName: _string | None
    Version: _integer | None
    Priority: _integer | None


ListOfCampaignResponse = list[CampaignResponse]


class CampaignsResponse(TypedDict, total=False):
    """Provides information about the configuration and other settings for all
    the campaigns that are associated with an application.
    """

    Item: ListOfCampaignResponse
    NextToken: _string | None


class ChannelResponse(TypedDict, total=False):
    """Provides information about the general settings and status of a channel
    for an application.
    """

    ApplicationId: _string | None
    CreationDate: _string | None
    Enabled: _boolean | None
    HasCredential: _boolean | None
    Id: _string | None
    IsArchived: _boolean | None
    LastModifiedBy: _string | None
    LastModifiedDate: _string | None
    Version: _integer | None


MapOfChannelResponse = dict[_string, ChannelResponse]


class ChannelsResponse(TypedDict, total=False):
    """Provides information about the general settings and status of all
    channels for an application, including channels that aren't enabled for
    the application.
    """

    Channels: MapOfChannelResponse


class CreateApplicationRequest(TypedDict, total=False):
    """Specifies the display name of an application and the tags to associate
    with the application.
    """

    Name: _string
    tags: MapOf__string | None


class CreateAppRequest(ServiceRequest):
    CreateApplicationRequest: CreateApplicationRequest


class CreateAppResponse(TypedDict, total=False):
    ApplicationResponse: ApplicationResponse


class WriteTreatmentResource(TypedDict, total=False):
    """Specifies the settings for a campaign treatment. A *treatment* is a
    variation of a campaign that's used for A/B testing of a campaign.
    """

    CustomDeliveryConfiguration: CustomDeliveryConfiguration | None
    MessageConfiguration: MessageConfiguration | None
    Schedule: Schedule | None
    SizePercent: _integer
    TemplateConfiguration: TemplateConfiguration | None
    TreatmentDescription: _string | None
    TreatmentName: _string | None


ListOfWriteTreatmentResource = list[WriteTreatmentResource]


class WriteCampaignRequest(TypedDict, total=False):
    """Specifies the configuration and other settings for a campaign."""

    AdditionalTreatments: ListOfWriteTreatmentResource | None
    CustomDeliveryConfiguration: CustomDeliveryConfiguration | None
    Description: _string | None
    HoldoutPercent: _integer | None
    Hook: CampaignHook | None
    IsPaused: _boolean | None
    Limits: CampaignLimits | None
    MessageConfiguration: MessageConfiguration | None
    Name: _string | None
    Schedule: Schedule | None
    SegmentId: _string | None
    SegmentVersion: _integer | None
    tags: MapOf__string | None
    TemplateConfiguration: TemplateConfiguration | None
    TreatmentDescription: _string | None
    TreatmentName: _string | None
    Priority: _integer | None


class CreateCampaignRequest(ServiceRequest):
    ApplicationId: _string
    WriteCampaignRequest: WriteCampaignRequest


class CreateCampaignResponse(TypedDict, total=False):
    CampaignResponse: CampaignResponse


class EmailTemplateRequest(TypedDict, total=False):
    """Specifies the content and settings for a message template that can be
    used in messages that are sent through the email channel.
    """

    DefaultSubstitutions: _string | None
    HtmlPart: _string | None
    RecommenderId: _string | None
    Subject: _string | None
    Headers: ListOfMessageHeader | None
    tags: MapOf__string | None
    TemplateDescription: _string | None
    TextPart: _string | None


class CreateEmailTemplateRequest(ServiceRequest):
    EmailTemplateRequest: EmailTemplateRequest
    TemplateName: _string


class CreateTemplateMessageBody(TypedDict, total=False):
    """Provides information about a request to create a message template."""

    Arn: _string | None
    Message: _string | None
    RequestID: _string | None


class CreateEmailTemplateResponse(TypedDict, total=False):
    CreateTemplateMessageBody: CreateTemplateMessageBody


class ExportJobRequest(TypedDict, total=False):
    """Specifies the settings for a job that exports endpoint definitions to an
    Amazon Simple Storage Service (Amazon S3) bucket.
    """

    RoleArn: _string
    S3UrlPrefix: _string
    SegmentId: _string | None
    SegmentVersion: _integer | None


class CreateExportJobRequest(ServiceRequest):
    ApplicationId: _string
    ExportJobRequest: ExportJobRequest


class ExportJobResource(TypedDict, total=False):
    """Provides information about the resource settings for a job that exports
    endpoint definitions to a file. The file can be added directly to an
    Amazon Simple Storage Service (Amazon S3) bucket by using the Amazon
    Pinpoint API or downloaded directly to a computer by using the Amazon
    Pinpoint console.
    """

    RoleArn: _string
    S3UrlPrefix: _string
    SegmentId: _string | None
    SegmentVersion: _integer | None


class ExportJobResponse(TypedDict, total=False):
    """Provides information about the status and settings of a job that exports
    endpoint definitions to a file. The file can be added directly to an
    Amazon Simple Storage Service (Amazon S3) bucket by using the Amazon
    Pinpoint API or downloaded directly to a computer by using the Amazon
    Pinpoint console.
    """

    ApplicationId: _string
    CompletedPieces: _integer | None
    CompletionDate: _string | None
    CreationDate: _string
    Definition: ExportJobResource
    FailedPieces: _integer | None
    Failures: ListOf__string | None
    Id: _string
    JobStatus: JobStatus
    TotalFailures: _integer | None
    TotalPieces: _integer | None
    TotalProcessed: _integer | None
    Type: _string


class CreateExportJobResponse(TypedDict, total=False):
    ExportJobResponse: ExportJobResponse


class ImportJobRequest(TypedDict, total=False):
    """Specifies the settings for a job that imports endpoint definitions from
    an Amazon Simple Storage Service (Amazon S3) bucket.
    """

    DefineSegment: _boolean | None
    ExternalId: _string | None
    Format: Format
    RegisterEndpoints: _boolean | None
    RoleArn: _string
    S3Url: _string
    SegmentId: _string | None
    SegmentName: _string | None


class CreateImportJobRequest(ServiceRequest):
    ApplicationId: _string
    ImportJobRequest: ImportJobRequest


class ImportJobResource(TypedDict, total=False):
    """Provides information about the resource settings for a job that imports
    endpoint definitions from one or more files. The files can be stored in
    an Amazon Simple Storage Service (Amazon S3) bucket or uploaded directly
    from a computer by using the Amazon Pinpoint console.
    """

    DefineSegment: _boolean | None
    ExternalId: _string | None
    Format: Format
    RegisterEndpoints: _boolean | None
    RoleArn: _string
    S3Url: _string
    SegmentId: _string | None
    SegmentName: _string | None


class ImportJobResponse(TypedDict, total=False):
    """Provides information about the status and settings of a job that imports
    endpoint definitions from one or more files. The files can be stored in
    an Amazon Simple Storage Service (Amazon S3) bucket or uploaded directly
    from a computer by using the Amazon Pinpoint console.
    """

    ApplicationId: _string
    CompletedPieces: _integer | None
    CompletionDate: _string | None
    CreationDate: _string
    Definition: ImportJobResource
    FailedPieces: _integer | None
    Failures: ListOf__string | None
    Id: _string
    JobStatus: JobStatus
    TotalFailures: _integer | None
    TotalPieces: _integer | None
    TotalProcessed: _integer | None
    Type: _string


class CreateImportJobResponse(TypedDict, total=False):
    ImportJobResponse: ImportJobResponse


class InAppTemplateRequest(TypedDict, total=False):
    """InApp Template Request."""

    Content: ListOfInAppMessageContent | None
    CustomConfig: MapOf__string | None
    Layout: Layout | None
    tags: MapOf__string | None
    TemplateDescription: _string | None


class CreateInAppTemplateRequest(ServiceRequest):
    InAppTemplateRequest: InAppTemplateRequest
    TemplateName: _string


class TemplateCreateMessageBody(TypedDict, total=False):
    """Provides information about a request to create a message template."""

    Arn: _string | None
    Message: _string | None
    RequestID: _string | None


class CreateInAppTemplateResponse(TypedDict, total=False):
    TemplateCreateMessageBody: TemplateCreateMessageBody


ListOf__TimezoneEstimationMethodsElement = list[_TimezoneEstimationMethodsElement]


class ClosedDaysRule(TypedDict, total=False):
    """Specifies the rule settings for when messages can't be sent."""

    Name: _string | None
    StartDateTime: _string | None
    EndDateTime: _string | None


ListOfClosedDaysRules = list[ClosedDaysRule]


class ClosedDays(TypedDict, total=False):
    """The time when a journey will not send messages. QuietTime should be
    configured first and SendingSchedule should be set to true.
    """

    EMAIL: ListOfClosedDaysRules | None
    SMS: ListOfClosedDaysRules | None
    PUSH: ListOfClosedDaysRules | None
    VOICE: ListOfClosedDaysRules | None
    CUSTOM: ListOfClosedDaysRules | None


class OpenHoursRule(TypedDict, total=False):
    """Specifies the start and end time for OpenHours."""

    StartTime: _string | None
    EndTime: _string | None


ListOfOpenHoursRules = list[OpenHoursRule]
MapOfListOfOpenHoursRules = dict[DayOfWeek, ListOfOpenHoursRules]


class OpenHours(TypedDict, total=False):
    """Specifies the times when message are allowed to be sent to endpoints."""

    EMAIL: MapOfListOfOpenHoursRules | None
    SMS: MapOfListOfOpenHoursRules | None
    PUSH: MapOfListOfOpenHoursRules | None
    VOICE: MapOfListOfOpenHoursRules | None
    CUSTOM: MapOfListOfOpenHoursRules | None


class JourneyChannelSettings(TypedDict, total=False):
    """The channel-specific configurations for the journey."""

    ConnectCampaignArn: _string | None
    ConnectCampaignExecutionRoleArn: _string | None


class EventFilter(TypedDict, total=False):
    """Specifies the settings for an event that causes a campaign to be sent or
    a journey activity to be performed.
    """

    Dimensions: EventDimensions
    FilterType: FilterType


class EventStartCondition(TypedDict, total=False):
    """Specifies the settings for an event that causes a journey activity to
    start.
    """

    EventFilter: EventFilter | None
    SegmentId: _string | None


class StartCondition(TypedDict, total=False):
    """Specifies the conditions for the first activity in a journey. This
    activity and its conditions determine which users are participants in a
    journey.
    """

    Description: _string | None
    EventStartCondition: EventStartCondition | None
    SegmentStartCondition: SegmentCondition | None


class JourneySchedule(TypedDict, total=False):
    """Specifies the schedule settings for a journey."""

    EndTime: _timestampIso8601 | None
    StartTime: _timestampIso8601 | None
    Timezone: _string | None


class JourneyLimits(TypedDict, total=False):
    """Specifies limits on the messages that a journey can send and the number
    of times participants can enter a journey.
    """

    DailyCap: _integer | None
    EndpointReentryCap: _integer | None
    MessagesPerSecond: _integer | None
    EndpointReentryInterval: _string | None
    TimeframeCap: JourneyTimeframeCap | None
    TotalCap: _integer | None


MapOfActivity = dict[_string, Activity]


class WriteJourneyRequest(TypedDict, total=False):
    """Specifies the configuration and other settings for a journey."""

    Activities: MapOfActivity | None
    CreationDate: _string | None
    LastModifiedDate: _string | None
    Limits: JourneyLimits | None
    LocalTime: _boolean | None
    Name: _string
    QuietTime: QuietTime | None
    RefreshFrequency: _string | None
    Schedule: JourneySchedule | None
    StartActivity: _string | None
    StartCondition: StartCondition | None
    State: State | None
    WaitForQuietTime: _boolean | None
    RefreshOnSegmentUpdate: _boolean | None
    JourneyChannelSettings: JourneyChannelSettings | None
    SendingSchedule: _boolean | None
    OpenHours: OpenHours | None
    ClosedDays: ClosedDays | None
    TimezoneEstimationMethods: ListOf__TimezoneEstimationMethodsElement | None


class CreateJourneyRequest(ServiceRequest):
    ApplicationId: _string
    WriteJourneyRequest: WriteJourneyRequest


class JourneyResponse(TypedDict, total=False):
    """Provides information about the status, configuration, and other settings
    for a journey.
    """

    Activities: MapOfActivity | None
    ApplicationId: _string
    CreationDate: _string | None
    Id: _string
    LastModifiedDate: _string | None
    Limits: JourneyLimits | None
    LocalTime: _boolean | None
    Name: _string
    QuietTime: QuietTime | None
    RefreshFrequency: _string | None
    Schedule: JourneySchedule | None
    StartActivity: _string | None
    StartCondition: StartCondition | None
    State: State | None
    tags: MapOf__string | None
    WaitForQuietTime: _boolean | None
    RefreshOnSegmentUpdate: _boolean | None
    JourneyChannelSettings: JourneyChannelSettings | None
    SendingSchedule: _boolean | None
    OpenHours: OpenHours | None
    ClosedDays: ClosedDays | None
    TimezoneEstimationMethods: ListOf__TimezoneEstimationMethodsElement | None


class CreateJourneyResponse(TypedDict, total=False):
    JourneyResponse: JourneyResponse


class DefaultPushNotificationTemplate(TypedDict, total=False):
    """Specifies the default settings and content for a message template that
    can be used in messages that are sent through a push notification
    channel.
    """

    Action: Action | None
    Body: _string | None
    Sound: _string | None
    Title: _string | None
    Url: _string | None


class PushNotificationTemplateRequest(TypedDict, total=False):
    """Specifies the content and settings for a message template that can be
    used in messages that are sent through a push notification channel.
    """

    ADM: AndroidPushNotificationTemplate | None
    APNS: APNSPushNotificationTemplate | None
    Baidu: AndroidPushNotificationTemplate | None
    Default: DefaultPushNotificationTemplate | None
    DefaultSubstitutions: _string | None
    GCM: AndroidPushNotificationTemplate | None
    RecommenderId: _string | None
    tags: MapOf__string | None
    TemplateDescription: _string | None


class CreatePushTemplateRequest(ServiceRequest):
    PushNotificationTemplateRequest: PushNotificationTemplateRequest
    TemplateName: _string


class CreatePushTemplateResponse(TypedDict, total=False):
    CreateTemplateMessageBody: CreateTemplateMessageBody


class CreateRecommenderConfiguration(TypedDict, total=False):
    """Specifies Amazon Pinpoint configuration settings for retrieving and
    processing recommendation data from a recommender model.
    """

    Attributes: MapOf__string | None
    Description: _string | None
    Name: _string | None
    RecommendationProviderIdType: _string | None
    RecommendationProviderRoleArn: _string
    RecommendationProviderUri: _string
    RecommendationTransformerUri: _string | None
    RecommendationsDisplayName: _string | None
    RecommendationsPerMessage: _integer | None


class CreateRecommenderConfigurationRequest(ServiceRequest):
    CreateRecommenderConfiguration: CreateRecommenderConfiguration


class RecommenderConfigurationResponse(TypedDict, total=False):
    """Provides information about Amazon Pinpoint configuration settings for
    retrieving and processing data from a recommender model.
    """

    Attributes: MapOf__string | None
    CreationDate: _string
    Description: _string | None
    Id: _string
    LastModifiedDate: _string
    Name: _string | None
    RecommendationProviderIdType: _string | None
    RecommendationProviderRoleArn: _string
    RecommendationProviderUri: _string
    RecommendationTransformerUri: _string | None
    RecommendationsDisplayName: _string | None
    RecommendationsPerMessage: _integer | None


class CreateRecommenderConfigurationResponse(TypedDict, total=False):
    RecommenderConfigurationResponse: RecommenderConfigurationResponse


class SegmentReference(TypedDict, total=False):
    """Specifies the segment identifier and version of a segment."""

    Id: _string
    Version: _integer | None


ListOfSegmentReference = list[SegmentReference]
ListOfSegmentDimensions = list[SegmentDimensions]


class SegmentGroup(TypedDict, total=False):
    """Specifies the base segments and dimensions for a segment, and the
    relationships between these base segments and dimensions.
    """

    Dimensions: ListOfSegmentDimensions | None
    SourceSegments: ListOfSegmentReference | None
    SourceType: SourceType | None
    Type: Type | None


ListOfSegmentGroup = list[SegmentGroup]


class SegmentGroupList(TypedDict, total=False):
    """Specifies the settings that define the relationships between segment
    groups for a segment.
    """

    Groups: ListOfSegmentGroup | None
    Include: Include | None


class WriteSegmentRequest(TypedDict, total=False):
    """Specifies the configuration, dimension, and other settings for a
    segment. A WriteSegmentRequest object can include a Dimensions object or
    a SegmentGroups object, but not both.
    """

    Dimensions: SegmentDimensions | None
    Name: _string | None
    SegmentGroups: SegmentGroupList | None
    tags: MapOf__string | None


class CreateSegmentRequest(ServiceRequest):
    ApplicationId: _string
    WriteSegmentRequest: WriteSegmentRequest


MapOf__integer = dict[_string, _integer]


class SegmentImportResource(TypedDict, total=False):
    """Provides information about the import job that created a segment. An
    import job is a job that creates a user segment by importing endpoint
    definitions.
    """

    ChannelCounts: MapOf__integer | None
    ExternalId: _string
    Format: Format
    RoleArn: _string
    S3Url: _string
    Size: _integer


class SegmentResponse(TypedDict, total=False):
    """Provides information about the configuration, dimension, and other
    settings for a segment.
    """

    ApplicationId: _string
    Arn: _string
    CreationDate: _string
    Dimensions: SegmentDimensions | None
    Id: _string
    ImportDefinition: SegmentImportResource | None
    LastModifiedDate: _string | None
    Name: _string | None
    SegmentGroups: SegmentGroupList | None
    SegmentType: SegmentType
    tags: MapOf__string | None
    Version: _integer | None


class CreateSegmentResponse(TypedDict, total=False):
    SegmentResponse: SegmentResponse


class SMSTemplateRequest(TypedDict, total=False):
    """Specifies the content and settings for a message template that can be
    used in text messages that are sent through the SMS channel.
    """

    Body: _string | None
    DefaultSubstitutions: _string | None
    RecommenderId: _string | None
    tags: MapOf__string | None
    TemplateDescription: _string | None


class CreateSmsTemplateRequest(ServiceRequest):
    SMSTemplateRequest: SMSTemplateRequest
    TemplateName: _string


class CreateSmsTemplateResponse(TypedDict, total=False):
    CreateTemplateMessageBody: CreateTemplateMessageBody


class VoiceTemplateRequest(TypedDict, total=False):
    """Specifies the content and settings for a message template that can be
    used in messages that are sent through the voice channel.
    """

    Body: _string | None
    DefaultSubstitutions: _string | None
    LanguageCode: _string | None
    tags: MapOf__string | None
    TemplateDescription: _string | None
    VoiceId: _string | None


class CreateVoiceTemplateRequest(ServiceRequest):
    TemplateName: _string
    VoiceTemplateRequest: VoiceTemplateRequest


class CreateVoiceTemplateResponse(TypedDict, total=False):
    CreateTemplateMessageBody: CreateTemplateMessageBody


class DefaultMessage(TypedDict, total=False):
    """Specifies the default message for all channels."""

    Body: _string | None
    Substitutions: MapOfListOf__string | None


class DefaultPushNotificationMessage(TypedDict, total=False):
    """Specifies the default settings and content for a push notification
    that's sent directly to an endpoint.
    """

    Action: Action | None
    Body: _string | None
    Data: MapOf__string | None
    SilentPush: _boolean | None
    Substitutions: MapOfListOf__string | None
    Title: _string | None
    Url: _string | None


class DeleteAdmChannelRequest(ServiceRequest):
    ApplicationId: _string


class DeleteAdmChannelResponse(TypedDict, total=False):
    ADMChannelResponse: ADMChannelResponse


class DeleteApnsChannelRequest(ServiceRequest):
    ApplicationId: _string


class DeleteApnsChannelResponse(TypedDict, total=False):
    APNSChannelResponse: APNSChannelResponse


class DeleteApnsSandboxChannelRequest(ServiceRequest):
    ApplicationId: _string


class DeleteApnsSandboxChannelResponse(TypedDict, total=False):
    APNSSandboxChannelResponse: APNSSandboxChannelResponse


class DeleteApnsVoipChannelRequest(ServiceRequest):
    ApplicationId: _string


class DeleteApnsVoipChannelResponse(TypedDict, total=False):
    APNSVoipChannelResponse: APNSVoipChannelResponse


class DeleteApnsVoipSandboxChannelRequest(ServiceRequest):
    ApplicationId: _string


class DeleteApnsVoipSandboxChannelResponse(TypedDict, total=False):
    APNSVoipSandboxChannelResponse: APNSVoipSandboxChannelResponse


class DeleteAppRequest(ServiceRequest):
    ApplicationId: _string


class DeleteAppResponse(TypedDict, total=False):
    ApplicationResponse: ApplicationResponse


class DeleteBaiduChannelRequest(ServiceRequest):
    ApplicationId: _string


class DeleteBaiduChannelResponse(TypedDict, total=False):
    BaiduChannelResponse: BaiduChannelResponse


class DeleteCampaignRequest(ServiceRequest):
    ApplicationId: _string
    CampaignId: _string


class DeleteCampaignResponse(TypedDict, total=False):
    CampaignResponse: CampaignResponse


class DeleteEmailChannelRequest(ServiceRequest):
    ApplicationId: _string


class EmailChannelResponse(TypedDict, total=False):
    """Provides information about the status and settings of the email channel
    for an application.
    """

    ApplicationId: _string | None
    ConfigurationSet: _string | None
    CreationDate: _string | None
    Enabled: _boolean | None
    FromAddress: _string | None
    HasCredential: _boolean | None
    Id: _string | None
    Identity: _string | None
    IsArchived: _boolean | None
    LastModifiedBy: _string | None
    LastModifiedDate: _string | None
    MessagesPerSecond: _integer | None
    Platform: _string
    RoleArn: _string | None
    OrchestrationSendingRoleArn: _string | None
    Version: _integer | None


class DeleteEmailChannelResponse(TypedDict, total=False):
    EmailChannelResponse: EmailChannelResponse


class DeleteEmailTemplateRequest(ServiceRequest):
    TemplateName: _string
    Version: _string | None


class MessageBody(TypedDict, total=False):
    """Provides information about an API request or response."""

    Message: _string | None
    RequestID: _string | None


class DeleteEmailTemplateResponse(TypedDict, total=False):
    MessageBody: MessageBody


class DeleteEndpointRequest(ServiceRequest):
    ApplicationId: _string
    EndpointId: _string


class EndpointUser(TypedDict, total=False):
    """Specifies data for one or more attributes that describe the user who's
    associated with an endpoint.
    """

    UserAttributes: MapOfListOf__string | None
    UserId: _string | None


MapOf__double = dict[_string, _double]


class EndpointLocation(TypedDict, total=False):
    """Specifies geographic information about an endpoint."""

    City: _string | None
    Country: _string | None
    Latitude: _double | None
    Longitude: _double | None
    PostalCode: _string | None
    Region: _string | None


class EndpointDemographic(TypedDict, total=False):
    """Specifies demographic information about an endpoint, such as the
    applicable time zone and platform.
    """

    AppVersion: _string | None
    Locale: _string | None
    Make: _string | None
    Model: _string | None
    ModelVersion: _string | None
    Platform: _string | None
    PlatformVersion: _string | None
    Timezone: _string | None


class EndpointResponse(TypedDict, total=False):
    """Provides information about the channel type and other settings for an
    endpoint.
    """

    Address: _string | None
    ApplicationId: _string | None
    Attributes: MapOfListOf__string | None
    ChannelType: ChannelType | None
    CohortId: _string | None
    CreationDate: _string | None
    Demographic: EndpointDemographic | None
    EffectiveDate: _string | None
    EndpointStatus: _string | None
    Id: _string | None
    Location: EndpointLocation | None
    Metrics: MapOf__double | None
    OptOut: _string | None
    RequestId: _string | None
    User: EndpointUser | None


class DeleteEndpointResponse(TypedDict, total=False):
    EndpointResponse: EndpointResponse


class DeleteEventStreamRequest(ServiceRequest):
    ApplicationId: _string


class EventStream(TypedDict, total=False):
    """Specifies settings for publishing event data to an Amazon Kinesis data
    stream or an Amazon Kinesis Data Firehose delivery stream.
    """

    ApplicationId: _string
    DestinationStreamArn: _string
    ExternalId: _string | None
    LastModifiedDate: _string | None
    LastUpdatedBy: _string | None
    RoleArn: _string


class DeleteEventStreamResponse(TypedDict, total=False):
    EventStream: EventStream


class DeleteGcmChannelRequest(ServiceRequest):
    ApplicationId: _string


class GCMChannelResponse(TypedDict, total=False):
    """Provides information about the status and settings of the GCM channel
    for an application. The GCM channel enables Amazon Pinpoint to send push
    notifications through the Firebase Cloud Messaging (FCM), formerly
    Google Cloud Messaging (GCM), service.
    """

    ApplicationId: _string | None
    CreationDate: _string | None
    Credential: _string | None
    DefaultAuthenticationMethod: _string | None
    Enabled: _boolean | None
    HasCredential: _boolean | None
    HasFcmServiceCredentials: _boolean | None
    Id: _string | None
    IsArchived: _boolean | None
    LastModifiedBy: _string | None
    LastModifiedDate: _string | None
    Platform: _string
    Version: _integer | None


class DeleteGcmChannelResponse(TypedDict, total=False):
    GCMChannelResponse: GCMChannelResponse


class DeleteInAppTemplateRequest(ServiceRequest):
    TemplateName: _string
    Version: _string | None


class DeleteInAppTemplateResponse(TypedDict, total=False):
    MessageBody: MessageBody


class DeleteJourneyRequest(ServiceRequest):
    ApplicationId: _string
    JourneyId: _string


class DeleteJourneyResponse(TypedDict, total=False):
    JourneyResponse: JourneyResponse


class DeletePushTemplateRequest(ServiceRequest):
    TemplateName: _string
    Version: _string | None


class DeletePushTemplateResponse(TypedDict, total=False):
    MessageBody: MessageBody


class DeleteRecommenderConfigurationRequest(ServiceRequest):
    RecommenderId: _string


class DeleteRecommenderConfigurationResponse(TypedDict, total=False):
    RecommenderConfigurationResponse: RecommenderConfigurationResponse


class DeleteSegmentRequest(ServiceRequest):
    ApplicationId: _string
    SegmentId: _string


class DeleteSegmentResponse(TypedDict, total=False):
    SegmentResponse: SegmentResponse


class DeleteSmsChannelRequest(ServiceRequest):
    ApplicationId: _string


class SMSChannelResponse(TypedDict, total=False):
    """Provides information about the status and settings of the SMS channel
    for an application.
    """

    ApplicationId: _string | None
    CreationDate: _string | None
    Enabled: _boolean | None
    HasCredential: _boolean | None
    Id: _string | None
    IsArchived: _boolean | None
    LastModifiedBy: _string | None
    LastModifiedDate: _string | None
    Platform: _string
    PromotionalMessagesPerSecond: _integer | None
    SenderId: _string | None
    ShortCode: _string | None
    TransactionalMessagesPerSecond: _integer | None
    Version: _integer | None


class DeleteSmsChannelResponse(TypedDict, total=False):
    SMSChannelResponse: SMSChannelResponse


class DeleteSmsTemplateRequest(ServiceRequest):
    TemplateName: _string
    Version: _string | None


class DeleteSmsTemplateResponse(TypedDict, total=False):
    MessageBody: MessageBody


class DeleteUserEndpointsRequest(ServiceRequest):
    ApplicationId: _string
    UserId: _string


ListOfEndpointResponse = list[EndpointResponse]


class EndpointsResponse(TypedDict, total=False):
    """Provides information about all the endpoints that are associated with a
    user ID.
    """

    Item: ListOfEndpointResponse


class DeleteUserEndpointsResponse(TypedDict, total=False):
    EndpointsResponse: EndpointsResponse


class DeleteVoiceChannelRequest(ServiceRequest):
    ApplicationId: _string


class VoiceChannelResponse(TypedDict, total=False):
    """Provides information about the status and settings of the voice channel
    for an application.
    """

    ApplicationId: _string | None
    CreationDate: _string | None
    Enabled: _boolean | None
    HasCredential: _boolean | None
    Id: _string | None
    IsArchived: _boolean | None
    LastModifiedBy: _string | None
    LastModifiedDate: _string | None
    Platform: _string
    Version: _integer | None


class DeleteVoiceChannelResponse(TypedDict, total=False):
    VoiceChannelResponse: VoiceChannelResponse


class DeleteVoiceTemplateRequest(ServiceRequest):
    TemplateName: _string
    Version: _string | None


class DeleteVoiceTemplateResponse(TypedDict, total=False):
    MessageBody: MessageBody


class VoiceMessage(TypedDict, total=False):
    """Specifies the settings for a one-time voice message that's sent directly
    to an endpoint through the voice channel.
    """

    Body: _string | None
    LanguageCode: _string | None
    OriginationNumber: _string | None
    Substitutions: MapOfListOf__string | None
    VoiceId: _string | None


class SMSMessage(TypedDict, total=False):
    """Specifies the default settings for a one-time SMS message that's sent
    directly to an endpoint.
    """

    Body: _string | None
    Keyword: _string | None
    MediaUrl: _string | None
    MessageType: MessageType | None
    OriginationNumber: _string | None
    SenderId: _string | None
    Substitutions: MapOfListOf__string | None
    EntityId: _string | None
    TemplateId: _string | None


class GCMMessage(TypedDict, total=False):
    """Specifies the settings for a one-time message that's sent directly to an
    endpoint through the GCM channel. The GCM channel enables Amazon
    Pinpoint to send messages to the Firebase Cloud Messaging (FCM),
    formerly Google Cloud Messaging (GCM), service.
    """

    Action: Action | None
    Body: _string | None
    CollapseKey: _string | None
    Data: MapOf__string | None
    IconReference: _string | None
    ImageIconUrl: _string | None
    ImageUrl: _string | None
    PreferredAuthenticationMethod: _string | None
    Priority: _string | None
    RawContent: _string | None
    RestrictedPackageName: _string | None
    SilentPush: _boolean | None
    SmallImageIconUrl: _string | None
    Sound: _string | None
    Substitutions: MapOfListOf__string | None
    TimeToLive: _integer | None
    Title: _string | None
    Url: _string | None


class SimpleEmailPart(TypedDict, total=False):
    """Specifies the subject or body of an email message, represented as
    textual email data and the applicable character set.
    """

    Charset: _string | None
    Data: _string | None


class SimpleEmail(TypedDict, total=False):
    """Specifies the contents of an email message, composed of a subject, a
    text part, and an HTML part.
    """

    HtmlPart: SimpleEmailPart | None
    Subject: SimpleEmailPart | None
    TextPart: SimpleEmailPart | None
    Headers: ListOfMessageHeader | None


_blob = bytes


class RawEmail(TypedDict, total=False):
    """Specifies the contents of an email message, represented as a raw MIME
    message.
    """

    Data: _blob | None


class EmailMessage(TypedDict, total=False):
    """Specifies the default settings and content for a one-time email message
    that's sent directly to an endpoint.
    """

    Body: _string | None
    FeedbackForwardingAddress: _string | None
    FromAddress: _string | None
    RawEmail: RawEmail | None
    ReplyToAddresses: ListOf__string | None
    SimpleEmail: SimpleEmail | None
    Substitutions: MapOfListOf__string | None


class DirectMessageConfiguration(TypedDict, total=False):
    """Specifies the settings and content for the default message and any
    default messages that you tailored for specific channels.
    """

    ADMMessage: ADMMessage | None
    APNSMessage: APNSMessage | None
    BaiduMessage: BaiduMessage | None
    DefaultMessage: DefaultMessage | None
    DefaultPushNotificationMessage: DefaultPushNotificationMessage | None
    EmailMessage: EmailMessage | None
    GCMMessage: GCMMessage | None
    SMSMessage: SMSMessage | None
    VoiceMessage: VoiceMessage | None


class EmailChannelRequest(TypedDict, total=False):
    """Specifies the status and settings of the email channel for an
    application.
    """

    ConfigurationSet: _string | None
    Enabled: _boolean | None
    FromAddress: _string
    Identity: _string
    RoleArn: _string | None
    OrchestrationSendingRoleArn: _string | None


class EmailTemplateResponse(TypedDict, total=False):
    """Provides information about the content and settings for a message
    template that can be used in messages that are sent through the email
    channel.
    """

    Arn: _string | None
    CreationDate: _string
    DefaultSubstitutions: _string | None
    HtmlPart: _string | None
    LastModifiedDate: _string
    RecommenderId: _string | None
    Subject: _string | None
    Headers: ListOfMessageHeader | None
    tags: MapOf__string | None
    TemplateDescription: _string | None
    TemplateName: _string
    TemplateType: TemplateType
    TextPart: _string | None
    Version: _string | None


class EndpointBatchItem(TypedDict, total=False):
    """Specifies an endpoint to create or update and the settings and
    attributes to set or change for the endpoint.
    """

    Address: _string | None
    Attributes: MapOfListOf__string | None
    ChannelType: ChannelType | None
    Demographic: EndpointDemographic | None
    EffectiveDate: _string | None
    EndpointStatus: _string | None
    Id: _string | None
    Location: EndpointLocation | None
    Metrics: MapOf__double | None
    OptOut: _string | None
    RequestId: _string | None
    User: EndpointUser | None


ListOfEndpointBatchItem = list[EndpointBatchItem]


class EndpointBatchRequest(TypedDict, total=False):
    """Specifies a batch of endpoints to create or update and the settings and
    attributes to set or change for each endpoint.
    """

    Item: ListOfEndpointBatchItem


class EndpointItemResponse(TypedDict, total=False):
    """Provides the status code and message that result from processing data
    for an endpoint.
    """

    Message: _string | None
    StatusCode: _integer | None


class EndpointMessageResult(TypedDict, total=False):
    """Provides information about the delivery status and results of sending a
    message directly to an endpoint.
    """

    Address: _string | None
    DeliveryStatus: DeliveryStatus
    MessageId: _string | None
    StatusCode: _integer
    StatusMessage: _string | None
    UpdatedToken: _string | None


class EndpointRequest(TypedDict, total=False):
    """Specifies the channel type and other settings for an endpoint."""

    Address: _string | None
    Attributes: MapOfListOf__string | None
    ChannelType: ChannelType | None
    Demographic: EndpointDemographic | None
    EffectiveDate: _string | None
    EndpointStatus: _string | None
    Location: EndpointLocation | None
    Metrics: MapOf__double | None
    OptOut: _string | None
    RequestId: _string | None
    User: EndpointUser | None


class EndpointSendConfiguration(TypedDict, total=False):
    """Specifies the content, including message variables and attributes, to
    use in a message that's sent directly to an endpoint.
    """

    BodyOverride: _string | None
    Context: MapOf__string | None
    RawContent: _string | None
    Substitutions: MapOfListOf__string | None
    TitleOverride: _string | None


class Session(TypedDict, total=False):
    """Provides information about a session."""

    Duration: _integer | None
    Id: _string
    StartTimestamp: _string
    StopTimestamp: _string | None


class Event(TypedDict, total=False):
    """Specifies information about an event that reports data to Amazon
    Pinpoint.
    """

    AppPackageName: _string | None
    AppTitle: _string | None
    AppVersionCode: _string | None
    Attributes: MapOf__string | None
    ClientSdkVersion: _string | None
    EventType: _string
    Metrics: MapOf__double | None
    SdkName: _string | None
    Session: Session | None
    Timestamp: _string


class EventItemResponse(TypedDict, total=False):
    """Provides the status code and message that result from processing an
    event.
    """

    Message: _string | None
    StatusCode: _integer | None


MapOfEvent = dict[_string, Event]


class PublicEndpoint(TypedDict, total=False):
    """Specifies the properties and attributes of an endpoint that's associated
    with an event.
    """

    Address: _string | None
    Attributes: MapOfListOf__string | None
    ChannelType: ChannelType | None
    Demographic: EndpointDemographic | None
    EffectiveDate: _string | None
    EndpointStatus: _string | None
    Location: EndpointLocation | None
    Metrics: MapOf__double | None
    OptOut: _string | None
    RequestId: _string | None
    User: EndpointUser | None


class EventsBatch(TypedDict, total=False):
    """Specifies a batch of endpoints and events to process."""

    Endpoint: PublicEndpoint
    Events: MapOfEvent


MapOfEventsBatch = dict[_string, EventsBatch]


class EventsRequest(TypedDict, total=False):
    """Specifies a batch of events to process."""

    BatchItem: MapOfEventsBatch


MapOfEventItemResponse = dict[_string, EventItemResponse]


class ItemResponse(TypedDict, total=False):
    """Provides information about the results of a request to create or update
    an endpoint that's associated with an event.
    """

    EndpointItemResponse: EndpointItemResponse | None
    EventsItemResponse: MapOfEventItemResponse | None


MapOfItemResponse = dict[_string, ItemResponse]


class EventsResponse(TypedDict, total=False):
    """Provides information about endpoints and the events that they're
    associated with.
    """

    Results: MapOfItemResponse | None


ListOfExportJobResponse = list[ExportJobResponse]


class ExportJobsResponse(TypedDict, total=False):
    """Provides information about all the export jobs that are associated with
    an application or segment. An export job is a job that exports endpoint
    definitions to a file.
    """

    Item: ListOfExportJobResponse
    NextToken: _string | None


class GCMChannelRequest(TypedDict, total=False):
    """Specifies the status and settings of the GCM channel for an application.
    This channel enables Amazon Pinpoint to send push notifications through
    the Firebase Cloud Messaging (FCM), formerly Google Cloud Messaging
    (GCM), service.
    """

    ApiKey: _string | None
    DefaultAuthenticationMethod: _string | None
    Enabled: _boolean | None
    ServiceJson: _string | None


class GetAdmChannelRequest(ServiceRequest):
    ApplicationId: _string


class GetAdmChannelResponse(TypedDict, total=False):
    ADMChannelResponse: ADMChannelResponse


class GetApnsChannelRequest(ServiceRequest):
    ApplicationId: _string


class GetApnsChannelResponse(TypedDict, total=False):
    APNSChannelResponse: APNSChannelResponse


class GetApnsSandboxChannelRequest(ServiceRequest):
    ApplicationId: _string


class GetApnsSandboxChannelResponse(TypedDict, total=False):
    APNSSandboxChannelResponse: APNSSandboxChannelResponse


class GetApnsVoipChannelRequest(ServiceRequest):
    ApplicationId: _string


class GetApnsVoipChannelResponse(TypedDict, total=False):
    APNSVoipChannelResponse: APNSVoipChannelResponse


class GetApnsVoipSandboxChannelRequest(ServiceRequest):
    ApplicationId: _string


class GetApnsVoipSandboxChannelResponse(TypedDict, total=False):
    APNSVoipSandboxChannelResponse: APNSVoipSandboxChannelResponse


class GetAppRequest(ServiceRequest):
    ApplicationId: _string


class GetAppResponse(TypedDict, total=False):
    ApplicationResponse: ApplicationResponse


class GetApplicationDateRangeKpiRequest(ServiceRequest):
    ApplicationId: _string
    EndTime: _timestampIso8601 | None
    KpiName: _string
    NextToken: _string | None
    PageSize: _string | None
    StartTime: _timestampIso8601 | None


class GetApplicationDateRangeKpiResponse(TypedDict, total=False):
    ApplicationDateRangeKpiResponse: ApplicationDateRangeKpiResponse


class GetApplicationSettingsRequest(ServiceRequest):
    ApplicationId: _string


class GetApplicationSettingsResponse(TypedDict, total=False):
    ApplicationSettingsResource: ApplicationSettingsResource


class GetAppsRequest(ServiceRequest):
    PageSize: _string | None
    Token: _string | None


class GetAppsResponse(TypedDict, total=False):
    ApplicationsResponse: ApplicationsResponse


class GetBaiduChannelRequest(ServiceRequest):
    ApplicationId: _string


class GetBaiduChannelResponse(TypedDict, total=False):
    BaiduChannelResponse: BaiduChannelResponse


class GetCampaignActivitiesRequest(ServiceRequest):
    ApplicationId: _string
    CampaignId: _string
    PageSize: _string | None
    Token: _string | None


class GetCampaignActivitiesResponse(TypedDict, total=False):
    ActivitiesResponse: ActivitiesResponse


class GetCampaignDateRangeKpiRequest(ServiceRequest):
    ApplicationId: _string
    CampaignId: _string
    EndTime: _timestampIso8601 | None
    KpiName: _string
    NextToken: _string | None
    PageSize: _string | None
    StartTime: _timestampIso8601 | None


class GetCampaignDateRangeKpiResponse(TypedDict, total=False):
    CampaignDateRangeKpiResponse: CampaignDateRangeKpiResponse


class GetCampaignRequest(ServiceRequest):
    ApplicationId: _string
    CampaignId: _string


class GetCampaignResponse(TypedDict, total=False):
    CampaignResponse: CampaignResponse


class GetCampaignVersionRequest(ServiceRequest):
    ApplicationId: _string
    CampaignId: _string
    Version: _string


class GetCampaignVersionResponse(TypedDict, total=False):
    CampaignResponse: CampaignResponse


class GetCampaignVersionsRequest(ServiceRequest):
    ApplicationId: _string
    CampaignId: _string
    PageSize: _string | None
    Token: _string | None


class GetCampaignVersionsResponse(TypedDict, total=False):
    CampaignsResponse: CampaignsResponse


class GetCampaignsRequest(ServiceRequest):
    ApplicationId: _string
    PageSize: _string | None
    Token: _string | None


class GetCampaignsResponse(TypedDict, total=False):
    CampaignsResponse: CampaignsResponse


class GetChannelsRequest(ServiceRequest):
    ApplicationId: _string


class GetChannelsResponse(TypedDict, total=False):
    ChannelsResponse: ChannelsResponse


class GetEmailChannelRequest(ServiceRequest):
    ApplicationId: _string


class GetEmailChannelResponse(TypedDict, total=False):
    EmailChannelResponse: EmailChannelResponse


class GetEmailTemplateRequest(ServiceRequest):
    TemplateName: _string
    Version: _string | None


class GetEmailTemplateResponse(TypedDict, total=False):
    EmailTemplateResponse: EmailTemplateResponse


class GetEndpointRequest(ServiceRequest):
    ApplicationId: _string
    EndpointId: _string


class GetEndpointResponse(TypedDict, total=False):
    EndpointResponse: EndpointResponse


class GetEventStreamRequest(ServiceRequest):
    ApplicationId: _string


class GetEventStreamResponse(TypedDict, total=False):
    EventStream: EventStream


class GetExportJobRequest(ServiceRequest):
    ApplicationId: _string
    JobId: _string


class GetExportJobResponse(TypedDict, total=False):
    ExportJobResponse: ExportJobResponse


class GetExportJobsRequest(ServiceRequest):
    ApplicationId: _string
    PageSize: _string | None
    Token: _string | None


class GetExportJobsResponse(TypedDict, total=False):
    ExportJobsResponse: ExportJobsResponse


class GetGcmChannelRequest(ServiceRequest):
    ApplicationId: _string


class GetGcmChannelResponse(TypedDict, total=False):
    GCMChannelResponse: GCMChannelResponse


class GetImportJobRequest(ServiceRequest):
    ApplicationId: _string
    JobId: _string


class GetImportJobResponse(TypedDict, total=False):
    ImportJobResponse: ImportJobResponse


class GetImportJobsRequest(ServiceRequest):
    ApplicationId: _string
    PageSize: _string | None
    Token: _string | None


ListOfImportJobResponse = list[ImportJobResponse]


class ImportJobsResponse(TypedDict, total=False):
    """Provides information about the status and settings of all the import
    jobs that are associated with an application or segment. An import job
    is a job that imports endpoint definitions from one or more files.
    """

    Item: ListOfImportJobResponse
    NextToken: _string | None


class GetImportJobsResponse(TypedDict, total=False):
    ImportJobsResponse: ImportJobsResponse


class GetInAppMessagesRequest(ServiceRequest):
    ApplicationId: _string
    EndpointId: _string


class InAppCampaignSchedule(TypedDict, total=False):
    """Schedule of the campaign."""

    EndDate: _string | None
    EventFilter: CampaignEventFilter | None
    QuietTime: QuietTime | None


class InAppMessage(TypedDict, total=False):
    """Provides all fields required for building an in-app message."""

    Content: ListOfInAppMessageContent | None
    CustomConfig: MapOf__string | None
    Layout: Layout | None


class InAppMessageCampaign(TypedDict, total=False):
    """Targeted in-app message campaign."""

    CampaignId: _string | None
    DailyCap: _integer | None
    InAppMessage: InAppMessage | None
    Priority: _integer | None
    Schedule: InAppCampaignSchedule | None
    SessionCap: _integer | None
    TotalCap: _integer | None
    TreatmentId: _string | None


ListOfInAppMessageCampaign = list[InAppMessageCampaign]


class InAppMessagesResponse(TypedDict, total=False):
    """Get in-app messages response object."""

    InAppMessageCampaigns: ListOfInAppMessageCampaign | None


class GetInAppMessagesResponse(TypedDict, total=False):
    InAppMessagesResponse: InAppMessagesResponse


class GetInAppTemplateRequest(ServiceRequest):
    TemplateName: _string
    Version: _string | None


class InAppTemplateResponse(TypedDict, total=False):
    """In-App Template Response."""

    Arn: _string | None
    Content: ListOfInAppMessageContent | None
    CreationDate: _string
    CustomConfig: MapOf__string | None
    LastModifiedDate: _string
    Layout: Layout | None
    tags: MapOf__string | None
    TemplateDescription: _string | None
    TemplateName: _string
    TemplateType: TemplateType
    Version: _string | None


class GetInAppTemplateResponse(TypedDict, total=False):
    InAppTemplateResponse: InAppTemplateResponse


class GetJourneyDateRangeKpiRequest(ServiceRequest):
    ApplicationId: _string
    EndTime: _timestampIso8601 | None
    JourneyId: _string
    KpiName: _string
    NextToken: _string | None
    PageSize: _string | None
    StartTime: _timestampIso8601 | None


class JourneyDateRangeKpiResponse(TypedDict, total=False):
    """Provides the results of a query that retrieved the data for a standard
    engagement metric that applies to a journey, and provides information
    about that query.
    """

    ApplicationId: _string
    EndTime: _timestampIso8601
    JourneyId: _string
    KpiName: _string
    KpiResult: BaseKpiResult
    NextToken: _string | None
    StartTime: _timestampIso8601


class GetJourneyDateRangeKpiResponse(TypedDict, total=False):
    JourneyDateRangeKpiResponse: JourneyDateRangeKpiResponse


class GetJourneyExecutionActivityMetricsRequest(ServiceRequest):
    ApplicationId: _string
    JourneyActivityId: _string
    JourneyId: _string
    NextToken: _string | None
    PageSize: _string | None


class JourneyExecutionActivityMetricsResponse(TypedDict, total=False):
    """Provides the results of a query that retrieved the data for a standard
    execution metric that applies to a journey activity, and provides
    information about that query.
    """

    ActivityType: _string
    ApplicationId: _string
    JourneyActivityId: _string
    JourneyId: _string
    LastEvaluatedTime: _string
    Metrics: MapOf__string


class GetJourneyExecutionActivityMetricsResponse(TypedDict, total=False):
    JourneyExecutionActivityMetricsResponse: JourneyExecutionActivityMetricsResponse


class GetJourneyExecutionMetricsRequest(ServiceRequest):
    ApplicationId: _string
    JourneyId: _string
    NextToken: _string | None
    PageSize: _string | None


class JourneyExecutionMetricsResponse(TypedDict, total=False):
    """Provides the results of a query that retrieved the data for a standard
    execution metric that applies to a journey, and provides information
    about that query.
    """

    ApplicationId: _string
    JourneyId: _string
    LastEvaluatedTime: _string
    Metrics: MapOf__string


class GetJourneyExecutionMetricsResponse(TypedDict, total=False):
    JourneyExecutionMetricsResponse: JourneyExecutionMetricsResponse


class GetJourneyRequest(ServiceRequest):
    ApplicationId: _string
    JourneyId: _string


class GetJourneyResponse(TypedDict, total=False):
    JourneyResponse: JourneyResponse


class GetJourneyRunExecutionActivityMetricsRequest(ServiceRequest):
    ApplicationId: _string
    JourneyActivityId: _string
    JourneyId: _string
    NextToken: _string | None
    PageSize: _string | None
    RunId: _string


class JourneyRunExecutionActivityMetricsResponse(TypedDict, total=False):
    """Provides the results of a query that retrieved the data for a standard
    execution metric that applies to a journey activity for a particular
    journey run, and provides information about that query.
    """

    ActivityType: _string
    ApplicationId: _string
    JourneyActivityId: _string
    JourneyId: _string
    LastEvaluatedTime: _string
    Metrics: MapOf__string
    RunId: _string


class GetJourneyRunExecutionActivityMetricsResponse(TypedDict, total=False):
    JourneyRunExecutionActivityMetricsResponse: JourneyRunExecutionActivityMetricsResponse


class GetJourneyRunExecutionMetricsRequest(ServiceRequest):
    ApplicationId: _string
    JourneyId: _string
    NextToken: _string | None
    PageSize: _string | None
    RunId: _string


class JourneyRunExecutionMetricsResponse(TypedDict, total=False):
    """Provides the results of a query that retrieved the data for a standard
    execution metric that applies to a journey run, and provides information
    about that query.
    """

    ApplicationId: _string
    JourneyId: _string
    LastEvaluatedTime: _string
    Metrics: MapOf__string
    RunId: _string


class GetJourneyRunExecutionMetricsResponse(TypedDict, total=False):
    JourneyRunExecutionMetricsResponse: JourneyRunExecutionMetricsResponse


class GetJourneyRunsRequest(ServiceRequest):
    ApplicationId: _string
    JourneyId: _string
    PageSize: _string | None
    Token: _string | None


class JourneyRunResponse(TypedDict, total=False):
    """Provides information from a specified run of a journey."""

    CreationTime: _string
    LastUpdateTime: _string
    RunId: _string
    Status: JourneyRunStatus


ListOfJourneyRunResponse = list[JourneyRunResponse]


class JourneyRunsResponse(TypedDict, total=False):
    """Provides information from all runs of a journey."""

    Item: ListOfJourneyRunResponse
    NextToken: _string | None


class GetJourneyRunsResponse(TypedDict, total=False):
    JourneyRunsResponse: JourneyRunsResponse


class GetPushTemplateRequest(ServiceRequest):
    TemplateName: _string
    Version: _string | None


class PushNotificationTemplateResponse(TypedDict, total=False):
    """Provides information about the content and settings for a message
    template that can be used in messages that are sent through a push
    notification channel.
    """

    ADM: AndroidPushNotificationTemplate | None
    APNS: APNSPushNotificationTemplate | None
    Arn: _string | None
    Baidu: AndroidPushNotificationTemplate | None
    CreationDate: _string
    Default: DefaultPushNotificationTemplate | None
    DefaultSubstitutions: _string | None
    GCM: AndroidPushNotificationTemplate | None
    LastModifiedDate: _string
    RecommenderId: _string | None
    tags: MapOf__string | None
    TemplateDescription: _string | None
    TemplateName: _string
    TemplateType: TemplateType
    Version: _string | None


class GetPushTemplateResponse(TypedDict, total=False):
    PushNotificationTemplateResponse: PushNotificationTemplateResponse


class GetRecommenderConfigurationRequest(ServiceRequest):
    RecommenderId: _string


class GetRecommenderConfigurationResponse(TypedDict, total=False):
    RecommenderConfigurationResponse: RecommenderConfigurationResponse


class GetRecommenderConfigurationsRequest(ServiceRequest):
    PageSize: _string | None
    Token: _string | None


ListOfRecommenderConfigurationResponse = list[RecommenderConfigurationResponse]


class ListRecommenderConfigurationsResponse(TypedDict, total=False):
    """Provides information about all the recommender model configurations that
    are associated with your Amazon Pinpoint account.
    """

    Item: ListOfRecommenderConfigurationResponse
    NextToken: _string | None


class GetRecommenderConfigurationsResponse(TypedDict, total=False):
    ListRecommenderConfigurationsResponse: ListRecommenderConfigurationsResponse


class GetSegmentExportJobsRequest(ServiceRequest):
    ApplicationId: _string
    PageSize: _string | None
    SegmentId: _string
    Token: _string | None


class GetSegmentExportJobsResponse(TypedDict, total=False):
    ExportJobsResponse: ExportJobsResponse


class GetSegmentImportJobsRequest(ServiceRequest):
    ApplicationId: _string
    PageSize: _string | None
    SegmentId: _string
    Token: _string | None


class GetSegmentImportJobsResponse(TypedDict, total=False):
    ImportJobsResponse: ImportJobsResponse


class GetSegmentRequest(ServiceRequest):
    ApplicationId: _string
    SegmentId: _string


class GetSegmentResponse(TypedDict, total=False):
    SegmentResponse: SegmentResponse


class GetSegmentVersionRequest(ServiceRequest):
    ApplicationId: _string
    SegmentId: _string
    Version: _string


class GetSegmentVersionResponse(TypedDict, total=False):
    SegmentResponse: SegmentResponse


class GetSegmentVersionsRequest(ServiceRequest):
    ApplicationId: _string
    PageSize: _string | None
    SegmentId: _string
    Token: _string | None


ListOfSegmentResponse = list[SegmentResponse]


class SegmentsResponse(TypedDict, total=False):
    """Provides information about all the segments that are associated with an
    application.
    """

    Item: ListOfSegmentResponse
    NextToken: _string | None


class GetSegmentVersionsResponse(TypedDict, total=False):
    SegmentsResponse: SegmentsResponse


class GetSegmentsRequest(ServiceRequest):
    ApplicationId: _string
    PageSize: _string | None
    Token: _string | None


class GetSegmentsResponse(TypedDict, total=False):
    SegmentsResponse: SegmentsResponse


class GetSmsChannelRequest(ServiceRequest):
    ApplicationId: _string


class GetSmsChannelResponse(TypedDict, total=False):
    SMSChannelResponse: SMSChannelResponse


class GetSmsTemplateRequest(ServiceRequest):
    TemplateName: _string
    Version: _string | None


class SMSTemplateResponse(TypedDict, total=False):
    """Provides information about the content and settings for a message
    template that can be used in text messages that are sent through the SMS
    channel.
    """

    Arn: _string | None
    Body: _string | None
    CreationDate: _string
    DefaultSubstitutions: _string | None
    LastModifiedDate: _string
    RecommenderId: _string | None
    tags: MapOf__string | None
    TemplateDescription: _string | None
    TemplateName: _string
    TemplateType: TemplateType
    Version: _string | None


class GetSmsTemplateResponse(TypedDict, total=False):
    SMSTemplateResponse: SMSTemplateResponse


class GetUserEndpointsRequest(ServiceRequest):
    ApplicationId: _string
    UserId: _string


class GetUserEndpointsResponse(TypedDict, total=False):
    EndpointsResponse: EndpointsResponse


class GetVoiceChannelRequest(ServiceRequest):
    ApplicationId: _string


class GetVoiceChannelResponse(TypedDict, total=False):
    VoiceChannelResponse: VoiceChannelResponse


class GetVoiceTemplateRequest(ServiceRequest):
    TemplateName: _string
    Version: _string | None


class VoiceTemplateResponse(TypedDict, total=False):
    """Provides information about the content and settings for a message
    template that can be used in messages that are sent through the voice
    channel.
    """

    Arn: _string | None
    Body: _string | None
    CreationDate: _string
    DefaultSubstitutions: _string | None
    LanguageCode: _string | None
    LastModifiedDate: _string
    tags: MapOf__string | None
    TemplateDescription: _string | None
    TemplateName: _string
    TemplateType: TemplateType
    Version: _string | None
    VoiceId: _string | None


class GetVoiceTemplateResponse(TypedDict, total=False):
    VoiceTemplateResponse: VoiceTemplateResponse


class JourneyStateRequest(TypedDict, total=False):
    """Changes the status of a journey."""

    State: State | None


ListOfJourneyResponse = list[JourneyResponse]


class JourneysResponse(TypedDict, total=False):
    """Provides information about the status, configuration, and other settings
    for all the journeys that are associated with an application.
    """

    Item: ListOfJourneyResponse
    NextToken: _string | None


class ListJourneysRequest(ServiceRequest):
    ApplicationId: _string
    PageSize: _string | None
    Token: _string | None


class ListJourneysResponse(TypedDict, total=False):
    JourneysResponse: JourneysResponse


class ListTagsForResourceRequest(ServiceRequest):
    ResourceArn: _string


class TagsModel(TypedDict, total=False):
    """Specifies the tags (keys and values) for an application, campaign,
    message template, or segment.
    """

    tags: MapOf__string


class ListTagsForResourceResponse(TypedDict, total=False):
    TagsModel: TagsModel


class ListTemplateVersionsRequest(ServiceRequest):
    NextToken: _string | None
    PageSize: _string | None
    TemplateName: _string
    TemplateType: _string


class TemplateVersionResponse(TypedDict, total=False):
    """Provides information about a specific version of a message template."""

    CreationDate: _string
    DefaultSubstitutions: _string | None
    LastModifiedDate: _string
    TemplateDescription: _string | None
    TemplateName: _string
    TemplateType: _string
    Version: _string | None


ListOfTemplateVersionResponse = list[TemplateVersionResponse]


class TemplateVersionsResponse(TypedDict, total=False):
    """Provides information about all the versions of a specific message
    template.
    """

    Item: ListOfTemplateVersionResponse
    Message: _string | None
    NextToken: _string | None
    RequestID: _string | None


class ListTemplateVersionsResponse(TypedDict, total=False):
    TemplateVersionsResponse: TemplateVersionsResponse


class ListTemplatesRequest(ServiceRequest):
    NextToken: _string | None
    PageSize: _string | None
    Prefix: _string | None
    TemplateType: _string | None


class TemplateResponse(TypedDict, total=False):
    """Provides information about a message template that's associated with
    your Amazon Pinpoint account.
    """

    Arn: _string | None
    CreationDate: _string
    DefaultSubstitutions: _string | None
    LastModifiedDate: _string
    tags: MapOf__string | None
    TemplateDescription: _string | None
    TemplateName: _string
    TemplateType: TemplateType
    Version: _string | None


ListOfTemplateResponse = list[TemplateResponse]


class TemplatesResponse(TypedDict, total=False):
    """Provides information about all the message templates that are associated
    with your Amazon Pinpoint account.
    """

    Item: ListOfTemplateResponse
    NextToken: _string | None


class ListTemplatesResponse(TypedDict, total=False):
    TemplatesResponse: TemplatesResponse


MapOfEndpointSendConfiguration = dict[_string, EndpointSendConfiguration]
MapOfAddressConfiguration = dict[_string, AddressConfiguration]


class MessageRequest(TypedDict, total=False):
    """Specifies the configuration and other settings for a message."""

    Addresses: MapOfAddressConfiguration | None
    Context: MapOf__string | None
    Endpoints: MapOfEndpointSendConfiguration | None
    MessageConfiguration: DirectMessageConfiguration
    TemplateConfiguration: TemplateConfiguration | None
    TraceId: _string | None


class MessageResult(TypedDict, total=False):
    """Provides information about the results of sending a message directly to
    an endpoint address.
    """

    DeliveryStatus: DeliveryStatus
    MessageId: _string | None
    StatusCode: _integer
    StatusMessage: _string | None
    UpdatedToken: _string | None


MapOfMessageResult = dict[_string, MessageResult]
MapOfEndpointMessageResult = dict[_string, EndpointMessageResult]


class MessageResponse(TypedDict, total=False):
    """Provides information about the results of a request to send a message to
    an endpoint address.
    """

    ApplicationId: _string
    EndpointResult: MapOfEndpointMessageResult | None
    RequestId: _string | None
    Result: MapOfMessageResult | None


class NumberValidateRequest(TypedDict, total=False):
    """Specifies a phone number to validate and retrieve information about."""

    IsoCountryCode: _string | None
    PhoneNumber: _string | None


class NumberValidateResponse(TypedDict, total=False):
    """Provides information about a phone number."""

    Carrier: _string | None
    City: _string | None
    CleansedPhoneNumberE164: _string | None
    CleansedPhoneNumberNational: _string | None
    Country: _string | None
    CountryCodeIso2: _string | None
    CountryCodeNumeric: _string | None
    County: _string | None
    OriginalCountryCodeIso2: _string | None
    OriginalPhoneNumber: _string | None
    PhoneType: _string | None
    PhoneTypeCode: _integer | None
    Timezone: _string | None
    ZipCode: _string | None


class PhoneNumberValidateRequest(ServiceRequest):
    NumberValidateRequest: NumberValidateRequest


class PhoneNumberValidateResponse(TypedDict, total=False):
    NumberValidateResponse: NumberValidateResponse


class WriteEventStream(TypedDict, total=False):
    """Specifies the Amazon Resource Name (ARN) of an event stream to publish
    events to and the AWS Identity and Access Management (IAM) role to use
    when publishing those events.
    """

    DestinationStreamArn: _string
    RoleArn: _string


class PutEventStreamRequest(ServiceRequest):
    ApplicationId: _string
    WriteEventStream: WriteEventStream


class PutEventStreamResponse(TypedDict, total=False):
    EventStream: EventStream


class PutEventsRequest(ServiceRequest):
    ApplicationId: _string
    EventsRequest: EventsRequest


class PutEventsResponse(TypedDict, total=False):
    EventsResponse: EventsResponse


class UpdateAttributesRequest(TypedDict, total=False):
    """Specifies one or more attributes to remove from all the endpoints that
    are associated with an application.
    """

    Blacklist: ListOf__string | None


class RemoveAttributesRequest(ServiceRequest):
    ApplicationId: _string
    AttributeType: _string
    UpdateAttributesRequest: UpdateAttributesRequest


class RemoveAttributesResponse(TypedDict, total=False):
    AttributesResource: AttributesResource


class SMSChannelRequest(TypedDict, total=False):
    """Specifies the status and settings of the SMS channel for an application."""

    Enabled: _boolean | None
    SenderId: _string | None
    ShortCode: _string | None


class SendMessagesRequest(ServiceRequest):
    ApplicationId: _string
    MessageRequest: MessageRequest


class SendMessagesResponse(TypedDict, total=False):
    MessageResponse: MessageResponse


class SendOTPMessageRequestParameters(TypedDict, total=False):
    """Send OTP message request parameters."""

    AllowedAttempts: _integer | None
    BrandName: _string
    Channel: _string
    CodeLength: _integer | None
    DestinationIdentity: _string
    EntityId: _string | None
    Language: _string | None
    OriginationIdentity: _string
    ReferenceId: _string
    TemplateId: _string | None
    ValidityPeriod: _integer | None


class SendOTPMessageRequest(ServiceRequest):
    ApplicationId: _string
    SendOTPMessageRequestParameters: SendOTPMessageRequestParameters


class SendOTPMessageResponse(TypedDict, total=False):
    MessageResponse: MessageResponse


class SendUsersMessageRequest(TypedDict, total=False):
    """Specifies the configuration and other settings for a message to send to
    all the endpoints that are associated with a list of users.
    """

    Context: MapOf__string | None
    MessageConfiguration: DirectMessageConfiguration
    TemplateConfiguration: TemplateConfiguration | None
    TraceId: _string | None
    Users: MapOfEndpointSendConfiguration


MapOfMapOfEndpointMessageResult = dict[_string, MapOfEndpointMessageResult]


class SendUsersMessageResponse(TypedDict, total=False):
    """Provides information about which users and endpoints a message was sent
    to.
    """

    ApplicationId: _string
    RequestId: _string | None
    Result: MapOfMapOfEndpointMessageResult | None


class SendUsersMessagesRequest(ServiceRequest):
    ApplicationId: _string
    SendUsersMessageRequest: SendUsersMessageRequest


class SendUsersMessagesResponse(TypedDict, total=False):
    SendUsersMessageResponse: SendUsersMessageResponse


class TagResourceRequest(ServiceRequest):
    ResourceArn: _string
    TagsModel: TagsModel


class TemplateActiveVersionRequest(TypedDict, total=False):
    """Specifies which version of a message template to use as the active
    version of the template.
    """

    Version: _string | None


class UntagResourceRequest(ServiceRequest):
    ResourceArn: _string
    TagKeys: ListOf__string


class UpdateAdmChannelRequest(ServiceRequest):
    ADMChannelRequest: ADMChannelRequest
    ApplicationId: _string


class UpdateAdmChannelResponse(TypedDict, total=False):
    ADMChannelResponse: ADMChannelResponse


class UpdateApnsChannelRequest(ServiceRequest):
    APNSChannelRequest: APNSChannelRequest
    ApplicationId: _string


class UpdateApnsChannelResponse(TypedDict, total=False):
    APNSChannelResponse: APNSChannelResponse


class UpdateApnsSandboxChannelRequest(ServiceRequest):
    APNSSandboxChannelRequest: APNSSandboxChannelRequest
    ApplicationId: _string


class UpdateApnsSandboxChannelResponse(TypedDict, total=False):
    APNSSandboxChannelResponse: APNSSandboxChannelResponse


class UpdateApnsVoipChannelRequest(ServiceRequest):
    APNSVoipChannelRequest: APNSVoipChannelRequest
    ApplicationId: _string


class UpdateApnsVoipChannelResponse(TypedDict, total=False):
    APNSVoipChannelResponse: APNSVoipChannelResponse


class UpdateApnsVoipSandboxChannelRequest(ServiceRequest):
    APNSVoipSandboxChannelRequest: APNSVoipSandboxChannelRequest
    ApplicationId: _string


class UpdateApnsVoipSandboxChannelResponse(TypedDict, total=False):
    APNSVoipSandboxChannelResponse: APNSVoipSandboxChannelResponse


class WriteApplicationSettingsRequest(TypedDict, total=False):
    """Specifies the default settings for an application."""

    CampaignHook: CampaignHook | None
    CloudWatchMetricsEnabled: _boolean | None
    EventTaggingEnabled: _boolean | None
    Limits: CampaignLimits | None
    QuietTime: QuietTime | None
    JourneyLimits: ApplicationSettingsJourneyLimits | None


class UpdateApplicationSettingsRequest(ServiceRequest):
    ApplicationId: _string
    WriteApplicationSettingsRequest: WriteApplicationSettingsRequest


class UpdateApplicationSettingsResponse(TypedDict, total=False):
    ApplicationSettingsResource: ApplicationSettingsResource


class UpdateBaiduChannelRequest(ServiceRequest):
    ApplicationId: _string
    BaiduChannelRequest: BaiduChannelRequest


class UpdateBaiduChannelResponse(TypedDict, total=False):
    BaiduChannelResponse: BaiduChannelResponse


class UpdateCampaignRequest(ServiceRequest):
    ApplicationId: _string
    CampaignId: _string
    WriteCampaignRequest: WriteCampaignRequest


class UpdateCampaignResponse(TypedDict, total=False):
    CampaignResponse: CampaignResponse


class UpdateEmailChannelRequest(ServiceRequest):
    ApplicationId: _string
    EmailChannelRequest: EmailChannelRequest


class UpdateEmailChannelResponse(TypedDict, total=False):
    EmailChannelResponse: EmailChannelResponse


class UpdateEmailTemplateRequest(ServiceRequest):
    CreateNewVersion: _boolean | None
    EmailTemplateRequest: EmailTemplateRequest
    TemplateName: _string
    Version: _string | None


class UpdateEmailTemplateResponse(TypedDict, total=False):
    MessageBody: MessageBody


class UpdateEndpointRequest(ServiceRequest):
    ApplicationId: _string
    EndpointId: _string
    EndpointRequest: EndpointRequest


class UpdateEndpointResponse(TypedDict, total=False):
    MessageBody: MessageBody


class UpdateEndpointsBatchRequest(ServiceRequest):
    ApplicationId: _string
    EndpointBatchRequest: EndpointBatchRequest


class UpdateEndpointsBatchResponse(TypedDict, total=False):
    MessageBody: MessageBody


class UpdateGcmChannelRequest(ServiceRequest):
    ApplicationId: _string
    GCMChannelRequest: GCMChannelRequest


class UpdateGcmChannelResponse(TypedDict, total=False):
    GCMChannelResponse: GCMChannelResponse


class UpdateInAppTemplateRequest(ServiceRequest):
    CreateNewVersion: _boolean | None
    InAppTemplateRequest: InAppTemplateRequest
    TemplateName: _string
    Version: _string | None


class UpdateInAppTemplateResponse(TypedDict, total=False):
    MessageBody: MessageBody


class UpdateJourneyRequest(ServiceRequest):
    ApplicationId: _string
    JourneyId: _string
    WriteJourneyRequest: WriteJourneyRequest


class UpdateJourneyResponse(TypedDict, total=False):
    JourneyResponse: JourneyResponse


class UpdateJourneyStateRequest(ServiceRequest):
    ApplicationId: _string
    JourneyId: _string
    JourneyStateRequest: JourneyStateRequest


class UpdateJourneyStateResponse(TypedDict, total=False):
    JourneyResponse: JourneyResponse


class UpdatePushTemplateRequest(ServiceRequest):
    CreateNewVersion: _boolean | None
    PushNotificationTemplateRequest: PushNotificationTemplateRequest
    TemplateName: _string
    Version: _string | None


class UpdatePushTemplateResponse(TypedDict, total=False):
    MessageBody: MessageBody


class UpdateRecommenderConfiguration(TypedDict, total=False):
    """Specifies Amazon Pinpoint configuration settings for retrieving and
    processing recommendation data from a recommender model.
    """

    Attributes: MapOf__string | None
    Description: _string | None
    Name: _string | None
    RecommendationProviderIdType: _string | None
    RecommendationProviderRoleArn: _string
    RecommendationProviderUri: _string
    RecommendationTransformerUri: _string | None
    RecommendationsDisplayName: _string | None
    RecommendationsPerMessage: _integer | None


class UpdateRecommenderConfigurationRequest(ServiceRequest):
    RecommenderId: _string
    UpdateRecommenderConfiguration: UpdateRecommenderConfiguration


class UpdateRecommenderConfigurationResponse(TypedDict, total=False):
    RecommenderConfigurationResponse: RecommenderConfigurationResponse


class UpdateSegmentRequest(ServiceRequest):
    ApplicationId: _string
    SegmentId: _string
    WriteSegmentRequest: WriteSegmentRequest


class UpdateSegmentResponse(TypedDict, total=False):
    SegmentResponse: SegmentResponse


class UpdateSmsChannelRequest(ServiceRequest):
    ApplicationId: _string
    SMSChannelRequest: SMSChannelRequest


class UpdateSmsChannelResponse(TypedDict, total=False):
    SMSChannelResponse: SMSChannelResponse


class UpdateSmsTemplateRequest(ServiceRequest):
    CreateNewVersion: _boolean | None
    SMSTemplateRequest: SMSTemplateRequest
    TemplateName: _string
    Version: _string | None


class UpdateSmsTemplateResponse(TypedDict, total=False):
    MessageBody: MessageBody


class UpdateTemplateActiveVersionRequest(ServiceRequest):
    TemplateActiveVersionRequest: TemplateActiveVersionRequest
    TemplateName: _string
    TemplateType: _string


class UpdateTemplateActiveVersionResponse(TypedDict, total=False):
    MessageBody: MessageBody


class VoiceChannelRequest(TypedDict, total=False):
    """Specifies the status and settings of the voice channel for an
    application.
    """

    Enabled: _boolean | None


class UpdateVoiceChannelRequest(ServiceRequest):
    ApplicationId: _string
    VoiceChannelRequest: VoiceChannelRequest


class UpdateVoiceChannelResponse(TypedDict, total=False):
    VoiceChannelResponse: VoiceChannelResponse


class UpdateVoiceTemplateRequest(ServiceRequest):
    CreateNewVersion: _boolean | None
    TemplateName: _string
    Version: _string | None
    VoiceTemplateRequest: VoiceTemplateRequest


class UpdateVoiceTemplateResponse(TypedDict, total=False):
    MessageBody: MessageBody


class VerificationResponse(TypedDict, total=False):
    """Verify OTP Message Response."""

    Valid: _boolean | None


class VerifyOTPMessageRequestParameters(TypedDict, total=False):
    """Verify OTP message request."""

    DestinationIdentity: _string
    Otp: _string
    ReferenceId: _string


class VerifyOTPMessageRequest(ServiceRequest):
    ApplicationId: _string
    VerifyOTPMessageRequestParameters: VerifyOTPMessageRequestParameters


class VerifyOTPMessageResponse(TypedDict, total=False):
    VerificationResponse: VerificationResponse


_long = int
_timestampUnix = datetime


class PinpointApi:
    service: str = "pinpoint"
    version: str = "2016-12-01"

    @handler("CreateApp")
    def create_app(
        self,
        context: RequestContext,
        create_application_request: CreateApplicationRequest,
        **kwargs,
    ) -> CreateAppResponse:
        """Creates an application.

        :param create_application_request: Specifies the display name of an application and the tags to associate
        with the application.
        :returns: CreateAppResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("CreateCampaign")
    def create_campaign(
        self,
        context: RequestContext,
        application_id: _string,
        write_campaign_request: WriteCampaignRequest,
        **kwargs,
    ) -> CreateCampaignResponse:
        """Creates a new campaign for an application or updates the settings of an
        existing campaign for an application.

        :param application_id: The unique identifier for the application.
        :param write_campaign_request: Specifies the configuration and other settings for a campaign.
        :returns: CreateCampaignResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("CreateEmailTemplate")
    def create_email_template(
        self,
        context: RequestContext,
        template_name: _string,
        email_template_request: EmailTemplateRequest,
        **kwargs,
    ) -> CreateEmailTemplateResponse:
        """Creates a message template for messages that are sent through the email
        channel.

        :param template_name: The name of the message template.
        :param email_template_request: Specifies the content and settings for a message template that can be
        used in messages that are sent through the email channel.
        :returns: CreateEmailTemplateResponse
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("CreateExportJob")
    def create_export_job(
        self,
        context: RequestContext,
        application_id: _string,
        export_job_request: ExportJobRequest,
        **kwargs,
    ) -> CreateExportJobResponse:
        """Creates an export job for an application.

        :param application_id: The unique identifier for the application.
        :param export_job_request: Specifies the settings for a job that exports endpoint definitions to an
        Amazon Simple Storage Service (Amazon S3) bucket.
        :returns: CreateExportJobResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("CreateImportJob")
    def create_import_job(
        self,
        context: RequestContext,
        application_id: _string,
        import_job_request: ImportJobRequest,
        **kwargs,
    ) -> CreateImportJobResponse:
        """Creates an import job for an application.

        :param application_id: The unique identifier for the application.
        :param import_job_request: Specifies the settings for a job that imports endpoint definitions from
        an Amazon Simple Storage Service (Amazon S3) bucket.
        :returns: CreateImportJobResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("CreateInAppTemplate")
    def create_in_app_template(
        self,
        context: RequestContext,
        template_name: _string,
        in_app_template_request: InAppTemplateRequest,
        **kwargs,
    ) -> CreateInAppTemplateResponse:
        """Creates a new message template for messages using the in-app message
        channel.

        :param template_name: The name of the message template.
        :param in_app_template_request: InApp Template Request.
        :returns: CreateInAppTemplateResponse
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("CreateJourney")
    def create_journey(
        self,
        context: RequestContext,
        application_id: _string,
        write_journey_request: WriteJourneyRequest,
        **kwargs,
    ) -> CreateJourneyResponse:
        """Creates a journey for an application.

        :param application_id: The unique identifier for the application.
        :param write_journey_request: Specifies the configuration and other settings for a journey.
        :returns: CreateJourneyResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("CreatePushTemplate")
    def create_push_template(
        self,
        context: RequestContext,
        template_name: _string,
        push_notification_template_request: PushNotificationTemplateRequest,
        **kwargs,
    ) -> CreatePushTemplateResponse:
        """Creates a message template for messages that are sent through a push
        notification channel.

        :param template_name: The name of the message template.
        :param push_notification_template_request: Specifies the content and settings for a message template that can be
        used in messages that are sent through a push notification channel.
        :returns: CreatePushTemplateResponse
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("CreateRecommenderConfiguration")
    def create_recommender_configuration(
        self,
        context: RequestContext,
        create_recommender_configuration: CreateRecommenderConfiguration,
        **kwargs,
    ) -> CreateRecommenderConfigurationResponse:
        """Creates an Amazon Pinpoint configuration for a recommender model.

        :param create_recommender_configuration: Specifies Amazon Pinpoint configuration settings for retrieving and
        processing recommendation data from a recommender model.
        :returns: CreateRecommenderConfigurationResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("CreateSegment")
    def create_segment(
        self,
        context: RequestContext,
        application_id: _string,
        write_segment_request: WriteSegmentRequest,
        **kwargs,
    ) -> CreateSegmentResponse:
        """Creates a new segment for an application or updates the configuration,
        dimension, and other settings for an existing segment that's associated
        with an application.

        :param application_id: The unique identifier for the application.
        :param write_segment_request: Specifies the configuration, dimension, and other settings for a
        segment.
        :returns: CreateSegmentResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("CreateSmsTemplate")
    def create_sms_template(
        self,
        context: RequestContext,
        template_name: _string,
        sms_template_request: SMSTemplateRequest,
        **kwargs,
    ) -> CreateSmsTemplateResponse:
        """Creates a message template for messages that are sent through the SMS
        channel.

        :param template_name: The name of the message template.
        :param sms_template_request: Specifies the content and settings for a message template that can be
        used in text messages that are sent through the SMS channel.
        :returns: CreateSmsTemplateResponse
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("CreateVoiceTemplate")
    def create_voice_template(
        self,
        context: RequestContext,
        template_name: _string,
        voice_template_request: VoiceTemplateRequest,
        **kwargs,
    ) -> CreateVoiceTemplateResponse:
        """Creates a message template for messages that are sent through the voice
        channel.

        :param template_name: The name of the message template.
        :param voice_template_request: Specifies the content and settings for a message template that can be
        used in messages that are sent through the voice channel.
        :returns: CreateVoiceTemplateResponse
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("DeleteAdmChannel")
    def delete_adm_channel(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> DeleteAdmChannelResponse:
        """Disables the ADM channel for an application and deletes any existing
        settings for the channel.

        :param application_id: The unique identifier for the application.
        :returns: DeleteAdmChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteApnsChannel")
    def delete_apns_channel(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> DeleteApnsChannelResponse:
        """Disables the APNs channel for an application and deletes any existing
        settings for the channel.

        :param application_id: The unique identifier for the application.
        :returns: DeleteApnsChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteApnsSandboxChannel")
    def delete_apns_sandbox_channel(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> DeleteApnsSandboxChannelResponse:
        """Disables the APNs sandbox channel for an application and deletes any
        existing settings for the channel.

        :param application_id: The unique identifier for the application.
        :returns: DeleteApnsSandboxChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteApnsVoipChannel")
    def delete_apns_voip_channel(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> DeleteApnsVoipChannelResponse:
        """Disables the APNs VoIP channel for an application and deletes any
        existing settings for the channel.

        :param application_id: The unique identifier for the application.
        :returns: DeleteApnsVoipChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteApnsVoipSandboxChannel")
    def delete_apns_voip_sandbox_channel(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> DeleteApnsVoipSandboxChannelResponse:
        """Disables the APNs VoIP sandbox channel for an application and deletes
        any existing settings for the channel.

        :param application_id: The unique identifier for the application.
        :returns: DeleteApnsVoipSandboxChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteApp")
    def delete_app(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> DeleteAppResponse:
        """Deletes an application.

        :param application_id: The unique identifier for the application.
        :returns: DeleteAppResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteBaiduChannel")
    def delete_baidu_channel(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> DeleteBaiduChannelResponse:
        """Disables the Baidu channel for an application and deletes any existing
        settings for the channel.

        :param application_id: The unique identifier for the application.
        :returns: DeleteBaiduChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteCampaign")
    def delete_campaign(
        self, context: RequestContext, campaign_id: _string, application_id: _string, **kwargs
    ) -> DeleteCampaignResponse:
        """Deletes a campaign from an application.

        :param campaign_id: The unique identifier for the campaign.
        :param application_id: The unique identifier for the application.
        :returns: DeleteCampaignResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteEmailChannel")
    def delete_email_channel(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> DeleteEmailChannelResponse:
        """Disables the email channel for an application and deletes any existing
        settings for the channel.

        :param application_id: The unique identifier for the application.
        :returns: DeleteEmailChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteEmailTemplate")
    def delete_email_template(
        self,
        context: RequestContext,
        template_name: _string,
        version: _string | None = None,
        **kwargs,
    ) -> DeleteEmailTemplateResponse:
        """Deletes a message template for messages that were sent through the email
        channel.

        :param template_name: The name of the message template.
        :param version: The unique identifier for the version of the message template to update,
        retrieve information about, or delete.
        :returns: DeleteEmailTemplateResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteEndpoint")
    def delete_endpoint(
        self, context: RequestContext, application_id: _string, endpoint_id: _string, **kwargs
    ) -> DeleteEndpointResponse:
        """Deletes an endpoint from an application.

        :param application_id: The unique identifier for the application.
        :param endpoint_id: The case insensitive unique identifier for the endpoint.
        :returns: DeleteEndpointResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteEventStream")
    def delete_event_stream(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> DeleteEventStreamResponse:
        """Deletes the event stream for an application.

        :param application_id: The unique identifier for the application.
        :returns: DeleteEventStreamResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteGcmChannel")
    def delete_gcm_channel(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> DeleteGcmChannelResponse:
        """Disables the GCM channel for an application and deletes any existing
        settings for the channel.

        :param application_id: The unique identifier for the application.
        :returns: DeleteGcmChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteInAppTemplate")
    def delete_in_app_template(
        self,
        context: RequestContext,
        template_name: _string,
        version: _string | None = None,
        **kwargs,
    ) -> DeleteInAppTemplateResponse:
        """Deletes a message template for messages sent using the in-app message
        channel.

        :param template_name: The name of the message template.
        :param version: The unique identifier for the version of the message template to update,
        retrieve information about, or delete.
        :returns: DeleteInAppTemplateResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteJourney")
    def delete_journey(
        self, context: RequestContext, journey_id: _string, application_id: _string, **kwargs
    ) -> DeleteJourneyResponse:
        """Deletes a journey from an application.

        :param journey_id: The unique identifier for the journey.
        :param application_id: The unique identifier for the application.
        :returns: DeleteJourneyResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeletePushTemplate")
    def delete_push_template(
        self,
        context: RequestContext,
        template_name: _string,
        version: _string | None = None,
        **kwargs,
    ) -> DeletePushTemplateResponse:
        """Deletes a message template for messages that were sent through a push
        notification channel.

        :param template_name: The name of the message template.
        :param version: The unique identifier for the version of the message template to update,
        retrieve information about, or delete.
        :returns: DeletePushTemplateResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteRecommenderConfiguration")
    def delete_recommender_configuration(
        self, context: RequestContext, recommender_id: _string, **kwargs
    ) -> DeleteRecommenderConfigurationResponse:
        """Deletes an Amazon Pinpoint configuration for a recommender model.

        :param recommender_id: The unique identifier for the recommender model configuration.
        :returns: DeleteRecommenderConfigurationResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteSegment")
    def delete_segment(
        self, context: RequestContext, segment_id: _string, application_id: _string, **kwargs
    ) -> DeleteSegmentResponse:
        """Deletes a segment from an application.

        :param segment_id: The unique identifier for the segment.
        :param application_id: The unique identifier for the application.
        :returns: DeleteSegmentResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteSmsChannel")
    def delete_sms_channel(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> DeleteSmsChannelResponse:
        """Disables the SMS channel for an application and deletes any existing
        settings for the channel.

        :param application_id: The unique identifier for the application.
        :returns: DeleteSmsChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteSmsTemplate")
    def delete_sms_template(
        self,
        context: RequestContext,
        template_name: _string,
        version: _string | None = None,
        **kwargs,
    ) -> DeleteSmsTemplateResponse:
        """Deletes a message template for messages that were sent through the SMS
        channel.

        :param template_name: The name of the message template.
        :param version: The unique identifier for the version of the message template to update,
        retrieve information about, or delete.
        :returns: DeleteSmsTemplateResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteUserEndpoints")
    def delete_user_endpoints(
        self, context: RequestContext, application_id: _string, user_id: _string, **kwargs
    ) -> DeleteUserEndpointsResponse:
        """Deletes all the endpoints that are associated with a specific user ID.

        :param application_id: The unique identifier for the application.
        :param user_id: The unique identifier for the user.
        :returns: DeleteUserEndpointsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteVoiceChannel")
    def delete_voice_channel(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> DeleteVoiceChannelResponse:
        """Disables the voice channel for an application and deletes any existing
        settings for the channel.

        :param application_id: The unique identifier for the application.
        :returns: DeleteVoiceChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteVoiceTemplate")
    def delete_voice_template(
        self,
        context: RequestContext,
        template_name: _string,
        version: _string | None = None,
        **kwargs,
    ) -> DeleteVoiceTemplateResponse:
        """Deletes a message template for messages that were sent through the voice
        channel.

        :param template_name: The name of the message template.
        :param version: The unique identifier for the version of the message template to update,
        retrieve information about, or delete.
        :returns: DeleteVoiceTemplateResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetAdmChannel")
    def get_adm_channel(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> GetAdmChannelResponse:
        """Retrieves information about the status and settings of the ADM channel
        for an application.

        :param application_id: The unique identifier for the application.
        :returns: GetAdmChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetApnsChannel")
    def get_apns_channel(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> GetApnsChannelResponse:
        """Retrieves information about the status and settings of the APNs channel
        for an application.

        :param application_id: The unique identifier for the application.
        :returns: GetApnsChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetApnsSandboxChannel")
    def get_apns_sandbox_channel(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> GetApnsSandboxChannelResponse:
        """Retrieves information about the status and settings of the APNs sandbox
        channel for an application.

        :param application_id: The unique identifier for the application.
        :returns: GetApnsSandboxChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetApnsVoipChannel")
    def get_apns_voip_channel(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> GetApnsVoipChannelResponse:
        """Retrieves information about the status and settings of the APNs VoIP
        channel for an application.

        :param application_id: The unique identifier for the application.
        :returns: GetApnsVoipChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetApnsVoipSandboxChannel")
    def get_apns_voip_sandbox_channel(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> GetApnsVoipSandboxChannelResponse:
        """Retrieves information about the status and settings of the APNs VoIP
        sandbox channel for an application.

        :param application_id: The unique identifier for the application.
        :returns: GetApnsVoipSandboxChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetApp")
    def get_app(self, context: RequestContext, application_id: _string, **kwargs) -> GetAppResponse:
        """Retrieves information about an application.

        :param application_id: The unique identifier for the application.
        :returns: GetAppResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetApplicationDateRangeKpi")
    def get_application_date_range_kpi(
        self,
        context: RequestContext,
        application_id: _string,
        kpi_name: _string,
        end_time: _timestampIso8601 | None = None,
        next_token: _string | None = None,
        page_size: _string | None = None,
        start_time: _timestampIso8601 | None = None,
        **kwargs,
    ) -> GetApplicationDateRangeKpiResponse:
        """Retrieves (queries) pre-aggregated data for a standard metric that
        applies to an application.

        :param application_id: The unique identifier for the application.
        :param kpi_name: The name of the metric, also referred to as a *key performance indicator
        (KPI)*, to retrieve data for.
        :param end_time: The last date and time to retrieve data for, as part of an inclusive
        date range that filters the query results.
        :param next_token: The string that specifies which page of results to return in a paginated
        response.
        :param page_size: The maximum number of items to include in each page of a paginated
        response.
        :param start_time: The first date and time to retrieve data for, as part of an inclusive
        date range that filters the query results.
        :returns: GetApplicationDateRangeKpiResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetApplicationSettings")
    def get_application_settings(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> GetApplicationSettingsResponse:
        """Retrieves information about the settings for an application.

        :param application_id: The unique identifier for the application.
        :returns: GetApplicationSettingsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetApps")
    def get_apps(
        self,
        context: RequestContext,
        page_size: _string | None = None,
        token: _string | None = None,
        **kwargs,
    ) -> GetAppsResponse:
        """Retrieves information about all the applications that are associated
        with your Amazon Pinpoint account.

        :param page_size: The maximum number of items to include in each page of a paginated
        response.
        :param token: The NextToken string that specifies which page of results to return in a
        paginated response.
        :returns: GetAppsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetBaiduChannel")
    def get_baidu_channel(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> GetBaiduChannelResponse:
        """Retrieves information about the status and settings of the Baidu channel
        for an application.

        :param application_id: The unique identifier for the application.
        :returns: GetBaiduChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetCampaign")
    def get_campaign(
        self, context: RequestContext, campaign_id: _string, application_id: _string, **kwargs
    ) -> GetCampaignResponse:
        """Retrieves information about the status, configuration, and other
        settings for a campaign.

        :param campaign_id: The unique identifier for the campaign.
        :param application_id: The unique identifier for the application.
        :returns: GetCampaignResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetCampaignActivities")
    def get_campaign_activities(
        self,
        context: RequestContext,
        application_id: _string,
        campaign_id: _string,
        page_size: _string | None = None,
        token: _string | None = None,
        **kwargs,
    ) -> GetCampaignActivitiesResponse:
        """Retrieves information about all the activities for a campaign.

        :param application_id: The unique identifier for the application.
        :param campaign_id: The unique identifier for the campaign.
        :param page_size: The maximum number of items to include in each page of a paginated
        response.
        :param token: The NextToken string that specifies which page of results to return in a
        paginated response.
        :returns: GetCampaignActivitiesResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetCampaignDateRangeKpi")
    def get_campaign_date_range_kpi(
        self,
        context: RequestContext,
        application_id: _string,
        kpi_name: _string,
        campaign_id: _string,
        end_time: _timestampIso8601 | None = None,
        next_token: _string | None = None,
        page_size: _string | None = None,
        start_time: _timestampIso8601 | None = None,
        **kwargs,
    ) -> GetCampaignDateRangeKpiResponse:
        """Retrieves (queries) pre-aggregated data for a standard metric that
        applies to a campaign.

        :param application_id: The unique identifier for the application.
        :param kpi_name: The name of the metric, also referred to as a *key performance indicator
        (KPI)*, to retrieve data for.
        :param campaign_id: The unique identifier for the campaign.
        :param end_time: The last date and time to retrieve data for, as part of an inclusive
        date range that filters the query results.
        :param next_token: The string that specifies which page of results to return in a paginated
        response.
        :param page_size: The maximum number of items to include in each page of a paginated
        response.
        :param start_time: The first date and time to retrieve data for, as part of an inclusive
        date range that filters the query results.
        :returns: GetCampaignDateRangeKpiResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetCampaignVersion")
    def get_campaign_version(
        self,
        context: RequestContext,
        version: _string,
        application_id: _string,
        campaign_id: _string,
        **kwargs,
    ) -> GetCampaignVersionResponse:
        """Retrieves information about the status, configuration, and other
        settings for a specific version of a campaign.

        :param version: The unique version number (Version property) for the campaign version.
        :param application_id: The unique identifier for the application.
        :param campaign_id: The unique identifier for the campaign.
        :returns: GetCampaignVersionResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetCampaignVersions")
    def get_campaign_versions(
        self,
        context: RequestContext,
        application_id: _string,
        campaign_id: _string,
        page_size: _string | None = None,
        token: _string | None = None,
        **kwargs,
    ) -> GetCampaignVersionsResponse:
        """Retrieves information about the status, configuration, and other
        settings for all versions of a campaign.

        :param application_id: The unique identifier for the application.
        :param campaign_id: The unique identifier for the campaign.
        :param page_size: The maximum number of items to include in each page of a paginated
        response.
        :param token: The NextToken string that specifies which page of results to return in a
        paginated response.
        :returns: GetCampaignVersionsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetCampaigns")
    def get_campaigns(
        self,
        context: RequestContext,
        application_id: _string,
        page_size: _string | None = None,
        token: _string | None = None,
        **kwargs,
    ) -> GetCampaignsResponse:
        """Retrieves information about the status, configuration, and other
        settings for all the campaigns that are associated with an application.

        :param application_id: The unique identifier for the application.
        :param page_size: The maximum number of items to include in each page of a paginated
        response.
        :param token: The NextToken string that specifies which page of results to return in a
        paginated response.
        :returns: GetCampaignsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetChannels")
    def get_channels(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> GetChannelsResponse:
        """Retrieves information about the history and status of each channel for
        an application.

        :param application_id: The unique identifier for the application.
        :returns: GetChannelsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetEmailChannel")
    def get_email_channel(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> GetEmailChannelResponse:
        """Retrieves information about the status and settings of the email channel
        for an application.

        :param application_id: The unique identifier for the application.
        :returns: GetEmailChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetEmailTemplate")
    def get_email_template(
        self,
        context: RequestContext,
        template_name: _string,
        version: _string | None = None,
        **kwargs,
    ) -> GetEmailTemplateResponse:
        """Retrieves the content and settings of a message template for messages
        that are sent through the email channel.

        :param template_name: The name of the message template.
        :param version: The unique identifier for the version of the message template to update,
        retrieve information about, or delete.
        :returns: GetEmailTemplateResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetEndpoint")
    def get_endpoint(
        self, context: RequestContext, application_id: _string, endpoint_id: _string, **kwargs
    ) -> GetEndpointResponse:
        """Retrieves information about the settings and attributes of a specific
        endpoint for an application.

        :param application_id: The unique identifier for the application.
        :param endpoint_id: The case insensitive unique identifier for the endpoint.
        :returns: GetEndpointResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetEventStream")
    def get_event_stream(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> GetEventStreamResponse:
        """Retrieves information about the event stream settings for an
        application.

        :param application_id: The unique identifier for the application.
        :returns: GetEventStreamResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetExportJob")
    def get_export_job(
        self, context: RequestContext, application_id: _string, job_id: _string, **kwargs
    ) -> GetExportJobResponse:
        """Retrieves information about the status and settings of a specific export
        job for an application.

        :param application_id: The unique identifier for the application.
        :param job_id: The unique identifier for the job.
        :returns: GetExportJobResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetExportJobs")
    def get_export_jobs(
        self,
        context: RequestContext,
        application_id: _string,
        page_size: _string | None = None,
        token: _string | None = None,
        **kwargs,
    ) -> GetExportJobsResponse:
        """Retrieves information about the status and settings of all the export
        jobs for an application.

        :param application_id: The unique identifier for the application.
        :param page_size: The maximum number of items to include in each page of a paginated
        response.
        :param token: The NextToken string that specifies which page of results to return in a
        paginated response.
        :returns: GetExportJobsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetGcmChannel")
    def get_gcm_channel(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> GetGcmChannelResponse:
        """Retrieves information about the status and settings of the GCM channel
        for an application.

        :param application_id: The unique identifier for the application.
        :returns: GetGcmChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetImportJob")
    def get_import_job(
        self, context: RequestContext, application_id: _string, job_id: _string, **kwargs
    ) -> GetImportJobResponse:
        """Retrieves information about the status and settings of a specific import
        job for an application.

        :param application_id: The unique identifier for the application.
        :param job_id: The unique identifier for the job.
        :returns: GetImportJobResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetImportJobs")
    def get_import_jobs(
        self,
        context: RequestContext,
        application_id: _string,
        page_size: _string | None = None,
        token: _string | None = None,
        **kwargs,
    ) -> GetImportJobsResponse:
        """Retrieves information about the status and settings of all the import
        jobs for an application.

        :param application_id: The unique identifier for the application.
        :param page_size: The maximum number of items to include in each page of a paginated
        response.
        :param token: The NextToken string that specifies which page of results to return in a
        paginated response.
        :returns: GetImportJobsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetInAppMessages")
    def get_in_app_messages(
        self, context: RequestContext, application_id: _string, endpoint_id: _string, **kwargs
    ) -> GetInAppMessagesResponse:
        """Retrieves the in-app messages targeted for the provided endpoint ID.

        :param application_id: The unique identifier for the application.
        :param endpoint_id: The unique identifier for the endpoint.
        :returns: GetInAppMessagesResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetInAppTemplate")
    def get_in_app_template(
        self,
        context: RequestContext,
        template_name: _string,
        version: _string | None = None,
        **kwargs,
    ) -> GetInAppTemplateResponse:
        """Retrieves the content and settings of a message template for messages
        sent through the in-app channel.

        :param template_name: The name of the message template.
        :param version: The unique identifier for the version of the message template to update,
        retrieve information about, or delete.
        :returns: GetInAppTemplateResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetJourney")
    def get_journey(
        self, context: RequestContext, journey_id: _string, application_id: _string, **kwargs
    ) -> GetJourneyResponse:
        """Retrieves information about the status, configuration, and other
        settings for a journey.

        :param journey_id: The unique identifier for the journey.
        :param application_id: The unique identifier for the application.
        :returns: GetJourneyResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetJourneyDateRangeKpi")
    def get_journey_date_range_kpi(
        self,
        context: RequestContext,
        journey_id: _string,
        application_id: _string,
        kpi_name: _string,
        end_time: _timestampIso8601 | None = None,
        next_token: _string | None = None,
        page_size: _string | None = None,
        start_time: _timestampIso8601 | None = None,
        **kwargs,
    ) -> GetJourneyDateRangeKpiResponse:
        """Retrieves (queries) pre-aggregated data for a standard engagement metric
        that applies to a journey.

        :param journey_id: The unique identifier for the journey.
        :param application_id: The unique identifier for the application.
        :param kpi_name: The name of the metric, also referred to as a *key performance indicator
        (KPI)*, to retrieve data for.
        :param end_time: The last date and time to retrieve data for, as part of an inclusive
        date range that filters the query results.
        :param next_token: The string that specifies which page of results to return in a paginated
        response.
        :param page_size: The maximum number of items to include in each page of a paginated
        response.
        :param start_time: The first date and time to retrieve data for, as part of an inclusive
        date range that filters the query results.
        :returns: GetJourneyDateRangeKpiResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetJourneyExecutionActivityMetrics")
    def get_journey_execution_activity_metrics(
        self,
        context: RequestContext,
        journey_activity_id: _string,
        application_id: _string,
        journey_id: _string,
        next_token: _string | None = None,
        page_size: _string | None = None,
        **kwargs,
    ) -> GetJourneyExecutionActivityMetricsResponse:
        """Retrieves (queries) pre-aggregated data for a standard execution metric
        that applies to a journey activity.

        :param journey_activity_id: The unique identifier for the journey activity.
        :param application_id: The unique identifier for the application.
        :param journey_id: The unique identifier for the journey.
        :param next_token: The ```` string that specifies which page of results to return in a
        paginated response.
        :param page_size: The maximum number of items to include in each page of a paginated
        response.
        :returns: GetJourneyExecutionActivityMetricsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetJourneyExecutionMetrics")
    def get_journey_execution_metrics(
        self,
        context: RequestContext,
        application_id: _string,
        journey_id: _string,
        next_token: _string | None = None,
        page_size: _string | None = None,
        **kwargs,
    ) -> GetJourneyExecutionMetricsResponse:
        """Retrieves (queries) pre-aggregated data for a standard execution metric
        that applies to a journey.

        :param application_id: The unique identifier for the application.
        :param journey_id: The unique identifier for the journey.
        :param next_token: The ```` string that specifies which page of results to return in a
        paginated response.
        :param page_size: The maximum number of items to include in each page of a paginated
        response.
        :returns: GetJourneyExecutionMetricsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetJourneyRunExecutionActivityMetrics")
    def get_journey_run_execution_activity_metrics(
        self,
        context: RequestContext,
        run_id: _string,
        journey_activity_id: _string,
        journey_id: _string,
        application_id: _string,
        next_token: _string | None = None,
        page_size: _string | None = None,
        **kwargs,
    ) -> GetJourneyRunExecutionActivityMetricsResponse:
        """Retrieves (queries) pre-aggregated data for a standard run execution
        metric that applies to a journey activity.

        :param run_id: The unique identifier for the journey run.
        :param journey_activity_id: The unique identifier for the journey activity.
        :param journey_id: The unique identifier for the journey.
        :param application_id: The unique identifier for the application.
        :param next_token: The ```` string that specifies which page of results to return in a
        paginated response.
        :param page_size: The maximum number of items to include in each page of a paginated
        response.
        :returns: GetJourneyRunExecutionActivityMetricsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetJourneyRunExecutionMetrics")
    def get_journey_run_execution_metrics(
        self,
        context: RequestContext,
        run_id: _string,
        application_id: _string,
        journey_id: _string,
        next_token: _string | None = None,
        page_size: _string | None = None,
        **kwargs,
    ) -> GetJourneyRunExecutionMetricsResponse:
        """Retrieves (queries) pre-aggregated data for a standard run execution
        metric that applies to a journey.

        :param run_id: The unique identifier for the journey run.
        :param application_id: The unique identifier for the application.
        :param journey_id: The unique identifier for the journey.
        :param next_token: The ```` string that specifies which page of results to return in a
        paginated response.
        :param page_size: The maximum number of items to include in each page of a paginated
        response.
        :returns: GetJourneyRunExecutionMetricsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetJourneyRuns")
    def get_journey_runs(
        self,
        context: RequestContext,
        application_id: _string,
        journey_id: _string,
        page_size: _string | None = None,
        token: _string | None = None,
        **kwargs,
    ) -> GetJourneyRunsResponse:
        """Provides information about the runs of a journey.

        :param application_id: The unique identifier for the application.
        :param journey_id: The unique identifier for the journey.
        :param page_size: The maximum number of items to include in each page of a paginated
        response.
        :param token: The NextToken string that specifies which page of results to return in a
        paginated response.
        :returns: GetJourneyRunsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetPushTemplate")
    def get_push_template(
        self,
        context: RequestContext,
        template_name: _string,
        version: _string | None = None,
        **kwargs,
    ) -> GetPushTemplateResponse:
        """Retrieves the content and settings of a message template for messages
        that are sent through a push notification channel.

        :param template_name: The name of the message template.
        :param version: The unique identifier for the version of the message template to update,
        retrieve information about, or delete.
        :returns: GetPushTemplateResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetRecommenderConfiguration")
    def get_recommender_configuration(
        self, context: RequestContext, recommender_id: _string, **kwargs
    ) -> GetRecommenderConfigurationResponse:
        """Retrieves information about an Amazon Pinpoint configuration for a
        recommender model.

        :param recommender_id: The unique identifier for the recommender model configuration.
        :returns: GetRecommenderConfigurationResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetRecommenderConfigurations")
    def get_recommender_configurations(
        self,
        context: RequestContext,
        page_size: _string | None = None,
        token: _string | None = None,
        **kwargs,
    ) -> GetRecommenderConfigurationsResponse:
        """Retrieves information about all the recommender model configurations
        that are associated with your Amazon Pinpoint account.

        :param page_size: The maximum number of items to include in each page of a paginated
        response.
        :param token: The NextToken string that specifies which page of results to return in a
        paginated response.
        :returns: GetRecommenderConfigurationsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetSegment")
    def get_segment(
        self, context: RequestContext, segment_id: _string, application_id: _string, **kwargs
    ) -> GetSegmentResponse:
        """Retrieves information about the configuration, dimension, and other
        settings for a specific segment that's associated with an application.

        :param segment_id: The unique identifier for the segment.
        :param application_id: The unique identifier for the application.
        :returns: GetSegmentResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetSegmentExportJobs")
    def get_segment_export_jobs(
        self,
        context: RequestContext,
        segment_id: _string,
        application_id: _string,
        page_size: _string | None = None,
        token: _string | None = None,
        **kwargs,
    ) -> GetSegmentExportJobsResponse:
        """Retrieves information about the status and settings of the export jobs
        for a segment.

        :param segment_id: The unique identifier for the segment.
        :param application_id: The unique identifier for the application.
        :param page_size: The maximum number of items to include in each page of a paginated
        response.
        :param token: The NextToken string that specifies which page of results to return in a
        paginated response.
        :returns: GetSegmentExportJobsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetSegmentImportJobs")
    def get_segment_import_jobs(
        self,
        context: RequestContext,
        segment_id: _string,
        application_id: _string,
        page_size: _string | None = None,
        token: _string | None = None,
        **kwargs,
    ) -> GetSegmentImportJobsResponse:
        """Retrieves information about the status and settings of the import jobs
        for a segment.

        :param segment_id: The unique identifier for the segment.
        :param application_id: The unique identifier for the application.
        :param page_size: The maximum number of items to include in each page of a paginated
        response.
        :param token: The NextToken string that specifies which page of results to return in a
        paginated response.
        :returns: GetSegmentImportJobsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetSegmentVersion")
    def get_segment_version(
        self,
        context: RequestContext,
        segment_id: _string,
        version: _string,
        application_id: _string,
        **kwargs,
    ) -> GetSegmentVersionResponse:
        """Retrieves information about the configuration, dimension, and other
        settings for a specific version of a segment that's associated with an
        application.

        :param segment_id: The unique identifier for the segment.
        :param version: The unique version number (Version property) for the campaign version.
        :param application_id: The unique identifier for the application.
        :returns: GetSegmentVersionResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetSegmentVersions")
    def get_segment_versions(
        self,
        context: RequestContext,
        segment_id: _string,
        application_id: _string,
        page_size: _string | None = None,
        token: _string | None = None,
        **kwargs,
    ) -> GetSegmentVersionsResponse:
        """Retrieves information about the configuration, dimension, and other
        settings for all the versions of a specific segment that's associated
        with an application.

        :param segment_id: The unique identifier for the segment.
        :param application_id: The unique identifier for the application.
        :param page_size: The maximum number of items to include in each page of a paginated
        response.
        :param token: The NextToken string that specifies which page of results to return in a
        paginated response.
        :returns: GetSegmentVersionsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetSegments")
    def get_segments(
        self,
        context: RequestContext,
        application_id: _string,
        page_size: _string | None = None,
        token: _string | None = None,
        **kwargs,
    ) -> GetSegmentsResponse:
        """Retrieves information about the configuration, dimension, and other
        settings for all the segments that are associated with an application.

        :param application_id: The unique identifier for the application.
        :param page_size: The maximum number of items to include in each page of a paginated
        response.
        :param token: The NextToken string that specifies which page of results to return in a
        paginated response.
        :returns: GetSegmentsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetSmsChannel")
    def get_sms_channel(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> GetSmsChannelResponse:
        """Retrieves information about the status and settings of the SMS channel
        for an application.

        :param application_id: The unique identifier for the application.
        :returns: GetSmsChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetSmsTemplate")
    def get_sms_template(
        self,
        context: RequestContext,
        template_name: _string,
        version: _string | None = None,
        **kwargs,
    ) -> GetSmsTemplateResponse:
        """Retrieves the content and settings of a message template for messages
        that are sent through the SMS channel.

        :param template_name: The name of the message template.
        :param version: The unique identifier for the version of the message template to update,
        retrieve information about, or delete.
        :returns: GetSmsTemplateResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetUserEndpoints")
    def get_user_endpoints(
        self, context: RequestContext, application_id: _string, user_id: _string, **kwargs
    ) -> GetUserEndpointsResponse:
        """Retrieves information about all the endpoints that are associated with a
        specific user ID.

        :param application_id: The unique identifier for the application.
        :param user_id: The unique identifier for the user.
        :returns: GetUserEndpointsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetVoiceChannel")
    def get_voice_channel(
        self, context: RequestContext, application_id: _string, **kwargs
    ) -> GetVoiceChannelResponse:
        """Retrieves information about the status and settings of the voice channel
        for an application.

        :param application_id: The unique identifier for the application.
        :returns: GetVoiceChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetVoiceTemplate")
    def get_voice_template(
        self,
        context: RequestContext,
        template_name: _string,
        version: _string | None = None,
        **kwargs,
    ) -> GetVoiceTemplateResponse:
        """Retrieves the content and settings of a message template for messages
        that are sent through the voice channel.

        :param template_name: The name of the message template.
        :param version: The unique identifier for the version of the message template to update,
        retrieve information about, or delete.
        :returns: GetVoiceTemplateResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("ListJourneys")
    def list_journeys(
        self,
        context: RequestContext,
        application_id: _string,
        page_size: _string | None = None,
        token: _string | None = None,
        **kwargs,
    ) -> ListJourneysResponse:
        """Retrieves information about the status, configuration, and other
        settings for all the journeys that are associated with an application.

        :param application_id: The unique identifier for the application.
        :param page_size: The maximum number of items to include in each page of a paginated
        response.
        :param token: The NextToken string that specifies which page of results to return in a
        paginated response.
        :returns: ListJourneysResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("ListTagsForResource")
    def list_tags_for_resource(
        self, context: RequestContext, resource_arn: _string, **kwargs
    ) -> ListTagsForResourceResponse:
        """Retrieves all the tags (keys and values) that are associated with an
        application, campaign, message template, or segment.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource.
        :returns: ListTagsForResourceResponse
        """
        raise NotImplementedError

    @handler("ListTemplateVersions")
    def list_template_versions(
        self,
        context: RequestContext,
        template_name: _string,
        template_type: _string,
        next_token: _string | None = None,
        page_size: _string | None = None,
        **kwargs,
    ) -> ListTemplateVersionsResponse:
        """Retrieves information about all the versions of a specific message
        template.

        :param template_name: The name of the message template.
        :param template_type: The type of channel that the message template is designed for.
        :param next_token: The string that specifies which page of results to return in a paginated
        response.
        :param page_size: The maximum number of items to include in each page of a paginated
        response.
        :returns: ListTemplateVersionsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("ListTemplates")
    def list_templates(
        self,
        context: RequestContext,
        next_token: _string | None = None,
        page_size: _string | None = None,
        prefix: _string | None = None,
        template_type: _string | None = None,
        **kwargs,
    ) -> ListTemplatesResponse:
        """Retrieves information about all the message templates that are
        associated with your Amazon Pinpoint account.

        :param next_token: The string that specifies which page of results to return in a paginated
        response.
        :param page_size: The maximum number of items to include in each page of a paginated
        response.
        :param prefix: The substring to match in the names of the message templates to include
        in the results.
        :param template_type: The type of message template to include in the results.
        :returns: ListTemplatesResponse
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("PhoneNumberValidate")
    def phone_number_validate(
        self, context: RequestContext, number_validate_request: NumberValidateRequest, **kwargs
    ) -> PhoneNumberValidateResponse:
        """Retrieves information about a phone number.

        :param number_validate_request: Specifies a phone number to validate and retrieve information about.
        :returns: PhoneNumberValidateResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("PutEventStream")
    def put_event_stream(
        self,
        context: RequestContext,
        application_id: _string,
        write_event_stream: WriteEventStream,
        **kwargs,
    ) -> PutEventStreamResponse:
        """Creates a new event stream for an application or updates the settings of
        an existing event stream for an application.

        :param application_id: The unique identifier for the application.
        :param write_event_stream: Specifies the Amazon Resource Name (ARN) of an event stream to publish
        events to and the AWS Identity and Access Management (IAM) role to use
        when publishing those events.
        :returns: PutEventStreamResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("PutEvents")
    def put_events(
        self,
        context: RequestContext,
        application_id: _string,
        events_request: EventsRequest,
        **kwargs,
    ) -> PutEventsResponse:
        """Creates a new event to record for endpoints, or creates or updates
        endpoint data that existing events are associated with.

        :param application_id: The unique identifier for the application.
        :param events_request: Specifies a batch of events to process.
        :returns: PutEventsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("RemoveAttributes")
    def remove_attributes(
        self,
        context: RequestContext,
        attribute_type: _string,
        application_id: _string,
        update_attributes_request: UpdateAttributesRequest,
        **kwargs,
    ) -> RemoveAttributesResponse:
        """Removes one or more custom attributes, of the same attribute type, from
        the application. Existing endpoints still have the attributes but Amazon
        Pinpoint will stop capturing new or changed values for these attributes.

        :param attribute_type: The type of attribute or attributes to remove.
        :param application_id: The unique identifier for the application.
        :param update_attributes_request: Specifies one or more attributes to remove from all the endpoints that
        are associated with an application.
        :returns: RemoveAttributesResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("SendMessages")
    def send_messages(
        self,
        context: RequestContext,
        application_id: _string,
        message_request: MessageRequest,
        **kwargs,
    ) -> SendMessagesResponse:
        """Creates and sends a direct message.

        :param application_id: The unique identifier for the application.
        :param message_request: Specifies the configuration and other settings for a message.
        :returns: SendMessagesResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("SendOTPMessage")
    def send_otp_message(
        self,
        context: RequestContext,
        application_id: _string,
        send_otp_message_request_parameters: SendOTPMessageRequestParameters,
        **kwargs,
    ) -> SendOTPMessageResponse:
        """Send an OTP message

        :param application_id: The unique ID of your Amazon Pinpoint application.
        :param send_otp_message_request_parameters: Send OTP message request parameters.
        :returns: SendOTPMessageResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("SendUsersMessages")
    def send_users_messages(
        self,
        context: RequestContext,
        application_id: _string,
        send_users_message_request: SendUsersMessageRequest,
        **kwargs,
    ) -> SendUsersMessagesResponse:
        """Creates and sends a message to a list of users.

        :param application_id: The unique identifier for the application.
        :param send_users_message_request: Specifies the configuration and other settings for a message to send to
        all the endpoints that are associated with a list of users.
        :returns: SendUsersMessagesResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("TagResource")
    def tag_resource(
        self, context: RequestContext, resource_arn: _string, tags_model: TagsModel, **kwargs
    ) -> None:
        """Adds one or more tags (keys and values) to an application, campaign,
        message template, or segment.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource.
        :param tags_model: Specifies the tags (keys and values) for an application, campaign,
        message template, or segment.
        """
        raise NotImplementedError

    @handler("UntagResource")
    def untag_resource(
        self, context: RequestContext, tag_keys: ListOf__string, resource_arn: _string, **kwargs
    ) -> None:
        """Removes one or more tags (keys and values) from an application,
        campaign, message template, or segment.

        :param tag_keys: The key of the tag to remove from the resource.
        :param resource_arn: The Amazon Resource Name (ARN) of the resource.
        """
        raise NotImplementedError

    @handler("UpdateAdmChannel")
    def update_adm_channel(
        self,
        context: RequestContext,
        application_id: _string,
        adm_channel_request: ADMChannelRequest,
        **kwargs,
    ) -> UpdateAdmChannelResponse:
        """Enables the ADM channel for an application or updates the status and
        settings of the ADM channel for an application.

        :param application_id: The unique identifier for the application.
        :param adm_channel_request: Specifies the status and settings of the ADM (Amazon Device Messaging)
        channel for an application.
        :returns: UpdateAdmChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateApnsChannel")
    def update_apns_channel(
        self,
        context: RequestContext,
        application_id: _string,
        apns_channel_request: APNSChannelRequest,
        **kwargs,
    ) -> UpdateApnsChannelResponse:
        """Enables the APNs channel for an application or updates the status and
        settings of the APNs channel for an application.

        :param application_id: The unique identifier for the application.
        :param apns_channel_request: Specifies the status and settings of the APNs (Apple Push Notification
        service) channel for an application.
        :returns: UpdateApnsChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateApnsSandboxChannel")
    def update_apns_sandbox_channel(
        self,
        context: RequestContext,
        application_id: _string,
        apns_sandbox_channel_request: APNSSandboxChannelRequest,
        **kwargs,
    ) -> UpdateApnsSandboxChannelResponse:
        """Enables the APNs sandbox channel for an application or updates the
        status and settings of the APNs sandbox channel for an application.

        :param application_id: The unique identifier for the application.
        :param apns_sandbox_channel_request: Specifies the status and settings of the APNs (Apple Push Notification
        service) sandbox channel for an application.
        :returns: UpdateApnsSandboxChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateApnsVoipChannel")
    def update_apns_voip_channel(
        self,
        context: RequestContext,
        application_id: _string,
        apns_voip_channel_request: APNSVoipChannelRequest,
        **kwargs,
    ) -> UpdateApnsVoipChannelResponse:
        """Enables the APNs VoIP channel for an application or updates the status
        and settings of the APNs VoIP channel for an application.

        :param application_id: The unique identifier for the application.
        :param apns_voip_channel_request: Specifies the status and settings of the APNs (Apple Push Notification
        service) VoIP channel for an application.
        :returns: UpdateApnsVoipChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateApnsVoipSandboxChannel")
    def update_apns_voip_sandbox_channel(
        self,
        context: RequestContext,
        application_id: _string,
        apns_voip_sandbox_channel_request: APNSVoipSandboxChannelRequest,
        **kwargs,
    ) -> UpdateApnsVoipSandboxChannelResponse:
        """Enables the APNs VoIP sandbox channel for an application or updates the
        status and settings of the APNs VoIP sandbox channel for an application.

        :param application_id: The unique identifier for the application.
        :param apns_voip_sandbox_channel_request: Specifies the status and settings of the APNs (Apple Push Notification
        service) VoIP sandbox channel for an application.
        :returns: UpdateApnsVoipSandboxChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateApplicationSettings")
    def update_application_settings(
        self,
        context: RequestContext,
        application_id: _string,
        write_application_settings_request: WriteApplicationSettingsRequest,
        **kwargs,
    ) -> UpdateApplicationSettingsResponse:
        """Updates the settings for an application.

        :param application_id: The unique identifier for the application.
        :param write_application_settings_request: Specifies the default settings for an application.
        :returns: UpdateApplicationSettingsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateBaiduChannel")
    def update_baidu_channel(
        self,
        context: RequestContext,
        application_id: _string,
        baidu_channel_request: BaiduChannelRequest,
        **kwargs,
    ) -> UpdateBaiduChannelResponse:
        """Enables the Baidu channel for an application or updates the status and
        settings of the Baidu channel for an application.

        :param application_id: The unique identifier for the application.
        :param baidu_channel_request: Specifies the status and settings of the Baidu (Baidu Cloud Push)
        channel for an application.
        :returns: UpdateBaiduChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateCampaign")
    def update_campaign(
        self,
        context: RequestContext,
        campaign_id: _string,
        application_id: _string,
        write_campaign_request: WriteCampaignRequest,
        **kwargs,
    ) -> UpdateCampaignResponse:
        """Updates the configuration and other settings for a campaign.

        :param campaign_id: The unique identifier for the campaign.
        :param application_id: The unique identifier for the application.
        :param write_campaign_request: Specifies the configuration and other settings for a campaign.
        :returns: UpdateCampaignResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateEmailChannel")
    def update_email_channel(
        self,
        context: RequestContext,
        application_id: _string,
        email_channel_request: EmailChannelRequest,
        **kwargs,
    ) -> UpdateEmailChannelResponse:
        """Enables the email channel for an application or updates the status and
        settings of the email channel for an application.

        :param application_id: The unique identifier for the application.
        :param email_channel_request: Specifies the status and settings of the email channel for an
        application.
        :returns: UpdateEmailChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateEmailTemplate")
    def update_email_template(
        self,
        context: RequestContext,
        template_name: _string,
        email_template_request: EmailTemplateRequest,
        create_new_version: _boolean | None = None,
        version: _string | None = None,
        **kwargs,
    ) -> UpdateEmailTemplateResponse:
        """Updates an existing message template for messages that are sent through
        the email channel.

        :param template_name: The name of the message template.
        :param email_template_request: Specifies the content and settings for a message template that can be
        used in messages that are sent through the email channel.
        :param create_new_version: Specifies whether to save the updates as a new version of the message
        template.
        :param version: The unique identifier for the version of the message template to update,
        retrieve information about, or delete.
        :returns: UpdateEmailTemplateResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateEndpoint")
    def update_endpoint(
        self,
        context: RequestContext,
        application_id: _string,
        endpoint_id: _string,
        endpoint_request: EndpointRequest,
        **kwargs,
    ) -> UpdateEndpointResponse:
        """Creates a new endpoint for an application or updates the settings and
        attributes of an existing endpoint for an application. You can also use
        this operation to define custom attributes for an endpoint. If an update
        includes one or more values for a custom attribute, Amazon Pinpoint
        replaces (overwrites) any existing values with the new values.

        :param application_id: The unique identifier for the application.
        :param endpoint_id: The case insensitive unique identifier for the endpoint.
        :param endpoint_request: Specifies the channel type and other settings for an endpoint.
        :returns: UpdateEndpointResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateEndpointsBatch")
    def update_endpoints_batch(
        self,
        context: RequestContext,
        application_id: _string,
        endpoint_batch_request: EndpointBatchRequest,
        **kwargs,
    ) -> UpdateEndpointsBatchResponse:
        """Creates a new batch of endpoints for an application or updates the
        settings and attributes of a batch of existing endpoints for an
        application. You can also use this operation to define custom attributes
        for a batch of endpoints. If an update includes one or more values for a
        custom attribute, Amazon Pinpoint replaces (overwrites) any existing
        values with the new values.

        :param application_id: The unique identifier for the application.
        :param endpoint_batch_request: Specifies a batch of endpoints to create or update and the settings and
        attributes to set or change for each endpoint.
        :returns: UpdateEndpointsBatchResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateGcmChannel")
    def update_gcm_channel(
        self,
        context: RequestContext,
        application_id: _string,
        gcm_channel_request: GCMChannelRequest,
        **kwargs,
    ) -> UpdateGcmChannelResponse:
        """Enables the GCM channel for an application or updates the status and
        settings of the GCM channel for an application.

        :param application_id: The unique identifier for the application.
        :param gcm_channel_request: Specifies the status and settings of the GCM channel for an application.
        :returns: UpdateGcmChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateInAppTemplate")
    def update_in_app_template(
        self,
        context: RequestContext,
        template_name: _string,
        in_app_template_request: InAppTemplateRequest,
        create_new_version: _boolean | None = None,
        version: _string | None = None,
        **kwargs,
    ) -> UpdateInAppTemplateResponse:
        """Updates an existing message template for messages sent through the
        in-app message channel.

        :param template_name: The name of the message template.
        :param in_app_template_request: InApp Template Request.
        :param create_new_version: Specifies whether to save the updates as a new version of the message
        template.
        :param version: The unique identifier for the version of the message template to update,
        retrieve information about, or delete.
        :returns: UpdateInAppTemplateResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateJourney")
    def update_journey(
        self,
        context: RequestContext,
        journey_id: _string,
        application_id: _string,
        write_journey_request: WriteJourneyRequest,
        **kwargs,
    ) -> UpdateJourneyResponse:
        """Updates the configuration and other settings for a journey.

        :param journey_id: The unique identifier for the journey.
        :param application_id: The unique identifier for the application.
        :param write_journey_request: Specifies the configuration and other settings for a journey.
        :returns: UpdateJourneyResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("UpdateJourneyState")
    def update_journey_state(
        self,
        context: RequestContext,
        journey_id: _string,
        application_id: _string,
        journey_state_request: JourneyStateRequest,
        **kwargs,
    ) -> UpdateJourneyStateResponse:
        """Cancels (stops) an active journey.

        :param journey_id: The unique identifier for the journey.
        :param application_id: The unique identifier for the application.
        :param journey_state_request: Changes the status of a journey.
        :returns: UpdateJourneyStateResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdatePushTemplate")
    def update_push_template(
        self,
        context: RequestContext,
        template_name: _string,
        push_notification_template_request: PushNotificationTemplateRequest,
        create_new_version: _boolean | None = None,
        version: _string | None = None,
        **kwargs,
    ) -> UpdatePushTemplateResponse:
        """Updates an existing message template for messages that are sent through
        a push notification channel.

        :param template_name: The name of the message template.
        :param push_notification_template_request: Specifies the content and settings for a message template that can be
        used in messages that are sent through a push notification channel.
        :param create_new_version: Specifies whether to save the updates as a new version of the message
        template.
        :param version: The unique identifier for the version of the message template to update,
        retrieve information about, or delete.
        :returns: UpdatePushTemplateResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateRecommenderConfiguration")
    def update_recommender_configuration(
        self,
        context: RequestContext,
        recommender_id: _string,
        update_recommender_configuration: UpdateRecommenderConfiguration,
        **kwargs,
    ) -> UpdateRecommenderConfigurationResponse:
        """Updates an Amazon Pinpoint configuration for a recommender model.

        :param recommender_id: The unique identifier for the recommender model configuration.
        :param update_recommender_configuration: Specifies Amazon Pinpoint configuration settings for retrieving and
        processing recommendation data from a recommender model.
        :returns: UpdateRecommenderConfigurationResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateSegment")
    def update_segment(
        self,
        context: RequestContext,
        segment_id: _string,
        application_id: _string,
        write_segment_request: WriteSegmentRequest,
        **kwargs,
    ) -> UpdateSegmentResponse:
        """Creates a new segment for an application or updates the configuration,
        dimension, and other settings for an existing segment that's associated
        with an application.

        :param segment_id: The unique identifier for the segment.
        :param application_id: The unique identifier for the application.
        :param write_segment_request: Specifies the configuration, dimension, and other settings for a
        segment.
        :returns: UpdateSegmentResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateSmsChannel")
    def update_sms_channel(
        self,
        context: RequestContext,
        application_id: _string,
        sms_channel_request: SMSChannelRequest,
        **kwargs,
    ) -> UpdateSmsChannelResponse:
        """Enables the SMS channel for an application or updates the status and
        settings of the SMS channel for an application.

        :param application_id: The unique identifier for the application.
        :param sms_channel_request: Specifies the status and settings of the SMS channel for an application.
        :returns: UpdateSmsChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateSmsTemplate")
    def update_sms_template(
        self,
        context: RequestContext,
        template_name: _string,
        sms_template_request: SMSTemplateRequest,
        create_new_version: _boolean | None = None,
        version: _string | None = None,
        **kwargs,
    ) -> UpdateSmsTemplateResponse:
        """Updates an existing message template for messages that are sent through
        the SMS channel.

        :param template_name: The name of the message template.
        :param sms_template_request: Specifies the content and settings for a message template that can be
        used in text messages that are sent through the SMS channel.
        :param create_new_version: Specifies whether to save the updates as a new version of the message
        template.
        :param version: The unique identifier for the version of the message template to update,
        retrieve information about, or delete.
        :returns: UpdateSmsTemplateResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateTemplateActiveVersion")
    def update_template_active_version(
        self,
        context: RequestContext,
        template_name: _string,
        template_type: _string,
        template_active_version_request: TemplateActiveVersionRequest,
        **kwargs,
    ) -> UpdateTemplateActiveVersionResponse:
        """Changes the status of a specific version of a message template to
        *active*.

        :param template_name: The name of the message template.
        :param template_type: The type of channel that the message template is designed for.
        :param template_active_version_request: Specifies which version of a message template to use as the active
        version of the template.
        :returns: UpdateTemplateActiveVersionResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateVoiceChannel")
    def update_voice_channel(
        self,
        context: RequestContext,
        application_id: _string,
        voice_channel_request: VoiceChannelRequest,
        **kwargs,
    ) -> UpdateVoiceChannelResponse:
        """Enables the voice channel for an application or updates the status and
        settings of the voice channel for an application.

        :param application_id: The unique identifier for the application.
        :param voice_channel_request: Specifies the status and settings of the voice channel for an
        application.
        :returns: UpdateVoiceChannelResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateVoiceTemplate")
    def update_voice_template(
        self,
        context: RequestContext,
        template_name: _string,
        voice_template_request: VoiceTemplateRequest,
        create_new_version: _boolean | None = None,
        version: _string | None = None,
        **kwargs,
    ) -> UpdateVoiceTemplateResponse:
        """Updates an existing message template for messages that are sent through
        the voice channel.

        :param template_name: The name of the message template.
        :param voice_template_request: Specifies the content and settings for a message template that can be
        used in messages that are sent through the voice channel.
        :param create_new_version: Specifies whether to save the updates as a new version of the message
        template.
        :param version: The unique identifier for the version of the message template to update,
        retrieve information about, or delete.
        :returns: UpdateVoiceTemplateResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("VerifyOTPMessage")
    def verify_otp_message(
        self,
        context: RequestContext,
        application_id: _string,
        verify_otp_message_request_parameters: VerifyOTPMessageRequestParameters,
        **kwargs,
    ) -> VerifyOTPMessageResponse:
        """Verify an OTP

        :param application_id: The unique ID of your Amazon Pinpoint application.
        :param verify_otp_message_request_parameters: Verify OTP message request.
        :returns: VerifyOTPMessageResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises PayloadTooLargeException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises MethodNotAllowedException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError
