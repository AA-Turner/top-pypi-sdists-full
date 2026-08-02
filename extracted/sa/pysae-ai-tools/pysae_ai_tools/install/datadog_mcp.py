"""Install the Datadog MCP server in ~/.claude.json."""

import os
from typing import Any

from .common.base import EnvVar, McpTool


class DatadogMcpTool(McpTool):
    name = "datadog-mcp"
    server_name = "datadog"
    cli_help = "Install/configure the Datadog MCP server"

    @property
    def env_vars(self) -> list[EnvVar]:
        return [
            EnvVar("DD_API_KEY", help="Datadog → Organization Settings → API Keys → New Key"),
            EnvVar("DD_APP_KEY", help="Datadog → Organization Settings → Application Keys → New Key"),
        ]

    def build_config(self) -> dict[str, Any]:
        api_key = os.environ.get("DD_API_KEY", "").strip()
        app_key = os.environ.get("DD_APP_KEY", "").strip()
        if not api_key or not app_key:
            raise ValueError("DD_API_KEY and DD_APP_KEY must be set")
        return {
            "command": "uvx",
            "args": ["--from", "git+https://github.com/shelfio/datadog-mcp.git", "datadog-mcp"],
            "env": {
                "DD_API_KEY": api_key,
                "DD_APP_KEY": app_key,
                "DD_SITE": os.environ.get("DD_SITE", "datadoghq.eu"),
            },
        }


tool = DatadogMcpTool()
