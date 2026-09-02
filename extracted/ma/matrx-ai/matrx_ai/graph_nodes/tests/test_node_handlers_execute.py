"""Execute every registered ``ai.*`` / ``human.*`` node handler for real.

``test_graph_nodes.py::test_register_with_graph_populates_default_registry``
only asserted that a node's NAME is in the registry — it never called the
handler. ``ai.conversation.continue`` raised ``AttributeError`` on every
single invocation for four months (``conversation_action.py:80`` read
``.config`` off a ``UnifiedConfig`` that has no such attribute — see
``common-docs/systems/workflows/NODE_API_PARITY.md``, "Finding Zero") and
that test suite stayed green the entire time.

This file is the fix one level up: it ENUMERATES the live action registry
(``default_action_registry().names()``) at collection time and, for every
name found, calls the REAL registered handler (via
``resolve_action_executor`` — the same adapter the scheduler and
``tool.call`` use) with a minimal, structurally-valid input. Only the
external boundary is mocked — the provider call (``execute_ai_request``,
the ``_strict_json`` primitives that route through it, or a host-injected
ext like ``agent_runner`` / ``brave_search`` / STT) — never the handler's
own body. A newly-registered node is picked up automatically the next time
this file runs; it does not need a hand-edited list here.

A node's handler is executed via a fixture registered in
``NODE_FIXTURES`` below. A node with NO fixture entry SKIPS LOUDLY, naming
the node and the reason — never silently, so an unfixtured node can never
read as "covered" in a green run. Today's one loud skip is
``ai.agent.assignment_batch`` (needs a durable ``AssignmentCoordinator``
session store behind a host-injected ``assignment_store_factory`` — out of
reach of a minimal in-process fixture).

Detection covers two shapes of "structural bug slipped through":

1. A raised ``AttributeError`` / ``TypeError`` / ``NameError`` /
   ``ImportError`` escaping the handler — Finding Zero's exact shape.
2. The SAME class of bug caught by one of the handler's own broad
   ``except Exception`` blocks (several nodes — ``ai.scrape.web``,
   ``ai.search.brave``, ``ai.generate_image``, ``ai.text_to_speech`` —
   convert ANY exception into a clean-looking ``Failure`` envelope whose
   message is ``f"{type(e).__name__}: {e}"``). A raised exception is caught
   here; a swallowed one is caught by inspecting the returned envelope.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Callable
from typing import Any, get_args, get_origin

import pytest
from pydantic import BaseModel

from matrx_graph.actions.decorator import resolve_action_executor
from matrx_graph.actions.registry import default_action_registry
from matrx_graph.errors import GraphInterrupt
from matrx_graph.types.context import ChannelView, NodeExecutionContext
from matrx_graph.types.node_spec import EmptyConfig
from matrx_graph.types.result import Failure, Success

from matrx_ai import _ext
from matrx_ai.graph_nodes import register_with_graph

register_with_graph()  # idempotent — make sure matrx-ai's nodes are registered

# ---------------------------------------------------------------------------
# Structural-error detection
# ---------------------------------------------------------------------------

_STRUCTURAL_ERROR_TYPES: tuple[type[BaseException], ...] = (
    AttributeError,
    TypeError,
    NameError,
    ImportError,
)
_STRUCTURAL_TYPE_NAMES = tuple(t.__name__ for t in _STRUCTURAL_ERROR_TYPES)


def _assert_no_hidden_structural_error(node_name: str, result: Any) -> None:
    """Catch a structural bug a handler's own try/except swallowed.

    Several handlers wrap their body in ``except Exception as e: return
    failure(code, f"{type(e).__name__}: {e}", ...)`` — a legitimate pattern
    for a real provider failure, but it also hides a Finding-Zero-class bug
    behind a clean-looking Failure envelope. If the message names one of the
    structural exception types, treat it exactly like an escaped raise.
    """
    if not isinstance(result, Failure):
        return
    message = result.error.message
    if message.startswith(_STRUCTURAL_TYPE_NAMES):
        pytest.fail(
            f"{node_name}: handler swallowed a structural error into its "
            f"Failure envelope — error.code={result.error.code!r} "
            f"message={message!r}. This is the Finding Zero shape (an "
            "AttributeError/TypeError/NameError/ImportError caught by a "
            "broad except-Exception and repackaged as a clean-looking "
            "failure) — fix the handler, not this test."
        )


# ---------------------------------------------------------------------------
# Generic minimal-instance filler — used to build canned LLM/tool return
# values for output_cls models the mocked primitive must hand back.
# ---------------------------------------------------------------------------


def _minimal_value(annotation: Any) -> Any:
    origin = get_origin(annotation)
    if origin in (list,):
        return []
    if origin in (dict,):
        return {}
    if origin is not None:  # Optional[...] / X | Y / other typing generics
        args = [a for a in get_args(annotation) if a is not type(None)]
        return _minimal_value(args[0]) if args else None
    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return _minimal_model(annotation)
    if annotation is str:
        return "x"
    if annotation is int:
        return 0
    if annotation is float:
        return 0.0
    if annotation is bool:
        return False
    return None


def _minimal_model(model_cls: type[BaseModel]) -> BaseModel:
    """Build a structurally-valid instance using the simplest legal value for
    every required field. Good enough as a canned LLM/tool response for
    exercising the code AROUND the call — not a substitute for testing the
    model's own validation rules."""
    kwargs = {}
    for name, field in model_cls.model_fields.items():
        if not field.is_required():
            continue
        kwargs[name] = _minimal_value(field.annotation)
    return model_cls(**kwargs)


