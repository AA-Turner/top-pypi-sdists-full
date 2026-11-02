import json
import subprocess
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci import windows_specific_cli
from agentic_devtools.cli.ci.windows_process_tree import ProcessCleanupDiagnostic, ProcessCleanupError


def _selection(groups=("setup-check",), **overrides):
    selection = {
        "ok": True,
        "product_groups": list(groups),
        "contract_required": False,
        "windows_required": bool(groups),
        "bootstrap_allowed": False,
    }
    selection.update(overrides)
    return selection


def _select_args(paths="[]", bootstrap=False):
    args = ["select", "--changed-paths-json", paths, "--manifest", "manifest.json", "--head-policy", "head.py"]
    return args + ["--bootstrap"] if bootstrap else args


def _run_args(selection=None):
    return [
        "run",
        "--selection-json",
        selection if selection is not None else json.dumps(_selection()),
        "--manifest",
        "manifest.json",
        "--head-policy",
        "head.py",
        "--root",
        "r",
        "--junit",
        "j",
    ]


def _invoke(
    monkeypatch,
    argv,
    *,
    env_path="trusted-policy.py",
    select_groups=None,
    load_policy=None,
    run_selected_tests=None,
    evaluate_gate=None,
):
    if env_path is None:
        monkeypatch.delenv("WINDOWS_CI_BASE_POLICY", raising=False)
    else:
        monkeypatch.setenv("WINDOWS_CI_BASE_POLICY", env_path)
    select_groups = select_groups or Mock(return_value=(frozenset(), True))
    load_policy = load_policy or Mock(return_value=object())
    run_selected_tests = run_selected_tests or Mock(
        return_value={"ok": True, "collected_ids": ["z"], "executed_ids": ["z"], "skipped": 0}
    )
    evaluate_gate = evaluate_gate or Mock(return_value={"ok": True, "classification": "not-applicable"})
    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        try:
            status = windows_specific_cli._Dispatcher(
                load_policy,
                select_groups,
                run_selected_tests,
                evaluate_gate,
            ).run(argv)
        except SystemExit as exc:
            status = exc.code
    return status, stdout.getvalue(), stderr.getvalue()


def _payload(stdout):
    lines = stdout.splitlines()
    assert len(lines) == 1
    return json.loads(lines[0])


@pytest.mark.parametrize(
    "argv",
    [
        [],
        ["unknown"],
        ["select"],
        ["gate", "--selection-json", "{}", "--unknown"],
    ],
)
def test_parser_errors_emit_one_json_object_to_stdout(monkeypatch, argv):
    status, stdout, stderr = _invoke(monkeypatch, argv)
    assert status == 2
    assert _payload(stdout) == {"ok": False, "error_code": "invalid_arguments"}
    assert "usage:" in stderr


def test_select_parses_paths_before_classification_and_policy(monkeypatch):
    calls = []
    groups = frozenset({"setup-check", "benchmark"})
    selector = Mock(side_effect=lambda paths: calls.append(("select", paths)) or (groups, True))
    loader = Mock(side_effect=lambda *args, **kwargs: calls.append(("load", args, kwargs)) or object())

    status, stdout, stderr = _invoke(
        monkeypatch, _select_args('["tests/a.py"]'), select_groups=selector, load_policy=loader
    )

    assert status == 0
    assert stderr == ""
    assert _payload(stdout) == {
        "ok": True,
        "product_groups": ["setup-check", "benchmark"],
        "contract_required": True,
        "windows_required": True,
        "bootstrap_allowed": False,
    }
    assert calls[0] == ("select", ["tests/a.py"])
    assert calls[1][0] == "load"
    assert calls[1][1] == ("manifest.json", "trusted-policy.py", "head.py")
    assert calls[1][2] == {"applicable_groups": groups, "bootstrap": False}


@pytest.mark.parametrize("raw", ["{", "{}", '["valid", 3]', "null"])
def test_select_rejects_malformed_path_json_without_policy_call(monkeypatch, raw):
    selector, loader = Mock(), Mock()
    status, stdout, _ = _invoke(monkeypatch, _select_args(raw), select_groups=selector, load_policy=loader)
    assert status != 0
    assert _payload(stdout) == {"ok": False, "error_code": "changed_paths_failed"}
    selector.assert_not_called()
    loader.assert_not_called()


