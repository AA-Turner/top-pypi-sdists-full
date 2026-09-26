import json
import subprocess
import sys
import uuid
from pathlib import Path

import pytest
from pytest_httpserver import HTTPServer

from mock_output_logger import MockOutputLoggerProvider
from statsig_python_core import InternedStore, Statsig, StatsigOptions, StatsigUser
from utils import get_test_data_resource, get_test_data_resource_bytes

EVAL_PROJ_JSON = get_test_data_resource_bytes("eval_proj_dcs.json")
DEMO_PROJ_PROTO = get_test_data_resource_bytes("demo_proj_dcs.pb.br")


@pytest.fixture
def server_setup(httpserver: HTTPServer):
    dcs_content = get_test_data_resource("eval_proj_dcs.json")
    json_data = json.loads(dcs_content)

    httpserver.expect_request(
        "/v2/download_config_specs"
    ).respond_with_json(json_data)
    httpserver.expect_request(
        "/v2/download_config_specs", headers={"STATSIG-API-KEY": "secret-key"}
    ).respond_with_json(json_data)

    httpserver.expect_request("/v1/log_event").respond_with_json({"success": True})

    yield (
        httpserver.url_for("/v2/download_config_specs"),
        httpserver.url_for("/v1/log_event"),
    )


def test_interned_store_preload(server_setup):
    InternedStore.preload_multi([EVAL_PROJ_JSON, DEMO_PROJ_PROTO])

    specs_url, log_event_url = server_setup

    log_provider = MockOutputLoggerProvider()
    log_provider.logs = []

    statsig = Statsig(
        "secret-key",
        StatsigOptions(
            specs_url=specs_url,
            log_event_url=log_event_url,
            output_logger_provider=log_provider,
        ),
    )
    statsig.initialize().wait()
    gate = statsig.get_feature_gate(StatsigUser("a-user"), "test_public")
    statsig.shutdown().wait()

    assert gate.details.reason == "Network:Recognized"
    assert log_provider.error_count == 0


def test_interned_store_mmap_preload(server_setup):
    _run_isolated("_assert_interned_store_mmap_preload", *server_setup)


def _run_isolated(function_name, *args):
    subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import sys; "
                "sys.path.insert(0, '.'); "
                "import test_interned_store_preload as tests; "
                "getattr(tests, sys.argv[1])(*sys.argv[2:])"
            ),
            function_name,
            *args,
        ],
        cwd=Path(__file__).parent,
        check=True,
        timeout=30,
    )


def _assert_interned_store_mmap_preload(specs_url, log_event_url):
    sdk_key = "secret-key"

    fetch_complete = InternedStore.fetch_and_write_mmap(sdk_key, specs_url)
    assert fetch_complete.wait(5)
    report = InternedStore.preload_mmap_multi(
        [sdk_key], [f"missing-{uuid.uuid4()}"]
    )
    assert report.loaded == 1
    assert report.skipped_optional_indexes == [0]

    memory = InternedStore.mmap_reader_memory_snapshot()
    assert memory is not None
    assert memory.format_version == 2
    assert memory.mapped_bytes > 0
    assert memory.loaded_generation_count == 1
    if sys.platform == "linux":
        assert memory.resident_bytes is not None
        assert memory.proportional_set_bytes is not None
        assert memory.private_dirty_bytes is not None
        assert memory.deleted_mapped_bytes == 0
        assert memory.vma_segment_count is not None
        assert memory.vma_segment_count >= 1
    else:
        assert memory.resident_bytes is None
        assert memory.proportional_set_bytes is None
        assert memory.private_dirty_bytes is None
        assert memory.deleted_mapped_bytes is None
        assert memory.vma_segment_count is None

    log_provider = MockOutputLoggerProvider()
    log_provider.logs = []

    statsig = Statsig(
        sdk_key,
        StatsigOptions(
            specs_url=specs_url,
            log_event_url=log_event_url,
            output_logger_provider=log_provider,
        ),
    )
    statsig.initialize().wait()
    gate = statsig.get_feature_gate(StatsigUser("a-user"), "test_public")
    config = statsig.get_dynamic_config(StatsigUser("a-user"), "big_number")
    statsig.shutdown().wait()

    assert gate.details.reason == "Network:Recognized"
    assert config.value["foo"] == 1e21
    assert isinstance(config.value["foo"], float)
    assert log_provider.error_count == 0


def test_interned_store_mmap_missing_required():
    _run_isolated("_assert_mmap_missing_required")


def _assert_mmap_missing_required():
    sdk_key = f"missing-{uuid.uuid4()}"
    message = "Invalid operation: No committed interned mmap V2 artifact was found"
    for preload, argument in (
        (InternedStore.preload_mmap, sdk_key),
        (InternedStore.preload_mmap_multi, [sdk_key]),
    ):
        with pytest.raises(RuntimeError) as raised:
            preload(argument)
        assert type(raised.value) is RuntimeError
        assert str(raised.value) == message
        assert raised.value.args == (message,)
        assert raised.value.error_name == "InvalidOperation"
        assert raised.value.error_message == message
