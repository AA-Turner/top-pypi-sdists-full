"""Root cyclopts App with top-level commands (tui, login, serve)."""

import importlib.metadata
import os
import secrets
import sys
import time
import typing as t

if t.TYPE_CHECKING:
    from dreadnode.app.tui.app import DreadnodeTextualApp

import cyclopts
from loguru import logger
from rich.panel import Panel

from dreadnode.app.cli.airt import cli as airt_cli
from dreadnode.app.cli.args import PlatformArgs, TuiArgs
from dreadnode.app.cli.capability import cli as capability_cli
from dreadnode.app.cli.dataset import cli as dataset_cli
from dreadnode.app.cli.environment import cli as environment_cli
from dreadnode.app.cli.evaluation import cli as evaluation_cli
from dreadnode.app.cli.inference_model import cli as inference_model_cli
from dreadnode.app.cli.judge import cli as judge_cli
from dreadnode.app.cli.model import cli as model_cli
from dreadnode.app.cli.optimize import cli as optimize_cli
from dreadnode.app.cli.runtime import cli as runtime_cli
from dreadnode.app.cli.sandbox import cli as sandbox_cli
from dreadnode.app.cli.secret import cli as secret_cli
from dreadnode.app.cli.session import cli as session_cli
from dreadnode.app.cli.shared import console, print_error, print_success
from dreadnode.app.cli.task import cli as task_cli
from dreadnode.app.cli.train import cli as train_cli
from dreadnode.app.cli.worlds import cli as worlds_cli
from dreadnode.app.model_catalog import resolve_model

DEBUG = bool(os.getenv("DREADNODE_DEBUG"))


def _get_version_safe() -> str:
    """Get package version safely, falling back to 'dev' if not installed."""
    try:
        return importlib.metadata.version("dreadnode")
    except importlib.metadata.PackageNotFoundError:
        return "dev"


def _new_device_login_api_key_name() -> str:
    return f"dreadnode-{secrets.token_hex(3)}"


def _render_profile_context(profile: t.Any) -> str:
    parts = [
        part
        for part in (
            getattr(profile, "default_organization", None),
            getattr(profile, "default_workspace", None),
            getattr(profile, "default_project", None),
        )
        if part
    ]
    return "/".join(parts)


# ---------------------------------------------------------------------------
# Root app
# ---------------------------------------------------------------------------

cli = cyclopts.App(
    name="dreadnode",
    help="Dreadnode CLI — agent development and platform tooling.",
    version=_get_version_safe(),
    help_on_error=True,
)
cli.register_install_completion_command()

# Move meta flags (--help, --version, --install-completion) out of Commands
cli["--help"].group = "Meta"
cli["--version"].group = "Meta"
cli["--install-completion"].group = "Meta"

# ---------------------------------------------------------------------------
# Subcommands
# ---------------------------------------------------------------------------

cli.command(airt_cli)
cli.command(capability_cli)
cli.command(dataset_cli)
cli.command(environment_cli, alias="env")
cli.command(evaluation_cli)
cli.command(inference_model_cli, alias="llm")
cli.command(judge_cli)
cli.command(model_cli)
cli.command(optimize_cli)
cli.command(runtime_cli)
cli.command(sandbox_cli)
cli.command(secret_cli)
cli.command(session_cli)
cli.command(task_cli)
cli.command(train_cli)
cli.command(worlds_cli)


# ---------------------------------------------------------------------------
# Meta handler — centralized exception formatting for all commands
# ---------------------------------------------------------------------------


@cli.meta.default
def _meta(
    *tokens: t.Annotated[str, cyclopts.Parameter(show=False, allow_leading_hyphen=True)],
) -> None:
    try:
        console.print()
        cli(tokens)
    except Exception as exc:
        if DEBUG:
            raise
        logger.exception("Unhandled exception")
        message = str(exc) or exc.__class__.__name__
        print_error(f"{message} [dim]({exc.__class__.__name__})[/dim]")
        sys.exit(1)


# ---------------------------------------------------------------------------
# Default command — handles bare `dn` (no subcommand) or `dn --model x ...`
# ---------------------------------------------------------------------------


@cli.default
def _default(*, tui_args: TuiArgs = TuiArgs()) -> None:
    """Launch the TUI (default) or headless print mode."""
    if tui_args.print_mode:
        _run_print(tui_args)
    else:
        _run_tui(tui_args)


# ---------------------------------------------------------------------------
# Internal TUI / print helpers
# ---------------------------------------------------------------------------


