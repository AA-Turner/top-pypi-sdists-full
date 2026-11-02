"""judge a plugin update's tap: did it advance, and what the stale-session notes in an update record now say."""

from __future__ import annotations
import re
from collections.abc import Callable
from probe.foundation.harness_registry import get_registry


def tap_verdict(result: PluginResult, target: str | None) -> tuple[str, bool]:
    """`(line, behind)` for the tap after an update run.

    `behind` is True for an INSTALLED tap still older than the manifest's
    `tap.latest` once the update ran -- the stale tap that capture relies on and
    that nothing reported -- and for a tap the run REMOVED (installed before,
    gone after: capture stops at the next session start). Either fails the
    plugin half. A tap that was never installed is a skip, not a failure. A
    behind line carries the reason (`tap_detail`), the way the plugin's own
    failure does, or "same failure as above" when it IS the plugin's failure,
    printed just above.
    """
    after = result.tap_after
    # A tap that failed with the plugin's own failure (a failed refresh, or any
    # Codex failure) is printed right under it: saying it twice doubled the
    # longest thing on the screen.
    detail = "same failure as above" if result.tap_detail == result.message else result.tap_detail
    if not after:
        if result.tap_before:
            # The no-op sentences ("did not advance") are not what happened. A
            # list that could not be read (Codex) cannot say it is gone.
            seen = "could not be confirmed" if result.list_unreadable else "is gone"
            line = f"transcript tap {result.tap_before} {seen} after the update"
            real = detail if detail not in (TAP_NOOP, CODEX_TAP_NOOP) else ""
            return (f"{line}: {real}" if real else line, True)
        return ("transcript tap not installed (skipped)", False)
    if target and is_newer(target, after):
        line = f"transcript tap is still {after}, behind the latest {target}"
        return (f"{line}: {detail}" if detail else line, True)
    if is_newer(after, result.tap_before):
        line = f"transcript tap updated to {after}"
    elif target:
        line = f"transcript tap already at the latest ({after})"
    else:
        line = f"transcript tap at {after}"
    # Not "behind": the update did its part, and the manual commands would not
    # help. What is left the line says.
    note = running_stale_note(result)
    return (f"{line}; {note}" if note else line, False)


def running_stale_note(result: PluginResult) -> str:
    """One sentence for live capture daemons still on an older tap, or "".

    Where open sessions follow the update (`result.follows`), they move by
    themselves: the plugin's prompt hook hands a watcher from before tap
    0.10.13 to the Probe service at its session's next prompt
    (`hooks/tap_handover.py`), a newer one hands itself over, and the service
    records on the newest installed tap. Anywhere else, a restart."""
    stale = result.tap_running_stale
    if not stale or not result.tap_after:
        return ""
    count = len(stale)
    versions = ", ".join(dict.fromkeys(stale))
    sessions = "1 session" if count == 1 else f"{count} sessions"
    run, them = ("runs", "it") if count == 1 else ("run", "them")
    if result.follows:
        moves = "moves" if count == 1 else "move"
        return (
            f"{sessions} started before the update still {run} tap {versions}; "
            f"{'it' if count == 1 else 'they'} {moves} to {result.tap_after} at the next prompt, no restart needed"
        )
    return (
        f"{sessions} started before the update still {run} tap {versions}; "
        f"restart {them} to switch to {result.tap_after}"
    )


#: The sentence `running_stale_note` stores in an update record, as this
#: release words it ("... move to X at the next prompt, no restart needed") and
#: as every release before 0.304.0 did ("... restart them to switch to X"),
#: with the agent `merged` put before it when the update ran for several.
_STALE_NOTE = re.compile(
    r"(?:(?P<agent>[A-Z][A-Za-z ]{0,30}): )?"
    r"(?:1 session|\d+ sessions) started before the update still runs? tap "
    r"[0-9][0-9A-Za-z.+-]*(?:, [0-9][0-9A-Za-z.+-]*)*; "
    r"(?:restart (?:it|them) to switch to (?P<to>[0-9][0-9A-Za-z.+-]*[0-9A-Za-z+-])"
    r"|(?:it|they) moves? to (?P<moved_to>[0-9][0-9A-Za-z.+-]*[0-9A-Za-z+-]) at the next prompt, no restart needed)"
)


def settle_stale_notes(detail: str, *, plugin_after: Callable[[str], str | None] | None = None) -> str:
    """An update record's plugin detail with each "sessions started before the
    update still run tap X; ..." sentence brought to what is true NOW. The
    record keeps the sentence as the update wrote it; `probe doctor` prints it
    as the state of the machine, and every release before 0.304.0 wrote
    "restart them" whatever was true, so doctor told people to restart sessions
    that move by themselves, long after they had.

    For the agent the sentence names (`merged` puts it first when the update
    ran for several), or, with no name (a record of one pass, whichever agent
    it was), for every agent that captures:
      * no live session runs a tap older than the one the sentence names
        (`stale_tap_sessions`): the sentence is taken out;
      * some still do, and every one of them moves by itself at its next
        prompt (`follows_without_restart` for its agent, on the state now:
        `plugin_after(agent)` is that agent's installed Probe plugin, None
        when it has none): the sentence says so, counted afresh;
      * otherwise, and whenever a look could not be made: the sentence stays
        word for word.
    Never raises: the detail as it was."""
    if not detail or "started before the update" not in detail:
        return detail
    try:
        harnesses = [h for h in get_registry().all() if getattr(h, "capture", None) is not None]
        by_label = {h.label: h.id for h in harnesses if getattr(h, "label", None)}

        def settle(match: re.Match) -> str:
            target = match["to"] or match["moved_to"]
            if match["agent"]:
                source = by_label.get(match["agent"])
                if source is None:
                    return match[0]
                candidates = [source]
            else:
                candidates = [h.id for h in harnesses]
            stale: dict[str, tuple[str, ...]] = {}
            for source in candidates:
                found = stale_tap_sessions(source, target)
                if found is None:
                    return match[0]  # could not look: never "none left"
                if found:
                    stale[source] = found
            if not stale:
                return ""
            follows = all(
                follows_without_restart(source, PluginResult(
                    True, True, False, None, plugin_after(source) if plugin_after else None, "",
                    tap_after=target, tap_running_stale=found))
                for source, found in stale.items()
            )
            if not follows:
                return match[0]
            versions = tuple(sorted((v for found in stale.values() for v in found),
                                    key=lambda v: _triplet(v) or (0, 0, 0)))
            note = running_stale_note(PluginResult(True, True, False, None, None, "", tap_after=target,
                                                   tap_running_stale=versions, follows=True))
            return f"{match['agent']}: {note}" if match["agent"] else note

        settled = _STALE_NOTE.sub(settle, detail)
        if settled == detail:
            return detail
        # The separators the taken sentences leave behind.
        settled = re.sub(r"(?:;\s*){2,}", "; ", settled)
        return re.sub(r"^\s*;\s*|\s*;\s*$", "", settled).strip()
    except Exception:  # noqa: BLE001 - see docstring
        return detail


def tap_changed(result: PluginResult) -> bool:
    return is_newer(result.tap_after, result.tap_before)
from probe.cli.install.updater.tap_sessions import follows_without_restart, stale_tap_sessions  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.harness.plugin_update import CODEX_TAP_NOOP, PluginResult, TAP_NOOP, _triplet, is_newer  # noqa: E402 -- pieces need each other; the front door loads this one first
