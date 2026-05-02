"""Plugin to expose event handlers as HTTP API endpoints.

Adapted from reflex-dev/reflex branch masenf/http-endpoint-demo.
Requires reflex >= 0.9.0 for the underlying plugin APIs.
"""

from __future__ import annotations

import contextlib
import importlib.util
import inspect
import json
from functools import partial
from typing import TYPE_CHECKING, Any, get_args, get_origin

from reflex.plugins.base import Plugin as PluginBase
from reflex.utils import console

if TYPE_CHECKING:
    from reflex.app import App


try:
    _HAS_REGISTRY = importlib.util.find_spec("reflex_base.registry") is not None
except (ModuleNotFoundError, ValueError):
    _HAS_REGISTRY = False

try:
    from reflex.event import Event as _Event

    _HAS_EVENT_FROM_EVENT_TYPE = hasattr(_Event, "from_event_type")
    del _Event
except ImportError:
    _HAS_EVENT_FROM_EVENT_TYPE = False


_MISSING_REFLEX_09_MSG = (
    "EventHandlerAPIPlugin requires reflex >= 0.9.0. "
    "Please upgrade: uv add reflex>=0.9.0"
)


# Mapping from Python types to OpenAPI (JSON Schema) types.
_PYTHON_TYPE_TO_OPENAPI: dict[type, dict[str, str]] = {
    str: {"type": "string"},
    int: {"type": "integer"},
    float: {"type": "number"},
    bool: {"type": "boolean"},
    bytes: {"type": "string", "format": "byte"},
}


def _python_type_to_openapi_schema(annotation: Any) -> dict[str, Any]:
    """Convert a Python type annotation to an OpenAPI JSON Schema fragment.

    Args:
        annotation: The Python type annotation.

    Returns:
        An OpenAPI-compatible schema dict.
    """
    if annotation is inspect.Parameter.empty or annotation is Any:
        return {}

    # Direct type match.
    if annotation in _PYTHON_TYPE_TO_OPENAPI:
        return dict(_PYTHON_TYPE_TO_OPENAPI[annotation])

    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle list[X] annotations.
    if origin is list:
        schema: dict[str, Any] = {"type": "array"}
        if args:
            schema["items"] = _python_type_to_openapi_schema(args[0])
        return schema

    # Handle dict[K, V] annotations.
    if origin is dict:
        schema = {"type": "object"}
        if len(args) >= 2:
            schema["additionalProperties"] = _python_type_to_openapi_schema(args[1])
        return schema

    # Optional[X] / X | None  ->  unwrap to X
    if origin is type(int | str):  # types.UnionType (3.10+)
        non_none = [a for a in args if a is not type(None)]
        if len(non_none) == 1:
            return {**_python_type_to_openapi_schema(non_none[0]), "nullable": True}

    # typing.Union / typing.Optional
    try:
        import typing

        if origin is typing.Union:
            non_none = [a for a in args if a is not type(None)]
            if len(non_none) == 1:
                return {
                    **_python_type_to_openapi_schema(non_none[0]),
                    "nullable": True,
                }
    except Exception:
        pass

    # Fallback - no schema constraint.
    return {}


