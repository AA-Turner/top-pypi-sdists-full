from collections.abc import Iterator

import pytest
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, SpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows.core.config.config import config
from mistralai.workflows.testing import create_test_worker

from .fixtures_chat_completion import ChatCompletionWorkflow, chat_completion_activity


@pytest.fixture
def global_span_exporter() -> Iterator[InMemorySpanExporter]:
    """Capture spans from the process-global tracer provider.

    Attaches a processor to whatever provider is already installed so the test
    is independent of module import order (OTel forbids overriding a provider
    once set).
    """
    provider = trace.get_tracer_provider()
    if not isinstance(provider, TracerProvider):
        provider = TracerProvider()
        trace.set_tracer_provider(provider)

    memory = InMemorySpanExporter()
    processor: SpanProcessor = SimpleSpanProcessor(memory)
    provider.add_span_processor(processor)
    try:
        yield memory
    finally:
        processor.shutdown()


def _genai_spans(exporter: InMemorySpanExporter) -> list:
    return [s for s in exporter.get_finished_spans() if (s.attributes or {}).get("gen_ai.operation.name")]


class TestSdkSpanEmissionInWorkflow:
    """Behavioral non-regression test for Mistral SDK spans emission in workflows."""

    @pytest.mark.asyncio
    async def test_workflow_sdk_call_emits_genai_span(
        self, temporal_env: WorkflowEnvironment, global_span_exporter: InMemorySpanExporter
    ) -> None:
        async with create_test_worker(
            temporal_env, workflows=[ChatCompletionWorkflow], activities=[chat_completion_activity]
        ):
            handle = await temporal_env.client.start_workflow(
                "chat_completion_workflow", id="test-sdk-span-emission", task_queue="test-task-queue"
            )
            result = await handle.result()
        trace.get_tracer_provider().force_flush()

        assert result == {"result": "hi there"}

        genai = _genai_spans(global_span_exporter)
        assert len(genai) == 1
        assert genai[0].attributes["gen_ai.operation.name"] == "chat"
        assert genai[0].attributes["gen_ai.request.model"] == "mistral-small-latest"

    @pytest.mark.asyncio
    async def test_no_genai_spans_when_otel_disabled(
        self,
        temporal_env: WorkflowEnvironment,
        global_span_exporter: InMemorySpanExporter,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(config.common, "otel_enabled", False)

        async with create_test_worker(
            temporal_env, workflows=[ChatCompletionWorkflow], activities=[chat_completion_activity]
        ):
            handle = await temporal_env.client.start_workflow(
                "chat_completion_workflow", id="test-sdk-span-emission-disabled", task_queue="test-task-queue"
            )
            result = await handle.result()
        trace.get_tracer_provider().force_flush()

        assert result == {"result": "hi there"}
        assert _genai_spans(global_span_exporter) == []
