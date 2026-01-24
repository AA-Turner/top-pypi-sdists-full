from enum import StrEnum
from typing import TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

AccountId = str
AmortizedRecurringFee = str
AmortizedUpfrontFee = str
AnalysisId = str
Arn = str
AttributeType = str
AttributeValue = str
BillingViewArn = str
CostAllocationTagsMaxResults = int
CostAndUsageComparisonsMaxResults = int
CostCategoryMaxResults = int
CostCategoryName = str
CostCategoryValue = str
CostComparisonDriversMaxResults = int
CoverageHoursPercentage = str
CoverageNormalizedUnitsPercentage = str
Entity = str
ErrorMessage = str
Estimated = bool
GenericBoolean = bool
GenericDouble = float
GenericString = str
GroupDefinitionKey = str
Key = str
MaxResults = int
MetricAmount = str
MetricName = str
MetricUnit = str
NetRISavings = str
NextPageToken = str
NonNegativeInteger = int
NullableNonNegativeDouble = float
OnDemandCost = str
OnDemandCostOfRIHoursUsed = str
OnDemandHours = str
OnDemandNormalizedUnits = str
PageSize = int
PredictionIntervalLevel = int
PurchasedHours = str
PurchasedUnits = str
RICostForUnusedHours = str
RealizedSavings = str
RecommendationDetailId = str
RecommendationId = str
ReservationGroupKey = str
ReservationGroupValue = str
ReservedHours = str
ReservedNormalizedUnits = str
ResourceTagKey = str
ResourceTagValue = str
SavingsPlanArn = str
SavingsPlansCommitment = float
SavingsPlansId = str
SearchString = str
SortDefinitionKey = str
SubscriberAddress = str
TagKey = str
TotalActualHours = str
TotalActualUnits = str
TotalAmortizedFee = str
TotalPotentialRISavings = str
TotalRunningHours = str
TotalRunningNormalizedUnits = str
UnrealizedSavings = str
UnusedHours = str
UnusedUnits = str
UtilizationPercentage = str
UtilizationPercentageInUnits = str
Value = str
YearMonthDay = str
ZonedDateTime = str


class AccountScope(StrEnum):
    PAYER = "PAYER"
    LINKED = "LINKED"


class AnalysisStatus(StrEnum):
    SUCCEEDED = "SUCCEEDED"
    PROCESSING = "PROCESSING"
    FAILED = "FAILED"


class AnalysisType(StrEnum):
    MAX_SAVINGS = "MAX_SAVINGS"
    CUSTOM_COMMITMENT = "CUSTOM_COMMITMENT"


class AnomalyFeedbackType(StrEnum):
    YES = "YES"
    NO = "NO"
    PLANNED_ACTIVITY = "PLANNED_ACTIVITY"


class AnomalySubscriptionFrequency(StrEnum):
    DAILY = "DAILY"
    IMMEDIATE = "IMMEDIATE"
    WEEKLY = "WEEKLY"


class ApproximationDimension(StrEnum):
    SERVICE = "SERVICE"
    RESOURCE = "RESOURCE"


class Context(StrEnum):
    COST_AND_USAGE = "COST_AND_USAGE"
    RESERVATIONS = "RESERVATIONS"
    SAVINGS_PLANS = "SAVINGS_PLANS"


class CostAllocationTagBackfillStatus(StrEnum):
    SUCCEEDED = "SUCCEEDED"
    PROCESSING = "PROCESSING"
    FAILED = "FAILED"


class CostAllocationTagStatus(StrEnum):
    Active = "Active"
    Inactive = "Inactive"


class CostAllocationTagType(StrEnum):
    AWSGenerated = "AWSGenerated"
    UserDefined = "UserDefined"


class CostCategoryInheritedValueDimensionName(StrEnum):
    LINKED_ACCOUNT_NAME = "LINKED_ACCOUNT_NAME"
    TAG = "TAG"


class CostCategoryRuleType(StrEnum):
    REGULAR = "REGULAR"
    INHERITED_VALUE = "INHERITED_VALUE"


class CostCategoryRuleVersion(StrEnum):
    CostCategoryExpression_v1 = "CostCategoryExpression.v1"


class CostCategorySplitChargeMethod(StrEnum):
    FIXED = "FIXED"
    PROPORTIONAL = "PROPORTIONAL"
    EVEN = "EVEN"


class CostCategorySplitChargeRuleParameterType(StrEnum):
    ALLOCATION_PERCENTAGES = "ALLOCATION_PERCENTAGES"


class CostCategoryStatus(StrEnum):
    PROCESSING = "PROCESSING"
    APPLIED = "APPLIED"


class CostCategoryStatusComponent(StrEnum):
    COST_EXPLORER = "COST_EXPLORER"


class Dimension(StrEnum):
    AZ = "AZ"
    INSTANCE_TYPE = "INSTANCE_TYPE"
    LINKED_ACCOUNT = "LINKED_ACCOUNT"
    PAYER_ACCOUNT = "PAYER_ACCOUNT"
    LINKED_ACCOUNT_NAME = "LINKED_ACCOUNT_NAME"
    OPERATION = "OPERATION"
    PURCHASE_TYPE = "PURCHASE_TYPE"
    REGION = "REGION"
    SERVICE = "SERVICE"
    SERVICE_CODE = "SERVICE_CODE"
    USAGE_TYPE = "USAGE_TYPE"
    USAGE_TYPE_GROUP = "USAGE_TYPE_GROUP"
    RECORD_TYPE = "RECORD_TYPE"
    OPERATING_SYSTEM = "OPERATING_SYSTEM"
    TENANCY = "TENANCY"
    SCOPE = "SCOPE"
    PLATFORM = "PLATFORM"
    SUBSCRIPTION_ID = "SUBSCRIPTION_ID"
    LEGAL_ENTITY_NAME = "LEGAL_ENTITY_NAME"
    DEPLOYMENT_OPTION = "DEPLOYMENT_OPTION"
    DATABASE_ENGINE = "DATABASE_ENGINE"
    CACHE_ENGINE = "CACHE_ENGINE"
    INSTANCE_TYPE_FAMILY = "INSTANCE_TYPE_FAMILY"
    BILLING_ENTITY = "BILLING_ENTITY"
    RESERVATION_ID = "RESERVATION_ID"
    RESOURCE_ID = "RESOURCE_ID"
    RIGHTSIZING_TYPE = "RIGHTSIZING_TYPE"
    SAVINGS_PLANS_TYPE = "SAVINGS_PLANS_TYPE"
    SAVINGS_PLAN_ARN = "SAVINGS_PLAN_ARN"
    PAYMENT_OPTION = "PAYMENT_OPTION"
    AGREEMENT_END_DATE_TIME_AFTER = "AGREEMENT_END_DATE_TIME_AFTER"
    AGREEMENT_END_DATE_TIME_BEFORE = "AGREEMENT_END_DATE_TIME_BEFORE"
    INVOICING_ENTITY = "INVOICING_ENTITY"
    ANOMALY_TOTAL_IMPACT_ABSOLUTE = "ANOMALY_TOTAL_IMPACT_ABSOLUTE"
    ANOMALY_TOTAL_IMPACT_PERCENTAGE = "ANOMALY_TOTAL_IMPACT_PERCENTAGE"


class ErrorCode(StrEnum):
    NO_USAGE_FOUND = "NO_USAGE_FOUND"
    INTERNAL_FAILURE = "INTERNAL_FAILURE"
    INVALID_SAVINGS_PLANS_TO_ADD = "INVALID_SAVINGS_PLANS_TO_ADD"
    INVALID_SAVINGS_PLANS_TO_EXCLUDE = "INVALID_SAVINGS_PLANS_TO_EXCLUDE"
    INVALID_ACCOUNT_ID = "INVALID_ACCOUNT_ID"


class FindingReasonCode(StrEnum):
    CPU_OVER_PROVISIONED = "CPU_OVER_PROVISIONED"
    CPU_UNDER_PROVISIONED = "CPU_UNDER_PROVISIONED"
    MEMORY_OVER_PROVISIONED = "MEMORY_OVER_PROVISIONED"
    MEMORY_UNDER_PROVISIONED = "MEMORY_UNDER_PROVISIONED"
    EBS_THROUGHPUT_OVER_PROVISIONED = "EBS_THROUGHPUT_OVER_PROVISIONED"
    EBS_THROUGHPUT_UNDER_PROVISIONED = "EBS_THROUGHPUT_UNDER_PROVISIONED"
    EBS_IOPS_OVER_PROVISIONED = "EBS_IOPS_OVER_PROVISIONED"
    EBS_IOPS_UNDER_PROVISIONED = "EBS_IOPS_UNDER_PROVISIONED"
    NETWORK_BANDWIDTH_OVER_PROVISIONED = "NETWORK_BANDWIDTH_OVER_PROVISIONED"
    NETWORK_BANDWIDTH_UNDER_PROVISIONED = "NETWORK_BANDWIDTH_UNDER_PROVISIONED"
    NETWORK_PPS_OVER_PROVISIONED = "NETWORK_PPS_OVER_PROVISIONED"
    NETWORK_PPS_UNDER_PROVISIONED = "NETWORK_PPS_UNDER_PROVISIONED"
    DISK_IOPS_OVER_PROVISIONED = "DISK_IOPS_OVER_PROVISIONED"
    DISK_IOPS_UNDER_PROVISIONED = "DISK_IOPS_UNDER_PROVISIONED"
    DISK_THROUGHPUT_OVER_PROVISIONED = "DISK_THROUGHPUT_OVER_PROVISIONED"
    DISK_THROUGHPUT_UNDER_PROVISIONED = "DISK_THROUGHPUT_UNDER_PROVISIONED"


class GenerationStatus(StrEnum):
    SUCCEEDED = "SUCCEEDED"
    PROCESSING = "PROCESSING"
    FAILED = "FAILED"


class Granularity(StrEnum):
    DAILY = "DAILY"
    MONTHLY = "MONTHLY"
    HOURLY = "HOURLY"


class GroupDefinitionType(StrEnum):
    DIMENSION = "DIMENSION"
    TAG = "TAG"
    COST_CATEGORY = "COST_CATEGORY"


class LookbackPeriodInDays(StrEnum):
    SEVEN_DAYS = "SEVEN_DAYS"
    THIRTY_DAYS = "THIRTY_DAYS"
    SIXTY_DAYS = "SIXTY_DAYS"


class MatchOption(StrEnum):
    EQUALS = "EQUALS"
    ABSENT = "ABSENT"
    STARTS_WITH = "STARTS_WITH"
    ENDS_WITH = "ENDS_WITH"
    CONTAINS = "CONTAINS"
    CASE_SENSITIVE = "CASE_SENSITIVE"
    CASE_INSENSITIVE = "CASE_INSENSITIVE"
    GREATER_THAN_OR_EQUAL = "GREATER_THAN_OR_EQUAL"


class Metric(StrEnum):
    BLENDED_COST = "BLENDED_COST"
    UNBLENDED_COST = "UNBLENDED_COST"
    AMORTIZED_COST = "AMORTIZED_COST"
    NET_UNBLENDED_COST = "NET_UNBLENDED_COST"
    NET_AMORTIZED_COST = "NET_AMORTIZED_COST"
    USAGE_QUANTITY = "USAGE_QUANTITY"
    NORMALIZED_USAGE_AMOUNT = "NORMALIZED_USAGE_AMOUNT"


class MonitorDimension(StrEnum):
    SERVICE = "SERVICE"
    LINKED_ACCOUNT = "LINKED_ACCOUNT"
    TAG = "TAG"
    COST_CATEGORY = "COST_CATEGORY"


class MonitorType(StrEnum):
    DIMENSIONAL = "DIMENSIONAL"
    CUSTOM = "CUSTOM"


class NumericOperator(StrEnum):
    EQUAL = "EQUAL"
    GREATER_THAN_OR_EQUAL = "GREATER_THAN_OR_EQUAL"
    LESS_THAN_OR_EQUAL = "LESS_THAN_OR_EQUAL"
    GREATER_THAN = "GREATER_THAN"
    LESS_THAN = "LESS_THAN"
    BETWEEN = "BETWEEN"


class OfferingClass(StrEnum):
    STANDARD = "STANDARD"
    CONVERTIBLE = "CONVERTIBLE"


class PaymentOption(StrEnum):
    NO_UPFRONT = "NO_UPFRONT"
    PARTIAL_UPFRONT = "PARTIAL_UPFRONT"
    ALL_UPFRONT = "ALL_UPFRONT"
    LIGHT_UTILIZATION = "LIGHT_UTILIZATION"
    MEDIUM_UTILIZATION = "MEDIUM_UTILIZATION"
    HEAVY_UTILIZATION = "HEAVY_UTILIZATION"


class PlatformDifference(StrEnum):
    HYPERVISOR = "HYPERVISOR"
    NETWORK_INTERFACE = "NETWORK_INTERFACE"
    STORAGE_INTERFACE = "STORAGE_INTERFACE"
    INSTANCE_STORE_AVAILABILITY = "INSTANCE_STORE_AVAILABILITY"
    VIRTUALIZATION_TYPE = "VIRTUALIZATION_TYPE"


class RecommendationTarget(StrEnum):
    SAME_INSTANCE_FAMILY = "SAME_INSTANCE_FAMILY"
    CROSS_INSTANCE_FAMILY = "CROSS_INSTANCE_FAMILY"


class RightsizingType(StrEnum):
    TERMINATE = "TERMINATE"
    MODIFY = "MODIFY"


class SavingsPlansDataType(StrEnum):
    ATTRIBUTES = "ATTRIBUTES"
    UTILIZATION = "UTILIZATION"
    AMORTIZED_COMMITMENT = "AMORTIZED_COMMITMENT"
    SAVINGS = "SAVINGS"


class SortOrder(StrEnum):
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"


class SubscriberStatus(StrEnum):
    CONFIRMED = "CONFIRMED"
    DECLINED = "DECLINED"


class SubscriberType(StrEnum):
    EMAIL = "EMAIL"
    SNS = "SNS"


class SupportedSavingsPlansType(StrEnum):
    COMPUTE_SP = "COMPUTE_SP"
    EC2_INSTANCE_SP = "EC2_INSTANCE_SP"
    SAGEMAKER_SP = "SAGEMAKER_SP"
    DATABASE_SP = "DATABASE_SP"


class TermInYears(StrEnum):
    ONE_YEAR = "ONE_YEAR"
    THREE_YEARS = "THREE_YEARS"


class AnalysisNotFoundException(ServiceException):
    """The requested analysis can't be found."""

    code: str = "AnalysisNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class BackfillLimitExceededException(ServiceException):
    """A request to backfill is already in progress. Once the previous request
    is complete, you can create another request.
    """

    code: str = "BackfillLimitExceededException"
    sender_fault: bool = False
    status_code: int = 400


class BillExpirationException(ServiceException):
    """The requested report expired. Update the date interval and try again."""

    code: str = "BillExpirationException"
    sender_fault: bool = False
    status_code: int = 400


class BillingViewHealthStatusException(ServiceException):
    """The billing view status must be ``HEALTHY`` to perform this action. Try
    again when the status is ``HEALTHY``.
    """

    code: str = "BillingViewHealthStatusException"
    sender_fault: bool = False
    status_code: int = 400


class DataUnavailableException(ServiceException):
    """The requested data is unavailable."""

    code: str = "DataUnavailableException"
    sender_fault: bool = False
    status_code: int = 400


class GenerationExistsException(ServiceException):
    """A request to generate a recommendation or analysis is already in
    progress.
    """

    code: str = "GenerationExistsException"
    sender_fault: bool = False
    status_code: int = 400


class InvalidNextTokenException(ServiceException):
    """The pagination token is invalid. Try again without a pagination token."""

    code: str = "InvalidNextTokenException"
    sender_fault: bool = False
    status_code: int = 400


class LimitExceededException(ServiceException):
    """You made too many calls in a short period of time. Try again later."""

    code: str = "LimitExceededException"
    sender_fault: bool = False
    status_code: int = 400


class RequestChangedException(ServiceException):
    """Your request parameters changed between pages. Try again with the old
    parameters or without a pagination token.
    """

    code: str = "RequestChangedException"
    sender_fault: bool = False
    status_code: int = 400


class ResourceNotFoundException(ServiceException):
    """The specified ARN in the request doesn't exist."""

    code: str = "ResourceNotFoundException"
    sender_fault: bool = False
    status_code: int = 400
    ResourceName: Arn | None


class ServiceQuotaExceededException(ServiceException):
    """You've reached the limit on the number of resources you can create, or
    exceeded the size of an individual resource.
    """

    code: str = "ServiceQuotaExceededException"
    sender_fault: bool = False
    status_code: int = 400


class TooManyTagsException(ServiceException):
    """Can occur if you specify a number of tags for a resource greater than
    the maximum 50 user tags per resource.
    """

    code: str = "TooManyTagsException"
    sender_fault: bool = False
    status_code: int = 400
    ResourceName: Arn | None


