"""Plato VM runtime — runs commands on Firecracker micro-VMs via Plato sessions."""

from __future__ import annotations

import asyncio
import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING

import tenacity

from plato.runtimes.base import Runtime, RuntimeInfo, VMMetadata
from plato.runtimes.settings import get_settings
from plato.utils.subprocess import VM_PATH_EXPORT, run_ssh, run_ssh_streaming
from plato.v2 import Env
from plato.v2.types import SimConfigCompute

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from plato.v2.async_.environment import Environment
    from plato.v2.async_.session import Session


def _use_mesh_ssh() -> bool:
    """Return True if SSH should use mesh IP directly instead of gateway proxy.

    Determined by ``PLATO_SSH_MODE``: 'mesh' always, 'gateway' never,
    'auto' (default) uses mesh when running on a Plato VM (JOB_ID set).
    """
    mode = get_settings().ssh_mode
    if mode == "mesh":
        return True
    if mode == "gateway":
        return False
    # auto: use mesh if we're on a Plato VM
    return bool(os.environ.get("JOB_ID"))


def _gateway_ssh_opts(job_id: str) -> list[tuple[str, str]]:
    """Build SSH ProxyCommand options to reach a VM through the Plato gateway."""
    gateway_host = get_settings().gateway_host
    sni = f"{job_id}--22.{gateway_host}"
    proxy_cmd = f"openssl s_client -quiet -connect {gateway_host}:443 -servername {sni} 2>/dev/null"
    return [("ProxyCommand", proxy_cmd)]


def _is_duplicate_alias_error(exc: BaseException) -> bool:
    return "Duplicate alias" in str(exc)


def _is_retryable_start_error(exc: BaseException) -> bool:
    return not _is_duplicate_alias_error(exc) and not isinstance(exc, asyncio.CancelledError)


def _with_vm_path(command: str) -> str:
    return f"{VM_PATH_EXPORT}; {command}"