def _build_endpoint_docstring(
    registered_event_handler: Any,
    dynamic_route_args: dict[str, str] | None = None,
    state_class_name: str | None = None,
) -> str:
    """Build an OpenAPI YAML docstring for a Starlette endpoint from an event handler.

    Args:
        registered_event_handler: The registered event handler.
        dynamic_route_args: Dynamic route arguments collected from all pages.
        state_class_name: The state class name to use for ``operationId`` and
            ``tags``. When omitted, those fields are not emitted.

    Returns:
        A YAML string suitable for use as an endpoint function docstring.
    """
    handler = registered_event_handler.handler
    fn = handler.fn
    if isinstance(fn, partial):
        fn = fn.func

    # --- Summary / description from the original docstring ---
    raw_doc = inspect.getdoc(fn) or ""
    lines = raw_doc.strip().splitlines()
    summary = lines[0] if lines else handler.fn.__name__
    description_lines = [
        line
        for line in lines[1:]
        if not line.strip().startswith(("Args:", "Returns:", "Raises:"))
    ]
    # Trim leading blank lines and trailing whitespace-only section headers.
    while description_lines and not description_lines[0].strip():
        description_lines.pop(0)
    while description_lines and not description_lines[-1].strip():
        description_lines.pop()
    # Fall back to the summary so `description` is always a non-empty string —
    # required by most OpenAPI linters.
    description = "\n".join(description_lines).strip() if description_lines else summary

    # --- Request body schema from function parameters ---
    params = iter(handler.get_parameters().items())
    if handler.state is not None:
        next(params, None)  # skip the bound `self` parameter
    properties: dict[str, Any] = {}
    required: list[str] = []

    for name, param in params:
        prop = _python_type_to_openapi_schema(param.annotation)
        if not prop:
            prop = {}
        properties[name] = prop
        if param.default is inspect.Parameter.empty:
            required.append(name)
        else:
            # Include the default value in the schema.
            try:
                json.dumps(param.default)  # ensure it's JSON-serialisable
                prop["default"] = param.default
            except (TypeError, ValueError):
                pass

    # --- Assemble the OpenAPI operation object as a dict ---
    operation: dict[str, Any] = {}
    operation["summary"] = summary
    operation["description"] = description

    if state_class_name is not None:
        operation["operationId"] = f"{state_class_name}_{handler.fn.__name__}"
        operation["tags"] = [state_class_name]

    # Always emit a requestBody so linters don't flag the POST as missing both
    # a body and parameters — handlers with no args still get an empty schema.
    operation["requestBody"] = {
        "required": bool(required),
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": properties,
                    **({"required": required} if required else {}),
                }
            }
        },
    }

    operation["responses"] = {
        200: {"$ref": "#/components/responses/StreamedDelta"},
        401: {"$ref": "#/components/responses/Unauthorized"},
    }

    # Reference shared dynamic route query parameters.
    if dynamic_route_args:
        operation["parameters"] = [
            {"$ref": f"#/components/parameters/route_{name}"}
            for name in dynamic_route_args
        ]

    return json.dumps(operation)


# RFC 9727 / RFC 9264 constants for the /.well-known/api-catalog endpoint.
_OPENAPI_PATH = "/_reflex/events/openapi.yaml"
_API_CATALOG_PATH = "/.well-known/api-catalog"
_OPENAPI_MEDIA_TYPE = "application/vnd.oai.openapi"
_LINKSET_MEDIA_TYPE = (
    'application/linkset+json; profile="https://www.rfc-editor.org/info/rfc9727"'
)
_API_CATALOG_LINK_HEADER = (
    f'<{_OPENAPI_PATH}>; rel="service-desc"; type="{_OPENAPI_MEDIA_TYPE}", '
    f'<{_API_CATALOG_PATH}>; rel="api-catalog"'
)


def _add_api_catalog_route(app: App) -> None:
    """Add the ``/.well-known/api-catalog`` endpoint per RFC 9727.

    Returns a Linkset (RFC 9264) listing the OpenAPI spec as a
    ``service-desc`` link. Supports ``GET`` (linkset body) and ``HEAD``
    (``Link`` header only), both required by RFC 9727.

    Args:
        app: The app to add the route to.
    """
    from starlette.requests import Request
    from starlette.responses import JSONResponse, Response

    if not app._api:
        return

    async def api_catalog_endpoint(request: Request) -> Response:
        base_url = str(request.base_url).rstrip("/")
        openapi_url = f"{base_url}{_OPENAPI_PATH}"

        if request.method == "HEAD":
            return Response(
                status_code=200,
                headers={"Link": _API_CATALOG_LINK_HEADER},
            )

        linkset = {
            "linkset": [
                {
                    "anchor": base_url + "/",
                    "service-desc": [
                        {
                            "href": openapi_url,
                            "type": _OPENAPI_MEDIA_TYPE,
                        }
                    ],
                }
            ]
        }
        return JSONResponse(
            linkset,
            media_type=_LINKSET_MEDIA_TYPE,
            headers={"Link": _API_CATALOG_LINK_HEADER},
        )

    app._api.add_route(
        _API_CATALOG_PATH,
        api_catalog_endpoint,
        methods=["GET", "HEAD"],
        include_in_schema=False,
    )


