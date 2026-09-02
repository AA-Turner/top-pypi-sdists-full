"""Top-level conftest for matrx-ai tests.

Runs ``_configure_stubs()`` at conftest *import* time so that test
modules anywhere under ``packages/matrx-ai/`` can freely import
``matrx_ai.providers``, ``matrx_ai.config``, ``matrx_ai.tools``, etc.
without tripping ``DBNotConfiguredError`` during collection.

This file lives OUTSIDE the ``matrx_ai`` package itself, so importing it
does not transitively import any matrx-ai submodule that would require
DB stubs to be configured first. By the time pytest descends into the
package and starts importing test modules, the registry is already
populated with safe stand-ins.

Idempotent — calling ``_configure_stubs()`` multiple times just merges
into the global registries again. Coexists cleanly with the per-suite
conftest at ``matrx_ai/testing/tests/conftest.py``.
"""

from __future__ import annotations

import pytest

from matrx_ai.testing.host_isolation import capture_baseline, restore_baseline
from matrx_ai.testing.tests.conftest import _configure_stubs

_configure_stubs()

# The pristine, host-free package configuration — captured immediately after the
# stubs are installed and BEFORE any test module is imported (pytest loads the
# conftest of every initial argument at session start, ahead of collection).
#
# Read matrx_ai/testing/host_isolation.py for the why. Short version: an aidream
# test collected before these ones fires the host bootstrap
# (`configure_packages()` -> `matrx_ai.configure(...)`) as an import-time side
# effect, and that rewrites matrx-ai's process globals — the `_ext` seam
# registry, the durable VFS backend, the mandate resolver. matrx-ai's own tests
# assert on the PACKAGE's behaviour, so they must not read the host's wiring.
_PRISTINE_HOST_SEAMS = capture_baseline()


@pytest.fixture(autouse=True)
def _pristine_matrx_ai_host_seams():
    """Run every matrx-ai test against the package's own configuration.

    Restored on BOTH sides: before, so a host bootstrap that already fired
    (another suite in the same process) cannot decide what this test sees;
    after, so a matrx-ai test that installs a seam cannot leak into the next
    test either. Ordering-independent by construction.
    """
    restore_baseline(_PRISTINE_HOST_SEAMS)
    try:
        yield
    finally:
        restore_baseline(_PRISTINE_HOST_SEAMS)


# Manual dev/demo scripts that live in the tests tree but are NOT automated
# unit tests: they make live provider API calls, take non-fixture positional
# args on their ``test_*`` functions, and/or run code at module import. pytest
# would either error at setup ("fixture not found") or abort collection. They
# are meant to be run by hand (``python <file>``), so exclude them from the
# automated suite rather than mangle them into fixtures.
collect_ignore = [
    "matrx_ai/tests/openai/openai_translation_test.py",
    "matrx_ai/tests/openai/conversation_id_test.py",
    "matrx_ai/tests/test_translations.py",
    # Manual smoke/integration scripts (run by hand: `python <file>`), NOT unit
    # tests. They either import `initialize_testing` at MODULE level — which fires
    # the whole aidream host bootstrap (`matrx_ai.configure(...)` + tool-registry
    # population) as a process-global side effect that pollutes singletons (vfs
    # _DURABLE_INSTALLED, the capability registry, ToolRegistry) for every test
    # collected afterward — or take positional args on `test_*` functions that
    # pytest mistakes for missing fixtures, or need a live AppContext/DB/LLM.
    # Collecting them is what made the suite's failure set nondeterministic.
    # (test_huggingface.py was MOVED to root scripts/hf_provider_smoke.py — it
    #  imported aidream-root `initialize_testing`, a package-boundary violation;
    #  a manual smoke script belongs outside the package.)
    "matrx_ai/agents/tests/test_categorization.py",
    "matrx_ai/agents/tests/new_agent_test.py",
]
