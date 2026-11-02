"""Claude Code headless: stream-json flags, read-only settings JSON, folders a permission rule cannot confine."""

from __future__ import annotations
from pathlib import Path

#: A permission rule's argument is delimited by parentheses, so a folder whose
#: own name contains one cannot be expressed as a rule -- and a rule that fails
#: to parse does not fail loudly, it just stops denying. `Research (old)` is an
#: ordinary macOS folder name, so this is a real path, not a theoretical one.
_UNRULEABLE = ("(", ")")


def readonly_settings(folder: Path | None) -> str:
    """Claude settings JSON for an agent the import launches.

    `folder`, when given, is made unwritable (the confinement rule). Every such
    agent also runs with NO HOOKS. It is Probe's own automation, not a session
    the researcher started: the researcher's hooks -- the Probe plugins' capture,
    daemon and guard among them -- would register it as theirs, and Probe then
    uploaded its own classifier sessions as the researcher's history (45 in one
    tenant on 2026-10-25). Its confinement does not come from hooks: it is the
    tool allowlist and this deny rule.

    And with NO AUTO MEMORY: Claude Code otherwise saves notes about the folder into
    the researcher's own `~/.claude/projects/<work dir>/memory/` (seen 2026-10-28: a
    classifier session wrote `MEMORY.md` and a note there). Headless flags leave it
    on; this setting turns it off, and so does `CLAUDE_CODE_DISABLE_AUTO_MEMORY`,
    which `_backfill_agent_env` sets too, so a Claude that ignores one still gets
    the other (each alone verified on Claude Code 2.1.296).

    Returned as a JSON string for `--settings`, which takes either that or a
    path. A string keeps the rule in the argv the test can read, rather than in
    a temp file whose lifetime is one more thing to get wrong.
    """
    import json

    settings: dict = {"disableAllHooks": True, "autoMemoryEnabled": False}
    if folder is not None:
        settings["permissions"] = {"deny": [f"Edit({folder}/**)"]}
    return json.dumps(settings)


def unruleable(folder: Path) -> bool:
    """Whether `folder` cannot be confined by a Claude permission rule."""
    return any(ch in str(folder) for ch in _UNRULEABLE)
