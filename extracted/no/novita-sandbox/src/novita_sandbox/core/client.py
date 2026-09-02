from __future__ import annotations

from typing import Any, Dict, Optional

from httpx._types import ProxyTypes

from novita_sandbox.core.connection_config import ApiParams, ConnectionConfig
from novita_sandbox.core.exceptions import (
    AuthenticationException,
    BuildException,
    FileNotFoundException,
    FileUploadException,
    GitAuthException,
    GitUpstreamException,
    InvalidArgumentException,
    NotEnoughSpaceException,
    NotFoundException,
    RateLimitException,
    SandboxException,
    SandboxNotFoundException,
    TemplateException,
    TimeoutException,
    VolumeException,
)
from novita_sandbox.core.sandbox.commands.command_handle import (
    CommandExitException,
    CommandResult,
    PtyOutput,
    PtySize,
    Stderr,
    Stdout,
)
from novita_sandbox.core.sandbox.commands.main import ProcessInfo
from novita_sandbox.core.sandbox.filesystem.filesystem import (
    EntryInfo,
    FileType,
    WriteInfo,
)
from novita_sandbox.core.sandbox.filesystem.watch_handle import (
    FilesystemEvent,
    FilesystemEventType,
)
from novita_sandbox.core.sandbox.network import ALL_TRAFFIC
from novita_sandbox.core.sandbox.sandbox_api import (
    GitHubMcpServer,
    GitHubMcpServerConfig,
    McpServer,
    SandboxEventItem,
    SandboxEventsResult,
    SandboxInfo,
    SandboxInfoLifecycle,
    SandboxLifecycle,
    SandboxMetrics,
    SandboxNetworkOpts,
    SandboxQuery,
    SandboxQuota,
    SandboxQuotaLimit,
    SandboxQuotaUsage,
    SandboxState,
    SnapshotInfo,
)
from novita_sandbox.core.sandbox_sync.sandbox_api import SandboxApi
from novita_sandbox.core.sandbox._git import GitBranches, GitFileStatus, GitStatus
from novita_sandbox.core.sandbox_async.commands.command_handle import AsyncCommandHandle
from novita_sandbox.core.sandbox_async.filesystem.watch_handle import AsyncWatchHandle
from novita_sandbox.core.sandbox_async.main import AsyncSandbox
from novita_sandbox.core.sandbox_async.paginator import (
    AsyncSandboxPaginator,
    AsyncSnapshotPaginator,
)
from novita_sandbox.core.sandbox_async.utils import OutputHandler
from novita_sandbox.core.sandbox_sync.commands.command_handle import CommandHandle
from novita_sandbox.core.sandbox_sync.filesystem.watch_handle import WatchHandle
from novita_sandbox.core.sandbox_sync.git import Git
from novita_sandbox.core.sandbox_sync.main import CloneResult, Sandbox
from novita_sandbox.core.sandbox_sync.paginator import (
    SandboxPaginator,
    SnapshotPaginator,
)
from novita_sandbox.core.secret import AsyncSecret, Secret, SecretBinding
from novita_sandbox.core.template.logger import (
    LogEntry,
    LogEntryEnd,
    LogEntryLevel,
    LogEntryStart,
    default_build_logger,
)
from novita_sandbox.core.template.main import TemplateBase, TemplateClass
from novita_sandbox.core.template.readycmd import (
    ReadyCmd,
    wait_for_file,
    wait_for_port,
    wait_for_process,
    wait_for_timeout,
    wait_for_url,
)
from novita_sandbox.core.template.types import (
    BuildInfo,
    BuildStatusReason,
    CopyItem,
    TemplateBuildStatus,
    TemplateBuildStatusResponse,
    TemplateInfo,
    TemplateList,
    TemplateTag,
    TemplateTagInfo,
)
from novita_sandbox.core.template_async.main import AsyncTemplate
from novita_sandbox.core.template_sync.main import Template
from novita_sandbox.core.volume.types import VolumeAndToken, VolumeInfo
from novita_sandbox.core.volume.volume_async import AsyncVolume
from novita_sandbox.core.volume.volume_sync import Volume


