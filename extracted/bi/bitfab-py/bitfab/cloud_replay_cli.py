from __future__ import annotations

import json
import os
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

HINT = "Add --cloud to run the same replay on GitHub Actions; bitfab-replay --cloud --help explains it."

HELPER = Path(__file__).with_name("cloudReplay.py")


def is_cloud_command(argv: Sequence[str]) -> bool:
    return any(arg == "--cloud" or arg.startswith("--cloud-") for arg in argv)


def run_cloud_command(argv: Sequence[str], *, helper: Path = HELPER) -> int:
    env = {
        **os.environ,
        "BITFAB_REPLAY_COMMAND": json.dumps(
            [sys.executable, "-m", "bitfab.replay_cli"]
        ),
        "BITFAB_SDK_LANGUAGE": "python",
    }
    with subprocess.Popen([sys.executable, "-I", str(helper), *argv], env=env) as child:
        while True:
            try:
                return child.wait()
            except KeyboardInterrupt:
                continue
