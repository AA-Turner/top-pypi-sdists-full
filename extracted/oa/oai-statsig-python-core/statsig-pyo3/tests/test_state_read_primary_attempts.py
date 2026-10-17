import pytest
from statsig_python_core import Statsig, StatsigOptions
from werkzeug.wrappers import Response


@pytest.mark.parametrize("attempts", [None, 0, -1, 1, 2, 4294967296])
def test_state_read_primary_attempts_native(httpserver, attempts):
    requests = []

    def fail(request):
        requests.append(request)
        return Response("retry", status=503)

    httpserver.expect_request("/v2/download_config_specs").respond_with_handler(fail)
    statsig = Statsig("secret-retry-option", StatsigOptions(
        specs_url=httpserver.url_for("/v2/download_config_specs"),
        state_read_primary_attempts=attempts,
        init_timeout_ms=5000,
        prefer_http2=False,
        disable_all_logging=True,
        disable_country_lookup=True,
        output_log_level="none",
    ))
    try:
        statsig.initialize().wait()
        assert len(requests) == (attempts if attempts in (1, 2) else 2)
    finally:
        statsig.shutdown().wait()


def test_state_read_primary_attempts_python_conversion():
    with pytest.raises((TypeError, OverflowError)):
        StatsigOptions(state_read_primary_attempts=1.5)
    with pytest.raises(OverflowError):
        StatsigOptions(state_read_primary_attempts=2**63)
