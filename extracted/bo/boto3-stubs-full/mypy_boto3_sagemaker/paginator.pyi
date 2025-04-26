"""
Type annotations for sagemaker service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_sagemaker.client import SageMakerClient
    from mypy_boto3_sagemaker.paginator import (
        ListActionsPaginator,
        ListAlgorithmsPaginator,
        ListAliasesPaginator,
        ListAppImageConfigsPaginator,
        ListAppsPaginator,
        ListArtifactsPaginator,
        ListAssociationsPaginator,
        ListAutoMLJobsPaginator,
        ListCandidatesForAutoMLJobPaginator,
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
        ListUserProfilesPaginator,
        ListWorkforcesPaginator,
        ListWorkteamsPaginator,
        SearchPaginator,
    )

    session = Session()
    client: SageMakerClient = session.client("sagemaker")

    list_actions_paginator: ListActionsPaginator = client.get_paginator("list_actions")
    list_algorithms_paginator: ListAlgorithmsPaginator = client.get_paginator("list_algorithms")
    list_aliases_paginator: ListAliasesPaginator = client.get_paginator("list_aliases")
    list_app_image_configs_paginator: ListAppImageConfigsPaginator = client.get_paginator("list_app_image_configs")
    list_apps_paginator: ListAppsPaginator = client.get_paginator("list_apps")
    list_artifacts_paginator: ListArtifactsPaginator = client.get_paginator("list_artifacts")
    list_associations_paginator: ListAssociationsPaginator = client.get_paginator("list_associations")
    list_auto_ml_jobs_paginator: ListAutoMLJobsPaginator = client.get_paginator("list_auto_ml_jobs")
    list_candidates_for_auto_ml_job_paginator: ListCandidatesForAutoMLJobPaginator = client.get_paginator("list_candidates_for_auto_ml_job")
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
    list_user_profiles_paginator: ListUserProfilesPaginator = client.get_paginator("list_user_profiles")
    list_workforces_paginator: ListWorkforcesPaginator = client.get_paginator("list_workforces")
    list_workteams_paginator: ListWorkteamsPaginator = client.get_paginator("list_workteams")
    search_paginator: SearchPaginator = client.get_paginator("search")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
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
    "ListActionsPaginator",
    "ListAlgorithmsPaginator",
    "ListAliasesPaginator",
    "ListAppImageConfigsPaginator",
    "ListAppsPaginator",
    "ListArtifactsPaginator",
    "ListAssociationsPaginator",
    "ListAutoMLJobsPaginator",
    "ListCandidatesForAutoMLJobPaginator",
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
    "ListUserProfilesPaginator",
    "ListWorkforcesPaginator",
    "ListWorkteamsPaginator",
    "SearchPaginator",
)

if TYPE_CHECKING:
    _ListActionsPaginatorBase = Paginator[ListActionsResponseTypeDef]
else:
    _ListActionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListActionsPaginator(_ListActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListActions.html#SageMaker.Paginator.ListActions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listactionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListActionsRequestPaginateTypeDef]
    ) -> PageIterator[ListActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListActions.html#SageMaker.Paginator.ListActions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listactionspaginator)
        """

if TYPE_CHECKING:
    _ListAlgorithmsPaginatorBase = Paginator[ListAlgorithmsOutputTypeDef]
