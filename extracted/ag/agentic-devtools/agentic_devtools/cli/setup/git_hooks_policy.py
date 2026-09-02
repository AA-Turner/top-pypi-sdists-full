"""Policy governing whether agentic-devtools manages ``core.hooksPath``.

Consumer repositories that manage git hooks with another tool (Husky, pre-commit,
…) can opt out entirely with ``"manage_git_hooks": false`` in
``.agdt/config/project.json``.

The messages defined here are duplicated verbatim inside the generated
``agentic-devtools-required-setup.py`` template, which is contractually
stdlib-only and therefore cannot import this module.  A parity test keeps the
two copies in sync.
"""

from __future__ import annotations

import sys
from pathlib import Path

from agentic_devtools.cli.config.project_config import load_project_config

#: Top-level key in ``.agdt/config/project.json``.
MANAGE_GIT_HOOKS_KEY = "manage_git_hooks"

HOOKS_DISABLED_MESSAGE = (
    "  ℹ Git hooks management is disabled by project config "
    "(manage_git_hooks: false in .agdt/config/project.json) — leaving core.hooksPath unchanged."
)

PRESERVED_MESSAGE_PREFIX = "  ⚠ core.hooksPath is already set to "

PRESERVED_MESSAGE_SUFFIX = (
    "    agentic-devtools did not overwrite it. "
    'Set "manage_git_hooks": false in .agdt/config/project.json to silence this notice.'
)

NON_BOOLEAN_WARNING_PREFIX = f"  ⚠ {MANAGE_GIT_HOOKS_KEY} in .agdt/config/project.json must be a boolean, got "


def format_preserved_message(current: str) -> str:
    """Return the two-line notice printed when a foreign hooks path is preserved.

    Args:
        current: The existing ``core.hooksPath`` value that is being kept.
    """
    return f"{PRESERVED_MESSAGE_PREFIX}'{current}' — leaving it unchanged.\n{PRESERVED_MESSAGE_SUFFIX}"


def is_git_hooks_management_enabled(git_root: Path) -> bool:
    """Return ``False`` only when the project config explicitly disables hooks management.

    Reads :func:`load_project_config` directly rather than the
    ``config_mode``-aware accessors: this is a safety toggle, so it must keep
    working in ``config_mode = "manual"`` repositories, and it must not be run
    through ``str()`` coercion (which would turn ``False`` into the truthy
    ``"False"``).

    Args:
        git_root: Repository root whose ``.agdt/config/project.json`` is read.

    Returns:
        ``True`` when the key is absent, ``null``, or not a boolean.
    """
    value = load_project_config(git_root=git_root).get(MANAGE_GIT_HOOKS_KEY)
    if value is None:
        return True
    if isinstance(value, bool):
        return value
    print(f"{NON_BOOLEAN_WARNING_PREFIX}{value!r}. Treating it as enabled.", file=sys.stderr)
    return True
