"""Capability subcommands for the cyclopts CLI."""

import asyncio
import hashlib
import json
import os
import re
import shutil
import typing as t
from datetime import UTC, datetime
from pathlib import Path

import cyclopts

from dreadnode.app.cli.args import PlatformArgs
from dreadnode.app.cli.shared import (
    _FLAG_SEARCH,
    ArtifactRef,
    _collect_pages,
    _hint,
    _print_json,
    _render_list,
    _sync_progress,
    _visibility_markup,
    configured_dreadnode,
    confirm_destructive,
    console,
    ensure_name_only_refs,
    ensure_version,
    print_error,
    print_markdown,
    print_success,
    print_warning,
    resolve_publish_flag,
)

# ---------------------------------------------------------------------------
# Starter file templates for `init`
# ---------------------------------------------------------------------------

_CAPABILITY_YAML = """\
schema: 1
name: {name}
version: "{version}"
description: "{description}"
"""

_CAPABILITY_YAML_AUTHOR = """\
author:
  name: {author}
"""

_AGENT_MD = """\
---
name: example
---
You are a helpful assistant.
"""

_SKILL_MD = """\
---
name: example
description: ""
---
"""

_MCP_JSON = """\
{
  "mcpServers": {}
}
"""

cli = cyclopts.App(
    name="capability",
    help="Composable packages of agents, tools, and skills — capture domain expertise, share it, and refine it over time.",
)


# ---------------------------------------------------------------------------
# init
# ---------------------------------------------------------------------------

_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def _write_file(path: Path, content: str) -> None:
    """Write a file, creating parent directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _write_json_file(path: Path, payload: t.Any) -> None:
    """Write JSON with stable formatting for CLI artifacts."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n")


@cli.command(alias="new")
def init(
    name: str,
    *,
    description: str = "A new capability",
    version: t.Annotated[str, cyclopts.Parameter(name="--initial-version")] = "0.1.0",
    author: str | None = None,
    with_skills: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    with_mcp: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    path: Path = Path(),
) -> None:
    """Scaffold a new capability directory ready for development.

    Creates a capability.yaml manifest and a starter agent definition.
    The result passes ``capability validate`` immediately. Use
    ``capability install`` to make it available to local agents.

    Args:
        name: Capability name (e.g. my-recon-cap). Lowercase letters,
            digits, and hyphens only.
        description: One-line description of what this capability does.
        version: Initial semver version.
        author: Author name to include in the manifest.
        with_skills: Also create a starter skill directory.
        with_mcp: Also create a starter .mcp.json file.
        path: Parent directory to create the capability folder in.
    """
    if not _NAME_PATTERN.fullmatch(name):
        raise ValueError(
            f'Invalid capability name "{name}" — use lowercase letters, digits, and hyphens only'
        )

    cap_dir = path.resolve() / name

    if cap_dir.exists():
        raise FileExistsError(f"{cap_dir} already exists")

    # Build manifest
    manifest = _CAPABILITY_YAML.format(name=name, version=version, description=description)
    if author:
        manifest += _CAPABILITY_YAML_AUTHOR.format(author=author)

    # Write files
    _write_file(cap_dir / "capability.yaml", manifest)
    print_success(f"{name}/capability.yaml")

    _write_file(cap_dir / "agents" / "example.md", _AGENT_MD)
    print_success(f"{name}/agents/example.md")

    if with_skills:
        _write_file(cap_dir / "skills" / "example" / "SKILL.md", _SKILL_MD)
        print_success(f"{name}/skills/example/SKILL.md")

    if with_mcp:
        _write_file(cap_dir / ".mcp.json", _MCP_JSON)
        print_success(f"{name}/.mcp.json")


# ---------------------------------------------------------------------------
# install
# ---------------------------------------------------------------------------