class UnknownMonitorException(ServiceException):
    """The cost anomaly monitor does not exist for the account."""

    code: str = "UnknownMonitorException"
    sender_fault: bool = False
    status_code: int = 400


class UnknownSubscriptionException(ServiceException):
    """The cost anomaly subscription does not exist for the account."""

    code: str = "UnknownSubscriptionException"
    sender_fault: bool = False
    status_code: int = 400


class UnresolvableUsageUnitException(ServiceException):
    """Cost Explorer was unable to identify the usage unit. Provide
    ``UsageType/UsageTypeGroup`` filter selections that contain matching
    units, for example: ``hours``.
    """

    code: str = "UnresolvableUsageUnitException"
    sender_fault: bool = False
    status_code: int = 400


class RecommendationDetailHourlyMetrics(TypedDict, total=False):
    """Contains the hourly metrics for the given recommendation over the
    lookback period.
    """

    StartTime: ZonedDateTime | None
    EstimatedOnDemandCost: GenericString | None
    CurrentCoverage: GenericString | None
    EstimatedCoverage: GenericString | None
    EstimatedNewCommitmentUtilization: GenericString | None


MetricsOverLookbackPeriod = list[RecommendationDetailHourlyMetrics]


class SavingsPlansPurchaseAnalysisDetails(TypedDict, total=False):
    """Details about the Savings Plans purchase analysis."""

    CurrencyCode: GenericString | None
    LookbackPeriodInHours: GenericString | None
    CurrentAverageCoverage: GenericString | None
    CurrentAverageHourlyOnDemandSpend: GenericString | None
    CurrentMaximumHourlyOnDemandSpend: GenericString | None
    CurrentMinimumHourlyOnDemandSpend: GenericString | None
    CurrentOnDemandSpend: GenericString | None
    ExistingHourlyCommitment: GenericString | None
    HourlyCommitmentToPurchase: GenericString | None
    EstimatedAverageCoverage: GenericString | None
    EstimatedAverageUtilization: GenericString | None
    EstimatedMonthlySavingsAmount: GenericString | None
    EstimatedOnDemandCost: GenericString | None
    EstimatedOnDemandCostWithCurrentCommitment: GenericString | None
    EstimatedROI: GenericString | None
    EstimatedSavingsAmount: GenericString | None
    EstimatedSavingsPercentage: GenericString | None
    EstimatedCommitmentCost: GenericString | None
    LatestUsageTimestamp: GenericString | None
    UpfrontCost: GenericString | None
    AdditionalMetadata: GenericString | None
    MetricsOverLookbackPeriod: MetricsOverLookbackPeriod | None


class AnalysisDetails(TypedDict, total=False):
    """Details about the analysis."""

    SavingsPlansPurchaseAnalysisDetails: SavingsPlansPurchaseAnalysisDetails | None


AnalysisIds = list[AnalysisId]


class DateInterval(TypedDict, total=False):
    """The time period of the request."""

    Start: YearMonthDay
    End: YearMonthDay


SavingsPlansToExclude = list[SavingsPlansId]


class SavingsPlans(TypedDict, total=False):
    """The Savings Plans commitment details."""

    PaymentOption: PaymentOption | None
    SavingsPlansType: SupportedSavingsPlansType | None
    Region: GenericString | None
    InstanceFamily: GenericString | None
    TermInYears: TermInYears | None
    SavingsPlansCommitment: SavingsPlansCommitment | None
    OfferingId: GenericString | None


SavingsPlansToAdd = list[SavingsPlans]


class SavingsPlansPurchaseAnalysisConfiguration(TypedDict, total=False):
    """The configuration for the Savings Plans purchase analysis."""

    AccountScope: AccountScope | None
    AccountId: AccountId | None
    AnalysisType: AnalysisType
    SavingsPlansToAdd: SavingsPlansToAdd
    SavingsPlansToExclude: SavingsPlansToExclude | None
    LookBackTimePeriod: DateInterval


class CommitmentPurchaseAnalysisConfiguration(TypedDict, total=False):
    """The configuration for the commitment purchase analysis."""

    SavingsPlansPurchaseAnalysisConfiguration: SavingsPlansPurchaseAnalysisConfiguration | None


class AnalysisSummary(TypedDict, total=False):
    """A summary of the analysis."""

    EstimatedCompletionTime: ZonedDateTime | None
    AnalysisCompletionTime: ZonedDateTime | None
    AnalysisStartedTime: ZonedDateTime | None
    AnalysisStatus: AnalysisStatus | None
    ErrorCode: ErrorCode | None
    AnalysisId: AnalysisId | None
    CommitmentPurchaseAnalysisConfiguration: CommitmentPurchaseAnalysisConfiguration | None


AnalysisSummaryList = list[AnalysisSummary]


class Impact(TypedDict, total=False):
    """The dollar value of the anomaly."""

    MaxImpact: GenericDouble
    TotalImpact: GenericDouble | None
    TotalActualSpend: NullableNonNegativeDouble | None
    TotalExpectedSpend: NullableNonNegativeDouble | None
    TotalImpactPercentage: NullableNonNegativeDouble | None


class AnomalyScore(TypedDict, total=False):
    """Quantifies the anomaly. The higher score means that it's more anomalous."""

    MaxScore: GenericDouble
    CurrentScore: GenericDouble


class RootCauseImpact(TypedDict, total=False):
    """The dollar value of the root cause."""

    Contribution: GenericDouble


class RootCause(TypedDict, total=False):
    """The combination of Amazon Web Services service, linked account, linked
    account name, Region, and usage type where a cost anomaly is observed,
    along with the dollar and percentage amount of the anomaly impact. The
    linked account name will only be available when the account name can be
    identified.
    """

    Service: GenericString | None
    Region: GenericString | None
    LinkedAccount: GenericString | None
    LinkedAccountName: GenericString | None
    UsageType: GenericString | None
    Impact: RootCauseImpact | None


RootCauses = list[RootCause]


class Anomaly(TypedDict, total=False):
    """An unusual cost pattern. This consists of the detailed metadata and the
    current status of the anomaly object.
    """

    AnomalyId: GenericString
    AnomalyStartDate: YearMonthDay | None
    AnomalyEndDate: YearMonthDay | None
    DimensionValue: GenericString | None
    RootCauses: RootCauses | None
    AnomalyScore: AnomalyScore
    Impact: Impact
    MonitorArn: GenericString
    Feedback: AnomalyFeedbackType | None


Anomalies = list[Anomaly]


class AnomalyDateInterval(TypedDict, total=False):
    """The time period for an anomaly."""

    StartDate: YearMonthDay
    EndDate: YearMonthDay | None


MatchOptions = list[MatchOption]
Values = list[Value]


class CostCategoryValues(TypedDict, total=False):
    """The Cost Categories values used for filtering the costs.

    If ``Values`` and ``Key`` are not specified, the ``ABSENT``
    ``MatchOption`` is applied to all Cost Categories. That is, it filters
    on resources that aren't mapped to any Cost Categories.

    If ``Values`` is provided and ``Key`` isn't specified, the ``ABSENT``
    ``MatchOption`` is applied to the Cost Categories ``Key`` only. That is,
    it filters on resources without the given Cost Categories key.
    """

    Key: CostCategoryName | None
    Values: Values | None
    MatchOptions: MatchOptions | None


class TagValues(TypedDict, total=False):
    """The values that are available for a tag.

    If ``Values`` and ``Key`` aren't specified, the ``ABSENT``
    ``MatchOption`` is applied to all tags. That is, it's filtered on
    resources with no tags.

    If ``Key`` is provided and ``Values`` isn't specified, the ``ABSENT``
    ``MatchOption`` is applied to the tag ``Key`` only. That is, it's
    filtered on resources without the given tag key.
    """

    Key: TagKey | None
    Values: Values | None
    MatchOptions: MatchOptions | None


class DimensionValues(TypedDict, total=False):
    """The metadata that you can use to filter and group your results. You can
    use ``GetDimensionValues`` to find specific values.
    """

    Key: Dimension | None
    Values: Values | None
    MatchOptions: MatchOptions | None


class Expression(TypedDict, total=False):
    """Use ``Expression`` to filter in various Cost Explorer APIs.

    Not all ``Expression`` types are supported in each API. Refer to the
    documentation for each specific API to see what is supported.

    There are two patterns:

    -  Simple dimension values.

       -  There are three types of simple dimension values:
          ``CostCategories``, ``Tags``, and ``Dimensions``.

          -  Specify the ``CostCategories`` field to define a filter that
             acts on Cost Categories.

          -  Specify the ``Tags`` field to define a filter that acts on Cost
             Allocation Tags.

          -  Specify the ``Dimensions`` field to define a filter that acts
             on the
             ```DimensionValues`` <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_DimensionValues.html>`__
             .

       -  For each filter type, you can set the dimension name and values
          for the filters that you plan to use.

          -  For example, you can filter for
             ``REGION==us-east-1 OR REGION==us-west-1``. For
             ``GetRightsizingRecommendation``, the Region is a full name
             (for example, ``REGION==US East (N. Virginia)``.

          -  The corresponding ``Expression`` for this example is as
             follows:
             ``{ "Dimensions": { "Key": "REGION", "Values": [ "us-east-1", "us-west-1" ] } }``

          -  As shown in the previous example, lists of dimension values are
             combined with ``OR`` when applying the filter.

       -  You can also set different match options to further control how
          the filter behaves. Not all APIs support match options. Refer to
          the documentation for each specific API to see what is supported.

          -  For example, you can filter for linked account names that start
             with "a".

          -  The corresponding ``Expression`` for this example is as
             follows:
             ``{ "Dimensions": { "Key": "LINKED_ACCOUNT_NAME", "MatchOptions": [ "STARTS_WITH" ], "Values": [ "a" ] } }``

    -  Compound ``Expression`` types with logical operations.

       -  You can use multiple ``Expression`` types and the logical
          operators ``AND/OR/NOT`` to create a list of one or more
          ``Expression`` objects. By doing this, you can filter by more
          advanced options.

       -  For example, you can filter by
          ``((REGION == us-east-1 OR REGION == us-west-1) OR (TAG.Type == Type1)) AND (USAGE_TYPE != DataTransfer)``.

       -  The corresponding ``Expression`` for this example is as follows:
          ``{ "And": [ {"Or": [ {"Dimensions": { "Key": "REGION", "Values": [ "us-east-1", "us-west-1" ] }}, {"Tags": { "Key": "TagName", "Values": ["Value1"] } } ]}, {"Not": {"Dimensions": { "Key": "USAGE_TYPE", "Values": ["DataTransfer"] }}} ] }``

       Because each ``Expression`` can have only one operator, the service
       returns an error if more than one is specified. The following example
       shows an ``Expression`` object that creates an error:
       ``{ "And": [ ... ], "Dimensions": { "Key": "USAGE_TYPE", "Values": [ "DataTransfer" ] } }``

       The following is an example of the corresponding error message:
       ``"Expression has more than one roots. Only one root operator is allowed for each expression: And, Or, Not, Dimensions, Tags, CostCategories"``

    For the ``GetRightsizingRecommendation`` action, a combination of OR and
    NOT isn't supported. OR isn't supported between different dimensions, or
    dimensions and tags. NOT operators aren't supported. Dimensions are also
    limited to ``LINKED_ACCOUNT``, ``REGION``, or ``RIGHTSIZING_TYPE``.

    For the ``GetReservationPurchaseRecommendation`` action, only NOT is
    supported. AND and OR aren't supported. Dimensions are limited to
    ``LINKED_ACCOUNT``.
    """

    Or: "Expressions | None"
    And: "Expressions | None"
    Not: "Expression | None"
    Dimensions: "DimensionValues | None"
    Tags: "TagValues | None"
    CostCategories: "CostCategoryValues | None"


Expressions = list[Expression]


class AnomalyMonitor(TypedDict, total=False):
    """This object continuously inspects your account's cost data for
    anomalies. It's based on ``MonitorType`` and ``MonitorSpecification``.
    The content consists of detailed metadata and the current status of the
    monitor object.
    """

    MonitorArn: GenericString | None
    MonitorName: GenericString
    CreationDate: YearMonthDay | None
    LastUpdatedDate: YearMonthDay | None
    LastEvaluatedDate: YearMonthDay | None
    MonitorType: MonitorType
    MonitorDimension: MonitorDimension | None
    MonitorSpecification: Expression | None
    DimensionalValueCount: NonNegativeInteger | None


AnomalyMonitors = list[AnomalyMonitor]


class Subscriber(TypedDict, total=False):
    """The recipient of ``AnomalySubscription`` notifications."""

    Address: SubscriberAddress | None
    Type: SubscriberType | None
    Status: SubscriberStatus | None


Subscribers = list[Subscriber]
MonitorArnList = list[Arn]


class AnomalySubscription(TypedDict, total=False):
    """An ``AnomalySubscription`` resource (also referred to as an alert
    subscription) sends notifications about specific anomalies that meet an
    alerting criteria defined by you.

    You can specify the frequency of the alerts and the subscribers to
    notify.

    Anomaly subscriptions can be associated with one or more
    ```AnomalyMonitor`` <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_AnomalyMonitor.html>`__
    resources, and they only send notifications about anomalies detected by
    those associated monitors. You can also configure a threshold to further
    control which anomalies are included in the notifications.

    Anomalies that don’t exceed the chosen threshold and therefore don’t
    trigger notifications from an anomaly subscription will still be
    available on the console and from the
    ```GetAnomalies`` <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetAnomalies.html>`__
    API.
    """

    SubscriptionArn: GenericString | None
    AccountId: GenericString | None
    MonitorArnList: MonitorArnList
    Subscribers: Subscribers
    Threshold: NullableNonNegativeDouble | None
    Frequency: AnomalySubscriptionFrequency
    SubscriptionName: GenericString
    ThresholdExpression: Expression | None


AnomalySubscriptions = list[AnomalySubscription]
NonNegativeLong = int
ApproximateUsageRecordsPerService = dict[GenericString, NonNegativeLong]
Attributes = dict[AttributeType, AttributeValue]


class ComparisonMetricValue(TypedDict, total=False):
    """Contains cost or usage metric values for comparing two time periods.
    Each value includes amounts for the baseline and comparison time
    periods, their difference, and the unit of measurement.
    """

    BaselineTimePeriodAmount: GenericString | None
    ComparisonTimePeriodAmount: GenericString | None
    Difference: GenericString | None
    Unit: GenericString | None


ComparisonMetrics = dict[MetricName, ComparisonMetricValue]


class CostAllocationTag(TypedDict, total=False):
    """The cost allocation tag structure. This includes detailed metadata for
    the ``CostAllocationTag`` object.
    """

    TagKey: TagKey
    Type: CostAllocationTagType
    Status: CostAllocationTagStatus
    LastUpdatedDate: ZonedDateTime | None
    LastUsedDate: ZonedDateTime | None


class CostAllocationTagBackfillRequest(TypedDict, total=False):
    """The cost allocation tag backfill request structure that contains
    metadata and details of a certain backfill.
    """

    BackfillFrom: ZonedDateTime | None
    RequestedAt: ZonedDateTime | None
    CompletedAt: ZonedDateTime | None
    BackfillStatus: CostAllocationTagBackfillStatus | None
    LastUpdatedAt: ZonedDateTime | None


CostAllocationTagBackfillRequestList = list[CostAllocationTagBackfillRequest]
CostAllocationTagKeyList = list[TagKey]
CostAllocationTagList = list[CostAllocationTag]


class CostAllocationTagStatusEntry(TypedDict, total=False):
    """The cost allocation tag status. The status of a key can either be active
    or inactive.
    """

    TagKey: TagKey
    Status: CostAllocationTagStatus


CostAllocationTagStatusList = list[CostAllocationTagStatusEntry]


class CostAndUsageComparison(TypedDict, total=False):
    """Represents a comparison of cost and usage metrics between two time
    periods.
    """

    CostAndUsageSelector: Expression | None
    Metrics: ComparisonMetrics | None


CostAndUsageComparisons = list[CostAndUsageComparison]


class CostCategoryProcessingStatus(TypedDict, total=False):
    """The list of processing statuses for Cost Management products for a
    specific cost category.
    """

    Component: CostCategoryStatusComponent | None
    Status: CostCategoryStatus | None


CostCategoryProcessingStatusList = list[CostCategoryProcessingStatus]
CostCategorySplitChargeRuleParameterValuesList = list[GenericString]


class CostCategorySplitChargeRuleParameter(TypedDict, total=False):
    """The parameters for a split charge method."""

    Type: CostCategorySplitChargeRuleParameterType
    Values: CostCategorySplitChargeRuleParameterValuesList


CostCategorySplitChargeRuleParametersList = list[CostCategorySplitChargeRuleParameter]
CostCategorySplitChargeRuleTargetsList = list[GenericString]


