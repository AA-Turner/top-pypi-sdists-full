"""Feedback about Probe for the Probe team, sent only after the person says yes.

Every agent uses one command, `probe feedback send "<text>"`: the coding agents
(agent profile, daemon profile, inline), the daemon's writer through its shell,
the daemon's reader through its `feedback` tool, and the dashboard assistant
through its `probe` tool.

    hold()     the text becomes a question on the approvals board (policy
               `feedback.send`, `probe.daemon.approvals`), put to the person
               word for word through the coding agent's question tool, pi's
               dialog, or `probe approvals` in a terminal. Asked in EVERY
               permission mode, bypass included (Richard, 2026-10-13, T1=A).
    the answer is written by the answer hook, pi's dialog or `probe approvals`,
               never by an agent. Whoever writes a yes starts `probe feedback
               flush`, and session start runs it too when a yes is unsent, so a
               yes is sent without a daemon (the daemon settles only its own
               questions and leaves these alone).
    flush()    sends every feedback question answered yes, with the person's
               own credential for the account the question was asked under,
               keyed by the question so a second flush lands nothing twice. A
               send that fails for now stays unsent and the next flush retries;
               only a refusal that can never land is recorded and dropped.
    the dashboard assistant asks with its own approval card. Its CLI child
               carries ASKED_ENV and `send` posts at once; the server accepts
               that source only from the assistant's own turn credential.

WHAT THE PERSON IS SHOWN IS WHAT IS SENT: the text is cleaned BEFORE the
question (`clean`), never cut (MAX_CHARS keeps it whole), and the transport's
own scrub leaves cleaned text unchanged.
"""

from __future__ import annotations

import os
import re
import unicodedata
import uuid
from probe._compat import StrEnum

from probe import __version__
from probe.daemon import approvals as appr
from probe.sdk import errors
from probe.sdk.stamp_scrub import scrub_body
from probe.tap_core import secrets

ROUTE = "/v1/feedback"
POLICY = appr.FEEDBACK
#: The longest feedback a question shows whole.
MAX_CHARS = 1000
#: Set (to "assistant") only in the dashboard assistant's CLI child, whose own
#: approval card has already asked (`app/assistant/cli_supervisor.py`).
ASKED_ENV = "PROBE_FEEDBACK_ASKED"
#: The server's idempotency key limit (`app/feedback/models.py`).
KEY_MAX_CHARS = 64
#: How much of the question's fingerprint goes into its key.
KEY_FINGERPRINT_CHARS = 20
#: How much of a refusal's message the board keeps.
REFUSAL_CHARS = 200
#: Statuses that can never land however often they are sent: recorded, dropped.
#: Anything else (no answer, a 404 from a server without the route yet, 429,
#: 5xx) stays unsent for the next flush.
PERMANENT_STATUSES = frozenset({400, 403, 413, 422})
#: Outcomes of a feedback question the person said yes to.
UNSENT = "yes: not sent yet"
SENT = "yes: sent"
#: What a daemon from before `feedback.send` existed writes on a yes it cannot
#: verify (`daemon/worker.py`): that yes is recovered when it still verifies.
OLD_DAEMON_VOID = "void: the held action changed on disk"
#: Characters a terminal or a dialog shows as nothing (or that reorder or
#: overwrite what it shows), so text could hide part of itself from the person:
#: these Unicode categories (control, format, line/paragraph separators,
#: surrogates, private use) -- newline and tab kept -- plus the invisible ones
#: in other categories (variation selectors, blank fillers).
_HIDDEN_CATEGORIES = frozenset({"Cc", "Cf", "Zl", "Zp", "Cs", "Co"})
_KEPT = frozenset("\n\t")
_INVISIBLE = re.compile("[\ufe00-\ufe0f\U000e0100-\U000e01ef\u115f\u1160\u3164\uffa0\u2800]")
#: Redaction settles in a round or two; this bounds a pathological text.
_CLEAN_ROUNDS = 4


class Source(StrEnum):
    AGENT = "agent"
    DAEMON_WRITER = "daemon_writer"
    DAEMON_READER = "daemon_reader"
    ASSISTANT = "assistant"


class Refused(Exception):
    """Nothing was held or sent; the message says why, for the agent."""


def clean(text: str) -> str:
    """The text as the person will see it and Probe will store it: hidden
    characters out, then the question's redaction and the transport's own scrub
    until neither changes it (the two catch different shapes)."""
    text = (text or "").replace("\r\n", "\n")
    text = _INVISIBLE.sub(" ", "".join(
        " " if ch not in _KEPT and unicodedata.category(ch) in _HIDDEN_CATEGORIES else ch for ch in text))
    for _ in range(_CLEAN_ROUNDS):
        scrubbed = scrub_body({"text": secrets.redact(text)[0]})["text"]
        if scrubbed == text:
            break
        text = scrubbed
    return text.strip()


def check_text(text: str) -> str:
    text = clean(text)
    if not text:
        raise Refused("the feedback is empty: say what happened and what would have helped")
    if len(text) > MAX_CHARS:
        raise Refused(f"the feedback is {len(text)} characters; keep it under {MAX_CHARS} so the person can "
                      "read all of it before it is sent")
    return text


def _harness_row(name: str | None):
    """The registry row an id, alias or display label names."""
    if not name:
        return None
    from probe.harness.registry import get_registry

    registry = get_registry()
    row = registry.find(name)
    if row is None:
        row = next((h for h in registry.all() if h.label.lower() == name.strip().lower()), None)
    return row


def harness_label(name: str | None) -> str | None:
    """The harness as people name it (its registry label), from an id or a label."""
    row = _harness_row(name)
    return row.label if row is not None else name


