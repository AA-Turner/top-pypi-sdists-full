from __future__ import annotations

import subprocess
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

from spec_kitty_tracker.context import LocalExecutionContext
from spec_kitty_tracker.errors import ConnectorRequestError


class CommandRunner(Protocol):
    def run(
        self,
        command: Sequence[str],
        *,
        cwd: str | None = None,
        context: LocalExecutionContext | None = None,
    ) -> str: ...


@dataclass(slots=True)
class SubprocessCommandRunner:
    """Direct-subprocess runner. Accepts ``context`` (TRK-M1-02 A4) but
    ignores it: this runner has no scoped transport to attribute the call
    to — it always spawns the configured command directly. A host that
    needs the context honored supplies its own scoped runner (e.g.
    ``GatewayCommandRunner`` in spec-kitty, TRK-M1-04) instead of this one.
    """

    timeout_seconds: float = 30.0

    def run(
        self,
        command: Sequence[str],
        *,
        cwd: str | None = None,
        context: LocalExecutionContext | None = None,
    ) -> str:
        del context
        try:
            completed = subprocess.run(
                list(command),
                cwd=cwd,
                check=True,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
            )
        except subprocess.CalledProcessError as exc:
            stderr = exc.stderr.strip() if exc.stderr else ""
            raise ConnectorRequestError(
                f"Command failed: {' '.join(command)} :: {stderr or exc}"
            ) from exc
        except subprocess.TimeoutExpired as exc:
            raise ConnectorRequestError(f"Command timed out: {' '.join(command)}") from exc
        return completed.stdout
