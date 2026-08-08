"""``AgentDaemonClient`` — one aiohttp session per agent VM.

Owns the request envelope (request id, deadline, idempotency key, trace
context), maps wire ``RpcError`` bodies and transport failures onto the
caller-facing exception taxonomy, and applies retry-once for safe resends.

Safe resend rule (fixes the git_ops blind-resend flaw): a request is retried
after a transport error ONLY if it is a GET or carries an idempotency key. The
daemon caches completed results per idempotency key, so retry-once is
exactly-once. A submitted non-idempotent op is never silently re-run.
"""

from __future__ import annotations

import logging
import uuid
from typing import TypeVar

import aiohttp
from opentelemetry import propagate
from pydantic import BaseModel

from plato.rpc.errors import (
    AgentAuthError,
    AgentUnreachableError,
    RpcError,
    RpcException,
    RpcTransportError,
    VMReclaimedError,
)
from plato.rpc.protocol import (
    API_PREFIX,
    HEADER_DEADLINE,
    HEADER_DEDUPED,
    HEADER_IDEMPOTENCY_KEY,
    HEADER_REQUEST_ID,
)

_RespT = TypeVar("_RespT", bound=BaseModel)

# Extra wall-clock the client waits beyond the server deadline before giving up
# on the socket, so the server's own DEADLINE_EXCEEDED wins the race and the
# caller gets a typed error instead of a transport timeout.
logger = logging.getLogger(__name__)

_CLIENT_TIMEOUT_GRACE_S = 10.0

# Transport-level failures that mean "the request or response was lost in
# flight" — retried once iff an idempotency key makes the resend safe.
# ClientPayloadError is the daemon dying MID-RESPONSE (truncated body, e.g.
# OOM-killed after headers were flushed): same recovery semantics as a dropped
# connection, and historically the most common real-world transport death.
_TRANSPORT_EXCS = (aiohttp.ClientConnectionError, aiohttp.ClientPayloadError, TimeoutError)


