"""Install the MongoDB Atlas prod MCP server."""

from .common import atlas

SERVER_NAME = "mongodb-atlas-mcp-prod"


class MongodbAtlasMcpProdTool(atlas.AtlasMcpTool):
    name = "mongodb-atlas-mcp-prod"
    cli_help = "Install/configure the MongoDB Atlas prod MCP server"
    server_name = SERVER_NAME
    secret_env = "prod"

    def resolve_keys(self) -> tuple[str, str]:
        return atlas.resolve_project_keys("prod")


tool = MongodbAtlasMcpProdTool()
