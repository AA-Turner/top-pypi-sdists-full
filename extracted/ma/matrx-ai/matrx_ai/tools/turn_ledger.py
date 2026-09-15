"""THE TOOL-CALL LEDGER — the platform's own record of what this turn's tools did.

Why this module exists
----------------------
Agents are routinely given an ``output_schema`` that asks them to report their
own tool usage (``tools_worked`` / ``tools_failed`` / ``commands_run``). A model
asked to grade its own history does not do it honestly: the Sandbox Specialist
agent returned ``tools_failed: []`` on a run in which FOUR tool calls errored
(agent-efficiency-loop, 2026-09-14). No amount of prompting fixes a model lying
about its own past — so the platform stops asking and fills those fields itself,
from the same truth it writes to ``chat.tool_call``.

Two halves:

* **The ledger.** ``ToolExecutionLogger`` records every started / completed /
  errored / rejected call here at the exact moment it queues the matching
  ``chat.tool_call`` write. It is an in-process mirror of the ledger rows, which
  is what makes it readable MID-TURN: the rows themselves are deferred on the
  request's WriteCoordinator and are not visible to a DB read until the turn
  barrier flushes — long after the structured output has been parsed and
  returned. Scope is one ``execute_until_complete`` run, via a ContextVar, so a
  sub-agent's calls never leak into its parent's report (and vice versa).

* **The override.** ``apply_ledger_truth`` takes the parsed structured output
  plus the schema it was parsed against and OVERWRITES any top-level
  ``tools_worked`` / ``tools_failed`` / ``commands_run`` with ledger truth. Not
  a merge, not fill-if-empty: the model's version of these three fields is
  never evidence. Generic by construction — any agent whose schema declares
  those names inherits it, with no per-agent code.

Nothing here raises: a failure to establish ledger truth degrades to a LOUD
warning naming the remedy (law 4, nothing fails silently), never to a broken run.
"""

from __future__ import annotations

import json
from contextvars import ContextVar, Token
from dataclasses import dataclass, field
from typing import Any

from matrx_utils import vcprint

__all__ = [
    "LEDGER_TRUTH_FIELDS",
    "ToolLedgerEntry",
    "TurnToolLedger",
    "apply_ledger_truth",
    "get_turn_ledger",
    "record_tool_outcome",
    "record_tool_started",
    "reset_turn_ledger",
    "rewrite_ledger_truth_in_text",
    "schema_declares_ledger_fields",
    "start_turn_ledger",
]

#: The schema property names the platform owns. An agent that declares one of
#: these at the TOP LEVEL of its ``output_schema`` is asking the platform for
#: the truth, whatever the model wrote.
LEDGER_TRUTH_FIELDS = ("tools_worked", "tools_failed", "commands_run")

#: How much of a tool's error text survives into the report. Long enough that
#: the failure is diagnosable from the report alone, short enough that four of
#: them don't bury the rest of the output.
_ERROR_TEXT_LIMIT = 500
_COMMAND_TEXT_LIMIT = 1000

# Property names an object-shaped item may use for the tool name / the error /
# the command. First match in the schema's declared properties wins, so a
# schema that spells it ``tool_name`` gets ``tool_name`` and one that spells it
# ``tool`` gets ``tool`` — we never invent a key the schema did not declare
# (strict schemas set ``additionalProperties: false`` and would reject it).
_NAME_KEYS = ("tool", "tool_name", "name")
_ERROR_KEYS = ("error", "error_message", "message", "reason", "error_text")
_COMMAND_KEYS = ("command", "cmd", "commandline", "command_line")


@dataclass(slots=True)
class ToolLedgerEntry:
    """One tool call in this turn, as the PLATFORM saw it."""

    key: str
    tool_name: str
    status: str = "running"  # running | completed | error | rejected
    error_text: str | None = None
    #: The literal shell/exec command this call ran, when the tool declared a
    #: free-form ``command`` argument (see ``_derive_command``). None otherwise —
    #: never a guess.
    command: str | None = None


