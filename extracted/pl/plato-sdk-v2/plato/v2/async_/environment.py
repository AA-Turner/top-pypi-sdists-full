"""Plato SDK v2 - Asynchronous Environment."""

from __future__ import annotations

import asyncio
import logging
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import BaseModel

from plato._generated.api.v2 import jobs
from plato._generated.models import (
    AddSSHKeyRequest,
    AppApiV2SchemasSessionCreateSnapshotRequest,
    ConnectRoutingInfoResult,
    CreateCheckpointRequest,
    CreateDiskSnapshotRequest,
    CreateDiskSnapshotResult,
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
    from plato.v2.async_.session import Session


class SSHInfo(BaseModel):
    """SSH connection information for an environment."""

    job_id: str
    gateway_host: str
    private_key_path: str | None = None

    @property
    def sni(self) -> str:
        """SNI for TLS routing through gateway."""
        return f"{self.job_id}--22.{self.gateway_host}"

    @property
    def proxy_command(self) -> str:
        """ProxyCommand for SSH config."""
        return f"openssl s_client -quiet -connect {self.gateway_host}:443 -servername {self.sni} 2>/dev/null"

    def ssh_command(self, command: str | None = None) -> list[str]:
        """Build SSH command with all necessary options.

        Args:
            command: Optional command to run on remote. If None, opens interactive shell.

        Returns:
            List of command arguments for subprocess.
        """
        args = [
            "ssh",
            "-o",
            "StrictHostKeyChecking=no",
            "-o",
            "UserKnownHostsFile=/dev/null",
            "-o",
            "LogLevel=ERROR",
            "-o",
            f"ProxyCommand={self.proxy_command}",
        ]
        if self.private_key_path:
            args.extend(["-i", self.private_key_path])
        args.append(f"root@{self.job_id}.plato")
        if command:
            args.append(command)
        return args

    def ssh_opts_string(self) -> str:
        """Get SSH options as a string for use with rsync -e."""
        opts = [
            "-o StrictHostKeyChecking=no",
            "-o UserKnownHostsFile=/dev/null",
            "-o LogLevel=ERROR",
            f"-o 'ProxyCommand={self.proxy_command}'",
        ]
        if self.private_key_path:
            opts.insert(0, f"-i {self.private_key_path}")
        return "ssh " + " ".join(opts)


class RsyncResult(BaseModel):
    """Result of an rsync operation."""

    success: bool
    message: str
    local_path: str
    remote_path: str


class ReverseTunnel:
    """A reverse SSH tunnel that allows the VM to connect back to local machine.

    Uses SSH -R flag through the gateway to set up port forwarding from
    VM back to local. This enables SSHFS mounts from VM to local filesystem.
    """

    def __init__(
        self,
        job_id: str,
        private_key_path: str,
        local_port: int = 22,
        remote_port: int = 2222,
    ):
        self.job_id = job_id
        self.private_key_path = private_key_path
        self.local_port = local_port
        self.remote_port = remote_port
        self._process: subprocess.Popen | None = None

    def start(self) -> bool:
        """Start the reverse tunnel in background.

        Returns:
            True if tunnel started successfully.
        """
        gateway_host = os.getenv("PLATO_GATEWAY_HOST", "gateway.plato.so")
        sni = f"{self.job_id}--22.{gateway_host}"
        proxy_cmd = f"openssl s_client -quiet -connect {gateway_host}:443 -servername {sni} 2>/dev/null"

        # SSH command with reverse port forwarding
        # -R remote_port:localhost:local_port makes remote_port on VM forward to local_port on local machine
        ssh_args = [
            "ssh",
            "-i",
            self.private_key_path,
            "-o",
            "StrictHostKeyChecking=no",
            "-o",
            "UserKnownHostsFile=/dev/null",
            "-o",
            "LogLevel=ERROR",
            "-o",
            f"ProxyCommand={proxy_cmd}",
            "-R",
            f"{self.remote_port}:localhost:{self.local_port}",
            "-N",  # Don't execute remote command
            f"root@{self.job_id}.plato",
        ]

        try:
            self._process = subprocess.Popen(
                ssh_args,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
            )
            # Give it a moment to establish
            import time

            time.sleep(1)
            # Check if still running
            if self._process.poll() is not None:
                return False
            return True
        except Exception:
            return False

    def stop(self) -> None:
        """Stop the reverse tunnel."""
        if self._process:
            self._process.terminate()
            try:
                self._process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._process.kill()
            self._process = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        return False


class Environment:
    """An environment represents a single VM within a session.

    Usage:
        async with client.session(envs=[EnvOption(simulator="espocrm")]) as session:
            for env in session.envs:
                state = await env.get_state()
                result = await env.execute("ls -la")
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
    ):
        self._session = session
        self.job_id = job_id
        self.alias = alias
        self.artifact_id = artifact_id
        self.simulator = simulator
        self.status = status
        self.public_url = public_url
        self.mesh_ip = mesh_ip

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

    async def get_mesh_ip(self) -> str | None:
        """Get the mesh network IP for this environment.

        Returns the cached mesh IP if available (set from wait_for_ready),
        otherwise fetches from the job info API.

        Returns:
            Mesh IP string (e.g., "10.100.0.123") or None if not assigned.
        """
        if self.mesh_ip:
            return self.mesh_ip

        logger.warning("mesh_ip not cached for job %s, falling back to API call", self.job_id)

        result = await jobs.get_job_info.asyncio(
            client=self._http,
            job_id=self.job_id,
            x_api_key=self._api_key,
        )
        if result and result.mesh_ip:
            self.mesh_ip = result.mesh_ip
        return self.mesh_ip

    async def add_ssh_key(self, public_key: str, username: str = "root") -> None:
        """Add an SSH public key to this specific VM.

        Args:
            public_key: SSH public key string.
            username: User to add the key for (default: root).
        """
        await jobs.add_ssh_key.asyncio(
            client=self._http,
            job_id=self.job_id,
            body=AddSSHKeyRequest(public_key=public_key, username=username),
            x_api_key=self._api_key,
        )

    async def reset(self, **kwargs) -> ResetJobResult:
        """Reset this environment to initial state."""
        request = ResetSessionRequest(**kwargs)
        return await jobs.reset.asyncio(
            client=self._http,
            job_id=self.job_id,
            body=request,
            x_api_key=self._api_key,
        )

    async def get_state(self) -> SessionStateResult:
        """Get state from this environment."""
        return await jobs.state.asyncio(
            client=self._http,
            job_id=self.job_id,
            x_api_key=self._api_key,
        )

    async def execute(
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
        return await jobs.execute.asyncio(
            client=self._http,
            job_id=self.job_id,
            body=request,
            x_api_key=self._api_key,
        )

    async def set_date(
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
        return await jobs.set_date.asyncio(
            client=self._http,
            job_id=self.job_id,
            body=request,
            x_api_key=self._api_key,
        )

    async def snapshot(self) -> CreateSnapshotResult:
        """Create a snapshot of this environment."""
        return await jobs.snapshot.asyncio(
            client=self._http,
            job_id=self.job_id,
            body=CreateCheckpointRequest(),
            x_api_key=self._api_key,
        )

    async def snapshot_store(
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
        return await jobs.snapshot_store.asyncio(
            client=self._http,
            job_id=self.job_id,
            body=AppApiV2SchemasSessionCreateSnapshotRequest(
                override_service=override_service,
                override_version=override_version,
                override_dataset=override_dataset,
            ),
            x_api_key=self._api_key,
        )

    async def close(self) -> None:
        """Close this environment."""
        await jobs.close.asyncio(
            client=self._http,
            job_id=self.job_id,
            x_api_key=self._api_key,
        )

    async def get_connection_info(self) -> ConnectRoutingInfoResult:
        """Get connection/routing info for this environment.

        Returns connection details including:
        - vm_gateway_ip: Gateway IP for VM to reach the host
        - vm_private_ip: Private IP of the VM
        - worker_private_ip: Private IP of the worker
        - ready: Whether the job is ready

        Returns:
            ConnectRoutingInfoResult with routing information.
        """
        return await jobs.connect_routing_info.asyncio(
            client=self._http,
            job_id=self.job_id,
        )

    def __repr__(self) -> str:
        return f"Environment(alias={self.alias!r}, job_id={self.job_id!r})"

    async def disk_snapshot(
        self,
        override_service: str | None = None,
        override_version: str | None = None,
        override_dataset: str | None = None,
        target: str | None = None,
    ) -> CreateDiskSnapshotResult:
        """Create a disk-only snapshot of this environment.

        Disk snapshots capture only the disk state (no memory). On resume, the VM
        will do a fresh boot with the preserved disk state. This is faster to
        create and smaller to store than full snapshots.

        Args:
            override_service: Override simulator/service name in artifact metadata.
            override_version: Override version/tag in artifact metadata.
            override_dataset: Override dataset name in artifact metadata.
            target: Target domain for routing (e.g., sims.plato.so).

        Returns:
            CreateDiskSnapshotResult with artifact_id.

        Example:
            # Save as my-app:v1@production
            result = await env.disk_snapshot(
                override_service="my-app",
                override_version="v1",
                override_dataset="production",
                target="sims.plato.so",
            )
            print(f"Artifact: {result.artifact_id}")
        """
        from plato._generated.api.v2.jobs import disk_snapshot

        return await disk_snapshot.asyncio(
            client=self._http,
            job_id=self.job_id,
            body=CreateDiskSnapshotRequest(
                override_service=override_service,
                override_version=override_version,
                override_dataset=override_dataset,
                target=target,
            ),
            x_api_key=self._api_key,
        )

    # =========================================================================
    # SSH/Rsync Helpers
    # =========================================================================

    def get_ssh_info(self, private_key_path: str | None = None) -> SSHInfo:
        """Get SSH connection info for this environment.

        Args:
            private_key_path: Path to private key file. Required for rsync/ssh.

        Returns:
            SSHInfo with connection details.

        Example:
            ssh_info = env.get_ssh_info("/path/to/key")
            subprocess.run(ssh_info.ssh_command("ls -la"))
        """
        gateway_host = os.getenv("PLATO_GATEWAY_HOST", "gateway.plato.so")
        return SSHInfo(
            job_id=self.job_id,
            gateway_host=gateway_host,
            private_key_path=private_key_path,
        )

    async def rsync(
        self,
        local_path: str | Path,
        remote_path: str,
        private_key_path: str,
        delete: bool = True,
        exclude: list[str] | None = None,
        verbose: bool = False,
    ) -> RsyncResult:
        """Rsync files to this environment.

        Args:
            local_path: Local file or directory path.
            remote_path: Remote destination path on VM.
            private_key_path: Path to SSH private key.
            delete: Delete files on remote that don't exist locally (default True).
            exclude: Additional patterns to exclude.
            verbose: Show verbose output.

        Returns:
            RsyncResult with success status and message.

        Example:
            result = await env.rsync("./src", "/app/src", key_path)
            if not result.success:
                print(f"Rsync failed: {result.message}")
        """
        local_path_obj = Path(local_path)
        if not local_path_obj.exists():
            return RsyncResult(
                success=False,
                message=f"Local path does not exist: {local_path}",
                local_path=str(local_path),
                remote_path=remote_path,
            )

        is_file = local_path_obj.is_file()
        ssh_info = self.get_ssh_info(private_key_path)

        # Create remote directory first
        if is_file:
            mkdir_target = str(Path(remote_path).parent)
        else:
            mkdir_target = remote_path

        await self.execute(f"mkdir -p {mkdir_target}", timeout=30)

        # Build rsync command
        ssh_cmd = ssh_info.ssh_opts_string()

        if is_file:
            rsync_args = [
                "rsync",
                "-az",
                "-e",
                ssh_cmd,
                str(local_path),
                f"root@{self.job_id}.plato:{remote_path}",
            ]
        else:
            rsync_args = [
                "rsync",
                "-az",
                "--filter=:- .gitignore",
                "--exclude=.git",
                "--exclude=__pycache__",
                "--exclude=node_modules",
                "--exclude=.venv",
                "--exclude=*.pyc",
                "-e",
                ssh_cmd,
                f"{local_path}/",
                f"root@{self.job_id}.plato:{remote_path}/",
            ]
            if delete:
                rsync_args.insert(2, "--delete")

        # Add custom excludes
        if exclude:
            for pattern in exclude:
                rsync_args.insert(-2, f"--exclude={pattern}")

        if verbose:
            rsync_args.insert(2, "-v")

        # Run rsync in executor to not block
        loop = asyncio.get_event_loop()

        def _run_rsync():
            try:
                result = subprocess.run(
                    rsync_args,
                    capture_output=True,
                    text=True,
                    timeout=600,
                )
                if result.returncode != 0:
                    return (False, f"rsync failed: {result.stderr[:200]}")
                return (True, "synced")
            except subprocess.TimeoutExpired:
                return (False, "rsync timed out")
            except Exception as e:
                return (False, str(e))

        success, message = await loop.run_in_executor(None, _run_rsync)
        return RsyncResult(
            success=success,
            message=message,
            local_path=str(local_path),
            remote_path=remote_path,
        )

    async def ensure_rsync(self) -> bool:
        """Ensure rsync is installed on the VM.

        Returns:
            True if rsync is available (was installed or already present).
        """
        result = await self.execute(
            "which rsync || apt-get install -y rsync",
            timeout=60,
        )
        return result.exit_code == 0

    async def ensure_sshfs(self) -> bool:
        """Ensure sshfs is installed on the VM.

        Returns:
            True if sshfs is available (was installed or already present).
        """
        result = await self.execute(
            "which sshfs || apt-get install -y sshfs",
            timeout=60,
        )
        return result.exit_code == 0

    async def mount_sshfs(
        self,
        local_path: str,
        remote_mount_path: str,
        ssh_port: int = 2222,
        use_overlay: bool = True,
        local_user: str | None = None,
        identity_file: str = "/root/.ssh/id_ed25519",
    ) -> bool:
        """Mount a local directory on the VM via SSHFS (requires reverse tunnel).

        This expects a reverse SSH tunnel to be set up from the VM back to
        the local machine. Use with `create_reverse_tunnel()`.

        Args:
            local_path: Path on local machine to mount.
            remote_mount_path: Where to mount on the VM.
            ssh_port: Port for reverse tunnel (default 2222).
            use_overlay: Use overlayfs for copy-on-write (default True).
            local_user: Username on local machine for SSH connection.
            identity_file: Path to SSH private key on the VM (default /root/.ssh/id_ed25519).

        Returns:
            True if mount succeeded.
        """
        # Create mount directories
        # Upper/work dirs must be on local filesystem for overlay to work
        if use_overlay:
            lower_dir = f"{remote_mount_path}-lower"
            upper_dir = f"/tmp/overlay{remote_mount_path}-upper"
            work_dir = f"/tmp/overlay{remote_mount_path}-work"
            setup_cmd = f"mkdir -p {lower_dir} {upper_dir} {work_dir} {remote_mount_path}"
        else:
            lower_dir = remote_mount_path
            setup_cmd = f"mkdir -p {remote_mount_path}"

        result = await self.execute(setup_cmd, timeout=30)
        if result.exit_code != 0:
            return False

        # Build SSHFS command
        # Note: uses 127.0.0.1 (not localhost) because of reverse tunnel and VM DNS issues
        user_prefix = f"{local_user}@" if local_user else ""
        sshfs_cmd = (
            f"sshfs -o ro,IdentityFile={identity_file},StrictHostKeyChecking=no,UserKnownHostsFile=/dev/null,reconnect,ServerAliveInterval=15 "
            f"-p {ssh_port} {user_prefix}127.0.0.1:{local_path} {lower_dir}"
        )
        result = await self.execute(sshfs_cmd, timeout=60)
        if result.exit_code != 0:
            return False

        # Set up fuse-overlayfs if requested (works with FUSE lower dirs)
        if use_overlay:
            await self.execute("which fuse-overlayfs || apt-get install -y fuse-overlayfs", timeout=60)
            overlay_cmd = (
                f"fuse-overlayfs -o lowerdir={lower_dir},upperdir={upper_dir},workdir={work_dir} {remote_mount_path}"
            )
            result = await self.execute(overlay_cmd, timeout=30)
            if result.exit_code != 0:
                return False

        return True

    async def ensure_nfs(self) -> bool:
        """Ensure NFS client is installed on the VM.

        Returns:
            True if nfs-common is available.
        """
        result = await self.execute(
            "which mount.nfs || apt-get install -y nfs-common",
            timeout=60,
        )
        return result.exit_code == 0

    async def mount_nfs(
        self,
        remote_mount_path: str,
        nfs_port: int = 2049,
        use_overlay: bool = True,
    ) -> bool:
        """Mount local NFS export on the VM via reverse tunnel.

        Expects a reverse tunnel forwarding nfs_port on VM to local NFS server.

        Args:
            remote_mount_path: Where to mount on the VM.
            nfs_port: Port for NFS (default 2049).
            use_overlay: Use overlayfs for copy-on-write (default True).

        Returns:
            True if mount succeeded.
        """
        # Create mount directories
        # Upper/work dirs must be on local filesystem for overlay to work
        if use_overlay:
            lower_dir = f"{remote_mount_path}-lower"
            upper_dir = f"/tmp/overlay{remote_mount_path}-upper"
            work_dir = f"/tmp/overlay{remote_mount_path}-work"
            setup_cmd = f"mkdir -p {lower_dir} {upper_dir} {work_dir} {remote_mount_path}"
        else:
            lower_dir = remote_mount_path
            setup_cmd = f"mkdir -p {remote_mount_path}"

        result = await self.execute(setup_cmd, timeout=30)
        if result.exit_code != 0:
            return False

        # Mount via NFS through the tunnel
        # 127.0.0.1 because reverse tunnel forwards to local NFS
        mount_cmd = f"mount -t nfs -o ro,port={nfs_port},mountport={nfs_port},tcp,vers=4,nolock 127.0.0.1:/ {lower_dir}"
        result = await self.execute(mount_cmd, timeout=60)
        if result.exit_code != 0:
            return False

        # Set up fuse-overlayfs if requested
        if use_overlay:
            await self.execute("which fuse-overlayfs || apt-get install -y fuse-overlayfs", timeout=60)
            overlay_cmd = (
                f"fuse-overlayfs -o lowerdir={lower_dir},upperdir={upper_dir},workdir={work_dir} {remote_mount_path}"
            )
            result = await self.execute(overlay_cmd, timeout=30)
            if result.exit_code != 0:
                return False

        return True

    async def unmount_nfs(self, remote_mount_path: str, use_overlay: bool = True) -> bool:
        """Unmount an NFS mount.

        Args:
            remote_mount_path: The mount path to unmount.
            use_overlay: Whether overlay was used.

        Returns:
            True if unmount succeeded.
        """
        if use_overlay:
            await self.execute(f"umount {remote_mount_path}", timeout=30)
            lower_dir = f"{remote_mount_path}-lower"
            result = await self.execute(f"umount {lower_dir}", timeout=30)
        else:
            result = await self.execute(f"umount {remote_mount_path}", timeout=30)

        return result.exit_code == 0

    async def unmount_sshfs(self, remote_mount_path: str, use_overlay: bool = True) -> bool:
        """Unmount an SSHFS mount.

        Args:
            remote_mount_path: The mount path to unmount.
            use_overlay: Whether overlay was used (unmounts both layers).

        Returns:
            True if unmount succeeded.
        """
        if use_overlay:
            # Unmount overlay first, then sshfs
            await self.execute(f"umount {remote_mount_path}", timeout=30)
            lower_dir = f"{remote_mount_path}-lower"
            result = await self.execute(f"fusermount -u {lower_dir}", timeout=30)
        else:
            result = await self.execute(f"fusermount -u {remote_mount_path}", timeout=30)

        return result.exit_code == 0

    def create_reverse_tunnel(
        self,
        private_key_path: str,
        local_port: int = 22,
        remote_port: int = 2222,
    ) -> ReverseTunnel:
        """Create a reverse tunnel for SSHFS mounts.

        The reverse tunnel allows the VM to connect back to your local machine,
        enabling SSHFS mounts of local directories.

        Args:
            private_key_path: Path to SSH private key.
            local_port: Local SSH port (default 22).
            remote_port: Port on VM that forwards to local (default 2222).

        Returns:
            ReverseTunnel instance (call .start() to activate).

        Example:
            tunnel = env.create_reverse_tunnel(key_path)
            tunnel.start()
            await env.mount_sshfs("/local/code", "/mnt/code", ssh_port=2222)
            # ... do work ...
            tunnel.stop()
        """
        return ReverseTunnel(
            job_id=self.job_id,
            private_key_path=private_key_path,
            local_port=local_port,
            remote_port=remote_port,
        )
