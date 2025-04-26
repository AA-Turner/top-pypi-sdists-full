import asyncio
import datetime
import logging
import random
import string
import weakref
from typing import AsyncGenerator, Optional

import grpc
from flyteidl.core import security_pb2 as _security_pb2
from flyteidl.core import tasks_pb2 as _tasks_pb2
from flytekit import WorkflowExecutionPhase
from flytekit.configuration import Config
from flytekit.models.core.execution import TaskExecutionPhase
from flytekit.models.execution import Execution
from flytekit.models.filters import Equal, ValueIn

from union.cli._common import _get_channel_with_org
from union.internal.common import identifier_pb2 as _identifier_pb2
from union.internal.common import list_pb2 as _list_pb2
from union.internal.workspace.workspace_definition_payload_pb2 import (
    CreateWorkspaceDefinitionRequest,
    CreateWorkspaceDefinitionResponse,
    GetWorkspaceDefinitionRequest,
    GetWorkspaceDefinitionResponse,
    ListWorkspaceDefinitionsRequest,
    ListWorkspaceDefinitionsResponse,
)
from union.internal.workspace.workspace_definition_pb2 import (
    WorkspaceDefinitionIdentifier,
    WorkspaceDefinitionSpec,
    WorkspaceDefinitionState,
)
from union.internal.workspace.workspace_definition_service_pb2_grpc import WorkspaceRegistryServiceStub
from union.internal.workspace.workspace_instance_payload_pb2 import (
    GetWorkspaceInstanceRequest,
    GetWorkspaceInstanceResponse,
    ListWorkspaceInstancesRequest,
    ListWorkspaceInstancesResponse,
    StartWorkspaceInstanceRequest,
    StartWorkspaceInstanceResponse,
    StopWorkspaceInstanceRequest,
    WatchWorkspaceInstancesRequest,
    WatchWorkspaceInstancesResponse,
)
from union.internal.workspace.workspace_instance_pb2 import (
    WorkspaceInstanceIdentifier,
    WorkspaceInstanceStatus,
)
from union.internal.workspace.workspace_instance_service_pb2_grpc import WorkspaceInstanceServiceStub
from union.remote import UnionRemote
from union.workspace._config import WorkspaceConfig

VERSION_STRING_LENGTH = 20
VSCODE_DEBUGGER_LOG_NAME = "VS Code Debugger"

_logger = logging.getLogger(__name__)


