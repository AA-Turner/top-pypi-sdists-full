"""the Probe-owned keys on our entry: daemon profile (skill filter) and the tracking axis."""

from __future__ import annotations
import os
from collections.abc import Mapping

# One of the two non-stdlib imports here (`durable` below is the other), and free:
# claude_cli.py is itself stdlib-only (shutil/subprocess/dataclasses, see its
# own docstring), so importing it adds no dependency weight and, critically,
# no import cycle -- it does not import agent_rules, pi_config, or anything
# else in this package back. It is imported for `Result`, and for the bounded
# way to run a binary (`claude_cli.capture`, `pi_binary_available`'s sniff).
# setup.py's install_plugin/uninstall_plugin already return claude_cli.Result,
# and a later task wires pi's install/remove into the SAME call sites
# (apply_capture, apply_tracking) that already know how to read `.ok` and
# `.detail` off one. Inventing a second, differently-shaped result type here
# would make that wiring a translation layer instead of a drop-in.
from probe.shared.harness.harnesses.claude_code import binary as claude_cli
from probe.shared.harness.harnesses.pi.package_source import (
    PackageRootError,
    _entry_source,
    _our_entry_index,
    _skill_prefix,
    local_package_root,
)
from probe.shared.harness.harnesses.pi.settings import (
    _SettingsRefusal,
    _load_settings,
    _write_settings,
    pi_agent_dir,
    settings_path,
)


# --- The daemon profile ("Who records" = daemon) ------------------------------
#
# Claude Code and Codex get the daemon profile by swapping in a second, lean
# plugin. pi has one package (from one git repo: pi identifies a git package by
# its repo URL), so the profile is the package's settings entry instead:
# narrowed to the daemon profile's skills, which pi honours as a real unload
# (verified on pi 1.0.0: `"skills": ["skills/instrument-code"]` loads exactly
# that one). The extension does the rest at runtime from the profile `probe
# session initialize` reports: no MCP bridge, the guard, the daemon's own
# `probe` and `visualize-progress` skills (their daemon-skills/ copies) and
# `plan-research-review` (all added through `resources_discover`), and the pi
# dialog for the daemon's questions.

#: The package version whose extension runs the daemon profile. Older ones
#: ignore `profile` and would connect the MCP bridge in a daemon session.
DAEMON_MIN_PACKAGE_VERSION = (0, 3, 0)

#: Skills the package's settings entry loads in the daemon profile: the
#: `daemon` profile of agent/skills/profiles.json minus `DAEMON_EXTENSION_SKILLS`.
#: tests/test_pi_daemon_profile.py pins this to profiles.json.
#:
#: NEVER WIDEN IT. The filter is written once, by the wizard, and
#: `_is_daemon_filter` matches it exactly: a longer tuple here would make every
#: machine already on the daemon profile read as the agent profile (doctor,
#: capture teardown), and still never load the new skill there. A skill added to
#: the daemon profile later goes in `DAEMON_EXTENSION_SKILLS` instead.
DAEMON_PACKAGE_SKILLS = ("instrument-code",)

#: Daemon-profile skills the pi EXTENSION adds itself through
#: `resources_discover`, at runtime, so they reach every machine on the profile
#: whatever filter its wizard wrote: `probe` and `visualize-progress` (the
#: daemon's own wording, their daemon-skills/ copies; the package's
#: `skills/<name>` is the agent profile's text) and the ones added after the
#: filter shipped (`DAEMON_ADDED_SKILLS` in the extension's src/profile.ts).
DAEMON_EXTENSION_SKILLS = ("probe", "plan-research-review", "visualize-progress")


def _loads_our_extension(extensions: object) -> bool:
    if not isinstance(extensions, list):
        return True  # no filter: pi loads every extension the package declares
    return any(
        isinstance(p, str) and not p.strip().startswith(("!", "-")) and p.strip().lstrip("+").endswith("index.ts")
        for p in extensions
    )


#: Where `set_profile` keeps the researcher's own `skills` filter while the
#: daemon profile's replaces it, beside it in the same entry (pi ignores a key
#: it does not know; verified on pi 1.0.0 with `pi list`).
AGENT_SKILLS_STASH_KEY = "probeAgentSkills"


def _daemon_filter(source: str) -> list[str]:
    return [_skill_prefix(source) + skill for skill in DAEMON_PACKAGE_SKILLS]


def _is_daemon_filter(skills: object, source: str) -> bool:
    return (
        isinstance(skills, list)
        and all(isinstance(path, str) for path in skills)
        and sorted(path.strip() for path in skills) == sorted(_daemon_filter(source))
    )


#: The settings-entry key that switches Probe's tracking (package skills and
#: the MCP bridge) off while the extension keeps capturing. pi ignores keys it
#: does not know (verified with `pi list`, as for `AGENT_SKILLS_STASH_KEY`).
TRACKING_KEY = "probeTracking"

#: The package version whose extension honours `TRACKING_KEY`. An older one
#: keeps bridging MCP whatever the entry says, so the wizard never writes the
#: flag below this version (`setup._settings_tracking_ready`).
TRACKING_OFF_MIN_PACKAGE_VERSION = (0, 4, 0)


