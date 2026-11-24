"""What a step says — live progress lines any step announces as its work happens (``data.says``).

THE GENERAL PROBLEM. A person watching a run wants to read "Analyzed page 3 of 10" the moment
page 3 lands, not a pile of lines when the whole list is done. A step that adds a second "say"
step after the work can only speak AFTER it (and costs a step on the canvas per line). The
engine already knows when each step starts, finishes, fails and when each item of a For each
settles — so the lines ride those real events, rendered at that moment.

Authored on a node (opt-in; Studio shows it as "Says" on the step card)::

    "data": {"says": [
        {"on": "start",       "event": "analysis_start",    "message": "Analyzing {inputs.job.title}"},
        {"on": "each_item",   "event": "analysis_complete", "message": "Analyzed page {done} of {total}"},
        {"on": "item_failed", "event": "analysis_failed",   "message": "Page {item.job.title} failed: {error}"},
        {"on": "done",        "event": "analyze_all_complete", "message": "Analyzed {result.count} pages"},
    ]}

* ``on``: ``start`` (the step's ``node_started``) · ``done`` (``node_completed``) · ``failed``
  (``node_failed``) · ``each_item`` (an item of a For each settled and did not fail:
  ``item_settled`` outcome ``succeeded`` / ``reused``) · ``item_failed`` (``item_settled`` outcome
  ``failed``). Lines ride the step's own event as ``says: [{event, message}]`` — no new step, no
  new event type.
* ``event``: a short name a screen keys on (``analysis_complete``). A name, never a sentence.
* ``event_from`` + ``events`` (+ ``default``), instead of ``event``: the line's name is picked at render
  time from a DECLARED set — ``event_from`` is one placeholder (``"{result.outcome}"``), ``events`` maps each
  value it may have to an event name (``{"skipped": "item_skipped", "complete": "item_complete"}``),
  ``default`` (optional, one of those names) is said when the value is missing or not declared; with no
  default such a line is not said (and flagged like a missing placeholder). A line only ever carries a
  declared name; a row that picks its event with no ``events``, or a ``default`` it does not declare, is
  refused at publish.
* ``each``: one placeholder naming a list (``"{result.progress_events}"``): the row says ONE line per
  element, in list order, each element read as ``{each.x}`` (in ``message`` and ``event_from``) — a step
  that settles many things at once says a line per thing with no For each. A missing value or a
  non-list says nothing (flagged); at most ``EACH_LINES_MAX`` lines per row.
* ``message``: words with placeholders only — ``{inputs.x}`` (the step's inputs), ``{result.x}``
  (what it returned), ``{item.x}`` (a For each item's own inputs), ``{error}``, ``{done}``,
  ``{failed}``, ``{total}``. Nothing else: no expressions, no conditions. Dotted paths read into
  dicts and list indexes (``{inputs.pages.0.url}``). Text that is not a placeholder is kept as
  written, braces included.

THE RULES (each has a test in ``tests/test_says.py``):

* An unknown placeholder or a malformed row fails compilation (loud, at publish) — never a run.
* A value that is missing when the line renders becomes empty text; the line is still sent, and
  the step carries ONE ``engine.says_failed`` review flag per run naming the placeholder. A render
  can never fail the run.
* ``{done}`` / ``{failed}`` / ``{total}`` are the engine's counts of the step's For each items
  (``ItemSettledEvent.done`` / ``failed`` / ``total``): ``done`` counts items that succeeded or
  were reused, ``failed`` the failed ones, a skipped item neither. They survive a resume: a resumed
  leg rebuilds them from the recorded outcomes of THAT pass before any item of that step runs; a
  For each in a cycle counts each lap from zero (a pass is the step its items run at). A paced
  For each (``wave_size`` / ``until``) knows its list's length, so ``{total}`` is that length even
  when an ``until`` condition stops it early (2026-11-19; it used to be empty there).
* A row that can never have a value for its row type is a finding at save and refused at publish
  (``row_problems``, F4): ``{result.x}`` outside done / each item, ``{error}`` outside the failure
  rows, counts / ``{item.x}`` / the per-item rows on a step with no For each.
* Size (F12): at most ``ROWS_MAX`` rows per step; one value at most ``VALUE_MAX_CHARS``, the whole
  rendered line at most ``LINE_MAX_CHARS`` (cut, marked "…").
* Retries and resumes (F11): ``start`` is said on every attempt (a retried item says its start
  line again; the screen keeps one row per item). After a resume, an item whose last attempt
  failed and that waits to be retried counts in ``{failed}`` until it settles again — then it
  moves to ``{done}`` (a later settle of an item replaces its earlier one).
"""

