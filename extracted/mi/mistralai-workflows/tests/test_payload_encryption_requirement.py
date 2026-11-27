import asyncio
import contextlib
from typing import Any
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import httpx
import pytest
from mistralai.extra.workflows.encoding.config import PayloadEncryptionMode
from pydantic import SecretStr

from mistralai.workflows.core.config import config_discovery
from mistralai.workflows.core.config.config import AppConfig, PayloadEncryptionConfig
from mistralai.workflows.core.config.config_discovery import apply_worker_runtime_config
from mistralai.workflows.core.worker import _register_workflow_specs, _worker_heartbeat, run_worker
from mistralai.workflows.exceptions import _TERMINAL_CODES, ErrorCode, WorkflowsException
from mistralai.workflows.protocol.v1.worker import PayloadEncryptionLevel
from mistralai.workflows.protocol.v1.workflow import WorkflowRegistrationRef
from mistralai.workflows.worker_client import models as wc_models

from .utils import create_http_test_worker_client

BASE_WHOAMI: dict[str, Any] = {"scheduler_url": "https://temporal.example.com:7233", "namespace": "customer:workspace"}
MAIN_KEY = SecretStr("00" * 32)
REQUIREMENT_NOT_MET_LABEL = _TERMINAL_CODES[ErrorCode.WORKER_PAYLOAD_ENCRYPTION_REQUIRED]


def _worker_config(mode: PayloadEncryptionMode | None) -> AppConfig:
    """A config of its own, so discovery never mutates the process-wide one."""
    app_config = AppConfig()
    app_config.worker.temporal_payload_encryption = (
        None if mode is None else PayloadEncryptionConfig(mode=mode, main_key=MAIN_KEY)
    )
    return app_config


@pytest.fixture
def whoami(monkeypatch: pytest.MonkeyPatch):
    def _serve(**payload: Any) -> None:
        transport = httpx.MockTransport(lambda _request: httpx.Response(200, json={**BASE_WHOAMI, **payload}))
        client = create_http_test_worker_client(transport)
        monkeypatch.setattr(config_discovery, "get_worker_client", lambda **kwargs: client)

    return _serve


class TestPayloadEncryptionLevel:
    @pytest.mark.parametrize(
        ("level", "required", "satisfied"),
        [
            (PayloadEncryptionLevel.NONE, PayloadEncryptionLevel.NONE, True),
            (PayloadEncryptionLevel.NONE, PayloadEncryptionLevel.PARTIAL, False),
            (PayloadEncryptionLevel.PARTIAL, PayloadEncryptionLevel.PARTIAL, True),
            (PayloadEncryptionLevel.PARTIAL, PayloadEncryptionLevel.FULL, False),
            (PayloadEncryptionLevel.FULL, PayloadEncryptionLevel.PARTIAL, True),
            (PayloadEncryptionLevel.FULL, PayloadEncryptionLevel.FULL, True),
        ],
    )
    def test_satisfies_requirements_up_to_its_own_level(
        self, level: PayloadEncryptionLevel, required: PayloadEncryptionLevel, satisfied: bool
    ) -> None:
        assert level.satisfies(required) is satisfied

    @pytest.mark.parametrize(
        ("mode", "level"),
        [
            (None, PayloadEncryptionLevel.NONE),
            (PayloadEncryptionMode.PARTIAL, PayloadEncryptionLevel.PARTIAL),
            (PayloadEncryptionMode.FULL, PayloadEncryptionLevel.FULL),
        ],
    )
    def test_worker_level_follows_its_encryption_config(
        self, mode: PayloadEncryptionMode | None, level: PayloadEncryptionLevel
    ) -> None:
        assert _worker_config(mode).worker.payload_encryption_level == level


