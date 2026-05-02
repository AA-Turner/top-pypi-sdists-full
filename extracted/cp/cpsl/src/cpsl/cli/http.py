from __future__ import annotations

from .. import terminal
from ..config import get_config_context

PROD_GATEWAY_HOST = "gateway.capsule.new"
PROD_API_HOST = "api.capsule.new"
API_PREFIX = "/api/v1"
HTTPS_PORT = 443
HTTP_PORT = 80


def api_base(path: str) -> tuple[str, dict[str, str]]:
    ctx = get_config_context()
    if not ctx or not ctx.is_valid():
        terminal.error("Not logged in. Run 'capsule login' first.")
        raise SystemExit(1)

    port = ctx.gateway_http_port
    if port is None:
        port = ctx.gateway_port if ctx.gateway_port in (HTTPS_PORT, HTTP_PORT) else ctx.gateway_port + 1
    scheme = "https" if port == HTTPS_PORT else "http"
    host = ctx.gateway_host if port in (HTTPS_PORT, HTTP_PORT) else f"{ctx.gateway_host}:{port}"
    if ctx.gateway_host == PROD_GATEWAY_HOST and port == HTTPS_PORT:
        host = PROD_API_HOST

    normalized = "/" + path.strip("/")
    return f"{scheme}://{host}{API_PREFIX}{normalized}", {"Authorization": f"Bearer {ctx.token}"}
