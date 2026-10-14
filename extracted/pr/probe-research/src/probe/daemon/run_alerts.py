"""The daemon's run alerts: a run this session launched or wrote to crashed or was
flagged, and the agent is told (run-alerts-to-agent, PR 2).

The server keeps a per-run alert log (the same alerts and gates as the email);
this lane polls it for the session and puts what is new in the agent's mailbox
(`mailbox.py`). The hooks deliver an alert like an answer -- every one, at the
next prompt or tool call -- and wake an idle agent where the harness can (Claude
Code's Stop waiter, pi's poller).

    every RUN_ALERT_POLL_S (its own asyncio task, beside the writer's loop and the
    reader's -- never inside `Worker.tick`, which returns early while the switch
    reads `read only (daemon)` and awaits a whole bite):
        GET /v1/sessions/{sid}/run-alerts   (`probe_api.run_alerts`)
        -> the alerts whose ids the store has not recorded
        -> ONE `alert` message for the batch: up to ALERT_MAX_LISTED texts, one
           per line, then "and N more runs."
        -> PUBLISHED first, then RECORDED -- the ids, and the message beside the
           reader's, published -- in one transaction

CRASH-SAFE HAND-OFF. The message file carries its alert ids (`Message.alerts`),
and its id is derived from them. A worker that dies between the publish and the
record finds the file at its next poll that sees an unrecorded alert, waiting or
claimed, and records its ids before it looks for new ones: each alert reaches the
agent once, and a crash never loses one (it was published first). The record is
what the writer reads the agent's claims against (`Worker._read_reader_log`).

QUIET. A server from before the route (404), a 5xx, a timeout, no network: logged
at debug and asked again at the next poll; the lane never ends the worker. The
server keeps two hours of alerts and the store dedupes by id, so a missed poll
costs nothing but delay.
"""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

from probe.daemon import lease, mailbox

if TYPE_CHECKING:  # pragma: no cover
    from probe.daemon.worker import Worker

log = logging.getLogger("probe.daemon.run_alerts")

#: The server is asked this often (Richard 2026-10-13, T2 = A: "lets do the 30 sec
#: poll"). An alert is already >= 90 s late by design (the watch sweep, the notice
#: window), so a held-open stream would buy ~15 s for four more moving parts.
RUN_ALERT_POLL_S = 30.0
#: After Probe refused the daemon's key: ask again this much later (a key the
#: researcher approves meanwhile is picked up within this).
RUN_ALERT_REFUSED_WAIT_S = 5 * 60.0
#: One message lists at most this many alerts: a group-scope incident (60 runs)
#: is one wake and one screen, not sixty.
ALERT_MAX_LISTED = 10
#: The line after the listed ones, when the batch holds more.
ALERT_MORE = "and {n} more runs."
ALERT_MORE_ONE = "and 1 more run."
#: One alert's text is cut here (the server renders one sentence; a runaway one
#: must not flood the agent's context).
ALERT_TEXT_CHARS = 500


def _line(text: str) -> str:
    """One alert as one line: whitespace folded, cut at ALERT_TEXT_CHARS."""
    line = " ".join(text.split())
    return line if len(line) <= ALERT_TEXT_CHARS else line[:ALERT_TEXT_CHARS - 3].rstrip() + "..."


def usable(alerts: list) -> list[tuple[int, str]]:
    """`(id, text)` of each alert the server sent whole -- an int id, a text -- by
    id, each id once. Anything else is skipped: one bad row never holds the rest."""
    out: dict[int, str] = {}
    for alert in alerts:
        if not isinstance(alert, dict):
            continue
        alert_id, text = alert.get("id"), alert.get("text")
        if isinstance(alert_id, bool) or not isinstance(alert_id, int) or not isinstance(text, str):
            continue
        line = _line(text)
        if line:
            out.setdefault(alert_id, line)
    return sorted(out.items())


def alert_message(session_id: str, alerts: list[tuple[int, str]], *, made_at: float,
                  origin_turn: int | None = None) -> mailbox.Message:
    """The one message for a batch: up to ALERT_MAX_LISTED texts, then how many
    more. Kept (`keep`): never replaced by a newer message, never dropped as stale
    before its ALERT_TTL_S."""
    lines = [text for _, text in alerts[:ALERT_MAX_LISTED]]
    more = len(alerts) - ALERT_MAX_LISTED
    if more > 0:
        lines.append(ALERT_MORE_ONE if more == 1 else ALERT_MORE.format(n=more))
    ids = [alert_id for alert_id, _ in alerts]
    return mailbox.Message(id=mailbox.alert_message_id(ids), session=session_id, kind=mailbox.Kind.ALERT,
                           text="\n".join(lines), made_at=made_at, origin_turn=origin_turn, keep=True, alerts=ids)


