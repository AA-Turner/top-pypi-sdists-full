"""The writer may end a run in the same response as its last writes (daemon cost
round 4, B2), and a write that did not land in that response keeps the run going.

pydantic-ai's default 'graceful' end strategy runs the tools that precede
`final_result` in one response, then ends: the model never reads their answers.
So every write that failed or was not run -- a nonzero exit, a pre-check block,
a refusal -- counts in `Deps.lost_writes` (`tools`), and the writer's shell tool
raises `ModelRetry` when it grew in a response that also ends the run
(`agent.lost_write_retry`), which suppresses the end. A write the researcher was
asked about is not lost: it waits for them.
"""

from __future__ import annotations

import asyncio
import time

import pytest

from probe.daemon import approvals as appr, lease, probe_api, tools
from probe.daemon.store import Store

SID = "11111111-2222-3333-4444-555555555555"


@pytest.fixture(autouse=True)
def _state(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_DAEMON_MCP", "0")
    monkeypatch.delenv("PROBE_AGENT", raising=False)
    monkeypatch.setattr(probe_api, "_features", None)


def _deps(tmp_path, *, bypass: bool = False) -> tools.Deps:
    work = tmp_path / "work"
    work.mkdir(parents=True, exist_ok=True)
    lease.sessions_dir().mkdir(parents=True, exist_ok=True)
    (lease.sessions_dir() / f"{SID}.state").write_text("daemon")
    assert lease.renew(SID)
    return tools.Deps(store=Store(tmp_path / "s.sqlite", clock=time.time), board=appr.Board(tmp_path / "appr"),
                      session_id=SID, cwd=work, workdirs=[work], home=tmp_path, write_dirs=[], probe_env={},
                      bypass=bypass, mode_known=True, bite_id=1, op_seed=f"{SID}:1")


class Probe:
    """Stands in for `tools.run_probe_process`: each command exits with its
    head's code (default 0)."""

    def __init__(self, codes: dict[str, int] | None = None) -> None:
        self.codes = codes or {}
        self.ran: list[list[str]] = []

    async def __call__(self, deps, argv, op_id, **kw):
        self.ran.append(list(argv))
        return tools.ProbeResult(self.codes.get(" ".join(argv[:2]), 0), "{}")


# ---------------------------------------------------------------------------
# What counts as a lost write.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("command, codes, bypass, lost", [
    ("probe run tag r1 done", {}, False, 0),                       # a write that ran
    ("probe run tag r1 done", {"run tag": 1}, False, 1),           # a write that failed
    ("probe run get r1", {"run get": 1}, False, 0),                # a read that failed: nothing lost
    ("probe session toggle", {}, False, 1),                        # a write the pre-checks blocked
    ("probe run tag r1 a && probe run tag r1 b", {"run tag": 1}, False, 2),  # failed, and the part after never ran
    ("probe run get r1 && probe run tag r1 b", {"run get": 1}, False, 1),  # a read failed: the write after it is lost
    ("touch done.txt", {}, False, 0),                              # asked about: it waits for the researcher
    ("touch done.txt", {}, True, 0),                               # bypass: it ran
    ("env -i true", {}, True, 1),                                  # refused in every mode
    ("ls", {}, False, 0),                                          # a safe read
], ids=["write-ran", "write-failed", "read-failed", "blocked", "compound", "compound-read-first", "asked",
        "bypass-ran", "refused", "read"])
def test_a_write_that_did_not_land_counts_as_lost(tmp_path, monkeypatch, command, codes, bypass, lost):
    monkeypatch.setattr(tools, "run_probe_process", Probe(codes))
    deps = _deps(tmp_path, bypass=bypass)
    out = asyncio.run(tools.shell(deps, command))
    assert deps.lost_writes == lost, out


def test_a_write_cut_off_by_a_lost_lease_is_not_lost(tmp_path, monkeypatch):
    """The run is stopping anyway (`Deps.stopped`): nothing to go on with."""
    monkeypatch.setattr(tools, "run_probe_process", Probe())
    deps = _deps(tmp_path)
    (lease.sessions_dir() / f"{SID}.state").write_text("off")
    out = asyncio.run(tools.shell(deps, "probe run tag r1 done"))
    assert deps.stopped and deps.lost_writes == 0, out


# ---------------------------------------------------------------------------
# Through the writer agent itself.
# ---------------------------------------------------------------------------


def _ending(command: str, summary: str):
    """One response: a shell call, then `final_result` -- the shape B2 asks for."""
    pytest.importorskip("pydantic_ai")  # the `daemon` extra; agent-ci's plain shards lack it
    from pydantic_ai.messages import ModelResponse, ToolCallPart

    return ModelResponse(parts=[ToolCallPart("shell", {"command": command, "why": "record"}),
                                ToolCallPart("final_result", {"summary": summary})])


def _run_writer(tmp_path, monkeypatch, responses, codes):
    pytest.importorskip("pydantic_ai")
    from pydantic_ai.models.function import FunctionModel

    from probe.daemon import agent as agent_mod

    probe = Probe(codes)
    monkeypatch.setattr(tools, "run_probe_process", probe)
    seen: list = []

    def model(messages, info):
        seen.append(messages)
        return responses[min(len(seen), len(responses)) - 1]

    agent = agent_mod.build_agent("instructions", model=FunctionModel(model))
    result = asyncio.run(agent.run("record the session", deps=_deps(tmp_path)))
    return result, seen, probe


