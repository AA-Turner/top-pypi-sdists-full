# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""Tests for the reproduction-case gate.

PRs are real commits in a temporary git repository, and the sandbox CLI is an
executable on `PATH` that answers `validate` and offline discovery commands, so
the code under test spawns real processes.
"""

from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

import pytest

from airbyte_ops_mcp.regression_tests import case_gate
from airbyte_ops_mcp.regression_tests.case_gate import (
    CASES_DIR,
    GateReport,
    case_scope,
    changed_paths,
    exists_at,
    gate_step_outputs,
    trusted_origin_problems,
)
from airbyte_ops_mcp.regression_tests.ci_output import write_github_outputs
from airbyte_ops_mcp.regression_tests.repro_case import CaseOrigin, ReproCase

pytestmark = pytest.mark.unit

# The pin the fixture cases' `origin.json` records.
PIN = "7b8a09d7c7a6769a245f577872c21356d5b8ecfd"


def check_case(*args, **kwargs):
    return case_gate.check_case(*args, **{"sandbox_ref": PIN, **kwargs})


def run_case_gate(*args, **kwargs):
    return case_gate.run_case_gate(*args, **{"sandbox_ref": PIN, **kwargs})


def run_case_dir_gate(*args, **kwargs):
    return case_gate.run_case_dir_gate(*args, **{"sandbox_ref": PIN, **kwargs})


FIXTURES = Path(__file__).parent / "fixtures"
CASE_FIXTURE = FIXTURES / "repro_case" / "minimal"
CONNECTOR_FIXTURE = FIXTURES / "sandbox_support" / "source-example"

DISCOVERY = {
    "providers": {
        "providers": [
            {"id": "slack", "hosts": ["slack.com"], "unknown_parameters": "reject"}
        ]
    },
    "operations slack": {
        "provider": "slack",
        "operations": [
            {
                "id": "get.api.conversations.list",
                "method": "GET",
                "path": "/api/conversations.list",
                "status": "supported",
                "parameters": [
                    {"name": name, "in": "query"}
                    for name in ("cursor", "limit", "types")
                ],
                "pagination": {"limit_param": "limit", "max_limit": 1000},
            }
        ],
    },
}

# `dataset validate` / `behavior validate` reject a file containing "INVALID".
_FAKE_SANDBOX = """\
import json, os, sys
args = sys.argv[1:]
if len(args) == 3 and args[1] == "validate":
    if "INVALID" in open(args[2]).read():
        print("Error: Invalid spec", file=sys.stderr)
        sys.exit(1)
    print(json.dumps({"valid": True}))
    sys.exit(0)
if args[-1] != "--offline":
    sys.exit(2)
discovery = json.load(open(os.environ["FAKE_DISCOVERY"]))
key = " ".join(args[:-1])
if key not in discovery:
    sys.exit(1)
print(json.dumps(discovery[key]))
"""


@pytest.fixture(autouse=True)
def fake_sandbox(tmp_path, monkeypatch):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    executable = bin_dir / "sandbox"
    executable.write_text(f"#!{sys.executable}\n{_FAKE_SANDBOX}")
    executable.chmod(executable.stat().st_mode | stat.S_IXUSR)
    discovery = tmp_path / "discovery.json"
    discovery.write_text(json.dumps(DISCOVERY))
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setenv("FAKE_DISCOVERY", str(discovery))


@pytest.fixture
def connector_dir(tmp_path) -> Path:
    """The example connector, with the case's `threads` stream reading channels."""
    target = tmp_path / "source-slack"
    shutil.copytree(CONNECTOR_FIXTURE, target)
    manifest = target / "manifest.yaml"
    manifest.write_text(
        manifest.read_text().replace("name: channels", "name: threads", 1)
    )
    return target


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.invalid",
            *args,
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


@pytest.fixture
def repo(tmp_path) -> Path:
    """A repository whose `main` holds one existing case; HEAD is a PR branch."""
    repo = tmp_path / "repo"
    subprocess.run(["git", "init", "-q", "-b", "main", str(repo)], check=True)
    (repo / "README.md").write_text("ops\n")
    shutil.copytree(CASE_FIXTURE, repo / CASES_DIR / "source-slack" / "existing")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "base")
    _git(repo, "checkout", "-qb", "pr")
    return repo