def _entry_for(entry: object, source: str, *, tracking: bool, daemon: bool) -> dict | str:
    """THE one writer of our entry's Probe-owned keys.

    Every profile/tracking change goes through here, so `skills` has one owner:

        tracking  recorder  skills                         probeTracking
        on        agent     the researcher's filter/none   absent
        on        daemon    the daemon filter              absent
        off       either    []                             false

    The researcher's own `skills` filter is kept under `AGENT_SKILLS_STASH_KEY`
    while one of ours replaces it. Which value is ours is read off the entry:
    the daemon filter, or `[]` beside `probeTracking: false`. Anything else in
    `skills` is the researcher's (a filter they changed while in a narrowed
    state stays theirs, and the stash goes). An `extensions` filter that would
    stop our extension loading is dropped whenever we narrow: the extension is
    the capture runtime and the one that enforces the narrowing. An entry left
    with nothing but its source goes back to the plain string it most likely
    was."""
    updated = dict(entry) if isinstance(entry, dict) else {"source": source}
    current = updated.get("skills")
    ours_now = _is_daemon_filter(current, source) or (
        updated.get(TRACKING_KEY) is False and current == []
    )
    stashed = updated.pop(AGENT_SKILLS_STASH_KEY, None)
    researcher = stashed if ours_now else current
    updated.pop(TRACKING_KEY, None)
    updated.pop("skills", None)
    if tracking and not daemon:
        if researcher is not None:
            updated["skills"] = researcher
    else:
        if researcher is not None:
            updated[AGENT_SKILLS_STASH_KEY] = researcher
        if tracking:
            updated["skills"] = _daemon_filter(source)
        else:
            updated["skills"] = []
            updated[TRACKING_KEY] = False
        if not _loads_our_extension(updated.get("extensions")):
            updated.pop("extensions", None)
    return source if set(updated) == {"source"} else updated


def _rewrite_entry(
    env: Mapping[str, str] | None, *, tracking: bool | None, daemon: bool | None, what: str
) -> claude_cli.Result:
    """Apply `_entry_for` to our GLOBAL entry; `None` keeps that axis as it is.

    Refuses an unreadable settings file without writing, like every other
    write here. Project-scope entries are never edited: `merged_package_entry`
    reports when one wins, and the wizard names it instead."""
    active = env if env is not None else os.environ
    agent_dir = pi_agent_dir(active)
    path = settings_path(active)
    try:
        root = local_package_root(active)
        data = _load_settings(path)
    except (_SettingsRefusal, PackageRootError) as exc:
        return claude_cli.Result(ok=False, detail=str(exc))
    index = _our_entry_index(data, root=root, agent_dir=agent_dir)
    if index is None:
        return claude_cli.Result(ok=False, detail=f"probe-research-pi is not installed in {path}")
    packages = list(data["packages"])
    entry = packages[index]
    source = _entry_source(entry) or ""
    tracking_now, daemon_now = _entry_axes(entry, source)
    packages[index] = _entry_for(
        entry,
        source,
        tracking=tracking_now if tracking is None else tracking,
        daemon=daemon_now if daemon is None else daemon,
    )
    if packages[index] == entry:
        return claude_cli.Result(ok=True, detail="no change")
    data["packages"] = packages
    try:
        _write_settings(path, data)
    except _SettingsRefusal as exc:
        return claude_cli.Result(ok=False, detail=str(exc))
    return claude_cli.Result(ok=True, detail=f"pi {what} ({path})")


def _entry_axes(entry: object, source: str) -> tuple[bool, bool]:
    """(tracking, daemon) as the entry records them. A tracking-off entry does
    not say which profile it was on, so daemon reads False there; callers that
    know the recorder pass it explicitly."""
    if not isinstance(entry, dict):
        return True, False
    if entry.get(TRACKING_KEY) is False:
        return False, False
    return True, _is_daemon_filter(entry.get("skills"), source)


def set_profile(daemon: bool, env: Mapping[str, str] | None = None) -> claude_cli.Result:
    """Narrow (daemon) or restore (agent) our entry's skills, keeping tracking
    as the entry has it (`_entry_for` owns the shape)."""
    return _rewrite_entry(env, tracking=None, daemon=daemon,
                          what=f"loads the {'daemon' if daemon else 'agent'} profile")


def set_tracking(on: bool, *, daemon: bool, env: Mapping[str, str] | None = None) -> claude_cli.Result:
    """Switch Probe's tracking (skills + MCP) on or off, keeping the entry, so
    capture keeps running. `daemon` is who records for pi (the caller reads
    `session_marker.recorder`), needed because a tracking-off entry does not
    record the profile it returns to."""
    return _rewrite_entry(env, tracking=on, daemon=daemon,
                          what=f"tracking {'on' if on else 'off'}")


#: `entry_profile`'s answer for an entry whose tracking is off: neither
#: profile's skills load, and the recorder decides what the daemon does.
PROFILE_TRACKING_OFF = "tracking-off"


def entry_profile(env: Mapping[str, str] | None = None) -> str | None:
    """"daemon" when our global entry carries the daemon profile's skills
    filter, "tracking-off" when Probe's tracking is switched off on it,
    "agent" when it is installed with neither, None when not installed."""
    active = env if env is not None else os.environ
    try:
        data = _load_settings(settings_path(active))
        index = _our_entry_index(data, root=local_package_root(active), agent_dir=pi_agent_dir(active))
    except (_SettingsRefusal, PackageRootError):
        return None
    if index is None:
        return None
    entry = data["packages"][index]
    if not isinstance(entry, dict):
        return "agent"
    if entry.get(TRACKING_KEY) is False:
        return PROFILE_TRACKING_OFF
    # Only the daemon profile's exact filter is the daemon: a researcher's own
    # filter is the agent profile, narrowed by them.
    return "daemon" if _is_daemon_filter(entry.get("skills"), _entry_source(entry) or "") else "agent"
