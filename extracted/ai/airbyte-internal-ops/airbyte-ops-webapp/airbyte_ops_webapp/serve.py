"""Production entrypoint for serving the Airbyte Ops Webapp container."""

from __future__ import annotations

import asyncio
import contextlib
import json
import os
import re
import signal
import sys

import uvicorn
from fastmcp.cli.apps_dev import (
    _EXT_APPS_VERSION,
    _HOST_HTML_TEMPLATE,
    _MCP_SDK_VERSION,
    _fetch_app_bridge_bundle,
    _inject_log_panel,
    _make_dev_app,
    _MessageLog,
    _read_mcp_resource,
    _start_user_server,
    _wait_for_server,
)
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, RedirectResponse, Response
from starlette.routing import Route

from airbyte_ops_webapp.auth.google_oauth import (
    GOOGLE_OAUTH_CALLBACK_PATH,
    GOOGLE_OAUTH_JS_ACTIONS,
    GOOGLE_OAUTH_SESSION_PATH,
    GOOGLE_OAUTH_TOKEN_PATH,
    google_oauth_callback_response,
    google_oauth_session_response,
    google_oauth_token_response,
)
from airbyte_ops_webapp.auth.oauth import (
    OAUTH_CALLBACK_PATH,
    OAUTH_JS_ACTIONS,
    OAUTH_SESSION_PATH,
    OAUTH_TOKEN_PATH,
    oauth_callback_response,
    oauth_session_response,
    oauth_token_response,
)
from airbyte_ops_webapp.pages.authorization.defaults import (
    OPS_AUTHORIZATION_PATH,
    OPS_AUTHORIZATION_TOOL_NAME,
)
from airbyte_ops_webapp.pages.connector_version_manager.defaults import (
    CONNECTOR_VERSION_MANAGER_PATH,
    CONNECTOR_VERSION_MANAGER_TOOL_NAME,
)
from airbyte_ops_webapp.pages.customer_billing.defaults import (
    CUSTOMER_BILLING_PATH,
    CUSTOMER_BILLING_TOOL_NAME,
)
from airbyte_ops_webapp.pages.home.page import OPS_HOME_TOOL_NAME
from airbyte_ops_webapp.pages.login.page import OPS_LOGIN_PATH
from airbyte_ops_webapp.pages.shared_components.layout import OPS_HOME_PATH
from airbyte_ops_webapp.theme import RENDERER_OVERRIDE_CSS

DEFAULT_SERVER_SPEC = "airbyte_ops_webapp/app.py:mcp"
DEFAULT_MCP_PORT = 8000
DEFAULT_WEBAPP_PORT = 8080
DEFAULT_STARTUP_TIMEOUT_SECONDS = 60.0
MCP_PORT_ENV_VAR = "AIRBYTE_OPS_WEBAPP_MCP_PORT"
SERVER_SPEC_ENV_VAR = "AIRBYTE_OPS_WEBAPP_SERVER_SPEC"
STARTUP_TIMEOUT_ENV_VAR = "AIRBYTE_OPS_WEBAPP_STARTUP_TIMEOUT_SECONDS"


def main() -> None:
    """Serve the webapp host and its local FastMCP backend."""
    asyncio.run(_serve())


