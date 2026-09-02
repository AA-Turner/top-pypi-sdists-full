import json
import queue
import threading
from pathlib import Path
from typing import Any, cast
from unittest.mock import patch

import pytest

from agentic_devtools.ai_providers.copilot_discovery import CopilotACPDiscovery
from agentic_devtools.ai_providers.errors import ProviderError

_FIXTURES = Path(__file__).resolve().parents[3] / "fixtures" / "acp"
_INITIALIZE_RESPONSE = (_FIXTURES / "copilot-initialize-response.json").read_text(encoding="utf-8")
_SESSION_NEW_RESPONSE = (_FIXTURES / "copilot-session-new-response.json").read_text(encoding="utf-8")

_SESSION_UPDATE_NOTIFICATION = json.dumps(
    {"jsonrpc": "2.0", "method": "session/update", "params": {"sessionId": "s-1"}}
)
_UNRELATED_RESPONSE = json.dumps({"jsonrpc": "2.0", "id": 99, "result": {}})


def _compact(raw: str) -> str:
    return json.dumps(json.loads(raw), separators=(",", ":"))


def _label(line: str) -> str:
    """Describe a scripted line for the interleaving journal."""
    try:
        message = json.loads(line)
    except json.JSONDecodeError:
        return "malformed"
    if isinstance(message, dict):
        return str(message.get("id", "notification"))
    return "non-object"


def _script(**responses: list[Any]) -> dict[str, list[Any]]:
    return dict(responses)


class _Stdin:
    def __init__(self, process: "FakeACPProcess") -> None:
        self._process = process
        self.closed = False

    def write(self, data: str) -> None:
        self._process.handle_write(data)

    def flush(self) -> None:
        return None

    def close(self) -> None:
        self.closed = True


class _Stdout:
    def __init__(self, process: "FakeACPProcess") -> None:
        self._process = process

    def readline(self) -> str:
        return self._process.next_line()

    def close(self) -> None:
        return None


class FakeACPProcess:
    """A scripted ACP responder that only replies after a request is written."""

    def __init__(self, script: dict[str, list[Any]], *, read_wait: float = 2.0) -> None:
        self._script = script
        self._read_wait = read_wait
        self._pending: queue.Queue[Any] = queue.Queue()
        self.journal: list[tuple[str, str]] = []
        self.stdin = _Stdin(self)
        self.stdout = _Stdout(self)
        self.terminated = False

    def handle_write(self, data: str) -> None:
        message = json.loads(data)
        self.journal.append(("write", message["method"]))
        for line in self._script.get(message["method"], []):
            self._pending.put(line)

    def next_line(self) -> str:
        try:
            line = self._pending.get(timeout=self._read_wait)
        except queue.Empty:
            return ""
        if line is None:
            return ""
        self.journal.append(("read", _label(line)))
        return line + "\n"

    def poll(self) -> int | None:
        return None

    def terminate(self) -> None:
        self.terminated = True

    def wait(self, timeout: float | None = None) -> int:
        return 0

    def kill(self) -> None:  # pragma: no cover - only used on teardown failures
        return None


def _discovery(process: FakeACPProcess, **overrides: Any) -> CopilotACPDiscovery:
    options: dict[str, Any] = {
        "command": ["copilot", "--acp"],
        "cwd": Path.cwd(),
        "initialize_read_timeout": 1.0,
        "session_new_write_timeout": 1.0,
        "session_new_read_timeout": 1.0,
        "overall_timeout": 5.0,
        "spawn": lambda _command, _cwd: process,
    }
    options.update(overrides)
    return CopilotACPDiscovery(**options)


def _successful_process(**kwargs: Any) -> FakeACPProcess:
    return FakeACPProcess(
        _script(
            initialize=[_compact(_INITIALIZE_RESPONSE)],
            **{"session/new": [_compact(_SESSION_NEW_RESPONSE)]},
        ),
        **kwargs,
    )


def test_returns_the_authoritative_model_list() -> None:
    process = _successful_process()

    records = _discovery(process).discover_models()

    assert [record.model_id for record in records] == ["auto", "gpt-5-mini", "claude-haiku-4.5"]
    assert cast("dict[str, Any]", records[1].raw_metadata["_meta"]) == {
        "copilotUsage": "0x",
        "copilotPriceCategory": "low",
        "copilotEnablement": "enabled",
    }


