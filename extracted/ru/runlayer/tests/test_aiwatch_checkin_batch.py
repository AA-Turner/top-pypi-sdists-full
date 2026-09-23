"""One batched request per scan tick, sequential fallback for older backends."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from unittest.mock import Mock, patch

import httpx
import pytest

from runlayer_cli import aiwatch_checkin
from runlayer_cli.scan.device import DeviceContext
from runlayer_cli.scan.service import ScanResult, device_context_dict

_DAEMON_DETAIL = {
    "state": "healthy",
    "gate_open": True,
    "supervisor_running": True,
    "probe": "ok",
    "probe_version": "1.2.3",
}
_SCAN_TICK_FEATURES = ["protect", "enforce", "sessions", "daemon", "detect"]


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
        tools=[{"name": "aiwatch", "version": "1.2.3"}],
    )


def _http_status_error(status_code: int) -> httpx.HTTPStatusError:
    request = httpx.Request(
        "POST", "https://runlayer.test/api/v1/ai-watch/check-in/batch"
    )
    response = httpx.Response(status_code, request=request, text="rejected")
    return httpx.HTTPStatusError("batch rejected", request=request, response=response)


@contextmanager
def _scan_tick() -> Iterator[None]:
    """Monitor-mode, sessions-off, healthy-daemon macOS device: five features."""
    with (
        patch.object(
            aiwatch_checkin,
            "read_managed_config",
            return_value={"enforcement": False, "sessions": False},
        ),
        patch.object(aiwatch_checkin, "check_all", return_value=[]),
        patch.object(aiwatch_checkin.sys, "platform", "darwin"),
        patch.object(
            aiwatch_checkin, "_daemon_health_snapshot", return_value=_DAEMON_DETAIL
        ),
        patch.object(aiwatch_checkin, "_hook_host_detail", return_value=None),
        patch.object(aiwatch_checkin.time, "sleep"),
    ):
        yield


def test_device_keys_match_the_context_the_builders_merge() -> None:
    """The fold is defined by subtraction, so the key set must equal what
    ``_base_payload`` merges in: every ``DeviceContext`` key plus ``tools``.
    The backend contract test pins the same set to its request model."""
    assert aiwatch_checkin.BATCH_CHECKIN_DEVICE_KEYS == (
        frozenset(DeviceContext.__annotations__) | {"tools"}
    )


def test_scan_sends_one_batch_when_the_backend_supports_it() -> None:
    client = Mock()
    client.submit_aiwatch_checkin_batch.return_value = {"results": []}
    result = _scan_result()

    with _scan_tick():
        aiwatch_checkin.submit_all_scan_checkins(client, result)

    client.submit_aiwatch_checkin.assert_not_called()
    client.submit_aiwatch_checkin_batch.assert_called_once()
    batch = client.submit_aiwatch_checkin_batch.call_args.args[0]
    assert "features" in batch
    assert set(batch) - {"features"} <= aiwatch_checkin.BATCH_CHECKIN_DEVICE_KEYS
    assert batch["device_id"] == "device-1"
    assert batch["tools"] == result.tools
    features = batch["features"]
    assert [entry["feature"] for entry in features] == _SCAN_TICK_FEATURES
    assert all(
        not (set(entry) & aiwatch_checkin.BATCH_CHECKIN_DEVICE_KEYS)
        for entry in features
    )
    by_feature = {entry["feature"]: entry for entry in features}
    assert by_feature["daemon"]["daemon_detail"] == _DAEMON_DETAIL
    assert by_feature["detect"]["status"] == "ok"
    assert "container_detail" in by_feature["detect"]
    assert "hook_host_detail" in by_feature["detect"]
    assert by_feature["protect"]["status"] == "disabled"


def test_scan_falls_back_to_one_request_per_feature_when_unsupported() -> None:
    client = Mock()
    client.submit_aiwatch_checkin_batch.return_value = {"unsupported": True}
    result = _scan_result()

    with _scan_tick():
        aiwatch_checkin.submit_all_scan_checkins(client, result)

    client.submit_aiwatch_checkin_batch.assert_called_once()
    singles = [call.args[0] for call in client.submit_aiwatch_checkin.call_args_list]
    assert [payload["feature"] for payload in singles] == _SCAN_TICK_FEATURES
    # The batch is a lossless re-fold of the single-form payloads.
    batch = client.submit_aiwatch_checkin_batch.call_args.args[0]
    ctx = device_context_dict(result)
    for payload, entry in zip(singles, batch["features"], strict=True):
        assert payload == {**ctx, "tools": result.tools, **entry}


@pytest.mark.parametrize(
    ("status_code", "sequential_calls"),
    [
        pytest.param(422, len(_SCAN_TICK_FEATURES), id="body_rejected"),
        pytest.param(401, 0, id="credential_rejected"),
        pytest.param(503, 0, id="backend_unavailable"),
    ],
)
def test_batch_http_errors_fall_back_only_when_sequential_can_help(
    status_code: int, sequential_calls: int
) -> None:
    client = Mock()
    client.submit_aiwatch_checkin_batch.side_effect = _http_status_error(status_code)

    with _scan_tick():
        aiwatch_checkin.submit_all_scan_checkins(client, _scan_result())

    client.submit_aiwatch_checkin_batch.assert_called_once()
    assert client.submit_aiwatch_checkin.call_count == sequential_calls


def test_batch_retries_transport_errors_then_gives_up_for_this_tick() -> None:
    client = Mock()
    client.submit_aiwatch_checkin_batch.side_effect = httpx.ConnectError("refused")

    with _scan_tick():
        aiwatch_checkin.submit_all_scan_checkins(client, _scan_result())

    assert client.submit_aiwatch_checkin_batch.call_count == 3
    client.submit_aiwatch_checkin.assert_not_called()


def test_one_failing_builder_does_not_drop_the_other_features() -> None:
    client = Mock()
    client.submit_aiwatch_checkin_batch.return_value = {"results": []}

    with (
        _scan_tick(),
        patch.object(
            aiwatch_checkin,
            "_daemon_health_snapshot",
            side_effect=RuntimeError("probe exploded"),
        ),
    ):
        aiwatch_checkin.submit_all_scan_checkins(client, _scan_result())

    batch = client.submit_aiwatch_checkin_batch.call_args.args[0]
    assert [entry["feature"] for entry in batch["features"]] == [
        "protect",
        "enforce",
        "sessions",
        "detect",
    ]


def test_enroll_path_still_submits_one_request_per_feature() -> None:
    """``submit_validation_checkins`` keeps its single-form contract."""
    client = Mock()

    with _scan_tick():
        aiwatch_checkin.submit_validation_checkins(
            client, ctx=device_context_dict(_scan_result()), tools=[]
        )

    client.submit_aiwatch_checkin_batch.assert_not_called()
    assert client.submit_aiwatch_checkin.call_count == 3
