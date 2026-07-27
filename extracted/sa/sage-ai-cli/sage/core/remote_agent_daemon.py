"""Unified remote-agent daemon — OpenClaw-style "control your computer from your phone".

Subscribes to multiple messaging bridges (iMessage, Telegram, Discord)
simultaneously, routes every incoming message through ONE sage agent,
and sends the reply back via the same channel the message came from.

Architecture:

    Phone (iMessage)  ─┐
    Phone (Telegram)  ─┼─► RemoteAgentDaemon ─► sage agent loop ─► reply
    Phone (Discord)   ─┘                          (locks; one-at-a-time)

Each bridge runs in its own thread (BridgeRunner) so a wedged Telegram
poll doesn't block iMessage delivery. The agent is invoked behind a
lock because the sage agent loop is stateful (conversation context,
working directory, file ops) and would corrupt itself under concurrent
calls.

Wiring (CLI side):

    daemon = RemoteAgentDaemon(
        agent=lambda msg: sage_agent.run(msg.text),
        bridges=[
            BridgeRunner("imessage",  poll_once=imessage.poll),
            BridgeRunner("telegram",  poll_once=telegram.poll),
            BridgeRunner("discord",   poll_once=discord.poll),
        ],
    )
    daemon.start()
    daemon.join()  # blocks until stopped

The individual bridges (TelegramBridge, DiscordBridge in
messaging_bridges.py; sms_bridge for iMessage) supply the poll_once
callables — this module is the coordination layer.
"""

from __future__ import annotations

import logging
import threading
import time
from dataclasses import dataclass, field
from typing import Callable

from .messaging_bridges import BridgeMessage

logger = logging.getLogger("sage.remote_agent_daemon")


# Type aliases for clarity.
AgentFn = Callable[[BridgeMessage], str]
PollFn = Callable[[], None]


# ── BridgeRunner ─────────────────────────────────────────────────────────────


class BridgeRunner:
    """Wraps a bridge's poll loop in a thread with start/stop lifecycle.

    Each bridge implementation supplies a ``poll_once`` callable — fetch
    pending messages, process them, return. The runner calls it
    repeatedly until stopped. Exceptions are caught and logged so a
    transient network blip doesn't kill the thread.
    """

    def __init__(
        self,
        name: str,
        poll_once: PollFn,
        poll_interval: float = 1.0,
    ):
        self.name = name
        self._poll_once = poll_once
        self._interval = poll_interval
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return  # idempotent
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run_loop, name=f"bridge-{self.name}", daemon=True,
        )
        self._thread.start()

    def stop(self, timeout: float = 5.0) -> None:
        """Signal stop. Waits up to `timeout` seconds for the thread to
        notice. Won't block forever — daemon threads die with the parent
        if they ignore the stop signal."""
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=timeout)

    def is_alive(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def _run_loop(self) -> None:
        while not self._stop_event.is_set():
            try:
                self._poll_once()
            except Exception as exc:
                # Don't let a per-tick error kill the bridge — log and
                # carry on. Truly fatal config errors should manifest as
                # poll_once raising on EVERY tick; user will see the
                # log spam and act.
                logger.warning(
                    "BridgeRunner %s: poll_once raised %s; continuing",
                    self.name, exc,
                )
            # Sleep in small slices so stop() takes effect promptly even
            # for longer intervals.
            remaining = self._interval
            while remaining > 0 and not self._stop_event.is_set():
                step = min(0.05, remaining)
                time.sleep(step)
                remaining -= step


# ── RemoteAgentDaemon ────────────────────────────────────────────────────────


class RemoteAgentDaemon:
    """Coordinates multiple bridges + one agent.

    Bridges deliver messages concurrently (each in its own thread); the
    agent call is serialized via a lock so the agent's internal state
    isn't corrupted by interleaved invocations.
    """

    def __init__(
        self,
        agent: AgentFn,
        bridges: list[BridgeRunner],
    ):
        self._agent = agent
        self._bridges = list(bridges)
        self._agent_lock = threading.Lock()
        self._running = False

    # ── Lifecycle ────────────────────────────────────────────────────────

    def start(self) -> None:
        """Start every bridge thread. Idempotent."""
        if self._running:
            return
        self._running = True
        for runner in self._bridges:
            runner.start()

    def stop(self) -> None:
        """Signal stop to every bridge. Waits briefly for them to die."""
        self._running = False
        for runner in self._bridges:
            runner.stop()

    def join(self, timeout: float | None = None) -> None:
        """Block until all bridges have stopped (use with Ctrl-C trap)."""
        for runner in self._bridges:
            if runner._thread is not None:
                runner._thread.join(timeout=timeout)

    @property
    def is_running(self) -> bool:
        return self._running

    # ── Message handling ─────────────────────────────────────────────────

    def handle_message(self, message: BridgeMessage) -> str:
        """Forward a message to the agent. Bridges call this from inside
        their poll loops.

        Serialized via lock — the agent loop is stateful and a second
        concurrent call would corrupt the conversation context, working
        directory, or in-flight file edits.
        """
        with self._agent_lock:
            try:
                return self._agent(message)
            except Exception as exc:
                logger.exception(
                    "Agent raised on message from %s/%s: %s",
                    message.platform, message.chat_id, exc,
                )
                # Return a user-facing error rather than blowing up the
                # whole bridge loop — recipient should see "something
                # went wrong" not silence.
                return f"sage hit an error: {exc}"

    # ── Introspection ────────────────────────────────────────────────────

    def status(self) -> dict:
        """Snapshot of daemon state for `sage daemon status` CLI."""
        return {
            "running": self._running,
            "bridges": {
                runner.name: {"alive": runner.is_alive()}
                for runner in self._bridges
            },
        }


__all__ = [
    "BridgeRunner",
    "RemoteAgentDaemon",
]
