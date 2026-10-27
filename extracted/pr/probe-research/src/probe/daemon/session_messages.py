"""Messages sent to this session through Probe reach its agent (swarm visibility
G7, `~/plans/swarm-visibility-gaps/PLAN.md` D8).

The session's own person (from the dashboard) or one of their agent sessions
(an orchestrator, `probe session send`) leaves a message for the session on the
server (`app/sessions/messages.py`). This poller, on the run-alert lane's task
and its RUN_ALERT_POLL_S tick (`run_alerts.RunAlertLane`), brings each one into
the agent's mailbox, where the hooks deliver it like a run alert: every one, at
the next prompt or tool call, waking an idle Claude Code or pi (Codex reads it
at its next prompt).

    every RUN_ALERT_POLL_S:
        first, a claim a hook never marked shown, a minute on: back to waiting;
        every inbox message a hook showed here (its `shown` line) that Probe has
        not been told of (all of them, after a restart): ack
        `delivered_to_agent`, within RECEIPT_BUDGET_S, the rest next tick
        GET /v1/sessions/{sid}/messages      (`probe_api.session_messages`),
                                             each message leased to this daemon;
                                             says when this daemon's agent was
                                             last active (`agent_active_at`)
        for each message, oldest first:
            not here    PUBLISH it (`kind` message, `origin` inbox, `keep`, its
                        INBOX_TTL_S, the file named by the message id, the
                        lease holder's name: this daemon), THEN ack `acked`
                        (also when not acked yet)
            shown       a hook took it and marked it shown (`mailbox.inbox_shown`):
                        ack `delivered_to_agent` (in the same budget), and the
                        poll lists it no more
            refused     another daemon holds it (409): drop the waiting copy
        and every waiting copy the poll REVOKES (it names the ones still here:
        leased to another daemon since, shown, expired or gone): dropped

PUBLISH, THEN ACK (R6). The mailbox dedupes by the message's id, so a worker
that dies between the publish and the ack finds the message listed again and
already in the mailbox: it acks and sends nothing twice. One that dies before
the publish loses nothing: the message is still listed. An ack that fails is
said again at the next poll.

SHOWN ONCE. The hook that shows an inbox message tells Probe itself
(`reads_hook.report_delivered`, pi's `reportDelivered`: `delivered_to_agent`
under the name in the file, this daemon's, best effort within 1.5 s, never
following a redirect), so a daemon that dies right after its hook showed a
message never leaves it for another machine to show again. Its own report
follows (idempotent), and a daemon that starts reports every inbox message its
hook already showed before it polls (`report_shown`), all of this tick's
receipts within RECEIPT_BUDGET_S so they never hold the poll. Probe takes the
holder's report after its lease lapsed too, until another daemon took the
message, and never leases a shown message again.

SHOWN MEANS MARKED. A claim (the rename) comes before the hook's output, so
only a `shown` line -- written once the output went out -- says the agent saw
it. Decided per claim (`mailbox.InboxClaims`): a current hook or pi marks every
claim of an inbox message (`shows: 1`, on a receipt line after a Probe service
claim too), and a marked claim counts only with its `shown` line; an unmarked
one is an older hook's, taken at its claim. A marked claim never shown goes
back to waiting UNSHOWN_RETURN_S on (the hook itself returns it at once when
its output fails), and is never reported. A receipt Probe did not answer backs
off (RECEIPT_BACKOFF_S, doubling) behind the ones not tried yet, so receipts
that always time out never starve the rest.

ONE DAEMON DELIVERS IT. The server leases each message it lists to the polling
daemon (`X-Probe-Daemon-Instance`: this machine's device id, `daemon_instance`)
for 2 minutes, renewed by each poll, and takes an ack from the holder only.
Another machine's daemon of the same session is listed nothing meanwhile; one
whose ack is refused (409) drops the copy still waiting in its mailbox. When the
holder stops polling (the session resumed elsewhere) the lease lapses, and the
next daemon is listed the message even if it was received: it publishes it
when its own mailbox lacks it. Each poll names the copies still waiting here
(`held`), and Probe REVOKES those this daemon may no longer deliver (another
daemon holds them now, they were shown, expired or are gone): their files go,
so the old machine's copy of a message the new one took is never shown too.

WHERE THE RESEARCHER IS. Each poll says when this session's agent was last
active on this machine (`X-Probe-Agent-Active-At`: the transcript's newest chat
line, `Worker.agent_active_at`; none before the first). Probe moves a message
leased but not yet shown to a daemon whose agent was active more than a minute
later, so a researcher who moved to another machine gets it there while this
daemon still polls; this daemon's next poll revokes its copy. A daemon that says
nothing (an older one) is never moved from and never moves one.

KNOWN LIMITS (CONTRACT.md G7): a message shown here is shown again elsewhere
only if neither the hook's report nor this daemon's reached Probe before the
other daemon took it over; one this daemon took before the other polled is
shown here when the hook shows it at once (an idle agent wakes for it); a copy
a hook shows after another daemon took the message, before this daemon's next
poll revokes it, is shown on both machines; the activity times come from
two machines' clocks, so a skew past a minute can pick the wrong one; and a
hook that dies after its output but before its `shown` line leaves the message
to be shown again.

WHO SAID IT is the server's word, from the sender's credential (A26): a
dashboard login is the person; every token is one of the person's agent
sessions, named by its title when the same person owns it. Anything this module
does not recognise as the person is labelled as an agent session.

QUIET, as the run-alert poll: a server from before the route, a session it has
not recorded, no network -- asked again at the next poll. A key Probe refused
waits RUN_ALERT_REFUSED_WAIT_S; this poller never ends the worker.
"""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING

