"""The rig seam every attended embodiment implements.

A rig owns the local hardware for one robot (arms, cameras) and exposes exactly the
callbacks a policy run consumes, plus the stop/hold/home lifecycle the attended
runner drives. Units and action layout are the embodiment's own.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

import numpy as np

from dreamscale.policy.types import ActResult, RunContext


class RigFault(RuntimeError):
    """The rig refused a command or could not confirm its hold."""


@dataclass(frozen=True)
class MeasuredState:
    """One feedback read, flattened in action order, for recorders."""

    position: tuple[float, ...]
    velocity: tuple[float, ...] | None
    capture_unix_s: float


@runtime_checkable
class Rig(Protocol):
    """Hardware callbacks for policy.run, plus the attended stop/hold/home lifecycle.

    stop() blocks dispatch and commands a hold at the measured pose; it returns one
    entry per arm, True when that hold is confirmed. A rig whose hold is unconfirmed
    latches faulted and refuses to move again. home() returns the largest measured
    joint offset from home, or None when the rig has no home pose and only holds.
    """

    faulted: bool
    on_state: Callable[[MeasuredState], None] | None
    held_on_close: dict[str, bool]

    @property
    def has_home(self) -> bool: ...
    def open(self, *, attended: bool = False) -> Any: ...
    def observe(self, ctx: RunContext | None = None) -> Any: ...
    def act(self, action: Any, ctx: RunContext | None = None) -> ActResult: ...
    def read_hold_action(self, ctx: RunContext | None = None) -> tuple[float, ...]: ...
    def latest_frames(self) -> dict[str, np.ndarray]: ...
    def validate_action(self, action: Any, *, check_step: bool = True,
                        saturate: bool = False) -> Any: ...
    def action_limits(self) -> dict[str, list]: ...
    def metadata(self) -> dict[str, Any]: ...
    def enable_dispatch(self) -> None: ...
    def block_dispatch(self) -> None: ...
    async def home(self) -> float | None: ...
    def stop(self) -> dict[str, bool]: ...
    def close(self) -> None: ...
