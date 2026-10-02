"""T1 parity: our validate_artifacts and newsjack's grade.py agree check for check.

Break this catches: any drift between our ported check logic and theirs — a
check we dropped, renamed, loosened or tightened. Their grader runs from a
vendored copy (tests/fixtures/ai_visibility_panel/grader, MIT, commit 092d882)
on the same files our function reads, and on mutated copies where one field is
broken; both must fail the SAME check ID, and it must have passed before.
"""

from __future__ import annotations

import copy
import importlib
import json
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
import yaml

from matrx_seo.ai_visibility_design import REQUIRED_ARTIFACTS, checks_passed, validate_artifacts

FIXTURES = Path(__file__).parent / "fixtures" / "ai_visibility_panel"
RUNS = ["2026-07-25-opus5-heldout-airalo", "2026-07-25-opus5-retest-zocdoc"]


@pytest.fixture(scope="module")
def grade() -> Any:
    sys.path.insert(0, str(FIXTURES / "grader"))
    try:
        return importlib.import_module("grade")
    finally:
        sys.path.remove(str(FIXTURES / "grader"))


def _case_dir(run_dir: Path) -> Path:
    return next(p for p in (run_dir / "cases").iterdir() if p.is_dir())


def _load(case_dir: Path) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for name in REQUIRED_ARTIFACTS:
        text = (case_dir / name).read_text(encoding="utf-8")
        if name.endswith(".json"):
            out[name] = json.loads(text)
        elif name.endswith(".yaml"):
            out[name] = yaml.safe_load(text)
        else:
            out[name] = text
    return out


def _write(case_dir: Path, artifacts: dict[str, Any]) -> None:
    case_dir.mkdir(parents=True, exist_ok=True)
    for name, value in artifacts.items():
        if name.endswith(".md"):
            (case_dir / name).write_text(value, encoding="utf-8")
        else:  # JSON is valid YAML 1.2, so .yaml files are written as JSON too.
            (case_dir / name).write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


def _theirs(grade: Any, run_dir: Path) -> dict[str, bool]:
    case_dir = _case_dir(run_dir)
    result = grade.grade_case({"id": case_dir.name}, {}, run_dir, False)
    return {c["id"]: c["passed"] for c in result["checks"]}


def _ours(artifacts: dict[str, Any]) -> dict[str, bool]:
    return {c.id: c.passed for c in validate_artifacts(artifacts) if not c.id.startswith("schema:")}


@pytest.mark.parametrize("run", RUNS)
def test_every_grader_check_has_the_same_verdict_on_their_passing_runs(
    grade: Any, run: str
) -> None:
    theirs = _theirs(grade, FIXTURES / run)
    ours = _ours(_load(_case_dir(FIXTURES / run)))
    assert len(theirs) == 108  # their committed grading.json recorded 108 checks per case
    assert ours == theirs


# --- mutations: one broken field → both graders fail the same ID --------------


