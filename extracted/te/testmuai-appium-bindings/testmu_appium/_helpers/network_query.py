"""Versioned network-capture query and assertion contracts.

``network_query`` is deliberately a small sync adapter, rather than a second
HAR implementation in generated tests.  A stable local provider speaks
``network.capture.v1`` at ``GET {base}/v1/network/capture/flows`` and
``GET {base}/v1/network/capture/flows/{id}``.  LambdaTest device hosts expose
their legacy ``/har`` representation; that provider is adapted here and never
escapes as raw HAR.
"""
from __future__ import annotations

import base64
import json
import logging
import math
import os
import re
import time
from typing import Any
from urllib.parse import quote, urlsplit

from testmu_appium._errors import NetworkQueryUnavailable
from testmu_appium._helpers._http import request_with_retry
from testmu_appium._helpers._rd import proxy_host_port
from testmu_appium._vars import _variable_store, set_var

_log = logging.getLogger("testmu_appium")

CAPTURE_SCHEMA_VERSION = "network.capture.v1"
ASSERTION_SCHEMA_VERSION = "network.assert.v1"
_JSON_PREFIXES = (")]}',\n", ")]}'\n", "while(1);", "for(;;);")
_TRUTHY = {"1", "true", "yes", "on"}
_METHOD_RE = re.compile(r"^[A-Z][A-Z0-9_-]*$")
_MAX_OCCURRENCE = 10000
_MAX_TIMEOUT_MS = 120000


class NetworkCaptureError(Exception):
    """Base class for invalid or inaccessible network-capture providers."""


class NetworkCaptureUnavailable(NetworkCaptureError, NetworkQueryUnavailable):
    """Raised when no capture provider has been configured for this run."""


class NetworkCaptureTimeout(NetworkCaptureError):
    """Raised when a matching flow did not arrive before the polling budget."""


class NetworkCaptureNotFound(NetworkCaptureError):
    """Raised when a requested flow id is not present in the capture provider."""


class NetworkCaptureContractError(NetworkCaptureError):
    """Raised when a provider response cannot satisfy the pinned contract."""


class NetworkAssertionError(AssertionError):
    """AssertionError-compatible failure carrying the deterministic verdict."""

    def __init__(self, message: str, result: dict):
        super().__init__(message)
        self.result = result


def _clean_base(url: str) -> str:
    return url.rstrip("/")


def _provider() -> tuple[str, str]:
    """Return (kind, base), preferring an explicit environment-only endpoint."""
    explicit = os.getenv("TESTMU_NETWORK_CAPTURE_URL", "").strip()
    explicit_kind = os.getenv("TESTMU_NETWORK_CAPTURE_PROVIDER", "contract").strip().lower()
    if explicit:
        if explicit_kind not in {"contract", "lambda-har"}:
            raise NetworkCaptureContractError(
                "TESTMU_NETWORK_CAPTURE_PROVIDER must be 'contract' or 'lambda-har'"
            )
        return explicit_kind, _clean_base(explicit)

    host, port = proxy_host_port()
    if not host or not port:
        raise NetworkCaptureUnavailable(
            "network capture requires TESTMU_NETWORK_CAPTURE_URL or HOST_IP and "
            "PROXY_API_PORT from the environment or tempfile rd-details.env"
        )
    scheme = os.getenv("TESTMU_NETWORK_CAPTURE_SCHEME", "http").strip() or "http"
    return "lambda-har", f"{scheme}://{host}:{port}"


def _request_json(url: str, *, timeout: int) -> tuple[int, Any]:
    """Use the shared retry helper once per provider fetch, with safe logging."""
    try:
        response = request_with_retry("GET", url, timeout=timeout, silent=True)
    except Exception as exc:
        raise NetworkCaptureUnavailable("network capture provider could not be reached") from exc
    try:
        return response.status_code, response.json()
    except ValueError as exc:
        # A failing status often carries a non-JSON body (an empty 404, an HTML
        # error page). The status is the truthful signal there — hand it to the
        # caller to translate (404 -> NotFound) instead of masking it as a
        # contract violation. Only a 2xx with an unparseable body is one.
        if response.status_code < 200 or response.status_code >= 300:
            return response.status_code, None
        raise NetworkCaptureContractError("network capture provider returned invalid JSON") from exc


