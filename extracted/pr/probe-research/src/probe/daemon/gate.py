"""The ML gate: the daemon pauses itself in a session that is not ML work.

Most of what the daemon spent in its first fortnight went to sessions that
were not ML work (daemon cost cut W3, 2026-10-06). So the worker asks Probe
(`POST /v1/companion/classify`, which asks Jev) whether this session is ML
work, and pauses itself when it is confidently not -- ONLY where the session's
state is a default, never one the researcher set (`session_marker.
state_source`; Richard 2026-10-06: "only if the researcher didnt explicit set
the state either at the beginning or during the conversation").

A PAUSE LOSES NOTHING. It is a marker beside the switch
(`session_marker.set_auto_pause`), not a state: while it stands the writer
starts no bite and the reader takes no unasked turn, the events stay queued,
and once it lifts the writer records them. The researcher sees it on the
status line (`on (daemon) · paused: not ML`) and ends it for good with any
`/probe ...`.

THE POLICY, the consensus rule the team's earlier auto-tracking study kept
(Probe project `auto-session-tracking`): anything that says ML wins.

- DETERMINISTIC SIGNALS say ML, never "not ML", and cost no call: a framework
  or `import probe` / `probe.init(` / `probe.log(` in a Python file the agent
  wrote (never the SDK's own source), a training or job launch or `probe exec`
  the shell ran (never text a command only writes), a Probe SDK run event (the
  SDK really ran), a notebook, `nvidia-smi`. One signal and the session is ML for good: the gate
  never asks again and lifts a pause at once.
- JEV is asked when each of the researcher's first ASK_TURNS turns ends (or
  the next prompt arrives). The gate pauses when the last PAUSE_ANSWERS
  answers are all below PAUSE_BELOW and no signal fired -- two answers, and a
  margin wide, because Jev drifts +-0.06 on identical input.
- WHILE PAUSED: signals on every event, Jev at every new researcher prompt.
  The pause holds only on an ACTING answer below RESUME_AT: an answer at or
  above it, the server off or in shadow, the team off its list, an outage or
  no answer lifts it (a rollback undoes every pause; an outage fails open).
- Never the folder's history (that study: anti-causal, it silenced 10 of 11
  research sessions).

In SHADOW (the server answers `act: false`) the gate never pauses: it writes
`gate` lines to the writer's trace with what it would have done -- after a
`would_pause` it asks at every new prompt as a pause would, and writes
`would_resume` where a pause would have lifted.

The digest Jev reads is the researcher's prompts, the agent's commands (first
line), the files it wrote and the tools it used: never a tool's output.
"""

from __future__ import annotations

import json
import logging
import re
import time
from collections import Counter
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

log = logging.getLogger("probe.daemon")

ROUTE = "/v1/companion/classify"
#: Ask Jev when each of the researcher's first this-many turns ends.
ASK_TURNS = 3
#: Pause when the last PAUSE_ANSWERS answers are all below PAUSE_BELOW...
PAUSE_ANSWERS = 2
PAUSE_BELOW = 0.15
#: ...and lift a pause at RESUME_AT or above.
RESUME_AT = 0.5
#: The digest's size: Jev's request budget is ~90K characters.
DIGEST_CHARS = 80_000
PROMPT_CHARS = 2_000
COMMAND_CHARS = 300
#: One question's wall clock. The gate never waits longer than this per check.
TIMEOUT_S = 10.0
#: Facts in the session's store, so a restarted worker carries on.
FACT_SEQ = "gate_seq"
FACT_PROMPTS = "gate_prompts"
FACT_ENDED = "gate_turns_ended"
FACT_ASKED = "gate_asked"
FACT_ANSWERS = "gate_answers"
FACT_SIGNAL = "gate_signal"
FACT_WOULD = "gate_would_pause"
#: In shadow, the gate WOULD be paused now (it asks as a pause would).
FACT_SHADOW = "gate_shadow_paused"

