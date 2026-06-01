# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""GitHub Actions secret-masking helpers for connector integration-test configs.

Emits `::add-mask::` workflow commands for any secret-valued properties in
fetched connector configs, using the shared connector spec-mask list at
[`specs_secrets_mask.yaml`](https://connectors.airbyte.com/files/registries/v0/specs_secrets_mask.yaml).

See the GitHub Actions docs on
[workflow commands](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/workflow-commands-for-github-actions#example-masking-an-environment-variable).
"""

from __future__ import annotations

import json
import logging
import os
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal, cast

import requests
import yaml

__all__ = [
    "GLOBAL_MASK_KEYS_URL",
    "get_spec_mask",
    "is_running_in_ci",
    "is_secret_property",
    "print_ci_secret_mask_for_string",
    "print_ci_secret_mask_for_value",
    "print_ci_secrets_masks",
    "print_ci_secrets_masks_for_config",
]

logger = logging.getLogger(__name__)

GLOBAL_MASK_KEYS_URL = (
    "https://connectors.airbyte.com/files/registries/v0/specs_secrets_mask.yaml"
)
"""URL of the canonical list of property names to treat as secrets."""

_SPEC_MASK_FETCH_TIMEOUT_SECONDS = 30
"""Hard upper bound on the spec-mask fetch to prevent hangs in CI."""


def is_running_in_ci() -> bool:
    """Return `True` if the process is running inside a CI environment.

    Detection is by the `CI` env var, which GitHub Actions, GitLab CI,
    CircleCI, and most other CI providers set to a truthy value. An empty
    `CI=""` is treated as non-CI so that developers who accidentally export
    the variable don't get CI-only behavior.
    """
    return bool(os.environ.get("CI"))


def print_ci_secrets_masks(
    secrets_dir: Path,
    *,
    strict_ci_env_check: Literal[True],
) -> None:
    """Emit GitHub `::add-mask::` lines for every secret value under `secrets_dir`.

    Walks each `*.json` file in the directory and recursively masks any value
    whose key matches the global spec-mask list.

    `strict_ci_env_check` is a required keyword-only sentinel that must be
    `True`. It exists to make the CI-env gate visible at every call site:
    this function is a no-op (with a notice on stderr) when `CI` is unset or
    empty, preventing accidental emission of secret values to a developer's
    terminal. The typing of `strict_ci_env_check` guarantees that this gate
    cannot be silently disabled by a caller.
    """
    _ = strict_ci_env_check
    if not is_running_in_ci():
        sys.stderr.write(
            "`print_ci_secrets_masks` is a no-op outside CI; "
            "set `CI` to emit `::add-mask::` lines.\n"
        )
        return
    for secret_file_path in secrets_dir.glob("*.json"):
        config_dict = json.loads(secret_file_path.read_text())
        print_ci_secrets_masks_for_config(config=config_dict)


def print_ci_secret_mask_for_string(value: str) -> None:
    """Emit one `::add-mask::` line per non-empty line in `value`.

    Multi-line values (e.g. PEM private keys) must be masked line-by-line;
    GitHub Actions does not match masks across newlines.

    The explicit `::add-mask::` prefix is required by GitHub Actions so that
    subsequent log output containing these values is redacted in the workflow
    UI. Emitting the raw text to stdout is therefore intentional and local to
    a trusted CI context only.
    """
    for line in value.splitlines():
        line_to_mask = line.strip()
        if line_to_mask:
            sys.stdout.write(f"::add-mask::{line_to_mask}\n")


def print_ci_secret_mask_for_value(value: Any) -> None:
    """Mask a value of any type, recursing into dicts and lists."""
    if isinstance(value, dict):
        for v in value.values():
            print_ci_secret_mask_for_value(v)
        return

    if isinstance(value, list):
        for list_item in value:
            print_ci_secret_mask_for_value(list_item)
        return

    for line in str(value).splitlines():
        if line.strip():
            print_ci_secret_mask_for_string(line)


def print_ci_secrets_masks_for_config(config: dict[str, Any] | list[Any] | Any) -> None:
    """Walk a config tree and mask any secret-valued leaves."""
    if isinstance(config, list):
        for item in config:
            print_ci_secrets_masks_for_config(item)
        return

    if isinstance(config, dict):
        for key, value in config.items():
            if is_secret_property(key):
                logger.debug("Masking secret for config key: %s", key)
                print_ci_secret_mask_for_value(value)
            elif isinstance(value, (dict, list)):
                print_ci_secrets_masks_for_config(value)


def is_secret_property(property_name: str) -> bool:
    """Return `True` if `property_name` should be treated as a secret.

    Matches case-insensitively and substring-wise, so a rule of `password` also
    masks `my_password` and `PASSWORD`.
    """
    names_to_mask: list[str] = get_spec_mask()
    return any(mask.lower() in property_name.lower() for mask in names_to_mask)


@lru_cache
def get_spec_mask() -> list[str]:
    """Fetch and cache the global list of property names to mask.

    Raises on HTTP or parse failure rather than returning an empty list:
    `lru_cache` does not cache exceptions, so a transient CDN error will be
    retried on the next call instead of permanently disabling masking for
    the rest of the process.
    """
    response = requests.get(
        GLOBAL_MASK_KEYS_URL,
        allow_redirects=True,
        timeout=_SPEC_MASK_FETCH_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    parsed = yaml.safe_load(response.content)
    return cast(list[str], parsed["properties"])