def _body(
    content: Any,
    *,
    fallback_mime_type: str = "",
    fallback_size: Any = None,
    fallback_content_encoding: str = "",
) -> dict:
    """Turn a HAR/request body into the fixed, non-HAR body envelope."""
    content = content if isinstance(content, dict) else {}
    encoded = content.get("text", content.get("data"))
    if encoded is None and "json" in content:
        encoded = content["json"]
    source_encoding = str(content.get("encoding") or "")
    content_encoding = str(
        content.get("content_encoding") or fallback_content_encoding or ""
    )
    mime_type = str(content.get("mimeType") or content.get("mime_type") or fallback_mime_type or "")
    explicitly_available = content.get("available")
    if encoded is None and fallback_size == 0 and explicitly_available is not False:
        encoded = ""
    available = encoded is not None and explicitly_available is not False
    data: str | None = None
    parsed_json = None
    encoding = source_encoding or "utf-8"
    truncation_reason = content.get("truncation_reason")
    if content.get("_truncated") and not truncation_reason:
        truncation_reason = "provider_truncated"

    if available:
        if isinstance(encoded, (dict, list)):
            parsed_json = encoded
            data = json.dumps(encoded, separators=(",", ":"), ensure_ascii=False)
            encoding = "utf-8"
        elif isinstance(encoded, bytes):
            try:
                data = encoded.decode("utf-8")
                encoding = "utf-8"
            except UnicodeDecodeError:
                data = base64.b64encode(encoded).decode("ascii")
                encoding = "base64"
        else:
            data = str(encoded)
            if source_encoding.lower() == "base64":
                try:
                    decoded = base64.b64decode(data, validate=True)
                    data = decoded.decode("utf-8")
                    encoding = "utf-8"
                except (ValueError, UnicodeDecodeError):
                    # Preserve opaque bytes as base64 rather than fabricating text.
                    encoding = "base64"
            if encoding != "base64":
                candidate = data.lstrip()
                for prefix in _JSON_PREFIXES:
                    if candidate.startswith(prefix):
                        candidate = candidate[len(prefix):].lstrip()
                        break
                if "json" in mime_type.lower() or candidate[:1] in {"{", "["}:
                    try:
                        parsed_json = json.loads(candidate)
                    except (TypeError, ValueError):
                        pass

    size = content.get("size", fallback_size)
    captured_size = content.get("captured_size", content.get("bodySize", fallback_size))
    if captured_size is None and data is not None:
        captured_size = len(data.encode("utf-8"))
    availability = str(content.get("availability") or "")
    if availability not in {"complete", "partial", "omitted", "unavailable"}:
        availability = "partial" if truncation_reason else "complete" if available else (
            "unavailable" if explicitly_available is False else "omitted"
        )
    return {
        "availability": availability,
        # Compatibility alias: partial bytes can still be evaluated, while an
        # omitted/unavailable body must produce an indeterminate assertion.
        "available": availability in {"complete", "partial"},
        "encoding": encoding,
        "mime_type": mime_type,
        "content_encoding": content_encoding,
        "size": size if isinstance(size, int) else None,
        "captured_size": captured_size if isinstance(captured_size, int) else None,
        "data": data,
        "json": parsed_json,
        "truncation_reason": str(truncation_reason) if truncation_reason else None,
    }