# ---------------------------------------------------------------------------
# Shared fakes
# ---------------------------------------------------------------------------


class _PermissiveEmitter:
    """Answers any emitter method with an async no-op — a node's own choice
    of emitter method name is not what this suite is checking."""

    async def _noop(self, *_a: Any, **_k: Any) -> None:
        return None

    def __getattr__(self, _name: str) -> Callable[..., Any]:
        return self._noop


@dataclasses.dataclass
class _FakeUnifiedResponse:
    text: str = "ok"
    finish_reason: str | None = "stop"


@dataclasses.dataclass
class _FakeConfig:
    messages: list[dict[str, Any]] = dataclasses.field(
        default_factory=lambda: [{"role": "user", "content": "hi"}]
    )

    def get_last_output(self) -> str:
        # ai.extract reads the final text through this method, not
        # final_response.text — matched here so extraction has real JSON to
        # parse instead of failing the fixture, not the node, on a KeyError.
        return '{"ok": true}'


@dataclasses.dataclass
class _FakeRequest:
    conversation_id: str = "conv-1"
    request_id: str = "req-1"
    config: _FakeConfig = dataclasses.field(default_factory=_FakeConfig)


@dataclasses.dataclass
class _FakeTotals:
    input_tokens: int = 10
    output_tokens: int = 20
    total_tokens: int = 30
    cost_usd: float = 0.01


@dataclasses.dataclass
class _FakeUsage:
    totals: _FakeTotals = dataclasses.field(default_factory=_FakeTotals)


@dataclasses.dataclass
class _FakeCompleted:
    """Shape a ``CompletedRequest`` — matches ``normalize_completed``'s
    contract (see ``test_graph_nodes.py``) and is tolerant enough (every
    field read through ``getattr`` with a default) to also serve the
    media-generation nodes (image/tts/video), which read
    ``final_response``/``total_usage`` directly."""

    request: _FakeRequest = dataclasses.field(default_factory=_FakeRequest)
    iterations: int = 1
    final_response: _FakeUnifiedResponse = dataclasses.field(
        default_factory=_FakeUnifiedResponse
    )
    total_usage: _FakeUsage = dataclasses.field(default_factory=_FakeUsage)
    timing_stats: dict[str, Any] = dataclasses.field(default_factory=dict)
    tool_call_stats: dict[str, Any] = dataclasses.field(default_factory=dict)
    metadata: dict[str, Any] = dataclasses.field(default_factory=dict)


def _ctx(*, organization_id: str = "test-org", output_kind: str | None = None) -> NodeExecutionContext:
    from matrx_connect.context.app_context import AppContext

    return NodeExecutionContext(
        app=AppContext(
            emitter=_PermissiveEmitter(),
            user_id="test-user",
            is_authenticated=True,
            conversation_id="test-conv",
            request_id="test-req",
            organization_id=organization_id,
        ),
        run_id="run-1",
        thread_id="run-1",
        node_id="test-node",
        step=0,
        attempt=1,
        channels=ChannelView(_values={}, _pending_writes=[]),
        checkpointer=None,
        output_kind=output_kind,
    )