def test_select_maps_path_validation_error(monkeypatch):
    selector = Mock(side_effect=ValueError("bad changed path"))
    loader = Mock()
    status, stdout, stderr = _invoke(
        monkeypatch, _select_args('["../bad"]'), select_groups=selector, load_policy=loader
    )
    assert status != 0
    assert _payload(stdout) == {"ok": False, "error_code": "changed_paths_failed"}
    assert "bad changed path" in stderr
    loader.assert_not_called()


def test_select_unset_policy_is_reported_after_path_classification(monkeypatch):
    calls = []
    selector = Mock(side_effect=lambda paths: calls.append("select") or (frozenset(), False))
    loader = Mock()
    status, stdout, _ = _invoke(monkeypatch, _select_args(), env_path="", select_groups=selector, load_policy=loader)
    assert status != 0
    assert _payload(stdout) == {"ok": False, "error_code": "base_policy_unset"}
    assert calls == ["select"]
    loader.assert_not_called()


@pytest.mark.parametrize(
    ("filename", "code"),
    [
        ("trusted-policy.py", "base_policy_missing"),
        ("manifest.json", "manifest_missing"),
        ("head.py", "head_policy_missing"),
        ("elsewhere", "policy_io_failed"),
        (None, "policy_io_failed"),
    ],
)
def test_select_maps_normal_policy_file_errors(monkeypatch, filename, code):
    exception = FileNotFoundError("missing") if filename is None else FileNotFoundError(2, "missing", filename)
    loader = Mock(side_effect=exception)
    status, stdout, stderr = _invoke(monkeypatch, _select_args(), load_policy=loader)
    assert status != 0
    assert _payload(stdout) == {"ok": False, "error_code": code}
    assert "missing" in stderr
    loader.assert_called_once()
    assert loader.call_args.kwargs["bootstrap"] is False


def test_select_maps_policy_validation_and_io_errors(monkeypatch):
    for exception, code in [(ValueError("invalid"), "policy_invalid"), (OSError("unreadable"), "policy_io_failed")]:
        loader = Mock(side_effect=exception)
        status, stdout, _ = _invoke(monkeypatch, _select_args(), load_policy=loader)
        assert status != 0
        assert _payload(stdout) == {"ok": False, "error_code": code}


def test_select_existing_policy_rejects_bootstrap(monkeypatch):
    loader = Mock(return_value=object())
    status, stdout, _ = _invoke(monkeypatch, _select_args(bootstrap=True), load_policy=loader)
    assert status != 0
    assert _payload(stdout) == {"ok": False, "error_code": "bootstrap_not_allowed"}
    loader.assert_called_once_with(
        "manifest.json", "trusted-policy.py", "head.py", applicable_groups=frozenset(), bootstrap=False
    )


def test_select_bootstrap_with_product_groups_does_not_retry(monkeypatch):
    loader = Mock(side_effect=FileNotFoundError(2, "missing", "trusted-policy.py"))
    selector = Mock(return_value=(frozenset({"setup-check"}), False))
    status, stdout, _ = _invoke(
        monkeypatch,
        _select_args(bootstrap=True),
        select_groups=selector,
        load_policy=loader,
    )
    assert status != 0
    assert _payload(stdout) == {"ok": False, "error_code": "base_policy_missing"}
    loader.assert_called_once()


def test_select_bootstrap_retry_reports_only_accepted_retry(monkeypatch):
    loader = Mock(
        side_effect=[
            FileNotFoundError(2, "missing", "trusted-policy.py"),
            object(),
        ]
    )
    status, stdout, _ = _invoke(
        monkeypatch,
        _select_args(bootstrap=True),
        load_policy=loader,
    )
    assert status == 0
    assert _payload(stdout)["bootstrap_allowed"] is True
    assert loader.call_count == 2
    assert loader.call_args_list[1].kwargs["bootstrap"] is True


