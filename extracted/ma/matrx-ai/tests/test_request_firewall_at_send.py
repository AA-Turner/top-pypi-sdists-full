"""THE REQUEST FIREWALL AT THE SEND BOUNDARY — nothing reaches a provider unscanned while a caller's
firewall scope is open (adversarial review of 7b3ee2b37258, 2026-10-27).

Before: the doors scanned the request in ``prepare_agent_run`` / the programmatic hook, and then
``run_ai_task`` kept adding to it (response format, observational memory, group view, remarks and
surface notes, picked shapes) and the loop added tool results — all sent unscanned. A door that
never ran the firewall (a compiled Orchestra, a future door) was only noticed AFTER the provider
was paid. Now ``send_boundary.prepare_for_send`` checks the open scope LAST, on the exact wire
config, every loop turn and every retry (``request_firewall.check_at_send``).

Each test names the break that turns it red.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.config.context_trim import TrimPolicy
from matrx_ai.config.message_config import MessageList
from matrx_ai.config.request_firewall import (
    RequestFirewallRefused,
    UnmatchableFirewallTerms,
    check_request,
    firewall_from_step_fields,
    request_firewall_scope,
)
from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.orchestrator.execution_state import ExecutionState
from matrx_ai.orchestrator.requests import AIMatrixRequest
from matrx_ai.orchestrator.send_once import send_once

BRAND = "Fabrikam"


def _config(extra: str = "") -> UnifiedConfig:
    messages = MessageList()
    messages.append_or_extend_user_text(f"Write five buyer questions about CRM tools. {extra}".strip())
    return UnifiedConfig(
        model="claude-sonnet-4-6",
        messages=messages,
        system_instruction="You write buyer questions for a product category.",
    )


def _door(scope: Any, config: UnifiedConfig) -> None:
    """What a host door does: check the rendered request and record it on the scope."""
    scope.records.append(
        check_request(config, scope.firewall, auto_context_disabled=True, door="agent_run")
    )


async def _send(config: UnifiedConfig) -> Any:
    return await prepare_for_send(config, stage=STAGE_LOOP, policy=TrimPolicy())


# ── P0: what is added after the door's scan is scanned at the send boundary ─────────────────


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "late_addition",
    ["observational_memory", "response_format", "tool_result_next_turn", "surface_note"],
)
async def test_a_term_added_after_the_door_cleared_is_refused_at_the_send_boundary(late_addition: str) -> None:
    """Break: the boundary does not check the scope, or checks the canonical config instead of the
    one sent, or only on the first turn."""
    config = _config()
    with request_firewall_scope(firewall_from_step_fields([BRAND]), mandate_key="seo.blind_writer") as scope:
        _door(scope, config)  # the door cleared the request it saw
        if late_addition == "observational_memory":
            config.messages.attach_turn_context(f"Remembered: the user works at {BRAND}.", slot="observational_memory")
        elif late_addition == "surface_note":
            config.messages.attach_turn_context(f"Shown on screen: {BRAND} pricing page.", slot="surface_notes")
        elif late_addition == "response_format":
            config.response_format = {
                "type": "json_schema",
                "json_schema": {"name": "q", "schema": {"type": "object", "description": f"Questions about {BRAND}"}},
            }
        else:
            await _send(config)  # turn 1 is clean and cleared
            config.messages.append_or_extend_user_text(f"Search result: {BRAND} leads the category.")
        with pytest.raises(RequestFirewallRefused) as refused:
            await _send(config)
    assert refused.value.door == "send_boundary"
    assert BRAND not in str(refused.value), "a refusal must never echo the term"
    assert scope is not None and scope.refusals[-1] is refused.value


@pytest.mark.asyncio
async def test_send_once_never_calls_the_provider_when_the_boundary_refuses() -> None:
    """Break: the refusal happens after ``client.execute`` (money already spent)."""
    calls: list[Any] = []

    class _Client:
        async def execute(self, request: Any) -> Any:
            calls.append(request)
            return SimpleNamespace()

    request = AIMatrixRequest(
        conversation_id="5b0f3c8e-7d0e-4c55-9a51-1f3f0b8f6a21",
        request_id="0e9b6f2a-2b8c-4a8e-8a7e-6d1c4c3b2a10",
        config=_config(f"Our client is {BRAND}."),
    )
    with request_firewall_scope(firewall_from_step_fields([BRAND])):
        with pytest.raises(RequestFirewallRefused):
            await send_once(_Client(), request, state=ExecutionState(), iteration=1)
    assert calls == [], "the provider was called before the firewall refused"


@pytest.mark.asyncio
async def test_a_clean_send_is_recorded_per_call_and_no_scope_changes_nothing() -> None:
    config = _config()
    prep = await _send(config)
    assert "request_firewall" in prep.steps  # no scope: the step ran and did nothing
    with request_firewall_scope(firewall_from_step_fields([BRAND])) as scope:
        await _send(config)
        await _send(config)
    assert scope is not None and [r.door for r in scope.sends] == ["send_boundary", "send_boundary"]
    assert not scope.records and not scope.refusals


# ── P0: a call no door checked is refused before it is sent ────────────────────────────────


@pytest.mark.asyncio
async def test_no_automatic_context_with_no_door_record_refuses_before_the_call() -> None:
    """Break: only a door can see the auto-context switch; a path that skipped every door would
    send with automatic context open and be noticed after spend."""
    with request_firewall_scope(firewall_from_step_fields(None, no_auto_context=True)) as scope:
        with pytest.raises(RequestFirewallRefused, match="no door checked"):
            await _send(_config())
        _door(scope, _config())
        await _send(_config())  # a door proved it closed: the call goes out
    assert scope is not None and len(scope.sends) == 1


# ── P1: no tools counts provider-hosted tools and MCP servers ───────────────────────────────


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("internal_web_search", True),
        ("internal_url_context", True),
        ("internal_x_search", True),
        ("mcp_servers", ["crm-research-server"]),
    ],
)
def test_no_tools_counts_hosted_tools_and_mcp_servers(field: str, value: Any) -> None:
    """Break: ``_tool_count`` reads only ``tools`` / ``custom_tools``."""
    config = _config()
    setattr(config, field, value)
    with pytest.raises(RequestFirewallRefused, match="tool"):
        check_request(config, firewall_from_step_fields(None, no_tools=True), auto_context_disabled=True, door="t")


# ── P0: a term the firewall cannot find refuses at step start ───────────────────────────────


@pytest.mark.parametrize("term", ["++", "—", "  &  "])
def test_a_term_with_nothing_to_match_refuses_at_step_start_with_the_count_only(term: str) -> None:
    """Break: the matcher silently skips the term, so the record claims it was scanned."""
    with pytest.raises(UnmatchableFirewallTerms) as refused:
        firewall_from_step_fields([BRAND, term])
    assert "1 of the 2 terms" in str(refused.value)
    assert term.strip() not in str(refused.value).replace("terms", "")


def test_every_matchable_term_is_found_where_it_is_written() -> None:
    """Cyrillic as a whole word; CJK inside unspaced text — or refused at start, never skipped."""
    fw = firewall_from_step_fields(["Москва"])
    with pytest.raises(RequestFirewallRefused):
        check_request(_config("Офис в Москва"), fw, auto_context_disabled=True, door="t")
    try:
        fw = firewall_from_step_fields(["北京"])
    except UnmatchableFirewallTerms:
        return  # the matcher cannot find it inside unspaced text: refused, never skipped
    with pytest.raises(RequestFirewallRefused):
        check_request(_config("总部在北京"), fw, auto_context_disabled=True, door="t")


# ── P2: files cannot be read; HTML is read as text ──────────────────────────────────────────


def test_a_file_or_image_refuses_while_a_term_list_is_set() -> None:
    """Break: a PDF or image rides unscanned while the record says the request was clean."""
    config = UnifiedConfig.from_dict(
        {
            "model": "claude-sonnet-4-6",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Summarize the attached brief."},
                        {"type": "document", "url": "https://files.example.com/brief.pdf", "mime_type": "application/pdf"},
                    ],
                }
            ],
        }
    )
    with pytest.raises(RequestFirewallRefused, match="file"):
        check_request(config, firewall_from_step_fields([BRAND]), auto_context_disabled=True, door="t")
    # Without a term list there is nothing to read the file for.
    check_request(config, firewall_from_step_fields(None, no_tools=True), auto_context_disabled=True, door="t")


def test_a_term_split_by_inline_html_is_found() -> None:
    with pytest.raises(RequestFirewallRefused):
        check_request(
            _config("<p>Our client <b>Fabri</b>kam wants this.</p>"),
            firewall_from_step_fields([BRAND]),
            auto_context_disabled=True,
            door="t",
        )


# ── Owner ruling 2026-10-27: the platform does not describe itself to a firewalled call ─────


def _with_context_block(extra: str = "") -> UnifiedConfig:
    config = _config(extra)
    config.messages.attach_turn_context("Category notes: buyers compare price and support.", slot="history")
    return config


@pytest.mark.asyncio
async def test_a_firewall_naming_our_platform_runs_and_the_request_never_names_it() -> None:
    """Break: the context frame's note ("the AI Matrx platform") or the who-made-this-agent note
    rides the request, so a blind run about a brand sharing our platform's words always refuses."""
    from matrx_ai.config.request_firewall import find_hits, rendered_request_text

    control = _with_context_block()
    await _send(control)
    assert "AI Matrx" in (control.messages.render_turn_context() or ""), "control: the frame names the platform"

    firewall = firewall_from_step_fields(["AI Matrx"])
    assert firewall is not None
    config = _with_context_block()
    with request_firewall_scope(firewall) as scope:
        prep = await _send(config)
        sent = rendered_request_text(prep.wire_config if prep.wire_config is not None else config)
    assert scope is not None and len(scope.sends) == 1 and not scope.refusals
    assert not find_hits(sent, firewall), "the request still names the platform"
    assert "Category notes" in sent, "the context block itself must still be sent"