async def _serve() -> None:
    server_spec = os.getenv(SERVER_SPEC_ENV_VAR, DEFAULT_SERVER_SPEC)
    mcp_port = int(os.getenv(MCP_PORT_ENV_VAR, str(DEFAULT_MCP_PORT)))
    webapp_port = int(os.getenv("PORT", str(DEFAULT_WEBAPP_PORT)))
    startup_timeout = float(
        os.getenv(
            STARTUP_TIMEOUT_ENV_VAR,
            str(DEFAULT_STARTUP_TIMEOUT_SECONDS),
        )
    )
    mcp_url = f"http://localhost:{mcp_port}/mcp"
    user_proc: asyncio.subprocess.Process | None = None

    try:
        user_proc = await _start_user_server(server_spec, mcp_port, reload=False)
        app_bridge_js, import_map_json = await _fetch_app_bridge_bundle(
            _EXT_APPS_VERSION,
            _MCP_SDK_VERSION,
        )
        import_map_tag = (
            f'  <script type="importmap">\n  {import_map_json}\n  </script>'
        )
        ready = await _wait_for_server(mcp_url, timeout=startup_timeout)
        if not ready:
            raise RuntimeError(f"User server did not start on port {mcp_port}")

        app = _make_dev_app(mcp_url, app_bridge_js, import_map_tag, _MessageLog())
        remove_generic_app_routes(app)
        add_home_routes(app, import_map_tag)
        add_login_routes(app, import_map_tag)
        add_authorization_routes(app, import_map_tag)
        add_connector_version_manager_routes(app, import_map_tag)
        add_customer_billing_routes(app, import_map_tag)
        add_prefab_renderer_route(app, mcp_url)
        add_oauth_routes(app)
        print(
            f"Airbyte Ops Webapp available at {_local_display_url(webapp_port)}",
            flush=True,
        )
        config = uvicorn.Config(
            app,
            host="0.0.0.0",
            port=webapp_port,
            log_level=os.getenv("AIRBYTE_OPS_WEBAPP_UVICORN_LOG_LEVEL", "warning"),
            ws="websockets-sansio",
        )
        await uvicorn.Server(config).serve()
    finally:
        if user_proc is not None and user_proc.returncode is None:
            _terminate_process(user_proc)
            with contextlib.suppress(TimeoutError):
                await asyncio.wait_for(user_proc.wait(), timeout=5)


def add_oauth_routes(app: Starlette) -> None:
    add_oauth_callback_route(app)
    app.routes.append(Route(OAUTH_TOKEN_PATH, oauth_token_response, methods=["POST"]))
    app.routes.append(
        Route(
            OAUTH_SESSION_PATH,
            oauth_session_response,
            methods=["GET", "POST", "DELETE"],
        )
    )
    # Google OAuth routes
    app.routes.append(
        Route(
            GOOGLE_OAUTH_CALLBACK_PATH, google_oauth_callback_response, methods=["GET"]
        )
    )
    app.routes.append(
        Route(GOOGLE_OAUTH_TOKEN_PATH, google_oauth_token_response, methods=["POST"])
    )
    app.routes.append(
        Route(
            GOOGLE_OAUTH_SESSION_PATH,
            google_oauth_session_response,
            methods=["GET", "POST", "DELETE"],
        )
    )


def remove_generic_app_routes(app: Starlette) -> None:
    generic_route_paths = {"/", "/picker-app", "/launch", "/api/launch"}
    app.router.routes[:] = [
        route
        for route in app.routes
        if getattr(route, "path", "") not in generic_route_paths
    ]


APP_TITLE = "Airbyte Internal Ops"


def add_home_routes(app: Starlette, import_map_tag: str) -> None:
    async def home_redirect(_request) -> RedirectResponse:
        return RedirectResponse(OPS_HOME_PATH)

    async def home(_request) -> HTMLResponse:
        return HTMLResponse(
            _tool_host_html(
                tool_name=OPS_HOME_TOOL_NAME,
                tool_args={},
                import_map_tag=import_map_tag,
                page_title=APP_TITLE,
            )
        )

    app.routes.insert(0, Route("/", home_redirect))
    app.routes.insert(0, Route(OPS_HOME_PATH, home))


def add_login_routes(app: Starlette, import_map_tag: str) -> None:
    async def login(_request) -> RedirectResponse:
        return RedirectResponse(OPS_AUTHORIZATION_PATH, status_code=302)

    app.routes.insert(0, Route(OPS_LOGIN_PATH, login))


def add_authorization_routes(app: Starlette, import_map_tag: str) -> None:
    async def authorization(_request) -> HTMLResponse:
        return HTMLResponse(
            _tool_host_html(
                tool_name=OPS_AUTHORIZATION_TOOL_NAME,
                tool_args={},
                import_map_tag=import_map_tag,
                page_title=f"{APP_TITLE} — Authorization",
            )
        )

    app.routes.insert(0, Route(OPS_AUTHORIZATION_PATH, authorization))


