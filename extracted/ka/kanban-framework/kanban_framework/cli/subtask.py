"""
Subtask lifecycle management — atomic claim/unclaim for multi-window workflows.

Each subtask transitions through: pending → claimed → in_progress → completed
- claim: atomic CAS on task_breakdown.json, prevents two windows claiming same ST
- unclaim: release back to pending (only if not yet completed)
- done: mark completed with optional commit_hash and file list
- status: show all subtasks with claim info
"""

from __future__ import annotations
import json
import os
import tempfile
import time
from pathlib import Path
from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.infra.config import Config
from kanban_framework.domain.task import TaskManager
from kanban_framework.domain.progress import ProgressTracker


def _resolve(task_id: str) -> tuple[Filesystem, TaskManager, dict, Path]:
    root = Filesystem.find_project_root()
    fs = Filesystem(root=root)
    tm = TaskManager(fs, Config(fs))
    task = tm.show(task_id)
    breakdown_path = fs.task_dir(task.id) / "task_breakdown.json"
    if not fs.file_exists(breakdown_path):
        raise FileNotFoundError(f"task_breakdown.json not found for {task_id}")
    breakdown = json.loads(breakdown_path.read_text(encoding="utf-8"))
    return fs, tm, breakdown, breakdown_path


def _atomic_write(path: Path, data: dict) -> bool:
    """Write atomically via temp file + rename."""
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".breakdown_", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, str(path))
        return True
    except Exception:
        os.unlink(tmp)
        return False


# ── batch planning ─────────────────────────────────────────────────

def plan_batches(task_id: str) -> dict:
    """Compute parallel execution batches from task_breakdown.json."""
    _, _, breakdown, _ = _resolve(task_id)
    subtasks = breakdown.get("subtasks", [])

    if not subtasks:
        return {"task_id": task_id, "batches": [], "total_subtasks": 0}

    deps: dict[str, set[str]] = {}
    for st in subtasks:
        deps[st["id"]] = set(st.get("dependencies", []))

    remaining = set(deps.keys())
    batches: list[list[str]] = []
    completed: set[str] = set()

    while remaining:
        ready = sorted(sid for sid in remaining if deps[sid].issubset(completed))
        if not ready:
            return {
                "task_id": task_id, "error": "circular dependency detected",
                "remaining": sorted(remaining), "batches": [[s] for s in remaining],
            }
        st_map = {s["id"]: s for s in subtasks}
        current_batch: list[str] = []
        for sid in ready:
            st = st_map[sid]
            if not st.get("parallelizable"):
                if current_batch:
                    batches.append(current_batch)
                    current_batch = []
                batches.append([sid])
                remaining.discard(sid)
                completed.add(sid)
                continue
            my_files = set(st.get("file_ownership", []))
            batch_files = set()
            for b_sid in current_batch:
                batch_files.update(st_map[b_sid].get("file_ownership", []))
            if my_files & batch_files:
                if current_batch:
                    batches.append(current_batch)
                    current_batch = []
                current_batch.append(sid)
                remaining.discard(sid)
                completed.add(sid)
            else:
                current_batch.append(sid)
                remaining.discard(sid)
                completed.add(sid)
        if current_batch:
            batches.append(current_batch)

    return {
        "task_id": task_id, "batches": batches, "total_subtasks": len(subtasks),
        "total_batches": len(batches),
        "parallel_subtasks": sum(len(b) for b in batches if len(b) > 1),
        "serial_subtasks": sum(1 for b in batches if len(b) == 1),
    }


def batch_details(task_id: str) -> dict:
    _, _, breakdown, _ = _resolve(task_id)
    subtasks = breakdown.get("subtasks", [])
    st_map = {s["id"]: s for s in subtasks}
    plan = plan_batches(task_id)
    if "error" in plan:
        return plan
    detailed = []
    for i, batch in enumerate(plan["batches"]):
        detailed.append({"batch_index": i, "size": len(batch), "subtasks": [
            {"id": sid, "title": st_map.get(sid, {}).get("title", ""),
             "file_ownership": st_map.get(sid, {}).get("file_ownership", []),
             "dependencies": st_map.get(sid, {}).get("dependencies", []),
             "status": st_map.get(sid, {}).get("status", "pending")}
            for sid in batch
        ]})
    return {"task_id": task_id, "batches": detailed, "total_batches": len(detailed),
            "total_subtasks": plan["total_subtasks"]}


