from core.indexer import CodeIndex
from core.swagger_client import fetch_swagger_endpoints
async def list_endpoints(index: CodeIndex, spring_boot_url: str = "") -> str:
    """"
    List all endpoints found in the codebase.
    If spring_boot_url is provided and the app is running, enriches with live data.
    """
    results = []

    live_endpoints = None
    if spring_boot_url:
        live_endpoints = await fetch_swagger_endpoints(spring_boot_url)

    if live_endpoints:
        results.append("=== Live endpoints from running app ===")
        for ep in live_endpoints:
            summary = f" — {ep['summary']}" if ep.get('summary') else ""
            results.append(f"  [{ep['method']}] {ep['path']}{summary}")
        results.append("")


    results.append("=== Endpoints found in source code analysis ===")
    if not index.endpoints:
        results.append("No endpoints found.")
    else:
        by_controller: dict[str, list] = {}
        for ep in index.endpoints:
            by_controller.setdefault(ep.controller_class, []).append(ep)

        for controller, eps in by_controller.items():
            results.append(f"\n  {controller}:")
            for ep in eps:
                service_note = ""
                if ep.calls_service:
                    service_note = f" → calls: {', '.join(ep.calls_service)}"
                results.append(f"    [{ep.http_method}] {ep.path}  ({ep.method_name}){service_note}")

    return "\n".join(results)

    
