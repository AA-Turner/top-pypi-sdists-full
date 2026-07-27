"""Item #21 — Replay session against a different model."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from sage.core.session_recorder import replay

__all__ = ["replay_with_model", "ReplayResult"]

SendFn = Callable[..., str]


@dataclass
class ReplayResult:
    session_id: str
    model: str
    prompts_replayed: int
    outputs: list[str]


def replay_with_model(*,
                      session_id: str,
                      model: str,
                      send_fn: SendFn,
                      system: str = "") -> ReplayResult:
    outputs: list[str] = []
    n = 0
    for ev in replay(session_id=session_id):
        if ev.kind != "user":
            continue
        try:
            out = send_fn(ev.prompt, model=model, system=system)
        except Exception as exc:
            out = f"[error: {exc}]"
        outputs.append(out)
        n += 1
    return ReplayResult(
        session_id=session_id, model=model,
        prompts_replayed=n, outputs=outputs,
    )
