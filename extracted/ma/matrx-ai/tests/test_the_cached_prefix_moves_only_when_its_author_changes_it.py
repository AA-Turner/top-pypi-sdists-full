"""FORCING GUARD — an agent's cached prefix changes only when its author changes it (lane 6, 2026-11-17).

Anthropic caches ``tools -> system -> messages`` and a cache entry is the exact bytes up to a mark.
Measured before this guard:

* Badass Agent (506a20fc, Opus): 6 cache variants in 32 h, 5 of them from tools the PLATFORM adds per
  app or mid-turn (iOS surface tools, the data/office bundle, desktop, sandbox ``fs_*``/``shell_*``).
  The wire list was ONE flat name order, so ``apply_surface_write`` or ``data`` sorted in among the
  authored tools and every variant shared only ~5k tokens; ~67% of its spend was cache writes.
* Chief of Staff (4383174d): every new person (or a new conversation after five minutes) re-wrote all
  ~23k tokens because the per-person ``<org_catalog>`` sat at the END of the one marked system block.

Each test drives the real seams (``BaseTranslator.build_provider_tools`` -> the declaration ledger,
``prompt_warm`` layout, ``AnthropicTranslator.to_anthropic``) and compares the BYTES before a cache
mark for one unchanged agent across what the platform varies. Proven red on the code before the fix.
"""

from __future__ import annotations

import json
from typing import Any

import pytest
from matrx_connect.emitters.silent_emitter import SilentEmitter

from matrx_ai.providers import cache_guard, prompt_warm
from matrx_ai.tools import declaration_ledger

AUTHORED = ("research_web", "memory", "records", "sql", "update_plan")
#: What the platform adds on different apps / mid-turn (real names from the Badass variants).
SURFACES: dict[str, tuple[str, ...]] = {
    "agent_builder": (),
    "ios": ("advanced_read", "apply_surface_write", "page_check", "skill", "tasks"),
    "data_bundle": ("apply_surface_write", "data", "data_action", "document", "office", "workbook"),
    "sandbox": ("fs_list", "fs_read", "fs_write", "git_ingest", "shell_execute"),
}


class _NullEmitter(SilentEmitter):
    def __getattr__(self, _name: str):
        async def _noop(*_a: Any, **_kw: Any) -> None: ...

        return _noop


class _Inline:
    def __init__(self, name: str):
        self.name = name

    def get_provider_format(self, provider: str) -> dict[str, Any]:
        return {"name": self.name, "description": f"The {self.name} tool.", "input_schema": {"type": "object"}}


class _Config:
    """The two fields the boundary reads: what is offered, and what the agent authored."""

    def __init__(self, extra: tuple[str, ...]):
        self.tools: list[str] = []
        self.custom_tools = [_Inline(n) for n in (*AUTHORED, *extra)]
        self.authored_custom_tools = [_Inline(n) for n in AUTHORED]


@pytest.fixture()
def translator():
    from matrx_ai.providers.base_translator import BaseTranslator

    class _T(BaseTranslator):
        def _assemble_request(self, config, api_class=""):  # pragma: no cover
            return None

    declaration_ledger.reset_for_tests()
    yield _T()
    declaration_ledger.reset_for_tests()


@pytest.fixture()
def conversation():
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    ctx = AppContext(
        emitter=_NullEmitter(),
        metadata={},
        is_authenticated=True,
        conversation_id="33333333-3333-4333-8333-333333333333",
    )
    token = set_app_context(ctx)
    yield ctx
    clear_app_context(token)


def _prefix_before_tool_mark(tools: list[dict[str, Any]]) -> bytes:
    """The bytes the always-warm layout caches at its tool mark: the authored run, as sent."""
    run = 0
    for decl in tools:
        if decl.get("name") not in AUTHORED:
            break
        run += 1
    return json.dumps(tools[:run], separators=(",", ":"), ensure_ascii=False).encode()


def test_no_surface_moves_the_authored_tools(translator):
    """Untracked sends (a new conversation's first request) on every app: the agent's own tools are
    the same bytes at the head of the array, whatever the platform added."""
    seen: dict[str, bytes] = {}
    for surface, extra in SURFACES.items():
        tools = translator.build_provider_tools(_Config(extra), "anthropic")
        names = [t["name"] for t in tools]
        assert names[: len(AUTHORED)] == sorted(AUTHORED), (surface, names)
        seen[surface] = _prefix_before_tool_mark(tools)
    assert len(set(seen.values())) == 1, f"the authored run differs by surface: {sorted(seen)}"


