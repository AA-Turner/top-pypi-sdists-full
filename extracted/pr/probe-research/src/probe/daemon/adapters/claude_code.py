"""Claude Code: `~/.claude/projects/<slug>/<sid>.jsonl`.

Line shapes read here (checked against real transcripts, 2026-09-26):

    {"type":"user","message":{"content":"..."}}                 a prompt (string)
    {"type":"user","isMeta":true,...}                           META (caveats, command output)
    {"type":"user","isCompactSummary":true,...}                 COMPACTION
    {"type":"user","message":{"content":"<task-notification>..."}}  META, not a person (E3)
    {"type":"user","message":{"content":[{"type":"tool_result",...}]}}  TOOL_OUTPUT
    {"type":"assistant","message":{"content":[text|thinking|tool_use]}}
    {"type":"system","subtype":"turn_duration"}                 TURN_END (every finished turn;
                                                                 `end_turn` misses 21% of turns)
    {"type":"system","subtype":"compact_boundary"}              COMPACTION
    {"type":"permission-mode","permissionMode":"bypassPermissions"}  session fact
    {"type":"attachment","attachment":{"type":"queued_command","commandMode":"prompt",
     "origin":{"kind":"human"},"prompt":"..."}}                 PROMPT typed while the agent
                                                                 worked (221 of 228 measured,
                                                                 2026-09-29, had no `user` line)

A queued prompt whose origin is not `human` (`peer`: another session's message,
`isMeta: true`; `auto-continuation`; missing) is META: the daemon sees it, never
as the researcher. A queued line whose `commandMode` is not `prompt` is not
read: a `task-notification`, or a `coordinator`/`peer` message to a helper
agent, which carries no mode.

A message another AGENT sent (origin `{"kind":"peer","from","name","body",...}`,
checked against real transcripts 2026-10-23) is META marked as one
(`events.PEER_TOOL`, its sender in `command`, its text the message alone). It
arrives two ways:

    {"type":"attachment","attachment":{"type":"queued_command","commandMode":"prompt",
     "isMeta":true,"origin":{"kind":"peer",...},"prompt":"<WRAPPER ...>\\n...\\n</WRAPPER>"}}
                                                                 the agent was working
    {"type":"user","isMeta":true,"origin":{"kind":"peer",...},
     "message":{"content":"Another Claude session sent a message:\\n<WRAPPER ...>..."}}
                                                                 the agent was idle

where WRAPPER is `cross-session-message from="uds:<socket>" from-name="<session
name>" from-mode="..."` (another session) or `agent-message from="<agent id>"` (a
helper agent's SendMessage, `name` its agent type). The line carries no sender
session id. Auto-continuation and every other META line stay unmarked.

A tool output over ~30 KB is replaced by a `<persisted-output>` preview naming
`<sid>/tool-results/<id>.txt`, where the full text lives (E4). Helper agents
write `<sid>/subagents/agent-<id>.jsonl` with a `.meta.json` naming the parent
tool call (E9); their lines carry `isSidechain: true`.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from probe.daemon.adapters.base import (
    MODE_BYPASS,
    MODE_DEFAULT,
    Adapter,
    Capabilities,
    ContextFile,
    SessionFiles,
    block_texts,
    event,
    existing,
    peer_message,
    persisted_path,
)
from probe.daemon import mailbox
from probe.daemon.events import Event, Kind

#: User-role strings no person typed.
_META_PREFIXES = (
    "<task-notification>",
    "<local-command",
    "<command-name>",
    "<command-message>",
    "<system-reminder>",
    "Caveat: The messages below were generated",
    "[Request interrupted",
)


def normalize_mode(mode: object) -> str | None:
    if not isinstance(mode, str) or not mode:
        return None
    return MODE_BYPASS if mode == "bypassPermissions" else MODE_DEFAULT


#: How every daemon-reads message the agent receives begins (`mailbox.TEXT_*`).
PROBE_MESSAGE_PREFIX = "[Probe] "

#: How a queued message another sender wrote begins (another session's
#: SendMessage, a channel, the daemon itself): never the researcher's, whatever
#: its `origin` says.
_NOT_TYPED_PREFIXES = ("<agent-message", "<channel", PROBE_MESSAGE_PREFIX)

#: Exactly what Claude Code writes when the reads hook's Stop waiter wakes the
#: agent (it prints only the reader's answers, then exits 2).
_STOP_WAKE = re.compile(r'\A<task-notification>\n<summary>Stop hook feedback</summary>\n</task-notification>\n'
                        r'<system-reminder>\nStop hook blocking error from command "[^"\n]*": (?P<body>.*)\n'
                        r'</system-reminder>\Z', re.S)


def _stop_wake_of_deliveries(text: str) -> bool:
    """Is this line only the reader's answers the Stop waiter woke the agent with?"""
    m = _STOP_WAKE.match(text)
    return bool(m) and not mailbox.before_deliveries(m.group("body")).strip()