class CostCategorySplitChargeRule(TypedDict, total=False):
    """Use the split charge rule to split the cost of one Cost Category value
    across several other target values.
    """

    Source: GenericString
    Targets: CostCategorySplitChargeRuleTargetsList
    Method: CostCategorySplitChargeMethod
    Parameters: CostCategorySplitChargeRuleParametersList | None


CostCategorySplitChargeRulesList = list[CostCategorySplitChargeRule]


class CostCategoryInheritedValueDimension(TypedDict, total=False):
    """When you create or update a cost category, you can define the
    ``CostCategoryRule`` rule type as ``INHERITED_VALUE``. This rule type
    adds the flexibility to define a rule that dynamically inherits the cost
    category value from the dimension value that's defined by
    ``CostCategoryInheritedValueDimension``. For example, suppose that you
    want to dynamically group costs that are based on the value of a
    specific tag key. First, choose an inherited value rule type, and then
    choose the tag dimension and specify the tag key to use.
    """

    DimensionName: CostCategoryInheritedValueDimensionName | None
    DimensionKey: GenericString | None


class CostCategoryRule(TypedDict, total=False):
    """Rules are processed in order. If there are multiple rules that match the
    line item, then the first rule to match is used to determine that Cost
    Category value.
    """

    Value: CostCategoryValue | None
    Rule: Expression | None
    InheritedValue: CostCategoryInheritedValueDimension | None
    Type: CostCategoryRuleType | None


CostCategoryRulesList = list[CostCategoryRule]


class CostCategory(TypedDict, total=False):
    """The structure of Cost Categories. This includes detailed metadata and
    the set of rules for the ``CostCategory`` object.
    """

    CostCategoryArn: Arn
    EffectiveStart: ZonedDateTime
    EffectiveEnd: ZonedDateTime | None
    Name: CostCategoryName
    RuleVersion: CostCategoryRuleVersion
    Rules: CostCategoryRulesList
    SplitChargeRules: CostCategorySplitChargeRulesList | None
    ProcessingStatus: CostCategoryProcessingStatusList | None
    DefaultValue: CostCategoryValue | None


CostCategoryNamesList = list[CostCategoryName]
CostCategoryValuesList = list[CostCategoryValue]


class CostCategoryReference(TypedDict, total=False):
    """A reference to a Cost Category containing only enough information to
    identify the Cost Category.

    You can use this information to retrieve the full Cost Category
    information using ``DescribeCostCategory``.
    """

    CostCategoryArn: Arn | None
    Name: CostCategoryName | None
    EffectiveStart: ZonedDateTime | None
    EffectiveEnd: ZonedDateTime | None
    NumberOfRules: NonNegativeInteger | None
    ProcessingStatus: CostCategoryProcessingStatusList | None
    Values: CostCategoryValuesList | None
    DefaultValue: CostCategoryValue | None


CostCategoryReferencesList = list[CostCategoryReference]


class CostDriver(TypedDict, total=False):
    """Represents factors that contribute to cost variations between the
    baseline and comparison time periods, including the type of driver, an
    identifier of the driver, and associated metrics.
    """

    Type: GenericString | None
    Name: GenericString | None
    Metrics: ComparisonMetrics | None


CostDrivers = list[CostDriver]


class CostComparisonDriver(TypedDict, total=False):
    """Represents a collection of cost drivers and their associated metrics for
    cost comparison analysis.
    """

    CostSelector: Expression | None
    Metrics: ComparisonMetrics | None
    CostDrivers: CostDrivers | None


CostComparisonDrivers = list[CostComparisonDriver]


class CoverageCost(TypedDict, total=False):
    """How much it costs to run an instance."""

    OnDemandCost: OnDemandCost | None


class CoverageNormalizedUnits(TypedDict, total=False):
    """The amount of instance usage, in normalized units. You can use
    normalized units to see your EC2 usage for multiple sizes of instances
    in a uniform way. For example, suppose that you run an xlarge instance
    and a 2xlarge instance. If you run both instances for the same amount of
    time, the 2xlarge instance uses twice as much of your reservation as the
    xlarge instance, even though both instances show only one instance-hour.
    When you use normalized units instead of instance-hours, the xlarge
    instance used 8 normalized units, and the 2xlarge instance used 16
    normalized units.

    For more information, see `Modifying Reserved
    Instances <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ri-modifying.html>`__
    in the *Amazon Elastic Compute Cloud User Guide for Linux Instances*.
    """

    OnDemandNormalizedUnits: OnDemandNormalizedUnits | None
    ReservedNormalizedUnits: ReservedNormalizedUnits | None
    TotalRunningNormalizedUnits: TotalRunningNormalizedUnits | None
    CoverageNormalizedUnitsPercentage: CoverageNormalizedUnitsPercentage | None


class CoverageHours(TypedDict, total=False):
    """How long a running instance either used a reservation or was On-Demand."""

    OnDemandHours: OnDemandHours | None
    ReservedHours: ReservedHours | None
    TotalRunningHours: TotalRunningHours | None
    CoverageHoursPercentage: CoverageHoursPercentage | None


class Coverage(TypedDict, total=False):
    """The amount of instance usage that a reservation covered."""

    CoverageHours: CoverageHours | None
    CoverageNormalizedUnits: CoverageNormalizedUnits | None
    CoverageCost: CoverageCost | None


class ReservationCoverageGroup(TypedDict, total=False):
    """A group of reservations that share a set of attributes."""

    Attributes: Attributes | None
    Coverage: Coverage | None


ReservationCoverageGroups = list[ReservationCoverageGroup]


class CoverageByTime(TypedDict, total=False):
    """Reservation coverage for a specified period, in hours."""

    TimePeriod: DateInterval | None
    Groups: ReservationCoverageGroups | None
    Total: Coverage | None


CoveragesByTime = list[CoverageByTime]


class ResourceTag(TypedDict, total=False):
    """The tag structure that contains a tag key and value.

    Tagging is supported only for the following Cost Explorer resource
    types:
    ```AnomalyMonitor`` <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_AnomalyMonitor.html>`__
    ,
    ```AnomalySubscription`` <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_AnomalySubscription.html>`__
    ,
    ```CostCategory`` <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_CostCategory.html>`__
    .
    """

    Key: ResourceTagKey
    Value: ResourceTagValue


ResourceTagList = list[ResourceTag]


class CreateAnomalyMonitorRequest(ServiceRequest):
    AnomalyMonitor: AnomalyMonitor
    ResourceTags: ResourceTagList | None


class CreateAnomalyMonitorResponse(TypedDict, total=False):
    MonitorArn: GenericString


class CreateAnomalySubscriptionRequest(ServiceRequest):
    AnomalySubscription: AnomalySubscription
    ResourceTags: ResourceTagList | None


class CreateAnomalySubscriptionResponse(TypedDict, total=False):
    SubscriptionArn: GenericString


class CreateCostCategoryDefinitionRequest(ServiceRequest):
    Name: CostCategoryName
    EffectiveStart: ZonedDateTime | None
    RuleVersion: CostCategoryRuleVersion
    Rules: CostCategoryRulesList
    DefaultValue: CostCategoryValue | None
    SplitChargeRules: CostCategorySplitChargeRulesList | None
    ResourceTags: ResourceTagList | None


class CreateCostCategoryDefinitionResponse(TypedDict, total=False):
    CostCategoryArn: Arn | None
    EffectiveStart: ZonedDateTime | None


class NetworkResourceUtilization(TypedDict, total=False):
    """The network field that contains a list of network metrics that are
    associated with the current instance.
    """

    NetworkInBytesPerSecond: GenericString | None
    NetworkOutBytesPerSecond: GenericString | None
    NetworkPacketsInPerSecond: GenericString | None
    NetworkPacketsOutPerSecond: GenericString | None


class DiskResourceUtilization(TypedDict, total=False):
    """The field that contains a list of disk (local storage) metrics that are
    associated with the current instance.
    """

    DiskReadOpsPerSecond: GenericString | None
    DiskWriteOpsPerSecond: GenericString | None
    DiskReadBytesPerSecond: GenericString | None
    DiskWriteBytesPerSecond: GenericString | None


class EBSResourceUtilization(TypedDict, total=False):
    """The EBS field that contains a list of EBS metrics that are associated
    with the current instance.
    """

    EbsReadOpsPerSecond: GenericString | None
    EbsWriteOpsPerSecond: GenericString | None
    EbsReadBytesPerSecond: GenericString | None
    EbsWriteBytesPerSecond: GenericString | None


class EC2ResourceUtilization(TypedDict, total=False):
    """Utilization metrics for the instance."""

    MaxCpuUtilizationPercentage: GenericString | None
    MaxMemoryUtilizationPercentage: GenericString | None
    MaxStorageUtilizationPercentage: GenericString | None
    EBSResourceUtilization: EBSResourceUtilization | None
    DiskResourceUtilization: DiskResourceUtilization | None
    NetworkResourceUtilization: NetworkResourceUtilization | None


class ResourceUtilization(TypedDict, total=False):
    """Resource utilization of current resource."""

    EC2ResourceUtilization: EC2ResourceUtilization | None


class EC2ResourceDetails(TypedDict, total=False):
    """Details on the Amazon EC2 Resource."""

    HourlyOnDemandRate: GenericString | None
    InstanceType: GenericString | None
    Platform: GenericString | None
    Region: GenericString | None
    Sku: GenericString | None
    Memory: GenericString | None
    NetworkPerformance: GenericString | None
    Storage: GenericString | None
    Vcpu: GenericString | None


class ResourceDetails(TypedDict, total=False):
    """Details for the resource."""

    EC2ResourceDetails: EC2ResourceDetails | None


TagValuesList = list[TagValues]


class CurrentInstance(TypedDict, total=False):
    """Context about the current instance."""

    ResourceId: GenericString | None
    InstanceName: GenericString | None
    Tags: TagValuesList | None
    ResourceDetails: ResourceDetails | None
    ResourceUtilization: ResourceUtilization | None
    ReservationCoveredHoursInLookbackPeriod: GenericString | None
    SavingsPlansCoveredHoursInLookbackPeriod: GenericString | None
    OnDemandHoursInLookbackPeriod: GenericString | None
    TotalRunningHoursInLookbackPeriod: GenericString | None
    MonthlyCost: GenericString | None
    CurrencyCode: GenericString | None


class DeleteAnomalyMonitorRequest(ServiceRequest):
    MonitorArn: GenericString


class DeleteAnomalyMonitorResponse(TypedDict, total=False):
    pass


class DeleteAnomalySubscriptionRequest(ServiceRequest):
    SubscriptionArn: GenericString


class DeleteAnomalySubscriptionResponse(TypedDict, total=False):
    pass


class DeleteCostCategoryDefinitionRequest(ServiceRequest):
    CostCategoryArn: Arn


class DeleteCostCategoryDefinitionResponse(TypedDict, total=False):
    CostCategoryArn: Arn | None
    EffectiveEnd: ZonedDateTime | None


class DescribeCostCategoryDefinitionRequest(ServiceRequest):
    CostCategoryArn: Arn
    EffectiveOn: ZonedDateTime | None


class DescribeCostCategoryDefinitionResponse(TypedDict, total=False):
    CostCategory: CostCategory | None


class DimensionValuesWithAttributes(TypedDict, total=False):
    """The metadata of a specific type that you can use to filter and group
    your results. You can use ``GetDimensionValues`` to find specific
    values.
    """

    Value: Value | None
    Attributes: Attributes | None


DimensionValuesWithAttributesList = list[DimensionValuesWithAttributes]


class DynamoDBCapacityDetails(TypedDict, total=False):
    """The DynamoDB reservations that Amazon Web Services recommends that you
    purchase.
    """

    CapacityUnits: GenericString | None
    Region: GenericString | None


class EC2InstanceDetails(TypedDict, total=False):
    """Details about the Amazon EC2 reservations that Amazon Web Services
    recommends that you purchase.
    """

    Family: GenericString | None
    InstanceType: GenericString | None
    Region: GenericString | None
    AvailabilityZone: GenericString | None
    Platform: GenericString | None
    Tenancy: GenericString | None
    CurrentGeneration: GenericBoolean | None
    SizeFlexEligible: GenericBoolean | None


class EC2Specification(TypedDict, total=False):
    """The Amazon EC2 hardware specifications that you want Amazon Web Services
    to provide recommendations for.
    """

    OfferingClass: OfferingClass | None


class ESInstanceDetails(TypedDict, total=False):
    """Details about the Amazon OpenSearch Service reservations that Amazon Web
    Services recommends that you purchase.
    """

    InstanceClass: GenericString | None
    InstanceSize: GenericString | None
    Region: GenericString | None
    CurrentGeneration: GenericBoolean | None
    SizeFlexEligible: GenericBoolean | None


class ElastiCacheInstanceDetails(TypedDict, total=False):
    """Details about the Amazon ElastiCache reservations that Amazon Web
    Services recommends that you purchase.
    """

    Family: GenericString | None
    NodeType: GenericString | None
    Region: GenericString | None
    ProductDescription: GenericString | None
    CurrentGeneration: GenericBoolean | None
    SizeFlexEligible: GenericBoolean | None


FindingReasonCodes = list[FindingReasonCode]


class ForecastResult(TypedDict, total=False):
    """The forecast that's created for your query."""

    TimePeriod: DateInterval | None
    MeanValue: GenericString | None
    PredictionIntervalLowerBound: GenericString | None
    PredictionIntervalUpperBound: GenericString | None


ForecastResultsByTime = list[ForecastResult]


class GenerationSummary(TypedDict, total=False):
    """The summary of the Savings Plans recommendation generation."""

    RecommendationId: RecommendationId | None
    GenerationStatus: GenerationStatus | None
    GenerationStartedTime: ZonedDateTime | None
    GenerationCompletionTime: ZonedDateTime | None
    EstimatedCompletionTime: ZonedDateTime | None


GenerationSummaryList = list[GenerationSummary]


class TotalImpactFilter(TypedDict, total=False):
    """Filters cost anomalies based on the total impact."""

    NumericOperator: NumericOperator
    StartValue: GenericDouble
    EndValue: GenericDouble | None


class GetAnomaliesRequest(ServiceRequest):
    MonitorArn: GenericString | None
    DateInterval: AnomalyDateInterval
    Feedback: AnomalyFeedbackType | None
    TotalImpact: TotalImpactFilter | None
    NextPageToken: NextPageToken | None
    MaxResults: PageSize | None


class GetAnomaliesResponse(TypedDict, total=False):
    Anomalies: Anomalies
    NextPageToken: NextPageToken | None


class GetAnomalyMonitorsRequest(ServiceRequest):
    MonitorArnList: Values | None
    NextPageToken: NextPageToken | None
    MaxResults: PageSize | None


class GetAnomalyMonitorsResponse(TypedDict, total=False):
    AnomalyMonitors: AnomalyMonitors
    NextPageToken: NextPageToken | None


class GetAnomalySubscriptionsRequest(ServiceRequest):
    SubscriptionArnList: Values | None
    MonitorArn: GenericString | None
    NextPageToken: NextPageToken | None
    MaxResults: PageSize | None


class GetAnomalySubscriptionsResponse(TypedDict, total=False):
    AnomalySubscriptions: AnomalySubscriptions
    NextPageToken: NextPageToken | None


UsageServices = list[GenericString]


class GetApproximateUsageRecordsRequest(ServiceRequest):
    Granularity: Granularity
    Services: UsageServices | None
    ApproximationDimension: ApproximationDimension


class GetApproximateUsageRecordsResponse(TypedDict, total=False):
    Services: ApproximateUsageRecordsPerService | None
    TotalRecords: NonNegativeLong | None
    LookbackPeriod: DateInterval | None


class GetCommitmentPurchaseAnalysisRequest(ServiceRequest):
    AnalysisId: AnalysisId


class GetCommitmentPurchaseAnalysisResponse(TypedDict, total=False):
    EstimatedCompletionTime: ZonedDateTime
    AnalysisCompletionTime: ZonedDateTime | None
    AnalysisStartedTime: ZonedDateTime
    AnalysisId: AnalysisId
    AnalysisStatus: AnalysisStatus
    ErrorCode: ErrorCode | None
    AnalysisDetails: AnalysisDetails | None
    CommitmentPurchaseAnalysisConfiguration: CommitmentPurchaseAnalysisConfiguration


class GroupDefinition(TypedDict, total=False):
    """Represents a group when you specify a group by criteria or in the
    response to a query with a specific grouping.
    """

    Type: GroupDefinitionType | None
    Key: GroupDefinitionKey | None


GroupDefinitions = list[GroupDefinition]


class GetCostAndUsageComparisonsRequest(ServiceRequest):
    BillingViewArn: BillingViewArn | None
    BaselineTimePeriod: DateInterval
    ComparisonTimePeriod: DateInterval
    MetricForComparison: MetricName
    Filter: Expression | None
    GroupBy: GroupDefinitions | None
    MaxResults: CostAndUsageComparisonsMaxResults | None
    NextPageToken: NextPageToken | None