def _pairs(value: Any) -> list[dict[str, str]]:
    """Preserve provider/HAR order while exposing only name/value pairs."""
    if isinstance(value, dict):
        return [{"name": str(key), "value": str(item)} for key, item in value.items()]
    if not isinstance(value, list):
        return []
    result = []
    for item in value:
        if isinstance(item, dict) and "name" in item:
            result.append({"name": str(item["name"]), "value": str(item.get("value", ""))})
    return result


def _header_value(headers: list[dict[str, str]], name: str) -> str:
    for header in headers:
        if header["name"].lower() == name.lower():
            return header["value"]
    return ""


def _normalize_flow(flow: Any, *, provider: str) -> dict:
    if not isinstance(flow, dict):
        raise NetworkCaptureContractError("network capture flow must be an object")
    if provider == "contract" and flow.get("schema_version") != CAPTURE_SCHEMA_VERSION:
        raise NetworkCaptureContractError("unsupported network capture schema_version")

    request = flow.get("request") if isinstance(flow.get("request"), dict) else {}
    response = flow.get("response") if isinstance(flow.get("response"), dict) else {}
    request_headers = _pairs(request.get("headers"))
    response_headers = _pairs(response.get("headers"))
    request_body = request.get("body", request.get("postData", {}))
    response_body = response.get("body", response.get("content", {}))
    flow_id = flow.get("id", flow.get("_id", ""))
    if not flow_id:
        raise NetworkCaptureContractError("network capture flow is missing id")

    error = flow.get("error")
    if not isinstance(error, dict):
        error = {}
        if flow.get("_error"):
            error["message"] = str(flow["_error"])
    lifecycle = str(
        flow.get("lifecycle")
        or ("failed" if error or response.get("status") == 0 else "completed")
    )
    messages = flow.get("messages", flow.get("_webSocketMessages", []))
    normalized_messages = []
    if isinstance(messages, list):
        for message in messages:
            if not isinstance(message, dict):
                continue
            payload = message.get("body", message.get("data", message.get("text")))
            normalized_messages.append({
                "direction": str(message.get("direction", message.get("type", "")) or ""),
                "time": message.get("time", message.get("started_at")),
                "opcode": message.get("opcode") if isinstance(message.get("opcode"), int) else None,
                "body": _body({
                    "text": payload,
                    "encoding": message.get("encoding", ""),
                    "mimeType": message.get("mime_type", message.get("mimeType", "")),
                    "available": payload is not None,
                    "truncation_reason": message.get("truncation_reason"),
                }),
            })
    raw_timings = flow.get("timings") if isinstance(flow.get("timings"), dict) else {}
    timings = {
        key: (None if value == -1 else value) for key, value in raw_timings.items()
        if key in {"blocked", "dns", "connect", "send", "wait", "receive", "ssl"}
        and isinstance(value, (int, float))
    }
    total = flow.get("duration", flow.get("time"))
    if isinstance(total, (int, float)):
        timings["total"] = None if total == -1 else total
    return {
        "schema_version": CAPTURE_SCHEMA_VERSION,
        "id": str(flow_id),
        "lifecycle": lifecycle,
        "resource_type": str(flow.get("resource_type", flow.get("_resourceType", flow.get("type", "http"))) or "http"),
        "started_at": str(flow.get("started_at", flow.get("startedDateTime", "")) or ""),
        "request": {
            "method": str(request.get("method", "")),
            "url": str(request.get("url", "")),
            "http_version": str(request.get("http_version", request.get("httpVersion", "")) or ""),
            "headers": request_headers,
            "query": _pairs(request.get("query", request.get("queryString"))),
            "cookies": _pairs(request.get("cookies")),
            "body": _body(
                request_body,
                fallback_mime_type=_header_value(request_headers, "content-type"),
                fallback_size=request.get("bodySize"),
                fallback_content_encoding=_header_value(
                    request_headers, "content-encoding"
                ),
            ),
        },
        "response": {
            "status": response.get("status") if isinstance(response.get("status"), int) else None,
            "status_text": str(response.get("status_text", response.get("statusText", "")) or ""),
            "http_version": str(response.get("http_version", response.get("httpVersion", "")) or ""),
            "redirect_url": str(response.get("redirect_url", response.get("redirectURL", "")) or ""),
            "headers": response_headers,
            "cookies": _pairs(response.get("cookies")),
            "body": _body(
                response_body,
                fallback_mime_type=_header_value(response_headers, "content-type"),
                fallback_size=response.get("bodySize"),
                fallback_content_encoding=_header_value(
                    response_headers, "content-encoding"
                ),
            ),
        },
        "error": {
            "code": str(error.get("code", "") or ""),
            "message": str(error.get("message", "") or ""),
        } if error else None,
        "timings": timings,
        "connection": {
            "server_ip": str(flow.get("server_ip", flow.get("serverIPAddress", "")) or ""),
            "id": str(flow.get("connection", flow.get("connection_id", "")) or ""),
        },
        "messages": normalized_messages,
    }


