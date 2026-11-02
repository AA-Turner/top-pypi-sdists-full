"""Trajectory persistence helpers."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any


def write_trajectory(
    logs_dir: Path,
    steps: list[dict[str, Any]],
    total_input: int,
    total_output: int,
    model_name: str,
    agent_name: str = "cua",
) -> None:
    trajectory = {
        "schema_version": "ATIF-v1.6",
        "session_id": str(uuid.uuid4()),
        "agent": {
            "name": agent_name,
            "version": "1.0.0",
            "model_name": model_name,
        },
        "steps": steps,
        "final_metrics": {
            "total_prompt_tokens": total_input,
            "total_completion_tokens": total_output,
            "total_steps": len(steps),
        },
    }
    (logs_dir / "trajectory.json").write_text(json.dumps(trajectory, indent=2))
