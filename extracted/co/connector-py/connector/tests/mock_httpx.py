import typing as t

from graphql import DocumentNode, print_ast
from pytest_httpx import HTTPXMock

from connector.tests.type_definitions import MockedResponse, ResponseBodyMap


def _build_url(request_line_or_path: str, host: str | None = None) -> str:
    """Build complete URL from request line/path and optional host."""
    if request_line_or_path.startswith("https://"):
        return request_line_or_path
    return f"{host or ''}{request_line_or_path}"


def _add_single_response(
    httpx_mock: HTTPXMock, method: str, url: str, response: MockedResponse
) -> None:
    """Add a single mocked response to httpx_mock."""
    httpx_mock.add_response(
        method=method,
        url=url,
        json=response.response_body,
        text=(response.response_body if isinstance(response.response_body, str) else None),
        status_code=response.status_code,
        headers=response.headers if response.headers else None,
        match_json=response.request_json_body,
        match_content=response.request_bytes_body,
    )


def mock_graphql_request_body(
    query: DocumentNode, variables: dict[str, t.Any] | None = None
) -> dict[str, t.Any]:
    body: dict[str, t.Any] = {"query": print_ast(query)}

    if variables:
        body.update({"variables": variables})

    return body


def mock_requests(
    response_body_map: ResponseBodyMap, httpx_mock: HTTPXMock, *, host: str | None = None
):
    if not response_body_map:
        # Don't mock any requests, and use the default behavior of
        # httpx_mock which is HTTP 200, empty body
        return

    for method, responses in response_body_map.items():
        if isinstance(responses, dict):
            for request_line, response in responses.items():
                url = _build_url(request_line, host)

                if isinstance(response, list):
                    for one_response in response:
                        _add_single_response(httpx_mock, method, url, one_response)
                else:
                    _add_single_response(httpx_mock, method, url, response)

        elif isinstance(responses, list):
            for response in responses:
                url = _build_url(response.request_path or "", host)
                _add_single_response(httpx_mock, method, url, response)
