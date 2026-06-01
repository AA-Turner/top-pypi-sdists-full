"""Tests for `efterlev doctor` (Priority 3).

The doctor checks are pure functions over environment + filesystem
state, easy to unit-test by manipulating env vars and tmp_path.
The CLI command tests live below alongside.
"""

from __future__ import annotations

import time
from pathlib import Path

import pytest
from typer.testing import CliRunner

from efterlev.cli.doctor import (
    Check,
    check_anthropic_api_key,
    check_bedrock_credentials,
    check_efterlev_dir,
    check_frmr_cache,
    check_python_version,
    has_failures,
    run_doctor_checks,
)
from efterlev.cli.main import app

runner = CliRunner()


# --- check_python_version --------------------------------------------------


def test_python_version_passes_on_supported_python() -> None:
    """Tests run on Python ≥3.10 by definition (pyproject.toml gates this)."""
    c = check_python_version()
    assert c.status == "pass"
    assert "Python" in c.detail


# --- check_anthropic_api_key ----------------------------------------------


def test_anthropic_api_key_warns_when_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    c = check_anthropic_api_key()
    assert c.status == "warn"
    assert "is not set" in c.detail
    assert c.hint is not None
    assert "console.anthropic.com" in c.hint


def test_anthropic_api_key_warns_on_wrong_shape(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "wrong_prefix_xxxxx")
    c = check_anthropic_api_key()
    assert c.status == "warn"
    assert "doesn't start with 'sk-ant-'" in c.detail


def test_anthropic_api_key_passes_on_realistic_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-" + "x" * 100)
    c = check_anthropic_api_key()
    assert c.status == "pass"
    assert "sk-ant-" in c.detail


# --- check_efterlev_dir ---------------------------------------------------


def test_efterlev_dir_passes_when_dir_exists(tmp_path: Path) -> None:
    (tmp_path / ".efterlev").mkdir()
    c = check_efterlev_dir(tmp_path)
    assert c.status == "pass"


def test_efterlev_dir_warns_when_missing(tmp_path: Path) -> None:
    c = check_efterlev_dir(tmp_path)
    assert c.status == "warn"
    assert "not initialized" in c.detail
    assert c.hint is not None
    assert "efterlev init" in c.hint


# --- check_frmr_cache -----------------------------------------------------


def test_frmr_cache_passes_when_recent(tmp_path: Path) -> None:
    cache = tmp_path / ".efterlev" / "cache" / "frmr_document.json"
    cache.parent.mkdir(parents=True)
    cache.write_text("{}", encoding="utf-8")
    c = check_frmr_cache(tmp_path)
    assert c.status == "pass"


def test_frmr_cache_warns_when_missing(tmp_path: Path) -> None:
    c = check_frmr_cache(tmp_path)
    assert c.status == "warn"
    assert "missing" in c.detail
    assert c.hint is not None
    assert "efterlev init" in c.hint


def test_frmr_cache_warns_when_stale(tmp_path: Path) -> None:
    cache = tmp_path / ".efterlev" / "cache" / "frmr_document.json"
    cache.parent.mkdir(parents=True)
    cache.write_text("{}", encoding="utf-8")
    # Force mtime to 100 days ago.
    old = time.time() - 100 * 86400
    cache.touch()
    import os

    os.utime(cache, (old, old))
    c = check_frmr_cache(tmp_path)
    assert c.status == "warn"
    assert "days old" in c.detail


# --- check_bedrock_credentials --------------------------------------------


def _patch_boto_session_creds(
    monkeypatch: pytest.MonkeyPatch,
    creds_obj: object | None,
    *,
    region_name: str | None = None,
) -> None:
    """Force `boto3.Session().get_credentials()` to return a stub.

    The doctor uses boto3's full credential chain (env, shared file,
    profile, IMDS, SSO) instead of just env vars. Tests can't rely on
    env-var-only stubbing anymore — they need to control what the
    chain reports.

    `region_name` controls what `Session.region_name` returns — boto3's
    own resolution chain pulls from `~/.aws/config`'s profile region
    when env vars are unset. v0.1.8 doctor reads this; tests can pass
    None (no profile region) or a region string.
    """
    import boto3

    class _FakeSession:
        @property
        def region_name(self) -> str | None:
            return region_name

        def get_credentials(self) -> object | None:
            return creds_obj

    monkeypatch.setattr(boto3, "Session", lambda *a, **kw: _FakeSession())


