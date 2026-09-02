"""Provider billed-usage capture on the failure/cancel path.

The money-path guarantee: when a streaming provider call raises AFTER the
provider has billed us (safety block mid-stream, network drop, client
disconnect -> CancelledError), the provider stamps the billed TokenUsage onto
the exception via ``attach_billed_usage`` so the orchestrator's failure
finalizer records real cost instead of cost=0.

These pin (a) the provider-agnostic contract in ``providers/errors.py`` and
(b) the xAI implementation (the reference fix; the OpenAI-compatible providers
follow the same shape).
"""
from __future__ import annotations

import asyncio
import types

from matrx_ai.config import TokenUsage
from matrx_ai.providers.errors import (
    accumulate_billed_usage,
    attach_billed_usage,
    attach_openai_billed_usage,
    get_billed_usage,
    stream_with_billed_usage,
)


class TestBilledUsageContract:
    def test_attach_then_get_roundtrips(self):
        exc = RuntimeError("boom")
        tu = TokenUsage(input_tokens=100, output_tokens=50, matrx_model_name="m", api="xai")
        attach_billed_usage(exc, tu)
        assert get_billed_usage(exc) is tu

    def test_none_usage_is_noop(self):
        exc = RuntimeError("boom")
        attach_billed_usage(exc, None)
        assert get_billed_usage(exc) is None

    def test_works_on_cancellederror(self):
        # CancelledError is a BaseException, not Exception — the cancel path is
        # exactly where cost was being lost.
        exc = asyncio.CancelledError()
        tu = TokenUsage(input_tokens=1, output_tokens=2, matrx_model_name="m", api="xai")
        attach_billed_usage(exc, tu)
        assert get_billed_usage(exc) is tu

    def test_innermost_capture_wins(self):
        # The capture closest to the wire wins; an outer re-attach must not clobber.
        exc = RuntimeError("boom")
        inner = TokenUsage(input_tokens=100, output_tokens=50, matrx_model_name="m", api="xai")
        outer = TokenUsage(input_tokens=1, output_tokens=1, matrx_model_name="m", api="xai")
        attach_billed_usage(exc, inner)
        attach_billed_usage(exc, outer)
        assert get_billed_usage(exc) is inner

    def test_explicit_accumulation_preserves_all_paid_attempts(self):
        exc = RuntimeError("boom")
        first = TokenUsage(
            input_tokens=100,
            output_tokens=50,
            matrx_model_name="m",
            api="anthropic",
            billing_components={"service.web_search": 1},
        )
        second = TokenUsage(
            input_tokens=20,
            output_tokens=5,
            matrx_model_name="m",
            api="anthropic",
            billing_components={"service.web_search": 2},
        )
        attach_billed_usage(exc, first)
        accumulate_billed_usage(exc, second)

        total = get_billed_usage(exc)
        assert total.input_tokens == 120
        assert total.output_tokens == 55
        assert total.billing_components == {"service.web_search": 3}

    def test_attach_on_setattr_rejecting_exception_is_swallowed(self):
        # Cost capture must NEVER mask the real error, even if the exception
        # type rejects attribute assignment.
        class Frozen(BaseException):
            def __setattr__(self, key, value):
                raise AttributeError("frozen")

        exc = Frozen()
        tu = TokenUsage(input_tokens=1, output_tokens=1, matrx_model_name="m", api="xai")
        attach_billed_usage(exc, tu)  # must not raise
        assert get_billed_usage(exc) is None

    def test_executor_harvest_is_idempotent_and_stamps_attempt(
        self,
        monkeypatch,
    ):
        from matrx_ai.orchestrator import executor

        class Request:
            request_id = "request-1"
            conversation_id = "conversation-1"

            def __init__(self):
                self.usage_history = []

            def add_usage(self, usage):
                self.usage_history.append(usage)

        request = Request()
        exc = RuntimeError("paid attempt failed")
        usage = TokenUsage(
            input_tokens=100,
            output_tokens=2,
            matrx_model_name="claude",
            api="anthropic",
        )
        attach_billed_usage(exc, usage)
        monkeypatch.setattr(executor, "_spine_meter_call", lambda _usage: None)

        executor._record_billed_usage_on_failure(
            request,
            exc,
            iteration=3,
            provider_attempt=2,
        )
        executor._record_billed_usage_on_failure(
            request,
            exc,
            iteration=3,
            provider_attempt=2,
        )

        assert request.usage_history == [usage]
        assert usage.metadata == {
            "iteration": 3,
            "provider_attempt": 2,
            "attempt_outcome": "failed",
        }


