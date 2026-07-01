"""
cvc.tools.clarify — Native CVC multi-choice user-prompt primitive.

Pure CVC implementation of the "ask the user a question, block the agent
thread until they answer" pattern. Lets the agent pause mid-turn to get
a decision from the user, with up to 4 multiple-choice options (the
dashboard auto-appends an "Other (type your answer)" affordance).

Why a separate module from cvc.agent.executor:
  * The agent executor runs the blocking tool call on the request-handling
    thread of whatever surface invoked it (CLI, gateway SSE, gateway WS).
    On the gateway SSE path that thread is the one writing to the
    StreamingResponse generator, so we want a single, well-tested
    "block + resolve" primitive shared by all surfaces.
  * Keeps dashboard-specific streaming/notify hooks out of the executor
    and lets the gateway/WS code own the wire format.

upstream compatibility:
  * Schema mirrors tools.clarify_tool.CLARIFY_SCHEMA on purpose: same
    `question` / `choices` shape, same `MAX_CHOICES = 4` cap, same
    JSON-string return so models that were trained on the upstream tool
    prompts work unchanged when the prompt happens to mention
    "clarify". But this module imports nothing from upstream — the only
    runtime dep is the Python stdlib.
  * resolve_clarify() is the gateway's "user clicked a button" path;
    mark_awaiting_text() flips an entry into text-capture mode when the
    user picks "Other".

Public API:
  register(clarify_id, session_key, question, choices) -> _ClarifyEntry
  wait_for_response(clarify_id, timeout) -> Optional[str]
  resolve_clarify(clarify_id, response) -> bool
  mark_awaiting_text(clarify_id) -> bool
  get_pending_for_session(session_key) -> Optional[_ClarifyEntry]
  has_pending(session_key) -> bool
  clear_session(session_key) -> int
  get_clarify_timeout() -> int         (seconds; 600 default)

State is module-level + thread-safe (RLock) so any surface — CLI,
gateway SSE, gateway WS, future TUI — can resolve a pending entry
without holding a back-reference to the surface that created it.
"""

from __future__ import annotations

import logging
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

logger = logging.getLogger("cvc.tools.clarify")

# Max predefined choices the agent may offer. The dashboard auto-appends
# a 5th "Other (type your answer)" row.
MAX_CHOICES = 4

# Default seconds to wait for the user to answer before giving up.
# Long enough for the user to read the question and pick thoughtfully,
# short enough that an abandoned prompt eventually unblocks the agent
# instead of pinning the running-agent guard forever.
_DEFAULT_TIMEOUT_S = 600


# =========================================================================
# Entry record — one pending clarify request
# =========================================================================

@dataclass
class _ClarifyEntry:
    """One pending clarify request inside a session."""
    clarify_id: str
    session_key: str
    question: str
    choices: Optional[List[str]]
    event: threading.Event = field(default_factory=threading.Event)
    response: Optional[str] = None
    # True when the user picked "Other" or the question had no choices
    # (open-ended). The dashboard's text intercept uses this to know
    # whether the next free-form message in this session is the answer.
    awaiting_text: bool = False

    def signature(self) -> Dict[str, object]:
        return {
            "clarify_id": self.clarify_id,
            "session_key": self.session_key,
            "question": self.question,
            "choices": list(self.choices) if self.choices else None,
        }


# =========================================================================
# Module-level state
# =========================================================================

_lock = threading.RLock()
# clarify_id → _ClarifyEntry  (primary lookup for button callbacks)
_entries: Dict[str, _ClarifyEntry] = {}
# session_key → list[clarify_id]  (FIFO; for text-fallback intercept and
# session cleanup)
_session_index: Dict[str, List[str]] = {}

# Per-session notify callback. The agent (or gateway) registers a callback
# that the calling surface uses to send the prompt to the user (e.g. emit
# the SSE `clarify_request` event). The blocking wait happens AFTER the
# notify fires so the user actually sees the prompt before the agent
# thread parks.
_notify_cbs: Dict[str, Callable[[_ClarifyEntry], None]] = {}


# =========================================================================
# Helpers
# =========================================================================

