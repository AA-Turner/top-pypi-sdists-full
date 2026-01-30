from collections.abc import Iterable, Iterator
from datetime import datetime
from enum import StrEnum
from typing import IO, TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

AccountId = str
AsyncInvokeArn = str
AsyncInvokeIdempotencyToken = str
AsyncInvokeIdentifier = str
AsyncInvokeMessage = str
AutomatedReasoningRuleIdentifier = str
Boolean = bool
CacheDetailInputTokensInteger = int
ConversationalModelId = str
ConverseRequestAdditionalModelResponseFieldPathsListMemberString = str
ConverseStreamRequestAdditionalModelResponseFieldPathsListMemberString = str
DocumentBlockNameString = str
DocumentCharLocationDocumentIndexInteger = int
DocumentCharLocationEndInteger = int
DocumentCharLocationStartInteger = int
DocumentChunkLocationDocumentIndexInteger = int
DocumentChunkLocationEndInteger = int
DocumentChunkLocationStartInteger = int
DocumentPageLocationDocumentIndexInteger = int
DocumentPageLocationEndInteger = int
DocumentPageLocationStartInteger = int
FoundationModelVersionIdentifier = str
GuardrailArn = str
GuardrailAutomatedReasoningPoliciesProcessed = int
GuardrailAutomatedReasoningPolicyUnitsProcessed = int
GuardrailAutomatedReasoningPolicyVersionArn = str
GuardrailAutomatedReasoningStatementLogicContent = str
GuardrailAutomatedReasoningStatementNaturalLanguageContent = str
GuardrailAutomatedReasoningTranslationConfidence = float
GuardrailContentPolicyImageUnitsProcessed = int
GuardrailContentPolicyUnitsProcessed = int
GuardrailContextualGroundingFilterScoreDouble = float
GuardrailContextualGroundingFilterThresholdDouble = float
GuardrailContextualGroundingPolicyUnitsProcessed = int
GuardrailId = str
GuardrailIdentifier = str
GuardrailOutputText = str
GuardrailSensitiveInformationPolicyFreeUnitsProcessed = int
GuardrailSensitiveInformationPolicyUnitsProcessed = int
GuardrailTopicPolicyUnitsProcessed = int
GuardrailVersion = str
GuardrailWordPolicyUnitsProcessed = int
ImagesGuarded = int
ImagesTotal = int
InferenceConfigurationMaxTokensInteger = int
InferenceConfigurationTemperatureFloat = float
InferenceConfigurationTopPFloat = float
Integer = int
InvocationArn = str
InvokeModelIdentifier = str
InvokedModelId = str
KmsKeyId = str
MaxResults = int
MimeType = str
NonBlankString = str
NonEmptyString = str
NonNegativeInteger = int
PaginationToken = str
RequestMetadataKeyString = str
RequestMetadataValueString = str
S3Uri = str
SearchResultLocationEndInteger = int
SearchResultLocationSearchResultIndexInteger = int
SearchResultLocationStartInteger = int
StatusCode = int
String = str
TagKey = str
TagValue = str
TextCharactersGuarded = int
TextCharactersTotal = int
TokenUsageCacheReadInputTokensInteger = int
TokenUsageCacheWriteInputTokensInteger = int
TokenUsageInputTokensInteger = int
TokenUsageOutputTokensInteger = int
TokenUsageTotalTokensInteger = int
ToolName = str
ToolUseId = str


class AsyncInvokeStatus(StrEnum):
    InProgress = "InProgress"
    Completed = "Completed"
    Failed = "Failed"


class AudioFormat(StrEnum):
    mp3 = "mp3"
    opus = "opus"
    wav = "wav"
    aac = "aac"
    flac = "flac"
    mp4 = "mp4"
    ogg = "ogg"
    mkv = "mkv"
    mka = "mka"
    x_aac = "x-aac"
    m4a = "m4a"
    mpeg = "mpeg"
    mpga = "mpga"
    pcm = "pcm"
    webm = "webm"


class CachePointType(StrEnum):
    default = "default"


class CacheTTL(StrEnum):
    i_5m = "5m"
    i_1h = "1h"


class ConversationRole(StrEnum):
    user = "user"
    assistant = "assistant"


class DocumentFormat(StrEnum):
    pdf = "pdf"
    csv = "csv"
    doc = "doc"
    docx = "docx"
    xls = "xls"
    xlsx = "xlsx"
    html = "html"
    txt = "txt"
    md = "md"


class GuardrailAction(StrEnum):
    NONE = "NONE"
    GUARDRAIL_INTERVENED = "GUARDRAIL_INTERVENED"


class GuardrailAutomatedReasoningLogicWarningType(StrEnum):
    ALWAYS_FALSE = "ALWAYS_FALSE"
    ALWAYS_TRUE = "ALWAYS_TRUE"


class GuardrailContentFilterConfidence(StrEnum):
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class GuardrailContentFilterStrength(StrEnum):
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class GuardrailContentFilterType(StrEnum):
    INSULTS = "INSULTS"
    HATE = "HATE"
    SEXUAL = "SEXUAL"
    VIOLENCE = "VIOLENCE"
    MISCONDUCT = "MISCONDUCT"
    PROMPT_ATTACK = "PROMPT_ATTACK"


class GuardrailContentPolicyAction(StrEnum):
    BLOCKED = "BLOCKED"
    NONE = "NONE"


class GuardrailContentQualifier(StrEnum):
    grounding_source = "grounding_source"
    query = "query"
    guard_content = "guard_content"


class GuardrailContentSource(StrEnum):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"


class GuardrailContextualGroundingFilterType(StrEnum):
    GROUNDING = "GROUNDING"
    RELEVANCE = "RELEVANCE"


class GuardrailContextualGroundingPolicyAction(StrEnum):
    BLOCKED = "BLOCKED"
    NONE = "NONE"


class GuardrailConverseContentQualifier(StrEnum):
    grounding_source = "grounding_source"
    query = "query"
    guard_content = "guard_content"


class GuardrailConverseImageFormat(StrEnum):
    png = "png"
    jpeg = "jpeg"


class GuardrailImageFormat(StrEnum):
    png = "png"
    jpeg = "jpeg"


class GuardrailManagedWordType(StrEnum):
    PROFANITY = "PROFANITY"


class GuardrailOrigin(StrEnum):
    REQUEST = "REQUEST"
    ACCOUNT_ENFORCED = "ACCOUNT_ENFORCED"
    ORGANIZATION_ENFORCED = "ORGANIZATION_ENFORCED"


class GuardrailOutputScope(StrEnum):
    INTERVENTIONS = "INTERVENTIONS"
    FULL = "FULL"


class GuardrailOwnership(StrEnum):
    SELF = "SELF"
    CROSS_ACCOUNT = "CROSS_ACCOUNT"


class GuardrailPiiEntityType(StrEnum):
    ADDRESS = "ADDRESS"
    AGE = "AGE"
    AWS_ACCESS_KEY = "AWS_ACCESS_KEY"
    AWS_SECRET_KEY = "AWS_SECRET_KEY"
    CA_HEALTH_NUMBER = "CA_HEALTH_NUMBER"
    CA_SOCIAL_INSURANCE_NUMBER = "CA_SOCIAL_INSURANCE_NUMBER"
    CREDIT_DEBIT_CARD_CVV = "CREDIT_DEBIT_CARD_CVV"
    CREDIT_DEBIT_CARD_EXPIRY = "CREDIT_DEBIT_CARD_EXPIRY"
    CREDIT_DEBIT_CARD_NUMBER = "CREDIT_DEBIT_CARD_NUMBER"
    DRIVER_ID = "DRIVER_ID"
    EMAIL = "EMAIL"
    INTERNATIONAL_BANK_ACCOUNT_NUMBER = "INTERNATIONAL_BANK_ACCOUNT_NUMBER"
    IP_ADDRESS = "IP_ADDRESS"
    LICENSE_PLATE = "LICENSE_PLATE"
    MAC_ADDRESS = "MAC_ADDRESS"
    NAME = "NAME"
    PASSWORD = "PASSWORD"
    PHONE = "PHONE"
    PIN = "PIN"
    SWIFT_CODE = "SWIFT_CODE"
    UK_NATIONAL_HEALTH_SERVICE_NUMBER = "UK_NATIONAL_HEALTH_SERVICE_NUMBER"
    UK_NATIONAL_INSURANCE_NUMBER = "UK_NATIONAL_INSURANCE_NUMBER"
    UK_UNIQUE_TAXPAYER_REFERENCE_NUMBER = "UK_UNIQUE_TAXPAYER_REFERENCE_NUMBER"
    URL = "URL"
    USERNAME = "USERNAME"
    US_BANK_ACCOUNT_NUMBER = "US_BANK_ACCOUNT_NUMBER"
    US_BANK_ROUTING_NUMBER = "US_BANK_ROUTING_NUMBER"
    US_INDIVIDUAL_TAX_IDENTIFICATION_NUMBER = "US_INDIVIDUAL_TAX_IDENTIFICATION_NUMBER"
    US_PASSPORT_NUMBER = "US_PASSPORT_NUMBER"
    US_SOCIAL_SECURITY_NUMBER = "US_SOCIAL_SECURITY_NUMBER"
    VEHICLE_IDENTIFICATION_NUMBER = "VEHICLE_IDENTIFICATION_NUMBER"


class GuardrailSensitiveInformationPolicyAction(StrEnum):
    ANONYMIZED = "ANONYMIZED"
    BLOCKED = "BLOCKED"
    NONE = "NONE"


class GuardrailStreamProcessingMode(StrEnum):
    sync = "sync"
    async_ = "async"


class GuardrailTopicPolicyAction(StrEnum):
    BLOCKED = "BLOCKED"
    NONE = "NONE"


class GuardrailTopicType(StrEnum):
    DENY = "DENY"


class GuardrailTrace(StrEnum):
    enabled = "enabled"
    disabled = "disabled"
    enabled_full = "enabled_full"


class GuardrailWordPolicyAction(StrEnum):
    BLOCKED = "BLOCKED"
    NONE = "NONE"


class ImageFormat(StrEnum):
    png = "png"
    jpeg = "jpeg"
    gif = "gif"
    webp = "webp"


class PerformanceConfigLatency(StrEnum):
    standard = "standard"
    optimized = "optimized"


