"""Unit tests for the version-keyed UDF sidecar registry."""

import threading

import pytest

from sagemaker_studio.utils.udf.registry import (
    SidecarEntry,
    clear_registry,
    client_python_version,
    get_sidecar,
    normalize_python_version,
    register_sidecar,
    registered_versions,
    unregister_sidecar,
)


@pytest.fixture(autouse=True)
def _clean_registry():
    clear_registry()
    yield
    clear_registry()


class _Builder:
    def __init__(self, spark_version):
        self.spark_version = spark_version

    def build(self, request):
        return {"ok": True, "spark_version": self.spark_version}


def test_normalize_drops_the_patch_component():
    assert normalize_python_version("3.11.13") == "3.11"
    assert normalize_python_version("3.13") == "3.13"


def test_normalize_rejects_something_with_no_minor():
    with pytest.raises(ValueError):
        normalize_python_version("3")


def test_client_python_version_is_major_minor():
    import sys

    assert client_python_version() == "%d.%d" % sys.version_info[:2]


def test_register_then_get_round_trips():
    entry = register_sidecar("3.13", lambda spark_version: _Builder(spark_version))
    assert isinstance(entry, SidecarEntry)
    assert get_sidecar("3.13") is entry
    assert get_sidecar("3.13.7") is entry  # normalized lookup
    assert registered_versions() == ["3.13"]


def test_get_returns_none_for_an_unregistered_version():
    assert get_sidecar("3.9") is None


def test_factory_is_lazy_and_called_once_per_spark_version():
    calls = []

    def factory(spark_version):
        calls.append(spark_version)
        return _Builder(spark_version)

    entry = register_sidecar("3.13", factory)
    assert calls == []  # registration must not invoke the factory

    first = entry.builder("4.1.1")
    second = entry.builder("4.1.1")
    assert first is second
    assert calls == ["4.1.1"]

    other = entry.builder("3.5.6")
    assert other is not first
    assert calls == ["4.1.1", "3.5.6"]


def test_concurrent_first_use_creates_exactly_one_builder():
    calls = []
    gate = threading.Event()

    def factory(spark_version):
        gate.wait(5)
        calls.append(spark_version)
        return _Builder(spark_version)

    entry = register_sidecar("3.13", factory)
    results = []
    threads = [
        threading.Thread(target=lambda: results.append(entry.builder("4.1.1"))) for _ in range(4)
    ]
    for t in threads:
        t.start()
    gate.set()
    for t in threads:
        t.join(10)

    assert len(calls) == 1
    assert len({id(r) for r in results}) == 1


def test_capabilities_default_to_the_scalar_pair():
    entry = register_sidecar("3.13", lambda sv: _Builder(sv))
    assert entry.capabilities == ["udf", "pandas_udf"]
    assert entry.supports("udf")
    assert not entry.supports("mapInPandas")


def test_re_registering_replaces_the_entry():
    first = register_sidecar("3.13", lambda sv: _Builder(sv))
    second = register_sidecar("3.13", lambda sv: _Builder(sv))
    assert get_sidecar("3.13") is second
    assert get_sidecar("3.13") is not first


def test_unregister_removes_only_that_version():
    register_sidecar("3.13", lambda sv: _Builder(sv))
    register_sidecar("3.11", lambda sv: _Builder(sv))
    unregister_sidecar("3.13")
    assert get_sidecar("3.13") is None
    assert get_sidecar("3.11") is not None
