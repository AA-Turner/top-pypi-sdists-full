"""The publish flow shared by ``plato world publish`` and ``plato agent publish``.

Both commands ship the same two artifacts for one package version: a Docker
image in ECR tagged ``:<version>`` and a wheel on the matching Plato PyPI
index. The wheel's ``schema.json`` pins that image tag, and Chronos resolves
``package:latest`` through the index, so **the wheel upload is the moment a
version becomes launchable**. Everything here is ordered around that:

1. Image first. Either retag an existing image as ``:<version>`` (a manifest
   copy, same digest, already warm), or push ``:<version>``, boot one VM from
   it so its rootfs lands in the snapshot store, and only then promote it to
   ``:latest``.
2. Wheel last. If any image step fails, nothing reaches the index and no
   launch can resolve a version whose image never booted.

What differs between worlds and agents is captured in :class:`PublishKind`.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import typer

from plato.cli.chronos.settings import get_settings as get_chronos_settings
from plato.cli.utils import console, wait_for_pypi_version
from plato.utils.ecr import (
    ECR_REGISTRY,
    ImageLookupError,
    describe_image_digest,
    get_agent_image_digest_via_chronos,
    get_world_image_digest_via_chronos,
    publish_docker_image,
    retag_agent_image_via_chronos,
    retag_image,
    retag_image_via_chronos,
)

# (chronos_url, package_name, source_tag, target_tag, api_key) -> (ok, error)
ChronosRetag = Callable[[str, str, str, str, str], tuple[bool, str | None]]
# (chronos_url, package_name, tag, api_key) -> (answered, digest_or_None, error)
ChronosDigest = Callable[[str, str, str, str], tuple[bool, str | None, str | None]]


@dataclass(frozen=True)
class PublishKind:
    """The per-package-type parameters of the publish flow."""

    pypi_repo: str
    """Plato PyPI repository the wheel goes to (``worlds`` / ``agents``)."""

    ecr_repo_prefix: str
    """ECR repository prefix the image goes under (``vm/rootfs/plato-worlds``)."""

    name_prefixes: tuple[str, ...]
    """Package-name prefixes stripped to get the short name used for the ECR repo."""

    retag_via_chronos: ChronosRetag
    """Server-side retag endpoint for this package type."""

    image_digest_via_chronos: ChronosDigest
    """Server-side, read-only digest lookup for this package type."""

    def short_name(self, package_name: str) -> str:
        for prefix in self.name_prefixes:
            if package_name.startswith(prefix):
                return package_name[len(prefix) :]
        return package_name

    def repository(self, package_name: str) -> str:
        return f"{self.ecr_repo_prefix}/{self.short_name(package_name)}"


WORLD = PublishKind(
    pypi_repo="worlds",
    ecr_repo_prefix="vm/rootfs/plato-worlds",
    name_prefixes=("plato-world-", "plato-"),
    retag_via_chronos=retag_image_via_chronos,
    image_digest_via_chronos=get_world_image_digest_via_chronos,
)

AGENT = PublishKind(
    pypi_repo="agents",
    ecr_repo_prefix="vm/rootfs/plato-agents",
    name_prefixes=("plato-agent-", "plato-"),
    retag_via_chronos=retag_agent_image_via_chronos,
    image_digest_via_chronos=get_agent_image_digest_via_chronos,
)


def registry_api_url() -> str:
    """``https://plato.so/api`` unless PLATO_REGISTRY_BASE_URL points elsewhere."""
    registry_url = os.getenv("PLATO_REGISTRY_BASE_URL", "https://plato.so").rstrip("/")
    if registry_url.endswith("/api"):
        registry_url = registry_url[:-4]
    return f"{registry_url}/api"


def find_wheel(pkg_path: Path, package_name: str, version: str) -> Path:
    """The wheel ``uv build`` just wrote for this version (falls back to any wheel in dist/)."""
    dist_dir = pkg_path / "dist"
    if not dist_dir.exists():
        console.print("[red]Error: dist/ directory not found after build[/red]")
        raise typer.Exit(1)

    normalized_name = package_name.replace("-", "_")
    wheel_files = list(dist_dir.glob(f"{normalized_name}-{version}-*.whl")) or list(dist_dir.glob("*.whl"))
    if not wheel_files:
        console.print(f"[red]Error: No wheel file found in {dist_dir}[/red]")
        raise typer.Exit(1)
    return wheel_files[0]


def retag_source_tags(previous_version: str, version: str) -> list[str]:
    """Image tags a --skip-docker publish tries, in order, as the source for :<version>.

    The version being bumped from comes first: it is the last thing this
    checkout published, so a ``--dev --no-skip-docker`` rebuild (which never
    moves :latest) chains forward into the python-only dev publishes that
    follow it, and a fresh checkout starts from its release tag. :latest is the
    fallback — it is also the only candidate when the version was bumped
    externally (CI's version-bump.sh) so previous == new.
    """
    tags = []
    if previous_version and previous_version != version:
        tags.append(previous_version)
    tags.append("latest")
    return tags