def test_writes_session_new_only_after_the_initialize_reply_is_read() -> None:
    process = _successful_process()

    _discovery(process).discover_models()

    assert process.journal == [
        ("write", "initialize"),
        ("read", "1"),
        ("write", "session/new"),
        ("read", "2"),
    ]


def test_sends_the_acp_handshake_payloads() -> None:
    process = _successful_process()
    written: list[dict[str, Any]] = []
    original = process.handle_write

    def _record(data: str) -> None:
        written.append(json.loads(data))
        original(data)

    process.handle_write = _record  # type: ignore[method-assign]

    _discovery(process, cwd=Path.cwd()).discover_models()

    assert written[0]["id"] == 1
    assert written[0]["method"] == "initialize"
    assert written[0]["params"]["protocolVersion"] == 1
    assert written[0]["params"]["clientCapabilities"]["fs"] == {"readTextFile": True, "listDirectory": True}
    assert written[1]["id"] == 2
    assert written[1]["method"] == "session/new"
    assert written[1]["params"]["cwd"] == str(Path.cwd().resolve())
    assert written[1]["params"]["mcpServers"] == []


def test_ignores_notifications_and_unrelated_responses() -> None:
    process = FakeACPProcess(
        _script(
            initialize=[_SESSION_UPDATE_NOTIFICATION, _compact(_INITIALIZE_RESPONSE)],
            **{"session/new": [_SESSION_UPDATE_NOTIFICATION, _UNRELATED_RESPONSE, _compact(_SESSION_NEW_RESPONSE)]},
        )
    )

    records = _discovery(process).discover_models()

    assert [record.model_id for record in records] == ["auto", "gpt-5-mini", "claude-haiku-4.5"]


def test_ignores_responses_with_boolean_or_float_ids() -> None:
    # Python equality: True == 1 and 2.0 == 2, so without an isinstance guard a
    # response with id=true could be accepted as the id-1 initialize reply and a
    # response with id=2.0 could be accepted as the id-2 session/new reply.
    bool_id_response = json.dumps({"jsonrpc": "2.0", "id": True, "result": {}})
    float_id_response = json.dumps({"jsonrpc": "2.0", "id": 2.0, "result": {}})
    process = FakeACPProcess(
        _script(
            initialize=[bool_id_response, _compact(_INITIALIZE_RESPONSE)],
            **{"session/new": [float_id_response, _compact(_SESSION_NEW_RESPONSE)]},
        )
    )

    records = _discovery(process).discover_models()

    assert [record.model_id for record in records] == ["auto", "gpt-5-mini", "claude-haiku-4.5"]

    process = _successful_process()

    _discovery(process).discover_models()

    assert process.stdin.closed is True
    assert process.terminated is True


def test_raises_when_the_stream_ends_before_the_response() -> None:
    process = FakeACPProcess(_script(initialize=[None]))

    with pytest.raises(ProviderError, match="stream ended before the response with id 1"):
        _discovery(process).discover_models()


def test_raises_when_the_response_never_arrives() -> None:
    process = _successful_process()
    process._script["session/new"] = []

    with pytest.raises(ProviderError, match="Timed out after 0.2s waiting for an ACP message"):
        _discovery(process, session_new_read_timeout=0.2).discover_models()


def test_raises_when_the_overall_budget_is_exhausted() -> None:
    with pytest.raises(ValueError, match="overall_timeout"):
        _discovery(cast(FakeACPProcess, None), overall_timeout=-1.0)


def test_raises_when_a_timeout_is_zero_or_negative() -> None:
    with pytest.raises(ValueError, match="initialize_read_timeout"):
        _discovery(cast(FakeACPProcess, None), initialize_read_timeout=0.0)

    with pytest.raises(ValueError, match="session_new_write_timeout"):
        _discovery(cast(FakeACPProcess, None), session_new_write_timeout=-5.0)


