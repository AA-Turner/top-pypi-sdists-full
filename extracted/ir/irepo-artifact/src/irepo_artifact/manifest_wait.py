"""Per-Job manifest budget; archive and file transfers keep their existing timeout."""
from functools import partial
from email.utils import parsedate_to_datetime
import http.client
import io
import math
import time
import urllib.request

from .errors import DownloadError


class ManifestBudget:
    def __init__(self, seconds):
        self.deadline = time.monotonic() + seconds

    def remaining(self):
        remaining = self.deadline - time.monotonic()
        if remaining <= 0:
            raise DownloadError('artifact manifest wait timed out')
        return remaining

    def sleep(self, seconds):
        time.sleep(min(seconds, self.remaining()))
        self.remaining()


def retry_delay(headers, default):
    try:
        delay = float(headers.get('Retry-After', default))
    except (ValueError, TypeError):
        return default
    return delay if math.isfinite(delay) and delay > 0 else default


def http_retry_delay(headers, failures):
    """AP v1.3 HTTP backoff; distinct from 202 preparation polling."""
    delay = min(.5 * 2 ** failures, 2.0)
    value = headers.get('Retry-After')
    if value is None or not value.strip():
        return delay
    try:
        server_delay = max(0.0, float(value))
    except ValueError:
        try:
            server_delay = max(0.0, parsedate_to_datetime(value).timestamp() - time.time())
        except (TypeError, ValueError, OverflowError):
            return delay
    return max(delay, server_delay)


class _BudgetReader(io.RawIOBase):
    def __init__(self, raw, sock, budget, timeout):
        self._raw = raw
        self._budget = budget
        self._socket = sock
        self._timeout = timeout

    def readable(self):
        return True

    def readinto(self, buffer):
        # Apply the remaining budget to every underlying socket read, including
        # HTTP status/headers and chunk framing, not just response body chunks.
        self._socket.settimeout(min(self._timeout, self._budget.remaining()))
        count = self._raw.readinto(buffer)
        self._budget.remaining()
        return count

    def close(self):
        try:
            self._raw.close()
        finally:
            super().close()


class _BudgetResponse(http.client.HTTPResponse):
    def __init__(self, sock, *args, budget, timeout, **kwargs):
        super().__init__(sock, *args, **kwargs)
        raw = self.fp.detach()
        self.fp = io.BufferedReader(_BudgetReader(raw, sock, budget, timeout))


def budget_handlers(budget, timeout):
    def connection(cls, host, **kwargs):
        conn = cls(host, **kwargs)
        conn.response_class = partial(_BudgetResponse, budget=budget, timeout=timeout)
        return conn

    class HTTPHandler(urllib.request.HTTPHandler):
        def http_open(self, req):
            return self.do_open(partial(connection, http.client.HTTPConnection), req)

    class HTTPSHandler(urllib.request.HTTPSHandler):
        def https_open(self, req):
            return self.do_open(partial(connection, http.client.HTTPSConnection), req,
                                context=self._context)

    return HTTPHandler(), HTTPSHandler()
