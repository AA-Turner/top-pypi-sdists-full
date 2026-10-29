"""The device hop: ``POST …/chat/completions`` becomes ``POST {relay}/v1/devices/{D}/stream``.

``DeviceChat``'s ``AsyncOpenAI`` sends through :class:`RelayStreamTransport` (an httpx transport),
so the OpenAI translator and streaming parser run unchanged; only the wire differs. The relay
contract is matrx-desktop ``relay/README.md`` § ``/stream`` (``relay/src/stream-sink.ts``):

* request body ``{cap: "models", op: "llm.chat", params: {model: <ModelKey>, body: <the OpenAI
  body, stream:true, stream_options.include_usage:true>, start_if_stopped: true},
  first_byte_timeout_ms, idle_timeout_ms}``, ``Authorization: Bearer <relay bearer>``,
  ``x-matrx-protocol-version`` = the version ``models.llm.chat`` arrived in;
* before the device answers: a typed status + ``RelayCallResponse`` JSON — passed through, so the
  SDK raises ``APIStatusError`` and ``classify.py`` types it;
* after: 200 with the device's SSE bytes. Each read waits at most the idle deadline; a body that
  breaks, idles or ends without ``[DONE]`` raises ``DeviceStreamDroppedError`` (an ``event: error``
  block is left to the SDK, which raises ``APIError``).

PER CALL, NEVER ON THE SINGLETON: the device, the ModelKey and the person's token ride
:data:`_device_call` (set by ``DeviceChat.execute`` from ``profile.served_via`` and the ambient
``AppContext``). No target → nothing is sent.

HOST SEAM: matrx-ai never imports the host. The host binds the relay base URL and the bearer
(``relay_bearer(device_id, token)`` in aidream: the person's JWT while it lives, else a
device-bound broker run credential) once at startup::

    from matrx_ai.providers.device.relay_transport import configure_device_relay
    configure_device_relay(url=relay_url, bearer=relay_bearer)

Unbound → every device call is refused ``device_offline`` ("not wired"), never sent blind.
"""

from __future__ import annotations

import asyncio
import json
import logging
import re
from collections.abc import AsyncIterator, Awaitable, Callable
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any

import httpx
from matrx_utils import vcprint

#: The relay op (desktop protocol ``OPS["models.llm.chat"]``, a stream op).
RELAY_CAP = "models"
RELAY_OP = "llm.chat"
#: ``models.llm.chat`` arrived in protocol 1.76; announcing it greets the device in that version
#: (without the header the relay greets 1.0, which has no such op). Nothing newer is read.
RELAY_PROTOCOL_VERSION = "1.76"
RELAY_VERSION_HEADER = "x-matrx-protocol-version"
#: The relay's own defaults (relay/README.md): the first byte may wait for a model to load;
#: idle is the silence allowed between DATA frames. The relay caps each at 900 000 ms.
#: Both are knobs (``ai.device_relay``); a host may still pin a value through ``configure_device_relay``.
RELAY_KNOB_FEATURE = "ai.device_relay"
FIRST_BYTE_TIMEOUT_KEY = "first_byte_timeout_ms"
#: KNOB MIRROR of platform.feature_knob "ai.device_relay" "first_byte_timeout_ms"
FIRST_BYTE_TIMEOUT_MS_MIRROR = 300_000
IDLE_TIMEOUT_KEY = "idle_timeout_ms"
#: KNOB MIRROR of platform.feature_knob "ai.device_relay" "idle_timeout_ms"
IDLE_TIMEOUT_MS_MIRROR = 120_000
#: Our backstop beyond the relay's own deadline, so the relay's typed answer arrives first.
_HOP_HEADROOM_S = 15.0
_CONNECT_TIMEOUT_S = 15.0

RelayUrl = Callable[[], str | None]
#: The protocol version a device declares (the relay's device status ``protocol_version``), or None when unknown.
RelayPeerVersion = Callable[[str, str], Awaitable[str | None]]
RelayBearer = Callable[[str, str], Awaitable[str]]


