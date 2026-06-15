from __future__ import annotations

import json
import time
from pathlib import Path

from kanban_framework.types import Task, TaskRun, TaskStatus, Phase, AutoMode, ControlMode
from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.infra.config import Config
from kanban_framework.infra.consts import Consts

from kanban_framework.domain.task_io import TaskNotFoundError, read_task_file, write_task_file  # noqa: F401
from kanban_framework.domain.task_run import RunManager


class TaskManager:
    def __init__(self, fs: Filesystem, config: Config):
        self._fs = fs
        self._cfg = config
        self._runs = RunManager(fs)

    def create(self, title: str, description: str, draft: bool = False) -> Task:
        task_id = self._next_task_id()
        status = TaskStatus.DRAFT if draft else TaskStatus.PENDING
        task = Task(id=task_id, title=title, description=description, status=status)
        if not draft:
            task.history.append({
                "phase": "plan",
                "status": "started",
                "started_at": time.time(),
            })
        write_task_file(self._fs, task)
        tf = self._fs.task_dir(task_id) / "task.json"
        if not tf.is_file():
            write_task_file(self._fs, task)
        if draft:
            self._create_inbox_only(task_id)
        else:
            self._create_task_templates(task_id)
        return task

    def _create_task_templates(self, task_id: str) -> None:
        task_dir = self._fs.task_dir(task_id)
        self._fs.ensure_dir(task_dir)
        inbox_path = task_dir / "inbox.md"
        if not self._fs.file_exists(inbox_path):
            inbox_path.write_text(
                f"# Task Inbox — {task_id}\n\n"
                f"## 用户反馈渠道\n\n"
                f"在此记录任务相关的用户反馈、改进建议、待办事项等。\n\n"
                f"可以使用自然语言自由记录，LLM 会自动解析和理解。\n\n"
                f"### 示例\n\n"
                f"- 觉得这个功能还需要优化一下性能\n"
                f"- 测试发现边界情况下有问题，需要修复\n"
                f"- 想增加一个导出功能\n\n"
                f"---\n\n"
                f"**提示**: 使用 \\`kanban inbox add {task_id} \"反馈内容\"\\` 添加新事项\n",
                encoding="utf-8",
            )

    def _create_inbox_only(self, task_id: str) -> None:
        task_dir = self._fs.task_dir(task_id)
        self._fs.ensure_dir(task_dir)
        inbox_path = task_dir / "inbox.md"
        if not self._fs.file_exists(inbox_path):
            inbox_path.write_text(
                f"# Task Inbox — {task_id}\n\n"
                f"## 需求收集\n\n"
                f"在此用自然语言描述需求，模型会自动分析并补全 spec.md。\n\n"
                f"可以填写：功能需求、改进建议、待修复问题、设计想法等。\n\n"
                f"---\n\n"
                f"**提示**: 使用 \\`kanban inbox add {task_id} \"内容\"\\` 或直接编辑此文件\n",
                encoding="utf-8",
            )

    def show(self, task_id: str) -> Task:
        # Directory format first (tasks/TASK-NNN/task.json)
        tf = self._fs.task_dir(task_id) / "task.json"
        if not self._fs.file_exists(tf):
            # Fall back to old flat format (tasks/TASK-NNN.json)
            tf = self._fs.task_file(task_id)
            if not self._fs.file_exists(tf):
                raise TaskNotFoundError(f"Task {task_id} not found")
        return read_task_file(self._fs, tf)

    def status(self) -> dict:
        tasks = []
        for f in sorted(self._fs.kanban_dir.glob("tasks/TASK-*/task.json")):
            data = json.loads(f.read_text(encoding="utf-8"))
            tasks.append(data)
        by_status: dict[str, int] = {}
        for t in tasks:
            s = t.get("status", "unknown")
            by_status[s] = by_status.get(s, 0) + 1
        tasks.sort(key=lambda t: t.get("priority", 5), reverse=True)
        return {"total": len(tasks), "by_status": by_status, "tasks": tasks}

    def update(self, task_id: str, **kwargs) -> Task:
        task = self.show(task_id)
        for key, value in kwargs.items():
            if key == "phase" and isinstance(value, str):
                value = Phase(value)
            if key == "status" and isinstance(value, str):
                value = TaskStatus(value)
            if key == "control_mode" and isinstance(value, str):
                value = ControlMode(value)
            if hasattr(task, key):
                setattr(task, key, value)
        write_task_file(self._fs, task)
        return task

    def record_decision(self, task_id: str, action: str) -> None:
        task = self.show(task_id)
        task.history.append({
            "phase": "user_decision",
            "action": action,
            "timestamp": time.time(),
        })
        write_task_file(self._fs, task)

    def delete(self, task_id: str) -> None:
        import shutil
        task_dir = self._fs.task_dir(task_id)
        if task_dir.is_dir():
            shutil.rmtree(task_dir)
        flat = self._fs.kanban_dir / "tasks" / f"{task_id}.json"
        if flat.is_file():
            flat.unlink()

    # ── TaskRun delegation ──────────────────────────────────────────────

    def create_run(self, task_id: str, phase: str, agent_role: str = "") -> TaskRun:
        task = self.show(task_id)
        task.total_runs += 1
        task.current_run_id = task.total_runs
        run = self._runs.create_run(task_id, phase, agent_role)
        run.run_id = task.total_runs
        write_task_file(self._fs, task)
        self._runs.save_new_run(run)
        return run

    def complete_run(self, task_id: str, run_id: int,
                     summary: str = "", metadata: dict | None = None) -> TaskRun:
        return self._runs.complete_run(task_id, run_id, summary, metadata)

    def fail_run(self, task_id: str, run_id: int, error: str = "") -> TaskRun:
        return self._runs.fail_run(task_id, run_id, error)

    def get_run(self, task_id: str, run_id: int) -> TaskRun | None:
        return self._runs.get_run(task_id, run_id)

    def list_runs(self, task_id: str) -> list[TaskRun]:
        return self._runs.list_runs(task_id)

    def build_worker_context(self, task_id: str) -> dict:
        return self._runs.build_worker_context(task_id)

    # ── File locking + ID generation ────────────────────────────────────

    @staticmethod
    def _file_lock(lock_path: str) -> object | None:
        try:
            import fcntl
            f = open(lock_path, "w", encoding="utf-8")
            fcntl.flock(f, fcntl.LOCK_EX)
            return f
        except Exception:
            pass
        try:
            import msvcrt
            f = open(lock_path, "w", encoding="utf-8")
            msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)
            return f
        except Exception:
            pass
        return None

    @staticmethod
    def _file_unlock(lock_file: object) -> None:
        try:
            import fcntl
            fcntl.flock(lock_file, fcntl.LOCK_UN)
        except Exception:
            pass
        try:
            import msvcrt
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
        except Exception:
            pass
        try:
            lock_file.close()
        except Exception:
            pass

    def _next_task_id(self) -> str:
        counter_file = self._fs.kanban_dir / "next_id.txt"
        base = self._cfg.task_id_base
        default_start = (base * 100 + 1) if base else 1

        lock_file = self._file_lock(str(counter_file) + ".lock")
        try:
            if counter_file.is_file():
                try:
                    next_num = int(counter_file.read_text(encoding="utf-8").strip())
                except (ValueError, OSError):
                    next_num = default_start
            else:
                next_num = default_start
        except Exception:
            if counter_file.is_file():
                try:
                    next_num = int(counter_file.read_text(encoding="utf-8").strip())
                except (ValueError, OSError):
                    next_num = default_start
            else:
                next_num = default_start
        finally:
            self._file_unlock(lock_file)

        for pattern in ("tasks/TASK-*/task.json", "tasks/TASK-*.json",
                        "archive/TASK-*/task.json", "archive/TASK-*.json"):
            for p in self._fs.kanban_dir.glob(pattern):
                parts = p.parts
                for part in parts:
                    if part.startswith("TASK-"):
                        try:
                            n = int(part.replace(".json", "").split("-")[1])
                            if n >= next_num:
                                next_num = n + 1
                        except (IndexError, ValueError):
                            pass
                        break

        task_id = f"{Consts.TASK_ID_PREFIX}{next_num:03d}"
        counter_file.write_text(str(next_num + 1), encoding="utf-8")
        return task_id
