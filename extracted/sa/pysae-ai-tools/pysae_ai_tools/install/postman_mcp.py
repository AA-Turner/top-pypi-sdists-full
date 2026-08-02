"""Install the Postman MCP server in ~/.claude.json."""

import os
from typing import Any

from .common.base import EnvVar, McpTool


class PostmanMcpTool(McpTool):
    name = "postman-mcp"
    server_name = "postman"
    cli_help = "Install/configure the Postman MCP server"

    @property
    def env_vars(self) -> list[EnvVar]:
        return [
            EnvVar("POSTMAN_API_KEY", help="Postman → Settings → API Keys → Generate API Key"),
        ]

    def build_config(self) -> dict[str, Any]:
        api_key = os.environ.get("POSTMAN_API_KEY", "").strip()
        if not api_key:
            raise ValueError("POSTMAN_API_KEY must be set")
        mode_arg = os.environ.get("POSTMAN_MCP_MODE", "--minimal")
        return {
            "command": "npx",
            "args": ["@postman/postman-mcp-server@latest", mode_arg],
            "env": {"POSTMAN_API_KEY": api_key},
        }


tool = PostmanMcpTool()
