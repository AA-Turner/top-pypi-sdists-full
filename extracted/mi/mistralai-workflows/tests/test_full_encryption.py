import base64
import contextlib
import json
from collections.abc import AsyncIterator, Sequence
from typing import Any

import pytest
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from mistralai.extra.workflows.encoding.config import PayloadEncryptionMode
from pydantic import SecretStr
from temporalio.api.history.v1 import History
from temporalio.client import WorkflowFailureError
from temporalio.converter import DataConverter
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.core.config.config import PayloadEncryptionConfig, WorkerConfig, config
from mistralai.workflows.core.temporal.context_handler_interceptor import ContextHandlerInterceptor
from mistralai.workflows.core.temporal.payload_converter import MistralWorkflowsPayloadConverter
from mistralai.workflows.core.tracing._temporal_tracing_interceptor import TraceDataSerializer
from mistralai.workflows.core.worker import _build_worker_payload_encoding
from mistralai.workflows.models import EncodedPayloadOptions
from mistralai.workflows.protocol.v1.events import (
    BaseCustomTaskAttributes,
    JSONPatchPayload,
    JSONPayload,
    WorkflowEvent,
    WorkflowEventType,
)
from mistralai.workflows.testing import create_capturing_mock_events_client, create_test_worker_with_events

from .fixtures_full_encryption import (
    PUBLIC,
    SECRET,
    FailureInput,
    FailureWorkflow,
    TaskFailureWorkflow,
    TaskWorkflow,
    WorkflowFailureWorkflow,
    fail,
    with_task,
)

TEST_MAIN_KEY = SecretStr(AESGCM.generate_key(bit_length=128).hex())
TASK_QUEUE = "test-task-queue"

FULL = PayloadEncryptionConfig(mode=PayloadEncryptionMode.FULL, main_key=TEST_MAIN_KEY)
FULL_WITH_PARTIAL_CUSTOM_EVENTS = PayloadEncryptionConfig(
    mode=PayloadEncryptionMode.FULL, custom_event_mode=PayloadEncryptionMode.PARTIAL, main_key=TEST_MAIN_KEY
)
PARTIAL = PayloadEncryptionConfig(mode=PayloadEncryptionMode.PARTIAL, main_key=TEST_MAIN_KEY)


def _events_containing(history: History, text: str) -> list[str]:
    return [str(e.event_type) for e in history.events if text.encode() in e.SerializeToString()]


def _event_payloads(event: WorkflowEvent) -> list[JSONPayload | JSONPatchPayload]:
    attributes = event.attributes
    if attributes is None:
        return []
    return [
        value
        for name in type(attributes).model_fields
        if isinstance(value := getattr(attributes, name), (JSONPayload, JSONPatchPayload))
    ]


def _keyless_view(payload: JSONPayload | JSONPatchPayload) -> str:
    """What a reader without the key sees: partially encrypted values are only base64-encoded."""
    if EncodedPayloadOptions.PARTIALLY_ENCRYPTED in (payload.encoding_options or []) and isinstance(payload.value, str):
        return base64.b64decode(payload.value).decode()
    return json.dumps(payload.model_dump(mode="json")["value"])


def _error_chain(error: BaseException | None) -> str:
    messages = []
    while error is not None:
        messages.append(str(error))
        error = error.__cause__
    return " | ".join(messages)


def _failure_messages(events: list[WorkflowEvent]) -> list[str]:
    return [
        failure.message
        for event in events
        if event.attributes is not None and (failure := getattr(event.attributes, "failure", None)) is not None
    ]


