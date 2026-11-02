"""Tests for classify_outcome function."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.setup.fixloop import ErrorClass, classify_outcome


class TestClassifyOutcomeSuccessOverride:
    """FR-002: Exit codes 0 and 1 always return SUCCESS."""

    def test_exit_code_zero_returns_success(self) -> None:
        result = classify_outcome(None, 0, "error text that would match")
        assert result is ErrorClass.SUCCESS

    def test_exit_code_one_returns_success(self) -> None:
        result = classify_outcome({"error_class": "auth-secret"}, 1, "")
        assert result is ErrorClass.SUCCESS

    def test_exit_code_zero_ignores_report(self) -> None:
        report: dict[str, object] = {"error_class": "missing-dependency"}
        assert classify_outcome(report, 0, "") is ErrorClass.SUCCESS

    def test_exit_code_one_ignores_stdout(self) -> None:
        assert classify_outcome(None, 1, "command not found") is ErrorClass.SUCCESS


class TestClassifyOutcomeReportPrimary:
    """FR-001: Report-primary classification for non-success exit codes."""

    @pytest.mark.parametrize(
        ("error_class_str", "expected"),
        [
            ("success", ErrorClass.SUCCESS),
            ("missing-dependency", ErrorClass.MISSING_DEPENDENCY),
            ("stale-partial-install", ErrorClass.STALE_PARTIAL_INSTALL),
            ("cert-ca-fetch", ErrorClass.CERT_CA_FETCH),
            ("path-profile-not-updated", ErrorClass.PATH_PROFILE_NOT_UPDATED),
            ("skill-injection-perms", ErrorClass.SKILL_INJECTION_PERMS),
            ("transient-network", ErrorClass.TRANSIENT_NETWORK),
            ("auth-secret", ErrorClass.AUTH_SECRET),
            ("unknown", ErrorClass.UNKNOWN),
        ],
    )
    def test_report_maps_to_error_class(self, error_class_str: str, expected: ErrorClass) -> None:
        report: dict[str, object] = {"error_class": error_class_str}
        assert classify_outcome(report, 99, "") is expected

    def test_unrecognized_error_class_falls_through(self) -> None:
        report: dict[str, object] = {"error_class": "not-a-real-class"}
        assert classify_outcome(report, 99, "") is ErrorClass.UNKNOWN


class TestClassifyOutcomeFallbackTriggers:
    """FR-003: Fallback triggers when report is None, empty, or has missing/unrecognized error_class."""

    def test_report_none_triggers_fallback(self) -> None:
        # exit_code 2 → MISSING_DEPENDENCY via _EXIT_CODE_MAP
        assert classify_outcome(None, 2, "") is ErrorClass.MISSING_DEPENDENCY

    def test_report_empty_dict_triggers_fallback(self) -> None:
        assert classify_outcome({}, 2, "") is ErrorClass.MISSING_DEPENDENCY

    def test_report_missing_error_class_field_triggers_fallback(self) -> None:
        report: dict[str, object] = {"other_field": "value"}
        assert classify_outcome(report, 2, "") is ErrorClass.MISSING_DEPENDENCY

    def test_report_non_string_error_class_triggers_fallback(self) -> None:
        report: dict[str, object] = {"error_class": 123}
        assert classify_outcome(report, 2, "") is ErrorClass.MISSING_DEPENDENCY


class TestClassifyOutcomeExitCodeTaxonomy:
    """FR-003 step 1: Exit-code taxonomy mapping."""

    def test_exit_code_2_maps_to_missing_dependency(self) -> None:
        assert classify_outcome(None, 2, "") is ErrorClass.MISSING_DEPENDENCY

    def test_exit_code_3_maps_to_unknown(self) -> None:
        # VERSION_BLOCKED maps to UNKNOWN — falls through to stdout
        assert classify_outcome(None, 3, "") is ErrorClass.UNKNOWN

    def test_exit_code_4_maps_to_unknown(self) -> None:
        assert classify_outcome(None, 4, "") is ErrorClass.UNKNOWN

    def test_exit_code_5_maps_to_unknown(self) -> None:
        assert classify_outcome(None, 5, "") is ErrorClass.UNKNOWN

    def test_exit_code_6_maps_to_unknown(self) -> None:
        assert classify_outcome(None, 6, "") is ErrorClass.UNKNOWN

    def test_unmapped_exit_code_falls_to_stdout(self) -> None:
        # exit code 99 is not in the map → goes to stdout fallback
        assert classify_outcome(None, 99, "command not found") is ErrorClass.MISSING_DEPENDENCY


class TestClassifyOutcomeStdoutFallback:
    """FR-003 step 2: Stdout regex fallback patterns."""

    def test_missing_dependency_pattern(self) -> None:
        assert classify_outcome(None, 99, "Error: command not found") is ErrorClass.MISSING_DEPENDENCY

    def test_missing_dependency_not_installed(self) -> None:
        assert classify_outcome(None, 99, "gh is not installed") is ErrorClass.MISSING_DEPENDENCY

    def test_missing_dependency_missing_dep(self) -> None:
        assert classify_outcome(None, 99, "missing required dependency") is ErrorClass.MISSING_DEPENDENCY

    def test_auth_secret_pattern(self) -> None:
        assert classify_outcome(None, 99, "token is missing or invalid") is ErrorClass.AUTH_SECRET

    def test_auth_secret_credential_expired(self) -> None:
        assert classify_outcome(None, 99, "credential has expired") is ErrorClass.AUTH_SECRET

    def test_cert_ca_fetch_pattern(self) -> None:
        assert classify_outcome(None, 99, "certificate verification failed") is ErrorClass.CERT_CA_FETCH

    def test_cert_ssl_error(self) -> None:
        assert classify_outcome(None, 99, "SSL certificate error") is ErrorClass.CERT_CA_FETCH

    def test_stale_partial_install_pattern(self) -> None:
        assert classify_outcome(None, 99, "stale partial install detected") is ErrorClass.STALE_PARTIAL_INSTALL

    def test_stale_partial_install_corrupted_installation_phrase(self) -> None:
        msg = "Scanning for corrupted installation artefacts..."
        assert classify_outcome(None, 99, msg) is ErrorClass.STALE_PARTIAL_INSTALL

    def test_stale_partial_install_not_matched_with_different_noun(self) -> None:
        msg = "Scanning for corrupted package artefacts..."
        assert classify_outcome(None, 99, msg) is ErrorClass.UNKNOWN

    def test_transient_network_timeout(self) -> None:
        assert classify_outcome(None, 99, "connection timeout occurred") is ErrorClass.TRANSIENT_NETWORK

    def test_transient_network_refused(self) -> None:
        assert classify_outcome(None, 99, "connection refused by server") is ErrorClass.TRANSIENT_NETWORK

    def test_path_profile_pattern(self) -> None:
        assert classify_outcome(None, 99, "PATH not updated after install") is ErrorClass.PATH_PROFILE_NOT_UPDATED

    def test_skill_injection_perms_pattern(self) -> None:
        assert classify_outcome(None, 99, "permission denied for skill injection") is ErrorClass.SKILL_INJECTION_PERMS

    def test_skill_injection_perms_with_copilot_context(self) -> None:
        msg = "Permission denied when injecting Copilot agent skills"
        assert classify_outcome(None, 99, msg) is ErrorClass.SKILL_INJECTION_PERMS

    def test_skill_injection_perms_requires_skill_context(self) -> None:
        msg = "⚠ Permission denied (read-only site-packages?): /path/to/pkg"
        assert classify_outcome(None, 99, msg) is ErrorClass.UNKNOWN

    def test_auth_secret_does_not_match_path_word(self) -> None:
        # "PAT" in "PATH" must not trigger AUTH_SECRET — requires word boundary after token keyword.
        result = classify_outcome(None, 99, "PATH variable is missing")
        assert result is ErrorClass.PATH_PROFILE_NOT_UPDATED

    def test_empty_stdout_returns_unknown(self) -> None:
        assert classify_outcome(None, 99, "") is ErrorClass.UNKNOWN

    def test_unmatched_stdout_returns_unknown(self) -> None:
        assert classify_outcome(None, 99, "some random output") is ErrorClass.UNKNOWN
