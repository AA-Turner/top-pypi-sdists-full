from datetime import datetime
from enum import StrEnum
from typing import TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

AccountSettingName = str
AccountSettingValue = str
Arch = str
Arn = str
ArtifactType = str
AttributeKey = str
AttributeValue = str
Author = str
Base64 = str
BaseScore = float
BatchedOperationLayerDigest = str
CredentialArn = str
CustomRoleArn = str
Epoch = int
ExceptionMessage = str
ExploitAvailable = str
FiftyMaxResults = int
FilePath = str
FindingArn = str
FindingDescription = str
FindingName = str
FixAvailable = str
FixedInVersion = str
ForceFlag = bool
ImageCount = int
ImageDigest = str
ImageFailureReason = str
ImageManifest = str
ImageTag = str
ImageTagMutabilityExclusionFilterValue = str
IsPTCRuleValid = bool
KmsError = str
KmsKey = str
KmsKeyForRepositoryCreationTemplate = str
LayerDigest = str
LayerFailureReason = str
LifecyclePolicyRulePriority = int
LifecyclePolicyText = str
LifecyclePolicyTextForRepositoryCreationTemplate = str
LifecyclePreviewMaxResults = int
MaxResults = int
MediaType = str
Metric = str
NextToken = str
PTCValidateFailure = str
PackageManager = str
Platform = str
Prefix = str
PrincipalArn = str
ProxyEndpoint = str
PullThroughCacheRuleRepositoryPrefix = str
Reason = str
RecommendationText = str
Region = str
RegistryId = str
RegistryPolicyText = str
RelatedVulnerability = str
Release = str
ReplicationError = str
RepositoryFilterValue = str
RepositoryName = str
RepositoryPolicyText = str
RepositoryTemplateDescription = str
ResourceId = str
ScanOnPushFlag = bool
ScanStatusDescription = str
ScanningConfigurationFailureReason = str
ScanningRepositoryFilterValue = str
Score = float
ScoringVector = str
Severity = str
SeverityCount = int
SigningProfileArn = str
SigningRepositoryFilterValue = str
SigningStatusFailureCode = str
SigningStatusFailureReason = str
Source = str
SourceLayerHash = str
Status = str
String = str
TagKey = str
TagValue = str
Title = str
Type = str
UploadId = str
Url = str
Version = str
VulnerabilityId = str
VulnerablePackageName = str