def test_raises_when_a_timeout_is_not_finite() -> None:
    with pytest.raises(ValueError, match="overall_timeout"):
        _discovery(cast(FakeACPProcess, None), overall_timeout=float("nan"))

    with pytest.raises(ValueError, match="session_new_read_timeout"):
        _discovery(cast(FakeACPProcess, None), session_new_read_timeout=float("inf"))


def test_raises_when_a_timeout_is_a_boolean() -> None:
    with pytest.raises(ValueError, match="initialize_read_timeout"):
        _discovery(cast(FakeACPProcess, None), initialize_read_timeout=True)  # type: ignore[arg-type]


def test_raises_on_malformed_json() -> None:
    process = FakeACPProcess(_script(initialize=['{"jsonrpc":"2.0",']))

    with pytest.raises(ProviderError, match="malformed JSON"):
        _discovery(process).discover_models()


def test_raises_on_non_json_constants() -> None:
    process = FakeACPProcess(_script(initialize=['{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":NaN}}']))

    with pytest.raises(ProviderError, match="malformed JSON"):
        _discovery(process).discover_models()


def test_raises_when_a_json_message_is_not_an_object() -> None:
    process = FakeACPProcess(_script(initialize=["[1, 2, 3]"]))

    with pytest.raises(ProviderError, match="not an object"):
        _discovery(process).discover_models()


@pytest.mark.parametrize(
    ("response",),
    [
        (json.dumps({"id": 1, "result": {"protocolVersion": 1}}),),
        (json.dumps({"jsonrpc": "1.0", "id": 1, "result": {"protocolVersion": 1}}),),
    ],
)
def test_raises_on_non_json_rpc_2_0_response(response: str) -> None:
    process = FakeACPProcess(_script(initialize=[response]))

    with pytest.raises(ProviderError, match=r"The ACP responder returned a non-JSON-RPC-2\.0 response for id 1\."):
        _discovery(process).discover_models()


def test_raises_on_a_json_rpc_error_response() -> None:
    error_response = json.dumps({"jsonrpc": "2.0", "id": 2, "error": {"code": -32000, "message": "no session"}})
    process = FakeACPProcess(_script(initialize=[_compact(_INITIALIZE_RESPONSE)], **{"session/new": [error_response]}))

    with pytest.raises(ProviderError, match="JSON-RPC error for id 2"):
        _discovery(process).discover_models()


def test_raises_when_the_model_list_is_missing() -> None:
    response = json.dumps({"jsonrpc": "2.0", "id": 2, "result": {"sessionId": "s-1"}})
    process = FakeACPProcess(_script(initialize=[_compact(_INITIALIZE_RESPONSE)], **{"session/new": [response]}))

    with pytest.raises(ProviderError, match="no models object"):
        _discovery(process).discover_models()


def test_raises_when_initialize_response_has_no_result_object() -> None:
    response = json.dumps({"jsonrpc": "2.0", "id": 1})
    process = FakeACPProcess(_script(initialize=[response]))

    with pytest.raises(ProviderError, match="initialize response has no result object"):
        _discovery(process).discover_models()


def test_raises_when_initialize_protocol_version_is_invalid() -> None:
    response = json.dumps({"jsonrpc": "2.0", "id": 1, "result": {"protocolVersion": "1"}})
    process = FakeACPProcess(_script(initialize=[response]))

    with pytest.raises(ProviderError, match="invalid protocolVersion"):
        _discovery(process).discover_models()


def test_raises_when_initialize_protocol_version_mismatches() -> None:
    response = json.dumps({"jsonrpc": "2.0", "id": 1, "result": {"protocolVersion": 2}})
    process = FakeACPProcess(_script(initialize=[response]))

    with pytest.raises(ProviderError, match="protocolVersion mismatch"):
        _discovery(process).discover_models()


def test_raises_when_no_entry_is_usable() -> None:
    response = json.dumps({"jsonrpc": "2.0", "id": 2, "result": {"models": {"availableModels": [{"name": "no id"}]}}})
    process = FakeACPProcess(_script(initialize=[_compact(_INITIALIZE_RESPONSE)], **{"session/new": [response]}))

    with pytest.raises(ProviderError, match="no usable model entries"):
        _discovery(process).discover_models()