@pytest.mark.parametrize(
    ("exception", "code"),
    [
        (ValueError("seed mismatch"), "bootstrap_not_allowed"),
        (FileNotFoundError(2, "missing", "manifest.json"), "manifest_missing"),
        (FileNotFoundError(2, "missing", "head.py"), "head_policy_missing"),
        (OSError("disk error"), "policy_io_failed"),
    ],
)
def test_select_bootstrap_retry_maps_failure(monkeypatch, exception, code):
    loader = Mock(side_effect=[FileNotFoundError(2, "missing", "trusted-policy.py"), exception])
    status, stdout, _ = _invoke(
        monkeypatch,
        _select_args(bootstrap=True),
        load_policy=loader,
    )
    assert status != 0
    assert _payload(stdout) == {"ok": False, "error_code": code}
    assert loader.call_count == 2


@pytest.mark.parametrize(
    "selection",
    [
        '{"ok":true,"ok":true,"product_groups":["setup-check"],"contract_required":false,"windows_required":true,"bootstrap_allowed":false}',
        '{"ok":false,"error_code":"changed_paths_failed"}',
        '{"ok":true,"product_groups":["unknown"],"contract_required":false,"windows_required":true,"bootstrap_allowed":false}',
        '{"ok":true,"product_groups":null,"contract_required":false,"windows_required":false,"bootstrap_allowed":false}',
        '{"ok":true,"product_groups":["portability","setup-check"],"contract_required":false,"windows_required":true,"bootstrap_allowed":false}',
        '{"ok":true,"product_groups":["setup-check","setup-check"],"contract_required":false,"windows_required":true,"bootstrap_allowed":false}',
        '{"ok":true,"product_groups":["setup-check"],"contract_required":false,"windows_required":false,"bootstrap_allowed":false}',
        '{"ok":true,"product_groups":["setup-check"],"contract_required":false,"windows_required":true,"bootstrap_allowed":true}',
        '{"ok":true,"product_groups":["setup-check"],"contract_required":"false","windows_required":true,"bootstrap_allowed":false}',
        '{"ok":true,"product_groups":[],"contract_required":false,"windows_required":false,"bootstrap_allowed":false,"extra":true}',
    ],
)
def test_run_rejects_invalid_selection_before_policy_or_tests(monkeypatch, selection):
    loader, runner = Mock(), Mock()
    status, stdout, _ = _invoke(monkeypatch, _run_args(selection), load_policy=loader, run_selected_tests=runner)
    assert status != 0
    assert _payload(stdout) == {"ok": False, "error_code": "selection_failed"}
    loader.assert_not_called()
    runner.assert_not_called()


def test_run_empty_groups_precedes_policy_environment_and_subprocess(monkeypatch):
    loader, runner = Mock(), Mock()
    status, stdout, _ = _invoke(
        monkeypatch,
        _run_args(json.dumps(_selection(groups=()))),
        env_path=None,
        load_policy=loader,
        run_selected_tests=runner,
    )
    assert status != 0
    assert _payload(stdout) == {"ok": False, "error_code": "no_product_groups"}
    loader.assert_not_called()
    runner.assert_not_called()


def test_run_reports_unset_policy_before_loading_or_testing(monkeypatch):
    loader, runner = Mock(), Mock()
    status, stdout, _ = _invoke(monkeypatch, _run_args(), env_path=None, load_policy=loader, run_selected_tests=runner)
    assert status != 0
    assert _payload(stdout) == {"ok": False, "error_code": "base_policy_unset"}
    loader.assert_not_called()
    runner.assert_not_called()


def test_run_success_uses_trusted_policy_and_selected_groups(monkeypatch):
    groups = ["setup-check", "benchmark"]
    expected_policy = object()
    loader = Mock(return_value=expected_policy)
    result = {"ok": True, "collected_ids": ["b", "a"], "executed_ids": ["b", "a"], "skipped": 0}
    runner = Mock(return_value=result)
    selection = _selection(groups=groups, contract_required=True)
    status, stdout, stderr = _invoke(
        monkeypatch,
        _run_args(json.dumps(selection)),
        load_policy=loader,
        run_selected_tests=runner,
    )
    assert status == 0
    assert stderr == ""
    assert _payload(stdout) == {"ok": True, "collected_ids": ["b", "a"], "executed_ids": ["b", "a"], "skipped": 0}
    loader.assert_called_once_with(
        "manifest.json", "trusted-policy.py", "head.py", applicable_groups=groups, bootstrap=False
    )
    runner.assert_called_once_with("r", expected_policy, groups, junit_path="j")


