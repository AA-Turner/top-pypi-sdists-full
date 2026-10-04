"""Remarks — the person's comments, choices, edits, answers and interactions on
earlier output, riding along with their NEXT message (`input_remarks` part).

A person highlights a passage of an agent reply and comments on it, picks an
option in a decision block, edits an answer, submits a questionnaire, or
changes an interactive shape. None of that triggers a reply. Each one is staged
as a removable chip and travels with the person's next message as ONE
``input_remarks`` part carrying a list of structured items.

THE MODEL READS MARKDOWN, NOT AN ENVELOPE (Arman, 2026-10-03). Each item is
projected as a one-line hidden marker naming the kind and the location, then
the person's own material::

    <!-- comment on your previous reply -->
    > quoted passage

    the person's words

The marker is the only platform-authored text and it is minimal: the person's
turn is the person's alone (see the header of ``unified_content.py``).

LOCATION WORDING MUST BE SOMETHING THE MODEL CAN RESOLVE. The model never sees
message ids or positions, so a chat target is counted in assistant TURNS back
from the user message that carries the remark ("your previous reply", "your
reply 3 back"); a tool loop's several assistant rows are ONE turn. When the
loaded replies come from more than one agent, another agent's reply is named
("Archaeologist's previous reply", "Archaeologist's reply 3 back"); the
answering agent's own replies, and any reply whose agent is unknown, keep
"your …". A non-chat
record is named by its type and title (note “Q3 plan”). A target that is not in
the loaded history falls back to "the passage quoted below" (or "an earlier
reply" when there is no quote). The wording is computed ONCE, when the
containing message is first sent, and frozen in ``resolved_text`` — a later
turn never re-counts it, so "your previous reply" stays true to the moment the
person wrote it.

The part type string lives in ONE constant, ``REMARKS_PART_TYPE``; the two
``Literal[...]`` annotations that must spell it are pinned to it by a test.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from matrx_ai.decisions.kinds import QUESTION_NAME_PATTERN

#: The wire discriminator for the remarks part. Rename here (and the two pinned
#: Literal annotations the test names) — nothing else spells it.
REMARKS_PART_TYPE = "input_remarks"

#: Every remark carries a conversation-wide short HANDLE the model can cite
#: (``c1``, ``c2`` …) — one prefix for every kind (THREADS R1). Rename here only.
REMARK_HANDLE_PREFIX = "c"
REMARK_HANDLE_PATTERN = rf"^{REMARK_HANDLE_PREFIX}[1-9][0-9]{{0,5}}$"
_HANDLE_RE = re.compile(REMARK_HANDLE_PATTERN)

RemarkKind = Literal["comment", "choice", "edit", "answers", "interaction"]

_STRICT = ConfigDict(extra="forbid", populate_by_name=True)


class RemarkTarget(BaseModel):
    """What the remark is about. A chat reply (``message_id``) or any other
    platform record (``record_token`` + ``record_id`` + ``record_title``)."""

    model_config = _STRICT

    #: chat.message id of the assistant reply the remark is on.
    message_id: str | None = None
    #: The record type noun (``note``, ``task``, ``project`` …) for a non-chat target.
    record_token: str | None = None
    record_id: str | None = None
    record_title: str | None = None


class RemarkAnswer(BaseModel):
    """One answered question. ``name``/``type`` reuse the decision_questions
    question vocabulary (snake_case output name; noul/choice/score) so a
    questionnaire built from decision questions maps 1:1; ``text`` covers the
    free-text questions a decision batch does not have."""

    model_config = _STRICT

    question: str = Field(min_length=1)
    answer: str | bool | float | list[str]
    name: str | None = None
    type: Literal["noul", "choice", "score", "text"] | None = None

    @field_validator("name")
    @classmethod
    def _snake_case_name(cls, value: str | None) -> str | None:
        if value is not None and not QUESTION_NAME_PATTERN.match(value):
            raise ValueError(
                f"Answer name {value!r} is not snake_case (the decision question name rule)."
            )
        return value


class RemarkThreadEntry(BaseModel):
    """One message of an existing comment thread, snapshotted onto a remark
    ("continue this thread in a new chat"). Oldest first."""

    model_config = _STRICT

    author_name: str = Field(min_length=1, max_length=200)
    author_kind: Literal["person", "agent"]
    body: str = Field(min_length=1)
    created_at: str | None = None


class RemarkItem(BaseModel):
    """One staged remark. Structured on the wire and in storage; only the
    model-facing projection (``render_remark``) is text."""

    model_config = _STRICT

    kind: RemarkKind
    target: RemarkTarget | None = None
    #: The exact passage the remark is anchored to, when there is one.
    quote: str | None = None
    #: The person's words — a comment, or the choice/interaction projection
    #: ("I chose SQLite.").
    body: str | None = None
    #: Unified diff text (``edit``).
    diff: str | None = None
    answers: list[RemarkAnswer] | None = None
    #: The shape / questionnaire title (``answers``, ``interaction``).
    title: str | None = None
    #: platform.comments id when the remark is also a stored comment.
    comment_id: str | None = None
    #: THE STABLE IDENTITY of this remark (THREADS R1): the client's resource id,
    #: or one the server mints when absent. A thread root is keyed on THIS,
    #: never on the handle.
    id: str | None = Field(default=None, min_length=1, max_length=200)
    #: The conversation-wide short handle (``c3``) the model cites to reply.
    #: Server-minted once, at first send, and frozen with ``resolved_text``.
    handle: str | None = Field(default=None, pattern=REMARK_HANDLE_PATTERN)
    #: The thread this remark continues (oldest first) — read by the model as
    #: quoted lines under the marker; the reply still lands in that thread.
    thread: list[RemarkThreadEntry] | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _carries_something(self) -> RemarkItem:
        if not (self.quote or self.body or self.diff or self.answers or self.thread):
            raise ValueError(
                f"A {self.kind} remark needs at least one of quote, body, diff or answers."
            )
        if self.kind == "edit" and not (self.diff or self.body):
            raise ValueError("An edit remark needs a diff (or a body projection).")
        if self.kind == "answers" and not self.answers:
            raise ValueError("An answers remark needs at least one answer.")
        return self


# ---------------------------------------------------------------------------
# Location wording
# ---------------------------------------------------------------------------

UNRESOLVED_QUOTED = "the passage quoted below"
UNRESOLVED_BARE = "an earlier reply"


def turns_back_by_message_id(messages: Sequence[Any], containing: Any) -> dict[str, int]:
    """Map every assistant message id before ``containing`` to how many assistant
    TURNS back it sits (1 = the previous reply).

    A turn is a maximal run of non-user messages between two user messages, so a
    tool loop (assistant → tool → assistant) is one turn and every row in it
    counts the same. Messages after ``containing`` are ignored.
    """
    end = next((i for i, m in enumerate(messages) if m is containing), len(messages))
    out: dict[str, int] = {}
    turn = 0
    in_turn = False
    for message in reversed(list(messages[:end])):
        raw_role = getattr(message, "role", "")
        role = str(getattr(raw_role, "value", raw_role))
        if role == "user":
            in_turn = False
            continue
        if role in ("system", "developer"):
            continue
        if not in_turn:
            turn += 1
            in_turn = True
        message_id = getattr(message, "id", None)
        if role == "assistant" and message_id:
            out.setdefault(str(message_id), turn)
    return out


def _clean_inline(text: str) -> str:
    """One line, and never able to close the HTML comment it sits in."""
    return re.sub(r"\s+", " ", text).strip().replace("--", "–")


def location_phrase(
    item: RemarkItem,
    turns_back: dict[str, int],
    authors: dict[str, str] | None = None,
) -> str | None:
    """The words naming WHERE the remark points, or None when it points nowhere.

    ``authors`` maps a reply's message id to the NAME of the agent that wrote
    it, and is only filled when the conversation holds replies from more than
    one agent and that reply is not the answering agent's own — then the reply
    is named ("Archaeologist's previous reply"). Otherwise it is "your …".
    """
    target = item.target
    if target is not None and target.message_id:
        n = turns_back.get(target.message_id)
        author = (authors or {}).get(target.message_id)
        owner = f"{_clean_inline(author)}'s" if author and author.strip() else "your"
        if n == 1:
            return f"{owner} previous reply"
        if n is not None:
            return f"{owner} reply {n} back"
        return UNRESOLVED_QUOTED if item.quote else UNRESOLVED_BARE
    if target is not None and (target.record_title or target.record_token):
        noun = _clean_inline((target.record_token or "record").replace("_", " "))
        if target.record_title:
            return f"{noun} “{_clean_inline(target.record_title)}”"
        return f"a {noun}"
    if item.quote:
        return UNRESOLVED_QUOTED
    return None


def marker_text(item: RemarkItem, location: str | None) -> str:
    """The hidden marker body, e.g. ``comment c3 on your previous reply``.

    The handle sits right after the kind word, so the model can cite it in a
    ``comment_reply`` (``answers c5 to "Intake questions" in …``)."""
    title = f' "{_clean_inline(item.title)}"' if item.title else ""
    kind = f"{item.kind} {item.handle}" if item.handle else item.kind
    if item.kind == "comment":
        head, prep = kind, "on"
    elif item.kind == "choice":
        head, prep = kind, "in"
    elif item.kind == "edit":
        head, prep = kind, "to"
    elif item.kind == "answers":
        head, prep = (f"{kind} to{title}", "in") if title else (kind, "in")
    else:
        head, prep = (f"{kind} with{title}", "in") if title else (kind, "in")
    return f"{head} {prep} {location}" if location else head


# ---------------------------------------------------------------------------
# Projection
# ---------------------------------------------------------------------------


def _quote_block(quote: str) -> str:
    return "\n".join(f"> {line}" if line.strip() else ">" for line in quote.strip("\n").split("\n"))


def _fence_for(text: str) -> str:
    longest = max((len(run) for run in re.findall(r"`+", text)), default=0)
    return "`" * max(3, longest + 1)


def _answer_value(value: str | bool | float | list[str]) -> str:
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def render_remark(
    item: RemarkItem,
    turns_back: dict[str, int],
    authors: dict[str, str] | None = None,
) -> str:
    """One remark as the model reads it: marker, then quote / diff / answers / body."""
    location = location_phrase(item, turns_back, authors)
    sections: list[str] = [f"<!-- {marker_text(item, location)} -->"]
    body_parts: list[str] = []
    if item.quote and item.quote.strip():
        body_parts.append(_quote_block(item.quote))
    if item.diff and item.diff.strip():
        diff = item.diff.strip("\n")
        fence = _fence_for(diff)
        body_parts.append(f"{fence}diff\n{diff}\n{fence}")
    if item.thread:
        body_parts.append(
            "\n".join(
                f"> {_clean_inline(e.author_name)}{' (agent)' if e.author_kind == 'agent' else ''}: "
                f"{_clean_inline(e.body)}"
                for e in item.thread
            )
        )
    if item.answers:
        body_parts.append(
            "\n".join(
                f"- {_clean_inline(a.question)}: {_answer_value(a.answer)}" for a in item.answers
            )
        )
    if item.body and item.body.strip():
        body_parts.append(item.body.strip())
    # The marker sits directly above its material; sections are blank-line separated.
    return sections[0] + "\n" + "\n\n".join(body_parts)


def render_remarks(
    items: Sequence[RemarkItem],
    turns_back: dict[str, int],
    authors: dict[str, str] | None = None,
    failures: Sequence[dict[str, Any]] | None = None,
) -> str:
    """Every remark, in order, blank-line separated — then one hidden line per
    ``comment_reply`` of the model's that FAILED since the last remarks were
    sent (THREADS R3: a failed reply is told to the model, never dropped)."""
    parts = [render_remark(item, turns_back, authors) for item in items]
    parts.extend(reply_failure_line(f) for f in failures or ())
    return "\n\n".join(parts)


def reply_failure_line(failure: dict[str, Any]) -> str:
    """``<!-- your reply to c99 failed: there is no remark c99 in this conversation -->``"""
    handle = _clean_inline(str(failure.get("to") or "a remark"))
    reason = _clean_inline(str(failure.get("reason") or "the reason was not reported"))
    return f"<!-- your reply to {handle} failed: {reason} -->"


# ---------------------------------------------------------------------------
# Handles — c1, c2 … one counter per conversation (THREADS R1)
# ---------------------------------------------------------------------------


def handle_number(handle: str | None) -> int | None:
    """``"c12"`` → 12; anything that is not a handle → None."""
    if not handle or not _HANDLE_RE.match(handle):
        return None
    return int(handle[len(REMARK_HANDLE_PREFIX):])


def format_handle(number: int) -> str:
    return f"{REMARK_HANDLE_PREFIX}{int(number)}"


def remark_item_dicts(content: Sequence[Any]) -> list[dict[str, Any]]:
    """Every remark item dict inside one message's content (typed blocks or
    stored dicts), in order."""
    out: list[dict[str, Any]] = []
    for part in content or ():
        part_type = part.get("type") if isinstance(part, dict) else getattr(part, "type", None)
        if part_type != REMARKS_PART_TYPE:
            continue
        items = part.get("items") if isinstance(part, dict) else getattr(part, "items", None)
        out.extend(i for i in items or () if isinstance(i, dict))
    return out


def reply_agents(messages: Sequence[Any], turns_back: dict[str, int]) -> dict[str, str]:
    """Map each counted reply's message id to the agent that wrote it — but ONLY
    when those replies come from more than one distinct agent. A single-agent
    (or unattributed) history returns {} and keeps the "your …" wording."""
    by_id: dict[str, str] = {}
    for message in messages:
        message_id = getattr(message, "id", None)
        agent_id = getattr(message, "agent_id", None)
        if message_id and agent_id and str(message_id) in turns_back:
            by_id[str(message_id)] = str(agent_id)
    return by_id if len(set(by_id.values())) > 1 else {}


def reply_authors(
    reply_agent_ids: dict[str, str],
    agent_names: dict[str, str],
    answering_agent_id: str | None,
) -> dict[str, str]:
    """message id -> agent NAME for the replies the answering agent did not
    write. Its own replies, and any agent whose name is unknown, are left out
    so they read "your …"."""
    return {
        message_id: agent_names[agent_id]
        for message_id, agent_id in reply_agent_ids.items()
        if agent_id != answering_agent_id and agent_names.get(agent_id, "").strip()
    }


__all__ = [
    "REMARKS_PART_TYPE",
    "REMARK_HANDLE_PATTERN",
    "REMARK_HANDLE_PREFIX",
    "format_handle",
    "handle_number",
    "remark_item_dicts",
    "reply_failure_line",
    "RemarkAnswer",
    "RemarkItem",
    "RemarkKind",
    "RemarkTarget",
    "RemarkThreadEntry",
    "UNRESOLVED_BARE",
    "UNRESOLVED_QUOTED",
    "location_phrase",
    "marker_text",
    "render_remark",
    "reply_agents",
    "reply_authors",
    "render_remarks",
    "turns_back_by_message_id",
]
