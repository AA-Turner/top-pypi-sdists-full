"""Tests for _retrieve_via_ado_api."""

from __future__ import annotations

from unittest.mock import MagicMock, patch


class TestRetrieveViaAdoApi:
    """Tests for _retrieve_via_ado_api."""

    def test_ado_fallback_missing_config(self) -> None:
        """ADO fallback with missing org/project/repo returns unavailable."""
        from agentic_devtools.orchestration.review.file_retriever import _retrieve_via_ado_api

        state: dict = {"organization": "", "project": "", "repo_id": ""}
        with (
            patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="fake-pat"),
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_auth_headers",
                return_value={"Authorization": "Basic fake"},
            ),
        ):
            result = _retrieve_via_ado_api("/src/app.py", "abc123", state)
        assert result.context_status == "unavailable"
        assert "missing_ado_config" in result.context_status_reason

    def test_ado_fallback_auth_failure(self) -> None:
        """ADO fallback with auth failure returns unavailable."""
        from agentic_devtools.orchestration.review.file_retriever import _retrieve_via_ado_api

        state: dict = {"organization": "https://dev.azure.com/org", "project": "proj", "repo_id": "repo-id"}
        with patch("agentic_devtools.cli.azure_devops.auth.get_pat", side_effect=Exception("no PAT")):
            result = _retrieve_via_ado_api("/src/app.py", "abc123", state)
        assert result.context_status == "unavailable"
        assert "auth" in result.context_status_reason

    def test_ado_fallback_success(self) -> None:
        """ADO fallback with successful text/plain response."""
        from agentic_devtools.orchestration.review.file_retriever import _retrieve_via_ado_api

        state: dict = {"organization": "https://dev.azure.com/org", "project": "proj", "repo_id": "repo-id"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "text/plain"}
        mock_response.iter_content.return_value = [b"file content here"]

        with (
            patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="fake-pat"),
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_auth_headers",
                return_value={"Authorization": "Basic fake"},
            ),
            patch("requests.get", return_value=mock_response),
        ):
            result = _retrieve_via_ado_api("/src/app.py", "abc123", state)
        assert result.context_status == "success"
        assert result.content == "file content here"

    def test_ado_fallback_http_error(self) -> None:
        """ADO fallback with non-200 response."""
        from agentic_devtools.orchestration.review.file_retriever import _retrieve_via_ado_api

        state: dict = {"organization": "https://dev.azure.com/org", "project": "proj", "repo_id": "repo-id"}

        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.headers = {"Content-Type": "text/plain"}

        with (
            patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="fake-pat"),
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_auth_headers",
                return_value={"Authorization": "Basic fake"},
            ),
            patch("requests.get", return_value=mock_response),
        ):
            result = _retrieve_via_ado_api("/src/app.py", "abc123", state)
        assert result.context_status == "unavailable"
        assert "404" in result.context_status_reason

    def test_ado_fallback_network_error(self) -> None:
        """ADO fallback with network exception."""
        from agentic_devtools.orchestration.review.file_retriever import _retrieve_via_ado_api

        state: dict = {"organization": "https://dev.azure.com/org", "project": "proj", "repo_id": "repo-id"}

        with (
            patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="fake-pat"),
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_auth_headers",
                return_value={"Authorization": "Basic fake"},
            ),
            patch("requests.get", side_effect=Exception("connection failed")),
        ):
            result = _retrieve_via_ado_api("/src/app.py", "abc123", state)
        assert result.context_status == "unavailable"
        assert "ado_api_error" in result.context_status_reason

    def test_ado_json_content_type(self) -> None:
        """ADO response with JSON content type extracts content field."""
        from agentic_devtools.orchestration.review.file_retriever import _retrieve_via_ado_api

        state: dict = {"organization": "https://dev.azure.com/org", "project": "proj", "repo_id": "repo-id"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json; charset=utf-8"}
        mock_response.iter_content.return_value = [b'{"content": "json file content"}']

        with (
            patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="fake-pat"),
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_auth_headers",
                return_value={"Authorization": "Basic fake"},
            ),
            patch("requests.get", return_value=mock_response),
        ):
            result = _retrieve_via_ado_api("/src/app.py", "abc123", state)
        assert result.context_status == "success"
        assert result.content == "json file content"

    def test_ado_json_non_string_content(self) -> None:
        """ADO JSON response with non-string content returns unavailable."""
        from agentic_devtools.orchestration.review.file_retriever import _retrieve_via_ado_api

        state: dict = {"organization": "https://dev.azure.com/org", "project": "proj", "repo_id": "repo-id"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.iter_content.return_value = [b'{"content": 12345}']

        with (
            patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="fake-pat"),
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_auth_headers",
                return_value={"Authorization": "Basic fake"},
            ),
            patch("requests.get", return_value=mock_response),
        ):
            result = _retrieve_via_ado_api("/src/app.py", "abc123", state)
        assert result.context_status == "unavailable"
        assert "non_string" in result.context_status_reason

    def test_ado_text_content_type(self) -> None:
        """ADO response with text content type returns text directly."""
        from agentic_devtools.orchestration.review.file_retriever import _retrieve_via_ado_api

        state: dict = {"organization": "https://dev.azure.com/org", "project": "proj", "repo_id": "repo-id"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "text/plain"}
        mock_response.iter_content.return_value = [b"plain text content"]

        with (
            patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="fake-pat"),
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_auth_headers",
                return_value={"Authorization": "Basic fake"},
            ),
            patch("requests.get", return_value=mock_response),
        ):
            result = _retrieve_via_ado_api("/src/app.py", "abc123", state)
        assert result.context_status == "success"
        assert result.content == "plain text content"

    def test_ado_binary_content_type(self) -> None:
        """ADO response with binary content type skips."""
        from agentic_devtools.orchestration.review.file_retriever import _retrieve_via_ado_api

        state: dict = {"organization": "https://dev.azure.com/org", "project": "proj", "repo_id": "repo-id"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/octet-stream"}
        mock_response.iter_content.return_value = [b"binary data"]

        with (
            patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="fake-pat"),
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_auth_headers",
                return_value={"Authorization": "Basic fake"},
            ),
            patch("requests.get", return_value=mock_response),
        ):
            result = _retrieve_via_ado_api("/src/app.py", "abc123", state)
        assert result.context_status == "skipped_binary"

    def test_ado_json_content_too_large(self) -> None:
        """ADO response body exceeding max_size_bytes stops streaming and returns skipped_too_large."""
        from agentic_devtools.orchestration.review.file_retriever import _retrieve_via_ado_api

        state: dict = {"organization": "https://dev.azure.com/org", "project": "proj", "repo_id": "repo-id"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.iter_content.return_value = [b"A" * 100]

        with (
            patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="fake-pat"),
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_auth_headers",
                return_value={"Authorization": "Basic fake"},
            ),
            patch("requests.get", return_value=mock_response),
        ):
            result = _retrieve_via_ado_api("/src/app.py", "abc123", state, max_size_bytes=10)
        assert result.context_status == "skipped_too_large"

    def test_ado_content_length_header_early_rejection(self) -> None:
        """Response with Content-Length exceeding max_size_bytes is rejected before streaming."""
        from agentic_devtools.orchestration.review.file_retriever import _retrieve_via_ado_api

        state: dict = {"organization": "https://dev.azure.com/org", "project": "proj", "repo_id": "repo-id"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "text/plain", "Content-Length": "1000000"}

        with (
            patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="fake-pat"),
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_auth_headers",
                return_value={"Authorization": "Basic fake"},
            ),
            patch("requests.get", return_value=mock_response),
        ):
            result = _retrieve_via_ado_api("/src/app.py", "abc123", state, max_size_bytes=10)
        assert result.context_status == "skipped_too_large"
        assert "content_length_exceeds" in result.context_status_reason
        mock_response.iter_content.assert_not_called()

    def test_ado_content_length_within_limit_proceeds_to_streaming(self) -> None:
        """Response with Content-Length within limit proceeds to stream the body."""
        from agentic_devtools.orchestration.review.file_retriever import _retrieve_via_ado_api

        state: dict = {"organization": "https://dev.azure.com/org", "project": "proj", "repo_id": "repo-id"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "text/plain", "Content-Length": "5"}
        mock_response.iter_content.return_value = [b"hello"]

        with (
            patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="fake-pat"),
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_auth_headers",
                return_value={"Authorization": "Basic fake"},
            ),
            patch("requests.get", return_value=mock_response),
        ):
            result = _retrieve_via_ado_api("/src/app.py", "abc123", state)
        assert result.context_status == "success"
        assert result.content == "hello"

    def test_ado_content_length_invalid_falls_through_to_streaming(self) -> None:
        """Non-numeric Content-Length is ignored and streaming proceeds normally."""
        from agentic_devtools.orchestration.review.file_retriever import _retrieve_via_ado_api

        state: dict = {"organization": "https://dev.azure.com/org", "project": "proj", "repo_id": "repo-id"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "text/plain", "Content-Length": "not-a-number"}
        mock_response.iter_content.return_value = [b"hello"]

        with (
            patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="fake-pat"),
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_auth_headers",
                return_value={"Authorization": "Basic fake"},
            ),
            patch("requests.get", return_value=mock_response),
        ):
            result = _retrieve_via_ado_api("/src/app.py", "abc123", state)
        assert result.context_status == "success"
        assert result.content == "hello"

    def test_ado_empty_iter_content_chunk_skipped(self) -> None:
        """Empty chunks from iter_content are silently skipped."""
        from agentic_devtools.orchestration.review.file_retriever import _retrieve_via_ado_api

        state: dict = {"organization": "https://dev.azure.com/org", "project": "proj", "repo_id": "repo-id"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "text/plain"}
        mock_response.iter_content.return_value = [b"", b"real content", b""]

        with (
            patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="fake-pat"),
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_auth_headers",
                return_value={"Authorization": "Basic fake"},
            ),
            patch("requests.get", return_value=mock_response),
        ):
            result = _retrieve_via_ado_api("/src/app.py", "abc123", state)
        assert result.context_status == "success"
        assert result.content == "real content"

    def test_ado_json_decode_error_returns_unavailable(self) -> None:
        """Malformed JSON body returns unavailable."""
        from agentic_devtools.orchestration.review.file_retriever import _retrieve_via_ado_api

        state: dict = {"organization": "https://dev.azure.com/org", "project": "proj", "repo_id": "repo-id"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.iter_content.return_value = [b"not valid json {{"]

        with (
            patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="fake-pat"),
            patch(
                "agentic_devtools.cli.azure_devops.auth.get_auth_headers",
                return_value={"Authorization": "Basic fake"},
            ),
            patch("requests.get", return_value=mock_response),
        ):
            result = _retrieve_via_ado_api("/src/app.py", "abc123", state)
        assert result.context_status == "unavailable"
        assert "json_decode_error" in result.context_status_reason
