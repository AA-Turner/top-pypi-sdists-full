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
    InternedStore.preload([EVAL_PROJ_JSON, DEMO_PROJ_PROTO])

    specs_url, log_event_url = server_setup

    log_provider = MockOutputLoggerProvider()

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


@pytest.mark.parametrize("preload_kind", ["single", "multi"])
@pytest.mark.parametrize("precompute", ["omitted", "false", "true"])
def test_interned_store_mmap_preload(server_setup, preload_kind, precompute):
    _run_isolated(
        "_assert_interned_store_mmap_preload", *server_setup, preload_kind, precompute
    )


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


def _assert_interned_store_mmap_preload(specs_url, log_event_url, preload_kind, precompute):
    sdk_key = "secret-key"

    fetch_complete = InternedStore.fetch_and_write_mmap(sdk_key, specs_url)
    assert fetch_complete.wait(5)
    options = (
        {} if precompute == "omitted"
        else {"precompute_returnable_stable_hashes": precompute == "true"}
    )
    if preload_kind == "single":
        report = InternedStore.preload_mmap(required=sdk_key, **options)
        assert report.loaded == 1
        assert report.skipped_optional_indexes == []
    else:
        report = InternedStore.preload_mmap(
            required=[sdk_key], optional=[f"missing-{uuid.uuid4()}"], **options
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


@pytest.mark.parametrize("precompute", ["omitted", "false", "true"])
def test_interned_store_mmap_missing_required(precompute):
    _run_isolated("_assert_mmap_missing_required", precompute)


def _assert_mmap_missing_required(precompute):
    options = (
        {} if precompute == "omitted"
        else {"precompute_returnable_stable_hashes": precompute == "true"}
    )
    sdk_key = f"missing-{uuid.uuid4()}"
    message = "Invalid operation: No committed interned mmap V2 artifact was found"
    for preload, argument in (
        (InternedStore.preload_mmap, sdk_key),
        (InternedStore.preload_mmap, [sdk_key]),
    ):
        with pytest.raises(RuntimeError) as raised:
            preload(argument, **options)
        assert type(raised.value) is RuntimeError
        assert str(raised.value) == message
        assert raised.value.args == (message,)
        assert raised.value.error_name == "InvalidOperation"
        assert raised.value.error_message == message


@pytest.mark.parametrize("kind", ["single", "list"])
def test_byte_preload_unified_inputs(server_setup, kind):
    _run_isolated("_assert_byte_preload_unified_inputs", *server_setup, kind)


def _assert_byte_preload_unified_inputs(specs_url, log_event_url, kind):
    assert not hasattr(InternedStore, "preload_multi")
    assert not hasattr(InternedStore, "preload_mmap_multi")
    # Reject wrong input types before installing anything.
    for data in ("not bytes", [EVAL_PROJ_JSON, "not bytes"]):
        with pytest.raises(TypeError):
            InternedStore.preload(data)
    with pytest.raises(RuntimeError):
        InternedStore.preload([EVAL_PROJ_JSON, b"invalid"])
    data = EVAL_PROJ_JSON if kind == "single" else [EVAL_PROJ_JSON, DEMO_PROJ_PROTO]
    assert InternedStore.preload(data) is None
    statsig = Statsig("secret-key", StatsigOptions(specs_url=specs_url, log_event_url=log_event_url))
    statsig.initialize().wait()
    assert statsig.get_feature_gate(StatsigUser("a-user"), "test_public").value is True
    statsig.shutdown().wait()
    with pytest.raises(RuntimeError):
        InternedStore.preload(data)


@pytest.mark.parametrize("kind", ["single", "list"])
def test_optional_mmap_zero_then_partial_success(server_setup, kind):
    _run_isolated("_assert_optional_mmap_zero_then_partial_success", *server_setup, kind)


def _assert_optional_mmap_zero_then_partial_success(specs_url, log_event_url, kind):
    missing = f"missing-{uuid.uuid4()}"
    for kwargs in ({}, {"required": [], "optional": []}):
        with pytest.raises(RuntimeError):
            InternedStore.preload_mmap(**kwargs)
    for kwargs in ({"required": 1}, {"optional": [missing, 1]}):
        with pytest.raises(TypeError):
            InternedStore.preload_mmap(**kwargs)
    report = InternedStore.preload_mmap(optional=missing if kind == "single" else [missing])
    assert report.loaded == 0
    assert report.skipped_optional_indexes == [0]
    assert InternedStore.mmap_reader_memory_snapshot() is None

    key = f"available-{uuid.uuid4()}"
    assert InternedStore.fetch_and_write_mmap(key, specs_url).wait(5)
    # A required failure must roll back even if an earlier key loaded.
    with pytest.raises(RuntimeError):
        InternedStore.preload_mmap(required=[key, missing], optional=key)
    assert InternedStore.mmap_reader_memory_snapshot() is None
    report = InternedStore.preload_mmap(optional=[missing, key, key])
    assert report.loaded == 1
    assert report.skipped_optional_indexes == [0, 2]
    # Both mapped and unmapped SDK keys must still initialize and evaluate.
    for sdk_key in (key, missing):
        statsig = Statsig(sdk_key, StatsigOptions(specs_url=specs_url, log_event_url=log_event_url))
        statsig.initialize().wait()
        assert statsig.get_feature_gate(StatsigUser("a-user"), "test_public").value is True
        statsig.shutdown().wait()
    with pytest.raises(RuntimeError):
        InternedStore.preload_mmap(optional=missing)
