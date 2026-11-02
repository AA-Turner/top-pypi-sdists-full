"""The OS keeper that restarts the service after a crash, one scheduler per OS.
Front door for the old `probe.service.keeper`: names read live, a patch reaches every piece binding the name."""

from __future__ import annotations

from probe.foundation.front_door.front_door import serve_pieces

# Every piece loads here, in load order, as the old module ran whole on import (static, so the
# test gate's import graph sees this door use them).
import probe.service.keeper.scheduler as _piece_scheduler  # noqa: F401
import probe.service.keeper.check as _piece_check  # noqa: F401
import probe.service.keeper.home as _piece_home  # noqa: F401
import probe.service.keeper.schedulers.launchd as _piece_launchd  # noqa: F401
import probe.service.keeper.schedulers.systemd as _piece_systemd  # noqa: F401
import probe.service.keeper.schedulers.windows_task as _piece_windows_task  # noqa: F401
import probe.service.keeper.keeper as _piece_keeper  # noqa: F401

#: The old module's pieces, in load order: a write through the door reaches these only.
_PIECES = (
    "probe.service.keeper.scheduler",
    "probe.service.keeper.check",
    "probe.service.keeper.home",
    "probe.service.keeper.schedulers.launchd",
    "probe.service.keeper.schedulers.systemd",
    "probe.service.keeper.schedulers.windows_task",
    "probe.service.keeper.keeper",
)

#: Every name the old module bound -> the piece that holds it (defines it, else imports it).
_HOMES = {
    # probe.service.keeper.scheduler
    "INTERVAL_S": "probe.service.keeper.scheduler",
    "LABEL": "probe.service.keeper.scheduler",
    "NAME": "probe.service.keeper.scheduler",
    "Path": "probe.service.keeper.scheduler",
    "START_TIMEOUT_S": "probe.service.keeper.scheduler",
    "TIMEOUT_S": "probe.service.keeper.scheduler",
    "_manager_env": "probe.service.keeper.scheduler",
    "_run": "probe.service.keeper.scheduler",
    "_write": "probe.service.keeper.scheduler",
    "os": "probe.service.keeper.scheduler",
    "subprocess": "probe.service.keeper.scheduler",
    # probe.service.keeper.check
    "DOWN_REPORT_S": "probe.service.keeper.check",
    "Down": "probe.service.keeper.check",
    "GAP_S": "probe.service.keeper.check",
    "HELLO_TIMEOUT_S": "probe.service.keeper.check",
    "REPORT_EVERY_S": "probe.service.keeper.check",
    "STATE_NAME": "probe.service.keeper.check",
    "_answers": "probe.service.keeper.check",
    "_log": "probe.service.keeper.check",
    "_monotonic": "probe.service.keeper.check",
    "_report": "probe.service.keeper.check",
    "_save": "probe.service.keeper.check",
    "_settle": "probe.service.keeper.check",
    "_state": "probe.service.keeper.check",
    "_uninstalling": "probe.service.keeper.check",
    "contextlib": "probe.service.keeper.check",
    "paths": "probe.service.keeper.check",
    "time": "probe.service.keeper.check",
    # probe.service.keeper.home
    "_home_without_entry": "probe.service.keeper.home",
    "_own_home": "probe.service.keeper.home",
    "_temp_roots": "probe.service.keeper.home",
    "_windows_profile": "probe.service.keeper.home",
    "stat": "probe.service.keeper.home",
    # probe.service.keeper.schedulers.launchd
    "_install_launchd": "probe.service.keeper.schedulers.launchd",
    "_plist": "probe.service.keeper.schedulers.launchd",
    "_plist_path": "probe.service.keeper.schedulers.launchd",
    "_remove_launchd": "probe.service.keeper.schedulers.launchd",
    # probe.service.keeper.schedulers.systemd
    "_install_systemd": "probe.service.keeper.schedulers.systemd",
    "_remove_systemd": "probe.service.keeper.schedulers.systemd",
    "_systemd_dir": "probe.service.keeper.schedulers.systemd",
    "_systemd_units": "probe.service.keeper.schedulers.systemd",
    "systemd_manager": "probe.service.keeper.schedulers.systemd",
    # probe.service.keeper.schedulers.windows_task
    "_install_schtasks": "probe.service.keeper.schedulers.windows_task",
    "_remove_schtasks": "probe.service.keeper.schedulers.windows_task",
    "_task_marker": "probe.service.keeper.schedulers.windows_task",
    "_task_name": "probe.service.keeper.schedulers.windows_task",
    "_task_xml": "probe.service.keeper.schedulers.windows_task",
    # probe.service.keeper.keeper
    "ENV": "probe.service.keeper.keeper",
    "LOCK_WAIT_S": "probe.service.keeper.keeper",
    "Mapping": "probe.service.keeper.keeper",
    "OFF_NAME": "probe.service.keeper.keeper",
    "_install": "probe.service.keeper.keeper",
    "_locked": "probe.service.keeper.keeper",
    "_off_path": "probe.service.keeper.keeper",
    "_python": "probe.service.keeper.keeper",
    "allow": "probe.service.keeper.keeper",
    "install": "probe.service.keeper.keeper",
    "install_lifeboat": "probe.service.keeper.keeper",
    "json": "probe.service.keeper.keeper",
    "lifeboat": "probe.service.keeper.keeper",
    "main": "probe.service.keeper.keeper",
    "needed": "probe.service.keeper.keeper",
    "procid": "probe.service.keeper.keeper",
    "refresh_lifeboat": "probe.service.keeper.keeper",
    "remove": "probe.service.keeper.keeper",
    "sys": "probe.service.keeper.keeper",
    "wanted": "probe.service.keeper.keeper",
}

serve_pieces(__name__, _HOMES, pieces=_PIECES)
