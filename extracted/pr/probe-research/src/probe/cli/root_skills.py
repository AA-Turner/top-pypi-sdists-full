"""The CLI's half of the root-skills install: which folder, and from where.

The copying itself is `probe.root_skills_core`, stdlib-only because the
session-start hook runs it under the system python (see that module). This half
knows the one thing only the CLI knows: where each harness keeps its skills.

WHAT TO INSTALL IS THE PLUGIN'S OWN `agent-skills/`, not a list read from
somewhere else. The two install profiles ARE two plugins -- the full one carries
eight skills, the lean daemon one carries four -- so the folder that is
installed answers "which profile" by itself. A second list here could disagree
with the plugin on the machine, and the way it would disagree is the dangerous
one: `track-work` left in place on the daemon profile has the agent recording
inline while the daemon records the same session.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from probe import root_skills_core as core
from probe.harness import get_registry


def skills_root(source: str, env: "dict[str, str] | None" = None) -> Path | None:
    """The agent's own skills folder, or None where the harness has none.

    Resolved through the harness row, so `CLAUDE_CONFIG_DIR` moves it -- the
    same rule `agent_rules.memory_path` follows, because a machine that moved
    its config must not get files written to the real home.
    """
    from probe.harness.registry import CAPABILITY_ROOT_SKILLS

    harness = get_registry().find(source)
    if harness is None or not harness.can(CAPABILITY_ROOT_SKILLS):
        return None
    home = harness.home_dir(env)
    return None if home is None else home / "skills"


def installed_plugin_root(prefer: "str | None" = None, env: "dict[str, str] | None" = None) -> Path | None:
    """Where the installed Probe plugin lives, from Claude Code's install ledger.

    `prefer` IS REQUIRED AT EVERY REAL CALL SITE, and the reason is the whole
    point of this module. A Who-records switch installs the new plugin, applies
    the skills, and only THEN uninstalls the old one, so in between the ledger
    holds BOTH Probe plugins -- in install order, which puts the profile being
    LEFT first. Picking the first match installed the old profile's skills:
    switching to the daemon landed `track-work`, telling the agent to record
    inline while the daemon recorded the same session. That is the exact failure
    this module exists to prevent, and it reproduced.

    The ledger rather than a glob of the version-qualified cache: several
    versions of one plugin sit in that cache at once (`0.127.1`, `0.128.0`,
    `0.129.0` on this box), and the highest may be one that never ran. The
    ledger names the copy Claude Code loads. Fail-soft to None -- a machine
    driving Probe from Codex has no such file, which is normal.
    """
    from probe.cli.capabilities import DAEMON_PLUGIN_NAME, TRACKING_PLUGIN_NAME, claude_plugin_ledger

    # The hooks' `dispatch._ledger` reads the same place.
    ledger = claude_plugin_ledger(env)
    try:
        raw = json.loads(ledger.read_text(encoding="utf-8"))
        plugins = raw["plugins"]
    except (OSError, ValueError, KeyError, TypeError):
        return None
    if not isinstance(plugins, dict):
        return None
    found: dict[str, Path] = {}
    for key, entries in plugins.items():
        if not isinstance(key, str):
            continue
        name = key.split("@", 1)[0]
        if name not in (TRACKING_PLUGIN_NAME, DAEMON_PLUGIN_NAME) or name in found:
            continue
        if not isinstance(entries, list):
            continue
        # One entry per key in every real ledger on this box; a `user`-scope
        # entry wins if a machine ever carries several, because that is the
        # scope the wizard installs into.
        ordered = sorted(
            (e for e in entries if isinstance(e, dict)),
            key=lambda e: e.get("scope") != "user",
        )
        for entry in ordered:
            path = entry.get("installPath")
            if isinstance(path, str) and (Path(path) / core.PLUGIN_SKILLS_DIR).is_dir():
                found[name] = Path(path)
                break
    if prefer and prefer in found:
        return found[prefer]
    if prefer and found:
        # The asked-for plugin is not in the ledger yet (its install is what
        # queued this) -- installing the OTHER profile's skills is the failure
        # above, so do nothing and let the session-start hook settle it.
        return None
    return next(iter(found.values()), None)


def apply(
    source: str,
    plugin_root: "Path | None",
    env: "dict[str, str] | None" = None,
    prefer: "str | None" = None,
) -> list[str]:
    """Install/refresh the installed plugin's skills for `source`.

    `plugin_root` None means the installed plugin was not found, so there is
    nothing to copy FROM. Reported, never guessed: the alternative is writing a
    copy out of the wheel and calling it the plugin's.

    `prefer`: the plugin `plugin_root` was looked up as (`installed_plugin_root`).
    The lookup is made again once the copy lock is held, and a `plugin_root` the
    ledger has moved past by then writes nothing: an update that landed in
    between must not have its newer text overwritten with this one's.
    """
    root = skills_root(source, env)
    if root is None:
        return []
    if plugin_root is None:
        # No install ledger, or no plugin carrying `agent-skills/`: an older
        # plugin beside a newer CLI, or a machine that drives Probe without one.
        # Silent on purpose -- the wizard already reports what it installed, and
        # the SessionStart hook installs these the moment a plugin arrives.
        return []
    still_installed = None
    if prefer is not None:
        here = os.path.realpath(plugin_root)

        def still_installed() -> bool:
            now = installed_plugin_root(prefer, env)
            return now is not None and os.path.realpath(now) == here

    report = core.apply(root, plugin_root, core.slugs(plugin_root), still_installed=still_installed)
    # No `!`: the wizard reads that prefix as a failed step (`_FAILURE_MARKERS`),
    # and "you already have a skill called probe" is a statement, not a fault.
    lines = list(report["notes"])
    for kind in ("installed", "refreshed", "removed"):
        if report[kind]:
            # A count and the folder, not every skill's name: the list was the
            # widest line on the wizard's screens (and its title on one).
            count = len(report[kind])
            lines.append(f"{kind.capitalize()} {count} skill{'' if count == 1 else 's'} in {_shown(root)}.")
    return lines


def _shown(path) -> str:
    """`path` with the home folder written `~`."""
    home = os.path.expanduser("~")
    text = str(path)
    return "~" + text[len(home):] if home and text.startswith(home + os.sep) else text


def refresh(source: str, env: "dict[str, str] | None" = None) -> list[str]:
    """After a plugin update: the agent's skills folder brought to the plugin
    now installed for `source`'s profile.

    `probe update` and the Probe service's updater call this right after the
    plugin moves. Claude Code re-reads its skills folder when a file there
    changes, so every session already open reads the new text on its next skill
    call; before this, only a session START refreshed the copies, and a machine
    with one long-lived session kept the old text for days. Fail-open, as
    the wizard's install is: a skills folder that cannot be written never fails
    the update."""
    from probe.cli.capabilities import tracking_plugin_name

    try:
        plugin = tracking_plugin_name(source)
        return apply(source, installed_plugin_root(plugin, env), env, prefer=plugin)
    except Exception as exc:  # noqa: BLE001 - never fail the update after its plugin step
        return [f"! could not refresh Probe's skills: {exc}"]


def remove(source: str, env: "dict[str, str] | None" = None) -> list[str]:
    """Every Probe skill out of the agent's folder (Uninstall). Ours only."""
    root = skills_root(source, env)
    if root is None:
        return []
    gone = core.prune(root, keep=frozenset())
    return [f"Removed {len(gone)} Probe skill{'' if len(gone) == 1 else 's'} from {_shown(root)}."] if gone else []
