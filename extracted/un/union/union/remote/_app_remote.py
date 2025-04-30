"""Module to manage applications on Union."""

import asyncio
import logging
import os
import tarfile
import weakref
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable, List, Optional

import grpc
from click import ClickException
from flyteidl.core.tasks_pb2 import Resources
from flytekit.configuration import Config
from flytekit.core.artifact import Artifact, ArtifactQuery
from flytekit.exceptions.system import FlyteSystemException
from flytekit.exceptions.user import FlyteEntityNotExistException
from flytekit.models.core.types import BlobType
from rich.console import Console

from union._async import merge, run_sync
from union._config import _get_organization, _is_serverless_endpoint
from union.app import App
from union.app._models import AppSerializationSettings, Input, MaterializedInput, URLQuery
from union.cli._common import _get_channel_with_org
from union.internal.app.app_definition_pb2 import App as AppIDL
from union.internal.app.app_definition_pb2 import Condition, Identifier, Spec, Status
from union.internal.app.app_logs_payload_pb2 import TailLogsRequest, TailLogsResponse
from union.internal.app.app_logs_service_pb2_grpc import AppLogsServiceStub
from union.internal.app.app_payload_pb2 import (
    CreateRequest,
    CreateResponse,
    GetRequest,
    GetResponse,
    ListResponse,
    UpdateRequest,
    UpdateResponse,
    WatchRequest,
    WatchResponse,
)
from union.internal.app.app_payload_pb2 import (
    ListRequest as ListAppsRequest,
)
from union.internal.app.app_service_pb2_grpc import AppServiceStub
from union.internal.common.identifier_pb2 import ProjectIdentifier
from union.internal.common.list_pb2 import ListRequest
from union.remote._remote import UnionRemote

logger = logging.getLogger(__name__)

FILES_TAR_FILE_NAME = "include-files.tar.gz"


