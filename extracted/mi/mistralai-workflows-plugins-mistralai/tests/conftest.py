import os

import pytest

from mistralai.workflows.testing.fixtures import (
    clear_dependency_cache,  # noqa: F401
    disable_otel_export,  # noqa: F401
    event_loop,  # noqa: F401
    mock_upsert_search_attributes,  # noqa: F401
    setup_test_config,  # noqa: F401
    temporal_env,  # noqa: F401
)


@pytest.fixture(scope="module")
def vcr_config():
    def before_record_request(request):
        url = request.uri
        if "api.mistral.ai" not in url:
            return None
        return request

    return {
        "record_mode": os.getenv("VCR_RECORD_MODE", "none"),
        "match_on": ["method", "host", "path"],
        "filter_headers": [
            ("authorization", "REDACTED"),
            ("x-api-key", "REDACTED"),
            ("set-cookie", "<IGNORED>"),
            ("cf-ray", "<IGNORED>"),
            ("date", "<IGNORED>"),
            ("mistral-correlation-id", "<IGNORED>"),
            ("x-kong-request-id", "<IGNORED>"),
            ("x-envoy-upstream-service-time", "<IGNORED>"),
        ],
        "before_record_request": before_record_request,
        "ignore_localhost": True,
        "cassette_library_dir": "tests/agents/cassettes",
        "decode_compressed_response": True,
    }


@pytest.fixture
def mock_mistral_client():
    """Fixture for mocking mistral client responses."""
    pass
