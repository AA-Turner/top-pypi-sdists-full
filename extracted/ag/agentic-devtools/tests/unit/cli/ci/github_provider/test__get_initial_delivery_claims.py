"""GitHub provider uses the repository-backed initial-delivery claim boundary."""

from unittest.mock import patch

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


def test_claim_store_is_scoped_to_provider_repository():
    with patch("agentic_devtools.cli.ci.initial_delivery_claims.InitialDeliveryClaims") as claims:
        assert GitHubActionsProvider(repo="org/repo")._get_initial_delivery_claims() is claims.return_value
    claims.assert_called_once_with("org/repo")
