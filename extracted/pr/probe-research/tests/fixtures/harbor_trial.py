"""Generate a synthetic Harbor trial from ONE timeline.

WHY THIS EXISTS
---------------

The `rl-ui-happy-path` fixture was hand-authored: someone wrote its
`result.json` phase timings and its `trajectory.json` step timestamps
separately, and they disagree. `agent_execution` starts at 18:15:05 while
`user turn 1` is stamped 18:15:00, so a turn precedes the phase that contains
it by five seconds. Every trial in it is exactly 120s on a 180s grid, which no
real trial is.

That is not a small blemish. It is the fixture people demo and design against,
so it exercised the containment clamp on every trial while real captures never
do -- the clamp stopped meaning "something is wrong" and started meaning "this
is the fixture". The team note names the general trap: *"Producer/consumer
mismatches hide behind hand-authored fixtures."*

The fix is structural, not a corrected set of numbers. A generator cannot
produce a disagreement it has no way to express::

    TrialScript  ──►  one advancing clock  ──┬──►  result.json   (phases)
                                             └──►  trajectory.json (steps)

Both artifacts are projections of the same cursor. A turn cannot fall outside
`agent_execution` because the cursor is inside that window when the turn is
emitted. Nothing here validates that afterwards; there is no code path that
could violate it.

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------

It does not round to whole seconds, and it does not lay trials out on a grid.
Real Harbor timings carry microseconds (the live `marshmallow-code__apispec`
trial has a 39-MICROSECOND seam between `environment_setup` and `agent_setup`),
and a fixture of tidy 120s trials on a 180s grid teaches every reader a shape
production does not have -- including the sub-millisecond seam that the gap
synthesis deliberately suppresses.

Run it to materialize a trial directory::

    python -m tests.fixtures.harbor_trial --out /tmp/trial-a
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

#: Sub-millisecond seams the way Harbor really records them. `_finalize` stamps
#: `finished_at` a hair after the phase it just closed, so consecutive phases
#: touch without being equal. Below `harbor_phases.MIN_GAP_MS`, so these must
#: NOT become gap spans -- which is exactly what makes them worth generating.
SEAM = timedelta(microseconds=39)


@dataclass(frozen=True)
class ToolCall:
    """One tool invocation inside a turn."""

    name: str
    arguments: dict
    result: str
    #: Wall clock from dispatch to result.
    seconds: float = 2.5
    call_id: str | None = None


@dataclass(frozen=True)
class Turn:
    """One trajectory step. ``seconds`` is the whole step including its calls."""

    source: str
    message: str
    seconds: float
    tool_calls: tuple[ToolCall, ...] = ()
    model_name: str | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None


@dataclass(frozen=True)
class TrialScript:
    """Everything that happened, in the order it happened.

    Every duration is a segment of one timeline. There is no field for "when a
    turn started" precisely because a caller must not be able to state one that
    contradicts the phase around it.
    """

    name: str
    task_name: str
    turns: tuple[Turn, ...]
    started_at: datetime = datetime(2026, 8, 5, 8, 49, 56, 441183, tzinfo=timezone.utc)
    agent_name: str = "claude-code"
    agent_version: str = "2.1.222"
    model_name: str = "claude-opus-5"
    reward: float | None = 1.0
    environment_setup_seconds: float = 1.723
    agent_setup_seconds: float = 17.859
    #: Trial orchestration between `_prepare()` finishing and AGENT_START.
    pre_agent_seconds: float = 1.287
    #: `_sync_agent_output` pulling the agent's transcript out of the sandbox.
    log_download_seconds: float = 2.725
    verifier_seconds: float = 10.760
    #: `_stop_agent_environment()` before `finished_at` is stamped.
    teardown_seconds: float = 10.824
    environment: dict = field(
        default_factory=lambda: {"image": "synthetic:fixture", "backend": "docker"}
    )


def _iso(moment: datetime) -> str:
    return moment.isoformat().replace("+00:00", "Z")


class _Clock:
    """A cursor that only moves forward. The single source of every stamp."""

    def __init__(self, start: datetime):
        self.now = start

    def advance(self, seconds: float) -> datetime:
        self.now = self.now + timedelta(seconds=seconds)
        return self.now

    def seam(self) -> datetime:
        self.now = self.now + SEAM
        return self.now


def build(script: TrialScript) -> dict:
    """``{"result": ..., "trajectory": ..., "session": ...}`` for one trial.

    The three artifacts a captured Harbor trial carries, all projected from one
    cursor: phase timings, the ATIF document, and the agent transcript whose
    `tool_result` stamps give tool calls their measured ends.
    """
    clock = _Clock(script.started_at)
    trial_started = clock.now

    env_start = clock.now
    env_end = clock.advance(script.environment_setup_seconds)
    setup_start = clock.seam()
    setup_end = clock.advance(script.agent_setup_seconds)

    clock.advance(script.pre_agent_seconds)
    agent_start = clock.now

    steps: list[dict] = []
    session: list[dict] = []
    for index, turn in enumerate(script.turns, start=1):
        step_at = clock.now
        step: dict = {
            "step_id": index,
            "source": turn.source,
            "message": turn.message,
            "timestamp": _iso(step_at),
        }
        if turn.source == "agent":
            step["model_name"] = turn.model_name or script.model_name
            metrics = {
                "prompt_tokens": turn.prompt_tokens,
                "completion_tokens": turn.completion_tokens,
            }
            if any(value is not None for value in metrics.values()):
                step["metrics"] = {k: v for k, v in metrics.items() if v is not None}

        if turn.tool_calls:
            calls, results, blocks = [], [], []
            for position, call in enumerate(turn.tool_calls):
                call_id = call.call_id or f"toolu_{index:02d}{position:02d}"
                calls.append(
                    {
                        "tool_call_id": call_id,
                        "function_name": call.name,
                        "arguments": call.arguments,
                    }
                )
                results.append({"source_call_id": call_id, "content": call.result})
                blocks.append(
                    {
                        "type": "tool_use",
                        "id": call_id,
                        "name": call.name,
                        "input": call.arguments,
                    }
                )
            step["tool_calls"] = calls
            step["observation"] = {"results": results}
            # The transcript's dispatch instant IS the step's stamp: Claude Code
            # writes the assistant message that carries every tool_use block at
            # one moment, which is why a batch shares a start.
            session.append(
                {
                    "type": "assistant",
                    "timestamp": _iso(step_at),
                    "message": {"role": "assistant", "content": blocks},
                }
            )
            for call, entry in zip(turn.tool_calls, calls):
                done = step_at + timedelta(seconds=call.seconds)
                session.append(
                    {
                        "type": "user",
                        "timestamp": _iso(done),
                        "message": {
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": entry["tool_call_id"],
                                    "content": call.result,
                                }
                            ],
                        },
                    }
                )
        steps.append(step)
        clock.advance(turn.seconds)

    agent_end = clock.now
    clock.advance(script.log_download_seconds)
    verifier_start = clock.now
    verifier_end = clock.advance(script.verifier_seconds)
    clock.advance(script.teardown_seconds)
    trial_finished = clock.now

    result: dict = {
        "trial_name": script.name,
        "task_name": script.task_name,
        "started_at": _iso(trial_started),
        "finished_at": _iso(trial_finished),
        "agent_info": {"name": script.agent_name, "version": script.agent_version},
        "environment_setup": {
            "started_at": _iso(env_start),
            "finished_at": _iso(env_end),
        },
        "agent_setup": {
            "started_at": _iso(setup_start),
            "finished_at": _iso(setup_end),
        },
        "agent_execution": {
            "started_at": _iso(agent_start),
            "finished_at": _iso(agent_end),
        },
        "verifier": {
            "started_at": _iso(verifier_start),
            "finished_at": _iso(verifier_end),
        },
    }
    if script.reward is not None:
        result["verifier_result"] = {"reward": script.reward}

    trajectory = {
        "schema_version": "ATIF-v1.7",
        "session_id": f"{script.name}-session",
        "agent": {
            "name": script.agent_name,
            "version": script.agent_version,
            "model_name": script.model_name,
        },
        "steps": steps,
    }
    return {"result": result, "trajectory": trajectory, "session": session}


def write(script: TrialScript, root: Path) -> Path:
    """Materialize a Harbor trial directory the real connector can capture."""
    built = build(script)
    root.mkdir(parents=True, exist_ok=True)
    (root / "result.json").write_text(json.dumps(built["result"], indent=2))
    (root / "config.json").write_text(
        json.dumps({"task": {"name": script.task_name}}, indent=2)
    )
    agent_dir = root / "agent"
    agent_dir.mkdir(exist_ok=True)
    (agent_dir / "trajectory.json").write_text(json.dumps(built["trajectory"], indent=2))
    # Where Harbor puts Claude Code's transcript, which is where the measured
    # tool-call ends are read back from.
    sessions = agent_dir / "sessions" / "projects" / "-testbed"
    sessions.mkdir(parents=True, exist_ok=True)
    (sessions / f"{script.name}.jsonl").write_text(
        "\n".join(json.dumps(event) for event in built["session"]) + "\n"
    )
    verifier = root / "logs" / "verifier"
    verifier.mkdir(parents=True, exist_ok=True)
    (verifier / "test-console-output.txt").write_text("2 passed\n")
    return root


#: The happy-path shape `rl-ui-happy-path` was trying to be, generated instead
#: of authored. Tool-heavy so the session transcript carries a batch AND a
#: solitary call, which are the two dispatch shapes the timing recovery reports
#: differently.
HAPPY_PATH = TrialScript(
    name="synthetic__refactor-calculator__s0",
    task_name="probe/rl-ui/refactor-calculator",
    turns=(
        Turn("user", "Refactor the calculator parser to reject blank values.", 2.653),
        Turn(
            "agent",
            "I will trace the parser and its tests before editing.",
            4.978,
            tool_calls=(
                ToolCall("rg", {"pattern": "def parse|test_parse"}, "src/calculator.py:1", 0.412),
                ToolCall("read_file", {"path": "src/calculator.py"}, "parse() passes raw values to int()", 1.244),
            ),
            prompt_tokens=920,
            completion_tokens=180,
        ),
        Turn(
            "agent",
            "The patch is applied; running the focused tests.",
            35.193,
            tool_calls=(
                ToolCall("bash_command", {"command": "pytest tests/test_calculator.py -q"}, "2 passed", 2.650),
            ),
            prompt_tokens=1180,
            completion_tokens=130,
        ),
    ),
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--name", default=HAPPY_PATH.name)
    args = parser.parse_args()
    root = write(TrialScript(**{**HAPPY_PATH.__dict__, "name": args.name}), args.out)
    print(root)


if __name__ == "__main__":  # pragma: no cover - operator entry point
    main()
