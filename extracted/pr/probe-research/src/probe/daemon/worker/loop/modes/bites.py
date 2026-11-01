"""bites mode: a fresh capped model call built from disk (bite.build) for every bite."""

from __future__ import annotations
from probe.daemon.store.logbook import CARRY_ON


class BitesMixin:
    """Part of Worker: its methods run with `self` the Worker; compose() folds them into Worker."""

    def _end_conversation_for_bites(self) -> None:
        """Bites record what a conversation does not know about: switched back to
        conversation mode later, the session starts one fresh from disk, never the
        old one with a hole in it."""
        live = self.store.live_conversation()
        if live is not None:
            log.info("conversation %s ends: this worker runs in %s mode", live["id"], Mode.BITES)
            with self.store.tx():
                self.store.end_conversation(live["id"], f"a worker ran in {Mode.BITES} mode after it")
                self.store.set_fact(CARRY_ON, None)
from probe.daemon.worker.loop.mode import Mode  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.loop.reading import log  # noqa: E402 -- pieces need each other; the front door loads this one first
