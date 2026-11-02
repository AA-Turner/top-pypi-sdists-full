"""Codex's HookTrust: approve Probe's own hooks so they run without /hooks, for the plugins this run keeps on."""

from __future__ import annotations


def codex_hooks_waiting() -> bool:
    """Probe's plugins are in Codex and some of their hooks wait for an approval
    Probe may give (`codex_hooks.waiting`, `approve`'s own rule). Asks Codex
    (one app-server start, ~0.2s, at most STATUS_TIMEOUT_S) only where a Probe
    plugin copy is in Codex's cache."""
    from probe.shared.harness.harnesses.codex import hooks as codex_hooks

    try:
        if not codex_hooks.installed_copies():
            return False
        return codex_hooks.waiting(timeout=codex_hooks.STATUS_TIMEOUT_S)
    except Exception:  # noqa: BLE001 - a question asked before the plan never fails it
        return False


def approve_codex_hooks(only: frozenset[str] | None = None) -> tuple[list[str], bool]:
    """Approve Probe's own hooks in Codex, so they run without a trip to `/hooks`:
    (lines to show, whether none of Probe's hooks waits for approval now).

    Codex skips a plugin's hook until it is approved and says nothing in the
    session, so a fresh install recorded nothing until the person found `/hooks`
    (and T3 Code, which drives Codex, has no `/hooks` at all). Only Probe's own
    plugins' hooks are approved (`codex_hooks.approvable`). Never a failure line:
    a hook left waiting is what `/hooks` already fixes, so the line names it
    instead of failing the install."""
    from probe.shared.harness.harnesses.codex import hooks as codex_hooks

    try:
        outcome = codex_hooks.approve(only=only)
    except Exception:  # noqa: BLE001 - approve never raises; an install never fails on it either way
        outcome = None
    lines: list[str] = []
    if outcome is not None and outcome.approved:
        count = len(outcome.approved)
        lines.append(f"Approved Probe's {count} hook{'s' if count != 1 else ''} in Codex.")
    if outcome is not None and outcome.done:
        return lines, True
    why = "Codex could not be asked" if outcome is None else (outcome.error or "a Probe hook still waits")
    lines.append(f"Probe's hooks in Codex still need approval ({why}): {CODEX_HOOKS_INSTRUCTION}")
    return lines, False


#: The person's own way to approve Probe's hooks, for when Probe could not.
CODEX_HOOKS_INSTRUCTION = "in a new Codex session, type /hooks and approve the Probe hooks."
