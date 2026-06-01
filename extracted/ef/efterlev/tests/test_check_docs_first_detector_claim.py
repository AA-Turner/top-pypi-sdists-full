"""Tests for `scripts/check-docs.py::check_first_detector_claims`.

Locks the bug-class catch added 2026-05-10 (PR follow-up to PR #211).
The check function flags doc prose that pairs a "first-detector"
claim with a KSI-XXX-YYY identifier when that KSI is actually
evidenced by more than one detector. The bug it would have caught
(if shipped earlier) was PR #205 / PR #207 / v0.1.45 CHANGELOG
all claiming `aws.api_gateway_auth_required` was the library's
first detector for KSI-CNA-EIS / KSI-CNA-DFP — both KSIs were
already covered.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_check_docs():
    """Import `scripts/check-docs.py` as a module (its name has a hyphen
    so a normal `import` won't work). Mirrors the pattern in
    `test_e2e_smoke_retry.py` — register in sys.modules BEFORE
    `exec_module` so dataclass / typing introspection works.
    """
    path = REPO_ROOT / "scripts" / "check-docs.py"
    spec = importlib.util.spec_from_file_location("check_docs", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["check_docs"] = module
    spec.loader.exec_module(module)
    return module


def _write_md(tmp_path: Path, name: str, body: str) -> Path:
    p = tmp_path / name
    p.write_text(body, encoding="utf-8")
    return p


@pytest.fixture
def cd(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """Load check-docs and patch REPO_ROOT so `relative_to` calls inside
    the check function work against the test's tmp_path.

    The check formats findings with `path.relative_to(REPO_ROOT)` —
    if REPO_ROOT is the live repo and the doc is under tmp_path,
    `.relative_to()` raises ValueError. Patching REPO_ROOT to tmp_path
    makes synthetic test docs work like real ones.
    """
    module = _load_check_docs()
    monkeypatch.setattr(module, "REPO_ROOT", tmp_path)
    return module


def test_wrong_claim_with_multi_detector_ksi_emits_finding(cd, tmp_path: Path) -> None:
    """The canonical bug shape: prose says 'first detector evidencing
    KSI-X' but KSI-X is actually evidenced by 2 detectors. Surface
    the drift."""
    doc = _write_md(
        tmp_path,
        "wrong.md",
        "**Library's first detector** evidencing KSI-CNA-EIS — "
        "this KSI was previously uncovered.\n",
    )
    findings = cd.check_first_detector_claims(doc, {"KSI-CNA-EIS": 2})
    assert len(findings) == 1
    assert "KSI-CNA-EIS" in findings[0]
    assert "evidenced by 2 detectors" in findings[0]


def test_correct_claim_with_singleton_ksi_emits_no_finding(cd, tmp_path: Path) -> None:
    """If the cited KSI is in fact evidenced by exactly one detector,
    the 'first-detector' claim is accurate and emits no finding."""
    doc = _write_md(
        tmp_path,
        "correct.md",
        "**First detector** evidencing KSI-NEW-ONE — landing in this PR.\n",
    )
    findings = cd.check_first_detector_claims(doc, {"KSI-NEW-ONE": 1})
    assert findings == []


def test_resource_type_side_claim_with_no_ksi_emits_no_finding(cd, tmp_path: Path) -> None:
    """Claims like `library's first aws_lambda_function-side detector`
    are about resource-type coverage, not KSI coverage. The regex
    matches the 'first detector' phrase but no KSI in proximity →
    no finding. This protects accurate slice-claims like the one in
    aws.lambda_logging_configured's README."""
    doc = _write_md(
        tmp_path,
        "slice.md",
        "Library's first `aws_lambda_function`-side detector. "
        "Reads function resources and emits per-resource evidence.\n",
    )
    # Even with a heavily-populated KSI map, no KSI is cited in the
    # match window so no finding fires.
    findings = cd.check_first_detector_claims(doc, {"KSI-MLA-LET": 5, "KSI-CNA-MAT": 7})
    assert findings == []


def test_multiple_ksis_only_wrong_ones_flagged(cd, tmp_path: Path) -> None:
    """A 'first-detector' claim citing multiple KSIs: only the ones
    with count > 1 should flag. The detector might be first for some
    KSIs but not others; surface only the wrong assertions."""
    doc = _write_md(
        tmp_path,
        "mixed.md",
        "**Library's first detector** evidencing both KSI-CNA-EIS and "
        "KSI-FOO-NEW — covers two new dimensions.\n",
    )
    findings = cd.check_first_detector_claims(doc, {"KSI-CNA-EIS": 2, "KSI-FOO-NEW": 1})
    assert len(findings) == 1
    assert "KSI-CNA-EIS" in findings[0]
    assert "KSI-FOO-NEW" not in findings[0]


def test_decisions_md_is_excluded_from_check(cd, tmp_path: Path) -> None:
    """DECISIONS.md is append-only — wrong claims are corrected via
    adjacent correction entries, not edited retroactively. The check
    must not flag preserved-wrong text in DECISIONS.md (would fight
    the append-only contract). The `cd` fixture already patches
    REPO_ROOT to tmp_path, so a file at `tmp_path / DECISIONS.md`
    resolves to relative `DECISIONS.md` for the exclusion check."""
    decisions_doc = tmp_path / "DECISIONS.md"
    decisions_doc.write_text(
        "Library's first detector evidencing KSI-CNA-EIS.\n",
        encoding="utf-8",
    )
    findings = cd.check_first_detector_claims(decisions_doc, {"KSI-CNA-EIS": 2})
    assert findings == []


def test_unrelated_first_word_does_not_match(cd, tmp_path: Path) -> None:
    """Defense-in-depth: prose that contains 'first' near a KSI but
    not as 'first detector' should not trip. Common case: 'good first
    issue', 'first DECISIONS entry'."""
    doc = _write_md(
        tmp_path,
        "unrelated.md",
        "Pick an issue labeled 'good first issue' to start. "
        "See KSI-CNA-EIS for the relevant KSI mapping.\n",
    )
    findings = cd.check_first_detector_claims(doc, {"KSI-CNA-EIS": 5})
    assert findings == []


def test_runtime_ksi_detector_counts_finds_known_multi_detector_ksis() -> None:
    """Smoke test that the runtime KSI counter walks the live
    detector library and returns sensible counts. Locks against
    a future refactor that breaks the mapping.yaml walk. Uses the
    real REPO_ROOT (no fixture patching)."""
    module = _load_check_docs()
    counts = module.runtime_ksi_detector_counts()
    # KSI-MLA-LET is evidenced by at least 4 detectors as of v0.1.45
    # (CloudTrail, CloudWatch alarms, CloudTrail log-file validation,
    # Lambda log groups, APIGW stage access logs). If this drops below
    # 2 something has gone very wrong.
    assert counts.get("KSI-MLA-LET", 0) >= 2
    # KSI-CNA-EIS is evidenced by access_analyzer_enabled +
    # api_gateway_auth_required as of v0.1.45.
    assert counts.get("KSI-CNA-EIS", 0) >= 2
