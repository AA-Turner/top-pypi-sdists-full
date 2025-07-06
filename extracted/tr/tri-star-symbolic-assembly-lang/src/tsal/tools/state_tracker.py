"""Track WAS_THEN / IS_NOW / WILL_BE states in a YAML log."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Any

import yaml

LOG_PATH = Path("state_log.yaml")


def load_log() -> Dict[str, Any]:
    if LOG_PATH.exists():
        with open(LOG_PATH) as f:
            data = yaml.safe_load(f) or {}
    else:
        data = {}
    return data


def save_log(data: Dict[str, Any]) -> None:
    with open(LOG_PATH, "w") as f:
        yaml.safe_dump(data, f)


def update_entry(module: str, was: str | None, now: str | None, will: str | None) -> None:
    data = load_log()
    entry = data.get(module, {})
    if was:
        entry["WAS_THEN"] = was
    if now:
        entry["IS_NOW"] = now
    if will:
        entry["WILL_BE"] = will
    data[module] = entry
    save_log(data)


def show_entry(module: str) -> None:
    data = load_log()
    entry = data.get(module)
    if entry:
        print(yaml.safe_dump({module: entry}, sort_keys=False))
    else:
        print(f"No entry for {module}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Update or view state log")
    parser.add_argument("module")
    parser.add_argument("--was")
    parser.add_argument("--now")
    parser.add_argument("--will")
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args()

    if args.show:
        show_entry(args.module)
    else:
        update_entry(args.module, args.was, args.now, args.will)


if __name__ == "__main__":
    main()
