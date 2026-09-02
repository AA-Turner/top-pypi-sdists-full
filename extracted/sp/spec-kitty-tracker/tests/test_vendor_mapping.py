from spec_kitty_tracker import (
    CanonicalStatus,
    GitHubConnector,
    GitHubConnectorConfig,
    GitLabConnector,
    GitLabConnectorConfig,
    JiraConnector,
    JiraConnectorConfig,
    LinearConnector,
    LinearConnectorConfig,
)


def test_jira_payload_mapping() -> None:
    connector = JiraConnector(
        JiraConnectorConfig(
            base_url="https://example.atlassian.net",
            email="user@example.com",
            api_token="token",
            project_key="PROJ",
        )
    )

    issue = connector._to_canonical(  # noqa: SLF001
        {
            "id": "10001",
            "key": "PROJ-1",
            "fields": {
                "summary": "Issue",
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": "Hello"}],
                        }
                    ],
                },
                "status": {"name": "In Progress"},
                "priority": {"name": "High"},
                "issuetype": {"name": "Task"},
                "labels": ["backend"],
            },
        }
    )

    assert issue.ref.key == "PROJ-1"
    assert issue.status == CanonicalStatus.IN_PROGRESS


async def test_linear_payload_mapping() -> None:
    connector = LinearConnector(LinearConnectorConfig(api_key="lin_api", team_id="team-1"))

    issue = connector._to_canonical(  # noqa: SLF001
        {
            "id": "abc",
            "identifier": "ENG-1",
            "title": "Linear issue",
            "description": "Body",
            "priority": 2,
            "createdAt": "2026-02-26T12:00:00Z",
            "updatedAt": "2026-02-26T13:00:00Z",
            "state": {"id": "st", "name": "In Progress", "type": "started"},
            "labels": {"nodes": [{"name": "feature"}]},
        }
    )

    assert issue.ref.id == "abc"
    assert issue.status == CanonicalStatus.IN_PROGRESS


def test_github_payload_mapping() -> None:
    connector = GitHubConnector(
        GitHubConnectorConfig(
            owner="spec-kitty",
            repo="tracker",
            token="ghp_test",
        )
    )

    issue = connector._to_canonical(  # noqa: SLF001
        {
            "number": 42,
            "title": "GitHub issue",
            "body": "Body",
            "state": "open",
            "html_url": "https://github.com/spec-kitty/tracker/issues/42",
            "labels": [{"name": "bug"}, {"name": "backend"}],
            "assignees": [{"login": "alice"}, {"login": "bob"}],
            "created_at": "2026-03-01T10:00:00Z",
            "updated_at": "2026-03-01T11:00:00Z",
        }
    )

    assert issue.ref.id == "42"
    assert issue.ref.key == "#42"
    assert issue.status == CanonicalStatus.TODO
    assert issue.issue_type.value == "bug"
    assert issue.assignees == ["alice", "bob"]


def test_gitlab_payload_mapping() -> None:
    connector = GitLabConnector(
        GitLabConnectorConfig(
            project_id="123",
            token="glpat_test",
        )
    )

    issue = connector._to_canonical(  # noqa: SLF001
        {
            "iid": 7,
            "title": "GitLab issue",
            "description": "Body",
            "state": "closed",
            "web_url": "https://gitlab.com/spec-kitty/tracker/-/issues/7",
            "labels": ["bug", "ops"],
            "assignees": [{"username": "maintainer"}],
            "created_at": "2026-03-01T08:30:00Z",
            "updated_at": "2026-03-01T09:45:00Z",
        }
    )

    assert issue.ref.id == "7"
    assert issue.ref.key == "7"
    assert issue.status == CanonicalStatus.DONE
    assert issue.issue_type.value == "bug"
    assert issue.assignees == ["maintainer"]