@dataclass(frozen=True)
class DeviceCallTarget:
    """One device call: which device, which model the device loads, whose token."""

    device_id: str
    model_key: str
    token: str
    #: The conversation's real title, when it has one (never an "Auto:" placeholder): sent as
    #: ``params.chat_title`` so a busy refusal on the computer can name this chat (protocol 1.92).
    chat_title: str | None = None


@dataclass
class _RelaySeam:
    url: RelayUrl | None = None
    bearer: RelayBearer | None = None
    first_byte_timeout_ms: int | None = None
    idle_timeout_ms: int | None = None
    #: The hop's own httpx transport (``None`` = the network). Tests bind a fake relay here.
    http_transport: httpx.AsyncBaseTransport | None = None
    peer_version: RelayPeerVersion | None = None


_seam = _RelaySeam()
_device_call: ContextVar[DeviceCallTarget | None] = ContextVar("matrx_device_call", default=None)


def configure_device_relay(
    *,
    url: RelayUrl | None,
    bearer: RelayBearer | None,
    first_byte_timeout_ms: int | None = None,
    idle_timeout_ms: int | None = None,
    http_transport: httpx.AsyncBaseTransport | None = None,
    peer_version: RelayPeerVersion | None = None,
) -> None:
    """Bind the host's relay URL and bearer; ``url=None`` unbinds (every device call refused).

    The two waits are read live from their knobs unless the host pins one here."""
    global _seam
    _seam = _RelaySeam(
        url=url,
        bearer=bearer,
        first_byte_timeout_ms=None if first_byte_timeout_ms is None else int(first_byte_timeout_ms),
        idle_timeout_ms=None if idle_timeout_ms is None else int(idle_timeout_ms),
        http_transport=http_transport,
        peer_version=peer_version,
    )


def first_byte_timeout_ms() -> int:
    """How long a device call waits for its first byte: the host's pinned value, else the live knob."""
    if _seam.first_byte_timeout_ms is not None:
        return _seam.first_byte_timeout_ms
    from matrx_ai.knobs import package_knob_number

    return package_knob_number(RELAY_KNOB_FEATURE, FIRST_BYTE_TIMEOUT_KEY, FIRST_BYTE_TIMEOUT_MS_MIRROR,
                               low=1_000, high=900_000)  # the relay's own cap


def idle_timeout_ms() -> int:
    """The silence allowed between DATA frames: the host's pinned value, else the live knob."""
    if _seam.idle_timeout_ms is not None:
        return _seam.idle_timeout_ms
    from matrx_ai.knobs import package_knob_number

    return package_knob_number(RELAY_KNOB_FEATURE, IDLE_TIMEOUT_KEY, IDLE_TIMEOUT_MS_MIRROR,
                               low=1_000, high=900_000)  # the relay's own cap


#: The first desktop-protocol minor whose ``models.llm.chat`` takes ``chat_title`` (a strict schema refuses it before).
CHAT_TITLE_SINCE = (1, 92)


def version_at_least(version: str | None, since: tuple[int, int]) -> bool:
    """True only for a well-formed ``major.minor`` at or above ``since``; an unknown or odd version counts as old."""
    match = re.fullmatch(r"(\d+)\.(\d+)", (version or "").strip())
    return bool(match) and (int(match.group(1)), int(match.group(2))) >= since


async def peer_accepts_chat_title(target: DeviceCallTarget) -> bool:
    """Does the device declare protocol 1.92+? No declaration, or a failed read, means no: old peers refuse an unknown param."""
    reader = _seam.peer_version
    if reader is None:
        return False
    try:
        return version_at_least(await reader(target.device_id, target.token), CHAT_TITLE_SINCE)
    except Exception as exc:  # the title is a courtesy; an unreadable status must not fail the chat
        logging.getLogger(__name__).warning("device %s protocol version unreadable (%s): chat_title not sent", target.device_id, exc)
        return False


def device_relay_seam() -> _RelaySeam:
    """The bound seam (the host's wiring guard reads it)."""
    return _seam


