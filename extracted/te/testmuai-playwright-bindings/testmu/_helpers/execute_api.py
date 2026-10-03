"""execute_api helper — makes HTTP API requests, optionally via HyperExecute proxy.

Variable resolution: {{var}} templates in URL, headers, body, and params are
resolved via testmu._vars.var() before the request is made.

Proxy routing: when running on HyperExecute (run_target == "cloud"),
routes all requests through the local proxy at 127.0.0.1:22000. On local
run target, makes direct requests.

Raises RuntimeError on bad/unsupported input (invalid URL, unsupported method).
When kane_version=="v3", a request failure (network error, proxy/connect
stall, or timeout) fails OPEN with a soft {"status": 400, "message": ...} dict
(parity with the existing runtime behavior); otherwise it stays fail-closed and
raises RuntimeError. A successful request returns the response dict directly.
"""
import asyncio
import json
import logging
import os
import time
from pathlib import Path
from urllib.parse import urlparse, parse_qsl, quote, unquote, urlencode

_log = logging.getLogger("testmu")

# Binding-internal record of agent/test-executed API calls. Read by
# api_calls_query in exported-test runtime (mirrors how devtools capture is
# binding-internal). Requests are stored AS RECEIVED — templates unresolved.
_api_call_log: list = []
_API_BODY_CAP = 65536
# Entry-count cap (parity with devtools_network's _MAX_NETWORK_ENTRIES): evict
# the oldest 10% when the log fills, so a long-running session can't grow it
# without bound.
_MAX_API_CALLS_ENTRIES = 5000


def _deep_unwrap_json(node):
    """Recursively parse JSON that arrived as a string inside a JSON payload.

    V2: APIs routinely return a field whose value is itself a
    serialised JSON object (``{"data": "{\"id\": 7}"}``). Only the top level
    was parsed, so the nested value stayed a string and could not be addressed
    as ``data.id`` when saving it to a variable. Anything that does not look
    like JSON, or fails to parse, is returned unchanged.
    """
    if isinstance(node, dict):
        return {k: _deep_unwrap_json(v) for k, v in node.items()}
    if isinstance(node, list):
        return [_deep_unwrap_json(v) for v in node]
    if isinstance(node, str):
        s = node.strip()
        if s and s[0] in "{[":
            try:
                return _deep_unwrap_json(json.loads(s))
            except (ValueError, TypeError):
                return node
    return node


def get_api_call_log() -> list:
    return list(_api_call_log)


def clear_api_call_log() -> None:
    _api_call_log.clear()


