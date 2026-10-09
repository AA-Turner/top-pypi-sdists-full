"""``plato gpu``: renders and pods from a laptop, with the environment's keys.

    export RUNPOD_API_KEY=... PLATO_GPU_BUCKET=gpu-box-runpod-<account> AWS_PROFILE=...
    plato gpu pod up mindustry-desktop --option PLATO_MCP_MODE=campaign
    plato gpu pod status <pod id>
    plato gpu pod list
    plato gpu pod down <pod id>          # terminates: billing stops
    plato gpu render scene.blend --frames 1..4 --out frames/
    plato gpu form <artifact-id>                                   # the artifact's GPU form, if any
    plato gpu form <artifact-id> --image <account>.dkr.ecr.<region>.amazonaws.com/plato-sims/mindustry:160.5 --command /usr/local/bin/entrypoint \
        --option PLATO_MCP_MODE --env PLATO_MCP_MODE=campaign    # record one (app admin)
    plato gpu form <artifact-id> --image <ecr image> --push --from mindustry-sim:dev ...   # push the local image there first

Pods are owned by ``--owner`` (default: ``dev-<user>``), the same way a
world owns the pods it creates, so ``list`` and ``down`` only ever see yours.
"""

from __future__ import annotations

import asyncio
import getpass
import io
import json
import os
import re
import tarfile
from pathlib import Path

import httpx
import typer
from pydantic import BaseModel, JsonValue
from rich.console import Console

from plato.gpu.client import GpuClient, GpuUnavailable
from plato.gpu.pods import PodView
from plato.gpu.profiles import PodImage
from plato.gpu.providers.base import GpuProviderError
from plato.gpu.registry import push_to_ecr
from plato.gpu.render import RenderFailed
from plato.gpu.settings import GpuSettings
from plato.gpu.storage import StorageError

# Not plato.cli.utils: plato.cli imports this module, so that would be a cycle.
console = Console()

gpu_app = typer.Typer(help="GPU renders and pods, with the environment's provider key", no_args_is_help=True)
pod_app = typer.Typer(help="Whole GPU machines from named profiles", no_args_is_help=True)
gpu_app.add_typer(pod_app, name="pod")

_OWNER = re.compile(r"[^a-z0-9-]+")


def _default_owner() -> str:
    return "dev-" + (_OWNER.sub("-", getpass.getuser().lower()).strip("-") or "user")


OwnerOption = typer.Option(None, "--owner", help="Whose pods these are (default dev-<user>)")


def _client(owner: str | None) -> GpuClient:
    return GpuClient(GpuSettings.from_env(), owner=owner or _default_owner())


def _run(coro):  # noqa: ANN001, ANN202 - typer command plumbing
    try:
        return asyncio.run(coro)
    except (GpuUnavailable, GpuProviderError, StorageError, RenderFailed) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error


def _print_view(view: PodView) -> None:
    cost = f" at ${view.cost_per_hour:.2f}/h" if view.cost_per_hour is not None else ""
    console.print(f"{view.id} ({view.slug or '?'}): {view.status.value}{cost}")
    console.print(f"  mcp: {view.mcp_url}")
    console.print(f"  desktop: {view.desktop_url}")
    if view.recording_url:
        console.print(f"  recording: {view.recording_url}")


@pod_app.command("up")
def pod_up(
    profile: str = typer.Argument(..., help="A pod profile name (plato.gpu.profiles.PROFILES)"),
    option: list[str] = typer.Option([], "--option", help="ENV=value the profile allows"),
    wait: bool = typer.Option(True, help="Wait until the pod's MCP server answers"),
    owner: str | None = OwnerOption,
) -> None:
    """Create a pod; prints its URLs and, once, its secrets."""

    options: dict[str, str] = {}
    for entry in option:
        name, separator, value = entry.partition("=")
        if not separator:
            raise typer.BadParameter(f"--option takes ENV=value, not {entry!r}")
        options[name] = value

    async def go() -> None:
        client = _client(owner)
        session = await client.create_pod(profile, options)
        _print_view(session)
        console.print(f"  mcp bearer: {session.mcp_token}")
        console.print(f"  admin bearer: {session.admin_token}")
        console.print(f"  VNC password: {session.vnc_password}")
        console.print("[dim]billing until `plato gpu pod down` or the idle timeout[/dim]")
        if wait:
            console.print("waiting for the pod's MCP server...")
            _print_view(await client.wait_pod_ready(session.id))

    _run(go())


@pod_app.command("status")
def pod_status(pod_id: str, owner: str | None = OwnerOption) -> None:
    _run(_status(pod_id, owner))


async def _status(pod_id: str, owner: str | None) -> None:
    _print_view(await _client(owner).pod_status(pod_id))


@pod_app.command("down")
def pod_down(pod_id: str, owner: str | None = OwnerOption) -> None:
    """Terminate a pod; billing stops and its recording is uploaded."""

    _run(_down(pod_id, owner))


async def _down(pod_id: str, owner: str | None) -> None:
    view = await _client(owner).terminate_pod(pod_id)
    console.print(f"terminated {pod_id}")
    if view.recording_url:
        console.print(f"  recording: {view.recording_url}")


@pod_app.command("list")
def pod_list(owner: str | None = OwnerOption) -> None:
    """The owner's running pods."""

    _run(_list(owner))


async def _list(owner: str | None) -> None:
    views = await _client(owner).pods()
    if not views:
        console.print("no pods running")
    for view in views:
        _print_view(view)


