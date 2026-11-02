"""GitHub API lookup and cooldown checks for the AI PR Loop dispatcher."""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
from collections.abc import Callable, Mapping
from datetime import UTC, datetime
from urllib.parse import quote

from agentic_devtools.cli.ci.dispatcher_policy import (
    MAX_RETRY_WINDOW_SECONDS,
    _is_rate_limit,
    _notify_rate_limit,
    _parse_workflow_run,
    _rate_limit_error,
    _validate_retry_settings,
    calculate_dispatch_retry_delay,
)
from agentic_devtools.cli.shared.retry import ProviderRateLimitError
from agentic_devtools.cli.subprocess_utils import run_safe

COOLDOWN_SECONDS = 60
MAX_ATTEMPTS = 3
_HTTP_STATUS = re.compile(r"^HTTP/[0-9.]+\s+(\d{3})(?:\s|$)")


class DispatcherThrottle:
    """Look up the latest throttler run and decide whether the dispatcher should wait."""

    def __init__(
        self,
        *,
        on_rate_limit: Callable[[ProviderRateLimitError], None] | None = None,
        max_attempts: int = MAX_ATTEMPTS,
        retry_window_seconds: float = MAX_RETRY_WINDOW_SECONDS,
    ) -> None:
        _validate_retry_settings(max_attempts, retry_window_seconds)
        self._on_rate_limit = on_rate_limit
        self._max_attempts = max_attempts
        self._retry_window_seconds = retry_window_seconds

    def check(self, *, repository: str, default_branch: str, output_path: str) -> bool:
        """Write the throttle decision to the GitHub Actions output file and return it."""
        if repository.count("/") != 1 or not all(repository.split("/")):
            raise ValueError("GITHUB_REPOSITORY must use owner/repo format")
        if not default_branch:
            raise ValueError("default_branch must not be empty")

        last_run = self._lookup_last_run(repository, default_branch)
        throttled = self._is_throttled(last_run)
        with open(output_path, "a", encoding="utf-8") as output:
            output.write(f"throttled={'true' if throttled else 'false'}\n")
        return throttled

    def _lookup_last_run(self, repository: str, default_branch: str) -> dict[str, object]:
        endpoint = (
            f"/repos/{repository}/actions/workflows/ai-pr-loop-throttler.yml/runs"
            f"?per_page=1&branch={quote(default_branch, safe='')}"
        )
        retry_deadline = time.time() + self._retry_window_seconds
        attempt = 1
        while True:
            uses_read_pool = "AGDT_GITHUB_SECRETS_JSON" in os.environ
            if uses_read_pool:
                from agentic_devtools.cli.ci.github_provider import _run_readonly_gh_command

                try:
                    result = _run_readonly_gh_command(
                        ["api", endpoint, "--include"],
                        resource="rest",
                        return_rate_limit_result=True,
                        runner=run_safe,
                    )
                except ProviderRateLimitError as exc:
                    _notify_rate_limit(exc, self._on_rate_limit)
                    raise
            else:
                result = run_safe(["gh", "api", endpoint, "--include"], capture_output=True, text=False, shell=False)
            stdout = result.stdout or b""
            stderr_value = result.stderr or b""
            stderr = stderr_value if isinstance(stderr_value, str) else stderr_value.decode("utf-8", errors="replace")
            stdout_bytes = stdout.encode("utf-8") if isinstance(stdout, str) else stdout
            parts = re.split(rb"\r?\n\r?\n", stdout_bytes, maxsplit=1)
            header_block = parts[0].decode("utf-8", errors="replace")
            body = parts[1] if len(parts) == 2 else b""
            status_code, headers, error_message = self._parse_diagnostics(header_block, stderr)
            retry_reason: str | None = None
            rate_limit = False

            if result.returncode == 0:
                if not body.strip():
                    retry_reason = "empty successful response"
                else:
                    content_length = headers.get("content-length")
                    if content_length and content_length.isascii() and content_length.isdigit():
                        declared_length = content_length.lstrip("0") or "0"
                        received_length = str(len(body))
                        if len(declared_length) > len(received_length) or (
                            len(declared_length) == len(received_length) and declared_length > received_length
                        ):
                            retry_reason = "truncated successful response"

                if retry_reason is None:
                    return _parse_workflow_run(body)
            else:
                rate_limit = _is_rate_limit(status_code, headers, f"{stderr}\n{body.decode('utf-8', errors='replace')}")
                if rate_limit:
                    retry_reason = "confirmed rate limit"
                    delay = calculate_dispatch_retry_delay(headers)
                    rate_error = _rate_limit_error(headers, delay)
                    _notify_rate_limit(rate_error, self._on_rate_limit)
                else:
                    message = error_message or "Throttle lookup failed with a non-rate-limit API error."
                    raise RuntimeError(
                        f"{message} Throttle state is unknown and the scheduler wake-up was not handled."
                    )

            if attempt == self._max_attempts:
                if rate_limit:
                    raise rate_error
                raise RuntimeError(
                    f"Throttle lookup returned an {retry_reason} after {self._max_attempts} attempts; "
                    "throttle state is unknown and the scheduler wake-up was not handled."
                )

            if not rate_limit:
                delay = calculate_dispatch_retry_delay(headers)
            now = time.time()
            if now + delay > retry_deadline:
                if rate_limit:
                    raise rate_error
                raise RuntimeError(
                    "Throttle-state retry time exceeds the bounded retry window; "
                    "throttle state is unknown and the scheduler wake-up was not handled."
                )

            if rate_limit:
                print(
                    f"::notice::GitHub rate-limited the throttle lookup; retrying in {delay:g}s "
                    f"(attempt {attempt}/{self._max_attempts})."
                )
            else:
                print(
                    f"::notice::Throttle lookup returned an {retry_reason}; retrying in {delay:g}s "
                    f"(attempt {attempt}/{self._max_attempts})."
                )
            time.sleep(delay)
            attempt += 1

    @staticmethod
    def _parse_diagnostics(header_block: str, stderr: str) -> tuple[int | None, dict[str, str], str | None]:
        status_code: int | None = None
        headers: dict[str, str] = {}
        error_message: str | None = None
        for line in header_block.splitlines():
            response_line = line.strip()
            status_match = _HTTP_STATUS.match(response_line)
            if status_match:
                status_code = int(status_match.group(1))
                continue
            name, separator, value = response_line.partition(":")
            if separator:
                headers[name.strip().lower()] = value.strip()
        for line in stderr.splitlines():
            stripped = line.strip()
            if stripped.startswith("gh:"):
                error_message = stripped
        return status_code, headers, error_message

    def _is_throttled(self, last_run: Mapping[str, object]) -> bool:
        status = last_run.get("status")
        if status and status != "completed":
            print(f"::notice::Throttled — ai-pr-loop-throttler is currently {status}")
            return True

        conclusion = last_run.get("conclusion")
        if conclusion and conclusion != "success":
            print(f"Last monitor run concluded as '{conclusion}' — proceeding with dispatch (no cooldown).")
            return False

        last_run_end = last_run.get("updated_at")
        if not last_run_end:
            print("No prior runs found — proceeding with dispatch.")
            return False
        if not isinstance(last_run_end, str):
            raise RuntimeError("Throttle lookup returned an invalid updated_at value.")
        try:
            parsed_end = datetime.fromisoformat(last_run_end.replace("Z", "+00:00"))
        except ValueError as exc:
            raise RuntimeError("Throttle lookup returned an invalid updated_at timestamp.") from exc
        if parsed_end.tzinfo is None:
            parsed_end = parsed_end.replace(tzinfo=UTC)
        elapsed = time.time() - parsed_end.timestamp()
        print(f"Last monitor run ended {elapsed:g}s ago (cooldown={COOLDOWN_SECONDS}s)")
        if elapsed < COOLDOWN_SECONDS:
            print(f"::notice::Throttled — last run ended {elapsed:g}s ago, cooldown is {COOLDOWN_SECONDS}s")
            return True
        return False


def main(argv: list[str] | None = None) -> None:
    """Run the dispatcher throttle check as a command-line entry point."""
    parser = argparse.ArgumentParser(description="Check whether the AI PR Loop dispatcher should be throttled")
    parser.add_argument("--default-branch", required=True)
    args = parser.parse_args(argv)

    repository = os.environ.get("GITHUB_REPOSITORY", "")
    output_path = os.environ.get("GITHUB_OUTPUT", "")
    if not repository or not output_path:
        print("::error::GITHUB_REPOSITORY and GITHUB_OUTPUT must be set.", file=sys.stderr)
        raise SystemExit(1)

    try:
        DispatcherThrottle().check(
            repository=repository,
            default_branch=args.default_branch,
            output_path=output_path,
        )
    except (OSError, RuntimeError, ValueError, ProviderRateLimitError) as exc:
        print(f"::error::{exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
