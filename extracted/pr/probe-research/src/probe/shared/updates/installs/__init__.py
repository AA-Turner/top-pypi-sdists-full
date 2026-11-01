"""Side-by-side CLI installs: layout, install, switch, active record, health checks, repair, shims, pruning.
Names are served live, so a patch on the defining piece reaches callers here."""

from __future__ import annotations

import importlib

# Every piece loads here, as the module did whole; names are served live below.
for _piece in (
    "probe.shared.updates.installs.active_record",
    "probe.shared.updates.installs.env_checks",
    "probe.shared.updates.installs.layout",
    "probe.shared.updates.installs.link",
    "probe.shared.updates.installs.pruning",
    "probe.shared.updates.installs.repair",
    "probe.shared.updates.installs.shims",
    "probe.shared.updates.installs.installs",
):
    importlib.import_module(_piece)
del _piece

#: Every name the front door serves -> the module that defines it.
_HOMES = {
    "ACTIVE_NAME": "probe.shared.updates.installs.active_record",
    "_record_path": "probe.shared.updates.installs.active_record",
    "record": "probe.shared.updates.installs.active_record",
    "_write_record": "probe.shared.updates.installs.active_record",
    "active": "probe.shared.updates.installs.active_record",
    "REJECT_TTL_S": "probe.shared.updates.installs.active_record",
    "_mark": "probe.shared.updates.installs.active_record",
    "rejected": "probe.shared.updates.installs.active_record",
    "reject": "probe.shared.updates.installs.active_record",
    "set_fields": "probe.shared.updates.installs.active_record",
    "record_dropped_with": "probe.shared.updates.installs.active_record",
    "dropped_with": "probe.shared.updates.installs.active_record",
    "dropped_python": "probe.shared.updates.installs.active_record",
    "clear_rejected": "probe.shared.updates.installs.active_record",
    "UNKNOWN_SIGNALS": "probe.shared.updates.installs.env_checks",
    "UNKNOWN_SPAWN_ERRNOS": "probe.shared.updates.installs.env_checks",
    "env_version": "probe.shared.updates.installs.env_checks",
    "selftest": "probe.shared.updates.installs.env_checks",
    "selftest_checked": "probe.shared.updates.installs.env_checks",
    "health": "probe.shared.updates.installs.env_checks",
    "check": "probe.shared.updates.installs.env_checks",
    "_machines": "probe.shared.updates.installs.env_checks",
    "_dist_info_version": "probe.shared.updates.installs.env_checks",
    "DIST": "probe.shared.updates.installs.layout",
    "VERSIONS_DIRNAME": "probe.shared.updates.installs.layout",
    "_VERSION": "probe.shared.updates.installs.layout",
    "_UV_TIMEOUT_S": "probe.shared.updates.installs.layout",
    "tool_dir": "probe.shared.updates.installs.layout",
    "tool_env": "probe.shared.updates.installs.layout",
    "versions_root": "probe.shared.updates.installs.layout",
    "version_env": "probe.shared.updates.installs.layout",
    "_FOLDER": "probe.shared.updates.installs.layout",
    "folder_parts": "probe.shared.updates.installs.layout",
    "generation_env": "probe.shared.updates.installs.layout",
    "_folders": "probe.shared.updates.installs.layout",
    "next_generation": "probe.shared.updates.installs.layout",
    "envs_of": "probe.shared.updates.installs.layout",
    "same_filesystem": "probe.shared.updates.installs.layout",
    "usable": "probe.shared.updates.installs.layout",
    "running_from_versions": "probe.shared.updates.installs.layout",
    "versions_root_of": "probe.shared.updates.installs.layout",
    "is_link": "probe.shared.updates.installs.link",
    "_make_link": "probe.shared.updates.installs.link",
    "_drop_link": "probe.shared.updates.installs.link",
    "_swap_link": "probe.shared.updates.installs.link",
    "env_python": "probe.shared.updates.installs.link",
    "KEEP": "probe.shared.updates.installs.pruning",
    "PRUNE_MIN_AGE_S": "probe.shared.updates.installs.pruning",
    "discard": "probe.shared.updates.installs.pruning",
    "USED_PREFIX": "probe.shared.updates.installs.pruning",
    "USED_FRESH_S": "probe.shared.updates.installs.pruning",
    "_commands": "probe.shared.updates.installs.pruning",
    "_in_use": "probe.shared.updates.installs.pruning",
    "_machine": "probe.shared.updates.installs.pruning",
    "_mtime": "probe.shared.updates.installs.pruning",
    "mark_in_use": "probe.shared.updates.installs.pruning",
    "_version_key": "probe.shared.updates.installs.pruning",
    "_place": "probe.shared.updates.installs.pruning",
    "_installed_at": "probe.shared.updates.installs.pruning",
    "_used_elsewhere": "probe.shared.updates.installs.pruning",
    "prune": "probe.shared.updates.installs.pruning",
    "needs_migration": "probe.shared.updates.installs.repair",
    "_migrate": "probe.shared.updates.installs.repair",
    "recover": "probe.shared.updates.installs.repair",
    "ToolPath": "probe.shared.updates.installs.repair",
    "adopt_plain": "probe.shared.updates.installs.repair",
    "tool_state": "probe.shared.updates.installs.repair",
    "fix_record": "probe.shared.updates.installs.repair",
    "cleanup": "probe.shared.updates.installs.repair",
    "RECEIPT": "probe.shared.updates.installs.shims",
    "_INSTALL_PATH": "probe.shared.updates.installs.shims",
    "_receipt_bins": "probe.shared.updates.installs.shims",
    "bin_dir": "probe.shared.updates.installs.shims",
    "fix_receipt": "probe.shared.updates.installs.shims",
    "entrypoints": "probe.shared.updates.installs.shims",
    "_ours": "probe.shared.updates.installs.shims",
    "ensure_shims": "probe.shared.updates.installs.shims",
    "LOCK_WAIT_S": "probe.shared.updates.installs.installs",
    "refuse_while_uninstalling": "probe.shared.updates.installs.installs",
    "_UV_TRUE": "probe.shared.updates.installs.installs",
    "uv_offline": "probe.shared.updates.installs.installs",
    "install_command": "probe.shared.updates.installs.installs",
    "install": "probe.shared.updates.installs.installs",
    "protected": "probe.shared.updates.installs.installs",
    "_target": "probe.shared.updates.installs.installs",
    "_install": "probe.shared.updates.installs.installs",
    "activate": "probe.shared.updates.installs.installs",
    "_activate": "probe.shared.updates.installs.installs",
    "_same": "probe.shared.updates.installs.installs",
    "previous": "probe.shared.updates.installs.installs",
    "switch_back": "probe.shared.updates.installs.installs",
    # Imported by the module before the split: served for its callers too.
    "Path": "probe.shared.updates.installs.active_record",
    "contextlib": "probe.shared.updates.installs.active_record",
    "errno": "probe.shared.updates.installs.env_checks",
    "handoff": "probe.shared.updates.installs.active_record",
    "json": "probe.shared.updates.installs.active_record",
    "os": "probe.shared.updates.installs.active_record",
    "re": "probe.shared.updates.installs.env_checks",
    "shutil": "probe.shared.updates.installs.layout",
    "signal": "probe.shared.updates.installs.env_checks",
    "subprocess": "probe.shared.updates.installs.env_checks",
    "sys": "probe.shared.updates.installs.layout",
    "time": "probe.shared.updates.installs.active_record",
    "uninstall_barrier": "probe.shared.updates.installs.installs",
}


def __getattr__(name: str):
    home = _HOMES.get(name)
    if home is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return getattr(importlib.import_module(home), name)


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(_HOMES))
