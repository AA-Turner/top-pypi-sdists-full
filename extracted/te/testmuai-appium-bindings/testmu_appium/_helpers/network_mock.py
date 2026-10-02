"""Network mock-set CRUD — replay of authored mock steps.

Talks to the per-session mock API on the device host:
http://{HOST_IP}:{PROXY_API_PORT+200}/v1/mocksets (offset = MDM's
MOCK_API_PORT_INCR; V2 parity: auteur-utils appium_uiActions
.execute_network_mock). The recorded engine uid doubles as the mockset name
(V2 contract). Driverless in substance — the driver arg keeps the uniform
DRIVER-verb call shape and is unused."""

import logging
from urllib.parse import quote

from testmu_appium._errors import NetworkMockUnavailable
from testmu_appium._helpers._http import request_with_retry
from testmu_appium._helpers._rd import proxy_host_port
from testmu_appium._vars import var

_log = logging.getLogger("testmu_appium")

_ACTIONS = frozenset(
    {"create", "activate", "deactivate", "update", "delete", "deactivate_all"}
)
_UID_OPTIONAL = frozenset({"create", "deactivate_all"})


def _mock_api_url() -> str:
    host, port = proxy_host_port()
    if not port or port == "0":
        raise NetworkMockUnavailable(
            "PROXY_API_PORT not available — cannot reach the mock API. Ensure "
            "the device session was started with mitmProxy enabled."
        )
    return f"http://{host or '127.0.0.1'}:{int(port) + 200}"


def network_mock(driver, *, action: str, uid: str = "", urls: list = None,
                 configurations: list = None, description: str = "") -> None:
    suffix = f" — {description}" if description else ""
    if action not in _ACTIONS:
        raise ValueError(
            f"network_mock action {action!r} not supported — expected one of "
            f"{sorted(_ACTIONS)}"
        )
    resolved_uid = str(var(uid))
    if not resolved_uid and action not in _UID_OPTIONAL:
        raise ValueError(f"network_mock action {action!r} requires 'uid'")
    encoded = quote(resolved_uid, safe="")
    base = _mock_api_url()

    if action == "create":
        payload = {"name": resolved_uid, "urls": urls or [],
                   "configurations": configurations or []}
        resp = request_with_retry("POST", f"{base}/v1/mocksets",
                                  json_data=payload, timeout=10)
    elif action == "update":
        payload = {"name": resolved_uid, "urls": urls or [],
                   "configurations": configurations or []}
        resp = request_with_retry("PUT", f"{base}/v1/mocksets/{encoded}",
                                  json_data=payload, timeout=10)
    elif action == "activate":
        resp = request_with_retry("PATCH", f"{base}/v1/mocksets/{encoded}/activate", timeout=10)
    elif action == "deactivate":
        resp = request_with_retry("PATCH", f"{base}/v1/mocksets/{encoded}/deactivate", timeout=10)
    elif action == "delete":
        resp = request_with_retry("DELETE", f"{base}/v1/mocksets/{encoded}", timeout=10)
    else:  # deactivate_all
        resp = request_with_retry("PATCH", f"{base}/v1/mocksets/-/deactivate-all", timeout=10)
    resp.raise_for_status()
    _log.info("network_mock: %s %s%s", action, resolved_uid, suffix)