def _add_retrieve_state_route(app: App) -> Any | None:
    """Add the ``/_reflex/retrieve_state`` endpoint.

    Returns the full root state ``.dict()`` for the Bearer token's session.
    Unlike ``hydrate``, this does NOT reset client storage vars — it simply
    reads and serialises the existing state.

    Args:
        app: The app to add the route to.

    Returns:
        The added route, or None if the route was not added.
    """
    from reflex.istate.manager.token import BaseStateToken
    from reflex.state import State, _resolve_delta
    from reflex.utils.format import json_dumps
    from starlette.requests import Request
    from starlette.responses import JSONResponse, Response

    if not app._api:
        return None

    docstring = json.dumps(
        {
            "summary": "Retrieve the full client state.",
            "description": (
                "Return the full root state `.dict()` for the session "
                "identified by the Bearer token. Unlike `hydrate`, this "
                "endpoint does not reset client storage vars."
            ),
            "operationId": "retrieve_state",
            "tags": ["system"],
            "requestBody": {
                "required": False,
                "content": {
                    "application/json": {
                        "schema": {"type": "object", "properties": {}},
                    }
                },
            },
            "responses": {
                200: {
                    "description": "The full state dict as JSON.",
                    "content": {
                        "application/json": {
                            "schema": {"type": "object"},
                        }
                    },
                },
                401: {"$ref": "#/components/responses/Unauthorized"},
            },
        }
    )

    async def retrieve_state_endpoint(request: Request) -> Response:
        token = request.headers.get("Authorization", "").removeprefix("Bearer ")
        if not token:
            return JSONResponse(
                {
                    "error": "Unauthorized: Provide a generated UUID as your Authorization: Bearer <token>."
                },
                status_code=401,
            )

        state_token = BaseStateToken(ident=token, cls=State)
        with app.set_contexts():
            state = await app.state_manager.get_state(state_token)
            state_dict = await _resolve_delta(state.dict())

        return Response(
            content=json_dumps(state_dict),
            media_type="application/json",
        )

    retrieve_state_endpoint.__doc__ = docstring

    app._api.add_route(
        path="/_reflex/retrieve_state",
        route=retrieve_state_endpoint,
        methods=["POST"],
    )
    return app._api.routes[-1]


