"""The residual check must not report an agent's OWN system text just because the always-warm layout
re-cut the system channel (providers/prompt_warm.py ``apply_warm_layout``).

Live defect (2026-11-15..19, 683 ``unregistered_request_content`` reports, all Anthropic, all
``system`` / ``system part 0``): the warm layout sends ``[shared.rstrip(), rest.strip()]`` — the
whitespace that separated the two pieces (and any trailing whitespace of the authored text) is not on
the wire any more, so the rendered system text is no longer a substring of the wire text and the whole
prompt was left over. Built through the REAL translator + warm layout.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.config import UnifiedConfig
from matrx_ai.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_ai.providers import final_outbound_snapshot as fos
from matrx_ai.providers import prompt_warm, residual_check
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.providers.unified_client import _build_provider_wire_config
from matrx_ai.testing.profile_factory import make_profile

AGENT = "6b6b4e45-4699-4860-8dea-d8a60e07d69a"
AUTHORED = "You are the Personal Chief of Staff. " + "Be precise and kind. " * 40
PLANT = "Planted platform sentence that no registered block accounts for."


@pytest.fixture(autouse=True)
def _enrolled(monkeypatch: pytest.MonkeyPatch):
    profiles = {AGENT: prompt_warm.WarmProfile(shared_text=AUTHORED.rstrip(), prompt_chars=len(AUTHORED))}
    prompt_warm.configure_prompt_warm(profiles.get, lambda _o: None)
    monkeypatch.setattr(residual_check, "_will_be_checked", lambda _provider: True)
    token = set_app_context(AppContext(emitter=None, user_id="u1", agent_id=AGENT, conversation_id="c1"))
    yield
    clear_app_context(token)
    prompt_warm.configure_prompt_warm(None, None)
    prompt_warm.take_layout()
    residual_check.reset_for_tests()


def _build(system: str) -> tuple[dict[str, Any], Any]:
    config = UnifiedConfig.from_dict(
        {
            "model": "claude-opus-5-5",
            "system_instruction": system,
            "messages": [{"role": "user", "content": [{"type": "text", "text": "Hello there."}]}],
        }
    )
    profile = make_profile(model_name="claude-opus-5-5", wire_format="anthropic_chat")
    request = AnthropicTranslator().to_anthropic(_build_provider_wire_config(config, profile), profile)
    return request, residual_check.take_wire_source()


def _residual(request: dict[str, Any], source: Any) -> list[tuple[str, str]]:
    return residual_check.residual_of(fos.SHAPE_ANTHROPIC, request, residual_check.known_texts(source))


@pytest.mark.parametrize(
    "system",
    [
        AUTHORED + "\n\n<org_catalog>Acme</org_catalog>",  # two blocks: the separator is not on the wire
        AUTHORED + "\n",  # one block: the trailing whitespace is not on the wire
    ],
    ids=["two_blocks", "one_block"],
)
def test_the_agents_own_system_text_is_not_a_residual_after_the_warm_layout(system: str) -> None:
    request, source = _build(system)
    assert source is not None
    assert [b["text"] for b in request["system"]][0] == AUTHORED.rstrip(), "the warm layout did not apply"
    leftover = _residual(request, source)
    assert [t for _w, t in leftover if AUTHORED[:40] in t] == [], leftover


def test_a_planted_span_in_a_warm_system_channel_is_still_reported() -> None:
    request, source = _build(AUTHORED + "\n\n<org_catalog>Acme</org_catalog>")
    request["system"] = [*request["system"], {"type": "text", "text": PLANT}]
    leftover = _residual(request, source)
    assert len(leftover) == 1 and PLANT in leftover[0][1], leftover

