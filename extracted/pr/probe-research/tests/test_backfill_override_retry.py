"""One relaunch, without the override, when an agent refuses a setting at start.

The server can name a model or an effort an account cannot use: a model an API
key runs is refused for a ChatGPT account. The agent says so in about four
seconds with no output tokens, and the import must not fail over it. But the
relaunch is only safe in a narrow case, and every edge of it is pinned here:

  * an override was actually sent (the lane's builtin value would not have);
  * the agent's own structured error names that setting;
  * it refused before any tool call or work item, so nothing was written
    (a classifier files decisions as it goes).

Anything else, or a second failure, is the failure it always was.

A real subprocess, not a mock: the agent is a script that prints the lines the
real agents printed (`recorded_agent_events`) depending on its argv, and logs
each argv it was started with.
"""

from __future__ import annotations

import json
import sys

import pytest

from probe.cli import backfill as bf
from probe.cli import import_agent_settings as settings_mod
from probe.cli.import_agent_settings import Lane, LaneSettings, Meter, Source
from recorded_agent_events import (
    CLAUDE_BAD_MODEL,
    CLAUDE_OK,
    CODEX_BAD_EFFORT,
    CODEX_BAD_MODEL,
    CODEX_OK,
)

_TOOL_CALL = json.dumps({"type": "item.started", "item": {
    "id": "item_1", "type": "command_execution", "command": "/bin/bash -lc 'probe-backfill-plan assign'",
}})
_UNRELATED = json.dumps({"type": "turn.failed", "error": {"message": json.dumps({
    "type": "error", "status": 400, "error": {
        "type": "invalid_request_error", "code": "context_length_exceeded",
        "message": "Your input exceeds the context window of this model.",
    },
})}})

#: The settings these tests send. `sonnet` is not one: it is the record lane's
#: builtin model, the fallback.
_OVERRIDES = ("gpt-6-astra", "opus", 'model_reasoning_effort="xhigh"', 'model_reasoning_effort="low"')

_AGENT = """#!{python}
import json, sys
from pathlib import Path
here = Path(__file__).parent
argv = sys.argv[1:]
with open(here / "argv.jsonl", "a") as log:
    log.write(json.dumps(argv) + "\\n")
sys.stdin.read()
script = json.loads((here / "script.json").read_text())
lines, code = script["override" if set(argv) & set(script["refuse"]) else "plain"]
effort = next((a.split("=", 1)[1].strip('"') for a in argv if a.startswith("model_reasoning_effort=")), "")
for line in lines:
    print(line.replace("'bogus'", "'" + effort + "'") if effort else line, flush=True)
sys.exit(code)
"""


