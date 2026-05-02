"""Internal child-process runner for ``tool.sub_agents`` tasks."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import traceback
from typing import Any

from .runtime import CliRuntime


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run one Aegis sub-agent task.")
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--profile-dir", type=Path, required=True)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--prompt-file", type=Path, required=True)
    parser.add_argument("--result-file", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    previous_sub_agent_flag = os.environ.get("AEGIS_SUB_AGENT_CHILD")
    os.environ["AEGIS_SUB_AGENT_CHILD"] = "1"
    try:
        prompt = args.prompt_file.read_text(encoding="utf-8")
        runtime = CliRuntime.create(state_dir=args.state_dir, profile_dir=args.profile_dir)
        runtime.prepare_session_surface(args.session_id)
        outcome = runtime.explain_next_step(session_id=args.session_id, prompt=prompt)
        execution = outcome.execution
        _write_result(
            args.result_file,
            {
                "status": "completed",
                "summary": execution.summary,
                "execution_id": execution.execution_id,
                "session_id": execution.session_id,
                "outcome": execution.outcome,
            },
        )
        return 0
    except Exception as error:
        _write_result(
            args.result_file,
            {
                "status": "failed",
                "summary": f"{type(error).__name__}: {error}",
                "error": type(error).__name__,
                "traceback": traceback.format_exc(limit=8),
            },
        )
        return 1
    finally:
        if previous_sub_agent_flag is None:
            os.environ.pop("AEGIS_SUB_AGENT_CHILD", None)
        else:
            os.environ["AEGIS_SUB_AGENT_CHILD"] = previous_sub_agent_flag


def _write_result(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