@contextlib.asynccontextmanager
async def _run_encrypted_worker(
    encryption_config: PayloadEncryptionConfig,
    captured_events: list[Any],
    workflows: Sequence[type],
    activities: Sequence[Any],
) -> AsyncIterator[WorkflowEnvironment]:
    """Run a worker wired like production: payload codec, failure converter, event encoder and worker config."""
    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.setattr(config.worker, "temporal_payload_encryption", encryption_config)
        # The trace encoder is cached on first use; keep this config's encoder out of other tests.
        monkeypatch.setattr(TraceDataSerializer, "_trace_encoder", None)
        payload_encoding = _build_worker_payload_encoding(config.worker)
        data_converter = DataConverter(
            payload_converter_class=MistralWorkflowsPayloadConverter,
            payload_codec=payload_encoding.payload_codec,
            failure_converter_class=payload_encoding.failure_converter,
        )
        async with (
            await WorkflowEnvironment.start_time_skipping(data_converter=data_converter) as env,
            EventContext(
                create_capturing_mock_events_client(captured_events),
                payload_encoder=payload_encoding.event_payload_encoder,
                custom_event_payload_encoder=payload_encoding.custom_event_payload_encoder,
            ),
            create_test_worker_with_events(
                env,
                workflows=list(workflows),
                activities=list(activities),
                task_queue=TASK_QUEUE,
                interceptors=[ContextHandlerInterceptor()],
            ),
        ):
            yield env


class TestCustomEventModeConfig:
    @pytest.mark.parametrize("mode", list(PayloadEncryptionMode))
    @pytest.mark.parametrize("custom_event_mode", list(PayloadEncryptionMode))
    def test_overrides_mode_for_custom_events(
        self, mode: PayloadEncryptionMode, custom_event_mode: PayloadEncryptionMode
    ) -> None:
        encryption_config = PayloadEncryptionConfig(
            mode=mode, custom_event_mode=custom_event_mode, main_key=TEST_MAIN_KEY
        )

        assert encryption_config.mode == mode
        assert encryption_config.custom_event_config.mode == custom_event_mode

    def test_read_from_environment(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("TEMPORAL_PAYLOAD_ENCRYPTION__MODE", "full")
        monkeypatch.setenv("TEMPORAL_PAYLOAD_ENCRYPTION__CUSTOM_EVENT_MODE", "partial")
        monkeypatch.setenv("TEMPORAL_PAYLOAD_ENCRYPTION__MAIN_KEY", TEST_MAIN_KEY.get_secret_value())

        encryption_config = WorkerConfig().temporal_payload_encryption

        assert encryption_config is not None
        assert encryption_config.custom_event_mode == PayloadEncryptionMode.PARTIAL
        assert encryption_config.custom_event_config.mode == PayloadEncryptionMode.PARTIAL


class TestCustomEventMode:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "encryption_config, custom_events_readable",
        [
            pytest.param(FULL, False, id="full"),
            pytest.param(FULL_WITH_PARTIAL_CUSTOM_EVENTS, True, id="full-with-partial-custom-events"),
        ],
    )
    async def test_only_custom_task_events_follow_custom_event_mode(
        self, encryption_config: PayloadEncryptionConfig, custom_events_readable: bool
    ) -> None:
        captured_events: list[WorkflowEvent] = []
        async with _run_encrypted_worker(encryption_config, captured_events, [TaskWorkflow], [with_task]) as env:
            handle = await env.client.start_workflow(
                TaskWorkflow, id=f"custom-event-mode-{custom_events_readable}", task_queue=TASK_QUEUE
            )
            assert (await handle.result()).payload == {"result": f"{SECRET}-result"}
            history = await handle.fetch_history()

        assert _events_containing(history, SECRET) == []
        assert _events_containing(history, PUBLIC) == []

        custom_events = [e for e in captured_events if isinstance(e.attributes, BaseCustomTaskAttributes)]
        other_events = [e for e in captured_events if not isinstance(e.attributes, BaseCustomTaskAttributes)]
        assert custom_events and other_events
        assert {
            (e.attributes.custom_task_type, e.event_type)
            for e in custom_events
            if isinstance(e.attributes, BaseCustomTaskAttributes)
        } == {
            (task_type, event_type)
            for task_type in ("activity_content_task", "workflow_content_task")
            for event_type in (
                WorkflowEventType.CUSTOM_TASK_STARTED,
                WorkflowEventType.CUSTOM_TASK_IN_PROGRESS,
                WorkflowEventType.CUSTOM_TASK_COMPLETED,
            )
        }
        # Marked fields are encrypted in every mode; unmarked fields are readable only in custom events.
        custom_payloads = [p for e in custom_events for p in _event_payloads(e)]
        other_payloads = [p for e in other_events for p in _event_payloads(e)]
        assert custom_payloads and other_payloads
        assert all(SECRET not in _keyless_view(p) for p in custom_payloads + other_payloads)
        assert all(PUBLIC not in _keyless_view(p) for p in other_payloads)
        assert all((PUBLIC in _keyless_view(p)) is custom_events_readable for p in custom_payloads)
        assert all(p.encoding_options == [EncodedPayloadOptions.ENCRYPTED] for p in other_payloads)


