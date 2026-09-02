"""Partial-kinds fixture drift gate — the TS twin cannot go stale silently.

`@ai-matrx/content-ir`'s `partial-kind.test.ts` (apps/shared/content-ir-core,
in THIS repo since 0.2.0) and matrx-frontend's route test assert against events
this repo's producer really emitted (`partial-kind-events.generated.json`),
which is the right way to pin a twin — but a COMMITTED snapshot moves the drift
channel rather than closing it: change the producer's shape and the TS suites
keep passing against yesterday's events, green and wrong.

This is the second, independent layer. It regenerates from the live producer and
fails the moment the committed fixture stops describing what the server sends.

Lives beside the detection-parity gate because it is the same discipline applied
to the same seam:

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
    script = root / "scripts" / "generate_partial_kind_fixture.py"
    if not script.is_file():
        pytest.fail(
            f"the partial-kind fixture generator is MISSING at {script} — the "
            "TS twin has no way to be regenerated or checked"
        )
    spec = importlib.util.spec_from_file_location("_partial_kind_fixture", script)
    module = importlib.util.module_from_spec(spec)
    sys.modules["_partial_kind_fixture"] = module
    spec.loader.exec_module(module)
    return module


def test_the_committed_fixtures_match_the_live_producer():
    generator = _load_generator()

    # The canonical fixture lives in this repo — no sibling checkout can make
    # this gate skip any more. A missing file is a FAILURE, not a skip.
    assert generator.FIXTURE_PATH.exists(), (
        f"the canonical partial-kind fixture is MISSING at {generator.FIXTURE_PATH}"
    )

    differences = generator.verify()
    if differences:
        listed = "\n  - ".join(differences)
        pytest.fail(
            "A committed partial-kind fixture is STALE: it asserts against "
            "events this producer no longer sends, so a TS suite is "
            "green against yesterday's contract.\n\n"
            f"  - {listed}\n\n"
            "Fix: uv run python scripts/generate_partial_kind_fixture.py\n"
            "Then re-run apps/shared/content-ir-core: pnpm test, and "
            "matrx-frontend: pnpm test features/content-ir\n"
            "If the event SHAPE changed, reconcile the wire contract too: "
            "common-docs/systems/content-ir-system/STREAMING_PARTIAL_KINDS.md"
        )


def test_the_gate_would_actually_catch_drift():
    """Forcing function: prove the comparison is not vacuous.

    A gate nobody has watched fail is a gate nobody should trust. This mutates
    one event in the committed fixture and asserts `verify()` reports it, then
    restores the file byte-for-byte.
    """
    generator = _load_generator()
    assert generator.FIXTURE_PATH.exists()

    original = generator.FIXTURE_PATH.read_text()
    assert generator.verify() == [], "fixture is already stale — run the generator"

    import json

    payload = json.loads(original)
    rows = payload["fixtures"]["clean_finish"]
    assert rows, "the clean_finish fixture is empty — this test proves nothing"
    rows[0]["event"]["seq"] = 999_999

    try:
        generator.FIXTURE_PATH.write_text(json.dumps(payload, indent=2) + "\n")
        differences = generator.verify()
        assert differences, "the gate passed on a fixture that no longer matches the producer"
        assert "clean_finish" in differences[0]
    finally:
        generator.FIXTURE_PATH.write_text(original)

    assert generator.FIXTURE_PATH.read_text() == original
    assert generator.verify() == []


def test_a_missing_frontend_checkout_FAILS_in_ci(tmp_path, monkeypatch):
    """The gate must never report a pass on a copy it did not look at.

    This generator used to drop the frontend copy whenever the sibling checkout
    was absent, silently. In an aidream-only CI job that made "parity is gated
    on BOTH copies" false exactly where the claim carries weight — matrx-frontend's
    `partial-kind-route.test.ts` could sit green against yesterday's events for
    as long as nobody happened to run this locally with the checkout present.

    Same posture as the rest of this harness: unverifiable never reads as passing.
    """
    generator = _load_generator()
    monkeypatch.setattr(generator, "FRONTEND_ROOT", tmp_path / "no-such-checkout")

    with pytest.raises(generator.FrontendCheckoutMissing) as excinfo:
        generator.fixture_paths(strict=True)

    message = str(excinfo.value)
    # The message has to name the missing path and say what to do — a failure
    # nobody can act on gets disabled, which is worse than not having it.
    assert "no-such-checkout" in message
    assert "MATRX_FRONTEND_ROOT" in message


def test_a_missing_frontend_checkout_only_WARNS_locally(tmp_path, monkeypatch, capsys):
    """A developer with no frontend checkout is a normal state, not a broken
    build — but the skip is marked, loudly, on stderr. Silence is the defect."""
    generator = _load_generator()
    monkeypatch.setattr(generator, "FRONTEND_ROOT", tmp_path / "no-such-checkout")

    paths = generator.fixture_paths(strict=False)

    assert paths == [generator.FIXTURE_PATH]
    warning = capsys.readouterr().err
    assert "PARTIAL PARITY" in warning
    assert "In CI this is a FAILURE" in warning


def test_ci_detection_reads_the_runner_env(monkeypatch):
    """`CI` is set by GitHub Actions and effectively every other runner;
    `GITHUB_ACTIONS` is checked too so a workflow that unsets CI still gets the
    strict posture rather than quietly downgrading to the local one."""
    generator = _load_generator()

    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    assert generator.in_ci() is False

    monkeypatch.setenv("CI", "true")
    assert generator.in_ci() is True

    monkeypatch.delenv("CI")
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    assert generator.in_ci() is True


def test_both_copies_are_checked_when_the_checkout_is_present(monkeypatch):
    """The positive case: with the sibling present BOTH paths are returned, in
    CI and out of it. Without this, the two tests above would still pass if
    someone made the frontend copy unreachable in every posture."""
    generator = _load_generator()
    if not generator.FRONTEND_ROOT.is_dir():
        pytest.skip("matrx-frontend is not checked out beside this repo")

    for strict in (True, False):
        paths = generator.fixture_paths(strict=strict)
        assert paths == [generator.FIXTURE_PATH, generator.FRONTEND_FIXTURE_PATH]
