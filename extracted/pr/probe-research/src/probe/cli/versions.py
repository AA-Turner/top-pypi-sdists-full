"""What is installed on THIS machine, and how it compares to the manifest.

WHY THIS IS THE AUTHORITATIVE ANSWER, AND THE SERVER'S IS NOT.

The backend knows what a machine last REPORTED. That is a different fact from
what it is running, and the two diverge in exactly the cases that matter: a
laptop that has not opened Probe in a fortnight reports a fortnight-old version,
and a machine that never authenticates at all -- a self-hosted install, a box
behind a proxy, a researcher who has not paired yet -- reports nothing ever. The
server cannot distinguish "current" from "never heard from" for those, which is
the whole reason its silence was ambiguous in the first place.

This module reads the disk. It is right for every machine including the ones the
server cannot see, and it is why `probe doctor` is the answer to "am I current?"
rather than a dashboard someone has to remember to visit.

WHAT IT CANNOT DETERMINE IS SAID OUT LOUD. `None` for a component's local version
means "not installed, or installed in a place this cannot read" -- never "current".
A caller that renders `None` as a tick reintroduces the bug this file exists to
close, so `Comparison.status` carries UNKNOWN as a first-class value rather than
letting an absent version fall through the current/stale branch.
"""

from __future__ import annotations

import json
import os
import time
from collections.abc import Iterable
from dataclasses import dataclass
from probe._compat import StrEnum
from pathlib import Path

from probe import __version__
from probe.cli import capabilities

#: Plugin ids as Claude Code records them in `installed_plugins.json`. The key
#: there is `<plugin>@<marketplace>`; the marketplace half varies by how the user
#: installed, so entries are matched on the plugin half alone.
_TAP_PLUGIN = "probe-research-tap"
#: The tap's retired standalone id. Still installed on machines that paired before
#: the rename, and still the thing actually capturing their transcripts.
_LEGACY_TAP_PLUGINS = ("prbe-cc-tap-plugin", "prbe-codex-tap-plugin")


class VersionStatus(StrEnum):
    """How one installed component compares to the manifest."""

    CURRENT = "current"
    UPDATE = "update"
    #: Below the manifest's `recommended`: still supported, but KNOWN to
    #: misbehave. The tier between "newer exists" and "we no longer support
    #: this", and the one a breaking release needs -- raising `min` to a
    #: just-published version would mark the whole fleet unsupported, and
    #: UPDATE alone says nothing a user is wrong to ignore.
    NEEDED = "needed"
    REQUIRED = "required"
    #: Local version unreadable, or the manifest has no entry to compare against.
    #: DISTINCT FROM CURRENT ON PURPOSE -- see the module docstring.
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Comparison:
    """One component: what is installed, what is published, and the verdict."""

    kind: str
    installed: str | None
    latest: str | None
    minimum: str | None
    status: VersionStatus
    #: The publisher's own sentence for this component, when the manifest ships
    #: one. Shown INSTEAD of the canned mark for an urgent row: the tier is
    #: always the same shape and what it breaks is different every time, so the
    #: release that introduced the break is the only thing that can say.
    message: str | None = None

    @property
    def behind(self) -> bool:
        return self.status in (
            VersionStatus.UPDATE,
            VersionStatus.NEEDED,
            VersionStatus.REQUIRED,
        )


def _installed_plugins_path() -> Path:
    override = os.environ.get("PROBE_INSTALLED_PLUGINS_JSON")
    if override:
        return Path(override)
    return Path.home() / ".claude" / "plugins" / "installed_plugins.json"


