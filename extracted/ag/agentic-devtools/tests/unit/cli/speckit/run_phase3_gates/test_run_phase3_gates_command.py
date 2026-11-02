"""Tests for the hierarchy-aware Phase 3 gate CLI."""

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from agentic_devtools.cli.speckit import run_phase3_gates


def _write_inputs(spec_dir: Path, *, hierarchy: str) -> Path:
    spec_dir.mkdir(parents=True)
    if hierarchy == "feature":
        (spec_dir / "spec.md").write_text("# Spec\nFR-001\n", encoding="utf-8")
        (spec_dir / "tasks.md").write_text("- [ ] [T001] [US1] Implement FR-001\n", encoding="utf-8")
    elif hierarchy == "task":
        (spec_dir / "tasks.md").write_text("- [ ] [T001] [US1] Implement FR-001\n", encoding="utf-8")
    if hierarchy != "task":
        (spec_dir / "plan.md").write_text("# Plan\n", encoding="utf-8")
    return spec_dir


def _gate(payload: object, exit_code: int = 0, calls: list | None = None, name: str = ""):
    def command(argv: list[str]) -> None:
        if calls is not None:
            calls.append((name, argv))
        print(json.dumps(payload))
        raise SystemExit(exit_code)

    return command


def _install_gates(
    monkeypatch,
    *,
    calls: list | None = None,
    overrides: dict | None = None,
    exit_codes: dict | None = None,
) -> None:
    outputs = {
        "fr": {"covered": ["FR-001"], "uncovered": [], "total": 1},
        "coverage": {
            "findings": [],
            "coverage": {"FR-001": {"is_covered": True}},
            "summary_table": "| FR | Result |\n|---|---|\n| FR-001 | Covered |",
            "summary": {"total_frs": 1, "covered_frs": 1, "uncovered_frs": 0, "total_findings": 0},
        },
        "artifacts": {"passed": True, "violations": [], "checks_run": []},
        "cross_ref": {"findings": [], "summary": {}},
    }
    outputs.update(overrides or {})
    functions = (
        ("validate_frs_command", "fr", 0),
        ("test_coverage_command", "coverage", 0),
        ("verify_artifacts_command", "artifacts", 0),
        ("cross_ref_command", "cross_ref", 0),
    )
    for function_name, output_name, code in functions:
        monkeypatch.setattr(
            run_phase3_gates,
            function_name,
            _gate(outputs[output_name], (exit_codes or {}).get(output_name, code), calls, output_name),
        )


def _prepare_feature(
    tmp_path: Path,
    monkeypatch,
    *,
    overrides: dict | None = None,
    exit_codes: dict | None = None,
) -> Path:
    spec_dir = _write_inputs(tmp_path / "feature", hierarchy="feature")
    _install_gates(monkeypatch, overrides=overrides, exit_codes=exit_codes)
    monkeypatch.setattr(run_phase3_gates, "get_repo_root", lambda: tmp_path)
    return spec_dir


