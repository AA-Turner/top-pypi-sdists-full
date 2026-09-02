"""Tests for run_doctor()."""

from unittest.mock import MagicMock

from agentic_devtools.cli.setup.dependency_checker import DependencyStatus
from agentic_devtools.cli.setup.doctor import RepairRegistry, run_doctor
from agentic_devtools.cli.setup.exit_codes import ExitCode
from agentic_devtools.cli.setup.fixloop import ErrorClass


def _dep(name: str, *, required: bool, found: bool) -> DependencyStatus:
    return DependencyStatus(name=name, found=found, required=required)


def _healthy() -> list[DependencyStatus]:
    return [
        _dep("git", required=True, found=True),
        _dep("gh", required=False, found=True),
    ]


def _missing_required() -> list[DependencyStatus]:
    return [
        _dep("git", required=True, found=False),
        _dep("gh", required=False, found=True),
    ]


def _missing_optional() -> list[DependencyStatus]:
    return [
        _dep("git", required=True, found=True),
        _dep("copilot", required=False, found=False),
    ]


class TestRunDoctorHealthyEnvironment:
    """run_doctor() short-circuits to OK when no problems are detected."""

    def test_exit_code_ok_when_all_deps_present(self):
        """Exit code is OK (0) when all required deps are present."""
        result = run_doctor(_healthy())
        assert result.report.exit_code == ExitCode.OK.value

    def test_mode_check_without_fix_flag(self):
        """Report mode is 'check' when fix=False (default)."""
        result = run_doctor(_healthy(), fix=False)
        assert result.report.mode == "check"

    def test_mode_check_fix_with_fix_flag(self):
        """Report mode is 'check-fix' when fix=True, even with no problems."""
        result = run_doctor(_healthy(), fix=True)
        assert result.report.mode == "check-fix"

    def test_no_problems_when_healthy(self):
        """problems list is empty when all deps are found."""
        result = run_doctor(_healthy())
        assert result.problems == []

    def test_no_repair_outcomes_when_healthy(self):
        """No repairs are attempted when no problems are detected."""
        result = run_doctor(_healthy(), fix=True)
        assert result.repair_outcomes == []

    def test_no_factory_invoked_when_healthy(self):
        """Registered factory is NOT invoked when system is healthy."""
        registry = RepairRegistry()
        factory = MagicMock()
        registry.register(ErrorClass.MISSING_DEPENDENCY, factory)

        run_doctor(_healthy(), fix=True, registry=registry)

        factory.assert_not_called()

    def test_optional_missing_is_not_a_problem(self):
        """A missing optional dependency does not create a problem entry."""
        result = run_doctor(_missing_optional())
        assert result.problems == []
        assert result.report.exit_code == ExitCode.OK.value


class TestRunDoctorWithProblems:
    """run_doctor() detects and reports missing required dependencies."""

    def test_missing_required_yields_problem(self):
        """Missing required dep appears in result.problems."""
        result = run_doctor(_missing_required())
        assert len(result.problems) == 1
        assert result.problems[0].name == "git"

    def test_exit_code_missing_required_when_no_fix(self):
        """Exit code is MISSING_REQUIRED_DEP when problem exists and fix=False."""
        result = run_doctor(_missing_required(), fix=False)
        assert result.report.exit_code == ExitCode.MISSING_REQUIRED_DEP.value

    def test_check_phase_is_failed_when_problems(self):
        """The 'check' phase result status is 'failed' when problems are detected."""
        result = run_doctor(_missing_required())
        check_phase = next(p for p in result.report.phases if p.name == "check")
        assert check_phase.status == "failed"

    def test_no_repair_without_fix_flag(self):
        """No factory is invoked and no repair outcomes are produced when fix=False."""
        registry = RepairRegistry()
        factory = MagicMock()
        registry.register(ErrorClass.MISSING_DEPENDENCY, factory)

        result = run_doctor(_missing_required(), fix=False, registry=registry)

        factory.assert_not_called()
        assert result.repair_outcomes == []


