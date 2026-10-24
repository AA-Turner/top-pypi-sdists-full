"""API step lines for the run log. On HyperExecute the run log is the test's terminal log.

A call answered with a 2xx/3xx is one line. Anything else also prints what was sent:
the values used, each header with where it came from, the body, and the timing.
Secrets never print: a field authored with {{secrets.*}} / {{totp.*}} shows as authored,
credential headers and the variables behind them are masked, and any value resolved from a
secret is cut out wherever it ends up (see _vars._mark_secret).
"""

import importlib
import json
import logging
import os
import re
import socket
import ssl
from http import HTTPStatus

import httpx

# The same file ships in each Python binding; only these two names differ.
_LOGGER = "testmu_selenium"
_VARS = "testmu_selenium._vars"

_log = logging.getLogger(_LOGGER)

_SECRET_RE = re.compile(r"\{\{\s*(?:secrets|totp)\.")
_TOKEN_RE = re.compile(r"\{\{([^{}]+)\}\}|\$\{([^{}]+)\}")
_MASKED_HEADERS = {"authorization", "proxy-authorization", "cookie", "set-cookie", "x-api-key", "x-amz-security-token"}
# only these keep their scheme word; anything else could be part of the credential
_SCHEMES = {"bearer", "basic", "digest", "token", "negotiate", "ntlm", "oauth", "aws4-hmac-sha256"}
_MASK = "********"
_BODY_CAP = 2000
_PHASES = (("prepare", "preparing"), ("wait", "connect + waiting"), ("download", "download"))
_STAGES = {"dns": "DNS lookup", "connect": "connecting", "tls": "the TLS handshake",
           "wait": "waiting for the response", "download": "downloading the response"}

_ERRORS = {"dns": "host not found", "connect": "could not connect", "tls": "TLS handshake failed",
           "timeout": "timed out", "connect_timeout": "timed out", "proxy": "the proxy could not reach the server",
           "protocol": "the server closed the connection"}


def _text(value):
    if value is None or isinstance(value, str):
        return value or ""
    if isinstance(value, (bytes, bytearray)):
        return f"<binary, {_size(len(value))}>"
    try:
        return json.dumps(value, default=str)
    except (TypeError, ValueError):
        return str(value)


def has_secret(value):
    return bool(_SECRET_RE.search(_text(value)))


def _size(n):
    return f"{n} B" if n < 1024 else f"{n / 1024:.1f} KB" if n < 1048576 else f"{n / 1048576:.1f} MB"


def _ms(value):
    return f"{value:.0f} ms" if isinstance(value, (int, float)) else "?"


def _authored_headers(headers):
    if isinstance(headers, str):
        try:
            headers = json.loads(headers)
        except (TypeError, ValueError):
            return {}
    return {str(k).lower(): v for k, v in headers.items()} if isinstance(headers, dict) else {}


def _header_value(name, value, authored):
    """What a header line may show: credentials masked, secret-authored values shown as authored."""
    key = name.lower()
    if key in _MASKED_HEADERS:
        scheme, _, rest = str(value).partition(" ")
        keep = key in ("authorization", "proxy-authorization") and rest and scheme.lower() in _SCHEMES
        return f"{scheme} {_MASK}" if keep else _MASK
    if has_secret(authored.get(key)):
        return _text(authored[key])
    return str(value)


def _source(name, authored, auth_keys):
    key = name.lower()
    if key in auth_keys:
        return "from Authorization"
    if key in authored:
        return "typed"
    return "added by KaneAI"


def _token(match):
    mustache, dollar = match.group(1), match.group(2)
    name = (mustache or dollar).strip()
    return name, (f"{{{{{name}}}}}" if mustache else f"${{{name}}}")


def _tokens(fields):
    return {_token(m)[1] for m in _TOKEN_RE.finditer(" ".join(_text(f) for f in fields))}


def _scrub(text):
    """Cut every value resolved from {{secrets.*}} / {{totp.*}} out of a log line."""
    for secret in sorted(importlib.import_module(_VARS)._SECRET_VALUES, key=len, reverse=True):
        text = text.replace(secret, _MASK)
    return text