from probe._compat import fromisoformat
from probe.daemon import mailbox

if TYPE_CHECKING:  # pragma: no cover
    from probe.daemon.run_alerts import RunAlertLane

log = logging.getLogger("probe.daemon.session_messages")

#: The server's `sender.kind` for the session's own person, from a dashboard
#: login (`app/sessions/messages.py` SenderKind.PERSON). Anything else is one
#: of their agent sessions.
SENDER_PERSON = "person"
#: The longest message the server takes; a longer one is cut here.
BODY_MAX_CHARS = 2000
#: The sending session's title is cut here (`mailbox.inbox_text`).
TITLE_MAX_CHARS = mailbox.INBOX_TITLE_CHARS
#: The name a sender with none is given.
NO_NAME = "your researcher"
#: Reporting what the hooks showed takes at most this long per tick, before the
#: poll; the rest is said at the next tick (review of #3530: twenty receipts at
#: 10 s each held the poll, and the run alerts on the same task, past the lease).
RECEIPT_BUDGET_S = 3.0
#: ...and each receipt at most this long.
RECEIPT_TIMEOUT_S = 1.5
#: A receipt that got no answer waits this long before it is tried again,
#: doubling with each miss up to RECEIPT_BACKOFF_MAX_S, and goes after every one
#: not tried yet: two that always time out never use up the budget of the rest.
RECEIPT_BACKOFF_S = 30.0
RECEIPT_BACKOFF_MAX_S = 600.0


def _fold(value: object) -> str:
    """One line: whitespace folded."""
    return " ".join(value.split()) if isinstance(value, str) else ""


def _epoch(value: object) -> "float | None":
    """An ISO-8601 time as epoch seconds, or None."""
    if not isinstance(value, str) or not value:
        return None
    try:
        return fromisoformat(value).timestamp()
    except ValueError:
        return None


def delivered_text(sender: object, body: str) -> str:
    """The line the agent reads (`mailbox.inbox_text`, the delivery rule): who
    sent it, then the message, its further lines quoted and never tagged."""
    sender = sender if isinstance(sender, dict) else {}
    person = _fold(sender.get("name")) or NO_NAME
    title = sender.get("session_title")
    return mailbox.inbox_text(person, body, from_person=sender.get("kind") == SENDER_PERSON,
                              title=title if isinstance(title, str) else None)