def create_app(tui_args: TuiArgs) -> "DreadnodeTextualApp":
    """Build a :class:`DreadnodeTextualApp` from resolved CLI/TUI args.

    This is the single entrypoint for constructing the app from
    :class:`TuiArgs` — used by both the CLI and the tui-pilot MCP server.
    """
    from dreadnode.app.config import ProfileError
    from dreadnode.app.tui.app import DreadnodeTextualApp

    # Resolve profile using the config system before entering the TUI.
    # None is fine — the TUI will show the auth modal. Seed platform_url
    # from --server so AuthModal points at the right server even when
    # resolve() raises (e.g. --profile + --server mutex error).
    platform_url: str | None = tui_args.server
    try:
        profile = tui_args.resolve()
        platform_url = profile.url
        if not profile.url or not profile.api_key:
            profile = None
    except ProfileError as exc:
        import sys

        print(f"⚠ Profile error: {exc}", file=sys.stderr)
        profile = None
    except Exception:
        profile = None

    initial_policy: dict[str, t.Any] | None = None
    if tui_args.policy:
        from dreadnode.app.tui.app import _coerce_policy_arg

        initial_policy = {"name": tui_args.policy}
        for kv in tui_args.policy_arg or []:
            if "=" not in kv:
                raise ValueError(f"--policy-arg expects key=value, got {kv!r}")
            key, _, value = kv.partition("=")
            initial_policy[key.strip()] = _coerce_policy_arg(value.strip())
        # `--max-steps` is a long-standing shortcut; honor it when the policy
        # accepts a step budget but the user didn't explicitly pass it.
        if tui_args.max_steps is not None and "max_steps" not in initial_policy:
            initial_policy["max_steps"] = tui_args.max_steps
    elif tui_args.auto:
        initial_policy = {"name": "headless"}
        if tui_args.max_steps is not None:
            initial_policy["max_steps"] = tui_args.max_steps

    return DreadnodeTextualApp(
        profile=profile,
        platform_url=platform_url,
        server_url=tui_args.runtime_server,
        resume_session_id=tui_args.resume,
        initial_model=resolve_model(tui_args.model) if tui_args.model else None,
        initial_agent=tui_args.agent,
        initial_prompt=tui_args.prompt,
        capabilities_dirs=tui_args.capabilities_dirs,
        capabilities=tui_args.capabilities,
        capability_flags=tui_args.capability_flags,
        system_prompt=tui_args.system_prompt,
        initial_policy=initial_policy,
    )


def _run_tui(tui_args: TuiArgs) -> None:
    app = create_app(tui_args)
    app.run()

    if app.active_session_id:
        print(
            f"\nTo resume this session, run: dreadnode --resume {app.active_session_id}",
            file=sys.stderr,
        )


def _run_print(tui_args: TuiArgs) -> None:
    import asyncio

    from dreadnode.app.print_mode import run_print_mode

    if not tui_args.prompt:
        raise ValueError("--print requires --prompt")

    asyncio.run(
        run_print_mode(
            prompt=tui_args.prompt,
            model=resolve_model(tui_args.model) if tui_args.model else None,
            agent=tui_args.agent,
            capabilities_dirs=tui_args.capabilities_dirs,
            capabilities=tui_args.capabilities,
            capability_flags=tui_args.capability_flags,
            system_prompt=tui_args.system_prompt,
            server_url=tui_args.runtime_server,
            platform_url=tui_args.server,
        )
    )


# ---------------------------------------------------------------------------
# login command
# ---------------------------------------------------------------------------


@cli.command()
def login(
    api_key: t.Annotated[
        str | None,
        cyclopts.Parameter(
            help="API key to save locally. Omit to use browser-based device login.",
        ),
    ] = None,
    *,
    server: t.Annotated[
        str | None,
        cyclopts.Parameter(help="Platform API URL override for login and profile storage"),
    ] = None,
    profile: t.Annotated[
        str | None,
        cyclopts.Parameter(
            name=["--profile", "-p"],
            help="Profile name to create or update. Defaults to your username.",
        ),
    ] = None,
    organization: str | None = None,
    workspace: str | None = None,
    project: str | None = None,
    poll_interval_sec: t.Annotated[
        float,
        cyclopts.Parameter(help="Polling interval for browser-based device login"),
    ] = 2.0,
    timeout_sec: t.Annotated[
        float | None,
        cyclopts.Parameter(help="Optional timeout for browser-based device login"),
    ] = None,
) -> None:
    """Authenticate with the Dreadnode platform."""
    from dreadnode.app.config import DEFAULT_PLATFORM_URL
    from dreadnode.app.tui.auth_flow import _login_with_api_key

    server_url = (server or DEFAULT_PLATFORM_URL).rstrip("/")

    if api_key:
        result = _login_with_api_key(
            server_url,
            api_key,
            organization=organization,
            workspace=workspace,
            project=project,
            profile_name=profile,
        )
    else:
        result = _login_with_device_code(
            server_url=server_url,
            organization=organization,
            workspace=workspace,
            project=project,
            poll_interval_sec=poll_interval_sec,
            timeout_sec=timeout_sec,
            profile_name=profile,
        )

    identity = getattr(result, "username", None) or getattr(result, "user_key", None) or "unknown"
    profile_label = getattr(result, "_name", None) or identity
    print_success(f"Logged in to {result.url} as [cyan]{identity}[/cyan]")
    if profile_label != identity:
        console.print(f"Profile: [bold]{profile_label}[/bold]")
    context = _render_profile_context(result)
    if context:
        console.print(f"Active context: [dim]{context}[/dim]")


