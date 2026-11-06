"""A sandbox hook that sets the git identity of the commits an agent makes in its sandbox."""

from __future__ import annotations

import shlex

from mistralai.vibe_agents.sdk.authoring.contracts import SandboxCallbackContext, SandboxHook

_FORBIDDEN_CHARACTERS = frozenset("<>\n\r\0")


class GitIdentity(SandboxHook):
    """Set the sandbox's global git ``user.name`` and ``user.email`` when it is created::

    agents.pattern.sandbox_hook.GitIdentity(name="Acme Bot", email="bot@acme.com")

    ``DangerousLocalSandbox`` refuses it: on your machine, it would overwrite your ``~/.gitconfig``.

    Args:
        name: The git ``user.name``.
        email: The git ``user.email``.
    """

    _changes_host_state = True

    def __init__(self, *, name: str, email: str) -> None:
        super().__init__()
        self._name = _checked_git_value("name", name)
        self._email = _checked_git_value("email", email)

    async def on_create(self, ctx: SandboxCallbackContext) -> None:
        command = (
            f"git config --global user.name {shlex.quote(self._name)} && "
            f"git config --global user.email {shlex.quote(self._email)}"
        )
        result = await ctx.sandbox.execute(command)
        if result.exit_code != 0:
            raise RuntimeError(f"git config failed with exit code {result.exit_code}: {result.stderr.strip()[:500]}")


def _checked_git_value(field: str, value: str) -> str:
    # git refuses an identity it cannot write between "<" and ">" on one line.
    if not value.strip() or _FORBIDDEN_CHARACTERS.intersection(value):
        raise ValueError(f"GitIdentity {field} must be non-empty, on one line, and contain no '<' or '>'")
    return value


__all__ = ["GitIdentity"]
