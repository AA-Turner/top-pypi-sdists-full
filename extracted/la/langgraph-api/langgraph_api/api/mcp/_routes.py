from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

from starlette.responses import Response

from langgraph_api.api.mcp._origins import OriginPolicy
from langgraph_api.api.mcp._server import serve
from langgraph_api.config import CORS_SETTINGS
from langgraph_api.route import ApiRequest, ApiResponse, ApiRoute

if TYPE_CHECKING:
    from starlette.types import ASGIApp

__all__ = ["mcp_routes"]

ORIGIN_POLICY = OriginPolicy.of(CORS_SETTINGS)


async def handle_mcp_endpoint(request: ApiRequest) -> ASGIApp:
    if not ORIGIN_POLICY.allows(request.headers.get("origin")):
        return ApiResponse(
            {"error": "Origin is not allowed"}, status_code=HTTPStatus.FORBIDDEN
        )
    if request.method != "POST":
        return Response(
            status_code=HTTPStatus.METHOD_NOT_ALLOWED, headers={"Allow": "POST"}
        )
    return serve


mcp_routes = [
    ApiRoute("/mcp", handle_mcp_endpoint, methods=["GET", "POST", "DELETE"]),
]
