"""Tests for `efterlev.profile` + multi-environment path scoping.

v0.1.166 / #371 — workspace profiles. The active profile is selected
by the `EFTERLEV_PROFILE` environment variable; path helpers and
`load_config` both read it.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from efterlev.paths import (
    inventory_dir,
    oscal_dir,
    output_root,
    poam_dir,
    reports_dir,
    submissions_dir,
    vdr_dir,
)
from efterlev.profile import (
    PROFILE_ENV_VAR,
    InvalidProfileNameError,
    get_active_profile,
    profile_output_subdir,
    validate_profile_name,
)

# --- validate_profile_name -----------------------------------------------


def test_validate_accepts_lowercase_alphanumeric() -> None:
    assert validate_profile_name("prod") == "prod"
    assert validate_profile_name("staging") == "staging"
    assert validate_profile_name("a") == "a"
    assert validate_profile_name("env123") == "env123"


def test_validate_accepts_hyphens_and_underscores_in_middle() -> None:
    assert validate_profile_name("us-east-1") == "us-east-1"
    assert validate_profile_name("prod_west") == "prod_west"


def test_validate_rejects_uppercase() -> None:
    """Mac is case-insensitive by default; lowercase only avoids
    filesystem-collision surprises across platforms."""
    with pytest.raises(InvalidProfileNameError, match="invalid"):
        validate_profile_name("Prod")
    with pytest.raises(InvalidProfileNameError):
        validate_profile_name("PROD")


def test_validate_rejects_special_chars() -> None:
    for bad in ["prod.env", "prod env", "prod/env", "prod..", "../etc/passwd"]:
        with pytest.raises(InvalidProfileNameError):
            validate_profile_name(bad)


def test_validate_rejects_leading_or_trailing_dash() -> None:
    with pytest.raises(InvalidProfileNameError):
        validate_profile_name("-prod")
    with pytest.raises(InvalidProfileNameError):
        validate_profile_name("prod-")


def test_validate_rejects_too_long_name() -> None:
    too_long = "a" * 33
    with pytest.raises(InvalidProfileNameError):
        validate_profile_name(too_long)


def test_validate_rejects_empty_string() -> None:
    with pytest.raises(InvalidProfileNameError):
        validate_profile_name("")


# --- get_active_profile --------------------------------------------------


def test_active_profile_none_when_env_unset(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(PROFILE_ENV_VAR, raising=False)
    assert get_active_profile() is None


def test_active_profile_none_when_env_empty_string(monkeypatch: pytest.MonkeyPatch) -> None:
    """Explicit empty-string override = "no profile" rather than error.
    Lets a caller turn off an inherited env var."""
    monkeypatch.setenv(PROFILE_ENV_VAR, "")
    assert get_active_profile() is None


def test_active_profile_returns_validated_name(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(PROFILE_ENV_VAR, "prod")
    assert get_active_profile() == "prod"


def test_active_profile_raises_on_invalid_env_value(monkeypatch: pytest.MonkeyPatch) -> None:
    """Typo'd profile name should surface immediately, not silently
    fall back to no-profile."""
    monkeypatch.setenv(PROFILE_ENV_VAR, "../etc/passwd")
    with pytest.raises(InvalidProfileNameError):
        get_active_profile()


# --- profile_output_subdir ----------------------------------------------


def test_subdir_empty_for_none() -> None:
    """No profile → empty subdir → output paths stay at backward-
    compatible default (no `profile-<name>` segment)."""
    assert profile_output_subdir(None) == ""


def test_subdir_prefixed_with_profile_kebab() -> None:
    """The `profile-<name>` prefix is load-bearing — it's what keeps
    profiled output from colliding with un-profiled output in the same
    workspace."""
    assert profile_output_subdir("prod") == "profile-prod"
    assert profile_output_subdir("us-east-1") == "profile-us-east-1"


def test_subdir_validates_name_to_prevent_path_traversal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A corrupted env var must not smuggle `..` into a path."""
    with pytest.raises(InvalidProfileNameError):
        profile_output_subdir("../escape")


# --- path helpers scope to active profile -------------------------------


