import sys
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from http import HTTPStatus
from pathlib import Path
from typing import TYPE_CHECKING, Annotated

import click
import typer
from rich.console import Console

from mistralai.agents._cli_commands._shared import can_prompt as _can_prompt
from mistralai.agents._cli_commands._shared import fail as _fail
from mistralai.agents._cli_commands._shared import loading_spinner as _loading_spinner
from mistralai.agents._cli_commands.init.command import init_command
from mistralai.agents._cli_commands.skills.command import skills_app

if TYPE_CHECKING:
    from mistralai.vibe.harness.app_server.session import ApprovalCallback, SessionClient
    from mistralai.vibe_agents.sdk.app.chat import ApprovalAnswer
    from mistralai.vibe_agents.sdk.app.deploy import BuildFilesMissing, DeployPlan
    from mistralai.vibe_agents.sdk.app.loader import AgentApp
    from mistralai.vibe_agents.sdk.app.logs import LogLine
    from mistralai.vibe_agents.sdk.app.worker.serve import ServeReady

# The CLI is a rendering layer: each command calls one operation of `mistralai.vibe_agents.sdk.app`,
# then turns its result into terminal output and its errors into an exit code. Behaviour that a script
# or a platform could also want belongs in that package, not here.

_SESSIONS_DOCS_URL = "https://docs-internal-frameworks.mistral.ai/agents-sdk/learn/sessions/"
_OWN_DOCKERFILE_DOCS_URL = (
    "https://docs-internal-frameworks.mistral.ai/agents-sdk/learn/where-it-runs/deploy#bring-your-own-dockerfile"
)

app = typer.Typer(
    help="Run agents defined in Python.",
    no_args_is_help=True,
)

ProjectArg = Annotated[Path, typer.Argument(help="Project root (default: current directory).")]


def _print_version(value: bool) -> None:
    if not value:
        return
    from importlib.metadata import version  # noqa: PLC0415

    typer.echo(f"mistralai-agents {version('mistralai-agents')}")
    raise typer.Exit(0)


@app.callback()
def _main(
    _version: Annotated[
        bool,
        typer.Option(
            "--version",
            callback=_print_version,
            is_eager=True,
            help="Show the installed mistralai-agents version and exit.",
        ),
    ] = False,
) -> None:
    """Run agents defined in Python."""


@contextmanager
def _silenced_sdk_imports() -> Iterator[None]:
    from mistralai.agents import _silence

    _silence.presilence()
    try:
        from mistralai.vibe_agents.sdk.quiet import quiet_local_sdk_logs

        quiet_local_sdk_logs()
        yield
    finally:
        _silence.restore_runtime_warning_levels()


# `init` creates a project rather than running one, so it lives with its helpers in its own module.
app.command(name="init")(init_command)
# `skills` installs files the SDK ships rather than running a project, so it lives in its own module too.
app.add_typer(skills_app, name="skills")


@app.command(name="info")
def info_command(path: ProjectArg = Path(".")) -> None:
    """Show the agent surface and diagnostics."""
    from rich.text import Text  # noqa: PLC0415

    rendered: Text | None = None
    error: str | None = None
    with _loading_spinner("Loading agents SDK...") as set_stage:
        with _silenced_sdk_imports():
            from mistralai.vibe_agents.sdk.app import info, loader, preflight
            from mistralai.vibe_agents.sdk.app.errors import AgentProjectError

        set_stage("Loading agent...")
        failed = False
        try:
            loaded = loader.load_app(path)
            errors = [
                *preflight.connector_issues(loaded.harness, loaded.agent.subagents),
                *preflight.sandbox_dependency_issues(loaded),
            ]
            # Warnings, not errors: a deployed worker reads these variables from its own secret bindings.
            warnings = [
                f"{issue} Until then, `agents serve` refuses to start here."
                for issue in preflight.mcp_credential_issues(loaded.harness, loaded.agent.subagents)
            ]
            rendered = info.render(loaded, errors=errors, warnings=warnings)
            failed = bool(errors)
        except AgentProjectError as exc:
            error = exc.message

    if error is not None:
        raise _fail(error)
    # Soft wrap: piped output keeps one line per entry instead of breaking at 80 columns.
    Console(highlight=False, soft_wrap=True).print(rendered, markup=False)
    if failed:
        raise typer.Exit(1)