def _add_event_handler_route(
    app: App,
    registered_event_handler: Any,
    dynamic_route_args: dict[str, str] | None = None,
) -> Any | None:
    """Add an API route for a registered event handler.

    Args:
        app: The app to add the route to.
        registered_event_handler: The registered event handler to add the route for.
        dynamic_route_args: Dynamic route arguments collected from all pages.

    Returns:
        The added route, or None if the route was not added.
    """
    from reflex.constants import RouteVar
    from reflex.event import Event
    from reflex.state import State
    from reflex.utils.format import get_event_handler_parts, json_dumps
    from starlette.requests import Request
    from starlette.responses import JSONResponse, Response, StreamingResponse

    if not app._api:
        return None

    handler_state = registered_event_handler.handler.state
    state_class_name = handler_state.__name__ if handler_state is not None else None
    docstring = _build_endpoint_docstring(
        registered_event_handler,
        dynamic_route_args,
        state_class_name=state_class_name,
    )

    async def event_handler_endpoint(request: Request) -> Response:
        token = request.headers.get("Authorization", "").removeprefix("Bearer ")
        if not token:
            return JSONResponse(
                {
                    "error": "Unauthorized: Provide a generated UUID as your Authorization: Bearer <token>."
                },
                status_code=401,
            )
        if request.headers.get("Content-Length", "0") != "0":
            rbody = await request.json()
        else:
            rbody = None

        # Build router_data from the incoming HTTP request.
        headers = dict(request.headers)
        client_ip = request.client.host if request.client else "0.0.0.0"
        headers["asgi-scope-client"] = client_ip
        client_ip = headers.get("x-forwarded-for", client_ip).partition(",")[0].strip()
        router_data = {
            RouteVar.CLIENT_TOKEN: token,
            RouteVar.HEADERS: headers,
            RouteVar.CLIENT_IP: client_ip,
            RouteVar.QUERY: dict(request.query_params),
            RouteVar.PATH: str(request.url.path),
        }

        async def _stream_response():
            try:
                async with contextlib.aclosing(
                    app.event_processor.enqueue_stream_delta(
                        token,
                        *Event.from_event_type(
                            registered_event_handler.handler(**(rbody or {})),
                            router_data=router_data,
                        ),
                    )
                ) as delta_stream:
                    async for delta in delta_stream:
                        yield json_dumps(delta) + "\n"
            except Exception as e:
                yield json.dumps(
                    {
                        "error": f"Error processing event: {e!s}. Check server logs for more details."
                    }
                )
                return

        return StreamingResponse(_stream_response(), media_type="application/x-ndjson")

    # Attach the generated OpenAPI YAML as the endpoint's docstring
    # so that Starlette's SchemaGenerator picks it up.
    event_handler_endpoint.__doc__ = docstring

    if registered_event_handler.handler.state:
        state_name, handler_name = get_event_handler_parts(
            registered_event_handler.handler
        )
        state_name = state_name.removeprefix(State.get_full_name() + ".")
        path = f"/_reflex/event/{state_name}/{handler_name}"
        app._api.add_route(
            path=path,
            route=event_handler_endpoint,
            methods=["POST"],
        )
        return app._api.routes[-1]
    return None


