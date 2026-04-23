"""Apple runtime client backed by the host-side Apple container server."""

from __future__ import annotations

import logging
from pathlib import Path

import httpx

from plato.runtimes.base import Runtime, RuntimeInfo
from plato.utils.subprocess import run_ssh, run_ssh_streaming

logger = logging.getLogger(__name__)

_SSH_EXTRA_OPTS: list[tuple[str, str]] = [
    ("ServerAliveInterval", "30"),
    ("ServerAliveCountMax", "3"),
]


class AppleRuntime(Runtime):
    """Runtime backed by the host-side Apple container server.

    Args:
        image: OCI image name (e.g. ``"plato-world-test:latest"``).
        cpus: Number of CPUs to allocate.
        memory: Memory string with optional suffix (e.g. ``"4G"``).
        ssh_key_path: Path to SSH private key. The public key is sent to the
            server so the container is reachable over SSH.
        server_url: Base URL for ``plato-apple-container-server``.
    """

    def __init__(
        self,
        image: str,
        *,
        cpus: int = 4,
        memory: str = "4G",
        ssh_key_path: Path,
        server_url: str,
    ) -> None:
        super().__init__(image)
        self._cpus = cpus
        self._memory = memory
        self._ssh_key_path = ssh_key_path
        self._server_url = server_url.rstrip("/")
        self._hostnames: dict[str, str] = {}

    async def start(self, *, timeout: int = 300, alias: str | None = None) -> RuntimeInfo:
        logger.debug(
            "apple runtime start requested: image=%s alias=%s server=%s ssh_key=%s",
            self.image,
            alias,
            self._server_url,
            self._ssh_key_path,
        )
        return await self._start_via_server(timeout=timeout, alias=alias)

    async def stop(self, runtime_id: str) -> None:
        logger.debug("apple runtime stop requested: runtime_id=%s server=%s", runtime_id, self._server_url)
        await self._stop_via_server(runtime_id)

    async def exec(
        self,
        runtime_id: str,
        command: str,
        *,
        timeout: int = 300,
        stream: bool = False,
    ) -> tuple[int, str, str]:
        hostname = self._hostnames.get(runtime_id)
        if hostname is None:
            raise RuntimeError(f"Unknown Apple runtime_id: {runtime_id}")

        logger.debug(
            "apple runtime exec requested: runtime_id=%s hostname=%s timeout=%ss stream=%s command=%r",
            runtime_id,
            hostname,
            timeout,
            stream,
            command,
        )
        if stream:
            exit_code = await run_ssh_streaming(
                self._ssh_key_path,
                hostname,
                command,
                user="root",
                extra_opts=_SSH_EXTRA_OPTS,
            )
            return exit_code, "", ""

        return await run_ssh(
            self._ssh_key_path,
            hostname,
            command,
            user="root",
            timeout=timeout,
            extra_opts=_SSH_EXTRA_OPTS,
        )

    @property
    def ssh_key_path(self) -> Path | None:
        return self._ssh_key_path

    async def _start_via_server(self, *, timeout: int, alias: str | None) -> RuntimeInfo:
        public_key = Path(str(self._ssh_key_path) + ".pub").read_text().strip()

        async with httpx.AsyncClient(timeout=timeout) as client:
            logger.debug("apple runtime POST %s/runtimes/start", self._server_url)
            response = await client.post(
                f"{self._server_url}/runtimes/start",
                json={
                    "image": self.image,
                    "cpus": self._cpus,
                    "memory": self._memory,
                    "alias": alias,
                    "public_key": public_key,
                    "timeout": timeout,
                },
            )
            response.raise_for_status()

        info = RuntimeInfo.model_validate(response.json()).model_copy(update={"ssh_key_path": self._ssh_key_path})
        logger.debug("apple runtime start response: runtime_id=%s hostname=%s", info.runtime_id, info.hostname)
        logger.debug("apple runtime probing ssh readiness: runtime_id=%s hostname=%s", info.runtime_id, info.hostname)
        ssh_code, _, ssh_stderr = await run_ssh(
            self._ssh_key_path,
            info.hostname,
            "echo ready",
            user="root",
            timeout=min(timeout, 15),
            extra_opts=_SSH_EXTRA_OPTS,
        )
        if ssh_code != 0:
            raise RuntimeError(f"SSH not ready for apple runtime {info.runtime_id}: {ssh_stderr.strip()}")
        self._hostnames[info.runtime_id] = info.hostname
        logger.debug("Apple runtime started via server: runtime_id=%s hostname=%s", info.runtime_id, info.hostname)
        return info

    async def _stop_via_server(self, runtime_id: str) -> None:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.delete(f"{self._server_url}/runtimes/{runtime_id}")
            response.raise_for_status()
        self._hostnames.pop(runtime_id, None)
        logger.debug("Apple runtime stopped via server: runtime_id=%s", runtime_id)
