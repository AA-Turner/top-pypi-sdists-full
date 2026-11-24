"""Pytest tier system for matrx-graph.

Three tiers; each test gets exactly one marker auto-applied based on
where it lives:

- ``level1`` — pure unit tests, no network, fast. Default for any test
  outside ``level2/`` and ``judge/``. Runs in CI on every commit.
- ``level2`` — real provider calls (LLM / scrape / external APIs).
  Asserts structural shape only (no semantic judgment). Skip-if-no-key.
  Lives in ``tests/level2/``. Runs nightly + on demand.
- ``judge`` — real workflow runs whose final output is piped to an
  ``AIJudge`` (Claude Opus / Sonnet) for strict-JSON pass/fail.
  Lives in ``tests/judge/``. Runs pre-release + nightly. A judge whose proof lives in the host
  (the news proof run) is the host's ``tests/matrx_graph_judge/``.

Run examples::

    pytest packages/matrx-graph/tests                 # everything (default)
    pytest packages/matrx-graph/tests -m level1       # cheap, fast
    pytest packages/matrx-graph/tests -m level2       # real provider calls
    pytest packages/matrx-graph/tests -m judge        # AI-judged
    pytest packages/matrx-graph/tests -m "not judge"  # skip the expensive tier
"""

from __future__ import annotations


import pytest

# Every ctx.send in this package's tests must be DECLARED (dispatcher config
# target or launches_nodes) — executor/resume_preflight.py.
from matrx_graph.executor.resume_preflight import configure_strict_launches  # noqa: E402

configure_strict_launches(lambda: True)


def pytest_configure(config: pytest.Config) -> None:
    # The proof behind interning each value once (checkpoint.values § ONE INTERNING PER VALUE): in this
    # suite every interned-value cache hit is re-hashed and every step's delivered inputs are compared
    # before and after it runs — a step that edits what it was handed fails its run.
    from matrx_graph.checkpoint import values as _values

    _values.VERIFY_INTERNED_VALUES = True
    config.addinivalue_line("markers", "level1: pure unit; no network; runs every commit")
    config.addinivalue_line(
        "markers", "level2: real provider calls; structural assertions; needs API keys"
    )
    config.addinivalue_line(
        "markers", "judge: real workflow + AIJudge verdict; pre-release / nightly only"
    )


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    for item in items:
        path = str(item.fspath)
        if "/judge/" in path:
            item.add_marker(pytest.mark.judge)
        elif "/level2/" in path:
            item.add_marker(pytest.mark.level2)
        else:
            item.add_marker(pytest.mark.level1)


@pytest.fixture(scope="module", autouse=True)
def _db_registry_restored_after_each_module():
    """The DB registry is process-global (``matrx_graph.db._registry``): a module that registers models — a live
    suite's ``configure_standalone_db``, the judge tier's ``wire_package_db``, a fixture's ``configure_db`` — and
    never takes them back leaves every later module running with them. A registered ``WfCheckpointValue`` switches
    by-reference run output on, so the run-store unit tests' fake ``WfRun`` (no ``filter``) failed only in the full
    suite (2026-10-27). Module scope, so a module's own module-scoped registration lives for all its tests."""
    from matrx_graph.db import _registry

    saved = (dict(_registry._models), dict(_registry._bases), dict(_registry._instances), dict(_registry._extras))
    configured = _registry._configured
    yield
    for bucket, before in zip(
        (_registry._models, _registry._bases, _registry._instances, _registry._extras), saved, strict=True
    ):
        bucket.clear()
        bucket.update(before)
    _registry._configured = configured


@pytest.fixture(autouse=True)
async def _settle_after_work_drained(monkeypatch: pytest.MonkeyPatch):
    """A terminal write starts its after-work as a task the caller never awaits (``run_store._settle_after``). The
    session shares one event loop, so a test that ended a run left that task to run inside the NEXT test, against the
    next test's patched ``get_model``: its marker-clear write landed in that test's capture
    (``test_a_timed_out_completion_write_ends_the_run_failed`` failed only after
    ``test_the_completion_writes_the_reason``, lane M1 2026-11-17). Drained here, before this test's patches undo
    (requesting ``monkeypatch`` orders this teardown first)."""
    yield
    from matrx_graph.db.run_store import drain_settle_after

    await drain_settle_after()


@pytest.fixture(autouse=True)
def _level1_never_reaches_the_database(request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch):
    """``level1`` is "no network" (see the module docstring), but the scheduler reads ``platform.feature_knob``
    (step clock, fan-out, checkpoint policy...) and the kind catalog on EVERY run. With the environment's real
    database registered and unreachable, each read waited out a 30 s pool-creation timeout, so unit tests that
    finish in under a second (cancel mid-step, cancel while draining) took minutes and failed their timing and
    ``asyncio.timeout`` assertions. In this tier an unreadable knob is an immediate, announced degradation (the
    engine's own documented fallback posture); a test that wants other values primes ``knobs._cache``. The kind
    catalog is NOT touched here: it resolves only through the package's DI seam, where kind tests register their
    own fake manager."""
    path = str(request.node.fspath)
    if "/judge/" in path or "/level2/" in path:
        yield
        return
    from matrx_graph import knobs

    def _no_database(*_a: object, **_k: object) -> object:
        raise ConnectionError("level1 tier: no database (reads degrade at once, never wait on a pool)")

    monkeypatch.setattr(knobs, "_feature_knob_model", _no_database)
    yield