def _flows_payload(payload: Any, *, provider: str) -> list[Any]:
    if provider == "lambda-har":
        if isinstance(payload, dict):
            return payload.get("log", {}).get("entries", []) if isinstance(payload.get("log"), dict) else []
        return []
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        flows = payload.get("flows", payload.get("data"))
        if isinstance(flows, list):
            return flows
    raise NetworkCaptureContractError("network capture list response must contain a flows list")


def _detail_payload(payload: Any, *, provider: str) -> Any:
    if provider == "lambda-har":
        if not isinstance(payload, dict):
            return None
        # Device-host builds have returned both a bare HAR entry and the
        # historical {"entry": ...} wrapper; normalize either without exposing it.
        return payload.get("entry", payload.get("flow", payload))
    if isinstance(payload, dict):
        return payload.get("flow", payload.get("data", payload))
    return None


def _fetch_flow(kind: str, base: str, flow_id: str, timeout: int) -> dict:
    if kind == "contract":
        endpoint = f"{base}/v1/network/capture/flows/{quote(str(flow_id), safe='')}"
    else:
        endpoint = f"{base}/har/{quote(str(flow_id), safe='')}"
    status, payload = _request_json(endpoint, timeout=timeout)
    if status == 404:
        raise NetworkCaptureNotFound("network capture flow id was not found")
    if status < 200 or status >= 300:
        raise NetworkCaptureUnavailable(f"network capture provider returned HTTP {status}")
    flow = _detail_payload(payload, provider=kind)
    if not flow:
        raise NetworkCaptureNotFound("network capture flow id was not found")
    return _normalize_flow(flow, provider=kind)


def _list_flows(kind: str, base: str, timeout: int) -> list[dict]:
    endpoint = f"{base}/v1/network/capture/flows" if kind == "contract" else f"{base}/har"
    status, payload = _request_json(endpoint, timeout=timeout)
    if status < 200 or status >= 300:
        raise NetworkCaptureUnavailable(f"network capture provider returned HTTP {status}")
    return [_normalize_flow(flow, provider=kind) for flow in _flows_payload(payload, provider=kind)]