def _load_worker_app(path: Path, *, command: str) -> "AgentApp":
    loaded: AgentApp | None = None
    error_lines: list[str] = []
    with _loading_spinner("Loading agents SDK...") as set_stage:
        with _silenced_sdk_imports():
            from mistralai.vibe_agents.sdk.app import preflight
            from mistralai.vibe_agents.sdk.app.errors import AgentProjectError

        set_stage("Loading agent...")
        try:
            loaded = preflight.load_worker_app(path)
        except preflight.PreflightError as exc:
            error_lines = [f"Cannot start `{command}`:", *(f"  - {issue}" for issue in exc.issues)]
        except AgentProjectError as exc:
            error_lines = [exc.message]

    if loaded is None:
        raise _fail(*error_lines)
    return loaded


def _print_serve_banner(ready: "ServeReady") -> None:
    typer.echo(f"\n✓ Agent {ready.agent_name} is serving on {ready.deployment_name}")
    typer.echo("")
    _print_try_the_agent(ready.chat_url)
    if ready.debug_url is not None:
        typer.echo(f"  Debug:  {ready.debug_url}")
        typer.echo("")
    typer.echo("Press Ctrl+C to stop.\n")


def _print_try_the_agent(chat_url: str | None) -> None:
    # The control plane sends the chat link of its environment; without one, only the Session API remains.
    typer.echo("  Try the agent:")
    if chat_url is not None:
        typer.echo(f"  • in Vibe Code Web:          {chat_url}")
    typer.echo(f"  • programmatically, using the Session API: {_SESSIONS_DOCS_URL}")
    typer.echo("")


@app.command(name="serve")
def serve_command(
    path: ProjectArg = Path("."),
    name: Annotated[str | None, typer.Option(help="Agent name (overrides the agent's defined name).")] = None,
    send_config: Annotated[
        bool,
        typer.Option(
            "--send-config/--no-send-config",
            envvar="AGENTS_SDK_SERVE_SEND_CONFIG",
            help=(
                "Send the agent's configuration to Mistral, as `agents deploy` does, so it shows "
                "with the agent and its sessions in your workspace. A restart of the same code keeps the agent. "
                "Pass --no-send-config to register the agent without its configuration."
            ),
        ),
    ] = True,
) -> None:
    """Run the agent on your machine, register it in your workspace, and print a link to trigger it."""
    import asyncio  # noqa: PLC0415

    loaded = _load_worker_app(path, command="agents serve")
    with _silenced_sdk_imports():
        from mistralai.vibe_agents.sdk.app.errors import AgentProjectError
        from mistralai.vibe_agents.sdk.app.worker import serve

    # Ctrl+C is a clean stop. Any startup failure (e.g. the detached worker exits during setup) is one
    # stderr line and a nonzero exit, never a raw traceback.
    try:
        asyncio.run(serve.serve(loaded, name, on_ready=_print_serve_banner, send_config=send_config))
    except KeyboardInterrupt:
        raise typer.Exit(0) from None
    except AgentProjectError as exc:
        raise _fail(exc.message) from exc
    except serve.RegistrationError as exc:
        raise _fail(
            f"Cannot serve agent: registration failed at {exc.control_plane_url}: {exc}",
            "The worker cannot receive sessions until it is registered.",
        ) from exc
    except Exception as exc:  # noqa: BLE001 - surface any startup failure as one friendly line
        if _worker_key_refused(exc):
            credential = _worker_credential()
            raise _fail(
                f"Cannot serve agent: {credential} was refused (HTTP 401).",
                f"agents serve needs a credential allowed to run agent workers in this workspace; check {credential}.",
            ) from exc
        raise _fail(f"Cannot serve agent: {exc}") from exc


