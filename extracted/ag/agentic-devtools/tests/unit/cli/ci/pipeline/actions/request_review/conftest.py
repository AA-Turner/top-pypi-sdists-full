from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.models import PRMetadata


@pytest.fixture
def verified_pr_provider() -> MagicMock:
    provider = MagicMock()
    provider.get_pr_metadata.return_value = PRMetadata(42, "change", "feature", "head-sha", "main", changed_files=1)
    provider.get_ref_sha.return_value = "base-sha"
    provider.list_pr_files_complete.return_value = ["src/main.py"]
    return provider
