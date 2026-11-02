"""
`seq.replay` - for a benchmark whose simulation the platform has no adapter for (`replay=seq.Replay(engine="own")`):
it hands the eval's 3D replay over itself. A MuJoCo, SAPIEN or Isaac benchmark writes `seq.Replay(state=...)` and never
calls these; the platform reads its simulation.

In one sentence: at each episode's start the benchmark gives the scene once (`scene`, a glTF binary whose nodes are flat
children of a root `seq_root` that turns Z-up into Y-up), and after its reset and after every step the world transform
of each node at that moment (`frame`) - the platform writes them into the episode's replay, which the owner's browser
draws after the eval.

The eval's machine installs where they go; anywhere else - a
local run, a test - they do nothing, so the same benchmark code runs everywhere.
"""
from __future__ import annotations

from typing import Any, Mapping, Optional, Sequence



_receiver: Optional[Any] = None


def _install(receiver: Optional[Any]) -> None:
    """Where `scene` and `frame` go (None: nowhere) - what the eval's machine sets `_receiver` to."""
    global _receiver
    _receiver = receiver


def scene(slot: int, glb: bytes) -> None:
    """The scene of the episode now starting in `slot` (any number for a benchmark that runs one environment): a glTF
    binary, its nodes flat children of `seq_root`, each named as `frame` names it. Given once an episode; the platform
    keeps one copy of the same bytes across episodes and evals."""
    if _receiver is not None:
        _receiver.scene(int(slot), bytes(glb))


def frame(slot: int, t: float, nodes: Sequence[str], pos: Any, quat: Any, step: Optional[int] = None,
          looks: Optional[Mapping[str, Mapping[str, Any]]] = None) -> None:
    """The scene in `slot` now: `t` seconds since its reset, `pos` [N, 3] metres in the world (Z up) and `quat` [N, 4]
    w x y z of the N `nodes`, named as in the scene and the same every frame of an episode; `step` the steps done (by
    default, as the platform counts them); `looks` what changes a node's look from this frame on, {node: {"rgba":
    [r, g, b, a]}} or {node: {"visible": False}}. Call it after the reset and after every step."""
    if _receiver is not None:
        _receiver.frame(int(slot), t, list(nodes), pos, quat, step=step, looks=dict(looks) if looks else None)


__all__ = ["scene", "frame"]