class ServiceTierType(StrEnum):
    priority = "priority"
    default = "default"
    flex = "flex"
    reserved = "reserved"


class SortAsyncInvocationBy(StrEnum):
    SubmissionTime = "SubmissionTime"


class SortOrder(StrEnum):
    Ascending = "Ascending"
    Descending = "Descending"


class StopReason(StrEnum):
    end_turn = "end_turn"
    tool_use = "tool_use"
    max_tokens = "max_tokens"
    stop_sequence = "stop_sequence"
    guardrail_intervened = "guardrail_intervened"
    content_filtered = "content_filtered"
    malformed_model_output = "malformed_model_output"
    malformed_tool_use = "malformed_tool_use"
    model_context_window_exceeded = "model_context_window_exceeded"


class ToolResultStatus(StrEnum):
    success = "success"
    error = "error"


class ToolUseType(StrEnum):
    server_tool_use = "server_tool_use"


class Trace(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"
    ENABLED_FULL = "ENABLED_FULL"


class VideoFormat(StrEnum):
    mkv = "mkv"
    mov = "mov"
    mp4 = "mp4"
    webm = "webm"
    flv = "flv"
    mpeg = "mpeg"
    mpg = "mpg"
    wmv = "wmv"
    three_gp = "three_gp"


class AccessDeniedException(ServiceException):
    """The request is denied because you do not have sufficient permissions to
    perform the requested action. For troubleshooting this error, see
    `AccessDeniedException <https://docs.aws.amazon.com/bedrock/latest/userguide/troubleshooting-api-error-codes.html#ts-access-denied>`__
    in the Amazon Bedrock User Guide
    """

    code: str = "AccessDeniedException"
    sender_fault: bool = True
    status_code: int = 403


class ConflictException(ServiceException):
    """Error occurred because of a conflict while performing an operation."""

    code: str = "ConflictException"
    sender_fault: bool = True
    status_code: int = 400


class InternalServerException(ServiceException):
    """An internal server error occurred. For troubleshooting this error, see
    `InternalFailure <https://docs.aws.amazon.com/bedrock/latest/userguide/troubleshooting-api-error-codes.html#ts-internal-failure>`__
    in the Amazon Bedrock User Guide
    """

    code: str = "InternalServerException"
    sender_fault: bool = False
    status_code: int = 500


class ModelErrorException(ServiceException):
    """The request failed due to an error while processing the model."""

    code: str = "ModelErrorException"
    sender_fault: bool = True
    status_code: int = 424
    originalStatusCode: StatusCode | None
    resourceName: NonBlankString | None


class ModelNotReadyException(ServiceException):
    """The model specified in the request is not ready to serve inference
    requests. The AWS SDK will automatically retry the operation up to 5
    times. For information about configuring automatic retries, see `Retry
    behavior <https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html>`__
    in the *AWS SDKs and Tools* reference guide.
    """

    code: str = "ModelNotReadyException"
    sender_fault: bool = True
    status_code: int = 429


class ModelStreamErrorException(ServiceException):
    """An error occurred while streaming the response. Retry your request."""

    code: str = "ModelStreamErrorException"
    sender_fault: bool = True
    status_code: int = 424
    originalStatusCode: StatusCode | None
    originalMessage: NonBlankString | None


class ModelTimeoutException(ServiceException):
    """The request took too long to process. Processing time exceeded the model
    timeout length.
    """

    code: str = "ModelTimeoutException"
    sender_fault: bool = True
    status_code: int = 408


class ResourceNotFoundException(ServiceException):
    """The specified resource ARN was not found. For troubleshooting this
    error, see
    `ResourceNotFound <https://docs.aws.amazon.com/bedrock/latest/userguide/troubleshooting-api-error-codes.html#ts-resource-not-found>`__
    in the Amazon Bedrock User Guide
    """

    code: str = "ResourceNotFoundException"
    sender_fault: bool = True
    status_code: int = 404


class ServiceQuotaExceededException(ServiceException):
    """Your request exceeds the service quota for your account. You can view
    your quotas at `Viewing service
    quotas <https://docs.aws.amazon.com/servicequotas/latest/userguide/gs-request-quota.html>`__.
    You can resubmit your request later.
    """

    code: str = "ServiceQuotaExceededException"
    sender_fault: bool = True
    status_code: int = 400


class ServiceUnavailableException(ServiceException):
    """The service isn't currently available. For troubleshooting this error,
    see
    `ServiceUnavailable <https://docs.aws.amazon.com/bedrock/latest/userguide/troubleshooting-api-error-codes.html#ts-service-unavailable>`__
    in the Amazon Bedrock User Guide
    """

    code: str = "ServiceUnavailableException"
    sender_fault: bool = False
    status_code: int = 503


class ThrottlingException(ServiceException):
    """Your request was denied due to exceeding the account quotas for *Amazon
    Bedrock*. For troubleshooting this error, see
    `ThrottlingException <https://docs.aws.amazon.com/bedrock/latest/userguide/troubleshooting-api-error-codes.html#ts-throttling-exception>`__
    in the Amazon Bedrock User Guide
    """

    code: str = "ThrottlingException"
    sender_fault: bool = True
    status_code: int = 429


class ValidationException(ServiceException):
    """The input fails to satisfy the constraints specified by *Amazon
    Bedrock*. For troubleshooting this error, see
    `ValidationError <https://docs.aws.amazon.com/bedrock/latest/userguide/troubleshooting-api-error-codes.html#ts-validation-error>`__
    in the Amazon Bedrock User Guide
    """

    code: str = "ValidationException"
    sender_fault: bool = True
    status_code: int = 400


class AnyToolChoice(TypedDict, total=False):
    """The model must request at least one tool (no text is generated). For
    example, ``{"any" : {}}``. For more information, see `Call a tool with
    the Converse
    API <https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html>`__
    in the Amazon Bedrock User Guide.
    """

    pass


GuardrailOriginList = list[GuardrailOrigin]


class AppliedGuardrailDetails(TypedDict, total=False):
    """Details about the specific guardrail that was applied during this
    assessment, including its identifier, version, ARN, origin, and
    ownership information.
    """

    guardrailId: GuardrailId | None
    guardrailVersion: GuardrailVersion | None
    guardrailArn: GuardrailArn | None
    guardrailOrigin: GuardrailOriginList | None
    guardrailOwnership: GuardrailOwnership | None


GuardrailImageSourceBytesBlob = bytes


class GuardrailImageSource(TypedDict, total=False):
    """The image source (image bytes) of the guardrail image source. Object
    used in independent api.
    """

    bytes: GuardrailImageSourceBytesBlob | None


class GuardrailImageBlock(TypedDict, total=False):
    """Contain an image which user wants guarded. This block is accepted by the
    guardrails independent API.
    """

    format: GuardrailImageFormat
    source: GuardrailImageSource


GuardrailContentQualifierList = list[GuardrailContentQualifier]


class GuardrailTextBlock(TypedDict, total=False):
    """The text block to be evaluated by the guardrail."""

    text: String
    qualifiers: GuardrailContentQualifierList | None


class GuardrailContentBlock(TypedDict, total=False):
    """The content block to be evaluated by the guardrail."""

    text: GuardrailTextBlock | None
    image: GuardrailImageBlock | None


GuardrailContentBlockList = list[GuardrailContentBlock]


class ApplyGuardrailRequest(ServiceRequest):
    guardrailIdentifier: GuardrailIdentifier
    guardrailVersion: GuardrailVersion
    source: GuardrailContentSource
    content: GuardrailContentBlockList
    outputScope: GuardrailOutputScope | None


class GuardrailImageCoverage(TypedDict, total=False):
    """The details of the guardrail image coverage."""

    guarded: ImagesGuarded | None
    total: ImagesTotal | None


class GuardrailTextCharactersCoverage(TypedDict, total=False):
    """The guardrail coverage for the text characters."""

    guarded: TextCharactersGuarded | None
    total: TextCharactersTotal | None


class GuardrailCoverage(TypedDict, total=False):
    """The action of the guardrail coverage details."""

    textCharacters: GuardrailTextCharactersCoverage | None
    images: GuardrailImageCoverage | None


class GuardrailUsage(TypedDict, total=False):
    """The details on the use of the guardrail."""

    topicPolicyUnits: GuardrailTopicPolicyUnitsProcessed
    contentPolicyUnits: GuardrailContentPolicyUnitsProcessed
    wordPolicyUnits: GuardrailWordPolicyUnitsProcessed
    sensitiveInformationPolicyUnits: GuardrailSensitiveInformationPolicyUnitsProcessed
    sensitiveInformationPolicyFreeUnits: GuardrailSensitiveInformationPolicyFreeUnitsProcessed
    contextualGroundingPolicyUnits: GuardrailContextualGroundingPolicyUnitsProcessed
    contentPolicyImageUnits: GuardrailContentPolicyImageUnitsProcessed | None
    automatedReasoningPolicyUnits: GuardrailAutomatedReasoningPolicyUnitsProcessed | None
    automatedReasoningPolicies: GuardrailAutomatedReasoningPoliciesProcessed | None


GuardrailProcessingLatency = int


class GuardrailInvocationMetrics(TypedDict, total=False):
    """The invocation metrics for the guardrail."""

    guardrailProcessingLatency: GuardrailProcessingLatency | None
    usage: GuardrailUsage | None
    guardrailCoverage: GuardrailCoverage | None


class GuardrailAutomatedReasoningNoTranslationsFinding(TypedDict, total=False):
    """Indicates that no relevant logical information could be extracted from
    the input for validation.
    """

    pass


class GuardrailAutomatedReasoningTooComplexFinding(TypedDict, total=False):
    """Indicates that the input exceeds the processing capacity due to the
    volume or complexity of the logical information.
    """

    pass


class GuardrailAutomatedReasoningStatement(TypedDict, total=False):
    """A logical statement that includes both formal logic representation and
    natural language explanation.
    """

    logic: GuardrailAutomatedReasoningStatementLogicContent | None
    naturalLanguage: GuardrailAutomatedReasoningStatementNaturalLanguageContent | None


GuardrailAutomatedReasoningStatementList = list[GuardrailAutomatedReasoningStatement]


class GuardrailAutomatedReasoningScenario(TypedDict, total=False):
    """Represents a logical scenario where claims can be evaluated as true or
    false, containing specific logical assignments.
    """

    statements: GuardrailAutomatedReasoningStatementList | None


GuardrailAutomatedReasoningDifferenceScenarioList = list[GuardrailAutomatedReasoningScenario]


class GuardrailAutomatedReasoningInputTextReference(TypedDict, total=False):
    """References a portion of the original input text that corresponds to
    logical elements.
    """

    text: GuardrailAutomatedReasoningStatementNaturalLanguageContent | None


GuardrailAutomatedReasoningInputTextReferenceList = list[
    GuardrailAutomatedReasoningInputTextReference
]


class GuardrailAutomatedReasoningTranslation(TypedDict, total=False):
    """Contains the logical translation of natural language input into formal
    logical statements, including premises, claims, and confidence scores.
    """

    premises: GuardrailAutomatedReasoningStatementList | None
    claims: GuardrailAutomatedReasoningStatementList | None
    untranslatedPremises: GuardrailAutomatedReasoningInputTextReferenceList | None
    untranslatedClaims: GuardrailAutomatedReasoningInputTextReferenceList | None
    confidence: GuardrailAutomatedReasoningTranslationConfidence | None


GuardrailAutomatedReasoningTranslationList = list[GuardrailAutomatedReasoningTranslation]


class GuardrailAutomatedReasoningTranslationOption(TypedDict, total=False):
    """Represents one possible logical interpretation of ambiguous input
    content.
    """

    translations: GuardrailAutomatedReasoningTranslationList | None


GuardrailAutomatedReasoningTranslationOptionList = list[
    GuardrailAutomatedReasoningTranslationOption
]


class GuardrailAutomatedReasoningTranslationAmbiguousFinding(TypedDict, total=False):
    """Indicates that the input has multiple valid logical interpretations,
    requiring additional context or clarification.
    """

    options: GuardrailAutomatedReasoningTranslationOptionList | None
    differenceScenarios: GuardrailAutomatedReasoningDifferenceScenarioList | None


class GuardrailAutomatedReasoningLogicWarning(TypedDict, total=False):
    type: GuardrailAutomatedReasoningLogicWarningType | None
    premises: GuardrailAutomatedReasoningStatementList | None
    claims: GuardrailAutomatedReasoningStatementList | None


class GuardrailAutomatedReasoningRule(TypedDict, total=False):
    """References a specific automated reasoning policy rule that was applied
    during evaluation.
    """

    identifier: AutomatedReasoningRuleIdentifier | None
    policyVersionArn: GuardrailAutomatedReasoningPolicyVersionArn | None


GuardrailAutomatedReasoningRuleList = list[GuardrailAutomatedReasoningRule]


class GuardrailAutomatedReasoningImpossibleFinding(TypedDict, total=False):
    """Indicates that no valid claims can be made due to logical contradictions
    in the premises or rules.
    """

    translation: GuardrailAutomatedReasoningTranslation | None
    contradictingRules: GuardrailAutomatedReasoningRuleList | None
    logicWarning: GuardrailAutomatedReasoningLogicWarning | None


class GuardrailAutomatedReasoningSatisfiableFinding(TypedDict, total=False):
    """Indicates that the claims could be either true or false depending on
    additional assumptions not provided in the input.
    """

    translation: GuardrailAutomatedReasoningTranslation | None
    claimsTrueScenario: GuardrailAutomatedReasoningScenario | None
    claimsFalseScenario: GuardrailAutomatedReasoningScenario | None
    logicWarning: GuardrailAutomatedReasoningLogicWarning | None


class GuardrailAutomatedReasoningInvalidFinding(TypedDict, total=False):
    """Indicates that the claims are logically false and contradictory to the
    established rules or premises.
    """

    translation: GuardrailAutomatedReasoningTranslation | None
    contradictingRules: GuardrailAutomatedReasoningRuleList | None
    logicWarning: GuardrailAutomatedReasoningLogicWarning | None


class GuardrailAutomatedReasoningValidFinding(TypedDict, total=False):
    """Indicates that the claims are definitively true and logically implied by
    the premises, with no possible alternative interpretations.
    """

    translation: GuardrailAutomatedReasoningTranslation | None
    claimsTrueScenario: GuardrailAutomatedReasoningScenario | None
    supportingRules: GuardrailAutomatedReasoningRuleList | None
    logicWarning: GuardrailAutomatedReasoningLogicWarning | None


class GuardrailAutomatedReasoningFinding(TypedDict, total=False):
    """Represents a logical validation result from automated reasoning policy
    evaluation. The finding indicates whether claims in the input are
    logically valid, invalid, satisfiable, impossible, or have other logical
    issues.
    """

    valid: GuardrailAutomatedReasoningValidFinding | None
    invalid: GuardrailAutomatedReasoningInvalidFinding | None
    satisfiable: GuardrailAutomatedReasoningSatisfiableFinding | None
    impossible: GuardrailAutomatedReasoningImpossibleFinding | None
    translationAmbiguous: GuardrailAutomatedReasoningTranslationAmbiguousFinding | None
    tooComplex: GuardrailAutomatedReasoningTooComplexFinding | None
    noTranslations: GuardrailAutomatedReasoningNoTranslationsFinding | None


GuardrailAutomatedReasoningFindingList = list[GuardrailAutomatedReasoningFinding]


class GuardrailAutomatedReasoningPolicyAssessment(TypedDict, total=False):
    """Contains the results of automated reasoning policy evaluation, including
    logical findings about the validity of claims made in the input content.
    """

    findings: GuardrailAutomatedReasoningFindingList | None


class GuardrailContextualGroundingFilter(TypedDict, total=False):
    type: GuardrailContextualGroundingFilterType
    threshold: GuardrailContextualGroundingFilterThresholdDouble
    score: GuardrailContextualGroundingFilterScoreDouble
    action: GuardrailContextualGroundingPolicyAction
    detected: Boolean | None


GuardrailContextualGroundingFilters = list[GuardrailContextualGroundingFilter]


class GuardrailContextualGroundingPolicyAssessment(TypedDict, total=False):
    """The policy assessment details for the guardrails contextual grounding
    filter.
    """

    filters: GuardrailContextualGroundingFilters | None


class GuardrailRegexFilter(TypedDict, total=False):
    """A Regex filter configured in a guardrail."""

    name: String | None
    match: String | None
    regex: String | None
    action: GuardrailSensitiveInformationPolicyAction
    detected: Boolean | None


GuardrailRegexFilterList = list[GuardrailRegexFilter]


class GuardrailPiiEntityFilter(TypedDict, total=False):
    match: String
    type: GuardrailPiiEntityType
    action: GuardrailSensitiveInformationPolicyAction
    detected: Boolean | None


GuardrailPiiEntityFilterList = list[GuardrailPiiEntityFilter]


class GuardrailSensitiveInformationPolicyAssessment(TypedDict, total=False):
    """The assessment for a Personally Identifiable Information (PII) policy."""

    piiEntities: GuardrailPiiEntityFilterList
    regexes: GuardrailRegexFilterList


class GuardrailManagedWord(TypedDict, total=False):
    match: String
    type: GuardrailManagedWordType
    action: GuardrailWordPolicyAction
    detected: Boolean | None


GuardrailManagedWordList = list[GuardrailManagedWord]


class GuardrailCustomWord(TypedDict, total=False):
    """A custom word configured in a guardrail."""

    match: String
    action: GuardrailWordPolicyAction
    detected: Boolean | None


GuardrailCustomWordList = list[GuardrailCustomWord]


class GuardrailWordPolicyAssessment(TypedDict, total=False):
    """The word policy assessment."""

    customWords: GuardrailCustomWordList
    managedWordLists: GuardrailManagedWordList


class GuardrailContentFilter(TypedDict, total=False):
    type: GuardrailContentFilterType
    confidence: GuardrailContentFilterConfidence
    filterStrength: GuardrailContentFilterStrength | None
    action: GuardrailContentPolicyAction
    detected: Boolean | None


GuardrailContentFilterList = list[GuardrailContentFilter]


class GuardrailContentPolicyAssessment(TypedDict, total=False):
    """An assessment of a content policy for a guardrail."""

    filters: GuardrailContentFilterList


class GuardrailTopic(TypedDict, total=False):
    name: String
    type: GuardrailTopicType
    action: GuardrailTopicPolicyAction
    detected: Boolean | None


GuardrailTopicList = list[GuardrailTopic]


class GuardrailTopicPolicyAssessment(TypedDict, total=False):
    """A behavior assessment of a topic policy."""

    topics: GuardrailTopicList


class GuardrailAssessment(TypedDict, total=False):
    """A behavior assessment of the guardrail policies used in a call to the
    Converse API.
    """

    topicPolicy: GuardrailTopicPolicyAssessment | None
    contentPolicy: GuardrailContentPolicyAssessment | None
    wordPolicy: GuardrailWordPolicyAssessment | None
    sensitiveInformationPolicy: GuardrailSensitiveInformationPolicyAssessment | None
    contextualGroundingPolicy: GuardrailContextualGroundingPolicyAssessment | None
    automatedReasoningPolicy: GuardrailAutomatedReasoningPolicyAssessment | None
    invocationMetrics: GuardrailInvocationMetrics | None
    appliedGuardrailDetails: AppliedGuardrailDetails | None


GuardrailAssessmentList = list[GuardrailAssessment]


class GuardrailOutputContent(TypedDict, total=False):
    """The output content produced by the guardrail."""

    text: GuardrailOutputText | None


GuardrailOutputContentList = list[GuardrailOutputContent]


class ApplyGuardrailResponse(TypedDict, total=False):
    usage: GuardrailUsage
    action: GuardrailAction
    actionReason: String | None
    outputs: GuardrailOutputContentList
    assessments: GuardrailAssessmentList
    guardrailCoverage: GuardrailCoverage | None


class AsyncInvokeS3OutputDataConfig(TypedDict, total=False):
    """Asynchronous invocation output data settings."""

    s3Uri: S3Uri
    kmsKeyId: KmsKeyId | None
    bucketOwner: AccountId | None


class AsyncInvokeOutputDataConfig(TypedDict, total=False):
    """Asynchronous invocation output data settings."""

    s3OutputDataConfig: AsyncInvokeS3OutputDataConfig | None


Timestamp = datetime


class AsyncInvokeSummary(TypedDict, total=False):
    """A summary of an asynchronous invocation."""

    invocationArn: InvocationArn
    modelArn: AsyncInvokeArn
    clientRequestToken: AsyncInvokeIdempotencyToken | None
    status: AsyncInvokeStatus | None
    failureMessage: AsyncInvokeMessage | None
    submitTime: Timestamp
    lastModifiedTime: Timestamp | None
    endTime: Timestamp | None
    outputDataConfig: AsyncInvokeOutputDataConfig


AsyncInvokeSummaries = list[AsyncInvokeSummary]


class ErrorBlock(TypedDict, total=False):
    """A block containing error information when content processing fails."""

    message: String | None


class S3Location(TypedDict, total=False):
    """A storage location in an Amazon S3 bucket."""

    uri: S3Uri
    bucketOwner: AccountId | None


AudioSourceBytesBlob = bytes


class AudioSource(TypedDict, total=False):
    """The source of audio data, which can be provided either as raw bytes or a
    reference to an S3 location.
    """

    bytes: AudioSourceBytesBlob | None
    s3Location: S3Location | None


class AudioBlock(TypedDict, total=False):
    """An audio content block that contains audio data in various supported
    formats.
    """

    format: AudioFormat
    source: AudioSource
    error: ErrorBlock | None


class AutoToolChoice(TypedDict, total=False):
    """The Model automatically decides if a tool should be called or whether to
    generate text instead. For example, ``{"auto" : {}}``. For more
    information, see `Call a tool with the Converse
    API <https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html>`__
    in the Amazon Bedrock User Guide
    """

    pass


PartBody = bytes


class BidirectionalInputPayloadPart(TypedDict, total=False):
    """Payload content for the bidirectional input. The input is an audio
    stream.
    """

    bytes: PartBody | None


class BidirectionalOutputPayloadPart(TypedDict, total=False):
    """Output from the bidirectional stream. The output is speech and a text
    transcription.
    """

    bytes: PartBody | None


Blob = bytes
Body = bytes


class CacheDetail(TypedDict, total=False):
    """Cache creation metrics for a specific TTL duration"""

    ttl: CacheTTL
    inputTokens: CacheDetailInputTokensInteger


CacheDetailsList = list[CacheDetail]


class CachePointBlock(TypedDict, total=False):
    type: CachePointType
    ttl: CacheTTL | None


class SearchResultLocation(TypedDict, total=False):
    """Specifies a search result location within the content array, providing
    positioning information for cited content using search result index and
    block positions.
    """

    searchResultIndex: SearchResultLocationSearchResultIndexInteger | None
    start: SearchResultLocationStartInteger | None
    end: SearchResultLocationEndInteger | None


class DocumentChunkLocation(TypedDict, total=False):
    """Specifies a chunk-level location within a document, providing
    positioning information for cited content using logical document
    segments or chunks.
    """

    documentIndex: DocumentChunkLocationDocumentIndexInteger | None
    start: DocumentChunkLocationStartInteger | None
    end: DocumentChunkLocationEndInteger | None


class DocumentPageLocation(TypedDict, total=False):
    """Specifies a page-level location within a document, providing positioning
    information for cited content using page numbers.
    """

    documentIndex: DocumentPageLocationDocumentIndexInteger | None
    start: DocumentPageLocationStartInteger | None
    end: DocumentPageLocationEndInteger | None


class DocumentCharLocation(TypedDict, total=False):
    """Specifies a character-level location within a document, providing
    precise positioning information for cited content using start and end
    character indices.
    """

    documentIndex: DocumentCharLocationDocumentIndexInteger | None
    start: DocumentCharLocationStartInteger | None
    end: DocumentCharLocationEndInteger | None


class WebLocation(TypedDict, total=False):
    """Provides the URL and domain information for the website that was cited
    when performing a web search.
    """

    url: String | None
    domain: String | None


class CitationLocation(TypedDict, total=False):
    """Specifies the precise location within a source document where cited
    content can be found. This can include character-level positions, page
    numbers, or document chunks depending on the document type and indexing
    method.
    """

    web: WebLocation | None
    documentChar: DocumentCharLocation | None
    documentPage: DocumentPageLocation | None
    documentChunk: DocumentChunkLocation | None
    searchResultLocation: SearchResultLocation | None


class CitationSourceContent(TypedDict, total=False):
    """Contains the actual text content from a source document that is being
    cited or referenced in the model's response.
    """

    text: String | None


CitationSourceContentList = list[CitationSourceContent]


class Citation(TypedDict, total=False):
    """Contains information about a citation that references a specific source
    document. Citations provide traceability between the model's generated
    response and the source documents that informed that response.
    """

    title: String | None
    source: String | None
    sourceContent: CitationSourceContentList | None
    location: CitationLocation | None


class CitationGeneratedContent(TypedDict, total=False):
    """Contains the generated text content that corresponds to or is supported
    by a citation from a source document.
    """

    text: String | None


CitationGeneratedContentList = list[CitationGeneratedContent]


class CitationSourceContentDelta(TypedDict, total=False):
    """Contains incremental updates to the source content text during streaming
    responses, allowing clients to build up the cited content progressively.
    """

    text: String | None


CitationSourceContentListDelta = list[CitationSourceContentDelta]
Citations = list[Citation]


class CitationsConfig(TypedDict, total=False):
    """Configuration settings for enabling and controlling document citations
    in Converse API responses. When enabled, the model can include citation
    information that links generated content back to specific source
    documents.
    """

    enabled: Boolean


class CitationsContentBlock(TypedDict, total=False):
    """A content block that contains both generated text and associated
    citation information. This block type is returned when document
    citations are enabled, providing traceability between the generated
    content and the source documents that informed the response.
    """

    content: CitationGeneratedContentList | None
    citations: Citations | None


class CitationsDelta(TypedDict, total=False):
    """Contains incremental updates to citation information during streaming
    responses. This allows clients to build up citation data progressively
    as the response is generated.
    """

    title: String | None
    source: String | None
    sourceContent: CitationSourceContentListDelta | None
    location: CitationLocation | None


class SearchResultContentBlock(TypedDict, total=False):
    """A block within a search result that contains the content."""

    text: String


SearchResultContentBlocks = list[SearchResultContentBlock]


class SearchResultBlock(TypedDict, total=False):
    """A search result block that enables natural citations with proper source
    attribution for retrieved content.

    This field is only supported by Anthropic Claude Opus 4.1, Opus 4,
    Sonnet 4.5, Sonnet 4, Sonnet 3.7, and 3.5 Haiku models.
    """

    source: String
    title: String
    content: SearchResultContentBlocks
    citations: CitationsConfig | None


class ReasoningTextBlock(TypedDict, total=False):
    """Contains the reasoning that the model used to return the output."""

    text: String
    signature: String | None


class ReasoningContentBlock(TypedDict, total=False):
    """Contains content regarding the reasoning that is carried out by the
    model with respect to the content in the content block. Reasoning refers
    to a Chain of Thought (CoT) that the model generates to enhance the
    accuracy of its final response.
    """

    reasoningText: ReasoningTextBlock | None
    redactedContent: Blob | None


GuardrailConverseImageSourceBytesBlob = bytes


class GuardrailConverseImageSource(TypedDict, total=False):
    """The image source (image bytes) of the guardrail converse image source."""

    bytes: GuardrailConverseImageSourceBytesBlob | None


class GuardrailConverseImageBlock(TypedDict, total=False):
    """An image block that contains images that you want to assess with a
    guardrail.
    """

    format: GuardrailConverseImageFormat
    source: GuardrailConverseImageSource


GuardrailConverseContentQualifierList = list[GuardrailConverseContentQualifier]


class GuardrailConverseTextBlock(TypedDict, total=False):
    """A text block that contains text that you want to assess with a
    guardrail. For more information, see
    `GuardrailConverseContentBlock <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_GuardrailConverseContentBlock.html>`__.
    """

    text: String
    qualifiers: GuardrailConverseContentQualifierList | None


class GuardrailConverseContentBlock(TypedDict, total=False):
    """A content block for selective guarding with the
    `Converse <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html>`__
    or
    `ConverseStream <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html>`__
    API operations.
    """

    text: GuardrailConverseTextBlock | None
    image: GuardrailConverseImageBlock | None


VideoSourceBytesBlob = bytes


class VideoSource(TypedDict, total=False):
    """A video source. You can upload a smaller video as a base64-encoded
    string as long as the encoded file is less than 25MB. You can also
    transfer videos up to 1GB in size from an S3 bucket.
    """

    bytes: VideoSourceBytesBlob | None
    s3Location: S3Location | None


class VideoBlock(TypedDict, total=False):
    """A video block."""

    format: VideoFormat
    source: VideoSource


class DocumentContentBlock(TypedDict, total=False):
    """Contains the actual content of a document that can be processed by the
    model and potentially cited in the response.
    """

    text: String | None


DocumentContentBlocks = list[DocumentContentBlock]
DocumentSourceBytesBlob = bytes


class DocumentSource(TypedDict, total=False):
    """Contains the content of a document."""

    bytes: DocumentSourceBytesBlob | None
    s3Location: S3Location | None
    text: String | None
    content: DocumentContentBlocks | None


class DocumentBlock(TypedDict, total=False):
    """A document to include in a message."""

    format: DocumentFormat | None
    name: DocumentBlockNameString
    source: DocumentSource
    context: String | None
    citations: CitationsConfig | None


ImageSourceBytesBlob = bytes


class ImageSource(TypedDict, total=False):
    """The source for an image."""

    bytes: ImageSourceBytesBlob | None
    s3Location: S3Location | None


class ImageBlock(TypedDict, total=False):
    """Image content for a message."""

    format: ImageFormat
    source: ImageSource
    error: ErrorBlock | None


class Document(TypedDict, total=False):
    pass


class ToolResultContentBlock(TypedDict, total=False):
    """The tool result content block. For more information, see `Call a tool
    with the Converse
    API <https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html>`__
    in the Amazon Bedrock User Guide.
    """

    json: Document | None
    text: String | None
    image: ImageBlock | None
    document: DocumentBlock | None
    video: VideoBlock | None
    searchResult: SearchResultBlock | None


ToolResultContentBlocks = list[ToolResultContentBlock]


class ToolResultBlock(TypedDict, total=False):
    toolUseId: ToolUseId
    content: ToolResultContentBlocks
    status: ToolResultStatus | None
    type: String | None


class ToolUseBlock(TypedDict, total=False):
    toolUseId: ToolUseId
    name: ToolName
    input: Document
    type: ToolUseType | None


class ContentBlock(TypedDict, total=False):
    """A block of content for a message that you pass to, or receive from, a
    model with the
    `Converse <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html>`__
    or
    `ConverseStream <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html>`__
    API operations.
    """

    text: String | None
    image: ImageBlock | None
    document: DocumentBlock | None
    video: VideoBlock | None
    audio: AudioBlock | None
    toolUse: ToolUseBlock | None
    toolResult: ToolResultBlock | None
    guardContent: GuardrailConverseContentBlock | None
    cachePoint: CachePointBlock | None
    reasoningContent: ReasoningContentBlock | None
    citationsContent: CitationsContentBlock | None
    searchResult: SearchResultBlock | None


class ImageBlockDelta(TypedDict, total=False):
    """A streaming delta event that contains incremental image data during
    streaming responses.
    """

    source: ImageSource | None
    error: ErrorBlock | None


class ReasoningContentBlockDelta(TypedDict, total=False):
    """Contains content regarding the reasoning that is carried out by the
    model with respect to the content in the content block. Reasoning refers
    to a Chain of Thought (CoT) that the model generates to enhance the
    accuracy of its final response.
    """

    text: String | None
    redactedContent: Blob | None
    signature: String | None


class ToolResultBlockDelta(TypedDict, total=False):
    """Contains incremental updates to tool results information during
    streaming responses. This allows clients to build up tool results data
    progressively as the response is generated.
    """

    text: String | None
    json: Document | None


ToolResultBlocksDelta = list[ToolResultBlockDelta]


class ToolUseBlockDelta(TypedDict, total=False):
    """The delta for a tool use block."""

    input: String


class ContentBlockDelta(TypedDict, total=False):
    """A block of content in a streaming response."""

    text: String | None
    toolUse: ToolUseBlockDelta | None
    toolResult: ToolResultBlocksDelta | None
    reasoningContent: ReasoningContentBlockDelta | None
    citation: CitationsDelta | None
    image: ImageBlockDelta | None


class ContentBlockDeltaEvent(TypedDict, total=False):
    """The content block delta event."""

    delta: ContentBlockDelta
    contentBlockIndex: NonNegativeInteger


class ImageBlockStart(TypedDict, total=False):
    """The initial event in a streaming image block that indicates the start of
    image content.
    """

    format: ImageFormat


class ToolResultBlockStart(TypedDict, total=False):
    toolUseId: ToolUseId
    type: String | None
    status: ToolResultStatus | None


class ToolUseBlockStart(TypedDict, total=False):
    toolUseId: ToolUseId
    name: ToolName
    type: ToolUseType | None


class ContentBlockStart(TypedDict, total=False):
    """Content block start information."""

    toolUse: ToolUseBlockStart | None
    toolResult: ToolResultBlockStart | None
    image: ImageBlockStart | None


class ContentBlockStartEvent(TypedDict, total=False):
    """Content block start event."""

    start: ContentBlockStart
    contentBlockIndex: NonNegativeInteger


class ContentBlockStopEvent(TypedDict, total=False):
    """A content block stop event."""

    contentBlockIndex: NonNegativeInteger


ContentBlocks = list[ContentBlock]
Long = int


class ConverseMetrics(TypedDict, total=False):
    """Metrics for a call to
    `Converse <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html>`__.
    """

    latencyMs: Long


class Message(TypedDict, total=False):
    """A message input, or returned from, a call to
    `Converse <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html>`__
    or
    `ConverseStream <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html>`__.
    """

    role: ConversationRole
    content: ContentBlocks


class ConverseOutput(TypedDict, total=False):
    """The output from a call to
    `Converse <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html>`__.
    """

    message: Message | None


class ServiceTier(TypedDict, total=False):
    type: ServiceTierType


class PerformanceConfiguration(TypedDict, total=False):
    """Performance settings for a model."""

    latency: PerformanceConfigLatency | None


RequestMetadata = dict[RequestMetadataKeyString, RequestMetadataValueString]
ConverseRequestAdditionalModelResponseFieldPathsList = list[
    ConverseRequestAdditionalModelResponseFieldPathsListMemberString
]


class PromptVariableValues(TypedDict, total=False):
    """Contains a map of variables in a prompt from Prompt management to an
    object containing the values to fill in for them when running model
    invocation. For more information, see `How Prompt management
    works <https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management-how.html>`__.
    """

    text: String | None


PromptVariableMap = dict[String, PromptVariableValues]


class GuardrailConfiguration(TypedDict, total=False):
    """Configuration information for a guardrail that you use with the
    `Converse <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html>`__
    operation.
    """

    guardrailIdentifier: GuardrailIdentifier | None
    guardrailVersion: GuardrailVersion | None
    trace: GuardrailTrace | None


class SpecificToolChoice(TypedDict, total=False):
    """The model must request a specific tool. For example,
    ``{"tool" : {"name" : "Your tool name"}}``. For more information, see
    `Call a tool with the Converse
    API <https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html>`__
    in the Amazon Bedrock User Guide

    This field is only supported by Anthropic Claude 3 models.
    """

    name: ToolName


class ToolChoice(TypedDict, total=False):
    """Determines which tools the model should request in a call to
    ``Converse`` or ``ConverseStream``. For more information, see `Call a
    tool with the Converse
    API <https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html>`__
    in the Amazon Bedrock User Guide.
    """

    auto: AutoToolChoice | None
    any: AnyToolChoice | None
    tool: SpecificToolChoice | None


class SystemTool(TypedDict, total=False):
    """Specifies a system-defined tool for the model to use. *System-defined
    tools* are tools that are created and provided by the model provider.
    """

    name: ToolName


class ToolInputSchema(TypedDict, total=False):
    """The schema for the tool. The top level schema type must be ``object``.
    For more information, see `Call a tool with the Converse
    API <https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html>`__
    in the Amazon Bedrock User Guide.
    """

    json: Document | None


class ToolSpecification(TypedDict, total=False):
    """The specification for the tool. For more information, see `Call a tool
    with the Converse
    API <https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html>`__
    in the Amazon Bedrock User Guide.
    """

    name: ToolName
    description: NonEmptyString | None
    inputSchema: ToolInputSchema


class Tool(TypedDict, total=False):
    """Information about a tool that you can use with the Converse API. For
    more information, see `Call a tool with the Converse
    API <https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html>`__
    in the Amazon Bedrock User Guide.
    """

    toolSpec: ToolSpecification | None
    systemTool: SystemTool | None
    cachePoint: CachePointBlock | None


ToolConfigurationToolsList = list[Tool]


class ToolConfiguration(TypedDict, total=False):
    """Configuration information for the tools that you pass to a model. For
    more information, see `Tool use (function
    calling) <https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html>`__
    in the Amazon Bedrock User Guide.
    """

    tools: ToolConfigurationToolsList
    toolChoice: ToolChoice | None


InferenceConfigurationStopSequencesList = list[NonEmptyString]


class InferenceConfiguration(TypedDict, total=False):
    """Base inference parameters to pass to a model in a call to
    `Converse <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html>`__
    or
    `ConverseStream <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html>`__.
    For more information, see `Inference parameters for foundation
    models <https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters.html>`__.

    If you need to pass additional parameters that the model supports, use
    the ``additionalModelRequestFields`` request field in the call to
    ``Converse`` or ``ConverseStream``. For more information, see `Model
    parameters <https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters.html>`__.
    """

    maxTokens: InferenceConfigurationMaxTokensInteger | None
    temperature: InferenceConfigurationTemperatureFloat | None
    topP: InferenceConfigurationTopPFloat | None
    stopSequences: InferenceConfigurationStopSequencesList | None


class SystemContentBlock(TypedDict, total=False):
    """Contains configurations for instructions to provide the model for how to
    handle input. To learn more, see `Using the Converse
    API <https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference-call.html>`__.
    """

    text: NonEmptyString | None
    guardContent: GuardrailConverseContentBlock | None
    cachePoint: CachePointBlock | None


SystemContentBlocks = list[SystemContentBlock]
Messages = list[Message]


class ConverseRequest(ServiceRequest):
    modelId: ConversationalModelId
    messages: Messages | None
    system: SystemContentBlocks | None
    inferenceConfig: InferenceConfiguration | None
    toolConfig: ToolConfiguration | None
    guardrailConfig: GuardrailConfiguration | None
    additionalModelRequestFields: Document | None
    promptVariables: PromptVariableMap | None
    additionalModelResponseFieldPaths: ConverseRequestAdditionalModelResponseFieldPathsList | None
    requestMetadata: RequestMetadata | None
    performanceConfig: PerformanceConfiguration | None
    serviceTier: ServiceTier | None


class PromptRouterTrace(TypedDict, total=False):
    """A prompt router trace."""

    invokedModelId: InvokedModelId | None


GuardrailAssessmentListMap = dict[String, GuardrailAssessmentList]
GuardrailAssessmentMap = dict[String, GuardrailAssessment]
ModelOutputs = list[GuardrailOutputText]


class GuardrailTraceAssessment(TypedDict, total=False):
    """A Top level guardrail trace object. For more information, see
    `ConverseTrace <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseTrace.html>`__.
    """

    modelOutput: ModelOutputs | None
    inputAssessment: GuardrailAssessmentMap | None
    outputAssessments: GuardrailAssessmentListMap | None
    actionReason: String | None


class ConverseTrace(TypedDict, total=False):
    """The trace object in a response from
    `Converse <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html>`__.
    """

    guardrail: GuardrailTraceAssessment | None
    promptRouter: PromptRouterTrace | None


class TokenUsage(TypedDict, total=False):
    """The tokens used in a message API inference call."""

    inputTokens: TokenUsageInputTokensInteger
    outputTokens: TokenUsageOutputTokensInteger
    totalTokens: TokenUsageTotalTokensInteger
    cacheReadInputTokens: TokenUsageCacheReadInputTokensInteger | None
    cacheWriteInputTokens: TokenUsageCacheWriteInputTokensInteger | None
    cacheDetails: CacheDetailsList | None


class ConverseResponse(TypedDict, total=False):
    output: ConverseOutput
    stopReason: StopReason
    usage: TokenUsage
    metrics: ConverseMetrics
    additionalModelResponseFields: Document | None
    trace: ConverseTrace | None
    performanceConfig: PerformanceConfiguration | None
    serviceTier: ServiceTier | None


class ConverseStreamTrace(TypedDict, total=False):
    """The trace object in a response from
    `ConverseStream <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html>`__.
    """

    guardrail: GuardrailTraceAssessment | None
    promptRouter: PromptRouterTrace | None


class ConverseStreamMetrics(TypedDict, total=False):
    """Metrics for the stream."""

    latencyMs: Long


class ConverseStreamMetadataEvent(TypedDict, total=False):
    """A conversation stream metadata event."""

    usage: TokenUsage
    metrics: ConverseStreamMetrics
    trace: ConverseStreamTrace | None
    performanceConfig: PerformanceConfiguration | None
    serviceTier: ServiceTier | None


class MessageStopEvent(TypedDict, total=False):
    """The stop event for a message."""

    stopReason: StopReason
    additionalModelResponseFields: Document | None


class MessageStartEvent(TypedDict, total=False):
    """The start of a message."""

    role: ConversationRole


class ConverseStreamOutput(TypedDict, total=False):
    """The messages output stream"""

    messageStart: MessageStartEvent | None
    contentBlockStart: ContentBlockStartEvent | None
    contentBlockDelta: ContentBlockDeltaEvent | None
    contentBlockStop: ContentBlockStopEvent | None
    messageStop: MessageStopEvent | None
    metadata: ConverseStreamMetadataEvent | None
    internalServerException: InternalServerException | None
    modelStreamErrorException: ModelStreamErrorException | None
    validationException: ValidationException | None
    throttlingException: ThrottlingException | None
    serviceUnavailableException: ServiceUnavailableException | None


ConverseStreamRequestAdditionalModelResponseFieldPathsList = list[
    ConverseStreamRequestAdditionalModelResponseFieldPathsListMemberString
]


class GuardrailStreamConfiguration(TypedDict, total=False):
    """Configuration information for a guardrail that you use with the
    `ConverseStream <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html>`__
    action.
    """

    guardrailIdentifier: GuardrailIdentifier | None
    guardrailVersion: GuardrailVersion | None
    trace: GuardrailTrace | None
    streamProcessingMode: GuardrailStreamProcessingMode | None


class ConverseStreamRequest(ServiceRequest):
    modelId: ConversationalModelId
    messages: Messages | None
    system: SystemContentBlocks | None
    inferenceConfig: InferenceConfiguration | None
    toolConfig: ToolConfiguration | None
    guardrailConfig: GuardrailStreamConfiguration | None
    additionalModelRequestFields: Document | None
    promptVariables: PromptVariableMap | None
    additionalModelResponseFieldPaths: (
        ConverseStreamRequestAdditionalModelResponseFieldPathsList | None
    )
    requestMetadata: RequestMetadata | None
    performanceConfig: PerformanceConfiguration | None
    serviceTier: ServiceTier | None


class ConverseStreamResponse(TypedDict, total=False):
    stream: Iterator[ConverseStreamOutput]


class ConverseTokensRequest(TypedDict, total=False):
    """The inputs from a ``Converse`` API request for token counting.

    This structure mirrors the input format for the ``Converse`` operation,
    allowing you to count tokens for conversation-based inference requests.
    """

    messages: Messages | None
    system: SystemContentBlocks | None
    toolConfig: ToolConfiguration | None
    additionalModelRequestFields: Document | None


class InvokeModelTokensRequest(TypedDict, total=False):
    """The body of an ``InvokeModel`` API request for token counting. This
    structure mirrors the input format for the ``InvokeModel`` operation,
    allowing you to count tokens for raw text inference requests.
    """

    body: Body


class CountTokensInput(TypedDict, total=False):
    """The input value for token counting. The value should be either an
    ``InvokeModel`` or ``Converse`` request body.
    """

    invokeModel: InvokeModelTokensRequest | None
    converse: ConverseTokensRequest | None


class CountTokensRequest(ServiceRequest):
    modelId: FoundationModelVersionIdentifier
    input: CountTokensInput


class CountTokensResponse(TypedDict, total=False):
    inputTokens: Integer


class GetAsyncInvokeRequest(ServiceRequest):
    invocationArn: InvocationArn


class GetAsyncInvokeResponse(TypedDict, total=False):
    invocationArn: InvocationArn
    modelArn: AsyncInvokeArn
    clientRequestToken: AsyncInvokeIdempotencyToken | None
    status: AsyncInvokeStatus
    failureMessage: AsyncInvokeMessage | None
    submitTime: Timestamp
    lastModifiedTime: Timestamp | None
    endTime: Timestamp | None
    outputDataConfig: AsyncInvokeOutputDataConfig


class InvokeModelRequest(ServiceRequest):
    body: IO[Body] | None
    contentType: MimeType | None
    accept: MimeType | None
    modelId: InvokeModelIdentifier
    trace: Trace | None
    guardrailIdentifier: GuardrailIdentifier | None
    guardrailVersion: GuardrailVersion | None
    performanceConfigLatency: PerformanceConfigLatency | None
    serviceTier: ServiceTierType | None


class InvokeModelResponse(TypedDict, total=False):
    body: Body | IO[Body] | Iterable[Body]
    contentType: MimeType
    performanceConfigLatency: PerformanceConfigLatency | None
    serviceTier: ServiceTierType | None


class InvokeModelWithBidirectionalStreamInput(TypedDict, total=False):
    """Payload content, the speech chunk, for the bidirectional input of the
    invocation step.
    """

    chunk: BidirectionalInputPayloadPart | None


class InvokeModelWithBidirectionalStreamOutput(TypedDict, total=False):
    """Output from the bidirectional stream that was used for model invocation."""

    chunk: BidirectionalOutputPayloadPart | None
    internalServerException: InternalServerException | None
    modelStreamErrorException: ModelStreamErrorException | None
    validationException: ValidationException | None
    throttlingException: ThrottlingException | None
    modelTimeoutException: ModelTimeoutException | None
    serviceUnavailableException: ServiceUnavailableException | None


class InvokeModelWithBidirectionalStreamRequest(ServiceRequest):
    modelId: InvokeModelIdentifier
    body: Iterator[InvokeModelWithBidirectionalStreamInput]


class InvokeModelWithBidirectionalStreamResponse(TypedDict, total=False):
    body: Iterator[InvokeModelWithBidirectionalStreamOutput]


class InvokeModelWithResponseStreamRequest(ServiceRequest):
    body: IO[Body] | None
    contentType: MimeType | None
    accept: MimeType | None
    modelId: InvokeModelIdentifier
    trace: Trace | None
    guardrailIdentifier: GuardrailIdentifier | None
    guardrailVersion: GuardrailVersion | None
    performanceConfigLatency: PerformanceConfigLatency | None
    serviceTier: ServiceTierType | None


class PayloadPart(TypedDict, total=False):
    """Payload content included in the response."""

    bytes: PartBody | None


class ResponseStream(TypedDict, total=False):
    """Definition of content in the response stream."""

    chunk: PayloadPart | None
    internalServerException: InternalServerException | None
    modelStreamErrorException: ModelStreamErrorException | None
    validationException: ValidationException | None
    throttlingException: ThrottlingException | None
    modelTimeoutException: ModelTimeoutException | None
    serviceUnavailableException: ServiceUnavailableException | None


class InvokeModelWithResponseStreamResponse(TypedDict, total=False):
    body: Iterator[ResponseStream]
    contentType: MimeType
    performanceConfigLatency: PerformanceConfigLatency | None
    serviceTier: ServiceTierType | None


class ListAsyncInvokesRequest(ServiceRequest):
    submitTimeAfter: Timestamp | None
    submitTimeBefore: Timestamp | None
    statusEquals: AsyncInvokeStatus | None
    maxResults: MaxResults | None
    nextToken: PaginationToken | None
    sortBy: SortAsyncInvocationBy | None
    sortOrder: SortOrder | None


class ListAsyncInvokesResponse(TypedDict, total=False):
    nextToken: PaginationToken | None
    asyncInvokeSummaries: AsyncInvokeSummaries | None


class ModelInputPayload(TypedDict, total=False):
    pass


class Tag(TypedDict, total=False):
    """A tag."""

    key: TagKey
    value: TagValue


TagList = list[Tag]


class StartAsyncInvokeRequest(ServiceRequest):
    clientRequestToken: AsyncInvokeIdempotencyToken | None
    modelId: AsyncInvokeIdentifier
    modelInput: ModelInputPayload
    outputDataConfig: AsyncInvokeOutputDataConfig
    tags: TagList | None


class StartAsyncInvokeResponse(TypedDict, total=False):
    invocationArn: InvocationArn


class BedrockRuntimeApi:
    service: str = "bedrock-runtime"
    version: str = "2023-09-30"

    @handler("ApplyGuardrail")
    def apply_guardrail(
        self,
        context: RequestContext,
        guardrail_identifier: GuardrailIdentifier,
        guardrail_version: GuardrailVersion,
        source: GuardrailContentSource,
        content: GuardrailContentBlockList,
        output_scope: GuardrailOutputScope | None = None,
        **kwargs,
    ) -> ApplyGuardrailResponse:
        """The action to apply a guardrail.

        For troubleshooting some of the common errors you might encounter when
        using the ``ApplyGuardrail`` API, see `Troubleshooting Amazon Bedrock
        API Error
        Codes <https://docs.aws.amazon.com/bedrock/latest/userguide/troubleshooting-api-error-codes.html>`__
        in the Amazon Bedrock User Guide

        :param guardrail_identifier: The guardrail identifier used in the request to apply the guardrail.
        :param guardrail_version: The guardrail version used in the request to apply the guardrail.
        :param source: The source of data used in the request to apply the guardrail.
        :param content: The content details used in the request to apply the guardrail.
        :param output_scope: Specifies the scope of the output that you get in the response.
        :returns: ApplyGuardrailResponse
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalServerException:
        :raises ServiceUnavailableException:
        :raises ValidationException:
        :raises ServiceQuotaExceededException:
        """
        raise NotImplementedError

    @handler("Converse")
    def converse(
        self,
        context: RequestContext,
        model_id: ConversationalModelId,
        messages: Messages | None = None,
        system: SystemContentBlocks | None = None,
        inference_config: InferenceConfiguration | None = None,
        tool_config: ToolConfiguration | None = None,
        guardrail_config: GuardrailConfiguration | None = None,
        additional_model_request_fields: Document | None = None,
        prompt_variables: PromptVariableMap | None = None,
        additional_model_response_field_paths: ConverseRequestAdditionalModelResponseFieldPathsList
        | None = None,
        request_metadata: RequestMetadata | None = None,
        performance_config: PerformanceConfiguration | None = None,
        service_tier: ServiceTier | None = None,
        **kwargs,
    ) -> ConverseResponse:
        """Sends messages to the specified Amazon Bedrock model. ``Converse``
        provides a consistent interface that works with all models that support
        messages. This allows you to write code once and use it with different
        models. If a model has unique inference parameters, you can also pass
        those unique parameters to the model.

        Amazon Bedrock doesn't store any text, images, or documents that you
        provide as content. The data is only used to generate the response.

        You can submit a prompt by including it in the ``messages`` field,
        specifying the ``modelId`` of a foundation model or inference profile to
        run inference on it, and including any other fields that are relevant to
        your use case.

        You can also submit a prompt from Prompt management by specifying the
        ARN of the prompt version and including a map of variables to values in
        the ``promptVariables`` field. You can append more messages to the
        prompt by using the ``messages`` field. If you use a prompt from Prompt
        management, you can't include the following fields in the request:
        ``additionalModelRequestFields``, ``inferenceConfig``, ``system``, or
        ``toolConfig``. Instead, these fields must be defined through Prompt
        management. For more information, see `Use a prompt from Prompt
        management <https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management-use.html>`__.

        For information about the Converse API, see *Use the Converse API* in
        the *Amazon Bedrock User Guide*. To use a guardrail, see *Use a
        guardrail with the Converse API* in the *Amazon Bedrock User Guide*. To
        use a tool with a model, see *Tool use (Function calling)* in the
        *Amazon Bedrock User Guide*

        For example code, see *Converse API examples* in the *Amazon Bedrock
        User Guide*.

        This operation requires permission for the ``bedrock:InvokeModel``
        action.

        To deny all inference access to resources that you specify in the
        modelId field, you need to deny access to the ``bedrock:InvokeModel``
        and ``bedrock:InvokeModelWithResponseStream`` actions. Doing this also
        denies access to the resource through the base inference actions
        (`InvokeModel <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html>`__
        and
        `InvokeModelWithResponseStream <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html>`__).
        For more information see `Deny access for inference on specific
        models <https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html#security_iam_id-based-policy-examples-deny-inference>`__.

        For troubleshooting some of the common errors you might encounter when
        using the ``Converse`` API, see `Troubleshooting Amazon Bedrock API
        Error
        Codes <https://docs.aws.amazon.com/bedrock/latest/userguide/troubleshooting-api-error-codes.html>`__
        in the Amazon Bedrock User Guide

        :param model_id: Specifies the model or throughput with which to run inference, or the
        prompt resource to use in inference.
        :param messages: The messages that you want to send to the model.
        :param system: A prompt that provides instructions or context to the model about the
        task it should perform, or the persona it should adopt during the
        conversation.
        :param inference_config: Inference parameters to pass to the model.
        :param tool_config: Configuration information for the tools that the model can use when
        generating a response.
        :param guardrail_config: Configuration information for a guardrail that you want to use in the
        request.
        :param additional_model_request_fields: Additional inference parameters that the model supports, beyond the base
        set of inference parameters that ``Converse`` and ``ConverseStream``
        support in the ``inferenceConfig`` field.
        :param prompt_variables: Contains a map of variables in a prompt from Prompt management to
        objects containing the values to fill in for them when running model
        invocation.
        :param additional_model_response_field_paths: Additional model parameters field paths to return in the response.
        :param request_metadata: Key-value pairs that you can use to filter invocation logs.
        :param performance_config: Model performance settings for the request.
        :param service_tier: Specifies the processing tier configuration used for serving the
        request.
        :returns: ConverseResponse
        :raises AccessDeniedException:
        :raises ThrottlingException:
        :raises ResourceNotFoundException:
        :raises ModelTimeoutException:
        :raises InternalServerException:
        :raises ServiceUnavailableException:
        :raises ValidationException:
        :raises ModelNotReadyException:
        :raises ModelErrorException:
        """
        raise NotImplementedError

    @handler("ConverseStream")
    def converse_stream(
        self,
        context: RequestContext,
        model_id: ConversationalModelId,
        messages: Messages | None = None,
        system: SystemContentBlocks | None = None,
        inference_config: InferenceConfiguration | None = None,
        tool_config: ToolConfiguration | None = None,
        guardrail_config: GuardrailStreamConfiguration | None = None,
        additional_model_request_fields: Document | None = None,
        prompt_variables: PromptVariableMap | None = None,
        additional_model_response_field_paths: ConverseStreamRequestAdditionalModelResponseFieldPathsList
        | None = None,
        request_metadata: RequestMetadata | None = None,
        performance_config: PerformanceConfiguration | None = None,
        service_tier: ServiceTier | None = None,
        **kwargs,
    ) -> ConverseStreamResponse:
        """Sends messages to the specified Amazon Bedrock model and returns the
        response in a stream. ``ConverseStream`` provides a consistent API that
        works with all Amazon Bedrock models that support messages. This allows
        you to write code once and use it with different models. Should a model
        have unique inference parameters, you can also pass those unique
        parameters to the model.

        To find out if a model supports streaming, call
        `GetFoundationModel <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetFoundationModel.html>`__
        and check the ``responseStreamingSupported`` field in the response.

        The CLI doesn't support streaming operations in Amazon Bedrock,
        including ``ConverseStream``.

        Amazon Bedrock doesn't store any text, images, or documents that you
        provide as content. The data is only used to generate the response.

        You can submit a prompt by including it in the ``messages`` field,
        specifying the ``modelId`` of a foundation model or inference profile to
        run inference on it, and including any other fields that are relevant to
        your use case.

        You can also submit a prompt from Prompt management by specifying the
        ARN of the prompt version and including a map of variables to values in
        the ``promptVariables`` field. You can append more messages to the
        prompt by using the ``messages`` field. If you use a prompt from Prompt
        management, you can't include the following fields in the request:
        ``additionalModelRequestFields``, ``inferenceConfig``, ``system``, or
        ``toolConfig``. Instead, these fields must be defined through Prompt
        management. For more information, see `Use a prompt from Prompt
        management <https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management-use.html>`__.

        For information about the Converse API, see *Use the Converse API* in
        the *Amazon Bedrock User Guide*. To use a guardrail, see *Use a
        guardrail with the Converse API* in the *Amazon Bedrock User Guide*. To
        use a tool with a model, see *Tool use (Function calling)* in the
        *Amazon Bedrock User Guide*

        For example code, see *Conversation streaming example* in the *Amazon
        Bedrock User Guide*.

        This operation requires permission for the
        ``bedrock:InvokeModelWithResponseStream`` action.

        To deny all inference access to resources that you specify in the
        modelId field, you need to deny access to the ``bedrock:InvokeModel``
        and ``bedrock:InvokeModelWithResponseStream`` actions. Doing this also
        denies access to the resource through the base inference actions
        (`InvokeModel <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html>`__
        and
        `InvokeModelWithResponseStream <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html>`__).
        For more information see `Deny access for inference on specific
        models <https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html#security_iam_id-based-policy-examples-deny-inference>`__.

        For troubleshooting some of the common errors you might encounter when
        using the ``ConverseStream`` API, see `Troubleshooting Amazon Bedrock
        API Error
        Codes <https://docs.aws.amazon.com/bedrock/latest/userguide/troubleshooting-api-error-codes.html>`__
        in the Amazon Bedrock User Guide

        :param model_id: Specifies the model or throughput with which to run inference, or the
        prompt resource to use in inference.
        :param messages: The messages that you want to send to the model.
        :param system: A prompt that provides instructions or context to the model about the
        task it should perform, or the persona it should adopt during the
        conversation.
        :param inference_config: Inference parameters to pass to the model.
        :param tool_config: Configuration information for the tools that the model can use when
        generating a response.
        :param guardrail_config: Configuration information for a guardrail that you want to use in the
        request.
        :param additional_model_request_fields: Additional inference parameters that the model supports, beyond the base
        set of inference parameters that ``Converse`` and ``ConverseStream``
        support in the ``inferenceConfig`` field.
        :param prompt_variables: Contains a map of variables in a prompt from Prompt management to
        objects containing the values to fill in for them when running model
        invocation.
        :param additional_model_response_field_paths: Additional model parameters field paths to return in the response.
        :param request_metadata: Key-value pairs that you can use to filter invocation logs.
        :param performance_config: Model performance settings for the request.
        :param service_tier: Specifies the processing tier configuration used for serving the
        request.
        :returns: ConverseStreamResponse
        :raises AccessDeniedException:
        :raises ThrottlingException:
        :raises ResourceNotFoundException:
        :raises ModelTimeoutException:
        :raises InternalServerException:
        :raises ServiceUnavailableException:
        :raises ValidationException:
        :raises ModelNotReadyException:
        :raises ModelErrorException:
        """
        raise NotImplementedError

    @handler("CountTokens")
    def count_tokens(
        self,
        context: RequestContext,
        model_id: FoundationModelVersionIdentifier,
        input: CountTokensInput,
        **kwargs,
    ) -> CountTokensResponse:
        """Returns the token count for a given inference request. This operation
        helps you estimate token usage before sending requests to foundation
        models by returning the token count that would be used if the same input
        were sent to the model in an inference request.

        Token counting is model-specific because different models use different
        tokenization strategies. The token count returned by this operation will
        match the token count that would be charged if the same input were sent
        to the model in an ``InvokeModel`` or ``Converse`` request.

        You can use this operation to:

        -  Estimate costs before sending inference requests.

        -  Optimize prompts to fit within token limits.

        -  Plan for token usage in your applications.

        This operation accepts the same input formats as ``InvokeModel`` and
        ``Converse``, allowing you to count tokens for both raw text inputs and
        structured conversation formats.

        The following operations are related to ``CountTokens``:

        -  `InvokeModel <https://docs.aws.amazon.com/bedrock/latest/API/API_runtime_InvokeModel.html>`__
           - Sends inference requests to foundation models

        -  `Converse <https://docs.aws.amazon.com/bedrock/latest/API/API_runtime_Converse.html>`__
           - Sends conversation-based inference requests to foundation models

        :param model_id: The unique identifier or ARN of the foundation model to use for token
        counting.
        :param input: The input for which to count tokens.
        :returns: CountTokensResponse
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalServerException:
        :raises ServiceUnavailableException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("GetAsyncInvoke")
    def get_async_invoke(
        self, context: RequestContext, invocation_arn: InvocationArn, **kwargs
    ) -> GetAsyncInvokeResponse:
        """Retrieve information about an asynchronous invocation.

        :param invocation_arn: The invocation's ARN.
        :returns: GetAsyncInvokeResponse
        :raises AccessDeniedException:
        :raises ThrottlingException:
        :raises InternalServerException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("InvokeModel")
    def invoke_model(
        self,
        context: RequestContext,
        model_id: InvokeModelIdentifier,
        body: IO[Body] | None = None,
        content_type: MimeType | None = None,
        accept: MimeType | None = None,
        trace: Trace | None = None,
        guardrail_identifier: GuardrailIdentifier | None = None,
        guardrail_version: GuardrailVersion | None = None,
        performance_config_latency: PerformanceConfigLatency | None = None,
        service_tier: ServiceTierType | None = None,
        **kwargs,
    ) -> InvokeModelResponse:
        """Invokes the specified Amazon Bedrock model to run inference using the
        prompt and inference parameters provided in the request body. You use
        model inference to generate text, images, and embeddings.

        For example code, see *Invoke model code examples* in the *Amazon
        Bedrock User Guide*.

        This operation requires permission for the ``bedrock:InvokeModel``
        action.

        To deny all inference access to resources that you specify in the
        modelId field, you need to deny access to the ``bedrock:InvokeModel``
        and ``bedrock:InvokeModelWithResponseStream`` actions. Doing this also
        denies access to the resource through the Converse API actions
        (`Converse <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html>`__
        and
        `ConverseStream <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html>`__).
        For more information see `Deny access for inference on specific
        models <https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html#security_iam_id-based-policy-examples-deny-inference>`__.

        For troubleshooting some of the common errors you might encounter when
        using the ``InvokeModel`` API, see `Troubleshooting Amazon Bedrock API
        Error
        Codes <https://docs.aws.amazon.com/bedrock/latest/userguide/troubleshooting-api-error-codes.html>`__
        in the Amazon Bedrock User Guide

        :param model_id: The unique identifier of the model to invoke to run inference.
        :param body: The prompt and inference parameters in the format specified in the
        ``contentType`` in the header.
        :param content_type: The MIME type of the input data in the request.
        :param accept: The desired MIME type of the inference body in the response.
        :param trace: Specifies whether to enable or disable the Bedrock trace.
        :param guardrail_identifier: The unique identifier of the guardrail that you want to use.
        :param guardrail_version: The version number for the guardrail.
        :param performance_config_latency: Model performance settings for the request.
        :param service_tier: Specifies the processing tier type used for serving the request.
        :returns: InvokeModelResponse
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ModelTimeoutException:
        :raises InternalServerException:
        :raises ServiceUnavailableException:
        :raises ValidationException:
        :raises ServiceQuotaExceededException:
        :raises ModelNotReadyException:
        :raises ModelErrorException:
        """
        raise NotImplementedError

    @handler("InvokeModelWithBidirectionalStream")
    def invoke_model_with_bidirectional_stream(
        self,
        context: RequestContext,
        model_id: InvokeModelIdentifier,
        body: InvokeModelWithBidirectionalStreamInput,
        **kwargs,
    ) -> InvokeModelWithBidirectionalStreamResponse:
        """Invoke the specified Amazon Bedrock model to run inference using the
        bidirectional stream. The response is returned in a stream that remains
        open for 8 minutes. A single session can contain multiple prompts and
        responses from the model. The prompts to the model are provided as audio
        files and the model's responses are spoken back to the user and
        transcribed.

        It is possible for users to interrupt the model's response with a new
        prompt, which will halt the response speech. The model will retain
        contextual awareness of the conversation while pivoting to respond to
        the new prompt.

        :param model_id: The model ID or ARN of the model ID to use.
        :param body: The prompt and inference parameters in the format specified in the
        ``BidirectionalInputPayloadPart`` in the header.
        :returns: InvokeModelWithBidirectionalStreamResponse
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ModelTimeoutException:
        :raises InternalServerException:
        :raises ServiceUnavailableException:
        :raises ModelStreamErrorException:
        :raises ValidationException:
        :raises ServiceQuotaExceededException:
        :raises ModelNotReadyException:
        :raises ModelErrorException:
        """
        raise NotImplementedError

    @handler("InvokeModelWithResponseStream")
    def invoke_model_with_response_stream(
        self,
        context: RequestContext,
        model_id: InvokeModelIdentifier,
        body: IO[Body] | None = None,
        content_type: MimeType | None = None,
        accept: MimeType | None = None,
        trace: Trace | None = None,
        guardrail_identifier: GuardrailIdentifier | None = None,
        guardrail_version: GuardrailVersion | None = None,
        performance_config_latency: PerformanceConfigLatency | None = None,
        service_tier: ServiceTierType | None = None,
        **kwargs,
    ) -> InvokeModelWithResponseStreamResponse:
        """Invoke the specified Amazon Bedrock model to run inference using the
        prompt and inference parameters provided in the request body. The
        response is returned in a stream.

        To see if a model supports streaming, call
        `GetFoundationModel <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetFoundationModel.html>`__
        and check the ``responseStreamingSupported`` field in the response.

        The CLI doesn't support streaming operations in Amazon Bedrock,
        including ``InvokeModelWithResponseStream``.

        For example code, see *Invoke model with streaming code example* in the
        *Amazon Bedrock User Guide*.

        This operation requires permissions to perform the
        ``bedrock:InvokeModelWithResponseStream`` action.

        To deny all inference access to resources that you specify in the
        modelId field, you need to deny access to the ``bedrock:InvokeModel``
        and ``bedrock:InvokeModelWithResponseStream`` actions. Doing this also
        denies access to the resource through the Converse API actions
        (`Converse <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html>`__
        and
        `ConverseStream <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html>`__).
        For more information see `Deny access for inference on specific
        models <https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html#security_iam_id-based-policy-examples-deny-inference>`__.

        For troubleshooting some of the common errors you might encounter when
        using the ``InvokeModelWithResponseStream`` API, see `Troubleshooting
        Amazon Bedrock API Error
        Codes <https://docs.aws.amazon.com/bedrock/latest/userguide/troubleshooting-api-error-codes.html>`__
        in the Amazon Bedrock User Guide

        :param model_id: The unique identifier of the model to invoke to run inference.
        :param body: The prompt and inference parameters in the format specified in the
        ``contentType`` in the header.
        :param content_type: The MIME type of the input data in the request.
        :param accept: The desired MIME type of the inference body in the response.
        :param trace: Specifies whether to enable or disable the Bedrock trace.
        :param guardrail_identifier: The unique identifier of the guardrail that you want to use.
        :param guardrail_version: The version number for the guardrail.
        :param performance_config_latency: Model performance settings for the request.
        :param service_tier: Specifies the processing tier type used for serving the request.
        :returns: InvokeModelWithResponseStreamResponse
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ModelTimeoutException:
        :raises InternalServerException:
        :raises ServiceUnavailableException:
        :raises ModelStreamErrorException:
        :raises ValidationException:
        :raises ServiceQuotaExceededException:
        :raises ModelNotReadyException:
        :raises ModelErrorException:
        """
        raise NotImplementedError

    @handler("ListAsyncInvokes")
    def list_async_invokes(
        self,
        context: RequestContext,
        submit_time_after: Timestamp | None = None,
        submit_time_before: Timestamp | None = None,
        status_equals: AsyncInvokeStatus | None = None,
        max_results: MaxResults | None = None,
        next_token: PaginationToken | None = None,
        sort_by: SortAsyncInvocationBy | None = None,
        sort_order: SortOrder | None = None,
        **kwargs,
    ) -> ListAsyncInvokesResponse:
        """Lists asynchronous invocations.

        :param submit_time_after: Include invocations submitted after this time.
        :param submit_time_before: Include invocations submitted before this time.
        :param status_equals: Filter invocations by status.
        :param max_results: The maximum number of invocations to return in one page of results.
        :param next_token: Specify the pagination token from a previous request to retrieve the
        next page of results.
        :param sort_by: How to sort the response.
        :param sort_order: The sorting order for the response.
        :returns: ListAsyncInvokesResponse
        :raises AccessDeniedException:
        :raises ThrottlingException:
        :raises InternalServerException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("StartAsyncInvoke")
    def start_async_invoke(
        self,
        context: RequestContext,
        model_id: AsyncInvokeIdentifier,
        model_input: ModelInputPayload,
        output_data_config: AsyncInvokeOutputDataConfig,
        client_request_token: AsyncInvokeIdempotencyToken | None = None,
        tags: TagList | None = None,
        **kwargs,
    ) -> StartAsyncInvokeResponse:
        """Starts an asynchronous invocation.

        This operation requires permission for the ``bedrock:InvokeModel``
        action.

        To deny all inference access to resources that you specify in the
        modelId field, you need to deny access to the ``bedrock:InvokeModel``
        and ``bedrock:InvokeModelWithResponseStream`` actions. Doing this also
        denies access to the resource through the Converse API actions
        (`Converse <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html>`__
        and
        `ConverseStream <https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ConverseStream.html>`__).
        For more information see `Deny access for inference on specific
        models <https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html#security_iam_id-based-policy-examples-deny-inference>`__.

        :param model_id: The model to invoke.
        :param model_input: Input to send to the model.
        :param output_data_config: Where to store the output.
        :param client_request_token: Specify idempotency token to ensure that requests are not duplicated.
        :param tags: Tags to apply to the invocation.
        :returns: StartAsyncInvokeResponse
        :raises AccessDeniedException:
        :raises ThrottlingException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ServiceUnavailableException:
        :raises ValidationException:
        :raises ServiceQuotaExceededException:
        :raises ConflictException:
        """
        raise NotImplementedError