#: `origin.kind` of a message another agent sent this session.
PEER_ORIGIN = "peer"
#: The wrapper around another agent's message, after the lead line a `user` copy
#: carries ("Another Claude session sent a message[ while you were working]:").
_PEER_WRAPPER = re.compile(r"\A\s*(?P<lead>Another Claude session sent a message[^\n]*\n)?"
                           r"<(?P<tag>cross-session-message|agent-message)(?P<attrs>(?:\s+[\w-]+=\"[^\"]*\")*)\s*>"
                           r"\n?(?P<body>.*?)\n?</(?P=tag)>", re.S)
_PEER_ATTR = re.compile(r'([\w-]+)="([^"]*)"')


def _peer(origin: object, text: str) -> "tuple[str, str | None, str | None] | None":
    """Another agent's message: `(its text without the wrapper, its sender's
    address, its sender's name)`; None when the line is not one, or its text is
    empty. A peer origin says so; so does the wrapper alone (no person types one),
    unless words follow it that the harness did not add (its lead line marks its
    own copy): then a person typed it around one, and the whole text is theirs."""
    by_origin = isinstance(origin, dict) and origin.get("kind") == PEER_ORIGIN
    m = _PEER_WRAPPER.match(text)
    if m and not by_origin and not m.group("lead") and text[m.end():].strip():
        m = None
    if not by_origin and not m:
        return None
    info: dict = origin if by_origin else {}  # type: ignore[assignment]
    attrs = dict(_PEER_ATTR.findall(m.group("attrs"))) if m else {}
    body = info.get("body")
    if not (isinstance(body, str) and body.strip()):
        body = m.group("body") if m else text
    sender = info.get("from") if isinstance(info.get("from"), str) else attrs.get("from")
    name = info.get("name") if isinstance(info.get("name"), str) else attrs.get("from-name")
    body = body.strip("\n")
    return (body, sender, name) if body.strip() else None


