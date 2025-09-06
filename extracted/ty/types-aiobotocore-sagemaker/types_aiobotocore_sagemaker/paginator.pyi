"""
Type annotations for sagemaker service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sagemaker.client import SageMakerClient
    from types_aiobotocore_sagemaker.paginator import (
        CreateHubContentPresignedUrlsPaginator,
        ListActionsPaginator,
        ListAlgorithmsPaginator,
        ListAliasesPaginator,
        ListAppImageConfigsPaginator,
        ListAppsPaginator,
        ListArtifactsPaginator,
        ListAssociationsPaginator,
        ListAutoMLJobsPaginator,
        ListCandidatesForAutoMLJobPaginator,
        ListClusterEventsPaginator,
        ListClusterNodesPaginator,
        ListClusterSchedulerConfigsPaginator,
        ListClustersPaginator,
        ListCodeRepositoriesPaginator,
        ListCompilationJobsPaginator,
        ListComputeQuotasPaginator,
        ListContextsPaginator,
        ListDataQualityJobDefinitionsPaginator,
        ListDeviceFleetsPaginator,
        ListDevicesPaginator,
        ListDomainsPaginator,
        ListEdgeDeploymentPlansPaginator,
        ListEdgePackagingJobsPaginator,
        ListEndpointConfigsPaginator,
        ListEndpointsPaginator,
        ListExperimentsPaginator,
        ListFeatureGroupsPaginator,
        ListFlowDefinitionsPaginator,
        ListHumanTaskUisPaginator,
        ListHyperParameterTuningJobsPaginator,
        ListImageVersionsPaginator,
        ListImagesPaginator,
        ListInferenceComponentsPaginator,
        ListInferenceExperimentsPaginator,
        ListInferenceRecommendationsJobStepsPaginator,
        ListInferenceRecommendationsJobsPaginator,
        ListLabelingJobsForWorkteamPaginator,
        ListLabelingJobsPaginator,
        ListLineageGroupsPaginator,
        ListMlflowTrackingServersPaginator,
        ListModelBiasJobDefinitionsPaginator,
        ListModelCardExportJobsPaginator,
        ListModelCardVersionsPaginator,
        ListModelCardsPaginator,
        ListModelExplainabilityJobDefinitionsPaginator,
        ListModelMetadataPaginator,
        ListModelPackageGroupsPaginator,
        ListModelPackagesPaginator,
        ListModelQualityJobDefinitionsPaginator,
        ListModelsPaginator,
        ListMonitoringAlertHistoryPaginator,
        ListMonitoringAlertsPaginator,
        ListMonitoringExecutionsPaginator,
        ListMonitoringSchedulesPaginator,
        ListNotebookInstanceLifecycleConfigsPaginator,
        ListNotebookInstancesPaginator,
        ListOptimizationJobsPaginator,
        ListPartnerAppsPaginator,
        ListPipelineExecutionStepsPaginator,
        ListPipelineExecutionsPaginator,
        ListPipelineParametersForExecutionPaginator,
        ListPipelineVersionsPaginator,
        ListPipelinesPaginator,
        ListProcessingJobsPaginator,
        ListResourceCatalogsPaginator,
        ListSpacesPaginator,
        ListStageDevicesPaginator,
        ListStudioLifecycleConfigsPaginator,
        ListSubscribedWorkteamsPaginator,
        ListTagsPaginator,
        ListTrainingJobsForHyperParameterTuningJobPaginator,
        ListTrainingJobsPaginator,
        ListTrainingPlansPaginator,
        ListTransformJobsPaginator,
        ListTrialComponentsPaginator,
        ListTrialsPaginator,
        ListUltraServersByReservedCapacityPaginator,
        ListUserProfilesPaginator,
        ListWorkforcesPaginator,
        ListWorkteamsPaginator,
        SearchPaginator,
    )

    session = get_session()
    with session.create_client("sagemaker") as client:
        client: SageMakerClient

        create_hub_content_presigned_urls_paginator: CreateHubContentPresignedUrlsPaginator = client.get_paginator("create_hub_content_presigned_urls")
        list_actions_paginator: ListActionsPaginator = client.get_paginator("list_actions")
        list_algorithms_paginator: ListAlgorithmsPaginator = client.get_paginator("list_algorithms")
        list_aliases_paginator: ListAliasesPaginator = client.get_paginator("list_aliases")
        list_app_image_configs_paginator: ListAppImageConfigsPaginator = client.get_paginator("list_app_image_configs")
        list_apps_paginator: ListAppsPaginator = client.get_paginator("list_apps")
        list_artifacts_paginator: ListArtifactsPaginator = client.get_paginator("list_artifacts")
        list_associations_paginator: ListAssociationsPaginator = client.get_paginator("list_associations")
        list_auto_ml_jobs_paginator: ListAutoMLJobsPaginator = client.get_paginator("list_auto_ml_jobs")
        list_candidates_for_auto_ml_job_paginator: ListCandidatesForAutoMLJobPaginator = client.get_paginator("list_candidates_for_auto_ml_job")
        list_cluster_events_paginator: ListClusterEventsPaginator = client.get_paginator("list_cluster_events")
        list_cluster_nodes_paginator: ListClusterNodesPaginator = client.get_paginator("list_cluster_nodes")
        list_cluster_scheduler_configs_paginator: ListClusterSchedulerConfigsPaginator = client.get_paginator("list_cluster_scheduler_configs")
        list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
        list_code_repositories_paginator: ListCodeRepositoriesPaginator = client.get_paginator("list_code_repositories")
        list_compilation_jobs_paginator: ListCompilationJobsPaginator = client.get_paginator("list_compilation_jobs")
        list_compute_quotas_paginator: ListComputeQuotasPaginator = client.get_paginator("list_compute_quotas")
        list_contexts_paginator: ListContextsPaginator = client.get_paginator("list_contexts")
        list_data_quality_job_definitions_paginator: ListDataQualityJobDefinitionsPaginator = client.get_paginator("list_data_quality_job_definitions")
        list_device_fleets_paginator: ListDeviceFleetsPaginator = client.get_paginator("list_device_fleets")
        list_devices_paginator: ListDevicesPaginator = client.get_paginator("list_devices")
        list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
        list_edge_deployment_plans_paginator: ListEdgeDeploymentPlansPaginator = client.get_paginator("list_edge_deployment_plans")
        list_edge_packaging_jobs_paginator: ListEdgePackagingJobsPaginator = client.get_paginator("list_edge_packaging_jobs")
        list_endpoint_configs_paginator: ListEndpointConfigsPaginator = client.get_paginator("list_endpoint_configs")
        list_endpoints_paginator: ListEndpointsPaginator = client.get_paginator("list_endpoints")
        list_experiments_paginator: ListExperimentsPaginator = client.get_paginator("list_experiments")
        list_feature_groups_paginator: ListFeatureGroupsPaginator = client.get_paginator("list_feature_groups")
        list_flow_definitions_paginator: ListFlowDefinitionsPaginator = client.get_paginator("list_flow_definitions")
        list_human_task_uis_paginator: ListHumanTaskUisPaginator = client.get_paginator("list_human_task_uis")
        list_hyper_parameter_tuning_jobs_paginator: ListHyperParameterTuningJobsPaginator = client.get_paginator("list_hyper_parameter_tuning_jobs")
        list_image_versions_paginator: ListImageVersionsPaginator = client.get_paginator("list_image_versions")
        list_images_paginator: ListImagesPaginator = client.get_paginator("list_images")
        list_inference_components_paginator: ListInferenceComponentsPaginator = client.get_paginator("list_inference_components")
        list_inference_experiments_paginator: ListInferenceExperimentsPaginator = client.get_paginator("list_inference_experiments")
        list_inference_recommendations_job_steps_paginator: ListInferenceRecommendationsJobStepsPaginator = client.get_paginator("list_inference_recommendations_job_steps")
        list_inference_recommendations_jobs_paginator: ListInferenceRecommendationsJobsPaginator = client.get_paginator("list_inference_recommendations_jobs")
        list_labeling_jobs_for_workteam_paginator: ListLabelingJobsForWorkteamPaginator = client.get_paginator("list_labeling_jobs_for_workteam")
        list_labeling_jobs_paginator: ListLabelingJobsPaginator = client.get_paginator("list_labeling_jobs")
        list_lineage_groups_paginator: ListLineageGroupsPaginator = client.get_paginator("list_lineage_groups")
        list_mlflow_tracking_servers_paginator: ListMlflowTrackingServersPaginator = client.get_paginator("list_mlflow_tracking_servers")
        list_model_bias_job_definitions_paginator: ListModelBiasJobDefinitionsPaginator = client.get_paginator("list_model_bias_job_definitions")
        list_model_card_export_jobs_paginator: ListModelCardExportJobsPaginator = client.get_paginator("list_model_card_export_jobs")
        list_model_card_versions_paginator: ListModelCardVersionsPaginator = client.get_paginator("list_model_card_versions")
        list_model_cards_paginator: ListModelCardsPaginator = client.get_paginator("list_model_cards")
        list_model_explainability_job_definitions_paginator: ListModelExplainabilityJobDefinitionsPaginator = client.get_paginator("list_model_explainability_job_definitions")
        list_model_metadata_paginator: ListModelMetadataPaginator = client.get_paginator("list_model_metadata")
        list_model_package_groups_paginator: ListModelPackageGroupsPaginator = client.get_paginator("list_model_package_groups")
        list_model_packages_paginator: ListModelPackagesPaginator = client.get_paginator("list_model_packages")
        list_model_quality_job_definitions_paginator: ListModelQualityJobDefinitionsPaginator = client.get_paginator("list_model_quality_job_definitions")
        list_models_paginator: ListModelsPaginator = client.get_paginator("list_models")
        list_monitoring_alert_history_paginator: ListMonitoringAlertHistoryPaginator = client.get_paginator("list_monitoring_alert_history")
        list_monitoring_alerts_paginator: ListMonitoringAlertsPaginator = client.get_paginator("list_monitoring_alerts")
        list_monitoring_executions_paginator: ListMonitoringExecutionsPaginator = client.get_paginator("list_monitoring_executions")
        list_monitoring_schedules_paginator: ListMonitoringSchedulesPaginator = client.get_paginator("list_monitoring_schedules")
        list_notebook_instance_lifecycle_configs_paginator: ListNotebookInstanceLifecycleConfigsPaginator = client.get_paginator("list_notebook_instance_lifecycle_configs")
        list_notebook_instances_paginator: ListNotebookInstancesPaginator = client.get_paginator("list_notebook_instances")
        list_optimization_jobs_paginator: ListOptimizationJobsPaginator = client.get_paginator("list_optimization_jobs")
        list_partner_apps_paginator: ListPartnerAppsPaginator = client.get_paginator("list_partner_apps")
        list_pipeline_execution_steps_paginator: ListPipelineExecutionStepsPaginator = client.get_paginator("list_pipeline_execution_steps")
        list_pipeline_executions_paginator: ListPipelineExecutionsPaginator = client.get_paginator("list_pipeline_executions")
        list_pipeline_parameters_for_execution_paginator: ListPipelineParametersForExecutionPaginator = client.get_paginator("list_pipeline_parameters_for_execution")
        list_pipeline_versions_paginator: ListPipelineVersionsPaginator = client.get_paginator("list_pipeline_versions")
        list_pipelines_paginator: ListPipelinesPaginator = client.get_paginator("list_pipelines")
        list_processing_jobs_paginator: ListProcessingJobsPaginator = client.get_paginator("list_processing_jobs")
        list_resource_catalogs_paginator: ListResourceCatalogsPaginator = client.get_paginator("list_resource_catalogs")
        list_spaces_paginator: ListSpacesPaginator = client.get_paginator("list_spaces")
        list_stage_devices_paginator: ListStageDevicesPaginator = client.get_paginator("list_stage_devices")
        list_studio_lifecycle_configs_paginator: ListStudioLifecycleConfigsPaginator = client.get_paginator("list_studio_lifecycle_configs")
        list_subscribed_workteams_paginator: ListSubscribedWorkteamsPaginator = client.get_paginator("list_subscribed_workteams")
        list_tags_paginator: ListTagsPaginator = client.get_paginator("list_tags")
        list_training_jobs_for_hyper_parameter_tuning_job_paginator: ListTrainingJobsForHyperParameterTuningJobPaginator = client.get_paginator("list_training_jobs_for_hyper_parameter_tuning_job")
        list_training_jobs_paginator: ListTrainingJobsPaginator = client.get_paginator("list_training_jobs")
        list_training_plans_paginator: ListTrainingPlansPaginator = client.get_paginator("list_training_plans")
        list_transform_jobs_paginator: ListTransformJobsPaginator = client.get_paginator("list_transform_jobs")
        list_trial_components_paginator: ListTrialComponentsPaginator = client.get_paginator("list_trial_components")
        list_trials_paginator: ListTrialsPaginator = client.get_paginator("list_trials")
        list_ultra_servers_by_reserved_capacity_paginator: ListUltraServersByReservedCapacityPaginator = client.get_paginator("list_ultra_servers_by_reserved_capacity")
        list_user_profiles_paginator: ListUserProfilesPaginator = client.get_paginator("list_user_profiles")
        list_workforces_paginator: ListWorkforcesPaginator = client.get_paginator("list_workforces")
        list_workteams_paginator: ListWorkteamsPaginator = client.get_paginator("list_workteams")
        search_paginator: SearchPaginator = client.get_paginator("search")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    CreateHubContentPresignedUrlsRequestPaginateTypeDef,
    CreateHubContentPresignedUrlsResponseTypeDef,
    ListActionsRequestPaginateTypeDef,
    ListActionsResponseTypeDef,
    ListAlgorithmsInputPaginateTypeDef,
    ListAlgorithmsOutputTypeDef,
    ListAliasesRequestPaginateTypeDef,
    ListAliasesResponseTypeDef,
    ListAppImageConfigsRequestPaginateTypeDef,
    ListAppImageConfigsResponseTypeDef,
    ListAppsRequestPaginateTypeDef,
    ListAppsResponseTypeDef,
    ListArtifactsRequestPaginateTypeDef,
    ListArtifactsResponseTypeDef,
    ListAssociationsRequestPaginateTypeDef,
    ListAssociationsResponseTypeDef,
    ListAutoMLJobsRequestPaginateTypeDef,
    ListAutoMLJobsResponseTypeDef,
    ListCandidatesForAutoMLJobRequestPaginateTypeDef,
    ListCandidatesForAutoMLJobResponseTypeDef,
    ListClusterEventsRequestPaginateTypeDef,
    ListClusterEventsResponseTypeDef,
    ListClusterNodesRequestPaginateTypeDef,
    ListClusterNodesResponseTypeDef,
    ListClusterSchedulerConfigsRequestPaginateTypeDef,
    ListClusterSchedulerConfigsResponseTypeDef,
    ListClustersRequestPaginateTypeDef,
    ListClustersResponseTypeDef,
    ListCodeRepositoriesInputPaginateTypeDef,
    ListCodeRepositoriesOutputTypeDef,
    ListCompilationJobsRequestPaginateTypeDef,
    ListCompilationJobsResponseTypeDef,
    ListComputeQuotasRequestPaginateTypeDef,
    ListComputeQuotasResponseTypeDef,
    ListContextsRequestPaginateTypeDef,
    ListContextsResponseTypeDef,
    ListDataQualityJobDefinitionsRequestPaginateTypeDef,
    ListDataQualityJobDefinitionsResponseTypeDef,
    ListDeviceFleetsRequestPaginateTypeDef,
    ListDeviceFleetsResponseTypeDef,
    ListDevicesRequestPaginateTypeDef,
    ListDevicesResponseTypeDef,
    ListDomainsRequestPaginateTypeDef,
    ListDomainsResponseTypeDef,
    ListEdgeDeploymentPlansRequestPaginateTypeDef,
    ListEdgeDeploymentPlansResponseTypeDef,
    ListEdgePackagingJobsRequestPaginateTypeDef,
    ListEdgePackagingJobsResponseTypeDef,
    ListEndpointConfigsInputPaginateTypeDef,
    ListEndpointConfigsOutputTypeDef,
    ListEndpointsInputPaginateTypeDef,
    ListEndpointsOutputTypeDef,
    ListExperimentsRequestPaginateTypeDef,
    ListExperimentsResponseTypeDef,
    ListFeatureGroupsRequestPaginateTypeDef,
    ListFeatureGroupsResponseTypeDef,
    ListFlowDefinitionsRequestPaginateTypeDef,
    ListFlowDefinitionsResponseTypeDef,
    ListHumanTaskUisRequestPaginateTypeDef,
    ListHumanTaskUisResponseTypeDef,
    ListHyperParameterTuningJobsRequestPaginateTypeDef,
    ListHyperParameterTuningJobsResponseTypeDef,
    ListImagesRequestPaginateTypeDef,
    ListImagesResponseTypeDef,
    ListImageVersionsRequestPaginateTypeDef,
    ListImageVersionsResponseTypeDef,
    ListInferenceComponentsInputPaginateTypeDef,
    ListInferenceComponentsOutputTypeDef,
    ListInferenceExperimentsRequestPaginateTypeDef,
    ListInferenceExperimentsResponseTypeDef,
    ListInferenceRecommendationsJobsRequestPaginateTypeDef,
    ListInferenceRecommendationsJobsResponseTypeDef,
    ListInferenceRecommendationsJobStepsRequestPaginateTypeDef,
    ListInferenceRecommendationsJobStepsResponseTypeDef,
    ListLabelingJobsForWorkteamRequestPaginateTypeDef,
    ListLabelingJobsForWorkteamResponseTypeDef,
    ListLabelingJobsRequestPaginateTypeDef,
    ListLabelingJobsResponseTypeDef,
    ListLineageGroupsRequestPaginateTypeDef,
    ListLineageGroupsResponseTypeDef,
    ListMlflowTrackingServersRequestPaginateTypeDef,
    ListMlflowTrackingServersResponseTypeDef,
    ListModelBiasJobDefinitionsRequestPaginateTypeDef,
    ListModelBiasJobDefinitionsResponseTypeDef,
    ListModelCardExportJobsRequestPaginateTypeDef,
    ListModelCardExportJobsResponseTypeDef,
    ListModelCardsRequestPaginateTypeDef,
    ListModelCardsResponseTypeDef,
    ListModelCardVersionsRequestPaginateTypeDef,
    ListModelCardVersionsResponseTypeDef,
    ListModelExplainabilityJobDefinitionsRequestPaginateTypeDef,
    ListModelExplainabilityJobDefinitionsResponseTypeDef,
    ListModelMetadataRequestPaginateTypeDef,
    ListModelMetadataResponseTypeDef,
    ListModelPackageGroupsInputPaginateTypeDef,
    ListModelPackageGroupsOutputTypeDef,
    ListModelPackagesInputPaginateTypeDef,
    ListModelPackagesOutputTypeDef,
    ListModelQualityJobDefinitionsRequestPaginateTypeDef,
    ListModelQualityJobDefinitionsResponseTypeDef,
    ListModelsInputPaginateTypeDef,
    ListModelsOutputTypeDef,
    ListMonitoringAlertHistoryRequestPaginateTypeDef,
    ListMonitoringAlertHistoryResponseTypeDef,
    ListMonitoringAlertsRequestPaginateTypeDef,
    ListMonitoringAlertsResponseTypeDef,
    ListMonitoringExecutionsRequestPaginateTypeDef,
    ListMonitoringExecutionsResponseTypeDef,
    ListMonitoringSchedulesRequestPaginateTypeDef,
    ListMonitoringSchedulesResponseTypeDef,
    ListNotebookInstanceLifecycleConfigsInputPaginateTypeDef,
    ListNotebookInstanceLifecycleConfigsOutputTypeDef,
    ListNotebookInstancesInputPaginateTypeDef,
    ListNotebookInstancesOutputTypeDef,
    ListOptimizationJobsRequestPaginateTypeDef,
    ListOptimizationJobsResponseTypeDef,
    ListPartnerAppsRequestPaginateTypeDef,
    ListPartnerAppsResponseTypeDef,
    ListPipelineExecutionsRequestPaginateTypeDef,
    ListPipelineExecutionsResponseTypeDef,
    ListPipelineExecutionStepsRequestPaginateTypeDef,
    ListPipelineExecutionStepsResponseTypeDef,
    ListPipelineParametersForExecutionRequestPaginateTypeDef,
    ListPipelineParametersForExecutionResponseTypeDef,
    ListPipelinesRequestPaginateTypeDef,
    ListPipelinesResponseTypeDef,
    ListPipelineVersionsRequestPaginateTypeDef,
    ListPipelineVersionsResponseTypeDef,
    ListProcessingJobsRequestPaginateTypeDef,
    ListProcessingJobsResponseTypeDef,
    ListResourceCatalogsRequestPaginateTypeDef,
    ListResourceCatalogsResponseTypeDef,
    ListSpacesRequestPaginateTypeDef,
    ListSpacesResponseTypeDef,
    ListStageDevicesRequestPaginateTypeDef,
    ListStageDevicesResponseTypeDef,
    ListStudioLifecycleConfigsRequestPaginateTypeDef,
    ListStudioLifecycleConfigsResponseTypeDef,
    ListSubscribedWorkteamsRequestPaginateTypeDef,
    ListSubscribedWorkteamsResponseTypeDef,
    ListTagsInputPaginateTypeDef,
    ListTagsOutputTypeDef,
    ListTrainingJobsForHyperParameterTuningJobRequestPaginateTypeDef,
    ListTrainingJobsForHyperParameterTuningJobResponseTypeDef,
    ListTrainingJobsRequestPaginateTypeDef,
    ListTrainingJobsResponseTypeDef,
    ListTrainingPlansRequestPaginateTypeDef,
    ListTrainingPlansResponseTypeDef,
    ListTransformJobsRequestPaginateTypeDef,
    ListTransformJobsResponseTypeDef,
    ListTrialComponentsRequestPaginateTypeDef,
    ListTrialComponentsResponseTypeDef,
    ListTrialsRequestPaginateTypeDef,
    ListTrialsResponseTypeDef,
    ListUltraServersByReservedCapacityRequestPaginateTypeDef,
    ListUltraServersByReservedCapacityResponseTypeDef,
    ListUserProfilesRequestPaginateTypeDef,
    ListUserProfilesResponseTypeDef,
    ListWorkforcesRequestPaginateTypeDef,
    ListWorkforcesResponseTypeDef,
    ListWorkteamsRequestPaginateTypeDef,
    ListWorkteamsResponseTypeDef,
    SearchRequestPaginateTypeDef,
    SearchResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "CreateHubContentPresignedUrlsPaginator",
    "ListActionsPaginator",
    "ListAlgorithmsPaginator",
    "ListAliasesPaginator",
    "ListAppImageConfigsPaginator",
    "ListAppsPaginator",
    "ListArtifactsPaginator",
    "ListAssociationsPaginator",
    "ListAutoMLJobsPaginator",
    "ListCandidatesForAutoMLJobPaginator",
    "ListClusterEventsPaginator",
    "ListClusterNodesPaginator",
    "ListClusterSchedulerConfigsPaginator",
    "ListClustersPaginator",
    "ListCodeRepositoriesPaginator",
    "ListCompilationJobsPaginator",
    "ListComputeQuotasPaginator",
    "ListContextsPaginator",
    "ListDataQualityJobDefinitionsPaginator",
    "ListDeviceFleetsPaginator",
    "ListDevicesPaginator",
    "ListDomainsPaginator",
    "ListEdgeDeploymentPlansPaginator",
    "ListEdgePackagingJobsPaginator",
    "ListEndpointConfigsPaginator",
    "ListEndpointsPaginator",
    "ListExperimentsPaginator",
    "ListFeatureGroupsPaginator",
    "ListFlowDefinitionsPaginator",
    "ListHumanTaskUisPaginator",
    "ListHyperParameterTuningJobsPaginator",
    "ListImageVersionsPaginator",
    "ListImagesPaginator",
    "ListInferenceComponentsPaginator",
    "ListInferenceExperimentsPaginator",
    "ListInferenceRecommendationsJobStepsPaginator",
    "ListInferenceRecommendationsJobsPaginator",
    "ListLabelingJobsForWorkteamPaginator",
    "ListLabelingJobsPaginator",
    "ListLineageGroupsPaginator",
    "ListMlflowTrackingServersPaginator",
    "ListModelBiasJobDefinitionsPaginator",
    "ListModelCardExportJobsPaginator",
    "ListModelCardVersionsPaginator",
    "ListModelCardsPaginator",
    "ListModelExplainabilityJobDefinitionsPaginator",
    "ListModelMetadataPaginator",
    "ListModelPackageGroupsPaginator",
    "ListModelPackagesPaginator",
    "ListModelQualityJobDefinitionsPaginator",
    "ListModelsPaginator",
    "ListMonitoringAlertHistoryPaginator",
    "ListMonitoringAlertsPaginator",
    "ListMonitoringExecutionsPaginator",
    "ListMonitoringSchedulesPaginator",
    "ListNotebookInstanceLifecycleConfigsPaginator",
    "ListNotebookInstancesPaginator",
    "ListOptimizationJobsPaginator",
    "ListPartnerAppsPaginator",
    "ListPipelineExecutionStepsPaginator",
    "ListPipelineExecutionsPaginator",
    "ListPipelineParametersForExecutionPaginator",
    "ListPipelineVersionsPaginator",
    "ListPipelinesPaginator",
    "ListProcessingJobsPaginator",
    "ListResourceCatalogsPaginator",
    "ListSpacesPaginator",
    "ListStageDevicesPaginator",
    "ListStudioLifecycleConfigsPaginator",
    "ListSubscribedWorkteamsPaginator",
    "ListTagsPaginator",
    "ListTrainingJobsForHyperParameterTuningJobPaginator",
    "ListTrainingJobsPaginator",
    "ListTrainingPlansPaginator",
    "ListTransformJobsPaginator",
    "ListTrialComponentsPaginator",
    "ListTrialsPaginator",
    "ListUltraServersByReservedCapacityPaginator",
    "ListUserProfilesPaginator",
    "ListWorkforcesPaginator",
    "ListWorkteamsPaginator",
    "SearchPaginator",
)

if TYPE_CHECKING:
    _CreateHubContentPresignedUrlsPaginatorBase = AioPaginator[
        CreateHubContentPresignedUrlsResponseTypeDef
    ]
else:
    _CreateHubContentPresignedUrlsPaginatorBase = AioPaginator  # type: ignore[assignment]

class CreateHubContentPresignedUrlsPaginator(_CreateHubContentPresignedUrlsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/CreateHubContentPresignedUrls.html#SageMaker.Paginator.CreateHubContentPresignedUrls)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#createhubcontentpresignedurlspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[CreateHubContentPresignedUrlsRequestPaginateTypeDef]
    ) -> AioPageIterator[CreateHubContentPresignedUrlsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/CreateHubContentPresignedUrls.html#SageMaker.Paginator.CreateHubContentPresignedUrls.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#createhubcontentpresignedurlspaginator)
        """