def set_device_call(target: DeviceCallTarget | None) -> Any:
    """Bind this call's device target; returns the reset token."""
    return _device_call.set(target)


def reset_device_call(token: Any) -> None:
    _device_call.reset(token)


def relay_stream_envelope(target: DeviceCallTarget, body: dict[str, Any]) -> dict[str, Any]:
    """The exact ``/stream`` body for one chat completion (stream + usage forced)."""
    sent = dict(body)
    sent["stream"] = True
    stream_options = dict(sent.get("stream_options") or {})
    stream_options["include_usage"] = True
    sent["stream_options"] = stream_options
    return {
        "cap": RELAY_CAP,
        "op": RELAY_OP,
        "params": {
            "model": target.model_key,
            "body": sent,
            "start_if_stopped": True,
            **({"chat_title": target.chat_title.strip()[:200]} if target.chat_title and target.chat_title.strip() else {}),
        },
        "first_byte_timeout_ms": first_byte_timeout_ms(),
        "idle_timeout_ms": idle_timeout_ms(),
    }


def _refuse(cls_name: str, message: str, **details: Any) -> Exception:
    from matrx_ai.providers.device import errors
    from matrx_ai.providers.device.classify import make_device_error

    return make_device_error(getattr(errors, cls_name), message, details=details or None)


class _GuardedSseStream(httpx.AsyncByteStream):
    """The relay body, read under the idle deadline, ending loudly when it was cut short."""

    def __init__(self, upstream: httpx.Response, *, idle_s: float, is_sse: bool) -> None:
        self._upstream = upstream
        self._idle_s = idle_s
        self._is_sse = is_sse
        self._tail = b""
        self.done_seen = False
        self.error_event_seen = False
        self.bytes_seen = 0

    def _scan(self, chunk: bytes) -> None:
        window = self._tail + chunk
        if b"data: [DONE]" in window:
            self.done_seen = True
        if b"event: error" in window:
            self.error_event_seen = True
        self._tail = window[-32:]

    async def __aiter__(self) -> AsyncIterator[bytes]:
        chunks = self._upstream.aiter_raw()
        while True:
            try:
                chunk = await asyncio.wait_for(chunks.__anext__(), timeout=self._idle_s)
            except StopAsyncIteration:
                break
            except (TimeoutError, httpx.TimeoutException):
                raise _refuse(
                    "DeviceStreamDroppedError",
                    f"the device sent nothing for {self._idle_s:.0f} s after {self.bytes_seen} bytes",
                    reason="idle_timeout",
                ) from None
            except httpx.TransportError as exc:
                raise _refuse(
                    "DeviceStreamDroppedError",
                    f"the relay body broke after {self.bytes_seen} bytes: {type(exc).__name__}",
                    reason="body_broken",
                ) from exc
            self.bytes_seen += len(chunk)
            self._scan(chunk)
            yield chunk
        if self._is_sse and not self.done_seen and not self.error_event_seen:
            raise _refuse(
                "DeviceStreamDroppedError",
                f"the device stream ended without [DONE] after {self.bytes_seen} bytes",
                reason="no_done",
            )

    async def aclose(self) -> None:
        # Closing the relay body cancels the generation on the device (stream-sink.ts).
        await self._upstream.aclose()


