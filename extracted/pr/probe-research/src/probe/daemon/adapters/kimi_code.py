"""Kimi Code: `$KIMI_CODE_HOME/sessions/wd_<slug>_<hash>/session_<uuid>/agents/main/wire.jsonl`.

The wire holds two record families for the same conversation (Kimi Code 2.1.1,
checked against real sessions 2026-10-05). This adapter reads ONE of them, the
context family, so nothing is doubled:

    {"type":"context.append_message","message":{"role":"user","content":[...],
        "origin":{"kind":"user"|"injection"|"hook_result"|"system_trigger"|...}}}
                                                    PROMPT when origin.kind is "user",
                                                    else META (Kimi- or hook-made)
    {"type":"context.append_loop_event","event":{"type":"content.part",
        "part":{"type":"text"|"think",...}}}        AGENT_TEXT / AGENT_REASONING
    {"type":"context.append_loop_event","event":{"type":"tool.call",
        "toolCallId","name","args":{...}}}          TOOL_CALL (Bash `command`,
                                                    Write/Edit `path`)
    {"type":"context.append_loop_event","event":{"type":"tool.result",
        "toolCallId","result":{"output","isError"}}}  TOOL_OUTPUT
    {"type":"turn.ended"}                           TURN_END (every finished turn)
    {"type":"context.apply_compaction","summary"}   COMPACTION
    {"type":"context.clear"}                        COMPACTION (the context emptied)
    {"type":"permission.set_mode","mode":"auto"}    session fact; the last one wins

The other family (`agent.message.appended`, `"kind":"event"`) repeats the same
messages whole, but the assistant's and the tools' are written only when the
turn ENDS: read live, the context family shows a tool call as it happens.

A prompt typed while the agent works is either queued (it later arrives as an
ordinary turn) or steered into the running turn (`turn.steer` + `prompt.steered`
+ its own `context.append_message`, origin kind "user"): either way, one user
message with origin "user", so one PROMPT. `turn.prompt`/`turn.steer` repeat
that message and are not read.

Permission modes: `manual` (asks), `yolo` (asks for dangerous commands, sensitive
files and plan exit), `auto` (approves everything, denies AskUserQuestion; `kimi
-p` always runs in it). BYPASS is `auto` alone. Kimi's hook payloads carry no
mode, so the log is the only place it is seen.

Helper agents write `agents/agent-N/wire.jsonl` beside the main wire; they are
not read (their Agent tool call and its result are, on the main wire).
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from probe.daemon.adapters.base import (
    MODE_BYPASS,
    MODE_DEFAULT,
    Adapter,
    Capabilities,
    ContextFile,
    block_texts,
    event,
    existing,
)
from probe.daemon.events import Event, Kind

#: The one permission mode in which Kimi approves everything ("Never Ask").
BYPASS_MODE = "auto"
#: The origin of a user message a person typed (a prompt, or a steer mid-turn).
TYPED_ORIGIN = "user"
#: The folder Kimi Code keeps its files in, under $HOME unless KIMI_CODE_HOME says.
HOME_DIR = ".kimi-code"
HOME_ENV = "KIMI_CODE_HOME"


def normalize_mode(mode: object) -> str | None:
    if not isinstance(mode, str) or not mode:
        return None
    return MODE_BYPASS if mode == BYPASS_MODE else MODE_DEFAULT


def _ts(obj: dict) -> str | None:
    """A record's `time` (epoch milliseconds) as an ISO stamp, like the other harnesses'."""
    ms = obj.get("time")
    if isinstance(ms, bool) or not isinstance(ms, (int, float)):
        return None
    try:
        at = datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
    except (OverflowError, OSError, ValueError):
        return None
    return at.strftime("%Y-%m-%dT%H:%M:%S.") + f"{int(ms) % 1000:03d}Z"


def _output_text(output: object) -> str:
    """A tool result's `output`: text, or content parts (their text only: an
    image part's data is not text)."""
    if isinstance(output, str):
        return output
    if isinstance(output, list):
        return "\n".join(block_texts(output))
    if output is None:
        return ""
    return json.dumps(output, default=str)