class RunAlertLane:
    """The run-alert poller beside the writer, in the writer's process and event loop."""

    def __init__(self, worker: "Worker") -> None:
        self.w = worker
        self.store = worker.store
        self.sid = worker.session.session_id
        self.clock = worker.clock
        #: No poll before this (`clock`): set after Probe refused the key.
        self.next_poll_at = 0.0
        self.task: asyncio.Task | None = None

    # -- life ----------------------------------------------------------------
    def start(self) -> None:
        if self.task is None:
            self.task = asyncio.ensure_future(self.run())

    async def stop(self) -> None:
        """Cancel and wait: at session end nobody is left to tell. An alert not
        polled yet stays on the server for a resumed session's worker."""
        task, self.task = self.task, None
        if task is not None and not task.done():
            task.cancel()
            try:
                await task
            except BaseException:  # noqa: BLE001 -- cancelled, or it had failed: either way it is over
                pass

    def quitting(self) -> bool:
        """Poll no more: the session is ending, or the switch left the daemon. Both
        `on (daemon)` and `read only (daemon)` keep polling: an alert is a read."""
        if self.w.stopping:
            return True
        return self.w.replay is None and not lease.worker_wanted(self.sid)

    async def run(self) -> None:
        try:
            # A worker that died between a publish and its record left the file:
            # record it now, not only when the next new alert arrives, so the
            # writer reads the agent's claim of it either way.
            self.recover()
        except Exception as exc:  # noqa: BLE001 -- the poller never ends the worker
            log.warning("run-alert recovery failed: %s: %s", type(exc).__name__, exc)
        while True:
            try:
                await self.tick()
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # noqa: BLE001 -- the poller never ends the worker
                log.warning("run-alert poll failed: %s: %s", type(exc).__name__, exc)
            await asyncio.sleep(RUN_ALERT_POLL_S)

    # -- one poll --------------------------------------------------------------
    async def tick(self) -> mailbox.Message | None:
        """One poll: the message it published, if any."""
        if self.quitting() or self.clock() < self.next_poll_at:
            return None
        from probe.daemon import worker as worker_mod

        if self.w.replay is None and worker_mod.install_replaced():
            return None  # the worker leaves for the new install, whose poller asks again
        alerts = await self.fetch()
        if alerts is None:
            return None
        return self.hand_over(alerts)

    async def fetch(self) -> list[dict] | None:
        """The server's alerts for this session, or None when it could not say."""
        from probe.daemon import probe_api
        from probe.daemon import worker as worker_mod

        env = worker_mod.probe_env(self.sid)
        if not env.get("PROBE_TOKEN"):
            log.debug("run alerts: the daemon has no key yet")
            return None
        try:
            alerts = await probe_api.run_alerts(env, self.sid)
        except probe_api.KeyRefused as exc:
            log.info("run alerts: Probe refused the daemon's key (%s); asking again in %.0f s",
                     exc, RUN_ALERT_REFUSED_WAIT_S)
            self.next_poll_at = self.clock() + RUN_ALERT_REFUSED_WAIT_S
            return None
        if alerts is None:
            log.debug("run alerts: no answer from Probe; asking again at the next poll")
        return alerts

    def hand_over(self, alerts: list) -> mailbox.Message | None:
        """Publish the alerts the mailbox has not had as ONE message, then record
        them. Returns the message, or None when nothing was new."""
        batch = usable(alerts)
        fresh = self._unrecorded(batch)
        if fresh:
            # Unrecorded ids are also what a worker that died after its publish
            # leaves behind: its file says which, so they are not sent again.
            self.recover()
            fresh = self._unrecorded(fresh)
        if not fresh:
            return None
        msg = alert_message(self.sid, fresh, made_at=self.clock(), origin_turn=self.store.current_turn())
        mailbox.publish(msg)
        self._record(msg)
        log.info("run alerts: %s new, sent as message %s", len(fresh), msg.id)
        return msg

    def recover(self) -> int:
        """Record each alert message in the mailbox (waiting or claimed) that the
        store does not know: published by a worker that died before it recorded.
        Returns how many."""
        paths = mailbox.alert_paths(self.sid)
        if not paths:
            return 0
        known = self.store.read_messages(sorted(paths))
        recovered = 0
        for message_id, path in sorted(paths.items()):
            if message_id in known:
                continue
            msg = mailbox.read_message(path)
            if msg is None or msg.kind != mailbox.Kind.ALERT or not msg.alerts:
                continue
            self._record(msg)
            recovered += 1
            log.info("run alerts: recorded message %s, published before a restart", msg.id)
        return recovered

    def _unrecorded(self, batch: list[tuple[int, str]]) -> list[tuple[int, str]]:
        done = self.store.delivered_run_alerts([alert_id for alert_id, _ in batch])
        return [(alert_id, text) for alert_id, text in batch if alert_id not in done]

    def _record(self, msg: mailbox.Message) -> None:
        """The ids and the message, in one transaction. Published: beside the
        reader's own messages, so the writer reads the agent's claim of it."""
        with self.store.tx():
            self.store.add_read_message(message_id=msg.id, kind=msg.kind, text=msg.text, origin_turn=msg.origin_turn)
            self.store.mark_read_message_published(msg.id)
            self.store.add_run_alerts(msg.alerts or [], msg.id)
