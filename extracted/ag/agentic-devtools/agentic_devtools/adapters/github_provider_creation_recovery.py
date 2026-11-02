"""Retry-safe issue creation request recovery."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from typing import Any

from agentic_devtools.adapters.github_provider_common import _detect_transient
from agentic_devtools.adapters.github_provider_idempotency import GitHubProviderIdempotencyMixin
from agentic_devtools.adapters.issue_provider import ProviderIssueResult
from agentic_devtools.adapters.retry import TransientError, retry_on_transient


@dataclass
class _CreationRecoveryState:
    recovered: ProviderIssueResult | None = None
    recovery_attempted: bool = False


class GitHubProviderCreationRecoveryMixin(GitHubProviderIdempotencyMixin):
    def _create_issue_with_recovery(
        self,
        args: list[str],
        payload: dict[str, Any],
        lookup_key: str,
    ) -> tuple[subprocess.CompletedProcess[str] | None, ProviderIssueResult | None]:
        state = _CreationRecoveryState()
        try:
            if lookup_key:
                result = retry_on_transient(lambda: self._create_issue_request(args, payload, lookup_key, state))()
            else:
                result = self._create_issue_request(args, payload, lookup_key, state)
        except TransientError as exc:
            if not lookup_key:
                raise
            raise RuntimeError(
                "Issue creation outcome is uncertain after a transient response; the mapping entry remains pending."
            ) from exc
        return result, state.recovered

    def _create_issue_request(
        self,
        args: list[str],
        payload: dict[str, Any],
        lookup_key: str,
        state: _CreationRecoveryState,
    ) -> subprocess.CompletedProcess[str] | None:
        if state.recovery_attempted and lookup_key:
            state.recovered = self._lookup_uncertain_creation(lookup_key)
            if state.recovered is not None:
                return None
            raise RuntimeError(
                "Issue creation outcome is uncertain after a transient response; the mapping entry remains pending."
            )

        result = self._run(
            args,
            capture_output=True,
            text=True,
            shell=False,
            input=json.dumps(payload),
        )
        if result.returncode == 0:
            return result
        stderr = result.stderr or ""
        try:
            _detect_transient(stderr)
        except TransientError:
            if lookup_key:
                state.recovery_attempted = True
                state.recovered = self._lookup_uncertain_creation(lookup_key)
                if state.recovered is not None:
                    return None
            raise
        raise RuntimeError(f"Failed to create issue: {stderr}")

    def _lookup_uncertain_creation(self, lookup_key: str) -> ProviderIssueResult | None:
        try:
            return self._find_by_orchestration_key(lookup_key)
        except TransientError:
            raise
        except Exception as lookup_exc:
            raise RuntimeError(
                "Issue creation outcome is uncertain after a transient response; the mapping entry remains pending."
            ) from lookup_exc
