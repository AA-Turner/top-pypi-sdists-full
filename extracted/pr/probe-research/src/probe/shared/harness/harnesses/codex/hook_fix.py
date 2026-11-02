"""probe doctor --fix for Codex: approve Probe's own hooks again (HookTrust)."""

from __future__ import annotations


def _doctor_fix_codex_hooks() -> list[str]:
    """`probe doctor --fix`: Probe's own hooks in Codex approved again, as an
    update and the Probe service's healer approve them (#3617), and what that
    did. Empty where Codex holds no copy of Probe's plugins."""
    from probe.shared.harness.harnesses.codex import hooks as codex_hooks
    from probe.cli import wizard as wizard

    if not codex_hooks.installed_copies():
        return []
    lines, done = wizard.approve_codex_hooks()
    return lines if lines or not done else ["None of Probe's hooks waited for approval."]
from probe.cli.commands.machine.wizard import wizard  # noqa: E402 -- pieces need each other; the front door loads this one first
