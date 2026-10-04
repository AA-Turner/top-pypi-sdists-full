"""THE call-time tool adaptation (TOOL-SOURCES.md rule L): the core never reads the model,
and every tool a model/provider limit removes is ANNOUNCED.

Arman, 2026-10-03: the core prepares a call without concern for the specific model; a
separate late layer adapts it, and every removal is announced to the person/creator. A
model's only tool fact is ``supports_function_calling``.

Before this, three core paths read ``config.supports_tools`` and silently built NO tools for
a model without function calling (``apply_unified_tools``' early return,
``merge_request_tools``' gate, ``inject_editable_tools``' gate), and the provider boundary
stripped tools with a console line only — the person was never told.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from matrx_connect import AppContext
from matrx_connect.context.app_context import _app_context, set_app_context

from matrx_ai.config import UnifiedConfig
from matrx_ai.orchestrator.snapshot_metadata import REQUEST_SNAPSHOT_METADATA_KEY
from matrx_ai.providers import tool_adaptation, unified_client
from matrx_ai.providers.unified_client import UnifiedAIClient
from matrx_ai.testing.profile_factory import make_profile
from matrx_ai.tools.merge import merge_request_tools
from matrx_ai.tools.specs import RegisteredToolSpec

# A real live text model that declares no function calling (ai.model_public, 2026-10-03).
_NO_FC_CAPS = {
    "input": ["text"],
    "output": ["text"],
    "features": ["json_mode", "structured_output"],
    "interaction": "turn",
}
_FC_CAPS = {**_NO_FC_CAPS, "features": ["function_calling", "json_mode", "structured_output"]}


@pytest.fixture(autouse=True)
def _no_gate_findings_cross_tests():
    """Gate findings held by a gate run here never leak into a later test's flush."""
    from matrx_ai.providers.structured_output_findings import _GATE_PENDING

    token = _GATE_PENDING.set(None)
    yield
    _GATE_PENDING.reset(token)


class _Emitter:
    def __init__(self) -> None:
        self.warnings: list[Any] = []

    async def send_warning(self, payload: Any) -> None:
        self.warnings.append(payload)

    async def send_info(self, payload: Any) -> None:  # pragma: no cover - not under test
        pass

    async def send_chunk(self, *_a: Any, **_k: Any) -> None:  # pragma: no cover
        pass


def _config(supports_tools: bool) -> UnifiedConfig:
    config = UnifiedConfig.from_dict(
        {
            "model": "deepseek-ai/DeepSeek-V3",
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": "Summarise the lease."}]}
            ],
        }
    )
    config.supports_tools = supports_tools
    return config


def _core_toolset(supports_tools: bool) -> list[str]:
    """What the core builds: the agent's tools plus a request-path injection."""
    config = _config(supports_tools)
    config.tools = ["web_search", "document_content"]
    merge_request_tools(
        config,
        AppContext(emitter=None),
        [RegisteredToolSpec(name="context"), RegisteredToolSpec(name="knowledge_search")],
    )
    return sorted(config.tools)


def test_the_core_toolset_is_the_same_for_a_model_without_function_calling() -> None:
    capable = _core_toolset(True)
    assert capable == ["context", "document_content", "knowledge_search", "web_search"]
    assert _core_toolset(False) == capable