def _add_case(repo: Path, name: str = "new-case") -> Path:
    case = repo / CASES_DIR / "source-slack" / name
    shutil.copytree(CASE_FIXTURE, case)
    return case


def _commit(repo: Path) -> None:
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "pr")


def _scope(repo: Path):
    return case_scope(
        changed_paths(repo, "main", "HEAD"),
        lambda path: exists_at(repo, "main", path),
    )


def test_a_pr_without_cases_is_not_a_case_pr(repo):
    (repo / "README.md").write_text("changed\n")
    _commit(repo)

    assert _scope(repo) == (None, None, [])


def test_a_pr_adding_one_new_case_is_in_scope(repo):
    _add_case(repo)
    _commit(repo)

    assert _scope(repo) == ("source-slack", "new-case", [])


def test_changing_an_existing_case_needs_a_human(repo):
    expectations = repo / CASES_DIR / "source-slack" / "existing" / "expectations.json"
    expectations.write_text(json.dumps({"records": {"threads": []}}))
    _commit(repo)

    connector, case, problems = _scope(repo)

    assert (connector, case) == ("source-slack", "existing")
    assert any("(M)" in problem for problem in problems)
    assert any("already exists" in problem for problem in problems)


def test_adding_a_file_to_an_existing_case_needs_a_human(repo):
    (repo / CASES_DIR / "source-slack" / "existing" / "notes.json").write_text("{}")
    _commit(repo)

    _, _, problems = _scope(repo)

    assert any("already exists" in problem for problem in problems)


def test_a_case_pr_may_not_change_anything_else(repo):
    _add_case(repo)
    (repo / "README.md").write_text("changed\n")
    _commit(repo)

    _, _, problems = _scope(repo)

    assert any("README.md" in problem for problem in problems)


def test_a_case_pr_adds_exactly_one_case(repo):
    _add_case(repo, "first")
    _add_case(repo, "second")
    _commit(repo)

    assert _scope(repo) == (
        None,
        None,
        ["a case PR must add exactly one case, not 2"],
    )


def test_a_valid_case_passes(repo, connector_dir):
    _add_case(repo)
    _commit(repo)

    report = run_case_gate(
        repo,
        "main",
        connector_dir=connector_dir,
        check_origin=lambda origin, connector: [],
    )

    assert report.problems == []
    assert report.status == "pass"
    assert report.affected_image == "airbyte/source-slack:3.2.19"
    assert report.affected_ref == "4d07056bddb097a417c5c8895a3885ae25a24628"
    assert report.support and report.support["result"] == "supported"


def test_a_pr_without_cases_passes_as_not_applicable(repo):
    (repo / "README.md").write_text("changed\n")
    _commit(repo)

    assert run_case_gate(repo, "main").status == "n/a"


def test_an_auto_merged_case_needs_an_origin(tmp_path):
    case = tmp_path / "case"
    shutil.copytree(CASE_FIXTURE, case)
    (case / "origin.json").unlink()

    report = check_case(case, "source-slack", check_origin=lambda origin, connector: [])

    assert report.status == "fail"
    assert any("origin.json is required" in problem for problem in report.problems)


def test_origin_problems_and_check_errors_fail_the_gate(tmp_path, connector_dir):
    case = tmp_path / "case"
    shutil.copytree(CASE_FIXTURE, case)

    def unreachable(origin, connector):
        raise ConnectionError("GitHub is down")

    for checker, expected in (
        (lambda origin, connector: ["image not published"], "image not published"),
        (unreachable, "could not check origin.json: GitHub is down"),
    ):
        report = check_case(
            case, "source-slack", check_origin=checker, connector_dir=connector_dir
        )
        assert report.status == "fail"
        assert expected in report.problems


def test_invalid_sandbox_inputs_fail_the_gate(tmp_path, connector_dir):
    case = tmp_path / "case"
    shutil.copytree(CASE_FIXTURE, case)
    (case / "sandbox" / "behavior.json").write_text('{"INVALID": true}')

    report = check_case(
        case,
        "source-slack",
        check_origin=lambda origin, connector: [],
        connector_dir=connector_dir,
    )

    assert report.problems == ["sandbox/behavior.json is invalid: Error: Invalid spec"]


