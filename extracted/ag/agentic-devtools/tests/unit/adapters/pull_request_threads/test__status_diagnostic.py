import pytest

from agentic_devtools.adapters.pull_request_threads import _status_diagnostic


@pytest.mark.parametrize(
    ("status_code", "diagnostic"),
    [
        (401, "unauthorized"),
        (403, "forbidden"),
        (404, "not_found"),
        (409, "conflict"),
        (422, "invalid_request"),
        (429, "rate_limited"),
        (400, "provider_error"),
        (500, "provider_unavailable"),
    ],
)
def test_status_codes_have_stable_diagnostics(status_code: int, diagnostic: str) -> None:
    assert _status_diagnostic(status_code) == diagnostic
