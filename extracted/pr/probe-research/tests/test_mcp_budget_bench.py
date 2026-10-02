"""Guard the synthetic benchmark's fixture and acceptance accounting."""

from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parents[2] / "scripts/mcp_budget_bench.py"
_SPEC = importlib.util.spec_from_file_location("mcp_budget_bench", _SCRIPT)
bench = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(bench)


def test_gold_fixture_parentage_and_counts_agree_with_records():
    source = bench.SyntheticSource()
    projects = source.browse()["projects"]
    assert sorted(row["name"] for row in projects if "LoRA" in row["name"]) == sorted(
        bench.PROJECT_NAMES
    )
    assert len(bench.PROJECT_NAMES) == bench.PROJECT_COUNT
    scoped = source.browse(scope=bench.PROJECT_REF)
    assert f"experiment:{scoped['experiments'][0]['id']}" == bench.LATEST_EXPERIMENT_REF
    _, project = source.get(bench.PROJECT_REF)
    assert project["active_run_count"] == sum(row["status"] == "running" for row in source.runs)
    for experiment in source.experiments:
        actual = [row for row in source.runs if row["experiment_id"] == experiment["id"]]
        assert experiment["run_count"] == len(actual)
        assert experiment["active_run_count"] == sum(row["status"] == "running" for row in actual)
    empty = source.browse(scope=f"project:{bench._uid(2)}")
    assert empty["experiments"] == empty["runs"] == empty["subprojects"] == []


def test_small_card_control_retains_gold_without_stress_fields():
    source = bench.SyntheticSource(large_entities=False)
    _, run = source.get(bench.RUN_REF)
    assert run["notes"] == bench.CAVEAT and run["status"] == "completed"
    assert "config" not in run and "document" not in run


def test_fixture_handle_walk_resumes_after_emitted_not_fetched_rows():
    source = bench.SyntheticSource(wide=True)
    cursor, emitted = None, []
    for _ in range(50):
        page = source.browse(limit=10, cursor=cursor, continuation_handles=True)
        rows, handle = page["projects"], page["continuation_handles"][0]
        prefix = rows[:2]
        emitted.extend(row["id"] for row in prefix)
        if len(prefix) == len(rows) and handle["next_cursor"] is None:
            break
        cursor = handle["after"][len(prefix) - 1]
    else:
        pytest.fail("synthetic handle source never terminated")
    assert emitted == [row["id"] for row in source.projects]


def _condition(
    *, tokens=100, byte_count=500, structured_bytes=0, calls=1, gold=True, ordinary=True
):
    return {
        "tasks": [
            {
                "task": "synthetic",
                "ordinary": ordinary,
                "gold_pass": gold,
                "read_calls": calls,
                "tokens": tokens,
                "bytes": byte_count,
                "source_reads": calls,
                "source_bytes": 1000 * calls,
                "tokens_with_catalog_once": tokens + 1000,
                "calls": [
                    {"tokens": tokens, "bytes": byte_count, "structured_bytes": structured_bytes}
                ],
            }
        ]
    }


@pytest.mark.parametrize(
    "change", [{"tokens": 2001}, {"byte_count": 16001}, {"structured_bytes": 10}]
)
def test_a_smaller_average_cannot_hide_one_cap_breach(change):
    result = bench.compare(_condition(tokens=3000, byte_count=30000), _condition(**change))
    assert result["candidate_cap_breaches"] == 1


def test_call_and_answer_gates_are_independent_of_size_savings():
    result = bench.compare(_condition(tokens=1000), _condition(tokens=10, calls=2, gold=False))
    assert result["tasks"][0]["token_reduction_pct"] == 99
    assert result["gold_gate"] is False
    assert result["ordinary_call_gate"] is False
    full_walk = bench.compare(_condition(ordinary=False), _condition(ordinary=False, calls=10))
    assert full_walk["ordinary_call_gate"] is True


def test_a_missing_candidate_task_cannot_make_the_pair_look_better():
    candidate = copy.deepcopy(_condition())
    candidate["tasks"] = []
    with pytest.raises(ValueError, match="same tasks"):
        bench.compare(_condition(), candidate)
