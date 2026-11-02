"""The standard input of a sandbox process."""

import json
from typing import ClassVar

from labqoat.json_document import JsonDocument
from labqoat.sandbox.sandbox_request import SandboxRequest
from labqoat.sandbox.sandbox_transport import SandboxTransport
from labqoat.sandbox.sandbox_unavailable_error import SandboxUnavailableError


class SandboxStreamWriter:
    """Buffer what is written and send it with ``drain``; ``write_eof`` closes the input once it is drained.

    Every send names the position of its first byte, so the host keeps each byte once and a send lost with its
    connection is simply sent again. Bytes written after the process exited are accepted and discarded.
    """

    RESENDS: ClassVar[int] = 3

    def __init__(self, transport: SandboxTransport, path: str, piped: bool) -> None:
        """Bind the process's input path; input that is not piped takes no writes."""
        self._transport = transport
        self._path = path
        self._piped = piped
        self._buffer = bytearray()
        self._sent = 0
        self._eof = False
        self._closed = False

    def write(self, data: bytes | bytearray | memoryview | str) -> None:
        """Add bytes, or text as UTF-8, to what the next ``drain`` sends."""
        self._open()
        self._buffer += data.encode() if isinstance(data, str) else data

    def write_eof(self) -> None:
        """Close the input after what is buffered; the next ``drain`` sends the end."""
        self._open()
        self._eof = True

    def drain(self) -> None:
        """Send what is buffered, and the end of input if it was written, before returning."""
        lost = 0
        while self._pending():
            try:
                self._accepted(self._transport.send(self._request()))
            except SandboxUnavailableError:
                lost += 1
                if lost == self.RESENDS:
                    raise

    async def drain_async(self) -> None:
        """Send what is buffered without blocking the event loop; see ``drain``."""
        lost = 0
        while self._pending():
            try:
                self._accepted(await self._transport.send_async(self._request()))
            except SandboxUnavailableError:
                lost += 1
                if lost == self.RESENDS:
                    raise

    def _open(self) -> None:
        """Refuse a write the input can no longer take."""
        if not self._piped:
            raise ValueError("this process's standard input is not a pipe; start it with stdin=StreamType.PIPE")
        if self._eof:
            raise ValueError("this process's standard input was closed with write_eof()")

    def _pending(self) -> bool:
        """Report whether bytes or the end of input still have to reach the host."""
        return bool(self._buffer) or (self._eof and not self._closed)

    def _request(self) -> SandboxRequest:
        """Send the buffer at the position of its first byte, with the end of input when it is due."""
        query = {"offset": str(self._sent), **({"eof": "true"} if self._eof else {})}
        return SandboxRequest("POST", self._path, query, content=bytes(self._buffer))

    def _accepted(self, content: bytes) -> None:
        """Forget the bytes the host now holds, and remember an end of input it took with them."""
        try:
            accepted = JsonDocument.expect_scalar(JsonDocument.expect_dict(json.loads(content))["accepted"], int)
            if not self._sent <= accepted <= self._sent + len(self._buffer):
                raise ValueError(f"the host accepted up to {accepted} after {self._sent} were sent")
        except (KeyError, TypeError, ValueError) as error:
            raise SandboxUnavailableError("Sandbox host returned a malformed response") from error
        del self._buffer[: accepted - self._sent]
        self._sent = accepted
        self._closed = self._eof
