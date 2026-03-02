"""JSON persistence for automation jobs and configuration."""

from __future__ import annotations

import json
import threading
from pathlib import Path

from .models import AutomationConfig, AutomationJob


class AutomationStorage:
    """Thread-safe JSON file storage for automation state.

    Files:
      - ``<emdash_dir>/automation/jobs.json``  — list of AutomationJob
      - ``<emdash_dir>/automation.json``        — AutomationConfig
    """

    def __init__(self, emdash_dir: Path) -> None:
        self._emdash_dir = emdash_dir
        self._jobs_file = emdash_dir / "automation" / "jobs.json"
        self._config_file = emdash_dir / "automation.json"
        self._lock = threading.Lock()

    # -- Jobs ----------------------------------------------------------------

    def load_jobs(self) -> list[AutomationJob]:
        with self._lock:
            if not self._jobs_file.exists():
                return []
            try:
                data = json.loads(self._jobs_file.read_text())
            except (json.JSONDecodeError, OSError):
                return []
            return [AutomationJob.from_dict(d) for d in data]

    def save_jobs(self, jobs: list[AutomationJob]) -> None:
        with self._lock:
            # Skip creating the automation folder when there's nothing to save.
            # This avoids polluting .emdash/ for agents that don't use automation.
            if not jobs and not self._jobs_file.exists():
                return
            self._jobs_file.parent.mkdir(parents=True, exist_ok=True)
            self._jobs_file.write_text(json.dumps(
                [j.to_dict() for j in jobs], indent=2,
            ))

    # -- Config --------------------------------------------------------------

    def load_config(self) -> AutomationConfig:
        with self._lock:
            if not self._config_file.exists():
                return AutomationConfig()
            try:
                data = json.loads(self._config_file.read_text())
            except (json.JSONDecodeError, OSError):
                return AutomationConfig()
            return AutomationConfig.from_dict(data)

    def save_config(self, config: AutomationConfig) -> None:
        with self._lock:
            self._config_file.parent.mkdir(parents=True, exist_ok=True)
            self._config_file.write_text(json.dumps(config.to_dict(), indent=2))
