"""Scan command for MCP Watch."""

import json

import structlog
import typer

from runlayer_cli import __version__
from runlayer_cli.api import RunlayerClient
from runlayer_cli.console import print_error
from runlayer_cli.symbols import OK, WARN
from runlayer_cli.config import (
    AI_WATCH_MDM_ORG_KEY_LABEL,
    resolve_credentials,
    set_credentials_in_context,
)
from runlayer_cli.logging import attach_system_scan_log_handler, setup_logging
from runlayer_cli.tls import set_ca_bundle_path
from runlayer_cli import telemetry
from runlayer_cli.scan.agents.report import format_summary
from runlayer_cli.scan.artifact_cache import ArtifactCache
from runlayer_cli.scan.project_scanner import (
    MAX_PROJECT_DEPTH,
    MAX_PROJECT_TIMEOUT,
)
from runlayer_cli.scan.run_lock import ScanRunLockError, acquire_scan_run_lock
from runlayer_cli.scan.resource_governor import (
    DEFAULT_CPU_PERCENT,
    DEFAULT_MEMORY_LIMIT_MB,
    MAX_CPU_CORES,
    MAX_CPU_PERCENT,
    MAX_MEMORY_LIMIT_MB,
    MIN_CPU_CORES,
    MIN_CPU_PERCENT,
    MIN_MEMORY_LIMIT_MB,
    default_cpu_cores,
)
from runlayer_cli.scan.service import (
    scan_all_clients,
    submit_scan_results,
)
from runlayer_cli.scan.windows_users import is_windows_system_context

logger = structlog.get_logger(__name__)

app = typer.Typer(help="Scan MCP client configurations")


def _agent_definition_count(result) -> int:
    definitions = getattr(result, "agent_definitions", ())
    return int(getattr(result, "total_agent_definitions", len(definitions)))


def _no_findings(result) -> bool:
    """True when the scan surfaced nothing across every category.

    A scan that found only clients, agent definitions, framework agents, runtime
    processes, containers, or a successfully collected WSL inventory must not
    print "nothing found" and exit silently. Client presence, runtime processes,
    and inventories are submitted with the MCP scan payload. Agent definitions
    use their own bounded report.
    """
    return (
        result.total_servers == 0
        and not result.detected_clients
        and result.total_skills == 0
        and result.total_plugins == 0
        and not result.agents
        and not getattr(result, "agent_definitions", ())
        and not result.processes
        and not result.containers
        and not result.containers_scanned
        and not result.wsl_distros
        and not result.wsl_scanned
    )