class _PermissiveHostRequest(BaseModel):
    """Stand-in for a host-owned strict request model (``AgentStartRequest``,
    ``ConversationContinueRequest``, ...). ``extra='allow'`` because this
    suite is exercising matrx-ai's OWN code up to the host boundary — the
    host's own request validation is that host's test surface, not this
    package's."""

    model_config = {"extra": "allow"}


def _patch_execute_ai_request(monkeypatch: pytest.MonkeyPatch, *, completed: Any = None) -> None:
    """Patch the ONE underlying primitive every LLM-calling node (chat,
    extract, agent-loop, image, tts, video) routes through, directly or via
    the ``_strict_json`` helpers — all of them do
    ``from matrx_ai.orchestrator.executor import execute_ai_request`` INSIDE
    the function body, so patching the attribute on the defining module is
    picked up at every call site without patching each node module."""
    from matrx_ai.orchestrator import executor as executor_module

    async def _fake_execute_ai_request(*_a: Any, **_k: Any) -> Any:
        return completed if completed is not None else _FakeCompleted()

    monkeypatch.setattr(executor_module, "execute_ai_request", _fake_execute_ai_request)


def _patch_agent_host(monkeypatch: pytest.MonkeyPatch, *, completed: Any = None) -> dict[str, Any]:
    """Stand in for the host's ``agent_runner`` + ``AgentStartRequest`` ext —
    the same seam ``ai.agent.start`` / ``ai.agent.produce`` /
    ``ai.agent.assignment_batch`` call through (``agent_action.py:587``)."""
    sent: dict[str, Any] = {}

    async def _agent_runner(agent_id: str, request: Any, _app: Any) -> Any:
        sent["agent_id"] = agent_id
        sent["request"] = request
        return completed if completed is not None else _FakeCompleted()

    monkeypatch.setitem(_ext._registry, "agent_runner", _agent_runner)
    monkeypatch.setitem(_ext._registry, "AgentStartRequest", _PermissiveHostRequest)
    return sent


# ---------------------------------------------------------------------------
# NODE_FIXTURES — name -> (monkeypatch) -> (inputs, ctx)
# ---------------------------------------------------------------------------

NODE_FIXTURES: dict[str, Callable[[pytest.MonkeyPatch], tuple[BaseModel, NodeExecutionContext]]] = {}


def node_fixture(name: str) -> Callable[[Callable], Callable]:
    def _register(fn: Callable) -> Callable:
        NODE_FIXTURES[name] = fn
        return fn

    return _register


@node_fixture("ai.llm.chat")
def _fx_llm_chat(monkeypatch):
    from matrx_ai.graph_nodes.llm_action import LlmChatInput

    _patch_execute_ai_request(monkeypatch)
    return LlmChatInput(model="gpt-5", prompt="hello"), _ctx()


@node_fixture("ai.chat.manual")
def _fx_chat_manual(monkeypatch):
    from matrx_ai.graph_nodes.chat_action import ChatManualInput

    _patch_execute_ai_request(monkeypatch)
    return ChatManualInput(model="claude-opus-4-7"), _ctx()


@node_fixture("ai.extract")
def _fx_extract(monkeypatch):
    from matrx_ai.graph_nodes.extract_action import ExtractInput

    _patch_execute_ai_request(monkeypatch)
    return (
        ExtractInput(text="the total is $5", instruction="extract the total"),
        _ctx(),
    )


@node_fixture("ai.agent.tool_calling")
def _fx_agent_tool_calling(monkeypatch):
    from matrx_ai.graph_nodes.agent_loop_actions import AgentLoopInput

    _patch_execute_ai_request(monkeypatch)
    return AgentLoopInput(model="gpt-5", user_input="do the thing"), _ctx()


@node_fixture("ai.agent.react")
def _fx_agent_react(monkeypatch):
    from matrx_ai.graph_nodes.agent_loop_actions import AgentLoopInput

    _patch_execute_ai_request(monkeypatch)
    return AgentLoopInput(model="gpt-5", user_input="reason about the thing"), _ctx()