def _plugin_versions() -> dict[str, str]:
    """`{plugin id: version}` from Claude Code's own install ledger.

    The ledger is the right source rather than globbing the version-qualified
    cache directory: several versions of one plugin can sit in that cache at
    once, and picking the highest reports a copy that may never have run.

    Fail-soft to `{}`. A machine driving Probe from Codex or from no agent at all
    has no such file, and that is a normal state, not an error.
    """
    try:
        raw = json.loads(_installed_plugins_path().read_text())
    except Exception:
        return {}
    plugins = raw.get("plugins")
    if not isinstance(plugins, dict):
        return {}
    found: dict[str, str] = {}
    for key, entries in plugins.items():
        if not isinstance(key, str) or not isinstance(entries, list) or not entries:
            continue
        name = key.split("@", 1)[0]
        newest: str | None = None
        for entry in entries:
            if isinstance(entry, dict) and isinstance(entry.get("version"), str):
                newest = entry["version"]
        if newest:
            found[name] = newest
    return found


def _tap_installed_version(source: str | None = None) -> str | None:
    """The tap version that actually RAN, from its own state file.

    `.installed_version` is written by the tap's own SessionStart hook, so it
    names the copy that executed rather than the copy that was downloaded -- and
    it therefore only moves when a session next STARTS. `local_versions` weighs
    it against the ledger for that reason.
    """
    try:
        return (
            (capabilities.tap_plugin_dir(source) / ".installed_version").read_text().strip() or None
        )
    except Exception:
        return None


#: The installed CLI's version, when this process knows it differs from its own:
#: after this process upgraded it, or under npx/uvx, where this process is a
#: temporary copy. The running interpreter keeps its own `__version__` until it
#: exits, so the wizard re-read state after its Update action and still graded
#: the old number: "Update available" right after "CLI upgraded 0.179.2 → 0.179.3".
_installed_cli: str | None = None


def record_installed_cli(version: str | None) -> None:
    """Grade the CLI at `version` from now on, in this process."""
    global _installed_cli
    if version:
        _installed_cli = version


def cli_version() -> str:
    """The installed CLI version, for every surface that prints one.

    One accessor, so `probe doctor`'s "CLI version" row and its Versions block
    cannot show two different numbers after an in-process upgrade.
    """
    return _installed_cli or __version__


def local_versions() -> dict[str, str | None]:
    """Installed version per kind. `None` means unreadable, never current."""
    plugins = _plugin_versions()
    source = capabilities.agent_source()
    tap = _tap_installed_version(source)
    # The ledger is Claude Code's alone. A Codex or pi tap is graded by its own
    # stamp, and without one reads unknown rather than borrowing Claude's number.
    if source == "claude_code":
        # `probe update`'s own reader, not a second parse of the same file: two
        # readers picked different entries on a multi-scope ledger, which put the
        # exact contradiction below straight back.
        from probe.cli import updater

        ledger_tap = updater.installed_tap_version()
        if tap is None:
            tap = ledger_tap or next(
                (plugins[name] for name in (_TAP_PLUGIN, *_LEGACY_TAP_PLUGINS) if name in plugins),
                None,
            )
        else:
            ran, installed = _triplet(tap), _triplet(ledger_tap or "")
            if ran and installed and installed > ran:
                # The ledger is AHEAD of the copy that last ran: an update landed
                # and no Claude Code session has started since. Grading the stale
                # stamp said "Update needed" directly under `probe update`'s
                # "already at the latest", and Update could never clear it -- only
                # a new session rewrites the stamp. Only the tap's own id, never a
                # retired one: the stamp belongs to `probe-research-tap`. And only
                # when both parse, so a dev stamp like 0.9.0.dev1 is never lowered.
                tap = ledger_tap
    cli = cli_version()
    return {
        "cli": cli,
        # The SDK ships inside this same distribution, so it is the same number
        # by construction. Listed anyway: a researcher asking "what am I running"
        # should not have to know which components share a package.
        "sdk": cli,
        # The profile's plugin: `probe-research-daemon` where the daemon records.
        "plugin": plugins.get(capabilities.tracking_plugin_name(source)),
        "tap": tap,
    }


