"""The generated per-app test suite (objective **O5**).

``_contracts/08-tobe-app-manifest.md`` §7 and ``ml-applications/guidelines/FIELD_REFERENCE.md`` §7 both
promise app authors that *a config-only app writes no tests*.  This package is that promise,
implemented: seven checks derived from an app folder alone -- schema validity, contract
conformance, metric presence, the three uploaded config files, dashboard reachability, incident
lifecycle and determinism.

Is one app ready to publish, or are all of them::

    from matrice_analytics.engine.testing import validate_app, validate_apps

    validate_app("./v1.4").ok                        # one app
    print(validate_apps("applications/").report())   # every folder holding an app.yaml

The whole suite, in a host repo's test file::

    from matrice_analytics.engine.testing import GeneratedCheck, suite_checks

    APP = "apps/people_counting"

    @pytest.mark.parametrize("check", suite_checks(APP), ids=lambda check: check.name)
    def test_generated_suite(check: GeneratedCheck) -> None:
        result = check()
        assert result.status != "failed", result.detail()

Or, without pytest::

    matrice-analytics validate apps/people_counting
    matrice-analytics validate --all apps/
    python -m matrice_analytics.engine.testing.generate --describe apps/people_counting

:mod:`matrice_analytics.engine.testing.generate` documents why this is a parametrised
in-process suite rather than generated pytest files, and what that trade gave up.

Nothing here imports ``post_processing`` or ``analytics`` (**PY-20**).
"""

from __future__ import annotations

from matrice_analytics.engine.testing.generate import (
    CHECK_APP_CONFIG,
    CHECK_CONFORMANCE,
    CHECK_DETERMINISM,
    CHECK_INCIDENTS,
    CHECK_METRICS,
    CHECK_NAMES,
    CHECK_REACHABILITY,
    CHECK_SCHEMA,
    DEFAULT_HASH_SEEDS,
    CheckResult,
    FramePlan,
    GeneratedCheck,
    SuiteResult,
    SyntheticFrame,
    SyntheticRun,
    check_app_config_files,
    check_contract_conformance,
    check_dashboard_reachability,
    check_determinism,
    check_incident_lifecycle,
    check_metric_presence,
    check_schema_validity,
    describe_suite,
    frame_plan,
    generate_suite,
    run_synthetic,
    suite_checks,
    synthesise_frames,
    synthetic_stream_info,
)
from matrice_analytics.engine.testing.validate import (
    AppsResult,
    discover_apps,
    validate_app,
    validate_apps,
)

__all__ = [
    # check names
    "CHECK_APP_CONFIG",
    "CHECK_CONFORMANCE",
    "CHECK_DETERMINISM",
    "CHECK_INCIDENTS",
    "CHECK_METRICS",
    "CHECK_NAMES",
    "CHECK_REACHABILITY",
    "CHECK_SCHEMA",
    "DEFAULT_HASH_SEEDS",
    # results
    "AppsResult",
    "CheckResult",
    "GeneratedCheck",
    "SuiteResult",
    # the synthetic input
    "FramePlan",
    "SyntheticFrame",
    "SyntheticRun",
    "frame_plan",
    "run_synthetic",
    "synthesise_frames",
    "synthetic_stream_info",
    # the checks
    "check_app_config_files",
    "check_contract_conformance",
    "check_dashboard_reachability",
    "check_determinism",
    "check_incident_lifecycle",
    "check_metric_presence",
    "check_schema_validity",
    # the suite
    "describe_suite",
    "discover_apps",
    "generate_suite",
    "suite_checks",
    "validate_app",
    "validate_apps",
]