@cli.command()
def install(
    ref: str,
    *,
    force: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    copy: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Install a capability so agents can use it.

    If the argument is a path to a directory on disk, the capability
    is validated and symlinked into ~/.dreadnode/capabilities/ so edits
    are live. Use --copy to create a frozen snapshot instead.

    Otherwise the argument is treated as a registry reference and the
    capability is downloaded from the platform.

    Args:
        ref: Capability reference or local path.
            Registry: my-cap, my-cap@1.0.0, acme/my-cap.
            Local: ./my-cap, /abs/path/to/cap.
        force: Overwrite if already installed.
        copy: Copy files instead of symlinking (local installs only).
    """
    candidate = Path(ref).resolve()
    if candidate.is_dir():
        _install_from_path(candidate, force=force, copy=copy)
    else:
        _install_from_registry(ref, force=force, platform=platform)


_RELOAD_HINT = "Run /reload in the TUI to pick up the change."


def _handle_already_installed(*, name: str, state_path: Path, version: str | None) -> bool:
    """Graceful 'already installed' path for ``install``.

    If the capability is on disk but disabled in the state file, flip it
    back to enabled and print a message. If it's already enabled, print
    a no-op message. Returns ``True`` when the situation was handled and
    the caller should not proceed to a fresh install.
    """
    from dreadnode.capabilities.capability import (
        read_local_capability_records,
        write_local_capability_records,
    )

    records = read_local_capability_records(state_path)
    record = records.get(name)
    if record is None:
        # On disk but no state record (manually copied?). Let the install
        # primitive raise its FileExistsError so the user picks --force.
        return False

    installed_version = record.get("version") or version or "?"
    enabled = bool(record.get("enabled", True))

    if not enabled:
        record["enabled"] = True
        records[name] = record
        write_local_capability_records(state_path, records)
        print_success(
            f"{name} v{installed_version} was installed but disabled — enabled now. {_RELOAD_HINT}"
        )
        return True

    print_success(
        f"{name} v{installed_version} already installed and enabled. Use --force to reinstall."
    )
    return True


def _install_from_path(source: Path, *, force: bool, copy: bool) -> None:
    """Install a capability from a local directory."""
    from dreadnode.capabilities.capability import Capability
    from dreadnode.capabilities.sync import install_local
    from dreadnode.storage.storage import Storage

    # Validate before touching anything
    cap = Capability(source)

    storage = Storage()
    target_dir = storage.capabilities_path / cap.name
    if not force and (target_dir.exists() or target_dir.is_symlink()):
        if _handle_already_installed(
            name=cap.name,
            state_path=storage.local_capability_state_path,
            version=cap.version,
        ):
            return

    install_local(
        source_path=source,
        local_dir=storage.capabilities_path,
        state_path=storage.local_capability_state_path,
        name=cap.name,
        version=cap.version,
        overwrite=force,
        copy=copy,
    )

    mode = "copied" if copy else "symlinked"
    local_ref = ArtifactRef(org="local", name=cap.name, version=cap.version)
    print_success(f"Installed {local_ref.format()} ({mode}). {_RELOAD_HINT}")


def _install_from_registry(raw_ref: str, *, force: bool, platform: PlatformArgs) -> None:
    """Install a capability from the platform registry."""
    from dreadnode.capabilities.sync import LocalInstallClient, bare_capability_name
    from dreadnode.storage.storage import Storage

    api, profile = platform.connect()
    ref = ensure_version(api, "capability", ArtifactRef.parse(raw_ref, profile.org_key))
    source = "public" if ref.org != profile.org_key else "org"

    storage = Storage()

    local_name = bare_capability_name(ref.name)
    target_dir = storage.capabilities_path / local_name
    if not force and target_dir.exists():
        if _handle_already_installed(
            name=local_name,
            state_path=storage.local_capability_state_path,
            version=ref.version,
        ):
            return

    installer = LocalInstallClient(
        api=api,
        org=ref.org,
        local_dir=storage.capabilities_path,
        state_path=storage.local_capability_state_path,
    )

    asyncio.run(
        installer.install(
            name=ref.name,
            version=ref.version,
            source=source,
            overwrite=force,
        )
    )
    print_success(f"Installed {ref.format()}. {_RELOAD_HINT}")


@cli.command()
def uninstall(name: str) -> None:
    """Uninstall a locally-installed capability.

    Removes the entry from the local user store (symlink or directory) and
    its state record. Idempotent: succeeds even if the capability was already
    partially removed.

    To delete a published capability version from the platform registry,
    use ``rm`` instead.

    Args:
        name: Bare or org-qualified capability name (e.g. ``my-cap`` or
            ``acme/my-cap``).
    """
    from dreadnode.capabilities.sync import uninstall_local
    from dreadnode.storage.storage import Storage

    storage = Storage()
    result = uninstall_local(
        name=name,
        local_dir=storage.capabilities_path,
        state_path=storage.local_capability_state_path,
    )

    if not result.removed_disk and not result.removed_state:
        print_warning(f"{name} is not installed locally")
        return

    detail = " (symlink)" if result.was_symlink else ""
    print_success(f"Uninstalled {name}{detail}")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _summarize_capability(p: dict[str, t.Any]) -> str:
    name = p.get("name", "unknown")
    version = p.get("version", "unknown")
    visibility = "public" if p.get("is_public") else "private"
    description = p.get("description")
    suffix = f" [dim]-[/dim] {description}" if description else ""
    return f"[cyan]{name}[/cyan]@[dim]{version}[/dim] {_visibility_markup(visibility)}{suffix}"


_CAPABILITY_LIST_ROW_FIELDS: tuple[str, ...] = (
    "description",
    "is_public",
    "keywords",
    "author_name",
    "license",
    "component_counts",
    "version_count",
    "versions",
    "created_at",
    "updated_at",
)


def _download_capability_files(
    api: t.Any,
    org: str,
    name: str,
    version: str,
    dest: Path,
) -> None:
    """Download capability files to *dest*, trying bundle then file-by-file."""
    from loguru import logger

    from dreadnode.capabilities.sync import _extract_tar_to_dir

    # Fast path: single tar.gz bundle download
    bundle_ok = False
    try:
        data = api.download_capability_bundle(org, name, version)
        _extract_tar_to_dir(data, dest)
        bundle_ok = True
    except Exception:
        logger.debug(
            "Bundle download unavailable for {}/{}@{}, falling back to file-by-file",
            org,
            name,
            version,
        )

    if bundle_ok:
        return

    # Slow path: fetch manifest and download each file individually
    detail = api.get_capability(org, name, version)
    file_manifest = detail.get("file_manifest", [])
    if not file_manifest:
        raise RuntimeError(f"Capability {org}/{name}@{version} has no downloadable files")

    dest.mkdir(parents=True, exist_ok=True)
    for entry in file_manifest:
        file_path = entry["path"]
        content = api.get_capability_file(org, name, version, file_path)
        file_dest = dest / file_path
        file_dest.parent.mkdir(parents=True, exist_ok=True)
        file_dest.write_bytes(content if isinstance(content, bytes) else content.encode())


# ---------------------------------------------------------------------------
# push
# ---------------------------------------------------------------------------


@cli.command(alias="upload")
def push(
    path: Path,
    *,
    name: str | None = None,
    skip_upload: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    force: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    publish: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    public_compat: t.Annotated[
        bool,
        cyclopts.Parameter(name="--public", negative=(), show=False),
    ] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Publish a capability to your organization's registry.

    Args:
        path: Capability directory containing capability.yaml.
        name: Override the registry name. Bare names are auto-prefixed
            with the active organization.
        skip_upload: Build and validate locally without publishing.
        force: Overwrite even if this version already exists with different content.
        publish: Ensure the capability is publicly discoverable after publishing.
    """
    publish = resolve_publish_flag(publish, public_compat)
    dn = configured_dreadnode(platform)
    result = dn.push_capability(
        path,
        name=name,
        skip_upload=skip_upload,
        force=force,
        publish=publish,
    )

    display = f"[cyan]{result.name}[/cyan]@[dim]{result.version}[/dim]"
    if result.status == "built":
        console.print(f"Built {display}")
    elif result.status == "up_to_date":
        console.print(f"{display} already up to date")
    else:
        digest = result.digest or "unknown"
        console.print(f"Pushed {display} [dim]({digest})[/dim]")


@cli.command()
def publish(
    refs: t.Annotated[list[str], cyclopts.Parameter(negative_iterable=())],
    *,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Make one or more capability families visible to other organizations."""
    dn = configured_dreadnode(platform)
    parsed_refs = ensure_name_only_refs(refs, dn.profile.org_key)
    for ref in parsed_refs:
        dn.set_capability_visibility(ref.org, ref.name, is_public=True)
        print_success(f"Published {ref.qualified_name}")


@cli.command()
def unpublish(
    refs: t.Annotated[list[str], cyclopts.Parameter(negative_iterable=())],
    *,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Make one or more capability families private."""
    dn = configured_dreadnode(platform)
    parsed_refs = ensure_name_only_refs(refs, dn.profile.org_key)
    for ref in parsed_refs:
        dn.set_capability_visibility(ref.org, ref.name, is_public=False)
        print_success(f"Unpublished {ref.qualified_name}")


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------


@cli.command(name="list", alias="ls")
def list_(
    *,
    search: t.Annotated[str | None, cyclopts.Parameter(name=_FLAG_SEARCH)] = None,
    limit: int = 50,
    include_public: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Show capabilities in your organization.

    Args:
        search: Search by name or description.
        limit: Maximum results to show.
        include_public: Include public capabilities from other organizations.
        as_json: Output raw JSON instead of a summary.
    """
    api, profile = platform.connect()
    items = _collect_pages(
        lambda page, page_size: api.list_capabilities(
            profile.org_key,
            search=search,
            page=page,
            limit=page_size,
            include_public=include_public,
        ),
        limit=limit,
        page_size=100,
        items_key="capabilities",
    )
    _render_list(
        items,
        as_json=as_json,
        summary=_summarize_capability,
        empty_msg="No capabilities found",
        fields=_CAPABILITY_LIST_ROW_FIELDS,
    )
    if not as_json and items:
        example = items[0].get("name", "<name>")
        _hint(f"dn capability info {example}")


# ---------------------------------------------------------------------------
# status
# ---------------------------------------------------------------------------


def _summarize_local_capability(p: dict[str, t.Any]) -> str:
    name = p.get("name", "unknown")
    version = p.get("version") or "?"
    enabled = bool(p.get("enabled", True))
    state = "[green]enabled[/green]" if enabled else "[yellow]disabled[/yellow]"
    source = p.get("source") or "local"
    suffix = f" [dim]({source})[/dim]"
    return f"[cyan]{name}[/cyan]@[dim]{version}[/dim] {state}{suffix}"


@cli.command()
def status(
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
) -> None:
    """Show capabilities installed locally and whether they're enabled.

    Reads the local install state (``~/.dreadnode/capabilities/`` plus the
    state file) so agents and humans can see at a glance what the running
    runtime will pick up on the next reload.

    Args:
        as_json: Output raw JSON instead of a summary.
    """
    from dreadnode.capabilities.capability import read_local_capability_records
    from dreadnode.storage.storage import Storage

    storage = Storage()
    records = read_local_capability_records(storage.local_capability_state_path)

    items: list[dict[str, t.Any]] = []
    for name, record in sorted(records.items()):
        target = storage.capabilities_path / name
        items.append(
            {
                "name": name,
                "version": record.get("version"),
                "enabled": bool(record.get("enabled", True)),
                "source": record.get("source", "local"),
                "path": str(target) if target.exists() or target.is_symlink() else None,
            }
        )

    _render_list(
        items,
        as_json=as_json,
        summary=_summarize_local_capability,
        empty_msg="No capabilities installed locally",
    )


# ---------------------------------------------------------------------------
# info
# ---------------------------------------------------------------------------


@cli.command()
def info(
    ref: str,
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    readme: t.Annotated[bool, cyclopts.Parameter(name="--readme", alias="-R", negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Show details and available versions for a capability.

    Version is optional — defaults to the latest. Use org/name to
    inspect public capabilities from other organizations.

    Args:
        ref: Capability to inspect (e.g. my-cap, my-cap@1.0.0,
            or acme/my-cap).
        as_json: Output raw JSON instead of a summary.
        readme: Render the bundled README (markdown) instead of the
            summary metadata.
    """
    api, profile = platform.connect()
    vref = ensure_version(api, "capability", ArtifactRef.parse(ref, profile.org_key))

    if readme:
        from dreadnode.app.api.client import NotFoundError

        try:
            payload = api.get_capability_readme(vref.org, vref.name, vref.version)
        except NotFoundError:
            print_warning(f"No README found in {vref.qualified_name}")
            return
        content = str(payload.get("content") or "")
        if not content.strip():
            print_warning(f"README in {vref.qualified_name} is empty")
            return
        print_markdown(content)
        return

    detail = api.get_capability(vref.org, vref.name, vref.version)
    versions_payload = api.list_capability_versions(vref.org, vref.name)

    if as_json:
        detail["available_versions"] = versions_payload.get("versions", [])
        _print_json(detail)
        return

    # Human-readable output
    console.print(_summarize_capability(detail))

    version_items = versions_payload.get("versions", [])
    if version_items:
        console.print(f"  [dim]versions:[/dim] {', '.join(str(v) for v in version_items)}")
    _hint(f"dn capability install {vref.qualified_name}")
    _hint(f"dn capability info {vref.qualified_name} --readme")


# ---------------------------------------------------------------------------
# pull
# ---------------------------------------------------------------------------


@cli.command(alias="download")
def pull(
    ref: str,
    *,
    output: t.Annotated[Path | None, cyclopts.Parameter(name="--output", alias="-o")] = None,
    force: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Download a capability to a local directory.

    Fetches the capability from the registry and writes it to disk.
    Defaults to a folder named after the capability in the current
    directory. Use ``--output`` to choose a different destination.

    This does **not** install or activate the capability — use
    ``install`` for that.

    Args:
        ref: Capability to pull (e.g. my-cap, my-cap@1.0.0, or acme/my-cap).
        output: Destination directory. Defaults to ./<capability-name>.
        force: Overwrite the destination if it already exists.
    """

    api, profile = platform.connect()
    parsed = ensure_version(api, "capability", ArtifactRef.parse(ref, profile.org_key))

    dest = (output or Path.cwd() / parsed.name).resolve()

    if dest.exists():
        if not force:
            raise FileExistsError(f"{dest} already exists — use --force to overwrite")
        shutil.rmtree(dest)

    _download_capability_files(api, parsed.org, parsed.name, parsed.version, dest)
    print_success(f"Pulled {parsed.format()} to {dest}")


# ---------------------------------------------------------------------------
# delete
# ---------------------------------------------------------------------------


@cli.command(alias="rm")
def delete(
    ref: str,
    *,
    yes: t.Annotated[bool, cyclopts.Parameter(name="--yes", alias="-y", negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Remove a published capability version from the registry.

    Args:
        ref: Capability to delete (e.g. my-cap@1.0.0). Version is required.
        yes: Skip the confirmation prompt.
    """
    api, profile = platform.connect()
    vref = ArtifactRef.parse_versioned(ref, profile.org_key)

    # Verify it exists before prompting
    api.get_capability(vref.org, vref.name, vref.version)

    if not confirm_destructive(f"Delete {vref.format()}?", yes=yes):
        console.print("[dim]Cancelled[/dim]")
        return

    api.delete_capability(vref.org, vref.name, vref.version)
    print_success(f"Deleted {vref.format()}")


# ---------------------------------------------------------------------------
# sync
# ---------------------------------------------------------------------------


@cli.command()
def sync(
    directory: Path,
    *,
    force: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    publish: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    public_compat: t.Annotated[
        bool,
        cyclopts.Parameter(name="--public", negative=(), show=False),
    ] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Publish all capabilities from a directory — ideal for CI pipelines.

    Discovers subdirectories containing capability.yaml, compares each
    against the registry by content hash, and only publishes those that
    changed.

    Args:
        directory: Root directory containing capability subdirectories.
        force: Publish all capabilities even if unchanged.
        publish: Ensure published capabilities are publicly discoverable.
    """
    publish = resolve_publish_flag(publish, public_compat)
    dn = configured_dreadnode(platform)
    result = dn.sync_capabilities(
        directory,
        force=force,
        publish=publish,
        on_progress=_sync_progress,
    )

    total = len(result.uploaded) + len(result.skipped) + len(result.failed)
    console.print(
        f"\nSynced {total}: "
        f"[green]{len(result.uploaded)} uploaded[/green], "
        f"[dim]{len(result.skipped)} skipped[/dim], "
        f"[red]{len(result.failed)} failed[/red]"
    )
    if not result.ok:
        raise SystemExit(1)


# ---------------------------------------------------------------------------
# improve
# ---------------------------------------------------------------------------


def _resolve_capability_agent(capability: t.Any, agent_name: str | None) -> t.Any:
    """Resolve one agent from a loaded capability."""
    agents = list(getattr(capability, "agents", []) or [])
    if not agents:
        raise ValueError(f"Capability {capability.name!r} does not expose any agents")
    if agent_name is None:
        return agents[0]
    for candidate in agents:
        if candidate.name == agent_name:
            return candidate
    raise ValueError(f"Agent {agent_name!r} was not found in capability {capability.name!r}")


def _resolve_improvement_model(
    capability: t.Any,
    *,
    agent_name: str | None,
    model: str | None,
) -> tuple[t.Any, str]:
    """Resolve the concrete execution model for local capability improvement."""
    from dreadnode.app.model_catalog import resolve_model

    agent_def = _resolve_capability_agent(capability, agent_name)
    selected_model = model or agent_def.model
    if not selected_model or selected_model == "inherit":
        raise ValueError(
            f"Agent {agent_def.name!r} in capability {capability.name!r} declares "
            "`model: inherit` and has no concrete model to fall back on. "
            "Pass --model. See `dn inference-model list` for available models."
        )
    return agent_def, resolve_model(selected_model)


_DEFAULT_PROPOSER_CAPABILITY = "dreadnode/capability-improver"
_LEGACY_CAPABILITY_ROOT_ENV = "DREADNODE_CAPABILITIES_DIR"
_CAPABILITY_ROOTS_ENV = "DREADNODE_CAPABILITY_DIRS"


def _env_capability_roots() -> list[Path]:
    """Parse configured capability roots from supported environment variables."""
    roots: list[Path] = []
    raw_values = [
        os.getenv(_CAPABILITY_ROOTS_ENV, "").strip(),
        os.getenv(_LEGACY_CAPABILITY_ROOT_ENV, "").strip(),
    ]
    for raw_value in raw_values:
        if not raw_value:
            continue
        for entry in raw_value.split(os.pathsep):
            candidate = Path(entry).expanduser().resolve()
            if candidate.exists() and candidate not in roots:
                roots.append(candidate)
    return roots


def _candidate_capability_roots() -> list[Path]:
    """Return local capability workspace roots used for proposer lookup."""
    return _env_capability_roots()


def _resolve_workspace_capability_dir(ref: str, roots: list[Path]) -> Path | None:
    """Resolve a capability directory from a path, org/name ref, or bare local name."""
    candidate_path = Path(ref).expanduser()
    if candidate_path.is_dir() and (candidate_path / "capability.yaml").exists():
        return candidate_path.resolve()

    normalized_ref = ref.strip().strip("/")
    if not normalized_ref:
        return None

    if "/" in normalized_ref:
        for root in roots:
            candidate = root / normalized_ref
            if (candidate / "capability.yaml").exists():
                return candidate.resolve()
        return None

    matches: list[Path] = []
    for root in roots:
        for org_dir in sorted(path for path in root.iterdir() if path.is_dir()):
            candidate = org_dir / normalized_ref
            if (candidate / "capability.yaml").exists():
                matches.append(candidate.resolve())

    if not matches:
        return None
    if len(matches) > 1:
        matched = ", ".join(str(path) for path in matches)
        raise ValueError(
            f"Multiple local capabilities matched {normalized_ref!r}: {matched}. "
            "Use an org/name ref or explicit path."
        )
    return matches[0]


def _build_capability_agent(
    capability: t.Any,
    *,
    agent_name: str | None,
    model: str | None,
) -> tuple[t.Any, t.Any, str]:
    """Build one agent from a capability using the normal runtime assembly path."""
    from dreadnode.agents.skills import attach_capability_skills
    from dreadnode.app.server.app import create_agent

    agent_def, resolved_model = _resolve_improvement_model(
        capability,
        agent_name=agent_name,
        model=model,
    )
    agent = create_agent(
        resolved_model,
        capability=capability,
        agent_def=agent_def,
        extra_tools=capability.tools,
    )
    attach_capability_skills(agent=agent, capability=capability)
    return agent, agent_def, resolved_model


def _load_proposer_agent(
    *,
    proposer_capability: str | None,
    proposer_agent_name: str | None,
    proposer_model: str | None,
) -> tuple[t.Any | None, str | None]:
    """Load the optional proposer capability agent for local improvement."""
    from dreadnode.capabilities.capability import Capability

    selected_ref = proposer_capability or _DEFAULT_PROPOSER_CAPABILITY
    roots = _candidate_capability_roots()
    local_dir = _resolve_workspace_capability_dir(selected_ref, roots)

    if local_dir is None:
        if proposer_capability is None:
            return None, None
        capability = Capability(selected_ref)
    else:
        capability = Capability(local_dir)

    agent, agent_def, resolved_model = _build_capability_agent(
        capability,
        agent_name=proposer_agent_name,
        model=proposer_model,
    )
    descriptor = f"{capability.name}:{agent_def.name} [dim](model={resolved_model}, path={capability.path})[/dim]"
    return agent, descriptor


def _load_improvement_rows(path: Path) -> list[dict[str, t.Any]]:
    """Load a local dataset file or dataset directory into evaluation rows."""
    from dreadnode.datasets.local import load_dataset as load_local_dataset
    from dreadnode.datasets.local import load_file

    resolved = path.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Dataset path not found: {resolved}")

    if resolved.is_dir():
        table = load_local_dataset(resolved).load()
    else:
        table = load_file(resolved)

    rows = [item for item in table.to_pylist() if isinstance(item, dict)]
    if not rows:
        raise ValueError(f"Dataset {resolved} did not contain any object rows")
    return rows


def _resolve_scorers(identifiers: list[str]) -> list[t.Any]:
    """Resolve scorer identifiers into Scorer instances."""
    from dreadnode.core.discovery import find
    from dreadnode.core.scorer import Scorer

    scorers = [find(Scorer, identifier) for identifier in identifiers]
    if not scorers:
        raise ValueError("Capability improvement requires at least one --scorer")
    return scorers


def _parse_dataset_input_mapping(
    raw_items: list[str] | None,
) -> list[str] | dict[str, str] | None:
    """Parse repeatable dataset input mappings from CLI strings."""
    if not raw_items:
        return None

    mapping: dict[str, str] = {}
    positional: list[str] = []
    for item in raw_items:
        if "=" in item:
            key, value = item.split("=", 1)
            key = key.strip()
            value = value.strip()
            if not key or not value:
                raise ValueError(
                    f"Invalid --dataset-input mapping {item!r}; expected DATASET_KEY=TASK_PARAM"
                )
            mapping[key] = value
            continue
        positional.append(item.strip())

    if mapping and positional:
        raise ValueError(
            "--dataset-input must use either positional parameter names or DATASET_KEY=TASK_PARAM mappings, not both"
        )
    return mapping or positional


def _candidate_hash(candidate: dict[str, str]) -> str:
    """Return a stable digest for a flat candidate map."""
    encoded = json.dumps(candidate, sort_keys=True, ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _candidate_complexity(candidate: dict[str, str]) -> int:
    """Return a simple size heuristic for tie-breaking candidate simplicity."""
    return sum(len(value.strip()) for value in candidate.values())


def _score_candidate(adapter: t.Any, candidate: dict[str, str]) -> dict[str, t.Any]:
    """Run one adapter candidate evaluation and normalize the result."""
    evaluation = asyncio.run(adapter.evaluate_candidate(candidate))
    score = evaluation.score if evaluation.score is not None else 0.0
    return {
        "score": float(score),
        "side_info": evaluation.side_info,
    }


def _default_improvement_output_dir(capability_path: Path) -> Path:
    """Return the default artifact directory for a local capability improvement run."""
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    return capability_path / ".dreadnode" / "improve" / stamp


def _select_improvement_winner(
    *,
    baseline_candidate: dict[str, str],
    best_candidate: dict[str, str],
    baseline_train_score: float,
    best_train_score: float,
    baseline_holdout_score: float | None,
    best_holdout_score: float | None,
) -> tuple[dict[str, str], bool, str]:
    """Apply first-pass keep/discard rules for local capability improvement."""
    tolerance = 1e-9
    holdout_delta = (
        None
        if baseline_holdout_score is None or best_holdout_score is None
        else best_holdout_score - baseline_holdout_score
    )
    if holdout_delta is not None and holdout_delta < -tolerance:
        return baseline_candidate, False, "Rejected because holdout score regressed"

    train_delta = best_train_score - baseline_train_score
    if train_delta > tolerance:
        return best_candidate, True, "Accepted because train score improved"

    if abs(train_delta) <= tolerance and _candidate_complexity(
        best_candidate
    ) < _candidate_complexity(baseline_candidate):
        return (
            best_candidate,
            True,
            "Accepted because train score tied and the candidate is simpler",
        )

    return baseline_candidate, False, "Rejected because train score did not improve"


@cli.command()
def improve(
    path: Path,
    *,
    dataset: t.Annotated[
        Path,
        cyclopts.Parameter(help="Local dataset file or dataset directory used for optimization"),
    ],
    scorer: t.Annotated[
        list[str],
        cyclopts.Parameter(
            negative_iterable=(),
            help="Repeatable scorer identifier (path.py:name or package.module.name)",
        ),
    ],
    agent: t.Annotated[
        str | None,
        cyclopts.Parameter(help="Optional agent name when the capability exports multiple agents"),
    ] = None,
    model: t.Annotated[
        str | None,
        cyclopts.Parameter(help="Execution model override; required for inheriting agents"),
    ] = None,
    reflection_model: t.Annotated[
        str | None,
        cyclopts.Parameter(help="Reflection model override; defaults to the execution model"),
    ] = None,
    proposer_capability: t.Annotated[
        str | None,
        cyclopts.Parameter(
            help=(
                "Optional capability path or ref used to propose candidate text updates. "
                "Defaults to dreadnode/capability-improver when available from local capability roots."
            ),
        ),
    ] = None,
    proposer_agent: t.Annotated[
        str | None,
        cyclopts.Parameter(help="Optional agent name inside the proposer capability"),
    ] = None,
    proposer_model: t.Annotated[
        str | None,
        cyclopts.Parameter(help="Model override for the proposer capability agent"),
    ] = None,
    holdout_dataset: t.Annotated[
        Path | None,
        cyclopts.Parameter(help="Optional held-out local dataset used for keep/discard gating"),
    ] = None,
    surface: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(
            negative_iterable=(),
            help="Mutable capability-owned surfaces to optimize (repeatable)",
        ),
    ] = None,
    score_name: t.Annotated[
        str | None,
        cyclopts.Parameter(help="Metric name to optimize when scorers emit multiple metrics"),
    ] = None,
    goal_field: t.Annotated[
        str,
        cyclopts.Parameter(
            help="Dataset field to map to the agent goal when no explicit mapping is provided"
        ),
    ] = "goal",
    dataset_input: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(
            negative_iterable=(),
            help="Repeatable dataset input mapping as DATASET_KEY=TASK_PARAM",
        ),
    ] = None,
    objective: t.Annotated[
        str | None,
        cyclopts.Parameter(help="Optional natural-language optimization objective"),
    ] = None,
    max_metric_calls: t.Annotated[
        int,
        cyclopts.Parameter(help="Metric-call budget for the local search"),
    ] = 40,
    max_trials: t.Annotated[
        int,
        cyclopts.Parameter(help="Maximum number of local search trials"),
    ] = 8,
    max_trials_without_improvement: t.Annotated[
        int,
        cyclopts.Parameter(help="Stop after this many finished trials without a better score"),
    ] = 3,
    seed: t.Annotated[
        int,
        cyclopts.Parameter(help="Deterministic seed for the local optimization run"),
    ] = 0,
    output_dir: t.Annotated[
        Path | None,
        cyclopts.Parameter(help="Directory for the optimization ledger and candidate artifacts"),
    ] = None,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
) -> None:
    """Improve a local capability against a local dataset with stack-aware optimization."""
    from dreadnode.capabilities.capability import Capability
    from dreadnode.optimization import (
        EngineConfig,
        OptimizationConfig,
        ReflectionConfig,
        optimize_anything,
    )
    from dreadnode.optimization.adapters.stack import (
        DEFAULT_SURFACES,
        StackAwareCapabilityAdapter,
    )
    from dreadnode.optimization.stopping import best_score_not_improved, trial_count

    resolved_capability_path = path.expanduser().resolve()
    capability = Capability(resolved_capability_path)
    selected_agent, execution_model = _resolve_improvement_model(
        capability,
        agent_name=agent,
        model=model,
    )
    reflection_lm = reflection_model or execution_model
    proposer_runtime_model = proposer_model or reflection_lm

    scorers = _resolve_scorers(list(scorer))
    resolved_score_name = score_name or (scorers[0].name if len(scorers) == 1 else None)
    if len(scorers) > 1 and resolved_score_name is None:
        raise ValueError(
            "Capability improvement requires --score-name when multiple --scorer values are provided"
        )

    train_rows = _load_improvement_rows(dataset)
    holdout_rows = _load_improvement_rows(holdout_dataset) if holdout_dataset is not None else None
    dataset_input_mapping = _parse_dataset_input_mapping(dataset_input)

    raw_surfaces = surface or list(DEFAULT_SURFACES)
    allowed_surfaces = tuple(raw_surfaces)
    invalid_surfaces = sorted(set(raw_surfaces) - set(DEFAULT_SURFACES))
    if invalid_surfaces:
        raise ValueError(f"Unknown improvement surfaces: {', '.join(invalid_surfaces)}")

    resolved_output_dir = (output_dir or _default_improvement_output_dir(capability.path)).resolve()
    if resolved_output_dir.exists():
        raise FileExistsError(f"Output directory already exists: {resolved_output_dir}")
    resolved_output_dir.mkdir(parents=True, exist_ok=False)

    proposer_agent_instance, proposer_descriptor = _load_proposer_agent(
        proposer_capability=proposer_capability,
        proposer_agent_name=proposer_agent,
        proposer_model=proposer_runtime_model,
    )

    adapter = StackAwareCapabilityAdapter(
        capability=capability,
        model=execution_model,
        agent_name=selected_agent.name,
        allowed_surfaces=t.cast("t.Any", allowed_surfaces),
        dataset=train_rows,
        scorers=scorers,
        score_name=resolved_score_name,
        goal_field=goal_field,
        dataset_input_mapping=dataset_input_mapping,
        name=f"{capability.name} capability improvement",
        objective=objective,
        proposer_agent=proposer_agent_instance,
    )

    baseline_candidate = adapter.seed_candidate()
    baseline_train = _score_candidate(adapter, baseline_candidate)

    holdout_adapter: t.Any = None
    baseline_holdout: dict[str, t.Any] | None = None
    if holdout_rows is not None:
        holdout_adapter = StackAwareCapabilityAdapter(
            capability=capability,
            model=execution_model,
            agent_name=selected_agent.name,
            allowed_surfaces=t.cast("t.Any", allowed_surfaces),
            dataset=holdout_rows,
            scorers=scorers,
            score_name=resolved_score_name,
            goal_field=goal_field,
            dataset_input_mapping=dataset_input_mapping,
            name=f"{capability.name} capability holdout",
        )
        baseline_holdout = _score_candidate(holdout_adapter, baseline_candidate)

    stop_callbacks: list[t.Any] = [trial_count(max_trials)]
    if max_trials_without_improvement > 0:
        stop_callbacks.append(best_score_not_improved(max_trials_without_improvement))

    optimization = optimize_anything(
        adapter=adapter,
        name=f"{capability.name}-improve",
        objective=objective
        or f"Improve {capability.name} capability behavior without regressing holdout performance.",
        trainset=train_rows,
        config=OptimizationConfig(
            engine=EngineConfig(
                run_dir=str((resolved_output_dir / "gepa").resolve()),
                seed=seed,
                max_metric_calls=max_metric_calls,
            ),
            reflection=ReflectionConfig(reflection_lm=reflection_lm),
            stop_callbacks=stop_callbacks,
        ),
    )
    result = asyncio.run(optimization.run())

    raw_best_candidate = result.best_candidate
    best_candidate = (
        dict(raw_best_candidate) if isinstance(raw_best_candidate, dict) else baseline_candidate
    )
    best_train = _score_candidate(adapter, best_candidate)
    best_holdout = (
        _score_candidate(holdout_adapter, best_candidate) if holdout_adapter is not None else None
    )

    winner_candidate, accepted, decision_reason = _select_improvement_winner(
        baseline_candidate=baseline_candidate,
        best_candidate=best_candidate,
        baseline_train_score=float(baseline_train["score"]),
        best_train_score=float(best_train["score"]),
        baseline_holdout_score=(
            float(baseline_holdout["score"]) if baseline_holdout is not None else None
        ),
        best_holdout_score=(float(best_holdout["score"]) if best_holdout is not None else None),
    )

    if best_candidate:
        materialized = adapter.materialize_candidate(best_candidate)
        try:
            target_dir = resolved_output_dir / "best-capability"
            target_dir.mkdir(parents=True, exist_ok=False)
            for child in materialized.root.iterdir():
                destination = target_dir / child.name
                if child.is_dir():
                    shutil.copytree(child, destination)
                else:
                    destination.write_bytes(child.read_bytes())
        finally:
            materialized.cleanup()

    summary = {
        "capability": {
            "path": str(capability.path),
            "name": capability.name,
            "version": capability.version,
            "agent": selected_agent.name,
        },
        "run": {
            "model": execution_model,
            "reflection_model": reflection_lm,
            "proposer_model": proposer_runtime_model,
            "proposer_capability": proposer_descriptor,
            "dataset": str(dataset.expanduser().resolve()),
            "holdout_dataset": (
                str(holdout_dataset.expanduser().resolve()) if holdout_dataset is not None else None
            ),
            "surfaces": list(allowed_surfaces),
            "score_name": resolved_score_name,
            "output_dir": str(resolved_output_dir),
        },
        "baseline": {
            "candidate_hash": _candidate_hash(baseline_candidate),
            "complexity": _candidate_complexity(baseline_candidate),
            "train": baseline_train,
            "holdout": baseline_holdout,
        },
        "best_candidate": {
            "candidate_hash": _candidate_hash(best_candidate),
            "complexity": _candidate_complexity(best_candidate),
            "train": best_train,
            "holdout": best_holdout,
        },
        "decision": {
            "accepted": accepted,
            "reason": decision_reason,
            "winner_hash": _candidate_hash(winner_candidate),
            "winner_matches_baseline": winner_candidate == baseline_candidate,
        },
        "optimization": {
            "backend": result.backend,
            "best_score": result.best_score,
            "best_scores": result.best_scores,
            "train_size": result.train_size,
            "val_size": result.val_size,
            "history_length": len(result.history),
            "metadata": result.metadata,
        },
    }

    _write_json_file(resolved_output_dir / "ledger.json", summary)
    _write_json_file(resolved_output_dir / "baseline-candidate.json", baseline_candidate)
    _write_json_file(resolved_output_dir / "best-candidate.json", best_candidate)
    _write_json_file(resolved_output_dir / "winner-candidate.json", winner_candidate)
    _write_json_file(resolved_output_dir / "history.json", result.history)

    if as_json:
        _print_json(summary)
        return

    console.print(
        f"Improvement run for [cyan]{capability.name}[/cyan] "
        f"[dim](agent={selected_agent.name}, model={execution_model})[/dim]"
    )
    if proposer_descriptor is not None:
        console.print(f"  proposer={proposer_descriptor}")
    else:
        console.print("  proposer=[dim]none (using backend default proposals)[/dim]")
    console.print(
        f"  baseline train={float(baseline_train['score']):.4f} "
        f"best train={float(best_train['score']):.4f}"
    )
    if baseline_holdout is not None and best_holdout is not None:
        console.print(
            f"  baseline holdout={float(baseline_holdout['score']):.4f} "
            f"best holdout={float(best_holdout['score']):.4f}"
        )
    if accepted:
        print_success(f"Accepted candidate: {decision_reason}")
    else:
        print_warning(f"Discarded candidate: {decision_reason}")
    console.print(f"  artifacts: {resolved_output_dir}")


# ---------------------------------------------------------------------------
# validate
# ---------------------------------------------------------------------------


@cli.command(alias="check")
def validate(
    path: Path,
    *,
    strict: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
) -> None:
    """Check that a capability is well-formed before publishing.

    Loads and validates agents, tools, skills, MCP server, and worker
    definitions. Validates a single capability if the path contains
    capability.yaml, otherwise discovers and validates all capability
    subdirectories.

    Args:
        path: Capability directory or parent directory containing
            multiple capabilities.
        strict: Treat warnings as failures (exit code 1).
    """
    from dreadnode.capabilities.capability import Capability

    resolved = path.resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Path not found: {resolved}")

    if (resolved / "capability.yaml").exists():
        dirs = [resolved]
    else:
        dirs = sorted(
            d for d in resolved.iterdir() if d.is_dir() and (d / "capability.yaml").exists()
        )
        if not dirs:
            raise FileNotFoundError(f"No capability.yaml found in {resolved} or its subdirectories")

    errors: list[tuple[str, str]] = []
    warnings: list[str] = []

    for cap_dir in dirs:
        dir_name = cap_dir.name
        try:
            cap = Capability(cap_dir)
            agents = cap.agents
            tools = cap.tools
            mcp = cap.mcp_server_defs
            workers = cap.worker_defs

            health_errors = [h for h in cap.component_health if h.get("status") == "error"]
            # Count loadable skills (one SKILL.md per skill), not manifest path
            # entries — `skills_paths` is a list of search roots and overstates
            # the count, especially when entries fail to parse.
            skill_count = sum(
                1
                for h in cap.component_health
                if h.get("kind") == "skill" and h.get("status") == "ok"
            )

            summary = (
                f"agents={len(agents)}, tools={len(tools)}, "
                f"skills={skill_count}, mcp={len(mcp)}, workers={len(workers)}"
            )

            if health_errors:
                warnings.append(cap.name)
                print_warning(f"{cap.name}@{cap.version} ({summary})", indent=2)
                for h in health_errors:
                    kind = h.get("kind", "?")
                    name = h.get("name", "?")
                    console.print(f"       {kind}:{name}: {h.get('error', 'unknown')}")
            else:
                print_success(f"{cap.name}@{cap.version} ({summary})", indent=2)
        except (ValueError, FileNotFoundError) as exc:
            errors.append((dir_name, str(exc)))
            print_error(f"{dir_name}: {exc}", indent=2)

    total = len(dirs)
    failed = len(errors)
    warned = len(warnings)
    ok_count = total - failed - warned
    console.print(
        f"\nValidated {total}: "
        f"[green]{ok_count} ok[/green], [yellow]{warned} warn[/yellow], [red]{failed} failed[/red]"
    )
    if errors or (strict and warnings):
        raise SystemExit(1)
