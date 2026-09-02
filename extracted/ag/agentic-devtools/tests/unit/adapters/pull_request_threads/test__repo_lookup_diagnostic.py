import pytest

from agentic_devtools.adapters.pull_request_threads import _repo_lookup_diagnostic


@pytest.mark.parametrize(
    ("message", "diagnostic"),
    [
        ("REST API returned 401: Unauthorized", "unauthorized"),
        ("REST API returned 403: Forbidden", "forbidden"),
        ("REST API returned 404: Not Found", "not_found"),
        ("REST API returned 429: Too Many Requests", "rate_limited"),
        ("REST API returned 500: Internal Server Error", "provider_unavailable"),
        ("REST API returned 503: Service Unavailable", "provider_unavailable"),
        ("REST API returned 123: Continue", "provider_unavailable"),
        ("Azure CLI not found", "provider_unavailable"),
        ("REST lookup failed for 'repo': REST API returned 401: Unauthorized", "unauthorized"),
        ("REST lookup failed for '404': REST API returned 401: Unauthorized", "unauthorized"),
        ("Error code 123 is not HTTP", "provider_unavailable"),
    ],
)
def test_maps_runtime_error_message_to_diagnostic(message: str, diagnostic: str) -> None:
    assert _repo_lookup_diagnostic(RuntimeError(message)) == diagnostic
