"""Tests for the ``check_provider_connectivity`` re-export in issue_type_discovery."""

from agentic_devtools.cli.setup.issue_type_discovery import check_provider_connectivity
from agentic_devtools.cli.setup.provider_connectivity import (
    check_provider_connectivity as provider_connectivity_impl,
)


def test_reexports_provider_connectivity_function() -> None:
    """issue_type_discovery exposes the shared connectivity helper unchanged."""
    assert check_provider_connectivity is provider_connectivity_impl