def test_raises_when_no_copilot_binary_is_available() -> None:
    with patch("agentic_devtools.ai_providers.copilot_discovery.resolve_acp_command", return_value=None):
        with pytest.raises(ProviderError, match="No Copilot binary is available"):
            CopilotACPDiscovery().discover_models()


def test_resolves_the_command_and_cwd_by_default() -> None:
    process = _successful_process()
    spawned: list[tuple[Any, str]] = []

    def _spawn(command: Any, cwd: str) -> FakeACPProcess:
        spawned.append((command, cwd))
        return process

    with patch(
        "agentic_devtools.ai_providers.copilot_discovery.resolve_acp_command",
        return_value=["copilot", "--acp"],
    ):
        CopilotACPDiscovery(spawn=_spawn).discover_models()

    assert spawned == [(["copilot", "--acp"], str(Path.cwd().resolve()))]


def test_times_out_when_spawn_never_returns() -> None:
    release = threading.Event()

    def _spawn(_command: Any, _cwd: str) -> FakeACPProcess:
        release.wait(timeout=1.0)
        return _successful_process()

    with pytest.raises(ProviderError, match="Timed out after 0.1s spawning"):
        CopilotACPDiscovery(
            command=["copilot", "--acp"],
            cwd=Path.cwd(),
            initialize_read_timeout=1.0,
            session_new_write_timeout=1.0,
            session_new_read_timeout=1.0,
            overall_timeout=0.1,
            spawn=_spawn,
        ).discover_models()

    release.set()


def test_terminates_orphan_process_spawned_after_timeout() -> None:
    """A process handle produced by the spawn worker after the caller times out must be terminated."""
    import time

    release = threading.Event()
    orphan = _successful_process()

    def _spawn(_command: Any, _cwd: str) -> FakeACPProcess:
        release.wait(timeout=2.0)
        return orphan

    with pytest.raises(ProviderError, match="Timed out after 0.1s spawning"):
        CopilotACPDiscovery(
            command=["copilot", "--acp"],
            cwd=Path.cwd(),
            initialize_read_timeout=1.0,
            session_new_write_timeout=1.0,
            session_new_read_timeout=1.0,
            overall_timeout=0.1,
            spawn=_spawn,
        ).discover_models()

    # Allow the blocked spawn to complete so the orphan can be cleaned up.
    release.set()

    # Wait up to 3 s for the worker to terminate the orphan (either via the
    # cancelled event in the worker or the finally-block cleanup path).
    for _ in range(60):
        if orphan.terminated:
            break
        time.sleep(0.05)

    assert orphan.terminated, "Orphan process was not terminated after spawn timeout"


def test_propagates_provider_errors_from_spawn() -> None:
    def _spawn(_command: Any, _cwd: str) -> FakeACPProcess:
        raise ProviderError("blocked", category="transport_error")

    with pytest.raises(ProviderError, match="blocked"):
        CopilotACPDiscovery(
            command=["copilot", "--acp"],
            cwd=Path.cwd(),
            initialize_read_timeout=1.0,
            session_new_write_timeout=1.0,
            session_new_read_timeout=1.0,
            overall_timeout=1.0,
            spawn=_spawn,
        ).discover_models()


def test_wraps_non_provider_spawn_failures() -> None:
    def _spawn(_command: Any, _cwd: str) -> FakeACPProcess:
        raise RuntimeError("boom")

    with pytest.raises(ProviderError, match="Failed to spawn the Copilot ACP process: boom"):
        CopilotACPDiscovery(
            command=["copilot", "--acp"],
            cwd=Path.cwd(),
            initialize_read_timeout=1.0,
            session_new_write_timeout=1.0,
            session_new_read_timeout=1.0,
            overall_timeout=1.0,
            spawn=_spawn,
        ).discover_models()


def test_raises_when_spawn_returns_no_process_handle() -> None:
    def _spawn(_command: Any, _cwd: str) -> None:
        return None

    with pytest.raises(ProviderError, match="no process handle was returned"):
        CopilotACPDiscovery(
            command=["copilot", "--acp"],
            cwd=Path.cwd(),
            initialize_read_timeout=1.0,
            session_new_write_timeout=1.0,
            session_new_read_timeout=1.0,
            overall_timeout=1.0,
            spawn=_spawn,
        ).discover_models()
