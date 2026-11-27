import dataclasses
import json
import threading
from collections.abc import Iterator
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any
from unittest.mock import patch

import pytest
import temporalio.activity
import temporalio.common
import temporalio.testing
import temporalio.workflow
from opentelemetry import metrics, trace
from opentelemetry.instrumentation import httpx as otel_httpx
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.trace import format_trace_id
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows._mistral_http import MISTRAL_HTTP
from mistralai.workflows.core.tracing import init_tracing
from mistralai.workflows.core.tracing._otel_config import (
    WORKFLOW_ROOT_ID_GENERATOR,
    config_otel,
    config_otel_local,
)
from mistralai.workflows.core.tracing._temporal_tracing_interceptor import (
    MistralTemporalTracingInterceptor,
    MistralWorkflowTracingInterceptor,
)
from mistralai.workflows.core.tracing.workflow_context import (
    GEN_AI_WORKFLOW_NAME_ATTRIBUTE,
    WorkflowContextSpanProcessor,
    workflow_context_span_attributes,
)
from mistralai.workflows.models import EventAttributes, SearchAttributes

from . import fixtures_workflow_context
from .fixtures_workflow_context import (
    ACTIVITY_TYPE,
    WORKFLOW_TYPE,
    WorkflowContextProbeWorkflow,
    workflow_context_probe_activity,
)
from .utils import create_test_worker

WORKFLOW_CONTEXT_KEYS = (
    EventAttributes.workflow_execution_id,
    EventAttributes.workflow_type,
    EventAttributes.workflow_run_id,
)
ACTIVITY_CONTEXT_KEYS = (
    EventAttributes.activity_type,
    EventAttributes.activity_execution_id,
    EventAttributes.activity_attempt,
)


def _fake_activity_info(**overrides: Any) -> temporalio.activity.Info:
    base = temporalio.testing.ActivityEnvironment.default_info()
    return dataclasses.replace(base, **overrides)


def _fake_workflow_info(**overrides: Any) -> temporalio.workflow.Info:
    now = datetime.now(timezone.utc)
    defaults = dict(
        attempt=1,
        continued_run_id=None,
        cron_schedule=None,
        execution_timeout=None,
        first_execution_run_id="run-1",
        headers={},
        namespace="ns",
        original_execution_run_id="run-1",
        parent=None,
        root=None,
        priority=temporalio.common.Priority.default,
        raw_memo={},
        retry_policy=None,
        run_id="run-1",
        run_timeout=None,
        search_attributes={},
        start_time=now,
        task_queue="tq",
        task_timeout=timedelta(seconds=10),
        typed_search_attributes=temporalio.common.TypedSearchAttributes.empty,
        workflow_id="wf-1",
        workflow_start_time=now,
        workflow_type="wf-type",
    )
    return temporalio.workflow.Info(**{**defaults, **overrides})


@pytest.fixture
def processor_tracer_exporter() -> Iterator[tuple[trace.Tracer, InMemorySpanExporter]]:
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(WorkflowContextSpanProcessor())
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    try:
        yield provider.get_tracer("test-workflow-context"), exporter
    finally:
        provider.shutdown()


def _finished_attributes(exporter: InMemorySpanExporter) -> dict[str, Any]:
    (span,) = exporter.get_finished_spans()
    assert span.attributes is not None
    return dict(span.attributes)


