"""A Gemini turn whose response schema is too big for Google's decoder must still reach Google.

THE BUG (2026-11-02 → 11-03): the Workflow Recovery Advisor (mandate
``workflow.recovery_advisor``, gemini-3.8-flash) failed EVERY run with a bare 400
"Request contains an invalid argument." and no tools on the request. Replay of the
recorded request: fails as sent; passes with the response schema removed; every
DefinitionPatch op passes alone; stripping every description, title, default, bound and
the discriminator still fails. The schema had grown (VariableDefinition bindings) past
what the constrained decoder holds: 28.8k chars of ``$ref``-expanded JSON passed, 33.6k
failed. The advisor's own earlier schema (24.0k expanded) passed live.

Pinned at the request boundary: the native schema switch is withheld and the schema
rides the system instruction as the JSON text contract (extract_json + kind validation
still enforce it). The rejection record now names the response schema as a suspect —
the rows had blamed ``response_mime_type``.
"""

from __future__ import annotations

import json
from pathlib import Path

from test_google_schema_beside_oversize_tool import _GEMINI_3

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.providers.google.translator import GoogleTranslator
from matrx_ai.providers.setting_rejection import response_schema_suspects

FIXTURE = json.loads(
    (Path(__file__).parent / "fixtures" / "gemini_response_schema_too_complex.json").read_text()
)
REFUSED = FIXTURE["refused_schema"]
ACCEPTED = FIXTURE["accepted_schema"]


def _wire(schema: dict, monkeypatch) -> dict:
    tr = GoogleTranslator()
    monkeypatch.setattr(tr, "build_provider_tools", lambda config, provider: [])
    config = UnifiedConfig(
        model=FIXTURE["model"],
        messages=MessageList(
            _messages=[
                UnifiedMessage(role="user", content=[TextContent(text="Step fetch failed: timeout.")])
            ]
        ),
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "recovery_advice", "schema": schema},
        },
    )
    return tr.to_google(config, _GEMINI_3)


def test_the_refused_schema_is_over_the_budget_and_the_accepted_one_is_not() -> None:
    budget = GoogleTranslator.GEMINI_RESPONSE_SCHEMA_EXPANDED_CHARS_BUDGET
    assert GoogleTranslator._expanded_schema_chars(REFUSED) > budget
    assert GoogleTranslator._expanded_schema_chars(ACCEPTED) <= budget
    conflict = GoogleTranslator._native_schema_too_complex(REFUSED)
    assert conflict is not None and conflict["budget"] == budget
    assert GoogleTranslator._native_schema_too_complex(ACCEPTED) is None


def test_recorded_refused_schema_moves_to_the_prompt(monkeypatch) -> None:
    cfg = _wire(REFUSED, monkeypatch)["config"]
    assert cfg.response_json_schema is None, "native schema sent past the decoder budget (the 400)"
    assert cfg.response_mime_type != "application/json"
    system = str(cfg.system_instruction)
    assert "FINAL ANSWER FORMAT" in system and "DefinitionPatch" in system


def test_accepted_schema_keeps_native_structured_output(monkeypatch) -> None:
    cfg = _wire(ACCEPTED, monkeypatch)["config"]
    assert cfg.response_json_schema is not None
    assert cfg.response_mime_type == "application/json"


def test_an_opaque_rejection_names_the_response_schema_as_a_suspect() -> None:
    wire = {"model": "gemini-3.8-flash", "config": {"response_mime_type": "application/json", "response_json_schema": REFUSED}}
    assert response_schema_suspects(wire) == ["config.response_json_schema"]
    assert response_schema_suspects({"config": {"temperature": 0.2}}) == []
