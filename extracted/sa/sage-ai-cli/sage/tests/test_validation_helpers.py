from dataclasses import dataclass

from sage.core.validation_helpers import aggregate_status, strict_aggregate_status


@dataclass
class MockReport:
    install_ok: bool | None = None
    build_ok: bool | None = None
    runs_ok: bool | None = None
    tests_ok: bool | None = None


class TestAggregateStatus:
    def test_empty_list_returns_none(self):
        assert aggregate_status([], "build_ok") is None
        assert strict_aggregate_status([], "tests_ok") is None

    def test_aggregate_status_lenient(self):
        # build_ok allows mixed [True, None] because not all sub-projects need a build step
        reports = [
            MockReport(build_ok=True),
            MockReport(build_ok=None),
        ]
        assert aggregate_status(reports, "build_ok") is True

        # If all are None, it returns None
        reports = [
            MockReport(build_ok=None),
            MockReport(build_ok=None),
        ]
        assert aggregate_status(reports, "build_ok") is None

        # If any is False, it returns False regardless of Trues
        reports = [
            MockReport(build_ok=True),
            MockReport(build_ok=False),
            MockReport(build_ok=None),
        ]
        assert aggregate_status(reports, "build_ok") is False

    def test_strict_aggregate_status(self):
        # tests_ok is strict: ALL components must have tests, so [True, None] must FAIL
        reports = [
            MockReport(tests_ok=True),
            MockReport(tests_ok=None),
        ]
        assert strict_aggregate_status(reports, "tests_ok") is False

        # If any is False, it also fails
        reports = [
            MockReport(tests_ok=True),
            MockReport(tests_ok=False),
        ]
        assert strict_aggregate_status(reports, "tests_ok") is False

        # It only passes if ALL are True
        reports = [
            MockReport(tests_ok=True),
            MockReport(tests_ok=True),
        ]
        assert strict_aggregate_status(reports, "tests_ok") is True

        # If all are None, it fails (because None in vals triggers False)
        reports = [
            MockReport(tests_ok=None),
            MockReport(tests_ok=None),
        ]
        assert strict_aggregate_status(reports, "tests_ok") is False
