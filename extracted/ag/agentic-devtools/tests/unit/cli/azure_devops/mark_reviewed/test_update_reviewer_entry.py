"""Tests for _update_reviewer_entry function."""

from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.azure_devops.mark_reviewed import _update_reviewer_entry


class TestUpdateReviewerEntry:
    """Tests for _update_reviewer_entry."""

    def test_patch_existing_entry(self, capsys):
        """Uses PATCH when existing_entry is provided."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_requests.patch.return_value = mock_response

        existing = {"vote": 10, "isFlagged": True, "hasDeclined": False}

        _update_reviewer_entry(
            mock_requests,
            {"Authorization": "Basic abc"},
            "https://dev.azure.com/org",
            "MyProject",
            "repo-id",
            123,
            "user-1",
            existing,
            ["/src/file.ts"],
        )

        mock_requests.patch.assert_called_once()
        captured = capsys.readouterr()
        assert "PATCH" in captured.out
        assert "successfully" in captured.out

    def test_put_new_entry(self, capsys):
        """Uses PUT when existing_entry is None."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_requests.put.return_value = mock_response

        _update_reviewer_entry(
            mock_requests,
            {"Authorization": "Basic abc"},
            "https://dev.azure.com/org",
            "MyProject",
            "repo-id",
            123,
            "user-1",
            None,
            ["/src/file.ts"],
        )

        mock_requests.put.assert_called_once()
        captured = capsys.readouterr()
        assert "PUT" in captured.out
        assert "successfully" in captured.out

    def test_raises_on_error(self, capsys):
        """Prints error and re-raises on failure."""
        mock_requests = MagicMock()
        mock_requests.patch.side_effect = Exception("Network failure")

        with pytest.raises(Exception, match="Network failure"):
            _update_reviewer_entry(
                mock_requests,
                {"Authorization": "Basic abc"},
                "https://dev.azure.com/org",
                "MyProject",
                "repo-id",
                123,
                "user-1",
                {"vote": 0},
                ["/src/file.ts"],
            )

        captured = capsys.readouterr()
        assert "Error during reviewer entry update" in captured.out
