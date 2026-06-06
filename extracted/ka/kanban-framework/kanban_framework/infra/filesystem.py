from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Any


class Filesystem:
    def __init__(self, root: Path):
        self._root = Path(root)
        # If root already points to .kanban, don't double-nest
        if self._root.name == ".kanban":
            self._kanban_dir = self._root
        else:
            self._kanban_dir = self._root / ".kanban"

    @property
    def root(self) -> Path:
        return self._root

    @staticmethod
    def find_skill_dir() -> Path:
        """Find the kanban skill directory (SKILL.md, agents, rules, etc).

        Works both pip-installed and from source.
        Resolution order:
        1. kanban_framework/_skill/ (pip-installed bundle)
        2. importlib.resources fallback (most reliable across platforms)
        3. parent of kanban_framework/ (source checkout)
        4. Best available: bundled dir with most content, or parent
        """
        import logging
        _log = logging.getLogger("kanban")

        pkg_dir = Path(__file__).resolve().parent.parent  # kanban_framework/
        candidates: list[tuple[Path, str]] = []

        # 1. Pip-installed: skill files bundled in kanban_framework/_skill/
        bundled = pkg_dir / "_skill"
        _log.info("find_skill_dir: checking bundled=%s (SKILL.md=%s)",
                  bundled, (bundled / "SKILL.md").is_file())
        if (bundled / "SKILL.md").is_file():
            return bundled
        candidates.append((bundled, "bundled"))

        # 2. importlib.resources fallback (most reliable on Windows)
        try:
            from importlib import resources
            res_path = Path(str(resources.files("kanban_framework") / "_skill"))
            _log.info("find_skill_dir: checking importlib=%s (SKILL.md=%s)",
                      res_path, (res_path / "SKILL.md").is_file())
            if (res_path / "SKILL.md").is_file():
                return res_path
            candidates.append((res_path, "importlib"))
        except Exception as exc:
            _log.warning("find_skill_dir: importlib.resources failed: %s", exc)

        # 3. Source install: walk up from kanban_framework/ to kanban skill dir
        skill_dir = pkg_dir.parent  # .claude/skills/kanban/
        _log.info("find_skill_dir: checking parent=%s (SKILL.md=%s)",
                  skill_dir, (skill_dir / "SKILL.md").is_file())
        if (skill_dir / "SKILL.md").is_file():
            return skill_dir
        candidates.append((skill_dir, "parent"))

        # 4. Best available: pick the candidate with most subdirectories
        best = bundled
        best_score = -1
        for path, label in candidates:
            if not path.is_dir():
                _log.info("find_skill_dir: candidate '%s' = %s (not a dir)", label, path)
                continue
            score = sum(1 for c in path.iterdir() if c.is_dir() or c.is_file())
            _log.warning("find_skill_dir: candidate '%s' = %s (score=%d, has_SKILL.md=%s)",
                         label, path, score, (path / "SKILL.md").is_file())
            if score > best_score:
                best_score = score
                best = path

        _log.warning("find_skill_dir: no candidate has SKILL.md, returning best=%s", best)
        return best

    @staticmethod
    def find_project_root() -> Path:
        """Find the project root by walking up from cwd looking for .kanban/config.json.

        Priority:
        1. KANBAN_ROOT env var (if valid — contains .kanban/config.json)
        2. Walk up from cwd until .kanban/config.json found
        3. Fall back to cwd
        """
        env_root = os.environ.get("KANBAN_ROOT")
        if env_root:
            env_path = Path(env_root)
            if (env_path / ".kanban" / "config.json").is_file():
                return env_path

        cwd = Path.cwd()
        for parent in [cwd] + list(cwd.parents):
            if (parent / ".kanban" / "config.json").is_file():
                return parent
        return cwd

    @property
    def kanban_dir(self) -> Path:
        return self._kanban_dir

    @property
    def tasks_dir(self) -> Path:
        return self._kanban_dir / "tasks"

    @staticmethod
    def _validate_task_id(task_id: str) -> None:
        """Reject task IDs that could cause path traversal. (#291)"""
        if not task_id or ".." in task_id or "/" in task_id or "\\" in task_id:
            raise ValueError(f"Invalid task_id: {task_id!r}")
        if not task_id.startswith("TASK-"):
            raise ValueError(f"task_id must start with TASK-: {task_id!r}")

    def task_dir(self, task_id: str) -> Path:
        self._validate_task_id(task_id)
        return self._kanban_dir / "tasks" / task_id

    def task_file(self, task_id: str) -> Path:
        self._validate_task_id(task_id)
        # New format: .kanban/tasks/TASK-077/task.json
        new_path = self._kanban_dir / "tasks" / task_id / "task.json"
        if new_path.is_file():
            return new_path
        # Old format (or new task not yet created): .kanban/tasks/TASK-077.json
        return self._kanban_dir / "tasks" / f"{task_id}.json"

    def report_dir(self, task_id: str, iteration: int) -> Path:
        return self.iteration_dir(task_id, iteration)

    def iteration_dir(self, task_id: str, iteration: int) -> Path:
        return self._kanban_dir / "tasks" / task_id / f"iteration-{iteration}"

    def archive_dir(self) -> Path:
        return self._kanban_dir / "archive"

    def archive_task_file(self, task_id: str) -> Path:
        # New format: archive/TASK-077/task.json
        new_path = self._kanban_dir / "archive" / task_id / "task.json"
        if new_path.is_file():
            return new_path
        # Old format: archive/TASK-077.json
        return self._kanban_dir / "archive" / f"{task_id}.json"

    def inbox_file(self) -> Path:
        return self._kanban_dir / "inbox" / "inbox.json"

    def dispatch_dir(self, task_id: str) -> Path:
        return self._kanban_dir / "tasks" / task_id / "dispatch"

    def config_file(self) -> Path:
        return self._kanban_dir / "config.json"

    def workflow_file(self) -> Path:
        return self._kanban_dir / "workflow.json"

    def read_json(self, path: Path) -> dict[str, Any]:
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON in {path} at line {e.lineno}: {e.msg}"
            ) from e

    def write_json(self, path: Path, data: dict[str, Any]) -> None:
        self.ensure_dir(path.parent)
        tmp = path.with_suffix(path.suffix + ".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        tmp.replace(path)  # atomic rename (#263)

    def file_exists(self, path: Path) -> bool:
        return path.is_file()

    @staticmethod
    def run_no_window(cmd: list[str], **kwargs):
        """Run a subprocess command without flashing a console window. (#218)"""
        import subprocess, sys
        if sys.platform == "win32":
            flags = 0
            for attr in ("CREATE_NO_WINDOW", "CREATE_NEW_PROCESS_GROUP"):
                if hasattr(subprocess, attr):
                    flags |= getattr(subprocess, attr)
            if flags and "creationflags" not in kwargs:
                kwargs["creationflags"] = flags
        kw = {"capture_output": True, "text": True, "encoding": "utf-8", "errors": "replace"}
        kw.update(kwargs)
        return subprocess.run(cmd, **kw)

    @staticmethod
    def ensure_dir(path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def resolve_python(config_path: Path | None = None) -> tuple[str, str]:
        """Resolve a working Python interpreter and the PYTHONPATH for kanban_framework module.

        Returns:
            (python_bin, pythonpath) where pythonpath is the dir containing kanban_framework/
        """
        import subprocess
        import sys

        # Determine PYTHONPATH: directory containing the kanban_framework/ package
        # __file__ = .../kanban_framework/infra/filesystem.py → parent.parent = .../kanban_framework → parent = .../kanban/
        pkg_parent = Path(__file__).parent.parent.parent  # .claude/skills/kanban/
        pythonpath = str(pkg_parent)

        # 1. Check config.json python_bin
        if config_path and config_path.is_file():
            try:
                cfg = json.loads(config_path.read_text(encoding="utf-8"))
                bin_path = cfg.get("python_bin")
                if bin_path:
                    # Resolve relative to project root
                    if not Path(bin_path).is_absolute():
                        bin_path = str(config_path.parent.parent / bin_path)
                    result = subprocess.run(
                        [bin_path, "--version"],
                        capture_output=True, timeout=5,
                    )
                    if result.returncode == 0:
                        return bin_path, pythonpath
            except Exception:
                pass

        # 2. Use current interpreter (most reliable)
        if sys.executable and Path(sys.executable).exists():
            return sys.executable, pythonpath

        # 3. Try platform-appropriate candidates
        candidates = ["python", "python3"]
        for candidate in candidates:
            try:
                result = subprocess.run(
                    [candidate, "--version"],
                    capture_output=True, timeout=5,
                )
                # exit code 49 = Windows Store python3 stub; skip it
                if result.returncode == 0:
                    return candidate, pythonpath
                if result.returncode == 49:
                    continue
            except Exception:
                continue

        # Last resort
        return "python3", pythonpath
