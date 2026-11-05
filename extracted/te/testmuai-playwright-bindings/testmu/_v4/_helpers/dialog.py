"""V4 Playwright JS-dialog handling: answers armed before the trigger, events read after.

Playwright auto-dismisses a JavaScript dialog (alert / confirm / prompt /
beforeunload) unless a ``dialog`` listener exists BEFORE the action that opens it,
and while a dialog is open every page call blocks. So the answer is decided up
front and given the instant the dialog opens:

- One listener per browser context (``ensure_dialog_listener``), so tabs and
  popups opened later are covered and Playwright's auto-dismiss is off everywhere.
- ``prime_dialog`` arms a one-shot answer in a FIFO per context and returns its
  id. When a dialog opens, the earliest armed entry that fits its type
  (``expect``; ``*`` fits any type but beforeunload) answers it and is popped
  unless ``repeat``; an entry for a dialog that never opened therefore never
  blocks a later one of another type. No fitting entry: the type default, alert
  accept, confirm dismiss, prompt dismiss, beforeunload accept (Playwright's own
  outcome).
- Every answered dialog is appended to an event list that hosts read with
  ``take_dialog_events`` and record as a ``JS_DIALOG`` step after the trigger;
  ``armed_id`` names the entry that answered it, and ``disarm_dialogs(page,
  entry_id)`` drops one entry that is no longer wanted.
- Hosts that arm a queue of answers (authoring) use ``DialogQueue``; replay
  checks one armed answer with ``wait_for_dialog_answer``.
- A host in manual interaction installs a mode provider
  (``set_dialog_mode_provider``); while it returns True the dialog is left open
  for the user to answer in the browser.

Exported code needs none of the host calls: ``prime_dialog`` before each trigger
attaches the listener and arms the answer by itself.
"""
from __future__ import annotations

import asyncio
import logging
import re
from weakref import WeakKeyDictionary

_log = logging.getLogger("testmu")

_ACTIONS = ("accept", "dismiss")
# Kept per context until a host takes them; exported code never does.
_MAX_EVENTS = 200

# Answer for a dialog no armed entry fits.
_TYPE_DEFAULTS = {
    "alert": "accept",
    "confirm": "dismiss",
    "prompt": "dismiss",
    "beforeunload": "accept",
}


class _ContextDialogs:
    """Armed answers, answered-dialog events and the mode provider of one context."""

    def __init__(self) -> None:
        self.armed: list = []
        self.events: list = []
        self.seq = 0
        self.next_id = 0
        self.mode_provider = None


# Keyed weakly by BrowserContext so a closed context evicts itself.
_contexts: "WeakKeyDictionary" = WeakKeyDictionary()


def _peek(page):
    """The context's state, or None: read-only calls never attach the listener."""
    return _contexts.get(page.context)


def _state(page) -> _ContextDialogs:
    context = page.context
    state = _contexts.get(context)
    if state is None:
        state = _ContextDialogs()
        _contexts[context] = state
        context.on("dialog", lambda dialog: _on_dialog(state, dialog))
    return state


def _fits(entry: dict, dialog_type: str) -> bool:
    # A wildcard never answers beforeunload: a dismiss would cancel the navigation.
    if entry["expect"] == "*":
        return dialog_type != "beforeunload"
    return entry["expect"] == dialog_type


def _user_answers(state: _ContextDialogs) -> bool:
    if state.mode_provider is None:
        return False
    try:
        return bool(state.mode_provider())
    except Exception as exc:
        _log.warning("[v4] JS dialog mode provider failed, answering automatically: %s", exc)
        return False