class _Namespace:
    def __init__(self, opts: Dict[str, Any]) -> None:
        self._opts = opts

    def _merge(self, opts: Dict[str, Any]) -> Dict[str, Any]:
        merged = dict(self._opts)
        headers = {
            **(self._opts.get("headers") or {}),
            **(opts.get("headers") or {}),
        }
        merged.update(opts)
        if headers:
            merged["headers"] = headers
        return {key: value for key, value in merged.items() if value is not None}


class _SandboxNamespace(_Namespace):
    Sandbox = Sandbox
    AsyncSandbox = AsyncSandbox
    SandboxPaginator = SandboxPaginator
    AsyncSandboxPaginator = AsyncSandboxPaginator
    SnapshotPaginator = SnapshotPaginator
    AsyncSnapshotPaginator = AsyncSnapshotPaginator
    CloneResult = CloneResult

    SandboxInfo = SandboxInfo
    SandboxInfoLifecycle = SandboxInfoLifecycle
    SandboxMetrics = SandboxMetrics
    SandboxQuery = SandboxQuery
    SandboxState = SandboxState
    SandboxLifecycle = SandboxLifecycle
    SandboxNetworkOpts = SandboxNetworkOpts
    SandboxQuota = SandboxQuota
    SandboxQuotaLimit = SandboxQuotaLimit
    SandboxQuotaUsage = SandboxQuotaUsage
    SandboxEventItem = SandboxEventItem
    SandboxEventsResult = SandboxEventsResult
    SnapshotInfo = SnapshotInfo
    McpServer = McpServer
    GitHubMcpServer = GitHubMcpServer
    GitHubMcpServerConfig = GitHubMcpServerConfig
    ALL_TRAFFIC = ALL_TRAFFIC

    CommandResult = CommandResult
    CommandExitException = CommandExitException
    CommandHandle = CommandHandle
    AsyncCommandHandle = AsyncCommandHandle
    ProcessInfo = ProcessInfo
    Stderr = Stderr
    Stdout = Stdout
    PtyOutput = PtyOutput
    PtySize = PtySize

    EntryInfo = EntryInfo
    WriteInfo = WriteInfo
    FileType = FileType
    FilesystemEvent = FilesystemEvent
    FilesystemEventType = FilesystemEventType
    WatchHandle = WatchHandle
    AsyncWatchHandle = AsyncWatchHandle

    Git = Git
    GitStatus = GitStatus
    GitBranches = GitBranches
    GitFileStatus = GitFileStatus
    OutputHandler = OutputHandler

    SandboxException = SandboxException
    TimeoutException = TimeoutException
    NotFoundException = NotFoundException
    FileNotFoundException = FileNotFoundException
    SandboxNotFoundException = SandboxNotFoundException
    AuthenticationException = AuthenticationException
    GitAuthException = GitAuthException
    GitUpstreamException = GitUpstreamException
    InvalidArgumentException = InvalidArgumentException
    NotEnoughSpaceException = NotEnoughSpaceException
    RateLimitException = RateLimitException

    def create(self, *args: Any, **opts: Any) -> Sandbox:
        return Sandbox.create(*args, **self._merge(opts))

    def beta_create(self, *args: Any, **opts: Any) -> Sandbox:
        return Sandbox.beta_create(*args, **self._merge(opts))

    def connect(self, sandbox_id: str, *args: Any, **opts: Any) -> Sandbox:
        return Sandbox.connect(sandbox_id, *args, **self._merge(opts))

    def get(self, sandbox_id: str, *args: Any, **opts: Any) -> Sandbox:
        return self.connect(sandbox_id, *args, **opts)

    def list(self, **opts: Any):
        return Sandbox.list(**self._merge(opts))

    def kill(self, sandbox_id: str, *args: Any, **opts: Any) -> bool:
        return Sandbox.kill(sandbox_id, *args, **self._merge(opts))

    def set_timeout(self, sandbox_id: str, timeout: int, **opts: Any) -> None:
        return Sandbox.set_timeout(sandbox_id, timeout, **self._merge(opts))

    def get_info(self, sandbox_id: str, **opts: Any):
        return Sandbox.get_info(sandbox_id, **self._merge(opts))

    def get_metrics(self, sandbox_id: str, *args: Any, **opts: Any):
        return Sandbox.get_metrics(sandbox_id, *args, **self._merge(opts))

    def pause(self, sandbox_id: str, *args: Any, **opts: Any) -> None:
        return Sandbox.pause(sandbox_id, *args, **self._merge(opts))

    def beta_pause(self, sandbox_id: str, *args: Any, **opts: Any) -> None:
        return Sandbox.beta_pause(sandbox_id, *args, **self._merge(opts))

    def clone(self, sandbox_id: str, *args: Any, **opts: Any) -> CloneResult:
        return Sandbox.clone(sandbox_id, *args, **self._merge(opts))

    def reset(self, sandbox_id: str, *args: Any, **opts: Any) -> bool:
        return Sandbox.reset(sandbox_id, *args, **self._merge(opts))

    def commit(self, sandbox_id: str, *args: Any, **opts: Any):
        return Sandbox.commit(sandbox_id, *args, **self._merge(opts))

    def set_network(self, sandbox_id: str, *args: Any, **opts: Any) -> None:
        return Sandbox.set_network(sandbox_id, *args, **self._merge(opts))

    def create_snapshot(self, sandbox_id: str, **opts: Any):
        return Sandbox.create_snapshot(sandbox_id, **self._merge(opts))

    def list_snapshots(self, *args: Any, **opts: Any):
        return Sandbox.list_snapshots(*args, **self._merge(opts))

    def delete_snapshot(self, snapshot_id: str, **opts: Any) -> bool:
        return Sandbox.delete_snapshot(snapshot_id, **self._merge(opts))

    def get_quota(self, **opts: Any):
        return Sandbox.get_quota(**self._merge(opts))

    def get_events(self, *args: Any, **opts: Any):
        return Sandbox.get_events(*args, **self._merge(opts))

    def resize(
        self,
        sandbox_id: str,
        *,
        memory_mib: Optional[int] = None,
        **opts: Any,
    ) -> None:
        """
        Add hotplug memory to a running sandbox.

        `memory_mib=512` adds 512 MiB of memory; it does not resize the
        sandbox to a total of 512 MiB.
        """
        if memory_mib is None:
            raise ValueError("resize requires memory_mib")

        return SandboxApi._cls_hotplug_memory(
            sandbox_id=sandbox_id,
            requested_size_mib=memory_mib,
            **self._merge(opts),
        )


