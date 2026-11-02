"""Loop-confined TLS resumption for async connections.

Tickets are consumed once and kept only in memory. No early data is sent.
"""

from __future__ import annotations

from collections import OrderedDict
from collections.abc import Callable
import ssl
import time
from types import MethodType
from typing import Any

Origin = tuple[str, int]
_MAX_SESSIONS = 256


def _normalize_hostname(hostname: str) -> str:
    # aiohttp removes trailing DNS dots from the TLS server hostname.
    # Normalize cache matching only; pass the original hostname to OpenSSL.
    return hostname.encode("idna").decode("ascii").lower().rstrip(".")


class _TLSResumption:
    def __init__(self, context_factory: Callable[[], ssl.SSLContext]) -> None:
        self._context_factory = context_factory
        self._contexts: dict[Origin, ssl.SSLContext] = {}
        self._sessions: OrderedDict[int, tuple[ssl.SSLContext, ssl.SSLSession]] = (
            OrderedDict()
        )
        self._next_id = 0
        self._closed = False

    def context(self, hostname: str, port: int) -> ssl.SSLContext:
        hostname = _normalize_hostname(hostname)
        origin = (hostname, port)
        if origin not in self._contexts:
            context = self._context_factory()
            context.sslobject_class = _SessionSSLObject
            # Configure only this client's context; never patch global asyncio/ssl.
            context.wrap_bio = MethodType(_wrap_bio, context)
            context._runta_tls = self
            context._runta_origin = origin
            self._contexts[origin] = context
        return self._contexts[origin]

    def _expire(self) -> None:
        now = time.time()
        for key, (_, session) in list(self._sessions.items()):
            if session.time + session.timeout <= now:
                del self._sessions[key]

    def take(self, context: ssl.SSLContext) -> ssl.SSLSession | None:
        self._expire()
        for key, (owner, session) in self._sessions.items():
            if owner is context:
                del self._sessions[key]
                return session
        return None

    def save(self, context: ssl.SSLContext, session: ssl.SSLSession) -> None:
        if self._closed:
            return
        self._expire()
        if session.time + session.timeout <= time.time():
            return
        self._next_id += 1
        self._sessions[self._next_id] = (context, session)
        while len(self._sessions) > _MAX_SESSIONS:
            self._sessions.popitem(last=False)

    def close(self) -> None:
        self._closed = True
        self._sessions.clear()
        self._contexts.clear()


def _wrap_bio(
    context: ssl.SSLContext,
    incoming: ssl.MemoryBIO,
    outgoing: ssl.MemoryBIO,
    server_side: bool = False,
    server_hostname: str | None = None,
    session: ssl.SSLSession | None = None,
) -> ssl.SSLObject:
    candidate = None
    if (
        not server_side
        and server_hostname is not None
        and _normalize_hostname(server_hostname) == context._runta_origin[0]
    ):
        candidate = context._runta_tls.take(context) if session is None else session
    try:
        obj = ssl.SSLContext.wrap_bio(
            context,
            incoming,
            outgoing,
            server_side=server_side,
            server_hostname=server_hostname,
            session=candidate,
        )
        obj._offered_session_id = candidate.id if candidate is not None else None
        return obj
    except (ValueError, ssl.SSLError):
        if candidate is None:
            raise
        # Only session attachment is retried, before handshake or HTTP bytes.
        return ssl.SSLContext.wrap_bio(
            context,
            incoming,
            outgoing,
            server_side=server_side,
            server_hostname=server_hostname,
        )


class _SessionSSLObject(ssl.SSLObject):
    _saved = False
    _offered_session_id: bytes | None = None

    def _save_session(self) -> None:
        if self._saved:
            return
        version = self.version()
        if version is None:
            return
        session = self.session
        if version == "TLSv1.3" and (
            not session.has_ticket or session.id == self._offered_session_id
        ):
            # The offered ticket must not be cached again after resumption.
            return
        if not session.has_ticket and not session.id:
            return
        self.context._runta_tls.save(self.context, session)
        self._saved = True

    def do_handshake(self) -> None:
        super().do_handshake()
        self._save_session()

    def read(self, len: int = 1024, buffer: Any = None) -> Any:
        try:
            result = super().read(len, buffer)
        except (ssl.SSLWantReadError, ssl.SSLWantWriteError):
            # A read may consume a post-handshake ticket without returning data.
            self._save_session()
            raise
        self._save_session()
        return result