def usable(rows: list) -> list[dict]:
    """The messages the server sent whole -- a uuid id, a non-empty body --
    oldest first by the server's order, each id once. Anything else is
    skipped: one bad row never holds the rest."""
    import uuid

    out, seen = [], set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        body = row.get("body")
        try:
            server_id = str(uuid.UUID(str(row.get("id"))))
        except ValueError:
            continue
        if not isinstance(body, str) or not body.strip() or server_id in seen:
            continue
        seen.add(server_id)
        out.append({**row, "id": server_id, "body": body[:BODY_MAX_CHARS]})
    return out


def inbox_message(session_id: str, row: dict, *, now: float, origin_turn: "int | None" = None,
                  daemon_instance: "str | None" = None) -> mailbox.Message:
    """The mailbox message for one server message: kept, delivered like a run
    alert, its file named by the server id. `made_at` is when it was SENT, so its
    INBOX_TTL_S counts from there, as the server's does, and the same message is
    always the same file. `daemon_instance`: the lease holder (this daemon),
    under whose name the hook that shows it reports it shown."""
    made_at = _epoch(row.get("created_at"))
    if made_at is None or made_at > now + 300:
        made_at = now
    return mailbox.Message(id=mailbox.inbox_message_id(row["id"]), session=session_id, kind=mailbox.Kind.MESSAGE,
                           text=delivered_text(row.get("sender"), row["body"]), made_at=made_at,
                           origin_turn=origin_turn, keep=True, origin=mailbox.ORIGIN_INBOX,
                           daemon_instance=daemon_instance)


def iso_utc(epoch: "float | None") -> "str | None":
    """`epoch` as the ISO 8601 UTC time the poll's activity header carries, or None."""
    if epoch is None:
        return None
    from datetime import datetime

    from probe._compat import UTC

    try:
        return datetime.fromtimestamp(float(epoch), tz=UTC).isoformat()
    except (OverflowError, OSError, ValueError):
        return None


def daemon_instance() -> str:
    """Which daemon this is, for the server's delivery lease: this machine's
    device id (`sdk.device_identity`), so a worker restarted here still holds
    what the one before it leased. A machine that cannot keep one gets an id
    for this process: its leases lapse, and are taken again, when it restarts."""
    global _PROCESS_INSTANCE
    try:
        from probe.sdk.device_identity import device_instance_id

        machine = device_instance_id()
    except Exception:  # noqa: BLE001 -- no identity file: this process's own id
        machine = None
    if machine:
        return machine
    if _PROCESS_INSTANCE is None:
        import secrets

        _PROCESS_INSTANCE = "daemon-" + secrets.token_hex(12)
    return _PROCESS_INSTANCE


_PROCESS_INSTANCE: "str | None" = None