else:
    _ListAlgorithmsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAlgorithmsPaginator(_ListAlgorithmsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAlgorithms.html#SageMaker.Paginator.ListAlgorithms)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listalgorithmspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAlgorithmsInputPaginateTypeDef]
    ) -> PageIterator[ListAlgorithmsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAlgorithms.html#SageMaker.Paginator.ListAlgorithms.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listalgorithmspaginator)
        """

if TYPE_CHECKING:
    _ListAliasesPaginatorBase = Paginator[ListAliasesResponseTypeDef]
else:
    _ListAliasesPaginatorBase = Paginator  # type: ignore[assignment]

class ListAliasesPaginator(_ListAliasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAliases.html#SageMaker.Paginator.ListAliases)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listaliasespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAliasesRequestPaginateTypeDef]
    ) -> PageIterator[ListAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAliases.html#SageMaker.Paginator.ListAliases.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listaliasespaginator)
        """

if TYPE_CHECKING:
    _ListAppImageConfigsPaginatorBase = Paginator[ListAppImageConfigsResponseTypeDef]
else:
    _ListAppImageConfigsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAppImageConfigsPaginator(_ListAppImageConfigsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAppImageConfigs.html#SageMaker.Paginator.ListAppImageConfigs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listappimageconfigspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAppImageConfigsRequestPaginateTypeDef]
    ) -> PageIterator[ListAppImageConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAppImageConfigs.html#SageMaker.Paginator.ListAppImageConfigs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listappimageconfigspaginator)
        """

if TYPE_CHECKING:
    _ListAppsPaginatorBase = Paginator[ListAppsResponseTypeDef]
else:
    _ListAppsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAppsPaginator(_ListAppsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListApps.html#SageMaker.Paginator.ListApps)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listappspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAppsRequestPaginateTypeDef]
    ) -> PageIterator[ListAppsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListApps.html#SageMaker.Paginator.ListApps.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listappspaginator)
        """

if TYPE_CHECKING:
    _ListArtifactsPaginatorBase = Paginator[ListArtifactsResponseTypeDef]
else:
    _ListArtifactsPaginatorBase = Paginator  # type: ignore[assignment]

class ListArtifactsPaginator(_ListArtifactsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListArtifacts.html#SageMaker.Paginator.ListArtifacts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listartifactspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListArtifactsRequestPaginateTypeDef]
    ) -> PageIterator[ListArtifactsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListArtifacts.html#SageMaker.Paginator.ListArtifacts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listartifactspaginator)
        """

if TYPE_CHECKING:
    _ListAssociationsPaginatorBase = Paginator[ListAssociationsResponseTypeDef]
else:
    _ListAssociationsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAssociationsPaginator(_ListAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAssociations.html#SageMaker.Paginator.ListAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssociationsRequestPaginateTypeDef]
    ) -> PageIterator[ListAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAssociations.html#SageMaker.Paginator.ListAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listassociationspaginator)
        """

if TYPE_CHECKING:
    _ListAutoMLJobsPaginatorBase = Paginator[ListAutoMLJobsResponseTypeDef]
else:
    _ListAutoMLJobsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAutoMLJobsPaginator(_ListAutoMLJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAutoMLJobs.html#SageMaker.Paginator.ListAutoMLJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listautomljobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAutoMLJobsRequestPaginateTypeDef]
    ) -> PageIterator[ListAutoMLJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListAutoMLJobs.html#SageMaker.Paginator.ListAutoMLJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listautomljobspaginator)
        """

if TYPE_CHECKING:
    _ListCandidatesForAutoMLJobPaginatorBase = Paginator[ListCandidatesForAutoMLJobResponseTypeDef]
else:
    _ListCandidatesForAutoMLJobPaginatorBase = Paginator  # type: ignore[assignment]

class ListCandidatesForAutoMLJobPaginator(_ListCandidatesForAutoMLJobPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListCandidatesForAutoMLJob.html#SageMaker.Paginator.ListCandidatesForAutoMLJob)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listcandidatesforautomljobpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCandidatesForAutoMLJobRequestPaginateTypeDef]
    ) -> PageIterator[ListCandidatesForAutoMLJobResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListCandidatesForAutoMLJob.html#SageMaker.Paginator.ListCandidatesForAutoMLJob.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listcandidatesforautomljobpaginator)
        """

if TYPE_CHECKING:
    _ListClusterNodesPaginatorBase = Paginator[ListClusterNodesResponseTypeDef]
else:
    _ListClusterNodesPaginatorBase = Paginator  # type: ignore[assignment]

class ListClusterNodesPaginator(_ListClusterNodesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListClusterNodes.html#SageMaker.Paginator.ListClusterNodes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listclusternodespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListClusterNodesRequestPaginateTypeDef]
    ) -> PageIterator[ListClusterNodesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListClusterNodes.html#SageMaker.Paginator.ListClusterNodes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listclusternodespaginator)
        """

if TYPE_CHECKING:
    _ListClusterSchedulerConfigsPaginatorBase = Paginator[
        ListClusterSchedulerConfigsResponseTypeDef
    ]
else:
    _ListClusterSchedulerConfigsPaginatorBase = Paginator  # type: ignore[assignment]

class ListClusterSchedulerConfigsPaginator(_ListClusterSchedulerConfigsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListClusterSchedulerConfigs.html#SageMaker.Paginator.ListClusterSchedulerConfigs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listclusterschedulerconfigspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListClusterSchedulerConfigsRequestPaginateTypeDef]
    ) -> PageIterator[ListClusterSchedulerConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListClusterSchedulerConfigs.html#SageMaker.Paginator.ListClusterSchedulerConfigs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listclusterschedulerconfigspaginator)
        """

if TYPE_CHECKING:
    _ListClustersPaginatorBase = Paginator[ListClustersResponseTypeDef]
else:
    _ListClustersPaginatorBase = Paginator  # type: ignore[assignment]

class ListClustersPaginator(_ListClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListClusters.html#SageMaker.Paginator.ListClusters)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listclusterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListClustersRequestPaginateTypeDef]
    ) -> PageIterator[ListClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListClusters.html#SageMaker.Paginator.ListClusters.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listclusterspaginator)
        """

if TYPE_CHECKING:
    _ListCodeRepositoriesPaginatorBase = Paginator[ListCodeRepositoriesOutputTypeDef]
else:
    _ListCodeRepositoriesPaginatorBase = Paginator  # type: ignore[assignment]

class ListCodeRepositoriesPaginator(_ListCodeRepositoriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListCodeRepositories.html#SageMaker.Paginator.ListCodeRepositories)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listcoderepositoriespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCodeRepositoriesInputPaginateTypeDef]
    ) -> PageIterator[ListCodeRepositoriesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListCodeRepositories.html#SageMaker.Paginator.ListCodeRepositories.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listcoderepositoriespaginator)
        """

if TYPE_CHECKING:
    _ListCompilationJobsPaginatorBase = Paginator[ListCompilationJobsResponseTypeDef]
else:
    _ListCompilationJobsPaginatorBase = Paginator  # type: ignore[assignment]

class ListCompilationJobsPaginator(_ListCompilationJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListCompilationJobs.html#SageMaker.Paginator.ListCompilationJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listcompilationjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCompilationJobsRequestPaginateTypeDef]
    ) -> PageIterator[ListCompilationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListCompilationJobs.html#SageMaker.Paginator.ListCompilationJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listcompilationjobspaginator)
        """

if TYPE_CHECKING:
    _ListComputeQuotasPaginatorBase = Paginator[ListComputeQuotasResponseTypeDef]
else:
    _ListComputeQuotasPaginatorBase = Paginator  # type: ignore[assignment]

class ListComputeQuotasPaginator(_ListComputeQuotasPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListComputeQuotas.html#SageMaker.Paginator.ListComputeQuotas)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listcomputequotaspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListComputeQuotasRequestPaginateTypeDef]
    ) -> PageIterator[ListComputeQuotasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListComputeQuotas.html#SageMaker.Paginator.ListComputeQuotas.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listcomputequotaspaginator)
        """

if TYPE_CHECKING:
    _ListContextsPaginatorBase = Paginator[ListContextsResponseTypeDef]
else:
    _ListContextsPaginatorBase = Paginator  # type: ignore[assignment]

class ListContextsPaginator(_ListContextsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListContexts.html#SageMaker.Paginator.ListContexts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listcontextspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListContextsRequestPaginateTypeDef]
    ) -> PageIterator[ListContextsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListContexts.html#SageMaker.Paginator.ListContexts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listcontextspaginator)
        """

if TYPE_CHECKING:
    _ListDataQualityJobDefinitionsPaginatorBase = Paginator[
        ListDataQualityJobDefinitionsResponseTypeDef
    ]
else:
    _ListDataQualityJobDefinitionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListDataQualityJobDefinitionsPaginator(_ListDataQualityJobDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDataQualityJobDefinitions.html#SageMaker.Paginator.ListDataQualityJobDefinitions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listdataqualityjobdefinitionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataQualityJobDefinitionsRequestPaginateTypeDef]
    ) -> PageIterator[ListDataQualityJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDataQualityJobDefinitions.html#SageMaker.Paginator.ListDataQualityJobDefinitions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listdataqualityjobdefinitionspaginator)
        """

if TYPE_CHECKING:
    _ListDeviceFleetsPaginatorBase = Paginator[ListDeviceFleetsResponseTypeDef]
else:
    _ListDeviceFleetsPaginatorBase = Paginator  # type: ignore[assignment]

class ListDeviceFleetsPaginator(_ListDeviceFleetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDeviceFleets.html#SageMaker.Paginator.ListDeviceFleets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listdevicefleetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeviceFleetsRequestPaginateTypeDef]
    ) -> PageIterator[ListDeviceFleetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDeviceFleets.html#SageMaker.Paginator.ListDeviceFleets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listdevicefleetspaginator)
        """

if TYPE_CHECKING:
    _ListDevicesPaginatorBase = Paginator[ListDevicesResponseTypeDef]
else:
    _ListDevicesPaginatorBase = Paginator  # type: ignore[assignment]

class ListDevicesPaginator(_ListDevicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDevices.html#SageMaker.Paginator.ListDevices)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listdevicespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDevicesRequestPaginateTypeDef]
    ) -> PageIterator[ListDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDevices.html#SageMaker.Paginator.ListDevices.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listdevicespaginator)
        """

if TYPE_CHECKING:
    _ListDomainsPaginatorBase = Paginator[ListDomainsResponseTypeDef]
else:
    _ListDomainsPaginatorBase = Paginator  # type: ignore[assignment]

class ListDomainsPaginator(_ListDomainsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDomains.html#SageMaker.Paginator.ListDomains)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listdomainspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDomainsRequestPaginateTypeDef]
    ) -> PageIterator[ListDomainsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListDomains.html#SageMaker.Paginator.ListDomains.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listdomainspaginator)
        """

if TYPE_CHECKING:
    _ListEdgeDeploymentPlansPaginatorBase = Paginator[ListEdgeDeploymentPlansResponseTypeDef]
else:
    _ListEdgeDeploymentPlansPaginatorBase = Paginator  # type: ignore[assignment]

class ListEdgeDeploymentPlansPaginator(_ListEdgeDeploymentPlansPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEdgeDeploymentPlans.html#SageMaker.Paginator.ListEdgeDeploymentPlans)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listedgedeploymentplanspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEdgeDeploymentPlansRequestPaginateTypeDef]
    ) -> PageIterator[ListEdgeDeploymentPlansResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEdgeDeploymentPlans.html#SageMaker.Paginator.ListEdgeDeploymentPlans.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listedgedeploymentplanspaginator)
        """

if TYPE_CHECKING:
    _ListEdgePackagingJobsPaginatorBase = Paginator[ListEdgePackagingJobsResponseTypeDef]
else:
    _ListEdgePackagingJobsPaginatorBase = Paginator  # type: ignore[assignment]

class ListEdgePackagingJobsPaginator(_ListEdgePackagingJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEdgePackagingJobs.html#SageMaker.Paginator.ListEdgePackagingJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listedgepackagingjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEdgePackagingJobsRequestPaginateTypeDef]
    ) -> PageIterator[ListEdgePackagingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEdgePackagingJobs.html#SageMaker.Paginator.ListEdgePackagingJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listedgepackagingjobspaginator)
        """

if TYPE_CHECKING:
    _ListEndpointConfigsPaginatorBase = Paginator[ListEndpointConfigsOutputTypeDef]
else:
    _ListEndpointConfigsPaginatorBase = Paginator  # type: ignore[assignment]

class ListEndpointConfigsPaginator(_ListEndpointConfigsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEndpointConfigs.html#SageMaker.Paginator.ListEndpointConfigs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listendpointconfigspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEndpointConfigsInputPaginateTypeDef]
    ) -> PageIterator[ListEndpointConfigsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEndpointConfigs.html#SageMaker.Paginator.ListEndpointConfigs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listendpointconfigspaginator)
        """

if TYPE_CHECKING:
    _ListEndpointsPaginatorBase = Paginator[ListEndpointsOutputTypeDef]
else:
    _ListEndpointsPaginatorBase = Paginator  # type: ignore[assignment]

class ListEndpointsPaginator(_ListEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEndpoints.html#SageMaker.Paginator.ListEndpoints)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listendpointspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEndpointsInputPaginateTypeDef]
    ) -> PageIterator[ListEndpointsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListEndpoints.html#SageMaker.Paginator.ListEndpoints.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listendpointspaginator)
        """

if TYPE_CHECKING:
    _ListExperimentsPaginatorBase = Paginator[ListExperimentsResponseTypeDef]
else:
    _ListExperimentsPaginatorBase = Paginator  # type: ignore[assignment]

class ListExperimentsPaginator(_ListExperimentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListExperiments.html#SageMaker.Paginator.ListExperiments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listexperimentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExperimentsRequestPaginateTypeDef]
    ) -> PageIterator[ListExperimentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListExperiments.html#SageMaker.Paginator.ListExperiments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listexperimentspaginator)
        """

if TYPE_CHECKING:
    _ListFeatureGroupsPaginatorBase = Paginator[ListFeatureGroupsResponseTypeDef]
else:
    _ListFeatureGroupsPaginatorBase = Paginator  # type: ignore[assignment]

class ListFeatureGroupsPaginator(_ListFeatureGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListFeatureGroups.html#SageMaker.Paginator.ListFeatureGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listfeaturegroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFeatureGroupsRequestPaginateTypeDef]
    ) -> PageIterator[ListFeatureGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListFeatureGroups.html#SageMaker.Paginator.ListFeatureGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listfeaturegroupspaginator)
        """

if TYPE_CHECKING:
    _ListFlowDefinitionsPaginatorBase = Paginator[ListFlowDefinitionsResponseTypeDef]
else:
    _ListFlowDefinitionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListFlowDefinitionsPaginator(_ListFlowDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListFlowDefinitions.html#SageMaker.Paginator.ListFlowDefinitions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listflowdefinitionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFlowDefinitionsRequestPaginateTypeDef]
    ) -> PageIterator[ListFlowDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListFlowDefinitions.html#SageMaker.Paginator.ListFlowDefinitions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listflowdefinitionspaginator)
        """

if TYPE_CHECKING:
    _ListHumanTaskUisPaginatorBase = Paginator[ListHumanTaskUisResponseTypeDef]
else:
    _ListHumanTaskUisPaginatorBase = Paginator  # type: ignore[assignment]

class ListHumanTaskUisPaginator(_ListHumanTaskUisPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListHumanTaskUis.html#SageMaker.Paginator.ListHumanTaskUis)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listhumantaskuispaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListHumanTaskUisRequestPaginateTypeDef]
    ) -> PageIterator[ListHumanTaskUisResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListHumanTaskUis.html#SageMaker.Paginator.ListHumanTaskUis.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listhumantaskuispaginator)
        """

if TYPE_CHECKING:
    _ListHyperParameterTuningJobsPaginatorBase = Paginator[
        ListHyperParameterTuningJobsResponseTypeDef
    ]
else:
    _ListHyperParameterTuningJobsPaginatorBase = Paginator  # type: ignore[assignment]

class ListHyperParameterTuningJobsPaginator(_ListHyperParameterTuningJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListHyperParameterTuningJobs.html#SageMaker.Paginator.ListHyperParameterTuningJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listhyperparametertuningjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListHyperParameterTuningJobsRequestPaginateTypeDef]
    ) -> PageIterator[ListHyperParameterTuningJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListHyperParameterTuningJobs.html#SageMaker.Paginator.ListHyperParameterTuningJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listhyperparametertuningjobspaginator)
        """

if TYPE_CHECKING:
    _ListImageVersionsPaginatorBase = Paginator[ListImageVersionsResponseTypeDef]
else:
    _ListImageVersionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListImageVersionsPaginator(_ListImageVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListImageVersions.html#SageMaker.Paginator.ListImageVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listimageversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImageVersionsRequestPaginateTypeDef]
    ) -> PageIterator[ListImageVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListImageVersions.html#SageMaker.Paginator.ListImageVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listimageversionspaginator)
        """

if TYPE_CHECKING:
    _ListImagesPaginatorBase = Paginator[ListImagesResponseTypeDef]
else:
    _ListImagesPaginatorBase = Paginator  # type: ignore[assignment]

class ListImagesPaginator(_ListImagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListImages.html#SageMaker.Paginator.ListImages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listimagespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImagesRequestPaginateTypeDef]
    ) -> PageIterator[ListImagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListImages.html#SageMaker.Paginator.ListImages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listimagespaginator)
        """

if TYPE_CHECKING:
    _ListInferenceComponentsPaginatorBase = Paginator[ListInferenceComponentsOutputTypeDef]
else:
    _ListInferenceComponentsPaginatorBase = Paginator  # type: ignore[assignment]

class ListInferenceComponentsPaginator(_ListInferenceComponentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceComponents.html#SageMaker.Paginator.ListInferenceComponents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listinferencecomponentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInferenceComponentsInputPaginateTypeDef]
    ) -> PageIterator[ListInferenceComponentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceComponents.html#SageMaker.Paginator.ListInferenceComponents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listinferencecomponentspaginator)
        """

if TYPE_CHECKING:
    _ListInferenceExperimentsPaginatorBase = Paginator[ListInferenceExperimentsResponseTypeDef]
else:
    _ListInferenceExperimentsPaginatorBase = Paginator  # type: ignore[assignment]

class ListInferenceExperimentsPaginator(_ListInferenceExperimentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceExperiments.html#SageMaker.Paginator.ListInferenceExperiments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listinferenceexperimentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInferenceExperimentsRequestPaginateTypeDef]
    ) -> PageIterator[ListInferenceExperimentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceExperiments.html#SageMaker.Paginator.ListInferenceExperiments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listinferenceexperimentspaginator)
        """

if TYPE_CHECKING:
    _ListInferenceRecommendationsJobStepsPaginatorBase = Paginator[
        ListInferenceRecommendationsJobStepsResponseTypeDef
    ]
else:
    _ListInferenceRecommendationsJobStepsPaginatorBase = Paginator  # type: ignore[assignment]

class ListInferenceRecommendationsJobStepsPaginator(
    _ListInferenceRecommendationsJobStepsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceRecommendationsJobSteps.html#SageMaker.Paginator.ListInferenceRecommendationsJobSteps)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listinferencerecommendationsjobstepspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInferenceRecommendationsJobStepsRequestPaginateTypeDef]
    ) -> PageIterator[ListInferenceRecommendationsJobStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceRecommendationsJobSteps.html#SageMaker.Paginator.ListInferenceRecommendationsJobSteps.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listinferencerecommendationsjobstepspaginator)
        """

if TYPE_CHECKING:
    _ListInferenceRecommendationsJobsPaginatorBase = Paginator[
        ListInferenceRecommendationsJobsResponseTypeDef
    ]
else:
    _ListInferenceRecommendationsJobsPaginatorBase = Paginator  # type: ignore[assignment]

class ListInferenceRecommendationsJobsPaginator(_ListInferenceRecommendationsJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceRecommendationsJobs.html#SageMaker.Paginator.ListInferenceRecommendationsJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listinferencerecommendationsjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInferenceRecommendationsJobsRequestPaginateTypeDef]
    ) -> PageIterator[ListInferenceRecommendationsJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListInferenceRecommendationsJobs.html#SageMaker.Paginator.ListInferenceRecommendationsJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listinferencerecommendationsjobspaginator)
        """

if TYPE_CHECKING:
    _ListLabelingJobsForWorkteamPaginatorBase = Paginator[
        ListLabelingJobsForWorkteamResponseTypeDef
    ]
else:
    _ListLabelingJobsForWorkteamPaginatorBase = Paginator  # type: ignore[assignment]

class ListLabelingJobsForWorkteamPaginator(_ListLabelingJobsForWorkteamPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListLabelingJobsForWorkteam.html#SageMaker.Paginator.ListLabelingJobsForWorkteam)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listlabelingjobsforworkteampaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLabelingJobsForWorkteamRequestPaginateTypeDef]
    ) -> PageIterator[ListLabelingJobsForWorkteamResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListLabelingJobsForWorkteam.html#SageMaker.Paginator.ListLabelingJobsForWorkteam.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listlabelingjobsforworkteampaginator)
        """

if TYPE_CHECKING:
    _ListLabelingJobsPaginatorBase = Paginator[ListLabelingJobsResponseTypeDef]
else:
    _ListLabelingJobsPaginatorBase = Paginator  # type: ignore[assignment]

class ListLabelingJobsPaginator(_ListLabelingJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListLabelingJobs.html#SageMaker.Paginator.ListLabelingJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listlabelingjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLabelingJobsRequestPaginateTypeDef]
    ) -> PageIterator[ListLabelingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListLabelingJobs.html#SageMaker.Paginator.ListLabelingJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listlabelingjobspaginator)
        """

if TYPE_CHECKING:
    _ListLineageGroupsPaginatorBase = Paginator[ListLineageGroupsResponseTypeDef]
else:
    _ListLineageGroupsPaginatorBase = Paginator  # type: ignore[assignment]

class ListLineageGroupsPaginator(_ListLineageGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListLineageGroups.html#SageMaker.Paginator.ListLineageGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listlineagegroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLineageGroupsRequestPaginateTypeDef]
    ) -> PageIterator[ListLineageGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListLineageGroups.html#SageMaker.Paginator.ListLineageGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listlineagegroupspaginator)
        """

if TYPE_CHECKING:
    _ListMlflowTrackingServersPaginatorBase = Paginator[ListMlflowTrackingServersResponseTypeDef]
else:
    _ListMlflowTrackingServersPaginatorBase = Paginator  # type: ignore[assignment]

class ListMlflowTrackingServersPaginator(_ListMlflowTrackingServersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMlflowTrackingServers.html#SageMaker.Paginator.ListMlflowTrackingServers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmlflowtrackingserverspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMlflowTrackingServersRequestPaginateTypeDef]
    ) -> PageIterator[ListMlflowTrackingServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMlflowTrackingServers.html#SageMaker.Paginator.ListMlflowTrackingServers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmlflowtrackingserverspaginator)
        """

if TYPE_CHECKING:
    _ListModelBiasJobDefinitionsPaginatorBase = Paginator[
        ListModelBiasJobDefinitionsResponseTypeDef
    ]
else:
    _ListModelBiasJobDefinitionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListModelBiasJobDefinitionsPaginator(_ListModelBiasJobDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelBiasJobDefinitions.html#SageMaker.Paginator.ListModelBiasJobDefinitions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelbiasjobdefinitionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelBiasJobDefinitionsRequestPaginateTypeDef]
    ) -> PageIterator[ListModelBiasJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelBiasJobDefinitions.html#SageMaker.Paginator.ListModelBiasJobDefinitions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelbiasjobdefinitionspaginator)
        """

if TYPE_CHECKING:
    _ListModelCardExportJobsPaginatorBase = Paginator[ListModelCardExportJobsResponseTypeDef]
else:
    _ListModelCardExportJobsPaginatorBase = Paginator  # type: ignore[assignment]

class ListModelCardExportJobsPaginator(_ListModelCardExportJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelCardExportJobs.html#SageMaker.Paginator.ListModelCardExportJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelcardexportjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelCardExportJobsRequestPaginateTypeDef]
    ) -> PageIterator[ListModelCardExportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelCardExportJobs.html#SageMaker.Paginator.ListModelCardExportJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelcardexportjobspaginator)
        """

if TYPE_CHECKING:
    _ListModelCardVersionsPaginatorBase = Paginator[ListModelCardVersionsResponseTypeDef]
else:
    _ListModelCardVersionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListModelCardVersionsPaginator(_ListModelCardVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelCardVersions.html#SageMaker.Paginator.ListModelCardVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelcardversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelCardVersionsRequestPaginateTypeDef]
    ) -> PageIterator[ListModelCardVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelCardVersions.html#SageMaker.Paginator.ListModelCardVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelcardversionspaginator)
        """

if TYPE_CHECKING:
    _ListModelCardsPaginatorBase = Paginator[ListModelCardsResponseTypeDef]
else:
    _ListModelCardsPaginatorBase = Paginator  # type: ignore[assignment]

class ListModelCardsPaginator(_ListModelCardsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelCards.html#SageMaker.Paginator.ListModelCards)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelcardspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelCardsRequestPaginateTypeDef]
    ) -> PageIterator[ListModelCardsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelCards.html#SageMaker.Paginator.ListModelCards.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelcardspaginator)
        """

if TYPE_CHECKING:
    _ListModelExplainabilityJobDefinitionsPaginatorBase = Paginator[
        ListModelExplainabilityJobDefinitionsResponseTypeDef
    ]
else:
    _ListModelExplainabilityJobDefinitionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListModelExplainabilityJobDefinitionsPaginator(
    _ListModelExplainabilityJobDefinitionsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelExplainabilityJobDefinitions.html#SageMaker.Paginator.ListModelExplainabilityJobDefinitions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelexplainabilityjobdefinitionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelExplainabilityJobDefinitionsRequestPaginateTypeDef]
    ) -> PageIterator[ListModelExplainabilityJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelExplainabilityJobDefinitions.html#SageMaker.Paginator.ListModelExplainabilityJobDefinitions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelexplainabilityjobdefinitionspaginator)
        """

if TYPE_CHECKING:
    _ListModelMetadataPaginatorBase = Paginator[ListModelMetadataResponseTypeDef]
else:
    _ListModelMetadataPaginatorBase = Paginator  # type: ignore[assignment]

class ListModelMetadataPaginator(_ListModelMetadataPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelMetadata.html#SageMaker.Paginator.ListModelMetadata)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelmetadatapaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelMetadataRequestPaginateTypeDef]
    ) -> PageIterator[ListModelMetadataResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelMetadata.html#SageMaker.Paginator.ListModelMetadata.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelmetadatapaginator)
        """

if TYPE_CHECKING:
    _ListModelPackageGroupsPaginatorBase = Paginator[ListModelPackageGroupsOutputTypeDef]
else:
    _ListModelPackageGroupsPaginatorBase = Paginator  # type: ignore[assignment]

class ListModelPackageGroupsPaginator(_ListModelPackageGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelPackageGroups.html#SageMaker.Paginator.ListModelPackageGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelpackagegroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelPackageGroupsInputPaginateTypeDef]
    ) -> PageIterator[ListModelPackageGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelPackageGroups.html#SageMaker.Paginator.ListModelPackageGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelpackagegroupspaginator)
        """

if TYPE_CHECKING:
    _ListModelPackagesPaginatorBase = Paginator[ListModelPackagesOutputTypeDef]
else:
    _ListModelPackagesPaginatorBase = Paginator  # type: ignore[assignment]

class ListModelPackagesPaginator(_ListModelPackagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelPackages.html#SageMaker.Paginator.ListModelPackages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelpackagespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelPackagesInputPaginateTypeDef]
    ) -> PageIterator[ListModelPackagesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelPackages.html#SageMaker.Paginator.ListModelPackages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelpackagespaginator)
        """

if TYPE_CHECKING:
    _ListModelQualityJobDefinitionsPaginatorBase = Paginator[
        ListModelQualityJobDefinitionsResponseTypeDef
    ]
else:
    _ListModelQualityJobDefinitionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListModelQualityJobDefinitionsPaginator(_ListModelQualityJobDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelQualityJobDefinitions.html#SageMaker.Paginator.ListModelQualityJobDefinitions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelqualityjobdefinitionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelQualityJobDefinitionsRequestPaginateTypeDef]
    ) -> PageIterator[ListModelQualityJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModelQualityJobDefinitions.html#SageMaker.Paginator.ListModelQualityJobDefinitions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelqualityjobdefinitionspaginator)
        """

if TYPE_CHECKING:
    _ListModelsPaginatorBase = Paginator[ListModelsOutputTypeDef]
else:
    _ListModelsPaginatorBase = Paginator  # type: ignore[assignment]

class ListModelsPaginator(_ListModelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModels.html#SageMaker.Paginator.ListModels)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelsInputPaginateTypeDef]
    ) -> PageIterator[ListModelsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListModels.html#SageMaker.Paginator.ListModels.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmodelspaginator)
        """

if TYPE_CHECKING:
    _ListMonitoringAlertHistoryPaginatorBase = Paginator[ListMonitoringAlertHistoryResponseTypeDef]
else:
    _ListMonitoringAlertHistoryPaginatorBase = Paginator  # type: ignore[assignment]

class ListMonitoringAlertHistoryPaginator(_ListMonitoringAlertHistoryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringAlertHistory.html#SageMaker.Paginator.ListMonitoringAlertHistory)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmonitoringalerthistorypaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMonitoringAlertHistoryRequestPaginateTypeDef]
    ) -> PageIterator[ListMonitoringAlertHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringAlertHistory.html#SageMaker.Paginator.ListMonitoringAlertHistory.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmonitoringalerthistorypaginator)
        """

if TYPE_CHECKING:
    _ListMonitoringAlertsPaginatorBase = Paginator[ListMonitoringAlertsResponseTypeDef]
else:
    _ListMonitoringAlertsPaginatorBase = Paginator  # type: ignore[assignment]

class ListMonitoringAlertsPaginator(_ListMonitoringAlertsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringAlerts.html#SageMaker.Paginator.ListMonitoringAlerts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmonitoringalertspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMonitoringAlertsRequestPaginateTypeDef]
    ) -> PageIterator[ListMonitoringAlertsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringAlerts.html#SageMaker.Paginator.ListMonitoringAlerts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmonitoringalertspaginator)
        """

if TYPE_CHECKING:
    _ListMonitoringExecutionsPaginatorBase = Paginator[ListMonitoringExecutionsResponseTypeDef]
else:
    _ListMonitoringExecutionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListMonitoringExecutionsPaginator(_ListMonitoringExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringExecutions.html#SageMaker.Paginator.ListMonitoringExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmonitoringexecutionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMonitoringExecutionsRequestPaginateTypeDef]
    ) -> PageIterator[ListMonitoringExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringExecutions.html#SageMaker.Paginator.ListMonitoringExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmonitoringexecutionspaginator)
        """

if TYPE_CHECKING:
    _ListMonitoringSchedulesPaginatorBase = Paginator[ListMonitoringSchedulesResponseTypeDef]
else:
    _ListMonitoringSchedulesPaginatorBase = Paginator  # type: ignore[assignment]

class ListMonitoringSchedulesPaginator(_ListMonitoringSchedulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringSchedules.html#SageMaker.Paginator.ListMonitoringSchedules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmonitoringschedulespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMonitoringSchedulesRequestPaginateTypeDef]
    ) -> PageIterator[ListMonitoringSchedulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListMonitoringSchedules.html#SageMaker.Paginator.ListMonitoringSchedules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listmonitoringschedulespaginator)
        """

if TYPE_CHECKING:
    _ListNotebookInstanceLifecycleConfigsPaginatorBase = Paginator[
        ListNotebookInstanceLifecycleConfigsOutputTypeDef
    ]
else:
    _ListNotebookInstanceLifecycleConfigsPaginatorBase = Paginator  # type: ignore[assignment]

class ListNotebookInstanceLifecycleConfigsPaginator(
    _ListNotebookInstanceLifecycleConfigsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListNotebookInstanceLifecycleConfigs.html#SageMaker.Paginator.ListNotebookInstanceLifecycleConfigs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listnotebookinstancelifecycleconfigspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNotebookInstanceLifecycleConfigsInputPaginateTypeDef]
    ) -> PageIterator[ListNotebookInstanceLifecycleConfigsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListNotebookInstanceLifecycleConfigs.html#SageMaker.Paginator.ListNotebookInstanceLifecycleConfigs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listnotebookinstancelifecycleconfigspaginator)
        """

if TYPE_CHECKING:
    _ListNotebookInstancesPaginatorBase = Paginator[ListNotebookInstancesOutputTypeDef]
else:
    _ListNotebookInstancesPaginatorBase = Paginator  # type: ignore[assignment]

class ListNotebookInstancesPaginator(_ListNotebookInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListNotebookInstances.html#SageMaker.Paginator.ListNotebookInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listnotebookinstancespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNotebookInstancesInputPaginateTypeDef]
    ) -> PageIterator[ListNotebookInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListNotebookInstances.html#SageMaker.Paginator.ListNotebookInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listnotebookinstancespaginator)
        """

if TYPE_CHECKING:
    _ListOptimizationJobsPaginatorBase = Paginator[ListOptimizationJobsResponseTypeDef]
else:
    _ListOptimizationJobsPaginatorBase = Paginator  # type: ignore[assignment]

class ListOptimizationJobsPaginator(_ListOptimizationJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListOptimizationJobs.html#SageMaker.Paginator.ListOptimizationJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listoptimizationjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOptimizationJobsRequestPaginateTypeDef]
    ) -> PageIterator[ListOptimizationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListOptimizationJobs.html#SageMaker.Paginator.ListOptimizationJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listoptimizationjobspaginator)
        """

if TYPE_CHECKING:
    _ListPartnerAppsPaginatorBase = Paginator[ListPartnerAppsResponseTypeDef]
else:
    _ListPartnerAppsPaginatorBase = Paginator  # type: ignore[assignment]

class ListPartnerAppsPaginator(_ListPartnerAppsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPartnerApps.html#SageMaker.Paginator.ListPartnerApps)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listpartnerappspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPartnerAppsRequestPaginateTypeDef]
    ) -> PageIterator[ListPartnerAppsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPartnerApps.html#SageMaker.Paginator.ListPartnerApps.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listpartnerappspaginator)
        """

if TYPE_CHECKING:
    _ListPipelineExecutionStepsPaginatorBase = Paginator[ListPipelineExecutionStepsResponseTypeDef]
else:
    _ListPipelineExecutionStepsPaginatorBase = Paginator  # type: ignore[assignment]

class ListPipelineExecutionStepsPaginator(_ListPipelineExecutionStepsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineExecutionSteps.html#SageMaker.Paginator.ListPipelineExecutionSteps)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listpipelineexecutionstepspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPipelineExecutionStepsRequestPaginateTypeDef]
    ) -> PageIterator[ListPipelineExecutionStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineExecutionSteps.html#SageMaker.Paginator.ListPipelineExecutionSteps.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listpipelineexecutionstepspaginator)
        """

if TYPE_CHECKING:
    _ListPipelineExecutionsPaginatorBase = Paginator[ListPipelineExecutionsResponseTypeDef]
else:
    _ListPipelineExecutionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListPipelineExecutionsPaginator(_ListPipelineExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineExecutions.html#SageMaker.Paginator.ListPipelineExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listpipelineexecutionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPipelineExecutionsRequestPaginateTypeDef]
    ) -> PageIterator[ListPipelineExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineExecutions.html#SageMaker.Paginator.ListPipelineExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listpipelineexecutionspaginator)
        """

if TYPE_CHECKING:
    _ListPipelineParametersForExecutionPaginatorBase = Paginator[
        ListPipelineParametersForExecutionResponseTypeDef
    ]
else:
    _ListPipelineParametersForExecutionPaginatorBase = Paginator  # type: ignore[assignment]

class ListPipelineParametersForExecutionPaginator(_ListPipelineParametersForExecutionPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineParametersForExecution.html#SageMaker.Paginator.ListPipelineParametersForExecution)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listpipelineparametersforexecutionpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPipelineParametersForExecutionRequestPaginateTypeDef]
    ) -> PageIterator[ListPipelineParametersForExecutionResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelineParametersForExecution.html#SageMaker.Paginator.ListPipelineParametersForExecution.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listpipelineparametersforexecutionpaginator)
        """

if TYPE_CHECKING:
    _ListPipelinesPaginatorBase = Paginator[ListPipelinesResponseTypeDef]
else:
    _ListPipelinesPaginatorBase = Paginator  # type: ignore[assignment]

class ListPipelinesPaginator(_ListPipelinesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelines.html#SageMaker.Paginator.ListPipelines)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listpipelinespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPipelinesRequestPaginateTypeDef]
    ) -> PageIterator[ListPipelinesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListPipelines.html#SageMaker.Paginator.ListPipelines.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listpipelinespaginator)
        """

if TYPE_CHECKING:
    _ListProcessingJobsPaginatorBase = Paginator[ListProcessingJobsResponseTypeDef]
else:
    _ListProcessingJobsPaginatorBase = Paginator  # type: ignore[assignment]

class ListProcessingJobsPaginator(_ListProcessingJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListProcessingJobs.html#SageMaker.Paginator.ListProcessingJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listprocessingjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProcessingJobsRequestPaginateTypeDef]
    ) -> PageIterator[ListProcessingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListProcessingJobs.html#SageMaker.Paginator.ListProcessingJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listprocessingjobspaginator)
        """

if TYPE_CHECKING:
    _ListResourceCatalogsPaginatorBase = Paginator[ListResourceCatalogsResponseTypeDef]
else:
    _ListResourceCatalogsPaginatorBase = Paginator  # type: ignore[assignment]

class ListResourceCatalogsPaginator(_ListResourceCatalogsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListResourceCatalogs.html#SageMaker.Paginator.ListResourceCatalogs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listresourcecatalogspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceCatalogsRequestPaginateTypeDef]
    ) -> PageIterator[ListResourceCatalogsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListResourceCatalogs.html#SageMaker.Paginator.ListResourceCatalogs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listresourcecatalogspaginator)
        """

if TYPE_CHECKING:
    _ListSpacesPaginatorBase = Paginator[ListSpacesResponseTypeDef]
else:
    _ListSpacesPaginatorBase = Paginator  # type: ignore[assignment]

class ListSpacesPaginator(_ListSpacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListSpaces.html#SageMaker.Paginator.ListSpaces)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listspacespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSpacesRequestPaginateTypeDef]
    ) -> PageIterator[ListSpacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListSpaces.html#SageMaker.Paginator.ListSpaces.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listspacespaginator)
        """

if TYPE_CHECKING:
    _ListStageDevicesPaginatorBase = Paginator[ListStageDevicesResponseTypeDef]
else:
    _ListStageDevicesPaginatorBase = Paginator  # type: ignore[assignment]

class ListStageDevicesPaginator(_ListStageDevicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListStageDevices.html#SageMaker.Paginator.ListStageDevices)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#liststagedevicespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStageDevicesRequestPaginateTypeDef]
    ) -> PageIterator[ListStageDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListStageDevices.html#SageMaker.Paginator.ListStageDevices.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#liststagedevicespaginator)
        """

if TYPE_CHECKING:
    _ListStudioLifecycleConfigsPaginatorBase = Paginator[ListStudioLifecycleConfigsResponseTypeDef]
else:
    _ListStudioLifecycleConfigsPaginatorBase = Paginator  # type: ignore[assignment]

class ListStudioLifecycleConfigsPaginator(_ListStudioLifecycleConfigsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListStudioLifecycleConfigs.html#SageMaker.Paginator.ListStudioLifecycleConfigs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#liststudiolifecycleconfigspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStudioLifecycleConfigsRequestPaginateTypeDef]
    ) -> PageIterator[ListStudioLifecycleConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListStudioLifecycleConfigs.html#SageMaker.Paginator.ListStudioLifecycleConfigs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#liststudiolifecycleconfigspaginator)
        """

if TYPE_CHECKING:
    _ListSubscribedWorkteamsPaginatorBase = Paginator[ListSubscribedWorkteamsResponseTypeDef]
else:
    _ListSubscribedWorkteamsPaginatorBase = Paginator  # type: ignore[assignment]

class ListSubscribedWorkteamsPaginator(_ListSubscribedWorkteamsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListSubscribedWorkteams.html#SageMaker.Paginator.ListSubscribedWorkteams)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listsubscribedworkteamspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSubscribedWorkteamsRequestPaginateTypeDef]
    ) -> PageIterator[ListSubscribedWorkteamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListSubscribedWorkteams.html#SageMaker.Paginator.ListSubscribedWorkteams.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listsubscribedworkteamspaginator)
        """

if TYPE_CHECKING:
    _ListTagsPaginatorBase = Paginator[ListTagsOutputTypeDef]
else:
    _ListTagsPaginatorBase = Paginator  # type: ignore[assignment]

class ListTagsPaginator(_ListTagsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTags.html#SageMaker.Paginator.ListTags)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtagspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsInputPaginateTypeDef]
    ) -> PageIterator[ListTagsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTags.html#SageMaker.Paginator.ListTags.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtagspaginator)
        """

if TYPE_CHECKING:
    _ListTrainingJobsForHyperParameterTuningJobPaginatorBase = Paginator[
        ListTrainingJobsForHyperParameterTuningJobResponseTypeDef
    ]
else:
    _ListTrainingJobsForHyperParameterTuningJobPaginatorBase = Paginator  # type: ignore[assignment]

class ListTrainingJobsForHyperParameterTuningJobPaginator(
    _ListTrainingJobsForHyperParameterTuningJobPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrainingJobsForHyperParameterTuningJob.html#SageMaker.Paginator.ListTrainingJobsForHyperParameterTuningJob)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtrainingjobsforhyperparametertuningjobpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTrainingJobsForHyperParameterTuningJobRequestPaginateTypeDef]
    ) -> PageIterator[ListTrainingJobsForHyperParameterTuningJobResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrainingJobsForHyperParameterTuningJob.html#SageMaker.Paginator.ListTrainingJobsForHyperParameterTuningJob.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtrainingjobsforhyperparametertuningjobpaginator)
        """

if TYPE_CHECKING:
    _ListTrainingJobsPaginatorBase = Paginator[ListTrainingJobsResponseTypeDef]
else:
    _ListTrainingJobsPaginatorBase = Paginator  # type: ignore[assignment]

class ListTrainingJobsPaginator(_ListTrainingJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrainingJobs.html#SageMaker.Paginator.ListTrainingJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtrainingjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTrainingJobsRequestPaginateTypeDef]
    ) -> PageIterator[ListTrainingJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrainingJobs.html#SageMaker.Paginator.ListTrainingJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtrainingjobspaginator)
        """

if TYPE_CHECKING:
    _ListTrainingPlansPaginatorBase = Paginator[ListTrainingPlansResponseTypeDef]
else:
    _ListTrainingPlansPaginatorBase = Paginator  # type: ignore[assignment]

class ListTrainingPlansPaginator(_ListTrainingPlansPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrainingPlans.html#SageMaker.Paginator.ListTrainingPlans)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtrainingplanspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTrainingPlansRequestPaginateTypeDef]
    ) -> PageIterator[ListTrainingPlansResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrainingPlans.html#SageMaker.Paginator.ListTrainingPlans.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtrainingplanspaginator)
        """

if TYPE_CHECKING:
    _ListTransformJobsPaginatorBase = Paginator[ListTransformJobsResponseTypeDef]
else:
    _ListTransformJobsPaginatorBase = Paginator  # type: ignore[assignment]

class ListTransformJobsPaginator(_ListTransformJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTransformJobs.html#SageMaker.Paginator.ListTransformJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtransformjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTransformJobsRequestPaginateTypeDef]
    ) -> PageIterator[ListTransformJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTransformJobs.html#SageMaker.Paginator.ListTransformJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtransformjobspaginator)
        """

if TYPE_CHECKING:
    _ListTrialComponentsPaginatorBase = Paginator[ListTrialComponentsResponseTypeDef]
else:
    _ListTrialComponentsPaginatorBase = Paginator  # type: ignore[assignment]

class ListTrialComponentsPaginator(_ListTrialComponentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrialComponents.html#SageMaker.Paginator.ListTrialComponents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtrialcomponentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTrialComponentsRequestPaginateTypeDef]
    ) -> PageIterator[ListTrialComponentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrialComponents.html#SageMaker.Paginator.ListTrialComponents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtrialcomponentspaginator)
        """

if TYPE_CHECKING:
    _ListTrialsPaginatorBase = Paginator[ListTrialsResponseTypeDef]
else:
    _ListTrialsPaginatorBase = Paginator  # type: ignore[assignment]

class ListTrialsPaginator(_ListTrialsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrials.html#SageMaker.Paginator.ListTrials)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtrialspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTrialsRequestPaginateTypeDef]
    ) -> PageIterator[ListTrialsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListTrials.html#SageMaker.Paginator.ListTrials.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listtrialspaginator)
        """

if TYPE_CHECKING:
    _ListUserProfilesPaginatorBase = Paginator[ListUserProfilesResponseTypeDef]
else:
    _ListUserProfilesPaginatorBase = Paginator  # type: ignore[assignment]

class ListUserProfilesPaginator(_ListUserProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListUserProfiles.html#SageMaker.Paginator.ListUserProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listuserprofilespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUserProfilesRequestPaginateTypeDef]
    ) -> PageIterator[ListUserProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListUserProfiles.html#SageMaker.Paginator.ListUserProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listuserprofilespaginator)
        """

if TYPE_CHECKING:
    _ListWorkforcesPaginatorBase = Paginator[ListWorkforcesResponseTypeDef]
else:
    _ListWorkforcesPaginatorBase = Paginator  # type: ignore[assignment]

class ListWorkforcesPaginator(_ListWorkforcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListWorkforces.html#SageMaker.Paginator.ListWorkforces)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listworkforcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkforcesRequestPaginateTypeDef]
    ) -> PageIterator[ListWorkforcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListWorkforces.html#SageMaker.Paginator.ListWorkforces.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listworkforcespaginator)
        """

if TYPE_CHECKING:
    _ListWorkteamsPaginatorBase = Paginator[ListWorkteamsResponseTypeDef]
else:
    _ListWorkteamsPaginatorBase = Paginator  # type: ignore[assignment]

class ListWorkteamsPaginator(_ListWorkteamsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListWorkteams.html#SageMaker.Paginator.ListWorkteams)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listworkteamspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkteamsRequestPaginateTypeDef]
    ) -> PageIterator[ListWorkteamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/ListWorkteams.html#SageMaker.Paginator.ListWorkteams.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#listworkteamspaginator)
        """

if TYPE_CHECKING:
    _SearchPaginatorBase = Paginator[SearchResponseTypeDef]
else:
    _SearchPaginatorBase = Paginator  # type: ignore[assignment]

class SearchPaginator(_SearchPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/Search.html#SageMaker.Paginator.Search)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#searchpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchRequestPaginateTypeDef]
    ) -> PageIterator[SearchResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/paginator/Search.html#SageMaker.Paginator.Search.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker/paginators/#searchpaginator)
        """