class ArtifactStatus(StrEnum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    ACTIVATING = "ACTIVATING"


class ArtifactStatusFilter(StrEnum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    ACTIVATING = "ACTIVATING"
    ANY = "ANY"


class EncryptionType(StrEnum):
    AES256 = "AES256"
    KMS = "KMS"
    KMS_DSSE = "KMS_DSSE"


class FindingSeverity(StrEnum):
    INFORMATIONAL = "INFORMATIONAL"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    UNDEFINED = "UNDEFINED"


class ImageActionType(StrEnum):
    EXPIRE = "EXPIRE"
    TRANSITION = "TRANSITION"


class ImageFailureCode(StrEnum):
    InvalidImageDigest = "InvalidImageDigest"
    InvalidImageTag = "InvalidImageTag"
    ImageTagDoesNotMatchDigest = "ImageTagDoesNotMatchDigest"
    ImageNotFound = "ImageNotFound"
    MissingDigestAndTag = "MissingDigestAndTag"
    ImageReferencedByManifestList = "ImageReferencedByManifestList"
    KmsError = "KmsError"
    UpstreamAccessDenied = "UpstreamAccessDenied"
    UpstreamTooManyRequests = "UpstreamTooManyRequests"
    UpstreamUnavailable = "UpstreamUnavailable"
    ImageInaccessible = "ImageInaccessible"


class ImageStatus(StrEnum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    ACTIVATING = "ACTIVATING"


class ImageStatusFilter(StrEnum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    ACTIVATING = "ACTIVATING"
    ANY = "ANY"


class ImageTagMutability(StrEnum):
    MUTABLE = "MUTABLE"
    IMMUTABLE = "IMMUTABLE"
    IMMUTABLE_WITH_EXCLUSION = "IMMUTABLE_WITH_EXCLUSION"
    MUTABLE_WITH_EXCLUSION = "MUTABLE_WITH_EXCLUSION"


class ImageTagMutabilityExclusionFilterType(StrEnum):
    WILDCARD = "WILDCARD"


class LayerAvailability(StrEnum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    ARCHIVED = "ARCHIVED"


class LayerFailureCode(StrEnum):
    InvalidLayerDigest = "InvalidLayerDigest"
    MissingLayerDigest = "MissingLayerDigest"


class LifecyclePolicyPreviewStatus(StrEnum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    EXPIRED = "EXPIRED"
    FAILED = "FAILED"


class LifecyclePolicyStorageClass(StrEnum):
    ARCHIVE = "ARCHIVE"
    STANDARD = "STANDARD"


class LifecyclePolicyTargetStorageClass(StrEnum):
    ARCHIVE = "ARCHIVE"


class RCTAppliedFor(StrEnum):
    REPLICATION = "REPLICATION"
    PULL_THROUGH_CACHE = "PULL_THROUGH_CACHE"
    CREATE_ON_PUSH = "CREATE_ON_PUSH"


class ReplicationStatus(StrEnum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


class RepositoryFilterType(StrEnum):
    PREFIX_MATCH = "PREFIX_MATCH"


class ScanFrequency(StrEnum):
    SCAN_ON_PUSH = "SCAN_ON_PUSH"
    CONTINUOUS_SCAN = "CONTINUOUS_SCAN"
    MANUAL = "MANUAL"


class ScanStatus(StrEnum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    UNSUPPORTED_IMAGE = "UNSUPPORTED_IMAGE"
    ACTIVE = "ACTIVE"
    PENDING = "PENDING"
    SCAN_ELIGIBILITY_EXPIRED = "SCAN_ELIGIBILITY_EXPIRED"
    FINDINGS_UNAVAILABLE = "FINDINGS_UNAVAILABLE"
    LIMIT_EXCEEDED = "LIMIT_EXCEEDED"
    IMAGE_ARCHIVED = "IMAGE_ARCHIVED"


class ScanType(StrEnum):
    BASIC = "BASIC"
    ENHANCED = "ENHANCED"


class ScanningConfigurationFailureCode(StrEnum):
    REPOSITORY_NOT_FOUND = "REPOSITORY_NOT_FOUND"


class ScanningRepositoryFilterType(StrEnum):
    WILDCARD = "WILDCARD"


class SigningRepositoryFilterType(StrEnum):
    WILDCARD_MATCH = "WILDCARD_MATCH"


class SigningStatus(StrEnum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


class TagStatus(StrEnum):
    TAGGED = "TAGGED"
    UNTAGGED = "UNTAGGED"
    ANY = "ANY"


class TargetStorageClass(StrEnum):
    STANDARD = "STANDARD"
    ARCHIVE = "ARCHIVE"


class UpstreamRegistry(StrEnum):
    ecr = "ecr"
    ecr_public = "ecr-public"
    quay = "quay"
    k8s = "k8s"
    docker_hub = "docker-hub"
    github_container_registry = "github-container-registry"
    azure_container_registry = "azure-container-registry"
    gitlab_container_registry = "gitlab-container-registry"


class BlockedByOrganizationPolicyException(ServiceException):
    """The operation did not succeed because the account is managed by a
    organization policy.
    """

    code: str = "BlockedByOrganizationPolicyException"
    sender_fault: bool = False
    status_code: int = 400


class EmptyUploadException(ServiceException):
    """The specified layer upload does not contain any layer parts."""

    code: str = "EmptyUploadException"
    sender_fault: bool = False
    status_code: int = 400


class ExclusionAlreadyExistsException(ServiceException):
    """The specified pull time update exclusion already exists for the
    registry.
    """

    code: str = "ExclusionAlreadyExistsException"
    sender_fault: bool = False
    status_code: int = 400


class ExclusionNotFoundException(ServiceException):
    """The specified pull time update exclusion was not found."""

    code: str = "ExclusionNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class ImageAlreadyExistsException(ServiceException):
    """The specified image has already been pushed, and there were no changes
    to the manifest or image tag after the last push.
    """

    code: str = "ImageAlreadyExistsException"
    sender_fault: bool = False
    status_code: int = 400


class ImageArchivedException(ServiceException):
    """The specified image is archived and cannot be scanned."""

    code: str = "ImageArchivedException"
    sender_fault: bool = False
    status_code: int = 400


class ImageDigestDoesNotMatchException(ServiceException):
    """The specified image digest does not match the digest that Amazon ECR
    calculated for the image.
    """

    code: str = "ImageDigestDoesNotMatchException"
    sender_fault: bool = False
    status_code: int = 400


class ImageNotFoundException(ServiceException):
    """The image requested does not exist in the specified repository."""

    code: str = "ImageNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class ImageStorageClassUpdateNotSupportedException(ServiceException):
    """The requested image storage class update is not supported."""

    code: str = "ImageStorageClassUpdateNotSupportedException"
    sender_fault: bool = False
    status_code: int = 400


class ImageTagAlreadyExistsException(ServiceException):
    """The specified image is tagged with a tag that already exists. The
    repository is configured for tag immutability.
    """

    code: str = "ImageTagAlreadyExistsException"
    sender_fault: bool = False
    status_code: int = 400


class InvalidLayerException(ServiceException):
    """The layer digest calculation performed by Amazon ECR upon receipt of the
    image layer does not match the digest specified.
    """

    code: str = "InvalidLayerException"
    sender_fault: bool = False
    status_code: int = 400


PartSize = int


class InvalidLayerPartException(ServiceException):
    """The layer part size is not valid, or the first byte specified is not
    consecutive to the last byte of a previous layer part upload.
    """

    code: str = "InvalidLayerPartException"
    sender_fault: bool = False
    status_code: int = 400
    registryId: RegistryId | None
    repositoryName: RepositoryName | None
    uploadId: UploadId | None
    lastValidByteReceived: PartSize | None


class InvalidParameterException(ServiceException):
    """The specified parameter is invalid. Review the available parameters for
    the API request.
    """

    code: str = "InvalidParameterException"
    sender_fault: bool = False
    status_code: int = 400


class InvalidTagParameterException(ServiceException):
    """An invalid parameter has been specified. Tag keys can have a maximum
    character length of 128 characters, and tag values can have a maximum
    length of 256 characters.
    """

    code: str = "InvalidTagParameterException"
    sender_fault: bool = False
    status_code: int = 400


class KmsException(ServiceException):
    """The operation failed due to a KMS exception."""

    code: str = "KmsException"
    sender_fault: bool = False
    status_code: int = 400
    kmsError: KmsError | None


class LayerAlreadyExistsException(ServiceException):
    """The image layer already exists in the associated repository."""

    code: str = "LayerAlreadyExistsException"
    sender_fault: bool = False
    status_code: int = 400


class LayerInaccessibleException(ServiceException):
    """The specified layer is not available because it is not associated with
    an image. Unassociated image layers may be cleaned up at any time.
    """

    code: str = "LayerInaccessibleException"
    sender_fault: bool = False
    status_code: int = 400


class LayerPartTooSmallException(ServiceException):
    """Layer parts must be at least 5 MiB in size."""

    code: str = "LayerPartTooSmallException"
    sender_fault: bool = False
    status_code: int = 400


class LayersNotFoundException(ServiceException):
    """The specified layers could not be found, or the specified layer is not
    valid for this repository.
    """

    code: str = "LayersNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class LifecyclePolicyNotFoundException(ServiceException):
    """The lifecycle policy could not be found, and no policy is set to the
    repository.
    """

    code: str = "LifecyclePolicyNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class LifecyclePolicyPreviewInProgressException(ServiceException):
    """The previous lifecycle policy preview request has not completed. Wait
    and try again.
    """

    code: str = "LifecyclePolicyPreviewInProgressException"
    sender_fault: bool = False
    status_code: int = 400


class LifecyclePolicyPreviewNotFoundException(ServiceException):
    """There is no dry run for this repository."""

    code: str = "LifecyclePolicyPreviewNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class LimitExceededException(ServiceException):
    """The operation did not succeed because it would have exceeded a service
    limit for your account. For more information, see `Amazon ECR service
    quotas <https://docs.aws.amazon.com/AmazonECR/latest/userguide/service-quotas.html>`__
    in the Amazon Elastic Container Registry User Guide.
    """

    code: str = "LimitExceededException"
    sender_fault: bool = False
    status_code: int = 400


class PullThroughCacheRuleAlreadyExistsException(ServiceException):
    """A pull through cache rule with these settings already exists for the
    private registry.
    """

    code: str = "PullThroughCacheRuleAlreadyExistsException"
    sender_fault: bool = False
    status_code: int = 400


class PullThroughCacheRuleNotFoundException(ServiceException):
    """The pull through cache rule was not found. Specify a valid pull through
    cache rule and try again.
    """

    code: str = "PullThroughCacheRuleNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class ReferencedImagesNotFoundException(ServiceException):
    """The manifest list is referencing an image that does not exist."""

    code: str = "ReferencedImagesNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class RegistryPolicyNotFoundException(ServiceException):
    """The registry doesn't have an associated registry policy."""

    code: str = "RegistryPolicyNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class RepositoryAlreadyExistsException(ServiceException):
    """The specified repository already exists in the specified registry."""

    code: str = "RepositoryAlreadyExistsException"
    sender_fault: bool = False
    status_code: int = 400


class RepositoryNotEmptyException(ServiceException):
    """The specified repository contains images. To delete a repository that
    contains images, you must force the deletion with the ``force``
    parameter.
    """

    code: str = "RepositoryNotEmptyException"
    sender_fault: bool = False
    status_code: int = 400


class RepositoryNotFoundException(ServiceException):
    """The specified repository could not be found. Check the spelling of the
    specified repository and ensure that you are performing operations on
    the correct registry.
    """

    code: str = "RepositoryNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class RepositoryPolicyNotFoundException(ServiceException):
    """The specified repository and registry combination does not have an
    associated repository policy.
    """

    code: str = "RepositoryPolicyNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class ScanNotFoundException(ServiceException):
    """The specified image scan could not be found. Ensure that image scanning
    is enabled on the repository and try again.
    """

    code: str = "ScanNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class SecretNotFoundException(ServiceException):
    """The ARN of the secret specified in the pull through cache rule was not
    found. Update the pull through cache rule with a valid secret ARN and
    try again.
    """

    code: str = "SecretNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class ServerException(ServiceException):
    """These errors are usually caused by a server-side issue."""

    code: str = "ServerException"
    sender_fault: bool = False
    status_code: int = 400


class SigningConfigurationNotFoundException(ServiceException):
    """The specified signing configuration was not found. This occurs when
    attempting to retrieve or delete a signing configuration that does not
    exist.
    """

    code: str = "SigningConfigurationNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class TemplateAlreadyExistsException(ServiceException):
    """The repository creation template already exists. Specify a unique prefix
    and try again.
    """

    code: str = "TemplateAlreadyExistsException"
    sender_fault: bool = False
    status_code: int = 400


class TemplateNotFoundException(ServiceException):
    """The specified repository creation template can't be found. Verify the
    registry ID and prefix and try again.
    """

    code: str = "TemplateNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class TooManyTagsException(ServiceException):
    """The list of tags on the repository is over the limit. The maximum number
    of tags that can be applied to a repository is 50.
    """

    code: str = "TooManyTagsException"
    sender_fault: bool = False
    status_code: int = 400


class UnableToAccessSecretException(ServiceException):
    """The secret is unable to be accessed. Verify the resource permissions for
    the secret and try again.
    """

    code: str = "UnableToAccessSecretException"
    sender_fault: bool = False
    status_code: int = 400


class UnableToDecryptSecretValueException(ServiceException):
    """The secret is accessible but is unable to be decrypted. Verify the
    resource permisisons and try again.
    """

    code: str = "UnableToDecryptSecretValueException"
    sender_fault: bool = False
    status_code: int = 400


class UnableToGetUpstreamImageException(ServiceException):
    """The image or images were unable to be pulled using the pull through
    cache rule. This is usually caused because of an issue with the Secrets
    Manager secret containing the credentials for the upstream registry.
    """

    code: str = "UnableToGetUpstreamImageException"
    sender_fault: bool = False
    status_code: int = 400


class UnableToGetUpstreamLayerException(ServiceException):
    """There was an issue getting the upstream layer matching the pull through
    cache rule.
    """

    code: str = "UnableToGetUpstreamLayerException"
    sender_fault: bool = False
    status_code: int = 400


class UnsupportedImageTypeException(ServiceException):
    """The image is of a type that cannot be scanned."""

    code: str = "UnsupportedImageTypeException"
    sender_fault: bool = False
    status_code: int = 400


class UnsupportedUpstreamRegistryException(ServiceException):
    """The specified upstream registry isn't supported."""

    code: str = "UnsupportedUpstreamRegistryException"
    sender_fault: bool = False
    status_code: int = 400


class UploadNotFoundException(ServiceException):
    """The upload could not be found, or the specified upload ID is not valid
    for this repository.
    """

    code: str = "UploadNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class ValidationException(ServiceException):
    """There was an exception validating this request."""

    code: str = "ValidationException"
    sender_fault: bool = False
    status_code: int = 400


Annotations = dict[String, String]
ArtifactTypeList = list[ArtifactType]


class Attribute(TypedDict, total=False):
    """This data type is used in the ImageScanFinding data type."""

    key: AttributeKey
    value: AttributeValue | None


AttributeList = list[Attribute]
ExpirationTimestamp = datetime


class AuthorizationData(TypedDict, total=False):
    """An object representing authorization data for an Amazon ECR registry."""

    authorizationToken: Base64 | None
    expiresAt: ExpirationTimestamp | None
    proxyEndpoint: ProxyEndpoint | None


AuthorizationDataList = list[AuthorizationData]
InUseCount = int
Date = datetime
ImageTagsList = list[ImageTag]


class AwsEcrContainerImageDetails(TypedDict, total=False):
    """The image details of the Amazon ECR container image."""

    architecture: Arch | None
    author: Author | None
    imageHash: ImageDigest | None
    imageTags: ImageTagsList | None
    platform: Platform | None
    pushedAt: Date | None
    lastInUseAt: Date | None
    inUseCount: InUseCount | None
    registry: RegistryId | None
    repositoryName: RepositoryName | None


BatchedOperationLayerDigestList = list[BatchedOperationLayerDigest]


class BatchCheckLayerAvailabilityRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryName: RepositoryName
    layerDigests: BatchedOperationLayerDigestList


class LayerFailure(TypedDict, total=False):
    """An object representing an Amazon ECR image layer failure."""

    layerDigest: BatchedOperationLayerDigest | None
    failureCode: LayerFailureCode | None
    failureReason: LayerFailureReason | None


LayerFailureList = list[LayerFailure]
LayerSizeInBytes = int


class Layer(TypedDict, total=False):
    """An object representing an Amazon ECR image layer."""

    layerDigest: LayerDigest | None
    layerAvailability: LayerAvailability | None
    layerSize: LayerSizeInBytes | None
    mediaType: MediaType | None


LayerList = list[Layer]


class BatchCheckLayerAvailabilityResponse(TypedDict, total=False):
    layers: LayerList | None
    failures: LayerFailureList | None


class ImageIdentifier(TypedDict, total=False):
    """An object with identifying information for an image in an Amazon ECR
    repository.
    """

    imageDigest: ImageDigest | None
    imageTag: ImageTag | None


ImageIdentifierList = list[ImageIdentifier]


class BatchDeleteImageRequest(ServiceRequest):
    """Deletes specified images within a specified repository. Images are
    specified with either the ``imageTag`` or ``imageDigest``.
    """

    registryId: RegistryId | None
    repositoryName: RepositoryName
    imageIds: ImageIdentifierList


class ImageFailure(TypedDict, total=False):
    """An object representing an Amazon ECR image failure."""

    imageId: ImageIdentifier | None
    failureCode: ImageFailureCode | None
    failureReason: ImageFailureReason | None


ImageFailureList = list[ImageFailure]


class BatchDeleteImageResponse(TypedDict, total=False):
    imageIds: ImageIdentifierList | None
    failures: ImageFailureList | None


MediaTypeList = list[MediaType]


class BatchGetImageRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryName: RepositoryName
    imageIds: ImageIdentifierList
    acceptedMediaTypes: MediaTypeList | None


class Image(TypedDict, total=False):
    """An object representing an Amazon ECR image."""

    registryId: RegistryId | None
    repositoryName: RepositoryName | None
    imageId: ImageIdentifier | None
    imageManifest: ImageManifest | None
    imageManifestMediaType: MediaType | None


ImageList = list[Image]


class BatchGetImageResponse(TypedDict, total=False):
    images: ImageList | None
    failures: ImageFailureList | None


ScanningConfigurationRepositoryNameList = list[RepositoryName]


class BatchGetRepositoryScanningConfigurationRequest(ServiceRequest):
    repositoryNames: ScanningConfigurationRepositoryNameList


class RepositoryScanningConfigurationFailure(TypedDict, total=False):
    """The details about any failures associated with the scanning
    configuration of a repository.
    """

    repositoryName: RepositoryName | None
    failureCode: ScanningConfigurationFailureCode | None
    failureReason: ScanningConfigurationFailureReason | None


RepositoryScanningConfigurationFailureList = list[RepositoryScanningConfigurationFailure]


class ScanningRepositoryFilter(TypedDict, total=False):
    """The details of a scanning repository filter. For more information on how
    to use filters, see `Using
    filters <https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning.html#image-scanning-filters>`__
    in the *Amazon Elastic Container Registry User Guide*.
    """

    filter: ScanningRepositoryFilterValue
    filterType: ScanningRepositoryFilterType


ScanningRepositoryFilterList = list[ScanningRepositoryFilter]


class RepositoryScanningConfiguration(TypedDict, total=False):
    """The details of the scanning configuration for a repository."""

    repositoryArn: Arn | None
    repositoryName: RepositoryName | None
    scanOnPush: ScanOnPushFlag | None
    scanFrequency: ScanFrequency | None
    appliedScanFilters: ScanningRepositoryFilterList | None


RepositoryScanningConfigurationList = list[RepositoryScanningConfiguration]


class BatchGetRepositoryScanningConfigurationResponse(TypedDict, total=False):
    scanningConfigurations: RepositoryScanningConfigurationList | None
    failures: RepositoryScanningConfigurationFailureList | None


LayerDigestList = list[LayerDigest]


class CompleteLayerUploadRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryName: RepositoryName
    uploadId: UploadId
    layerDigests: LayerDigestList


class CompleteLayerUploadResponse(TypedDict, total=False):
    registryId: RegistryId | None
    repositoryName: RepositoryName | None
    uploadId: UploadId | None
    layerDigest: LayerDigest | None


class CreatePullThroughCacheRuleRequest(ServiceRequest):
    ecrRepositoryPrefix: PullThroughCacheRuleRepositoryPrefix
    upstreamRegistryUrl: Url
    registryId: RegistryId | None
    upstreamRegistry: UpstreamRegistry | None
    credentialArn: CredentialArn | None
    customRoleArn: CustomRoleArn | None
    upstreamRepositoryPrefix: PullThroughCacheRuleRepositoryPrefix | None


CreationTimestamp = datetime


class CreatePullThroughCacheRuleResponse(TypedDict, total=False):
    ecrRepositoryPrefix: PullThroughCacheRuleRepositoryPrefix | None
    upstreamRegistryUrl: Url | None
    createdAt: CreationTimestamp | None
    registryId: RegistryId | None
    upstreamRegistry: UpstreamRegistry | None
    credentialArn: CredentialArn | None
    customRoleArn: CustomRoleArn | None
    upstreamRepositoryPrefix: PullThroughCacheRuleRepositoryPrefix | None


RCTAppliedForList = list[RCTAppliedFor]


class ImageTagMutabilityExclusionFilter(TypedDict, total=False):
    """A filter that specifies which image tags should be excluded from the
    repository's image tag mutability setting.
    """

    filterType: ImageTagMutabilityExclusionFilterType
    filter: ImageTagMutabilityExclusionFilterValue


ImageTagMutabilityExclusionFilters = list[ImageTagMutabilityExclusionFilter]


class Tag(TypedDict, total=False):
    """The metadata to apply to a resource to help you categorize and organize
    them. Each tag consists of a key and a value, both of which you define.
    Tag keys can have a maximum character length of 128 characters, and tag
    values can have a maximum length of 256 characters.
    """

    Key: TagKey
    Value: TagValue


TagList = list[Tag]


class EncryptionConfigurationForRepositoryCreationTemplate(TypedDict, total=False):
    """The encryption configuration to associate with the repository creation
    template.
    """

    encryptionType: EncryptionType
    kmsKey: KmsKeyForRepositoryCreationTemplate | None


class CreateRepositoryCreationTemplateRequest(ServiceRequest):
    prefix: Prefix
    description: RepositoryTemplateDescription | None
    encryptionConfiguration: EncryptionConfigurationForRepositoryCreationTemplate | None
    resourceTags: TagList | None
    imageTagMutability: ImageTagMutability | None
    imageTagMutabilityExclusionFilters: ImageTagMutabilityExclusionFilters | None
    repositoryPolicy: RepositoryPolicyText | None
    lifecyclePolicy: LifecyclePolicyTextForRepositoryCreationTemplate | None
    appliedFor: RCTAppliedForList
    customRoleArn: CustomRoleArn | None


class RepositoryCreationTemplate(TypedDict, total=False):
    """The details of the repository creation template associated with the
    request.
    """

    prefix: Prefix | None
    description: RepositoryTemplateDescription | None
    encryptionConfiguration: EncryptionConfigurationForRepositoryCreationTemplate | None
    resourceTags: TagList | None
    imageTagMutability: ImageTagMutability | None
    imageTagMutabilityExclusionFilters: ImageTagMutabilityExclusionFilters | None
    repositoryPolicy: RepositoryPolicyText | None
    lifecyclePolicy: LifecyclePolicyTextForRepositoryCreationTemplate | None
    appliedFor: RCTAppliedForList | None
    customRoleArn: CustomRoleArn | None
    createdAt: Date | None
    updatedAt: Date | None


class CreateRepositoryCreationTemplateResponse(TypedDict, total=False):
    registryId: RegistryId | None
    repositoryCreationTemplate: RepositoryCreationTemplate | None


class EncryptionConfiguration(TypedDict, total=False):
    """The encryption configuration for the repository. This determines how the
    contents of your repository are encrypted at rest.

    By default, when no encryption configuration is set or the ``AES256``
    encryption type is used, Amazon ECR uses server-side encryption with
    Amazon S3-managed encryption keys which encrypts your data at rest using
    an AES256 encryption algorithm. This does not require any action on your
    part.

    For more control over the encryption of the contents of your repository,
    you can use server-side encryption with Key Management Service key
    stored in Key Management Service (KMS) to encrypt your images. For more
    information, see `Amazon ECR encryption at
    rest <https://docs.aws.amazon.com/AmazonECR/latest/userguide/encryption-at-rest.html>`__
    in the *Amazon Elastic Container Registry User Guide*.
    """

    encryptionType: EncryptionType
    kmsKey: KmsKey | None


class ImageScanningConfiguration(TypedDict, total=False):
    """The image scanning configuration for a repository."""

    scanOnPush: ScanOnPushFlag | None


class CreateRepositoryRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryName: RepositoryName
    tags: TagList | None
    imageTagMutability: ImageTagMutability | None
    imageTagMutabilityExclusionFilters: ImageTagMutabilityExclusionFilters | None
    imageScanningConfiguration: ImageScanningConfiguration | None
    encryptionConfiguration: EncryptionConfiguration | None


class Repository(TypedDict, total=False):
    """An object representing a repository."""

    repositoryArn: Arn | None
    registryId: RegistryId | None
    repositoryName: RepositoryName | None
    repositoryUri: Url | None
    createdAt: CreationTimestamp | None
    imageTagMutability: ImageTagMutability | None
    imageTagMutabilityExclusionFilters: ImageTagMutabilityExclusionFilters | None
    imageScanningConfiguration: ImageScanningConfiguration | None
    encryptionConfiguration: EncryptionConfiguration | None


class CreateRepositoryResponse(TypedDict, total=False):
    repository: Repository | None


class CvssScore(TypedDict, total=False):
    """The CVSS score for a finding."""

    baseScore: BaseScore | None
    scoringVector: ScoringVector | None
    source: Source | None
    version: Version | None


class CvssScoreAdjustment(TypedDict, total=False):
    """Details on adjustments Amazon Inspector made to the CVSS score for a
    finding.
    """

    metric: Metric | None
    reason: Reason | None


CvssScoreAdjustmentList = list[CvssScoreAdjustment]


class CvssScoreDetails(TypedDict, total=False):
    """Information about the CVSS score."""

    adjustments: CvssScoreAdjustmentList | None
    score: Score | None
    scoreSource: Source | None
    scoringVector: ScoringVector | None
    version: Version | None


CvssScoreList = list[CvssScore]


class DeleteLifecyclePolicyRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryName: RepositoryName


EvaluationTimestamp = datetime


class DeleteLifecyclePolicyResponse(TypedDict, total=False):
    registryId: RegistryId | None
    repositoryName: RepositoryName | None
    lifecyclePolicyText: LifecyclePolicyText | None
    lastEvaluatedAt: EvaluationTimestamp | None


class DeletePullThroughCacheRuleRequest(ServiceRequest):
    ecrRepositoryPrefix: PullThroughCacheRuleRepositoryPrefix
    registryId: RegistryId | None


class DeletePullThroughCacheRuleResponse(TypedDict, total=False):
    ecrRepositoryPrefix: PullThroughCacheRuleRepositoryPrefix | None
    upstreamRegistryUrl: Url | None
    createdAt: CreationTimestamp | None
    registryId: RegistryId | None
    credentialArn: CredentialArn | None
    customRoleArn: CustomRoleArn | None
    upstreamRepositoryPrefix: PullThroughCacheRuleRepositoryPrefix | None


class DeleteRegistryPolicyRequest(ServiceRequest):
    pass


class DeleteRegistryPolicyResponse(TypedDict, total=False):
    registryId: RegistryId | None
    policyText: RegistryPolicyText | None


class DeleteRepositoryCreationTemplateRequest(ServiceRequest):
    prefix: Prefix


class DeleteRepositoryCreationTemplateResponse(TypedDict, total=False):
    registryId: RegistryId | None
    repositoryCreationTemplate: RepositoryCreationTemplate | None


class DeleteRepositoryPolicyRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryName: RepositoryName


class DeleteRepositoryPolicyResponse(TypedDict, total=False):
    registryId: RegistryId | None
    repositoryName: RepositoryName | None
    policyText: RepositoryPolicyText | None


class DeleteRepositoryRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryName: RepositoryName
    force: ForceFlag | None


class DeleteRepositoryResponse(TypedDict, total=False):
    repository: Repository | None


class DeleteSigningConfigurationRequest(ServiceRequest):
    pass


class SigningRepositoryFilter(TypedDict, total=False):
    """A repository filter used to determine which repositories have their
    images automatically signed on push. Each filter consists of a filter
    type and filter value.
    """

    filter: SigningRepositoryFilterValue
    filterType: SigningRepositoryFilterType


SigningRepositoryFilterList = list[SigningRepositoryFilter]


class SigningRule(TypedDict, total=False):
    """A signing rule that specifies a signing profile and optional repository
    filters. When an image is pushed to a matching repository, a signing job
    is created using the specified profile.
    """

    signingProfileArn: SigningProfileArn
    repositoryFilters: SigningRepositoryFilterList | None


SigningRuleList = list[SigningRule]


class SigningConfiguration(TypedDict, total=False):
    """The signing configuration for a registry, which specifies rules for
    automatically signing images when pushed.
    """

    rules: SigningRuleList


class DeleteSigningConfigurationResponse(TypedDict, total=False):
    registryId: RegistryId | None
    signingConfiguration: SigningConfiguration | None


class DeregisterPullTimeUpdateExclusionRequest(ServiceRequest):
    principalArn: PrincipalArn


class DeregisterPullTimeUpdateExclusionResponse(TypedDict, total=False):
    principalArn: PrincipalArn | None


class DescribeImageReplicationStatusRequest(ServiceRequest):
    repositoryName: RepositoryName
    imageId: ImageIdentifier
    registryId: RegistryId | None


class ImageReplicationStatus(TypedDict, total=False):
    """The status of the replication process for an image."""

    region: Region | None
    registryId: RegistryId | None
    status: ReplicationStatus | None
    failureCode: ReplicationError | None


ImageReplicationStatusList = list[ImageReplicationStatus]


class DescribeImageReplicationStatusResponse(TypedDict, total=False):
    repositoryName: RepositoryName | None
    imageId: ImageIdentifier | None
    replicationStatuses: ImageReplicationStatusList | None


class DescribeImageScanFindingsRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryName: RepositoryName
    imageId: ImageIdentifier
    nextToken: NextToken | None
    maxResults: MaxResults | None


class ScoreDetails(TypedDict, total=False):
    """Information about the Amazon Inspector score given to a finding."""

    cvss: CvssScoreDetails | None


Tags = dict[TagKey, TagValue]


class ResourceDetails(TypedDict, total=False):
    """Contains details about the resource involved in the finding."""

    awsEcrContainerImage: AwsEcrContainerImageDetails | None


class Resource(TypedDict, total=False):
    details: ResourceDetails | None
    id: ResourceId | None
    tags: Tags | None
    type: Type | None


ResourceList = list[Resource]


class Recommendation(TypedDict, total=False):
    """Details about the recommended course of action to remediate the finding."""

    url: Url | None
    text: RecommendationText | None


class Remediation(TypedDict, total=False):
    """Information on how to remediate a finding."""

    recommendation: Recommendation | None


class VulnerablePackage(TypedDict, total=False):
    """Information on the vulnerable package identified by a finding."""

    arch: Arch | None
    epoch: Epoch | None
    filePath: FilePath | None
    name: VulnerablePackageName | None
    packageManager: PackageManager | None
    release: Release | None
    sourceLayerHash: SourceLayerHash | None
    version: Version | None
    fixedInVersion: FixedInVersion | None


VulnerablePackagesList = list[VulnerablePackage]
RelatedVulnerabilitiesList = list[RelatedVulnerability]
ReferenceUrlsList = list[Url]


class PackageVulnerabilityDetails(TypedDict, total=False):
    """Information about a package vulnerability finding."""

    cvss: CvssScoreList | None
    referenceUrls: ReferenceUrlsList | None
    relatedVulnerabilities: RelatedVulnerabilitiesList | None
    source: Source | None
    sourceUrl: Url | None
    vendorCreatedAt: Date | None
    vendorSeverity: Severity | None
    vendorUpdatedAt: Date | None
    vulnerabilityId: VulnerabilityId | None
    vulnerablePackages: VulnerablePackagesList | None


class EnhancedImageScanFinding(TypedDict, total=False):
    awsAccountId: RegistryId | None
    description: FindingDescription | None
    findingArn: FindingArn | None
    firstObservedAt: Date | None
    lastObservedAt: Date | None
    packageVulnerabilityDetails: PackageVulnerabilityDetails | None
    remediation: Remediation | None
    resources: ResourceList | None
    score: Score | None
    scoreDetails: ScoreDetails | None
    severity: Severity | None
    status: Status | None
    title: Title | None
    type: Type | None
    updatedAt: Date | None
    fixAvailable: FixAvailable | None
    exploitAvailable: ExploitAvailable | None


EnhancedImageScanFindingList = list[EnhancedImageScanFinding]


class ImageScanFinding(TypedDict, total=False):
    """Contains information about an image scan finding."""

    name: FindingName | None
    description: FindingDescription | None
    uri: Url | None
    severity: FindingSeverity | None
    attributes: AttributeList | None


ImageScanFindingList = list[ImageScanFinding]
FindingSeverityCounts = dict[FindingSeverity, SeverityCount]
VulnerabilitySourceUpdateTimestamp = datetime
ScanTimestamp = datetime


class ImageScanFindings(TypedDict, total=False):
    """The details of an image scan."""

    imageScanCompletedAt: ScanTimestamp | None
    vulnerabilitySourceUpdatedAt: VulnerabilitySourceUpdateTimestamp | None
    findingSeverityCounts: FindingSeverityCounts | None
    findings: ImageScanFindingList | None
    enhancedFindings: EnhancedImageScanFindingList | None


class ImageScanStatus(TypedDict, total=False):
    """The current status of an image scan."""

    status: ScanStatus | None
    description: ScanStatusDescription | None


class DescribeImageScanFindingsResponse(TypedDict, total=False):
    registryId: RegistryId | None
    repositoryName: RepositoryName | None
    imageId: ImageIdentifier | None
    imageScanStatus: ImageScanStatus | None
    imageScanFindings: ImageScanFindings | None
    nextToken: NextToken | None


class DescribeImageSigningStatusRequest(ServiceRequest):
    repositoryName: RepositoryName
    imageId: ImageIdentifier
    registryId: RegistryId | None


class ImageSigningStatus(TypedDict, total=False):
    """The signing status for an image. Each status corresponds to a signing
    profile.
    """

    signingProfileArn: SigningProfileArn | None
    failureCode: SigningStatusFailureCode | None
    failureReason: SigningStatusFailureReason | None
    status: SigningStatus | None


ImageSigningStatusList = list[ImageSigningStatus]


class DescribeImageSigningStatusResponse(TypedDict, total=False):
    repositoryName: RepositoryName | None
    imageId: ImageIdentifier | None
    registryId: RegistryId | None
    signingStatuses: ImageSigningStatusList | None


class DescribeImagesFilter(TypedDict, total=False):
    """An object representing a filter on a DescribeImages operation."""

    tagStatus: TagStatus | None
    imageStatus: ImageStatusFilter | None


class DescribeImagesRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryName: RepositoryName
    imageIds: ImageIdentifierList | None
    nextToken: NextToken | None
    maxResults: MaxResults | None
    filter: DescribeImagesFilter | None


LastActivatedAtTimestamp = datetime
LastArchivedAtTimestamp = datetime
RecordedPullTimestamp = datetime


class ImageScanFindingsSummary(TypedDict, total=False):
    """A summary of the last completed image scan."""

    imageScanCompletedAt: ScanTimestamp | None
    vulnerabilitySourceUpdatedAt: VulnerabilitySourceUpdateTimestamp | None
    findingSeverityCounts: FindingSeverityCounts | None


PushTimestamp = datetime
ImageSizeInBytes = int
ImageTagList = list[ImageTag]


class ImageDetail(TypedDict, total=False):
    """An object that describes an image returned by a DescribeImages
    operation.
    """

    registryId: RegistryId | None
    repositoryName: RepositoryName | None
    imageDigest: ImageDigest | None
    imageTags: ImageTagList | None
    imageSizeInBytes: ImageSizeInBytes | None
    imagePushedAt: PushTimestamp | None
    imageScanStatus: ImageScanStatus | None
    imageScanFindingsSummary: ImageScanFindingsSummary | None
    imageManifestMediaType: MediaType | None
    artifactMediaType: MediaType | None
    lastRecordedPullTime: RecordedPullTimestamp | None
    subjectManifestDigest: ImageDigest | None
    imageStatus: ImageStatus | None
    lastArchivedAt: LastArchivedAtTimestamp | None
    lastActivatedAt: LastActivatedAtTimestamp | None


ImageDetailList = list[ImageDetail]


class DescribeImagesResponse(TypedDict, total=False):
    imageDetails: ImageDetailList | None
    nextToken: NextToken | None


PullThroughCacheRuleRepositoryPrefixList = list[PullThroughCacheRuleRepositoryPrefix]


class DescribePullThroughCacheRulesRequest(ServiceRequest):
    registryId: RegistryId | None
    ecrRepositoryPrefixes: PullThroughCacheRuleRepositoryPrefixList | None
    nextToken: NextToken | None
    maxResults: MaxResults | None


UpdatedTimestamp = datetime


class PullThroughCacheRule(TypedDict, total=False):
    """The details of a pull through cache rule."""

    ecrRepositoryPrefix: PullThroughCacheRuleRepositoryPrefix | None
    upstreamRegistryUrl: Url | None
    createdAt: CreationTimestamp | None
    registryId: RegistryId | None
    credentialArn: CredentialArn | None
    customRoleArn: CustomRoleArn | None
    upstreamRepositoryPrefix: PullThroughCacheRuleRepositoryPrefix | None
    upstreamRegistry: UpstreamRegistry | None
    updatedAt: UpdatedTimestamp | None


PullThroughCacheRuleList = list[PullThroughCacheRule]


class DescribePullThroughCacheRulesResponse(TypedDict, total=False):
    pullThroughCacheRules: PullThroughCacheRuleList | None
    nextToken: NextToken | None


class DescribeRegistryRequest(ServiceRequest):
    pass


class RepositoryFilter(TypedDict, total=False):
    """The filter settings used with image replication. Specifying a repository
    filter to a replication rule provides a method for controlling which
    repositories in a private registry are replicated. If no filters are
    added, the contents of all repositories are replicated.
    """

    filter: RepositoryFilterValue
    filterType: RepositoryFilterType


RepositoryFilterList = list[RepositoryFilter]


class ReplicationDestination(TypedDict, total=False):
    """An array of objects representing the destination for a replication rule."""

    region: Region
    registryId: RegistryId


ReplicationDestinationList = list[ReplicationDestination]


class ReplicationRule(TypedDict, total=False):
    """An array of objects representing the replication destinations and
    repository filters for a replication configuration.
    """

    destinations: ReplicationDestinationList
    repositoryFilters: RepositoryFilterList | None


ReplicationRuleList = list[ReplicationRule]


class ReplicationConfiguration(TypedDict, total=False):
    """The replication configuration for a registry."""

    rules: ReplicationRuleList


class DescribeRegistryResponse(TypedDict, total=False):
    registryId: RegistryId | None
    replicationConfiguration: ReplicationConfiguration | None


RepositoryNameList = list[RepositoryName]


class DescribeRepositoriesRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryNames: RepositoryNameList | None
    nextToken: NextToken | None
    maxResults: MaxResults | None


RepositoryList = list[Repository]


class DescribeRepositoriesResponse(TypedDict, total=False):
    repositories: RepositoryList | None
    nextToken: NextToken | None


PrefixList = list[Prefix]


class DescribeRepositoryCreationTemplatesRequest(ServiceRequest):
    prefixes: PrefixList | None
    nextToken: NextToken | None
    maxResults: MaxResults | None


RepositoryCreationTemplateList = list[RepositoryCreationTemplate]


class DescribeRepositoryCreationTemplatesResponse(TypedDict, total=False):
    registryId: RegistryId | None
    repositoryCreationTemplates: RepositoryCreationTemplateList | None
    nextToken: NextToken | None


class GetAccountSettingRequest(ServiceRequest):
    name: AccountSettingName


class GetAccountSettingResponse(TypedDict, total=False):
    name: AccountSettingName | None
    value: AccountSettingName | None


GetAuthorizationTokenRegistryIdList = list[RegistryId]


class GetAuthorizationTokenRequest(ServiceRequest):
    registryIds: GetAuthorizationTokenRegistryIdList | None


class GetAuthorizationTokenResponse(TypedDict, total=False):
    authorizationData: AuthorizationDataList | None


class GetDownloadUrlForLayerRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryName: RepositoryName
    layerDigest: LayerDigest


class GetDownloadUrlForLayerResponse(TypedDict, total=False):
    downloadUrl: Url | None
    layerDigest: LayerDigest | None


class LifecyclePolicyPreviewFilter(TypedDict, total=False):
    """The filter for the lifecycle policy preview."""

    tagStatus: TagStatus | None


class GetLifecyclePolicyPreviewRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryName: RepositoryName
    imageIds: ImageIdentifierList | None
    nextToken: NextToken | None
    maxResults: LifecyclePreviewMaxResults | None
    filter: LifecyclePolicyPreviewFilter | None


class TransitioningImageTotalCount(TypedDict, total=False):
    """The total count of images transitioning to a storage class."""

    targetStorageClass: LifecyclePolicyTargetStorageClass | None
    imageTotalCount: ImageCount | None


TransitioningImageTotalCounts = list[TransitioningImageTotalCount]


class LifecyclePolicyPreviewSummary(TypedDict, total=False):
    """The summary of the lifecycle policy preview request."""

    expiringImageTotalCount: ImageCount | None
    transitioningImageTotalCounts: TransitioningImageTotalCounts | None


class LifecyclePolicyRuleAction(TypedDict, total=False):
    type: ImageActionType | None
    targetStorageClass: LifecyclePolicyTargetStorageClass | None


class LifecyclePolicyPreviewResult(TypedDict, total=False):
    """The result of the lifecycle policy preview."""

    imageTags: ImageTagList | None
    imageDigest: ImageDigest | None
    imagePushedAt: PushTimestamp | None
    action: LifecyclePolicyRuleAction | None
    appliedRulePriority: LifecyclePolicyRulePriority | None
    storageClass: LifecyclePolicyStorageClass | None


LifecyclePolicyPreviewResultList = list[LifecyclePolicyPreviewResult]


class GetLifecyclePolicyPreviewResponse(TypedDict, total=False):
    registryId: RegistryId | None
    repositoryName: RepositoryName | None
    lifecyclePolicyText: LifecyclePolicyText | None
    status: LifecyclePolicyPreviewStatus | None
    nextToken: NextToken | None
    previewResults: LifecyclePolicyPreviewResultList | None
    summary: LifecyclePolicyPreviewSummary | None


class GetLifecyclePolicyRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryName: RepositoryName


class GetLifecyclePolicyResponse(TypedDict, total=False):
    registryId: RegistryId | None
    repositoryName: RepositoryName | None
    lifecyclePolicyText: LifecyclePolicyText | None
    lastEvaluatedAt: EvaluationTimestamp | None


class GetRegistryPolicyRequest(ServiceRequest):
    pass


class GetRegistryPolicyResponse(TypedDict, total=False):
    registryId: RegistryId | None
    policyText: RegistryPolicyText | None


class GetRegistryScanningConfigurationRequest(ServiceRequest):
    pass


class RegistryScanningRule(TypedDict, total=False):
    """The details of a scanning rule for a private registry."""

    scanFrequency: ScanFrequency
    repositoryFilters: ScanningRepositoryFilterList


RegistryScanningRuleList = list[RegistryScanningRule]


class RegistryScanningConfiguration(TypedDict, total=False):
    """The scanning configuration for a private registry."""

    scanType: ScanType | None
    rules: RegistryScanningRuleList | None


class GetRegistryScanningConfigurationResponse(TypedDict, total=False):
    registryId: RegistryId | None
    scanningConfiguration: RegistryScanningConfiguration | None


class GetRepositoryPolicyRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryName: RepositoryName


class GetRepositoryPolicyResponse(TypedDict, total=False):
    registryId: RegistryId | None
    repositoryName: RepositoryName | None
    policyText: RepositoryPolicyText | None


class GetSigningConfigurationRequest(ServiceRequest):
    pass


class GetSigningConfigurationResponse(TypedDict, total=False):
    registryId: RegistryId | None
    signingConfiguration: SigningConfiguration | None


class ImageReferrer(TypedDict, total=False):
    """An object representing an artifact associated with a subject image."""

    digest: ImageDigest
    mediaType: MediaType
    artifactType: ArtifactType | None
    size: ImageSizeInBytes
    annotations: Annotations | None
    artifactStatus: ArtifactStatus | None


ImageReferrerList = list[ImageReferrer]


class InitiateLayerUploadRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryName: RepositoryName


class InitiateLayerUploadResponse(TypedDict, total=False):
    uploadId: UploadId | None
    partSize: PartSize | None


LayerPartBlob = bytes


class ListImageReferrersFilter(TypedDict, total=False):
    """An object representing a filter on a ListImageReferrers operation."""

    artifactTypes: ArtifactTypeList | None
    artifactStatus: ArtifactStatusFilter | None


class SubjectIdentifier(TypedDict, total=False):
    """An object that identifies an image subject."""

    imageDigest: ImageDigest


class ListImageReferrersRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryName: RepositoryName
    subjectId: SubjectIdentifier
    filter: ListImageReferrersFilter | None
    nextToken: NextToken | None
    maxResults: FiftyMaxResults | None


class ListImageReferrersResponse(TypedDict, total=False):
    referrers: ImageReferrerList | None
    nextToken: NextToken | None


class ListImagesFilter(TypedDict, total=False):
    """An object representing a filter on a ListImages operation."""

    tagStatus: TagStatus | None
    imageStatus: ImageStatusFilter | None


class ListImagesRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryName: RepositoryName
    nextToken: NextToken | None
    maxResults: MaxResults | None
    filter: ListImagesFilter | None


class ListImagesResponse(TypedDict, total=False):
    imageIds: ImageIdentifierList | None
    nextToken: NextToken | None


class ListPullTimeUpdateExclusionsRequest(ServiceRequest):
    maxResults: MaxResults | None
    nextToken: NextToken | None


PullTimeUpdateExclusionList = list[PrincipalArn]


class ListPullTimeUpdateExclusionsResponse(TypedDict, total=False):
    pullTimeUpdateExclusions: PullTimeUpdateExclusionList | None
    nextToken: NextToken | None


class ListTagsForResourceRequest(ServiceRequest):
    resourceArn: Arn


class ListTagsForResourceResponse(TypedDict, total=False):
    tags: TagList | None


class PutAccountSettingRequest(ServiceRequest):
    name: AccountSettingName
    value: AccountSettingValue


class PutAccountSettingResponse(TypedDict, total=False):
    name: AccountSettingName | None
    value: AccountSettingValue | None


class PutImageRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryName: RepositoryName
    imageManifest: ImageManifest
    imageManifestMediaType: MediaType | None
    imageTag: ImageTag | None
    imageDigest: ImageDigest | None


class PutImageResponse(TypedDict, total=False):
    image: Image | None


class PutImageScanningConfigurationRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryName: RepositoryName
    imageScanningConfiguration: ImageScanningConfiguration


class PutImageScanningConfigurationResponse(TypedDict, total=False):
    registryId: RegistryId | None
    repositoryName: RepositoryName | None
    imageScanningConfiguration: ImageScanningConfiguration | None


class PutImageTagMutabilityRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryName: RepositoryName
    imageTagMutability: ImageTagMutability
    imageTagMutabilityExclusionFilters: ImageTagMutabilityExclusionFilters | None


class PutImageTagMutabilityResponse(TypedDict, total=False):
    registryId: RegistryId | None
    repositoryName: RepositoryName | None
    imageTagMutability: ImageTagMutability | None
    imageTagMutabilityExclusionFilters: ImageTagMutabilityExclusionFilters | None


class PutLifecyclePolicyRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryName: RepositoryName
    lifecyclePolicyText: LifecyclePolicyText


class PutLifecyclePolicyResponse(TypedDict, total=False):
    registryId: RegistryId | None
    repositoryName: RepositoryName | None
    lifecyclePolicyText: LifecyclePolicyText | None


class PutRegistryPolicyRequest(ServiceRequest):
    policyText: RegistryPolicyText


class PutRegistryPolicyResponse(TypedDict, total=False):
    registryId: RegistryId | None
    policyText: RegistryPolicyText | None


class PutRegistryScanningConfigurationRequest(ServiceRequest):
    scanType: ScanType | None
    rules: RegistryScanningRuleList | None


class PutRegistryScanningConfigurationResponse(TypedDict, total=False):
    registryScanningConfiguration: RegistryScanningConfiguration | None


class PutReplicationConfigurationRequest(ServiceRequest):
    replicationConfiguration: ReplicationConfiguration


class PutReplicationConfigurationResponse(TypedDict, total=False):
    replicationConfiguration: ReplicationConfiguration | None


class PutSigningConfigurationRequest(ServiceRequest):
    signingConfiguration: SigningConfiguration


class PutSigningConfigurationResponse(TypedDict, total=False):
    signingConfiguration: SigningConfiguration | None


class RegisterPullTimeUpdateExclusionRequest(ServiceRequest):
    principalArn: PrincipalArn


class RegisterPullTimeUpdateExclusionResponse(TypedDict, total=False):
    principalArn: PrincipalArn | None
    createdAt: CreationTimestamp | None


class SetRepositoryPolicyRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryName: RepositoryName
    policyText: RepositoryPolicyText
    force: ForceFlag | None


class SetRepositoryPolicyResponse(TypedDict, total=False):
    registryId: RegistryId | None
    repositoryName: RepositoryName | None
    policyText: RepositoryPolicyText | None


class StartImageScanRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryName: RepositoryName
    imageId: ImageIdentifier


class StartImageScanResponse(TypedDict, total=False):
    registryId: RegistryId | None
    repositoryName: RepositoryName | None
    imageId: ImageIdentifier | None
    imageScanStatus: ImageScanStatus | None


class StartLifecyclePolicyPreviewRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryName: RepositoryName
    lifecyclePolicyText: LifecyclePolicyText | None


class StartLifecyclePolicyPreviewResponse(TypedDict, total=False):
    registryId: RegistryId | None
    repositoryName: RepositoryName | None
    lifecyclePolicyText: LifecyclePolicyText | None
    status: LifecyclePolicyPreviewStatus | None


TagKeyList = list[TagKey]


class TagResourceRequest(ServiceRequest):
    resourceArn: Arn
    tags: TagList


class TagResourceResponse(TypedDict, total=False):
    pass


class UntagResourceRequest(ServiceRequest):
    resourceArn: Arn
    tagKeys: TagKeyList


class UntagResourceResponse(TypedDict, total=False):
    pass


class UpdateImageStorageClassRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryName: RepositoryName
    imageId: ImageIdentifier
    targetStorageClass: TargetStorageClass


class UpdateImageStorageClassResponse(TypedDict, total=False):
    registryId: RegistryId | None
    repositoryName: RepositoryName | None
    imageId: ImageIdentifier | None
    imageStatus: ImageStatus | None


class UpdatePullThroughCacheRuleRequest(ServiceRequest):
    registryId: RegistryId | None
    ecrRepositoryPrefix: PullThroughCacheRuleRepositoryPrefix
    credentialArn: CredentialArn | None
    customRoleArn: CustomRoleArn | None


class UpdatePullThroughCacheRuleResponse(TypedDict, total=False):
    ecrRepositoryPrefix: PullThroughCacheRuleRepositoryPrefix | None
    registryId: RegistryId | None
    updatedAt: UpdatedTimestamp | None
    credentialArn: CredentialArn | None
    customRoleArn: CustomRoleArn | None
    upstreamRepositoryPrefix: PullThroughCacheRuleRepositoryPrefix | None


class UpdateRepositoryCreationTemplateRequest(ServiceRequest):
    prefix: Prefix
    description: RepositoryTemplateDescription | None
    encryptionConfiguration: EncryptionConfigurationForRepositoryCreationTemplate | None
    resourceTags: TagList | None
    imageTagMutability: ImageTagMutability | None
    imageTagMutabilityExclusionFilters: ImageTagMutabilityExclusionFilters | None
    repositoryPolicy: RepositoryPolicyText | None
    lifecyclePolicy: LifecyclePolicyTextForRepositoryCreationTemplate | None
    appliedFor: RCTAppliedForList | None
    customRoleArn: CustomRoleArn | None


class UpdateRepositoryCreationTemplateResponse(TypedDict, total=False):
    registryId: RegistryId | None
    repositoryCreationTemplate: RepositoryCreationTemplate | None


class UploadLayerPartRequest(ServiceRequest):
    registryId: RegistryId | None
    repositoryName: RepositoryName
    uploadId: UploadId
    partFirstByte: PartSize
    partLastByte: PartSize
    layerPartBlob: LayerPartBlob


class UploadLayerPartResponse(TypedDict, total=False):
    registryId: RegistryId | None
    repositoryName: RepositoryName | None
    uploadId: UploadId | None
    lastByteReceived: PartSize | None


class ValidatePullThroughCacheRuleRequest(ServiceRequest):
    ecrRepositoryPrefix: PullThroughCacheRuleRepositoryPrefix
    registryId: RegistryId | None


class ValidatePullThroughCacheRuleResponse(TypedDict, total=False):
    ecrRepositoryPrefix: PullThroughCacheRuleRepositoryPrefix | None
    registryId: RegistryId | None
    upstreamRegistryUrl: Url | None
    credentialArn: CredentialArn | None
    customRoleArn: CustomRoleArn | None
    upstreamRepositoryPrefix: PullThroughCacheRuleRepositoryPrefix | None
    isValid: IsPTCRuleValid | None
    failure: PTCValidateFailure | None


class EcrApi:
    service: str = "ecr"
    version: str = "2015-09-21"

    @handler("BatchCheckLayerAvailability")
    def batch_check_layer_availability(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        layer_digests: BatchedOperationLayerDigestList,
        registry_id: RegistryId | None = None,
        **kwargs,
    ) -> BatchCheckLayerAvailabilityResponse:
        """Checks the availability of one or more image layers in a repository.

        When an image is pushed to a repository, each image layer is checked to
        verify if it has been uploaded before. If it has been uploaded, then the
        image layer is skipped.

        This operation is used by the Amazon ECR proxy and is not generally used
        by customers for pulling and pushing images. In most cases, you should
        use the ``docker`` CLI to pull, tag, and push images.

        :param repository_name: The name of the repository that is associated with the image layers to
        check.
        :param layer_digests: The digests of the image layers to check.
        :param registry_id: The Amazon Web Services account ID associated with the registry that
        contains the image layers to check.
        :returns: BatchCheckLayerAvailabilityResponse
        :raises RepositoryNotFoundException:
        :raises InvalidParameterException:
        :raises ServerException:
        """
        raise NotImplementedError

    @handler("BatchDeleteImage")
    def batch_delete_image(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        image_ids: ImageIdentifierList,
        registry_id: RegistryId | None = None,
        **kwargs,
    ) -> BatchDeleteImageResponse:
        """Deletes a list of specified images within a repository. Images are
        specified with either an ``imageTag`` or ``imageDigest``.

        You can remove a tag from an image by specifying the image's tag in your
        request. When you remove the last tag from an image, the image is
        deleted from your repository.

        You can completely delete an image (and all of its tags) by specifying
        the image's digest in your request.

        :param repository_name: The repository that contains the image to delete.
        :param image_ids: A list of image ID references that correspond to images to delete.
        :param registry_id: The Amazon Web Services account ID associated with the registry that
        contains the image to delete.
        :returns: BatchDeleteImageResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises RepositoryNotFoundException:
        """
        raise NotImplementedError

    @handler("BatchGetImage")
    def batch_get_image(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        image_ids: ImageIdentifierList,
        registry_id: RegistryId | None = None,
        accepted_media_types: MediaTypeList | None = None,
        **kwargs,
    ) -> BatchGetImageResponse:
        """Gets detailed information for an image. Images are specified with either
        an ``imageTag`` or ``imageDigest``.

        When an image is pulled, the BatchGetImage API is called once to
        retrieve the image manifest.

        :param repository_name: The repository that contains the images to describe.
        :param image_ids: A list of image ID references that correspond to images to describe.
        :param registry_id: The Amazon Web Services account ID associated with the registry that
        contains the images to describe.
        :param accepted_media_types: The accepted media types for the request.
        :returns: BatchGetImageResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises RepositoryNotFoundException:
        :raises LimitExceededException:
        :raises UnableToGetUpstreamImageException:
        """
        raise NotImplementedError

    @handler("BatchGetRepositoryScanningConfiguration")
    def batch_get_repository_scanning_configuration(
        self,
        context: RequestContext,
        repository_names: ScanningConfigurationRepositoryNameList,
        **kwargs,
    ) -> BatchGetRepositoryScanningConfigurationResponse:
        """Gets the scanning configuration for one or more repositories.

        :param repository_names: One or more repository names to get the scanning configuration for.
        :returns: BatchGetRepositoryScanningConfigurationResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises RepositoryNotFoundException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("CompleteLayerUpload")
    def complete_layer_upload(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        upload_id: UploadId,
        layer_digests: LayerDigestList,
        registry_id: RegistryId | None = None,
        **kwargs,
    ) -> CompleteLayerUploadResponse:
        """Informs Amazon ECR that the image layer upload has completed for a
        specified registry, repository name, and upload ID. You can optionally
        provide a ``sha256`` digest of the image layer for data validation
        purposes.

        When an image is pushed, the CompleteLayerUpload API is called once per
        each new image layer to verify that the upload has completed.

        This operation is used by the Amazon ECR proxy and is not generally used
        by customers for pulling and pushing images. In most cases, you should
        use the ``docker`` CLI to pull, tag, and push images.

        :param repository_name: The name of the repository to associate with the image layer.
        :param upload_id: The upload ID from a previous InitiateLayerUpload operation to associate
        with the image layer.
        :param layer_digests: The ``sha256`` digest of the image layer.
        :param registry_id: The Amazon Web Services account ID associated with the registry to which
        to upload layers.
        :returns: CompleteLayerUploadResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises RepositoryNotFoundException:
        :raises UploadNotFoundException:
        :raises InvalidLayerException:
        :raises LayerPartTooSmallException:
        :raises LayerAlreadyExistsException:
        :raises EmptyUploadException:
        :raises KmsException:
        """
        raise NotImplementedError

    @handler("CreatePullThroughCacheRule")
    def create_pull_through_cache_rule(
        self,
        context: RequestContext,
        ecr_repository_prefix: PullThroughCacheRuleRepositoryPrefix,
        upstream_registry_url: Url,
        registry_id: RegistryId | None = None,
        upstream_registry: UpstreamRegistry | None = None,
        credential_arn: CredentialArn | None = None,
        custom_role_arn: CustomRoleArn | None = None,
        upstream_repository_prefix: PullThroughCacheRuleRepositoryPrefix | None = None,
        **kwargs,
    ) -> CreatePullThroughCacheRuleResponse:
        """Creates a pull through cache rule. A pull through cache rule provides a
        way to cache images from an upstream registry source in your Amazon ECR
        private registry. For more information, see `Using pull through cache
        rules <https://docs.aws.amazon.com/AmazonECR/latest/userguide/pull-through-cache.html>`__
        in the *Amazon Elastic Container Registry User Guide*.

        :param ecr_repository_prefix: The repository name prefix to use when caching images from the source
        registry.
        :param upstream_registry_url: The registry URL of the upstream public registry to use as the source
        for the pull through cache rule.
        :param registry_id: The Amazon Web Services account ID associated with the registry to
        create the pull through cache rule for.
        :param upstream_registry: The name of the upstream registry.
        :param credential_arn: The Amazon Resource Name (ARN) of the Amazon Web Services Secrets
        Manager secret that identifies the credentials to authenticate to the
        upstream registry.
        :param custom_role_arn: Amazon Resource Name (ARN) of the IAM role to be assumed by Amazon ECR
        to authenticate to the ECR upstream registry.
        :param upstream_repository_prefix: The repository name prefix of the upstream registry to match with the
        upstream repository name.
        :returns: CreatePullThroughCacheRuleResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises ValidationException:
        :raises PullThroughCacheRuleAlreadyExistsException:
        :raises UnsupportedUpstreamRegistryException:
        :raises LimitExceededException:
        :raises UnableToAccessSecretException:
        :raises SecretNotFoundException:
        :raises UnableToDecryptSecretValueException:
        """
        raise NotImplementedError

    @handler("CreateRepository")
    def create_repository(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        registry_id: RegistryId | None = None,
        tags: TagList | None = None,
        image_tag_mutability: ImageTagMutability | None = None,
        image_tag_mutability_exclusion_filters: ImageTagMutabilityExclusionFilters | None = None,
        image_scanning_configuration: ImageScanningConfiguration | None = None,
        encryption_configuration: EncryptionConfiguration | None = None,
        **kwargs,
    ) -> CreateRepositoryResponse:
        """Creates a repository. For more information, see `Amazon ECR
        repositories <https://docs.aws.amazon.com/AmazonECR/latest/userguide/Repositories.html>`__
        in the *Amazon Elastic Container Registry User Guide*.

        :param repository_name: The name to use for the repository.
        :param registry_id: The Amazon Web Services account ID associated with the registry to
        create the repository.
        :param tags: The metadata that you apply to the repository to help you categorize and
        organize them.
        :param image_tag_mutability: The tag mutability setting for the repository.
        :param image_tag_mutability_exclusion_filters: A list of filters that specify which image tags should be excluded from
        the repository's image tag mutability setting.
        :param image_scanning_configuration: The ``imageScanningConfiguration`` parameter is being deprecated, in
        favor of specifying the image scanning configuration at the registry
        level.
        :param encryption_configuration: The encryption configuration for the repository.
        :returns: CreateRepositoryResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises InvalidTagParameterException:
        :raises TooManyTagsException:
        :raises RepositoryAlreadyExistsException:
        :raises LimitExceededException:
        :raises KmsException:
        """
        raise NotImplementedError

    @handler("CreateRepositoryCreationTemplate")
    def create_repository_creation_template(
        self,
        context: RequestContext,
        prefix: Prefix,
        applied_for: RCTAppliedForList,
        description: RepositoryTemplateDescription | None = None,
        encryption_configuration: EncryptionConfigurationForRepositoryCreationTemplate
        | None = None,
        resource_tags: TagList | None = None,
        image_tag_mutability: ImageTagMutability | None = None,
        image_tag_mutability_exclusion_filters: ImageTagMutabilityExclusionFilters | None = None,
        repository_policy: RepositoryPolicyText | None = None,
        lifecycle_policy: LifecyclePolicyTextForRepositoryCreationTemplate | None = None,
        custom_role_arn: CustomRoleArn | None = None,
        **kwargs,
    ) -> CreateRepositoryCreationTemplateResponse:
        """Creates a repository creation template. This template is used to define
        the settings for repositories created by Amazon ECR on your behalf. For
        example, repositories created through pull through cache actions. For
        more information, see `Private repository creation
        templates <https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-creation-templates.html>`__
        in the *Amazon Elastic Container Registry User Guide*.

        :param prefix: The repository namespace prefix to associate with the template.
        :param applied_for: A list of enumerable strings representing the Amazon ECR repository
        creation scenarios that this template will apply towards.
        :param description: A description for the repository creation template.
        :param encryption_configuration: The encryption configuration to use for repositories created using the
        template.
        :param resource_tags: The metadata to apply to the repository to help you categorize and
        organize.
        :param image_tag_mutability: The tag mutability setting for the repository.
        :param image_tag_mutability_exclusion_filters: A list of filters that specify which image tags should be excluded from
        the repository creation template's image tag mutability setting.
        :param repository_policy: The repository policy to apply to repositories created using the
        template.
        :param lifecycle_policy: The lifecycle policy to use for repositories created using the template.
        :param custom_role_arn: The ARN of the role to be assumed by Amazon ECR.
        :returns: CreateRepositoryCreationTemplateResponse
        :raises ServerException:
        :raises ValidationException:
        :raises InvalidParameterException:
        :raises LimitExceededException:
        :raises TemplateAlreadyExistsException:
        """
        raise NotImplementedError

    @handler("DeleteLifecyclePolicy")
    def delete_lifecycle_policy(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        registry_id: RegistryId | None = None,
        **kwargs,
    ) -> DeleteLifecyclePolicyResponse:
        """Deletes the lifecycle policy associated with the specified repository.

        :param repository_name: The name of the repository.
        :param registry_id: The Amazon Web Services account ID associated with the registry that
        contains the repository.
        :returns: DeleteLifecyclePolicyResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises RepositoryNotFoundException:
        :raises LifecyclePolicyNotFoundException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("DeletePullThroughCacheRule")
    def delete_pull_through_cache_rule(
        self,
        context: RequestContext,
        ecr_repository_prefix: PullThroughCacheRuleRepositoryPrefix,
        registry_id: RegistryId | None = None,
        **kwargs,
    ) -> DeletePullThroughCacheRuleResponse:
        """Deletes a pull through cache rule.

        :param ecr_repository_prefix: The Amazon ECR repository prefix associated with the pull through cache
        rule to delete.
        :param registry_id: The Amazon Web Services account ID associated with the registry that
        contains the pull through cache rule.
        :returns: DeletePullThroughCacheRuleResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises ValidationException:
        :raises PullThroughCacheRuleNotFoundException:
        """
        raise NotImplementedError

    @handler("DeleteRegistryPolicy")
    def delete_registry_policy(
        self, context: RequestContext, **kwargs
    ) -> DeleteRegistryPolicyResponse:
        """Deletes the registry permissions policy.

        :returns: DeleteRegistryPolicyResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises RegistryPolicyNotFoundException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("DeleteRepository")
    def delete_repository(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        registry_id: RegistryId | None = None,
        force: ForceFlag | None = None,
        **kwargs,
    ) -> DeleteRepositoryResponse:
        """Deletes a repository. If the repository isn't empty, you must either
        delete the contents of the repository or use the ``force`` option to
        delete the repository and have Amazon ECR delete all of its contents on
        your behalf.

        :param repository_name: The name of the repository to delete.
        :param registry_id: The Amazon Web Services account ID associated with the registry that
        contains the repository to delete.
        :param force: If true, deleting the repository force deletes the contents of the
        repository.
        :returns: DeleteRepositoryResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises RepositoryNotFoundException:
        :raises RepositoryNotEmptyException:
        :raises KmsException:
        """
        raise NotImplementedError

    @handler("DeleteRepositoryCreationTemplate")
    def delete_repository_creation_template(
        self, context: RequestContext, prefix: Prefix, **kwargs
    ) -> DeleteRepositoryCreationTemplateResponse:
        """Deletes a repository creation template.

        :param prefix: The repository namespace prefix associated with the repository creation
        template.
        :returns: DeleteRepositoryCreationTemplateResponse
        :raises ServerException:
        :raises ValidationException:
        :raises InvalidParameterException:
        :raises TemplateNotFoundException:
        """
        raise NotImplementedError

    @handler("DeleteRepositoryPolicy")
    def delete_repository_policy(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        registry_id: RegistryId | None = None,
        **kwargs,
    ) -> DeleteRepositoryPolicyResponse:
        """Deletes the repository policy associated with the specified repository.

        :param repository_name: The name of the repository that is associated with the repository policy
        to delete.
        :param registry_id: The Amazon Web Services account ID associated with the registry that
        contains the repository policy to delete.
        :returns: DeleteRepositoryPolicyResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises RepositoryNotFoundException:
        :raises RepositoryPolicyNotFoundException:
        """
        raise NotImplementedError

    @handler("DeleteSigningConfiguration")
    def delete_signing_configuration(
        self, context: RequestContext, **kwargs
    ) -> DeleteSigningConfigurationResponse:
        """Deletes the registry's signing configuration. Images pushed after
        deletion of the signing configuration will no longer be automatically
        signed.

        For more information, see `Managed
        signing <https://docs.aws.amazon.com/AmazonECR/latest/userguide/managed-signing.html>`__
        in the *Amazon Elastic Container Registry User Guide*.

        Deleting the signing configuration does not affect existing image
        signatures.

        :returns: DeleteSigningConfigurationResponse
        :raises ServerException:
        :raises ValidationException:
        :raises SigningConfigurationNotFoundException:
        """
        raise NotImplementedError

    @handler("DeregisterPullTimeUpdateExclusion")
    def deregister_pull_time_update_exclusion(
        self, context: RequestContext, principal_arn: PrincipalArn, **kwargs
    ) -> DeregisterPullTimeUpdateExclusionResponse:
        """Removes a principal from the pull time update exclusion list for a
        registry. Once removed, Amazon ECR will resume updating the pull time if
        the specified principal pulls an image.

        :param principal_arn: The ARN of the IAM principal to remove from the pull time update
        exclusion list.
        :returns: DeregisterPullTimeUpdateExclusionResponse
        :raises InvalidParameterException:
        :raises ExclusionNotFoundException:
        :raises LimitExceededException:
        :raises ValidationException:
        :raises ServerException:
        """
        raise NotImplementedError

    @handler("DescribeImageReplicationStatus")
    def describe_image_replication_status(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        image_id: ImageIdentifier,
        registry_id: RegistryId | None = None,
        **kwargs,
    ) -> DescribeImageReplicationStatusResponse:
        """Returns the replication status for a specified image.

        :param repository_name: The name of the repository that the image is in.
        :param image_id: An object with identifying information for an image in an Amazon ECR
        repository.
        :param registry_id: The Amazon Web Services account ID associated with the registry.
        :returns: DescribeImageReplicationStatusResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises ImageNotFoundException:
        :raises RepositoryNotFoundException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("DescribeImageScanFindings")
    def describe_image_scan_findings(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        image_id: ImageIdentifier,
        registry_id: RegistryId | None = None,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> DescribeImageScanFindingsResponse:
        """Returns the scan findings for the specified image.

        :param repository_name: The repository for the image for which to describe the scan findings.
        :param image_id: An object with identifying information for an image in an Amazon ECR
        repository.
        :param registry_id: The Amazon Web Services account ID associated with the registry that
        contains the repository in which to describe the image scan findings
        for.
        :param next_token: The ``nextToken`` value returned from a previous paginated
        ``DescribeImageScanFindings`` request where ``maxResults`` was used and
        the results exceeded the value of that parameter.
        :param max_results: The maximum number of image scan results returned by
        ``DescribeImageScanFindings`` in paginated output.
        :returns: DescribeImageScanFindingsResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises RepositoryNotFoundException:
        :raises ImageNotFoundException:
        :raises ScanNotFoundException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("DescribeImageSigningStatus")
    def describe_image_signing_status(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        image_id: ImageIdentifier,
        registry_id: RegistryId | None = None,
        **kwargs,
    ) -> DescribeImageSigningStatusResponse:
        """Returns the signing status for a specified image. If the image matched
        signing rules that reference different signing profiles, a status is
        returned for each profile.

        For more information, see `Managed
        signing <https://docs.aws.amazon.com/AmazonECR/latest/userguide/managed-signing.html>`__
        in the *Amazon Elastic Container Registry User Guide*.

        :param repository_name: The name of the repository that contains the image.
        :param image_id: An object containing identifying information for an image.
        :param registry_id: The Amazon Web Services account ID associated with the registry that
        contains the repository.
        :returns: DescribeImageSigningStatusResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises ValidationException:
        :raises ImageNotFoundException:
        :raises RepositoryNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeImages")
    def describe_images(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        registry_id: RegistryId | None = None,
        image_ids: ImageIdentifierList | None = None,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        filter: DescribeImagesFilter | None = None,
        **kwargs,
    ) -> DescribeImagesResponse:
        """Returns metadata about the images in a repository.

        Starting with Docker version 1.9, the Docker client compresses image
        layers before pushing them to a V2 Docker registry. The output of the
        ``docker images`` command shows the uncompressed image size. Therefore,
        Docker might return a larger image than the image shown in the Amazon
        Web Services Management Console.

        The new version of Amazon ECR *Basic Scanning* doesn't use the
        ImageDetail$imageScanFindingsSummary and ImageDetail$imageScanStatus
        attributes from the API response to return scan results. Use the
        DescribeImageScanFindings API instead. For more information about Amazon
        Web Services native basic scanning, see `Scan images for software
        vulnerabilities in Amazon
        ECR <https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning.html>`__.

        :param repository_name: The repository that contains the images to describe.
        :param registry_id: The Amazon Web Services account ID associated with the registry that
        contains the repository in which to describe images.
        :param image_ids: The list of image IDs for the requested repository.
        :param next_token: The ``nextToken`` value returned from a previous paginated
        ``DescribeImages`` request where ``maxResults`` was used and the results
        exceeded the value of that parameter.
        :param max_results: The maximum number of repository results returned by ``DescribeImages``
        in paginated output.
        :param filter: The filter key and value with which to filter your ``DescribeImages``
        results.
        :returns: DescribeImagesResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises RepositoryNotFoundException:
        :raises ImageNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribePullThroughCacheRules")
    def describe_pull_through_cache_rules(
        self,
        context: RequestContext,
        registry_id: RegistryId | None = None,
        ecr_repository_prefixes: PullThroughCacheRuleRepositoryPrefixList | None = None,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> DescribePullThroughCacheRulesResponse:
        """Returns the pull through cache rules for a registry.

        :param registry_id: The Amazon Web Services account ID associated with the registry to
        return the pull through cache rules for.
        :param ecr_repository_prefixes: The Amazon ECR repository prefixes associated with the pull through
        cache rules to return.
        :param next_token: The ``nextToken`` value returned from a previous paginated
        ``DescribePullThroughCacheRulesRequest`` request where ``maxResults``
        was used and the results exceeded the value of that parameter.
        :param max_results: The maximum number of pull through cache rules returned by
        ``DescribePullThroughCacheRulesRequest`` in paginated output.
        :returns: DescribePullThroughCacheRulesResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises ValidationException:
        :raises PullThroughCacheRuleNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeRegistry")
    def describe_registry(self, context: RequestContext, **kwargs) -> DescribeRegistryResponse:
        """Describes the settings for a registry. The replication configuration for
        a repository can be created or updated with the
        PutReplicationConfiguration API action.

        :returns: DescribeRegistryResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("DescribeRepositories")
    def describe_repositories(
        self,
        context: RequestContext,
        registry_id: RegistryId | None = None,
        repository_names: RepositoryNameList | None = None,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> DescribeRepositoriesResponse:
        """Describes image repositories in a registry.

        :param registry_id: The Amazon Web Services account ID associated with the registry that
        contains the repositories to be described.
        :param repository_names: A list of repositories to describe.
        :param next_token: The ``nextToken`` value returned from a previous paginated
        ``DescribeRepositories`` request where ``maxResults`` was used and the
        results exceeded the value of that parameter.
        :param max_results: The maximum number of repository results returned by
        ``DescribeRepositories`` in paginated output.
        :returns: DescribeRepositoriesResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises RepositoryNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeRepositoryCreationTemplates")
    def describe_repository_creation_templates(
        self,
        context: RequestContext,
        prefixes: PrefixList | None = None,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> DescribeRepositoryCreationTemplatesResponse:
        """Returns details about the repository creation templates in a registry.
        The ``prefixes`` request parameter can be used to return the details for
        a specific repository creation template.

        :param prefixes: The repository namespace prefixes associated with the repository
        creation templates to describe.
        :param next_token: The ``nextToken`` value returned from a previous paginated
        ``DescribeRepositoryCreationTemplates`` request where ``maxResults`` was
        used and the results exceeded the value of that parameter.
        :param max_results: The maximum number of repository results returned by
        ``DescribeRepositoryCreationTemplatesRequest`` in paginated output.
        :returns: DescribeRepositoryCreationTemplatesResponse
        :raises ServerException:
        :raises ValidationException:
        :raises InvalidParameterException:
        """
        raise NotImplementedError

    @handler("GetAccountSetting")
    def get_account_setting(
        self, context: RequestContext, name: AccountSettingName, **kwargs
    ) -> GetAccountSettingResponse:
        """Retrieves the account setting value for the specified setting name.

        :param name: The name of the account setting, such as ``BASIC_SCAN_TYPE_VERSION`` or
        ``REGISTRY_POLICY_SCOPE``.
        :returns: GetAccountSettingResponse
        :raises ServerException:
        :raises ValidationException:
        :raises InvalidParameterException:
        """
        raise NotImplementedError

    @handler("GetAuthorizationToken")
    def get_authorization_token(
        self,
        context: RequestContext,
        registry_ids: GetAuthorizationTokenRegistryIdList | None = None,
        **kwargs,
    ) -> GetAuthorizationTokenResponse:
        """Retrieves an authorization token. An authorization token represents your
        IAM authentication credentials and can be used to access any Amazon ECR
        registry that your IAM principal has access to. The authorization token
        is valid for 12 hours.

        The ``authorizationToken`` returned is a base64 encoded string that can
        be decoded and used in a ``docker login`` command to authenticate to a
        registry. The CLI offers an ``get-login-password`` command that
        simplifies the login process. For more information, see `Registry
        authentication <https://docs.aws.amazon.com/AmazonECR/latest/userguide/Registries.html#registry_auth>`__
        in the *Amazon Elastic Container Registry User Guide*.

        :param registry_ids: A list of Amazon Web Services account IDs that are associated with the
        registries for which to get AuthorizationData objects.
        :returns: GetAuthorizationTokenResponse
        :raises ServerException:
        :raises InvalidParameterException:
        """
        raise NotImplementedError

    @handler("GetDownloadUrlForLayer")
    def get_download_url_for_layer(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        layer_digest: LayerDigest,
        registry_id: RegistryId | None = None,
        **kwargs,
    ) -> GetDownloadUrlForLayerResponse:
        """Retrieves the pre-signed Amazon S3 download URL corresponding to an
        image layer. You can only get URLs for image layers that are referenced
        in an image.

        When an image is pulled, the GetDownloadUrlForLayer API is called once
        per image layer that is not already cached.

        This operation is used by the Amazon ECR proxy and is not generally used
        by customers for pulling and pushing images. In most cases, you should
        use the ``docker`` CLI to pull, tag, and push images.

        :param repository_name: The name of the repository that is associated with the image layer to
        download.
        :param layer_digest: The digest of the image layer to download.
        :param registry_id: The Amazon Web Services account ID associated with the registry that
        contains the image layer to download.
        :returns: GetDownloadUrlForLayerResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises LayersNotFoundException:
        :raises LayerInaccessibleException:
        :raises RepositoryNotFoundException:
        :raises UnableToGetUpstreamLayerException:
        """
        raise NotImplementedError

    @handler("GetLifecyclePolicy")
    def get_lifecycle_policy(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        registry_id: RegistryId | None = None,
        **kwargs,
    ) -> GetLifecyclePolicyResponse:
        """Retrieves the lifecycle policy for the specified repository.

        :param repository_name: The name of the repository.
        :param registry_id: The Amazon Web Services account ID associated with the registry that
        contains the repository.
        :returns: GetLifecyclePolicyResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises RepositoryNotFoundException:
        :raises LifecyclePolicyNotFoundException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("GetLifecyclePolicyPreview")
    def get_lifecycle_policy_preview(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        registry_id: RegistryId | None = None,
        image_ids: ImageIdentifierList | None = None,
        next_token: NextToken | None = None,
        max_results: LifecyclePreviewMaxResults | None = None,
        filter: LifecyclePolicyPreviewFilter | None = None,
        **kwargs,
    ) -> GetLifecyclePolicyPreviewResponse:
        """Retrieves the results of the lifecycle policy preview request for the
        specified repository.

        :param repository_name: The name of the repository.
        :param registry_id: The Amazon Web Services account ID associated with the registry that
        contains the repository.
        :param image_ids: The list of imageIDs to be included.
        :param next_token: The ``nextToken`` value returned from a previous paginated
        ``GetLifecyclePolicyPreviewRequest`` request where ``maxResults`` was
        used and the  results exceeded the value of that parameter.
        :param max_results: The maximum number of repository results returned by
        ``GetLifecyclePolicyPreviewRequest`` in  paginated output.
        :param filter: An optional parameter that filters results based on image tag status and
        all tags, if tagged.
        :returns: GetLifecyclePolicyPreviewResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises RepositoryNotFoundException:
        :raises LifecyclePolicyPreviewNotFoundException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("GetRegistryPolicy")
    def get_registry_policy(self, context: RequestContext, **kwargs) -> GetRegistryPolicyResponse:
        """Retrieves the permissions policy for a registry.

        :returns: GetRegistryPolicyResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises RegistryPolicyNotFoundException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("GetRegistryScanningConfiguration")
    def get_registry_scanning_configuration(
        self, context: RequestContext, **kwargs
    ) -> GetRegistryScanningConfigurationResponse:
        """Retrieves the scanning configuration for a registry.

        :returns: GetRegistryScanningConfigurationResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("GetRepositoryPolicy")
    def get_repository_policy(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        registry_id: RegistryId | None = None,
        **kwargs,
    ) -> GetRepositoryPolicyResponse:
        """Retrieves the repository policy for the specified repository.

        :param repository_name: The name of the repository with the policy to retrieve.
        :param registry_id: The Amazon Web Services account ID associated with the registry that
        contains the repository.
        :returns: GetRepositoryPolicyResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises RepositoryNotFoundException:
        :raises RepositoryPolicyNotFoundException:
        """
        raise NotImplementedError

    @handler("GetSigningConfiguration")
    def get_signing_configuration(
        self, context: RequestContext, **kwargs
    ) -> GetSigningConfigurationResponse:
        """Retrieves the registry's signing configuration, which defines rules for
        automatically signing images using Amazon Web Services Signer.

        For more information, see `Managed
        signing <https://docs.aws.amazon.com/AmazonECR/latest/userguide/managed-signing.html>`__
        in the *Amazon Elastic Container Registry User Guide*.

        :returns: GetSigningConfigurationResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises ValidationException:
        :raises SigningConfigurationNotFoundException:
        """
        raise NotImplementedError

    @handler("InitiateLayerUpload")
    def initiate_layer_upload(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        registry_id: RegistryId | None = None,
        **kwargs,
    ) -> InitiateLayerUploadResponse:
        """Notifies Amazon ECR that you intend to upload an image layer.

        When an image is pushed, the InitiateLayerUpload API is called once per
        image layer that has not already been uploaded. Whether or not an image
        layer has been uploaded is determined by the BatchCheckLayerAvailability
        API action.

        This operation is used by the Amazon ECR proxy and is not generally used
        by customers for pulling and pushing images. In most cases, you should
        use the ``docker`` CLI to pull, tag, and push images.

        :param repository_name: The name of the repository to which you intend to upload layers.
        :param registry_id: The Amazon Web Services account ID associated with the registry to which
        you intend to upload layers.
        :returns: InitiateLayerUploadResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises RepositoryNotFoundException:
        :raises KmsException:
        """
        raise NotImplementedError

    @handler("ListImageReferrers")
    def list_image_referrers(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        subject_id: SubjectIdentifier,
        registry_id: RegistryId | None = None,
        filter: ListImageReferrersFilter | None = None,
        next_token: NextToken | None = None,
        max_results: FiftyMaxResults | None = None,
        **kwargs,
    ) -> ListImageReferrersResponse:
        """Lists the artifacts associated with a specified subject image.

        :param repository_name: The name of the repository that contains the subject image.
        :param subject_id: An object containing the image digest of the subject image for which to
        retrieve associated artifacts.
        :param registry_id: The Amazon Web Services account ID associated with the registry that
        contains the repository in which to list image referrers.
        :param filter: The filter key and value with which to filter your
        ``ListImageReferrers`` results.
        :param next_token: The ``nextToken`` value returned from a previous paginated
        ``ListImageReferrers`` request where ``maxResults`` was used and the
        results exceeded the value of that parameter.
        :param max_results: The maximum number of image referrer results returned by
        ``ListImageReferrers`` in paginated output.
        :returns: ListImageReferrersResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises RepositoryNotFoundException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("ListImages")
    def list_images(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        registry_id: RegistryId | None = None,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        filter: ListImagesFilter | None = None,
        **kwargs,
    ) -> ListImagesResponse:
        """Lists all the image IDs for the specified repository.

        You can filter images based on whether or not they are tagged by using
        the ``tagStatus`` filter and specifying either ``TAGGED``, ``UNTAGGED``
        or ``ANY``. For example, you can filter your results to return only
        ``UNTAGGED`` images and then pipe that result to a BatchDeleteImage
        operation to delete them. Or, you can filter your results to return only
        ``TAGGED`` images to list all of the tags in your repository.

        :param repository_name: The repository with image IDs to be listed.
        :param registry_id: The Amazon Web Services account ID associated with the registry that
        contains the repository in which to list images.
        :param next_token: The ``nextToken`` value returned from a previous paginated
        ``ListImages`` request where ``maxResults`` was used and the results
        exceeded the value of that parameter.
        :param max_results: The maximum number of image results returned by ``ListImages`` in
        paginated output.
        :param filter: The filter key and value with which to filter your ``ListImages``
        results.
        :returns: ListImagesResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises RepositoryNotFoundException:
        """
        raise NotImplementedError

    @handler("ListPullTimeUpdateExclusions")
    def list_pull_time_update_exclusions(
        self,
        context: RequestContext,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListPullTimeUpdateExclusionsResponse:
        """Lists the IAM principals that are excluded from having their image pull
        times recorded.

        :param max_results: The maximum number of pull time update exclusion results returned by
        ``ListPullTimeUpdateExclusions`` in paginated output.
        :param next_token: The ``nextToken`` value returned from a previous paginated
        ``ListPullTimeUpdateExclusions`` request where ``maxResults`` was used
        and the results exceeded the value of that parameter.
        :returns: ListPullTimeUpdateExclusionsResponse
        :raises InvalidParameterException:
        :raises ValidationException:
        :raises LimitExceededException:
        :raises ServerException:
        """
        raise NotImplementedError

    @handler("ListTagsForResource")
    def list_tags_for_resource(
        self, context: RequestContext, resource_arn: Arn, **kwargs
    ) -> ListTagsForResourceResponse:
        """List the tags for an Amazon ECR resource.

        :param resource_arn: The Amazon Resource Name (ARN) that identifies the resource for which to
        list the tags.
        :returns: ListTagsForResourceResponse
        :raises InvalidParameterException:
        :raises RepositoryNotFoundException:
        :raises ServerException:
        """
        raise NotImplementedError

    @handler("PutAccountSetting")
    def put_account_setting(
        self,
        context: RequestContext,
        name: AccountSettingName,
        value: AccountSettingValue,
        **kwargs,
    ) -> PutAccountSettingResponse:
        """Allows you to change the basic scan type version or registry policy
        scope.

        :param name: The name of the account setting, such as ``BASIC_SCAN_TYPE_VERSION`` or
        ``REGISTRY_POLICY_SCOPE``.
        :param value: Setting value that is specified.
        :returns: PutAccountSettingResponse
        :raises ServerException:
        :raises ValidationException:
        :raises InvalidParameterException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("PutImage")
    def put_image(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        image_manifest: ImageManifest,
        registry_id: RegistryId | None = None,
        image_manifest_media_type: MediaType | None = None,
        image_tag: ImageTag | None = None,
        image_digest: ImageDigest | None = None,
        **kwargs,
    ) -> PutImageResponse:
        """Creates or updates the image manifest and tags associated with an image.

        When an image is pushed and all new image layers have been uploaded, the
        PutImage API is called once to create or update the image manifest and
        the tags associated with the image.

        This operation is used by the Amazon ECR proxy and is not generally used
        by customers for pulling and pushing images. In most cases, you should
        use the ``docker`` CLI to pull, tag, and push images.

        :param repository_name: The name of the repository in which to put the image.
        :param image_manifest: The image manifest corresponding to the image to be uploaded.
        :param registry_id: The Amazon Web Services account ID associated with the registry that
        contains the repository in which to put the image.
        :param image_manifest_media_type: The media type of the image manifest.
        :param image_tag: The tag to associate with the image.
        :param image_digest: The image digest of the image manifest corresponding to the image.
        :returns: PutImageResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises RepositoryNotFoundException:
        :raises ImageAlreadyExistsException:
        :raises LayersNotFoundException:
        :raises ReferencedImagesNotFoundException:
        :raises LimitExceededException:
        :raises ImageTagAlreadyExistsException:
        :raises ImageDigestDoesNotMatchException:
        :raises KmsException:
        """
        raise NotImplementedError

    @handler("PutImageScanningConfiguration")
    def put_image_scanning_configuration(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        image_scanning_configuration: ImageScanningConfiguration,
        registry_id: RegistryId | None = None,
        **kwargs,
    ) -> PutImageScanningConfigurationResponse:
        """The ``PutImageScanningConfiguration`` API is being deprecated, in favor
        of specifying the image scanning configuration at the registry level.
        For more information, see PutRegistryScanningConfiguration.

        Updates the image scanning configuration for the specified repository.

        :param repository_name: The name of the repository in which to update the image scanning
        configuration setting.
        :param image_scanning_configuration: The image scanning configuration for the repository.
        :param registry_id: The Amazon Web Services account ID associated with the registry that
        contains the repository in which to update the image scanning
        configuration setting.
        :returns: PutImageScanningConfigurationResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises RepositoryNotFoundException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("PutImageTagMutability")
    def put_image_tag_mutability(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        image_tag_mutability: ImageTagMutability,
        registry_id: RegistryId | None = None,
        image_tag_mutability_exclusion_filters: ImageTagMutabilityExclusionFilters | None = None,
        **kwargs,
    ) -> PutImageTagMutabilityResponse:
        """Updates the image tag mutability settings for the specified repository.
        For more information, see `Image tag
        mutability <https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-tag-mutability.html>`__
        in the *Amazon Elastic Container Registry User Guide*.

        :param repository_name: The name of the repository in which to update the image tag mutability
        settings.
        :param image_tag_mutability: The tag mutability setting for the repository.
        :param registry_id: The Amazon Web Services account ID associated with the registry that
        contains the repository in which to update the image tag mutability
        settings.
        :param image_tag_mutability_exclusion_filters: A list of filters that specify which image tags should be excluded from
        the image tag mutability setting being applied.
        :returns: PutImageTagMutabilityResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises RepositoryNotFoundException:
        """
        raise NotImplementedError

    @handler("PutLifecyclePolicy")
    def put_lifecycle_policy(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        lifecycle_policy_text: LifecyclePolicyText,
        registry_id: RegistryId | None = None,
        **kwargs,
    ) -> PutLifecyclePolicyResponse:
        """Creates or updates the lifecycle policy for the specified repository.
        For more information, see `Lifecycle policy
        template <https://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html>`__.

        :param repository_name: The name of the repository to receive the policy.
        :param lifecycle_policy_text: The JSON repository policy text to apply to the repository.
        :param registry_id: The Amazon Web Services account ID associated with the registry that
        contains the repository.
        :returns: PutLifecyclePolicyResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises RepositoryNotFoundException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("PutRegistryPolicy")
    def put_registry_policy(
        self, context: RequestContext, policy_text: RegistryPolicyText, **kwargs
    ) -> PutRegistryPolicyResponse:
        """Creates or updates the permissions policy for your registry.

        A registry policy is used to specify permissions for another Amazon Web
        Services account and is used when configuring cross-account replication.
        For more information, see `Registry
        permissions <https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry-permissions.html>`__
        in the *Amazon Elastic Container Registry User Guide*.

        :param policy_text: The JSON policy text to apply to your registry.
        :returns: PutRegistryPolicyResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("PutRegistryScanningConfiguration")
    def put_registry_scanning_configuration(
        self,
        context: RequestContext,
        scan_type: ScanType | None = None,
        rules: RegistryScanningRuleList | None = None,
        **kwargs,
    ) -> PutRegistryScanningConfigurationResponse:
        """Creates or updates the scanning configuration for your private registry.

        :param scan_type: The scanning type to set for the registry.
        :param rules: The scanning rules to use for the registry.
        :returns: PutRegistryScanningConfigurationResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises ValidationException:
        :raises BlockedByOrganizationPolicyException:
        """
        raise NotImplementedError

    @handler("PutReplicationConfiguration")
    def put_replication_configuration(
        self, context: RequestContext, replication_configuration: ReplicationConfiguration, **kwargs
    ) -> PutReplicationConfigurationResponse:
        """Creates or updates the replication configuration for a registry. The
        existing replication configuration for a repository can be retrieved
        with the DescribeRegistry API action. The first time the
        PutReplicationConfiguration API is called, a service-linked IAM role is
        created in your account for the replication process. For more
        information, see `Using service-linked roles for Amazon
        ECR <https://docs.aws.amazon.com/AmazonECR/latest/userguide/using-service-linked-roles.html>`__
        in the *Amazon Elastic Container Registry User Guide*. For more
        information on the custom role for replication, see `Creating an IAM
        role for
        replication <https://docs.aws.amazon.com/AmazonECR/latest/userguide/replication-creation-templates.html#roles-creatingrole-user-console>`__.

        When configuring cross-account replication, the destination account must
        grant the source account permission to replicate. This permission is
        controlled using a registry permissions policy. For more information,
        see PutRegistryPolicy.

        :param replication_configuration: An object representing the replication configuration for a registry.
        :returns: PutReplicationConfigurationResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("PutSigningConfiguration")
    def put_signing_configuration(
        self, context: RequestContext, signing_configuration: SigningConfiguration, **kwargs
    ) -> PutSigningConfigurationResponse:
        """Creates or updates the registry's signing configuration, which defines
        rules for automatically signing images with Amazon Web Services Signer.

        For more information, see `Managed
        signing <https://docs.aws.amazon.com/AmazonECR/latest/userguide/managed-signing.html>`__
        in the *Amazon Elastic Container Registry User Guide*.

        To successfully generate a signature, the IAM principal pushing images
        must have permission to sign payloads with the Amazon Web Services
        Signer signing profile referenced in the signing configuration.

        :param signing_configuration: The signing configuration to assign to the registry.
        :returns: PutSigningConfigurationResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("RegisterPullTimeUpdateExclusion")
    def register_pull_time_update_exclusion(
        self, context: RequestContext, principal_arn: PrincipalArn, **kwargs
    ) -> RegisterPullTimeUpdateExclusionResponse:
        """Adds an IAM principal to the pull time update exclusion list for a
        registry. Amazon ECR will not record the pull time if an excluded
        principal pulls an image.

        :param principal_arn: The ARN of the IAM principal to exclude from having image pull times
        recorded.
        :returns: RegisterPullTimeUpdateExclusionResponse
        :raises InvalidParameterException:
        :raises ExclusionAlreadyExistsException:
        :raises LimitExceededException:
        :raises ValidationException:
        :raises ServerException:
        """
        raise NotImplementedError

    @handler("SetRepositoryPolicy")
    def set_repository_policy(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        policy_text: RepositoryPolicyText,
        registry_id: RegistryId | None = None,
        force: ForceFlag | None = None,
        **kwargs,
    ) -> SetRepositoryPolicyResponse:
        """Applies a repository policy to the specified repository to control
        access permissions. For more information, see `Amazon ECR Repository
        policies <https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-policies.html>`__
        in the *Amazon Elastic Container Registry User Guide*.

        :param repository_name: The name of the repository to receive the policy.
        :param policy_text: The JSON repository policy text to apply to the repository.
        :param registry_id: The Amazon Web Services account ID associated with the registry that
        contains the repository.
        :param force: If the policy you are attempting to set on a repository policy would
        prevent you from setting another policy in the future, you must force
        the SetRepositoryPolicy operation.
        :returns: SetRepositoryPolicyResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises RepositoryNotFoundException:
        """
        raise NotImplementedError

    @handler("StartImageScan")
    def start_image_scan(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        image_id: ImageIdentifier,
        registry_id: RegistryId | None = None,
        **kwargs,
    ) -> StartImageScanResponse:
        """Starts a basic image vulnerability scan.

        A basic image scan can only be started once per 24 hours on an
        individual image. This limit includes if an image was scanned on initial
        push. You can start up to 100,000 basic scans per 24 hours. This limit
        includes both scans on initial push and scans initiated by the
        StartImageScan API. For more information, see `Basic
        scanning <https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning-basic.html>`__
        in the *Amazon Elastic Container Registry User Guide*.

        :param repository_name: The name of the repository that contains the images to scan.
        :param image_id: An object with identifying information for an image in an Amazon ECR
        repository.
        :param registry_id: The Amazon Web Services account ID associated with the registry that
        contains the repository in which to start an image scan request.
        :returns: StartImageScanResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises UnsupportedImageTypeException:
        :raises LimitExceededException:
        :raises RepositoryNotFoundException:
        :raises ImageNotFoundException:
        :raises ValidationException:
        :raises ImageArchivedException:
        """
        raise NotImplementedError

    @handler("StartLifecyclePolicyPreview")
    def start_lifecycle_policy_preview(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        registry_id: RegistryId | None = None,
        lifecycle_policy_text: LifecyclePolicyText | None = None,
        **kwargs,
    ) -> StartLifecyclePolicyPreviewResponse:
        """Starts a preview of a lifecycle policy for the specified repository.
        This allows you to see the results before associating the lifecycle
        policy with the repository.

        :param repository_name: The name of the repository to be evaluated.
        :param registry_id: The Amazon Web Services account ID associated with the registry that
        contains the repository.
        :param lifecycle_policy_text: The policy to be evaluated against.
        :returns: StartLifecyclePolicyPreviewResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises RepositoryNotFoundException:
        :raises LifecyclePolicyNotFoundException:
        :raises LifecyclePolicyPreviewInProgressException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("TagResource")
    def tag_resource(
        self, context: RequestContext, resource_arn: Arn, tags: TagList, **kwargs
    ) -> TagResourceResponse:
        """Adds specified tags to a resource with the specified ARN. Existing tags
        on a resource are not changed if they are not specified in the request
        parameters.

        :param resource_arn: The Amazon Resource Name (ARN) of the the resource to which to add tags.
        :param tags: The tags to add to the resource.
        :returns: TagResourceResponse
        :raises InvalidParameterException:
        :raises InvalidTagParameterException:
        :raises TooManyTagsException:
        :raises RepositoryNotFoundException:
        :raises ServerException:
        """
        raise NotImplementedError

    @handler("UntagResource")
    def untag_resource(
        self, context: RequestContext, resource_arn: Arn, tag_keys: TagKeyList, **kwargs
    ) -> UntagResourceResponse:
        """Deletes specified tags from a resource.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource from which to remove
        tags.
        :param tag_keys: The keys of the tags to be removed.
        :returns: UntagResourceResponse
        :raises InvalidParameterException:
        :raises InvalidTagParameterException:
        :raises TooManyTagsException:
        :raises RepositoryNotFoundException:
        :raises ServerException:
        """
        raise NotImplementedError

    @handler("UpdateImageStorageClass")
    def update_image_storage_class(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        image_id: ImageIdentifier,
        target_storage_class: TargetStorageClass,
        registry_id: RegistryId | None = None,
        **kwargs,
    ) -> UpdateImageStorageClassResponse:
        """Transitions an image between storage classes. You can transition images
        from Amazon ECR standard storage class to Amazon ECR archival storage
        class for long-term storage, or restore archived images back to Amazon
        ECR standard.

        :param repository_name: The name of the repository that contains the image to transition.
        :param image_id: An object with identifying information for an image in an Amazon ECR
        repository.
        :param target_storage_class: The target storage class for the image.
        :param registry_id: The Amazon Web Services account ID associated with the registry that
        contains the image to transition.
        :returns: UpdateImageStorageClassResponse
        :raises InvalidParameterException:
        :raises ImageNotFoundException:
        :raises ImageStorageClassUpdateNotSupportedException:
        :raises RepositoryNotFoundException:
        :raises ServerException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("UpdatePullThroughCacheRule")
    def update_pull_through_cache_rule(
        self,
        context: RequestContext,
        ecr_repository_prefix: PullThroughCacheRuleRepositoryPrefix,
        registry_id: RegistryId | None = None,
        credential_arn: CredentialArn | None = None,
        custom_role_arn: CustomRoleArn | None = None,
        **kwargs,
    ) -> UpdatePullThroughCacheRuleResponse:
        """Updates an existing pull through cache rule.

        :param ecr_repository_prefix: The repository name prefix to use when caching images from the source
        registry.
        :param registry_id: The Amazon Web Services account ID associated with the registry
        associated with the pull through cache rule.
        :param credential_arn: The Amazon Resource Name (ARN) of the Amazon Web Services Secrets
        Manager secret that identifies the credentials to authenticate to the
        upstream registry.
        :param custom_role_arn: Amazon Resource Name (ARN) of the IAM role to be assumed by Amazon ECR
        to authenticate to the ECR upstream registry.
        :returns: UpdatePullThroughCacheRuleResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises ValidationException:
        :raises UnableToAccessSecretException:
        :raises PullThroughCacheRuleNotFoundException:
        :raises SecretNotFoundException:
        :raises UnableToDecryptSecretValueException:
        """
        raise NotImplementedError

    @handler("UpdateRepositoryCreationTemplate")
    def update_repository_creation_template(
        self,
        context: RequestContext,
        prefix: Prefix,
        description: RepositoryTemplateDescription | None = None,
        encryption_configuration: EncryptionConfigurationForRepositoryCreationTemplate
        | None = None,
        resource_tags: TagList | None = None,
        image_tag_mutability: ImageTagMutability | None = None,
        image_tag_mutability_exclusion_filters: ImageTagMutabilityExclusionFilters | None = None,
        repository_policy: RepositoryPolicyText | None = None,
        lifecycle_policy: LifecyclePolicyTextForRepositoryCreationTemplate | None = None,
        applied_for: RCTAppliedForList | None = None,
        custom_role_arn: CustomRoleArn | None = None,
        **kwargs,
    ) -> UpdateRepositoryCreationTemplateResponse:
        """Updates an existing repository creation template.

        :param prefix: The repository namespace prefix that matches an existing repository
        creation template in the registry.
        :param description: A description for the repository creation template.
        :param encryption_configuration: The encryption configuration to associate with the repository creation
        template.
        :param resource_tags: The metadata to apply to the repository to help you categorize and
        organize.
        :param image_tag_mutability: Updates the tag mutability setting for the repository.
        :param image_tag_mutability_exclusion_filters: A list of filters that specify which image tags should be excluded from
        the repository creation template's image tag mutability setting.
        :param repository_policy: Updates the repository policy created using the template.
        :param lifecycle_policy: Updates the lifecycle policy associated with the specified repository
        creation template.
        :param applied_for: Updates the list of enumerable strings representing the Amazon ECR
        repository creation scenarios that this template will apply towards.
        :param custom_role_arn: The ARN of the role to be assumed by Amazon ECR.
        :returns: UpdateRepositoryCreationTemplateResponse
        :raises ServerException:
        :raises ValidationException:
        :raises InvalidParameterException:
        :raises TemplateNotFoundException:
        """
        raise NotImplementedError

    @handler("UploadLayerPart")
    def upload_layer_part(
        self,
        context: RequestContext,
        repository_name: RepositoryName,
        upload_id: UploadId,
        part_first_byte: PartSize,
        part_last_byte: PartSize,
        layer_part_blob: LayerPartBlob,
        registry_id: RegistryId | None = None,
        **kwargs,
    ) -> UploadLayerPartResponse:
        """Uploads an image layer part to Amazon ECR.

        When an image is pushed, each new image layer is uploaded in parts. The
        maximum size of each image layer part can be 20971520 bytes (or about
        20MB). The UploadLayerPart API is called once per each new image layer
        part.

        This operation is used by the Amazon ECR proxy and is not generally used
        by customers for pulling and pushing images. In most cases, you should
        use the ``docker`` CLI to pull, tag, and push images.

        :param repository_name: The name of the repository to which you are uploading layer parts.
        :param upload_id: The upload ID from a previous InitiateLayerUpload operation to associate
        with the layer part upload.
        :param part_first_byte: The position of the first byte of the layer part witin the overall image
        layer.
        :param part_last_byte: The position of the last byte of the layer part within the overall image
        layer.
        :param layer_part_blob: The base64-encoded layer part payload.
        :param registry_id: The Amazon Web Services account ID associated with the registry to which
        you are uploading layer parts.
        :returns: UploadLayerPartResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises InvalidLayerPartException:
        :raises RepositoryNotFoundException:
        :raises UploadNotFoundException:
        :raises LimitExceededException:
        :raises KmsException:
        """
        raise NotImplementedError

    @handler("ValidatePullThroughCacheRule")
    def validate_pull_through_cache_rule(
        self,
        context: RequestContext,
        ecr_repository_prefix: PullThroughCacheRuleRepositoryPrefix,
        registry_id: RegistryId | None = None,
        **kwargs,
    ) -> ValidatePullThroughCacheRuleResponse:
        """Validates an existing pull through cache rule for an upstream registry
        that requires authentication. This will retrieve the contents of the
        Amazon Web Services Secrets Manager secret, verify the syntax, and then
        validate that authentication to the upstream registry is successful.

        :param ecr_repository_prefix: The repository name prefix associated with the pull through cache rule.
        :param registry_id: The registry ID associated with the pull through cache rule.
        :returns: ValidatePullThroughCacheRuleResponse
        :raises ServerException:
        :raises InvalidParameterException:
        :raises ValidationException:
        :raises PullThroughCacheRuleNotFoundException:
        """
        raise NotImplementedError