@dataclass(slots=True)
class TurnToolLedger:
    """Every tool call of one orchestrator run, in call order."""

    entries: list[ToolLedgerEntry] = field(default_factory=list)
    _by_key: dict[str, ToolLedgerEntry] = field(default_factory=dict)

    def upsert(self, key: str, tool_name: str) -> ToolLedgerEntry:
        entry = self._by_key.get(key)
        if entry is None:
            entry = ToolLedgerEntry(key=key, tool_name=tool_name or "unknown")
            self._by_key[key] = entry
            self.entries.append(entry)
        elif tool_name and entry.tool_name in ("", "unknown"):
            entry.tool_name = tool_name
        return entry


_TURN_LEDGER: ContextVar[TurnToolLedger | None] = ContextVar("matrx_turn_tool_ledger", default=None)

#: call key -> the ledger that recorded that call's START.
#:
#: THE CONTEXTVAR IS NOT ENOUGH, and this is the whole bug of 2026-09-15. A tool
#: call's terminal write (``log_completed`` / ``log_error``) does not always run
#: in the context that opened the ledger: out of a request coordinator the tool
#: executor hands that coroutine to ``detached_task``, which runs it in a FRESH
#: contextvars Context precisely so its DB write cannot land on the request's
#: transaction connection. A fresh Context has no ledger — so the outcome was
#: dropped silently, the entry stayed at ``running``, and the override then wrote
#: ``tools_failed: []`` over the model's text: the platform telling the same lie
#: it was built to stop.
#:
#: So the outcome is routed by the call's own key, back to the exact ledger that
#: recorded its start, wherever the writer happens to be running. Entries are
#: dropped when the ledger closes (``reset_turn_ledger``), so this never grows.
_LEDGER_BY_KEY: dict[str, TurnToolLedger] = {}


def _ledger_for(key: str) -> TurnToolLedger | None:
    """The ledger this call belongs to: the ambient one, else the one that
    recorded its start (a detached/forked writer), else None."""
    ledger = _TURN_LEDGER.get()
    if ledger is not None:
        return ledger
    return _LEDGER_BY_KEY.get(key) if key else None


def start_turn_ledger() -> Token:
    """Open a ledger for one orchestrator run. Returns the ContextVar token.

    Task-local, exactly like ``ExecutionState``: concurrent executors (parallel
    workflow agents, sub-agents) each get their own instance through the asyncio
    ContextVar fork, and tool tasks forked from a run inherit the SAME ledger
    object, so their appends are visible to the run that spawned them.
    """
    return _TURN_LEDGER.set(TurnToolLedger())


def reset_turn_ledger(token: Token) -> None:
    ledger = _TURN_LEDGER.get()
    if ledger is not None:
        for key in list(ledger._by_key):
            if _LEDGER_BY_KEY.get(key) is ledger:
                _LEDGER_BY_KEY.pop(key, None)
    try:
        _TURN_LEDGER.reset(token)
    except (ValueError, RuntimeError):  # different context — nothing to reset
        pass


def get_turn_ledger() -> TurnToolLedger | None:
    return _TURN_LEDGER.get()


def _truncate(text: Any, limit: int) -> str:
    value = "" if text is None else str(text)
    value = value.strip()
    if len(value) <= limit:
        return value
    return value[: limit - 1] + "…"


def _derive_command(arguments: Any, tool_def: Any) -> str | None:
    """The literal command this call ran — or None.

    Derived, never guessed: the argument must be a non-empty string under a
    command-shaped key AND the tool must declare that parameter as FREE-FORM.
    A tool whose ``command`` parameter is an enum is a dispatcher (the file /
    widget editors take ``command: "str_replace" | "append" | …``); its
    ``command`` is an opcode, not something anybody ran in a shell.
    """
    if not isinstance(arguments, dict):
        return None
    parameters = getattr(tool_def, "parameters", None)
    for key in _COMMAND_KEYS:
        value = arguments.get(key)
        if not isinstance(value, str) or not value.strip():
            continue
        declared = parameters.get(key) if isinstance(parameters, dict) else None
        if isinstance(declared, dict) and (declared.get("enum") or declared.get("const")):
            return None
        return _truncate(value, _COMMAND_TEXT_LIMIT)
    return None


