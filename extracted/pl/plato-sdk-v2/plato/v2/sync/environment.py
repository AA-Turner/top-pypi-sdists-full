"""Plato SDK v2 - Synchronous Environment."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING

from plato._generated.api.v2 import jobs
from plato._generated.models import (
    AddSSHKeyRequest,
    AppApiV2SchemasSessionCreateSnapshotRequest,
    CreateCheckpointRequest,
    CreateSnapshotResult,
    ExecuteCommandRequest,
    ExecuteCommandResult,
    ResetJobResult,
    ResetSessionRequest,
    SessionStateResult,
    SetDateRequest,
    SetDateResult,
)

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from plato.v2.sync.session import Session


class Environment:
    """An environment represents a single VM within a session.

    Usage:
        with client.session(envs=[EnvOption(simulator="espocrm")]) as session:
            for env in session.envs:
                state = env.get_state()
                result = env.execute("ls -la")
    """

    def __init__(
        self,
        session: Session,
        job_id: str,
        alias: str,
        artifact_id: str | None = None,
        simulator: str | None = None,
        status: str | None = None,
        public_url: str | None = None,
        mesh_ip: str | None = None,
        is_desktop: bool = False,
    ):
        self._session = session
        self.job_id = job_id
        self.alias = alias
        self.artifact_id = artifact_id
        self.simulator = simulator
        self.status = status
        self.public_url = public_url
        self.mesh_ip = mesh_ip
        self.is_desktop = is_desktop

    @property
    def _http(self):
        """Access the HTTP client from the session."""
        return self._session._http

    @property
    def _api_key(self) -> str:
        """Access the API key from the session."""
        return self._session._api_key

    @property
    def session_id(self) -> str:
        return self._session.session_id

    @property
    def internal_hostname(self) -> str:
        """Internal mesh network hostname for this environment.

        Returns the hostname that can be used to reach this VM from other VMs
        in the same session via the WireGuard mesh network. This hostname is
        registered in /etc/hosts on all session VMs after connect_network().

        Returns:
            Hostname in format "{alias}.plato.internal"
        """
        return f"{self.alias}.plato.internal"

    def get_mesh_ip(self) -> str | None:
        """Get the mesh network IP for this environment.

        Returns the cached mesh IP if available (set from wait_for_ready),
        otherwise fetches from the job info API.

        Returns:
            Mesh IP string (e.g., "10.100.0.123") or None if not assigned.
        """
        if self.mesh_ip:
            return self.mesh_ip

        logger.debug("mesh_ip not cached for job %s, falling back to API call", self.job_id)

        result = jobs.get_job_info.sync(
            client=self._http,
            job_id=self.job_id,
            x_api_key=self._api_key,
        )
        if result and result.mesh_ip:
            self.mesh_ip = result.mesh_ip
        return self.mesh_ip

    def add_ssh_key(self, public_key: str, username: str = "root") -> None:
        """Add an SSH public key to this specific VM.

        Args:
            public_key: SSH public key string.
            username: User to add the key for (default: root).
        """
        jobs.add_ssh_key.sync(
            client=self._http,
            job_id=self.job_id,
            body=AddSSHKeyRequest(public_key=public_key, username=username),
            x_api_key=self._api_key,
        )

    def reset(self, **kwargs) -> ResetJobResult:
        """Reset this environment to initial state."""
        request = ResetSessionRequest(**kwargs)
        return jobs.reset.sync(
            client=self._http,
            job_id=self.job_id,
            body=request,
            x_api_key=self._api_key,
        )

    def get_state(self) -> SessionStateResult:
        """Get state from this environment."""
        return jobs.state.sync(
            client=self._http,
            job_id=self.job_id,
            x_api_key=self._api_key,
        )

    def execute(
        self,
        command: str,
        timeout: int = 30,
    ) -> ExecuteCommandResult:
        """Execute a command on this environment.

        Args:
            command: Shell command to execute.
            timeout: Command timeout in seconds.

        Returns:
            Execution result with stdout, stderr, exit_code.
        """
        request = ExecuteCommandRequest(
            command=command,
            timeout=timeout,
        )
        return jobs.execute.sync(
            client=self._http,
            job_id=self.job_id,
            body=request,
            x_api_key=self._api_key,
        )

    def set_date(
        self,
        dt: datetime,
        timeout: int = 30,
    ) -> SetDateResult:
        """Set the system date on this environment.

        Args:
            dt: The datetime to set.
            timeout: Command timeout in seconds.

        Returns:
            SetDateResult with success status and command output.
        """
        request = SetDateRequest(
            datetime=dt.isoformat(),
            timeout=timeout,
        )
        return jobs.set_date.sync(
            client=self._http,
            job_id=self.job_id,
            body=request,
            x_api_key=self._api_key,
        )

    def snapshot(self) -> CreateSnapshotResult:
        """Create a snapshot of this environment."""
        return jobs.snapshot.sync(
            client=self._http,
            job_id=self.job_id,
            body=CreateCheckpointRequest(),
            x_api_key=self._api_key,
        )

    def snapshot_store(
        self,
        override_service: str | None = None,
        override_version: str | None = None,
        override_dataset: str | None = None,
    ) -> CreateSnapshotResult:
        """Create a snapshot-store snapshot of this environment.

        Uses the snapshot-store pipeline for chunk-based deduplication and
        efficient storage. This is the preferred method for new base snapshots.

        Args:
            override_service: Override simulator/service name in artifact metadata.
            override_version: Override version/git_hash in artifact metadata.
            override_dataset: Override dataset name in artifact metadata.

        Returns:
            CreateSnapshotResult with artifact_id.
        """
        return jobs.snapshot_store.sync(
            client=self._http,
            job_id=self.job_id,
            body=AppApiV2SchemasSessionCreateSnapshotRequest(
                override_service=override_service,
                override_version=override_version,
                override_dataset=override_dataset,
            ),
            x_api_key=self._api_key,
        )

    def close(self) -> None:
        """Close this environment."""
        jobs.close.sync(
            client=self._http,
            job_id=self.job_id,
            x_api_key=self._api_key,
        )

    @property
    def sdk(self):
        """Get the sim SDK client for this environment.

        Lazily imports the sim SDK package based on ``self.simulator`` and
        returns a cached :class:`Client` instance.

        Raises:
            ValueError: If ``simulator`` is not set (e.g. created via ``Env.artifact``).
            ImportError: If the sim SDK package is not installed.
        """
        if not hasattr(self, "_sdk"):
            if not self.simulator:
                raise ValueError(
                    "Cannot resolve sim SDK: 'simulator' is not set on this environment. "
                    "Set env.simulator = 'ubuntu-vm' or use Env.simulator() instead of Env.artifact()."
                )
            module_name = self.simulator.replace("-", "_")
            import importlib

            mod = importlib.import_module(f"plato.sims.{module_name}")
            self._sdk = mod.Client.from_environment(self)
        return self._sdk

    def __repr__(self) -> str:
        return f"Environment(alias={self.alias!r}, job_id={self.job_id!r})"