# ---------------------------------------------------------------------------
# Device-code login helper
# ---------------------------------------------------------------------------


def _login_with_device_code(
    *,
    server_url: str,
    organization: str | None,
    workspace: str | None,
    project: str | None,
    poll_interval_sec: float,
    timeout_sec: float | None,
    profile_name: str | None = None,
) -> t.Any:
    import httpx

    from dreadnode.app.api.client import ApiClient
    from dreadnode.app.tui.auth_flow import _login_with_api_key

    api = ApiClient(server_url)
    payload = api.create_device_code()

    user_code = payload.get("user_code")
    device_code = payload.get("device_code")
    if not isinstance(user_code, str) or not user_code:
        raise RuntimeError("Device login response missing user code")
    if not isinstance(device_code, str) or not device_code:
        raise RuntimeError("Device login response missing device code")

    verification_url = payload.get("verification_url")
    if not isinstance(verification_url, str) or not verification_url:
        verification_url = f"{server_url}/login/device?code={user_code}"

    # Attempt to open the browser automatically (mirrors TUI flow)
    import webbrowser

    try:
        opened = webbrowser.open(verification_url)
    except Exception:
        opened = False

    if opened:
        console.print(f"Opened browser to [cyan]{verification_url}[/cyan]")
    else:
        console.print(f"Open this URL in your browser:\n  [cyan]{verification_url}[/cyan]")
    console.print()
    console.print(
        Panel(
            f"[bold]{user_code}[/bold]",
            title="Your login code",
            expand=False,
            padding=(0, 4),
        )
    )
    console.print()

    timeout_deadline: float | None = None
    if timeout_sec is not None:
        timeout_deadline = time.monotonic() + timeout_sec
    expires_in = payload.get("expires_in")
    if isinstance(expires_in, (int, float)):
        expires_deadline = time.monotonic() + float(expires_in)
        timeout_deadline = (
            expires_deadline
            if timeout_deadline is None
            else min(timeout_deadline, expires_deadline)
        )

    from rich.live import Live
    from rich.spinner import Spinner

    consecutive_failures = 0
    with Live(
        Spinner("dots", text="[dim]Waiting for browser authorization...[/dim]"),
        console=console,
        refresh_per_second=10,
    ):
        while True:
            if timeout_deadline is not None and time.monotonic() >= timeout_deadline:
                raise TimeoutError("Device login timed out before authorization completed")

            try:
                status_code, poll_payload = api.poll_device_code(device_code)
            except (OSError, httpx.HTTPError) as exc:
                consecutive_failures += 1
                if consecutive_failures >= 3:
                    raise RuntimeError(f"Device login polling failed: {exc}") from exc
                time.sleep(poll_interval_sec)
                continue

            if status_code >= 500:
                consecutive_failures += 1
                if consecutive_failures >= 3:
                    raise RuntimeError("Device login polling failed")
                time.sleep(poll_interval_sec)
                continue

            consecutive_failures = 0
            if poll_payload and poll_payload.get("user_id"):
                break
            time.sleep(poll_interval_sec)

    tokens = api.exchange_device_code(device_code)
    access_token = tokens.get("access_token")
    if not isinstance(access_token, str) or not access_token:
        raise RuntimeError("Device login did not return an access token")

    created = api.create_api_key_with_jwt(
        access_token,
        _new_device_login_api_key_name(),
        allow_self_revoke=True,
    )
    api_key = created.get("key") or created.get("api_key")
    if not isinstance(api_key, str) or not api_key:
        raise RuntimeError("Device login failed to create an API key")

    return _login_with_api_key(
        server_url,
        api_key,
        organization=organization,
        workspace=workspace,
        project=project,
        profile_name=profile_name,
    )


