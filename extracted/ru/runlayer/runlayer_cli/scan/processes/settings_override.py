"""Extract and transform settings-override flags from raw client process argv.

The extractor intentionally operates before process argv redaction so PHASE 12
can read explicitly referenced MCP config files. Raw values remain local; only
sanitized values are added to process sightings.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol, Sequence

from runlayer_cli.scan.agents.redact import sanitize_path
from runlayer_cli.scan.processes.models import (
    MAX_SETTINGS_OVERRIDE_VALUE_LENGTH,
    MAX_SETTINGS_OVERRIDES_PER_PROCESS,
    OverrideConfigRef,
    ProcessCandidate,
    SettingsOverridePayload,
)


class SettingsOverrideFlagSpec(Protocol):
    """Duck-typed subset of the client registry's override flag spec."""

    flag: str
    takes_value: bool
    mcp_config: Literal["none", "file", "user_data_dir"]
    variadic: bool


@dataclass(frozen=True)
class SettingsOverrideMatch:
    """One settings-override flag occurrence in process argv."""

    flag: str
    value: str | None
    inline_json: bool
    mcp_config: Literal["none", "file", "user_data_dir"]


def extract_settings_overrides(
    argv: Sequence[str],
    specs: Sequence[SettingsOverrideFlagSpec],
) -> list[SettingsOverrideMatch]:
    """Return recognized override flags in argv order, preserving repeats."""

    specs_by_flag = {spec.flag: spec for spec in specs}
    matches: list[SettingsOverrideMatch] = []
    index = 0
    while index < len(argv):
        argument = argv[index]
        flag, separator, equals_value = argument.partition("=")
        spec = specs_by_flag.get(flag)
        if spec is None:
            index += 1
            continue

        values: list[str | None] = [None]
        if spec.takes_value:
            if separator:
                values = [equals_value or None]
            elif spec.variadic:
                values_end = index + 1
                while values_end < len(argv) and not argv[values_end].startswith("--"):
                    values_end += 1
                values.clear()
                values.extend(argv[index + 1 : values_end])
                if not values:
                    values.append(None)
                index = values_end - 1
            elif index + 1 < len(argv) and not argv[index + 1].startswith("--"):
                index += 1
                values = [argv[index]]

        matches.extend(
            SettingsOverrideMatch(
                flag=spec.flag,
                value=value,
                inline_json=bool(value and value.lstrip().startswith("{")),
                mcp_config=spec.mcp_config,
            )
            for value in values
        )
        index += 1

    return matches


def sanitized_settings_overrides(
    matches: Sequence[SettingsOverrideMatch],
    *,
    usernames: Sequence[str],
) -> list[SettingsOverridePayload]:
    """Build bounded, redacted process-sighting evidence."""

    overrides: list[SettingsOverridePayload] = []
    for match in matches[:MAX_SETTINGS_OVERRIDES_PER_PROCESS]:
        sanitized_value = (
            None
            if match.inline_json
            else sanitize_path(match.value, usernames=usernames)
        )
        if sanitized_value is not None:
            sanitized_value = sanitized_value[:MAX_SETTINGS_OVERRIDE_VALUE_LENGTH]
        overrides.append({"flag": match.flag, "value": sanitized_value})
    return overrides


def override_config_refs(
    candidate: ProcessCandidate,
    client_name: str | None,
    matches: Sequence[SettingsOverrideMatch],
) -> list[OverrideConfigRef]:
    """Build bounded local-only config refs from parseable override values."""

    if client_name is None:
        return []

    refs: list[OverrideConfigRef] = []
    for match in matches[:MAX_SETTINGS_OVERRIDES_PER_PROCESS]:
        kind = match.mcp_config
        if kind == "none" or match.value is None or match.inline_json:
            continue
        refs.append(
            OverrideConfigRef(
                client=client_name,
                flag=match.flag,
                value=match.value,
                mcp_config=kind,
                pid=candidate.pid,
                user=candidate.user,
                cwd=candidate.cwd,
                wsl_distro=candidate.wsl_distro,
            )
        )
    return refs
