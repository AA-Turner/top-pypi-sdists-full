"""Closed vocabularies + detection for CLI command performance telemetry.

Shared wire contract for the ``runlayer.cli.command.*`` OTel metrics recorded by
the backend relay (see ``command_metrics.py`` for the client emitter and
``backend/app/core/observability/cli_command_metrics.py`` for the backend
mirror + validator). The two copies are kept in lockstep by
``backend/app/tests/core/observability/test_cli_command_contract.py``.

Everything here is untrusted-input-safe, and depends only on the stdlib plus
the RE2 ``regex_safe`` wrapper, so it stays importable
inside the ``aiwatch`` PyInstaller bundle and on the latency-sensitive
``build_envelope`` path (see ``flow_contract.py``).
"""

from __future__ import annotations

import sys

from runlayer_cli import regex_safe

# Closed command vocabulary. ``argv`` is sanitized to one of these values (or
# ``other``); the backend validates the reported command against the same set
# before it becomes a Sentry tag. Keep in lockstep with the backend mirror.
COMMAND_VOCAB: frozenset[str] = frozenset(
    {
        # top-level commands (full `runlayer` CLI + `aiwatch` binary)
        "run",
        "doctor",
        "login",
        "logout",
        "logs",
        "status",
        "update",
        "update-now",
        "self-update",
        "cache",
        "config",
        "catalog",
        "credentials",
        "deploy",
        "hooks",
        "keychain",
        "org-api-key",
        "setup",
        "scan",
        "skills",
        "plugins",
        "terraform",
        "enroll",
        "bootstrap",
        "daemon",
        "version",
        # notable subcommands (command.subcommand); low-cardinality on purpose
        "plugins.install",
        "plugins.uninstall",
        "plugins.list",
        "skills.install",
        "skills.list",
        "config.show",
        "config.sync",
        "setup.config",
        "setup.hooks",
        "hooks.relay",
        "keychain.adopt",
        "org-api-key.list",
        "org-api-key.create",
        "org-api-key.remove",
        # hook operations, re-emitted from the backend client_flows piggyback
        "hook.pre_tool",
        "hook.post_tool",
        "hook.stop",
        "hook.event",
        # unknown / unmatched
        "other",
    }
)

# Which binary/distribution produced the event.
SOURCES: frozenset[str] = frozenset(
    {
        "aiwatch-binary",
        "runlayer-binary",
        "runlayer-pypi",
    }
)

# Coarse OS family.
OS_VALUES: frozenset[str] = frozenset({"darwin", "windows", "linux"})

STATUSES: frozenset[str] = frozenset({"ok", "error"})

# Exception class name only (no messages/args) per the no-PII tag contract in
# backend/app/core/observability/sentry/AGENTS.md.
ERROR_TYPE_RE = regex_safe.compile(r"^[A-Za-z_][A-Za-z0-9_.]{0,80}$")

# Global options (and their values) skipped when finding the command token.
_VALUE_OPTIONS: frozenset[str] = frozenset(
    {"--host", "-H", "--secret", "-s", "--org-api-key", "--ca-bundle"}
)

_TOP_LEVEL_COMMANDS: frozenset[str] = frozenset(
    c for c in COMMAND_VOCAB if "." not in c and c not in {"other", "version"}
)

_UUID_RE = regex_safe.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    regex_safe.IGNORECASE,
)


def sanitize_command(argv: list[str]) -> str:
    """Map a process ``argv`` to a closed-vocab command path.

    Best-effort argv parse: skips the program name, global value-taking options
    (and their values), and boolean flags, then reads up to two positionals as
    ``command`` / ``command.subcommand``. A leading UUID (legacy
    ``runlayer <uuid>``) maps to ``run``. Unknown commands collapse to
    ``other``; a bare invocation with ``--version`` maps to ``version``.
    """
    tokens = argv[1:]
    positionals: list[str] = []
    saw_version_flag = False
    i = 0
    while i < len(tokens) and len(positionals) < 2:
        token = tokens[i]
        if token in {"--version", "-v"}:
            saw_version_flag = True
            i += 1
            continue
        if token in _VALUE_OPTIONS:
            i += 2  # skip the option and its value
            continue
        if token.startswith("-"):
            i += 1
            continue
        positionals.append(token)
        i += 1

    if not positionals:
        return "version" if saw_version_flag else "other"

    command = positionals[0]
    if _UUID_RE.match(command):
        return "run"
    if command not in _TOP_LEVEL_COMMANDS:
        return "other"
    if len(positionals) >= 2:
        subcommand = f"{command}.{positionals[1]}"
        if subcommand in COMMAND_VOCAB:
            return subcommand
    return command


def detect_os() -> str:
    """Coarse OS family for tagging (``darwin`` / ``windows`` / ``linux``)."""
    platform_name = sys.platform
    if platform_name == "darwin":
        return "darwin"
    if platform_name == "win32":
        return "windows"
    if platform_name.startswith("linux"):
        return "linux"
    return "other"


def detect_os_version() -> str | None:
    """Coarse OS version (major only) to keep tag cardinality bounded."""
    try:
        import platform  # noqa: PLC0415 - stdlib, deferred to keep import cheap

        if sys.platform == "darwin":
            mac_version = platform.mac_ver()[0]
            return mac_version.split(".")[0] if mac_version else None
        release = platform.release()
        return release.split(".")[0] if release else None
    except Exception:
        return None


def detect_source() -> str:
    """Which binary/distribution is running (``sys.frozen`` + aiwatch runtime)."""
    from runlayer_cli.runtime import (
        is_aiwatch_runtime,  # noqa: PLC0415 - avoid import cycle
    )

    if is_aiwatch_runtime():
        return "aiwatch-binary"
    if getattr(sys, "frozen", False):
        return "runlayer-binary"
    return "runlayer-pypi"
