import datetime
import json
import logging
import shlex
import uuid
from typing import Dict, List, Optional, Union, overload

import httpx
from packaging.version import Version
from typing_extensions import Self, Unpack

from novita_sandbox.core.api.client.types import Unset
from novita_sandbox.core.api.client_sync import get_transport
from novita_sandbox.core.compat import raise_if_legacy
from novita_sandbox.core.connection_config import ApiParams, ConnectionConfig
from novita_sandbox.core.envd.api import ENVD_API_HEALTH_ROUTE, handle_envd_api_exception
from novita_sandbox.core.envd.versions import ENVD_DEBUG_FALLBACK
from novita_sandbox.core.exceptions import SandboxException, format_request_timeout_error
from novita_sandbox.core.sandbox.main import SandboxOpts
from novita_sandbox.core.sandbox.sandbox_api import (
    McpServer,
    SandboxLifecycle,
    SandboxMetrics,
    SandboxNetworkOpts,
    SnapshotInfo,
    SandboxQuota,
    SandboxEventsResult,
)
from novita_sandbox.core.sandbox.utils import class_method_variant
from novita_sandbox.core.sandbox_sync.commands.command import Commands
from novita_sandbox.core.sandbox_sync.commands.pty import Pty
from novita_sandbox.core.sandbox_sync.filesystem.filesystem import Filesystem
from novita_sandbox.core.sandbox_sync.git import Git
from novita_sandbox.core.sandbox_sync.sandbox_api import SandboxApi, SandboxInfo
from novita_sandbox.core.sandbox_sync.paginator import SnapshotPaginator
from novita_sandbox.core.api.client.models import SandboxVolumeMount as SandboxVolumeMountAPI
from novita_sandbox.core.volume.volume_sync import Volume

logger = logging.getLogger(__name__)

SandboxVolumeMount = Dict[str, Union[Volume, str]]


def _raise_if_legacy_mcp(mcp: Optional[McpServer], opts: dict) -> None:
    if mcp is not None:
        raise_if_legacy(opts, "Sandbox.create mcp")


def _resolve_secure(secure: Optional[bool], opts: ApiParams) -> bool:
    if secure is not None:
        return secure
    return not ConnectionConfig(**opts).is_legacy_domain


class CloneResult:
    """
    Result of a sandbox clone operation.

    Contains the list of cloned sandbox instances, count, and snapshot template ID.
    """

    def __init__(
        self,
        sandboxes: List["Sandbox"],
        count: int,
        snapshot_template_id: Optional[str] = None,
    ):
        self._sandboxes = sandboxes
        self._count = count
        self._snapshot_template_id = snapshot_template_id

    @property
    def sandboxes(self) -> List["Sandbox"]:
        return self._sandboxes

    @property
    def count(self) -> int:
        return self._count

    @property
    def snapshot_template_id(self) -> Optional[str]:
        return self._snapshot_template_id

    def __iter__(self):
        return iter(self._sandboxes)

    def __len__(self) -> int:
        return len(self._sandboxes)

    def __getitem__(self, index: int) -> "Sandbox":
        return self._sandboxes[index]

    def __repr__(self) -> str:
        return (
            f"CloneResult(count={self._count}, "
            f"snapshot_template_id={self._snapshot_template_id!r}, "
            f"sandboxes={len(self._sandboxes)})"
        )


