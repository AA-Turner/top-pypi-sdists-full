"""Simple HTTP server for provisioning Apple ``container`` runtimes."""

from __future__ import annotations

import argparse
import asyncio
import logging
import shlex
from contextlib import suppress

from aiohttp import web
from pydantic import BaseModel, Field

from plato.runtimes.base import AppleContainerMetadata, RuntimeInfo

logger = logging.getLogger(__name__)


class StartAppleContainerRequest(BaseModel):
    """Request payload for provisioning a container."""

    image: str
    cpus: int = Field(default=4, ge=1)
    memory: str = "4G"
    alias: str | None = None
    public_key: str | None = None
    timeout: int = Field(default=30, ge=1)


class ExecAppleContainerRequest(BaseModel):
    """Request payload for executing a command in a container."""

    command: str
    timeout: int = Field(default=300, ge=1)
    stream: bool = False


class ExecAppleContainerResponse(BaseModel):
    """Command execution response."""

    exit_code: int
    stdout: str = ""
    stderr: str = ""


class AppleContainerService:
    """Host-side controller for Apple ``container`` runtimes."""

    def __init__(self) -> None:
        self._container_ids: dict[str, str] = {}
        self._hostnames: dict[str, str] = {}

    async def start(self, req: StartAppleContainerRequest) -> RuntimeInfo:
        """Start a container and optionally configure SSH access."""
        logger.info(
            "apple server start requested: image=%s alias=%s cpus=%s memory=%s ssh=%s",
            req.image,
            req.alias,
            req.cpus,
            req.memory,
            bool(req.public_key),
        )
        stdout = await _container(
            "run",
            "-d",
            "--cpus",
            str(req.cpus),
            "--memory",
            req.memory,
            req.image,
            "sleep",
            "infinity",
        )
        container_id = stdout.strip()
        if not container_id:
            raise RuntimeError("container run returned empty ID")

        runtime_id = req.alias or container_id
        self._container_ids[runtime_id] = container_id
        hostname = container_id

        try:
            if req.public_key:
                await self._configure_ssh(container_id, req.public_key, timeout=req.timeout)
                hostname = await self._resolve_ip(container_id)
                self._hostnames[runtime_id] = hostname

            logger.info(
                "apple server start complete: runtime_id=%s container_id=%s hostname=%s",
                runtime_id,
                container_id,
                hostname,
            )
            return RuntimeInfo(
                runtime_id=runtime_id,
                hostname=hostname,
                metadata=AppleContainerMetadata(
                    container_id=container_id,
                    image=req.image,
                    alias=runtime_id,
                ),
            )
        except Exception:
            await self.stop(runtime_id)
            raise

    async def exec(self, runtime_id: str, req: ExecAppleContainerRequest) -> ExecAppleContainerResponse:
        """Execute a command in a managed container."""
        container_id = self._container_ids.get(runtime_id, runtime_id)
        logger.info(
            "apple server exec requested: runtime_id=%s container_id=%s timeout=%ss stream=%s command=%r",
            runtime_id,
            container_id,
            req.timeout,
            req.stream,
            req.command,
        )
        exit_code, stdout, stderr = await _container_exec(
            container_id,
            req.command,
            timeout=req.timeout,
            stream=req.stream,
        )
        logger.info(
            "apple server exec complete: runtime_id=%s exit_code=%s stdout_len=%s stderr_len=%s",
            runtime_id,
            exit_code,
            len(stdout),
            len(stderr),
        )
        return ExecAppleContainerResponse(
            exit_code=exit_code,
            stdout=stdout,
            stderr=stderr,
        )

    async def stop(self, runtime_id: str) -> None:
        """Stop and delete a managed container."""
        container_id = self._container_ids.pop(runtime_id, runtime_id)
        self._hostnames.pop(runtime_id, None)
        logger.info("apple server stop requested: runtime_id=%s container_id=%s", runtime_id, container_id)
        with suppress(Exception):
            await _container("kill", container_id)

        for attempt in range(5):
            try:
                await _container("delete", container_id)
                break
            except Exception:
                if attempt == 4:
                    logger.debug("Failed to delete apple container %s", container_id, exc_info=True)
                    break
                await asyncio.sleep(0.5)
        logger.info("apple server stop complete: runtime_id=%s container_id=%s", runtime_id, container_id)

    async def _configure_ssh(self, container_id: str, public_key: str, *, timeout: int) -> None:
        quoted_key = shlex.quote(public_key.strip())
        _, _, stderr = await _container_exec(
            container_id,
            (
                "mkdir -p /root/.ssh && chmod 700 /root/.ssh "
                f"&& printf '%s\\n' {quoted_key} > /root/.ssh/authorized_keys "
                "&& chmod 600 /root/.ssh/authorized_keys "
                "&& /usr/sbin/sshd"
            ),
            timeout=timeout,
        )
        await self._wait_for_ssh(container_id, timeout=timeout)
        if stderr:
            logger.debug("apple ssh setup stderr for %s: %s", container_id, stderr)

    async def _resolve_ip(self, container_id: str) -> str:
        exit_code, stdout, stderr = await _container_exec(
            container_id,
            "hostname -I | awk '{print $1}'",
            timeout=10,
        )
        if exit_code != 0:
            raise RuntimeError(f"Failed to resolve IP for container {container_id}: {stderr.strip()}")
        hostname = stdout.strip()
        if not hostname:
            raise RuntimeError(f"Failed to resolve IP for container {container_id}: empty output")
        return hostname

    async def _wait_for_ssh(self, container_id: str, *, timeout: int) -> None:
        deadline = asyncio.get_running_loop().time() + timeout
        probe = (
            "ss -ltn 2>/dev/null | grep -q ':22 ' "
            "|| netstat -ltn 2>/dev/null | grep -q ':22 ' "
            "|| pgrep -x sshd >/dev/null"
        )
        while True:
            exit_code, _, _ = await _container_exec(
                container_id,
                probe,
                timeout=5,
            )
            if exit_code == 0:
                return
            if asyncio.get_running_loop().time() >= deadline:
                raise RuntimeError(f"SSH not ready on container {container_id}")
            await asyncio.sleep(0.5)