class TestRunDoctorRepairDispatch:
    """run_doctor() dispatches registered repairs when fix=True."""

    def test_factory_invoked_once_and_repair_called_once(self):
        """Factory is invoked exactly once and returned repair is called exactly once."""
        registry = RepairRegistry()
        repair_fn = MagicMock()
        factory = MagicMock(return_value=repair_fn)
        registry.register(ErrorClass.MISSING_DEPENDENCY, factory)

        run_doctor(_missing_required(), fix=True, registry=registry)

        factory.assert_called_once()
        repair_fn.assert_called_once()

    def test_repair_receives_dependency_status(self):
        """Repair function is called with the problematic DependencyStatus."""
        registry = RepairRegistry()
        received: list[DependencyStatus] = []

        def capture(dep: DependencyStatus) -> None:
            received.append(dep)

        registry.register(ErrorClass.MISSING_DEPENDENCY, lambda: capture)
        run_doctor(_missing_required(), fix=True, registry=registry)

        assert len(received) == 1
        assert received[0].name == "git"

    def test_successful_repair_recorded_in_outcomes(self):
        """A successful repair produces a RepairOutcome with success=True."""
        registry = RepairRegistry()

        def fix_dep(dep: DependencyStatus) -> None:
            dep.found = True  # simulate a real repair mutating the status in-place

        registry.register(ErrorClass.MISSING_DEPENDENCY, lambda: fix_dep)

        result = run_doctor(_missing_required(), fix=True, registry=registry)

        assert len(result.repair_outcomes) == 1
        assert result.repair_outcomes[0].success is True

    def test_problems_snapshot_preserves_pre_repair_found_false(self):
        """result.problems reflects the pre-repair state even after a successful repair."""
        registry = RepairRegistry()

        def fix_dep(dep: DependencyStatus) -> None:
            dep.found = True  # mutates dep in-place

        registry.register(ErrorClass.MISSING_DEPENDENCY, lambda: fix_dep)

        result = run_doctor(_missing_required(), fix=True, registry=registry)

        # The repair succeeded (exit code OK) but problems snapshot still shows found=False
        assert result.report.exit_code == ExitCode.OK.value
        assert len(result.problems) == 1
        assert result.problems[0].found is False

    def test_exit_code_ok_after_successful_repair(self):
        """Exit code is OK (0) when the only problem is repaired successfully."""
        registry = RepairRegistry()

        def fix_dep(dep: DependencyStatus) -> None:
            dep.found = True  # simulate a real repair mutating the status in-place

        registry.register(ErrorClass.MISSING_DEPENDENCY, lambda: fix_dep)

        result = run_doctor(_missing_required(), fix=True, registry=registry)

        assert result.report.exit_code == ExitCode.OK.value

    def test_noop_repair_treated_as_failure(self):
        """A repair that returns without mutating dep is recorded as success=False."""
        registry = RepairRegistry()
        registry.register(ErrorClass.MISSING_DEPENDENCY, lambda: lambda _: None)  # no-op

        result = run_doctor(_missing_required(), fix=True, registry=registry)

        assert result.repair_outcomes[0].success is False
        assert "still unavailable" in (result.repair_outcomes[0].error_message or "")

    def test_noop_repair_exit_code_is_failing(self):
        """Exit code reflects unresolved problem when repair is a no-op."""
        registry = RepairRegistry()
        registry.register(ErrorClass.MISSING_DEPENDENCY, lambda: lambda _: None)  # no-op

        result = run_doctor(_missing_required(), fix=True, registry=registry)

        assert result.report.exit_code == ExitCode.MISSING_REQUIRED_DEP.value

    def test_no_registered_repair_produces_skipped_phase(self):
        """When no repair is registered, phase status is 'skipped' (not 'failed')."""
        registry = RepairRegistry()  # empty — no repair registered

        result = run_doctor(_missing_required(), fix=True, registry=registry)

        repair_phase = next(p for p in result.report.phases if p.name.startswith("repair:"))
        assert repair_phase.status == "skipped"

    def test_no_registered_repair_produces_failed_outcome(self):
        """RepairOutcome has success=False when no factory is registered."""
        registry = RepairRegistry()

        result = run_doctor(_missing_required(), fix=True, registry=registry)

        assert len(result.repair_outcomes) == 1
        assert result.repair_outcomes[0].success is False

    def test_repair_exception_is_caught_not_propagated(self):
        """Repair function raising an exception does not crash run_doctor()."""
        registry = RepairRegistry()

        def failing(_: DependencyStatus) -> None:
            raise RuntimeError("install network error")

        registry.register(ErrorClass.MISSING_DEPENDENCY, lambda: failing)

        result = run_doctor(_missing_required(), fix=True, registry=registry)  # must not raise

        assert result.repair_outcomes[0].success is False
        assert "install network error" in (result.repair_outcomes[0].error_message or "")

    def test_repair_exception_phase_status_is_failed(self):
        """Phase status is 'failed' when the repair function raises."""
        registry = RepairRegistry()

        def failing(_: DependencyStatus) -> None:
            raise ValueError("oops")

        registry.register(ErrorClass.MISSING_DEPENDENCY, lambda: failing)

        result = run_doctor(_missing_required(), fix=True, registry=registry)

        repair_phase = next(p for p in result.report.phases if p.name.startswith("repair:"))
        assert repair_phase.status == "failed"
        assert repair_phase.error is not None

    def test_exit_code_still_failing_after_failed_repair(self):
        """Exit code reflects unresolved problem when repair fails."""
        registry = RepairRegistry()

        def failing(_: DependencyStatus) -> None:
            raise RuntimeError("fail")

        registry.register(ErrorClass.MISSING_DEPENDENCY, lambda: failing)

        result = run_doctor(_missing_required(), fix=True, registry=registry)

        assert result.report.exit_code == ExitCode.MISSING_REQUIRED_DEP.value

    def test_factory_exception_is_caught_and_recorded_as_failed(self):
        """Factory invocation exception is caught and recorded as failed phase."""
        registry = RepairRegistry()

        def bad_factory():
            raise ImportError("module not found")

        registry.register(ErrorClass.MISSING_DEPENDENCY, bad_factory)

        result = run_doctor(_missing_required(), fix=True, registry=registry)

        assert result.repair_outcomes[0].success is False
        assert "module not found" in (result.repair_outcomes[0].error_message or "")
        repair_phase = next(p for p in result.report.phases if p.name.startswith("repair:"))
        assert repair_phase.status == "failed"

    def test_repair_exception_remaining_repairs_continue(self):
        """After one repair fails, remaining same-class repairs are still dispatched."""
        statuses = [
            _dep("git", required=True, found=False),
            _dep("node", required=True, found=False),
        ]
        registry = RepairRegistry()

        call_order: list[str] = []

        def failing(_: DependencyStatus) -> None:
            call_order.append("git")
            raise RuntimeError("git repair failed")

        def success(dep: DependencyStatus) -> None:
            call_order.append("node")
            dep.found = True

        # One factory dispatches to different repair behaviors based on dep name
        # within the same error class (MISSING_DEPENDENCY).
        def smart_factory():
            def repair(dep: DependencyStatus) -> None:
                if dep.name == "git":
                    failing(dep)
                else:
                    success(dep)

            return repair

        registry.register(ErrorClass.MISSING_DEPENDENCY, smart_factory)

        result = run_doctor(statuses, fix=True, registry=registry)

        assert call_order == ["git", "node"]
        assert len(result.repair_outcomes) == 2
        # git failed, node succeeded
        assert result.repair_outcomes[0].success is False
        assert result.repair_outcomes[1].success is True

    def test_multiple_same_class_problems_all_use_registered_factory(self):
        """Same-class problems invoke the registered factory and repair once per dep."""
        registry = RepairRegistry()
        repair_fn = MagicMock(
            side_effect=lambda dep: setattr(dep, "found", True),
        )
        factory = MagicMock(return_value=repair_fn)
        registry.register(ErrorClass.MISSING_DEPENDENCY, factory)

        statuses = [
            _dep("git", required=True, found=False),
            _dep("node", required=True, found=False),
        ]

        result = run_doctor(statuses, fix=True, registry=registry)

        assert factory.call_count == 2
        assert repair_fn.call_count == 2
        assert [call.args[0].name for call in repair_fn.call_args_list] == ["git", "node"]
        assert len(result.repair_outcomes) == 2
        assert all(o.success for o in result.repair_outcomes)


