import pytest

from agentic_devtools.cli.ci.guards import canonical_dispatch_token, validate_dispatch_identity

SHA = "b" * 40


def test_returns_canonical_token_from_identity_or_fields() -> None:
    identity = validate_dispatch_identity("Repo-Name", 8, SHA, 2)

    assert canonical_dispatch_token(identity) == f"agdt-dispatch-repo-name-8-{SHA}-2"
    assert canonical_dispatch_token("repo-name", 8, SHA, 2) == identity.token


def test_rejects_invalid_argument_shapes() -> None:
    identity = validate_dispatch_identity("repo-name", 8, SHA, 2)

    with pytest.raises(ValueError):
        canonical_dispatch_token(identity, 8, SHA, 2)
    with pytest.raises(ValueError):
        canonical_dispatch_token("repo", 8)