class TestRunPhase3GatesHierarchy:
    """Each hierarchy invokes only its required validators and path set."""

    def test_feature_runs_all_gates_and_persists_stdout_result(self, tmp_path: Path, monkeypatch, capsys) -> None:
        spec_dir = _write_inputs(tmp_path / "feature", hierarchy="feature")
        calls: list = []
        _install_gates(monkeypatch, calls=calls)
        monkeypatch.setattr(run_phase3_gates, "get_repo_root", lambda: tmp_path)

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(
                ["--hierarchy-level", "feature", "--spec-dir", str(spec_dir), "--json"]
            )

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert captured.out, captured.err
        result = json.loads(captured.out)
        saved = json.loads((spec_dir / "generated" / "phase3-gates.json").read_text(encoding="utf-8"))
        assert result == saved
        assert result["status"] == "passed"
        assert [call[0] for call in calls] == ["fr", "coverage", "artifacts", "cross_ref", "artifacts"]
        artifact_args = calls[2][1]
        assert artifact_args[artifact_args.index("--phase") + 1] == "3"
        assert "--phase" not in calls[4][1]
        assert "## Coverage Summary" in (spec_dir / "generated" / "analysis-report.md").read_text(encoding="utf-8")
        assert "## E.2 Test Coverage" in (spec_dir / "generated" / "analysis-report.md").read_text(encoding="utf-8")

    def test_epic_skips_fr_and_test_coverage(self, tmp_path: Path, monkeypatch, capsys) -> None:
        spec_dir = _write_inputs(tmp_path / "epic", hierarchy="epic")
        calls: list = []
        _install_gates(monkeypatch, calls=calls)
        monkeypatch.setattr(run_phase3_gates, "get_repo_root", lambda: tmp_path)

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(
                ["--hierarchy-level", "epic", "--spec-dir", str(spec_dir), "--json"]
            )

        result = json.loads(capsys.readouterr().out)
        assert exc_info.value.code == 0
        assert [call[0] for call in calls] == ["artifacts", "cross_ref", "artifacts"]
        assert result["gates"]["fr_validation"]["status"] == "skipped"
        assert result["gates"]["fr_validation"]["skip_reason"] == "epic level"
        assert result["gates"]["test_coverage"]["skip_reason"] == "epic level"
        assert result["gates"]["artifact_path_verification"]["status"] == "passed"
        assert calls[-1][1][calls[-1][1].index("--phase") + 1] == "3"

    def test_task_uses_parent_spec_and_skips_plan_cross_reference(self, tmp_path: Path, monkeypatch, capsys) -> None:
        spec_dir = _write_inputs(tmp_path / "task", hierarchy="task")
        parent_dir = tmp_path / "parent"
        parent_dir.mkdir()
        parent_spec = parent_dir / "spec.md"
        parent_spec.write_text("# Parent\nFR-001\n", encoding="utf-8")
        calls: list = []
        _install_gates(monkeypatch, calls=calls)
        monkeypatch.setattr(run_phase3_gates, "get_repo_root", lambda: tmp_path)

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(
                [
                    "--hierarchy-level",
                    "task",
                    "--spec-dir",
                    str(spec_dir),
                    "--spec-context",
                    str(parent_dir),
                    "--json",
                ]
            )

        result = json.loads(capsys.readouterr().out)
        assert exc_info.value.code == 0
        assert [call[0] for call in calls] == ["fr", "coverage", "artifacts", "artifacts"]
        assert calls[0][1][calls[0][1].index("--spec-file") + 1] == str(parent_spec)
        assert calls[2][1][calls[2][1].index("--spec-context") + 1] == str(parent_spec)
        assert calls[2][1][calls[2][1].index("--phase") + 1] == "4"
        assert calls[3][1][calls[3][1].index("--spec-context") + 1] == str(parent_spec)
        assert calls[3][1][calls[3][1].index("--phase") + 1] == "4"
        assert result["gates"]["pass_g"]["status"] == "skipped"
        assert result["gates"]["pass_g"]["skip_reason"] == "task level has no local plan.md"

    def test_default_stdout_is_the_persisted_human_readable_report(self, tmp_path: Path, monkeypatch, capsys) -> None:
        spec_dir = _prepare_feature(tmp_path, monkeypatch)

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(["--hierarchy-level", "feature", "--spec-dir", str(spec_dir)])

        report = (spec_dir / "generated" / "analysis-report.md").read_text(encoding="utf-8")
        assert exc_info.value.code == 0
        assert capsys.readouterr().out == report

    def test_resolves_directory_from_active_feature_when_spec_dir_is_omitted(
        self, tmp_path: Path, monkeypatch, capsys
    ) -> None:
        spec_dir = _write_inputs(tmp_path / "feature", hierarchy="feature")
        calls: list = []
        _install_gates(monkeypatch, calls=calls)
        monkeypatch.setattr(run_phase3_gates, "get_repo_root", lambda: tmp_path)
        monkeypatch.setattr(
            run_phase3_gates,
            "resolve_active_feature",
            lambda: SimpleNamespace(feature_dir=spec_dir),
        )

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(["--hierarchy-level", "feature", "--json"])

        assert exc_info.value.code == 0
        assert json.loads(capsys.readouterr().out)["spec_dir"] == str(spec_dir.resolve())


