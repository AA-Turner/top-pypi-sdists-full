from tests.markers import require_pytest_7_3, require_pytest_reportlog


@require_pytest_7_3
@require_pytest_reportlog
def test_report_log_does_not_crash(pytester):
    pytester.copy_example("examples/test_example_multiple_failures.py")
    report_log = pytester.path / "log.json"

    result = pytester.runpytest(
        "--report-log=log.json",
        "--check-max-tb=2",
        "--check-max-tb-line=5",
    )

    result.assert_outcomes(failed=1)
    assert report_log.exists()
