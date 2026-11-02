"""Fail-closed effective rules and complete current-head check-run evidence."""

import json
import subprocess
from copy import deepcopy
from unittest.mock import patch

import pytest

from agentic_devtools.cli.github._pr_check_requirements import _resolve_required_checks

_REPO = "swai-factory/agentic-devtools"
_HEAD = "c4870fc0018a5bbb80da69505126e864c3567d32"
_PAIRS = [
    ("Workflow Tests ✅", 122380957400),
    ("Smart Module Tests ✅", 122384266756),
    ("Targeted Checks ✅", 122378220001),
]
_RULES = [
    {
        "type": "required_status_checks",
        "parameters": {
            "strict_required_status_checks_policy": True,
            "required_status_checks": [{"context": name, "integration_id": 15368} for name, _ in _PAIRS],
        },
    }
]


def _run(run_id=1, name="extra", integration=15368, **changes):
    return {
        "id": run_id,
        "name": name,
        "app": {"id": integration},
        "head_sha": _HEAD,
        "status": "completed",
        "conclusion": "success",
        **changes,
    }


def _resolve(rules=None, runs=None, pages=None, **kwargs):
    runs = [_run(run_id, name) for name, run_id in _PAIRS] if runs is None else runs
    pages = [{"total_count": len(runs), "check_runs": runs}] if pages is None else pages
    responses = [
        subprocess.CompletedProcess([], 0, json.dumps([_RULES if rules is None else rules]), ""),
        subprocess.CompletedProcess([], 0, json.dumps(pages), ""),
    ]
    with patch("agentic_devtools.cli.github._pr_check_requirements.run_safe", side_effect=responses) as transport:
        result = _resolve_required_checks(kwargs.get("repo", _REPO), kwargs.get("base", "main"), _HEAD)
    return result, transport


def test_historical_required_pairs_and_exact_commands():
    result, transport = _resolve()
    assert result["ready"] and result["complete"]
    assert result["diagnostics"] == []
    assert {(r["name"], r["app"]["id"], r["id"]) for r in result["requiredChecks"]} == {
        (name, 15368, run_id) for name, run_id in _PAIRS
    }
    assert transport.call_count == 2
    for call in transport.call_args_list:
        assert call.kwargs == {"capture_output": True, "text": True, "shell": False, "timeout": 60}
        assert call.args[0][:2] == ["gh", "api"]
        assert call.args[0][-2:] == ["--paginate", "--slurp"]
        assert "per_page=100" in call.args[0][2]
    assert transport.call_args_list[0].args[0][2] == f"/repos/{_REPO}/rules/branches/main?per_page=100"
    assert transport.call_args_list[1].args[0][2] == (
        f"/repos/{_REPO}/commits/{_HEAD}/check-runs?per_page=100&filter=all"
    )


@pytest.mark.parametrize("conclusion", ["success", "neutral", "skipped"])
def test_actual_green_conclusions(conclusion):
    result, _ = _resolve(rules=[], runs=[_run(conclusion=conclusion)])
    assert result["ready"]
    assert result["checkRuns"][0]["conclusion"] == conclusion


@pytest.mark.parametrize(
    ("conclusion", "context_index"),
    [
        *[
            (conclusion, None)
            for conclusion in (
                "failure",
                "timed_out",
                "cancelled",
                "action_required",
                "startup_failure",
                "stale",
                "unknown",
                None,
                list[str](),
            )
        ],
        *[
            (outcome, context_index)
            for context_index in range(len(_PAIRS))
            for outcome in ("missing", "pending", "failure", "timed_out", "cancelled")
        ],
    ],
)
def test_newest_blocking_conclusions(conclusion, context_index):
    runs = [
        _run(run_id, name, conclusion=conclusion if context_index is None else "success") for name, run_id in _PAIRS
    ]
    if context_index is not None:
        context, run_id = _PAIRS[context_index]
        if conclusion == "missing":
            runs = [run for run in runs if run["name"] != context]
        else:
            runs[context_index] = _run(
                run_id,
                context,
                status="queued" if conclusion == "pending" else "completed",
                conclusion=None if conclusion == "pending" else conclusion,
            )
    result, _ = _resolve(runs=runs)
    assert not result["ready"] and result["diagnostics"]
    assert result["complete"]
    if conclusion == "missing":
        assert any("Missing required check" in d for d in result["diagnostics"])


@pytest.mark.parametrize("status", ["queued", "in_progress", "waiting", "pending", None, []])
def test_pending_or_unrecognized_status_blocks(status):
    result, _ = _resolve(rules=[], runs=[_run(status=status)])
    assert not result["ready"] and result["diagnostics"]


def test_missing_required_runs_never_pass():
    for runs in ([], [_run()], [_run(name=_PAIRS[0][0], integration=999)]):
        result, _ = _resolve(runs=runs)
        assert not result["ready"]
        assert any("Missing required check" in d for d in result["diagnostics"])


