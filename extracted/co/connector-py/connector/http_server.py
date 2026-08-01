import asyncio
import importlib
import json
import os
import tempfile
from collections.abc import Awaitable, Callable
from contextlib import nullcontext
from enum import Enum
from typing import Any

from connector_sdk_types.generated import AppInfoResponse

from connector.ca_certs import is_windows, set_python_to_use_system_ca_certificates
from connector.httpx_rewrite import proxy_settings
from connector.oai.integration import Integration
from connector.observability.logging import set_logger_config
from connector.observability.observer import Observations, Observer
from connector.utils import proxy_utils

FLOWS_V2_EXECUTION_ID_OBSERVABILITY_HEADER = "X-Lumos-Observability-flows_v2_execution_id"
DAGSTER_RUN_ID_OBSERVABILITY_HEADER = "X-Lumos-Observability-dagster.run_id"

Scope = dict[str, Any]
Receive = Callable[[], Awaitable[dict[str, Any]]]
Send = Callable[[dict[str, Any]], Awaitable[None]]

_DOCS_HTML = """<!DOCTYPE html>
<html>
<head>
    <title>{title} - Swagger UI</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
        SwaggerUIBundle({{
            url: "/openapi.json",
            dom_id: "#swagger-ui",
            presets: [SwaggerUIBundle.presets.apis, SwaggerUIBundle.SwaggerUIStandalonePresets],
            layout: "BaseLayout",
        }});
    </script>
</body>
</html>"""


def build_observations(headers: dict[str, str]) -> Observations:
    """Extract observability context from request headers (lowercase keys)."""
    observations: Observations = {
        "flows_v2_execution_id": headers.get(
            FLOWS_V2_EXECUTION_ID_OBSERVABILITY_HEADER.lower(),
            "",
        )
    }
    if run_id := headers.get(DAGSTER_RUN_ID_OBSERVABILITY_HEADER.lower(), ""):
        observations["dagster"] = {"run_id": run_id}
    return observations


async def dispatch_capability(
    integration: Integration,
    capability: str,
    request_body: str,
    headers: dict[str, str],
    use_proxy: bool,
) -> str:
    """Dispatch a capability request with proxy and observability context applied."""
    integration.handle_errors = True

    proxy_cm = (
        proxy_settings(
            proxy_url=proxy_utils.get_proxy_url(),
            proxy_headers={
                "X-Lumos-Proxy-Auth": (await proxy_utils.get_proxy_token_async()).token,
            },
        )
        if use_proxy
        else nullcontext()
    )

    with proxy_cm, Observer.observe(build_observations(headers)):
        return await integration.dispatch(capability, request_body)


async def _read_body(receive: Receive) -> bytes:
    body = b""
    while True:
        message = await receive()
        body += message.get("body", b"")
        if not message.get("more_body", False):
            return body


async def _send_response(send: Send, status: int, content_type: bytes, body: str) -> None:
    await send(
        {
            "type": "http.response.start",
            "status": status,
            "headers": [(b"content-type", content_type)],
        }
    )
    await send({"type": "http.response.body", "body": body.encode()})


async def _send_json(send: Send, status: int, body: str) -> None:
    await _send_response(send, status, b"application/json", body)


