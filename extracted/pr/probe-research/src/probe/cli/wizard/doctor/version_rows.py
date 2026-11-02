"""the Versions block and the warning when the transcript tap is behind."""

from __future__ import annotations
from probe.cli.wizard.state.state import Capabilities


def tap_behind_warning(rows, source: str | None = None, plugin: str | None = None) -> str | None:
    """A warning when the transcript tap is behind the manifest's `tap.latest`.

    The Versions block already grades the tap, but as one row among four; a tap
    left behind by `probe update` went unnoticed exactly that way, while it is
    the component whose staleness costs captured sessions. So it is repeated
    under Warnings, with the way out.

    What it says about sessions already open is what the update will do to
    them (`updater.follows_without_restart`): where they follow an update (the
    prompt hook hands an old watcher to the Probe service, which records on the
    newest installed tap), they move with no restart; only elsewhere does a
    session keep the old copy until it restarts. It said "until it restarts"
    everywhere, and on every machine the service had already moved. `plugin`:
    the agent's installed Probe plugin (None when it has none: then a watcher
    from before the hand-back has nothing to move it).
    """
    from probe.sdk.session_marker import WIZARD_HINT

    for row in rows:
        if row.kind == "tap" and row.behind and row.latest:
            head = (
                f"the transcript tap is {row.installed}, behind the published {row.latest}; "
                f"the wizard's Update updates it ({WIZARD_HINT}); "
            )
            if _sessions_follow(source, row.latest, plugin):
                return head + "open sessions move to it by themselves, with no restart"
            return head + "a session started before the update keeps running the old copy until it restarts"
    return None


def _sessions_follow(source: str | None, tap: str, plugin: str | None) -> bool:
    """Do `source`'s open sessions move to tap `tap` once it is installed, with
    no restart (`updater.follows_without_restart`, the update's own verdict, on
    the state now: its Probe plugin `plugin`, its sessions on older taps)? A
    prediction: an agent proven only from what is installed (Kimi Code) is
    never said to follow a tap not installed yet.
    Never raises: unknown (its sessions could not be looked at) keeps the
    restart line."""
    try:
        from probe.cli.install import updater
        from probe.cli.wizard.state.agent_identity import agent_source

        source = source or agent_source()
        stale = updater.stale_tap_sessions(source, tap)
        if stale is None:
            return False
        result = updater.PluginResult(True, True, False, None, plugin, "", tap_after=tap, tap_running_stale=stale)
        return updater.follows_without_restart(source, result, predicting=True)
    except Exception:  # noqa: BLE001 - see docstring
        return False


def _version_rows(caps: Capabilities) -> list[str]:
    """The Versions block: one line per component, good news included.

    Printing the current components too is the point of this section. Reporting
    only what is wrong is what made silence ambiguous -- a clean machine and a
    machine nothing had ever checked produced byte-identical output.
    """
    if not caps.version_rows:
        return [
            _row("Checked against", "no cached manifest — could not check"),
            _row("", "the wizard's Update fetches it and compares"),
        ]
    from probe.shared.updates.updates import render as render_versions

    lines = [line for line in render_versions(list(caps.version_rows))]
    age = caps.version_manifest_age_s
    lines.append(_row("Checked against", f"manifest fetched {_format_age(age)}"))
    # A comparison is only as current as the thing compared against. Past a day
    # the cache is well beyond both the 15m TTL and the 1h failure backoff, which
    # means fetches have been failing -- worth saying, because every verdict above
    # is then graded against a manifest that may predate several releases.
    if age is not None and age > 86400:
        lines.append(
            _row("", "manifest is over a day old — version checks may be failing")
        )
    return lines
from probe.cli.wizard.doctor.daemon_rows import _format_age  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.harness.diagnosis import _row  # noqa: E402 -- pieces need each other; the front door loads this one first