class GetCostAndUsageComparisonsResponse(TypedDict, total=False):
    CostAndUsageComparisons: CostAndUsageComparisons | None
    TotalCostAndUsage: ComparisonMetrics | None
    NextPageToken: NextPageToken | None


MetricNames = list[MetricName]


class GetCostAndUsageRequest(ServiceRequest):
    TimePeriod: DateInterval
    Granularity: Granularity
    Filter: Expression | None
    Metrics: MetricNames
    GroupBy: GroupDefinitions | None
    BillingViewArn: BillingViewArn | None
    NextPageToken: NextPageToken | None


class MetricValue(TypedDict, total=False):
    """The aggregated value for a metric."""

    Amount: MetricAmount | None
    Unit: MetricUnit | None


Metrics = dict[MetricName, MetricValue]
Keys = list[Key]


class Group(TypedDict, total=False):
    """One level of grouped data in the results."""

    Keys: Keys | None
    Metrics: Metrics | None


Groups = list[Group]


class ResultByTime(TypedDict, total=False):
    """The result that's associated with a time period."""

    TimePeriod: DateInterval | None
    Total: Metrics | None
    Groups: Groups | None
    Estimated: Estimated | None


ResultsByTime = list[ResultByTime]


class GetCostAndUsageResponse(TypedDict, total=False):
    NextPageToken: NextPageToken | None
    GroupDefinitions: GroupDefinitions | None
    ResultsByTime: ResultsByTime | None
    DimensionValueAttributes: DimensionValuesWithAttributesList | None


class GetCostAndUsageWithResourcesRequest(ServiceRequest):
    TimePeriod: DateInterval
    Granularity: Granularity
    Filter: Expression
    Metrics: MetricNames | None
    GroupBy: GroupDefinitions | None
    BillingViewArn: BillingViewArn | None
    NextPageToken: NextPageToken | None


class GetCostAndUsageWithResourcesResponse(TypedDict, total=False):
    NextPageToken: NextPageToken | None
    GroupDefinitions: GroupDefinitions | None
    ResultsByTime: ResultsByTime | None
    DimensionValueAttributes: DimensionValuesWithAttributesList | None


class SortDefinition(TypedDict, total=False):
    """The details for how to sort the data."""

    Key: SortDefinitionKey
    SortOrder: SortOrder | None


SortDefinitions = list[SortDefinition]


class GetCostCategoriesRequest(ServiceRequest):
    SearchString: SearchString | None
    TimePeriod: DateInterval
    CostCategoryName: CostCategoryName | None
    Filter: Expression | None
    SortBy: SortDefinitions | None
    BillingViewArn: BillingViewArn | None
    MaxResults: MaxResults | None
    NextPageToken: NextPageToken | None


class GetCostCategoriesResponse(TypedDict, total=False):
    NextPageToken: NextPageToken | None
    CostCategoryNames: CostCategoryNamesList | None
    CostCategoryValues: CostCategoryValuesList | None
    ReturnSize: PageSize
    TotalSize: PageSize


class GetCostComparisonDriversRequest(ServiceRequest):
    BillingViewArn: BillingViewArn | None
    BaselineTimePeriod: DateInterval
    ComparisonTimePeriod: DateInterval
    MetricForComparison: MetricName
    Filter: Expression | None
    GroupBy: GroupDefinitions | None
    MaxResults: CostComparisonDriversMaxResults | None
    NextPageToken: NextPageToken | None


class GetCostComparisonDriversResponse(TypedDict, total=False):
    CostComparisonDrivers: CostComparisonDrivers | None
    NextPageToken: NextPageToken | None


class GetCostForecastRequest(ServiceRequest):
    TimePeriod: DateInterval
    Metric: Metric
    Granularity: Granularity
    Filter: Expression | None
    BillingViewArn: BillingViewArn | None
    PredictionIntervalLevel: PredictionIntervalLevel | None


class GetCostForecastResponse(TypedDict, total=False):
    Total: MetricValue | None
    ForecastResultsByTime: ForecastResultsByTime | None


class GetDimensionValuesRequest(ServiceRequest):
    SearchString: SearchString | None
    TimePeriod: DateInterval
    Dimension: Dimension
    Context: Context | None
    Filter: Expression | None
    SortBy: SortDefinitions | None
    BillingViewArn: BillingViewArn | None
    MaxResults: MaxResults | None
    NextPageToken: NextPageToken | None


class GetDimensionValuesResponse(TypedDict, total=False):
    DimensionValues: DimensionValuesWithAttributesList
    ReturnSize: PageSize
    TotalSize: PageSize
    NextPageToken: NextPageToken | None


class GetReservationCoverageRequest(ServiceRequest):
    """You can use the following request parameters to query for how much of
    your instance usage a reservation covered.
    """

    TimePeriod: DateInterval
    GroupBy: GroupDefinitions | None
    Granularity: Granularity | None
    Filter: Expression | None
    Metrics: MetricNames | None
    NextPageToken: NextPageToken | None
    SortBy: SortDefinition | None
    MaxResults: MaxResults | None


class GetReservationCoverageResponse(TypedDict, total=False):
    CoveragesByTime: CoveragesByTime
    Total: Coverage | None
    NextPageToken: NextPageToken | None


class ServiceSpecification(TypedDict, total=False):
    """Hardware specifications for the service that you want recommendations
    for.
    """

    EC2Specification: EC2Specification | None


class GetReservationPurchaseRecommendationRequest(ServiceRequest):
    AccountId: GenericString | None
    Service: GenericString
    Filter: Expression | None
    AccountScope: AccountScope | None
    LookbackPeriodInDays: LookbackPeriodInDays | None
    TermInYears: TermInYears | None
    PaymentOption: PaymentOption | None
    ServiceSpecification: ServiceSpecification | None
    PageSize: NonNegativeInteger | None
    NextPageToken: NextPageToken | None


class ReservationPurchaseRecommendationSummary(TypedDict, total=False):
    """A summary about this recommendation, such as the currency code, the
    amount that Amazon Web Services estimates that you could save, and the
    total amount of reservation to purchase.
    """

    TotalEstimatedMonthlySavingsAmount: GenericString | None
    TotalEstimatedMonthlySavingsPercentage: GenericString | None
    CurrencyCode: GenericString | None


class ReservedCapacityDetails(TypedDict, total=False):
    """Details about the reservations that Amazon Web Services recommends that
    you purchase.
    """

    DynamoDBCapacityDetails: DynamoDBCapacityDetails | None


class MemoryDBInstanceDetails(TypedDict, total=False):
    """Details about the MemoryDB reservations that Amazon Web Services
    recommends that you purchase.
    """

    Family: GenericString | None
    NodeType: GenericString | None
    Region: GenericString | None
    CurrentGeneration: GenericBoolean | None
    SizeFlexEligible: GenericBoolean | None


class RedshiftInstanceDetails(TypedDict, total=False):
    """Details about the Amazon Redshift reservations that Amazon Web Services
    recommends that you purchase.
    """

    Family: GenericString | None
    NodeType: GenericString | None
    Region: GenericString | None
    CurrentGeneration: GenericBoolean | None
    SizeFlexEligible: GenericBoolean | None


class RDSInstanceDetails(TypedDict, total=False):
    """Details about the Amazon RDS reservations that Amazon Web Services
    recommends that you purchase.
    """

    Family: GenericString | None
    InstanceType: GenericString | None
    Region: GenericString | None
    DatabaseEngine: GenericString | None
    DatabaseEdition: GenericString | None
    DeploymentOption: GenericString | None
    LicenseModel: GenericString | None
    CurrentGeneration: GenericBoolean | None
    SizeFlexEligible: GenericBoolean | None


class InstanceDetails(TypedDict, total=False):
    """Details about the reservations that Amazon Web Services recommends that
    you purchase.
    """

    EC2InstanceDetails: EC2InstanceDetails | None
    RDSInstanceDetails: RDSInstanceDetails | None
    RedshiftInstanceDetails: RedshiftInstanceDetails | None
    ElastiCacheInstanceDetails: ElastiCacheInstanceDetails | None
    ESInstanceDetails: ESInstanceDetails | None
    MemoryDBInstanceDetails: MemoryDBInstanceDetails | None


class ReservationPurchaseRecommendationDetail(TypedDict, total=False):
    """Details about your recommended reservation purchase."""

    AccountId: GenericString | None
    InstanceDetails: InstanceDetails | None
    RecommendedNumberOfInstancesToPurchase: GenericString | None
    RecommendedNormalizedUnitsToPurchase: GenericString | None
    MinimumNumberOfInstancesUsedPerHour: GenericString | None
    MinimumNormalizedUnitsUsedPerHour: GenericString | None
    MaximumNumberOfInstancesUsedPerHour: GenericString | None
    MaximumNormalizedUnitsUsedPerHour: GenericString | None
    AverageNumberOfInstancesUsedPerHour: GenericString | None
    AverageNormalizedUnitsUsedPerHour: GenericString | None
    AverageUtilization: GenericString | None
    EstimatedBreakEvenInMonths: GenericString | None
    CurrencyCode: GenericString | None
    EstimatedMonthlySavingsAmount: GenericString | None
    EstimatedMonthlySavingsPercentage: GenericString | None
    EstimatedMonthlyOnDemandCost: GenericString | None
    EstimatedReservationCostForLookbackPeriod: GenericString | None
    UpfrontCost: GenericString | None
    RecurringStandardMonthlyCost: GenericString | None
    ReservedCapacityDetails: ReservedCapacityDetails | None
    RecommendedNumberOfCapacityUnitsToPurchase: GenericString | None
    MinimumNumberOfCapacityUnitsUsedPerHour: GenericString | None
    MaximumNumberOfCapacityUnitsUsedPerHour: GenericString | None
    AverageNumberOfCapacityUnitsUsedPerHour: GenericString | None


ReservationPurchaseRecommendationDetails = list[ReservationPurchaseRecommendationDetail]


class ReservationPurchaseRecommendation(TypedDict, total=False):
    """A specific reservation that Amazon Web Services recommends for purchase."""

    AccountScope: AccountScope | None
    LookbackPeriodInDays: LookbackPeriodInDays | None
    TermInYears: TermInYears | None
    PaymentOption: PaymentOption | None
    ServiceSpecification: ServiceSpecification | None
    RecommendationDetails: ReservationPurchaseRecommendationDetails | None
    RecommendationSummary: ReservationPurchaseRecommendationSummary | None


ReservationPurchaseRecommendations = list[ReservationPurchaseRecommendation]


class ReservationPurchaseRecommendationMetadata(TypedDict, total=False):
    """Information about a recommendation, such as the timestamp for when
    Amazon Web Services made a specific recommendation.
    """

    RecommendationId: GenericString | None
    GenerationTimestamp: GenericString | None
    AdditionalMetadata: GenericString | None


class GetReservationPurchaseRecommendationResponse(TypedDict, total=False):
    Metadata: ReservationPurchaseRecommendationMetadata | None
    Recommendations: ReservationPurchaseRecommendations | None
    NextPageToken: NextPageToken | None


class GetReservationUtilizationRequest(ServiceRequest):
    TimePeriod: DateInterval
    GroupBy: GroupDefinitions | None
    Granularity: Granularity | None
    Filter: Expression | None
    SortBy: SortDefinition | None
    NextPageToken: NextPageToken | None
    MaxResults: MaxResults | None


class ReservationAggregates(TypedDict, total=False):
    """The aggregated numbers for your reservation usage."""

    UtilizationPercentage: UtilizationPercentage | None
    UtilizationPercentageInUnits: UtilizationPercentageInUnits | None
    PurchasedHours: PurchasedHours | None
    PurchasedUnits: PurchasedUnits | None
    TotalActualHours: TotalActualHours | None
    TotalActualUnits: TotalActualUnits | None
    UnusedHours: UnusedHours | None
    UnusedUnits: UnusedUnits | None
    OnDemandCostOfRIHoursUsed: OnDemandCostOfRIHoursUsed | None
    NetRISavings: NetRISavings | None
    TotalPotentialRISavings: TotalPotentialRISavings | None
    AmortizedUpfrontFee: AmortizedUpfrontFee | None
    AmortizedRecurringFee: AmortizedRecurringFee | None
    TotalAmortizedFee: TotalAmortizedFee | None
    RICostForUnusedHours: RICostForUnusedHours | None
    RealizedSavings: RealizedSavings | None
    UnrealizedSavings: UnrealizedSavings | None


class ReservationUtilizationGroup(TypedDict, total=False):
    """A group of reservations that share a set of attributes."""

    Key: ReservationGroupKey | None
    Value: ReservationGroupValue | None
    Attributes: Attributes | None
    Utilization: ReservationAggregates | None


ReservationUtilizationGroups = list[ReservationUtilizationGroup]


class UtilizationByTime(TypedDict, total=False):
    """The amount of utilization, in hours."""

    TimePeriod: DateInterval | None
    Groups: ReservationUtilizationGroups | None
    Total: ReservationAggregates | None


UtilizationsByTime = list[UtilizationByTime]


class GetReservationUtilizationResponse(TypedDict, total=False):
    UtilizationsByTime: UtilizationsByTime
    Total: ReservationAggregates | None
    NextPageToken: NextPageToken | None


class RightsizingRecommendationConfiguration(TypedDict, total=False):
    """You can use ``RightsizingRecommendationConfiguration`` to customize
    recommendations across two attributes. You can choose to view
    recommendations for instances within the same instance families or
    across different instance families. You can also choose to view your
    estimated savings that are associated with recommendations with
    consideration of existing Savings Plans or Reserved Instance (RI)
    benefits, or neither.
    """

    RecommendationTarget: RecommendationTarget
    BenefitsConsidered: GenericBoolean


class GetRightsizingRecommendationRequest(ServiceRequest):
    Filter: Expression | None
    Configuration: RightsizingRecommendationConfiguration | None
    Service: GenericString
    PageSize: NonNegativeInteger | None
    NextPageToken: NextPageToken | None


class TerminateRecommendationDetail(TypedDict, total=False):
    """Details on termination recommendation."""

    EstimatedMonthlySavings: GenericString | None
    CurrencyCode: GenericString | None


PlatformDifferences = list[PlatformDifference]


class TargetInstance(TypedDict, total=False):
    """Details on recommended instance."""

    EstimatedMonthlyCost: GenericString | None
    EstimatedMonthlySavings: GenericString | None
    CurrencyCode: GenericString | None
    DefaultTargetInstance: GenericBoolean | None
    ResourceDetails: ResourceDetails | None
    ExpectedResourceUtilization: ResourceUtilization | None
    PlatformDifferences: PlatformDifferences | None


TargetInstancesList = list[TargetInstance]


class ModifyRecommendationDetail(TypedDict, total=False):
    """Details for the modification recommendation."""

    TargetInstances: TargetInstancesList | None


class RightsizingRecommendation(TypedDict, total=False):
    """Recommendations to rightsize resources."""

    AccountId: GenericString | None
    CurrentInstance: CurrentInstance | None
    RightsizingType: RightsizingType | None
    ModifyRecommendationDetail: ModifyRecommendationDetail | None
    TerminateRecommendationDetail: TerminateRecommendationDetail | None
    FindingReasonCodes: FindingReasonCodes | None


RightsizingRecommendationList = list[RightsizingRecommendation]


class RightsizingRecommendationSummary(TypedDict, total=False):
    """The summary of rightsizing recommendations"""

    TotalRecommendationCount: GenericString | None
    EstimatedTotalMonthlySavingsAmount: GenericString | None
    SavingsCurrencyCode: GenericString | None
    SavingsPercentage: GenericString | None


class RightsizingRecommendationMetadata(TypedDict, total=False):
    """Metadata for a recommendation set."""

    RecommendationId: GenericString | None
    GenerationTimestamp: GenericString | None
    LookbackPeriodInDays: LookbackPeriodInDays | None
    AdditionalMetadata: GenericString | None


class GetRightsizingRecommendationResponse(TypedDict, total=False):
    Metadata: RightsizingRecommendationMetadata | None
    Summary: RightsizingRecommendationSummary | None
    RightsizingRecommendations: RightsizingRecommendationList | None
    NextPageToken: NextPageToken | None
    Configuration: RightsizingRecommendationConfiguration | None


class GetSavingsPlanPurchaseRecommendationDetailsRequest(ServiceRequest):
    RecommendationDetailId: RecommendationDetailId


