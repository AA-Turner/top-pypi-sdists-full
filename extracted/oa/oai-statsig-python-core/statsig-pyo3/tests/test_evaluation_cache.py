import json
import os
import signal
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import pytest
from statsig_python_core import EvaluationCache
from statsig_python_core import evaluation_cache as evaluation_cache_module
from statsig_python_core.evaluation_cache import (
    _VALUE_CACHE_HIT_FIELD,
    _VALUE_CACHE_KEY_FIELD,
)


def _cache_result(cache: EvaluationCache, key: int, value: dict) -> dict:
    raw = {"value": value, "details": {"reason": "test"}}
    raw[_VALUE_CACHE_KEY_FIELD] = key
    raw[_VALUE_CACHE_HIT_FIELD] = False
    cache._consume_result(raw)
    return raw


def _record_hit(cache: EvaluationCache, key: int) -> dict:
    raw = {"details": {"reason": "fresh"}}
    raw[_VALUE_CACHE_KEY_FIELD] = key
    raw[_VALUE_CACHE_HIT_FIELD] = True
    cache._consume_result(raw)
    return raw


def test_cache_freezes_and_reuses_dynamic_returnable_values():
    cache = EvaluationCache()
    raw = _cache_result(
        cache,
        7,
        {
            "nested": {"value": "cached"},
            "items": [1, {"value": "cached"}],
        },
    )

    cached = cache._values_for_call()[7]
    assert raw["value"] is cached
    assert json.loads(json.dumps(raw["value"])) == raw["value"]

    with pytest.raises(TypeError, match="immutable"):
        raw["value"]["nested"]["value"] = "changed"
    with pytest.raises(TypeError, match="immutable"):
        raw["value"]["items"].append(2)
    with pytest.raises(TypeError, match="immutable"):
        raw["value"]["items"][1]["value"] = "changed"

    hit = _record_hit(cache, 7)
    assert hit["value"] is raw["value"]
    assert hit["details"] is not raw["details"]
    assert hit["details"] == {"reason": "fresh"}
    assert _VALUE_CACHE_KEY_FIELD not in hit
    assert _VALUE_CACHE_HIT_FIELD not in hit
    assert cache.misses == 1
    assert cache.hits == 1


def test_cache_can_admit_a_pending_bulk_value_marked_as_a_hit():
    cache = EvaluationCache()
    raw = {
        "value": {"shared": True},
        _VALUE_CACHE_KEY_FIELD: 7,
        _VALUE_CACHE_HIT_FIELD: True,
    }

    cache._consume_result(raw)

    assert raw["value"] is cache._values_for_call()[7]
    assert cache.misses == 1
    assert cache.hits == 0


def test_call_keys_retain_a_hit_across_concurrent_eviction():
    cache = EvaluationCache(max_entries=1)
    first = _cache_result(cache, 7, {"shared": True})
    call_keys = cache._keys_for_call()

    assert 7 in call_keys
    _cache_result(cache, 8, {"replacement": True})
    assert 7 not in cache._values_for_call()

    hit = {
        _VALUE_CACHE_KEY_FIELD: 7,
        _VALUE_CACHE_HIT_FIELD: True,
        "details": {"reason": "fresh"},
    }
    cache._consume_result(hit, call_keys)

    assert hit["value"] is first["value"]
    assert hit["details"] == {"reason": "fresh"}
    assert cache.hits == 1
    assert cache.entry_count == 1


def test_cache_ignores_results_without_a_valid_protocol_key():
    cache = EvaluationCache()

    raw = {"value": {"mutable": True}}
    cache._consume_result(raw)
    cache._consume_result({_VALUE_CACHE_KEY_FIELD: True})

    assert cache.entry_count == 0
    assert cache.hits == 0
    assert cache.misses == 0
    raw["value"]["still_mutable"] = True


def test_cache_clear_releases_retained_entries():
    cache = EvaluationCache()
    _cache_result(cache, 1, {"value": 1})

    assert cache.entry_count == 1
    assert cache.estimated_size_bytes > 0

    cache.clear()

    assert cache.entry_count == 0
    assert cache.estimated_size_bytes == 0
    assert cache._values_for_call() == {}


def test_cache_enforces_lru_entry_budget():
    cache = EvaluationCache(max_entries=2)
    _cache_result(cache, 1, {"text": "a"})
    _cache_result(cache, 2, {"text": "b"})

    _record_hit(cache, 1)
    _cache_result(cache, 3, {"text": "c"})

    retained = cache._values_for_call()
    assert set(retained) == {1, 3}
    assert cache.entry_count == 2
    assert cache.evictions == 1


def test_cache_enforces_entry_and_byte_budgets():
    cache = EvaluationCache(
        max_bytes=4096,
        max_entries=2,
        max_entry_bytes=2048,
    )

    _cache_result(cache, 1, {"text": "a" * 400})
    _cache_result(cache, 2, {"text": "b" * 400})
    _cache_result(cache, 3, {"text": "c" * 400})

    assert cache.entry_count <= 2
    assert cache.estimated_size_bytes <= cache.max_bytes
    assert cache.evictions >= 1
    assert 1 not in cache._values_for_call()


def test_cache_remains_bounded_under_sustained_unique_results():
    cache = EvaluationCache(
        max_bytes=64 * 1024,
        max_entries=32,
        max_entry_bytes=4096,
    )

    for key in range(5000):
        _cache_result(cache, key, {"key": key, "text": "x" * 128})

    assert cache.entry_count <= cache.max_entries
    assert cache.estimated_size_bytes <= cache.max_bytes
    assert cache.evictions > 0


