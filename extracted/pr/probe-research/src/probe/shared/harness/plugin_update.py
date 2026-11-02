"""the update half of the PluginInstaller facet every harness implements: the marketplace and tracking plugin id, version order, PluginResult, Probe plugins under ids an update does not move, a failed command as one safe line (a Mac's blocked git named with its fix)."""

from __future__ import annotations
import re
from dataclasses import dataclass
from probe.shared.harness.harnesses.claude_code import binary as claude_cli
from probe.cli.wizard.state.state import (
    DAEMON_PLUGIN_NAME,
    TAP_PLUGIN_NAME,
    TRACKING_PLUGIN_NAME)
from probe.cli.wizard.state.agent_identity import tracking_plugin_name
from probe.shared.updates.updates import _LEGACY_TAP_PLUGINS
from probe.sdk.redaction import scrub_text

# Resolved once, at import (H8): `is_newer` runs AFTER the tree is replaced, and a
# deferred `import packaging` there could fail; loading it now keeps it in memory.
try:
    from packaging.version import Version as _Version  # type: ignore
except Exception:  # pragma: no cover - packaging is a transitive dep, usually present
    _Version = None
PLUGIN_ID = "probe-research@research-os-agent"
# Imported, NOT redefined: capabilities.py already owns this identity and
# actions.py/capture.py use it from there. A second literal here would be a
# second source of truth for the same plugin — the exact thing that lets one
# copy drift after a rename. (The PLUGIN_ID literal above predates this and
# duplicates capabilities.PLUGIN_ID; left alone rather than silently widened.)
#
# The tap ships from the same marketplace as a SEPARATE plugin, so
# `claude plugin update probe-research@…` never touched it. Leaving it out made
# `probe update` a command that reports success while the component whose
# staleness is invisible (a stale tap captures nothing and says nothing) stays
# behind. Updated alongside, and `claude` failing on it is NOT fatal: `probe
# capture off --uninstall` removes the tap while leaving the CLI and plugin in
# place, so "not installed" is a SUPPORTED state that `claude plugin update`
# reports as an error. What IS a failure is an installed tap still behind the
# manifest after the run: that one used to pass in silence (`tap_verdict`).
MARKETPLACE = "research-os-agent"
MARKETPLACE_REPO = "prbe-ai/research-os-agent"


# -- version compare + manifest ---------------------------------------------
def _triplet(v: str):
    if not v:
        return None
    v = str(v).strip().split()[-1]
    for sep in ("+", "-"):
        v = v.split(sep, 1)[0]
    try:
        nums = [int(p) for p in v.split(".")]
    except ValueError:
        return None
    while len(nums) < 3:
        nums.append(0)
    return tuple(nums[:3])


def is_newer(candidate: str | None, base: str | None) -> bool:
    """True iff `candidate` is strictly newer than `base`."""
    if not candidate or not base:
        return False
    if _Version is not None:
        try:
            return _Version(str(candidate)) > _Version(str(base))
        except Exception:
            pass
    c, b = _triplet(candidate), _triplet(base)
    return bool(c and b and c > b)


def tracking_plugin_id(source: str = "claude_code") -> str:
    """`PLUGIN_ID`, or the lean `probe-research-daemon@…` for an agent whose
    "Who records" is the daemon: an update must move the plugin the profile
    installed, never put the other one back."""
    return f"{tracking_plugin_name(source)}@{MARKETPLACE}"


#: Probe plugin names an update can meet. A ledger entry under one of these
#: names but NOT under `MARKETPLACE`, or under a retired name, is a copy no
#: `claude plugin update <name>@research-os-agent` will ever move.
_PROBE_PLUGIN_NAMES = (TRACKING_PLUGIN_NAME, DAEMON_PLUGIN_NAME, TAP_PLUGIN_NAME)

#: The shape the server accepts for a reported plugin id. A ledger key outside it
#: (an uppercase marketplace, a local path) is left out of the report rather than
#: refusing the whole report over it.
_REPORTABLE_PLUGIN_ID = re.compile(
    r"^(?:probe|prbe)-[a-z0-9-]{1,60}(?:@[a-z0-9][a-z0-9._-]{0,63})?$"
)


def legacy_plugin_ids(names: list[str] | None = None) -> tuple[str, ...]:
    """Probe plugins installed under an id an update does not move.

    Two kinds: a RETIRED name (`prbe-cc-tap-plugin`, `prbe-codex-tap-plugin`,
    the tap's ids before the rename), and a current name from ANOTHER
    marketplace. Either one can be the copy actually running -- and capturing --
    on a machine where the update reports the tap "not installed".

    Observation only: nothing here migrates them. `names` is Codex's installed
    list (bare names); without it, Claude Code's ledger is read.
    """
    found: list[str] = []
    for key in _ledger_ids() if names is None else names:
        name, _, marketplace = key.partition("@")
        retired = name in _LEGACY_TAP_PLUGINS
        elsewhere = name in _PROBE_PLUGIN_NAMES and bool(marketplace) and marketplace != MARKETPLACE
        if (retired or elsewhere) and _REPORTABLE_PLUGIN_ID.match(key):
            found.append(key)
    return tuple(dict.fromkeys(found))[:8]