class _RuntimeSandboxNamespace(_Namespace):
    SandboxQuery = SandboxQuery
    SandboxState = SandboxState
    SandboxInfo = SandboxInfo
    SandboxMetrics = SandboxMetrics
    SandboxQuota = SandboxQuota
    SandboxEventsResult = SandboxEventsResult
    SnapshotInfo = SnapshotInfo
    FilesystemEvent = FilesystemEvent
    FilesystemEventType = FilesystemEventType

    def _sandbox_cls(self):
        raise NotImplementedError

    def create(self, *args: Any, **opts: Any):
        return self._sandbox_cls().create(*args, **self._merge(opts))

    def beta_create(self, *args: Any, **opts: Any):
        return self._sandbox_cls().beta_create(*args, **self._merge(opts))

    def connect(self, sandbox_id: str, *args: Any, **opts: Any):
        return self._sandbox_cls().connect(sandbox_id, *args, **self._merge(opts))

    def get(self, sandbox_id: str, *args: Any, **opts: Any):
        return self.connect(sandbox_id, *args, **opts)

    def list(self, **opts: Any):
        return self._sandbox_cls().list(**self._merge(opts))

    def kill(self, sandbox_id: str, *args: Any, **opts: Any) -> bool:
        return self._sandbox_cls().kill(sandbox_id, *args, **self._merge(opts))

    def set_timeout(self, sandbox_id: str, timeout: int, **opts: Any) -> None:
        return self._sandbox_cls().set_timeout(sandbox_id, timeout, **self._merge(opts))

    def get_info(self, sandbox_id: str, **opts: Any):
        return self._sandbox_cls().get_info(sandbox_id, **self._merge(opts))

    def get_metrics(self, sandbox_id: str, *args: Any, **opts: Any):
        return self._sandbox_cls().get_metrics(sandbox_id, *args, **self._merge(opts))

    def pause(self, sandbox_id: str, *args: Any, **opts: Any) -> None:
        return self._sandbox_cls().pause(sandbox_id, *args, **self._merge(opts))

    def beta_pause(self, sandbox_id: str, *args: Any, **opts: Any) -> None:
        return self._sandbox_cls().beta_pause(sandbox_id, *args, **self._merge(opts))

    def clone(self, sandbox_id: str, *args: Any, **opts: Any):
        return self._sandbox_cls().clone(sandbox_id, *args, **self._merge(opts))

    def reset(self, sandbox_id: str, *args: Any, **opts: Any) -> bool:
        return self._sandbox_cls().reset(sandbox_id, *args, **self._merge(opts))

    def commit(self, sandbox_id: str, *args: Any, **opts: Any):
        return self._sandbox_cls().commit(sandbox_id, *args, **self._merge(opts))

    def set_network(self, sandbox_id: str, *args: Any, **opts: Any) -> None:
        return self._sandbox_cls().set_network(sandbox_id, *args, **self._merge(opts))

    def create_snapshot(self, sandbox_id: str, **opts: Any):
        return self._sandbox_cls().create_snapshot(sandbox_id, **self._merge(opts))

    def list_snapshots(self, *args: Any, **opts: Any):
        return self._sandbox_cls().list_snapshots(*args, **self._merge(opts))

    def delete_snapshot(self, snapshot_id: str, **opts: Any) -> bool:
        return self._sandbox_cls().delete_snapshot(snapshot_id, **self._merge(opts))

    def get_quota(self, **opts: Any):
        return self._sandbox_cls().get_quota(**self._merge(opts))

    def get_events(self, *args: Any, **opts: Any):
        return self._sandbox_cls().get_events(*args, **self._merge(opts))

    def resize(
        self,
        sandbox_id: str,
        *,
        memory_mib: Optional[int] = None,
        **opts: Any,
    ) -> None:
        """
        Add hotplug memory to a running sandbox.

        `memory_mib=512` adds 512 MiB of memory; it does not resize the
        sandbox to a total of 512 MiB.
        """
        if memory_mib is None:
            raise ValueError("resize requires memory_mib")

        return SandboxApi._cls_hotplug_memory(
            sandbox_id=sandbox_id,
            requested_size_mib=memory_mib,
            **self._merge(opts),
        )


