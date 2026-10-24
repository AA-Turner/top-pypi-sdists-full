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
import time
from typing import Any
from urllib.parse import urlparse

import httpx

from testmu_appium import _config
from testmu_appium._v4._helpers._api_log import _enabled, _scrub, has_secret, log_api_call, scrub_tree
from testmu_appium._v4._helpers._http import TransientHTTPError, request_with_retry
from testmu_appium._v4._helpers._wire import WireCapture
from testmu_appium._v4._helpers.driver import get_driver
from testmu_appium._v4._vars import _SECRET_VALUES, _mark_secret, set_var, var

_log = logging.getLogger("testmu_appium")


def _resolve_str(value: str) -> str:
    """Resolve a value that has to reach the wire as text (the URL, a header)."""
    if not isinstance(value, str):
        return value
    resolved = var(value)
    return resolved if isinstance(resolved, str) else str(resolved)


def _maybe_json_container(value: Any, kinds) -> Any:
    if not isinstance(value, str) or not value.strip():
        return value
    try:
        decoded = json.loads(value)
    except (ValueError, TypeError):
        return value
    return decoded if isinstance(decoded, kinds) else value


def _structured_auth(authorization: Any) -> dict | None:
    candidate = _maybe_json_container(authorization, dict)
    if isinstance(candidate, dict) and isinstance(candidate.get("type"), str):
        return candidate
    return None


def _apply_header_auth(auth: dict, headers: dict) -> None:
    if any(str(key).lower() == "authorization" for key in headers):
        return
    auth_type = str(auth.get("type", "")).lower()
    data = auth.get("data") or {}
    if not isinstance(data, dict):
        return
    if auth_type == "bearer" and data.get("token"):
        headers["Authorization"] = f"Bearer {data['token']}"
    elif auth_type == "basic" and data.get("username"):
        import base64 as _b64
        cred = _b64.b64encode(f"{data['username']}:{data.get('password', '')}".encode()).decode()
        headers["Authorization"] = f"Basic {cred}"
        if {data["username"], data.get("password")} & _SECRET_VALUES:
            _mark_secret(cred)  # a server that echoes the header would print it


def _apply_aws_signature(auth: dict, *, method: str, url: str, body, headers: dict, params: dict) -> None:
    data = auth.get("data") or {}
    if not isinstance(data, dict):
        return
    try:
        from botocore.auth import SigV4Auth, SigV4QueryAuth
        from botocore.awsrequest import AWSRequest
        from botocore.credentials import Credentials
        from urllib.parse import parse_qs, urlparse
    except Exception as exc:
        _log.warning("[execute_api] aws-signature auth skipped, botocore unavailable: %s", exc)
        return
    try:
        service_name = str(data.get("service_name", ""))
        payload = body if isinstance(body, (str, bytes)) else (json.dumps(body) if body else None)
        aws_req = AWSRequest(method=method.upper(), url=url, data=payload)
        if service_name.lower() == "s3":
            aws_req.context["payload_signing_enabled"] = False
        credentials = Credentials(data.get("access_key"), data.get("secret_key"), data.get("session_token"))
        region = data.get("region", "us-east-1")
        if data.get("add_to") == "params":
            SigV4QueryAuth(credentials, service_name, region).add_auth(aws_req)
            signed = parse_qs(urlparse(aws_req.url).query)
            params.update({k: v[0] if len(v) == 1 else v for k, v in signed.items()})
        else:
            SigV4Auth(credentials, service_name, region).add_auth(aws_req)
            headers.update(dict(aws_req.headers))
    except Exception as exc:
        _log.warning("[execute_api] aws-signature signing failed: %s", exc)


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


def _timeout_response(timeout) -> dict:
    """The 408 result a timed-out request resolves to (auteur's hook shape)."""
    return {
        "status": 408,
        "response_body": None,
        "status_code": 408,
        "headers": {},
        "body": None,
        "message": "Request Timed out",
        "time": int(float(timeout) * 1000) if timeout is not None else None,
    }


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


def _timeout_seconds(timeout):
    if timeout is None:
        return None
    try:
        value = float(timeout)
    except (TypeError, ValueError):
        return None
    if value <= 0:
        return None
    return value / 1000 if value > 100 else value