def _pair(manifest: dict, kind: str) -> tuple[str | None, str | None, str | None, str | None]:
    """`(latest, min, recommended, message)` for a kind. `sdk` grades against
    `cli` -- one package.

    `recommended` is optional and absent from every manifest published before it
    existed, so None here must read as "no opinion" rather than as a floor of
    zero -- see `compare`, which skips the tier entirely when it is None.
    """
    entry = manifest.get("cli" if kind == "sdk" else kind)
    if not isinstance(entry, dict):
        return (None, None, None, None)
    latest = entry.get("latest")
    minimum = entry.get("min")
    recommended = entry.get("recommended")
    message = entry.get("message")
    return (
        latest if isinstance(latest, str) else None,
        minimum if isinstance(minimum, str) else None,
        recommended if isinstance(recommended, str) else None,
        _clip_message(message),
    )


#: Cap on manifest prose rendered into a doctor row. Same reasoning as the
#: SessionStart hook's: the manifest is fetched over the network, so a hostile
#: or fat-fingered publish must not be able to paste paragraphs -- or a newline,
#: which would forge an extra row -- into a diagnostic whose rows are its output.
_MESSAGE_CAP = 160


def _clip_message(value: object) -> str | None:
    """One flattened, bounded line of publisher prose, or None if unusable."""
    if not isinstance(value, str) or not value.strip():
        return None
    text = " ".join(value.split())
    if len(text) <= _MESSAGE_CAP:
        return text
    head = text[:_MESSAGE_CAP]
    cut = head.rsplit(" ", 1)[0] or head
    return f"{cut.rstrip(',;:.')}…"


def _triplet(value: str) -> tuple[int, ...] | None:
    """Normalized (major, minor, patch); pre-release and build suffixes ignored."""
    words = str(value).split() if value else []
    # A blank string has no last word; it is unreadable, not an IndexError.
    text = words[-1] if words else ""
    for sep in ("+", "-"):
        text = text.split(sep, 1)[0]
    try:
        parts = [int(p) for p in text.split(".")]
    except ValueError:
        return None
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts[:3])


def compare(manifest: dict, local: dict[str, str | None] | None = None) -> list[Comparison]:
    """Grade every component against the manifest, in a stable display order."""
    installed = local if local is not None else local_versions()
    rows: list[Comparison] = []
    for kind in ("cli", "sdk", "plugin", "tap"):
        have = installed.get(kind)
        latest, minimum, recommended, message = _pair(
            manifest if isinstance(manifest, dict) else {}, kind
        )
        have_t = _triplet(have) if have else None
        latest_t = _triplet(latest) if latest else None
        if have_t is None or latest_t is None:
            status = VersionStatus.UNKNOWN
        else:
            minimum_t = _triplet(minimum) if minimum else None
            recommended_t = _triplet(recommended) if recommended else None
            if minimum_t is not None and have_t < minimum_t:
                status = VersionStatus.REQUIRED
            elif recommended_t is not None and have_t < recommended_t:
                status = VersionStatus.NEEDED
            elif have_t < latest_t:
                status = VersionStatus.UPDATE
            else:
                status = VersionStatus.CURRENT
        rows.append(
            Comparison(
                kind=kind,
                installed=have,
                latest=latest,
                minimum=minimum,
                status=status,
                # Carried only for the tiers that print it, so a message left in
                # the manifest after a fix cannot resurface on a current row.
                message=message
                if status in (VersionStatus.NEEDED, VersionStatus.REQUIRED)
                else None,
            )
        )
    return rows


