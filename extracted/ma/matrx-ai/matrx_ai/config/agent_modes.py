"""Agent modes: an agent's named hints, and which one this conversation is in.

An agent's modes come from its definition (``understanding.modes``: ``[{key, name, description,
instructions}]``, order = menu order, the first is the starting mode) and ride the run config as
``UnifiedConfig.agent_modes``. The conversation's mode is the override ``agent_mode`` (a mode
``key``); absent or unknown = the first mode. The send boundary appends :func:`render_block` on
every model call (part ``agent_modes``). A mode changes nothing in the program.

One mode per line under "Modes:" (``- <name> — <description>``, or ``- <name>`` with no description).
The only platform words in the block are "Modes:" and "Current mode:" (and the "- " list marker); everything
else is the maker's own text.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

#: The part's tag (``platform_parts`` block ``agent_modes``).
BLOCK_TAG = "agent_modes"

#: A sourced mode filled from its row carries this flag in the run config, so it is resolved once (D12, D14).
RESOLVED_FLAG = "resolved"


def _text(value: Any) -> str:
    return " ".join(value.split()) if isinstance(value, str) else ""


def normalize_modes(raw: Any) -> list[dict[str, str]] | None:
    """The agent's modes as ``[{key, name, description, instructions}]``, in order; ``None`` when none.

    A mode without a key is dropped; a missing name is the key; a repeated key keeps its first entry."""
    if not isinstance(raw, list):
        return None
    out: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in raw:
        if not isinstance(item, dict):
            continue
        key = _text(item.get("key"))
        if not key or key in seen:
            continue
        seen.add(key)
        instructions = item.get("instructions")
        mode = {
            "key": key,
            "name": _text(item.get("name")) or key,
            "description": _text(item.get("description")),
            "instructions": instructions.strip() if isinstance(instructions, str) else "",
        }
        source = _text(item.get("source"))
        if source:
            mode["source"] = source
            if item.get(RESOLVED_FLAG):
                mode[RESOLVED_FLAG] = "true"
        out.append(mode)
    return out or None


def modes_need_resolving(config: Any) -> bool:
    """True while a mode follows a platform default not yet filled for this conversation."""
    return any(m.get("source") and not m.get(RESOLVED_FLAG) for m in getattr(config, "agent_modes", None) or [])


async def resolve_agent_modes(config: Any, *, organization_id: str | None, source: Any = None) -> list[str]:
    """Fill every mode that follows a platform default (``source``) from its live row, once per conversation (D14).

    The row is read through the prompt-block host seam (``prompt_blocks.source.BlockSource``, the same ladder as
    declared blocks: the run's organization, the agent's, then the platform): name = label, description,
    instructions = content. A mode whose row is missing is left out and captured as a system error; there is no
    fallback text. Already-resolved modes are left as they are. Returns the sources that were missing."""
    modes = list(getattr(config, "agent_modes", None) or [])
    pending = [m for m in modes if m.get("source") and not m.get(RESOLVED_FLAG)]
    if not pending:
        return []
    from matrx_ai.prompt_blocks.resolve import _agent_organization_rows, _pick
    from matrx_ai.prompt_blocks.source import get_block_source

    block_source = source or get_block_source()
    names = list(dict.fromkeys(m["source"] for m in pending))
    chosen: dict[str, Any] = {}
    if block_source is not None:
        rows = list(await block_source.candidates(names, organization_id=organization_id, personal_user_id=None))
        rows += await _agent_organization_rows(block_source, config, names, rows, organization_id)
        chosen = _pick(rows, allow_personal=False)
    missing = [n for n in names if n not in chosen]
    out: list[dict[str, str]] = []
    for mode in modes:
        if mode.get("source") and not mode.get(RESOLVED_FLAG):
            row = chosen.get(mode["source"])
            if row is None:
                continue
            mode = {
                "key": mode["key"],
                "name": _text(row.label) or mode["key"],
                "description": _text(row.description),
                "instructions": (row.content or "").strip(),
                "source": mode["source"],
                RESOLVED_FLAG: "true",
            }
        out.append(mode)
    config.agent_modes = out or None
    if missing:
        await _capture_missing(missing, have_source=block_source is not None)
    return missing


async def _capture_missing(missing: list[str], *, have_source: bool) -> None:
    """A default mode whose platform row is gone (or no row source at all) is said, never silent."""
    import inspect
    import logging

    reason = "no prompt-block source is configured" if not have_source else "no live agent.prompt_block row"
    logging.getLogger(__name__).error("[agent_modes] default mode(s) %s left out: %s", missing, reason)
    try:
        from matrx_ai._ext import get_ext

        record_error = get_ext("record_error")
    except Exception:
        return
    if record_error is None:
        return
    try:
        pending = record_error(
            RuntimeError(f"default agent mode row missing: {', '.join(missing)}"),
            kind="agent_mode_default_missing",
            error_type="agent_mode_default_missing",
            error_text=f"Agent mode default(s) {', '.join(missing)} left out: {reason}",
            route="matrx_ai.config.agent_modes.resolve_agent_modes",
            payload={"sources": missing, "reason": reason},
        )
        if inspect.isawaitable(pending):
            await pending
    except Exception:  # noqa: BLE001 - the capture never fails the run
        logging.getLogger(__name__).exception("[agent_modes] capture of a missing default failed")


def modes_of_understanding(understanding: Any) -> list[dict[str, str]] | None:
    """The ``modes`` list of an ``agent.definition.understanding`` value (C1), normalized."""
    return normalize_modes(understanding.get("modes")) if isinstance(understanding, dict) else None


def find_mode(modes: list[dict[str, str]] | None, wanted: Any) -> dict[str, str] | None:
    """The mode ``wanted`` names, by key or name, case-insensitive; ``None`` when it names none."""
    term = _text(wanted).casefold()
    if not term or not modes:
        return None
    for mode in modes:
        if mode["key"].casefold() == term:
            return mode
    for mode in modes:
        if mode["name"].casefold() == term:
            return mode
    return None


def current_mode(modes: list[dict[str, str]] | None, agent_mode: Any) -> dict[str, str] | None:
    """The conversation's mode: the one ``agent_mode`` names by key, else the first; ``None`` when no modes."""
    if not modes:
        return None
    key = _text(agent_mode)
    for mode in modes:
        if mode["key"] == key:
            return mode
    return modes[0]