def _values(fields, hidden):
    """Each {{name}} / ${name} in the authored request and the value it had.

    ``hidden``: tokens behind a masked header or the Authorization tab; their values never print."""
    _vars = importlib.import_module(_VARS)
    rows, seen = [], set()
    for match in _TOKEN_RE.finditer(" ".join(_text(f) for f in fields)):
        name, token = _token(match)
        if token in seen:
            continue
        seen.add(token)
        kind = name.split(".")[0] if match.group(1) and "." in name else "variable"
        if kind in ("secrets", "totp") or token in hidden:
            rows.append(f"{token} = {_MASK} ({kind}, hidden)")
            continue
        if kind == "smart":
            rows.append(f"{token} (smart, generated per call)")
            continue
        try:
            # not var(): in some bindings it logs the value it resolves
            if match.group(1):
                value = _vars._resolve_single(name)
            elif hasattr(_vars, "_dollar_lookup"):
                value = _vars._dollar_lookup(match.group(2))
            else:
                value = _vars.var(match.group(0))
            if value is getattr(_vars, "_SENTINEL", None):  # plain names live in the store there
                value = _vars.var(match.group(0))
        except Exception:  # an unresolvable name reads as empty, as the request saw it
            value = ""
        shown = _text(value)
        # some bindings hand an unresolved token back as-is, and send it that way
        rows.append(f"{token} = <no value> ({kind}, empty variable)" if shown in ("", match.group(0)) else
                    f"{token} = {shown[:200]} ({kind})")
    return rows


def _error_kind(exc):
    if isinstance(exc, httpx.ProxyError):
        return "proxy"
    if isinstance(exc, httpx.ConnectTimeout):
        return "connect_timeout"
    if isinstance(exc, httpx.TimeoutException):
        return "timeout"
    if isinstance(exc, httpx.ConnectError):
        # the cause, not the OS's wording: httpx chains the socket/ssl error it got
        cause = exc.__cause__ or exc.__context__
        for _ in range(5):
            if cause is None:
                break
            if isinstance(cause, socket.gaierror):
                return "dns"
            if isinstance(cause, ssl.SSLError):
                return "tls"
            cause = cause.__cause__ or cause.__context__
        return "connect"
    if isinstance(exc, httpx.RemoteProtocolError):
        return "protocol"
    return "other"


def _error_reason(error, capture):
    if str(error).startswith("Invalid URL"):
        return "the URL has no host, so nothing was sent (check the variables it uses)"
    kind = ((capture or {}).get("error") or {}).get("kind") or _error_kind(error)
    return _ERRORS.get(kind, _scrub(str(error))[:300] or type(error).__name__)


def _enabled():
    """TESTMU_API_LOG=0 turns API step logging off (auteur sets it)."""
    return os.getenv("TESTMU_API_LOG") != "0"


def _sent_url(url, params):
    """The URL with its query, merged the way httpx merges it when sending."""
    if not params:
        return str(url)
    try:
        import httpx
        return str(httpx.URL(str(url)).copy_merge_params(params))
    except Exception:  # params httpx would not take: the bare URL still says where it went
        return str(url)


def _response_lines(response, emit):
    """The server's headers and body (httpx response), for every answered call."""
    if response is None:
        return
    for name, value in response.headers.multi_items():
        emit("      header  %s: %s", name, _MASK if name.lower() in _MASKED_HEADERS else _scrub(value))
    try:
        text = _scrub(response.content.decode("utf-8"))
    except UnicodeDecodeError:  # text in another charset, or an image / file download
        is_text = response.headers.get("content-type", "").lower().startswith("text/")
        text = _scrub(response.text) if is_text else f"<binary, {_size(len(response.content))}>"
    if text:
        emit("      body    %s (%s)", text[:_BODY_CAP] + ("…" if len(text) > _BODY_CAP else ""), _size(len(response.content)))


