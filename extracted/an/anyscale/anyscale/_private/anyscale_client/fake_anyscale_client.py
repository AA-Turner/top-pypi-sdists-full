from collections import defaultdict
from datetime import date, datetime
import logging
import os
from typing import DefaultDict, Dict, Generator, List, Optional, Tuple
from unittest.mock import Mock
import uuid

from anyscale._private.anyscale_client.common import (
    AnyscaleClientInterface,
    WORKSPACE_CLUSTER_NAME_PREFIX,
)
from anyscale._private.models.image_uri import ImageURI
from anyscale._private.models.model_base import ListResponse
from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.models import (
    AdminCreatedUser,
    AdminCreateUser,
    AnyscaleServiceAccount,
    Cloud,
    CloudProviders,
    ClusterOperation,
    ClusteroperationResponse,
    ClusterState,
    ComputeTemplateConfig,
    CreateCloudCollaborator,
    CreateExperimentalWorkspace,
    CreateInternalProductionJob,
    CreateResourceQuota,
    CreateUserProjectCollaborator,
    DecoratedComputeTemplate,
    DecoratedlistserviceapimodelListResponse,
    DecoratedProductionServiceV2APIModel,
    DeletedPlatformFineTunedModel,
    ExperimentalWorkspace,
    FineTunedModel,
    FineTuneType,
    HaJobGoalStates,
    HaJobStates,
    InternalProductionJob,
    ListResponseMetadata,
    MiniCloud,
    MiniUser,
    OrganizationCollaborator,
    OrganizationInvitation,
    OrganizationPermissionLevel,
    ProductionJob,
    ProductionJobStateTransition,
    Project,
    ResourceQuota,
    ServerSessionToken,
    WorkspaceDataplaneProxiedArtifacts,
)
from anyscale.client.openapi_client.models.create_schedule import CreateSchedule
from anyscale.client.openapi_client.models.decorated_job_queue import DecoratedJobQueue
from anyscale.client.openapi_client.models.decorated_schedule import DecoratedSchedule
from anyscale.client.openapi_client.models.decorated_session import DecoratedSession
from anyscale.client.openapi_client.models.session_ssh_key import SessionSshKey
from anyscale.cluster_compute import parse_cluster_compute_name_version
from anyscale.llm.dataset._private.models import Dataset
from anyscale.sdk.anyscale_client.configuration import Configuration
from anyscale.sdk.anyscale_client.models import (
    ApplyProductionServiceV2Model,
    Cluster,
    ClusterCompute,
    ClusterComputeConfig,
    ClusterEnvironmentBuild,
    ClusterEnvironmentBuildStatus,
    ComputeNodeType,
    Job as APIJobRun,
    ProductionServiceV2VersionModel,
    ServiceEventCurrentState,
    ServiceVersionState,
    SessionState,
)
from anyscale.sdk.anyscale_client.models.cluster_environment import ClusterEnvironment
from anyscale.shared_anyscale_utils.latest_ray_version import LATEST_RAY_VERSION
from anyscale.utils.workspace_notification import WorkspaceNotification


block_logger = BlockLogger()
logger = logging.getLogger(__name__)

OPENAPI_NO_VALIDATION = Configuration()
OPENAPI_NO_VALIDATION.client_side_validation = False