def harness_id(name: str | None) -> str | None:
    """The harness's registry id: what the server reads."""
    row = _harness_row(name)
    return row.id if row is not None else name


def _settle(req: appr.Request, board: appr.Board) -> str | None:
    """Take the person's answer to a waiting feedback question, without sending:
    "no", "void", "expired" or "yes" (now APPROVED and UNSENT); None while it is
    unanswered. The answer is read before expiry: `take_answer` already ignores
    one given outside the question's life, so a yes given in time is never lost
    to a flush that ran late."""
    answer = board.take_answer(req.id)
    if answer is None:
        if req.expires_at and board.clock() > req.expires_at:
            board.resolve(req, state=appr.EXPIRED, outcome="expired: nobody answered")
            return "expired"
        return None
    channel = answer.get("channel")
    if answer.get("answer") != appr.YES:
        board.resolve(req, state=appr.DENIED, outcome=f"no ({answer.get('choice')!r})", channel=channel)
        return "no"
    if not appr.verify_held(req):
        board.resolve(req, state=appr.VOID, outcome="void: the question changed on disk", channel=channel)
        return "void"
    board.resolve(req, state=appr.APPROVED, outcome=UNSENT, channel=channel)
    return "yes"


def _current_context() -> str | None:
    try:
        from probe.sdk.config import current_context_name

        return current_context_name()
    except Exception:  # noqa: BLE001 -- an unreadable config: the flush uses whatever is active then
        return None


def hold(text: str, *, session_id: str, source: Source, harness: str | None,
         board: appr.Board | None = None) -> appr.Request:
    """Hold `text` as a question for this session's person. Returns the request:
    WAITING, or DENIED when they already said no to exactly this."""
    text = check_text(text)
    board = board or appr.Board()
    for req in board.all(session_id=session_id, state=appr.WAITING):
        if req.policy != POLICY or _settle(req, board) is not None:
            continue  # answered (or expired) just now: it no longer waits
        if req.facts.get("text") == text:
            return req
        raise Refused(f"feedback question {req.question.header!r} is still waiting for an answer; "
                      "send more after it is answered")
    facts = {"text": text, "source": str(source), "harness": harness_label(harness), "client_version": __version__,
             "session_id": session_id}
    # The account it is asked under: a flush later sends it with that one's credential.
    held = {"kind": "feedback", "context": _current_context()}
    return board.hold(policy=POLICY, session_id=session_id, facts=facts, held=held, bypass=False)


def body(*, key: str, text: str, source: str, harness: str | None, client_version: str | None,
         session_id: str | None) -> dict:
    out = {"key": key, "text": text, "source": source}
    for name, value in (("harness", harness), ("client_version", client_version), ("session_id", session_id)):
        if value:
            out[name] = value
    return out


def request_body(req: appr.Request) -> dict:
    """The POST for a question answered yes, keyed by the question: its id is
    random per board, and its fingerprint is the facts the person saw."""
    facts = req.facts
    return body(key=f"q-{req.id}-{req.fingerprint[:KEY_FINGERPRINT_CHARS]}", text=facts["text"],
                source=facts["source"], harness=harness_id(facts.get("harness")),
                client_version=facts.get("client_version"), session_id=facts.get("session_id"))


def send_asked(client, text: str) -> dict:
    """The dashboard assistant's send: its card already asked. Direct, and a
    failure raises (its CLI child is short-lived; there is nothing to retry from)."""
    text = check_text(text)
    key = os.environ.get("PROBE_IDEMPOTENCY_KEY") or f"a-{uuid.uuid4().hex}"
    return client.write("POST", ROUTE, body(key=key[:KEY_MAX_CHARS], text=text, source=Source.ASSISTANT,
                                            harness=None, client_version=__version__, session_id=None),
                        durable=False)


def flush(client_factory, board: appr.Board | None = None) -> list[tuple[str, str]]:
    """Send every feedback question answered yes; settle the noes and the
    expired. Returns `(question id, outcome)` for each one acted on.

    `client_factory(context)` builds a client for the account a question was
    asked under (None: the active one), once per account and only when
    something is to be sent: a flush with nothing to do builds none. Safe to
    run twice at once: the server keys each item, so a race lands it once."""
    board = board or appr.Board()
    done: list[tuple[str, str]] = []
    clients: dict[str | None, object] = {}
    for req in board.all():
        if req.policy != POLICY:
            continue
        if req.state == appr.VOID and req.outcome == OLD_DAEMON_VOID:
            # An older daemon voided it before this code could read the answer.
            req.state, req.outcome = appr.WAITING, None
        if req.state == appr.WAITING:
            settled = _settle(req, board)
            if settled is None:
                continue
            if settled != "yes":
                done.append((req.id, settled))
                continue
        if req.state != appr.APPROVED or req.outcome != UNSENT:
            continue
        context = req.held.get("context")
        try:
            if context not in clients:
                clients[context] = client_factory(context)
            clients[context].write("POST", ROUTE, request_body(req), durable=False)
        except errors.RosError as exc:
            if exc.status not in PERMANENT_STATUSES:
                done.append((req.id, f"{UNSENT} ({exc.status or type(exc).__name__})"))
                continue
            outcome = f"yes: refused ({exc.status}: {str(exc)[:REFUSAL_CHARS]})"
        except Exception as exc:  # noqa: BLE001 -- not sent at all: the next flush tries again
            done.append((req.id, f"{UNSENT} ({type(exc).__name__})"))
            continue
        else:
            outcome = SENT
        req.outcome = outcome
        board.save(req)
        done.append((req.id, outcome))
    return done