def _worker_key_refused(exc: BaseException) -> bool:
    from mistralai.workflows.exceptions import ErrorCode, WorkflowsException  # noqa: PLC0415

    pending: list[BaseException] = [exc]
    seen: set[int] = set()
    while pending:
        error = pending.pop()
        if id(error) in seen:
            continue
        seen.add(id(error))
        if (
            isinstance(error, WorkflowsException)
            and str(error.code) == ErrorCode.TEMPORAL_CONNECTION_ERROR
            and error.status == HTTPStatus.UNAUTHORIZED
        ):
            return True
        if isinstance(error, BaseExceptionGroup):
            pending.extend(error.exceptions)
        linked = error.__cause__ or (None if error.__suppress_context__ else error.__context__)
        if linked is not None:
            pending.append(linked)
    return False


def _worker_credential() -> str:
    from mistralai.workflows.core.config.config import config  # noqa: PLC0415

    if config.temporal.api_key:
        return "the worker's API key"
    if config.common.mistral_sa_token_path:
        return "the service-account token"
    return "MISTRAL_API_KEY"


# Hidden from `agents --help`: the command is the CMD of an `agents deploy` image, not something to run by
# hand. Run an agent with `agents serve` or `agents deploy`.
@app.command(name="run-worker", hidden=True)
def run_worker_command(path: ProjectArg = Path(".")) -> None:
    """Run the agent's worker only, without registering it. Use this as the Dockerfile CMD for `agents deploy`."""
    import asyncio  # noqa: PLC0415

    loaded = _load_worker_app(path, command="agents run-worker")
    with _silenced_sdk_imports():
        from mistralai.vibe_agents.sdk.app.deployment import DeploymentNameError

    try:
        asyncio.run(loaded.agent.run_worker())
    except KeyboardInterrupt:
        raise typer.Exit(0) from None
    except DeploymentNameError as exc:
        raise _fail(f"Cannot run the worker: {exc}") from exc


# The platform runs this command; an author never does, so it stays out of the help.
@app.command(name="run-shared-worker", hidden=True)
def run_shared_worker_command() -> None:
    """Run the platform's shared worker, which serves the agents the control plane runs without building them."""
    import asyncio  # noqa: PLC0415

    with _silenced_sdk_imports():
        from mistralai.vibe_agents.sdk.app.worker import runner  # noqa: PLC0415

    try:
        asyncio.run(runner.run_shared_worker())
    except runner.SharedWorkerConfigError as exc:
        raise _fail("Cannot run the shared worker:", *(f"  - {issue}" for issue in exc.issues)) from exc
    except KeyboardInterrupt:
        raise typer.Exit(0) from None


@app.command(name="shutdown")
def shutdown_command(
    name: Annotated[str, typer.Argument(help="Agent name to shut down.")],
    yes: Annotated[
        bool,
        typer.Option("--yes", "-y", help="Skip the confirmation prompt."),
    ] = False,
) -> None:
    """Shut an agent down permanently.

    The name is required rather than derived from the project: `--name` can give an agent
    another name than the one in its code. Guessing the target of a one-way action from
    the working directory is how the wrong agent gets shut down.
    """
    import asyncio  # noqa: PLC0415

    from mistralai.vibe_agents.sdk.app import shutdown  # noqa: PLC0415

    if not yes:
        typer.echo(f"Shutting down {name} cannot be undone.")
        typer.confirm(f"Shut down agent {name}?", abort=True)

    try:
        with _loading_spinner(f"Shutting down {name}..."):
            result = asyncio.run(shutdown.shutdown(name))
    except shutdown.ShutdownError as exc:
        raise _fail(str(exc)) from exc

    typer.echo(f"Agent {result.agent_name} is shut down. Sessions can no longer reach it.")
    if result.managed:
        typer.echo(f"  Its managed deployment {result.deployment_name} was deleted.")
        typer.echo("  Deploy again to bring the agent back, under a new agent id.")
    else:
        # Be explicit: the operator will otherwise assume their worker was stopped for them.
        typer.echo(f"  Its worker on {result.deployment_name} is not managed here and may still be running.")
        typer.echo("  If it is, stop that process yourself. Running `agents serve` again re-registers the name.")
    raise typer.Exit(0)


