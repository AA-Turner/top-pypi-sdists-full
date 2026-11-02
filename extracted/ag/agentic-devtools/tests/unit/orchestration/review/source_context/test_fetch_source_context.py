"""Tests for fetch_source_context()."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from agentic_devtools.orchestration.review.source_context import fetch_source_context


class TestFetchSourceContext:
    """Tests for source context retrieval."""

    def test_returns_none_when_missing_repo_info(self) -> None:
        """Returns None when repo_id/organization/project are missing."""
        result = fetch_source_context(
            file_path="/src/main.py",
            state={},
        )
        assert result is None

    def test_returns_none_when_commit_hash_missing(self) -> None:
        """Returns None when the commit hash needed for item lookup is missing."""
        result = fetch_source_context(
            file_path="/src/main.py",
            state={
                "repo_id": "repo-guid",
                "organization": "https://dev.azure.com/org",
                "project": "MyProject",
            },
        )
        assert result is None

    @patch("agentic_devtools.orchestration.review.source_context.get_auth_headers")
    @patch("agentic_devtools.orchestration.review.source_context.get_pat")
    @patch("agentic_devtools.orchestration.review.source_context.requests")
    def test_successful_retrieval(self, mock_requests, mock_pat, mock_auth) -> None:
        """Successfully retrieves file content from ADO."""
        mock_pat.return_value = "fake-pat"
        mock_auth.return_value = {"Authorization": "Basic fake"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "text/plain"}
        mock_response.text = "import os\n\nclass MyClass:\n    pass\n"
        mock_requests.get.return_value = mock_response

        result = fetch_source_context(
            file_path="/src/main.py",
            state={
                "commit_hash": "abc123",
                "repo_id": "repo-guid",
                "organization": "https://dev.azure.com/org",
                "project": "MyProject",
            },
        )

        assert result is not None
        assert "import os" in result

    @patch("agentic_devtools.orchestration.review.source_context.get_auth_headers")
    @patch("agentic_devtools.orchestration.review.source_context.get_pat")
    @patch("agentic_devtools.orchestration.review.source_context.requests")
    def test_successful_json_retrieval_normalizes_scope_path(
        self,
        mock_requests,
        mock_pat,
        mock_auth,
    ) -> None:
        """JSON item responses return the embedded content payload."""
        mock_pat.return_value = "fake-pat"
        mock_auth.return_value = {"Authorization": "Basic fake"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json; charset=utf-8"}
        mock_response.json.return_value = {"content": "print('hi')\n"}
        mock_requests.get.return_value = mock_response

        result = fetch_source_context(
            file_path="src/my file#1?.py",
            state={
                "commit_hash": "abc123",
                "repo_id": "repo-guid",
                "organization": "https://dev.azure.com/org",
                "project": "My Project/#1",
            },
        )

        assert result == "print('hi')\n"
        called_url = mock_requests.get.call_args.args[0]
        assert "My%20Project%2F%231" in called_url
        assert "path=/src/my%20file%231%3F.py" in called_url

    @patch("agentic_devtools.orchestration.review.source_context.get_auth_headers")
    @patch("agentic_devtools.orchestration.review.source_context.get_pat")
    @patch("agentic_devtools.orchestration.review.source_context.requests")
    def test_returns_none_on_404(self, mock_requests, mock_pat, mock_auth) -> None:
        """Returns None when file is not found (newly added)."""
        mock_pat.return_value = "fake-pat"
        mock_auth.return_value = {"Authorization": "Basic fake"}

        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests.get.return_value = mock_response

        result = fetch_source_context(
            file_path="/src/new_file.py",
            state={
                "commit_hash": "abc123",
                "repo_id": "repo-guid",
                "organization": "https://dev.azure.com/org",
                "project": "MyProject",
            },
        )

        assert result is None

    def test_returns_none_when_auth_fails(self) -> None:
        """Returns None when authentication fails."""
        with patch(
            "agentic_devtools.orchestration.review.source_context.get_pat",
            side_effect=RuntimeError("no PAT"),
        ):
            result = fetch_source_context(
                file_path="/src/main.py",
                state={
                    "commit_hash": "abc",
                    "repo_id": "r",
                    "organization": "o",
                    "project": "p",
                },
            )
            assert result is None

    @patch("agentic_devtools.orchestration.review.source_context.get_auth_headers")
    @patch("agentic_devtools.orchestration.review.source_context.get_pat")
    @patch("agentic_devtools.orchestration.review.source_context.requests")
    def test_returns_none_when_json_content_is_not_string(
        self,
        mock_requests,
        mock_pat,
        mock_auth,
    ) -> None:
        """Returns None when JSON response has a non-string 'content' field."""
        mock_pat.return_value = "fake-pat"
        mock_auth.return_value = {"Authorization": "Basic fake"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json; charset=utf-8"}
        # content is a list, not a string — should be treated as a fetch failure
        mock_response.json.return_value = {"content": ["not", "a", "string"]}
        mock_requests.get.return_value = mock_response

        result = fetch_source_context(
            file_path="/src/main.py",
            state={
                "commit_hash": "abc123",
                "repo_id": "repo-guid",
                "organization": "https://dev.azure.com/org",
                "project": "MyProject",
            },
        )

        assert result is None

    @patch("agentic_devtools.orchestration.review.source_context.get_auth_headers")
    @patch("agentic_devtools.orchestration.review.source_context.get_pat")
    @patch("agentic_devtools.orchestration.review.source_context.requests")
    def test_returns_none_and_warns_on_request_exception(
        self,
        mock_requests,
        mock_pat,
        mock_auth,
        capsys,
    ) -> None:
        """Unexpected request failures are reported to stderr."""
        mock_pat.return_value = "fake-pat"
        mock_auth.return_value = {"Authorization": "Basic fake"}
        mock_requests.get.side_effect = RuntimeError("network down")

        result = fetch_source_context(
            file_path="/src/main.py",
            state={
                "commit_hash": "abc123",
                "repo_id": "repo-guid",
                "organization": "https://dev.azure.com/org",
                "project": "MyProject",
            },
        )

        assert result is None
        assert "could not fetch source context" in capsys.readouterr().err

    @patch("agentic_devtools.orchestration.review.source_context.get_auth_headers")
    @patch("agentic_devtools.orchestration.review.source_context.get_pat")
    @patch("agentic_devtools.orchestration.review.source_context.requests")
    def test_returns_none_for_binary_content_type(
        self,
        mock_requests,
        mock_pat,
        mock_auth,
    ) -> None:
        """Returns None for non-text, non-JSON 200 responses (e.g. application/octet-stream)."""
        mock_pat.return_value = "fake-pat"
        mock_auth.return_value = {"Authorization": "Basic fake"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/octet-stream"}
        mock_response.text = "\x00\x01binary garbage"
        mock_requests.get.return_value = mock_response

        result = fetch_source_context(
            file_path="/assets/logo.png",
            state={
                "commit_hash": "abc123",
                "repo_id": "repo-guid",
                "organization": "https://dev.azure.com/org",
                "project": "MyProject",
            },
        )

        assert result is None
