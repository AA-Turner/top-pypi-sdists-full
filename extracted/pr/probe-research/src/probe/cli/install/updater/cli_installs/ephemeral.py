"""an ephemeral uvx/pipx run: the update is a persistent install brought up to date from it (CliInstallMethod for Method.EPHEMERAL)."""

from __future__ import annotations

from probe import __version__
# `update_report` is imported HERE, at the top, for the same reason updater.py
# imports its whole call graph eagerly (H8): it runs after `uv tool upgrade` has
# replaced the installed tree, when a first import would read the new files.
from probe.cli.install import updater
from probe.shared.updates import updates as versions


def _update_persistent_copy(cli_target: str | None, lines: list[str]) -> updater.CliResult | None:
    """Bring the persistent install up to date from a temporary (npx/uvx) run.

    This environment is discarded on exit, so there is nothing here to upgrade:
    the persistent install is what matters. Each outcome is said outright. This
    used to print "upgrading your installed copy instead" and then nothing,
    because bootstrap has no message for "already current", which read as the
    upgrade having silently failed.

    None means nothing needed doing; otherwise the outcome to record.
    """
    from probe.cli.install import bootstrap

    from probe.cli.install import install as install_pipeline

    # Finishes an uninstall that stopped halfway only for an update a person asked for.
    boot = bootstrap.ensure_persistent_install(target=cli_target,
                                               finish_uninstall=install_pipeline.update_may_finish())
    if boot.already_persistent:
        # Bootstrap proves only that the installed copy is at least THIS one, and
        # a uvx/pipx cache can serve a stale copy: compare with the latest too.
        installed = bootstrap.installed_version() or __version__
        if not updater.is_newer(cli_target, installed):
            lines.append(
                "  running from a temporary environment — your installed copy is "
                f"already {installed}, nothing to upgrade"
            )
            versions.record_installed_cli(installed)
            return None
        lines.append(
            "  running from a temporary environment — upgrading your installed copy "
            f"({installed} → {cli_target})"
        )
        # The version itself, never `@latest`: the one installer puts a known
        # version beside the running one (`install_pipeline`).
        boot = bootstrap.install_persistent(f"{bootstrap.INSTALL_SPEC}=={cli_target}")
    else:
        lines.append("  running from a temporary environment — installing a permanent copy")
    # Installer output, shown and (on failure) stored: scrubbed once for both.
    said = updater.clean_reason(boot.message) if boot.message else ""
    if said:
        lines.append(f"  {said}")
    if not boot.installed or getattr(boot, "waiting", False):
        # A failed install was recorded as a success: `probe doctor` said
        # "success -> CLI <latest>" and `probe update` exited 0. One that
        # waits for a quiet machine to switch over is not done either.
        return updater.CliResult(True, False, False, __version__, None, said)
    after = bootstrap.installed_version()
    versions.record_installed_cli(after)
    if not after:
        message = "installed, but no `probe` could be found to confirm its version"
    elif updater.is_newer(cli_target, after):
        message = f"the installed copy is still {after} after installing {cli_target}"
    else:
        return updater.CliResult(True, True, True, __version__, after, "")
    # On screen too: "Installed `probe`" alone read as the upgrade landing.
    lines.append(f"  {message}")
    return updater.CliResult(True, False, True, __version__, after, message)
