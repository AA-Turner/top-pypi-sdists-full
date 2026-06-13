"""SDK configuration resolution: defaults → file → env vars → constructor args."""

from __future__ import annotations

import configparser
import os
from dataclasses import dataclass
from pathlib import Path

from smplkit.errors import Error


# Known config keys and their corresponding environment variables.
_CONFIG_KEYS: dict[str, str] = {
    "api_key": "SMPLKIT_API_KEY",
    "base_domain": "SMPLKIT_BASE_DOMAIN",
    "scheme": "SMPLKIT_SCHEME",
    "environment": "SMPLKIT_ENVIRONMENT",
    "service": "SMPLKIT_SERVICE",
    "debug": "SMPLKIT_DEBUG",
    "telemetry": "SMPLKIT_TELEMETRY",
}

_BOOL_TRUE = frozenset({"true", "1", "yes"})
_BOOL_FALSE = frozenset({"false", "0", "no"})


@dataclass(frozen=True)
class ResolvedConfig:
    """Fully resolved SDK configuration after the 4-step resolution."""

    api_key: str
    base_domain: str
    scheme: str
    # Optional: when absent the SDK sends no environment/service signal and
    # the server derives the environment from the API key (ADR-021 update).
    # Audit/jobs-only customers never need to supply either.
    environment: str | None
    service: str | None
    debug: bool
    telemetry: bool


@dataclass(frozen=True)
class ResolvedClientConfig:
    """Resolved configuration for a product client.

    CRUD operations against the platform are not tied to an environment
    or service, so those fields are not part of the resolved config and
    not required at construction time.
    """

    api_key: str
    base_domain: str
    scheme: str
    debug: bool
    extra_headers: dict[str, str] | None = None


def _parse_bool(value: str, key: str) -> bool:
    """Parse a boolean string value. Raises Error for invalid values."""
    lower = value.strip().lower()
    if lower in _BOOL_TRUE:
        return True
    if lower in _BOOL_FALSE:
        return False
    raise Error(f"Invalid boolean value for {key}: {value!r}. Expected one of: true, false, 1, 0, yes, no")


def _read_config_file(
    profile: str,
    home_dir: Path | None = None,
) -> dict[str, str]:
    """Read ~/.smplkit and return merged [common] + profile values.

    Returns an empty dict if the file doesn't exist or has no relevant sections.
    Raises Error if the named profile section doesn't exist but the file
    has other sections.
    """
    config_path = (home_dir or Path.home()) / ".smplkit"
    if not config_path.is_file():
        return {}

    try:
        parser = configparser.ConfigParser(interpolation=None)
        parser.optionxform = str  # type: ignore[assignment]  # preserve case
        parser.read(config_path)
    except Exception:
        return {}  # Malformed file — skip silently

    values: dict[str, str] = {}

    # Step 1: Load [common] if it exists
    if parser.has_section("common"):
        for key, val in parser.items("common"):
            if val:  # empty values treated as unset
                values[key] = val

    # Step 2: Overlay the selected profile section
    has_profile = parser.has_section(profile)

    if not has_profile:
        # If the file has sections but NOT the requested profile, error
        # unless the file only has [common] (or no sections at all)
        non_common_sections = [s for s in parser.sections() if s != "common"]
        if non_common_sections and profile != "default":
            raise Error(
                f"Profile [{profile}] not found in ~/.smplkit. Available profiles: {', '.join(non_common_sections)}"
            )
        if non_common_sections and profile == "default":
            # default profile missing but other profiles exist — proceed silently
            # (user might only use named profiles with SMPLKIT_PROFILE)
            pass
    else:
        for key, val in parser.items(profile):
            if val:  # empty values treated as unset
                values[key] = val

    return values


def _service_url(scheme: str, subdomain: str, base_domain: str) -> str:
    """Build a service URL: {scheme}://{subdomain}.{base_domain}."""
    return f"{scheme}://{subdomain}.{base_domain}"