def test_a_stream_the_twin_does_not_cover_fails_the_gate(tmp_path):
    case = tmp_path / "case"
    shutil.copytree(CASE_FIXTURE, case)

    # The example connector has no `threads` stream, so nothing can be checked.
    report = check_case(
        case,
        "source-slack",
        check_origin=lambda origin, connector: [],
        connector_dir=CONNECTOR_FIXTURE,
    )

    assert report.status == "fail"
    assert report.support and report.support["result"] != "supported"
    assert any("static support check says" in p for p in report.problems)


def _no_origin_problems(origin, connector):
    return []


def test_the_case_is_read_at_the_head_commit_not_from_the_working_tree(
    repo, connector_dir
):
    case = _add_case(repo)
    _commit(repo)
    # Uncommitted edits are not what would merge, so the gate ignores them.
    (case / "sandbox" / "behavior.json").write_text('{"INVALID": true}')

    report = run_case_gate(
        repo, "main", connector_dir=connector_dir, check_origin=_no_origin_problems
    )

    assert report.status == "pass"
    assert report.case_dir == f"{CASES_DIR}/source-slack/new-case"


def test_a_committed_invalid_case_fails_even_if_the_working_tree_is_fixed(
    repo, connector_dir
):
    case = _add_case(repo)
    behavior = case / "sandbox" / "behavior.json"
    valid = behavior.read_text()
    behavior.write_text('{"INVALID": true}')
    _commit(repo)
    behavior.write_text(valid)

    report = run_case_gate(
        repo, "main", connector_dir=connector_dir, check_origin=_no_origin_problems
    )

    assert report.problems == ["sandbox/behavior.json is invalid: Error: Invalid spec"]


def test_a_clone_like_the_workflow_reads_the_head_by_sha(repo, tmp_path, connector_dir):
    _add_case(repo)
    _commit(repo)
    head = _git(repo, "rev-parse", "HEAD")
    # The workflow checks out `main` with every branch fetched, then names the
    # PR head by SHA.
    clone = tmp_path / "clone"
    subprocess.run(
        ["git", "clone", "-q", "--no-local", "-b", "main", str(repo), str(clone)],
        check=True,
    )

    report = run_case_gate(
        clone,
        "origin/main",
        head,
        require_case=True,
        connector_dir=connector_dir,
        check_origin=_no_origin_problems,
    )

    assert report.status == "pass"
    with pytest.raises(subprocess.CalledProcessError):
        run_case_gate(clone, "origin/main", "0" * 40, require_case=True)


def test_require_case_turns_not_applicable_into_a_failure(repo):
    (repo / "README.md").write_text("changed\n")
    _commit(repo)

    report = run_case_gate(repo, "main", require_case=True)

    assert report.status == "fail"
    assert report.problems == ["the PR adds no case"]


def test_a_symlink_in_a_case_is_refused(repo):
    case = _add_case(repo)
    (case / "state.json").unlink()
    (case / "state.json").symlink_to("../../../README.md")
    _commit(repo)

    _, _, problems = _scope(repo)

    assert any("state.json (120000)" in problem for problem in problems)
    assert run_case_gate(repo, "main").status == "fail"


def test_an_executable_in_a_case_is_refused(repo):
    case = _add_case(repo)
    state = case / "state.json"
    state.chmod(state.stat().st_mode | stat.S_IXUSR)
    _commit(repo)

    _, _, problems = _scope(repo)

    assert any("state.json (100755)" in problem for problem in problems)


@pytest.mark.parametrize("name", ["notes.md", ".gitattributes", "sandbox/extra.json"])
def test_files_a_case_may_not_hold_are_refused(repo, name):
    case = _add_case(repo)
    (case / name).write_text("{}")
    _commit(repo)

    _, _, problems = _scope(repo)

    assert any(
        problem.startswith("files a case may not hold: " + name) for problem in problems
    )


def _origin(**overrides: str) -> CaseOrigin:
    payload = json.loads((CASE_FIXTURE / "origin.json").read_text())
    return CaseOrigin.from_json({**payload, **overrides})