@gpu_app.command("render")
def render(
    blend: Path = typer.Argument(..., exists=True, dir_okay=False, help="The .blend to render as saved"),
    frames: str = typer.Option("all", help='Blender frame selection: "1", "1..8", "1,3,5", or all'),
    out: Path = typer.Option(Path("frames"), help="Directory the frames are unpacked into"),
    owner: str | None = OwnerOption,
) -> None:
    """Render a .blend on a serverless GPU and unpack the frames."""

    async def say(line: str) -> None:
        console.print(f"[dim]{line}[/dim]")

    async def go() -> None:
        outcome = await _client(owner).render(blend.read_bytes(), frames=frames, on_status=say)
        out.mkdir(parents=True, exist_ok=True)
        with tarfile.open(fileobj=io.BytesIO(outcome.archive)) as tar:
            tar.extractall(out, filter="data")
        console.print(f"{outcome.summary}; frames in {out}")

    _run(go())


class _ArtifactView(BaseModel):
    """The two fields of ``GET /api/v2/artifacts/{id}`` the form command reads."""

    artifact_id: str
    additional_metadata: dict[str, JsonValue] | None = None


def _app() -> httpx.Client:
    api_key = os.environ.get("PLATO_API_KEY", "")
    if not api_key:
        console.print("[red]PLATO_API_KEY is not set[/red]")
        raise typer.Exit(1)
    base_url = os.environ.get("PLATO_BASE_URL", "https://plato.so").removesuffix("/api").rstrip("/")
    return httpx.Client(base_url=base_url, timeout=60, headers={"X-API-Key": api_key})


def _kv(entries: list[str], flag: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for entry in entries:
        name, separator, value = entry.partition("=")
        if not separator:
            raise typer.BadParameter(f"{flag} takes NAME=value, not {entry!r}")
        out[name] = value
    return out


@gpu_app.command("form")
def form(
    artifact_id: str = typer.Argument(..., help="The simulator artifact (its VM form)"),
    image: str | None = typer.Option(None, help="A Docker image of the same simulator (ECR, private): its GPU form"),
    push: bool = typer.Option(
        False,
        "--push",
        help="docker push the image to ECR first with your AWS login; creates the repository if missing",
    ),
    source: str | None = typer.Option(None, "--from", help="With --push: the local image to tag and push as --image"),
    command: list[str] = typer.Option([], help="The image's start command (repeat per argument)"),
    gpu: list[str] = typer.Option([], help="GPU type ids the pod may run on (default RTX 4090)"),
    disk_gb: int | None = typer.Option(None, help="Container disk in GB (default 20)"),
    mcp_port: int | None = typer.Option(None, help="Port the image serves MCP on (default 8765)"),
    desktop_port: int | None = typer.Option(None, help="Port the image serves noVNC on (default 6080)"),
    env: list[str] = typer.Option([], help="NAME=value the image's command expects"),
    option: list[str] = typer.Option([], help="Environment NAME a task may set beyond --env"),
    clear: bool = typer.Option(False, help="Remove the GPU form"),
) -> None:
    """Show or record an artifact's GPU form: the image a pod boots for it
    in a world granted pods. Recording needs app admin; --push also needs an
    AWS login that may write the ECR repository."""

    if push and image is None:
        raise typer.BadParameter("--push needs --image")
    if image is not None and not command:
        raise typer.BadParameter("--command is required with --image")
    with _app() as app:
        response = app.get(f"/api/v2/artifacts/{artifact_id}")
        if response.status_code != 200:
            console.print(f"[red]{response.status_code}: {response.text}[/red]")
            raise typer.Exit(1)
        artifact = _ArtifactView.model_validate_json(response.content)
        metadata: dict[str, JsonValue] = dict(artifact.additional_metadata or {})
        if image is None and not clear:
            current = metadata.get("gpu_pod")
            console.print(json.dumps(current, indent=2) if current else "no GPU form")
            return
        if clear:
            metadata.pop("gpu_pod", None)
        else:
            if push and image is not None:
                # Only now, with the key, the artifact and the arguments all
                # good: a pushed tag is live for every later pod.
                try:
                    pushed = push_to_ecr(image, source=source, settings=GpuSettings.from_env())
                except (ValueError, RuntimeError) as error:
                    console.print(f"[red]{error}[/red]")
                    raise typer.Exit(1) from error
                console.print(f"pushed {pushed.repository}:{pushed.tag} to {pushed.registry}")
                # The push took minutes and the endpoint replaces the whole
                # object: write over what is there now, not what was read first.
                fresh = app.get(f"/api/v2/artifacts/{artifact_id}")
                if fresh.status_code != 200:
                    console.print(f"[red]{fresh.status_code}: {fresh.text}[/red]")
                    raise typer.Exit(1)
                metadata = dict(_ArtifactView.model_validate_json(fresh.content).additional_metadata or {})
            fields: dict[str, object] = {
                "image": image,
                "command": command,
                "env": _kv(env, "--env"),
                "options": option,
            }
            if gpu:
                fields["gpu_type_ids"] = gpu
            if disk_gb is not None:
                fields["container_disk_gb"] = disk_gb
            if mcp_port is not None:
                fields["mcp_port"] = mcp_port
            if desktop_port is not None:
                fields["desktop_port"] = desktop_port
            metadata["gpu_pod"] = PodImage.model_validate(fields).model_dump(mode="json")
        written = app.put(
            f"/api/v2/artifacts/{artifact_id}/additional_metadata", json={"additional_metadata": metadata}
        )
        if written.status_code != 200:
            console.print(f"[red]{written.status_code}: {written.text}[/red]")
            raise typer.Exit(1)
        console.print("GPU form removed" if clear else json.dumps(metadata["gpu_pod"], indent=2))
