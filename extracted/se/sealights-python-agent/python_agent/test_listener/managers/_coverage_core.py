"""Coverage core selection helper.

On Python 3.12+ the vendored coverage.py exposes a ``sys.monitoring``
("sysmon") tracer core. That core uses PEP 669's ``DISABLE`` mechanism:
once a bytecode offset fires its event, it is permanently muted for that
monitoring tool.

For **server-mode** (long-running) commands, the agent calls erase()
periodically between footprint flushes. erase() clears recorded data but
does not restart disabled events, so sysmon goes silent after the first
flush. These commands need pytrace.

For **runner-managed** commands (pytest, nose, unittest, behave), erase()
is not called in the hot loop and set_execution_active() no longer
discards pre-execution coverage. Coverage uses a cumulative snapshot;
sysmon works correctly for these commands and is much faster than pytrace.
"""

from __future__ import annotations

import os
import sys
from typing import Optional

from python_agent.common.constants import RUNNER_MANAGED_COMMANDS

COVERAGE_CORE_ENV = "COVERAGE_CORE"
PYTRACE = "pytrace"
MIN_PY_FOR_PYTRACE_DEFAULT = (3, 12)


def apply_pytrace_default(command_name: Optional[str] = None) -> None:
    """Default ``COVERAGE_CORE`` to ``pytrace`` on Python >= 3.12,
    but only for non-runner-managed commands (server mode).

    Runner-managed commands (pytest, nose, unittest, behave) use the
    cumulative snapshot path which never calls erase() in the hot loop,
    so sysmon works correctly and is much faster.

    No-op when ``COVERAGE_CORE`` is already set in the environment,
    when the running interpreter is older than 3.12, or when the
    command is runner-managed.
    """
    if sys.version_info < MIN_PY_FOR_PYTRACE_DEFAULT:
        return
    if command_name in RUNNER_MANAGED_COMMANDS:
        return
    os.environ.setdefault(COVERAGE_CORE_ENV, PYTRACE)
