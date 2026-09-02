from __future__ import annotations

from unittest.mock import patch

import pytest

from agentic_devtools.orchestration.safety.exceptions import BranchIsolationError
from agentic_devtools.orchestration.safety.isolation import BranchIsolationGuard


class TestBranchIsolationGuardGitMissing:
    """Tests for git-not-installed branch isolation behavior."""

    @patch("agentic_devtools.orchestration.safety.isolation.subprocess.run", side_effect=FileNotFoundError)
    def test_git_not_available_raises_branch_isolation_error(self, _mock_run) -> None:
        guard = BranchIsolationGuard(["main"])

        with pytest.raises(BranchIsolationError, match="git not available"):
            guard.check("git_push")