class ClaudeCode(Adapter):
    name = "claude_code"
    question_tool_name = "AskUserQuestion"
    capabilities = Capabilities(
        watch_log=True,
        subagent_logs=True,
        hooks=True,
        inject_line=True,  # UserPromptSubmit `additionalContext`
        question_tool=True,  # AskUserQuestion; PostToolUse carries the pick (S14's first task proves it)
        permission_mode=True,  # `permission-mode` lines, and `permission_mode` in every hook input
        instruction_files=("CLAUDE.md",),
        inject_tool=True,  # PostToolUse `additionalContext` (reads_hook.py)
        wake=True,  # Stop hook with `asyncRewake`: exit 2 wakes the model (interactive sessions only)
    )

    #: This session's side folder, set by `session_files` (the worker calls it
    #: before it parses a line): a persisted output is read only from there.
    side_dir: Path | None = None

    def session_files(self, transcript: Path) -> SessionFiles:
        side = transcript.with_suffix("")
        subagents = sorted((side / "subagents").glob("agent-*.jsonl")) if (side / "subagents").is_dir() else []
        self.side_dir = side / "tool-results"
        return SessionFiles(main=transcript, subagents=subagents, side_dir=self.side_dir)

    def subagent_event(self, path: Path) -> Event | None:
        meta: dict = {}
        try:
            meta = json.loads(path.with_suffix(".meta.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            pass
        label = meta.get("description") or meta.get("agentType") or path.stem
        return event(Kind.SUBAGENT, f"subagent:{path.stem}", 0, text=str(label),
                     parent=meta.get("toolUseId") if isinstance(meta.get("toolUseId"), str) else None)

    def permission_mode(self, obj: dict) -> str | None:
        if obj.get("type") == "permission-mode":
            return normalize_mode(obj.get("permissionMode"))
        return None

    def parse_line(self, obj: dict, *, stream: str, offset: int) -> list[Event]:
        kind = obj.get("type")
        ts = obj.get("timestamp") if isinstance(obj.get("timestamp"), str) else None
        cwd = obj.get("cwd") if isinstance(obj.get("cwd"), str) else None
        if kind == "system":
            sub = obj.get("subtype")
            if sub == "turn_duration":
                return [event(Kind.TURN_END, stream, offset, ts=ts, cwd=cwd)]
            if sub == "compact_boundary":
                return [event(Kind.COMPACTION, stream, offset, ts=ts, text="(the agent's context was compacted)")]
            return []
        if kind == "attachment":
            # Hook context. The reader's own `[Probe]` messages in it reach the
            # daemon whole from the mailbox's claim log (the worker's reader
            # stream), so they are cut here; `[Probe]` text left over (a wording
            # this CLI does not know) is still read.
            att = obj.get("attachment")
            if isinstance(att, dict) and att.get("type") == "hook_additional_context":
                text = "\n".join(t for t in (mailbox.before_deliveries(b).strip("\n")
                                             for b in block_texts(att.get("content"))) if t)
                if PROBE_MESSAGE_PREFIX in text:
                    return [event(Kind.META, stream, offset, ts=ts, text=text)]
            if isinstance(att, dict) and att.get("type") == "queued_command":
                return self._queued(obj, att, stream=stream, offset=offset, ts=ts, cwd=cwd)
            return []
        message = obj.get("message")
        if kind not in ("user", "assistant") or not isinstance(message, dict):
            return []
        if obj.get("isSidechain") and stream == "main":
            return []  # a helper agent's line: read from its own log
        content = message.get("content")
        common = {"ts": ts, "cwd": cwd}
        if kind == "user":
            if obj.get("isCompactSummary"):
                return [event(Kind.COMPACTION, stream, offset, text="\n".join(block_texts(content)), **common)]
            events: list[Event] = []
            if isinstance(content, str):
                content = [{"type": "text", "text": content}]
            origin = obj.get("origin")
            if isinstance(origin, dict) and origin.get("kind") == PEER_ORIGIN:
                # Another agent's message, the agent idle: one event, whatever its blocks.
                peer = _peer(origin, "\n".join(block_texts(content)))
                if peer is not None:
                    return [peer_message(stream, offset, text=peer[0], sender_from=peer[1], sender_name=peer[2],
                                         **common)]
            for block in content if isinstance(content, list) else []:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "text" and isinstance(block.get("text"), str):
                    text = block["text"]
                    meta = obj.get("isMeta") or text.lstrip().startswith(_META_PREFIXES) or stream != "main"
                    if meta and _stop_wake_of_deliveries(text):
                        continue  # the reader's answers: whole from the claim log
                    peer = _peer(None, text) if meta else None
                    if peer is not None:
                        events.append(peer_message(stream, offset, text=peer[0], sender_from=peer[1],
                                                   sender_name=peer[2], **common))
                        continue
                    events.append(event(Kind.META if meta else Kind.PROMPT, stream, offset, text=text, **common))
                elif block.get("type") == "tool_result":
                    text = "\n".join(block_texts(block.get("content")))
                    events.append(event(Kind.TOOL_OUTPUT, stream, offset, text=text, call_id=block.get("tool_use_id"),
                                        is_error=bool(block.get("is_error")),
                                        side_file=persisted_path(text, self.side_dir), **common))
            return events
        events = []
        for block in content if isinstance(content, list) else []:
            if not isinstance(block, dict):
                continue
            btype = block.get("type")
            if btype == "text" and isinstance(block.get("text"), str) and block["text"].strip():
                events.append(event(Kind.AGENT_TEXT, stream, offset, text=block["text"], **common))
            elif btype == "thinking" and isinstance(block.get("thinking"), str) and block["thinking"].strip():
                events.append(event(Kind.AGENT_REASONING, stream, offset, text=block["thinking"], **common))
            elif btype == "tool_use":
                tool_input = block.get("input") if isinstance(block.get("input"), dict) else {}
                events.append(event(Kind.TOOL_CALL, stream, offset, tool=str(block.get("name") or ""),
                                    call_id=block.get("id"), tool_input=tool_input, **common))
        return events

    def _queued(self, obj: dict, att: dict, *, stream: str, offset: int, ts: str | None,
                cwd: str | None) -> list[Event]:
        """A message Claude Code slipped in between the agent's steps."""
        if obj.get("isSidechain") and stream == "main":
            return []  # a helper agent's line: read from its own log
        if att.get("commandMode") != "prompt":
            return []
        text = "\n".join(block_texts(att.get("prompt")))
        if not text.strip():
            return []
        origin = att.get("origin")
        peer = _peer(origin, text)
        if peer is not None:
            # Another agent's message (another session, a helper agent): never the
            # researcher's, and marked so its consumers can tell it apart.
            return [peer_message(stream, offset, ts=ts, cwd=cwd, text=peer[0], sender_from=peer[1],
                                 sender_name=peer[2], mid_turn=True)]
        human = (isinstance(origin, dict) and origin.get("kind") == "human"
                 and not att.get("isMeta") and not obj.get("isMeta")
                 and not text.lstrip().startswith(_META_PREFIXES + _NOT_TYPED_PREFIXES))
        kind = Kind.PROMPT if human and stream == "main" else Kind.META
        return [event(kind, stream, offset, ts=ts, cwd=cwd, text=text)]

    def context_files(self, cwd: Path, home: Path) -> list[ContextFile]:
        candidates: list[tuple[str, Path]] = []
        # The project's instruction files, from the working folder up to the repo root.
        folder = cwd
        for _ in range(8):
            candidates.append((f"CLAUDE.md in {folder}", folder / "CLAUDE.md"))
            candidates.append((f"CLAUDE.local.md in {folder}", folder / "CLAUDE.local.md"))
            if (folder / ".git").exists() or folder.parent == folder or folder == home:
                break
            folder = folder.parent
        candidates.append(("user CLAUDE.md", home / ".claude" / "CLAUDE.md"))
        # The agent's memory for this project: ~/.claude/projects/<slug>/memory/MEMORY.md.
        slug = str(cwd).replace("/", "-").replace(".", "-")
        memory = home / ".claude" / "projects" / slug / "memory"
        candidates.append(("MEMORY.md (the agent's memory)", memory / "MEMORY.md"))
        found = existing(candidates)
        skills = home / ".claude" / "skills"
        if skills.is_dir():
            count = sum(1 for p in skills.glob("*/SKILL.md"))
            if count:
                found.append(ContextFile(f"{count} installed skills under ~/.claude/skills", skills))
        return found