@pytest.fixture
def agent(tmp_path, monkeypatch):
    """A scripted agent binary; `agent(override=(lines, code), plain=(lines, code))`."""
    binary = tmp_path / "agent" / "fake-agent"
    binary.parent.mkdir()
    binary.write_text(_AGENT.format(python=sys.executable))
    binary.chmod(0o755)
    monkeypatch.setattr(bf, "which_agent", lambda _agent: str(binary))
    monkeypatch.setattr(bf, "supported_flags", lambda *_a, **_k: None)  # unknown: every flag passes
    monkeypatch.setattr(bf, "codex_features", lambda _binary: None)

    def script(*, override, plain=(CODEX_OK, 0), refuse=_OVERRIDES):
        """`override` answers a launch carrying any argv element in `refuse`."""
        (binary.parent / "script.json").write_text(json.dumps(
            {"override": override, "plain": plain, "refuse": list(refuse)}))

    def launches() -> list[list[str]]:
        log = binary.parent / "argv.jsonl"
        return [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []

    script.launches = launches
    return script


def _launch(tmp_path, *, agent=bf.Agent.CODEX, settings=None, meter=None, **kwargs):
    folder = tmp_path / "folder"
    folder.mkdir(exist_ok=True)
    return bf.launch_agent(
        folder, "file these", agent=agent, workdir=folder, progress=False,
        stream=open("/dev/null", "w"), settings=settings, meter=meter, **kwargs,
    )


def _codex(lane=Lane.CLASSIFY, **fields) -> LaneSettings:
    return LaneSettings(lane, source=Source.SERVER, **fields)


def test_a_refused_model_relaunches_once_without_it(agent, tmp_path):
    agent(override=(CODEX_BAD_MODEL, 1))
    meter = Meter()
    ok, tail = _launch(tmp_path, settings=_codex(model="gpt-6-astra"), meter=meter)
    first, second = agent.launches()
    assert ok and '"turn.completed"' in tail
    assert first[first.index("-m") + 1] == "gpt-6-astra"
    assert "-m" not in second, "the relaunch carries no override"
    counts = meter.properties()
    assert counts["classify_launches"] == 2 and counts["classify_rejected"] == 1
    assert counts["classify_usage_missing"] == 1, "the refused launch reported no usage"
    assert counts["classify_input_tokens"] == 30047


def test_a_refused_effort_relaunches_once_without_it(agent, tmp_path):
    agent(override=(CODEX_BAD_EFFORT, 1))
    ok, _ = _launch(tmp_path, settings=_codex(effort="xhigh"))
    first, second = agent.launches()
    assert ok
    assert 'model_reasoning_effort="xhigh"' in first
    assert not any(a.startswith("model_reasoning_effort=") for a in second)


def test_no_relaunch_without_an_override(agent, tmp_path):
    """The agent's own configured model failing is not ours to work around."""
    agent(override=(CODEX_BAD_MODEL, 1), plain=(CODEX_BAD_MODEL, 1))
    meter = Meter()
    ok, _ = _launch(tmp_path, settings=_codex(), meter=meter)
    assert not ok and len(agent.launches()) == 1
    assert meter.properties()["classify_rejected"] == 0
    ok, _ = _launch(tmp_path)  # no settings at all: today's launch
    assert not ok and len(agent.launches()) == 2


def test_no_relaunch_after_the_agent_has_done_work(agent, tmp_path):
    """A classifier files decisions as it goes; replaying it would build on a
    half-written plan."""
    agent(override=([_TOOL_CALL, *CODEX_BAD_MODEL], 1))
    ok, _ = _launch(tmp_path, settings=_codex(model="gpt-6-astra"))
    assert not ok and len(agent.launches()) == 1


def test_no_relaunch_for_an_error_that_does_not_name_the_setting(agent, tmp_path):
    agent(override=([_UNRELATED], 1))
    ok, _ = _launch(tmp_path, settings=_codex(model="gpt-6-astra", effort="low"))
    assert not ok and len(agent.launches()) == 1


def test_no_relaunch_when_the_refused_setting_was_not_the_one_sent(agent, tmp_path):
    """An effort override, but the agent refuses its own configured model."""
    agent(override=(CODEX_BAD_MODEL, 1))
    ok, _ = _launch(tmp_path, settings=_codex(effort="low"))
    assert not ok and len(agent.launches()) == 1


def test_a_relaunch_that_fails_too_is_the_ordinary_failure(agent, tmp_path):
    agent(override=(CODEX_BAD_MODEL, 1), plain=(["agent exited"], 1))
    ok, tail = _launch(tmp_path, settings=_codex(model="gpt-6-astra"))
    assert not ok and tail == "agent exited"
    assert len(agent.launches()) == 2, "once, never a loop"


def test_claude_relaunches_under_a_fresh_session(agent, tmp_path):
    """A refused Claude session may already exist under its id, and the caller
    is told the new one (a revision resumes the session that has the evidence)."""
    agent(override=(CLAUDE_BAD_MODEL, 1), plain=(CLAUDE_OK, 0))
    told = []
    ok, _ = _launch(
        tmp_path, agent=bf.Agent.CLAUDE, session_id="11111111-1111-4111-8111-111111111111",
        settings=_codex(model="opus"), on_relaunch=told.append,
    )
    first, second = agent.launches()
    assert ok
    assert first[first.index("--model") + 1] == "opus" and "--model" not in second
    fresh = second[second.index("--session-id") + 1]
    assert fresh != "11111111-1111-4111-8111-111111111111" and told == [fresh]


def test_a_refused_record_model_falls_back_to_the_lanes_builtin_model(agent, tmp_path):
    """The fallback is what the lane ran with before any setting: Claude records
    on sonnet, not on no model at all."""
    agent(override=(CLAUDE_BAD_MODEL, 1), plain=(CLAUDE_OK, 0))
    agents = settings_mod.resolve(
        None, bf.Agent.CLAUDE, environ={settings_mod.ENV_VAR: '{"claude": {"record": {"model": "opus"}}}'},
    )
    ok, _ = _launch(tmp_path, agent=bf.Agent.CLAUDE, settings=agents.lane(Lane.RECORD))
    first, second = agent.launches()
    assert ok
    assert first[first.index("--model") + 1] == "opus"
    assert second[second.index("--model") + 1] == "sonnet"


def test_a_cancelled_import_is_not_relaunched(agent, tmp_path):
    import threading

    agent(override=(CODEX_BAD_MODEL, 1))
    cancel = threading.Event()

    class CancelOnRefusal(Meter):
        def launched(self, lane, usage):
            super().launched(lane, usage)
            cancel.set()

    ok, _ = _launch(tmp_path, settings=_codex(model="gpt-6-astra"), meter=CancelOnRefusal(),
                    cancel_event=cancel)
    assert not ok and len(agent.launches()) == 1