@pytest.mark.asyncio
async def test_a_value_naming_our_platform_is_still_refused() -> None:
    """Break: withholding the platform's notes weakened the scan."""
    with request_firewall_scope(firewall_from_step_fields(["AI Matrx"])):
        with pytest.raises(RequestFirewallRefused):
            await _send(_with_context_block("Compare AIMatrx with the others."))


# ── ROUND 2 (adversarial review after 8c3ec72939d7) ─────────────────────────────────────────


@pytest.mark.asyncio
async def test_the_live_plan_in_the_tail_channel_is_scanned_before_send() -> None:
    """Break (P0): the live plan rides the TAIL channel after the newest tool result
    (``get_trailing_context_text``) but the scan read only ``to_dict`` + the turn context."""
    from matrx_ai.config.live_plan import (
        LivePlanSnapshot,
        PlanTask,
        get_live_plan_source,
        set_live_plan_source,
    )

    async def source(_conversation: Any, _org: Any) -> Any:
        return LivePlanSnapshot(tasks=[PlanTask(id="1", title=f"Draft questions for {BRAND} launch", status="in_progress")])

    config = UnifiedConfig.from_dict(
        {
            "model": "claude-sonnet-4-6",
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": "Category: small-business CRM."}]},
                {"role": "assistant", "content": [{"type": "tool_call", "id": "t1", "name": "web_search", "arguments": {"q": "crm"}}]},
                {"role": "tool", "content": [{"type": "tool_result", "tool_use_id": "t1", "call_id": "t1", "name": "web_search", "content": "ten CRMs compared"}]},
            ],
        }
    )
    previous = get_live_plan_source()
    set_live_plan_source(source)
    try:
        with request_firewall_scope(firewall_from_step_fields([BRAND])) as scope:
            _door(scope, config)
            with pytest.raises(RequestFirewallRefused):
                await prepare_for_send(
                    config, stage=STAGE_LOOP, conversation_id="2b9d4f6a-8c1e-4a3b-b5d7-9e0f1a2b3c4d",
                    request_id="r1", policy=TrimPolicy(),
                )
        assert BRAND in (config.messages.render_tail_context() or ""), "control: the plan was staged"
    finally:
        set_live_plan_source(previous)