class _CodeInterpreterNamespace(_RuntimeSandboxNamespace):
    @property
    def Sandbox(self):
        from novita_sandbox.code_interpreter import Sandbox as CodeInterpreterSandbox

        return CodeInterpreterSandbox

    @property
    def AsyncSandbox(self):
        from novita_sandbox.code_interpreter import AsyncSandbox

        return AsyncSandbox

    @property
    def Context(self):
        from novita_sandbox.code_interpreter import Context

        return Context

    @property
    def Execution(self):
        from novita_sandbox.code_interpreter import Execution

        return Execution

    @property
    def ExecutionError(self):
        from novita_sandbox.code_interpreter import ExecutionError

        return ExecutionError

    @property
    def Result(self):
        from novita_sandbox.code_interpreter import Result

        return Result

    @property
    def MIMEType(self):
        from novita_sandbox.code_interpreter import MIMEType

        return MIMEType

    @property
    def Logs(self):
        from novita_sandbox.code_interpreter import Logs

        return Logs

    @property
    def OutputMessage(self):
        from novita_sandbox.code_interpreter import OutputMessage

        return OutputMessage

    def _sandbox_cls(self):
        return self.Sandbox


class _DesktopNamespace(_RuntimeSandboxNamespace):
    @property
    def Sandbox(self):
        from novita_sandbox.desktop import Sandbox as DesktopSandbox

        return DesktopSandbox

    def _sandbox_cls(self):
        return self.Sandbox