async def _run_dispatch(
    monkeypatch: pytest.MonkeyPatch, caps: dict[str, Any], *, web_search: bool = False
):
    """Drive the REAL ``_execute_dispatch`` to the provider client and capture the wire."""
    profile = make_profile(model_name="deepseek-ai/DeepSeek-V3", wire_format="together_chat",
                           capabilities=dict(caps))
    sent: dict[str, Any] = {}

    async def _resolve(*_a: Any, **_k: Any):
        return profile

    class _Provider:
        async def execute(self, wire_config: Any, _profile: Any, _debug: bool) -> Any:
            sent["tools"] = list(wire_config.tools or [])
            sent["custom_tools"] = list(wire_config.custom_tools or [])
            if web_search:
                sent["internal_web_search"] = wire_config.internal_web_search
            return SimpleNamespace(usage=None, messages=[])

    async def _client(_self: Any, _name: str) -> Any:
        return _Provider()

    async def _net(thunk: Any, **_k: Any) -> Any:
        return await thunk()

    import matrx_ai.catalog.resolve as resolve_mod

    monkeypatch.setattr(resolve_mod, "resolve_tts_call_profile", _resolve)
    monkeypatch.setattr(UnifiedAIClient, "_get_provider_client", _client)
    monkeypatch.setattr(UnifiedAIClient, "_dispatch_with_billing_net", staticmethod(_net))

    config = _config(caps is _FC_CAPS)
    config.tools = ["web_search", "document_content", "context", "knowledge_search"]
    if web_search:
        config.internal_web_search = True
        sent["live_config"] = config
    emitter = _Emitter()
    token = set_app_context(AppContext(emitter=emitter, metadata={}))
    try:
        from matrx_connect.context.app_context import try_get_app_context

        ctx = try_get_app_context()
        request = SimpleNamespace(config=config, debug=False, add_usage=lambda _u: None)
        await UnifiedAIClient()._execute_dispatch(request)
        return sent, emitter, ctx.metadata
    finally:
        _app_context.reset(token)


@pytest.mark.asyncio
async def test_a_no_function_calling_run_sends_zero_tools_and_announces_it(monkeypatch) -> None:
    sent, emitter, metadata = await _run_dispatch(monkeypatch, _NO_FC_CAPS)

    assert sent == {"tools": [], "custom_tools": []}
    codes = [w.code for w in emitter.warnings]
    assert codes == [tool_adaptation.NO_FUNCTION_CALLING]
    warning = emitter.warnings[0]
    assert warning.metadata["removed"] == ["web_search", "document_content", "context", "knowledge_search"]
    assert warning.metadata["model"] == "deepseek-ai/DeepSeek-V3"
    assert warning.user_message
    # …and the removal rides the turn's request snapshot.
    recorded = metadata[REQUEST_SNAPSHOT_METADATA_KEY][tool_adaptation.SNAPSHOT_FIELD]
    assert [r["code"] for r in recorded] == [tool_adaptation.NO_FUNCTION_CALLING]


@pytest.mark.asyncio
async def test_a_tool_capable_run_keeps_its_tools_and_announces_nothing(monkeypatch) -> None:
    sent, emitter, metadata = await _run_dispatch(monkeypatch, _FC_CAPS)

    assert sent["tools"] == ["web_search", "document_content", "context", "knowledge_search"]
    assert emitter.warnings == []
    assert REQUEST_SNAPSHOT_METADATA_KEY not in metadata


@pytest.mark.parametrize(
    ("wire_format", "config_kwargs", "code"),
    [
        ("openai_chat", {"internal_x_search": True}, tool_adaptation.SEARCH_UNSUPPORTED),
        ("openai_chat", {"internal_web_search": True}, tool_adaptation.WEB_SEARCH_TRANSLATED),
        ("cerebras_chat", {"response_format": {"type": "json_object"}},
         tool_adaptation.SCHEMA_CONFLICT),
    ],
)
def test_every_call_time_removal_is_returned_for_announcement(
    wire_format: str, config_kwargs: dict[str, Any], code: str
) -> None:
    profile = make_profile(wire_format=wire_format, capabilities=dict(_FC_CAPS))
    config = _config(True)
    config.tools = ["lookup"]
    for key, value in config_kwargs.items():
        setattr(config, key, value)
    adaptations = unified_client.apply_capability_gates(config, profile.capabilities, wire_format)
    assert code in [a.code for a in adaptations]


def test_context_reach_follows_the_models_output_and_function_calling() -> None:
    caps = lambda row: make_profile(capabilities=row).capabilities  # noqa: E731
    assert tool_adaptation.context_reach(caps(_FC_CAPS)) == tool_adaptation.ContextReach(True, True)
    assert tool_adaptation.context_reach(caps(_NO_FC_CAPS)) == tool_adaptation.ContextReach(True, False)
    image = {**_NO_FC_CAPS, "output": ["image", "text"], "features": []}
    assert tool_adaptation.context_reach(caps(image)) == tool_adaptation.ContextReach(False, False)


