"""Tests for `efterlev.shell.credentials` — load/save/resolve."""

from __future__ import annotations

import os
import stat
from pathlib import Path

import pytest

from efterlev.shell import credentials as creds_mod
from efterlev.shell.credentials import (
    Credentials,
    load_credentials,
    resolve_anthropic_api_key,
    resolve_openai_api_key,
    save_credentials,
)


@pytest.fixture
def isolated_creds(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point CREDENTIALS_DIR at a tmp dir so tests don't touch ~/.efterlev."""
    monkeypatch.setattr(creds_mod, "CREDENTIALS_DIR", tmp_path)
    monkeypatch.setattr(creds_mod, "CREDENTIALS_PATH", tmp_path / "credentials.toml")
    return tmp_path


def test_load_returns_empty_when_file_missing(isolated_creds: Path) -> None:
    c = load_credentials()
    assert c.anthropic_api_key is None
    assert c.bedrock_region is None
    assert c.has_anthropic is False
    assert c.has_bedrock is False


def test_save_then_load_roundtrips_anthropic_key(isolated_creds: Path) -> None:
    save_credentials(Credentials(anthropic_api_key="sk-ant-test123"))
    c = load_credentials()
    assert c.anthropic_api_key == "sk-ant-test123"
    assert c.has_anthropic is True


def test_save_then_load_roundtrips_bedrock_region(isolated_creds: Path) -> None:
    save_credentials(Credentials(bedrock_region="us-east-1"))
    c = load_credentials()
    assert c.bedrock_region == "us-east-1"
    assert c.has_bedrock is True


def test_save_then_load_roundtrips_both(isolated_creds: Path) -> None:
    save_credentials(
        Credentials(
            anthropic_api_key="sk-ant-test123",
            bedrock_region="us-west-2",
            default_model="claude-sonnet-4-6",
        )
    )
    c = load_credentials()
    assert c.anthropic_api_key == "sk-ant-test123"
    assert c.bedrock_region == "us-west-2"
    assert c.default_model == "claude-sonnet-4-6"


def test_save_writes_mode_0600(isolated_creds: Path) -> None:
    """The credentials file must be readable only by the owner."""
    save_credentials(Credentials(anthropic_api_key="sk-ant-secret"))
    file_mode = stat.S_IMODE(os.stat(creds_mod.CREDENTIALS_PATH).st_mode)
    assert file_mode == 0o600


def test_load_tolerates_malformed_toml(isolated_creds: Path) -> None:
    """Malformed TOML must not crash the shell — degrades to empty creds."""
    creds_mod.CREDENTIALS_PATH.write_text("this is = not valid = toml\n", encoding="utf-8")
    c = load_credentials()
    assert c.anthropic_api_key is None
    assert c.bedrock_region is None


def test_resolve_anthropic_prefers_env_over_file(
    isolated_creds: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Env var takes precedence so CI overrides keep working."""
    save_credentials(Credentials(anthropic_api_key="sk-ant-from-file"))
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-from-env")
    assert resolve_anthropic_api_key() == "sk-ant-from-env"


def test_resolve_anthropic_falls_back_to_file(
    isolated_creds: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """When env is unset, the file's value is returned."""
    save_credentials(Credentials(anthropic_api_key="sk-ant-from-file"))
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    assert resolve_anthropic_api_key() == "sk-ant-from-file"


def test_resolve_anthropic_returns_none_when_neither_set(
    isolated_creds: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    assert resolve_anthropic_api_key() is None


def test_save_then_load_roundtrips_openai_key(isolated_creds: Path) -> None:
    save_credentials(Credentials(openai_api_key="sk-proj-test123"))
    c = load_credentials()
    assert c.openai_api_key == "sk-proj-test123"
    assert c.has_openai is True


def test_save_roundtrips_openai_alongside_anthropic(isolated_creds: Path) -> None:
    """The shell `/setup` OpenAI path preserves an already-configured
    Anthropic key (passes it through to save_credentials)."""
    save_credentials(Credentials(anthropic_api_key="sk-ant-x", openai_api_key="sk-proj-y"))
    c = load_credentials()
    assert c.anthropic_api_key == "sk-ant-x"
    assert c.openai_api_key == "sk-proj-y"


def test_resolve_openai_prefers_env_over_file(
    isolated_creds: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    save_credentials(Credentials(openai_api_key="sk-proj-from-file"))
    monkeypatch.setenv("OPENAI_API_KEY", "sk-proj-from-env")
    assert resolve_openai_api_key() == "sk-proj-from-env"


def test_resolve_openai_falls_back_to_file(
    isolated_creds: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    save_credentials(Credentials(openai_api_key="sk-proj-from-file"))
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert resolve_openai_api_key() == "sk-proj-from-file"


def test_resolve_openai_returns_none_when_neither_set(
    isolated_creds: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert resolve_openai_api_key() is None


def test_save_preserves_existing_when_only_updating_one_field(isolated_creds: Path) -> None:
    """Caller is responsible for preserving fields; this verifies save respects
    None vs explicit value distinction (None = omit section, value = write section).
    """
    save_credentials(Credentials(anthropic_api_key="sk-ant-x", bedrock_region="us-east-1"))
    # Now save with anthropic only — bedrock section should be gone.
    save_credentials(Credentials(anthropic_api_key="sk-ant-x"))
    c = load_credentials()
    assert c.anthropic_api_key == "sk-ant-x"
    assert c.bedrock_region is None