class TestRunDoctorDispatchOrder:
    """run_doctor() dispatches repairs in ErrorClass enum definition order."""

    def test_same_class_stable_sort_preserves_discovery_order(self):
        """Same-ErrorClass problems preserve check-phase discovery order after sorting."""
        statuses = [
            _dep("node", required=True, found=False),
            _dep("git", required=True, found=False),
        ]

        registry = RepairRegistry()
        dispatch_order: list[str] = []

        def tracking_repair(dep: DependencyStatus) -> None:
            dispatch_order.append(dep.name)
            dep.found = True

        registry.register(ErrorClass.MISSING_DEPENDENCY, lambda: tracking_repair)

        run_doctor(statuses, fix=True, registry=registry)

        # Same ErrorClass — check-phase discovery order preserved (stable sort)
        assert dispatch_order == ["node", "git"]

    def test_same_class_preserves_check_phase_order(self):
        """Same-ErrorClass problems preserve check-phase discovery order."""
        statuses = [
            _dep("alpha", required=True, found=False),
            _dep("beta", required=True, found=False),
            _dep("gamma", required=True, found=False),
        ]

        registry = RepairRegistry()
        dispatch_order: list[str] = []

        def tracking_repair(dep: DependencyStatus) -> None:
            dispatch_order.append(dep.name)
            dep.found = True

        registry.register(ErrorClass.MISSING_DEPENDENCY, lambda: tracking_repair)

        run_doctor(statuses, fix=True, registry=registry)

        assert dispatch_order == ["alpha", "beta", "gamma"]

    def test_no_factory_invoked_in_check_only_mode(self):
        """No factory is invoked when fix=False regardless of registry contents."""
        registry = RepairRegistry()
        factory = MagicMock()
        registry.register(ErrorClass.MISSING_DEPENDENCY, factory)

        run_doctor(_missing_required(), fix=False, registry=registry)

        factory.assert_not_called()

    def test_unregistered_error_class_produces_skipped_phase(self):
        """Unregistered error class produces skipped phase and success=False without crashing."""
        registry = RepairRegistry()  # empty registry

        result = run_doctor(_missing_required(), fix=True, registry=registry)

        repair_phase = next(p for p in result.report.phases if p.name.startswith("repair:"))
        assert repair_phase.status == "skipped"
        assert result.repair_outcomes[0].success is False
        # Exit code reflects worst unresolved
        assert result.report.exit_code == ExitCode.MISSING_REQUIRED_DEP.value


