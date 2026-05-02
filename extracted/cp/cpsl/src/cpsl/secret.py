"""Secrets — secure credential references for channels and apps.

A ``Secret`` is a reference to a value stored on the platform.  Use it
anywhere a credential field accepts ``str | Secret``:

    # In channel config — resolved at deploy time, injected as env var
    cpsl.Telegram(bot_token=cpsl.Secret.from_name("TELEGRAM_BOT_TOKEN"))

    # At runtime — reads env var if injected, otherwise fetches via gRPC
    token = cpsl.Secret.from_name("TELEGRAM_BOT_TOKEN").value

Create secrets with the CLI::

    capsule secret create TELEGRAM_BOT_TOKEN=8625198465:AAEj...
"""

from __future__ import annotations

import os
import threading
from dataclasses import dataclass, field
from typing import Callable, Optional

_resolver: Optional[Callable[[str], str]] = None
_resolver_lock = threading.Lock()
_cache: dict[str, str] = {}


def _set_resolver(fn: Callable[[str], str]) -> None:
    global _resolver
    with _resolver_lock:
        _resolver = fn


@dataclass
class Secret:
    """Reference to a secret stored on the platform.

    Use ``Secret.from_name(...)`` — don't instantiate directly.
    """

    _name: Optional[str] = field(default=None, repr=False)

    @staticmethod
    def from_name(name: str) -> Secret:
        """Reference a secret stored on the platform by name."""
        return Secret(_name=name)

    @property
    def name(self) -> str | None:
        return self._name

    @property
    def value(self) -> str:
        """Read the secret value at runtime.

        Checks the environment first (secrets in the ``secrets`` list or
        channel configs are injected as env vars).  Falls back to an
        on-demand gRPC fetch for any other platform secret.
        """
        if not self._name:
            raise ValueError("Secret has no name")

        val = os.environ.get(self._name)
        if val is not None:
            return val

        if self._name in _cache:
            return _cache[self._name]

        with _resolver_lock:
            fn = _resolver
        if fn is None:
            raise ValueError(
                f"Secret '{self._name}' not found in environment and no "
                f"runtime connection available. Are you inside a running app?"
            )

        val = fn(self._name)
        _cache[self._name] = val
        return val

    def to_dict(self) -> dict:
        return {"_secret_name": self._name}

    def __str__(self) -> str:
        return f"Secret({self._name})"