def test_bedrock_credentials_warn_when_no_creds_resolvable(monkeypatch: pytest.MonkeyPatch) -> None:
    """No env vars and no shared-credential file → boto3 returns None."""
    for var in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_PROFILE", "AWS_REGION"):
        monkeypatch.delenv(var, raising=False)
    _patch_boto_session_creds(monkeypatch, None)
    c = check_bedrock_credentials()
    assert c.status == "warn"
    assert "No AWS credentials resolvable" in c.detail


def test_bedrock_credentials_warn_when_no_region(monkeypatch: pytest.MonkeyPatch) -> None:
    """Creds resolve from ANY source, but region is unset."""
    monkeypatch.delenv("AWS_REGION", raising=False)
    monkeypatch.delenv("AWS_DEFAULT_REGION", raising=False)
    _patch_boto_session_creds(monkeypatch, object())  # truthy stand-in for a Credentials object
    c = check_bedrock_credentials()
    assert c.status == "warn"
    assert "no region configured" in c.detail


def test_bedrock_credentials_pass_when_creds_resolve_via_shared_file(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Real-world fix: `~/.aws/credentials` + `aws configure set region` are
    the canonical install pattern. Earlier env-var-only logic false-warned
    on this path even though boto3's runtime client used those creds fine.
    """
    for var in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_PROFILE"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("AWS_REGION", "us-gov-west-1")
    _patch_boto_session_creds(monkeypatch, object())  # creds came from ~/.aws/credentials
    c = check_bedrock_credentials()
    assert c.status == "pass"
    assert "Bedrock backend usable" in c.detail


def test_bedrock_credentials_pass_when_region_resolved_from_aws_config_file(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """v0.1.8: when AWS_REGION isn't set in env but `aws configure set region`
    has written it to `~/.aws/config`, boto3 resolves the region via the
    profile chain. The doctor should mirror — pre-v0.1.8 it false-warned
    'no region configured' even though the runtime worked fine.
    """
    for var in (
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_PROFILE",
        "AWS_REGION",
        "AWS_DEFAULT_REGION",
    ):
        monkeypatch.delenv(var, raising=False)
    # Creds + region BOTH come from ~/.aws/* — env is empty but session
    # exposes them via the resolution chain.
    _patch_boto_session_creds(monkeypatch, object(), region_name="us-east-1")
    c = check_bedrock_credentials()
    assert c.status == "pass"
    assert "Bedrock backend usable" in c.detail


def test_bedrock_credentials_pass_with_profile_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AWS_ACCESS_KEY_ID", raising=False)
    monkeypatch.delenv("AWS_SECRET_ACCESS_KEY", raising=False)
    monkeypatch.setenv("AWS_PROFILE", "govcloud")
    monkeypatch.setenv("AWS_REGION", "us-gov-west-1")
    _patch_boto_session_creds(monkeypatch, object())
    c = check_bedrock_credentials()
    assert c.status == "pass"


def test_anthropic_api_key_skipped_when_backend_is_bedrock(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Workspaces configured for Bedrock shouldn't generate noise about a
    missing Anthropic key — that path doesn't use one.
    """
    from efterlev.cli.doctor import check_anthropic_api_key

    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    c = check_anthropic_api_key(configured_backend="bedrock")
    assert c.status == "pass"
    assert "skipped" in c.detail.lower()


def test_anthropic_api_key_skipped_when_backend_is_claude_code(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """v0.1.175 / #381: claude_code (subscription) uses OAuth via
    `claude --print` and efterlev strips ANTHROPIC_API_KEY from that
    subprocess — so doctor must NOT nag a subscription user about a
    missing/odd key (it read as 'it still wants the API key')."""
    from efterlev.cli.doctor import check_anthropic_api_key

    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    c = check_anthropic_api_key(configured_backend="claude_code")
    assert c.status == "pass"
    assert "skipped" in c.detail.lower()
    # Even a wrong-shape stray key (the sk-proj- footgun) must not warn.
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-proj-bogus")
    c2 = check_anthropic_api_key(configured_backend="claude_code")
    assert c2.status == "pass"


# --- v0.1.9: installer detection in bedrock_credentials hint ---


def test_bedrock_install_hint_uv_path(monkeypatch: pytest.MonkeyPatch) -> None:
    """v0.1.9: when efterlev was installed via `uv tool install`, the
    boto3-missing hint must point at `uv tool install --reinstall
    'efterlev[bedrock]'`, NOT at `pipx inject` (which silently fails for
    uv-managed venvs)."""
    import sys

    from efterlev.cli.doctor import _bedrock_install_hint

    monkeypatch.setattr(sys, "executable", "/Users/u/.local/share/uv/tools/efterlev/bin/python")
    hint = _bedrock_install_hint()
    assert "uv tool install --reinstall" in hint
    assert "pipx inject" not in hint


def test_bedrock_install_hint_pipx_path(monkeypatch: pytest.MonkeyPatch) -> None:
    """pipx-installed efterlev gets the pipx-shaped hint."""
    import sys

    from efterlev.cli.doctor import _bedrock_install_hint

    monkeypatch.setattr(sys, "executable", "/Users/u/.local/pipx/venvs/efterlev/bin/python")
    hint = _bedrock_install_hint()
    assert "pipx install" in hint or "pipx inject" in hint
    assert "uv tool install" not in hint


def test_bedrock_install_hint_generic_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    """System / container / pip-installed efterlev gets the generic hint."""
    import sys

    from efterlev.cli.doctor import _bedrock_install_hint

    monkeypatch.setattr(sys, "executable", "/usr/local/bin/python3.12")
    hint = _bedrock_install_hint()
    assert "pip install" in hint
    assert "uv tool" not in hint
    assert "pipx" not in hint


# --- run_doctor_checks aggregator -----------------------------------------


def test_run_doctor_checks_returns_all_categories(tmp_path: Path) -> None:
    """All 9 checks run in a defined order (cloudformation_templates added
    v0.1.84; openai_api_key added v0.1.211 alongside the OpenAI backend)."""
    (tmp_path / ".efterlev").mkdir()
    checks = run_doctor_checks(tmp_path)
    names = [c.name for c in checks]
    assert names == [
        "python_version",
        "install_uniqueness",
        "efterlev_dir",
        "frmr_cache",
        "anthropic_api_key",
        "openai_api_key",
        "bedrock_credentials",
        "boundary_declared",
        "cloudformation_templates",
    ]


def test_check_install_uniqueness_warns_on_multiple_path_binaries(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """G2 (v0.1.14): two `efterlev` binaries on PATH from custom installs
    (e.g. `/usr/local/bin/efterlev` + `~/.local/bin/efterlev`)."""
    from efterlev.cli.doctor import check_install_uniqueness

    a_dir = tmp_path / "a"
    b_dir = tmp_path / "b"
    a_dir.mkdir()
    b_dir.mkdir()
    (a_dir / "efterlev").write_text("#!/bin/sh\necho a\n")
    (b_dir / "efterlev").write_text("#!/bin/sh\necho b\n")
    (a_dir / "efterlev").chmod(0o755)
    (b_dir / "efterlev").chmod(0o755)
    monkeypatch.setenv("PATH", f"{a_dir}:{b_dir}")
    monkeypatch.setenv("HOME", str(tmp_path / "empty_home"))  # no manager dirs

    result = check_install_uniqueness()
    assert result.status == "warn"
    assert "2 parallel" in result.detail
    assert str(a_dir / "efterlev") in result.detail
    assert str(b_dir / "efterlev") in result.detail


def test_check_install_uniqueness_passes_on_single(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Single install on PATH (no manager dirs) is the green case."""
    from efterlev.cli.doctor import check_install_uniqueness

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    (bin_dir / "efterlev").write_text("#!/bin/sh\necho ok\n")
    (bin_dir / "efterlev").chmod(0o755)
    monkeypatch.setenv("PATH", str(bin_dir))
    monkeypatch.setenv("HOME", str(tmp_path / "empty_home"))

    result = check_install_uniqueness()
    assert result.status == "pass"
    assert "single `efterlev` on PATH" in result.detail


def test_check_install_uniqueness_dedups_symlinked_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Two PATH entries pointing at the same target via different symlink
    chains shouldn't double-count — guards against false-positive on
    setups like `/usr/local/bin → /opt/bin`."""
    from efterlev.cli.doctor import check_install_uniqueness

    real_dir = tmp_path / "real"
    real_dir.mkdir()
    (real_dir / "efterlev").write_text("#!/bin/sh\necho ok\n")
    (real_dir / "efterlev").chmod(0o755)
    link_dir = tmp_path / "link"
    link_dir.symlink_to(real_dir)
    monkeypatch.setenv("PATH", f"{real_dir}:{link_dir}")
    monkeypatch.setenv("HOME", str(tmp_path / "empty_home"))

    result = check_install_uniqueness()
    assert result.status == "pass"


def test_check_install_uniqueness_detects_pipx_and_uv_tool_managers(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """H1 (v0.1.15): the dominant footgun. pipx and uv tool both have
    venvs but only one of them owns the `~/.local/bin/efterlev` symlink.
    PATH-only walk (v0.1.14 G2) misses this. The new manager-metadata
    walk catches it."""
    from efterlev.cli.doctor import check_install_uniqueness

    home = tmp_path / "home"
    # pipx venv + uv tool dir present; PATH symlink only points at one.
    pipx_venv = home / ".local" / "pipx" / "venvs" / "efterlev"
    pipx_venv.mkdir(parents=True)
    uv_tool = home / ".local" / "share" / "uv" / "tools" / "efterlev"
    uv_tool.mkdir(parents=True)
    bin_dir = home / ".local" / "bin"
    bin_dir.mkdir(parents=True)
    # The PATH symlink — winner is uv tool.
    (uv_tool / "bin").mkdir()
    (uv_tool / "bin" / "efterlev").write_text("#!/bin/sh\necho uv\n")
    (uv_tool / "bin" / "efterlev").chmod(0o755)
    (bin_dir / "efterlev").symlink_to(uv_tool / "bin" / "efterlev")

    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("PATH", str(bin_dir))

    result = check_install_uniqueness()
    assert result.status == "warn", result.detail
    # Both managers named in the detail.
    assert "pipx" in result.detail
    assert "uv tool" in result.detail
    # Hint surfaces both uninstall commands.
    assert result.hint is not None
    assert "pipx uninstall efterlev" in result.hint
    assert "uv tool uninstall efterlev" in result.hint


def test_check_install_uniqueness_does_not_double_count_path_under_manager(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A PATH binary that resolves under a known manager dir is the same
    install as the manager — don't double-count. Otherwise a single
    pipx install + the corresponding ~/.local/bin shim would get
    flagged as 'two installs'."""
    from efterlev.cli.doctor import check_install_uniqueness

    home = tmp_path / "home"
    pipx_venv = home / ".local" / "pipx" / "venvs" / "efterlev"
    pipx_bin = pipx_venv / "bin"
    pipx_bin.mkdir(parents=True)
    (pipx_bin / "efterlev").write_text("#!/bin/sh\necho pipx\n")
    (pipx_bin / "efterlev").chmod(0o755)
    bin_dir = home / ".local" / "bin"
    bin_dir.mkdir(parents=True)
    # PATH shim is a symlink into the pipx venv — same install.
    (bin_dir / "efterlev").symlink_to(pipx_bin / "efterlev")

    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("PATH", str(bin_dir))

    result = check_install_uniqueness()
    assert result.status == "pass", result.detail
    assert "pipx" in result.detail


def test_has_failures_only_counts_fail_status() -> None:
    """`warn` does NOT count as failure — exit-code gate is only `fail`."""
    only_warns = [
        Check(name="x", status="warn", detail="."),
        Check(name="y", status="warn", detail="."),
    ]
    assert has_failures(only_warns) is False

    has_fail = [
        Check(name="x", status="warn", detail="."),
        Check(name="y", status="fail", detail="."),
    ]
    assert has_failures(has_fail) is True


# --- CLI integration ------------------------------------------------------


def test_doctor_cli_prints_per_check_lines(tmp_path: Path) -> None:
    (tmp_path / ".efterlev").mkdir()
    result = runner.invoke(app, ["doctor", "--target", str(tmp_path)])
    # Doctor exits 0 when no `fail` status — only the API-key warn etc.
    assert result.exit_code == 0
    out = result.output
    assert "Efterlev doctor — pre-flight checks" in out
    assert "python_version" in out
    assert "anthropic_api_key" in out
    assert "frmr_cache" in out
    assert "bedrock_credentials" in out
    assert "summary:" in out
    assert "pass" in out


def test_doctor_subcommand_in_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "doctor" in result.output


def test_doctor_warning_lines_print_hint(tmp_path: Path) -> None:
    """Warn-status checks render their `hint` text inline."""
    # Empty target → no .efterlev dir → warn with hint.
    result = runner.invoke(app, ["doctor", "--target", str(tmp_path)])
    assert "hint:" in result.output
    assert "efterlev init" in result.output
