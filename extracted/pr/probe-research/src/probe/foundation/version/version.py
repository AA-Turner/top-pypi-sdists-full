"""The installed probe-research version: `probe.__version__` re-exports it, and a lower layer
reads it here (`import probe` loads the SDK's errors, which foundation and analytics never import).
"""

from __future__ import annotations

import os
import sys

# The distribution name, not the import name (`probe`). Renamed from `probe-agent` on
# 2026-07-15: that name is an unrelated project on PyPI that we never owned, so
# `pip install probe-agent` fetched a stranger's package. Keep this in step with
# `[project].name` in pyproject.toml — a mismatch is silent, and degrades `probe
# --version` to the dev fallback below.
DISTRIBUTION = "probe-research"



def read_installed_version(distribution: str = DISTRIBUTION, paths: list[str] | None = None) -> str | None:
    """The first `<distribution>-<v>.dist-info` on `paths` (sys.path) says the version, as
    `importlib.metadata.version` finds it, without importing that (~40 ms of every `probe`)."""
    prefix = distribution.replace("-", "_") + "-"
    for entry in sys.path if paths is None else paths:
        try:
            names = os.listdir(entry or ".")
        except OSError:
            continue
        for name in names:
            if not (name.lower().startswith(prefix) and name.endswith(".dist-info")):
                continue
            try:
                with open(os.path.join(entry or ".", name, "METADATA"), encoding="utf-8") as handle:
                    for line in handle:
                        if line.startswith("Version:"):
                            return line.split(":", 1)[1].strip()
                        if not line.strip():
                            break
            except OSError:
                continue
    return None


def _read_version() -> str:
    found = read_installed_version()
    if found:
        return found
    from importlib import metadata

    try:  # the installed dist is the single source of version truth (pyproject)
        return metadata.version(DISTRIBUTION)
    except metadata.PackageNotFoundError:  # running from a source tree
        return "0.0.0.dev0"


VERSION = _read_version()


def is_older(found: object, own: object) -> bool:
    """Is release `found` older than release `own`? False when either is no release
    (`0.0.0.dev0`, a local build): nothing to compare."""
    def parse(value: object) -> tuple | None:
        if not isinstance(value, str):
            return None
        head = value.split("+", 1)[0].split(".")
        return tuple(int(p) for p in head) if len(head) >= 3 and all(p.isdigit() for p in head) else None

    older, newer = parse(found), parse(own)
    return older is not None and newer is not None and older < newer
