"""Tests for the best-effort Detect error check-in fired on scan failure."""

from __future__ import annotations

from unittest import mock
from unittest.mock import patch

import pytest
import typer

from runlayer_cli.commands import scan
from runlayer_cli.scan.config_parser import MCPClientConfig, MCPServerConfig
from runlayer_cli.scan.service import ScanResult, ScanSubmissionResult


def _result_with_one_server() -> ScanResult:
    return ScanResult(
        device_id="d",
        hostname=None,
        os=None,
        os_version=None,
        username=None,
        org_device_id=None,
        scan_duration_ms=0,
        collector_version="test",
        configurations=[
            MCPClientConfig(
                client="cursor",
                servers=[MCPServerConfig(name="s", type="stdio")],
            ),
        ],
    )


def _result_with_no_findings() -> ScanResult:
    return ScanResult(
        device_id="d",
        hostname=None,
        os=None,
        os_version=None,
        username=None,
        org_device_id=None,
        scan_duration_ms=0,
        collector_version="test",
        configurations=[],
    )


def _run_scan_submit_path(*, artifact_lookup_cache: bool = False) -> None:
    scan._run_scan(
        effective_host="h",
        effective_secret="s",
        device_id=None,
        org_device_id=None,
        dry_run=False,
        verbose=False,
        quiet=True,
        no_projects=True,
        project_depth=7,
        project_timeout=60,
        cpu_cores=2,
        max_cpu_percent=50,
        memory_limit_mb=1024,
        username=None,
        detect_agents=False,
        detect_agent_frameworks=False,
        detect_processes=False,
        detect_containers=False,
        detect_disguised_skills=False,
        detect_renamed_plugin_caches=False,
        log_file_path="x",
        artifact_lookup_cache=artifact_lookup_cache,
    )


def test_report_detect_scan_failure_submits_error_checkin() -> None:
    """With creds and not a dry run, a Detect error check-in is fired."""
    with (
        patch.object(scan, "RunlayerClient") as mock_client_cls,
        patch(
            "runlayer_cli.aiwatch_checkin.submit_detect_error_checkin"
        ) as mock_submit,
        patch(
            "runlayer_cli.aiwatch_checkin._make_device_context",
            return_value={"device_id": "d1"},
        ),
    ):
        scan._report_detect_scan_failure(
            effective_host="https://api.example.com",
            effective_secret="secret",
            dry_run=False,
            error_message="scan blew up",
        )

    mock_client_cls.assert_called_once_with(
        hostname="https://api.example.com", secret="secret"
    )
    mock_submit.assert_called_once()
    assert mock_submit.call_args.kwargs["error_message"] == "scan blew up"


def test_report_detect_scan_failure_skips_on_dry_run() -> None:
    with (
        patch.object(scan, "RunlayerClient") as mock_client_cls,
        patch(
            "runlayer_cli.aiwatch_checkin.submit_detect_error_checkin"
        ) as mock_submit,
    ):
        scan._report_detect_scan_failure(
            effective_host="https://api.example.com",
            effective_secret="secret",
            dry_run=True,
            error_message="scan blew up",
        )

    mock_client_cls.assert_not_called()
    mock_submit.assert_not_called()


def test_report_detect_scan_failure_skips_without_credentials() -> None:
    with (
        patch.object(scan, "RunlayerClient") as mock_client_cls,
        patch(
            "runlayer_cli.aiwatch_checkin.submit_detect_error_checkin"
        ) as mock_submit,
    ):
        scan._report_detect_scan_failure(
            effective_host="",
            effective_secret="",
            dry_run=False,
            error_message="scan blew up",
        )

    mock_client_cls.assert_not_called()
    mock_submit.assert_not_called()


def test_report_detect_scan_failure_never_raises() -> None:
    """A check-in failure must not mask the original scan error."""
    with (
        patch.object(scan, "RunlayerClient", side_effect=RuntimeError("client boom")),
        patch(
            "runlayer_cli.aiwatch_checkin.submit_detect_error_checkin"
        ) as mock_submit,
    ):
        scan._report_detect_scan_failure(
            effective_host="https://api.example.com",
            effective_secret="secret",
            dry_run=False,
            error_message="scan blew up",
        )

    mock_submit.assert_not_called()


def test_scan_checkins_run_after_submission() -> None:
    """On the submit path, check-ins fire after submit_scan_results."""
    with (
        patch.object(scan, "scan_all_clients", return_value=_result_with_one_server()),
        patch.object(scan, "RunlayerClient"),
        patch.object(
            scan, "submit_scan_results", return_value=ScanSubmissionResult()
        ) as mock_submit,
        patch("runlayer_cli.aiwatch_checkin.submit_all_scan_checkins") as mock_checkins,
    ):
        manager = mock.Mock()
        manager.attach_mock(mock_submit, "submit")
        manager.attach_mock(mock_checkins, "checkin")

        _run_scan_submit_path()

    call_names = [c[0] for c in manager.mock_calls]
    assert "submit" in call_names
    assert "checkin" in call_names
    assert call_names.index("submit") < call_names.index("checkin")