_TRANSLATORS = [
    ("matrx_ai.providers.anthropic.translator", "AnthropicTranslator", "anthropic_chat"),
    ("matrx_ai.providers.openai.translator", "OpenAITranslator", "openai_responses"),
    ("matrx_ai.providers.groq.translator", "GroqTranslator", "groq_chat"),
    ("matrx_ai.providers.cerebras.translator", "CerebrasTranslator", "cerebras_chat"),
    ("matrx_ai.providers.together.translator", "TogetherTranslator", "together_chat"),
    ("matrx_ai.providers.generic_openai.translator", "GenericOpenAITranslator", "openai_chat"),
    ("matrx_ai.providers.google.translator", "GoogleTranslator", "google_chat"),
]

#: Words a translator adds that are wire STRUCTURE, never content (roles, part types, cache
#: settings). Anything else the payload carries must be in the scan.
_STRUCTURAL = {
    "user", "assistant", "system", "developer", "model", "tool", "text", "function", "auto",
    "ephemeral", "input_text", "output_text", "message", "function_call", "function_call_output",
    "tool_use", "tool_result", "input", "type", "required", "none", "low", "medium", "high",
    "object", "string", "json_schema", "call", "true", "false",
    "reasoning", "encrypted", "content", "output",  # OpenAI Responses part types / include list
}


