"""pi: its settings entry, package source and profile, pins, its session log (pi_config split by job).
Names are served live, so a patch on the defining piece reaches callers here."""

from __future__ import annotations

import importlib

# Every piece loads here, as the module did whole; names are served live below.
for _piece in (
    "probe.shared.harness.harnesses.pi.package_source",
    "probe.shared.harness.harnesses.pi.settings",
    "probe.shared.harness.harnesses.pi.profile",
    "probe.shared.harness.harnesses.pi.package_entry",
    "probe.shared.harness.harnesses.pi.package_update",
    "probe.shared.harness.harnesses.pi.pi",
):
    importlib.import_module(_piece)
del _piece

#: Every name the front door serves -> the module that defines it.
_HOMES = {
    "PACKAGE_NAME": "probe.shared.harness.harnesses.pi.package_source",
    "OUR_NPM_SOURCE": "probe.shared.harness.harnesses.pi.package_source",
    "PACKAGE_ROOT_ENV": "probe.shared.harness.harnesses.pi.package_source",
    "_PACKAGE_RELATIVE_PATH": "probe.shared.harness.harnesses.pi.package_source",
    "MIRROR_REPO": "probe.shared.harness.harnesses.pi.package_source",
    "MIRROR_GIT_SOURCE": "probe.shared.harness.harnesses.pi.package_source",
    "_MIRROR_IDENTITY": "probe.shared.harness.harnesses.pi.package_source",
    "PackageRootError": "probe.shared.harness.harnesses.pi.package_source",
    "resolve_package_root": "probe.shared.harness.harnesses.pi.package_source",
    "local_package_root": "probe.shared.harness.harnesses.pi.package_source",
    "resolve_install_source": "probe.shared.harness.harnesses.pi.package_source",
    "_git_repo_identity": "probe.shared.harness.harnesses.pi.package_source",
    "_entry_source": "probe.shared.harness.harnesses.pi.package_source",
    "_identifies_ours": "probe.shared.harness.harnesses.pi.package_source",
    "_declared_package_name": "probe.shared.harness.harnesses.pi.package_source",
    "_our_entry_index": "probe.shared.harness.harnesses.pi.package_source",
    "_skill_prefix": "probe.shared.harness.harnesses.pi.package_source",
    "_SettingsRefusal": "probe.shared.harness.harnesses.pi.settings",
    "pi_agent_dir": "probe.shared.harness.harnesses.pi.settings",
    "settings_path": "probe.shared.harness.harnesses.pi.settings",
    "project_settings_path": "probe.shared.harness.harnesses.pi.settings",
    "_load_settings": "probe.shared.harness.harnesses.pi.settings",
    "_write_settings": "probe.shared.harness.harnesses.pi.settings",
    "DAEMON_MIN_PACKAGE_VERSION": "probe.shared.harness.harnesses.pi.profile",
    "DAEMON_PACKAGE_SKILLS": "probe.shared.harness.harnesses.pi.profile",
    "DAEMON_EXTENSION_SKILLS": "probe.shared.harness.harnesses.pi.profile",
    "_loads_our_extension": "probe.shared.harness.harnesses.pi.profile",
    "AGENT_SKILLS_STASH_KEY": "probe.shared.harness.harnesses.pi.profile",
    "_daemon_filter": "probe.shared.harness.harnesses.pi.profile",
    "_is_daemon_filter": "probe.shared.harness.harnesses.pi.profile",
    "TRACKING_KEY": "probe.shared.harness.harnesses.pi.profile",
    "TRACKING_OFF_MIN_PACKAGE_VERSION": "probe.shared.harness.harnesses.pi.profile",
    "_entry_for": "probe.shared.harness.harnesses.pi.profile",
    "_rewrite_entry": "probe.shared.harness.harnesses.pi.profile",
    "_entry_axes": "probe.shared.harness.harnesses.pi.profile",
    "set_profile": "probe.shared.harness.harnesses.pi.profile",
    "set_tracking": "probe.shared.harness.harnesses.pi.profile",
    "PROFILE_TRACKING_OFF": "probe.shared.harness.harnesses.pi.profile",
    "entry_profile": "probe.shared.harness.harnesses.pi.profile",
    "_LEGACY_EXTENSION_RELATIVE": "probe.shared.harness.harnesses.pi.package_entry",
    "MergedPackageEntry": "probe.shared.harness.harnesses.pi.package_entry",
    "_our_entry_in": "probe.shared.harness.harnesses.pi.package_entry",
    "merged_package_entry": "probe.shared.harness.harnesses.pi.package_entry",
    "MCP_ADAPTER_NAME": "probe.shared.harness.harnesses.pi.package_entry",
    "mcp_adapter_installed": "probe.shared.harness.harnesses.pi.package_entry",
    "install_package_entry": "probe.shared.harness.harnesses.pi.package_entry",
    "remove_package_entry": "probe.shared.harness.harnesses.pi.package_entry",
    "package_entry_installed": "probe.shared.harness.harnesses.pi.package_entry",
    "migrate_legacy_symlink": "probe.shared.harness.harnesses.pi.package_entry",
    "UPDATE_TIMEOUT_S": "probe.shared.harness.harnesses.pi.package_update",
    "installed_package_dir": "probe.shared.harness.harnesses.pi.package_update",
    "installed_package_version": "probe.shared.harness.harnesses.pi.package_update",
    "update_package": "probe.shared.harness.harnesses.pi.package_update",
    "HARNESS_ID": "probe.shared.harness.harnesses.pi.pi",
    "pi_on_path": "probe.shared.harness.harnesses.pi.pi",
    "pi_binary_available": "probe.shared.harness.harnesses.pi.pi",
    # Imported by the module before the split: served for its callers too.
    "Mapping": "probe.shared.harness.harnesses.pi.package_source",
    "Path": "probe.shared.harness.harnesses.pi.package_source",
    "claude_cli": "probe.shared.harness.harnesses.pi.profile",
    "dataclass": "probe.shared.harness.harnesses.pi.package_entry",
    "json": "probe.shared.harness.harnesses.pi.package_source",
    "lru_cache": "probe.shared.harness.harnesses.pi.pi",
    "os": "probe.shared.harness.harnesses.pi.package_source",
    "shutil": "probe.shared.harness.harnesses.pi.package_update",
    "subprocess": "probe.shared.harness.harnesses.pi.package_update",
    "through_symlink": "probe.shared.harness.harnesses.pi.settings",
    "write_text_atomic": "probe.shared.harness.harnesses.pi.settings",
}


def __getattr__(name: str):
    home = _HOMES.get(name)
    if home is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return getattr(importlib.import_module(home), name)


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(_HOMES))