class _FakeUsage:
    def __init__(self, p, c):
        self.prompt_tokens = p
        self.completion_tokens = c
        self.total_tokens = p + c


class _FakeProto:
    model = "grok-4"


class _FakePartialResponse:
    """Shape of the accumulating xai_sdk response object mid-stream."""
    def __init__(self, p=120, c=40):
        self.usage = _FakeUsage(p, c)
        self.proto = _FakeProto()
        self.id = "resp_abc"


class TestXaiBilledUsageCapture:
    def test_extracts_usage_from_partial_response(self):
        from matrx_ai.providers.xai.xai_api import XAIChat

        tu = XAIChat._billed_usage_from_response(_FakePartialResponse(p=120, c=40))
        assert tu is not None
        assert tu.input_tokens == 120
        assert tu.output_tokens == 40
        assert tu.matrx_model_name == "grok-4"

    def test_none_response_returns_none(self):
        from matrx_ai.providers.xai.xai_api import XAIChat

        assert XAIChat._billed_usage_from_response(None) is None

    def test_no_tokens_yet_returns_none(self):
        from matrx_ai.providers.xai.xai_api import XAIChat

        assert XAIChat._billed_usage_from_response(_FakePartialResponse(p=0, c=0)) is None

    def test_attach_stamps_cost_onto_cancellation(self):
        from matrx_ai.providers.xai.xai_api import XAIChat

        chat = XAIChat.__new__(XAIChat)  # bypass __init__ (needs an API client)
        exc = asyncio.CancelledError()
        chat._attach_billed_usage(exc, _FakePartialResponse(p=120, c=40))
        got = get_billed_usage(exc)
        assert got is not None and got.input_tokens == 120 and got.output_tokens == 40


class TestOpenAICompatibleStreamCapture:
    """The shared wrapper used by cerebras/groq/together/generic_openai."""

    def test_attaches_usage_on_mid_stream_failure(self):
        async def fake_stream():
            yield types.SimpleNamespace(usage=None)
            yield types.SimpleNamespace(usage=_FakeUsage(120, 40))
            raise RuntimeError("boom mid-stream")

        async def drive():
            try:
                async for _ in stream_with_billed_usage(
                    fake_stream(), model="llama-x", api="groq"
                ):
                    pass
            except RuntimeError as exc:
                return exc
            return None

        exc = asyncio.run(drive())
        assert exc is not None
        usage = get_billed_usage(exc)
        assert usage is not None
        assert usage.input_tokens == 120 and usage.output_tokens == 40
        assert usage.matrx_model_name == "llama-x"

    def test_attaches_choice_usage_on_mid_stream_failure(self):
        """Moonshot places terminal usage on choice.usage, not chunk.usage."""
        async def fake_stream():
            yield types.SimpleNamespace(
                usage=None,
                choices=[types.SimpleNamespace(usage=_FakeUsage(120, 40))],
            )
            raise RuntimeError("boom after Moonshot terminal chunk")

        async def drive():
            try:
                async for _ in stream_with_billed_usage(
                    fake_stream(), model="moonshotai/Kimi-K3", api="moonshot"
                ):
                    pass
            except RuntimeError as exc:
                return exc
            return None

        exc = asyncio.run(drive())
        usage = get_billed_usage(exc)
        assert usage is not None
        assert usage.input_tokens == 120 and usage.output_tokens == 40

    def test_attaches_usage_on_cancellation(self):
        async def fake_stream():
            yield types.SimpleNamespace(usage=_FakeUsage(7, 3))
            raise asyncio.CancelledError()

        async def drive():
            try:
                async for _ in stream_with_billed_usage(fake_stream(), model="m", api="cerebras"):
                    pass
            except asyncio.CancelledError as exc:
                return exc
            return None

        exc = asyncio.run(drive())
        assert exc is not None
        assert get_billed_usage(exc).output_tokens == 3

    def test_clean_stream_passes_chunks_through_with_no_attach(self):
        async def fake_stream():
            yield types.SimpleNamespace(usage=None)
            yield types.SimpleNamespace(usage=_FakeUsage(1, 1))

        async def drive():
            return [
                c async for c in stream_with_billed_usage(fake_stream(), model="m", api="groq")
            ]

        chunks = asyncio.run(drive())
        assert len(chunks) == 2

    def test_attach_openai_none_is_noop(self):
        exc = RuntimeError("boom")
        attach_openai_billed_usage(exc, None, model="m", api="groq")
        assert get_billed_usage(exc) is None

    def test_attach_openai_preserves_provider_charge_evidence(self):
        usage_data = types.SimpleNamespace(
            prompt_tokens=100,
            completion_tokens=20,
            cost=0.0042,
        )
        exc = RuntimeError("stream failed")

        attach_openai_billed_usage(exc, usage_data, model="gateway/model", api="gateway")

        usage = get_billed_usage(exc)
        assert usage is not None
        assert usage.raw_usage == {
            "prompt_tokens": 100,
            "completion_tokens": 20,
            "cost": 0.0042,
        }
        assert usage.provider_charge is not None
        assert usage.provider_charge.authoritative_usd == 0.0042


