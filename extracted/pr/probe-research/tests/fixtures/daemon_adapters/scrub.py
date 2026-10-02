#!/usr/bin/env python3
"""Make an adapter conformance fixture from a real chat log: STRUCTURE ONLY.

    python scrub.py <real.jsonl> <out.jsonl> [--lines N] [--start K]

Every string value is replaced by a placeholder except the structural keys the
adapters branch on (types, roles, subtypes, tool names, stop reasons, modes);
ids are re-numbered. What is left is the shape of a real session with none of
its words, so it may be committed (real transcripts never are).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re

KEEP_KEYS = {"type", "role", "subtype", "name", "stop_reason", "stopReason", "permissionMode", "approval_policy",
             "isMeta", "isSidechain", "isCompactSummary", "is_error", "isError", "toolName", "mode"}
ID_KEYS = {"id", "tool_use_id", "call_id", "toolCallId", "toolUseId", "uuid", "parentUuid", "sessionId",
           "session_id", "promptId", "turn_id", "agentId"}
UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")


def _stable(value: str, prefix: str) -> str:
    return prefix + hashlib.sha256(value.encode()).hexdigest()[:10]


TOOL_NAME = re.compile(r"^(?:[A-Z][A-Za-z]+|[a-z_]+|mcp__[A-Za-z0-9_-]+)$")


def _key(k: str) -> str:
    return _stable(k, "path-") if "/" in k or "." in k else k


def scrub(value, key: str | None = None):
    if isinstance(value, dict):
        return {_key(k): scrub(v, k) for k, v in value.items()}
    if isinstance(value, list):
        return [scrub(v, key) for v in value]
    if isinstance(value, str):
        if key == "name":
            return value if TOOL_NAME.match(value) else f"text-{len(value)}"
        if key in KEEP_KEYS:
            return value
        if key in ID_KEYS:
            return _stable(value, "id-")
        if key == "timestamp":
            return value
        if "<persisted-output>" in value:
            return "<persisted-output>\nOutput too large (64KB). Full output saved to: /x/tool-results/b1.txt\n"
        if value.lstrip().startswith(("<task-notification>", "<local-command", "<command-name>", "Caveat:",
                                      "<environment_context>", "<user_instructions>")):
            return value.lstrip()[:20] + " (scrubbed)"
        if key == "arguments":
            try:
                return json.dumps(scrub(json.loads(value)))
            except ValueError:
                return "{}"
        return f"text-{len(value)}"
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("src")
    parser.add_argument("out")
    parser.add_argument("--lines", type=int, default=120)
    parser.add_argument("--start", type=int, default=0)
    args = parser.parse_args()
    kept = []
    with open(args.src, encoding="utf-8") as handle:
        for i, line in enumerate(handle):
            if i < args.start:
                continue
            if len(kept) >= args.lines:
                break
            try:
                obj = json.loads(line)
            except ValueError:
                continue
            kept.append(json.dumps(scrub(obj), separators=(",", ":")))
    with open(args.out, "w", encoding="utf-8") as handle:
        handle.write("\n".join(kept) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