@node_fixture("ai.agent.start")
def _fx_agent_start(monkeypatch):
    from matrx_ai.graph_nodes.agent_action import AgentStartInput

    _patch_agent_host(monkeypatch)
    return (
        AgentStartInput(agent_id="11111111-2222-3333-4444-555555555555", user_input="hi"),
        _ctx(),
    )


@node_fixture("ai.agent.produce")
def _fx_agent_produce(monkeypatch):
    from matrx_ai.graph_nodes import agent_produce_action
    from matrx_ai.graph_nodes.agent_produce_action import AgentProduceInput

    # agent_id (not mandate_key) skips the whole mandate-resolver seam —
    # resolve_step_agent_full returns declared_output_kind=None, and
    # _assert_declarations_agree treats "mandate declares nothing" as
    # non-contradictory (just a warning), so the node reaches the real
    # response_format binding + agent_runner call this test wants to exercise.
    monkeypatch.setattr(agent_produce_action, "is_bindable_kind", lambda _k: True)

    async def _fake_response_format_for_kind(_kind: str) -> Any:
        class _Bound:
            def model_dump(self, **_kw: Any) -> dict[str, Any]:
                return {"type": "json_schema", "json_schema": {"name": "x", "schema": {}}}

        return _Bound()

    monkeypatch.setattr(
        agent_produce_action, "response_format_for_kind", _fake_response_format_for_kind
    )
    _patch_agent_host(monkeypatch)
    return (
        AgentProduceInput(agent_id="11111111-2222-3333-4444-555555555555", user_input="hi"),
        _ctx(output_kind="some_kind"),
    )


@node_fixture("ai.conversation.continue")
def _fx_conversation_continue(monkeypatch):
    from matrx_ai.graph_nodes.conversation_action import ConversationContinueInput

    async def _fake_continuer(_conversation_id: str, _request: Any, _app: Any) -> Any:
        return _FakeCompleted()

    monkeypatch.setitem(_ext._registry, "conversation_continuer", _fake_continuer)
    monkeypatch.setitem(_ext._registry, "ConversationContinueRequest", _PermissiveHostRequest)
    return (
        ConversationContinueInput(conversation_id="conv-1", user_input="continue please"),
        _ctx(),
    )


@node_fixture("ai.generate_image")
def _fx_generate_image(monkeypatch):
    from matrx_ai.graph_nodes.image_action import GenerateImageInput

    _patch_execute_ai_request(monkeypatch)
    return GenerateImageInput(model="dall-e-3", prompt="a red bicycle"), _ctx()


@node_fixture("ai.text_to_speech")
def _fx_tts(monkeypatch):
    from matrx_ai.graph_nodes.tts_action import TextToSpeechInput

    _patch_execute_ai_request(monkeypatch)
    return TextToSpeechInput(model="eleven_v3", text="hello there"), _ctx()


@node_fixture("ai.generate_video")
def _fx_generate_video(monkeypatch):
    from matrx_ai.graph_nodes.video_action import GenerateVideoInput

    _patch_execute_ai_request(monkeypatch)
    return GenerateVideoInput(model="veo-3.1-generate-preview", prompt="a sunrise"), _ctx()


@node_fixture("ai.edit_video")
def _fx_edit_video(monkeypatch):
    from matrx_ai.graph_nodes.video_action import EditVideoInput

    _patch_execute_ai_request(monkeypatch)
    return (
        EditVideoInput(
            model="grok-imagine-video",
            prompt="make it night",
            video_input_url="https://example.com/v.mp4",
        ),
        _ctx(),
    )


@node_fixture("ai.extend_video")
def _fx_extend_video(monkeypatch):
    from matrx_ai.graph_nodes.video_action import ExtendVideoInput

    _patch_execute_ai_request(monkeypatch)
    return (
        ExtendVideoInput(
            model="sora-2",
            prompt="keep going",
            video_input_url="https://example.com/v.mp4",
        ),
        _ctx(),
    )