class VMRuntime(Runtime):
    """Runtime backed by Plato-managed Firecracker VMs.

    Uses a Plato session to provision VMs and SSH for command execution.

    When running on a Plato VM (``JOB_ID`` env var set), SSH goes directly
    to the mesh IP over the WireGuard network. When running locally, SSH
    goes through the Plato gateway proxy.

    Args:
        image: Docker image URL for the VM rootfs.
        session: Plato session for VM lifecycle management.
        ssh_key_path: Path to the SSH private key for VM access.
        cpus: Number of CPUs for the VM.
        memory: Memory in MB.
        disk: Disk in MB.
        timeout: VM job timeout in seconds (how long the VM stays alive).
        heartbeat_timeout: Per-VM heartbeat timeout in seconds.
            None = use server default (300s), 0 = disabled.
    """

    def __init__(
        self,
        image: str,
        *,
        session: Session,
        ssh_key_path: Path | None = None,
        cpus: int = 2,
        memory: int = 4096,
        disk: int = 10240,
        timeout: int = 7200,
        heartbeat_timeout: int | None = None,
    ) -> None:
        super().__init__(image)
        self._session = session
        self._ssh_key_path = ssh_key_path
        self._cpus = cpus
        self._memory = memory
        self._disk = disk
        self._timeout = timeout
        self._heartbeat_timeout = heartbeat_timeout
        self._envs: dict[str, Environment] = {}

    def _ssh_target(self, env: Environment) -> tuple[str, list[tuple[str, str]]]:
        """Return (hostname, extra_ssh_opts) for reaching the given env.

        On a Plato VM: uses the mesh IP directly (no proxy).
        Locally: uses the gateway proxy with the job ID.
        """
        extra_opts: list[tuple[str, str]] = [
            ("ServerAliveInterval", "30"),
            ("ServerAliveCountMax", "3"),
        ]

        if _use_mesh_ssh():
            mesh_ip = env.mesh_ip
            if mesh_ip is None:
                raise RuntimeError(f"Mesh SSH requested but env {env.alias or env.job_id} has no mesh IP")
            return mesh_ip, extra_opts

        # Local machine — route through gateway
        job_id = env.job_id
        extra_opts.extend(_gateway_ssh_opts(job_id))
        return job_id, extra_opts

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_exponential(multiplier=10, min=10, max=60),
        before_sleep=tenacity.before_sleep_log(logger, logging.WARNING),
        retry=tenacity.retry_if_exception(_is_retryable_start_error),
        reraise=True,
    )
    async def start(self, *, timeout: int = 300, alias: str | None = None) -> RuntimeInfo:
        """Provision and start a VM.

        Args:
            timeout: Maximum seconds to wait for the VM to be ready.
            alias: Custom alias for the VM. If None, an auto-generated alias is used.
        """
        alias = alias or f"vm-{id(self):x}"

        # Reuse an already-provisioned env on retry.  When start() retries
        # after connect_network or SSH fails, the env from the prior attempt
        # is still live on the backend — calling add_env again with the same
        # alias would raise "Duplicate alias".
        env = self._envs.get(alias)
        if env is None:
            env = await self._session.add_env(
                Env.resource(
                    simulator=alias,
                    sim_config=SimConfigCompute(
                        cpus=self._cpus,
                        memory=self._memory,
                        disk=self._disk,
                    ),
                    alias=alias,
                    docker_image_url=self.image,
                    upload_rootfs=False,
                    rootfs_storage_backend="snapshot-store",
                ),
                timeout=self._timeout,
                heartbeat_timeout=self._heartbeat_timeout,
            )
            self._envs[alias] = env

        await self._session.connect_network()

        # Add SSH public key to the VM.
        if self._ssh_key_path:
            pub_key = Path(str(self._ssh_key_path) + ".pub").read_text().strip()
            await env.add_ssh_key(pub_key)
        hostname, extra_opts = self._ssh_target(env)
        if self._ssh_key_path is not None:
            await self._wait_for_ssh(hostname, extra_opts=extra_opts, timeout=min(timeout, 60))
        logger.debug("VM runtime started: alias=%s job_id=%s hostname=%s", alias, env.job_id, hostname)

        return RuntimeInfo(
            runtime_id=alias,
            hostname=hostname,
            ssh_key_path=self._ssh_key_path,
            metadata=VMMetadata(
                job_id=env.job_id,
                alias=alias,
                hostname=env.mesh_ip or "",
            ),
            env=env,
        )

    @property
    def session(self) -> Session:
        """The Plato session used for VM lifecycle."""
        return self._session

    @property
    def ssh_key_path(self) -> Path | None:
        """SSH private key path."""
        return self._ssh_key_path

    def get_env(self, runtime_id: str) -> Environment:
        """Get the Environment object for a running VM."""
        env = self._envs.get(runtime_id)
        if env is None:
            raise RuntimeError(f"Unknown runtime_id: {runtime_id}")
        return env

    async def stop(self, runtime_id: str) -> None:
        env = self._envs.pop(runtime_id, None)
        if env is None:
            logger.warning("VM runtime stop: unknown runtime_id %s", runtime_id)
            return
        try:
            await self._session.remove_env(env)
            logger.debug("VM runtime stopped: %s", runtime_id)
        except Exception as e:
            logger.warning("Failed to stop VM %s: %s", runtime_id, e)

    async def exec(
        self,
        runtime_id: str,
        command: str,
        *,
        timeout: int = 300,
        stream: bool = False,
    ) -> tuple[int, str, str]:
        env = self._envs.get(runtime_id)
        if env is None:
            raise RuntimeError(f"Unknown runtime_id: {runtime_id}")
        if self._ssh_key_path is None:
            raise RuntimeError("ssh_key_path required for VM exec")

        hostname, extra_opts = self._ssh_target(env)
        remote_command = _with_vm_path(command)

        if stream:
            exit_code = await run_ssh_streaming(
                self._ssh_key_path,
                hostname,
                remote_command,
                user="root",
                extra_opts=extra_opts,
            )
            return exit_code, "", ""

        exit_code, stdout, stderr = await run_ssh(
            self._ssh_key_path,
            hostname,
            remote_command,
            user="root",
            timeout=timeout,
            extra_opts=extra_opts,
        )
        return exit_code, stdout, stderr

    async def _wait_for_ssh(
        self,
        hostname: str,
        *,
        extra_opts: list[tuple[str, str]],
        timeout: int,
    ) -> None:
        """Wait for SSH to accept commands on a newly provisioned VM."""
        if self._ssh_key_path is None:
            raise RuntimeError("ssh_key_path required for VM startup readiness")

        deadline = asyncio.get_running_loop().time() + timeout
        last_stderr = ""
        while True:
            exit_code, _, stderr = await run_ssh(
                self._ssh_key_path,
                hostname,
                "echo ready",
                user="root",
                timeout=10,
                extra_opts=extra_opts,
            )
            if exit_code == 0:
                return
            last_stderr = stderr.strip()
            if asyncio.get_running_loop().time() >= deadline:
                raise RuntimeError(f"SSH not ready for VM {hostname}: {last_stderr}")
            await asyncio.sleep(2)
