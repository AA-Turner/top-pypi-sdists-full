from __future__ import annotations
import sys
import re
from pathlib import Path

from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.infra.consts import Consts

_SCOPE_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,15}$")


class Config:
    def __init__(self, fs: Filesystem):
        self._fs = fs
        self._config = self._load_json(fs.config_file(), {"output_dir": "src"})
        self._workflow = self._load_json(fs.workflow_file(), {})

    @property
    def python_bin(self) -> str:
        default = "venv/Scripts/python.exe" if sys.platform == "win32" else "venv/bin/python"
        return self._config.get("python_bin", default)

    @property
    def python_cmd(self) -> str:
        """The python command name itself (python3 vs python)."""
        if sys.platform == "win32":
            return "python"
        import shutil
        return "python3" if shutil.which("python3") else "python"

    @property
    def output_dir(self) -> str:
        return self._config.get("output_dir", Consts.OUTPUT_DIR_DEFAULT)

    @property
    def pass_threshold(self) -> float:
        val = self._config.get("pass_threshold")
        if val is not None:
            return float(val)
        return self._workflow.get("pass_threshold", Consts.PASS_THRESHOLD)

    @property
    def max_iterations(self) -> int:
        val = self._config.get("max_iterations")
        if val is not None:
            return int(val)
        return self._workflow.get("max_iterations", Consts.MAX_ITERATIONS)

    @property
    def phases(self) -> list[str]:
        raw = self._workflow.get(
            "phases",
            ["plan", "execute", "evaluate", "user_decision", "archive"],
        )
        if raw and isinstance(raw[0], dict):
            return [p["id"] for p in raw]
        return raw

    @property
    def phases_detail(self) -> list[dict]:
        return self._workflow.get("phases", [])

    @property
    def task_id_base(self) -> int:
        return self._config.get("task_id_base", 0)

    @property
    def default_mode(self) -> str:
        """Default workflow mode when task has no mode set."""
        return self._config.get("default_mode", Consts.DEFAULT_MODE)

    @property
    def worktree_base_dir(self) -> Path | None:
        raw = self._config.get("worktree_base_dir")
        if raw:
            return Path(raw)
        return None

    @property
    def worktree_enabled(self) -> bool:
        return self._config.get("worktree", {}).get("enabled", False)

    @property
    def raw(self) -> dict:
        return dict(self._config)

    @property
    def workflow(self) -> dict:
        return dict(self._workflow)

    @property
    def knowledge_backend(self) -> str:
        """Knowledge base backend name. Default: 'builtin'.
        Set via config.json: {"knowledge": {"backend": "lightrag"}}
        """
        kb_cfg = self._config.get("knowledge", {})
        if isinstance(kb_cfg, dict):
            return kb_cfg.get("backend", "builtin")
        return "builtin"

    @property
    def knowledge_scope(self) -> str:
        """Personal knowledge base ID prefix. Default: '' (uses K001 format).
        Set via config.json: {"knowledge": {"scope": "alice"}}
        Must match: ^[a-z][a-z0-9-]{1,15}$ (lowercase, 2-16 chars)
        """
        kb_cfg = self._config.get("knowledge", {})
        if isinstance(kb_cfg, dict):
            scope = kb_cfg.get("scope", "")
            if isinstance(scope, str) and scope and _SCOPE_RE.match(scope):
                return scope
        return ""

    @property
    def code_index_backend(self) -> str:
        """Code index backend name. Default: '' (disabled).
        Set via config.json: {"code_index": {"backend": "code-review-graph"}}
        """
        ci_cfg = self._config.get("code_index", {})
        if isinstance(ci_cfg, dict):
            return ci_cfg.get("backend", "")
        return ""

    @property
    def prompt_hooks(self) -> dict[str, str]:
        """Custom prompt injections per phase or step.

        config.json example:
        {
          "prompt_hooks": {
            "qa_spec": "本项目使用 Playwright E2E 测试...",
            "execute.spawn": "所有代码必须通过 ruff check"
          }
        }
        Keys can be phase names (e.g. "plan", "execute") or specific
        step IDs (e.g. "execute.spawn", "plan.plan_A").
        """
        raw = self._config.get("prompt_hooks", {})
        if isinstance(raw, dict):
            return {str(k): str(v) for k, v in raw.items()}
        return {}

    def _load_json(self, path: Path, default: dict) -> dict:
        if self._fs.file_exists(path):
            try:
                data = self._fs.read_json(path)
                return data if isinstance(data, dict) else default
            except (ValueError, OSError):
                return default
        return default