def record_tool_started(
    *,
    key: str,
    tool_name: str,
    arguments: Any = None,
    tool_def: Any = None,
) -> None:
    """Mirror a ``chat.tool_call`` INSERT into this turn's ledger."""
    try:
        ledger = _TURN_LEDGER.get()
        if ledger is None or not key:
            return
        # Route this call's terminal write back here even if it runs in a
        # detached/forked context (see _LEDGER_BY_KEY).
        _LEDGER_BY_KEY[key] = ledger
        entry = ledger.upsert(key, tool_name)
        entry.status = "running"
        command = _derive_command(arguments, tool_def)
        if command:
            entry.command = command
    except Exception as exc:  # noqa: BLE001 — the ledger never breaks a run
        vcprint(f"[ToolLedger] record_tool_started failed: {exc}", color="yellow")


def record_tool_outcome(
    *,
    key: str,
    tool_name: str = "",
    status: str,
    error_text: Any = None,
) -> None:
    """Mirror a ``chat.tool_call`` terminal UPDATE into this turn's ledger."""
    try:
        ledger = _ledger_for(key)
        if ledger is None or not key:
            return
        entry = ledger.upsert(key, tool_name)
        entry.status = status
        if status in ("error", "rejected"):
            entry.error_text = _truncate(error_text or "Unknown error", _ERROR_TEXT_LIMIT)
    except Exception as exc:  # noqa: BLE001
        vcprint(f"[ToolLedger] record_tool_outcome failed: {exc}", color="yellow")


# ---------------------------------------------------------------------------
# The override
# ---------------------------------------------------------------------------


def _declared_fields(schema: Any) -> dict[str, dict]:
    if not isinstance(schema, dict):
        return {}
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        return {}
    return {
        name: properties[name]
        for name in LEDGER_TRUTH_FIELDS
        if isinstance(properties.get(name), dict)
    }


def schema_declares_ledger_fields(schema: Any) -> bool:
    return bool(_declared_fields(schema))


def _item_properties(field_schema: dict) -> dict | None:
    """The declared object properties of the array's items, or None if the
    schema wants plain strings (or says nothing — strings are the safe default:
    a string never violates a strict object schema's ``additionalProperties``)."""
    items = field_schema.get("items")
    if not isinstance(items, dict):
        return None
    if items.get("type") == "object" or isinstance(items.get("properties"), dict):
        properties = items.get("properties")
        return properties if isinstance(properties, dict) else {}
    return None


def _pick_key(properties: dict, candidates: tuple[str, ...], fallback: str) -> str:
    for candidate in candidates:
        if candidate in properties:
            return candidate
    return fallback


#: The text a call with NO terminal outcome carries into ``tools_failed``. A
#: call the platform started and never saw finish is NOT a success, and
#: silently dropping it would reproduce the exact lie this module exists to
#: stop — so it lands in the failure list, named for what it is.
_NO_TERMINAL_OUTCOME = (
    "no terminal outcome was recorded for this call — the platform started it and "
    "never saw it finish, so it is reported as a failure rather than assumed to have worked"
)


