"""tool_loop: verl's agent loop messages as the loop built them (tool calls with ids and arguments, results linked by
`tool_call_id`, reasoning apart), each call's run, and the files the rollout's tools and reward function attach, on
the rollout's own generator part (RL sample capture D1-D13, F0-F5). Nothing here imports verl until it runs.
Why: ../DESIGN.md "Tool loop capture"."""

from __future__ import annotations

from typing import Any

from .plan import build_unsupported
from .recording import LoopRecording, get_recording
from .stamps import FINISH_FIELD, ROLLOUT_EVAL_FIELD, ROLLOUT_FIELD, read_stamp, to_stamp

__all__ = [
    "FINISH_FIELD",
    "ROLLOUT_EVAL_FIELD",
    "ROLLOUT_FIELD",
    "LoopRecording",
    "build_unsupported",
    "get_recording",
    "open_recording",
    "read_stamp",
    "to_stamp",
    "watch_tool_loop_imports",
]


def open_recording(run: Any, attempt_key: str) -> LoopRecording:
    """One agent loop's recording: a `RolloutCapture` for ``attempt_key`` on ``run`` (the worker's joined run)."""
    from probe.sdk.run.samples.rollout import RolloutCapture

    return LoopRecording(RolloutCapture(run, attempt_key))


def watch_tool_loop_imports() -> None:
    """Wrap `ToolAgentLoop`, the hermes parser and `RewardLoopWorker` the moment each module loads in this process
    (now, when it already has). Ray's setup hook calls it in every worker."""
    from probe.sdk.run.samples.points import watch_import

    from . import parser, reward, tool_loop

    for module_name, install in ((tool_loop.TOOL_LOOP_MODULE, tool_loop.install),
                                 (parser.PARSER_MODULE, parser.install), (reward.REWARD_LOOP_MODULE, reward.install)):
        watch_import(module_name, install, framework="verl")