def _normalise_choice_text(text: str) -> str:
    """Squeeze a single choice down to a clean one-liner.

    Models love to embed structural noise inside choice strings — literal
    newlines, escaped backslash-n sequences, leading numbers like
    "1) ", and surrounding whitespace. Any of those would leak into the
    dashboard as literal characters (`\\n`) or wrap a button label
    awkwardly. We strip aggressively here so the front-end can render
    the button with a simple `<span>`, no escaping required.
    """
    s = str(text or "")
    # Models sometimes emit literal `\n` (two characters) instead of an
    # actual newline — treat both the same way.
    s = s.replace("\\r\\n", " ").replace("\\n", " ").replace("\\t", " ")
    s = s.replace("\r", " ").replace("\n", " ").replace("\t", " ")
    # Collapse repeated whitespace.
    s = " ".join(s.split())
    # Strip leading numbering like "1)", "1.", "1 -", "Option 1:" — the
    # UI already numbers the buttons, so re-numbering in the label looks
    # ugly and bloaty.
    import re as _re
    s = _re.sub(r"^\s*(?:option\s*)?\d+\s*[\.\)\:\-]\s*", "", s, flags=_re.IGNORECASE)
    return s.strip()


def _flatten_choice(c) -> str:
    """Coerce a single choice into its user-facing display string.

    LLMs sometimes emit dict-shaped choices like ``[{"description": "..."}]``
    instead of bare strings. A naive ``str(c)`` turns the dict into its
    Python repr — ``{'description': '...'}`` — which then leaks onto every
    surface that renders the choice (dashboard buttons, CLI panel,
    messaging numbered list) AND is returned verbatim as the user's
    answer. Normalising here, at the one platform-agnostic entry point,
    fixes the whole class in one place.

    Every successful flatten also runs through ``_normalise_choice_text``
    so embedded newlines and re-numbering noise never reach the UI.
    Returns an empty string for unsupported shapes so the caller can
    drop them — a garbage label is worse than no choice at all.
    """
    if c is None:
        return ""
    if isinstance(c, str):
        return _normalise_choice_text(c)
    if isinstance(c, dict):
        for key in ("label", "description", "text", "title", "value"):
            v = c.get(key)
            if isinstance(v, str) and v.strip():
                return _normalise_choice_text(v)
        return ""
    if isinstance(c, (list, tuple)):
        return " ".join(_flatten_choice(x) for x in c).strip()
    return _normalise_choice_text(str(c))


def sanitise_choices(choices) -> Optional[List[str]]:
    """Validate and trim a choices list per the schema.

    Returns:
    - A list of up to MAX_CHOICES non-empty strings, OR
    - None if ``choices`` is None/empty (open-ended question), OR
    - The original list unchanged if it isn't actually a list (the
      executor will surface a tool-error string back to the model).
    """
    if choices is None:
        return None
    if not isinstance(choices, list):
        return choices  # type: ignore[return-value]
    cleaned = [s for s in (_flatten_choice(c) for c in choices) if s]
    if len(cleaned) > MAX_CHOICES:
        cleaned = cleaned[:MAX_CHOICES]
    if not cleaned:
        return None  # empty list → open-ended
    return cleaned


def normalise_question(question: str) -> str:
    """Same hygiene as ``_normalise_choice_text`` but for the question.

    Question text usually doesn't have numbering noise, but models do
    embed `\n` in questions too. Collapse whitespace and trim.
    """
    return _normalise_choice_text(question)


def new_clarify_id() -> str:
    """Return a fresh, unique clarify_id (16 hex chars)."""
    return uuid.uuid4().hex[:16]


# =========================================================================
# Public API — agent-thread side
# =========================================================================

def register(
    clarify_id: str,
    session_key: str,
    question: str,
    choices: Optional[List[str]],
) -> _ClarifyEntry:
    """Register a pending clarify request and return the entry.

    The caller (gateway SSE/WS, or the agent's ask_user handler) will
    then send the prompt to the user and block on
    ``wait_for_response(clarify_id, timeout)``.

    Open-ended questions (``choices`` is None) automatically enter
    text-capture mode — the next free-form message in the session
    resolves them.
    """
    entry = _ClarifyEntry(
        clarify_id=clarify_id,
        session_key=session_key,
        question=question,
        choices=list(choices) if choices else None,
        awaiting_text=not bool(choices),
    )
    with _lock:
        _entries[clarify_id] = entry
        _session_index.setdefault(session_key, []).append(clarify_id)
    return entry


