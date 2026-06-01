"""Workspace profiles — multi-environment scoping for Efterlev.

v0.1.166 / #371 introduces named profiles so a single workspace can
support prod / staging / dev (or any other slicing) without losing
the prod report each time the customer scans staging.

## Design

A **profile** bundles overrides for `boundary`, `baseline`, and
`scan.target_dir`. The active profile is selected by the
`EFTERLEV_PROFILE` environment variable. When set, `load_config()`
merges the matching `[profile.<name>]` section over the top-level
config; output paths land under `efterlev-out/profile-<name>/...`
so profiles don't collide.

When `EFTERLEV_PROFILE` is unset (the default), Efterlev behaves
exactly as before v0.1.166. Backward-compatible by construction.

## Activation

Three equivalent ways to select a profile:

  1. `EFTERLEV_PROFILE=prod efterlev report run`
  2. `efterlev report run --profile prod` (sets the env var for the
     subprocess invocations the orchestrator makes)
  3. Set `EFTERLEV_PROFILE=prod` in your shell once

## Why env var, not just a flag

`efterlev report run` is an orchestrator: it shells out to `efterlev
scan`, `efterlev agent gap`, etc. as subprocesses. Threading a
`--profile` flag through every subprocess invocation works but adds
boilerplate to each subcommand definition. The env var rides in
the subprocess environment by default — every subcommand sees the
same active profile without explicit wiring. The `--profile` flag
on `report run` (and on individual subcommands for ad-hoc use) is
sugar that exports the env var first.

## Profile-aware code

Use `get_active_profile()` to read the currently-active profile
(or None). Use the `profile=` parameter on the path helpers
(`reports_dir`, `submissions_dir`, etc.) when constructing
output paths. CLI commands surface a `--profile <name>` flag that
sets the env var for the duration of the command.
"""

from __future__ import annotations

import os
import re

# The env var name. Pin in one place so the CLI's `--profile` flag and
# the path helpers and `load_config` all read the same source of truth.
PROFILE_ENV_VAR = "EFTERLEV_PROFILE"

# Profile names land in directory names + TOML section names. Keep the
# valid character set narrow on purpose — no shell-metachar risk, no
# Windows-path-illegal characters, no accidental newlines.
_VALID_PROFILE_NAME = re.compile(r"^[a-z0-9][a-z0-9_-]{0,30}[a-z0-9]$|^[a-z0-9]$")


class InvalidProfileNameError(ValueError):
    """Raised when a profile name contains disallowed characters."""


def validate_profile_name(name: str) -> str:
    """Return the name unchanged on success; raise on invalid.

    Profile names:
      - lowercase ASCII letters, digits, hyphens, underscores
      - first and last char must be alphanumeric
      - 1-32 characters
      - case-sensitive — `prod` and `Prod` are different names but we
        require lowercase to avoid OS-case-folding surprises (mac is
        case-insensitive by default; linux is case-sensitive)
    """
    if not isinstance(name, str) or not _VALID_PROFILE_NAME.match(name):
        raise InvalidProfileNameError(
            f"profile name {name!r} is invalid; must be 1-32 chars of "
            f"[a-z0-9_-], starting and ending with [a-z0-9]"
        )
    return name


def get_active_profile() -> str | None:
    """Return the active profile name, or None when no profile is set.

    Reads `EFTERLEV_PROFILE` from the process environment. Empty
    string is treated as None (so `EFTERLEV_PROFILE= efterlev ...`
    works as an explicit "no profile" override).

    Validates the name; raises `InvalidProfileNameError` if the env
    var holds an unsupported value. We fail loudly rather than
    silently fall back to no-profile — a typo'd profile name should
    surface immediately, not silently scan the wrong thing.
    """
    raw = os.environ.get(PROFILE_ENV_VAR)
    if not raw:
        return None
    return validate_profile_name(raw)


def profile_output_subdir(profile: str | None) -> str:
    """Return the output-directory segment for a profile, or empty.

    Used by the path helpers in `efterlev.paths` to compute where a
    profile's reports / submissions land. `prod` → `"profile-prod"`;
    `None` → `""` (default top-level output dir, unchanged).

    Pre-validates the name so a corrupted env var doesn't smuggle a
    `..` into a path. Returns the validated, kebab-prefixed form.
    """
    if profile is None:
        return ""
    validate_profile_name(profile)  # raises on garbage
    return f"profile-{profile}"