def _capture_contract(contract: Any) -> tuple[dict, dict]:
    """Validate the deliberately small, generator-facing capture contract."""
    if not isinstance(contract, dict) or set(contract) != {"schema_version", "selector", "wait"}:
        raise NetworkCaptureContractError(
            "network capture contract must contain exactly schema_version, selector, and wait"
        )
    if contract["schema_version"] != CAPTURE_SCHEMA_VERSION:
        raise NetworkCaptureContractError("unsupported network capture schema_version")
    selector, wait = contract["selector"], contract["wait"]
    if not isinstance(selector, dict) or set(selector) != {"method", "url", "occurrence", "flow_id"}:
        raise NetworkCaptureContractError(
            "network capture selector must contain exactly method, url, occurrence, and flow_id"
        )
    if not isinstance(wait, dict) or set(wait) != {"poll_interval_ms", "timeout_ms"}:
        raise NetworkCaptureContractError(
            "network capture wait must contain exactly poll_interval_ms and timeout_ms"
        )
    if not isinstance(selector["method"], str) or not isinstance(selector["url"], str) or not isinstance(selector["flow_id"], str):
        raise NetworkCaptureContractError("network capture selector method, url, and flow_id must be strings")
    if not _METHOD_RE.fullmatch(selector["method"]):
        raise NetworkCaptureContractError(
            "network capture method must be an uppercase HTTP method"
        )
    try:
        parsed_url = urlsplit(selector["url"])
    except ValueError as exc:
        raise NetworkCaptureContractError(
            "network capture URL must be an absolute HTTP or HTTPS URL"
        ) from exc
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        raise NetworkCaptureContractError(
            "network capture URL must be an absolute HTTP or HTTPS URL"
        )
    if selector["flow_id"] and (
        len(selector["flow_id"]) > 256
        or any(char.isspace() for char in selector["flow_id"])
    ):
        raise NetworkCaptureContractError(
            "network capture flow_id must not contain whitespace and must be "
            "at most 256 characters"
        )
    if (
        isinstance(selector["occurrence"], bool)
        or not isinstance(selector["occurrence"], int)
        or not 0 <= selector["occurrence"] <= _MAX_OCCURRENCE
    ):
        raise NetworkCaptureContractError(
            f"network capture occurrence must be between 0 and {_MAX_OCCURRENCE}"
        )
    for field in ("poll_interval_ms", "timeout_ms"):
        if (
            isinstance(wait[field], bool)
            or not isinstance(wait[field], int)
            or not 1 <= wait[field] <= _MAX_TIMEOUT_MS
        ):
            raise NetworkCaptureContractError(
                f"network capture {field} must be between 1 and "
                f"{_MAX_TIMEOUT_MS}"
            )
    if wait["timeout_ms"] < wait["poll_interval_ms"]:
        raise NetworkCaptureContractError(
            "network capture timeout_ms must be greater than or equal to poll_interval_ms"
        )
    return selector, wait


def network_capture_capabilities() -> dict:
    """Return provider readiness/capabilities without querying captured flows.

    Contract providers expose ``GET /v1/network/capture/capabilities``.  The
    legacy Lambda HAR sidecar has no equivalent endpoint, so its supported
    capabilities and limitations are pinned by this adapter.
    """
    kind, base = _provider()
    if kind == "lambda-har":
        return {
            "schema_version": CAPTURE_SCHEMA_VERSION,
            "provider": "lambda-har",
            "protocols": ["http", "https", "websocket", "sse"],
            "https_decryption": True,
            "request_bodies": "partial",
            "response_bodies": "partial",
            "live_events": False,
            "tls_metadata": False,
            "limitations": ["legacy HAR provider; request and response bodies may be omitted or truncated"],
        }
    status, payload = _request_json(f"{base}/v1/network/capture/capabilities", timeout=10)
    if status < 200 or status >= 300:
        raise NetworkCaptureUnavailable(f"network capture provider returned HTTP {status}")
    if not isinstance(payload, dict) or payload.get("schema_version") != CAPTURE_SCHEMA_VERSION:
        raise NetworkCaptureContractError("network capture capabilities have an unsupported schema_version")
    required = {
        "provider": str,
        "protocols": list,
        "https_decryption": bool,
        "request_bodies": str,
        "response_bodies": str,
        "live_events": bool,
        "tls_metadata": bool,
        "limitations": list,
    }
    for field, expected_type in required.items():
        if not isinstance(payload.get(field), expected_type):
            raise NetworkCaptureContractError(
                f"network capture capabilities.{field} has an invalid type"
            )
    if not payload["provider"]:
        raise NetworkCaptureContractError(
            "network capture capabilities.provider must not be empty"
        )
    if not all(isinstance(item, str) and item for item in payload["protocols"]):
        raise NetworkCaptureContractError(
            "network capture capabilities.protocols must contain strings"
        )
    if payload["request_bodies"] not in {"complete", "partial", "unavailable"}:
        raise NetworkCaptureContractError(
            "network capture capabilities.request_bodies is invalid"
        )
    if payload["response_bodies"] not in {"complete", "partial", "unavailable"}:
        raise NetworkCaptureContractError(
            "network capture capabilities.response_bodies is invalid"
        )
    if not all(isinstance(item, str) for item in payload["limitations"]):
        raise NetworkCaptureContractError(
            "network capture capabilities.limitations must contain strings"
        )
    return payload


