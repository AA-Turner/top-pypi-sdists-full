from __future__ import annotations
import json
import sys
from pathlib import Path
from kanban_framework.infra.filesystem import Filesystem


def dispatch(args: list[str]) -> dict:
    if not args:
        return {"error": "subcommand required", "available": ["inspect", "save"]}

    sub = args[0]
    if sub == "inspect":
        return _cmd_inspect(args[1:])
    if sub == "save":
        return _cmd_save(args[1:])
    return {"error": f"unknown subcommand: {sub}", "available": ["inspect", "save"]}


def _cmd_inspect(args: list[str]) -> dict:
    if not args:
        return {"error": "task_id required"}
    task_id = args[0]
    fs = Filesystem(root=Filesystem.find_project_root())
    plan_path = fs.task_dir(task_id) / "plan.md"

    if not plan_path.is_file():
        return {"task_id": task_id, "plan_exists": False}

    text = plan_path.read_text(encoding="utf-8")
    return {
        "task_id": task_id,
        "plan_exists": True,
        "plan_path": str(plan_path),
        "size_bytes": len(text.encode("utf-8")),
    }


def _cmd_save(args: list[str]) -> dict:
    if not args:
        return {"error": "task_id required"}

    task_id = args[0]
    file_input = None
    if len(args) > 2 and args[1] == "--file":
        file_input = args[2]

    fs = Filesystem(root=Filesystem.find_project_root())
    task_dir = fs.task_dir(task_id)

    try:
        if file_input:
            data = json.loads(Path(file_input).read_text(encoding="utf-8"))
        else:
            data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        return {"error": f"invalid JSON: {e}"}

    if not isinstance(data, dict) or "subtasks" not in data:
        return {"error": "JSON must be an object with 'subtasks' array"}
    if not data["subtasks"]:
        return {"error": "'subtasks' must not be empty"}
    for i, st in enumerate(data["subtasks"]):
        for field in ("id", "title", "estimated_files"):
            if field not in st:
                return {"error": f"subtask[{i}] missing '{field}'"}

    task_dir.mkdir(parents=True, exist_ok=True)
    output_path = task_dir / "task_breakdown.json"
    output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    return {
        "task_id": task_id,
        "subtask_count": len(data["subtasks"]),
        "output": str(output_path),
    }
