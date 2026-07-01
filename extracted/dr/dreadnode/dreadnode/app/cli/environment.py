"""Task environment subcommands for the cyclopts CLI.

Six commands matching the environments API surface: create (provision), list,
get, wait (block on terminal state), delete (tear down), exec
(token-authenticated command run).
"""

import os
import time
import typing as t

import cyclopts

from dreadnode.app.cli.args import PlatformScopeArgs
from dreadnode.app.cli.shared import (
    _FLAG_STATE,
    ArtifactRef,
    _print_json,
    _render_list,
    _status_color,
    confirm_destructive,
    console,
    print_error,
    print_success,
)

cli = cyclopts.App(
    name="environment",
    help="Provision and tear down task environments (sandboxed task instances).",
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _parse_kv_pairs(values: list[str] | None, *, flag: str) -> dict[str, t.Any]:
    """Parse ``key=value`` flag repeats into a dict.

    JSON-decodes the value if it parses cleanly, otherwise keeps it as a string.
    """
    if not values:
        return {}
    import json

    out: dict[str, t.Any] = {}
    for raw in values:
        if "=" not in raw:
            raise ValueError(f"{flag} expects KEY=VALUE, got: {raw!r}")
        key, _, value = raw.partition("=")
        key = key.strip()
        if not key:
            raise ValueError(f"{flag} key must not be empty: {raw!r}")
        try:
            out[key] = json.loads(value)
        except json.JSONDecodeError:
            out[key] = value
    return out


def _format_preview(text: str | None, *, limit: int = 200) -> str:
    if not text:
        return "[dim](none)[/dim]"
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[:limit].rstrip() + "…"


def _summarize_environment(payload: dict[str, t.Any]) -> str:
    """One-line summary header; use alongside the detail panel."""
    env_id = str(payload.get("id", "?"))
    task_ref = payload.get("task_ref") or "?"
    state = str(payload.get("state", "?"))
    return (
        f"[cyan]{env_id}[/cyan]  "
        f"[bold]{task_ref}[/bold]  "
        f"[{_status_color(state)}]{state}[/{_status_color(state)}]"
    )


_ENVIRONMENT_LIST_ROW_FIELDS: tuple[str, ...] = (
    "task_ref",
    "state",
    "project_id",
    "project_key",
    "created_at",
    "expires_at",
    "updated_at",
)


def _print_environment_detail(payload: dict[str, t.Any]) -> None:
    """Rich multi-line view for `env get` and post-create output."""
    console.print(_summarize_environment(payload))
    created_at = payload.get("created_at")
    expires_at = payload.get("expires_at")
    if created_at or expires_at:
        parts = []
        if created_at:
            parts.append(f"created={created_at}")
        if expires_at:
            parts.append(f"expires={expires_at}")
        console.print(f"  [dim]{' · '.join(parts)}[/dim]")

    service_urls = payload.get("service_urls") or {}
    if isinstance(service_urls, dict) and service_urls:
        console.print()
        console.print("[bold]Service URLs[/bold]")
        for service, meta in service_urls.items():
            if not isinstance(meta, dict):
                continue
            url = meta.get("url") or meta.get("host") or "(no url)"
            port = meta.get("port")
            port_suffix = f" [dim]:{port}[/dim]" if port is not None else ""
            console.print(f"  [cyan]{service}[/cyan]  {url}{port_suffix}")

    instruction = payload.get("instruction")
    if instruction:
        console.print()
        console.print("[bold]Instruction template[/bold] [dim](raw — render client-side)[/dim]")
        console.print(f"  [dim]{_format_preview(instruction, limit=400)}[/dim]")

    token = payload.get("execute_token")
    if isinstance(token, str) and token:
        console.print()
        console.print("[bold]Execute token[/bold] [dim](not recoverable — copy now)[/dim]")
        console.print(f"  [cyan]{token}[/cyan]")


# ---------------------------------------------------------------------------
# create
# ---------------------------------------------------------------------------


@cli.command()
def create(
    task_ref: str,
    *,
    input: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(
            name="--input",
            help=(
                "Template variable binding (KEY=VALUE, e.g. --input target=https://example.com; "
                "JSON value allowed, repeatable)."
            ),
            negative_iterable=(),
        ),
    ] = None,
    secret: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(
            name="--secret",
            help="Secret id to inject into the sandbox (repeatable).",
            negative_iterable=(),
        ),
    ] = None,
    project_id: t.Annotated[
        str | None,
        cyclopts.Parameter(help="Optional explicit project UUID."),
    ] = None,
    timeout_sec: t.Annotated[
        int | None,
        cyclopts.Parameter(help="Sandbox lifetime in seconds (capped by org max)."),
    ] = None,
    wait: t.Annotated[
        bool,
        cyclopts.Parameter(
            name="--wait",
            help="Poll until the environment reaches a terminal state (ready/failed/torn_down).",
            negative=(),
        ),
    ] = False,
    wait_timeout_sec: t.Annotated[
        float,
        cyclopts.Parameter(
            name=("--wait-timeout-sec", "--wait-timeout"),
            help="Max seconds to wait for --wait (default 300).",
            validator=cyclopts.validators.Number(gt=0),
        ),
    ] = 300.0,
    poll_interval_sec: t.Annotated[
        float,
        cyclopts.Parameter(
            name=("--poll-interval-sec", "--poll-interval"),
            help="Seconds between status polls under --wait.",
            validator=cyclopts.validators.Number(gt=0),
        ),
    ] = 2.0,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Provision a task environment.

    ``task_ref`` follows the canonical ``[org/]name[@version]`` format:

    - ``my-task``              — latest visible version
    - ``my-task@1.0.0``        — exact version
    - ``acme/my-task``         — cross-org (must be public or owned by you)
    - ``acme/my-task@1.0.0``   — cross-org exact version

    Use ``--input name=value`` repeatedly to bind template variables (values
    are JSON-decoded when possible, falling back to plain strings).

    With ``--wait``, poll until the environment is ``ready`` (or reaches a
    terminal failure/torn-down state). Without it, return as soon as the
    server accepts the request.
    """
    # Validate ref structure early so bad input fails with a clean message
    # instead of a server-side 404.
    api, profile = platform.connect()
    ArtifactRef.parse(task_ref, profile.org_key)

    inputs = _parse_kv_pairs(input, flag="--input")

    body: dict[str, t.Any] = {"task_ref": task_ref}
    if project_id is not None:
        body["project_id"] = project_id
    if inputs:
        body["inputs"] = inputs
    if secret:
        body["secret_ids"] = list(secret)
    if timeout_sec is not None:
        body["timeout_sec"] = timeout_sec

    payload = api.create_environment(profile.org_key, profile.workspace_key, body)
    env_id = str(payload.get("id", ""))

    if wait and env_id:
        state = _wait_for_ready(
            api,
            profile.org_key,
            profile.workspace_key,
            env_id,
            timeout_sec=wait_timeout_sec,
            poll_interval=poll_interval_sec,
        )
        # Refresh the full payload so service_urls + instruction reflect the
        # post-ready state. Preserve execute_token — it's only returned on the
        # original provision response and is not recoverable later.
        execute_token = payload.get("execute_token")
        payload = api.get_environment(profile.org_key, profile.workspace_key, env_id)
        if execute_token:
            payload["execute_token"] = execute_token
        if state != "ready":
            if as_json:
                _print_json(payload)
            else:
                _print_environment_detail(payload)
            raise ValueError(f"Environment {env_id} ended in state {state}")

    if as_json:
        _print_json(payload)
        return

    print_success(f"Provisioned environment [cyan]{payload.get('id', '?')}[/cyan]")
    _print_environment_detail(payload)


# ---------------------------------------------------------------------------
# --wait helper
# ---------------------------------------------------------------------------


_TERMINAL_STATES: frozenset[str] = frozenset({"ready", "torn_down"})


def _wait_for_ready(
    api: t.Any,
    org: str,
    workspace: str,
    environment_id: str,
    *,
    timeout_sec: float,
    poll_interval: float,
) -> str:
    """Poll ``/environments/{id}/status`` until terminal or timeout.

    Returns the final state string. Callers decide what to do with
    non-``ready`` terminal states.
    """
    deadline = time.monotonic() + timeout_sec
    last_state = "provisioning"
    while time.monotonic() < deadline:
        snapshot = api.get_environment_status(org, workspace, environment_id)
        state = str(snapshot.get("state", "")) or last_state
        if state in _TERMINAL_STATES:
            return state
        last_state = state
        time.sleep(poll_interval)
    return f"timeout (last observed: {last_state})"


# ---------------------------------------------------------------------------
# get
# ---------------------------------------------------------------------------


@cli.command(name="list", alias="ls")
def list_(
    *,
    state: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(
            name=_FLAG_STATE,
            help="Filter by sandbox state (repeatable: running, paused, killed, etc.).",
            negative_iterable=(),
        ),
    ] = None,
    page: t.Annotated[int, cyclopts.Parameter(help="1-indexed page number.")] = 1,
    limit: t.Annotated[int, cyclopts.Parameter(help="Items per page.")] = 50,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """List task environments in the current workspace."""
    api, profile = platform.connect()
    payload = api.list_environments(
        profile.org_key,
        profile.workspace_key,
        state=state,
        page=page,
        limit=limit,
    )
    _render_list(
        payload,
        as_json=as_json,
        summary=_summarize_environment,
        empty_msg="No environments in this workspace",
        items_key="environments",
        fields=_ENVIRONMENT_LIST_ROW_FIELDS,
    )


@cli.command()
def get(
    environment_id: str,
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Fetch a task environment by id."""
    api, profile = platform.connect()
    payload = api.get_environment(profile.org_key, profile.workspace_key, environment_id)
    if as_json:
        _print_json(payload)
        return
    _print_environment_detail(payload)


