"""Runtime subcommands for the cyclopts CLI."""

import fnmatch
import typing as t
from pathlib import Path
from uuid import UUID

import cyclopts
import yaml

from dreadnode.app.cli.args import PlatformScopeArgs
from dreadnode.app.cli.shared import (
    _render,
    _render_list,
    _status_color,
    console,
    print_info,
    print_success,
)

cli = cyclopts.App(name="runtime", help="Manage agent runtime environments.")

_RUNTIME_CONFIG_KEYS = {
    "version",
    "capabilities",
    "defaults",
    "secrets",
    "build",
    "resources",
    "sandbox",
    "runtime_server",
    "metadata",
}
_RUNTIME_IDENTITY_KEYS = {"project", "key", "name", "description"}


def _summarize_runtime(payload: dict[str, t.Any]) -> str:
    runtime_id = payload.get("id", "unknown")
    status = payload.get("status", "unknown")
    name = payload.get("name") or payload.get("key") or "unnamed-runtime"
    key = payload.get("key")
    project = (
        payload.get("project_key")
        or payload.get("project_name")
        or payload.get("project_id", "unknown")
    )
    color = _status_color(status)
    key_suffix = f" [dim]({key})[/dim]" if isinstance(key, str) and key and key != name else ""
    return (
        f"[dim]{runtime_id}[/dim] [{color}]{status}[/{color}] "
        f"[bold]{name}[/bold]{key_suffix} [cyan]{project}[/cyan]"
    )


_RUNTIME_LIST_ROW_FIELDS: tuple[str, ...] = (
    "status",
    "key",
    "project_id",
    "project_key",
    "project_name",
    "created_at",
    "updated_at",
)


def _is_secret_selector_pattern(selector: str) -> bool:
    return any(char in selector for char in "*?[")


def _field_value(item: t.Any, key: str) -> t.Any:
    if isinstance(item, dict):
        return item.get(key)
    return getattr(item, key, None)


def _resolve_secret_ids(api: t.Any, selectors: list[str]) -> list[str] | None:
    if not selectors:
        return None

    secrets_response = api.list_secrets()
    raw_secrets = (
        secrets_response.get("secrets", [])
        if isinstance(secrets_response, dict)
        else getattr(secrets_response, "secrets", [])
    )

    ordered_secrets: list[tuple[str, str]] = []
    secrets_by_name: dict[str, str] = {}
    for secret in raw_secrets:
        name = _field_value(secret, "name")
        secret_id = _field_value(secret, "id")
        if not isinstance(name, str) or not isinstance(secret_id, str):
            continue
        normalized_name = name.upper()
        ordered_secrets.append((normalized_name, secret_id))
        secrets_by_name[normalized_name] = secret_id

    resolved_ids: list[str] = []
    seen_ids: set[str] = set()
    missing_exact: list[str] = []

    for raw_selector in selectors:
        selector = raw_selector.strip().upper()
        if not selector:
            continue

        if _is_secret_selector_pattern(selector):
            for name, secret_id in ordered_secrets:
                if not fnmatch.fnmatchcase(name, selector) or secret_id in seen_ids:
                    continue
                resolved_ids.append(secret_id)
                seen_ids.add(secret_id)
            continue

        secret_id = secrets_by_name.get(selector)
        if secret_id is None:
            missing_exact.append(selector)
            continue
        if secret_id in seen_ids:
            continue
        resolved_ids.append(secret_id)
        seen_ids.add(secret_id)

    if missing_exact:
        if len(missing_exact) == 1:
            raise ValueError(f"Secret not found: {missing_exact[0]}")
        raise ValueError("Secrets not found: " + ", ".join(sorted(missing_exact)))

    return resolved_ids or None


def _load_runtime_manifest(path: Path) -> dict[str, t.Any]:
    resolved = path.expanduser()
    if resolved.is_dir():
        resolved = resolved / "runtime.yaml"
    if not resolved.exists():
        raise FileNotFoundError(f"No runtime.yaml found at {resolved}")

    parsed = yaml.safe_load(resolved.read_text())
    if parsed is None:
        return {}
    if not isinstance(parsed, dict):
        raise TypeError("runtime.yaml must contain a YAML mapping")
    return dict(parsed)


