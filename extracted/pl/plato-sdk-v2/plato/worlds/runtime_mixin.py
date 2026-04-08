"""Runtime mixin for Plato worlds.

Provides the world's runtime context (RuntimeInfo) and manages the Plato
session lifecycle when running on a VM runtime.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from plato.runtimes.base import RuntimeInfo

if TYPE_CHECKING:
    from plato.v2.async_.environment import Environment
    from plato.v2.async_.session import SerializedSession, Session

logger = logging.getLogger(__name__)


class RuntimeMixin:
    """Mixin providing runtime context and Plato session for BaseWorld.

    Holds the :class:`RuntimeInfo` describing the world's execution environment
    and manages the Plato session (heartbeat, env access) when running on a VM.
    """

    def __init__(self) -> None:
        super().__init__()
        self._runtime_info: RuntimeInfo | None = None
        self._plato_session: Session | None = None

    @property
    def runtime_info(self) -> RuntimeInfo:
        """The world's runtime environment info.

        Raises:
            RuntimeError: If accessed before ``run()`` is called with runtime info.
        """
        if self._runtime_info is None:
            raise RuntimeError("No runtime info — world not started or no runtime provided")
        return self._runtime_info

    @property
    def plato_session(self) -> Session | None:
        """The connected Plato session, if running on a managed VM."""
        return self._plato_session

    # -- Plato session lifecycle -------------------------------------------

    async def _connect_plato_session(self) -> None:
        """Restore the Plato session from RuntimeInfo if available."""
        from plato.v2.async_.session import Session

        if self._runtime_info is None or self._runtime_info.serialized_session is None:
            return

        serialized_session = cast("SerializedSession | Mapping[str, object]", self._runtime_info.serialized_session)
        logger.debug("Restoring Plato session from runtime info")
        self._plato_session = await Session.load(
            serialized_session,
            start_heartbeat=True,
            heartbeat_use_process=True,
        )
        logger.debug(f"Plato session {self._plato_session.session_id} restored, heartbeat started")

    async def _resolve_world_hostname(self) -> None:
        """Resolve the world VM's mesh IP and update runtime_info hostname.

        When launched by Chronos, the runner creates RuntimeInfo with
        hostname='localhost'. After the Plato session is restored we can
        look up the world VM's actual mesh IP so agent VMs can reach it.
        """
        if self._runtime_info is None or self._plato_session is None:
            return
        if self._runtime_info.hostname not in ("localhost", "127.0.0.1", ""):
            return  # already has a real hostname
        envs = self._plato_session.envs
        if not envs:
            return
        world_env = envs[0]
        mesh_ip = await world_env.get_mesh_ip()
        if mesh_ip:
            self._runtime_info = self._runtime_info.model_copy(update={"hostname": mesh_ip})
            logger.info("Resolved world hostname to %s", mesh_ip)

        # Register the SSH public key on the world VM so agent VMs can
        # clone git repos back from it.
        ssh_key_path = self._runtime_info.ssh_key_path
        if ssh_key_path:
            pub_key_path = Path(str(ssh_key_path) + ".pub")
            if pub_key_path.exists():
                await world_env.add_ssh_key(pub_key_path.read_text().strip())
                logger.info("Registered SSH public key on world VM")

    async def _disconnect_plato_session(self) -> None:
        """Stop heartbeat for the Plato session (does not close the session)."""
        if self._plato_session:
            try:
                await self._plato_session.stop_heartbeat()
                logger.debug("Plato session heartbeat stopped")
            except Exception as e:
                logger.warning(f"Error stopping Plato heartbeat: {e}")

    # -- Environment access ------------------------------------------------

    def get_env(self, alias: str) -> Environment | None:
        """Get an environment by alias from the Plato session."""
        if not self._plato_session:
            logger.warning("Cannot get env: Plato session not connected")
            return None
        return self._plato_session.get_env(alias)

    @property
    def envs(self) -> list[Any]:
        """Get all environments in the Plato session."""
        if not self._plato_session:
            return []
        return self._plato_session.envs