def add_connector_version_manager_routes(app: Starlette, import_map_tag: str) -> None:
    async def connector_version_manager(request) -> HTMLResponse:
        tool_args = {
            key: value for key, value in request.query_params.items() if value.strip()
        }
        return HTMLResponse(
            _tool_host_html(
                tool_name=CONNECTOR_VERSION_MANAGER_TOOL_NAME,
                tool_args=tool_args,
                import_map_tag=import_map_tag,
                page_title="Airbyte Ops — Connector Versions",
            )
        )

    app.routes.insert(
        0, Route(CONNECTOR_VERSION_MANAGER_PATH, connector_version_manager)
    )


def add_customer_billing_routes(app: Starlette, import_map_tag: str) -> None:
    async def customer_billing(request) -> HTMLResponse:
        tool_args = {
            key: value for key, value in request.query_params.items() if value.strip()
        }
        return HTMLResponse(
            _tool_host_html(
                tool_name=CUSTOMER_BILLING_TOOL_NAME,
                tool_args=tool_args,
                import_map_tag=import_map_tag,
                page_title="Airbyte Ops \u2014 Customer Billing",
            )
        )

    app.routes.insert(0, Route(CUSTOMER_BILLING_PATH, customer_billing))


_TITLE_RE = re.compile(r"<title>[^<]*</title>")


def _tool_host_html(
    *,
    tool_name: str,
    tool_args: dict[str, str],
    import_map_tag: str,
    page_title: str | None = None,
) -> str:
    host_html = _HOST_HTML_TEMPLATE.format(
        tool_name=tool_name,
        import_map_tag=import_map_tag,
        tool_name_json=json.dumps(tool_name),
        tool_args_json=json.dumps(tool_args),
        mcp_sdk_version=_MCP_SDK_VERSION,
    )
    if page_title:
        host_html = _TITLE_RE.sub(f"<title>{page_title}</title>", host_html, count=1)
    return _inject_log_panel(host_html)


def _local_display_url(webapp_port: int) -> str:
    return f"http://localhost:{webapp_port}"


def add_prefab_renderer_route(app: Starlette, mcp_url: str) -> None:
    async def ui_resource(request) -> Response:
        uri = request.query_params.get("uri", "")
        if not uri:
            return Response("Missing uri parameter", status_code=400)
        html = await _read_mcp_resource(mcp_url, uri)
        if html is None:
            return Response(f"Could not read MCP resource: {uri}", status_code=502)
        if uri.startswith("ui://prefab/") and uri.endswith("/renderer.html"):
            html = _inject_oauth_handlers(html)
            html = _inject_renderer_overrides(html)
        return HTMLResponse(html)

    app.routes.insert(0, Route("/ui-resource", ui_resource))


def add_oauth_callback_route(app: Starlette) -> None:
    app.routes.append(
        Route(OAUTH_CALLBACK_PATH, oauth_callback_response, methods=["GET"])
    )


def _inject_oauth_handlers(html: str) -> str:
    handlers_script = _oauth_handlers_script()
    if "</head>" in html:
        return html.replace("</head>", f"{handlers_script}\n</head>", 1)
    return f"{handlers_script}\n{html}"


def _inject_renderer_overrides(html: str) -> str:
    """Inject CSS overrides into the renderer iframe."""
    if not RENDERER_OVERRIDE_CSS:
        return html
    style_tag = f"<style>{RENDERER_OVERRIDE_CSS}</style>"
    if "</head>" in html:
        return html.replace("</head>", f"{style_tag}\n</head>", 1)
    return f"{style_tag}\n{html}"


def _oauth_handlers_script() -> str:
    all_actions = {**OAUTH_JS_ACTIONS, **GOOGLE_OAUTH_JS_ACTIONS}
    action_entries = ",\n    ".join(
        f"{name}: {body}" for name, body in all_actions.items()
    )
    return f"""<script>
window.__prefab_handlers = {{
  actions: {{
    {action_entries}
  }}
}};
</script>"""


def _terminate_process(process: asyncio.subprocess.Process) -> None:
    if sys.platform == "win32":
        process.terminate()
        return

    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        process.terminate()


if __name__ == "__main__":
    main()
