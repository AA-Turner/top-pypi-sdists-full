"""execute_api() — issue an arbitrary HTTP request via the shared retry client.

Deliberately thin compared to the selenium sibling's execute_api (no auth-type
dispatch, no binary-body download) — the mobile AST contract carries only
method/url/headers/body; anything the test author needs beyond that (auth
headers, form-encoding, ...) is expressed as plain headers/body.

Where the request is issued from depends on the run:

- ``TESTMU_API_PROXY_PORT`` set (auteur in-process): direct httpx through that
  proxy — the device's mitm on the same host, so the call lands in the device
  network log. The web binding's env contract; this helper's request only.
- cloud run target with no proxy env (an exported test on HyperExecute): the
  LambdaTest grid hook (``lambda-kane-ai`` / ``executeAPI``). The grid forwards
  the payload to auteur beside the device, which issues the request through the
  local mitm — the V2 exported runtime's path (auteur models/appium_uiActions.py::
  execute_api_action). The HYE box cannot reach the device's proxy itself, so a
  direct request from there never appears in the network log.
- otherwise (local): direct httpx, no proxy.
"""
import json
import logging
import math

import httpx
from typing import Any

from testmu_appium import _config
from testmu_appium._helpers._http import request_with_retry
from testmu_appium._helpers.driver import get_driver
from testmu_appium._vars import set_var, var

_log = logging.getLogger("testmu_appium")


def _resolve_str(value: str) -> str:
    """Resolve a value that has to reach the wire as text (the URL, a header)."""
    if not isinstance(value, str):
        return value
    resolved = var(value)
    return resolved if isinstance(resolved, str) else str(resolved)


