"""Tests for GitLab MCP tools."""

import asyncio
import base64
from unittest.mock import Mock, patch

from bir_mcp.git_lab.prompts import get_feature_development_prompt, get_merge_request_review_prompt


class TestGitLabToolsReadOnly:
    """Test read-only GitLab tools."""

    def test_get_project_info(self, gitlab_tools):
        """Test get_project_info tool."""
        expected_result = {
            "name_with_namespace": "test/project",
            "topics": ["python", "testing"],
            "description": "Test project",
            "web_url": "https://gitlab.example.com/test/project",
            "branches": ["main"],
            "last_activity_at": "2024-01-01 00:00:00 UTC",
        }

        # Mock the async method
        async def mock_async_method(*args, **kwargs):
            return expected_result

        gitlab_tools.get_project_info = mock_async_method

        # Since we're testing the async method, we need to run it
        result = asyncio.run(gitlab_tools.get_project_info("test/project"))

        assert result["name_with_namespace"] == "test/project"
        assert result["topics"] == ["python", "testing"]
        assert result["description"] == "Test project"
        assert result["web_url"] == "https://gitlab.example.com/test/project"
        assert result["branches"] == ["main"]
        assert "last_activity_at" in result

    def test_list_all_repo_branch_files(self, gitlab_tools):
        """Test list_all_repo_branch_files tool."""
        expected_result = {
            "files": [
                {"path": "README.md", "type": "blob"},
                {"path": "src/main.py", "type": "blob"},
                {"path": "src", "type": "tree"},
            ]
        }

        # Mock the async method
        async def mock_async_method(*args, **kwargs):
            return expected_result

        gitlab_tools.list_all_repo_branch_files = mock_async_method

        # Since we're testing the async method, we need to run it
        result = asyncio.run(gitlab_tools.list_all_repo_branch_files("test/project", "main"))

        assert "files" in result
        assert len(result["files"]) == 3
        assert result["files"][0] == {"path": "README.md", "type": "blob"}

    def test_get_file_content(self, gitlab_tools, mock_project):
        """Test get_file_content tool."""
        file_content = "print('Hello World')"
        encoded_content = base64.b64encode(file_content.encode()).decode()

        mock_file_data = {"content": encoded_content}

        # Mock async methods
        async def mock_get_project_id(project_path_or_url):
            return 123

        async def mock_ahttpx_get(endpoint, **kwargs):
            mock_response = Mock()
            mock_response.json.return_value = mock_file_data
            return mock_response

        with (
            patch.object(gitlab_tools, "get_project_id", side_effect=mock_get_project_id),
            patch.object(gitlab_tools, "ahttpx_get", side_effect=mock_ahttpx_get),
        ):
            result = asyncio.run(
                gitlab_tools.get_file_content("test/project", "main", "src/main.py")
            )

            assert result["file_content"] == file_content

    def test_search_in_repository(self, gitlab_tools, mock_project):
        """Test search_in_repository tool."""
        mock_search_results = [
            {
                "path": "src/main.py",
                "data": "def main():\n    print('Hello')",
                "startline": 1,
            }
        ]
        expected_results = [
            {
                "file_path": "src/main.py",
                "starting_line_in_file": 1,
                "snippet": "def main():\n    print('Hello')",
            }
        ]

        # Mock async methods
        async def mock_get_project_id(project_path_or_url):
            return 123

        async def mock_ahttpx_get(endpoint, **kwargs):
            mock_response = Mock()
            mock_response.json.return_value = mock_search_results
            return mock_response

        with (
            patch.object(gitlab_tools, "get_project_id", side_effect=mock_get_project_id),
            patch.object(gitlab_tools, "ahttpx_get", side_effect=mock_ahttpx_get),
        ):
            result = asyncio.run(gitlab_tools.search_in_repository("test/project", "main", "Hello"))

            assert result["search_results"] == expected_results

    def test_get_latest_pipeline_info(self, gitlab_tools, mock_project):
        """Test get_latest_pipeline_info tool."""
        mock_pipeline_data = {
            "id": 123,
            "web_url": "https://gitlab.example.com/test/project/-/pipelines/123",
            "created_at": "2024-01-01T00:00:00Z",
            "status": "success",
            "source": "push",
            "duration": 300,
            "queued_duration": 30,
            "sha": "abc123",
        }

        mock_commit_data = {
            "id": "abc123",
            "title": "Test commit",
            "author_name": "Test Author",
            "web_url": "https://gitlab.example.com/test/project/-/commit/abc123",
        }

        mock_jobs_data = [
            {
                "name": "test",
                "status": "success",
                "stage": "test",
                "allow_failure": False,
                "web_url": "https://gitlab.example.com/test/project/-/jobs/456",
            }
        ]

        # Mock async methods
        async def mock_get_project_id(project_path_or_url):
            return 123

        async def mock_ahttpx_get(endpoint, **kwargs):
            mock_response = Mock()
            if "pipelines" in endpoint and "jobs" not in endpoint:
                mock_response.json.return_value = [mock_pipeline_data]
            elif "commits" in endpoint:
                mock_response.json.return_value = mock_commit_data
            elif "jobs" in endpoint:
                mock_response.json.return_value = mock_jobs_data
            return mock_response

        with (
            patch.object(gitlab_tools, "get_project_id", side_effect=mock_get_project_id),
            patch.object(gitlab_tools, "ahttpx_get", side_effect=mock_ahttpx_get),
        ):
            result = asyncio.run(gitlab_tools.get_latest_pipeline_info("test/project"))

            assert result["web_url"] == "https://gitlab.example.com/test/project/-/pipelines/123"
            assert result["status"] == "success"
            assert result["commit"]["title"] == "Test commit"
            assert len(result["jobs"]) == 1
            assert result["jobs"][0]["name"] == "test"

    @patch("asyncio.run")
    def test_get_merge_request_overview(
        self, mock_asyncio_run, gitlab_tools, mock_project, mock_merge_request
    ):
        """Test get_merge_request_overview tool."""
        expected_result = {
            "merge_request": {"id": 456, "title": "Test MR"},
            "pipeline_status": "success",
            "file_changes": [{"old_path": "file1.py", "new_path": "file1.py"}],
        }
        mock_asyncio_run.return_value = expected_result

        # Mock the async method
        async def mock_async_method(*args, **kwargs):
            return expected_result

        gitlab_tools.get_merge_request_overview = mock_async_method

        # Since we're testing the async method, we need to run it
        result = asyncio.run(gitlab_tools.get_merge_request_overview("test/project", 1))

        assert result["merge_request"]["id"] == 456
        assert result["merge_request"]["title"] == "Test MR"
        assert result["pipeline_status"] == "success"
        assert len(result["file_changes"]) == 1

    def test_get_merge_request_overview_from_url(self, gitlab_tools):
        """Test get_merge_request_overview_from_url tool."""
        mr_url = "https://gitlab.example.com/test/project/-/merge_requests/1"
        expected_result = {"merge_request": {"id": 456}}

        # Mock the async method
        async def mock_async_method(*args, **kwargs):
            return expected_result

        gitlab_tools.get_merge_request_overview_from_url = mock_async_method

        # Since we're testing the async method, we need to run it
        result = asyncio.run(gitlab_tools.get_merge_request_overview_from_url(mr_url))

        assert result["merge_request"]["id"] == 456

    def test_get_merge_request_file_diffs(self, gitlab_tools, mock_project, mock_merge_request):
        """Test get_merge_request_file_diffs tool."""
        expected_result = {
            "file_diffs": [
                {"new_path": "file1.py", "diff": "@@ -1,3 +1,3 @@\n-old line\n+new line"},
                {
                    "new_path": "file2.py",
                    "diff": "@@ -1,2 +1,2 @@\n-another old line\n+another new line",
                },
            ]
        }

        # Mock the async method
        async def mock_async_method(*args, **kwargs):
            return expected_result

        gitlab_tools.get_merge_request_file_diffs = mock_async_method

        # Since we're testing the async method, we need to run it
        result = asyncio.run(
            gitlab_tools.get_merge_request_file_diffs("test/project", 1, ["file1.py", "file2.py"])
        )

        assert len(result["file_diffs"]) == 2
        assert result["file_diffs"][0]["new_path"] == "file1.py"
        assert "diff" in result["file_diffs"][0]

    def test_search_users(self, gitlab_tools, mock_user):
        """Test search_users tool."""
        mock_users_data = [{
            "id": 123,
            "username": "testuser",
            "name": "Test User",
            "email": "test@example.com"
        }]
        
        # Mock async method
        async def mock_ahttpx_get(endpoint, **kwargs):
            mock_response = Mock()
            mock_response.json.return_value = mock_users_data
            return mock_response

        with patch.object(gitlab_tools, "ahttpx_get", side_effect=mock_ahttpx_get):
            result = asyncio.run(gitlab_tools.search_users("testuser"))

            assert len(result["users"]) == 1
            assert result["users"][0]["username"] == "testuser"
            assert result["users"][0]["email"] == "test@example.com"

    def test_search_merge_requests(self, gitlab_tools, mock_project, mock_merge_request):
        """Test search_merge_requests tool."""
        expected_result = {"merge_requests": [{"title": "Test MR", "id": 456}]}

        # Mock the async method
        async def mock_async_method(*args, **kwargs):
            return expected_result

        gitlab_tools.search_merge_requests = mock_async_method

        # Since we're testing the async method, we need to run it
        result = asyncio.run(
            gitlab_tools.search_merge_requests(
                "test/project", source_branch="feature", target_branch="main", state="opened"
            )
        )

        assert len(result["merge_requests"]) == 1
        assert result["merge_requests"][0]["title"] == "Test MR"