# Cold-image boot = docker pull + rootfs conversion + snapshot-store ingest,
# which is the 10+ minute path this prefetch exists to absorb, so the client
# polls wait_for_ready for up to 30 minutes (a timeout here blocks promotion
# to :latest and the wheel upload). The VM lifetime sent in the /make body must
# cover that same window: the backend stamps job_start_time when the job is
# matched to a VM slot — before the rootfs build — and the VM agent force-shuts
# the VM once job_max_timeout elapses (plato: node_provider match callback +
# vm_lifecycle.check_job_timeout), so a short lifetime would kill a slow ingest
# mid-flight. The VM is closed the moment it is ready and the worker heartbeat
# timeout (300s) reaps it if this CLI dies, so the long lifetime never actually
# keeps a VM alive.
PREFETCH_TIMEOUT_S = 1800


def prefetch_image(image_url: str, short_name: str) -> bool:
    """Boot one throwaway VM from ``image_url`` so its rootfs lands in the snapshot store.

    Returns True only if the VM actually came up. This is the gate for promoting
    the image to ``:latest`` and for uploading the wheel: a digest that has never
    booted must not become the tag every launch resolves.
    """
    console.print(f"[cyan]Starting VM to prefetch {image_url}...[/cyan]")

    try:
        from plato.v2 import Env, Plato
        from plato.v2.types import SimConfigCompute

        plato = Plato()
        env = Env.resource(
            simulator=f"prefetch-{short_name}",
            sim_config=SimConfigCompute(),
            docker_image_url=image_url,
            upload_rootfs=True,
            rootfs_storage_backend="snapshot-store",
        )
        session = plato.sessions.create(
            envs=[env],
            timeout=PREFETCH_TIMEOUT_S,
            ready_timeout=PREFETCH_TIMEOUT_S,
            connect_network=False,
        )
        console.print("[green]Prefetch complete - rootfs cached[/green]")
        session.close()
        plato.close()
        return True
    except Exception as e:
        console.print(f"[red]Prefetch failed: {e}[/red]")
        return False


def image_digest(kind: PublishKind, package_name: str, tag: str, api_key: str | None) -> str | None:
    """Digest of ``:tag`` in the package's ECR repo, or ``None`` if the tag does not exist.

    Read-only. Asks Chronos first (its ECS task role reads ECR, so the author
    needs no local AWS access and nothing is mutated), and falls back to the
    local aws CLI only when Chronos could not answer — endpoint not deployed,
    unreachable, or no API key on a dry run. Raises :class:`ImageLookupError`
    when neither could answer, so "couldn't ask" is never mistaken for "absent".
    """
    if api_key is not None:
        answered, digest, reason = kind.image_digest_via_chronos(
            get_chronos_settings().chronos_url, package_name, tag, api_key
        )
        if answered:
            return digest
        console.print(f"[dim]Chronos digest lookup for :{tag} failed ({reason}); trying local AWS[/dim]")
    return describe_image_digest(kind.repository(package_name), tag)


def _image_digest_or_none(kind: PublishKind, package_name: str, tag: str, api_key: str | None) -> str | None:
    """:func:`image_digest` for the no-op-rebuild check, where an unanswerable lookup just means "prefetch"."""
    try:
        return image_digest(kind, package_name, tag, api_key)
    except ImageLookupError as e:
        console.print(f"[dim]Could not look up :{tag} ({e}); assuming it changed[/dim]")
        return None


def retag(
    kind: PublishKind,
    package_name: str,
    source_tag: str,
    target_tag: str,
    api_key: str | None,
) -> bool:
    """Copy ``source_tag`` -> ``target_tag`` in the package's ECR repo (manifest copy, same digest).

    Prefers the server-side retag (Chronos uses its own ECS task creds, so the
    author needs no local AWS access), falling back to local AWS credentials if
    the endpoint is unavailable. The Chronos call needs an API key, which is
    absent on dry runs — those go straight to the local fallback.
    """
    retagged = False
    if api_key is not None:
        retagged, retag_err = kind.retag_via_chronos(
            get_chronos_settings().chronos_url, package_name, source_tag, target_tag, api_key
        )
        if not retagged:
            console.print(
                f"[dim]Chronos retag :{source_tag} -> :{target_tag} failed ({retag_err}); trying local AWS[/dim]"
            )
    if not retagged:
        retagged = retag_image(kind.repository(package_name), source_tag, target_tag)
    return retagged


