"""Tests for the single-finding dispatch host CLI entry point."""

import json
from pathlib import Path

import pytest

from agentic_devtools.ai_providers.agent_tasks_payload import AgentTasksPayload
from agentic_devtools.cli.github.single_finding_dispatch import SingleFindingDispatchResult, SingleFindingHandoff
from agentic_devtools.cli.github.single_finding_dispatch_host import main


def test_dispatches_json_handoff_and_emits_result(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    handoff_and_payload: tuple[SingleFindingHandoff, AgentTasksPayload],
) -> None:
    from agentic_devtools.cli.github import single_finding_dispatch_host as module

    handoff, payload = handoff_and_payload
    handoff_file = tmp_path / "handoff.json"
    handoff_file.write_text(
        json.dumps({"handoff": handoff.model_dump(mode="json"), "payload": payload.to_dict()}),
        encoding="utf-8",
    )

    class DummyHost:
        def __init__(self, state_dir: Path) -> None:
            assert state_dir == tmp_path

    class DummyAdapter:
        def __init__(self, host: object, *, clock: object) -> None:
            assert isinstance(host, DummyHost)

        def dispatch(self, parsed_handoff: SingleFindingHandoff, parsed_payload: AgentTasksPayload):
            assert parsed_handoff == handoff
            assert parsed_payload == payload
            return SingleFindingDispatchResult(
                outcome="already_active",
                reason="duplicate",
                expected_head=handoff.expected_head,
                finding_id=handoff.finding_id,
                attempt_id=handoff.attempt_id,
                task_id=None,
                session_id=None,
            )

    monkeypatch.setattr(module, "get_state_dir", lambda: tmp_path)
    monkeypatch.setattr(module, "GitHubSingleFindingDispatchHost", DummyHost)
    monkeypatch.setattr(module, "SingleFindingDispatchAdapter", DummyAdapter)

    main([str(handoff_file)])

    assert json.loads(capsys.readouterr().out)["outcome"] == "already_active"


def test_reports_payload_digest_mismatch_as_cli_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    handoff_and_payload: tuple[SingleFindingHandoff, AgentTasksPayload],
) -> None:
    from agentic_devtools.cli.github import single_finding_dispatch_host as module

    handoff, payload = handoff_and_payload
    invalid_payload = AgentTasksPayload(**{**payload.to_dict(), "prompt": "repair a different finding"})
    handoff_file = tmp_path / "handoff.json"
    handoff_file.write_text(
        json.dumps({"handoff": handoff.model_dump(mode="json"), "payload": invalid_payload.to_dict()}),
        encoding="utf-8",
    )
    monkeypatch.setattr(module, "get_state_dir", lambda: tmp_path)

    with pytest.raises(SystemExit) as exc_info:
        main([str(handoff_file)])

    assert exc_info.value.code == 2
    assert "payload digest" in capsys.readouterr().err


@pytest.mark.parametrize(
    ("content", "message"),
    [
        ("{", "could not read handoff JSON"),
        ("[]", "exactly 'handoff' and 'payload'"),
        ('{"handoff":{}}', "exactly 'handoff' and 'payload'"),
        ('{"handoff":[],"payload":{}}', "must both be JSON objects"),
        ('{"handoff":{},"payload":[]}', "must both be JSON objects"),
        ('{"handoff":{},"payload":{}}', "validation failed"),
    ],
)
def test_rejects_invalid_handoff_files(
    tmp_path: Path,
    content: str,
    message: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    handoff_file = tmp_path / "invalid.json"
    handoff_file.write_text(content, encoding="utf-8")

    with pytest.raises(SystemExit) as exc_info:
        main([str(handoff_file)])
    assert exc_info.value.code == 2
    assert message in capsys.readouterr().err


def test_reports_missing_handoff_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main([str(tmp_path / "missing.json")])
    assert exc_info.value.code == 2
    error = capsys.readouterr().err
    assert "could not read handoff JSON" in error
    assert "missing.json" in error


def test_reports_non_utf8_handoff_file_as_cli_error(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    handoff_file = tmp_path / "non-utf8.json"
    handoff_file.write_bytes(b"\xff")

    with pytest.raises(SystemExit) as exc_info:
        main([str(handoff_file)])

    assert exc_info.value.code == 2
    assert "could not read handoff JSON" in capsys.readouterr().err
