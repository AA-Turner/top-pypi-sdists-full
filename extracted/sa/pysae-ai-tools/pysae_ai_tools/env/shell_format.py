"""Shell-syntax formatting and shell detection — public API of the ``env`` group.

Turns a resolved ``name`` / ``value`` pair into the assignment (or removal)
syntax of a target shell, and best-effort detects the invoking shell. Consumed
by ``env resolve`` / ``activate`` / ``deactivate`` / ``dotenv`` / ``run`` /
``shell-init`` — the single place that knows how each shell spells an export,
so no module reaches into another's internals for it.
"""

import os
import shlex
import sys

VALID_SHELLS = ("posix", "powershell", "cmd", "fish")


def detect_shell() -> str:
    """Best-effort detection of the invoking shell.

    ``fish`` when the shell is fish (``$FISH_VERSION`` or ``$SHELL`` ends in
    ``fish``); otherwise ``posix`` (bash/zsh/sh/dash/ksh — same syntax). On
    Windows: ``posix`` if ``SHELL`` is set (Git Bash / MSYS2 / Cygwin / WSL),
    else ``powershell`` if ``PSModulePath`` is set, else ``cmd``.
    """
    if os.environ.get("FISH_VERSION") or os.environ.get("SHELL", "").endswith("fish"):
        return "fish"
    if sys.platform != "win32":
        return "posix"
    if os.environ.get("SHELL"):
        return "posix"
    if os.environ.get("PSModulePath"):
        return "powershell"
    return "cmd"


def format_set_line(shell: str, name: str, value: str) -> str:
    """Format a single variable assignment for the given shell."""
    if shell == "posix":
        return f"export {name}={shlex.quote(value)}"
    if shell == "powershell":
        escaped = value.replace("'", "''")
        return f"$env:{name} = '{escaped}'"
    if shell == "cmd":
        escaped = value.replace("%", "%%").replace('"', '""')
        return f'set "{name}={escaped}"'
    if shell == "fish":
        escaped = value.replace("\\", "\\\\").replace("'", "\\'")
        return f"set -gx {name} '{escaped}'"
    raise ValueError(f"unknown shell: {shell}")


def format_unset_line(shell: str, name: str) -> str:
    """Format a single variable removal for the given shell."""
    if shell == "posix":
        return f"unset {name}"
    if shell == "powershell":
        return f"Remove-Item Env:{name} -ErrorAction SilentlyContinue"
    if shell == "cmd":
        return f'set "{name}="'
    if shell == "fish":
        return f"set -e {name}"
    raise ValueError(f"unknown shell: {shell}")


def set_mode_hint(shell: str) -> str:
    """Shell-compatible comment telling the user how to consume the output."""
    if shell == "posix":
        return '# Pipe into `eval "$(…)"` to apply the exports in your shell.'
    if shell == "powershell":
        return "# Pipe into `Invoke-Expression` (alias `iex`) to apply: `… | iex`."
    if shell == "cmd":
        return ":: Consume via `for /f \"delims=\" %i in ('…') do @%i` to apply."
    if shell == "fish":
        return "# Pipe into `source`: `pysae-ai-tools env resolve --set … | source`."
    raise ValueError(f"unknown shell: {shell}")
