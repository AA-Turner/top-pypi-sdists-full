"""Kimi Code's plugin update: re-copy every installed Probe plugin (Kimi has no update verb)."""

from __future__ import annotations
from probe.shared.harness import plugins as plugin_cli


def update_kimi_plugins() -> PluginResult:
    """Re-copy every Probe plugin Kimi Code has installed (Kimi has no update
    command; `kimi_config.install_plugin` replaces the copy in place), then
    verify the versions from the copies themselves."""
    from probe.shared.harness.harnesses.kimi_code import config as kimi_config

    if not kimi_config.binary_available():
        return PluginResult(
            False, False, False, None, None, "`kimi` not found on PATH (skipping plugin update)",
            missing_binary=True,
        )
    listed = plugin_cli.list_plugins(plugin_cli.KIMI)
    if not listed.ok:
        # Unread, not empty: a failure, never "nothing installed".
        return PluginResult(
            True, False, False, None, None,
            listed.detail or "could not read Kimi Code's plugin list",
            command_failed=True, list_unreadable=True,
        )
    installed = [
        line.split()[0]
        for line in listed.detail.splitlines()
        if line.split() and line.split()[0] in kimi_config.PLUGIN_IDS
    ]
    before_versions = {name: kimi_config.plugin_version(name) for name in installed}
    failed_run = None
    for name in installed:
        result = plugin_cli.install(plugin_cli.KIMI, name)
        if not result.ok:
            failed_run = result
            break
    failure = _failed(failed_run) if failed_run is not None else ""
    after_versions = {name: kimi_config.plugin_version(name) for name in installed}
    confirmed = not failure and all(after_versions.values())
    changed = confirmed and any(before_versions[n] != after_versions[n] for n in installed)
    before = ", ".join(f"{n}={v}" for n, v in sorted(before_versions.items())) or None
    after = ", ".join(f"{n}={after_versions[n]}" for n in installed) if confirmed else None
    tap = {
        "tap_before": before_versions.get("probe-research-tap"),
        "tap_after": after_versions.get("probe-research-tap"),
        "tap_detail": failure,
        "git_blocked": False,
        "command_failed": failed_run is not None,
    }
    if not installed:
        return PluginResult(False, False, False, None, None, "no Probe plugins installed in Kimi Code", **tap)
    if confirmed:
        message = f"Kimi Code plugins {'updated' if changed else 'verified'} ({after})"
        return PluginResult(True, True, changed, before, after, message, **tap)
    return PluginResult(True, False, False, before, after, failure or "could not confirm the Kimi Code plugins", **tap)


def manual_kimi_plugin_commands() -> str:
    from probe.shared.harness.harnesses.kimi_code import config as kimi_config

    return "\n".join(
        f"/plugins install {kimi_config.managed_dir(name)}   # inside Kimi Code"
        for name in ("probe-research", "probe-research-tap")
    )
from probe.shared.harness.plugin_update import PluginResult, _failed  # noqa: E402 -- pieces need each other; the front door loads this one first