class Sandbox(SandboxApi):
    """
    Novita AI sandbox cloud sandbox is a secure and isolated cloud environment.

    The sandbox allows you to:
    - Access Linux OS
    - Create, list, and delete files and directories
    - Run commands
    - Run isolated code
    - Access the internet

    Check docs [here](https://novita.ai/docs/guides/sandbox-overview).

    Use the `Sandbox.create()` to create a new sandbox.

    Example:
    ```python
    from novita_sandbox.core import Sandbox

    sandbox = Sandbox.create()
    ```
    """

    @property
    def files(self) -> Filesystem:
        """
        Module for interacting with the sandbox filesystem.
        """
        return self._filesystem

    @property
    def commands(self) -> Commands:
        """
        Module for running commands in the sandbox.
        """
        return self._commands

    @property
    def pty(self) -> Pty:
        """
        Module for interacting with the sandbox pseudo-terminal.
        """
        return self._pty

    @property
    def git(self) -> Git:
        """
        Module for running git operations in the sandbox.
        """
        return self._git

    def __init__(self, **opts: Unpack[SandboxOpts]):
        """
        :deprecated: This constructor is deprecated

        Use `Sandbox.create()` to create a new sandbox instead.
        """
        super().__init__(**opts)

        self._transport = get_transport(self.connection_config)

        self._envd_api = httpx.Client(
            base_url=self.envd_api_url,
            transport=self._transport,
            headers=self.connection_config.sandbox_headers,
        )
        self._filesystem = Filesystem(
            self.envd_api_url,
            self._envd_version,
            self.connection_config,
            self._transport.pool,
            self._envd_api,
        )
        self._commands = Commands(
            self.envd_api_url,
            self.connection_config,
            self._transport.pool,
            self._envd_version,
        )
        self._pty = Pty(
            self.envd_api_url,
            self.connection_config,
            self._transport.pool,
            self._envd_version,
        )
        self._git = Git(self._commands)

    def is_running(self, request_timeout: Optional[float] = None) -> bool:
        """
        Check if the sandbox is running.

        :param request_timeout: Timeout for the request in **seconds**

        :return: `True` if the sandbox is running, `False` otherwise

        Example
        ```python
        sandbox = Sandbox.create()
        sandbox.is_running() # Returns True

        sandbox.kill()
        sandbox.is_running() # Returns False
        ```
        """
        try:
            r = self._envd_api.get(
                ENVD_API_HEALTH_ROUTE,
                timeout=self.connection_config.get_request_timeout(request_timeout),
            )

            if r.status_code == 502:
                return False

            err = handle_envd_api_exception(r)

            if err:
                raise err
        except httpx.TimeoutException:
            raise format_request_timeout_error()

        return True

    @classmethod
    def create(
        cls,
        template: Optional[str] = None,
        timeout: Optional[int] = None,
        metadata: Optional[Dict[str, str]] = None,
        envs: Optional[Dict[str, str]] = None,
        secure: Optional[bool] = None,
        allow_internet_access: bool = True,
        auto_pause: Optional[bool] = None,
        mcp: Optional[McpServer] = None,
        network: Optional[SandboxNetworkOpts] = None,
        secret_envs: Optional[Dict[str, str]] = None,
        lifecycle: Optional[SandboxLifecycle] = None,
        volume_mounts: Optional[SandboxVolumeMount] = None,
        node_id: Optional[str] = None,
        **opts: Unpack[ApiParams],
    ) -> Self:
        """
        Create a new sandbox.

        By default, the sandbox is created from the default `base` sandbox template.

        :param template: Sandbox template name or ID
        :param timeout: Timeout for the sandbox in **seconds**, default to 300 seconds. The maximum time a sandbox can be kept alive is 24 hours (86_400 seconds) for Pro users and 1 hour (3_600 seconds) for Hobby users.
        :param metadata: Custom metadata for the sandbox
        :param envs: Custom environment variables for the sandbox
        :param secure: Envd is secured with access token and cannot be used without it, defaults to `True` on modern domains and `False` on legacy domains.
        :param allow_internet_access: Allow sandbox to access the internet, defaults to `True`. If set to `False`, it works the same as setting network `deny_out` to `[0.0.0.0/0]`.
        :param auto_pause: Automatically pause the sandbox after the timeout expires. Defaults to `False`. Use `lifecycle` for new code.
        :param mcp: MCP server to enable in the sandbox
        :param network: Sandbox network configuration
        :param secret_envs: Map sandbox environment variable names to stored secret names
        :param lifecycle: Sandbox lifecycle configuration — ``on_timeout``: ``"kill"`` (default) or ``"pause"``; ``auto_resume``: ``False`` (default) or ``True`` (only when ``on_timeout="pause"``). Example: ``{"on_timeout": "pause", "auto_resume": True}``
        :param volume_mounts: Dictionary mapping mount paths to Volume instances or volume names
        :param node_id: Optional node ID to schedule the sandbox on

        :return: A Sandbox instance for the new sandbox

        Use this method instead of using the constructor to create a new sandbox.
        """
        _raise_if_legacy_mcp(mcp, opts)

        if not template and mcp is not None:
            template = cls.default_mcp_template
        elif not template:
            template = cls.default_template

        transformed_mounts = None
        if volume_mounts:
            transformed_mounts = [
                SandboxVolumeMountAPI(
                    name=vol.name if isinstance(vol, Volume) else vol,
                    path=path,
                )
                for path, vol in volume_mounts.items()
            ]

        sandbox = cls._create(
            template=template,
            auto_pause=auto_pause or False,
            timeout=timeout,
            metadata=metadata,
            envs=envs,
            secure=secure,
            allow_internet_access=allow_internet_access,
            mcp=mcp,
            network=network,
            secret_envs=secret_envs,
            lifecycle=(
                lifecycle
                if lifecycle is not None
                else {"on_timeout": "pause", "auto_resume": False}
                if auto_pause
                else None
            ),
            volume_mounts=transformed_mounts,
            node_id=node_id,
            **opts,
        )

        if mcp is not None:
            token = str(uuid.uuid4())
            sandbox._mcp_token = token

            res = sandbox.commands.run(
                f"mcp-gateway --config {shlex.quote(json.dumps(mcp))}",
                user="root",
                envs={"GATEWAY_ACCESS_TOKEN": token},
            )
            if res.exit_code != 0:
                raise Exception(f"Failed to start MCP gateway: {res.stderr}")

        return sandbox

    @overload
    def connect(
        self,
        timeout: Optional[int] = None,
        **opts: Unpack[ApiParams],
    ) -> Self:
        """
        Connect to a sandbox. If the sandbox is paused, it will be automatically resumed.
        Sandbox must be either running or be paused.

        With sandbox ID you can connect to the same sandbox from different places or environments (serverless functions, etc).

        :param timeout: Timeout for the sandbox in **seconds**
            For running sandboxes, the timeout will update only if the new timeout is longer than the existing one.
        :return: A running sandbox instance

        @example
        ```python
        sandbox = Sandbox.create()
        sandbox.pause()

        # Another code block
        same_sandbox = sandbox.connect()

        :return: A running sandbox instance
        """
        ...

    @overload
    @staticmethod
    def connect(
        sandbox_id: str,
        timeout: Optional[int] = None,
        **opts: Unpack[ApiParams],
    ) -> "Sandbox":
        """
        Connect to a sandbox. If the sandbox is paused, it will be automatically resumed.
        Sandbox must be either running or be paused.

        With sandbox ID you can connect to the same sandbox from different places or environments (serverless functions, etc).

        :param sandbox_id: Sandbox ID
        :param timeout: Timeout for the sandbox in **seconds**.
            For running sandboxes, the timeout will update only if the new timeout is longer than the existing one.
        :return: A running sandbox instance

        @example
        ```python
        sandbox = Sandbox.create()
        Sandbox.pause(sandbox.sandbox_id)

        # Another code block
        same_sandbox = Sandbox.connect(sandbox.sandbox_id)
        ```
        """
        ...

    @class_method_variant("_cls_connect_sandbox")
    def connect(
        self,
        timeout: Optional[int] = None,
        **opts: Unpack[ApiParams],
    ) -> Self:
        """
        Connect to a sandbox. If the sandbox is paused, it will be automatically resumed.
        Sandbox must be either running or be paused.

        With sandbox ID you can connect to the same sandbox from different places or environments (serverless functions, etc).

        :param timeout: Timeout for the sandbox in **seconds**.
            For running sandboxes, the timeout will update only if the new timeout is longer than the existing one.
        :return: A running sandbox instance

        @example
        ```python
        sandbox = Sandbox.create()
        sandbox.pause()

        # Another code block
        same_sandbox = sandbox.connect()
        ```
        """
        SandboxApi._cls_connect(
            sandbox_id=self.sandbox_id,
            timeout=timeout,
            **self.connection_config.get_api_params(**opts),
        )

        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.kill()

    @overload
    def kill(
        self,
        **opts: Unpack[ApiParams],
    ) -> bool:
        """
        Kill the sandbox.

        :return: `True` if the sandbox was killed, `False` if the sandbox was not found
        """
        ...

    @overload
    @staticmethod
    def kill(
        sandbox_id: str,
        **opts: Unpack[ApiParams],
    ) -> bool:
        """
        Kill the sandbox specified by sandbox ID.

        :param sandbox_id: Sandbox ID

        :return: `True` if the sandbox was killed, `False` if the sandbox was not found
        """
        ...

    @class_method_variant("_cls_kill")
    def kill(
        self,
        **opts: Unpack[ApiParams],
    ) -> bool:
        """
        Kill the sandbox specified by sandbox ID.

        :return: `True` if the sandbox was killed, `False` if the sandbox was not found
        """
        return SandboxApi._cls_kill(
            sandbox_id=self.sandbox_id,
            **self.connection_config.get_api_params(**opts),
        )

    @overload
    def set_timeout(
        self,
        timeout: int,
        **opts: Unpack[ApiParams],
    ) -> None:
        """
        Set the timeout of the sandbox.
        This method can extend or reduce the sandbox timeout set when creating the sandbox or from the last call to `.set_timeout`.

        The maximum time a sandbox can be kept alive is 24 hours (86_400 seconds) for Pro users and 1 hour (3_600 seconds) for Hobby users.

        :param timeout: Timeout for the sandbox in **seconds**
        """
        ...

    @overload
    @staticmethod
    def set_timeout(
        sandbox_id: str,
        timeout: int,
        **opts: Unpack[ApiParams],
    ) -> None:
        """
        Set the timeout of the sandbox specified by sandbox ID.
        This method can extend or reduce the sandbox timeout set when creating the sandbox or from the last call to `.set_timeout`.

        The maximum time a sandbox can be kept alive is 24 hours (86_400 seconds) for Pro users and 1 hour (3_600 seconds) for Hobby users.

        :param sandbox_id: Sandbox ID
        :param timeout: Timeout for the sandbox in **seconds**
        """
        ...

    @class_method_variant("_cls_set_timeout")
    def set_timeout(
        self,
        timeout: int,
        **opts: Unpack[ApiParams],
    ) -> None:
        """
        Set the timeout of the sandbox.
        This method can extend or reduce the sandbox timeout set when creating the sandbox or from the last call to `.set_timeout`.

        The maximum time a sandbox can be kept alive is 24 hours (86_400 seconds) for Pro users and 1 hour (3_600 seconds) for Hobby users.

        :param timeout: Timeout for the sandbox in **seconds**

        """

        SandboxApi._cls_set_timeout(
            sandbox_id=self.sandbox_id,
            timeout=timeout,
            **self.connection_config.get_api_params(**opts),
        )

    @overload
    def get_info(
        self,
        **opts: Unpack[ApiParams],
    ) -> SandboxInfo:
        """
        Get sandbox information like sandbox ID, template, metadata, started at/end at date.

        :return: Sandbox info
        """
        ...

    @overload
    @staticmethod
    def get_info(
        sandbox_id: str,
        **opts: Unpack[ApiParams],
    ) -> SandboxInfo:
        """
        Get sandbox information like sandbox ID, template, metadata, started at/end at date.

        :param sandbox_id: Sandbox ID

        :return: Sandbox info
        """
        ...

    @class_method_variant("_cls_get_info")
    def get_info(
        self,
        **opts: Unpack[ApiParams],
    ) -> SandboxInfo:
        """
        Get sandbox information like sandbox ID, template, metadata, started at/end at date.

        :return: Sandbox info
        """
        return SandboxApi._cls_get_info(
            sandbox_id=self.sandbox_id,
            **self.connection_config.get_api_params(**opts),
        )

    @overload
    def get_metrics(
        self,
        start: Optional[datetime.datetime] = None,
        end: Optional[datetime.datetime] = None,
        **opts: Unpack[ApiParams],
    ) -> List[SandboxMetrics]:
        """
        Get the metrics of the current sandbox.

        :param start: Start time for the metrics, defaults to the start of the sandbox
        :param end: End time for the metrics, defaults to the current time

        :return: List of sandbox metrics containing CPU, memory and disk usage information
        """
        ...

    @overload
    @staticmethod
    def get_metrics(
        sandbox_id: str,
        start: Optional[datetime.datetime] = None,
        end: Optional[datetime.datetime] = None,
        **opts: Unpack[ApiParams],
    ) -> List[SandboxMetrics]:
        """
        Get the metrics of the sandbox specified by sandbox ID.

        :param sandbox_id: Sandbox ID
        :param start: Start time for the metrics, defaults to the start of the sandbox
        :param end: End time for the metrics, defaults to the current time

        :return: List of sandbox metrics containing CPU, memory and disk usage information
        """
        ...

    @class_method_variant("_cls_get_metrics")
    def get_metrics(
        self,
        start: Optional[datetime.datetime] = None,
        end: Optional[datetime.datetime] = None,
        **opts: Unpack[ApiParams],
    ) -> List[SandboxMetrics]:
        """
        Get the metrics of the sandbox specified by sandbox ID.

        :param start: Start time for the metrics, defaults to the start of the sandbox
        :param end: End time for the metrics, defaults to the current time

        :return: List of sandbox metrics containing CPU, memory and disk usage information
        """
        if self._envd_version < Version("0.1.5"):
            raise SandboxException(
                "Metrics are not supported in this version of the sandbox, please rebuild your template."
            )

        if self._envd_version < Version("0.2.4"):
            logger.warning(
                "Disk metrics are not supported in this version of the sandbox, please rebuild the template to get disk metrics."
            )

        return SandboxApi._cls_get_metrics(
            sandbox_id=self.sandbox_id,
            start=start,
            end=end,
            **self.connection_config.get_api_params(**opts),
        )

    @classmethod
    def beta_create(
        cls,
        template: Optional[str] = None,
        timeout: Optional[int] = None,
        auto_pause: bool = False,
        metadata: Optional[Dict[str, str]] = None,
        envs: Optional[Dict[str, str]] = None,
        secure: Optional[bool] = None,
        allow_internet_access: bool = True,
        mcp: Optional[McpServer] = None,
        volume_mounts: Optional[SandboxVolumeMount] = None,
        **opts: Unpack[ApiParams],
    ) -> Self:
        """
        [BETA] This feature is in beta and may change in the future.

        Create a new sandbox.

        By default, the sandbox is created from the default `base` sandbox template.

        :param template: Sandbox template name or ID
        :param timeout: Timeout for the sandbox in **seconds**, default to 300 seconds. The maximum time a sandbox can be kept alive is 24 hours (86_400 seconds) for Pro users and 1 hour (3_600 seconds) for Hobby users.
        :param auto_pause: Automatically pause the sandbox after the timeout expires. Defaults to `False`.
        :param metadata: Custom metadata for the sandbox
        :param envs: Custom environment variables for the sandbox
        :param secure: Envd is secured with access token and cannot be used without it, defaults to `True` on modern domains and `False` on legacy domains.
        :param allow_internet_access: Allow sandbox to access the internet, defaults to `True`.
        :param mcp: MCP server to enable in the sandbox
        :param volume_mounts: Dictionary mapping mount paths to Volume instances or volume names

        :return: A Sandbox instance for the new sandbox

        Use this method instead of using the constructor to create a new sandbox.
        """
        _raise_if_legacy_mcp(mcp, opts)

        if not template and mcp is not None:
            template = cls.default_mcp_template
        elif not template:
            template = cls.default_template

        transformed_mounts = None
        if volume_mounts:
            transformed_mounts = [
                SandboxVolumeMountAPI(
                    name=vol.name if isinstance(vol, Volume) else vol,
                    path=path,
                )
                for path, vol in volume_mounts.items()
            ]

        sandbox = cls._create(
            template=template,
            auto_pause=auto_pause,
            timeout=timeout,
            metadata=metadata,
            envs=envs,
            secure=secure,
            allow_internet_access=allow_internet_access,
            mcp=mcp,
            lifecycle=(
                {"on_timeout": "pause", "auto_resume": False} if auto_pause else None
            ),
            volume_mounts=transformed_mounts,
            **opts,
        )

        if mcp is not None:
            token = str(uuid.uuid4())
            sandbox._mcp_token = token

            res = sandbox.commands.run(
                f"mcp-gateway --config {shlex.quote(json.dumps(mcp))}",
                user="root",
                envs={"GATEWAY_ACCESS_TOKEN": token},
            )
            if res.exit_code != 0:
                raise Exception(f"Failed to start MCP gateway: {res.stderr}")

        return sandbox

    @overload
    def pause(
        self,
        **opts: Unpack[ApiParams],
    ) -> None:
        """
        Pause the sandbox.
        """
        ...

    @overload
    @staticmethod
    def pause(
        sandbox_id: str,
        **opts: Unpack[ApiParams],
    ) -> None:
        """
        Pause the sandbox specified by sandbox ID.

        :param sandbox_id: Sandbox ID
        """
        ...

    @class_method_variant("_cls_pause")
    def pause(
        self,
        **opts: Unpack[ApiParams],
    ) -> None:
        """
        Pause the sandbox.

        :return: Sandbox ID that can be used to resume the sandbox
        """

        SandboxApi._cls_pause(
            sandbox_id=self.sandbox_id,
            **self.connection_config.get_api_params(**opts),
        )

    @overload
    def beta_pause(
        self,
        sync: bool = False,
        **opts: Unpack[ApiParams],
    ) -> None: ...

    @overload
    @staticmethod
    def beta_pause(
        sandbox_id: str,
        sync: bool = False,
        **opts: Unpack[ApiParams],
    ) -> None: ...

    @class_method_variant("_cls_pause")
    def beta_pause(
        self,
        sync: bool = False,
        **opts: Unpack[ApiParams],
    ) -> None:
        """
        :deprecated: Use `pause()` instead.
        """
        SandboxApi._cls_pause(
            sandbox_id=self.sandbox_id,
            sync=sync,
            **self.connection_config.get_api_params(**opts),
        )

    @classmethod
    def clone(
        cls,
        sandbox_id: str,
        count: int = 1,
        *,
        node_id: Optional[str] = None,
        strict: bool = False,
        timeout: Optional[int] = None,
        **opts: Unpack[ApiParams],
    ) -> CloneResult:
        """
        Clone a sandbox to create multiple identical sandboxes.

        :param sandbox_id: Source sandbox ID
        :param count: Number of sandboxes to clone
        :param node_id: Optional node ID to schedule the clones on
        :param strict: If true, require exact count or fail
        :param timeout: Timeout for cloned sandboxes in seconds. If omitted, backend applies:
                        - running parent: inherit parent's timeout
                        - paused parent: 15 seconds
        :return: CloneResult containing sandboxes, count, and snapshot_template_id
        """
        clone_result = SandboxApi._cls_clone_sandboxes(
            sandbox_id=sandbox_id,
            count=count,
            node_id=node_id,
            strict=strict,
            timeout=timeout,
            **opts,
        )

        instances: List[Sandbox] = []
        for sb in clone_result.get("sandboxes", []):
            extra_headers = {}
            envd_access_token = sb.get("envd_access_token")
            if envd_access_token:
                extra_headers["X-Access-Token"] = envd_access_token

            connection_config = ConnectionConfig(
                extra_sandbox_headers=extra_headers,
                **opts,
            )

            instances.append(
                cls(
                    sandbox_id=sb["sandbox_id"],
                    sandbox_domain=None,
                    envd_version=Version(sb.get("envd_version") or "0.0.0"),
                    envd_access_token=envd_access_token,
                    traffic_access_token=sb.get("traffic_access_token"),
                    connection_config=connection_config,
                )
            )

        return CloneResult(
            sandboxes=instances,
            count=len(instances),
            snapshot_template_id=clone_result.get("snapshot_template_id"),
        )

    @overload
    def reset(
        self,
        resume: Optional[bool] = None,
        timeout: Optional[int] = None,
        **opts: Unpack[ApiParams],
    ) -> bool:
        """
        Reset sandbox memory and optionally resume the sandbox.
        """
        ...

    @overload
    @staticmethod
    def reset(
        sandbox_id: str,
        resume: Optional[bool] = None,
        timeout: Optional[int] = None,
        **opts: Unpack[ApiParams],
    ) -> bool:
        """
        Reset sandbox memory and optionally resume the sandbox by ID.
        """
        ...

    @class_method_variant("_cls_reset")
    def reset(
        self,
        resume: Optional[bool] = None,
        timeout: Optional[int] = None,
        **opts: Unpack[ApiParams],
    ) -> bool:
        return SandboxApi._cls_reset(
            sandbox_id=self.sandbox_id,
            resume=resume,
            timeout=timeout,
            **self.connection_config.get_api_params(**opts),
        )

    def hotplug_memory(
        self,
        requested_size_mib: int,
        **opts: Unpack[ApiParams],
    ) -> None:
        """
        Add hotplug memory to the running sandbox.

        `requested_size_mib=512` adds 512 MiB of memory; it does not resize the
        sandbox to a total of 512 MiB.

        Deprecated: use `resize(memory_mib=...)` instead.
        """
        return SandboxApi._cls_hotplug_memory(
            sandbox_id=self.sandbox_id,
            requested_size_mib=requested_size_mib,
            **self.connection_config.get_api_params(**opts),
        )

    def resize(
        self,
        *,
        memory_mib: Optional[int] = None,
        **opts: Unpack[ApiParams],
    ) -> None:
        """
        Add hotplug memory to the running sandbox.

        `memory_mib=512` adds 512 MiB of memory; it does not resize the
        sandbox to a total of 512 MiB.
        """
        if memory_mib is None:
            raise ValueError("resize requires memory_mib")

        return self.hotplug_memory(memory_mib, **opts)

    @overload
    def commit(
        self,
        alias: Optional[str] = None,
        **opts: Unpack[ApiParams],
    ):
        ...

    @overload
    @staticmethod
    def commit(
        sandbox_id: str,
        alias: Optional[str] = None,
        **opts: Unpack[ApiParams],
    ):
        ...

    @class_method_variant("_cls_commit")
    def commit(
        self,
        alias: Optional[str] = None,
        **opts: Unpack[ApiParams],
    ):
        """
        Commit this sandbox to create a snapshot template.

        :deprecated: Only legacy domains support this method. Use ``create_snapshot()`` for modern domains.
        """
        return SandboxApi._cls_commit(
            sandbox_id=self.sandbox_id,
            alias=alias,
            **self.connection_config.get_api_params(**opts),
        )

    @classmethod
    def _cls_commit(
        cls,
        sandbox_id: str,
        alias: Optional[str] = None,
        **opts: Unpack[ApiParams],
    ):
        """
        Commit a sandbox to create a snapshot template.

        :deprecated: Only legacy domains support this method. Use ``create_snapshot()`` for modern domains.
        """
        return SandboxApi._cls_commit(sandbox_id, alias=alias, **opts)

    def set_network(
        self,
        allow_out: Optional[List[str]] = None,
        deny_out: Optional[List[str]] = None,
        **opts: Unpack[ApiParams],
    ) -> None: ...

    @overload
    @staticmethod
    def set_network(
        sandbox_id: str,
        allow_out: Optional[List[str]] = None,
        deny_out: Optional[List[str]] = None,
        **opts: Unpack[ApiParams],
    ) -> None: ...

    @class_method_variant("_cls_set_network")
    def set_network(
        self,
        allow_out: Optional[List[str]] = None,
        deny_out: Optional[List[str]] = None,
        **opts: Unpack[ApiParams],
    ) -> None:
        return SandboxApi._cls_set_network(
            sandbox_id=self.sandbox_id,
            allow_out=allow_out,
            deny_out=deny_out,
            **self.connection_config.get_api_params(**opts),
        )

    @overload
    def create_snapshot(
        self,
        **opts: Unpack[ApiParams],
    ) -> SnapshotInfo:
        """
        Create a snapshot of the sandbox's current state.

        The sandbox will be paused while the snapshot is being created.
        The snapshot can be used to create new sandboxes with the same filesystem and state.
        Snapshots are persistent and survive sandbox deletion.

        Use the returned `snapshot_id` with `Sandbox.create(snapshot_id)` to create a new sandbox from the snapshot.

        :return: Snapshot information including the snapshot ID
        """
        ...

    @overload
    @staticmethod
    def create_snapshot(
        sandbox_id: str,
        **opts: Unpack[ApiParams],
    ) -> SnapshotInfo:
        """
        Create a snapshot from the sandbox specified by sandbox ID.

        The sandbox will be paused while the snapshot is being created.

        :param sandbox_id: Sandbox ID

        :return: Snapshot information including the snapshot ID
        """
        ...

    @class_method_variant("_cls_create_snapshot")
    def create_snapshot(
        self,
        **opts: Unpack[ApiParams],
    ) -> SnapshotInfo:
        """
        Create a snapshot of the sandbox's current state.

        The sandbox will be paused while the snapshot is being created.
        The snapshot can be used to create new sandboxes with the same filesystem and state.
        Snapshots are persistent and survive sandbox deletion.

        Use the returned `snapshot_id` with `Sandbox.create(snapshot_id)` to create a new sandbox from the snapshot.

        :return: Snapshot information including the snapshot ID
        """
        return SandboxApi._cls_create_snapshot(
            sandbox_id=self.sandbox_id,
            **self.connection_config.get_api_params(**opts),
        )

    @overload
    def list_snapshots(
        self,
        limit: Optional[int] = None,
        next_token: Optional[str] = None,
        **opts: Unpack[ApiParams],
    ) -> SnapshotPaginator:
        """
        List snapshots for this sandbox.

        :param limit: Maximum number of snapshots to return per page
        :param next_token: Token for pagination

        :return: Paginator for listing snapshots
        """
        ...

    @overload
    @staticmethod
    def list_snapshots(
        sandbox_id: Optional[str] = None,
        limit: Optional[int] = None,
        next_token: Optional[str] = None,
        **opts: Unpack[ApiParams],
    ) -> SnapshotPaginator:
        """
        List all snapshots.

        :param sandbox_id: Filter snapshots by source sandbox ID
        :param limit: Maximum number of snapshots to return per page
        :param next_token: Token for pagination

        :return: Paginator for listing snapshots
        """
        ...

    @class_method_variant("_cls_list_snapshots")
    def list_snapshots(
        self,
        limit: Optional[int] = None,
        next_token: Optional[str] = None,
        **opts: Unpack[ApiParams],
    ) -> SnapshotPaginator:
        """
        List snapshots for this sandbox.

        :param limit: Maximum number of snapshots to return per page
        :param next_token: Token for pagination

        :return: Paginator for listing snapshots
        """
        return SnapshotPaginator(
            sandbox_id=self.sandbox_id,
            limit=limit,
            next_token=next_token,
            **self.connection_config.get_api_params(**opts),
        )

    @staticmethod
    def _cls_list_snapshots(
        sandbox_id: Optional[str] = None,
        limit: Optional[int] = None,
        next_token: Optional[str] = None,
        **opts: Unpack[ApiParams],
    ) -> SnapshotPaginator:
        raise_if_legacy(opts, "Sandbox.list_snapshots")

        return SnapshotPaginator(
            sandbox_id=sandbox_id,
            limit=limit,
            next_token=next_token,
            **opts,
        )

    @staticmethod
    def delete_snapshot(
        snapshot_id: str,
        **opts: Unpack[ApiParams],
    ) -> bool:
        """
        Delete a snapshot.

        :param snapshot_id: Snapshot ID
        :return: `True` if the snapshot was deleted, `False` if it was not found
        """
        return SandboxApi._cls_delete_snapshot(
            snapshot_id=snapshot_id,
            **opts,
        )

    @staticmethod
    def get_quota(**opts: Unpack[ApiParams]) -> "SandboxQuota":
        """
        Get the current account's sandbox quota and usage.

        :return: SandboxQuota containing limit and usage
        """
        return SandboxApi._cls_get_quota(**opts)

    @staticmethod
    def get_events(
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        sandbox_id: Optional[str] = None,
        template_id: Optional[str] = None,
        events: Optional[str] = None,
        state: Optional[str] = None,
        order_asc: Optional[bool] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        **opts: Unpack[ApiParams],
    ) -> "SandboxEventsResult":
        """
        Query sandbox events timeline.

        :param start_time: Unix seconds, inclusive. Defaults to endTime - 30 days.
        :param end_time: Unix seconds, inclusive. Defaults to now.
        :param sandbox_id: Filter by sandbox ID (fuzzy match).
        :param template_id: Filter by template ID (fuzzy match).
        :param events: Comma-separated event types, e.g. "create,pause,resume".
        :param state: Filter by operation status.
        :param order_asc: Sort ascending by recordAt. Default False (descending).
        :param offset: Pagination offset. Default 0.
        :param limit: Max items per page. Default 10, max 100.
        :return: SandboxEventsResult with items, total, and has_more
        """
        return SandboxApi._cls_get_events(
            start_time=start_time,
            end_time=end_time,
            sandbox_id=sandbox_id,
            template_id=template_id,
            events=events,
            state=state,
            order_asc=order_asc,
            offset=offset,
            limit=limit,
            **opts,
        )

    def mount_volume(self, name: str, path: str, **opts: Unpack[ApiParams]):
        """
        Mount a volume to this sandbox.

        :param name: Volume name
        :param path: Mount path inside the sandbox

        :return: Updated sandbox information
        """
        return SandboxApi._cls_mount_volume(
            sandbox_id=self.sandbox_id,
            name=name,
            path=path,
            **self.connection_config.get_api_params(**opts),
        )

    def unmount_volume(self, path: str, force: bool = False, **opts: Unpack[ApiParams]):
        """
        Unmount a volume from this sandbox.

        :param path: Mount path to unmount
        :param force: Force unmount

        :return: Updated sandbox information
        """
        return SandboxApi._cls_unmount_volume(
            sandbox_id=self.sandbox_id,
            path=path,
            force=force,
            **self.connection_config.get_api_params(**opts),
        )

    def get_mcp_token(self) -> Optional[str]:
        """
        Get the MCP token for the sandbox.

        :return: MCP token for the sandbox, or None if MCP is not enabled.
        """
        if not self._mcp_token:
            self._mcp_token = self.files.read("/etc/mcp-gateway/.token", user="root")
        return self._mcp_token

    @classmethod
    def _cls_connect_sandbox(
        cls,
        sandbox_id: str,
        timeout: Optional[int] = None,
        **opts: Unpack[ApiParams],
    ) -> Self:
        sandbox = SandboxApi._cls_connect(
            sandbox_id=sandbox_id,
            timeout=timeout,
            **opts,
        )

        sandbox_headers = {}
        envd_access_token = sandbox.envd_access_token
        if envd_access_token is not None and not isinstance(envd_access_token, Unset):
            sandbox_headers["X-Access-Token"] = envd_access_token

        connection_config = ConnectionConfig(
            extra_sandbox_headers=sandbox_headers,
            **opts,
        )

        return cls(
            sandbox_id=sandbox.sandbox_id,
            sandbox_domain=sandbox.domain,
            connection_config=connection_config,
            envd_version=Version(sandbox.envd_version),
            envd_access_token=envd_access_token,
            traffic_access_token=sandbox.traffic_access_token,
        )

    @classmethod
    def _create(
        cls,
        template: Optional[str],
        timeout: Optional[int],
        auto_pause: Optional[bool],
        metadata: Optional[Dict[str, str]],
        envs: Optional[Dict[str, str]],
        secure: Optional[bool],
        allow_internet_access: bool,
        mcp: Optional[McpServer] = None,
        network: Optional[SandboxNetworkOpts] = None,
        secret_envs: Optional[Dict[str, str]] = None,
        lifecycle: Optional[SandboxLifecycle] = None,
        volume_mounts: Optional[list] = None,
        node_id: Optional[str] = None,
        **opts: Unpack[ApiParams],
    ) -> Self:
        extra_sandbox_headers = {}

        debug = opts.get("debug")
        if debug:
            sandbox_id = "debug_sandbox_id"
            sandbox_domain = None
            envd_version = ENVD_DEBUG_FALLBACK
            envd_access_token = None
            traffic_access_token = None
        else:
            secure = _resolve_secure(secure, opts)
            response = SandboxApi._create_sandbox(
                template=template or cls.default_template,
                timeout=timeout or cls.default_sandbox_timeout,
                auto_pause=auto_pause,
                metadata=metadata,
                env_vars=envs,
                secure=secure,
                allow_internet_access=allow_internet_access,
                mcp=mcp,
                network=network,
                secret_envs=secret_envs,
                lifecycle=lifecycle,
                volume_mounts=volume_mounts,
                node_id=node_id,
                **opts,
            )

            sandbox_id = response.sandbox_id
            sandbox_domain = response.sandbox_domain
            envd_version = Version(response.envd_version)
            envd_access_token = response.envd_access_token
            traffic_access_token = response.traffic_access_token

            if envd_access_token is not None and not isinstance(
                envd_access_token, Unset
            ):
                extra_sandbox_headers["X-Access-Token"] = envd_access_token

        extra_sandbox_headers["Novita-Sandbox-Id"] = sandbox_id
        extra_sandbox_headers["Novita-Sandbox-Port"] = str(ConnectionConfig.envd_port)

        connection_config = ConnectionConfig(
            extra_sandbox_headers=extra_sandbox_headers,
            **opts,
        )

        return cls(
            sandbox_id=sandbox_id,
            sandbox_domain=sandbox_domain,
            envd_version=envd_version,
            envd_access_token=envd_access_token,
            traffic_access_token=traffic_access_token,
            connection_config=connection_config,
        )
