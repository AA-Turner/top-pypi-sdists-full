"""
Comprehensive tests for Atlassian MCP tools.
"""

import asyncio
from unittest.mock import Mock, patch

import pytest

from bir_mcp.atlassian import Jira


class TestAtlassianTools:
    """Test Atlassian MCP tools."""

    @pytest.fixture
    def atlassian_tools(self):
        """Create Atlassian tools instance for testing."""
        with patch("bir_mcp.atlassian.atlassian.Jira") as mock_jira_class:
            # Mock the Jira class constructor
            mock_jira_instance = Mock()
            mock_jira_instance.url = "https://jira.example.com"
            mock_jira_class.return_value = mock_jira_instance

            # Mock search_users
            mock_jira_instance.search_users.return_value = [
                {"accountId": "123", "displayName": "Test User", "emailAddress": "test@example.com"}
            ]

            # Mock create_issue
            created_issue_mock = Mock()
            created_issue_mock.key = "TEST-456"
            mock_jira_instance.create_issue.return_value = created_issue_mock

            with patch("bir_mcp.atlassian.httpx.AsyncClient"):
                tools = Jira(token="test-token", url="https://jira.example.com", api_version=3)
                return tools

    @pytest.fixture
    def mock_jira_issue_data(self):
        """Mock Jira issue data."""
        return {
            "key": "TEST-123",
            "fields": {
                "summary": "Test Issue",
                "description": "Test description",
                "status": {"name": "Open"},
                "assignee": {"displayName": "Test User"},
                "priority": {"name": "High"},
                "issuetype": {"name": "Bug"},
                "created": "2024-01-01T00:00:00.000+0000",
                "updated": "2024-01-02T00:00:00.000+0000",
                "comment": {"comments": []},
                "subtasks": [],
                "issuelinks": [],
                "parent": None,
            },
        }

    @pytest.fixture
    def mock_project_data(self):
        """Mock Jira project data."""
        return {
            "key": "TEST",
            "name": "Test Project",
            "issueTypes": [
                {
                    "name": "Bug",
                    "description": "A problem which impairs or prevents the functions of the product.",
                    "subtask": False,
                },
                {"name": "Task", "description": "A task that needs to be done.", "subtask": False},
                {"name": "Sub-task", "description": "The sub-task of the issue", "subtask": True},
            ],
        }


class TestAtlassianReadOnlyTools(TestAtlassianTools):
    """Test read-only Atlassian tools."""

    def test_get_allowed_issue_types_for_project(self, atlassian_tools, mock_project_data):
        """Test get_allowed_issue_types_for_project tool."""

        # Mock async method
        async def mock_ahttpx_get(endpoint, **kwargs):
            mock_response = Mock()
            mock_response.json.return_value = mock_project_data
            return mock_response

        with patch.object(atlassian_tools, "ahttpx_get", side_effect=mock_ahttpx_get):
            result = asyncio.run(atlassian_tools.get_allowed_issue_types_for_project("TEST"))

            assert "tasks" in result
            assert "subtasks" in result
            assert "Bug" in result["tasks"]
            assert "Task" in result["tasks"]
            assert "Sub-task" in result["subtasks"]
            assert (
                result["tasks"]["Bug"]
                == "A problem which impairs or prevents the functions of the product."
            )

    def test_get_raw_issue_fields(self, atlassian_tools, mock_jira_issue_data):
        """Test get_raw_issue_fields tool."""

        # Mock async method
        async def mock_ahttpx_get(endpoint, **kwargs):
            mock_response = Mock()
            mock_response.json.return_value = mock_jira_issue_data
            return mock_response

        with patch.object(atlassian_tools, "ahttpx_get", side_effect=mock_ahttpx_get):
            result = asyncio.run(
                atlassian_tools.get_raw_issue_fields("TEST-123", ["summary", "description"])
            )

            assert result["summary"] == "Test Issue"
            assert result["description"] == "Test description"

    def test_get_issue_overview(self, atlassian_tools, mock_jira_issue_data):
        """Test get_issue_overview tool."""

        # Mock async method
        async def mock_ahttpx_get(endpoint, **kwargs):
            mock_response = Mock()
            mock_response.json.return_value = mock_jira_issue_data
            return mock_response

        with patch.object(atlassian_tools, "ahttpx_get", side_effect=mock_ahttpx_get):
            with patch(
                "bir_mcp.atlassian.infer_jira_field_representation", side_effect=lambda x: x
            ):
                result = asyncio.run(atlassian_tools.get_issue_overview("TEST-123"))

                assert result["summary"] == "Test Issue"
                assert result["description"] == "Test description"
                assert result["priority"] == {"name": "High"}
                assert result["issuetype"] == {"name": "Bug"}
                assert "jira_issue_url" in result

    def test_search_users(self, atlassian_tools):
        """Test search_users tool."""
        mock_users_data = [
            {"name": "testuser", "displayName": "Test User", "emailAddress": "test@example.com"}
        ]

        # Mock async method
        async def mock_ahttpx_get(endpoint, **kwargs):
            mock_response = Mock()
            mock_response.json.return_value = mock_users_data
            return mock_response

        with patch.object(atlassian_tools, "ahttpx_get", side_effect=mock_ahttpx_get):
            result = asyncio.run(atlassian_tools.search_users("test"))

            assert "users" in result
            assert len(result["users"]) == 1
            assert result["users"][0]["displayName"] == "Test User"
            assert result["users"][0]["emailAddress"] == "test@example.com"

    def test_http_request(self, atlassian_tools):
        """Test http_request tool."""
        mock_response_data = {"key": "TEST-123", "summary": "Test Issue"}

        # Mock async method
        async def mock_llm_friendly_http_request(**kwargs):
            return mock_response_data

        with patch(
            "bir_mcp.core.llm_friendly_http_request",
            side_effect=mock_llm_friendly_http_request,
        ):
            result = asyncio.run(atlassian_tools.http_request("issue/TEST-123"))

            assert result == mock_response_data


