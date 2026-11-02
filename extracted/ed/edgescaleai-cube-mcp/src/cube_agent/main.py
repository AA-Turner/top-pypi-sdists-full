"""cube-agent — thin local MCP agent.

Presents a unified tool surface to the MCP client. Each tool is routed to
either local execution or proxied to cube-cloud transparently.

Local tools (only needs Docker for builds):
- build_and_publish_to_apollo: Docker buildx + pure Python chart packaging + OCI push
- app_proxy / app_proxy_stop / app_proxy_status: tunnel via cube-cloud (Phase 4)

Remote tools (proxied to cube-cloud):
- All Apollo environment/entity management tools
- Server-side kubectl/Teleport tools

Auth tools (local):
- agent_login_browser / agent_logout / agent_status
"""

from __future__ import annotations

import asyncio
import logging
import sys

import truststore
from mcp.server import stdio
from mcp.server.lowlevel import Server
from mcp.types import TextContent, Tool

from cube_agent.auth.login import login_browser, logout, status as auth_status
from cube_agent.local.build_pipeline import build_and_publish
from cube_agent.remote.client import CloudClient, CloudClientError
from cube_agent.remote.proxy_tools import REMOTE_TOOL_NAMES, REMOTE_TOOLS
from cube_agent.tunnel.agent_tunnel import start_proxy, stop_proxy, proxy_status

logger = logging.getLogger(__name__)

mcp_server = Server("cube-agent")

# ---------------------------------------------------------------------------
# Local-only tools
# ---------------------------------------------------------------------------

LOCAL_TOOLS: list[Tool] = [
    Tool(
        name="build_and_publish_to_apollo",
        description=(
            "Build and publish an app to Apollo Container Registry. Builds the "
            "Docker image (locally via buildx, or remotely via cube-cloud/kaniko "
            "when no local Docker daemon is present), packages the Helm chart "
            "(pure Python, honoring the chart's .helmignore), pushes to the OCI "
            "registry, and publishes the manifest via cube-cloud."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "chart_path": {
                    "type": "string",
                    "description": "Path to chart directory or Chart.yaml (auto-detected if not specified).",
                },
                "version": {
                    "type": "string",
                    "description": 'Exact version to use (e.g., "1.0.0"). If not specified, bumps current version.',
                },
                "bump": {
                    "type": "string",
                    "description": 'Version bump type: "patch" (default), "minor", or "major".',
                    "default": "patch",
                },
                "app_version": {
                    "type": "string",
                    "description": (
                        "Chart appVersion, i.e. the image tag the chart deploys. When "
                        "an image is built, defaults to the chart version and is the "
                        "tag pushed. When no image is built (skip_docker, or no "
                        "Dockerfile), appVersion is left unchanged unless this is "
                        "given — pass it to point the chart at an image built "
                        "separately, and make sure that tag exists. A dockerfile "
                        "that is named but not found is not a chart-only publish: "
                        "appVersion is then left unchanged even if this is given."
                    ),
                },
                "skip_docker": {
                    "type": "boolean",
                    "description": (
                        "Skip Docker build/push even if Dockerfile exists. The chart's "
                        "appVersion is then kept unless app_version is given."
                    ),
                    "default": False,
                },
                "dry_run": {
                    "type": "boolean",
                    "description": "Show what would be done without actually doing it.",
                    "default": False,
                },
                "build_args": {
                    "type": "object",
                    "description": (
                        'Build-time variables passed to Docker as --build-arg key=value '
                        '(e.g., {"NPM_TOKEN": "abc123"}).'
                    ),
                    "additionalProperties": {"type": "string"},
                },
                "dockerfile": {
                    "type": "string",
                    "description": (
                        "Path to the Dockerfile, if not the default in the chart "
                        "directory or its parent (e.g. Dockerfile.prod)."
                    ),
                },
                "target": {
                    "type": "string",
                    "description": "Build stage to target in a multi-stage Dockerfile.",
                },
                "build_mode": {
                    "type": "string",
                    "enum": ["auto", "local", "remote"],
                    "description": (
                        "Where to build the image. 'auto' (default) uses local "
                        "docker buildx if a daemon is present, otherwise builds "
                        "remotely via cube-cloud/kaniko. 'local' forces buildx; "
                        "'remote' forces the server-side build (no local Docker)."
                    ),
                    "default": "auto",
                },
                "platform": {
                    "type": "string",
                    "description": "Target image platform. Defaults to 'linux/amd64' (the cube architecture).",
                    "default": "linux/amd64",
                },
                "show_build_log": {
                    "type": "boolean",
                    "description": (
                        "For remote builds, include the kaniko build-log tail in "
                        "the result on success, so build output (e.g. build-arg "
                        "effects) is visible without CloudWatch access. Defaults "
                        "to false to keep successful builds terse; set true when "
                        "debugging. Build-log output is always included on failure."
                    ),
                    "default": False,
                },
            },
        },
    ),
    # Phase 4: App proxy tunnel tools
    Tool(
        name="app_proxy",
        description=(
            "Port-forward an ALREADY-EXPOSED app to a local TCP port, via "
            "cube-cloud's WebSocket relay. No tsh needed locally. Works for ANY "
            "exposed app, HTTP or tcp://, and is the only way into a tcp:// one "
            "(the app's public URL serves HTTP/WebSocket only). Use it whenever a "
            "local port is what you want — psql, an MQTT client, scripting, "
            "port-restricted tooling. Independent of the app's public URL: both "
            "work at once and neither affects the other. Requires expose to have "
            "been run — it cannot reach a service that was never exposed."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "app": {
                    "type": "string",
                    "description": "Qualified app name, as shown by list_exposed / app_list.",
                },
                "port": {
                    "type": "integer",
                    "description": "Local port to listen on (auto-assigned if not specified).",
                },
            },
            "required": ["app"],
        },
    ),
    Tool(
        name="app_proxy_stop",
        description="Stop a running app proxy tunnel.",
        inputSchema={
            "type": "object",
            "properties": {
                "app": {
                    "type": "string",
                    "description": "App name to stop. If not specified, stops all proxies.",
                },
            },
        },
    ),
    Tool(
        name="app_proxy_status",
        description="Show status of running app proxy tunnels.",
        inputSchema={"type": "object", "properties": {}},
    ),
    # Auth tools
    Tool(
        name="agent_login_browser",
        description="Authenticate via browser login (opens sign-in page, auto-provisions API key).",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="agent_logout",
        description="Remove stored cube-agent API key.",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="agent_status",
        description="Check cube-agent authentication and connectivity status.",
        inputSchema={"type": "object", "properties": {}},
    ),
]