class RecommendationDetailData(TypedDict, total=False):
    """The details and metrics for the given recommendation."""

    AccountScope: AccountScope | None
    LookbackPeriodInDays: LookbackPeriodInDays | None
    SavingsPlansType: SupportedSavingsPlansType | None
    TermInYears: TermInYears | None
    PaymentOption: PaymentOption | None
    AccountId: GenericString | None
    CurrencyCode: GenericString | None
    InstanceFamily: GenericString | None
    Region: GenericString | None
    OfferingId: GenericString | None
    GenerationTimestamp: ZonedDateTime | None
    LatestUsageTimestamp: ZonedDateTime | None
    CurrentAverageHourlyOnDemandSpend: GenericString | None
    CurrentMaximumHourlyOnDemandSpend: GenericString | None
    CurrentMinimumHourlyOnDemandSpend: GenericString | None
    EstimatedAverageUtilization: GenericString | None
    EstimatedMonthlySavingsAmount: GenericString | None
    EstimatedOnDemandCost: GenericString | None
    EstimatedOnDemandCostWithCurrentCommitment: GenericString | None
    EstimatedROI: GenericString | None
    EstimatedSPCost: GenericString | None
    EstimatedSavingsAmount: GenericString | None
    EstimatedSavingsPercentage: GenericString | None
    ExistingHourlyCommitment: GenericString | None
    HourlyCommitmentToPurchase: GenericString | None
    UpfrontCost: GenericString | None
    CurrentAverageCoverage: GenericString | None
    EstimatedAverageCoverage: GenericString | None
    MetricsOverLookbackPeriod: MetricsOverLookbackPeriod | None


class GetSavingsPlanPurchaseRecommendationDetailsResponse(TypedDict, total=False):
    RecommendationDetailId: RecommendationDetailId | None
    RecommendationDetailData: RecommendationDetailData | None


class GetSavingsPlansCoverageRequest(ServiceRequest):
    TimePeriod: DateInterval
    GroupBy: GroupDefinitions | None
    Granularity: Granularity | None
    Filter: Expression | None
    Metrics: MetricNames | None
    NextToken: NextPageToken | None
    MaxResults: MaxResults | None
    SortBy: SortDefinition | None


class SavingsPlansCoverageData(TypedDict, total=False):
    """Specific coverage percentage, On-Demand costs, and spend covered by
    Savings Plans, and total Savings Plans costs for an account.
    """

    SpendCoveredBySavingsPlans: GenericString | None
    OnDemandCost: GenericString | None
    TotalCost: GenericString | None
    CoveragePercentage: GenericString | None


class SavingsPlansCoverage(TypedDict, total=False):
    """The amount of Savings Plans eligible usage that's covered by Savings
    Plans. All calculations consider the On-Demand equivalent of your
    Savings Plans usage.
    """

    Attributes: Attributes | None
    Coverage: SavingsPlansCoverageData | None
    TimePeriod: DateInterval | None


SavingsPlansCoverages = list[SavingsPlansCoverage]


class GetSavingsPlansCoverageResponse(TypedDict, total=False):
    SavingsPlansCoverages: SavingsPlansCoverages
    NextToken: NextPageToken | None


class GetSavingsPlansPurchaseRecommendationRequest(ServiceRequest):
    SavingsPlansType: SupportedSavingsPlansType
    TermInYears: TermInYears
    PaymentOption: PaymentOption
    AccountScope: AccountScope | None
    NextPageToken: NextPageToken | None
    PageSize: NonNegativeInteger | None
    LookbackPeriodInDays: LookbackPeriodInDays
    Filter: Expression | None


class SavingsPlansPurchaseRecommendationSummary(TypedDict, total=False):
    """Summary metrics for your Savings Plans Purchase Recommendations."""

    EstimatedROI: GenericString | None
    CurrencyCode: GenericString | None
    EstimatedTotalCost: GenericString | None
    CurrentOnDemandSpend: GenericString | None
    EstimatedSavingsAmount: GenericString | None
    TotalRecommendationCount: GenericString | None
    DailyCommitmentToPurchase: GenericString | None
    HourlyCommitmentToPurchase: GenericString | None
    EstimatedSavingsPercentage: GenericString | None
    EstimatedMonthlySavingsAmount: GenericString | None
    EstimatedOnDemandCostWithCurrentCommitment: GenericString | None


class SavingsPlansDetails(TypedDict, total=False):
    """The attribute details on a specific Savings Plan."""

    Region: GenericString | None
    InstanceFamily: GenericString | None
    OfferingId: GenericString | None


class SavingsPlansPurchaseRecommendationDetail(TypedDict, total=False):
    """Details for your recommended Savings Plans."""

    SavingsPlansDetails: SavingsPlansDetails | None
    AccountId: GenericString | None
    UpfrontCost: GenericString | None
    EstimatedROI: GenericString | None
    CurrencyCode: GenericString | None
    EstimatedSPCost: GenericString | None
    EstimatedOnDemandCost: GenericString | None
    EstimatedOnDemandCostWithCurrentCommitment: GenericString | None
    EstimatedSavingsAmount: GenericString | None
    EstimatedSavingsPercentage: GenericString | None
    HourlyCommitmentToPurchase: GenericString | None
    EstimatedAverageUtilization: GenericString | None
    EstimatedMonthlySavingsAmount: GenericString | None
    CurrentMinimumHourlyOnDemandSpend: GenericString | None
    CurrentMaximumHourlyOnDemandSpend: GenericString | None
    CurrentAverageHourlyOnDemandSpend: GenericString | None
    RecommendationDetailId: RecommendationDetailId | None


SavingsPlansPurchaseRecommendationDetailList = list[SavingsPlansPurchaseRecommendationDetail]


class SavingsPlansPurchaseRecommendation(TypedDict, total=False):
    """Contains your request parameters, Savings Plan Recommendations Summary,
    and Details.
    """

    AccountScope: AccountScope | None
    SavingsPlansType: SupportedSavingsPlansType | None
    TermInYears: TermInYears | None
    PaymentOption: PaymentOption | None
    LookbackPeriodInDays: LookbackPeriodInDays | None
    SavingsPlansPurchaseRecommendationDetails: SavingsPlansPurchaseRecommendationDetailList | None
    SavingsPlansPurchaseRecommendationSummary: SavingsPlansPurchaseRecommendationSummary | None


class SavingsPlansPurchaseRecommendationMetadata(TypedDict, total=False):
    """Metadata about your Savings Plans Purchase Recommendations."""

    RecommendationId: GenericString | None
    GenerationTimestamp: GenericString | None
    AdditionalMetadata: GenericString | None


class GetSavingsPlansPurchaseRecommendationResponse(TypedDict, total=False):
    Metadata: SavingsPlansPurchaseRecommendationMetadata | None
    SavingsPlansPurchaseRecommendation: SavingsPlansPurchaseRecommendation | None
    NextPageToken: NextPageToken | None


SavingsPlansDataTypes = list[SavingsPlansDataType]


class GetSavingsPlansUtilizationDetailsRequest(ServiceRequest):
    TimePeriod: DateInterval
    Filter: Expression | None
    DataType: SavingsPlansDataTypes | None
    NextToken: NextPageToken | None
    MaxResults: MaxResults | None
    SortBy: SortDefinition | None


class SavingsPlansAmortizedCommitment(TypedDict, total=False):
    """The amortized amount of Savings Plans purchased in a specific account
    during a specific time interval.
    """

    AmortizedRecurringCommitment: GenericString | None
    AmortizedUpfrontCommitment: GenericString | None
    TotalAmortizedCommitment: GenericString | None


class SavingsPlansSavings(TypedDict, total=False):
    """The amount of savings that you're accumulating, against the public
    On-Demand rate of the usage accrued in an account.
    """

    NetSavings: GenericString | None
    OnDemandCostEquivalent: GenericString | None


class SavingsPlansUtilization(TypedDict, total=False):
    """The measurement of how well you're using your existing Savings Plans."""

    TotalCommitment: GenericString | None
    UsedCommitment: GenericString | None
    UnusedCommitment: GenericString | None
    UtilizationPercentage: GenericString | None


class SavingsPlansUtilizationAggregates(TypedDict, total=False):
    """The aggregated utilization metrics for your Savings Plans usage."""

    Utilization: SavingsPlansUtilization
    Savings: SavingsPlansSavings | None
    AmortizedCommitment: SavingsPlansAmortizedCommitment | None


class SavingsPlansUtilizationDetail(TypedDict, total=False):
    """A single daily or monthly Savings Plans utilization rate and details for
    your account. A management account in an organization have access to
    member accounts. You can use ``GetDimensionValues`` to determine the
    possible dimension values.
    """

    SavingsPlanArn: SavingsPlanArn | None
    Attributes: Attributes | None
    Utilization: SavingsPlansUtilization | None
    Savings: SavingsPlansSavings | None
    AmortizedCommitment: SavingsPlansAmortizedCommitment | None


SavingsPlansUtilizationDetails = list[SavingsPlansUtilizationDetail]


class GetSavingsPlansUtilizationDetailsResponse(TypedDict, total=False):
    SavingsPlansUtilizationDetails: SavingsPlansUtilizationDetails
    Total: SavingsPlansUtilizationAggregates | None
    TimePeriod: DateInterval
    NextToken: NextPageToken | None


class GetSavingsPlansUtilizationRequest(ServiceRequest):
    TimePeriod: DateInterval
    Granularity: Granularity | None
    Filter: Expression | None
    SortBy: SortDefinition | None


class SavingsPlansUtilizationByTime(TypedDict, total=False):
    """The amount of Savings Plans utilization (in hours)."""

    TimePeriod: DateInterval
    Utilization: SavingsPlansUtilization
    Savings: SavingsPlansSavings | None
    AmortizedCommitment: SavingsPlansAmortizedCommitment | None


SavingsPlansUtilizationsByTime = list[SavingsPlansUtilizationByTime]


class GetSavingsPlansUtilizationResponse(TypedDict, total=False):
    SavingsPlansUtilizationsByTime: SavingsPlansUtilizationsByTime | None
    Total: SavingsPlansUtilizationAggregates


class GetTagsRequest(ServiceRequest):
    SearchString: SearchString | None
    TimePeriod: DateInterval
    TagKey: TagKey | None
    Filter: Expression | None
    SortBy: SortDefinitions | None
    BillingViewArn: BillingViewArn | None
    MaxResults: MaxResults | None
    NextPageToken: NextPageToken | None


TagList = list[Entity]


class GetTagsResponse(TypedDict, total=False):
    NextPageToken: NextPageToken | None
    Tags: TagList
    ReturnSize: PageSize
    TotalSize: PageSize


class GetUsageForecastRequest(ServiceRequest):
    TimePeriod: DateInterval
    Metric: Metric
    Granularity: Granularity
    Filter: Expression | None
    BillingViewArn: BillingViewArn | None
    PredictionIntervalLevel: PredictionIntervalLevel | None


class GetUsageForecastResponse(TypedDict, total=False):
    Total: MetricValue | None
    ForecastResultsByTime: ForecastResultsByTime | None


class ListCommitmentPurchaseAnalysesRequest(ServiceRequest):
    AnalysisStatus: AnalysisStatus | None
    NextPageToken: NextPageToken | None
    PageSize: NonNegativeInteger | None
    AnalysisIds: AnalysisIds | None


class ListCommitmentPurchaseAnalysesResponse(TypedDict, total=False):
    AnalysisSummaryList: AnalysisSummaryList | None
    NextPageToken: NextPageToken | None


class ListCostAllocationTagBackfillHistoryRequest(ServiceRequest):
    NextToken: NextPageToken | None
    MaxResults: CostAllocationTagsMaxResults | None


class ListCostAllocationTagBackfillHistoryResponse(TypedDict, total=False):
    BackfillRequests: CostAllocationTagBackfillRequestList | None
    NextToken: NextPageToken | None


class ListCostAllocationTagsRequest(ServiceRequest):
    Status: CostAllocationTagStatus | None
    TagKeys: CostAllocationTagKeyList | None
    Type: CostAllocationTagType | None
    NextToken: NextPageToken | None
    MaxResults: CostAllocationTagsMaxResults | None


class ListCostAllocationTagsResponse(TypedDict, total=False):
    CostAllocationTags: CostAllocationTagList | None
    NextToken: NextPageToken | None


class ListCostCategoryDefinitionsRequest(ServiceRequest):
    EffectiveOn: ZonedDateTime | None
    NextToken: NextPageToken | None
    MaxResults: CostCategoryMaxResults | None


class ListCostCategoryDefinitionsResponse(TypedDict, total=False):
    CostCategoryReferences: CostCategoryReferencesList | None
    NextToken: NextPageToken | None


RecommendationIdList = list[RecommendationId]


class ListSavingsPlansPurchaseRecommendationGenerationRequest(ServiceRequest):
    GenerationStatus: GenerationStatus | None
    RecommendationIds: RecommendationIdList | None
    PageSize: NonNegativeInteger | None
    NextPageToken: NextPageToken | None


class ListSavingsPlansPurchaseRecommendationGenerationResponse(TypedDict, total=False):
    GenerationSummaryList: GenerationSummaryList | None
    NextPageToken: NextPageToken | None


class ListTagsForResourceRequest(ServiceRequest):
    ResourceArn: Arn


class ListTagsForResourceResponse(TypedDict, total=False):
    ResourceTags: ResourceTagList | None


class ProvideAnomalyFeedbackRequest(ServiceRequest):
    AnomalyId: GenericString
    Feedback: AnomalyFeedbackType


class ProvideAnomalyFeedbackResponse(TypedDict, total=False):
    AnomalyId: GenericString


ResourceTagKeyList = list[ResourceTagKey]


class StartCommitmentPurchaseAnalysisRequest(ServiceRequest):
    CommitmentPurchaseAnalysisConfiguration: CommitmentPurchaseAnalysisConfiguration


class StartCommitmentPurchaseAnalysisResponse(TypedDict, total=False):
    AnalysisId: AnalysisId
    AnalysisStartedTime: ZonedDateTime
    EstimatedCompletionTime: ZonedDateTime


class StartCostAllocationTagBackfillRequest(ServiceRequest):
    BackfillFrom: ZonedDateTime


class StartCostAllocationTagBackfillResponse(TypedDict, total=False):
    BackfillRequest: CostAllocationTagBackfillRequest | None


class StartSavingsPlansPurchaseRecommendationGenerationRequest(ServiceRequest):
    pass


class StartSavingsPlansPurchaseRecommendationGenerationResponse(TypedDict, total=False):
    RecommendationId: RecommendationId | None
    GenerationStartedTime: ZonedDateTime | None
    EstimatedCompletionTime: ZonedDateTime | None


class TagResourceRequest(ServiceRequest):
    ResourceArn: Arn
    ResourceTags: ResourceTagList


class TagResourceResponse(TypedDict, total=False):
    pass


class UntagResourceRequest(ServiceRequest):
    ResourceArn: Arn
    ResourceTagKeys: ResourceTagKeyList


class UntagResourceResponse(TypedDict, total=False):
    pass


class UpdateAnomalyMonitorRequest(ServiceRequest):
    MonitorArn: GenericString
    MonitorName: GenericString | None


class UpdateAnomalyMonitorResponse(TypedDict, total=False):
    MonitorArn: GenericString


class UpdateAnomalySubscriptionRequest(ServiceRequest):
    SubscriptionArn: GenericString
    Threshold: NullableNonNegativeDouble | None
    Frequency: AnomalySubscriptionFrequency | None
    MonitorArnList: MonitorArnList | None
    Subscribers: Subscribers | None
    SubscriptionName: GenericString | None
    ThresholdExpression: Expression | None


class UpdateAnomalySubscriptionResponse(TypedDict, total=False):
    SubscriptionArn: GenericString


class UpdateCostAllocationTagsStatusError(TypedDict, total=False):
    """Gives a detailed description of the result of an action. It's on each
    cost allocation tag entry in the request.
    """

    TagKey: TagKey | None
    Code: GenericString | None
    Message: ErrorMessage | None


UpdateCostAllocationTagsStatusErrors = list[UpdateCostAllocationTagsStatusError]


class UpdateCostAllocationTagsStatusRequest(ServiceRequest):
    CostAllocationTagsStatus: CostAllocationTagStatusList


class UpdateCostAllocationTagsStatusResponse(TypedDict, total=False):
    Errors: UpdateCostAllocationTagsStatusErrors | None


class UpdateCostCategoryDefinitionRequest(ServiceRequest):
    CostCategoryArn: Arn
    EffectiveStart: ZonedDateTime | None
    RuleVersion: CostCategoryRuleVersion
    Rules: CostCategoryRulesList
    DefaultValue: CostCategoryValue | None
    SplitChargeRules: CostCategorySplitChargeRulesList | None


class UpdateCostCategoryDefinitionResponse(TypedDict, total=False):
    CostCategoryArn: Arn | None
    EffectiveStart: ZonedDateTime | None


