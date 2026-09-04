"""Runtime subcommands for the cyclopts CLI."""

import fnmatch
import typing as t
from pathlib import Path

import cyclopts
import yaml

from dreadnode.app.api.client import ConflictError, NotFoundError
from dreadnode.app.cli.args import PlatformScopeArgs
from dreadnode.app.cli.shared import (
    _FLAG_STATE,
    _LABEL_W,
    _collect_cursor_pages,
    _hint,
    _render,
    _render_list,
    _short_id,
    _status_color,
    confirm_destructive,
    console,
    parse_egress_targets,
    print_info,
    print_success,
)
from dreadnode.packaging.egress import merge_targets, normalize_declaration

RuntimeStatus = t.Literal["idle", "running", "paused"]

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


def _ownership_token(payload: dict[str, t.Any]) -> str:
    """Mark a runtime the caller cannot operate.

    Reads are workspace-wide but every mutation is owner-gated (RT-OWN-020,
    RT-OWN-012), so a listing mixes runtimes the caller can drive with ones
    that answer 403. Owning it is the baseline and carries no token; the
    exception is marked, following the session summary's convention.

    ``owned_by_me`` absent means the server predates RT-OWN-022 and has not
    told us either way, which is not the same as "not yours" — say nothing
    rather than mark every row.
    """
    owned = payload.get("owned_by_me")
    if owned is False:
        return " [yellow]read-only[/yellow]"
    return ""


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
        f"{_ownership_token(payload)}"
    )