def test_paths_default_when_no_profile_active(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Backward compat: with no profile, paths are exactly what
    v0.1.160-v0.1.165 produced."""
    monkeypatch.delenv(PROFILE_ENV_VAR, raising=False)
    assert output_root(tmp_path) == tmp_path / "efterlev-out"
    assert reports_dir(tmp_path) == tmp_path / "efterlev-out" / "reports"
    assert submissions_dir(tmp_path) == tmp_path / "efterlev-out" / "submissions"
    assert poam_dir(tmp_path) == tmp_path / "efterlev-out" / "reports" / "poam"
    assert oscal_dir(tmp_path) == tmp_path / "efterlev-out" / "reports" / "oscal"
    assert vdr_dir(tmp_path) == tmp_path / "efterlev-out" / "reports" / "vdr"
    assert inventory_dir(tmp_path) == tmp_path / "efterlev-out" / "reports" / "inventory"


def test_paths_scope_to_active_profile_from_env(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """When EFTERLEV_PROFILE is set, every path helper auto-scopes."""
    monkeypatch.setenv(PROFILE_ENV_VAR, "prod")
    assert output_root(tmp_path) == tmp_path / "efterlev-out" / "profile-prod"
    assert reports_dir(tmp_path) == tmp_path / "efterlev-out" / "profile-prod" / "reports"
    assert submissions_dir(tmp_path) == tmp_path / "efterlev-out" / "profile-prod" / "submissions"
    assert poam_dir(tmp_path) == tmp_path / "efterlev-out" / "profile-prod" / "reports" / "poam"
    assert oscal_dir(tmp_path) == tmp_path / "efterlev-out" / "profile-prod" / "reports" / "oscal"
    assert vdr_dir(tmp_path) == tmp_path / "efterlev-out" / "profile-prod" / "reports" / "vdr"
    assert (
        inventory_dir(tmp_path)
        == tmp_path / "efterlev-out" / "profile-prod" / "reports" / "inventory"
    )


def test_paths_explicit_profile_arg_overrides_env(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Explicit `profile=` always wins over the env var. Lets a caller
    explicitly target prod even when staging is the ambient default."""
    monkeypatch.setenv(PROFILE_ENV_VAR, "staging")
    assert (
        reports_dir(tmp_path, profile="prod")
        == tmp_path / "efterlev-out" / "profile-prod" / "reports"
    )


def test_paths_two_profiles_dont_collide(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The whole point of profiles: prod and staging produce distinct
    output directories so they don't overwrite each other."""
    monkeypatch.delenv(PROFILE_ENV_VAR, raising=False)
    prod = reports_dir(tmp_path, profile="prod")
    staging = reports_dir(tmp_path, profile="staging")
    assert prod != staging
    assert "profile-prod" in str(prod)
    assert "profile-staging" in str(staging)


# --- iter_report_dirs profile-awareness ---------------------------------


def test_iter_report_dirs_includes_unprofiled_when_profile_active(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """When a profile is active, readers walk: profile-scoped (where new
    writes land), unprofiled (artifacts from before the profile was
    active), legacy (pre-v0.1.160). Mtime decides; never miss an old
    artifact just because the customer recently switched profiles."""
    from efterlev.paths import iter_report_dirs

    monkeypatch.setenv(PROFILE_ENV_VAR, "prod")
    dirs = iter_report_dirs(tmp_path)
    assert tmp_path / "efterlev-out" / "profile-prod" / "reports" in dirs
    assert tmp_path / "efterlev-out" / "reports" in dirs
    assert tmp_path / ".efterlev" / "reports" in dirs


def test_iter_report_dirs_no_profile_keeps_v0_1_160_behavior(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from efterlev.paths import iter_report_dirs

    monkeypatch.delenv(PROFILE_ENV_VAR, raising=False)
    dirs = iter_report_dirs(tmp_path)
    # Backward compat: only the v0.1.160 layout (new + legacy).
    assert dirs == [
        tmp_path / "efterlev-out" / "reports",
        tmp_path / ".efterlev" / "reports",
    ]