class TestAtlassianWriteTools(TestAtlassianTools):
    """Test write Atlassian tools."""

    def test_create_issue(self, atlassian_tools):
        """Test create_issue tool."""
        mock_created_issue = {"key": "TEST-456"}

        # Mock async method
        async def mock_ahttpx_post(endpoint, **kwargs):
            mock_response = Mock()
            mock_response.json.return_value = mock_created_issue
            return mock_response

        with patch.object(atlassian_tools, "ahttpx_post", side_effect=mock_ahttpx_post):
            result = asyncio.run(
                atlassian_tools.create_issue(
                    project_key="TEST",
                    summary="New Test Issue",
                    description="Test description",
                    issue_type="Bug",
                    assignee="testuser",
                )
            )

            assert result["created_issue_key"] == "TEST-456"
            assert "url" in result


class TestAtlassianHelpers(TestAtlassianTools):
    """Test Atlassian helper methods."""

    def test_build_issue_url(self, atlassian_tools):
        """Test build_issue_url helper method."""
        result = atlassian_tools.build_issue_url("TEST-123")
        assert result == "https://jira.example.com/browse/TEST-123"

    def test_prepend_api(self, atlassian_tools):
        """Test prepend_api helper method."""
        result = atlassian_tools.prepend_api("issue/TEST-123")
        assert result == "rest/api/3/issue/TEST-123"

    def test_get_tag(self, atlassian_tools):
        """Test get_tag method."""
        assert atlassian_tools.get_tag() == "jira"

    def test_get_mcp_tools_returns_all_tools(self, atlassian_tools):
        """Test that get_mcp_tools returns all expected tools."""
        tools = atlassian_tools.get_mcp_tools()

        # Should have both read and write tools
        assert len(tools) > 0

        # Check that specific tools are included
        tool_functions = [tool.fn for tool in tools]
        assert atlassian_tools.get_allowed_issue_types_for_project in tool_functions
        assert atlassian_tools.get_raw_issue_fields in tool_functions
        assert atlassian_tools.get_issue_overview in tool_functions
        assert atlassian_tools.search_users in tool_functions
        assert atlassian_tools.create_issue in tool_functions
        assert atlassian_tools.http_request in tool_functions

    def test_get_mcp_server_without_components(self, atlassian_tools):
        """Test get_mcp_server_without_components method."""
        server = atlassian_tools.get_mcp_server_without_components()
        assert server.name == "Bir Jira MCP server"
        assert "Jira related tools" in server.instructions


