"""Behavioral regression tests for labels on generated SpecKit pull requests."""

import json
import os
import shlex
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
CREATE_SPEC_PR = REPO_ROOT / ".github" / "scripts" / "speckit-trigger" / "create-spec-pr.sh"
PR_URL = "https://github.com/swai-factory/agentic-devtools/pull/123"


FAKE_GH = """gh() {
printf '%s\\n' "$*" >> "$FAKE_GH_CALL_LOG"

if [[ "$1" == "pr" && "$2" == "create" ]]; then
    if [[ "${FAKE_GH_PR_CREATE_ALREADY_EXISTS:-false}" == "true" ]]; then
        echo "a pull request already exists for this branch" >&2
        return 1
    fi
    while [[ $# -gt 0 ]]; do
        if [[ "$1" == "--body" ]]; then
            shift
            printf '%s' "$1" > "$FAKE_GH_PR_BODY"
            break
        fi
        shift
    done
    printf '%s\\n' "$FAKE_GH_PR_URL"
    return 0
fi

if [[ "$1" == "pr" && "$2" == "ready" ]]; then
    printf '%s' '{"draft":true,"labels":[{"name":"ai-auto-merge-allowed"}]}' > "$FAKE_GH_PR_STATE_FILE"
    return 0
fi

if [[ "$1" == "pr" && "$2" == "edit" ]]; then
    printf '%s' '{"draft":true,"labels":[]}' > "$FAKE_GH_PR_STATE_FILE"
    return 0
fi

if [[ "$1" == "label" && "$2" == "create" ]]; then
    if [[ "${FAKE_GH_CREATE_FAIL_LABEL:-}" == "$3" ]]; then
        echo "simulated label-create failure" >&2
        return 1
    fi
    return 0
fi

if [[ "$1" == "api" ]]; then
    endpoint=""
    method="GET"
    paginate=false
    while [[ $# -gt 0 ]]; do
        if [[ "$1" == "--paginate" ]]; then
            paginate=true
        fi
        if [[ "$1" == /repos/* ]]; then
            endpoint="$1"
        fi
        if [[ "$1" == "--method" ]]; then
            shift
            method="$1"
        fi
        shift
    done

    if [[ "$endpoint" == "/repos/swai-factory/agentic-devtools/labels" ]]; then
        if [[ "${GH_TOKEN:-}" != "${LABEL_TOKEN:-}" ]]; then
            echo "label preflight did not use LABEL_TOKEN" >&2
            return 1
        fi
        if [[ "${FAKE_GH_PREFLIGHT_FAIL_ONCE:-false}" == "true" ]]; then
            FAKE_GH_PREFLIGHT_FAIL_ONCE=false
            echo "simulated transient preflight failure" >&2
            return 1
        fi
        printf '[]\\n'
        return 0
    fi
    if [[ "$endpoint" == "/repos/swai-factory/agentic-devtools/issues/123/labels" ]]; then
        if [[ "$method" == "POST" && "${FAKE_GH_POST_FAIL:-false}" == "true" ]]; then
            echo "simulated REST label-write failure" >&2
            return 1
        fi
        if [[ "$method" == "POST" ]]; then
            return 0
        fi
        printf '%s\\n' "$FAKE_GH_PR_LABELS"
        if [[ "$paginate" == "true" && -n "${FAKE_GH_PR_LABELS_PAGE_2:-}" ]]; then
            printf '%s\\n' "$FAKE_GH_PR_LABELS_PAGE_2"
        fi
        return 0
    fi
fi

echo "Unexpected gh invocation: $*" >&2
return 2
}"""


