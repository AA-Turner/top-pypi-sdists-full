"""Tests for _get_reviewer_entry function."""

from unittest.mock import MagicMock

import pytest
import requests as real_requests

from agentic_devtools.cli.azure_devops.mark_reviewed import _get_reviewer_entry


class TestGetReviewerEntry:
    """Tests for _get_reviewer_entry."""

    def test_returns_reviewer_entry_on_success(self):
        """Returns reviewer entry dict when user is a reviewer."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"id": "user-1", "vote": 0, "reviewedFiles": []}
        mock_requests.get.return_value = mock_response

        result = _get_reviewer_entry(
            mock_requests,
            {"Authorization": "Basic abc"},
            "https://dev.azure.com/org",
            "MyProject",
            "repo-id",
            123,
            "user-1",
        )
        assert result == {"id": "user-1", "vote": 0, "reviewedFiles": []}

    def test_returns_none_on_404(self, capsys):
        """Returns None when user is not a reviewer (404)."""
        mock_requests = MagicMock()
        # Create a proper HTTPError with a response attribute
        mock_error_response = MagicMock()
        mock_error_response.status_code = 404
        error = real_requests.exceptions.HTTPError(response=mock_error_response)

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = error
        mock_requests.get.return_value = mock_response
        mock_requests.exceptions = real_requests.exceptions

        result = _get_reviewer_entry(
            mock_requests,
            {"Authorization": "Basic abc"},
            "https://dev.azure.com/org",
            "MyProject",
            "repo-id",
            123,
            "user-1",
        )
        assert result is None
        captured = capsys.readouterr()
        assert "not yet a reviewer" in captured.out

    def test_returns_none_on_400_invalid_argument_json(self, capsys):
        """Returns None on 400 with InvalidArgumentValueException."""
        mock_requests = MagicMock()
        mock_error_response = MagicMock()
        mock_error_response.status_code = 400
        mock_error_response.json.return_value = {
            "message": "Invalid argument value",
            "typeKey": "InvalidArgumentValueException",
        }
        error = real_requests.exceptions.HTTPError(response=mock_error_response)

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = error
        mock_requests.get.return_value = mock_response
        mock_requests.exceptions = real_requests.exceptions

        result = _get_reviewer_entry(
            mock_requests,
            {"Authorization": "Basic abc"},
            "https://dev.azure.com/org",
            "MyProject",
            "repo-id",
            123,
            "user-1",
        )
        assert result is None

    def test_returns_none_on_400_invalid_argument_text(self, capsys):
        """Returns None on 400 with invalid argument in text body."""
        mock_requests = MagicMock()
        mock_error_response = MagicMock()
        mock_error_response.status_code = 400
        mock_error_response.json.side_effect = ValueError("not json")
        mock_error_response.text = "invalid argument value in request"
        error = real_requests.exceptions.HTTPError(response=mock_error_response)

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = error
        mock_requests.get.return_value = mock_response
        mock_requests.exceptions = real_requests.exceptions

        result = _get_reviewer_entry(
            mock_requests,
            {"Authorization": "Basic abc"},
            "https://dev.azure.com/org",
            "MyProject",
            "repo-id",
            123,
            "user-1",
        )
        assert result is None

    def test_raises_on_other_http_error(self):
        """Raises on non-404/non-400 HTTP error."""
        mock_requests = MagicMock()
        mock_error_response = MagicMock()
        mock_error_response.status_code = 500
        error = real_requests.exceptions.HTTPError(response=mock_error_response)

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = error
        mock_requests.get.return_value = mock_response
        mock_requests.exceptions = real_requests.exceptions

        with pytest.raises(real_requests.exceptions.HTTPError):
            _get_reviewer_entry(
                mock_requests,
                {"Authorization": "Basic abc"},
                "https://dev.azure.com/org",
                "MyProject",
                "repo-id",
                123,
                "user-1",
            )

    def test_raises_on_400_non_invalid_argument_json_parse_failure(self):
        """Raises when 400 with json parse error AND text has no 'invalid argument'."""
        mock_requests = MagicMock()
        mock_error_response = MagicMock()
        mock_error_response.status_code = 400
        mock_error_response.json.side_effect = ValueError("parse error")
        mock_error_response.text = "some other error message"
        error = real_requests.exceptions.HTTPError(response=mock_error_response)

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = error
        mock_requests.get.return_value = mock_response
        mock_requests.exceptions = real_requests.exceptions

        with pytest.raises(real_requests.exceptions.HTTPError):
            _get_reviewer_entry(
                mock_requests,
                {"Authorization": "Basic abc"},
                "https://dev.azure.com/org",
                "MyProject",
                "repo-id",
                123,
                "user-1",
            )

    def test_raises_on_400_non_matching_json_message(self):
        """Raises when 400 with JSON body that doesn't match invalid argument."""
        mock_requests = MagicMock()
        mock_error_response = MagicMock()
        mock_error_response.status_code = 400
        mock_error_response.json.return_value = {"message": "Some other error", "typeKey": "SomeOtherException"}
        error = real_requests.exceptions.HTTPError(response=mock_error_response)

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = error
        mock_requests.get.return_value = mock_response
        mock_requests.exceptions = real_requests.exceptions

        with pytest.raises(real_requests.exceptions.HTTPError):
            _get_reviewer_entry(
                mock_requests,
                {"Authorization": "Basic abc"},
                "https://dev.azure.com/org",
                "MyProject",
                "repo-id",
                123,
                "user-1",
            )
