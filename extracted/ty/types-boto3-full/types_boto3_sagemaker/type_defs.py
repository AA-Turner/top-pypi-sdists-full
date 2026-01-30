"""
Type annotations for sagemaker service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_sagemaker.type_defs import AcceleratorPartitionConfigTypeDef

    data: AcceleratorPartitionConfigTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Union

from .literals import (
    AccountDefaultStatusType,
    ActionStatusType,
    ActivationStateType,
    AdditionalS3DataSourceDataTypeType,
    AggregationTransformationValueType,
    AlgorithmSortByType,
    AlgorithmStatusType,
    AppImageConfigSortKeyType,
    AppInstanceTypeType,
    AppNetworkAccessTypeType,
    AppSecurityGroupManagementType,
    AppStatusType,
    AppTypeType,
    ArtifactSourceIdTypeType,
    AssemblyTypeType,
    AssociationEdgeTypeType,
    AsyncNotificationTopicTypesType,
    AthenaResultCompressionTypeType,
    AthenaResultFormatType,
    AuthModeType,
    AutoMLAlgorithmType,
    AutoMLChannelTypeType,
    AutoMLJobObjectiveTypeType,
    AutoMLJobSecondaryStatusType,
    AutoMLJobStatusType,
    AutoMLMetricEnumType,
    AutoMLMetricExtendedEnumType,
    AutoMLModeType,
    AutoMLProblemTypeConfigNameType,
    AutoMLProcessingUnitType,
    AutoMLS3DataTypeType,
    AutoMLSortByType,
    AutoMLSortOrderType,
    AutoMountHomeEFSType,
    AwsManagedHumanLoopRequestSourceType,
    BatchAddClusterNodesErrorCodeType,
    BatchDeleteClusterNodesErrorCodeType,
    BatchRebootClusterNodesErrorCodeType,
    BatchReplaceClusterNodesErrorCodeType,
    BatchStrategyType,
    BooleanOperatorType,
    CandidateSortByType,
    CandidateStatusType,
    CandidateStepTypeType,
    CapacityReservationTypeType,
    CapacitySizeTypeType,
    CaptureModeType,
    CaptureStatusType,
    ClarifyFeatureTypeType,
    ClarifyTextGranularityType,
    ClarifyTextLanguageType,
    ClusterAutoScalingModeType,
    ClusterAutoScalingStatusType,
    ClusterCapacityTypeType,
    ClusterConfigModeType,
    ClusterEventResourceTypeType,
    ClusterInstanceStatusType,
    ClusterInstanceTypeType,
    ClusterKubernetesTaintEffectType,
    ClusterNodeRecoveryType,
    ClusterSortByType,
    ClusterStatusType,
    CodeRepositorySortByType,
    CodeRepositorySortOrderType,
    CollectionTypeType,
    CompilationJobStatusType,
    CompleteOnConvergenceType,
    CompressionTypeType,
    ConditionOutcomeType,
    ContainerModeType,
    ContentClassifierType,
    CrossAccountFilterOptionType,
    CustomizationTechniqueType,
    DataDistributionTypeType,
    DataSourceNameType,
    DeepHealthCheckTypeType,
    DetailedAlgorithmStatusType,
    DetailedModelPackageStatusType,
    DeviceDeploymentStatusType,
    DeviceSubsetTypeType,
    DirectInternetAccessType,
    DirectionType,
    DomainStatusType,
    EdgePackagingJobStatusType,
    EdgePresetDeploymentStatusType,
    EnabledOrDisabledType,
    EndpointConfigSortKeyType,
    EndpointSortKeyType,
    EndpointStatusType,
    EvaluationTypeType,
    ExecutionRoleIdentityConfigType,
    ExecutionStatusType,
    FailureHandlingPolicyType,
    FairShareType,
    FeatureGroupSortByType,
    FeatureGroupSortOrderType,
    FeatureGroupStatusType,
    FeatureStatusType,
    FeatureTypeType,
    FileSystemAccessModeType,
    FileSystemTypeType,
    FillingTypeType,
    FlatInvocationsType,
    FlowDefinitionStatusType,
    FrameworkType,
    HubContentSortByType,
    HubContentStatusType,
    HubContentSupportStatusType,
    HubContentTypeType,
    HubSortByType,
    HubStatusType,
    HumanTaskUiStatusType,
    HyperParameterScalingTypeType,
    HyperParameterTuningJobObjectiveTypeType,
    HyperParameterTuningJobSortByOptionsType,
    HyperParameterTuningJobStatusType,
    HyperParameterTuningJobStrategyTypeType,
    HyperParameterTuningJobWarmStartTypeType,
    IdleResourceSharingType,
    ImageSortByType,
    ImageSortOrderType,
    ImageStatusType,
    ImageVersionSortByType,
    ImageVersionSortOrderType,
    ImageVersionStatusType,
    InferenceComponentCapacitySizeTypeType,
    InferenceComponentSortKeyType,
    InferenceComponentStatusType,
    InferenceExecutionModeType,
    InferenceExperimentStatusType,
    InferenceExperimentStopDesiredStateType,
    InputModeType,
    InstanceGroupStatusType,
    InstanceTypeType,
    IPAddressTypeType,
    IsTrackingServerActiveType,
    JobTypeType,
    JoinSourceType,
    LabelingJobStatusType,
    LastUpdateStatusValueType,
    LifecycleManagementType,
    LineageTypeType,
    ListCompilationJobsSortByType,
    ListDeviceFleetsSortByType,
    ListEdgeDeploymentPlansSortByType,
    ListEdgePackagingJobsSortByType,
    ListInferenceRecommendationsJobsSortByType,
    ListOptimizationJobsSortByType,
    ListWorkforcesSortByOptionsType,
    ListWorkteamsSortByOptionsType,
    MaintenanceStatusType,
    ManagedInstanceScalingStatusType,
    MetricSetSourceType,
    MIGProfileTypeType,
    MlflowAppStatusType,
    MlToolsType,
    ModelApprovalStatusType,
    ModelCacheSettingType,
    ModelCardExportJobSortByType,
    ModelCardExportJobSortOrderType,
    ModelCardExportJobStatusType,
    ModelCardProcessingStatusType,
    ModelCardSortByType,
    ModelCardSortOrderType,
    ModelCardStatusType,
    ModelCompressionTypeType,
    ModelMetadataFilterTypeType,
    ModelPackageGroupSortByType,
    ModelPackageGroupStatusType,
    ModelPackageRegistrationTypeType,
    ModelPackageSortByType,
    ModelPackageStatusType,
    ModelPackageTypeType,
    ModelRegistrationModeType,
    ModelSortKeyType,
    ModelSpeculativeDecodingS3DataTypeType,
    ModelVariantActionType,
    ModelVariantStatusType,
    MonitoringAlertHistorySortKeyType,
    MonitoringAlertStatusType,
    MonitoringExecutionSortKeyType,
    MonitoringJobDefinitionSortKeyType,
    MonitoringProblemTypeType,
    MonitoringScheduleSortKeyType,
    MonitoringTypeType,
    NodeUnavailabilityTypeType,
    NotebookInstanceAcceleratorTypeType,
    NotebookInstanceLifecycleConfigSortKeyType,
    NotebookInstanceLifecycleConfigSortOrderType,
    NotebookInstanceSortKeyType,
    NotebookInstanceSortOrderType,
    NotebookInstanceStatusType,
    NotebookOutputOptionType,
    ObjectiveStatusType,
    OfflineStoreStatusValueType,
    OperatorType,
    OptimizationJobDeploymentInstanceTypeType,
    OptimizationJobStatusType,
    OrderKeyType,
    OutputCompressionTypeType,
    ParameterTypeType,
    PartnerAppStatusType,
    PartnerAppTypeType,
    PipelineExecutionStatusType,
    PipelineStatusType,
    PreemptTeamTasksType,
    ProblemTypeType,
    ProcessingInstanceTypeType,
    ProcessingJobStatusType,
    ProcessingS3CompressionTypeType,
    ProcessingS3DataDistributionTypeType,
    ProcessingS3DataTypeType,
    ProcessingS3InputModeType,
    ProcessingS3UploadModeType,
    ProcessorType,
    ProductionVariantAcceleratorTypeType,
    ProductionVariantInferenceAmiVersionType,
    ProductionVariantInstanceTypeType,
    ProfilingStatusType,
    ProjectSortByType,
    ProjectSortOrderType,
    ProjectStatusType,
    RecommendationJobStatusType,
    RecommendationJobSupportedEndpointTypeType,
    RecommendationJobTypeType,
    RecommendationStatusType,
    RecordWrapperType,
    RedshiftResultCompressionTypeType,
    RedshiftResultFormatType,
    RelationType,
    RepositoryAccessModeType,
    ReservedCapacityInstanceTypeType,
    ReservedCapacityStatusType,
    ReservedCapacityTypeType,
    ResourceCatalogSortOrderType,
    ResourceSharingStrategyType,
    ResourceTypeType,
    RetentionTypeType,
    RootAccessType,
    RoutingStrategyType,
    RStudioServerProAccessStatusType,
    RStudioServerProUserGroupType,
    RuleEvaluationStatusType,
    S3DataDistributionType,
    S3DataTypeType,
    S3ModelDataTypeType,
    SageMakerResourceNameType,
    SagemakerServicecatalogStatusType,
    SchedulerConfigComponentType,
    SchedulerResourceStatusType,
    ScheduleStatusType,
    SearchSortOrderType,
    SecondaryStatusType,
    ServerlessJobTypeType,
    SharingTypeType,
    SkipModelValidationType,
    SoftwareUpdateStatusType,
    SortActionsByType,
    SortAssociationsByType,
    SortByType,
    SortClusterSchedulerConfigByType,
    SortContextsByType,
    SortExperimentsByType,
    SortInferenceExperimentsByType,
    SortLineageGroupsByType,
    SortMlflowAppByType,
    SortOrderType,
    SortPipelineExecutionsByType,
    SortPipelinesByType,
    SortQuotaByType,
    SortTrackingServerByType,
    SortTrialComponentsByType,
    SortTrialsByType,
    SpaceSortKeyType,
    SpaceStatusType,
    SplitTypeType,
    StageStatusType,
    StatisticType,
    StepStatusType,
    StorageTypeType,
    StudioLifecycleConfigAppTypeType,
    StudioLifecycleConfigSortKeyType,
    StudioWebPortalType,
    TableFormatType,
    TagPropagationType,
    TargetDeviceType,
    TargetPlatformAcceleratorType,
    TargetPlatformArchType,
    TargetPlatformOsType,
    ThroughputModeType,
    TrackingServerMaintenanceStatusType,
    TrackingServerSizeType,
    TrackingServerStatusType,
    TrafficRoutingConfigTypeType,
    TrafficTypeType,
    TrainingInputModeType,
    TrainingInstanceTypeType,
    TrainingJobEarlyStoppingTypeType,
    TrainingJobSortByOptionsType,
    TrainingJobStatusType,
    TrainingPlanSortByType,
    TrainingPlanSortOrderType,
    TrainingPlanStatusType,
    TrainingRepositoryAccessModeType,
    TransformInstanceTypeType,
    TransformJobStatusType,
    TrialComponentPrimaryStatusType,
    TtlDurationUnitType,
    UltraServerHealthStatusType,
    UserProfileSortKeyType,
    UserProfileStatusType,
    VariantPropertyTypeType,
    VariantStatusType,
    VendorGuidanceType,
    VolumeAttachmentStatusType,
    WarmPoolResourceStatusType,
    WorkforceIpAddressTypeType,
    WorkforceStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AcceleratorPartitionConfigTypeDef",
    "ActionSourceTypeDef",
    "ActionSummaryTypeDef",
    "AddAssociationRequestTypeDef",
    "AddAssociationResponseTypeDef",
    "AddClusterNodeSpecificationTypeDef",
    "AddTagsInputTypeDef",
    "AddTagsOutputTypeDef",
    "AdditionalEnisTypeDef",
    "AdditionalInferenceSpecificationDefinitionOutputTypeDef",
    "AdditionalInferenceSpecificationDefinitionTypeDef",
    "AdditionalInferenceSpecificationDefinitionUnionTypeDef",
    "AdditionalModelDataSourceTypeDef",
    "AdditionalS3DataSourceTypeDef",
    "AgentVersionTypeDef",
    "AlarmDetailsTypeDef",
    "AlarmTypeDef",
    "AlgorithmSpecificationOutputTypeDef",
    "AlgorithmSpecificationTypeDef",
    "AlgorithmSpecificationUnionTypeDef",
    "AlgorithmStatusDetailsTypeDef",
    "AlgorithmStatusItemTypeDef",
    "AlgorithmSummaryTypeDef",
    "AlgorithmValidationProfileOutputTypeDef",
    "AlgorithmValidationProfileTypeDef",
    "AlgorithmValidationSpecificationOutputTypeDef",
    "AlgorithmValidationSpecificationTypeDef",
    "AlgorithmValidationSpecificationUnionTypeDef",
    "AmazonQSettingsTypeDef",
    "AnnotationConsolidationConfigTypeDef",
    "AppDetailsTypeDef",
    "AppImageConfigDetailsTypeDef",
    "AppLifecycleManagementTypeDef",
    "AppSpecificationOutputTypeDef",
    "AppSpecificationTypeDef",
    "AppSpecificationUnionTypeDef",
    "ArtifactSourceOutputTypeDef",
    "ArtifactSourceTypeDef",
    "ArtifactSourceTypeTypeDef",
    "ArtifactSourceUnionTypeDef",
    "ArtifactSummaryTypeDef",
    "AssociateTrialComponentRequestTypeDef",
    "AssociateTrialComponentResponseTypeDef",
    "AssociationInfoTypeDef",
    "AssociationSummaryTypeDef",
    "AsyncInferenceClientConfigTypeDef",
    "AsyncInferenceConfigOutputTypeDef",
    "AsyncInferenceConfigTypeDef",
    "AsyncInferenceConfigUnionTypeDef",
    "AsyncInferenceNotificationConfigOutputTypeDef",
    "AsyncInferenceNotificationConfigTypeDef",
    "AsyncInferenceOutputConfigOutputTypeDef",
    "AsyncInferenceOutputConfigTypeDef",
    "AthenaDatasetDefinitionTypeDef",
    "AttachClusterNodeVolumeRequestTypeDef",
    "AttachClusterNodeVolumeResponseTypeDef",
    "AuthorizedUrlTypeDef",
    "AutoMLAlgorithmConfigOutputTypeDef",
    "AutoMLAlgorithmConfigTypeDef",
    "AutoMLCandidateGenerationConfigOutputTypeDef",
    "AutoMLCandidateGenerationConfigTypeDef",
    "AutoMLCandidateStepTypeDef",
    "AutoMLCandidateTypeDef",
    "AutoMLChannelTypeDef",
    "AutoMLComputeConfigTypeDef",
    "AutoMLContainerDefinitionTypeDef",
    "AutoMLDataSourceTypeDef",
    "AutoMLDataSplitConfigTypeDef",
    "AutoMLJobArtifactsTypeDef",
    "AutoMLJobChannelTypeDef",
    "AutoMLJobCompletionCriteriaTypeDef",
    "AutoMLJobConfigOutputTypeDef",
    "AutoMLJobConfigTypeDef",
    "AutoMLJobConfigUnionTypeDef",
    "AutoMLJobObjectiveTypeDef",
    "AutoMLJobStepMetadataTypeDef",
    "AutoMLJobSummaryTypeDef",
    "AutoMLOutputDataConfigTypeDef",
    "AutoMLPartialFailureReasonTypeDef",
    "AutoMLProblemTypeConfigOutputTypeDef",
    "AutoMLProblemTypeConfigTypeDef",
    "AutoMLProblemTypeConfigUnionTypeDef",
    "AutoMLProblemTypeResolvedAttributesTypeDef",
    "AutoMLResolvedAttributesTypeDef",
    "AutoMLS3DataSourceTypeDef",
    "AutoMLSecurityConfigOutputTypeDef",
    "AutoMLSecurityConfigTypeDef",
    "AutoMLSecurityConfigUnionTypeDef",
    "AutoParameterTypeDef",
    "AutoRollbackConfigOutputTypeDef",
    "AutoRollbackConfigTypeDef",
    "AutotuneTypeDef",
    "AvailableUpgradeTypeDef",
    "BaseModelTypeDef",
    "BatchAddClusterNodesErrorTypeDef",
    "BatchAddClusterNodesRequestTypeDef",
    "BatchAddClusterNodesResponseTypeDef",
    "BatchDataCaptureConfigTypeDef",
    "BatchDeleteClusterNodeLogicalIdsErrorTypeDef",
    "BatchDeleteClusterNodesErrorTypeDef",
    "BatchDeleteClusterNodesRequestTypeDef",
    "BatchDeleteClusterNodesResponseTypeDef",
    "BatchDescribeModelPackageErrorTypeDef",
    "BatchDescribeModelPackageInputTypeDef",
    "BatchDescribeModelPackageOutputTypeDef",
    "BatchDescribeModelPackageSummaryTypeDef",
    "BatchRebootClusterNodeLogicalIdsErrorTypeDef",
    "BatchRebootClusterNodesErrorTypeDef",
    "BatchRebootClusterNodesRequestTypeDef",
    "BatchRebootClusterNodesResponseTypeDef",
    "BatchReplaceClusterNodeLogicalIdsErrorTypeDef",
    "BatchReplaceClusterNodesErrorTypeDef",
    "BatchReplaceClusterNodesRequestTypeDef",
    "BatchReplaceClusterNodesResponseTypeDef",
    "BatchTransformInputOutputTypeDef",
    "BatchTransformInputTypeDef",
    "BedrockCustomModelDeploymentMetadataTypeDef",
    "BedrockCustomModelMetadataTypeDef",
    "BedrockModelImportMetadataTypeDef",
    "BedrockProvisionedModelThroughputMetadataTypeDef",
    "BestObjectiveNotImprovingTypeDef",
    "BiasTypeDef",
    "BlueGreenUpdatePolicyTypeDef",
    "CacheHitResultTypeDef",
    "CallbackStepMetadataTypeDef",
    "CandidateArtifactLocationsTypeDef",
    "CandidateGenerationConfigOutputTypeDef",
    "CandidateGenerationConfigTypeDef",
    "CandidatePropertiesTypeDef",
    "CanvasAppSettingsOutputTypeDef",
    "CanvasAppSettingsTypeDef",
    "CapacityReservationTypeDef",
    "CapacitySizeConfigTypeDef",
    "CapacitySizeTypeDef",
    "CaptureContentTypeHeaderOutputTypeDef",
    "CaptureContentTypeHeaderTypeDef",
    "CaptureOptionTypeDef",
    "CategoricalParameterOutputTypeDef",
    "CategoricalParameterRangeOutputTypeDef",
    "CategoricalParameterRangeSpecificationOutputTypeDef",
    "CategoricalParameterRangeSpecificationTypeDef",
    "CategoricalParameterRangeTypeDef",
    "CategoricalParameterRangeUnionTypeDef",
    "CategoricalParameterTypeDef",
    "CfnCreateTemplateProviderTypeDef",
    "CfnStackCreateParameterTypeDef",
    "CfnStackDetailTypeDef",
    "CfnStackParameterTypeDef",
    "CfnStackUpdateParameterTypeDef",
    "CfnTemplateProviderDetailTypeDef",
    "CfnUpdateTemplateProviderTypeDef",
    "ChannelOutputTypeDef",
    "ChannelSpecificationOutputTypeDef",
    "ChannelSpecificationTypeDef",
    "ChannelTypeDef",
    "ChannelUnionTypeDef",
    "CheckpointConfigTypeDef",
    "ClarifyCheckStepMetadataTypeDef",
    "ClarifyExplainerConfigOutputTypeDef",
    "ClarifyExplainerConfigTypeDef",
    "ClarifyInferenceConfigOutputTypeDef",
    "ClarifyInferenceConfigTypeDef",
    "ClarifyShapBaselineConfigTypeDef",
    "ClarifyShapConfigTypeDef",
    "ClarifyTextConfigTypeDef",
    "ClusterAutoScalingConfigOutputTypeDef",
    "ClusterAutoScalingConfigTypeDef",
    "ClusterCapacityRequirementsOutputTypeDef",
    "ClusterCapacityRequirementsTypeDef",
    "ClusterCapacityRequirementsUnionTypeDef",
    "ClusterEbsVolumeConfigTypeDef",
    "ClusterEventDetailTypeDef",
    "ClusterEventSummaryTypeDef",
    "ClusterInstanceGroupDetailsTypeDef",
    "ClusterInstanceGroupSpecificationTypeDef",
    "ClusterInstancePlacementTypeDef",
    "ClusterInstanceStatusDetailsTypeDef",
    "ClusterInstanceStorageConfigTypeDef",
    "ClusterKubernetesConfigDetailsTypeDef",
    "ClusterKubernetesConfigNodeDetailsTypeDef",
    "ClusterKubernetesConfigTypeDef",
    "ClusterKubernetesTaintTypeDef",
    "ClusterLifeCycleConfigTypeDef",
    "ClusterMetadataTypeDef",
    "ClusterNodeDetailsTypeDef",
    "ClusterNodeSummaryTypeDef",
    "ClusterOrchestratorEksConfigTypeDef",
    "ClusterOrchestratorTypeDef",
    "ClusterRestrictedInstanceGroupDetailsTypeDef",
    "ClusterRestrictedInstanceGroupSpecificationTypeDef",
    "ClusterSchedulerConfigSummaryTypeDef",
    "ClusterSummaryTypeDef",
    "ClusterTieredStorageConfigTypeDef",
    "CodeEditorAppImageConfigOutputTypeDef",
    "CodeEditorAppImageConfigTypeDef",
    "CodeEditorAppImageConfigUnionTypeDef",
    "CodeEditorAppSettingsOutputTypeDef",
    "CodeEditorAppSettingsTypeDef",
    "CodeRepositorySummaryTypeDef",
    "CodeRepositoryTypeDef",
    "CognitoConfigTypeDef",
    "CognitoMemberDefinitionTypeDef",
    "CollectionConfigTypeDef",
    "CollectionConfigurationOutputTypeDef",
    "CollectionConfigurationTypeDef",
    "CompilationJobSummaryTypeDef",
    "ComputeQuotaConfigOutputTypeDef",
    "ComputeQuotaConfigTypeDef",
    "ComputeQuotaConfigUnionTypeDef",
    "ComputeQuotaResourceConfigTypeDef",
    "ComputeQuotaSummaryTypeDef",
    "ComputeQuotaTargetTypeDef",
    "ConditionStepMetadataTypeDef",
    "ContainerConfigOutputTypeDef",
    "ContainerConfigTypeDef",
    "ContainerDefinitionOutputTypeDef",
    "ContainerDefinitionTypeDef",
    "ContainerDefinitionUnionTypeDef",
    "ContextSourceTypeDef",
    "ContextSummaryTypeDef",
    "ContinuousParameterRangeSpecificationTypeDef",
    "ContinuousParameterRangeTypeDef",
    "ConvergenceDetectedTypeDef",
    "CreateActionRequestTypeDef",
    "CreateActionResponseTypeDef",
    "CreateAlgorithmInputTypeDef",
    "CreateAlgorithmOutputTypeDef",
    "CreateAppImageConfigRequestTypeDef",
    "CreateAppImageConfigResponseTypeDef",
    "CreateAppRequestTypeDef",
    "CreateAppResponseTypeDef",
    "CreateArtifactRequestTypeDef",
    "CreateArtifactResponseTypeDef",
    "CreateAutoMLJobRequestTypeDef",
    "CreateAutoMLJobResponseTypeDef",
    "CreateAutoMLJobV2RequestTypeDef",
    "CreateAutoMLJobV2ResponseTypeDef",
    "CreateClusterRequestTypeDef",
    "CreateClusterResponseTypeDef",
    "CreateClusterSchedulerConfigRequestTypeDef",
    "CreateClusterSchedulerConfigResponseTypeDef",
    "CreateCodeRepositoryInputTypeDef",
    "CreateCodeRepositoryOutputTypeDef",
    "CreateCompilationJobRequestTypeDef",
    "CreateCompilationJobResponseTypeDef",
    "CreateComputeQuotaRequestTypeDef",
    "CreateComputeQuotaResponseTypeDef",
    "CreateContextRequestTypeDef",
    "CreateContextResponseTypeDef",
    "CreateDataQualityJobDefinitionRequestTypeDef",
    "CreateDataQualityJobDefinitionResponseTypeDef",
    "CreateDeviceFleetRequestTypeDef",
    "CreateDomainRequestTypeDef",
    "CreateDomainResponseTypeDef",
    "CreateEdgeDeploymentPlanRequestTypeDef",
    "CreateEdgeDeploymentPlanResponseTypeDef",
    "CreateEdgeDeploymentStageRequestTypeDef",
    "CreateEdgePackagingJobRequestTypeDef",
    "CreateEndpointConfigInputTypeDef",
    "CreateEndpointConfigOutputTypeDef",
    "CreateEndpointInputTypeDef",
    "CreateEndpointOutputTypeDef",
    "CreateExperimentRequestTypeDef",
    "CreateExperimentResponseTypeDef",
    "CreateFeatureGroupRequestTypeDef",
    "CreateFeatureGroupResponseTypeDef",
    "CreateFlowDefinitionRequestTypeDef",
    "CreateFlowDefinitionResponseTypeDef",
    "CreateHubContentPresignedUrlsRequestPaginateTypeDef",
    "CreateHubContentPresignedUrlsRequestTypeDef",
    "CreateHubContentPresignedUrlsResponseTypeDef",
    "CreateHubContentReferenceRequestTypeDef",
    "CreateHubContentReferenceResponseTypeDef",
    "CreateHubRequestTypeDef",
    "CreateHubResponseTypeDef",
    "CreateHumanTaskUiRequestTypeDef",
    "CreateHumanTaskUiResponseTypeDef",
    "CreateHyperParameterTuningJobRequestTypeDef",
    "CreateHyperParameterTuningJobResponseTypeDef",
    "CreateImageRequestTypeDef",
    "CreateImageResponseTypeDef",
    "CreateImageVersionRequestTypeDef",
    "CreateImageVersionResponseTypeDef",
    "CreateInferenceComponentInputTypeDef",
    "CreateInferenceComponentOutputTypeDef",
    "CreateInferenceExperimentRequestTypeDef",
    "CreateInferenceExperimentResponseTypeDef",
    "CreateInferenceRecommendationsJobRequestTypeDef",
    "CreateInferenceRecommendationsJobResponseTypeDef",
    "CreateLabelingJobRequestTypeDef",
    "CreateLabelingJobResponseTypeDef",
    "CreateMlflowAppRequestTypeDef",
    "CreateMlflowAppResponseTypeDef",
    "CreateMlflowTrackingServerRequestTypeDef",
    "CreateMlflowTrackingServerResponseTypeDef",
    "CreateModelBiasJobDefinitionRequestTypeDef",
    "CreateModelBiasJobDefinitionResponseTypeDef",
    "CreateModelCardExportJobRequestTypeDef",
    "CreateModelCardExportJobResponseTypeDef",
    "CreateModelCardRequestTypeDef",
    "CreateModelCardResponseTypeDef",
    "CreateModelExplainabilityJobDefinitionRequestTypeDef",
    "CreateModelExplainabilityJobDefinitionResponseTypeDef",
    "CreateModelInputTypeDef",
    "CreateModelOutputTypeDef",
    "CreateModelPackageGroupInputTypeDef",
    "CreateModelPackageGroupOutputTypeDef",
    "CreateModelPackageInputTypeDef",
    "CreateModelPackageOutputTypeDef",
    "CreateModelQualityJobDefinitionRequestTypeDef",
    "CreateModelQualityJobDefinitionResponseTypeDef",
    "CreateMonitoringScheduleRequestTypeDef",
    "CreateMonitoringScheduleResponseTypeDef",
    "CreateNotebookInstanceInputTypeDef",
    "CreateNotebookInstanceLifecycleConfigInputTypeDef",
    "CreateNotebookInstanceLifecycleConfigOutputTypeDef",
    "CreateNotebookInstanceOutputTypeDef",
    "CreateOptimizationJobRequestTypeDef",
    "CreateOptimizationJobResponseTypeDef",
    "CreatePartnerAppPresignedUrlRequestTypeDef",
    "CreatePartnerAppPresignedUrlResponseTypeDef",
    "CreatePartnerAppRequestTypeDef",
    "CreatePartnerAppResponseTypeDef",
    "CreatePipelineRequestTypeDef",
    "CreatePipelineResponseTypeDef",
    "CreatePresignedDomainUrlRequestTypeDef",
    "CreatePresignedDomainUrlResponseTypeDef",
    "CreatePresignedMlflowAppUrlRequestTypeDef",
    "CreatePresignedMlflowAppUrlResponseTypeDef",
    "CreatePresignedMlflowTrackingServerUrlRequestTypeDef",
    "CreatePresignedMlflowTrackingServerUrlResponseTypeDef",
    "CreatePresignedNotebookInstanceUrlInputTypeDef",
    "CreatePresignedNotebookInstanceUrlOutputTypeDef",
    "CreateProcessingJobRequestTypeDef",
    "CreateProcessingJobResponseTypeDef",
    "CreateProjectInputTypeDef",
    "CreateProjectOutputTypeDef",
    "CreateSpaceRequestTypeDef",
    "CreateSpaceResponseTypeDef",
    "CreateStudioLifecycleConfigRequestTypeDef",
    "CreateStudioLifecycleConfigResponseTypeDef",
    "CreateTemplateProviderTypeDef",
    "CreateTrainingJobRequestTypeDef",
    "CreateTrainingJobResponseTypeDef",
    "CreateTrainingPlanRequestTypeDef",
    "CreateTrainingPlanResponseTypeDef",
    "CreateTransformJobRequestTypeDef",
    "CreateTransformJobResponseTypeDef",
    "CreateTrialComponentRequestTypeDef",
    "CreateTrialComponentResponseTypeDef",
    "CreateTrialRequestTypeDef",
    "CreateTrialResponseTypeDef",
    "CreateUserProfileRequestTypeDef",
    "CreateUserProfileResponseTypeDef",
    "CreateWorkforceRequestTypeDef",
    "CreateWorkforceResponseTypeDef",
    "CreateWorkteamRequestTypeDef",
    "CreateWorkteamResponseTypeDef",
    "CustomFileSystemConfigTypeDef",
    "CustomFileSystemTypeDef",
    "CustomImageTypeDef",
    "CustomPosixUserConfigTypeDef",
    "CustomizedMetricSpecificationTypeDef",
    "DataCaptureConfigOutputTypeDef",
    "DataCaptureConfigSummaryTypeDef",
    "DataCaptureConfigTypeDef",
    "DataCaptureConfigUnionTypeDef",
    "DataCatalogConfigTypeDef",
    "DataProcessingTypeDef",
    "DataQualityAppSpecificationOutputTypeDef",
    "DataQualityAppSpecificationTypeDef",
    "DataQualityAppSpecificationUnionTypeDef",
    "DataQualityBaselineConfigTypeDef",
    "DataQualityJobInputOutputTypeDef",
    "DataQualityJobInputTypeDef",
    "DataQualityJobInputUnionTypeDef",
    "DataSourceOutputTypeDef",
    "DataSourceTypeDef",
    "DataSourceUnionTypeDef",
    "DatasetDefinitionTypeDef",
    "DatasetSourceTypeDef",
    "DebugHookConfigOutputTypeDef",
    "DebugHookConfigTypeDef",
    "DebugHookConfigUnionTypeDef",
    "DebugRuleConfigurationOutputTypeDef",
    "DebugRuleConfigurationTypeDef",
    "DebugRuleConfigurationUnionTypeDef",
    "DebugRuleEvaluationStatusTypeDef",
    "DefaultEbsStorageSettingsTypeDef",
    "DefaultSpaceSettingsOutputTypeDef",
    "DefaultSpaceSettingsTypeDef",
    "DefaultSpaceSettingsUnionTypeDef",
    "DefaultSpaceStorageSettingsTypeDef",
    "DeleteActionRequestTypeDef",
    "DeleteActionResponseTypeDef",
    "DeleteAlgorithmInputTypeDef",
    "DeleteAppImageConfigRequestTypeDef",
    "DeleteAppRequestTypeDef",
    "DeleteArtifactRequestTypeDef",
    "DeleteArtifactResponseTypeDef",
    "DeleteAssociationRequestTypeDef",
    "DeleteAssociationResponseTypeDef",
    "DeleteClusterRequestTypeDef",
    "DeleteClusterResponseTypeDef",
    "DeleteClusterSchedulerConfigRequestTypeDef",
    "DeleteCodeRepositoryInputTypeDef",
    "DeleteCompilationJobRequestTypeDef",
    "DeleteComputeQuotaRequestTypeDef",
    "DeleteContextRequestTypeDef",
    "DeleteContextResponseTypeDef",
    "DeleteDataQualityJobDefinitionRequestTypeDef",
    "DeleteDeviceFleetRequestTypeDef",
    "DeleteDomainRequestTypeDef",
    "DeleteEdgeDeploymentPlanRequestTypeDef",
    "DeleteEdgeDeploymentStageRequestTypeDef",
    "DeleteEndpointConfigInputTypeDef",
    "DeleteEndpointInputTypeDef",
    "DeleteExperimentRequestTypeDef",
    "DeleteExperimentResponseTypeDef",
    "DeleteFeatureGroupRequestTypeDef",
    "DeleteFlowDefinitionRequestTypeDef",
    "DeleteHubContentReferenceRequestTypeDef",
    "DeleteHubContentRequestTypeDef",
    "DeleteHubRequestTypeDef",
    "DeleteHumanTaskUiRequestTypeDef",
    "DeleteHyperParameterTuningJobRequestTypeDef",
    "DeleteImageRequestTypeDef",
    "DeleteImageVersionRequestTypeDef",
    "DeleteInferenceComponentInputTypeDef",
    "DeleteInferenceExperimentRequestTypeDef",
    "DeleteInferenceExperimentResponseTypeDef",
    "DeleteMlflowAppRequestTypeDef",
    "DeleteMlflowAppResponseTypeDef",
    "DeleteMlflowTrackingServerRequestTypeDef",
    "DeleteMlflowTrackingServerResponseTypeDef",
    "DeleteModelBiasJobDefinitionRequestTypeDef",
    "DeleteModelCardRequestTypeDef",
    "DeleteModelExplainabilityJobDefinitionRequestTypeDef",
    "DeleteModelInputTypeDef",
    "DeleteModelPackageGroupInputTypeDef",
    "DeleteModelPackageGroupPolicyInputTypeDef",
    "DeleteModelPackageInputTypeDef",
    "DeleteModelQualityJobDefinitionRequestTypeDef",
    "DeleteMonitoringScheduleRequestTypeDef",
    "DeleteNotebookInstanceInputTypeDef",
    "DeleteNotebookInstanceLifecycleConfigInputTypeDef",
    "DeleteOptimizationJobRequestTypeDef",
    "DeletePartnerAppRequestTypeDef",
    "DeletePartnerAppResponseTypeDef",
    "DeletePipelineRequestTypeDef",
    "DeletePipelineResponseTypeDef",
    "DeleteProcessingJobRequestTypeDef",
    "DeleteProjectInputTypeDef",
    "DeleteSpaceRequestTypeDef",
    "DeleteStudioLifecycleConfigRequestTypeDef",
    "DeleteTagsInputTypeDef",
    "DeleteTrainingJobRequestTypeDef",
    "DeleteTrialComponentRequestTypeDef",
    "DeleteTrialComponentResponseTypeDef",
    "DeleteTrialRequestTypeDef",
    "DeleteTrialResponseTypeDef",
    "DeleteUserProfileRequestTypeDef",
    "DeleteWorkforceRequestTypeDef",
    "DeleteWorkteamRequestTypeDef",
    "DeleteWorkteamResponseTypeDef",
    "DeployedImageTypeDef",
    "DeploymentConfigOutputTypeDef",
    "DeploymentConfigTypeDef",
    "DeploymentConfigUnionTypeDef",
    "DeploymentConfigurationOutputTypeDef",
    "DeploymentConfigurationTypeDef",
    "DeploymentConfigurationUnionTypeDef",
    "DeploymentRecommendationTypeDef",
    "DeploymentStageStatusSummaryTypeDef",
    "DeploymentStageTypeDef",
    "DeregisterDevicesRequestTypeDef",
    "DerivedInformationTypeDef",
    "DescribeActionRequestTypeDef",
    "DescribeActionResponseTypeDef",
    "DescribeAlgorithmInputTypeDef",
    "DescribeAlgorithmOutputTypeDef",
    "DescribeAppImageConfigRequestTypeDef",
    "DescribeAppImageConfigResponseTypeDef",
    "DescribeAppRequestTypeDef",
    "DescribeAppResponseTypeDef",
    "DescribeArtifactRequestTypeDef",
    "DescribeArtifactResponseTypeDef",
    "DescribeAutoMLJobRequestTypeDef",
    "DescribeAutoMLJobResponseTypeDef",
    "DescribeAutoMLJobV2RequestTypeDef",
    "DescribeAutoMLJobV2ResponseTypeDef",
    "DescribeClusterEventRequestTypeDef",
    "DescribeClusterEventResponseTypeDef",
    "DescribeClusterNodeRequestTypeDef",
    "DescribeClusterNodeResponseTypeDef",
    "DescribeClusterRequestTypeDef",
    "DescribeClusterResponseTypeDef",
    "DescribeClusterSchedulerConfigRequestTypeDef",
    "DescribeClusterSchedulerConfigResponseTypeDef",
    "DescribeCodeRepositoryInputTypeDef",
    "DescribeCodeRepositoryOutputTypeDef",
    "DescribeCompilationJobRequestTypeDef",
    "DescribeCompilationJobResponseTypeDef",
    "DescribeComputeQuotaRequestTypeDef",
    "DescribeComputeQuotaResponseTypeDef",
    "DescribeContextRequestTypeDef",
    "DescribeContextResponseTypeDef",
    "DescribeDataQualityJobDefinitionRequestTypeDef",
    "DescribeDataQualityJobDefinitionResponseTypeDef",
    "DescribeDeviceFleetRequestTypeDef",
    "DescribeDeviceFleetResponseTypeDef",
    "DescribeDeviceRequestTypeDef",
    "DescribeDeviceResponseTypeDef",
    "DescribeDomainRequestTypeDef",
    "DescribeDomainResponseTypeDef",
    "DescribeEdgeDeploymentPlanRequestTypeDef",
    "DescribeEdgeDeploymentPlanResponseTypeDef",
    "DescribeEdgePackagingJobRequestTypeDef",
    "DescribeEdgePackagingJobResponseTypeDef",
    "DescribeEndpointConfigInputTypeDef",
    "DescribeEndpointConfigOutputTypeDef",
    "DescribeEndpointInputTypeDef",
    "DescribeEndpointInputWaitExtraTypeDef",
    "DescribeEndpointInputWaitTypeDef",
    "DescribeEndpointOutputTypeDef",
    "DescribeExperimentRequestTypeDef",
    "DescribeExperimentResponseTypeDef",
    "DescribeFeatureGroupRequestTypeDef",
    "DescribeFeatureGroupResponseTypeDef",
    "DescribeFeatureMetadataRequestTypeDef",
    "DescribeFeatureMetadataResponseTypeDef",
    "DescribeFlowDefinitionRequestTypeDef",
    "DescribeFlowDefinitionResponseTypeDef",
    "DescribeHubContentRequestTypeDef",
    "DescribeHubContentResponseTypeDef",
    "DescribeHubRequestTypeDef",
    "DescribeHubResponseTypeDef",
    "DescribeHumanTaskUiRequestTypeDef",
    "DescribeHumanTaskUiResponseTypeDef",
    "DescribeHyperParameterTuningJobRequestTypeDef",
    "DescribeHyperParameterTuningJobResponseTypeDef",
    "DescribeImageRequestTypeDef",
    "DescribeImageRequestWaitExtraExtraTypeDef",
    "DescribeImageRequestWaitExtraTypeDef",
    "DescribeImageRequestWaitTypeDef",
    "DescribeImageResponseTypeDef",
    "DescribeImageVersionRequestTypeDef",
    "DescribeImageVersionRequestWaitExtraTypeDef",
    "DescribeImageVersionRequestWaitTypeDef",
    "DescribeImageVersionResponseTypeDef",
    "DescribeInferenceComponentInputTypeDef",
    "DescribeInferenceComponentOutputTypeDef",
    "DescribeInferenceExperimentRequestTypeDef",
    "DescribeInferenceExperimentResponseTypeDef",
    "DescribeInferenceRecommendationsJobRequestTypeDef",
    "DescribeInferenceRecommendationsJobResponseTypeDef",
    "DescribeLabelingJobRequestTypeDef",
    "DescribeLabelingJobResponseTypeDef",
    "DescribeLineageGroupRequestTypeDef",
    "DescribeLineageGroupResponseTypeDef",
    "DescribeMlflowAppRequestTypeDef",
    "DescribeMlflowAppResponseTypeDef",
    "DescribeMlflowTrackingServerRequestTypeDef",
    "DescribeMlflowTrackingServerResponseTypeDef",
    "DescribeModelBiasJobDefinitionRequestTypeDef",
    "DescribeModelBiasJobDefinitionResponseTypeDef",
    "DescribeModelCardExportJobRequestTypeDef",
    "DescribeModelCardExportJobResponseTypeDef",
    "DescribeModelCardRequestTypeDef",
    "DescribeModelCardResponseTypeDef",
    "DescribeModelExplainabilityJobDefinitionRequestTypeDef",
    "DescribeModelExplainabilityJobDefinitionResponseTypeDef",
    "DescribeModelInputTypeDef",
    "DescribeModelOutputTypeDef",
    "DescribeModelPackageGroupInputTypeDef",
    "DescribeModelPackageGroupOutputTypeDef",
    "DescribeModelPackageInputTypeDef",
    "DescribeModelPackageOutputTypeDef",
    "DescribeModelQualityJobDefinitionRequestTypeDef",
    "DescribeModelQualityJobDefinitionResponseTypeDef",
    "DescribeMonitoringScheduleRequestTypeDef",
    "DescribeMonitoringScheduleResponseTypeDef",
    "DescribeNotebookInstanceInputTypeDef",
    "DescribeNotebookInstanceInputWaitExtraExtraTypeDef",
    "DescribeNotebookInstanceInputWaitExtraTypeDef",
    "DescribeNotebookInstanceInputWaitTypeDef",
    "DescribeNotebookInstanceLifecycleConfigInputTypeDef",
    "DescribeNotebookInstanceLifecycleConfigOutputTypeDef",
    "DescribeNotebookInstanceOutputTypeDef",
    "DescribeOptimizationJobRequestTypeDef",
    "DescribeOptimizationJobResponseTypeDef",
    "DescribePartnerAppRequestTypeDef",
    "DescribePartnerAppResponseTypeDef",
    "DescribePipelineDefinitionForExecutionRequestTypeDef",
    "DescribePipelineDefinitionForExecutionResponseTypeDef",
    "DescribePipelineExecutionRequestTypeDef",
    "DescribePipelineExecutionResponseTypeDef",
    "DescribePipelineRequestTypeDef",
    "DescribePipelineResponseTypeDef",
    "DescribeProcessingJobRequestTypeDef",
    "DescribeProcessingJobRequestWaitTypeDef",
    "DescribeProcessingJobResponseTypeDef",
    "DescribeProjectInputTypeDef",
    "DescribeProjectOutputTypeDef",
    "DescribeReservedCapacityRequestTypeDef",
    "DescribeReservedCapacityResponseTypeDef",
    "DescribeSpaceRequestTypeDef",
    "DescribeSpaceResponseTypeDef",
    "DescribeStudioLifecycleConfigRequestTypeDef",
    "DescribeStudioLifecycleConfigResponseTypeDef",
    "DescribeSubscribedWorkteamRequestTypeDef",
    "DescribeSubscribedWorkteamResponseTypeDef",
    "DescribeTrainingJobRequestTypeDef",
    "DescribeTrainingJobRequestWaitTypeDef",
    "DescribeTrainingJobResponseTypeDef",
    "DescribeTrainingPlanRequestTypeDef",
    "DescribeTrainingPlanResponseTypeDef",
    "DescribeTransformJobRequestTypeDef",
    "DescribeTransformJobRequestWaitTypeDef",
    "DescribeTransformJobResponseTypeDef",
    "DescribeTrialComponentRequestTypeDef",
    "DescribeTrialComponentResponseTypeDef",
    "DescribeTrialRequestTypeDef",
    "DescribeTrialResponseTypeDef",
    "DescribeUserProfileRequestTypeDef",
    "DescribeUserProfileResponseTypeDef",
    "DescribeWorkforceRequestTypeDef",
    "DescribeWorkforceResponseTypeDef",
    "DescribeWorkteamRequestTypeDef",
    "DescribeWorkteamResponseTypeDef",
    "DesiredWeightAndCapacityTypeDef",
    "DetachClusterNodeVolumeRequestTypeDef",
    "DetachClusterNodeVolumeResponseTypeDef",
    "DeviceDeploymentSummaryTypeDef",
    "DeviceFleetSummaryTypeDef",
    "DeviceSelectionConfigOutputTypeDef",
    "DeviceSelectionConfigTypeDef",
    "DeviceSelectionConfigUnionTypeDef",
    "DeviceStatsTypeDef",
    "DeviceSummaryTypeDef",
    "DeviceTypeDef",
    "DirectDeploySettingsTypeDef",
    "DisassociateTrialComponentRequestTypeDef",
    "DisassociateTrialComponentResponseTypeDef",
    "DockerSettingsOutputTypeDef",
    "DockerSettingsTypeDef",
    "DockerSettingsUnionTypeDef",
    "DomainDetailsTypeDef",
    "DomainSettingsForUpdateTypeDef",
    "DomainSettingsOutputTypeDef",
    "DomainSettingsTypeDef",
    "DomainSettingsUnionTypeDef",
    "DriftCheckBaselinesTypeDef",
    "DriftCheckBiasTypeDef",
    "DriftCheckExplainabilityTypeDef",
    "DriftCheckModelDataQualityTypeDef",
    "DriftCheckModelQualityTypeDef",
    "DynamicScalingConfigurationTypeDef",
    "EFSFileSystemConfigTypeDef",
    "EFSFileSystemTypeDef",
    "EMRStepMetadataTypeDef",
    "EbsStorageSettingsTypeDef",
    "Ec2CapacityReservationTypeDef",
    "EdgeDeploymentConfigTypeDef",
    "EdgeDeploymentModelConfigTypeDef",
    "EdgeDeploymentPlanSummaryTypeDef",
    "EdgeDeploymentStatusTypeDef",
    "EdgeModelStatTypeDef",
    "EdgeModelSummaryTypeDef",
    "EdgeModelTypeDef",
    "EdgeOutputConfigTypeDef",
    "EdgePackagingJobSummaryTypeDef",
    "EdgePresetDeploymentOutputTypeDef",
    "EdgeTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EmrServerlessComputeConfigTypeDef",
    "EmrServerlessSettingsTypeDef",
    "EmrSettingsOutputTypeDef",
    "EmrSettingsTypeDef",
    "EndpointConfigStepMetadataTypeDef",
    "EndpointConfigSummaryTypeDef",
    "EndpointInfoTypeDef",
    "EndpointInputConfigurationOutputTypeDef",
    "EndpointInputConfigurationTypeDef",
    "EndpointInputTypeDef",
    "EndpointMetadataTypeDef",
    "EndpointOutputConfigurationTypeDef",
    "EndpointPerformanceTypeDef",
    "EndpointStepMetadataTypeDef",
    "EndpointSummaryTypeDef",
    "EndpointTypeDef",
    "EnvironmentConfigDetailsTypeDef",
    "EnvironmentConfigTypeDef",
    "EnvironmentParameterRangesOutputTypeDef",
    "EnvironmentParameterRangesTypeDef",
    "EnvironmentParameterTypeDef",
    "ErrorInfoTypeDef",
    "EventDetailsTypeDef",
    "EventMetadataTypeDef",
    "ExperimentConfigTypeDef",
    "ExperimentSourceTypeDef",
    "ExperimentSummaryTypeDef",
    "ExperimentTypeDef",
    "ExplainabilityTypeDef",
    "ExplainerConfigOutputTypeDef",
    "ExplainerConfigTypeDef",
    "ExplainerConfigUnionTypeDef",
    "FSxLustreConfigTypeDef",
    "FSxLustreFileSystemConfigTypeDef",
    "FSxLustreFileSystemTypeDef",
    "FailStepMetadataTypeDef",
    "FeatureDefinitionTypeDef",
    "FeatureGroupSummaryTypeDef",
    "FeatureGroupTypeDef",
    "FeatureMetadataTypeDef",
    "FeatureParameterTypeDef",
    "FileSourceTypeDef",
    "FileSystemConfigTypeDef",
    "FileSystemDataSourceTypeDef",
    "FilterTypeDef",
    "FinalAutoMLJobObjectiveMetricTypeDef",
    "FinalHyperParameterTuningJobObjectiveMetricTypeDef",
    "FlowDefinitionOutputConfigTypeDef",
    "FlowDefinitionSummaryTypeDef",
    "GenerativeAiSettingsTypeDef",
    "GetDeviceFleetReportRequestTypeDef",
    "GetDeviceFleetReportResponseTypeDef",
    "GetLineageGroupPolicyRequestTypeDef",
    "GetLineageGroupPolicyResponseTypeDef",
    "GetModelPackageGroupPolicyInputTypeDef",
    "GetModelPackageGroupPolicyOutputTypeDef",
    "GetSagemakerServicecatalogPortfolioStatusOutputTypeDef",
    "GetScalingConfigurationRecommendationRequestTypeDef",
    "GetScalingConfigurationRecommendationResponseTypeDef",
    "GetSearchSuggestionsRequestTypeDef",
    "GetSearchSuggestionsResponseTypeDef",
    "GitConfigForUpdateTypeDef",
    "GitConfigTypeDef",
    "HiddenSageMakerImageOutputTypeDef",
    "HiddenSageMakerImageTypeDef",
    "HolidayConfigAttributesTypeDef",
    "HubAccessConfigTypeDef",
    "HubContentDependencyTypeDef",
    "HubContentInfoTypeDef",
    "HubInfoTypeDef",
    "HubS3StorageConfigTypeDef",
    "HumanLoopActivationConditionsConfigTypeDef",
    "HumanLoopActivationConfigTypeDef",
    "HumanLoopConfigOutputTypeDef",
    "HumanLoopConfigTypeDef",
    "HumanLoopConfigUnionTypeDef",
    "HumanLoopRequestSourceTypeDef",
    "HumanTaskConfigOutputTypeDef",
    "HumanTaskConfigTypeDef",
    "HumanTaskConfigUnionTypeDef",
    "HumanTaskUiSummaryTypeDef",
    "HyperParameterAlgorithmSpecificationOutputTypeDef",
    "HyperParameterAlgorithmSpecificationTypeDef",
    "HyperParameterAlgorithmSpecificationUnionTypeDef",
    "HyperParameterSpecificationOutputTypeDef",
    "HyperParameterSpecificationTypeDef",
    "HyperParameterTrainingJobDefinitionOutputTypeDef",
    "HyperParameterTrainingJobDefinitionTypeDef",
    "HyperParameterTrainingJobDefinitionUnionTypeDef",
    "HyperParameterTrainingJobSummaryTypeDef",
    "HyperParameterTuningInstanceConfigTypeDef",
    "HyperParameterTuningJobCompletionDetailsTypeDef",
    "HyperParameterTuningJobConfigOutputTypeDef",
    "HyperParameterTuningJobConfigTypeDef",
    "HyperParameterTuningJobConfigUnionTypeDef",
    "HyperParameterTuningJobConsumedResourcesTypeDef",
    "HyperParameterTuningJobObjectiveTypeDef",
    "HyperParameterTuningJobSearchEntityTypeDef",
    "HyperParameterTuningJobStrategyConfigTypeDef",
    "HyperParameterTuningJobSummaryTypeDef",
    "HyperParameterTuningJobWarmStartConfigOutputTypeDef",
    "HyperParameterTuningJobWarmStartConfigTypeDef",
    "HyperParameterTuningJobWarmStartConfigUnionTypeDef",
    "HyperParameterTuningResourceConfigOutputTypeDef",
    "HyperParameterTuningResourceConfigTypeDef",
    "HyperParameterTuningResourceConfigUnionTypeDef",
    "HyperbandStrategyConfigTypeDef",
    "IamIdentityTypeDef",
    "IamPolicyConstraintsTypeDef",
    "IdentityProviderOAuthSettingTypeDef",
    "IdleSettingsTypeDef",
    "ImageClassificationJobConfigTypeDef",
    "ImageConfigTypeDef",
    "ImageTypeDef",
    "ImageVersionTypeDef",
    "ImportHubContentRequestTypeDef",
    "ImportHubContentResponseTypeDef",
    "InferenceComponentCapacitySizeTypeDef",
    "InferenceComponentComputeResourceRequirementsTypeDef",
    "InferenceComponentContainerSpecificationSummaryTypeDef",
    "InferenceComponentContainerSpecificationTypeDef",
    "InferenceComponentDataCacheConfigSummaryTypeDef",
    "InferenceComponentDataCacheConfigTypeDef",
    "InferenceComponentDeploymentConfigOutputTypeDef",
    "InferenceComponentDeploymentConfigTypeDef",
    "InferenceComponentDeploymentConfigUnionTypeDef",
    "InferenceComponentMetadataTypeDef",
    "InferenceComponentRollingUpdatePolicyTypeDef",
    "InferenceComponentRuntimeConfigSummaryTypeDef",
    "InferenceComponentRuntimeConfigTypeDef",
    "InferenceComponentSpecificationSummaryTypeDef",
    "InferenceComponentSpecificationTypeDef",
    "InferenceComponentStartupParametersTypeDef",
    "InferenceComponentSummaryTypeDef",
    "InferenceExecutionConfigTypeDef",
    "InferenceExperimentDataStorageConfigOutputTypeDef",
    "InferenceExperimentDataStorageConfigTypeDef",
    "InferenceExperimentDataStorageConfigUnionTypeDef",
    "InferenceExperimentScheduleOutputTypeDef",
    "InferenceExperimentScheduleTypeDef",
    "InferenceExperimentScheduleUnionTypeDef",
    "InferenceExperimentSummaryTypeDef",
    "InferenceHubAccessConfigTypeDef",
    "InferenceMetricsTypeDef",
    "InferenceRecommendationTypeDef",
    "InferenceRecommendationsJobStepTypeDef",
    "InferenceRecommendationsJobTypeDef",
    "InferenceSpecificationOutputTypeDef",
    "InferenceSpecificationTypeDef",
    "InferenceSpecificationUnionTypeDef",
    "InfraCheckConfigTypeDef",
    "InputConfigTypeDef",
    "InstanceGroupMetadataTypeDef",
    "InstanceGroupScalingMetadataTypeDef",
    "InstanceGroupTypeDef",
    "InstanceMetadataServiceConfigurationTypeDef",
    "InstanceMetadataTypeDef",
    "InstancePlacementConfigOutputTypeDef",
    "InstancePlacementConfigTypeDef",
    "InstancePlacementConfigUnionTypeDef",
    "IntegerParameterRangeSpecificationTypeDef",
    "IntegerParameterRangeTypeDef",
    "JupyterLabAppImageConfigOutputTypeDef",
    "JupyterLabAppImageConfigTypeDef",
    "JupyterLabAppImageConfigUnionTypeDef",
    "JupyterLabAppSettingsOutputTypeDef",
    "JupyterLabAppSettingsTypeDef",
    "JupyterServerAppSettingsOutputTypeDef",
    "JupyterServerAppSettingsTypeDef",
    "KendraSettingsTypeDef",
    "KernelGatewayAppSettingsOutputTypeDef",
    "KernelGatewayAppSettingsTypeDef",
    "KernelGatewayImageConfigOutputTypeDef",
    "KernelGatewayImageConfigTypeDef",
    "KernelGatewayImageConfigUnionTypeDef",
    "KernelSpecTypeDef",
    "LabelCountersForWorkteamTypeDef",
    "LabelCountersTypeDef",
    "LabelingJobAlgorithmsConfigOutputTypeDef",
    "LabelingJobAlgorithmsConfigTypeDef",
    "LabelingJobAlgorithmsConfigUnionTypeDef",
    "LabelingJobDataAttributesOutputTypeDef",
    "LabelingJobDataAttributesTypeDef",
    "LabelingJobDataSourceTypeDef",
    "LabelingJobForWorkteamSummaryTypeDef",
    "LabelingJobInputConfigOutputTypeDef",
    "LabelingJobInputConfigTypeDef",
    "LabelingJobInputConfigUnionTypeDef",
    "LabelingJobOutputConfigTypeDef",
    "LabelingJobOutputTypeDef",
    "LabelingJobResourceConfigOutputTypeDef",
    "LabelingJobResourceConfigTypeDef",
    "LabelingJobS3DataSourceTypeDef",
    "LabelingJobSnsDataSourceTypeDef",
    "LabelingJobStoppingConditionsTypeDef",
    "LabelingJobSummaryTypeDef",
    "LambdaStepMetadataTypeDef",
    "LastUpdateStatusTypeDef",
    "LineageGroupSummaryTypeDef",
    "LineageMetadataTypeDef",
    "ListActionsRequestPaginateTypeDef",
    "ListActionsRequestTypeDef",
    "ListActionsResponseTypeDef",
    "ListAlgorithmsInputPaginateTypeDef",
    "ListAlgorithmsInputTypeDef",
    "ListAlgorithmsOutputTypeDef",
    "ListAliasesRequestPaginateTypeDef",
    "ListAliasesRequestTypeDef",
    "ListAliasesResponseTypeDef",
    "ListAppImageConfigsRequestPaginateTypeDef",
    "ListAppImageConfigsRequestTypeDef",
    "ListAppImageConfigsResponseTypeDef",
    "ListAppsRequestPaginateTypeDef",
    "ListAppsRequestTypeDef",
    "ListAppsResponseTypeDef",
    "ListArtifactsRequestPaginateTypeDef",
    "ListArtifactsRequestTypeDef",
    "ListArtifactsResponseTypeDef",
    "ListAssociationsRequestPaginateTypeDef",
    "ListAssociationsRequestTypeDef",
    "ListAssociationsResponseTypeDef",
    "ListAutoMLJobsRequestPaginateTypeDef",
    "ListAutoMLJobsRequestTypeDef",
    "ListAutoMLJobsResponseTypeDef",
    "ListCandidatesForAutoMLJobRequestPaginateTypeDef",
    "ListCandidatesForAutoMLJobRequestTypeDef",
    "ListCandidatesForAutoMLJobResponseTypeDef",
    "ListClusterEventsRequestPaginateTypeDef",
    "ListClusterEventsRequestTypeDef",
    "ListClusterEventsResponseTypeDef",
    "ListClusterNodesRequestPaginateTypeDef",
    "ListClusterNodesRequestTypeDef",
    "ListClusterNodesResponseTypeDef",
    "ListClusterSchedulerConfigsRequestPaginateTypeDef",
    "ListClusterSchedulerConfigsRequestTypeDef",
    "ListClusterSchedulerConfigsResponseTypeDef",
    "ListClustersRequestPaginateTypeDef",
    "ListClustersRequestTypeDef",
    "ListClustersResponseTypeDef",
    "ListCodeRepositoriesInputPaginateTypeDef",
    "ListCodeRepositoriesInputTypeDef",
    "ListCodeRepositoriesOutputTypeDef",
    "ListCompilationJobsRequestPaginateTypeDef",
    "ListCompilationJobsRequestTypeDef",
    "ListCompilationJobsResponseTypeDef",
    "ListComputeQuotasRequestPaginateTypeDef",
    "ListComputeQuotasRequestTypeDef",
    "ListComputeQuotasResponseTypeDef",
    "ListContextsRequestPaginateTypeDef",
    "ListContextsRequestTypeDef",
    "ListContextsResponseTypeDef",
    "ListDataQualityJobDefinitionsRequestPaginateTypeDef",
    "ListDataQualityJobDefinitionsRequestTypeDef",
    "ListDataQualityJobDefinitionsResponseTypeDef",
    "ListDeviceFleetsRequestPaginateTypeDef",
    "ListDeviceFleetsRequestTypeDef",
    "ListDeviceFleetsResponseTypeDef",
    "ListDevicesRequestPaginateTypeDef",
    "ListDevicesRequestTypeDef",
    "ListDevicesResponseTypeDef",
    "ListDomainsRequestPaginateTypeDef",
    "ListDomainsRequestTypeDef",
    "ListDomainsResponseTypeDef",
    "ListEdgeDeploymentPlansRequestPaginateTypeDef",
    "ListEdgeDeploymentPlansRequestTypeDef",
    "ListEdgeDeploymentPlansResponseTypeDef",
    "ListEdgePackagingJobsRequestPaginateTypeDef",
    "ListEdgePackagingJobsRequestTypeDef",
    "ListEdgePackagingJobsResponseTypeDef",
    "ListEndpointConfigsInputPaginateTypeDef",
    "ListEndpointConfigsInputTypeDef",
    "ListEndpointConfigsOutputTypeDef",
    "ListEndpointsInputPaginateTypeDef",
    "ListEndpointsInputTypeDef",
    "ListEndpointsOutputTypeDef",
    "ListExperimentsRequestPaginateTypeDef",
    "ListExperimentsRequestTypeDef",
    "ListExperimentsResponseTypeDef",
    "ListFeatureGroupsRequestPaginateTypeDef",
    "ListFeatureGroupsRequestTypeDef",
    "ListFeatureGroupsResponseTypeDef",
    "ListFlowDefinitionsRequestPaginateTypeDef",
    "ListFlowDefinitionsRequestTypeDef",
    "ListFlowDefinitionsResponseTypeDef",
    "ListHubContentVersionsRequestTypeDef",
    "ListHubContentVersionsResponseTypeDef",
    "ListHubContentsRequestTypeDef",
    "ListHubContentsResponseTypeDef",
    "ListHubsRequestTypeDef",
    "ListHubsResponseTypeDef",
    "ListHumanTaskUisRequestPaginateTypeDef",
    "ListHumanTaskUisRequestTypeDef",
    "ListHumanTaskUisResponseTypeDef",
    "ListHyperParameterTuningJobsRequestPaginateTypeDef",
    "ListHyperParameterTuningJobsRequestTypeDef",
    "ListHyperParameterTuningJobsResponseTypeDef",
    "ListImageVersionsRequestPaginateTypeDef",
    "ListImageVersionsRequestTypeDef",
    "ListImageVersionsResponseTypeDef",
    "ListImagesRequestPaginateTypeDef",
    "ListImagesRequestTypeDef",
    "ListImagesResponseTypeDef",
    "ListInferenceComponentsInputPaginateTypeDef",
    "ListInferenceComponentsInputTypeDef",
    "ListInferenceComponentsOutputTypeDef",
    "ListInferenceExperimentsRequestPaginateTypeDef",
    "ListInferenceExperimentsRequestTypeDef",
    "ListInferenceExperimentsResponseTypeDef",
    "ListInferenceRecommendationsJobStepsRequestPaginateTypeDef",
    "ListInferenceRecommendationsJobStepsRequestTypeDef",
    "ListInferenceRecommendationsJobStepsResponseTypeDef",
    "ListInferenceRecommendationsJobsRequestPaginateTypeDef",
    "ListInferenceRecommendationsJobsRequestTypeDef",
    "ListInferenceRecommendationsJobsResponseTypeDef",
    "ListLabelingJobsForWorkteamRequestPaginateTypeDef",
    "ListLabelingJobsForWorkteamRequestTypeDef",
    "ListLabelingJobsForWorkteamResponseTypeDef",
    "ListLabelingJobsRequestPaginateTypeDef",
    "ListLabelingJobsRequestTypeDef",
    "ListLabelingJobsResponseTypeDef",
    "ListLineageGroupsRequestPaginateTypeDef",
    "ListLineageGroupsRequestTypeDef",
    "ListLineageGroupsResponseTypeDef",
    "ListMlflowAppsRequestPaginateTypeDef",
    "ListMlflowAppsRequestTypeDef",
    "ListMlflowAppsResponseTypeDef",
    "ListMlflowTrackingServersRequestPaginateTypeDef",
    "ListMlflowTrackingServersRequestTypeDef",
    "ListMlflowTrackingServersResponseTypeDef",
    "ListModelBiasJobDefinitionsRequestPaginateTypeDef",
    "ListModelBiasJobDefinitionsRequestTypeDef",
    "ListModelBiasJobDefinitionsResponseTypeDef",
    "ListModelCardExportJobsRequestPaginateTypeDef",
    "ListModelCardExportJobsRequestTypeDef",
    "ListModelCardExportJobsResponseTypeDef",
    "ListModelCardVersionsRequestPaginateTypeDef",
    "ListModelCardVersionsRequestTypeDef",
    "ListModelCardVersionsResponseTypeDef",
    "ListModelCardsRequestPaginateTypeDef",
    "ListModelCardsRequestTypeDef",
    "ListModelCardsResponseTypeDef",
    "ListModelExplainabilityJobDefinitionsRequestPaginateTypeDef",
    "ListModelExplainabilityJobDefinitionsRequestTypeDef",
    "ListModelExplainabilityJobDefinitionsResponseTypeDef",
    "ListModelMetadataRequestPaginateTypeDef",
    "ListModelMetadataRequestTypeDef",
    "ListModelMetadataResponseTypeDef",
    "ListModelPackageGroupsInputPaginateTypeDef",
    "ListModelPackageGroupsInputTypeDef",
    "ListModelPackageGroupsOutputTypeDef",
    "ListModelPackagesInputPaginateTypeDef",
    "ListModelPackagesInputTypeDef",
    "ListModelPackagesOutputTypeDef",
    "ListModelQualityJobDefinitionsRequestPaginateTypeDef",
    "ListModelQualityJobDefinitionsRequestTypeDef",
    "ListModelQualityJobDefinitionsResponseTypeDef",
    "ListModelsInputPaginateTypeDef",
    "ListModelsInputTypeDef",
    "ListModelsOutputTypeDef",
    "ListMonitoringAlertHistoryRequestPaginateTypeDef",
    "ListMonitoringAlertHistoryRequestTypeDef",
    "ListMonitoringAlertHistoryResponseTypeDef",
    "ListMonitoringAlertsRequestPaginateTypeDef",
    "ListMonitoringAlertsRequestTypeDef",
    "ListMonitoringAlertsResponseTypeDef",
    "ListMonitoringExecutionsRequestPaginateTypeDef",
    "ListMonitoringExecutionsRequestTypeDef",
    "ListMonitoringExecutionsResponseTypeDef",
    "ListMonitoringSchedulesRequestPaginateTypeDef",
    "ListMonitoringSchedulesRequestTypeDef",
    "ListMonitoringSchedulesResponseTypeDef",
    "ListNotebookInstanceLifecycleConfigsInputPaginateTypeDef",
    "ListNotebookInstanceLifecycleConfigsInputTypeDef",
    "ListNotebookInstanceLifecycleConfigsOutputTypeDef",
    "ListNotebookInstancesInputPaginateTypeDef",
    "ListNotebookInstancesInputTypeDef",
    "ListNotebookInstancesOutputTypeDef",
    "ListOptimizationJobsRequestPaginateTypeDef",
    "ListOptimizationJobsRequestTypeDef",
    "ListOptimizationJobsResponseTypeDef",
    "ListPartnerAppsRequestPaginateTypeDef",
    "ListPartnerAppsRequestTypeDef",
    "ListPartnerAppsResponseTypeDef",
    "ListPipelineExecutionStepsRequestPaginateTypeDef",
    "ListPipelineExecutionStepsRequestTypeDef",
    "ListPipelineExecutionStepsResponseTypeDef",
    "ListPipelineExecutionsRequestPaginateTypeDef",
    "ListPipelineExecutionsRequestTypeDef",
    "ListPipelineExecutionsResponseTypeDef",
    "ListPipelineParametersForExecutionRequestPaginateTypeDef",
    "ListPipelineParametersForExecutionRequestTypeDef",
    "ListPipelineParametersForExecutionResponseTypeDef",
    "ListPipelineVersionsRequestPaginateTypeDef",
    "ListPipelineVersionsRequestTypeDef",
    "ListPipelineVersionsResponseTypeDef",
    "ListPipelinesRequestPaginateTypeDef",
    "ListPipelinesRequestTypeDef",
    "ListPipelinesResponseTypeDef",
    "ListProcessingJobsRequestPaginateTypeDef",
    "ListProcessingJobsRequestTypeDef",
    "ListProcessingJobsResponseTypeDef",
    "ListProjectsInputTypeDef",
    "ListProjectsOutputTypeDef",
    "ListResourceCatalogsRequestPaginateTypeDef",
    "ListResourceCatalogsRequestTypeDef",
    "ListResourceCatalogsResponseTypeDef",
    "ListSpacesRequestPaginateTypeDef",
    "ListSpacesRequestTypeDef",
    "ListSpacesResponseTypeDef",
    "ListStageDevicesRequestPaginateTypeDef",
    "ListStageDevicesRequestTypeDef",
    "ListStageDevicesResponseTypeDef",
    "ListStudioLifecycleConfigsRequestPaginateTypeDef",
    "ListStudioLifecycleConfigsRequestTypeDef",
    "ListStudioLifecycleConfigsResponseTypeDef",
    "ListSubscribedWorkteamsRequestPaginateTypeDef",
    "ListSubscribedWorkteamsRequestTypeDef",
    "ListSubscribedWorkteamsResponseTypeDef",
    "ListTagsInputPaginateTypeDef",
    "ListTagsInputTypeDef",
    "ListTagsOutputTypeDef",
    "ListTrainingJobsForHyperParameterTuningJobRequestPaginateTypeDef",
    "ListTrainingJobsForHyperParameterTuningJobRequestTypeDef",
    "ListTrainingJobsForHyperParameterTuningJobResponseTypeDef",
    "ListTrainingJobsRequestPaginateTypeDef",
    "ListTrainingJobsRequestTypeDef",
    "ListTrainingJobsResponseTypeDef",
    "ListTrainingPlansRequestPaginateTypeDef",
    "ListTrainingPlansRequestTypeDef",
    "ListTrainingPlansResponseTypeDef",
    "ListTransformJobsRequestPaginateTypeDef",
    "ListTransformJobsRequestTypeDef",
    "ListTransformJobsResponseTypeDef",
    "ListTrialComponentsRequestPaginateTypeDef",
    "ListTrialComponentsRequestTypeDef",
    "ListTrialComponentsResponseTypeDef",
    "ListTrialsRequestPaginateTypeDef",
    "ListTrialsRequestTypeDef",
    "ListTrialsResponseTypeDef",
    "ListUltraServersByReservedCapacityRequestPaginateTypeDef",
    "ListUltraServersByReservedCapacityRequestTypeDef",
    "ListUltraServersByReservedCapacityResponseTypeDef",
    "ListUserProfilesRequestPaginateTypeDef",
    "ListUserProfilesRequestTypeDef",
    "ListUserProfilesResponseTypeDef",
    "ListWorkforcesRequestPaginateTypeDef",
    "ListWorkforcesRequestTypeDef",
    "ListWorkforcesResponseTypeDef",
    "ListWorkteamsRequestPaginateTypeDef",
    "ListWorkteamsRequestTypeDef",
    "ListWorkteamsResponseTypeDef",
    "MLflowConfigurationTypeDef",
    "MemberDefinitionOutputTypeDef",
    "MemberDefinitionTypeDef",
    "MemberDefinitionUnionTypeDef",
    "MetadataPropertiesTypeDef",
    "MetricDataTypeDef",
    "MetricDatumTypeDef",
    "MetricDefinitionTypeDef",
    "MetricSpecificationTypeDef",
    "MetricsConfigTypeDef",
    "MetricsSourceTypeDef",
    "MlflowAppSummaryTypeDef",
    "MlflowConfigTypeDef",
    "MlflowDetailsTypeDef",
    "ModelAccessConfigTypeDef",
    "ModelArtifactsTypeDef",
    "ModelBiasAppSpecificationOutputTypeDef",
    "ModelBiasAppSpecificationTypeDef",
    "ModelBiasAppSpecificationUnionTypeDef",
    "ModelBiasBaselineConfigTypeDef",
    "ModelBiasJobInputOutputTypeDef",
    "ModelBiasJobInputTypeDef",
    "ModelBiasJobInputUnionTypeDef",
    "ModelCardExportArtifactsTypeDef",
    "ModelCardExportJobSummaryTypeDef",
    "ModelCardExportOutputConfigTypeDef",
    "ModelCardSecurityConfigTypeDef",
    "ModelCardSummaryTypeDef",
    "ModelCardTypeDef",
    "ModelCardVersionSummaryTypeDef",
    "ModelClientConfigTypeDef",
    "ModelCompilationConfigOutputTypeDef",
    "ModelCompilationConfigTypeDef",
    "ModelCompilationConfigUnionTypeDef",
    "ModelConfigurationTypeDef",
    "ModelDashboardEndpointTypeDef",
    "ModelDashboardIndicatorActionTypeDef",
    "ModelDashboardModelCardTypeDef",
    "ModelDashboardModelTypeDef",
    "ModelDashboardMonitoringScheduleTypeDef",
    "ModelDataQualityTypeDef",
    "ModelDataSourceTypeDef",
    "ModelDeployConfigTypeDef",
    "ModelDeployResultTypeDef",
    "ModelDigestsTypeDef",
    "ModelExplainabilityAppSpecificationOutputTypeDef",
    "ModelExplainabilityAppSpecificationTypeDef",
    "ModelExplainabilityAppSpecificationUnionTypeDef",
    "ModelExplainabilityBaselineConfigTypeDef",
    "ModelExplainabilityJobInputOutputTypeDef",
    "ModelExplainabilityJobInputTypeDef",
    "ModelExplainabilityJobInputUnionTypeDef",
    "ModelInfrastructureConfigTypeDef",
    "ModelInputTypeDef",
    "ModelLatencyThresholdTypeDef",
    "ModelLifeCycleTypeDef",
    "ModelMetadataFilterTypeDef",
    "ModelMetadataSearchExpressionTypeDef",
    "ModelMetadataSummaryTypeDef",
    "ModelMetricsTypeDef",
    "ModelPackageConfigTypeDef",
    "ModelPackageContainerDefinitionOutputTypeDef",
    "ModelPackageContainerDefinitionTypeDef",
    "ModelPackageContainerDefinitionUnionTypeDef",
    "ModelPackageGroupSummaryTypeDef",
    "ModelPackageGroupTypeDef",
    "ModelPackageModelCardTypeDef",
    "ModelPackageSecurityConfigTypeDef",
    "ModelPackageStatusDetailsTypeDef",
    "ModelPackageStatusItemTypeDef",
    "ModelPackageSummaryTypeDef",
    "ModelPackageTypeDef",
    "ModelPackageValidationProfileOutputTypeDef",
    "ModelPackageValidationProfileTypeDef",
    "ModelPackageValidationSpecificationOutputTypeDef",
    "ModelPackageValidationSpecificationTypeDef",
    "ModelPackageValidationSpecificationUnionTypeDef",
    "ModelQualityAppSpecificationOutputTypeDef",
    "ModelQualityAppSpecificationTypeDef",
    "ModelQualityAppSpecificationUnionTypeDef",
    "ModelQualityBaselineConfigTypeDef",
    "ModelQualityJobInputOutputTypeDef",
    "ModelQualityJobInputTypeDef",
    "ModelQualityJobInputUnionTypeDef",
    "ModelQualityTypeDef",
    "ModelQuantizationConfigOutputTypeDef",
    "ModelQuantizationConfigTypeDef",
    "ModelQuantizationConfigUnionTypeDef",
    "ModelRegisterSettingsTypeDef",
    "ModelShardingConfigOutputTypeDef",
    "ModelShardingConfigTypeDef",
    "ModelShardingConfigUnionTypeDef",
    "ModelSpeculativeDecodingConfigTypeDef",
    "ModelSpeculativeDecodingTrainingDataSourceTypeDef",
    "ModelStepMetadataTypeDef",
    "ModelSummaryTypeDef",
    "ModelTypeDef",
    "ModelVariantConfigSummaryTypeDef",
    "ModelVariantConfigTypeDef",
    "MonitoringAlertActionsTypeDef",
    "MonitoringAlertHistorySummaryTypeDef",
    "MonitoringAlertSummaryTypeDef",
    "MonitoringAppSpecificationOutputTypeDef",
    "MonitoringAppSpecificationTypeDef",
    "MonitoringBaselineConfigTypeDef",
    "MonitoringClusterConfigTypeDef",
    "MonitoringConstraintsResourceTypeDef",
    "MonitoringCsvDatasetFormatTypeDef",
    "MonitoringDatasetFormatOutputTypeDef",
    "MonitoringDatasetFormatTypeDef",
    "MonitoringExecutionSummaryTypeDef",
    "MonitoringGroundTruthS3InputTypeDef",
    "MonitoringInputOutputTypeDef",
    "MonitoringInputTypeDef",
    "MonitoringJobDefinitionOutputTypeDef",
    "MonitoringJobDefinitionSummaryTypeDef",
    "MonitoringJobDefinitionTypeDef",
    "MonitoringJsonDatasetFormatTypeDef",
    "MonitoringNetworkConfigOutputTypeDef",
    "MonitoringNetworkConfigTypeDef",
    "MonitoringNetworkConfigUnionTypeDef",
    "MonitoringOutputConfigOutputTypeDef",
    "MonitoringOutputConfigTypeDef",
    "MonitoringOutputConfigUnionTypeDef",
    "MonitoringOutputTypeDef",
    "MonitoringResourcesTypeDef",
    "MonitoringS3OutputTypeDef",
    "MonitoringScheduleConfigOutputTypeDef",
    "MonitoringScheduleConfigTypeDef",
    "MonitoringScheduleConfigUnionTypeDef",
    "MonitoringScheduleSummaryTypeDef",
    "MonitoringScheduleTypeDef",
    "MonitoringStatisticsResourceTypeDef",
    "MonitoringStoppingConditionTypeDef",
    "MultiModelConfigTypeDef",
    "NeoVpcConfigOutputTypeDef",
    "NeoVpcConfigTypeDef",
    "NeoVpcConfigUnionTypeDef",
    "NestedFiltersTypeDef",
    "NetworkConfigOutputTypeDef",
    "NetworkConfigTypeDef",
    "NetworkConfigUnionTypeDef",
    "NodeAdditionResultTypeDef",
    "NotebookInstanceLifecycleConfigSummaryTypeDef",
    "NotebookInstanceLifecycleHookTypeDef",
    "NotebookInstanceSummaryTypeDef",
    "NotificationConfigurationTypeDef",
    "ObjectiveStatusCountersTypeDef",
    "OfflineStoreConfigTypeDef",
    "OfflineStoreStatusTypeDef",
    "OidcConfigForResponseTypeDef",
    "OidcConfigTypeDef",
    "OidcMemberDefinitionOutputTypeDef",
    "OidcMemberDefinitionTypeDef",
    "OidcMemberDefinitionUnionTypeDef",
    "OnlineStoreConfigTypeDef",
    "OnlineStoreConfigUpdateTypeDef",
    "OnlineStoreSecurityConfigTypeDef",
    "OptimizationConfigOutputTypeDef",
    "OptimizationConfigTypeDef",
    "OptimizationConfigUnionTypeDef",
    "OptimizationJobModelSourceS3TypeDef",
    "OptimizationJobModelSourceTypeDef",
    "OptimizationJobOutputConfigTypeDef",
    "OptimizationJobSummaryTypeDef",
    "OptimizationModelAccessConfigTypeDef",
    "OptimizationOutputTypeDef",
    "OptimizationSageMakerModelTypeDef",
    "OptimizationVpcConfigOutputTypeDef",
    "OptimizationVpcConfigTypeDef",
    "OptimizationVpcConfigUnionTypeDef",
    "OutputConfigTypeDef",
    "OutputDataConfigTypeDef",
    "OutputParameterTypeDef",
    "OwnershipSettingsSummaryTypeDef",
    "OwnershipSettingsTypeDef",
    "PaginatorConfigTypeDef",
    "ParallelismConfigurationTypeDef",
    "ParameterRangeOutputTypeDef",
    "ParameterRangeTypeDef",
    "ParameterRangesOutputTypeDef",
    "ParameterRangesTypeDef",
    "ParameterRangesUnionTypeDef",
    "ParameterTypeDef",
    "ParentHyperParameterTuningJobTypeDef",
    "ParentTypeDef",
    "PartnerAppConfigOutputTypeDef",
    "PartnerAppConfigTypeDef",
    "PartnerAppConfigUnionTypeDef",
    "PartnerAppMaintenanceConfigTypeDef",
    "PartnerAppSummaryTypeDef",
    "PendingDeploymentSummaryTypeDef",
    "PendingProductionVariantSummaryTypeDef",
    "PhaseTypeDef",
    "PipelineDefinitionS3LocationTypeDef",
    "PipelineExecutionStepMetadataTypeDef",
    "PipelineExecutionStepTypeDef",
    "PipelineExecutionSummaryTypeDef",
    "PipelineExecutionTypeDef",
    "PipelineExperimentConfigTypeDef",
    "PipelineSummaryTypeDef",
    "PipelineTypeDef",
    "PipelineVersionSummaryTypeDef",
    "PipelineVersionTypeDef",
    "PlacementSpecificationTypeDef",
    "PredefinedMetricSpecificationTypeDef",
    "PresignedUrlAccessConfigTypeDef",
    "PriorityClassTypeDef",
    "ProcessingClusterConfigTypeDef",
    "ProcessingFeatureStoreOutputTypeDef",
    "ProcessingInputTypeDef",
    "ProcessingJobStepMetadataTypeDef",
    "ProcessingJobSummaryTypeDef",
    "ProcessingJobTypeDef",
    "ProcessingOutputConfigOutputTypeDef",
    "ProcessingOutputConfigTypeDef",
    "ProcessingOutputConfigUnionTypeDef",
    "ProcessingOutputTypeDef",
    "ProcessingResourcesTypeDef",
    "ProcessingS3InputTypeDef",
    "ProcessingS3OutputTypeDef",
    "ProcessingStoppingConditionTypeDef",
    "ProductionVariantCapacityReservationConfigTypeDef",
    "ProductionVariantCapacityReservationSummaryTypeDef",
    "ProductionVariantCoreDumpConfigTypeDef",
    "ProductionVariantManagedInstanceScalingTypeDef",
    "ProductionVariantRoutingConfigTypeDef",
    "ProductionVariantServerlessConfigTypeDef",
    "ProductionVariantServerlessUpdateConfigTypeDef",
    "ProductionVariantStatusTypeDef",
    "ProductionVariantSummaryTypeDef",
    "ProductionVariantTypeDef",
    "ProfilerConfigForUpdateTypeDef",
    "ProfilerConfigOutputTypeDef",
    "ProfilerConfigTypeDef",
    "ProfilerConfigUnionTypeDef",
    "ProfilerRuleConfigurationOutputTypeDef",
    "ProfilerRuleConfigurationTypeDef",
    "ProfilerRuleConfigurationUnionTypeDef",
    "ProfilerRuleEvaluationStatusTypeDef",
    "ProjectSummaryTypeDef",
    "ProjectTypeDef",
    "PropertyNameQueryTypeDef",
    "PropertyNameSuggestionTypeDef",
    "ProvisioningParameterTypeDef",
    "PublicWorkforceTaskPriceTypeDef",
    "PutModelPackageGroupPolicyInputTypeDef",
    "PutModelPackageGroupPolicyOutputTypeDef",
    "QualityCheckStepMetadataTypeDef",
    "QueryFiltersTypeDef",
    "QueryLineageRequestTypeDef",
    "QueryLineageResponseTypeDef",
    "RSessionAppSettingsOutputTypeDef",
    "RSessionAppSettingsTypeDef",
    "RStudioServerProAppSettingsTypeDef",
    "RStudioServerProDomainSettingsForUpdateTypeDef",
    "RStudioServerProDomainSettingsTypeDef",
    "RealTimeInferenceConfigTypeDef",
    "RealTimeInferenceRecommendationTypeDef",
    "RecommendationJobCompiledOutputConfigTypeDef",
    "RecommendationJobContainerConfigOutputTypeDef",
    "RecommendationJobContainerConfigTypeDef",
    "RecommendationJobInferenceBenchmarkTypeDef",
    "RecommendationJobInputConfigOutputTypeDef",
    "RecommendationJobInputConfigTypeDef",
    "RecommendationJobInputConfigUnionTypeDef",
    "RecommendationJobOutputConfigTypeDef",
    "RecommendationJobPayloadConfigOutputTypeDef",
    "RecommendationJobPayloadConfigTypeDef",
    "RecommendationJobResourceLimitTypeDef",
    "RecommendationJobStoppingConditionsOutputTypeDef",
    "RecommendationJobStoppingConditionsTypeDef",
    "RecommendationJobStoppingConditionsUnionTypeDef",
    "RecommendationJobVpcConfigOutputTypeDef",
    "RecommendationJobVpcConfigTypeDef",
    "RecommendationMetricsTypeDef",
    "RedshiftDatasetDefinitionTypeDef",
    "RegisterDevicesRequestTypeDef",
    "RegisterModelStepMetadataTypeDef",
    "RemoteDebugConfigForUpdateTypeDef",
    "RemoteDebugConfigTypeDef",
    "RenderUiTemplateRequestTypeDef",
    "RenderUiTemplateResponseTypeDef",
    "RenderableTaskTypeDef",
    "RenderingErrorTypeDef",
    "RepositoryAuthConfigTypeDef",
    "ReservedCapacityOfferingTypeDef",
    "ReservedCapacitySummaryTypeDef",
    "ResolvedAttributesTypeDef",
    "ResourceCatalogTypeDef",
    "ResourceConfigForUpdateTypeDef",
    "ResourceConfigOutputTypeDef",
    "ResourceConfigTypeDef",
    "ResourceConfigUnionTypeDef",
    "ResourceLimitsTypeDef",
    "ResourceSharingConfigOutputTypeDef",
    "ResourceSharingConfigTypeDef",
    "ResourceSpecTypeDef",
    "ResponseMetadataTypeDef",
    "RetentionPolicyTypeDef",
    "RetryPipelineExecutionRequestTypeDef",
    "RetryPipelineExecutionResponseTypeDef",
    "RetryStrategyTypeDef",
    "RoleGroupAssignmentOutputTypeDef",
    "RoleGroupAssignmentTypeDef",
    "RollingDeploymentPolicyTypeDef",
    "RollingUpdatePolicyTypeDef",
    "S3DataSourceOutputTypeDef",
    "S3DataSourceTypeDef",
    "S3DataSourceUnionTypeDef",
    "S3FileSystemConfigTypeDef",
    "S3FileSystemTypeDef",
    "S3ModelDataSourceTypeDef",
    "S3PresignTypeDef",
    "S3StorageConfigTypeDef",
    "ScalingPolicyMetricTypeDef",
    "ScalingPolicyObjectiveTypeDef",
    "ScalingPolicyTypeDef",
    "ScheduleConfigTypeDef",
    "ScheduledUpdateConfigOutputTypeDef",
    "ScheduledUpdateConfigTypeDef",
    "ScheduledUpdateConfigUnionTypeDef",
    "SchedulerConfigOutputTypeDef",
    "SchedulerConfigTypeDef",
    "SchedulerConfigUnionTypeDef",
    "SearchExpressionPaginatorTypeDef",
    "SearchExpressionTypeDef",
    "SearchRecordTypeDef",
    "SearchRequestPaginateTypeDef",
    "SearchRequestTypeDef",
    "SearchResponseTypeDef",
    "SearchTrainingPlanOfferingsRequestTypeDef",
    "SearchTrainingPlanOfferingsResponseTypeDef",
    "SecondaryStatusTransitionTypeDef",
    "SelectedStepTypeDef",
    "SelectiveExecutionConfigOutputTypeDef",
    "SelectiveExecutionConfigTypeDef",
    "SelectiveExecutionConfigUnionTypeDef",
    "SelectiveExecutionResultTypeDef",
    "SendPipelineExecutionStepFailureRequestTypeDef",
    "SendPipelineExecutionStepFailureResponseTypeDef",
    "SendPipelineExecutionStepSuccessRequestTypeDef",
    "SendPipelineExecutionStepSuccessResponseTypeDef",
    "ServerlessJobConfigTypeDef",
    "ServiceCatalogProvisionedProductDetailsTypeDef",
    "ServiceCatalogProvisioningDetailsOutputTypeDef",
    "ServiceCatalogProvisioningDetailsTypeDef",
    "ServiceCatalogProvisioningDetailsUnionTypeDef",
    "ServiceCatalogProvisioningUpdateDetailsTypeDef",
    "SessionChainingConfigTypeDef",
    "ShadowModeConfigOutputTypeDef",
    "ShadowModeConfigTypeDef",
    "ShadowModeConfigUnionTypeDef",
    "ShadowModelVariantConfigTypeDef",
    "SharingSettingsTypeDef",
    "ShuffleConfigTypeDef",
    "SourceAlgorithmSpecificationOutputTypeDef",
    "SourceAlgorithmSpecificationTypeDef",
    "SourceAlgorithmSpecificationUnionTypeDef",
    "SourceAlgorithmTypeDef",
    "SourceIpConfigOutputTypeDef",
    "SourceIpConfigTypeDef",
    "SourceIpConfigUnionTypeDef",
    "SpaceAppLifecycleManagementTypeDef",
    "SpaceCodeEditorAppSettingsTypeDef",
    "SpaceDetailsTypeDef",
    "SpaceIdleSettingsTypeDef",
    "SpaceJupyterLabAppSettingsOutputTypeDef",
    "SpaceJupyterLabAppSettingsTypeDef",
    "SpaceSettingsOutputTypeDef",
    "SpaceSettingsSummaryTypeDef",
    "SpaceSettingsTypeDef",
    "SpaceSettingsUnionTypeDef",
    "SpaceSharingSettingsSummaryTypeDef",
    "SpaceSharingSettingsTypeDef",
    "SpaceStorageSettingsTypeDef",
    "StairsTypeDef",
    "StartEdgeDeploymentStageRequestTypeDef",
    "StartInferenceExperimentRequestTypeDef",
    "StartInferenceExperimentResponseTypeDef",
    "StartMlflowTrackingServerRequestTypeDef",
    "StartMlflowTrackingServerResponseTypeDef",
    "StartMonitoringScheduleRequestTypeDef",
    "StartNotebookInstanceInputTypeDef",
    "StartPipelineExecutionRequestTypeDef",
    "StartPipelineExecutionResponseTypeDef",
    "StartSessionRequestTypeDef",
    "StartSessionResponseTypeDef",
    "StopAutoMLJobRequestTypeDef",
    "StopCompilationJobRequestTypeDef",
    "StopEdgeDeploymentStageRequestTypeDef",
    "StopEdgePackagingJobRequestTypeDef",
    "StopHyperParameterTuningJobRequestTypeDef",
    "StopInferenceExperimentRequestTypeDef",
    "StopInferenceExperimentResponseTypeDef",
    "StopInferenceRecommendationsJobRequestTypeDef",
    "StopLabelingJobRequestTypeDef",
    "StopMlflowTrackingServerRequestTypeDef",
    "StopMlflowTrackingServerResponseTypeDef",
    "StopMonitoringScheduleRequestTypeDef",
    "StopNotebookInstanceInputTypeDef",
    "StopOptimizationJobRequestTypeDef",
    "StopPipelineExecutionRequestTypeDef",
    "StopPipelineExecutionResponseTypeDef",
    "StopProcessingJobRequestTypeDef",
    "StopTrainingJobRequestTypeDef",
    "StopTransformJobRequestTypeDef",
    "StoppingConditionTypeDef",
    "StudioLifecycleConfigDetailsTypeDef",
    "StudioWebPortalSettingsOutputTypeDef",
    "StudioWebPortalSettingsTypeDef",
    "SubscribedWorkteamTypeDef",
    "SuggestionQueryTypeDef",
    "TabularJobConfigOutputTypeDef",
    "TabularJobConfigTypeDef",
    "TabularResolvedAttributesTypeDef",
    "TagTypeDef",
    "TargetPlatformTypeDef",
    "TargetTrackingScalingPolicyConfigurationTypeDef",
    "TemplateProviderDetailTypeDef",
    "TensorBoardAppSettingsTypeDef",
    "TensorBoardOutputConfigTypeDef",
    "TextClassificationJobConfigTypeDef",
    "TextGenerationJobConfigOutputTypeDef",
    "TextGenerationJobConfigTypeDef",
    "TextGenerationResolvedAttributesTypeDef",
    "ThroughputConfigDescriptionTypeDef",
    "ThroughputConfigTypeDef",
    "ThroughputConfigUpdateTypeDef",
    "TimeSeriesConfigOutputTypeDef",
    "TimeSeriesConfigTypeDef",
    "TimeSeriesForecastingJobConfigOutputTypeDef",
    "TimeSeriesForecastingJobConfigTypeDef",
    "TimeSeriesForecastingSettingsTypeDef",
    "TimeSeriesTransformationsOutputTypeDef",
    "TimeSeriesTransformationsTypeDef",
    "TimestampTypeDef",
    "TotalHitsTypeDef",
    "TrackingServerSummaryTypeDef",
    "TrafficPatternOutputTypeDef",
    "TrafficPatternTypeDef",
    "TrafficRoutingConfigTypeDef",
    "TrainingImageConfigTypeDef",
    "TrainingJobDefinitionOutputTypeDef",
    "TrainingJobDefinitionTypeDef",
    "TrainingJobStatusCountersTypeDef",
    "TrainingJobStepMetadataTypeDef",
    "TrainingJobSummaryTypeDef",
    "TrainingJobTypeDef",
    "TrainingPlanFilterTypeDef",
    "TrainingPlanOfferingTypeDef",
    "TrainingPlanSummaryTypeDef",
    "TrainingProgressInfoTypeDef",
    "TrainingRepositoryAuthConfigTypeDef",
    "TrainingSpecificationOutputTypeDef",
    "TrainingSpecificationTypeDef",
    "TrainingSpecificationUnionTypeDef",
    "TransformDataSourceTypeDef",
    "TransformInputTypeDef",
    "TransformJobDefinitionOutputTypeDef",
    "TransformJobDefinitionTypeDef",
    "TransformJobStepMetadataTypeDef",
    "TransformJobSummaryTypeDef",
    "TransformJobTypeDef",
    "TransformOutputTypeDef",
    "TransformResourcesTypeDef",
    "TransformS3DataSourceTypeDef",
    "TrialComponentArtifactTypeDef",
    "TrialComponentMetricSummaryTypeDef",
    "TrialComponentParameterValueTypeDef",
    "TrialComponentSimpleSummaryTypeDef",
    "TrialComponentSourceDetailTypeDef",
    "TrialComponentSourceTypeDef",
    "TrialComponentStatusTypeDef",
    "TrialComponentSummaryTypeDef",
    "TrialComponentTypeDef",
    "TrialSourceTypeDef",
    "TrialSummaryTypeDef",
    "TrialTypeDef",
    "TrustedIdentityPropagationSettingsTypeDef",
    "TtlDurationTypeDef",
    "TuningJobCompletionCriteriaTypeDef",
    "TuningJobStepMetaDataTypeDef",
    "USDTypeDef",
    "UiConfigTypeDef",
    "UiTemplateInfoTypeDef",
    "UiTemplateTypeDef",
    "UltraServerInfoTypeDef",
    "UltraServerSummaryTypeDef",
    "UltraServerTypeDef",
    "UnifiedStudioSettingsTypeDef",
    "UpdateActionRequestTypeDef",
    "UpdateActionResponseTypeDef",
    "UpdateAppImageConfigRequestTypeDef",
    "UpdateAppImageConfigResponseTypeDef",
    "UpdateArtifactRequestTypeDef",
    "UpdateArtifactResponseTypeDef",
    "UpdateClusterRequestTypeDef",
    "UpdateClusterResponseTypeDef",
    "UpdateClusterSchedulerConfigRequestTypeDef",
    "UpdateClusterSchedulerConfigResponseTypeDef",
    "UpdateClusterSoftwareInstanceGroupSpecificationTypeDef",
    "UpdateClusterSoftwareRequestTypeDef",
    "UpdateClusterSoftwareResponseTypeDef",
    "UpdateCodeRepositoryInputTypeDef",
    "UpdateCodeRepositoryOutputTypeDef",
    "UpdateComputeQuotaRequestTypeDef",
    "UpdateComputeQuotaResponseTypeDef",
    "UpdateContextRequestTypeDef",
    "UpdateContextResponseTypeDef",
    "UpdateDeviceFleetRequestTypeDef",
    "UpdateDevicesRequestTypeDef",
    "UpdateDomainRequestTypeDef",
    "UpdateDomainResponseTypeDef",
    "UpdateEndpointInputTypeDef",
    "UpdateEndpointOutputTypeDef",
    "UpdateEndpointWeightsAndCapacitiesInputTypeDef",
    "UpdateEndpointWeightsAndCapacitiesOutputTypeDef",
    "UpdateExperimentRequestTypeDef",
    "UpdateExperimentResponseTypeDef",
    "UpdateFeatureGroupRequestTypeDef",
    "UpdateFeatureGroupResponseTypeDef",
    "UpdateFeatureMetadataRequestTypeDef",
    "UpdateHubContentReferenceRequestTypeDef",
    "UpdateHubContentReferenceResponseTypeDef",
    "UpdateHubContentRequestTypeDef",
    "UpdateHubContentResponseTypeDef",
    "UpdateHubRequestTypeDef",
    "UpdateHubResponseTypeDef",
    "UpdateImageRequestTypeDef",
    "UpdateImageResponseTypeDef",
    "UpdateImageVersionRequestTypeDef",
    "UpdateImageVersionResponseTypeDef",
    "UpdateInferenceComponentInputTypeDef",
    "UpdateInferenceComponentOutputTypeDef",
    "UpdateInferenceComponentRuntimeConfigInputTypeDef",
    "UpdateInferenceComponentRuntimeConfigOutputTypeDef",
    "UpdateInferenceExperimentRequestTypeDef",
    "UpdateInferenceExperimentResponseTypeDef",
    "UpdateMlflowAppRequestTypeDef",
    "UpdateMlflowAppResponseTypeDef",
    "UpdateMlflowTrackingServerRequestTypeDef",
    "UpdateMlflowTrackingServerResponseTypeDef",
    "UpdateModelCardRequestTypeDef",
    "UpdateModelCardResponseTypeDef",
    "UpdateModelPackageInputTypeDef",
    "UpdateModelPackageOutputTypeDef",
    "UpdateMonitoringAlertRequestTypeDef",
    "UpdateMonitoringAlertResponseTypeDef",
    "UpdateMonitoringScheduleRequestTypeDef",
    "UpdateMonitoringScheduleResponseTypeDef",
    "UpdateNotebookInstanceInputTypeDef",
    "UpdateNotebookInstanceLifecycleConfigInputTypeDef",
    "UpdatePartnerAppRequestTypeDef",
    "UpdatePartnerAppResponseTypeDef",
    "UpdatePipelineExecutionRequestTypeDef",
    "UpdatePipelineExecutionResponseTypeDef",
    "UpdatePipelineRequestTypeDef",
    "UpdatePipelineResponseTypeDef",
    "UpdatePipelineVersionRequestTypeDef",
    "UpdatePipelineVersionResponseTypeDef",
    "UpdateProjectInputTypeDef",
    "UpdateProjectOutputTypeDef",
    "UpdateSpaceRequestTypeDef",
    "UpdateSpaceResponseTypeDef",
    "UpdateTemplateProviderTypeDef",
    "UpdateTrainingJobRequestTypeDef",
    "UpdateTrainingJobResponseTypeDef",
    "UpdateTrialComponentRequestTypeDef",
    "UpdateTrialComponentResponseTypeDef",
    "UpdateTrialRequestTypeDef",
    "UpdateTrialResponseTypeDef",
    "UpdateUserProfileRequestTypeDef",
    "UpdateUserProfileResponseTypeDef",
    "UpdateWorkforceRequestTypeDef",
    "UpdateWorkforceResponseTypeDef",
    "UpdateWorkteamRequestTypeDef",
    "UpdateWorkteamResponseTypeDef",
    "UserContextTypeDef",
    "UserProfileDetailsTypeDef",
    "UserSettingsOutputTypeDef",
    "UserSettingsTypeDef",
    "UserSettingsUnionTypeDef",
    "VariantPropertyTypeDef",
    "VectorConfigTypeDef",
    "VertexTypeDef",
    "VisibilityConditionsTypeDef",
    "VpcConfigOutputTypeDef",
    "VpcConfigTypeDef",
    "VpcConfigUnionTypeDef",
    "WaiterConfigTypeDef",
    "WarmPoolStatusTypeDef",
    "WorkerAccessConfigurationTypeDef",
    "WorkforceTypeDef",
    "WorkforceVpcConfigRequestTypeDef",
    "WorkforceVpcConfigResponseTypeDef",
    "WorkspaceSettingsTypeDef",
    "WorkteamTypeDef",
)

AcceleratorPartitionConfigTypeDef = TypedDict(
    "AcceleratorPartitionConfigTypeDef",
    {
        "Type": MIGProfileTypeType,
        "Count": int,
    },
)


class ActionSourceTypeDef(TypedDict):
    SourceUri: str
    SourceType: NotRequired[str]
    SourceId: NotRequired[str]


class AddAssociationRequestTypeDef(TypedDict):
    SourceArn: str
    DestinationArn: str
    AssociationType: NotRequired[AssociationEdgeTypeType]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AddClusterNodeSpecificationTypeDef(TypedDict):
    InstanceGroupName: str
    IncrementTargetCountBy: int


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class AdditionalEnisTypeDef(TypedDict):
    EfaEnis: NotRequired[list[str]]


class AdditionalS3DataSourceTypeDef(TypedDict):
    S3DataType: AdditionalS3DataSourceDataTypeType
    S3Uri: str
    CompressionType: NotRequired[CompressionTypeType]
    ETag: NotRequired[str]


class AgentVersionTypeDef(TypedDict):
    Version: str
    AgentCount: int


class AlarmDetailsTypeDef(TypedDict):
    AlarmName: str


class AlarmTypeDef(TypedDict):
    AlarmName: NotRequired[str]


class MetricDefinitionTypeDef(TypedDict):
    Name: str
    Regex: str


class AlgorithmStatusItemTypeDef(TypedDict):
    Name: str
    Status: DetailedAlgorithmStatusType
    FailureReason: NotRequired[str]


class AlgorithmSummaryTypeDef(TypedDict):
    AlgorithmName: str
    AlgorithmArn: str
    CreationTime: datetime
    AlgorithmStatus: AlgorithmStatusType
    AlgorithmDescription: NotRequired[str]


class AmazonQSettingsTypeDef(TypedDict):
    Status: NotRequired[FeatureStatusType]
    QProfileArn: NotRequired[str]


class AnnotationConsolidationConfigTypeDef(TypedDict):
    AnnotationConsolidationLambdaArn: str


class ResourceSpecTypeDef(TypedDict):
    SageMakerImageArn: NotRequired[str]
    SageMakerImageVersionArn: NotRequired[str]
    SageMakerImageVersionAlias: NotRequired[str]
    InstanceType: NotRequired[AppInstanceTypeType]
    LifecycleConfigArn: NotRequired[str]


class IdleSettingsTypeDef(TypedDict):
    LifecycleManagement: NotRequired[LifecycleManagementType]
    IdleTimeoutInMinutes: NotRequired[int]
    MinIdleTimeoutInMinutes: NotRequired[int]
    MaxIdleTimeoutInMinutes: NotRequired[int]


class AppSpecificationOutputTypeDef(TypedDict):
    ImageUri: str
    ContainerEntrypoint: NotRequired[list[str]]
    ContainerArguments: NotRequired[list[str]]


class AppSpecificationTypeDef(TypedDict):
    ImageUri: str
    ContainerEntrypoint: NotRequired[Sequence[str]]
    ContainerArguments: NotRequired[Sequence[str]]


class ArtifactSourceTypeTypeDef(TypedDict):
    SourceIdType: ArtifactSourceIdTypeType
    Value: str


class AssociateTrialComponentRequestTypeDef(TypedDict):
    TrialComponentName: str
    TrialName: str


class AssociationInfoTypeDef(TypedDict):
    SourceArn: str
    DestinationArn: str


class AsyncInferenceClientConfigTypeDef(TypedDict):
    MaxConcurrentInvocationsPerInstance: NotRequired[int]


class AsyncInferenceNotificationConfigOutputTypeDef(TypedDict):
    SuccessTopic: NotRequired[str]
    ErrorTopic: NotRequired[str]
    IncludeInferenceResponseIn: NotRequired[list[AsyncNotificationTopicTypesType]]


class AsyncInferenceNotificationConfigTypeDef(TypedDict):
    SuccessTopic: NotRequired[str]
    ErrorTopic: NotRequired[str]
    IncludeInferenceResponseIn: NotRequired[Sequence[AsyncNotificationTopicTypesType]]


class AthenaDatasetDefinitionTypeDef(TypedDict):
    Catalog: str
    Database: str
    QueryString: str
    OutputS3Uri: str
    OutputFormat: AthenaResultFormatType
    WorkGroup: NotRequired[str]
    KmsKeyId: NotRequired[str]
    OutputCompression: NotRequired[AthenaResultCompressionTypeType]


class AttachClusterNodeVolumeRequestTypeDef(TypedDict):
    ClusterArn: str
    NodeId: str
    VolumeId: str


class AuthorizedUrlTypeDef(TypedDict):
    Url: NotRequired[str]
    LocalPath: NotRequired[str]


class AutoMLAlgorithmConfigOutputTypeDef(TypedDict):
    AutoMLAlgorithms: list[AutoMLAlgorithmType]


class AutoMLAlgorithmConfigTypeDef(TypedDict):
    AutoMLAlgorithms: Sequence[AutoMLAlgorithmType]


class AutoMLCandidateStepTypeDef(TypedDict):
    CandidateStepType: CandidateStepTypeType
    CandidateStepArn: str
    CandidateStepName: str


class AutoMLContainerDefinitionTypeDef(TypedDict):
    Image: str
    ModelDataUrl: str
    Environment: NotRequired[dict[str, str]]


FinalAutoMLJobObjectiveMetricTypeDef = TypedDict(
    "FinalAutoMLJobObjectiveMetricTypeDef",
    {
        "MetricName": AutoMLMetricEnumType,
        "Value": float,
        "Type": NotRequired[AutoMLJobObjectiveTypeType],
        "StandardMetricName": NotRequired[AutoMLMetricEnumType],
    },
)


class EmrServerlessComputeConfigTypeDef(TypedDict):
    ExecutionRoleARN: str


class AutoMLS3DataSourceTypeDef(TypedDict):
    S3DataType: AutoMLS3DataTypeType
    S3Uri: str


class AutoMLDataSplitConfigTypeDef(TypedDict):
    ValidationFraction: NotRequired[float]


class AutoMLJobArtifactsTypeDef(TypedDict):
    CandidateDefinitionNotebookLocation: NotRequired[str]
    DataExplorationNotebookLocation: NotRequired[str]


class AutoMLJobCompletionCriteriaTypeDef(TypedDict):
    MaxCandidates: NotRequired[int]
    MaxRuntimePerTrainingJobInSeconds: NotRequired[int]
    MaxAutoMLJobRuntimeInSeconds: NotRequired[int]


class AutoMLJobObjectiveTypeDef(TypedDict):
    MetricName: AutoMLMetricEnumType


class AutoMLJobStepMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]


class AutoMLPartialFailureReasonTypeDef(TypedDict):
    PartialFailureMessage: NotRequired[str]


class AutoMLOutputDataConfigTypeDef(TypedDict):
    S3OutputPath: str
    KmsKeyId: NotRequired[str]


class TabularResolvedAttributesTypeDef(TypedDict):
    ProblemType: NotRequired[ProblemTypeType]


class TextGenerationResolvedAttributesTypeDef(TypedDict):
    BaseModelName: NotRequired[str]


class VpcConfigOutputTypeDef(TypedDict):
    SecurityGroupIds: list[str]
    Subnets: list[str]


class VpcConfigTypeDef(TypedDict):
    SecurityGroupIds: Sequence[str]
    Subnets: Sequence[str]


class AutoParameterTypeDef(TypedDict):
    Name: str
    ValueHint: str


class AutotuneTypeDef(TypedDict):
    Mode: Literal["Enabled"]


class AvailableUpgradeTypeDef(TypedDict):
    Version: NotRequired[str]
    ReleaseNotes: NotRequired[list[str]]


class BaseModelTypeDef(TypedDict):
    HubContentName: NotRequired[str]
    HubContentVersion: NotRequired[str]
    RecipeName: NotRequired[str]


class BatchAddClusterNodesErrorTypeDef(TypedDict):
    InstanceGroupName: str
    ErrorCode: BatchAddClusterNodesErrorCodeType
    FailedCount: int
    Message: NotRequired[str]


class NodeAdditionResultTypeDef(TypedDict):
    NodeLogicalId: str
    InstanceGroupName: str
    Status: ClusterInstanceStatusType


class BatchDataCaptureConfigTypeDef(TypedDict):
    DestinationS3Uri: str
    KmsKeyId: NotRequired[str]
    GenerateInferenceId: NotRequired[bool]


class BatchDeleteClusterNodeLogicalIdsErrorTypeDef(TypedDict):
    Code: BatchDeleteClusterNodesErrorCodeType
    Message: str
    NodeLogicalId: str


class BatchDeleteClusterNodesErrorTypeDef(TypedDict):
    Code: BatchDeleteClusterNodesErrorCodeType
    Message: str
    NodeId: str


class BatchDeleteClusterNodesRequestTypeDef(TypedDict):
    ClusterName: str
    NodeIds: NotRequired[Sequence[str]]
    NodeLogicalIds: NotRequired[Sequence[str]]


class BatchDescribeModelPackageErrorTypeDef(TypedDict):
    ErrorCode: str
    ErrorResponse: str


class BatchDescribeModelPackageInputTypeDef(TypedDict):
    ModelPackageArnList: Sequence[str]


class BatchRebootClusterNodeLogicalIdsErrorTypeDef(TypedDict):
    NodeLogicalId: str
    ErrorCode: BatchRebootClusterNodesErrorCodeType
    Message: str


class BatchRebootClusterNodesErrorTypeDef(TypedDict):
    NodeId: str
    ErrorCode: BatchRebootClusterNodesErrorCodeType
    Message: str


class BatchRebootClusterNodesRequestTypeDef(TypedDict):
    ClusterName: str
    NodeIds: NotRequired[Sequence[str]]
    NodeLogicalIds: NotRequired[Sequence[str]]


class BatchReplaceClusterNodeLogicalIdsErrorTypeDef(TypedDict):
    NodeLogicalId: str
    ErrorCode: BatchReplaceClusterNodesErrorCodeType
    Message: str


class BatchReplaceClusterNodesErrorTypeDef(TypedDict):
    NodeId: str
    ErrorCode: BatchReplaceClusterNodesErrorCodeType
    Message: str


class BatchReplaceClusterNodesRequestTypeDef(TypedDict):
    ClusterName: str
    NodeIds: NotRequired[Sequence[str]]
    NodeLogicalIds: NotRequired[Sequence[str]]


class BedrockCustomModelDeploymentMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]


class BedrockCustomModelMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]


class BedrockModelImportMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]


class BedrockProvisionedModelThroughputMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]


class BestObjectiveNotImprovingTypeDef(TypedDict):
    MaxNumberOfTrainingJobsNotImproving: NotRequired[int]


class MetricsSourceTypeDef(TypedDict):
    ContentType: str
    S3Uri: str
    ContentDigest: NotRequired[str]


class CacheHitResultTypeDef(TypedDict):
    SourcePipelineExecutionArn: NotRequired[str]


class OutputParameterTypeDef(TypedDict):
    Name: str
    Value: str


class CandidateArtifactLocationsTypeDef(TypedDict):
    Explainability: str
    ModelInsights: NotRequired[str]
    BacktestResults: NotRequired[str]


MetricDatumTypeDef = TypedDict(
    "MetricDatumTypeDef",
    {
        "MetricName": NotRequired[AutoMLMetricEnumType],
        "StandardMetricName": NotRequired[AutoMLMetricExtendedEnumType],
        "Value": NotRequired[float],
        "Set": NotRequired[MetricSetSourceType],
    },
)


class DirectDeploySettingsTypeDef(TypedDict):
    Status: NotRequired[FeatureStatusType]


class EmrServerlessSettingsTypeDef(TypedDict):
    ExecutionRoleArn: NotRequired[str]
    Status: NotRequired[FeatureStatusType]


class GenerativeAiSettingsTypeDef(TypedDict):
    AmazonBedrockRoleArn: NotRequired[str]


class IdentityProviderOAuthSettingTypeDef(TypedDict):
    DataSourceName: NotRequired[DataSourceNameType]
    Status: NotRequired[FeatureStatusType]
    SecretArn: NotRequired[str]


class KendraSettingsTypeDef(TypedDict):
    Status: NotRequired[FeatureStatusType]


class ModelRegisterSettingsTypeDef(TypedDict):
    Status: NotRequired[FeatureStatusType]
    CrossAccountModelRegisterRoleArn: NotRequired[str]


class TimeSeriesForecastingSettingsTypeDef(TypedDict):
    Status: NotRequired[FeatureStatusType]
    AmazonForecastRoleArn: NotRequired[str]


class WorkspaceSettingsTypeDef(TypedDict):
    S3ArtifactPath: NotRequired[str]
    S3KmsKeyId: NotRequired[str]


CapacityReservationTypeDef = TypedDict(
    "CapacityReservationTypeDef",
    {
        "Arn": NotRequired[str],
        "Type": NotRequired[CapacityReservationTypeType],
    },
)
CapacitySizeConfigTypeDef = TypedDict(
    "CapacitySizeConfigTypeDef",
    {
        "Type": NodeUnavailabilityTypeType,
        "Value": int,
    },
)
CapacitySizeTypeDef = TypedDict(
    "CapacitySizeTypeDef",
    {
        "Type": CapacitySizeTypeType,
        "Value": int,
    },
)


class CaptureContentTypeHeaderOutputTypeDef(TypedDict):
    CsvContentTypes: NotRequired[list[str]]
    JsonContentTypes: NotRequired[list[str]]


class CaptureContentTypeHeaderTypeDef(TypedDict):
    CsvContentTypes: NotRequired[Sequence[str]]
    JsonContentTypes: NotRequired[Sequence[str]]


class CaptureOptionTypeDef(TypedDict):
    CaptureMode: CaptureModeType


class CategoricalParameterOutputTypeDef(TypedDict):
    Name: str
    Value: list[str]


class CategoricalParameterRangeOutputTypeDef(TypedDict):
    Name: str
    Values: list[str]


class CategoricalParameterRangeSpecificationOutputTypeDef(TypedDict):
    Values: list[str]


class CategoricalParameterRangeSpecificationTypeDef(TypedDict):
    Values: Sequence[str]


class CategoricalParameterRangeTypeDef(TypedDict):
    Name: str
    Values: Sequence[str]


class CategoricalParameterTypeDef(TypedDict):
    Name: str
    Value: Sequence[str]


class CfnStackCreateParameterTypeDef(TypedDict):
    Key: str
    Value: NotRequired[str]


class CfnStackDetailTypeDef(TypedDict):
    StatusMessage: str
    Name: NotRequired[str]
    Id: NotRequired[str]


class CfnStackParameterTypeDef(TypedDict):
    Key: str
    Value: NotRequired[str]


class CfnStackUpdateParameterTypeDef(TypedDict):
    Key: str
    Value: NotRequired[str]


class ShuffleConfigTypeDef(TypedDict):
    Seed: int


class ChannelSpecificationOutputTypeDef(TypedDict):
    Name: str
    SupportedContentTypes: list[str]
    SupportedInputModes: list[TrainingInputModeType]
    Description: NotRequired[str]
    IsRequired: NotRequired[bool]
    SupportedCompressionTypes: NotRequired[list[CompressionTypeType]]


class ChannelSpecificationTypeDef(TypedDict):
    Name: str
    SupportedContentTypes: Sequence[str]
    SupportedInputModes: Sequence[TrainingInputModeType]
    Description: NotRequired[str]
    IsRequired: NotRequired[bool]
    SupportedCompressionTypes: NotRequired[Sequence[CompressionTypeType]]


class CheckpointConfigTypeDef(TypedDict):
    S3Uri: str
    LocalPath: NotRequired[str]


class ClarifyCheckStepMetadataTypeDef(TypedDict):
    CheckType: NotRequired[str]
    BaselineUsedForDriftCheckConstraints: NotRequired[str]
    CalculatedBaselineConstraints: NotRequired[str]
    ModelPackageGroupName: NotRequired[str]
    ViolationReport: NotRequired[str]
    CheckJobArn: NotRequired[str]
    SkipCheck: NotRequired[bool]
    RegisterNewBaseline: NotRequired[bool]


class ClarifyInferenceConfigOutputTypeDef(TypedDict):
    FeaturesAttribute: NotRequired[str]
    ContentTemplate: NotRequired[str]
    MaxRecordCount: NotRequired[int]
    MaxPayloadInMB: NotRequired[int]
    ProbabilityIndex: NotRequired[int]
    LabelIndex: NotRequired[int]
    ProbabilityAttribute: NotRequired[str]
    LabelAttribute: NotRequired[str]
    LabelHeaders: NotRequired[list[str]]
    FeatureHeaders: NotRequired[list[str]]
    FeatureTypes: NotRequired[list[ClarifyFeatureTypeType]]


class ClarifyInferenceConfigTypeDef(TypedDict):
    FeaturesAttribute: NotRequired[str]
    ContentTemplate: NotRequired[str]
    MaxRecordCount: NotRequired[int]
    MaxPayloadInMB: NotRequired[int]
    ProbabilityIndex: NotRequired[int]
    LabelIndex: NotRequired[int]
    ProbabilityAttribute: NotRequired[str]
    LabelAttribute: NotRequired[str]
    LabelHeaders: NotRequired[Sequence[str]]
    FeatureHeaders: NotRequired[Sequence[str]]
    FeatureTypes: NotRequired[Sequence[ClarifyFeatureTypeType]]


class ClarifyShapBaselineConfigTypeDef(TypedDict):
    MimeType: NotRequired[str]
    ShapBaseline: NotRequired[str]
    ShapBaselineUri: NotRequired[str]


class ClarifyTextConfigTypeDef(TypedDict):
    Language: ClarifyTextLanguageType
    Granularity: ClarifyTextGranularityType


class ClusterAutoScalingConfigOutputTypeDef(TypedDict):
    Mode: ClusterAutoScalingModeType
    Status: ClusterAutoScalingStatusType
    AutoScalerType: NotRequired[Literal["Karpenter"]]
    FailureMessage: NotRequired[str]


class ClusterAutoScalingConfigTypeDef(TypedDict):
    Mode: ClusterAutoScalingModeType
    AutoScalerType: NotRequired[Literal["Karpenter"]]


class ClusterCapacityRequirementsOutputTypeDef(TypedDict):
    Spot: NotRequired[dict[str, Any]]
    OnDemand: NotRequired[dict[str, Any]]


class ClusterCapacityRequirementsTypeDef(TypedDict):
    Spot: NotRequired[Mapping[str, Any]]
    OnDemand: NotRequired[Mapping[str, Any]]


class ClusterEbsVolumeConfigTypeDef(TypedDict):
    VolumeSizeInGB: NotRequired[int]
    VolumeKmsKeyId: NotRequired[str]
    RootVolume: NotRequired[bool]


class ClusterEventSummaryTypeDef(TypedDict):
    EventId: str
    ClusterArn: str
    ClusterName: str
    ResourceType: ClusterEventResourceTypeType
    EventTime: datetime
    InstanceGroupName: NotRequired[str]
    InstanceId: NotRequired[str]
    Description: NotRequired[str]


class ClusterLifeCycleConfigTypeDef(TypedDict):
    SourceS3Uri: str
    OnCreate: str


class ClusterInstancePlacementTypeDef(TypedDict):
    AvailabilityZone: NotRequired[str]
    AvailabilityZoneId: NotRequired[str]


class ClusterInstanceStatusDetailsTypeDef(TypedDict):
    Status: ClusterInstanceStatusType
    Message: NotRequired[str]


class ClusterKubernetesTaintTypeDef(TypedDict):
    Key: str
    Effect: ClusterKubernetesTaintEffectType
    Value: NotRequired[str]


class ClusterMetadataTypeDef(TypedDict):
    FailureMessage: NotRequired[str]
    EksRoleAccessEntries: NotRequired[list[str]]
    SlrAccessEntry: NotRequired[str]


UltraServerInfoTypeDef = TypedDict(
    "UltraServerInfoTypeDef",
    {
        "Id": NotRequired[str],
        "Type": NotRequired[str],
    },
)


class ClusterOrchestratorEksConfigTypeDef(TypedDict):
    ClusterArn: str


class ClusterSchedulerConfigSummaryTypeDef(TypedDict):
    ClusterSchedulerConfigArn: str
    ClusterSchedulerConfigId: str
    Name: str
    CreationTime: datetime
    Status: SchedulerResourceStatusType
    ClusterSchedulerConfigVersion: NotRequired[int]
    LastModifiedTime: NotRequired[datetime]
    ClusterArn: NotRequired[str]


class ClusterSummaryTypeDef(TypedDict):
    ClusterArn: str
    ClusterName: str
    CreationTime: datetime
    ClusterStatus: ClusterStatusType
    TrainingPlanArns: NotRequired[list[str]]


class ClusterTieredStorageConfigTypeDef(TypedDict):
    Mode: ClusterConfigModeType
    InstanceMemoryAllocationPercentage: NotRequired[int]


class ContainerConfigOutputTypeDef(TypedDict):
    ContainerArguments: NotRequired[list[str]]
    ContainerEntrypoint: NotRequired[list[str]]
    ContainerEnvironmentVariables: NotRequired[dict[str, str]]


class FileSystemConfigTypeDef(TypedDict):
    MountPath: NotRequired[str]
    DefaultUid: NotRequired[int]
    DefaultGid: NotRequired[int]


class ContainerConfigTypeDef(TypedDict):
    ContainerArguments: NotRequired[Sequence[str]]
    ContainerEntrypoint: NotRequired[Sequence[str]]
    ContainerEnvironmentVariables: NotRequired[Mapping[str, str]]


class CustomImageTypeDef(TypedDict):
    ImageName: str
    AppImageConfigName: str
    ImageVersionNumber: NotRequired[int]


class GitConfigTypeDef(TypedDict):
    RepositoryUrl: str
    Branch: NotRequired[str]
    SecretArn: NotRequired[str]


class CodeRepositoryTypeDef(TypedDict):
    RepositoryUrl: str


class CognitoConfigTypeDef(TypedDict):
    UserPool: str
    ClientId: str


class CognitoMemberDefinitionTypeDef(TypedDict):
    UserPool: str
    UserGroup: str
    ClientId: str


class VectorConfigTypeDef(TypedDict):
    Dimension: int


class CollectionConfigurationOutputTypeDef(TypedDict):
    CollectionName: NotRequired[str]
    CollectionParameters: NotRequired[dict[str, str]]


class CollectionConfigurationTypeDef(TypedDict):
    CollectionName: NotRequired[str]
    CollectionParameters: NotRequired[Mapping[str, str]]


class CompilationJobSummaryTypeDef(TypedDict):
    CompilationJobName: str
    CompilationJobArn: str
    CreationTime: datetime
    CompilationJobStatus: CompilationJobStatusType
    CompilationStartTime: NotRequired[datetime]
    CompilationEndTime: NotRequired[datetime]
    CompilationTargetDevice: NotRequired[TargetDeviceType]
    CompilationTargetPlatformOs: NotRequired[TargetPlatformOsType]
    CompilationTargetPlatformArch: NotRequired[TargetPlatformArchType]
    CompilationTargetPlatformAccelerator: NotRequired[TargetPlatformAcceleratorType]
    LastModifiedTime: NotRequired[datetime]


class ComputeQuotaTargetTypeDef(TypedDict):
    TeamName: str
    FairShareWeight: NotRequired[int]


class ConditionStepMetadataTypeDef(TypedDict):
    Outcome: NotRequired[ConditionOutcomeType]


class MultiModelConfigTypeDef(TypedDict):
    ModelCacheSetting: NotRequired[ModelCacheSettingType]


class ContextSourceTypeDef(TypedDict):
    SourceUri: str
    SourceType: NotRequired[str]
    SourceId: NotRequired[str]


class ContinuousParameterRangeSpecificationTypeDef(TypedDict):
    MinValue: str
    MaxValue: str


class ContinuousParameterRangeTypeDef(TypedDict):
    Name: str
    MinValue: str
    MaxValue: str
    ScalingType: NotRequired[HyperParameterScalingTypeType]


class ConvergenceDetectedTypeDef(TypedDict):
    CompleteOnConvergence: NotRequired[CompleteOnConvergenceType]


class MetadataPropertiesTypeDef(TypedDict):
    CommitId: NotRequired[str]
    Repository: NotRequired[str]
    GeneratedBy: NotRequired[str]
    ProjectId: NotRequired[str]


class ModelDeployConfigTypeDef(TypedDict):
    AutoGenerateEndpointName: NotRequired[bool]
    EndpointName: NotRequired[str]


class InputConfigTypeDef(TypedDict):
    S3Uri: str
    Framework: FrameworkType
    DataInputConfig: NotRequired[str]
    FrameworkVersion: NotRequired[str]


class StoppingConditionTypeDef(TypedDict):
    MaxRuntimeInSeconds: NotRequired[int]
    MaxWaitTimeInSeconds: NotRequired[int]
    MaxPendingTimeInSeconds: NotRequired[int]


class MonitoringStoppingConditionTypeDef(TypedDict):
    MaxRuntimeInSeconds: int


class EdgeOutputConfigTypeDef(TypedDict):
    S3OutputLocation: str
    KmsKeyId: NotRequired[str]
    PresetDeploymentType: NotRequired[Literal["GreengrassV2Component"]]
    PresetDeploymentConfig: NotRequired[str]


class EdgeDeploymentModelConfigTypeDef(TypedDict):
    ModelHandle: str
    EdgePackagingJobName: str


class MetricsConfigTypeDef(TypedDict):
    EnableEnhancedMetrics: NotRequired[bool]
    MetricPublishFrequencyInSeconds: NotRequired[int]


class ThroughputConfigTypeDef(TypedDict):
    ThroughputMode: ThroughputModeType
    ProvisionedReadCapacityUnits: NotRequired[int]
    ProvisionedWriteCapacityUnits: NotRequired[int]


class FlowDefinitionOutputConfigTypeDef(TypedDict):
    S3OutputPath: str
    KmsKeyId: NotRequired[str]


class HumanLoopRequestSourceTypeDef(TypedDict):
    AwsManagedHumanLoopRequestSource: AwsManagedHumanLoopRequestSourceType


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class PresignedUrlAccessConfigTypeDef(TypedDict):
    AcceptEula: NotRequired[bool]
    ExpectedS3Url: NotRequired[str]


class HubS3StorageConfigTypeDef(TypedDict):
    S3OutputPath: NotRequired[str]


class UiTemplateTypeDef(TypedDict):
    Content: str


class CreateImageVersionRequestTypeDef(TypedDict):
    BaseImage: str
    ClientToken: str
    ImageName: str
    Aliases: NotRequired[Sequence[str]]
    VendorGuidance: NotRequired[VendorGuidanceType]
    JobType: NotRequired[JobTypeType]
    MLFramework: NotRequired[str]
    ProgrammingLang: NotRequired[str]
    Processor: NotRequired[ProcessorType]
    Horovod: NotRequired[bool]
    ReleaseNotes: NotRequired[str]


class InferenceComponentRuntimeConfigTypeDef(TypedDict):
    CopyCount: int


class LabelingJobOutputConfigTypeDef(TypedDict):
    S3OutputPath: str
    KmsKeyId: NotRequired[str]
    SnsTopicArn: NotRequired[str]


class LabelingJobStoppingConditionsTypeDef(TypedDict):
    MaxHumanLabeledObjectCount: NotRequired[int]
    MaxPercentageOfInputDatasetLabeled: NotRequired[int]


class ModelCardExportOutputConfigTypeDef(TypedDict):
    S3OutputPath: str


class ModelCardSecurityConfigTypeDef(TypedDict):
    KmsKeyId: NotRequired[str]


class InferenceExecutionConfigTypeDef(TypedDict):
    Mode: InferenceExecutionModeType


class ModelLifeCycleTypeDef(TypedDict):
    Stage: str
    StageStatus: str
    StageDescription: NotRequired[str]


class ModelPackageModelCardTypeDef(TypedDict):
    ModelCardContent: NotRequired[str]
    ModelCardStatus: NotRequired[ModelCardStatusType]


class ModelPackageSecurityConfigTypeDef(TypedDict):
    KmsKeyId: str


class InstanceMetadataServiceConfigurationTypeDef(TypedDict):
    MinimumInstanceMetadataServiceVersion: str


class NotebookInstanceLifecycleHookTypeDef(TypedDict):
    Content: NotRequired[str]


class CreatePartnerAppPresignedUrlRequestTypeDef(TypedDict):
    Arn: str
    ExpiresInSeconds: NotRequired[int]
    SessionExpirationDurationInSeconds: NotRequired[int]


class PartnerAppMaintenanceConfigTypeDef(TypedDict):
    MaintenanceWindowStart: NotRequired[str]


class ParallelismConfigurationTypeDef(TypedDict):
    MaxParallelExecutionSteps: int


class PipelineDefinitionS3LocationTypeDef(TypedDict):
    Bucket: str
    ObjectKey: str
    VersionId: NotRequired[str]


class CreatePresignedDomainUrlRequestTypeDef(TypedDict):
    DomainId: str
    UserProfileName: str
    SessionExpirationDurationInSeconds: NotRequired[int]
    ExpiresInSeconds: NotRequired[int]
    SpaceName: NotRequired[str]
    LandingUri: NotRequired[str]


class CreatePresignedMlflowAppUrlRequestTypeDef(TypedDict):
    Arn: str
    ExpiresInSeconds: NotRequired[int]
    SessionExpirationDurationInSeconds: NotRequired[int]


class CreatePresignedMlflowTrackingServerUrlRequestTypeDef(TypedDict):
    TrackingServerName: str
    ExpiresInSeconds: NotRequired[int]
    SessionExpirationDurationInSeconds: NotRequired[int]


class CreatePresignedNotebookInstanceUrlInputTypeDef(TypedDict):
    NotebookInstanceName: str
    SessionExpirationDurationInSeconds: NotRequired[int]


class ExperimentConfigTypeDef(TypedDict):
    ExperimentName: NotRequired[str]
    TrialName: NotRequired[str]
    TrialComponentDisplayName: NotRequired[str]
    RunName: NotRequired[str]


class ProcessingStoppingConditionTypeDef(TypedDict):
    MaxRuntimeInSeconds: int


class OwnershipSettingsTypeDef(TypedDict):
    OwnerUserProfileName: str


class SpaceSharingSettingsTypeDef(TypedDict):
    SharingType: SharingTypeType


class InfraCheckConfigTypeDef(TypedDict):
    EnableInfraCheck: NotRequired[bool]


class MlflowConfigTypeDef(TypedDict):
    MlflowResourceArn: str
    MlflowExperimentName: NotRequired[str]
    MlflowRunName: NotRequired[str]


class ModelPackageConfigTypeDef(TypedDict):
    ModelPackageGroupArn: str
    SourceModelPackageArn: NotRequired[str]


class OutputDataConfigTypeDef(TypedDict):
    S3OutputPath: str
    KmsKeyId: NotRequired[str]
    CompressionType: NotRequired[OutputCompressionTypeType]


class RemoteDebugConfigTypeDef(TypedDict):
    EnableRemoteDebug: NotRequired[bool]


class RetryStrategyTypeDef(TypedDict):
    MaximumRetryAttempts: int


class ServerlessJobConfigTypeDef(TypedDict):
    BaseModelArn: str
    JobType: ServerlessJobTypeType
    AcceptEula: NotRequired[bool]
    CustomizationTechnique: NotRequired[CustomizationTechniqueType]
    Peft: NotRequired[Literal["LORA"]]
    EvaluationType: NotRequired[EvaluationTypeType]
    EvaluatorArn: NotRequired[str]


class SessionChainingConfigTypeDef(TypedDict):
    EnableSessionTagChaining: NotRequired[bool]


class TensorBoardOutputConfigTypeDef(TypedDict):
    S3OutputPath: str
    LocalPath: NotRequired[str]


class DataProcessingTypeDef(TypedDict):
    InputFilter: NotRequired[str]
    OutputFilter: NotRequired[str]
    JoinSource: NotRequired[JoinSourceType]


class ModelClientConfigTypeDef(TypedDict):
    InvocationsTimeoutInSeconds: NotRequired[int]
    InvocationsMaxRetries: NotRequired[int]


class TransformOutputTypeDef(TypedDict):
    S3OutputPath: str
    Accept: NotRequired[str]
    AssembleWith: NotRequired[AssemblyTypeType]
    KmsKeyId: NotRequired[str]


class TransformResourcesTypeDef(TypedDict):
    InstanceType: TransformInstanceTypeType
    InstanceCount: int
    VolumeKmsKeyId: NotRequired[str]
    TransformAmiVersion: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class TrialComponentArtifactTypeDef(TypedDict):
    Value: str
    MediaType: NotRequired[str]


class TrialComponentParameterValueTypeDef(TypedDict):
    StringValue: NotRequired[str]
    NumberValue: NotRequired[float]


class TrialComponentStatusTypeDef(TypedDict):
    PrimaryStatus: NotRequired[TrialComponentPrimaryStatusType]
    Message: NotRequired[str]


class OidcConfigTypeDef(TypedDict):
    ClientId: str
    ClientSecret: str
    Issuer: str
    AuthorizationEndpoint: str
    TokenEndpoint: str
    UserInfoEndpoint: str
    LogoutEndpoint: str
    JwksUri: str
    Scope: NotRequired[str]
    AuthenticationRequestExtraParams: NotRequired[Mapping[str, str]]


class WorkforceVpcConfigRequestTypeDef(TypedDict):
    VpcId: NotRequired[str]
    SecurityGroupIds: NotRequired[Sequence[str]]
    Subnets: NotRequired[Sequence[str]]


class NotificationConfigurationTypeDef(TypedDict):
    NotificationTopicArn: NotRequired[str]


class EFSFileSystemConfigTypeDef(TypedDict):
    FileSystemId: str
    FileSystemPath: NotRequired[str]


class FSxLustreFileSystemConfigTypeDef(TypedDict):
    FileSystemId: str
    FileSystemPath: NotRequired[str]


class S3FileSystemConfigTypeDef(TypedDict):
    S3Uri: str
    MountPath: NotRequired[str]


class EFSFileSystemTypeDef(TypedDict):
    FileSystemId: str


class FSxLustreFileSystemTypeDef(TypedDict):
    FileSystemId: str


class S3FileSystemTypeDef(TypedDict):
    S3Uri: str


class CustomPosixUserConfigTypeDef(TypedDict):
    Uid: int
    Gid: int


class CustomizedMetricSpecificationTypeDef(TypedDict):
    MetricName: NotRequired[str]
    Namespace: NotRequired[str]
    Statistic: NotRequired[StatisticType]


class DataCaptureConfigSummaryTypeDef(TypedDict):
    EnableCapture: bool
    CaptureStatus: CaptureStatusType
    CurrentSamplingPercentage: int
    DestinationS3Uri: str
    KmsKeyId: str


class DataCatalogConfigTypeDef(TypedDict):
    TableName: str
    Catalog: str
    Database: str


class DataQualityAppSpecificationOutputTypeDef(TypedDict):
    ImageUri: str
    ContainerEntrypoint: NotRequired[list[str]]
    ContainerArguments: NotRequired[list[str]]
    RecordPreprocessorSourceUri: NotRequired[str]
    PostAnalyticsProcessorSourceUri: NotRequired[str]
    Environment: NotRequired[dict[str, str]]


class DataQualityAppSpecificationTypeDef(TypedDict):
    ImageUri: str
    ContainerEntrypoint: NotRequired[Sequence[str]]
    ContainerArguments: NotRequired[Sequence[str]]
    RecordPreprocessorSourceUri: NotRequired[str]
    PostAnalyticsProcessorSourceUri: NotRequired[str]
    Environment: NotRequired[Mapping[str, str]]


class MonitoringConstraintsResourceTypeDef(TypedDict):
    S3Uri: NotRequired[str]


class MonitoringStatisticsResourceTypeDef(TypedDict):
    S3Uri: NotRequired[str]


EndpointInputTypeDef = TypedDict(
    "EndpointInputTypeDef",
    {
        "EndpointName": str,
        "LocalPath": str,
        "S3InputMode": NotRequired[ProcessingS3InputModeType],
        "S3DataDistributionType": NotRequired[ProcessingS3DataDistributionTypeType],
        "FeaturesAttribute": NotRequired[str],
        "InferenceAttribute": NotRequired[str],
        "ProbabilityAttribute": NotRequired[str],
        "ProbabilityThresholdAttribute": NotRequired[float],
        "StartTimeOffset": NotRequired[str],
        "EndTimeOffset": NotRequired[str],
        "ExcludeFeaturesAttribute": NotRequired[str],
    },
)


class DatasetSourceTypeDef(TypedDict):
    DatasetArn: str


class FileSystemDataSourceTypeDef(TypedDict):
    FileSystemId: str
    FileSystemAccessMode: FileSystemAccessModeType
    FileSystemType: FileSystemTypeType
    DirectoryPath: str


class RedshiftDatasetDefinitionTypeDef(TypedDict):
    ClusterId: str
    Database: str
    DbUser: str
    QueryString: str
    ClusterRoleArn: str
    OutputS3Uri: str
    OutputFormat: RedshiftResultFormatType
    KmsKeyId: NotRequired[str]
    OutputCompression: NotRequired[RedshiftResultCompressionTypeType]


class DebugRuleConfigurationOutputTypeDef(TypedDict):
    RuleConfigurationName: str
    RuleEvaluatorImage: str
    LocalPath: NotRequired[str]
    S3OutputPath: NotRequired[str]
    InstanceType: NotRequired[ProcessingInstanceTypeType]
    VolumeSizeInGB: NotRequired[int]
    RuleParameters: NotRequired[dict[str, str]]


class DebugRuleConfigurationTypeDef(TypedDict):
    RuleConfigurationName: str
    RuleEvaluatorImage: str
    LocalPath: NotRequired[str]
    S3OutputPath: NotRequired[str]
    InstanceType: NotRequired[ProcessingInstanceTypeType]
    VolumeSizeInGB: NotRequired[int]
    RuleParameters: NotRequired[Mapping[str, str]]


class DebugRuleEvaluationStatusTypeDef(TypedDict):
    RuleConfigurationName: NotRequired[str]
    RuleEvaluationJobArn: NotRequired[str]
    RuleEvaluationStatus: NotRequired[RuleEvaluationStatusType]
    StatusDetails: NotRequired[str]
    LastModifiedTime: NotRequired[datetime]


class DefaultEbsStorageSettingsTypeDef(TypedDict):
    DefaultEbsVolumeSizeInGb: int
    MaximumEbsVolumeSizeInGb: int


class DeleteActionRequestTypeDef(TypedDict):
    ActionName: str


class DeleteAlgorithmInputTypeDef(TypedDict):
    AlgorithmName: str


class DeleteAppImageConfigRequestTypeDef(TypedDict):
    AppImageConfigName: str


class DeleteAppRequestTypeDef(TypedDict):
    DomainId: str
    AppType: AppTypeType
    AppName: str
    UserProfileName: NotRequired[str]
    SpaceName: NotRequired[str]


class DeleteAssociationRequestTypeDef(TypedDict):
    SourceArn: str
    DestinationArn: str


class DeleteClusterRequestTypeDef(TypedDict):
    ClusterName: str


class DeleteClusterSchedulerConfigRequestTypeDef(TypedDict):
    ClusterSchedulerConfigId: str


class DeleteCodeRepositoryInputTypeDef(TypedDict):
    CodeRepositoryName: str


class DeleteCompilationJobRequestTypeDef(TypedDict):
    CompilationJobName: str


class DeleteComputeQuotaRequestTypeDef(TypedDict):
    ComputeQuotaId: str


class DeleteContextRequestTypeDef(TypedDict):
    ContextName: str


class DeleteDataQualityJobDefinitionRequestTypeDef(TypedDict):
    JobDefinitionName: str


class DeleteDeviceFleetRequestTypeDef(TypedDict):
    DeviceFleetName: str


class RetentionPolicyTypeDef(TypedDict):
    HomeEfsFileSystem: NotRequired[RetentionTypeType]


class DeleteEdgeDeploymentPlanRequestTypeDef(TypedDict):
    EdgeDeploymentPlanName: str


class DeleteEdgeDeploymentStageRequestTypeDef(TypedDict):
    EdgeDeploymentPlanName: str
    StageName: str


class DeleteEndpointConfigInputTypeDef(TypedDict):
    EndpointConfigName: str


class DeleteEndpointInputTypeDef(TypedDict):
    EndpointName: str


class DeleteExperimentRequestTypeDef(TypedDict):
    ExperimentName: str


class DeleteFeatureGroupRequestTypeDef(TypedDict):
    FeatureGroupName: str


class DeleteFlowDefinitionRequestTypeDef(TypedDict):
    FlowDefinitionName: str


class DeleteHubContentReferenceRequestTypeDef(TypedDict):
    HubName: str
    HubContentType: HubContentTypeType
    HubContentName: str


class DeleteHubContentRequestTypeDef(TypedDict):
    HubName: str
    HubContentType: HubContentTypeType
    HubContentName: str
    HubContentVersion: str


class DeleteHubRequestTypeDef(TypedDict):
    HubName: str


class DeleteHumanTaskUiRequestTypeDef(TypedDict):
    HumanTaskUiName: str


class DeleteHyperParameterTuningJobRequestTypeDef(TypedDict):
    HyperParameterTuningJobName: str


class DeleteImageRequestTypeDef(TypedDict):
    ImageName: str


class DeleteImageVersionRequestTypeDef(TypedDict):
    ImageName: str
    Version: NotRequired[int]
    Alias: NotRequired[str]


class DeleteInferenceComponentInputTypeDef(TypedDict):
    InferenceComponentName: str


class DeleteInferenceExperimentRequestTypeDef(TypedDict):
    Name: str


class DeleteMlflowAppRequestTypeDef(TypedDict):
    Arn: str


class DeleteMlflowTrackingServerRequestTypeDef(TypedDict):
    TrackingServerName: str


class DeleteModelBiasJobDefinitionRequestTypeDef(TypedDict):
    JobDefinitionName: str


class DeleteModelCardRequestTypeDef(TypedDict):
    ModelCardName: str


class DeleteModelExplainabilityJobDefinitionRequestTypeDef(TypedDict):
    JobDefinitionName: str


class DeleteModelInputTypeDef(TypedDict):
    ModelName: str


class DeleteModelPackageGroupInputTypeDef(TypedDict):
    ModelPackageGroupName: str


class DeleteModelPackageGroupPolicyInputTypeDef(TypedDict):
    ModelPackageGroupName: str


class DeleteModelPackageInputTypeDef(TypedDict):
    ModelPackageName: str


class DeleteModelQualityJobDefinitionRequestTypeDef(TypedDict):
    JobDefinitionName: str


class DeleteMonitoringScheduleRequestTypeDef(TypedDict):
    MonitoringScheduleName: str


class DeleteNotebookInstanceInputTypeDef(TypedDict):
    NotebookInstanceName: str


class DeleteNotebookInstanceLifecycleConfigInputTypeDef(TypedDict):
    NotebookInstanceLifecycleConfigName: str


class DeleteOptimizationJobRequestTypeDef(TypedDict):
    OptimizationJobName: str


class DeletePartnerAppRequestTypeDef(TypedDict):
    Arn: str
    ClientToken: NotRequired[str]


class DeletePipelineRequestTypeDef(TypedDict):
    PipelineName: str
    ClientRequestToken: str


class DeleteProcessingJobRequestTypeDef(TypedDict):
    ProcessingJobName: str


class DeleteProjectInputTypeDef(TypedDict):
    ProjectName: str


class DeleteSpaceRequestTypeDef(TypedDict):
    DomainId: str
    SpaceName: str


class DeleteStudioLifecycleConfigRequestTypeDef(TypedDict):
    StudioLifecycleConfigName: str


class DeleteTagsInputTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class DeleteTrainingJobRequestTypeDef(TypedDict):
    TrainingJobName: str


class DeleteTrialComponentRequestTypeDef(TypedDict):
    TrialComponentName: str


class DeleteTrialRequestTypeDef(TypedDict):
    TrialName: str


class DeleteUserProfileRequestTypeDef(TypedDict):
    DomainId: str
    UserProfileName: str


class DeleteWorkforceRequestTypeDef(TypedDict):
    WorkforceName: str


class DeleteWorkteamRequestTypeDef(TypedDict):
    WorkteamName: str


class DeployedImageTypeDef(TypedDict):
    SpecifiedImage: NotRequired[str]
    ResolvedImage: NotRequired[str]
    ResolutionTime: NotRequired[datetime]


class RealTimeInferenceRecommendationTypeDef(TypedDict):
    RecommendationId: str
    InstanceType: ProductionVariantInstanceTypeType
    Environment: NotRequired[dict[str, str]]


class DeviceSelectionConfigOutputTypeDef(TypedDict):
    DeviceSubsetType: DeviceSubsetTypeType
    Percentage: NotRequired[int]
    DeviceNames: NotRequired[list[str]]
    DeviceNameContains: NotRequired[str]


class EdgeDeploymentConfigTypeDef(TypedDict):
    FailureHandlingPolicy: FailureHandlingPolicyType


class EdgeDeploymentStatusTypeDef(TypedDict):
    StageStatus: StageStatusType
    EdgeDeploymentSuccessInStage: int
    EdgeDeploymentPendingInStage: int
    EdgeDeploymentFailedInStage: int
    EdgeDeploymentStatusMessage: NotRequired[str]
    EdgeDeploymentStageStartTime: NotRequired[datetime]


class DeregisterDevicesRequestTypeDef(TypedDict):
    DeviceFleetName: str
    DeviceNames: Sequence[str]


class DerivedInformationTypeDef(TypedDict):
    DerivedDataInputConfig: NotRequired[str]


class DescribeActionRequestTypeDef(TypedDict):
    ActionName: str


class DescribeAlgorithmInputTypeDef(TypedDict):
    AlgorithmName: str


class DescribeAppImageConfigRequestTypeDef(TypedDict):
    AppImageConfigName: str


class DescribeAppRequestTypeDef(TypedDict):
    DomainId: str
    AppType: AppTypeType
    AppName: str
    UserProfileName: NotRequired[str]
    SpaceName: NotRequired[str]


class DescribeArtifactRequestTypeDef(TypedDict):
    ArtifactArn: str


class DescribeAutoMLJobRequestTypeDef(TypedDict):
    AutoMLJobName: str


class ModelDeployResultTypeDef(TypedDict):
    EndpointName: NotRequired[str]


class DescribeAutoMLJobV2RequestTypeDef(TypedDict):
    AutoMLJobName: str


class DescribeClusterEventRequestTypeDef(TypedDict):
    EventId: str
    ClusterName: str


class DescribeClusterNodeRequestTypeDef(TypedDict):
    ClusterName: str
    NodeId: NotRequired[str]
    NodeLogicalId: NotRequired[str]


class DescribeClusterRequestTypeDef(TypedDict):
    ClusterName: str


class DescribeClusterSchedulerConfigRequestTypeDef(TypedDict):
    ClusterSchedulerConfigId: str
    ClusterSchedulerConfigVersion: NotRequired[int]


class DescribeCodeRepositoryInputTypeDef(TypedDict):
    CodeRepositoryName: str


class DescribeCompilationJobRequestTypeDef(TypedDict):
    CompilationJobName: str


class ModelArtifactsTypeDef(TypedDict):
    S3ModelArtifacts: str


class ModelDigestsTypeDef(TypedDict):
    ArtifactDigest: NotRequired[str]


class NeoVpcConfigOutputTypeDef(TypedDict):
    SecurityGroupIds: list[str]
    Subnets: list[str]


class DescribeComputeQuotaRequestTypeDef(TypedDict):
    ComputeQuotaId: str
    ComputeQuotaVersion: NotRequired[int]


class DescribeContextRequestTypeDef(TypedDict):
    ContextName: str


class DescribeDataQualityJobDefinitionRequestTypeDef(TypedDict):
    JobDefinitionName: str


class DescribeDeviceFleetRequestTypeDef(TypedDict):
    DeviceFleetName: str


class DescribeDeviceRequestTypeDef(TypedDict):
    DeviceName: str
    DeviceFleetName: str
    NextToken: NotRequired[str]


class EdgeModelTypeDef(TypedDict):
    ModelName: str
    ModelVersion: str
    LatestSampleTime: NotRequired[datetime]
    LatestInference: NotRequired[datetime]


class DescribeDomainRequestTypeDef(TypedDict):
    DomainId: str


class DescribeEdgeDeploymentPlanRequestTypeDef(TypedDict):
    EdgeDeploymentPlanName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribeEdgePackagingJobRequestTypeDef(TypedDict):
    EdgePackagingJobName: str


EdgePresetDeploymentOutputTypeDef = TypedDict(
    "EdgePresetDeploymentOutputTypeDef",
    {
        "Type": Literal["GreengrassV2Component"],
        "Artifact": NotRequired[str],
        "Status": NotRequired[EdgePresetDeploymentStatusType],
        "StatusMessage": NotRequired[str],
    },
)


class DescribeEndpointConfigInputTypeDef(TypedDict):
    EndpointConfigName: str


class DescribeEndpointInputTypeDef(TypedDict):
    EndpointName: str


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class DescribeExperimentRequestTypeDef(TypedDict):
    ExperimentName: str


class ExperimentSourceTypeDef(TypedDict):
    SourceArn: str
    SourceType: NotRequired[str]


class DescribeFeatureGroupRequestTypeDef(TypedDict):
    FeatureGroupName: str
    NextToken: NotRequired[str]


class LastUpdateStatusTypeDef(TypedDict):
    Status: LastUpdateStatusValueType
    FailureReason: NotRequired[str]


class OfflineStoreStatusTypeDef(TypedDict):
    Status: OfflineStoreStatusValueType
    BlockedReason: NotRequired[str]


class ThroughputConfigDescriptionTypeDef(TypedDict):
    ThroughputMode: ThroughputModeType
    ProvisionedReadCapacityUnits: NotRequired[int]
    ProvisionedWriteCapacityUnits: NotRequired[int]


class DescribeFeatureMetadataRequestTypeDef(TypedDict):
    FeatureGroupName: str
    FeatureName: str


class FeatureParameterTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


class DescribeFlowDefinitionRequestTypeDef(TypedDict):
    FlowDefinitionName: str


class DescribeHubContentRequestTypeDef(TypedDict):
    HubName: str
    HubContentType: HubContentTypeType
    HubContentName: str
    HubContentVersion: NotRequired[str]


class HubContentDependencyTypeDef(TypedDict):
    DependencyOriginPath: NotRequired[str]
    DependencyCopyPath: NotRequired[str]


class DescribeHubRequestTypeDef(TypedDict):
    HubName: str


class DescribeHumanTaskUiRequestTypeDef(TypedDict):
    HumanTaskUiName: str


class UiTemplateInfoTypeDef(TypedDict):
    Url: NotRequired[str]
    ContentSha256: NotRequired[str]


class DescribeHyperParameterTuningJobRequestTypeDef(TypedDict):
    HyperParameterTuningJobName: str


class HyperParameterTuningJobCompletionDetailsTypeDef(TypedDict):
    NumberOfTrainingJobsObjectiveNotImproving: NotRequired[int]
    ConvergenceDetectedTime: NotRequired[datetime]


class HyperParameterTuningJobConsumedResourcesTypeDef(TypedDict):
    RuntimeInSeconds: NotRequired[int]


class ObjectiveStatusCountersTypeDef(TypedDict):
    Succeeded: NotRequired[int]
    Pending: NotRequired[int]
    Failed: NotRequired[int]


class TrainingJobStatusCountersTypeDef(TypedDict):
    Completed: NotRequired[int]
    InProgress: NotRequired[int]
    RetryableError: NotRequired[int]
    NonRetryableError: NotRequired[int]
    Stopped: NotRequired[int]


class DescribeImageRequestTypeDef(TypedDict):
    ImageName: str


class DescribeImageVersionRequestTypeDef(TypedDict):
    ImageName: str
    Version: NotRequired[int]
    Alias: NotRequired[str]


class DescribeInferenceComponentInputTypeDef(TypedDict):
    InferenceComponentName: str


class InferenceComponentRuntimeConfigSummaryTypeDef(TypedDict):
    DesiredCopyCount: NotRequired[int]
    CurrentCopyCount: NotRequired[int]


class DescribeInferenceExperimentRequestTypeDef(TypedDict):
    Name: str


class EndpointMetadataTypeDef(TypedDict):
    EndpointName: str
    EndpointConfigName: NotRequired[str]
    EndpointStatus: NotRequired[EndpointStatusType]
    FailureReason: NotRequired[str]


class InferenceExperimentScheduleOutputTypeDef(TypedDict):
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]


class DescribeInferenceRecommendationsJobRequestTypeDef(TypedDict):
    JobName: str


class DescribeLabelingJobRequestTypeDef(TypedDict):
    LabelingJobName: str


class LabelCountersTypeDef(TypedDict):
    TotalLabeled: NotRequired[int]
    HumanLabeled: NotRequired[int]
    MachineLabeled: NotRequired[int]
    FailedNonRetryableError: NotRequired[int]
    Unlabeled: NotRequired[int]


class LabelingJobOutputTypeDef(TypedDict):
    OutputDatasetS3Uri: str
    FinalActiveLearningModelArn: NotRequired[str]


class DescribeLineageGroupRequestTypeDef(TypedDict):
    LineageGroupName: str


class DescribeMlflowAppRequestTypeDef(TypedDict):
    Arn: str


class DescribeMlflowTrackingServerRequestTypeDef(TypedDict):
    TrackingServerName: str


class DescribeModelBiasJobDefinitionRequestTypeDef(TypedDict):
    JobDefinitionName: str


class ModelBiasAppSpecificationOutputTypeDef(TypedDict):
    ImageUri: str
    ConfigUri: str
    Environment: NotRequired[dict[str, str]]


class DescribeModelCardExportJobRequestTypeDef(TypedDict):
    ModelCardExportJobArn: str


class ModelCardExportArtifactsTypeDef(TypedDict):
    S3ExportArtifacts: str


class DescribeModelCardRequestTypeDef(TypedDict):
    ModelCardName: str
    ModelCardVersion: NotRequired[int]


class DescribeModelExplainabilityJobDefinitionRequestTypeDef(TypedDict):
    JobDefinitionName: str


class ModelExplainabilityAppSpecificationOutputTypeDef(TypedDict):
    ImageUri: str
    ConfigUri: str
    Environment: NotRequired[dict[str, str]]


class DescribeModelInputTypeDef(TypedDict):
    ModelName: str


class DescribeModelPackageGroupInputTypeDef(TypedDict):
    ModelPackageGroupName: str


class DescribeModelPackageInputTypeDef(TypedDict):
    ModelPackageName: str


class DescribeModelQualityJobDefinitionRequestTypeDef(TypedDict):
    JobDefinitionName: str


class ModelQualityAppSpecificationOutputTypeDef(TypedDict):
    ImageUri: str
    ContainerEntrypoint: NotRequired[list[str]]
    ContainerArguments: NotRequired[list[str]]
    RecordPreprocessorSourceUri: NotRequired[str]
    PostAnalyticsProcessorSourceUri: NotRequired[str]
    ProblemType: NotRequired[MonitoringProblemTypeType]
    Environment: NotRequired[dict[str, str]]


class DescribeMonitoringScheduleRequestTypeDef(TypedDict):
    MonitoringScheduleName: str


class MonitoringExecutionSummaryTypeDef(TypedDict):
    MonitoringScheduleName: str
    ScheduledTime: datetime
    CreationTime: datetime
    LastModifiedTime: datetime
    MonitoringExecutionStatus: ExecutionStatusType
    ProcessingJobArn: NotRequired[str]
    EndpointName: NotRequired[str]
    FailureReason: NotRequired[str]
    MonitoringJobDefinitionName: NotRequired[str]
    MonitoringType: NotRequired[MonitoringTypeType]


class DescribeNotebookInstanceInputTypeDef(TypedDict):
    NotebookInstanceName: str


class DescribeNotebookInstanceLifecycleConfigInputTypeDef(TypedDict):
    NotebookInstanceLifecycleConfigName: str


class DescribeOptimizationJobRequestTypeDef(TypedDict):
    OptimizationJobName: str


class OptimizationOutputTypeDef(TypedDict):
    RecommendedInferenceImage: NotRequired[str]


class OptimizationVpcConfigOutputTypeDef(TypedDict):
    SecurityGroupIds: list[str]
    Subnets: list[str]


class DescribePartnerAppRequestTypeDef(TypedDict):
    Arn: str
    IncludeAvailableUpgrade: NotRequired[bool]


class ErrorInfoTypeDef(TypedDict):
    Code: NotRequired[str]
    Reason: NotRequired[str]


class DescribePipelineDefinitionForExecutionRequestTypeDef(TypedDict):
    PipelineExecutionArn: str


class DescribePipelineExecutionRequestTypeDef(TypedDict):
    PipelineExecutionArn: str


class MLflowConfigurationTypeDef(TypedDict):
    MlflowResourceArn: NotRequired[str]
    MlflowExperimentName: NotRequired[str]


class PipelineExperimentConfigTypeDef(TypedDict):
    ExperimentName: NotRequired[str]
    TrialName: NotRequired[str]


class DescribePipelineRequestTypeDef(TypedDict):
    PipelineName: str
    PipelineVersionId: NotRequired[int]


class DescribeProcessingJobRequestTypeDef(TypedDict):
    ProcessingJobName: str


class DescribeProjectInputTypeDef(TypedDict):
    ProjectName: str


class ServiceCatalogProvisionedProductDetailsTypeDef(TypedDict):
    ProvisionedProductId: NotRequired[str]
    ProvisionedProductStatusMessage: NotRequired[str]


class DescribeReservedCapacityRequestTypeDef(TypedDict):
    ReservedCapacityArn: str


class UltraServerSummaryTypeDef(TypedDict):
    UltraServerType: str
    InstanceType: ReservedCapacityInstanceTypeType
    UltraServerCount: NotRequired[int]
    AvailableSpareInstanceCount: NotRequired[int]
    UnhealthyInstanceCount: NotRequired[int]


class DescribeSpaceRequestTypeDef(TypedDict):
    DomainId: str
    SpaceName: str


class DescribeStudioLifecycleConfigRequestTypeDef(TypedDict):
    StudioLifecycleConfigName: str


class DescribeSubscribedWorkteamRequestTypeDef(TypedDict):
    WorkteamArn: str


class SubscribedWorkteamTypeDef(TypedDict):
    WorkteamArn: str
    MarketplaceTitle: NotRequired[str]
    SellerName: NotRequired[str]
    MarketplaceDescription: NotRequired[str]
    ListingId: NotRequired[str]


class DescribeTrainingJobRequestTypeDef(TypedDict):
    TrainingJobName: str


class MetricDataTypeDef(TypedDict):
    MetricName: NotRequired[str]
    Value: NotRequired[float]
    Timestamp: NotRequired[datetime]


class MlflowDetailsTypeDef(TypedDict):
    MlflowExperimentId: NotRequired[str]
    MlflowRunId: NotRequired[str]


class ProfilerConfigOutputTypeDef(TypedDict):
    S3OutputPath: NotRequired[str]
    ProfilingIntervalInMilliseconds: NotRequired[int]
    ProfilingParameters: NotRequired[dict[str, str]]
    DisableProfiler: NotRequired[bool]


class ProfilerRuleConfigurationOutputTypeDef(TypedDict):
    RuleConfigurationName: str
    RuleEvaluatorImage: str
    LocalPath: NotRequired[str]
    S3OutputPath: NotRequired[str]
    InstanceType: NotRequired[ProcessingInstanceTypeType]
    VolumeSizeInGB: NotRequired[int]
    RuleParameters: NotRequired[dict[str, str]]


class ProfilerRuleEvaluationStatusTypeDef(TypedDict):
    RuleConfigurationName: NotRequired[str]
    RuleEvaluationJobArn: NotRequired[str]
    RuleEvaluationStatus: NotRequired[RuleEvaluationStatusType]
    StatusDetails: NotRequired[str]
    LastModifiedTime: NotRequired[datetime]


class SecondaryStatusTransitionTypeDef(TypedDict):
    Status: SecondaryStatusType
    StartTime: datetime
    EndTime: NotRequired[datetime]
    StatusMessage: NotRequired[str]


class TrainingProgressInfoTypeDef(TypedDict):
    TotalStepCountPerEpoch: NotRequired[int]
    CurrentStep: NotRequired[int]
    CurrentEpoch: NotRequired[int]
    MaxEpoch: NotRequired[int]


class WarmPoolStatusTypeDef(TypedDict):
    Status: WarmPoolResourceStatusType
    ResourceRetainedBillableTimeInSeconds: NotRequired[int]
    ReusedByJob: NotRequired[str]


class DescribeTrainingPlanRequestTypeDef(TypedDict):
    TrainingPlanName: str


class ReservedCapacitySummaryTypeDef(TypedDict):
    ReservedCapacityArn: str
    InstanceType: ReservedCapacityInstanceTypeType
    TotalInstanceCount: int
    Status: ReservedCapacityStatusType
    ReservedCapacityType: NotRequired[ReservedCapacityTypeType]
    UltraServerType: NotRequired[str]
    UltraServerCount: NotRequired[int]
    AvailabilityZone: NotRequired[str]
    DurationHours: NotRequired[int]
    DurationMinutes: NotRequired[int]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]


class DescribeTransformJobRequestTypeDef(TypedDict):
    TransformJobName: str


class DescribeTrialComponentRequestTypeDef(TypedDict):
    TrialComponentName: str


class TrialComponentMetricSummaryTypeDef(TypedDict):
    MetricName: NotRequired[str]
    SourceArn: NotRequired[str]
    TimeStamp: NotRequired[datetime]
    Max: NotRequired[float]
    Min: NotRequired[float]
    Last: NotRequired[float]
    Count: NotRequired[int]
    Avg: NotRequired[float]
    StdDev: NotRequired[float]


class TrialComponentSourceTypeDef(TypedDict):
    SourceArn: str
    SourceType: NotRequired[str]


class DescribeTrialRequestTypeDef(TypedDict):
    TrialName: str


class TrialSourceTypeDef(TypedDict):
    SourceArn: str
    SourceType: NotRequired[str]


class DescribeUserProfileRequestTypeDef(TypedDict):
    DomainId: str
    UserProfileName: str


class DescribeWorkforceRequestTypeDef(TypedDict):
    WorkforceName: str


class DescribeWorkteamRequestTypeDef(TypedDict):
    WorkteamName: str


class ProductionVariantServerlessUpdateConfigTypeDef(TypedDict):
    MaxConcurrency: NotRequired[int]
    ProvisionedConcurrency: NotRequired[int]


class DetachClusterNodeVolumeRequestTypeDef(TypedDict):
    ClusterArn: str
    NodeId: str
    VolumeId: str


class DeviceDeploymentSummaryTypeDef(TypedDict):
    EdgeDeploymentPlanArn: str
    EdgeDeploymentPlanName: str
    StageName: str
    DeviceName: str
    DeviceArn: str
    DeployedStageName: NotRequired[str]
    DeviceFleetName: NotRequired[str]
    DeviceDeploymentStatus: NotRequired[DeviceDeploymentStatusType]
    DeviceDeploymentStatusMessage: NotRequired[str]
    Description: NotRequired[str]
    DeploymentStartTime: NotRequired[datetime]


class DeviceFleetSummaryTypeDef(TypedDict):
    DeviceFleetArn: str
    DeviceFleetName: str
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]


class DeviceSelectionConfigTypeDef(TypedDict):
    DeviceSubsetType: DeviceSubsetTypeType
    Percentage: NotRequired[int]
    DeviceNames: NotRequired[Sequence[str]]
    DeviceNameContains: NotRequired[str]


class DeviceStatsTypeDef(TypedDict):
    ConnectedDeviceCount: int
    RegisteredDeviceCount: int


class EdgeModelSummaryTypeDef(TypedDict):
    ModelName: str
    ModelVersion: str


class DeviceTypeDef(TypedDict):
    DeviceName: str
    Description: NotRequired[str]
    IotThingName: NotRequired[str]


class DisassociateTrialComponentRequestTypeDef(TypedDict):
    TrialComponentName: str
    TrialName: str


class DockerSettingsOutputTypeDef(TypedDict):
    EnableDockerAccess: NotRequired[FeatureStatusType]
    VpcOnlyTrustedAccounts: NotRequired[list[str]]
    RootlessDocker: NotRequired[FeatureStatusType]


class DockerSettingsTypeDef(TypedDict):
    EnableDockerAccess: NotRequired[FeatureStatusType]
    VpcOnlyTrustedAccounts: NotRequired[Sequence[str]]
    RootlessDocker: NotRequired[FeatureStatusType]


class DomainDetailsTypeDef(TypedDict):
    DomainArn: NotRequired[str]
    DomainId: NotRequired[str]
    DomainName: NotRequired[str]
    Status: NotRequired[DomainStatusType]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    Url: NotRequired[str]


class TrustedIdentityPropagationSettingsTypeDef(TypedDict):
    Status: FeatureStatusType


class UnifiedStudioSettingsTypeDef(TypedDict):
    StudioWebPortalAccess: NotRequired[FeatureStatusType]
    DomainAccountId: NotRequired[str]
    DomainRegion: NotRequired[str]
    DomainId: NotRequired[str]
    ProjectId: NotRequired[str]
    EnvironmentId: NotRequired[str]
    ProjectS3Path: NotRequired[str]
    SingleSignOnApplicationArn: NotRequired[str]


class FileSourceTypeDef(TypedDict):
    S3Uri: str
    ContentType: NotRequired[str]
    ContentDigest: NotRequired[str]


class EMRStepMetadataTypeDef(TypedDict):
    ClusterId: NotRequired[str]
    StepId: NotRequired[str]
    StepName: NotRequired[str]
    LogFilePath: NotRequired[str]


class EbsStorageSettingsTypeDef(TypedDict):
    EbsVolumeSizeInGb: int


class Ec2CapacityReservationTypeDef(TypedDict):
    Ec2CapacityReservationId: NotRequired[str]
    TotalInstanceCount: NotRequired[int]
    AvailableInstanceCount: NotRequired[int]
    UsedByCurrentEndpoint: NotRequired[int]


class EdgeDeploymentPlanSummaryTypeDef(TypedDict):
    EdgeDeploymentPlanArn: str
    EdgeDeploymentPlanName: str
    DeviceFleetName: str
    EdgeDeploymentSuccess: int
    EdgeDeploymentPending: int
    EdgeDeploymentFailed: int
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]


class EdgeModelStatTypeDef(TypedDict):
    ModelName: str
    ModelVersion: str
    OfflineDeviceCount: int
    ConnectedDeviceCount: int
    ActiveDeviceCount: int
    SamplingDeviceCount: int


class EdgePackagingJobSummaryTypeDef(TypedDict):
    EdgePackagingJobArn: str
    EdgePackagingJobName: str
    EdgePackagingJobStatus: EdgePackagingJobStatusType
    CompilationJobName: NotRequired[str]
    ModelName: NotRequired[str]
    ModelVersion: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]


class EdgeTypeDef(TypedDict):
    SourceArn: NotRequired[str]
    DestinationArn: NotRequired[str]
    AssociationType: NotRequired[AssociationEdgeTypeType]


class EmrSettingsOutputTypeDef(TypedDict):
    AssumableRoleArns: NotRequired[list[str]]
    ExecutionRoleArns: NotRequired[list[str]]


class EmrSettingsTypeDef(TypedDict):
    AssumableRoleArns: NotRequired[Sequence[str]]
    ExecutionRoleArns: NotRequired[Sequence[str]]


class EndpointConfigStepMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]


class EndpointConfigSummaryTypeDef(TypedDict):
    EndpointConfigName: str
    EndpointConfigArn: str
    CreationTime: datetime


class EndpointInfoTypeDef(TypedDict):
    EndpointName: NotRequired[str]


class ProductionVariantServerlessConfigTypeDef(TypedDict):
    MemorySizeInMB: int
    MaxConcurrency: int
    ProvisionedConcurrency: NotRequired[int]


class InferenceMetricsTypeDef(TypedDict):
    MaxInvocations: int
    ModelLatency: int


class EndpointStepMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]


class EndpointSummaryTypeDef(TypedDict):
    EndpointName: str
    EndpointArn: str
    CreationTime: datetime
    LastModifiedTime: datetime
    EndpointStatus: EndpointStatusType


class FSxLustreConfigTypeDef(TypedDict):
    SizeInGiB: int
    PerUnitStorageThroughput: int


class EnvironmentParameterTypeDef(TypedDict):
    Key: str
    ValueType: str
    Value: str


class InstanceGroupScalingMetadataTypeDef(TypedDict):
    InstanceCount: NotRequired[int]
    TargetCount: NotRequired[int]
    MinCount: NotRequired[int]
    FailureMessage: NotRequired[str]


class FailStepMetadataTypeDef(TypedDict):
    ErrorMessage: NotRequired[str]


class FilterTypeDef(TypedDict):
    Name: str
    Operator: NotRequired[OperatorType]
    Value: NotRequired[str]


FinalHyperParameterTuningJobObjectiveMetricTypeDef = TypedDict(
    "FinalHyperParameterTuningJobObjectiveMetricTypeDef",
    {
        "MetricName": str,
        "Value": float,
        "Type": NotRequired[HyperParameterTuningJobObjectiveTypeType],
    },
)


class FlowDefinitionSummaryTypeDef(TypedDict):
    FlowDefinitionName: str
    FlowDefinitionArn: str
    FlowDefinitionStatus: FlowDefinitionStatusType
    CreationTime: datetime
    FailureReason: NotRequired[str]


class GetDeviceFleetReportRequestTypeDef(TypedDict):
    DeviceFleetName: str


class GetLineageGroupPolicyRequestTypeDef(TypedDict):
    LineageGroupName: str


class GetModelPackageGroupPolicyInputTypeDef(TypedDict):
    ModelPackageGroupName: str


class ScalingPolicyObjectiveTypeDef(TypedDict):
    MinInvocationsPerMinute: NotRequired[int]
    MaxInvocationsPerMinute: NotRequired[int]


class ScalingPolicyMetricTypeDef(TypedDict):
    InvocationsPerInstance: NotRequired[int]
    ModelLatency: NotRequired[int]


class PropertyNameSuggestionTypeDef(TypedDict):
    PropertyName: NotRequired[str]


class GitConfigForUpdateTypeDef(TypedDict):
    SecretArn: NotRequired[str]


class HiddenSageMakerImageOutputTypeDef(TypedDict):
    SageMakerImageName: NotRequired[Literal["sagemaker_distribution"]]
    VersionAliases: NotRequired[list[str]]


class HiddenSageMakerImageTypeDef(TypedDict):
    SageMakerImageName: NotRequired[Literal["sagemaker_distribution"]]
    VersionAliases: NotRequired[Sequence[str]]


class HolidayConfigAttributesTypeDef(TypedDict):
    CountryCode: NotRequired[str]


class HubAccessConfigTypeDef(TypedDict):
    HubContentArn: str


class HubContentInfoTypeDef(TypedDict):
    HubContentName: str
    HubContentArn: str
    HubContentVersion: str
    HubContentType: HubContentTypeType
    DocumentSchemaVersion: str
    HubContentStatus: HubContentStatusType
    CreationTime: datetime
    SageMakerPublicHubContentArn: NotRequired[str]
    HubContentDisplayName: NotRequired[str]
    HubContentDescription: NotRequired[str]
    SupportStatus: NotRequired[HubContentSupportStatusType]
    HubContentSearchKeywords: NotRequired[list[str]]
    OriginalCreationTime: NotRequired[datetime]


class HubInfoTypeDef(TypedDict):
    HubName: str
    HubArn: str
    HubStatus: HubStatusType
    CreationTime: datetime
    LastModifiedTime: datetime
    HubDisplayName: NotRequired[str]
    HubDescription: NotRequired[str]
    HubSearchKeywords: NotRequired[list[str]]


class HumanLoopActivationConditionsConfigTypeDef(TypedDict):
    HumanLoopActivationConditions: str


class UiConfigTypeDef(TypedDict):
    UiTemplateS3Uri: NotRequired[str]
    HumanTaskUiArn: NotRequired[str]


class HumanTaskUiSummaryTypeDef(TypedDict):
    HumanTaskUiName: str
    HumanTaskUiArn: str
    CreationTime: datetime


HyperParameterTuningJobObjectiveTypeDef = TypedDict(
    "HyperParameterTuningJobObjectiveTypeDef",
    {
        "Type": HyperParameterTuningJobObjectiveTypeType,
        "MetricName": str,
    },
)


class HyperParameterTuningInstanceConfigTypeDef(TypedDict):
    InstanceType: TrainingInstanceTypeType
    InstanceCount: int
    VolumeSizeInGB: int


class ResourceLimitsTypeDef(TypedDict):
    MaxParallelTrainingJobs: int
    MaxNumberOfTrainingJobs: NotRequired[int]
    MaxRuntimeInSeconds: NotRequired[int]


class HyperbandStrategyConfigTypeDef(TypedDict):
    MinResource: NotRequired[int]
    MaxResource: NotRequired[int]


class ParentHyperParameterTuningJobTypeDef(TypedDict):
    HyperParameterTuningJobName: NotRequired[str]


class IamIdentityTypeDef(TypedDict):
    Arn: NotRequired[str]
    PrincipalId: NotRequired[str]
    SourceIdentity: NotRequired[str]


class IamPolicyConstraintsTypeDef(TypedDict):
    SourceIp: NotRequired[EnabledOrDisabledType]
    VpcSourceIp: NotRequired[EnabledOrDisabledType]


class RepositoryAuthConfigTypeDef(TypedDict):
    RepositoryCredentialsProviderArn: str


class ImageTypeDef(TypedDict):
    CreationTime: datetime
    ImageArn: str
    ImageName: str
    ImageStatus: ImageStatusType
    LastModifiedTime: datetime
    Description: NotRequired[str]
    DisplayName: NotRequired[str]
    FailureReason: NotRequired[str]


class ImageVersionTypeDef(TypedDict):
    CreationTime: datetime
    ImageArn: str
    ImageVersionArn: str
    ImageVersionStatus: ImageVersionStatusType
    LastModifiedTime: datetime
    Version: int
    FailureReason: NotRequired[str]


InferenceComponentCapacitySizeTypeDef = TypedDict(
    "InferenceComponentCapacitySizeTypeDef",
    {
        "Type": InferenceComponentCapacitySizeTypeType,
        "Value": int,
    },
)


class InferenceComponentComputeResourceRequirementsTypeDef(TypedDict):
    MinMemoryRequiredInMb: int
    NumberOfCpuCoresRequired: NotRequired[float]
    NumberOfAcceleratorDevicesRequired: NotRequired[float]
    MaxMemoryRequiredInMb: NotRequired[int]


class InferenceComponentContainerSpecificationTypeDef(TypedDict):
    Image: NotRequired[str]
    ArtifactUrl: NotRequired[str]
    Environment: NotRequired[Mapping[str, str]]


class InferenceComponentDataCacheConfigSummaryTypeDef(TypedDict):
    EnableCaching: bool


class InferenceComponentDataCacheConfigTypeDef(TypedDict):
    EnableCaching: bool


class InferenceComponentMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]


class InferenceComponentStartupParametersTypeDef(TypedDict):
    ModelDataDownloadTimeoutInSeconds: NotRequired[int]
    ContainerStartupHealthCheckTimeoutInSeconds: NotRequired[int]


class InferenceComponentSummaryTypeDef(TypedDict):
    CreationTime: datetime
    InferenceComponentArn: str
    InferenceComponentName: str
    EndpointArn: str
    EndpointName: str
    VariantName: str
    LastModifiedTime: datetime
    InferenceComponentStatus: NotRequired[InferenceComponentStatusType]


class InferenceHubAccessConfigTypeDef(TypedDict):
    HubContentArn: str


class RecommendationMetricsTypeDef(TypedDict):
    CostPerHour: NotRequired[float]
    CostPerInference: NotRequired[float]
    MaxInvocations: NotRequired[int]
    ModelLatency: NotRequired[int]
    CpuUtilization: NotRequired[float]
    MemoryUtilization: NotRequired[float]
    ModelSetupTime: NotRequired[int]


class InferenceRecommendationsJobTypeDef(TypedDict):
    JobName: str
    JobDescription: str
    JobType: RecommendationJobTypeType
    JobArn: str
    Status: RecommendationJobStatusType
    CreationTime: datetime
    RoleArn: str
    LastModifiedTime: datetime
    CompletionTime: NotRequired[datetime]
    FailureReason: NotRequired[str]
    ModelName: NotRequired[str]
    SamplePayloadUrl: NotRequired[str]
    ModelPackageVersionArn: NotRequired[str]


class InstanceGroupTypeDef(TypedDict):
    InstanceType: TrainingInstanceTypeType
    InstanceCount: int
    InstanceGroupName: str


class PlacementSpecificationTypeDef(TypedDict):
    InstanceCount: int
    UltraServerId: NotRequired[str]


class IntegerParameterRangeSpecificationTypeDef(TypedDict):
    MinValue: str
    MaxValue: str


class IntegerParameterRangeTypeDef(TypedDict):
    Name: str
    MinValue: str
    MaxValue: str
    ScalingType: NotRequired[HyperParameterScalingTypeType]


class KernelSpecTypeDef(TypedDict):
    Name: str
    DisplayName: NotRequired[str]


class LabelCountersForWorkteamTypeDef(TypedDict):
    HumanLabeled: NotRequired[int]
    PendingHuman: NotRequired[int]
    Total: NotRequired[int]


class LabelingJobDataAttributesOutputTypeDef(TypedDict):
    ContentClassifiers: NotRequired[list[ContentClassifierType]]


class LabelingJobDataAttributesTypeDef(TypedDict):
    ContentClassifiers: NotRequired[Sequence[ContentClassifierType]]


class LabelingJobS3DataSourceTypeDef(TypedDict):
    ManifestS3Uri: str


class LabelingJobSnsDataSourceTypeDef(TypedDict):
    SnsTopicArn: str


class LineageGroupSummaryTypeDef(TypedDict):
    LineageGroupArn: NotRequired[str]
    LineageGroupName: NotRequired[str]
    DisplayName: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]


class ListAliasesRequestTypeDef(TypedDict):
    ImageName: str
    Alias: NotRequired[str]
    Version: NotRequired[int]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListAppsRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SortOrder: NotRequired[SortOrderType]
    SortBy: NotRequired[Literal["CreationTime"]]
    DomainIdEquals: NotRequired[str]
    UserProfileNameEquals: NotRequired[str]
    SpaceNameEquals: NotRequired[str]


class ListCandidatesForAutoMLJobRequestTypeDef(TypedDict):
    AutoMLJobName: str
    StatusEquals: NotRequired[CandidateStatusType]
    CandidateNameEquals: NotRequired[str]
    SortOrder: NotRequired[AutoMLSortOrderType]
    SortBy: NotRequired[CandidateSortByType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class MonitoringJobDefinitionSummaryTypeDef(TypedDict):
    MonitoringJobDefinitionName: str
    MonitoringJobDefinitionArn: str
    CreationTime: datetime
    EndpointName: str


class ListDomainsRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListInferenceRecommendationsJobStepsRequestTypeDef(TypedDict):
    JobName: str
    Status: NotRequired[RecommendationJobStatusType]
    StepType: NotRequired[Literal["BENCHMARK"]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class MlflowAppSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]
    Status: NotRequired[MlflowAppStatusType]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    MlflowVersion: NotRequired[str]


class TrackingServerSummaryTypeDef(TypedDict):
    TrackingServerArn: NotRequired[str]
    TrackingServerName: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    TrackingServerStatus: NotRequired[TrackingServerStatusType]
    IsActive: NotRequired[IsTrackingServerActiveType]
    MlflowVersion: NotRequired[str]


class ModelCardExportJobSummaryTypeDef(TypedDict):
    ModelCardExportJobName: str
    ModelCardExportJobArn: str
    Status: ModelCardExportJobStatusType
    ModelCardName: str
    ModelCardVersion: int
    CreatedAt: datetime
    LastModifiedAt: datetime


class ModelCardVersionSummaryTypeDef(TypedDict):
    ModelCardName: str
    ModelCardArn: str
    ModelCardStatus: ModelCardStatusType
    ModelCardVersion: int
    CreationTime: datetime
    LastModifiedTime: NotRequired[datetime]


class ModelCardSummaryTypeDef(TypedDict):
    ModelCardName: str
    ModelCardArn: str
    ModelCardStatus: ModelCardStatusType
    CreationTime: datetime
    LastModifiedTime: NotRequired[datetime]


class ModelMetadataSummaryTypeDef(TypedDict):
    Domain: str
    Framework: str
    Task: str
    Model: str
    FrameworkVersion: str


class ModelPackageGroupSummaryTypeDef(TypedDict):
    ModelPackageGroupName: str
    ModelPackageGroupArn: str
    CreationTime: datetime
    ModelPackageGroupStatus: ModelPackageGroupStatusType
    ModelPackageGroupDescription: NotRequired[str]


class ModelSummaryTypeDef(TypedDict):
    ModelName: str
    ModelArn: str
    CreationTime: datetime


class MonitoringAlertHistorySummaryTypeDef(TypedDict):
    MonitoringScheduleName: str
    MonitoringAlertName: str
    CreationTime: datetime
    AlertStatus: MonitoringAlertStatusType


class ListMonitoringAlertsRequestTypeDef(TypedDict):
    MonitoringScheduleName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class MonitoringScheduleSummaryTypeDef(TypedDict):
    MonitoringScheduleName: str
    MonitoringScheduleArn: str
    CreationTime: datetime
    LastModifiedTime: datetime
    MonitoringScheduleStatus: ScheduleStatusType
    EndpointName: NotRequired[str]
    MonitoringJobDefinitionName: NotRequired[str]
    MonitoringType: NotRequired[MonitoringTypeType]


class NotebookInstanceLifecycleConfigSummaryTypeDef(TypedDict):
    NotebookInstanceLifecycleConfigName: str
    NotebookInstanceLifecycleConfigArn: str
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]


class NotebookInstanceSummaryTypeDef(TypedDict):
    NotebookInstanceName: str
    NotebookInstanceArn: str
    NotebookInstanceStatus: NotRequired[NotebookInstanceStatusType]
    Url: NotRequired[str]
    InstanceType: NotRequired[InstanceTypeType]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    NotebookInstanceLifecycleConfigName: NotRequired[str]
    DefaultCodeRepository: NotRequired[str]
    AdditionalCodeRepositories: NotRequired[list[str]]


class OptimizationJobSummaryTypeDef(TypedDict):
    OptimizationJobName: str
    OptimizationJobArn: str
    CreationTime: datetime
    OptimizationJobStatus: OptimizationJobStatusType
    DeploymentInstanceType: OptimizationJobDeploymentInstanceTypeType
    OptimizationTypes: list[str]
    OptimizationStartTime: NotRequired[datetime]
    OptimizationEndTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    MaxInstanceCount: NotRequired[int]


class ListPartnerAppsRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


PartnerAppSummaryTypeDef = TypedDict(
    "PartnerAppSummaryTypeDef",
    {
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "Type": NotRequired[PartnerAppTypeType],
        "Status": NotRequired[PartnerAppStatusType],
        "CreationTime": NotRequired[datetime],
    },
)


class ListPipelineExecutionStepsRequestTypeDef(TypedDict):
    PipelineExecutionArn: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SortOrder: NotRequired[SortOrderType]


class PipelineExecutionSummaryTypeDef(TypedDict):
    PipelineExecutionArn: NotRequired[str]
    StartTime: NotRequired[datetime]
    PipelineExecutionStatus: NotRequired[PipelineExecutionStatusType]
    PipelineExecutionDescription: NotRequired[str]
    PipelineExecutionDisplayName: NotRequired[str]
    PipelineExecutionFailureReason: NotRequired[str]


class ListPipelineParametersForExecutionRequestTypeDef(TypedDict):
    PipelineExecutionArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ParameterTypeDef(TypedDict):
    Name: str
    Value: str


class PipelineVersionSummaryTypeDef(TypedDict):
    PipelineArn: NotRequired[str]
    PipelineVersionId: NotRequired[int]
    CreationTime: NotRequired[datetime]
    PipelineVersionDescription: NotRequired[str]
    PipelineVersionDisplayName: NotRequired[str]
    LastExecutionPipelineExecutionArn: NotRequired[str]


class PipelineSummaryTypeDef(TypedDict):
    PipelineArn: NotRequired[str]
    PipelineName: NotRequired[str]
    PipelineDisplayName: NotRequired[str]
    PipelineDescription: NotRequired[str]
    RoleArn: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    LastExecutionTime: NotRequired[datetime]


class ProcessingJobSummaryTypeDef(TypedDict):
    ProcessingJobName: str
    ProcessingJobArn: str
    CreationTime: datetime
    ProcessingJobStatus: ProcessingJobStatusType
    ProcessingEndTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    FailureReason: NotRequired[str]
    ExitMessage: NotRequired[str]


class ProjectSummaryTypeDef(TypedDict):
    ProjectName: str
    ProjectArn: str
    ProjectId: str
    CreationTime: datetime
    ProjectStatus: ProjectStatusType
    ProjectDescription: NotRequired[str]


class ResourceCatalogTypeDef(TypedDict):
    ResourceCatalogArn: str
    ResourceCatalogName: str
    Description: str
    CreationTime: datetime


class ListSpacesRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SortOrder: NotRequired[SortOrderType]
    SortBy: NotRequired[SpaceSortKeyType]
    DomainIdEquals: NotRequired[str]
    SpaceNameContains: NotRequired[str]


class ListStageDevicesRequestTypeDef(TypedDict):
    EdgeDeploymentPlanName: str
    StageName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ExcludeDevicesDeployedInOtherStage: NotRequired[bool]


class StudioLifecycleConfigDetailsTypeDef(TypedDict):
    StudioLifecycleConfigArn: NotRequired[str]
    StudioLifecycleConfigName: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    StudioLifecycleConfigAppType: NotRequired[StudioLifecycleConfigAppTypeType]


class ListSubscribedWorkteamsRequestTypeDef(TypedDict):
    NameContains: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListTagsInputTypeDef(TypedDict):
    ResourceArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListTrainingJobsForHyperParameterTuningJobRequestTypeDef(TypedDict):
    HyperParameterTuningJobName: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    StatusEquals: NotRequired[TrainingJobStatusType]
    SortBy: NotRequired[TrainingJobSortByOptionsType]
    SortOrder: NotRequired[SortOrderType]


class TrainingPlanFilterTypeDef(TypedDict):
    Name: Literal["Status"]
    Value: str


class TransformJobSummaryTypeDef(TypedDict):
    TransformJobName: str
    TransformJobArn: str
    CreationTime: datetime
    TransformJobStatus: TransformJobStatusType
    TransformEndTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    FailureReason: NotRequired[str]


class ListUltraServersByReservedCapacityRequestTypeDef(TypedDict):
    ReservedCapacityArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class UltraServerTypeDef(TypedDict):
    UltraServerId: str
    UltraServerType: str
    AvailabilityZone: str
    InstanceType: ReservedCapacityInstanceTypeType
    TotalInstanceCount: int
    ConfiguredSpareInstanceCount: NotRequired[int]
    AvailableInstanceCount: NotRequired[int]
    InUseInstanceCount: NotRequired[int]
    AvailableSpareInstanceCount: NotRequired[int]
    UnhealthyInstanceCount: NotRequired[int]
    HealthStatus: NotRequired[UltraServerHealthStatusType]


class ListUserProfilesRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SortOrder: NotRequired[SortOrderType]
    SortBy: NotRequired[UserProfileSortKeyType]
    DomainIdEquals: NotRequired[str]
    UserProfileNameContains: NotRequired[str]


class UserProfileDetailsTypeDef(TypedDict):
    DomainId: NotRequired[str]
    UserProfileName: NotRequired[str]
    Status: NotRequired[UserProfileStatusType]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]


class ListWorkforcesRequestTypeDef(TypedDict):
    SortBy: NotRequired[ListWorkforcesSortByOptionsType]
    SortOrder: NotRequired[SortOrderType]
    NameContains: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListWorkteamsRequestTypeDef(TypedDict):
    SortBy: NotRequired[ListWorkteamsSortByOptionsType]
    SortOrder: NotRequired[SortOrderType]
    NameContains: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class OidcMemberDefinitionOutputTypeDef(TypedDict):
    Groups: NotRequired[list[str]]


class PredefinedMetricSpecificationTypeDef(TypedDict):
    PredefinedMetricType: NotRequired[str]


class ModelAccessConfigTypeDef(TypedDict):
    AcceptEula: bool


class ModelBiasAppSpecificationTypeDef(TypedDict):
    ImageUri: str
    ConfigUri: str
    Environment: NotRequired[Mapping[str, str]]


class MonitoringGroundTruthS3InputTypeDef(TypedDict):
    S3Uri: NotRequired[str]


class ModelCompilationConfigOutputTypeDef(TypedDict):
    Image: NotRequired[str]
    OverrideEnvironment: NotRequired[dict[str, str]]


class ModelCompilationConfigTypeDef(TypedDict):
    Image: NotRequired[str]
    OverrideEnvironment: NotRequired[Mapping[str, str]]


class ModelDashboardEndpointTypeDef(TypedDict):
    EndpointName: str
    EndpointArn: str
    CreationTime: datetime
    LastModifiedTime: datetime
    EndpointStatus: EndpointStatusType


class ModelDashboardIndicatorActionTypeDef(TypedDict):
    Enabled: NotRequired[bool]


class ModelExplainabilityAppSpecificationTypeDef(TypedDict):
    ImageUri: str
    ConfigUri: str
    Environment: NotRequired[Mapping[str, str]]


class RealTimeInferenceConfigTypeDef(TypedDict):
    InstanceType: InstanceTypeType
    InstanceCount: int


class ModelInputTypeDef(TypedDict):
    DataInputConfig: str


class ModelLatencyThresholdTypeDef(TypedDict):
    Percentile: NotRequired[str]
    ValueInMilliseconds: NotRequired[int]


class ModelMetadataFilterTypeDef(TypedDict):
    Name: ModelMetadataFilterTypeType
    Value: str


class ModelPackageStatusItemTypeDef(TypedDict):
    Name: str
    Status: DetailedModelPackageStatusType
    FailureReason: NotRequired[str]


class ModelQualityAppSpecificationTypeDef(TypedDict):
    ImageUri: str
    ContainerEntrypoint: NotRequired[Sequence[str]]
    ContainerArguments: NotRequired[Sequence[str]]
    RecordPreprocessorSourceUri: NotRequired[str]
    PostAnalyticsProcessorSourceUri: NotRequired[str]
    ProblemType: NotRequired[MonitoringProblemTypeType]
    Environment: NotRequired[Mapping[str, str]]


class ModelQuantizationConfigOutputTypeDef(TypedDict):
    Image: NotRequired[str]
    OverrideEnvironment: NotRequired[dict[str, str]]


class ModelQuantizationConfigTypeDef(TypedDict):
    Image: NotRequired[str]
    OverrideEnvironment: NotRequired[Mapping[str, str]]


class ModelShardingConfigOutputTypeDef(TypedDict):
    Image: NotRequired[str]
    OverrideEnvironment: NotRequired[dict[str, str]]


class ModelShardingConfigTypeDef(TypedDict):
    Image: NotRequired[str]
    OverrideEnvironment: NotRequired[Mapping[str, str]]


class ModelSpeculativeDecodingTrainingDataSourceTypeDef(TypedDict):
    S3Uri: str
    S3DataType: ModelSpeculativeDecodingS3DataTypeType


class ModelStepMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]


class MonitoringAppSpecificationOutputTypeDef(TypedDict):
    ImageUri: str
    ContainerEntrypoint: NotRequired[list[str]]
    ContainerArguments: NotRequired[list[str]]
    RecordPreprocessorSourceUri: NotRequired[str]
    PostAnalyticsProcessorSourceUri: NotRequired[str]


class MonitoringAppSpecificationTypeDef(TypedDict):
    ImageUri: str
    ContainerEntrypoint: NotRequired[Sequence[str]]
    ContainerArguments: NotRequired[Sequence[str]]
    RecordPreprocessorSourceUri: NotRequired[str]
    PostAnalyticsProcessorSourceUri: NotRequired[str]


class MonitoringClusterConfigTypeDef(TypedDict):
    InstanceCount: int
    InstanceType: ProcessingInstanceTypeType
    VolumeSizeInGB: int
    VolumeKmsKeyId: NotRequired[str]


class MonitoringCsvDatasetFormatTypeDef(TypedDict):
    Header: NotRequired[bool]


class MonitoringJsonDatasetFormatTypeDef(TypedDict):
    Line: NotRequired[bool]


class MonitoringS3OutputTypeDef(TypedDict):
    S3Uri: str
    LocalPath: str
    S3UploadMode: NotRequired[ProcessingS3UploadModeType]


class ScheduleConfigTypeDef(TypedDict):
    ScheduleExpression: str
    DataAnalysisStartTime: NotRequired[str]
    DataAnalysisEndTime: NotRequired[str]


class NeoVpcConfigTypeDef(TypedDict):
    SecurityGroupIds: Sequence[str]
    Subnets: Sequence[str]


class S3StorageConfigTypeDef(TypedDict):
    S3Uri: str
    KmsKeyId: NotRequired[str]
    ResolvedOutputS3Uri: NotRequired[str]


class OidcConfigForResponseTypeDef(TypedDict):
    ClientId: NotRequired[str]
    Issuer: NotRequired[str]
    AuthorizationEndpoint: NotRequired[str]
    TokenEndpoint: NotRequired[str]
    UserInfoEndpoint: NotRequired[str]
    LogoutEndpoint: NotRequired[str]
    JwksUri: NotRequired[str]
    Scope: NotRequired[str]
    AuthenticationRequestExtraParams: NotRequired[dict[str, str]]


class OidcMemberDefinitionTypeDef(TypedDict):
    Groups: NotRequired[Sequence[str]]


class OnlineStoreSecurityConfigTypeDef(TypedDict):
    KmsKeyId: NotRequired[str]


class TtlDurationTypeDef(TypedDict):
    Unit: NotRequired[TtlDurationUnitType]
    Value: NotRequired[int]


class OptimizationModelAccessConfigTypeDef(TypedDict):
    AcceptEula: bool


class OptimizationSageMakerModelTypeDef(TypedDict):
    ModelName: NotRequired[str]


class OptimizationVpcConfigTypeDef(TypedDict):
    SecurityGroupIds: Sequence[str]
    Subnets: Sequence[str]


class TargetPlatformTypeDef(TypedDict):
    Os: TargetPlatformOsType
    Arch: TargetPlatformArchType
    Accelerator: NotRequired[TargetPlatformAcceleratorType]


class OwnershipSettingsSummaryTypeDef(TypedDict):
    OwnerUserProfileName: NotRequired[str]


class ParentTypeDef(TypedDict):
    TrialName: NotRequired[str]
    ExperimentName: NotRequired[str]


class RoleGroupAssignmentOutputTypeDef(TypedDict):
    RoleName: str
    GroupPatterns: list[str]


class RoleGroupAssignmentTypeDef(TypedDict):
    RoleName: str
    GroupPatterns: Sequence[str]


class ProductionVariantManagedInstanceScalingTypeDef(TypedDict):
    Status: NotRequired[ManagedInstanceScalingStatusType]
    MinInstanceCount: NotRequired[int]
    MaxInstanceCount: NotRequired[int]


class ProductionVariantRoutingConfigTypeDef(TypedDict):
    RoutingStrategy: RoutingStrategyType


class ProductionVariantStatusTypeDef(TypedDict):
    Status: VariantStatusType
    StatusMessage: NotRequired[str]
    StartTime: NotRequired[datetime]


class PhaseTypeDef(TypedDict):
    InitialNumberOfUsers: NotRequired[int]
    SpawnRate: NotRequired[int]
    DurationInSeconds: NotRequired[int]


class ProcessingJobStepMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]


class QualityCheckStepMetadataTypeDef(TypedDict):
    CheckType: NotRequired[str]
    BaselineUsedForDriftCheckStatistics: NotRequired[str]
    BaselineUsedForDriftCheckConstraints: NotRequired[str]
    CalculatedBaselineStatistics: NotRequired[str]
    CalculatedBaselineConstraints: NotRequired[str]
    ModelPackageGroupName: NotRequired[str]
    ViolationReport: NotRequired[str]
    CheckJobArn: NotRequired[str]
    SkipCheck: NotRequired[bool]
    RegisterNewBaseline: NotRequired[bool]


class RegisterModelStepMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]


class TrainingJobStepMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]


class TransformJobStepMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]


class TuningJobStepMetaDataTypeDef(TypedDict):
    Arn: NotRequired[str]


class SelectiveExecutionResultTypeDef(TypedDict):
    SourcePipelineExecutionArn: NotRequired[str]


class PriorityClassTypeDef(TypedDict):
    Name: str
    Weight: int


class ProcessingClusterConfigTypeDef(TypedDict):
    InstanceCount: int
    InstanceType: ProcessingInstanceTypeType
    VolumeSizeInGB: int
    VolumeKmsKeyId: NotRequired[str]


class ProcessingFeatureStoreOutputTypeDef(TypedDict):
    FeatureGroupName: str


ProcessingS3InputTypeDef = TypedDict(
    "ProcessingS3InputTypeDef",
    {
        "S3Uri": str,
        "S3DataType": ProcessingS3DataTypeType,
        "LocalPath": NotRequired[str],
        "S3InputMode": NotRequired[ProcessingS3InputModeType],
        "S3DataDistributionType": NotRequired[ProcessingS3DataDistributionTypeType],
        "S3CompressionType": NotRequired[ProcessingS3CompressionTypeType],
    },
)


class ProcessingS3OutputTypeDef(TypedDict):
    S3Uri: str
    S3UploadMode: ProcessingS3UploadModeType
    LocalPath: NotRequired[str]


class ProductionVariantCapacityReservationConfigTypeDef(TypedDict):
    CapacityReservationPreference: NotRequired[Literal["capacity-reservations-only"]]
    MlReservationArn: NotRequired[str]


class ProductionVariantCoreDumpConfigTypeDef(TypedDict):
    DestinationS3Uri: str
    KmsKeyId: NotRequired[str]


class ProfilerConfigForUpdateTypeDef(TypedDict):
    S3OutputPath: NotRequired[str]
    ProfilingIntervalInMilliseconds: NotRequired[int]
    ProfilingParameters: NotRequired[Mapping[str, str]]
    DisableProfiler: NotRequired[bool]


class ProfilerConfigTypeDef(TypedDict):
    S3OutputPath: NotRequired[str]
    ProfilingIntervalInMilliseconds: NotRequired[int]
    ProfilingParameters: NotRequired[Mapping[str, str]]
    DisableProfiler: NotRequired[bool]


class ProfilerRuleConfigurationTypeDef(TypedDict):
    RuleConfigurationName: str
    RuleEvaluatorImage: str
    LocalPath: NotRequired[str]
    S3OutputPath: NotRequired[str]
    InstanceType: NotRequired[ProcessingInstanceTypeType]
    VolumeSizeInGB: NotRequired[int]
    RuleParameters: NotRequired[Mapping[str, str]]


class PropertyNameQueryTypeDef(TypedDict):
    PropertyNameHint: str


class ProvisioningParameterTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


class USDTypeDef(TypedDict):
    Dollars: NotRequired[int]
    Cents: NotRequired[int]
    TenthFractionsOfACent: NotRequired[int]


class PutModelPackageGroupPolicyInputTypeDef(TypedDict):
    ModelPackageGroupName: str
    ResourcePolicy: str


VertexTypeDef = TypedDict(
    "VertexTypeDef",
    {
        "Arn": NotRequired[str],
        "Type": NotRequired[str],
        "LineageType": NotRequired[LineageTypeType],
    },
)


class RStudioServerProAppSettingsTypeDef(TypedDict):
    AccessStatus: NotRequired[RStudioServerProAccessStatusType]
    UserGroup: NotRequired[RStudioServerProUserGroupType]


class RecommendationJobCompiledOutputConfigTypeDef(TypedDict):
    S3OutputUri: NotRequired[str]


class RecommendationJobPayloadConfigOutputTypeDef(TypedDict):
    SamplePayloadUrl: NotRequired[str]
    SupportedContentTypes: NotRequired[list[str]]


class RecommendationJobPayloadConfigTypeDef(TypedDict):
    SamplePayloadUrl: NotRequired[str]
    SupportedContentTypes: NotRequired[Sequence[str]]


class RecommendationJobResourceLimitTypeDef(TypedDict):
    MaxNumberOfTests: NotRequired[int]
    MaxParallelOfTests: NotRequired[int]


class RecommendationJobVpcConfigOutputTypeDef(TypedDict):
    SecurityGroupIds: list[str]
    Subnets: list[str]


class RecommendationJobVpcConfigTypeDef(TypedDict):
    SecurityGroupIds: Sequence[str]
    Subnets: Sequence[str]


class RemoteDebugConfigForUpdateTypeDef(TypedDict):
    EnableRemoteDebug: NotRequired[bool]


class RenderableTaskTypeDef(TypedDict):
    Input: str


class RenderingErrorTypeDef(TypedDict):
    Code: str
    Message: str


class ReservedCapacityOfferingTypeDef(TypedDict):
    InstanceType: ReservedCapacityInstanceTypeType
    InstanceCount: int
    ReservedCapacityType: NotRequired[ReservedCapacityTypeType]
    UltraServerType: NotRequired[str]
    UltraServerCount: NotRequired[int]
    AvailabilityZone: NotRequired[str]
    DurationHours: NotRequired[int]
    DurationMinutes: NotRequired[int]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]


class ResourceConfigForUpdateTypeDef(TypedDict):
    KeepAlivePeriodInSeconds: int


class VisibilityConditionsTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


class TotalHitsTypeDef(TypedDict):
    Value: NotRequired[int]
    Relation: NotRequired[RelationType]


class SelectedStepTypeDef(TypedDict):
    StepName: str


class SendPipelineExecutionStepFailureRequestTypeDef(TypedDict):
    CallbackToken: str
    FailureReason: NotRequired[str]
    ClientRequestToken: NotRequired[str]


class ShadowModelVariantConfigTypeDef(TypedDict):
    ShadowModelVariantName: str
    SamplingPercentage: int


class SharingSettingsTypeDef(TypedDict):
    NotebookOutputOption: NotRequired[NotebookOutputOptionType]
    S3OutputPath: NotRequired[str]
    S3KmsKeyId: NotRequired[str]


class SourceIpConfigOutputTypeDef(TypedDict):
    Cidrs: list[str]


class SourceIpConfigTypeDef(TypedDict):
    Cidrs: Sequence[str]


class SpaceIdleSettingsTypeDef(TypedDict):
    IdleTimeoutInMinutes: NotRequired[int]


class SpaceSharingSettingsSummaryTypeDef(TypedDict):
    SharingType: NotRequired[SharingTypeType]


class StairsTypeDef(TypedDict):
    DurationInSeconds: NotRequired[int]
    NumberOfSteps: NotRequired[int]
    UsersPerStep: NotRequired[int]


class StartEdgeDeploymentStageRequestTypeDef(TypedDict):
    EdgeDeploymentPlanName: str
    StageName: str


class StartInferenceExperimentRequestTypeDef(TypedDict):
    Name: str


class StartMlflowTrackingServerRequestTypeDef(TypedDict):
    TrackingServerName: str


class StartMonitoringScheduleRequestTypeDef(TypedDict):
    MonitoringScheduleName: str


class StartNotebookInstanceInputTypeDef(TypedDict):
    NotebookInstanceName: str


class StartSessionRequestTypeDef(TypedDict):
    ResourceIdentifier: str


class StopAutoMLJobRequestTypeDef(TypedDict):
    AutoMLJobName: str


class StopCompilationJobRequestTypeDef(TypedDict):
    CompilationJobName: str


class StopEdgeDeploymentStageRequestTypeDef(TypedDict):
    EdgeDeploymentPlanName: str
    StageName: str


class StopEdgePackagingJobRequestTypeDef(TypedDict):
    EdgePackagingJobName: str


class StopHyperParameterTuningJobRequestTypeDef(TypedDict):
    HyperParameterTuningJobName: str


class StopInferenceRecommendationsJobRequestTypeDef(TypedDict):
    JobName: str


class StopLabelingJobRequestTypeDef(TypedDict):
    LabelingJobName: str


class StopMlflowTrackingServerRequestTypeDef(TypedDict):
    TrackingServerName: str


class StopMonitoringScheduleRequestTypeDef(TypedDict):
    MonitoringScheduleName: str


class StopNotebookInstanceInputTypeDef(TypedDict):
    NotebookInstanceName: str


class StopOptimizationJobRequestTypeDef(TypedDict):
    OptimizationJobName: str


class StopPipelineExecutionRequestTypeDef(TypedDict):
    PipelineExecutionArn: str
    ClientRequestToken: str


class StopProcessingJobRequestTypeDef(TypedDict):
    ProcessingJobName: str


class StopTrainingJobRequestTypeDef(TypedDict):
    TrainingJobName: str


class StopTransformJobRequestTypeDef(TypedDict):
    TransformJobName: str


class ThroughputConfigUpdateTypeDef(TypedDict):
    ThroughputMode: NotRequired[ThroughputModeType]
    ProvisionedReadCapacityUnits: NotRequired[int]
    ProvisionedWriteCapacityUnits: NotRequired[int]


class TimeSeriesConfigOutputTypeDef(TypedDict):
    TargetAttributeName: str
    TimestampAttributeName: str
    ItemIdentifierAttributeName: str
    GroupingAttributeNames: NotRequired[list[str]]


class TimeSeriesConfigTypeDef(TypedDict):
    TargetAttributeName: str
    TimestampAttributeName: str
    ItemIdentifierAttributeName: str
    GroupingAttributeNames: NotRequired[Sequence[str]]


class TimeSeriesTransformationsOutputTypeDef(TypedDict):
    Filling: NotRequired[dict[str, dict[FillingTypeType, str]]]
    Aggregation: NotRequired[dict[str, AggregationTransformationValueType]]


class TimeSeriesTransformationsTypeDef(TypedDict):
    Filling: NotRequired[Mapping[str, Mapping[FillingTypeType, str]]]
    Aggregation: NotRequired[Mapping[str, AggregationTransformationValueType]]


class TrainingRepositoryAuthConfigTypeDef(TypedDict):
    TrainingRepositoryCredentialsProviderArn: str


class TransformS3DataSourceTypeDef(TypedDict):
    S3DataType: S3DataTypeType
    S3Uri: str


class UpdateActionRequestTypeDef(TypedDict):
    ActionName: str
    Description: NotRequired[str]
    Status: NotRequired[ActionStatusType]
    Properties: NotRequired[Mapping[str, str]]
    PropertiesToRemove: NotRequired[Sequence[str]]


class UpdateArtifactRequestTypeDef(TypedDict):
    ArtifactArn: str
    ArtifactName: NotRequired[str]
    Properties: NotRequired[Mapping[str, str]]
    PropertiesToRemove: NotRequired[Sequence[str]]


class UpdateClusterSoftwareInstanceGroupSpecificationTypeDef(TypedDict):
    InstanceGroupName: str


class UpdateContextRequestTypeDef(TypedDict):
    ContextName: str
    Description: NotRequired[str]
    Properties: NotRequired[Mapping[str, str]]
    PropertiesToRemove: NotRequired[Sequence[str]]


class VariantPropertyTypeDef(TypedDict):
    VariantPropertyType: VariantPropertyTypeType


class UpdateExperimentRequestTypeDef(TypedDict):
    ExperimentName: str
    DisplayName: NotRequired[str]
    Description: NotRequired[str]


class UpdateHubContentReferenceRequestTypeDef(TypedDict):
    HubName: str
    HubContentName: str
    HubContentType: HubContentTypeType
    MinVersion: NotRequired[str]


class UpdateHubContentRequestTypeDef(TypedDict):
    HubName: str
    HubContentName: str
    HubContentType: HubContentTypeType
    HubContentVersion: str
    HubContentDisplayName: NotRequired[str]
    HubContentDescription: NotRequired[str]
    HubContentMarkdown: NotRequired[str]
    HubContentSearchKeywords: NotRequired[Sequence[str]]
    SupportStatus: NotRequired[HubContentSupportStatusType]


class UpdateHubRequestTypeDef(TypedDict):
    HubName: str
    HubDescription: NotRequired[str]
    HubDisplayName: NotRequired[str]
    HubSearchKeywords: NotRequired[Sequence[str]]


class UpdateImageRequestTypeDef(TypedDict):
    ImageName: str
    DeleteProperties: NotRequired[Sequence[str]]
    Description: NotRequired[str]
    DisplayName: NotRequired[str]
    RoleArn: NotRequired[str]


class UpdateImageVersionRequestTypeDef(TypedDict):
    ImageName: str
    Alias: NotRequired[str]
    Version: NotRequired[int]
    AliasesToAdd: NotRequired[Sequence[str]]
    AliasesToDelete: NotRequired[Sequence[str]]
    VendorGuidance: NotRequired[VendorGuidanceType]
    JobType: NotRequired[JobTypeType]
    MLFramework: NotRequired[str]
    ProgrammingLang: NotRequired[str]
    Processor: NotRequired[ProcessorType]
    Horovod: NotRequired[bool]
    ReleaseNotes: NotRequired[str]


class UpdateMlflowAppRequestTypeDef(TypedDict):
    Arn: str
    Name: NotRequired[str]
    ArtifactStoreUri: NotRequired[str]
    ModelRegistrationMode: NotRequired[ModelRegistrationModeType]
    WeeklyMaintenanceWindowStart: NotRequired[str]
    DefaultDomainIdList: NotRequired[Sequence[str]]
    AccountDefaultStatus: NotRequired[AccountDefaultStatusType]


class UpdateMlflowTrackingServerRequestTypeDef(TypedDict):
    TrackingServerName: str
    ArtifactStoreUri: NotRequired[str]
    TrackingServerSize: NotRequired[TrackingServerSizeType]
    AutomaticModelRegistration: NotRequired[bool]
    WeeklyMaintenanceWindowStart: NotRequired[str]


class UpdateModelCardRequestTypeDef(TypedDict):
    ModelCardName: str
    Content: NotRequired[str]
    ModelCardStatus: NotRequired[ModelCardStatusType]


class UpdateMonitoringAlertRequestTypeDef(TypedDict):
    MonitoringScheduleName: str
    MonitoringAlertName: str
    DatapointsToAlert: int
    EvaluationPeriod: int


class UpdatePipelineVersionRequestTypeDef(TypedDict):
    PipelineArn: str
    PipelineVersionId: int
    PipelineVersionDisplayName: NotRequired[str]
    PipelineVersionDescription: NotRequired[str]


class UpdateTrialRequestTypeDef(TypedDict):
    TrialName: str
    DisplayName: NotRequired[str]


class WorkforceVpcConfigResponseTypeDef(TypedDict):
    VpcId: str
    SecurityGroupIds: list[str]
    Subnets: list[str]
    VpcEndpointId: NotRequired[str]


class ComputeQuotaResourceConfigTypeDef(TypedDict):
    InstanceType: ClusterInstanceTypeType
    Count: NotRequired[int]
    Accelerators: NotRequired[int]
    VCpu: NotRequired[float]
    MemoryInGiB: NotRequired[float]
    AcceleratorPartition: NotRequired[AcceleratorPartitionConfigTypeDef]


class ActionSummaryTypeDef(TypedDict):
    ActionArn: NotRequired[str]
    ActionName: NotRequired[str]
    Source: NotRequired[ActionSourceTypeDef]
    ActionType: NotRequired[str]
    Status: NotRequired[ActionStatusType]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]


class AddAssociationResponseTypeDef(TypedDict):
    SourceArn: str
    DestinationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateTrialComponentResponseTypeDef(TypedDict):
    TrialComponentArn: str
    TrialArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class AttachClusterNodeVolumeResponseTypeDef(TypedDict):
    ClusterArn: str
    NodeId: str
    VolumeId: str
    AttachTime: datetime
    Status: VolumeAttachmentStatusType
    DeviceName: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateActionResponseTypeDef(TypedDict):
    ActionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAlgorithmOutputTypeDef(TypedDict):
    AlgorithmArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAppImageConfigResponseTypeDef(TypedDict):
    AppImageConfigArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAppResponseTypeDef(TypedDict):
    AppArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateArtifactResponseTypeDef(TypedDict):
    ArtifactArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAutoMLJobResponseTypeDef(TypedDict):
    AutoMLJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAutoMLJobV2ResponseTypeDef(TypedDict):
    AutoMLJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateClusterResponseTypeDef(TypedDict):
    ClusterArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateClusterSchedulerConfigResponseTypeDef(TypedDict):
    ClusterSchedulerConfigArn: str
    ClusterSchedulerConfigId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCodeRepositoryOutputTypeDef(TypedDict):
    CodeRepositoryArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCompilationJobResponseTypeDef(TypedDict):
    CompilationJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateComputeQuotaResponseTypeDef(TypedDict):
    ComputeQuotaArn: str
    ComputeQuotaId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateContextResponseTypeDef(TypedDict):
    ContextArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDataQualityJobDefinitionResponseTypeDef(TypedDict):
    JobDefinitionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDomainResponseTypeDef(TypedDict):
    DomainArn: str
    DomainId: str
    Url: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateEdgeDeploymentPlanResponseTypeDef(TypedDict):
    EdgeDeploymentPlanArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateEndpointConfigOutputTypeDef(TypedDict):
    EndpointConfigArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateEndpointOutputTypeDef(TypedDict):
    EndpointArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateExperimentResponseTypeDef(TypedDict):
    ExperimentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFeatureGroupResponseTypeDef(TypedDict):
    FeatureGroupArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFlowDefinitionResponseTypeDef(TypedDict):
    FlowDefinitionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateHubContentReferenceResponseTypeDef(TypedDict):
    HubArn: str
    HubContentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateHubResponseTypeDef(TypedDict):
    HubArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateHumanTaskUiResponseTypeDef(TypedDict):
    HumanTaskUiArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateHyperParameterTuningJobResponseTypeDef(TypedDict):
    HyperParameterTuningJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateImageResponseTypeDef(TypedDict):
    ImageArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateImageVersionResponseTypeDef(TypedDict):
    ImageVersionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateInferenceComponentOutputTypeDef(TypedDict):
    InferenceComponentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateInferenceExperimentResponseTypeDef(TypedDict):
    InferenceExperimentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateInferenceRecommendationsJobResponseTypeDef(TypedDict):
    JobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateLabelingJobResponseTypeDef(TypedDict):
    LabelingJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateMlflowAppResponseTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateMlflowTrackingServerResponseTypeDef(TypedDict):
    TrackingServerArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateModelBiasJobDefinitionResponseTypeDef(TypedDict):
    JobDefinitionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateModelCardExportJobResponseTypeDef(TypedDict):
    ModelCardExportJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateModelCardResponseTypeDef(TypedDict):
    ModelCardArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateModelExplainabilityJobDefinitionResponseTypeDef(TypedDict):
    JobDefinitionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateModelOutputTypeDef(TypedDict):
    ModelArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateModelPackageGroupOutputTypeDef(TypedDict):
    ModelPackageGroupArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateModelPackageOutputTypeDef(TypedDict):
    ModelPackageArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateModelQualityJobDefinitionResponseTypeDef(TypedDict):
    JobDefinitionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateMonitoringScheduleResponseTypeDef(TypedDict):
    MonitoringScheduleArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateNotebookInstanceLifecycleConfigOutputTypeDef(TypedDict):
    NotebookInstanceLifecycleConfigArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateNotebookInstanceOutputTypeDef(TypedDict):
    NotebookInstanceArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateOptimizationJobResponseTypeDef(TypedDict):
    OptimizationJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePartnerAppPresignedUrlResponseTypeDef(TypedDict):
    Url: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePartnerAppResponseTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePipelineResponseTypeDef(TypedDict):
    PipelineArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePresignedDomainUrlResponseTypeDef(TypedDict):
    AuthorizedUrl: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePresignedMlflowAppUrlResponseTypeDef(TypedDict):
    AuthorizedUrl: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePresignedMlflowTrackingServerUrlResponseTypeDef(TypedDict):
    AuthorizedUrl: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePresignedNotebookInstanceUrlOutputTypeDef(TypedDict):
    AuthorizedUrl: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateProcessingJobResponseTypeDef(TypedDict):
    ProcessingJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateProjectOutputTypeDef(TypedDict):
    ProjectArn: str
    ProjectId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSpaceResponseTypeDef(TypedDict):
    SpaceArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateStudioLifecycleConfigResponseTypeDef(TypedDict):
    StudioLifecycleConfigArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTrainingJobResponseTypeDef(TypedDict):
    TrainingJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTrainingPlanResponseTypeDef(TypedDict):
    TrainingPlanArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTransformJobResponseTypeDef(TypedDict):
    TransformJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTrialComponentResponseTypeDef(TypedDict):
    TrialComponentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTrialResponseTypeDef(TypedDict):
    TrialArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateUserProfileResponseTypeDef(TypedDict):
    UserProfileArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateWorkforceResponseTypeDef(TypedDict):
    WorkforceArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateWorkteamResponseTypeDef(TypedDict):
    WorkteamArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteActionResponseTypeDef(TypedDict):
    ActionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteArtifactResponseTypeDef(TypedDict):
    ArtifactArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteAssociationResponseTypeDef(TypedDict):
    SourceArn: str
    DestinationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteClusterResponseTypeDef(TypedDict):
    ClusterArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteContextResponseTypeDef(TypedDict):
    ContextArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteExperimentResponseTypeDef(TypedDict):
    ExperimentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteInferenceExperimentResponseTypeDef(TypedDict):
    InferenceExperimentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteMlflowAppResponseTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteMlflowTrackingServerResponseTypeDef(TypedDict):
    TrackingServerArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeletePartnerAppResponseTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeletePipelineResponseTypeDef(TypedDict):
    PipelineArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTrialComponentResponseTypeDef(TypedDict):
    TrialComponentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTrialResponseTypeDef(TypedDict):
    TrialArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteWorkteamResponseTypeDef(TypedDict):
    Success: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeImageResponseTypeDef(TypedDict):
    CreationTime: datetime
    Description: str
    DisplayName: str
    FailureReason: str
    ImageArn: str
    ImageName: str
    ImageStatus: ImageStatusType
    LastModifiedTime: datetime
    RoleArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeImageVersionResponseTypeDef(TypedDict):
    BaseImage: str
    ContainerImage: str
    CreationTime: datetime
    FailureReason: str
    ImageArn: str
    ImageVersionArn: str
    ImageVersionStatus: ImageVersionStatusType
    LastModifiedTime: datetime
    Version: int
    VendorGuidance: VendorGuidanceType
    JobType: JobTypeType
    MLFramework: str
    ProgrammingLang: str
    Processor: ProcessorType
    Horovod: bool
    ReleaseNotes: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribePipelineDefinitionForExecutionResponseTypeDef(TypedDict):
    PipelineDefinition: str
    CreationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeStudioLifecycleConfigResponseTypeDef(TypedDict):
    StudioLifecycleConfigArn: str
    StudioLifecycleConfigName: str
    CreationTime: datetime
    LastModifiedTime: datetime
    StudioLifecycleConfigContent: str
    StudioLifecycleConfigAppType: StudioLifecycleConfigAppTypeType
    ResponseMetadata: ResponseMetadataTypeDef


class DetachClusterNodeVolumeResponseTypeDef(TypedDict):
    ClusterArn: str
    NodeId: str
    VolumeId: str
    AttachTime: datetime
    Status: VolumeAttachmentStatusType
    DeviceName: str
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateTrialComponentResponseTypeDef(TypedDict):
    TrialComponentArn: str
    TrialArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetLineageGroupPolicyResponseTypeDef(TypedDict):
    LineageGroupArn: str
    ResourcePolicy: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetModelPackageGroupPolicyOutputTypeDef(TypedDict):
    ResourcePolicy: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetSagemakerServicecatalogPortfolioStatusOutputTypeDef(TypedDict):
    Status: SagemakerServicecatalogStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class ImportHubContentResponseTypeDef(TypedDict):
    HubArn: str
    HubContentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListAliasesResponseTypeDef(TypedDict):
    SageMakerImageVersionAliases: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PutModelPackageGroupPolicyOutputTypeDef(TypedDict):
    ModelPackageGroupArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class RetryPipelineExecutionResponseTypeDef(TypedDict):
    PipelineExecutionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class SendPipelineExecutionStepFailureResponseTypeDef(TypedDict):
    PipelineExecutionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class SendPipelineExecutionStepSuccessResponseTypeDef(TypedDict):
    PipelineExecutionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartInferenceExperimentResponseTypeDef(TypedDict):
    InferenceExperimentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartMlflowTrackingServerResponseTypeDef(TypedDict):
    TrackingServerArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartPipelineExecutionResponseTypeDef(TypedDict):
    PipelineExecutionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartSessionResponseTypeDef(TypedDict):
    SessionId: str
    StreamUrl: str
    TokenValue: str
    ResponseMetadata: ResponseMetadataTypeDef


class StopInferenceExperimentResponseTypeDef(TypedDict):
    InferenceExperimentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class StopMlflowTrackingServerResponseTypeDef(TypedDict):
    TrackingServerArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class StopPipelineExecutionResponseTypeDef(TypedDict):
    PipelineExecutionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateActionResponseTypeDef(TypedDict):
    ActionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAppImageConfigResponseTypeDef(TypedDict):
    AppImageConfigArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateArtifactResponseTypeDef(TypedDict):
    ArtifactArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateClusterResponseTypeDef(TypedDict):
    ClusterArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateClusterSchedulerConfigResponseTypeDef(TypedDict):
    ClusterSchedulerConfigArn: str
    ClusterSchedulerConfigVersion: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateClusterSoftwareResponseTypeDef(TypedDict):
    ClusterArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateCodeRepositoryOutputTypeDef(TypedDict):
    CodeRepositoryArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateComputeQuotaResponseTypeDef(TypedDict):
    ComputeQuotaArn: str
    ComputeQuotaVersion: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateContextResponseTypeDef(TypedDict):
    ContextArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDomainResponseTypeDef(TypedDict):
    DomainArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateEndpointOutputTypeDef(TypedDict):
    EndpointArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateEndpointWeightsAndCapacitiesOutputTypeDef(TypedDict):
    EndpointArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateExperimentResponseTypeDef(TypedDict):
    ExperimentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateFeatureGroupResponseTypeDef(TypedDict):
    FeatureGroupArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateHubContentReferenceResponseTypeDef(TypedDict):
    HubArn: str
    HubContentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateHubContentResponseTypeDef(TypedDict):
    HubArn: str
    HubContentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateHubResponseTypeDef(TypedDict):
    HubArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateImageResponseTypeDef(TypedDict):
    ImageArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateImageVersionResponseTypeDef(TypedDict):
    ImageVersionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateInferenceComponentOutputTypeDef(TypedDict):
    InferenceComponentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateInferenceComponentRuntimeConfigOutputTypeDef(TypedDict):
    InferenceComponentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateInferenceExperimentResponseTypeDef(TypedDict):
    InferenceExperimentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMlflowAppResponseTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMlflowTrackingServerResponseTypeDef(TypedDict):
    TrackingServerArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateModelCardResponseTypeDef(TypedDict):
    ModelCardArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateModelPackageOutputTypeDef(TypedDict):
    ModelPackageArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMonitoringAlertResponseTypeDef(TypedDict):
    MonitoringScheduleArn: str
    MonitoringAlertName: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMonitoringScheduleResponseTypeDef(TypedDict):
    MonitoringScheduleArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePartnerAppResponseTypeDef(TypedDict):
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePipelineExecutionResponseTypeDef(TypedDict):
    PipelineExecutionArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePipelineResponseTypeDef(TypedDict):
    PipelineArn: str
    PipelineVersionId: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePipelineVersionResponseTypeDef(TypedDict):
    PipelineArn: str
    PipelineVersionId: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateProjectOutputTypeDef(TypedDict):
    ProjectArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSpaceResponseTypeDef(TypedDict):
    SpaceArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTrainingJobResponseTypeDef(TypedDict):
    TrainingJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTrialComponentResponseTypeDef(TypedDict):
    TrialComponentArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTrialResponseTypeDef(TypedDict):
    TrialArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateUserProfileResponseTypeDef(TypedDict):
    UserProfileArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class BatchAddClusterNodesRequestTypeDef(TypedDict):
    ClusterName: str
    NodesToAdd: Sequence[AddClusterNodeSpecificationTypeDef]
    ClientToken: NotRequired[str]


class AddTagsInputTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]


class AddTagsOutputTypeDef(TypedDict):
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateExperimentRequestTypeDef(TypedDict):
    ExperimentName: str
    DisplayName: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateHubContentReferenceRequestTypeDef(TypedDict):
    HubName: str
    SageMakerPublicHubContentArn: str
    HubContentName: NotRequired[str]
    MinVersion: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateImageRequestTypeDef(TypedDict):
    ImageName: str
    RoleArn: str
    Description: NotRequired[str]
    DisplayName: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateMlflowAppRequestTypeDef(TypedDict):
    Name: str
    ArtifactStoreUri: str
    RoleArn: str
    ModelRegistrationMode: NotRequired[ModelRegistrationModeType]
    WeeklyMaintenanceWindowStart: NotRequired[str]
    AccountDefaultStatus: NotRequired[AccountDefaultStatusType]
    DefaultDomainIdList: NotRequired[Sequence[str]]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateMlflowTrackingServerRequestTypeDef(TypedDict):
    TrackingServerName: str
    ArtifactStoreUri: str
    RoleArn: str
    TrackingServerSize: NotRequired[TrackingServerSizeType]
    MlflowVersion: NotRequired[str]
    AutomaticModelRegistration: NotRequired[bool]
    WeeklyMaintenanceWindowStart: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateModelPackageGroupInputTypeDef(TypedDict):
    ModelPackageGroupName: str
    ModelPackageGroupDescription: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateStudioLifecycleConfigRequestTypeDef(TypedDict):
    StudioLifecycleConfigName: str
    StudioLifecycleConfigContent: str
    StudioLifecycleConfigAppType: StudioLifecycleConfigAppTypeType
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateTrainingPlanRequestTypeDef(TypedDict):
    TrainingPlanName: str
    TrainingPlanOfferingId: str
    SpareInstanceCountPerUltraServer: NotRequired[int]
    Tags: NotRequired[Sequence[TagTypeDef]]


class ImportHubContentRequestTypeDef(TypedDict):
    HubContentName: str
    HubContentType: HubContentTypeType
    DocumentSchemaVersion: str
    HubName: str
    HubContentDocument: str
    HubContentVersion: NotRequired[str]
    HubContentDisplayName: NotRequired[str]
    HubContentDescription: NotRequired[str]
    HubContentMarkdown: NotRequired[str]
    SupportStatus: NotRequired[HubContentSupportStatusType]
    HubContentSearchKeywords: NotRequired[Sequence[str]]
    Tags: NotRequired[Sequence[TagTypeDef]]


class ListTagsOutputTypeDef(TypedDict):
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AutoRollbackConfigOutputTypeDef(TypedDict):
    Alarms: NotRequired[list[AlarmTypeDef]]


class AutoRollbackConfigTypeDef(TypedDict):
    Alarms: NotRequired[Sequence[AlarmTypeDef]]


class HyperParameterAlgorithmSpecificationOutputTypeDef(TypedDict):
    TrainingInputMode: TrainingInputModeType
    TrainingImage: NotRequired[str]
    AlgorithmName: NotRequired[str]
    MetricDefinitions: NotRequired[list[MetricDefinitionTypeDef]]


class HyperParameterAlgorithmSpecificationTypeDef(TypedDict):
    TrainingInputMode: TrainingInputModeType
    TrainingImage: NotRequired[str]
    AlgorithmName: NotRequired[str]
    MetricDefinitions: NotRequired[Sequence[MetricDefinitionTypeDef]]


class AlgorithmStatusDetailsTypeDef(TypedDict):
    ValidationStatuses: NotRequired[list[AlgorithmStatusItemTypeDef]]
    ImageScanStatuses: NotRequired[list[AlgorithmStatusItemTypeDef]]


class ListAlgorithmsOutputTypeDef(TypedDict):
    AlgorithmSummaryList: list[AlgorithmSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AppDetailsTypeDef(TypedDict):
    DomainId: NotRequired[str]
    UserProfileName: NotRequired[str]
    SpaceName: NotRequired[str]
    AppType: NotRequired[AppTypeType]
    AppName: NotRequired[str]
    Status: NotRequired[AppStatusType]
    CreationTime: NotRequired[datetime]
    ResourceSpec: NotRequired[ResourceSpecTypeDef]


class CreateAppRequestTypeDef(TypedDict):
    DomainId: str
    AppType: AppTypeType
    AppName: str
    UserProfileName: NotRequired[str]
    SpaceName: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ResourceSpec: NotRequired[ResourceSpecTypeDef]
    RecoveryMode: NotRequired[bool]


class DescribeAppResponseTypeDef(TypedDict):
    AppArn: str
    AppType: AppTypeType
    AppName: str
    DomainId: str
    UserProfileName: str
    SpaceName: str
    Status: AppStatusType
    EffectiveTrustedIdentityPropagationStatus: FeatureStatusType
    RecoveryMode: bool
    LastHealthCheckTimestamp: datetime
    LastUserActivityTimestamp: datetime
    CreationTime: datetime
    FailureReason: str
    ResourceSpec: ResourceSpecTypeDef
    BuiltInLifecycleConfigArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class RStudioServerProDomainSettingsForUpdateTypeDef(TypedDict):
    DomainExecutionRoleArn: str
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    RStudioConnectUrl: NotRequired[str]
    RStudioPackageManagerUrl: NotRequired[str]


class RStudioServerProDomainSettingsTypeDef(TypedDict):
    DomainExecutionRoleArn: str
    RStudioConnectUrl: NotRequired[str]
    RStudioPackageManagerUrl: NotRequired[str]
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]


class TensorBoardAppSettingsTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]


class AppLifecycleManagementTypeDef(TypedDict):
    IdleSettings: NotRequired[IdleSettingsTypeDef]


AppSpecificationUnionTypeDef = Union[AppSpecificationTypeDef, AppSpecificationOutputTypeDef]


class ArtifactSourceOutputTypeDef(TypedDict):
    SourceUri: str
    SourceTypes: NotRequired[list[ArtifactSourceTypeTypeDef]]


class ArtifactSourceTypeDef(TypedDict):
    SourceUri: str
    SourceTypes: NotRequired[Sequence[ArtifactSourceTypeTypeDef]]


class LineageMetadataTypeDef(TypedDict):
    ActionArns: NotRequired[dict[str, str]]
    ArtifactArns: NotRequired[dict[str, str]]
    ContextArns: NotRequired[dict[str, str]]
    Associations: NotRequired[list[AssociationInfoTypeDef]]


class AsyncInferenceOutputConfigOutputTypeDef(TypedDict):
    KmsKeyId: NotRequired[str]
    S3OutputPath: NotRequired[str]
    NotificationConfig: NotRequired[AsyncInferenceNotificationConfigOutputTypeDef]
    S3FailurePath: NotRequired[str]


class AsyncInferenceOutputConfigTypeDef(TypedDict):
    KmsKeyId: NotRequired[str]
    S3OutputPath: NotRequired[str]
    NotificationConfig: NotRequired[AsyncInferenceNotificationConfigTypeDef]
    S3FailurePath: NotRequired[str]


class CreateHubContentPresignedUrlsResponseTypeDef(TypedDict):
    AuthorizedUrlConfigs: list[AuthorizedUrlTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AutoMLCandidateGenerationConfigOutputTypeDef(TypedDict):
    FeatureSpecificationS3Uri: NotRequired[str]
    AlgorithmsConfig: NotRequired[list[AutoMLAlgorithmConfigOutputTypeDef]]


class CandidateGenerationConfigOutputTypeDef(TypedDict):
    AlgorithmsConfig: NotRequired[list[AutoMLAlgorithmConfigOutputTypeDef]]


class AutoMLCandidateGenerationConfigTypeDef(TypedDict):
    FeatureSpecificationS3Uri: NotRequired[str]
    AlgorithmsConfig: NotRequired[Sequence[AutoMLAlgorithmConfigTypeDef]]


class CandidateGenerationConfigTypeDef(TypedDict):
    AlgorithmsConfig: NotRequired[Sequence[AutoMLAlgorithmConfigTypeDef]]


class AutoMLComputeConfigTypeDef(TypedDict):
    EmrServerlessComputeConfig: NotRequired[EmrServerlessComputeConfigTypeDef]


class AutoMLDataSourceTypeDef(TypedDict):
    S3DataSource: AutoMLS3DataSourceTypeDef


class ImageClassificationJobConfigTypeDef(TypedDict):
    CompletionCriteria: NotRequired[AutoMLJobCompletionCriteriaTypeDef]


class TextClassificationJobConfigTypeDef(TypedDict):
    ContentColumn: str
    TargetLabelColumn: str
    CompletionCriteria: NotRequired[AutoMLJobCompletionCriteriaTypeDef]


class ResolvedAttributesTypeDef(TypedDict):
    AutoMLJobObjective: NotRequired[AutoMLJobObjectiveTypeDef]
    ProblemType: NotRequired[ProblemTypeType]
    CompletionCriteria: NotRequired[AutoMLJobCompletionCriteriaTypeDef]


class AutoMLJobSummaryTypeDef(TypedDict):
    AutoMLJobName: str
    AutoMLJobArn: str
    AutoMLJobStatus: AutoMLJobStatusType
    AutoMLJobSecondaryStatus: AutoMLJobSecondaryStatusType
    CreationTime: datetime
    LastModifiedTime: datetime
    EndTime: NotRequired[datetime]
    FailureReason: NotRequired[str]
    PartialFailureReasons: NotRequired[list[AutoMLPartialFailureReasonTypeDef]]


class AutoMLProblemTypeResolvedAttributesTypeDef(TypedDict):
    TabularResolvedAttributes: NotRequired[TabularResolvedAttributesTypeDef]
    TextGenerationResolvedAttributes: NotRequired[TextGenerationResolvedAttributesTypeDef]


class AutoMLSecurityConfigOutputTypeDef(TypedDict):
    VolumeKmsKeyId: NotRequired[str]
    EnableInterContainerTrafficEncryption: NotRequired[bool]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]


class LabelingJobResourceConfigOutputTypeDef(TypedDict):
    VolumeKmsKeyId: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]


class MonitoringNetworkConfigOutputTypeDef(TypedDict):
    EnableInterContainerTrafficEncryption: NotRequired[bool]
    EnableNetworkIsolation: NotRequired[bool]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]


class NetworkConfigOutputTypeDef(TypedDict):
    EnableInterContainerTrafficEncryption: NotRequired[bool]
    EnableNetworkIsolation: NotRequired[bool]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]


class AutoMLSecurityConfigTypeDef(TypedDict):
    VolumeKmsKeyId: NotRequired[str]
    EnableInterContainerTrafficEncryption: NotRequired[bool]
    VpcConfig: NotRequired[VpcConfigTypeDef]


class LabelingJobResourceConfigTypeDef(TypedDict):
    VolumeKmsKeyId: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigTypeDef]


class MonitoringNetworkConfigTypeDef(TypedDict):
    EnableInterContainerTrafficEncryption: NotRequired[bool]
    EnableNetworkIsolation: NotRequired[bool]
    VpcConfig: NotRequired[VpcConfigTypeDef]


class NetworkConfigTypeDef(TypedDict):
    EnableInterContainerTrafficEncryption: NotRequired[bool]
    EnableNetworkIsolation: NotRequired[bool]
    VpcConfig: NotRequired[VpcConfigTypeDef]


VpcConfigUnionTypeDef = Union[VpcConfigTypeDef, VpcConfigOutputTypeDef]


class BatchAddClusterNodesResponseTypeDef(TypedDict):
    Successful: list[NodeAdditionResultTypeDef]
    Failed: list[BatchAddClusterNodesErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchDeleteClusterNodesResponseTypeDef(TypedDict):
    Failed: list[BatchDeleteClusterNodesErrorTypeDef]
    Successful: list[str]
    FailedNodeLogicalIds: list[BatchDeleteClusterNodeLogicalIdsErrorTypeDef]
    SuccessfulNodeLogicalIds: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchRebootClusterNodesResponseTypeDef(TypedDict):
    Successful: list[str]
    Failed: list[BatchRebootClusterNodesErrorTypeDef]
    FailedNodeLogicalIds: list[BatchRebootClusterNodeLogicalIdsErrorTypeDef]
    SuccessfulNodeLogicalIds: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchReplaceClusterNodesResponseTypeDef(TypedDict):
    Successful: list[str]
    Failed: list[BatchReplaceClusterNodesErrorTypeDef]
    FailedNodeLogicalIds: list[BatchReplaceClusterNodeLogicalIdsErrorTypeDef]
    SuccessfulNodeLogicalIds: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class BiasTypeDef(TypedDict):
    Report: NotRequired[MetricsSourceTypeDef]
    PreTrainingReport: NotRequired[MetricsSourceTypeDef]
    PostTrainingReport: NotRequired[MetricsSourceTypeDef]


class DriftCheckModelDataQualityTypeDef(TypedDict):
    Statistics: NotRequired[MetricsSourceTypeDef]
    Constraints: NotRequired[MetricsSourceTypeDef]


class DriftCheckModelQualityTypeDef(TypedDict):
    Statistics: NotRequired[MetricsSourceTypeDef]
    Constraints: NotRequired[MetricsSourceTypeDef]


class ExplainabilityTypeDef(TypedDict):
    Report: NotRequired[MetricsSourceTypeDef]


class ModelDataQualityTypeDef(TypedDict):
    Statistics: NotRequired[MetricsSourceTypeDef]
    Constraints: NotRequired[MetricsSourceTypeDef]


class ModelQualityTypeDef(TypedDict):
    Statistics: NotRequired[MetricsSourceTypeDef]
    Constraints: NotRequired[MetricsSourceTypeDef]


class CallbackStepMetadataTypeDef(TypedDict):
    CallbackToken: NotRequired[str]
    SqsQueueUrl: NotRequired[str]
    OutputParameters: NotRequired[list[OutputParameterTypeDef]]


class LambdaStepMetadataTypeDef(TypedDict):
    Arn: NotRequired[str]
    OutputParameters: NotRequired[list[OutputParameterTypeDef]]


class SendPipelineExecutionStepSuccessRequestTypeDef(TypedDict):
    CallbackToken: str
    OutputParameters: NotRequired[Sequence[OutputParameterTypeDef]]
    ClientRequestToken: NotRequired[str]


class CandidatePropertiesTypeDef(TypedDict):
    CandidateArtifactLocations: NotRequired[CandidateArtifactLocationsTypeDef]
    CandidateMetrics: NotRequired[list[MetricDatumTypeDef]]


class CanvasAppSettingsOutputTypeDef(TypedDict):
    TimeSeriesForecastingSettings: NotRequired[TimeSeriesForecastingSettingsTypeDef]
    ModelRegisterSettings: NotRequired[ModelRegisterSettingsTypeDef]
    WorkspaceSettings: NotRequired[WorkspaceSettingsTypeDef]
    IdentityProviderOAuthSettings: NotRequired[list[IdentityProviderOAuthSettingTypeDef]]
    DirectDeploySettings: NotRequired[DirectDeploySettingsTypeDef]
    KendraSettings: NotRequired[KendraSettingsTypeDef]
    GenerativeAiSettings: NotRequired[GenerativeAiSettingsTypeDef]
    EmrServerlessSettings: NotRequired[EmrServerlessSettingsTypeDef]


class CanvasAppSettingsTypeDef(TypedDict):
    TimeSeriesForecastingSettings: NotRequired[TimeSeriesForecastingSettingsTypeDef]
    ModelRegisterSettings: NotRequired[ModelRegisterSettingsTypeDef]
    WorkspaceSettings: NotRequired[WorkspaceSettingsTypeDef]
    IdentityProviderOAuthSettings: NotRequired[Sequence[IdentityProviderOAuthSettingTypeDef]]
    DirectDeploySettings: NotRequired[DirectDeploySettingsTypeDef]
    KendraSettings: NotRequired[KendraSettingsTypeDef]
    GenerativeAiSettings: NotRequired[GenerativeAiSettingsTypeDef]
    EmrServerlessSettings: NotRequired[EmrServerlessSettingsTypeDef]


class InstanceGroupMetadataTypeDef(TypedDict):
    FailureMessage: NotRequired[str]
    AvailabilityZoneId: NotRequired[str]
    CapacityReservation: NotRequired[CapacityReservationTypeDef]
    SubnetId: NotRequired[str]
    SecurityGroupIds: NotRequired[list[str]]
    AmiOverride: NotRequired[str]


class InstanceMetadataTypeDef(TypedDict):
    CustomerEni: NotRequired[str]
    AdditionalEnis: NotRequired[AdditionalEnisTypeDef]
    CapacityReservation: NotRequired[CapacityReservationTypeDef]
    FailureMessage: NotRequired[str]
    LcsExecutionState: NotRequired[str]
    NodeLogicalId: NotRequired[str]


class RollingDeploymentPolicyTypeDef(TypedDict):
    MaximumBatchSize: CapacitySizeConfigTypeDef
    RollbackMaximumBatchSize: NotRequired[CapacitySizeConfigTypeDef]


class RollingUpdatePolicyTypeDef(TypedDict):
    MaximumBatchSize: CapacitySizeTypeDef
    WaitIntervalInSeconds: int
    MaximumExecutionTimeoutInSeconds: NotRequired[int]
    RollbackMaximumBatchSize: NotRequired[CapacitySizeTypeDef]


TrafficRoutingConfigTypeDef = TypedDict(
    "TrafficRoutingConfigTypeDef",
    {
        "Type": TrafficRoutingConfigTypeType,
        "WaitIntervalInSeconds": int,
        "CanarySize": NotRequired[CapacitySizeTypeDef],
        "LinearStepSize": NotRequired[CapacitySizeTypeDef],
    },
)


class InferenceExperimentDataStorageConfigOutputTypeDef(TypedDict):
    Destination: str
    KmsKey: NotRequired[str]
    ContentType: NotRequired[CaptureContentTypeHeaderOutputTypeDef]


class InferenceExperimentDataStorageConfigTypeDef(TypedDict):
    Destination: str
    KmsKey: NotRequired[str]
    ContentType: NotRequired[CaptureContentTypeHeaderTypeDef]


class DataCaptureConfigOutputTypeDef(TypedDict):
    InitialSamplingPercentage: int
    DestinationS3Uri: str
    CaptureOptions: list[CaptureOptionTypeDef]
    EnableCapture: NotRequired[bool]
    KmsKeyId: NotRequired[str]
    CaptureContentTypeHeader: NotRequired[CaptureContentTypeHeaderOutputTypeDef]


class DataCaptureConfigTypeDef(TypedDict):
    InitialSamplingPercentage: int
    DestinationS3Uri: str
    CaptureOptions: Sequence[CaptureOptionTypeDef]
    EnableCapture: NotRequired[bool]
    KmsKeyId: NotRequired[str]
    CaptureContentTypeHeader: NotRequired[CaptureContentTypeHeaderTypeDef]


class EnvironmentParameterRangesOutputTypeDef(TypedDict):
    CategoricalParameterRanges: NotRequired[list[CategoricalParameterOutputTypeDef]]


CategoricalParameterRangeUnionTypeDef = Union[
    CategoricalParameterRangeTypeDef, CategoricalParameterRangeOutputTypeDef
]


class EnvironmentParameterRangesTypeDef(TypedDict):
    CategoricalParameterRanges: NotRequired[Sequence[CategoricalParameterTypeDef]]


class CfnCreateTemplateProviderTypeDef(TypedDict):
    TemplateName: str
    TemplateURL: str
    RoleARN: NotRequired[str]
    Parameters: NotRequired[Sequence[CfnStackCreateParameterTypeDef]]


class CfnTemplateProviderDetailTypeDef(TypedDict):
    TemplateName: str
    TemplateURL: str
    RoleARN: NotRequired[str]
    Parameters: NotRequired[list[CfnStackParameterTypeDef]]
    StackDetail: NotRequired[CfnStackDetailTypeDef]


class CfnUpdateTemplateProviderTypeDef(TypedDict):
    TemplateName: str
    TemplateURL: str
    Parameters: NotRequired[Sequence[CfnStackUpdateParameterTypeDef]]


class ClarifyShapConfigTypeDef(TypedDict):
    ShapBaselineConfig: ClarifyShapBaselineConfigTypeDef
    NumberOfSamples: NotRequired[int]
    UseLogit: NotRequired[bool]
    Seed: NotRequired[int]
    TextConfig: NotRequired[ClarifyTextConfigTypeDef]


ClusterCapacityRequirementsUnionTypeDef = Union[
    ClusterCapacityRequirementsTypeDef, ClusterCapacityRequirementsOutputTypeDef
]


class ClusterInstanceStorageConfigTypeDef(TypedDict):
    EbsVolumeConfig: NotRequired[ClusterEbsVolumeConfigTypeDef]


class ListClusterEventsResponseTypeDef(TypedDict):
    Events: list[ClusterEventSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ClusterKubernetesConfigDetailsTypeDef(TypedDict):
    CurrentLabels: NotRequired[dict[str, str]]
    DesiredLabels: NotRequired[dict[str, str]]
    CurrentTaints: NotRequired[list[ClusterKubernetesTaintTypeDef]]
    DesiredTaints: NotRequired[list[ClusterKubernetesTaintTypeDef]]


class ClusterKubernetesConfigNodeDetailsTypeDef(TypedDict):
    CurrentLabels: NotRequired[dict[str, str]]
    DesiredLabels: NotRequired[dict[str, str]]
    CurrentTaints: NotRequired[list[ClusterKubernetesTaintTypeDef]]
    DesiredTaints: NotRequired[list[ClusterKubernetesTaintTypeDef]]


class ClusterKubernetesConfigTypeDef(TypedDict):
    Labels: NotRequired[Mapping[str, str]]
    Taints: NotRequired[Sequence[ClusterKubernetesTaintTypeDef]]


class ClusterNodeSummaryTypeDef(TypedDict):
    InstanceGroupName: str
    InstanceId: str
    InstanceType: ClusterInstanceTypeType
    LaunchTime: datetime
    InstanceStatus: ClusterInstanceStatusDetailsTypeDef
    NodeLogicalId: NotRequired[str]
    LastSoftwareUpdateTime: NotRequired[datetime]
    UltraServerInfo: NotRequired[UltraServerInfoTypeDef]
    PrivateDnsHostname: NotRequired[str]


class ClusterOrchestratorTypeDef(TypedDict):
    Eks: NotRequired[ClusterOrchestratorEksConfigTypeDef]


class ListClusterSchedulerConfigsResponseTypeDef(TypedDict):
    ClusterSchedulerConfigSummaries: list[ClusterSchedulerConfigSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListClustersResponseTypeDef(TypedDict):
    ClusterSummaries: list[ClusterSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CodeEditorAppImageConfigOutputTypeDef(TypedDict):
    FileSystemConfig: NotRequired[FileSystemConfigTypeDef]
    ContainerConfig: NotRequired[ContainerConfigOutputTypeDef]


class JupyterLabAppImageConfigOutputTypeDef(TypedDict):
    FileSystemConfig: NotRequired[FileSystemConfigTypeDef]
    ContainerConfig: NotRequired[ContainerConfigOutputTypeDef]


class CodeEditorAppImageConfigTypeDef(TypedDict):
    FileSystemConfig: NotRequired[FileSystemConfigTypeDef]
    ContainerConfig: NotRequired[ContainerConfigTypeDef]


class JupyterLabAppImageConfigTypeDef(TypedDict):
    FileSystemConfig: NotRequired[FileSystemConfigTypeDef]
    ContainerConfig: NotRequired[ContainerConfigTypeDef]


class KernelGatewayAppSettingsOutputTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    CustomImages: NotRequired[list[CustomImageTypeDef]]
    LifecycleConfigArns: NotRequired[list[str]]


class KernelGatewayAppSettingsTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    CustomImages: NotRequired[Sequence[CustomImageTypeDef]]
    LifecycleConfigArns: NotRequired[Sequence[str]]


class RSessionAppSettingsOutputTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    CustomImages: NotRequired[list[CustomImageTypeDef]]


class RSessionAppSettingsTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    CustomImages: NotRequired[Sequence[CustomImageTypeDef]]


class CodeRepositorySummaryTypeDef(TypedDict):
    CodeRepositoryName: str
    CodeRepositoryArn: str
    CreationTime: datetime
    LastModifiedTime: datetime
    GitConfig: NotRequired[GitConfigTypeDef]


class CreateCodeRepositoryInputTypeDef(TypedDict):
    CodeRepositoryName: str
    GitConfig: GitConfigTypeDef
    Tags: NotRequired[Sequence[TagTypeDef]]


class DescribeCodeRepositoryOutputTypeDef(TypedDict):
    CodeRepositoryName: str
    CodeRepositoryArn: str
    CreationTime: datetime
    LastModifiedTime: datetime
    GitConfig: GitConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class JupyterServerAppSettingsOutputTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    LifecycleConfigArns: NotRequired[list[str]]
    CodeRepositories: NotRequired[list[CodeRepositoryTypeDef]]


class JupyterServerAppSettingsTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    LifecycleConfigArns: NotRequired[Sequence[str]]
    CodeRepositories: NotRequired[Sequence[CodeRepositoryTypeDef]]


class CollectionConfigTypeDef(TypedDict):
    VectorConfig: NotRequired[VectorConfigTypeDef]


class DebugHookConfigOutputTypeDef(TypedDict):
    S3OutputPath: str
    LocalPath: NotRequired[str]
    HookParameters: NotRequired[dict[str, str]]
    CollectionConfigurations: NotRequired[list[CollectionConfigurationOutputTypeDef]]


class DebugHookConfigTypeDef(TypedDict):
    S3OutputPath: str
    LocalPath: NotRequired[str]
    HookParameters: NotRequired[Mapping[str, str]]
    CollectionConfigurations: NotRequired[Sequence[CollectionConfigurationTypeDef]]


class ListCompilationJobsResponseTypeDef(TypedDict):
    CompilationJobSummaries: list[CompilationJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ContextSummaryTypeDef(TypedDict):
    ContextArn: NotRequired[str]
    ContextName: NotRequired[str]
    Source: NotRequired[ContextSourceTypeDef]
    ContextType: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]


class CreateContextRequestTypeDef(TypedDict):
    ContextName: str
    Source: ContextSourceTypeDef
    ContextType: str
    Description: NotRequired[str]
    Properties: NotRequired[Mapping[str, str]]
    Tags: NotRequired[Sequence[TagTypeDef]]


class TuningJobCompletionCriteriaTypeDef(TypedDict):
    TargetObjectiveMetricValue: NotRequired[float]
    BestObjectiveNotImproving: NotRequired[BestObjectiveNotImprovingTypeDef]
    ConvergenceDetected: NotRequired[ConvergenceDetectedTypeDef]


class CreateActionRequestTypeDef(TypedDict):
    ActionName: str
    Source: ActionSourceTypeDef
    ActionType: str
    Description: NotRequired[str]
    Status: NotRequired[ActionStatusType]
    Properties: NotRequired[Mapping[str, str]]
    MetadataProperties: NotRequired[MetadataPropertiesTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateTrialRequestTypeDef(TypedDict):
    TrialName: str
    ExperimentName: str
    DisplayName: NotRequired[str]
    MetadataProperties: NotRequired[MetadataPropertiesTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateDeviceFleetRequestTypeDef(TypedDict):
    DeviceFleetName: str
    OutputConfig: EdgeOutputConfigTypeDef
    RoleArn: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    EnableIotRoleAlias: NotRequired[bool]


class CreateEdgePackagingJobRequestTypeDef(TypedDict):
    EdgePackagingJobName: str
    CompilationJobName: str
    ModelName: str
    ModelVersion: str
    RoleArn: str
    OutputConfig: EdgeOutputConfigTypeDef
    ResourceKey: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class DescribeDeviceFleetResponseTypeDef(TypedDict):
    DeviceFleetName: str
    DeviceFleetArn: str
    OutputConfig: EdgeOutputConfigTypeDef
    Description: str
    CreationTime: datetime
    LastModifiedTime: datetime
    RoleArn: str
    IotRoleAlias: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDeviceFleetRequestTypeDef(TypedDict):
    DeviceFleetName: str
    OutputConfig: EdgeOutputConfigTypeDef
    RoleArn: NotRequired[str]
    Description: NotRequired[str]
    EnableIotRoleAlias: NotRequired[bool]


class ListAliasesRequestPaginateTypeDef(TypedDict):
    ImageName: str
    Alias: NotRequired[str]
    Version: NotRequired[int]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAppsRequestPaginateTypeDef(TypedDict):
    SortOrder: NotRequired[SortOrderType]
    SortBy: NotRequired[Literal["CreationTime"]]
    DomainIdEquals: NotRequired[str]
    UserProfileNameEquals: NotRequired[str]
    SpaceNameEquals: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCandidatesForAutoMLJobRequestPaginateTypeDef(TypedDict):
    AutoMLJobName: str
    StatusEquals: NotRequired[CandidateStatusType]
    CandidateNameEquals: NotRequired[str]
    SortOrder: NotRequired[AutoMLSortOrderType]
    SortBy: NotRequired[CandidateSortByType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDomainsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListInferenceRecommendationsJobStepsRequestPaginateTypeDef(TypedDict):
    JobName: str
    Status: NotRequired[RecommendationJobStatusType]
    StepType: NotRequired[Literal["BENCHMARK"]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMonitoringAlertsRequestPaginateTypeDef(TypedDict):
    MonitoringScheduleName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPartnerAppsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPipelineExecutionStepsRequestPaginateTypeDef(TypedDict):
    PipelineExecutionArn: NotRequired[str]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPipelineParametersForExecutionRequestPaginateTypeDef(TypedDict):
    PipelineExecutionArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSpacesRequestPaginateTypeDef(TypedDict):
    SortOrder: NotRequired[SortOrderType]
    SortBy: NotRequired[SpaceSortKeyType]
    DomainIdEquals: NotRequired[str]
    SpaceNameContains: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListStageDevicesRequestPaginateTypeDef(TypedDict):
    EdgeDeploymentPlanName: str
    StageName: str
    ExcludeDevicesDeployedInOtherStage: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSubscribedWorkteamsRequestPaginateTypeDef(TypedDict):
    NameContains: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTagsInputPaginateTypeDef(TypedDict):
    ResourceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTrainingJobsForHyperParameterTuningJobRequestPaginateTypeDef(TypedDict):
    HyperParameterTuningJobName: str
    StatusEquals: NotRequired[TrainingJobStatusType]
    SortBy: NotRequired[TrainingJobSortByOptionsType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListUltraServersByReservedCapacityRequestPaginateTypeDef(TypedDict):
    ReservedCapacityArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListUserProfilesRequestPaginateTypeDef(TypedDict):
    SortOrder: NotRequired[SortOrderType]
    SortBy: NotRequired[UserProfileSortKeyType]
    DomainIdEquals: NotRequired[str]
    UserProfileNameContains: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWorkforcesRequestPaginateTypeDef(TypedDict):
    SortBy: NotRequired[ListWorkforcesSortByOptionsType]
    SortOrder: NotRequired[SortOrderType]
    NameContains: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListWorkteamsRequestPaginateTypeDef(TypedDict):
    SortBy: NotRequired[ListWorkteamsSortByOptionsType]
    SortOrder: NotRequired[SortOrderType]
    NameContains: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class CreateHubContentPresignedUrlsRequestPaginateTypeDef(TypedDict):
    HubName: str
    HubContentType: HubContentTypeType
    HubContentName: str
    HubContentVersion: NotRequired[str]
    AccessConfig: NotRequired[PresignedUrlAccessConfigTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class CreateHubContentPresignedUrlsRequestTypeDef(TypedDict):
    HubName: str
    HubContentType: HubContentTypeType
    HubContentName: str
    HubContentVersion: NotRequired[str]
    AccessConfig: NotRequired[PresignedUrlAccessConfigTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class CreateHubRequestTypeDef(TypedDict):
    HubName: str
    HubDescription: str
    HubDisplayName: NotRequired[str]
    HubSearchKeywords: NotRequired[Sequence[str]]
    S3StorageConfig: NotRequired[HubS3StorageConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class DescribeHubResponseTypeDef(TypedDict):
    HubName: str
    HubArn: str
    HubDisplayName: str
    HubDescription: str
    HubSearchKeywords: list[str]
    S3StorageConfig: HubS3StorageConfigTypeDef
    HubStatus: HubStatusType
    FailureReason: str
    CreationTime: datetime
    LastModifiedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class CreateHumanTaskUiRequestTypeDef(TypedDict):
    HumanTaskUiName: str
    UiTemplate: UiTemplateTypeDef
    Tags: NotRequired[Sequence[TagTypeDef]]


class UpdateInferenceComponentRuntimeConfigInputTypeDef(TypedDict):
    InferenceComponentName: str
    DesiredRuntimeConfig: InferenceComponentRuntimeConfigTypeDef


class CreateModelCardExportJobRequestTypeDef(TypedDict):
    ModelCardName: str
    ModelCardExportJobName: str
    OutputConfig: ModelCardExportOutputConfigTypeDef
    ModelCardVersion: NotRequired[int]


class CreateModelCardRequestTypeDef(TypedDict):
    ModelCardName: str
    Content: str
    ModelCardStatus: ModelCardStatusType
    SecurityConfig: NotRequired[ModelCardSecurityConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class ModelPackageSummaryTypeDef(TypedDict):
    ModelPackageArn: str
    CreationTime: datetime
    ModelPackageStatus: ModelPackageStatusType
    ModelPackageName: NotRequired[str]
    ModelPackageGroupName: NotRequired[str]
    ModelPackageVersion: NotRequired[int]
    ModelPackageDescription: NotRequired[str]
    ModelApprovalStatus: NotRequired[ModelApprovalStatusType]
    ModelLifeCycle: NotRequired[ModelLifeCycleTypeDef]
    ModelPackageRegistrationType: NotRequired[ModelPackageRegistrationTypeType]


class CreateNotebookInstanceInputTypeDef(TypedDict):
    NotebookInstanceName: str
    InstanceType: InstanceTypeType
    RoleArn: str
    SubnetId: NotRequired[str]
    SecurityGroupIds: NotRequired[Sequence[str]]
    IpAddressType: NotRequired[IPAddressTypeType]
    KmsKeyId: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    LifecycleConfigName: NotRequired[str]
    DirectInternetAccess: NotRequired[DirectInternetAccessType]
    VolumeSizeInGB: NotRequired[int]
    AcceleratorTypes: NotRequired[Sequence[NotebookInstanceAcceleratorTypeType]]
    DefaultCodeRepository: NotRequired[str]
    AdditionalCodeRepositories: NotRequired[Sequence[str]]
    RootAccess: NotRequired[RootAccessType]
    PlatformIdentifier: NotRequired[str]
    InstanceMetadataServiceConfiguration: NotRequired[InstanceMetadataServiceConfigurationTypeDef]


class DescribeNotebookInstanceOutputTypeDef(TypedDict):
    NotebookInstanceArn: str
    NotebookInstanceName: str
    NotebookInstanceStatus: NotebookInstanceStatusType
    FailureReason: str
    Url: str
    InstanceType: InstanceTypeType
    IpAddressType: IPAddressTypeType
    SubnetId: str
    SecurityGroups: list[str]
    RoleArn: str
    KmsKeyId: str
    NetworkInterfaceId: str
    LastModifiedTime: datetime
    CreationTime: datetime
    NotebookInstanceLifecycleConfigName: str
    DirectInternetAccess: DirectInternetAccessType
    VolumeSizeInGB: int
    AcceleratorTypes: list[NotebookInstanceAcceleratorTypeType]
    DefaultCodeRepository: str
    AdditionalCodeRepositories: list[str]
    RootAccess: RootAccessType
    PlatformIdentifier: str
    InstanceMetadataServiceConfiguration: InstanceMetadataServiceConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateNotebookInstanceInputTypeDef(TypedDict):
    NotebookInstanceName: str
    InstanceType: NotRequired[InstanceTypeType]
    IpAddressType: NotRequired[IPAddressTypeType]
    PlatformIdentifier: NotRequired[str]
    RoleArn: NotRequired[str]
    LifecycleConfigName: NotRequired[str]
    DisassociateLifecycleConfig: NotRequired[bool]
    VolumeSizeInGB: NotRequired[int]
    DefaultCodeRepository: NotRequired[str]
    AdditionalCodeRepositories: NotRequired[Sequence[str]]
    AcceleratorTypes: NotRequired[Sequence[NotebookInstanceAcceleratorTypeType]]
    DisassociateAcceleratorTypes: NotRequired[bool]
    DisassociateDefaultCodeRepository: NotRequired[bool]
    DisassociateAdditionalCodeRepositories: NotRequired[bool]
    RootAccess: NotRequired[RootAccessType]
    InstanceMetadataServiceConfiguration: NotRequired[InstanceMetadataServiceConfigurationTypeDef]


class CreateNotebookInstanceLifecycleConfigInputTypeDef(TypedDict):
    NotebookInstanceLifecycleConfigName: str
    OnCreate: NotRequired[Sequence[NotebookInstanceLifecycleHookTypeDef]]
    OnStart: NotRequired[Sequence[NotebookInstanceLifecycleHookTypeDef]]
    Tags: NotRequired[Sequence[TagTypeDef]]


class DescribeNotebookInstanceLifecycleConfigOutputTypeDef(TypedDict):
    NotebookInstanceLifecycleConfigArn: str
    NotebookInstanceLifecycleConfigName: str
    OnCreate: list[NotebookInstanceLifecycleHookTypeDef]
    OnStart: list[NotebookInstanceLifecycleHookTypeDef]
    LastModifiedTime: datetime
    CreationTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateNotebookInstanceLifecycleConfigInputTypeDef(TypedDict):
    NotebookInstanceLifecycleConfigName: str
    OnCreate: NotRequired[Sequence[NotebookInstanceLifecycleHookTypeDef]]
    OnStart: NotRequired[Sequence[NotebookInstanceLifecycleHookTypeDef]]


class RetryPipelineExecutionRequestTypeDef(TypedDict):
    PipelineExecutionArn: str
    ClientRequestToken: str
    ParallelismConfiguration: NotRequired[ParallelismConfigurationTypeDef]


class UpdatePipelineExecutionRequestTypeDef(TypedDict):
    PipelineExecutionArn: str
    PipelineExecutionDescription: NotRequired[str]
    PipelineExecutionDisplayName: NotRequired[str]
    ParallelismConfiguration: NotRequired[ParallelismConfigurationTypeDef]


class CreatePipelineRequestTypeDef(TypedDict):
    PipelineName: str
    ClientRequestToken: str
    RoleArn: str
    PipelineDisplayName: NotRequired[str]
    PipelineDefinition: NotRequired[str]
    PipelineDefinitionS3Location: NotRequired[PipelineDefinitionS3LocationTypeDef]
    PipelineDescription: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ParallelismConfiguration: NotRequired[ParallelismConfigurationTypeDef]


class UpdatePipelineRequestTypeDef(TypedDict):
    PipelineName: str
    PipelineDisplayName: NotRequired[str]
    PipelineDefinition: NotRequired[str]
    PipelineDefinitionS3Location: NotRequired[PipelineDefinitionS3LocationTypeDef]
    PipelineDescription: NotRequired[str]
    RoleArn: NotRequired[str]
    ParallelismConfiguration: NotRequired[ParallelismConfigurationTypeDef]


class InferenceExperimentScheduleTypeDef(TypedDict):
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]


class ListActionsRequestPaginateTypeDef(TypedDict):
    SourceUri: NotRequired[str]
    ActionType: NotRequired[str]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortActionsByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListActionsRequestTypeDef(TypedDict):
    SourceUri: NotRequired[str]
    ActionType: NotRequired[str]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortActionsByType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListAlgorithmsInputPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    SortBy: NotRequired[AlgorithmSortByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAlgorithmsInputTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    NextToken: NotRequired[str]
    SortBy: NotRequired[AlgorithmSortByType]
    SortOrder: NotRequired[SortOrderType]


class ListAppImageConfigsRequestPaginateTypeDef(TypedDict):
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    ModifiedTimeBefore: NotRequired[TimestampTypeDef]
    ModifiedTimeAfter: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[AppImageConfigSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAppImageConfigsRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    ModifiedTimeBefore: NotRequired[TimestampTypeDef]
    ModifiedTimeAfter: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[AppImageConfigSortKeyType]
    SortOrder: NotRequired[SortOrderType]


class ListArtifactsRequestPaginateTypeDef(TypedDict):
    SourceUri: NotRequired[str]
    ArtifactType: NotRequired[str]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[Literal["CreationTime"]]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListArtifactsRequestTypeDef(TypedDict):
    SourceUri: NotRequired[str]
    ArtifactType: NotRequired[str]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[Literal["CreationTime"]]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListAssociationsRequestPaginateTypeDef(TypedDict):
    SourceArn: NotRequired[str]
    DestinationArn: NotRequired[str]
    SourceType: NotRequired[str]
    DestinationType: NotRequired[str]
    AssociationType: NotRequired[AssociationEdgeTypeType]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortAssociationsByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAssociationsRequestTypeDef(TypedDict):
    SourceArn: NotRequired[str]
    DestinationArn: NotRequired[str]
    SourceType: NotRequired[str]
    DestinationType: NotRequired[str]
    AssociationType: NotRequired[AssociationEdgeTypeType]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortAssociationsByType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListAutoMLJobsRequestPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[AutoMLJobStatusType]
    SortOrder: NotRequired[AutoMLSortOrderType]
    SortBy: NotRequired[AutoMLSortByType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAutoMLJobsRequestTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[AutoMLJobStatusType]
    SortOrder: NotRequired[AutoMLSortOrderType]
    SortBy: NotRequired[AutoMLSortByType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListClusterEventsRequestPaginateTypeDef(TypedDict):
    ClusterName: str
    InstanceGroupName: NotRequired[str]
    NodeId: NotRequired[str]
    EventTimeAfter: NotRequired[TimestampTypeDef]
    EventTimeBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[Literal["EventTime"]]
    SortOrder: NotRequired[SortOrderType]
    ResourceType: NotRequired[ClusterEventResourceTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListClusterEventsRequestTypeDef(TypedDict):
    ClusterName: str
    InstanceGroupName: NotRequired[str]
    NodeId: NotRequired[str]
    EventTimeAfter: NotRequired[TimestampTypeDef]
    EventTimeBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[Literal["EventTime"]]
    SortOrder: NotRequired[SortOrderType]
    ResourceType: NotRequired[ClusterEventResourceTypeType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListClusterNodesRequestPaginateTypeDef(TypedDict):
    ClusterName: str
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    InstanceGroupNameContains: NotRequired[str]
    SortBy: NotRequired[ClusterSortByType]
    SortOrder: NotRequired[SortOrderType]
    IncludeNodeLogicalIds: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListClusterNodesRequestTypeDef(TypedDict):
    ClusterName: str
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    InstanceGroupNameContains: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    SortBy: NotRequired[ClusterSortByType]
    SortOrder: NotRequired[SortOrderType]
    IncludeNodeLogicalIds: NotRequired[bool]


class ListClusterSchedulerConfigsRequestPaginateTypeDef(TypedDict):
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    ClusterArn: NotRequired[str]
    Status: NotRequired[SchedulerResourceStatusType]
    SortBy: NotRequired[SortClusterSchedulerConfigByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListClusterSchedulerConfigsRequestTypeDef(TypedDict):
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    ClusterArn: NotRequired[str]
    Status: NotRequired[SchedulerResourceStatusType]
    SortBy: NotRequired[SortClusterSchedulerConfigByType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListClustersRequestPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    SortBy: NotRequired[ClusterSortByType]
    SortOrder: NotRequired[SortOrderType]
    TrainingPlanArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListClustersRequestTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    NextToken: NotRequired[str]
    SortBy: NotRequired[ClusterSortByType]
    SortOrder: NotRequired[SortOrderType]
    TrainingPlanArn: NotRequired[str]


class ListCodeRepositoriesInputPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    SortBy: NotRequired[CodeRepositorySortByType]
    SortOrder: NotRequired[CodeRepositorySortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCodeRepositoriesInputTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    NextToken: NotRequired[str]
    SortBy: NotRequired[CodeRepositorySortByType]
    SortOrder: NotRequired[CodeRepositorySortOrderType]


class ListCompilationJobsRequestPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[CompilationJobStatusType]
    SortBy: NotRequired[ListCompilationJobsSortByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCompilationJobsRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[CompilationJobStatusType]
    SortBy: NotRequired[ListCompilationJobsSortByType]
    SortOrder: NotRequired[SortOrderType]


class ListComputeQuotasRequestPaginateTypeDef(TypedDict):
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    Status: NotRequired[SchedulerResourceStatusType]
    ClusterArn: NotRequired[str]
    SortBy: NotRequired[SortQuotaByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListComputeQuotasRequestTypeDef(TypedDict):
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    Status: NotRequired[SchedulerResourceStatusType]
    ClusterArn: NotRequired[str]
    SortBy: NotRequired[SortQuotaByType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListContextsRequestPaginateTypeDef(TypedDict):
    SourceUri: NotRequired[str]
    ContextType: NotRequired[str]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortContextsByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListContextsRequestTypeDef(TypedDict):
    SourceUri: NotRequired[str]
    ContextType: NotRequired[str]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortContextsByType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListDataQualityJobDefinitionsRequestPaginateTypeDef(TypedDict):
    EndpointName: NotRequired[str]
    SortBy: NotRequired[MonitoringJobDefinitionSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataQualityJobDefinitionsRequestTypeDef(TypedDict):
    EndpointName: NotRequired[str]
    SortBy: NotRequired[MonitoringJobDefinitionSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]


class ListDeviceFleetsRequestPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    SortBy: NotRequired[ListDeviceFleetsSortByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDeviceFleetsRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    SortBy: NotRequired[ListDeviceFleetsSortByType]
    SortOrder: NotRequired[SortOrderType]


class ListDevicesRequestPaginateTypeDef(TypedDict):
    LatestHeartbeatAfter: NotRequired[TimestampTypeDef]
    ModelName: NotRequired[str]
    DeviceFleetName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDevicesRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    LatestHeartbeatAfter: NotRequired[TimestampTypeDef]
    ModelName: NotRequired[str]
    DeviceFleetName: NotRequired[str]


class ListEdgeDeploymentPlansRequestPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    DeviceFleetNameContains: NotRequired[str]
    SortBy: NotRequired[ListEdgeDeploymentPlansSortByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEdgeDeploymentPlansRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    DeviceFleetNameContains: NotRequired[str]
    SortBy: NotRequired[ListEdgeDeploymentPlansSortByType]
    SortOrder: NotRequired[SortOrderType]


class ListEdgePackagingJobsRequestPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    ModelNameContains: NotRequired[str]
    StatusEquals: NotRequired[EdgePackagingJobStatusType]
    SortBy: NotRequired[ListEdgePackagingJobsSortByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEdgePackagingJobsRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    ModelNameContains: NotRequired[str]
    StatusEquals: NotRequired[EdgePackagingJobStatusType]
    SortBy: NotRequired[ListEdgePackagingJobsSortByType]
    SortOrder: NotRequired[SortOrderType]


class ListEndpointConfigsInputPaginateTypeDef(TypedDict):
    SortBy: NotRequired[EndpointConfigSortKeyType]
    SortOrder: NotRequired[OrderKeyType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEndpointConfigsInputTypeDef(TypedDict):
    SortBy: NotRequired[EndpointConfigSortKeyType]
    SortOrder: NotRequired[OrderKeyType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]


class ListEndpointsInputPaginateTypeDef(TypedDict):
    SortBy: NotRequired[EndpointSortKeyType]
    SortOrder: NotRequired[OrderKeyType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[EndpointStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEndpointsInputTypeDef(TypedDict):
    SortBy: NotRequired[EndpointSortKeyType]
    SortOrder: NotRequired[OrderKeyType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[EndpointStatusType]


class ListExperimentsRequestPaginateTypeDef(TypedDict):
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortExperimentsByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListExperimentsRequestTypeDef(TypedDict):
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortExperimentsByType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListFeatureGroupsRequestPaginateTypeDef(TypedDict):
    NameContains: NotRequired[str]
    FeatureGroupStatusEquals: NotRequired[FeatureGroupStatusType]
    OfflineStoreStatusEquals: NotRequired[OfflineStoreStatusValueType]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    SortOrder: NotRequired[FeatureGroupSortOrderType]
    SortBy: NotRequired[FeatureGroupSortByType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFeatureGroupsRequestTypeDef(TypedDict):
    NameContains: NotRequired[str]
    FeatureGroupStatusEquals: NotRequired[FeatureGroupStatusType]
    OfflineStoreStatusEquals: NotRequired[OfflineStoreStatusValueType]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    SortOrder: NotRequired[FeatureGroupSortOrderType]
    SortBy: NotRequired[FeatureGroupSortByType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListFlowDefinitionsRequestPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFlowDefinitionsRequestTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListHubContentVersionsRequestTypeDef(TypedDict):
    HubName: str
    HubContentType: HubContentTypeType
    HubContentName: str
    MinVersion: NotRequired[str]
    MaxSchemaVersion: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[HubContentSortByType]
    SortOrder: NotRequired[SortOrderType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListHubContentsRequestTypeDef(TypedDict):
    HubName: str
    HubContentType: HubContentTypeType
    NameContains: NotRequired[str]
    MaxSchemaVersion: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[HubContentSortByType]
    SortOrder: NotRequired[SortOrderType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListHubsRequestTypeDef(TypedDict):
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[HubSortByType]
    SortOrder: NotRequired[SortOrderType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListHumanTaskUisRequestPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListHumanTaskUisRequestTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListHyperParameterTuningJobsRequestPaginateTypeDef(TypedDict):
    SortBy: NotRequired[HyperParameterTuningJobSortByOptionsType]
    SortOrder: NotRequired[SortOrderType]
    NameContains: NotRequired[str]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[HyperParameterTuningJobStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListHyperParameterTuningJobsRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SortBy: NotRequired[HyperParameterTuningJobSortByOptionsType]
    SortOrder: NotRequired[SortOrderType]
    NameContains: NotRequired[str]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[HyperParameterTuningJobStatusType]


class ListImageVersionsRequestPaginateTypeDef(TypedDict):
    ImageName: str
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[ImageVersionSortByType]
    SortOrder: NotRequired[ImageVersionSortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListImageVersionsRequestTypeDef(TypedDict):
    ImageName: str
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    SortBy: NotRequired[ImageVersionSortByType]
    SortOrder: NotRequired[ImageVersionSortOrderType]


class ListImagesRequestPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    SortBy: NotRequired[ImageSortByType]
    SortOrder: NotRequired[ImageSortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListImagesRequestTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    NextToken: NotRequired[str]
    SortBy: NotRequired[ImageSortByType]
    SortOrder: NotRequired[ImageSortOrderType]


class ListInferenceComponentsInputPaginateTypeDef(TypedDict):
    SortBy: NotRequired[InferenceComponentSortKeyType]
    SortOrder: NotRequired[OrderKeyType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[InferenceComponentStatusType]
    EndpointNameEquals: NotRequired[str]
    VariantNameEquals: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListInferenceComponentsInputTypeDef(TypedDict):
    SortBy: NotRequired[InferenceComponentSortKeyType]
    SortOrder: NotRequired[OrderKeyType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[InferenceComponentStatusType]
    EndpointNameEquals: NotRequired[str]
    VariantNameEquals: NotRequired[str]


ListInferenceExperimentsRequestPaginateTypeDef = TypedDict(
    "ListInferenceExperimentsRequestPaginateTypeDef",
    {
        "NameContains": NotRequired[str],
        "Type": NotRequired[Literal["ShadowMode"]],
        "StatusEquals": NotRequired[InferenceExperimentStatusType],
        "CreationTimeAfter": NotRequired[TimestampTypeDef],
        "CreationTimeBefore": NotRequired[TimestampTypeDef],
        "LastModifiedTimeAfter": NotRequired[TimestampTypeDef],
        "LastModifiedTimeBefore": NotRequired[TimestampTypeDef],
        "SortBy": NotRequired[SortInferenceExperimentsByType],
        "SortOrder": NotRequired[SortOrderType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListInferenceExperimentsRequestTypeDef = TypedDict(
    "ListInferenceExperimentsRequestTypeDef",
    {
        "NameContains": NotRequired[str],
        "Type": NotRequired[Literal["ShadowMode"]],
        "StatusEquals": NotRequired[InferenceExperimentStatusType],
        "CreationTimeAfter": NotRequired[TimestampTypeDef],
        "CreationTimeBefore": NotRequired[TimestampTypeDef],
        "LastModifiedTimeAfter": NotRequired[TimestampTypeDef],
        "LastModifiedTimeBefore": NotRequired[TimestampTypeDef],
        "SortBy": NotRequired[SortInferenceExperimentsByType],
        "SortOrder": NotRequired[SortOrderType],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)


class ListInferenceRecommendationsJobsRequestPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[RecommendationJobStatusType]
    SortBy: NotRequired[ListInferenceRecommendationsJobsSortByType]
    SortOrder: NotRequired[SortOrderType]
    ModelNameEquals: NotRequired[str]
    ModelPackageVersionArnEquals: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListInferenceRecommendationsJobsRequestTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[RecommendationJobStatusType]
    SortBy: NotRequired[ListInferenceRecommendationsJobsSortByType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ModelNameEquals: NotRequired[str]
    ModelPackageVersionArnEquals: NotRequired[str]


class ListLabelingJobsForWorkteamRequestPaginateTypeDef(TypedDict):
    WorkteamArn: str
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    JobReferenceCodeContains: NotRequired[str]
    SortBy: NotRequired[Literal["CreationTime"]]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListLabelingJobsForWorkteamRequestTypeDef(TypedDict):
    WorkteamArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    JobReferenceCodeContains: NotRequired[str]
    SortBy: NotRequired[Literal["CreationTime"]]
    SortOrder: NotRequired[SortOrderType]


class ListLabelingJobsRequestPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    SortBy: NotRequired[SortByType]
    SortOrder: NotRequired[SortOrderType]
    StatusEquals: NotRequired[LabelingJobStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListLabelingJobsRequestTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    NameContains: NotRequired[str]
    SortBy: NotRequired[SortByType]
    SortOrder: NotRequired[SortOrderType]
    StatusEquals: NotRequired[LabelingJobStatusType]


class ListLineageGroupsRequestPaginateTypeDef(TypedDict):
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortLineageGroupsByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListLineageGroupsRequestTypeDef(TypedDict):
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortLineageGroupsByType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListMlflowAppsRequestPaginateTypeDef(TypedDict):
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    Status: NotRequired[MlflowAppStatusType]
    MlflowVersion: NotRequired[str]
    DefaultForDomainId: NotRequired[str]
    AccountDefaultStatus: NotRequired[AccountDefaultStatusType]
    SortBy: NotRequired[SortMlflowAppByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMlflowAppsRequestTypeDef(TypedDict):
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    Status: NotRequired[MlflowAppStatusType]
    MlflowVersion: NotRequired[str]
    DefaultForDomainId: NotRequired[str]
    AccountDefaultStatus: NotRequired[AccountDefaultStatusType]
    SortBy: NotRequired[SortMlflowAppByType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListMlflowTrackingServersRequestPaginateTypeDef(TypedDict):
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    TrackingServerStatus: NotRequired[TrackingServerStatusType]
    MlflowVersion: NotRequired[str]
    SortBy: NotRequired[SortTrackingServerByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMlflowTrackingServersRequestTypeDef(TypedDict):
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    TrackingServerStatus: NotRequired[TrackingServerStatusType]
    MlflowVersion: NotRequired[str]
    SortBy: NotRequired[SortTrackingServerByType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListModelBiasJobDefinitionsRequestPaginateTypeDef(TypedDict):
    EndpointName: NotRequired[str]
    SortBy: NotRequired[MonitoringJobDefinitionSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListModelBiasJobDefinitionsRequestTypeDef(TypedDict):
    EndpointName: NotRequired[str]
    SortBy: NotRequired[MonitoringJobDefinitionSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]


class ListModelCardExportJobsRequestPaginateTypeDef(TypedDict):
    ModelCardName: str
    ModelCardVersion: NotRequired[int]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    ModelCardExportJobNameContains: NotRequired[str]
    StatusEquals: NotRequired[ModelCardExportJobStatusType]
    SortBy: NotRequired[ModelCardExportJobSortByType]
    SortOrder: NotRequired[ModelCardExportJobSortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListModelCardExportJobsRequestTypeDef(TypedDict):
    ModelCardName: str
    ModelCardVersion: NotRequired[int]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    ModelCardExportJobNameContains: NotRequired[str]
    StatusEquals: NotRequired[ModelCardExportJobStatusType]
    SortBy: NotRequired[ModelCardExportJobSortByType]
    SortOrder: NotRequired[ModelCardExportJobSortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListModelCardVersionsRequestPaginateTypeDef(TypedDict):
    ModelCardName: str
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    ModelCardStatus: NotRequired[ModelCardStatusType]
    SortBy: NotRequired[Literal["Version"]]
    SortOrder: NotRequired[ModelCardSortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListModelCardVersionsRequestTypeDef(TypedDict):
    ModelCardName: str
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    ModelCardStatus: NotRequired[ModelCardStatusType]
    NextToken: NotRequired[str]
    SortBy: NotRequired[Literal["Version"]]
    SortOrder: NotRequired[ModelCardSortOrderType]


class ListModelCardsRequestPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    ModelCardStatus: NotRequired[ModelCardStatusType]
    SortBy: NotRequired[ModelCardSortByType]
    SortOrder: NotRequired[ModelCardSortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListModelCardsRequestTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    ModelCardStatus: NotRequired[ModelCardStatusType]
    NextToken: NotRequired[str]
    SortBy: NotRequired[ModelCardSortByType]
    SortOrder: NotRequired[ModelCardSortOrderType]


class ListModelExplainabilityJobDefinitionsRequestPaginateTypeDef(TypedDict):
    EndpointName: NotRequired[str]
    SortBy: NotRequired[MonitoringJobDefinitionSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListModelExplainabilityJobDefinitionsRequestTypeDef(TypedDict):
    EndpointName: NotRequired[str]
    SortBy: NotRequired[MonitoringJobDefinitionSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]


class ListModelPackageGroupsInputPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    SortBy: NotRequired[ModelPackageGroupSortByType]
    SortOrder: NotRequired[SortOrderType]
    CrossAccountFilterOption: NotRequired[CrossAccountFilterOptionType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListModelPackageGroupsInputTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    NextToken: NotRequired[str]
    SortBy: NotRequired[ModelPackageGroupSortByType]
    SortOrder: NotRequired[SortOrderType]
    CrossAccountFilterOption: NotRequired[CrossAccountFilterOptionType]


class ListModelPackagesInputPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    ModelApprovalStatus: NotRequired[ModelApprovalStatusType]
    ModelPackageGroupName: NotRequired[str]
    ModelPackageType: NotRequired[ModelPackageTypeType]
    SortBy: NotRequired[ModelPackageSortByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListModelPackagesInputTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    ModelApprovalStatus: NotRequired[ModelApprovalStatusType]
    ModelPackageGroupName: NotRequired[str]
    ModelPackageType: NotRequired[ModelPackageTypeType]
    NextToken: NotRequired[str]
    SortBy: NotRequired[ModelPackageSortByType]
    SortOrder: NotRequired[SortOrderType]


class ListModelQualityJobDefinitionsRequestPaginateTypeDef(TypedDict):
    EndpointName: NotRequired[str]
    SortBy: NotRequired[MonitoringJobDefinitionSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListModelQualityJobDefinitionsRequestTypeDef(TypedDict):
    EndpointName: NotRequired[str]
    SortBy: NotRequired[MonitoringJobDefinitionSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]


class ListModelsInputPaginateTypeDef(TypedDict):
    SortBy: NotRequired[ModelSortKeyType]
    SortOrder: NotRequired[OrderKeyType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListModelsInputTypeDef(TypedDict):
    SortBy: NotRequired[ModelSortKeyType]
    SortOrder: NotRequired[OrderKeyType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]


class ListMonitoringAlertHistoryRequestPaginateTypeDef(TypedDict):
    MonitoringScheduleName: NotRequired[str]
    MonitoringAlertName: NotRequired[str]
    SortBy: NotRequired[MonitoringAlertHistorySortKeyType]
    SortOrder: NotRequired[SortOrderType]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[MonitoringAlertStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMonitoringAlertHistoryRequestTypeDef(TypedDict):
    MonitoringScheduleName: NotRequired[str]
    MonitoringAlertName: NotRequired[str]
    SortBy: NotRequired[MonitoringAlertHistorySortKeyType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[MonitoringAlertStatusType]


class ListMonitoringExecutionsRequestPaginateTypeDef(TypedDict):
    MonitoringScheduleName: NotRequired[str]
    EndpointName: NotRequired[str]
    SortBy: NotRequired[MonitoringExecutionSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    ScheduledTimeBefore: NotRequired[TimestampTypeDef]
    ScheduledTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[ExecutionStatusType]
    MonitoringJobDefinitionName: NotRequired[str]
    MonitoringTypeEquals: NotRequired[MonitoringTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMonitoringExecutionsRequestTypeDef(TypedDict):
    MonitoringScheduleName: NotRequired[str]
    EndpointName: NotRequired[str]
    SortBy: NotRequired[MonitoringExecutionSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ScheduledTimeBefore: NotRequired[TimestampTypeDef]
    ScheduledTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[ExecutionStatusType]
    MonitoringJobDefinitionName: NotRequired[str]
    MonitoringTypeEquals: NotRequired[MonitoringTypeType]


class ListMonitoringSchedulesRequestPaginateTypeDef(TypedDict):
    EndpointName: NotRequired[str]
    SortBy: NotRequired[MonitoringScheduleSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[ScheduleStatusType]
    MonitoringJobDefinitionName: NotRequired[str]
    MonitoringTypeEquals: NotRequired[MonitoringTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMonitoringSchedulesRequestTypeDef(TypedDict):
    EndpointName: NotRequired[str]
    SortBy: NotRequired[MonitoringScheduleSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[ScheduleStatusType]
    MonitoringJobDefinitionName: NotRequired[str]
    MonitoringTypeEquals: NotRequired[MonitoringTypeType]


class ListNotebookInstanceLifecycleConfigsInputPaginateTypeDef(TypedDict):
    SortBy: NotRequired[NotebookInstanceLifecycleConfigSortKeyType]
    SortOrder: NotRequired[NotebookInstanceLifecycleConfigSortOrderType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListNotebookInstanceLifecycleConfigsInputTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SortBy: NotRequired[NotebookInstanceLifecycleConfigSortKeyType]
    SortOrder: NotRequired[NotebookInstanceLifecycleConfigSortOrderType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]


class ListNotebookInstancesInputPaginateTypeDef(TypedDict):
    SortBy: NotRequired[NotebookInstanceSortKeyType]
    SortOrder: NotRequired[NotebookInstanceSortOrderType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[NotebookInstanceStatusType]
    NotebookInstanceLifecycleConfigNameContains: NotRequired[str]
    DefaultCodeRepositoryContains: NotRequired[str]
    AdditionalCodeRepositoryEquals: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListNotebookInstancesInputTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    SortBy: NotRequired[NotebookInstanceSortKeyType]
    SortOrder: NotRequired[NotebookInstanceSortOrderType]
    NameContains: NotRequired[str]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    StatusEquals: NotRequired[NotebookInstanceStatusType]
    NotebookInstanceLifecycleConfigNameContains: NotRequired[str]
    DefaultCodeRepositoryContains: NotRequired[str]
    AdditionalCodeRepositoryEquals: NotRequired[str]


class ListOptimizationJobsRequestPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    OptimizationContains: NotRequired[str]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[OptimizationJobStatusType]
    SortBy: NotRequired[ListOptimizationJobsSortByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListOptimizationJobsRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    OptimizationContains: NotRequired[str]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[OptimizationJobStatusType]
    SortBy: NotRequired[ListOptimizationJobsSortByType]
    SortOrder: NotRequired[SortOrderType]


class ListPipelineExecutionsRequestPaginateTypeDef(TypedDict):
    PipelineName: str
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortPipelineExecutionsByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPipelineExecutionsRequestTypeDef(TypedDict):
    PipelineName: str
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortPipelineExecutionsByType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListPipelineVersionsRequestPaginateTypeDef(TypedDict):
    PipelineName: str
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPipelineVersionsRequestTypeDef(TypedDict):
    PipelineName: str
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListPipelinesRequestPaginateTypeDef(TypedDict):
    PipelineNamePrefix: NotRequired[str]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortPipelinesByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPipelinesRequestTypeDef(TypedDict):
    PipelineNamePrefix: NotRequired[str]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortPipelinesByType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListProcessingJobsRequestPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[ProcessingJobStatusType]
    SortBy: NotRequired[SortByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProcessingJobsRequestTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[ProcessingJobStatusType]
    SortBy: NotRequired[SortByType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListProjectsInputTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NameContains: NotRequired[str]
    NextToken: NotRequired[str]
    SortBy: NotRequired[ProjectSortByType]
    SortOrder: NotRequired[ProjectSortOrderType]


class ListResourceCatalogsRequestPaginateTypeDef(TypedDict):
    NameContains: NotRequired[str]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    SortOrder: NotRequired[ResourceCatalogSortOrderType]
    SortBy: NotRequired[Literal["CreationTime"]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResourceCatalogsRequestTypeDef(TypedDict):
    NameContains: NotRequired[str]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    SortOrder: NotRequired[ResourceCatalogSortOrderType]
    SortBy: NotRequired[Literal["CreationTime"]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListStudioLifecycleConfigsRequestPaginateTypeDef(TypedDict):
    NameContains: NotRequired[str]
    AppTypeEquals: NotRequired[StudioLifecycleConfigAppTypeType]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    ModifiedTimeBefore: NotRequired[TimestampTypeDef]
    ModifiedTimeAfter: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[StudioLifecycleConfigSortKeyType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListStudioLifecycleConfigsRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    NameContains: NotRequired[str]
    AppTypeEquals: NotRequired[StudioLifecycleConfigAppTypeType]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    ModifiedTimeBefore: NotRequired[TimestampTypeDef]
    ModifiedTimeAfter: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[StudioLifecycleConfigSortKeyType]
    SortOrder: NotRequired[SortOrderType]


class ListTrainingJobsRequestPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[TrainingJobStatusType]
    SortBy: NotRequired[SortByType]
    SortOrder: NotRequired[SortOrderType]
    WarmPoolStatusEquals: NotRequired[WarmPoolResourceStatusType]
    TrainingPlanArnEquals: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTrainingJobsRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[TrainingJobStatusType]
    SortBy: NotRequired[SortByType]
    SortOrder: NotRequired[SortOrderType]
    WarmPoolStatusEquals: NotRequired[WarmPoolResourceStatusType]
    TrainingPlanArnEquals: NotRequired[str]


class ListTransformJobsRequestPaginateTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[TransformJobStatusType]
    SortBy: NotRequired[SortByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTransformJobsRequestTypeDef(TypedDict):
    CreationTimeAfter: NotRequired[TimestampTypeDef]
    CreationTimeBefore: NotRequired[TimestampTypeDef]
    LastModifiedTimeAfter: NotRequired[TimestampTypeDef]
    LastModifiedTimeBefore: NotRequired[TimestampTypeDef]
    NameContains: NotRequired[str]
    StatusEquals: NotRequired[TransformJobStatusType]
    SortBy: NotRequired[SortByType]
    SortOrder: NotRequired[SortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListTrialComponentsRequestPaginateTypeDef(TypedDict):
    ExperimentName: NotRequired[str]
    TrialName: NotRequired[str]
    SourceArn: NotRequired[str]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortTrialComponentsByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTrialComponentsRequestTypeDef(TypedDict):
    ExperimentName: NotRequired[str]
    TrialName: NotRequired[str]
    SourceArn: NotRequired[str]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortTrialComponentsByType]
    SortOrder: NotRequired[SortOrderType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListTrialsRequestPaginateTypeDef(TypedDict):
    ExperimentName: NotRequired[str]
    TrialComponentName: NotRequired[str]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortTrialsByType]
    SortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTrialsRequestTypeDef(TypedDict):
    ExperimentName: NotRequired[str]
    TrialComponentName: NotRequired[str]
    CreatedAfter: NotRequired[TimestampTypeDef]
    CreatedBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[SortTrialsByType]
    SortOrder: NotRequired[SortOrderType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class QueryFiltersTypeDef(TypedDict):
    Types: NotRequired[Sequence[str]]
    LineageTypes: NotRequired[Sequence[LineageTypeType]]
    CreatedBefore: NotRequired[TimestampTypeDef]
    CreatedAfter: NotRequired[TimestampTypeDef]
    ModifiedBefore: NotRequired[TimestampTypeDef]
    ModifiedAfter: NotRequired[TimestampTypeDef]
    Properties: NotRequired[Mapping[str, str]]


class SearchTrainingPlanOfferingsRequestTypeDef(TypedDict):
    InstanceType: NotRequired[ReservedCapacityInstanceTypeType]
    InstanceCount: NotRequired[int]
    UltraServerType: NotRequired[str]
    UltraServerCount: NotRequired[int]
    StartTimeAfter: NotRequired[TimestampTypeDef]
    EndTimeBefore: NotRequired[TimestampTypeDef]
    DurationHours: NotRequired[int]
    TargetResources: NotRequired[Sequence[SageMakerResourceNameType]]


class CreateTrialComponentRequestTypeDef(TypedDict):
    TrialComponentName: str
    DisplayName: NotRequired[str]
    Status: NotRequired[TrialComponentStatusTypeDef]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    Parameters: NotRequired[Mapping[str, TrialComponentParameterValueTypeDef]]
    InputArtifacts: NotRequired[Mapping[str, TrialComponentArtifactTypeDef]]
    OutputArtifacts: NotRequired[Mapping[str, TrialComponentArtifactTypeDef]]
    MetadataProperties: NotRequired[MetadataPropertiesTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class UpdateTrialComponentRequestTypeDef(TypedDict):
    TrialComponentName: str
    DisplayName: NotRequired[str]
    Status: NotRequired[TrialComponentStatusTypeDef]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    Parameters: NotRequired[Mapping[str, TrialComponentParameterValueTypeDef]]
    ParametersToRemove: NotRequired[Sequence[str]]
    InputArtifacts: NotRequired[Mapping[str, TrialComponentArtifactTypeDef]]
    InputArtifactsToRemove: NotRequired[Sequence[str]]
    OutputArtifacts: NotRequired[Mapping[str, TrialComponentArtifactTypeDef]]
    OutputArtifactsToRemove: NotRequired[Sequence[str]]


class CustomFileSystemConfigTypeDef(TypedDict):
    EFSFileSystemConfig: NotRequired[EFSFileSystemConfigTypeDef]
    FSxLustreFileSystemConfig: NotRequired[FSxLustreFileSystemConfigTypeDef]
    S3FileSystemConfig: NotRequired[S3FileSystemConfigTypeDef]


class CustomFileSystemTypeDef(TypedDict):
    EFSFileSystem: NotRequired[EFSFileSystemTypeDef]
    FSxLustreFileSystem: NotRequired[FSxLustreFileSystemTypeDef]
    S3FileSystem: NotRequired[S3FileSystemTypeDef]


DataQualityAppSpecificationUnionTypeDef = Union[
    DataQualityAppSpecificationTypeDef, DataQualityAppSpecificationOutputTypeDef
]


class ModelBiasBaselineConfigTypeDef(TypedDict):
    BaseliningJobName: NotRequired[str]
    ConstraintsResource: NotRequired[MonitoringConstraintsResourceTypeDef]


class ModelExplainabilityBaselineConfigTypeDef(TypedDict):
    BaseliningJobName: NotRequired[str]
    ConstraintsResource: NotRequired[MonitoringConstraintsResourceTypeDef]


class ModelQualityBaselineConfigTypeDef(TypedDict):
    BaseliningJobName: NotRequired[str]
    ConstraintsResource: NotRequired[MonitoringConstraintsResourceTypeDef]


class DataQualityBaselineConfigTypeDef(TypedDict):
    BaseliningJobName: NotRequired[str]
    ConstraintsResource: NotRequired[MonitoringConstraintsResourceTypeDef]
    StatisticsResource: NotRequired[MonitoringStatisticsResourceTypeDef]


class MonitoringBaselineConfigTypeDef(TypedDict):
    BaseliningJobName: NotRequired[str]
    ConstraintsResource: NotRequired[MonitoringConstraintsResourceTypeDef]
    StatisticsResource: NotRequired[MonitoringStatisticsResourceTypeDef]


class DatasetDefinitionTypeDef(TypedDict):
    AthenaDatasetDefinition: NotRequired[AthenaDatasetDefinitionTypeDef]
    RedshiftDatasetDefinition: NotRequired[RedshiftDatasetDefinitionTypeDef]
    LocalPath: NotRequired[str]
    DataDistributionType: NotRequired[DataDistributionTypeType]
    InputMode: NotRequired[InputModeType]


DebugRuleConfigurationUnionTypeDef = Union[
    DebugRuleConfigurationTypeDef, DebugRuleConfigurationOutputTypeDef
]


class DefaultSpaceStorageSettingsTypeDef(TypedDict):
    DefaultEbsStorageSettings: NotRequired[DefaultEbsStorageSettingsTypeDef]


class DeleteDomainRequestTypeDef(TypedDict):
    DomainId: str
    RetentionPolicy: NotRequired[RetentionPolicyTypeDef]


class InferenceComponentContainerSpecificationSummaryTypeDef(TypedDict):
    DeployedImage: NotRequired[DeployedImageTypeDef]
    ArtifactUrl: NotRequired[str]
    Environment: NotRequired[dict[str, str]]


class DeploymentRecommendationTypeDef(TypedDict):
    RecommendationStatus: RecommendationStatusType
    RealTimeInferenceRecommendations: NotRequired[list[RealTimeInferenceRecommendationTypeDef]]


class DeploymentStageStatusSummaryTypeDef(TypedDict):
    StageName: str
    DeviceSelectionConfig: DeviceSelectionConfigOutputTypeDef
    DeploymentConfig: EdgeDeploymentConfigTypeDef
    DeploymentStatus: EdgeDeploymentStatusTypeDef


class DescribeDeviceResponseTypeDef(TypedDict):
    DeviceArn: str
    DeviceName: str
    Description: str
    DeviceFleetName: str
    IotThingName: str
    RegistrationTime: datetime
    LatestHeartbeat: datetime
    Models: list[EdgeModelTypeDef]
    MaxModels: int
    AgentVersion: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeEdgePackagingJobResponseTypeDef(TypedDict):
    EdgePackagingJobArn: str
    EdgePackagingJobName: str
    CompilationJobName: str
    ModelName: str
    ModelVersion: str
    RoleArn: str
    OutputConfig: EdgeOutputConfigTypeDef
    ResourceKey: str
    EdgePackagingJobStatus: EdgePackagingJobStatusType
    EdgePackagingJobStatusMessage: str
    CreationTime: datetime
    LastModifiedTime: datetime
    ModelArtifact: str
    ModelSignature: str
    PresetDeploymentOutput: EdgePresetDeploymentOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeEndpointInputWaitExtraTypeDef(TypedDict):
    EndpointName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeEndpointInputWaitTypeDef(TypedDict):
    EndpointName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeImageRequestWaitExtraExtraTypeDef(TypedDict):
    ImageName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeImageRequestWaitExtraTypeDef(TypedDict):
    ImageName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeImageRequestWaitTypeDef(TypedDict):
    ImageName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeImageVersionRequestWaitExtraTypeDef(TypedDict):
    ImageName: str
    Version: NotRequired[int]
    Alias: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeImageVersionRequestWaitTypeDef(TypedDict):
    ImageName: str
    Version: NotRequired[int]
    Alias: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeNotebookInstanceInputWaitExtraExtraTypeDef(TypedDict):
    NotebookInstanceName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeNotebookInstanceInputWaitExtraTypeDef(TypedDict):
    NotebookInstanceName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeNotebookInstanceInputWaitTypeDef(TypedDict):
    NotebookInstanceName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeProcessingJobRequestWaitTypeDef(TypedDict):
    ProcessingJobName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeTrainingJobRequestWaitTypeDef(TypedDict):
    TrainingJobName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeTransformJobRequestWaitTypeDef(TypedDict):
    TransformJobName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class ExperimentSummaryTypeDef(TypedDict):
    ExperimentArn: NotRequired[str]
    ExperimentName: NotRequired[str]
    DisplayName: NotRequired[str]
    ExperimentSource: NotRequired[ExperimentSourceTypeDef]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]


class FeatureGroupSummaryTypeDef(TypedDict):
    FeatureGroupName: str
    FeatureGroupArn: str
    CreationTime: datetime
    FeatureGroupStatus: NotRequired[FeatureGroupStatusType]
    OfflineStoreStatus: NotRequired[OfflineStoreStatusTypeDef]


class DescribeFeatureMetadataResponseTypeDef(TypedDict):
    FeatureGroupArn: str
    FeatureGroupName: str
    FeatureName: str
    FeatureType: FeatureTypeType
    CreationTime: datetime
    LastModifiedTime: datetime
    Description: str
    Parameters: list[FeatureParameterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class FeatureMetadataTypeDef(TypedDict):
    FeatureGroupArn: NotRequired[str]
    FeatureGroupName: NotRequired[str]
    FeatureName: NotRequired[str]
    FeatureType: NotRequired[FeatureTypeType]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    Description: NotRequired[str]
    Parameters: NotRequired[list[FeatureParameterTypeDef]]


class UpdateFeatureMetadataRequestTypeDef(TypedDict):
    FeatureGroupName: str
    FeatureName: str
    Description: NotRequired[str]
    ParameterAdditions: NotRequired[Sequence[FeatureParameterTypeDef]]
    ParameterRemovals: NotRequired[Sequence[str]]


class DescribeHubContentResponseTypeDef(TypedDict):
    HubContentName: str
    HubContentArn: str
    HubContentVersion: str
    HubContentType: HubContentTypeType
    DocumentSchemaVersion: str
    HubName: str
    HubArn: str
    HubContentDisplayName: str
    HubContentDescription: str
    HubContentMarkdown: str
    HubContentDocument: str
    SageMakerPublicHubContentArn: str
    ReferenceMinVersion: str
    SupportStatus: HubContentSupportStatusType
    HubContentSearchKeywords: list[str]
    HubContentDependencies: list[HubContentDependencyTypeDef]
    HubContentStatus: HubContentStatusType
    FailureReason: str
    CreationTime: datetime
    LastModifiedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeHumanTaskUiResponseTypeDef(TypedDict):
    HumanTaskUiArn: str
    HumanTaskUiName: str
    HumanTaskUiStatus: HumanTaskUiStatusType
    CreationTime: datetime
    UiTemplate: UiTemplateInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


InferenceExperimentSummaryTypeDef = TypedDict(
    "InferenceExperimentSummaryTypeDef",
    {
        "Name": str,
        "Type": Literal["ShadowMode"],
        "Status": InferenceExperimentStatusType,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "Schedule": NotRequired[InferenceExperimentScheduleOutputTypeDef],
        "StatusReason": NotRequired[str],
        "Description": NotRequired[str],
        "CompletionTime": NotRequired[datetime],
        "RoleArn": NotRequired[str],
    },
)


class DescribeModelCardExportJobResponseTypeDef(TypedDict):
    ModelCardExportJobName: str
    ModelCardExportJobArn: str
    Status: ModelCardExportJobStatusType
    ModelCardName: str
    ModelCardVersion: int
    OutputConfig: ModelCardExportOutputConfigTypeDef
    CreatedAt: datetime
    LastModifiedAt: datetime
    FailureReason: str
    ExportArtifacts: ModelCardExportArtifactsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListMonitoringExecutionsResponseTypeDef(TypedDict):
    MonitoringExecutionSummaries: list[MonitoringExecutionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeReservedCapacityResponseTypeDef(TypedDict):
    ReservedCapacityArn: str
    ReservedCapacityType: ReservedCapacityTypeType
    Status: ReservedCapacityStatusType
    AvailabilityZone: str
    DurationHours: int
    DurationMinutes: int
    StartTime: datetime
    EndTime: datetime
    InstanceType: ReservedCapacityInstanceTypeType
    TotalInstanceCount: int
    AvailableInstanceCount: int
    InUseInstanceCount: int
    UltraServerSummary: UltraServerSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeSubscribedWorkteamResponseTypeDef(TypedDict):
    SubscribedWorkteam: SubscribedWorkteamTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListSubscribedWorkteamsResponseTypeDef(TypedDict):
    SubscribedWorkteams: list[SubscribedWorkteamTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class TrainingJobSummaryTypeDef(TypedDict):
    TrainingJobName: str
    TrainingJobArn: str
    CreationTime: datetime
    TrainingJobStatus: TrainingJobStatusType
    TrainingEndTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    SecondaryStatus: NotRequired[SecondaryStatusType]
    WarmPoolStatus: NotRequired[WarmPoolStatusTypeDef]
    TrainingPlanArn: NotRequired[str]


class DescribeTrainingPlanResponseTypeDef(TypedDict):
    TrainingPlanArn: str
    TrainingPlanName: str
    Status: TrainingPlanStatusType
    StatusMessage: str
    DurationHours: int
    DurationMinutes: int
    StartTime: datetime
    EndTime: datetime
    UpfrontFee: str
    CurrencyCode: str
    TotalInstanceCount: int
    AvailableInstanceCount: int
    InUseInstanceCount: int
    UnhealthyInstanceCount: int
    AvailableSpareInstanceCount: int
    TotalUltraServerCount: int
    TargetResources: list[SageMakerResourceNameType]
    ReservedCapacitySummaries: list[ReservedCapacitySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TrainingPlanSummaryTypeDef(TypedDict):
    TrainingPlanArn: str
    TrainingPlanName: str
    Status: TrainingPlanStatusType
    StatusMessage: NotRequired[str]
    DurationHours: NotRequired[int]
    DurationMinutes: NotRequired[int]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    UpfrontFee: NotRequired[str]
    CurrencyCode: NotRequired[str]
    TotalInstanceCount: NotRequired[int]
    AvailableInstanceCount: NotRequired[int]
    InUseInstanceCount: NotRequired[int]
    TotalUltraServerCount: NotRequired[int]
    TargetResources: NotRequired[list[SageMakerResourceNameType]]
    ReservedCapacitySummaries: NotRequired[list[ReservedCapacitySummaryTypeDef]]


class TrialSummaryTypeDef(TypedDict):
    TrialArn: NotRequired[str]
    TrialName: NotRequired[str]
    DisplayName: NotRequired[str]
    TrialSource: NotRequired[TrialSourceTypeDef]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]


class DesiredWeightAndCapacityTypeDef(TypedDict):
    VariantName: str
    DesiredWeight: NotRequired[float]
    DesiredInstanceCount: NotRequired[int]
    ServerlessUpdateConfig: NotRequired[ProductionVariantServerlessUpdateConfigTypeDef]


class ListStageDevicesResponseTypeDef(TypedDict):
    DeviceDeploymentSummaries: list[DeviceDeploymentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListDeviceFleetsResponseTypeDef(TypedDict):
    DeviceFleetSummaries: list[DeviceFleetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


DeviceSelectionConfigUnionTypeDef = Union[
    DeviceSelectionConfigTypeDef, DeviceSelectionConfigOutputTypeDef
]


class DeviceSummaryTypeDef(TypedDict):
    DeviceName: str
    DeviceArn: str
    Description: NotRequired[str]
    DeviceFleetName: NotRequired[str]
    IotThingName: NotRequired[str]
    RegistrationTime: NotRequired[datetime]
    LatestHeartbeat: NotRequired[datetime]
    Models: NotRequired[list[EdgeModelSummaryTypeDef]]
    AgentVersion: NotRequired[str]


class RegisterDevicesRequestTypeDef(TypedDict):
    DeviceFleetName: str
    Devices: Sequence[DeviceTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class UpdateDevicesRequestTypeDef(TypedDict):
    DeviceFleetName: str
    Devices: Sequence[DeviceTypeDef]


DockerSettingsUnionTypeDef = Union[DockerSettingsTypeDef, DockerSettingsOutputTypeDef]


class ListDomainsResponseTypeDef(TypedDict):
    Domains: list[DomainDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DriftCheckBiasTypeDef(TypedDict):
    ConfigFile: NotRequired[FileSourceTypeDef]
    PreTrainingConstraints: NotRequired[MetricsSourceTypeDef]
    PostTrainingConstraints: NotRequired[MetricsSourceTypeDef]


class DriftCheckExplainabilityTypeDef(TypedDict):
    Constraints: NotRequired[MetricsSourceTypeDef]
    ConfigFile: NotRequired[FileSourceTypeDef]


class SpaceStorageSettingsTypeDef(TypedDict):
    EbsStorageSettings: NotRequired[EbsStorageSettingsTypeDef]


class ProductionVariantCapacityReservationSummaryTypeDef(TypedDict):
    MlReservationArn: NotRequired[str]
    CapacityReservationPreference: NotRequired[Literal["capacity-reservations-only"]]
    TotalInstanceCount: NotRequired[int]
    AvailableInstanceCount: NotRequired[int]
    UsedByCurrentEndpoint: NotRequired[int]
    Ec2CapacityReservations: NotRequired[list[Ec2CapacityReservationTypeDef]]


class ListEdgeDeploymentPlansResponseTypeDef(TypedDict):
    EdgeDeploymentPlanSummaries: list[EdgeDeploymentPlanSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetDeviceFleetReportResponseTypeDef(TypedDict):
    DeviceFleetArn: str
    DeviceFleetName: str
    OutputConfig: EdgeOutputConfigTypeDef
    Description: str
    ReportGenerated: datetime
    DeviceStats: DeviceStatsTypeDef
    AgentVersions: list[AgentVersionTypeDef]
    ModelStats: list[EdgeModelStatTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListEdgePackagingJobsResponseTypeDef(TypedDict):
    EdgePackagingJobSummaries: list[EdgePackagingJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListEndpointConfigsOutputTypeDef(TypedDict):
    EndpointConfigs: list[EndpointConfigSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class EndpointOutputConfigurationTypeDef(TypedDict):
    EndpointName: str
    VariantName: str
    InstanceType: NotRequired[ProductionVariantInstanceTypeType]
    InitialInstanceCount: NotRequired[int]
    ServerlessConfig: NotRequired[ProductionVariantServerlessConfigTypeDef]


class EndpointPerformanceTypeDef(TypedDict):
    Metrics: InferenceMetricsTypeDef
    EndpointInfo: EndpointInfoTypeDef


class ListEndpointsOutputTypeDef(TypedDict):
    Endpoints: list[EndpointSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class EnvironmentConfigDetailsTypeDef(TypedDict):
    FSxLustreConfig: NotRequired[FSxLustreConfigTypeDef]
    S3OutputPath: NotRequired[str]


class EnvironmentConfigTypeDef(TypedDict):
    FSxLustreConfig: NotRequired[FSxLustreConfigTypeDef]


class ModelConfigurationTypeDef(TypedDict):
    InferenceSpecificationName: NotRequired[str]
    EnvironmentParameters: NotRequired[list[EnvironmentParameterTypeDef]]
    CompilationJobName: NotRequired[str]


class NestedFiltersTypeDef(TypedDict):
    NestedPropertyName: str
    Filters: Sequence[FilterTypeDef]


class HyperParameterTrainingJobSummaryTypeDef(TypedDict):
    TrainingJobName: str
    TrainingJobArn: str
    CreationTime: datetime
    TrainingJobStatus: TrainingJobStatusType
    TunedHyperParameters: dict[str, str]
    TrainingJobDefinitionName: NotRequired[str]
    TuningJobName: NotRequired[str]
    TrainingStartTime: NotRequired[datetime]
    TrainingEndTime: NotRequired[datetime]
    FailureReason: NotRequired[str]
    FinalHyperParameterTuningJobObjectiveMetric: NotRequired[
        FinalHyperParameterTuningJobObjectiveMetricTypeDef
    ]
    ObjectiveStatus: NotRequired[ObjectiveStatusType]


class ListFlowDefinitionsResponseTypeDef(TypedDict):
    FlowDefinitionSummaries: list[FlowDefinitionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetScalingConfigurationRecommendationRequestTypeDef(TypedDict):
    InferenceRecommendationsJobName: str
    RecommendationId: NotRequired[str]
    EndpointName: NotRequired[str]
    TargetCpuUtilizationPerCore: NotRequired[int]
    ScalingPolicyObjective: NotRequired[ScalingPolicyObjectiveTypeDef]


class GetSearchSuggestionsResponseTypeDef(TypedDict):
    PropertyNameSuggestions: list[PropertyNameSuggestionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateCodeRepositoryInputTypeDef(TypedDict):
    CodeRepositoryName: str
    GitConfig: NotRequired[GitConfigForUpdateTypeDef]


class StudioWebPortalSettingsOutputTypeDef(TypedDict):
    HiddenMlTools: NotRequired[list[MlToolsType]]
    HiddenAppTypes: NotRequired[list[AppTypeType]]
    HiddenInstanceTypes: NotRequired[list[AppInstanceTypeType]]
    HiddenSageMakerImageVersionAliases: NotRequired[list[HiddenSageMakerImageOutputTypeDef]]


class StudioWebPortalSettingsTypeDef(TypedDict):
    HiddenMlTools: NotRequired[Sequence[MlToolsType]]
    HiddenAppTypes: NotRequired[Sequence[AppTypeType]]
    HiddenInstanceTypes: NotRequired[Sequence[AppInstanceTypeType]]
    HiddenSageMakerImageVersionAliases: NotRequired[Sequence[HiddenSageMakerImageTypeDef]]


class ListHubContentVersionsResponseTypeDef(TypedDict):
    HubContentSummaries: list[HubContentInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListHubContentsResponseTypeDef(TypedDict):
    HubContentSummaries: list[HubContentInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListHubsResponseTypeDef(TypedDict):
    HubSummaries: list[HubInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class HumanLoopActivationConfigTypeDef(TypedDict):
    HumanLoopActivationConditionsConfig: HumanLoopActivationConditionsConfigTypeDef


class ListHumanTaskUisResponseTypeDef(TypedDict):
    HumanTaskUiSummaries: list[HumanTaskUiSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class HyperParameterTuningResourceConfigOutputTypeDef(TypedDict):
    InstanceType: NotRequired[TrainingInstanceTypeType]
    InstanceCount: NotRequired[int]
    VolumeSizeInGB: NotRequired[int]
    VolumeKmsKeyId: NotRequired[str]
    AllocationStrategy: NotRequired[Literal["Prioritized"]]
    InstanceConfigs: NotRequired[list[HyperParameterTuningInstanceConfigTypeDef]]


class HyperParameterTuningResourceConfigTypeDef(TypedDict):
    InstanceType: NotRequired[TrainingInstanceTypeType]
    InstanceCount: NotRequired[int]
    VolumeSizeInGB: NotRequired[int]
    VolumeKmsKeyId: NotRequired[str]
    AllocationStrategy: NotRequired[Literal["Prioritized"]]
    InstanceConfigs: NotRequired[Sequence[HyperParameterTuningInstanceConfigTypeDef]]


class HyperParameterTuningJobSummaryTypeDef(TypedDict):
    HyperParameterTuningJobName: str
    HyperParameterTuningJobArn: str
    HyperParameterTuningJobStatus: HyperParameterTuningJobStatusType
    Strategy: HyperParameterTuningJobStrategyTypeType
    CreationTime: datetime
    TrainingJobStatusCounters: TrainingJobStatusCountersTypeDef
    ObjectiveStatusCounters: ObjectiveStatusCountersTypeDef
    HyperParameterTuningEndTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    ResourceLimits: NotRequired[ResourceLimitsTypeDef]


class HyperParameterTuningJobStrategyConfigTypeDef(TypedDict):
    HyperbandStrategyConfig: NotRequired[HyperbandStrategyConfigTypeDef]


class HyperParameterTuningJobWarmStartConfigOutputTypeDef(TypedDict):
    ParentHyperParameterTuningJobs: list[ParentHyperParameterTuningJobTypeDef]
    WarmStartType: HyperParameterTuningJobWarmStartTypeType


class HyperParameterTuningJobWarmStartConfigTypeDef(TypedDict):
    ParentHyperParameterTuningJobs: Sequence[ParentHyperParameterTuningJobTypeDef]
    WarmStartType: HyperParameterTuningJobWarmStartTypeType


class UserContextTypeDef(TypedDict):
    UserProfileArn: NotRequired[str]
    UserProfileName: NotRequired[str]
    DomainId: NotRequired[str]
    IamIdentity: NotRequired[IamIdentityTypeDef]


class S3PresignTypeDef(TypedDict):
    IamPolicyConstraints: NotRequired[IamPolicyConstraintsTypeDef]


class ImageConfigTypeDef(TypedDict):
    RepositoryAccessMode: RepositoryAccessModeType
    RepositoryAuthConfig: NotRequired[RepositoryAuthConfigTypeDef]


class ListImagesResponseTypeDef(TypedDict):
    Images: list[ImageTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListImageVersionsResponseTypeDef(TypedDict):
    ImageVersions: list[ImageVersionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class InferenceComponentRollingUpdatePolicyTypeDef(TypedDict):
    MaximumBatchSize: InferenceComponentCapacitySizeTypeDef
    WaitIntervalInSeconds: int
    MaximumExecutionTimeoutInSeconds: NotRequired[int]
    RollbackMaximumBatchSize: NotRequired[InferenceComponentCapacitySizeTypeDef]


InferenceComponentSpecificationTypeDef = TypedDict(
    "InferenceComponentSpecificationTypeDef",
    {
        "ModelName": NotRequired[str],
        "Container": NotRequired[InferenceComponentContainerSpecificationTypeDef],
        "StartupParameters": NotRequired[InferenceComponentStartupParametersTypeDef],
        "ComputeResourceRequirements": NotRequired[
            InferenceComponentComputeResourceRequirementsTypeDef
        ],
        "BaseInferenceComponentName": NotRequired[str],
        "DataCacheConfig": NotRequired[InferenceComponentDataCacheConfigTypeDef],
    },
)


class ListInferenceComponentsOutputTypeDef(TypedDict):
    InferenceComponents: list[InferenceComponentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListInferenceRecommendationsJobsResponseTypeDef(TypedDict):
    InferenceRecommendationsJobs: list[InferenceRecommendationsJobTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class InstancePlacementConfigOutputTypeDef(TypedDict):
    EnableMultipleJobs: NotRequired[bool]
    PlacementSpecifications: NotRequired[list[PlacementSpecificationTypeDef]]


class InstancePlacementConfigTypeDef(TypedDict):
    EnableMultipleJobs: NotRequired[bool]
    PlacementSpecifications: NotRequired[Sequence[PlacementSpecificationTypeDef]]


class ParameterRangeOutputTypeDef(TypedDict):
    IntegerParameterRangeSpecification: NotRequired[IntegerParameterRangeSpecificationTypeDef]
    ContinuousParameterRangeSpecification: NotRequired[ContinuousParameterRangeSpecificationTypeDef]
    CategoricalParameterRangeSpecification: NotRequired[
        CategoricalParameterRangeSpecificationOutputTypeDef
    ]


class ParameterRangeTypeDef(TypedDict):
    IntegerParameterRangeSpecification: NotRequired[IntegerParameterRangeSpecificationTypeDef]
    ContinuousParameterRangeSpecification: NotRequired[ContinuousParameterRangeSpecificationTypeDef]
    CategoricalParameterRangeSpecification: NotRequired[
        CategoricalParameterRangeSpecificationTypeDef
    ]


class ParameterRangesOutputTypeDef(TypedDict):
    IntegerParameterRanges: NotRequired[list[IntegerParameterRangeTypeDef]]
    ContinuousParameterRanges: NotRequired[list[ContinuousParameterRangeTypeDef]]
    CategoricalParameterRanges: NotRequired[list[CategoricalParameterRangeOutputTypeDef]]
    AutoParameters: NotRequired[list[AutoParameterTypeDef]]


class KernelGatewayImageConfigOutputTypeDef(TypedDict):
    KernelSpecs: list[KernelSpecTypeDef]
    FileSystemConfig: NotRequired[FileSystemConfigTypeDef]


class KernelGatewayImageConfigTypeDef(TypedDict):
    KernelSpecs: Sequence[KernelSpecTypeDef]
    FileSystemConfig: NotRequired[FileSystemConfigTypeDef]


class LabelingJobForWorkteamSummaryTypeDef(TypedDict):
    JobReferenceCode: str
    WorkRequesterAccountId: str
    CreationTime: datetime
    LabelingJobName: NotRequired[str]
    LabelCounters: NotRequired[LabelCountersForWorkteamTypeDef]
    NumberOfHumanWorkersPerDataObject: NotRequired[int]


class LabelingJobDataSourceTypeDef(TypedDict):
    S3DataSource: NotRequired[LabelingJobS3DataSourceTypeDef]
    SnsDataSource: NotRequired[LabelingJobSnsDataSourceTypeDef]


class ListLineageGroupsResponseTypeDef(TypedDict):
    LineageGroupSummaries: list[LineageGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListDataQualityJobDefinitionsResponseTypeDef(TypedDict):
    JobDefinitionSummaries: list[MonitoringJobDefinitionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListModelBiasJobDefinitionsResponseTypeDef(TypedDict):
    JobDefinitionSummaries: list[MonitoringJobDefinitionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListModelExplainabilityJobDefinitionsResponseTypeDef(TypedDict):
    JobDefinitionSummaries: list[MonitoringJobDefinitionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListModelQualityJobDefinitionsResponseTypeDef(TypedDict):
    JobDefinitionSummaries: list[MonitoringJobDefinitionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListMlflowAppsResponseTypeDef(TypedDict):
    Summaries: list[MlflowAppSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListMlflowTrackingServersResponseTypeDef(TypedDict):
    TrackingServerSummaries: list[TrackingServerSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListModelCardExportJobsResponseTypeDef(TypedDict):
    ModelCardExportJobSummaries: list[ModelCardExportJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListModelCardVersionsResponseTypeDef(TypedDict):
    ModelCardVersionSummaryList: list[ModelCardVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListModelCardsResponseTypeDef(TypedDict):
    ModelCardSummaries: list[ModelCardSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListModelMetadataResponseTypeDef(TypedDict):
    ModelMetadataSummaries: list[ModelMetadataSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListModelPackageGroupsOutputTypeDef(TypedDict):
    ModelPackageGroupSummaryList: list[ModelPackageGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListModelsOutputTypeDef(TypedDict):
    Models: list[ModelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListMonitoringAlertHistoryResponseTypeDef(TypedDict):
    MonitoringAlertHistory: list[MonitoringAlertHistorySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListMonitoringSchedulesResponseTypeDef(TypedDict):
    MonitoringScheduleSummaries: list[MonitoringScheduleSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListNotebookInstanceLifecycleConfigsOutputTypeDef(TypedDict):
    NotebookInstanceLifecycleConfigs: list[NotebookInstanceLifecycleConfigSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListNotebookInstancesOutputTypeDef(TypedDict):
    NotebookInstances: list[NotebookInstanceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListOptimizationJobsResponseTypeDef(TypedDict):
    OptimizationJobSummaries: list[OptimizationJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListPartnerAppsResponseTypeDef(TypedDict):
    Summaries: list[PartnerAppSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListPipelineExecutionsResponseTypeDef(TypedDict):
    PipelineExecutionSummaries: list[PipelineExecutionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListPipelineParametersForExecutionResponseTypeDef(TypedDict):
    PipelineParameters: list[ParameterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListPipelineVersionsResponseTypeDef(TypedDict):
    PipelineVersionSummaries: list[PipelineVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListPipelinesResponseTypeDef(TypedDict):
    PipelineSummaries: list[PipelineSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListProcessingJobsResponseTypeDef(TypedDict):
    ProcessingJobSummaries: list[ProcessingJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListProjectsOutputTypeDef(TypedDict):
    ProjectSummaryList: list[ProjectSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListResourceCatalogsResponseTypeDef(TypedDict):
    ResourceCatalogs: list[ResourceCatalogTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListStudioLifecycleConfigsResponseTypeDef(TypedDict):
    StudioLifecycleConfigs: list[StudioLifecycleConfigDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTrainingPlansRequestPaginateTypeDef(TypedDict):
    StartTimeAfter: NotRequired[TimestampTypeDef]
    StartTimeBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[TrainingPlanSortByType]
    SortOrder: NotRequired[TrainingPlanSortOrderType]
    Filters: NotRequired[Sequence[TrainingPlanFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTrainingPlansRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    StartTimeAfter: NotRequired[TimestampTypeDef]
    StartTimeBefore: NotRequired[TimestampTypeDef]
    SortBy: NotRequired[TrainingPlanSortByType]
    SortOrder: NotRequired[TrainingPlanSortOrderType]
    Filters: NotRequired[Sequence[TrainingPlanFilterTypeDef]]


class ListTransformJobsResponseTypeDef(TypedDict):
    TransformJobSummaries: list[TransformJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListUltraServersByReservedCapacityResponseTypeDef(TypedDict):
    UltraServers: list[UltraServerTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListUserProfilesResponseTypeDef(TypedDict):
    UserProfiles: list[UserProfileDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class MemberDefinitionOutputTypeDef(TypedDict):
    CognitoMemberDefinition: NotRequired[CognitoMemberDefinitionTypeDef]
    OidcMemberDefinition: NotRequired[OidcMemberDefinitionOutputTypeDef]


class MetricSpecificationTypeDef(TypedDict):
    Predefined: NotRequired[PredefinedMetricSpecificationTypeDef]
    Customized: NotRequired[CustomizedMetricSpecificationTypeDef]


S3DataSourceOutputTypeDef = TypedDict(
    "S3DataSourceOutputTypeDef",
    {
        "S3DataType": S3DataTypeType,
        "S3Uri": str,
        "S3DataDistributionType": NotRequired[S3DataDistributionType],
        "AttributeNames": NotRequired[list[str]],
        "InstanceGroupNames": NotRequired[list[str]],
        "ModelAccessConfig": NotRequired[ModelAccessConfigTypeDef],
        "HubAccessConfig": NotRequired[HubAccessConfigTypeDef],
    },
)
S3DataSourceTypeDef = TypedDict(
    "S3DataSourceTypeDef",
    {
        "S3DataType": S3DataTypeType,
        "S3Uri": str,
        "S3DataDistributionType": NotRequired[S3DataDistributionType],
        "AttributeNames": NotRequired[Sequence[str]],
        "InstanceGroupNames": NotRequired[Sequence[str]],
        "ModelAccessConfig": NotRequired[ModelAccessConfigTypeDef],
        "HubAccessConfig": NotRequired[HubAccessConfigTypeDef],
    },
)


class S3ModelDataSourceTypeDef(TypedDict):
    S3Uri: str
    S3DataType: S3ModelDataTypeType
    CompressionType: ModelCompressionTypeType
    ModelAccessConfig: NotRequired[ModelAccessConfigTypeDef]
    HubAccessConfig: NotRequired[InferenceHubAccessConfigTypeDef]
    ManifestS3Uri: NotRequired[str]
    ETag: NotRequired[str]
    ManifestEtag: NotRequired[str]


class TextGenerationJobConfigOutputTypeDef(TypedDict):
    CompletionCriteria: NotRequired[AutoMLJobCompletionCriteriaTypeDef]
    BaseModelName: NotRequired[str]
    TextGenerationHyperParameters: NotRequired[dict[str, str]]
    ModelAccessConfig: NotRequired[ModelAccessConfigTypeDef]


class TextGenerationJobConfigTypeDef(TypedDict):
    CompletionCriteria: NotRequired[AutoMLJobCompletionCriteriaTypeDef]
    BaseModelName: NotRequired[str]
    TextGenerationHyperParameters: NotRequired[Mapping[str, str]]
    ModelAccessConfig: NotRequired[ModelAccessConfigTypeDef]


ModelBiasAppSpecificationUnionTypeDef = Union[
    ModelBiasAppSpecificationTypeDef, ModelBiasAppSpecificationOutputTypeDef
]
ModelCompilationConfigUnionTypeDef = Union[
    ModelCompilationConfigTypeDef, ModelCompilationConfigOutputTypeDef
]


class MonitoringAlertActionsTypeDef(TypedDict):
    ModelDashboardIndicator: NotRequired[ModelDashboardIndicatorActionTypeDef]


ModelExplainabilityAppSpecificationUnionTypeDef = Union[
    ModelExplainabilityAppSpecificationTypeDef, ModelExplainabilityAppSpecificationOutputTypeDef
]


class ModelInfrastructureConfigTypeDef(TypedDict):
    InfrastructureType: Literal["RealTimeInference"]
    RealTimeInferenceConfig: RealTimeInferenceConfigTypeDef


class RecommendationJobStoppingConditionsOutputTypeDef(TypedDict):
    MaxInvocations: NotRequired[int]
    ModelLatencyThresholds: NotRequired[list[ModelLatencyThresholdTypeDef]]
    FlatInvocations: NotRequired[FlatInvocationsType]


class RecommendationJobStoppingConditionsTypeDef(TypedDict):
    MaxInvocations: NotRequired[int]
    ModelLatencyThresholds: NotRequired[Sequence[ModelLatencyThresholdTypeDef]]
    FlatInvocations: NotRequired[FlatInvocationsType]


class ModelMetadataSearchExpressionTypeDef(TypedDict):
    Filters: NotRequired[Sequence[ModelMetadataFilterTypeDef]]


class ModelPackageStatusDetailsTypeDef(TypedDict):
    ValidationStatuses: list[ModelPackageStatusItemTypeDef]
    ImageScanStatuses: NotRequired[list[ModelPackageStatusItemTypeDef]]


ModelQualityAppSpecificationUnionTypeDef = Union[
    ModelQualityAppSpecificationTypeDef, ModelQualityAppSpecificationOutputTypeDef
]
ModelQuantizationConfigUnionTypeDef = Union[
    ModelQuantizationConfigTypeDef, ModelQuantizationConfigOutputTypeDef
]
ModelShardingConfigUnionTypeDef = Union[
    ModelShardingConfigTypeDef, ModelShardingConfigOutputTypeDef
]


class ModelSpeculativeDecodingConfigTypeDef(TypedDict):
    Technique: Literal["EAGLE"]
    TrainingDataSource: NotRequired[ModelSpeculativeDecodingTrainingDataSourceTypeDef]


class MonitoringResourcesTypeDef(TypedDict):
    ClusterConfig: MonitoringClusterConfigTypeDef


class MonitoringDatasetFormatOutputTypeDef(TypedDict):
    Csv: NotRequired[MonitoringCsvDatasetFormatTypeDef]
    Json: NotRequired[MonitoringJsonDatasetFormatTypeDef]
    Parquet: NotRequired[dict[str, Any]]


class MonitoringDatasetFormatTypeDef(TypedDict):
    Csv: NotRequired[MonitoringCsvDatasetFormatTypeDef]
    Json: NotRequired[MonitoringJsonDatasetFormatTypeDef]
    Parquet: NotRequired[Mapping[str, Any]]


class MonitoringOutputTypeDef(TypedDict):
    S3Output: MonitoringS3OutputTypeDef


NeoVpcConfigUnionTypeDef = Union[NeoVpcConfigTypeDef, NeoVpcConfigOutputTypeDef]


class OfflineStoreConfigTypeDef(TypedDict):
    S3StorageConfig: S3StorageConfigTypeDef
    DisableGlueTableCreation: NotRequired[bool]
    DataCatalogConfig: NotRequired[DataCatalogConfigTypeDef]
    TableFormat: NotRequired[TableFormatType]


OidcMemberDefinitionUnionTypeDef = Union[
    OidcMemberDefinitionTypeDef, OidcMemberDefinitionOutputTypeDef
]


class OnlineStoreConfigTypeDef(TypedDict):
    SecurityConfig: NotRequired[OnlineStoreSecurityConfigTypeDef]
    EnableOnlineStore: NotRequired[bool]
    TtlDuration: NotRequired[TtlDurationTypeDef]
    StorageType: NotRequired[StorageTypeType]


class OnlineStoreConfigUpdateTypeDef(TypedDict):
    TtlDuration: NotRequired[TtlDurationTypeDef]


class OptimizationJobModelSourceS3TypeDef(TypedDict):
    S3Uri: NotRequired[str]
    ModelAccessConfig: NotRequired[OptimizationModelAccessConfigTypeDef]


class OptimizationJobOutputConfigTypeDef(TypedDict):
    S3OutputLocation: str
    KmsKeyId: NotRequired[str]
    SageMakerModel: NotRequired[OptimizationSageMakerModelTypeDef]


OptimizationVpcConfigUnionTypeDef = Union[
    OptimizationVpcConfigTypeDef, OptimizationVpcConfigOutputTypeDef
]


class OutputConfigTypeDef(TypedDict):
    S3OutputLocation: str
    TargetDevice: NotRequired[TargetDeviceType]
    TargetPlatform: NotRequired[TargetPlatformTypeDef]
    CompilerOptions: NotRequired[str]
    KmsKeyId: NotRequired[str]


class PartnerAppConfigOutputTypeDef(TypedDict):
    AdminUsers: NotRequired[list[str]]
    Arguments: NotRequired[dict[str, str]]
    AssignedGroupPatterns: NotRequired[list[str]]
    RoleGroupAssignments: NotRequired[list[RoleGroupAssignmentOutputTypeDef]]


class PartnerAppConfigTypeDef(TypedDict):
    AdminUsers: NotRequired[Sequence[str]]
    Arguments: NotRequired[Mapping[str, str]]
    AssignedGroupPatterns: NotRequired[Sequence[str]]
    RoleGroupAssignments: NotRequired[Sequence[RoleGroupAssignmentTypeDef]]


class PendingProductionVariantSummaryTypeDef(TypedDict):
    VariantName: str
    DeployedImages: NotRequired[list[DeployedImageTypeDef]]
    CurrentWeight: NotRequired[float]
    DesiredWeight: NotRequired[float]
    CurrentInstanceCount: NotRequired[int]
    DesiredInstanceCount: NotRequired[int]
    InstanceType: NotRequired[ProductionVariantInstanceTypeType]
    AcceleratorType: NotRequired[ProductionVariantAcceleratorTypeType]
    VariantStatus: NotRequired[list[ProductionVariantStatusTypeDef]]
    CurrentServerlessConfig: NotRequired[ProductionVariantServerlessConfigTypeDef]
    DesiredServerlessConfig: NotRequired[ProductionVariantServerlessConfigTypeDef]
    ManagedInstanceScaling: NotRequired[ProductionVariantManagedInstanceScalingTypeDef]
    RoutingConfig: NotRequired[ProductionVariantRoutingConfigTypeDef]


class SchedulerConfigOutputTypeDef(TypedDict):
    PriorityClasses: NotRequired[list[PriorityClassTypeDef]]
    FairShare: NotRequired[FairShareType]
    IdleResourceSharing: NotRequired[IdleResourceSharingType]


class SchedulerConfigTypeDef(TypedDict):
    PriorityClasses: NotRequired[Sequence[PriorityClassTypeDef]]
    FairShare: NotRequired[FairShareType]
    IdleResourceSharing: NotRequired[IdleResourceSharingType]


class ProcessingResourcesTypeDef(TypedDict):
    ClusterConfig: ProcessingClusterConfigTypeDef


class ProcessingOutputTypeDef(TypedDict):
    OutputName: str
    S3Output: NotRequired[ProcessingS3OutputTypeDef]
    FeatureStoreOutput: NotRequired[ProcessingFeatureStoreOutputTypeDef]
    AppManaged: NotRequired[bool]


class ProductionVariantTypeDef(TypedDict):
    VariantName: str
    ModelName: NotRequired[str]
    InitialInstanceCount: NotRequired[int]
    InstanceType: NotRequired[ProductionVariantInstanceTypeType]
    InitialVariantWeight: NotRequired[float]
    AcceleratorType: NotRequired[ProductionVariantAcceleratorTypeType]
    CoreDumpConfig: NotRequired[ProductionVariantCoreDumpConfigTypeDef]
    ServerlessConfig: NotRequired[ProductionVariantServerlessConfigTypeDef]
    VolumeSizeInGB: NotRequired[int]
    ModelDataDownloadTimeoutInSeconds: NotRequired[int]
    ContainerStartupHealthCheckTimeoutInSeconds: NotRequired[int]
    EnableSSMAccess: NotRequired[bool]
    ManagedInstanceScaling: NotRequired[ProductionVariantManagedInstanceScalingTypeDef]
    RoutingConfig: NotRequired[ProductionVariantRoutingConfigTypeDef]
    InferenceAmiVersion: NotRequired[ProductionVariantInferenceAmiVersionType]
    CapacityReservationConfig: NotRequired[ProductionVariantCapacityReservationConfigTypeDef]


ProfilerConfigUnionTypeDef = Union[ProfilerConfigTypeDef, ProfilerConfigOutputTypeDef]
ProfilerRuleConfigurationUnionTypeDef = Union[
    ProfilerRuleConfigurationTypeDef, ProfilerRuleConfigurationOutputTypeDef
]


class SuggestionQueryTypeDef(TypedDict):
    PropertyNameQuery: NotRequired[PropertyNameQueryTypeDef]


class ServiceCatalogProvisioningDetailsOutputTypeDef(TypedDict):
    ProductId: str
    ProvisioningArtifactId: NotRequired[str]
    PathId: NotRequired[str]
    ProvisioningParameters: NotRequired[list[ProvisioningParameterTypeDef]]


class ServiceCatalogProvisioningDetailsTypeDef(TypedDict):
    ProductId: str
    ProvisioningArtifactId: NotRequired[str]
    PathId: NotRequired[str]
    ProvisioningParameters: NotRequired[Sequence[ProvisioningParameterTypeDef]]


class ServiceCatalogProvisioningUpdateDetailsTypeDef(TypedDict):
    ProvisioningArtifactId: NotRequired[str]
    ProvisioningParameters: NotRequired[Sequence[ProvisioningParameterTypeDef]]


class PublicWorkforceTaskPriceTypeDef(TypedDict):
    AmountInUsd: NotRequired[USDTypeDef]


class QueryLineageResponseTypeDef(TypedDict):
    Vertices: list[VertexTypeDef]
    Edges: list[EdgeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class RecommendationJobOutputConfigTypeDef(TypedDict):
    KmsKeyId: NotRequired[str]
    CompiledOutputConfig: NotRequired[RecommendationJobCompiledOutputConfigTypeDef]


class RecommendationJobContainerConfigOutputTypeDef(TypedDict):
    Domain: NotRequired[str]
    Task: NotRequired[str]
    Framework: NotRequired[str]
    FrameworkVersion: NotRequired[str]
    PayloadConfig: NotRequired[RecommendationJobPayloadConfigOutputTypeDef]
    NearestModelName: NotRequired[str]
    SupportedInstanceTypes: NotRequired[list[str]]
    SupportedEndpointType: NotRequired[RecommendationJobSupportedEndpointTypeType]
    DataInputConfig: NotRequired[str]
    SupportedResponseMIMETypes: NotRequired[list[str]]


class RecommendationJobContainerConfigTypeDef(TypedDict):
    Domain: NotRequired[str]
    Task: NotRequired[str]
    Framework: NotRequired[str]
    FrameworkVersion: NotRequired[str]
    PayloadConfig: NotRequired[RecommendationJobPayloadConfigTypeDef]
    NearestModelName: NotRequired[str]
    SupportedInstanceTypes: NotRequired[Sequence[str]]
    SupportedEndpointType: NotRequired[RecommendationJobSupportedEndpointTypeType]
    DataInputConfig: NotRequired[str]
    SupportedResponseMIMETypes: NotRequired[Sequence[str]]


class RenderUiTemplateRequestTypeDef(TypedDict):
    Task: RenderableTaskTypeDef
    RoleArn: str
    UiTemplate: NotRequired[UiTemplateTypeDef]
    HumanTaskUiArn: NotRequired[str]


class RenderUiTemplateResponseTypeDef(TypedDict):
    RenderedContent: str
    Errors: list[RenderingErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TrainingPlanOfferingTypeDef(TypedDict):
    TrainingPlanOfferingId: str
    TargetResources: list[SageMakerResourceNameType]
    RequestedStartTimeAfter: NotRequired[datetime]
    RequestedEndTimeBefore: NotRequired[datetime]
    DurationHours: NotRequired[int]
    DurationMinutes: NotRequired[int]
    UpfrontFee: NotRequired[str]
    CurrencyCode: NotRequired[str]
    ReservedCapacityOfferings: NotRequired[list[ReservedCapacityOfferingTypeDef]]


class SelectiveExecutionConfigOutputTypeDef(TypedDict):
    SelectedSteps: list[SelectedStepTypeDef]
    SourcePipelineExecutionArn: NotRequired[str]


class SelectiveExecutionConfigTypeDef(TypedDict):
    SelectedSteps: Sequence[SelectedStepTypeDef]
    SourcePipelineExecutionArn: NotRequired[str]


class ShadowModeConfigOutputTypeDef(TypedDict):
    SourceModelVariantName: str
    ShadowModelVariants: list[ShadowModelVariantConfigTypeDef]


class ShadowModeConfigTypeDef(TypedDict):
    SourceModelVariantName: str
    ShadowModelVariants: Sequence[ShadowModelVariantConfigTypeDef]


SourceIpConfigUnionTypeDef = Union[SourceIpConfigTypeDef, SourceIpConfigOutputTypeDef]


class SpaceAppLifecycleManagementTypeDef(TypedDict):
    IdleSettings: NotRequired[SpaceIdleSettingsTypeDef]


class TrafficPatternOutputTypeDef(TypedDict):
    TrafficType: NotRequired[TrafficTypeType]
    Phases: NotRequired[list[PhaseTypeDef]]
    Stairs: NotRequired[StairsTypeDef]


class TrafficPatternTypeDef(TypedDict):
    TrafficType: NotRequired[TrafficTypeType]
    Phases: NotRequired[Sequence[PhaseTypeDef]]
    Stairs: NotRequired[StairsTypeDef]


class TrainingImageConfigTypeDef(TypedDict):
    TrainingRepositoryAccessMode: TrainingRepositoryAccessModeType
    TrainingRepositoryAuthConfig: NotRequired[TrainingRepositoryAuthConfigTypeDef]


class TransformDataSourceTypeDef(TypedDict):
    S3DataSource: TransformS3DataSourceTypeDef


class WorkforceTypeDef(TypedDict):
    WorkforceName: str
    WorkforceArn: str
    LastUpdatedDate: NotRequired[datetime]
    SourceIpConfig: NotRequired[SourceIpConfigOutputTypeDef]
    SubDomain: NotRequired[str]
    CognitoConfig: NotRequired[CognitoConfigTypeDef]
    OidcConfig: NotRequired[OidcConfigForResponseTypeDef]
    CreateDate: NotRequired[datetime]
    WorkforceVpcConfig: NotRequired[WorkforceVpcConfigResponseTypeDef]
    Status: NotRequired[WorkforceStatusType]
    FailureReason: NotRequired[str]
    IpAddressType: NotRequired[WorkforceIpAddressTypeType]


class ResourceSharingConfigOutputTypeDef(TypedDict):
    Strategy: ResourceSharingStrategyType
    BorrowLimit: NotRequired[int]
    AbsoluteBorrowLimits: NotRequired[list[ComputeQuotaResourceConfigTypeDef]]


class ResourceSharingConfigTypeDef(TypedDict):
    Strategy: ResourceSharingStrategyType
    BorrowLimit: NotRequired[int]
    AbsoluteBorrowLimits: NotRequired[Sequence[ComputeQuotaResourceConfigTypeDef]]


class ListActionsResponseTypeDef(TypedDict):
    ActionSummaries: list[ActionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


HyperParameterAlgorithmSpecificationUnionTypeDef = Union[
    HyperParameterAlgorithmSpecificationTypeDef, HyperParameterAlgorithmSpecificationOutputTypeDef
]


class ListAppsResponseTypeDef(TypedDict):
    Apps: list[AppDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DomainSettingsOutputTypeDef(TypedDict):
    SecurityGroupIds: NotRequired[list[str]]
    RStudioServerProDomainSettings: NotRequired[RStudioServerProDomainSettingsTypeDef]
    ExecutionRoleIdentityConfig: NotRequired[ExecutionRoleIdentityConfigType]
    TrustedIdentityPropagationSettings: NotRequired[TrustedIdentityPropagationSettingsTypeDef]
    DockerSettings: NotRequired[DockerSettingsOutputTypeDef]
    AmazonQSettings: NotRequired[AmazonQSettingsTypeDef]
    UnifiedStudioSettings: NotRequired[UnifiedStudioSettingsTypeDef]
    IpAddressType: NotRequired[IPAddressTypeType]


class DomainSettingsTypeDef(TypedDict):
    SecurityGroupIds: NotRequired[Sequence[str]]
    RStudioServerProDomainSettings: NotRequired[RStudioServerProDomainSettingsTypeDef]
    ExecutionRoleIdentityConfig: NotRequired[ExecutionRoleIdentityConfigType]
    TrustedIdentityPropagationSettings: NotRequired[TrustedIdentityPropagationSettingsTypeDef]
    DockerSettings: NotRequired[DockerSettingsTypeDef]
    AmazonQSettings: NotRequired[AmazonQSettingsTypeDef]
    UnifiedStudioSettings: NotRequired[UnifiedStudioSettingsTypeDef]
    IpAddressType: NotRequired[IPAddressTypeType]


class CodeEditorAppSettingsOutputTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    CustomImages: NotRequired[list[CustomImageTypeDef]]
    LifecycleConfigArns: NotRequired[list[str]]
    AppLifecycleManagement: NotRequired[AppLifecycleManagementTypeDef]
    BuiltInLifecycleConfigArn: NotRequired[str]


class CodeEditorAppSettingsTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    CustomImages: NotRequired[Sequence[CustomImageTypeDef]]
    LifecycleConfigArns: NotRequired[Sequence[str]]
    AppLifecycleManagement: NotRequired[AppLifecycleManagementTypeDef]
    BuiltInLifecycleConfigArn: NotRequired[str]


class JupyterLabAppSettingsOutputTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    CustomImages: NotRequired[list[CustomImageTypeDef]]
    LifecycleConfigArns: NotRequired[list[str]]
    CodeRepositories: NotRequired[list[CodeRepositoryTypeDef]]
    AppLifecycleManagement: NotRequired[AppLifecycleManagementTypeDef]
    EmrSettings: NotRequired[EmrSettingsOutputTypeDef]
    BuiltInLifecycleConfigArn: NotRequired[str]


class JupyterLabAppSettingsTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    CustomImages: NotRequired[Sequence[CustomImageTypeDef]]
    LifecycleConfigArns: NotRequired[Sequence[str]]
    CodeRepositories: NotRequired[Sequence[CodeRepositoryTypeDef]]
    AppLifecycleManagement: NotRequired[AppLifecycleManagementTypeDef]
    EmrSettings: NotRequired[EmrSettingsTypeDef]
    BuiltInLifecycleConfigArn: NotRequired[str]


class ArtifactSummaryTypeDef(TypedDict):
    ArtifactArn: NotRequired[str]
    ArtifactName: NotRequired[str]
    Source: NotRequired[ArtifactSourceOutputTypeDef]
    ArtifactType: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]


ArtifactSourceUnionTypeDef = Union[ArtifactSourceTypeDef, ArtifactSourceOutputTypeDef]


class AsyncInferenceConfigOutputTypeDef(TypedDict):
    OutputConfig: AsyncInferenceOutputConfigOutputTypeDef
    ClientConfig: NotRequired[AsyncInferenceClientConfigTypeDef]


class AsyncInferenceConfigTypeDef(TypedDict):
    OutputConfig: AsyncInferenceOutputConfigTypeDef
    ClientConfig: NotRequired[AsyncInferenceClientConfigTypeDef]


class TabularJobConfigOutputTypeDef(TypedDict):
    TargetAttributeName: str
    CandidateGenerationConfig: NotRequired[CandidateGenerationConfigOutputTypeDef]
    CompletionCriteria: NotRequired[AutoMLJobCompletionCriteriaTypeDef]
    FeatureSpecificationS3Uri: NotRequired[str]
    Mode: NotRequired[AutoMLModeType]
    GenerateCandidateDefinitionsOnly: NotRequired[bool]
    ProblemType: NotRequired[ProblemTypeType]
    SampleWeightAttributeName: NotRequired[str]


class TimeSeriesForecastingJobConfigOutputTypeDef(TypedDict):
    ForecastFrequency: str
    ForecastHorizon: int
    TimeSeriesConfig: TimeSeriesConfigOutputTypeDef
    FeatureSpecificationS3Uri: NotRequired[str]
    CompletionCriteria: NotRequired[AutoMLJobCompletionCriteriaTypeDef]
    ForecastQuantiles: NotRequired[list[str]]
    Transformations: NotRequired[TimeSeriesTransformationsOutputTypeDef]
    HolidayConfig: NotRequired[list[HolidayConfigAttributesTypeDef]]
    CandidateGenerationConfig: NotRequired[CandidateGenerationConfigOutputTypeDef]


class TabularJobConfigTypeDef(TypedDict):
    TargetAttributeName: str
    CandidateGenerationConfig: NotRequired[CandidateGenerationConfigTypeDef]
    CompletionCriteria: NotRequired[AutoMLJobCompletionCriteriaTypeDef]
    FeatureSpecificationS3Uri: NotRequired[str]
    Mode: NotRequired[AutoMLModeType]
    GenerateCandidateDefinitionsOnly: NotRequired[bool]
    ProblemType: NotRequired[ProblemTypeType]
    SampleWeightAttributeName: NotRequired[str]


class TimeSeriesForecastingJobConfigTypeDef(TypedDict):
    ForecastFrequency: str
    ForecastHorizon: int
    TimeSeriesConfig: TimeSeriesConfigTypeDef
    FeatureSpecificationS3Uri: NotRequired[str]
    CompletionCriteria: NotRequired[AutoMLJobCompletionCriteriaTypeDef]
    ForecastQuantiles: NotRequired[Sequence[str]]
    Transformations: NotRequired[TimeSeriesTransformationsTypeDef]
    HolidayConfig: NotRequired[Sequence[HolidayConfigAttributesTypeDef]]
    CandidateGenerationConfig: NotRequired[CandidateGenerationConfigTypeDef]


class AutoMLChannelTypeDef(TypedDict):
    TargetAttributeName: str
    DataSource: NotRequired[AutoMLDataSourceTypeDef]
    CompressionType: NotRequired[CompressionTypeType]
    ContentType: NotRequired[str]
    ChannelType: NotRequired[AutoMLChannelTypeType]
    SampleWeightAttributeName: NotRequired[str]


class AutoMLJobChannelTypeDef(TypedDict):
    ChannelType: NotRequired[AutoMLChannelTypeType]
    ContentType: NotRequired[str]
    CompressionType: NotRequired[CompressionTypeType]
    DataSource: NotRequired[AutoMLDataSourceTypeDef]


class ListAutoMLJobsResponseTypeDef(TypedDict):
    AutoMLJobSummaries: list[AutoMLJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AutoMLResolvedAttributesTypeDef(TypedDict):
    AutoMLJobObjective: NotRequired[AutoMLJobObjectiveTypeDef]
    CompletionCriteria: NotRequired[AutoMLJobCompletionCriteriaTypeDef]
    AutoMLProblemTypeResolvedAttributes: NotRequired[AutoMLProblemTypeResolvedAttributesTypeDef]


class AutoMLJobConfigOutputTypeDef(TypedDict):
    CompletionCriteria: NotRequired[AutoMLJobCompletionCriteriaTypeDef]
    SecurityConfig: NotRequired[AutoMLSecurityConfigOutputTypeDef]
    CandidateGenerationConfig: NotRequired[AutoMLCandidateGenerationConfigOutputTypeDef]
    DataSplitConfig: NotRequired[AutoMLDataSplitConfigTypeDef]
    Mode: NotRequired[AutoMLModeType]


class LabelingJobAlgorithmsConfigOutputTypeDef(TypedDict):
    LabelingJobAlgorithmSpecificationArn: str
    InitialActiveLearningModelArn: NotRequired[str]
    LabelingJobResourceConfig: NotRequired[LabelingJobResourceConfigOutputTypeDef]


class AutoMLJobConfigTypeDef(TypedDict):
    CompletionCriteria: NotRequired[AutoMLJobCompletionCriteriaTypeDef]
    SecurityConfig: NotRequired[AutoMLSecurityConfigTypeDef]
    CandidateGenerationConfig: NotRequired[AutoMLCandidateGenerationConfigTypeDef]
    DataSplitConfig: NotRequired[AutoMLDataSplitConfigTypeDef]
    Mode: NotRequired[AutoMLModeType]


AutoMLSecurityConfigUnionTypeDef = Union[
    AutoMLSecurityConfigTypeDef, AutoMLSecurityConfigOutputTypeDef
]


class LabelingJobAlgorithmsConfigTypeDef(TypedDict):
    LabelingJobAlgorithmSpecificationArn: str
    InitialActiveLearningModelArn: NotRequired[str]
    LabelingJobResourceConfig: NotRequired[LabelingJobResourceConfigTypeDef]


MonitoringNetworkConfigUnionTypeDef = Union[
    MonitoringNetworkConfigTypeDef, MonitoringNetworkConfigOutputTypeDef
]
NetworkConfigUnionTypeDef = Union[NetworkConfigTypeDef, NetworkConfigOutputTypeDef]


class ModelMetricsTypeDef(TypedDict):
    ModelQuality: NotRequired[ModelQualityTypeDef]
    ModelDataQuality: NotRequired[ModelDataQualityTypeDef]
    Bias: NotRequired[BiasTypeDef]
    Explainability: NotRequired[ExplainabilityTypeDef]


class PipelineExecutionStepMetadataTypeDef(TypedDict):
    TrainingJob: NotRequired[TrainingJobStepMetadataTypeDef]
    ProcessingJob: NotRequired[ProcessingJobStepMetadataTypeDef]
    TransformJob: NotRequired[TransformJobStepMetadataTypeDef]
    TuningJob: NotRequired[TuningJobStepMetaDataTypeDef]
    Model: NotRequired[ModelStepMetadataTypeDef]
    RegisterModel: NotRequired[RegisterModelStepMetadataTypeDef]
    Condition: NotRequired[ConditionStepMetadataTypeDef]
    Callback: NotRequired[CallbackStepMetadataTypeDef]
    Lambda: NotRequired[LambdaStepMetadataTypeDef]
    EMR: NotRequired[EMRStepMetadataTypeDef]
    QualityCheck: NotRequired[QualityCheckStepMetadataTypeDef]
    ClarifyCheck: NotRequired[ClarifyCheckStepMetadataTypeDef]
    Fail: NotRequired[FailStepMetadataTypeDef]
    AutoMLJob: NotRequired[AutoMLJobStepMetadataTypeDef]
    Endpoint: NotRequired[EndpointStepMetadataTypeDef]
    EndpointConfig: NotRequired[EndpointConfigStepMetadataTypeDef]
    BedrockCustomModel: NotRequired[BedrockCustomModelMetadataTypeDef]
    BedrockCustomModelDeployment: NotRequired[BedrockCustomModelDeploymentMetadataTypeDef]
    BedrockProvisionedModelThroughput: NotRequired[BedrockProvisionedModelThroughputMetadataTypeDef]
    BedrockModelImport: NotRequired[BedrockModelImportMetadataTypeDef]
    InferenceComponent: NotRequired[InferenceComponentMetadataTypeDef]
    Lineage: NotRequired[LineageMetadataTypeDef]


class AutoMLCandidateTypeDef(TypedDict):
    CandidateName: str
    ObjectiveStatus: ObjectiveStatusType
    CandidateSteps: list[AutoMLCandidateStepTypeDef]
    CandidateStatus: CandidateStatusType
    CreationTime: datetime
    LastModifiedTime: datetime
    FinalAutoMLJobObjectiveMetric: NotRequired[FinalAutoMLJobObjectiveMetricTypeDef]
    InferenceContainers: NotRequired[list[AutoMLContainerDefinitionTypeDef]]
    EndTime: NotRequired[datetime]
    FailureReason: NotRequired[str]
    CandidateProperties: NotRequired[CandidatePropertiesTypeDef]
    InferenceContainerDefinitions: NotRequired[
        dict[AutoMLProcessingUnitType, list[AutoMLContainerDefinitionTypeDef]]
    ]


class EventMetadataTypeDef(TypedDict):
    Cluster: NotRequired[ClusterMetadataTypeDef]
    InstanceGroup: NotRequired[InstanceGroupMetadataTypeDef]
    InstanceGroupScaling: NotRequired[InstanceGroupScalingMetadataTypeDef]
    Instance: NotRequired[InstanceMetadataTypeDef]


class DeploymentConfigurationOutputTypeDef(TypedDict):
    RollingUpdatePolicy: NotRequired[RollingDeploymentPolicyTypeDef]
    WaitIntervalInSeconds: NotRequired[int]
    AutoRollbackConfiguration: NotRequired[list[AlarmDetailsTypeDef]]


class DeploymentConfigurationTypeDef(TypedDict):
    RollingUpdatePolicy: NotRequired[RollingDeploymentPolicyTypeDef]
    WaitIntervalInSeconds: NotRequired[int]
    AutoRollbackConfiguration: NotRequired[Sequence[AlarmDetailsTypeDef]]


class BlueGreenUpdatePolicyTypeDef(TypedDict):
    TrafficRoutingConfiguration: TrafficRoutingConfigTypeDef
    TerminationWaitInSeconds: NotRequired[int]
    MaximumExecutionTimeoutInSeconds: NotRequired[int]


InferenceExperimentDataStorageConfigUnionTypeDef = Union[
    InferenceExperimentDataStorageConfigTypeDef, InferenceExperimentDataStorageConfigOutputTypeDef
]
DataCaptureConfigUnionTypeDef = Union[DataCaptureConfigTypeDef, DataCaptureConfigOutputTypeDef]


class EndpointInputConfigurationOutputTypeDef(TypedDict):
    InstanceType: NotRequired[ProductionVariantInstanceTypeType]
    ServerlessConfig: NotRequired[ProductionVariantServerlessConfigTypeDef]
    InferenceSpecificationName: NotRequired[str]
    EnvironmentParameterRanges: NotRequired[EnvironmentParameterRangesOutputTypeDef]


class ParameterRangesTypeDef(TypedDict):
    IntegerParameterRanges: NotRequired[Sequence[IntegerParameterRangeTypeDef]]
    ContinuousParameterRanges: NotRequired[Sequence[ContinuousParameterRangeTypeDef]]
    CategoricalParameterRanges: NotRequired[Sequence[CategoricalParameterRangeUnionTypeDef]]
    AutoParameters: NotRequired[Sequence[AutoParameterTypeDef]]


class EndpointInputConfigurationTypeDef(TypedDict):
    InstanceType: NotRequired[ProductionVariantInstanceTypeType]
    ServerlessConfig: NotRequired[ProductionVariantServerlessConfigTypeDef]
    InferenceSpecificationName: NotRequired[str]
    EnvironmentParameterRanges: NotRequired[EnvironmentParameterRangesTypeDef]


class CreateTemplateProviderTypeDef(TypedDict):
    CfnTemplateProvider: NotRequired[CfnCreateTemplateProviderTypeDef]


class TemplateProviderDetailTypeDef(TypedDict):
    CfnTemplateProviderDetail: NotRequired[CfnTemplateProviderDetailTypeDef]


class UpdateTemplateProviderTypeDef(TypedDict):
    CfnTemplateProvider: NotRequired[CfnUpdateTemplateProviderTypeDef]


class ClarifyExplainerConfigOutputTypeDef(TypedDict):
    ShapConfig: ClarifyShapConfigTypeDef
    EnableExplanations: NotRequired[str]
    InferenceConfig: NotRequired[ClarifyInferenceConfigOutputTypeDef]


class ClarifyExplainerConfigTypeDef(TypedDict):
    ShapConfig: ClarifyShapConfigTypeDef
    EnableExplanations: NotRequired[str]
    InferenceConfig: NotRequired[ClarifyInferenceConfigTypeDef]


class ClusterNodeDetailsTypeDef(TypedDict):
    InstanceGroupName: NotRequired[str]
    InstanceId: NotRequired[str]
    NodeLogicalId: NotRequired[str]
    InstanceStatus: NotRequired[ClusterInstanceStatusDetailsTypeDef]
    InstanceType: NotRequired[ClusterInstanceTypeType]
    LaunchTime: NotRequired[datetime]
    LastSoftwareUpdateTime: NotRequired[datetime]
    LifeCycleConfig: NotRequired[ClusterLifeCycleConfigTypeDef]
    OverrideVpcConfig: NotRequired[VpcConfigOutputTypeDef]
    ThreadsPerCore: NotRequired[int]
    InstanceStorageConfigs: NotRequired[list[ClusterInstanceStorageConfigTypeDef]]
    PrivatePrimaryIp: NotRequired[str]
    PrivatePrimaryIpv6: NotRequired[str]
    PrivateDnsHostname: NotRequired[str]
    Placement: NotRequired[ClusterInstancePlacementTypeDef]
    CurrentImageId: NotRequired[str]
    DesiredImageId: NotRequired[str]
    UltraServerInfo: NotRequired[UltraServerInfoTypeDef]
    KubernetesConfig: NotRequired[ClusterKubernetesConfigNodeDetailsTypeDef]
    CapacityType: NotRequired[ClusterCapacityTypeType]


class ListClusterNodesResponseTypeDef(TypedDict):
    ClusterNodeSummaries: list[ClusterNodeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


CodeEditorAppImageConfigUnionTypeDef = Union[
    CodeEditorAppImageConfigTypeDef, CodeEditorAppImageConfigOutputTypeDef
]
JupyterLabAppImageConfigUnionTypeDef = Union[
    JupyterLabAppImageConfigTypeDef, JupyterLabAppImageConfigOutputTypeDef
]


class ListCodeRepositoriesOutputTypeDef(TypedDict):
    CodeRepositorySummaryList: list[CodeRepositorySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class FeatureDefinitionTypeDef(TypedDict):
    FeatureName: str
    FeatureType: FeatureTypeType
    CollectionType: NotRequired[CollectionTypeType]
    CollectionConfig: NotRequired[CollectionConfigTypeDef]


DebugHookConfigUnionTypeDef = Union[DebugHookConfigTypeDef, DebugHookConfigOutputTypeDef]


class ListContextsResponseTypeDef(TypedDict):
    ContextSummaries: list[ContextSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListModelPackagesOutputTypeDef(TypedDict):
    ModelPackageSummaryList: list[ModelPackageSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


InferenceExperimentScheduleUnionTypeDef = Union[
    InferenceExperimentScheduleTypeDef, InferenceExperimentScheduleOutputTypeDef
]


class QueryLineageRequestTypeDef(TypedDict):
    StartArns: NotRequired[Sequence[str]]
    Direction: NotRequired[DirectionType]
    IncludeEdges: NotRequired[bool]
    Filters: NotRequired[QueryFiltersTypeDef]
    MaxDepth: NotRequired[int]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ProcessingInputTypeDef(TypedDict):
    InputName: str
    AppManaged: NotRequired[bool]
    S3Input: NotRequired[ProcessingS3InputTypeDef]
    DatasetDefinition: NotRequired[DatasetDefinitionTypeDef]


InferenceComponentSpecificationSummaryTypeDef = TypedDict(
    "InferenceComponentSpecificationSummaryTypeDef",
    {
        "ModelName": NotRequired[str],
        "Container": NotRequired[InferenceComponentContainerSpecificationSummaryTypeDef],
        "StartupParameters": NotRequired[InferenceComponentStartupParametersTypeDef],
        "ComputeResourceRequirements": NotRequired[
            InferenceComponentComputeResourceRequirementsTypeDef
        ],
        "BaseInferenceComponentName": NotRequired[str],
        "DataCacheConfig": NotRequired[InferenceComponentDataCacheConfigSummaryTypeDef],
    },
)


class DescribeEdgeDeploymentPlanResponseTypeDef(TypedDict):
    EdgeDeploymentPlanArn: str
    EdgeDeploymentPlanName: str
    ModelConfigs: list[EdgeDeploymentModelConfigTypeDef]
    DeviceFleetName: str
    EdgeDeploymentSuccess: int
    EdgeDeploymentPending: int
    EdgeDeploymentFailed: int
    Stages: list[DeploymentStageStatusSummaryTypeDef]
    CreationTime: datetime
    LastModifiedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListExperimentsResponseTypeDef(TypedDict):
    ExperimentSummaries: list[ExperimentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListFeatureGroupsResponseTypeDef(TypedDict):
    FeatureGroupSummaries: list[FeatureGroupSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListInferenceExperimentsResponseTypeDef(TypedDict):
    InferenceExperiments: list[InferenceExperimentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTrainingJobsResponseTypeDef(TypedDict):
    TrainingJobSummaries: list[TrainingJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTrainingPlansResponseTypeDef(TypedDict):
    TrainingPlanSummaries: list[TrainingPlanSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTrialsResponseTypeDef(TypedDict):
    TrialSummaries: list[TrialSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateEndpointWeightsAndCapacitiesInputTypeDef(TypedDict):
    EndpointName: str
    DesiredWeightsAndCapacities: Sequence[DesiredWeightAndCapacityTypeDef]


class DeploymentStageTypeDef(TypedDict):
    StageName: str
    DeviceSelectionConfig: DeviceSelectionConfigUnionTypeDef
    DeploymentConfig: NotRequired[EdgeDeploymentConfigTypeDef]


class ListDevicesResponseTypeDef(TypedDict):
    DeviceSummaries: list[DeviceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DomainSettingsForUpdateTypeDef(TypedDict):
    RStudioServerProDomainSettingsForUpdate: NotRequired[
        RStudioServerProDomainSettingsForUpdateTypeDef
    ]
    ExecutionRoleIdentityConfig: NotRequired[ExecutionRoleIdentityConfigType]
    SecurityGroupIds: NotRequired[Sequence[str]]
    TrustedIdentityPropagationSettings: NotRequired[TrustedIdentityPropagationSettingsTypeDef]
    DockerSettings: NotRequired[DockerSettingsUnionTypeDef]
    AmazonQSettings: NotRequired[AmazonQSettingsTypeDef]
    UnifiedStudioSettings: NotRequired[UnifiedStudioSettingsTypeDef]
    IpAddressType: NotRequired[IPAddressTypeType]


class DriftCheckBaselinesTypeDef(TypedDict):
    Bias: NotRequired[DriftCheckBiasTypeDef]
    Explainability: NotRequired[DriftCheckExplainabilityTypeDef]
    ModelQuality: NotRequired[DriftCheckModelQualityTypeDef]
    ModelDataQuality: NotRequired[DriftCheckModelDataQualityTypeDef]


class SpaceSettingsSummaryTypeDef(TypedDict):
    AppType: NotRequired[AppTypeType]
    RemoteAccess: NotRequired[FeatureStatusType]
    SpaceStorageSettings: NotRequired[SpaceStorageSettingsTypeDef]


class ProductionVariantSummaryTypeDef(TypedDict):
    VariantName: str
    DeployedImages: NotRequired[list[DeployedImageTypeDef]]
    CurrentWeight: NotRequired[float]
    DesiredWeight: NotRequired[float]
    CurrentInstanceCount: NotRequired[int]
    DesiredInstanceCount: NotRequired[int]
    VariantStatus: NotRequired[list[ProductionVariantStatusTypeDef]]
    CurrentServerlessConfig: NotRequired[ProductionVariantServerlessConfigTypeDef]
    DesiredServerlessConfig: NotRequired[ProductionVariantServerlessConfigTypeDef]
    ManagedInstanceScaling: NotRequired[ProductionVariantManagedInstanceScalingTypeDef]
    RoutingConfig: NotRequired[ProductionVariantRoutingConfigTypeDef]
    CapacityReservationConfig: NotRequired[ProductionVariantCapacityReservationSummaryTypeDef]


class InferenceRecommendationTypeDef(TypedDict):
    EndpointConfiguration: EndpointOutputConfigurationTypeDef
    ModelConfiguration: ModelConfigurationTypeDef
    RecommendationId: NotRequired[str]
    Metrics: NotRequired[RecommendationMetricsTypeDef]
    InvocationEndTime: NotRequired[datetime]
    InvocationStartTime: NotRequired[datetime]


class RecommendationJobInferenceBenchmarkTypeDef(TypedDict):
    ModelConfiguration: ModelConfigurationTypeDef
    Metrics: NotRequired[RecommendationMetricsTypeDef]
    EndpointMetrics: NotRequired[InferenceMetricsTypeDef]
    EndpointConfiguration: NotRequired[EndpointOutputConfigurationTypeDef]
    FailureReason: NotRequired[str]
    InvocationEndTime: NotRequired[datetime]
    InvocationStartTime: NotRequired[datetime]


class SearchExpressionPaginatorTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    NestedFilters: NotRequired[Sequence[NestedFiltersTypeDef]]
    SubExpressions: NotRequired[Sequence[Mapping[str, Any]]]
    Operator: NotRequired[BooleanOperatorType]


class SearchExpressionTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    NestedFilters: NotRequired[Sequence[NestedFiltersTypeDef]]
    SubExpressions: NotRequired[Sequence[Mapping[str, Any]]]
    Operator: NotRequired[BooleanOperatorType]


class ListTrainingJobsForHyperParameterTuningJobResponseTypeDef(TypedDict):
    TrainingJobSummaries: list[HyperParameterTrainingJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


HyperParameterTuningResourceConfigUnionTypeDef = Union[
    HyperParameterTuningResourceConfigTypeDef, HyperParameterTuningResourceConfigOutputTypeDef
]


class ListHyperParameterTuningJobsResponseTypeDef(TypedDict):
    HyperParameterTuningJobSummaries: list[HyperParameterTuningJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


HyperParameterTuningJobWarmStartConfigUnionTypeDef = Union[
    HyperParameterTuningJobWarmStartConfigTypeDef,
    HyperParameterTuningJobWarmStartConfigOutputTypeDef,
]


class AssociationSummaryTypeDef(TypedDict):
    SourceArn: NotRequired[str]
    DestinationArn: NotRequired[str]
    SourceType: NotRequired[str]
    DestinationType: NotRequired[str]
    AssociationType: NotRequired[AssociationEdgeTypeType]
    SourceName: NotRequired[str]
    DestinationName: NotRequired[str]
    CreationTime: NotRequired[datetime]
    CreatedBy: NotRequired[UserContextTypeDef]


class DescribeActionResponseTypeDef(TypedDict):
    ActionName: str
    ActionArn: str
    Source: ActionSourceTypeDef
    ActionType: str
    Description: str
    Status: ActionStatusType
    Properties: dict[str, str]
    CreationTime: datetime
    CreatedBy: UserContextTypeDef
    LastModifiedTime: datetime
    LastModifiedBy: UserContextTypeDef
    MetadataProperties: MetadataPropertiesTypeDef
    LineageGroupArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeArtifactResponseTypeDef(TypedDict):
    ArtifactName: str
    ArtifactArn: str
    Source: ArtifactSourceOutputTypeDef
    ArtifactType: str
    Properties: dict[str, str]
    CreationTime: datetime
    CreatedBy: UserContextTypeDef
    LastModifiedTime: datetime
    LastModifiedBy: UserContextTypeDef
    MetadataProperties: MetadataPropertiesTypeDef
    LineageGroupArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeContextResponseTypeDef(TypedDict):
    ContextName: str
    ContextArn: str
    Source: ContextSourceTypeDef
    ContextType: str
    Description: str
    Properties: dict[str, str]
    CreationTime: datetime
    CreatedBy: UserContextTypeDef
    LastModifiedTime: datetime
    LastModifiedBy: UserContextTypeDef
    LineageGroupArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeExperimentResponseTypeDef(TypedDict):
    ExperimentName: str
    ExperimentArn: str
    DisplayName: str
    Source: ExperimentSourceTypeDef
    Description: str
    CreationTime: datetime
    CreatedBy: UserContextTypeDef
    LastModifiedTime: datetime
    LastModifiedBy: UserContextTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeLineageGroupResponseTypeDef(TypedDict):
    LineageGroupName: str
    LineageGroupArn: str
    DisplayName: str
    Description: str
    CreationTime: datetime
    CreatedBy: UserContextTypeDef
    LastModifiedTime: datetime
    LastModifiedBy: UserContextTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeMlflowAppResponseTypeDef(TypedDict):
    Arn: str
    Name: str
    ArtifactStoreUri: str
    MlflowVersion: str
    RoleArn: str
    Status: MlflowAppStatusType
    ModelRegistrationMode: ModelRegistrationModeType
    AccountDefaultStatus: AccountDefaultStatusType
    DefaultDomainIdList: list[str]
    CreationTime: datetime
    CreatedBy: UserContextTypeDef
    LastModifiedTime: datetime
    LastModifiedBy: UserContextTypeDef
    WeeklyMaintenanceWindowStart: str
    MaintenanceStatus: MaintenanceStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeMlflowTrackingServerResponseTypeDef(TypedDict):
    TrackingServerArn: str
    TrackingServerName: str
    ArtifactStoreUri: str
    TrackingServerSize: TrackingServerSizeType
    MlflowVersion: str
    RoleArn: str
    TrackingServerStatus: TrackingServerStatusType
    TrackingServerMaintenanceStatus: TrackingServerMaintenanceStatusType
    IsActive: IsTrackingServerActiveType
    TrackingServerUrl: str
    WeeklyMaintenanceWindowStart: str
    AutomaticModelRegistration: bool
    CreationTime: datetime
    CreatedBy: UserContextTypeDef
    LastModifiedTime: datetime
    LastModifiedBy: UserContextTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeModelCardResponseTypeDef(TypedDict):
    ModelCardArn: str
    ModelCardName: str
    ModelCardVersion: int
    Content: str
    ModelCardStatus: ModelCardStatusType
    SecurityConfig: ModelCardSecurityConfigTypeDef
    CreationTime: datetime
    CreatedBy: UserContextTypeDef
    LastModifiedTime: datetime
    LastModifiedBy: UserContextTypeDef
    ModelCardProcessingStatus: ModelCardProcessingStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeModelPackageGroupOutputTypeDef(TypedDict):
    ModelPackageGroupName: str
    ModelPackageGroupArn: str
    ModelPackageGroupDescription: str
    CreationTime: datetime
    CreatedBy: UserContextTypeDef
    ModelPackageGroupStatus: ModelPackageGroupStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class DescribePipelineResponseTypeDef(TypedDict):
    PipelineArn: str
    PipelineName: str
    PipelineDisplayName: str
    PipelineDefinition: str
    PipelineDescription: str
    RoleArn: str
    PipelineStatus: PipelineStatusType
    CreationTime: datetime
    LastModifiedTime: datetime
    LastRunTime: datetime
    CreatedBy: UserContextTypeDef
    LastModifiedBy: UserContextTypeDef
    ParallelismConfiguration: ParallelismConfigurationTypeDef
    PipelineVersionDisplayName: str
    PipelineVersionDescription: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTrialComponentResponseTypeDef(TypedDict):
    TrialComponentName: str
    TrialComponentArn: str
    DisplayName: str
    Source: TrialComponentSourceTypeDef
    Status: TrialComponentStatusTypeDef
    StartTime: datetime
    EndTime: datetime
    CreationTime: datetime
    CreatedBy: UserContextTypeDef
    LastModifiedTime: datetime
    LastModifiedBy: UserContextTypeDef
    Parameters: dict[str, TrialComponentParameterValueTypeDef]
    InputArtifacts: dict[str, TrialComponentArtifactTypeDef]
    OutputArtifacts: dict[str, TrialComponentArtifactTypeDef]
    MetadataProperties: MetadataPropertiesTypeDef
    Metrics: list[TrialComponentMetricSummaryTypeDef]
    LineageGroupArn: str
    Sources: list[TrialComponentSourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTrialResponseTypeDef(TypedDict):
    TrialName: str
    TrialArn: str
    DisplayName: str
    ExperimentName: str
    Source: TrialSourceTypeDef
    CreationTime: datetime
    CreatedBy: UserContextTypeDef
    LastModifiedTime: datetime
    LastModifiedBy: UserContextTypeDef
    MetadataProperties: MetadataPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ExperimentTypeDef(TypedDict):
    ExperimentName: NotRequired[str]
    ExperimentArn: NotRequired[str]
    DisplayName: NotRequired[str]
    Source: NotRequired[ExperimentSourceTypeDef]
    Description: NotRequired[str]
    CreationTime: NotRequired[datetime]
    CreatedBy: NotRequired[UserContextTypeDef]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedBy: NotRequired[UserContextTypeDef]
    Tags: NotRequired[list[TagTypeDef]]


class ModelCardTypeDef(TypedDict):
    ModelCardArn: NotRequired[str]
    ModelCardName: NotRequired[str]
    ModelCardVersion: NotRequired[int]
    Content: NotRequired[str]
    ModelCardStatus: NotRequired[ModelCardStatusType]
    SecurityConfig: NotRequired[ModelCardSecurityConfigTypeDef]
    CreationTime: NotRequired[datetime]
    CreatedBy: NotRequired[UserContextTypeDef]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedBy: NotRequired[UserContextTypeDef]
    Tags: NotRequired[list[TagTypeDef]]
    ModelId: NotRequired[str]
    RiskRating: NotRequired[str]
    ModelPackageGroupName: NotRequired[str]


class ModelDashboardModelCardTypeDef(TypedDict):
    ModelCardArn: NotRequired[str]
    ModelCardName: NotRequired[str]
    ModelCardVersion: NotRequired[int]
    ModelCardStatus: NotRequired[ModelCardStatusType]
    SecurityConfig: NotRequired[ModelCardSecurityConfigTypeDef]
    CreationTime: NotRequired[datetime]
    CreatedBy: NotRequired[UserContextTypeDef]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedBy: NotRequired[UserContextTypeDef]
    Tags: NotRequired[list[TagTypeDef]]
    ModelId: NotRequired[str]
    RiskRating: NotRequired[str]


class ModelPackageGroupTypeDef(TypedDict):
    ModelPackageGroupName: NotRequired[str]
    ModelPackageGroupArn: NotRequired[str]
    ModelPackageGroupDescription: NotRequired[str]
    CreationTime: NotRequired[datetime]
    CreatedBy: NotRequired[UserContextTypeDef]
    ModelPackageGroupStatus: NotRequired[ModelPackageGroupStatusType]
    Tags: NotRequired[list[TagTypeDef]]


class PipelineTypeDef(TypedDict):
    PipelineArn: NotRequired[str]
    PipelineName: NotRequired[str]
    PipelineDisplayName: NotRequired[str]
    PipelineDescription: NotRequired[str]
    RoleArn: NotRequired[str]
    PipelineStatus: NotRequired[PipelineStatusType]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    LastRunTime: NotRequired[datetime]
    CreatedBy: NotRequired[UserContextTypeDef]
    LastModifiedBy: NotRequired[UserContextTypeDef]
    ParallelismConfiguration: NotRequired[ParallelismConfigurationTypeDef]
    Tags: NotRequired[list[TagTypeDef]]


class PipelineVersionTypeDef(TypedDict):
    PipelineArn: NotRequired[str]
    PipelineVersionId: NotRequired[int]
    PipelineVersionDisplayName: NotRequired[str]
    PipelineVersionDescription: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    CreatedBy: NotRequired[UserContextTypeDef]
    LastModifiedBy: NotRequired[UserContextTypeDef]
    LastExecutedPipelineExecutionArn: NotRequired[str]
    LastExecutedPipelineExecutionDisplayName: NotRequired[str]
    LastExecutedPipelineExecutionStatus: NotRequired[PipelineExecutionStatusType]


class TrialComponentSimpleSummaryTypeDef(TypedDict):
    TrialComponentName: NotRequired[str]
    TrialComponentArn: NotRequired[str]
    TrialComponentSource: NotRequired[TrialComponentSourceTypeDef]
    CreationTime: NotRequired[datetime]
    CreatedBy: NotRequired[UserContextTypeDef]


class TrialComponentSummaryTypeDef(TypedDict):
    TrialComponentName: NotRequired[str]
    TrialComponentArn: NotRequired[str]
    DisplayName: NotRequired[str]
    TrialComponentSource: NotRequired[TrialComponentSourceTypeDef]
    Status: NotRequired[TrialComponentStatusTypeDef]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    CreationTime: NotRequired[datetime]
    CreatedBy: NotRequired[UserContextTypeDef]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedBy: NotRequired[UserContextTypeDef]


class WorkerAccessConfigurationTypeDef(TypedDict):
    S3Presign: NotRequired[S3PresignTypeDef]


class InferenceComponentDeploymentConfigOutputTypeDef(TypedDict):
    RollingUpdatePolicy: InferenceComponentRollingUpdatePolicyTypeDef
    AutoRollbackConfiguration: NotRequired[AutoRollbackConfigOutputTypeDef]


class InferenceComponentDeploymentConfigTypeDef(TypedDict):
    RollingUpdatePolicy: InferenceComponentRollingUpdatePolicyTypeDef
    AutoRollbackConfiguration: NotRequired[AutoRollbackConfigTypeDef]


class CreateInferenceComponentInputTypeDef(TypedDict):
    InferenceComponentName: str
    EndpointName: str
    Specification: InferenceComponentSpecificationTypeDef
    VariantName: NotRequired[str]
    RuntimeConfig: NotRequired[InferenceComponentRuntimeConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class ResourceConfigOutputTypeDef(TypedDict):
    InstanceType: NotRequired[TrainingInstanceTypeType]
    InstanceCount: NotRequired[int]
    VolumeSizeInGB: NotRequired[int]
    VolumeKmsKeyId: NotRequired[str]
    KeepAlivePeriodInSeconds: NotRequired[int]
    InstanceGroups: NotRequired[list[InstanceGroupTypeDef]]
    TrainingPlanArn: NotRequired[str]
    InstancePlacementConfig: NotRequired[InstancePlacementConfigOutputTypeDef]


InstancePlacementConfigUnionTypeDef = Union[
    InstancePlacementConfigTypeDef, InstancePlacementConfigOutputTypeDef
]
HyperParameterSpecificationOutputTypeDef = TypedDict(
    "HyperParameterSpecificationOutputTypeDef",
    {
        "Name": str,
        "Type": ParameterTypeType,
        "Description": NotRequired[str],
        "Range": NotRequired[ParameterRangeOutputTypeDef],
        "IsTunable": NotRequired[bool],
        "IsRequired": NotRequired[bool],
        "DefaultValue": NotRequired[str],
    },
)
HyperParameterSpecificationTypeDef = TypedDict(
    "HyperParameterSpecificationTypeDef",
    {
        "Name": str,
        "Type": ParameterTypeType,
        "Description": NotRequired[str],
        "Range": NotRequired[ParameterRangeTypeDef],
        "IsTunable": NotRequired[bool],
        "IsRequired": NotRequired[bool],
        "DefaultValue": NotRequired[str],
    },
)


class HyperParameterTuningJobConfigOutputTypeDef(TypedDict):
    Strategy: HyperParameterTuningJobStrategyTypeType
    ResourceLimits: ResourceLimitsTypeDef
    StrategyConfig: NotRequired[HyperParameterTuningJobStrategyConfigTypeDef]
    HyperParameterTuningJobObjective: NotRequired[HyperParameterTuningJobObjectiveTypeDef]
    ParameterRanges: NotRequired[ParameterRangesOutputTypeDef]
    TrainingJobEarlyStoppingType: NotRequired[TrainingJobEarlyStoppingTypeType]
    TuningJobCompletionCriteria: NotRequired[TuningJobCompletionCriteriaTypeDef]
    RandomSeed: NotRequired[int]


class AppImageConfigDetailsTypeDef(TypedDict):
    AppImageConfigArn: NotRequired[str]
    AppImageConfigName: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    KernelGatewayImageConfig: NotRequired[KernelGatewayImageConfigOutputTypeDef]
    JupyterLabAppImageConfig: NotRequired[JupyterLabAppImageConfigOutputTypeDef]
    CodeEditorAppImageConfig: NotRequired[CodeEditorAppImageConfigOutputTypeDef]


class DescribeAppImageConfigResponseTypeDef(TypedDict):
    AppImageConfigArn: str
    AppImageConfigName: str
    CreationTime: datetime
    LastModifiedTime: datetime
    KernelGatewayImageConfig: KernelGatewayImageConfigOutputTypeDef
    JupyterLabAppImageConfig: JupyterLabAppImageConfigOutputTypeDef
    CodeEditorAppImageConfig: CodeEditorAppImageConfigOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


KernelGatewayImageConfigUnionTypeDef = Union[
    KernelGatewayImageConfigTypeDef, KernelGatewayImageConfigOutputTypeDef
]


class ListLabelingJobsForWorkteamResponseTypeDef(TypedDict):
    LabelingJobSummaryList: list[LabelingJobForWorkteamSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class LabelingJobInputConfigOutputTypeDef(TypedDict):
    DataSource: LabelingJobDataSourceTypeDef
    DataAttributes: NotRequired[LabelingJobDataAttributesOutputTypeDef]


class LabelingJobInputConfigTypeDef(TypedDict):
    DataSource: LabelingJobDataSourceTypeDef
    DataAttributes: NotRequired[LabelingJobDataAttributesTypeDef]


class TargetTrackingScalingPolicyConfigurationTypeDef(TypedDict):
    MetricSpecification: NotRequired[MetricSpecificationTypeDef]
    TargetValue: NotRequired[float]


class DataSourceOutputTypeDef(TypedDict):
    S3DataSource: NotRequired[S3DataSourceOutputTypeDef]
    FileSystemDataSource: NotRequired[FileSystemDataSourceTypeDef]
    DatasetSource: NotRequired[DatasetSourceTypeDef]


S3DataSourceUnionTypeDef = Union[S3DataSourceTypeDef, S3DataSourceOutputTypeDef]


class AdditionalModelDataSourceTypeDef(TypedDict):
    ChannelName: str
    S3DataSource: S3ModelDataSourceTypeDef


class ModelDataSourceTypeDef(TypedDict):
    S3DataSource: NotRequired[S3ModelDataSourceTypeDef]


class MonitoringAlertSummaryTypeDef(TypedDict):
    MonitoringAlertName: str
    CreationTime: datetime
    LastModifiedTime: datetime
    AlertStatus: MonitoringAlertStatusType
    DatapointsToAlert: int
    EvaluationPeriod: int
    Actions: MonitoringAlertActionsTypeDef


class ModelVariantConfigSummaryTypeDef(TypedDict):
    ModelName: str
    VariantName: str
    InfrastructureConfig: ModelInfrastructureConfigTypeDef
    Status: ModelVariantStatusType


class ModelVariantConfigTypeDef(TypedDict):
    ModelName: str
    VariantName: str
    InfrastructureConfig: ModelInfrastructureConfigTypeDef


RecommendationJobStoppingConditionsUnionTypeDef = Union[
    RecommendationJobStoppingConditionsTypeDef, RecommendationJobStoppingConditionsOutputTypeDef
]


class ListModelMetadataRequestPaginateTypeDef(TypedDict):
    SearchExpression: NotRequired[ModelMetadataSearchExpressionTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListModelMetadataRequestTypeDef(TypedDict):
    SearchExpression: NotRequired[ModelMetadataSearchExpressionTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class OptimizationConfigOutputTypeDef(TypedDict):
    ModelQuantizationConfig: NotRequired[ModelQuantizationConfigOutputTypeDef]
    ModelCompilationConfig: NotRequired[ModelCompilationConfigOutputTypeDef]
    ModelShardingConfig: NotRequired[ModelShardingConfigOutputTypeDef]
    ModelSpeculativeDecodingConfig: NotRequired[ModelSpeculativeDecodingConfigTypeDef]


class OptimizationConfigTypeDef(TypedDict):
    ModelQuantizationConfig: NotRequired[ModelQuantizationConfigUnionTypeDef]
    ModelCompilationConfig: NotRequired[ModelCompilationConfigUnionTypeDef]
    ModelShardingConfig: NotRequired[ModelShardingConfigUnionTypeDef]
    ModelSpeculativeDecodingConfig: NotRequired[ModelSpeculativeDecodingConfigTypeDef]


BatchTransformInputOutputTypeDef = TypedDict(
    "BatchTransformInputOutputTypeDef",
    {
        "DataCapturedDestinationS3Uri": str,
        "DatasetFormat": MonitoringDatasetFormatOutputTypeDef,
        "LocalPath": str,
        "S3InputMode": NotRequired[ProcessingS3InputModeType],
        "S3DataDistributionType": NotRequired[ProcessingS3DataDistributionTypeType],
        "FeaturesAttribute": NotRequired[str],
        "InferenceAttribute": NotRequired[str],
        "ProbabilityAttribute": NotRequired[str],
        "ProbabilityThresholdAttribute": NotRequired[float],
        "StartTimeOffset": NotRequired[str],
        "EndTimeOffset": NotRequired[str],
        "ExcludeFeaturesAttribute": NotRequired[str],
    },
)
BatchTransformInputTypeDef = TypedDict(
    "BatchTransformInputTypeDef",
    {
        "DataCapturedDestinationS3Uri": str,
        "DatasetFormat": MonitoringDatasetFormatTypeDef,
        "LocalPath": str,
        "S3InputMode": NotRequired[ProcessingS3InputModeType],
        "S3DataDistributionType": NotRequired[ProcessingS3DataDistributionTypeType],
        "FeaturesAttribute": NotRequired[str],
        "InferenceAttribute": NotRequired[str],
        "ProbabilityAttribute": NotRequired[str],
        "ProbabilityThresholdAttribute": NotRequired[float],
        "StartTimeOffset": NotRequired[str],
        "EndTimeOffset": NotRequired[str],
        "ExcludeFeaturesAttribute": NotRequired[str],
    },
)


class MonitoringOutputConfigOutputTypeDef(TypedDict):
    MonitoringOutputs: list[MonitoringOutputTypeDef]
    KmsKeyId: NotRequired[str]


class MonitoringOutputConfigTypeDef(TypedDict):
    MonitoringOutputs: Sequence[MonitoringOutputTypeDef]
    KmsKeyId: NotRequired[str]


class MemberDefinitionTypeDef(TypedDict):
    CognitoMemberDefinition: NotRequired[CognitoMemberDefinitionTypeDef]
    OidcMemberDefinition: NotRequired[OidcMemberDefinitionUnionTypeDef]


class OptimizationJobModelSourceTypeDef(TypedDict):
    S3: NotRequired[OptimizationJobModelSourceS3TypeDef]
    SageMakerModel: NotRequired[OptimizationSageMakerModelTypeDef]


class CreateCompilationJobRequestTypeDef(TypedDict):
    CompilationJobName: str
    RoleArn: str
    OutputConfig: OutputConfigTypeDef
    StoppingCondition: StoppingConditionTypeDef
    ModelPackageVersionArn: NotRequired[str]
    InputConfig: NotRequired[InputConfigTypeDef]
    VpcConfig: NotRequired[NeoVpcConfigUnionTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class DescribeCompilationJobResponseTypeDef(TypedDict):
    CompilationJobName: str
    CompilationJobArn: str
    CompilationJobStatus: CompilationJobStatusType
    CompilationStartTime: datetime
    CompilationEndTime: datetime
    StoppingCondition: StoppingConditionTypeDef
    InferenceImage: str
    ModelPackageVersionArn: str
    CreationTime: datetime
    LastModifiedTime: datetime
    FailureReason: str
    ModelArtifacts: ModelArtifactsTypeDef
    ModelDigests: ModelDigestsTypeDef
    RoleArn: str
    InputConfig: InputConfigTypeDef
    OutputConfig: OutputConfigTypeDef
    VpcConfig: NeoVpcConfigOutputTypeDef
    DerivedInformation: DerivedInformationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


DescribePartnerAppResponseTypeDef = TypedDict(
    "DescribePartnerAppResponseTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Type": PartnerAppTypeType,
        "Status": PartnerAppStatusType,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "ExecutionRoleArn": str,
        "KmsKeyId": str,
        "BaseUrl": str,
        "MaintenanceConfig": PartnerAppMaintenanceConfigTypeDef,
        "Tier": str,
        "Version": str,
        "ApplicationConfig": PartnerAppConfigOutputTypeDef,
        "AuthType": Literal["IAM"],
        "EnableIamSessionBasedIdentity": bool,
        "Error": ErrorInfoTypeDef,
        "EnableAutoMinorVersionUpgrade": bool,
        "CurrentVersionEolDate": datetime,
        "AvailableUpgrade": AvailableUpgradeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PartnerAppConfigUnionTypeDef = Union[PartnerAppConfigTypeDef, PartnerAppConfigOutputTypeDef]


class PendingDeploymentSummaryTypeDef(TypedDict):
    EndpointConfigName: str
    ProductionVariants: NotRequired[list[PendingProductionVariantSummaryTypeDef]]
    StartTime: NotRequired[datetime]
    ShadowProductionVariants: NotRequired[list[PendingProductionVariantSummaryTypeDef]]


class DescribeClusterSchedulerConfigResponseTypeDef(TypedDict):
    ClusterSchedulerConfigArn: str
    ClusterSchedulerConfigId: str
    Name: str
    ClusterSchedulerConfigVersion: int
    Status: SchedulerResourceStatusType
    FailureReason: str
    StatusDetails: dict[SchedulerConfigComponentType, SchedulerResourceStatusType]
    ClusterArn: str
    SchedulerConfig: SchedulerConfigOutputTypeDef
    Description: str
    CreationTime: datetime
    CreatedBy: UserContextTypeDef
    LastModifiedTime: datetime
    LastModifiedBy: UserContextTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


SchedulerConfigUnionTypeDef = Union[SchedulerConfigTypeDef, SchedulerConfigOutputTypeDef]


class ProcessingOutputConfigOutputTypeDef(TypedDict):
    Outputs: list[ProcessingOutputTypeDef]
    KmsKeyId: NotRequired[str]


class ProcessingOutputConfigTypeDef(TypedDict):
    Outputs: Sequence[ProcessingOutputTypeDef]
    KmsKeyId: NotRequired[str]


class UpdateTrainingJobRequestTypeDef(TypedDict):
    TrainingJobName: str
    ProfilerConfig: NotRequired[ProfilerConfigForUpdateTypeDef]
    ProfilerRuleConfigurations: NotRequired[Sequence[ProfilerRuleConfigurationUnionTypeDef]]
    ResourceConfig: NotRequired[ResourceConfigForUpdateTypeDef]
    RemoteDebugConfig: NotRequired[RemoteDebugConfigForUpdateTypeDef]


class GetSearchSuggestionsRequestTypeDef(TypedDict):
    Resource: ResourceTypeType
    SuggestionQuery: NotRequired[SuggestionQueryTypeDef]


ServiceCatalogProvisioningDetailsUnionTypeDef = Union[
    ServiceCatalogProvisioningDetailsTypeDef, ServiceCatalogProvisioningDetailsOutputTypeDef
]


class HumanLoopConfigOutputTypeDef(TypedDict):
    WorkteamArn: str
    HumanTaskUiArn: str
    TaskTitle: str
    TaskDescription: str
    TaskCount: int
    TaskAvailabilityLifetimeInSeconds: NotRequired[int]
    TaskTimeLimitInSeconds: NotRequired[int]
    TaskKeywords: NotRequired[list[str]]
    PublicWorkforceTaskPrice: NotRequired[PublicWorkforceTaskPriceTypeDef]


class HumanLoopConfigTypeDef(TypedDict):
    WorkteamArn: str
    HumanTaskUiArn: str
    TaskTitle: str
    TaskDescription: str
    TaskCount: int
    TaskAvailabilityLifetimeInSeconds: NotRequired[int]
    TaskTimeLimitInSeconds: NotRequired[int]
    TaskKeywords: NotRequired[Sequence[str]]
    PublicWorkforceTaskPrice: NotRequired[PublicWorkforceTaskPriceTypeDef]


class HumanTaskConfigOutputTypeDef(TypedDict):
    WorkteamArn: str
    UiConfig: UiConfigTypeDef
    TaskTitle: str
    TaskDescription: str
    NumberOfHumanWorkersPerDataObject: int
    TaskTimeLimitInSeconds: int
    PreHumanTaskLambdaArn: NotRequired[str]
    TaskKeywords: NotRequired[list[str]]
    TaskAvailabilityLifetimeInSeconds: NotRequired[int]
    MaxConcurrentTaskCount: NotRequired[int]
    AnnotationConsolidationConfig: NotRequired[AnnotationConsolidationConfigTypeDef]
    PublicWorkforceTaskPrice: NotRequired[PublicWorkforceTaskPriceTypeDef]


class HumanTaskConfigTypeDef(TypedDict):
    WorkteamArn: str
    UiConfig: UiConfigTypeDef
    TaskTitle: str
    TaskDescription: str
    NumberOfHumanWorkersPerDataObject: int
    TaskTimeLimitInSeconds: int
    PreHumanTaskLambdaArn: NotRequired[str]
    TaskKeywords: NotRequired[Sequence[str]]
    TaskAvailabilityLifetimeInSeconds: NotRequired[int]
    MaxConcurrentTaskCount: NotRequired[int]
    AnnotationConsolidationConfig: NotRequired[AnnotationConsolidationConfigTypeDef]
    PublicWorkforceTaskPrice: NotRequired[PublicWorkforceTaskPriceTypeDef]


class SearchTrainingPlanOfferingsResponseTypeDef(TypedDict):
    TrainingPlanOfferings: list[TrainingPlanOfferingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribePipelineExecutionResponseTypeDef(TypedDict):
    PipelineArn: str
    PipelineExecutionArn: str
    PipelineExecutionDisplayName: str
    PipelineExecutionStatus: PipelineExecutionStatusType
    PipelineExecutionDescription: str
    PipelineExperimentConfig: PipelineExperimentConfigTypeDef
    FailureReason: str
    CreationTime: datetime
    LastModifiedTime: datetime
    CreatedBy: UserContextTypeDef
    LastModifiedBy: UserContextTypeDef
    ParallelismConfiguration: ParallelismConfigurationTypeDef
    SelectiveExecutionConfig: SelectiveExecutionConfigOutputTypeDef
    PipelineVersionId: int
    MLflowConfig: MLflowConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PipelineExecutionTypeDef(TypedDict):
    PipelineArn: NotRequired[str]
    PipelineExecutionArn: NotRequired[str]
    PipelineExecutionDisplayName: NotRequired[str]
    PipelineExecutionStatus: NotRequired[PipelineExecutionStatusType]
    PipelineExecutionDescription: NotRequired[str]
    PipelineExperimentConfig: NotRequired[PipelineExperimentConfigTypeDef]
    FailureReason: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    CreatedBy: NotRequired[UserContextTypeDef]
    LastModifiedBy: NotRequired[UserContextTypeDef]
    ParallelismConfiguration: NotRequired[ParallelismConfigurationTypeDef]
    SelectiveExecutionConfig: NotRequired[SelectiveExecutionConfigOutputTypeDef]
    PipelineParameters: NotRequired[list[ParameterTypeDef]]
    PipelineVersionId: NotRequired[int]
    PipelineVersionDisplayName: NotRequired[str]


SelectiveExecutionConfigUnionTypeDef = Union[
    SelectiveExecutionConfigTypeDef, SelectiveExecutionConfigOutputTypeDef
]
ShadowModeConfigUnionTypeDef = Union[ShadowModeConfigTypeDef, ShadowModeConfigOutputTypeDef]


class CreateWorkforceRequestTypeDef(TypedDict):
    WorkforceName: str
    CognitoConfig: NotRequired[CognitoConfigTypeDef]
    OidcConfig: NotRequired[OidcConfigTypeDef]
    SourceIpConfig: NotRequired[SourceIpConfigUnionTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    WorkforceVpcConfig: NotRequired[WorkforceVpcConfigRequestTypeDef]
    IpAddressType: NotRequired[WorkforceIpAddressTypeType]


class UpdateWorkforceRequestTypeDef(TypedDict):
    WorkforceName: str
    SourceIpConfig: NotRequired[SourceIpConfigUnionTypeDef]
    OidcConfig: NotRequired[OidcConfigTypeDef]
    WorkforceVpcConfig: NotRequired[WorkforceVpcConfigRequestTypeDef]
    IpAddressType: NotRequired[WorkforceIpAddressTypeType]


class SpaceCodeEditorAppSettingsTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    AppLifecycleManagement: NotRequired[SpaceAppLifecycleManagementTypeDef]


class SpaceJupyterLabAppSettingsOutputTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    CodeRepositories: NotRequired[list[CodeRepositoryTypeDef]]
    AppLifecycleManagement: NotRequired[SpaceAppLifecycleManagementTypeDef]


class SpaceJupyterLabAppSettingsTypeDef(TypedDict):
    DefaultResourceSpec: NotRequired[ResourceSpecTypeDef]
    CodeRepositories: NotRequired[Sequence[CodeRepositoryTypeDef]]
    AppLifecycleManagement: NotRequired[SpaceAppLifecycleManagementTypeDef]


class AlgorithmSpecificationOutputTypeDef(TypedDict):
    TrainingInputMode: TrainingInputModeType
    TrainingImage: NotRequired[str]
    AlgorithmName: NotRequired[str]
    MetricDefinitions: NotRequired[list[MetricDefinitionTypeDef]]
    EnableSageMakerMetricsTimeSeries: NotRequired[bool]
    ContainerEntrypoint: NotRequired[list[str]]
    ContainerArguments: NotRequired[list[str]]
    TrainingImageConfig: NotRequired[TrainingImageConfigTypeDef]


class AlgorithmSpecificationTypeDef(TypedDict):
    TrainingInputMode: TrainingInputModeType
    TrainingImage: NotRequired[str]
    AlgorithmName: NotRequired[str]
    MetricDefinitions: NotRequired[Sequence[MetricDefinitionTypeDef]]
    EnableSageMakerMetricsTimeSeries: NotRequired[bool]
    ContainerEntrypoint: NotRequired[Sequence[str]]
    ContainerArguments: NotRequired[Sequence[str]]
    TrainingImageConfig: NotRequired[TrainingImageConfigTypeDef]


class TransformInputTypeDef(TypedDict):
    DataSource: TransformDataSourceTypeDef
    ContentType: NotRequired[str]
    CompressionType: NotRequired[CompressionTypeType]
    SplitType: NotRequired[SplitTypeType]


class DescribeWorkforceResponseTypeDef(TypedDict):
    Workforce: WorkforceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListWorkforcesResponseTypeDef(TypedDict):
    Workforces: list[WorkforceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateWorkforceResponseTypeDef(TypedDict):
    Workforce: WorkforceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ComputeQuotaConfigOutputTypeDef(TypedDict):
    ComputeQuotaResources: NotRequired[list[ComputeQuotaResourceConfigTypeDef]]
    ResourceSharingConfig: NotRequired[ResourceSharingConfigOutputTypeDef]
    PreemptTeamTasks: NotRequired[PreemptTeamTasksType]


class ComputeQuotaConfigTypeDef(TypedDict):
    ComputeQuotaResources: NotRequired[Sequence[ComputeQuotaResourceConfigTypeDef]]
    ResourceSharingConfig: NotRequired[ResourceSharingConfigTypeDef]
    PreemptTeamTasks: NotRequired[PreemptTeamTasksType]


DomainSettingsUnionTypeDef = Union[DomainSettingsTypeDef, DomainSettingsOutputTypeDef]


class DefaultSpaceSettingsOutputTypeDef(TypedDict):
    ExecutionRole: NotRequired[str]
    SecurityGroups: NotRequired[list[str]]
    JupyterServerAppSettings: NotRequired[JupyterServerAppSettingsOutputTypeDef]
    KernelGatewayAppSettings: NotRequired[KernelGatewayAppSettingsOutputTypeDef]
    JupyterLabAppSettings: NotRequired[JupyterLabAppSettingsOutputTypeDef]
    SpaceStorageSettings: NotRequired[DefaultSpaceStorageSettingsTypeDef]
    CustomPosixUserConfig: NotRequired[CustomPosixUserConfigTypeDef]
    CustomFileSystemConfigs: NotRequired[list[CustomFileSystemConfigTypeDef]]


class UserSettingsOutputTypeDef(TypedDict):
    ExecutionRole: NotRequired[str]
    SecurityGroups: NotRequired[list[str]]
    SharingSettings: NotRequired[SharingSettingsTypeDef]
    JupyterServerAppSettings: NotRequired[JupyterServerAppSettingsOutputTypeDef]
    KernelGatewayAppSettings: NotRequired[KernelGatewayAppSettingsOutputTypeDef]
    TensorBoardAppSettings: NotRequired[TensorBoardAppSettingsTypeDef]
    RStudioServerProAppSettings: NotRequired[RStudioServerProAppSettingsTypeDef]
    RSessionAppSettings: NotRequired[RSessionAppSettingsOutputTypeDef]
    CanvasAppSettings: NotRequired[CanvasAppSettingsOutputTypeDef]
    CodeEditorAppSettings: NotRequired[CodeEditorAppSettingsOutputTypeDef]
    JupyterLabAppSettings: NotRequired[JupyterLabAppSettingsOutputTypeDef]
    SpaceStorageSettings: NotRequired[DefaultSpaceStorageSettingsTypeDef]
    DefaultLandingUri: NotRequired[str]
    StudioWebPortal: NotRequired[StudioWebPortalType]
    CustomPosixUserConfig: NotRequired[CustomPosixUserConfigTypeDef]
    CustomFileSystemConfigs: NotRequired[list[CustomFileSystemConfigTypeDef]]
    StudioWebPortalSettings: NotRequired[StudioWebPortalSettingsOutputTypeDef]
    AutoMountHomeEFS: NotRequired[AutoMountHomeEFSType]


class DefaultSpaceSettingsTypeDef(TypedDict):
    ExecutionRole: NotRequired[str]
    SecurityGroups: NotRequired[Sequence[str]]
    JupyterServerAppSettings: NotRequired[JupyterServerAppSettingsTypeDef]
    KernelGatewayAppSettings: NotRequired[KernelGatewayAppSettingsTypeDef]
    JupyterLabAppSettings: NotRequired[JupyterLabAppSettingsTypeDef]
    SpaceStorageSettings: NotRequired[DefaultSpaceStorageSettingsTypeDef]
    CustomPosixUserConfig: NotRequired[CustomPosixUserConfigTypeDef]
    CustomFileSystemConfigs: NotRequired[Sequence[CustomFileSystemConfigTypeDef]]


class UserSettingsTypeDef(TypedDict):
    ExecutionRole: NotRequired[str]
    SecurityGroups: NotRequired[Sequence[str]]
    SharingSettings: NotRequired[SharingSettingsTypeDef]
    JupyterServerAppSettings: NotRequired[JupyterServerAppSettingsTypeDef]
    KernelGatewayAppSettings: NotRequired[KernelGatewayAppSettingsTypeDef]
    TensorBoardAppSettings: NotRequired[TensorBoardAppSettingsTypeDef]
    RStudioServerProAppSettings: NotRequired[RStudioServerProAppSettingsTypeDef]
    RSessionAppSettings: NotRequired[RSessionAppSettingsTypeDef]
    CanvasAppSettings: NotRequired[CanvasAppSettingsTypeDef]
    CodeEditorAppSettings: NotRequired[CodeEditorAppSettingsTypeDef]
    JupyterLabAppSettings: NotRequired[JupyterLabAppSettingsTypeDef]
    SpaceStorageSettings: NotRequired[DefaultSpaceStorageSettingsTypeDef]
    DefaultLandingUri: NotRequired[str]
    StudioWebPortal: NotRequired[StudioWebPortalType]
    CustomPosixUserConfig: NotRequired[CustomPosixUserConfigTypeDef]
    CustomFileSystemConfigs: NotRequired[Sequence[CustomFileSystemConfigTypeDef]]
    StudioWebPortalSettings: NotRequired[StudioWebPortalSettingsTypeDef]
    AutoMountHomeEFS: NotRequired[AutoMountHomeEFSType]


class ListArtifactsResponseTypeDef(TypedDict):
    ArtifactSummaries: list[ArtifactSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateArtifactRequestTypeDef(TypedDict):
    Source: ArtifactSourceUnionTypeDef
    ArtifactType: str
    ArtifactName: NotRequired[str]
    Properties: NotRequired[Mapping[str, str]]
    MetadataProperties: NotRequired[MetadataPropertiesTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class DeleteArtifactRequestTypeDef(TypedDict):
    ArtifactArn: NotRequired[str]
    Source: NotRequired[ArtifactSourceUnionTypeDef]


AsyncInferenceConfigUnionTypeDef = Union[
    AsyncInferenceConfigTypeDef, AsyncInferenceConfigOutputTypeDef
]


class AutoMLProblemTypeConfigOutputTypeDef(TypedDict):
    ImageClassificationJobConfig: NotRequired[ImageClassificationJobConfigTypeDef]
    TextClassificationJobConfig: NotRequired[TextClassificationJobConfigTypeDef]
    TimeSeriesForecastingJobConfig: NotRequired[TimeSeriesForecastingJobConfigOutputTypeDef]
    TabularJobConfig: NotRequired[TabularJobConfigOutputTypeDef]
    TextGenerationJobConfig: NotRequired[TextGenerationJobConfigOutputTypeDef]


class AutoMLProblemTypeConfigTypeDef(TypedDict):
    ImageClassificationJobConfig: NotRequired[ImageClassificationJobConfigTypeDef]
    TextClassificationJobConfig: NotRequired[TextClassificationJobConfigTypeDef]
    TimeSeriesForecastingJobConfig: NotRequired[TimeSeriesForecastingJobConfigTypeDef]
    TabularJobConfig: NotRequired[TabularJobConfigTypeDef]
    TextGenerationJobConfig: NotRequired[TextGenerationJobConfigTypeDef]


AutoMLJobConfigUnionTypeDef = Union[AutoMLJobConfigTypeDef, AutoMLJobConfigOutputTypeDef]
LabelingJobAlgorithmsConfigUnionTypeDef = Union[
    LabelingJobAlgorithmsConfigTypeDef, LabelingJobAlgorithmsConfigOutputTypeDef
]


class PipelineExecutionStepTypeDef(TypedDict):
    StepName: NotRequired[str]
    StepDisplayName: NotRequired[str]
    StepDescription: NotRequired[str]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    StepStatus: NotRequired[StepStatusType]
    CacheHitResult: NotRequired[CacheHitResultTypeDef]
    FailureReason: NotRequired[str]
    Metadata: NotRequired[PipelineExecutionStepMetadataTypeDef]
    AttemptCount: NotRequired[int]
    SelectiveExecutionResult: NotRequired[SelectiveExecutionResultTypeDef]


class DescribeAutoMLJobResponseTypeDef(TypedDict):
    AutoMLJobName: str
    AutoMLJobArn: str
    InputDataConfig: list[AutoMLChannelTypeDef]
    OutputDataConfig: AutoMLOutputDataConfigTypeDef
    RoleArn: str
    AutoMLJobObjective: AutoMLJobObjectiveTypeDef
    ProblemType: ProblemTypeType
    AutoMLJobConfig: AutoMLJobConfigOutputTypeDef
    CreationTime: datetime
    EndTime: datetime
    LastModifiedTime: datetime
    FailureReason: str
    PartialFailureReasons: list[AutoMLPartialFailureReasonTypeDef]
    BestCandidate: AutoMLCandidateTypeDef
    AutoMLJobStatus: AutoMLJobStatusType
    AutoMLJobSecondaryStatus: AutoMLJobSecondaryStatusType
    GenerateCandidateDefinitionsOnly: bool
    AutoMLJobArtifacts: AutoMLJobArtifactsTypeDef
    ResolvedAttributes: ResolvedAttributesTypeDef
    ModelDeployConfig: ModelDeployConfigTypeDef
    ModelDeployResult: ModelDeployResultTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListCandidatesForAutoMLJobResponseTypeDef(TypedDict):
    Candidates: list[AutoMLCandidateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class EventDetailsTypeDef(TypedDict):
    EventMetadata: NotRequired[EventMetadataTypeDef]


class ScheduledUpdateConfigOutputTypeDef(TypedDict):
    ScheduleExpression: str
    DeploymentConfig: NotRequired[DeploymentConfigurationOutputTypeDef]


DeploymentConfigurationUnionTypeDef = Union[
    DeploymentConfigurationTypeDef, DeploymentConfigurationOutputTypeDef
]


class DeploymentConfigOutputTypeDef(TypedDict):
    BlueGreenUpdatePolicy: NotRequired[BlueGreenUpdatePolicyTypeDef]
    RollingUpdatePolicy: NotRequired[RollingUpdatePolicyTypeDef]
    AutoRollbackConfiguration: NotRequired[AutoRollbackConfigOutputTypeDef]


class DeploymentConfigTypeDef(TypedDict):
    BlueGreenUpdatePolicy: NotRequired[BlueGreenUpdatePolicyTypeDef]
    RollingUpdatePolicy: NotRequired[RollingUpdatePolicyTypeDef]
    AutoRollbackConfiguration: NotRequired[AutoRollbackConfigTypeDef]


class RecommendationJobInputConfigOutputTypeDef(TypedDict):
    ModelPackageVersionArn: NotRequired[str]
    ModelName: NotRequired[str]
    JobDurationInSeconds: NotRequired[int]
    TrafficPattern: NotRequired[TrafficPatternOutputTypeDef]
    ResourceLimit: NotRequired[RecommendationJobResourceLimitTypeDef]
    EndpointConfigurations: NotRequired[list[EndpointInputConfigurationOutputTypeDef]]
    VolumeKmsKeyId: NotRequired[str]
    ContainerConfig: NotRequired[RecommendationJobContainerConfigOutputTypeDef]
    Endpoints: NotRequired[list[EndpointInfoTypeDef]]
    VpcConfig: NotRequired[RecommendationJobVpcConfigOutputTypeDef]


class HyperParameterTuningJobConfigTypeDef(TypedDict):
    Strategy: HyperParameterTuningJobStrategyTypeType
    ResourceLimits: ResourceLimitsTypeDef
    StrategyConfig: NotRequired[HyperParameterTuningJobStrategyConfigTypeDef]
    HyperParameterTuningJobObjective: NotRequired[HyperParameterTuningJobObjectiveTypeDef]
    ParameterRanges: NotRequired[ParameterRangesTypeDef]
    TrainingJobEarlyStoppingType: NotRequired[TrainingJobEarlyStoppingTypeType]
    TuningJobCompletionCriteria: NotRequired[TuningJobCompletionCriteriaTypeDef]
    RandomSeed: NotRequired[int]


ParameterRangesUnionTypeDef = Union[ParameterRangesTypeDef, ParameterRangesOutputTypeDef]


class RecommendationJobInputConfigTypeDef(TypedDict):
    ModelPackageVersionArn: NotRequired[str]
    ModelName: NotRequired[str]
    JobDurationInSeconds: NotRequired[int]
    TrafficPattern: NotRequired[TrafficPatternTypeDef]
    ResourceLimit: NotRequired[RecommendationJobResourceLimitTypeDef]
    EndpointConfigurations: NotRequired[Sequence[EndpointInputConfigurationTypeDef]]
    VolumeKmsKeyId: NotRequired[str]
    ContainerConfig: NotRequired[RecommendationJobContainerConfigTypeDef]
    Endpoints: NotRequired[Sequence[EndpointInfoTypeDef]]
    VpcConfig: NotRequired[RecommendationJobVpcConfigTypeDef]


class DescribeProjectOutputTypeDef(TypedDict):
    ProjectArn: str
    ProjectName: str
    ProjectId: str
    ProjectDescription: str
    ServiceCatalogProvisioningDetails: ServiceCatalogProvisioningDetailsOutputTypeDef
    ServiceCatalogProvisionedProductDetails: ServiceCatalogProvisionedProductDetailsTypeDef
    ProjectStatus: ProjectStatusType
    TemplateProviderDetails: list[TemplateProviderDetailTypeDef]
    CreatedBy: UserContextTypeDef
    CreationTime: datetime
    LastModifiedTime: datetime
    LastModifiedBy: UserContextTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ProjectTypeDef(TypedDict):
    ProjectArn: NotRequired[str]
    ProjectName: NotRequired[str]
    ProjectId: NotRequired[str]
    ProjectDescription: NotRequired[str]
    ServiceCatalogProvisioningDetails: NotRequired[ServiceCatalogProvisioningDetailsOutputTypeDef]
    ServiceCatalogProvisionedProductDetails: NotRequired[
        ServiceCatalogProvisionedProductDetailsTypeDef
    ]
    ProjectStatus: NotRequired[ProjectStatusType]
    CreatedBy: NotRequired[UserContextTypeDef]
    CreationTime: NotRequired[datetime]
    TemplateProviderDetails: NotRequired[list[TemplateProviderDetailTypeDef]]
    Tags: NotRequired[list[TagTypeDef]]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedBy: NotRequired[UserContextTypeDef]


class UpdateProjectInputTypeDef(TypedDict):
    ProjectName: str
    ProjectDescription: NotRequired[str]
    ServiceCatalogProvisioningUpdateDetails: NotRequired[
        ServiceCatalogProvisioningUpdateDetailsTypeDef
    ]
    Tags: NotRequired[Sequence[TagTypeDef]]
    TemplateProvidersToUpdate: NotRequired[Sequence[UpdateTemplateProviderTypeDef]]


class ExplainerConfigOutputTypeDef(TypedDict):
    ClarifyExplainerConfig: NotRequired[ClarifyExplainerConfigOutputTypeDef]


class ExplainerConfigTypeDef(TypedDict):
    ClarifyExplainerConfig: NotRequired[ClarifyExplainerConfigTypeDef]


class DescribeClusterNodeResponseTypeDef(TypedDict):
    NodeDetails: ClusterNodeDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFeatureGroupRequestTypeDef(TypedDict):
    FeatureGroupName: str
    RecordIdentifierFeatureName: str
    EventTimeFeatureName: str
    FeatureDefinitions: Sequence[FeatureDefinitionTypeDef]
    OnlineStoreConfig: NotRequired[OnlineStoreConfigTypeDef]
    OfflineStoreConfig: NotRequired[OfflineStoreConfigTypeDef]
    ThroughputConfig: NotRequired[ThroughputConfigTypeDef]
    RoleArn: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class DescribeFeatureGroupResponseTypeDef(TypedDict):
    FeatureGroupArn: str
    FeatureGroupName: str
    RecordIdentifierFeatureName: str
    EventTimeFeatureName: str
    FeatureDefinitions: list[FeatureDefinitionTypeDef]
    CreationTime: datetime
    LastModifiedTime: datetime
    OnlineStoreConfig: OnlineStoreConfigTypeDef
    OfflineStoreConfig: OfflineStoreConfigTypeDef
    ThroughputConfig: ThroughputConfigDescriptionTypeDef
    RoleArn: str
    FeatureGroupStatus: FeatureGroupStatusType
    OfflineStoreStatus: OfflineStoreStatusTypeDef
    LastUpdateStatus: LastUpdateStatusTypeDef
    FailureReason: str
    Description: str
    NextToken: str
    OnlineStoreTotalSizeBytes: int
    ResponseMetadata: ResponseMetadataTypeDef


class FeatureGroupTypeDef(TypedDict):
    FeatureGroupArn: NotRequired[str]
    FeatureGroupName: NotRequired[str]
    RecordIdentifierFeatureName: NotRequired[str]
    EventTimeFeatureName: NotRequired[str]
    FeatureDefinitions: NotRequired[list[FeatureDefinitionTypeDef]]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    OnlineStoreConfig: NotRequired[OnlineStoreConfigTypeDef]
    OfflineStoreConfig: NotRequired[OfflineStoreConfigTypeDef]
    RoleArn: NotRequired[str]
    FeatureGroupStatus: NotRequired[FeatureGroupStatusType]
    OfflineStoreStatus: NotRequired[OfflineStoreStatusTypeDef]
    LastUpdateStatus: NotRequired[LastUpdateStatusTypeDef]
    FailureReason: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


class UpdateFeatureGroupRequestTypeDef(TypedDict):
    FeatureGroupName: str
    FeatureAdditions: NotRequired[Sequence[FeatureDefinitionTypeDef]]
    OnlineStoreConfig: NotRequired[OnlineStoreConfigUpdateTypeDef]
    ThroughputConfig: NotRequired[ThroughputConfigUpdateTypeDef]


class CreateEdgeDeploymentPlanRequestTypeDef(TypedDict):
    EdgeDeploymentPlanName: str
    ModelConfigs: Sequence[EdgeDeploymentModelConfigTypeDef]
    DeviceFleetName: str
    Stages: NotRequired[Sequence[DeploymentStageTypeDef]]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateEdgeDeploymentStageRequestTypeDef(TypedDict):
    EdgeDeploymentPlanName: str
    Stages: Sequence[DeploymentStageTypeDef]


class SpaceDetailsTypeDef(TypedDict):
    DomainId: NotRequired[str]
    SpaceName: NotRequired[str]
    Status: NotRequired[SpaceStatusType]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    SpaceSettingsSummary: NotRequired[SpaceSettingsSummaryTypeDef]
    SpaceSharingSettingsSummary: NotRequired[SpaceSharingSettingsSummaryTypeDef]
    OwnershipSettingsSummary: NotRequired[OwnershipSettingsSummaryTypeDef]
    SpaceDisplayName: NotRequired[str]


class InferenceRecommendationsJobStepTypeDef(TypedDict):
    StepType: Literal["BENCHMARK"]
    JobName: str
    Status: RecommendationJobStatusType
    InferenceBenchmark: NotRequired[RecommendationJobInferenceBenchmarkTypeDef]


class SearchRequestPaginateTypeDef(TypedDict):
    Resource: ResourceTypeType
    SearchExpression: NotRequired[SearchExpressionPaginatorTypeDef]
    SortBy: NotRequired[str]
    SortOrder: NotRequired[SearchSortOrderType]
    CrossAccountFilterOption: NotRequired[CrossAccountFilterOptionType]
    VisibilityConditions: NotRequired[Sequence[VisibilityConditionsTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchRequestTypeDef(TypedDict):
    Resource: ResourceTypeType
    SearchExpression: NotRequired[SearchExpressionTypeDef]
    SortBy: NotRequired[str]
    SortOrder: NotRequired[SearchSortOrderType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    CrossAccountFilterOption: NotRequired[CrossAccountFilterOptionType]
    VisibilityConditions: NotRequired[Sequence[VisibilityConditionsTypeDef]]


class ListAssociationsResponseTypeDef(TypedDict):
    AssociationSummaries: list[AssociationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class TrialTypeDef(TypedDict):
    TrialName: NotRequired[str]
    TrialArn: NotRequired[str]
    DisplayName: NotRequired[str]
    ExperimentName: NotRequired[str]
    Source: NotRequired[TrialSourceTypeDef]
    CreationTime: NotRequired[datetime]
    CreatedBy: NotRequired[UserContextTypeDef]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedBy: NotRequired[UserContextTypeDef]
    MetadataProperties: NotRequired[MetadataPropertiesTypeDef]
    Tags: NotRequired[list[TagTypeDef]]
    TrialComponentSummaries: NotRequired[list[TrialComponentSimpleSummaryTypeDef]]


class ListTrialComponentsResponseTypeDef(TypedDict):
    TrialComponentSummaries: list[TrialComponentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class WorkteamTypeDef(TypedDict):
    WorkteamName: str
    MemberDefinitions: list[MemberDefinitionOutputTypeDef]
    WorkteamArn: str
    Description: str
    WorkforceArn: NotRequired[str]
    ProductListingIds: NotRequired[list[str]]
    SubDomain: NotRequired[str]
    CreateDate: NotRequired[datetime]
    LastUpdatedDate: NotRequired[datetime]
    NotificationConfiguration: NotRequired[NotificationConfigurationTypeDef]
    WorkerAccessConfiguration: NotRequired[WorkerAccessConfigurationTypeDef]


class DescribeInferenceComponentOutputTypeDef(TypedDict):
    InferenceComponentName: str
    InferenceComponentArn: str
    EndpointName: str
    EndpointArn: str
    VariantName: str
    FailureReason: str
    Specification: InferenceComponentSpecificationSummaryTypeDef
    RuntimeConfig: InferenceComponentRuntimeConfigSummaryTypeDef
    CreationTime: datetime
    LastModifiedTime: datetime
    InferenceComponentStatus: InferenceComponentStatusType
    LastDeploymentConfig: InferenceComponentDeploymentConfigOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


InferenceComponentDeploymentConfigUnionTypeDef = Union[
    InferenceComponentDeploymentConfigTypeDef, InferenceComponentDeploymentConfigOutputTypeDef
]


class ResourceConfigTypeDef(TypedDict):
    InstanceType: NotRequired[TrainingInstanceTypeType]
    InstanceCount: NotRequired[int]
    VolumeSizeInGB: NotRequired[int]
    VolumeKmsKeyId: NotRequired[str]
    KeepAlivePeriodInSeconds: NotRequired[int]
    InstanceGroups: NotRequired[Sequence[InstanceGroupTypeDef]]
    TrainingPlanArn: NotRequired[str]
    InstancePlacementConfig: NotRequired[InstancePlacementConfigUnionTypeDef]


class TrainingSpecificationOutputTypeDef(TypedDict):
    TrainingImage: str
    SupportedTrainingInstanceTypes: list[TrainingInstanceTypeType]
    TrainingChannels: list[ChannelSpecificationOutputTypeDef]
    TrainingImageDigest: NotRequired[str]
    SupportedHyperParameters: NotRequired[list[HyperParameterSpecificationOutputTypeDef]]
    SupportsDistributedTraining: NotRequired[bool]
    MetricDefinitions: NotRequired[list[MetricDefinitionTypeDef]]
    SupportedTuningJobObjectiveMetrics: NotRequired[list[HyperParameterTuningJobObjectiveTypeDef]]
    AdditionalS3DataSource: NotRequired[AdditionalS3DataSourceTypeDef]


class TrainingSpecificationTypeDef(TypedDict):
    TrainingImage: str
    SupportedTrainingInstanceTypes: Sequence[TrainingInstanceTypeType]
    TrainingChannels: Sequence[ChannelSpecificationTypeDef]
    TrainingImageDigest: NotRequired[str]
    SupportedHyperParameters: NotRequired[Sequence[HyperParameterSpecificationTypeDef]]
    SupportsDistributedTraining: NotRequired[bool]
    MetricDefinitions: NotRequired[Sequence[MetricDefinitionTypeDef]]
    SupportedTuningJobObjectiveMetrics: NotRequired[
        Sequence[HyperParameterTuningJobObjectiveTypeDef]
    ]
    AdditionalS3DataSource: NotRequired[AdditionalS3DataSourceTypeDef]


class ListAppImageConfigsResponseTypeDef(TypedDict):
    AppImageConfigs: list[AppImageConfigDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateAppImageConfigRequestTypeDef(TypedDict):
    AppImageConfigName: str
    Tags: NotRequired[Sequence[TagTypeDef]]
    KernelGatewayImageConfig: NotRequired[KernelGatewayImageConfigUnionTypeDef]
    JupyterLabAppImageConfig: NotRequired[JupyterLabAppImageConfigUnionTypeDef]
    CodeEditorAppImageConfig: NotRequired[CodeEditorAppImageConfigUnionTypeDef]


class UpdateAppImageConfigRequestTypeDef(TypedDict):
    AppImageConfigName: str
    KernelGatewayImageConfig: NotRequired[KernelGatewayImageConfigUnionTypeDef]
    JupyterLabAppImageConfig: NotRequired[JupyterLabAppImageConfigUnionTypeDef]
    CodeEditorAppImageConfig: NotRequired[CodeEditorAppImageConfigUnionTypeDef]


class LabelingJobSummaryTypeDef(TypedDict):
    LabelingJobName: str
    LabelingJobArn: str
    CreationTime: datetime
    LastModifiedTime: datetime
    LabelingJobStatus: LabelingJobStatusType
    LabelCounters: LabelCountersTypeDef
    WorkteamArn: str
    PreHumanTaskLambdaArn: NotRequired[str]
    AnnotationConsolidationLambdaArn: NotRequired[str]
    FailureReason: NotRequired[str]
    LabelingJobOutput: NotRequired[LabelingJobOutputTypeDef]
    InputConfig: NotRequired[LabelingJobInputConfigOutputTypeDef]


LabelingJobInputConfigUnionTypeDef = Union[
    LabelingJobInputConfigTypeDef, LabelingJobInputConfigOutputTypeDef
]


class ScalingPolicyTypeDef(TypedDict):
    TargetTracking: NotRequired[TargetTrackingScalingPolicyConfigurationTypeDef]


ChannelOutputTypeDef = TypedDict(
    "ChannelOutputTypeDef",
    {
        "ChannelName": str,
        "DataSource": DataSourceOutputTypeDef,
        "ContentType": NotRequired[str],
        "CompressionType": NotRequired[CompressionTypeType],
        "RecordWrapperType": NotRequired[RecordWrapperType],
        "InputMode": NotRequired[TrainingInputModeType],
        "ShuffleConfig": NotRequired[ShuffleConfigTypeDef],
    },
)


class DataSourceTypeDef(TypedDict):
    S3DataSource: NotRequired[S3DataSourceUnionTypeDef]
    FileSystemDataSource: NotRequired[FileSystemDataSourceTypeDef]
    DatasetSource: NotRequired[DatasetSourceTypeDef]


class ContainerDefinitionOutputTypeDef(TypedDict):
    ContainerHostname: NotRequired[str]
    Image: NotRequired[str]
    ImageConfig: NotRequired[ImageConfigTypeDef]
    Mode: NotRequired[ContainerModeType]
    ModelDataUrl: NotRequired[str]
    ModelDataSource: NotRequired[ModelDataSourceTypeDef]
    AdditionalModelDataSources: NotRequired[list[AdditionalModelDataSourceTypeDef]]
    Environment: NotRequired[dict[str, str]]
    ModelPackageName: NotRequired[str]
    InferenceSpecificationName: NotRequired[str]
    MultiModelConfig: NotRequired[MultiModelConfigTypeDef]


class ContainerDefinitionTypeDef(TypedDict):
    ContainerHostname: NotRequired[str]
    Image: NotRequired[str]
    ImageConfig: NotRequired[ImageConfigTypeDef]
    Mode: NotRequired[ContainerModeType]
    ModelDataUrl: NotRequired[str]
    ModelDataSource: NotRequired[ModelDataSourceTypeDef]
    AdditionalModelDataSources: NotRequired[Sequence[AdditionalModelDataSourceTypeDef]]
    Environment: NotRequired[Mapping[str, str]]
    ModelPackageName: NotRequired[str]
    InferenceSpecificationName: NotRequired[str]
    MultiModelConfig: NotRequired[MultiModelConfigTypeDef]


class ModelPackageContainerDefinitionOutputTypeDef(TypedDict):
    ContainerHostname: NotRequired[str]
    Image: NotRequired[str]
    ImageDigest: NotRequired[str]
    ModelDataUrl: NotRequired[str]
    ModelDataSource: NotRequired[ModelDataSourceTypeDef]
    ProductId: NotRequired[str]
    Environment: NotRequired[dict[str, str]]
    ModelInput: NotRequired[ModelInputTypeDef]
    Framework: NotRequired[str]
    FrameworkVersion: NotRequired[str]
    NearestModelName: NotRequired[str]
    AdditionalS3DataSource: NotRequired[AdditionalS3DataSourceTypeDef]
    ModelDataETag: NotRequired[str]
    IsCheckpoint: NotRequired[bool]
    BaseModel: NotRequired[BaseModelTypeDef]


class ModelPackageContainerDefinitionTypeDef(TypedDict):
    ContainerHostname: NotRequired[str]
    Image: NotRequired[str]
    ImageDigest: NotRequired[str]
    ModelDataUrl: NotRequired[str]
    ModelDataSource: NotRequired[ModelDataSourceTypeDef]
    ProductId: NotRequired[str]
    Environment: NotRequired[Mapping[str, str]]
    ModelInput: NotRequired[ModelInputTypeDef]
    Framework: NotRequired[str]
    FrameworkVersion: NotRequired[str]
    NearestModelName: NotRequired[str]
    AdditionalS3DataSource: NotRequired[AdditionalS3DataSourceTypeDef]
    ModelDataETag: NotRequired[str]
    IsCheckpoint: NotRequired[bool]
    BaseModel: NotRequired[BaseModelTypeDef]


class SourceAlgorithmTypeDef(TypedDict):
    AlgorithmName: str
    ModelDataUrl: NotRequired[str]
    ModelDataSource: NotRequired[ModelDataSourceTypeDef]
    ModelDataETag: NotRequired[str]


class ListMonitoringAlertsResponseTypeDef(TypedDict):
    MonitoringAlertSummaries: list[MonitoringAlertSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


DescribeInferenceExperimentResponseTypeDef = TypedDict(
    "DescribeInferenceExperimentResponseTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Type": Literal["ShadowMode"],
        "Schedule": InferenceExperimentScheduleOutputTypeDef,
        "Status": InferenceExperimentStatusType,
        "StatusReason": str,
        "Description": str,
        "CreationTime": datetime,
        "CompletionTime": datetime,
        "LastModifiedTime": datetime,
        "RoleArn": str,
        "EndpointMetadata": EndpointMetadataTypeDef,
        "ModelVariants": list[ModelVariantConfigSummaryTypeDef],
        "DataStorageConfig": InferenceExperimentDataStorageConfigOutputTypeDef,
        "ShadowModeConfig": ShadowModeConfigOutputTypeDef,
        "KmsKey": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class StopInferenceExperimentRequestTypeDef(TypedDict):
    Name: str
    ModelVariantActions: Mapping[str, ModelVariantActionType]
    DesiredModelVariants: NotRequired[Sequence[ModelVariantConfigTypeDef]]
    DesiredState: NotRequired[InferenceExperimentStopDesiredStateType]
    Reason: NotRequired[str]


OptimizationConfigUnionTypeDef = Union[OptimizationConfigTypeDef, OptimizationConfigOutputTypeDef]


class DataQualityJobInputOutputTypeDef(TypedDict):
    EndpointInput: NotRequired[EndpointInputTypeDef]
    BatchTransformInput: NotRequired[BatchTransformInputOutputTypeDef]


class ModelBiasJobInputOutputTypeDef(TypedDict):
    GroundTruthS3Input: MonitoringGroundTruthS3InputTypeDef
    EndpointInput: NotRequired[EndpointInputTypeDef]
    BatchTransformInput: NotRequired[BatchTransformInputOutputTypeDef]


class ModelExplainabilityJobInputOutputTypeDef(TypedDict):
    EndpointInput: NotRequired[EndpointInputTypeDef]
    BatchTransformInput: NotRequired[BatchTransformInputOutputTypeDef]


class ModelQualityJobInputOutputTypeDef(TypedDict):
    GroundTruthS3Input: MonitoringGroundTruthS3InputTypeDef
    EndpointInput: NotRequired[EndpointInputTypeDef]
    BatchTransformInput: NotRequired[BatchTransformInputOutputTypeDef]


class MonitoringInputOutputTypeDef(TypedDict):
    EndpointInput: NotRequired[EndpointInputTypeDef]
    BatchTransformInput: NotRequired[BatchTransformInputOutputTypeDef]


class DataQualityJobInputTypeDef(TypedDict):
    EndpointInput: NotRequired[EndpointInputTypeDef]
    BatchTransformInput: NotRequired[BatchTransformInputTypeDef]


class ModelBiasJobInputTypeDef(TypedDict):
    GroundTruthS3Input: MonitoringGroundTruthS3InputTypeDef
    EndpointInput: NotRequired[EndpointInputTypeDef]
    BatchTransformInput: NotRequired[BatchTransformInputTypeDef]


class ModelExplainabilityJobInputTypeDef(TypedDict):
    EndpointInput: NotRequired[EndpointInputTypeDef]
    BatchTransformInput: NotRequired[BatchTransformInputTypeDef]


class ModelQualityJobInputTypeDef(TypedDict):
    GroundTruthS3Input: MonitoringGroundTruthS3InputTypeDef
    EndpointInput: NotRequired[EndpointInputTypeDef]
    BatchTransformInput: NotRequired[BatchTransformInputTypeDef]


class MonitoringInputTypeDef(TypedDict):
    EndpointInput: NotRequired[EndpointInputTypeDef]
    BatchTransformInput: NotRequired[BatchTransformInputTypeDef]


MonitoringOutputConfigUnionTypeDef = Union[
    MonitoringOutputConfigTypeDef, MonitoringOutputConfigOutputTypeDef
]
MemberDefinitionUnionTypeDef = Union[MemberDefinitionTypeDef, MemberDefinitionOutputTypeDef]


class DescribeOptimizationJobResponseTypeDef(TypedDict):
    OptimizationJobArn: str
    OptimizationJobStatus: OptimizationJobStatusType
    OptimizationStartTime: datetime
    OptimizationEndTime: datetime
    CreationTime: datetime
    LastModifiedTime: datetime
    FailureReason: str
    OptimizationJobName: str
    ModelSource: OptimizationJobModelSourceTypeDef
    OptimizationEnvironment: dict[str, str]
    DeploymentInstanceType: OptimizationJobDeploymentInstanceTypeType
    MaxInstanceCount: int
    OptimizationConfigs: list[OptimizationConfigOutputTypeDef]
    OutputConfig: OptimizationJobOutputConfigTypeDef
    OptimizationOutput: OptimizationOutputTypeDef
    RoleArn: str
    StoppingCondition: StoppingConditionTypeDef
    VpcConfig: OptimizationVpcConfigOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


CreatePartnerAppRequestTypeDef = TypedDict(
    "CreatePartnerAppRequestTypeDef",
    {
        "Name": str,
        "Type": PartnerAppTypeType,
        "ExecutionRoleArn": str,
        "Tier": str,
        "AuthType": Literal["IAM"],
        "KmsKeyId": NotRequired[str],
        "MaintenanceConfig": NotRequired[PartnerAppMaintenanceConfigTypeDef],
        "ApplicationConfig": NotRequired[PartnerAppConfigUnionTypeDef],
        "EnableIamSessionBasedIdentity": NotRequired[bool],
        "EnableAutoMinorVersionUpgrade": NotRequired[bool],
        "ClientToken": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)


class UpdatePartnerAppRequestTypeDef(TypedDict):
    Arn: str
    MaintenanceConfig: NotRequired[PartnerAppMaintenanceConfigTypeDef]
    Tier: NotRequired[str]
    ApplicationConfig: NotRequired[PartnerAppConfigUnionTypeDef]
    EnableIamSessionBasedIdentity: NotRequired[bool]
    EnableAutoMinorVersionUpgrade: NotRequired[bool]
    AppVersion: NotRequired[str]
    ClientToken: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateClusterSchedulerConfigRequestTypeDef(TypedDict):
    Name: str
    ClusterArn: str
    SchedulerConfig: SchedulerConfigUnionTypeDef
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class UpdateClusterSchedulerConfigRequestTypeDef(TypedDict):
    ClusterSchedulerConfigId: str
    TargetVersion: int
    SchedulerConfig: NotRequired[SchedulerConfigUnionTypeDef]
    Description: NotRequired[str]


class DescribeProcessingJobResponseTypeDef(TypedDict):
    ProcessingInputs: list[ProcessingInputTypeDef]
    ProcessingOutputConfig: ProcessingOutputConfigOutputTypeDef
    ProcessingJobName: str
    ProcessingResources: ProcessingResourcesTypeDef
    StoppingCondition: ProcessingStoppingConditionTypeDef
    AppSpecification: AppSpecificationOutputTypeDef
    Environment: dict[str, str]
    NetworkConfig: NetworkConfigOutputTypeDef
    RoleArn: str
    ExperimentConfig: ExperimentConfigTypeDef
    ProcessingJobArn: str
    ProcessingJobStatus: ProcessingJobStatusType
    ExitMessage: str
    FailureReason: str
    ProcessingEndTime: datetime
    ProcessingStartTime: datetime
    LastModifiedTime: datetime
    CreationTime: datetime
    MonitoringScheduleArn: str
    AutoMLJobArn: str
    TrainingJobArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ProcessingJobTypeDef(TypedDict):
    ProcessingInputs: NotRequired[list[ProcessingInputTypeDef]]
    ProcessingOutputConfig: NotRequired[ProcessingOutputConfigOutputTypeDef]
    ProcessingJobName: NotRequired[str]
    ProcessingResources: NotRequired[ProcessingResourcesTypeDef]
    StoppingCondition: NotRequired[ProcessingStoppingConditionTypeDef]
    AppSpecification: NotRequired[AppSpecificationOutputTypeDef]
    Environment: NotRequired[dict[str, str]]
    NetworkConfig: NotRequired[NetworkConfigOutputTypeDef]
    RoleArn: NotRequired[str]
    ExperimentConfig: NotRequired[ExperimentConfigTypeDef]
    ProcessingJobArn: NotRequired[str]
    ProcessingJobStatus: NotRequired[ProcessingJobStatusType]
    ExitMessage: NotRequired[str]
    FailureReason: NotRequired[str]
    ProcessingEndTime: NotRequired[datetime]
    ProcessingStartTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    CreationTime: NotRequired[datetime]
    MonitoringScheduleArn: NotRequired[str]
    AutoMLJobArn: NotRequired[str]
    TrainingJobArn: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


ProcessingOutputConfigUnionTypeDef = Union[
    ProcessingOutputConfigTypeDef, ProcessingOutputConfigOutputTypeDef
]


class CreateProjectInputTypeDef(TypedDict):
    ProjectName: str
    ProjectDescription: NotRequired[str]
    ServiceCatalogProvisioningDetails: NotRequired[ServiceCatalogProvisioningDetailsUnionTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    TemplateProviders: NotRequired[Sequence[CreateTemplateProviderTypeDef]]


class DescribeFlowDefinitionResponseTypeDef(TypedDict):
    FlowDefinitionArn: str
    FlowDefinitionName: str
    FlowDefinitionStatus: FlowDefinitionStatusType
    CreationTime: datetime
    HumanLoopRequestSource: HumanLoopRequestSourceTypeDef
    HumanLoopActivationConfig: HumanLoopActivationConfigTypeDef
    HumanLoopConfig: HumanLoopConfigOutputTypeDef
    OutputConfig: FlowDefinitionOutputConfigTypeDef
    RoleArn: str
    FailureReason: str
    ResponseMetadata: ResponseMetadataTypeDef


HumanLoopConfigUnionTypeDef = Union[HumanLoopConfigTypeDef, HumanLoopConfigOutputTypeDef]


class DescribeLabelingJobResponseTypeDef(TypedDict):
    LabelingJobStatus: LabelingJobStatusType
    LabelCounters: LabelCountersTypeDef
    FailureReason: str
    CreationTime: datetime
    LastModifiedTime: datetime
    JobReferenceCode: str
    LabelingJobName: str
    LabelingJobArn: str
    LabelAttributeName: str
    InputConfig: LabelingJobInputConfigOutputTypeDef
    OutputConfig: LabelingJobOutputConfigTypeDef
    RoleArn: str
    LabelCategoryConfigS3Uri: str
    StoppingConditions: LabelingJobStoppingConditionsTypeDef
    LabelingJobAlgorithmsConfig: LabelingJobAlgorithmsConfigOutputTypeDef
    HumanTaskConfig: HumanTaskConfigOutputTypeDef
    Tags: list[TagTypeDef]
    LabelingJobOutput: LabelingJobOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


HumanTaskConfigUnionTypeDef = Union[HumanTaskConfigTypeDef, HumanTaskConfigOutputTypeDef]


class StartPipelineExecutionRequestTypeDef(TypedDict):
    PipelineName: str
    ClientRequestToken: str
    PipelineExecutionDisplayName: NotRequired[str]
    PipelineParameters: NotRequired[Sequence[ParameterTypeDef]]
    PipelineExecutionDescription: NotRequired[str]
    ParallelismConfiguration: NotRequired[ParallelismConfigurationTypeDef]
    SelectiveExecutionConfig: NotRequired[SelectiveExecutionConfigUnionTypeDef]
    PipelineVersionId: NotRequired[int]
    MlflowExperimentName: NotRequired[str]


CreateInferenceExperimentRequestTypeDef = TypedDict(
    "CreateInferenceExperimentRequestTypeDef",
    {
        "Name": str,
        "Type": Literal["ShadowMode"],
        "RoleArn": str,
        "EndpointName": str,
        "ModelVariants": Sequence[ModelVariantConfigTypeDef],
        "ShadowModeConfig": ShadowModeConfigUnionTypeDef,
        "Schedule": NotRequired[InferenceExperimentScheduleUnionTypeDef],
        "Description": NotRequired[str],
        "DataStorageConfig": NotRequired[InferenceExperimentDataStorageConfigUnionTypeDef],
        "KmsKey": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)


class UpdateInferenceExperimentRequestTypeDef(TypedDict):
    Name: str
    Schedule: NotRequired[InferenceExperimentScheduleUnionTypeDef]
    Description: NotRequired[str]
    ModelVariants: NotRequired[Sequence[ModelVariantConfigTypeDef]]
    DataStorageConfig: NotRequired[InferenceExperimentDataStorageConfigUnionTypeDef]
    ShadowModeConfig: NotRequired[ShadowModeConfigUnionTypeDef]


class SpaceSettingsOutputTypeDef(TypedDict):
    JupyterServerAppSettings: NotRequired[JupyterServerAppSettingsOutputTypeDef]
    KernelGatewayAppSettings: NotRequired[KernelGatewayAppSettingsOutputTypeDef]
    CodeEditorAppSettings: NotRequired[SpaceCodeEditorAppSettingsTypeDef]
    JupyterLabAppSettings: NotRequired[SpaceJupyterLabAppSettingsOutputTypeDef]
    AppType: NotRequired[AppTypeType]
    SpaceStorageSettings: NotRequired[SpaceStorageSettingsTypeDef]
    SpaceManagedResources: NotRequired[FeatureStatusType]
    CustomFileSystems: NotRequired[list[CustomFileSystemTypeDef]]
    RemoteAccess: NotRequired[FeatureStatusType]


class SpaceSettingsTypeDef(TypedDict):
    JupyterServerAppSettings: NotRequired[JupyterServerAppSettingsTypeDef]
    KernelGatewayAppSettings: NotRequired[KernelGatewayAppSettingsTypeDef]
    CodeEditorAppSettings: NotRequired[SpaceCodeEditorAppSettingsTypeDef]
    JupyterLabAppSettings: NotRequired[SpaceJupyterLabAppSettingsTypeDef]
    AppType: NotRequired[AppTypeType]
    SpaceStorageSettings: NotRequired[SpaceStorageSettingsTypeDef]
    SpaceManagedResources: NotRequired[FeatureStatusType]
    CustomFileSystems: NotRequired[Sequence[CustomFileSystemTypeDef]]
    RemoteAccess: NotRequired[FeatureStatusType]


AlgorithmSpecificationUnionTypeDef = Union[
    AlgorithmSpecificationTypeDef, AlgorithmSpecificationOutputTypeDef
]


class CreateTransformJobRequestTypeDef(TypedDict):
    TransformJobName: str
    ModelName: str
    TransformInput: TransformInputTypeDef
    TransformOutput: TransformOutputTypeDef
    TransformResources: TransformResourcesTypeDef
    MaxConcurrentTransforms: NotRequired[int]
    ModelClientConfig: NotRequired[ModelClientConfigTypeDef]
    MaxPayloadInMB: NotRequired[int]
    BatchStrategy: NotRequired[BatchStrategyType]
    Environment: NotRequired[Mapping[str, str]]
    DataCaptureConfig: NotRequired[BatchDataCaptureConfigTypeDef]
    DataProcessing: NotRequired[DataProcessingTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ExperimentConfig: NotRequired[ExperimentConfigTypeDef]


class DescribeTransformJobResponseTypeDef(TypedDict):
    TransformJobName: str
    TransformJobArn: str
    TransformJobStatus: TransformJobStatusType
    FailureReason: str
    ModelName: str
    MaxConcurrentTransforms: int
    ModelClientConfig: ModelClientConfigTypeDef
    MaxPayloadInMB: int
    BatchStrategy: BatchStrategyType
    Environment: dict[str, str]
    TransformInput: TransformInputTypeDef
    TransformOutput: TransformOutputTypeDef
    DataCaptureConfig: BatchDataCaptureConfigTypeDef
    TransformResources: TransformResourcesTypeDef
    CreationTime: datetime
    TransformStartTime: datetime
    TransformEndTime: datetime
    LabelingJobArn: str
    AutoMLJobArn: str
    DataProcessing: DataProcessingTypeDef
    ExperimentConfig: ExperimentConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class TransformJobDefinitionOutputTypeDef(TypedDict):
    TransformInput: TransformInputTypeDef
    TransformOutput: TransformOutputTypeDef
    TransformResources: TransformResourcesTypeDef
    MaxConcurrentTransforms: NotRequired[int]
    MaxPayloadInMB: NotRequired[int]
    BatchStrategy: NotRequired[BatchStrategyType]
    Environment: NotRequired[dict[str, str]]


class TransformJobDefinitionTypeDef(TypedDict):
    TransformInput: TransformInputTypeDef
    TransformOutput: TransformOutputTypeDef
    TransformResources: TransformResourcesTypeDef
    MaxConcurrentTransforms: NotRequired[int]
    MaxPayloadInMB: NotRequired[int]
    BatchStrategy: NotRequired[BatchStrategyType]
    Environment: NotRequired[Mapping[str, str]]


class TransformJobTypeDef(TypedDict):
    TransformJobName: NotRequired[str]
    TransformJobArn: NotRequired[str]
    TransformJobStatus: NotRequired[TransformJobStatusType]
    FailureReason: NotRequired[str]
    ModelName: NotRequired[str]
    MaxConcurrentTransforms: NotRequired[int]
    ModelClientConfig: NotRequired[ModelClientConfigTypeDef]
    MaxPayloadInMB: NotRequired[int]
    BatchStrategy: NotRequired[BatchStrategyType]
    Environment: NotRequired[dict[str, str]]
    TransformInput: NotRequired[TransformInputTypeDef]
    TransformOutput: NotRequired[TransformOutputTypeDef]
    DataCaptureConfig: NotRequired[BatchDataCaptureConfigTypeDef]
    TransformResources: NotRequired[TransformResourcesTypeDef]
    CreationTime: NotRequired[datetime]
    TransformStartTime: NotRequired[datetime]
    TransformEndTime: NotRequired[datetime]
    LabelingJobArn: NotRequired[str]
    AutoMLJobArn: NotRequired[str]
    DataProcessing: NotRequired[DataProcessingTypeDef]
    ExperimentConfig: NotRequired[ExperimentConfigTypeDef]
    Tags: NotRequired[list[TagTypeDef]]


class ComputeQuotaSummaryTypeDef(TypedDict):
    ComputeQuotaArn: str
    ComputeQuotaId: str
    Name: str
    Status: SchedulerResourceStatusType
    ComputeQuotaTarget: ComputeQuotaTargetTypeDef
    CreationTime: datetime
    ComputeQuotaVersion: NotRequired[int]
    ClusterArn: NotRequired[str]
    ComputeQuotaConfig: NotRequired[ComputeQuotaConfigOutputTypeDef]
    ActivationState: NotRequired[ActivationStateType]
    LastModifiedTime: NotRequired[datetime]


class DescribeComputeQuotaResponseTypeDef(TypedDict):
    ComputeQuotaArn: str
    ComputeQuotaId: str
    Name: str
    Description: str
    ComputeQuotaVersion: int
    Status: SchedulerResourceStatusType
    FailureReason: str
    ClusterArn: str
    ComputeQuotaConfig: ComputeQuotaConfigOutputTypeDef
    ComputeQuotaTarget: ComputeQuotaTargetTypeDef
    ActivationState: ActivationStateType
    CreationTime: datetime
    CreatedBy: UserContextTypeDef
    LastModifiedTime: datetime
    LastModifiedBy: UserContextTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


ComputeQuotaConfigUnionTypeDef = Union[ComputeQuotaConfigTypeDef, ComputeQuotaConfigOutputTypeDef]


class DescribeDomainResponseTypeDef(TypedDict):
    DomainArn: str
    DomainId: str
    DomainName: str
    HomeEfsFileSystemId: str
    SingleSignOnManagedApplicationInstanceId: str
    SingleSignOnApplicationArn: str
    Status: DomainStatusType
    CreationTime: datetime
    LastModifiedTime: datetime
    FailureReason: str
    SecurityGroupIdForDomainBoundary: str
    AuthMode: AuthModeType
    DefaultUserSettings: UserSettingsOutputTypeDef
    DomainSettings: DomainSettingsOutputTypeDef
    AppNetworkAccessType: AppNetworkAccessTypeType
    HomeEfsFileSystemKmsKeyId: str
    SubnetIds: list[str]
    Url: str
    VpcId: str
    KmsKeyId: str
    AppSecurityGroupManagement: AppSecurityGroupManagementType
    TagPropagation: TagPropagationType
    DefaultSpaceSettings: DefaultSpaceSettingsOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeUserProfileResponseTypeDef(TypedDict):
    DomainId: str
    UserProfileArn: str
    UserProfileName: str
    HomeEfsFileSystemUid: str
    Status: UserProfileStatusType
    LastModifiedTime: datetime
    CreationTime: datetime
    FailureReason: str
    SingleSignOnUserIdentifier: str
    SingleSignOnUserValue: str
    UserSettings: UserSettingsOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


DefaultSpaceSettingsUnionTypeDef = Union[
    DefaultSpaceSettingsTypeDef, DefaultSpaceSettingsOutputTypeDef
]
UserSettingsUnionTypeDef = Union[UserSettingsTypeDef, UserSettingsOutputTypeDef]


class DescribeAutoMLJobV2ResponseTypeDef(TypedDict):
    AutoMLJobName: str
    AutoMLJobArn: str
    AutoMLJobInputDataConfig: list[AutoMLJobChannelTypeDef]
    OutputDataConfig: AutoMLOutputDataConfigTypeDef
    RoleArn: str
    AutoMLJobObjective: AutoMLJobObjectiveTypeDef
    AutoMLProblemTypeConfig: AutoMLProblemTypeConfigOutputTypeDef
    AutoMLProblemTypeConfigName: AutoMLProblemTypeConfigNameType
    CreationTime: datetime
    EndTime: datetime
    LastModifiedTime: datetime
    FailureReason: str
    PartialFailureReasons: list[AutoMLPartialFailureReasonTypeDef]
    BestCandidate: AutoMLCandidateTypeDef
    AutoMLJobStatus: AutoMLJobStatusType
    AutoMLJobSecondaryStatus: AutoMLJobSecondaryStatusType
    AutoMLJobArtifacts: AutoMLJobArtifactsTypeDef
    ResolvedAttributes: AutoMLResolvedAttributesTypeDef
    ModelDeployConfig: ModelDeployConfigTypeDef
    ModelDeployResult: ModelDeployResultTypeDef
    DataSplitConfig: AutoMLDataSplitConfigTypeDef
    SecurityConfig: AutoMLSecurityConfigOutputTypeDef
    AutoMLComputeConfig: AutoMLComputeConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


AutoMLProblemTypeConfigUnionTypeDef = Union[
    AutoMLProblemTypeConfigTypeDef, AutoMLProblemTypeConfigOutputTypeDef
]


class CreateAutoMLJobRequestTypeDef(TypedDict):
    AutoMLJobName: str
    InputDataConfig: Sequence[AutoMLChannelTypeDef]
    OutputDataConfig: AutoMLOutputDataConfigTypeDef
    RoleArn: str
    ProblemType: NotRequired[ProblemTypeType]
    AutoMLJobObjective: NotRequired[AutoMLJobObjectiveTypeDef]
    AutoMLJobConfig: NotRequired[AutoMLJobConfigUnionTypeDef]
    GenerateCandidateDefinitionsOnly: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ModelDeployConfig: NotRequired[ModelDeployConfigTypeDef]


class ListPipelineExecutionStepsResponseTypeDef(TypedDict):
    PipelineExecutionSteps: list[PipelineExecutionStepTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ClusterEventDetailTypeDef(TypedDict):
    EventId: str
    ClusterArn: str
    ClusterName: str
    ResourceType: ClusterEventResourceTypeType
    EventTime: datetime
    InstanceGroupName: NotRequired[str]
    InstanceId: NotRequired[str]
    EventDetails: NotRequired[EventDetailsTypeDef]
    Description: NotRequired[str]


class ClusterInstanceGroupDetailsTypeDef(TypedDict):
    CurrentCount: NotRequired[int]
    TargetCount: NotRequired[int]
    MinCount: NotRequired[int]
    InstanceGroupName: NotRequired[str]
    InstanceType: NotRequired[ClusterInstanceTypeType]
    LifeCycleConfig: NotRequired[ClusterLifeCycleConfigTypeDef]
    ExecutionRole: NotRequired[str]
    ThreadsPerCore: NotRequired[int]
    InstanceStorageConfigs: NotRequired[list[ClusterInstanceStorageConfigTypeDef]]
    OnStartDeepHealthChecks: NotRequired[list[DeepHealthCheckTypeType]]
    Status: NotRequired[InstanceGroupStatusType]
    TrainingPlanArn: NotRequired[str]
    TrainingPlanStatus: NotRequired[str]
    OverrideVpcConfig: NotRequired[VpcConfigOutputTypeDef]
    ScheduledUpdateConfig: NotRequired[ScheduledUpdateConfigOutputTypeDef]
    CurrentImageId: NotRequired[str]
    DesiredImageId: NotRequired[str]
    ActiveOperations: NotRequired[dict[Literal["Scaling"], int]]
    KubernetesConfig: NotRequired[ClusterKubernetesConfigDetailsTypeDef]
    CapacityRequirements: NotRequired[ClusterCapacityRequirementsOutputTypeDef]
    TargetStateCount: NotRequired[int]
    SoftwareUpdateStatus: NotRequired[SoftwareUpdateStatusType]
    ActiveSoftwareUpdateConfig: NotRequired[DeploymentConfigurationOutputTypeDef]


class ClusterRestrictedInstanceGroupDetailsTypeDef(TypedDict):
    CurrentCount: NotRequired[int]
    TargetCount: NotRequired[int]
    InstanceGroupName: NotRequired[str]
    InstanceType: NotRequired[ClusterInstanceTypeType]
    ExecutionRole: NotRequired[str]
    ThreadsPerCore: NotRequired[int]
    InstanceStorageConfigs: NotRequired[list[ClusterInstanceStorageConfigTypeDef]]
    OnStartDeepHealthChecks: NotRequired[list[DeepHealthCheckTypeType]]
    Status: NotRequired[InstanceGroupStatusType]
    TrainingPlanArn: NotRequired[str]
    TrainingPlanStatus: NotRequired[str]
    OverrideVpcConfig: NotRequired[VpcConfigOutputTypeDef]
    ScheduledUpdateConfig: NotRequired[ScheduledUpdateConfigOutputTypeDef]
    EnvironmentConfig: NotRequired[EnvironmentConfigDetailsTypeDef]


class ScheduledUpdateConfigTypeDef(TypedDict):
    ScheduleExpression: str
    DeploymentConfig: NotRequired[DeploymentConfigurationUnionTypeDef]


class UpdateClusterSoftwareRequestTypeDef(TypedDict):
    ClusterName: str
    InstanceGroups: NotRequired[Sequence[UpdateClusterSoftwareInstanceGroupSpecificationTypeDef]]
    DeploymentConfig: NotRequired[DeploymentConfigurationUnionTypeDef]
    ImageId: NotRequired[str]


DeploymentConfigUnionTypeDef = Union[DeploymentConfigTypeDef, DeploymentConfigOutputTypeDef]


class DescribeInferenceRecommendationsJobResponseTypeDef(TypedDict):
    JobName: str
    JobDescription: str
    JobType: RecommendationJobTypeType
    JobArn: str
    RoleArn: str
    Status: RecommendationJobStatusType
    CreationTime: datetime
    CompletionTime: datetime
    LastModifiedTime: datetime
    FailureReason: str
    InputConfig: RecommendationJobInputConfigOutputTypeDef
    StoppingConditions: RecommendationJobStoppingConditionsOutputTypeDef
    InferenceRecommendations: list[InferenceRecommendationTypeDef]
    EndpointPerformances: list[EndpointPerformanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


HyperParameterTuningJobConfigUnionTypeDef = Union[
    HyperParameterTuningJobConfigTypeDef, HyperParameterTuningJobConfigOutputTypeDef
]
RecommendationJobInputConfigUnionTypeDef = Union[
    RecommendationJobInputConfigTypeDef, RecommendationJobInputConfigOutputTypeDef
]


class DescribeEndpointConfigOutputTypeDef(TypedDict):
    EndpointConfigName: str
    EndpointConfigArn: str
    ProductionVariants: list[ProductionVariantTypeDef]
    DataCaptureConfig: DataCaptureConfigOutputTypeDef
    KmsKeyId: str
    CreationTime: datetime
    AsyncInferenceConfig: AsyncInferenceConfigOutputTypeDef
    ExplainerConfig: ExplainerConfigOutputTypeDef
    ShadowProductionVariants: list[ProductionVariantTypeDef]
    ExecutionRoleArn: str
    VpcConfig: VpcConfigOutputTypeDef
    EnableNetworkIsolation: bool
    MetricsConfig: MetricsConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeEndpointOutputTypeDef(TypedDict):
    EndpointName: str
    EndpointArn: str
    EndpointConfigName: str
    ProductionVariants: list[ProductionVariantSummaryTypeDef]
    DataCaptureConfig: DataCaptureConfigSummaryTypeDef
    EndpointStatus: EndpointStatusType
    FailureReason: str
    CreationTime: datetime
    LastModifiedTime: datetime
    LastDeploymentConfig: DeploymentConfigOutputTypeDef
    AsyncInferenceConfig: AsyncInferenceConfigOutputTypeDef
    PendingDeploymentSummary: PendingDeploymentSummaryTypeDef
    ExplainerConfig: ExplainerConfigOutputTypeDef
    ShadowProductionVariants: list[ProductionVariantSummaryTypeDef]
    MetricsConfig: MetricsConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


ExplainerConfigUnionTypeDef = Union[ExplainerConfigTypeDef, ExplainerConfigOutputTypeDef]


class ListSpacesResponseTypeDef(TypedDict):
    Spaces: list[SpaceDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListInferenceRecommendationsJobStepsResponseTypeDef(TypedDict):
    Steps: list[InferenceRecommendationsJobStepTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeWorkteamResponseTypeDef(TypedDict):
    Workteam: WorkteamTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListWorkteamsResponseTypeDef(TypedDict):
    Workteams: list[WorkteamTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateWorkteamResponseTypeDef(TypedDict):
    Workteam: WorkteamTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateInferenceComponentInputTypeDef(TypedDict):
    InferenceComponentName: str
    Specification: NotRequired[InferenceComponentSpecificationTypeDef]
    RuntimeConfig: NotRequired[InferenceComponentRuntimeConfigTypeDef]
    DeploymentConfig: NotRequired[InferenceComponentDeploymentConfigUnionTypeDef]


ResourceConfigUnionTypeDef = Union[ResourceConfigTypeDef, ResourceConfigOutputTypeDef]
TrainingSpecificationUnionTypeDef = Union[
    TrainingSpecificationTypeDef, TrainingSpecificationOutputTypeDef
]


class ListLabelingJobsResponseTypeDef(TypedDict):
    LabelingJobSummaryList: list[LabelingJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DynamicScalingConfigurationTypeDef(TypedDict):
    MinCapacity: NotRequired[int]
    MaxCapacity: NotRequired[int]
    ScaleInCooldown: NotRequired[int]
    ScaleOutCooldown: NotRequired[int]
    ScalingPolicies: NotRequired[list[ScalingPolicyTypeDef]]


class DescribeTrainingJobResponseTypeDef(TypedDict):
    TrainingJobName: str
    TrainingJobArn: str
    TuningJobArn: str
    LabelingJobArn: str
    AutoMLJobArn: str
    ModelArtifacts: ModelArtifactsTypeDef
    TrainingJobStatus: TrainingJobStatusType
    SecondaryStatus: SecondaryStatusType
    FailureReason: str
    HyperParameters: dict[str, str]
    AlgorithmSpecification: AlgorithmSpecificationOutputTypeDef
    RoleArn: str
    InputDataConfig: list[ChannelOutputTypeDef]
    OutputDataConfig: OutputDataConfigTypeDef
    ResourceConfig: ResourceConfigOutputTypeDef
    WarmPoolStatus: WarmPoolStatusTypeDef
    VpcConfig: VpcConfigOutputTypeDef
    StoppingCondition: StoppingConditionTypeDef
    CreationTime: datetime
    TrainingStartTime: datetime
    TrainingEndTime: datetime
    LastModifiedTime: datetime
    SecondaryStatusTransitions: list[SecondaryStatusTransitionTypeDef]
    FinalMetricDataList: list[MetricDataTypeDef]
    EnableNetworkIsolation: bool
    EnableInterContainerTrafficEncryption: bool
    EnableManagedSpotTraining: bool
    CheckpointConfig: CheckpointConfigTypeDef
    TrainingTimeInSeconds: int
    BillableTimeInSeconds: int
    BillableTokenCount: int
    DebugHookConfig: DebugHookConfigOutputTypeDef
    ExperimentConfig: ExperimentConfigTypeDef
    DebugRuleConfigurations: list[DebugRuleConfigurationOutputTypeDef]
    TensorBoardOutputConfig: TensorBoardOutputConfigTypeDef
    DebugRuleEvaluationStatuses: list[DebugRuleEvaluationStatusTypeDef]
    ProfilerConfig: ProfilerConfigOutputTypeDef
    ProfilerRuleConfigurations: list[ProfilerRuleConfigurationOutputTypeDef]
    ProfilerRuleEvaluationStatuses: list[ProfilerRuleEvaluationStatusTypeDef]
    ProfilingStatus: ProfilingStatusType
    Environment: dict[str, str]
    RetryStrategy: RetryStrategyTypeDef
    RemoteDebugConfig: RemoteDebugConfigTypeDef
    InfraCheckConfig: InfraCheckConfigTypeDef
    ServerlessJobConfig: ServerlessJobConfigTypeDef
    MlflowConfig: MlflowConfigTypeDef
    ModelPackageConfig: ModelPackageConfigTypeDef
    MlflowDetails: MlflowDetailsTypeDef
    ProgressInfo: TrainingProgressInfoTypeDef
    OutputModelPackageArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class HyperParameterTrainingJobDefinitionOutputTypeDef(TypedDict):
    AlgorithmSpecification: HyperParameterAlgorithmSpecificationOutputTypeDef
    RoleArn: str
    OutputDataConfig: OutputDataConfigTypeDef
    StoppingCondition: StoppingConditionTypeDef
    DefinitionName: NotRequired[str]
    TuningObjective: NotRequired[HyperParameterTuningJobObjectiveTypeDef]
    HyperParameterRanges: NotRequired[ParameterRangesOutputTypeDef]
    StaticHyperParameters: NotRequired[dict[str, str]]
    InputDataConfig: NotRequired[list[ChannelOutputTypeDef]]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]
    ResourceConfig: NotRequired[ResourceConfigOutputTypeDef]
    HyperParameterTuningResourceConfig: NotRequired[HyperParameterTuningResourceConfigOutputTypeDef]
    EnableNetworkIsolation: NotRequired[bool]
    EnableInterContainerTrafficEncryption: NotRequired[bool]
    EnableManagedSpotTraining: NotRequired[bool]
    CheckpointConfig: NotRequired[CheckpointConfigTypeDef]
    RetryStrategy: NotRequired[RetryStrategyTypeDef]
    Environment: NotRequired[dict[str, str]]


class TrainingJobDefinitionOutputTypeDef(TypedDict):
    TrainingInputMode: TrainingInputModeType
    InputDataConfig: list[ChannelOutputTypeDef]
    OutputDataConfig: OutputDataConfigTypeDef
    ResourceConfig: ResourceConfigOutputTypeDef
    StoppingCondition: StoppingConditionTypeDef
    HyperParameters: NotRequired[dict[str, str]]


class TrainingJobTypeDef(TypedDict):
    TrainingJobName: NotRequired[str]
    TrainingJobArn: NotRequired[str]
    TuningJobArn: NotRequired[str]
    LabelingJobArn: NotRequired[str]
    AutoMLJobArn: NotRequired[str]
    ModelArtifacts: NotRequired[ModelArtifactsTypeDef]
    TrainingJobStatus: NotRequired[TrainingJobStatusType]
    SecondaryStatus: NotRequired[SecondaryStatusType]
    FailureReason: NotRequired[str]
    HyperParameters: NotRequired[dict[str, str]]
    AlgorithmSpecification: NotRequired[AlgorithmSpecificationOutputTypeDef]
    RoleArn: NotRequired[str]
    InputDataConfig: NotRequired[list[ChannelOutputTypeDef]]
    OutputDataConfig: NotRequired[OutputDataConfigTypeDef]
    ResourceConfig: NotRequired[ResourceConfigOutputTypeDef]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]
    StoppingCondition: NotRequired[StoppingConditionTypeDef]
    CreationTime: NotRequired[datetime]
    TrainingStartTime: NotRequired[datetime]
    TrainingEndTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    SecondaryStatusTransitions: NotRequired[list[SecondaryStatusTransitionTypeDef]]
    FinalMetricDataList: NotRequired[list[MetricDataTypeDef]]
    EnableNetworkIsolation: NotRequired[bool]
    EnableInterContainerTrafficEncryption: NotRequired[bool]
    EnableManagedSpotTraining: NotRequired[bool]
    CheckpointConfig: NotRequired[CheckpointConfigTypeDef]
    TrainingTimeInSeconds: NotRequired[int]
    BillableTimeInSeconds: NotRequired[int]
    DebugHookConfig: NotRequired[DebugHookConfigOutputTypeDef]
    ExperimentConfig: NotRequired[ExperimentConfigTypeDef]
    DebugRuleConfigurations: NotRequired[list[DebugRuleConfigurationOutputTypeDef]]
    TensorBoardOutputConfig: NotRequired[TensorBoardOutputConfigTypeDef]
    DebugRuleEvaluationStatuses: NotRequired[list[DebugRuleEvaluationStatusTypeDef]]
    OutputModelPackageArn: NotRequired[str]
    ModelPackageConfig: NotRequired[ModelPackageConfigTypeDef]
    ProfilerConfig: NotRequired[ProfilerConfigOutputTypeDef]
    Environment: NotRequired[dict[str, str]]
    RetryStrategy: NotRequired[RetryStrategyTypeDef]
    Tags: NotRequired[list[TagTypeDef]]


DataSourceUnionTypeDef = Union[DataSourceTypeDef, DataSourceOutputTypeDef]


class DescribeModelOutputTypeDef(TypedDict):
    ModelName: str
    PrimaryContainer: ContainerDefinitionOutputTypeDef
    Containers: list[ContainerDefinitionOutputTypeDef]
    InferenceExecutionConfig: InferenceExecutionConfigTypeDef
    ExecutionRoleArn: str
    VpcConfig: VpcConfigOutputTypeDef
    CreationTime: datetime
    ModelArn: str
    EnableNetworkIsolation: bool
    DeploymentRecommendation: DeploymentRecommendationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModelTypeDef(TypedDict):
    ModelName: NotRequired[str]
    PrimaryContainer: NotRequired[ContainerDefinitionOutputTypeDef]
    Containers: NotRequired[list[ContainerDefinitionOutputTypeDef]]
    InferenceExecutionConfig: NotRequired[InferenceExecutionConfigTypeDef]
    ExecutionRoleArn: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigOutputTypeDef]
    CreationTime: NotRequired[datetime]
    ModelArn: NotRequired[str]
    EnableNetworkIsolation: NotRequired[bool]
    Tags: NotRequired[list[TagTypeDef]]
    DeploymentRecommendation: NotRequired[DeploymentRecommendationTypeDef]


ContainerDefinitionUnionTypeDef = Union[
    ContainerDefinitionTypeDef, ContainerDefinitionOutputTypeDef
]


class AdditionalInferenceSpecificationDefinitionOutputTypeDef(TypedDict):
    Name: str
    Containers: list[ModelPackageContainerDefinitionOutputTypeDef]
    Description: NotRequired[str]
    SupportedTransformInstanceTypes: NotRequired[list[TransformInstanceTypeType]]
    SupportedRealtimeInferenceInstanceTypes: NotRequired[list[ProductionVariantInstanceTypeType]]
    SupportedContentTypes: NotRequired[list[str]]
    SupportedResponseMIMETypes: NotRequired[list[str]]


class InferenceSpecificationOutputTypeDef(TypedDict):
    Containers: list[ModelPackageContainerDefinitionOutputTypeDef]
    SupportedTransformInstanceTypes: NotRequired[list[TransformInstanceTypeType]]
    SupportedRealtimeInferenceInstanceTypes: NotRequired[list[ProductionVariantInstanceTypeType]]
    SupportedContentTypes: NotRequired[list[str]]
    SupportedResponseMIMETypes: NotRequired[list[str]]


class InferenceSpecificationTypeDef(TypedDict):
    Containers: Sequence[ModelPackageContainerDefinitionTypeDef]
    SupportedTransformInstanceTypes: NotRequired[Sequence[TransformInstanceTypeType]]
    SupportedRealtimeInferenceInstanceTypes: NotRequired[
        Sequence[ProductionVariantInstanceTypeType]
    ]
    SupportedContentTypes: NotRequired[Sequence[str]]
    SupportedResponseMIMETypes: NotRequired[Sequence[str]]


ModelPackageContainerDefinitionUnionTypeDef = Union[
    ModelPackageContainerDefinitionTypeDef, ModelPackageContainerDefinitionOutputTypeDef
]


class SourceAlgorithmSpecificationOutputTypeDef(TypedDict):
    SourceAlgorithms: list[SourceAlgorithmTypeDef]


class SourceAlgorithmSpecificationTypeDef(TypedDict):
    SourceAlgorithms: Sequence[SourceAlgorithmTypeDef]


class CreateOptimizationJobRequestTypeDef(TypedDict):
    OptimizationJobName: str
    RoleArn: str
    ModelSource: OptimizationJobModelSourceTypeDef
    DeploymentInstanceType: OptimizationJobDeploymentInstanceTypeType
    OptimizationConfigs: Sequence[OptimizationConfigUnionTypeDef]
    OutputConfig: OptimizationJobOutputConfigTypeDef
    StoppingCondition: StoppingConditionTypeDef
    MaxInstanceCount: NotRequired[int]
    OptimizationEnvironment: NotRequired[Mapping[str, str]]
    Tags: NotRequired[Sequence[TagTypeDef]]
    VpcConfig: NotRequired[OptimizationVpcConfigUnionTypeDef]


class DescribeDataQualityJobDefinitionResponseTypeDef(TypedDict):
    JobDefinitionArn: str
    JobDefinitionName: str
    CreationTime: datetime
    DataQualityBaselineConfig: DataQualityBaselineConfigTypeDef
    DataQualityAppSpecification: DataQualityAppSpecificationOutputTypeDef
    DataQualityJobInput: DataQualityJobInputOutputTypeDef
    DataQualityJobOutputConfig: MonitoringOutputConfigOutputTypeDef
    JobResources: MonitoringResourcesTypeDef
    NetworkConfig: MonitoringNetworkConfigOutputTypeDef
    RoleArn: str
    StoppingCondition: MonitoringStoppingConditionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeModelBiasJobDefinitionResponseTypeDef(TypedDict):
    JobDefinitionArn: str
    JobDefinitionName: str
    CreationTime: datetime
    ModelBiasBaselineConfig: ModelBiasBaselineConfigTypeDef
    ModelBiasAppSpecification: ModelBiasAppSpecificationOutputTypeDef
    ModelBiasJobInput: ModelBiasJobInputOutputTypeDef
    ModelBiasJobOutputConfig: MonitoringOutputConfigOutputTypeDef
    JobResources: MonitoringResourcesTypeDef
    NetworkConfig: MonitoringNetworkConfigOutputTypeDef
    RoleArn: str
    StoppingCondition: MonitoringStoppingConditionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeModelExplainabilityJobDefinitionResponseTypeDef(TypedDict):
    JobDefinitionArn: str
    JobDefinitionName: str
    CreationTime: datetime
    ModelExplainabilityBaselineConfig: ModelExplainabilityBaselineConfigTypeDef
    ModelExplainabilityAppSpecification: ModelExplainabilityAppSpecificationOutputTypeDef
    ModelExplainabilityJobInput: ModelExplainabilityJobInputOutputTypeDef
    ModelExplainabilityJobOutputConfig: MonitoringOutputConfigOutputTypeDef
    JobResources: MonitoringResourcesTypeDef
    NetworkConfig: MonitoringNetworkConfigOutputTypeDef
    RoleArn: str
    StoppingCondition: MonitoringStoppingConditionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeModelQualityJobDefinitionResponseTypeDef(TypedDict):
    JobDefinitionArn: str
    JobDefinitionName: str
    CreationTime: datetime
    ModelQualityBaselineConfig: ModelQualityBaselineConfigTypeDef
    ModelQualityAppSpecification: ModelQualityAppSpecificationOutputTypeDef
    ModelQualityJobInput: ModelQualityJobInputOutputTypeDef
    ModelQualityJobOutputConfig: MonitoringOutputConfigOutputTypeDef
    JobResources: MonitoringResourcesTypeDef
    NetworkConfig: MonitoringNetworkConfigOutputTypeDef
    RoleArn: str
    StoppingCondition: MonitoringStoppingConditionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class MonitoringJobDefinitionOutputTypeDef(TypedDict):
    MonitoringInputs: list[MonitoringInputOutputTypeDef]
    MonitoringOutputConfig: MonitoringOutputConfigOutputTypeDef
    MonitoringResources: MonitoringResourcesTypeDef
    MonitoringAppSpecification: MonitoringAppSpecificationOutputTypeDef
    RoleArn: str
    BaselineConfig: NotRequired[MonitoringBaselineConfigTypeDef]
    StoppingCondition: NotRequired[MonitoringStoppingConditionTypeDef]
    Environment: NotRequired[dict[str, str]]
    NetworkConfig: NotRequired[NetworkConfigOutputTypeDef]


DataQualityJobInputUnionTypeDef = Union[
    DataQualityJobInputTypeDef, DataQualityJobInputOutputTypeDef
]
ModelBiasJobInputUnionTypeDef = Union[ModelBiasJobInputTypeDef, ModelBiasJobInputOutputTypeDef]
ModelExplainabilityJobInputUnionTypeDef = Union[
    ModelExplainabilityJobInputTypeDef, ModelExplainabilityJobInputOutputTypeDef
]
ModelQualityJobInputUnionTypeDef = Union[
    ModelQualityJobInputTypeDef, ModelQualityJobInputOutputTypeDef
]


class MonitoringJobDefinitionTypeDef(TypedDict):
    MonitoringInputs: Sequence[MonitoringInputTypeDef]
    MonitoringOutputConfig: MonitoringOutputConfigTypeDef
    MonitoringResources: MonitoringResourcesTypeDef
    MonitoringAppSpecification: MonitoringAppSpecificationTypeDef
    RoleArn: str
    BaselineConfig: NotRequired[MonitoringBaselineConfigTypeDef]
    StoppingCondition: NotRequired[MonitoringStoppingConditionTypeDef]
    Environment: NotRequired[Mapping[str, str]]
    NetworkConfig: NotRequired[NetworkConfigTypeDef]


class CreateWorkteamRequestTypeDef(TypedDict):
    WorkteamName: str
    MemberDefinitions: Sequence[MemberDefinitionUnionTypeDef]
    Description: str
    WorkforceName: NotRequired[str]
    NotificationConfiguration: NotRequired[NotificationConfigurationTypeDef]
    WorkerAccessConfiguration: NotRequired[WorkerAccessConfigurationTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class UpdateWorkteamRequestTypeDef(TypedDict):
    WorkteamName: str
    MemberDefinitions: NotRequired[Sequence[MemberDefinitionUnionTypeDef]]
    Description: NotRequired[str]
    NotificationConfiguration: NotRequired[NotificationConfigurationTypeDef]
    WorkerAccessConfiguration: NotRequired[WorkerAccessConfigurationTypeDef]


class CreateProcessingJobRequestTypeDef(TypedDict):
    ProcessingJobName: str
    ProcessingResources: ProcessingResourcesTypeDef
    AppSpecification: AppSpecificationUnionTypeDef
    RoleArn: str
    ProcessingInputs: NotRequired[Sequence[ProcessingInputTypeDef]]
    ProcessingOutputConfig: NotRequired[ProcessingOutputConfigUnionTypeDef]
    StoppingCondition: NotRequired[ProcessingStoppingConditionTypeDef]
    Environment: NotRequired[Mapping[str, str]]
    NetworkConfig: NotRequired[NetworkConfigUnionTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ExperimentConfig: NotRequired[ExperimentConfigTypeDef]


class CreateFlowDefinitionRequestTypeDef(TypedDict):
    FlowDefinitionName: str
    OutputConfig: FlowDefinitionOutputConfigTypeDef
    RoleArn: str
    HumanLoopRequestSource: NotRequired[HumanLoopRequestSourceTypeDef]
    HumanLoopActivationConfig: NotRequired[HumanLoopActivationConfigTypeDef]
    HumanLoopConfig: NotRequired[HumanLoopConfigUnionTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateLabelingJobRequestTypeDef(TypedDict):
    LabelingJobName: str
    LabelAttributeName: str
    InputConfig: LabelingJobInputConfigUnionTypeDef
    OutputConfig: LabelingJobOutputConfigTypeDef
    RoleArn: str
    HumanTaskConfig: HumanTaskConfigUnionTypeDef
    LabelCategoryConfigS3Uri: NotRequired[str]
    StoppingConditions: NotRequired[LabelingJobStoppingConditionsTypeDef]
    LabelingJobAlgorithmsConfig: NotRequired[LabelingJobAlgorithmsConfigUnionTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class DescribeSpaceResponseTypeDef(TypedDict):
    DomainId: str
    SpaceArn: str
    SpaceName: str
    HomeEfsFileSystemUid: str
    Status: SpaceStatusType
    LastModifiedTime: datetime
    CreationTime: datetime
    FailureReason: str
    SpaceSettings: SpaceSettingsOutputTypeDef
    OwnershipSettings: OwnershipSettingsTypeDef
    SpaceSharingSettings: SpaceSharingSettingsTypeDef
    SpaceDisplayName: str
    Url: str
    ResponseMetadata: ResponseMetadataTypeDef


SpaceSettingsUnionTypeDef = Union[SpaceSettingsTypeDef, SpaceSettingsOutputTypeDef]


class ModelPackageValidationProfileOutputTypeDef(TypedDict):
    ProfileName: str
    TransformJobDefinition: TransformJobDefinitionOutputTypeDef


class ModelPackageValidationProfileTypeDef(TypedDict):
    ProfileName: str
    TransformJobDefinition: TransformJobDefinitionTypeDef


class ListComputeQuotasResponseTypeDef(TypedDict):
    ComputeQuotaSummaries: list[ComputeQuotaSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateComputeQuotaRequestTypeDef(TypedDict):
    Name: str
    ClusterArn: str
    ComputeQuotaConfig: ComputeQuotaConfigUnionTypeDef
    ComputeQuotaTarget: ComputeQuotaTargetTypeDef
    Description: NotRequired[str]
    ActivationState: NotRequired[ActivationStateType]
    Tags: NotRequired[Sequence[TagTypeDef]]


class UpdateComputeQuotaRequestTypeDef(TypedDict):
    ComputeQuotaId: str
    TargetVersion: int
    ComputeQuotaConfig: NotRequired[ComputeQuotaConfigUnionTypeDef]
    ComputeQuotaTarget: NotRequired[ComputeQuotaTargetTypeDef]
    ActivationState: NotRequired[ActivationStateType]
    Description: NotRequired[str]


class CreateDomainRequestTypeDef(TypedDict):
    DomainName: str
    AuthMode: AuthModeType
    DefaultUserSettings: UserSettingsUnionTypeDef
    DomainSettings: NotRequired[DomainSettingsUnionTypeDef]
    SubnetIds: NotRequired[Sequence[str]]
    VpcId: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    AppNetworkAccessType: NotRequired[AppNetworkAccessTypeType]
    HomeEfsFileSystemKmsKeyId: NotRequired[str]
    KmsKeyId: NotRequired[str]
    AppSecurityGroupManagement: NotRequired[AppSecurityGroupManagementType]
    TagPropagation: NotRequired[TagPropagationType]
    DefaultSpaceSettings: NotRequired[DefaultSpaceSettingsUnionTypeDef]


class CreateUserProfileRequestTypeDef(TypedDict):
    DomainId: str
    UserProfileName: str
    SingleSignOnUserIdentifier: NotRequired[str]
    SingleSignOnUserValue: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    UserSettings: NotRequired[UserSettingsUnionTypeDef]


class UpdateDomainRequestTypeDef(TypedDict):
    DomainId: str
    DefaultUserSettings: NotRequired[UserSettingsUnionTypeDef]
    DomainSettingsForUpdate: NotRequired[DomainSettingsForUpdateTypeDef]
    AppSecurityGroupManagement: NotRequired[AppSecurityGroupManagementType]
    DefaultSpaceSettings: NotRequired[DefaultSpaceSettingsUnionTypeDef]
    SubnetIds: NotRequired[Sequence[str]]
    AppNetworkAccessType: NotRequired[AppNetworkAccessTypeType]
    TagPropagation: NotRequired[TagPropagationType]
    VpcId: NotRequired[str]


class UpdateUserProfileRequestTypeDef(TypedDict):
    DomainId: str
    UserProfileName: str
    UserSettings: NotRequired[UserSettingsUnionTypeDef]


class CreateAutoMLJobV2RequestTypeDef(TypedDict):
    AutoMLJobName: str
    AutoMLJobInputDataConfig: Sequence[AutoMLJobChannelTypeDef]
    OutputDataConfig: AutoMLOutputDataConfigTypeDef
    AutoMLProblemTypeConfig: AutoMLProblemTypeConfigUnionTypeDef
    RoleArn: str
    Tags: NotRequired[Sequence[TagTypeDef]]
    SecurityConfig: NotRequired[AutoMLSecurityConfigUnionTypeDef]
    AutoMLJobObjective: NotRequired[AutoMLJobObjectiveTypeDef]
    ModelDeployConfig: NotRequired[ModelDeployConfigTypeDef]
    DataSplitConfig: NotRequired[AutoMLDataSplitConfigTypeDef]
    AutoMLComputeConfig: NotRequired[AutoMLComputeConfigTypeDef]


class DescribeClusterEventResponseTypeDef(TypedDict):
    EventDetails: ClusterEventDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeClusterResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterName: str
    ClusterStatus: ClusterStatusType
    CreationTime: datetime
    FailureMessage: str
    InstanceGroups: list[ClusterInstanceGroupDetailsTypeDef]
    RestrictedInstanceGroups: list[ClusterRestrictedInstanceGroupDetailsTypeDef]
    VpcConfig: VpcConfigOutputTypeDef
    Orchestrator: ClusterOrchestratorTypeDef
    TieredStorageConfig: ClusterTieredStorageConfigTypeDef
    NodeRecovery: ClusterNodeRecoveryType
    NodeProvisioningMode: Literal["Continuous"]
    ClusterRole: str
    AutoScaling: ClusterAutoScalingConfigOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


ScheduledUpdateConfigUnionTypeDef = Union[
    ScheduledUpdateConfigTypeDef, ScheduledUpdateConfigOutputTypeDef
]


class CreateEndpointInputTypeDef(TypedDict):
    EndpointName: str
    EndpointConfigName: str
    DeploymentConfig: NotRequired[DeploymentConfigUnionTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class UpdateEndpointInputTypeDef(TypedDict):
    EndpointName: str
    EndpointConfigName: str
    RetainAllVariantProperties: NotRequired[bool]
    ExcludeRetainedVariantProperties: NotRequired[Sequence[VariantPropertyTypeDef]]
    DeploymentConfig: NotRequired[DeploymentConfigUnionTypeDef]
    RetainDeploymentConfig: NotRequired[bool]


class CreateInferenceRecommendationsJobRequestTypeDef(TypedDict):
    JobName: str
    JobType: RecommendationJobTypeType
    RoleArn: str
    InputConfig: RecommendationJobInputConfigUnionTypeDef
    JobDescription: NotRequired[str]
    StoppingConditions: NotRequired[RecommendationJobStoppingConditionsUnionTypeDef]
    OutputConfig: NotRequired[RecommendationJobOutputConfigTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateEndpointConfigInputTypeDef(TypedDict):
    EndpointConfigName: str
    ProductionVariants: Sequence[ProductionVariantTypeDef]
    DataCaptureConfig: NotRequired[DataCaptureConfigUnionTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    KmsKeyId: NotRequired[str]
    AsyncInferenceConfig: NotRequired[AsyncInferenceConfigUnionTypeDef]
    ExplainerConfig: NotRequired[ExplainerConfigUnionTypeDef]
    ShadowProductionVariants: NotRequired[Sequence[ProductionVariantTypeDef]]
    ExecutionRoleArn: NotRequired[str]
    VpcConfig: NotRequired[VpcConfigUnionTypeDef]
    EnableNetworkIsolation: NotRequired[bool]
    MetricsConfig: NotRequired[MetricsConfigTypeDef]


class GetScalingConfigurationRecommendationResponseTypeDef(TypedDict):
    InferenceRecommendationsJobName: str
    RecommendationId: str
    EndpointName: str
    TargetCpuUtilizationPerCore: int
    ScalingPolicyObjective: ScalingPolicyObjectiveTypeDef
    Metric: ScalingPolicyMetricTypeDef
    DynamicScalingConfiguration: DynamicScalingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeHyperParameterTuningJobResponseTypeDef(TypedDict):
    HyperParameterTuningJobName: str
    HyperParameterTuningJobArn: str
    HyperParameterTuningJobConfig: HyperParameterTuningJobConfigOutputTypeDef
    TrainingJobDefinition: HyperParameterTrainingJobDefinitionOutputTypeDef
    TrainingJobDefinitions: list[HyperParameterTrainingJobDefinitionOutputTypeDef]
    HyperParameterTuningJobStatus: HyperParameterTuningJobStatusType
    CreationTime: datetime
    HyperParameterTuningEndTime: datetime
    LastModifiedTime: datetime
    TrainingJobStatusCounters: TrainingJobStatusCountersTypeDef
    ObjectiveStatusCounters: ObjectiveStatusCountersTypeDef
    BestTrainingJob: HyperParameterTrainingJobSummaryTypeDef
    OverallBestTrainingJob: HyperParameterTrainingJobSummaryTypeDef
    WarmStartConfig: HyperParameterTuningJobWarmStartConfigOutputTypeDef
    Autotune: AutotuneTypeDef
    FailureReason: str
    TuningJobCompletionDetails: HyperParameterTuningJobCompletionDetailsTypeDef
    ConsumedResources: HyperParameterTuningJobConsumedResourcesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class HyperParameterTuningJobSearchEntityTypeDef(TypedDict):
    HyperParameterTuningJobName: NotRequired[str]
    HyperParameterTuningJobArn: NotRequired[str]
    HyperParameterTuningJobConfig: NotRequired[HyperParameterTuningJobConfigOutputTypeDef]
    TrainingJobDefinition: NotRequired[HyperParameterTrainingJobDefinitionOutputTypeDef]
    TrainingJobDefinitions: NotRequired[list[HyperParameterTrainingJobDefinitionOutputTypeDef]]
    HyperParameterTuningJobStatus: NotRequired[HyperParameterTuningJobStatusType]
    CreationTime: NotRequired[datetime]
    HyperParameterTuningEndTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    TrainingJobStatusCounters: NotRequired[TrainingJobStatusCountersTypeDef]
    ObjectiveStatusCounters: NotRequired[ObjectiveStatusCountersTypeDef]
    BestTrainingJob: NotRequired[HyperParameterTrainingJobSummaryTypeDef]
    OverallBestTrainingJob: NotRequired[HyperParameterTrainingJobSummaryTypeDef]
    WarmStartConfig: NotRequired[HyperParameterTuningJobWarmStartConfigOutputTypeDef]
    FailureReason: NotRequired[str]
    TuningJobCompletionDetails: NotRequired[HyperParameterTuningJobCompletionDetailsTypeDef]
    ConsumedResources: NotRequired[HyperParameterTuningJobConsumedResourcesTypeDef]
    Tags: NotRequired[list[TagTypeDef]]


class AlgorithmValidationProfileOutputTypeDef(TypedDict):
    ProfileName: str
    TrainingJobDefinition: TrainingJobDefinitionOutputTypeDef
    TransformJobDefinition: NotRequired[TransformJobDefinitionOutputTypeDef]


class TrialComponentSourceDetailTypeDef(TypedDict):
    SourceArn: NotRequired[str]
    TrainingJob: NotRequired[TrainingJobTypeDef]
    ProcessingJob: NotRequired[ProcessingJobTypeDef]
    TransformJob: NotRequired[TransformJobTypeDef]


ChannelTypeDef = TypedDict(
    "ChannelTypeDef",
    {
        "ChannelName": str,
        "DataSource": DataSourceUnionTypeDef,
        "ContentType": NotRequired[str],
        "CompressionType": NotRequired[CompressionTypeType],
        "RecordWrapperType": NotRequired[RecordWrapperType],
        "InputMode": NotRequired[TrainingInputModeType],
        "ShuffleConfig": NotRequired[ShuffleConfigTypeDef],
    },
)


class CreateModelInputTypeDef(TypedDict):
    ModelName: str
    PrimaryContainer: NotRequired[ContainerDefinitionUnionTypeDef]
    Containers: NotRequired[Sequence[ContainerDefinitionUnionTypeDef]]
    InferenceExecutionConfig: NotRequired[InferenceExecutionConfigTypeDef]
    ExecutionRoleArn: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    VpcConfig: NotRequired[VpcConfigUnionTypeDef]
    EnableNetworkIsolation: NotRequired[bool]


class BatchDescribeModelPackageSummaryTypeDef(TypedDict):
    ModelPackageGroupName: str
    ModelPackageArn: str
    CreationTime: datetime
    InferenceSpecification: InferenceSpecificationOutputTypeDef
    ModelPackageStatus: ModelPackageStatusType
    ModelPackageVersion: NotRequired[int]
    ModelPackageDescription: NotRequired[str]
    ModelApprovalStatus: NotRequired[ModelApprovalStatusType]
    ModelPackageRegistrationType: NotRequired[ModelPackageRegistrationTypeType]


InferenceSpecificationUnionTypeDef = Union[
    InferenceSpecificationTypeDef, InferenceSpecificationOutputTypeDef
]


class AdditionalInferenceSpecificationDefinitionTypeDef(TypedDict):
    Name: str
    Containers: Sequence[ModelPackageContainerDefinitionUnionTypeDef]
    Description: NotRequired[str]
    SupportedTransformInstanceTypes: NotRequired[Sequence[TransformInstanceTypeType]]
    SupportedRealtimeInferenceInstanceTypes: NotRequired[
        Sequence[ProductionVariantInstanceTypeType]
    ]
    SupportedContentTypes: NotRequired[Sequence[str]]
    SupportedResponseMIMETypes: NotRequired[Sequence[str]]


SourceAlgorithmSpecificationUnionTypeDef = Union[
    SourceAlgorithmSpecificationTypeDef, SourceAlgorithmSpecificationOutputTypeDef
]


class MonitoringScheduleConfigOutputTypeDef(TypedDict):
    ScheduleConfig: NotRequired[ScheduleConfigTypeDef]
    MonitoringJobDefinition: NotRequired[MonitoringJobDefinitionOutputTypeDef]
    MonitoringJobDefinitionName: NotRequired[str]
    MonitoringType: NotRequired[MonitoringTypeType]


class CreateDataQualityJobDefinitionRequestTypeDef(TypedDict):
    JobDefinitionName: str
    DataQualityAppSpecification: DataQualityAppSpecificationUnionTypeDef
    DataQualityJobInput: DataQualityJobInputUnionTypeDef
    DataQualityJobOutputConfig: MonitoringOutputConfigUnionTypeDef
    JobResources: MonitoringResourcesTypeDef
    RoleArn: str
    DataQualityBaselineConfig: NotRequired[DataQualityBaselineConfigTypeDef]
    NetworkConfig: NotRequired[MonitoringNetworkConfigUnionTypeDef]
    StoppingCondition: NotRequired[MonitoringStoppingConditionTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateModelBiasJobDefinitionRequestTypeDef(TypedDict):
    JobDefinitionName: str
    ModelBiasAppSpecification: ModelBiasAppSpecificationUnionTypeDef
    ModelBiasJobInput: ModelBiasJobInputUnionTypeDef
    ModelBiasJobOutputConfig: MonitoringOutputConfigUnionTypeDef
    JobResources: MonitoringResourcesTypeDef
    RoleArn: str
    ModelBiasBaselineConfig: NotRequired[ModelBiasBaselineConfigTypeDef]
    NetworkConfig: NotRequired[MonitoringNetworkConfigUnionTypeDef]
    StoppingCondition: NotRequired[MonitoringStoppingConditionTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateModelExplainabilityJobDefinitionRequestTypeDef(TypedDict):
    JobDefinitionName: str
    ModelExplainabilityAppSpecification: ModelExplainabilityAppSpecificationUnionTypeDef
    ModelExplainabilityJobInput: ModelExplainabilityJobInputUnionTypeDef
    ModelExplainabilityJobOutputConfig: MonitoringOutputConfigUnionTypeDef
    JobResources: MonitoringResourcesTypeDef
    RoleArn: str
    ModelExplainabilityBaselineConfig: NotRequired[ModelExplainabilityBaselineConfigTypeDef]
    NetworkConfig: NotRequired[MonitoringNetworkConfigUnionTypeDef]
    StoppingCondition: NotRequired[MonitoringStoppingConditionTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateModelQualityJobDefinitionRequestTypeDef(TypedDict):
    JobDefinitionName: str
    ModelQualityAppSpecification: ModelQualityAppSpecificationUnionTypeDef
    ModelQualityJobInput: ModelQualityJobInputUnionTypeDef
    ModelQualityJobOutputConfig: MonitoringOutputConfigUnionTypeDef
    JobResources: MonitoringResourcesTypeDef
    RoleArn: str
    ModelQualityBaselineConfig: NotRequired[ModelQualityBaselineConfigTypeDef]
    NetworkConfig: NotRequired[MonitoringNetworkConfigUnionTypeDef]
    StoppingCondition: NotRequired[MonitoringStoppingConditionTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class MonitoringScheduleConfigTypeDef(TypedDict):
    ScheduleConfig: NotRequired[ScheduleConfigTypeDef]
    MonitoringJobDefinition: NotRequired[MonitoringJobDefinitionTypeDef]
    MonitoringJobDefinitionName: NotRequired[str]
    MonitoringType: NotRequired[MonitoringTypeType]


class CreateSpaceRequestTypeDef(TypedDict):
    DomainId: str
    SpaceName: str
    Tags: NotRequired[Sequence[TagTypeDef]]
    SpaceSettings: NotRequired[SpaceSettingsUnionTypeDef]
    OwnershipSettings: NotRequired[OwnershipSettingsTypeDef]
    SpaceSharingSettings: NotRequired[SpaceSharingSettingsTypeDef]
    SpaceDisplayName: NotRequired[str]


class UpdateSpaceRequestTypeDef(TypedDict):
    DomainId: str
    SpaceName: str
    SpaceSettings: NotRequired[SpaceSettingsUnionTypeDef]
    SpaceDisplayName: NotRequired[str]


class ModelPackageValidationSpecificationOutputTypeDef(TypedDict):
    ValidationRole: str
    ValidationProfiles: list[ModelPackageValidationProfileOutputTypeDef]


class ModelPackageValidationSpecificationTypeDef(TypedDict):
    ValidationRole: str
    ValidationProfiles: Sequence[ModelPackageValidationProfileTypeDef]


class ClusterInstanceGroupSpecificationTypeDef(TypedDict):
    InstanceCount: int
    InstanceGroupName: str
    InstanceType: ClusterInstanceTypeType
    LifeCycleConfig: ClusterLifeCycleConfigTypeDef
    ExecutionRole: str
    MinInstanceCount: NotRequired[int]
    ThreadsPerCore: NotRequired[int]
    InstanceStorageConfigs: NotRequired[Sequence[ClusterInstanceStorageConfigTypeDef]]
    OnStartDeepHealthChecks: NotRequired[Sequence[DeepHealthCheckTypeType]]
    TrainingPlanArn: NotRequired[str]
    OverrideVpcConfig: NotRequired[VpcConfigUnionTypeDef]
    ScheduledUpdateConfig: NotRequired[ScheduledUpdateConfigUnionTypeDef]
    ImageId: NotRequired[str]
    KubernetesConfig: NotRequired[ClusterKubernetesConfigTypeDef]
    CapacityRequirements: NotRequired[ClusterCapacityRequirementsUnionTypeDef]


class ClusterRestrictedInstanceGroupSpecificationTypeDef(TypedDict):
    InstanceCount: int
    InstanceGroupName: str
    InstanceType: ClusterInstanceTypeType
    ExecutionRole: str
    EnvironmentConfig: EnvironmentConfigTypeDef
    ThreadsPerCore: NotRequired[int]
    InstanceStorageConfigs: NotRequired[Sequence[ClusterInstanceStorageConfigTypeDef]]
    OnStartDeepHealthChecks: NotRequired[Sequence[DeepHealthCheckTypeType]]
    TrainingPlanArn: NotRequired[str]
    OverrideVpcConfig: NotRequired[VpcConfigUnionTypeDef]
    ScheduledUpdateConfig: NotRequired[ScheduledUpdateConfigUnionTypeDef]


class AlgorithmValidationSpecificationOutputTypeDef(TypedDict):
    ValidationRole: str
    ValidationProfiles: list[AlgorithmValidationProfileOutputTypeDef]


class TrialComponentTypeDef(TypedDict):
    TrialComponentName: NotRequired[str]
    DisplayName: NotRequired[str]
    TrialComponentArn: NotRequired[str]
    Source: NotRequired[TrialComponentSourceTypeDef]
    Status: NotRequired[TrialComponentStatusTypeDef]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    CreationTime: NotRequired[datetime]
    CreatedBy: NotRequired[UserContextTypeDef]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedBy: NotRequired[UserContextTypeDef]
    Parameters: NotRequired[dict[str, TrialComponentParameterValueTypeDef]]
    InputArtifacts: NotRequired[dict[str, TrialComponentArtifactTypeDef]]
    OutputArtifacts: NotRequired[dict[str, TrialComponentArtifactTypeDef]]
    Metrics: NotRequired[list[TrialComponentMetricSummaryTypeDef]]
    MetadataProperties: NotRequired[MetadataPropertiesTypeDef]
    SourceDetail: NotRequired[TrialComponentSourceDetailTypeDef]
    LineageGroupArn: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    Parents: NotRequired[list[ParentTypeDef]]
    RunName: NotRequired[str]


ChannelUnionTypeDef = Union[ChannelTypeDef, ChannelOutputTypeDef]


class TrainingJobDefinitionTypeDef(TypedDict):
    TrainingInputMode: TrainingInputModeType
    InputDataConfig: Sequence[ChannelTypeDef]
    OutputDataConfig: OutputDataConfigTypeDef
    ResourceConfig: ResourceConfigTypeDef
    StoppingCondition: StoppingConditionTypeDef
    HyperParameters: NotRequired[Mapping[str, str]]


class BatchDescribeModelPackageOutputTypeDef(TypedDict):
    ModelPackageSummaries: dict[str, BatchDescribeModelPackageSummaryTypeDef]
    BatchDescribeModelPackageErrorMap: dict[str, BatchDescribeModelPackageErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


AdditionalInferenceSpecificationDefinitionUnionTypeDef = Union[
    AdditionalInferenceSpecificationDefinitionTypeDef,
    AdditionalInferenceSpecificationDefinitionOutputTypeDef,
]


class DescribeMonitoringScheduleResponseTypeDef(TypedDict):
    MonitoringScheduleArn: str
    MonitoringScheduleName: str
    MonitoringScheduleStatus: ScheduleStatusType
    MonitoringType: MonitoringTypeType
    FailureReason: str
    CreationTime: datetime
    LastModifiedTime: datetime
    MonitoringScheduleConfig: MonitoringScheduleConfigOutputTypeDef
    EndpointName: str
    LastMonitoringExecutionSummary: MonitoringExecutionSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModelDashboardMonitoringScheduleTypeDef(TypedDict):
    MonitoringScheduleArn: NotRequired[str]
    MonitoringScheduleName: NotRequired[str]
    MonitoringScheduleStatus: NotRequired[ScheduleStatusType]
    MonitoringType: NotRequired[MonitoringTypeType]
    FailureReason: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    MonitoringScheduleConfig: NotRequired[MonitoringScheduleConfigOutputTypeDef]
    EndpointName: NotRequired[str]
    MonitoringAlertSummaries: NotRequired[list[MonitoringAlertSummaryTypeDef]]
    LastMonitoringExecutionSummary: NotRequired[MonitoringExecutionSummaryTypeDef]
    BatchTransformInput: NotRequired[BatchTransformInputOutputTypeDef]


class MonitoringScheduleTypeDef(TypedDict):
    MonitoringScheduleArn: NotRequired[str]
    MonitoringScheduleName: NotRequired[str]
    MonitoringScheduleStatus: NotRequired[ScheduleStatusType]
    MonitoringType: NotRequired[MonitoringTypeType]
    FailureReason: NotRequired[str]
    CreationTime: NotRequired[datetime]
    LastModifiedTime: NotRequired[datetime]
    MonitoringScheduleConfig: NotRequired[MonitoringScheduleConfigOutputTypeDef]
    EndpointName: NotRequired[str]
    LastMonitoringExecutionSummary: NotRequired[MonitoringExecutionSummaryTypeDef]
    Tags: NotRequired[list[TagTypeDef]]


MonitoringScheduleConfigUnionTypeDef = Union[
    MonitoringScheduleConfigTypeDef, MonitoringScheduleConfigOutputTypeDef
]


class DescribeModelPackageOutputTypeDef(TypedDict):
    ModelPackageName: str
    ModelPackageGroupName: str
    ModelPackageVersion: int
    ModelPackageRegistrationType: ModelPackageRegistrationTypeType
    ModelPackageArn: str
    ModelPackageDescription: str
    CreationTime: datetime
    InferenceSpecification: InferenceSpecificationOutputTypeDef
    SourceAlgorithmSpecification: SourceAlgorithmSpecificationOutputTypeDef
    ValidationSpecification: ModelPackageValidationSpecificationOutputTypeDef
    ModelPackageStatus: ModelPackageStatusType
    ModelPackageStatusDetails: ModelPackageStatusDetailsTypeDef
    CertifyForMarketplace: bool
    ModelApprovalStatus: ModelApprovalStatusType
    CreatedBy: UserContextTypeDef
    MetadataProperties: MetadataPropertiesTypeDef
    ModelMetrics: ModelMetricsTypeDef
    LastModifiedTime: datetime
    LastModifiedBy: UserContextTypeDef
    ApprovalDescription: str
    Domain: str
    Task: str
    SamplePayloadUrl: str
    CustomerMetadataProperties: dict[str, str]
    DriftCheckBaselines: DriftCheckBaselinesTypeDef
    AdditionalInferenceSpecifications: list[AdditionalInferenceSpecificationDefinitionOutputTypeDef]
    SkipModelValidation: SkipModelValidationType
    SourceUri: str
    SecurityConfig: ModelPackageSecurityConfigTypeDef
    ModelCard: ModelPackageModelCardTypeDef
    ModelLifeCycle: ModelLifeCycleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModelPackageTypeDef(TypedDict):
    ModelPackageName: NotRequired[str]
    ModelPackageGroupName: NotRequired[str]
    ModelPackageVersion: NotRequired[int]
    ModelPackageRegistrationType: NotRequired[ModelPackageRegistrationTypeType]
    ModelPackageArn: NotRequired[str]
    ModelPackageDescription: NotRequired[str]
    CreationTime: NotRequired[datetime]
    InferenceSpecification: NotRequired[InferenceSpecificationOutputTypeDef]
    SourceAlgorithmSpecification: NotRequired[SourceAlgorithmSpecificationOutputTypeDef]
    ValidationSpecification: NotRequired[ModelPackageValidationSpecificationOutputTypeDef]
    ModelPackageStatus: NotRequired[ModelPackageStatusType]
    ModelPackageStatusDetails: NotRequired[ModelPackageStatusDetailsTypeDef]
    CertifyForMarketplace: NotRequired[bool]
    ModelApprovalStatus: NotRequired[ModelApprovalStatusType]
    CreatedBy: NotRequired[UserContextTypeDef]
    MetadataProperties: NotRequired[MetadataPropertiesTypeDef]
    ModelMetrics: NotRequired[ModelMetricsTypeDef]
    LastModifiedTime: NotRequired[datetime]
    LastModifiedBy: NotRequired[UserContextTypeDef]
    ApprovalDescription: NotRequired[str]
    Domain: NotRequired[str]
    Task: NotRequired[str]
    SamplePayloadUrl: NotRequired[str]
    AdditionalInferenceSpecifications: NotRequired[
        list[AdditionalInferenceSpecificationDefinitionOutputTypeDef]
    ]
    SourceUri: NotRequired[str]
    SecurityConfig: NotRequired[ModelPackageSecurityConfigTypeDef]
    ModelCard: NotRequired[ModelPackageModelCardTypeDef]
    ModelLifeCycle: NotRequired[ModelLifeCycleTypeDef]
    Tags: NotRequired[list[TagTypeDef]]
    CustomerMetadataProperties: NotRequired[dict[str, str]]
    DriftCheckBaselines: NotRequired[DriftCheckBaselinesTypeDef]
    SkipModelValidation: NotRequired[SkipModelValidationType]


ModelPackageValidationSpecificationUnionTypeDef = Union[
    ModelPackageValidationSpecificationTypeDef, ModelPackageValidationSpecificationOutputTypeDef
]


class CreateClusterRequestTypeDef(TypedDict):
    ClusterName: str
    InstanceGroups: NotRequired[Sequence[ClusterInstanceGroupSpecificationTypeDef]]
    RestrictedInstanceGroups: NotRequired[
        Sequence[ClusterRestrictedInstanceGroupSpecificationTypeDef]
    ]
    VpcConfig: NotRequired[VpcConfigUnionTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    Orchestrator: NotRequired[ClusterOrchestratorTypeDef]
    NodeRecovery: NotRequired[ClusterNodeRecoveryType]
    TieredStorageConfig: NotRequired[ClusterTieredStorageConfigTypeDef]
    NodeProvisioningMode: NotRequired[Literal["Continuous"]]
    ClusterRole: NotRequired[str]
    AutoScaling: NotRequired[ClusterAutoScalingConfigTypeDef]


class UpdateClusterRequestTypeDef(TypedDict):
    ClusterName: str
    InstanceGroups: NotRequired[Sequence[ClusterInstanceGroupSpecificationTypeDef]]
    RestrictedInstanceGroups: NotRequired[
        Sequence[ClusterRestrictedInstanceGroupSpecificationTypeDef]
    ]
    TieredStorageConfig: NotRequired[ClusterTieredStorageConfigTypeDef]
    NodeRecovery: NotRequired[ClusterNodeRecoveryType]
    InstanceGroupsToDelete: NotRequired[Sequence[str]]
    NodeProvisioningMode: NotRequired[Literal["Continuous"]]
    ClusterRole: NotRequired[str]
    AutoScaling: NotRequired[ClusterAutoScalingConfigTypeDef]


class DescribeAlgorithmOutputTypeDef(TypedDict):
    AlgorithmName: str
    AlgorithmArn: str
    AlgorithmDescription: str
    CreationTime: datetime
    TrainingSpecification: TrainingSpecificationOutputTypeDef
    InferenceSpecification: InferenceSpecificationOutputTypeDef
    ValidationSpecification: AlgorithmValidationSpecificationOutputTypeDef
    AlgorithmStatus: AlgorithmStatusType
    AlgorithmStatusDetails: AlgorithmStatusDetailsTypeDef
    ProductId: str
    CertifyForMarketplace: bool
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTrainingJobRequestTypeDef(TypedDict):
    TrainingJobName: str
    RoleArn: str
    OutputDataConfig: OutputDataConfigTypeDef
    HyperParameters: NotRequired[Mapping[str, str]]
    AlgorithmSpecification: NotRequired[AlgorithmSpecificationUnionTypeDef]
    InputDataConfig: NotRequired[Sequence[ChannelUnionTypeDef]]
    ResourceConfig: NotRequired[ResourceConfigUnionTypeDef]
    VpcConfig: NotRequired[VpcConfigUnionTypeDef]
    StoppingCondition: NotRequired[StoppingConditionTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    EnableNetworkIsolation: NotRequired[bool]
    EnableInterContainerTrafficEncryption: NotRequired[bool]
    EnableManagedSpotTraining: NotRequired[bool]
    CheckpointConfig: NotRequired[CheckpointConfigTypeDef]
    DebugHookConfig: NotRequired[DebugHookConfigUnionTypeDef]
    DebugRuleConfigurations: NotRequired[Sequence[DebugRuleConfigurationUnionTypeDef]]
    TensorBoardOutputConfig: NotRequired[TensorBoardOutputConfigTypeDef]
    ExperimentConfig: NotRequired[ExperimentConfigTypeDef]
    ProfilerConfig: NotRequired[ProfilerConfigUnionTypeDef]
    ProfilerRuleConfigurations: NotRequired[Sequence[ProfilerRuleConfigurationUnionTypeDef]]
    Environment: NotRequired[Mapping[str, str]]
    RetryStrategy: NotRequired[RetryStrategyTypeDef]
    RemoteDebugConfig: NotRequired[RemoteDebugConfigTypeDef]
    InfraCheckConfig: NotRequired[InfraCheckConfigTypeDef]
    SessionChainingConfig: NotRequired[SessionChainingConfigTypeDef]
    ServerlessJobConfig: NotRequired[ServerlessJobConfigTypeDef]
    MlflowConfig: NotRequired[MlflowConfigTypeDef]
    ModelPackageConfig: NotRequired[ModelPackageConfigTypeDef]


class HyperParameterTrainingJobDefinitionTypeDef(TypedDict):
    AlgorithmSpecification: HyperParameterAlgorithmSpecificationUnionTypeDef
    RoleArn: str
    OutputDataConfig: OutputDataConfigTypeDef
    StoppingCondition: StoppingConditionTypeDef
    DefinitionName: NotRequired[str]
    TuningObjective: NotRequired[HyperParameterTuningJobObjectiveTypeDef]
    HyperParameterRanges: NotRequired[ParameterRangesUnionTypeDef]
    StaticHyperParameters: NotRequired[Mapping[str, str]]
    InputDataConfig: NotRequired[Sequence[ChannelUnionTypeDef]]
    VpcConfig: NotRequired[VpcConfigUnionTypeDef]
    ResourceConfig: NotRequired[ResourceConfigUnionTypeDef]
    HyperParameterTuningResourceConfig: NotRequired[HyperParameterTuningResourceConfigUnionTypeDef]
    EnableNetworkIsolation: NotRequired[bool]
    EnableInterContainerTrafficEncryption: NotRequired[bool]
    EnableManagedSpotTraining: NotRequired[bool]
    CheckpointConfig: NotRequired[CheckpointConfigTypeDef]
    RetryStrategy: NotRequired[RetryStrategyTypeDef]
    Environment: NotRequired[Mapping[str, str]]


class AlgorithmValidationProfileTypeDef(TypedDict):
    ProfileName: str
    TrainingJobDefinition: TrainingJobDefinitionTypeDef
    TransformJobDefinition: NotRequired[TransformJobDefinitionTypeDef]


class UpdateModelPackageInputTypeDef(TypedDict):
    ModelPackageArn: str
    ModelApprovalStatus: NotRequired[ModelApprovalStatusType]
    ModelPackageRegistrationType: NotRequired[ModelPackageRegistrationTypeType]
    ApprovalDescription: NotRequired[str]
    CustomerMetadataProperties: NotRequired[Mapping[str, str]]
    CustomerMetadataPropertiesToRemove: NotRequired[Sequence[str]]
    AdditionalInferenceSpecificationsToAdd: NotRequired[
        Sequence[AdditionalInferenceSpecificationDefinitionUnionTypeDef]
    ]
    InferenceSpecification: NotRequired[InferenceSpecificationUnionTypeDef]
    SourceUri: NotRequired[str]
    ModelCard: NotRequired[ModelPackageModelCardTypeDef]
    ModelLifeCycle: NotRequired[ModelLifeCycleTypeDef]
    ClientToken: NotRequired[str]


class ModelDashboardModelTypeDef(TypedDict):
    Model: NotRequired[ModelTypeDef]
    Endpoints: NotRequired[list[ModelDashboardEndpointTypeDef]]
    LastBatchTransformJob: NotRequired[TransformJobTypeDef]
    MonitoringSchedules: NotRequired[list[ModelDashboardMonitoringScheduleTypeDef]]
    ModelCard: NotRequired[ModelDashboardModelCardTypeDef]


class EndpointTypeDef(TypedDict):
    EndpointName: str
    EndpointArn: str
    EndpointConfigName: str
    EndpointStatus: EndpointStatusType
    CreationTime: datetime
    LastModifiedTime: datetime
    ProductionVariants: NotRequired[list[ProductionVariantSummaryTypeDef]]
    DataCaptureConfig: NotRequired[DataCaptureConfigSummaryTypeDef]
    FailureReason: NotRequired[str]
    MonitoringSchedules: NotRequired[list[MonitoringScheduleTypeDef]]
    Tags: NotRequired[list[TagTypeDef]]
    ShadowProductionVariants: NotRequired[list[ProductionVariantSummaryTypeDef]]


class CreateMonitoringScheduleRequestTypeDef(TypedDict):
    MonitoringScheduleName: str
    MonitoringScheduleConfig: MonitoringScheduleConfigUnionTypeDef
    Tags: NotRequired[Sequence[TagTypeDef]]


class UpdateMonitoringScheduleRequestTypeDef(TypedDict):
    MonitoringScheduleName: str
    MonitoringScheduleConfig: MonitoringScheduleConfigUnionTypeDef


class CreateModelPackageInputTypeDef(TypedDict):
    ModelPackageName: NotRequired[str]
    ModelPackageGroupName: NotRequired[str]
    ModelPackageDescription: NotRequired[str]
    ModelPackageRegistrationType: NotRequired[ModelPackageRegistrationTypeType]
    InferenceSpecification: NotRequired[InferenceSpecificationUnionTypeDef]
    ValidationSpecification: NotRequired[ModelPackageValidationSpecificationUnionTypeDef]
    SourceAlgorithmSpecification: NotRequired[SourceAlgorithmSpecificationUnionTypeDef]
    CertifyForMarketplace: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]
    ModelApprovalStatus: NotRequired[ModelApprovalStatusType]
    MetadataProperties: NotRequired[MetadataPropertiesTypeDef]
    ModelMetrics: NotRequired[ModelMetricsTypeDef]
    ClientToken: NotRequired[str]
    Domain: NotRequired[str]
    Task: NotRequired[str]
    SamplePayloadUrl: NotRequired[str]
    CustomerMetadataProperties: NotRequired[Mapping[str, str]]
    DriftCheckBaselines: NotRequired[DriftCheckBaselinesTypeDef]
    AdditionalInferenceSpecifications: NotRequired[
        Sequence[AdditionalInferenceSpecificationDefinitionUnionTypeDef]
    ]
    SkipModelValidation: NotRequired[SkipModelValidationType]
    SourceUri: NotRequired[str]
    SecurityConfig: NotRequired[ModelPackageSecurityConfigTypeDef]
    ModelCard: NotRequired[ModelPackageModelCardTypeDef]
    ModelLifeCycle: NotRequired[ModelLifeCycleTypeDef]


HyperParameterTrainingJobDefinitionUnionTypeDef = Union[
    HyperParameterTrainingJobDefinitionTypeDef, HyperParameterTrainingJobDefinitionOutputTypeDef
]


class AlgorithmValidationSpecificationTypeDef(TypedDict):
    ValidationRole: str
    ValidationProfiles: Sequence[AlgorithmValidationProfileTypeDef]


class SearchRecordTypeDef(TypedDict):
    TrainingJob: NotRequired[TrainingJobTypeDef]
    Experiment: NotRequired[ExperimentTypeDef]
    Trial: NotRequired[TrialTypeDef]
    TrialComponent: NotRequired[TrialComponentTypeDef]
    Endpoint: NotRequired[EndpointTypeDef]
    ModelPackage: NotRequired[ModelPackageTypeDef]
    ModelPackageGroup: NotRequired[ModelPackageGroupTypeDef]
    Pipeline: NotRequired[PipelineTypeDef]
    PipelineExecution: NotRequired[PipelineExecutionTypeDef]
    PipelineVersion: NotRequired[PipelineVersionTypeDef]
    FeatureGroup: NotRequired[FeatureGroupTypeDef]
    FeatureMetadata: NotRequired[FeatureMetadataTypeDef]
    Project: NotRequired[ProjectTypeDef]
    HyperParameterTuningJob: NotRequired[HyperParameterTuningJobSearchEntityTypeDef]
    ModelCard: NotRequired[ModelCardTypeDef]
    Model: NotRequired[ModelDashboardModelTypeDef]


class CreateHyperParameterTuningJobRequestTypeDef(TypedDict):
    HyperParameterTuningJobName: str
    HyperParameterTuningJobConfig: HyperParameterTuningJobConfigUnionTypeDef
    TrainingJobDefinition: NotRequired[HyperParameterTrainingJobDefinitionUnionTypeDef]
    TrainingJobDefinitions: NotRequired[Sequence[HyperParameterTrainingJobDefinitionUnionTypeDef]]
    WarmStartConfig: NotRequired[HyperParameterTuningJobWarmStartConfigUnionTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    Autotune: NotRequired[AutotuneTypeDef]


AlgorithmValidationSpecificationUnionTypeDef = Union[
    AlgorithmValidationSpecificationTypeDef, AlgorithmValidationSpecificationOutputTypeDef
]


class SearchResponseTypeDef(TypedDict):
    Results: list[SearchRecordTypeDef]
    TotalHits: TotalHitsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateAlgorithmInputTypeDef(TypedDict):
    AlgorithmName: str
    TrainingSpecification: TrainingSpecificationUnionTypeDef
    AlgorithmDescription: NotRequired[str]
    InferenceSpecification: NotRequired[InferenceSpecificationUnionTypeDef]
    ValidationSpecification: NotRequired[AlgorithmValidationSpecificationUnionTypeDef]
    CertifyForMarketplace: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]
