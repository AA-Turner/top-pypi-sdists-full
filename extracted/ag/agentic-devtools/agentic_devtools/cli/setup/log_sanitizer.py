"""Output sanitizer for setup logs — value-based secret redaction.

Redacts known secret values from environment variables and GitHub token
prefixes from arbitrary text.  Designed for sanitizing setup logs and
issue reports before they are displayed or persisted.

Downstream consumer: #2299 orchestrator imports ``sanitize()`` directly.
"""

from __future__ import annotations

import os
import re

REDACTION_PLACEHOLDER: str = "[REDACTED]"
"""Uniform placeholder inserted in place of every redacted secret."""

_SECRET_ENV_VARS: tuple[str, ...] = (
    "AZURE_DEV_OPS_COPILOT_PAT",
    "GITHUB_TOKEN",
    "JIRA_COPILOT_PAT",
)
"""Environment variable names whose *values* are treated as secrets."""

_GITHUB_PREFIX_PATTERN: re.Pattern[str] = re.compile(r"(ghp_|gho_|ghs_|github_pat_)[A-Za-z0-9_]+")
"""Compiled regex matching GitHub token prefix patterns (FR-003: no unbounded
generic base64 regex)."""


def sanitize(text: str) -> str:
    """Redact known secrets from *text* and return the sanitized result.

    The function is:
    - **Stateless**: environment variables are read fresh on every call
      (NFR-004).
    - **Idempotent**: ``sanitize(sanitize(x)) == sanitize(x)`` (FR-006).
    - **Safe**: absent or empty env vars are silently skipped (FR-007).

    Ordering guarantee (FR-010): value-based replacement runs *before*
    prefix-pattern matching so that a full token present in the environment
    is replaced by value rather than partially matched by prefix.
    """
    # --- Step 1: Value-based redaction (FR-001, FR-002) ---
    # Read env vars fresh each call for statelessness (NFR-004).
    secret_values: list[str] = []
    for var_name in _SECRET_ENV_VARS:
        value = os.environ.get(var_name, "")
        if value:  # skip empty/unset (FR-007)
            secret_values.append(value)

    # Sort by length descending so longer secrets are replaced first,
    # preventing partial matches when one secret is a substring of another.
    secret_values.sort(key=len, reverse=True)

    # Use str.replace() — treats values as literals, no regex metachar
    # issues (FR-008), replaces all occurrences (FR-009).
    for secret in secret_values:
        text = text.replace(secret, REDACTION_PLACEHOLDER)

    # --- Step 2: Prefix-pattern redaction (FR-003, FR-010) ---
    text = _GITHUB_PREFIX_PATTERN.sub(REDACTION_PLACEHOLDER, text)

    return text