def wait_for_response(clarify_id: str, timeout: float) -> Optional[str]:
    """Block on the entry's event until resolved or timeout fires.

    Polls in 1-second slices so the calling surface can keep the
    connection alive / emit heartbeats while the user is typing. Without
    the slice-and-yield loop, ``Event.wait(timeout=600)`` blocks the
    thread for 10 minutes with zero activity and the gateway's
    inactivity watchdog would kill the agent while the user is still
    typing.

    Returns the resolved response string, or ``None`` on timeout.
    """
    with _lock:
        entry = _entries.get(clarify_id)
    if entry is None:
        return None

    deadline = time.monotonic() + max(timeout, 0.0)
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        # Slice into 1s windows so surfaces can do per-tick work
        # (heartbeat emission, etc.) by hooking the wait loop. The
        # default loop here just yields via Event.wait.
        if entry.event.wait(timeout=min(1.0, remaining)):
            break

    with _lock:
        # Remove from indices regardless of resolution outcome so a
        # second wait_for_response on the same id returns None.
        _entries.pop(clarify_id, None)
        ids = _session_index.get(entry.session_key)
        if ids and clarify_id in ids:
            ids.remove(clarify_id)
            if not ids:
                _session_index.pop(entry.session_key, None)

    return entry.response


# =========================================================================
# Public API — gateway / adapter side
# =========================================================================

def resolve_clarify(clarify_id: str, response: str) -> bool:
    """Unblock the agent thread waiting on ``clarify_id``.

    Returns True if an entry was found and resolved, False otherwise
    (already resolved, expired, or never existed).
    """
    with _lock:
        entry = _entries.get(clarify_id)
        if entry is None:
            return False
    entry.response = str(response) if response is not None else ""
    entry.event.set()
    return True


def get_pending_for_session(session_key: str) -> Optional[_ClarifyEntry]:
    """Return the OLDEST pending clarify entry for a session, or None.

    Used by the text-fallback intercept — when a clarify is awaiting a
    free-form text response, the next user message in that session is
    captured as the answer.
    """
    with _lock:
        ids = _session_index.get(session_key) or []
        for cid in ids:
            entry = _entries.get(cid)
            if entry is None:
                continue
            if entry.awaiting_text:
                return entry
        return None


def mark_awaiting_text(clarify_id: str) -> bool:
    """Flip an entry into text-capture mode (user picked the 'Other' button).

    Returns True if the entry exists and was flipped, False otherwise.
    """
    with _lock:
        entry = _entries.get(clarify_id)
        if entry is None:
            return False
        entry.awaiting_text = True
        return True


def has_pending(session_key: str) -> bool:
    """Return True when this session has at least one pending clarify entry."""
    with _lock:
        ids = _session_index.get(session_key) or []
        return any(_entries.get(cid) is not None for cid in ids)


def clear_session(session_key: str) -> int:
    """Resolve and drop every pending clarify for a session.

    Used by session-boundary cleanup (``/new``, gateway shutdown,
    cached-agent eviction) so blocked agent threads don't hang past the
    end of their session. Returns the number of entries cancelled.
    """
    with _lock:
        ids = list(_session_index.pop(session_key, []) or [])
        entries = [_entries.pop(cid, None) for cid in ids]
    cancelled = 0
    for entry in entries:
        if entry is None:
            continue
        # Empty string sentinel — agent code can distinguish from a real
        # response by inspecting the wait_for_response return value
        # alongside its own timeout deadline. Most callers just treat
        # any falsy result as "user did not respond".
        entry.response = ""
        entry.event.set()
        cancelled += 1
    return cancelled


# =========================================================================
# Notify hooks — gateway / adapter → user-side delivery
# =========================================================================

def register_notify(
    session_key: str,
    cb: Callable[[_ClarifyEntry], None],
) -> None:
    """Register a per-session notify callback used by ``wait_and_notify``.

    The callback receives the freshly-registered entry and is responsible
    for pushing the prompt to the user (e.g. emitting an SSE event,
    sending a Telegram message). It runs synchronously on the calling
    thread; the agent thread blocks in ``wait_and_notify`` afterwards
    until the surface calls ``resolve_clarify``.
    """
    with _lock:
        _notify_cbs[session_key] = cb


def unregister_notify(session_key: str) -> None:
    """Drop the per-session notify callback and cancel any pending entries.

    Call this on session boundaries (interrupt, completion, gateway
    shutdown) so a blocked agent thread doesn't outlive its session.
    """
    with _lock:
        _notify_cbs.pop(session_key, None)
    clear_session(session_key)


def get_notify(session_key: str) -> Optional[Callable[[_ClarifyEntry], None]]:
    with _lock:
        return _notify_cbs.get(session_key)


# =========================================================================
# High-level helper — register + notify + wait
# =========================================================================