def test_the_no_function_calling_strip_removes_the_context_fetch_instructions() -> None:
    """The model cannot call ``context``: the instructions to call it go with the tools; the
    inline values (what it CAN read) stay."""
    config = _config(False)
    config.tools = ["context"]
    config.messages.attach_turn_context(
        "<available_context>\n  <inline>unit 4B</inline>\n"
        '  <retrieval note="How">\n    <get>context(action="get")</get>\n  </retrieval>\n'
        "</available_context>",
        slot="context_manifest",
    )
    config.messages.attach_turn_context(
        "<deferred_context_available>\n  Keys: lease\n</deferred_context_available>",
        slot="active_context",
    )
    caps = make_profile(capabilities=dict(_NO_FC_CAPS)).capabilities
    unified_client._strip_tools_for_no_function_calling(config, caps, "together_chat")
    blocks = config.messages.turn_context_blocks()
    assert "retrieval" not in blocks["context_manifest"] and "unit 4B" in blocks["context_manifest"]
    assert "active_context" not in blocks


# ── The request is never denied: built-in web search TRANSLATES to our ``web`` tool ──


@pytest.mark.asyncio
async def test_built_in_web_search_on_a_model_without_it_runs_through_our_web_tool(
    monkeypatch,
) -> None:
    sent, emitter, metadata = await _run_dispatch(monkeypatch, _FC_CAPS, web_search=True)

    assert "web" in sent["tools"] and sent["internal_web_search"] is None
    [warning] = emitter.warnings
    assert warning.code == tool_adaptation.WEB_SEARCH_TRANSLATED
    assert warning.level == "low"
    assert warning.metadata["added"] == ["web"]
    assert warning.metadata["removed"] == ["internal_web_search"]
    # The authored setting survives on the live config, so a model that hosts search uses it.
    live = sent["live_config"]
    assert live.internal_web_search is True
    recorded = metadata[REQUEST_SNAPSHOT_METADATA_KEY][tool_adaptation.SNAPSHOT_FIELD]
    assert recorded[0]["code"] == tool_adaptation.WEB_SEARCH_TRANSLATED


def test_the_translated_web_tool_is_gone_and_native_search_is_back_on_the_next_turn() -> None:
    from matrx_ai.tools.merge import restore_request_filtered_tool_surface

    config = UnifiedConfig.from_dict(
        {
            "model": "deepseek-ai/DeepSeek-V3",
            "messages": [{"role": "user", "content": [{"type": "text", "text": "Rates?"}]}],
            "tools": ["lookup"],  # authored by the agent
            "internal_web_search": True,
        }
    )
    profile = make_profile(wire_format="together_chat", capabilities=dict(_FC_CAPS))
    flags = tool_adaptation.authored_tool_flags(config)
    [translated] = unified_client.apply_capability_gates(
        config, profile.capabilities, "together_chat"
    )
    # The translation is a WIRE addition: the live config never carries ``web``.
    assert translated.added == ["web"] and "web" not in config.tools
    assert not config.tool_capability_filtered
    tool_adaptation.restore_tool_flags(config, flags)

    stored = config.to_storage_dict()
    reloaded = UnifiedConfig.from_dict(
        {"model": stored["model"], "messages": stored["messages"], **stored["config"]}
    )
    restore_request_filtered_tool_surface(reloaded)
    assert reloaded.tools == ["lookup"]
    assert reloaded.internal_web_search is True


def test_a_model_that_cannot_call_tools_drops_web_search_and_says_so() -> None:
    config = _config(False)
    config.internal_web_search = True
    profile = make_profile(wire_format="together_chat", capabilities=dict(_NO_FC_CAPS))
    adaptations = unified_client.apply_capability_gates(
        config, profile.capabilities, "together_chat"
    )
    assert [a.code for a in adaptations] == [tool_adaptation.SEARCH_UNSUPPORTED]
    assert "web" not in (config.tools or [])