def _failed_values(entries: list[ToolLedgerEntry], field_schema: dict) -> list[Any]:
    failures = [e for e in entries if e.status != "completed"]
    for entry in failures:
        if entry.status not in ("error", "rejected"):
            vcprint(
                f"[ToolLedger] tool call '{entry.tool_name}' is still at status "
                f"{entry.status!r} at the structured-output chokepoint — no terminal "
                "outcome ever reached the ledger. It is reported as FAILED (never as a "
                "success, never dropped). Remedy: the call's log_completed / log_error "
                "must run in the same context as log_started.",
                color="red",
            )
    properties = _item_properties(field_schema)
    if properties is None:
        return [
            f"{e.tool_name}: {e.error_text or (_NO_TERMINAL_OUTCOME if e.status not in ('error', 'rejected') else 'Unknown error')}"
            for e in failures
        ]
    name_key = _pick_key(properties, _NAME_KEYS, "tool")
    error_key = _pick_key(properties, _ERROR_KEYS, "error")
    return [
        {
            name_key: e.tool_name,
            error_key: e.error_text
            or (
                _NO_TERMINAL_OUTCOME
                if e.status not in ("error", "rejected")
                else "Unknown error"
            ),
        }
        for e in failures
    ]


def _worked_values(entries: list[ToolLedgerEntry], field_schema: dict) -> list[Any]:
    names: list[str] = []
    for entry in entries:
        if entry.status == "completed" and entry.tool_name not in names:
            names.append(entry.tool_name)
    properties = _item_properties(field_schema)
    if properties is None:
        return names
    name_key = _pick_key(properties, _NAME_KEYS, "tool")
    return [{name_key: name} for name in names]


def _command_values(entries: list[ToolLedgerEntry], field_schema: dict) -> list[Any] | None:
    commands = [e.command for e in entries if e.command]
    if not commands:
        # NOT derivable from this turn's ledger — no call declared a free-form
        # command argument. Emitting [] here would be an invention dressed as
        # truth (an MCP tool can run a command under an argument name we cannot
        # recognize), so this field is left alone and the absence is announced.
        return None
    properties = _item_properties(field_schema)
    if properties is None:
        return commands
    command_key = _pick_key(properties, _COMMAND_KEYS, "command")
    return [{command_key: command} for command in commands]


def apply_ledger_truth(data: Any, schema: Any) -> Any:
    """Overwrite the schema's declared tool-report fields with ledger truth.

    ``data`` is the structured output just parsed out of the model's text;
    ``schema`` is the JSON Schema it was parsed against. Any top-level
    ``tools_worked`` / ``tools_failed`` / ``commands_run`` the schema declares is
    REPLACED (never merged, never filled-only-if-empty) by what this turn's tool
    ledger says actually happened.

    Returns ``data`` — mutated in place when there was something to correct.
    Never raises.
    """
    try:
        declared = _declared_fields(schema)
        if not declared or not isinstance(data, dict):
            return data

        ledger = get_turn_ledger()
        if ledger is None:
            vcprint(
                "[ToolLedger] An agent's output_schema declares "
                f"{sorted(declared)} but NO tool-call ledger is open for this turn, so "
                "the model's self-reported values are being passed through UNVERIFIED — "
                "treat them as a claim, not as truth. Remedy: this turn did not run under "
                "matrx_ai.orchestrator.executor.execute_until_complete (which opens the "
                "ledger via start_turn_ledger()); route the run through the orchestrator, "
                "or open a ledger around the call.",
                color="red",
            )
            return data

        entries = list(ledger.entries)
        for name, field_schema in declared.items():
            declared_type = field_schema.get("type")
            if declared_type not in (None, "array") and "array" not in (
                declared_type if isinstance(declared_type, list) else []
            ):
                vcprint(
                    f"[ToolLedger] '{name}' is declared as {declared_type!r}, not an array, so "
                    "the platform cannot fill it with ledger truth and the model's own value "
                    f"stands UNVERIFIED. Remedy: declare '{name}' as an array in the agent's "
                    "output_schema.",
                    color="yellow",
                )
                continue

            if name == "tools_failed":
                data[name] = _failed_values(entries, field_schema)
            elif name == "tools_worked":
                data[name] = _worked_values(entries, field_schema)
            elif name == "commands_run":
                commands = _command_values(entries, field_schema)
                if commands is None:
                    vcprint(
                        "[ToolLedger] 'commands_run' is declared but no tool call in this turn "
                        "carried a free-form command argument, so the platform has nothing to "
                        "derive it from and the model's own value stands UNVERIFIED (it is NOT "
                        "being blanked — inventing [] would be a lie of a different shape). "
                        "Remedy: declare the executing tool's command parameter as a free-form "
                        "string so the ledger can capture it.",
                        color="yellow",
                    )
                    continue
                data[name] = commands
        return data
    except Exception as exc:  # noqa: BLE001 — truth-filling never breaks a run
        vcprint(
            f"[ToolLedger] apply_ledger_truth failed ({exc}); the model's self-reported "
            "tool fields are passing through UNVERIFIED. Remedy: file this traceback — the "
            "override is supposed to be total.",
            color="red",
        )
        return data