class CeApi:
    service: str = "ce"
    version: str = "2017-10-25"

    @handler("CreateAnomalyMonitor")
    def create_anomaly_monitor(
        self,
        context: RequestContext,
        anomaly_monitor: AnomalyMonitor,
        resource_tags: ResourceTagList | None = None,
        **kwargs,
    ) -> CreateAnomalyMonitorResponse:
        """Creates a new cost anomaly detection monitor with the requested type and
        monitor specification.

        :param anomaly_monitor: The cost anomaly detection monitor object that you want to create.
        :param resource_tags: An optional list of tags to associate with the specified
        ```AnomalyMonitor`` <https://docs.
        :returns: CreateAnomalyMonitorResponse
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("CreateAnomalySubscription")
    def create_anomaly_subscription(
        self,
        context: RequestContext,
        anomaly_subscription: AnomalySubscription,
        resource_tags: ResourceTagList | None = None,
        **kwargs,
    ) -> CreateAnomalySubscriptionResponse:
        """Adds an alert subscription to a cost anomaly detection monitor. You can
        use each subscription to define subscribers with email or SNS
        notifications. Email subscribers can set an absolute or percentage
        threshold and a time frequency for receiving notifications.

        :param anomaly_subscription: The cost anomaly subscription object that you want to create.
        :param resource_tags: An optional list of tags to associate with the specified
        ```AnomalySubscription`` <https://docs.
        :returns: CreateAnomalySubscriptionResponse
        :raises UnknownMonitorException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("CreateCostCategoryDefinition")
    def create_cost_category_definition(
        self,
        context: RequestContext,
        name: CostCategoryName,
        rule_version: CostCategoryRuleVersion,
        rules: CostCategoryRulesList,
        effective_start: ZonedDateTime | None = None,
        default_value: CostCategoryValue | None = None,
        split_charge_rules: CostCategorySplitChargeRulesList | None = None,
        resource_tags: ResourceTagList | None = None,
        **kwargs,
    ) -> CreateCostCategoryDefinitionResponse:
        """Creates a new Cost Category with the requested name and rules.

        :param name: The unique name of the Cost Category.
        :param rule_version: The rule schema version in this particular Cost Category.
        :param rules: The Cost Category rules used to categorize costs.
        :param effective_start: The Cost Category's effective start date.
        :param default_value: The default value for the cost category.
        :param split_charge_rules: The split charge rules used to allocate your charges between your Cost
        Category values.
        :param resource_tags: An optional list of tags to associate with the specified
        ```CostCategory`` <https://docs.
        :returns: CreateCostCategoryDefinitionResponse
        :raises ServiceQuotaExceededException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("DeleteAnomalyMonitor")
    def delete_anomaly_monitor(
        self, context: RequestContext, monitor_arn: GenericString, **kwargs
    ) -> DeleteAnomalyMonitorResponse:
        """Deletes a cost anomaly monitor.

        :param monitor_arn: The unique identifier of the cost anomaly monitor that you want to
        delete.
        :returns: DeleteAnomalyMonitorResponse
        :raises LimitExceededException:
        :raises UnknownMonitorException:
        """
        raise NotImplementedError

    @handler("DeleteAnomalySubscription")
    def delete_anomaly_subscription(
        self, context: RequestContext, subscription_arn: GenericString, **kwargs
    ) -> DeleteAnomalySubscriptionResponse:
        """Deletes a cost anomaly subscription.

        :param subscription_arn: The unique identifier of the cost anomaly subscription that you want to
        delete.
        :returns: DeleteAnomalySubscriptionResponse
        :raises LimitExceededException:
        :raises UnknownSubscriptionException:
        """
        raise NotImplementedError

    @handler("DeleteCostCategoryDefinition")
    def delete_cost_category_definition(
        self, context: RequestContext, cost_category_arn: Arn, **kwargs
    ) -> DeleteCostCategoryDefinitionResponse:
        """Deletes a Cost Category. Expenses from this month going forward will no
        longer be categorized with this Cost Category.

        :param cost_category_arn: The unique identifier for your Cost Category.
        :returns: DeleteCostCategoryDefinitionResponse
        :raises ResourceNotFoundException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("DescribeCostCategoryDefinition")
    def describe_cost_category_definition(
        self,
        context: RequestContext,
        cost_category_arn: Arn,
        effective_on: ZonedDateTime | None = None,
        **kwargs,
    ) -> DescribeCostCategoryDefinitionResponse:
        """Returns the name, Amazon Resource Name (ARN), rules, definition, and
        effective dates of a Cost Category that's defined in the account.

        You have the option to use ``EffectiveOn`` to return a Cost Category
        that's active on a specific date. If there's no ``EffectiveOn``
        specified, you see a Cost Category that's effective on the current date.
        If Cost Category is still effective, ``EffectiveEnd`` is omitted in the
        response.

        :param cost_category_arn: The unique identifier for your Cost Category.
        :param effective_on: The date when the Cost Category was effective.
        :returns: DescribeCostCategoryDefinitionResponse
        :raises ResourceNotFoundException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("GetAnomalies")
    def get_anomalies(
        self,
        context: RequestContext,
        date_interval: AnomalyDateInterval,
        monitor_arn: GenericString | None = None,
        feedback: AnomalyFeedbackType | None = None,
        total_impact: TotalImpactFilter | None = None,
        next_page_token: NextPageToken | None = None,
        max_results: PageSize | None = None,
        **kwargs,
    ) -> GetAnomaliesResponse:
        """Retrieves all of the cost anomalies detected on your account during the
        time period that's specified by the ``DateInterval`` object. Anomalies
        are available for up to 90 days.

        :param date_interval: Assigns the start and end dates for retrieving cost anomalies.
        :param monitor_arn: Retrieves all of the cost anomalies detected for a specific cost anomaly
        monitor Amazon Resource Name (ARN).
        :param feedback: Filters anomaly results by the feedback field on the anomaly object.
        :param total_impact: Filters anomaly results by the total impact field on the anomaly object.
        :param next_page_token: The token to retrieve the next set of results.
        :param max_results: The number of entries a paginated response contains.
        :returns: GetAnomaliesResponse
        :raises LimitExceededException:
        :raises InvalidNextTokenException:
        """
        raise NotImplementedError

    @handler("GetAnomalyMonitors")
    def get_anomaly_monitors(
        self,
        context: RequestContext,
        monitor_arn_list: Values | None = None,
        next_page_token: NextPageToken | None = None,
        max_results: PageSize | None = None,
        **kwargs,
    ) -> GetAnomalyMonitorsResponse:
        """Retrieves the cost anomaly monitor definitions for your account. You can
        filter using a list of cost anomaly monitor Amazon Resource Names
        (ARNs).

        :param monitor_arn_list: A list of cost anomaly monitor ARNs.
        :param next_page_token: The token to retrieve the next set of results.
        :param max_results: The number of entries that a paginated response contains.
        :returns: GetAnomalyMonitorsResponse
        :raises LimitExceededException:
        :raises UnknownMonitorException:
        :raises InvalidNextTokenException:
        """
        raise NotImplementedError

    @handler("GetAnomalySubscriptions")
    def get_anomaly_subscriptions(
        self,
        context: RequestContext,
        subscription_arn_list: Values | None = None,
        monitor_arn: GenericString | None = None,
        next_page_token: NextPageToken | None = None,
        max_results: PageSize | None = None,
        **kwargs,
    ) -> GetAnomalySubscriptionsResponse:
        """Retrieves the cost anomaly subscription objects for your account. You
        can filter using a list of cost anomaly monitor Amazon Resource Names
        (ARNs).

        :param subscription_arn_list: A list of cost anomaly subscription ARNs.
        :param monitor_arn: Cost anomaly monitor ARNs.
        :param next_page_token: The token to retrieve the next set of results.
        :param max_results: The number of entries a paginated response contains.
        :returns: GetAnomalySubscriptionsResponse
        :raises LimitExceededException:
        :raises UnknownSubscriptionException:
        :raises InvalidNextTokenException:
        """
        raise NotImplementedError

    @handler("GetApproximateUsageRecords")
    def get_approximate_usage_records(
        self,
        context: RequestContext,
        granularity: Granularity,
        approximation_dimension: ApproximationDimension,
        services: UsageServices | None = None,
        **kwargs,
    ) -> GetApproximateUsageRecordsResponse:
        """Retrieves estimated usage records for hourly granularity or
        resource-level data at daily granularity.

        :param granularity: How granular you want the data to be.
        :param approximation_dimension: The service to evaluate for the usage records.
        :param services: The service metadata for the service or services you want to query.
        :returns: GetApproximateUsageRecordsResponse
        :raises LimitExceededException:
        :raises DataUnavailableException:
        """
        raise NotImplementedError

    @handler("GetCommitmentPurchaseAnalysis")
    def get_commitment_purchase_analysis(
        self, context: RequestContext, analysis_id: AnalysisId, **kwargs
    ) -> GetCommitmentPurchaseAnalysisResponse:
        """Retrieves a commitment purchase analysis result based on the
        ``AnalysisId``.

        :param analysis_id: The analysis ID that's associated with the commitment purchase analysis.
        :returns: GetCommitmentPurchaseAnalysisResponse
        :raises LimitExceededException:
        :raises AnalysisNotFoundException:
        :raises DataUnavailableException:
        """
        raise NotImplementedError

    @handler("GetCostAndUsage")
    def get_cost_and_usage(
        self,
        context: RequestContext,
        time_period: DateInterval,
        granularity: Granularity,
        metrics: MetricNames,
        filter: Expression | None = None,
        group_by: GroupDefinitions | None = None,
        billing_view_arn: BillingViewArn | None = None,
        next_page_token: NextPageToken | None = None,
        **kwargs,
    ) -> GetCostAndUsageResponse:
        """Retrieves cost and usage metrics for your account. You can specify which
        cost and usage-related metric that you want the request to return. For
        example, you can specify ``BlendedCosts`` or ``UsageQuantity``. You can
        also filter and group your data by various dimensions, such as
        ``SERVICE`` or ``AZ``, in a specific time range. For a complete list of
        valid dimensions, see the
        `GetDimensionValues <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetDimensionValues.html>`__
        operation. Management account in an organization in Organizations have
        access to all member accounts.

        For information about filter limitations, see `Quotas and
        restrictions <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/billing-limits.html>`__
        in the *Billing and Cost Management User Guide*.

        :param time_period: Sets the start date and end date for retrieving Amazon Web Services
        costs.
        :param granularity: Sets the Amazon Web Services cost granularity to ``MONTHLY`` or
        ``DAILY``, or ``HOURLY``.
        :param metrics: Which metrics are returned in the query.
        :param filter: Filters Amazon Web Services costs by different dimensions.
        :param group_by: You can group Amazon Web Services costs using up to two different
        groups, either dimensions, tag keys, cost categories, or any two group
        by types.
        :param billing_view_arn: The Amazon Resource Name (ARN) that uniquely identifies a specific
        billing view.
        :param next_page_token: The token to retrieve the next set of results.
        :returns: GetCostAndUsageResponse
        :raises LimitExceededException:
        :raises BillExpirationException:
        :raises DataUnavailableException:
        :raises InvalidNextTokenException:
        :raises RequestChangedException:
        :raises ResourceNotFoundException:
        :raises BillingViewHealthStatusException:
        """
        raise NotImplementedError

    @handler("GetCostAndUsageComparisons")
    def get_cost_and_usage_comparisons(
        self,
        context: RequestContext,
        baseline_time_period: DateInterval,
        comparison_time_period: DateInterval,
        metric_for_comparison: MetricName,
        billing_view_arn: BillingViewArn | None = None,
        filter: Expression | None = None,
        group_by: GroupDefinitions | None = None,
        max_results: CostAndUsageComparisonsMaxResults | None = None,
        next_page_token: NextPageToken | None = None,
        **kwargs,
    ) -> GetCostAndUsageComparisonsResponse:
        """Retrieves cost and usage comparisons for your account between two
        periods within the last 13 months. If you have enabled multi-year data
        at monthly granularity, you can go back up to 38 months.

        :param baseline_time_period: The reference time period for comparison.
        :param comparison_time_period: The comparison time period for analysis.
        :param metric_for_comparison: The cost and usage metric to compare.
        :param billing_view_arn: The Amazon Resource Name (ARN) that uniquely identifies a specific
        billing view.
        :param filter: Use ``Expression`` to filter in various Cost Explorer APIs.
        :param group_by: You can group results using the attributes ``DIMENSION``, ``TAG``, and
        ``COST_CATEGORY``.
        :param max_results: The maximum number of results that are returned for the request.
        :param next_page_token: The token to retrieve the next set of paginated results.
        :returns: GetCostAndUsageComparisonsResponse
        :raises DataUnavailableException:
        :raises InvalidNextTokenException:
        :raises LimitExceededException:
        :raises ResourceNotFoundException:
        :raises BillingViewHealthStatusException:
        """
        raise NotImplementedError

    @handler("GetCostAndUsageWithResources")
    def get_cost_and_usage_with_resources(
        self,
        context: RequestContext,
        time_period: DateInterval,
        granularity: Granularity,
        filter: Expression,
        metrics: MetricNames | None = None,
        group_by: GroupDefinitions | None = None,
        billing_view_arn: BillingViewArn | None = None,
        next_page_token: NextPageToken | None = None,
        **kwargs,
    ) -> GetCostAndUsageWithResourcesResponse:
        """Retrieves cost and usage metrics with resources for your account. You
        can specify which cost and usage-related metric, such as
        ``BlendedCosts`` or ``UsageQuantity``, that you want the request to
        return. You can also filter and group your data by various dimensions,
        such as ``SERVICE`` or ``AZ``, in a specific time range. For a complete
        list of valid dimensions, see the
        `GetDimensionValues <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetDimensionValues.html>`__
        operation. Management account in an organization in Organizations have
        access to all member accounts.

        Hourly granularity is only available for EC2-Instances (Elastic Compute
        Cloud) resource-level data. All other resource-level data is available
        at daily granularity.

        This is an opt-in only feature. You can enable this feature from the
        Cost Explorer Settings page. For information about how to access the
        Settings page, see `Controlling Access for Cost
        Explorer <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ce-access.html>`__
        in the *Billing and Cost Management User Guide*.

        :param time_period: Sets the start and end dates for retrieving Amazon Web Services costs.
        :param granularity: Sets the Amazon Web Services cost granularity to ``MONTHLY``, ``DAILY``,
        or ``HOURLY``.
        :param filter: Filters Amazon Web Services costs by different dimensions.
        :param metrics: Which metrics are returned in the query.
        :param group_by: You can group Amazon Web Services costs using up to two different
        groups: ``DIMENSION``, ``TAG``, ``COST_CATEGORY``.
        :param billing_view_arn: The Amazon Resource Name (ARN) that uniquely identifies a specific
        billing view.
        :param next_page_token: The token to retrieve the next set of results.
        :returns: GetCostAndUsageWithResourcesResponse
        :raises DataUnavailableException:
        :raises LimitExceededException:
        :raises BillExpirationException:
        :raises InvalidNextTokenException:
        :raises RequestChangedException:
        :raises ResourceNotFoundException:
        :raises BillingViewHealthStatusException:
        """
        raise NotImplementedError

    @handler("GetCostCategories")
    def get_cost_categories(
        self,
        context: RequestContext,
        time_period: DateInterval,
        search_string: SearchString | None = None,
        cost_category_name: CostCategoryName | None = None,
        filter: Expression | None = None,
        sort_by: SortDefinitions | None = None,
        billing_view_arn: BillingViewArn | None = None,
        max_results: MaxResults | None = None,
        next_page_token: NextPageToken | None = None,
        **kwargs,
    ) -> GetCostCategoriesResponse:
        """Retrieves an array of Cost Category names and values incurred cost.

        If some Cost Category names and values are not associated with any cost,
        they will not be returned by this API.

        :param time_period: The time period of the request.
        :param search_string: The value that you want to search the filter values for.
        :param cost_category_name: The unique name of the Cost Category.
        :param filter: Use ``Expression`` to filter in various Cost Explorer APIs.
        :param sort_by: The value that you sort the data by.
        :param billing_view_arn: The Amazon Resource Name (ARN) that uniquely identifies a specific
        billing view.
        :param max_results: This field is only used when the ``SortBy`` value is provided in the
        request.
        :param next_page_token: If the number of objects that are still available for retrieval exceeds
        the quota, Amazon Web Services returns a NextPageToken value in the
        response.
        :returns: GetCostCategoriesResponse
        :raises LimitExceededException:
        :raises BillExpirationException:
        :raises DataUnavailableException:
        :raises InvalidNextTokenException:
        :raises RequestChangedException:
        :raises ResourceNotFoundException:
        :raises BillingViewHealthStatusException:
        """
        raise NotImplementedError

    @handler("GetCostComparisonDrivers")
    def get_cost_comparison_drivers(
        self,
        context: RequestContext,
        baseline_time_period: DateInterval,
        comparison_time_period: DateInterval,
        metric_for_comparison: MetricName,
        billing_view_arn: BillingViewArn | None = None,
        filter: Expression | None = None,
        group_by: GroupDefinitions | None = None,
        max_results: CostComparisonDriversMaxResults | None = None,
        next_page_token: NextPageToken | None = None,
        **kwargs,
    ) -> GetCostComparisonDriversResponse:
        """Retrieves key factors driving cost changes between two time periods
        within the last 13 months, such as usage changes, discount changes, and
        commitment-based savings. If you have enabled multi-year data at monthly
        granularity, you can go back up to 38 months.

        :param baseline_time_period: The reference time period for comparison.
        :param comparison_time_period: The comparison time period for analysis.
        :param metric_for_comparison: The cost and usage metric to compare.
        :param billing_view_arn: The Amazon Resource Name (ARN) that uniquely identifies a specific
        billing view.
        :param filter: Use ``Expression`` to filter in various Cost Explorer APIs.
        :param group_by: You can group results using the attributes ``DIMENSION``, ``TAG``, and
        ``COST_CATEGORY``.
        :param max_results: The maximum number of results that are returned for the request.
        :param next_page_token: The token to retrieve the next set of paginated results.
        :returns: GetCostComparisonDriversResponse
        :raises DataUnavailableException:
        :raises InvalidNextTokenException:
        :raises LimitExceededException:
        :raises ResourceNotFoundException:
        :raises BillingViewHealthStatusException:
        """
        raise NotImplementedError

    @handler("GetCostForecast")
    def get_cost_forecast(
        self,
        context: RequestContext,
        time_period: DateInterval,
        metric: Metric,
        granularity: Granularity,
        filter: Expression | None = None,
        billing_view_arn: BillingViewArn | None = None,
        prediction_interval_level: PredictionIntervalLevel | None = None,
        **kwargs,
    ) -> GetCostForecastResponse:
        """Retrieves a forecast for how much Amazon Web Services predicts that you
        will spend over the forecast time period that you select, based on your
        past costs.

        :param time_period: The period of time that you want the forecast to cover.
        :param metric: Which metric Cost Explorer uses to create your forecast.
        :param granularity: How granular you want the forecast to be.
        :param filter: The filters that you want to use to filter your forecast.
        :param billing_view_arn: The Amazon Resource Name (ARN) that uniquely identifies a specific
        billing view.
        :param prediction_interval_level: Cost Explorer always returns the mean forecast as a single point.
        :returns: GetCostForecastResponse
        :raises LimitExceededException:
        :raises DataUnavailableException:
        :raises ResourceNotFoundException:
        :raises BillingViewHealthStatusException:
        """
        raise NotImplementedError

    @handler("GetDimensionValues", expand=False)
    def get_dimension_values(
        self, context: RequestContext, request: GetDimensionValuesRequest, **kwargs
    ) -> GetDimensionValuesResponse:
        """Retrieves all available filter values for a specified filter over a
        period of time. You can search the dimension values for an arbitrary
        string.

        :param time_period: The start date and end date for retrieving the dimension values.
        :param dimension: The name of the dimension.
        :param search_string: The value that you want to search the filter values for.
        :param context: The context for the call to ``GetDimensionValues``.
        :param filter: Use ``Expression`` to filter in various Cost Explorer APIs.
        :param sort_by: The value that you want to sort the data by.
        :param billing_view_arn: The Amazon Resource Name (ARN) that uniquely identifies a specific
        billing view.
        :param max_results: This field is only used when SortBy is provided in the request.
        :param next_page_token: The token to retrieve the next set of results.
        :returns: GetDimensionValuesResponse
        :raises LimitExceededException:
        :raises BillExpirationException:
        :raises DataUnavailableException:
        :raises InvalidNextTokenException:
        :raises RequestChangedException:
        :raises ResourceNotFoundException:
        :raises BillingViewHealthStatusException:
        """
        raise NotImplementedError

    @handler("GetReservationCoverage")
    def get_reservation_coverage(
        self,
        context: RequestContext,
        time_period: DateInterval,
        group_by: GroupDefinitions | None = None,
        granularity: Granularity | None = None,
        filter: Expression | None = None,
        metrics: MetricNames | None = None,
        next_page_token: NextPageToken | None = None,
        sort_by: SortDefinition | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> GetReservationCoverageResponse:
        """Retrieves the reservation coverage for your account, which you can use
        to see how much of your Amazon Elastic Compute Cloud, Amazon
        ElastiCache, Amazon Relational Database Service, or Amazon Redshift
        usage is covered by a reservation. An organization's management account
        can see the coverage of the associated member accounts. This supports
        dimensions, Cost Categories, and nested expressions. For any time
        period, you can filter data about reservation usage by the following
        dimensions:

        -  AZ

        -  CACHE_ENGINE

        -  DATABASE_ENGINE

        -  DEPLOYMENT_OPTION

        -  INSTANCE_TYPE

        -  LINKED_ACCOUNT

        -  OPERATING_SYSTEM

        -  PLATFORM

        -  REGION

        -  SERVICE

        -  TAG

        -  TENANCY

        To determine valid values for a dimension, use the
        ``GetDimensionValues`` operation.

        :param time_period: The start and end dates of the period that you want to retrieve data
        about reservation coverage for.
        :param group_by: You can group the data by the following attributes:

        -  AZ

        -  CACHE_ENGINE

        -  DATABASE_ENGINE

        -  DEPLOYMENT_OPTION

        -  INSTANCE_TYPE

        -  INVOICING_ENTITY

        -  LINKED_ACCOUNT

        -  OPERATING_SYSTEM

        -  PLATFORM

        -  REGION

        -  TENANCY.
        :param granularity: The granularity of the Amazon Web Services cost data for the
        reservation.
        :param filter: Filters utilization data by dimensions.
        :param metrics: The measurement that you want your reservation coverage reported in.
        :param next_page_token: The token to retrieve the next set of results.
        :param sort_by: The value by which you want to sort the data.
        :param max_results: The maximum number of objects that you returned for this request.
        :returns: GetReservationCoverageResponse
        :raises LimitExceededException:
        :raises DataUnavailableException:
        :raises InvalidNextTokenException:
        """
        raise NotImplementedError

    @handler("GetReservationPurchaseRecommendation")
    def get_reservation_purchase_recommendation(
        self,
        context: RequestContext,
        service: GenericString,
        account_id: GenericString | None = None,
        filter: Expression | None = None,
        account_scope: AccountScope | None = None,
        lookback_period_in_days: LookbackPeriodInDays | None = None,
        term_in_years: TermInYears | None = None,
        payment_option: PaymentOption | None = None,
        service_specification: ServiceSpecification | None = None,
        page_size: NonNegativeInteger | None = None,
        next_page_token: NextPageToken | None = None,
        **kwargs,
    ) -> GetReservationPurchaseRecommendationResponse:
        """Gets recommendations for reservation purchases. These recommendations
        might help you to reduce your costs. Reservations provide a discounted
        hourly rate (up to 75%) compared to On-Demand pricing.

        Amazon Web Services generates your recommendations by identifying your
        On-Demand usage during a specific time period and collecting your usage
        into categories that are eligible for a reservation. After Amazon Web
        Services has these categories, it simulates every combination of
        reservations in each category of usage to identify the best number of
        each type of Reserved Instance (RI) to purchase to maximize your
        estimated savings.

        For example, Amazon Web Services automatically aggregates your Amazon
        EC2 Linux, shared tenancy, and c4 family usage in the US West (Oregon)
        Region and recommends that you buy size-flexible regional reservations
        to apply to the c4 family usage. Amazon Web Services recommends the
        smallest size instance in an instance family. This makes it easier to
        purchase a size-flexible Reserved Instance (RI). Amazon Web Services
        also shows the equal number of normalized units. This way, you can
        purchase any instance size that you want. For this example, your RI
        recommendation is for ``c4.large`` because that is the smallest size
        instance in the c4 instance family.

        :param service: The specific service that you want recommendations for.
        :param account_id: The account ID that's associated with the recommendation.
        :param filter: Use ``Expression`` to filter in various Cost Explorer APIs.
        :param account_scope: The account scope that you want your recommendations for.
        :param lookback_period_in_days: The number of previous days that you want Amazon Web Services to
        consider when it calculates your recommendations.
        :param term_in_years: The reservation term that you want recommendations for.
        :param payment_option: The reservation purchase option that you want recommendations for.
        :param service_specification: The hardware specifications for the service instances that you want
        recommendations for, such as standard or convertible Amazon EC2
        instances.
        :param page_size: The number of recommendations that you want returned in a single
        response object.
        :param next_page_token: The pagination token that indicates the next set of results that you
        want to retrieve.
        :returns: GetReservationPurchaseRecommendationResponse
        :raises LimitExceededException:
        :raises DataUnavailableException:
        :raises InvalidNextTokenException:
        """
        raise NotImplementedError

    @handler("GetReservationUtilization")
    def get_reservation_utilization(
        self,
        context: RequestContext,
        time_period: DateInterval,
        group_by: GroupDefinitions | None = None,
        granularity: Granularity | None = None,
        filter: Expression | None = None,
        sort_by: SortDefinition | None = None,
        next_page_token: NextPageToken | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> GetReservationUtilizationResponse:
        """Retrieves the reservation utilization for your account. Management
        account in an organization have access to member accounts. You can
        filter data by dimensions in a time period. You can use
        ``GetDimensionValues`` to determine the possible dimension values.
        Currently, you can group only by ``SUBSCRIPTION_ID``.

        :param time_period: Sets the start and end dates for retrieving Reserved Instance (RI)
        utilization.
        :param group_by: Groups only by ``SUBSCRIPTION_ID``.
        :param granularity: If ``GroupBy`` is set, ``Granularity`` can't be set.
        :param filter: Filters utilization data by dimensions.
        :param sort_by: The value that you want to sort the data by.
        :param next_page_token: The token to retrieve the next set of results.
        :param max_results: The maximum number of objects that you returned for this request.
        :returns: GetReservationUtilizationResponse
        :raises LimitExceededException:
        :raises DataUnavailableException:
        :raises InvalidNextTokenException:
        """
        raise NotImplementedError

    @handler("GetRightsizingRecommendation")
    def get_rightsizing_recommendation(
        self,
        context: RequestContext,
        service: GenericString,
        filter: Expression | None = None,
        configuration: RightsizingRecommendationConfiguration | None = None,
        page_size: NonNegativeInteger | None = None,
        next_page_token: NextPageToken | None = None,
        **kwargs,
    ) -> GetRightsizingRecommendationResponse:
        """Creates recommendations that help you save cost by identifying idle and
        underutilized Amazon EC2 instances.

        Recommendations are generated to either downsize or terminate instances,
        along with providing savings detail and metrics. For more information
        about calculation and function, see `Optimizing Your Cost with
        Rightsizing
        Recommendations <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ce-rightsizing.html>`__
        in the *Billing and Cost Management User Guide*.

        :param service: The specific service that you want recommendations for.
        :param filter: Use ``Expression`` to filter in various Cost Explorer APIs.
        :param configuration: You can use Configuration to customize recommendations across two
        attributes.
        :param page_size: The number of recommendations that you want returned in a single
        response object.
        :param next_page_token: The pagination token that indicates the next set of results that you
        want to retrieve.
        :returns: GetRightsizingRecommendationResponse
        :raises LimitExceededException:
        :raises InvalidNextTokenException:
        """
        raise NotImplementedError

    @handler("GetSavingsPlanPurchaseRecommendationDetails")
    def get_savings_plan_purchase_recommendation_details(
        self, context: RequestContext, recommendation_detail_id: RecommendationDetailId, **kwargs
    ) -> GetSavingsPlanPurchaseRecommendationDetailsResponse:
        """Retrieves the details for a Savings Plan recommendation. These details
        include the hourly data-points that construct the cost, coverage, and
        utilization charts.

        :param recommendation_detail_id: The ID that is associated with the Savings Plan recommendation.
        :returns: GetSavingsPlanPurchaseRecommendationDetailsResponse
        :raises LimitExceededException:
        :raises DataUnavailableException:
        """
        raise NotImplementedError

    @handler("GetSavingsPlansCoverage")
    def get_savings_plans_coverage(
        self,
        context: RequestContext,
        time_period: DateInterval,
        group_by: GroupDefinitions | None = None,
        granularity: Granularity | None = None,
        filter: Expression | None = None,
        metrics: MetricNames | None = None,
        next_token: NextPageToken | None = None,
        max_results: MaxResults | None = None,
        sort_by: SortDefinition | None = None,
        **kwargs,
    ) -> GetSavingsPlansCoverageResponse:
        """Retrieves the Savings Plans covered for your account. This enables you
        to see how much of your cost is covered by a Savings Plan. An
        organization’s management account can see the coverage of the associated
        member accounts. This supports dimensions, Cost Categories, and nested
        expressions. For any time period, you can filter data for Savings Plans
        usage with the following dimensions:

        -  ``LINKED_ACCOUNT``

        -  ``REGION``

        -  ``SERVICE``

        -  ``INSTANCE_FAMILY``

        To determine valid values for a dimension, use the
        ``GetDimensionValues`` operation.

        :param time_period: The time period that you want the usage and costs for.
        :param group_by: You can group the data using the attributes ``INSTANCE_FAMILY``,
        ``REGION``, or ``SERVICE``.
        :param granularity: The granularity of the Amazon Web Services cost data for your Savings
        Plans.
        :param filter: Filters Savings Plans coverage data by dimensions.
        :param metrics: The measurement that you want your Savings Plans coverage reported in.
        :param next_token: The token to retrieve the next set of results.
        :param max_results: The number of items to be returned in a response.
        :param sort_by: The value that you want to sort the data by.
        :returns: GetSavingsPlansCoverageResponse
        :raises LimitExceededException:
        :raises DataUnavailableException:
        :raises InvalidNextTokenException:
        """
        raise NotImplementedError

    @handler("GetSavingsPlansPurchaseRecommendation")
    def get_savings_plans_purchase_recommendation(
        self,
        context: RequestContext,
        savings_plans_type: SupportedSavingsPlansType,
        term_in_years: TermInYears,
        payment_option: PaymentOption,
        lookback_period_in_days: LookbackPeriodInDays,
        account_scope: AccountScope | None = None,
        next_page_token: NextPageToken | None = None,
        page_size: NonNegativeInteger | None = None,
        filter: Expression | None = None,
        **kwargs,
    ) -> GetSavingsPlansPurchaseRecommendationResponse:
        """Retrieves the Savings Plans recommendations for your account. First use
        ``StartSavingsPlansPurchaseRecommendationGeneration`` to generate a new
        set of recommendations, and then use
        ``GetSavingsPlansPurchaseRecommendation`` to retrieve them.

        :param savings_plans_type: The Savings Plans recommendation type that's requested.
        :param term_in_years: The savings plan recommendation term that's used to generate these
        recommendations.
        :param payment_option: The payment option that's used to generate these recommendations.
        :param lookback_period_in_days: The lookback period that's used to generate the recommendation.
        :param account_scope: The account scope that you want your recommendations for.
        :param next_page_token: The token to retrieve the next set of results.
        :param page_size: The number of recommendations that you want returned in a single
        response object.
        :param filter: You can filter your recommendations by Account ID with the
        ``LINKED_ACCOUNT`` dimension.
        :returns: GetSavingsPlansPurchaseRecommendationResponse
        :raises LimitExceededException:
        :raises InvalidNextTokenException:
        """
        raise NotImplementedError

    @handler("GetSavingsPlansUtilization")
    def get_savings_plans_utilization(
        self,
        context: RequestContext,
        time_period: DateInterval,
        granularity: Granularity | None = None,
        filter: Expression | None = None,
        sort_by: SortDefinition | None = None,
        **kwargs,
    ) -> GetSavingsPlansUtilizationResponse:
        """Retrieves the Savings Plans utilization for your account across date
        ranges with daily or monthly granularity. Management account in an
        organization have access to member accounts. You can use
        ``GetDimensionValues`` in ``SAVINGS_PLANS`` to determine the possible
        dimension values.

        You can't group by any dimension values for
        ``GetSavingsPlansUtilization``.

        :param time_period: The time period that you want the usage and costs for.
        :param granularity: The granularity of the Amazon Web Services utillization data for your
        Savings Plans.
        :param filter: Filters Savings Plans utilization coverage data for active Savings Plans
        dimensions.
        :param sort_by: The value that you want to sort the data by.
        :returns: GetSavingsPlansUtilizationResponse
        :raises LimitExceededException:
        :raises DataUnavailableException:
        """
        raise NotImplementedError

    @handler("GetSavingsPlansUtilizationDetails")
    def get_savings_plans_utilization_details(
        self,
        context: RequestContext,
        time_period: DateInterval,
        filter: Expression | None = None,
        data_type: SavingsPlansDataTypes | None = None,
        next_token: NextPageToken | None = None,
        max_results: MaxResults | None = None,
        sort_by: SortDefinition | None = None,
        **kwargs,
    ) -> GetSavingsPlansUtilizationDetailsResponse:
        """Retrieves attribute data along with aggregate utilization and savings
        data for a given time period. This doesn't support granular or grouped
        data (daily/monthly) in response. You can't retrieve data by dates in a
        single response similar to ``GetSavingsPlanUtilization``, but you have
        the option to make multiple calls to
        ``GetSavingsPlanUtilizationDetails`` by providing individual dates. You
        can use ``GetDimensionValues`` in ``SAVINGS_PLANS`` to determine the
        possible dimension values.

        ``GetSavingsPlanUtilizationDetails`` internally groups data by
        ``SavingsPlansArn``.

        :param time_period: The time period that you want the usage and costs for.
        :param filter: Filters Savings Plans utilization coverage data for active Savings Plans
        dimensions.
        :param data_type: The data type.
        :param next_token: The token to retrieve the next set of results.
        :param max_results: The number of items to be returned in a response.
        :param sort_by: The value that you want to sort the data by.
        :returns: GetSavingsPlansUtilizationDetailsResponse
        :raises LimitExceededException:
        :raises DataUnavailableException:
        :raises InvalidNextTokenException:
        """
        raise NotImplementedError

    @handler("GetTags")
    def get_tags(
        self,
        context: RequestContext,
        time_period: DateInterval,
        search_string: SearchString | None = None,
        tag_key: TagKey | None = None,
        filter: Expression | None = None,
        sort_by: SortDefinitions | None = None,
        billing_view_arn: BillingViewArn | None = None,
        max_results: MaxResults | None = None,
        next_page_token: NextPageToken | None = None,
        **kwargs,
    ) -> GetTagsResponse:
        """Queries for available tag keys and tag values for a specified period.
        You can search the tag values for an arbitrary string.

        :param time_period: The start and end dates for retrieving the dimension values.
        :param search_string: The value that you want to search for.
        :param tag_key: The key of the tag that you want to return values for.
        :param filter: Use ``Expression`` to filter in various Cost Explorer APIs.
        :param sort_by: The value that you want to sort the data by.
        :param billing_view_arn: The Amazon Resource Name (ARN) that uniquely identifies a specific
        billing view.
        :param max_results: This field is only used when SortBy is provided in the request.
        :param next_page_token: The token to retrieve the next set of results.
        :returns: GetTagsResponse
        :raises LimitExceededException:
        :raises BillExpirationException:
        :raises DataUnavailableException:
        :raises InvalidNextTokenException:
        :raises RequestChangedException:
        :raises ResourceNotFoundException:
        :raises BillingViewHealthStatusException:
        """
        raise NotImplementedError

    @handler("GetUsageForecast")
    def get_usage_forecast(
        self,
        context: RequestContext,
        time_period: DateInterval,
        metric: Metric,
        granularity: Granularity,
        filter: Expression | None = None,
        billing_view_arn: BillingViewArn | None = None,
        prediction_interval_level: PredictionIntervalLevel | None = None,
        **kwargs,
    ) -> GetUsageForecastResponse:
        """Retrieves a forecast for how much Amazon Web Services predicts that you
        will use over the forecast time period that you select, based on your
        past usage.

        :param time_period: The start and end dates of the period that you want to retrieve usage
        forecast for.
        :param metric: Which metric Cost Explorer uses to create your forecast.
        :param granularity: How granular you want the forecast to be.
        :param filter: The filters that you want to use to filter your forecast.
        :param billing_view_arn: The Amazon Resource Name (ARN) that uniquely identifies a specific
        billing view.
        :param prediction_interval_level: Amazon Web Services Cost Explorer always returns the mean forecast as a
        single point.
        :returns: GetUsageForecastResponse
        :raises LimitExceededException:
        :raises DataUnavailableException:
        :raises UnresolvableUsageUnitException:
        :raises ResourceNotFoundException:
        :raises BillingViewHealthStatusException:
        """
        raise NotImplementedError

    @handler("ListCommitmentPurchaseAnalyses")
    def list_commitment_purchase_analyses(
        self,
        context: RequestContext,
        analysis_status: AnalysisStatus | None = None,
        next_page_token: NextPageToken | None = None,
        page_size: NonNegativeInteger | None = None,
        analysis_ids: AnalysisIds | None = None,
        **kwargs,
    ) -> ListCommitmentPurchaseAnalysesResponse:
        """Lists the commitment purchase analyses for your account.

        :param analysis_status: The status of the analysis.
        :param next_page_token: The token to retrieve the next set of results.
        :param page_size: The number of analyses that you want returned in a single response
        object.
        :param analysis_ids: The analysis IDs associated with the commitment purchase analyses.
        :returns: ListCommitmentPurchaseAnalysesResponse
        :raises LimitExceededException:
        :raises InvalidNextTokenException:
        :raises DataUnavailableException:
        """
        raise NotImplementedError

    @handler("ListCostAllocationTagBackfillHistory")
    def list_cost_allocation_tag_backfill_history(
        self,
        context: RequestContext,
        next_token: NextPageToken | None = None,
        max_results: CostAllocationTagsMaxResults | None = None,
        **kwargs,
    ) -> ListCostAllocationTagBackfillHistoryResponse:
        """Retrieves a list of your historical cost allocation tag backfill
        requests.

        :param next_token: The token to retrieve the next set of results.
        :param max_results: The maximum number of objects that are returned for this request.
        :returns: ListCostAllocationTagBackfillHistoryResponse
        :raises LimitExceededException:
        :raises InvalidNextTokenException:
        """
        raise NotImplementedError

    @handler("ListCostAllocationTags", expand=False)
    def list_cost_allocation_tags(
        self, context: RequestContext, request: ListCostAllocationTagsRequest, **kwargs
    ) -> ListCostAllocationTagsResponse:
        """Get a list of cost allocation tags. All inputs in the API are optional
        and serve as filters. By default, all cost allocation tags are returned.

        :param status: The status of cost allocation tag keys that are returned for this
        request.
        :param tag_keys: The list of cost allocation tag keys that are returned for this request.
        :param type: The type of ``CostAllocationTag`` object that are returned for this
        request.
        :param next_token: The token to retrieve the next set of results.
        :param max_results: The maximum number of objects that are returned for this request.
        :returns: ListCostAllocationTagsResponse
        :raises LimitExceededException:
        :raises InvalidNextTokenException:
        """
        raise NotImplementedError

    @handler("ListCostCategoryDefinitions")
    def list_cost_category_definitions(
        self,
        context: RequestContext,
        effective_on: ZonedDateTime | None = None,
        next_token: NextPageToken | None = None,
        max_results: CostCategoryMaxResults | None = None,
        **kwargs,
    ) -> ListCostCategoryDefinitionsResponse:
        """Returns the name, Amazon Resource Name (ARN), ``NumberOfRules`` and
        effective dates of all Cost Categories defined in the account. You have
        the option to use ``EffectiveOn`` to return a list of Cost Categories
        that were active on a specific date. If there is no ``EffectiveOn``
        specified, you’ll see Cost Categories that are effective on the current
        date. If Cost Category is still effective, ``EffectiveEnd`` is omitted
        in the response. ``ListCostCategoryDefinitions`` supports pagination.
        The request can have a ``MaxResults`` range up to 100.

        :param effective_on: The date when the Cost Category was effective.
        :param next_token: The token to retrieve the next set of results.
        :param max_results: The number of entries a paginated response contains.
        :returns: ListCostCategoryDefinitionsResponse
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("ListSavingsPlansPurchaseRecommendationGeneration")
    def list_savings_plans_purchase_recommendation_generation(
        self,
        context: RequestContext,
        generation_status: GenerationStatus | None = None,
        recommendation_ids: RecommendationIdList | None = None,
        page_size: NonNegativeInteger | None = None,
        next_page_token: NextPageToken | None = None,
        **kwargs,
    ) -> ListSavingsPlansPurchaseRecommendationGenerationResponse:
        """Retrieves a list of your historical recommendation generations within
        the past 30 days.

        :param generation_status: The status of the recommendation generation.
        :param recommendation_ids: The IDs for each specific recommendation.
        :param page_size: The number of recommendations that you want returned in a single
        response object.
        :param next_page_token: The token to retrieve the next set of results.
        :returns: ListSavingsPlansPurchaseRecommendationGenerationResponse
        :raises LimitExceededException:
        :raises InvalidNextTokenException:
        :raises DataUnavailableException:
        """
        raise NotImplementedError

    @handler("ListTagsForResource")
    def list_tags_for_resource(
        self, context: RequestContext, resource_arn: Arn, **kwargs
    ) -> ListTagsForResourceResponse:
        """Returns a list of resource tags associated with the resource specified
        by the Amazon Resource Name (ARN).

        :param resource_arn: The Amazon Resource Name (ARN) of the resource.
        :returns: ListTagsForResourceResponse
        :raises ResourceNotFoundException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("ProvideAnomalyFeedback")
    def provide_anomaly_feedback(
        self,
        context: RequestContext,
        anomaly_id: GenericString,
        feedback: AnomalyFeedbackType,
        **kwargs,
    ) -> ProvideAnomalyFeedbackResponse:
        """Modifies the feedback property of a given cost anomaly.

        :param anomaly_id: A cost anomaly ID.
        :param feedback: Describes whether the cost anomaly was a planned activity or you
        considered it an anomaly.
        :returns: ProvideAnomalyFeedbackResponse
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("StartCommitmentPurchaseAnalysis")
    def start_commitment_purchase_analysis(
        self,
        context: RequestContext,
        commitment_purchase_analysis_configuration: CommitmentPurchaseAnalysisConfiguration,
        **kwargs,
    ) -> StartCommitmentPurchaseAnalysisResponse:
        """Specifies the parameters of a planned commitment purchase and starts the
        generation of the analysis. This enables you to estimate the cost,
        coverage, and utilization impact of your planned commitment purchases.

        :param commitment_purchase_analysis_configuration: The configuration for the commitment purchase analysis.
        :returns: StartCommitmentPurchaseAnalysisResponse
        :raises LimitExceededException:
        :raises ServiceQuotaExceededException:
        :raises DataUnavailableException:
        :raises GenerationExistsException:
        """
        raise NotImplementedError

    @handler("StartCostAllocationTagBackfill")
    def start_cost_allocation_tag_backfill(
        self, context: RequestContext, backfill_from: ZonedDateTime, **kwargs
    ) -> StartCostAllocationTagBackfillResponse:
        """Request a cost allocation tag backfill. This will backfill the
        activation status (either ``active`` or ``inactive``) for all tag keys
        from ``para:BackfillFrom`` up to the time this request is made.

        You can request a backfill once every 24 hours.

        :param backfill_from: The date you want the backfill to start from.
        :returns: StartCostAllocationTagBackfillResponse
        :raises LimitExceededException:
        :raises BackfillLimitExceededException:
        """
        raise NotImplementedError

    @handler("StartSavingsPlansPurchaseRecommendationGeneration")
    def start_savings_plans_purchase_recommendation_generation(
        self, context: RequestContext, **kwargs
    ) -> StartSavingsPlansPurchaseRecommendationGenerationResponse:
        """Requests a Savings Plans recommendation generation. This enables you to
        calculate a fresh set of Savings Plans recommendations that takes your
        latest usage data and current Savings Plans inventory into account. You
        can refresh Savings Plans recommendations up to three times daily for a
        consolidated billing family.

        ``StartSavingsPlansPurchaseRecommendationGeneration`` has no request
        syntax because no input parameters are needed to support this operation.

        :returns: StartSavingsPlansPurchaseRecommendationGenerationResponse
        :raises LimitExceededException:
        :raises ServiceQuotaExceededException:
        :raises GenerationExistsException:
        :raises DataUnavailableException:
        """
        raise NotImplementedError

    @handler("TagResource")
    def tag_resource(
        self, context: RequestContext, resource_arn: Arn, resource_tags: ResourceTagList, **kwargs
    ) -> TagResourceResponse:
        """An API operation for adding one or more tags (key-value pairs) to a
        resource.

        You can use the ``TagResource`` operation with a resource that already
        has tags. If you specify a new tag key for the resource, this tag is
        appended to the list of tags associated with the resource. If you
        specify a tag key that is already associated with the resource, the new
        tag value you specify replaces the previous value for that tag.

        Although the maximum number of array members is 200, user-tag maximum is
        50. The remaining are reserved for Amazon Web Services use.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource.
        :param resource_tags: A list of tag key-value pairs to be added to the resource.
        :returns: TagResourceResponse
        :raises ResourceNotFoundException:
        :raises TooManyTagsException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("UntagResource")
    def untag_resource(
        self,
        context: RequestContext,
        resource_arn: Arn,
        resource_tag_keys: ResourceTagKeyList,
        **kwargs,
    ) -> UntagResourceResponse:
        """Removes one or more tags from a resource. Specify only tag keys in your
        request. Don't specify the value.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource.
        :param resource_tag_keys: A list of tag keys associated with tags that need to be removed from the
        resource.
        :returns: UntagResourceResponse
        :raises ResourceNotFoundException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("UpdateAnomalyMonitor")
    def update_anomaly_monitor(
        self,
        context: RequestContext,
        monitor_arn: GenericString,
        monitor_name: GenericString | None = None,
        **kwargs,
    ) -> UpdateAnomalyMonitorResponse:
        """Updates an existing cost anomaly monitor. The changes made are applied
        going forward, and doesn't change anomalies detected in the past.

        :param monitor_arn: Cost anomaly monitor Amazon Resource Names (ARNs).
        :param monitor_name: The new name for the cost anomaly monitor.
        :returns: UpdateAnomalyMonitorResponse
        :raises LimitExceededException:
        :raises UnknownMonitorException:
        """
        raise NotImplementedError

    @handler("UpdateAnomalySubscription")
    def update_anomaly_subscription(
        self,
        context: RequestContext,
        subscription_arn: GenericString,
        threshold: NullableNonNegativeDouble | None = None,
        frequency: AnomalySubscriptionFrequency | None = None,
        monitor_arn_list: MonitorArnList | None = None,
        subscribers: Subscribers | None = None,
        subscription_name: GenericString | None = None,
        threshold_expression: Expression | None = None,
        **kwargs,
    ) -> UpdateAnomalySubscriptionResponse:
        """Updates an existing cost anomaly subscription. Specify the fields that
        you want to update. Omitted fields are unchanged.

        The JSON below describes the generic construct for each type. See
        `Request
        Parameters <https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_UpdateAnomalySubscription.html#API_UpdateAnomalySubscription_RequestParameters>`__
        for possible values as they apply to ``AnomalySubscription``.

        :param subscription_arn: A cost anomaly subscription Amazon Resource Name (ARN).
        :param threshold: (deprecated)

        The update to the threshold value for receiving notifications.
        :param frequency: The update to the frequency value that subscribers receive
        notifications.
        :param monitor_arn_list: A list of cost anomaly monitor ARNs.
        :param subscribers: The update to the subscriber list.
        :param subscription_name: The new name of the subscription.
        :param threshold_expression: The update to the
        `Expression <https://docs.
        :returns: UpdateAnomalySubscriptionResponse
        :raises LimitExceededException:
        :raises UnknownMonitorException:
        :raises UnknownSubscriptionException:
        """
        raise NotImplementedError

    @handler("UpdateCostAllocationTagsStatus")
    def update_cost_allocation_tags_status(
        self,
        context: RequestContext,
        cost_allocation_tags_status: CostAllocationTagStatusList,
        **kwargs,
    ) -> UpdateCostAllocationTagsStatusResponse:
        """Updates status for cost allocation tags in bulk, with maximum batch size
        of 20. If the tag status that's updated is the same as the existing tag
        status, the request doesn't fail. Instead, it doesn't have any effect on
        the tag status (for example, activating the active tag).

        :param cost_allocation_tags_status: The list of ``CostAllocationTagStatusEntry`` objects that are used to
        update cost allocation tags status for this request.
        :returns: UpdateCostAllocationTagsStatusResponse
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("UpdateCostCategoryDefinition")
    def update_cost_category_definition(
        self,
        context: RequestContext,
        cost_category_arn: Arn,
        rule_version: CostCategoryRuleVersion,
        rules: CostCategoryRulesList,
        effective_start: ZonedDateTime | None = None,
        default_value: CostCategoryValue | None = None,
        split_charge_rules: CostCategorySplitChargeRulesList | None = None,
        **kwargs,
    ) -> UpdateCostCategoryDefinitionResponse:
        """Updates an existing Cost Category. Changes made to the Cost Category
        rules will be used to categorize the current month’s expenses and future
        expenses. This won’t change categorization for the previous months.

        :param cost_category_arn: The unique identifier for your Cost Category.
        :param rule_version: The rule schema version in this particular Cost Category.
        :param rules: The ``Expression`` object used to categorize costs.
        :param effective_start: The Cost Category's effective start date.
        :param default_value: The default value for the cost category.
        :param split_charge_rules: The split charge rules used to allocate your charges between your Cost
        Category values.
        :returns: UpdateCostCategoryDefinitionResponse
        :raises ResourceNotFoundException:
        :raises ServiceQuotaExceededException:
        :raises LimitExceededException:
        """
        raise NotImplementedError