def _print_deploy_plan(plan: "DeployPlan") -> None:
    from rich.table import Table  # noqa: PLC0415

    from mistralai.vibe_agents.sdk.app import preflight  # noqa: PLC0415

    git_config = Table(title="Git configuration", show_header=False)
    git_config.add_column(style="bold")
    git_config.add_column()
    git_config.add_row("Repository", plan.spec.github_url)
    git_config.add_row("Revision", plan.spec.revision)
    git_config.add_row("Working directory", plan.spec.working_dir or "(root)")
    git_config.add_row("Dockerfile", plan.spec.dockerfile_path or preflight.DEFAULT_DOCKERFILE)
    git_config.add_row("Agents SDK", plan.sdk_version or "unknown")
    console = Console()
    console.print(git_config)
    if plan.secret_bindings:
        secret_config = Table(title="Secret bindings", show_header=False)
        secret_config.add_column(style="bold")
        secret_config.add_column()
        for binding in plan.secret_bindings:
            secret_config.add_row(binding.env_var_name, binding.reference)
        console.print(secret_config)
    for warning in plan.warnings:
        typer.echo(f"Warning: {warning}", err=True)


def _worker_output_lines(plan: "DeployPlan", service_id: str) -> list[str]:
    # The status only says the worker is unhealthy; its own output says why.
    import asyncio  # noqa: PLC0415

    from mistralai.vibe_agents.sdk.app import deploy  # noqa: PLC0415

    with _loading_spinner("Reading the worker's logs..."):
        output = asyncio.run(deploy.worker_output(plan, service_id))
    if output is None:
        return [
            "",
            "Could not read the worker's logs. Read them with:",
            f"  {deploy.worker_logs_command(plan, service_id)}",
        ]
    if not output:
        return []
    return ["", "Last output from the worker:", *(f"  {line}" for line in output)]


def _write_build_files(missing: "BuildFilesMissing", *, yes: bool) -> typer.Exit:
    # The deploy only ever writes these files once the user agreed, and never commits them: the user
    # reviews, commits and pushes them, then deploys again.
    from mistralai.vibe_agents.sdk.app import deploy  # noqa: PLC0415

    files = " and ".join(missing.names)
    if not yes:
        if not _can_prompt():
            return _fail(
                str(missing),
                f"Run `agents deploy` in a terminal to have {files} written, or pass --yes.",
                f"To write your own Dockerfile, see {_OWN_DOCKERFILE_DOCS_URL}",
            )
        if not typer.confirm(f"{missing} Write {files}?", default=True):
            return _fail(f"Add a Dockerfile before you deploy. To write your own, see {_OWN_DOCKERFILE_DOCS_URL}")
    written = deploy.write_build_files(missing.project)
    typer.echo(f"Wrote {' and '.join(written)} in {missing.project}.")
    typer.echo("Commit and push them with pyproject.toml and uv.lock, then run `agents deploy` again.")
    return typer.Exit(1)