def _first_unaided_core(artifacts: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    accepted = set(artifacts["prompt_qa.json"]["accepted_candidate_ids"])
    for cell in artifacts["prompt_universe.json"]["canonical_cells"]:
        if cell["aided_status"] == "unaided" and cell["partition"] == "core":
            for cand in cell["candidates"]:
                if cand["candidate_id"] in accepted:
                    return cell, cand
    raise AssertionError("fixture has no accepted unaided core candidate")


def _break_job_reference(a: dict[str, Any]) -> None:
    a["prompt_architecture.json"]["cells"][0]["job_id"] = "job-nonexistent-intake"


def _leak_brand_into_unaided(a: dict[str, Any]) -> None:
    _, cand = _first_unaided_core(a)
    brand = a["contamination_register.yaml"]["target_terms"]["brands"][0]
    cand["text"] = f"{cand['text']} is {brand} any good"


def _drop_qa_decision(a: dict[str, Any]) -> None:
    a["prompt_qa.json"]["decisions"].pop()


def _miscount_qa(a: dict[str, Any]) -> None:
    a["prompt_qa.json"]["counts"]["pass"] += 1


def _unseparate_weights(a: dict[str, Any]) -> None:
    del a["panel.yaml"]["weight"]["priority"]


def _select_unapproved(a: dict[str, Any]) -> None:
    a["panel.yaml"]["selected_candidate_ids"].append("prompt-never-reviewed")


def _freeze_with_pending_gate(a: dict[str, Any]) -> None:
    a["panel.yaml"]["status"] = "frozen"
    a["panel.yaml"]["approvals"] = [{"gate": "gate_4", "status": "pending"}]


def _drop_prompt_text_from_report(a: dict[str, Any]) -> None:
    _, cand = _first_unaided_core(a)
    report = a["panel_report.md"]
    a["panel_report.md"] = report.replace(cand["text"], "").replace(
        cand["text"].replace("|", r"\|"), ""
    )


def _bad_enum(a: dict[str, Any]) -> None:
    _, cand = _first_unaided_core(a)
    cand["transformation"] = "paraphrased_by_model"


def _brand_in_blind_brief(a: dict[str, Any]) -> None:
    brand = a["contamination_register.yaml"]["target_terms"]["brands"][0]
    a["blind_design_brief.json"]["warnings"].append(f"sanitized mention of {brand}")


def _duplicate_accepted_text(a: dict[str, Any]) -> None:
    cells = a["prompt_universe.json"]["canonical_cells"]
    accepted = set(a["prompt_qa.json"]["accepted_candidate_ids"])
    texts = [c for cell in cells for c in cell["candidates"] if c["candidate_id"] in accepted]
    texts[1]["text"] = texts[0]["text"].upper() + "!!"


def _competitor_named_outside_shortlist(a: dict[str, Any]) -> None:
    cell, _ = _first_unaided_core(a)
    cell["aided_status"] = "competitor_aided"


def _campaign_term_without_exposure(a: dict[str, Any]) -> None:
    cell, cand = _first_unaided_core(a)
    cell["partition"] = "rotating"
    a["contamination_register.yaml"]["target_terms"]["campaign_terms"].append("Roam Free Week")
    cand["text"] = f"{cand['text']} during Roam Free Week"


def _accept_a_quarantined_candidate(a: dict[str, Any]) -> None:
    qa = a["prompt_qa.json"]
    decision = next(d for d in qa["decisions"] if d["candidate_id"] in qa["accepted_candidate_ids"])
    decision["status"] = "quarantine"


def _unknown_source(a: dict[str, Any]) -> None:
    a["buyer_jobs.json"]["jobs"][0]["supporting_source_ids"].append("source-never-fetched")


MUTATIONS: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
    ("architecture_job_references_resolve", _break_job_reference),
    ("accepted_prompt_contamination_zero", _leak_brand_into_unaided),
    ("qa_one_decision_per_candidate", _drop_qa_decision),
    ("qa_counts_reconcile", _miscount_qa),
    ("weights_exposure_priority_separate", _unseparate_weights),
    ("panel_selected_candidates_qa_approved", _select_unapproved),
    ("pending_gates_not_frozen", _freeze_with_pending_gate),
    ("report_lists_exact_prompt_text", _drop_prompt_text_from_report),
    ("prompt_enums_valid", _bad_enum),
    ("blind_brief_target_free", _brand_in_blind_brief),
    ("accepted_prompts_exact_unique", _duplicate_accepted_text),
    ("source_references_resolve", _unknown_source),
    ("band_aided_partition_consistent", _competitor_named_outside_shortlist),
    ("qa_accepted_are_pass", _accept_a_quarantined_candidate),
    ("accepted_prompt_contamination_zero", _campaign_term_without_exposure),
]


@pytest.mark.parametrize("run", RUNS)
@pytest.mark.parametrize(
    ("check_id", "mutate"), MUTATIONS, ids=[m[1].__name__.lstrip("_") for m in MUTATIONS]
)
def test_one_broken_field_fails_the_same_check_in_both_graders(
    grade: Any, tmp_path: Path, run: str, check_id: str, mutate: Callable[[dict[str, Any]], None]
) -> None:
    original = _load(_case_dir(FIXTURES / run))
    assert _ours(original)[check_id] is True

    mutated = copy.deepcopy(original)
    mutate(mutated)
    _write(tmp_path / "cases" / "mutated", mutated)
    theirs = _theirs(grade, tmp_path)
    ours = _ours(mutated)

    assert theirs[check_id] is False
    assert ours[check_id] is False
    assert ours == theirs


def test_a_missing_artifact_is_the_critical_parse_failure_and_nothing_else_runs() -> None:
    artifacts = _load(_case_dir(FIXTURES / RUNS[0]))
    del artifacts["prompt_qa.json"]
    checks = validate_artifacts(artifacts, strict_schema=False)
    assert [(c.id, c.passed, c.severity) for c in checks] == [
        ("required_artifacts_parse", False, "critical")
    ]
    assert checks_passed(checks) is False


def test_bare_contract_names_are_accepted_as_keys() -> None:
    by_file = _load(_case_dir(FIXTURES / RUNS[1]))
    by_name = {name.rsplit(".", 1)[0]: value for name, value in by_file.items()}
    assert _ours(by_name) == _ours(by_file)
