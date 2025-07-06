from __future__ import annotations
import time
from typing import Dict


class StatusManager:
    """In-memory status tracker."""

    def __init__(self) -> None:
        self._status: Dict[str, str] = {}

    def start(self, name: str) -> None:
        self._status[name] = "in-progress"

    def complete(self, name: str) -> None:
        self._status[name] = "done"

    def fail(self, name: str) -> None:
        self._status[name] = "failed"

    def state(self, name: str) -> str:
        return self._status.get(name, "pending")

    def wait(self, name: str, check_func, interval: int = 5) -> None:
        """Poll until check_func returns True."""
        while not check_func():
            print(f"Waiting for {name}...")
            time.sleep(interval)
        self.complete(name)

    def summary(self) -> None:
        for k, v in self._status.items():
            print(f"{k}: {v}")