@app.command(name="deploy")
def deploy_command(
    path: ProjectArg = Path("."),
    name: Annotated[str | None, typer.Option(help="Agent name (overrides the agent's defined name).")] = None,
    hardened: Annotated[
        bool | None,
        typer.Option(
            "--hardened/--no-hardened",
            help=(
                "Harden the deployment so the agent can use connectors/MCPs "
                "on behalf of the user who triggered the session. "
                "Default: hardened when the agent acts on behalf of the session's user."
            ),
        ),
    ] = None,
    dockerfile: Annotated[
        str | None,
        typer.Option(
            "--dockerfile",
            help="Dockerfile to build, relative to the project (default: Dockerfile).",
        ),
    ] = None,
    secret_binding: Annotated[
        list[str] | None,
        typer.Option(
            "--secret-binding",
            metavar="ENV_VAR=secret:workspace:NAME",
            help=(
                "Bind a workspace secret to an environment variable on the deployed agent, "
                "as ENV_VAR=secret:workspace:NAME. Pass a reference, never a secret value. "
                "Repeat for several variables. This is the complete set: a deploy that omits "
                "the option unbinds the secrets a previous deploy bound."
            ),
        ),
    ] = None,
    yes: Annotated[
        bool,
        typer.Option("--yes", "-y", help="Write a missing Dockerfile and .python-version without asking."),
    ] = False,
) -> None:
    """Build the project into an image and deploy it to Mistral, in your workspace."""
    import asyncio  # noqa: PLC0415

    plan: DeployPlan | None = None
    missing: BuildFilesMissing | None = None
    setup_error: list[str] = []
    with _loading_spinner("Loading agents SDK...") as set_stage:
        with _silenced_sdk_imports():
            from mistralai.vibe_agents.sdk.app import deploy, deploy_wait, preflight
            from mistralai.vibe_agents.sdk.app.errors import AgentProjectError

        set_stage("Preparing deploy...")
        try:
            plan = deploy.plan_deploy(
                path,
                name=name,
                dockerfile=dockerfile,
                secret_bindings=secret_binding or [],
                hardened=hardened,
                on_stage=set_stage,
            )
        except preflight.PreflightError as exc:
            setup_error = ["Cannot deploy:", *(f"  - {issue}" for issue in exc.issues)]
        except AgentProjectError as exc:
            setup_error = [exc.message]
        except deploy.BuildFilesMissing as exc:
            missing = exc
        except deploy.DeployError as exc:
            setup_error = [str(exc)]

    if missing is not None:
        raise _write_build_files(missing, yes=yes)
    if plan is None:
        raise _fail(*setup_error)

    _print_deploy_plan(plan)
    agent_name = plan.spec.agent_name
    typer.echo(f"Deploying {agent_name} to managed platform...")
    if plan.hardened and hardened is None:
        typer.echo("Hardening the deployment: the agent acts on behalf of the session user.")
    requested_at = datetime.now(UTC)
    try:
        response = asyncio.run(deploy.create_deployment(plan))
    except deploy.DeployError as exc:
        raise _fail(str(exc)) from exc

    typer.echo(f"Created agent {response.agent_id} (managed deployment: {response.service_id}).")
    try:
        with Console().status("Waiting for the deployment...", spinner="dots") as spinner:
            elapsed_seconds = asyncio.run(
                deploy.wait_until_live(
                    plan,
                    response.agent_id,
                    requested_at=requested_at,
                    on_progress=lambda progress, elapsed: spinner.update(
                        f"{progress.label} · {deploy_wait.format_elapsed(elapsed)}"
                    ),
                )
            )
    except KeyboardInterrupt:
        typer.echo(
            f"\nStopped waiting. Agent {agent_name} is still deploying and is not ready yet; "
            "it keeps deploying in the background.",
            err=True,
        )
        raise typer.Exit(130) from None
    except deploy.WorkerStartError as exc:
        raise _fail(str(exc), *_worker_output_lines(plan, response.service_id)) from exc
    except deploy.DeployError as exc:
        raise _fail(str(exc)) from exc

    typer.echo(f"Agent {agent_name} is live after {deploy_wait.format_elapsed(elapsed_seconds)}.")
    _print_try_the_agent(response.chat_url)
    raise typer.Exit(0)


@app.command(name="list")
def list_command() -> None:
    """List this workspace's agents, served or deployed, and whether they are running."""
    import asyncio  # noqa: PLC0415

    from mistralai.vibe_agents.sdk.app import catalog  # noqa: PLC0415

    try:
        with _loading_spinner("Listing agents..."):
            agents = asyncio.run(catalog.list_workspace_agents_from_env())
    except catalog.CatalogError as exc:
        raise _fail(str(exc)) from exc

    if not agents:
        typer.echo("No agents in this workspace. Start one with `agents serve` or `agents deploy`.")
        raise typer.Exit(0)
    # Plain aligned columns: the name is what every other command takes, so it is never truncated.
    width = max(len("NAME"), *(len(agent.agent_name) for agent in agents))
    typer.echo(f"{'NAME':<{width}}  {'KIND':<8}  STATUS")
    for agent in agents:
        kind = "deployed" if agent.managed else "served"
        # The control plane cannot tell a stopped worker from one it failed to look up, so "not running" would
        # claim more than it knows.
        status = "running" if agent.is_active else "not observed"
        typer.echo(f"{agent.agent_name:<{width}}  {kind:<8}  {status}")
    raise typer.Exit(0)


