import json
import threading
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

import pytest
from opentelemetry import trace
from opentelemetry.instrumentation import httpx as otel_httpx
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, SpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows._mistral_http import MISTRAL_HTTP
from mistralai.workflows.client import get_mistral_client
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.tracing import init_tracing
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


class _ModelsHandler(BaseHTTPRequestHandler):
    received_headers: list[dict[str, str]] = []

    def do_GET(self) -> None:
        self.received_headers.append({key.lower(): value for key, value in self.headers.items()})
        body = json.dumps({"object": "list", "data": []}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args: object) -> None:
        pass


@pytest.fixture
def models_server() -> Iterator[str]:
    """A real local HTTP server: MockTransport bypasses the httpx instrumentors."""
    _ModelsHandler.received_headers = []
    server = HTTPServer(("127.0.0.1", 0), _ModelsHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        thread.join()


def _http_instrumentors() -> list[Any]:
    instrumentors: list[Any] = [HTTPXClientInstrumentor()]
    if hasattr(otel_httpx, "HTTPX2ClientInstrumentor"):
        instrumentors.append(otel_httpx.HTTPX2ClientInstrumentor())
    return instrumentors


@pytest.fixture
def http_client_instrumentation() -> Iterator[None]:
    """Instrument HTTP clients through init_tracing's own helper.

    Instrumentors are process-wide singletons, so only undo the ones this fixture turned on.
    """
    already_on = {type(i) for i in _http_instrumentors() if i.is_instrumented_by_opentelemetry}
    tracer_provider = trace.get_tracer_provider()
    assert isinstance(tracer_provider, TracerProvider)
    init_tracing._instrument_http_clients(meter_provider=None, tracer_provider=tracer_provider)
    try:
        yield
    finally:
        for instrumentor in _http_instrumentors():
            if type(instrumentor) not in already_on and instrumentor.is_instrumented_by_opentelemetry:
                instrumentor.uninstrument()


class TestMistralClientTracing:
    @pytest.mark.asyncio
    async def test_mistral_call_emits_client_spans_and_propagates_context(
        self,
        global_span_exporter: InMemorySpanExporter,
        http_client_instrumentation: None,
        models_server: str,
    ) -> None:
        # Decided from the installed package only, never from init_tracing's flag, so a broken
        # flag fails this test instead of skipping it. compat_mistral_v3 pins a release that has it.
        if MISTRAL_HTTP.__name__ == "httpx2" and not hasattr(otel_httpx, "HTTPX2ClientInstrumentor"):
            pytest.skip("HTTPX2ClientInstrumentor needs opentelemetry-instrumentation-httpx>=0.65b0")
        client = get_mistral_client(api_key="test-key", server_url=models_server)

        with trace.get_tracer(__name__).start_as_current_span("activity") as activity_span:
            await client.models.list_async()
        trace.get_tracer_provider().force_flush()

        trace_id = activity_span.get_span_context().trace_id
        span_names = {
            span.name for span in global_span_exporter.get_finished_spans() if span.context.trace_id == trace_id
        }
        assert "GET" in span_names, "transport span from the httpx/httpx2 instrumentor"
        assert "list_models_v1_models_get" in span_names, "operation span from the Mistral SDK"
        (headers,) = _ModelsHandler.received_headers
        assert f"{trace_id:032x}" in headers["traceparent"]
