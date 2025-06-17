"""Entrypoint to generate reference docs for the Anyscale CLI/SDK.

Usage: python -m anyscale._private.docgen --help
"""
import os

import click

import anyscale
from anyscale import scripts
from anyscale._private.docgen.generator import MarkdownGenerator, Module
from anyscale.aggregated_instance_usage.models import DownloadCSVFilters
from anyscale.cloud.models import (
    Cloud,
    CloudPermissionLevel,
    CloudProvider,
    ComputeStack,
    CreateCloudCollaborator,
)
from anyscale.commands import (
    aggregated_instance_usage_commands,
    cloud_commands,
    cluster_commands,
    cluster_env_commands,
    compute_config_commands,
    image_commands,
    job_commands,
    login_commands,
    logs_commands,
    machine_commands,
    machine_pool_commands,
    organization_invitation_commands,
    project_commands,
    resource_quota_commands,
    schedule_commands,
    service_account_commands,
    service_commands,
    user_commands,
    workspace_commands,
    workspace_commands_v2,
)
from anyscale.commands.llm import dataset_commands, models_commands
from anyscale.compute_config.models import (
    CloudDeployment,
    ComputeConfig,
    ComputeConfigVersion,
    HeadNodeConfig,
    MarketType,
    WorkerNodeGroupConfig,
)
from anyscale.image.models import ImageBuild, ImageBuildStatus
from anyscale.job.models import (
    JobConfig,
    JobLogMode,
    JobQueueConfig,
    JobQueueExecutionMode,
    JobQueueSpec,
    JobRunState,
    JobRunStatus,
    JobState,
    JobStatus,
)
from anyscale.llm.dataset._private.models import Dataset
from anyscale.llm.model.models import (
    DeletedFineTunedModel,
    FineTunedModel,
    FineTuningType,
)
from anyscale.organization_invitation.models import OrganizationInvitation
from anyscale.project.models import CreateProjectCollaborator, ProjectPermissionLevel
from anyscale.resource_quota.models import CreateResourceQuota, Quota, ResourceQuota
from anyscale.schedule.models import ScheduleConfig, ScheduleState, ScheduleStatus
from anyscale.service.models import (
    RayGCSExternalStorageConfig,
    ServiceConfig,
    ServiceState,
    ServiceStatus,
    ServiceVersionState,
    ServiceVersionStatus,
    TracingConfig,
)
from anyscale.service_account.models import OrganizationPermissionLevel, ServiceAccount
from anyscale.user.models import AdminCreatedUser, AdminCreateUser
from anyscale.workspace.models import WorkspaceConfig


