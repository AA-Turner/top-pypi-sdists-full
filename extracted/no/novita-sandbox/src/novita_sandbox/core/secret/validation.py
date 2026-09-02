"""Validation helpers shared by sandbox secret APIs."""

from __future__ import annotations

import re
from typing import Dict, List, Mapping, Optional, Sequence

from novita_sandbox.core.exceptions import InvalidArgumentException

_SECRET_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_ENV_NAME_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_HOST_PATTERN = re.compile(
    r"^(\*\.)?[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*$"
)


def validate_secret_name(name: str) -> None:
    if not isinstance(name, str) or not _SECRET_NAME_PATTERN.match(name):
        raise InvalidArgumentException(
            f"secret name {name!r} must be 1-128 characters and contain only letters, numbers, dots, underscores, and hyphens"
        )


def normalize_secret_hosts(hosts: Sequence[str]) -> List[str]:
    if not hosts:
        raise InvalidArgumentException("hosts is required")

    seen = set()
    normalized_hosts = []
    for raw_host in hosts:
        if not isinstance(raw_host, str):
            raise InvalidArgumentException("host must be a string")

        host = raw_host.strip().lower()
        if not host:
            raise InvalidArgumentException("host cannot be empty")
        if "://" in host or any(char in host for char in "/?#@:"):
            raise InvalidArgumentException(f"host {host!r} must be a hostname only")

        wildcard = host.startswith("*.")
        lookup_host = host[2:] if wildcard else host
        if not lookup_host or "*" in lookup_host:
            raise InvalidArgumentException(f"invalid host {host!r}")

        try:
            ascii_host = lookup_host.encode("idna").decode("ascii")
        except UnicodeError as exc:
            raise InvalidArgumentException(f"invalid host {host!r}") from exc

        normalized = f"*.{ascii_host}" if wildcard else ascii_host
        if not _HOST_PATTERN.match(normalized):
            raise InvalidArgumentException(
                f"host {host!r} must be a hostname or wildcard hostname"
            )
        if normalized in seen:
            continue

        seen.add(normalized)
        normalized_hosts.append(normalized)

    return normalized_hosts


def validate_secret_envs(
    secret_envs: Optional[Mapping[str, str]],
    envs: Optional[Mapping[str, str]] = None,
) -> Dict[str, str]:
    if secret_envs is None:
        return {}

    if not isinstance(secret_envs, Mapping):
        raise InvalidArgumentException("secret_envs must be a mapping")
    if not secret_envs:
        return {}

    env_names = set(envs or {})
    validated = {}
    for env_name, secret_name in secret_envs.items():
        if not isinstance(env_name, str) or not _ENV_NAME_PATTERN.match(env_name):
            raise InvalidArgumentException(
                f"secret_envs key {env_name!r} must be a valid sandbox environment variable name"
            )
        if env_name in env_names:
            raise InvalidArgumentException(
                f"envs and secret_envs both define {env_name!r}"
            )

        validate_secret_name(secret_name)
        validated[env_name] = secret_name

    return validated