MAIN = "main"
#: The arguments that carry what a call WROTE (content, an edit, a patch).
_WRITE_KEYS = ("content", "new_string", "new_source", "edits", "patch", "input", "text")
#: The arguments that name the file a call wrote.
_PATH_KEYS = ("file_path", "path", "notebook_path", "filename")

#: Code the agent wrote that imports an ML framework, or uses the Probe SDK the
#: way a training script does (`import probe`, `probe.init(`, `probe.log(`).
#: Never `from probe import ...` or `from probe.sdk ...`: that is work ON Probe.
_IMPORTS = re.compile(
    r"^\s*(?:import|from)\s+(?:torch|torchvision|jax|flax|transformers|wandb|lightning|"
    r"pytorch_lightning|sklearn|tensorflow|keras|datasets|accelerate|deepspeed|trl|peft|vllm|"
    r"xgboost|lightgbm|optax|timm)\b|^\s*import\s+probe\s*(?:$|as\b)",
    re.MULTILINE)
_SDK_CALLS = re.compile(r"\bprobe\.(?:init|log)\(")
#: Commands the agent RAN that launch training, evaluation or a job on
#: accelerators, or a run through the Probe CLI's launcher (`probe exec`: only
#: in a command, never in a file the agent wrote). A python script counts when
#: a word of its name is train / finetune / sweep / eval (`train.py`,
#: `my_train.py`, `eval_digits.py`; not `constraint.py`, `resweep_x.py`).
_LAUNCH = re.compile(
    r"\b(?:torchrun|deepspeed|sbatch|srun|nvidia-smi)\b|\baccelerate\s+launch\b|\bmodal\s+run\b|"
    r"\bprobe\s+exec\b|"
    r"\bpython[0-9.]*\s+(?:-u\s+)?(?:-m\s+)?(?:\S*[/_.\-])?(?:train|finetune|fine_tune|sweep|eval)(?=[_.\-\s]|$)",
    re.IGNORECASE)
#: The folder check's line for a notebook the agent created or changed.
_NOTEBOOK_CHANGE = re.compile(r"^(?:new file|changed) (.+?\.ipynb) \(")
#: A heredoc's body (kept: the rest of its first line, which is still shell).
_HEREDOC = re.compile(r"<<-?[ \t]*(['\"]?)(\w+)\1([^\n]*)\n(?:.*?\n)??[ \t]*\2[ \t]*(?:\n|$)", re.DOTALL)
_QUOTED = re.compile(r"'[^']*'|\"(?:[^\"\\]|\\.)*\"")
#: Written code counts in a Python file only, and never in the Probe SDK's own
#: source (`src/probe/...`): a plan, a doc or the SDK itself that mentions
#: `probe.init(` is work ON Probe, not ML work.
_CODE_FILE = re.compile(r"\.pyw?$")
_PROBE_SOURCE = re.compile(r"(?:^|/)src/probe/")
_PATCH_FILE = re.compile(r"^\*\*\* (?:Add|Update) File: (.+)$", re.MULTILINE)


@dataclass
class Answer:
    """What `POST /v1/companion/classify` said. `p_ml` None: no answer."""

    p_ml: float | None
    act: bool = False
    mode: str = "off"


Classify = Callable[[str], Awaitable[Answer]]


# -- reading events -----------------------------------------------------------
def _input(row: Any) -> dict:
    raw = row["tool_input"]
    if not raw:
        return {}
    try:
        value = json.loads(raw)
    except ValueError:
        return {}
    return value if isinstance(value, dict) else {}


