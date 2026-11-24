"""A Gemini turn with a response schema AND 53 small tools must reach Google intact.

THE BUG (2026-11-02): the "Sandbox Specialist" agent (structured output + the Work-mode
tool surface, 53 declarations, none over 12 parameters) failed every run on
gemini-3.8-flash with a bare 400 "Request contains an invalid argument." The recorded
request replays: fails as sent; passes with the schema removed; passes with the tools
removed; the first 52 declarations pass, every declaration passes alone. Google's
constrained decoder refuses declarations that are too big IN TOTAL (edge ~67k chars of
declaration JSON; this turn is 69.2k), which the per-declaration parameter budget
could not see.

Pinned at the request boundary: tools kept whole, native schema switch withheld, schema
rides the system instruction. The offline tests go red if the translator sends
`response_json_schema` beside the recorded declarations.
"""

from __future__ import annotations

import json
from pathlib import Path

from test_google_schema_beside_oversize_tool import _GEMINI_3, _wire

from matrx_ai.providers.google.translator import GoogleTranslator

FIXTURE = json.loads(
    (Path(__file__).parent / "fixtures" / "gemini_schema_beside_53_tools_refused.json").read_text()
)
DECLS: list[dict] = FIXTURE["declarations"]


def test_no_single_tool_is_oversize_only_the_total_is() -> None:
    assert len(DECLS) == 53
    assert all(
        GoogleTranslator._count_param_names(d.get("parameters"))
        <= GoogleTranslator.GEMINI_SCHEMA_TOOL_PARAM_BUDGET
        for d in DECLS
    )
    conflict = GoogleTranslator._native_schema_tool_conflict(DECLS, is_gemini_3=True)
    assert conflict is not None and "total_chars" in conflict
    # the 52 that Google accepted (measured) stay native
    assert GoogleTranslator._native_schema_tool_conflict(DECLS[:40], is_gemini_3=True) is None


def test_recorded_53_tool_request_keeps_every_tool_and_moves_the_schema_to_the_prompt(
    monkeypatch,
) -> None:
    cfg = _wire(_GEMINI_3, DECLS, monkeypatch)["config"]
    sent = [fd.name for t in cfg.tools or [] for fd in (t.function_declarations or [])]
    assert sent == [d["name"] for d in DECLS], "a tool was dropped"
    assert cfg.response_json_schema is None, "native schema sent beside 53 tools (the 400)"
    assert cfg.response_mime_type != "application/json"
