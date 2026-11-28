from __future__ import annotations

from starlette_compress._responder import PendingStart, ResponsePhase
from starlette_compress._utils import (
    DEFAULT_CONTENT_TYPES,
    DEFAULT_STREAMING_CONTENT_TYPES,
    StartVerdict,
    classify_start_message,
    mutable_response_headers,
)

TYPE_CHECKING = False
if TYPE_CHECKING:
    from starlette.types import ASGIApp, Message, Receive, Scope, Send


class IdentityResponder:
    __slots__ = (
        'app',
        'content_types',
        'minimum_size',
        'streaming_content_types',
    )

    def __init__(
        self,
        app: ASGIApp,
        minimum_size: int,
        content_types: frozenset[str] = DEFAULT_CONTENT_TYPES,
        streaming_content_types: frozenset[str] = DEFAULT_STREAMING_CONTENT_TYPES,
    ) -> None:
        self.app = app
        self.minimum_size = minimum_size
        self.content_types = content_types
        self.streaming_content_types = streaming_content_types

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        state: ResponsePhase | PendingStart = ResponsePhase.AWAITING_START
        pathsend_capable = 'http.response.pathsend' in scope.get('extensions', ())

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

                # Streaming types without pathsend: send start immediately so
                # clients see headers before the first body; pass messages through.
                if streaming and not pathsend_capable:
                    headers = mutable_response_headers(message)
                    headers.add_vary_header('Accept-Encoding')
                    state = ResponsePhase.FORWARDING
                    await send(message)
                    return

                state = PendingStart(message, streaming)
                return

            if isinstance(state, PendingStart):
                pending = state.message
                streaming = state.streaming
                state = ResponsePhase.FORWARDING
                if message_type != 'http.response.body':
                    await send(pending)
                    await send(message)
                    return

                body: bytes = message.get('body', b'')
                more_body: bool = message.get('more_body', False)

                if not streaming and not more_body and len(body) < self.minimum_size:
                    await send(pending)
                    await send(message)
                    return

                headers = mutable_response_headers(pending)
                headers.add_vary_header('Accept-Encoding')
                await send(pending)
                await send(message)
                return

            # Committed identity: pure passthrough, including empty bodies.
            await send(message)

        await self.app(scope, receive, wrapper)
