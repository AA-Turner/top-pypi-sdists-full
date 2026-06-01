from __future__ import annotations
import json
import time
from pathlib import Path


class TimeTracker:
    def __init__(self, data_file: Path):
        self._file = Path(data_file)
        self._data = self._load()

    def start_phase(self, task_id: str, phase: str) -> None:
        entry = self._data.setdefault(task_id, {})
        entry.setdefault("phases", {}).setdefault(phase, {})
        entry["phases"][phase]["started_at"] = time.time()
        self._save()

    def end_phase(self, task_id: str, phase: str) -> None:
        entry = self._data.setdefault(task_id, {})
        ph = entry.get("phases", {}).get(phase, {})
        if "started_at" in ph:
            ph["elapsed_seconds"] = time.time() - ph.get("started_at", time.time())
        self._save()

    def track_agent(self, task_id: str, phase: str, agent: str, elapsed_seconds: float) -> None:
        entry = self._data.setdefault(task_id, {})
        entry.setdefault("agents", {}).setdefault(agent, {})
        entry["agents"][agent].setdefault("by_phase", {})
        ag = entry["agents"][agent]["by_phase"].setdefault(phase, [])
        ag.append(elapsed_seconds)
        entry["agents"][agent]["total_seconds"] = entry["agents"][agent].get("total_seconds", 0) + elapsed_seconds
        self._save()

    def report(self, task_id: str) -> dict:
        entry = self._data.get(task_id, {})
        phases = entry.get("phases", {})
        total = sum(p.get("elapsed_seconds", 0) for p in phases.values())
        agents = entry.get("agents", {})
        agent_total = sum(a.get("total_seconds", 0) for a in agents.values())
        return {
            "task_id": task_id,
            "total_seconds": total + agent_total,
            "phases": dict(phases),
            "agents": dict(agents),
        }

    def _load(self) -> dict:
        if self._file.exists():
            return json.loads(self._file.read_text(encoding="utf-8"))
        return {}

    def _save(self) -> None:
        self._file.parent.mkdir(parents=True, exist_ok=True)
        self._file.write_text(json.dumps(self._data, indent=2), encoding="utf-8")