class TestRunDoctorReportSchema:
    """run_doctor() always produces a valid SetupReport."""

    def test_report_has_check_phase(self):
        """Every invocation includes a 'check' phase in the report."""
        result = run_doctor(_healthy())
        names = [p.name for p in result.report.phases]
        assert "check" in names

    def test_report_exit_code_name_ok(self):
        """exit_code_name is 'OK' when all deps are healthy."""
        result = run_doctor(_healthy())
        assert result.report.exit_code_name == "OK"

    def test_report_schema_version_is_1(self):
        """Schema version is always 1."""
        result = run_doctor(_healthy())
        assert result.report.schema_version == 1

    def test_to_dict_is_valid_json_serialisable(self):
        """to_dict() output is JSON-serialisable in all cases."""
        import json

        for statuses in [_healthy(), _missing_required()]:
            result = run_doctor(statuses, fix=True)
            serialised = json.dumps(result.report.to_dict())
            parsed = json.loads(serialised)
            assert "mode" in parsed
            assert "exit_code" in parsed

    def test_to_dict_mode_check_when_fix_false(self):
        """to_dict() returns mode='check' when fix=False."""
        import json

        result = run_doctor(_healthy(), fix=False)
        data = json.loads(json.dumps(result.report.to_dict()))
        assert data["mode"] == "check"
        assert data["schema_version"] == 1

    def test_to_dict_mode_check_fix_when_fix_true_healthy(self):
        """to_dict() returns mode='check-fix' when fix=True and env is healthy."""
        import json

        result = run_doctor(_healthy(), fix=True)
        data = json.loads(json.dumps(result.report.to_dict()))
        assert data["mode"] == "check-fix"

    def test_to_dict_exit_code_2_when_missing_required(self):
        """to_dict() includes exit_code=2 and MISSING_REQUIRED_DEP when dep is missing."""
        import json

        result = run_doctor(_missing_required(), fix=False)
        data = json.loads(json.dumps(result.report.to_dict()))
        assert data["exit_code"] == 2
        assert data["exit_code_name"] == "MISSING_REQUIRED_DEP"


