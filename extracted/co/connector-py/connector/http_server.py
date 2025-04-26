import asyncio
import importlib
import json
import os
import tempfile
from typing import Any

from fastapi import FastAPI, Request

from connector.generated.models.app_info_response import AppInfoResponse
from connector.httpx_rewrite import proxy_settings
from connector.logging import set_logger_config
from connector.oai.integration import Integration
from connector.utils import proxy_utils


def create_req_handler(
    capability: str,
    integration: Integration,
    use_proxy: bool = False,
):
    async def req_handler(request: Request):
        body = await request.body()
        req_str = body.decode()
        integration.handle_errors = True

        if use_proxy:
            with proxy_settings(
                proxy_url=proxy_utils.get_proxy_url(),
                proxy_headers={
                    "X-Lumos-Proxy-Auth": (await proxy_utils.get_proxy_token_async()).token,
                },
            ):
                response = await integration.dispatch(capability, req_str)
        else:
            response = await integration.dispatch(capability, req_str)

        return json.loads(response)

    return req_handler


def collect_integration_routes(
    integration: Integration,
    prefix_app_id: bool = False,
    use_proxy: bool = False,
):
    """Create API endpoint for each method in integration."""
    from fastapi import APIRouter

    router = APIRouter()
    for capability_name, _ in integration.capabilities.items():
        prefix = f"/{integration.app_id}" if prefix_app_id else ""
        # replace `-` in prefix (e.g. app_id) and capability name
        route = f"{prefix}/{capability_name}".replace("-", "_")
        handler = create_req_handler(capability_name, integration, use_proxy=use_proxy)
        router.add_api_route(route, handler, methods=["POST"])

    return router


def create_app() -> FastAPI:
    """Create a FastAPI app for the integration, if a factory is needed (hot reload)."""
    integration_id = os.environ.get("HTTP_SERVER_INTEGRATION_ID")
    if not integration_id:
        raise ValueError("HTTP_SERVER_INTEGRATION_ID environment variable is not set!")

    integration = load_integration(integration_id)
    set_logger_config(integration.app_id)
    app = FastAPI()

    def get_schema():
        try:
            temp_dir = tempfile.gettempdir()
            schema_path = os.path.join(temp_dir, f"{integration.app_id}.json")
            with open(schema_path) as f:
                openapi_schema = json.load(f)
            return openapi_schema
        except OSError:
            print(f"Error retrieving OAS schema for {integration.app_id}")
            return {}

    app.openapi = get_schema  # type: ignore
    router = collect_integration_routes(
        integration,
        use_proxy=os.environ.get("HTTP_SERVER_USE_PROXY", "False") == "True",
    )
    app.include_router(router)
    return app


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

        # Generate OAS for integration
        schema = create_oas_schema(integration)

        if reload:
            os.environ["HTTP_SERVER_INTEGRATION_ID"] = integration.app_id
            os.environ["HTTP_SERVER_USE_PROXY"] = str(use_proxy)
        else:
            app = FastAPI()
            app.openapi = lambda: schema  # type: ignore
            router = collect_integration_routes(integration, use_proxy=use_proxy)
            app.include_router(router)

        uvicorn.run(
            app=app if not reload else "connector.http_server:create_app",
            factory=True if reload else False,
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