def test_cache_serializes_concurrent_state_updates(monkeypatch):
    real_monotonic = time.monotonic

    def yielding_monotonic():
        time.sleep(0)
        return real_monotonic()

    monkeypatch.setattr(evaluation_cache_module, "monotonic", yielding_monotonic)
    cache = EvaluationCache(
        max_bytes=4096,
        max_entries=1,
        max_entry_bytes=2048,
    )
    worker_count = 8
    entries_per_worker = 100

    def populate(worker: int) -> None:
        for index in range(entries_per_worker):
            key = worker * entries_per_worker + index
            _cache_result(cache, key, {"key": key})

    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = [executor.submit(populate, worker) for worker in range(worker_count)]
        for future in futures:
            future.result()

    expected_misses = worker_count * entries_per_worker
    assert cache.misses == expected_misses
    assert cache.entry_count == 1
    assert cache.evictions == expected_misses - 1
    assert cache.estimated_size_bytes <= cache.max_bytes


@pytest.mark.skipif(not hasattr(os, "fork"), reason="requires os.fork")
@pytest.mark.filterwarnings(
    "ignore:This process .* is multi-threaded.*:DeprecationWarning"
)
def test_cache_lock_is_reinitialized_after_fork():
    cache = EvaluationCache()
    lock_held = threading.Event()
    release_lock = threading.Event()

    def hold_cache_lock() -> None:
        with cache._lock:
            lock_held.set()
            release_lock.wait()

    holder = threading.Thread(target=hold_cache_lock)
    holder.start()
    lock_held.wait()
    release_timer = threading.Timer(0.05, release_lock.set)
    release_timer.start()

    child_pid = os.fork()
    if child_pid == 0:
        signal.alarm(2)
        cache.clear()
        os._exit(0)

    _, child_status = os.waitpid(child_pid, 0)
    holder.join()
    release_timer.join()

    assert os.waitstatus_to_exitcode(child_status) == 0


def test_cache_evicts_by_byte_budget_before_entry_limit():
    cache = EvaluationCache(
        max_bytes=2500,
        max_entries=100,
        max_entry_bytes=2000,
    )

    _cache_result(cache, 1, {"text": "a" * 700})
    _cache_result(cache, 2, {"text": "b" * 700})

    assert cache.entry_count == 1
    assert cache.estimated_size_bytes <= cache.max_bytes
    assert cache.evictions == 1


def test_cache_bypasses_oversized_entries_without_retaining_them():
    cache = EvaluationCache(
        max_bytes=2048,
        max_entries=10,
        max_entry_bytes=512,
    )

    raw = _cache_result(cache, 1, {"text": "x" * 4096})

    assert cache.entry_count == 0
    assert cache.estimated_size_bytes == 0
    assert cache.oversized_bypasses == 1
    assert isinstance(raw["value"], dict)
    raw["value"]["still_mutable"] = True


def test_cache_detaches_pending_bulk_values_when_oversized():
    cache = EvaluationCache(
        max_bytes=2048,
        max_entries=10,
        max_entry_bytes=512,
    )
    shared = {
        "nested": {"value": "x" * 4096},
        "items": [{"value": "shared"}],
    }
    first = {
        "value": shared,
        _VALUE_CACHE_KEY_FIELD: 1,
        _VALUE_CACHE_HIT_FIELD: False,
    }
    pending = {
        "value": shared,
        _VALUE_CACHE_KEY_FIELD: 1,
        _VALUE_CACHE_HIT_FIELD: True,
    }

    cache._consume_result(first)
    cache._consume_result(pending)

    assert cache.entry_count == 0
    assert cache.oversized_bypasses == 2
    assert first["value"] is shared
    assert pending["value"] is not first["value"]
    assert pending["value"]["nested"] is not first["value"]["nested"]
    assert pending["value"]["items"] is not first["value"]["items"]

    first["value"]["nested"]["value"] = "mutated"
    first["value"]["items"][0]["value"] = "mutated"
    assert pending["value"]["nested"]["value"] == "x" * 4096
    assert pending["value"]["items"][0]["value"] == "shared"


def test_cache_bypasses_values_that_cannot_be_safely_measured(monkeypatch):
    def raise_memory_error(_value, _limit):
        raise MemoryError

    monkeypatch.setattr(
        evaluation_cache_module,
        "_estimated_deep_size",
        raise_memory_error,
    )
    cache = EvaluationCache()

    raw = _cache_result(cache, 1, {"value": 1})

    assert cache.entry_count == 0
    assert cache.estimated_size_bytes == 0
    assert cache.oversized_bypasses == 1
    raw["value"]["still_mutable"] = True


def test_cache_expires_dormant_entries_on_any_later_call(monkeypatch):
    now = [100.0]
    monkeypatch.setattr(evaluation_cache_module, "monotonic", lambda: now[0])
    cache = EvaluationCache(ttl_seconds=5)

    _cache_result(cache, 1, {"value": 1})
    assert cache.entry_count == 1

    now[0] += 6
    assert cache._values_for_call() == {}
    assert cache.entry_count == 0
    assert cache.evictions == 1


@pytest.mark.parametrize(
    "kwargs",
    [
        {"max_bytes": 0},
        {"max_bytes": True},
        {"max_entries": 0},
        {"max_entry_bytes": 0},
        {"ttl_seconds": 0},
        {"ttl_seconds": float("inf")},
        {"max_bytes": 1024, "max_entry_bytes": 2048},
    ],
)
def test_cache_rejects_unbounded_or_invalid_limits(kwargs):
    with pytest.raises(ValueError):
        EvaluationCache(**kwargs)