class TestAnthropicBilledUsageCapture:
    def test_uninitialized_pre_response_snapshot_is_not_a_capture_failure(self, monkeypatch):
        from matrx_ai.providers.anthropic.anthropic_api import AnthropicChat
        from matrx_ai.providers.errors import report_unbilled_provider_failure

        class _PreResponseStream:
            @property
            def current_message_snapshot(self):
                raise AssertionError

        reports = []
        monkeypatch.setattr(
            "matrx_ai.providers.errors.report_billed_usage_capture_failure",
            lambda provider, exc: reports.append((provider, exc)),
        )
        chat = AnthropicChat.__new__(AnthropicChat)
        provider_exc = RuntimeError("Anthropic overloaded before response")

        chat._attach_billed_usage_from_stream(
            provider_exc,
            _PreResponseStream(),
            "claude-test",
        )

        assert reports == []
        assert (
            report_unbilled_provider_failure(
                provider_exc,
                provider="anthropic",
                model="claude-test",
            )
            is False
        )


class TestLayerTwoUnbilledFailureNet:
    """LAYER 2 — the net for a provider adapter that never runs billing capture.

    Layer 1 is invisible when it is simply never called: downstream, a forgetful
    adapter and an honest $0 look identical. These pin that the net fires for the
    forgetful case and stays quiet for every honest one.
    """

    def _fire(self, exc, *, provider="xai_chat", model="m"):
        from matrx_ai.providers.errors import report_unbilled_provider_failure

        return report_unbilled_provider_failure(exc, provider=provider, model=model)

    def test_fires_on_a_wire_failure_nobody_billing_checked(self):
        import httpx

        assert self._fire(httpx.ReadTimeout("boom")) is True

    def test_silent_on_cancellation(self):
        # Cancels ARE billed, but layer 2 cannot judge them: the consumer, not the
        # async generator, receives the CancelledError, so a correct adapter still
        # cannot mark it. Alarming would fire on every stop-button press and blame
        # an adapter that did everything right. See wire_was_engaged.
        assert self._fire(asyncio.CancelledError()) is False

    def test_silent_when_an_adapter_already_looked_and_found_nothing(self):
        # attach_billed_usage(None) is a no-op for USAGE but still records that
        # the adapter looked. That distinction is the whole point of layer 2.
        import httpx

        exc = httpx.ReadTimeout("boom")
        attach_billed_usage(exc, None)
        assert self._fire(exc) is False

    def test_silent_on_pre_inference_rejections(self):
        # A rejection is not a charge. A red line per bad key / bad schema /
        # rate-limit is how an alarm becomes background noise.
        import httpx

        for status in (400, 401, 402, 403, 404, 422, 429):
            exc = httpx.HTTPStatusError(
                f"{status}",
                request=httpx.Request("POST", "https://api.example/v1/x"),
                response=httpx.Response(status),
            )
            assert self._fire(exc) is False, status

    def test_fires_on_a_server_error_that_could_land_after_generation(self):
        import httpx

        exc = httpx.HTTPStatusError(
            "500",
            request=httpx.Request("POST", "https://api.example/v1/x"),
            response=httpx.Response(500),
        )
        assert self._fire(exc) is True

    def test_silent_when_the_request_never_reached_a_server(self):
        import socket

        import httpx

        assert self._fire(httpx.ConnectError("refused")) is False
        assert self._fire(socket.gaierror("dns")) is False

    def test_silent_on_interpreter_shutdown(self):
        # SystemExit carries an int `.code`, which a naive status sniffer reads
        # as an HTTP status.
        assert self._fire(SystemExit(1)) is False

    def test_silent_when_an_adapter_attached_real_usage(self):
        import httpx

        exc = httpx.ReadTimeout("boom")
        attach_billed_usage(
            exc, TokenUsage(input_tokens=10, output_tokens=1, matrx_model_name="m", api="xai")
        )
        assert self._fire(exc) is False

    def test_silent_when_the_wire_was_never_engaged(self):
        # A capability gate raising before dispatch cannot have been billed.
        # Alarming here would train everyone to ignore the alarm.
        assert self._fire(ValueError("model does not support tools")) is False

    def test_fires_only_once_per_failure(self):
        import httpx

        exc = httpx.ReadTimeout("boom")
        assert self._fire(exc) is True
        assert self._fire(exc) is False

    def test_never_raises_on_an_exception_that_rejects_attributes(self):
        # Cost alarms must never mask the real error.
        class _Mandated(BaseException):
            __slots__ = ()

        assert self._fire(_Mandated()) in (True, False)