# ---------------------------------------------------------------------------
# whoami command
# ---------------------------------------------------------------------------


@cli.command()
def whoami(
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Show current user, organization, and profile context."""
    _api, profile = platform.connect()

    if as_json:
        import json

        info: dict[str, t.Any] = {
            "profile": profile.name,
            "server": profile.url,
            "username": profile.username,
            "email": profile.email,
            "organization": profile.organization,
            "workspace": profile.workspace,
            "project": profile.project,
        }
        print(json.dumps(info, indent=2))
        return

    name = profile.name or "default"
    console.print(f"[bold cyan]{name}[/bold cyan]  [dim]profile[/dim]")
    fields: list[tuple[str, str | None]] = [
        ("user", profile.username),
        ("email", profile.email),
        ("org", profile.organization),
        ("workspace", profile.workspace),
        ("project", profile.project),
        ("server", profile.url),
    ]
    for label, value in fields:
        if value:
            dim = "dim" if label == "server" else ""
            style = f"[{dim}]{value}[/{dim}]" if dim else value
            console.print(f"  [dim]{label:<10}[/dim] {style}")


# ---------------------------------------------------------------------------
# update command
# ---------------------------------------------------------------------------


@cli.command()
def update(
    *,
    check: t.Annotated[
        bool,
        cyclopts.Parameter(
            negative=(),
            help="Only check for updates; exit 1 if an update is available, 0 if up to date.",
        ),
    ] = False,
) -> None:
    """Update the Dreadnode CLI to the latest version on PyPI."""
    import asyncio
    import shlex
    import subprocess

    from dreadnode.app.tui.update_check import (
        check_for_update,
        detect_upgrade_command,
        verify_upgrade,
    )

    console.print("Checking for updates...")
    info = asyncio.run(check_for_update(suppress_errors=False))

    if info is None:
        print_success("Already up to date")
        return

    console.print(
        f"Update available: [dim]{info.current}[/dim] → [bold cyan]{info.latest}[/bold cyan]"
    )

    if check:
        sys.exit(1)

    cmd = detect_upgrade_command()
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)

    cmd_display = " ".join(cmd)
    console.print(f"Running: [dim]{cmd_display}[/dim]")

    try:
        result = subprocess.run(cmd, check=False)  # noqa: S603
    except Exception as exc:
        console.print(f"[red]Update failed: {exc}[/red]")
        sys.exit(1)

    if result.returncode != 0:
        console.print(f"[red]Upgrade command exited with code {result.returncode}[/red]")
        sys.exit(1)

    verified = verify_upgrade(info.latest)
    if verified:
        print_success(f"Updated to v{verified} — restart [bold]dn[/bold] to use the new version")
        return

    console.print(
        "[red]Upgrade command succeeded but version unchanged — "
        "you may have multiple installations. Check which dn is on your PATH.[/red]"
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# serve command
# ---------------------------------------------------------------------------


@cli.command()
def serve(
    *,
    host: t.Annotated[str | None, cyclopts.Parameter(help="Server bind host")] = None,
    port: t.Annotated[int | None, cyclopts.Parameter(help="Server bind port")] = None,
    working_dir: t.Annotated[
        str | None, cyclopts.Parameter(help="Working directory for the server")
    ] = None,
    platform_server: t.Annotated[
        str | None, cyclopts.Parameter(help="Platform API URL override")
    ] = None,
    api_key: t.Annotated[
        str | None, cyclopts.Parameter(help="API key for platform authentication")
    ] = None,
    organization: t.Annotated[
        str | None, cyclopts.Parameter(help="Organization slug override")
    ] = None,
    workspace: t.Annotated[str | None, cyclopts.Parameter(help="Workspace slug override")] = None,
    project: t.Annotated[str | None, cyclopts.Parameter(help="Project slug override")] = None,
    verbose: t.Annotated[
        bool,
        cyclopts.Parameter(negative=(), help="Enable verbose trace logging for the local server"),
    ] = False,
) -> None:
    """Host a runtime server for the TUI."""
    from dreadnode.app.server import run_server
    from dreadnode.core.log import configure_server_logging

    configure_server_logging("trace" if verbose else None)
    if working_dir:
        os.chdir(working_dir)
    run_server(
        host=host,
        port=port,
        server=platform_server,
        api_key=api_key,
        organization=organization,
        workspace=workspace,
        project=project,
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def run(argv: list[str] | None = None) -> None:
    """CLI entry point."""
    try:
        if argv is not None:
            cli.meta(argv)
        else:
            cli.meta()
    except SystemExit as exc:
        if exc.code not in (None, 0):
            raise