class TestRunPhase3GatesFailures:
    """Operational errors and validator violations have distinct exit codes."""

    def test_rejects_unknown_hierarchy_level(self, tmp_path: Path, capsys) -> None:
        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(["--hierarchy-level", "unknown", "--spec-dir", str(tmp_path)])

        assert exc_info.value.code == 2
        assert "invalid choice" in capsys.readouterr().err

    def test_rejects_spec_context_for_non_task_hierarchy(self, tmp_path: Path, capsys) -> None:
        spec_dir = _write_inputs(tmp_path / "feature", hierarchy="feature")

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(
                [
                    "--hierarchy-level",
                    "feature",
                    "--spec-dir",
                    str(spec_dir),
                    "--spec-context",
                    str(tmp_path),
                ]
            )

        assert exc_info.value.code == 2
        assert "--spec-context is only valid for task hierarchy" in capsys.readouterr().err

    def test_missing_local_input_is_operational_error(self, tmp_path: Path, capsys) -> None:
        spec_dir = tmp_path / "incomplete"
        spec_dir.mkdir()

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(["--hierarchy-level", "feature", "--spec-dir", str(spec_dir)])

        assert exc_info.value.code == 2
        assert "spec.md" in capsys.readouterr().err

    def test_task_requires_parent_directory_with_spec_file(self, tmp_path: Path, capsys) -> None:
        spec_dir = _write_inputs(tmp_path / "task", hierarchy="task")
        parent = tmp_path / "parent"
        parent.mkdir()

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(
                [
                    "--hierarchy-level",
                    "task",
                    "--spec-dir",
                    str(spec_dir),
                    "--spec-context",
                    str(parent),
                ]
            )

        assert exc_info.value.code == 2
        assert "spec.md" in capsys.readouterr().err

    def test_continues_other_gates_and_returns_one_for_violations(self, tmp_path: Path, monkeypatch, capsys) -> None:
        spec_dir = _write_inputs(tmp_path / "feature", hierarchy="feature")
        calls: list = []
        failures = {
            "fr": {"covered": [], "uncovered": ["FR-001"], "total": 1},
            "coverage": {"findings": [{"key": "FR-001:no-test-task", "severity": "CRITICAL"}], "summary": {}},
            "artifacts": {
                "passed": False,
                "violations": [{"check": "referenced-path", "detail": "missing"}],
                "checks_run": ["referenced-path"],
            },
            "cross_ref": {"findings": [], "summary": {}},
        }
        _install_gates(monkeypatch, calls=calls, overrides=failures)
        for function_name in ("validate_frs_command", "test_coverage_command", "verify_artifacts_command"):
            original = getattr(run_phase3_gates, function_name)
            monkeypatch.setattr(
                run_phase3_gates,
                function_name,
                lambda argv, original=original: _run_gate_with_code(original, argv, 1),
            )
        monkeypatch.setattr(run_phase3_gates, "get_repo_root", lambda: tmp_path)

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(
                ["--hierarchy-level", "feature", "--spec-dir", str(spec_dir), "--json"]
            )

        captured = capsys.readouterr()
        assert captured.out, captured.err
        result = json.loads(captured.out)
        assert exc_info.value.code == 1
        assert len(calls) == 5
        assert result["status"] == "failed"
        assert result["gates"]["fr_validation"]["status"] == "failed"
        assert result["gates"]["test_coverage"]["status"] == "failed"
        assert result["gates"]["artifact_path_verification"]["status"] == "failed"

    def test_unscoped_final_verification_failure_is_persisted(self, tmp_path: Path, monkeypatch, capsys) -> None:
        spec_dir = _write_inputs(tmp_path / "feature", hierarchy="feature")
        calls: list = []
        _install_gates(monkeypatch, calls=calls)
        original_verify = run_phase3_gates.verify_artifacts_command

        def verify(argv: list[str]) -> None:
            calls.append(("artifacts", argv))
            if "--phase" in argv:
                return original_verify(argv)
            result_path = spec_dir / "generated" / "phase3-gates.json"
            report_path = spec_dir / "generated" / "analysis-report.md"
            assert result_path.is_file()
            assert report_path.is_file()
            print(
                json.dumps(
                    {
                        "passed": False,
                        "violations": [{"check": "unmapped-test-task", "detail": "task reference mismatch"}],
                        "checks_run": ["referenced-path", "unmapped-test-task"],
                    }
                )
            )
            raise SystemExit(1)

        monkeypatch.setattr(run_phase3_gates, "verify_artifacts_command", verify)
        monkeypatch.setattr(run_phase3_gates, "get_repo_root", lambda: tmp_path)

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(
                ["--hierarchy-level", "feature", "--spec-dir", str(spec_dir), "--json"]
            )

        captured = capsys.readouterr()
        result = json.loads(captured.out)
        saved = json.loads((spec_dir / "generated" / "phase3-gates.json").read_text(encoding="utf-8"))
        assert exc_info.value.code == 1
        assert result == saved
        assert result["status"] == "failed"
        assert result["gates"]["artifact_path_verification"]["findings"][0]["detail"] == "task reference mismatch"
        assert "--phase" not in calls[-1][1]

    def test_pass_g_high_severity_is_warning_not_failure(self, tmp_path: Path, monkeypatch, capsys) -> None:
        spec_dir = _write_inputs(tmp_path / "feature", hierarchy="feature")
        finding = {
            "reference": {"text": "missing.py", "plan_location": "L1"},
            "status": "invalid",
            "candidates": [],
            "explanation": "No match.",
        }
        _install_gates(
            monkeypatch,
            overrides={"cross_ref": {"findings": [finding], "summary": {"invalid": 1}}},
            exit_codes={"cross_ref": 1},
        )
        monkeypatch.setattr(run_phase3_gates, "get_repo_root", lambda: tmp_path)

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(
                ["--hierarchy-level", "feature", "--spec-dir", str(spec_dir), "--json"]
            )

        result = json.loads(capsys.readouterr().out)
        assert exc_info.value.code == 0
        assert result["status"] == "passed_with_warnings"
        assert result["gates"]["pass_g"]["findings"][0]["severity"] == "HIGH"

    def test_critical_pass_g_severity_fails_consolidated_run(self, tmp_path: Path, monkeypatch, capsys) -> None:
        spec_dir = _write_inputs(tmp_path / "feature", hierarchy="feature")
        finding = {"reference": {}, "status": "partial", "candidates": []}
        _install_gates(monkeypatch, overrides={"cross_ref": {"findings": [finding], "summary": {"partial": 1}}})
        monkeypatch.setattr(run_phase3_gates, "get_repo_root", lambda: tmp_path)
        monkeypatch.setattr(run_phase3_gates, "_pass_g_severity", lambda finding: "CRITICAL")

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(
                ["--hierarchy-level", "feature", "--spec-dir", str(spec_dir), "--json"]
            )

        result = json.loads(capsys.readouterr().out)
        assert exc_info.value.code == 1
        assert result["gates"]["pass_g"]["status"] == "failed"
        assert result["gates"]["pass_g"]["findings"][0]["severity"] == "CRITICAL"

    def test_malformed_gate_json_is_operational_error(self, tmp_path: Path, monkeypatch, capsys) -> None:
        spec_dir = _write_inputs(tmp_path / "feature", hierarchy="feature")
        _install_gates(monkeypatch)

        def malformed(argv: list[str]) -> None:
            print("not json")
            raise SystemExit(0)

        monkeypatch.setattr(run_phase3_gates, "validate_frs_command", malformed)

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(["--hierarchy-level", "feature", "--spec-dir", str(spec_dir)])

        assert exc_info.value.code == 2
        assert "malformed JSON" in capsys.readouterr().err

    def test_automatic_directory_resolution_failure_is_operational(self, monkeypatch, capsys) -> None:
        def fail_resolve_active_feature():
            raise run_phase3_gates.FeatureResolutionError("no active feature")

        monkeypatch.setattr(run_phase3_gates, "resolve_active_feature", fail_resolve_active_feature)

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(["--hierarchy-level", "feature"])

        assert exc_info.value.code == 2
        assert "no active feature" in capsys.readouterr().err

    def test_output_write_failure_is_operational(self, tmp_path: Path, monkeypatch, capsys) -> None:
        spec_dir = _write_inputs(tmp_path / "feature", hierarchy="feature")
        _install_gates(monkeypatch)
        monkeypatch.setattr(run_phase3_gates, "get_repo_root", lambda: tmp_path)
        monkeypatch.setattr(run_phase3_gates, "_write_atomically", lambda *args: (_ for _ in ()).throw(OSError("disk")))

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(
                ["--hierarchy-level", "feature", "--spec-dir", str(spec_dir), "--json"]
            )

        assert exc_info.value.code == 2
        assert "disk" in capsys.readouterr().err