# ── atomic claim / unclaim / done ───────────────────────────────────

def claim(task_id: str, subtask_id: str, claimant: str = "") -> dict:
    """Atomically claim a subtask.  Returns error if already claimed."""
    _, _, breakdown, path = _resolve(task_id)
    subtasks = breakdown.get("subtasks", [])

    for st in subtasks:
        if st["id"] == subtask_id:
            current_status = st.get("status", "pending")
            if current_status in ("claimed", "in_progress", "completed"):
                return {
                    "task_id": task_id, "subtask_id": subtask_id,
                    "claimed": False,
                    "reason": f"subtask already {current_status}",
                    "current_claimant": st.get("claimed_by", ""),
                    "claimed_at": st.get("claimed_at", ""),
                }
            # CAS: set claimed
            st["status"] = "claimed"
            st["claimed_by"] = claimant or os.environ.get("USER", os.environ.get("USERNAME", "unknown"))
            st["claimed_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            breakdown["subtasks"] = subtasks
            if not _atomic_write(path, breakdown):
                return {"task_id": task_id, "subtask_id": subtask_id,
                        "claimed": False, "reason": "write failed — retry"}
            return {
                "task_id": task_id, "subtask_id": subtask_id,
                "claimed": True, "status": "claimed",
                "claimant": st["claimed_by"], "claimed_at": st["claimed_at"],
                "title": st.get("title", ""),
                "plan_file": st.get("plan_file", ""),
                "dependencies": st.get("dependencies", []),
            }

    return {"task_id": task_id, "subtask_id": subtask_id,
            "claimed": False, "reason": "subtask not found in task_breakdown.json"}


def unclaim(task_id: str, subtask_id: str) -> dict:
    """Release a claimed subtask back to pending."""
    _, _, breakdown, path = _resolve(task_id)
    subtasks = breakdown.get("subtasks", [])

    for st in subtasks:
        if st["id"] == subtask_id:
            current_status = st.get("status", "pending")
            if current_status == "completed":
                return {"task_id": task_id, "subtask_id": subtask_id,
                        "unclaimed": False, "reason": "cannot unclaim completed subtask"}
            st["status"] = "pending"
            st.pop("claimed_by", None)
            st.pop("claimed_at", None)
            breakdown["subtasks"] = subtasks
            _atomic_write(path, breakdown)
            return {"task_id": task_id, "subtask_id": subtask_id,
                    "unclaimed": True, "status": "pending"}

    return {"task_id": task_id, "subtask_id": subtask_id,
            "unclaimed": False, "reason": "subtask not found"}


def done(task_id: str, subtask_id: str, commit_hash: str | None = None,
         files: list[str] | None = None) -> dict:
    """Mark a subtask as completed."""
    root = Filesystem.find_project_root()
    fs = Filesystem(root=root)
    tracker = ProgressTracker(fs)
    tracker.subtask_done(task_id, subtask_id, commit_hash=commit_hash, files=files)

    # Also update task_breakdown.json
    _, _, breakdown, path = _resolve(task_id)
    subtasks = breakdown.get("subtasks", [])
    for st in subtasks:
        if st["id"] == subtask_id:
            st["status"] = "completed"
            st["completed_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            if commit_hash:
                st["commit_hash"] = commit_hash
            if files:
                st["files"] = files
            break
    _atomic_write(path, breakdown)

    result: dict = {"task_id": task_id, "subtask_id": subtask_id, "status": "completed"}
    if commit_hash:
        result["commit_hash"] = commit_hash
    if files:
        result["files"] = files
    return result


def status(task_id: str) -> dict:
    """Show all subtask statuses with claim info."""
    _, _, breakdown, _ = _resolve(task_id)
    subtasks = breakdown.get("subtasks", [])
    st_list = []
    for st in subtasks:
        st_list.append({
            "id": st.get("id", ""),
            "title": st.get("title", ""),
            "status": st.get("status", "pending"),
            "claimant": st.get("claimed_by", ""),
            "claimed_at": st.get("claimed_at", ""),
            "completed_at": st.get("completed_at", ""),
            "priority": st.get("priority", "medium"),
            "blocking": st.get("blocking", False),
            "owner": st.get("owner", ""),
            "suggested_owner": st.get("suggested_owner", ""),
        })
    pending = sum(1 for s in st_list if s["status"] in ("pending",))
    claimed = sum(1 for s in st_list if s["status"] in ("claimed", "in_progress"))
    completed_count = sum(1 for s in st_list if s["status"] == "completed")
    return {
        "task_id": task_id,
        "subtasks": st_list,
        "summary": {"total": len(st_list), "pending": pending,
                     "claimed": claimed, "completed": completed_count},
    }


# ── CLI dispatch ────────────────────────────────────────────────────

def dispatch(args: list[str]) -> dict:
    if not args:
        return {"error": "subcommand required (claim, unclaim, done, start, status, plan, details, assign, assign-batch)"}

    sub = args[0]

    if sub == "plan":
        if len(args) < 2:
            return {"error": "task_id required"}
        return plan_batches(args[1])

    if sub == "details":
        if len(args) < 2:
            return {"error": "task_id required"}
        return batch_details(args[1])

    if sub == "claim":
        if len(args) < 3:
            return {"error": "task_id and subtask_id required"}
        return claim(args[1], args[2])

    if sub == "unclaim":
        if len(args) < 3:
            return {"error": "task_id and subtask_id required"}
        return unclaim(args[1], args[2])

    if sub == "status":
        if len(args) < 2:
            return {"error": "task_id required"}
        return status(args[1])

    if sub == "start":
        if len(args) < 3:
            return {"error": "task_id and subtask_id required"}
        # claim + mark in_progress
        result = claim(args[1], args[2])
        if not result.get("claimed"):
            return result
        # Set to in_progress
        _, _, breakdown, path = _resolve(args[1])
        for st in breakdown.get("subtasks", []):
            if st["id"] == args[2]:
                st["status"] = "in_progress"
                break
        _atomic_write(path, breakdown)
        result["status"] = "in_progress"
        return result

    if sub == "done":
        if len(args) < 3:
            return {"error": "task_id and subtask_id required"}
        task_id = args[1]
        subtask_id = args[2]
        commit_hash: str | None = None
        files: list[str] | None = None
        remaining = args[3:]
        i = 0
        while i < len(remaining):
            if remaining[i] == "--commit-hash" and i + 1 < len(remaining):
                commit_hash = remaining[i + 1]; i += 2
            elif remaining[i] == "--files" and i + 1 < len(remaining):
                files = [f.strip() for f in remaining[i + 1].split(",") if f.strip()]; i += 2
            else:
                i += 1
        return done(task_id, subtask_id, commit_hash=commit_hash, files=files)

    if sub == "assign":
        if len(args) < 4:
            return {"error": "task_id, subtask_id, and --owner required"}
        task_id = args[1]
        subtask_id = args[2]
        owner = None
        for i, arg in enumerate(args):
            if arg == "--owner" and i + 1 < len(args):
                owner = args[i + 1]
                break
        if owner not in ("ai", "human"):
            return {"error": "--owner must be ai or human"}
        _, _, breakdown, path = _resolve(task_id)
        found = False
        for st in breakdown.get("subtasks", []):
            if st["id"] == subtask_id:
                st["owner"] = owner
                found = True
                break
        if not found:
            return {"error": f"subtask {subtask_id} not found"}
        _atomic_write(path, breakdown)
        return {"task_id": task_id, "subtask_id": subtask_id, "owner": owner}

    if sub == "assign-batch":
        if len(args) < 4:
            return {"error": "task_id, --owner, and --subtask required"}
        task_id = args[1]
        owner = None
        subtask_ids = []
        for i, arg in enumerate(args):
            if arg == "--owner" and i + 1 < len(args):
                owner = args[i + 1]
            if arg == "--subtask" and i + 1 < len(args):
                subtask_ids = [s.strip() for s in args[i + 1].split(",") if s.strip()]
        if owner not in ("ai", "human"):
            return {"error": "--owner must be ai or human"}
        if not subtask_ids:
            return {"error": "--subtask required (comma-separated list)"}
        _, _, breakdown, path = _resolve(task_id)
        assigned = []
        for st in breakdown.get("subtasks", []):
            if st["id"] in subtask_ids:
                st["owner"] = owner
                assigned.append(st["id"])
        _atomic_write(path, breakdown)
        return {"task_id": task_id, "assigned": assigned, "owner": owner}

    return {"error": f"unknown subtask subcommand: {sub}"}