def _resolve_deep(obj: Any) -> Any:
    """Recursively resolve {{var}}/${var} tokens in every string leaf of a dict/list.

    NATIVE TYPES SURVIVE. `var()` returns the stored value unchanged for a
    whole-string template, so `{"qty": "{{n}}"}` with n=42 sends the JSON number 42
    and `{"active": "{{flag}}"}` with flag=True sends the JSON literal `true`. No
    leaf is coerced to `str` on this path.
    """
    if isinstance(obj, dict):
        return {k: _resolve_deep(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_resolve_deep(item) for item in obj]
    if isinstance(obj, str):
        return var(obj)
    return obj


def _wire_headers(headers: dict) -> dict:
    """Header values as text.

    Headers are the one place native types cannot survive: HTTP header values are
    byte strings, and httpx rejects anything else. The resolution itself is still the
    native `_resolve_deep` walk, so `{{n}}` resolves to 42 and is rendered as '42'
    here.
    """
    return {key: value if isinstance(value, str) else str(value)
            for key, value in headers.items()}


def _hook_headers(headers) -> dict:
    """Response headers as a dict, whichever shape the hook answered with.

    auteur's helper flattens ``httpx.Headers`` to a list of single-key dicts
    (``[{"content-type": "application/json"}, ...]``); the binding's contract is
    a dict.
    """
    if isinstance(headers, dict):
        return dict(headers)
    merged: dict = {}
    for item in headers or []:
        if isinstance(item, dict):
            merged.update(item)
    return merged


def _via_hook(driver, *, method: str, url: str, headers: dict, body, params,
              timeout, verify: bool, follow_redirects: bool) -> dict:
    """Issue the request through the grid hook; returns the binding's result shape.

    The payload mirrors the V2 exported runtime's call exactly (method, url,
    headers, body, params, authorization, timeout in ms, verify, settings);
    auteur's ``execute_api_helper`` divides ``timeout`` by 1000. ``requestTimeout``
    is the grid's own client deadline, in seconds. A grid-side failure surfaces
    as the driver's WebDriverException, as it does for V2; auteur's own refusal
    (``{"status": 400|408, "message": ...}``) is returned as the result.
    """
    payload = {
        "method": method.upper(),
        "url": url,
        "headers": headers,
        "body": body,
        "params": params or {},
        "authorization": {},
        "verify": verify,
        "settings": {"automatically_follow_redirect": follow_redirects},
    }
    args = {"command": "executeAPI", "testId": driver.session_id, "payload": payload}
    if timeout is not None:
        payload["timeout"] = int(float(timeout) * 1000)
        args["requestTimeout"] = int(float(timeout))
    _log.info("[execute_api] via grid hook (device-side proxy)")
    response = driver.execute_script("lambda-kane-ai", args)
    if not isinstance(response, dict):
        raise RuntimeError(f"invalid executeAPI response from lambda hook: {response!r}")

    status = response.get("status", response.get("status_code"))
    parsed_body = response.get("response_body", response.get("body"))
    result = {
        "status": status,
        "response_body": parsed_body,
        "status_code": status,
        "headers": _hook_headers(response.get("headers")),
        "body": parsed_body,
    }
    if response.get("message") is not None:
        result["message"] = response["message"]
    return result


def execute_api(
    *,
    method: str,
    url: str,
    headers: dict | None = None,
    body=None,
    params: dict | None = None,
    authorization: str | None = None,
    timeout: float | None = None,
    timeout_ms: float | None = None,
    verify: bool = True,
    settings: dict | None = None,
    output_variable: str = "",
    description: str = "",
) -> dict:
    """Issue an HTTP request and return its status/headers/body.

    ``{{var}}``/``${var}`` tokens are resolved in ``url``, every header value,
    and every string leaf of ``body`` and ``params`` before the request is sent.
    Body and param leaves keep the stored value's NATIVE type — a leaf recorded as
    ``"{{n}}"`` with ``n=42`` is sent as the JSON number ``42``, and one recorded as
    ``"{{flag}}"`` with ``flag=True`` as the JSON literal ``true``. Header values are
    rendered as text, because HTTP header values are byte strings.

    Args:
        method: HTTP method (GET, POST, PUT, PATCH, DELETE, ...).
        url: Request URL. May carry variable tokens.
        headers: Request headers. May carry variable tokens in values; values are
            rendered as text.
        body: Request body — dict/list (sent as JSON) or a string (sent as-is).
            May carry variable tokens in string leaves, which resolve to their
            native stored type.
        params: Query-string parameters. May carry variable tokens in values.
        authorization: Value for the Authorization header, e.g. "Bearer {{token}}".
            An explicit Authorization in `headers` wins — the recorded header is
            more specific than the recorded field.
        timeout: Request timeout in seconds. None uses the shared client default.
        timeout_ms: Explicit millisecond timeout for generated API calls.
            Mutually exclusive with timeout. The budget also bounds retries.
        verify: TLS certificate verification. False only for a recorded call
            against a self-signed staging host.
        settings: Request settings, matching V4 web. Automatically follow
            redirects unless automatically_follow_redirect is explicitly False.
        output_variable: When non-empty, the result dict is written via
            ``set_var(output_variable, result)``.
        description: Step description (logging only).

    Returns:
        ``{"status_code": int, "headers": dict, "body": <parsed JSON or text>}``.

    Raises:
        RuntimeError: On request timeout, matching V4 web execution failures.
    """
    if timeout_ms is not None:
        if timeout is not None:
            raise ValueError("Specify only one of timeout and timeout_ms")
        if (isinstance(timeout_ms, bool) or not isinstance(timeout_ms, (int, float))
                or not math.isfinite(timeout_ms) or timeout_ms <= 0):
            raise ValueError("timeout_ms must be a positive finite number")
        timeout = timeout_ms / 1000

    follow_redirects = (settings or {}).get("automatically_follow_redirect", True)

    resolved_url = _resolve_str(url)
    resolved_headers: dict = _resolve_deep(headers or {})
    resolved_params = _resolve_deep(params) if params else None
    resolved_body = _resolve_deep(body) if body is not None else None

    # Match V4 web: parse a string body once before choosing its wire encoding.
    # Auteur json.dumps() wraps raw JSON text; one decode removes that wrapper
    # so it is sent as JSON text rather than as a quoted JSON string.
    if isinstance(resolved_body, str):
        try:
            parsed_body = json.loads(resolved_body)
        except (json.JSONDecodeError, TypeError):
            pass  # Plain text/form bodies keep their original bytes.
        else:
            # Keep scalar JSON text as text: httpx content= cannot send a
            # bool/number/None, and the original text already encodes it.
            if isinstance(parsed_body, (dict, list, str)):
                resolved_body = _resolve_deep(parsed_body)

    if authorization is not None and not any(
        key.lower() == "authorization" for key in resolved_headers
    ):
        resolved_headers["Authorization"] = _resolve_str(authorization)

    _log.info("[execute_api] %s %s", method, resolved_url)

    wire_headers = _wire_headers(resolved_headers)
    proxy = _config.get_api_proxy_url()

    try:
        if proxy is None and _config.run_target == "cloud":
            driver = get_driver()
            if driver is None:
                raise RuntimeError(
                    "execute_api on a cloud run issues the request through the "
                    "LambdaTest grid hook and needs the live session (run it inside "
                    "testmu_appium.run)"
                )
            result = _via_hook(
                driver, method=method, url=resolved_url, headers=wire_headers,
                body=resolved_body, params=resolved_params, timeout=timeout, verify=verify,
                follow_redirects=follow_redirects,
            )
        else:
            request_kwargs: dict = {}
            if isinstance(resolved_body, (dict, list)):
                request_kwargs["json_data"] = resolved_body
            elif resolved_body is not None:
                request_kwargs["data"] = resolved_body

            if resolved_params:
                request_kwargs["params"] = resolved_params
            if timeout is not None:
                request_kwargs["timeout"] = timeout
                request_kwargs["total_timeout_s"] = timeout

            response = request_with_retry(
                method.upper(), resolved_url,
                headers=wire_headers or None,
                verify=verify, proxy=proxy, follow_redirects=follow_redirects, **request_kwargs,
            )

            try:
                parsed_body = response.json()
            except ValueError:  # json.JSONDecodeError is a ValueError subclass
                parsed_body = response.text

            result = {
                # Canonical API-variable names shared with the Playwright/Selenium
                # bindings and V16 objectives. Keep the Appium names below as aliases
                # for backwards compatibility with existing generated tests.
                "status": response.status_code,
                "response_body": parsed_body,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "body": parsed_body,
            }
    except httpx.TimeoutException as exc:
        # Match V4 web: fail the API step so Auteur displays the execution error.
        # Do not synthesize an HTTP response or publish an output variable.
        raise RuntimeError(f"execute_api failed: {exc}") from exc
    _log.info("[execute_api] status_code=%s", result["status_code"])
    if output_variable:
        set_var(output_variable, result)
    return result