@app.callback(invoke_without_command=True)
def scan(
    ctx: typer.Context,
    secret: str | None = typer.Option(
        None,
        "--secret",
        "-s",
        envvar="RUNLAYER_API_KEY",
        help="API secret for authentication",
    ),
    host: str | None = typer.Option(
        None,
        "--host",
        "-H",
        envvar="RUNLAYER_HOST",
        help="Runlayer host URL (required if not in config)",
    ),
    org_api_key: str | None = typer.Option(
        None,
        "--org-api-key",
        envvar="RUNLAYER_ORG_API_KEY_NAME",
        help="Name of a stored org API key to use for authentication",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-n",
        help="Print scan results without submitting to API",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose output",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress all output except errors",
    ),
    device_id: str | None = typer.Option(
        None,
        "--device-id",
        help="Custom device identifier (auto-generated if not provided)",
    ),
    org_device_id: str | None = typer.Option(
        None,
        "--org-device-id",
        help="Organization-provided device ID (e.g., MDM asset tag)",
    ),
    no_projects: bool = typer.Option(
        False,
        "--no-projects",
        help="Skip scanning for project-level configurations",
    ),
    detect_agents: bool = typer.Option(
        True,
        "--detect-agents/--no-detect-agents",
        help="Master switch for agent detection (on by default). Runs the "
        "install-detected channel (e.g. OpenClaw) and gates "
        "--detect-agent-frameworks. --no-detect-agents disables every agent "
        "channel.",
    ),
    detect_agent_frameworks: bool = typer.Option(
        True,
        "--detect-agent-frameworks/--no-detect-agent-frameworks",
        help="Static agent-framework scan (dependency-manifest + source "
        "scoring), on by default. Discovered agents are submitted to Runlayer "
        "(POST /ai-watch/agents). --no-detect-agent-frameworks skips the extra "
        "crawl/walk I/O and reports only install-detected agents. Requires "
        "--detect-agents.",
    ),
    detect_processes: bool = typer.Option(
        False,
        "--detect-processes/--no-detect-processes",
        envvar="RUNLAYER_DETECT_PROCESSES",
        help="Runtime process discovery (off by default). Enumerates running "
        "processes and listening sockets, scores AI-relatedness, and correlates "
        "them to configured MCP servers. Discovered processes are submitted with "
        "the MCP scan payload.",
    ),
    detect_containers: bool = typer.Option(
        False,
        "--detect-containers/--no-detect-containers",
        envvar="RUNLAYER_DETECT_CONTAINERS",
        help="Temporary opt-in for container & WSL discovery: read-only "
        "artifact discovery inside running containers (Docker; k3s on Linux) "
        "plus running/stopped Docker container and local image inventory; on "
        "Windows, also runs a bounded project walk across WSL homes. Missing "
        "or denied Docker daemons and unavailable WSL distributions are skipped.",
    ),
    detect_disguised_skills: bool = typer.Option(
        False,
        "--detect-disguised-skills/--no-detect-disguised-skills",
        envvar="RUNLAYER_DETECT_DISGUISED_SKILLS",
        help="Opt-in browser/cache probe for disguised skill artifacts.",
    ),
    artifact_lookup_cache: bool = typer.Option(
        False,
        "--artifact-lookup-cache/--no-artifact-lookup-cache",
        envvar="RUNLAYER_ARTIFACT_LOOKUP_CACHE",
        help="Cache server-confirmed artifact identifiers to reduce lookup requests.",
    ),
    detect_renamed_plugin_caches: bool = typer.Option(
        False,
        "--detect-renamed-plugin-caches/--no-detect-renamed-plugin-caches",
        envvar="RUNLAYER_DETECT_RENAMED_PLUGIN_CACHES",
        help="Opt-in marker-based probe for renamed plugin cache directories "
        "under known client roots.",
    ),
    project_depth: int = typer.Option(
        7,
        "--project-depth",
        envvar="RUNLAYER_PROJECT_DEPTH",
        min=1,
        max=MAX_PROJECT_DEPTH,
        clamp=True,
        help=f"Maximum directory depth for project scanning (max {MAX_PROJECT_DEPTH})",
    ),
    project_timeout: int = typer.Option(
        60,
        "--project-timeout",
        envvar="RUNLAYER_PROJECT_TIMEOUT",
        min=1,
        max=MAX_PROJECT_TIMEOUT,
        clamp=True,
        help=f"Timeout in seconds for project scanning (max {MAX_PROJECT_TIMEOUT})",
    ),
    cpu_cores: int = typer.Option(
        default_cpu_cores(),
        "--cpu-cores",
        envvar="RUNLAYER_CPU_CORES",
        min=MIN_CPU_CORES,
        max=MAX_CPU_CORES,
        clamp=True,
        help=(
            "Concurrency ceiling for scan workers "
            f"({MIN_CPU_CORES}..{MAX_CPU_CORES}, default half this machine's cores)"
        ),
    ),
    max_cpu_percent: int = typer.Option(
        DEFAULT_CPU_PERCENT,
        "--max-cpu-percent",
        envvar="RUNLAYER_MAX_CPU_PERCENT",
        min=MIN_CPU_PERCENT,
        max=MAX_CPU_PERCENT,
        clamp=True,
        help=(
            "Single-core-equivalent CPU duty budget; 50 means 0.5 core "
            "regardless machine size "
            f"({MIN_CPU_PERCENT}..{MAX_CPU_PERCENT}, default {DEFAULT_CPU_PERCENT})"
        ),
    ),
    memory_limit_mb: int = typer.Option(
        DEFAULT_MEMORY_LIMIT_MB,
        "--memory-limit-mb",
        envvar="RUNLAYER_MEMORY_LIMIT_MB",
        min=MIN_MEMORY_LIMIT_MB,
        max=MAX_MEMORY_LIMIT_MB,
        clamp=True,
        help=(
            "Abort the scan if its memory use grows more than this many MB "
            "(peak-RSS growth; Python-heap tracing where no RSS probe exists) "
            f"({MIN_MEMORY_LIMIT_MB}..{MAX_MEMORY_LIMIT_MB}, "
            f"default {DEFAULT_MEMORY_LIMIT_MB})"
        ),
    ),
    username: str | None = typer.Option(
        None,
        "--username",
        envvar="RUNLAYER_USERNAME",
        help="Override detected username (e.g., for MDM deployments running as root)",
    ),
    all_users: bool = typer.Option(
        False,
        "--all-users",
        help=(
            "Windows SYSTEM only: scan every real user profile, dropping "
            "privileges to each logged-on user (incl. Entra) and scanning "
            "logged-off users as SYSTEM with paths pointed at their profile."
        ),
    ),
    ca_bundle: str | None = typer.Option(
        None,
        "--ca-bundle",
        help="Path to a PEM CA bundle for TLS inspection proxies",
    ),
) -> None:
    """
    Scan all MCP client configurations and skill artifacts on this device.

    Discovers MCP servers and skill-like artifacts (SKILL.md, AGENTS.md,
    rule files) across Cursor, Claude Desktop, Claude Code, VS Code,
    Windsurf, and other supported clients.

    Examples:

        # Scan and submit to Runlayer
        runlayer scan

        # Dry run - print results without submitting
        runlayer scan --dry-run

        # With MDM-provided device ID
        runlayer scan --org-device-id $ASSET_TAG

        # Skip project scanning for faster results
        runlayer scan --no-projects
    """
    # If subcommand was invoked, let it handle things
    if ctx.invoked_subcommand is not None:
        return

    set_ca_bundle_path(ca_bundle)
    log_file_path = setup_logging(command="scan", quiet_console=quiet)
    try:
        scan_lock = acquire_scan_run_lock()
    except ScanRunLockError as exc:
        logger.warning("scan_run_lock_unavailable", error=str(exc))
    else:
        if scan_lock is None:
            logger.info("scan_skipped_lock_busy")
            raise typer.Exit(0)
        ctx.call_on_close(scan_lock.close)

    # SYSTEM-only fan-out: enumerate every real profile and scan each as the
    # user (token-drop when logged on, SYSTEM env-pointed when logged off).
    # Replaces the per-user Interactive scheduled-task fan-out, which couldn't
    # register a task for Entra (S-1-12-1) accounts. Credentials/device-id come
    # from HKLM in each child, so this path resolves no per-user secret itself.
    if all_users:
        from runlayer_cli.scan.windows_users import (  # noqa: PLC0415
            EXIT_MISCONFIG,
            run_all_users_scan,
        )

        # --dry-run can't be honored by the fan-out: each profile is scanned in
        # an isolated child whose stdout is captured (logged-off) or hidden
        # (logged-on, CREATE_NO_WINDOW), so a forwarded --dry-run would read
        # every profile yet surface nothing. Reject the combo rather than run
        # real child scans under a flag that implies none will run.
        if dry_run:
            logger.error("scan_all_users_dry_run_rejected")
            print_error(
                "--dry-run cannot be combined with --all-users. Preview a "
                "single profile with 'aiwatch scan --dry-run' instead.",
                str(log_file_path),
            )
            raise typer.Exit(EXIT_MISCONFIG)

        # SYSTEM's ~/.runlayer log lands under systemprofile (operators can't
        # find it), so also mirror this orchestrator process's full log output
        # (summary + per-profile lines plus any errors) to
        # C:\ProgramData\Runlayer\Logs\scheduled-task.log (best-effort).
        attach_system_scan_log_handler()

        raise typer.Exit(
            run_all_users_scan(
                scan_projects=not no_projects,
                project_timeout=project_timeout,
                project_depth=project_depth,
                cpu_cores=cpu_cores,
                max_cpu_percent=max_cpu_percent,
                memory_limit_mb=memory_limit_mb,
                artifact_lookup_cache=artifact_lookup_cache,
            )
        )

    set_credentials_in_context(ctx, secret, host, org_api_key_name=org_api_key)
    credentials = resolve_credentials(
        ctx,
        require_auth=not dry_run,
        allow_org_key=True,
        implicit_org_key_label=AI_WATCH_MDM_ORG_KEY_LABEL,
        interactive_login_on_missing=False,
    )
    effective_secret = credentials["secret"]
    effective_host = credentials["host"]

    # Best-effort distributed tracing: a CLI scan span + W3C propagation into the
    # backend ingest. No-op when unauthenticated, opted out, or OTEL unavailable.
    telemetry.init_cli_tracing(
        host=effective_host,
        api_key=effective_secret,
        collector_version=__version__,
    )

    try:
        with telemetry.command_span(
            "cli.scan", command="scan", collector_version=__version__
        ):
            _run_scan(
                effective_host=effective_host,
                effective_secret=effective_secret,
                device_id=device_id,
                org_device_id=org_device_id,
                dry_run=dry_run,
                verbose=verbose,
                quiet=quiet,
                no_projects=no_projects,
                project_depth=project_depth,
                project_timeout=project_timeout,
                cpu_cores=cpu_cores,
                max_cpu_percent=max_cpu_percent,
                memory_limit_mb=memory_limit_mb,
                username=username,
                detect_agents=detect_agents,
                detect_agent_frameworks=detect_agent_frameworks,
                detect_processes=detect_processes,
                detect_containers=detect_containers,
                detect_disguised_skills=detect_disguised_skills,
                artifact_lookup_cache=artifact_lookup_cache,
                detect_renamed_plugin_caches=detect_renamed_plugin_caches,
                log_file_path=log_file_path,
            )
    finally:
        telemetry.shutdown_cli_tracing()


