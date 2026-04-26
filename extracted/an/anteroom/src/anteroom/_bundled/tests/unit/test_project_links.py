from __future__ import annotations

from anteroom.services.project_links import build_project_config, issue_label, issue_url, project_display_label


def test_public_profile_loaded_from_package() -> None:
    project = build_project_config({"profile": "public"})

    assert project_display_label(project) == "github.com/troylar/anteroom"
    assert issue_url(project, 1580) == "https://github.com/troylar/anteroom/issues/1580"


def test_neutral_profile_has_no_provider_links() -> None:
    project = build_project_config({"profile": "neutral"})

    assert project.name == "Anteroom"
    assert project.repo_url == ""
    assert issue_url(project, 1580) == ""
    assert issue_label(project, 1580) == "#1580"


def test_configured_internal_project_can_disable_issues() -> None:
    project = build_project_config(
        {
            "profile": "neutral",
            "name": "Internal Gateway",
            "repo_label": "bitbucket.internal/platform/gateway",
            "repo_url": "https://bitbucket.internal/platform/gateway",
            "issue_tracking": {"enabled": False},
        }
    )

    assert project_display_label(project) == "bitbucket.internal/platform/gateway"
    assert issue_url(project, 1580) == ""
    assert issue_label(project, 1580) == "#1580"
