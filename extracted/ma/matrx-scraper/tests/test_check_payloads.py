"""The evidence payloads stay declared — a guard, not a snapshot.

A passing sweep proves the past; new code is written tomorrow. These tests read
the PRODUCING SOURCE every run and fail the build the moment a check starts
emitting an evidence key that ``check_payloads`` does not declare. That is the
whole point: the shape of this data was always knowable, and the way it stops
being knowable again is one undeclared key at a time.
"""

from __future__ import annotations

import ast
import pathlib

import pytest
from matrx_scraper.check_payloads import (
    CHECK_EVIDENCE_MODELS,
    EVIDENCE_KIND_SLUGS,
    evidence_kind_for,
    evidence_model_for,
)

_PKG = pathlib.Path(__file__).resolve().parents[1] / "matrx_scraper"
_SOURCES = ("seo_audit.py", "web_crawl/analysis.py", "web_crawl/site_analysis.py")

#: Check functions whose evidence is not a per-check payload.
_NOT_A_CHECK = {
    "_gsc_unavailable",  # shared "no GSC binding" branch, folded into both gsc kinds
}


def _evidence_keys_by_function() -> dict[str, set[str]]:
    """Every ``evidence={...}`` literal in the producing code, by function."""
    found: dict[str, set[str]] = {}
    for rel in _SOURCES:
        tree = ast.parse((_PKG / rel).read_text())
        for fn in [
            n
            for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef | ast.AsyncFunctionDef)
        ]:
            for node in ast.walk(fn):
                literal = None
                if (
                    isinstance(node, ast.keyword)
                    and node.arg == "evidence"
                    and isinstance(node.value, ast.Dict)
                ):
                    literal = node.value
                elif (
                    isinstance(node, ast.Assign)
                    and len(node.targets) == 1
                    and isinstance(node.targets[0], ast.Name)
                    and node.targets[0].id == "evidence"
                    and isinstance(node.value, ast.Dict)
                ):
                    literal = node.value
                if literal is None:
                    continue
                keys = {k.value for k in literal.keys if isinstance(k, ast.Constant)}
                if keys:
                    found.setdefault(fn.name, set()).update(keys)
    return found


def _item_key(function_name: str) -> str:
    """``_site_check_hsts_policy`` / ``check_cwv_lcp`` -> the catalog item key."""
    for prefix in ("_site_check_", "_check_", "check_"):
        if function_name.startswith(prefix):
            return function_name[len(prefix) :]
    return function_name


def test_source_has_evidence_literals_to_check():
    """A silent zero here would make every other assertion vacuous."""
    assert len(_evidence_keys_by_function()) > 40


@pytest.mark.parametrize(
    ("function_name", "keys"), sorted(_evidence_keys_by_function().items())
)
def test_every_emitted_evidence_key_is_declared(function_name: str, keys: set[str]):
    if function_name in _NOT_A_CHECK:
        return
    item_key = _item_key(function_name)
    model = evidence_model_for(item_key)
    assert model is not None, (
        f"{function_name} emits evidence {sorted(keys)} but no model is registered "
        f"for check {item_key!r}. Declare one in matrx_scraper.check_payloads — an "
        f"undeclared payload is the untyped blob this module exists to end."
    )
    undeclared = sorted(keys - set(model.model_fields))
    assert not undeclared, (
        f"{function_name} emits undeclared evidence field(s) {undeclared}; add them "
        f"to {model.__name__}."
    )


def test_every_model_has_a_kind_slug():
    missing = sorted(set(CHECK_EVIDENCE_MODELS) - set(EVIDENCE_KIND_SLUGS))
    assert not missing, f"checks with a model but no kind slug: {missing}"


def test_shared_shapes_share_one_kind():
    """Checks that share a model share its slug — never a near-duplicate kind."""
    assert evidence_kind_for("broken_internal_links") == evidence_kind_for(
        "broken_external_links"
    )
    assert (
        evidence_kind_for("title_duplication")
        == evidence_kind_for("meta_description_duplication")
        == evidence_kind_for("duplicate_content_exact")
    )
    assert len(set(EVIDENCE_KIND_SLUGS.values())) < len(EVIDENCE_KIND_SLUGS)


def test_stamping_marks_the_kind_and_keeps_every_key():
    from matrx_scraper.seo_audit import CheckOutcome
    from matrx_scraper.web_crawl.analysis import _result_metadata

    outcome = CheckOutcome(
        "fail", 43, "Slow.", issue_count=1, evidence={"lcp_ms": 5285.7, "strategy": "mobile"}
    )
    evidence = _result_metadata(outcome, "cwv_lcp")["evidence"]
    assert evidence["__kind"] == "web_evidence_lcp_v1"
    assert evidence["lcp_ms"] == 5285.7


def test_an_undeclared_key_is_kept_not_dropped():
    """Loud-open: evidence we paid to compute survives a shape it outgrew."""
    from matrx_scraper.seo_audit import CheckOutcome
    from matrx_scraper.web_crawl.analysis import _result_metadata

    outcome = CheckOutcome(
        "warn", 60, "Odd.", issue_count=1, evidence={"lcp_ms": 1.0, "unforeseen": "kept"}
    )
    evidence = _result_metadata(outcome, "cwv_lcp")["evidence"]
    assert evidence["unforeseen"] == "kept"


def test_explicit_null_survives_stamping():
    """`measured, absent` must stay distinct from `this branch never set it`."""
    from matrx_scraper.seo_audit import CheckOutcome
    from matrx_scraper.web_crawl.analysis import _result_metadata

    outcome = CheckOutcome(
        "warn", 60, "No OG.", issue_count=1, evidence={"og_url": None, "missing_og_tags": []}
    )
    evidence = _result_metadata(outcome, "social_meta_completeness")["evidence"]
    assert "og_url" in evidence and evidence["og_url"] is None
    assert "twitter_card" not in evidence


def test_a_check_with_no_model_passes_evidence_through_unchanged():
    from matrx_scraper.seo_audit import CheckOutcome
    from matrx_scraper.web_crawl.analysis import _result_metadata

    outcome = CheckOutcome("warn", 60, "?", issue_count=1, evidence={"anything": 1})
    evidence = _result_metadata(outcome, "not_a_registered_check")["evidence"]
    assert evidence == {"anything": 1}