def publish_image(
    kind: PublishKind,
    *,
    package_name: str,
    previous_version: str,
    version: str,
    build_path: Path,
    api_key: str | None,
    dry_run: bool,
    skip_docker: bool,
    promote_latest: bool,
    build_args: dict[str, str] | None = None,
    no_cache: bool = False,
) -> None:
    """Make ``:<version>`` exist in ECR and be warm.

    ``skip_docker``: retag the image of the version being bumped from (falling
    back to :latest) as :<version>. No boot needed — it is a digest that has
    already been through this gate.

    Otherwise: push :<version> -> prefetch :<version> -> retag :<version> as
    :latest. :latest only ever moves to a digest that has already booted on a
    node and seeded the snapshot store; a retag is a manifest copy, so the
    promoted tag is warm the instant it flips. With ``promote_latest=False``
    (dev publishes) the image is pushed and prefetched under :<version> only —
    :latest is prod's tag and a laptop iteration has no business moving it;
    the next --dev --skip-docker publish chains from :<version> via
    :func:`retag_source_tags`.
    """
    short_name = kind.short_name(package_name)
    repository = kind.repository(package_name)
    version_image = f"{ECR_REGISTRY}/{repository}:{version}"
    latest_image = f"{ECR_REGISTRY}/{repository}:latest"

    if dry_run:
        if skip_docker:
            console.print("[yellow]Dry run - would retag the existing image:[/yellow]")
            console.print(f"  {version_image}")
        else:
            console.print("[yellow]Dry run - would build and push Docker image:[/yellow]")
            console.print(f"  {version_image}")
            if promote_latest:
                console.print(f"  then prefetch it and promote it to {latest_image}")
            else:
                console.print("  then prefetch it (dev publish: :latest is not moved)")
        return

    if skip_docker:
        source_tags = retag_source_tags(previous_version, version)
        for source_tag in source_tags:
            console.print(f"[cyan]Retagging :{source_tag} as :{version}...[/cyan]")
            if retag(kind, package_name, source_tag, version, api_key):
                console.print(f"[green]Retagged:[/green] {version_image} (from :{source_tag})")
                return
        console.print(f"[red]Failed to retag image from any of {source_tags}. Is there an existing :latest?[/red]")
        raise typer.Exit(1)

    if not shutil.which("docker"):
        console.print("[red]Error: docker not found[/red]")
        raise typer.Exit(1)

    # Current :latest digest, to detect a no-op rebuild below.
    old_latest_digest = _image_digest_or_none(kind, package_name, "latest", api_key)

    console.print("[cyan]Building and pushing Docker image...[/cyan]")
    result = publish_docker_image(
        name=short_name,
        version=version,
        build_path=str(build_path),
        repo_prefix=kind.ecr_repo_prefix,
        build_args=build_args,
        no_cache=no_cache,
    )
    if not result.success:
        console.print(f"[red]{result.error}[/red]")
        raise typer.Exit(1)
    console.print(f"[green]Published:[/green] {result.ecr_image}")

    new_digest = _image_digest_or_none(kind, package_name, version, api_key)
    if new_digest is not None and new_digest == old_latest_digest:
        console.print("\n[dim]Docker image digest unchanged - :latest already points at it, skipping prefetch[/dim]")
        return

    prefetch_then_promote(
        kind, package_name=package_name, version=version, api_key=api_key, promote_latest=promote_latest
    )


def prefetch_then_promote(
    kind: PublishKind,
    *,
    package_name: str,
    version: str,
    api_key: str | None,
    promote_latest: bool,
) -> None:
    """Boot ``:<version>`` once, then (release publishes only) retag it as ``:latest``.

    Shared by a rebuild and by ``--wheel-only``, which re-runs exactly this step
    after a publish whose prefetch or promote failed. Both failures leave the
    pushed ``:<version>`` in place, so the recovery is ``--wheel-only`` — a plain
    re-run would bump the version again.
    """
    short_name = kind.short_name(package_name)
    repository = kind.repository(package_name)
    version_image = f"{ECR_REGISTRY}/{repository}:{version}"
    latest_image = f"{ECR_REGISTRY}/{repository}:latest"

    console.print()
    console.print("[bold]Prefetching image...[/bold]")
    if not prefetch_image(version_image, short_name):
        console.print(
            f"[red]Prefetch failed: {version_image} is pushed but has not booted"
            + (" and :latest was NOT moved" if promote_latest else "")
            + ". Fix the boot failure (or, for a transient scheduling error, just retry) and re-run the publish "
            "with --wheel-only - it prefetches the pushed image without rebuilding or bumping.[/red]"
        )
        raise typer.Exit(1)

    if not promote_latest:
        console.print(
            f"[dim]Dev publish - :latest not moved. Launch by pinned version {package_name}:{version}; "
            "later --dev publishes retag from it.[/dim]"
        )
        return

    console.print("[cyan]Promoting to :latest...[/cyan]")
    if not retag(kind, package_name, version, "latest", api_key):
        console.print(
            f"[red]Failed to promote {version_image} to :latest (prefetch succeeded; "
            ":latest was NOT moved). Re-run the publish with --wheel-only.[/red]"
        )
        raise typer.Exit(1)
    console.print(f"[green]Promoted:[/green] {latest_image}")


