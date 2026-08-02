"""Session protocols shared by SDK helper APIs."""

from typing import Protocol

from mistralai.vibe.sdk.transports.events import CallbackResultEvent


class AsyncCallbackSession(Protocol):
    """Async session shape required to send callback results upstream."""

    async def send_message(self, message: CallbackResultEvent) -> None: ...


class SyncCallbackSession(Protocol):
    """Sync session shape required to send callback results upstream."""

    def send_message(self, message: CallbackResultEvent) -> None: ...