@cli.command()
def wait(
    environment_id: str,
    *,
    timeout_sec: t.Annotated[
        float,
        cyclopts.Parameter(
            name=("--timeout-sec", "--wait-timeout-sec", "--wait-timeout"),
            help="Max seconds to wait (default 300).",
            validator=cyclopts.validators.Number(gt=0),
        ),
    ] = 300.0,
    poll_interval_sec: t.Annotated[
        float,
        cyclopts.Parameter(
            name=("--poll-interval-sec", "--poll-interval"),
            help="Seconds between status polls.",
            validator=cyclopts.validators.Number(gt=0),
        ),
    ] = 2.0,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Block until an environment reaches a terminal state.

    Polls until the environment is ``ready`` or ``torn_down``, then prints
    the current detail. Exits non-zero if the wait times out.
    """
    api, profile = platform.connect()
    state = _wait_for_ready(
        api,
        profile.org_key,
        profile.workspace_key,
        environment_id,
        timeout_sec=timeout_sec,
        poll_interval=poll_interval_sec,
    )
    payload = api.get_environment(profile.org_key, profile.workspace_key, environment_id)
    if as_json:
        _print_json(payload)
    else:
        _print_environment_detail(payload)
    if state != "ready":
        raise ValueError(f"Environment {environment_id} ended in state {state}")


# ---------------------------------------------------------------------------
# delete
# ---------------------------------------------------------------------------


@cli.command(alias="rm")
def delete(
    environment_id: str,
    *,
    yes: t.Annotated[bool, cyclopts.Parameter(name="--yes", alias="-y", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Tear down a task environment (terminates the sandbox).

    Args:
        environment_id: The environment ID.
        yes: Skip the confirmation prompt.
    """
    api, profile = platform.connect()

    if not confirm_destructive(f"Tear down environment [cyan]{environment_id}[/cyan]?", yes=yes):
        console.print("[dim]aborted[/dim]")
        return

    api.delete_environment(profile.org_key, profile.workspace_key, environment_id)
    print_success(f"Environment [cyan]{environment_id}[/cyan] torn down")


# ---------------------------------------------------------------------------
# exec
# ---------------------------------------------------------------------------


@cli.command()
def exec(  # noqa: A001 — matches the familiar `docker exec` / `kubectl exec` name
    environment_id: str,
    command: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(
            name="*",
            help="Command to run inside the environment (pass after `--`).",
        ),
    ] = None,
    *,
    token: t.Annotated[
        str | None,
        cyclopts.Parameter(
            help=(
                "Execute token from `dn env create`. Falls back to "
                "$DREADNODE_ENVIRONMENT_TOKEN when unset."
            ),
        ),
    ] = None,
    timeout_sec: t.Annotated[
        int,
        cyclopts.Parameter(
            help="Max execution time in seconds (1-600).",
            validator=cyclopts.validators.Number(gte=1, lte=600),
        ),
    ] = 30,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformScopeArgs = PlatformScopeArgs(),
) -> None:
    """Run a shell command inside a provisioned task environment.

    Requires the per-environment execute token returned by ``dn env create``.
    The token is not recoverable later — pass it via ``--token`` or
    ``DREADNODE_ENVIRONMENT_TOKEN``.

    Exits with the command's exit code so the CLI composes in shell scripts.
    """
    if not command:
        raise ValueError("Provide a command to run, e.g. `dn env exec ENV_ID -- echo hi`.")

    resolved_token = token or os.environ.get("DREADNODE_ENVIRONMENT_TOKEN")
    if not resolved_token:
        raise ValueError("Missing execute token. Pass --token or set DREADNODE_ENVIRONMENT_TOKEN.")

    api, profile = platform.connect()
    shell_command = " ".join(command)
    payload = api.execute_in_environment(
        profile.org_key,
        profile.workspace_key,
        environment_id,
        command=shell_command,
        timeout_sec=timeout_sec,
        execute_token=resolved_token,
    )

    if as_json:
        _print_json(payload)
        raise SystemExit(int(payload.get("exit_code", 1)))

    output = str(payload.get("output", ""))
    if output:
        console.print(output, end="" if output.endswith("\n") else "\n")
    exit_code = int(payload.get("exit_code", 1))
    if exit_code != 0:
        print_error(f"Command exited [red]{exit_code}[/red]")
    raise SystemExit(exit_code)
