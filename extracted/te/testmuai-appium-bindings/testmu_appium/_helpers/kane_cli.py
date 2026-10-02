"""execute_kane_cli — walk a conditional branch nobody recorded, at run time.

A recorded if/else carries every branch's objective (auteur's custom_event)
but operations only for the branch that ran during authoring. The others
export as a handoff: kane-cli joins THIS Appium session and lets the agent
walk the branch objective on the live device, then returns the session
untouched. The Playwright binding does the same through a relay proxy because
a browser connection cannot be shared; an Appium session is a plain HTTP
session, so here the handoff is the server URL plus the session id.

Environment (all set by the export's job config, or by the caller's shell):
    LT_USERNAME / LT_ACCESS_KEY — kane-cli auth
    TESTMUAI_ENV                — stage | prod, the controller kane-cli talks to
"""
import logging
import os
import shutil
import subprocess

from testmu_appium import _config
from testmu_appium._errors import TestmuConfigError
from testmu_appium._vars import var

_log = logging.getLogger("testmu_appium")

#: Upper bound on one branch walk. The same ceiling the Playwright binding gives
#: kane-cli; a branch that has not finished in ten minutes is not going to.
_TIMEOUT_S = 600

#: How much of kane-cli's output to keep in a failure message.
_TAIL = 2000


def _session_endpoint(driver) -> tuple[str, str]:
    """The Appium server URL this driver talks to, and its session id."""
    executor = getattr(driver, "command_executor", None)
    url = getattr(executor, "_url", None)
    if not url:
        url = (
            _config.resolved("lt_hub_url", _config._resolve_lt_hub_url)
            if _config.run_target == "cloud"
            else _config.resolved("appium_url", _config._resolve_appium_url)
        )
    session_id = getattr(driver, "session_id", None) or ""
    return str(url), str(session_id)


def _resolve_objective(objective: str) -> str:
    """The branch objective with ``{{var}}`` / ``${param}`` references filled in.

    kane-cli runs with ``--local`` and has no view of this test's variable
    store, so a reference left in the text would reach the agent as literal
    braces.
    """
    resolved = var(objective)
    return objective if resolved is None else str(resolved)


def _reapply_driver_settings(driver) -> None:
    """Restore this binding's Appium settings after the runner applied its own.

    The runner tunes the shared session for its perception (idle waits, tree
    depth); those settings persist on the server and would otherwise shape
    every step that follows the branch.
    """
    from testmu_appium import _session  # noqa: PLC0415 — avoid a module cycle

    _session._apply_driver_settings(driver)


def execute_kane_cli(driver, *, objective: str, description: str = "") -> bool:
    """Hand ``objective`` to kane-cli on the live session; True when it ran.

    Raises when the handoff cannot be made — smart mode off, kane-cli not on
    PATH, no live session — and when kane-cli ran and failed. A branch that was
    reachable and did not complete is a test failure, not a skip.
    """
    label = description or objective
    if not _config.smart_enabled():
        raise TestmuConfigError(
            "execute_kane_cli: smart mode is not enabled (TESTMU_SMART off, or degraded "
            "because LT_USERNAME/LT_ACCESS_KEY are missing); an unrecorded branch needs "
            f"the agent to run it: {label[:80]!r}"
        )
    kane_cli = shutil.which("kane-cli")
    if not kane_cli:
        raise TestmuConfigError(
            "execute_kane_cli: kane-cli is not on PATH; install it (npm install -g "
            f"kane-cli) to run the unrecorded branch {label[:80]!r}"
        )

    url, session_id = _session_endpoint(driver)
    if not session_id:
        raise TestmuConfigError(
            "execute_kane_cli: the driver has no session id; a handoff needs a live session"
        )
    resolved_objective = _resolve_objective(objective)
    cmd = [
        kane_cli, "run", resolved_objective,
        "--appium-url", url,
        "--appium-session-id", session_id,
        # Beside a session id kane-cli's --target names the session's platform,
        # not a device class to boot.
        "--target", _config.platform(),
        "--username", os.getenv("LT_USERNAME", ""),
        "--access-key", os.getenv("LT_ACCESS_KEY", ""),
        "--env", os.getenv("TESTMUAI_ENV", "prod"),
        "--local",
        "--agent",
    ]
    _log.info(
        "[execute_kane_cli] handing the session to kane-cli | objective=%r url=%s session=%s platform=%s",
        resolved_objective[:80], url, session_id, _config.platform(),
    )
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=_TIMEOUT_S)
    finally:
        _reapply_driver_settings(driver)
    if proc.returncode != 0:
        raise RuntimeError(
            f"kane-cli failed (exit {proc.returncode}) on branch {resolved_objective!r}: "
            f"{(proc.stderr or proc.stdout or '')[-_TAIL:]}"
        )
    _log.info("[execute_kane_cli] kane-cli finished the branch; session resumes | %s",
              (proc.stdout or "")[-300:].strip())
    return True