# Defines all modules to be documented.
ALL_MODULES = [
    Module(
        title="Aggregated Instance Usage",
        filename="aggregated-instance-usage.md",
        cli_prefix="anyscale aggregated-instance-usage",
        cli_commands=[aggregated_instance_usage_commands.download_csv],
        sdk_prefix="anyscale.aggregated_instance_usage",
        sdk_commands=[anyscale.aggregated_instance_usage.download_csv,],
        models=[DownloadCSVFilters],
    ),
    Module(
        title="User",
        filename="user.md",
        cli_prefix="user",
        cli_commands=[user_commands.admin_batch_create],
        sdk_prefix="anyscale.user",
        sdk_commands=[anyscale.user.admin_batch_create,],
        models=[AdminCreateUser, AdminCreatedUser],
    ),
    Module(
        title="Project",
        filename="project-api.md",
        cli_prefix="anyscale project",
        cli_commands=[project_commands.add_collaborators,],
        sdk_prefix="anyscale.project",
        sdk_commands=[anyscale.project.add_collaborators,],
        models=[ProjectPermissionLevel, CreateProjectCollaborator],
        legacy_cli_commands=[project_commands.create, project_commands.list,],
        legacy_sdk_commands={
            "create_project": None,
            "delete_project": None,
            "get_default_project": None,
            "get_project": None,
            "search_projects": None,
        },
        legacy_sdk_models=[
            "CreateProject",
            "Project",
            "ProjectListResponse",
            "ProjectResponse",
            "ProjectsQuery",
        ],
    ),
    Module(
        title="Job",
        filename="job-api.md",
        cli_prefix="anyscale job",
        cli_commands=[
            job_commands.submit,
            job_commands.status,
            job_commands.terminate,
            job_commands.archive,
            job_commands.logs,
            job_commands.wait,
            job_commands.list,
        ],
        sdk_prefix="anyscale.job",
        sdk_commands=[
            anyscale.job.submit,
            anyscale.job.status,
            anyscale.job.terminate,
            anyscale.job.archive,
            anyscale.job.get_logs,
            anyscale.job.wait,
        ],
        models=[
            JobQueueSpec,
            JobQueueConfig,
            JobQueueExecutionMode,
            JobConfig,
            JobState,
            JobStatus,
            JobRunStatus,
            JobRunState,
            JobLogMode,
        ],
        # The following commands are legacy
        legacy_sdk_commands={
            "create_job": anyscale.job.submit,
            "get_production_job": anyscale.job.status,
            "terminate_job": anyscale.job.terminate,
            "fetch_job_logs": anyscale.job.get_logs,
            "fetch_production_job_logs": anyscale.job.get_logs,
            "get_job_logs_download": anyscale.job.get_logs,
            "get_job_logs_stream": anyscale.job.get_logs,
            # limited support, no replacement yet
            "search_jobs": None,
            "list_production_jobs": None,
        },
        legacy_sdk_models=[
            "BaseJobStatus",
            "CreateClusterComputeConfig",
            "CreateJobQueueConfig",
            "CreateProductionJob",
            "CreateProductionJobConfig",
            "HaJobGoalStates",
            "HaJobStates",
            "Job",
            "JobListResponse",
            "JobQueueConfig",
            "JobQueueExecutionMode",
            "JobQueueSpec",
            "JobRunType",
            "JobStatus",
            "JobsSortField",
            "ProductionJob",
            "ProductionJobConfig",
            "ProductionJobStateTransition",
            "ProductionjobListResponse",
            "ProductionjobResponse",
            "RayRuntimeEnvConfig",
            "SortByClauseJobsSortField",
        ],
    ),
    Module(
        title="Schedule",
        filename="schedule-api.md",
        cli_prefix="anyscale schedule",
        cli_commands=[
            schedule_commands.apply,
            schedule_commands.list,
            schedule_commands.pause,
            schedule_commands.resume,
            schedule_commands.status,
            schedule_commands.trigger,
            schedule_commands.url,
        ],
        sdk_prefix="anyscale.schedule",
        sdk_commands=[
            anyscale.schedule.apply,
            anyscale.schedule.set_state,
            anyscale.schedule.status,
            anyscale.schedule.trigger,
        ],
        models=[ScheduleConfig, ScheduleState, ScheduleStatus],
        # The following commands are legacy
        legacy_sdk_commands={
            "create_or_update_schedule": anyscale.schedule.apply,
            "get_schedule": anyscale.schedule.status,
            "pause_schedule": anyscale.schedule.set_state,
            "run_schedule": anyscale.schedule.trigger,
            # limited support, no replacement yet
            "list_schedules": None,
        },
        legacy_cli_prefix="anyscale schedule",
        legacy_cli_commands=[schedule_commands.create, schedule_commands.update],
    ),
    Module(
        title="Service",
        filename="service-api.md",
        cli_prefix="anyscale service",
        cli_commands=[
            service_commands.deploy,
            service_commands.status,
            service_commands.wait,
            service_commands.rollback,
            service_commands.terminate,
            service_commands.archive,
            service_commands.delete,
        ],
        sdk_prefix="anyscale.service",
        sdk_commands=[
            anyscale.service.deploy,
            anyscale.service.status,
            anyscale.service.wait,
            anyscale.service.rollback,
            anyscale.service.terminate,
            anyscale.service.archive,
            anyscale.service.delete,
        ],
        models=[
            ServiceConfig,
            RayGCSExternalStorageConfig,
            TracingConfig,
            ServiceStatus,
            ServiceState,
            ServiceVersionStatus,
            ServiceVersionState,
        ],
        # The following commands are legacy
        legacy_sdk_commands={
            "get_service": anyscale.service.status,
            "rollback_service": anyscale.service.rollback,
            "rollout_service": anyscale.service.deploy,
            "terminate_service": anyscale.service.terminate,
            # limited support, no replacement yet
            "list_services": None,
        },
        legacy_sdk_models=[
            "ApplyProductionServiceV2Model",
            "ApplyServiceModel",
            "ListServiceModel",
            "ListservicemodelListResponse",
            "ProductionServiceV2Model",
            "ProductionServiceV2VersionModel",
            "Productionservicev2ModelResponse",
            "RollbackServiceModel",
            "RolloutStrategy",
            "ServiceConfig",
            "ServiceEventCurrentState",
            "ServiceGoalStates",
            "ServiceModel",
            "ServiceObservabilityUrls",
            "ServiceSortField",
            "ServiceType",
            "ServiceVersionState",
            "ServicemodelListResponse",
            "ServicemodelResponse",
        ],
        legacy_cli_prefix="anyscale service",
        legacy_cli_commands=[service_commands.rollout],
    ),
    Module(
        title="Compute Config",
        filename="compute-config-api.md",
        cli_prefix="anyscale compute-config",
        cli_commands=[
            compute_config_commands.create_compute_config,
            compute_config_commands.get_compute_config,
            compute_config_commands.archive_compute_config,
        ],
        sdk_prefix="anyscale.compute_config",
        sdk_commands=[
            anyscale.compute_config.create,
            anyscale.compute_config.get,
            anyscale.compute_config.archive,
        ],
        models=[
            ComputeConfig,
            HeadNodeConfig,
            WorkerNodeGroupConfig,
            MarketType,
            CloudDeployment,
            ComputeConfigVersion,
        ],
        legacy_sdk_commands={
            "create_cluster_compute": anyscale.compute_config.create,
            "delete_cluster_compute": anyscale.compute_config.archive,
            "get_cluster_compute": anyscale.compute_config.get,
            "get_default_cluster_compute": anyscale.compute_config.get,
            # limited support, no replacement yet
            "search_cluster_computes": None,
        },
        legacy_sdk_models=[
            "ClusterCompute",
            "ClusterComputeConfig",
            "ClusterComputesQuery",
            "ClustercomputeListResponse",
            "ClustercomputeResponse",
            "ComputeNodeType",
            "ComputeTemplate",
            "ComputeTemplateConfig",
            "ComputetemplateResponse",
            "ComputetemplateconfigResponse",
            "CreateClusterCompute",
            "CreateClusterComputeConfig",
        ],
    ),
    Module(
        title="Service Account",
        filename="service-account.md",
        cli_prefix="anyscale service-account",
        cli_commands=[
            service_account_commands.create,
            service_account_commands.create_api_key,
            service_account_commands.list_service_accounts,
            service_account_commands.delete,
            service_account_commands.rotate_api_keys,
        ],
        sdk_prefix="anyscale.service_account",
        sdk_commands=[
            anyscale.service_account.create,
            anyscale.service_account.create_api_key,
            anyscale.service_account.list,
            anyscale.service_account.delete,
            anyscale.service_account.rotate_api_keys,
        ],
        models=[ServiceAccount, OrganizationPermissionLevel],
    ),
    Module(
        title="Image",
        filename="image.md",
        cli_prefix="anyscale image",
        cli_commands=[
            image_commands.build,
            image_commands.get,
            image_commands.register,
        ],
        sdk_prefix="anyscale.image",
        sdk_commands=[
            anyscale.image.build,
            anyscale.image.get,
            anyscale.image.register,
        ],
        models=[ImageBuild, ImageBuildStatus],
        legacy_title="Cluster environment",
        legacy_cli_prefix="anyscale image",
        legacy_cli_commands=[
            cluster_env_commands.archive,
            cluster_env_commands.build,
            cluster_env_commands.get,
            cluster_env_commands.list,
        ],
        legacy_sdk_commands={
            "create_byod_cluster_environment_build": anyscale.image.build,
            "create_cluster_environment_build": anyscale.image.build,
            "find_cluster_environment_build_by_identifier": None,
            "get_cluster_environment_build": None,
            "get_default_cluster_environment_build": None,
            "list_cluster_environment_builds": None,
            "create_byod_cluster_environment": anyscale.image.build,
            "create_cluster_environment": anyscale.image.build,
            "get_cluster_environment": None,
            "search_cluster_environments": None,
        },
        legacy_sdk_models=[
            "ClusterEnvironment",
            "ClusterEnvironmentBuild",
            "ClusterEnvironmentBuildOperation",
            "ClusterEnvironmentBuildStatus",
            "ClusterEnvironmentsQuery",
            "ClusterenvironmentListResponse",
            "ClusterenvironmentResponse",
            "ClusterenvironmentbuildListResponse",
            "ClusterenvironmentbuildoperationResponse",
            "CreateBYODClusterEnvironment",
            "CreateBYODClusterEnvironmentBuild",
            "CreateBYODClusterEnvironmentConfigurationSchema",
            "CreateClusterEnvironment",
            "CreateClusterEnvironmentBuild",
            "CreateClusterEnvironmentConfigurationSchema",
            "RayRuntimeEnvConfig",
        ],
    ),
    Module(
        title="Cloud",
        filename="cloud.md",
        cli_prefix="anyscale cloud",
        cli_commands=[
            cloud_commands.setup_cloud,
            cloud_commands.register_cloud,
            cloud_commands.cloud_edit,
            cloud_commands.cloud_update,
            cloud_commands.cloud_delete,
            cloud_commands.cloud_verify,
            cloud_commands.list_cloud,
            cloud_commands.cloud_config_update,
            cloud_commands.cloud_set_default,
            cloud_commands.add_collaborators,
            cloud_commands.get_cloud,
            cloud_commands.get_default_cloud,
            cloud_commands.terminate_system_cluster,
        ],
        sdk_prefix="anyscale.cloud",
        sdk_commands=[
            anyscale.cloud.add_collaborators,
            anyscale.cloud.get,
            anyscale.cloud.get_default,
            anyscale.cloud.terminate_system_cluster,
        ],
        models=[
            CloudPermissionLevel,
            CreateCloudCollaborator,
            Cloud,
            ComputeStack,
            CloudProvider,
        ],
        cli_command_group_prefix={cloud_commands.cloud_config_update: "config"},
        legacy_sdk_commands={
            # limited support, no replacement yet
            "get_cloud": None,
            "get_default_cloud": None,
            "search_clouds": None,
        },
        legacy_sdk_models=[
            "Cloud",
            "CloudConfig",
            "CloudListResponse",
            "CloudProviders",
            "CloudResponse",
            "CloudState",
            "CloudStatus",
            "CloudTypes",
            "CloudVersion",
            "CloudsQuery",
        ],
    ),
    Module(
        title="Logs",
        filename="logs.md",
        cli_prefix="anyscale logs",
        cli_commands=[logs_commands.anyscale_logs_cluster],
        sdk_prefix="anyscale.logs",
        sdk_commands=[],
        models=[],
    ),
    Module(
        title="Workspaces",
        filename="workspaces.md",
        cli_prefix="anyscale workspace_v2",
        cli_commands=[
            workspace_commands_v2.create,
            workspace_commands_v2.start,
            workspace_commands_v2.terminate,
            workspace_commands_v2.status,
            workspace_commands_v2.wait,
            workspace_commands_v2.ssh,
            workspace_commands_v2.run_command,
            workspace_commands_v2.pull,
            workspace_commands_v2.push,
            workspace_commands_v2.update,
            workspace_commands_v2.get,
        ],
        sdk_prefix="anyscale.workspace",
        sdk_commands=[
            anyscale.workspace.create,
            anyscale.workspace.start,
            anyscale.workspace.terminate,
            anyscale.workspace.status,
            anyscale.workspace.wait,
            anyscale.workspace.generate_ssh_config_file,
            anyscale.workspace.run_command,
        ],
        models=[WorkspaceConfig],
        legacy_cli_prefix="anyscale workspace",
        legacy_cli_commands=[
            workspace_commands.create,
            workspace_commands.run,
            workspace_commands.ssh,
            workspace_commands.start,
            workspace_commands.terminate,
            workspace_commands.pull,
            workspace_commands.push,
            # limited support, no replacement yet
            workspace_commands.clone,
            workspace_commands.copy_command,
        ],
    ),
    Module(
        title="Machine Pool",
        filename="machine-pool.md",
        cli_prefix="anyscale machine-pool",
        cli_commands=[
            machine_pool_commands.create_machine_pool,
            machine_pool_commands.update_machine_pool,
            machine_pool_commands.delete_machine_pool,
            machine_pool_commands.attach_machine_pool_to_cloud,
            machine_pool_commands.detach_machine_pool_from_cloud,
            machine_pool_commands.list_machine_pools,
            machine_pool_commands.describe,
        ],
        sdk_prefix="anyscale.machine_pool",
        sdk_commands=[],
        models=[],
    ),
    Module(
        title="Cluster",
        filename="cluster.md",
        cli_prefix="anyscale cluster",
        cli_commands=[],
        sdk_prefix="anyscale.cluster",  # fake name used as id, cluster has no SDK commands
        sdk_commands=[],
        models=[],
        legacy_cli_commands=[cluster_commands.start, cluster_commands.terminate,],
        legacy_cli_prefix="anyscale cluster",
        legacy_sdk_commands={
            "launch_cluster": None,
            "launch_cluster_with_new_cluster_environment": None,
            "create_cluster": None,
            "delete_cluster": None,
            "get_cluster": None,
            "search_clusters": None,
            "start_cluster": None,
            "terminate_cluster": None,
            "update_cluster": None,
        },
        legacy_sdk_models=[
            "ClusterHeadNodeInfo",
            "ClusterListResponse",
            "ClusterManagementStackVersions",
            "ClusterOperation",
            "ClusterResponse",
            "ClusterServicesUrls",
            "ClusterState",
            "ClusterStatus",
            "ClusterStatusDetails",
            "ClusteroperationResponse",
            "ClustersQuery",
            "CreateCluster",
            "StartClusterOptions",
            "TerminateClusterOptions",
            "UpdateCluster",
        ],
    ),
    Module(
        title="LLM Model",
        filename="llm_models.md",
        cli_prefix="anyscale llm model",
        cli_commands=[
            models_commands.get_model,
            models_commands.list_models,
            models_commands.delete_model,
        ],
        sdk_prefix="anyscale.llm.model",
        sdk_commands=[
            anyscale.llm.model.get,
            anyscale.llm.model.list,
            anyscale.llm.model.delete,
        ],
        models=[FineTunedModel, FineTuningType, DeletedFineTunedModel],
    ),
    Module(
        title="LLM Dataset",
        filename="llm_dataset.md",
        cli_prefix="anyscale llm dataset",
        cli_commands=[
            dataset_commands.get_dataset,
            dataset_commands.upload_dataset,
            dataset_commands.download_dataset,
        ],
        sdk_prefix="anyscale.llm.dataset",
        sdk_commands=[
            anyscale.llm.dataset.get,
            anyscale.llm.dataset.upload,
            anyscale.llm.dataset.download,
        ],
        models=[Dataset],
    ),
    Module(
        title="Resource quotas",
        filename="resource-quotas.md",
        cli_prefix="anyscale resource-quota",
        cli_commands=[
            resource_quota_commands.create,
            resource_quota_commands.list_resource_quotas,
            resource_quota_commands.delete,
            resource_quota_commands.enable,
            resource_quota_commands.disable,
        ],
        sdk_prefix="anyscale.resource_quota",
        sdk_commands=[
            anyscale.resource_quota.create,
            anyscale.resource_quota.list,
            anyscale.resource_quota.delete,
            anyscale.resource_quota.enable,
            anyscale.resource_quota.disable,
        ],
        models=[CreateResourceQuota, Quota, ResourceQuota],
    ),
    Module(
        title="Organization Invitation",
        filename="organization-invitation.md",
        cli_prefix="anyscale organization-invitation",
        cli_commands=[
            organization_invitation_commands.create,
            organization_invitation_commands.list,
            organization_invitation_commands.delete,
        ],
        sdk_prefix="anyscale.organization-invitation",
        sdk_commands=[
            anyscale.organization_invitation.create,
            anyscale.organization_invitation.list,
            anyscale.organization_invitation.delete,
        ],
        models=[OrganizationInvitation],
    ),
    Module(
        title="Other",
        filename="other.md",
        cli_prefix="anyscale",
        cli_commands=[
            login_commands.anyscale_login,
            login_commands.anyscale_logout,
            scripts.version_cli,
        ],
        sdk_prefix="",
        sdk_commands=[],
        models=[],
        # The following commands are legacy
        legacy_cli_prefix="anyscale",
        legacy_cli_commands=[
            machine_commands.delete_machine,
            machine_commands.list_machines,
        ],
        legacy_sdk_commands={
            "partial_update_organization": None,
            "upsert_sso_config": None,
            "upsert_test_sso_config": None,
        },
        legacy_sdk_models=[
            "AccessConfig",
            "ArchiveStatus",
            "BASEIMAGESENUM",
            "BaseJobStatus",
            "Build",
            "BuildResponse",
            "BuildStatus",
            "CreateSSOConfig",
            "GrpcProtocolConfig",
            "HTTPValidationError",
            "HttpProtocolConfig",
            "IdleTerminationStatus",
            "ListResponseMetadata",
            "NodeType",
            "OperationError",
            "OperationProgress",
            "OperationResult",
            "Organization",
            "OrganizationResponse",
            "PageQuery",
            "Protocols",
            "PythonModules",
            "PythonVersion",
            "RayGCSExternalStorageConfig",
            "Resources",
            "SSOConfig",
            "SSOMode",
            "SUPPORTEDBASEIMAGESENUM",
            "SortOrder",
            "SsoconfigResponse",
            "StaticSSOConfig",
            "TextQuery",
            "TracingConfig",
            "UpdateOrganization",
            "UserServiceAccessTypes",
            "WorkerNodeType",
        ],
    ),
]


@click.command(help="Generate markdown docs for the Anyscale CLI & SDK.")
@click.argument("output_dir")
@click.option(
    "-r",
    "--remove-existing",
    is_flag=True,
    default=False,
    help="If set, all files in the 'output_dir' that were not generated will be removed.",
)
def generate(
    output_dir: str, *, remove_existing: bool = False,
):
    if not os.path.isdir(output_dir):
        raise RuntimeError(f"output_dir '{output_dir}' does not exist.")

    gen = MarkdownGenerator(ALL_MODULES)
    gen.generate()

    generated_files = set()
    os.makedirs(output_dir, exist_ok=True)
    for filename, content in gen.generate().items():
        generated_files.add(filename)
        full_path = os.path.join(output_dir, filename)
        print(f"Writing output file {full_path}")
        with open(full_path, "w") as f:
            f.write(content)

    if remove_existing:
        to_remove = set(os.listdir(output_dir)) - generated_files
        for path in to_remove:
            full_path = os.path.join(output_dir, path)
            print(f"Removing existing file {full_path}")
            os.unlink(full_path)


if __name__ == "__main__":
    generate()