def resolve_config(
    *,
    profile: str | None = None,
    api_key: str | None = None,
    base_domain: str | None = None,
    scheme: str | None = None,
    environment: str | None = None,
    service: str | None = None,
    debug: bool | None = None,
    telemetry: bool | None = None,
    _home_dir: Path | None = None,
) -> ResolvedConfig:
    """Resolve SDK configuration using the 4-step algorithm.

    1. SDK hardcoded defaults
    2. Configuration file (~/.smplkit): [common] + selected profile
    3. Environment variables (SMPLKIT_*)
    4. Constructor arguments

    Args:
        _home_dir: Override home directory for testing (not part of public API).
    """
    # Step 1: Hardcoded defaults
    resolved: dict[str, str | bool | None] = {
        "api_key": None,
        "base_domain": "smplkit.com",
        "scheme": "https",
        "environment": None,
        "service": None,
        "debug": False,
        "telemetry": True,
    }

    # Determine profile: constructor arg > SMPLKIT_PROFILE env > "default"
    active_profile = profile or os.environ.get("SMPLKIT_PROFILE") or "default"

    # Step 2: Configuration file
    file_values = _read_config_file(active_profile, home_dir=_home_dir)
    for key in _CONFIG_KEYS:
        if key in file_values:
            val = file_values[key]
            if key in ("debug", "telemetry"):
                resolved[key] = _parse_bool(val, key)
            else:
                resolved[key] = val

    # Step 3: Environment variables
    for key, env_var in _CONFIG_KEYS.items():
        env_val = os.environ.get(env_var, "")
        if env_val:
            if key in ("debug", "telemetry"):
                resolved[key] = _parse_bool(env_val, env_var)
            else:
                resolved[key] = env_val

    # Step 4: Constructor arguments
    constructor_args: dict[str, str | bool | None] = {
        "api_key": api_key,
        "base_domain": base_domain,
        "scheme": scheme,
        "environment": environment,
        "service": service,
        "debug": debug,
        "telemetry": telemetry,
    }
    for key, val in constructor_args.items():
        if val is not None:
            resolved[key] = val

    # Validate required fields.
    #
    # ``environment`` and ``service`` are OPTIONAL: an audit-only or
    # jobs-only customer needs neither, and when ``environment`` is absent
    # the server derives it from the API key (the key can be scoped to an
    # environment). config/flags/logging simply send no environment signal
    # when it's unset. ``api_key`` remains required.
    if not resolved["api_key"]:
        raise Error(
            "No API key provided. Set one of:\n"
            "  1. Pass api_key to the constructor\n"
            "  2. Set the SMPLKIT_API_KEY environment variable\n"
            f"  3. Add api_key to the [{active_profile}] section in ~/.smplkit"
        )

    environment = resolved["environment"]
    service = resolved["service"]
    return ResolvedConfig(
        api_key=str(resolved["api_key"]),
        base_domain=str(resolved["base_domain"]),
        scheme=str(resolved["scheme"]),
        # Preserve None rather than coercing to the literal string "None".
        environment=str(environment) if environment is not None else None,
        service=str(service) if service is not None else None,
        debug=bool(resolved["debug"]),
        telemetry=bool(resolved["telemetry"]),
    )


def resolve_client_config(
    *,
    profile: str | None = None,
    api_key: str | None = None,
    base_domain: str | None = None,
    scheme: str | None = None,
    debug: bool | None = None,
    _home_dir: Path | None = None,
) -> ResolvedClientConfig:
    """Resolve configuration for a product client.

    Mirrors :func:`resolve_config` but skips ``environment`` / ``service``
    requirements — they have no meaning for CRUD operations.
    """
    resolved: dict[str, str | bool | None] = {
        "api_key": None,
        "base_domain": "smplkit.com",
        "scheme": "https",
        "debug": False,
    }

    active_profile = profile or os.environ.get("SMPLKIT_PROFILE") or "default"

    file_values = _read_config_file(active_profile, home_dir=_home_dir)
    for key in ("api_key", "base_domain", "scheme", "debug"):
        if key in file_values:
            val = file_values[key]
            if key == "debug":
                resolved[key] = _parse_bool(val, key)
            else:
                resolved[key] = val

    for key, env_var in (
        ("api_key", "SMPLKIT_API_KEY"),
        ("base_domain", "SMPLKIT_BASE_DOMAIN"),
        ("scheme", "SMPLKIT_SCHEME"),
        ("debug", "SMPLKIT_DEBUG"),
    ):
        env_val = os.environ.get(env_var, "")
        if env_val:
            if key == "debug":
                resolved[key] = _parse_bool(env_val, env_var)
            else:
                resolved[key] = env_val

    constructor_args: dict[str, str | bool | None] = {
        "api_key": api_key,
        "base_domain": base_domain,
        "scheme": scheme,
        "debug": debug,
    }
    for key, val in constructor_args.items():
        if val is not None:
            resolved[key] = val

    if not resolved["api_key"]:
        raise Error(
            "No API key provided. Set one of:\n"
            "  1. Pass api_key to the constructor\n"
            "  2. Set the SMPLKIT_API_KEY environment variable\n"
            f"  3. Add api_key to the [{active_profile}] section in ~/.smplkit"
        )

    return ResolvedClientConfig(
        api_key=str(resolved["api_key"]),
        base_domain=str(resolved["base_domain"]),
        scheme=str(resolved["scheme"]),
        debug=bool(resolved["debug"]),
    )
