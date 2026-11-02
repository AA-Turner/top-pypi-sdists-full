"""Inspect Robots (inspect-robots): evaluate Dreamscale models with `--policy dreamscale`.

`dreamscale integrations inspect-robots setup` installs Inspect Robots next to
Dreamscale, signs in if needed, and checks that Inspect Robots resolves the
`dreamscale` policy and `dreamscale_yam` embodiment this package registers (see
`inspect_robots_policy` and `inspect_robots_yam`). `plan_tasks` turns
`dreamscale run <robot> --inspect-robots` options into the tasks the attended runner
runs while `inspect_robots_recorder` writes their eval log.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from dreamscale import errors
from dreamscale.config import load_config

NAME = "inspect-robots"
EXTRA = "inspect-robots"
SETUP_COMMAND = "dreamscale integrations inspect-robots setup"
POLICY = "dreamscale"
RUN_EXAMPLE = (
    "dreamscale run yam --model molmoact2-bimanual-yam --inspect-robots "
    "--instruction \"fold the towel\""
)


def _registered(kind: str) -> dict:
    from inspect_robots.registry import registered

    return registered(kind)


def _login(*, print_fn: Callable[[str], None]) -> None:
    from dreamscale.quickstart import run_login

    run_login(api_key=None, print_fn=print_fn)


def signed_in() -> bool:
    """A key `--policy dreamscale` connects with: DREAMSCALE_API_KEY or the saved login."""
    return bool(load_config().api_key)


def run_setup(
    *,
    print_fn: Callable[[str], None] = print,
    login: Callable[..., None] = _login,
    registered: Callable[[str], dict] = _registered,
) -> None:
    """Sign in if needed, then confirm Inspect Robots can resolve `--policy dreamscale`."""
    if not signed_in():
        print_fn("Sign in to Dreamscale first.")
        login(print_fn=print_fn)
    if POLICY not in registered("policy"):
        raise errors.DreamscaleError(errors.ErrorInfo(
            "inspect_robots_plugin_missing",
            "Inspect Robots does not list the dreamscale policy",
            "Dreamscale and Inspect Robots are installed in different Python environments",
            "install Dreamscale where Inspect Robots runs: "
            'uv pip install "dreamscale[inspect-robots]"',
        ))
    print_fn(
        "✓ Inspect Robots can run Dreamscale models (--policy dreamscale) on your YAM rig "
        "(--embodiment dreamscale_yam)"
    )
    print_fn(f"  {RUN_EXAMPLE}")


@dataclass(frozen=True)
class TaskPlan:
    """What `dreamscale run <robot> --inspect-robots` runs: None asks for instructions."""

    instructions: str | list[str] | None
    # (scene id, instruction) per queued task, in order; empty for ad-hoc instructions.
    scenes: list[tuple[str, str]]
    max_actions: int | None
    task: str | None


def plan_tasks(*, instruction, task, epochs, max_actions, action_hz,
               resolve_task: Callable[[str], Any] | None = None) -> TaskPlan:
    """One instruction (repeated `epochs` times), a registered task's scenes × epochs,
    or, with neither, the usual instruction prompt."""
    if instruction is not None and task is not None:
        raise ValueError("Give --instruction or --task, not both.")
    if task is None:
        if epochs is not None and instruction is None:
            raise ValueError("--epochs repeats an --instruction or a --task.")
        repeats = epochs or 1
        instructions = (
            None if instruction is None
            else instruction if repeats == 1 else [instruction] * repeats
        )
        return TaskPlan(instructions, [], max_actions, None)
    if max_actions is not None:
        raise ValueError("--max-actions applies to --instruction; a --task sets its own horizon.")
    if resolve_task is None:
        from inspect_robots.registry import resolve

        def resolve_task(name):
            return resolve("task", name)

    try:
        spec = resolve_task(task)
    except Exception as exc:
        raise ValueError(f"No Inspect Robots task {task!r}: {exc}") from exc
    scenes = list(spec.scenes)
    repeats = epochs or getattr(spec.epochs, "epochs", spec.epochs) or 1
    horizon = spec.max_steps or math.ceil(spec.max_seconds * action_hz)
    # Scenes may share an instruction and differ only in setup, so keep each one.
    queue = [(scene.id, scene.instruction) for scene in scenes for _ in range(int(repeats))]
    return TaskPlan([instruction for _, instruction in queue], queue, int(horizon), task)
