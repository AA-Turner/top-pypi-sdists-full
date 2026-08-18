"""
Tests for the per-worker thread budget (geocif/ml/threads.py).

Without it, every pool worker's model grabs all cores: 19 workers x 131
threads measured load 940 on a 128-core node and starved co-tenant jobs.
"""

import configparser
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from geocif.ml import threads as ml_threads


def parser_with(value=None):
    p = configparser.ConfigParser()
    p.add_section("ML")
    if value is not None:
        p.set("ML", "threads_per_worker", value)
    return p


# ------------------------------------------------------------ automatic


def test_budget_divides_cores_among_workers():
    assert ml_threads.resolve_threads_per_worker(19, 128) == 6
    assert 19 * 6 <= 128


def test_budget_never_exceeds_the_machine():
    for workers in (2, 5, 16, 32, 64, 128):
        threads = ml_threads.resolve_threads_per_worker(workers, 128)
        assert workers * threads <= 128


def test_more_workers_than_cores_gets_one_thread():
    assert ml_threads.resolve_threads_per_worker(256, 128) == 1


def test_serial_run_is_not_limited():
    """One process should use the whole box."""
    assert ml_threads.resolve_threads_per_worker(1, 128) is None
    assert ml_threads.resolve_threads_per_worker(0, 128) is None


def test_nonsense_inputs_do_not_limit():
    assert ml_threads.resolve_threads_per_worker(None, 128) is None
    assert ml_threads.resolve_threads_per_worker(8, 0) is None
    assert ml_threads.resolve_threads_per_worker("many", 128) is None


# --------------------------------------------------------------- config


def test_explicit_setting_overrides_the_automatic_budget():
    assert ml_threads.resolve_threads_per_worker(19, 128, parser=parser_with("4")) == 4


def test_negative_setting_restores_unlimited_behaviour():
    assert ml_threads.resolve_threads_per_worker(19, 128, parser=parser_with("-1")) is None


def test_auto_and_zero_fall_back_to_automatic():
    for value in ("auto", "AUTO", "0", ""):
        assert ml_threads.resolve_threads_per_worker(19, 128, parser=parser_with(value)) == 6


def test_missing_option_falls_back_to_automatic():
    assert ml_threads.resolve_threads_per_worker(19, 128, parser=parser_with()) == 6


def test_unparseable_setting_falls_back_to_automatic():
    assert ml_threads.resolve_threads_per_worker(19, 128, parser=parser_with("lots")) == 6


# ------------------------------------------------------- applying limits


def test_apply_sets_every_thread_env_var(monkeypatch):
    for var in ml_threads.THREAD_ENV_VARS + (ml_threads.ENV_KEY,):
        monkeypatch.delenv(var, raising=False)

    ml_threads.apply_worker_limits(6)

    assert ml_threads.thread_count() == 6
    for var in ml_threads.THREAD_ENV_VARS:
        assert ml_threads.os.environ[var] == "6"


def test_apply_with_no_budget_is_a_noop(monkeypatch):
    monkeypatch.delenv(ml_threads.ENV_KEY, raising=False)
    ml_threads.apply_worker_limits(None)
    assert ml_threads.thread_count("unset") == "unset"


def test_apply_survives_missing_threadpoolctl(monkeypatch):
    """A missing optional dep must not kill the worker."""
    import builtins

    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "threadpoolctl":
            raise ImportError("simulated missing threadpoolctl")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    ml_threads.apply_worker_limits(3)
    assert ml_threads.thread_count() == 3


# --------------------------------------------------- reading it back


def test_thread_count_returns_default_when_unset(monkeypatch):
    monkeypatch.delenv(ml_threads.ENV_KEY, raising=False)
    assert ml_threads.thread_count(-1) == -1
    assert ml_threads.thread_count() is None


def test_thread_count_reads_the_budget(monkeypatch):
    monkeypatch.setenv(ml_threads.ENV_KEY, "8")
    assert ml_threads.thread_count(-1) == 8


def test_thread_count_ignores_junk_and_zero(monkeypatch):
    """-1 is CatBoost/joblib's own 'all cores' sentinel, so it is the default."""
    monkeypatch.setenv(ml_threads.ENV_KEY, "not-a-number")
    assert ml_threads.thread_count(-1) == -1
    monkeypatch.setenv(ml_threads.ENV_KEY, "0")
    assert ml_threads.thread_count(-1) == -1


def test_catboost_receives_the_budget(monkeypatch):
    """The value handed to CatBoost's thread_count must be the budget."""
    monkeypatch.setenv(ml_threads.ENV_KEY, "6")
    params = {"n_estimators": 500}
    params.setdefault("thread_count", ml_threads.thread_count(-1))
    assert params["thread_count"] == 6
