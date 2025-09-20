import httpx
from graphql import (
    DocumentNode,
    FieldNode,
    NameNode,
    OperationDefinitionNode,
    OperationType,
    SelectionSetNode,
)

from connector.tests.mock_httpx import (
    _add_single_response,
    _build_url,
    mock_graphql_request_body,
    mock_requests,
)
from connector.tests.type_definitions import MockedResponse


class TestBuildUrl:
    """Test the _build_url helper function."""

    def test_build_url_with_absolute_url(self):
        """Should return absolute URL unchanged."""
        url = "https://example.com/api/endpoint"
        result = _build_url(url)
        assert result == "https://example.com/api/endpoint"

    def test_build_url_with_absolute_url_and_host(self):
        """Should return absolute URL unchanged, ignoring host."""
        url = "https://example.com/api/endpoint"
        host = "https://ignored.com"
        result = _build_url(url, host)
        assert result == "https://example.com/api/endpoint"

    def test_build_url_with_relative_path_and_host(self):
        """Should combine host with relative path."""
        path = "/api/endpoint"
        host = "https://example.com"
        result = _build_url(path, host)
        assert result == "https://example.com/api/endpoint"

    def test_build_url_with_relative_path_no_host(self):
        """Should use empty string as host when None provided."""
        path = "/api/endpoint"
        result = _build_url(path)
        assert result == "/api/endpoint"

    def test_build_url_with_relative_path_empty_host(self):
        """Should handle empty host string."""
        path = "/api/endpoint"
        host = ""
        result = _build_url(path, host)
        assert result == "/api/endpoint"

    def test_build_url_with_empty_path(self):
        """Should handle empty path."""
        path = ""
        host = "https://example.com"
        result = _build_url(path, host)
        assert result == "https://example.com"

    def test_build_url_edge_case_https_in_path(self):
        """Should only consider URLs starting with https:// as absolute."""
        path = "some-https://weird-path"
        host = "https://example.com"
        result = _build_url(path, host)
        assert result == "https://example.comsome-https://weird-path"


class TestAddSingleResponse:
    """Test the _add_single_response helper function."""

    def test_add_response_basic_functionality(self):
        """Test that _add_single_response works without raising exceptions."""

        # Create a mock that behaves like HTTPXMock for our purposes
        class MockHTTPX:
            def add_response(self, **kwargs):
                # Store the parameters to verify they were passed correctly
                self.last_call = kwargs

        mock = MockHTTPX()
        response = MockedResponse(
            status_code=httpx.codes.OK,
            response_body={"key": "value"},
            headers={"Content-Type": "application/json"},
        )

        # Should not raise any exceptions and should pass the right parameters
        _add_single_response(mock, "GET", "https://test.com", response)

        # Verify the mock was called with expected parameters
        assert mock.last_call["method"] == "GET"
        assert mock.last_call["url"] == "https://test.com"
        assert mock.last_call["json"] == {"key": "value"}
        assert mock.last_call["status_code"] == httpx.codes.OK

    def test_add_response_string_body_handling(self):
        """Test string response body is handled correctly."""

        class MockHTTPX:
            def add_response(self, **kwargs):
                self.last_call = kwargs

        mock = MockHTTPX()
        response = MockedResponse(
            status_code=httpx.codes.CREATED,
            response_body="plain text response",
        )

        _add_single_response(mock, "POST", "https://test.com", response)

        # String response should be passed as 'text' parameter
        assert mock.last_call["text"] == "plain text response"
        assert mock.last_call["json"] == "plain text response"

    def test_add_response_none_body_handling(self):
        """Test None response body is handled correctly."""

        class MockHTTPX:
            def add_response(self, **kwargs):
                self.last_call = kwargs

        mock = MockHTTPX()
        response = MockedResponse(
            status_code=httpx.codes.NO_CONTENT,
            response_body=None,
        )

        _add_single_response(mock, "DELETE", "https://test.com", response)

        # None response should be passed as-is
        assert mock.last_call["json"] is None
        assert mock.last_call["text"] is None


class TestMockGraphqlRequestBody:
    """Test the mock_graphql_request_body function."""

    def test_mock_graphql_without_variables(self):
        """Should create request body with query only."""
        query_doc = DocumentNode(
            definitions=[
                OperationDefinitionNode(
                    operation=OperationType.QUERY,
                    selection_set=SelectionSetNode(
                        selections=[FieldNode(name=NameNode(value="hello"))]
                    ),
                )
            ]
        )

        result = mock_graphql_request_body(query_doc)

        assert "query" in result
        assert "hello" in result["query"]
        assert "variables" not in result

    def test_mock_graphql_with_variables(self):
        """Should create request body with query and variables."""
        query_doc = DocumentNode(
            definitions=[
                OperationDefinitionNode(
                    operation=OperationType.QUERY,
                    selection_set=SelectionSetNode(
                        selections=[FieldNode(name=NameNode(value="hello"))]
                    ),
                )
            ]
        )

        variables = {"name": "test", "id": 123}

        result = mock_graphql_request_body(query_doc, variables)

        assert "query" in result
        assert "variables" in result
        assert result["variables"] == {"name": "test", "id": 123}

    def test_mock_graphql_with_empty_variables(self):
        """Should not include variables when empty dict provided."""
        query_doc = DocumentNode(
            definitions=[
                OperationDefinitionNode(
                    operation=OperationType.QUERY,
                    selection_set=SelectionSetNode(
                        selections=[FieldNode(name=NameNode(value="hello"))]
                    ),
                )
            ]
        )

        result = mock_graphql_request_body(query_doc, {})

        assert "query" in result
        assert "variables" not in result