APPLE_CONTAINER_SERVICE_KEY = web.AppKey("apple_container_service", AppleContainerService)


async def healthz(_: web.Request) -> web.Response:
    """Health check endpoint."""
    logger.debug("apple server healthz")
    return web.json_response({"status": "ok"})


async def start_container(request: web.Request) -> web.Response:
    """Provision a new Apple container."""
    service = request.app[APPLE_CONTAINER_SERVICE_KEY]
    payload = StartAppleContainerRequest.model_validate(await request.json())
    logger.debug("http POST /runtimes/start payload=%s", payload.model_dump(exclude={"public_key"}))
    info = await service.start(payload)
    return web.json_response(info.model_dump(mode="json"))


async def exec_container(request: web.Request) -> web.Response:
    """Execute a command in an Apple container."""
    service = request.app[APPLE_CONTAINER_SERVICE_KEY]
    payload = ExecAppleContainerRequest.model_validate(await request.json())
    runtime_id = request.match_info["runtime_id"]
    logger.debug(
        "http POST /runtimes/%s/exec payload=%s",
        runtime_id,
        payload.model_dump(),
    )
    result = await service.exec(runtime_id, payload)
    return web.json_response(result.model_dump())


async def stop_container(request: web.Request) -> web.Response:
    """Stop and delete an Apple container."""
    service = request.app[APPLE_CONTAINER_SERVICE_KEY]
    runtime_id = request.match_info["runtime_id"]
    logger.debug("http DELETE /runtimes/%s", runtime_id)
    await service.stop(runtime_id)
    return web.json_response({"status": "stopped", "runtime_id": runtime_id})


def create_app(service: AppleContainerService | None = None) -> web.Application:
    """Build the aiohttp application."""
    app = web.Application()
    app[APPLE_CONTAINER_SERVICE_KEY] = service or AppleContainerService()
    app.router.add_get("/healthz", healthz)
    app.router.add_post("/runtimes/start", start_container)
    app.router.add_post("/runtimes/{runtime_id}/exec", exec_container)
    app.router.add_delete("/runtimes/{runtime_id}", stop_container)
    return app


def main() -> None:
    """Run the Apple container service."""
    parser = argparse.ArgumentParser(description="Serve Apple container runtime operations over HTTP")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8766)
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    web.run_app(create_app(), host=args.host, port=args.port)


async def _container(*args: str) -> str:
    """Run a ``container`` CLI command and return stdout."""
    logger.debug("container cli: %s", " ".join(args))
    proc = await asyncio.create_subprocess_exec(
        "container",
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"container {' '.join(args)} failed (rc={proc.returncode}): {stderr.decode().strip()}")
    return stdout.decode().strip()


async def _container_exec(
    container_id: str,
    command: str,
    *,
    timeout: int = 300,
    stream: bool = False,
) -> tuple[int, str, str]:
    """Execute a command inside a container via ``container exec``."""
    args = ["exec", container_id, "sh", "-c", command]
    logger.debug(
        "container exec: container_id=%s timeout=%ss stream=%s command=%r", container_id, timeout, stream, command
    )

    if stream:
        proc = await asyncio.create_subprocess_exec(
            "container",
            *args,
            stdout=None,
            stderr=None,
        )
        await asyncio.wait_for(proc.wait(), timeout=timeout)
        return proc.returncode or 0, "", ""

    proc = await asyncio.create_subprocess_exec(
        "container",
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
    return (
        proc.returncode or 0,
        stdout.decode(errors="replace"),
        stderr.decode(errors="replace"),
    )