@node_fixture("ai.image.concept_generate")
def _fx_image_concept_generate(monkeypatch):
    from matrx_ai.graph_nodes import image_pipeline_actions
    from matrx_ai.graph_nodes.image_pipeline_actions import ConceptGenerateInput

    async def _fake_llm_to_pydantic(*, output_cls: type[BaseModel], **_kw: Any) -> BaseModel:
        return _minimal_model(output_cls)

    monkeypatch.setattr(image_pipeline_actions, "llm_to_pydantic", _fake_llm_to_pydantic)
    return ConceptGenerateInput(topic="photosynthesis"), _ctx()


@node_fixture("ai.image.prompt_write")
def _fx_image_prompt_write(monkeypatch):
    from matrx_ai.graph_nodes import image_pipeline_actions
    from matrx_ai.graph_nodes.image_pipeline_actions import ImageConcept, PromptWriteInput

    async def _fake_llm_to_pydantic(*, output_cls: type[BaseModel], **_kw: Any) -> BaseModel:
        return _minimal_model(output_cls)

    monkeypatch.setattr(image_pipeline_actions, "llm_to_pydantic", _fake_llm_to_pydantic)
    concept = ImageConcept(name="Leaf cell", description="A cross-section of a leaf cell")
    return PromptWriteInput(concept=concept), _ctx()


@node_fixture("ai.image.qc_judge")
def _fx_image_qc_judge(monkeypatch):
    from matrx_ai.graph_nodes import image_pipeline_actions
    from matrx_ai.graph_nodes.image_pipeline_actions import ImageQcInput, ImageQcVerdict

    async def _fake_llm_messages_to_pydantic(*, output_cls: type[BaseModel], **_kw: Any) -> BaseModel:
        assert output_cls is ImageQcVerdict
        return ImageQcVerdict(passed=True, confidence=0.9, reasoning="looks fine")

    monkeypatch.setattr(
        image_pipeline_actions, "llm_messages_to_pydantic", _fake_llm_messages_to_pydantic
    )
    return (
        # api_key set directly so the node never calls resolve_api_key
        # (which would otherwise need a real env var); image_b64 skips the
        # cloud-FileManager URL-resolution branch entirely.
        ImageQcInput(image_b64="QUJD", api_key="test-key"),
        _ctx(),
    )


@node_fixture("ai.transcribe")
def _fx_transcribe(monkeypatch):
    from matrx_ai.processing.audio import stt as stt_module
    from matrx_ai.graph_nodes.transcribe_action import TranscribeInput

    class _FakeTokenUsage:
        def calculate_cost(self) -> float:
            return 0.001

    class _FakeSTTUsage:
        duration_seconds = 1.5
        matrx_model_name = "whisper-fake"

        def to_token_usage(self) -> Any:
            return _FakeTokenUsage()

    class _FakeSTTResult:
        text = "hello world"
        language = "en"
        duration = 1.5
        usage = _FakeSTTUsage()

    async def _fake_execute_stt(_request: Any) -> Any:
        return _FakeSTTResult()

    monkeypatch.setattr(stt_module, "execute_stt", _fake_execute_stt)
    return TranscribeInput(audio_source="/tmp/fake.wav"), _ctx()


@node_fixture("ai.search.brave")
def _fx_search_brave(monkeypatch):
    from matrx_ai.graph_nodes.search_action import BraveSearchInput

    async def _fake_async_brave_search(**_kw: Any) -> dict[str, Any]:
        return {"web": {"results": []}, "news": {"results": []}}

    monkeypatch.setitem(
        _ext._registry, "brave_search", {"async_brave_search": _fake_async_brave_search}
    )
    return BraveSearchInput(query="photosynthesis"), _ctx()


@node_fixture("ai.scrape.web")
def _fx_scrape_web(monkeypatch):
    from matrx_ai.graph_nodes.scrape_action import WebScrapeInput

    try:
        from matrx_scraper.features import read_page as read_page_module
    except ImportError:
        pytest.skip(
            "ai.scrape.web: matrx_scraper is not installed in this test "
            "environment — the node's own try/except would swallow the "
            "resulting ImportError into a Failure, which is real coverage "
            "this suite cannot fake without the package present."
        )

    async def _fake_read_page_mcp_quick(**_kw: Any) -> dict[str, Any]:
        return {"content": "page text", "is_good_scrape": True}

    monkeypatch.setattr(read_page_module, "read_page_mcp_quick", _fake_read_page_mcp_quick)
    return WebScrapeInput(url="https://example.com"), _ctx()


