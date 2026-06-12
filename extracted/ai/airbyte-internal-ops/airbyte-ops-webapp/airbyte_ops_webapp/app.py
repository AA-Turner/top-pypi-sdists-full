"""FastMCP entrypoint for the Airbyte Ops Webapp."""

from fastmcp import FastMCP

from airbyte_ops_webapp.auth.oauth import register_oauth_routes
from airbyte_ops_webapp.pages.connector_version_manager.page import (
    register_connector_version_manager_app,
)
from airbyte_ops_webapp.pages.home.page import register_home_app

mcp = FastMCP("Airbyte Ops Webapp")
register_oauth_routes(mcp)
register_home_app(mcp)
register_connector_version_manager_app(mcp)