def create_asgi_app(
    integration: Integration,
    use_proxy: bool = False,
    schema: dict[str, Any] | None = None,
) -> Callable[[Scope, Receive, Send], Awaitable[None]]:
    """Create the ASGI app serving [POST] /{capability_name} for each capability.

    The app also serves the integration's OAS schema at [GET] /openapi.json and
    a Swagger UI for it at [GET] /docs.
    """
    routes = {
        f"/{capability_name}".replace("-", "_"): capability_name
        for capability_name in integration.capabilities
    }
    openapi_schema = schema or {}

    async def app(scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "lifespan":
            while True:
                message = await receive()
                if message["type"] == "lifespan.startup":
                    await send({"type": "lifespan.startup.complete"})
                elif message["type"] == "lifespan.shutdown":
                    await send({"type": "lifespan.shutdown.complete"})
                    return
        if scope["type"] != "http":
            return

        path = scope["path"]
        method = scope["method"]

        if path == "/openapi.json" and method == "GET":
            await _send_json(send, 200, json.dumps(openapi_schema))
            return
        if path == "/docs" and method == "GET":
            await _send_response(
                send, 200, b"text/html", _DOCS_HTML.format(title=integration.app_id)
            )
            return

        capability = routes.get(path)
        if capability is None:
            await _send_json(send, 404, '{"detail": "Not Found"}')
            return
        if method != "POST":
            await _send_json(send, 405, '{"detail": "Method Not Allowed"}')
            return

        try:
            body = await _read_body(receive)
            headers = {
                key.decode("latin-1").lower(): value.decode("latin-1")
                for key, value in scope.get("headers", [])
            }
            response = await dispatch_capability(
                integration,
                capability,
                body.decode(),
                headers,
                use_proxy=use_proxy,
            )
        except Exception as e:
            await _send_json(send, 500, json.dumps({"detail": str(e)}))
            return
        await _send_json(send, 200, response)

    return app


def collect_integration_routes(
    integration: Integration,
    prefix_app_id: bool = False,
    use_proxy: bool = False,
    tags: list[str | Enum] | None = None,
):
    """Create a FastAPI ``APIRouter`` with an endpoint for each capability.

    Compatibility shim for host applications that mount connector capabilities
    into their own FastAPI app. Requires fastapi to be installed by the caller;
    the SDK itself no longer depends on it. ``tags`` is applied to every route
    for OpenAPI grouping in the host app. New code should use
    ``create_asgi_app`` instead.
    """
    from fastapi import APIRouter, Request

    def create_req_handler(capability: str):
        async def req_handler(request: Request):
            body = await request.body()
            response = await dispatch_capability(
                integration,
                capability,
                body.decode(),
                dict(request.headers),
                use_proxy=use_proxy,
            )
            return json.loads(response)

        return req_handler

    router = APIRouter()
    for capability_name in integration.capabilities:
        prefix = f"/{integration.app_id}" if prefix_app_id else ""
        # replace `-` in prefix (e.g. app_id) and capability name
        route = f"{prefix}/{capability_name}".replace("-", "_")
        router.add_api_route(
            route, create_req_handler(capability_name), methods=["POST"], tags=tags
        )

    return router


def create_app() -> Callable[[Scope, Receive, Send], Awaitable[None]]:
    """Create the ASGI app for the integration, if a factory is needed (hot reload)."""
    integration_id = os.environ.get("HTTP_SERVER_INTEGRATION_ID")
    if not integration_id:
        raise ValueError("HTTP_SERVER_INTEGRATION_ID environment variable is not set!")

    integration = load_integration(integration_id)
    set_logger_config(integration.app_id)
    if is_windows():
        set_python_to_use_system_ca_certificates()

    try:
        temp_dir = tempfile.gettempdir()
        schema_path = os.path.join(temp_dir, f"{integration.app_id}.json")
        with open(schema_path) as f:
            openapi_schema = json.load(f)
    except OSError:
        print(f"Error retrieving OAS schema for {integration.app_id}")
        openapi_schema = {}

    return create_asgi_app(
        integration,
        use_proxy=os.environ.get("HTTP_SERVER_USE_PROXY", "False") == "True",
        schema=openapi_schema,
    )


def load_integration(integration_id: str):
    """Import the integration module and return the integration object, uvicorn needs a import when running with reload True."""
    integration_module_name = integration_id.replace("-", "_")
    try:
        module = importlib.import_module(f"{integration_module_name}.integration")
        return module.integration
    except ModuleNotFoundError as e:
        raise ValueError(f"Integration {integration_module_name} not found") from e


def create_oas_schema(integration: Integration) -> dict[str, Any]:
    """Collect the OAS schema for the integration."""
    try:
        app_info = asyncio.run(integration.dispatch("app_info", json.dumps({"request": {}})))
        response = AppInfoResponse.model_validate_json(app_info)
        schema = response.response.app_schema
    except Exception as e:
        print(f"Error collecting OAS schema for {integration.app_id}:")
        print(e)
        schema = {}

    if schema:
        try:
            temp_dir = tempfile.gettempdir()
            schema_path = os.path.join(temp_dir, f"{integration.app_id}.json")
            with open(schema_path, "w") as f:
                json.dump(schema, f)
        except OSError:
            print(f"Error retrieving OAS schema for {integration.app_id}")

    return schema


def runserver(port: int, integration: Integration, reload: bool = False, use_proxy: bool = False):
    try:
        import uvicorn
    except ImportError as e:
        raise SystemExit(
            "The dev http-server requires uvicorn, which is not installed.\n"
            "In the integration-connectors workspace, run `uv sync` to install the\n"
            "dev dependency group; elsewhere, `pip install uvicorn`."
        ) from e

    # Generate OAS for integration (also cached to a temp file for the reload factory)
    schema = create_oas_schema(integration)

    app: Any
    if reload:
        os.environ["HTTP_SERVER_INTEGRATION_ID"] = integration.app_id
        os.environ["HTTP_SERVER_USE_PROXY"] = str(use_proxy)
        app = "connector.http_server:create_app"
    else:
        app = create_asgi_app(integration, use_proxy=use_proxy, schema=schema)

    try:
        uvicorn.run(
            app=app,
            factory=reload,
            port=port,
            reload=reload,
            reload_dirs=[
                "projects/libs/python/connector-sdk",
                f"projects/connectors/python/{integration.app_id}",
            ]
            if reload
            else None,
        )
    except KeyboardInterrupt:
        pass
