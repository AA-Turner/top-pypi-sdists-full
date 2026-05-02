import httpx
from typing import Optional

async def fetch_swagger_endpoints(base_url: str) -> Optional[list[dict]]:
    """
    Try to fetch endpoint list from a running Spring Boot app.
    Tries Swagger v3 first, then Spring Actuator mappings.
    Returns None if the app isn't running or doesn't expose these.
    """
    urls_to_try = [
        f"{base_url.rstrip('/')}/v3/api-docs",
        f"{base_url.rstrip('/')}/v2/api-docs",
        f"{base_url.rstrip('/')}/actuator/mappings",
    ]

    async with httpx.AsyncClient(timeout=3.0) as client:
        for url in urls_to_try:
            try:
                resp = await client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    return _parse_response(url, data)
            except Exception:
                continue
    return None

def _parse_response(url: str, data: dict) -> list[dict]:
    results = []

    if "paths" in data:
        for path, methods in data["paths"].items():
            for method, details in methods.items():
                results.append({
                    "path": path,
                    "method": method.upper(),
                    "summary": details.get("summary", ""),
                    "tags": details.get("tags", []),
                    "source": "swagger",
                })
    elif "contexts" in data:
        for context in data["contexts"].values():
            mappings = context.get("mappings", {})
            for handler in mappings.get("dispatcherServlets", {}).get("dispatcherServlet", []):
                details = handler.get("details", {})
                request_info = details.get("requestMappingConditions", {})
                patterns = request_info.get("patterns", ["/unknown"])
                methods = request_info.get("methods", ["GET"])
                for path in patterns:
                    for method in methods:
                        results.append({
                            "path": path,
                            "method": method,
                            "summary": handler.get("handler", ""),
                            "source": "actuator",
                        })
    return results