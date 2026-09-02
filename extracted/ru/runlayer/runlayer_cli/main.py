from runlayer_cli.truststore_init import inject as _inject_truststore

_inject_truststore()

# ruff: noqa: E402 - imports below intentionally come after _inject_truststore() and warnings.filterwarnings()
import os
import sys
import warnings
from functools import partial
from typing import Optional, Union
from uuid import UUID

warnings.filterwarnings("ignore", message="authlib.jose module is deprecated")

import anyio
import structlog
import typer
from fastmcp.client.transports import (
    SSETransport,
    StdioTransport,
    StreamableHttpTransport,
)
from fastmcp.server.proxy import FastMCPProxy, ProxyClient

from runlayer_cli import flow_trace
from runlayer_cli.error_classification import classify_exception
from runlayer_cli.flow_delivery import FlowDeliveryQueue
from runlayer_cli.identity_forward import (
    merge_bundle_into_headers,
    refresh_loop as identity_forward_refresh_loop,
)
from runlayer_cli.middleware import RunlayerMiddleware
from runlayer_cli.models import ServerDetails
from runlayer_cli.oauth import OAuth
from runlayer_cli.api import RunlayerClient, USER_AGENT
from runlayer_cli.commands.auth import login, logout
from runlayer_cli.commands.cache import app as cache_app
from runlayer_cli.commands.catalog import app as catalog_app
from runlayer_cli.commands.credentials import app as credentials_app
from runlayer_cli.commands.decide_approval import decide_approval
from runlayer_cli.commands.deploy import app as deploy_app
from runlayer_cli.commands.doctor import doctor
from runlayer_cli.commands.hooks import app as hooks_app
from runlayer_cli.commands.keychain import app as keychain_app, maybe_auto_adopt
from runlayer_cli.commands.logs import logs
from runlayer_cli.commands.org_api_key import app as org_api_key_app
from runlayer_cli.commands.plugins import app as plugins_app
from runlayer_cli.commands.reconnect_account import reconnect_account
from runlayer_cli.commands.reject_access_request import reject_access_request
from runlayer_cli.commands.scan import app as scan_app
from runlayer_cli.commands.setup import app as setup_app
from runlayer_cli.commands.skills import app as skills_app
from runlayer_cli.commands.status import status
from runlayer_cli.commands.terraform import app as terraform_app
from runlayer_cli.commands.cli_update import scheduled_update
from runlayer_cli.commands.schedule import schedule
from runlayer_cli.commands.update import privileged_update, update
from runlayer_cli.commands.url_handler import handle_url
from runlayer_cli.console import print_error
from runlayer_cli import __version__
from runlayer_cli.hook import TRANSCRIPT_STREAM_WORKER_SENTINEL
from runlayer_cli.config import resolve_credentials, set_credentials_in_context
from runlayer_cli.logging import setup_logging
from runlayer_cli.tls import async_http_client, set_ca_bundle_path
from runlayer_cli.verified_local_proxy.config import VERIFICATION_CONFIGS
from runlayer_cli.verified_local_proxy.proxy import run_proxy as run_verified_proxy
from runlayer_cli.uuid_utils import is_uuid

logger = structlog.get_logger("cli")


def _build_stdio_env(transport_config: dict[str, object]) -> dict[str, str]:
    env = dict(os.environ)
    config_env = transport_config.get("env")
    if isinstance(config_env, dict):
        for key, value in config_env.items():
            if isinstance(key, str) and isinstance(value, str):
                env[key] = value
    return env


def _resolve_server_id(runlayer_api_client: RunlayerClient, target: str) -> str:
    if is_uuid(target):
        return target
    return runlayer_api_client.resolve_server_target(target)


def _oauth_for_server(server: ServerDetails, callback_port: int | None = None) -> OAuth:
    manual = server.requires_manual_oauth_setup
    if manual and not server.manual_oauth_client_id:
        raise ValueError("Manual OAuth setup is incomplete: client ID is required.")

    return OAuth(
        mcp_url=server.url,
        client_name=USER_AGENT,
        # IdPs match the redirect URI exactly, so a server-configured fixed
        # port beats the random per-machine default; an explicit flag wins.
        # Manual-only: a stale stored port must not constrain DCR/broker
        # flows after the server leaves manual registration.
        callback_port=callback_port
        or (server.manual_oauth_callback_port if manual else None),
        manual_client_id=(server.manual_oauth_client_id if manual else None),
        manual_client_secret=(server.manual_oauth_client_secret if manual else None),
        scopes=(server.manual_oauth_scopes if manual else None),
        # oauth.py owns the secret-less default ("none" for public PKCE clients).
        token_endpoint_auth_method=server.preferred_token_endpoint_auth_method,
    )