class TestWorkflowContextSpanProcessor:
    def test_enriches_from_activity_context(
        self, processor_tracer_exporter: tuple[trace.Tracer, InMemorySpanExporter]
    ) -> None:
        tracer, exporter = processor_tracer_exporter
        info = _fake_activity_info(
            workflow_id="wf-1",
            workflow_run_id="run-1",
            workflow_type="wf-type",
            activity_type=ACTIVITY_TYPE,
            activity_id="act-1",
            attempt=2,
        )
        with (
            patch("temporalio.activity.in_activity", return_value=True),
            patch("temporalio.activity.info", return_value=info),
        ):
            with tracer.start_span("probe"):
                pass

        attributes = _finished_attributes(exporter)
        assert attributes[EventAttributes.workflow_execution_id] == "wf-1"
        assert attributes["temporalWorkflowID"] == "wf-1"
        assert attributes[EventAttributes.workflow_type] == "wf-type"
        assert attributes[GEN_AI_WORKFLOW_NAME_ATTRIBUTE] == "wf-type"
        assert attributes[EventAttributes.workflow_run_id] == "run-1"
        assert attributes[EventAttributes.activity_type] == ACTIVITY_TYPE
        assert attributes[EventAttributes.activity_execution_id] == "act-1"
        assert attributes[EventAttributes.activity_attempt] == 2

    def test_enriches_from_workflow_context(
        self, processor_tracer_exporter: tuple[trace.Tracer, InMemorySpanExporter]
    ) -> None:
        tracer, exporter = processor_tracer_exporter
        with (
            patch("temporalio.workflow.in_workflow", return_value=True),
            patch("temporalio.workflow.info", return_value=_fake_workflow_info()),
        ):
            with tracer.start_span("probe"):
                pass

        attributes = _finished_attributes(exporter)
        assert attributes[EventAttributes.workflow_execution_id] == "wf-1"
        assert attributes[EventAttributes.workflow_type] == "wf-type"
        assert attributes[GEN_AI_WORKFLOW_NAME_ATTRIBUTE] == "wf-type"
        assert attributes[EventAttributes.workflow_run_id] == "run-1"
        assert all(key not in attributes for key in ACTIVITY_CONTEXT_KEYS)

    def test_does_not_touch_spans_outside_a_workflow(
        self, processor_tracer_exporter: tuple[trace.Tracer, InMemorySpanExporter]
    ) -> None:
        tracer, exporter = processor_tracer_exporter
        with tracer.start_span("probe"):
            pass

        assert _finished_attributes(exporter) == {}

    def test_does_not_overwrite_producer_attributes(
        self, processor_tracer_exporter: tuple[trace.Tracer, InMemorySpanExporter]
    ) -> None:
        tracer, exporter = processor_tracer_exporter
        info = _fake_activity_info(workflow_id="wf-1", workflow_run_id="run-1", workflow_type="wf-type")
        producer_attributes = {
            EventAttributes.workflow_type: "producer-set",
            EventAttributes.workflow_run_id: "producer-run",
        }
        with (
            patch("temporalio.activity.in_activity", return_value=True),
            patch("temporalio.activity.info", return_value=info),
        ):
            with tracer.start_span("probe", attributes=producer_attributes):
                pass

        attributes = _finished_attributes(exporter)
        assert attributes[EventAttributes.workflow_type] == "producer-set"
        assert attributes[EventAttributes.workflow_run_id] == "producer-run"
        assert attributes[EventAttributes.workflow_execution_id] == "wf-1"


class TestWorkflowContextSpanAttributesHelper:
    def test_returns_empty_mapping_outside_a_workflow(self) -> None:
        assert workflow_context_span_attributes() == {}


