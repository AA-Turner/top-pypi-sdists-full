import typing as t

from graphql import DocumentNode, print_ast
from pytest_httpx import HTTPXMock

from connector.tests.type_definitions import ResponseBodyMap


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

    for method, requests in response_body_map.items():
        if isinstance(requests, dict):
            for request_line, response in requests.items():
                if isinstance(response.response_body, str):
                    httpx_mock.add_response(
                        method=method,
                        url=f"{host or ''}{request_line}",
                        content=response.response_body.encode(),
                        status_code=response.status_code,
                    )
                else:
                    httpx_mock.add_response(
                        method=method,
                        url=f"{host or ''}{request_line}",
                        json=response.response_body,
                        status_code=response.status_code,
                        headers=response.headers if response.headers else None,
                        match_json=response.request_json_body
                        if response.request_json_body
                        else None,
                    )
        elif isinstance(requests, list):
            for response in requests:
                if isinstance(response.response_body, str):
                    httpx_mock.add_response(
                        method=method,
                        url=host or "",
                        content=response.response_body.encode(),
                        status_code=response.status_code,
                    )
                else:
                    httpx_mock.add_response(
                        method=method,
                        url=host or "",
                        json=response.response_body,
                        status_code=response.status_code,
                        headers=response.headers if response.headers else None,
                        match_json=response.request_json_body
                        if response.request_json_body
                        else None,
                    )