def upload_wheel(
    kind: PublishKind,
    *,
    package_name: str,
    version: str,
    wheel_file: Path,
    api_key: str,
) -> None:
    """Upload the wheel to the package type's Plato PyPI index and wait for it to be listed."""
    upload_url = f"{registry_api_url()}/v2/pypi/{kind.pypi_repo}/"
    console.print(f"\n[cyan]Uploading to {upload_url}...[/cyan]")

    try:
        result = subprocess.run(
            [
                "uv",
                "publish",
                "--publish-url",
                upload_url,
                "--username",
                "__token__",
                "--password",
                api_key,
                str(wheel_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        console.print("[red]Error: uv not found[/red]")
        raise typer.Exit(1) from None

    if result.returncode != 0:
        console.print("[red]Upload failed:[/red]")
        if result.stdout:
            console.print(result.stdout)
        if result.stderr:
            console.print(result.stderr)
        raise typer.Exit(1)

    console.print("[green]Upload successful![/green]")
    wait_for_pypi_version(package_name, version, repo=kind.pypi_repo, api_key=api_key)


def publish_image_then_wheel(
    kind: PublishKind,
    *,
    package_name: str,
    previous_version: str,
    version: str,
    pkg_path: Path,
    wheel_file: Path,
    api_key: str | None,
    dry_run: bool,
    skip_docker: bool,
    promote_latest: bool,
    build_args: dict[str, str] | None = None,
    no_cache: bool = False,
    wheel_only: bool = False,
) -> None:
    """Image (if the package has a Dockerfile), then the wheel. See the module docstring.

    ``wheel_only`` is the re-run after a publish that pushed ``:<version>`` but
    failed later — prefetch (e.g. a VM demand that was never scheduled), promote,
    or upload (index conflict, CodeArtifact hiccup). It never rebuilds, and only
    proceeds if ``:<version>`` really is in ECR, because the wheel pins that tag.
    Unless ``:latest`` already points at that digest (the earlier run got through
    promotion), it redoes :func:`prefetch_then_promote` before the upload, so the
    gate holds: nothing reaches the index until its image has booted.
    """
    has_dockerfile = (pkg_path / "Dockerfile").exists()
    if wheel_only and has_dockerfile:
        repository = kind.repository(package_name)
        version_image = f"{ECR_REGISTRY}/{repository}:{version}"
        if dry_run:
            console.print(
                f"\n[yellow]Dry run - would check {version_image} exists, then upload the wheel only[/yellow]"
            )
        else:
            try:
                digest = image_digest(kind, package_name, version, api_key)
            except ImageLookupError as e:
                console.print(
                    f"[red]--wheel-only: could not verify that {version_image} exists ({e}). "
                    "Refusing to upload a wheel for an image that may not be there.[/red]"
                )
                raise typer.Exit(1) from None
            if digest is None:
                console.print(
                    f"[red]--wheel-only: no image {version_image} in ECR. The wheel pins that tag, so uploading "
                    "it now would publish a version nothing can boot. Re-run without --wheel-only "
                    "(or with --skip-docker to retag an existing image) to create it first.[/red]"
                )
                raise typer.Exit(1)
            console.print(f"\n[green]Image already published:[/green] {version_image} ({digest})")
            if _image_digest_or_none(kind, package_name, "latest", api_key) == digest:
                console.print("[dim]:latest already points at it - already booted and promoted[/dim]")
            else:
                prefetch_then_promote(
                    kind, package_name=package_name, version=version, api_key=api_key, promote_latest=promote_latest
                )
    elif has_dockerfile:
        console.print()
        publish_image(
            kind,
            package_name=package_name,
            previous_version=previous_version,
            version=version,
            build_path=pkg_path,
            api_key=api_key,
            dry_run=dry_run,
            skip_docker=skip_docker,
            promote_latest=promote_latest,
            build_args=build_args,
            no_cache=no_cache,
        )
    else:
        console.print("\n[dim]No Dockerfile found - skipping Docker image build[/dim]")

    if dry_run:
        console.print("\n[yellow]Dry run - skipping PyPI upload[/yellow]")
        return
    assert api_key is not None
    upload_wheel(kind, package_name=package_name, version=version, wheel_file=wheel_file, api_key=api_key)
