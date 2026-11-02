import pytest

from agentic_devtools.adapters.pull_request_details import detect_provider


def test_detect_provider_prefers_explicit_value() -> None:
    assert detect_provider("github", {"platform": {"code_hosting": "azure_devops"}}) == "github"


def test_detect_provider_uses_github_repository_override(monkeypatch) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.azure_devops.config.get_azure_devops_context_from_git_remote",
        lambda: None,
    )

    assert detect_provider(repository="owner/repo") == "github"


def test_detect_provider_uses_explicit_value_then_state() -> None:
    assert detect_provider(None, {"provider": "azure_devops"}) == "azure_devops"
    assert detect_provider(None, {"provider": "azure_devops", "platform": {"code_hosting": "github"}}) == "github"
    assert detect_provider(None, {"github": {"provider": "github"}}) == "github"


def test_detect_provider_uses_configured_github_repository(monkeypatch) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.azure_devops.config.get_azure_devops_context_from_git_remote",
        lambda: None,
    )

    assert detect_provider(state={"github": {"repo": "owner/repo"}}) == "github"


def test_detect_provider_infers_from_checkout_remote(monkeypatch) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.azure_devops.config.get_azure_devops_context_from_git_remote",
        lambda: None,
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.github.repo_resolution._resolve_repo_from_git_remote",
        lambda: "owner/repo",
    )

    assert detect_provider() == "github"


def test_detect_provider_infers_azure_from_legacy_context() -> None:
    assert detect_provider(state={"organization": "https://dev.azure.com/org", "project": "project"}) == "azure_devops"


def test_detect_provider_infers_azure_from_checkout_remote(monkeypatch) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.azure_devops.config.get_azure_devops_context_from_git_remote",
        lambda: ("https://dev.azure.com/org", "project", "repo"),
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.github.repo_resolution._resolve_repo_from_git_remote",
        lambda: None,
    )

    assert detect_provider() == "azure_devops"


def test_detect_provider_can_require_configured_provider(monkeypatch) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.azure_devops.config.get_azure_devops_context_from_git_remote",
        lambda: pytest.fail("remote lookup should be skipped"),
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.github.repo_resolution._resolve_repo_from_git_remote",
        lambda: pytest.fail("remote lookup should be skipped"),
    )
    with pytest.raises(ValueError, match="origin remote"):
        detect_provider(allow_remote=False)


def test_detect_provider_rejects_unknown_or_missing(monkeypatch) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.azure_devops.config.get_azure_devops_context_from_git_remote",
        lambda: None,
    )
    monkeypatch.setattr(
        "agentic_devtools.cli.github.repo_resolution._resolve_repo_from_git_remote",
        lambda: None,
    )

    with pytest.raises(ValueError, match="must be 'azure_devops' or 'github'"):
        detect_provider("bitbucket", {})
    with pytest.raises(ValueError, match="must be 'azure_devops' or 'github'"):
        detect_provider(42, {})  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="origin remote"):
        detect_provider(None, {})