def _on_dialog(state: _ContextDialogs, dialog) -> None:
    dialog_type = dialog.type
    message = dialog.message
    if _user_answers(state):
        _log.info("[v4] JS dialog left open for the user: type=%s message=%r", dialog_type, message)
        return

    entry = next((e for e in state.armed if _fits(e, dialog_type)), None)
    used = None
    if entry is not None:
        if not entry["repeat"]:
            state.armed.remove(entry)
            used = entry
        action, value, source = entry["action"], entry["value"], "armed"
    else:
        action, value, source = _TYPE_DEFAULTS.get(dialog_type, "dismiss"), None, "default"

    if action == "accept":
        if dialog_type == "prompt":
            value = (dialog.default_value or "") if value is None else _resolve_value(str(value))
            coro = dialog.accept(value)
        else:
            value = ""
            coro = dialog.accept()
    else:
        value = ""
        coro = dialog.dismiss()

    state.seq += 1
    event = {
        "seq": state.seq, "type": dialog_type, "message": message,
        "action": action, "value": value, "source": source,
        "armed_id": entry["id"] if entry is not None else None,
    }
    state.events.append(event)
    del state.events[:-_MAX_EVENTS]
    _log.info("[v4] JS dialog %s: type=%s message=%r source=%s", action, dialog_type, message, source)

    # The listener runs synchronously; accept()/dismiss() are coroutines, so
    # resolve the dialog on the running loop while the trigger awaits.
    task = asyncio.ensure_future(coro)
    task.add_done_callback(lambda t: _answer_done(state, event, used, t))


def _answer_done(state: _ContextDialogs, event: dict, used, task) -> None:
    """An answer that failed (another listener took the dialog, the page closed)
    was not given: its event is withdrawn and its one-shot entry re-armed."""
    if task.cancelled() or task.exception() is None:
        return
    _log.warning("[v4] JS dialog answer failed: %s", task.exception())
    if event in state.events:
        state.events.remove(event)
    if used is not None:
        state.armed.append(used)
        state.armed.sort(key=lambda e: e["id"])


def ensure_dialog_listener(page) -> None:
    """Attach the context-level dialog listener for ``page`` (idempotent)."""
    _state(page)


async def prime_dialog(
    page,
    *,
    action: str = "dismiss",
    value: str | None = None,
    expect: str | None = None,
    repeat: bool = False,
) -> int:
    """Arm a one-shot answer for the next fitting JS dialog of ``page``'s
    context; returns the entry's id (``armed_id`` on the event it answers).

    Args:
        page:   The Playwright ``Page``.
        action: ``"accept"`` or ``"dismiss"`` (case-insensitive).
        value:  Text typed into a prompt when accepting (``""`` submits an
                empty answer); ``{{var}}`` / ``${var}`` references resolve
                through ``testmu.var`` when the dialog opens (a reference with
                no value is typed as written). ``None`` uses the prompt's own
                default value.
        expect: Dialog type the answer is for (``alert``, ``confirm``,
                ``prompt``, ``beforeunload``); ``None`` or ``"*"`` fits any type
                but beforeunload.
        repeat: Keep the entry armed after it is used (answers every fitting
                dialog).

    Entries are tried in arming order; the first that fits the dialog's type
    answers it. A dialog no entry fits gets the type default.
    """
    action = (action or "dismiss").strip().lower()
    if action not in _ACTIONS:
        raise ValueError(f"prime_dialog action must be 'accept' or 'dismiss', got {action!r}")
    state = _state(page)
    state.next_id += 1
    state.armed.append({
        "id": state.next_id,
        "action": action,
        "value": value,
        "expect": (expect or "*").strip().lower(),
        "repeat": bool(repeat),
    })
    return state.next_id


_PURE_TEMPLATE = re.compile(r"\{\{[^{}]+\}\}|\$\{[^{}]+\}")


def _resolve_value(value: str) -> str:
    """Resolve a prompt answer's variable references as the dialog opens. A
    pure reference with no value is typed as written (var() returns "" for a
    miss), so a missing variable shows instead of submitting an empty answer."""
    if "{{" not in value and "${" not in value:
        return value
    from testmu._v4._vars import var
    try:
        resolved = var(value)
    except Exception as exc:
        _log.warning("[v4] JS dialog prompt text not resolved: %s", exc)
        return value
    if resolved in (None, "") and _PURE_TEMPLATE.fullmatch(value):
        _log.warning("[v4] JS dialog prompt text %s has no value; typed as written", value)
        return value
    return str(resolved)


def dialog_armed(page) -> bool:
    """True while an armed answer is waiting for a dialog."""
    state = _peek(page)
    return bool(state and state.armed)


def disarm_dialogs(page, entry_id: int | None = None) -> None:
    """Drop the armed answer ``entry_id``, or every armed answer when None."""
    state = _peek(page)
    if state is None:
        return
    if entry_id is None:
        state.armed.clear()
    else:
        state.armed[:] = [e for e in state.armed if e["id"] != entry_id]


