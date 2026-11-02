"""One attended managed-LLM run on any rig: the same startup home, powered hold, Ctrl+C,
return home and disconnect as policy tasks (dreamscale.attended)."""

import asyncio
import signal

from dreamscale.attended.lifecycle import AttendedLifecycle
from dreamscale.attended.runner import _arms_word

from .runner import run


class _AttendedAdapter:
    """Suppress automatic return-home after uncertain physical execution or holds."""

    def __init__(self, inner, lifecycle):
        self._inner, self._lifecycle = inner, lifecycle

    def __getattr__(self, name):
        return getattr(self._inner, name)

    async def execute(self, call):
        try:
            receipt = await self._inner.execute(call)
        except BaseException:
            self._lifecycle.inhibit_return_home(
                "Cannot return home automatically after uncertain physical execution."
            )
            raise
        if receipt.status in {"partial", "unknown"}:
            self._lifecycle.inhibit_return_home(
                "Cannot return home automatically after uncertain physical execution."
            )
        return receipt

    async def stop(self):
        try:
            await self._inner.stop()
        except BaseException:
            self._lifecycle.inhibit_return_home(
                "Measured-pose hold unconfirmed. Use hardware E-stop."
            )
            raise


def _confirmed(input_fn, print_fn):
    """The policy runs' start prompt: Enter starts; Ctrl+C, EOF, cancel or exit don't."""
    while True:
        try:
            choice = input_fn("Enter to start · Ctrl+C to cancel: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return False
        if choice in {"cancel", "exit"}:
            return False
        if not choice:
            return True
        print_fn("Enter to start · Ctrl+C to cancel.")


def run_attended_llm(
    *, request, embodiment, make_gateway, make_rig, make_adapter, journal_dir,
    input_fn=input, print_fn=print,
):
    """Create the LLM session, confirm, open the rig, home, run the agent loop, clean up.

    Everything but the agent turns reads as a policy run (dreamscale.attended.run_attended).
    make_rig() returns an unopened rig; make_adapter(rig) returns its RobotAdapter once the
    rig is open and holding. The rig is closed by the lifecycle, never by the adapter.
    """
    arms = _arms_word(embodiment)

    async def work():
        gateway = make_gateway()
        sid = None
        rig = None
        lifecycle = None
        previous_signal = None
        try:
            sid = await gateway.create(request)
            print_fn(f"{arms.title()} will move. Clear the workspace; keep E-stop ready.")
            if not _confirmed(input_fn, print_fn):
                return None
            rig = make_rig()
            lifecycle = AttendedLifecycle(rig, print_fn=print_fn, ready=False, arms=arms)
            task = asyncio.current_task()
            previous_signal = signal.getsignal(signal.SIGINT)

            def stop_now(signum, frame):
                homing = lifecycle.homing
                try:
                    lifecycle.request_stop()
                finally:
                    if not homing:
                        task.cancel()

            signal.signal(signal.SIGINT, stop_now)
            print_fn("Connecting robot…")
            rig.open(attended=True)
            await asyncio.sleep(0)
            adapter = _AttendedAdapter(make_adapter(rig), lifecycle)
            lifecycle.opened()
            offset = await lifecycle.startup_home()
            if lifecycle.has_home:
                note = (
                    "" if offset is None
                    else f"; largest measured arm offset {offset:.4f} {embodiment.unit}"
                )
                print_fn(f"Homing ramp complete{note}.")
            lifecycle.task_started()
            return await run(
                adapter, gateway, sid, journal_dir / f"{sid}.jsonl", print_fn=print_fn,
            )
        finally:
            try:
                try:
                    if lifecycle is not None:
                        try:
                            lifecycle.stop_and_hold()
                            await lifecycle.return_home()
                        finally:
                            print_fn("Disconnecting local hardware…")
                            lifecycle.close()
                            held = getattr(rig, "held_on_close", {})
                            if held and all(held.values()):
                                print_fn(embodiment.held_message())
                            else:
                                print_fn("Disconnected.")
                finally:
                    if previous_signal is not None:
                        signal.signal(signal.SIGINT, previous_signal)
            finally:
                try:
                    if sid:
                        async with asyncio.timeout(10):
                            await gateway.close(sid)
                finally:
                    await gateway.aclose()

    try:
        return asyncio.run(work())
    except (KeyboardInterrupt, EOFError, asyncio.CancelledError):
        # The agent loop already said "Stopped"; cleanup above reported the arms.
        return None
