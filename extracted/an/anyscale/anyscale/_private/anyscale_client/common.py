from abc import ABC, abstractmethod
from datetime import date
from typing import Dict, Generator, List, Optional, Tuple

from anyscale._private.models.image_uri import ImageURI
from anyscale.client.openapi_client.models import (
    AdminCreatedUser,
    AdminCreateUser,
    AnyscaleServiceAccount,
    Cloud,
    ClusteroperationResponse,
    ComputeTemplateConfig,
    CreateCloudCollaborator,
    CreateExperimentalWorkspace,
    CreateInternalProductionJob,
    CreateResourceQuota,
    CreateUserProjectCollaborator,
    DecoratedComputeTemplate,
    DecoratedjobqueueListResponse,
    DecoratedlistserviceapimodelListResponse,
    DecoratedProductionServiceV2APIModel,
    DeletedPlatformFineTunedModel,
    FineTunedModel,
    InternalProductionJob,
    JobQueueSortDirective,
    OrganizationCollaborator,
    OrganizationInvitation,
    Project,
    ResourceQuota,
    ServerSessionToken,
    SessionState,
    WorkspaceDataplaneProxiedArtifacts,
)
from anyscale.client.openapi_client.models.create_schedule import CreateSchedule
from anyscale.client.openapi_client.models.decorated_job_queue import DecoratedJobQueue
from anyscale.client.openapi_client.models.decorated_schedule import DecoratedSchedule
from anyscale.client.openapi_client.models.decorated_session import DecoratedSession
from anyscale.client.openapi_client.models.production_job import ProductionJob
from anyscale.client.openapi_client.models.session_ssh_key import SessionSshKey
from anyscale.sdk.anyscale_client.models import (
    ApplyProductionServiceV2Model,
    Cluster,
    ClusterCompute,
    ClusterEnvironment,
    Job as APIJobRun,
    ProductionServiceV2VersionModel,
)
from anyscale.sdk.anyscale_client.models.cluster_environment_build import (
    ClusterEnvironmentBuild,
)
from anyscale.utils.workspace_notification import WorkspaceNotification


# TODO(edoakes): figure out a sane policy for this.
# Maybe just make it part of the release process to update it, or fetch the
# default builds and get the latest one. The best thing to do is probably
# to populate this in the backend.
DEFAULT_RAY_VERSION = "2.47.1"  # RAY_RELEASE_UPDATE: update to latest version.
DEFAULT_PYTHON_VERSION = "py311"
RUNTIME_ENV_PACKAGE_FORMAT = "pkg_{content_hash}.zip"

# All workspace cluster names should start with this prefix.
WORKSPACE_CLUSTER_NAME_PREFIX = "workspace-cluster-"