from __future__ import annotations

import json
import re
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

SaysOn = Literal["start", "done", "failed", "each_item", "item_failed"]

#: Placeholders reading a path (``{inputs.job.title}``) and the bare ones (``{done}``).
PATH_ROOTS: frozenset[str] = frozenset({"inputs", "result", "item", "each"})
BARE_NAMES: frozenset[str] = frozenset({"error", "done", "failed", "total"})

#: A candidate placeholder: ``{`` + a word, then dotted segments + ``}``. Anything else in braces is text.
PLACEHOLDER_RE = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z0-9_\-]+)*)\}")

EVENT_NAME_RE = r"^[a-z][a-z0-9_:.\-]{0,79}$"

#: The longest value one placeholder puts into a message (a whole list or object is cut, marked).
VALUE_MAX_CHARS = 200
#: The longest a whole rendered line may be (many long values in one message are cut, marked) — F12.
LINE_MAX_CHARS = 500
#: The most rows one step may say (each rides an event the step sends anyway) — F12.
ROWS_MAX = 20  # protocol-constant: display cap on rows echoed in a says line, layout not a limit
#: The most lines one ``each`` row says on one event (the rest are not said; flagged) — F12.
EACH_LINES_MAX = 500  # protocol-constant: bounds one event's size, layout not a limit


class SaysLine(BaseModel):
    """One authored row of ``data.says``: a fixed ``event``, or one picked from the declared ``events``."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    on: SaysOn
    event: str | None = Field(default=None, pattern=EVENT_NAME_RE)
    event_from: str | None = None
    events: dict[str, str] | None = None
    default: str | None = Field(default=None, pattern=EVENT_NAME_RE)
    each: str | None = None
    message: str = Field(default="", max_length=500)

    @model_validator(mode="after")
    def _one_way_to_name_the_line(self) -> SaysLine:
        if (self.event is None) == (self.event_from is None):
            raise ValueError("name the line with event, or pick it with event_from + events (one of the two)")
        if self.event is not None and (self.events is not None or self.default is not None):
            raise ValueError("events and default go with event_from; a row with event says that one event")
        if self.event_from is not None:
            _one_placeholder(self.event_from, "event_from")
            if not self.events:
                raise ValueError("event_from picks from the events it declares: add events {value: event name}")
            for value, name in self.events.items():
                if not re.match(EVENT_NAME_RE, name):
                    raise ValueError(f"events: {value!r} -> {name!r} is not an event name")
            if self.default is not None and self.default not in self.events.values():
                raise ValueError(f"default {self.default!r} is not one of the declared events")
        if self.each is not None:
            if _one_placeholder(self.each, "each").partition(".")[0] == "each":
                raise ValueError("each names a list of the step ({result.x}, {inputs.x}, {item.x}), not {each.x}")
        elif any(n.partition(".")[0] == "each" for n in self.placeholders()):
            raise ValueError("{each.x} reads the element of an each row; add each")
        return self

    def placeholders(self) -> list[str]:
        """Every placeholder the row reads: its message, event_from and each."""
        out = placeholders_of(self.message)
        for raw in (self.event_from, self.each):
            if raw:
                out += placeholders_of(raw)
        return out

    def declared_events(self) -> tuple[str, ...]:
        """Every name a line of this row can carry."""
        return (self.event,) if self.event is not None else tuple(dict.fromkeys((self.events or {}).values()))


def _one_placeholder(raw: str, what: str) -> str:
    m = PLACEHOLDER_RE.fullmatch(raw.strip())
    if not m:
        raise ValueError(f"{what} is one placeholder, like {{result.outcome}} (got {raw!r})")
    return m.group(1)


class SaysPolicy(BaseModel):
    """A parsed ``data.says`` setting: the rows in authored order."""

    model_config = ConfigDict(frozen=True)

    lines: tuple[SaysLine, ...]

    def for_on(self, on: SaysOn) -> tuple[SaysLine, ...]:
        return tuple(line for line in self.lines if line.on == on)


class SaidLine(BaseModel):
    """One rendered line, as it rides the step's event (``says``)."""

    model_config = ConfigDict(frozen=True)

    event: str
    message: str


def placeholders_of(message: str) -> list[str]:
    return PLACEHOLDER_RE.findall(message)


def _placeholder_problem(name: str) -> str | None:
    root, _, rest = name.partition(".")
    if root in BARE_NAMES:
        return None if not rest else f"{{{name}}}: {{{root}}} takes no path"
    if root in PATH_ROOTS:
        return None if rest else f"{{{name}}}: name what to read, like {{{root}.title}}"
    allowed = ", ".join(sorted({f"{{{r}.x}}" for r in PATH_ROOTS} | {f"{{{b}}}" for b in BARE_NAMES}))
    return f"{{{name}}} is not a placeholder (use {allowed})"


