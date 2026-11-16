"""The CommandActor wrap: an SGLang engine or Miles session server Miles launches gets Probe's site folder first on
`PYTHONPATH` and `PROBE_MILES_SERVING` (the modules to wrap there); every other command runs as Miles built it."""

from __future__ import annotations

import functools
import logging
import os
import shlex
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from .serving import SERVING_ENV, SERVING_MODULES

log = logging.getLogger(__name__)

#: The folder holding Probe's `sitecustomize.py` for launched processes (shipped in the wheel with the package).
SITE_DIR = str(Path(__file__).resolve().parent / "sitecustomize")
_MARK = "__probe_wrapped__"


def find_serving_module(cmd: str) -> str | None:
    """The launch module a shell command runs with `python -m`, when it is one of `SERVING_MODULES`."""
    try:
        words = shlex.split(cmd)
    except ValueError:
        return None
    for word, following in zip(words, words[1:]):
        if word == "-m" and following in SERVING_MODULES:
            return following
    return None


def build_serving_env(cmd: str, envs: Mapping[str, str], environ: Mapping[str, str] = os.environ) -> dict[str, str]:
    """``envs`` plus Probe's two variables for a serving command; ``envs`` unchanged for any other command, or when
    Probe or its live wraps are off here (`PROBE_MILES=off`, `PROBE_MODE=disabled`, `PROBE_MILES_LIVE=0`)."""
    module = find_serving_module(cmd)
    if module is None or not is_serving_on():
        return dict(envs)
    path = envs.get("PYTHONPATH", environ.get("PYTHONPATH", ""))
    entries = [entry for entry in path.split(os.pathsep) if entry and entry != SITE_DIR]
    targets = ",".join(f"{name}={kind.value}" for name, kind in SERVING_MODULES[module].items())
    return {**envs, SERVING_ENV: targets, "PYTHONPATH": os.pathsep.join([SITE_DIR, *entries])}


def is_serving_on() -> bool:
    from probe.integrations.miles.live import is_live_on
    from probe.integrations.miles.samples.producers import is_probe_off

    return is_live_on() and not is_probe_off()


def wrap_command_actor(module: Any) -> None:
    """`miles.utils.workers.command_actor` as it loads: `CommandActor.run(cmd, envs)` (`command_actor.py:20-24`)
    launches with Probe's env when the command is a serving one."""
    actor = getattr(module, "CommandActor", None)
    original = getattr(actor, "run", None)
    if not callable(original) or getattr(original, _MARK, False):
        return

    @functools.wraps(original)
    def run(self: Any, cmd: str, envs: dict[str, str], *args: Any, **kwargs: Any) -> Any:
        try:
            envs = build_serving_env(cmd, envs or {})
        except Exception as exc:  # noqa: BLE001 -- fail open: the command launches as Miles built it
            log.warning("Probe could not prepare %r for GPU readings; it launches without them: %s", cmd, exc)
        return original(self, cmd, envs, *args, **kwargs)

    setattr(run, _MARK, True)
    actor.run = run