def _retries(messages) -> list[str]:
    from pydantic_ai.messages import ModelRequest, RetryPromptPart

    return [p.content for m in messages if isinstance(m, ModelRequest) for p in m.parts
            if isinstance(p, RetryPromptPart)]


def test_a_run_ends_in_the_same_response_as_writes_that_landed(tmp_path, monkeypatch):
    pytest.importorskip("pydantic_ai")  # the `daemon` extra; agent-ci's plain shards lack it
    result, seen, probe = _run_writer(tmp_path, monkeypatch, [_ending("probe run tag r1 done", "tagged r1")], {})
    assert result.output.summary == "tagged r1"
    assert len(seen) == 1, "one model round: the write and the end together"
    assert probe.ran == [["run", "tag", "r1", "done"]]


def test_a_failed_write_in_the_ending_response_keeps_the_run_going(tmp_path, monkeypatch):
    pytest.importorskip("pydantic_ai")  # the `daemon` extra; agent-ci's plain shards lack it
    from pydantic_ai.messages import ModelResponse, ToolCallPart

    second = ModelResponse(parts=[ToolCallPart("final_result", {"summary": "tag failed: the run is gone"})])
    result, seen, _ = _run_writer(tmp_path, monkeypatch, [_ending("probe run tag r1 done", "tagged r1"), second],
                                  {"run tag": 1})
    assert result.output.summary == "tag failed: the run is gone", "the first end was suppressed"
    assert len(seen) == 2
    retry = _retries(result.all_messages())
    assert len(retry) == 1 and retry[0].startswith("Not ended: a write in this response did not land")
    assert "[exit 1]" in retry[0], "the model reads what the command answered"


def test_a_blocked_write_in_the_ending_response_keeps_the_run_going(tmp_path, monkeypatch):
    pytest.importorskip("pydantic_ai")  # the `daemon` extra; agent-ci's plain shards lack it
    from pydantic_ai.messages import ModelResponse, ToolCallPart

    second = ModelResponse(parts=[ToolCallPart("final_result", {"summary": "nothing new"})])
    result, seen, probe = _run_writer(tmp_path, monkeypatch, [_ending("probe session toggle", "toggled"), second],
                                      {})
    assert len(seen) == 2 and probe.ran == []
    assert "isn't the daemon's to run" in _retries(result.all_messages())[0]


def test_a_failed_write_answered_before_the_end_is_not_retried(tmp_path, monkeypatch):
    """The model read the failure (its own round), then ended: nothing is lost."""
    pytest.importorskip("pydantic_ai")  # the `daemon` extra; agent-ci's plain shards lack it
    from pydantic_ai.messages import ModelResponse, ToolCallPart

    first = ModelResponse(parts=[ToolCallPart("shell", {"command": "probe run tag r1 done"})])
    second = ModelResponse(parts=[ToolCallPart("final_result", {"summary": "tag failed"})])
    result, seen, _ = _run_writer(tmp_path, monkeypatch, [first, second], {"run tag": 1})
    assert len(seen) == 2 and _retries(result.all_messages()) == []


def test_a_write_that_keeps_failing_still_lets_the_run_end(tmp_path, monkeypatch):
    """On the tool's last attempt the end goes through: past it pydantic-ai
    would fail the whole run, and the next run's open-failures list shows it."""
    pytest.importorskip("pydantic_ai")  # the `daemon` extra; agent-ci's plain shards lack it
    result, seen, _ = _run_writer(tmp_path, monkeypatch, [_ending("probe run tag r1 done", "tagged r1")],
                                  {"run tag": 1})
    assert result.output.summary == "tagged r1"
    assert len(seen) == 3 and len(_retries(result.all_messages())) == 2


def test_a_tool_that_raised_in_the_ending_response_keeps_the_run_going(tmp_path, monkeypatch):
    """Review 10-13: a command whose tool raised (a folder gone, a process that
    could not start) may have been a write: the end waits for the model to see it."""
    pytest.importorskip("pydantic_ai")  # the `daemon` extra; agent-ci's plain shards lack it
    from pydantic_ai.messages import ModelResponse, ToolCallPart

    async def boom(deps, command, why=""):
        raise OSError("the working folder is gone")

    monkeypatch.setattr(tools, "shell", boom)
    second = ModelResponse(parts=[ToolCallPart("final_result", {"summary": "could not tag: folder gone"})])
    result, seen, _ = _run_writer(tmp_path, monkeypatch, [_ending("probe run tag r1 done", "tagged r1"), second], {})
    assert len(seen) == 2 and result.output.summary == "could not tag: folder gone"
    assert "OSError" in _retries(result.all_messages())[0]


def test_a_skipped_pipeline_that_writes_counts_as_lost(tmp_path, monkeypatch):
    """Review 10-13 (second pass): `probe <read> | tee FILE` writes through its
    filter; skipped after a failed `&&`, that write never ran."""
    monkeypatch.setattr(tools, "run_probe_process", Probe({"run get": 1}))
    deps = _deps(tmp_path, bypass=True)
    asyncio.run(tools.shell(deps, "probe run get missing && probe run list | tee result.json"))
    assert deps.lost_writes == 1