def _payload_words(value: Any) -> set[str]:
    import re

    out: set[str] = set()
    if isinstance(value, str):
        out |= {w.lower() for w in re.findall(r"[A-Za-z]{4,}", value)}
    elif isinstance(value, dict):
        for v in value.values():
            out |= _payload_words(v)
    elif isinstance(value, (list, tuple)):
        for v in value:
            out |= _payload_words(v)
    return out


def _unscanned_words(module: str, cls: str, wire_format: str, last: str, scan: Any) -> set[str]:
    import importlib

    from matrx_ai.config.send_boundary import order_for_wire
    from matrx_ai.testing.profile_factory import make_profile

    messages = [{"role": "user", "content": [{"type": "text", "text": "Questions about zephyrbound gadgets."}]}]
    if last == "tool_result":
        messages += [
            {"role": "assistant", "content": [{"type": "tool_call", "id": "t1", "name": "web_search", "arguments": {"q": "quillfeather"}}]},
            {"role": "tool", "content": [{"type": "tool_result", "tool_use_id": "t1", "call_id": "t1", "name": "web_search", "content": "marrowlight results"}]},
        ]
    config = UnifiedConfig.from_dict({"model": "m", "messages": messages})
    config.system_instruction = "Systemic thornwhistle guidance."
    config.dictionary = {"entries": [{"term": "Vexlorn", "definition": "a glimmerstone widget", "sounds_like": ["veks lorn"]}]}
    config.messages.attach_turn_context("Turnwise brambleglow notes.", slot="history")
    config.messages.attach_tail_context("Tailward cindermoss plan.", slot="live_plan")
    profile = make_profile(model_name="m", wire_format=wire_format)
    prep = order_for_wire(config, profile)
    wire = prep.wire_config if prep.wire_config is not None else config
    translator = getattr(importlib.import_module(module), cls)()
    payload = translator.build_request(wire, profile)
    import json

    scanned = _payload_words(json.loads(scan(wire))) | _payload_words(json.loads(scan(config)))
    return _payload_words(payload) - scanned - _STRUCTURAL


@pytest.mark.parametrize(("module", "cls", "wire_format"), _TRANSLATORS)
@pytest.mark.parametrize("last", ["person", "tool_result"])
def test_the_scan_covers_every_word_a_translator_sends(module: str, cls: str, wire_format: str, last: str) -> None:
    """THE CHANNEL GUARD: every content word a chat translator puts on the wire is in
    ``rendered_request_text``. Break: a translator renders a channel the scan does not read
    (the live plan tail was one) — add it to ``request_firewall.SCANNED_CHANNELS``."""
    from matrx_ai.config.request_firewall import rendered_request_text

    missing = _unscanned_words(module, cls, wire_format, last, rendered_request_text)
    assert not missing, f"{cls} sends words the firewall never scanned: {sorted(missing)}"


