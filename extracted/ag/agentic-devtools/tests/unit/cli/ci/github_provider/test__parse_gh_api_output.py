"""Tests for _parse_gh_api_output()."""

from agentic_devtools.cli.ci.github_provider import _parse_gh_api_output


def test_parse_gh_api_output_preserves_paginated_bodies_and_latest_headers() -> None:
    raw = (
        'HTTP/2 200 OK\nRetry-After: bad\n\n[{"id": 1}]\n'
        'HTTP/2 200 OK\nRetry-After: 12\nX-RateLimit-Reset: bad, 500\n\n[{"id": 2}]\n'
    )
    status, headers, body = _parse_gh_api_output(raw)
    assert status == 200
    assert headers["retry-after"] == "12"
    assert body == '[{"id": 1}]\n[{"id": 2}]\n'
    assert _parse_gh_api_output("HTTP/1.1 204 No Content\n") == (204, {}, "")


def test_parse_gh_api_output_keeps_plain_text_status_like_body_lines() -> None:
    raw = "HTTP/2 200 OK\nContent-Type: text/plain\n\nfirst\nHTTP/1.1 503 Service Unavailable\nstill body\n"

    status, headers, body = _parse_gh_api_output(raw)

    assert status == 200
    assert headers == {"content-type": "text/plain"}
    assert body == "first\nHTTP/1.1 503 Service Unavailable\nstill body\n"


def test_parse_gh_api_output_keeps_status_like_body_without_header_shape() -> None:
    raw = "HTTP/2 200 OK\nContent-Type: text/plain\n\nfirst\nHTTP/1.1 503\nbody\n"

    status, headers, body = _parse_gh_api_output(raw)

    assert status == 200
    assert headers == {"content-type": "text/plain"}
    assert body == "first\nHTTP/1.1 503\nbody\n"


def test_parse_gh_api_output_keeps_status_like_body_without_header_terminator() -> None:
    raw = "HTTP/2 200 OK\nContent-Type: text/plain\n\nfirst\nHTTP/1.1 503\nRetry-After: 5"

    status, headers, body = _parse_gh_api_output(raw)

    assert status == 200
    assert headers == {"content-type": "text/plain"}
    assert body == "first\nHTTP/1.1 503\nRetry-After: 5"