_RUNTIME_LIST_ROW_FIELDS: tuple[str, ...] = (
    "status",
    "key",
    "project_id",
    "project_key",
    "project_name",
    "owned_by_me",
    "created_by",
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


def _apply_egress_targets(
    config: dict[str, t.Any] | None,
    cli_targets: list[str] | None,
) -> dict[str, t.Any] | None:
    """Merge ``--egress`` targets into ``sandbox.egress.allow`` (`RT-SBX-006`).

    Also validates a ``sandbox.egress`` block loaded from ``runtime.yaml``, so a
    malformed target is named here rather than after a round trip.

    Absent stays absent (`RT-SBX-009`): with no declaration on either side the
    sandbox inherits the operator's floor unchanged, which is not the same as
    an empty allow list restricting it to the platform's own destinations.
    """
    sandbox_raw = (config or {}).get("sandbox")
    if sandbox_raw is not None and not isinstance(sandbox_raw, dict):
        raise TypeError("runtime.yaml sandbox must be a mapping")

    declared = normalize_declaration((sandbox_raw or {}).get("egress"))
    merged = merge_targets(declared, cli_targets)
    if merged is None:
        return config

    updated = dict(config or {})
    sandbox = dict(sandbox_raw or {})
    sandbox["egress"] = {"allow": merged}
    updated["sandbox"] = sandbox
    return updated


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


def _print_started_runtime(payload: dict[str, t.Any]) -> None:
    runtime_label = payload.get("name") or payload.get("key") or payload.get("id", "runtime")
    print_success(f"Started runtime '{runtime_label}'")
    console.print(_summarize_runtime(payload))

    if payload.get("materialization_stale"):
        # start returns the running instance as-is rather than rebuilding it,
        # so config or capability changes made since it was provisioned are
        # not live in it. Applying them costs the instance's state, so it is
        # the user's call, not ours.
        print_info(
            "This instance predates the runtime's current configuration. "
            "Run 'dreadnode runtime reset' then 'start' to apply the changes "
            "(this discards everything in the current instance)."
        )

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

    timing_line = _format_startup_timing(instance.get("startup_timing"))
    if timing_line:
        console.print(f"[dim]Cold start:[/dim] {timing_line}")


def _format_startup_timing(timing: t.Any) -> str | None:
    """One line of where a cold start spent its time, from the API's breakdown.

    Only the phases that were recorded are shown, so an instance started before
    timing existed prints nothing rather than a row of blanks.
    """
    if not isinstance(timing, dict):
        return None
    total = timing.get("total_sec")
    if not isinstance(total, int | float):
        return None
    runtime_raw = timing.get("runtime")
    runtime: dict[str, t.Any] = runtime_raw if isinstance(runtime_raw, dict) else {}
    marks_raw = runtime.get("timings")
    marks: dict[str, t.Any] = marks_raw if isinstance(marks_raw, dict) else {}
    durations_raw = runtime.get("durations")
    durations: dict[str, t.Any] = durations_raw if isinstance(durations_raw, dict) else {}
    install_total = sum(
        v for k, v in durations.items() if k.startswith("install.") and isinstance(v, int | float)
    )
    parts: list[tuple[str, t.Any]] = [
        ("api", timing.get("api_pre_provision_sec")),
        ("provider", timing.get("provider_provision_sec")),
        ("runtime boot", marks.get("serve_entered")),
        ("install", install_total or None),
        ("ready", marks.get("ready")),
        ("detect lag", timing.get("ready_detect_lag_sec")),
    ]
    rendered = [f"{label} {value:.1f}s" for label, value in parts if isinstance(value, int | float)]
    phases_raw = timing.get("phases")
    phases = (
        {k: v for k, v in phases_raw.items() if isinstance(v, int | float)}
        if isinstance(phases_raw, dict)
        else {}
    )
    if phases:
        # The api and provider figures above are totals; name the single
        # platform-side step that cost the most so a slow one is attributable
        # from the terminal.
        slowest = max(phases, key=lambda k: phases[k])
        rendered.append(f"slowest {slowest} {phases[slowest]:.1f}s")
    return f"{total:.1f}s" + (f" ({', '.join(rendered)})" if rendered else "")


# ---------------------------------------------------------------------------
# list / get
# ---------------------------------------------------------------------------


@cli.command(name="list", alias="ls")
def list_(
    *,
    state: t.Annotated[
        list[RuntimeStatus] | None,
        cyclopts.Parameter(name=_FLAG_STATE, negative_iterable=()),
    ] = None,
    project_id: t.Annotated[str | None, cyclopts.Parameter(name="--project-id")] = None,
    mine: t.Annotated[bool, cyclopts.Parameter(name="--mine", negative=())] = False,
    limit: int = 50,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """List runtimes in your workspace.

    Runtimes you do not own are listed too — reads span the workspace — and are
    marked ``read-only``, since starting, pausing, resuming or resetting one
    answers 403. Use ``--mine`` to leave them out.

    Args:
        state: Filter by runtime status (``idle``, ``running``, ``paused``).
            Repeatable; values combine with OR. Also accepts ``--status``.
        project_id: Only show runtimes belonging to this project UUID.
        mine: Only show runtimes you own, and can therefore operate.
        limit: Maximum results to show. Server pages are walked internally.
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    items = _collect_cursor_pages(
        lambda cursor, page_size: api.list_runtimes(
            profile.org_key,
            profile.workspace_key,
            state=list(state) if state else None,
            project_id=project_id,
            owner="me" if mine else None,
            limit=page_size,
            cursor=cursor,
        ),
        limit=limit,
    )
    _render_list(
        {"items": items},
        as_json=as_json,
        summary=_summarize_runtime,
        empty_msg="No runtimes found",
        fields=_RUNTIME_LIST_ROW_FIELDS,
    )
    if items and not as_json:
        _hint("dn runtime get <runtime-id>")


@cli.command()
def get(
    runtime_id: t.Annotated[str, cyclopts.Parameter(name="runtime-id")],
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Get details of a runtime.

    Args:
        runtime_id: Runtime key or UUID, as shown by `dn runtime list`.
        as_json: Output as JSON.
    """
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
    egress: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(
            name="--egress",
            help=(
                "Outbound destination this runtime's sandbox may reach "
                "(e.g. --egress target.example.com, --egress '*.internal.corp', "
                "--egress 10.20.0.0/16; repeatable). Adds to any "
                "sandbox.egress.allow from --file. A declaration can only "
                "narrow what the deployment already permits, and declaring "
                "anything restricts the sandbox to what is named plus the "
                "platform destinations the platform derives. Pass "
                "--empty-egress to declare a scope that names nothing, "
                "restricting the sandbox to the platform destinations alone."
            ),
        ),
    ] = None,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Ensure a runtime exists for a project or the workspace default project.

    Idempotent — re-running against an existing runtime returns it unchanged.
    Re-running with a *different* config is a conflict, not an update.

    Args:
        project_ref: Project key or UUID. Defaults to the active project scope,
            then the workspace default project.
        key: Runtime key. Required with --name when no project is resolved.
        name: Runtime display name. Required with --key when no project is resolved.
        description: Optional runtime description.
        file: Load runtime.yaml from a file or directory.
        egress: Outbound destination this runtime's sandbox may reach, as an
            FQDN, a '*.suffix' wildcard, an IP, or a CIDR (repeatable). Adds to
            any `sandbox.egress.allow` from --file. Narrowing only, so it needs
            no permission beyond owning the runtime.
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    manifest_identity: dict[str, t.Any] = {}
    manifest_config: dict[str, t.Any] | None = None
    if file is not None:
        manifest_identity, manifest_config = _split_runtime_manifest(api, file)
    manifest_config = _apply_egress_targets(manifest_config, parse_egress_targets(egress))

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

    try:
        payload = api.create_runtime(
            profile.org_key,
            profile.workspace_key,
            resolved_project,
            **create_kwargs,
        )
    except ConflictError as exc:
        # The runtime exists with a different configuration. Create is ensure,
        # not update, so say where updates go rather than leaving the user
        # to re-run the same command.
        runtime_ref = resolved_key or "<runtime-id>"
        raise ConflictError(
            f"{exc} To change a runtime's configuration, run "
            f"`dn runtime config-set {runtime_ref} --egress <target>` or "
            f"`dn runtime config-set {runtime_ref} --file runtime.yaml`."
        ) from exc
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
    _hint(f"dn runtime start {payload.get('key') or payload.get('id', '<runtime-id>')}")


@cli.command()
def start(
    target: str | None = None,
    *,
    runtime_id: t.Annotated[str | None, cyclopts.Parameter(name="--runtime-id")] = None,
    key: str | None = None,
    name: str | None = None,
    description: str | None = None,
    file: t.Annotated[Path | None, cyclopts.Parameter(name="--file")] = None,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Start a runtime, creating it first when the target flow requires it.

    A cold start provisions a sandbox and can take a couple of minutes. Every
    successful call returns the runtime's credential; retry the command
    if its response is lost.

    Args:
        target: Runtime key/UUID, or project key/UUID. Resolved as a runtime
            first. Defaults to the active project scope.
        runtime_id: Start a specific runtime by key or UUID. Mutually exclusive
            with <target>.
        key: Runtime key to ensure before starting.
        name: Runtime name to ensure before starting.
        description: Optional runtime description when ensuring a runtime.
        file: Load runtime.yaml from a file or directory.
        as_json: Output as JSON.
    """
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
    if runtime_target is None and target:
        # The platform resolves a runtime key or UUID on this path, so probe it
        # as a runtime first and fall back to treating <target> as a project.
        # Previously this was gated on the target looking like a UUID, which
        # meant a runtime key only ever started by accident — via the project
        # branch below, and only when the project happened to share its name.
        try:
            api.get_runtime(profile.org_key, profile.workspace_key, target)
        except NotFoundError:
            runtime_target = None
        else:
            runtime_target = target

    if runtime_target is not None:
        payload = api.start_runtime(
            profile.org_key,
            profile.workspace_key,
            runtime_target,
        )
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

    payload = api.start_runtime(
        profile.org_key,
        profile.workspace_key,
        runtime_to_start,
    )
    if as_json:
        _render(payload, as_json=True, summary=_summarize_runtime)
        return
    _print_started_runtime(payload)


# ---------------------------------------------------------------------------
# lifecycle: pause / resume / keepalive / reset
# ---------------------------------------------------------------------------


def _print_lifecycle_result(runtime_id: str, verb: str, color: str) -> None:
    console.print(f"  {_short_id(runtime_id)}  [{color}]{verb}[/{color}]")


@cli.command()
def pause(
    runtime_id: t.Annotated[str, cyclopts.Parameter(name="runtime-id")],
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Pause a runtime's sandbox, preserving its state.

    Args:
        runtime_id: Runtime key or UUID, as shown by `dn runtime list`.
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    payload = api.pause_runtime(profile.org_key, profile.workspace_key, runtime_id)
    if as_json:
        _render(payload, as_json=True, summary=_summarize_runtime)
        return
    _print_lifecycle_result(str(payload.get("id", runtime_id)), "paused", "yellow")


@cli.command()
def resume(
    runtime_id: t.Annotated[str, cyclopts.Parameter(name="runtime-id")],
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Resume a paused runtime's sandbox.

    Resuming does not return an access token. Run `dn runtime start` afterward
    when the credential is needed.

    Args:
        runtime_id: Runtime key or UUID, as shown by `dn runtime list`.
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    payload = api.resume_runtime(profile.org_key, profile.workspace_key, runtime_id)
    if as_json:
        _render(payload, as_json=True, summary=_summarize_runtime)
        return
    _print_lifecycle_result(str(payload.get("id", runtime_id)), "resumed", "green")


@cli.command()
def keepalive(
    runtime_id: t.Annotated[str, cyclopts.Parameter(name="runtime-id")],
    *,
    extend_seconds: t.Annotated[int, cyclopts.Parameter(name="--extend-seconds")] = 300,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Push back a running runtime's expiry.

    Args:
        runtime_id: Runtime key or UUID, as shown by `dn runtime list`.
        extend_seconds: Seconds to extend the runtime's expiry by.
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    payload = api.keepalive_runtime(
        profile.org_key,
        profile.workspace_key,
        runtime_id,
        extend_seconds=extend_seconds,
    )
    if as_json:
        _render(payload, as_json=True, summary=lambda p: str(p))
        return
    expires_at = payload.get("expires_at") if isinstance(payload, dict) else None
    suffix = f" [dim]until {expires_at}[/dim]" if expires_at else ""
    console.print(f"  {_short_id(runtime_id)}  [green]extended[/green]{suffix}")


@cli.command()
def reset(
    runtime_id: t.Annotated[str, cyclopts.Parameter(name="runtime-id")],
    *,
    yes: t.Annotated[bool, cyclopts.Parameter(name="--yes", alias="-y", negative=())] = False,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Discard a runtime's sandbox, returning the runtime to idle.

    The runtime, its configuration, and its capability bindings survive; only
    the compute instance and everything inside it is destroyed. This is how a
    configuration change is applied to a running runtime — `start` never
    rebuilds implicitly.

    Args:
        runtime_id: Runtime key or UUID, as shown by `dn runtime list`.
        yes: Skip the confirmation prompt.
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    payload = api.get_runtime(profile.org_key, profile.workspace_key, runtime_id)
    label = payload.get("name") or payload.get("key") or _short_id(runtime_id)

    if not confirm_destructive(
        f"Reset runtime '{label}'? This destroys the running sandbox and everything inside it.",
        yes=yes,
    ):
        console.print("[dim]Aborted[/dim]")
        return

    result = api.reset_runtime(profile.org_key, profile.workspace_key, runtime_id)
    if as_json:
        _render(result, as_json=True, summary=_summarize_runtime)
        return
    _print_lifecycle_result(str(result.get("id", runtime_id)), "reset", "red")
    _hint(f"dn runtime start {runtime_id}")


# ---------------------------------------------------------------------------
# Durable configuration (RT-API-023 / RT-API-024)
# ---------------------------------------------------------------------------


def _summarize_runtime_config(payload: dict[str, t.Any]) -> str:
    config = payload.get("config") or {}
    sandbox = config.get("sandbox") or {}
    egress = sandbox.get("egress")

    if egress is None:
        # RT-SBX-009: absent is not empty. Say which one this is, because the
        # difference decides whether the sandbox inherits the deployment's
        # floor or is restricted to the platform's own destinations.
        egress_line = "[dim]inherits the deployment's floor[/dim]"
    else:
        allowed = egress.get("allow") or []
        egress_line = (
            ", ".join(str(target) for target in allowed)
            if allowed
            else "[dim]declared, names nothing (platform destinations only)[/dim]"
        )

    capabilities = config.get("capabilities") or []
    return "\n".join(
        [
            f"[dim]{'runtime':<{_LABEL_W}}[/dim]{payload.get('runtime_id', 'unknown')}",
            f"[dim]{'version':<{_LABEL_W}}[/dim]{config.get('version', 'unknown')}",
            f"[dim]{'capabilities':<{_LABEL_W}}[/dim]{len(capabilities)}",
            f"[dim]{'egress':<{_LABEL_W}}[/dim]{egress_line}",
            f"[dim]{'digest':<{_LABEL_W}}[/dim]{payload.get('config_digest', 'unknown')}",
        ]
    )


@cli.command(name="config-get", alias="config")
def config_get(
    runtime_id: t.Annotated[str, cyclopts.Parameter(name="runtime-id")],
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Show a runtime's durable configuration.

    Workspace read access is enough to read a config; only the owner may
    replace one. Use --json for the full document — the summary shows the
    fields with a CLI surface.

    Args:
        runtime_id: Runtime key or UUID, as shown by `dn runtime list`.
        as_json: Output as JSON.
    """
    api, profile = platform.connect()
    payload = api.get_runtime_config(profile.org_key, profile.workspace_key, runtime_id)
    _render(payload, as_json=as_json, summary=_summarize_runtime_config)
    if not as_json:
        _hint(f"dn runtime config-set {runtime_id} --egress <target>")


@cli.command(name="config-set")
def config_set(
    runtime_id: t.Annotated[str, cyclopts.Parameter(name="runtime-id")],
    *,
    file: t.Annotated[
        Path | None,
        cyclopts.Parameter(
            name="--file",
            help=(
                "Replace the whole configuration with this runtime.yaml. "
                "Wholesale, not a merge: a field the file omits is reset to "
                "its default. Without --file the stored configuration is "
                "edited in place and every other field is preserved."
            ),
        ),
    ] = None,
    egress: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(
            name="--egress",
            help=(
                "Outbound destination this runtime's sandbox may reach "
                "(e.g. --egress target.example.com, --egress '*.internal.corp', "
                "--egress 10.20.0.0/16; repeatable). Adds to the scope already "
                "stored, or to --file's when given. Pass --empty-egress to "
                "declare a scope that names nothing, restricting the sandbox "
                "to the platform destinations alone."
            ),
        ),
    ] = None,
    yes: t.Annotated[bool, cyclopts.Parameter(name="--yes", alias="-y", negative=())] = False,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Replace a runtime's durable configuration.

    Only the runtime's owner may call this, and it does not alter an already
    running sandbox — the new configuration applies from the next start.

    A narrowing egress declaration needs no permission beyond owning the
    runtime, and is re-checked against the deployment's egress floor at start,
    so a target the floor denies fails the start naming the target rather than
    starting without it.

    Args:
        runtime_id: Runtime key or UUID, as shown by `dn runtime list`.
        file: Replace the whole configuration with this runtime.yaml. Wholesale,
            not a merge — a field the file omits is reset to its default.
        egress: Outbound destination this runtime's sandbox may reach, as an
            FQDN, a '*.suffix' wildcard, an IP, or a CIDR (repeatable).
        yes: Skip the confirmation prompt when replacing wholesale with --file.
        as_json: Output as JSON.
    """
    if file is None and egress is None:
        raise ValueError(
            "dn runtime config-set requires --file or --egress. "
            "Run `dn runtime config-get <runtime-id>` to see the current configuration."
        )

    api, profile = platform.connect()

    if file is not None:
        manifest_identity, base = _split_runtime_manifest(api, file)
        if manifest_identity:
            # Identity is not part of the configuration document, so silently
            # dropping these would look like they had been applied.
            raise ValueError(
                "runtime.yaml passed to config-set may not carry identity fields: "
                + ", ".join(sorted(manifest_identity))
                + ". Set those with `dn runtime create`."
            )
        base = base or {}
        if not confirm_destructive(
            f"Replace the configuration of runtime '{runtime_id}' wholesale? "
            "Fields absent from the file are reset to their defaults.",
            yes=yes,
        ):
            print_info("Aborted")
            return
    else:
        current = api.get_runtime_config(profile.org_key, profile.workspace_key, runtime_id)
        base = dict(current.get("config") or {})

    updated = _apply_egress_targets(base, parse_egress_targets(egress)) or {}
    payload = api.update_runtime_config(
        profile.org_key,
        profile.workspace_key,
        runtime_id,
        updated,
    )

    if as_json:
        _render(payload, as_json=True, summary=_summarize_runtime_config)
        return
    print_success(f"Updated configuration for runtime '{runtime_id}'")
    console.print(_summarize_runtime_config(payload))
    _hint(f"dn runtime start {runtime_id}")