@pytest.mark.parametrize("integration", [None, 0, -1, True, "15368", {}, []])
def test_invalid_required_integration(integration):
    rules = deepcopy(_RULES)
    rules[0]["parameters"]["required_status_checks"][0]["integration_id"] = integration
    result, _ = _resolve(rules=rules)
    assert not result["ready"] and not result["complete"]
    assert "integration_id" in result["diagnostics"][0]


def test_absent_required_integration():
    rules = deepcopy(_RULES)
    del rules[0]["parameters"]["required_status_checks"][0]["integration_id"]
    result, _ = _resolve(rules=rules)
    assert not result["ready"] and "integration_id" in result["diagnostics"][0]


@pytest.mark.parametrize("app", [None, {}, {"id": None}, {"id": True}, {"id": 0}, {"id": "15368"}])
def test_uncertain_run_integration(app):
    result, _ = _resolve(rules=[], runs=[_run(app=app)])
    assert not result["ready"] and not result["complete"]


@pytest.mark.parametrize(
    "rules",
    [
        {},
        [None],
        [{}],
        [{"type": None}],
        [{"type": []}],
        [{"type": ""}],
        [{"type": "required_status_checks"}],
        [{"type": "required_status_checks", "parameters": []}],
        [{"type": "required_status_checks", "parameters": {}}],
        [{"type": "required_status_checks", "parameters": {"required_status_checks": {}}}],
        [{"type": "required_status_checks", "parameters": {"required_status_checks": [None]}}],
        [{"type": "required_status_checks", "parameters": {"required_status_checks": [{"context": ""}]}}],
        [{"type": "required_status_checks", "parameters": {"required_status_checks": [{"context": 1}]}}],
    ],
)
def test_malformed_rules(rules):
    result, _ = _resolve(rules=rules)
    assert not result["ready"] and not result["complete"]
    assert result["diagnostics"]


def test_empty_required_list_and_unrelated_rules_are_valid():
    result, _ = _resolve(
        rules=[{"type": "deletion"}, {"type": "required_status_checks", "parameters": {"required_status_checks": []}}],
        runs=[],
    )
    assert result["ready"] and result["requiredChecks"] == []


@pytest.mark.parametrize("conclusion,status", [("success", "completed"), ("failure", "completed"), (None, "queued")])
def test_empty_rules_preserve_actual_run_blockers(conclusion, status):
    result, _ = _resolve(rules=[], runs=[_run(conclusion=conclusion, status=status)])
    assert result["ready"] == (conclusion == "success")
    assert len(result["checkRuns"]) == 1


def test_truncated_30_of_42_and_complete_30_plus_12():
    runs = [_run(i + 1) for i in range(42)]
    first = {"total_count": 42, "check_runs": runs[:30]}
    result, _ = _resolve(rules=[], pages=[first])
    assert not result["ready"] and not result["complete"]
    assert "42" in result["diagnostics"][0]
    result, _ = _resolve(rules=[], pages=[first, {"total_count": 42, "check_runs": runs[30:]}])
    assert result["ready"] and len(result["checkRuns"]) == 1
    assert result["checkRuns"][0]["id"] == 42


@pytest.mark.parametrize(
    "pages",
    [
        [],
        {},
        [None],
        [{}],
        [{"total_count": True, "check_runs": []}],
        [{"total_count": -1, "check_runs": []}],
        [{"total_count": "0", "check_runs": []}],
        [{"total_count": 0, "check_runs": {}}],
        [{"total_count": 0, "check_runs": []}, {"total_count": 1, "check_runs": []}],
        [{"total_count": 0, "check_runs": [_run()]}],
        [{"total_count": 1, "check_runs": [None]}],
    ],
)
def test_malformed_or_incomplete_pages(pages):
    result, _ = _resolve(rules=[], pages=pages)
    assert not result["ready"] and not result["complete"] and result["diagnostics"]


@pytest.mark.parametrize(
    "changes",
    [{"id": None}, {"id": True}, {"id": "1"}, {"id": 0}, {"name": None}, {"name": ""}, {"head_sha": "a" * 40}],
)
def test_invalid_run_identity_or_wrong_head(changes):
    result, _ = _resolve(rules=[], runs=[_run(**changes)])
    assert not result["ready"] and not result["complete"]


def test_identical_duplicate_ids_allowed_but_conflicts_rejected():
    run = _run()
    result, _ = _resolve(rules=[], pages=[{"total_count": 1, "check_runs": [run, deepcopy(run)]}])
    assert result["ready"]
    result, _ = _resolve(rules=[], pages=[{"total_count": 1, "check_runs": [run, _run(conclusion="failure")]}])
    assert not result["ready"] and "Conflicting" in result["diagnostics"][0]