class RelayStreamTransport(httpx.AsyncBaseTransport):
    """httpx transport for ``DeviceChat``'s ``AsyncOpenAI``: every request goes to the relay."""

    def __init__(self) -> None:
        self._hop: httpx.AsyncClient | None = None
        self._hop_loop: asyncio.AbstractEventLoop | None = None
        self._hop_transport: httpx.AsyncBaseTransport | None = None

    def _client(self) -> httpx.AsyncClient:
        loop = asyncio.get_running_loop()
        bound = _seam.http_transport
        if self._hop is None or self._hop_loop is not loop or self._hop_transport is not bound:
            read_s = first_byte_timeout_ms() / 1000 + _HOP_HEADROOM_S
            self._hop = httpx.AsyncClient(
                transport=bound,
                timeout=httpx.Timeout(
                    connect=_CONNECT_TIMEOUT_S, read=read_s, write=60.0, pool=30.0
                ),
            )
            self._hop_loop = loop
            self._hop_transport = bound
        return self._hop

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        target = _device_call.get()
        if target is None:
            raise _refuse(
                "DeviceInvalidRequestError",
                "device transport called with no device target on this call; nothing was sent",
                reason="no_target",
            )
        if request.method != "POST" or not request.url.path.endswith("/chat/completions"):
            raise _refuse(
                "DeviceInvalidRequestError",
                f"a device runs chat completions only, not {request.method} {request.url.path}",
                reason="unsupported_path",
            )
        url_fn, bearer_fn = _seam.url, _seam.bearer
        base = url_fn() if url_fn is not None else None
        if not base or bearer_fn is None:
            raise _refuse(
                "DeviceOfflineError",
                "the device relay is not wired in this process; nothing was sent",
                reason="relay_not_wired",
            )
        bearer = await bearer_fn(target.device_id, target.token or "")
        if not bearer:
            raise _refuse(
                "DeviceAuthExpiredError",
                f"no relay credential for device {target.device_id}; nothing was sent",
                reason="no_credential",
            )
        body = json.loads((await request.aread()) or b"{}")
        envelope = relay_stream_envelope(target, body)
        hop = self._client()
        relay_request = hop.build_request(
            "POST",
            f"{base.rstrip('/')}/v1/devices/{target.device_id}/stream",
            content=json.dumps(envelope).encode("utf-8"),
            headers={
                "authorization": f"Bearer {bearer}",
                "content-type": "application/json",
                "accept": "text/event-stream",
                RELAY_VERSION_HEADER: RELAY_PROTOCOL_VERSION,
            },
        )
        try:
            upstream = await hop.send(relay_request, stream=True)
        except httpx.TimeoutException:
            raise _refuse(
                "DeviceTimeoutError",
                f"the relay gave no answer within {first_byte_timeout_ms()} ms (+ headroom)",
                reason="hop_timeout",
            ) from None
        except httpx.TransportError as exc:
            raise _refuse(
                "DeviceOfflineError",
                f"the relay could not be reached: {type(exc).__name__}",
                reason="relay_unreachable",
            ) from exc

        if upstream.status_code != 200:
            # A typed answer before the device responded: hand it to the SDK as is, which
            # raises APIStatusError with this body; classify.py types it.
            content = await upstream.aread()
            await upstream.aclose()
            return httpx.Response(
                upstream.status_code,
                headers={"content-type": upstream.headers.get("content-type", "application/json")},
                content=content,
                request=request,
            )

        content_type = upstream.headers.get("content-type", "")
        result = upstream.headers.get("x-matrx-stream-result")
        if result:
            vcprint(
                f"[DEVICE CHAT] device {target.device_id} answers: {result[:200]}", color="cyan"
            )
        return httpx.Response(
            200,
            headers={"content-type": content_type or "text/event-stream"},
            stream=_GuardedSseStream(
                upstream,
                idle_s=idle_timeout_ms() / 1000 + _HOP_HEADROOM_S,
                is_sse=content_type.lower().startswith("text/event-stream"),
            ),
            request=request,
        )

    async def aclose(self) -> None:
        if self._hop is not None:
            await self._hop.aclose()
            self._hop = None


__all__ = [
    "FIRST_BYTE_TIMEOUT_MS_MIRROR",
    "IDLE_TIMEOUT_MS_MIRROR",
    "first_byte_timeout_ms",
    "idle_timeout_ms",
    "RELAY_CAP",
    "RELAY_OP",
    "RELAY_PROTOCOL_VERSION",
    "DeviceCallTarget",
    "RelayStreamTransport",
    "configure_device_relay",
    "device_relay_seam",
    "relay_stream_envelope",
    "reset_device_call",
    "set_device_call",
]
