"""THE FUNNEL LAW — raw Anthropic SDK use lives in the provider adapter, nowhere else.

A module that constructs its own ``AsyncAnthropic`` in a production path bypasses
``execute_ai_request``: no routing, no cost capture, no request row. So the class
name may appear in exactly two places — the sanctioned adapter
(``matrx_ai/providers/anthropic/``), and the tests that PROVE the adapter works.

🚨 THE SCOPE, and why it moved (2026-09-08). This scan used to walk every ``.py``
under ``matrx_ai/`` and match the bare substring, so it went red the moment
``providers/tests/test_capture_client_sdk_flavor.py`` — the forcing-function test
for the httpx-flavor defect that killed EVERY Anthropic call at client
construction — named ``AsyncAnthropic`` in its provider census table. That test is
not a caller: it constructs SDK clients precisely to prove our capture client is
accepted, and it dials nothing. matrx-ai keeps its tests INSIDE the package (14
``tests/`` directories under ``matrx_ai/``), so a whole-package scan and a
"production callers only" rule were never the same rule; the scan now says which
one it is. Every production module is still scanned, and
``test_the_guard_still_bites`` is what keeps that claim honest — it plants a
violation in a scanned location and fails if the scan shrugs.
"""

from __future__ import annotations

from pathlib import Path

PACKAGE_ROOT = Path(__file__).parents[1] / "matrx_ai"

#: The one place raw SDK construction belongs.
SANCTIONED_ADAPTER = ("providers", "anthropic")


def _is_test_module(relative: Path) -> bool:
    """A test module — not a production path, and never a caller."""
    return (
        "tests" in relative.parts
        or relative.name.startswith("test_")
        or relative.name == "conftest.py"
    )


def _scan(root: Path) -> tuple[list[str], int]:
    """(violations, production modules actually read) — the second half matters.

    A scan that quietly stops reading files reports zero violations and reads
    identically to a clean repo. The count is returned so a caller can refuse
    a vacuous verdict.
    """
    violations: list[str] = []
    scanned = 0
    for path in sorted(root.rglob("*.py")):
        relative = path.relative_to(root)
        if relative.parts[: len(SANCTIONED_ADAPTER)] == SANCTIONED_ADAPTER:
            continue
        if _is_test_module(relative):
            continue
        scanned += 1
        if "AsyncAnthropic" in path.read_text(encoding="utf-8"):
            violations.append(str(relative))
    return violations, scanned


def test_raw_anthropic_sdk_is_confined_to_provider_adapter():
    violations, scanned = _scan(PACKAGE_ROOT)

    assert scanned > 100, (
        "the funnel scan read only "
        f"{scanned} production modules — it has stopped walking the package, so a "
        "clean verdict here would mean nothing. Fix the scan, never this bound."
    )
    assert violations == [], (
        "Raw Anthropic SDK callers bypass routing and cost capture; route them "
        f"through execute_ai_request instead: {violations}"
    )


def test_the_guard_still_bites(tmp_path: Path) -> None:
    """Falsifiability: a planted off-funnel caller MUST be caught.

    Without this, the exemptions above could widen until the guard was quiet
    about everything — the exact way a guard rots into decoration.
    """
    fake_package = tmp_path / "matrx_ai"
    (fake_package / "providers" / "anthropic").mkdir(parents=True)
    (fake_package / "providers" / "tests").mkdir(parents=True)

    # The sanctioned adapter: allowed.
    (fake_package / "providers" / "anthropic" / "client.py").write_text(
        "from anthropic import AsyncAnthropic\n", encoding="utf-8"
    )
    # A test that names the class: allowed.
    (fake_package / "providers" / "tests" / "test_flavor.py").write_text(
        'SDKS = [("anthropic", "AsyncAnthropic")]\n', encoding="utf-8"
    )
    # A production module that builds its own client: NOT allowed.
    (fake_package / "rogue.py").write_text(
        "from anthropic import AsyncAnthropic\nclient = AsyncAnthropic()\n", encoding="utf-8"
    )

    violations, scanned = _scan(fake_package)

    assert violations == ["rogue.py"], (
        "the funnel scan no longer catches a production module constructing its own "
        f"Anthropic client (saw {violations!r}) — the exemptions have eaten the rule."
    )
    assert scanned == 1
