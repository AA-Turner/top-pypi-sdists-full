"""Response admission and compression ownership across ASGI send messages."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import assert_never

from starlette_compress._utils import (
    DEFAULT_CONTENT_TYPES,
    DEFAULT_STREAMING_CONTENT_TYPES,
    StartVerdict,
    classify_start_message,
    mutable_response_headers,
)

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    from typing import Protocol

    from starlette.types import ASGIApp, Message, Receive, Scope, Send

    class StreamEncoder(Protocol):
        def feed(self, data: bytes, flush: bool) -> Iterable[bytes]: ...
        def finish(self) -> Iterable[bytes]: ...

    OneshotCompress = Callable[[bytes], bytes]
    EncoderFactory = Callable[[int], StreamEncoder]


class ResponsePhase(Enum):
    AWAITING_START = auto()
    FORWARDING = auto()


@dataclass(frozen=True, slots=True)
class PendingStart:
    """Original response start retained until its body selects an encoding."""

    message: Message
    streaming: bool


@dataclass(frozen=True, slots=True)
class _Encoding:
    """Live stream compressor with its response flush policy."""

    encoder: StreamEncoder
    streaming: bool


def _content_length_from_raw(headers: Iterable[tuple[bytes, bytes]]) -> int:
    """Read Content-Length without mutating the header list."""
    for name, value in headers:
        if (name if name.islower() else name.lower()) == b'content-length':
            try:
                return int(value)
            except ValueError:
                return -1
    return -1


class CompressionResponder:
    """Shared ASGI control loop for encoded compression responders."""

    __slots__ = (
        'app',
        'content_types',
        'create_encoder',
        'encoding',
        'minimum_size',
        'oneshot',
        'streaming_content_types',
    )

    def __init__(
        self,
        app: ASGIApp,
        minimum_size: int,
        encoding: str,
        oneshot: OneshotCompress,
        create_encoder: EncoderFactory,
        content_types: frozenset[str] = DEFAULT_CONTENT_TYPES,
        streaming_content_types: frozenset[str] = DEFAULT_STREAMING_CONTENT_TYPES,
    ) -> None:
        self.app = app
        self.minimum_size = minimum_size
        self.encoding = encoding
        self.oneshot = oneshot
        self.create_encoder = create_encoder
        self.content_types = content_types
        self.streaming_content_types = streaming_content_types

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        state: ResponsePhase | PendingStart | _Encoding = ResponsePhase.AWAITING_START
        extensions: dict[str, object] = scope.get('extensions', {})
        pathsend_capable = 'http.response.pathsend' in extensions

        # Encoded path: never advertise zerocopysend — after Content-Encoding
        # is committed, a raw file would corrupt the response. Shallow-copy
        # only; do not mutate the caller's scope.
        if 'http.response.zerocopysend' in extensions:
            extensions = dict(extensions)
            del extensions['http.response.zerocopysend']
            scope = {**scope, 'extensions': extensions}

        async def wrapper(message: Message) -> None:
            nonlocal state

            message_type: str = message['type']

            if message_type == 'http.response.start':
                if state is not ResponsePhase.AWAITING_START:
                    raise RuntimeError('http.response.start has already been received')

                verdict = classify_start_message(
                    message, self.content_types, self.streaming_content_types
                )
                if verdict is StartVerdict.SKIP:
                    state = ResponsePhase.FORWARDING
                    await send(message)
                    return

                streaming = verdict is StartVerdict.STREAMING

                # Streaming types without pathsend: commit at start so clients
                # (e.g. EventSource) see headers before the first body event.
                if streaming and not pathsend_capable:
                    # Streaming: never pledge Content-Length to the encoder
                    # (SSE body size may not match the header).
                    active = _Encoding(self.create_encoder(-1), streaming)
                    headers = mutable_response_headers(message)
                    headers['Content-Encoding'] = self.encoding
                    headers.add_vary_header('Accept-Encoding')
                    del headers['Content-Length']
                    state = active
                    await send(message)
                    return

                state = PendingStart(message, streaming)
                return

            current = state
            if isinstance(current, _Encoding):
                active = current
                if message_type != 'http.response.body':
                    # Trailers / extensions after start — do not re-send start
                    await send(message)
                    return

                body: bytes = message.get('body', b'')
                more_body: bool = message.get('more_body', False)

            elif isinstance(current, PendingStart):
                start_message = current.message
                streaming = current.streaming
                if message_type != 'http.response.body':
                    # pathsend / trailers / unknown: forward original start raw
                    pending = start_message
                    state = ResponsePhase.FORWARDING
                    await send(pending)
                    await send(message)
                    return

                body = message.get('body', b'')
                more_body = message.get('more_body', False)

                if not streaming and not more_body and len(body) < self.minimum_size:
                    pending = start_message
                    state = ResponsePhase.FORWARDING
                    await send(pending)
                    await send(message)
                    return

                if not more_body:
                    # Terminal commit: fallible oneshot before any header mutation
                    # so a raised codec error leaves the app's start message intact.
                    compressed_body = self.oneshot(body)
                    headers = mutable_response_headers(start_message)
                    headers['Content-Encoding'] = self.encoding
                    headers.add_vary_header('Accept-Encoding')
                    headers['Content-Length'] = str(len(compressed_body))
                    message['body'] = compressed_body
                    del body
                    pending = start_message
                    state = ResponsePhase.FORWARDING
                    await send(pending)
                    await send(message)
                    return

                # Stream-begin: fallible encoder create before any header mutation.
                # Only buffered (non-streaming) paths may pledge Content-Length;
                # streaming always uses -1. CL is read via a non-mutating raw scan.
                if streaming:
                    content_length = -1
                else:
                    content_length = _content_length_from_raw(start_message['headers'])
                active = _Encoding(self.create_encoder(content_length), streaming)
                state = active
                headers = mutable_response_headers(start_message)
                headers['Content-Encoding'] = self.encoding
                headers.add_vary_header('Accept-Encoding')
                del headers['Content-Length']
                pending = start_message
                await send(pending)

            else:
                # Passthrough, finished, or a pre-start extension message.
                match current:
                    case ResponsePhase.AWAITING_START | ResponsePhase.FORWARDING:
                        await send(message)
                        return
                    case _:
                        assert_never(current)

            encoder = active.encoder
            streaming = active.streaming

            if more_body:
                if not body:
                    return
                for chunk in encoder.feed(body, streaming):
                    if chunk:
                        await send({
                            'type': 'http.response.body',
                            'body': chunk,
                            'more_body': True,
                        })
                return

            if body:
                for chunk in encoder.feed(body, False):
                    if chunk:
                        await send({
                            'type': 'http.response.body',
                            'body': chunk,
                            'more_body': True,
                        })

            final_chunk = b''
            for chunk in encoder.finish():
                if chunk:
                    if final_chunk:
                        await send({
                            'type': 'http.response.body',
                            'body': final_chunk,
                            'more_body': True,
                        })
                    final_chunk = chunk
            await send({'type': 'http.response.body', 'body': final_chunk})
            state = ResponsePhase.FORWARDING

        await self.app(scope, receive, wrapper)
