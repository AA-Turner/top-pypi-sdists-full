"""The scripted SDK session the wire and journal nets replay, and how to drive it.

init (with config), 3 logs, a span, a small and a large artifact, update_config, finish.
"""

from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import probe
from probe.sdk.artifact.storage_handlers.multipart.multipart import threshold_bytes

#: Where the scripted run goes: project and experiment are created on the way.
SESSION = {
    "project": "wire-net",
    "experiment": "wire-exp",
    "question": "Does the wire hold?",
    "name": "wire-run",
    "config": {"lr": 0.1, "layers": 2, "optimizer": {"name": "adam", "betas": [0.9, 0.99]}},
}
#: The fake's seeded workspace (`tests.conftest._WS_MINE`): a set-up computer pins one.
WORKSPACE = "11111111-1111-1111-1111-111111111111"
TOKEN = "ros_pat_deadbeef"


def artifact_files(folder: Path) -> tuple[Path, Path]:
    """A small text file and a sparse one just over the multipart threshold."""
    folder.mkdir(parents=True, exist_ok=True)
    small = folder / "notes.txt"
    small.write_text("eval notes\n", encoding="utf-8")
    big = folder / "ckpt.bin"
    with open(big, "wb") as fh:
        fh.write(b"weights!")
        fh.truncate(threshold_bytes() + 4096)
    return small, big


def run_session(folder: Path, *, big: bool = True, after_init: Callable[[], None] | None = None, **init_kw) -> None:
    """The scripted session, through the fluent API a training script uses."""
    small, large = artifact_files(folder)
    probe.init(**SESSION, **init_kw)
    if after_init is not None:
        after_init()
    for step in range(3):
        probe.log({"loss": round(1.0 / (step + 1), 4), "acc": 0.5 + step / 10}, step=step)
    with probe.span("eval", name="holdout"):
        pass
    probe.log_artifact("notes", path=str(small))
    if big:
        probe.log_artifact("ckpt", path=str(large))
    probe.update_config({"warmup": 5})
    probe.finish()


def close_open_runs() -> None:
    """Public-API cleanup: no run stays bound from an earlier test."""
    while probe.active_run() is not None:
        probe.finish()


def cli(args: list[str], env: dict[str, str], cwd: Path) -> subprocess.CompletedProcess:
    """`python -m probe.cli ...` (a kept process entry path) in an isolated child."""
    return subprocess.run(
        [sys.executable, "-m", "probe.cli", *args],
        env=env,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=300,
    )


def child_env(url: str, tmp: Path) -> dict[str, str]:
    """The suite's isolated environment (HOME, XDG_*, outbox) aimed at a served fake."""
    scratch = tmp / "child-tmp"
    scratch.mkdir(exist_ok=True)
    return {
        **os.environ,
        "PROBE_BASE_URL": url,
        "PROBE_TOKEN": TOKEN,
        "PROBE_WORKSPACE": WORKSPACE,
        "PROBE_AUTO_SNAPSHOT": "0",
        "PROBE_CAPTURE_OUTPUTS": "0",
        "TMPDIR": str(scratch),
    }
