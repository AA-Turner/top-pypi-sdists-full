"""Agent Tasks transport-failure diagnostics."""

from __future__ import annotations

import importlib.metadata
import os
import re
import shutil
import subprocess
from collections.abc import Callable, Mapping, Sequence
from urllib.parse import urlsplit

from agentic_devtools.cli.ci.retry import RetryableError


class AgentTaskDiagnostics:
    """Format best-effort Agent Tasks failure metadata."""

    def __init__(
        self,
        endpoint: str,
        env: Mapping[str, str] | None,
        sanitize: Callable[[str], str],
        *,
        is_agent_tasks: bool = False,
    ) -> None:
        self.endpoint = endpoint
        self.env = env
        self.sanitize = sanitize
        self._is_agent_tasks = is_agent_tasks
        self.status: int | None = None
        self.status_source: str | None = None
        self.returncode: int | None = None

    @property
    def is_agent_tasks(self) -> bool:
        """Return the provider's endpoint classification for this request."""
        return self._is_agent_tasks

    def format_error(self, text: str, *, prefix: str | None = None) -> str:
        """Format an error while preserving legacy non-Agent error behavior."""
        if not self.is_agent_tasks:
            if prefix is None:
                return text
            return f"{prefix}{self.sanitize(text)}"
        sanitized = self.sanitize(text)
        request_url = urlsplit(self.endpoint)
        subprocess_environment = self.env if self.env is not None else os.environ
        try:
            package_version = importlib.metadata.version("agentic-devtools")
        except Exception:
            package_version = "not captured"
        path = subprocess_environment.get("PATH")
        try:
            executable = shutil.which("gh", path=path) if path else None
        except Exception:
            executable = None
        status_source = self.status_source or ("response_headers" if self.status is not None else "not captured")
        fields = (
            f"agentic_devtools_version={self.sanitize(package_version or 'not captured')}",
            f"gh_executable={self.sanitize(executable or 'not captured')}",
            f"endpoint={self.sanitize(request_url.path or 'not captured')}",
            f"host={self.sanitize(request_url.hostname or subprocess_environment.get('GH_HOST') or 'not captured')}",
            f"query={self.sanitize(request_url.query or 'not captured')}",
            "url=not captured",
            f"http_status={self.status if self.status is not None else 'not captured'}",
            f"http_status_source={status_source}",
            f"returncode={self.returncode if self.returncode is not None else 'not captured'}",
            "response_body=not captured",
        )
        return (
            f"{prefix or ''}{sanitized[:512]}{'; ' if sanitized else ''}"
            f"Agent Tasks failure diagnostics: {'; '.join(fields)}"
        )

    def add_launch_failure_note(self, error: OSError) -> None:
        """Attach transport metadata without replacing a local launch error."""
        if self.is_agent_tasks:
            error.add_note(self.format_error(""))

    def run(
        self,
        runner: Callable[..., subprocess.CompletedProcess[str]],
        command: Sequence[str],
        timeout_message: str,
        **kwargs: object,
    ) -> subprocess.CompletedProcess[str]:
        """Run ``gh``, preserving retryable timeout and launch failures."""
        try:
            return runner(command, **kwargs)
        except subprocess.TimeoutExpired as error:
            raise RetryableError(self.format_error(timeout_message)) from error
        except OSError as error:
            self.add_launch_failure_note(error)
            raise

    def record_result(
        self,
        result: subprocess.CompletedProcess[str],
        status: int | None,
        stderr: str,
        status_pattern: re.Pattern[str],
    ) -> int | None:
        """Store the transport fields available from a completed ``gh`` call."""
        self.returncode = result.returncode
        self.status = status
        status_match = status_pattern.search(stderr)
        if self.status is None and status_match:
            self.status = int(status_match.group(1))
            self.status_source = "stderr"
        return self.status