class TestMockRequests:
    """Test the mock_requests function with comprehensive code path coverage."""

    def test_mock_requests_with_none_response_map(self):
        """Should return early when response_body_map is None."""

        class MockHTTPX:
            def __init__(self):
                self.calls = []

            def add_response(self, **kwargs):
                self.calls.append(kwargs)

        mock = MockHTTPX()
        mock_requests(None, mock)

        # Should not have made any calls
        assert len(mock.calls) == 0

    def test_mock_requests_with_empty_response_map(self):
        """Should return early when response_body_map is empty dict."""

        class MockHTTPX:
            def __init__(self):
                self.calls = []

            def add_response(self, **kwargs):
                self.calls.append(kwargs)

        mock = MockHTTPX()
        mock_requests({}, mock)

        # Should not have made any calls
        assert len(mock.calls) == 0

    def test_mock_requests_dict_responses_single_response(self):
        """Should handle dict responses with single MockedResponse."""

        class MockHTTPX:
            def __init__(self):
                self.calls = []

            def add_response(self, **kwargs):
                self.calls.append(kwargs)

        mock = MockHTTPX()
        response_map = {
            "GET": {
                "/api/test": MockedResponse(
                    status_code=httpx.codes.OK, response_body={"success": True}
                )
            }
        }

        mock_requests(response_map, mock, host="https://api.com")

        # Should have made one call
        assert len(mock.calls) == 1
        call = mock.calls[0]
        assert call["method"] == "GET"
        assert call["url"] == "https://api.com/api/test"
        assert call["json"] == {"success": True}

    def test_mock_requests_dict_responses_list_responses(self):
        """Should handle dict responses with list of MockedResponse."""

        class MockHTTPX:
            def __init__(self):
                self.calls = []

            def add_response(self, **kwargs):
                self.calls.append(kwargs)

        mock = MockHTTPX()
        response_map = {
            "POST": {
                "/api/create": [
                    MockedResponse(status_code=httpx.codes.CREATED, response_body={"id": 1}),
                    MockedResponse(status_code=httpx.codes.CREATED, response_body={"id": 2}),
                ]
            }
        }

        mock_requests(response_map, mock, host="https://api.com")

        # Should have made two calls
        assert len(mock.calls) == 2
        assert all(call["method"] == "POST" for call in mock.calls)
        assert all(call["url"] == "https://api.com/api/create" for call in mock.calls)

    def test_mock_requests_list_responses(self):
        """Should handle direct list responses."""

        class MockHTTPX:
            def __init__(self):
                self.calls = []

            def add_response(self, **kwargs):
                self.calls.append(kwargs)

        mock = MockHTTPX()
        response_map = {
            "DELETE": [
                MockedResponse(
                    status_code=httpx.codes.NO_CONTENT,
                    response_body=None,
                    request_path="/api/delete/1",
                ),
                MockedResponse(
                    status_code=httpx.codes.NO_CONTENT,
                    response_body=None,
                    request_path="/api/delete/2",
                ),
            ]
        }

        mock_requests(response_map, mock, host="https://api.com")

        # Should have made two calls
        assert len(mock.calls) == 2
        assert mock.calls[0]["url"] == "https://api.com/api/delete/1"
        assert mock.calls[1]["url"] == "https://api.com/api/delete/2"

    def test_mock_requests_absolute_urls_in_dict(self):
        """Should handle absolute URLs in dict responses."""

        class MockHTTPX:
            def __init__(self):
                self.calls = []

            def add_response(self, **kwargs):
                self.calls.append(kwargs)

        mock = MockHTTPX()
        response_map = {
            "GET": {
                "https://external-api.com/data": MockedResponse(
                    status_code=httpx.codes.OK, response_body={"external": True}
                )
            }
        }

        mock_requests(response_map, mock)

        # Should use absolute URL as-is
        assert len(mock.calls) == 1
        assert mock.calls[0]["url"] == "https://external-api.com/data"

    def test_mock_requests_url_building_logic(self):
        """Test that URL building works correctly for different cases."""

        class MockHTTPX:
            def __init__(self):
                self.calls = []

            def add_response(self, **kwargs):
                self.calls.append(kwargs)

        mock = MockHTTPX()

        # Test relative paths with host
        response_map = {
            "GET": {"/path": MockedResponse(status_code=httpx.codes.OK, response_body={})}
        }
        mock_requests(response_map, mock, host="https://example.com")
        assert mock.calls[0]["url"] == "https://example.com/path"

        # Test absolute URLs (should ignore host)
        mock.calls.clear()
        response_map = {
            "GET": {
                "https://absolute.com/path": MockedResponse(
                    status_code=httpx.codes.OK, response_body={}
                )
            }
        }
        mock_requests(response_map, mock, host="https://ignored.com")
        assert mock.calls[0]["url"] == "https://absolute.com/path"

    def test_mock_requests_handles_all_response_body_types(self):
        """Test different response body types are handled correctly."""

        class MockHTTPX:
            def __init__(self):
                self.calls = []

            def add_response(self, **kwargs):
                self.calls.append(kwargs)

        mock = MockHTTPX()

        response_map = {
            "GET": {
                "/json": MockedResponse(status_code=httpx.codes.OK, response_body={"json": True}),
                "/string": MockedResponse(
                    status_code=httpx.codes.OK, response_body="text response"
                ),
                "/none": MockedResponse(status_code=httpx.codes.NO_CONTENT, response_body=None),
            }
        }

        mock_requests(response_map, mock, host="https://api.com")

        # Should handle different response types correctly
        json_call = next(call for call in mock.calls if call["url"].endswith("/json"))
        string_call = next(call for call in mock.calls if call["url"].endswith("/string"))
        none_call = next(call for call in mock.calls if call["url"].endswith("/none"))

        assert json_call["json"] == {"json": True}
        assert string_call["text"] == "text response"
        assert none_call["json"] is None
