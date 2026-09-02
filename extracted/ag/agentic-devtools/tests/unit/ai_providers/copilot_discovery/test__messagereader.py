import time

import pytest

from agentic_devtools.ai_providers.copilot_discovery import _MessageReader
from agentic_devtools.ai_providers.errors import ProviderError


class _FragmentStream:
    """A stdout stub whose ``readline`` yields caller-supplied fragments."""

    def __init__(self, fragments: list[str], *, error: Exception | None = None) -> None:
        self._fragments = list(fragments)
        self._error = error
        self.closed = False

    def readline(self) -> str:
        if self._fragments:
            return self._fragments.pop(0)
        if self._error is not None:
            raise self._error
        return ""

    def close(self) -> None:
        self.closed = True


def _drain(reader: _MessageReader) -> list[str | None]:
    messages: list[str | None] = []
    while True:
        message = reader.next_message(2.0)
        messages.append(message)
        if message is None:
            return messages


def test_reassembles_a_message_split_across_reads() -> None:
    reader = _MessageReader(_FragmentStream(['{"jsonrpc":"2.0",', '"id":1,', '"result":{}}\n']))

    assert _drain(reader) == ['{"jsonrpc":"2.0","id":1,"result":{}}', None]


def test_splits_multiple_messages_delivered_in_one_read() -> None:
    reader = _MessageReader(_FragmentStream(['{"id":1}\n\n{"id":2}\n']))

    assert _drain(reader) == ['{"id":1}', '{"id":2}', None]


def test_flushes_a_trailing_fragment_at_eof() -> None:
    reader = _MessageReader(_FragmentStream(['{"id":1}']))

    assert _drain(reader) == ['{"id":1}', None]


def test_stops_reading_when_the_stream_raises() -> None:
    reader = _MessageReader(_FragmentStream(['{"id":1}\n'], error=ValueError("closed")))

    assert _drain(reader) == ['{"id":1}', None]


def test_raises_a_provider_error_when_no_message_arrives() -> None:
    class _BlockingStream:
        def readline(self) -> str:
            time.sleep(5)
            return ""

        def close(self) -> None:
            return None

    reader = _MessageReader(_BlockingStream())

    with pytest.raises(ProviderError, match="Timed out after 0.1s waiting for an ACP message"):
        reader.next_message(0.1)


def test_stop_closes_the_stream_and_swallows_close_failures() -> None:
    stream = _FragmentStream([])
    reader = _MessageReader(stream)
    reader.stop()

    assert stream.closed is True

    class _UnclosableStream:
        def readline(self) -> str:
            return ""

        def close(self) -> None:
            raise OSError("already closed")

    _MessageReader(_UnclosableStream()).stop()