def test_scan_threads_enabled_artifact_cache_to_submission() -> None:
    cache = mock.Mock()
    client = mock.Mock()
    with (
        patch.object(scan, "scan_all_clients", return_value=_result_with_one_server()),
        patch.object(scan, "RunlayerClient", return_value=client),
        patch.object(scan, "ArtifactCache", return_value=cache) as cache_cls,
        patch.object(
            scan,
            "submit_scan_results",
            return_value=ScanSubmissionResult(),
        ) as mock_submit,
        patch("runlayer_cli.aiwatch_checkin.submit_all_scan_checkins"),
    ):
        _run_scan_submit_path(artifact_lookup_cache=True)

    cache_cls.assert_called_once_with("h", "s")
    mock_submit.assert_called_once_with(
        client,
        mock.ANY,
        artifact_cache=cache,
    )


def test_scan_disables_artifact_cache_in_windows_system_context() -> None:
    client = mock.Mock()
    with (
        patch.object(scan, "scan_all_clients", return_value=_result_with_one_server()),
        patch.object(scan, "RunlayerClient", return_value=client),
        patch.object(scan, "ArtifactCache") as cache_cls,
        patch.object(scan, "is_windows_system_context", return_value=True),
        patch.object(
            scan,
            "submit_scan_results",
            return_value=ScanSubmissionResult(),
        ) as mock_submit,
        patch("runlayer_cli.aiwatch_checkin.submit_all_scan_checkins"),
    ):
        _run_scan_submit_path(artifact_lookup_cache=True)

    cache_cls.assert_not_called()
    mock_submit.assert_called_once_with(client, mock.ANY, artifact_cache=None)


def test_scan_checkins_run_even_when_submission_fails() -> None:
    """A failed submission still fires check-ins before the nonzero exit."""
    with (
        patch.object(scan, "scan_all_clients", return_value=_result_with_one_server()),
        patch.object(scan, "RunlayerClient"),
        patch.object(
            scan,
            "submit_scan_results",
            return_value=ScanSubmissionResult(failed_submissions=["servers"]),
        ),
        patch("runlayer_cli.aiwatch_checkin.submit_all_scan_checkins") as mock_checkins,
    ):
        with pytest.raises(typer.Exit):
            _run_scan_submit_path()

    mock_checkins.assert_called_once()


def test_checkin_failure_does_not_fail_successful_submission() -> None:
    """A raising check-in after a successful submission must not mis-report a
    Detect failure or exit nonzero."""
    with (
        patch.object(scan, "scan_all_clients", return_value=_result_with_one_server()),
        patch.object(scan, "RunlayerClient"),
        patch.object(scan, "submit_scan_results", return_value=ScanSubmissionResult()),
        patch(
            "runlayer_cli.aiwatch_checkin.submit_all_scan_checkins",
            side_effect=RuntimeError("checkin boom"),
        ),
        patch.object(scan, "_report_detect_scan_failure") as mock_fail,
    ):
        # Submission succeeded, so _run_scan returns normally (exit 0) -- the
        # check-in blowing up must not propagate to the failure handler.
        _run_scan_submit_path()

    mock_fail.assert_not_called()


def test_checkin_failure_on_no_findings_path_still_exits_zero() -> None:
    """A raising check-in on the no-findings path must still exit 0, not report
    a Detect failure."""
    with (
        patch.object(scan, "scan_all_clients", return_value=_result_with_no_findings()),
        patch.object(scan, "RunlayerClient"),
        patch(
            "runlayer_cli.aiwatch_checkin.submit_all_scan_checkins",
            side_effect=RuntimeError("checkin boom"),
        ),
        patch.object(scan, "_report_detect_scan_failure") as mock_fail,
    ):
        with pytest.raises(typer.Exit) as exc_info:
            _run_scan_submit_path()

    assert exc_info.value.exit_code == 0
    mock_fail.assert_not_called()


def test_checkin_import_failure_does_not_fail_successful_submission() -> None:
    """A failing *import* inside the best-effort wrapper (not just a raising
    check-in) must be swallowed too -- an ImportError from the aiwatch_checkin
    module must not mis-report a Detect failure for a scan that persisted."""
    with (
        patch.object(scan, "scan_all_clients", return_value=_result_with_one_server()),
        patch.object(scan, "RunlayerClient"),
        patch.object(scan, "submit_scan_results", return_value=ScanSubmissionResult()),
        # A None entry makes ``from runlayer_cli.aiwatch_checkin import ...`` raise
        # ModuleNotFoundError, simulating a broken/absent module at call time.
        patch.dict("sys.modules", {"runlayer_cli.aiwatch_checkin": None}),
        patch.object(scan, "_report_detect_scan_failure") as mock_fail,
    ):
        _run_scan_submit_path()

    mock_fail.assert_not_called()


def test_checkin_import_failure_on_no_findings_path_still_exits_zero() -> None:
    """A failing import on the no-findings path must still exit 0, not report a
    Detect failure."""
    with (
        patch.object(scan, "scan_all_clients", return_value=_result_with_no_findings()),
        patch.object(scan, "RunlayerClient"),
        patch.dict("sys.modules", {"runlayer_cli.aiwatch_checkin": None}),
        patch.object(scan, "_report_detect_scan_failure") as mock_fail,
    ):
        with pytest.raises(typer.Exit) as exc_info:
            _run_scan_submit_path()

    assert exc_info.value.exit_code == 0
    mock_fail.assert_not_called()