def take_dialog_events(page, since_seq: int = 0) -> list:
    """Return and clear the answered-dialog events, oldest first.

    Each event is ``{seq, type, message, action, value, source, armed_id}``
    with ``source`` ``"armed"`` (the entry ``armed_id`` answered it) or
    ``"default"`` (the type default, ``armed_id`` None). Events at or below ``since_seq`` are dropped unreturned.
    """
    state = _peek(page)
    if state is None:
        return []
    events = [e for e in state.events if e["seq"] > since_seq]
    state.events.clear()
    return events


def set_dialog_mode_provider(page, provider) -> None:
    """Install ``provider()``; while it returns True dialogs are left open for the user.

    It is called when each dialog opens, so the host's live mode is read at
    that moment. ``None`` removes it. The provider is held by the context's
    state, so it must not hold the page or context strongly.
    """
    _state(page).mode_provider = provider


async def wait_for_dialog_answer(page, entry_id: int, timeout: float = 3.0, poll: float = 0.1):
    """Replay: wait up to ``timeout`` s for the dialog the armed entry
    ``entry_id`` answered (one may open after its trigger returned) and return
    its event, taken. None when it did not open in time; the entry is then
    disarmed so it cannot answer a later, different dialog. Other events stay."""
    loop = asyncio.get_running_loop()
    deadline = loop.time() + timeout
    while True:
        state = _peek(page)
        if state is not None:
            event = next((e for e in state.events if e.get("armed_id") == entry_id), None)
            if event is not None:
                state.events.remove(event)
                return event
        if loop.time() >= deadline:
            disarm_dialogs(page, entry_id)
            return None
        await asyncio.sleep(poll)


class DialogQueue:
    """A flow's answers (``{type, action, text?, repeat?}``) armed for a host
    that records each answered dialog: every entry is armed once, and leaves
    the queue when the dialog it answered is taken (unless ``repeat``), so a
    used answer is never armed again and one whose dialog never opened blocks
    nothing (the binding answers by type)."""

    def __init__(self) -> None:
        self._entries: list = []
        self._armed: dict = {}   # entry id -> queue entry

    def reset(self, page, entries=None) -> None:
        """Start a flow: its answers, with nothing left armed or answered before it."""
        self._entries = [dict(e) for e in entries or []]
        self._armed = {}
        disarm_dialogs(page)
        take_dialog_events(page)

    async def arm(self, page) -> None:
        """Arm every entry not armed yet."""
        armed = {id(entry) for entry in self._armed.values()}
        for entry in self._entries:
            if id(entry) in armed:
                continue
            entry_id = await prime_dialog(
                page,
                action=entry.get("action") or "dismiss",
                # None keeps a prompt's own value; "" submits an empty answer.
                value=entry.get("text"),
                expect=entry.get("type") or "*",
                repeat=bool(entry.get("repeat")),
            )
            self._armed[entry_id] = entry

    def take(self, page) -> list:
        """The answered dialogs since the last take; an armed one carries the
        queue entry it used under ``"entry"``."""
        events = take_dialog_events(page)
        for event in events:
            entry = self._armed.get(event.get("armed_id"))
            if entry is None:
                continue
            event["entry"] = entry
            if not entry.get("repeat"):
                del self._armed[event["armed_id"]]
                self._entries = [e for e in self._entries if e is not entry]
        return events

    def close(self, page) -> list:
        """End of flow: the dialogs answered since the last take, then nothing
        of this flow stays armed."""
        events = self.take(page)
        disarm_dialogs(page)
        self._armed = {}
        return events

    def unconsumed(self) -> list:
        """Entries no dialog used (sticky entries never count)."""
        return [e for e in self._entries if not e.get("repeat")]


class _ListenerProbe:
    """``_handler_registered.get(page)``: the pre-FIFO name hosts probed to learn
    whether the binding answers ``page``'s dialogs (it does once the context
    listener is attached). Kept so those hosts do not race the listener."""

    def get(self, page, default=None):
        return _contexts.get(page.context) is not None or default


_handler_registered = _ListenerProbe()


__all__ = [
    "prime_dialog", "ensure_dialog_listener", "dialog_armed", "disarm_dialogs",
    "take_dialog_events", "set_dialog_mode_provider", "wait_for_dialog_answer",
    "DialogQueue",
]
