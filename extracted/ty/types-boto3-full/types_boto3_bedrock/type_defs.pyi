"""
Type annotations for bedrock service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from types_boto3_bedrock.type_defs import AgreementAvailabilityTypeDef

    data: AgreementAvailabilityTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import IO, Any, Union

from botocore.response import StreamingBody

from .literals import (
    AgreementStatusType,
    ApplicationTypeType,
    AttributeTypeType,
    AuthorizationStatusType,
    CommitmentDurationType,
    CustomizationTypeType,
    CustomModelDeploymentStatusType,
    EntitlementAvailabilityType,
    EvaluationJobStatusType,
    EvaluationJobTypeType,
    EvaluationTaskTypeType,
    ExternalSourceTypeType,
    FineTuningJobStatusType,
    FoundationModelLifecycleStatusType,
    GuardrailContentFilterActionType,
    GuardrailContentFiltersTierNameType,
    GuardrailContentFilterTypeType,
    GuardrailContextualGroundingActionType,
    GuardrailContextualGroundingFilterTypeType,
    GuardrailFilterStrengthType,
    GuardrailModalityType,
    GuardrailPiiEntityTypeType,
    GuardrailSensitiveInformationActionType,
    GuardrailStatusType,
    GuardrailTopicActionType,
    GuardrailTopicsTierNameType,
    GuardrailWordActionType,
    InferenceProfileTypeType,
    InferenceTypeType,
    JobStatusDetailsType,
    ModelCopyJobStatusType,
    ModelCustomizationJobStatusType,
    ModelCustomizationType,
    ModelImportJobStatusType,
    ModelInvocationJobStatusType,
    ModelModalityType,
    ModelStatusType,
    OfferTypeType,
    PerformanceConfigLatencyType,
    PromptRouterTypeType,
    ProvisionedModelStatusType,
    RegionAvailabilityType,
    RerankingMetadataSelectionModeType,
    RetrieveAndGenerateTypeType,
    SearchTypeType,
    SortOrderType,
    StatusType,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import list as List
    from collections.abc import Mapping, Sequence
else:
    from typing import Dict, List, Mapping, Sequence
if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AgreementAvailabilityTypeDef",
    "AutomatedEvaluationConfigOutputTypeDef",
    "AutomatedEvaluationConfigTypeDef",
    "AutomatedEvaluationCustomMetricConfigOutputTypeDef",
    "AutomatedEvaluationCustomMetricConfigTypeDef",
    "AutomatedEvaluationCustomMetricSourceOutputTypeDef",
    "AutomatedEvaluationCustomMetricSourceTypeDef",
    "BatchDeleteEvaluationJobErrorTypeDef",
    "BatchDeleteEvaluationJobItemTypeDef",
    "BatchDeleteEvaluationJobRequestTypeDef",
    "BatchDeleteEvaluationJobResponseTypeDef",
    "BedrockEvaluatorModelTypeDef",
    "BlobTypeDef",
    "ByteContentDocOutputTypeDef",
    "ByteContentDocTypeDef",
    "CloudWatchConfigTypeDef",
    "CreateCustomModelDeploymentRequestTypeDef",
    "CreateCustomModelDeploymentResponseTypeDef",
    "CreateCustomModelRequestTypeDef",
    "CreateCustomModelResponseTypeDef",
    "CreateEvaluationJobRequestTypeDef",
    "CreateEvaluationJobResponseTypeDef",
    "CreateFoundationModelAgreementRequestTypeDef",
    "CreateFoundationModelAgreementResponseTypeDef",
    "CreateGuardrailRequestTypeDef",
    "CreateGuardrailResponseTypeDef",
    "CreateGuardrailVersionRequestTypeDef",
    "CreateGuardrailVersionResponseTypeDef",
    "CreateInferenceProfileRequestTypeDef",
    "CreateInferenceProfileResponseTypeDef",
    "CreateMarketplaceModelEndpointRequestTypeDef",
    "CreateMarketplaceModelEndpointResponseTypeDef",
    "CreateModelCopyJobRequestTypeDef",
    "CreateModelCopyJobResponseTypeDef",
    "CreateModelCustomizationJobRequestTypeDef",
    "CreateModelCustomizationJobResponseTypeDef",
    "CreateModelImportJobRequestTypeDef",
    "CreateModelImportJobResponseTypeDef",
    "CreateModelInvocationJobRequestTypeDef",
    "CreateModelInvocationJobResponseTypeDef",
    "CreatePromptRouterRequestTypeDef",
    "CreatePromptRouterResponseTypeDef",
    "CreateProvisionedModelThroughputRequestTypeDef",
    "CreateProvisionedModelThroughputResponseTypeDef",
    "CustomMetricBedrockEvaluatorModelTypeDef",
    "CustomMetricDefinitionOutputTypeDef",
    "CustomMetricDefinitionTypeDef",
    "CustomMetricEvaluatorModelConfigOutputTypeDef",
    "CustomMetricEvaluatorModelConfigTypeDef",
    "CustomModelDeploymentSummaryTypeDef",
    "CustomModelSummaryTypeDef",
    "CustomModelUnitsTypeDef",
    "CustomizationConfigTypeDef",
    "DataProcessingDetailsTypeDef",
    "DeleteCustomModelDeploymentRequestTypeDef",
    "DeleteCustomModelRequestTypeDef",
    "DeleteFoundationModelAgreementRequestTypeDef",
    "DeleteGuardrailRequestTypeDef",
    "DeleteImportedModelRequestTypeDef",
    "DeleteInferenceProfileRequestTypeDef",
    "DeleteMarketplaceModelEndpointRequestTypeDef",
    "DeletePromptRouterRequestTypeDef",
    "DeleteProvisionedModelThroughputRequestTypeDef",
    "DeregisterMarketplaceModelEndpointRequestTypeDef",
    "DimensionalPriceRateTypeDef",
    "DistillationConfigTypeDef",
    "EndpointConfigOutputTypeDef",
    "EndpointConfigTypeDef",
    "EndpointConfigUnionTypeDef",
    "EvaluationBedrockModelTypeDef",
    "EvaluationConfigOutputTypeDef",
    "EvaluationConfigTypeDef",
    "EvaluationConfigUnionTypeDef",
    "EvaluationDatasetLocationTypeDef",
    "EvaluationDatasetMetricConfigOutputTypeDef",
    "EvaluationDatasetMetricConfigTypeDef",
    "EvaluationDatasetTypeDef",
    "EvaluationInferenceConfigOutputTypeDef",
    "EvaluationInferenceConfigSummaryTypeDef",
    "EvaluationInferenceConfigTypeDef",
    "EvaluationInferenceConfigUnionTypeDef",
    "EvaluationModelConfigSummaryTypeDef",
    "EvaluationModelConfigTypeDef",
    "EvaluationOutputDataConfigTypeDef",
    "EvaluationPrecomputedInferenceSourceTypeDef",
    "EvaluationPrecomputedRagSourceConfigTypeDef",
    "EvaluationPrecomputedRetrieveAndGenerateSourceConfigTypeDef",
    "EvaluationPrecomputedRetrieveSourceConfigTypeDef",
    "EvaluationRagConfigSummaryTypeDef",
    "EvaluationSummaryTypeDef",
    "EvaluatorModelConfigOutputTypeDef",
    "EvaluatorModelConfigTypeDef",
    "ExternalSourceOutputTypeDef",
    "ExternalSourceTypeDef",
    "ExternalSourcesGenerationConfigurationOutputTypeDef",
    "ExternalSourcesGenerationConfigurationTypeDef",
    "ExternalSourcesRetrieveAndGenerateConfigurationOutputTypeDef",
    "ExternalSourcesRetrieveAndGenerateConfigurationTypeDef",
    "FieldForRerankingTypeDef",
    "FilterAttributeOutputTypeDef",
    "FilterAttributeTypeDef",
    "FoundationModelDetailsTypeDef",
    "FoundationModelLifecycleTypeDef",
    "FoundationModelSummaryTypeDef",
    "GenerationConfigurationOutputTypeDef",
    "GenerationConfigurationTypeDef",
    "GetCustomModelDeploymentRequestTypeDef",
    "GetCustomModelDeploymentResponseTypeDef",
    "GetCustomModelRequestTypeDef",
    "GetCustomModelResponseTypeDef",
    "GetEvaluationJobRequestTypeDef",
    "GetEvaluationJobResponseTypeDef",
    "GetFoundationModelAvailabilityRequestTypeDef",
    "GetFoundationModelAvailabilityResponseTypeDef",
    "GetFoundationModelRequestTypeDef",
    "GetFoundationModelResponseTypeDef",
    "GetGuardrailRequestTypeDef",
    "GetGuardrailResponseTypeDef",
    "GetImportedModelRequestTypeDef",
    "GetImportedModelResponseTypeDef",
    "GetInferenceProfileRequestTypeDef",
    "GetInferenceProfileResponseTypeDef",
    "GetMarketplaceModelEndpointRequestTypeDef",
    "GetMarketplaceModelEndpointResponseTypeDef",
    "GetModelCopyJobRequestTypeDef",
    "GetModelCopyJobResponseTypeDef",
    "GetModelCustomizationJobRequestTypeDef",
    "GetModelCustomizationJobResponseTypeDef",
    "GetModelImportJobRequestTypeDef",
    "GetModelImportJobResponseTypeDef",
    "GetModelInvocationJobRequestTypeDef",
    "GetModelInvocationJobResponseTypeDef",
    "GetModelInvocationLoggingConfigurationResponseTypeDef",
    "GetPromptRouterRequestTypeDef",
    "GetPromptRouterResponseTypeDef",
    "GetProvisionedModelThroughputRequestTypeDef",
    "GetProvisionedModelThroughputResponseTypeDef",
    "GetUseCaseForModelAccessResponseTypeDef",
    "GuardrailConfigurationTypeDef",
    "GuardrailContentFilterConfigTypeDef",
    "GuardrailContentFilterTypeDef",
    "GuardrailContentFiltersTierConfigTypeDef",
    "GuardrailContentFiltersTierTypeDef",
    "GuardrailContentPolicyConfigTypeDef",
    "GuardrailContentPolicyTypeDef",
    "GuardrailContextualGroundingFilterConfigTypeDef",
    "GuardrailContextualGroundingFilterTypeDef",
    "GuardrailContextualGroundingPolicyConfigTypeDef",
    "GuardrailContextualGroundingPolicyTypeDef",
    "GuardrailCrossRegionConfigTypeDef",
    "GuardrailCrossRegionDetailsTypeDef",
    "GuardrailManagedWordsConfigTypeDef",
    "GuardrailManagedWordsTypeDef",
    "GuardrailPiiEntityConfigTypeDef",
    "GuardrailPiiEntityTypeDef",
    "GuardrailRegexConfigTypeDef",
    "GuardrailRegexTypeDef",
    "GuardrailSensitiveInformationPolicyConfigTypeDef",
    "GuardrailSensitiveInformationPolicyTypeDef",
    "GuardrailSummaryTypeDef",
    "GuardrailTopicConfigTypeDef",
    "GuardrailTopicPolicyConfigTypeDef",
    "GuardrailTopicPolicyTypeDef",
    "GuardrailTopicTypeDef",
    "GuardrailTopicsTierConfigTypeDef",
    "GuardrailTopicsTierTypeDef",
    "GuardrailWordConfigTypeDef",
    "GuardrailWordPolicyConfigTypeDef",
    "GuardrailWordPolicyTypeDef",
    "GuardrailWordTypeDef",
    "HumanEvaluationConfigOutputTypeDef",
    "HumanEvaluationConfigTypeDef",
    "HumanEvaluationCustomMetricTypeDef",
    "HumanWorkflowConfigTypeDef",
    "ImplicitFilterConfigurationOutputTypeDef",
    "ImplicitFilterConfigurationTypeDef",
    "ImportedModelSummaryTypeDef",
    "InferenceProfileModelSourceTypeDef",
    "InferenceProfileModelTypeDef",
    "InferenceProfileSummaryTypeDef",
    "InvocationLogSourceTypeDef",
    "InvocationLogsConfigOutputTypeDef",
    "InvocationLogsConfigTypeDef",
    "KbInferenceConfigOutputTypeDef",
    "KbInferenceConfigTypeDef",
    "KnowledgeBaseConfigOutputTypeDef",
    "KnowledgeBaseConfigTypeDef",
    "KnowledgeBaseRetrievalConfigurationOutputTypeDef",
    "KnowledgeBaseRetrievalConfigurationTypeDef",
    "KnowledgeBaseRetrieveAndGenerateConfigurationOutputTypeDef",
    "KnowledgeBaseRetrieveAndGenerateConfigurationTypeDef",
    "KnowledgeBaseVectorSearchConfigurationOutputTypeDef",
    "KnowledgeBaseVectorSearchConfigurationTypeDef",
    "LegalTermTypeDef",
    "ListCustomModelDeploymentsRequestPaginateTypeDef",
    "ListCustomModelDeploymentsRequestTypeDef",
    "ListCustomModelDeploymentsResponseTypeDef",
    "ListCustomModelsRequestPaginateTypeDef",
    "ListCustomModelsRequestTypeDef",
    "ListCustomModelsResponseTypeDef",
    "ListEvaluationJobsRequestPaginateTypeDef",
    "ListEvaluationJobsRequestTypeDef",
    "ListEvaluationJobsResponseTypeDef",
    "ListFoundationModelAgreementOffersRequestTypeDef",
    "ListFoundationModelAgreementOffersResponseTypeDef",
    "ListFoundationModelsRequestTypeDef",
    "ListFoundationModelsResponseTypeDef",
    "ListGuardrailsRequestPaginateTypeDef",
    "ListGuardrailsRequestTypeDef",
    "ListGuardrailsResponseTypeDef",
    "ListImportedModelsRequestPaginateTypeDef",
    "ListImportedModelsRequestTypeDef",
    "ListImportedModelsResponseTypeDef",
    "ListInferenceProfilesRequestPaginateTypeDef",
    "ListInferenceProfilesRequestTypeDef",
    "ListInferenceProfilesResponseTypeDef",
    "ListMarketplaceModelEndpointsRequestPaginateTypeDef",
    "ListMarketplaceModelEndpointsRequestTypeDef",
    "ListMarketplaceModelEndpointsResponseTypeDef",
    "ListModelCopyJobsRequestPaginateTypeDef",
    "ListModelCopyJobsRequestTypeDef",
    "ListModelCopyJobsResponseTypeDef",
    "ListModelCustomizationJobsRequestPaginateTypeDef",
    "ListModelCustomizationJobsRequestTypeDef",
    "ListModelCustomizationJobsResponseTypeDef",
    "ListModelImportJobsRequestPaginateTypeDef",
    "ListModelImportJobsRequestTypeDef",
    "ListModelImportJobsResponseTypeDef",
    "ListModelInvocationJobsRequestPaginateTypeDef",
    "ListModelInvocationJobsRequestTypeDef",
    "ListModelInvocationJobsResponseTypeDef",
    "ListPromptRoutersRequestPaginateTypeDef",
    "ListPromptRoutersRequestTypeDef",
    "ListPromptRoutersResponseTypeDef",
    "ListProvisionedModelThroughputsRequestPaginateTypeDef",
    "ListProvisionedModelThroughputsRequestTypeDef",
    "ListProvisionedModelThroughputsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "LoggingConfigTypeDef",
    "MarketplaceModelEndpointSummaryTypeDef",
    "MarketplaceModelEndpointTypeDef",
    "MetadataAttributeSchemaTypeDef",
    "MetadataConfigurationForRerankingOutputTypeDef",
    "MetadataConfigurationForRerankingTypeDef",
    "ModelCopyJobSummaryTypeDef",
    "ModelCustomizationJobSummaryTypeDef",
    "ModelDataSourceTypeDef",
    "ModelImportJobSummaryTypeDef",
    "ModelInvocationJobInputDataConfigTypeDef",
    "ModelInvocationJobOutputDataConfigTypeDef",
    "ModelInvocationJobS3InputDataConfigTypeDef",
    "ModelInvocationJobS3OutputDataConfigTypeDef",
    "ModelInvocationJobSummaryTypeDef",
    "OfferTypeDef",
    "OrchestrationConfigurationTypeDef",
    "OutputDataConfigTypeDef",
    "PaginatorConfigTypeDef",
    "PerformanceConfigurationTypeDef",
    "PricingTermTypeDef",
    "PromptRouterSummaryTypeDef",
    "PromptRouterTargetModelTypeDef",
    "PromptTemplateTypeDef",
    "ProvisionedModelSummaryTypeDef",
    "PutModelInvocationLoggingConfigurationRequestTypeDef",
    "PutUseCaseForModelAccessRequestTypeDef",
    "QueryTransformationConfigurationTypeDef",
    "RAGConfigOutputTypeDef",
    "RAGConfigTypeDef",
    "RatingScaleItemTypeDef",
    "RatingScaleItemValueTypeDef",
    "RegisterMarketplaceModelEndpointRequestTypeDef",
    "RegisterMarketplaceModelEndpointResponseTypeDef",
    "RequestMetadataBaseFiltersOutputTypeDef",
    "RequestMetadataBaseFiltersTypeDef",
    "RequestMetadataFiltersOutputTypeDef",
    "RequestMetadataFiltersTypeDef",
    "RerankingMetadataSelectiveModeConfigurationOutputTypeDef",
    "RerankingMetadataSelectiveModeConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "RetrievalFilterOutputTypeDef",
    "RetrievalFilterTypeDef",
    "RetrieveAndGenerateConfigurationOutputTypeDef",
    "RetrieveAndGenerateConfigurationTypeDef",
    "RetrieveConfigOutputTypeDef",
    "RetrieveConfigTypeDef",
    "RoutingCriteriaTypeDef",
    "S3ConfigTypeDef",
    "S3DataSourceTypeDef",
    "S3ObjectDocTypeDef",
    "SageMakerEndpointOutputTypeDef",
    "SageMakerEndpointTypeDef",
    "StatusDetailsTypeDef",
    "StopEvaluationJobRequestTypeDef",
    "StopModelCustomizationJobRequestTypeDef",
    "StopModelInvocationJobRequestTypeDef",
    "SupportTermTypeDef",
    "TagResourceRequestTypeDef",
    "TagTypeDef",
    "TeacherModelConfigTypeDef",
    "TermDetailsTypeDef",
    "TextInferenceConfigOutputTypeDef",
    "TextInferenceConfigTypeDef",
    "TimestampTypeDef",
    "TrainingDataConfigOutputTypeDef",
    "TrainingDataConfigTypeDef",
    "TrainingDataConfigUnionTypeDef",
    "TrainingDetailsTypeDef",
    "TrainingMetricsTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateGuardrailRequestTypeDef",
    "UpdateGuardrailResponseTypeDef",
    "UpdateMarketplaceModelEndpointRequestTypeDef",
    "UpdateMarketplaceModelEndpointResponseTypeDef",
    "UpdateProvisionedModelThroughputRequestTypeDef",
    "ValidationDataConfigOutputTypeDef",
    "ValidationDataConfigTypeDef",
    "ValidationDataConfigUnionTypeDef",
    "ValidationDetailsTypeDef",
    "ValidatorMetricTypeDef",
    "ValidatorTypeDef",
    "ValidityTermTypeDef",
    "VectorSearchBedrockRerankingConfigurationOutputTypeDef",
    "VectorSearchBedrockRerankingConfigurationTypeDef",
    "VectorSearchBedrockRerankingModelConfigurationOutputTypeDef",
    "VectorSearchBedrockRerankingModelConfigurationTypeDef",
    "VectorSearchRerankingConfigurationOutputTypeDef",
    "VectorSearchRerankingConfigurationTypeDef",
    "VpcConfigOutputTypeDef",
    "VpcConfigTypeDef",
    "VpcConfigUnionTypeDef",
)

class AgreementAvailabilityTypeDef(TypedDict):
    status: AgreementStatusType
    errorMessage: NotRequired[str]

class BatchDeleteEvaluationJobErrorTypeDef(TypedDict):
    jobIdentifier: str
    code: str
    message: NotRequired[str]

class BatchDeleteEvaluationJobItemTypeDef(TypedDict):
    jobIdentifier: str
    jobStatus: EvaluationJobStatusType

class BatchDeleteEvaluationJobRequestTypeDef(TypedDict):
    jobIdentifiers: Sequence[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class BedrockEvaluatorModelTypeDef(TypedDict):
    modelIdentifier: str

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class ByteContentDocOutputTypeDef(TypedDict):
    identifier: str
    contentType: str
    data: bytes

class S3ConfigTypeDef(TypedDict):
    bucketName: str
    keyPrefix: NotRequired[str]

class TagTypeDef(TypedDict):
    key: str
    value: str

class EvaluationOutputDataConfigTypeDef(TypedDict):
    s3Uri: str

class CreateFoundationModelAgreementRequestTypeDef(TypedDict):
    offerToken: str
    modelId: str

class GuardrailCrossRegionConfigTypeDef(TypedDict):
    guardrailProfileIdentifier: str

class CreateGuardrailVersionRequestTypeDef(TypedDict):
    guardrailIdentifier: str
    description: NotRequired[str]
    clientRequestToken: NotRequired[str]

class InferenceProfileModelSourceTypeDef(TypedDict):
    copyFrom: NotRequired[str]

class OutputDataConfigTypeDef(TypedDict):
    s3Uri: str

class PromptRouterTargetModelTypeDef(TypedDict):
    modelArn: str

class RoutingCriteriaTypeDef(TypedDict):
    responseQualityDifference: float

class CustomMetricBedrockEvaluatorModelTypeDef(TypedDict):
    modelIdentifier: str

class CustomModelDeploymentSummaryTypeDef(TypedDict):
    customModelDeploymentArn: str
    customModelDeploymentName: str
    modelArn: str
    createdAt: datetime
    status: CustomModelDeploymentStatusType
    lastUpdatedAt: NotRequired[datetime]
    failureMessage: NotRequired[str]

class CustomModelSummaryTypeDef(TypedDict):
    modelArn: str
    modelName: str
    creationTime: datetime
    baseModelArn: str
    baseModelName: str
    customizationType: NotRequired[CustomizationTypeType]
    ownerAccountId: NotRequired[str]
    modelStatus: NotRequired[ModelStatusType]

class CustomModelUnitsTypeDef(TypedDict):
    customModelUnitsPerModelCopy: NotRequired[int]
    customModelUnitsVersion: NotRequired[str]

class DataProcessingDetailsTypeDef(TypedDict):
    status: NotRequired[JobStatusDetailsType]
    creationTime: NotRequired[datetime]
    lastModifiedTime: NotRequired[datetime]

class DeleteCustomModelDeploymentRequestTypeDef(TypedDict):
    customModelDeploymentIdentifier: str

class DeleteCustomModelRequestTypeDef(TypedDict):
    modelIdentifier: str

class DeleteFoundationModelAgreementRequestTypeDef(TypedDict):
    modelId: str

class DeleteGuardrailRequestTypeDef(TypedDict):
    guardrailIdentifier: str
    guardrailVersion: NotRequired[str]

class DeleteImportedModelRequestTypeDef(TypedDict):
    modelIdentifier: str

class DeleteInferenceProfileRequestTypeDef(TypedDict):
    inferenceProfileIdentifier: str

class DeleteMarketplaceModelEndpointRequestTypeDef(TypedDict):
    endpointArn: str

class DeletePromptRouterRequestTypeDef(TypedDict):
    promptRouterArn: str

class DeleteProvisionedModelThroughputRequestTypeDef(TypedDict):
    provisionedModelId: str

class DeregisterMarketplaceModelEndpointRequestTypeDef(TypedDict):
    endpointArn: str

class DimensionalPriceRateTypeDef(TypedDict):
    dimension: NotRequired[str]
    price: NotRequired[str]
    description: NotRequired[str]
    unit: NotRequired[str]

class TeacherModelConfigTypeDef(TypedDict):
    teacherModelIdentifier: str
    maxResponseLengthForInference: NotRequired[int]

class PerformanceConfigurationTypeDef(TypedDict):
    latency: NotRequired[PerformanceConfigLatencyType]

class EvaluationDatasetLocationTypeDef(TypedDict):
    s3Uri: NotRequired[str]

class EvaluationModelConfigSummaryTypeDef(TypedDict):
    bedrockModelIdentifiers: NotRequired[List[str]]
    precomputedInferenceSourceIdentifiers: NotRequired[List[str]]

class EvaluationRagConfigSummaryTypeDef(TypedDict):
    bedrockKnowledgeBaseIdentifiers: NotRequired[List[str]]
    precomputedRagSourceIdentifiers: NotRequired[List[str]]

class EvaluationPrecomputedInferenceSourceTypeDef(TypedDict):
    inferenceSourceIdentifier: str

class EvaluationPrecomputedRetrieveAndGenerateSourceConfigTypeDef(TypedDict):
    ragSourceIdentifier: str

class EvaluationPrecomputedRetrieveSourceConfigTypeDef(TypedDict):
    ragSourceIdentifier: str

class S3ObjectDocTypeDef(TypedDict):
    uri: str

class GuardrailConfigurationTypeDef(TypedDict):
    guardrailId: str
    guardrailVersion: str

class PromptTemplateTypeDef(TypedDict):
    textPromptTemplate: NotRequired[str]

class FieldForRerankingTypeDef(TypedDict):
    fieldName: str

class FilterAttributeOutputTypeDef(TypedDict):
    key: str
    value: Dict[str, Any]

class FilterAttributeTypeDef(TypedDict):
    key: str
    value: Mapping[str, Any]

class FoundationModelLifecycleTypeDef(TypedDict):
    status: FoundationModelLifecycleStatusType

class GetCustomModelDeploymentRequestTypeDef(TypedDict):
    customModelDeploymentIdentifier: str

class GetCustomModelRequestTypeDef(TypedDict):
    modelIdentifier: str

class TrainingMetricsTypeDef(TypedDict):
    trainingLoss: NotRequired[float]

class ValidatorMetricTypeDef(TypedDict):
    validationLoss: NotRequired[float]

class GetEvaluationJobRequestTypeDef(TypedDict):
    jobIdentifier: str

class GetFoundationModelAvailabilityRequestTypeDef(TypedDict):
    modelId: str

class GetFoundationModelRequestTypeDef(TypedDict):
    modelIdentifier: str

class GetGuardrailRequestTypeDef(TypedDict):
    guardrailIdentifier: str
    guardrailVersion: NotRequired[str]

class GuardrailCrossRegionDetailsTypeDef(TypedDict):
    guardrailProfileId: NotRequired[str]
    guardrailProfileArn: NotRequired[str]

class GetImportedModelRequestTypeDef(TypedDict):
    modelIdentifier: str

class GetInferenceProfileRequestTypeDef(TypedDict):
    inferenceProfileIdentifier: str

class InferenceProfileModelTypeDef(TypedDict):
    modelArn: NotRequired[str]

class GetMarketplaceModelEndpointRequestTypeDef(TypedDict):
    endpointArn: str

class GetModelCopyJobRequestTypeDef(TypedDict):
    jobArn: str

class GetModelCustomizationJobRequestTypeDef(TypedDict):
    jobIdentifier: str

class VpcConfigOutputTypeDef(TypedDict):
    subnetIds: List[str]
    securityGroupIds: List[str]

class GetModelImportJobRequestTypeDef(TypedDict):
    jobIdentifier: str

class GetModelInvocationJobRequestTypeDef(TypedDict):
    jobIdentifier: str

class GetPromptRouterRequestTypeDef(TypedDict):
    promptRouterArn: str

class GetProvisionedModelThroughputRequestTypeDef(TypedDict):
    provisionedModelId: str

GuardrailContentFilterConfigTypeDef = TypedDict(
    "GuardrailContentFilterConfigTypeDef",
    {
        "type": GuardrailContentFilterTypeType,
        "inputStrength": GuardrailFilterStrengthType,
        "outputStrength": GuardrailFilterStrengthType,
        "inputModalities": NotRequired[Sequence[GuardrailModalityType]],
        "outputModalities": NotRequired[Sequence[GuardrailModalityType]],
        "inputAction": NotRequired[GuardrailContentFilterActionType],
        "outputAction": NotRequired[GuardrailContentFilterActionType],
        "inputEnabled": NotRequired[bool],
        "outputEnabled": NotRequired[bool],
    },
)
GuardrailContentFilterTypeDef = TypedDict(
    "GuardrailContentFilterTypeDef",
    {
        "type": GuardrailContentFilterTypeType,
        "inputStrength": GuardrailFilterStrengthType,
        "outputStrength": GuardrailFilterStrengthType,
        "inputModalities": NotRequired[List[GuardrailModalityType]],
        "outputModalities": NotRequired[List[GuardrailModalityType]],
        "inputAction": NotRequired[GuardrailContentFilterActionType],
        "outputAction": NotRequired[GuardrailContentFilterActionType],
        "inputEnabled": NotRequired[bool],
        "outputEnabled": NotRequired[bool],
    },
)

class GuardrailContentFiltersTierConfigTypeDef(TypedDict):
    tierName: GuardrailContentFiltersTierNameType

class GuardrailContentFiltersTierTypeDef(TypedDict):
    tierName: GuardrailContentFiltersTierNameType

GuardrailContextualGroundingFilterConfigTypeDef = TypedDict(
    "GuardrailContextualGroundingFilterConfigTypeDef",
    {
        "type": GuardrailContextualGroundingFilterTypeType,
        "threshold": float,
        "action": NotRequired[GuardrailContextualGroundingActionType],
        "enabled": NotRequired[bool],
    },
)
GuardrailContextualGroundingFilterTypeDef = TypedDict(
    "GuardrailContextualGroundingFilterTypeDef",
    {
        "type": GuardrailContextualGroundingFilterTypeType,
        "threshold": float,
        "action": NotRequired[GuardrailContextualGroundingActionType],
        "enabled": NotRequired[bool],
    },
)
GuardrailManagedWordsConfigTypeDef = TypedDict(
    "GuardrailManagedWordsConfigTypeDef",
    {
        "type": Literal["PROFANITY"],
        "inputAction": NotRequired[GuardrailWordActionType],
        "outputAction": NotRequired[GuardrailWordActionType],
        "inputEnabled": NotRequired[bool],
        "outputEnabled": NotRequired[bool],
    },
)
GuardrailManagedWordsTypeDef = TypedDict(
    "GuardrailManagedWordsTypeDef",
    {
        "type": Literal["PROFANITY"],
        "inputAction": NotRequired[GuardrailWordActionType],
        "outputAction": NotRequired[GuardrailWordActionType],
        "inputEnabled": NotRequired[bool],
        "outputEnabled": NotRequired[bool],
    },
)
GuardrailPiiEntityConfigTypeDef = TypedDict(
    "GuardrailPiiEntityConfigTypeDef",
    {
        "type": GuardrailPiiEntityTypeType,
        "action": GuardrailSensitiveInformationActionType,
        "inputAction": NotRequired[GuardrailSensitiveInformationActionType],
        "outputAction": NotRequired[GuardrailSensitiveInformationActionType],
        "inputEnabled": NotRequired[bool],
        "outputEnabled": NotRequired[bool],
    },
)
GuardrailPiiEntityTypeDef = TypedDict(
    "GuardrailPiiEntityTypeDef",
    {
        "type": GuardrailPiiEntityTypeType,
        "action": GuardrailSensitiveInformationActionType,
        "inputAction": NotRequired[GuardrailSensitiveInformationActionType],
        "outputAction": NotRequired[GuardrailSensitiveInformationActionType],
        "inputEnabled": NotRequired[bool],
        "outputEnabled": NotRequired[bool],
    },
)

class GuardrailRegexConfigTypeDef(TypedDict):
    name: str
    pattern: str
    action: GuardrailSensitiveInformationActionType
    description: NotRequired[str]
    inputAction: NotRequired[GuardrailSensitiveInformationActionType]
    outputAction: NotRequired[GuardrailSensitiveInformationActionType]
    inputEnabled: NotRequired[bool]
    outputEnabled: NotRequired[bool]

class GuardrailRegexTypeDef(TypedDict):
    name: str
    pattern: str
    action: GuardrailSensitiveInformationActionType
    description: NotRequired[str]
    inputAction: NotRequired[GuardrailSensitiveInformationActionType]
    outputAction: NotRequired[GuardrailSensitiveInformationActionType]
    inputEnabled: NotRequired[bool]
    outputEnabled: NotRequired[bool]

GuardrailTopicConfigTypeDef = TypedDict(
    "GuardrailTopicConfigTypeDef",
    {
        "name": str,
        "definition": str,
        "type": Literal["DENY"],
        "examples": NotRequired[Sequence[str]],
        "inputAction": NotRequired[GuardrailTopicActionType],
        "outputAction": NotRequired[GuardrailTopicActionType],
        "inputEnabled": NotRequired[bool],
        "outputEnabled": NotRequired[bool],
    },
)

class GuardrailTopicsTierConfigTypeDef(TypedDict):
    tierName: GuardrailTopicsTierNameType

GuardrailTopicTypeDef = TypedDict(
    "GuardrailTopicTypeDef",
    {
        "name": str,
        "definition": str,
        "examples": NotRequired[List[str]],
        "type": NotRequired[Literal["DENY"]],
        "inputAction": NotRequired[GuardrailTopicActionType],
        "outputAction": NotRequired[GuardrailTopicActionType],
        "inputEnabled": NotRequired[bool],
        "outputEnabled": NotRequired[bool],
    },
)

class GuardrailTopicsTierTypeDef(TypedDict):
    tierName: GuardrailTopicsTierNameType

class GuardrailWordConfigTypeDef(TypedDict):
    text: str
    inputAction: NotRequired[GuardrailWordActionType]
    outputAction: NotRequired[GuardrailWordActionType]
    inputEnabled: NotRequired[bool]
    outputEnabled: NotRequired[bool]

class GuardrailWordTypeDef(TypedDict):
    text: str
    inputAction: NotRequired[GuardrailWordActionType]
    outputAction: NotRequired[GuardrailWordActionType]
    inputEnabled: NotRequired[bool]
    outputEnabled: NotRequired[bool]

class HumanEvaluationCustomMetricTypeDef(TypedDict):
    name: str
    ratingMethod: str
    description: NotRequired[str]

class HumanWorkflowConfigTypeDef(TypedDict):
    flowDefinitionArn: str
    instructions: NotRequired[str]

MetadataAttributeSchemaTypeDef = TypedDict(
    "MetadataAttributeSchemaTypeDef",
    {
        "key": str,
        "type": AttributeTypeType,
        "description": str,
    },
)

class ImportedModelSummaryTypeDef(TypedDict):
    modelArn: str
    modelName: str
    creationTime: datetime
    instructSupported: NotRequired[bool]
    modelArchitecture: NotRequired[str]

class InvocationLogSourceTypeDef(TypedDict):
    s3Uri: NotRequired[str]

class TextInferenceConfigOutputTypeDef(TypedDict):
    temperature: NotRequired[float]
    topP: NotRequired[float]
    maxTokens: NotRequired[int]
    stopSequences: NotRequired[List[str]]

class TextInferenceConfigTypeDef(TypedDict):
    temperature: NotRequired[float]
    topP: NotRequired[float]
    maxTokens: NotRequired[int]
    stopSequences: NotRequired[Sequence[str]]

class LegalTermTypeDef(TypedDict):
    url: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

TimestampTypeDef = Union[datetime, str]

class ListFoundationModelAgreementOffersRequestTypeDef(TypedDict):
    modelId: str
    offerType: NotRequired[OfferTypeType]

class ListFoundationModelsRequestTypeDef(TypedDict):
    byProvider: NotRequired[str]
    byCustomizationType: NotRequired[ModelCustomizationType]
    byOutputModality: NotRequired[ModelModalityType]
    byInferenceType: NotRequired[InferenceTypeType]

class ListGuardrailsRequestTypeDef(TypedDict):
    guardrailIdentifier: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListInferenceProfilesRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    typeEquals: NotRequired[InferenceProfileTypeType]

class ListMarketplaceModelEndpointsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    modelSourceEquals: NotRequired[str]

class MarketplaceModelEndpointSummaryTypeDef(TypedDict):
    endpointArn: str
    modelSourceIdentifier: str
    createdAt: datetime
    updatedAt: datetime
    status: NotRequired[StatusType]
    statusMessage: NotRequired[str]

class ModelImportJobSummaryTypeDef(TypedDict):
    jobArn: str
    jobName: str
    status: ModelImportJobStatusType
    creationTime: datetime
    lastModifiedTime: NotRequired[datetime]
    endTime: NotRequired[datetime]
    importedModelArn: NotRequired[str]
    importedModelName: NotRequired[str]

ListPromptRoutersRequestTypeDef = TypedDict(
    "ListPromptRoutersRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "type": NotRequired[PromptRouterTypeType],
    },
)

class ProvisionedModelSummaryTypeDef(TypedDict):
    provisionedModelName: str
    provisionedModelArn: str
    modelArn: str
    desiredModelArn: str
    foundationModelArn: str
    modelUnits: int
    desiredModelUnits: int
    status: ProvisionedModelStatusType
    creationTime: datetime
    lastModifiedTime: datetime
    commitmentDuration: NotRequired[CommitmentDurationType]
    commitmentExpirationTime: NotRequired[datetime]

class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceARN: str

class S3DataSourceTypeDef(TypedDict):
    s3Uri: str

class ModelInvocationJobS3InputDataConfigTypeDef(TypedDict):
    s3Uri: str
    s3InputFormat: NotRequired[Literal["JSONL"]]
    s3BucketOwner: NotRequired[str]

class ModelInvocationJobS3OutputDataConfigTypeDef(TypedDict):
    s3Uri: str
    s3EncryptionKeyId: NotRequired[str]
    s3BucketOwner: NotRequired[str]

QueryTransformationConfigurationTypeDef = TypedDict(
    "QueryTransformationConfigurationTypeDef",
    {
        "type": Literal["QUERY_DECOMPOSITION"],
    },
)

class RatingScaleItemValueTypeDef(TypedDict):
    stringValue: NotRequired[str]
    floatValue: NotRequired[float]

class RegisterMarketplaceModelEndpointRequestTypeDef(TypedDict):
    endpointIdentifier: str
    modelSourceIdentifier: str

class RequestMetadataBaseFiltersOutputTypeDef(TypedDict):
    equals: NotRequired[Dict[str, str]]
    notEquals: NotRequired[Dict[str, str]]

class RequestMetadataBaseFiltersTypeDef(TypedDict):
    equals: NotRequired[Mapping[str, str]]
    notEquals: NotRequired[Mapping[str, str]]

class VpcConfigTypeDef(TypedDict):
    subnetIds: Sequence[str]
    securityGroupIds: Sequence[str]

class TrainingDetailsTypeDef(TypedDict):
    status: NotRequired[JobStatusDetailsType]
    creationTime: NotRequired[datetime]
    lastModifiedTime: NotRequired[datetime]

class ValidationDetailsTypeDef(TypedDict):
    status: NotRequired[JobStatusDetailsType]
    creationTime: NotRequired[datetime]
    lastModifiedTime: NotRequired[datetime]

class StopEvaluationJobRequestTypeDef(TypedDict):
    jobIdentifier: str

class StopModelCustomizationJobRequestTypeDef(TypedDict):
    jobIdentifier: str

class StopModelInvocationJobRequestTypeDef(TypedDict):
    jobIdentifier: str

class SupportTermTypeDef(TypedDict):
    refundPolicyDescription: NotRequired[str]

class ValidityTermTypeDef(TypedDict):
    agreementDuration: NotRequired[str]

class UntagResourceRequestTypeDef(TypedDict):
    resourceARN: str
    tagKeys: Sequence[str]

class UpdateProvisionedModelThroughputRequestTypeDef(TypedDict):
    provisionedModelId: str
    desiredProvisionedModelName: NotRequired[str]
    desiredModelId: NotRequired[str]

class ValidatorTypeDef(TypedDict):
    s3Uri: str

class VectorSearchBedrockRerankingModelConfigurationOutputTypeDef(TypedDict):
    modelArn: str
    additionalModelRequestFields: NotRequired[Dict[str, Dict[str, Any]]]

class VectorSearchBedrockRerankingModelConfigurationTypeDef(TypedDict):
    modelArn: str
    additionalModelRequestFields: NotRequired[Mapping[str, Mapping[str, Any]]]

class BatchDeleteEvaluationJobResponseTypeDef(TypedDict):
    errors: List[BatchDeleteEvaluationJobErrorTypeDef]
    evaluationJobs: List[BatchDeleteEvaluationJobItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCustomModelDeploymentResponseTypeDef(TypedDict):
    customModelDeploymentArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCustomModelResponseTypeDef(TypedDict):
    modelArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateEvaluationJobResponseTypeDef(TypedDict):
    jobArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateFoundationModelAgreementResponseTypeDef(TypedDict):
    modelId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateGuardrailResponseTypeDef(TypedDict):
    guardrailId: str
    guardrailArn: str
    version: str
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateGuardrailVersionResponseTypeDef(TypedDict):
    guardrailId: str
    version: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateInferenceProfileResponseTypeDef(TypedDict):
    inferenceProfileArn: str
    status: Literal["ACTIVE"]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateModelCopyJobResponseTypeDef(TypedDict):
    jobArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateModelCustomizationJobResponseTypeDef(TypedDict):
    jobArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateModelImportJobResponseTypeDef(TypedDict):
    jobArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateModelInvocationJobResponseTypeDef(TypedDict):
    jobArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreatePromptRouterResponseTypeDef(TypedDict):
    promptRouterArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateProvisionedModelThroughputResponseTypeDef(TypedDict):
    provisionedModelArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetCustomModelDeploymentResponseTypeDef(TypedDict):
    customModelDeploymentArn: str
    modelDeploymentName: str
    modelArn: str
    createdAt: datetime
    status: CustomModelDeploymentStatusType
    description: str
    failureMessage: str
    lastUpdatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetFoundationModelAvailabilityResponseTypeDef(TypedDict):
    modelId: str
    agreementAvailability: AgreementAvailabilityTypeDef
    authorizationStatus: AuthorizationStatusType
    entitlementAvailability: EntitlementAvailabilityType
    regionAvailability: RegionAvailabilityType
    ResponseMetadata: ResponseMetadataTypeDef

class GetProvisionedModelThroughputResponseTypeDef(TypedDict):
    modelUnits: int
    desiredModelUnits: int
    provisionedModelName: str
    provisionedModelArn: str
    modelArn: str
    desiredModelArn: str
    foundationModelArn: str
    status: ProvisionedModelStatusType
    creationTime: datetime
    lastModifiedTime: datetime
    failureMessage: str
    commitmentDuration: CommitmentDurationType
    commitmentExpirationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetUseCaseForModelAccessResponseTypeDef(TypedDict):
    formData: bytes
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateGuardrailResponseTypeDef(TypedDict):
    guardrailId: str
    guardrailArn: str
    version: str
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class EvaluatorModelConfigOutputTypeDef(TypedDict):
    bedrockEvaluatorModels: NotRequired[List[BedrockEvaluatorModelTypeDef]]

class EvaluatorModelConfigTypeDef(TypedDict):
    bedrockEvaluatorModels: NotRequired[Sequence[BedrockEvaluatorModelTypeDef]]

class ByteContentDocTypeDef(TypedDict):
    identifier: str
    contentType: str
    data: BlobTypeDef

class PutUseCaseForModelAccessRequestTypeDef(TypedDict):
    formData: BlobTypeDef

class CloudWatchConfigTypeDef(TypedDict):
    logGroupName: str
    roleArn: str
    largeDataDeliveryS3Config: NotRequired[S3ConfigTypeDef]

class CreateCustomModelDeploymentRequestTypeDef(TypedDict):
    modelDeploymentName: str
    modelArn: str
    description: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    clientRequestToken: NotRequired[str]

class CreateModelCopyJobRequestTypeDef(TypedDict):
    sourceModelArn: str
    targetModelName: str
    modelKmsKeyId: NotRequired[str]
    targetModelTags: NotRequired[Sequence[TagTypeDef]]
    clientRequestToken: NotRequired[str]

class CreateProvisionedModelThroughputRequestTypeDef(TypedDict):
    modelUnits: int
    provisionedModelName: str
    modelId: str
    clientRequestToken: NotRequired[str]
    commitmentDuration: NotRequired[CommitmentDurationType]
    tags: NotRequired[Sequence[TagTypeDef]]

class GetModelCopyJobResponseTypeDef(TypedDict):
    jobArn: str
    status: ModelCopyJobStatusType
    creationTime: datetime
    targetModelArn: str
    targetModelName: str
    sourceAccountId: str
    sourceModelArn: str
    targetModelKmsKeyArn: str
    targetModelTags: List[TagTypeDef]
    failureMessage: str
    sourceModelName: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ModelCopyJobSummaryTypeDef(TypedDict):
    jobArn: str
    status: ModelCopyJobStatusType
    creationTime: datetime
    targetModelArn: str
    sourceAccountId: str
    sourceModelArn: str
    targetModelName: NotRequired[str]
    targetModelKmsKeyArn: NotRequired[str]
    targetModelTags: NotRequired[List[TagTypeDef]]
    failureMessage: NotRequired[str]
    sourceModelName: NotRequired[str]

class TagResourceRequestTypeDef(TypedDict):
    resourceARN: str
    tags: Sequence[TagTypeDef]

class CreateInferenceProfileRequestTypeDef(TypedDict):
    inferenceProfileName: str
    modelSource: InferenceProfileModelSourceTypeDef
    description: NotRequired[str]
    clientRequestToken: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class CreatePromptRouterRequestTypeDef(TypedDict):
    promptRouterName: str
    models: Sequence[PromptRouterTargetModelTypeDef]
    routingCriteria: RoutingCriteriaTypeDef
    fallbackModel: PromptRouterTargetModelTypeDef
    clientRequestToken: NotRequired[str]
    description: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

GetPromptRouterResponseTypeDef = TypedDict(
    "GetPromptRouterResponseTypeDef",
    {
        "promptRouterName": str,
        "routingCriteria": RoutingCriteriaTypeDef,
        "description": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "promptRouterArn": str,
        "models": List[PromptRouterTargetModelTypeDef],
        "fallbackModel": PromptRouterTargetModelTypeDef,
        "status": Literal["AVAILABLE"],
        "type": PromptRouterTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PromptRouterSummaryTypeDef = TypedDict(
    "PromptRouterSummaryTypeDef",
    {
        "promptRouterName": str,
        "routingCriteria": RoutingCriteriaTypeDef,
        "promptRouterArn": str,
        "models": List[PromptRouterTargetModelTypeDef],
        "fallbackModel": PromptRouterTargetModelTypeDef,
        "status": Literal["AVAILABLE"],
        "type": PromptRouterTypeType,
        "description": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
    },
)

class CustomMetricEvaluatorModelConfigOutputTypeDef(TypedDict):
    bedrockEvaluatorModels: List[CustomMetricBedrockEvaluatorModelTypeDef]

class CustomMetricEvaluatorModelConfigTypeDef(TypedDict):
    bedrockEvaluatorModels: Sequence[CustomMetricBedrockEvaluatorModelTypeDef]

class ListCustomModelDeploymentsResponseTypeDef(TypedDict):
    modelDeploymentSummaries: List[CustomModelDeploymentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListCustomModelsResponseTypeDef(TypedDict):
    modelSummaries: List[CustomModelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class PricingTermTypeDef(TypedDict):
    rateCard: List[DimensionalPriceRateTypeDef]

class DistillationConfigTypeDef(TypedDict):
    teacherModelConfig: TeacherModelConfigTypeDef

class EvaluationBedrockModelTypeDef(TypedDict):
    modelIdentifier: str
    inferenceParams: NotRequired[str]
    performanceConfig: NotRequired[PerformanceConfigurationTypeDef]

class EvaluationDatasetTypeDef(TypedDict):
    name: str
    datasetLocation: NotRequired[EvaluationDatasetLocationTypeDef]

class EvaluationInferenceConfigSummaryTypeDef(TypedDict):
    modelConfigSummary: NotRequired[EvaluationModelConfigSummaryTypeDef]
    ragConfigSummary: NotRequired[EvaluationRagConfigSummaryTypeDef]

class EvaluationPrecomputedRagSourceConfigTypeDef(TypedDict):
    retrieveSourceConfig: NotRequired[EvaluationPrecomputedRetrieveSourceConfigTypeDef]
    retrieveAndGenerateSourceConfig: NotRequired[
        EvaluationPrecomputedRetrieveAndGenerateSourceConfigTypeDef
    ]

class ExternalSourceOutputTypeDef(TypedDict):
    sourceType: ExternalSourceTypeType
    s3Location: NotRequired[S3ObjectDocTypeDef]
    byteContent: NotRequired[ByteContentDocOutputTypeDef]

class RerankingMetadataSelectiveModeConfigurationOutputTypeDef(TypedDict):
    fieldsToInclude: NotRequired[List[FieldForRerankingTypeDef]]
    fieldsToExclude: NotRequired[List[FieldForRerankingTypeDef]]

class RerankingMetadataSelectiveModeConfigurationTypeDef(TypedDict):
    fieldsToInclude: NotRequired[Sequence[FieldForRerankingTypeDef]]
    fieldsToExclude: NotRequired[Sequence[FieldForRerankingTypeDef]]

RetrievalFilterOutputTypeDef = TypedDict(
    "RetrievalFilterOutputTypeDef",
    {
        "equals": NotRequired[FilterAttributeOutputTypeDef],
        "notEquals": NotRequired[FilterAttributeOutputTypeDef],
        "greaterThan": NotRequired[FilterAttributeOutputTypeDef],
        "greaterThanOrEquals": NotRequired[FilterAttributeOutputTypeDef],
        "lessThan": NotRequired[FilterAttributeOutputTypeDef],
        "lessThanOrEquals": NotRequired[FilterAttributeOutputTypeDef],
        "in": NotRequired[FilterAttributeOutputTypeDef],
        "notIn": NotRequired[FilterAttributeOutputTypeDef],
        "startsWith": NotRequired[FilterAttributeOutputTypeDef],
        "listContains": NotRequired[FilterAttributeOutputTypeDef],
        "stringContains": NotRequired[FilterAttributeOutputTypeDef],
        "andAll": NotRequired[List[Dict[str, Any]]],
        "orAll": NotRequired[List[Dict[str, Any]]],
    },
)
RetrievalFilterTypeDef = TypedDict(
    "RetrievalFilterTypeDef",
    {
        "equals": NotRequired[FilterAttributeTypeDef],
        "notEquals": NotRequired[FilterAttributeTypeDef],
        "greaterThan": NotRequired[FilterAttributeTypeDef],
        "greaterThanOrEquals": NotRequired[FilterAttributeTypeDef],
        "lessThan": NotRequired[FilterAttributeTypeDef],
        "lessThanOrEquals": NotRequired[FilterAttributeTypeDef],
        "in": NotRequired[FilterAttributeTypeDef],
        "notIn": NotRequired[FilterAttributeTypeDef],
        "startsWith": NotRequired[FilterAttributeTypeDef],
        "listContains": NotRequired[FilterAttributeTypeDef],
        "stringContains": NotRequired[FilterAttributeTypeDef],
        "andAll": NotRequired[Sequence[Mapping[str, Any]]],
        "orAll": NotRequired[Sequence[Mapping[str, Any]]],
    },
)

class FoundationModelDetailsTypeDef(TypedDict):
    modelArn: str
    modelId: str
    modelName: NotRequired[str]
    providerName: NotRequired[str]
    inputModalities: NotRequired[List[ModelModalityType]]
    outputModalities: NotRequired[List[ModelModalityType]]
    responseStreamingSupported: NotRequired[bool]
    customizationsSupported: NotRequired[List[ModelCustomizationType]]
    inferenceTypesSupported: NotRequired[List[InferenceTypeType]]
    modelLifecycle: NotRequired[FoundationModelLifecycleTypeDef]

class FoundationModelSummaryTypeDef(TypedDict):
    modelArn: str
    modelId: str
    modelName: NotRequired[str]
    providerName: NotRequired[str]
    inputModalities: NotRequired[List[ModelModalityType]]
    outputModalities: NotRequired[List[ModelModalityType]]
    responseStreamingSupported: NotRequired[bool]
    customizationsSupported: NotRequired[List[ModelCustomizationType]]
    inferenceTypesSupported: NotRequired[List[InferenceTypeType]]
    modelLifecycle: NotRequired[FoundationModelLifecycleTypeDef]

GuardrailSummaryTypeDef = TypedDict(
    "GuardrailSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "status": GuardrailStatusType,
        "name": str,
        "version": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "description": NotRequired[str],
        "crossRegionDetails": NotRequired[GuardrailCrossRegionDetailsTypeDef],
    },
)
GetInferenceProfileResponseTypeDef = TypedDict(
    "GetInferenceProfileResponseTypeDef",
    {
        "inferenceProfileName": str,
        "description": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "inferenceProfileArn": str,
        "models": List[InferenceProfileModelTypeDef],
        "inferenceProfileId": str,
        "status": Literal["ACTIVE"],
        "type": InferenceProfileTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
InferenceProfileSummaryTypeDef = TypedDict(
    "InferenceProfileSummaryTypeDef",
    {
        "inferenceProfileName": str,
        "inferenceProfileArn": str,
        "models": List[InferenceProfileModelTypeDef],
        "inferenceProfileId": str,
        "status": Literal["ACTIVE"],
        "type": InferenceProfileTypeType,
        "description": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
    },
)

class SageMakerEndpointOutputTypeDef(TypedDict):
    initialInstanceCount: int
    instanceType: str
    executionRole: str
    kmsEncryptionKey: NotRequired[str]
    vpc: NotRequired[VpcConfigOutputTypeDef]

class GuardrailContentPolicyConfigTypeDef(TypedDict):
    filtersConfig: Sequence[GuardrailContentFilterConfigTypeDef]
    tierConfig: NotRequired[GuardrailContentFiltersTierConfigTypeDef]

class GuardrailContentPolicyTypeDef(TypedDict):
    filters: NotRequired[List[GuardrailContentFilterTypeDef]]
    tier: NotRequired[GuardrailContentFiltersTierTypeDef]

class GuardrailContextualGroundingPolicyConfigTypeDef(TypedDict):
    filtersConfig: Sequence[GuardrailContextualGroundingFilterConfigTypeDef]

class GuardrailContextualGroundingPolicyTypeDef(TypedDict):
    filters: List[GuardrailContextualGroundingFilterTypeDef]

class GuardrailSensitiveInformationPolicyConfigTypeDef(TypedDict):
    piiEntitiesConfig: NotRequired[Sequence[GuardrailPiiEntityConfigTypeDef]]
    regexesConfig: NotRequired[Sequence[GuardrailRegexConfigTypeDef]]

class GuardrailSensitiveInformationPolicyTypeDef(TypedDict):
    piiEntities: NotRequired[List[GuardrailPiiEntityTypeDef]]
    regexes: NotRequired[List[GuardrailRegexTypeDef]]

class GuardrailTopicPolicyConfigTypeDef(TypedDict):
    topicsConfig: Sequence[GuardrailTopicConfigTypeDef]
    tierConfig: NotRequired[GuardrailTopicsTierConfigTypeDef]

class GuardrailTopicPolicyTypeDef(TypedDict):
    topics: List[GuardrailTopicTypeDef]
    tier: NotRequired[GuardrailTopicsTierTypeDef]

class GuardrailWordPolicyConfigTypeDef(TypedDict):
    wordsConfig: NotRequired[Sequence[GuardrailWordConfigTypeDef]]
    managedWordListsConfig: NotRequired[Sequence[GuardrailManagedWordsConfigTypeDef]]

class GuardrailWordPolicyTypeDef(TypedDict):
    words: NotRequired[List[GuardrailWordTypeDef]]
    managedWordLists: NotRequired[List[GuardrailManagedWordsTypeDef]]

class ImplicitFilterConfigurationOutputTypeDef(TypedDict):
    metadataAttributes: List[MetadataAttributeSchemaTypeDef]
    modelArn: str

class ImplicitFilterConfigurationTypeDef(TypedDict):
    metadataAttributes: Sequence[MetadataAttributeSchemaTypeDef]
    modelArn: str

class ListImportedModelsResponseTypeDef(TypedDict):
    modelSummaries: List[ImportedModelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class KbInferenceConfigOutputTypeDef(TypedDict):
    textInferenceConfig: NotRequired[TextInferenceConfigOutputTypeDef]

class KbInferenceConfigTypeDef(TypedDict):
    textInferenceConfig: NotRequired[TextInferenceConfigTypeDef]

class ListGuardrailsRequestPaginateTypeDef(TypedDict):
    guardrailIdentifier: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListInferenceProfilesRequestPaginateTypeDef(TypedDict):
    typeEquals: NotRequired[InferenceProfileTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListMarketplaceModelEndpointsRequestPaginateTypeDef(TypedDict):
    modelSourceEquals: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListPromptRoutersRequestPaginateTypeDef = TypedDict(
    "ListPromptRoutersRequestPaginateTypeDef",
    {
        "type": NotRequired[PromptRouterTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListCustomModelDeploymentsRequestPaginateTypeDef(TypedDict):
    createdBefore: NotRequired[TimestampTypeDef]
    createdAfter: NotRequired[TimestampTypeDef]
    nameContains: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]
    statusEquals: NotRequired[CustomModelDeploymentStatusType]
    modelArnEquals: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCustomModelDeploymentsRequestTypeDef(TypedDict):
    createdBefore: NotRequired[TimestampTypeDef]
    createdAfter: NotRequired[TimestampTypeDef]
    nameContains: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]
    statusEquals: NotRequired[CustomModelDeploymentStatusType]
    modelArnEquals: NotRequired[str]

class ListCustomModelsRequestPaginateTypeDef(TypedDict):
    creationTimeBefore: NotRequired[TimestampTypeDef]
    creationTimeAfter: NotRequired[TimestampTypeDef]
    nameContains: NotRequired[str]
    baseModelArnEquals: NotRequired[str]
    foundationModelArnEquals: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]
    isOwned: NotRequired[bool]
    modelStatus: NotRequired[ModelStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCustomModelsRequestTypeDef(TypedDict):
    creationTimeBefore: NotRequired[TimestampTypeDef]
    creationTimeAfter: NotRequired[TimestampTypeDef]
    nameContains: NotRequired[str]
    baseModelArnEquals: NotRequired[str]
    foundationModelArnEquals: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]
    isOwned: NotRequired[bool]
    modelStatus: NotRequired[ModelStatusType]

class ListEvaluationJobsRequestPaginateTypeDef(TypedDict):
    creationTimeAfter: NotRequired[TimestampTypeDef]
    creationTimeBefore: NotRequired[TimestampTypeDef]
    statusEquals: NotRequired[EvaluationJobStatusType]
    applicationTypeEquals: NotRequired[ApplicationTypeType]
    nameContains: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEvaluationJobsRequestTypeDef(TypedDict):
    creationTimeAfter: NotRequired[TimestampTypeDef]
    creationTimeBefore: NotRequired[TimestampTypeDef]
    statusEquals: NotRequired[EvaluationJobStatusType]
    applicationTypeEquals: NotRequired[ApplicationTypeType]
    nameContains: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]

class ListImportedModelsRequestPaginateTypeDef(TypedDict):
    creationTimeBefore: NotRequired[TimestampTypeDef]
    creationTimeAfter: NotRequired[TimestampTypeDef]
    nameContains: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListImportedModelsRequestTypeDef(TypedDict):
    creationTimeBefore: NotRequired[TimestampTypeDef]
    creationTimeAfter: NotRequired[TimestampTypeDef]
    nameContains: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]

class ListModelCopyJobsRequestPaginateTypeDef(TypedDict):
    creationTimeAfter: NotRequired[TimestampTypeDef]
    creationTimeBefore: NotRequired[TimestampTypeDef]
    statusEquals: NotRequired[ModelCopyJobStatusType]
    sourceAccountEquals: NotRequired[str]
    sourceModelArnEquals: NotRequired[str]
    targetModelNameContains: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListModelCopyJobsRequestTypeDef(TypedDict):
    creationTimeAfter: NotRequired[TimestampTypeDef]
    creationTimeBefore: NotRequired[TimestampTypeDef]
    statusEquals: NotRequired[ModelCopyJobStatusType]
    sourceAccountEquals: NotRequired[str]
    sourceModelArnEquals: NotRequired[str]
    targetModelNameContains: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]

class ListModelCustomizationJobsRequestPaginateTypeDef(TypedDict):
    creationTimeAfter: NotRequired[TimestampTypeDef]
    creationTimeBefore: NotRequired[TimestampTypeDef]
    statusEquals: NotRequired[FineTuningJobStatusType]
    nameContains: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListModelCustomizationJobsRequestTypeDef(TypedDict):
    creationTimeAfter: NotRequired[TimestampTypeDef]
    creationTimeBefore: NotRequired[TimestampTypeDef]
    statusEquals: NotRequired[FineTuningJobStatusType]
    nameContains: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]

class ListModelImportJobsRequestPaginateTypeDef(TypedDict):
    creationTimeAfter: NotRequired[TimestampTypeDef]
    creationTimeBefore: NotRequired[TimestampTypeDef]
    statusEquals: NotRequired[ModelImportJobStatusType]
    nameContains: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListModelImportJobsRequestTypeDef(TypedDict):
    creationTimeAfter: NotRequired[TimestampTypeDef]
    creationTimeBefore: NotRequired[TimestampTypeDef]
    statusEquals: NotRequired[ModelImportJobStatusType]
    nameContains: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]

class ListModelInvocationJobsRequestPaginateTypeDef(TypedDict):
    submitTimeAfter: NotRequired[TimestampTypeDef]
    submitTimeBefore: NotRequired[TimestampTypeDef]
    statusEquals: NotRequired[ModelInvocationJobStatusType]
    nameContains: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListModelInvocationJobsRequestTypeDef(TypedDict):
    submitTimeAfter: NotRequired[TimestampTypeDef]
    submitTimeBefore: NotRequired[TimestampTypeDef]
    statusEquals: NotRequired[ModelInvocationJobStatusType]
    nameContains: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]

class ListProvisionedModelThroughputsRequestPaginateTypeDef(TypedDict):
    creationTimeAfter: NotRequired[TimestampTypeDef]
    creationTimeBefore: NotRequired[TimestampTypeDef]
    statusEquals: NotRequired[ProvisionedModelStatusType]
    modelArnEquals: NotRequired[str]
    nameContains: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListProvisionedModelThroughputsRequestTypeDef(TypedDict):
    creationTimeAfter: NotRequired[TimestampTypeDef]
    creationTimeBefore: NotRequired[TimestampTypeDef]
    statusEquals: NotRequired[ProvisionedModelStatusType]
    modelArnEquals: NotRequired[str]
    nameContains: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    sortBy: NotRequired[Literal["CreationTime"]]
    sortOrder: NotRequired[SortOrderType]

class ListMarketplaceModelEndpointsResponseTypeDef(TypedDict):
    marketplaceModelEndpoints: List[MarketplaceModelEndpointSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListModelImportJobsResponseTypeDef(TypedDict):
    modelImportJobSummaries: List[ModelImportJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListProvisionedModelThroughputsResponseTypeDef(TypedDict):
    provisionedModelSummaries: List[ProvisionedModelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ModelDataSourceTypeDef(TypedDict):
    s3DataSource: NotRequired[S3DataSourceTypeDef]

class ModelInvocationJobInputDataConfigTypeDef(TypedDict):
    s3InputDataConfig: NotRequired[ModelInvocationJobS3InputDataConfigTypeDef]

class ModelInvocationJobOutputDataConfigTypeDef(TypedDict):
    s3OutputDataConfig: NotRequired[ModelInvocationJobS3OutputDataConfigTypeDef]

class OrchestrationConfigurationTypeDef(TypedDict):
    queryTransformationConfiguration: QueryTransformationConfigurationTypeDef

class RatingScaleItemTypeDef(TypedDict):
    definition: str
    value: RatingScaleItemValueTypeDef

class RequestMetadataFiltersOutputTypeDef(TypedDict):
    equals: NotRequired[Dict[str, str]]
    notEquals: NotRequired[Dict[str, str]]
    andAll: NotRequired[List[RequestMetadataBaseFiltersOutputTypeDef]]
    orAll: NotRequired[List[RequestMetadataBaseFiltersOutputTypeDef]]

class RequestMetadataFiltersTypeDef(TypedDict):
    equals: NotRequired[Mapping[str, str]]
    notEquals: NotRequired[Mapping[str, str]]
    andAll: NotRequired[Sequence[RequestMetadataBaseFiltersTypeDef]]
    orAll: NotRequired[Sequence[RequestMetadataBaseFiltersTypeDef]]

class SageMakerEndpointTypeDef(TypedDict):
    initialInstanceCount: int
    instanceType: str
    executionRole: str
    kmsEncryptionKey: NotRequired[str]
    vpc: NotRequired[VpcConfigTypeDef]

VpcConfigUnionTypeDef = Union[VpcConfigTypeDef, VpcConfigOutputTypeDef]

class StatusDetailsTypeDef(TypedDict):
    validationDetails: NotRequired[ValidationDetailsTypeDef]
    dataProcessingDetails: NotRequired[DataProcessingDetailsTypeDef]
    trainingDetails: NotRequired[TrainingDetailsTypeDef]

class ValidationDataConfigOutputTypeDef(TypedDict):
    validators: List[ValidatorTypeDef]

class ValidationDataConfigTypeDef(TypedDict):
    validators: Sequence[ValidatorTypeDef]

class ExternalSourceTypeDef(TypedDict):
    sourceType: ExternalSourceTypeType
    s3Location: NotRequired[S3ObjectDocTypeDef]
    byteContent: NotRequired[ByteContentDocTypeDef]

class LoggingConfigTypeDef(TypedDict):
    cloudWatchConfig: NotRequired[CloudWatchConfigTypeDef]
    s3Config: NotRequired[S3ConfigTypeDef]
    textDataDeliveryEnabled: NotRequired[bool]
    imageDataDeliveryEnabled: NotRequired[bool]
    embeddingDataDeliveryEnabled: NotRequired[bool]
    videoDataDeliveryEnabled: NotRequired[bool]

class ListModelCopyJobsResponseTypeDef(TypedDict):
    modelCopyJobSummaries: List[ModelCopyJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListPromptRoutersResponseTypeDef(TypedDict):
    promptRouterSummaries: List[PromptRouterSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class TermDetailsTypeDef(TypedDict):
    usageBasedPricingTerm: PricingTermTypeDef
    legalTerm: LegalTermTypeDef
    supportTerm: SupportTermTypeDef
    validityTerm: NotRequired[ValidityTermTypeDef]

class CustomizationConfigTypeDef(TypedDict):
    distillationConfig: NotRequired[DistillationConfigTypeDef]

class EvaluationModelConfigTypeDef(TypedDict):
    bedrockModel: NotRequired[EvaluationBedrockModelTypeDef]
    precomputedInferenceSource: NotRequired[EvaluationPrecomputedInferenceSourceTypeDef]

class EvaluationDatasetMetricConfigOutputTypeDef(TypedDict):
    taskType: EvaluationTaskTypeType
    dataset: EvaluationDatasetTypeDef
    metricNames: List[str]

class EvaluationDatasetMetricConfigTypeDef(TypedDict):
    taskType: EvaluationTaskTypeType
    dataset: EvaluationDatasetTypeDef
    metricNames: Sequence[str]

class EvaluationSummaryTypeDef(TypedDict):
    jobArn: str
    jobName: str
    status: EvaluationJobStatusType
    creationTime: datetime
    jobType: EvaluationJobTypeType
    evaluationTaskTypes: List[EvaluationTaskTypeType]
    modelIdentifiers: NotRequired[List[str]]
    ragIdentifiers: NotRequired[List[str]]
    evaluatorModelIdentifiers: NotRequired[List[str]]
    customMetricsEvaluatorModelIdentifiers: NotRequired[List[str]]
    inferenceConfigSummary: NotRequired[EvaluationInferenceConfigSummaryTypeDef]
    applicationType: NotRequired[ApplicationTypeType]

class MetadataConfigurationForRerankingOutputTypeDef(TypedDict):
    selectionMode: RerankingMetadataSelectionModeType
    selectiveModeConfiguration: NotRequired[
        RerankingMetadataSelectiveModeConfigurationOutputTypeDef
    ]

class MetadataConfigurationForRerankingTypeDef(TypedDict):
    selectionMode: RerankingMetadataSelectionModeType
    selectiveModeConfiguration: NotRequired[RerankingMetadataSelectiveModeConfigurationTypeDef]

class GetFoundationModelResponseTypeDef(TypedDict):
    modelDetails: FoundationModelDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListFoundationModelsResponseTypeDef(TypedDict):
    modelSummaries: List[FoundationModelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListGuardrailsResponseTypeDef(TypedDict):
    guardrails: List[GuardrailSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListInferenceProfilesResponseTypeDef(TypedDict):
    inferenceProfileSummaries: List[InferenceProfileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class EndpointConfigOutputTypeDef(TypedDict):
    sageMaker: NotRequired[SageMakerEndpointOutputTypeDef]

class CreateGuardrailRequestTypeDef(TypedDict):
    name: str
    blockedInputMessaging: str
    blockedOutputsMessaging: str
    description: NotRequired[str]
    topicPolicyConfig: NotRequired[GuardrailTopicPolicyConfigTypeDef]
    contentPolicyConfig: NotRequired[GuardrailContentPolicyConfigTypeDef]
    wordPolicyConfig: NotRequired[GuardrailWordPolicyConfigTypeDef]
    sensitiveInformationPolicyConfig: NotRequired[GuardrailSensitiveInformationPolicyConfigTypeDef]
    contextualGroundingPolicyConfig: NotRequired[GuardrailContextualGroundingPolicyConfigTypeDef]
    crossRegionConfig: NotRequired[GuardrailCrossRegionConfigTypeDef]
    kmsKeyId: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    clientRequestToken: NotRequired[str]

class UpdateGuardrailRequestTypeDef(TypedDict):
    guardrailIdentifier: str
    name: str
    blockedInputMessaging: str
    blockedOutputsMessaging: str
    description: NotRequired[str]
    topicPolicyConfig: NotRequired[GuardrailTopicPolicyConfigTypeDef]
    contentPolicyConfig: NotRequired[GuardrailContentPolicyConfigTypeDef]
    wordPolicyConfig: NotRequired[GuardrailWordPolicyConfigTypeDef]
    sensitiveInformationPolicyConfig: NotRequired[GuardrailSensitiveInformationPolicyConfigTypeDef]
    contextualGroundingPolicyConfig: NotRequired[GuardrailContextualGroundingPolicyConfigTypeDef]
    crossRegionConfig: NotRequired[GuardrailCrossRegionConfigTypeDef]
    kmsKeyId: NotRequired[str]

class GetGuardrailResponseTypeDef(TypedDict):
    name: str
    description: str
    guardrailId: str
    guardrailArn: str
    version: str
    status: GuardrailStatusType
    topicPolicy: GuardrailTopicPolicyTypeDef
    contentPolicy: GuardrailContentPolicyTypeDef
    wordPolicy: GuardrailWordPolicyTypeDef
    sensitiveInformationPolicy: GuardrailSensitiveInformationPolicyTypeDef
    contextualGroundingPolicy: GuardrailContextualGroundingPolicyTypeDef
    crossRegionDetails: GuardrailCrossRegionDetailsTypeDef
    createdAt: datetime
    updatedAt: datetime
    statusReasons: List[str]
    failureRecommendations: List[str]
    blockedInputMessaging: str
    blockedOutputsMessaging: str
    kmsKeyArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class ExternalSourcesGenerationConfigurationOutputTypeDef(TypedDict):
    promptTemplate: NotRequired[PromptTemplateTypeDef]
    guardrailConfiguration: NotRequired[GuardrailConfigurationTypeDef]
    kbInferenceConfig: NotRequired[KbInferenceConfigOutputTypeDef]
    additionalModelRequestFields: NotRequired[Dict[str, Dict[str, Any]]]

class GenerationConfigurationOutputTypeDef(TypedDict):
    promptTemplate: NotRequired[PromptTemplateTypeDef]
    guardrailConfiguration: NotRequired[GuardrailConfigurationTypeDef]
    kbInferenceConfig: NotRequired[KbInferenceConfigOutputTypeDef]
    additionalModelRequestFields: NotRequired[Dict[str, Dict[str, Any]]]

class ExternalSourcesGenerationConfigurationTypeDef(TypedDict):
    promptTemplate: NotRequired[PromptTemplateTypeDef]
    guardrailConfiguration: NotRequired[GuardrailConfigurationTypeDef]
    kbInferenceConfig: NotRequired[KbInferenceConfigTypeDef]
    additionalModelRequestFields: NotRequired[Mapping[str, Mapping[str, Any]]]

class GenerationConfigurationTypeDef(TypedDict):
    promptTemplate: NotRequired[PromptTemplateTypeDef]
    guardrailConfiguration: NotRequired[GuardrailConfigurationTypeDef]
    kbInferenceConfig: NotRequired[KbInferenceConfigTypeDef]
    additionalModelRequestFields: NotRequired[Mapping[str, Mapping[str, Any]]]

class CreateCustomModelRequestTypeDef(TypedDict):
    modelName: str
    modelSourceConfig: ModelDataSourceTypeDef
    modelKmsKeyArn: NotRequired[str]
    roleArn: NotRequired[str]
    modelTags: NotRequired[Sequence[TagTypeDef]]
    clientRequestToken: NotRequired[str]

class GetImportedModelResponseTypeDef(TypedDict):
    modelArn: str
    modelName: str
    jobName: str
    jobArn: str
    modelDataSource: ModelDataSourceTypeDef
    creationTime: datetime
    modelArchitecture: str
    modelKmsKeyArn: str
    instructSupported: bool
    customModelUnits: CustomModelUnitsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetModelImportJobResponseTypeDef(TypedDict):
    jobArn: str
    jobName: str
    importedModelName: str
    importedModelArn: str
    roleArn: str
    modelDataSource: ModelDataSourceTypeDef
    status: ModelImportJobStatusType
    failureMessage: str
    creationTime: datetime
    lastModifiedTime: datetime
    endTime: datetime
    vpcConfig: VpcConfigOutputTypeDef
    importedModelKmsKeyArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetModelInvocationJobResponseTypeDef(TypedDict):
    jobArn: str
    jobName: str
    modelId: str
    clientRequestToken: str
    roleArn: str
    status: ModelInvocationJobStatusType
    message: str
    submitTime: datetime
    lastModifiedTime: datetime
    endTime: datetime
    inputDataConfig: ModelInvocationJobInputDataConfigTypeDef
    outputDataConfig: ModelInvocationJobOutputDataConfigTypeDef
    vpcConfig: VpcConfigOutputTypeDef
    timeoutDurationInHours: int
    jobExpirationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ModelInvocationJobSummaryTypeDef(TypedDict):
    jobArn: str
    jobName: str
    modelId: str
    roleArn: str
    submitTime: datetime
    inputDataConfig: ModelInvocationJobInputDataConfigTypeDef
    outputDataConfig: ModelInvocationJobOutputDataConfigTypeDef
    clientRequestToken: NotRequired[str]
    status: NotRequired[ModelInvocationJobStatusType]
    message: NotRequired[str]
    lastModifiedTime: NotRequired[datetime]
    endTime: NotRequired[datetime]
    vpcConfig: NotRequired[VpcConfigOutputTypeDef]
    timeoutDurationInHours: NotRequired[int]
    jobExpirationTime: NotRequired[datetime]

class CustomMetricDefinitionOutputTypeDef(TypedDict):
    name: str
    instructions: str
    ratingScale: NotRequired[List[RatingScaleItemTypeDef]]

class CustomMetricDefinitionTypeDef(TypedDict):
    name: str
    instructions: str
    ratingScale: NotRequired[Sequence[RatingScaleItemTypeDef]]

class InvocationLogsConfigOutputTypeDef(TypedDict):
    invocationLogSource: InvocationLogSourceTypeDef
    usePromptResponse: NotRequired[bool]
    requestMetadataFilters: NotRequired[RequestMetadataFiltersOutputTypeDef]

class InvocationLogsConfigTypeDef(TypedDict):
    invocationLogSource: InvocationLogSourceTypeDef
    usePromptResponse: NotRequired[bool]
    requestMetadataFilters: NotRequired[RequestMetadataFiltersTypeDef]

class EndpointConfigTypeDef(TypedDict):
    sageMaker: NotRequired[SageMakerEndpointTypeDef]

class CreateModelImportJobRequestTypeDef(TypedDict):
    jobName: str
    importedModelName: str
    roleArn: str
    modelDataSource: ModelDataSourceTypeDef
    jobTags: NotRequired[Sequence[TagTypeDef]]
    importedModelTags: NotRequired[Sequence[TagTypeDef]]
    clientRequestToken: NotRequired[str]
    vpcConfig: NotRequired[VpcConfigUnionTypeDef]
    importedModelKmsKeyId: NotRequired[str]

class CreateModelInvocationJobRequestTypeDef(TypedDict):
    jobName: str
    roleArn: str
    modelId: str
    inputDataConfig: ModelInvocationJobInputDataConfigTypeDef
    outputDataConfig: ModelInvocationJobOutputDataConfigTypeDef
    clientRequestToken: NotRequired[str]
    vpcConfig: NotRequired[VpcConfigUnionTypeDef]
    timeoutDurationInHours: NotRequired[int]
    tags: NotRequired[Sequence[TagTypeDef]]

class ModelCustomizationJobSummaryTypeDef(TypedDict):
    jobArn: str
    baseModelArn: str
    jobName: str
    status: ModelCustomizationJobStatusType
    creationTime: datetime
    statusDetails: NotRequired[StatusDetailsTypeDef]
    lastModifiedTime: NotRequired[datetime]
    endTime: NotRequired[datetime]
    customModelArn: NotRequired[str]
    customModelName: NotRequired[str]
    customizationType: NotRequired[CustomizationTypeType]

ValidationDataConfigUnionTypeDef = Union[
    ValidationDataConfigTypeDef, ValidationDataConfigOutputTypeDef
]

class GetModelInvocationLoggingConfigurationResponseTypeDef(TypedDict):
    loggingConfig: LoggingConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutModelInvocationLoggingConfigurationRequestTypeDef(TypedDict):
    loggingConfig: LoggingConfigTypeDef

class OfferTypeDef(TypedDict):
    offerToken: str
    termDetails: TermDetailsTypeDef
    offerId: NotRequired[str]

class HumanEvaluationConfigOutputTypeDef(TypedDict):
    datasetMetricConfigs: List[EvaluationDatasetMetricConfigOutputTypeDef]
    humanWorkflowConfig: NotRequired[HumanWorkflowConfigTypeDef]
    customMetrics: NotRequired[List[HumanEvaluationCustomMetricTypeDef]]

class HumanEvaluationConfigTypeDef(TypedDict):
    datasetMetricConfigs: Sequence[EvaluationDatasetMetricConfigTypeDef]
    humanWorkflowConfig: NotRequired[HumanWorkflowConfigTypeDef]
    customMetrics: NotRequired[Sequence[HumanEvaluationCustomMetricTypeDef]]

class ListEvaluationJobsResponseTypeDef(TypedDict):
    jobSummaries: List[EvaluationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class VectorSearchBedrockRerankingConfigurationOutputTypeDef(TypedDict):
    modelConfiguration: VectorSearchBedrockRerankingModelConfigurationOutputTypeDef
    numberOfRerankedResults: NotRequired[int]
    metadataConfiguration: NotRequired[MetadataConfigurationForRerankingOutputTypeDef]

class VectorSearchBedrockRerankingConfigurationTypeDef(TypedDict):
    modelConfiguration: VectorSearchBedrockRerankingModelConfigurationTypeDef
    numberOfRerankedResults: NotRequired[int]
    metadataConfiguration: NotRequired[MetadataConfigurationForRerankingTypeDef]

class MarketplaceModelEndpointTypeDef(TypedDict):
    endpointArn: str
    modelSourceIdentifier: str
    createdAt: datetime
    updatedAt: datetime
    endpointConfig: EndpointConfigOutputTypeDef
    endpointStatus: str
    status: NotRequired[StatusType]
    statusMessage: NotRequired[str]
    endpointStatusMessage: NotRequired[str]

class ExternalSourcesRetrieveAndGenerateConfigurationOutputTypeDef(TypedDict):
    modelArn: str
    sources: List[ExternalSourceOutputTypeDef]
    generationConfiguration: NotRequired[ExternalSourcesGenerationConfigurationOutputTypeDef]

class ExternalSourcesRetrieveAndGenerateConfigurationTypeDef(TypedDict):
    modelArn: str
    sources: Sequence[ExternalSourceTypeDef]
    generationConfiguration: NotRequired[ExternalSourcesGenerationConfigurationTypeDef]

class ListModelInvocationJobsResponseTypeDef(TypedDict):
    invocationJobSummaries: List[ModelInvocationJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class AutomatedEvaluationCustomMetricSourceOutputTypeDef(TypedDict):
    customMetricDefinition: NotRequired[CustomMetricDefinitionOutputTypeDef]

class AutomatedEvaluationCustomMetricSourceTypeDef(TypedDict):
    customMetricDefinition: NotRequired[CustomMetricDefinitionTypeDef]

class TrainingDataConfigOutputTypeDef(TypedDict):
    s3Uri: NotRequired[str]
    invocationLogsConfig: NotRequired[InvocationLogsConfigOutputTypeDef]

class TrainingDataConfigTypeDef(TypedDict):
    s3Uri: NotRequired[str]
    invocationLogsConfig: NotRequired[InvocationLogsConfigTypeDef]

EndpointConfigUnionTypeDef = Union[EndpointConfigTypeDef, EndpointConfigOutputTypeDef]

class ListModelCustomizationJobsResponseTypeDef(TypedDict):
    modelCustomizationJobSummaries: List[ModelCustomizationJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListFoundationModelAgreementOffersResponseTypeDef(TypedDict):
    modelId: str
    offers: List[OfferTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

VectorSearchRerankingConfigurationOutputTypeDef = TypedDict(
    "VectorSearchRerankingConfigurationOutputTypeDef",
    {
        "type": Literal["BEDROCK_RERANKING_MODEL"],
        "bedrockRerankingConfiguration": NotRequired[
            VectorSearchBedrockRerankingConfigurationOutputTypeDef
        ],
    },
)
VectorSearchRerankingConfigurationTypeDef = TypedDict(
    "VectorSearchRerankingConfigurationTypeDef",
    {
        "type": Literal["BEDROCK_RERANKING_MODEL"],
        "bedrockRerankingConfiguration": NotRequired[
            VectorSearchBedrockRerankingConfigurationTypeDef
        ],
    },
)

class CreateMarketplaceModelEndpointResponseTypeDef(TypedDict):
    marketplaceModelEndpoint: MarketplaceModelEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetMarketplaceModelEndpointResponseTypeDef(TypedDict):
    marketplaceModelEndpoint: MarketplaceModelEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class RegisterMarketplaceModelEndpointResponseTypeDef(TypedDict):
    marketplaceModelEndpoint: MarketplaceModelEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateMarketplaceModelEndpointResponseTypeDef(TypedDict):
    marketplaceModelEndpoint: MarketplaceModelEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class AutomatedEvaluationCustomMetricConfigOutputTypeDef(TypedDict):
    customMetrics: List[AutomatedEvaluationCustomMetricSourceOutputTypeDef]
    evaluatorModelConfig: CustomMetricEvaluatorModelConfigOutputTypeDef

class AutomatedEvaluationCustomMetricConfigTypeDef(TypedDict):
    customMetrics: Sequence[AutomatedEvaluationCustomMetricSourceTypeDef]
    evaluatorModelConfig: CustomMetricEvaluatorModelConfigTypeDef

class GetCustomModelResponseTypeDef(TypedDict):
    modelArn: str
    modelName: str
    jobName: str
    jobArn: str
    baseModelArn: str
    customizationType: CustomizationTypeType
    modelKmsKeyArn: str
    hyperParameters: Dict[str, str]
    trainingDataConfig: TrainingDataConfigOutputTypeDef
    validationDataConfig: ValidationDataConfigOutputTypeDef
    outputDataConfig: OutputDataConfigTypeDef
    trainingMetrics: TrainingMetricsTypeDef
    validationMetrics: List[ValidatorMetricTypeDef]
    creationTime: datetime
    customizationConfig: CustomizationConfigTypeDef
    modelStatus: ModelStatusType
    failureMessage: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetModelCustomizationJobResponseTypeDef(TypedDict):
    jobArn: str
    jobName: str
    outputModelName: str
    outputModelArn: str
    clientRequestToken: str
    roleArn: str
    status: ModelCustomizationJobStatusType
    statusDetails: StatusDetailsTypeDef
    failureMessage: str
    creationTime: datetime
    lastModifiedTime: datetime
    endTime: datetime
    baseModelArn: str
    hyperParameters: Dict[str, str]
    trainingDataConfig: TrainingDataConfigOutputTypeDef
    validationDataConfig: ValidationDataConfigOutputTypeDef
    outputDataConfig: OutputDataConfigTypeDef
    customizationType: CustomizationTypeType
    outputModelKmsKeyArn: str
    trainingMetrics: TrainingMetricsTypeDef
    validationMetrics: List[ValidatorMetricTypeDef]
    vpcConfig: VpcConfigOutputTypeDef
    customizationConfig: CustomizationConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

TrainingDataConfigUnionTypeDef = Union[TrainingDataConfigTypeDef, TrainingDataConfigOutputTypeDef]

class CreateMarketplaceModelEndpointRequestTypeDef(TypedDict):
    modelSourceIdentifier: str
    endpointConfig: EndpointConfigUnionTypeDef
    endpointName: str
    acceptEula: NotRequired[bool]
    clientRequestToken: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class UpdateMarketplaceModelEndpointRequestTypeDef(TypedDict):
    endpointArn: str
    endpointConfig: EndpointConfigUnionTypeDef
    clientRequestToken: NotRequired[str]

KnowledgeBaseVectorSearchConfigurationOutputTypeDef = TypedDict(
    "KnowledgeBaseVectorSearchConfigurationOutputTypeDef",
    {
        "numberOfResults": NotRequired[int],
        "overrideSearchType": NotRequired[SearchTypeType],
        "filter": NotRequired[RetrievalFilterOutputTypeDef],
        "implicitFilterConfiguration": NotRequired[ImplicitFilterConfigurationOutputTypeDef],
        "rerankingConfiguration": NotRequired[VectorSearchRerankingConfigurationOutputTypeDef],
    },
)
KnowledgeBaseVectorSearchConfigurationTypeDef = TypedDict(
    "KnowledgeBaseVectorSearchConfigurationTypeDef",
    {
        "numberOfResults": NotRequired[int],
        "overrideSearchType": NotRequired[SearchTypeType],
        "filter": NotRequired[RetrievalFilterTypeDef],
        "implicitFilterConfiguration": NotRequired[ImplicitFilterConfigurationTypeDef],
        "rerankingConfiguration": NotRequired[VectorSearchRerankingConfigurationTypeDef],
    },
)

class AutomatedEvaluationConfigOutputTypeDef(TypedDict):
    datasetMetricConfigs: List[EvaluationDatasetMetricConfigOutputTypeDef]
    evaluatorModelConfig: NotRequired[EvaluatorModelConfigOutputTypeDef]
    customMetricConfig: NotRequired[AutomatedEvaluationCustomMetricConfigOutputTypeDef]

class AutomatedEvaluationConfigTypeDef(TypedDict):
    datasetMetricConfigs: Sequence[EvaluationDatasetMetricConfigTypeDef]
    evaluatorModelConfig: NotRequired[EvaluatorModelConfigTypeDef]
    customMetricConfig: NotRequired[AutomatedEvaluationCustomMetricConfigTypeDef]

class CreateModelCustomizationJobRequestTypeDef(TypedDict):
    jobName: str
    customModelName: str
    roleArn: str
    baseModelIdentifier: str
    trainingDataConfig: TrainingDataConfigUnionTypeDef
    outputDataConfig: OutputDataConfigTypeDef
    clientRequestToken: NotRequired[str]
    customizationType: NotRequired[CustomizationTypeType]
    customModelKmsKeyId: NotRequired[str]
    jobTags: NotRequired[Sequence[TagTypeDef]]
    customModelTags: NotRequired[Sequence[TagTypeDef]]
    validationDataConfig: NotRequired[ValidationDataConfigUnionTypeDef]
    hyperParameters: NotRequired[Mapping[str, str]]
    vpcConfig: NotRequired[VpcConfigUnionTypeDef]
    customizationConfig: NotRequired[CustomizationConfigTypeDef]

class KnowledgeBaseRetrievalConfigurationOutputTypeDef(TypedDict):
    vectorSearchConfiguration: KnowledgeBaseVectorSearchConfigurationOutputTypeDef

class KnowledgeBaseRetrievalConfigurationTypeDef(TypedDict):
    vectorSearchConfiguration: KnowledgeBaseVectorSearchConfigurationTypeDef

class EvaluationConfigOutputTypeDef(TypedDict):
    automated: NotRequired[AutomatedEvaluationConfigOutputTypeDef]
    human: NotRequired[HumanEvaluationConfigOutputTypeDef]

class EvaluationConfigTypeDef(TypedDict):
    automated: NotRequired[AutomatedEvaluationConfigTypeDef]
    human: NotRequired[HumanEvaluationConfigTypeDef]

class KnowledgeBaseRetrieveAndGenerateConfigurationOutputTypeDef(TypedDict):
    knowledgeBaseId: str
    modelArn: str
    retrievalConfiguration: NotRequired[KnowledgeBaseRetrievalConfigurationOutputTypeDef]
    generationConfiguration: NotRequired[GenerationConfigurationOutputTypeDef]
    orchestrationConfiguration: NotRequired[OrchestrationConfigurationTypeDef]

class RetrieveConfigOutputTypeDef(TypedDict):
    knowledgeBaseId: str
    knowledgeBaseRetrievalConfiguration: KnowledgeBaseRetrievalConfigurationOutputTypeDef

class KnowledgeBaseRetrieveAndGenerateConfigurationTypeDef(TypedDict):
    knowledgeBaseId: str
    modelArn: str
    retrievalConfiguration: NotRequired[KnowledgeBaseRetrievalConfigurationTypeDef]
    generationConfiguration: NotRequired[GenerationConfigurationTypeDef]
    orchestrationConfiguration: NotRequired[OrchestrationConfigurationTypeDef]

class RetrieveConfigTypeDef(TypedDict):
    knowledgeBaseId: str
    knowledgeBaseRetrievalConfiguration: KnowledgeBaseRetrievalConfigurationTypeDef

EvaluationConfigUnionTypeDef = Union[EvaluationConfigTypeDef, EvaluationConfigOutputTypeDef]
RetrieveAndGenerateConfigurationOutputTypeDef = TypedDict(
    "RetrieveAndGenerateConfigurationOutputTypeDef",
    {
        "type": RetrieveAndGenerateTypeType,
        "knowledgeBaseConfiguration": NotRequired[
            KnowledgeBaseRetrieveAndGenerateConfigurationOutputTypeDef
        ],
        "externalSourcesConfiguration": NotRequired[
            ExternalSourcesRetrieveAndGenerateConfigurationOutputTypeDef
        ],
    },
)
RetrieveAndGenerateConfigurationTypeDef = TypedDict(
    "RetrieveAndGenerateConfigurationTypeDef",
    {
        "type": RetrieveAndGenerateTypeType,
        "knowledgeBaseConfiguration": NotRequired[
            KnowledgeBaseRetrieveAndGenerateConfigurationTypeDef
        ],
        "externalSourcesConfiguration": NotRequired[
            ExternalSourcesRetrieveAndGenerateConfigurationTypeDef
        ],
    },
)

class KnowledgeBaseConfigOutputTypeDef(TypedDict):
    retrieveConfig: NotRequired[RetrieveConfigOutputTypeDef]
    retrieveAndGenerateConfig: NotRequired[RetrieveAndGenerateConfigurationOutputTypeDef]

class KnowledgeBaseConfigTypeDef(TypedDict):
    retrieveConfig: NotRequired[RetrieveConfigTypeDef]
    retrieveAndGenerateConfig: NotRequired[RetrieveAndGenerateConfigurationTypeDef]

class RAGConfigOutputTypeDef(TypedDict):
    knowledgeBaseConfig: NotRequired[KnowledgeBaseConfigOutputTypeDef]
    precomputedRagSourceConfig: NotRequired[EvaluationPrecomputedRagSourceConfigTypeDef]

class RAGConfigTypeDef(TypedDict):
    knowledgeBaseConfig: NotRequired[KnowledgeBaseConfigTypeDef]
    precomputedRagSourceConfig: NotRequired[EvaluationPrecomputedRagSourceConfigTypeDef]

class EvaluationInferenceConfigOutputTypeDef(TypedDict):
    models: NotRequired[List[EvaluationModelConfigTypeDef]]
    ragConfigs: NotRequired[List[RAGConfigOutputTypeDef]]

class EvaluationInferenceConfigTypeDef(TypedDict):
    models: NotRequired[Sequence[EvaluationModelConfigTypeDef]]
    ragConfigs: NotRequired[Sequence[RAGConfigTypeDef]]

class GetEvaluationJobResponseTypeDef(TypedDict):
    jobName: str
    status: EvaluationJobStatusType
    jobArn: str
    jobDescription: str
    roleArn: str
    customerEncryptionKeyId: str
    jobType: EvaluationJobTypeType
    applicationType: ApplicationTypeType
    evaluationConfig: EvaluationConfigOutputTypeDef
    inferenceConfig: EvaluationInferenceConfigOutputTypeDef
    outputDataConfig: EvaluationOutputDataConfigTypeDef
    creationTime: datetime
    lastModifiedTime: datetime
    failureMessages: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

EvaluationInferenceConfigUnionTypeDef = Union[
    EvaluationInferenceConfigTypeDef, EvaluationInferenceConfigOutputTypeDef
]

class CreateEvaluationJobRequestTypeDef(TypedDict):
    jobName: str
    roleArn: str
    evaluationConfig: EvaluationConfigUnionTypeDef
    inferenceConfig: EvaluationInferenceConfigUnionTypeDef
    outputDataConfig: EvaluationOutputDataConfigTypeDef
    jobDescription: NotRequired[str]
    clientRequestToken: NotRequired[str]
    customerEncryptionKeyId: NotRequired[str]
    jobTags: NotRequired[Sequence[TagTypeDef]]
    applicationType: NotRequired[ApplicationTypeType]