# ---------------------------------------------------------------------------
# THE DURABLE HALF OF THE OVERRIDE
# ---------------------------------------------------------------------------
# ``apply_ledger_truth`` corrects the PARSED copy handed to the stream event and
# the output-apply dispatcher. That copy is ephemeral. The only durable record a
# turn leaves is its assistant TEXT (chat.message) — and every later consumer
# re-derives the structured answer by parsing that text again: the frontend, the
# v1/v2 API callers, ``matrx_ai.graph_nodes.shared._extract_structured_output``,
# a resume, a human reading the row. Correcting only the ephemeral copy is
# therefore not a fix: it leaves the model's ``tools_failed: []`` as the single
# durable truth of the run (proven live on conversations 74bcf027…, ed621e74…,
# 2026-09-15, both of whose first shell_execute errored).
#
# So the text itself is corrected, in place, BEFORE the turn's persistence
# barrier. After that every route and every consumer — now and a year from now,
# with no ledger in memory — reads truth, because there is nothing else to read.


def _locate_json_span(text: str, target: Any) -> tuple[int, int] | None:
    """The [start, end) span of the JSON document in ``text`` that decodes to
    ``target`` — or None. Scans every ``{``/``[`` and uses the stdlib decoder,
    so fences, prose, and trailing commentary around the object are preserved
    untouched when the span is replaced."""
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char not in "{[":
            continue
        try:
            value, end = decoder.raw_decode(text, index)
        except ValueError:
            continue
        if value == target:
            return index, end
    return None


def rewrite_ledger_truth_in_text(text: str, envelope: Any, schema: Any) -> str | None:
    """Return ``text`` with its structured answer's ledger fields corrected.

    Returns None when there is nothing to change: the schema declares none of
    the ledger fields, the text carries no parseable structured answer, the
    answer's ledger fields already match the ledger, or the JSON span cannot be
    located for an exact splice. Never raises.
    """
    try:
        if not text or not text.strip():
            return None
        if not schema_declares_ledger_fields(schema):
            return None

        from matrx_ai.agents.output import parse_agent_output

        extraction = parse_agent_output(text, envelope)
        if not extraction.success or not isinstance(extraction.data, dict):
            return None

        original = json.loads(json.dumps(extraction.data, default=str))
        corrected = apply_ledger_truth(extraction.data, schema)
        if corrected == original:
            return None

        span = _locate_json_span(text, original)
        if span is None:
            vcprint(
                "[ToolLedger] this turn's structured answer disagrees with the platform's "
                "tool ledger, but its JSON could not be located verbatim inside the "
                "assistant text, so the DURABLE text keeps the model's unverified values "
                "(the emitted structured_output event is still corrected). Remedy: file "
                "this — the parsed object is expected to appear literally in the text.",
                color="red",
            )
            return None

        start, end = span
        return text[:start] + json.dumps(corrected, indent=2, ensure_ascii=False) + text[end:]
    except Exception as exc:  # noqa: BLE001 — truth-filling never breaks a run
        vcprint(
            f"[ToolLedger] rewrite_ledger_truth_in_text failed ({exc}); this turn's durable "
            "text keeps the model's unverified tool fields. Remedy: file this traceback.",
            color="red",
        )
        return None
