"""Resolve the shell used for agent-executed bash commands.

Precedence:
  1. $SHELL if set and executable
  2. The login shell from /etc/passwd (via pwd.getpwuid)
  3. First available of bash/zsh — preferring zsh on macOS, bash elsewhere
  4. /bin/sh
"""

from __future__ import annotations

import os
import platform
import shutil


def resolve_shell() -> str:
    env_shell = os.environ.get("SHELL")
    if env_shell and os.access(env_shell, os.X_OK):
        return env_shell

    login_shell = _login_shell_from_passwd()
    if login_shell and os.access(login_shell, os.X_OK):
        return login_shell

    prefer_zsh = platform.system() == "Darwin"
    ordered = ("zsh", "bash") if prefer_zsh else ("bash", "zsh")
    for name in ordered:
        found = shutil.which(name)
        if found:
            return found

    return "/bin/sh"


def _login_shell_from_passwd() -> str | None:
    try:
        import pwd

        return pwd.getpwuid(os.getuid()).pw_shell or None
    except (ImportError, KeyError, OSError):
        return None