class _TemplateNamespace(_Namespace):
    Template = Template
    AsyncTemplate = AsyncTemplate
    TemplateBase = TemplateBase
    TemplateClass = TemplateClass

    BuildInfo = BuildInfo
    BuildStatusReason = BuildStatusReason
    CopyItem = CopyItem
    TemplateBuildStatus = TemplateBuildStatus
    TemplateBuildStatusResponse = TemplateBuildStatusResponse
    TemplateInfo = TemplateInfo
    TemplateList = TemplateList
    TemplateTag = TemplateTag
    TemplateTagInfo = TemplateTagInfo

    ReadyCmd = ReadyCmd
    wait_for_file = staticmethod(wait_for_file)
    wait_for_url = staticmethod(wait_for_url)
    wait_for_port = staticmethod(wait_for_port)
    wait_for_process = staticmethod(wait_for_process)
    wait_for_timeout = staticmethod(wait_for_timeout)

    LogEntry = LogEntry
    LogEntryStart = LogEntryStart
    LogEntryEnd = LogEntryEnd
    LogEntryLevel = LogEntryLevel
    default_build_logger = staticmethod(default_build_logger)

    TemplateException = TemplateException
    BuildException = BuildException
    FileUploadException = FileUploadException
    NotFoundException = NotFoundException
    RateLimitException = RateLimitException

    def new(self, *args: Any, **kwargs: Any) -> Template:
        return Template(*args, **kwargs)

    def create(self, *args: Any, **kwargs: Any) -> Template:
        return self.new(*args, **kwargs)

    def skip_cache(self, *args: Any, **kwargs: Any):
        return self.new().skip_cache(*args, **kwargs)

    def from_debian_image(self, *args: Any, **kwargs: Any):
        return self.new().from_debian_image(*args, **kwargs)

    def from_ubuntu_image(self, *args: Any, **kwargs: Any):
        return self.new().from_ubuntu_image(*args, **kwargs)

    def from_python_image(self, *args: Any, **kwargs: Any):
        return self.new().from_python_image(*args, **kwargs)

    def from_node_image(self, *args: Any, **kwargs: Any):
        return self.new().from_node_image(*args, **kwargs)

    def from_bun_image(self, *args: Any, **kwargs: Any):
        return self.new().from_bun_image(*args, **kwargs)

    def from_base_image(self, *args: Any, **kwargs: Any):
        return self.new().from_base_image(*args, **kwargs)

    def from_image(self, *args: Any, **kwargs: Any):
        return self.new().from_image(*args, **kwargs)

    def from_template(self, *args: Any, **kwargs: Any):
        return self.new().from_template(*args, **kwargs)

    def from_dockerfile(self, *args: Any, **kwargs: Any):
        return self.new().from_dockerfile(*args, **kwargs)

    def from_aws_registry(self, *args: Any, **kwargs: Any):
        return self.new().from_aws_registry(*args, **kwargs)

    def from_gcp_registry(self, *args: Any, **kwargs: Any):
        return self.new().from_gcp_registry(*args, **kwargs)

    def from_oci_registry(self, *args: Any, **kwargs: Any):
        return self.new().from_oci_registry(*args, **kwargs)

    def from_huawei_cloud_registry(self, *args: Any, **kwargs: Any):
        return self.new().from_huawei_cloud_registry(*args, **kwargs)

    def to_json(self, *args: Any, **kwargs: Any) -> str:
        return TemplateBase.to_json(*args, **kwargs)

    def to_dockerfile(self, *args: Any, **kwargs: Any) -> str:
        return TemplateBase.to_dockerfile(*args, **kwargs)

    def list(self, *args: Any, **opts: Any):
        return Template.list(*args, **self._merge(opts))

    def delete(self, template_id: str, **opts: Any) -> bool:
        return Template.delete(template_id, **self._merge(opts))

    def build(self, *args: Any, **opts: Any):
        return Template.build(*args, **self._merge(opts))

    def build_in_background(self, *args: Any, **opts: Any):
        return Template.build_in_background(*args, **self._merge(opts))

    def get_build_status(self, *args: Any, **opts: Any):
        return Template.get_build_status(*args, **self._merge(opts))

    def exists(self, name: str, **opts: Any) -> bool:
        return Template.exists(name, **self._merge(opts))

    def alias_exists(self, alias: str, **opts: Any) -> bool:
        return Template.alias_exists(alias, **self._merge(opts))

    def assign_tags(self, *args: Any, **opts: Any):
        return Template.assign_tags(*args, **self._merge(opts))

    def remove_tags(self, *args: Any, **opts: Any):
        return Template.remove_tags(*args, **self._merge(opts))

    def get_tags(self, template_id: str, **opts: Any):
        return Template.get_tags(template_id, **self._merge(opts))


