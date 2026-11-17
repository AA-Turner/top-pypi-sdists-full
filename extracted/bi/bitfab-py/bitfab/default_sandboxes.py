from __future__ import annotations

from bitfab.github_sandbox import github_sandbox
from bitfab.gmail_sandbox import gmail_sandbox
from bitfab.sandbox import Sandbox


def default_sandboxes() -> list[Sandbox]:
    return [gmail_sandbox(), github_sandbox()]