class FakeAnyscaleClient(AnyscaleClientInterface):
    BASE_UI_URL = "http://fake.com"
    CLOUD_BUCKET = "s3://fake-bucket/{cloud_id}"
    DEFAULT_CLOUD_ID = "fake-default-cloud-id"
    DEFAULT_CLOUD_NAME = "fake-default-cloud"
    DEFAULT_PROJECT_NAME = "fake-default-project"
    DEFAULT_PROJECT_ID = "fake-default-project-id"
    DEFAULT_CLUSTER_COMPUTE_NAME = "fake-default-cluster-compute"
    DEFAULT_CLUSTER_COMPUTE_ID = "fake-default-cluster-compute-id"
    DEFAULT_CLUSTER_ENV_BUILD_ID = "fake-default-cluster-env-build-id"
    DEFAULT_USER_ID = "fake-user-id"
    DEFAULT_USER_EMAIL = "user@email.com"
    DEFAULT_ORGANIZATION_ID = "fake-org-id"

    WORKSPACE_ID = "fake-workspace-id"
    WORKSPACE_CLOUD_ID = "fake-workspace-cloud-id"
    WORKSPACE_CLUSTER_ID = "fake-workspace-cluster-id"
    WORKSPACE_PROJECT_ID = "fake-workspace-project-id"
    WORKSPACE_CLUSTER_COMPUTE_ID = "fake-workspace-cluster-compute-id"
    WORKSPACE_CLUSTER_ENV_BUILD_ID = "fake-workspace-cluster-env-build-id"

    SCHEDULE_NEXT_TRIGGER_AT_TIME = datetime.utcnow()

    def __init__(self):
        self._builds: Dict[str, ClusterEnvironmentBuild] = {
            self.DEFAULT_CLUSTER_ENV_BUILD_ID: ClusterEnvironmentBuild(
                id=self.DEFAULT_CLUSTER_ENV_BUILD_ID,
                cluster_environment_id="default-cluster-env-id",
                docker_image_name="docker.io/my/base-image:latest",
                status=ClusterEnvironmentBuildStatus.SUCCEEDED,
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            ),
            self.WORKSPACE_CLUSTER_ENV_BUILD_ID: ClusterEnvironmentBuild(
                id=self.WORKSPACE_CLUSTER_ENV_BUILD_ID,
                cluster_environment_id="workspace-cluster-env-id",
                docker_image_name="docker.io/my/base-ws-image:latest",
                status=ClusterEnvironmentBuildStatus.SUCCEEDED,
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            ),
        }
        self._images: Dict[str, ClusterEnvironment] = {
            "default-cluster-env-id": ClusterEnvironment(
                id="default-cluster-env-id",
                name="default-cluster-env",
                anonymous=True,
                is_default=True,
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            ),
            "workspace-cluster-env-id": ClusterEnvironment(
                id="workspace-cluster-env-id",
                name="default-workspace-cluster-env",
                anonymous=True,
                is_default=True,
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            ),
        }
        self._compute_config_name_to_ids: DefaultDict[str, List[str]] = defaultdict(
            list
        )
        self._compute_config_id_to_cloud_id: Dict[str, str] = {}
        self._compute_configs: Dict[str, ClusterCompute] = {}
        self._archived_compute_configs: Dict[str, ClusterCompute] = {}
        self._workspace_cluster: Optional[Cluster] = None
        self._workspace_dependency_tracking_enabled: bool = False
        self._services: Dict[str, DecoratedProductionServiceV2APIModel] = {}
        self._archived_services: Dict[str, DecoratedProductionServiceV2APIModel] = {}
        self._deleted_services: Dict[str, DecoratedProductionServiceV2APIModel] = {}
        self._jobs: Dict[str, ProductionJob] = {}
        self._job_runs: Dict[str, List[APIJobRun]] = defaultdict(list)
        self._job_queues: Dict[str, DecoratedJobQueue] = {}
        self._project_to_id: Dict[Optional[str] : Dict[Optional[str], str]] = {}
        self._project_collaborators: Dict[str, List[CreateUserProjectCollaborator]] = {}
        self._rolled_out_model: Optional[ApplyProductionServiceV2Model] = None
        self._sent_workspace_notifications: List[WorkspaceNotification] = []
        self._rolled_back_service: Optional[Tuple[str, Optional[int]]] = None
        self._terminated_service: Optional[str] = None
        self._archived_jobs: Dict[str, ProductionJob] = {}
        self._requirements_path: Optional[str] = None
        self._upload_uri_mapping: Dict[str, str] = {}
        self._submitted_job: Optional[CreateInternalProductionJob] = None
        self._env_vars: Optional[Dict[str, str]] = None
        self._job_run_logs: Dict[str, str] = {}
        self._controller_logs: Dict[str, str] = {}
        self._schedules: Dict[str, DecoratedSchedule] = {}
        self._schedule_trigger_counts: Dict[str, int] = defaultdict(int)
        self._users: Dict[str, AdminCreatedUser] = {}
        self._workspaces: Dict[str, ExperimentalWorkspace] = {}
        self._workspaces_dependencies: Dict[str, List[str]] = {}
        self._workspaces_env_vars: Dict[str, Dict[str, str]] = {}
        self._clusters_headnode_ip: Dict[str, str] = {}
        self._clusters_ssh_key: Dict[str, SessionSshKey] = {}
        self._api_keys: Dict[str, List[str]] = defaultdict(list)
        self._organization_collaborators: List[OrganizationCollaborator] = []
        self._organization_invitations: Dict[str, OrganizationInvitation] = {}
        self._resource_quotas: Dict[str, ResourceQuota] = {}
        self._system_cluster_status: Dict[str, str] = {}

        # Cloud ID -> Cloud.
        self._clouds: Dict[str, Cloud] = {
            self.DEFAULT_CLOUD_ID: Cloud(
                id=self.DEFAULT_CLOUD_ID,
                name=self.DEFAULT_CLOUD_NAME,
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            ),
        }

        # Cloud ID -> collaborators
        self._cloud_collaborators: Dict[str, List[CreateCloudCollaborator]] = {}

        # Cloud ID -> default ClusterCompute.
        compute_config = ClusterCompute(
            id=self.DEFAULT_CLUSTER_COMPUTE_ID,
            name=self.DEFAULT_CLUSTER_COMPUTE_NAME,
            config=ClusterComputeConfig(
                cloud_id=self.DEFAULT_CLOUD_ID,
                head_node_type=ComputeNodeType(
                    name="default-head-node",
                    instance_type="m5.2xlarge",
                    resources={"CPU": 8, "GPU": 1},
                ),
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            ),
            local_vars_configuration=OPENAPI_NO_VALIDATION,
        )
        self._default_compute_configs: Dict[str, ClusterCompute] = {
            self.DEFAULT_CLOUD_ID: compute_config,
        }
        self.add_compute_config(compute_config)

    def get_job_ui_url(self, job_id: str) -> str:
        return f"{self.BASE_UI_URL}/jobs/{job_id}"

    def get_service_ui_url(self, service_id: str) -> str:
        return f"{self.BASE_UI_URL}/services/{service_id}"

    def get_compute_config_ui_url(
        self, compute_config_id: str, *, cloud_id: str
    ) -> str:
        return f"{self.BASE_UI_URL}/v2/{cloud_id}/compute-configs/{compute_config_id}"

    def set_inside_workspace(
        self,
        inside_workspace: bool,
        *,
        requirements_path: Optional[str] = None,
        cluster_name: Optional[str] = None,
        env_vars: Optional[Dict[str, str]] = None,
    ):
        self._requirements_path = requirements_path
        self._env_vars = env_vars
        if inside_workspace:
            self._workspace_cluster = Cluster(
                id=self.WORKSPACE_CLUSTER_ID,
                name=cluster_name
                if cluster_name is not None
                else WORKSPACE_CLUSTER_NAME_PREFIX + "test",
                project_id=self.WORKSPACE_PROJECT_ID,
                cluster_compute_id=self.WORKSPACE_CLUSTER_COMPUTE_ID,
                cluster_environment_build_id=self.WORKSPACE_CLUSTER_ENV_BUILD_ID,
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            )
        else:
            self._workspace_cluster = None

    def get_current_workspace_id(self) -> Optional[str]:
        return (
            self.WORKSPACE_ID
            if self.get_current_workspace_cluster() is not None
            else None
        )

    def inside_workspace(self) -> bool:
        return self.get_current_workspace_cluster() is not None

    def get_workspace_env_vars(self) -> Optional[Dict[str, str]]:
        return self._env_vars

    def get_workspace_requirements_path(self) -> Optional[str]:
        if self.inside_workspace():
            return self._requirements_path
        return None

    def get_current_workspace_cluster(self) -> Optional[Cluster]:
        return self._workspace_cluster

    @property
    def sent_workspace_notifications(self) -> List[WorkspaceNotification]:
        return self._sent_workspace_notifications

    def send_workspace_notification(self, notification: WorkspaceNotification):
        if self.inside_workspace():
            self._sent_workspace_notifications.append(notification)

    def _find_project_cloud_id_tuples_by_name(self, name):
        """Returns list of (cloud_id, project_id) tuples with name == name."""
        project_id_cloud_id_pairs = []
        for cloud_id, cloud_project_dict in self._project_to_id.items():
            for p_name, p_id in cloud_project_dict.items():
                if name == p_name:
                    project_id_cloud_id_pairs.append((cloud_id, p_id))
        return project_id_cloud_id_pairs

    def _get_project_id_by_name(
        self, *, parent_cloud_id: Optional[str] = None, name: Optional[str] = None
    ) -> str:
        # items of existing_projects are (cloud_id, project_id)
        existing_projects = self._find_project_cloud_id_tuples_by_name(name)
        if len(existing_projects) == 0:
            raise ValueError(f"Project '{name}' was not found.")
        else:
            for cloud_id, project_id in existing_projects:
                if cloud_id == parent_cloud_id:
                    return project_id
            raise ValueError(
                f"{len(existing_projects)} project(s) found with name '{name}' and none matched cloud_id '{parent_cloud_id}'"
            )

    def _get_project_id_by_cloud_id(
        self, *, parent_cloud_id: Optional[str] = None,
    ) -> str:
        workspace_cluster = self.get_current_workspace_cluster()
        if workspace_cluster is not None:
            if (
                workspace_cluster.cluster_compute_config is not None
                and workspace_cluster.cluster_compute_config.cloud_id == parent_cloud_id
            ):
                return workspace_cluster.project_id
            elif workspace_cluster.cluster_compute_id is not None:
                workspace_cluster_compute = self.get_compute_config(
                    workspace_cluster.cluster_compute_id
                )
                if (
                    workspace_cluster_compute is not None
                    and workspace_cluster_compute.config is not None
                    and workspace_cluster_compute.config.cloud_id == parent_cloud_id
                ):
                    return workspace_cluster.project_id

        return self.DEFAULT_PROJECT_ID

    def get_project_id(
        self,
        *,
        parent_cloud_id: Optional[str] = None,  # noqa: ARG002
        name: Optional[str] = None,  # noqa: ARG002
    ) -> str:
        if name is not None:
            return self._get_project_id_by_name(
                parent_cloud_id=parent_cloud_id, name=name
            )
        else:
            return self._get_project_id_by_cloud_id(parent_cloud_id=parent_cloud_id)

    def get_cloud_id(
        self,
        *,
        cloud_name: Optional[str] = None,
        compute_config_id: Optional[str] = None,
    ) -> str:
        assert not (cloud_name and compute_config_id)
        workspace_cluster = self.get_current_workspace_cluster()
        if workspace_cluster is not None:
            return self.WORKSPACE_CLOUD_ID

        if compute_config_id is not None:
            return self._compute_configs[compute_config_id].config.cloud_id

        if cloud_name is None:
            return self.DEFAULT_CLOUD_ID

        for cloud in self._clouds.values():
            if cloud.name == cloud_name:
                return cloud.id

        raise RuntimeError(f"Cloud with name '{cloud_name}' not found.")

    def get_image_uri_from_build_id(self, build_id: str) -> Optional[ImageURI]:
        cluster_env_build_id = self._builds[build_id].cluster_environment_id
        return self.get_cluster_env_build_image_uri(cluster_env_build_id)

    def add_build(self, build: ClusterEnvironmentBuild):
        self._builds[build.id] = build

    def add_image(self, image: ClusterEnvironment):
        self._images[image.id] = image

    def add_cloud(self, cloud: Cloud):
        self._clouds[cloud.id] = cloud
        self._system_cluster_status[cloud.id] = ClusterState.RUNNING

    def get_cloud(self, *, cloud_id: str) -> Optional[Cloud]:
        return self._clouds.get(cloud_id, None)

    def get_cloud_by_name(self, *, name: str) -> Optional[Cloud]:
        for c in self._clouds.values():
            if c.name == name:
                return c
        return None

    def get_default_cloud(self) -> Optional[Cloud]:
        return self._clouds.get(self.DEFAULT_CLOUD_ID, None)

    def add_cloud_collaborators(
        self, cloud_id: str, collaborators: List[CreateCloudCollaborator]
    ) -> None:
        existing_collaborators = [
            collaborator.email
            for collaborator in self._cloud_collaborators.get(cloud_id, [])
        ]

        for collaborator in collaborators:
            if collaborator.email in existing_collaborators:
                raise ValueError(
                    f"Collaborator with email '{collaborator.email}' already exists in cloud '{cloud_id}'."
                )

        if cloud_id not in self._cloud_collaborators:
            self._cloud_collaborators[cloud_id] = collaborators
        else:
            self._cloud_collaborators[cloud_id].extend(collaborators)

    def terminate_system_cluster(
        self, cloud_id: str
    ) -> Optional[ClusteroperationResponse]:
        self._system_cluster_status[cloud_id] = ClusterState.TERMINATING
        return ClusteroperationResponse(
            result=ClusterOperation(
                id="sop_123",
                completed=False,
                progress=None,
                result=None,
                cluster_id="fake-system-cluster-id",
                cluster_operation_type="terminate",
            )
        )

    def describe_system_workload_get_status(self, cloud_id: str) -> str:
        self._system_cluster_status[cloud_id] = ClusterState.TERMINATED
        return self._system_cluster_status[cloud_id]

    def add_compute_config(self, compute_config: DecoratedComputeTemplate) -> int:
        compute_config.version = (
            len(self._compute_config_name_to_ids[compute_config.name]) + 1
        )
        self._compute_configs[compute_config.id] = compute_config
        self._compute_config_name_to_ids[compute_config.name].append(compute_config.id)

        return compute_config.version

    def create_compute_config(
        self, config: ComputeTemplateConfig, *, name: Optional[str] = None
    ) -> Tuple[str, str]:
        unique_id = str(uuid.uuid4())
        compute_config_id = f"compute-config-id-{unique_id}"
        if name is None:
            anonymous = True
            name = f"anonymous-compute-config-{unique_id}"
        else:
            anonymous = False

        version = self.add_compute_config(
            DecoratedComputeTemplate(
                id=compute_config_id,
                name=name,
                config=config,
                anonymous=anonymous,
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            ),
        )
        return f"{name}:{version}", compute_config_id

    def get_compute_config(
        self, compute_config_id: str
    ) -> Optional[DecoratedComputeTemplate]:
        if compute_config_id in self._compute_configs:
            return self._compute_configs[compute_config_id]

        if compute_config_id in self._archived_compute_configs:
            return self._archived_compute_configs[compute_config_id]

        return None

    def get_compute_config_id(
        self,
        compute_config_name: Optional[str] = None,
        cloud: Optional[str] = None,
        *,
        include_archived=False,
    ) -> Optional[str]:
        if compute_config_name is not None:
            name, version = parse_cluster_compute_name_version(compute_config_name)
            if name not in self._compute_config_name_to_ids:
                return None

            if version is None:
                version = len(self._compute_config_name_to_ids[name])

            compute_config_id = self._compute_config_name_to_ids[name][version - 1]
            if (
                not include_archived
                and compute_config_id in self._archived_compute_configs
            ):
                return None

            return compute_config_id

        workspace_cluster = self.get_current_workspace_cluster()
        if workspace_cluster is not None:
            return workspace_cluster.cluster_compute_id

        cloud_id = self.get_cloud_id(cloud_name=cloud)
        return self.get_default_compute_config(cloud_id=cloud_id).id

    def archive_compute_config(self, *, compute_config_id: str):
        archived_config = self._compute_configs.pop(compute_config_id)
        archived_config.archived_at = datetime.utcnow()
        self._archived_compute_configs[compute_config_id] = archived_config

    def is_archived_compute_config(self, compute_config_id: str) -> bool:
        return compute_config_id in self._archived_compute_configs

    def set_default_compute_config(
        self, compute_config: ClusterCompute, *, cloud_id: str
    ):
        self._default_compute_configs[cloud_id] = compute_config

    def get_default_compute_config(self, *, cloud_id: str) -> ClusterCompute:
        return self._default_compute_configs[cloud_id]

    def list_cluster_env_builds(
        self, cluster_env_id: str,
    ) -> Generator[ClusterEnvironmentBuild, None, None]:
        for v in self._builds.values():
            if v.cluster_environment_id == cluster_env_id:
                yield v

    def get_non_default_cluster_env_builds(self) -> List[ClusterEnvironmentBuild]:
        return [
            v
            for v in self._builds.values()
            if v.id
            not in [
                self.DEFAULT_CLUSTER_ENV_BUILD_ID,
                self.WORKSPACE_CLUSTER_ENV_BUILD_ID,
            ]
        ]

    def get_default_build_id(self) -> str:
        workspace_cluster = self.get_current_workspace_cluster()
        if workspace_cluster is not None:
            return workspace_cluster.cluster_environment_build_id
        return self.DEFAULT_CLUSTER_ENV_BUILD_ID

    def get_cluster_env_build(self, build_id: str) -> Optional[ClusterEnvironmentBuild]:
        return self._builds.get(build_id, None)

    def get_cluster_env_by_name(self, name) -> Optional[ClusterEnvironment]:
        for v in self._images.values():
            if v.name == name:
                return v
        return None

    def get_cluster_env_build_id_from_containerfile(
        self,
        cluster_env_name: str,
        containerfile: str,
        anonymous: bool,
        ray_version: Optional[str] = None,  # noqa: ARG002
    ) -> str:
        for build in self._builds.values():
            if build.containerfile == containerfile:
                cluster_env = self._images.get(build.cluster_environment_id, None)  # type: ignore
                if cluster_env is not None and cluster_env.name == cluster_env_name:
                    return build.id  # type: ignore
        # create a new one if not found
        cluster_env_id = f"cluster-env-id-{uuid.uuid4()!s}"
        self._images[cluster_env_id] = ClusterEnvironment(
            id=cluster_env_id,
            name=cluster_env_name,
            anonymous=anonymous,
            local_vars_configuration=OPENAPI_NO_VALIDATION,
        )
        latest_build = None
        for build in self._builds.values():
            if build.cluster_environment_id == cluster_env_id and (latest_build is None or build.revision > latest_build.revision):  # type: ignore
                latest_build = build
        build_id = f"cluster-env-build-id-{uuid.uuid4()!s}"
        self._builds[build_id] = ClusterEnvironmentBuild(
            id=build_id,
            cluster_environment_id=cluster_env_id,
            containerfile=containerfile,
            status=ClusterEnvironmentBuildStatus.SUCCEEDED,
            local_vars_configuration=OPENAPI_NO_VALIDATION,
            ray_version=ray_version,
            revision=latest_build.revision + 1 if latest_build is not None else 1,  # type: ignore
        )
        return build_id

    def get_cluster_env_build_id_from_image_uri(
        self,
        image_uri: ImageURI,
        registry_login_secret: Optional[str] = None,
        ray_version: Optional[str] = None,
        name: Optional[str] = None,
    ) -> str:
        for build in self._builds.values():
            build_image_uri = self.get_cluster_env_build_image_uri(build.id)
            if (
                build_image_uri.image_uri == image_uri.image_uri
                if build_image_uri
                else False
            ):
                return build.id  # type: ignore
        cluster_env_id = f"cluster-env-id-{uuid.uuid4()!s}"
        cluster_env_name = name if name else image_uri.to_cluster_env_name()
        self._images[cluster_env_id] = ClusterEnvironment(
            id=cluster_env_id,
            name=cluster_env_name,
            anonymous=False,
            local_vars_configuration=OPENAPI_NO_VALIDATION,
        )
        build_id = f"cluster-env-build-id-{uuid.uuid4()!s}"
        self._builds[build_id] = ClusterEnvironmentBuild(
            id=build_id,
            cluster_environment_id=cluster_env_id,
            docker_image_name=image_uri.image_uri,
            status=ClusterEnvironmentBuildStatus.SUCCEEDED,
            registry_login_secret=registry_login_secret,
            ray_version=ray_version if ray_version else LATEST_RAY_VERSION,
            local_vars_configuration=OPENAPI_NO_VALIDATION,
        )
        return build_id

    def get_cluster_env_build_image_uri(
        self, cluster_env_build_id: str, use_image_alias: bool = False
    ) -> Optional[ImageURI]:
        build = self._builds.get(cluster_env_build_id, None)
        if build is None:
            return None
        else:
            if build.docker_image_name is not None and not use_image_alias:
                return ImageURI.from_str(build.docker_image_name)
            else:
                cluster_env = self._images[build.cluster_environment_id]
                return ImageURI.from_cluster_env_build(cluster_env, build)

    def update_service(self, model: DecoratedProductionServiceV2APIModel):
        self._services[model.id] = model

    def get_service(
        self,
        name: str,
        *,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        include_archived: bool = False,
    ) -> Optional[DecoratedProductionServiceV2APIModel]:
        cloud_id = self.get_cloud_id(cloud_name=cloud)
        cloud_project_dict = self._project_to_id.get(cloud_id, None)
        project_id = (
            cloud_project_dict.get(project, None) if cloud_project_dict else None
        )
        for service in self._services.values():
            if service.name == name and (
                project_id is None or service.project_id == project_id
            ):
                return service

        if include_archived:
            for service in self._archived_services.values():
                if service.name == name and (
                    project_id is None or service.project_id == project_id
                ):
                    return service

        return None

    def get_project(self, project_id: str) -> Optional[Project]:
        for cloud_project_dict in self._project_to_id.values():
            for p_name, p_id in cloud_project_dict.items():
                if p_id == project_id:
                    # return stub project
                    return Project(
                        name=p_name,
                        id=p_id,
                        local_vars_configuration=OPENAPI_NO_VALIDATION,
                    )
        return None

    def add_project_collaborators(
        self, project_id: str, collaborators: List[CreateUserProjectCollaborator]
    ):
        existing_collaborators = [
            collaborator.value.email if collaborator.value else None
            for collaborator in self._project_collaborators.get(project_id, [])
        ]

        for collaborator in collaborators:
            if (
                collaborator.value
                and collaborator.value.email in existing_collaborators
            ):
                raise ValueError(
                    f"Collaborator with email '{collaborator.value.email}' already exists in project '{project_id}'."
                )

        if project_id not in self._project_collaborators:
            self._project_collaborators[project_id] = collaborators
        else:
            self._project_collaborators[project_id].extend(collaborators)

    def get_job(
        self,
        *,
        name: Optional[str],
        job_id: Optional[str],
        cloud: Optional[str],
        project: Optional[str],
    ) -> Optional[ProductionJob]:
        if job_id is not None:
            return self._jobs.get(job_id, None)
        else:
            cloud_id = self.get_cloud_id(cloud_name=cloud)
            cloud_project_dict = self._project_to_id.get(cloud_id, None)
            project_id = (
                cloud_project_dict.get(project, None) if cloud_project_dict else None
            )
            result: ProductionJob = None
            for job in self._jobs.values():
                if (
                    job is not None
                    and job.name == name
                    and (project_id is None or job.project_id == project_id)
                    and (result is None or job.created_at > result.created_at)
                ):
                    result = job

        return result

    def get_job_runs(self, job_id: str) -> List[APIJobRun]:
        return self._job_runs.get(job_id, [])

    def update_job(self, model: ProductionJob):
        self._jobs[model.id] = model

    def update_job_run(self, prod_job_id: str, model: APIJobRun):
        self._job_runs[prod_job_id].append(model)

    def list_job_queues(self) -> List[DecoratedJobQueue]:
        return list(self._job_queues.values())

    def get_job_queue(self, job_queue_id: str) -> Optional[DecoratedJobQueue]:
        return self._job_queues.get(job_queue_id, None)

    def update_job_queue(self, model: DecoratedJobQueue):
        self._job_queues[model.id] = model

    def register_project_by_name(
        self,
        name: str,
        cloud: str = DEFAULT_CLOUD_NAME,
        project_id: Optional[str] = None,
    ) -> str:
        """Helper method to create project name to project id mapping."""
        cloud_id = self.get_cloud_id(cloud_name=cloud)
        if cloud_id not in self._project_to_id:
            self._project_to_id[cloud_id] = {}
        cloud_project_dict = self._project_to_id[cloud_id]
        if name in cloud_project_dict:
            return cloud_project_dict[name]
        else:
            if project_id is None:
                project_id = f"project-id-{uuid.uuid4()!s}"
            cloud_project_dict[name] = project_id
            return project_id

    @property
    def rolled_out_model(self) -> Optional[ApplyProductionServiceV2Model]:
        return self._rolled_out_model

    def rollout_service(
        self, model: ApplyProductionServiceV2Model
    ) -> DecoratedProductionServiceV2APIModel:
        self._rolled_out_model = model
        # TODO(mowen): This feels convoluted, is there a better way to pull cloud name and project name from the model?
        project_model = self.get_project(model.project_id)
        project = project_model.name if project_model else None
        compute_config = self.get_compute_config(model.compute_config_id)
        cloud_id = compute_config.config.cloud_id if compute_config else None
        cloud_model = self.get_cloud(cloud_id=cloud_id)
        cloud = cloud_model.name if cloud_model else None
        existing_service = self.get_service(model.name, project=project, cloud=cloud)
        if existing_service is not None:
            service_id = existing_service.id
        else:
            service_id = f"service-id-{uuid.uuid4()!s}"

        service = DecoratedProductionServiceV2APIModel(
            id=service_id,
            name=model.name,
            project_id=model.project_id,
            cloud_id=self.get_cloud_id(compute_config_id=model.compute_config_id),
            current_state=ServiceEventCurrentState.STARTING,
            base_url=f"http://{model.name}.fake.url",
            auth_token="fake-auth-token",
            primary_version=ProductionServiceV2VersionModel(
                id=str(uuid.uuid4()),
                created_at=datetime.now(),
                version="primary",
                current_state=ServiceVersionState.RUNNING,
                weight=100,
                build_id=model.build_id,
                compute_config_id=model.compute_config_id,
                ray_serve_config=model.ray_serve_config,
                ray_gcs_external_storage_config=model.ray_gcs_external_storage_config,
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            ),
            local_vars_configuration=OPENAPI_NO_VALIDATION,
        )
        self.update_service(service)
        return service

    @property
    def submitted_job(self) -> Optional[CreateInternalProductionJob]:
        return self._submitted_job

    @property
    def rolled_back_service(self) -> Optional[Tuple[str, Optional[int]]]:
        return self._rolled_back_service

    def rollback_service(
        self, service_id: str, *, max_surge_percent: Optional[int] = None
    ):
        self._rolled_back_service = (service_id, max_surge_percent)

    @property
    def terminated_service(self) -> Optional[str]:
        return self._terminated_service

    def terminate_service(self, service_id: str):
        self._terminated_service = service_id
        self._services[service_id].current_state = ServiceEventCurrentState.TERMINATED
        self._services[service_id].canary_version = None
        if self._services[service_id].primary_version is not None:
            # The backend leaves the primary_version populated upon termination.
            self._services[service_id].primary_version.weight = 100
            self._services[
                service_id
            ].primary_version.current_state = ServiceVersionState.TERMINATED

    @property
    def archived_services(self) -> Dict[str, DecoratedProductionServiceV2APIModel]:
        return self._archived_services

    def archive_service(self, service_id: str):
        self._archived_services[service_id] = self._services.pop(service_id)

    @property
    def deleted_services(self) -> Dict[str, DecoratedProductionServiceV2APIModel]:
        return self._deleted_services

    def delete_service(self, service_id: str):
        self._deleted_services[service_id] = self._services.pop(service_id)

    def submit_job(self, model: CreateInternalProductionJob) -> InternalProductionJob:
        self._submitted_job = model

        job = InternalProductionJob(
            id=f"job-{uuid.uuid4()!s}",
            name=model.name,
            config=model.config,
            state=ProductionJobStateTransition(
                current_state=HaJobStates.PENDING,
                goal_state=HaJobGoalStates.SUCCESS,
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            ),
            project_id=model.project_id,
            local_vars_configuration=OPENAPI_NO_VALIDATION,
        )

        self.update_job(job)
        return job

    def terminate_job(self, job_id: str):
        self._jobs[job_id].state = HaJobStates.TERMINATED

    def archive_job(self, job_id: str):
        self._archived_jobs[job_id] = self._jobs.pop(job_id)

    def is_archived_job(self, job_id: str) -> bool:
        return job_id in self._archived_jobs

    def upload_local_dir_to_cloud_storage(
        self,
        local_dir: str,  # noqa: ARG002
        *,
        cloud_id: str,
        excludes: Optional[List[str]] = None,  # noqa: ARG002
        overwrite_existing_file: bool = False,  # noqa: ARG002
    ) -> str:
        # Ensure that URIs are consistent for the same passed directory.
        bucket = self.CLOUD_BUCKET.format(cloud_id=cloud_id)
        if local_dir not in self._upload_uri_mapping:
            self._upload_uri_mapping[
                local_dir
            ] = f"{bucket}/fake_pkg_{str(uuid.uuid4())}.zip"

        return self._upload_uri_mapping[local_dir]

    def add_job_run_logs(self, job_run_id: str, logs: str):
        self._job_run_logs[job_run_id] = logs

    def logs_for_job_run(
        self,
        job_run_id: str,
        head: bool = False,  # noqa: ARG002
        tail: bool = True,  # noqa: ARG002
        max_lines: Optional[int] = None,  # noqa: ARG002
        parse_json: Optional[bool] = None,  # noqa: ARG002
    ) -> str:
        log_lines = self._job_run_logs.get(job_run_id, "").splitlines()
        if max_lines is None:
            max_lines = len(log_lines)
        if head:
            return "\n".join(log_lines[:max_lines])
        else:
            return "\n".join(log_lines[-1 * max_lines :])

    def add_controller_logs(self, service_version_id: str, logs: str):
        self._controller_logs[service_version_id] = logs

    def controller_logs_for_service_version(
        self,
        service_version: ProductionServiceV2VersionModel,
        head: bool = False,
        max_lines: Optional[int] = None,
        parse_json: Optional[bool] = None,  # noqa: ARG002
    ) -> str:
        log_lines = self._controller_logs.get(service_version.id, "").splitlines()
        if max_lines is None:
            max_lines = len(log_lines)
        if head:
            return "\n".join(log_lines[:max_lines])
        else:
            return "\n".join(log_lines[-1 * max_lines :])

    def get_schedule(
        self,
        *,
        name: Optional[str],
        id: Optional[str],  # noqa: A002
        cloud: Optional[str],
        project: Optional[str],
    ) -> Optional[DecoratedSchedule]:
        if id is not None:
            return self._schedules.get(id, None)
        else:
            cloud_id = self.get_cloud_id(cloud_name=cloud)
            cloud_project_dict = self._project_to_id.get(cloud_id, None)
            project_id = (
                cloud_project_dict.get(project, None) if cloud_project_dict else None
            )
            result: DecoratedSchedule = None
            for schedule in self._schedules.values():
                if (
                    schedule is not None
                    and schedule.name == name
                    and (project_id is None or schedule.project_id == project_id)
                ):
                    result = schedule
                    break

        return result

    def update_schedule(self, model: DecoratedSchedule):
        self._schedules[model.id] = model

    def apply_schedule(self, model: CreateSchedule) -> DecoratedSchedule:
        schedule = DecoratedSchedule(
            id=f"sched-{uuid.uuid4()!s}",
            name=model.name,
            project_id=model.project_id,
            config=model.config,
            schedule=model.schedule,
            # Fill in dummy time to represent schedule is enabled.
            next_trigger_at=self.SCHEDULE_NEXT_TRIGGER_AT_TIME,
            local_vars_configuration=OPENAPI_NO_VALIDATION,
        )

        self.update_schedule(schedule)
        return schedule

    def set_schedule_state(self, id: str, is_paused: bool):  # noqa: A002
        if is_paused:
            self._schedules[id].next_trigger_at = None
        else:
            self._schedules[id].next_trigger_at = self.SCHEDULE_NEXT_TRIGGER_AT_TIME

    def schedule_is_enabled(self, id: str) -> bool:  # noqa: A002
        return self._schedules[id].next_trigger_at is not None

    def trigger_schedule(self, id: str):  # noqa: A002
        self._schedule_trigger_counts[id] += 1

    def trigger_counts(self, id: str):  # noqa: A002
        return self._schedule_trigger_counts[id]

    def get_dataset(
        self, name: str, version: Optional[int], project: Optional[str]  # noqa: ARG002
    ) -> Dataset:
        raise NotImplementedError

    def upload_dataset(
        self,
        dataset_file: str,  # noqa: ARG002
        name: Optional[str],  # noqa: ARG002
        description: Optional[str],  # noqa: ARG002
        cloud: Optional[str],  # noqa: ARG002
        project: Optional[str],  # noqa: ARG002
    ) -> Dataset:
        raise NotImplementedError

    def download_dataset(
        self, name: str, version: Optional[int], project: Optional[str]  # noqa: ARG002
    ) -> bytes:
        return b""

    def list_datasets(
        self,
        limit: Optional[int] = None,  # noqa: ARG002
        after: Optional[str] = None,  # noqa: ARG002
        name_contains: Optional[str] = None,  # noqa: ARG002
        cloud: Optional[str] = None,  # noqa: ARG002
        project: Optional[str] = None,  # noqa: ARG002
    ) -> ListResponse[Dataset]:
        raise NotImplementedError

    def get_finetuned_model(
        self, model_id: Optional[str], job_id: Optional[str]  # noqa: ARG002
    ) -> FineTunedModel:
        return FineTunedModel(
            id=model_id if model_id else "test-model-id",
            model_id=model_id if model_id else "test-model-id",
            base_model_id="my_base_model_id",
            ft_type=FineTuneType.LORA,
            creator_id="",
            creator_email="",
            created_at=datetime.utcnow(),
            storage_uri="s3://fake_bucket/fake_folder/",
        )

    def create_workspace(self, model: CreateExperimentalWorkspace) -> str:
        workspace_id = uuid.uuid4()

        # this usually happens on the backend
        compute_config = self.get_compute_config(model.compute_config_id)
        assert compute_config is not None
        compute_config.idle_timeout_minutes = model.idle_timeout_minutes

        workspace = ExperimentalWorkspace(
            id=f"workspace-id-{workspace_id!s}",
            name=model.name,
            project_id=model.project_id or self.get_project_id(),
            compute_config_id=model.compute_config_id,
            environment_id=model.cluster_environment_build_id,
            cloud_id=model.cloud_id or self.get_cloud_id(),
            created_at=datetime.utcnow(),
            creator_id=self.DEFAULT_USER_ID,
            creator_email=self.DEFAULT_USER_EMAIL,
            organization_id=self.DEFAULT_ORGANIZATION_ID,
            cluster_id=self.DEFAULT_CLOUD_ID,
            state=SessionState.RUNNING
            if not model.skip_start
            else SessionState.TERMINATED,
        )
        self._workspaces[workspace.id] = workspace
        return workspace.id

    def get_workspace(
        self,
        *,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ) -> Optional[ExperimentalWorkspace]:
        if id is not None:
            return self._workspaces.get(id, None)
        else:
            cloud_id = self.get_cloud_id(cloud_name=cloud)
            cloud_project_dict = self._project_to_id.get(cloud_id, None)
            project_id = (
                cloud_project_dict.get(project, None) if cloud_project_dict else None
            )
            result: ExperimentalWorkspace = None
            for workspace in self._workspaces.values():
                if (
                    workspace is not None
                    and workspace.name == name
                    and (project_id is None or workspace.project_id == project_id)
                ):
                    result = workspace
                    break

        return result

    @property
    def workspaces(self) -> Dict[str, ExperimentalWorkspace]:
        return self._workspaces

    def start_workspace(self, workspace_id: str):
        workspace = self._workspaces.get(workspace_id, None)
        if workspace is None:
            raise ValueError(f"Workspace '{workspace_id}' not found.")
        workspace.state = SessionState.RUNNING

    def terminate_workspace(self, workspace_id: str):
        workspace = self._workspaces.get(workspace_id, None)
        if workspace is None:
            raise ValueError(f"Workspace '{workspace_id}' not found.")
        workspace.state = SessionState.TERMINATED

    def update_workspace_dependencies_offline_only(
        self, workspace_id: Optional[str], requirements: List[str]
    ):
        assert workspace_id is not None
        self._workspaces_dependencies[workspace_id] = requirements

    def update_workspace_env_vars_offline_only(
        self, workspace_id: Optional[str], env_vars: Dict[str, str]
    ):
        assert workspace_id is not None
        self._workspaces_env_vars[workspace_id] = env_vars

    def get_workspace_cluster(
        self, workspace_id: Optional[str]
    ) -> Optional[DecoratedSession]:
        workspace_model = (
            self._workspaces.get(workspace_id, None) if workspace_id else None
        )
        compute_config = self.get_compute_config(workspace_model.compute_config_id)
        assert compute_config is not None
        return Mock(
            name=f"workspace-cluster-{workspace_model.name}",
            build_id=workspace_model.environment_id,
            state=workspace_model.state,
            project_id=workspace_model.project_id,
            cloud_id=workspace_model.cloud_id,
            idle_timeout=compute_config.idle_timeout_minutes,
        )

    def get_workspace_proxied_dataplane_artifacts(
        self, workspace_id: str
    ) -> WorkspaceDataplaneProxiedArtifacts:
        env_vars_dict = self._workspaces_env_vars.get(workspace_id, None)
        return WorkspaceDataplaneProxiedArtifacts(
            requirements=self._workspaces_dependencies.get(workspace_id, None),
            environment_variables=[
                f"{key}={value}" for key, value in env_vars_dict.items()
            ]
            if env_vars_dict
            else None,
        )

    def get_cluster_head_node_ip(self, cluster_id: str) -> str:
        return self._clusters_headnode_ip.get(cluster_id, "")

    def get_cluster_ssh_key(self, cluster_id: str) -> SessionSshKey:
        return self._clusters_ssh_key.get(cluster_id, None)  # type: ignore

    def get_workspace_default_dir_name(self, workspace_id) -> str:
        workspace = self._workspaces.get(workspace_id, None)
        if workspace is None:
            raise ValueError(f"Workspace '{workspace_id}' not found.")
        return "default"

    def delete_finetuned_model(self, model_id: str) -> DeletedPlatformFineTunedModel:
        return DeletedPlatformFineTunedModel(id=model_id, deleted_at=datetime.utcnow())

    def list_finetuned_models(
        self,
        cloud_id: Optional[str],  # noqa: ARG002
        project_id: Optional[str],  # noqa: ARG002
        max_items: int,
    ) -> List[FineTunedModel]:
        return [
            FineTunedModel(
                id="test-model-id",
                model_id="test-model-id",
                base_model_id="my_base_model_id",
                ft_type=FineTuneType.LORA,
                creator_id="",
                creator_email="",
                created_at=datetime.utcnow(),
                storage_uri="s3://fake_bucket/fake_folder/",
            )
            for _ in range(max_items)
        ]

    def update_workspace(
        self,
        *,
        workspace_id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        compute_config_id: Optional[str] = None,
        cluster_environment_build_id: Optional[str] = None,
        idle_timeout_minutes: Optional[int] = None,
    ):
        if workspace_id not in self._workspaces:
            raise ValueError(f"Workspace '{workspace_id}' not found.")

        workspace = self._workspaces[workspace_id]

        if name:
            workspace.name = name

        if compute_config_id:
            workspace.compute_config_id = compute_config_id

        if cluster_environment_build_id:
            workspace.environment_id = cluster_environment_build_id

        if idle_timeout_minutes:
            workspace.idle_timeout_minutes = idle_timeout_minutes

            compute_config = self.get_compute_config(workspace.compute_config_id)
            assert compute_config is not None
            compute_config.idle_timeout_minutes = idle_timeout_minutes

    def download_aggregated_instance_usage_csv(
        self,
        start_date: date,
        end_date: date,
        cloud_id: Optional[str] = None,  # noqa: ARG002
        project_id: Optional[str] = None,  # noqa: ARG002
        directory: Optional[str] = None,
        hide_progress_bar: bool = False,  # noqa: ARG002
    ) -> str:
        filename = f"aggregated_instance_usage_{start_date}_{end_date}.zip"
        if directory:
            filepath = os.path.join(directory, filename)
        else:
            filepath = filename

        return filepath

    def create_api_key(
        self, duration: float, user_id: Optional[str]  # noqa: ARG002
    ) -> ServerSessionToken:
        api_key = f"{uuid.uuid4()!s}"
        api_keys = self._api_keys.get(user_id or "usr_1", [])
        self._api_keys[user_id or "usr_1"] = api_keys + [api_key]

        return ServerSessionToken(server_session_id=api_key)

    def rotate_api_key(self, user_id: str) -> None:
        if user_id not in self._api_keys:
            raise ValueError(f"User '{user_id}' not found.")
        self._api_keys[user_id] = [f"{uuid.uuid4()!s}"]

    def admin_batch_create_users(
        self, admin_create_users: List[AdminCreateUser]
    ) -> List[AdminCreatedUser]:
        created_users = []
        for admin_create_user in admin_create_users:
            if admin_create_user.email in self._users:
                raise ValueError(
                    f"User with email '{admin_create_user.email}' already exists."
                )

            user_id = f"user-id-{uuid.uuid4()!s}"
            created_user = AdminCreatedUser(
                user_id=user_id,
                email=admin_create_user.email,
                created_at=datetime.utcnow(),
                name=admin_create_user.name,
                lastname=admin_create_user.lastname,
                title=admin_create_user.title,
                is_sso_user=admin_create_user.is_sso_user,
            )
            created_users.append(created_user)
            self._users[admin_create_user.email] = created_user

        return created_users

    def create_organization_invitations(
        self, emails: List[str]
    ) -> Tuple[List[str], List[str]]:
        success_emails, error_messages = [], []
        for email in emails:
            if email in self._users:
                error_messages.append(
                    f"User with email {email} is already a member of your organization."
                )
            else:
                orginv_id = f"orginv_{uuid.uuid4()!s}"
                self._organization_invitations[email] = OrganizationInvitation(
                    email=email,
                    id=orginv_id,
                    organization_id="org_1",
                    created_at=datetime.utcnow(),
                    expires_at=datetime.utcnow(),
                )
                success_emails.append(email)

        return success_emails, error_messages

    def list_organization_invitations(self) -> List[OrganizationInvitation]:
        return list(self._organization_invitations.values())

    def delete_organization_invitation(self, email: str) -> OrganizationInvitation:
        if email not in self._organization_invitations:
            raise ValueError(f"Invitation for email '{email}' not found.")

        return self._organization_invitations.pop(email)

    def get_organization_collaborators(
        self,
        email: Optional[str] = None,
        name: Optional[str] = None,
        is_service_account: Optional[bool] = None,  # noqa: ARG002
    ) -> List[OrganizationCollaborator]:
        # Since organization collaborator doesn't include whether it's a service account or not, we'll just return all
        results = []
        for organization_collaborator in self._organization_collaborators:
            if email and organization_collaborator.email != email:
                continue
            if name and organization_collaborator.name != name:
                continue

            results.append(organization_collaborator)

        return results

    def delete_organization_collaborator(self, identity_id: str) -> None:
        for organization_collaborator in self._organization_collaborators:
            if organization_collaborator.id == identity_id:
                self._organization_collaborators.remove(organization_collaborator)
                return

        raise ValueError(
            f"Organization collaborator with id '{identity_id}' not found."
        )

    def create_service_account(self, name) -> AnyscaleServiceAccount:
        for organization_collaborator in self._organization_collaborators:
            if organization_collaborator.name == name:
                raise ValueError(f"Service account with name '{name}' already exists.")

        identity_id = f"id_{uuid.uuid4()!s}"
        user_id = f"usr_{uuid.uuid4()!s}"
        organization_collaborator = OrganizationCollaborator(
            permission_level=OrganizationPermissionLevel.COLLABORATOR,
            id=identity_id,
            name=name,
            email=f"{name}@service-account.com",
            user_id=user_id,
            created_at=datetime.utcnow(),
        )

        self._organization_collaborators.append((organization_collaborator))

        return AnyscaleServiceAccount(
            user_id=organization_collaborator.user_id,
            name=organization_collaborator.name,
            organization_id="org_1",
            email=organization_collaborator.email,
            permission_level=organization_collaborator.permission_level,
            created_at=organization_collaborator.created_at,
        )

    def create_resource_quota(
        self, create_resource_quota: CreateResourceQuota
    ) -> ResourceQuota:
        resource_quota_id = f"rq_{uuid.uuid4()!s}"
        resource_quota = ResourceQuota(
            id=resource_quota_id,
            name=create_resource_quota.name,
            cloud_id=create_resource_quota.cloud_id,
            project_id=create_resource_quota.project_id,
            quota=create_resource_quota.quota,
            is_enabled=True,
            created_at=datetime.utcnow(),
            creator=MiniUser(
                id="user_1",
                email="test@anyscale.com",
                name="Test User",
                username="testuser",
            ),
            cloud=MiniCloud(
                id=create_resource_quota.cloud_id,
                name="Test Cloud",
                provider=CloudProviders.AWS,
            ),
        )

        self._resource_quotas[resource_quota_id] = resource_quota

        return self._resource_quotas[resource_quota_id]

    def list_resource_quotas(
        self,
        name: Optional[str] = None,
        cloud_id: Optional[str] = None,
        creator_id: Optional[str] = None,
        is_enabled: Optional[bool] = None,
        max_items: int = 20,
    ) -> List[ResourceQuota]:
        results = []
        for resource_quota in self._resource_quotas.values():
            if name and resource_quota.name != name:
                continue
            if cloud_id and resource_quota.cloud_id != cloud_id:
                continue
            if creator_id and resource_quota.creator.id != creator_id:
                continue
            if is_enabled is not None and resource_quota.is_enabled != is_enabled:
                continue
            results.append(resource_quota)

        return results[:max_items]

    def delete_resource_quota(self, resource_quota_id: str) -> None:
        if resource_quota_id not in self._resource_quotas:
            raise ValueError(f"Resource Quota with id '{resource_quota_id}' not found.")

        self._resource_quotas.pop(resource_quota_id)

    def set_resource_quota_status(
        self, resource_quota_id: str, is_enabled: bool
    ) -> None:
        resource_quota = self._resource_quotas.get(resource_quota_id)
        if resource_quota is None:
            raise ValueError(f"Resource Quota with id '{resource_quota_id}' not found.")

        resource_quota.is_enabled = is_enabled

    def get_service_by_id(
        self, service_id: str
    ) -> Optional[DecoratedProductionServiceV2APIModel]:
        if service_id in self._services:
            return self._services[service_id]
        if service_id in self._archived_services:
            return self._archived_services[service_id]
        if service_id in self._deleted_services:
            return self._deleted_services[service_id]
        return None

    def list_services(
        self,
        *,
        name: Optional[str] = None,
        state_filter: Optional[List[str]] = None,
        creator_id: Optional[str] = None,  # noqa: ARG002
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        include_archived: bool = False,
        count: Optional[int] = None,
        paging_token: Optional[str] = None,  # noqa: ARG002
        sort_field: Optional[str] = None,  # noqa: ARG002
        sort_order: Optional[str] = None,  # noqa: ARG002
    ) -> DecoratedlistserviceapimodelListResponse:
        target_services = list(self._services.values())
        if include_archived:
            target_services.extend(list(self._archived_services.values()))

        target_cloud_id = self.get_cloud_id(cloud_name=cloud) if cloud else None
        target_project_id = (
            self.get_project_id(parent_cloud_id=target_cloud_id, name=project)
            if project
            else None
        )

        filtered_results = []
        for svc in target_services:
            if name is not None and svc.name != name:
                continue
            # Ensure state comparison works whether svc.current_state is Enum or str
            current_state_str = (
                svc.current_state.value
                if hasattr(svc.current_state, "value")
                else svc.current_state
            )
            if state_filter is not None and current_state_str not in state_filter:
                continue
            if target_project_id is not None and svc.project_id != target_project_id:
                continue
            if target_cloud_id is not None and svc.cloud_id != target_cloud_id:
                continue

            filtered_results.append(svc)

        if count is None:
            count = len(filtered_results)
        final_results = filtered_results[:count]

        response = DecoratedlistserviceapimodelListResponse(
            results=final_results,
            metadata=ListResponseMetadata(
                total=len(final_results),
                next_paging_token=None,  # Fake doesn't support paging
            ),
            local_vars_configuration=OPENAPI_NO_VALIDATION,
        )
        return response
