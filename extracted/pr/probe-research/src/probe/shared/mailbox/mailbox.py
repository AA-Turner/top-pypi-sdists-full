"""The daemon's mailbox: the agent's asks and requests in, `[Probe]` messages out. Plain JSON files under `<state>/probe/reads/`, one folder per session; hooks stay stdlib Python 3.9 (`reads_hook.py` reads the same files with the same rules). Details: DESIGN.md."""

from __future__ import annotations

import hashlib
import re
import secrets
import time
from dataclasses import dataclass, field
from pathlib import Path

from probe.foundation.compat.compat import StrEnum
#: How long an unasked message (the reader's own, or a hint) may wait to be delivered.
UNASKED_TTL_S = 30 * 60
#: How long an answer may wait to be delivered.
ANSWER_TTL_S = 24 * 3600
#: How long a run alert may wait to be delivered: past half a day the run has
#: moved on, and the server keeps no alert older than two hours to send again.
ALERT_TTL_S = 12 * 3600
#: How long a message Probe held for the session may wait to be delivered: the
#: server serves one this long too (`app/sessions/messages.py` MESSAGE_TTL).
INBOX_TTL_S = 12 * 3600
#: The most an UNASKED message may carry (the reader is told; `final_result`
#: refuses more). Answers to asks have no limit (Richard, 2026-09-28).
MESSAGE_MAX_CHARS = 1200
#: `Message.origin` of what the daemon's WRITER sends: its reply to a request,
#: a request that failed, a receipt for structural writes nobody asked for, and
#: a receipt for the researcher (WRITER_RELAY_PREFIX).
#: Every other message is the reader's (no origin).
ORIGIN_WRITER = "writer"
#: `Message.origin` of a hint the Probe service posts (plan probe-hints: the
#: team's records nearest a prompt, a peer agent's message, a web search or a
#: run launch). Unasked, like the reader's own messages, but in a slot of its
#: own: one hint and one reader message can both go out in a turn, a newer hint
#: replaces only an older waiting hint, and nothing of the reader's (a newer
#: message, an answer's withdrawal, a stale drop) ever removes one. Its text is
#: rendered whole by Probe (`/v1/hints`, in the `[Probe]` evidence framing) and
#: shown as it came.
ORIGIN_HINT = "hint"
#: How a hint's own text begins (Probe frames it): one that does not is framed as
#: a reader message, so the agent always reads it as Probe's evidence.
HINT_PREFIX = "[Probe] "
#: `Message.origin` of a message sent to this session through Probe (swarm
#: visibility G7): by the session's own person from the dashboard, or by one of
#: their agent sessions (an orchestrator), polled by the worker's run-alert lane
#: (`session_messages.py`). Delivered like a run alert -- every one, outside the
#: turn's unasked slot, waking an idle agent -- and kept (`keep`) for INBOX_TTL_S.
#: Its text is the whole delivered line (`TEXT_INBOX_*`, rendered by the
#: worker), shown as it came. Hooks from before it read only the fields they
#: know: it reaches them as the reader's unasked message (framed as team
#: context, in its one slot a turn, never a wake) until their plugin updates.
ORIGIN_INBOX = "inbox"
#: How an inbox message's text begins: one that does not is framed as a reader
#: message, so `origin` alone never takes a label off.
INBOX_PREFIX = "[Probe] Message from "


class Kind(StrEnum):
    """What a message is: sent on its own, the end of an ask, or a run alert."""

    MESSAGE = "message"  # unasked: the reader's own, the writer's receipt, or a hint (`origin`)
    ANSWER = "answer"
    NOTHING = "nothing"  # an ask with nothing in the team's records
    FAILED = "failed"  # an ask that will not be answered
    #: A run this session launched or wrote to crashed or was flagged (the
    #: worker's run-alert poller, `run_alerts.py`). Delivered like an answer --
    #: every one, never the turn's one unasked slot, never replaced -- and it
    #: wakes an idle agent, though nobody asked for it.
    ALERT = "alert"


# ---------------------------------------------------------------------------
# Messages.
# ---------------------------------------------------------------------------


