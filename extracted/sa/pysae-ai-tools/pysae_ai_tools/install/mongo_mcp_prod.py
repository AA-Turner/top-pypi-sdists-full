"""Install the MongoDB prod MCP server (read-only)."""

import os
from typing import Any

from .common.base import EnvVar, McpTool

SERVER_NAME = "mongodb-prod"


class MongoMcpProdTool(McpTool):
    name = "mongo-mcp-prod"
    server_name = SERVER_NAME
    cli_help = "Install/configure the MongoDB prod MCP server (read-only)"

    @property
    def env_vars(self) -> list[EnvVar]:
        return [
            EnvVar(
                "MONGO_URI_PROD",
                help="pysae-ai-tools secrets read --secret-id pysae/local-prod/secrets api-mongo-uri --show-value",
            )
        ]

    def build_config(self) -> dict[str, Any]:
        uri = os.environ.get("MONGO_URI_PROD", "").strip()
        if not uri:
            raise RuntimeError("MONGO_URI_PROD is required")
        return {
            "type": "stdio",
            "command": "npx",
            "args": ["-y", "mongodb-mcp-server@latest", "--readOnly"],
            "env": {"MDB_MCP_CONNECTION_STRING": uri},
        }


tool = MongoMcpProdTool()
