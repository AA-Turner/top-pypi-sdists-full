import io
import time

import pytest

from agentic_devtools.ai_providers.copilot_discovery import _write_message
from agentic_devtools.ai_providers.errors import ProviderError


class _Process:
    def __init__(self, stdin: object) -> None:
        self.stdin = stdin


def test_writes_a_newline_delimited_json_rpc_message() -> None:
    stdin = io.StringIO()
    process = _Process(stdin)

    _write_message(process, {"id": 1, "method": "initialize"}, 1.0)

    assert stdin.getvalue() == '{"id":1,"method":"initialize"}\n'


def test_raises_when_the_write_times_out() -> None:
    class _BlockingStdin:
        def write(self, _data: str) -> None:
            time.sleep(5)

        def flush(self) -> None:  # pragma: no cover - never reached
            return None

    with pytest.raises(ProviderError, match="Timed out after 0.1s writing an ACP request"):
        _write_message(_Process(_BlockingStdin()), {"id": 1}, 0.1)


def test_raises_when_the_pipe_is_broken() -> None:
    class _BrokenStdin:
        def write(self, _data: str) -> None:
            raise BrokenPipeError("stdin closed")

        def flush(self) -> None:  # pragma: no cover - never reached
            return None

    with pytest.raises(ProviderError, match="Failed to write an ACP request"):
        _write_message(_Process(_BrokenStdin()), {"id": 1}, 1.0)