def test_only_airbyte_origins_are_trusted():
    problems = trusted_origin_problems(
        _origin(repo="airbyte-enterprise"),
        "source-slack",
        None,
        check_origin=lambda origin, connector, token: [],
        is_ancestor=lambda *args: True,
    )

    assert problems == [
        "origin.json `repo` is 'airbyte-enterprise'; only 'airbyte' cases merge "
        "without review"
    ]


def test_an_affected_ref_off_master_is_not_trusted():
    calls = []

    def is_ancestor(owner, repo, sha, branch, token):
        calls.append((owner, repo, sha, branch))
        return False

    problems = trusted_origin_problems(
        _origin(),
        "source-slack",
        None,
        check_origin=lambda origin, connector, token: ["image not published"],
        is_ancestor=is_ancestor,
    )

    sha = "4d07056bddb097a417c5c8895a3885ae25a24628"
    assert calls == [("airbytehq", "airbyte", sha, "master")]
    assert problems == [
        "image not published",
        f"affected_ref {sha} is not on airbytehq/airbyte master",
    ]


def test_an_ancestry_check_error_fails_the_gate_closed(tmp_path, connector_dir):
    case = tmp_path / "case"
    shutil.copytree(CASE_FIXTURE, case)

    def is_ancestor(*args):
        raise TimeoutError("compare timed out")

    report = check_case(
        case,
        "source-slack",
        check_origin=lambda origin, connector: trusted_origin_problems(
            origin,
            connector,
            None,
            check_origin=lambda *args: [],
            is_ancestor=is_ancestor,
        ),
        connector_dir=connector_dir,
    )

    assert report.status == "fail"
    assert report.problems == ["could not check origin.json: compare timed out"]


def test_a_case_directory_is_checked_without_a_pr(tmp_path, connector_dir):
    case = tmp_path / "source-slack" / "new-case"
    shutil.copytree(CASE_FIXTURE, case)

    report = run_case_dir_gate(
        case, connector_dir=connector_dir, check_origin=_no_origin_problems
    )

    assert report.status == "pass"
    assert (report.connector, report.case) == ("source-slack", "new-case")

    (case / "notes.md").write_text("hi")
    report = run_case_dir_gate(
        case, connector_dir=connector_dir, check_origin=_no_origin_problems
    )
    (problem,) = report.problems
    assert problem.startswith("files a case may not hold: notes.md (allowed: ")

    (case / "notes.md").unlink()
    (case / "state.json").unlink()
    (case / "state.json").symlink_to(tmp_path / "elsewhere.json")
    report = run_case_dir_gate(
        case, connector_dir=connector_dir, check_origin=_no_origin_problems
    )
    assert report.problems == ["case files must not be symlinks: state.json"]


def test_step_outputs_cannot_be_forged_by_problems(tmp_path, monkeypatch):
    output = tmp_path / "github_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(output))
    report = GateReport(
        status="fail",
        connector="source-slack\nstatus=pass",
        case="new-case",
        problems=["bad name\nstatus=pass", "second"],
    )

    write_github_outputs(gate_step_outputs(report))

    lines = output.read_text().splitlines()
    assert [line for line in lines if line.startswith("status=")] == ["status=fail"]
    assert lines[-1] == "status=fail"
    assert "connector=" in lines
    assert json.loads(
        next(line for line in lines if line.startswith("problems="))[9:]
    ) == ["bad name\nstatus=pass", "second"]


def test_paths_with_control_characters_are_refused_before_anything_quotes_them(repo):
    case = _add_case(repo)
    (case / "state.json").rename(case / "sta\nte.json")
    _commit(repo)

    path = f"{CASES_DIR}/source-slack/new-case/sta\nte.json"
    assert _scope(repo) == (None, None, [f"paths with control characters: {path!r}"])


def test_a_case_deleted_on_the_base_since_the_pr_branched_cannot_be_added_to(repo):
    existing = repo / CASES_DIR / "source-slack" / "existing"
    _git(repo, "checkout", "-q", "main")
    origin = (existing / "origin.json").read_text()
    (existing / "origin.json").unlink()
    _commit(repo)
    _git(repo, "checkout", "-qb", "pr2")
    _git(repo, "checkout", "-q", "main")
    _git(repo, "rm", "-rq", str(existing))
    _commit(repo)
    _git(repo, "checkout", "-q", "pr2")
    existing.mkdir(parents=True, exist_ok=True)
    (existing / "origin.json").write_text(origin)
    _commit(repo)

    report = run_case_gate(repo, "main", check_origin=_no_origin_problems)

    assert report.status == "fail"
    assert any("already exists on the base branch" in p for p in report.problems)


