"""Only leading HTTP error codes are safe bare status evidence."""

import pytest

from agentic_devtools.cli.ci.github_api_error import parse_bare_http_status


@pytest.mark.parametrize(
    ("stderr", "status"),
    [
        ("401 Bad credentials", 401),
        ("404 Not Found", 404),
        ("422: invalid", 422),
        ("https://github.com/o/r/issues/404", None),
        ("4040 rows", None),
        ("", None),
    ],
)
def test_leading_status_only(stderr: str, status: int | None) -> None:
    assert parse_bare_http_status(stderr) == status
