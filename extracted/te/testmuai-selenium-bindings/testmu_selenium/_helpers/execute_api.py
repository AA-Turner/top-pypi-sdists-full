"""execute_api helper — makes HTTP API requests, optionally via HyperExecute proxy.

Sync version for the V3 Selenium runtime. Variable resolution: {{var}} templates
in URL, headers, body, and params are resolved via testmu_selenium._vars.var()
before the request is made.

Proxy routing: when running on HyperExecute (TESTMU_RUN_TARGET=cloud),
routes all requests through the local proxy at 127.0.0.1:22000. On local
run target, makes direct requests. TESTMU_API_PROXY_HOST/PORT env vars
override unconditionally when PORT is set.

Raises RuntimeError on request failure (network error or bad/unsupported input).
Returns the response dict directly on success.
"""
import json
import logging
import os
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse, parse_qsl, urlencode

_log = logging.getLogger("testmu_selenium")


_BINARY_CONTENT_TYPES = {
    "application/octet-stream",
    "application/pdf",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}


def _is_binary_content_type(content_type: str) -> bool:
    """Match V2 binary content-type detection — exact set plus
    image/*, audio/*, video/*, text/* prefixes."""
    ct = (content_type or "").lower().strip()
    return (ct in _BINARY_CONTENT_TYPES
            or ct.startswith(("image/", "audio/", "video/", "text/")))


def _resolve_templates(value):
    """Resolve {{var}} templates in a string value using testmu_selenium._vars.var()."""
    if not isinstance(value, str):
        return value
    from testmu_selenium._vars import var
    return var(value)