def version_callback(value: bool):
    """Show version information."""
    if value:
        typer.echo(f"runlayer version {__version__}")
        raise typer.Exit()


app = typer.Typer(help="Run MCP servers via HTTP transport")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool | None = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
    secret: str | None = typer.Option(
        None,
        "--secret",
        "-s",
        help="API secret for authentication (optional if logged in)",
    ),
    host: str | None = typer.Option(
        None,
        "--host",
        "-H",
        help="Runlayer host URL (required if not in config)",
    ),
    org_api_key: str | None = typer.Option(
        None,
        "--org-api-key",
        help="Name of a stored org API key to use for authentication",
    ),
    ca_bundle: str | None = typer.Option(
        None,
        "--ca-bundle",
        help="Path to a PEM CA bundle for TLS inspection proxies",
    ),
):
    """Runlayer CLI - Run MCP servers via HTTP transport."""
    ctx.ensure_object(dict)
    ctx.obj["secret"] = secret
    ctx.obj["host"] = host
    ctx.obj["org_api_key_name"] = org_api_key
    set_ca_bundle_path(ca_bundle)
    maybe_auto_adopt(ctx.invoked_subcommand)
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


@app.command(name="run", help="Run an MCP server via HTTP transport")
def run(
    ctx: typer.Context,
    target: str = typer.Argument(
        ..., help="UUID or supported alias of the MCP server to run"
    ),
    secret: Optional[str] = typer.Option(
        None,
        "--secret",
        "-s",
        help="API secret for authentication (optional if logged in)",
    ),
    host: Optional[str] = typer.Option(
        None,
        "--host",
        "-H",
        help="Runlayer host URL (required if not in config)",
    ),
    oauth_callback_port: Optional[int] = typer.Option(
        None,
        "--oauth-callback-port",
        envvar="RUNLAYER_OAUTH_CALLBACK_PORT",
        min=1,
        max=65535,
        help=(
            "Fixed localhost port for the OAuth callback server; register "
            "http://localhost:<port>/callback in the IdP redirect-URI allowlist "
            "(for IdPs without wildcard port support, e.g. Okta)."
        ),
    ),
    ca_bundle: Optional[str] = typer.Option(
        None,
        "--ca-bundle",
        help="Path to a PEM CA bundle for TLS inspection proxies",
    ),
):
    log_file_path = setup_logging(command="run", quiet_console=True)

    set_ca_bundle_path(ca_bundle)
    set_credentials_in_context(ctx, secret, host)
    credentials = resolve_credentials(ctx, require_auth=True)
    effective_host = credentials["host"]
    effective_secret = credentials["secret"]

    try:
        # Flow tracing: completed flow summaries go to the local log file and a
        # lag-one queue that piggybacks them onto the next pre/post call (see
        # flow_delivery). RUNLAYER_FLOW_TRACE=0 disables.
        flow_queue = FlowDeliveryQueue()

        def _flow_sink(summary: dict) -> None:
            logger.info("flow_trace", **summary)
            flow_queue.enqueue(summary)

        flow_trace.enable_flow_tracing(_flow_sink)
        # Sanitized failure classification for errored flows (closed
        # vocabulary + optional HTTP status; never message text). Injected
        # here because the classifier needs httpx/mcp types, which must stay
        # out of the flow_* stdlib-only closure (cli/AGENTS.md).
        flow_trace.set_error_classifier(classify_exception)

        runlayer_api_client = RunlayerClient(
            hostname=effective_host, secret=effective_secret, flow_queue=flow_queue
        )

        server_id = _resolve_server_id(runlayer_api_client, target)
        # Stamp every flow summary with the server this process runs, so
        # server-side triage doesn't need the customer's local log files.
        flow_trace.set_server_id(server_id)
        server_details = runlayer_api_client.get_server_details(server_id)
        server_name = server_details.name

        # Check if this server maps to a verified-local config (e.g. Figma Desktop).
        # If so, do codesign verification and proxy to localhost instead of using
        # the backend URL, while still keeping RunlayerMiddleware for governance.
        verified_local_config = VERIFICATION_CONFIGS.get(
            server_details.catalog_entry_name or ""
        )
        if verified_local_config:
            logger.info(
                "Verified-local server detected",
                server_name=server_name,
                catalog_entry=server_details.catalog_entry_name,
            )
            middleware = RunlayerMiddleware(
                runlayer_api_client=runlayer_api_client,
                proxy=None,  # Set by create_proxy
                server=server_details,
            )
            verified_headers: dict[str, str] = {}
            verified_bundle = server_details.identity_forward
            merge_bundle_into_headers(verified_headers, verified_bundle)

            refresher = None
            if verified_bundle is not None and verified_bundle.needs_refresh:
                refresher = partial(
                    identity_forward_refresh_loop,
                    runlayer_api_client,
                    server_id,
                    verified_bundle,
                    verified_headers,
                )

            run_verified_proxy(
                verified_local_config,
                middleware=middleware,
                identity_forward_headers=verified_headers or None,
                identity_forward_refresher=refresher,
            )
            return

        headers_dict = {}
        headers_dict["User-Agent"] = USER_AGENT

        # Identity-forward headers arrive on the server-details read — the
        # backend can't inject them on a connection the CLI owns. ``None``
        # (stdio, toggles off, older backend) merges as a no-op.
        identity_forward_bundle = server_details.identity_forward
        merge_bundle_into_headers(headers_dict, identity_forward_bundle)

        transport: Union[SSETransport, StdioTransport, StreamableHttpTransport]
        match server_details.transport_type:
            case "sse":
                transport = SSETransport(
                    url=server_details.url,
                    headers=headers_dict,
                    auth=_oauth_for_server(
                        server_details, callback_port=oauth_callback_port
                    ),
                    httpx_client_factory=async_http_client,
                )
            case "stdio":
                transport_config = server_details.transport_config or {}
                transport = StdioTransport(
                    command=server_details.url,
                    args=transport_config.get("args", []),
                    env=_build_stdio_env(transport_config),
                )
            case "streaming-http":
                transport = StreamableHttpTransport(
                    url=server_details.url,
                    headers=headers_dict,
                    auth=_oauth_for_server(
                        server_details, callback_port=oauth_callback_port
                    ),
                    httpx_client_factory=async_http_client,
                )
            case _:
                raise ValueError(
                    f"Unknown transport type: {server_details.transport_type}"
                )

        proxy_client = ProxyClient(transport)

        # Create a factory that reuses the same client instead of creating new ones.
        # This is critical for SSE transports - creating a new SSE connection for each
        # request causes timeouts because some servers (like Atlassian) don't properly
        # respond to subsequent SSE connections from the same OAuth token.
        def reuse_client_factory() -> ProxyClient:
            return proxy_client

        proxy = FastMCPProxy(client_factory=reuse_client_factory, name=server_name)

        middleware = RunlayerMiddleware(
            runlayer_api_client=runlayer_api_client,
            proxy=proxy,
            server=server_details,
        )
        proxy.add_middleware(middleware)

        logger.info(
            "Starting Runlayer CLI",
            server_name=server_name,
            server_id=server_id,
            target=target,
        )

        async def tasks():
            async with anyio.create_task_group() as tg:
                middleware.background_tasks = tg
                # Signed identity tokens expire after ~5min; keep them
                # fresh for the proxy's lifetime.
                if (
                    identity_forward_bundle is not None
                    and identity_forward_bundle.needs_refresh
                ):
                    tg.start_soon(
                        identity_forward_refresh_loop,
                        runlayer_api_client,
                        server_id,
                        identity_forward_bundle,
                        headers_dict,
                    )

                # Eager kick (stdio only): clients cache tools/list across
                # reconnects, so the on_list_tools hook alone may never fire.
                # Background, so serving starts immediately either way. Remote
                # transports stay lazy — eager connect could trigger OAuth
                # flows at startup.
                if server_details.transport_type == "stdio":
                    await middleware.maybe_start_sync()
                try:
                    await proxy.run_stdio_async(
                        show_banner=False,
                    )
                finally:
                    # Serving is done; don't let a still-hanging background
                    # sync keep the process alive.
                    tg.cancel_scope.cancel()

        anyio.run(tasks)
    except KeyboardInterrupt:
        logger.info("MCP server shutdown requested by user")
    except Exception as e:
        logger.error(
            "Error running MCP server",
            error=str(e),
            error_type=type(e).__name__,
            exc_info=True,
        )
        print_error(str(e), str(log_file_path))
        raise typer.Exit(1)