@pytest.mark.parametrize(
    ("exception", "code"),
    [
        (FileNotFoundError(2, "missing", "trusted-policy.py"), "base_policy_missing"),
        (FileNotFoundError(2, "missing", "manifest.json"), "manifest_missing"),
        (FileNotFoundError(2, "missing", "head.py"), "head_policy_missing"),
        (ValueError("invalid"), "policy_invalid"),
        (OSError("unreadable"), "policy_io_failed"),
    ],
)
def test_run_maps_policy_errors(monkeypatch, exception, code):
    loader, runner = Mock(side_effect=exception), Mock()
    status, stdout, _ = _invoke(
        monkeypatch,
        _run_args(),
        load_policy=loader,
        run_selected_tests=runner,
    )
    assert status != 0
    assert _payload(stdout) == {"ok": False, "error_code": code}
    runner.assert_not_called()


@pytest.mark.parametrize(
    "error",
    [
        subprocess.CalledProcessError(7, ["pytest"], output="collected", stderr="failed"),
        subprocess.CalledProcessError(9, ["pytest"], output="", stderr=""),
        subprocess.TimeoutExpired(["pytest"], 600, output="partial stdout", stderr="partial stderr"),
        subprocess.TimeoutExpired(["pytest"], 600),
        ProcessCleanupError(
            subprocess.CompletedProcess([], 0, "out", "err"), (ProcessCleanupDiagnostic("close", "failed"),)
        ),
        ValueError("invalid input"),
        OSError("read failed"),
    ],
)
def test_run_maps_test_errors_with_evidence(monkeypatch, error):
    if isinstance(error, (subprocess.TimeoutExpired, subprocess.CalledProcessError, OSError)):
        error.cleanup_errors = (ProcessCleanupDiagnostic("cleanup", "cleanup failed"),)
    if isinstance(error, OSError):
        error.output = error.stderr = "recovered output"
    if isinstance(error, ProcessCleanupError):
        setattr(error, "output", error.completed_process.stdout)
        setattr(error, "stderr", error.completed_process.stderr)
    status, stdout, stderr = _invoke(monkeypatch, _run_args(), run_selected_tests=Mock(side_effect=error))
    failure_code = {OSError: "test_io_failed", ValueError: "test_validation_failed"}.get(
        type(error), "test_process_failed"
    )
    assert status == getattr(error, "returncode", 1) and _payload(stdout) == {
        "ok": False,
        "error_code": failure_code,
    }
    output = (getattr(error, "output", None), getattr(error, "stderr", None))
    details = (*output, *(f"{item.stage}: {item.message}" for item in getattr(error, "cleanup_errors", ())))
    assert all(detail in stderr for detail in details if detail)
    assert ("stdout:" in stderr, "stderr:" in stderr) == tuple(map(bool, output))


@pytest.mark.parametrize("outcome", ["not-applicable", "native-evidence"])
def test_gate_delegates_decoded_inputs_without_reading_policy(monkeypatch, outcome):
    selection = _selection(groups=() if outcome == "not-applicable" else ("setup-check",))
    evaluator = Mock(return_value={"ok": True, "classification": outcome})
    loader = Mock()
    status, stdout, stderr = _invoke(
        monkeypatch,
        ["gate", "--selection-json", json.dumps(selection), "--linux-result", "success", "--windows-result", "success"],
        env_path=None,
        load_policy=loader,
        evaluate_gate=evaluator,
    )
    assert status == 0
    assert stderr == ""
    assert _payload(stdout) == {"ok": True, "classification": outcome}
    evaluator.assert_called_once_with(selection, "success", "success")
    loader.assert_not_called()