@dataclass
class Message:
    id: str
    session: str
    kind: str
    text: str = ""
    ask: "str | None" = None
    question: "str | None" = None
    reason: "str | None" = None
    made_at: float = field(default_factory=time.time)
    expires_at: float = 0.0
    origin_turn: "int | None" = None
    #: An unasked message that is neither replaced by a newer one nor replaces one,
    #: lives as long as an answer and is never dropped as stale: the team-note
    #: audit's report, the only record a person sees of a change nobody was asked
    #: about (daemon-team-note-audit). The hooks deliver one unasked message a turn,
    #: so it waits its turn beside the reader's.
    keep: bool = False
    #: A run alert's server ids (`Kind.ALERT` only). The file is the poller's
    #: record of what it published before its store says so: a worker that died
    #: in between reads them back from here and never sends them twice.
    alerts: "list[int] | None" = None
    #: ORIGIN_WRITER for the writer's messages, ORIGIN_HINT for the Probe
    #: service's hints; None for the reader's. Hooks from before it read only the
    #: fields they know: a writer receipt reaches them as an unasked message
    #: (never a wake), a reply as an answer, and a hint as the reader's unasked
    #: message (framed twice, sharing its one slot a turn) until their plugin updates.
    origin: "str | None" = None
    #: An inbox message's (ORIGIN_INBOX) server lease holder: the daemon whose
    #: poll handed it over (`session_messages.daemon_instance`). The hook that
    #: shows it reports `delivered_to_agent` to Probe under this name
    #: (`reads_hook.report_delivered`), so a daemon that dies before its own
    #: report never lets another machine show it again. None for every other
    #: message, and for one an older worker published (its hook reports nothing).
    daemon_instance: "str | None" = None

    @classmethod
    def from_dict(cls, data: dict) -> "Message | None":
        try:
            return cls(id=str(data["id"]), session=str(data["session"]), kind=str(data["kind"]),
                       text=str(data.get("text") or ""), ask=data.get("ask"), question=data.get("question"),
                       reason=data.get("reason"), made_at=float(data.get("made_at") or 0.0),
                       expires_at=float(data.get("expires_at") or 0.0), origin_turn=data.get("origin_turn"),
                       keep=bool(data.get("keep")), alerts=_alert_ids(data.get("alerts")),
                       origin=data.get("origin"), daemon_instance=_instance_of(data.get("daemon_instance")))
        except (KeyError, TypeError, ValueError):
            return None

    @property
    def from_writer(self) -> bool:
        return self.origin == ORIGIN_WRITER

    @property
    def from_hint(self) -> bool:
        return self.origin == ORIGIN_HINT

    @property
    def from_inbox(self) -> bool:
        """A message Probe held for this session (G7), delivered like a run alert."""
        return self.origin == ORIGIN_INBOX and self.kind == Kind.MESSAGE

    def rendered(self) -> str:
        """What the main agent reads: the message framed by its kind, then
        `one_label` -- only its own label keeps the `[Probe]` tag, whatever a
        quoted record, an answer or a hint carries."""
        return one_label(self._framed())

    def _framed(self) -> str:
        if self.from_hint and self.kind == Kind.MESSAGE and self.text.startswith(HINT_PREFIX):
            # Rendered whole by Probe, its `[Probe]` framing included. Anything else
            # with this origin renders as its kind does: `origin` alone never takes
            # the `[Probe] ... not instructions` label off.
            return self.text
        if self.from_inbox and self.text.startswith(INBOX_PREFIX):
            return inbox_safe(self.text)  # the delivered line, labelled by the worker, under the rule
        if self.from_writer:
            if self.kind == Kind.FAILED:
                return TEXT_WRITER_FAILED.format(reason=self.reason or "unknown")
            if self.kind == Kind.MESSAGE and self.text.startswith(WRITER_RELAY_PREFIX):
                return TEXT_WRITER_RELAY.format(message=self.text)
            if self.kind == Kind.MESSAGE:
                return TEXT_WRITER_RECEIPT.format(message=self.text)
            return TEXT_WRITER_REPLY.format(message=self.text)
        question = self.question or ""
        if len(question) > LABEL_QUESTION_CHARS:
            question = question[:LABEL_QUESTION_CHARS - 3].rstrip() + "..."
        if self.kind == Kind.ANSWER:
            return TEXT_ANSWER.format(id=self.ask, question=question, message=self.text)
        if self.kind == Kind.NOTHING:
            return TEXT_NOTHING.format(id=self.ask, question=question)
        if self.kind == Kind.FAILED:
            return TEXT_FAILED.format(id=self.ask, question=question, reason=self.reason or "unknown")
        if self.kind == Kind.ALERT:
            return TEXT_ALERT.format(message=self.text)
        return TEXT_MESSAGE.format(message=self.text)