class TestFailureEncryption:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("run_locally", [False, True], ids=["remote", "local"])
    async def test_workflow_reads_full_message_while_history_stays_encrypted(self, run_locally: bool) -> None:
        captured_events: list[WorkflowEvent] = []
        async with _run_encrypted_worker(FULL, captured_events, [FailureWorkflow], [fail]) as env:
            handle = await env.client.start_workflow(
                FailureWorkflow,
                FailureInput(run_locally=run_locally, catch=True),
                id=f"caught-failure-{run_locally}",
                task_queue=TASK_QUEUE,
            )
            result = (await handle.result()).payload["result"]
            history = await handle.fetch_history()

        assert f"{SECRET} from-activity" in result
        assert _events_containing(history, SECRET) == []
        assert all(SECRET not in e.model_dump_json() for e in captured_events)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("run_locally", [False, True], ids=["remote", "local"])
    async def test_escaped_activity_failure_stays_encrypted(self, run_locally: bool) -> None:
        captured_events: list[WorkflowEvent] = []
        async with _run_encrypted_worker(FULL, captured_events, [FailureWorkflow], [fail]) as env:
            handle = await env.client.start_workflow(
                FailureWorkflow,
                FailureInput(run_locally=run_locally, catch=False),
                id=f"escaped-failure-{run_locally}",
                task_queue=TASK_QUEUE,
            )
            with pytest.raises(WorkflowFailureError) as exc_info:
                await handle.result()
            history = await handle.fetch_history()

        assert _events_containing(history, SECRET) == []
        # A client holding the key still reads the full message.
        assert f"{SECRET} from-activity" in _error_chain(exc_info.value)
        assert all(SECRET not in e.model_dump_json() for e in captured_events)
        assert "ValueError" in _failure_messages(captured_events)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "workflow",
        [pytest.param(WorkflowFailureWorkflow, id="workflow"), pytest.param(TaskFailureWorkflow, id="task")],
    )
    @pytest.mark.parametrize(
        "encryption_config, leaks",
        [pytest.param(FULL, False, id="full"), pytest.param(PARTIAL, True, id="partial")],
    )
    async def test_failures_follow_mode(
        self, workflow: type, encryption_config: PayloadEncryptionConfig, leaks: bool
    ) -> None:
        captured_events: list[WorkflowEvent] = []
        async with _run_encrypted_worker(encryption_config, captured_events, [workflow], []) as env:
            handle = await env.client.start_workflow(
                workflow, id=f"failure-{workflow.__name__}-{leaks}", task_queue=TASK_QUEUE
            )
            with pytest.raises(WorkflowFailureError):
                await handle.result()
            history = await handle.fetch_history()

        assert bool(_events_containing(history, SECRET)) is leaks
        failure_messages = _failure_messages(captured_events)
        assert failure_messages
        if leaks:
            assert any(SECRET in message for message in failure_messages)
        else:
            assert set(failure_messages) == {"ContentError"}
