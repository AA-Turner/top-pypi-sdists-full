"""Codex's plugin update: refresh and re-add both plugins, verify the installed list, approve hooks after."""

from __future__ import annotations
import json
import threading
import shutil
from probe.shared.harness import plugins as plugin_cli
from probe.cli.wizard.state.agent_identity import tracking_plugin_name
#: Codex's `marketplace upgrade` refusal for a name with no config entry.
_CODEX_NOT_CONFIGURED = "is not configured as a git marketplace"


#: Why this thread's last `_codex_plugin_versions` read nothing, for the
#: update's failure line ("" when it read the list).
_codex_list = threading.local()


def _codex_plugin_versions(_codex: str | None = None) -> dict[str, str] | None:
    """Codex's installed plugins, `{name: version}`. None when the list could
    not be read (the command failed, or printed something that is not its JSON
    object): that is not an empty list, and `nothing_installed` must not read
    it as one. Why it could not is `_codex_list.problem`."""
    _codex_list.problem = ""
    result = plugin_cli.list_plugins(plugin_cli.CODEX)
    if not result.ok:
        _codex_list.problem = clean_reason(result.detail or "it failed with no output")
        return None
    try:
        body = json.loads(result.detail)
    except ValueError:
        _codex_list.problem = f"it printed something that is not JSON: {clean_reason(result.detail)[:120]!r}"
        return None
    if not isinstance(body, dict):
        _codex_list.problem = "it printed JSON that is not an object"
        return None
    return {
        row["name"]: row["version"]
        for row in body.get("installed") or []
        if isinstance(row, dict)
        and isinstance(row.get("name"), str)
        and isinstance(row.get("version"), str)
    }


def _codex_versions_on_disk() -> dict[str, str] | None:
    """`codex_config.installed_plugin_versions` for Probe's marketplace; None
    when it cannot be read."""
    from probe.shared.harness.harnesses.codex import config as codex_config

    try:
        return codex_config.installed_plugin_versions(MARKETPLACE)
    except Exception:  # noqa: BLE001 - a second opinion that cannot answer is no answer
        return None


def _listed_summary(versions: dict[str, str]) -> str:
    """How many plugins a Codex list read, naming Probe's."""
    probe = sorted(name for name in versions if name.startswith("probe-"))
    named = f": {', '.join(f'{name}={versions[name]}' for name in probe)}" if probe else ""
    return f"{len(versions)} plugin{'' if len(versions) == 1 else 's'}{named}"