app.command(name="login", help="Authenticate with Runlayer")(login)
app.command(name="logout", help="Clear saved credentials")(logout)
app.command(
    name="doctor",
    help="Preflight OAuth/connectivity checks for an MCP server (read-only)",
)(doctor)
app.command(name="logs", help="Query audit logs")(logs)
app.command(name="status", help="Show local CLI and hook status")(status)
app.command(name="update", help="Install the backend-selected CLI version")(update)
app.command(
    name="schedule",
    help="Run due scheduled tasks once; packaging provides the cadence",
)(schedule)
app.command(name="__handle-url", hidden=True)(handle_url)
app.command(name="__decide-approval", hidden=True)(decide_approval)
app.command(name="__reconnect-account", hidden=True)(reconnect_account)
app.command(name="__reject-access-request", hidden=True)(reject_access_request)
app.command(name="__scheduled-update", hidden=True)(scheduled_update)
app.command(name="__self-update-root", hidden=True)(privileged_update)
app.add_typer(cache_app, name="cache")
app.add_typer(catalog_app, name="catalog")
app.add_typer(credentials_app, name="credentials")
app.add_typer(deploy_app, name="deploy")
app.add_typer(hooks_app, name="hooks")
app.add_typer(keychain_app, name="keychain")
app.add_typer(org_api_key_app, name="org-api-key")
app.add_typer(setup_app, name="setup")
app.add_typer(scan_app, name="scan")
app.add_typer(skills_app, name="skills")
app.add_typer(plugins_app, name="plugins")
app.add_typer(terraform_app, name="terraform")