# A field longer than this is cut: one structured record must stay one readable line.
_MAX_FIELD_LENGTH = 120


def _short_field(value: object) -> object:
    text = value if isinstance(value, str) else repr(value)
    return value if len(text) <= _MAX_FIELD_LENGTH else f"{text[: _MAX_FIELD_LENGTH - 1]}…"


class _LogPrinter:
    """Prints each parsed log line through structlog's console renderer, the format `agents serve` prints.

    Colored only when the line's stream is a terminal, so a pipe or a file gets plain text.
    """

    def __init__(self, *, timestamps: bool, as_json: bool) -> None:
        from structlog.dev import ConsoleRenderer  # noqa: PLC0415

        self._timestamps = timestamps
        self._as_json = as_json
        # pad_event_to=0: most lines are a bare message, which padding would only end with spaces.
        self._renderers = {
            colors: ConsoleRenderer(colors=colors, sort_keys=False, pad_event_to=0) for colors in (True, False)
        }

    def print(self, line: "LogLine") -> None:
        import json  # noqa: PLC0415

        if self._as_json:
            typer.echo(json.dumps(line.to_record(), ensure_ascii=False, default=str))
            return
        err = line.stream == "stderr"
        stream = sys.stderr if err else sys.stdout
        event: dict[str, object] = {"event": line.message}
        event.update((key, _short_field(value)) for key, value in line.fields.items())
        if self._timestamps and line.created_at is not None:
            event["timestamp"] = line.created_at.isoformat(timespec="seconds")
        if line.is_platform:
            event["logger"] = "platform"
        elif line.logger:
            event["logger"] = line.logger
        level = line.level.name.lower() if line.level is not None else ""
        if level:
            event["level"] = level
        # The detail is printed as the worker wrote it: handed to the renderer, it would be re-formatted
        # as a local exception and draw a warning.
        rendered = self._renderers[stream.isatty()](None, level, event)
        typer.echo(f"{rendered}\n{line.detail}" if line.detail else rendered, err=err)


@app.command(name="logs")
def logs_command(
    name: Annotated[str, typer.Argument(help="Name of the deployed agent.")],
    follow: Annotated[
        bool, typer.Option("--follow", "-f", help="Keep printing new lines as they are written.")
    ] = False,
    lines: Annotated[
        int,
        typer.Option("--lines", "-n", min=1, max=1000, help="How many of the latest lines to print first."),
    ] = 100,
    timestamps: Annotated[bool, typer.Option("--timestamps", "-t", help="Prefix each line with its time.")] = False,
    level: Annotated[
        str | None,
        typer.Option(
            "--level",
            "-l",
            metavar="LEVEL",
            help=(
                "Only lines at this level or above: debug, info, warning, error. "
                "Indented continuations of kept lines, such as traceback frames, are kept too."
            ),
        ),
    ] = None,
    as_json: Annotated[
        bool,
        typer.Option("--json", help="One JSON object per line, with time, stream, level, logger, message and fields."),
    ] = False,
) -> None:
    """Print a deployed agent's logs.

    A served agent's logs are in the terminal that runs `agents serve`.
    """
    import asyncio  # noqa: PLC0415

    from mistralai.vibe_agents.sdk.app import logs  # noqa: PLC0415

    minimum = None
    if level is not None:
        minimum = logs.parse_level(level)
        if minimum is None:
            raise _fail(f"Unknown level {level!r}: use debug, info, warning or error.")

    try:
        with _loading_spinner(f"Finding {name}..."):
            source = asyncio.run(logs.resolve(name))
    except logs.LogsError as exc:
        raise _fail(str(exc)) from exc

    printer = _LogPrinter(timestamps=timestamps, as_json=as_json)

    # False: a continuation the read starts on, cut from its first line, has no kept line to follow.
    previous_shown = False

    def show(line: "LogLine") -> None:
        nonlocal previous_shown
        if minimum is None:
            printer.print(line)
            return
        # An indented line, such as a traceback frame, follows the line it belongs to; any other line
        # without a level is noise once the user asked for a level.
        shown = previous_shown if line.is_continuation else line.level is not None and line.level >= minimum
        previous_shown = shown
        if shown:
            printer.print(line)

    async def stream() -> None:
        if not follow:
            read = await logs.read(source, lines=lines)
            if not read:
                typer.echo(f"{name} has not logged anything yet.", err=True)
            for line in read:
                show(line)
            return
        async for line in logs.follow(source, lines=lines):
            show(line)

    try:
        asyncio.run(stream())
    except KeyboardInterrupt:
        raise typer.Exit(0) from None
    except logs.LogRetentionError as exc:
        # The equivalent request is refused the same way, so it is not offered.
        raise _fail(str(exc)) from exc
    except logs.LogsError as exc:
        raise _fail(str(exc), "Read them with:", f"  {logs.logs_command(source)}") from exc
    raise typer.Exit(0)


