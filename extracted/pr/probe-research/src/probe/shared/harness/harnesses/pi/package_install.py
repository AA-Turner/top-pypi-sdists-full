"""pi's PluginInstaller: install or remove our settings.json package entry (both halves ride one package) and the project-entry override check."""

from __future__ import annotations
from pathlib import Path
from probe.shared.harness.harnesses.claude_code import binary as claude_cli
from probe.shared.harness.harnesses import pi as pi_config
from probe.cli.wizard.state.capture_credentials import (
    capture_token_sources,
    tap_plugin_dir)


def _install_pi_package(*, tracking: bool = True) -> claude_cli.Result:
    """The `source == "pi"` half of `install_plugin`.

    Kept as its own function so `install_plugin` itself stays one dispatch
    read top to bottom, not a growing if/elif column -- the same reason
    `refresh_marketplace` got hoisted out from per-plugin duplication.

    `pi_config.install_package_entry` is already idempotent and already
    returns exactly the `claude_cli.Result` shape this call site needs (see
    that module's own docstring on why `claude_cli.Result` specifically).
    Migration (plan D4) only changes the returned `detail` when it actually
    removed something -- a legacy `~/.pi/agent/extensions/probe-research-pi`
    symlink still pointing inside OUR package root. The far more common
    "nothing to migrate" / "left alone, it resolves elsewhere" outcomes are
    not worth repeating on every single install, and folding a migration
    FAILURE in here would misreport the install itself as failed when the
    settings.json write -- the part that actually matters -- succeeded.

    No local checkout is NOT a failure. This used to resolve a package root
    up front and return `reachable=False` when none existed, which is every
    machine without a research-os clone -- so the wizard told each of those
    users "could not find the probe-research-pi package", naming an env var
    and a checkout neither of which they have. `install_package_entry` now
    picks the source itself (`resolve_install_source`: local checkout for a
    plugin developer, the published mirror repo otherwise), so this call site
    just asks for the install and reports what happened.
    """
    result = pi_config.install_package_entry(tracking=tracking)
    if not result.ok:
        return result

    root = pi_config.local_package_root()
    if root is None:
        # Mirror install: `~/.pi/agent/extensions/probe-research-pi` can only
        # ever have pointed inside a local checkout, so with no checkout there
        # is nothing D4 could match -- skip the migration rather than resolve
        # a root that does not exist just to hand it a guaranteed no-op.
        return result

    migration = pi_config.migrate_legacy_symlink(root)
    if migration.detail.startswith("removed legacy symlink"):
        return claude_cli.Result(ok=True, detail=f"{result.detail}; {migration.detail}")
    return result


def _settings_capture_on(source: str) -> bool:
    """A settings-package agent's (pi's) capture is live here: its own
    credential, no killswitch. Decides whether unticking tracking may delete
    the one package both halves share."""
    try:
        return bool(capture_token_sources(source)) and not (tap_plugin_dir(source) / ".disabled").exists()
    except Exception:  # noqa: BLE001 - unknown is "keep the package"
        return True


def _pi_project_override(*, want: bool) -> list[str]:
    """The wizard writes pi's GLOBAL entry; a project entry in this folder wins
    over it (pi's merge rule). Say so instead of editing someone's project file."""
    merged = pi_config.merged_package_entry(cwd=Path.cwd())
    if merged.scope != "project" or not merged.installed:
        return []
    if merged.tracking_off == (not want):
        return []
    project = pi_config.project_settings_path(Path.cwd())
    state = "on" if want is False else "off"
    return [f"! {project} keeps Probe's tracking {state} in this folder (pi lets a project entry win); "
            f"edit or remove its probe-research-pi entry to match."]