class TestDiscoveredEncryptionRequirement:
    async def test_discovery_alone_does_not_enforce_the_requirement(self, whoami) -> None:
        # Client-only callers, such as a Temporal client factory, discover config without starting a worker.
        whoami(required_payload_encryption_mode="full")

        runtime_config = await apply_worker_runtime_config(config=_worker_config(None))

        assert runtime_config is not None
        assert runtime_config.required_payload_encryption_mode == PayloadEncryptionLevel.FULL

    async def test_worker_below_requirement_exits_with_remediation(self, whoami) -> None:
        whoami(required_payload_encryption_mode="full")

        with (
            patch("mistralai.workflows.core.worker.logger") as worker_logger,
            pytest.raises(SystemExit) as exc_info,
        ):
            await run_worker([], enable_config_discovery=True, config=_worker_config(None))

        assert exc_info.value.code == 1
        remediation, label = worker_logger.error.call_args_list
        assert "TEMPORAL_PAYLOAD_ENCRYPTION__MODE=full" in remediation.kwargs["reason"]
        assert label.args[0] == REQUIREMENT_NOT_MET_LABEL

    async def test_detached_worker_below_requirement_reaches_the_caller(self, whoami) -> None:
        whoami(required_payload_encryption_mode="full")

        with (
            patch("mistralai.workflows.core.worker.logger") as worker_logger,
            pytest.raises(WorkflowsException) as exc_info,
        ):
            await run_worker(
                [], detach=True, enable_config_discovery=True, config=_worker_config(PayloadEncryptionMode.PARTIAL)
            )

        assert exc_info.value.code == ErrorCode.WORKER_PAYLOAD_ENCRYPTION_REQUIRED
        assert "TEMPORAL_PAYLOAD_ENCRYPTION__MODE=full" in exc_info.value.message
        assert worker_logger.error.call_args.args[0] == REQUIREMENT_NOT_MET_LABEL

    @pytest.mark.parametrize(
        ("mode", "whoami_payload"),
        [
            (PayloadEncryptionMode.FULL, {"required_payload_encryption_mode": "partial"}),
            (None, {}),
        ],
        ids=["above-requirement", "server-without-requirement"],
    )
    async def test_worker_meeting_requirement_starts(
        self, whoami, mode: PayloadEncryptionMode | None, whoami_payload: dict[str, Any]
    ) -> None:
        whoami(**whoami_payload)

        task = await run_worker([], detach=True, enable_config_discovery=True, config=_worker_config(mode))

        assert task is not None
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task


class TestReportedEncryptionMode:
    @pytest.mark.parametrize(
        ("mode", "reported"),
        [(None, "none"), (PayloadEncryptionMode.PARTIAL, "partial"), (PayloadEncryptionMode.FULL, "full")],
    )
    async def test_registration_reports_the_configured_mode(
        self, mode: PayloadEncryptionMode | None, reported: str
    ) -> None:
        client = AsyncMock()
        client.register_workflow_definitions_async.return_value = wc_models.WorkflowSpecsRegisterResponse(
            has_conflicts=False
        )

        await _register_workflow_specs(
            client,
            [],
            "dep",
            "worker",
            None,
            payload_encryption_mode=_worker_config(mode).worker.payload_encryption_level,
        )

        assert client.register_workflow_definitions_async.call_args.kwargs["payload_encryption_mode"] == reported

    async def test_heartbeat_reports_the_configured_mode(self) -> None:
        client = AsyncMock()

        async def _stop_after_first_heartbeat(delay: float) -> None:
            if client.heartbeat_async.await_count:
                raise asyncio.CancelledError

        with (
            pytest.raises(asyncio.CancelledError),
            patch("asyncio.sleep", new=_stop_after_first_heartbeat),
        ):
            await _worker_heartbeat(
                worker_client=client,
                workflow_definitions=[],
                workflow_registration_refs=[
                    WorkflowRegistrationRef(workflow_id=uuid4(), workflow_registration_id=uuid4())
                ],
                interval=10,
                deployment_name="dep",
                worker_name="worker",
                payload_encryption_mode=_worker_config(PayloadEncryptionMode.FULL).worker.payload_encryption_level,
            )

        assert client.heartbeat_async.call_args.kwargs["payload_encryption_mode"] == "full"
