"""Run predefined agent tasks from tasks.yaml."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from typing import Dict

import yaml

TASKS_FILE = Path("tasks.yaml")
LOG_FILE = Path("task_agent.log")

DEFAULT_TASKS: Dict[str, str] = {
    "repair": "tsal-bestest-beast 3 src/tsal --safe",
    "improve": "brian optimize src/tsal",
    "overhaul": "tsal-bestest-beast 9 src/tsal",
    "rebuild": "python makeBrian.py all",
    "clone": "python makeBrian.py init",
    "learn": "python -m tsal.utils.language_db --reset",
    "help": "python makeBrian.py help",
}


def load_tasks() -> Dict[str, str]:
    if TASKS_FILE.exists():
        data = yaml.safe_load(TASKS_FILE.read_text()) or {}
        tasks = data.get("tasks", {})
        merged = DEFAULT_TASKS | tasks
        return merged
    return DEFAULT_TASKS


def run_task(name: str) -> None:
    tasks = load_tasks()
    cmd = tasks.get(name)
    if not cmd:
        raise SystemExit(f"Unknown task: {name}")
    with LOG_FILE.open("a") as log:
        log.write(f"$ {cmd}\n")
        subprocess.run(cmd, shell=True, check=False, stdout=log, stderr=log)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run agent task from YAML")
    parser.add_argument("task", help="Task name")
    args = parser.parse_args()
    run_task(args.task)


if __name__ == "__main__":
    main()
