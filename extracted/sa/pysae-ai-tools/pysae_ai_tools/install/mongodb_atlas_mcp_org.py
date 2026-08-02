"""Install the MongoDB Atlas org MCP server (env-agnostic organisation keys)."""

from .common import atlas

SERVER_NAME = "mongodb-atlas-mcp-org"


class MongodbAtlasMcpOrgTool(atlas.AtlasMcpTool):
    name = "mongodb-atlas-mcp-org"
    cli_help = "Install/configure the MongoDB Atlas org MCP server"
    server_name = SERVER_NAME

    def resolve_keys(self) -> tuple[str, str]:
        return atlas.resolve_org_keys()


tool = MongodbAtlasMcpOrgTool()