def parse_says(raw: Any) -> SaysPolicy | None:
    """``data.says`` → a policy; None when absent or empty. Raises ``ValueError`` naming the problem."""
    if raw is None or raw == []:
        return None
    if not isinstance(raw, list):
        raise ValueError("says must be a list of {on, event, message} rows")  # event_from/events/each: see the doc
    if len(raw) > ROWS_MAX:
        raise ValueError(f"a step says at most {ROWS_MAX} rows ({len(raw)} written)")
    lines: list[SaysLine] = []
    for i, row in enumerate(raw):
        try:
            line = SaysLine.model_validate(row)
        except ValidationError as e:
            first = e.errors()[0]
            where = ".".join(str(p) for p in first.get("loc", ())) or "row"
            raise ValueError(f"row {i + 1}: {where}: {first.get('msg')}") from e
        for name in line.placeholders():
            problem = _placeholder_problem(name)
            if problem:
                raise ValueError(f"row {i + 1}: {problem}")
        lines.append(line)
    return SaysPolicy(lines=tuple(lines))


#: The rows a For each item's settle fires: they exist only on a step that runs once per item.
PER_ITEM_ONS: frozenset[str] = frozenset({"each_item", "item_failed"})
#: The rows a result exists on, and the rows an error exists on.
RESULT_ONS: frozenset[str] = frozenset({"done", "each_item"})
ERROR_ONS: frozenset[str] = frozenset({"failed", "item_failed"})
COUNT_NAMES: frozenset[str] = frozenset({"done", "failed", "total"})

_ON_WORDS = {"start": "when the step starts", "done": "when the step is done", "failed": "when the step fails",
             "each_item": "on each item", "item_failed": "when an item fails"}


def row_problems(policy: SaysPolicy, *, per_item: bool) -> list[str]:
    """What a row says that can never have a value for its row type (F4, checked at save and publish; each
    a sentence naming the row). ``per_item``: the step runs once per item of a For each (a dispatch target or
    an ``each`` connection's target)."""
    out: list[str] = []
    for i, line in enumerate(policy.lines, start=1):
        where = f"row {i} ({_ON_WORDS[line.on]})"
        if line.on in PER_ITEM_ONS and not per_item:
            out.append(f"{where} runs for each item of a For each, and this step has no For each")
            continue
        for name in dict.fromkeys(line.placeholders()):
            root = name.partition(".")[0]
            if root == "result" and line.on not in RESULT_ONS:
                out.append(f"{where}: {{{name}}} has no value {_ON_WORDS[line.on]}; use it when done or on each item")
            elif root == "error" and line.on not in ERROR_ONS:
                out.append(f"{where}: {{error}} has a value only when the step or an item fails")
            elif root in COUNT_NAMES | {"item"} and not per_item:
                out.append(f"{where}: {{{name}}} reads a For each's items, and this step has no For each")
    return out


_MISSING = object()


def _read_path(value: Any, path: list[str]) -> Any:
    for part in path:
        if isinstance(value, dict):
            value = value.get(part, _MISSING)
        elif isinstance(value, (list, tuple)) and part.lstrip("-").isdigit():
            idx = int(part)
            value = value[idx] if -len(value) <= idx < len(value) else _MISSING
        else:
            value = getattr(value, part, _MISSING) if isinstance(value, BaseModel) else _MISSING
        if value is _MISSING:
            return _MISSING
    return value


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, (str, int, float)):
        text = str(value)
    elif isinstance(value, BaseModel):
        text = json.dumps(value.model_dump(mode="json"), ensure_ascii=False, default=str)
    else:
        text = json.dumps(value, ensure_ascii=False, default=str)
    return text if len(text) <= VALUE_MAX_CHARS else text[: VALUE_MAX_CHARS - 1] + "…"


def _value_of(name: str, scope: dict[str, Any]) -> Any:
    root, _, rest = name.partition(".")
    value = scope.get(root, _MISSING)
    if rest and value is not _MISSING:
        value = _read_path(value, rest.split("."))
    return value


def _event_of(line: SaysLine, scope: dict[str, Any], missing: list[str]) -> str | None:
    """The row's event for this scope: its fixed ``event``, or the declared name ``event_from``'s value picks
    (``default`` when the value is missing or undeclared; None — say nothing — with no default)."""
    if line.event is not None:
        return line.event
    name = PLACEHOLDER_RE.fullmatch((line.event_from or "").strip())
    value = _value_of(name.group(1), scope) if name else _MISSING
    picked = (line.events or {}).get(_text(value)) if value is not _MISSING and value is not None else None
    if picked is None and line.default is None and name:
        missing.append(name.group(1))
    return picked or line.default