def test_the_channel_guard_can_fail() -> None:
    """Falsifiability: a scan that drops the tail channel is caught on a tool-result send."""
    import json

    from matrx_ai.config.request_firewall import rendered_request_text

    def without_tail(config: Any) -> str:
        channels = json.loads(rendered_request_text(config))
        channels.pop("tail_context", None)
        return json.dumps(channels)

    module, cls, wire_format = _TRANSLATORS[0]
    assert "cindermoss" in _unscanned_words(module, cls, wire_format, "tool_result", without_tail)


@pytest.mark.parametrize(
    ("term", "text"),
    [("Acme", "Ac me"), ("Acme", "Ac&shy;me"), ("Acme", "Ac&#109;e"), ("Acme", "&lt;b&gt;Ac&lt;/b&gt;me")],
)
def test_split_and_entity_written_terms_hit(term: str, text: str) -> None:
    """Break (P2): a one-word term split by one space, or written with an HTML entity, passed."""
    from matrx_ai.config.request_firewall import FirewallTerm, RequestFirewall, find_hits

    assert find_hits(text, RequestFirewall(must_not_contain=[FirewallTerm(term=term)]))


@pytest.mark.parametrize(("term", "text"), [("Acme", "4cme"), ("Acme", "QWNtZQ=="), ("Acme", "emcA")])
def test_encodings_a_person_must_decode_are_out_of_scope_and_said_so(term: str, text: str) -> None:
    """Leetspeak, base64 and reversed text are OUT OF SCOPE — documented on ``find_hits`` so no
    one mistakes the firewall for a decoder. If one starts hitting, update the docstring."""
    from matrx_ai.config.request_firewall import FirewallTerm, RequestFirewall, find_hits

    assert "OUT OF SCOPE" in (find_hits.__doc__ or "")
    assert not find_hits(text, RequestFirewall(must_not_contain=[FirewallTerm(term=term)]))


@pytest.mark.parametrize(
    "body",
    [
        {"contents": [], "tools": [{"functionDeclarations": [{"name": "lookup"}]}]},
        {"contents": [], "config": {"tools": [{"googleSearch": {}}]}},
        {"request": {"contents": [], "generationConfig": {}, "tools": [{"urlContext": {}}]}},
        {"messages": [], "tools": [{"type": "web_search"}]},
    ],
)
def test_no_tools_counts_tools_anywhere_in_a_rendered_batch_body(body: dict[str, Any]) -> None:
    """Break (P2): a rendered Google body nests its tools; the count read only the top level."""
    with pytest.raises(RequestFirewallRefused, match="tool"):
        check_request(body, firewall_from_step_fields(None, no_tools=True), auto_context_disabled=True, door="batch")


@pytest.mark.asyncio
async def test_the_wire_copy_the_client_shapes_after_the_boundary_is_checked_before_dispatch() -> None:
    """Break (P1): ``UnifiedAIClient`` shapes its wire copy AFTER the send boundary (message flags'
    converted prefill instruction, capability gates); the billing net is the last step before the
    provider and must check what is really dispatched — and refuse a call it cannot read."""
    from matrx_ai.providers.unified_client import UnifiedAIClient

    calls: list[str] = []

    async def dispatch() -> Any:
        calls.append("sent")
        return SimpleNamespace()

    wire = _config()
    wire.messages.attach_turn_context(f"Continue the answer that began: {BRAND} is", slot="convert_prefill")
    profile = SimpleNamespace(provider="anthropic", model_name="m", endpoint_id="e", api_id="a")
    with request_firewall_scope(firewall_from_step_fields([BRAND])) as scope:
        with pytest.raises(RequestFirewallRefused) as refused:
            await UnifiedAIClient._dispatch_with_billing_net(dispatch, profile=profile, config=wire)
        with pytest.raises(RequestFirewallRefused, match="cannot read"):
            await UnifiedAIClient._dispatch_with_billing_net(dispatch, profile=profile)
    assert calls == [] and refused.value.door == "provider_dispatch"
    assert scope is not None and not scope.sends, "the dispatch re-check never adds a second record"