@pytest.mark.parametrize(
    ("selection", "linux", "windows", "expected"),
    [
        ({"ok": False, "error_code": "changed_paths_failed"}, None, None, "changed_paths_failed"),
        (_selection(groups=("setup-check",)), None, "success", "required_evidence_missing"),
        (_selection(groups=(), contract_required=True), "skipped", None, "required_evidence_missing"),
    ],
)
def test_gate_preserves_errors_and_required_evidence(monkeypatch, selection, linux, windows, expected):
    evaluator = Mock(return_value={"ok": False, "error_code": expected})
    argv = ["gate", "--selection-json", json.dumps(selection)]
    if linux is not None:
        argv += ["--linux-result", linux]
    if windows is not None:
        argv += ["--windows-result", windows]
    status, stdout, _ = _invoke(monkeypatch, argv, evaluate_gate=evaluator)
    assert status != 0
    assert _payload(stdout) == {"ok": False, "error_code": expected}


def test_gate_maps_malformed_json_without_calling_evaluator(monkeypatch):
    evaluator = Mock()
    status, stdout, _ = _invoke(
        monkeypatch,
        ["gate", "--selection-json", "{"],
        evaluate_gate=evaluator,
    )
    assert status != 0
    assert _payload(stdout) == {"ok": False, "error_code": "selection_failed"}
    evaluator.assert_not_called()


def test_gate_passes_unknown_job_value_to_gate(monkeypatch):
    selection = {"ok": False, "error_code": "changed_paths_failed"}
    evaluator = Mock(return_value={"ok": False, "error_code": "selection_failed"})
    status, stdout, _ = _invoke(
        monkeypatch,
        ["gate", "--selection-json", json.dumps(selection), "--linux-result", "mystery"],
        evaluate_gate=evaluator,
    )
    assert status != 0
    assert _payload(stdout) == {"ok": False, "error_code": "selection_failed"}
    evaluator.assert_called_once_with(selection, "mystery", None)


def test_verify_fixtures_passes_commit_and_path(monkeypatch):
    verifier = Mock(return_value=4)
    monkeypatch.setattr(windows_specific_cli, "verify_fixture_bytes", verifier)
    status, stdout, stderr = _invoke(monkeypatch, ["verify-fixtures", "--commit", "abc123", "--root", "fixture-root"])
    assert status == 0
    assert stderr == ""
    assert _payload(stdout) == {"ok": True, "files_checked": 4}
    verifier.assert_called_once_with("abc123", Path("fixture-root"))


@pytest.mark.parametrize(
    "exception",
    [
        ValueError("bad fixture"),
        FileNotFoundError(2, "missing"),
        NotADirectoryError(20, "not a directory"),
        subprocess.CalledProcessError(2, ["git"], stderr="bad tree"),
        subprocess.CalledProcessError(2, ["git"], output=b"git out", stderr=b"git err"),
        OSError("filesystem failure"),
    ],
)
def test_verify_fixtures_maps_documented_failures(monkeypatch, exception):
    verifier = Mock(side_effect=exception)
    monkeypatch.setattr(windows_specific_cli, "verify_fixture_bytes", verifier)
    status, stdout, stderr = _invoke(monkeypatch, ["verify-fixtures", "--commit", "abc123", "--root", "root"])
    assert status != 0
    assert _payload(stdout) == {"ok": False, "error_code": "fixture_audit_failed"}
    assert stderr and (not getattr(exception, "stdout", None) or "git out" in stderr and "git err" in stderr)


def test_verify_fixtures_propagates_unexpected_exceptions(monkeypatch):
    verifier = Mock(side_effect=RuntimeError("unexpected"))
    monkeypatch.setattr(windows_specific_cli, "verify_fixture_bytes", verifier)
    with pytest.raises(RuntimeError, match="unexpected"):
        _invoke(monkeypatch, ["verify-fixtures", "--commit", "abc123", "--root", "root"])


def test_help_is_the_only_text_stdout_exception(monkeypatch):
    status, stdout, stderr = _invoke(monkeypatch, ["--help"])
    assert status == 0
    assert "usage:" in stdout
    assert stderr == ""


def test_callable_protocol_declarations_are_executable():
    declarations = (
        ("_LoadPolicy", ("m", "b", "h"), {"applicable_groups": (), "bootstrap": False}),
        ("_SelectGroups", ([],), {}),
        ("_RunSelectedTests", ("r", object(), ()), {"junit_path": "j"}),
        ("_EvaluateGate", ({}, None, None), {}),
    )
    for name, args, kwargs in declarations:
        call = getattr(windows_specific_cli, name).__dict__["__call__"]
        assert call(object(), *args, **kwargs) is None