def _alert_ids(value: object) -> "list[int] | None":
    """A message file's `alerts`, when it is a list of ids (ints, never bools)."""
    if not isinstance(value, list) or not all(isinstance(v, int) and not isinstance(v, bool) for v in value):
        return None
    return list(value)


#: A daemon instance as the server takes one (`X-Probe-Daemon-Instance`, a
#: device id's shape: `app/client_installations/devices.py`).
DAEMON_INSTANCE_RE = re.compile(r"^[A-Za-z0-9_-]{16,128}$")


def _instance_of(value: object) -> "str | None":
    """A message file's `daemon_instance`, when it is one the server would take."""
    return value if isinstance(value, str) and DAEMON_INSTANCE_RE.fullmatch(value) else None


def new_message_id() -> str:
    return "m" + secrets.token_hex(4)


#: A claim token (`claim`): never a dot or a path separator, so a claimed file's
#: name `<ns>-<id>.<token>.json` always parses back.
TOKEN = re.compile(r"[A-Za-z0-9_]{1,64}")

#: How a run-alert message's id begins (the reader's begin with "m").
ALERT_ID_PREFIX = "r"


def alert_message_id(alert_ids: "list[int]") -> str:
    """The id of the message carrying these run alerts: the same ids give the same
    id (no `-`: `claimed_ids` reads the id after the file name's last one)."""
    key = ",".join(str(int(i)) for i in sorted(alert_ids))
    return ALERT_ID_PREFIX + hashlib.sha256(key.encode("utf-8")).hexdigest()[:12]


def message_id_of(path: Path) -> str:
    """The message id a mailbox file's name carries: `<ns>-<id>.json`, or a
    service claim's `<ns>-<id>.<token>.json`."""
    return path.name[: -len(".json")].split(".", 1)[0].rsplit("-", 1)[-1]


def alert_paths(session_id: str) -> "dict[str, Path]":
    """The run-alert message files in this session's mailbox, waiting or claimed
    (until the sweep), by message id: what the poller published, whatever its
    store says."""
    out: dict[str, Path] = {}
    for folder in (messages_dir(session_id), claimed_dir(session_id)):
        if folder.is_dir():
            for path in folder.glob(f"*-{ALERT_ID_PREFIX}*.json"):
                out[message_id_of(path)] = path
    return out


#: How an inbox message's id begins: then its server id, a uuid without dashes.
INBOX_ID_PREFIX = "s"


def inbox_message_id(server_id: str) -> str:
    """The mailbox id of the message Probe holds as `server_id` (a uuid): the
    same message always gets the same id, the dedupe key of every publish (no
    `-`: `claimed_ids` reads the id after the file name's last one)."""
    import uuid

    return INBOX_ID_PREFIX + uuid.UUID(str(server_id)).hex


def read_message(path: Path) -> "Message | None":
    """One message file, or None when it cannot be read as one."""
    data = _read_json(path)
    return Message.from_dict(data) if data else None


def _ttl(msg: Message) -> float:
    """How long `msg` may wait to be delivered."""
    if msg.from_inbox:
        return INBOX_TTL_S
    if msg.kind == Kind.MESSAGE and not msg.keep and not msg.from_writer:
        return UNASKED_TTL_S  # the reader's unasked message (and a hint) goes stale; a writer receipt is a record
    return ALERT_TTL_S if msg.kind == Kind.ALERT else ANSWER_TTL_S


def _file_name(msg: Message) -> str:
    return f"{int(msg.made_at * 1e9):020d}-{msg.id}.json"
from probe.shared.mailbox.inbox_format import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    LABEL_QUESTION_CHARS,
    TEXT_ALERT,
    TEXT_ANSWER,
    TEXT_FAILED,
    TEXT_MESSAGE,
    TEXT_NOTHING,
    TEXT_WRITER_FAILED,
    TEXT_WRITER_RECEIPT,
    TEXT_WRITER_RELAY,
    TEXT_WRITER_REPLY,
    WRITER_RELAY_PREFIX,
    inbox_safe,
    one_label,
)
from probe.shared.mailbox.layout import _read_json, claimed_dir, messages_dir  # noqa: E402 -- pieces need each other; the front door loads this one first
