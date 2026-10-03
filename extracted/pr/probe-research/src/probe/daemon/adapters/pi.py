"""pi: `~/.pi/agent/sessions/<cwd-slug>/<ts>_<id>.jsonl`.

    {"type":"message","message":{"role":"user"|"assistant"|"toolResult"|"bashExecution",...}}

pi has no hooks: its extension (`index.ts`) starts capture and writes the turn
file. Its session is a tree (abandoned branches keep their lines, E9); the
daemon reads lines in file order.
"""

from __future__ import annotations

from pathlib import Path

from probe.daemon.adapters.base import Adapter, Capabilities, ContextFile, block_texts, event, existing
from probe.daemon.events import Event, Kind


class Pi(Adapter):
    name = "pi"
    question_tool_name = None
    capabilities = Capabilities(
        watch_log=True,
        subagent_logs=False,
        hooks=False,  # the extension, not hooks
        inject_line=False,
        question_tool=False,
        permission_mode=False,
        instruction_files=("AGENTS.md",),
        inject_tool=True,  # the extension steers a message in mid-run (probe-research-pi/src/core/reads.ts)
        wake=True,  # an extension message with triggerTurn starts a turn for an answer
    )

    def parse_line(self, obj: dict, *, stream: str, offset: int) -> list[Event]:
        if obj.get("type") != "message":
            return []
        message = obj.get("message")
        if not isinstance(message, dict):
            return []
        ts = obj.get("timestamp") if isinstance(obj.get("timestamp"), str) else None
        role = message.get("role")
        content = message.get("content")
        if role == "user":
            return [event(Kind.PROMPT, stream, offset, ts=ts, text=t) for t in block_texts(content) if t.strip()]
        if role == "assistant":
            out: list[Event] = []
            for block in content if isinstance(content, list) else []:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "text" and isinstance(block.get("text"), str) and block["text"].strip():
                    out.append(event(Kind.AGENT_TEXT, stream, offset, ts=ts, text=block["text"]))
                elif block.get("type") == "thinking" and isinstance(block.get("thinking"), str):
                    out.append(event(Kind.AGENT_REASONING, stream, offset, ts=ts, text=block["thinking"]))
                elif block.get("type") == "toolCall":
                    args = block.get("arguments") if isinstance(block.get("arguments"), dict) else {}
                    out.append(event(Kind.TOOL_CALL, stream, offset, ts=ts, tool=str(block.get("name") or ""),
                                     call_id=block.get("id"), tool_input=args))
            if message.get("stopReason") == "stop":
                out.append(event(Kind.TURN_END, stream, offset, ts=ts))
            return out
        if role == "toolResult":
            return [event(Kind.TOOL_OUTPUT, stream, offset, ts=ts, text="\n".join(block_texts(content)),
                          tool=message.get("toolName") if isinstance(message.get("toolName"), str) else None,
                          call_id=message.get("toolCallId") if isinstance(message.get("toolCallId"), str) else None,
                          is_error=bool(message.get("isError")))]
        if role == "bashExecution":
            command = message.get("command") if isinstance(message.get("command"), str) else ""
            output = message.get("output") if isinstance(message.get("output"), str) else ""
            return [event(Kind.TOOL_CALL, stream, offset, ts=ts, tool="bash", tool_input={"command": command}),
                    event(Kind.TOOL_OUTPUT, stream, offset, ts=ts, text=output)]
        return []

    def context_files(self, cwd: Path, home: Path) -> list[ContextFile]:
        candidates: list[tuple[str, Path]] = []
        folder = cwd
        for _ in range(8):
            candidates.append((f"AGENTS.md in {folder}", folder / "AGENTS.md"))
            if (folder / ".git").exists() or folder.parent == folder or folder == home:
                break
            folder = folder.parent
        candidates.append(("user AGENTS.md", home / ".pi" / "agent" / "AGENTS.md"))
        return existing(candidates)
