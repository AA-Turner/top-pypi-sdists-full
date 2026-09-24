"""A Gemini turn with a response schema AND the `records` tool must reach Google intact.

THE BUG (2026-09-22): every Gemini agent that returns structured output and carries
`records` failed every turn with a bare 400 "Request contains an invalid argument."
(Flashcard Detail Enricher, Spoken Answer Grader, Source Deck Composer). Replay of the
recorded request: fails as sent; passes with `records` removed; passes with the schema
removed; still fails with every description stripped or every type set to STRING.
Google's constrained decoder cannot hold a declaration naming 85 parameters beside
a response schema. Gemini 2.5 refuses ANY function calling beside one.

The fix, pinned here at the request boundary: tools are kept whole, Google's native
schema switch is withheld, and the schema rides the system instruction as a fenced-JSON
contract (extract_json + kind validation still enforce it downstream).

The fixture is the recorded failing request itself. The offline tests go red if the
translator sends `response_json_schema` beside it; the live test (GOOGLE_API_KEY and
MATRX_LIVE_GOOGLE=1) sends the translator's real output to Google.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
from test_chat_param_golden import load_golden

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.providers.google.translator import GoogleTranslator
from matrx_ai.testing.profile_factory import make_profile

FIXTURE = json.loads(
    (Path(__file__).parent / "fixtures" / "gemini_schema_beside_records_refused.json").read_text()
)
DECLS: list[dict] = FIXTURE["declarations"]
RECORDS = next(d for d in DECLS if d["name"] == "records")


def _profile(variant_key: str):
    payload = load_golden(variant_key)
    return make_profile(
        model_name=payload["model"],
        wire_format=payload["wire_format"],
        rules=payload["rules"],
        value_orders=payload["value_orders"],
    )


_GEMINI_3 = _profile("google_thinking_3__flash")
_GEMINI_25 = _profile("google_thinking")

_FORMAT = {
    "type": "json_schema",
    "json_schema": {"name": "card_enrichment", "schema": FIXTURE["response_json_schema"]},
}


def _config() -> UnifiedConfig:
    text = FIXTURE["contents"][0]["parts"][0]["text"]
    return UnifiedConfig(
        model=FIXTURE["model"],
        messages=MessageList(
            _messages=[UnifiedMessage(role="user", content=[TextContent(text=text)])]
        ),
        response_format=_FORMAT,
    )


def _wire(profile, decls, monkeypatch):
    tr = GoogleTranslator()
    monkeypatch.setattr(tr, "build_provider_tools", lambda config, provider: decls)
    return tr.to_google(_config(), profile)


def test_the_real_records_schema_is_over_googles_budget_and_nothing_else_is() -> None:
    counts = {d["name"]: GoogleTranslator._count_param_names(d.get("parameters")) for d in DECLS}
    assert counts["records"] == 85
    budget = GoogleTranslator.GEMINI_SCHEMA_TOOL_PARAM_BUDGET
    assert [n for n, c in counts.items() if c > budget] == ["records"], counts
    conflict = GoogleTranslator._native_schema_tool_conflict(DECLS, is_gemini_3=True)
    assert conflict is not None and conflict["oversize_tools"] == {"records": 85}
    assert GoogleTranslator._native_schema_tool_conflict(
        [d for d in DECLS if d["name"] != "records"], is_gemini_3=True
    ) is None


def test_recorded_request_keeps_every_tool_and_moves_the_schema_to_the_prompt(
    monkeypatch,
) -> None:
    out = _wire(_GEMINI_3, DECLS, monkeypatch)
    cfg = out["config"]
    sent = [fd.name for t in cfg.tools or [] for fd in (t.function_declarations or [])]
    assert sent == [d["name"] for d in DECLS], "a tool was dropped"
    assert cfg.response_json_schema is None, "native schema sent beside records (the 400)"
    assert cfg.response_mime_type != "application/json"
    system = str(cfg.system_instruction)
    assert "FINAL ANSWER FORMAT" in system and '"card_enrichment"' in system


def test_small_tools_keep_native_structured_output_on_gemini_3(monkeypatch) -> None:
    small = [d for d in DECLS if d["name"] != "records"]
    cfg = _wire(_GEMINI_3, small, monkeypatch)["config"]
    assert cfg.response_json_schema is not None
    assert cfg.response_mime_type == "application/json"


def test_gemini_25_never_pairs_function_calling_with_a_json_mime_type(monkeypatch) -> None:
    small = [d for d in DECLS if d["name"] == "data"]
    cfg = _wire(_GEMINI_25, small, monkeypatch)["config"]
    assert cfg.response_json_schema is None
    assert cfg.response_mime_type != "application/json"


@pytest.mark.skipif(
    os.environ.get("MATRX_LIVE_GOOGLE") != "1"
    or not (os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")),
    reason="live Google replay: set MATRX_LIVE_GOOGLE=1 and GOOGLE_API_KEY",
)
@pytest.mark.asyncio
async def test_live_google_accepts_the_translated_request_and_refused_the_native_one(
    monkeypatch,
) -> None:
    from google import genai

    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY") or os.environ["GEMINI_API_KEY"])
    out = _wire(_GEMINI_3, DECLS, monkeypatch)
    cfg = out["config"]
    cfg.max_output_tokens = 64
    # Before: the same declarations with Google's native schema switch → refused.
    native = cfg.model_copy(
        update={
            "response_json_schema": FIXTURE["response_json_schema"],
            "response_mime_type": "application/json",
        }
    )
    with pytest.raises(Exception, match="INVALID_ARGUMENT"):
        await client.aio.models.generate_content(
            model=FIXTURE["model"], contents=out["contents"], config=native
        )
    # After: what the translator actually sends → accepted.
    resp = await client.aio.models.generate_content(
        model=FIXTURE["model"], contents=out["contents"], config=cfg
    )
    assert resp.candidates
