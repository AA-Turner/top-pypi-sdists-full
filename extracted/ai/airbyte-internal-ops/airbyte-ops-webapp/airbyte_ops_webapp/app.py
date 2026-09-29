"""FastMCP entrypoint for the Airbyte Ops Webapp."""

from airbyte_ops_mcp._sentry import init_sentry_tracking
from fastmcp import FastMCP

from airbyte_ops_webapp.auth.oauth import register_oauth_routes
from airbyte_ops_webapp.pages.authorization.page import register_authorization_app
from airbyte_ops_webapp.pages.connector_version_manager.page import (
    register_connector_version_manager_app,
)
from airbyte_ops_webapp.pages.customer_billing.page import (
    register_customer_billing_app,
)
from airbyte_ops_webapp.pages.home.page import register_home_app
from airbyte_ops_webapp.pages.login.page import register_login_app
from airbyte_ops_webapp.pages.motherduck_diagnostics.page import (
    register_motherduck_diagnostics_app,
)
from airbyte_ops_webapp.pages.platform_admin.data_worker_allocation.page import (
    register_data_worker_allocation_app,
)
from airbyte_ops_webapp.pages.platform_admin.page import register_platform_admin_app

# `serve.py` loads this module in a separate backend process, and that is the
# process that runs the Prod DB Replica queries. Initializing here is what makes
# webapp DB spans and swallowed-query errors visible at all; the host process
# initializes separately in `serve.main`. `"mcp"` mode roots each trace at the
# `mcp.server` tool-call transaction rather than the `/mcp` HTTP request.
init_sentry_tracking(mode="mcp")

mcp = FastMCP("Airbyte Ops Webapp")
register_oauth_routes(mcp)
register_home_app(mcp)
register_login_app(mcp)
register_authorization_app(mcp)
register_connector_version_manager_app(mcp)
register_customer_billing_app(mcp)
register_motherduck_diagnostics_app(mcp)
register_platform_admin_app(mcp)
register_data_worker_allocation_app(mcp)