def _report_detect_scan_failure(
    *,
    effective_host: str,
    effective_secret: str,
    dry_run: bool,
    error_message: str,
) -> None:
    """Best-effort Detect error check-in when a scan fails.

    So a failed scan surfaces a Detect *error* on the device instead of silence
    (Detect otherwise only reports on success). Skipped for dry-run / missing
    creds, and never raises — a check-in failure must not mask the scan error.
    """
    if dry_run or not effective_host or not effective_secret:
        return
    try:
        from runlayer_cli.aiwatch_checkin import (  # noqa: PLC0415
            _make_device_context,
            submit_detect_error_checkin,
        )

        client = RunlayerClient(hostname=effective_host, secret=effective_secret)
        submit_detect_error_checkin(
            client,
            ctx=_make_device_context(),
            error_message=error_message,
        )
    except Exception as exc:
        logger.debug("aiwatch_detect_error_checkin_skipped", error=str(exc))


def _submit_scan_checkins_best_effort(client: RunlayerClient, result) -> None:
    """Fire the best-effort scan check-ins without ever failing the scan.

    ``submit_all_scan_checkins`` isolates each individual check-in, but it runs
    *after* ``submit_scan_results`` has already succeeded. Any unexpected raise
    (e.g. its unguarded device-context prologue) must be swallowed here rather
    than propagate to the outer handler, which would mis-report a Detect
    *failure* + exit nonzero for a scan that actually persisted.

    The import lives inside the ``try`` so an import-time failure is swallowed
    too (matching ``_report_detect_scan_failure``); otherwise it would escape to
    the outer handler and trigger exactly the mis-report this guards against.
    """
    try:
        from runlayer_cli.aiwatch_checkin import (  # noqa: PLC0415
            submit_all_scan_checkins,
        )

        submit_all_scan_checkins(client, result)
    except Exception as exc:
        logger.warning(
            "aiwatch_scan_checkins_failed",
            error=str(exc),
            error_type=type(exc).__name__,
            exc_info=True,
        )