class TestRunPhase3GatesOutputValidation:
    """Malformed gate results and inconsistent artifacts fail explicitly."""

    @pytest.mark.parametrize(
        ("gate", "payload", "message"),
        [
            ("fr", {"covered": "bad", "uncovered": [], "total": 1}, "FR validation emitted an invalid result schema"),
            ("coverage", {"findings": "bad", "summary": {}}, "E.2 test coverage emitted an invalid result schema"),
            (
                "artifacts",
                {"violations": [], "checks_run": [], "passed": "yes"},
                "Artifact-path verification emitted an invalid result schema",
            ),
            (
                "artifacts",
                {"violations": [], "checks_run": [], "passed": False},
                "Artifact-path verification passed value does not match its violations",
            ),
            ("cross_ref", {"findings": "bad"}, "Pass G cross-reference emitted an invalid result schema"),
        ],
    )
    def test_rejects_invalid_gate_payload_shapes(
        self, tmp_path: Path, monkeypatch, capsys, gate: str, payload: dict, message: str
    ) -> None:
        spec_dir = _prepare_feature(tmp_path, monkeypatch, overrides={gate: payload})

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(["--hierarchy-level", "feature", "--spec-dir", str(spec_dir)])

        assert exc_info.value.code == 2
        assert message in capsys.readouterr().err

    @pytest.mark.parametrize(
        ("gate", "payload", "message"),
        [
            (
                "fr",
                {"covered": [], "uncovered": ["FR-001"], "total": 1},
                "FR validation exit code does not match",
            ),
            (
                "coverage",
                {"findings": [{"key": "FR-001"}], "summary": {}, "coverage": {}, "summary_table": ""},
                "E.2 test coverage exit code does not match",
            ),
            (
                "artifacts",
                {"passed": True, "violations": [], "checks_run": []},
                "Artifact-path verification exit code does not match",
            ),
            (
                "cross_ref",
                {"findings": [{"reference": {}, "status": "invalid", "candidates": [], "explanation": "Missing."}]},
                "Pass G exit code does not match",
            ),
        ],
    )
    def test_rejects_gate_exit_code_mismatches(
        self, tmp_path: Path, monkeypatch, capsys, gate: str, payload: dict, message: str
    ) -> None:
        spec_dir = _prepare_feature(
            tmp_path,
            monkeypatch,
            overrides={gate: payload},
            exit_codes={gate: 1 if gate == "artifacts" else 0},
        )

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(["--hierarchy-level", "feature", "--spec-dir", str(spec_dir)])

        assert exc_info.value.code == 2
        assert message in capsys.readouterr().err

    @pytest.mark.parametrize(
        "payload",
        [
            {"covered": [], "uncovered": [], "total": 1},
            {"covered": ["FR-001"], "uncovered": [], "total": -1},
        ],
    )
    def test_rejects_inconsistent_fr_totals(self, tmp_path: Path, monkeypatch, capsys, payload: dict) -> None:
        spec_dir = _prepare_feature(tmp_path, monkeypatch, overrides={"fr": payload})

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(["--hierarchy-level", "feature", "--spec-dir", str(spec_dir)])

        assert exc_info.value.code == 2
        assert "FR validation total does not match unique covered and uncovered FRs" in capsys.readouterr().err

    def test_rejects_non_object_coverage_findings(self, tmp_path: Path, monkeypatch, capsys) -> None:
        spec_dir = _prepare_feature(
            tmp_path,
            monkeypatch,
            overrides={"coverage": {"findings": ["bad"], "summary": {}, "coverage": {}, "summary_table": ""}},
        )

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(["--hierarchy-level", "feature", "--spec-dir", str(spec_dir)])

        assert exc_info.value.code == 2
        assert "findings must be JSON objects" in capsys.readouterr().err

    def test_rejects_non_object_artifact_violations(self, tmp_path: Path, monkeypatch, capsys) -> None:
        spec_dir = _prepare_feature(
            tmp_path,
            monkeypatch,
            overrides={"artifacts": {"passed": True, "violations": ["bad"], "checks_run": []}},
        )

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(["--hierarchy-level", "feature", "--spec-dir", str(spec_dir)])

        assert exc_info.value.code == 2
        assert "violations must be JSON objects" in capsys.readouterr().err

    @pytest.mark.parametrize(
        ("finding", "message"),
        [
            ({"reference": [], "status": "partial", "candidates": []}, "reference must be a JSON object"),
            (
                {"reference": {}, "status": "partial", "candidates": [], "explanation": 7},
                "explanation must be a string",
            ),
            (
                {"reference": {}, "status": "unknown", "candidates": []},
                "unsupported Pass G status",
            ),
        ],
    )
    def test_rejects_invalid_pass_g_findings(
        self, tmp_path: Path, monkeypatch, capsys, finding: dict, message: str
    ) -> None:
        spec_dir = _prepare_feature(
            tmp_path,
            monkeypatch,
            overrides={"cross_ref": {"findings": [finding]}},
        )

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(["--hierarchy-level", "feature", "--spec-dir", str(spec_dir)])

        assert exc_info.value.code == 2
        assert message in capsys.readouterr().err

    def test_rejects_non_string_fr_warning(self, tmp_path: Path, monkeypatch, capsys) -> None:
        spec_dir = _prepare_feature(
            tmp_path,
            monkeypatch,
            overrides={"fr": {"covered": ["FR-001"], "uncovered": [], "total": 1, "warning": 5}},
        )

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(["--hierarchy-level", "feature", "--spec-dir", str(spec_dir)])

        assert exc_info.value.code == 2
        assert "FR validation warning must be a string" in capsys.readouterr().err

    def test_reports_fr_warning_without_failing(self, tmp_path: Path, monkeypatch, capsys) -> None:
        spec_dir = _prepare_feature(
            tmp_path,
            monkeypatch,
            overrides={"fr": {"covered": ["FR-001"], "uncovered": [], "total": 1, "warning": "No FRs found."}},
        )

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(
                ["--hierarchy-level", "feature", "--spec-dir", str(spec_dir), "--json"]
            )

        result = json.loads(capsys.readouterr().out)
        assert exc_info.value.code == 0
        assert result["status"] == "passed_with_warnings"
        assert result["gates"]["fr_validation"]["status"] == "passed_with_warnings"

    def test_missing_spec_directory_is_operational_error(self, tmp_path: Path, capsys) -> None:
        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(
                ["--hierarchy-level", "epic", "--spec-dir", str(tmp_path / "missing")]
            )

        assert exc_info.value.code == 2
        assert "does not exist" in capsys.readouterr().err

    def test_task_requires_spec_context(self, tmp_path: Path, capsys) -> None:
        spec_dir = _write_inputs(tmp_path / "task", hierarchy="task")

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(["--hierarchy-level", "task", "--spec-dir", str(spec_dir)])

        assert exc_info.value.code == 2
        assert "requires --spec-context" in capsys.readouterr().err

    def test_task_spec_context_must_be_a_directory(self, tmp_path: Path, capsys) -> None:
        spec_dir = _write_inputs(tmp_path / "task", hierarchy="task")
        parent = tmp_path / "file"
        parent.write_text("not a directory", encoding="utf-8")

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(
                [
                    "--hierarchy-level",
                    "task",
                    "--spec-dir",
                    str(spec_dir),
                    "--spec-context",
                    str(parent),
                ]
            )

        assert exc_info.value.code == 2
        assert "must be a parent directory" in capsys.readouterr().err

    def test_unreadable_required_input_is_operational_error(self, tmp_path: Path, monkeypatch, capsys) -> None:
        spec_dir = _write_inputs(tmp_path / "feature", hierarchy="feature")
        original_read_text = Path.read_text

        def fail_spec_read(path: Path, *args, **kwargs):
            if path == spec_dir / "spec.md":
                raise OSError("unreadable")
            return original_read_text(path, *args, **kwargs)

        monkeypatch.setattr(Path, "read_text", fail_spec_read)

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(["--hierarchy-level", "feature", "--spec-dir", str(spec_dir)])

        assert exc_info.value.code == 2
        assert "Cannot read required Phase 3 input" in capsys.readouterr().err

    @pytest.mark.parametrize(
        "failure",
        ["result", "missing-section", "report", "final-result", "final-missing-section", "final-report"],
    )
    def test_rejects_inconsistent_persisted_artifacts(self, tmp_path: Path, monkeypatch, capsys, failure: str) -> None:
        spec_dir = _prepare_feature(tmp_path, monkeypatch)
        original_write = run_phase3_gates._write_atomically
        original_render = run_phase3_gates._render_report
        render_count = 0
        write_count = 0

        def write_tampered(path: Path, content: str) -> None:
            nonlocal write_count
            if path.name == "phase3-gates.json":
                write_count += 1
            if failure == "result" and path.name == "phase3-gates.json":
                content = content.replace('"schema_version": 1', '"schema_version": 2')
            if failure == "final-result" and path.name == "phase3-gates.json" and write_count == 2:
                content = content.replace('"schema_version": 1', '"schema_version": 2')
            original_write(path, content)

        def render_report(result: dict) -> str:
            nonlocal render_count
            render_count += 1
            report = "" if failure == "missing-section" else original_render(result)
            return report + ("inconsistent\n" if failure == "report" and render_count > 1 else "")

        def render_final_report(result: dict) -> str:
            nonlocal render_count
            render_count += 1
            if failure == "final-missing-section" and render_count == 3:
                return ""
            report = original_render(result)
            return report + ("inconsistent\n" if failure == "final-report" and render_count > 3 else "")

        monkeypatch.setattr(run_phase3_gates, "_write_atomically", write_tampered)
        monkeypatch.setattr(
            run_phase3_gates,
            "_render_report",
            render_final_report if failure.startswith("final-") else render_report,
        )

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(["--hierarchy-level", "feature", "--spec-dir", str(spec_dir)])

        assert exc_info.value.code == 2
        errors = capsys.readouterr().err
        expected = {
            "result": "does not match the staged result",
            "missing-section": "missing a required section",
            "report": "inconsistent with phase3-gates.json",
            "final-result": "does not match the final result",
            "final-missing-section": "missing a required section",
            "final-report": "inconsistent with phase3-gates.json",
        }
        assert expected[failure] in errors

    @pytest.mark.parametrize(
        ("payload", "exit_code", "message"),
        [
            (
                {"passed": "yes", "violations": [], "checks_run": []},
                0,
                "Complete artifact verification emitted an invalid result schema",
            ),
            (
                {"passed": True, "violations": ["bad"], "checks_run": []},
                0,
                "Complete artifact verification violations must be JSON objects",
            ),
            (
                {"passed": True, "violations": [{}], "checks_run": []},
                0,
                "Complete artifact verification passed value does not match its violations",
            ),
            (
                {"passed": False, "violations": [{}], "checks_run": []},
                0,
                "Complete artifact verification exit code does not match",
            ),
        ],
    )
    def test_rejects_invalid_final_verification_results(
        self, tmp_path: Path, monkeypatch, capsys, payload: dict, exit_code: int, message: str
    ) -> None:
        spec_dir = _prepare_feature(tmp_path, monkeypatch)
        original_verify = run_phase3_gates.verify_artifacts_command

        def verify(argv: list[str]) -> None:
            if "--phase" in argv:
                original_verify(argv)
                return
            print(json.dumps(payload))
            raise SystemExit(exit_code)

        monkeypatch.setattr(run_phase3_gates, "verify_artifacts_command", verify)

        with pytest.raises(SystemExit) as exc_info:
            run_phase3_gates.run_phase3_gates_command(["--hierarchy-level", "feature", "--spec-dir", str(spec_dir)])

        assert exc_info.value.code == 2
        assert message in capsys.readouterr().err


def _run_gate_with_code(command, argv: list[str], code: int) -> None:
    try:
        command(argv)
    except SystemExit:
        raise SystemExit(code)