def legacy_tap_ids(ids: tuple[str, ...]) -> tuple[str, ...]:
    """The tap among `legacy_plugin_ids`: a retired tap name, or the tap's own
    name from another marketplace."""
    return tuple(
        key for key in ids if key.partition("@")[0] in (*_LEGACY_TAP_PLUGINS, TAP_PLUGIN_NAME)
    )


@dataclass
class PluginResult:
    attempted: bool
    confirmed: bool  # plugin is at/past the target — trusted, NOT from claude's exit code
    changed: bool  # the version actually moved this run (vs already-current)
    before: str | None
    after: str | None
    message: str
    # The transcript tap, read before and after the same run. None after means
    # not installed, a supported state (`probe capture off --uninstall`); see
    # `tap_verdict` for how the pair reads against the manifest.
    tap_before: str | None = None
    tap_after: str | None = None
    # WHY the tap did not move, when it did not: the failed command and what it
    # said (`_failed`; the marketplace refresh's own when that failed first), or
    # the in-session no-op the plugin's own branch names. Empty when it moved.
    tap_detail: str = ""
    # Git itself cannot run on this machine (`git_blocker`), so the manual
    # commands would fail the same way and `perform_update` leaves them off.
    # The fix is already in `message` or `tap_detail`, whichever is shown.
    git_blocked: bool = False
    # OBSERVATIONS, never inputs to what this run installs: they say how it
    # ended, for the server's update report (`update_report`) and for whether
    # it failed (`nothing_installed`). Each separates a cause the message alone
    # could only say in prose:
    #: the coding agent's own CLI is not on this process's PATH -- the
    #: detached updater's PATH, not the user's shell.
    missing_binary: bool = False
    #: the marketplace refresh failed, so nothing new could be installed.
    refresh_failed: bool = False
    #: a refresh, update or install command did not complete.
    command_failed: bool = False
    #: the agent's own list of installed plugins could not be read, before or
    #: after the run: nothing listed is then not nothing installed.
    list_unreadable: bool = False
    #: Probe plugins installed under an id this update does not move
    #: (`legacy_plugin_ids`).
    legacy_ids: tuple[str, ...] = ()
    #: The tap version each live capture daemon of this agent still runs, for
    #: every one older than `tap_after` (`stale_tap_daemons`): sessions that
    #: started before the tap was updated. Set by `perform_update`.
    tap_running_stale: tuple[str, ...] = ()
    #: Open sessions follow this update with no restart
    #: (`follows_without_restart`). Set by `perform_update`.
    follows: bool = False


#: The tap's counterpart of the plugin's "returned success but did not advance".
TAP_NOOP = (
    "`claude` returned success but the tap version did not advance "
    "(it may have run inside a Claude Code session, which no-ops)"
)
CODEX_TAP_NOOP = "the Codex reinstall returned success but the tap version did not advance"


def listed_version(listing: str | None, name: str) -> str | None:
    """`name`'s version out of Codex/Kimi's `a=1.0, b=2.0` listing; a bare
    version (Claude's) passes through."""
    if not listing:
        return None
    if "=" not in listing:
        return listing
    for part in listing.split(","):
        key, _, value = part.strip().partition("=")
        if key == name:
            return value or None
    return None


def nothing_installed(result: PluginResult, source: str) -> bool:
    """True when an attempted run found none of Probe's plugins in `source`'s
    agent -- neither the tracking plugin nor the tap, before the run or after
    it, by a list it could read. The update had nothing to move, so whatever its
    commands said (a `claude plugin update` of a plugin that is not there fails,
    as does a refresh of a marketplace never added), it is NOT a failed update:
    the same reading as an agent that is not on PATH at all.

    THE ONE RULE for both readings of a run: whether the plugin half failed
    (`upgrading._perform_update`'s `plugin_ok`, the local record and the
    report's outcome) and what the report's plugin component says
    (`update_report.plugin_component`, `not_installed`). They used to disagree:
    a machine with Claude Code or Codex but no Probe plugin in it reported a
    failed update on every session start, with nothing in the report failing.
    """
    if not result.attempted or result.confirmed or result.list_unreadable:
        return False
    name = tracking_plugin_name(source)
    return not (
        listed_version(result.before, name)
        or listed_version(result.after, name)
        or result.tap_before
        or result.tap_after
    )


_REASON_MAX = 500
#: Codex opens with "WARNING: proceeding, even though we could not create PATH
#: aliases" on some machines, whatever the actual failure was.
_NOISE_PREFIX = "WARNING:"
#: Complete CSI (colour) and OSC sequences. Removed whole: dropping only the ESC
#: byte leaves `[31m` glued to the next word, which hides it from the scrubber.
_TERMINAL_SEQUENCE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]|\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)")