def test_several_merge_bases_fail_the_gate(repo):
    # Criss-cross history: main and the PR each merged the other's commit.
    _git(repo, "checkout", "-q", "main")
    (repo / "a.txt").write_text("a\n")
    _commit(repo)
    _git(repo, "checkout", "-q", "pr")
    (repo / "p.txt").write_text("p\n")
    _commit(repo)
    _git(repo, "checkout", "-q", "main")
    _git(repo, "merge", "-q", "--no-ff", "--no-edit", "pr")
    _git(repo, "checkout", "-q", "pr")
    _git(repo, "merge", "-q", "--no-ff", "--no-edit", "main~1")
    _add_case(repo)
    _commit(repo)

    report = run_case_gate(repo, "main", check_origin=_no_origin_problems)

    assert report.status == "fail"
    assert report.problems == ["HEAD has 2 merge bases with main"]


def test_a_sandbox_validate_that_cannot_run_is_a_problem(tmp_path, monkeypatch):
    case = tmp_path / "case"
    shutil.copytree(CASE_FIXTURE, case)
    executable = shutil.which("sandbox")
    assert executable
    Path(executable).write_text("#!/bin/sh\nsleep 5\n")
    monkeypatch.setattr(case_gate, "SANDBOX_COMMAND_TIMEOUT_SECONDS", 0.1)

    problems = case_gate.sandbox_input_problems(ReproCase.load(case))

    assert len(problems) == 2
    assert all("could not be validated" in problem for problem in problems)


def test_a_symlinked_case_directory_is_refused(tmp_path, connector_dir):
    case = tmp_path / "source-slack" / "real-case"
    shutil.copytree(CASE_FIXTURE, case)
    link = tmp_path / "source-slack" / "linked-case"
    link.symlink_to(case)

    report = run_case_dir_gate(
        link, connector_dir=connector_dir, check_origin=_no_origin_problems
    )

    assert report.problems == ["case files must not be symlinks: ."]


def _origin_payload(**overrides):
    return {**json.loads((CASE_FIXTURE / "origin.json").read_text()), **overrides}


def test_a_case_without_a_sandbox_ref_is_refused(tmp_path, connector_dir):
    case = tmp_path / "case"
    shutil.copytree(CASE_FIXTURE, case)
    payload = _origin_payload()
    del payload["sandbox_ref"]
    (case / "origin.json").write_text(json.dumps(payload))

    report = check_case(
        case,
        "source-slack",
        check_origin=_no_origin_problems,
        connector_dir=connector_dir,
    )

    assert report.problems == [
        f"origin.json sandbox_ref is missing; set it to the current saas-sandbox pin {PIN}"
    ]


def test_a_sandbox_ref_that_is_not_a_full_sha_is_refused(tmp_path, connector_dir):
    case = tmp_path / "case"
    shutil.copytree(CASE_FIXTURE, case)
    (case / "origin.json").write_text(
        json.dumps(_origin_payload(sandbox_ref="7b8a09d"))
    )

    report = check_case(
        case,
        "source-slack",
        check_origin=_no_origin_problems,
        connector_dir=connector_dir,
    )

    assert report.problems == [
        "origin.json sandbox_ref must be a full 40-character commit SHA"
    ]


def test_a_case_validated_on_another_sandbox_commit_is_refused(repo, connector_dir):
    case = _add_case(repo)
    other = "1" * 40
    (case / "origin.json").write_text(json.dumps(_origin_payload(sandbox_ref=other)))
    _commit(repo)

    report = run_case_gate(
        repo, "main", connector_dir=connector_dir, check_origin=_no_origin_problems
    )

    assert report.status == "fail"
    assert report.problems == [
        f"origin.json sandbox_ref {other} is not the current saas-sandbox pin {PIN}"
    ]