def test_detached_work_is_refused_and_carries_the_scope() -> None:
    """Break (P1): work handed off detached saw no firewall. Leaving for a place the scope cannot
    follow is refused; a plain detached task carries the scope so its own sends are checked."""
    import asyncio

    from matrx_utils import detached_task, refuse_detached_work_if_forbidden

    from matrx_ai.config.request_firewall import active_request_firewall

    refuse_detached_work_if_forbidden("anything")  # no scope: nothing refused
    with request_firewall_scope(firewall_from_step_fields([BRAND])) as scope:
        with pytest.raises(RequestFirewallRefused, match="background job"):
            refuse_detached_work_if_forbidden("a background job")

        async def seen() -> Any:
            return active_request_firewall()

        async def run() -> Any:
            return await detached_task(seen())

        carried = asyncio.run(run())
    assert carried is scope


@pytest.mark.asyncio
async def test_a_firewall_skips_compaction_instead_of_failing_after_the_answer() -> None:
    """Break (P3): condensing at the resolve stage sent the whole conversation through a second
    model call; refused there, it failed the step AFTER the main call. With a term list open the
    compactor is skipped, said, and the forced trim makes the call fit."""
    from matrx_ai.config import input_fit
    from matrx_ai.config.context_preflight import estimate_prompt_tokens
    from matrx_ai.config.send_boundary import STAGE_RESOLVE, _forced_trim
    from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent
    from matrx_ai.config.unified_config import UnifiedMessage

    messages: list[Any] = [UnifiedMessage(role="user", content=[])]
    for i in range(12):
        messages.append(UnifiedMessage(role="assistant", position=None, content=[ToolCallContent(id=f"c{i}", name="shell_execute", arguments={"command": f"step {i}"})]))
        messages.append(UnifiedMessage(role="tool", position=None, content=[ToolResultContent(tool_use_id=f"c{i}", name="shell_execute", content="x" * 60_000, output_chars=60_000)]))
    config = SimpleNamespace(model="claude-opus-5-5", matrx_model_name="claude-opus-5-5", messages=messages,
                             system_instruction=None, tools=[], prompt_cache_key=None)
    limit = estimate_prompt_tokens(config) // 3
    condensed: list[int] = []

    async def compactor(_cfg: Any, **_kw: Any) -> bool:
        condensed.append(1)
        return False

    input_fit.set_input_budget_resolver(lambda _ctx, cfg, _p: (limit, estimate_prompt_tokens(cfg)))
    input_fit.set_compactor(compactor)
    try:
        with request_firewall_scope(firewall_from_step_fields([BRAND])) as scope:
            record = await input_fit.ensure_fits(
                config, policy=None, stage=STAGE_RESOLVE, conversation_id="c", trim=_forced_trim
            )
    finally:
        input_fit.set_compactor(None)
        input_fit.set_input_budget_resolver(None)
    assert condensed == [] and record["passes"][0] == {"pass": "compaction", "changed": False, "skipped": "request_firewall"}
    assert record["fits"] is True and scope is not None and not scope.refusals


@pytest.mark.parametrize(
    ("text", "hits"),
    [
        ("Render times got slow after the update.", False),
        ("We compared Render with two other hosts.", True),
        ("Why does Render fail on deploys?", True),
    ],
)
def test_a_proper_name_only_term_hits_only_where_it_is_written_as_a_name(text: str, hits: bool) -> None:
    """Break (V6): the firewall ignored the per-term mode the never-say list sets, so an everyday-word
    brand ("Render") refused ordinary sentences — or, unmarked, nothing told it apart."""
    from matrx_ai.config.request_firewall import FirewallTerm, RequestFirewall, find_hits

    fw = firewall_from_step_fields([FirewallTerm.model_validate({"term": "Render", "class": "brand", "match": "proper_name_only"})])
    assert fw is not None and isinstance(fw, RequestFirewall)
    assert bool(find_hits(text, fw)) is hits