def _written(tool_input: dict) -> str:
    """The text a tool call wrote (an edit's new text, a file's content, a patch)."""
    parts: list[str] = []
    for key in _WRITE_KEYS:
        value = tool_input.get(key)
        if isinstance(value, str):
            parts.append(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    parts.extend(v for k, v in item.items() if k in _WRITE_KEYS and isinstance(v, str))
    return "\n".join(parts)


def written_paths(row: Any, tool_input: dict | None = None) -> list[str]:
    """The files a tool call wrote: a path argument beside written content, or a
    patch's file headers."""
    tool_input = _input(row) if tool_input is None else tool_input
    paths = [m.strip() for m in _PATCH_FILE.findall(_written(tool_input) + "\n" + (row["command"] or ""))]
    if _written(tool_input) or row["tool"] and "notebook" in str(row["tool"]).lower():
        paths += [v for k in _PATH_KEYS if isinstance(v := tool_input.get(k), str) and v]
    return paths


def ml_signal(row: Any) -> str | None:
    """The deterministic ML signal in one event, or None. Says ML, never "not ML"."""
    kind = row["kind"]
    if kind == "run_event":
        return "a Probe run event"  # the SDK announced a run over the local socket
    if kind == "file_change":
        hit = _NOTEBOOK_CHANGE.match(row["text"] or "")
        return f"notebook {_one_line(hit.group(1))}" if hit else None
    if kind != "tool_call":
        return None
    tool_input = _input(row)
    command = row["command"] or ""
    if command:
        # Not `probe.init(` in code python ran (`-c`, a heredoc): an agent edits
        # Probe's own files that way. Code that really runs the SDK announces a
        # run over the local socket: a `run_event`, the signal above.
        hit = _LAUNCH.search(shell_part(command))
        if hit:
            return f"ran `{_one_line(hit.group(0))}`"
    code = _written(tool_input)
    if code and any(_CODE_FILE.search(path) and not _PROBE_SOURCE.search(path)
                    for path in written_paths(row, tool_input)):
        hit = _IMPORTS.search(code) or _SDK_CALLS.search(code)
        if hit:
            return f"wrote `{_one_line(hit.group(0))}`"
    for path in written_paths(row, tool_input):
        if path.endswith(".ipynb"):
            return f"wrote {_one_line(path)}"
    return None


def shell_part(command: str) -> str:
    """What the shell itself runs: heredoc bodies and quoted strings blanked, so
    text a command only writes (a CHANGELOG line, a doc) never reads as run."""
    return _QUOTED.sub("''", _HEREDOC.sub(lambda m: f"<<{m.group(2)}{m.group(3)}\n", command))


def _one_line(text: Any, limit: int = COMMAND_CHARS) -> str:
    """One line of plain text: every run of whitespace (newlines included) one
    space, so nothing the agent wrote can start a line of the digest."""
    return " ".join(str(text).split())[:limit]


def digest(rows: list[Any], *, limit: int = DIGEST_CHARS) -> str:
    """The session as Jev reads it, oldest first: prompts, commands, files
    written, and the tools used. Over `limit`, the oldest lines go -- all but
    the researcher's first prompt, which says what the session is for."""
    lines: list[str] = []
    tools: Counter = Counter()
    for row in rows:
        if row["kind"] == "prompt":
            if row["stream"] != MAIN:
                continue
            text = " ".join((row["text"] or "").split())[:PROMPT_CHARS]
            if text:
                lines.append(f"[researcher] {text}")
            continue
        tool = _one_line(row["tool"] or "", 80)
        if tool:
            tools[tool] += 1
        command = (row["command"] or "").strip()
        if command:
            lines.append(f"[command] {_one_line(command.splitlines()[0])}")
        for path in written_paths(row):
            path = _one_line(path)
            if path:
                lines.append(f"[wrote] {path}")
    head = "tools used: " + ", ".join(f"{name} x{n}" for name, n in tools.most_common()) if tools else ""
    first = next((i for i, line in enumerate(lines) if line.startswith("[researcher]")), None)
    kept: list[str] = []
    used = len(head) + 1
    for i in range(len(lines) - 1, -1, -1):
        if i == first:
            continue
        if used + len(lines[i]) + 1 > limit - (len(lines[first]) + 1 if first is not None else 0):
            break
        kept.append(lines[i])
        used += len(lines[i]) + 1
    kept.reverse()
    if first is not None:
        kept.insert(0, lines[first])
    return "\n".join(([head] if head else []) + kept)


# -- where a pause lives --------------------------------------------------------
class Marker:
    """The pause marker beside the session's switch (`session_marker`)."""

    def __init__(self, session_id: str) -> None:
        self.sid = session_id

    def applies(self) -> bool:
        from probe.sdk import session_marker as sm

        return (sm.session_state(self.sid) in sm.PAUSABLE_STATES
                and sm.state_source(self.sid) == sm.SOURCE_DEFAULT)

    def paused(self) -> bool:
        from probe.sdk import session_marker as sm

        return sm.auto_paused(self.sid)

    def pause(self, record: dict) -> bool:
        from probe.sdk import session_marker as sm

        return sm.set_auto_pause(self.sid, record)

    def resume(self) -> bool:
        from probe.sdk import session_marker as sm

        return sm.clear_auto_pause(self.sid)


class Gate:
    def __init__(self, store, marker, classify: Classify, *, trace=None, clock=time.time) -> None:
        self.store = store
        self.marker = marker
        self.classify = classify
        self.trace = trace
        self.clock = clock
        #: The last check's verdict, read by the worker and the reader each poll.
        #: Starts from the marker, so a restarted worker's reader takes no unasked
        #: turn before the first check.
        try:
            self.paused = bool(marker.paused())
        except Exception:  # noqa: BLE001 -- unreadable: records
            self.paused = False

    def _fact(self, key: str, default: Any = None) -> Any:
        value = self.store.fact(key)
        return default if value is None else value

    def _line(self, decision: str, **fields: Any) -> None:
        if self.trace is not None:
            self.trace.write({"type": "gate", "decision": decision, **fields})

    def note(self, decision: str, **fields: Any) -> None:
        """A `gate` trace line from outside a check (the worker's session end)."""
        self._line(decision, **fields)

    def _set(self, key: str, value: Any) -> None:
        with self.store.tx():
            self.store.set_fact(key, value)

    async def check(self) -> bool:
        """Read what arrived, ask when due, pause or lift. True while paused.
        Never raises: a gate that fails keeps the daemon recording."""
        try:
            self.paused = await self._check()
        except Exception as exc:  # noqa: BLE001 -- the gate never stops the daemon
            log.warning("the ML gate failed (the daemon records): %s: %s", type(exc).__name__, exc)
            self.paused = False
        return self.paused

    async def _check(self) -> bool:
        if not self.marker.applies():
            return False
        seq = int(self._fact(FACT_SEQ, 0))
        prompts = int(self._fact(FACT_PROMPTS, 0))
        ended = int(self._fact(FACT_ENDED, 0))
        signal = self._fact(FACT_SIGNAL)
        new_prompt = False
        rows = self.store.gate_rows(seq)
        for row in rows:
            seq = row["seq"]
            if row["kind"] == "prompt" and row["stream"] == MAIN:
                # A new prompt ends the turn before it, whether or not its end was logged.
                ended = max(ended, prompts)
                prompts += 1
                new_prompt = True
            elif row["kind"] == "turn_end" and row["stream"] == MAIN:
                ended = max(ended, prompts)
            if signal is None:
                signal = ml_signal(row)
        if rows:
            with self.store.tx():
                self.store.set_fact(FACT_SEQ, seq)
                self.store.set_fact(FACT_PROMPTS, prompts)
                self.store.set_fact(FACT_ENDED, ended)
                if signal is not None and self._fact(FACT_SIGNAL) is None:
                    self.store.set_fact(FACT_SIGNAL, signal)
                    self._line("ml_signal", signal=signal, prompts=prompts)
        paused = self.marker.paused()
        shadow = bool(self._fact(FACT_SHADOW))
        if signal is not None:
            # ML for good: never asked about again, and a pause lifts at once.
            if paused and self.marker.resume():
                log.info("ML gate: %s -- the daemon records again", signal)
                self._line("resumed", reason=signal, prompts=prompts)
            if shadow:
                self._set(FACT_SHADOW, None)
                self._line("would_resume", reason=signal, prompts=prompts)
            return False
        asked = int(self._fact(FACT_ASKED, 0))
        if paused or shadow:
            due = new_prompt  # a pause (or, in shadow, what would be one) asks at every new prompt
        else:
            due = asked < min(ended, ASK_TURNS)
        if not due:
            return paused
        text = digest(self.store.digest_rows())
        answer = await self.classify(text)
        answers = [*list(self._fact(FACT_ANSWERS, [])), answer.p_ml][-ASK_TURNS:]
        with self.store.tx():
            self.store.set_fact(FACT_ASKED, max(asked, min(ended, ASK_TURNS)))
            self.store.set_fact(FACT_ANSWERS, answers)
        self._line("asked", p_ml=answer.p_ml, act=answer.act, mode=answer.mode, prompts=prompts,
                   turns_ended=ended, digest_chars=len(text))
        lifts = answer.p_ml is None or answer.p_ml >= RESUME_AT
        if paused:
            # A pause holds only on a fresh ACTING answer below RESUME_AT. The
            # server off or in shadow, a team taken off the list, an outage, no
            # answer: each lifts it, so a rollback undoes every pause and a Jev
            # outage fails open.
            if not answer.act or lifts:
                if self.marker.resume():
                    log.info("ML gate: p(ML)=%s act=%s -- the daemon records again", answer.p_ml, answer.act)
                    self._line("resumed", p_ml=answer.p_ml, act=answer.act, mode=answer.mode, prompts=prompts)
                return False
            return True
        if shadow:
            if lifts:
                self._set(FACT_SHADOW, None)
                self._line("would_resume", p_ml=answer.p_ml, mode=answer.mode, prompts=prompts)
                return False
        recent = answers[-PAUSE_ANSWERS:]
        if len(recent) < PAUSE_ANSWERS or any(p is None or p >= PAUSE_BELOW for p in recent):
            return False
        record = {"since": self.clock(), "p_ml": recent, "reason": "not ML work", "prompts": prompts}
        if not answer.act:
            if not self._fact(FACT_WOULD):
                with self.store.tx():
                    self.store.set_fact(FACT_WOULD, record)
                    self.store.set_fact(FACT_SHADOW, True)
                self._line("would_pause", p_ml=recent, mode=answer.mode, prompts=prompts)
            return False
        if self.marker.pause(record):
            if shadow:
                self._set(FACT_SHADOW, None)
            log.info("ML gate: p(ML)=%s -- not ML work: the daemon pauses (events stay queued)", recent)
            self._line("paused", p_ml=recent, mode=answer.mode, prompts=prompts)
            return True
        return False


# -- asking Probe -----------------------------------------------------------
async def ask_probe(text: str) -> Answer:
    """`POST /v1/companion/classify` with the daemon's key. Any failure is no
    answer (the daemon keeps recording)."""
    from probe.daemon import model as model_mod

    try:
        ep = model_mod.endpoint()
        resp = await model_mod._http_client().post(
            ep.base_url.rstrip("/") + ROUTE, json={"digest": text},
            headers={"Authorization": f"Bearer {ep.key}"}, timeout=TIMEOUT_S)
    except Exception as exc:  # noqa: BLE001
        log.info("ML gate: Probe did not answer: %s: %s", type(exc).__name__, exc)
        return Answer(p_ml=None)
    if resp.status_code != 200:
        log.info("ML gate: Probe answered %s", resp.status_code)
        return Answer(p_ml=None)
    try:
        body = resp.json()
        p = body.get("p_ml")
        p = float(p) if isinstance(p, (int, float)) and not isinstance(p, bool) and 0.0 <= p <= 1.0 else None
        return Answer(p_ml=p, act=bool(body.get("act")) and p is not None, mode=str(body.get("mode") or "off"))
    except (ValueError, AttributeError, TypeError):
        return Answer(p_ml=None)