class SessionMessages:
    """The session-message poll, on the run-alert lane's task (`lane.run`)."""

    def __init__(self, lane: "RunAlertLane") -> None:
        self.lane = lane
        self.sid = lane.sid
        #: No poll before this (`lane.clock`).
        self.next_poll_at = 0.0
        #: This daemon's id for the server's delivery lease (`daemon_instance`).
        self.instance: "str | None" = None
        #: The server ids whose `delivered_to_agent` Probe has answered in this
        #: process (taken, another daemon's, or gone): not said again. Empty at
        #: start, so a restarted daemon says it for every message its hook took.
        self.reported: set[str] = set()
        #: Past this (`time.monotonic`), this tick says nothing more was shown:
        #: the receipts of one tick share RECEIPT_BUDGET_S.
        self.receipt_deadline = 0.0
        #: server id -> (misses so far, not before this `time.monotonic`): a
        #: receipt Probe did not answer, tried again after its backoff.
        self.receipt_misses: dict[str, tuple[int, float]] = {}

    async def tick(self) -> int:
        """One poll, when it is due: how many messages it published."""
        from probe.daemon import run_alerts

        lane = self.lane
        if lane.quitting() or lane.clock() < self.next_poll_at:
            return 0
        from probe.daemon import worker as worker_mod

        if lane.w.replay is None and worker_mod.install_replaced():
            return 0  # the worker leaves for the new install, whose poller asks again
        self.next_poll_at = lane.clock() + run_alerts.RUN_ALERT_POLL_S
        self.receipt_deadline = time.monotonic() + RECEIPT_BUDGET_S  # every receipt of this tick
        if not await self.report_shown():
            return 0
        answer = await self.fetch()
        if answer is None:
            return 0
        for server_id in answer.get("revoked") or []:
            try:
                self._drop(mailbox.inbox_message_id(server_id))
            except ValueError:
                continue
        return await self.hand_over(answer.get("messages") or [])

    def _instance(self) -> str:
        if self.instance is None:
            self.instance = daemon_instance()
        return self.instance

    def _refused(self, exc: Exception) -> None:
        from probe.daemon import run_alerts

        log.info("session messages: Probe refused the daemon's key (%s); asking again in %.0f s",
                 exc, run_alerts.RUN_ALERT_REFUSED_WAIT_S)
        self.next_poll_at = self.lane.clock() + run_alerts.RUN_ALERT_REFUSED_WAIT_S

    async def report_shown(self) -> bool:
        """Before the poll: put back to waiting each inbox message a hook claimed
        and never showed (`mailbox.return_unshown_inbox`: its output never went
        out), then ack `delivered_to_agent` for each one a hook showed here
        (`mailbox.shown_inbox_ids`: its `shown` line) that Probe has not answered
        in this process -- after a restart, all of them -- within the tick's
        receipt budget (`_say_shown`); what is left is said at the next tick, so
        receipts never hold the poll (or the run alerts on the same task) past
        RECEIPT_BUDGET_S. The hook said it already when it could
        (`reads_hook.report_delivered`); saying it again is idempotent, and it
        is what counts when the hook could not. False when Probe refused the
        key (no poll this time)."""
        from probe.daemon import worker as worker_mod

        for message_id in mailbox.return_unshown_inbox(self.sid):
            log.info("session messages: %s was claimed and never shown; it waits again", message_id)
        env = worker_mod.probe_env(self.sid)
        if not env.get("PROBE_TOKEN"):
            return True
        from probe.daemon import probe_api

        now = time.monotonic()
        shown = [server_id for server_id in mailbox.shown_inbox_ids(self.sid) if server_id not in self.reported]
        # Back-off state only for receipts still owed: an expired or settled
        # message leaves it, so it never grows past the mailbox.
        self.receipt_misses = {k: v for k, v in self.receipt_misses.items() if k in shown}
        due = [(self.receipt_misses.get(server_id, (0, 0.0)), server_id) for server_id in shown]
        # Never tried first, then the longest waiting; one still backing off waits.
        for (misses, not_before), server_id in sorted(due):
            if not_before > now:
                continue
            if self.receipt_deadline <= time.monotonic():
                break  # out of this tick's budget: the rest at the next tick
            try:
                await self._say_shown(env, server_id)
            except probe_api.KeyRefused as exc:
                self._refused(exc)
                return False
        return True

    async def _say_shown(self, env: dict, server_id: str) -> "object | None":
        """Ack `delivered_to_agent` for `server_id` within what is left of the
        tick's receipt budget and at most RECEIPT_TIMEOUT_S, the wait included:
        Probe's answer (`AckResult`; one that settles it is remembered in
        `reported`), or None when the budget was spent or no answer came in
        time. A receipt that settled nothing backs off (`receipt_misses`).
        `KeyRefused` as every call."""
        import asyncio

        from probe.daemon import probe_api

        left = self.receipt_deadline - time.monotonic()
        if left <= 0:
            return None
        limit = min(RECEIPT_TIMEOUT_S, left)
        try:
            said = await asyncio.wait_for(
                probe_api.ack_session_message(env, self.sid, server_id, probe_api.ACK_DELIVERED_TO_AGENT,
                                              self._instance(), timeout=limit),
                limit)
        except asyncio.TimeoutError:
            said = None
        if said in (probe_api.AckResult.RECORDED, probe_api.AckResult.LEASE_LOST, probe_api.AckResult.GONE):
            self.reported.add(server_id)
            self.receipt_misses.pop(server_id, None)
            log.info("session messages: reported %s shown (%s)", server_id, said.value)
        else:
            misses = self.receipt_misses.get(server_id, (0, 0.0))[0] + 1
            wait = min(RECEIPT_BACKOFF_MAX_S, RECEIPT_BACKOFF_S * 2 ** (misses - 1))
            self.receipt_misses[server_id] = (misses, time.monotonic() + wait)
        return said

    def _active_at(self) -> "str | None":
        """When this session's agent was last active here, for the poll's header."""
        try:
            return iso_utc(self.lane.w.agent_active_at())
        except Exception:  # noqa: BLE001 -- no reading is no header, never a missed poll
            return None

    async def fetch(self) -> "dict | None":
        from probe.daemon import probe_api
        from probe.daemon import worker as worker_mod

        env = worker_mod.probe_env(self.sid)
        if not env.get("PROBE_TOKEN"):
            return None
        try:
            # The copies still waiting here: Probe answers which another daemon
            # (or the agent, elsewhere) has had since, and they go.
            return await probe_api.session_messages(env, self.sid, self._instance(),
                                                    mailbox.waiting_inbox_ids(self.sid), active_at=self._active_at())
        except probe_api.KeyRefused as exc:
            self._refused(exc)
            return None

    async def hand_over(self, rows: list) -> int:
        """Every row the poll hands this daemon is leased to it. Publish what the
        mailbox does not have -- received elsewhere or not: a session resumed
        here gets what the last machine never showed -- then ack it; ack what a
        hook took as delivered. An ack another daemon's lease refuses drops the
        copy still waiting here. Returns how many it published."""
        from probe.daemon import probe_api
        from probe.daemon import worker as worker_mod

        env = worker_mod.probe_env(self.sid)
        instance = self._instance()
        published = 0
        for row in usable(rows):
            message_id = mailbox.inbox_message_id(row["id"])
            where = mailbox.where(self.sid, message_id)
            fresh = where is None
            if fresh:
                msg = inbox_message(self.sid, row, now=self._now(), origin_turn=self._turn(),
                                    daemon_instance=instance)
                mailbox.publish(msg)  # BEFORE the ack: a crash between the two re-lists it here
                published += 1
                log.info("session messages: published %s", message_id)
                where = mailbox.where(self.sid, message_id)
            if fresh or row.get("acked_at") is None:
                said = await probe_api.ack_session_message(env, self.sid, row["id"], probe_api.ACK_ACKED, instance)
                if said is probe_api.AckResult.LEASE_LOST:
                    self._drop(message_id)
                    continue
                if said is not probe_api.AckResult.RECORDED:
                    continue  # said again at the next poll; the mailbox has it
            if (where is mailbox.Where.CLAIMED and row["id"] not in self.reported
                    and self.receipt_misses.get(row["id"], (0, 0.0))[1] <= time.monotonic()
                    and mailbox.inbox_shown(self.sid, message_id)):
                # Only once a hook marked it shown (its output went out): a claim
                # whose handoff failed goes back to waiting (`report_shown`). In
                # the tick's receipt budget; past it, the next tick says it.
                await self._say_shown(env, row["id"])
        return published

    def _drop(self, message_id: str) -> None:
        if mailbox.drop_waiting(self.sid, message_id):
            log.info("session messages: dropped %s, another Probe daemon of the session delivers it", message_id)

    def _now(self) -> float:
        import time

        return time.time()

    def _turn(self) -> "int | None":
        try:
            return self.lane.store.current_turn()
        except Exception:  # noqa: BLE001 -- the turn is a hint for the writer, never a reason not to deliver
            return None
