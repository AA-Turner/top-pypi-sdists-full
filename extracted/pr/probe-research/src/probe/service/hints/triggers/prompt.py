"""a researcher prompt on the main stream (not a slash command or hook echo)."""

from __future__ import annotations
#: A "prompt" that is no researcher's message: a `!command` (Claude Code's
#: bash-mode turns, Codex's `<user_shell_command>`), whose output the capture
#: withholds (the consent screen), or a `[Probe]` message the agent was handed.
_NOT_PROMPTS = ("<bash-input>", "<bash-stdout>", "<bash-stderr>", "<user_shell_command>", "[Probe]")