LOCAL_TOOL_NAMES = {t.name for t in LOCAL_TOOLS}


# ---------------------------------------------------------------------------
# Tool listing — unified surface
# ---------------------------------------------------------------------------


@mcp_server.list_tools()
async def list_tools() -> list[Tool]:
    return REMOTE_TOOLS + LOCAL_TOOLS


# ---------------------------------------------------------------------------
# Tool dispatch
# ---------------------------------------------------------------------------


@mcp_server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        result = await _dispatch(name, arguments)
    except Exception as e:
        result = f"Error: {e}"
    return [TextContent(type="text", text=result)]


async def _dispatch(name: str, args: dict) -> str:
    # Local tools — executed in-process
    if name == "build_and_publish_to_apollo":
        return await build_and_publish(
            chart_path=args.get("chart_path"),
            version=args.get("version"),
            bump=args.get("bump", "patch"),
            app_version=args.get("app_version"),
            skip_docker=args.get("skip_docker", False),
            dry_run=args.get("dry_run", False),
            build_args=args.get("build_args"),
            dockerfile=args.get("dockerfile"),
            target=args.get("target"),
            build_mode=args.get("build_mode", "auto"),
            platform=args.get("platform", "linux/amd64"),
            show_build_log=args.get("show_build_log", False),
        )

    # Phase 4: App proxy tunnel (local TCP listener + WebSocket relay)
    if name == "app_proxy":
        return await start_proxy(args["app"], args.get("port"))
    if name == "app_proxy_stop":
        return await stop_proxy(args.get("app"))
    if name == "app_proxy_status":
        return await proxy_status()

    # Auth tools
    if name == "agent_login_browser":
        return await login_browser()
    if name == "agent_logout":
        return logout()
    if name == "agent_status":
        lines = [auth_status()]
        async with CloudClient() as cloud:
            try:
                await cloud.call_tool("list_environments", {"search": "__ping__"})
                lines.append("cube-cloud: connected")
            except CloudClientError as e:
                lines.append(f"cube-cloud: {e}")
            except Exception:
                lines.append("cube-cloud: unreachable")
        return "\n".join(lines)

    # Remote tools — proxy to cube-cloud
    if name in REMOTE_TOOL_NAMES:
        async with CloudClient() as cloud:
            return await cloud.call_tool(name, args)

    return f"Unknown tool: {name}"


# ---------------------------------------------------------------------------
# Entry points
# ---------------------------------------------------------------------------


def cli():
    """Entry point for the cube-agent CLI (stdio MCP server)."""
    # Route ALL TLS verification in this process through the OS trust store
    # (macOS Keychain, Windows cert store, Linux CA paths), so every client
    # trusts corporate / TLS-inspection CAs — the proxied tool calls (httpx in
    # remote/client.py), the app tunnel (websockets in tunnel/agent_tunnel.py),
    # and the build/publish uploads (httpx to S3 + ACR) — not just the login
    # flow. Without this, only login (which builds its own truststore
    # SSLContext) survives behind a TLS-inspecting proxy such as McAfee Web
    # Gateway; everything else falls back to certifi and fails cert
    # verification. Must run before any SSLContext is created.
    truststore.inject_into_ssl()

    logging.basicConfig(level=logging.INFO, stream=sys.stderr)

    async def run():
        async with stdio.stdio_server() as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    asyncio.run(run())


if __name__ == "__main__":
    cli()
