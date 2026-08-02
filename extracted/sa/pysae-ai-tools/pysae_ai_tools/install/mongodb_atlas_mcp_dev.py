"""Install the MongoDB Atlas dev MCP server."""

from .common import atlas

SERVER_NAME = "mongodb-atlas-mcp-dev"


class MongodbAtlasMcpDevTool(atlas.AtlasMcpTool):
    name = "mongodb-atlas-mcp-dev"
    cli_help = "Install/configure the MongoDB Atlas dev MCP server"
    server_name = SERVER_NAME
    secret_env = "dev"

    def resolve_keys(self) -> tuple[str, str]:
        return atlas.resolve_project_keys("dev")


tool = MongodbAtlasMcpDevTool()