def _deep_resolve(obj):
    """Recursively resolve {{var}} templates in all string leaves of a dict or list.

    Walks nested dicts and lists; calls _resolve_templates on each string leaf.
    Non-string leaves (int, bool, None, etc.) are returned unchanged, preserving
    native types (e.g. {{n}} where n=42 yields int 42, not str '42').
    """
    if isinstance(obj, dict):
        return {k: _deep_resolve(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_deep_resolve(item) for item in obj]
    if isinstance(obj, str):
        return _resolve_templates(obj)
    return obj


def _get_api_proxy_url() -> Optional[str]:
    """Resolve the API proxy URL at call time.

    PORT is the activation key — when set, env wins unconditionally; otherwise
    fall back to the cloud-only default when TESTMU_RUN_TARGET=cloud, else None.
    """
    port = os.getenv("TESTMU_API_PROXY_PORT")
    if port:
        host = os.getenv("TESTMU_API_PROXY_HOST", "127.0.0.1")
        return f"http://{host}:{port}"
    if os.getenv("TESTMU_RUN_TARGET") == "cloud":
        return "http://127.0.0.1:22000"
    return None


def execute_api(
    method,
    url,
    headers=None,
    body=None,
    params=None,
    authorization=None,
    timeout=30000,
    verify=False,
    settings=None,
):
    """Execute an HTTP API request synchronously.

    Routes through the HyperExecute proxy (127.0.0.1:22000) when
    TESTMU_RUN_TARGET=cloud; makes direct requests on local runs.

    Variable templates ({{var}}) in url, headers, body, and params are resolved
    via testmu_selenium._vars.var() before the request is made.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE, PATCH).
        url: Request URL (may contain {{var}} templates).
        headers: Request headers (dict or JSON string).
        body: Request body (dict, str, or JSON string).
        params: Query parameters (dict or JSON string).
        authorization: Auth config dict with 'type' and 'data' keys.
        timeout: Request timeout in milliseconds (default 30000).
        verify: Whether to verify SSL certificates.
        settings: Settings dict (e.g. automatically_follow_redirect).

    Returns:
        Response dict with keys: status, headers, cookies, body/response_body, time.
        On a request failure (network error, proxy/connect stall, or timeout) the
        request fails OPEN with a soft {"status": 400, "message": "API request
        failed ..."} dict (V2 parity) so the test continues.

    Raises:
        RuntimeError: On invalid URL or unsupported method (input validation).
    """
    import httpx as _httpx

    _log.info("    [execute_api] %s %s", method, url[:80])

    # -- Resolve variable templates ------------------------------------------
    url = _resolve_templates(url)

    # -- Parse string inputs -------------------------------------------------
    _headers = headers or {}
    if isinstance(_headers, str):
        try:
            _headers = json.loads(_headers)
        except (json.JSONDecodeError, TypeError):
            _headers = {}
    _headers = _deep_resolve(_headers)

    _params = params or {}
    if isinstance(_params, str):
        try:
            _params = json.loads(_params)
        except (json.JSONDecodeError, TypeError):
            _params = {}
    _params = _deep_resolve(_params)

    _settings = settings or {}
    follow_redirects = _settings.get("automatically_follow_redirect", True)

    _timeout = timeout
    if isinstance(_timeout, str):
        try:
            _timeout = int(_timeout)
        except (ValueError, TypeError):
            _timeout = 30000
    _timeout_sec = _timeout / 1000 if _timeout and _timeout > 100 else (_timeout or 30)

    # -- Normalise headers ---------------------------------------------------
    # Strip multipart/form-data Content-Type so httpx auto-generates boundary
    if isinstance(_headers, dict):
        _headers = {
            k: v for k, v in _headers.items()
            if not (str(k).lower() == "content-type" and v == "multipart/form-data")
        }

    if isinstance(_headers, dict) and "User-Agent" not in _headers:
        _headers["User-Agent"] = "Mozilla/5.0"

    # -- Validate URL --------------------------------------------------------
    parsed = urlparse(url)
    if not all([parsed.scheme, parsed.netloc]):
        raise RuntimeError(f"Invalid URL: {url!r}")
    if url.startswith("wss://") or url.startswith("ws://"):
        raise RuntimeError("Websockets not supported")
    for hval in (_headers or {}).values():
        if hval == "text/event-stream":
            raise RuntimeError("SSE not supported")

    # -- Handle URL-encoded body ---------------------------------------------
    if isinstance(_headers, dict):
        ct = _headers.get("Content-Type") or _headers.get("content-type") or ""
        if str(ct).lower() == "application/x-www-form-urlencoded" and body and isinstance(body, str):
            try:
                pairs = parse_qsl(body, keep_blank_values=True, strict_parsing=False)
                _body = urlencode(pairs, doseq=True)
            except Exception:
                _body = body
        else:
            _body = body
    else:
        _body = body

    # Resolve templates in body string. Dict/list bodies are walked
    # recursively by _deep_resolve after the JSON parse below.
    _body = _resolve_templates(_body)

    # -- Handle binary body (file_url / file_path → bytes) -------------------
    # Port of the V2 effective-body resolution. Handles double-json-encoded
    # body strings from the V4 authoring path (the code exporter wraps body with
    # json.dumps() before AST conversion).
    def _get_effective_body(hdrs, raw_body):
        try:
            ct = ""
            if isinstance(hdrs, dict):
                ct = hdrs.get("Content-Type") or hdrs.get("content-type") or ""
            if _is_binary_content_type(ct) and raw_body and isinstance(raw_body, str):
                data = json.loads(raw_body)
                if isinstance(data, str):
                    data = json.loads(data)
                if isinstance(data, dict):
                    if "file_url" in data:
                        file_url = data["file_url"]
                        if not file_url.startswith(("http://", "https://")):
                            file_url = "http://" + file_url
                        _log.info("[execute_api] binary body: downloading %s", file_url)
                        resp = _httpx.get(file_url, timeout=120, follow_redirects=True)
                        resp.raise_for_status()
                        return resp.content
                    elif "file_path" in data:
                        file_name = Path(data["file_path"]).name
                        downloads = os.path.expanduser("~/Downloads")
                        full_path = os.path.join(downloads, file_name)
                        _log.info("[execute_api] binary body: reading %s", full_path)
                        with open(full_path, "rb") as f:
                            return f.read()
        except Exception as e:
            _log.info("[execute_api] binary body fallback: %s", e)
        return raw_body

    _body = _get_effective_body(_headers, _body)

    # -- Parse body ----------------------------------------------------------
    if isinstance(_body, str):
        try:
            _body = json.loads(_body)
        except (json.JSONDecodeError, TypeError):
            pass  # keep as string

    # -- Resolve templates in dict/list body ---------------------------------
    # String bodies hit _resolve_templates above (line 183). Native dict/list
    # bodies (and JSON-string bodies parsed to dict/list above) are walked here
    # so that nested {{...}} / ${...} templates in every leaf string are resolved.
    # This is idempotent for string-bodied flows (templates already resolved).
    if isinstance(_body, (dict, list)):
        _body = _deep_resolve(_body)

    # -- Handle authorization ------------------------------------------------
    _auth = authorization
    if isinstance(_auth, str):
        try:
            _auth = json.loads(_auth)
        except (json.JSONDecodeError, TypeError):
            _auth = {}

    if _auth and isinstance(_auth, dict):
        auth_type = _auth.get("type", "").lower()
        auth_data = _auth.get("data", {})
        if auth_type == "bearer" and auth_data.get("token"):
            _headers["Authorization"] = f"Bearer {auth_data['token']}"
        elif auth_type == "basic" and auth_data.get("username"):
            import base64 as _b64
            cred = _b64.b64encode(
                f"{auth_data['username']}:{auth_data.get('password', '')}".encode()
            ).decode()
            _headers["Authorization"] = f"Basic {cred}"
        elif auth_type == "aws-signature":
            try:
                from botocore.awsrequest import AWSRequest
                from botocore.auth import SigV4Auth, SigV4QueryAuth
                from botocore.credentials import Credentials
                from urllib.parse import parse_qs
                region = auth_data.get("region", "us-east-1")
                session_token = auth_data.get("session_token")
                access_key = auth_data.get("access_key")
                secret_key = auth_data.get("secret_key")
                service_name = auth_data.get("service_name", "")
                aws_req = AWSRequest(
                    method=method,
                    url=url,
                    data=_body if isinstance(_body, str) else json.dumps(_body) if _body else None,
                )
                if service_name.lower() == "s3":
                    aws_req.context["payload_signing_enabled"] = False
                credentials = Credentials(access_key, secret_key, session_token)
                if auth_data.get("add_to") == "params":
                    SigV4QueryAuth(credentials, service_name, region).add_auth(aws_req)
                    sig_parsed = urlparse(aws_req.url)
                    sig_params = parse_qs(sig_parsed.query)
                    sig_params = {k: v[0] if len(v) == 1 else v for k, v in sig_params.items()}
                    _params.update(sig_params)
                else:
                    SigV4Auth(credentials, service_name, region).add_auth(aws_req)
                    _headers.update(dict(aws_req.headers))
            except Exception as e:
                _log.debug(f"AWS Signature auth failed: {e}")

    # -- Proxy ---------------------------------------------------------------
    # Resolved at call time. Env vars (TESTMU_API_PROXY_HOST/PORT) win when
    # PORT is set; else cloud default 127.0.0.1:22000 if TESTMU_RUN_TARGET=cloud;
    # else None (no proxy).
    proxy = _get_api_proxy_url()

    # -- Build request kwargs ------------------------------------------------
    # Match V2 behaviour: only json.dumps when Content-Type is
    # application/json. For form-data/urlencoded (or stripped multipart CT),
    # pass the dict directly so httpx form-encodes it.
    _method = method.upper()
    data_kwarg = None
    if _body is not None and _body != "" and _body != {}:
        if isinstance(_body, dict):
            _ct = (_headers.get("Content-Type") or _headers.get("content-type") or "").lower() if isinstance(_headers, dict) else ""
            if "application/json" in _ct:
                data_kwarg = json.dumps(_body)
            else:
                data_kwarg = _body
        else:
            data_kwarg = _body

    start = time.time()

    try:
        if _method == "GET":
            if data_kwarg is not None:
                response = _httpx.request(
                    method="GET", url=url, headers=_headers, data=data_kwarg,
                    params=_params, timeout=_timeout_sec, proxy=proxy,
                    verify=verify, follow_redirects=follow_redirects,
                )
            else:
                response = _httpx.get(
                    url, headers=_headers, params=_params, timeout=_timeout_sec,
                    proxy=proxy, verify=verify, follow_redirects=follow_redirects,
                )
        elif _method == "POST":
            response = _httpx.post(
                url, headers=_headers, data=data_kwarg, params=_params,
                timeout=_timeout_sec, proxy=proxy, verify=verify,
                follow_redirects=follow_redirects,
            )
        elif _method == "PUT":
            response = _httpx.put(
                url, headers=_headers, data=data_kwarg, params=_params,
                timeout=_timeout_sec, proxy=proxy, verify=verify,
                follow_redirects=follow_redirects,
            )
        elif _method == "DELETE":
            if data_kwarg is not None:
                response = _httpx.request(
                    method="DELETE", url=url, headers=_headers, data=data_kwarg,
                    params=_params, timeout=_timeout_sec, proxy=proxy,
                    verify=verify, follow_redirects=follow_redirects,
                )
            else:
                response = _httpx.delete(
                    url, headers=_headers, params=_params, timeout=_timeout_sec,
                    proxy=proxy, verify=verify, follow_redirects=follow_redirects,
                )
        elif _method == "PATCH":
            response = _httpx.patch(
                url, headers=_headers, data=data_kwarg, params=_params,
                timeout=_timeout_sec, proxy=proxy, verify=verify,
                follow_redirects=follow_redirects,
            )
        else:
            raise RuntimeError(f"Unsupported HTTP method: {_method!r}")
    except RuntimeError:
        raise
    except Exception as e:
        # V2 parity (V2 source execute_api): a request failure —
        # including proxy/connect stalls through the HyperExecute proxy and
        # ReadTimeout — fails OPEN, returning a soft {status:400} result so the
        # test continues and the author's own status assertion can handle it,
        # instead of hard-failing the test. Input-validation errors (invalid URL,
        # unsupported method) are raised as RuntimeError above and still propagate.
        return {"status": 400, "message": "API request failed " + str(e)}

    elapsed_ms = (time.time() - start) * 1000
    _log.info("    [execute_api] status=%d time=%.0fms", response.status_code, elapsed_ms)

    # -- Build response dict -------------------------------------------------
    resp = {
        "status": response.status_code,
        "headers": response.headers,
        "cookies": response.cookies,
        "body": response.content,
        "time": elapsed_ms,
    }

    # Normalise non-JSON-serialisable values
    for key in list(resp.keys()):
        try:
            json.dumps(resp[key])
        except (TypeError, ValueError):
            if isinstance(resp[key], bytes):
                try:
                    decoded = resp[key].decode("utf-8")
                    if not decoded:
                        resp["response_body"] = None
                        resp[key] = []
                    else:
                        try:
                            resp["response_body"] = json.loads(decoded)
                        except (TypeError, ValueError):
                            resp["response_body"] = decoded
                            resp[key] = list(decoded)
                except Exception:
                    fallback = str(resp[key])
                    if len(fallback) > 255:
                        fallback = fallback[:255] + "..."
                    resp["response_body"] = fallback
                    resp[key] = [fallback]
            else:
                resp[key] = [{k: v} for k, v in resp[key].items()]
            for i in range(len(resp[key])):
                try:
                    json.dumps(resp[key][i])
                except (TypeError, ValueError):
                    resp[key][i] = str(resp[key][i])

    # Surface the response body in the step log (parity with execute_db/js) so
    # the result is visible on the LambdaTest automation dashboard.
    _body_for_log = resp.get("response_body", resp.get("body"))
    _log.info("    [execute_api] result=%s", str(_body_for_log)[:200])

    return resp