class TestRunDoctorRepairDetails:
    """run_doctor() copies repair_details into outcome and merges into extra_details."""

    def test_repair_details_copied_to_outcome_on_success(self):
        """On successful repair, dep.repair_details is copied to outcome.details."""
        dep = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True)
        registry = RepairRegistry()

        def _factory():
            def _repair(d):
                d.found = True
                d.repair_details["deleted_artifacts"] = ["/sp/foo"]

            return _repair

        registry.register(ErrorClass.STALE_PARTIAL_INSTALL, _factory)
        result = run_doctor([dep], fix=True, registry=registry)
        assert result.repair_outcomes[0].details == {"deleted_artifacts": ["/sp/foo"]}

    def test_repair_details_merged_into_report_details(self):
        """Outcome details are merged into the report's extra_details."""
        dep = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True)
        registry = RepairRegistry()

        def _factory():
            def _repair(d):
                d.found = True
                d.repair_details["deleted_artifacts"] = ["/sp/foo"]

            return _repair

        registry.register(ErrorClass.STALE_PARTIAL_INSTALL, _factory)
        result = run_doctor([dep], fix=True, registry=registry)
        assert result.report.details.get("deleted_artifacts") == ["/sp/foo"]

    def test_list_collision_concatenated(self):
        """Colliding list keys are concatenated."""
        dep1 = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True)
        dep2 = DependencyStatus(name="path-profile", found=False, required=True)
        registry = RepairRegistry()

        def _factory1():
            def _repair(d):
                d.found = True
                d.repair_details["items"] = ["a"]

            return _repair

        def _factory2():
            def _repair(d):
                d.found = True
                d.repair_details["items"] = ["b"]

            return _repair

        registry.register(ErrorClass.STALE_PARTIAL_INSTALL, _factory1)
        registry.register(ErrorClass.PATH_PROFILE_NOT_UPDATED, _factory2)
        result = run_doctor([dep1, dep2], fix=True, registry=registry)
        assert result.report.details.get("items") == ["a", "b"]

    def test_non_list_collision_earlier_wins(self):
        """Non-list collision: earlier value wins."""
        dep1 = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True)
        dep2 = DependencyStatus(name="path-profile", found=False, required=True)
        registry = RepairRegistry()

        def _factory1():
            def _repair(d):
                d.found = True
                d.repair_details["key"] = "first"

            return _repair

        def _factory2():
            def _repair(d):
                d.found = True
                d.repair_details["key"] = "second"

            return _repair

        registry.register(ErrorClass.STALE_PARTIAL_INSTALL, _factory1)
        registry.register(ErrorClass.PATH_PROFILE_NOT_UPDATED, _factory2)
        result = run_doctor([dep1, dep2], fix=True, registry=registry)
        assert result.report.details["key"] == "first"

    def test_problems_snapshot_has_empty_repair_details(self):
        """problems snapshot has repair_details reset to {} (mutation isolation)."""
        dep = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True)
        registry = RepairRegistry()

        def _factory():
            def _repair(d):
                d.found = True
                d.repair_details["deleted_artifacts"] = ["/sp/foo"]

            return _repair

        registry.register(ErrorClass.STALE_PARTIAL_INSTALL, _factory)
        result = run_doctor([dep], fix=True, registry=registry)
        assert result.problems[0].repair_details == {}

    def test_repair_never_invoked_when_found_true(self):
        """Repair is never dispatched when dep.found is already True."""
        dep = DependencyStatus(name="corrupted-install-artifacts", found=True, required=True)
        registry = RepairRegistry()
        mock_fn = MagicMock()
        registry.register(ErrorClass.STALE_PARTIAL_INSTALL, lambda: mock_fn)
        result = run_doctor([dep], fix=True, registry=registry)
        mock_fn.assert_not_called()
        assert result.repair_outcomes == []

    def test_user_declined_repair_recorded_as_error_message(self):
        """UserDeclinedRepairError str is recorded as error_message."""
        from agentic_devtools.cli.setup.doctor_repair import UserDeclinedRepairError

        dep = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True)
        registry = RepairRegistry()

        def _factory():
            def _repair(d):
                raise UserDeclinedRepairError("User declined destructive repair")

            return _repair

        registry.register(ErrorClass.STALE_PARTIAL_INSTALL, _factory)
        result = run_doctor([dep], fix=True, registry=registry)
        assert result.repair_outcomes[0].success is False
        assert "User declined" in (result.repair_outcomes[0].error_message or "")

    def test_exception_outcome_preserves_repair_details(self):
        """Exception path still carries repair_details into outcome and report."""
        dep = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True)
        registry = RepairRegistry()

        def _factory():
            def _repair(d):
                d.repair_details["detected_artifacts"] = ["/sp/foo"]
                raise RuntimeError("boom")

            return _repair

        registry.register(ErrorClass.STALE_PARTIAL_INSTALL, _factory)
        result = run_doctor([dep], fix=True, registry=registry)
        assert result.repair_outcomes[0].details == {"detected_artifacts": ["/sp/foo"]}
        assert result.report.details.get("detected_artifacts") == ["/sp/foo"]

    def test_failed_artifacts_builds_descriptive_error_message(self):
        """When failed_artifacts present, error_message is descriptive."""
        dep = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True)
        registry = RepairRegistry()

        def _factory():
            def _repair(d):
                d.repair_details["failed_artifacts"] = [{"path": "/sp/foo", "error": "Permission denied"}]
                # dep.found stays False -> repair_failed

            return _repair

        registry.register(ErrorClass.STALE_PARTIAL_INSTALL, _factory)
        result = run_doctor([dep], fix=True, registry=registry)
        msg = result.repair_outcomes[0].error_message or ""
        assert "1 artifact(s) could not be deleted" in msg
        assert "/sp/foo" in msg
        assert "Permission denied" in msg

    def test_failed_artifacts_non_dict_entry_falls_back_to_str(self):
        """When failed_artifacts contains non-dict entries, str() is used instead of .get()."""
        dep = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True)
        registry = RepairRegistry()

        def _factory():
            def _repair(d):
                d.repair_details["failed_artifacts"] = ["unexpected-string-entry"]
                # dep.found stays False -> repair_failed

            return _repair

        registry.register(ErrorClass.STALE_PARTIAL_INSTALL, _factory)
        result = run_doctor([dep], fix=True, registry=registry)
        msg = result.repair_outcomes[0].error_message or ""
        assert "1 artifact(s) could not be deleted" in msg
        assert "unexpected-string-entry" in msg

    def test_failed_artifacts_scalar_value_is_treated_as_single_entry(self):
        """A truthy non-list failed_artifacts value is wrapped instead of iterated."""
        dep = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True)
        registry = RepairRegistry()

        def _factory():
            def _repair(d):
                d.repair_details["failed_artifacts"] = 7
                # dep.found stays False -> repair_failed

            return _repair

        registry.register(ErrorClass.STALE_PARTIAL_INSTALL, _factory)
        result = run_doctor([dep], fix=True, registry=registry)
        msg = result.repair_outcomes[0].error_message or ""
        assert "1 artifact(s) could not be deleted" in msg
        assert "7" in msg

    def test_no_fix_does_not_dispatch_repair(self):
        """run_doctor with fix=False does not dispatch repair."""
        dep = DependencyStatus(name="corrupted-install-artifacts", found=False, required=True)
        registry = RepairRegistry()
        mock_fn = MagicMock()
        registry.register(ErrorClass.STALE_PARTIAL_INSTALL, lambda: mock_fn)
        result = run_doctor([dep], fix=False, registry=registry)
        mock_fn.assert_not_called()
        assert result.repair_outcomes == []
