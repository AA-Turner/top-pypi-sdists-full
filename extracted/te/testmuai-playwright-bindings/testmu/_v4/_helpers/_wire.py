"""Wire capture for execute_api (KaneAI API console).

Records what an API request actually sent: the request as it went out, redirects and timing, from
httpx's own objects and event hooks (no httpx internals). execute_api returns it as `request_sent`
with secrets scrubbed; auteur's set_var keeps it for the API console, the binding's set_var drops it.
auteur's utils/api_capture.py carries the same logic.
"""
import socket
import ssl
import time

import httpx

# where a transport error stopped, by its kind; anything else stopped while waiting
_FAILED_AT = {"dns": "dns", "connect": "connect", "connect_timeout": "connect", "proxy": "connect", "tls": "tls"}


def _ms(start, end):
    return round(max(end - start, 0.0) * 1000, 1)


def _wire_request(req):
    try:
        content = req.read()
        body = content.decode("utf-8") if content else None
    except UnicodeDecodeError:
        body = f"<binary {len(content)} bytes>"
    except Exception:  # body stream can't be replayed
        body = None
    headers = [[k.decode("latin-1"), v.decode("latin-1")] for k, v in req.headers.raw]
    return {"method": req.method, "url": str(req.url), "headers": headers, "body": body}


def _redirects(response):
    if not response.history:
        return []
    return [{"code": r.status_code, "text": r.reason_phrase, "method": r.request.method,
             "url": str(r.request.url), "location": r.headers.get("location") if r.is_redirect else None,
             "ms": round(r.elapsed.total_seconds() * 1000, 1)}
            for r in [*response.history, response]]


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


class WireCapture:
    """Times one request through httpx event hooks; attach() it to the httpx client that sends it."""

    def __init__(self, proxy=None):
        self.proxy = proxy
        self.started = time.perf_counter()
        self.sent_at = self.headers_at = None

    def attach(self, client):
        client.event_hooks = {"request": [*client.event_hooks["request"], self._on_request],
                              "response": [*client.event_hooks["response"], self._on_response]}

    def _on_request(self, request):
        self.sent_at = self.sent_at or time.perf_counter()
        self.headers_at = None  # a redirect hop is waiting again

    def _on_response(self, response):
        self.headers_at = time.perf_counter()

    def _timing(self, now, exc):
        failed_at = None
        if isinstance(exc, httpx.TransportError):
            failed_at = "download" if self.headers_at else _FAILED_AT.get(_error_kind(exc), "wait")
        return {"total_ms": _ms(self.started, now),
                "prepare": _ms(self.started, self.sent_at or now),
                "wait": _ms(self.sent_at, self.headers_at or now) if self.sent_at else None,  # connect + TLS + server
                "download": _ms(self.headers_at, now) if self.headers_at else None,
                "failed_at": failed_at}

    def build(self, response=None, exc=None, method=None, url=None):
        """The capture dict, or None — building it must never break the request."""
        try:
            now = time.perf_counter()
            if response is not None:
                req = response.history[0].request if response.history else response.request
            else:
                try:
                    req = exc.request
                except Exception:  # not an httpx error, or no request attached
                    req = None
            wire = _wire_request(req) if req is not None else {"method": method, "url": str(url), "headers": [], "body": None}
            return {**wire, "redirects": _redirects(response) if response is not None else [],
                    "timing": self._timing(now, exc), "network": {"proxy": self.proxy},
                    "error": {"kind": _error_kind(exc), "message": str(exc)[:500]} if exc else None}
        except Exception:  # capture must never break the request
            return None


def api_send(method, url, *, proxy=None, verify=False, follow_redirects=True, timeout=None, **kwargs):
    """httpx request that attaches `.api_capture` to the response, or to the exception it raises."""
    wire = WireCapture(proxy)
    try:
        with httpx.Client(proxy=proxy, verify=verify, follow_redirects=follow_redirects, timeout=timeout) as client:
            wire.attach(client)
            response = client.request(method, url, **kwargs)
        response.api_capture = wire.build(response)
        return response
    except Exception as exc:
        exc.api_capture = wire.build(exc=exc, method=method, url=url)
        raise