def _ensure_backwards_compatibility():
    """Ensure backwards compatibility with the initial CLI release.

    The first version allowed: runlayer <uuid> --secret <key>
    The current version requires: runlayer run <uuid> --secret <key>

    This function detects when a UUID is passed as the first argument
    and automatically inserts the "run" subcommand for backwards compatibility.
    """

    if len(sys.argv) < 2:
        return

    current_command = sys.argv[1]
    commands = app.registered_commands

    if current_command in commands:
        return

    try:
        UUID(current_command)
        sys.argv.insert(1, "run")
    except ValueError:
        pass


_HOOK_SUBCOMMAND = "hook"


def cli():
    # Fast in-process hook dispatch, mirroring ``aiwatch.py:main``. ``runlayer
    # hook [--client X] [--no-enforcement]`` is wired into each AI client's hook
    # config by ``runlayer setup hooks --install`` and fires here before the
    # typer app loads. The sentinel comes from the lightweight ``hook`` package
    # and each branch lazy-imports its target, so non-hook commands never load
    # the heavy ``relay`` chain.
    if len(sys.argv) >= 2 and sys.argv[1] == TRANSCRIPT_STREAM_WORKER_SENTINEL:
        from runlayer_cli.hook import _transcript_stream_worker  # noqa: PLC0415

        sys.argv = [sys.argv[0], *sys.argv[2:]]
        _transcript_stream_worker.main()
        return

    if len(sys.argv) >= 2 and sys.argv[1] == _HOOK_SUBCOMMAND:
        from runlayer_cli.hook.dispatch import run_hook  # noqa: PLC0415

        sys.argv = [sys.argv[0], *sys.argv[2:]]
        run_hook()
        return

    _ensure_backwards_compatibility()

    # Best-effort per-command perf telemetry (command time, CPU, peak memory).
    # Deferred import keeps it off the fast hook-dispatch branches above.
    from runlayer_cli.command_metrics import (  # noqa: PLC0415
        run_with_command_metrics,
    )

    run_with_command_metrics(app)


if __name__ == "__main__":
    cli()