@pytest.fixture
def fake_gh(tmp_path: Path) -> tuple[dict[str, str], Path, Path, Path]:
    script_dir = tmp_path / "scripts"
    (script_dir / "lib").mkdir(parents=True)
    script = script_dir / "create-spec-pr.sh"
    script.write_text(CREATE_SPEC_PR.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
    reader_script = CREATE_SPEC_PR.parent / "pr-read-session.py"
    (script_dir / reader_script.name).write_text(
        reader_script.read_text(encoding="utf-8"),
        encoding="utf-8",
        newline="\n",
    )
    retry_lib = CREATE_SPEC_PR.parent / "lib" / "retry.sh"
    (script_dir / "lib" / "retry.sh").write_text(
        retry_lib.read_text(encoding="utf-8"),
        encoding="utf-8",
        newline="\n",
    )

    output_file = script_dir / "github-output.txt"
    output_file.touch()
    call_log = script_dir / "gh-calls.txt"
    pool_init_log = script_dir / "pool-initializations.txt"
    body_file = script_dir / "pr-body.txt"
    python_stub = script_dir / "python-stubs" / "agentic_devtools"
    for package_dir in (python_stub, python_stub / "cli", python_stub / "cli" / "ci"):
        package_dir.mkdir(parents=True, exist_ok=True)
        (package_dir / "__init__.py").write_text("", encoding="utf-8")
    pr_state_file = script_dir / "pr-state.json"
    pr_state_file.write_text('{"draft":false,"labels":[]}', encoding="utf-8")
    (python_stub / "cli" / "ci" / "github_provider.py").write_text(
        "import os\n"
        "from pathlib import Path\n"
        "\n"
        "_pool_initialized = False\n"
        "\n"
        "def _gh_api(path, *, token=None, read_pool=True, **kwargs):\n"
        "    global _pool_initialized\n"
        "    if not _pool_initialized:\n"
        '        Path(os.environ["FAKE_POOL_INIT_LOG"]).open("a", encoding="utf-8").write("initialized\\n")\n'
        "        _pool_initialized = True\n"
        "    if path in {\n"
        '        "/repos/swai-factory/agentic-devtools/pulls/123",\n'
        '        "/repos/swai-factory/agentic-devtools/pulls/99",\n'
        "    }:\n"
        '        return Path(os.environ["FAKE_GH_PR_STATE_FILE"]).read_text(encoding="utf-8")\n'
        '    if path.startswith("/repos/swai-factory/agentic-devtools/pulls?"):\n'
        '        return \'[{"html_url":"https://github.com/swai-factory/agentic-devtools/pull/99","number":99}]\'\n'
        '    if path.startswith("/search/issues?") and "repo%3Aswai-factory%2Fagentic-devtools" in path:\n'
        '        return \'{"items":[{"html_url":"https://github.com/swai-factory/agentic-devtools/pull/99"}]}\'\n'
        "    raise AssertionError(f'Unexpected API request: {path}')\n",
        encoding="utf-8",
    )
    env = os.environ.copy()
    env.update(
        {
            "GITHUB_OUTPUT": output_file.name,
            "GITHUB_REPOSITORY": "swai-factory/agentic-devtools",
            "GH_TOKEN": "limited-repo-workflow-token",
            "GITHUB_TOKEN": "limited-repo-workflow-token",
            "LABEL_TOKEN": "label-write-token",
            "HIERARCHY_LEVEL": "feature",
            "FAKE_GH_CALL_LOG": call_log.name,
            "FAKE_POOL_INIT_LOG": pool_init_log.name,
            "FAKE_GH_PR_BODY": body_file.name,
            "FAKE_GH_PR_STATE_FILE": pr_state_file.name,
            "FAKE_GH_PR_URL": PR_URL,
            "FAKE_GH_PR_CREATE_ALREADY_EXISTS": "false",
            "FAKE_GH_PR_LABELS": "speckit:phase-1\nspeckit:level-feature",
            "FAKE_GH_CREATE_FAIL_LABEL": "",
            "PYTHONPATH": str(script_dir / "python-stubs"),
        }
    )
    return env, output_file, call_log, script


def _run_create_spec_pr(
    tmp_path: Path,
    env: dict[str, str],
    script: Path,
    *,
    phase: bool = True,
    phase_number: int = 1,
    enforce_draft_state: bool = False,
) -> subprocess.CompletedProcess[str]:
    spec_dir = script.parent / "spec"
    spec_dir.mkdir(exist_ok=True)
    args = [
        "bash",
        "./create-spec-pr.sh",
        "speckit/42/phase-1",
        "./spec",
        "42",
        "Example issue",
    ]
    if phase:
        phase_names = {1: "specify", 2: "clarify", 3: "plan"}
        args.extend(["--phase-number", str(phase_number), "--phase-name", phase_names[phase_number]])
    if enforce_draft_state:
        args.append("--enforce-draft-state")
    runtime_variables = (
        "GITHUB_OUTPUT",
        "GITHUB_REPOSITORY",
        "GH_TOKEN",
        "GITHUB_TOKEN",
        "LABEL_TOKEN",
        "HIERARCHY_LEVEL",
        "FAKE_GH_CALL_LOG",
        "FAKE_POOL_INIT_LOG",
        "FAKE_GH_PR_BODY",
        "FAKE_GH_PR_STATE_FILE",
        "FAKE_GH_PR_URL",
        "FAKE_GH_PR_CREATE_ALREADY_EXISTS",
        "FAKE_GH_PR_LABELS",
        "FAKE_GH_PR_LABELS_PAGE_2",
        "FAKE_GH_CREATE_FAIL_LABEL",
        "FAKE_GH_PREFLIGHT_FAIL_ONCE",
        "FAKE_GH_POST_FAIL",
        "ENFORCE_DRAFT_STATE",
        "PYTHONPATH",
    )
    wrapper = script.parent / "run-create-spec-pr.sh"
    exports = "\n".join(f"export {name}={shlex.quote(env.get(name, ''))}" for name in runtime_variables)
    labels_json = shlex.quote(env.get("LABELS_JSON", "[]"))
    wrapper.write_text(
        f"#!/usr/bin/env bash\nset -euo pipefail\n{exports}\n{FAKE_GH}\nsleep() {{ :; }}\n"
        f"labels_json={labels_json}\n"
        'source ./create-spec-pr.sh "$1" "$2" "$3" "$4" "$labels_json" "${@:5}"\n',
        encoding="utf-8",
        newline="\n",
    )
    bash = shutil.which("bash")
    assert bash is not None, "Git Bash or Bash must be installed to exercise the PR creation script"
    return subprocess.run(
        [bash, "./run-create-spec-pr.sh", *args[2:]],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=os.environ.copy(),
        cwd=script.parent,
        shell=False,
    )  # noqa: S603


def test_phase_pr_uses_rest_labels_and_verifies_required_labels(
    tmp_path: Path, fake_gh: tuple[dict[str, str], Path, Path, Path]
) -> None:
    env, output_file, call_log, script = fake_gh

    result = _run_create_spec_pr(tmp_path, env, script)

    assert result.returncode == 0, result.stderr
    calls = call_log.read_text(encoding="utf-8")
    assert (
        "api --method POST /repos/swai-factory/agentic-devtools/issues/123/labels "
        "--raw-field labels[]=speckit:phase-1 --raw-field labels[]=speckit:level-feature"
    ) in calls
    assert "pr edit" not in calls
    assert output_file.read_text(encoding="utf-8").splitlines() == [
        f"pr_url={PR_URL}",
        "pr_number=123",
        "routing_labels_verified=true",
    ]
    assert "=== Pull Request Created ===" in result.stdout

    pr_body = (script.parent / "pr-body.txt").read_text(encoding="utf-8")
    assert "Confirm `speckit:phase-1` and `speckit:level-feature` are present before merging" in pr_body


def test_phase_two_previous_pr_lookup_uses_repository_environment(
    tmp_path: Path, fake_gh: tuple[dict[str, str], Path, Path, Path]
) -> None:
    env, _output_file, _call_log, script = fake_gh
    env["FAKE_GH_PR_LABELS"] = "speckit:phase-2\nspeckit:level-feature"

    result = _run_create_spec_pr(tmp_path, env, script, phase_number=2)

    assert result.returncode == 0, result.stderr
    pr_body = (script.parent / "pr-body.txt").read_text(encoding="utf-8")
    assert "https://github.com/swai-factory/agentic-devtools/pull/99" in pr_body
    assert (script.parent / env["FAKE_POOL_INIT_LOG"]).read_text(encoding="utf-8").splitlines() == ["initialized"]


def test_draft_enforcement_preserves_rest_label_objects(
    tmp_path: Path, fake_gh: tuple[dict[str, str], Path, Path, Path]
) -> None:
    env, _output_file, call_log, script = fake_gh
    Path(script.parent / env["FAKE_GH_PR_STATE_FILE"]).write_text(
        '{"draft":false,"labels":[{"name":"ai-auto-merge-allowed"}]}',
        encoding="utf-8",
    )

    result = _run_create_spec_pr(tmp_path, env, script, phase=False, enforce_draft_state=True)

    assert result.returncode == 0, result.stderr
    calls = call_log.read_text(encoding="utf-8")
    assert "pr ready 123 --undo" in calls
    assert "pr edit 123 --repo swai-factory/agentic-devtools --remove-label ai-auto-merge-allowed" in calls
    assert (script.parent / env["FAKE_POOL_INIT_LOG"]).read_text(encoding="utf-8").splitlines() == ["initialized"]


def test_recovered_pr_lookup_and_draft_readbacks_share_one_pool_process(
    tmp_path: Path, fake_gh: tuple[dict[str, str], Path, Path, Path]
) -> None:
    env, output_file, _call_log, script = fake_gh
    env["FAKE_GH_PR_CREATE_ALREADY_EXISTS"] = "true"
    Path(script.parent / env["FAKE_GH_PR_STATE_FILE"]).write_text(
        '{"draft":true,"labels":[]}',
        encoding="utf-8",
    )

    result = _run_create_spec_pr(tmp_path, env, script, phase=False, enforce_draft_state=True)

    assert result.returncode == 0, result.stderr
    assert output_file.read_text(encoding="utf-8").splitlines()[:2] == [
        "pr_url=https://github.com/swai-factory/agentic-devtools/pull/99",
        "pr_number=99",
    ]
    assert (script.parent / env["FAKE_POOL_INIT_LOG"]).read_text(encoding="utf-8").splitlines() == ["initialized"]


def test_phase_pr_retries_transient_label_preflight_failure(
    tmp_path: Path, fake_gh: tuple[dict[str, str], Path, Path, Path]
) -> None:
    env, output_file, call_log, script = fake_gh
    env["FAKE_GH_PREFLIGHT_FAIL_ONCE"] = "true"

    result = _run_create_spec_pr(tmp_path, env, script)

    assert result.returncode == 0, result.stderr
    calls = call_log.read_text(encoding="utf-8").splitlines()
    preflight_calls = [call for call in calls if call.startswith("api /repos/swai-factory/agentic-devtools/labels ")]
    assert len(preflight_calls) == 2
    assert "routing_labels_verified=true" in output_file.read_text(encoding="utf-8")


def test_phase_pr_fails_when_required_label_verification_is_incomplete(
    tmp_path: Path, fake_gh: tuple[dict[str, str], Path, Path, Path]
) -> None:
    env, output_file, call_log, script = fake_gh
    env["FAKE_GH_PR_LABELS"] = "speckit:phase-1"

    result = _run_create_spec_pr(tmp_path, env, script)

    assert result.returncode != 0
    assert "Required label is missing from PR #123: speckit:level-feature" in result.stderr
    assert output_file.read_text(encoding="utf-8").splitlines() == [
        f"pr_url={PR_URL}",
        "pr_number=123",
        "label_setup_status=failed",
        "routing_labels_verified=false",
    ]
    assert "=== Pull Request Created ===" not in result.stdout
    assert call_log.read_text(encoding="utf-8").count("--method POST") == 3


def test_phase_pr_verifies_required_labels_on_second_page(
    tmp_path: Path, fake_gh: tuple[dict[str, str], Path, Path, Path]
) -> None:
    env, output_file, call_log, script = fake_gh
    env["FAKE_GH_PR_LABELS"] = "\n".join(["speckit:phase-1", *(f"extra-label-{i}" for i in range(29))])
    env["FAKE_GH_PR_LABELS_PAGE_2"] = "speckit:level-feature"

    result = _run_create_spec_pr(tmp_path, env, script)

    assert result.returncode == 0, result.stderr
    assert output_file.read_text(encoding="utf-8").splitlines() == [
        f"pr_url={PR_URL}",
        "pr_number=123",
        "routing_labels_verified=true",
    ]
    assert call_log.read_text(encoding="utf-8").count("--method POST") == 1


def test_phase_pr_reports_rest_retry_exhaustion_with_recovery_identifiers(
    tmp_path: Path, fake_gh: tuple[dict[str, str], Path, Path, Path]
) -> None:
    env, output_file, call_log, script = fake_gh
    env["FAKE_GH_POST_FAIL"] = "true"

    result = _run_create_spec_pr(tmp_path, env, script)

    assert result.returncode != 0
    assert "Routing-label setup failed for the already-created PR #123" in result.stderr
    assert PR_URL in result.stderr
    assert "Recovery: create any missing required labels, then apply and verify them before merging." in result.stderr
    assert output_file.read_text(encoding="utf-8").splitlines() == [
        f"pr_url={PR_URL}",
        "pr_number=123",
        "label_setup_status=failed",
        "routing_labels_verified=false",
    ]
    assert "=== Pull Request Created ===" not in result.stdout
    assert call_log.read_text(encoding="utf-8").count("--method POST") == 3


def test_phase_pr_fails_when_required_label_creation_is_exhausted(
    tmp_path: Path, fake_gh: tuple[dict[str, str], Path, Path, Path]
) -> None:
    env, output_file, call_log, script = fake_gh
    env["FAKE_GH_CREATE_FAIL_LABEL"] = "speckit:level-feature"

    result = _run_create_spec_pr(tmp_path, env, script)

    assert result.returncode != 0
    assert "Could not create required label(s): speckit:level-feature" in result.stderr
    assert 'gh label create "speckit:level-feature"' in result.stderr
    assert output_file.read_text(encoding="utf-8").splitlines() == [
        f"pr_url={PR_URL}",
        "pr_number=123",
        "label_setup_status=failed",
        "routing_labels_verified=false",
    ]
    assert "=== Pull Request Created ===" not in result.stdout
    assert call_log.read_text(encoding="utf-8").count("label create speckit:level-feature") == 3


def test_non_phase_pr_keeps_generic_speckit_spec_label(
    tmp_path: Path, fake_gh: tuple[dict[str, str], Path, Path, Path]
) -> None:
    env, output_file, call_log, script = fake_gh
    env["HIERARCHY_LEVEL"] = ""
    env["FAKE_GH_PR_LABELS"] = "speckit:spec"

    result = _run_create_spec_pr(tmp_path, env, script, phase=False)

    assert result.returncode == 0, result.stderr
    calls = call_log.read_text(encoding="utf-8")
    assert "--raw-field labels[]=speckit:spec" in calls
    assert output_file.read_text(encoding="utf-8").splitlines() == [f"pr_url={PR_URL}", "pr_number=123"]


@pytest.mark.parametrize("label", ["123", "true", "null", "@private-label.txt"])
def test_inherited_labels_are_posted_as_literal_strings(
    tmp_path: Path,
    fake_gh: tuple[dict[str, str], Path, Path, Path],
    label: str,
) -> None:
    env, output_file, call_log, script = fake_gh
    env["LABELS_JSON"] = json.dumps([label])
    (script.parent / "private-label.txt").write_text("not-a-label", encoding="utf-8")

    result = _run_create_spec_pr(tmp_path, env, script)

    assert result.returncode == 0, result.stderr
    calls = call_log.read_text(encoding="utf-8")
    assert f"--raw-field labels[]={label}" in calls, result.stdout + result.stderr
    assert "--field labels[]=" not in calls
    assert "routing_labels_verified=true" in output_file.read_text(encoding="utf-8")