if TYPE_CHECKING:
    _ListActionsPaginatorBase = AioPaginator[ListActionsResponseTypeDef]
else:
    _ListActionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListActionsPaginator(_ListActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListActions.html#SageMaker.Paginator.ListActions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listactionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListActionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListActions.html#SageMaker.Paginator.ListActions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listactionspaginator)
        """

if TYPE_CHECKING:
    _ListAlgorithmsPaginatorBase = AioPaginator[ListAlgorithmsOutputTypeDef]
else:
    _ListAlgorithmsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAlgorithmsPaginator(_ListAlgorithmsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAlgorithms.html#SageMaker.Paginator.ListAlgorithms)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listalgorithmspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAlgorithmsInputPaginateTypeDef]
    ) -> AioPageIterator[ListAlgorithmsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAlgorithms.html#SageMaker.Paginator.ListAlgorithms.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listalgorithmspaginator)
        """

if TYPE_CHECKING:
    _ListAliasesPaginatorBase = AioPaginator[ListAliasesResponseTypeDef]
else:
    _ListAliasesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAliasesPaginator(_ListAliasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAliases.html#SageMaker.Paginator.ListAliases)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listaliasespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAliasesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAliases.html#SageMaker.Paginator.ListAliases.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listaliasespaginator)
        """

if TYPE_CHECKING:
    _ListAppImageConfigsPaginatorBase = AioPaginator[ListAppImageConfigsResponseTypeDef]
else:
    _ListAppImageConfigsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAppImageConfigsPaginator(_ListAppImageConfigsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAppImageConfigs.html#SageMaker.Paginator.ListAppImageConfigs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listappimageconfigspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAppImageConfigsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAppImageConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAppImageConfigs.html#SageMaker.Paginator.ListAppImageConfigs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listappimageconfigspaginator)
        """

if TYPE_CHECKING:
    _ListAppsPaginatorBase = AioPaginator[ListAppsResponseTypeDef]
else:
    _ListAppsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAppsPaginator(_ListAppsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListApps.html#SageMaker.Paginator.ListApps)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listappspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAppsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAppsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListApps.html#SageMaker.Paginator.ListApps.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listappspaginator)
        """

if TYPE_CHECKING:
    _ListArtifactsPaginatorBase = AioPaginator[ListArtifactsResponseTypeDef]
else:
    _ListArtifactsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListArtifactsPaginator(_ListArtifactsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListArtifacts.html#SageMaker.Paginator.ListArtifacts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listartifactspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListArtifactsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListArtifactsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListArtifacts.html#SageMaker.Paginator.ListArtifacts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listartifactspaginator)
        """

if TYPE_CHECKING:
    _ListAssociationsPaginatorBase = AioPaginator[ListAssociationsResponseTypeDef]
else:
    _ListAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAssociationsPaginator(_ListAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAssociations.html#SageMaker.Paginator.ListAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAssociations.html#SageMaker.Paginator.ListAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listassociationspaginator)
        """

if TYPE_CHECKING:
    _ListAutoMLJobsPaginatorBase = AioPaginator[ListAutoMLJobsResponseTypeDef]
else:
    _ListAutoMLJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAutoMLJobsPaginator(_ListAutoMLJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAutoMLJobs.html#SageMaker.Paginator.ListAutoMLJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listautomljobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAutoMLJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAutoMLJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAutoMLJobs.html#SageMaker.Paginator.ListAutoMLJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listautomljobspaginator)
        """

if TYPE_CHECKING:
    _ListCandidatesForAutoMLJobPaginatorBase = AioPaginator[
        ListCandidatesForAutoMLJobResponseTypeDef
    ]
else:
    _ListCandidatesForAutoMLJobPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCandidatesForAutoMLJobPaginator(_ListCandidatesForAutoMLJobPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListCandidatesForAutoMLJob.html#SageMaker.Paginator.ListCandidatesForAutoMLJob)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcandidatesforautomljobpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCandidatesForAutoMLJobRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCandidatesForAutoMLJobResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListCandidatesForAutoMLJob.html#SageMaker.Paginator.ListCandidatesForAutoMLJob.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcandidatesforautomljobpaginator)
        """

if TYPE_CHECKING:
    _ListClusterEventsPaginatorBase = AioPaginator[ListClusterEventsResponseTypeDef]
else:
    _ListClusterEventsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListClusterEventsPaginator(_ListClusterEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListClusterEvents.html#SageMaker.Paginator.ListClusterEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listclustereventspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListClusterEventsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListClusterEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListClusterEvents.html#SageMaker.Paginator.ListClusterEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listclustereventspaginator)
        """

if TYPE_CHECKING:
    _ListClusterNodesPaginatorBase = AioPaginator[ListClusterNodesResponseTypeDef]
else:
    _ListClusterNodesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListClusterNodesPaginator(_ListClusterNodesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListClusterNodes.html#SageMaker.Paginator.ListClusterNodes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listclusternodespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListClusterNodesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListClusterNodesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListClusterNodes.html#SageMaker.Paginator.ListClusterNodes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listclusternodespaginator)
        """

if TYPE_CHECKING:
    _ListClusterSchedulerConfigsPaginatorBase = AioPaginator[
        ListClusterSchedulerConfigsResponseTypeDef
    ]
else:
    _ListClusterSchedulerConfigsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListClusterSchedulerConfigsPaginator(_ListClusterSchedulerConfigsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListClusterSchedulerConfigs.html#SageMaker.Paginator.ListClusterSchedulerConfigs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listclusterschedulerconfigspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListClusterSchedulerConfigsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListClusterSchedulerConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListClusterSchedulerConfigs.html#SageMaker.Paginator.ListClusterSchedulerConfigs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listclusterschedulerconfigspaginator)
        """

if TYPE_CHECKING:
    _ListClustersPaginatorBase = AioPaginator[ListClustersResponseTypeDef]
else:
    _ListClustersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListClustersPaginator(_ListClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListClusters.html#SageMaker.Paginator.ListClusters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listclusterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListClustersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListClusters.html#SageMaker.Paginator.ListClusters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listclusterspaginator)
        """

if TYPE_CHECKING:
    _ListCodeRepositoriesPaginatorBase = AioPaginator[ListCodeRepositoriesOutputTypeDef]
else:
    _ListCodeRepositoriesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCodeRepositoriesPaginator(_ListCodeRepositoriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListCodeRepositories.html#SageMaker.Paginator.ListCodeRepositories)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcoderepositoriespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCodeRepositoriesInputPaginateTypeDef]
    ) -> AioPageIterator[ListCodeRepositoriesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListCodeRepositories.html#SageMaker.Paginator.ListCodeRepositories.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcoderepositoriespaginator)
        """

if TYPE_CHECKING:
    _ListCompilationJobsPaginatorBase = AioPaginator[ListCompilationJobsResponseTypeDef]
else:
    _ListCompilationJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCompilationJobsPaginator(_ListCompilationJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListCompilationJobs.html#SageMaker.Paginator.ListCompilationJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcompilationjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCompilationJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCompilationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListCompilationJobs.html#SageMaker.Paginator.ListCompilationJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcompilationjobspaginator)
        """

if TYPE_CHECKING:
    _ListComputeQuotasPaginatorBase = AioPaginator[ListComputeQuotasResponseTypeDef]
else:
    _ListComputeQuotasPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListComputeQuotasPaginator(_ListComputeQuotasPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListComputeQuotas.html#SageMaker.Paginator.ListComputeQuotas)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcomputequotaspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListComputeQuotasRequestPaginateTypeDef]
    ) -> AioPageIterator[ListComputeQuotasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListComputeQuotas.html#SageMaker.Paginator.ListComputeQuotas.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcomputequotaspaginator)
        """

if TYPE_CHECKING:
    _ListContextsPaginatorBase = AioPaginator[ListContextsResponseTypeDef]
else:
    _ListContextsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListContextsPaginator(_ListContextsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListContexts.html#SageMaker.Paginator.ListContexts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcontextspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListContextsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListContextsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListContexts.html#SageMaker.Paginator.ListContexts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listcontextspaginator)
        """

if TYPE_CHECKING:
    _ListDataQualityJobDefinitionsPaginatorBase = AioPaginator[
        ListDataQualityJobDefinitionsResponseTypeDef
    ]
else:
    _ListDataQualityJobDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataQualityJobDefinitionsPaginator(_ListDataQualityJobDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDataQualityJobDefinitions.html#SageMaker.Paginator.ListDataQualityJobDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listdataqualityjobdefinitionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataQualityJobDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataQualityJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDataQualityJobDefinitions.html#SageMaker.Paginator.ListDataQualityJobDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listdataqualityjobdefinitionspaginator)
        """

if TYPE_CHECKING:
    _ListDeviceFleetsPaginatorBase = AioPaginator[ListDeviceFleetsResponseTypeDef]
else:
    _ListDeviceFleetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDeviceFleetsPaginator(_ListDeviceFleetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDeviceFleets.html#SageMaker.Paginator.ListDeviceFleets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listdevicefleetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeviceFleetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDeviceFleetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDeviceFleets.html#SageMaker.Paginator.ListDeviceFleets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listdevicefleetspaginator)
        """

if TYPE_CHECKING:
    _ListDevicesPaginatorBase = AioPaginator[ListDevicesResponseTypeDef]
else:
    _ListDevicesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDevicesPaginator(_ListDevicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDevices.html#SageMaker.Paginator.ListDevices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listdevicespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDevicesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDevices.html#SageMaker.Paginator.ListDevices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listdevicespaginator)
        """

if TYPE_CHECKING:
    _ListDomainsPaginatorBase = AioPaginator[ListDomainsResponseTypeDef]
else:
    _ListDomainsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDomainsPaginator(_ListDomainsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDomains.html#SageMaker.Paginator.ListDomains)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listdomainspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDomainsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDomainsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDomains.html#SageMaker.Paginator.ListDomains.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listdomainspaginator)
        """

if TYPE_CHECKING:
    _ListEdgeDeploymentPlansPaginatorBase = AioPaginator[ListEdgeDeploymentPlansResponseTypeDef]
else:
    _ListEdgeDeploymentPlansPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEdgeDeploymentPlansPaginator(_ListEdgeDeploymentPlansPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEdgeDeploymentPlans.html#SageMaker.Paginator.ListEdgeDeploymentPlans)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listedgedeploymentplanspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEdgeDeploymentPlansRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEdgeDeploymentPlansResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEdgeDeploymentPlans.html#SageMaker.Paginator.ListEdgeDeploymentPlans.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listedgedeploymentplanspaginator)
        """

if TYPE_CHECKING:
    _ListEdgePackagingJobsPaginatorBase = AioPaginator[ListEdgePackagingJobsResponseTypeDef]
else:
    _ListEdgePackagingJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEdgePackagingJobsPaginator(_ListEdgePackagingJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEdgePackagingJobs.html#SageMaker.Paginator.ListEdgePackagingJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listedgepackagingjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEdgePackagingJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEdgePackagingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEdgePackagingJobs.html#SageMaker.Paginator.ListEdgePackagingJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listedgepackagingjobspaginator)
        """

if TYPE_CHECKING:
    _ListEndpointConfigsPaginatorBase = AioPaginator[ListEndpointConfigsOutputTypeDef]
else:
    _ListEndpointConfigsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEndpointConfigsPaginator(_ListEndpointConfigsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEndpointConfigs.html#SageMaker.Paginator.ListEndpointConfigs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listendpointconfigspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEndpointConfigsInputPaginateTypeDef]
    ) -> AioPageIterator[ListEndpointConfigsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEndpointConfigs.html#SageMaker.Paginator.ListEndpointConfigs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listendpointconfigspaginator)
        """

if TYPE_CHECKING:
    _ListEndpointsPaginatorBase = AioPaginator[ListEndpointsOutputTypeDef]
else:
    _ListEndpointsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEndpointsPaginator(_ListEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEndpoints.html#SageMaker.Paginator.ListEndpoints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listendpointspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEndpointsInputPaginateTypeDef]
    ) -> AioPageIterator[ListEndpointsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEndpoints.html#SageMaker.Paginator.ListEndpoints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listendpointspaginator)
        """

if TYPE_CHECKING:
    _ListExperimentsPaginatorBase = AioPaginator[ListExperimentsResponseTypeDef]
else:
    _ListExperimentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListExperimentsPaginator(_ListExperimentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListExperiments.html#SageMaker.Paginator.ListExperiments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listexperimentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExperimentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListExperimentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListExperiments.html#SageMaker.Paginator.ListExperiments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listexperimentspaginator)
        """

if TYPE_CHECKING:
    _ListFeatureGroupsPaginatorBase = AioPaginator[ListFeatureGroupsResponseTypeDef]
else:
    _ListFeatureGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFeatureGroupsPaginator(_ListFeatureGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListFeatureGroups.html#SageMaker.Paginator.ListFeatureGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listfeaturegroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFeatureGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFeatureGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListFeatureGroups.html#SageMaker.Paginator.ListFeatureGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listfeaturegroupspaginator)
        """

if TYPE_CHECKING:
    _ListFlowDefinitionsPaginatorBase = AioPaginator[ListFlowDefinitionsResponseTypeDef]
else:
    _ListFlowDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFlowDefinitionsPaginator(_ListFlowDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListFlowDefinitions.html#SageMaker.Paginator.ListFlowDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listflowdefinitionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFlowDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFlowDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListFlowDefinitions.html#SageMaker.Paginator.ListFlowDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listflowdefinitionspaginator)
        """

if TYPE_CHECKING:
    _ListHumanTaskUisPaginatorBase = AioPaginator[ListHumanTaskUisResponseTypeDef]
else:
    _ListHumanTaskUisPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListHumanTaskUisPaginator(_ListHumanTaskUisPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListHumanTaskUis.html#SageMaker.Paginator.ListHumanTaskUis)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listhumantaskuispaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListHumanTaskUisRequestPaginateTypeDef]
    ) -> AioPageIterator[ListHumanTaskUisResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListHumanTaskUis.html#SageMaker.Paginator.ListHumanTaskUis.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listhumantaskuispaginator)
        """

if TYPE_CHECKING:
    _ListHyperParameterTuningJobsPaginatorBase = AioPaginator[
        ListHyperParameterTuningJobsResponseTypeDef
    ]
else:
    _ListHyperParameterTuningJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListHyperParameterTuningJobsPaginator(_ListHyperParameterTuningJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListHyperParameterTuningJobs.html#SageMaker.Paginator.ListHyperParameterTuningJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listhyperparametertuningjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListHyperParameterTuningJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListHyperParameterTuningJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListHyperParameterTuningJobs.html#SageMaker.Paginator.ListHyperParameterTuningJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listhyperparametertuningjobspaginator)
        """

if TYPE_CHECKING:
    _ListImageVersionsPaginatorBase = AioPaginator[ListImageVersionsResponseTypeDef]
else:
    _ListImageVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListImageVersionsPaginator(_ListImageVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListImageVersions.html#SageMaker.Paginator.ListImageVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listimageversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImageVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListImageVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListImageVersions.html#SageMaker.Paginator.ListImageVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listimageversionspaginator)
        """

if TYPE_CHECKING:
    _ListImagesPaginatorBase = AioPaginator[ListImagesResponseTypeDef]
else:
    _ListImagesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListImagesPaginator(_ListImagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListImages.html#SageMaker.Paginator.ListImages)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listimagespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImagesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListImagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListImages.html#SageMaker.Paginator.ListImages.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listimagespaginator)
        """

if TYPE_CHECKING:
    _ListInferenceComponentsPaginatorBase = AioPaginator[ListInferenceComponentsOutputTypeDef]
else:
    _ListInferenceComponentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListInferenceComponentsPaginator(_ListInferenceComponentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceComponents.html#SageMaker.Paginator.ListInferenceComponents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listinferencecomponentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInferenceComponentsInputPaginateTypeDef]
    ) -> AioPageIterator[ListInferenceComponentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceComponents.html#SageMaker.Paginator.ListInferenceComponents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listinferencecomponentspaginator)
        """

if TYPE_CHECKING:
    _ListInferenceExperimentsPaginatorBase = AioPaginator[ListInferenceExperimentsResponseTypeDef]
else:
    _ListInferenceExperimentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListInferenceExperimentsPaginator(_ListInferenceExperimentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceExperiments.html#SageMaker.Paginator.ListInferenceExperiments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listinferenceexperimentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInferenceExperimentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInferenceExperimentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceExperiments.html#SageMaker.Paginator.ListInferenceExperiments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listinferenceexperimentspaginator)
        """

if TYPE_CHECKING:
    _ListInferenceRecommendationsJobStepsPaginatorBase = AioPaginator[
        ListInferenceRecommendationsJobStepsResponseTypeDef
    ]
else:
    _ListInferenceRecommendationsJobStepsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListInferenceRecommendationsJobStepsPaginator(
    _ListInferenceRecommendationsJobStepsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceRecommendationsJobSteps.html#SageMaker.Paginator.ListInferenceRecommendationsJobSteps)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listinferencerecommendationsjobstepspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInferenceRecommendationsJobStepsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInferenceRecommendationsJobStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceRecommendationsJobSteps.html#SageMaker.Paginator.ListInferenceRecommendationsJobSteps.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listinferencerecommendationsjobstepspaginator)
        """

if TYPE_CHECKING:
    _ListInferenceRecommendationsJobsPaginatorBase = AioPaginator[
        ListInferenceRecommendationsJobsResponseTypeDef
    ]
else:
    _ListInferenceRecommendationsJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListInferenceRecommendationsJobsPaginator(_ListInferenceRecommendationsJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceRecommendationsJobs.html#SageMaker.Paginator.ListInferenceRecommendationsJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listinferencerecommendationsjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInferenceRecommendationsJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInferenceRecommendationsJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceRecommendationsJobs.html#SageMaker.Paginator.ListInferenceRecommendationsJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listinferencerecommendationsjobspaginator)
        """

if TYPE_CHECKING:
    _ListLabelingJobsForWorkteamPaginatorBase = AioPaginator[
        ListLabelingJobsForWorkteamResponseTypeDef
    ]
else:
    _ListLabelingJobsForWorkteamPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListLabelingJobsForWorkteamPaginator(_ListLabelingJobsForWorkteamPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListLabelingJobsForWorkteam.html#SageMaker.Paginator.ListLabelingJobsForWorkteam)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listlabelingjobsforworkteampaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLabelingJobsForWorkteamRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLabelingJobsForWorkteamResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListLabelingJobsForWorkteam.html#SageMaker.Paginator.ListLabelingJobsForWorkteam.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listlabelingjobsforworkteampaginator)
        """

if TYPE_CHECKING:
    _ListLabelingJobsPaginatorBase = AioPaginator[ListLabelingJobsResponseTypeDef]
else:
    _ListLabelingJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListLabelingJobsPaginator(_ListLabelingJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListLabelingJobs.html#SageMaker.Paginator.ListLabelingJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listlabelingjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLabelingJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLabelingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListLabelingJobs.html#SageMaker.Paginator.ListLabelingJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listlabelingjobspaginator)
        """

if TYPE_CHECKING:
    _ListLineageGroupsPaginatorBase = AioPaginator[ListLineageGroupsResponseTypeDef]
else:
    _ListLineageGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListLineageGroupsPaginator(_ListLineageGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListLineageGroups.html#SageMaker.Paginator.ListLineageGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listlineagegroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLineageGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLineageGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListLineageGroups.html#SageMaker.Paginator.ListLineageGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listlineagegroupspaginator)
        """

if TYPE_CHECKING:
    _ListMlflowTrackingServersPaginatorBase = AioPaginator[ListMlflowTrackingServersResponseTypeDef]
else:
    _ListMlflowTrackingServersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMlflowTrackingServersPaginator(_ListMlflowTrackingServersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMlflowTrackingServers.html#SageMaker.Paginator.ListMlflowTrackingServers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmlflowtrackingserverspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMlflowTrackingServersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMlflowTrackingServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMlflowTrackingServers.html#SageMaker.Paginator.ListMlflowTrackingServers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmlflowtrackingserverspaginator)
        """

if TYPE_CHECKING:
    _ListModelBiasJobDefinitionsPaginatorBase = AioPaginator[
        ListModelBiasJobDefinitionsResponseTypeDef
    ]
else:
    _ListModelBiasJobDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListModelBiasJobDefinitionsPaginator(_ListModelBiasJobDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelBiasJobDefinitions.html#SageMaker.Paginator.ListModelBiasJobDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelbiasjobdefinitionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelBiasJobDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListModelBiasJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelBiasJobDefinitions.html#SageMaker.Paginator.ListModelBiasJobDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelbiasjobdefinitionspaginator)
        """

if TYPE_CHECKING:
    _ListModelCardExportJobsPaginatorBase = AioPaginator[ListModelCardExportJobsResponseTypeDef]
else:
    _ListModelCardExportJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListModelCardExportJobsPaginator(_ListModelCardExportJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelCardExportJobs.html#SageMaker.Paginator.ListModelCardExportJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelcardexportjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelCardExportJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListModelCardExportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelCardExportJobs.html#SageMaker.Paginator.ListModelCardExportJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelcardexportjobspaginator)
        """

if TYPE_CHECKING:
    _ListModelCardVersionsPaginatorBase = AioPaginator[ListModelCardVersionsResponseTypeDef]
else:
    _ListModelCardVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListModelCardVersionsPaginator(_ListModelCardVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelCardVersions.html#SageMaker.Paginator.ListModelCardVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelcardversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelCardVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListModelCardVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelCardVersions.html#SageMaker.Paginator.ListModelCardVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelcardversionspaginator)
        """

if TYPE_CHECKING:
    _ListModelCardsPaginatorBase = AioPaginator[ListModelCardsResponseTypeDef]
else:
    _ListModelCardsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListModelCardsPaginator(_ListModelCardsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelCards.html#SageMaker.Paginator.ListModelCards)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelcardspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelCardsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListModelCardsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelCards.html#SageMaker.Paginator.ListModelCards.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelcardspaginator)
        """

if TYPE_CHECKING:
    _ListModelExplainabilityJobDefinitionsPaginatorBase = AioPaginator[
        ListModelExplainabilityJobDefinitionsResponseTypeDef
    ]
else:
    _ListModelExplainabilityJobDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListModelExplainabilityJobDefinitionsPaginator(
    _ListModelExplainabilityJobDefinitionsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelExplainabilityJobDefinitions.html#SageMaker.Paginator.ListModelExplainabilityJobDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelexplainabilityjobdefinitionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelExplainabilityJobDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListModelExplainabilityJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelExplainabilityJobDefinitions.html#SageMaker.Paginator.ListModelExplainabilityJobDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelexplainabilityjobdefinitionspaginator)
        """

if TYPE_CHECKING:
    _ListModelMetadataPaginatorBase = AioPaginator[ListModelMetadataResponseTypeDef]
else:
    _ListModelMetadataPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListModelMetadataPaginator(_ListModelMetadataPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelMetadata.html#SageMaker.Paginator.ListModelMetadata)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelmetadatapaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelMetadataRequestPaginateTypeDef]
    ) -> AioPageIterator[ListModelMetadataResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelMetadata.html#SageMaker.Paginator.ListModelMetadata.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelmetadatapaginator)
        """

if TYPE_CHECKING:
    _ListModelPackageGroupsPaginatorBase = AioPaginator[ListModelPackageGroupsOutputTypeDef]
else:
    _ListModelPackageGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListModelPackageGroupsPaginator(_ListModelPackageGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelPackageGroups.html#SageMaker.Paginator.ListModelPackageGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelpackagegroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelPackageGroupsInputPaginateTypeDef]
    ) -> AioPageIterator[ListModelPackageGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelPackageGroups.html#SageMaker.Paginator.ListModelPackageGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelpackagegroupspaginator)
        """

if TYPE_CHECKING:
    _ListModelPackagesPaginatorBase = AioPaginator[ListModelPackagesOutputTypeDef]
else:
    _ListModelPackagesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListModelPackagesPaginator(_ListModelPackagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelPackages.html#SageMaker.Paginator.ListModelPackages)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelpackagespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelPackagesInputPaginateTypeDef]
    ) -> AioPageIterator[ListModelPackagesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelPackages.html#SageMaker.Paginator.ListModelPackages.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelpackagespaginator)
        """

if TYPE_CHECKING:
    _ListModelQualityJobDefinitionsPaginatorBase = AioPaginator[
        ListModelQualityJobDefinitionsResponseTypeDef
    ]
else:
    _ListModelQualityJobDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListModelQualityJobDefinitionsPaginator(_ListModelQualityJobDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelQualityJobDefinitions.html#SageMaker.Paginator.ListModelQualityJobDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelqualityjobdefinitionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelQualityJobDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListModelQualityJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelQualityJobDefinitions.html#SageMaker.Paginator.ListModelQualityJobDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelqualityjobdefinitionspaginator)
        """

if TYPE_CHECKING:
    _ListModelsPaginatorBase = AioPaginator[ListModelsOutputTypeDef]
else:
    _ListModelsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListModelsPaginator(_ListModelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModels.html#SageMaker.Paginator.ListModels)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelsInputPaginateTypeDef]
    ) -> AioPageIterator[ListModelsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModels.html#SageMaker.Paginator.ListModels.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmodelspaginator)
        """

if TYPE_CHECKING:
    _ListMonitoringAlertHistoryPaginatorBase = AioPaginator[
        ListMonitoringAlertHistoryResponseTypeDef
    ]
else:
    _ListMonitoringAlertHistoryPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMonitoringAlertHistoryPaginator(_ListMonitoringAlertHistoryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringAlertHistory.html#SageMaker.Paginator.ListMonitoringAlertHistory)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmonitoringalerthistorypaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMonitoringAlertHistoryRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMonitoringAlertHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringAlertHistory.html#SageMaker.Paginator.ListMonitoringAlertHistory.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmonitoringalerthistorypaginator)
        """

if TYPE_CHECKING:
    _ListMonitoringAlertsPaginatorBase = AioPaginator[ListMonitoringAlertsResponseTypeDef]
else:
    _ListMonitoringAlertsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMonitoringAlertsPaginator(_ListMonitoringAlertsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringAlerts.html#SageMaker.Paginator.ListMonitoringAlerts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmonitoringalertspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMonitoringAlertsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMonitoringAlertsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringAlerts.html#SageMaker.Paginator.ListMonitoringAlerts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmonitoringalertspaginator)
        """

if TYPE_CHECKING:
    _ListMonitoringExecutionsPaginatorBase = AioPaginator[ListMonitoringExecutionsResponseTypeDef]
else:
    _ListMonitoringExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMonitoringExecutionsPaginator(_ListMonitoringExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringExecutions.html#SageMaker.Paginator.ListMonitoringExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmonitoringexecutionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMonitoringExecutionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMonitoringExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringExecutions.html#SageMaker.Paginator.ListMonitoringExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmonitoringexecutionspaginator)
        """

if TYPE_CHECKING:
    _ListMonitoringSchedulesPaginatorBase = AioPaginator[ListMonitoringSchedulesResponseTypeDef]
else:
    _ListMonitoringSchedulesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMonitoringSchedulesPaginator(_ListMonitoringSchedulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringSchedules.html#SageMaker.Paginator.ListMonitoringSchedules)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmonitoringschedulespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMonitoringSchedulesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMonitoringSchedulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringSchedules.html#SageMaker.Paginator.ListMonitoringSchedules.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listmonitoringschedulespaginator)
        """

if TYPE_CHECKING:
    _ListNotebookInstanceLifecycleConfigsPaginatorBase = AioPaginator[
        ListNotebookInstanceLifecycleConfigsOutputTypeDef
    ]
else:
    _ListNotebookInstanceLifecycleConfigsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListNotebookInstanceLifecycleConfigsPaginator(
    _ListNotebookInstanceLifecycleConfigsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListNotebookInstanceLifecycleConfigs.html#SageMaker.Paginator.ListNotebookInstanceLifecycleConfigs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listnotebookinstancelifecycleconfigspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNotebookInstanceLifecycleConfigsInputPaginateTypeDef]
    ) -> AioPageIterator[ListNotebookInstanceLifecycleConfigsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListNotebookInstanceLifecycleConfigs.html#SageMaker.Paginator.ListNotebookInstanceLifecycleConfigs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listnotebookinstancelifecycleconfigspaginator)
        """

if TYPE_CHECKING:
    _ListNotebookInstancesPaginatorBase = AioPaginator[ListNotebookInstancesOutputTypeDef]
else:
    _ListNotebookInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListNotebookInstancesPaginator(_ListNotebookInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListNotebookInstances.html#SageMaker.Paginator.ListNotebookInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listnotebookinstancespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNotebookInstancesInputPaginateTypeDef]
    ) -> AioPageIterator[ListNotebookInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListNotebookInstances.html#SageMaker.Paginator.ListNotebookInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listnotebookinstancespaginator)
        """

if TYPE_CHECKING:
    _ListOptimizationJobsPaginatorBase = AioPaginator[ListOptimizationJobsResponseTypeDef]
else:
    _ListOptimizationJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListOptimizationJobsPaginator(_ListOptimizationJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListOptimizationJobs.html#SageMaker.Paginator.ListOptimizationJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listoptimizationjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOptimizationJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOptimizationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListOptimizationJobs.html#SageMaker.Paginator.ListOptimizationJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listoptimizationjobspaginator)
        """

if TYPE_CHECKING:
    _ListPartnerAppsPaginatorBase = AioPaginator[ListPartnerAppsResponseTypeDef]
else:
    _ListPartnerAppsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPartnerAppsPaginator(_ListPartnerAppsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPartnerApps.html#SageMaker.Paginator.ListPartnerApps)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpartnerappspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPartnerAppsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPartnerAppsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPartnerApps.html#SageMaker.Paginator.ListPartnerApps.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpartnerappspaginator)
        """

if TYPE_CHECKING:
    _ListPipelineExecutionStepsPaginatorBase = AioPaginator[
        ListPipelineExecutionStepsResponseTypeDef
    ]
else:
    _ListPipelineExecutionStepsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPipelineExecutionStepsPaginator(_ListPipelineExecutionStepsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineExecutionSteps.html#SageMaker.Paginator.ListPipelineExecutionSteps)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelineexecutionstepspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPipelineExecutionStepsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPipelineExecutionStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineExecutionSteps.html#SageMaker.Paginator.ListPipelineExecutionSteps.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelineexecutionstepspaginator)
        """

if TYPE_CHECKING:
    _ListPipelineExecutionsPaginatorBase = AioPaginator[ListPipelineExecutionsResponseTypeDef]
else:
    _ListPipelineExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPipelineExecutionsPaginator(_ListPipelineExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineExecutions.html#SageMaker.Paginator.ListPipelineExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelineexecutionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPipelineExecutionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPipelineExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineExecutions.html#SageMaker.Paginator.ListPipelineExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelineexecutionspaginator)
        """

if TYPE_CHECKING:
    _ListPipelineParametersForExecutionPaginatorBase = AioPaginator[
        ListPipelineParametersForExecutionResponseTypeDef
    ]
else:
    _ListPipelineParametersForExecutionPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPipelineParametersForExecutionPaginator(_ListPipelineParametersForExecutionPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineParametersForExecution.html#SageMaker.Paginator.ListPipelineParametersForExecution)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelineparametersforexecutionpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPipelineParametersForExecutionRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPipelineParametersForExecutionResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineParametersForExecution.html#SageMaker.Paginator.ListPipelineParametersForExecution.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelineparametersforexecutionpaginator)
        """

if TYPE_CHECKING:
    _ListPipelineVersionsPaginatorBase = AioPaginator[ListPipelineVersionsResponseTypeDef]
else:
    _ListPipelineVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPipelineVersionsPaginator(_ListPipelineVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineVersions.html#SageMaker.Paginator.ListPipelineVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelineversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPipelineVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPipelineVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineVersions.html#SageMaker.Paginator.ListPipelineVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelineversionspaginator)
        """

if TYPE_CHECKING:
    _ListPipelinesPaginatorBase = AioPaginator[ListPipelinesResponseTypeDef]
else:
    _ListPipelinesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPipelinesPaginator(_ListPipelinesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelines.html#SageMaker.Paginator.ListPipelines)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelinespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPipelinesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPipelinesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelines.html#SageMaker.Paginator.ListPipelines.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listpipelinespaginator)
        """

if TYPE_CHECKING:
    _ListProcessingJobsPaginatorBase = AioPaginator[ListProcessingJobsResponseTypeDef]
else:
    _ListProcessingJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListProcessingJobsPaginator(_ListProcessingJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListProcessingJobs.html#SageMaker.Paginator.ListProcessingJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listprocessingjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProcessingJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListProcessingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListProcessingJobs.html#SageMaker.Paginator.ListProcessingJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listprocessingjobspaginator)
        """

if TYPE_CHECKING:
    _ListResourceCatalogsPaginatorBase = AioPaginator[ListResourceCatalogsResponseTypeDef]
else:
    _ListResourceCatalogsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListResourceCatalogsPaginator(_ListResourceCatalogsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListResourceCatalogs.html#SageMaker.Paginator.ListResourceCatalogs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listresourcecatalogspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceCatalogsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResourceCatalogsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListResourceCatalogs.html#SageMaker.Paginator.ListResourceCatalogs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listresourcecatalogspaginator)
        """

if TYPE_CHECKING:
    _ListSpacesPaginatorBase = AioPaginator[ListSpacesResponseTypeDef]
else:
    _ListSpacesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSpacesPaginator(_ListSpacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListSpaces.html#SageMaker.Paginator.ListSpaces)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listspacespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSpacesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSpacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListSpaces.html#SageMaker.Paginator.ListSpaces.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listspacespaginator)
        """

if TYPE_CHECKING:
    _ListStageDevicesPaginatorBase = AioPaginator[ListStageDevicesResponseTypeDef]
else:
    _ListStageDevicesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListStageDevicesPaginator(_ListStageDevicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListStageDevices.html#SageMaker.Paginator.ListStageDevices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#liststagedevicespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStageDevicesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListStageDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListStageDevices.html#SageMaker.Paginator.ListStageDevices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#liststagedevicespaginator)
        """

if TYPE_CHECKING:
    _ListStudioLifecycleConfigsPaginatorBase = AioPaginator[
        ListStudioLifecycleConfigsResponseTypeDef
    ]
else:
    _ListStudioLifecycleConfigsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListStudioLifecycleConfigsPaginator(_ListStudioLifecycleConfigsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListStudioLifecycleConfigs.html#SageMaker.Paginator.ListStudioLifecycleConfigs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#liststudiolifecycleconfigspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStudioLifecycleConfigsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListStudioLifecycleConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListStudioLifecycleConfigs.html#SageMaker.Paginator.ListStudioLifecycleConfigs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#liststudiolifecycleconfigspaginator)
        """

if TYPE_CHECKING:
    _ListSubscribedWorkteamsPaginatorBase = AioPaginator[ListSubscribedWorkteamsResponseTypeDef]
else:
    _ListSubscribedWorkteamsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSubscribedWorkteamsPaginator(_ListSubscribedWorkteamsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListSubscribedWorkteams.html#SageMaker.Paginator.ListSubscribedWorkteams)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listsubscribedworkteamspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSubscribedWorkteamsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSubscribedWorkteamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListSubscribedWorkteams.html#SageMaker.Paginator.ListSubscribedWorkteams.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listsubscribedworkteamspaginator)
        """

if TYPE_CHECKING:
    _ListTagsPaginatorBase = AioPaginator[ListTagsOutputTypeDef]
else:
    _ListTagsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTagsPaginator(_ListTagsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTags.html#SageMaker.Paginator.ListTags)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtagspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsInputPaginateTypeDef]
    ) -> AioPageIterator[ListTagsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTags.html#SageMaker.Paginator.ListTags.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtagspaginator)
        """

if TYPE_CHECKING:
    _ListTrainingJobsForHyperParameterTuningJobPaginatorBase = AioPaginator[
        ListTrainingJobsForHyperParameterTuningJobResponseTypeDef
    ]
else:
    _ListTrainingJobsForHyperParameterTuningJobPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTrainingJobsForHyperParameterTuningJobPaginator(
    _ListTrainingJobsForHyperParameterTuningJobPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrainingJobsForHyperParameterTuningJob.html#SageMaker.Paginator.ListTrainingJobsForHyperParameterTuningJob)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrainingjobsforhyperparametertuningjobpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTrainingJobsForHyperParameterTuningJobRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTrainingJobsForHyperParameterTuningJobResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrainingJobsForHyperParameterTuningJob.html#SageMaker.Paginator.ListTrainingJobsForHyperParameterTuningJob.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrainingjobsforhyperparametertuningjobpaginator)
        """

if TYPE_CHECKING:
    _ListTrainingJobsPaginatorBase = AioPaginator[ListTrainingJobsResponseTypeDef]
else:
    _ListTrainingJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTrainingJobsPaginator(_ListTrainingJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrainingJobs.html#SageMaker.Paginator.ListTrainingJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrainingjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTrainingJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTrainingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrainingJobs.html#SageMaker.Paginator.ListTrainingJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrainingjobspaginator)
        """

if TYPE_CHECKING:
    _ListTrainingPlansPaginatorBase = AioPaginator[ListTrainingPlansResponseTypeDef]
else:
    _ListTrainingPlansPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTrainingPlansPaginator(_ListTrainingPlansPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrainingPlans.html#SageMaker.Paginator.ListTrainingPlans)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrainingplanspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTrainingPlansRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTrainingPlansResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrainingPlans.html#SageMaker.Paginator.ListTrainingPlans.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrainingplanspaginator)
        """

if TYPE_CHECKING:
    _ListTransformJobsPaginatorBase = AioPaginator[ListTransformJobsResponseTypeDef]
else:
    _ListTransformJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTransformJobsPaginator(_ListTransformJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTransformJobs.html#SageMaker.Paginator.ListTransformJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtransformjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTransformJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTransformJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTransformJobs.html#SageMaker.Paginator.ListTransformJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtransformjobspaginator)
        """

if TYPE_CHECKING:
    _ListTrialComponentsPaginatorBase = AioPaginator[ListTrialComponentsResponseTypeDef]
else:
    _ListTrialComponentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTrialComponentsPaginator(_ListTrialComponentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrialComponents.html#SageMaker.Paginator.ListTrialComponents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrialcomponentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTrialComponentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTrialComponentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrialComponents.html#SageMaker.Paginator.ListTrialComponents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrialcomponentspaginator)
        """

if TYPE_CHECKING:
    _ListTrialsPaginatorBase = AioPaginator[ListTrialsResponseTypeDef]
else:
    _ListTrialsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTrialsPaginator(_ListTrialsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrials.html#SageMaker.Paginator.ListTrials)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrialspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTrialsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTrialsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrials.html#SageMaker.Paginator.ListTrials.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listtrialspaginator)
        """

if TYPE_CHECKING:
    _ListUltraServersByReservedCapacityPaginatorBase = AioPaginator[
        ListUltraServersByReservedCapacityResponseTypeDef
    ]
else:
    _ListUltraServersByReservedCapacityPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListUltraServersByReservedCapacityPaginator(_ListUltraServersByReservedCapacityPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListUltraServersByReservedCapacity.html#SageMaker.Paginator.ListUltraServersByReservedCapacity)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listultraserversbyreservedcapacitypaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUltraServersByReservedCapacityRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUltraServersByReservedCapacityResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListUltraServersByReservedCapacity.html#SageMaker.Paginator.ListUltraServersByReservedCapacity.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listultraserversbyreservedcapacitypaginator)
        """

if TYPE_CHECKING:
    _ListUserProfilesPaginatorBase = AioPaginator[ListUserProfilesResponseTypeDef]
else:
    _ListUserProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListUserProfilesPaginator(_ListUserProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListUserProfiles.html#SageMaker.Paginator.ListUserProfiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listuserprofilespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUserProfilesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUserProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListUserProfiles.html#SageMaker.Paginator.ListUserProfiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listuserprofilespaginator)
        """

if TYPE_CHECKING:
    _ListWorkforcesPaginatorBase = AioPaginator[ListWorkforcesResponseTypeDef]
else:
    _ListWorkforcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListWorkforcesPaginator(_ListWorkforcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListWorkforces.html#SageMaker.Paginator.ListWorkforces)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listworkforcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkforcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorkforcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListWorkforces.html#SageMaker.Paginator.ListWorkforces.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listworkforcespaginator)
        """

if TYPE_CHECKING:
    _ListWorkteamsPaginatorBase = AioPaginator[ListWorkteamsResponseTypeDef]
else:
    _ListWorkteamsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListWorkteamsPaginator(_ListWorkteamsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListWorkteams.html#SageMaker.Paginator.ListWorkteams)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listworkteamspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkteamsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorkteamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListWorkteams.html#SageMaker.Paginator.ListWorkteams.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#listworkteamspaginator)
        """

if TYPE_CHECKING:
    _SearchPaginatorBase = AioPaginator[SearchResponseTypeDef]
else:
    _SearchPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchPaginator(_SearchPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/Search.html#SageMaker.Paginator.Search)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#searchpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/Search.html#SageMaker.Paginator.Search.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/paginators/#searchpaginator)
        """