class AgentDaemonClient:
    """Typed HTTP/WS client for one agent daemon. Construct via the manager so
    connections are cached per host."""

    def __init__(self, hostname: str, token: str, *, port: int, base_url: str | None = None) -> None:
        self.hostname = hostname
        self._token = token
        self._base_url = base_url or f"http://{hostname}:{port}"
        self._session: aiohttp.ClientSession | None = None

    @property
    def base_url(self) -> str:
        return self._base_url

    def _ensure_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                base_url=self._base_url,
                headers={"Authorization": f"Bearer {self._token}"},
            )
        return self._session

    async def close(self) -> None:
        if self._session is not None and not self._session.closed:
            await self._session.close()
        self._session = None

    def _envelope_headers(self, *, deadline_s: float | None, idempotency_key: str | None) -> dict[str, str]:
        headers = {HEADER_REQUEST_ID: uuid.uuid4().hex}
        if deadline_s is not None:
            headers[HEADER_DEADLINE] = str(deadline_s)
        if idempotency_key is not None:
            headers[HEADER_IDEMPOTENCY_KEY] = idempotency_key
        propagate.inject(headers)  # W3C traceparent for cross-VM span linkage
        return headers

    async def post(
        self,
        op_path: str,
        body: BaseModel,
        response_model: type[_RespT],
        *,
        deadline_s: float | None = None,
        idempotency_key: str | None = None,
    ) -> _RespT:
        """POST a pydantic body to /v1/<op_path>, return a typed response.

        Retries once on transport failure iff an idempotency key is present.
        """
        return await self._request(
            "POST",
            f"{API_PREFIX}/{op_path}",
            response_model,
            json_body=body.model_dump(mode="json"),
            deadline_s=deadline_s,
            idempotency_key=idempotency_key,
            safe_resend=idempotency_key is not None,
        )

    async def get(
        self,
        op_path: str,
        response_model: type[_RespT],
        *,
        params: dict[str, str] | None = None,
        deadline_s: float | None = None,
    ) -> _RespT:
        """GET /v1/<op_path>, return a typed response. GETs are always safe to
        resend."""
        return await self._request(
            "GET",
            f"{API_PREFIX}/{op_path}",
            response_model,
            params=params,
            deadline_s=deadline_s,
            safe_resend=True,
        )

    async def _request(
        self,
        method: str,
        path: str,
        response_model: type[_RespT],
        *,
        json_body: object | None = None,
        params: dict[str, str] | None = None,
        deadline_s: float | None = None,
        idempotency_key: str | None = None,
        safe_resend: bool,
    ) -> _RespT:
        attempts = 2 if safe_resend else 1
        last_transport_exc: RpcTransportError | None = None
        for attempt in range(attempts):
            headers = self._envelope_headers(deadline_s=deadline_s, idempotency_key=idempotency_key)
            timeout = aiohttp.ClientTimeout(total=(deadline_s + _CLIENT_TIMEOUT_GRACE_S) if deadline_s else None)
            try:
                session = self._ensure_session()
                async with session.request(
                    method, path, json=json_body, params=params, headers=headers, timeout=timeout
                ) as resp:
                    if resp.status >= 400:
                        await self._raise_for_error(resp)
                    deduped = resp.headers.get(HEADER_DEDUPED)
                    if deduped:
                        # The daemon answered our resend from its idempotency
                        # machinery instead of re-executing — the exactly-once
                        # guarantee exercised for real. Centralized receipt.
                        logger.warning(
                            "Server deduplicated resend of %s %s on %s (%s)",
                            method,
                            path,
                            self.hostname,
                            deduped,
                        )
                    payload = await resp.read()
                return response_model.model_validate_json(payload)
            except _TRANSPORT_EXCS as exc:
                # Transport failure on THIS request's connection. Do NOT close
                # the shared session — it is reused for every op to this host,
                # so closing it would break other in-flight requests. aiohttp's
                # connector already discards the failed connection and opens a
                # fresh one on the retry below.
                last_transport_exc = RpcTransportError(f"{method} {path} on {self.hostname}: {exc}")
                if attempt + 1 < attempts:
                    # An ABSORBED transport failure must still leave a trace:
                    # silent recovery makes transport-health regressions
                    # (daemon deaths mid-response, connection churn) invisible
                    # until they exceed the retry budget.
                    logger.warning(
                        "RPC transport retry on %s: %s %s failed (%s), resending once",
                        self.hostname,
                        method,
                        path,
                        exc,
                    )
                    continue
        assert last_transport_exc is not None
        raise AgentUnreachableError(str(last_transport_exc)) from last_transport_exc

    async def put_bytes(
        self,
        op_path: str,
        data: bytes,
        response_model: type[_RespT],
        *,
        params: dict[str, str] | None = None,
        deadline_s: float | None = None,
    ) -> _RespT:
        """PUT a raw octet-stream body (files push). Idempotent by path, so
        safe to resend once on a transport blip."""
        path = f"{API_PREFIX}/{op_path}"
        for attempt in range(2):
            headers = self._envelope_headers(deadline_s=deadline_s, idempotency_key=None)
            headers["Content-Type"] = "application/octet-stream"
            timeout = aiohttp.ClientTimeout(total=(deadline_s + _CLIENT_TIMEOUT_GRACE_S) if deadline_s else None)
            try:
                session = self._ensure_session()
                async with session.put(path, data=data, params=params, headers=headers, timeout=timeout) as resp:
                    if resp.status >= 400:
                        await self._raise_for_error(resp)
                    payload = await resp.read()
                return response_model.model_validate_json(payload)
            except _TRANSPORT_EXCS as exc:
                # Per-request failure; the shared session stays open (see _request).
                if attempt == 0:
                    continue
                raise AgentUnreachableError(f"PUT {path} on {self.hostname}: {exc}") from exc
        raise AgentUnreachableError(f"PUT {path} on {self.hostname}: exhausted")

    async def get_bytes(
        self,
        op_path: str,
        *,
        params: dict[str, str] | None = None,
        deadline_s: float | None = None,
    ) -> bytes:
        """GET a raw octet-stream body (files pull), streamed into memory.
        Callers that need unbounded size should stream instead; the current
        consumers (spools, stamps) are bounded."""
        path = f"{API_PREFIX}/{op_path}"
        for attempt in range(2):
            headers = self._envelope_headers(deadline_s=deadline_s, idempotency_key=None)
            timeout = aiohttp.ClientTimeout(total=(deadline_s + _CLIENT_TIMEOUT_GRACE_S) if deadline_s else None)
            try:
                session = self._ensure_session()
                async with session.get(path, params=params, headers=headers, timeout=timeout) as resp:
                    if resp.status >= 400:
                        await self._raise_for_error(resp)
                    return await resp.read()
            except _TRANSPORT_EXCS as exc:
                # Per-request failure; the shared session stays open (see _request).
                if attempt == 0:
                    continue
                raise AgentUnreachableError(f"GET {path} on {self.hostname}: {exc}") from exc
        raise AgentUnreachableError(f"GET {path} on {self.hostname}: exhausted")

    async def _raise_for_error(self, resp: aiohttp.ClientResponse) -> None:
        try:
            error = RpcError.model_validate_json(await resp.read())
        except Exception:  # noqa: BLE001 - non-JSON error body
            raise RpcTransportError(f"HTTP {resp.status} from {self.hostname} with no structured body")
        if error.code == "UNAUTHORIZED":
            raise AgentAuthError(error.message)
        if error.code == "RECLAIMED":
            # In-flight op landed on a VM mid-teardown: the typed error is the
            # designed outcome (vs the SSH era's dropped-connection storms),
            # but it must leave a centralized trace that it happened.
            logger.warning("Op on %s received RECLAIMED mid-flight (VM being torn down)", self.hostname)
            raise VMReclaimedError(error.message)
        raise RpcException(error)
