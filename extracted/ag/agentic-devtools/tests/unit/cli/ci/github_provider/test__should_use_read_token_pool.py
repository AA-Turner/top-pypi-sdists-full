"""Tests for github_provider._should_use_read_token_pool()."""

from types import SimpleNamespace

import pytest

import agentic_devtools.cli.ci.github_provider as github_provider

_DEFAULT = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"


def _pool(default_token: str = "default-token") -> SimpleNamespace:
    return SimpleNamespace(default_identity=_DEFAULT, default_token=default_token, repo="owner/repo")


def test_short_circuits_when_pooling_is_disabled_or_bypassed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        github_provider,
        "_get_read_token_pool",
        lambda: (_ for _ in ()).throw(AssertionError("pool should not be loaded")),
    )
    assert not github_provider._should_use_read_token_pool(
        token=None,
        credential_identity=_DEFAULT,
        read_pool=False,
    )

    bypass = github_provider._READ_POOL_BYPASS.set(True)
    try:
        assert not github_provider._should_use_read_token_pool(
            token=None,
            credential_identity=_DEFAULT,
            read_pool=True,
        )
    finally:
        github_provider._READ_POOL_BYPASS.reset(bypass)


def test_rejects_missing_pool_unsupported_identity_and_missing_default_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(github_provider, "_get_read_token_pool", lambda: None)
    assert not github_provider._should_use_read_token_pool(
        token=None,
        credential_identity=_DEFAULT,
        read_pool=True,
    )

    monkeypatch.setattr(github_provider, "_get_read_token_pool", _pool)
    assert not github_provider._should_use_read_token_pool(
        token=None,
        credential_identity="UNRELATED_TOKEN",
        read_pool=True,
    )

    monkeypatch.setattr(github_provider, "_get_read_token_pool", lambda: _pool(""))
    assert not github_provider._should_use_read_token_pool(
        token=None,
        credential_identity=_DEFAULT,
        read_pool=True,
    )


def test_token_and_ambient_identity_must_match_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(github_provider, "_get_read_token_pool", _pool)

    assert github_provider._should_use_read_token_pool(
        token="default-token",
        credential_identity=_DEFAULT,
        read_pool=True,
    )
    assert not github_provider._should_use_read_token_pool(
        token="other-token",
        credential_identity=_DEFAULT,
        read_pool=True,
    )

    monkeypatch.delenv("GH_TOKEN", raising=False)
    assert github_provider._should_use_read_token_pool(
        token=None,
        credential_identity=_DEFAULT,
        read_pool=True,
    )
    monkeypatch.setenv("GH_TOKEN", "default-token")
    assert github_provider._should_use_read_token_pool(
        token=None,
        credential_identity=_DEFAULT,
        read_pool=True,
    )
    monkeypatch.setenv("GH_TOKEN", "other-token")
    assert not github_provider._should_use_read_token_pool(
        token=None,
        credential_identity=_DEFAULT,
        read_pool=True,
    )


def test_target_repository_must_match_the_validated_pool_repository(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(github_provider, "_get_read_token_pool", _pool)
    monkeypatch.delenv("GH_TOKEN", raising=False)

    assert github_provider._should_use_read_token_pool(
        token=None,
        credential_identity=_DEFAULT,
        read_pool=True,
        target_repository="owner/REPO",
    )
    monkeypatch.setenv("GH_TOKEN", "default-token")
    assert github_provider._should_use_read_token_pool(
        token=None,
        credential_identity=_DEFAULT,
        read_pool=True,
        target_repository="owner/REPO",
    )
    assert not github_provider._should_use_read_token_pool(
        token=None,
        credential_identity=_DEFAULT,
        read_pool=True,
        target_repository="owner/private",
    )
