"""Workflow credential resolver — named credential binding (#970).

Resolves named credentials from environment variables or shell commands.
Raw secret values are NEVER logged, persisted, or included in error messages.
Follows the same security boundary as api_key_command / TokenProvider.
"""

from __future__ import annotations

import logging
import os
import shlex
import subprocess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..config import WorkflowCredentialConfig

logger = logging.getLogger(__name__)


class CredentialResolutionError(Exception):
    """Raised when a credential cannot be resolved. Message is always redacted."""

    pass


class CredentialResolver:
    """Resolves named credentials at execution time.

    Each credential maps a name to either an env var or a shell command.
    Resolved values exist only in memory — never persisted or logged.
    """

    def __init__(self, credentials: list[WorkflowCredentialConfig]) -> None:
        self._credentials: dict[str, WorkflowCredentialConfig] = {c.name: c for c in credentials}

    def has(self, name: str) -> bool:
        return name in self._credentials

    def get_config(self, name: str) -> WorkflowCredentialConfig | None:
        return self._credentials.get(name)

    def resolve(self, name: str) -> str:
        """Resolve a named credential to its value.

        Raises CredentialResolutionError on failure. Exception messages
        contain the credential name but NEVER the resolved value.
        """
        config = self._credentials.get(name)
        if config is None:
            raise CredentialResolutionError(f"Credential {name!r} is not declared in workflow config")

        if config.env_var:
            value = os.environ.get(config.env_var)
            if value is None:
                raise CredentialResolutionError(
                    f"Credential {name!r}: environment variable {config.env_var!r} is not set"
                )
            if not value:
                raise CredentialResolutionError(
                    f"Credential {name!r}: environment variable {config.env_var!r} is empty"
                )
            return value

        if config.command:
            try:
                result = subprocess.run(
                    shlex.split(config.command),
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
            except subprocess.TimeoutExpired:
                raise CredentialResolutionError(f"Credential {name!r}: command timed out after 30s") from None
            except FileNotFoundError:
                raise CredentialResolutionError(f"Credential {name!r}: command not found") from None
            except Exception:
                raise CredentialResolutionError(f"Credential {name!r}: command execution failed") from None

            if result.returncode != 0:
                raise CredentialResolutionError(f"Credential {name!r}: command exited with code {result.returncode}")
            value = result.stdout.strip()
            if not value:
                raise CredentialResolutionError(f"Credential {name!r}: command produced empty output")
            return value

        raise CredentialResolutionError(f"Credential {name!r}: neither env_var nor command is configured")