def _run_scan(
    *,
    effective_host: str,
    effective_secret: str,
    device_id: str | None,
    org_device_id: str | None,
    dry_run: bool,
    verbose: bool,
    quiet: bool,
    no_projects: bool,
    project_depth: int,
    project_timeout: int,
    cpu_cores: int,
    max_cpu_percent: int,
    memory_limit_mb: int,
    username: str | None,
    detect_agents: bool,
    detect_agent_frameworks: bool,
    detect_processes: bool,
    detect_containers: bool,
    detect_disguised_skills: bool,
    detect_renamed_plugin_caches: bool,
    log_file_path: object,
    artifact_lookup_cache: bool = False,
) -> None:
    try:
        if not quiet:
            typer.echo("Scanning MCP client configurations and skills...")

        result = scan_all_clients(
            device_id=device_id,
            org_device_id=org_device_id,
            collector_version=__version__,
            scan_projects=not no_projects,
            project_scan_timeout=project_timeout,
            project_scan_depth=project_depth,
            username_override=username,
            detect_agents=detect_agents,
            detect_agent_frameworks=detect_agent_frameworks,
            detect_processes=detect_processes,
            detect_containers=detect_containers,
            detect_disguised_skills=detect_disguised_skills,
            detect_renamed_plugin_caches=detect_renamed_plugin_caches,
            cpu_cores=cpu_cores,
            max_cpu_percent=max_cpu_percent,
            memory_limit_mb=memory_limit_mb,
        )
        agent_definition_count = _agent_definition_count(result)

        if verbose and not quiet:
            typer.echo(f"  Device ID: {result.device_id[:8]}...")
            typer.echo(f"  Hostname: {result.hostname}")
            typer.echo(f"  OS: {result.os} {result.os_version}")
            if result.detected_clients:
                typer.echo(f"  AI clients: {result.total_detected_clients}")
            for config in result.configurations:
                scope_label = f"[{config.config_scope}]"
                typer.echo(
                    f"  {config.client} {scope_label}: {len(config.servers)} servers"
                )
            if result.skills:
                global_skill_count = len(result.global_skills)
                user_skill_count = len(result.user_skills)
                project_skill_count = len(result.project_skills)
                typer.echo(
                    f"  Skills: {result.total_skills} "
                    f"({global_skill_count} global, {user_skill_count} user, "
                    f"{project_skill_count} project)"
                )
            if result.plugins:
                typer.echo(f"  Plugins: {result.total_plugins}")
            if result.agents:
                typer.echo(format_summary(result.agents, verbose=True))
            if agent_definition_count:
                typer.echo(f"  Agent definitions: {agent_definition_count}")
            if result.processes:
                typer.echo(f"  Runtime processes: {result.total_processes}")
                for proc in result.processes:
                    ports = (
                        f" :{','.join(str(p) for p in proc.listening_ports)}"
                        if proc.listening_ports
                        else ""
                    )
                    signals = (
                        f" [{', '.join(proc.ai_signals)}]" if proc.ai_signals else ""
                    )
                    typer.echo(
                        f"    {proc.kind} pid={proc.pid}{ports} "
                        f"conf={proc.confidence:.2f}{signals}"
                    )
            if result.containers:
                typer.echo(f"  Running containers: {result.total_containers}")
            if result.wsl_scanned:
                typer.echo(f"  WSL distributions: {result.total_wsl_distros}")

        if dry_run:
            if _no_findings(result):
                if not quiet:
                    typer.secho(
                        "No AI clients, MCP servers, skills, plugins, agents, "
                        "processes, or containers found.",
                        fg=typer.colors.YELLOW,
                    )
                raise typer.Exit(0)
            # to_full_payload owns the full dry-run view; both agent artifact
            # classes retain their richer local shape there.
            payload = result.to_full_payload(include_agents=True)
            typer.echo(json.dumps(payload, indent=2, default=str))
            raise typer.Exit(0)

        client = RunlayerClient(hostname=effective_host, secret=effective_secret)
        # SYSTEM fallback children point home variables at user-controlled
        # profiles, so they must never create a privileged cache file there.
        windows_system_context = is_windows_system_context()
        local_artifact_cache = (
            ArtifactCache(effective_host, effective_secret)
            if artifact_lookup_cache and not windows_system_context
            else None
        )

        # Best-effort liveness/health check-ins, independent of the submission
        # outcome (a rejected batch shows up via the WARN lines + nonzero exit
        # below; a re-raised auth error as a Detect *error* via
        # _report_detect_scan_failure). Ordered after submission so that
        # re-raise skips them. No-findings path just records liveness and exits.
        if _no_findings(result):
            _submit_scan_checkins_best_effort(client, result)
            if not quiet:
                typer.secho(
                    "No AI clients, MCP servers, skills, plugins, agents, "
                    "processes, or containers found.",
                    fg=typer.colors.YELLOW,
                )
            raise typer.Exit(0)

        if not quiet:
            global_count = len(result.global_configs)
            project_count = len(result.project_configs)
            wsl_count = len(result.wsl_configs)
            scope_counts = f"{global_count} global, {project_count} project"
            if wsl_count:
                scope_counts += f", {wsl_count} WSL"
            parts = [
                f"{result.total_servers} servers from "
                f"{len(result.configurations)} configs "
                f"({scope_counts})"
            ]
            if result.total_detected_clients:
                parts.append(f"{result.total_detected_clients} AI clients")
            if result.total_skills:
                parts.append(f"{result.total_skills} skills")
            if result.total_plugins:
                parts.append(f"{result.total_plugins} plugins")
            if result.total_agents:
                parts.append(f"{result.total_agents} agents")
            if result.containers_scanned:
                parts.append(f"{result.total_containers} running containers")
            if result.wsl_scanned:
                parts.append(f"{result.total_wsl_distros} WSL distributions")
            typer.echo(f"Submitting {', '.join(parts)}...")

        submission = submit_scan_results(
            client,
            result,
            artifact_cache=local_artifact_cache,
        )

        _submit_scan_checkins_best_effort(client, result)

        if submission.unsupported and not quiet:
            typer.secho(
                f"{WARN} {' and '.join(submission.unsupported)} "
                "not supported by this server",
                fg=typer.colors.YELLOW,
            )

        if submission.failed_submissions and not quiet:
            typer.secho(
                f"{WARN} Could not submit "
                f"{' and '.join(submission.failed_submissions)}; "
                "scan may be incomplete",
                fg=typer.colors.YELLOW,
            )

        # The WARN lines above already told the user what happened; here we only
        # act on the exit-code policy the orchestrator computed.
        exit_code = submission.exit_code
        if exit_code != 0:
            logger.warning(
                "Scan did not persist all findings",
                exit_code=exit_code,
                unsupported=submission.unsupported,
                failed_submissions=submission.failed_submissions,
            )
            raise typer.Exit(exit_code)

        response = submission.response
        if not quiet:
            if response:
                msg = (
                    f"{OK} Scan complete: {response['servers_processed']} servers, "
                    f"{response['shadow_servers_found']} shadow, "
                    f"{response['managed_servers_matched']} managed"
                )
            else:
                msg = f"{OK} Scan complete: 0 servers"
            if result.total_detected_clients:
                msg += f", {result.total_detected_clients} AI clients detected"
            if result.total_skills:
                msg += f", {result.total_skills} skills discovered"
            if result.total_plugins:
                msg += f", {result.total_plugins} plugins detected"
            if result.total_agents:
                msg += f", {result.total_agents} agents discovered"
            if agent_definition_count:
                msg += f", {agent_definition_count} agent definitions discovered"
            if result.containers_scanned:
                msg += f", {result.total_containers} running containers"
            if result.wsl_scanned:
                msg += f", {result.total_wsl_distros} WSL distributions"
            typer.secho(msg, fg=typer.colors.GREEN)

        logger.info(
            "Scan completed successfully",
            servers_processed=response["servers_processed"] if response else 0,
            shadow_servers=response["shadow_servers_found"] if response else 0,
            managed_servers=response["managed_servers_matched"] if response else 0,
            clients_detected=result.total_detected_clients,
            skills_discovered=result.total_skills,
            plugins_detected=result.total_plugins,
            agents_discovered=result.total_agents,
            agent_definitions_discovered=agent_definition_count,
            running_containers=result.total_containers,
            wsl_distros=result.total_wsl_distros,
        )

    except typer.Exit:
        raise
    except Exception as e:
        logger.error(
            "Scan failed",
            error=str(e),
            error_type=type(e).__name__,
            exc_info=True,
        )
        _report_detect_scan_failure(
            effective_host=effective_host,
            effective_secret=effective_secret,
            dry_run=dry_run,
            error_message=str(e),
        )
        print_error(str(e), str(log_file_path))
        raise typer.Exit(1)