class EventHandlerAPIPlugin(PluginBase):
    """Plugin that exposes registered event handlers as HTTP API endpoints with OpenAPI schema.

    This is an enterprise plugin that requires:
    - reflex >= 0.9.0 for the underlying event handler registry APIs
    - reflex_enterprise.AppEnterprise as the app class (for license enforcement)

    Usage in rxconfig.py::

        import reflex_enterprise as rxe

        config = rxe.Config(
            app_name="my_app",
            plugins=[rxe.EventHandlerAPIPlugin()],
        )
    """

    def __init__(
        self,
        *,
        api_version: str = "1.0.0",
        contact: dict[str, str] | None = None,
        license_info: dict[str, str] | None = None,
    ) -> None:
        """Initialise the plugin.

        Args:
            api_version: Value for ``info.version`` in the generated OpenAPI
                spec. OpenAPI requires this field.
            contact: Optional ``info.contact`` object (e.g.
                ``{"name": "Ops", "email": "ops@example.com"}``).
            license_info: Optional ``info.license`` object (e.g.
                ``{"name": "Apache-2.0", "url": "https://..."}``).
        """
        self.api_version = api_version
        self.contact = contact
        self.license_info = license_info

    def _check_requirements(self, app: App) -> bool:
        """Check that the app meets the requirements for this plugin.

        Args:
            app: The app instance.

        Returns:
            True if requirements are met, False otherwise.

        Raises:
            RuntimeError: If the app is not an AppEnterprise instance.
        """
        from reflex_enterprise.app import AppEnterprise

        if not isinstance(app, AppEnterprise):
            raise RuntimeError(
                "EventHandlerAPIPlugin requires the app to be a "
                "reflex_enterprise.App (AppEnterprise) instance. "
                "Update your rxconfig.py to use:\n\n"
                "  import reflex_enterprise as rxe\n"
                "  config = rxe.Config(\n"
                "      app_name='my_app',\n"
                "      plugins=[rxe.EventHandlerAPIPlugin()],\n"
                "  )\n\n"
                "  app = rxe.App()\n"
            )

        if not _HAS_REGISTRY:
            console.error(_MISSING_REFLEX_09_MSG)
            return False

        if not _HAS_EVENT_FROM_EVENT_TYPE:
            console.error(_MISSING_REFLEX_09_MSG)
            return False

        return True

    def post_compile(self, **context) -> None:
        """Add event handler API routes after compilation.

        Args:
            context: The post-compile context containing the app.
        """
        from reflex.config import get_config
        from reflex.event import EventHandler, EventSpec
        from reflex.state import State
        from reflex.utils.format import get_event_handler_parts
        from starlette.requests import Request
        from starlette.responses import Response
        from starlette.schemas import OpenAPIResponse, SchemaGenerator

        app: App = context["app"]

        if not self._check_requirements(app):
            return

        if not app._api:
            return

        # Import guarded APIs (verified by _check_requirements).
        from reflex.state import (
            EventHandlerSetVar,
            FrontendEventExceptionState,
            OnLoadInternalState,
            UpdateVarsInternalState,
        )
        from reflex_base.registry import RegistrationContext

        config = get_config()

        # Collect dynamic route args from all registered pages.
        all_dynamic_args: dict[str, str] = {}

        try:
            from reflex.route import get_route_args
        except ImportError:
            get_route_args = None

        if get_route_args is not None:
            for route in app._unevaluated_pages:
                all_dynamic_args.update(get_route_args(route))

        # Build page route documentation with on_load references.
        base_url = (config.deploy_url or "").rstrip("/")
        page_lines: list[str] = []
        for route in app._unevaluated_pages:
            display_route = f"/{route}" if route else "/"
            full_url = f"{base_url}{display_route}" if base_url else display_route
            load_events = app._load_events.get(route, [])
            if not load_events:
                page_lines.append(f"- `{full_url}`")
                continue
            handler_names: list[str] = []
            for evt in load_events:
                handler = None
                if isinstance(evt, EventHandler):
                    handler = evt
                elif isinstance(evt, EventSpec):
                    handler = evt.handler
                if handler and handler.state:
                    s_name, h_name = get_event_handler_parts(handler)
                    s_name = s_name.removeprefix(State.get_full_name() + ".")
                    handler_names.append(f"`POST /_reflex/event/{s_name}/{h_name}`")
            if handler_names:
                page_lines.append(
                    f"- `{full_url}` -- on_load triggers " + ", ".join(handler_names)
                )
            else:
                page_lines.append(f"- `{full_url}`")

        description = (
            "Auto-generated API for Reflex event handlers.\n\n"
            "## Authentication\n\n"
            "All endpoints require a Bearer token passed via the "
            "`Authorization` header. The token should be a random UUID "
            "that identifies the client session.\n\n"
            "```\nAuthorization: Bearer <random-uuid>\n```\n\n"
            "Generate a token with any UUID library, e.g. "
            '`python -c "import uuid; print(uuid.uuid4())"`.'
        )

        if page_lines:
            description += (
                "\n\n## Pages\n\n"
                "The following pages are defined in the app. Pages with "
                "`on_load` handlers automatically trigger the referenced "
                "endpoint when a user navigates to them.\n\n" + "\n".join(page_lines)
            )

        if all_dynamic_args:
            description += (
                "\n\n## Dynamic Route Variables\n\n"
                "The app defines dynamic route segments in its page URLs. "
                "These are exposed as optional query parameters on every "
                "endpoint so the state can access them via `self.router`.\n\n"
                + "\n".join(
                    f"- `{name}` (from page URL pattern)" for name in all_dynamic_args
                )
            )

        # Build shared components for $ref reuse across endpoints.
        components: dict[str, Any] = {
            "securitySchemes": {
                "BearerToken": {
                    "type": "http",
                    "scheme": "bearer",
                    "description": "A random UUID that identifies the client session.",
                }
            },
            "responses": {
                "StreamedDelta": {
                    "description": "Streamed state deltas as newline-delimited JSON.",
                    "content": {
                        "application/x-ndjson": {
                            "schema": {"type": "object"},
                        }
                    },
                },
                "Unauthorized": {
                    "description": "Missing or invalid Bearer token.",
                },
            },
        }

        if all_dynamic_args:
            from reflex.constants.route import RouteArgType

            components["parameters"] = {}
            for arg_name, arg_type in all_dynamic_args.items():
                param_schema: dict[str, Any] = (
                    {"type": "array", "items": {"type": "string"}}
                    if arg_type == RouteArgType.LIST
                    else {"type": "string"}
                )
                components["parameters"][f"route_{arg_name}"] = {
                    "name": arg_name,
                    "in": "query",
                    "required": False,
                    "schema": param_schema,
                    "description": "Dynamic route variable from a page URL.",
                }

        info: dict[str, Any] = {
            "title": f"{config.app_name} API",
            "description": description,
            "version": self.api_version,
        }
        if self.contact:
            info["contact"] = self.contact
        if self.license_info:
            info["license"] = self.license_info

        base_schema: dict[str, Any] = {
            "openapi": "3.0.0",
            "info": info,
            "components": components,
            "security": [{"BearerToken": []}],
        }

        if config.api_url:
            try:
                from reflex.environment import environment

                if environment.REFLEX_MOUNT_FRONTEND_COMPILED_APP.get():
                    server_url = config.deploy_url
                else:
                    server_url = config.api_url
            except (ImportError, AttributeError):
                server_url = config.api_url
            if server_url:
                base_schema["servers"] = [{"url": server_url}]

        schemas = SchemaGenerator(base_schema)

        # Register the retrieve_state endpoint first so it appears at the top
        # of the openapi.yaml spec, before any event handler routes.
        routes: list[Any] = []
        retrieve_state_route = _add_retrieve_state_route(app)
        if retrieve_state_route is not None:
            routes.append(retrieve_state_route)

        state_class_names: set[str] = set()
        for reh in RegistrationContext.get().event_handlers.values():
            if reh.handler.state in (
                FrontendEventExceptionState,
                OnLoadInternalState,
                UpdateVarsInternalState,
            ):
                continue
            if isinstance(reh.handler, EventHandlerSetVar):
                continue
            route = _add_event_handler_route(app, reh, all_dynamic_args or None)
            if route is None:
                continue
            routes.append(route)
            if reh.handler.state is not None:
                state_class_names.add(reh.handler.state.__name__)

        # Top-level `tags` — the "system" tag is used by the retrieve_state
        # endpoint; per-state tags group the event handler endpoints.
        # Sorted alphabetically (case-insensitive) — OpenAPI linters expect it.
        tags: list[dict[str, str]] = sorted(
            [
                {
                    "name": "system",
                    "description": "Framework-level endpoints (state retrieval, etc.).",
                },
                *(
                    {
                        "name": name,
                        "description": f"Event handlers on `{name}`.",
                    }
                    for name in state_class_names
                ),
            ],
            key=lambda t: t["name"].lower(),
        )
        base_schema["tags"] = tags

        def openapi_response(request: Request) -> Response:
            schema = schemas.get_schema(routes=routes)
            response = OpenAPIResponse(schema)
            # RFC 9727 §5: link from the API description back to the catalog
            # so clients discovering the spec can find the catalog too.
            response.headers["Link"] = f'<{_API_CATALOG_PATH}>; rel="api-catalog"'
            return response

        app._api.add_route(
            _OPENAPI_PATH,
            openapi_response,
            methods=["GET"],
            include_in_schema=False,
        )

        _add_api_catalog_route(app)