class TestProviderAttachment:
    @pytest.fixture(autouse=True)
    def _isolate_global_providers(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # config_otel/config_otel_local install their providers globally; the process-global
        # provider belongs to whichever test module set it first, so swallow the installs.
        monkeypatch.setattr(trace, "set_tracer_provider", lambda provider: None)
        monkeypatch.setattr(metrics, "set_meter_provider", lambda provider: None)

    def test_config_otel_attaches_workflow_context_processor(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT", raising=False)
        _, tracer_provider, _ = config_otel(component="worker", service_name="wf-ctx-test")

        processors = tracer_provider._active_span_processor._span_processors
        assert any(isinstance(p, WorkflowContextSpanProcessor) for p in processors)

    def test_config_otel_local_attaches_workflow_context_processor(self) -> None:
        _, tracer_provider, _ = config_otel_local(service_name="wf-ctx-test")

        processors = tracer_provider._active_span_processor._span_processors
        assert any(isinstance(p, WorkflowContextSpanProcessor) for p in processors)


class _ProbeHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        body = json.dumps({"ok": True}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args: object) -> None:
        pass


@pytest.fixture
def probe_server() -> Iterator[str]:
    server = HTTPServer(("127.0.0.1", 0), _ProbeHandler)
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


@dataclasses.dataclass
class ProbeTelemetry:
    """A provider dedicated to one test, so nothing here depends on the process-global one."""

    provider: TracerProvider
    tracer: trace.Tracer
    exporter: InMemorySpanExporter


@pytest.fixture
def probe_telemetry() -> Iterator[ProbeTelemetry]:
    exporter = InMemorySpanExporter()
    provider = TracerProvider(id_generator=WORKFLOW_ROOT_ID_GENERATOR)
    provider.add_span_processor(WorkflowContextSpanProcessor())
    provider.add_span_processor(SimpleSpanProcessor(exporter))

    previous_tracer = fixtures_workflow_context.probe_tracer
    fixtures_workflow_context.probe_tracer = provider.get_tracer("test-workflow-context")
    try:
        yield ProbeTelemetry(
            provider=provider,
            tracer=fixtures_workflow_context.probe_tracer,
            exporter=exporter,
        )
    finally:
        fixtures_workflow_context.probe_tracer = previous_tracer
        provider.shutdown()


@pytest.fixture
def http_client_instrumentation(probe_telemetry: ProbeTelemetry) -> Iterator[None]:
    """Bind the HTTP client instrumentors to the probe's tracer provider.

    Instrumentors are process-wide singletons and may have been left instrumented by an
    earlier test bound to another provider (e.g. a detached run_worker), in which case
    spans would silently land there. Rebind them here, and on teardown only undo what
    this fixture turned on.
    """
    was_on = {type(i) for i in _http_instrumentors() if i.is_instrumented_by_opentelemetry}
    for instrumentor in _http_instrumentors():
        if instrumentor.is_instrumented_by_opentelemetry:
            instrumentor.uninstrument()
    init_tracing._instrument_http_clients(meter_provider=None, tracer_provider=probe_telemetry.provider)
    try:
        yield
    finally:
        for instrumentor in _http_instrumentors():
            if type(instrumentor) not in was_on and instrumentor.is_instrumented_by_opentelemetry:
                instrumentor.uninstrument()


class TestEverySpanCarriesWorkflowContext:
    @pytest.mark.asyncio
    async def test_workflow_run_spans_carry_context_attributes(
        self,
        temporal_env: WorkflowEnvironment,
        probe_telemetry: ProbeTelemetry,
        http_client_instrumentation: None,
        probe_server: str,
        mock_upsert_search_attributes: Any,
    ) -> None:
        if MISTRAL_HTTP.__name__ == "httpx2" and not hasattr(otel_httpx, "HTTPX2ClientInstrumentor"):
            pytest.skip("HTTPX2ClientInstrumentor needs opentelemetry-instrumentation-httpx>=0.65b0")

        interceptors = [
            MistralTemporalTracingInterceptor(tracer=probe_telemetry.tracer, always_create_workflow_spans=True),
            MistralWorkflowTracingInterceptor(tracer=probe_telemetry.tracer),
        ]
        async with create_test_worker(
            temporal_env,
            workflows=[WorkflowContextProbeWorkflow],
            activities=[workflow_context_probe_activity],
            interceptors=interceptors,
        ):
            handle = await temporal_env.client.start_workflow(
                WORKFLOW_TYPE,
                probe_server,
                id="test-workflow-context-spans",
                task_queue="test-task-queue",
            )
            result = await handle.result()
        probe_telemetry.provider.force_flush()

        assert result == {"result": "ok"}

        upserted_attrs = mock_upsert_search_attributes.call_args.args[0]
        search_attrs = {pair.key.name: pair.value for pair in upserted_attrs}
        workflow_trace_id = search_attrs[SearchAttributes.otel_trace_id]
        spans = [
            s
            for s in probe_telemetry.exporter.get_finished_spans()
            if format_trace_id(s.context.trace_id) == workflow_trace_id
        ]
        assert spans, "no spans captured for the workflow's trace"

        names = {span.name for span in spans}
        for expected_name in (
            f"StartWorkflow:{WORKFLOW_TYPE}",
            f"RunWorkflow:{WORKFLOW_TYPE}",
            f"WorkflowInit:{WORKFLOW_TYPE}",
            f"StartActivity:{ACTIVITY_TYPE}",
            f"RunActivity:{ACTIVITY_TYPE}",
            f"ExecuteActivity:{ACTIVITY_TYPE}",
            "manual_probe_span",
            "GET",
            f"WorkflowReport:{WORKFLOW_TYPE}",
        ):
            assert expected_name in names, f"missing span {expected_name}; got {sorted(names)}"

        for span in spans:
            attrs = span.attributes or {}
            if span.name == "manual_probe_span":
                continue
            assert attrs.get(EventAttributes.workflow_execution_id) == "test-workflow-context-spans", (
                f"{span.name} missing wf.workflow.execution_id"
            )
            assert attrs.get(EventAttributes.workflow_type) == WORKFLOW_TYPE, f"{span.name} missing wf.workflow.type"
            assert attrs.get(GEN_AI_WORKFLOW_NAME_ATTRIBUTE) == WORKFLOW_TYPE, (
                f"{span.name} missing gen_ai.workflow.name"
            )
            assert attrs.get(EventAttributes.workflow_run_id), f"{span.name} missing wf.workflow.run_id"

        activity_side_names = {
            f"RunActivity:{ACTIVITY_TYPE}",
            f"ExecuteActivity:{ACTIVITY_TYPE}",
            "manual_probe_span",
            "GET",
        }
        activity_side_spans = [s for s in spans if s.name in activity_side_names]
        assert len(activity_side_spans) == len(activity_side_names)
        for span in activity_side_spans:
            attrs = span.attributes or {}
            assert attrs.get(EventAttributes.activity_type) == ACTIVITY_TYPE, span.name
            assert attrs.get(EventAttributes.activity_execution_id), span.name
            assert attrs.get(EventAttributes.activity_attempt) == 1, span.name

        workflow_side_spans = [s for s in spans if s.name not in activity_side_names]
        for span in workflow_side_spans:
            attrs = span.attributes or {}
            assert all(key not in attrs for key in ACTIVITY_CONTEXT_KEYS), span.name

        manual_span = next(s for s in spans if s.name == "manual_probe_span")
        assert manual_span.attributes[EventAttributes.workflow_type] == "producer-set-type"