def network_capture_query(driver, *, contract: dict) -> dict:
    """Canonical ``network.capture.v1`` query API used by generated artifacts.

    ``contract`` is exactly ``{schema_version, selector, wait}``; occurrence is
    zero-based and matching is exact for both method and URL.  A non-empty
    ``flow_id`` selects the detail endpoint directly.
    """
    del driver
    selector, wait = _capture_contract(contract)
    kind, base = _provider()
    timeout = max(1, math.ceil(wait["timeout_ms"] / 1000))
    if selector["flow_id"]:
        # The recorded flow id is a fast path, not an identity: it was minted
        # by the AUTHORING session's provider, and a replay's provider mints
        # its own — so a miss is the expected case there, and the live
        # method/url match below is what actually re-finds the flow (the web
        # helper's semantics exactly). The contract guarantees the selector:
        # method and url are validated non-empty above.
        try:
            return _fetch_flow(kind, base, selector["flow_id"], timeout)
        except NetworkCaptureError as exc:
            _log.info(
                "[network_query] flow id %s did not resolve (%s); matching by "
                "method/url instead", selector["flow_id"], exc)

    deadline = time.monotonic() + (wait["timeout_ms"] / 1000)
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        flows = _list_flows(kind, base, min(timeout, max(1, math.ceil(remaining))))
        matches = [
            flow for flow in flows
            if flow["request"]["method"] == selector["method"]
            and flow["request"]["url"] == selector["url"]
        ]
        if len(matches) > selector["occurrence"]:
            return matches[selector["occurrence"]]
        remaining = deadline - time.monotonic()
        if remaining > 0:
            time.sleep(min(wait["poll_interval_ms"] / 1000, remaining))
    raise NetworkCaptureTimeout(
        "network capture did not observe occurrence "
        f"{selector['occurrence']} of {selector['method']!r} {selector['url']!r}"
    )


def network_query(
    driver,
    *,
    method: str = "",
    url: str = "",
    index: int = 0,
    network_log_id: str = "",
    polling_interval: int = 2,
    max_polling_time: int = 10,
    output_variable: str = "",
    description: str = "",
) -> dict:
    """Legacy wrapper translating flat generated arguments to ``network.capture.v1``.

    The public output is always a ``network.capture.v1`` dictionary.  The
    capture URL is configuration only (environment/runtime detail), never a
    generated-artifact argument.  Missing capture, timeout, malformed provider
    output, and a requested id that does not exist are typed failures.
    """
    del description
    try:
        poll_interval_ms = int(float(polling_interval) * 1000)
        timeout_ms = int(float(max_polling_time) * 1000)
        # The generated argument counts occurrences the way V2's poll loop and
        # the web helper do — 1-based, `index=1` is the FIRST match — while the
        # canonical contract's occurrence is 0-based. Passing it raw asked for
        # the occurrence AFTER the recorded one, which for a single matching
        # flow is a guaranteed timeout.
        occurrence = max(0, int(index) - 1)
    except (TypeError, ValueError) as exc:
        raise NetworkCaptureContractError("legacy polling times must be numeric") from exc
    result = network_capture_query(driver, contract={
        "schema_version": CAPTURE_SCHEMA_VERSION,
        "selector": {
            "method": method, "url": url, "occurrence": occurrence, "flow_id": network_log_id,
        },
        "wait": {"poll_interval_ms": poll_interval_ms, "timeout_ms": timeout_ms},
    })
    if output_variable:
        set_var(output_variable, result)
    return result


