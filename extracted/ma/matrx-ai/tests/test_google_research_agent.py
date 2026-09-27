"""Google Deep Research as an agent turn — request shape, stream relay, result.

The fake Interactions client below speaks the SDK's event/record shapes as
plain objects; the adapter reads everything through attribute access, so the
same code path runs against google-genai's pydantic models.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace as NS
from typing import Any

import pytest

from matrx_ai.config import TextContent, ThinkingContent, UnifiedConfig
from matrx_ai.providers.google import google_research_agent as gra


def _config(**overrides: Any) -> UnifiedConfig:
    data: dict[str, Any] = {
        "model": "deep-research-preview-04-2026",
        "messages": [{"role": "user", "content": "How do heat pumps perform below -15C?"}],
        "system_instruction": "Write for a homeowner.",
    }
    data.update(overrides)
    return UnifiedConfig.from_dict(data)


_PROFILE = NS(
    provider_model_id="deep-research-preview-04-2026",
    model_name="deep-research-preview-04-2026",
)


def test_request_carries_agent_background_and_author_settings() -> None:
    kwargs = gra.build_research_kwargs(
        _config(reasoning_summary="never", visualization="off"), _PROFILE
    )
    assert kwargs["agent"] == "deep-research-preview-04-2026"
    assert kwargs["background"] is True and kwargs["store"] is True
    assert kwargs["agent_config"] == {
        "type": "deep-research",
        "thinking_summaries": "none",
        "visualization": "off",
    }
    # Google refuses system_instruction on research agents; instructions lead the input.
    assert "system_instruction" not in kwargs
    assert kwargs["input"].startswith("Instructions:\n")
    assert "Write for a homeowner." in kwargs["input"]
    assert kwargs["input"].endswith("How do heat pumps perform below -15C?")
    assert "tools" not in kwargs  # Google's default research tools


def test_defaults_show_thinking_and_allow_charts() -> None:
    kwargs = gra.build_research_kwargs(_config(), _PROFILE)
    assert kwargs["agent_config"]["thinking_summaries"] == "auto"
    assert kwargs["agent_config"]["visualization"] == "auto"


def test_web_search_off_is_honored() -> None:
    kwargs = gra.build_research_kwargs(_config(internal_web_search=False), _PROFILE)
    assert {"type": "google_search"} not in kwargs["tools"]
    assert {"type": "url_context"} in kwargs["tools"]


def test_follow_up_carries_earlier_turns() -> None:
    cfg = _config(
        messages=[
            {"role": "user", "content": "Research heat pumps."},
            {"role": "assistant", "content": "Report: they work."},
            {"role": "user", "content": "Now compare with gas furnaces."},
        ]
    )
    text = gra.research_input(cfg)
    assert text.endswith("Now compare with gas furnaces.")
    assert "Report: they work." in text


def test_no_user_text_is_refused_by_name() -> None:
    with pytest.raises(ValueError, match="needs a question"):
        gra.research_input(_config(messages=[{"role": "assistant", "content": "hi"}]))


def _finished(status: str = "completed") -> Any:
    return NS(
        id="int-1",
        status=status,
        output_text=None,
        errors=[],
        usage=NS(
            total_input_tokens=1200,
            total_output_tokens=800,
            total_thought_tokens=200,
            total_cached_tokens=100,
            total_tool_use_tokens=50,
            grounding_tool_count=None,
            model_dump=lambda **_: {"total_input_tokens": 1200},
        ),
        steps=[
            NS(type="thought", summary=[NS(type="text", text="Plan: search COP data.")]),
            NS(type="google_search_call", arguments=NS(queries=["heat pump COP -15C"])),
            NS(
                type="model_output",
                content=[
                    NS(
                        type="text",
                        text="Cold-climate units keep a COP near 2.",
                        annotations=[
                            {
                                "type": "url_citation",
                                "url": "https://example.org/neep",
                                "title": "NEEP list",
                                "start_index": 0,
                                "end_index": 10,
                            }
                        ],
                    ),
                    NS(
                        type="text",
                        text="Defrost cycles cost 10 percent.",
                        annotations=[
                            {
                                "type": "url_citation",
                                "url": "https://example.org/doe",
                                "title": "DOE",
                                "start_index": 0,
                                "end_index": 7,
                            }
                        ],
                    ),
                ],
            ),
        ],
    )


def test_usage_counts_thoughts_as_output_and_splits_cache() -> None:
    usage = gra.research_usage(
        _finished(), model_name="deep-research-preview-04-2026", provider_model_name="x"
    )
    assert usage is not None
    # input = total_input - cached + tool-use tokens (prompt the tools read back)
    assert usage.input_tokens == 1150 and usage.cached_input_tokens == 100
    assert usage.output_tokens == 1000
    assert usage.metadata["tool_use_tokens"] == 50
    assert usage.billing_components == {}


def _usage_with_grounding(grounding: list[dict[str, Any]]) -> Any:
    raw = {
        "total_input_tokens": 825_504,
        "total_cached_tokens": 172_032,
        "total_output_tokens": 14_352,
        "total_thought_tokens": 38_205,
        "total_tool_use_tokens": 73_728,
        "grounding_tool_count": grounding,
    }
    return NS(
        id="int-2",
        usage=NS(**{k: v for k, v in raw.items()}, model_dump=lambda **_: dict(raw)),
    )


_DEEP_RESEARCH_TIER = {
    "max_tokens": None,
    "input_price": 2.0,
    "output_price": 12.0,
    "cached_input_price": 0.2,
    "component_prices": {"service.google_search": 14000.0},
}


def _pricing_lookup() -> dict[str, Any]:
    from matrx_ai.config.usage_config import ModelPricing, PricingTier

    tier = PricingTier(
        max_tokens=None,
        input_price=2.0,
        output_price=12.0,
        cached_input_price=0.2,
        component_prices={"service.google_search": 14000.0},
    )
    return {"deep-research-preview-04-2026": ModelPricing("deep-research-preview-04-2026", "google", [tier])}


def test_real_run_usage_prices_at_gemini_list_rates_plus_search_fee() -> None:
    """The live 2026-09-26 run (chat.request bed17842) that recorded NO cost."""
    usage = gra.research_usage(
        _usage_with_grounding([{"type": "google_search", "count": 24}]),
        model_name="deep-research-preview-04-2026",
        provider_model_name="deep-research-preview-04-2026",
    )
    assert usage is not None
    assert usage.billing_components == {"service.google_search": 24}
    cost = usage.calculate_cost(_pricing_lookup())
    expected = (
        (825_504 - 172_032 + 73_728) / 1e6 * 2.0
        + 172_032 / 1e6 * 0.2
        + (14_352 + 38_205) / 1e6 * 12.0
        + 24 / 1e6 * 14000.0
    )
    assert cost == pytest.approx(expected)
    assert 2.0 < cost < 2.5  # $2.46 — inside Google's own $1-$3 estimate


def test_free_tool_calls_add_no_fee_and_unknown_tool_is_never_a_silent_zero() -> None:
    free = gra.research_usage(
        _usage_with_grounding([{"type": "url_context", "count": 9}]),
        model_name="deep-research-preview-04-2026",
        provider_model_name="x",
    )
    assert free is not None and free.billing_components == {}
    assert free.calculate_cost(_pricing_lookup()) is not None

    unknown = gra.research_usage(
        _usage_with_grounding([{"type": "google_maps", "count": 3}]),
        model_name="deep-research-preview-04-2026",
        provider_model_name="x",
    )
    assert unknown is not None
    assert unknown.billing_components == {"service.google_maps": 3}
    assert unknown.calculate_cost(_pricing_lookup()) is None
    assert unknown.metadata["cost_reconciliation"] == "unknown_component_price"


def test_offering_pricing_row_satisfies_the_pricing_validator() -> None:
    from matrx_ai.config.usage_config import validate_model_pricing

    caps = NS(
        produces_image=False,
        produces_video=False,
        produces_audio=False,
        supports_audio_input=False,
        supports_text_input=True,
        native_capabilities={"web_search", "file_search"},
    )
    assert validate_model_pricing(
        "deep-research-preview-04-2026", "google_interactions", caps, [_DEEP_RESEARCH_TIER],
        token_billed=False,
    ) == []
    missing = validate_model_pricing(
        "deep-research-preview-04-2026", "google_interactions", caps,
        [{**_DEEP_RESEARCH_TIER, "component_prices": {}}], token_billed=False,
    )
    assert [issue.code for issue in missing] == ["missing_service_price"]


def test_report_parts_join_and_citation_offsets_shift() -> None:
    content = asyncio.run(gra.research_content(_finished()))
    thinking = [c for c in content if isinstance(c, ThinkingContent)]
    text = [c for c in content if isinstance(c, TextContent)]
    assert thinking and thinking[0].text == "Plan: search COP data."
    assert len(text) == 1
    report = text[0].text
    second = report.index("Defrost")
    cites = text[0].metadata["citations"]
    assert [c["url"] for c in cites] == ["https://example.org/neep", "https://example.org/doe"]
    assert cites[0]["answer_start"] == 0 and cites[0]["kind"] == "web"
    assert cites[1]["answer_start"] == second and cites[1]["answer_end"] == second + 7


class _Stream:
    def __init__(self, events: list[Any], fail_after: bool = False) -> None:
        self._events = events
        self._fail_after = fail_after

    def __aiter__(self) -> _Stream:
        self._iter = iter(self._events)
        return self

    async def __anext__(self) -> Any:
        try:
            return next(self._iter)
        except StopIteration:
            if self._fail_after:
                self._fail_after = False
                raise ConnectionError("stream dropped") from None
            raise StopAsyncIteration from None


class _FakeInteractions:
    def __init__(self, final: Any) -> None:
        self.final = final
        self.created: dict[str, Any] | None = None
        self.resumed_from: str | None = None
        self.cancelled: list[str] = []

    async def create(self, **kwargs: Any) -> _Stream:
        self.created = kwargs
        return _Stream(
            [
                NS(event_type="interaction.created", event_id="e1", interaction=NS(id="int-1", status="in_progress")),
                NS(
                    event_type="step.delta",
                    event_id="e2",
                    delta=NS(type="thought_summary", content=NS(type="text", text="Planning")),
                ),
            ],
            fail_after=True,
        )

    async def get(self, id: str, stream: bool = False, last_event_id: str | None = None) -> Any:
        if stream:
            self.resumed_from = last_event_id
            return _Stream(
                [
                    NS(event_type="step.delta", event_id="e3", delta=NS(type="text", text="Cold-climate")),
                    NS(event_type="interaction.completed", event_id="e4", interaction=NS(id=id, status="completed")),
                ]
            )
        return self.final

    async def cancel(self, id: str) -> None:
        self.cancelled.append(id)


class _Emitter:
    def __init__(self) -> None:
        self.chunks: list[str] = []
        self.infos: list[str] = []
        self.reasoning: list[str] = []
        self.data: list[Any] = []

    async def send_chunk(self, text: str) -> None:
        self.chunks.append(text)

    async def send_info(self, payload: Any) -> None:
        self.infos.append(payload.code)

    async def send_reasoning_state(self, state: str) -> None:
        self.reasoning.append(state)

    async def send_data(self, payload: Any) -> None:
        self.data.append(payload)


def _run(agent: gra.GoogleDeepResearchAgent, fake: _FakeInteractions, emitter: _Emitter) -> Any:
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

    async def go() -> Any:
        token = set_app_context(AppContext(emitter=emitter, user_id="research-test"))
        try:
            return await agent.execute(_config(), _PROFILE)
        finally:
            clear_app_context(token)

    type(agent)._interactions = property(lambda self: fake)  # type: ignore[assignment]
    return asyncio.run(go())


def test_turn_streams_resumes_after_a_drop_and_returns_the_report() -> None:
    fake = _FakeInteractions(_finished())
    emitter = _Emitter()
    response = _run(gra.GoogleDeepResearchAgent(), fake, emitter)
    assert fake.created is not None and fake.created["stream"] is True
    assert fake.resumed_from == "e2"  # resumed exactly where the stream dropped
    assert "Cold-climate" in emitter.chunks
    assert any("Planning" in c for c in emitter.chunks)
    assert emitter.reasoning == ["started", "stopped"]
    assert "research_started" in emitter.infos
    message = response.messages[0]
    assert any(isinstance(c, TextContent) for c in message.content)
    assert response.usage.output_tokens == 1000


def test_failed_research_is_never_retried_and_carries_billed_usage() -> None:
    from matrx_ai.providers.errors import get_billed_usage

    fake = _FakeInteractions(_finished(status="failed"))
    with pytest.raises(gra.DeepResearchFailed) as info:
        _run(gra.GoogleDeepResearchAgent(), fake, _Emitter())
    assert info.value.error_info.is_retryable is False
    billed = get_billed_usage(info.value)
    assert billed is not None and billed.input_tokens == 1150


class _Admission:
    async def __aenter__(self) -> _Admission:
        return self

    async def __aexit__(self, *_args: Any) -> bool:
        return False


def _research_profile(wire_format: str = "google_interactions") -> Any:
    return NS(
        wire_format=wire_format,
        client_attr=wire_format,
        capabilities=NS(interaction="agent"),
        byok_secret_key=None,
        provider_model_id="deep-research-preview-04-2026",
        model_name="deep-research-preview-04-2026",
        vendor="google",
        endpoint_id="endpoint-google",
        api_id="api-interactions",
        offering_id="offering-deep-research",
        resolution_route="pinned",
    )


def test_an_agent_turn_on_a_research_model_reaches_the_research_translator(monkeypatch) -> None:
    """Before 2026-09-26 this model's wire (google_interactions) sent an agent
    turn to the VIDEO generator. The research model must reach the research
    translator, and nothing else."""
    from matrx_ai.catalog import resolve as resolve_mod
    from matrx_ai.config import UnifiedResponse
    from matrx_ai.orchestrator.requests import AIMatrixRequest
    from matrx_ai.providers import admission
    from matrx_ai.providers.unified_client import UnifiedAIClient

    async def _profile(*_a: Any, **_k: Any) -> Any:
        return _research_profile()

    monkeypatch.setattr(resolve_mod, "resolve_tts_call_profile", _profile)
    monkeypatch.setattr(admission, "admit_provider_call", lambda _p: _Admission())
    seen: list[str] = []

    class _Research:
        async def execute(self, config: Any, profile: Any, debug: bool = False) -> Any:
            seen.append(profile.model_name)
            return UnifiedResponse(messages=[], usage=None)

    client = UnifiedAIClient()

    async def _get(name: str) -> Any:
        assert name == "google_research_agent", f"research turn routed to {name!r}"
        return _Research()

    monkeypatch.setattr(client, "_get_provider_client", _get)
    request = AIMatrixRequest(config=_config(), conversation_id="conv-research-test")
    asyncio.run(client.execute(request))
    assert seen == ["deep-research-preview-04-2026"]


def test_a_managed_agent_on_another_wire_is_refused_by_name(monkeypatch) -> None:
    from matrx_ai.catalog import resolve as resolve_mod
    from matrx_ai.orchestrator.requests import AIMatrixRequest
    from matrx_ai.providers.unified_client import UnifiedAIClient

    async def _profile(*_a: Any, **_k: Any) -> Any:
        return _research_profile("some_other_agents_api")

    monkeypatch.setattr(resolve_mod, "resolve_tts_call_profile", _profile)
    with pytest.raises(ValueError, match="provider-managed agent"):
        asyncio.run(UnifiedAIClient().execute(AIMatrixRequest(config=_config(), conversation_id="conv-research-test")))


def test_a_chart_that_cannot_be_stored_never_costs_the_report(monkeypatch) -> None:
    """Live 2026-09-26: storage refused a generated chart and the finished,
    paid report was thrown away with it. The report survives and says so."""
    import base64

    from matrx_ai.config import ImageContent

    async def _refuse(*_a: Any, **_k: Any) -> Any:
        raise RuntimeError("storage refused the upload")

    monkeypatch.setattr(ImageContent, "from_google_async", _refuse)
    finished = _finished()
    finished.steps[-1].content.append(
        NS(type="image", data=base64.b64encode(b"\x89PNG fake").decode(), mime_type="image/png")
    )
    content = asyncio.run(gra.research_content(finished))
    text = [c for c in content if isinstance(c, TextContent)][0].text
    assert "Cold-climate units keep a COP near 2." in text
    assert "1 chart(s) the research produced could not be saved" in text
    assert not any(isinstance(c, ImageContent) for c in content)


def test_thought_summaries_share_one_reasoning_block() -> None:
    fake = _FakeInteractions(_finished())
    emitter = _Emitter()
    _run(gra.GoogleDeepResearchAgent(), fake, emitter)
    stream = "".join(emitter.chunks)
    assert stream.count("<reasoning>") == 1 and stream.count("</reasoning>") == 1
    assert stream.index("</reasoning>") < stream.index("Cold-climate")


def test_inline_markdown_links_become_structured_citations_when_google_annotates_nothing() -> None:
    """Live 2026-09-26 (interaction v1_ChdPcEMz…): the brief asked for inline links,
    Google returned 0 annotations, and the model fenced every link in backticks —
    the stored message carried no citations and the viewer showed code, not links."""
    report = (
        "**Answer** HR 0.69 `([NEJM 2018](https://example.org/nejm))` and "
        "0.70 ([PDF](https://example.org/pdf.pdf)); again ([NEJM 2018](https://example.org/nejm))."
    )
    interaction = NS(
        id="int-3",
        output_text=None,
        steps=[NS(type="model_output", content=[NS(type="text", text=report, annotations=None)])],
    )
    content = asyncio.run(gra.research_content(interaction))
    text = [c for c in content if isinstance(c, TextContent)][0]
    assert "`" not in text.text  # the code span around the link is gone
    cites = text.metadata["citations"]
    assert [c["url"] for c in cites] == [
        "https://example.org/nejm",
        "https://example.org/pdf.pdf",
        "https://example.org/nejm",
    ]
    assert [c["source_index"] for c in cites] == [0, 1, 0]
    first = cites[0]
    assert first["kind"] == "web" and first["title"] == "NEJM 2018"
    assert text.text[first["answer_start"] : first["answer_end"]] == "[NEJM 2018](https://example.org/nejm)"


def test_annotated_report_is_left_exactly_as_google_sent_it() -> None:
    content = asyncio.run(gra.research_content(_finished()))
    text = [c for c in content if isinstance(c, TextContent)][0]
    assert all(c.get("raw", {}).get("type") != "markdown_link" for c in text.metadata["citations"])


def test_only_deep_research_agents_ride_the_research_translator() -> None:
    """The Interactions wire also serves the Antigravity sandbox agent, which
    takes a different agent_config — it must never be sent as a research run."""
    assert gra.is_google_research_agent("deep-research-preview-04-2026")
    assert gra.is_google_research_agent("deep-research-max-preview-04-2026")
    assert not gra.is_google_research_agent("antigravity-preview-05-2026")
    assert not gra.is_google_research_agent(None)
