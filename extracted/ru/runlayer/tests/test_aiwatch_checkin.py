"""Unit tests for best-effort AI Watch check-ins."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock, patch

import httpx
import pytest
import structlog

from runlayer_cli import aiwatch_checkin
from runlayer_cli.hook_install import Client, ClientStatus, InstalledClient
from runlayer_cli.scan.service import ScanResult
from runlayer_cli.skills.device_sync import SyncReport


def _device_ctx() -> aiwatch_checkin.DeviceContext:
    return {
        "device_id": "device-1",
        "hostname": "host-1",
        "os": "darwin",
        "os_version": "15.0",
        "username": "user-1",
        "org_device_id": None,
        "serial_number": "SERIAL123",
    }


def _scan_result() -> ScanResult:
    return ScanResult(
        device_id="device-1",
        hostname="host-1",
        os="darwin",
        os_version="15.0",
        username="user-1",
        org_device_id=None,
        scan_duration_ms=1,
        collector_version="1.2.3",
        configurations=[],
        serial_number="SERIAL123",
    )


def _unprocessable_checkin_error(
    response_body: str = "",
) -> httpx.HTTPStatusError:
    """Model an old backend rejecting the unknown Protect feature enum."""
    request = httpx.Request("POST", "https://runlayer.test/api/v1/ai-watch/check-in")
    response = httpx.Response(422, request=request, text=response_body)
    return httpx.HTTPStatusError(
        "unprocessable check-in",
        request=request,
        response=response,
    )


@pytest.mark.parametrize("key_hash", ["abc123", None])
def test_submit_llm_routing_checkin_returns_body_and_carries_hash(
    key_hash: str | None,
) -> None:
    client = Mock()
    response = {"device_key_status": "active", "device_key": "k"}
    client.submit_aiwatch_checkin.return_value = response

    result = aiwatch_checkin.submit_llm_routing_checkin(
        client,
        ctx=_device_ctx(),
        tools=[],
        status="ok",
        device_key_hash=key_hash,
    )

    assert result == response
    payload = client.submit_aiwatch_checkin.call_args.args[0]
    assert payload["feature"] == "llm_routing"
    assert payload["status"] == "ok"
    assert "device_key_hash" in payload
    assert payload["device_key_hash"] == key_hash


def test_submit_llm_routing_checkin_rotate_flag() -> None:
    rotating_client = Mock()
    aiwatch_checkin.submit_llm_routing_checkin(
        rotating_client,
        ctx=_device_ctx(),
        tools=[],
        status="ok",
        device_key_hash=None,
        rotate=True,
    )
    rotating_payload = rotating_client.submit_aiwatch_checkin.call_args.args[0]
    assert rotating_payload["rotate"] is True

    default_client = Mock()
    aiwatch_checkin.submit_llm_routing_checkin(
        default_client,
        ctx=_device_ctx(),
        tools=[],
        status="ok",
        device_key_hash="abc123",
    )
    default_payload = default_client.submit_aiwatch_checkin.call_args.args[0]
    assert "rotate" not in default_payload


def test_submit_llm_routing_checkin_returns_none_when_unsupported() -> None:
    client = Mock()
    client.submit_aiwatch_checkin.return_value = {"unsupported": True}

    result = aiwatch_checkin.submit_llm_routing_checkin(
        client,
        ctx=_device_ctx(),
        tools=[],
        status="ok",
        device_key_hash=None,
    )

    assert result is None


def test_submit_llm_routing_checkin_retries_then_returns_none() -> None:
    client = Mock()
    client.submit_aiwatch_checkin.side_effect = httpx.ConnectError("refused")

    with patch.object(aiwatch_checkin.time, "sleep"):
        result = aiwatch_checkin.submit_llm_routing_checkin(
            client,
            ctx=_device_ctx(),
            tools=[],
            status="ok",
            device_key_hash=None,
        )

    assert result is None
    assert client.submit_aiwatch_checkin.call_count == 3


def test_submit_llm_routing_checkin_returns_none_on_http_status_error() -> None:
    client = Mock()
    client.submit_aiwatch_checkin.side_effect = _unprocessable_checkin_error()

    result = aiwatch_checkin.submit_llm_routing_checkin(
        client,
        ctx=_device_ctx(),
        tools=[],
        status="ok",
        device_key_hash=None,
    )

    assert result is None
    client.submit_aiwatch_checkin.assert_called_once()


@pytest.mark.parametrize(
    ("exc", "expected_attempts"),
    [
        pytest.param(httpx.ConnectError("connection refused"), 3, id="transport_error"),
        # SSL failures from a TLS-inspecting proxy surface as bare OSError,
        # not httpx.HTTPError — a best-effort liveness ping must not blow up.
        pytest.param(OSError("SSL: CERTIFICATE_VERIFY_FAILED"), 3, id="os_error"),
        pytest.param(ValueError("invalid json body"), 1, id="value_error"),
    ],
)
def test_submit_detect_checkin_swallows_expected_errors(
    exc: Exception, expected_attempts: int
) -> None:
    client = Mock()
    client.submit_aiwatch_checkin.side_effect = exc

    with (
        patch.object(aiwatch_checkin.time, "sleep"),
        structlog.testing.capture_logs() as logs,
    ):
        aiwatch_checkin.submit_detect_checkin(client, _scan_result())

    assert client.submit_aiwatch_checkin.call_count == expected_attempts
    assert [(log["event"], log["log_level"]) for log in logs] == [
        ("aiwatch_detect_checkin_failed", "warning")
    ]


def test_submit_detect_checkin_logs_rejected_http_status() -> None:
    client = Mock()
    client.submit_aiwatch_checkin.side_effect = _unprocessable_checkin_error(
        '{"detail":"unknown feature: daemon"}'
    )

    with structlog.testing.capture_logs() as logs:
        aiwatch_checkin.submit_detect_checkin(client, _scan_result())

    client.submit_aiwatch_checkin.assert_called_once()
    assert len(logs) == 1
    assert logs[0]["event"] == "aiwatch_checkin_rejected"
    assert logs[0]["log_level"] == "warning"
    assert logs[0]["status_code"] == 422
    assert logs[0]["feature"] == "detect"
    assert logs[0]["response_body"] == '{"detail":"unknown feature: daemon"}'


def test_submit_detect_checkin_retries_transient_network_error() -> None:
    client = Mock()
    client.submit_aiwatch_checkin.side_effect = [
        httpx.ConnectError("connection refused"),
        None,
    ]

    with patch.object(aiwatch_checkin.time, "sleep"):
        aiwatch_checkin.submit_detect_checkin(client, _scan_result())

    assert client.submit_aiwatch_checkin.call_count == 2


@pytest.mark.parametrize(
    (
        "enabled",
        "host_containers_scanned",
        "failure_reason",
        "expected_detail",
    ),
    [
        pytest.param(
            False,
            False,
            None,
            {
                "enabled": False,
                "host_containers_scanned": False,
                "failure_reason": None,
            },
            id="disabled",
        ),
        pytest.param(
            True,
            True,
            None,
            {
                "enabled": True,
                "host_containers_scanned": True,
                "failure_reason": None,
            },
            id="clean",
        ),
        pytest.param(
            True,
            False,
            "Container runtime unavailable or access denied",
            {
                "enabled": True,
                "host_containers_scanned": False,
                "failure_reason": "Container runtime unavailable or access denied",
            },
            id="unavailable",
        ),
        pytest.param(
            True,
            False,
            None,
            {
                "enabled": True,
                "host_containers_scanned": False,
                "failure_reason": "Container inventory incomplete",
            },
            id="failed_without_reason",
        ),
        pytest.param(
            True,
            False,
            "\x00 \t\n",
            {
                "enabled": True,
                "host_containers_scanned": False,
                "failure_reason": "Container inventory incomplete",
            },
            id="failed_with_unprintable_reason",
        ),
    ],
)
def test_submit_detect_checkin_includes_container_detail(
    enabled: bool,
    host_containers_scanned: bool,
    failure_reason: str | None,
    expected_detail: dict[str, object],
) -> None:
    client = Mock()
    result = _scan_result()
    result.container_scan_requested = enabled
    result.containers_scanned = host_containers_scanned
    result.container_scan_error = failure_reason

    aiwatch_checkin.submit_detect_checkin(client, result)

    payload = client.submit_aiwatch_checkin.call_args.args[0]
    assert payload["status"] == "ok"
    assert payload["container_detail"] == expected_detail


def test_submit_detect_checkin_swallows_persistent_failure_and_warns() -> None:
    client = Mock()
    client.submit_aiwatch_checkin.side_effect = httpx.ConnectError("connection refused")

    with (
        patch.object(aiwatch_checkin.time, "sleep") as mock_sleep,
        structlog.testing.capture_logs() as logs,
    ):
        aiwatch_checkin.submit_detect_checkin(client, _scan_result())

    assert client.submit_aiwatch_checkin.call_count == 3
    assert mock_sleep.call_count == 2
    assert [(log["event"], log["log_level"]) for log in logs] == [
        ("aiwatch_detect_checkin_failed", "warning")
    ]


def test_submit_enforce_checkin_reports_disabled_when_enforcement_off() -> None:
    """Monitoring-only fleet (Enforcement=false, Sessions=true) records sessions,
    never runs enforce hook validation — but now reports Enforce ``disabled``
    (not silence) so the backend can tell "intentionally off" from "never ran"."""
    client = Mock()

    with (
        patch.object(
            aiwatch_checkin,
            "read_managed_config",
            return_value={"enforcement": False, "sessions": True},
        ),
        patch.object(aiwatch_checkin, "check_all") as mock_check_all,
    ):
        aiwatch_checkin.submit_enforce_validation_checkin(
            client, ctx=_device_ctx(), tools=[]
        )

    mock_check_all.assert_not_called()
    calls = [call.args[0] for call in client.submit_aiwatch_checkin.call_args_list]
    assert [(payload["feature"], payload["status"]) for payload in calls] == [
        ("protect", "disabled"),
        ("enforce", "disabled"),
    ]


@pytest.mark.parametrize(
    ("results", "expected_status"),
    [
        pytest.param(
            [InstalledClient(Client.CURSOR, ClientStatus.DRIFTED, "hook mismatch")],
            "drifted",
            id="drifted",
        ),
        pytest.param(
            [InstalledClient(Client.CURSOR, ClientStatus.MISSING, "hook absent")],
            "drifted",
            id="missing",
        ),
        pytest.param(
            # Multiple hook problems still collapse to one drifted feature status.
            [
                InstalledClient(Client.CURSOR, ClientStatus.MISSING),
                InstalledClient(Client.CLAUDE_CODE, ClientStatus.DRIFTED),
            ],
            "drifted",
            id="multiple_problems",
        ),
        pytest.param(
            # OK + not-installed clients are not problems -> ok.
            [
                InstalledClient(Client.CURSOR, ClientStatus.OK),
                InstalledClient(Client.CODEX, ClientStatus.CLIENT_NOT_INSTALLED),
            ],
            "ok",
            id="ok",
        ),
    ],
)
def test_submit_enforce_checkin_classifies_hook_validation(
    results: list[InstalledClient], expected_status: str
) -> None:
    """Any installed-client hook problem reports drifted; otherwise ok."""
    client = Mock()

    with (
        patch.object(
            aiwatch_checkin,
            "read_managed_config",
            return_value={"enforcement": True},
        ),
        patch.object(aiwatch_checkin, "check_all", return_value=results),
    ):
        aiwatch_checkin.submit_enforce_validation_checkin(
            client, ctx=_device_ctx(), tools=[]
        )

    assert client.submit_aiwatch_checkin.call_count == 2
    disabled, payload = [
        call.args[0] for call in client.submit_aiwatch_checkin.call_args_list
    ]
    assert (disabled["feature"], disabled["status"]) == ("protect", "disabled")
    assert payload["feature"] == "enforce"
    assert payload["status"] == expected_status
    if expected_status == "ok":
        assert "error_message" not in payload
    else:
        assert payload["error_message"]


def test_submit_enforce_checkin_reports_feature_enforce_when_enabled() -> None:
    client = Mock()

    with (
        patch.object(
            aiwatch_checkin,
            "read_managed_config",
            return_value={"enforcement": True},
        ),
        patch.object(aiwatch_checkin, "check_all", return_value=[]) as mock_check_all,
    ):
        aiwatch_checkin.submit_enforce_validation_checkin(
            client, ctx=_device_ctx(), tools=[]
        )

    mock_check_all.assert_called_once()
    assert client.submit_aiwatch_checkin.call_count == 2
    disabled, payload = [
        call.args[0] for call in client.submit_aiwatch_checkin.call_args_list
    ]
    assert (disabled["feature"], disabled["status"]) == ("protect", "disabled")
    assert payload["feature"] == "enforce"
    assert payload["status"] == "ok"


def test_submit_enforce_checkin_reports_distinct_protect_hook_health() -> None:
    """Protect hook health must not make full Enforce appear active."""
    client = Mock()

    with (
        patch.object(
            aiwatch_checkin,
            "read_managed_config",
            return_value={"mode": "protect", "sessions": False},
        ),
        patch.object(aiwatch_checkin, "check_all", return_value=[]) as mock_check_all,
    ):
        aiwatch_checkin.submit_enforce_validation_checkin(
            client, ctx=_device_ctx(), tools=[]
        )

    mock_check_all.assert_called_once_with(
        scope=aiwatch_checkin.InstallScope.MDM,
        include_pipeline=False,
    )
    calls = [call.args[0] for call in client.submit_aiwatch_checkin.call_args_list]
    assert [(payload["feature"], payload["status"]) for payload in calls] == [
        ("enforce", "disabled"),
        ("protect", "ok"),
    ]


def test_old_backend_rejecting_protect_does_not_suppress_legacy_enforce_checkin() -> (
    None
):
    """A pre-Protect backend 422s that enum but still receives Enforce state."""
    client = Mock()
    client.submit_aiwatch_checkin.side_effect = [
        _unprocessable_checkin_error(),
        {},
    ]

    with (
        patch.object(
            aiwatch_checkin,
            "read_managed_config",
            return_value={"mode": "monitor", "sessions": True},
        ),
        patch.object(aiwatch_checkin, "check_all") as mock_check_all,
    ):
        aiwatch_checkin.submit_enforce_validation_checkin(
            client, ctx=_device_ctx(), tools=[]
        )

    mock_check_all.assert_not_called()
    calls = [call.args[0] for call in client.submit_aiwatch_checkin.call_args_list]
    assert [(payload["feature"], payload["status"]) for payload in calls] == [
        ("protect", "disabled"),
        ("enforce", "disabled"),
    ]


def test_old_backend_rejecting_protect_does_not_fail_protect_checkin() -> None:
    """Protect behavior stays live while its new liveness row is unsupported."""
    client = Mock()
    client.submit_aiwatch_checkin.side_effect = [
        {},
        _unprocessable_checkin_error(),
    ]

    with (
        patch.object(
            aiwatch_checkin,
            "read_managed_config",
            return_value={"mode": "protect", "sessions": False},
        ),
        patch.object(aiwatch_checkin, "check_all", return_value=[]),
    ):
        aiwatch_checkin.submit_enforce_validation_checkin(
            client, ctx=_device_ctx(), tools=[]
        )

    calls = [call.args[0] for call in client.submit_aiwatch_checkin.call_args_list]
    assert [(payload["feature"], payload["status"]) for payload in calls] == [
        ("enforce", "disabled"),
        ("protect", "ok"),
    ]


def test_submit_sessions_checkin_reports_disabled_when_sessions_off() -> None:
    client = Mock()

    with (
        patch.object(aiwatch_checkin, "read_managed_config", return_value={}),
        patch.object(aiwatch_checkin, "resolve_include_pipeline", return_value=False),
        patch.object(aiwatch_checkin, "check_all") as mock_check_all,
    ):
        aiwatch_checkin.submit_sessions_validation_checkin(
            client, ctx=_device_ctx(), tools=[]
        )

    mock_check_all.assert_not_called()
    client.submit_aiwatch_checkin.assert_called_once()
    payload = client.submit_aiwatch_checkin.call_args.args[0]
    assert payload["feature"] == "sessions"
    assert payload["status"] == "disabled"


def test_submit_sessions_checkin_reports_feature_sessions() -> None:
    client = Mock()

    with (
        patch.object(aiwatch_checkin, "read_managed_config", return_value={}),
        patch.object(aiwatch_checkin, "resolve_include_pipeline", return_value=True),
        patch.object(aiwatch_checkin, "check_all", return_value=[]) as mock_check_all,
    ):
        aiwatch_checkin.submit_sessions_validation_checkin(
            client, ctx=_device_ctx(), tools=[]
        )

    # Sessions forces the full event/session pipeline into the verdict.
    assert mock_check_all.call_args.kwargs["include_pipeline"] is True
    client.submit_aiwatch_checkin.assert_called_once()
    payload = client.submit_aiwatch_checkin.call_args.args[0]
    assert payload["feature"] == "sessions"
    assert payload["status"] == "ok"


@pytest.mark.parametrize(
    ("exc", "expected_attempts"),
    [
        pytest.param(httpx.ConnectError("connection refused"), 3, id="httpx_error"),
        pytest.param(OSError("SSL: CERTIFICATE_VERIFY_FAILED"), 3, id="os_error"),
        pytest.param(ValueError("invalid json body"), 1, id="value_error"),
    ],
)
def test_submit_sessions_checkin_swallows_expected_errors(
    exc: Exception, expected_attempts: int
) -> None:
    client = Mock()
    client.submit_aiwatch_checkin.side_effect = exc

    with (
        patch.object(aiwatch_checkin, "read_managed_config", return_value={}),
        patch.object(aiwatch_checkin, "resolve_include_pipeline", return_value=True),
        patch.object(aiwatch_checkin, "check_all", return_value=[]),
        patch.object(aiwatch_checkin.time, "sleep"),
    ):
        aiwatch_checkin.submit_sessions_validation_checkin(
            client, ctx=_device_ctx(), tools=[]
        )

    assert client.submit_aiwatch_checkin.call_count == expected_attempts


def test_submit_validation_checkins_runs_both() -> None:
    client = Mock()
    ctx = _device_ctx()

    with (
        patch.object(
            aiwatch_checkin, "submit_enforce_validation_checkin"
        ) as mock_enforce,
        patch.object(
            aiwatch_checkin, "submit_sessions_validation_checkin"
        ) as mock_sessions,
    ):
        aiwatch_checkin.submit_validation_checkins(client, ctx=ctx, tools=[])

    mock_enforce.assert_called_once_with(client, ctx=ctx, tools=[])
    mock_sessions.assert_called_once_with(client, ctx=ctx, tools=[])


def test_submit_sessions_checkin_reports_drifted() -> None:
    """The Sessions path also classifies hook drift as ``drifted``."""
    client = Mock()

    with (
        patch.object(aiwatch_checkin, "read_managed_config", return_value={}),
        patch.object(aiwatch_checkin, "resolve_include_pipeline", return_value=True),
        patch.object(
            aiwatch_checkin,
            "check_all",
            return_value=[
                InstalledClient(Client.CLAUDE_CODE, ClientStatus.DRIFTED, "drift")
            ],
        ),
    ):
        aiwatch_checkin.submit_sessions_validation_checkin(
            client, ctx=_device_ctx(), tools=[]
        )

    payload = client.submit_aiwatch_checkin.call_args.args[0]
    assert payload["feature"] == "sessions"
    assert payload["status"] == "drifted"
    assert payload["error_message"]


def test_submit_detect_error_checkin_reports_error() -> None:
    """Detect scan failures report a Detect error (not silence)."""
    client = Mock()

    aiwatch_checkin.submit_detect_error_checkin(
        client, ctx=_device_ctx(), error_message="scan blew up"
    )

    client.submit_aiwatch_checkin.assert_called_once()
    payload = client.submit_aiwatch_checkin.call_args.args[0]
    assert payload["feature"] == "detect"
    assert payload["status"] == "error"
    assert payload["error_message"] == "scan blew up"


@pytest.mark.parametrize(
    ("exc", "expected_attempts"),
    [
        pytest.param(httpx.ConnectError("connection refused"), 3, id="httpx_error"),
        pytest.param(OSError("SSL: CERTIFICATE_VERIFY_FAILED"), 3, id="os_error"),
        pytest.param(ValueError("invalid json body"), 1, id="value_error"),
    ],
)
def test_submit_detect_error_checkin_swallows_expected_errors(
    exc: Exception, expected_attempts: int
) -> None:
    client = Mock()
    client.submit_aiwatch_checkin.side_effect = exc

    with patch.object(aiwatch_checkin.time, "sleep"):
        aiwatch_checkin.submit_detect_error_checkin(
            client, ctx=_device_ctx(), error_message="scan blew up"
        )

    assert client.submit_aiwatch_checkin.call_count == expected_attempts


def test_submit_validation_checkins_isolates_failures() -> None:
    # An unexpected blow-up in Enforce (e.g. corrupt MDM plist) must not stop
    # the Sessions check-in or propagate to the caller.
    client = Mock()

    with (
        patch.object(
            aiwatch_checkin,
            "submit_enforce_validation_checkin",
            side_effect=RuntimeError("corrupt MDM plist"),
        ) as mock_enforce,
        patch.object(
            aiwatch_checkin, "submit_sessions_validation_checkin"
        ) as mock_sessions,
    ):
        aiwatch_checkin.submit_validation_checkins(client, ctx=_device_ctx(), tools=[])

    mock_enforce.assert_called_once()
    mock_sessions.assert_called_once()


def test_skill_sync_checkin_clean_report_is_ok() -> None:
    client = Mock()
    report = SyncReport(
        installed=["a"], updated=["b"], restored=["r"], up_to_date=["c", "d"]
    )

    aiwatch_checkin.submit_skill_sync_checkin(
        client, ctx=_device_ctx(), tools=[], report=report
    )

    payload = client.submit_aiwatch_checkin.call_args.args[0]
    assert payload["feature"] == "skill_sync"
    # Restores are normal enforcement, not drift or failure.
    assert payload["status"] == "ok"
    assert "error_message" not in payload
    assert payload["sync_detail"] == {
        "installed": ["a"],
        "updated": ["b"],
        "removed": [],
        "restored": ["r"],
        "skipped": [],
        "errors": [],
        "up_to_date_count": 2,
    }
    assert payload["agent_version"]
    assert payload["serial_number"] == "SERIAL123"


def test_skill_sync_checkin_errors_report_error_with_joined_message() -> None:
    client = Mock()
    report = SyncReport(errors=["boom one", "boom two"], skipped=["also drifted"])

    aiwatch_checkin.submit_skill_sync_checkin(
        client, ctx=_device_ctx(), tools=[], report=report
    )

    payload = client.submit_aiwatch_checkin.call_args.args[0]
    assert payload["status"] == "error"
    assert payload["error_message"] == "boom one; boom two"


def test_skill_sync_checkin_skips_report_drifted() -> None:
    client = Mock()
    report = SyncReport(up_to_date=["kept"], skipped=["user dir squats managed name"])

    aiwatch_checkin.submit_skill_sync_checkin(
        client, ctx=_device_ctx(), tools=[], report=report
    )

    payload = client.submit_aiwatch_checkin.call_args.args[0]
    assert payload["status"] == "drifted"
    assert payload["error_message"] == "user dir squats managed name"


def test_skill_sync_checkin_error_message_capped_at_500() -> None:
    client = Mock()
    report = SyncReport(errors=["x" * 400, "y" * 400])

    aiwatch_checkin.submit_skill_sync_checkin(
        client, ctx=_device_ctx(), tools=[], report=report
    )

    payload = client.submit_aiwatch_checkin.call_args.args[0]
    assert len(payload["error_message"]) == 500


def test_skill_sync_checkin_caps_detail_items_and_lengths() -> None:
    client = Mock()
    report = SyncReport(
        installed=[f"skill-{i}-" + "z" * 300 for i in range(51)],
        restored=[f"restored-{i}-" + "w" * 300 for i in range(51)],
        up_to_date=["a", "b", "c"],
    )

    aiwatch_checkin.submit_skill_sync_checkin(
        client, ctx=_device_ctx(), tools=[], report=report
    )

    detail = client.submit_aiwatch_checkin.call_args.args[0]["sync_detail"]
    assert len(detail["installed"]) == 50
    assert all(len(item) == 200 for item in detail["installed"])
    assert len(detail["restored"]) == 50
    assert all(len(item) == 200 for item in detail["restored"])
    assert detail["up_to_date_count"] == 3


def test_skill_sync_disabled_checkin() -> None:
    client = Mock()

    aiwatch_checkin.submit_skill_sync_disabled_checkin(
        client, ctx=_device_ctx(), tools=[]
    )

    client.submit_aiwatch_checkin.assert_called_once()
    payload = client.submit_aiwatch_checkin.call_args.args[0]
    assert payload["feature"] == "skill_sync"
    assert payload["status"] == "disabled"


@pytest.mark.parametrize(
    ("exc", "expected_attempts"),
    [
        pytest.param(httpx.ConnectError("connection refused"), 3, id="httpx_error"),
        pytest.param(OSError("SSL: CERTIFICATE_VERIFY_FAILED"), 3, id="os_error"),
        pytest.param(ValueError("invalid json body"), 1, id="value_error"),
    ],
)
def test_skill_sync_checkin_swallows_expected_errors(
    exc: Exception, expected_attempts: int
) -> None:
    client = Mock()
    client.submit_aiwatch_checkin.side_effect = exc

    with patch.object(aiwatch_checkin.time, "sleep"):
        aiwatch_checkin.submit_skill_sync_checkin(
            client, ctx=_device_ctx(), tools=[], report=SyncReport()
        )

    assert client.submit_aiwatch_checkin.call_count == expected_attempts


def test_skill_sync_checkin_retries_transient_network_error() -> None:
    client = Mock()
    client.submit_aiwatch_checkin.side_effect = [
        httpx.ConnectError("connection refused"),
        None,
    ]
    report = SyncReport(installed=["managed-skill"])

    with patch.object(aiwatch_checkin.time, "sleep"):
        aiwatch_checkin.submit_skill_sync_checkin(
            client, ctx=_device_ctx(), tools=[], report=report
        )

    assert client.submit_aiwatch_checkin.call_count == 2
    payloads = [call.args[0] for call in client.submit_aiwatch_checkin.call_args_list]
    assert payloads[0] == payloads[1]
    assert payloads[1]["sync_detail"]["installed"] == ["managed-skill"]


def test_submit_daemon_checkin_stays_silent_for_windows_system() -> None:
    client = Mock()

    with (
        patch.object(aiwatch_checkin.sys, "platform", "win32"),
        patch.object(
            aiwatch_checkin,
            "is_running_as_system",
            return_value=True,
        ) as mock_is_system,
        patch.object(
            aiwatch_checkin, "_daemon_health_snapshot"
        ) as mock_health_snapshot,
    ):
        aiwatch_checkin.submit_daemon_checkin(client, ctx=_device_ctx(), tools=[])

    mock_is_system.assert_called_once_with()
    mock_health_snapshot.assert_not_called()
    client.submit_aiwatch_checkin.assert_not_called()


def test_submit_daemon_checkin_reports_for_windows_non_system() -> None:
    client = Mock()
    detail = {"state": "healthy"}

    with (
        patch.object(aiwatch_checkin.sys, "platform", "win32"),
        patch.object(
            aiwatch_checkin, "is_running_as_system", return_value=False
        ) as mock_is_system,
        patch.object(
            aiwatch_checkin, "_daemon_health_snapshot", return_value=detail
        ) as mock_health_snapshot,
    ):
        aiwatch_checkin.submit_daemon_checkin(client, ctx=_device_ctx(), tools=[])

    mock_is_system.assert_called_once_with()
    mock_health_snapshot.assert_called_once_with()
    client.submit_aiwatch_checkin.assert_called_once()
    payload = client.submit_aiwatch_checkin.call_args.args[0]
    assert payload["feature"] == "daemon"
    assert payload["status"] == "ok"
    assert payload["daemon_detail"] == detail


def test_submit_daemon_checkin_logs_rejected_http_status() -> None:
    client = Mock()
    client.submit_aiwatch_checkin.side_effect = _unprocessable_checkin_error(
        '{"detail":"unknown feature: daemon"}'
    )

    with (
        patch.object(aiwatch_checkin.sys, "platform", "darwin"),
        patch.object(
            aiwatch_checkin,
            "_daemon_health_snapshot",
            return_value={"state": "healthy"},
        ),
        structlog.testing.capture_logs() as logs,
    ):
        aiwatch_checkin.submit_daemon_checkin(client, ctx=_device_ctx(), tools=[])

    client.submit_aiwatch_checkin.assert_called_once()
    assert len(logs) == 1
    assert logs[0]["event"] == "aiwatch_checkin_rejected"
    assert logs[0]["log_level"] == "warning"
    assert logs[0]["status_code"] == 422
    assert logs[0]["feature"] == "daemon"


def test_make_device_context_includes_serial_number() -> None:
    """The scan-less check-in context carries the collected hardware serial."""
    with (
        patch.object(
            aiwatch_checkin,
            "get_device_metadata",
            return_value={
                "hostname": "host-1",
                "os": "darwin",
                "os_version": "15.0",
                "username": "alice",
                "serial_number": "C02XYZ123ABC",
            },
        ),
        patch.object(
            aiwatch_checkin, "get_or_create_device_id", return_value="device-uuid"
        ),
    ):
        ctx = aiwatch_checkin._make_device_context()

    assert ctx["serial_number"] == "C02XYZ123ABC"


def test_make_device_context_uses_console_user_for_windows_system() -> None:
    """Scheduled-task check-ins must not create a SYSTEM-attributed device user."""
    with (
        patch.object(
            aiwatch_checkin,
            "get_device_metadata",
            return_value={
                "hostname": "DESKTOP-1",
                "os": "windows",
                "os_version": "11",
                "username": "SYSTEM",
                "serial_number": "SERIAL-1",
            },
        ),
        patch.object(aiwatch_checkin, "get_or_create_device_id", return_value="dev-1"),
        patch(
            "runlayer_cli.hook_install.console_user.find_console_user_home",
            return_value=Path("C:/Users/alex"),
        ),
    ):
        ctx = aiwatch_checkin._make_device_context()

    assert ctx["username"] == "alex"


@pytest.mark.parametrize(
    ("os_name", "service_username"),
    [("windows", "SYSTEM"), ("darwin", "root")],
)
def test_make_device_context_omits_unresolved_service_user(
    os_name: str, service_username: str
) -> None:
    with (
        patch.object(
            aiwatch_checkin,
            "get_device_metadata",
            return_value={
                "hostname": "host-1",
                "os": os_name,
                "os_version": "1",
                "username": service_username,
                "serial_number": "SERIAL-1",
            },
        ),
        patch.object(aiwatch_checkin, "get_or_create_device_id", return_value="dev-1"),
        patch(
            "runlayer_cli.hook_install.console_user.find_console_user_home",
            return_value=None,
        ),
    ):
        ctx = aiwatch_checkin._make_device_context()

    assert ctx["username"] is None


def test_detect_checkin_payload_carries_serial_number() -> None:
    """serial_number rides the check-in payload (via _base_payload's **ctx)."""
    client = Mock()

    aiwatch_checkin.submit_detect_checkin(client, _scan_result())

    payload = client.submit_aiwatch_checkin.call_args.args[0]
    assert payload["serial_number"] == "SERIAL123"


_HOOK_HOST_DETAIL = {
    "user_host": "https://staging.example.com",
    "managed_host": "https://prod.example.com",
    "last_seen_at": "2026-09-16T12:00:00+00:00",
}


def _managed_client() -> Mock:
    """Check-in client pointed at the marker's managed host (the scan default)."""
    client = Mock()
    client.base_url = _HOOK_HOST_DETAIL["managed_host"]
    return client


def test_detect_checkin_carries_hook_host_detail_from_marker() -> None:
    client = _managed_client()
    with patch(
        "runlayer_cli.hook.host_override.read_marker", return_value=_HOOK_HOST_DETAIL
    ):
        aiwatch_checkin.submit_detect_checkin(client, _scan_result())

    payload = client.submit_aiwatch_checkin.call_args.args[0]
    assert payload["hook_host_detail"] == _HOOK_HOST_DETAIL


def test_detect_checkin_tolerates_trailing_slash_on_destination() -> None:
    client = _managed_client()
    client.base_url = _HOOK_HOST_DETAIL["managed_host"] + "/"
    with patch(
        "runlayer_cli.hook.host_override.read_marker", return_value=_HOOK_HOST_DETAIL
    ):
        aiwatch_checkin.submit_detect_checkin(client, _scan_result())

    payload = client.submit_aiwatch_checkin.call_args.args[0]
    assert payload["hook_host_detail"] == _HOOK_HOST_DETAIL


def test_detect_checkin_withholds_hook_host_detail_from_other_destination() -> None:
    """An explicit ``--host`` / ``RUNLAYER_HOST`` can still send the scan
    check-in elsewhere; the marker describes hooks bound for the managed host,
    so a different destination (e.g. the user's own tenant) must not get it."""
    client = Mock()
    client.base_url = _HOOK_HOST_DETAIL["user_host"]
    with patch(
        "runlayer_cli.hook.host_override.read_marker", return_value=_HOOK_HOST_DETAIL
    ):
        aiwatch_checkin.submit_detect_checkin(client, _scan_result())

    payload = client.submit_aiwatch_checkin.call_args.args[0]
    assert "hook_host_detail" in payload
    assert payload["hook_host_detail"] is None


def test_detect_checkin_sends_null_hook_host_detail_without_marker() -> None:
    """Explicit ``None`` so the backend clears a stale tenant-side record."""
    client = _managed_client()
    with patch("runlayer_cli.hook.host_override.read_marker", return_value=None):
        aiwatch_checkin.submit_detect_checkin(client, _scan_result())

    payload = client.submit_aiwatch_checkin.call_args.args[0]
    assert "hook_host_detail" in payload
    assert payload["hook_host_detail"] is None


def test_detect_error_checkin_carries_hook_host_detail() -> None:
    """The marker is independent of scan outcome: a failed scan must not
    clear the tenant-side record (the backend rewrites it on every Detect
    check-in, ``None`` included)."""
    client = _managed_client()
    with patch(
        "runlayer_cli.hook.host_override.read_marker", return_value=_HOOK_HOST_DETAIL
    ):
        aiwatch_checkin.submit_detect_error_checkin(
            client, ctx=_device_ctx(), error_message="scan blew up"
        )

    payload = client.submit_aiwatch_checkin.call_args.args[0]
    assert payload["status"] == "error"
    assert payload["hook_host_detail"] == _HOOK_HOST_DETAIL


def test_non_detect_checkins_do_not_carry_hook_host_detail() -> None:
    """Only the Detect carrier reports the marker."""
    client = Mock()
    with patch(
        "runlayer_cli.hook.host_override.read_marker", return_value=_HOOK_HOST_DETAIL
    ):
        aiwatch_checkin._submit_simple_checkin(
            client,
            feature="enforce",
            status="disabled",
            ctx=_device_ctx(),
            tools=[],
            log_event="x",
        )

    payload = client.submit_aiwatch_checkin.call_args.args[0]
    assert "hook_host_detail" not in payload