def _split_runtime_manifest(
    api: t.Any,
    path: Path,
) -> tuple[dict[str, t.Any], dict[str, t.Any] | None]:
    manifest = _load_runtime_manifest(path)

    identity: dict[str, t.Any] = {}
    nested_identity = manifest.pop("identity", None)
    if nested_identity is not None:
        if not isinstance(nested_identity, dict):
            raise TypeError("runtime.yaml identity must be a mapping")
        unexpected_identity = sorted(set(nested_identity) - _RUNTIME_IDENTITY_KEYS)
        if unexpected_identity:
            raise ValueError(
                "runtime.yaml identity has unexpected fields: " + ", ".join(unexpected_identity)
            )
        identity.update(nested_identity)

    for key in _RUNTIME_IDENTITY_KEYS:
        if key in manifest:
            if key in identity:
                raise ValueError(f"runtime.yaml may specify '{key}' only once")
            identity[key] = manifest.pop(key)

    config = {key: manifest.pop(key) for key in list(_RUNTIME_CONFIG_KEYS) if key in manifest}
    if manifest:
        raise ValueError("runtime.yaml contains unexpected fields: " + ", ".join(sorted(manifest)))

    secrets = config.get("secrets")
    if isinstance(secrets, dict) and "selectors" in secrets:
        selectors = secrets.get("selectors")
        if not isinstance(selectors, list) or not all(
            isinstance(selector, str) for selector in selectors
        ):
            raise TypeError("runtime.yaml secrets.selectors must be a list of strings")
        if "secret_ids" in secrets:
            raise ValueError(
                "runtime.yaml secrets may specify only one of 'selectors' or 'secret_ids'"
            )
        resolved_secret_ids = _resolve_secret_ids(api, [str(selector) for selector in selectors])
        config["secrets"] = {"secret_ids": resolved_secret_ids or []}

    return identity, (config or None)


def _coalesce_manifest_value(
    explicit: str | None,
    manifest_identity: dict[str, t.Any],
    field_name: str,
) -> str | None:
    if explicit is not None:
        return explicit
    value = manifest_identity.get(field_name)
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError(f"runtime.yaml {field_name} must be a string")
    return value


def _is_uuid_like(value: str) -> bool:
    try:
        UUID(value)
    except ValueError:
        return False
    return True


def _print_started_runtime(payload: dict[str, t.Any]) -> None:
    runtime_label = payload.get("name") or payload.get("key") or payload.get("id", "runtime")
    print_success(f"Started runtime '{runtime_label}'")
    console.print(_summarize_runtime(payload))

    instance = payload.get("instance") if isinstance(payload.get("instance"), dict) else None
    if instance is None:
        return

    sandbox_url = instance.get("sandbox_url")
    provider_sandbox_id = instance.get("provider_sandbox_id")
    if sandbox_url:
        console.print(f"[dim]URL:[/dim] {sandbox_url}")
    elif provider_sandbox_id:
        console.print(f"[dim]Sandbox:[/dim] {provider_sandbox_id}")

    sandbox_token = payload.get("sandbox_token")
    if sandbox_token:
        console.print(f"[dim]Token:[/dim] {sandbox_token}")