@node_fixture("ai.util.extract_search_urls")
def _fx_util_extract_search_urls(_monkeypatch):
    from matrx_ai.graph_nodes.util_action import ExtractSearchUrlsInput

    return (
        ExtractSearchUrlsInput(values=[{"results": [{"url": "https://example.com"}]}]),
        _ctx(),
    )


@node_fixture("ai.util.format_scraped_content")
def _fx_util_format_scraped_content(_monkeypatch):
    from matrx_ai.graph_nodes.util_action import FormatScrapedContentInput

    return (
        FormatScrapedContentInput(
            values=[{"url": "https://example.com", "text": "some page content"}]
        ),
        _ctx(),
    )


@node_fixture("ai.util.cost_summary")
def _fx_util_cost_summary(_monkeypatch):
    from matrx_ai.graph_nodes.util_action import CostSummaryInput

    # No conversation_id and no ctx.app.conversation_id override means the
    # node takes its early all-zero return WITHOUT touching the DB — the
    # cxm/get_model path is real DB access this fixture deliberately avoids.
    ctx = _ctx()
    return CostSummaryInput(), dataclasses.replace(ctx, app=ctx.app.with_overrides(conversation_id=""))


@node_fixture("ai.util.parse_llm_json")
def _fx_util_parse_llm_json(_monkeypatch):
    from matrx_ai.graph_nodes.util_action import ParseLlmJsonInput

    return ParseLlmJsonInput(text='{"answer": 42}'), _ctx()


# ---------------------------------------------------------------------------
# The sweep
# ---------------------------------------------------------------------------

_ALL_REGISTERED_NAMES = sorted(a.name for a in default_action_registry().all())


@pytest.mark.asyncio
@pytest.mark.parametrize("node_name", _ALL_REGISTERED_NAMES)
async def test_node_handler_executes_without_structural_error(node_name, monkeypatch):
    fixture = NODE_FIXTURES.get(node_name)
    if fixture is None:
        pytest.skip(
            f"NO FIXTURE REGISTERED for node {node_name!r} in "
            "NODE_FIXTURES (test_node_handlers_execute.py) — this is a named "
            "gap, not a silent pass. Add a fixture before shipping, or leave "
            "this skip if the node genuinely cannot be driven in-process "
            "(name the reason at the call site if you do)."
        )

    inputs, ctx = fixture(monkeypatch)
    executor = resolve_action_executor(node_name)

    try:
        result = await executor.execute(ctx, inputs, EmptyConfig())
    except GraphInterrupt:
        # Legitimate control flow (a node that parks for a person) — not a
        # structural failure.
        return
    except _STRUCTURAL_ERROR_TYPES as exc:
        pytest.fail(
            f"{node_name}: handler raised a structural error — "
            f"{type(exc).__name__}: {exc}. This is exactly Finding Zero's "
            "shape (a code path that has never actually executed)."
        )

    assert isinstance(result, Success | Failure), (
        f"{node_name}: handler returned {type(result).__name__}, not a "
        "NodeResult envelope (Success/Failure) — every action MUST return "
        "success(...)/failure(...)."
    )
    _assert_no_hidden_structural_error(node_name, result)


def test_every_registered_node_is_either_fixtured_or_named_as_skipped():
    """A second, cheap assertion that the sweep above is complete: every
    name the registry currently knows about is accounted for in this file
    (fixtured, or explicitly acknowledged as unfixtured via the parametrized
    test's loud skip). Fails at COLLECTION-adjacent time if the registry is
    empty (register_with_graph() silently did nothing), which the
    parametrized test alone would not surface — an empty parametrize list
    just collects zero tests."""
    assert _ALL_REGISTERED_NAMES, "the action registry is empty — register_with_graph() did not run"
    known_unfixtured = {"ai.agent.assignment_batch"}
    missing = set(_ALL_REGISTERED_NAMES) - set(NODE_FIXTURES) - known_unfixtured
    assert not missing, (
        f"node(s) {sorted(missing)} have no NODE_FIXTURES entry and are not "
        "in known_unfixtured — every registered node must be either "
        "fixtured or explicitly named here with a reason."
    )
