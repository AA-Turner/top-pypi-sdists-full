"""CLI hook entrypoints for pre-tool execution attribution."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import UTC, datetime
from pathlib import Path

from plato.utils.tool_execution import (
    DEFAULT_TOOL_EXECUTION_CONTEXT_PATH,
    ToolStartRecord,
    append_tool_start_record,
    load_tool_execution_context,
    normalize_tool_input,
)

logger = logging.getLogger(__name__)


def _write_record(mode: str, payload: dict[str, object]) -> None:
    context = load_tool_execution_context(DEFAULT_TOOL_EXECUTION_CONTEXT_PATH)
    if context is None:
        return

    hook_spool_path = Path(context.hook_spool_path)
    record = ToolStartRecord(
        source=mode,
        observed_at=datetime.now(UTC),
        tool_name=str(payload.get("tool_name", "")),
        normalized_tool_input=normalize_tool_input(payload.get("tool_input", {})),
        tool_use_id=(str(payload["tool_use_id"]) if isinstance(payload.get("tool_use_id"), str) else None),
        session_id=str(payload.get("session_id", "")),
        transcript_path=str(payload.get("transcript_path", "")),
        cwd=str(payload.get("cwd", "")),
    )
    append_tool_start_record(hook_spool_path, record)


def main(argv: list[str] | None = None) -> int:
    """Record pre-tool sidecar data for agent CLIs."""
    parser = argparse.ArgumentParser(description="Record pre-tool execution hook data")
    parser.add_argument(
        "mode",
        choices=("claude-pretooluse", "gemini-beforetool", "codex-pretooluse"),
    )
    args = parser.parse_args(argv)

    raw_payload = sys.stdin.read()
    if not raw_payload.strip():
        return 0

    try:
        payload = json.loads(raw_payload)
    except json.JSONDecodeError:
        logger.warning("Failed to parse pre-tool hook payload: %s", raw_payload[:200])
        return 0

    _write_record(args.mode, payload)

    if args.mode == "gemini-beforetool":
        sys.stdout.write("{}\n")
    elif args.mode == "codex-pretooluse":
        sys.stdout.write(json.dumps({"decision": "approve"}) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