class KimiCode(Adapter):
    name = "kimi_code"
    question_tool_name = "AskUserQuestion"
    capabilities = Capabilities(
        watch_log=True,
        subagent_logs=False,  # agents/agent-N/wire.jsonl are not read
        hooks=True,
        inject_line=True,  # UserPromptSubmit `{"message"}` (registry: prompt_context)
        question_tool=True,  # AskUserQuestion; its answer is the PostToolUse output
        # NOT trusted: a resumed session writes no new `permission.set_mode`, so a
        # session started in `auto` (every `kimi -p`) and resumed in the TUI would
        # still read as bypass, and the daemon would act without asking. Unknown
        # is "ask" (review, 2026-10-05).
        permission_mode=False,
        instruction_files=("AGENTS.md",),
        inject_tool=False,  # Kimi 2.1.1 fires PostToolUse and forgets it: its output reaches no one
        wake=False,  # a Stop hook also fires for helper agents, with no agent id (registry: wake)
    )

    def permission_mode(self, obj: dict) -> str | None:
        if obj.get("type") == "permission.set_mode":
            return normalize_mode(obj.get("mode"))
        return None

    def parse_line(self, obj: dict, *, stream: str, offset: int) -> list[Event]:
        kind = obj.get("type")
        ts = _ts(obj)
        if kind == "context.append_message":
            return self._message(obj.get("message"), stream=stream, offset=offset, ts=ts)
        if kind == "context.append_loop_event":
            loop = obj.get("event")
            return self._loop_event(loop, stream=stream, offset=offset, ts=ts) if isinstance(loop, dict) else []
        if kind == "turn.ended":
            return [event(Kind.TURN_END, stream, offset, ts=ts)]
        if kind == "context.apply_compaction":
            summary = obj.get("summary") if isinstance(obj.get("summary"), str) else ""
            return [event(Kind.COMPACTION, stream, offset, ts=ts,
                          text=summary if summary.strip() else "(the agent's context was compacted)")]
        if kind == "context.clear":
            return [event(Kind.COMPACTION, stream, offset, ts=ts, text="(the agent's context was cleared)")]
        return []

    def _message(self, message: object, *, stream: str, offset: int, ts: str | None) -> list[Event]:
        if not isinstance(message, dict) or message.get("role") != "user":
            return []
        origin = message.get("origin")
        typed = isinstance(origin, dict) and origin.get("kind") == TYPED_ORIGIN and stream == "main"
        kind = Kind.PROMPT if typed else Kind.META
        return [event(kind, stream, offset, ts=ts, text=text)
                for text in block_texts(message.get("content")) if text.strip()]

    def _loop_event(self, loop: dict, *, stream: str, offset: int, ts: str | None) -> list[Event]:
        etype = loop.get("type")
        if etype == "content.part":
            part = loop.get("part")
            if not isinstance(part, dict):
                return []
            if part.get("type") == "text" and isinstance(part.get("text"), str) and part["text"].strip():
                return [event(Kind.AGENT_TEXT, stream, offset, ts=ts, text=part["text"])]
            if part.get("type") == "think" and isinstance(part.get("think"), str) and part["think"].strip():
                return [event(Kind.AGENT_REASONING, stream, offset, ts=ts, text=part["think"])]
            return []
        if etype == "tool.call":
            args = loop.get("args") if isinstance(loop.get("args"), dict) else {}
            display = loop.get("display") if isinstance(loop.get("display"), dict) else {}
            cwd = display.get("cwd") if isinstance(display.get("cwd"), str) else None
            call_id = loop.get("toolCallId") if isinstance(loop.get("toolCallId"), str) else None
            return [event(Kind.TOOL_CALL, stream, offset, ts=ts, tool=str(loop.get("name") or ""),
                          call_id=call_id, tool_input=args, cwd=cwd)]
        if etype == "tool.result":
            result = loop.get("result") if isinstance(loop.get("result"), dict) else {}
            call_id = loop.get("toolCallId") if isinstance(loop.get("toolCallId"), str) else None
            return [event(Kind.TOOL_OUTPUT, stream, offset, ts=ts, text=_output_text(result.get("output")),
                          call_id=call_id, is_error=bool(result.get("isError")))]
        return []

    def context_files(self, cwd: Path, home: Path) -> list[ContextFile]:
        """What Kimi Code concatenates into its instructions: the project's
        `.kimi-code/AGENTS.md` and `AGENTS.md` from the working folder up to the
        repo root, then `$KIMI_CODE_HOME/AGENTS.md`."""
        candidates: list[tuple[str, Path]] = []
        folder = cwd
        for _ in range(8):
            candidates.append((f"AGENTS.md in {folder}", folder / "AGENTS.md"))
            candidates.append((f".kimi-code/AGENTS.md in {folder}", folder / HOME_DIR / "AGENTS.md"))
            if (folder / ".git").exists() or folder.parent == folder or folder == home:
                break
            folder = folder.parent
        override = (os.environ.get(HOME_ENV) or "").strip()
        kimi_home = Path(override).expanduser() if override else home / HOME_DIR
        candidates.append(("user AGENTS.md", kimi_home / "AGENTS.md"))
        return existing(candidates)