def test_a_tool_added_mid_conversation_never_lands_inside_the_authored_run(translator, conversation):
    """A bundle opened mid-turn whose names sort before the authored ones (``advanced_read``,
    ``apply_surface_write``, ``data``) rides AFTER them; the wire guard stays silent."""
    first = translator.build_provider_tools(_Config(()), "anthropic")
    later = translator.build_provider_tools(_Config(SURFACES["data_bundle"] + SURFACES["ios"]), "anthropic")
    assert _prefix_before_tool_mark(first) == _prefix_before_tool_mark(later)
    assert [t["name"] for t in later][: len(AUTHORED)] == sorted(AUTHORED)
    payload = {"model": "m", "tools": first}
    assert cache_guard.observe_tool_declarations(
        provider="anthropic", conversation_id=conversation.conversation_id, payload=payload
    ) is None
    payload = {"model": "m", "tools": later}
    assert cache_guard.observe_tool_declarations(
        provider="anthropic", conversation_id=conversation.conversation_id, payload=payload
    ) is None


def test_the_authored_tier_survives_the_record(translator, conversation):
    """Another server resumes the conversation from its record: same bytes, authored tier intact."""
    conv = conversation.conversation_id
    sent = translator.build_provider_tools(_Config(SURFACES["sandbox"]), "anthropic")
    record = declaration_ledger.export_record(conv)
    declaration_ledger.forget_conversation(conv)
    assert declaration_ledger.hydrate_from_record(conv, json.loads(json.dumps(record)))
    again = translator.build_provider_tools(_Config(SURFACES["sandbox"]), "anthropic")
    assert json.dumps(again) == json.dumps(sent)


def test_the_warm_tool_mark_closes_the_authored_run():
    """The always-warm layout marks the LAST authored tool when platform tools follow it."""
    tools = [{"name": n, "input_schema": {"type": "object"}} for n in (*sorted(AUTHORED), "apply_surface_write")]
    assert prompt_warm.authored_tool_run(tools, set(AUTHORED)) == len(AUTHORED)


# ── the system channel: a per-person tail never moves the shared lead ───────────────────────────────

LEAD = "You are this person's Chief of Staff. " + "Answer first, then reach for a tool. " * 60


def _catalog(org: str) -> str:
    return f"\n\n<org_catalog>\nThe full landscape.\n  org {org} \"Some organization\"\n</org_catalog>"


def _wire(system: str) -> dict[str, Any]:
    from matrx_ai.config import UnifiedConfig
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator
    from matrx_ai.providers.unified_client import _build_provider_wire_config
    from matrx_ai.testing.profile_factory import make_profile

    config = UnifiedConfig.from_dict(
        {
            "model": "claude-opus-5-5",
            "system_instruction": system,
            "messages": [{"role": "user", "content": [{"type": "text", "text": "What is open?"}]}],
        }
    )
    profile = make_profile(model_name="claude-opus-5-5", wire_format="anthropic_chat")
    return AnthropicTranslator().to_anthropic(_build_provider_wire_config(config, profile), profile)


def _marked_system_prefixes(request: dict[str, Any]) -> list[str]:
    """The system text up to and including each marked block (what each system mark caches)."""
    out: list[str] = []
    text = ""
    for block in request["system"]:
        text += block["text"]
        if "cache_control" in block:
            out.append(text)
    return out


def test_two_people_share_the_cached_system_lead():
    a = _wire(LEAD + _catalog("7bff905b-7d70-48b6-a7ca-4c807f412c9b"))
    b = _wire(LEAD + _catalog("e4e9867c-62c8-4623-97e4-cd697d4a778b"))
    shared = set(_marked_system_prefixes(a)) & set(_marked_system_prefixes(b))
    assert shared, "no system cache mark is common to two people: each re-writes the whole prompt"
    assert max(len(s) for s in shared) >= len(LEAD.strip()) - 1
    # The model still reads exactly the same characters.
    assert "".join(blk["text"] for blk in a["system"]).endswith("</org_catalog>")
    assert len(a["system"]) <= 2


def test_a_system_text_without_a_per_person_part_stays_one_block():
    request = _wire(LEAD)
    assert len(request["system"]) == 1 and "cache_control" in request["system"][0]
