"""Docker image build for cube-agent.

Two paths:
- Local `docker buildx` (the only CLI dependency) — used when a Docker daemon
  is available.
- `remote_build_and_push` — a Docker-daemonless path that ships the build
  context to cube-cloud, which builds it with kaniko and pushes to ACR. Used on
  machines without Docker (locked-down laptops, on-cube code servers). See
  docs/remote-build-spec.md.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import shutil
import time
from pathlib import Path
from typing import Callable

import httpx

from cube_common.build_context import BuildContextError, build_context_tarball

logger = logging.getLogger(__name__)


class DockerBuildError(Exception):
    """Raised when a Docker build fails."""


def docker_available() -> bool:
    """Check if docker CLI is available.

    Honors CUBE_AGENT_DISABLE_DOCKER: set it (to any non-empty value) to force
    the "no local Docker" behavior without uninstalling Docker — under
    build_mode=auto the pipeline then builds remotely, and under
    build_mode=local it raises the Docker-not-found error. Useful for testing
    the cloud-build fallback on a machine that does have Docker.
    """
    if os.environ.get("CUBE_AGENT_DISABLE_DOCKER"):
        return False
    return shutil.which("docker") is not None


async def docker_login(registry: str, token: str) -> None:
    """Login to a Docker registry using a token."""
    proc = await asyncio.create_subprocess_exec(
        "docker", "login", registry,
        "--username", "apollo",
        "--password-stdin",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    _, stderr = await proc.communicate(token.encode())
    if proc.returncode != 0:
        raise DockerBuildError(f"Docker login failed: {stderr.decode().strip()}")


async def build_and_push(
    context_dir: str,
    tag: str,
    platforms: str = "linux/amd64",
    build_args: dict[str, str] | None = None,
    dockerfile: str | None = None,
    target: str | None = None,
) -> str:
    """Build and push a Docker image using buildx.

    Args:
        context_dir: Build context directory (where Dockerfile lives).
        tag: Full image tag (e.g. "registry/repo:version").
        platforms: Comma-separated target platforms.
        build_args: Build-time variables passed as `--build-arg key=value`.
        dockerfile: Path to the Dockerfile, if not the default in context_dir.
        target: Build stage to target in a multi-stage Dockerfile.

    Returns:
        Status message.
    """
    if not docker_available():
        raise DockerBuildError("Docker not found. Install Docker to build images.")

    cmd = [
        "docker", "buildx", "build",
        "--platform", platforms,
        "--tag", tag,
        "--output", "type=image,push=true",
    ]

    for key, value in (build_args or {}).items():
        if "=" in key:
            raise DockerBuildError(f"Invalid build-arg name '{key}': must not contain '='")
        cmd += ["--build-arg", f"{key}={value}"]

    if dockerfile:
        cmd += ["--file", dockerfile]

    if target:
        cmd += ["--target", target]

    cmd.append(context_dir)

    logger.info("Building Docker image: %s", tag)

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=600)

    if proc.returncode != 0:
        raise DockerBuildError(f"Docker build failed: {stderr.decode().strip()}")

    return f"Image pushed: {tag}"


async def remote_build_and_push(
    cloud,
    context_dir: str,
    image_name: str,
    tag: str,
    dockerfile_rel: str = "Dockerfile",
    target: str | None = None,
    build_args: dict[str, str] | None = None,
    platform: str = "linux/amd64",
    poll_interval: float = 5.0,
    timeout: float = 900.0,
    show_build_log: bool = False,
    log: Callable[[str], None] | None = None,
) -> str:
    """Build + push an image server-side (no local Docker), returning the image URI.

    Tars the context, PUTs it to a presigned S3 URL from ``build_image_prepare``,
    starts the kaniko build, and polls ``build_image_status`` to completion.

    Args:
        cloud: A connected ``CloudClient`` (provides ``call_tool``).
        context_dir: Build context directory (contains the Dockerfile).
        image_name: Bare image name (no registry/tag).
        tag: Image tag.
        dockerfile_rel: Dockerfile path relative to the context root.
        target / build_args / platform: passed through to the builder.
        show_build_log: when True, surface the kaniko build-log tail on success
            (it's always surfaced on failure) so the build output is visible
            inline without needing CloudWatch access. Defaults to False to avoid
            dumping build output into the caller's context on every success.
        log: optional progress callback.
    """
    emit = log or (lambda _m: None)

    tgz_path = build_context_tarball(context_dir)
    try:
        prep = json.loads(await cloud.call_tool(
            "build_image_prepare", {"image_name": image_name, "tag": tag}
        ))
        if "error" in prep:
            raise DockerBuildError(f"prepare failed: {prep['error']}")
        job_id = prep["job_id"]
        upload_url = prep["upload_url"]

        emit("uploading build context")
        data = Path(tgz_path).read_bytes()
        async with httpx.AsyncClient(timeout=300, follow_redirects=True) as http:
            put = await http.put(upload_url, content=data)
        if put.status_code not in (200, 201):
            raise DockerBuildError(
                f"context upload failed ({put.status_code}): {put.text[:300]}"
            )

        start_args: dict = {"job_id": job_id, "dockerfile": dockerfile_rel, "platform": platform}
        if target:
            start_args["target"] = target
        if build_args:
            start_args["build_args"] = build_args
        started = json.loads(await cloud.call_tool("build_image_start", start_args))
        if "error" in started:
            raise DockerBuildError(f"start failed: {started['error']}")
        emit("remote build started")

        deadline = time.monotonic() + timeout
        last_state: str | None = None
        while True:
            status = json.loads(await cloud.call_tool("build_image_status", {"job_id": job_id}))
            if "error" in status:
                raise DockerBuildError(f"status failed: {status['error']}")
            state = status.get("state", "UNKNOWN")
            if state != last_state:
                emit(f"build {state.lower()}")
                last_state = state
            if state == "SUCCEEDED":
                if show_build_log:
                    tail = status.get("logs_tail") or ""
                    if tail:
                        emit("build log (tail):")
                        for line in tail.splitlines():
                            emit(f"  {line}")
                return status.get("image_uri", f"{image_name}:{tag}")
            if state == "FAILED":
                tail = (status.get("logs_tail") or "")[-2000:]
                reason = status.get("stopped_reason") or ""
                raise DockerBuildError(
                    f"remote build failed (exit {status.get('exit_code', '?')}) {reason}\n{tail}"
                )
            if time.monotonic() > deadline:
                raise DockerBuildError(f"remote build timed out after {int(timeout)}s")
            await asyncio.sleep(poll_interval)
    except BuildContextError as e:
        raise DockerBuildError(str(e))
    finally:
        try:
            os.remove(tgz_path)
        except OSError:
            pass