@pytest.mark.parametrize(
    "new_conclusion,new_status", [("success", "completed"), ("failure", "completed"), (None, "queued")]
)
@pytest.mark.parametrize("reverse", [False, True])
def test_greatest_numeric_id_selects_attempt(new_conclusion, new_status, reverse):
    name = _PAIRS[0][0]
    rules = deepcopy(_RULES)
    rules[0]["parameters"]["required_status_checks"] = [{"context": name, "integration_id": 15368}]
    runs = [
        _run(9, name, conclusion="failure" if new_conclusion == "success" else "success"),
        _run(10, name, conclusion=new_conclusion, status=new_status),
    ]
    result, _ = _resolve(rules=rules, runs=list(reversed(runs)) if reverse else runs)
    assert result["ready"] == (new_conclusion == "success")
    assert result["requiredChecks"][0]["id"] == 10


def test_same_name_different_integrations_do_not_supersede():
    rules = deepcopy(_RULES)
    rules[0]["parameters"]["required_status_checks"] = [{"context": "extra", "integration_id": 15368}]
    result, _ = _resolve(rules=rules, runs=[_run(1), _run(2, integration=999, conclusion="failure")])
    assert not result["ready"]
    assert result["requiredChecks"][0]["id"] == 1
    assert len(result["checkRuns"]) == 2


def test_multiple_rule_pages_are_aggregated():
    responses = [
        subprocess.CompletedProcess([], 0, json.dumps([[], _RULES]), ""),
        subprocess.CompletedProcess([], 0, json.dumps([{"total_count": 0, "check_runs": []}]), ""),
    ]
    with patch("agentic_devtools.cli.github._pr_check_requirements.run_safe", side_effect=responses):
        result = _resolve_required_checks(_REPO, "main", _HEAD)
    assert not result["ready"] and len(result["diagnostics"]) == 3


@pytest.mark.parametrize("stage", [0, 1])
@pytest.mark.parametrize(
    "response",
    [
        subprocess.CompletedProcess([], 1, "", "HTTP 429 rate limited"),
        subprocess.CompletedProcess([], 1, "", "503 service unavailable"),
        subprocess.CompletedProcess([], 1, "", ""),
        subprocess.CompletedProcess([], 0, "not json", ""),
        subprocess.CompletedProcess([], 0, "[]\n[]", ""),
        subprocess.CompletedProcess([], 0, "[]", ""),
        subprocess.CompletedProcess([], 0, "{}", ""),
        FileNotFoundError("gh missing"),
        subprocess.TimeoutExpired("gh", 60),
        subprocess.CalledProcessError(1, "gh"),
    ],
)
def test_transport_errors_and_malformed_slurped_response(stage, response):
    good = subprocess.CompletedProcess([], 0, json.dumps([[]]), "")
    with patch("agentic_devtools.cli.github._pr_check_requirements.run_safe", side_effect=[good] * stage + [response]):
        result = _resolve_required_checks(_REPO, "main", _HEAD)
    assert not result["ready"] and not result["complete"] and result["diagnostics"]


@pytest.mark.parametrize(
    "base",
    [
        None,
        "",
        42,
        " main",
        "main ",
        "-main",
        "a..b",
        "a@{b",
        "a//b",
        "/main",
        "main/",
        "a.lock",
        "a/.b",
        "a b",
        "a\\b",
        "a?b",
        "a*b",
        "a[b",
        "a~b",
        "a^b",
        "a:b",
        "a\x7fb",
        "a\nb",
        "@",
        "main.",
    ],
)
def test_invalid_base_fails_before_transport(base):
    result, transport = _resolve(base=base)
    assert not result["ready"] and "base" in result["diagnostics"][0]
    transport.assert_not_called()


@pytest.mark.parametrize("repo", ["owner/.github", "owner/-repo"])
def test_valid_repository_with_leading_dot_or_hyphen(repo):
    result, transport = _resolve(repo=repo)
    assert result["ready"]
    assert transport.call_args_list[0].args[0][2].startswith(f"/repos/{repo}/rules/")


@pytest.mark.parametrize("repo", [None, "", "owner", "a/b/c", "../repo", "a/.", "a/..", "-a/b", "a/b?x=y"])
def test_invalid_repository(repo):
    with patch("agentic_devtools.cli.github._pr_check_requirements.run_safe") as transport:
        result = _resolve_required_checks(repo, "main", _HEAD)
    assert not result["ready"] and "repo" in result["diagnostics"][0]
    transport.assert_not_called()


@pytest.mark.parametrize("head", [None, "", "a" * 39, "g" * 40, 42])
def test_invalid_head(head):
    with patch("agentic_devtools.cli.github._pr_check_requirements.run_safe") as transport:
        result = _resolve_required_checks(_REPO, "main", head)
    assert not result["ready"] and "head" in result["diagnostics"][0]
    transport.assert_not_called()


def test_branch_path_is_url_encoded():
    result, transport = _resolve(base="release/é#100%")
    assert result["ready"]
    assert "/rules/branches/release%2F%C3%A9%23100%25?per_page=100" in transport.call_args_list[0].args[0][2]
