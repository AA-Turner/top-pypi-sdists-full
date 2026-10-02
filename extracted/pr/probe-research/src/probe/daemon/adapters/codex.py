"""Codex: `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`.

    {"type":"session_meta","payload":{...}}                       session facts
    {"type":"turn_context","payload":{"approval_policy":"never",
        "sandbox_policy":{"type":"danger-full-access"},...}}      permission mode
    {"type":"response_item","payload":{"type":"message"|"function_call"|
        "function_call_output"|"custom_tool_call"|"custom_tool_call_output"|
        "local_shell_call"|"reasoning"}}
    {"type":"event_msg","payload":{"type":"task_complete"}}       TURN_END

Codex's reasoning is usually encrypted; only a plain `summary` is read. Helper
agents are separate rollouts that carry `parent_thread_id` (E9, to confirm).

BYPASS is `approval_policy: never` AND a `danger-full-access` sandbox. "never"
alone only means Codex asks nothing: inside a read-only or workspace sandbox the
harness still stops what it would ask about, so the daemon asks too.
"""

from __future__ import annotations

import json
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

_STARTUP_PREFIXES = ("<environment_context>", "<user_instructions>", "# AGENTS.md", "<permissions", "<turn_aborted>")
FULL_ACCESS = "danger-full-access"


def _sandbox(policy: object) -> str | None:
    """`{"type": "danger-full-access"}` (current) or the bare string (older rollouts)."""
    if isinstance(policy, dict):
        policy = policy.get("type") or policy.get("mode")
    return policy if isinstance(policy, str) else None


def _mode(context: dict) -> str | None:
    policy = context.get("approval_policy")
    if not isinstance(policy, str) or not policy:
        return None
    bypass = policy == "never" and _sandbox(context.get("sandbox_policy")) == FULL_ACCESS
    return MODE_BYPASS if bypass else MODE_DEFAULT


class Codex(Adapter):
    name = "codex"
    question_tool_name = None
    capabilities = Capabilities(
        watch_log=True,
        subagent_logs=True,
        hooks=True,
        inject_line=False,  # unconfirmed: requests wait for `probe approvals`
        question_tool=False,  # terminal fallback
        permission_mode=True,  # turn_context.approval_policy + sandbox_policy
        instruction_files=("AGENTS.md",),
        inject_tool=True,  # PostToolUse `additionalContext` (reads_hook.py, the shared hooks.json)
        wake=False,  # no rewake: a late answer waits for the next prompt or tool call
    )

    def permission_mode(self, obj: dict) -> str | None:
        if obj.get("type") == "turn_context" and isinstance(obj.get("payload"), dict):
            return _mode(obj["payload"])
        return None

    def parse_line(self, obj: dict, *, stream: str, offset: int) -> list[Event]:
        ts = obj.get("timestamp") if isinstance(obj.get("timestamp"), str) else None
        payload = obj.get("payload")
        if not isinstance(payload, dict):
            return []
        if obj.get("type") == "event_msg":
            if payload.get("type") == "task_complete":
                return [event(Kind.TURN_END, stream, offset, ts=ts)]
            if payload.get("type") in ("context_compacted", "compaction"):
                return [event(Kind.COMPACTION, stream, offset, ts=ts, text="(the agent's context was compacted)")]
            return []
        if obj.get("type") != "response_item":
            return []
        inner = payload.get("type")
        if inner == "message":
            role = payload.get("role")
            if role not in ("user", "assistant"):
                return []
            out = []
            for text in block_texts(payload.get("content")):
                if not text.strip():
                    continue
                if role == "assistant":
                    out.append(event(Kind.AGENT_TEXT, stream, offset, ts=ts, text=text))
                else:
                    meta = text.lstrip().startswith(_STARTUP_PREFIXES) or stream != "main"
                    out.append(event(Kind.META if meta else Kind.PROMPT, stream, offset, ts=ts, text=text))
            return out
        if inner == "reasoning":
            summary = payload.get("summary")
            texts = [s.get("text") for s in summary if isinstance(s, dict) and isinstance(s.get("text"), str)] \
                if isinstance(summary, list) else []
            text = "\n".join(t for t in texts if t and t.strip())
            return [event(Kind.AGENT_REASONING, stream, offset, ts=ts, text=text)] if text else []
        if inner == "function_call":
            raw = payload.get("arguments")
            try:
                args = json.loads(raw) if isinstance(raw, str) else (raw if isinstance(raw, dict) else {})
            except ValueError:
                args = {"arguments": raw}
            if not isinstance(args, dict):
                args = {"arguments": args}
            if isinstance(args.get("command"), list):
                args = {**args, "command": " ".join(str(part) for part in args["command"])}
            return [event(Kind.TOOL_CALL, stream, offset, ts=ts, tool=str(payload.get("name") or ""),
                          call_id=payload.get("call_id"), tool_input=args)]
        if inner == "local_shell_call":
            action = payload.get("action") if isinstance(payload.get("action"), dict) else {}
            command = action.get("command")
            text = " ".join(command) if isinstance(command, list) else str(command or "")
            return [event(Kind.TOOL_CALL, stream, offset, ts=ts, tool="shell",
                          call_id=payload.get("call_id") or payload.get("id"), tool_input={"command": text})]
        if inner == "custom_tool_call":
            value = payload.get("input") if isinstance(payload.get("input"), str) else ""
            return [event(Kind.TOOL_CALL, stream, offset, ts=ts, tool=str(payload.get("name") or "custom_tool"),
                          call_id=payload.get("call_id"), tool_input={"input": value})]
        if inner in ("function_call_output", "custom_tool_call_output", "local_shell_call_output"):
            output = payload.get("output")
            if isinstance(output, dict):
                output = output.get("content") or output.get("output") or json.dumps(output)
            elif isinstance(output, str):
                try:
                    parsed = json.loads(output)
                    if isinstance(parsed, dict) and isinstance(parsed.get("output"), str):
                        output = parsed["output"]
                except ValueError:
                    pass
            return [event(Kind.TOOL_OUTPUT, stream, offset, ts=ts, text=str(output or ""),
                          call_id=payload.get("call_id"))]
        return []

    def context_files(self, cwd: Path, home: Path) -> list[ContextFile]:
        candidates: list[tuple[str, Path]] = []
        folder = cwd
        for _ in range(8):
            candidates.append((f"AGENTS.md in {folder}", folder / "AGENTS.md"))
            if (folder / ".git").exists() or folder.parent == folder or folder == home:
                break
            folder = folder.parent
        candidates.append(("user AGENTS.md", home / ".codex" / "AGENTS.md"))
        return existing(candidates)
