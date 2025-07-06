"""Export high-integrity constants and oaths."""

from __future__ import annotations

import argparse
import json
import hashlib
from pathlib import Path
from typing import Dict, Any

import yaml

from tsal.core.oaths import GUARDIAN_OATH, ARC_REACTOR_BOOT_OATH
from tsal.core.ethics_engine import PRIME_DIRECTIVE
from tsal.core.guardian_constants import (
    PHI,
    PERCEPTION_THRESHOLD,
    LEARNING_RATE,
    CONNECTION_DECAY,
    MAX_NODES,
    MAX_AGENTS,
    MAX_DIMENSIONS,
)


def build_sanctum(include_ethics: bool = False) -> Dict[str, Any]:
    data: Dict[str, Any] = {
        "constants": {
            "PHI": PHI,
            "PERCEPTION_THRESHOLD": PERCEPTION_THRESHOLD,
            "LEARNING_RATE": LEARNING_RATE,
            "CONNECTION_DECAY": CONNECTION_DECAY,
            "MAX_NODES": MAX_NODES,
            "MAX_AGENTS": MAX_AGENTS,
            "MAX_DIMENSIONS": MAX_DIMENSIONS,
        }
    }
    if include_ethics:
        data["prime_directive"] = list(PRIME_DIRECTIVE)
        data["oath"] = list(GUARDIAN_OATH)
        data["boot_oath"] = list(ARC_REACTOR_BOOT_OATH)
    encoded = json.dumps(data, sort_keys=True).encode()
    data["sha256"] = hashlib.sha256(encoded).hexdigest()
    return data


def export_sanctum(path: str | None, fmt: str = "json", include_ethics: bool = False) -> str:
    data = build_sanctum(include_ethics=include_ethics)
    if fmt == "yaml":
        text = yaml.safe_dump(data, sort_keys=False)
    else:
        text = json.dumps(data, indent=2)
    if path:
        Path(path).write_text(text)
    return text


def main() -> None:
    parser = argparse.ArgumentParser(description="export project sanctum")
    parser.add_argument("--out")
    parser.add_argument("--format", choices=["json", "yaml"], default="json")
    parser.add_argument("--include-ethics", action="store_true")
    args = parser.parse_args()

    result = export_sanctum(args.out, args.format, args.include_ethics)
    if not args.out:
        print(result)


if __name__ == "__main__":
    main()