class _VolumeNamespace(_Namespace):
    Volume = Volume
    AsyncVolume = AsyncVolume
    VolumeInfo = VolumeInfo
    VolumeAndToken = VolumeAndToken

    VolumeException = VolumeException
    NotFoundException = NotFoundException
    RateLimitException = RateLimitException

    def create(self, name: str, *args: Any, **opts: Any) -> Volume:
        return Volume.create(name, *args, **self._merge(opts))

    def connect(self, volume_id: str, **opts: Any) -> Volume:
        return Volume.connect(volume_id, **self._merge(opts))

    def get_info(self, volume_id: str, **opts: Any):
        return Volume.get_info(volume_id, **self._merge(opts))

    def list(self, **opts: Any):
        return Volume.list(**self._merge(opts))

    def update_quota(self, volume_id: str, *args: Any, **opts: Any):
        return Volume.update_quota(volume_id, *args, **self._merge(opts))

    def destroy(self, volume_id: str, **opts: Any) -> bool:
        return Volume.destroy(volume_id, **self._merge(opts))


class _SecretNamespace(_Namespace):
    Secret = Secret
    AsyncSecret = AsyncSecret
    SecretBinding = SecretBinding

    InvalidArgumentException = InvalidArgumentException
    NotFoundException = NotFoundException
    RateLimitException = RateLimitException

    _supported_opts = {"api_key", "api_url", "domain", "request_timeout"}

    def _secret_connection_opts(self, opts: Dict[str, Any]) -> Dict[str, Any]:
        merged = self._merge(opts)
        return {
            key: value for key, value in merged.items() if key in self._supported_opts
        }

    def create(
        self,
        *,
        name: str,
        value: str,
        hosts: list[str],
        description: str | None = None,
        **opts: Any,
    ):
        return Secret.create(
            name=name,
            value=value,
            hosts=hosts,
            description=description,
            **self._secret_connection_opts(opts),
        )

    def list(self, **opts: Any):
        return Secret.list(**self._secret_connection_opts(opts))

    def get(self, name: str, **opts: Any):
        return Secret.get(name, **self._secret_connection_opts(opts))

    def update(
        self,
        *,
        name: str,
        value: str,
        hosts: list[str],
        description: str | None = None,
        **opts: Any,
    ):
        return Secret.update(
            name=name,
            value=value,
            hosts=hosts,
            description=description,
            **self._secret_connection_opts(opts),
        )

    def delete(self, name: str, **opts: Any) -> str:
        return Secret.delete(name, **self._secret_connection_opts(opts))


class Novita:
    """
    High-level client facade for Novita Sandbox resources and runtimes.
    """

    def __init__(
        self,
        domain: Optional[str] = None,
        debug: Optional[bool] = None,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        sandbox_url: Optional[str] = None,
        access_token: Optional[str] = None,
        request_timeout: Optional[float] = None,
        headers: Optional[Dict[str, str]] = None,
        extra_sandbox_headers: Optional[Dict[str, str]] = None,
        proxy: Optional[ProxyTypes] = None,
    ) -> None:
        config = ConnectionConfig(
            domain=domain,
            debug=debug,
            api_key=api_key,
            api_url=api_url,
            sandbox_url=sandbox_url,
            access_token=access_token,
            request_timeout=request_timeout,
            headers=headers,
            extra_sandbox_headers=extra_sandbox_headers,
            proxy=proxy,
        )
        self._opts: Dict[str, Any] = {
            "domain": config.domain,
            "debug": config.debug,
            "api_key": config.api_key,
            "api_url": config.api_url,
            "sandbox_url": sandbox_url,
            "access_token": access_token,
            "request_timeout": config.request_timeout,
            "headers": dict(config.headers),
            "extra_sandbox_headers": extra_sandbox_headers,
            "proxy": config.proxy,
        }

        self.sandbox = _SandboxNamespace(self._opts)
        self.code_interpreter = _CodeInterpreterNamespace(self._opts)
        self.desktop = _DesktopNamespace(self._opts)
        self.template = _TemplateNamespace(self._opts)
        self.volume = _VolumeNamespace(self._opts)
        self.secret = _SecretNamespace(self._opts)

    def create(self, *args: Any, **opts: ApiParams) -> Sandbox:
        return self.sandbox.create(*args, **opts)

    def connect(self, sandbox_id: str, **opts: ApiParams) -> Sandbox:
        return self.sandbox.connect(sandbox_id, **opts)

    def get(self, sandbox_id: str, **opts: ApiParams) -> Sandbox:
        return self.sandbox.get(sandbox_id, **opts)
