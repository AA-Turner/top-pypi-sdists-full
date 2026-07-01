"""RuntimeConnectionManager — manages local and remote runtime client switching."""

import asyncio
import contextlib
import logging
import typing as t
from dataclasses import dataclass

from dreadnode.app.client.managed_client import ManagedRuntimeClient
from dreadnode.app.tui.sessions_manager import SessionStateBundle

if t.TYPE_CHECKING:
    from dreadnode.app.api.client import ApiClient
    from dreadnode.app.client.models import RuntimeInfo

__all__ = [
    "RemoteConnectionInfo",
    "RuntimeConnectionManager",
    "SessionStateBundle",
]

logger = logging.getLogger(__name__)

_KEEPALIVE_INTERVAL_SECONDS = 30
_KEEPALIVE_EXTEND_SECONDS = 300


@dataclass
class RemoteConnectionInfo:
    """Metadata about the active remote connection."""

    runtime_id: str
    sandbox_url: str


class RuntimeConnectionManager:
    """Holds local + optional remote ManagedRuntimeClient, tracks which is active.

    - ``local_client``: always the in-process local server (boot, restart, profile).
    - ``active_client``: whichever runtime is currently active (chat, files, shell).
    """

    def __init__(
        self,
        local_client: ManagedRuntimeClient,
        api_client: "ApiClient | None" = None,
        org: str | None = None,
        workspace: str | None = None,
        on_stash_state: t.Callable[[], SessionStateBundle] | None = None,
        on_restore_state: t.Callable[[SessionStateBundle], None] | None = None,
        on_after_connect: t.Callable[[], t.Awaitable[None]] | None = None,
        on_after_disconnect: t.Callable[[], t.Awaitable[None]] | None = None,
    ) -> None:
        self._local_client = local_client
        self._remote_client: ManagedRuntimeClient | None = None
        self._remote_runtime_info: t.Any = None
        self._is_remote = False
        self._connected_runtime_id: str | None = None
        self._keepalive_task: asyncio.Task[None] | None = None
        self._api_client = api_client
        self._org = org
        self._workspace = workspace
        self._on_stash_state = on_stash_state
        self._on_restore_state = on_restore_state
        self._on_after_connect = on_after_connect
        self._on_after_disconnect = on_after_disconnect
        self._local_state_bundle: SessionStateBundle | None = None

    @property
    def local_client(self) -> ManagedRuntimeClient:
        return self._local_client

    @property
    def active_client(self) -> ManagedRuntimeClient:
        if self._is_remote and self._remote_client is not None:
            return self._remote_client
        return self._local_client

    @property
    def is_remote(self) -> bool:
        return self._is_remote

    @property
    def connected_runtime_id(self) -> str | None:
        return self._connected_runtime_id

    @property
    def remote_runtime_info(self) -> "RuntimeInfo | None":
        """RuntimeInfo from the connected remote, if available."""
        return self._remote_runtime_info if self._is_remote else None

    @property
    def connection_info(self) -> RemoteConnectionInfo | None:
        if not self._is_remote or self._remote_client is None or self._connected_runtime_id is None:
            return None
        return RemoteConnectionInfo(
            runtime_id=self._connected_runtime_id,
            sandbox_url=self._remote_client.server_url,
        )

    def set_api_context(
        self,
        api_client: "ApiClient",
        org: str,
        workspace: str,
    ) -> None:
        """Update platform API context (called after auth/boot)."""
        self._api_client = api_client
        self._org = org
        self._workspace = workspace

    async def connect(
        self,
        runtime_id: str,
        sandbox_url: str,
        token: str,
    ) -> None:
        """Create a remote client, health check it, and switch active."""
        remote = ManagedRuntimeClient(
            server_url=sandbox_url,
            auto_start=False,
            auth_token=token,
        )
        previous_remote_client = self._remote_client
        previous_remote_runtime_info = self._remote_runtime_info
        previous_runtime_id = self._connected_runtime_id
        previous_remote_state_bundle: SessionStateBundle | None = None

        try:
            await remote.start()
        except RuntimeError as exc:
            raise ConnectionError(str(exc)) from exc

        # Only stash local state on the first remote connection.
        # If we're already remote (switching remotes), the original local
        # bundle is already saved and must not be overwritten.
        if self._on_stash_state is not None:
            if self._is_remote:
                previous_remote_state_bundle = self._on_stash_state()
            else:
                self._local_state_bundle = self._on_stash_state()

        # Propagate platform project from local client so remote sessions
        # get proper project binding
        local_project = self._local_client._platform_project
        if local_project:
            remote._platform_project = local_project

        # Validates auth — /api/health is public but /api/runtime
        # requires a valid token. A failure here rolls back the connection.
        try:
            remote_runtime_info = await remote.fetch_runtime_info()
        except Exception as exc:
            await remote.close()
            raise ConnectionError(
                f"Failed to connect to remote runtime {runtime_id}: {exc}"
            ) from exc

        if previous_remote_client is not None:
            await self._stop_keepalive()

        self._remote_client = remote
        self._connected_runtime_id = runtime_id
        self._remote_runtime_info = remote_runtime_info
        self._is_remote = True
        self._start_keepalive(runtime_id)

        logger.info("Connected to remote runtime %s at %s", runtime_id, sandbox_url)

        # Let the app refresh runtime info, sessions, UI state for the remote.
        # If this fails, roll back — a half-switched state is worse than no switch.
        if self._on_after_connect is not None:
            try:
                await self._on_after_connect()
            except Exception as exc:
                await self._rollback_failed_connect(
                    failed_remote=remote,
                    previous_remote_client=previous_remote_client,
                    previous_remote_runtime_info=previous_remote_runtime_info,
                    previous_runtime_id=previous_runtime_id,
                    previous_remote_state_bundle=previous_remote_state_bundle,
                )
                raise ConnectionError(
                    f"Failed to set up remote runtime {runtime_id}: {exc}"
                ) from exc

        if previous_remote_client is not None:
            await previous_remote_client.close()

    async def disconnect(self) -> None:
        """Stop keepalive, close remote client, restore local state, switch back to local."""
        await self._teardown_remote()
        logger.info("Disconnected from remote runtime, back to local")

        if self._on_after_disconnect is not None:
            await self._on_after_disconnect()

    async def close(self) -> None:
        """Tear down everything — remote (if active) and local."""
        await self._teardown_remote()
        await self._local_client.close()

    async def _teardown_remote(self) -> None:
        """Shared cleanup: stop keepalive, close remote, restore local state."""
        await self._stop_keepalive()
        if self._remote_client is not None:
            await self._remote_client.close()
            self._remote_client = None
        self._connected_runtime_id = None
        self._is_remote = False
        self._remote_runtime_info = None
        if self._local_state_bundle is not None and self._on_restore_state is not None:
            self._on_restore_state(self._local_state_bundle)
            self._local_state_bundle = None

    async def _rollback_failed_connect(
        self,
        failed_remote: ManagedRuntimeClient,
        previous_remote_client: ManagedRuntimeClient | None,
        previous_remote_runtime_info: t.Any,
        previous_runtime_id: str | None,
        previous_remote_state_bundle: SessionStateBundle | None,
    ) -> None:
        """Undo a failed connect without dropping a working remote session."""
        await self._stop_keepalive()
        if self._remote_client is failed_remote:
            self._remote_client = None
        await failed_remote.close()

        if previous_remote_client is not None and previous_runtime_id is not None:
            self._remote_client = previous_remote_client
            self._remote_runtime_info = previous_remote_runtime_info
            self._connected_runtime_id = previous_runtime_id
            self._is_remote = True
            self._start_keepalive(previous_runtime_id)
            if previous_remote_state_bundle is not None and self._on_restore_state is not None:
                self._on_restore_state(previous_remote_state_bundle)
            return

        self._connected_runtime_id = None
        self._is_remote = False
        self._remote_runtime_info = None
        if self._local_state_bundle is not None and self._on_restore_state is not None:
            self._on_restore_state(self._local_state_bundle)
            self._local_state_bundle = None

    def _start_keepalive(self, runtime_id: str) -> None:
        if self._keepalive_task is not None:
            self._keepalive_task.cancel()
        self._keepalive_task = asyncio.create_task(self._keepalive_loop(runtime_id))

    async def _stop_keepalive(self) -> None:
        if self._keepalive_task is not None:
            self._keepalive_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._keepalive_task
            self._keepalive_task = None

    async def _keepalive_loop(self, runtime_id: str) -> None:
        while True:
            await asyncio.sleep(_KEEPALIVE_INTERVAL_SECONDS)
            try:
                if self._api_client is not None and self._org and self._workspace:
                    await asyncio.to_thread(
                        self._api_client.keepalive_runtime,
                        self._org,
                        self._workspace,
                        runtime_id,
                        extend_seconds=_KEEPALIVE_EXTEND_SECONDS,
                    )
            except Exception:
                logger.warning("Keepalive failed for runtime %s", runtime_id, exc_info=True)

            if (
                not self._is_remote
                or self._connected_runtime_id != runtime_id
                or self._remote_client is None
            ):
                return

            try:
                interactive_alive = await self._remote_client.probe_interactive_transport()
                if interactive_alive:
                    try:
                        self._remote_runtime_info = await self._remote_client.fetch_runtime_info()
                    except Exception:
                        logger.debug(
                            "Remote runtime info refresh failed after successful websocket probe for runtime %s",
                            runtime_id,
                            exc_info=True,
                        )
                    continue

                self._remote_runtime_info = await self._remote_client.fetch_runtime_info()
            except Exception:
                logger.warning(
                    "Remote health check failed for runtime %s", runtime_id, exc_info=True
                )
                await self._handle_remote_health_failure(runtime_id)
                return

    async def _handle_remote_health_failure(self, runtime_id: str) -> None:
        """Fall back to local if the active remote becomes unreachable."""
        if (
            not self._is_remote
            or self._connected_runtime_id != runtime_id
            or self._remote_client is None
        ):
            return

        current_task = asyncio.current_task()
        if self._keepalive_task is current_task:
            self._keepalive_task = None

        remote_client = self._remote_client
        self._remote_client = None
        self._connected_runtime_id = None
        self._is_remote = False
        self._remote_runtime_info = None

        await remote_client.close()

        if self._local_state_bundle is not None and self._on_restore_state is not None:
            self._on_restore_state(self._local_state_bundle)
            self._local_state_bundle = None

        if self._on_after_disconnect is not None:
            await self._on_after_disconnect()
