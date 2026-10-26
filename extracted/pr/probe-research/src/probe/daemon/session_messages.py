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
        GET /v1/sessions/{sid}/messages      (`probe_api.session_messages`),
                                             each message leased to this daemon
        for each message, oldest first:
            not here    PUBLISH it (`kind` message, `origin` inbox, `keep`, its
                        INBOX_TTL_S, the file named by the message id), THEN
                        ack `acked` (also when not acked yet)
            claimed     a hook took it (`mailbox.where`): ack
                        `delivered_to_agent`, and the poll lists it no more
            refused     another daemon holds it (409): drop the waiting copy
        and every waiting copy the poll REVOKES (it names the ones still here:
        leased to another daemon since, shown, expired or gone): dropped

PUBLISH, THEN ACK (R6). The mailbox dedupes by the message's id, so a worker
that dies between the publish and the ack finds the message listed again and
already in the mailbox: it acks and sends nothing twice. One that dies before
the publish loses nothing: the message is still listed. An ack that fails is
said again at the next poll.

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
KNOWN LIMITS (CONTRACT.md): a message shown here whose last receipt was lost
before this daemon died can be shown again on the next machine; and while this
daemon keeps polling it holds new messages, even if the researcher moved on.

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


def inbox_message(session_id: str, row: dict, *, now: float, origin_turn: "int | None" = None) -> mailbox.Message:
    """The mailbox message for one server message: kept, delivered like a run
    alert, its file named by the server id. `made_at` is when it was SENT, so its
    INBOX_TTL_S counts from there, as the server's does, and the same message is
    always the same file."""
    made_at = _epoch(row.get("created_at"))
    if made_at is None or made_at > now + 300:
        made_at = now
    return mailbox.Message(id=mailbox.inbox_message_id(row["id"]), session=session_id, kind=mailbox.Kind.MESSAGE,
                           text=delivered_text(row.get("sender"), row["body"]), made_at=made_at,
                           origin_turn=origin_turn, keep=True, origin=mailbox.ORIGIN_INBOX)


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

    async def fetch(self) -> "dict | None":
        from probe.daemon import probe_api, run_alerts
        from probe.daemon import worker as worker_mod

        env = worker_mod.probe_env(self.sid)
        if not env.get("PROBE_TOKEN"):
            return None
        try:
            # The copies still waiting here: Probe answers which another daemon
            # (or the agent, elsewhere) has had since, and they go.
            return await probe_api.session_messages(env, self.sid, self._instance(),
                                                    mailbox.waiting_inbox_ids(self.sid))
        except probe_api.KeyRefused as exc:
            log.info("session messages: Probe refused the daemon's key (%s); asking again in %.0f s",
                     exc, run_alerts.RUN_ALERT_REFUSED_WAIT_S)
            self.next_poll_at = self.lane.clock() + run_alerts.RUN_ALERT_REFUSED_WAIT_S
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
                msg = inbox_message(self.sid, row, now=self._now(), origin_turn=self._turn())
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
            if where is mailbox.Where.CLAIMED:
                await probe_api.ack_session_message(env, self.sid, row["id"], probe_api.ACK_DELIVERED_TO_AGENT,
                                                    instance)
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
