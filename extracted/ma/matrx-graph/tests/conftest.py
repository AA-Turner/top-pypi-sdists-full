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
  Lives in ``tests/judge/``. Runs pre-release + nightly.

Run examples::

    pytest packages/matrx-graph/tests                 # everything (default)
    pytest packages/matrx-graph/tests -m level1       # cheap, fast
    pytest packages/matrx-graph/tests -m level2       # real provider calls
    pytest packages/matrx-graph/tests -m judge        # AI-judged
    pytest packages/matrx-graph/tests -m "not judge"  # skip the expensive tier
"""

from __future__ import annotations

import os

import pytest

# Every ctx.send in this package's tests must be DECLARED (dispatcher config
# target or launches_nodes) — executor/resume_preflight.py.
os.environ.setdefault("MATRX_GRAPH_STRICT_LAUNCHES", "1")


def pytest_configure(config: pytest.Config) -> None:
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