def log_api_call(method, url, *, authored, sent_headers, body, auth_keys, elapsed_ms, params=None,
                 status=None, reason="", size=0, message="", error=None, capture=None, response=None):
    """Log one API step: the response whenever it was answered, the full request too when >= 400.

    ``response`` (httpx) adds the response headers and body, for every answered call.
    """
    if not _enabled():
        return
    try:
        if status is not None and not reason:
            try:
                reason = HTTPStatus(int(status)).phrase
            except ValueError:
                reason = ""
        failed = status is None or status >= 400
        shown_url = _scrub(_text(authored.get("url")) if has_secret(authored.get("url")) or has_secret(authored.get("params")) else _sent_url(url, params))
        headers_authored = _authored_headers(authored.get("headers"))
        headers = [{"name": name, "value": _scrub(_header_value(name, value, headers_authored)),
                    "source": _source(name, headers_authored, auth_keys)}
                   for name, value in (capture or {}).get("headers") or list((sent_headers or {}).items())]
        sent_body = (capture or {}).get("body") if capture else _text(body)
        shown_body = _scrub((_text(authored.get("body")) if has_secret(authored.get("body")) else sent_body) or "")
        timing = (capture or {}).get("timing") or {}
        keys = [key for key, _ in _PHASES]
        last = keys.index(timing["failed_at"]) if timing.get("failed_at") in keys else len(keys) - 1
        phases = {key: timing[key] for key, _ in _PHASES[:last + 1] if timing.get(key) is not None}
        stage = _STAGES.get(timing.get("failed_at"))
        error_text = ""
        if status is None:
            error_text = (f"No response: {_error_reason(error, capture)}" + (f", stopped at {stage}" if stage else "")
                          + (f" after {_ms(elapsed_ms)}" if elapsed_ms else ""))
        message = _scrub(str(message))[:500] if message else ""
        hidden = _tokens([v for k, v in headers_authored.items() if k in _MASKED_HEADERS] + [authored.get("authorization")])
        values = [_scrub(row) for row in _values([authored.get("url"), authored.get("params"), authored.get("headers"),
                                                  authored.get("body"), authored.get("authorization")], hidden)] if failed else []
        shown_body = shown_body[:_BODY_CAP] + ("…" if len(shown_body) > _BODY_CAP else "")
        body_size = _size(len(sent_body.encode("utf-8"))) if sent_body else ""

        if not failed:
            hops = len((capture or {}).get("redirects") or []) - 1  # the list ends with the final response
            _log.info("    [API RESPONSE] %s %s  %s %s in %s, %s%s", method, shown_url, status, reason,
                      _ms(elapsed_ms), _size(size), f", {hops} redirect{'s' if hops > 1 else ''}" if hops > 0 else "")
            _response_lines(response, _log.info)
        else:
            _log.info("    [API REQUEST] %s %s", method, shown_url)
            for row in values:
                _log.info("      value   %s", row)
            for header in headers:
                _log.info("      header  %s: %s (%s)", header["name"], header["value"], header["source"])
            if sent_body:
                _log.info("      body    %s (%s)", shown_body, body_size)
            if status is not None:
                _log.error("    [API RESPONSE] %s %s in %s, %s", status, reason, _ms(elapsed_ms), _size(size))
                if message:
                    _log.error("      message %s", message)
                _response_lines(response, _log.error)
            else:
                _log.error("    [API ERROR] %s", error_text)
            if phases:
                note = " (measured to the proxy)" if ((capture or {}).get("network") or {}).get("proxy") else ""
                labels = dict(_PHASES)
                _log.info("      timing  %s%s", ", ".join(f"{labels[k]} {_ms(v)}" for k, v in phases.items()), note)
    except Exception as exc:  # logging must never fail the step
        _log.debug("API step log failed: %s", exc)
    if error is not None:
        error._api_logged = True


def log_not_sent(method, url, error):
    """A call that failed before anything was logged for it, e.g. a variable that could not be resolved."""
    if not _enabled():
        return
    if getattr(error, "_api_logged", False) or getattr(error.__cause__, "_api_logged", False):
        return
    shown_url = _scrub(_text(url) if has_secret(url) else str(url))
    reason = f"Not sent: {_scrub(str(error))[:500]}"
    _log.error("    [API ERROR] %s %s  %s", str(method).upper(), shown_url, reason)
