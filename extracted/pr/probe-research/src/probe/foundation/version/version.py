"""The installed probe-research version: `probe.__version__` re-exports it, and a lower layer
reads it here (`import probe` loads the SDK's errors, which foundation and analytics never import).
"""

from __future__ import annotations

from importlib import metadata

# The distribution name, not the import name (`probe`). Renamed from `probe-agent` on
# 2026-07-15: that name is an unrelated project on PyPI that we never owned, so
# `pip install probe-agent` fetched a stranger's package. Keep this in step with
# `[project].name` in pyproject.toml — a mismatch is silent, and degrades `probe
# --version` to the dev fallback below.
DISTRIBUTION = "probe-research"

try:  # the installed dist is the single source of version truth (pyproject)
    VERSION = metadata.version(DISTRIBUTION)
except metadata.PackageNotFoundError:  # running from a source tree
    VERSION = "0.0.0.dev0"