def render_row(line: SaysLine, scope: dict[str, Any]) -> tuple[list[SaidLine], list[str]]:
    """Every line one row says over ``scope``: one, none (an event_from with no declared pick and no default), or
    one per element of its ``each`` list. Returns the lines and the placeholders that had no value. Never raises."""
    missing: list[str] = []
    try:
        if line.each is None:
            said, gaps = render_line(line, scope)
            return ([said] if said is not None else []), gaps
        name = PLACEHOLDER_RE.fullmatch(line.each.strip())
        elements = _value_of(name.group(1), scope) if name else _MISSING
        if not isinstance(elements, (list, tuple)):
            return [], [name.group(1) if name else "each"]
        out: list[SaidLine] = []
        for element in list(elements)[:EACH_LINES_MAX]:
            said, gaps = render_line(line, {**scope, "each": element})
            missing.extend(gaps)
            if said is not None:
                out.append(said)
        if len(elements) > EACH_LINES_MAX:
            missing.append(f"{name.group(1) if name else 'each'} (over {EACH_LINES_MAX} lines)")
        return out, missing
    except Exception:  # noqa: BLE001 — a render never fails the run
        return [], [*missing, "*"]


def render_line(line: SaysLine, scope: dict[str, Any]) -> tuple[SaidLine | None, list[str]]:
    """Render one row over ``scope`` (``inputs`` / ``result`` / ``item`` / ``each`` / ``error`` / ``done`` /
    ``failed`` / ``total``). Returns the line (None when an ``event_from`` row picks nothing) and the
    placeholders that had no value (rendered empty). Never raises."""
    missing: list[str] = []
    try:
        event = _event_of(line, scope, missing)
    except Exception:  # noqa: BLE001 — a render never fails the run
        missing.append("*")
        event = line.default
    if event is None:
        return None, missing

    def _sub(m: re.Match[str]) -> str:
        name = m.group(1)
        root, _, rest = name.partition(".")
        if root not in PATH_ROOTS and root not in BARE_NAMES:
            return m.group(0)
        value = scope.get(root, _MISSING)
        if rest and value is not _MISSING:
            value = _read_path(value, rest.split("."))
        if value is _MISSING or value is None:
            missing.append(name)
            return ""
        try:
            return _text(value)
        except Exception:  # noqa: BLE001 — a value that will not print is a missing value
            missing.append(name)
            return ""

    try:
        message = PLACEHOLDER_RE.sub(_sub, line.message)
    except Exception:  # noqa: BLE001 — a render never fails the run
        missing.append("*")
        message = line.message
    if len(message) > LINE_MAX_CHARS:
        message = message[: LINE_MAX_CHARS - 1] + "…"
    return SaidLine(event=event, message=message), missing


def render_lines(
    policy: SaysPolicy | None, on: SaysOn, scope: dict[str, Any]
) -> tuple[list[SaidLine] | None, list[str]]:
    """Every row of ``policy`` for ``on``, rendered. ``(None, [])`` when the step says nothing then."""
    if policy is None:
        return None, []
    rows = policy.for_on(on)
    if not rows:
        return None, []
    said: list[SaidLine] = []
    missing: list[str] = []
    for row in rows:
        lines, gaps = render_row(row, scope)
        said.extend(lines)
        missing.extend(gaps)
    return (said or None), missing


class ItemTally:
    """The engine's count of ONE PASS of one dispatch's items (``{done}`` / ``{failed}`` / ``{total}``).

    A pass is the step the items run at: a For each in a cycle runs its list again on a later step
    under the same dispatch id, and that lap counts from zero (``step`` tells the passes apart).
    ``states`` is item_index → its settled outcome; a later settle of the same item (a retried
    failure that now succeeds) replaces the earlier one."""

    __slots__ = ("total", "states", "step")

    def __init__(self, total: int | None, step: int | None = None) -> None:
        self.total = total
        self.step = step
        self.states: dict[int, str] = {}

    def settle(self, item_index: int, outcome: str) -> None:
        self.states[item_index] = outcome

    @property
    def done(self) -> int:
        return sum(1 for s in self.states.values() if s in ("succeeded", "reused"))

    @property
    def failed(self) -> int:
        return sum(1 for s in self.states.values() if s == "failed")

    def scope(self) -> dict[str, Any]:
        return {"done": self.done, "failed": self.failed, "total": self.total}