def update_codex_plugins() -> PluginResult:
    """Refresh and re-add both Codex plugins, then verify the installed list.

    Codex has no separate ``plugin update`` command. Re-adding an installed
    plugin is its idempotent reinstall path and moves it to the refreshed
    marketplace snapshot without first removing the working copy.
    """
    codex = shutil.which("codex")
    if not codex:
        return PluginResult(
            False, False, False, None, None, "`codex` not found on PATH (skipping plugin update)",
            missing_binary=True,
        )
    names = (tracking_plugin_name("codex"), "probe-research-tap")
    listed_before = _codex_plugin_versions(codex)
    before_versions = listed_before if listed_before is not None else _codex_versions_on_disk() or {}
    failed_run = None
    result = plugin_cli.refresh_marketplace(plugin_cli.CODEX, MARKETPLACE)
    if not result.ok and _CODEX_NOT_CONFIGURED in (result.detail or "").lower():
        # The config entry is gone (a hand-edited or deleted config.toml),
        # so `upgrade` can never succeed again. Re-add it -- which also clears
        # a stale checkout left behind -- and refresh once more.
        added = plugin_cli.add_marketplace(plugin_cli.CODEX, MARKETPLACE_REPO, name=MARKETPLACE)
        result = plugin_cli.refresh_marketplace(plugin_cli.CODEX, MARKETPLACE) if added.ok else added
    refresh_failed = not result.ok
    if not result.ok:
        failed_run = result
    for name in names:
        if failed_run is not None:
            break
        result = plugin_cli.install(plugin_cli.CODEX, f"{name}@{MARKETPLACE}")
        if not result.ok:
            failed_run = result
    failure = _failed(failed_run) if failed_run is not None else ""
    listed_after = _codex_plugin_versions(codex)
    list_problem = getattr(_codex_list, "problem", "")
    after_versions = listed_after or {}
    read_from_files = False
    if listed_after is None and not failure:
        # The list could not answer (a timeout, on a Mac): Codex's own files
        # say what it installed (`codex_config.installed_plugin_versions`).
        on_disk = _codex_versions_on_disk()
        if on_disk and all(on_disk.get(name) for name in names):
            after_versions, read_from_files = on_disk, True
    missing = [name for name in names if not after_versions.get(name)]
    confirmed = not failure and not missing
    changed = confirmed and any(
        before_versions.get(name) != after_versions.get(name) for name in names
    )
    before = (
        ", ".join(f"{name}={version}" for name, version in sorted(before_versions.items())) or None
    )
    # Unconfirmed, still what IS listed: a first install that added the
    # tracking plugin and then failed on the tap left Probe in Codex, and
    # reading None here made that "nothing installed" (`nothing_installed`).
    after = (
        ", ".join(f"{name}={after_versions.get(name)}" for name in names)
        if confirmed
        else ", ".join(f"{name}={after_versions[name]}" for name in names if after_versions.get(name))
        or None
    )
    tap_before = before_versions.get("probe-research-tap")
    tap_after = after_versions.get("probe-research-tap")
    tap = {
        "tap_before": tap_before,
        "tap_after": tap_after,
        "tap_detail": failure
        or ("" if is_newer(tap_after, tap_before) else CODEX_TAP_NOOP),
        "git_blocked": failed_run is not None and bool(git_blocker(failed_run.detail)),
        "refresh_failed": refresh_failed,
        "command_failed": failed_run is not None,
        "list_unreadable": listed_before is None or listed_after is None,
        "legacy_ids": legacy_plugin_ids(sorted({*before_versions, *after_versions})),
    }
    if confirmed:
        message = f"Codex plugins {'updated' if changed else 'verified'} ({after})"
        if read_from_files:
            message += f"; read from Codex's plugin files (`codex plugin list --json`: {list_problem})"
        message += approve_codex_hooks_note()
        return PluginResult(True, True, changed, before, after, message, **tap)
    return PluginResult(
        True,
        False,
        False,
        before,
        after,
        # Not "does not show": the list may be the thing that failed
        # (`list_unreadable` says which; the sentence is true either way).
        failure
        or (
            f"could not confirm {' or '.join(missing)}: `codex plugin list --json` could not be read "
            f"after reinstalling ({problem})"
            if listed_after is None and (problem := list_problem)
            else f"could not confirm {' or '.join(missing)} in `codex plugin list --json` after reinstalling"
            # What it does list: none at all is a list Probe could not parse.
            f" (it lists {_listed_summary(after_versions)})"
        ),
        **tap,
    )


def approve_codex_hooks_note() -> str:
    """Approve Probe's hooks in Codex after an update, or one a live run deferred
    (`upgrading._update_prelude`), and say so. Codex skips an entry whose text
    changed until it is approved again, and a machine set up before the wizard
    approved them has never had them approved. Empty where Codex holds no copy of
    Probe's plugins, when nothing waited, or when Codex could not be asked
    (status and doctor still say). Never raises."""
    from probe.shared.harness.harnesses.codex import hooks as codex_hooks

    try:
        if not codex_hooks.installed_copies():
            return ""
        outcome = codex_hooks.approve()
    except Exception:  # noqa: BLE001 - approve never raises; an update never fails on it either way
        return ""
    if outcome is None:
        return ""
    count = len(outcome.approved)
    said = f"; approved {count} Probe hook{'s' if count != 1 else ''} in Codex" if count else ""
    if not outcome.done:
        said += f"; Probe's hooks still wait for approval in Codex ({outcome.error or 'a Probe hook still waits'}): type /hooks there"
    return said


def manual_codex_plugin_commands() -> str:
    return (
        f"codex plugin marketplace upgrade {MARKETPLACE}\n"
        f"codex plugin add {tracking_plugin_id('codex')}\n"
        f"codex plugin add probe-research-tap@{MARKETPLACE}"
    )
from probe.shared.harness.plugin_update import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    CODEX_TAP_NOOP,
    MARKETPLACE,
    MARKETPLACE_REPO,
    PluginResult,
    _failed,
    clean_reason,
    git_blocker,
    is_newer,
    legacy_plugin_ids,
    tracking_plugin_id,
)