def _record_api_call(method, url, headers, body, params, authorization,
                     timeout, verify, resp) -> None:
    from testmu._helpers.devtools_types import ApiCallEntry
    response = dict(resp) if isinstance(resp, dict) else {"value": resp}
    response.pop("body", None)  # bytes/raw — full body never enters the log
    rb = response.get("response_body")
    if isinstance(rb, str) and len(rb) > _API_BODY_CAP:
        response["response_body"] = rb[:_API_BODY_CAP]
    if len(_api_call_log) >= _MAX_API_CALLS_ENTRIES:
        del _api_call_log[:_MAX_API_CALLS_ENTRIES // 10]
    _api_call_log.append(ApiCallEntry(
        sequence=len(_api_call_log) + 1,
        request={"method": method, "url": url, "headers": headers,
                 "params": params, "body": body,
                 "authorization": authorization, "timeout": timeout,
                 "verify": verify},
        response=response,
    ))


_BINARY_CONTENT_TYPES = {
    "application/octet-stream",
    "application/pdf",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}


def _is_binary_content_type(content_type: str) -> bool:
    """Binary content-type detection — exact set plus
    image/*, audio/*, video/*, text/* prefixes."""
    ct = (content_type or "").lower().strip()
    return (ct in _BINARY_CONTENT_TYPES
            or ct.startswith(("image/", "audio/", "video/", "text/")))


def _resolve_templates(value):
    """Resolve {{var}} templates in a string value using testmu._vars.var()."""
    if not isinstance(value, str):
        return value
    from testmu._vars import var
    return var(value)


def _deep_resolve(value):
    """Recursively resolve {{var}} / ${var} templates in every string within a dict or list.

    Walks nested dicts and lists so that templates at any depth are substituted.
    Non-string leaf values are returned unchanged (type-preserving).
    """
    if isinstance(value, dict):
        return {k: _deep_resolve(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_deep_resolve(item) for item in value]
    return _resolve_templates(value)



def _do_request(method, url, headers, body, params, authorization, timeout, verify, settings):
    """Synchronous inner function executed via asyncio.to_thread."""
    import httpx as _httpx
    from testmu import _config

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

    # httpx >= 0.28 treats an EMPTY params dict as "replace the query
    # string", so passing {} strips a ?key=value the caller baked into the URL
    # (reported as an API returning 401 instead of 302). None means "leave the
    # URL alone". pyproject allows httpx>=0.27.0, so both behaviours are in range
    # — normalise the empty case to None rather than pinning the dependency.
    _params = params or None
    if isinstance(_params, str):
        try:
            _params = json.loads(_params)
        except (json.JSONDecodeError, TypeError):
            _params = None
    _params = _deep_resolve(_params) if _params else None
    if not _params:
        _params = None

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
    # V2: a multipart request needs a real multipart body, and the
    # boundary must come from the client — so record multipart-ness, then drop the
    # authored Content-Type. Matched by prefix: authored headers usually carry
    # `; boundary=...`, which an exact comparison missed entirely.
    _is_multipart = False
    if isinstance(_headers, dict):
        _is_multipart = any(
            str(k).lower() == "content-type"
            and str(v).lower().startswith("multipart/form-data")
            for k, v in _headers.items()
        )
        _headers = {
            k: v for k, v in _headers.items()
            if not (str(k).lower() == "content-type" and _is_multipart)
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

    # Resolve templates in body string. Dict/list bodies are walked
    # recursively by _deep_resolve after the JSON parse below.
    #
    # This MUST run before the urlencoded re-encode below. The old
    # order re-encoded first, which percent-encoded the template's own braces
    # ("phone={{phone}}" -> "phone=%7B%7Bphone%7D%7D") so the resolver could
    # never match them and the literal encoded braces went to the API.
    _body = _resolve_templates(body)

    # -- Handle URL-encoded body ---------------------------------------------
    if isinstance(_headers, dict):
        ct = _headers.get("Content-Type") or _headers.get("content-type") or ""
        if str(ct).lower() == "application/x-www-form-urlencoded" and _body and isinstance(_body, str):
            _body = _reencode_urlencoded_body(_body)

    # -- Handle binary body (file_url / file_path → bytes) -------------------
    # Effective-body resolution. Handles double-json-encoded
    # body strings from the generated test path (the code exporter wraps body with
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

    # Resolve any remaining {{var}} / ${var} templates in parsed dict/list bodies.
    # String bodies are already resolved above by _resolve_templates; dict/list
    # bodies passed directly (or obtained via JSON parse) are resolved here.
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
    proxy = _config.get_api_proxy_url()

    # -- Build request kwargs ------------------------------------------------
    # Match existing behavior: only json.dumps when Content-Type is
    # application/json. For form-data/urlencoded, pass the dict directly so
    # httpx form-encodes it. A multipart dict body goes out as files= below.
    _method = method.upper()
    data_kwarg = None
    files_kwarg = None
    if _is_multipart and isinstance(_body, dict) and _body:
        # Stripping the Content-Type alone left httpx form-URL-encoding the dict,
        # so a multipart API received application/x-www-form-urlencoded. files=
        # with (None, value) tuples sends real multipart/form-data fields.
        # V2: httpx calls .read() on anything that is not str or
        # bytes, so values substituted from earlier captures (ints, dicts) must be
        # coerced to text first or the request crashes before it is sent.
        files_kwarg = {
            k: (None, v if isinstance(v, (str, bytes))
                else json.dumps(v) if isinstance(v, (dict, list))
                else str(v))
            for k, v in _body.items()
        }
    elif _body is not None and _body != "" and _body != {}:
        if isinstance(_body, dict):
            _ct = (_headers.get("Content-Type") or _headers.get("content-type") or "").lower() if isinstance(_headers, dict) else ""
            if "application/json" in _ct:
                data_kwarg = json.dumps(_body)
            else:
                data_kwarg = _body
        elif isinstance(_body, list):
            data_kwarg = json.dumps(_body)
        else:
            data_kwarg = _body

    start = time.time()

    # V2: name the cause when the server was never reached.
    # Scoped to proxy/connect only — other failures keep the existing handling.
    try:
        if _method == "GET":
            if data_kwarg is not None or files_kwarg:
                response = _httpx.request(
                    method="GET", url=url, headers=_headers, data=data_kwarg, files=files_kwarg,
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
                url, headers=_headers, data=data_kwarg, files=files_kwarg, params=_params,
                timeout=_timeout_sec, proxy=proxy, verify=verify,
                follow_redirects=follow_redirects,
            )
        elif _method == "PUT":
            response = _httpx.put(
                url, headers=_headers, data=data_kwarg, files=files_kwarg, params=_params,
                timeout=_timeout_sec, proxy=proxy, verify=verify,
                follow_redirects=follow_redirects,
            )
        elif _method == "DELETE":
            if data_kwarg is not None or files_kwarg:
                response = _httpx.request(
                    method="DELETE", url=url, headers=_headers, data=data_kwarg, files=files_kwarg,
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
                url, headers=_headers, data=data_kwarg, files=files_kwarg, params=_params,
                timeout=_timeout_sec, proxy=proxy, verify=verify,
                follow_redirects=follow_redirects,
            )
        else:
            raise RuntimeError(f"Unsupported HTTP method: {_method!r}")
    except _httpx.ProxyError as e:
        raise _httpx.ProxyError(
            f"API request failed — proxy could not reach the server: {e}"
        ) from e
    except _httpx.ConnectError as e:
        raise _httpx.ConnectError(
            f"API request failed — could not connect to the server: {e}"
        ) from e

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

    if isinstance(settings, dict) and settings.get("normalization", False):
        for key in ("headers", "cookies"):
            folded = {}
            for k, v in resp[key].items():
                fk = str(k).lower()
                folded[fk] = f"{folded[fk]}, {v}" if fk in folded else v
            resp[key] = folded
        for _gh in ("content-type", "cache-control", "x-request-id", "x-ratelimit-remaining"):
            resp["headers"].setdefault(_gh, "")
        body = resp["body"]
        if isinstance(body, bytes):
            try:
                decoded = body.decode("utf-8")
                if not decoded:
                    resp["body"] = None
                    resp["response_body"] = None
                else:
                    try:
                        parsed = json.loads(decoded)
                        if _settings.get("enable_json_splitter", False):
                            parsed = _deep_unwrap_json(parsed)
                    except (TypeError, ValueError):
                        parsed = decoded
                    resp["body"] = parsed
                    resp["response_body"] = parsed
            except Exception:
                fallback = str(body)
                if len(fallback) > 255:
                    fallback = fallback[:255] + "..."
                resp["body"] = fallback
                resp["response_body"] = fallback
        return resp

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
                            _parsed = json.loads(decoded)
                            # V2: opt-in, as in V2 — the author enables
                            # the JSON splitter per API step.
                            if _settings.get("enable_json_splitter", False):
                                _parsed = _deep_unwrap_json(_parsed)
                            resp["response_body"] = _parsed
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

    return resp



def _reencode_urlencoded_body(body: str) -> str:
    """Normalise an ``application/x-www-form-urlencoded`` body, keeping a literal ``+``.

    the previous implementation round-tripped through
    ``parse_qsl``/``urlencode``, which is *plus-decoding* — an unencoded ``+``
    is read as a space. That is correct for a hand-authored body, but wrong for
    a value that arrived from variable resolution: ``{{phone}}`` holding an
    E.164 number resolves to ``+919876543210`` and the ``+`` is data, not a
    space. The number reached the API with a leading space instead.

    So decoding uses ``unquote`` (percent-decoding only, ``+`` left alone) and
    encoding uses ``quote`` (which escapes ``+`` to ``%2B``). The deliberate
    trade-off: a hand-authored ``a+b`` meaning "a b" now travels as a literal
    ``a+b``. Values come from variables far more often than bodies rely on
    ``+``-as-space, and a corrupted phone number is a silent data bug while
    a literal ``+`` is visible.

    Malformed input is returned unchanged rather than raising — an API step must
    not die in the encoder.
    """
    try:
        out_pairs = []
        for pair in body.split("&"):
            if not pair:
                continue
            key, sep, value = pair.partition("=")
            key = quote(unquote(key), safe="")
            if sep:
                out_pairs.append(f"{key}={quote(unquote(value), safe='')}")
            else:
                out_pairs.append(key)
        return "&".join(out_pairs)
    except Exception:  # noqa: BLE001 — never fail a request in the encoder
        return body

async def execute_api(
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
    """Execute an HTTP API request.

    Routes through the HyperExecute proxy (127.0.0.1:22000) when
    run_target == "cloud"; makes direct requests on local runs.

    Variable templates ({{var}}) in url, headers, body, and params are resolved
    via testmu._vars.var() before the request is made.

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
        When kane_version=="v3", a request failure (network error, proxy/connect
        stall, or timeout) fails OPEN with a soft {"status": 400, "message": "API
        request failed ..."} dict (parity with the existing runtime behavior) so the
        test continues.

    Raises:
        RuntimeError: On invalid URL or unsupported method (input validation), or —
            on the default path only — any request failure (fail-closed contract).
    """
    _log.info("    [execute_api] %s %s", method, url[:80])
    try:
        resp = await asyncio.to_thread(
            _do_request, method, url, headers, body, params,
            authorization, timeout, verify, settings,
        )
        try:
            _record_api_call(method, url, headers, body, params,
                             authorization, timeout, verify, resp)
        except Exception:
            pass  # recording must never fail the call
        return resp
    except RuntimeError:
        raise
    except Exception as e:
        from testmu import _configure
        if _configure.get("kane_version", "v4") == "v3":
            import httpx as _httpx
            # V2: proxy and connect failures mean the server was
            # never reached, so there is no response for a status assertion to
            # judge — V2 fails the step with a message naming the cause.
            if isinstance(e, (_httpx.ProxyError, _httpx.ConnectError)):
                raise
            # Any OTHER request failure (e.g. ReadTimeout) fails OPEN, returning a
            # soft {status:400} result so the test continues and the author's own
            # status assertion can handle it. Input-validation errors (invalid URL,
            # unsupported method) are raised as RuntimeError above and still
            # propagate.
            return {"status": 400, "message": "API request failed " + str(e)}
        # The default path keeps the fail-closed contract — unchanged.
        raise RuntimeError(f"execute_api failed: {e}") from e
