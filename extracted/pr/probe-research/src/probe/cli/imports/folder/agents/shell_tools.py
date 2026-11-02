"""the commands an agent's shell may run, pinned to this interpreter: our `probe` and the session's `probe-backfill-plan`."""

from __future__ import annotations

import os
import contextlib
import shlex
import sys
import tempfile
import threading
from dataclasses import dataclass
from pathlib import Path


_BACKFILL_CLI_LOCK = threading.Lock()
_BACKFILL_CLI_BIN: tempfile.TemporaryDirectory | None = None


def _backfill_cli_bin() -> tempfile.TemporaryDirectory:
    """Keep agent shell commands on the importer's package and interpreter.

    A wizard launched from an isolated installation can inherit an older
    ``probe`` on PATH. That CLI may lack backfill attribution and attach the
    importing agent's session to reconstructed entities. A private launcher
    also supports editable/source installs without a sibling console script.
    The cached directory stays alive until this importer process exits.
    """
    global _BACKFILL_CLI_BIN
    with _BACKFILL_CLI_LOCK:
        if _BACKFILL_CLI_BIN is None:
            directory = tempfile.TemporaryDirectory(prefix="probe-backfill-cli-")
            bootstrap = (
                "import os, sys; "
                f"sys.path.insert(0, {str(Path(__file__).resolve().parents[5])!r}); "
                "os.environ['PROBE_ATTRIBUTION'] = 'backfill'; "
                "from probe.cli import main; raise SystemExit(main())"
            )
            launcher = Path(directory.name) / "probe"
            launcher.write_text(
                "#!/bin/sh\nexec "
                + shlex.quote(sys.executable)
                + " -c "
                + shlex.quote(bootstrap)
                + ' "$@"\n',
                encoding="utf-8",
            )
            launcher.chmod(0o700)
            _BACKFILL_CLI_BIN = directory
        return _BACKFILL_CLI_BIN


def _backfill_agent_env(path_prepend: str | None = None) -> dict[str, str]:
    path = _backfill_cli_bin().name + os.pathsep + os.environ.get("PATH", "")
    if path_prepend:
        path = path_prepend + os.pathsep + path
    # No Claude Code auto memory either (see `readonly_settings`): headless flags alone
    # leave it on, so the variable is set beside the setting.
    return {**os.environ, "PROBE_ATTRIBUTION": "backfill", "PATH": path,
            "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1"}


#: The classifier's filing tool, as the agent types it. See `plan_tool_launcher`.
PLAN_TOOL_COMMAND = "probe-backfill-plan"


@dataclass(frozen=True)
class PlanTool:
    """One classifier session's `probe-backfill-plan` state.

    `ref_dir` holds the session's file list and project list and sits OUTSIDE
    the agent's work dir, so the agent can read it but not rewrite what it is
    checked against. `log` is the decisions log and sits INSIDE the work dir,
    because Codex's sandbox confines the tool's writes as well as the agent's.
    """

    ref_dir: Path
    log: Path


@contextlib.contextmanager
def plan_tool_launcher(tool: PlanTool):
    """A `probe` for ONE agent session, with its plan state baked in.

    Per launch because classifier sessions run concurrently in one work dir,
    and baked into the script rather than passed as environment variables
    because Codex filters what reaches its shell; PATH is the one channel the
    import already depends on. It runs the stdlib-only tool module by file path
    (importing `probe.cli` costs ~0.8 s a call).

    ITS OWN EXECUTABLE, `probe-backfill-plan`, not a `probe` subcommand,
    because it is not a Probe command: no network, no credential, no team
    record read or written. It edits one local file in the agent's own work dir
    (the decisions log) after checking each line against a local file list --
    the same file the agent could already write with its `Write` tool, minus the
    checking. The researcher's tracking guard governs `probe` commands, which
    reach the team's records; a session-local helper is outside what it guards,
    exactly like `Write` or `ls`, so there is nothing for it to allow or refuse.
    Being a `probe` subcommand would also have put it behind the CLI's whole
    import path (~0.8 s a call) and behind each machine's installed plugin
    allowlist, which a CLI release does not update.
    """
    directory = tempfile.TemporaryDirectory(prefix="probe-backfill-plan-")
    # ABSOLUTE: the agent's shell runs in its work dir, so a relative state
    # path baked in here would resolve against the wrong directory and every
    # call would fail to find its file list.
    tool = PlanTool(ref_dir=Path(os.path.abspath(tool.ref_dir)), log=Path(os.path.abspath(tool.log)))
    try:
        tool_file = Path(__file__).resolve().parents[1] / "classify" / "plan_tool.py"
        fast = (
            "import importlib.util, sys; "
            f"spec = importlib.util.spec_from_file_location('probe_backfill_plan_tool', {str(tool_file)!r}); "
            "m = importlib.util.module_from_spec(spec); sys.modules[spec.name] = m; "
            "spec.loader.exec_module(m); raise SystemExit(m.main(sys.argv[1:]))"
        )
        launcher = Path(directory.name) / PLAN_TOOL_COMMAND
        launcher.write_text(
            "#!/bin/sh\n"
            f"PROBE_PLAN_REF={shlex.quote(str(tool.ref_dir))}; export PROBE_PLAN_REF\n"
            f"PROBE_PLAN_LOG={shlex.quote(str(tool.log))}; export PROBE_PLAN_LOG\n"
            "exec " + shlex.quote(sys.executable) + " -c " + shlex.quote(fast) + ' "$@"\n',
            encoding="utf-8",
        )
        launcher.chmod(0o700)
        yield directory.name
    finally:
        directory.cleanup()