#: The interactive form, not `-license accept`: `probe doctor` replays this
#: inside agent sessions, and accepting Apple's license is the person's call.
_LICENSE_FIX = (
    "git on this Mac is blocked until the Xcode license is accepted. "
    "Run `sudo xcodebuild -license` in a terminal and agree to it, then try again."
)
#: Never installed or removed by an OS upgrade (`--install`), or pointing at
#: an Xcode that was moved or deleted (`--reset`).
_TOOLS_FIX = (
    "git on this Mac cannot find the Xcode command line tools. Run "
    "`xcode-select --install`, or `sudo xcode-select --reset` if they are already "
    "installed, then try again."
)
#: Machine problems that stop git itself, and so every marketplace refresh,
#: before `claude` or `codex` get anywhere: macOS runs `git` through an Xcode
#: shim that refuses until its license is accepted and its tools are in place.
#: Both CLIs pass that on as a paragraph that buries the one command that fixes
#: it, and the manual commands printed after a failure would hit the same wall.
#: Keyed on lowercased fragments of Apple's own sentences, which it rewords:
#: "You have not agreed to the Xcode license agreements", "... to the Xcode
#: and Apple SDKs license", "Agreeing to the Xcode/iOS license requires admin
#: privileges", "Agreeing to the Xcode and Apple SDKs license requires ...".
_GIT_BLOCKERS = {
    "xcodebuild -license": _LICENSE_FIX,
    "not agreed to the xcode": _LICENSE_FIX,
    "xcode and apple sdks license": _LICENSE_FIX,
    "xcode/ios license": _LICENSE_FIX,
    # "invalid active developer path (…)", "active developer path (…) does not
    # exist", and the shim on a Mac that never had them.
    "active developer path": _TOOLS_FIX,
    "no developer tools were found": _TOOLS_FIX,
}


def git_blocker(text: str | None) -> str:
    """The fix for a machine problem that stopped git, or "" for any other failure.

    A line carrying what the git SERVER sent (`remote: …` wherever a CLI
    wrapped it, or git's own `fatal: remote error: …` for an ERR packet) is
    never read: a server quoting Apple's wording must not stand in for the
    real error, which this replaces.
    """
    for line in _TERMINAL_SEQUENCE.sub("", text or "").lower().splitlines():
        if "remote:" in line or "remote error:" in line:
            continue
        for key, fix in _GIT_BLOCKERS.items():
            if key in line:
                return fix
    return ""


def _failed(result: claude_cli.Result) -> str:
    """Which command failed and everything it said about why, on one line.

    A known machine problem is said as its fix instead. The raw output is
    matched, not the cleaned reason, which can lose its middle.
    """
    fix = git_blocker(result.detail)
    if fix:
        return f"not updated: {fix}"
    return f"`{result.command}` did not complete: {clean_reason(result.detail)}"


def clean_reason(text: str | None) -> str:
    """A child's output as one line that is safe to print, store and replay.

    Printing only "did not complete" left a researcher with nothing to act on
    and nothing to report: the child's own error was captured and dropped, and
    `probe doctor` recorded the same empty sentence.

    NOT the last line. Codex puts the reason first and ends on a bare "Error: 1
    upgrade failure(s) occurred."; Claude splits one error over its own summary
    and git's `fatal:` line. So every line is kept, bar Codex's WARNING noise
    (unless that is all there is), and an over-long one loses its MIDDLE: the
    deciding line can be either end.

    It is printed, stored in the update record and replayed by `probe doctor`,
    which agents run inside captured sessions. So credentials in a git URL and
    home paths are scrubbed from the RAW text first (the scanner recognises a
    token by what surrounds it, and a colour code glued on defeats that), then
    terminal sequences and control characters go, then it is scrubbed again in
    case removing them joined a token back together. The scrubber raises on
    input it cannot bound; that withholds the text rather than crashing the
    update before it records its outcome.
    """
    try:
        text = _TERMINAL_SEQUENCE.sub("", scrub_text(text or ""))
        lines = [
            "".join(ch for ch in line.replace("\t", " ") if ch.isprintable()).strip()
            for line in text.splitlines()
        ]
        lines = [line for line in lines if line]
        lines = [line for line in lines if not line.startswith(_NOISE_PREFIX)] or lines
        reason = scrub_text(" · ".join(lines))
    except Exception:  # noqa: BLE001 - see the docstring: withhold, never crash
        return "output withheld: it could not be scrubbed"
    if not reason:
        return "no output"
    if len(reason) > _REASON_MAX:
        keep = (_REASON_MAX - 3) // 2
        reason = f"{reason[:keep]} … {reason[-keep:]}"
    return reason
from probe.shared.harness.harnesses.claude_code.plugins import _ledger_ids  # noqa: E402 -- pieces need each other; the front door loads this one first
