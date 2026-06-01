"""`efterlev shell` — interactive REPL.

Compresses the 36-command CLI surface into one persistent session.
Workspace state shows on entry and re-prints after state-changing
commands. Tab-completion derives from the slash-command registry.
Slash commands dispatch to the same Typer entrypoints the bare CLI
uses; no command logic is duplicated.

Design intent: subtle styling (one accent color + one muted), no
panels or screen-grabbing, plays nice with terminal scrollback. See
the v0.1.132 release notes for the full UX rationale.
"""

from __future__ import annotations

from efterlev.shell.session import run_shell

__all__ = ["run_shell"]
