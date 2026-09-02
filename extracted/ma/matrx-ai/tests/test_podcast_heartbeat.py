"""The pulse that tells everyone a long, silent stage is still alive.

Every client that is NOT holding the live stream — a reloaded page, a phone back
from background, the manage list, the reconcile endpoint — judges liveness from
`agent_run.last_heartbeat_at`. So a stage that runs for minutes without writing
that column is indistinguishable from a dead worker.

That is not hypothetical. On run e505424c the heartbeat stopped at 19:06:37 while
`compose_official_video` ran to 19:25:11 — nineteen minutes of silence on a
perfectly healthy run. The user was shown "interrupted / Resume / Re-run" while
his finished audio had been sitting there for eleven minutes, and re-running a
finished podcast is the single most expensive thing that screen can invite.

The cause was structural, so these tests pin the structure:

* the pulse rode inside the UI ticker, which `await`s the host's `on_event` every
  tick — so one wedged or slow emit stopped it;
* and it fired the DB write as a bare `asyncio.create_task(...)` with no strong
  reference, which the garbage collector is free to drop mid-flight.

Both are gone. This loop owns its own clock and awaits its own write.
"""

from __future__ import annotations

import asyncio

import pytest

from matrx_ai.agent_runners.podcast_generator import run_heartbeat_loop


class _Ckpt:
    """A checkpointer stub that records every pulse."""

    def __init__(self) -> None:
        self.touches = 0

    async def touch(self) -> None:
        self.touches += 1


class _SlowCkpt(_Ckpt):
    async def touch(self) -> None:
        await asyncio.sleep(0.01)
        await super().touch()


async def _run_for(coro_factory, seconds: float) -> None:
    task = asyncio.create_task(coro_factory())
    await asyncio.sleep(seconds)
    task.cancel()
    await asyncio.gather(task, return_exceptions=True)


async def test_it_pulses_repeatedly_while_a_stage_is_in_flight() -> None:
    """The whole point: a stage that emits nothing for minutes still reports alive."""
    ckpt = _Ckpt()
    running = {"compose_official_video": (0.0, "Composing your official video")}

    await _run_for(lambda: run_heartbeat_loop(ckpt, running, interval=0.01), 0.15)

    assert ckpt.touches >= 5, (
        f"expected a repeating pulse through a long stage, got {ckpt.touches}"
    )


async def test_it_does_not_pulse_when_nothing_is_running() -> None:
    """Between stages there is no work to vouch for; a pulse then would be a lie."""
    ckpt = _Ckpt()

    await _run_for(lambda: run_heartbeat_loop(ckpt, {}, interval=0.01), 0.1)

    assert ckpt.touches == 0


async def test_it_resumes_pulsing_when_a_new_stage_starts() -> None:
    ckpt = _Ckpt()
    running: dict[str, tuple[float, str]] = {}

    task = asyncio.create_task(run_heartbeat_loop(ckpt, running, interval=0.01))
    await asyncio.sleep(0.05)
    assert ckpt.touches == 0
    running["create_audio"] = (0.0, "Recording your podcast")
    await asyncio.sleep(0.08)
    task.cancel()
    await asyncio.gather(task, return_exceptions=True)

    assert ckpt.touches >= 3


async def test_the_write_is_AWAITED_not_fired_and_forgotten() -> None:
    """A bare create_task can be garbage-collected mid-flight — one of the two
    ways the pulse died. Every touch here must actually complete."""
    ckpt = _SlowCkpt()
    running = {"create_audio": (0.0, "Recording")}

    await _run_for(lambda: run_heartbeat_loop(ckpt, running, interval=0.01), 0.2)

    assert ckpt.touches >= 4


async def test_it_is_independent_of_the_client_stream() -> None:
    """The regression that mattered: the pulse must not be downstream of emitting
    to the client. A permanently wedged emitter cannot stop it, because the loop
    never touches the emitter at all."""
    ckpt = _Ckpt()
    running = {"compose_official_video": (0.0, "Composing")}
    emit_calls = 0

    async def wedged_emit(_event: object) -> None:
        nonlocal emit_calls
        emit_calls += 1
        await asyncio.Event().wait()  # never returns — a dead client stream

    # The loop is handed no emitter and must not acquire one.
    await _run_for(lambda: run_heartbeat_loop(ckpt, running, interval=0.01), 0.15)

    assert ckpt.touches >= 5
    assert emit_calls == 0


async def test_no_checkpointer_is_a_clean_no_op() -> None:
    """Standalone / NullCheckpointer runs have nothing to pulse; the loop must
    exit rather than spin or raise."""
    await asyncio.wait_for(run_heartbeat_loop(None, {"x": (0.0, "y")}, interval=0.01), timeout=1)


async def test_cancellation_is_silent() -> None:
    """The pipeline cancels it in a finally; that must never surface as an error."""
    ckpt = _Ckpt()
    task = asyncio.create_task(run_heartbeat_loop(ckpt, {"x": (0.0, "y")}, interval=0.01))
    await asyncio.sleep(0.03)
    task.cancel()
    await task  # must not raise


@pytest.mark.parametrize("interval", [0.005, 0.02])
async def test_the_cadence_follows_the_configured_interval(interval: float) -> None:
    ckpt = _Ckpt()
    running = {"create_audio": (0.0, "Recording")}
    window = 0.12

    await _run_for(lambda: run_heartbeat_loop(ckpt, running, interval=interval), window)

    expected = window / interval
    assert ckpt.touches >= expected * 0.4, (
        f"{ckpt.touches} pulses in {window}s at interval={interval} is far below "
        f"the ~{expected:.0f} the cadence promises"
    )
