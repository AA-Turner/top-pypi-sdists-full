"""Mandate-candidate taps — the host seam that lets a HOST observe real mandate runs.

A mandate *candidate* (common-docs/systems/intelligence/mandates/projects/mandate-candidates/REGISTER.md) re-runs a
real mandate run through a different Holder in the background. To do that the
host must see each real run: its input BEFORE the door mutates it, the ids it
ran under, the exact model-facing result of every tool call (so the candidate
can borrow them, P12), what the first provider call carried (the input digest,
P10), and how the run ended. matrx-ai never imports its host, so this module is
the seam, in three parts:

* :func:`tapped_door` — wraps one run DOOR (``run_mandated``, the Run Mandate
  workflow step, and the host's own doors). ``begin`` copies the input and must
  be synchronous and cheap; ``finish`` hands the outcome over and must be
  synchronous (the host schedules its own background work). No tap installed →
  the door runs untouched.
* :func:`observe_first_send` — called by ``send_once`` before the send boundary.
* :func:`observe_tool_results` — called by ``handle_tool_calls_v2`` after a
  batch, with the model-facing ``content`` dicts.

THE ONE RULE: a tap can never change, block, slow down or fail the run it
observes. Every host call here is wrapped; an exception is logged and
swallowed, and the run proceeds exactly as if no tap existed. The door's own
result and exception are passed through untouched.
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any, Protocol

logger = logging.getLogger(__name__)

class DoorTapHandle(Protocol):
    def finish(self, result: Any, error: BaseException | None) -> None: ...


class DoorTap(Protocol):
    def begin(
        self, door: str, mandate_key: str, snapshot: Callable[[], dict[str, Any]]
    ) -> DoorTapHandle | None: ...


class LiveRunObserver(Protocol):
    def first_send(self, request: Any, iteration: int | None) -> None: ...

    def tool_results(
        self,
        calls: list[dict[str, Any]],
        content_results: list[dict[str, Any]],
        full_results: list[Any],
    ) -> None: ...


class MandateReplay(Protocol):
    """The host's TEST-MODE answer source for a mandate step (aidream: ``services/runtime/ai_test_mode.py``).

    Unlike a tap, this one CAN answer instead of the real run — so it is the opposite of silent: the
    host decides everything (who, when, which mode), and an answer it returns must carry its own loud
    ``ai_test_replay`` stamp. ``lookup`` returns an ``AiExecutionResult``-shaped dict or None (= run
    for real); ``store`` is offered the real result afterwards. Not installed (every package test,
    every host that never opts in) → both are skipped and the step is exactly the real one.
    """

    async def lookup(
        self, door: str, mandate_key: str, run_id: str | None, fingerprint: dict[str, Any]
    ) -> dict[str, Any] | None: ...

    async def store(
        self, door: str, mandate_key: str, run_id: str | None, fingerprint: dict[str, Any],
        result: dict[str, Any],
    ) -> None: ...


_DOOR_TAP: DoorTap | None = None
_OBSERVER: LiveRunObserver | None = None
_REPLAY: MandateReplay | None = None


def set_mandate_replay(replay: MandateReplay | None) -> None:
    """Install (or clear) the host's test-mode answer source. Called once at host startup."""
    global _REPLAY
    _REPLAY = replay


async def replay_lookup(
    door: str, mandate_key: str, run_id: str | None, fingerprint: dict[str, Any]
) -> dict[str, Any] | None:
    """The host's test-mode answer for this exact step, or None. A broken seam is a miss — the real
    run follows — never a failed step."""
    replay = _REPLAY
    if replay is None:
        return None
    try:
        return await replay.lookup(door, mandate_key, run_id, fingerprint)
    except Exception:  # noqa: BLE001 — a broken test seam is a miss, never a failed run
        logger.exception("[mandate replay] lookup failed for %s %s — the real run follows", door, mandate_key)
        return None


async def replay_store(
    door: str, mandate_key: str, run_id: str | None, fingerprint: dict[str, Any], result: dict[str, Any]
) -> None:
    replay = _REPLAY
    if replay is None:
        return
    try:
        await replay.store(door, mandate_key, run_id, fingerprint, result)
    except Exception:  # noqa: BLE001 — the real result is already in hand; never lose it
        logger.exception("[mandate replay] store failed for %s %s — result not saved", door, mandate_key)


def set_mandate_door_tap(tap: DoorTap | None) -> None:
    """Install (or clear) the host's door tap. Called once at host startup."""
    global _DOOR_TAP
    _DOOR_TAP = tap


def get_mandate_door_tap() -> DoorTap | None:
    return _DOOR_TAP


def set_live_run_observer(observer: LiveRunObserver | None) -> None:
    """Install (or clear) the host's send / tool-result observer."""
    global _OBSERVER
    _OBSERVER = observer


def get_live_run_observer() -> LiveRunObserver | None:
    return _OBSERVER


async def tapped_door[T](
    door: str,
    mandate_key: str,
    snapshot: Callable[[], dict[str, Any]],
    run: Callable[[], Awaitable[T]],
) -> T:
    """Run ``run()`` as one observed mandate door. Never alters the run."""
    tap = _DOOR_TAP
    if tap is None:
        return await run()
    handle: DoorTapHandle | None = None
    try:
        handle = tap.begin(door, mandate_key, snapshot)
    except Exception:  # noqa: BLE001 — a tap never touches the run
        logger.exception("[mandate taps] begin failed for %s %s — the run is untouched", door, mandate_key)
        handle = None
    if handle is None:
        return await run()
    try:
        result = await run()
    except BaseException as exc:
        _finish(handle, None, exc, door, mandate_key)
        raise
    _finish(handle, result, None, door, mandate_key)
    return result


def _finish(
    handle: DoorTapHandle, result: Any, error: BaseException | None, door: str, mandate_key: str
) -> None:
    try:
        handle.finish(result, error)
    except Exception:  # noqa: BLE001 — a tap never touches the run
        logger.exception("[mandate taps] finish failed for %s %s — the run is untouched", door, mandate_key)


def observe_first_send(request: Any, iteration: int | None) -> None:
    observer = _OBSERVER
    if observer is None:
        return
    try:
        observer.first_send(request, iteration)
    except Exception:  # noqa: BLE001 — observation never touches the send
        logger.exception("[mandate taps] first_send observer failed — the send is untouched")


def observe_tool_results(
    calls: list[dict[str, Any]],
    content_results: list[dict[str, Any]],
    full_results: list[Any],
) -> None:
    observer = _OBSERVER
    if observer is None:
        return
    try:
        observer.tool_results(calls, content_results, full_results)
    except Exception:  # noqa: BLE001 — observation never touches the tool loop
        logger.exception("[mandate taps] tool_results observer failed — the loop is untouched")


__all__ = [
    "DoorTap",
    "DoorTapHandle",
    "LiveRunObserver",
    "MandateReplay",
    "get_live_run_observer",
    "get_mandate_door_tap",
    "observe_first_send",
    "observe_tool_results",
    "replay_lookup",
    "replay_store",
    "set_live_run_observer",
    "set_mandate_replay",
    "set_mandate_door_tap",
    "tapped_door",
]
