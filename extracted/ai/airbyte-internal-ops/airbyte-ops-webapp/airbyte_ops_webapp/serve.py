"""Production entrypoint for serving the Airbyte Ops Webapp container."""

from __future__ import annotations

import asyncio
import contextlib
import os
import signal
import sys
import urllib.parse

import uvicorn
from fastmcp.cli.apps_dev import (
    _EXT_APPS_VERSION,
    _MCP_SDK_VERSION,
    _fetch_app_bridge_bundle,
    _make_dev_app,
    _MessageLog,
    _read_mcp_resource,
    _start_user_server,
    _wait_for_server,
)
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, RedirectResponse, Response
from starlette.routing import Route

from airbyte_ops_webapp.auth.oauth import (
    OAUTH_CALLBACK_PATH,
    OAUTH_JS_ACTIONS,
    OAUTH_TOKEN_PATH,
    oauth_callback_response,
    oauth_token_response,
)
from airbyte_ops_webapp.pages.home.page import OPS_HOME_TOOL_NAME

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
        add_home_redirect_route(app)
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


def add_home_redirect_route(app: Starlette) -> None:
    async def home_redirect(_request) -> RedirectResponse:
        return RedirectResponse(_home_launch_path())

    app.routes.insert(0, Route("/", home_redirect))


def _home_launch_path() -> str:
    args = urllib.parse.quote("{}", safe="")
    return f"/launch?tool={OPS_HOME_TOOL_NAME}&args={args}"


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


def _oauth_handlers_script() -> str:
    action_entries = ",\n    ".join(
        f"{name}: {body}" for name, body in OAUTH_JS_ACTIONS.items()
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