class _TerminalChat:
    """Renders a turn in the terminal: the reply as it streams, tool calls dimmed, approvals as a prompt.

    Every value comes from the agent or the model, so it is appended to a `Text` as plain text: passed as a
    markup string, a `[/dim]` in a tool argument would raise, and other tags would restyle the output.
    """

    def __init__(self, console: Console) -> None:
        self._console = console

    def _print(self, *parts: tuple[str, str]) -> None:
        from rich.text import Text  # noqa: PLC0415

        from mistralai.vibe_agents.sdk.app.runtime_logs import terminal_safe  # noqa: PLC0415

        # Plain Text stops Rich markup, not escape sequences: a tool name or argument from the model could still
        # carry one, so each part is cleaned before it is printed. One line each, so none can forge another.
        self._console.print(Text.assemble(*((terminal_safe(text), style) for text, style in parts)), soft_wrap=True)

    def reply(self, text: str) -> None:
        self._console.print(text, end="", markup=False, highlight=False, soft_wrap=True)

    def reply_done(self) -> None:
        self._console.print()

    def tool_call(self, name: str, arguments: object) -> None:
        import json  # noqa: PLC0415

        rendered = json.dumps(arguments, ensure_ascii=False) if arguments not in (None, {}) else ""
        if len(rendered) > 200:
            rendered = f"{rendered[:199]}…"
        self._print((f"→ {name}", "dim"), (f" {rendered}" if rendered else "", "dim"))

    def tool_result(self, name: str, error: str | None) -> None:
        if error is None:
            self._print((f"← {name} done", "dim"))
        else:
            self._print((f"← {name} failed:", "red"), (f" {error}", ""))

    def ask_approval(self, callback: "ApprovalCallback") -> "ApprovalAnswer":
        import json  # noqa: PLC0415

        from mistralai.vibe_agents.sdk.app.chat import ApprovalAnswer  # noqa: PLC0415

        tool = callback.name or callback.tool_id
        self._print((f"? Allow {tool}?" if tool else f"? {callback.title}", "bold yellow"))
        if callback.input not in (None, {}):
            self._print((f"  {json.dumps(callback.input, ensure_ascii=False)}", ""))
        if not _can_prompt():
            self._print(("  No terminal to ask in: denied.", ""))
            return ApprovalAnswer.DENY
        # A hook's approval keeps no grant for the session, so the Session refuses a session-wide allow.
        offers_session = callback.hook is None
        options = "[y]es once / [a]lways in this session / [n]o" if offers_session else "[y]es once / [n]o"
        choice = typer.prompt(f"  {options}", default="n").strip().lower()
        if choice in ("y", "yes"):
            return ApprovalAnswer.ONCE
        if offers_session and choice in ("a", "always"):
            return ApprovalAnswer.SESSION
        return ApprovalAnswer.DENY

    def notice(self, message: str) -> None:
        self._print((message, "yellow"))

    def turn_failed(self, message: str) -> None:
        self._print((f"The turn failed: {message}", "red"))

    def turn_cancelled(self, reason: str | None) -> None:
        # A cancel from the server carries a reason; without it, it would read like the user's own Ctrl+C.
        self._print((f"Interrupted: {reason}" if reason else "Interrupted.", "dim"))