class AnyscaleClientInterface(ABC):
    @abstractmethod
    def get_job_ui_url(self, job_id: str) -> str:
        """Get a URL to the webpage for a job."""
        raise NotImplementedError

    @abstractmethod
    def get_service_ui_url(self, service_id: str) -> str:
        """Get a URL to the webpage for a service."""
        raise NotImplementedError

    @abstractmethod
    def get_compute_config_ui_url(
        self, compute_config_id: str, *, cloud_id: str
    ) -> str:
        """Get a URL to the webpage for a compute config."""
        raise NotImplementedError

    @abstractmethod
    def get_current_workspace_id(self) -> Optional[str]:
        """Returns the ID of the workspace this is running in (or `None`)."""
        raise NotImplementedError

    @abstractmethod
    def inside_workspace(self) -> bool:
        """Returns true if this code is running inside a workspace."""
        raise NotImplementedError

    @abstractmethod
    def get_workspace_requirements_path(self) -> Optional[str]:
        """Returns the path to the workspace-managed requirements file.

        Returns None if dependency tracking is disable or the file does not exist or is not in a workspace.
        """
        raise NotImplementedError

    @abstractmethod
    def get_workspace_env_vars(self) -> Optional[Dict[str, str]]:
        """Returns the environment variables specified in workspace runtime dependencies."""
        raise NotImplementedError

    @abstractmethod
    def get_current_workspace_cluster(self) -> Optional[Cluster]:
        """Get the cluster model for the workspace this code is running in.

        Returns None if not running in a workspace.
        """
        raise NotImplementedError

    def send_workspace_notification(self, notification: WorkspaceNotification):
        """Send a workspace notification to be displayed to the user.

        This is a no-op if called from outside a workspace.
        """
        raise NotImplementedError

    @abstractmethod
    def get_project_id(
        self, *, parent_cloud_id: Optional[str] = None, name: Optional[str] = None
    ) -> str:
        """Get the project ID.

        If name is passed, projects with that name will be checked for a project with
        a cloud matching parent_cloud_id. If a match is found the cloud id is returned,
        otherwise a ValueError is raised.

        If name is not passed, but parent_cloud_id is, the default project for that cloud
        will be used.

        If running in a workspace, returns the workspace project ID.
        """
        raise NotImplementedError

    @abstractmethod
    def get_cloud_id(
        self, *, cloud_name: Optional[str] = None, compute_config_id: Optional[str]
    ) -> str:
        """Get the cloud ID for the provided cloud name or compute config ID.

        If both arguments are None:
            - if running in a workspace, get the workspace's cloud ID.
            - else, get the user's default cloud ID.
        """
        raise NotImplementedError

    @abstractmethod
    def get_cloud(self, *, cloud_id: str) -> Optional[Cloud]:
        """Get the cloud model for the provided cloud ID.

        Returns `None` if the cloud ID was not found.
        """
        raise NotImplementedError

    @abstractmethod
    def get_cloud_by_name(self, *, name: str) -> Optional[Cloud]:
        """Get the cloud model for the provided cloud name.

        Returns `None` if the cloud name was not found.
        """
        raise NotImplementedError

    @abstractmethod
    def get_default_cloud(self) -> Optional[Cloud]:
        """Get the user's default cloud."""
        raise NotImplementedError

    @abstractmethod
    def add_cloud_collaborators(
        self, cloud_id: str, collaborators: List[CreateCloudCollaborator]
    ) -> None:
        """Batch add collaborators to a cloud."""
        raise NotImplementedError

    @abstractmethod
    def terminate_system_cluster(self, cloud_id: str) -> ClusteroperationResponse:
        """Terminate the system cluster for the provided cloud ID."""
        raise NotImplementedError

    @abstractmethod
    def describe_system_workload_get_status(self, cloud_id: str) -> str:
        """Get the status of the system cluster for the provided cloud ID."""
        raise NotImplementedError

    @abstractmethod
    def create_compute_config(
        self, config: ComputeTemplateConfig, *, name: Optional[str] = None
    ) -> Tuple[str, str]:
        """Create a compute config and return its ID.

        If a name is not provided, the compute config will be "anonymous."

        Returns (name, ID).
        """
        raise NotImplementedError

    @abstractmethod
    def get_compute_config_id(
        self,
        compute_config_name: Optional[str] = None,
        cloud: Optional[str] = None,
        *,
        include_archived=False,
    ) -> Optional[str]:
        """Get the compute config ID for the provided name.

        If compute_config_name is None:
            - if running in a workspace, get the workspace's compute config ID.
            - else, get the user's default compute config ID.

        Returns None if the compute config name does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    def get_compute_config(
        self, compute_config_id: str
    ) -> Optional[DecoratedComputeTemplate]:
        """Get the compute config for the provided ID.

        Returns None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    def archive_compute_config(self, *, compute_config_id: str):
        """Archive the compute config for the provided ID."""
        raise NotImplementedError

    @abstractmethod
    def get_default_compute_config(self, *, cloud_id: str) -> ClusterCompute:
        """Get the default compute config for the provided cloud ID."""
        raise NotImplementedError

    @abstractmethod
    def get_default_build_id(self) -> str:
        """Get the default build id.

        If running in a workspace, it returns the workspace build id.
        Else it returns the default build id.
        """
        raise NotImplementedError

    @abstractmethod
    def get_cluster_env_by_name(self, name: str) -> Optional[ClusterEnvironment]:
        """Get a cluster environment by its name.

        """
        raise NotImplementedError

    @abstractmethod
    def list_cluster_env_builds(
        self, cluster_env_id: str
    ) -> Generator[ClusterEnvironmentBuild, None, None]:
        """List cluster environment builds for the provided cluster environment id.

        Returns a list of cluster environment builds.
        """
        raise NotImplementedError

    @abstractmethod
    def get_cluster_env_build(self, build_id: str) -> Optional[ClusterEnvironmentBuild]:
        """Get the cluster env build.
        """
        raise NotImplementedError

    @abstractmethod
    def get_cluster_env_build_id_from_containerfile(
        self,
        cluster_env_name: str,
        containerfile: str,
        anonymous: bool,
        ray_version: Optional[str] = None,
    ) -> str:
        """Get the cluster environment build ID for the cluster environment with provided containerfile.
        Look for an existing cluster environment with the provided name.
        If found, reuse it. Else, create a new cluster environment. The created cluster environment will be anonymous if anonymous is True.
        Create a new cluster environment build with the provided containerfile or try to reuse one with the same containerfile if exists.
        """
        raise NotImplementedError

    @abstractmethod
    def get_cluster_env_build_id_from_image_uri(
        self,
        image_uri: ImageURI,
        registry_login_secret: Optional[str] = None,
        ray_version: Optional[str] = None,
        name: Optional[str] = None,
    ):
        """Get the cluster environment build ID for the cluster environment with provided image_uri.

        It maps a image_uri to a cluster env name if a name is not provided, and then use the name to get the cluster env.
        If there exists a cluster environment for the image_uri, it will reuse the cluster env.
        Else it will create a new cluster environment.
        It will create a new cluster environment build with the provided image_uri or try to reuse one with the same image_uri if exists.

        The same URI should map to the same cluster env name and therefore the build but it is not guaranteed since
        the name format can change.

        """
        raise NotImplementedError

    @abstractmethod
    def get_cluster_env_build_image_uri(
        self, cluster_env_build_id: str, use_image_alias: bool = False
    ) -> Optional[ImageURI]:
        """Get the image URI for the provided build ID.
        If `use_image_alias` is True, the container image alias will be used if the build is BYOD.

        Returns None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    def get_service(
        self,
        name: str,
        *,
        cloud: Optional[str],
        project: Optional[str],
        include_archived=False,
    ) -> Optional[DecoratedProductionServiceV2APIModel]:
        """Get a service by name. Filter by cloud and project.

        Returns None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    def get_service_by_id(
        self, service_id: str
    ) -> Optional[DecoratedProductionServiceV2APIModel]:
        """Get a service by id."""
        raise NotImplementedError

    @abstractmethod
    def list_services(
        self,
        *,
        name: Optional[str],
        state_filter: Optional[List[str]],
        creator_id: Optional[str],
        cloud: Optional[str],
        project: Optional[str],
        include_archived: bool,
        count: Optional[int],
        paging_token: Optional[str],
        sort_field: Optional[str],
        sort_order: Optional[str],
    ) -> DecoratedlistserviceapimodelListResponse:
        """List services."""
        raise NotImplementedError

    @abstractmethod
    def get_project(self, project_id: str) -> Optional[Project]:
        """Get a project by id.

        Returns None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    def add_project_collaborators(
        self, project_id: str, collaborators: List[CreateUserProjectCollaborator]
    ) -> None:
        """Batch add collaborators to a project."""
        raise NotImplementedError

    @abstractmethod
    def get_job(
        self,
        *,
        name: Optional[str],
        job_id: Optional[str],
        cloud: Optional[str],
        project: Optional[str],
    ) -> Optional[ProductionJob]:
        """Get a job by either name or id. Filter by cloud and project.

        Returns None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    def get_job_queue(self, job_queue_id: str) -> Optional[DecoratedJobQueue]:
        """Get a job queue by id.

        Returns None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    def update_job_queue(
        self,
        job_queue_id: str,
        max_concurrency: Optional[int] = None,
        idle_timeout_s: Optional[int] = None,
    ) -> DecoratedJobQueue:
        """Update a job queue."""
        raise NotImplementedError

    @abstractmethod
    def get_job_runs(self, job_id: str) -> List[APIJobRun]:
        """Returns all job runs for a given job id.

        Returned in ascending order by creation time.
        """
        raise NotImplementedError

    @abstractmethod
    def list_job_queues(
        self,
        *,
        name: Optional[str] = None,
        creator_id: Optional[str] = None,
        cluster_status: Optional[SessionState] = None,
        project: Optional[str] = None,
        cloud: Optional[str] = None,
        count: Optional[int] = None,
        paging_token: Optional[str] = None,
        sorting_directives: Optional[List[JobQueueSortDirective]] = None,
    ) -> DecoratedjobqueueListResponse:
        """List job queues."""
        raise NotImplementedError

    @abstractmethod
    def rollout_service(
        self, model: ApplyProductionServiceV2Model
    ) -> DecoratedProductionServiceV2APIModel:
        """Deploy or update the service to use the provided config.

        Returns the service ID.
        """
        raise NotImplementedError

    @abstractmethod
    def rollback_service(
        self, service_id: str, *, max_surge_percent: Optional[int] = None
    ):
        """Roll the service back to the primary version.

        This can only be used during an active rollout.
        """
        raise NotImplementedError

    @abstractmethod
    def terminate_service(
        self, service_id: str
    ) -> DecoratedProductionServiceV2APIModel:
        """Mark the service to be terminated asynchronously."""
        raise NotImplementedError

    @abstractmethod
    def archive_service(self, service_id: str) -> DecoratedProductionServiceV2APIModel:
        """Mark the service to be archived asynchronously."""
        raise NotImplementedError

    @abstractmethod
    def delete_service(self, service_id: str) -> None:
        """Mark the service to be deleted asynchronously."""
        raise NotImplementedError

    @abstractmethod
    def submit_job(self, model: CreateInternalProductionJob) -> InternalProductionJob:
        """Submit the job to run."""
        raise NotImplementedError

    @abstractmethod
    def terminate_job(self, job_id: str):
        """Mark the job to be terminated asynchronously."""
        raise NotImplementedError

    @abstractmethod
    def archive_job(self, job_id: str):
        """Mark the job to be archived asynchronously."""
        raise NotImplementedError

    @abstractmethod
    def upload_local_dir_to_cloud_storage(
        self,
        local_dir: str,
        *,
        cloud_id: str,
        excludes: Optional[List[str]] = None,
        overwrite_existing_file: bool = False,
    ) -> str:
        """Upload the provided directory to cloud storage and return a URI for it.

        The directory will be zipped and the resulting URI can be used in a Ray runtime_env.

        The upload is preformed using a pre-signed URL fetched from Anyscale, so no
        local cloud provider authentication is required.

        The URI is content-addressable (containing a hash of the directory contents), so by
        default if the target file URI already exists it will not be overwritten.
        """
        raise NotImplementedError

    @abstractmethod
    def logs_for_job_run(
        self,
        job_run_id: str,
        head: bool = False,
        tail: bool = True,
        max_lines: Optional[int] = None,
        parse_json: Optional[bool] = None,
    ) -> str:
        """Returns the logs associated with a particular job run.

        The job_run_id is the backend id for the job run.

        Args:
        - parse_json: If true, we will always attempt to parse the logs as JSON.
            If false, we will always attempt to parse the logs as text. If None, we
            will attempt to parse the logs as JSON and fall back to text if parsing
            fails.
        """
        raise NotImplementedError

    @abstractmethod
    def controller_logs_for_service_version(
        self,
        service_version: ProductionServiceV2VersionModel,
        head: bool = False,
        max_lines: Optional[int] = None,
        parse_json: Optional[bool] = None,
    ) -> str:
        """
        Returns the controller logs associated with a particular service version.

        Args:
        - parse_json: If true, we will always attempt to parse the logs as JSON.
            If false, we will always attempt to parse the logs as text. If None, we
            will attempt to parse the logs as JSON and fall back to text if parsing
            fails.
        """
        raise NotImplementedError

    @abstractmethod
    def apply_schedule(self, model: CreateSchedule) -> DecoratedSchedule:
        """Creates or applies the schedule.

        Returns the DecoratedSchedule created.
        """
        raise NotImplementedError

    def get_schedule(
        self,
        *,
        name: Optional[str],
        id: Optional[str],  # noqa: A002
        cloud: Optional[str],
        project: Optional[str],
    ) -> Optional[DecoratedSchedule]:
        """Get a schedule by either name or id. Filter by cloud and project.

        Returns None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    def set_schedule_state(self, id: str, is_paused: bool):  # noqa: A002
        """Set the state of a schedule with id.
        """
        raise NotImplementedError

    @abstractmethod
    def trigger_schedule(self, id: str):  # noqa: A002
        """Trigger a schedule with id.
        """
        raise NotImplementedError

    @abstractmethod
    def get_dataset(self, name: str, version: Optional[int], project: Optional[str]):
        """See docstring for `anyscale.llm.dataset.get()`."""
        raise NotImplementedError

    @abstractmethod
    def upload_dataset(
        self,
        dataset_file: str,
        name: Optional[str],
        description: Optional[str],
        cloud: Optional[str],
        project: Optional[str],
    ):
        """See docstring for `anyscale.llm.dataset.upload()`."""
        raise NotImplementedError

    @abstractmethod
    def download_dataset(
        self, name: str, version: Optional[int], project: Optional[str]
    ) -> bytes:
        """See docstring for `anyscale.llm.dataset.download()`."""

    @abstractmethod
    def list_datasets(
        self,
        limit: Optional[int] = None,
        after: Optional[str] = None,  # Unique ID to start listing after
        name_contains: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ):
        """See docstring for `anyscale.llm.dataset.list()`."""
        raise NotImplementedError

    @abstractmethod
    def create_workspace(self, model: CreateExperimentalWorkspace) -> str:
        """Creates a workspace

        Returns the id of the workspace created.
        """
        raise NotImplementedError

    @abstractmethod
    def get_workspace(
        self,
        *,
        name: Optional[str],
        id: Optional[str],  # noqa: A002
        cloud: Optional[str],
        project: Optional[str],
    ) -> Optional[DecoratedSchedule]:
        """Get a workspace by either name or id. Filter by cloud and project.

        Returns None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    def start_workspace(self, workspace_id: str):
        """Start a workspace."""
        raise NotImplementedError

    @abstractmethod
    def terminate_workspace(self, workspace_id: str):
        """Terminate a workspace."""
        raise NotImplementedError

    @abstractmethod
    def update_workspace_dependencies_offline_only(
        self, workspace_id: Optional[str], requirements: List[str]
    ):
        """Updates the dynamic dependencies of a workspace while the workspace is offline"""
        raise NotImplementedError

    @abstractmethod
    def update_workspace_env_vars_offline_only(
        self, workspace_id: Optional[str], env_vars: Dict[str, str]
    ):
        """Updates the dynamic dependencies of a workspace"""
        raise NotImplementedError

    @abstractmethod
    def get_finetuned_model(
        self, model_id: Optional[str], job_id: Optional[str]
    ) -> FineTunedModel:  # noqa: A002
        """Returns LLM model information for the given model ID"""
        raise NotImplementedError

    @abstractmethod
    def get_workspace_cluster(
        self, workspace_id: Optional[str]
    ) -> Optional[DecoratedSession]:
        """Get the cluster model for the provided workspace ID."""
        raise NotImplementedError

    @abstractmethod
    def get_workspace_proxied_dataplane_artifacts(
        self, workspace_id: str
    ) -> WorkspaceDataplaneProxiedArtifacts:
        """Get the dataplane artifacts of the workspace."""
        raise NotImplementedError

    @abstractmethod
    def get_cluster_head_node_ip(self, cluster_id: str) -> Optional[str]:
        """Get the head node IP of the cluster."""
        raise NotImplementedError

    @abstractmethod
    def get_cluster_ssh_key(self, cluster_id: str) -> SessionSshKey:
        """Get the SSH key for the cluster."""
        raise NotImplementedError

    @abstractmethod
    def get_workspace_default_dir_name(self, workspace_id) -> str:
        """Get the default directory name for a workspace."""
        raise NotImplementedError

    @abstractmethod
    def delete_finetuned_model(self, model_id: str) -> DeletedPlatformFineTunedModel:
        """Deletes a finetuned model from the model registry given the model ID"""
        raise NotImplementedError

    @abstractmethod
    def list_finetuned_models(
        self, cloud_id: Optional[str], project_id: Optional[str], max_items: int,
    ) -> List[FineTunedModel]:
        raise NotImplementedError

    @abstractmethod
    def update_workspace(
        self,
        *,
        workspace_id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        compute_config_id: Optional[str] = None,
        cluster_environment_build_id: Optional[str] = None,
        idle_timeout_minutes: Optional[int] = None,
    ):
        """Update a workspace."""
        raise NotImplementedError

    @abstractmethod
    def download_aggregated_instance_usage_csv(
        self,
        start_date: date,
        end_date: date,
        cloud_id: Optional[str] = None,
        project_id: Optional[str] = None,
        directory: Optional[str] = None,
        hide_progress_bar: bool = False,
    ) -> str:
        """Download the aggregated instance usage csv."""
        raise NotImplementedError

    @abstractmethod
    def create_api_key(
        self, duration: float, user_id: Optional[str]
    ) -> ServerSessionToken:
        """Create a new API key."""
        raise NotImplementedError

    @abstractmethod
    def rotate_api_key(self, user_id: str) -> None:
        """Rotate the API key for user."""
        raise NotImplementedError

    @abstractmethod
    def admin_batch_create_users(
        self, admin_create_users: List[AdminCreateUser]
    ) -> List[AdminCreatedUser]:
        """Batch create, as an admin, users without email verification."""
        raise NotImplementedError

    @abstractmethod
    def create_organization_invitations(
        self, emails: List[str]
    ) -> Tuple[List[str], List[str]]:
        """Create organization invitations."""
        raise NotImplementedError

    @abstractmethod
    def list_organization_invitations(self) -> List[OrganizationInvitation]:
        """List organization invitations."""
        raise NotImplementedError

    @abstractmethod
    def delete_organization_invitation(self, email: str) -> OrganizationInvitation:
        """Delete organization invitation."""
        raise NotImplementedError

    @abstractmethod
    def get_organization_collaborators(
        self,
        email: Optional[str] = None,
        name: Optional[str] = None,
        is_service_account: Optional[bool] = None,
    ) -> List[OrganizationCollaborator]:
        """Get organization collaborators."""
        raise NotImplementedError

    @abstractmethod
    def delete_organization_collaborator(self, identity_id: str) -> None:
        """Delete organization collaborator."""
        raise NotImplementedError

    @abstractmethod
    def create_service_account(self, name: str) -> AnyscaleServiceAccount:
        """Create a service account."""
        raise NotImplementedError

    @abstractmethod
    def create_resource_quota(
        self, create_resource_quota: CreateResourceQuota
    ) -> ResourceQuota:
        """Create a resource quota."""
        raise NotImplementedError

    @abstractmethod
    def list_resource_quotas(
        self,
        name: Optional[str] = None,
        cloud_id: Optional[str] = None,
        creator_id: Optional[str] = None,
        is_enabled: Optional[bool] = None,
        max_items: int = 20,
    ) -> List[ResourceQuota]:
        """List resource quotas."""
        raise NotImplementedError

    @abstractmethod
    def delete_resource_quota(self, resource_quota_id: str) -> None:
        """Delete a resource quota."""
        raise NotImplementedError

    @abstractmethod
    def set_resource_quota_status(
        self, resource_quota_id: str, is_enabled: bool
    ) -> None:
        """Set the status of a resource quota."""
        raise NotImplementedError