class TestDispatchBillingNet:
    """The net is wired at the ONE chokepoint every catalog-routed call passes."""

    def test_dispatch_reraises_untouched_and_reports(self):
        import httpx
        from types import SimpleNamespace

        from matrx_ai.providers.errors import was_billing_checked
        from matrx_ai.providers.unified_client import UnifiedAIClient

        original = httpx.ReadTimeout("provider died mid-stream")

        async def _boom():
            raise original

        async def _run():
            try:
                await UnifiedAIClient._dispatch_with_billing_net(
                    _boom,
                    profile=SimpleNamespace(
                        vendor="xai",
                        model_name="grok",
                        endpoint_id="xai-test",
                        base_url=None,
                        offering_metadata={},
                    ),
                )
            except BaseException as exc:  # noqa: BLE001
                return exc
            return None

        raised = asyncio.run(_run())
        assert raised is original, "the net must never swallow or replace the error"
        assert was_billing_checked(original), "the net should have fired and marked it"

    def test_dispatch_passes_a_successful_response_through(self):
        from types import SimpleNamespace

        from matrx_ai.providers.unified_client import UnifiedAIClient

        sentinel = object()

        async def _ok():
            return sentinel

        async def _run():
            return await UnifiedAIClient._dispatch_with_billing_net(
                _ok,
                profile=SimpleNamespace(
                    vendor="xai",
                    model_name="grok",
                    endpoint_id="xai-test",
                    base_url=None,
                    offering_metadata={},
                ),
            )

        assert asyncio.run(_run()) is sentinel

    def test_dispatch_billing_gap_creates_structured_system_error(self, monkeypatch):
        import httpx
        from types import SimpleNamespace

        from matrx_ai.providers.unified_client import UnifiedAIClient

        captured = []

        async def _capture(exc, **fields):
            captured.append((exc, fields))

        monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", _capture)
        original = httpx.ReadTimeout("provider died after dispatch")

        async def _boom():
            raise original

        async def _run():
            try:
                await UnifiedAIClient._dispatch_with_billing_net(
                    _boom,
                    profile=SimpleNamespace(vendor="xai", model_name="grok"),
                )
            except BaseException as exc:  # noqa: BLE001
                return exc
            return None

        assert asyncio.run(_run()) is original
        assert captured == [
            (
                original,
                {
                    "kind": "provider_billing_capture_missing",
                    "route": "providers/dispatch",
                    "error_type": "httpx.ReadTimeout",
                    "payload": {"provider": "xai", "model": "grok"},
                },
            )
        ]

    def test_google_adapter_marks_zero_chunk_failure_as_billing_checked(self):
        import httpx

        from matrx_ai.providers.errors import report_unbilled_provider_failure
        from matrx_ai.providers.google.google_api import GoogleChat

        chat = GoogleChat.__new__(GoogleChat)
        exc = httpx.HTTPStatusError(
            "503",
            request=httpx.Request("POST", "https://google.example/generate"),
            response=httpx.Response(503),
        )

        chat._attach_billed_usage_from_chunks(exc, [], "gemini-test")
        assert (
            report_unbilled_provider_failure(exc, provider="google", model="gemini-test")
            is False
        )