def _entry(mode: dict[str, str]) -> str:
    return f"{mode['name']} — {mode['description']}" if mode["description"] else mode["name"]


def _mode_name(modes: list[dict[str, str]], key: Any) -> str:
    found = next((m for m in modes if m["key"] == key), None)
    return found["name"] if found else _text(key)


def render_block(
    modes: list[dict[str, str]] | None, agent_mode: Any, person_set: dict[str, Any] | None = None
) -> str | None:
    """The ``<agent_modes>`` block (PLAN C5), or ``None`` when the agent has no modes.

    ``person_set`` (``{"mode": key, "was": key}``, D17): the person flipped the mode this turn; one data line
    says so, on that turn only (:func:`settle_turn_mode`)."""
    current = current_mode(modes, agent_mode)
    if current is None or not modes:
        return None
    lines = [f"<{BLOCK_TAG}>", "Modes:", *(f"- {_entry(m)}" for m in modes), f"Current mode: {current['name']}."]
    if person_set and person_set.get("mode") == current["key"] and person_set.get("was"):
        # One ADDITIONAL line (D17): the list, "Current mode:" and the instructions are always there.
        lines.append(
            f"The person switched the mode to {current['name']} by hand this turn "
            f"(it was {_mode_name(modes, person_set['was'])})."
        )
    if current["instructions"]:
        lines.append(current["instructions"])
    lines.append(f"</{BLOCK_TAG}>")
    return "\n".join(lines)


#: ``chat.conversation.metadata`` key: the mode the agent last knew (D17) — recorded when a turn's block is first
#: built and when the agent's own switch goes through; a person's change never writes it.
KNOWN_MODE_KEY = "agent_mode_known"


def person_set_this_turn(known: Any, current_key: Any) -> dict[str, Any] | None:
    """Pure: ``{"mode": current, "was": known}`` when the mode now differs from the one the agent last knew; None
    when nothing was known (a first turn, an older conversation, a chat that simply opens in a mode)."""
    known_key, now = _text(known), _text(current_key)
    if not known_key or not now or known_key == now:
        return None
    return {"mode": now, "was": known_key}


def remember_known_mode(conversation_id: Any, key: Any) -> None:
    """Queue the mode the agent now knows into the conversation's metadata (only this key), through the request's
    write coordinator (``queue_conversation_metadata_patch``). No coordinator (a run with nothing stored): nothing."""
    if not conversation_id or not _text(key):
        return
    from matrx_ai.persistence.queue_helpers import get_coordinator, queue_conversation_metadata_patch

    if get_coordinator() is None:
        return
    queue_conversation_metadata_patch(str(conversation_id), {KNOWN_MODE_KEY: _text(key)})


def settle_turn_mode(config: Any, *, request_id: Any, conversation_id: Any) -> None:
    """Once per turn (per request id), before the block is built: did the person flip the mode since the agent last
    knew it? The answer rides the config for every call of this turn (``agent_mode_person_set``), and the mode now
    becomes the one the agent knows (in memory and in the conversation's metadata)."""
    if not getattr(config, "agent_modes", None):
        return
    turn = _text(request_id) or "-"
    if getattr(config, "agent_mode_settled_request", None) == turn:
        return
    current = current_mode(config.agent_modes, getattr(config, "agent_mode", None))
    key = current["key"] if current else None
    config.agent_mode_person_set = person_set_this_turn(getattr(config, "agent_mode_known", None), key)
    config.agent_mode_settled_request = turn
    config.agent_mode_known = key
    remember_known_mode(conversation_id, key)


@dataclass
class RunningModes:
    """The running turn's modes, handed to a tool on ``ToolContext.running_modes``.

    ``switch`` sets the turn's ``agent_mode`` on the live config, so the next model call of the
    same tool loop is sent the new mode (the send boundary reads the config on every call)."""

    config: Any

    @property
    def modes(self) -> list[dict[str, str]]:
        return list(getattr(self.config, "agent_modes", None) or [])

    @property
    def current(self) -> dict[str, str] | None:
        return current_mode(self.modes, getattr(self.config, "agent_mode", None))

    def switch(self, key: str) -> None:
        """The agent's own switch: the mode it now knows is this one, and no person-set line follows (D17)."""
        self.config.agent_mode = key
        self.config.agent_mode_known = key
        self.config.agent_mode_person_set = None


def running_modes_for(config: Any) -> RunningModes | None:
    """A :class:`RunningModes` for a run whose agent has modes; ``None`` otherwise."""
    return RunningModes(config) if getattr(config, "agent_modes", None) else None