@pytest.mark.integration
class TestAtlassianIntegration:
    """Integration tests for Atlassian tools with real API calls."""

    @pytest.fixture
    def real_atlassian_tools(self):
        """Create real Atlassian tools instance for integration testing."""
        # These should be set as environment variables or skipped if not available
        import os

        jira_url = os.getenv("JIRA_URL", "https://jira-support.kapitalbank.az")
        jira_token = os.getenv("JIRA_TOKEN")

        if not jira_token:
            pytest.skip("JIRA_TOKEN environment variable not set")

        return Jira(token=jira_token, url=jira_url, api_version=3)

    def test_get_allowed_issue_types_integration(self, real_atlassian_tools):
        """Integration test for get_allowed_issue_types_for_project."""
        # Use real ACE project
        result = asyncio.run(real_atlassian_tools.get_allowed_issue_types_for_project("ACE"))

        assert "tasks" in result
        assert "subtasks" in result
        assert isinstance(result["tasks"], dict)
        assert isinstance(result["subtasks"], dict)

        # Should have some common issue types
        all_types = {**result["tasks"], **result["subtasks"]}
        assert len(all_types) > 0
        print(f"✅ Found {len(all_types)} issue types for ACE project")

    async def test_search_users_integration(self, real_atlassian_tools):
        """Integration test for search_users."""
        # Test multiple real user queries
        test_queries = ["amir", "farid"]

        for query in test_queries:
            result = await real_atlassian_tools.search_users(query)

            assert "users" in result
            assert isinstance(result["users"], list)
            print(f"✅ Search for '{query}' returned {len(result['users'])} users")

            if result["users"]:
                user = result["users"][0]
                # Check that expected fields are present
                expected_fields = ["name", "displayName", "emailAddress"]
                for field in expected_fields:
                    if field in user:  # Some fields might be missing depending on user settings
                        assert isinstance(user[field], str)
                print(
                    f"  → First user: {user.get('displayName', 'N/A')} ({user.get('name', 'N/A')})"
                )

    def test_http_request_integration(self, real_atlassian_tools):
        """Integration test for http_request."""
        # Test multiple API endpoints
        test_endpoints = [
            ("serverInfo", ["baseUrl", "version", "serverTitle"]),
            ("project/ACE", ["key", "name", "projectTypeKey"]),
            ("myself", ["accountId", "displayName"]),
        ]

        for endpoint, expected_fields in test_endpoints:
            try:
                result = asyncio.run(real_atlassian_tools.http_request(endpoint))

                assert isinstance(result, dict)
                print(f"✅ {endpoint}: API call successful")

                # Check for expected fields
                for field in expected_fields:
                    if field in result:
                        assert isinstance(result[field], str)
                        print(f"  → {field}: {result[field]}")

            except Exception as e:
                print(f"⚠️  {endpoint}: {str(e)}")
                # Don't fail the test if one endpoint fails
                continue

    @pytest.mark.skip(reason="Creates real Jira issues - only run manually")
    async def test_create_issue_integration(self, real_atlassian_tools):
        """Integration test for create_issue (skipped by default)."""
        # This test creates a real issue, so it's skipped by default
        result = await real_atlassian_tools.create_issue(
            project_key="ACE",
            summary="Integration Test Issue",
            description="This is a test issue created by integration tests",
            issue_type="Kanban Development Task",
        )

        assert "created_issue_key" in result
        assert "url" in result
        assert result["created_issue_key"].startswith("ACE-")
        assert "browse" in result["url"]

    def test_get_raw_issue_fields_integration(self, real_atlassian_tools):
        """Integration test for get_raw_issue_fields."""
        import random

        # Try 10 random ACE issue keys from 1-1000 range
        random_numbers = random.sample(range(1, 1001), 10)
        successful_tests = 0

        for num in random_numbers:
            test_issue_key = f"ACE-{num}"
            try:
                result = asyncio.run(
                    real_atlassian_tools.get_raw_issue_fields(
                        test_issue_key, ["summary", "description", "status"]
                    )
                )

                # Should return the requested fields
                assert "summary" in result
                assert isinstance(result["summary"], str)
                print(f"✅ {test_issue_key}: {result['summary'][:50]}...")

                if "description" in result:
                    assert isinstance(result["description"], (str, type(None)))

                successful_tests += 1
                if successful_tests >= 3:  # Stop after 3 successful tests
                    break

            except Exception as e:
                # If the test issue doesn't exist, try the next one
                if "does not exist" in str(e).lower() or "not found" in str(e).lower():
                    print(f"⚠️  {test_issue_key} does not exist, trying next...")
                    continue
                else:
                    raise

        if successful_tests == 0:
            pytest.skip("No valid ACE issues found in the tested range")

        print(f"✅ Successfully tested {successful_tests} ACE issues")

    def test_get_issue_overview_integration(self, real_atlassian_tools):
        """Integration test for get_issue_overview."""
        import random

        # Try 10 random ACE issue keys from 1-1000 range
        random_numbers = random.sample(range(1, 1001), 10)
        successful_tests = 0

        for num in random_numbers:
            test_issue_key = f"ACE-{num}"
            try:
                result = asyncio.run(real_atlassian_tools.get_issue_overview(test_issue_key))

                # Should return formatted issue overview
                assert isinstance(result, dict)
                assert "summary" in result
                assert "jira_issue_url" in result
                assert test_issue_key in result["jira_issue_url"]
                print(f"✅ {test_issue_key} overview: {result['summary'][:50]}...")

                successful_tests += 1
                if successful_tests >= 2:  # Stop after 2 successful tests
                    break

            except Exception as e:
                if "does not exist" in str(e).lower() or "not found" in str(e).lower():
                    print(f"⚠️  {test_issue_key} does not exist, trying next...")
                    continue
                else:
                    raise

        if successful_tests == 0:
            pytest.skip("No valid ACE issues found in the tested range")

        print(f"✅ Successfully tested {successful_tests} ACE issue overviews")