def test_the_dry_run_runs_the_same_gates_on_a_copy_and_records_nothing(monkeypatch) -> None:
    """The preview simulates ``apply_capability_gates`` (downgrade included) on a copy: it
    predicts the run, leaves the live config alone, and writes no finding."""
    from matrx_ai.providers import structured_output_findings as findings

    written: list[str] = []
    monkeypatch.setattr(
        findings, "record_structured_output_finding", lambda key, **_k: written.append(key)
    )
    config = _config(True)
    config.tools = ["lookup"]
    config.response_format = {"type": "json_object"}
    profile = make_profile(wire_format="cerebras_chat", capabilities=dict(_FC_CAPS))
    probe, adaptations = unified_client.simulate_capability_gates(
        config, profile.capabilities, "cerebras_chat"
    )
    assert [a.code for a in adaptations] == [tool_adaptation.SCHEMA_CONFLICT]
    assert probe.tools == [] and config.tools == ["lookup"]
    assert written == [] and not findings._GATE_PENDING.get()


@pytest.mark.asyncio
async def test_a_batch_build_with_no_one_listening_records_the_removal_durably(monkeypatch) -> None:
    """``translate_request`` (the batch lane) has no emitter: the adaptation is still recorded
    as an issue event, never left as a console line."""
    import matrx_ai.catalog.resolve as resolve_mod
    from matrx_ai.ops import issue_capture

    captured: list[tuple[str, dict[str, Any]]] = []

    async def _capture(key: str, **kw: Any) -> None:
        captured.append((key, kw))

    profile = make_profile(model_name="deepseek-ai/DeepSeek-V3", wire_format="together_chat",
                           capabilities=dict(_NO_FC_CAPS))

    async def _resolve(*_a: Any, **_k: Any):
        return profile

    monkeypatch.setattr(issue_capture, "capture_issue", _capture)
    monkeypatch.setattr(resolve_mod, "resolve_call_profile", _resolve)
    config = _config(False)
    config.tools = ["lookup"]
    token = set_app_context(AppContext(emitter=None, metadata={}))
    try:
        await UnifiedAIClient().translate_request(SimpleNamespace(config=config, debug=False))
    finally:
        _app_context.reset(token)
    assert [k for k, _ in captured] == [f"tool_adaptation.{tool_adaptation.NO_FUNCTION_CALLING}"]
    assert captured[0][1]["detail"]["removed"] == ["lookup"]


def test_a_removed_web_tool_is_never_the_stand_in(monkeypatch) -> None:
    """A removal wins (rule U): the agent's forbidden list keeps ``web`` out — web search is
    dropped and announced, not translated."""
    config = _config(True)
    config.internal_web_search = True
    config.agent_excluded_tools = ["web"]
    profile = make_profile(wire_format="together_chat", capabilities=dict(_FC_CAPS))
    [adaptation] = unified_client.apply_capability_gates(
        config, profile.capabilities, "together_chat"
    )
    assert adaptation.code == tool_adaptation.SEARCH_UNSUPPORTED and not adaptation.added
    assert "excludes the web tool" in adaptation.reason


def test_a_call_that_cannot_carry_tools_never_hears_translated_then_tools_off() -> None:
    """Cerebras refuses tools beside a schema: the later gate removes the tools, so the
    translation becomes a drop — one true announcement."""
    config = _config(True)
    config.tools = ["lookup"]
    config.internal_web_search = True
    config.response_format = {"type": "json_object"}
    profile = make_profile(wire_format="cerebras_chat", capabilities=dict(_FC_CAPS))
    adaptations = unified_client.apply_capability_gates(
        config, profile.capabilities, "cerebras_chat"
    )
    codes = [a.code for a in adaptations]
    assert tool_adaptation.WEB_SEARCH_TRANSLATED not in codes
    assert codes == [tool_adaptation.SEARCH_UNSUPPORTED, tool_adaptation.SCHEMA_CONFLICT]
    assert not any(a.added for a in adaptations)
