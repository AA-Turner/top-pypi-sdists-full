"""Every GPU process gets the command (agentic W&B C.1, Codex O4). Rank 0 claims a run's commands; a checkpoint under
DeepSpeed or FSDP is a collective and an LR change on one rank splits the model, so the claimed commands go to every
rank in one small `all_gather_object`, and every rank acts on the same step. Torch is only read when the script
already imported it. Why: DESIGN.md "Every rank"."""

from __future__ import annotations

import sys
from datetime import timedelta
from typing import Any

#: The integrations share every this many steps (a collective per step would cost every step).
SHARE_EVERY_STEPS = 20


def get_world() -> tuple[int, int]:
    """This process's (rank, world size) in torch.distributed, or (0, 1) when it is not running (or not imported)."""
    dist = _get_dist()
    if dist is None:
        return 0, 1
    return int(dist.get_rank()), int(dist.get_world_size())


def send_to_every_rank(commands: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    """Every rank's commands, on every rank, in rank order: one `all_gather_object`. Rank 0 passes what it claimed
    and the others usually nothing, but a rank that claimed before torch.distributed numbered it passes its own, so
    no claimed command is left in one process. A single process gets them back as they are. Every rank must call it
    at the same point, or the job hangs."""
    dist = _get_dist()
    if dist is None:
        return list(commands or [])
    gathered: list[Any] = [None] * dist.get_world_size()
    dist.all_gather_object(gathered, list(commands or []))
    return [command for part in gathered for command in part or []]


#: Each rank whose integration can take commands says so in the process group's store; rank 0 decides once.
_READY_KEY = "probe/commands/ready/{rank}"
_MODE_KEY = "probe/commands/mode"
#: How long a rank above 0 waits for rank 0's decision at the first hand-off step.
MODE_WAIT_SECONDS = 60.0
#: Why rank 0 cannot hand a command on: a rank runs without the integration.
NOT_EVERY_RANK = ("not every rank of this {world}-process job runs the integration (it is on rank 0 only?): add it "
                  "on every rank, or call probe.commands.sync() on every rank")  # fmt: skip


class RankChannel:
    """An integration's hand-off of rank 0's commands to every rank, at a step every rank reaches.

    Never a hang when the integration runs on rank 0 only (a common shape): every rank that runs it says so in the
    store at train begin (`announce`, one set); at the first hand-off step rank 0 checks that every rank said so
    and writes its decision, which the others read (waiting at most `MODE_WAIT_SECONDS`). Only when every rank
    said so do they broadcast; otherwise rank 0 refuses what needs every rank, saying why."""

    def __init__(self) -> None:
        self._is_shared: bool | None = None

    def announce(self) -> None:
        dist = _get_dist()
        store = _get_store(dist)
        if store is not None:
            _try(lambda: store.set(_READY_KEY.format(rank=dist.get_rank()), "1"))

    def is_handoff(self, step: int) -> bool:
        """Whether this step hands commands on: every step for one process, every `SHARE_EVERY_STEPS` for many."""
        return _get_dist() is None or (step > 0 and step % SHARE_EVERY_STEPS == 0)

    def exchange(self, mine: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], str | None]:
        """At a hand-off step on every rank: the commands to act on here, and (rank 0) why `mine` cannot reach every
        rank, when it cannot."""
        dist = _get_dist()
        if dist is None:
            return list(mine), None
        if self._is_shared is None:
            self._is_shared = self._decide(dist)
        if self._is_shared:
            return send_to_every_rank(mine), None
        return [], NOT_EVERY_RANK.format(world=dist.get_world_size())

    def _decide(self, dist: Any) -> bool:
        store = _get_store(dist)
        if store is None:
            return False
        if dist.get_rank() == 0:
            keys = [_READY_KEY.format(rank=rank) for rank in range(dist.get_world_size())]
            is_shared = bool(_try(lambda: store.check(keys)))
            _try(lambda: store.set(_MODE_KEY, "1" if is_shared else "0"))
            return is_shared
        waited = _try(lambda: store.wait([_MODE_KEY], timedelta(seconds=MODE_WAIT_SECONDS)) or True)
        return bool(waited) and _try(lambda: store.get(_MODE_KEY)) == b"1"


def _get_store(dist: Any) -> Any:
    if dist is None:
        return None
    return _try(lambda: dist.distributed_c10d._get_default_store())


def _try(call: Any) -> Any:
    try:
        return call()
    except Exception:  # noqa: BLE001 -- a store that fails costs the hand-off, never the training
        return None


def _get_dist() -> Any:
    torch = sys.modules.get("torch")
    if torch is None:
        return None
    dist = getattr(torch, "distributed", None)
    if dist is None or not dist.is_available() or not dist.is_initialized() or dist.get_world_size() <= 1:
        return None
    return dist


__all__ = ["MODE_WAIT_SECONDS", "NOT_EVERY_RANK", "SHARE_EVERY_STEPS", "RankChannel", "get_world", "send_to_every_rank"]
