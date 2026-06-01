from __future__ import annotations
import json
import tempfile
from pathlib import Path
from kanban_framework.cli.plan import _cmd_inspect, _cmd_save
from kanban_framework.infra.filesystem import Filesystem


SAMPLE_PLAN = """# Snake Game Implementation Plan

**Goal:** Build a classic Snake game

### Task 1: Game Board
**Files:**
- Create: `games/snake/index.html`

### Task 2: Movement
**Files:**
- Modify: `games/snake/game.js`
"""


def test_inspect_plan_exists():
    with tempfile.TemporaryDirectory() as tmp:
        plan_path = Path(tmp) / ".kanban" / "tasks" / "TASK-001" / "plan.md"
        plan_path.parent.mkdir(parents=True)
        plan_path.write_text(SAMPLE_PLAN, encoding="utf-8")

        import os
        cwd = os.getcwd()
        try:
            os.chdir(tmp)
            result = _cmd_inspect(["TASK-001"])
            assert result["plan_exists"] is True
            assert result["size_bytes"] > 50
        finally:
            os.chdir(cwd)


def test_inspect_plan_missing():
    import os
    with tempfile.TemporaryDirectory() as tmp:
        cwd = os.getcwd()
        try:
            os.chdir(tmp)
            # Create task dir without plan.md
            task_dir = Path(tmp) / ".kanban" / "tasks" / "TASK-001"
            task_dir.mkdir(parents=True, exist_ok=True)
            result = _cmd_inspect(["TASK-001"])
            assert result["plan_exists"] is False
        finally:
            os.chdir(cwd)


def test_save_valid_breakdown():
    breakdown = {
        "task_name": "snake",
        "subtasks": [
            {
                "id": "ST-001",
                "title": "Game Board",
                "estimated_files": ["games/snake/index.html"],
                "description": "Setup",
                "priority": 1,
                "dependencies": [],
            },
        ],
    }
    import os
    with tempfile.TemporaryDirectory() as tmp:
        cwd = os.getcwd()
        try:
            os.chdir(tmp)
            from kanban_framework.infra.filesystem import Filesystem
            task_dir = Filesystem(root=Path(tmp)).task_dir("TASK-001")
            task_dir.mkdir(parents=True, exist_ok=True)
            # Write JSON to a file and use --file
            json_path = Path(tmp) / "llm_output.json"
            json_path.write_text(json.dumps(breakdown, ensure_ascii=False), encoding="utf-8")
            result = _cmd_save(["TASK-001", "--file", str(json_path)])
            assert result["subtask_count"] == 1
            assert (task_dir / "task_breakdown.json").is_file()
        finally:
            os.chdir(cwd)


def test_save_invalid_json():
    import os
    with tempfile.TemporaryDirectory() as tmp:
        cwd = os.getcwd()
        try:
            os.chdir(tmp)
            from kanban_framework.infra.filesystem import Filesystem
            Filesystem(root=Path(tmp)).task_dir("TASK-001").mkdir(parents=True, exist_ok=True)
            json_path = Path(tmp) / "bad.json"
            json_path.write_text("not json", encoding="utf-8")
            result = _cmd_save(["TASK-001", "--file", str(json_path)])
            assert "error" in result
        finally:
            os.chdir(cwd)


def test_save_missing_subtasks():
    import os
    with tempfile.TemporaryDirectory() as tmp:
        cwd = os.getcwd()
        try:
            os.chdir(tmp)
            from kanban_framework.infra.filesystem import Filesystem
            Filesystem(root=Path(tmp)).task_dir("TASK-001").mkdir(parents=True, exist_ok=True)
            json_path = Path(tmp) / "empty.json"
            json_path.write_text(json.dumps({"task_name": "x", "subtasks": []}), encoding="utf-8")
            result = _cmd_save(["TASK-001", "--file", str(json_path)])
            assert "error" in result
        finally:
            os.chdir(cwd)
