import pytest

from agentic_devtools.cli.ci.guards import validate_dispatch_identity

SHA = "b" * 40


def test_returns_strict_identity() -> None:
    identity = validate_dispatch_identity("Repo-Name", 8, SHA, 2)

    assert identity.repo == "repo-name"


def test_rejects_invalid_identity_fields() -> None:
    with pytest.raises(ValueError):
        validate_dispatch_identity("owner/repo", 8, SHA, 2)
    with pytest.raises(ValueError):
        validate_dispatch_identity("repo", 8, SHA.upper(), 2)
