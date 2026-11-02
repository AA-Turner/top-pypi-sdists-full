"""Windows: a Task Scheduler task running `-I -m probe.service.keeper`."""

from __future__ import annotations

import contextlib
import os
from pathlib import Path

from ....foundation.service_api import paths
from probe.service.keeper.scheduler import _run, _write


# -- Windows: a Task Scheduler task ----------------------------------------------------

def _task_name() -> str:
    """Task names are machine-wide: one per Windows user (by their SID)."""
    import hashlib

    try:
        from ....foundation.service_api import winpipe

        who = hashlib.sha256(winpipe.user_sid().encode("utf-8")).hexdigest()[:12]
    except Exception:  # noqa: BLE001
        who = hashlib.sha256(os.environ.get("USERNAME", "user").encode("utf-8")).hexdigest()[:12]
    return f"Probe service keeper {who}"


def _task_marker() -> Path:
    return paths.root_dir() / "keeper-task.txt"


def _task_xml(runner: str) -> str:
    """The task: every minute, indefinitely, only while this user is logged
    on, and on battery too (`schtasks /SC MINUTE` would take the AC-only
    defaults, and a laptop on battery would never start the service again)."""
    from xml.sax.saxutils import escape

    return (
        '<?xml version="1.0" encoding="UTF-16"?>\n'
        '<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">\n'
        "  <RegistrationInfo><Description>Start the Probe service again when it stopped while recording"
        "</Description></RegistrationInfo>\n"
        "  <Triggers><TimeTrigger><Repetition><Interval>PT1M</Interval>"
        "<StopAtDurationEnd>false</StopAtDurationEnd></Repetition>"
        "<StartBoundary>2026-01-01T00:00:00</StartBoundary><Enabled>true</Enabled></TimeTrigger></Triggers>\n"
        '  <Principals><Principal id="Author"><LogonType>InteractiveToken</LogonType>'
        "<RunLevel>LeastPrivilege</RunLevel></Principal></Principals>\n"
        "  <Settings><MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>"
        "<DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>"
        "<StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>"
        "<StartWhenAvailable>true</StartWhenAvailable>"
        "<RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>"
        "<IdleSettings><StopOnIdleEnd>false</StopOnIdleEnd><RestartOnIdle>false</RestartOnIdle></IdleSettings>"
        "<AllowStartOnDemand>true</AllowStartOnDemand><Enabled>true</Enabled><Hidden>true</Hidden>"
        "<RunOnlyIfIdle>false</RunOnlyIfIdle><ExecutionTimeLimit>PT5M</ExecutionTimeLimit>"
        "<Priority>7</Priority></Settings>\n"
        f'  <Actions Context="Author"><Exec><Command>{escape(runner)}</Command>'
        "<Arguments>-I -m probe.service.keeper</Arguments></Exec></Actions>\n"
        "</Task>\n"
    )


def _install_schtasks(python: str) -> str:
    windowless = Path(python).with_name("pythonw.exe")
    runner = str(windowless) if windowless.exists() else python
    xml = _task_xml(runner)
    try:
        if _task_marker().read_text(encoding="utf-8") == xml:
            listed = _run(["schtasks", "/Query", "/TN", _task_name()])
            if listed is not None and listed.returncode == 0:
                return "current"
    except OSError:
        pass
    definition = paths.root_dir() / f".keeper-task.{os.getpid()}.xml"
    try:
        definition.write_text(xml, encoding="utf-16")  # what schtasks reads (with its BOM)
        done = _run(["schtasks", "/Create", "/F", "/TN", _task_name(), "/XML", str(definition)])
    finally:
        with contextlib.suppress(OSError):
            definition.unlink()
    if done is None or done.returncode != 0:
        return f"schtasks /Create failed: {((done.stderr or done.stdout) if done else '').strip()[:200]}"
    with contextlib.suppress(OSError):
        _write(_task_marker(), xml)
    return "installed"


def _remove_schtasks() -> None:
    _run(["schtasks", "/Delete", "/F", "/TN", _task_name()])
    with contextlib.suppress(OSError):
        _task_marker().unlink()
