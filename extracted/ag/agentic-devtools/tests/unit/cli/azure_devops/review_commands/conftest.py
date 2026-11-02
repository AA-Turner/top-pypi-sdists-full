"""Shared fixtures for review_commands unit tests."""

from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def _mock_generate_v2_review_artifacts():
    """Keep ``setup_pull_request_review`` tests hermetic.

    ``setup_pull_request_review`` calls ``generate_v2_review_artifacts`` with the
    ``prompts_dir`` returned by ``generate_review_prompts`` — a ``MagicMock`` in
    these tests. Because ``Path(MagicMock())`` resolves to a junk path instead of
    raising, the real function would create stray ``MagicMock/`` directories and
    perform real disk/git I/O. Mocking it keeps the wiring call site covered
    without those side effects.
    """
    with patch("agentic_devtools.cli.azure_devops.pr_review_artifacts.generate_v2_review_artifacts"):
        yield