def _via_hook(driver, *, method: str, url: str, headers: dict, body, params,
              timeout, verify: bool, settings: dict | None = None, normalize: bool = False,
              authorization: dict | None = None) -> dict:
    """Issue the request through the grid hook; returns the binding's result shape.

    The payload mirrors the V2 exported runtime's call exactly (method, url,
    headers, body, params, authorization, timeout in ms, verify, settings);
    auteur's ``execute_api_helper`` divides ``timeout`` by 1000. ``requestTimeout``
    is the grid's own client deadline, in seconds. A grid-side failure surfaces
    as the driver's WebDriverException, as it does for V2; auteur's own refusal
    (``{"status": 400|408, "message": ...}``) is returned as the result.
    ``settings`` is the step's own (automatically_follow_redirect, normalization)
    so auteur honours the recorded redirect choice; the default matches V2.

    A dict or list body is sent as JSON text, the shape of V2's recorded body;
    a string body is sent as is.
    """
    hook_settings = {"automatically_follow_redirect": True}
    hook_settings.update(settings or {})
    if isinstance(body, (dict, list)):
        body = json.dumps(body)
    payload = {
        "method": method.upper(),
        "url": url,
        "headers": headers,
        "body": body,
        "params": params or {},
        "authorization": authorization or {},
        "verify": verify,
        "settings": hook_settings,
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
    if normalize:
        result = _normalize_hook(result, response)
    return result


_GUARANTEED_HEADERS = ("content-type", "cache-control", "x-request-id", "x-ratelimit-remaining")


def _fold_pairs(pairs) -> dict:
    folded: dict = {}
    for k, v in pairs:
        fk = str(k).lower()
        folded[fk] = f"{folded[fk]}, {v}" if fk in folded else v
    return folded


def _normalize_direct(result: dict, response) -> dict:
    result["headers"] = _fold_pairs(response.headers.multi_items())
    result["cookies"] = _fold_pairs((c.name, c.value) for c in response.cookies.jar)
    for _gh in _GUARANTEED_HEADERS:
        result["headers"].setdefault(_gh, "")
    if not response.content:
        result["body"] = None
        result["response_body"] = None
    return result


def _normalize_hook(result: dict, response: dict) -> dict:
    result["headers"] = _fold_pairs(result.get("headers", {}).items())
    cookies = response.get("cookies")
    if isinstance(cookies, dict):
        result["cookies"] = _fold_pairs(cookies.items())
    else:
        result["cookies"] = _fold_pairs(
            (k, v) for item in (cookies or []) if isinstance(item, dict) for k, v in item.items())
    for _gh in _GUARANTEED_HEADERS:
        result["headers"].setdefault(_gh, "")
    if result.get("body") in ("", b""):
        result["body"] = None
        result["response_body"] = None
    return result


def execute_api(
    *,
    method: str,
    url: str,
    headers: dict | None = None,
    body=None,
    params: dict | None = None,
    authorization: str | None = None,
    timeout: int | None = None,
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
        authorization: Either the recorded auth object — ``{"type": "bearer" |
            "basic" | "aws-signature", "data": {...}}``, as a dict or its JSON
            text — or a bare value for the Authorization header, e.g.
            "Bearer {{token}}". bearer/basic become the Authorization header;
            aws-signature is signed here on a direct request and by auteur's
            helper on the grid-hook path. An explicit Authorization in
            `headers` wins — the recorded header is more specific.
        timeout: Request timeout as older generated tests emit it — milliseconds,
            with a value of 100 or less read as seconds. None uses the shared
            client default. Mutually exclusive with ``timeout_ms``.
        timeout_ms: Explicit millisecond timeout for generated API calls (the
            code-gen emits this today). The budget also bounds retries.
        verify: TLS certificate verification. False only for a recorded call
            against a self-signed staging host.
        settings: Request settings, matching V4 web. Automatically follow
            redirects unless automatically_follow_redirect is explicitly False.
        output_variable: When non-empty, the result dict is written via
            ``set_var(output_variable, result)``.
        description: Step description (logging only).

    Returns:
        ``{"status_code": int, "headers": dict, "body": <parsed JSON or text>}``.
        A request that exceeds ``timeout`` resolves to a 408 result
        (``status_code=408``, ``body=None``, ``message="Request Timed out"``).
    """
    headers = _maybe_json_container(headers, dict)
    params = _maybe_json_container(params, dict)
    body = _maybe_json_container(body, (dict, list))
    settings = _maybe_json_container(settings, dict)

    if timeout_ms is not None:
        if timeout is not None:
            raise ValueError("Specify only one of timeout and timeout_ms")
        if (isinstance(timeout_ms, bool) or not isinstance(timeout_ms, (int, float))
                or not math.isfinite(timeout_ms) or timeout_ms <= 0):
            raise ValueError("timeout_ms must be a positive finite number")
        timeout_sec = timeout_ms / 1000
    else:
        timeout_sec = _timeout_seconds(timeout)
    # The request as authored, so the API log can name its values and mask secrets
    authored = {"url": url, "headers": headers, "body": body, "params": params, "authorization": authorization}
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

    typed_keys = {str(k).lower() for k in resolved_headers}
    structured_auth = _structured_auth(authorization)
    if structured_auth is not None:
        structured_auth = _resolve_deep(structured_auth)
        _apply_header_auth(structured_auth, resolved_headers)
    elif authorization is not None and not any(
        key.lower() == "authorization" for key in resolved_headers
    ):
        resolved_headers["Authorization"] = _resolve_str(authorization)
    auth_keys = {str(k).lower() for k in resolved_headers} - typed_keys

    if _enabled():  # inside auteur the URL arrives resolved (TESTMU_API_LOG=0)
        _log.info("[execute_api] %s %s", method, _scrub(str(url if has_secret(url) else resolved_url)))

    _settings = settings or {}
    follow_redirects = _settings.get("automatically_follow_redirect", True)
    normalize = bool(_settings.get("normalization", False))

    wire_headers = _wire_headers(resolved_headers)
    proxy = _config.get_api_proxy_url()
    started = time.monotonic()

    def _log_call(**outcome):
        log_api_call(method.upper(), resolved_url, authored=authored, sent_headers=wire_headers,
                     body=resolved_body, auth_keys=auth_keys, params=resolved_params,
                     elapsed_ms=(time.monotonic() - started) * 1000, **outcome)

    # Same check as the Playwright and Selenium bindings: stop before sending, not with httpx's own error
    parsed_url = urlparse(resolved_url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        error = RuntimeError(f"Invalid URL: {resolved_url!r}")
        _log_call(error=error)
        raise error

    if proxy is None and _config.run_target == "cloud":
        driver = get_driver()
        if driver is None:
            raise RuntimeError(
                "execute_api on a cloud run issues the request through the "
                "LambdaTest grid hook and needs the live session (run it inside "
                "testmu_appium.run)"
            )
        try:
            result = _via_hook(
                driver, method=method, url=resolved_url, headers=wire_headers,
                body=resolved_body, params=resolved_params, timeout=timeout_sec, verify=verify,
                settings={"automatically_follow_redirect": follow_redirects,
                          **({"normalization": True} if normalize else {})},
                normalize=normalize,
                authorization=structured_auth,
            )
        except Exception as exc:
            _log_call(error=exc)
            raise
        hook_body = result.get("body")
        _log_call(status=result.get("status_code"), message=result.get("message", ""),
                  size=len(hook_body if isinstance(hook_body, (str, bytes)) else json.dumps(hook_body, default=str))
                  if hook_body is not None else 0)
    else:
        if structured_auth is not None and str(structured_auth.get("type", "")).lower() == "aws-signature":
            resolved_params = dict(resolved_params or {})
            unsigned = {str(k).lower() for k in wire_headers}
            _apply_aws_signature(
                structured_auth, method=method, url=resolved_url, body=resolved_body,
                headers=wire_headers, params=resolved_params)
            auth_keys |= {str(k).lower() for k in wire_headers} - unsigned
            resolved_params = resolved_params or None
        request_kwargs: dict = {"follow_redirects": follow_redirects}
        if isinstance(resolved_body, (dict, list)):
            request_kwargs["json_data"] = resolved_body
        elif resolved_body is not None:
            request_kwargs["data"] = resolved_body

        if resolved_params:
            request_kwargs["params"] = resolved_params
        if timeout_sec is not None:
            request_kwargs["timeout"] = timeout_sec
            request_kwargs["total_timeout_s"] = timeout_sec

        # record the wire request for the API log and auteur's API console
        capture = WireCapture(proxy)
        try:
            response = request_with_retry(
                method.upper(), resolved_url,
                headers=wire_headers or None,
                verify=verify, proxy=proxy, wire=capture, silent=True, **request_kwargs,
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
                "time": (time.monotonic() - started) * 1000,  # ms, as the Playwright binding returns it
            }
            if normalize:
                result = _normalize_direct(result, response)
            request_sent = capture.build(response)
            _log_call(status=response.status_code, reason=getattr(response, "reason_phrase", ""),
                      size=len(getattr(response, "content", b"") or b""), capture=request_sent, response=response)
        except httpx.TimeoutException as exc:
            # A timed-out request is a 408 response the test can assert on, as V2
            # answered it; the step passes and the output variable is written.
            _log.info("[execute_api] timed out: %s", exc)
            result = _timeout_response(timeout_sec)
            request_sent = capture.build(exc=exc, method=method, url=resolved_url)
            _log_call(error=exc, capture=request_sent)
        except Exception as exc:
            exc.api_capture = capture.build(exc=exc, method=method, url=resolved_url)
            # retries ran out on a 408/429/5xx: the server answered, so log its status
            status = exc.status_code if isinstance(exc, TransientHTTPError) else None
            _log_call(status=status, error=None if status else exc, capture=getattr(exc, "api_capture", None))
            raise
        if request_sent:
            result["request_sent"] = scrub_tree(request_sent)
    if output_variable:
        set_var(output_variable, result)
    return result