@app.command(name="chat")
def chat_command(
    name: Annotated[
        str | None,
        typer.Argument(help="Served or deployed agent to talk to. Omit to run the project's agent in this process."),
    ] = None,
    path: Annotated[
        Path, typer.Option("--path", help="Project root, without NAME (default: current directory).")
    ] = Path("."),
    message: Annotated[
        str | None,
        typer.Option("--message", "-m", help="Send this one message, print the reply and exit."),
    ] = None,
) -> None:
    """Talk to an agent: the project's agent in this process, or a served or deployed agent by name.

    Ctrl+C interrupts the agent's turn; Ctrl+D, or `/exit`, ends the chat.
    """
    import asyncio  # noqa: PLC0415

    session: SessionClient | None = None
    error: str | None = None
    target = name or "the agent"
    with _loading_spinner("Loading agents SDK...") as set_stage:
        with _silenced_sdk_imports():
            from mistralai.vibe_agents.sdk.app import chat
            from mistralai.vibe_agents.sdk.app.errors import AgentProjectError
            from mistralai.vibe_agents.sdk.app.runtime_logs import terminal_safe

        chat.hide_noticed_connector_logs()
        set_stage(f"Connecting to {name}..." if name else "Loading agent...")
        runner = asyncio.Runner()
        try:
            session = runner.run(chat.open_session(agent_name=name, path=path))
        except AgentProjectError as exc:
            error = exc.message
        except chat.ChatError as exc:
            # Kept multi-line (the preflight list), but cleaned: the text can come from the control plane.
            error = terminal_safe(str(exc), keep_newlines=True)
    if session is None:
        runner.close()
        raise _fail(error or f"Cannot start a session with {target}.")

    console = Console(highlight=False)
    output = _TerminalChat(console)

    def turn(text: str) -> bool | None:
        """Run one turn: True when it completed, False when it failed or was interrupted, None if the stream was lost.

        Every expected error ends as one line instead of a traceback, in both modes.
        """
        from mistralai.vibe.harness.app_server.session import SessionEventStreamLostError  # noqa: PLC0415

        try:
            return runner.run(chat.run_turn(session, text, output))
        # click raises Abort, not KeyboardInterrupt, for a Ctrl+C at the approval prompt.
        except (KeyboardInterrupt, click.exceptions.Abort):
            # The turn is interrupted on the agent's side; the session stays open for the next message.
            console.print("\nInterrupted.", style="dim", markup=False)
            return False
        except SessionEventStreamLostError as exc:
            # The turn may still be running on the agent's side, so another message now would collide with it.
            console.print(
                f"\nLost the connection to the session; its turn may still be running. {terminal_safe(str(exc))}",
                style="red",
                markup=False,
            )
            if name is not None:
                console.print(
                    f"Read it later with `Agent.load_from(agent_name={name!r}).session({session.session_id!r})`.",
                    style="dim",
                    markup=False,
                )
            return None
        except Exception as exc:  # noqa: BLE001 - a failed turn is one line, not a traceback
            # The error text can come from the network, so it is cleaned like everything else the chat prints.
            console.print(f"The turn failed: {terminal_safe(str(exc))}", style="red", markup=False)
            return False

    try:
        # Inside the try, so a Ctrl+C while the notices are read still closes the session.
        try:
            runner.run(chat.report_startup_notices(session, output))
        except Exception:  # noqa: BLE001 - the notices only inform; the chat works without them
            import structlog  # noqa: PLC0415

            structlog.get_logger(__name__).debug(
                "agents chat could not read the session's startup notices", exc_info=True
            )
        if message is not None:
            completed = turn(message)
            if completed is not True:
                # The failure is already printed; a script needs the exit code to tell it from a reply.
                raise typer.Exit(1)
            return
        where = f"{name}" if name else f"{target} in this process"
        console.print(
            f"Talking to {where} (session {session.session_id}). Ctrl+D or /exit to quit.", style="dim", markup=False
        )
        while True:
            try:
                text = console.input("[bold cyan]> [/bold cyan]")
            except (EOFError, KeyboardInterrupt):
                console.print()
                return
            if text.strip() in ("/exit", "/quit"):
                return
            if not text.strip():
                continue
            if turn(text) is None:
                raise typer.Exit(1)
    finally:
        try:
            runner.run(session.close())
        finally:
            runner.close()
