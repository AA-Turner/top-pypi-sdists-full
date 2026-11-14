import json
import time

import pytest

from statsig_python_core import EvaluationCache, Statsig, StatsigOptions
from test_observability_client import MockObservabilityClient
from mock_scrapi import MockScrapi
from utils import get_test_data_resource


def test_default_statsig_options():
    options = StatsigOptions()
    assert options.specs_url is None
    assert options.service_name is None
    assert options.runtime_thread_start_callback is None
    assert options.evaluation_cache is None
    assert options.prefer_http2 is None
    assert options.disable_remote_telemetry is None
    assert options.shared_id_lists_dir is None
    assert options.id_list_init_build_concurrency is None
    assert options.lazy_load_id_lists is None


def test_lazy_id_list_option():
    options = StatsigOptions(lazy_load_id_lists=True)
    assert options.lazy_load_id_lists is True
    options.lazy_load_id_lists = False
    assert options.lazy_load_id_lists is False
    options.lazy_load_id_lists = None
    assert options.lazy_load_id_lists is None


@pytest.mark.parametrize("value", ["true", "false", [], {}])
def test_lazy_id_list_option_rejects_invalid_values(value):
    with pytest.raises(TypeError):
        StatsigOptions(lazy_load_id_lists=value)


def test_shared_id_lists_directory_option():
    options = StatsigOptions(shared_id_lists_dir="/tmp/statsig-id-lists")
    assert options.shared_id_lists_dir == "/tmp/statsig-id-lists"
    options.shared_id_lists_dir = "/tmp/other-id-lists"
    assert options.shared_id_lists_dir == "/tmp/other-id-lists"
    options.shared_id_lists_dir = None
    assert options.shared_id_lists_dir is None


def test_prefer_http2_supported_option():
    options = StatsigOptions(prefer_http2=True)
    assert options.prefer_http2 is True
    assert options.experimental_flags is None
    options.prefer_http2 = False
    assert options.prefer_http2 is False
    options.prefer_http2 = None
    assert options.prefer_http2 is None


def test_initialize_partial_statsig_options():
    options = StatsigOptions(
        specs_url="https://statsigcdn.openai.com/v1",
    )
    assert options.specs_url == "https://statsigcdn.openai.com/v1"
    assert options.log_event_url is None


def test_positional_statsig_options_preserve_existing_order():
    options = StatsigOptions(None, 1000)

    assert options.specs_sync_interval_ms == 1000


def test_evaluation_cache_option():
    cache = EvaluationCache(max_bytes=1024, max_entry_bytes=512)
    options = StatsigOptions(evaluation_cache=cache)
    assert options.evaluation_cache is cache

    replacement = EvaluationCache(max_bytes=2048, max_entry_bytes=1024)
    options.evaluation_cache = replacement
    assert options.evaluation_cache is replacement

    options.evaluation_cache = None
    assert options.evaluation_cache is None


def test_runtime_thread_start_callback_option():
    def callback():
        pass

    options = StatsigOptions(runtime_thread_start_callback=callback)
    assert options.runtime_thread_start_callback is callback

    def replacement():
        pass

    options.runtime_thread_start_callback = replacement
    assert options.runtime_thread_start_callback is replacement

    options.runtime_thread_start_callback = None
    assert options.runtime_thread_start_callback is None


# Mostly testing that there are no errors
def test_full_statsig_options():
    options = StatsigOptions(
        specs_url="https://statsigcdn.openai.com/v1",
        specs_sync_interval_ms=1000,
        init_timeout_ms=1000,
        log_event_url="https://api.oaistatsig.com/v1/log_event",
        disable_all_logging=True,
        event_logging_flush_interval_ms=1000,
        event_logging_max_queue_size=1000,
        enable_id_lists=False,
        wait_for_user_agent_init=False,
        wait_for_country_lookup_init=False,
        id_lists_url="https://statsigcdn.openai.com/v1/id_lists",
        id_lists_sync_interval_ms=1000,
        fallback_to_statsig_api=False,
        environment="production",
        service_name="statsig-python-service",
        output_log_level="debug",
        global_custom_fields={"key": "value"},
        observability_client=MockObservabilityClient(),
    )
    assert options.specs_url == "https://statsigcdn.openai.com/v1"
    assert options.log_event_url == "https://api.oaistatsig.com/v1/log_event"
    assert options.specs_sync_interval_ms == 1000
    assert options.output_log_level == "debug"
    assert options.service_name == "statsig-python-service"


@pytest.mark.parametrize("disabled", [True, False, None])
def test_remote_telemetry_option_reaches_core(httpserver, disabled):
    scrapi = MockScrapi(httpserver)
    specs = json.loads(get_test_data_resource("eval_proj_dcs.json"))
    specs.pop("checksum", None)
    scrapi.stub("/v2/download_config_specs", json.dumps(specs))
    scrapi.stub("/v1/log_event", '{"success": true}', method="POST")
    statsig = Statsig("secret-option-fixture", StatsigOptions(
        specs_url=scrapi.url_for_endpoint("/v2/download_config_specs"),
        log_event_url=scrapi.url_for_endpoint("/v1/log_event"),
        **({"disable_remote_telemetry": disabled} if disabled is not None else {}),
    ))
    try:
        statsig.initialize().wait()
        deadline = time.monotonic() + 1
        # Diagnostic delivery is asynchronous; bound both presence and absence checks.
        while True:
            statsig.flush_events().wait()
            diagnostics = [
                e for e in scrapi.get_logged_events(include_diagnostics=True)
                if e["eventName"] == "statsig::diagnostics"
            ]
            if diagnostics or time.monotonic() >= deadline:
                break
            time.sleep(0.01)
        assert bool(diagnostics) is (disabled is not True)
    finally:
        statsig.shutdown().wait()


def test_appended_statsig_options_preserve_existing_positions():
    options = StatsigOptions(
        *([None] * 39), True, 3, "/tmp/shared-id-lists", False, True, 8, False, True
    )
    assert options.prefer_http2 is True
    assert options.state_read_primary_attempts == 3
    assert options.shared_id_lists_dir == "/tmp/shared-id-lists"
    assert options.enable_id_list_elias_fano is False
    assert options.disable_remote_telemetry is True
    assert options.id_list_init_build_concurrency == 8
    assert options.enable_id_list_access_metrics is False
    assert options.lazy_load_id_lists is True
