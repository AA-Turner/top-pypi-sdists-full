"""Tests for the compatibility facade's finding-content helper export."""

from agentic_devtools.cli.github import ccr_finding_content, ccr_finding_content_key


def test_finding_content_key_is_reexported_from_its_helper_module() -> None:
    assert ccr_finding_content._finding_content_key is ccr_finding_content_key._finding_content_key