def render(rows: list[Comparison]) -> list[str]:
    """Human lines for `probe doctor`. Says the good news as well as the bad.

    An entirely current machine still prints a line per component. That is the
    point: "nothing was wrong" and "nothing was checked" produced identical
    output before, and a researcher could not tell which one they were looking at.
    """
    labels = {"cli": "CLI", "sdk": "SDK", "plugin": "plugin", "tap": "transcript tap"}
    marks = {
        VersionStatus.CURRENT: "ok",
        VersionStatus.UPDATE: "update available",
        # Upper-cased like REQUIRED, not sentence-cased like UPDATE: the whole
        # point of the tier is that it reads differently from housekeeping at a
        # glance, in a list where every other line is housekeeping.
        VersionStatus.NEEDED: "UPDATE NEEDED: features may not work correctly",
        VersionStatus.REQUIRED: "UPDATE REQUIRED",
        VersionStatus.UNKNOWN: "not installed / version unreadable",
    }
    lines: list[str] = []
    for row in rows:
        label = labels.get(row.kind, row.kind)
        if row.status is VersionStatus.UNKNOWN:
            lines.append(f"  {label:<24} {marks[row.status]}")
            continue
        # THE SEVERITY LABEL STAYS, the sentence after it is the publisher's.
        # In a four-row list the label is what a reader scans for, so replacing
        # it with prose would cost the one thing this rendering is good at;
        # the message says what the label cannot, which is what broke.
        mark = marks[row.status]
        if row.message and row.status in (VersionStatus.NEEDED, VersionStatus.REQUIRED):
            mark = f"{mark.split(':')[0]}: {row.message}"
        detail = f"{row.installed} ({mark}"
        if row.behind and row.latest:
            detail += f" — latest {row.latest}"
        detail += ")"
        lines.append(f"  {label:<24} {detail}")
    return lines


def overall(rows: Iterable[Comparison]) -> VersionStatus:
    """One verdict for the whole machine, for surfaces with a single line to spend.

    The worst tier any component is in, with UNKNOWN reserved for machines where
    NOTHING could be graded. Letting one unreadable component outrank three good
    ones would report every Codex-only box as unchecked -- it has no Claude plugin
    ledger to read -- while the inverse, an all-unknown machine reading as CURRENT,
    is the exact bug this module exists to prevent. So an unknown row is ignored
    when anything else was gradeable, and decisive when nothing was.
    """
    seen = {row.status for row in rows}
    for status in (VersionStatus.REQUIRED, VersionStatus.NEEDED, VersionStatus.UPDATE):
        if status in seen:
            return status
    return VersionStatus.CURRENT if VersionStatus.CURRENT in seen else VersionStatus.UNKNOWN


def warm_manifest(*, wait_s: float = 2.0) -> None:
    """Make the cached manifest current, if it is not already. Bounded, fail-soft.

    `probe doctor` deliberately never does this and must not start: it is the
    command people run when things are broken, and it has to work offline. The
    WIZARD is the opposite case -- interactive, already behind a spinner, already
    talking to the API to resolve the account -- and its version row is a thing
    the user opened the menu to read.

    Without this the row would be blank on the machines that need it most. The
    only other things that refresh the cache are the wizard's one server call
    (`capabilities.fetch_device_state`) and the detached refresher in
    `main._version_notice`, and that is gated on auto-update being ENABLED, so a
    box with auto-update off never fetches a manifest at all and could only ever
    be told "not checked yet" -- while being exactly the box nothing else is
    keeping current.

    Single-flight, so this never races the detached refresher into a second
    request for the same 150-byte document. When that refresher holds the claim we
    wait for it ONLY if we have nothing to show: a stale manifest is a perfectly
    good thing to render while a fresh one lands, and is what the age qualifier
    beside the verdict is for.
    """
    from probe import version_policy
    from probe.sdk.tls import ssl_context

    try:
        manifest, fetched_at, ok = version_policy.read_cache()
        if version_policy.cache_is_fresh(fetched_at, ok):
            return
        if version_policy.claim_refresh():
            try:
                version_policy.refresh(context=ssl_context())
            finally:
                version_policy.release_refresh()
            return
        if manifest is not None:
            return
        deadline = time.monotonic() + wait_s
        while time.monotonic() < deadline:
            time.sleep(0.2)
            if version_policy.read_cache()[0] is not None:
                return
    except Exception:  # noqa: BLE001 - a version row must never break the menu
        return