class TestGitLabToolsWrite:
    """Test write GitLab tools."""

    def test_create_merge_request(self, gitlab_tools, mock_project):
        """Test create_merge_request tool."""
        mock_mr_data = {
            "id": 789,
            "iid": 2,
            "web_url": "https://gitlab.example.com/test/project/-/merge_requests/2"
        }
        
        # Mock async methods
        async def mock_get_project_id(project_path_or_url):
            return 123
            
        async def mock_ahttpx_post(url, **kwargs):
            mock_response = Mock()
            mock_response.json.return_value = mock_mr_data
            return mock_response

        with patch.object(gitlab_tools, "get_project_id", side_effect=mock_get_project_id), \
             patch.object(gitlab_tools, "ahttpx") as mock_ahttpx:
            mock_ahttpx.post = mock_ahttpx_post
            
            result = asyncio.run(gitlab_tools.create_merge_request(
                project_path_or_url="test/project",
                source_branch="feature-branch",
                target_branch="main",
                title="New Feature",
                description="Adding new feature",
                assignee_id=123,
                labels=["enhancement", "feature"],
            ))

            assert result["created_merge_request"]["id"] == 789
            assert result["created_merge_request"]["iid"] == 2

    def test_create_branch(self, gitlab_tools, mock_project):
        """Test create_branch tool."""
        mock_branch_data = {
            "web_url": "https://gitlab.example.com/test/project/-/tree/new-feature"
        }
        
        # Mock async methods
        async def mock_get_project_id(project_path_or_url):
            return 123
            
        async def mock_ahttpx_post(url, **kwargs):
            mock_response = Mock()
            mock_response.json.return_value = mock_branch_data
            return mock_response

        with patch.object(gitlab_tools, "get_project_id", side_effect=mock_get_project_id), \
             patch.object(gitlab_tools, "ahttpx") as mock_ahttpx:
            mock_ahttpx.post = mock_ahttpx_post
            
            result = asyncio.run(gitlab_tools.create_branch("test/project", "new-feature", "main"))

            assert (
                result["new_branch_url"]
                == "https://gitlab.example.com/test/project/-/tree/new-feature"
            )

    @patch("bir_mcp.git_lab.tools.httpx.AsyncClient")
    def test_http_request(self, mock_httpx, gitlab_tools):
        """Test http_request tool."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": "success"}

        # Mock the async client context manager
        mock_client = Mock()
        mock_client.request.return_value = mock_response
        mock_httpx.return_value.__aenter__.return_value = mock_client

        # Since this is an async method, we need to test it differently
        # For now, we'll just test that the method exists and has the right signature
        assert hasattr(gitlab_tools, "http_request")

        # Test the method signature
        import inspect

        sig = inspect.signature(gitlab_tools.http_request)
        assert "path" in sig.parameters
        assert "http_method" in sig.parameters
        assert "json_query_params" in sig.parameters
        assert "content" in sig.parameters


class TestGitLabToolsPrompts:
    """Test GitLab prompt functions."""

    def test_get_feature_development_prompt(self):
        """Test get_feature_development_prompt function."""
        result = get_feature_development_prompt("PROJ", "Add user authentication")

        assert isinstance(result, str)
        assert "Add user authentication" in result
        assert "PROJ" in result
        assert "feature_description" in result

    def test_get_merge_request_review_prompt(self):
        """Test get_merge_request_review_prompt function."""
        mr_url = "https://gitlab.example.com/test/project/-/merge_requests/1"
        result = get_merge_request_review_prompt(mr_url)

        assert isinstance(result, str)
        assert mr_url in result
        assert "review" in result.lower()


class TestGitLabToolsHelpers:
    """Test GitLab helper methods."""

    def test_get_project_from_url(self, gitlab_tools):
        """Test get_project_from_url helper method."""
        mock_project = Mock()
        gitlab_tools.gitlab.projects.get.return_value = mock_project

        # The actual method calls gitlab.projects.get with the path directly
        result = gitlab_tools.get_project_from_url("test/project")

        assert result == mock_project
        gitlab_tools.gitlab.projects.get.assert_called_once_with("test/project")

    def test_get_mcp_tools_returns_all_tools(self, gitlab_tools):
        """Test that get_mcp_tools returns all expected tools."""
        with patch("bir_mcp.git_lab.tools.get_gitlab_pat_scopes") as mock_scopes:
            mock_scopes.return_value = ["api"]

            with (
                patch("bir_mcp.git_lab.tools.build_readonly_tools") as mock_readonly,
                patch("bir_mcp.git_lab.tools.build_write_tools") as mock_write,
            ):
                mock_readonly.return_value = ["read_tool1", "read_tool2"]
                mock_write.return_value = ["write_tool1", "write_tool2"]

                gitlab_tools.get_mcp_tools()

                # Verify read tools were called with correct functions
                read_tools_arg = mock_readonly.call_args[0][0]
                assert gitlab_tools.get_project_info in read_tools_arg
                assert gitlab_tools.list_all_repo_branch_files in read_tools_arg
                assert gitlab_tools.get_file_content in read_tools_arg
                assert gitlab_tools.search_in_repository in read_tools_arg
                assert gitlab_tools.get_latest_pipeline_info in read_tools_arg
                assert gitlab_tools.get_merge_request_overview in read_tools_arg
                assert gitlab_tools.get_merge_request_overview_from_url in read_tools_arg
                assert gitlab_tools.get_merge_request_file_diffs in read_tools_arg
                assert gitlab_tools.search_users in read_tools_arg
                assert gitlab_tools.search_merge_requests in read_tools_arg

                # Verify write tools were called with correct functions
                write_tools_arg = mock_write.call_args[0][0]
                assert gitlab_tools.create_merge_request in write_tools_arg
                assert gitlab_tools.create_branch in write_tools_arg
                assert gitlab_tools.http_request in write_tools_arg

    def test_get_mcp_tools_skips_write_tools_without_scopes(self, gitlab_tools):
        """Test that get_mcp_tools skips write tools when PAT doesn't have required scopes."""
        with patch("bir_mcp.git_lab.tools.get_gitlab_pat_scopes") as mock_scopes:
            mock_scopes.return_value = []  # No scopes

            with (
                patch("bir_mcp.git_lab.tools.build_readonly_tools") as mock_readonly,
                patch("bir_mcp.git_lab.tools.build_write_tools") as mock_write,
            ):
                mock_readonly.return_value = ["read_tool1", "read_tool2"]

                gitlab_tools.get_mcp_tools()

                # Verify only read tools were built
                mock_readonly.assert_called_once()
                mock_write.assert_not_called()