def wait_and_notify(
    session_key: str,
    question: str,
    choices: Optional[List[str]],
    timeout: float = 0.0,
) -> str:
    """Register a clarify, notify the user, then block for the answer.

    This is the one-call entry point surfaces should use. It:
      1. Generates a fresh ``clarify_id``
      2. Registers the entry
      3. Calls the session's notify callback (so the user sees the
         prompt immediately, even if the gateway hasn't started the
         HTTP response yet)
      4. Blocks on the event until the user resolves it OR the timeout
         fires (whichever comes first)

    Returns:
        The user's response as a string. Empty string on timeout or
        cancellation — the caller should treat that as "user did not
        respond" and decide whether to abort, retry, or fall through.
    """
    if timeout <= 0:
        timeout = float(get_clarify_timeout())
    clarify_id = new_clarify_id()
    entry = register(clarify_id, session_key, question, choices)
    cb = get_notify(session_key)
    if cb is not None:
        try:
            cb(entry)
        except Exception:
            # A broken notify must not hang the agent. Log and continue
            # to the wait — if the user truly can't see the prompt, the
            # timeout will eventually free the thread.
            logger.warning("clarify notify callback raised", exc_info=True)
    return wait_for_response(clarify_id, timeout) or ""


# =========================================================================
# Config
# =========================================================================

def get_clarify_timeout() -> int:
    """Read the clarify response timeout (seconds) from CVC config.

    Defaults to 600 (10 minutes). Reads ``agent.clarify_timeout`` from
    config.yaml. Falls back to the default on any read/parse error so
    the agent never wedges because of a config issue.
    """
    try:
        # cvc.core.config is the CVC-native config layer; no upstream dep.
        from cvc.core.config import get_config  # type: ignore
        cfg = get_config() or {}
        agent_cfg = cfg.get("agent", {}) or {}
        return int(agent_cfg.get("clarify_timeout", _DEFAULT_TIMEOUT_S))
    except Exception:
        return _DEFAULT_TIMEOUT_S


# =========================================================================
# Tool schema (mirrors upstream for prompt-compat; not registered here)
# =========================================================================

CLARIFY_SCHEMA = {
    "name": "ask_user",
    # The CVC tool is still called ``ask_user`` so existing prompts and
    # test fixtures keep working. The description is intentionally
    # similar to upstream's so models that have seen the tool before
    # behave the same way.
    "description": (
        "Ask the user a question when you need clarification, feedback, or a "
        "decision before proceeding. Supports two modes:\n\n"
        "1. **Multiple choice** — provide up to 4 choices. The user picks "
        "one or types their own answer via a 5th 'Other' option.\n"
        "2. **Open-ended** — omit choices entirely. The user types a "
        "free-form response.\n\n"
        "CRITICAL: when you are offering options, put each option ONLY in "
        "the `options` array — NEVER enumerate the options inside the "
        "`question` text. The UI renders `options` as selectable rows; "
        "options written into the question string render as dead prose "
        "the user can't pick. Right: question='Which deployment target?', "
        "options=['staging', 'prod']. Wrong: question='Which target? 1) "
        "staging 2) prod', options=[].\n\n"
        "Use this tool when:\n"
        "- The task is ambiguous and you need the user to choose an approach\n"
        "- You want post-task feedback ('How did that work out?')\n"
        "- A decision has meaningful trade-offs the user should weigh in on"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": (
                    "The question itself, and ONLY the question (e.g. "
                    "'Which deployment target?'). Do NOT embed the answer "
                    "options here — pass them as separate elements in "
                    "`options`."
                ),
            },
            "options": {
                "type": "array",
                "items": {"type": "string"},
                "maxItems": MAX_CHOICES,
                "description": (
                    "Optional list of choices (e.g. ['Option A', 'Option B']). "
                    "If provided, the user picks one. Omit for a free-form "
                    "question."
                ),
            },
        },
        "required": ["question"],
    },
}


__all__ = [
    "MAX_CHOICES",
    "CLARIFY_SCHEMA",
    "_ClarifyEntry",
    "register",
    "wait_for_response",
    "resolve_clarify",
    "mark_awaiting_text",
    "get_pending_for_session",
    "has_pending",
    "clear_session",
    "register_notify",
    "unregister_notify",
    "get_notify",
    "wait_and_notify",
    "get_clarify_timeout",
    "new_clarify_id",
    "sanitise_choices",
    "_flatten_choice",
]