class WorkspaceRemote:
    def __init__(
        self,
        default_project: str,
        default_domain: str,
        config: Optional[Config] = None,
        union_remote: Optional[UnionRemote] = None,
    ):
        if union_remote is None:
            union_remote = UnionRemote(config=config, default_domain=default_domain, default_project=default_project)
            self._union_remote = union_remote
            self._union_remote_ref = weakref.ref(self._union_remote)
        else:
            # Union remote is passed in directly. We assume that the caller will have a reference to `AppRemote`.
            self._union_remote_ref = weakref.ref(union_remote)

        self.config = union_remote.config
        self.default_project = union_remote.default_project
        self.default_domain = union_remote.default_domain

    @property
    def union_remote(self) -> UnionRemote:
        union_remote = self._union_remote_ref()
        if union_remote is None:
            raise ValueError("Unable to find union remote")
        return union_remote

    def get_workspace_definition_id(
        self,
        workspace_definition_name: str,
        project: Optional[str] = None,
        domain: Optional[str] = None,
        version: Optional[str] = None,
    ) -> WorkspaceDefinitionIdentifier:
        return WorkspaceDefinitionIdentifier(
            org=self.org,
            project=project or self.default_project,
            domain=domain or self.default_domain,
            name=workspace_definition_name,
            version=version or f"{workspace_definition_name}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
        )

    def get_workspace_instance_id(
        self,
        workspace_instance_name: str,
        project: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> WorkspaceInstanceIdentifier:
        return WorkspaceInstanceIdentifier(
            org=self.org,
            project=project or self.default_project,
            domain=domain or self.default_domain,
            name=workspace_instance_name,
            host=self.org,
        )

    async def workspace_instance_is_stopping(
        self,
        workspace_instance_name: str,
        project: Optional[str] = None,
        domain: Optional[str] = None,
        logger: Optional[logging.Logger] = _logger,
    ) -> bool:
        """
        Check if the workspace instance is terminated or terminating.
        """
        workspace_instance_id = self.get_workspace_instance_id(
            workspace_instance_name=workspace_instance_name,
            project=project or self.default_project,
            domain=domain or self.default_domain,
        )
        logger.info(f"GetWorkspaceInstance {workspace_instance_id}")
        response: GetWorkspaceInstanceResponse = await self.instance_async_client.GetWorkspaceInstance(
            GetWorkspaceInstanceRequest(id=workspace_instance_id)
        )
        return response.workspace_instance.spec.status.phase in (
            WorkspaceInstanceStatus.WorkspaceInstancePhase.WORKSPACE_INSTANCE_PHASE_TERMINATING,
            WorkspaceInstanceStatus.WorkspaceInstancePhase.WORKSPACE_INSTANCE_PHASE_TERMINATED,
        )

    async def watch_workspace_instance(
        self,
        workspace_instance_name: str,
        project: Optional[str] = None,
        domain: Optional[str] = None,
        logger: Optional[logging.Logger] = _logger,
    ) -> AsyncGenerator[bool, None]:
        """
        Watch the workspace instance for stopping event.
        """

        logger.info(f"Watching workspace instance {workspace_instance_name} in project {project} and domain {domain}")

        workspace_instance_id = self.get_workspace_instance_id(
            workspace_instance_name=workspace_instance_name,
            project=project or self.default_project,
            domain=domain or self.default_domain,
        )
        watch_request = WatchWorkspaceInstancesRequest(workspace_instance_id=workspace_instance_id)

        response: WatchWorkspaceInstancesResponse
        logger.info(f"WatchWorkspaceInstances request {watch_request}")

        stream = self.instance_async_client.WatchWorkspaceInstances(watch_request)
        while True:
            try:
                async for response in stream:
                    logger.info(f"WatchWorkspaceInstances response {response}")
                    is_stopping = response.WhichOneof("event") == "stopping_event"
                    logger.info(f"Workspace instance is stopping: {is_stopping}")
                    yield is_stopping
                    if is_stopping:
                        return
            except Exception as exc:
                logger.info(f"Error watching workspace instance {exc}, resetting stream")
                stream = self.instance_async_client.WatchWorkspaceInstances(watch_request)
                continue

    async def _create_workspace_definition(
        self,
        workspace_config: WorkspaceConfig,
        version: Optional[str] = None,
        create_workspace_definition_entity: bool = True,
    ) -> CreateWorkspaceDefinitionResponse:
        """
        Create a workspace definition.

        :param workspace_config: The workspace config to create the workspace definition from.
        :param version: The version of the workspace definition.
        :param create_workspace_definition_entity: Whether to create the workspace definition entity.
        """
        workspace_definition_id = self.get_workspace_definition_id(
            workspace_definition_name=workspace_config.name,
            project=workspace_config.project,
            domain=workspace_config.domain,
            version=version,
        )

        kwargs = {}
        if workspace_config.resources:
            kwargs["resources"] = _tasks_pb2.Resources(
                requests=[
                    _tasks_pb2.Resources.ResourceEntry(name=name, value=value)
                    for name, value in (
                        (_tasks_pb2.Resources.ResourceName.CPU, workspace_config.resources.cpu),
                        (_tasks_pb2.Resources.ResourceName.MEMORY, workspace_config.resources.mem),
                        (_tasks_pb2.Resources.ResourceName.GPU, workspace_config.resources.gpu),
                        (
                            _tasks_pb2.Resources.ResourceName.EPHEMERAL_STORAGE,
                            workspace_config.resources.ephemeral_storage,
                        ),
                    )
                    if value is not None
                ],
            )
        if workspace_config.accelerator:
            kwargs["extended_resources"] = _tasks_pb2.ExtendedResources(
                gpu_accelerator=_tasks_pb2.GPUAccelerator(
                    device=workspace_config.accelerator,
                    unpartitioned=True,
                ),
            )
        if workspace_config.secrets:
            kwargs["security_context"] = _security_pb2.SecurityContext(
                secrets=[secret.to_flyte_idl() for secret in workspace_config.secrets]
            )

        workspace_definition_spec = WorkspaceDefinitionSpec(
            short_description=workspace_config.description,
            state=WorkspaceDefinitionState.WORKSPACE_DEFINITION_STATE_ACTIVE,
            ttl_seconds=workspace_config.ttl_seconds,
            on_startup=workspace_config.on_startup,
            container_image=workspace_config.container_image,
            workspace_root=workspace_config.workspace_root,
            working_dir=workspace_config.working_dir,
            **kwargs,
        )
        create_request = CreateWorkspaceDefinitionRequest(
            id=workspace_definition_id,
            workspace_spec=workspace_definition_spec,
            create_workspace_definition_entity=create_workspace_definition_entity,
        )
        try:
            response: CreateWorkspaceDefinitionResponse = await self.definition_async_client.CreateWorkspaceDefinition(
                create_request
            )
        except Exception as e:
            raise RuntimeError(f"Failed to create workspace definition: {e}") from e
        return response

    async def create_workspace_definition(
        self,
        workspace_config: WorkspaceConfig,
        version: Optional[str] = None,
    ) -> CreateWorkspaceDefinitionResponse:
        try:
            return await self._create_workspace_definition(
                workspace_config=workspace_config,
                version=version,
                create_workspace_definition_entity=True,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to create workspace definition: {e}") from e

    async def update_workspace_definition(
        self,
        workspace_config: WorkspaceConfig,
        version: Optional[str] = None,
    ) -> CreateWorkspaceDefinitionResponse:
        try:
            return await self._create_workspace_definition(
                workspace_config=workspace_config,
                version=version,
                create_workspace_definition_entity=False,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to update workspace definition: {e}") from e

    async def get_workspace_definition(
        self,
        workspace_definition_name: str,
        project: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> GetWorkspaceDefinitionResponse:
        get_request = GetWorkspaceDefinitionRequest(
            id=WorkspaceDefinitionIdentifier(
                org=self.org,
                project=project or self.default_project,
                domain=domain or self.default_domain,
                name=workspace_definition_name,
            )
        )
        response: GetWorkspaceDefinitionResponse = await self.definition_async_client.GetWorkspaceDefinition(
            get_request
        )
        return response

    async def list_workspace_definitions(
        self,
        workspace_definition_name: Optional[str] = None,
        project: Optional[str] = None,
        domain: Optional[str] = None,
        sort_by: str = "created_at",
        direction: str = "desc",
    ) -> ListWorkspaceDefinitionsResponse:
        list_request = ListWorkspaceDefinitionsRequest(
            org=self.org,
            project=project or self.default_project,
            domain=domain or self.default_domain,
            name=workspace_definition_name,
            request=_list_pb2.ListRequest(
                limit=1000,
                sort_by=_list_pb2.Sort(
                    key=sort_by,
                    direction=(
                        _list_pb2.Sort.Direction.DESCENDING
                        if direction == "desc"
                        else _list_pb2.Sort.Direction.ASCENDING
                    ),
                ),
            ),
        )
        return await self.definition_async_client.ListWorkspaceDefinitions(list_request)

    async def get_latest_workspace_definition_id(
        self,
        workspace_definition_name: str,
        project: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> WorkspaceDefinitionIdentifier:
        list_request = ListWorkspaceDefinitionsRequest(
            org=self.org,
            project=project or self.default_project,
            domain=domain or self.default_domain,
            name=workspace_definition_name,
            request=_list_pb2.ListRequest(
                limit=1,
                sort_by=_list_pb2.Sort(
                    key="created_at",
                    direction=_list_pb2.Sort.Direction.DESCENDING,
                ),
            ),
        )
        list_response: ListWorkspaceDefinitionsResponse = await self.definition_async_client.ListWorkspaceDefinitions(
            list_request
        )
        if len(list_response.workspace_definitions) == 0:
            raise RuntimeError(f"Workspace definition {workspace_definition_name} not found")
        return self.get_workspace_definition_id(
            workspace_definition_name=workspace_definition_name,
            project=project,
            domain=domain,
            version=list_response.workspace_definitions[0].id.version,
        )

    async def get_latest_workspace_instance_uri(
        self,
        workspace_definition_name: str,
        version: str,
        project: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> str:
        workspace_definition_id = self.get_workspace_definition_id(
            workspace_definition_name=workspace_definition_name,
            project=project or self.default_project,
            domain=domain or self.default_domain,
            version=version,
        )
        list_request = ListWorkspaceInstancesRequest(
            request=_list_pb2.ListRequest(
                limit=1,
                sort_by=_list_pb2.Sort(
                    key="created_at",
                    direction=_list_pb2.Sort.Direction.DESCENDING,
                ),
            ),
            org=self.org,
            project=_identifier_pb2.ProjectIdentifier(
                organization=self.org,
                domain=domain or self.default_domain,
                name=project or self.default_project,
            ),
            workspace_definition_id=workspace_definition_id,
        )
        list_response: ListWorkspaceInstancesResponse = await self.instance_async_client.ListWorkspaceInstances(
            list_request
        )
        if len(list_response.workspace_instances) == 0:
            raise RuntimeError(f"Workspace instance for workspace '{workspace_definition_name}' not found")
        if (
            list_response.workspace_instances[0].spec.status.phase
            != WorkspaceInstanceStatus.WorkspaceInstancePhase.WORKSPACE_INSTANCE_PHASE_RUNNING
        ):
            return None
        return list_response.workspace_instances[0].spec.uri

    async def start_workspace_instance(
        self,
        workspace_definition_name: str,
        project: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> GetWorkspaceInstanceResponse:
        workspace_definition_id = await self.get_latest_workspace_definition_id(
            workspace_definition_name=workspace_definition_name,
            project=project or self.default_project,
            domain=domain or self.default_domain,
        )
        _logger.info(f"WorkspaceDefinitionIdentifier: {workspace_definition_id}")
        start_request = StartWorkspaceInstanceRequest(
            org=workspace_definition_id.org,
            project=workspace_definition_id.project,
            domain=workspace_definition_id.domain,
            workspace_definition_id=workspace_definition_id,
        )
        _logger.info(f"StartWorkspaceInstanceRequest: {start_request}")
        try:
            start_response: StartWorkspaceInstanceResponse = await self.instance_async_client.StartWorkspaceInstance(
                start_request
            )
        except Exception:
            raise

        get_request = GetWorkspaceInstanceRequest(id=start_response.workspace_instance.id)
        uri = None
        _logger.info(f"GetWorkspaceInstanceRequest: {get_request}")
        while not uri:
            get_response: GetWorkspaceInstanceResponse = await self.instance_async_client.GetWorkspaceInstance(
                get_request
            )
            uri = get_response.workspace_instance.spec.uri

            if not uri:
                await asyncio.sleep(3)
        return get_response

    async def stop_workspace_instance(
        self,
        workspace_definition_name: str,
        project: Optional[str] = None,
        domain: Optional[str] = None,
    ):
        workspace_definition_id = await self.get_latest_workspace_definition_id(
            workspace_definition_name=workspace_definition_name,
            project=project or self.default_project,
            domain=domain or self.default_domain,
        )
        list_request = ListWorkspaceInstancesRequest(
            request=_list_pb2.ListRequest(
                limit=1,
                sort_by=_list_pb2.Sort(
                    key="created_at",
                    direction=_list_pb2.Sort.Direction.DESCENDING,
                ),
            ),
            org=self.org,
            project=_identifier_pb2.ProjectIdentifier(
                organization=self.org,
                domain=domain or self.default_domain,
                name=project or self.default_project,
            ),
            workspace_definition_id=workspace_definition_id,
        )
        list_response: ListWorkspaceInstancesResponse = await self.instance_async_client.ListWorkspaceInstances(
            list_request
        )
        if len(list_response.workspace_instances) == 0:
            raise RuntimeError(f"Workspace instance for workspace '{workspace_definition_name}' not found")

        workspace_instance_id = list_response.workspace_instances[0].id

        stop_request = StopWorkspaceInstanceRequest(id=workspace_instance_id)
        _logger.info(f"StopWorkspaceInstanceRequest: {stop_request}")
        try:
            await self.instance_async_client.StopWorkspaceInstance(stop_request)
        except Exception:
            raise
        return workspace_instance_id

    @property
    def instance_async_client(self) -> WorkspaceInstanceServiceStub:
        try:
            return self._instance_async_client
        except AttributeError:
            self._instance_async_client = WorkspaceInstanceServiceStub(self.async_channel)
            return self._instance_async_client

    @property
    def definition_async_client(self) -> WorkspaceRegistryServiceStub:
        try:
            return self._definition_async_client
        except AttributeError:
            self._definition_async_client = WorkspaceRegistryServiceStub(self.async_channel)
            return self._definition_async_client

    @property
    def sync_channel(self) -> grpc.Channel:
        try:
            return self._sync_channel
        except AttributeError:
            self._sync_channel, self._org = _get_channel_with_org(self.config.platform)
            return self._sync_channel

    @property
    def async_channel(self) -> grpc.aio.Channel:
        from union.filesystems._endpoint import _create_secure_channel_from_config

        try:
            return self._async_channel
        except AttributeError:
            self._async_channel = _create_secure_channel_from_config(self.config.platform, self.sync_channel)
            return self._async_channel

    @property
    def org(self) -> Optional[str]:
        try:
            return self._org
        except AttributeError:
            self._sync_channel, self._org = _get_channel_with_org(self.config.platform)
            if self._org is None or self._org == "":
                self._org = self.config.platform.endpoint.split(".")[0]
            return self._org


def _generate_random_str(N: int):
    items = string.ascii_letters + string.digits
    return "".join(random.choice(items) for _ in range(N))


def _generate_workspace_name(name: str):
    """Generate workspace name prefixed by name."""
    return f"{name}-{_generate_random_str(VERSION_STRING_LENGTH)}"


def _get_workspace_name(version):
    return version[: -(VERSION_STRING_LENGTH + 1)]


def _get_workspace_executions(remote: UnionRemote, project: str, domain: str):
    executions, _ = remote.client.list_executions_paginated(
        project=project,
        domain=domain,
        limit=1000,
        filters=[
            Equal("task.name", "union.workspace._vscode.workspace"),
            ValueIn("phase", ["RUNNING", "QUEUED"]),
        ],
    )
    return [(e, _get_workspace_name(e.spec.launch_plan.version)) for e in executions]


def _get_vscode_link(remote: UnionRemote, execution: Execution) -> str:
    if execution.closure.phase != WorkflowExecutionPhase.RUNNING:
        return "Unavailable"

    workflow_execution = remote.fetch_execution(
        project=execution.id.project,
        domain=execution.id.domain,
        name=execution.id.name,
    )
    workflow_execution = remote.sync_execution(workflow_execution, sync_nodes=True)

    if not workflow_execution.node_executions:
        return "Unavailable"

    all_keys = [e for e in workflow_execution.node_executions if e != "start-node"]
    if not all_keys:
        return "Unavailable"

    vscode_key = all_keys[0]
    vscode_node = workflow_execution.node_executions[vscode_key]

    if vscode_node.closure.phase != TaskExecutionPhase.RUNNING or not vscode_node.task_executions:
        return "Unavailable"

    task_execution = vscode_node.task_executions[-1]
    if task_execution.closure.phase != TaskExecutionPhase.RUNNING:
        return "Unavailable"

    for log in task_execution.closure.logs:
        if VSCODE_DEBUGGER_LOG_NAME in log.name:
            return remote.generate_console_http_domain() + log.uri