@cli.command(name="list", alias="ls")
def list_(
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """List available runtimes."""
    api, profile = platform.connect()
    payload = api.list_runtimes(profile.org_key, profile.workspace_key)
    _render_list(
        payload,
        as_json=as_json,
        summary=_summarize_runtime,
        empty_msg="No runtimes found",
        fields=_RUNTIME_LIST_ROW_FIELDS,
    )


@cli.command()
def get(
    runtime_id: str,
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Get details of a runtime."""
    api, profile = platform.connect()
    payload = api.get_runtime(profile.org_key, profile.workspace_key, runtime_id)
    _render(payload, as_json=as_json, summary=_summarize_runtime)


@cli.command(alias="new")
def create(
    project_ref: t.Annotated[
        str | None,
        cyclopts.Parameter(
            help="Project key or UUID. Defaults to the active project scope, then workspace default.",
        ),
    ] = None,
    *,
    key: t.Annotated[
        str | None,
        cyclopts.Parameter(help="Runtime key. Required with --name when no project is resolved."),
    ] = None,
    name: t.Annotated[
        str | None,
        cyclopts.Parameter(
            help="Runtime display name. Required with --key when no project is resolved."
        ),
    ] = None,
    description: t.Annotated[
        str | None,
        cyclopts.Parameter(help="Optional runtime description."),
    ] = None,
    file: t.Annotated[
        Path | None,
        cyclopts.Parameter(name="--file", help="Load runtime.yaml from a file or directory."),
    ] = None,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Ensure a runtime exists for a project or the workspace default project."""
    api, profile = platform.connect()
    manifest_identity: dict[str, t.Any] = {}
    manifest_config: dict[str, t.Any] | None = None
    if file is not None:
        manifest_identity, manifest_config = _split_runtime_manifest(api, file)

    resolved_project = (
        project_ref
        or _coalesce_manifest_value(None, manifest_identity, "project")
        or profile.project_key
    )
    resolved_key = _coalesce_manifest_value(key, manifest_identity, "key")
    resolved_name = _coalesce_manifest_value(name, manifest_identity, "name")
    resolved_description = _coalesce_manifest_value(
        description,
        manifest_identity,
        "description",
    )
    if resolved_project is None and (resolved_key is None or resolved_name is None):
        raise ValueError(
            "Pass <project> or set --project in your platform scope, or provide both --key and --name."
        )

    create_kwargs: dict[str, t.Any] = {}
    if resolved_key is not None:
        create_kwargs["key"] = resolved_key
    if resolved_name is not None:
        create_kwargs["name"] = resolved_name
    if resolved_description is not None:
        create_kwargs["description"] = resolved_description
    if manifest_config is not None:
        create_kwargs["config"] = manifest_config

    payload = api.create_runtime(
        profile.org_key,
        profile.workspace_key,
        resolved_project,
        **create_kwargs,
    )
    if as_json:
        _render(payload, as_json=True, summary=_summarize_runtime)
        return

    runtime_label = payload.get("name") or payload.get("key") or payload.get("id", "runtime")
    project = payload.get("project_key") or payload.get("project_name") or resolved_project
    if payload.get("created"):
        if project:
            print_success(f"Created runtime '{runtime_label}' in project '{project}'")
        else:
            print_success(f"Created runtime '{runtime_label}'")
    elif project:
        print_info(f"Runtime '{runtime_label}' already exists in project '{project}'")
    else:
        print_info(f"Runtime '{runtime_label}' already exists")
    console.print(_summarize_runtime(payload))


@cli.command()
def start(
    target: t.Annotated[
        str | None,
        cyclopts.Parameter(
            help="Runtime UUID or project key/UUID. Defaults to the active project scope.",
        ),
    ] = None,
    *,
    runtime_id: t.Annotated[
        str | None,
        cyclopts.Parameter(name="--runtime-id", help="Start a specific runtime by UUID."),
    ] = None,
    key: t.Annotated[
        str | None,
        cyclopts.Parameter(help="Runtime key to ensure before starting."),
    ] = None,
    name: t.Annotated[
        str | None,
        cyclopts.Parameter(help="Runtime name to ensure before starting."),
    ] = None,
    description: t.Annotated[
        str | None,
        cyclopts.Parameter(help="Optional runtime description when ensuring a runtime."),
    ] = None,
    file: t.Annotated[
        Path | None,
        cyclopts.Parameter(name="--file", help="Load runtime.yaml from a file or directory."),
    ] = None,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Start a runtime, creating it first when the target flow requires it."""
    api, profile = platform.connect()
    manifest_identity: dict[str, t.Any] = {}
    manifest_config: dict[str, t.Any] | None = None
    if file is not None:
        manifest_identity, manifest_config = _split_runtime_manifest(api, file)

    if runtime_id is not None and target is not None:
        raise ValueError("Pass either <target> or --runtime-id, not both.")

    resolved_key = _coalesce_manifest_value(key, manifest_identity, "key")
    resolved_name = _coalesce_manifest_value(name, manifest_identity, "name")
    resolved_description = _coalesce_manifest_value(
        description,
        manifest_identity,
        "description",
    )
    runtime_target = runtime_id
    if runtime_target is None and target and _is_uuid_like(target):
        try:
            api.get_runtime(profile.org_key, profile.workspace_key, target)
        except Exception:
            runtime_target = None
        else:
            runtime_target = target

    if runtime_target is not None:
        payload = api.start_runtime(profile.org_key, profile.workspace_key, runtime_target)
        if as_json:
            _render(payload, as_json=True, summary=_summarize_runtime)
            return
        _print_started_runtime(payload)
        return

    resolved_project = (
        target
        or _coalesce_manifest_value(None, manifest_identity, "project")
        or profile.project_key
    )
    runtime_to_start: str | None = None
    if resolved_key is not None or resolved_name is not None or manifest_config is not None:
        if resolved_project is None and (resolved_key is None or resolved_name is None):
            raise ValueError(
                "Pass a project or provide both --key and --name when starting via a runtime config."
            )
        ensure_kwargs: dict[str, t.Any] = {}
        if resolved_key is not None:
            ensure_kwargs["key"] = resolved_key
        if resolved_name is not None:
            ensure_kwargs["name"] = resolved_name
        if resolved_description is not None:
            ensure_kwargs["description"] = resolved_description
        if manifest_config is not None:
            ensure_kwargs["config"] = manifest_config
        created = api.create_runtime(
            profile.org_key,
            profile.workspace_key,
            resolved_project,
            **ensure_kwargs,
        )
        runtime_to_start = t.cast("str", created["id"])
    else:
        if resolved_project is None:
            raise ValueError(
                "Pass a runtime id or project, or set --project in your platform scope."
            )
        project = api.get_project(profile.org_key, profile.workspace_key, resolved_project)
        project_id = _field_value(project, "id")
        if not isinstance(project_id, str) or not project_id:
            raise ValueError(f"Project '{resolved_project}' did not include an id")
        runtimes_payload = api.list_runtimes(
            profile.org_key,
            profile.workspace_key,
            project_id=project_id,
            limit=100,
        )
        items = runtimes_payload.get("items", [])
        if len(items) == 0:
            created = api.create_runtime(
                profile.org_key,
                profile.workspace_key,
                resolved_project,
            )
            runtime_to_start = t.cast("str", created["id"])
        elif len(items) == 1:
            runtime_to_start = t.cast("str", items[0]["id"])
        else:
            raise ValueError(
                "Project has multiple runtimes. Pass --runtime-id or ensure a specific runtime with --key/--name."
            )

    payload = api.start_runtime(profile.org_key, profile.workspace_key, runtime_to_start)
    if as_json:
        _render(payload, as_json=True, summary=_summarize_runtime)
        return
    _print_started_runtime(payload)