def test_the_reference_case_records_the_repository_pin():
    # The gate smoke runs the reference case against the pin, so a pin bump
    # must update the fixture too.
    repo_root = Path(__file__).resolve().parents[1]
    reference = (
        repo_root / "tests/fixtures/regression_cases/source-slack"
        "/threads-fractional-cursor-429/origin.json"
    )
    pin = case_gate.read_sandbox_pin(repo_root / case_gate.SANDBOX_PIN_FILE)

    assert json.loads(reference.read_text())["sandbox_ref"] == pin


def _case_with_expectations(tmp_path: Path, **changes: object) -> Path:
    case = tmp_path / "case"
    shutil.copytree(CASE_FIXTURE, case)
    expectations = json.loads((case / "expectations.json").read_text())
    for key, value in changes.items():
        if value is None:
            expectations.pop(key, None)
        else:
            expectations[key] = value
    (case / "expectations.json").write_text(json.dumps(expectations))
    return case


def _manifest_only(connector: Path) -> Path:
    metadata = connector / "metadata.yaml"
    metadata.write_text(
        metadata.read_text() + "  tags:\n    - language:manifest-only\n"
    )
    return connector


def test_a_new_stream_case_passes_when_the_affected_release_lacks_the_stream(
    tmp_path,
):
    case = _case_with_expectations(tmp_path, new_streams=["threads"])
    connector = tmp_path / "source-slack"
    shutil.copytree(CONNECTOR_FIXTURE, connector)

    # The example connector defines no `threads` stream.
    report = check_case(
        case,
        "source-slack",
        check_origin=_no_origin_problems,
        connector_dir=_manifest_only(connector),
    )

    assert report.problems == []
    assert report.status == "pass"
    assert report.support is not None
    # Only the provider host is checked, since no other stream is configured.
    assert (report.support["result"], report.support["operations"]) == ("supported", [])
    assert report.support["new_streams_unchecked"] == ["threads"]


def test_a_new_stream_case_fails_when_no_stream_calls_a_host_the_twin_serves(
    tmp_path,
):
    # allowedHosts reach the slack twin (as a shared token host would), but
    # every stream calls another host.
    case = _case_with_expectations(tmp_path, new_streams=["threads"])
    connector = tmp_path / "source-slack"
    shutil.copytree(CONNECTOR_FIXTURE, connector)
    _manifest_only(connector)
    manifest = connector / "manifest.yaml"
    manifest.write_text(
        manifest.read_text().replace(
            "https://slack.com/api/", "https://files.example.com/api/"
        )
    )
    metadata = connector / "metadata.yaml"
    metadata.write_text(
        metadata.read_text().replace(
            "- slack.com", "- slack.com\n      - files.example.com"
        )
    )

    report = check_case(
        case, "source-slack", check_origin=_no_origin_problems, connector_dir=connector
    )

    assert report.status == "fail"
    assert report.support is not None
    assert report.support["result"] == "unsupported"
    assert "no stream requests a host they serve" in report.support["reasons"][0]


def test_a_new_stream_the_affected_release_defines_fails_the_gate(
    tmp_path, connector_dir
):
    case = _case_with_expectations(tmp_path, new_streams=["threads"])

    report = check_case(
        case,
        "source-slack",
        check_origin=_no_origin_problems,
        connector_dir=_manifest_only(connector_dir),
    )

    assert report.status == "fail"
    assert any("which the manifest at" in problem for problem in report.problems)


def test_a_new_stream_needs_a_manifest_only_connector(tmp_path):
    case = _case_with_expectations(tmp_path, new_streams=["threads"])

    # Without the manifest-only tag, Python streams could define it.
    report = check_case(
        case,
        "source-slack",
        check_origin=_no_origin_problems,
        connector_dir=CONNECTOR_FIXTURE,
    )

    assert report.status == "fail"
    assert any("manifest-only connector" in problem for problem in report.problems)


def test_a_new_stream_needs_a_manifest_to_confirm_it(tmp_path):
    case = _case_with_expectations(tmp_path, new_streams=["threads"])
    connector = tmp_path / "source-slack"
    connector.mkdir()
    shutil.copy(CONNECTOR_FIXTURE / "metadata.yaml", connector / "metadata.yaml")

    report = check_case(
        case, "source-slack", check_origin=_no_origin_problems, connector_dir=connector
    )

    assert report.status == "fail"
    assert any("manifest-only connector" in problem for problem in report.problems)


