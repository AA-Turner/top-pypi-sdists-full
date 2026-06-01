from runlayer_cli.truststore_init import inject as _inject_truststore

_inject_truststore()

# ruff: noqa: E402 - imports below intentionally come after _inject_truststore() and warnings.filterwarnings()
import os
import sys
import warnings
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

from runlayer_cli.middleware import RunlayerMiddleware
from runlayer_cli.oauth import OAuth
from runlayer_cli.api import RunlayerClient, USER_AGENT
from runlayer_cli.sync import sync_local_capabilities
from runlayer_cli.commands.auth import login, logout
from runlayer_cli.commands.cache import app as cache_app
from runlayer_cli.commands.credentials import app as credentials_app
from runlayer_cli.commands.deploy import app as deploy_app
from runlayer_cli.commands.hooks import app as hooks_app
from runlayer_cli.commands.logs import logs
from runlayer_cli.commands.org_api_key import app as org_api_key_app
from runlayer_cli.commands.plugins import app as plugins_app
from runlayer_cli.commands.scan import app as scan_app
from runlayer_cli.commands.setup import app as setup_app
from runlayer_cli.commands.skills import app as skills_app
from runlayer_cli.commands.terraform import app as terraform_app
from runlayer_cli.console import print_error
from runlayer_cli import __version__
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
        runlayer_api_client = RunlayerClient(
            hostname=effective_host, secret=effective_secret
        )

        server_id = _resolve_server_id(runlayer_api_client, target)
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
            run_verified_proxy(verified_local_config, middleware=middleware)
            return

        headers_dict = {}
        headers_dict["User-Agent"] = USER_AGENT

        transport: Union[SSETransport, StdioTransport, StreamableHttpTransport]
        match server_details.transport_type:
            case "sse":
                transport = SSETransport(
                    url=server_details.url,
                    headers=headers_dict,
                    auth=OAuth(mcp_url=server_details.url, client_name=USER_AGENT),
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
                    auth=OAuth(mcp_url=server_details.url, client_name=USER_AGENT),
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

        proxy.add_middleware(
            RunlayerMiddleware(
                runlayer_api_client=runlayer_api_client,
                proxy=proxy,
                server=server_details,
            )
        )

        logger.info(
            "Starting Runlayer CLI",
            server_name=server_name,
            server_id=server_id,
            target=target,
        )

        async def tasks():
            if (
                server_details.sync_required
                and server_details.transport_type == "stdio"
            ):
                await sync_local_capabilities(runlayer_api_client, proxy, server_id)
            await proxy.run_stdio_async(
                show_banner=False,
            )

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
app.command(name="logs", help="Query audit logs")(logs)
app.add_typer(cache_app, name="cache")
app.add_typer(credentials_app, name="credentials")
app.add_typer(deploy_app, name="deploy")
app.add_typer(hooks_app, name="hooks")
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


def cli():
    _ensure_backwards_compatibility()
    app()


if __name__ == "__main__":
    cli()
