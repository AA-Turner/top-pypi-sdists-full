"""Debug-agent value objects."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPLAY_DELAY_SEC = 2.0
REAL_ACTIONS_PER_STEP = 2
REAL_TYPE_LEN = 100
REAL_EXEC_SLEEP_SEC = 2.0

DESKTOP_ACTION_POOL = (
    "click",
    "type",
    "scroll",
    "hotkey",
    "move",
    "press",
    "drag",
    "rclick",
)
IOS_ACTION_POOL = ("tap", "long_press", "swipe", "type", "button", "tap", "swipe")


@dataclass(frozen=True)
class ReplayAction:
    function: str
    args: dict[str, Any]

    @classmethod
    def from_raw(cls, raw: dict[str, Any]) -> ReplayAction:
        function = str(raw.get("function") or "")
        if not function:
            raise ValueError(f"replay action missing function: {raw}")
        args = raw.get("args") or {}
        if not isinstance(args, dict):
            raise ValueError(f"replay action args must be a dict: {raw}")
        return cls(function=function, args=args)

    @property
    def is_type(self) -> bool:
        return self.function in {"type", "type_text"}

    @property
    def label(self) -> str:
        return f"{self.function}({self.args})"


def load_replay_actions(
    task_dir: Path | None, *, coalesce_ios_types: bool = False
) -> list[ReplayAction]:
    actions_path = task_dir / "actions.json" if task_dir else None
    if actions_path is None or not actions_path.exists():
        raise RuntimeError(f"replay: actions.json missing at {actions_path}; re-export the task")

    data = json.loads(actions_path.read_text())
    actions = [ReplayAction.from_raw(raw) for raw in data.get("steps", []) if isinstance(raw, dict)]
    if coalesce_ios_types:
        return coalesce_type_runs(actions)
    return actions


def coalesce_type_runs(actions: list[ReplayAction]) -> list[ReplayAction]:
    out: list[ReplayAction] = []
    index = 0
    while index < len(actions):
        action = actions[index]
        if not action.is_type:
            out.append(action)
            index += 1
            continue

        text = str(action.args.get("text", ""))
        next_index = index + 1
        while next_index < len(actions) and actions[next_index].is_type:
            text += str(actions[next_index].args.get("text", ""))
            next_index += 1
        out.append(ReplayAction("type_text", {"text": text}))
        index = next_index
    return out


def rotating_actions(pool: tuple[str, ...], step: int) -> list[str]:
    start = ((step - 1) * REAL_ACTIONS_PER_STEP) % len(pool)
    return [pool[(start + idx) % len(pool)] for idx in range(REAL_ACTIONS_PER_STEP)]