def test_a_check_case_checks_the_streams_the_check_reads(tmp_path, connector_dir):
    case = _case_with_expectations(
        tmp_path,
        records=None,
        final_state=None,
        command="check",
        check_status="SUCCEEDED",
    )
    manifest = connector_dir / "manifest.yaml"
    manifest.write_text(
        manifest.read_text().replace(
            "stream_names: [channels]", "stream_names: [members]"
        )
    )

    report = check_case(
        case,
        "source-slack",
        check_origin=_no_origin_problems,
        connector_dir=connector_dir,
    )

    # `members` calls an operation the twin does not list, unlike `threads`.
    assert report.support is not None
    assert {need["stream"] for need in report.support["operations"]} == {"members"}
    assert report.status == "fail"


def test_a_check_case_with_an_empty_catalog_still_checks_the_check(
    tmp_path, connector_dir
):
    case = _case_with_expectations(
        tmp_path,
        records=None,
        final_state=None,
        command="check",
        check_status="SUCCEEDED",
    )
    catalog = json.loads((case / "catalog.json").read_text())
    (case / "catalog.json").write_text(json.dumps({**catalog, "streams": []}))
    manifest = connector_dir / "manifest.yaml"
    manifest.write_text(
        manifest.read_text().replace(
            "stream_names: [channels]", "stream_names: [members]"
        )
    )

    report = check_case(
        case,
        "source-slack",
        check_origin=_no_origin_problems,
        connector_dir=connector_dir,
    )

    assert report.support is not None
    assert {need["stream"] for need in report.support["operations"]} == {"members"}


def test_a_manifest_that_does_not_resolve_confirms_no_new_stream(tmp_path):
    case = _case_with_expectations(tmp_path, new_streams=["threads"])
    connector = tmp_path / "source-slack"
    shutil.copytree(CONNECTOR_FIXTURE, connector)
    manifest = connector / "manifest.yaml"
    manifest.write_text(
        manifest.read_text().replace("#/definitions/requester", "#/definitions/nope")
    )

    report = check_case(
        case,
        "source-slack",
        check_origin=_no_origin_problems,
        connector_dir=_manifest_only(connector),
    )

    assert report.status == "fail"
    assert any("cannot be confirmed" in problem for problem in report.problems)


@pytest.mark.parametrize(
    "api_url,result",
    [
        (None, "supported"),
        ("https://slack.com/api/", "supported"),
        ("https://slack.example.com/api/", "unsupported"),
    ],
)
def test_the_support_check_reads_hosts_from_the_case_config(
    tmp_path, connector_dir, api_url, result
):
    # The url_base reads `api_url`, which the spec defaults to the twin's host.
    manifest = connector_dir / "manifest.yaml"
    manifest.write_text(
        manifest.read_text()
        .replace(
            "url_base: https://slack.com/api/",
            "url_base: \"{{ config.get('api_url', 'https://slack.com/api/') }}\"",
            1,
        )
        .replace(
            "properties: {}",
            "properties:\n      api_url:\n        default: https://slack.com/api/",
        )
    )
    case = tmp_path / "case"
    shutil.copytree(CASE_FIXTURE, case)
    if api_url is not None:
        template = case / "config.template.json"
        template.write_text(
            json.dumps({**json.loads(template.read_text()), "api_url": api_url})
        )

    report = check_case(
        case,
        "source-slack",
        check_origin=_no_origin_problems,
        connector_dir=connector_dir,
    )

    assert report.support and report.support["result"] == result
    assert report.status == ("pass" if result == "supported" else "fail")


def test_an_unreadable_case_config_fails_the_gate(tmp_path, connector_dir):
    case = tmp_path / "case"
    shutil.copytree(CASE_FIXTURE, case)
    (case / "config.template.json").write_text("[]")

    report = check_case(
        case,
        "source-slack",
        check_origin=_no_origin_problems,
        connector_dir=connector_dir,
    )

    assert report.status == "fail"
    assert "config.template.json is not a JSON object" in report.problems
