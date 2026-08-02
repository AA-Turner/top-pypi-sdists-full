"""Install the MongoDB dev MCP server (read/write)."""

import os
from typing import Any

from .common.base import EnvVar, McpTool

SERVER_NAME = "mongodb-dev"


class MongoMcpDevTool(McpTool):
    name = "mongo-mcp-dev"
    server_name = SERVER_NAME
    cli_help = "Install/configure the MongoDB dev MCP server (read/write)"

    @property
    def env_vars(self) -> list[EnvVar]:
        return [
            EnvVar(
                "MONGO_URI_DEV",
                help="pysae-ai-tools secrets read --secret-id pysae/local-dev/secrets api-mongo-uri --show-value",
            )
        ]

    def build_config(self) -> dict[str, Any]:
        uri = os.environ.get("MONGO_URI_DEV", "").strip()
        if not uri:
            raise RuntimeError("MONGO_URI_DEV is required")
        return {
            "type": "stdio",
            "command": "npx",
            "args": ["-y", "mongodb-mcp-server@latest"],
            "env": {"MDB_MCP_CONNECTION_STRING": uri},
        }


tool = MongoMcpDevTool()