_TOKEN = re.compile(r"^\s*(?:\{\{(?P<braced>.+?)\}\}|\$\{(?P<dollar>.+?)\})\s*$")
_PART = re.compile(r"([^.[\]]+)|\[(\d+)\]")


def _lookup(path: str) -> tuple[Any, str | None]:
    parts: list[str | int] = []
    for index, match in enumerate(_PART.finditer(path)):
        token = match.group(1)
        if match.group(2) is not None:
            parts.append(int(match.group(2)))
        elif index > 0 and token.isdigit():
            parts.append(int(token))
        else:
            parts.append(token)
    if not parts or not isinstance(parts[0], str) or parts[0] not in _variable_store:
        return None, "variable_unavailable"
    value: Any = _variable_store[parts[0]]
    for part in parts[1:]:
        if isinstance(value, dict) and value.get("available") is False and (
            part in {"data", "json"} or "body" in path
        ):
            return None, "body_unavailable"
        if isinstance(part, int):
            if not isinstance(value, list) or part >= len(value):
                return None, "path_unavailable"
            value = value[part]
        elif isinstance(value, dict):
            if part not in value:
                return None, "path_unavailable"
            value = value[part]
        else:
            return None, "path_unavailable"
    if isinstance(value, dict) and value.get("available") is False:
        return None, "body_unavailable"
    return value, None


def _resolve_operand(operand: Any) -> tuple[Any, str | None]:
    if isinstance(operand, dict) and len(operand) == 1:
        operand = next(iter(operand))
    if not isinstance(operand, str):
        return operand, None
    match = _TOKEN.match(operand)
    return _lookup(match.group("braced") or match.group("dollar")) if match else (operand, None)


def _leaf(node: dict) -> tuple[str, dict]:
    op = str(node.get("operator", "")).lower()
    left, left_reason = _resolve_operand(node.get("left_operand", ""))
    right, right_reason = _resolve_operand(node.get("right_operand", ""))
    evidence = {"operator": op, "left": left, "right": right}
    if op in {"exists", "not_exists"}:
        if left_reason == "body_unavailable":
            evidence.update(status="indeterminate", reason=left_reason)
            return "indeterminate", evidence
        exists = left_reason is None
        status = "passed" if exists == (op == "exists") else "failed"
        evidence["status"] = status
        if left_reason:
            evidence["reason"] = left_reason
        return status, evidence
    if left_reason or right_reason:
        evidence["status"] = "indeterminate"
        evidence["reason"] = left_reason or right_reason
        return "indeterminate", evidence
    left_str, right_str = str(left), str(right)
    try:
        comparisons = {
            "equals": lambda: (str(left).lower() == str(right).lower()) if isinstance(left, bool) or isinstance(right, bool) else left_str == right_str,
            "not_equals": lambda: (str(left).lower() != str(right).lower()) if isinstance(left, bool) or isinstance(right, bool) else left_str != right_str,
            "contains": lambda: right_str in left_str,
            "not_contains": lambda: right_str not in left_str,
            "greater_than": lambda: float(left) > float(right),
            "greater_than_or_equal": lambda: float(left) >= float(right),
            "less_than": lambda: float(left) < float(right),
            "less_than_or_equal": lambda: float(left) <= float(right),
            "start_with": lambda: left_str.startswith(right_str),
            "end_with": lambda: left_str.endswith(right_str),
            "matches": lambda: re.search(right_str, left_str) is not None,
        }
        if op not in comparisons:
            evidence.update(status="indeterminate", reason="unknown_operator")
            return "indeterminate", evidence
        status = "passed" if comparisons[op]() else "failed"
    except (TypeError, ValueError, re.error):
        status = "failed"
    evidence["status"] = status
    return status, evidence


