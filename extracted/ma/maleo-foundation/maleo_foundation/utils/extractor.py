from datetime import datetime, timezone
from fastapi import Request
from starlette.requests import HTTPConnection
from uuid import uuid4
from maleo_foundation.models.transfers.general.request import RequestContext

def extract_client_ip(conn: HTTPConnection) -> str:
    """Extract client IP with more robust handling of proxies"""
    #* Check for X-Forwarded-For header (common when behind proxy/load balancer)
    x_forwarded_for = conn.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        #* The client's IP is the first one in the list
        ips = [ip.strip() for ip in x_forwarded_for.split(",")]
        return ips[0]

    #* Check for X-Real-IP header (used by some proxies)
    x_real_ip = conn.headers.get("X-Real-IP")
    if x_real_ip:
        return x_real_ip

    #* Fall back to direct client connection
    return conn.client.host if conn.client else "unknown"

def extract_request_context(request: Request) -> RequestContext:
    headers = request.headers

    request_id = headers.get("x-request-id")
    if request_id is None:
        request_id = uuid4()

    ip_address = extract_client_ip(request)

    ua_browser = headers.get("sec-ch-ua", "")
    if ua_browser:
        ua_browser = ua_browser.replace('"', "").split(",")[0].strip()

    return RequestContext(
        request_id=request_id,
        requested_at=datetime.now(tz=timezone.utc),
        method=request.method,
        url=request.url.path,
        path_params=None if not request.path_params else request.path_params,
        query_params=None if not request.query_params else str(request.query_params),
        ip_address=ip_address,
        is_internal=None if ip_address=="unknown" else (ip_address.startswith("10.") or ip_address.startswith("192.168.") or ip_address.startswith("172.")),
        user_agent=headers.get("user-agent"),
        ua_browser=ua_browser,
        ua_mobile=headers.get("sec-ch-ua-mobile"),
        platform=headers.get("sec-ch-ua-platform"),
        referer=headers.get("referer"),
        origin=headers.get("origin"),
        host=headers.get("host"),
        forwarded_proto=headers.get("x-forwarded-proto"),
        language=headers.get("accept-language"),
    )
