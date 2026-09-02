"""Agent-input bridge fixture drift gate — the TS twin cannot go stale silently.

matrx-frontend's `variable-kind-bridge-parity.test.ts` asserts that its
converters reproduce what THIS repo's bridge produced
(`variable-kind-bridge.generated.json`). That is the right way to pin a twin,
but a COMMITTED snapshot moves the drift channel rather than closing it: change
`matrx_ai.agents.variable_kinds` and the TS suite keeps passing against
yesterday's contract, green and wrong.

This is the second, independent layer: it regenerates from the live bridge and
fails the moment a committed copy stops describing what the bridge does.

    uv run pytest packages/matrx-ai/tests/parity
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


def _load_generator():
    """Import the generator by path — `scripts/` is not an importable package."""
    root = Path(__file__).resolve().parents[4]
    script = root / "scripts" / "generate_variable_kind_fixture.py"
    if not script.is_file():
        pytest.fail(
            f"the agent-input bridge fixture generator is MISSING at {script} — "
            "the TS twin has no way to be regenerated or checked"
        )
    spec = importlib.util.spec_from_file_location("_variable_kind_fixture", script)
    module = importlib.util.module_from_spec(spec)
    sys.modules["_variable_kind_fixture"] = module
    spec.loader.exec_module(module)
    return module


def test_the_committed_fixtures_match_the_live_bridge():
    generator = _load_generator()

    # The canonical fixture lives in this repo — a missing sibling checkout can
    # shrink the comparison set but never make this gate vacuous.
    assert generator.FIXTURE_PATH.exists(), (
        f"the canonical agent-input bridge fixture is MISSING at {generator.FIXTURE_PATH}"
    )

    differences = generator.verify()
    if differences:
        listed = "\n  - ".join(differences)
        pytest.fail(
            "A committed agent-input bridge fixture is STALE: it asserts against "
            "a conversion this bridge no longer produces, so the TS parity suite "
            "is green against yesterday's contract.\n\n"
            f"  - {listed}\n\n"
            "Re-run: uv run python scripts/generate_variable_kind_fixture.py — "
            "then re-run the TS suite "
            "(features/content-ir/__tests__/variable-kind-bridge-parity.test.ts)."
        )


def test_the_case_set_still_covers_every_construct():
    """A case set that quietly shrinks is a gate that quietly stops gating."""
    generator = _load_generator()
    names = {case["name"] for case in generator.CASES}
    required = {
        "bare_variable",
        "open_enum",  # enum.open — the A2 construct
        "items_enum_checkbox",  # string[].values
        "numeric_bounds",  # min/max/step
        "help_and_default",  # description + default
        "picklist_static_single",  # out-of-band binding, options kept
        "picklist_runtime_options",  # out-of-band binding, recorded loss
        "scope_binding",  # out-of-band scope binding
        "unknown_component_type",  # must never throw
    }
    missing = required - names
    assert not missing, (
        f"the agent-input bridge fixture no longer covers: {sorted(missing)}. "
        "Every construct A2 made expressible has to stay in the case set."
    )