def _referenced_flow_ids(node: Any) -> set[str]:
    """Find flow roots used by token operands, including scalar dotted paths."""
    if not isinstance(node, dict):
        return set()
    found: set[str] = set()
    for key in ("left_operand", "right_operand"):
        operand = node.get(key)
        if isinstance(operand, str):
            match = _TOKEN.match(operand)
            if match:
                path = match.group("braced") or match.group("dollar")
                parts = list(_PART.finditer(path))
                if parts and parts[0].group(1):
                    root = _variable_store.get(parts[0].group(1))
                    if isinstance(root, dict) and root.get("schema_version") == CAPTURE_SCHEMA_VERSION and root.get("id"):
                        found.add(str(root["id"]))
    for child in node.get("operands", []):
        found.update(_referenced_flow_ids(child))
    return found


def _evaluate(node: Any) -> tuple[str, dict]:
    if not isinstance(node, dict):
        return "indeterminate", {"status": "indeterminate", "reason": "invalid_node"}
    op = str(node.get("operator", "")).lower()
    if op not in {"and", "or"}:
        return _leaf(node)
    children = [_evaluate(child) for child in node.get("operands", [])]
    statuses = [status for status, _ in children]
    if not children:
        status = "indeterminate"
    elif op == "and":
        status = "failed" if "failed" in statuses else "indeterminate" if "indeterminate" in statuses else "passed"
    else:
        status = "passed" if "passed" in statuses else "indeterminate" if "indeterminate" in statuses else "failed"
    return status, {"operator": op, "status": status, "evaluations": [evidence for _, evidence in children]}


def evaluate_network_assertion(
    assertion_tree: dict,
    *,
    contract_version: str = ASSERTION_SCHEMA_VERSION,
) -> dict:
    """Evaluate a recorded network assertion tree and return ``network.assert.v1``.

    Failed and indeterminate results raise :class:`NetworkAssertionError` unless
    ``TESTMU_SKIP_ASSERTION_FAILURE`` is a truthy value.  The returned result
    includes per-node evidence, making unavailable captured bodies visibly
    indeterminate instead of treating them as empty payloads.
    """
    if contract_version != ASSERTION_SCHEMA_VERSION:
        raise NetworkAssertionError(
            "unsupported network assertion schema_version",
            {"schema_version": ASSERTION_SCHEMA_VERSION, "outcome": "indeterminate", "status": "indeterminate", "evaluations": []},
        )
    status, evaluation = _evaluate(assertion_tree)
    # A tree normally references a stored flow through a dotted variable path.
    # Include IDs recursively from resolved operands without requiring producers
    # to add a second, non-semantic field to the assertion AST.
    def _flow_ids(evidence: Any) -> set[str]:
        if not isinstance(evidence, dict):
            return set()
        found = set()
        for value in (evidence.get("left"), evidence.get("right")):
            if isinstance(value, dict) and value.get("schema_version") == CAPTURE_SCHEMA_VERSION and value.get("id"):
                found.add(str(value["id"]))
        for child in evidence.get("evaluations", []):
            found.update(_flow_ids(child))
        return found
    result = {
        "schema_version": ASSERTION_SCHEMA_VERSION,
        "outcome": status,
        "status": status,
        "tree": assertion_tree,
        "evaluations": [evaluation],
        "matched_flow_ids": sorted(_flow_ids(evaluation) | _referenced_flow_ids(assertion_tree)),
    }
    if status != "passed" and os.getenv("TESTMU_SKIP_ASSERTION_FAILURE", "").strip().lower() not in _TRUTHY:
        raise NetworkAssertionError(f"Network assertion {status}: {assertion_tree}", result)
    return result
