"""Scan command for MCP Watch."""

import json
from typing import Any

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
from runlayer_cli.logging import setup_logging
from runlayer_cli.tls import set_ca_bundle_path
from runlayer_cli.scan.service import (
    scan_all_clients,
    submit_discovered_plugins,
    submit_discovered_skills,
)

logger = structlog.get_logger(__name__)

app = typer.Typer(help="Scan MCP client configurations")


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
    project_depth: int = typer.Option(
        7,
        "--project-depth",
        help="Maximum directory depth for project scanning",
    ),
    project_timeout: int = typer.Option(
        60,
        "--project-timeout",
        help="Timeout in seconds for project scanning",
    ),
    username: str | None = typer.Option(
        None,
        "--username",
        envvar="RUNLAYER_USERNAME",
        help="Override detected username (e.g., for MDM deployments running as root)",
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
        )

        if verbose and not quiet:
            typer.echo(f"  Device ID: {result.device_id[:8]}...")
            typer.echo(f"  Hostname: {result.hostname}")
            typer.echo(f"  OS: {result.os} {result.os_version}")
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

        if (
            result.total_servers == 0
            and result.total_skills == 0
            and result.total_plugins == 0
        ):
            if not quiet:
                typer.secho(
                    "No MCP servers, skills, or plugins found.",
                    fg=typer.colors.YELLOW,
                )
            raise typer.Exit(0)

        if dry_run:
            payload = result.to_api_payload()
            if result.skills:
                payload["skills"] = [s.to_api_payload() for s in result.skills]
            if result.plugins:
                payload["plugins"] = [p.to_api_payload() for p in result.plugins]
            typer.echo(json.dumps(payload, indent=2, default=str))
            raise typer.Exit(0)

        if not quiet:
            global_count = len(result.global_configs)
            project_count = len(result.project_configs)
            parts = [
                f"{result.total_servers} servers from "
                f"{len(result.configurations)} configs "
                f"({global_count} global, {project_count} project)"
            ]
            if result.total_skills:
                parts.append(f"{result.total_skills} skills")
            if result.total_plugins:
                parts.append(f"{result.total_plugins} plugins")
            typer.echo(f"Submitting {', '.join(parts)}...")

        client = RunlayerClient(hostname=effective_host, secret=effective_secret)

        response: dict[str, Any] | None = None
        unsupported: list[str] = []
        failed_submissions: list[str] = []

        if result.total_servers > 0:
            response = client.submit_mcp_watch_scan(result.to_api_payload())
            if response.get("unsupported"):
                unsupported.append("Shadow MCP Detection")
                response = None

        if result.skills:
            skill_submission = submit_discovered_skills(client, result.skills, result)
            if skill_submission == "unsupported":
                unsupported.append("Shadow Skill Detection")
            elif skill_submission == "failed":
                failed_submissions.append("skills")

        if result.plugins:
            plugin_submission = submit_discovered_plugins(
                client, result.plugins, result
            )
            if plugin_submission == "unsupported":
                unsupported.append("Shadow Plugin Detection")
            elif plugin_submission == "failed":
                failed_submissions.append("plugins")

        if unsupported and not quiet:
            typer.secho(
                f"{WARN} {' and '.join(unsupported)} not supported by this server",
                fg=typer.colors.YELLOW,
            )

        if failed_submissions and not quiet:
            typer.secho(
                f"{WARN} Could not submit {' and '.join(failed_submissions)}; "
                "scan may be incomplete",
                fg=typer.colors.YELLOW,
            )

        if not quiet:
            if response:
                msg = (
                    f"{OK} Scan complete: {response['servers_processed']} servers, "
                    f"{response['shadow_servers_found']} shadow, "
                    f"{response['managed_servers_matched']} managed"
                )
            else:
                msg = f"{OK} Scan complete: 0 servers"
            if result.total_skills:
                msg += f", {result.total_skills} skills discovered"
            if result.total_plugins:
                msg += f", {result.total_plugins} plugins detected"
            typer.secho(msg, fg=typer.colors.GREEN)

        logger.info(
            "Scan completed successfully",
            servers_processed=response["servers_processed"] if response else 0,
            shadow_servers=response["shadow_servers_found"] if response else 0,
            managed_servers=response["managed_servers_matched"] if response else 0,
            skills_discovered=result.total_skills,
            plugins_detected=result.total_plugins,
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
        print_error(str(e), str(log_file_path))
        raise typer.Exit(1)