class AppRemote:
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

    def list(self) -> List[AppIDL]:
        def create_list_request(token: str):
            return ListAppsRequest(
                request=ListRequest(token=token),
                org=self.org,
                project=ProjectIdentifier(name=self.default_project, domain=self.default_domain, organization=self.org),
            )

        results = []
        response: ListResponse
        token, has_next = "", True

        while has_next:
            list_request = create_list_request(token=token)

            response = self.sync_client.List(list_request)
            token = response.token
            has_next = token != ""

            results.extend(response.apps)

        return results

    def deploy(self, app: App, project: Optional[str] = None, domain: Optional[str] = None) -> AppIDL:
        # Deploy apps that are required by this app.
        console = Console()
        for dep_app in app.dependencies:
            console.print(f"⏳  Deploying dependent app: {dep_app.name}")
            self.deploy(dep_app, project=project, domain=domain)
            console.print()

        try:
            orig_app_idl = self.get(name=app.name, project=project, domain=domain)
        except FlyteEntityNotExistException:
            return self.create(app, project=project, domain=domain)

        try:
            return self.update(app, project=project, domain=domain)
        except FlyteSystemException as e:
            if "Either the change has already" in str(e.__cause__):
                console.print(f"✅ {app.name} app was already deployed with the current spec")

                _url = orig_app_idl.status.ingress.public_url
                url = f"[link={_url}]{_url}[/link]"

                console.print()
                console.print(f"🚀 Deployed Endpoint: {url}")

                return orig_app_idl
            raise

    def get(self, name: str, project: Optional[str] = None, domain: Optional[str] = None) -> AppIDL:
        app_id = Identifier(
            org=self.org,
            project=project or self.default_project,
            domain=domain or self.default_domain,
            name=name,
        )
        get_app_request = GetRequest(app_id=app_id)

        get_response: GetResponse = self.sync_client.Get(get_app_request)
        app = get_response.app

        return app

    def start(self, name: str, project: Optional[str] = None, domain: Optional[str] = None) -> AppIDL:
        app_idl = self.get(name, project=project, domain=domain)
        app_idl.spec.desired_state = Spec.DesiredState.DESIRED_STATE_ACTIVE

        def run_request():
            update_request = UpdateRequest(app=app_idl)
            update_response: UpdateResponse = self.sync_client.Update(update_request)
            return update_response.app

        initial_condition = None
        if app_idl.status.conditions:
            initial_condition = app_idl.status.conditions[-1]

        app_idl = self._watch_update(app_idl, run_request, initial_condition)
        return app_idl

    def update(self, app: App, project: Optional[str] = None, domain: Optional[str] = None) -> AppIDL:
        additional_distribution = self.upload_files(app)
        materialized_input_values = self.materialize_values(app, project=project, domain=domain)
        settings = AppSerializationSettings(
            org=self.org,
            project=project or self.default_project,
            domain=domain or self.default_domain,
            additional_distribution=additional_distribution,
            desired_state=Spec.DesiredState.DESIRED_STATE_ACTIVE,
            materialized_inputs=materialized_input_values,
            is_serverless=_is_serverless_endpoint(self.config.platform.endpoint),
        )
        new_app_idl = app._to_union_idl(settings=settings)

        get_app_request = GetRequest(app_id=new_app_idl.metadata.id)
        get_response: GetResponse = self.sync_client.Get(get_app_request)

        old_app_idl = get_response.app

        initial_condition = None
        if old_app_idl.status.conditions:
            initial_condition = old_app_idl.status.conditions[-1]

        updated_app_idl = App._update_app_idl(old_app_idl, new_app_idl)

        def run_request():
            update_request = UpdateRequest(app=updated_app_idl)
            update_response: UpdateResponse = self.sync_client.Update(update_request)
            return update_response.app

        app_idl = self._watch_update(updated_app_idl, run_request, initial_condition)
        return app_idl

    def create(self, app: App, project: Optional[str] = None, domain: Optional[str] = None) -> AppIDL:
        additional_distribution = self.upload_files(app)
        materialized_input_values = self.materialize_values(app, project=project, domain=domain)
        settings = AppSerializationSettings(
            org=self.org,
            project=project or self.default_project,
            domain=domain or self.default_domain,
            additional_distribution=additional_distribution,
            desired_state=Spec.DesiredState.DESIRED_STATE_ACTIVE,
            materialized_inputs=materialized_input_values,
            is_serverless=_is_serverless_endpoint(self.config.platform.endpoint),
        )
        app_idl = app._to_union_idl(settings=settings)

        def run_request():
            create_request = CreateRequest(app=app_idl)
            create_response: CreateResponse = self.sync_client.Create(create_request)
            return create_response.app

        self._watch_update(app_idl, run_request, None)
        return app_idl

    def _watch_update(
        self, app_idl: AppIDL, run_request: Callable[[], AppIDL], initial_condition: Optional[Condition] = None
    ) -> AppIDL:
        console = Console()

        # TODO: Revise when log streaming comes back
        # initial_datetime = None
        # if initial_condition:
        #     initial_datetime = initial_condition.last_transition_time.ToDatetime().replace(tzinfo=timezone.utc)

        name = app_idl.metadata.id.name
        _console_url = self.generate_console_url(app_idl)
        console_url = f"[link={_console_url}]{_console_url}[/link]"
        console.print(f"✨ Deploying Application: [link={_console_url}]{name}[/link]")
        console.print(f"🔎 Console URL: {console_url}")

        updated_idl = run_request()
        watch_request = WatchRequest(app_id=updated_idl.metadata.id)
        get_app_request = GetRequest(app_id=updated_idl.metadata.id)

        async def watch_for_status():
            response: WatchResponse
            async for response in self.async_client.Watch(watch_request):
                status = response.update_event.updated_app.status
                yield status

        async def poll_for_status():
            loop = asyncio.get_running_loop()
            while True:
                get_response: GetResponse = await loop.run_in_executor(None, self.sync_client.Get, get_app_request)
                yield get_response.app.status
                await asyncio.sleep(2)

        async def watch_status(console):
            latest_message = ""
            status: Status

            loop = asyncio.get_running_loop()
            async for status in merge(loop, watch_for_status(), poll_for_status()):
                if not status.conditions:
                    continue
                latest_condition = status.conditions[-1]
                if initial_condition == latest_condition:
                    # The status did not update from the initial condition
                    continue
                deployment_status = latest_condition.deployment_status
                status_str = Status.DeploymentStatus.Name(deployment_status).split("_")[-1].title()
                if latest_condition.message != latest_message:
                    escaped_message = latest_condition.message.replace("[", "\\[")
                    console.print(f"[bold]\\[Status][/] [italic]{status_str}:[/] {escaped_message}")
                    latest_message = latest_condition.message

                if deployment_status in (
                    Status.DeploymentStatus.DEPLOYMENT_STATUS_UNSPECIFIED,
                    Status.DeploymentStatus.DEPLOYMENT_STATUS_STOPPED,
                    Status.DeploymentStatus.DEPLOYMENT_STATUS_FAILED,
                ):
                    raise ClickException("Application failed to deploy")
                elif deployment_status == Status.DEPLOYMENT_STATUS_UNASSIGNED:
                    raise ClickException("Application was unassigned")
                elif (
                    deployment_status == Status.DeploymentStatus.DEPLOYMENT_STATUS_ACTIVE
                    or deployment_status == Status.DeploymentStatus.DEPLOYMENT_STATUS_STARTED
                ):
                    yield True

        async def watch(console):
            # TODO: Fix log streaming
            # status_iter = merge(watch_status(console), self._watch_logs(updated_idl, initial_datetime, console))
            status_iter = watch_status(console)
            try:
                async for to_stop in status_iter:
                    if to_stop:
                        return
            finally:
                await status_iter.aclose()

        run_sync(watch, console)

        _url = updated_idl.status.ingress.public_url
        url = f"[link={_url}]{_url}[/link]"

        console.print()
        console.print(f"🚀 Deployed Endpoint: {url}")
        return updated_idl

    @staticmethod
    def _format_line(line: str, initial_datetime: Optional[datetime]) -> str:
        whitespace_idx = line.find(" ")
        if whitespace_idx == -1:
            return line
        datetime_str = line[:whitespace_idx]

        try:
            dt = datetime.fromisoformat(datetime_str)
        except ValueError:
            return line

        if initial_datetime is not None and dt > initial_datetime:
            # Do not show logs that are older than the previous initial condition
            return ""

        formatted_dt = dt.strftime("%H:%M:%S")
        return f"{formatted_dt}{line[whitespace_idx:]}"

    async def _watch_logs(self, app_idl: AppIDL, initial_datetime: Optional[datetime], console: Console):
        async_log_client = AppLogsServiceStub(self.async_channel)
        tail_request = TailLogsRequest(app_id=app_idl.metadata.id)
        response: TailLogsResponse
        async for response in async_log_client.TailLogs(tail_request):
            for log in response.batches.logs:
                for line in log.lines:
                    formatted_line = self._format_line(line, initial_datetime).strip()
                    if not formatted_line:
                        continue
                    console.print(f"[bold]\\[App][/] {formatted_line}")
                    # TODO: Detect errors and stop

            yield False

    def stop(self, name: str, project: Optional[str] = None, domain: Optional[str] = None) -> AppIDL:
        app_idl = self.get(name, project=project, domain=domain)
        app_idl.spec.desired_state = Spec.DesiredState.DESIRED_STATE_STOPPED

        console = Console()

        console_url = self.generate_console_url(app_idl)
        console.print(f"🛑 Stopping Application: [link={console_url}]{name}[/link]")

        update_request = UpdateRequest(app=app_idl)
        update_response: UpdateResponse = self.sync_client.Update(update_request)
        return update_response.app

    def upload_files(self, app: App) -> Optional[str]:
        """Upload files required by app."""
        if not app.include:
            return None

        with TemporaryDirectory() as temp_dir:
            tar_path = os.path.join(temp_dir, FILES_TAR_FILE_NAME)
            with tarfile.open(tar_path, "w:gz") as tar:
                for resolve_include in app.include_resolved:
                    tar.add(resolve_include.src, arcname=resolve_include.dest)

            _, upload_native_url = self.union_remote.upload_file(Path(tar_path))

            return upload_native_url

    def _process_artifact(self, artifact: Artifact) -> MaterializedInput:
        scalar = artifact.literal.scalar
        input_type = None
        if scalar.blob is not None:
            # Handle FlyteFiles and FlyteDirectories
            if scalar.blob.metadata.type.dimensionality == BlobType.BlobDimensionality.SINGLE:
                input_type = Input.Type.File
            elif scalar.blob.metadata.type.dimensionality == BlobType.BlobDimensionality.MULTIPART:
                input_type = Input.Type.Directory
            value = artifact.literal.scalar.blob.uri
        elif scalar.primitive is not None and scalar.primitive.string_value is not None:
            value = scalar.primitive.string_value
            input_type = Input.Type.String
        else:
            msg = (
                f"Artifact '{artifact.name}' is not supported as an App input, Only strings, files, "
                "and directory are supported."
            )
            raise ValueError(msg)

        return MaterializedInput(value=value, type=input_type)

    def materialize_values(self, app: App, project: Optional[str] = None, domain: Optional[str] = None) -> dict:
        output = {}
        for user_input in app.inputs:
            if isinstance(user_input.value, ArtifactQuery):
                query = deepcopy(user_input.value)
                query.project = project or self.default_project
                query.domain = domain or self.default_domain
                result = self.union_remote.get_artifact(query=query.to_flyte_idl())
                output[user_input.name] = self._process_artifact(result)

            elif user_input.type == Input.Type._ArtifactUri:
                if not isinstance(user_input.value, str):
                    raise ValueError("Artifact URI must be a string")

                result = self.union_remote.get_artifact(user_input.value)
                output[user_input.name] = self._process_artifact(result)

            elif isinstance(user_input.value, URLQuery):
                query = user_input.value
                # TODO: Assuming application has the same project and domain
                # TODO: Raise more informative error the assumption does not hold
                app_idl = self.get(name=query.name, project=project, domain=domain)
                if user_input.value.public:
                    output[user_input.name] = MaterializedInput(
                        value=app_idl.status.ingress.public_url,
                        type=Input.Type.String,
                    )
                else:
                    app_id = app_idl.metadata.id
                    output[user_input.name] = MaterializedInput(
                        value=app_id.name,
                        type=Input.Type._UrlQuery,
                    )

        return output

    def generate_console_url(self, app_idl: AppIDL) -> str:
        """Generate console url for app_idl."""
        http_domain = self.union_remote.generate_console_http_domain()
        org = _get_organization(self.config.platform, self.sync_channel)

        app_id = app_idl.metadata.id

        if org is None or org == "":
            console = "console"
        else:
            console = f"org/{org}"

        return f"{http_domain}/{console}/projects/{app_id.project}/domains/{app_id.domain}/apps/{app_id.name}"

    @property
    def sync_channel(self) -> grpc.Channel:
        try:
            return self._sync_channel
        except AttributeError:
            self._sync_channel, self._org = _get_channel_with_org(self.config.platform)
            return self._sync_channel

    @property
    def org(self) -> Optional[str]:
        try:
            return self._org
        except AttributeError:
            self._sync_channel, self._org = _get_channel_with_org(self.config.platform)
            if self._org is None or self._org == "":
                self._org = self.config.platform.endpoint.split(".")[0]
            return self._org

    @property
    def sync_client(self) -> AppServiceStub:
        try:
            return self._sync_client
        except AttributeError:
            self._sync_client = AppServiceStub(self.sync_channel)
            return self._sync_client

    @property
    def async_client(self) -> AppServiceStub:
        try:
            return self._async_client
        except AttributeError:
            self._async_client = AppServiceStub(self.async_channel)
            return self._async_client

    @property
    def async_channel(self) -> grpc.aio.Channel:
        from union.filesystems._endpoint import _create_secure_channel_from_config

        try:
            return self._async_channel
        except AttributeError:
            self._async_channel = _create_secure_channel_from_config(self.config.platform, self.sync_channel)
            return self._async_channel

    @staticmethod
    def deployment_status(app_idl: AppIDL) -> str:
        try:
            current_status = app_idl.status.conditions[-1].deployment_status
            return Status.DeploymentStatus.Name(current_status).split("_")[-1].title()
        except Exception:
            return "Unknown"

    @staticmethod
    def desired_state(app_idl: AppIDL) -> str:
        return Spec.DesiredState.Name(app_idl.spec.desired_state).split("_")[-1].title()

    @staticmethod
    def get_message(app_idl: AppIDL) -> str:
        if len(app_idl.status.conditions) == 0:
            return "Unknown"
        return app_idl.status.conditions[-1].message

    @staticmethod
    def get_limits(app_idl: AppIDL) -> dict:
        output = {}
        for limit in app_idl.spec.container.resources.limits:
            if limit.name == Resources.ResourceName.CPU:
                output["cpu"] = limit.value
            if limit.name == Resources.ResourceName.MEMORY:
                output["memory"] = limit.value
        return output
