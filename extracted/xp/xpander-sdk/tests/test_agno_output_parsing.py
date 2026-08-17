"""Structured-output parsing keeps the markdown a model wrote with literal newlines."""

import json
from typing import Any, Callable, List

import pytest
from pydantic import BaseModel

from xpander_sdk.utils.agno_output_parsing import (
    install_agno_output_parsing_patch,
    lenient_structured_parse,
)


class Envelope(BaseModel):
    title: str
    short_summary: str
    final_result: str


ANSWER = (
    "I researched xpander.ai and sent the summary.\n\n"
    "### What it is\n"
    "xpander.ai is an **AI Agent platform**.\n\n"
    "### Key features\n"
    "| Feature | Detail |\n|---|---|\n| Workbench | build/test/deploy |\n"
)


def _raw_with_literal_newlines() -> str:
    """The failing shape: escaped JSON, but final_result has real line breaks."""
    head = json.dumps({"title": "Research", "short_summary": "Sent."})[:-1]
    return head + ', "final_result": "' + ANSWER.replace('"', '\\"') + '"}'


@pytest.fixture(autouse=True)
def _patched():
    install_agno_output_parsing_patch()


def _parse(content: str):
    from agno.agent import _response as agno_response

    return agno_response.parse_response_model_str(content, Envelope)


def test_literal_newlines_survive():
    parsed = _parse(_raw_with_literal_newlines())
    assert parsed is not None
    assert parsed.final_result == ANSWER
    assert "### What it is" in parsed.final_result.split("\n")
    assert "|---|---|" in parsed.final_result.split("\n")


def test_agno_alone_flattens_the_same_payload():
    """Guard the diagnosis: without the lenient tier agno destroys the line breaks."""
    from agno.utils.string import _clean_json_content

    cleaned = _clean_json_content(_raw_with_literal_newlines())
    assert "\n" not in cleaned


def test_escaped_payload_unchanged():
    raw = json.dumps({"title": "T", "short_summary": "S", "final_result": ANSWER})
    parsed = _parse(raw)
    assert parsed.final_result == ANSWER


def test_json_fenced_envelope():
    raw = "```json\n" + _raw_with_literal_newlines() + "\n```"
    parsed = _parse(raw)
    assert parsed.final_result == ANSWER


def test_inner_code_fence_kept_verbatim():
    answer = "Here:\n\n```python\nprint('hi')\n```\n\nDone."
    raw = '{"title": "T", "short_summary": "S", "final_result": "' + answer + '"}'
    parsed = _parse(raw)
    assert parsed.final_result == answer
    assert parsed.final_result.count("```") == 2


def test_unescaped_interior_quotes_still_parse():
    """Interior quotes the model forgot to escape - the raw-envelope-in-chat shape."""
    answer = 'The paper "Attention Is All You Need" matters.\n\n- point one'
    raw = '{"title": "T", "short_summary": "S", "final_result": "' + answer + '"}'
    parsed = _parse(raw)
    assert parsed is not None
    assert "Attention Is All You Need" in parsed.final_result


def test_multiple_objects_defer_to_agno():
    """A discarded draft plus the real envelope: agno's merge path stays in charge."""
    draft = json.dumps({"title": "draft", "short_summary": "", "final_result": ""})
    real = json.dumps({"title": "T", "short_summary": "S", "final_result": "done"})
    assert lenient_structured_parse(draft + "\n" + real) is None
    assert _parse(draft + "\n" + real) is not None


def test_prose_only_input_is_not_hijacked():
    assert lenient_structured_parse("just a sentence, no json here") is None
    assert _parse("just a sentence, no json here") is None


def _counting_original(calls: List[Any]) -> Callable:
    """Stand-in for agno's parser that records every content it is delegated."""

    def original(content: Any, output_schema: Any = None) -> None:
        calls.append(content)
        return None

    return original


def test_empty_and_prose_content_never_reach_agno() -> None:
    """Streaming narration/empty turns must not enter agno's warning chain."""
    from xpander_sdk.utils.agno_output_parsing import (
        _patch_parse_response_dict_str,
        _patch_parse_response_model_str,
    )

    calls: List[Any] = []
    wrapped = _patch_parse_response_model_str(_counting_original(calls))
    assert wrapped("", Envelope) is None
    assert wrapped("   \n", Envelope) is None
    assert wrapped("Let me check the calendar first.", Envelope) is None
    assert calls == []

    dict_calls: List[Any] = []
    wrapped_dict = _patch_parse_response_dict_str(_counting_original(dict_calls))
    assert wrapped_dict("") is None
    assert wrapped_dict("plain narration, nothing structured") is None
    assert dict_calls == []


def test_bare_scalar_json_still_delegates() -> None:
    """agno's json.loads tier accepts scalars - a brace-less 'true' stays agno's call."""
    from xpander_sdk.utils.agno_output_parsing import _patch_parse_response_dict_str

    calls: List[Any] = []
    wrapped = _patch_parse_response_dict_str(_counting_original(calls))
    assert wrapped("true") is None
    assert wrapped("42") is None
    assert wrapped('"quoted answer"') is None
    assert len(calls) == 3


def test_prose_wrapping_a_real_envelope_still_parses() -> None:
    """Prose followed by a real envelope keeps parsing end to end."""
    raw = "Here you go:\n" + json.dumps(
        {"title": "T", "short_summary": "S", "final_result": "done"}
    )
    assert _parse(raw).final_result == "done"


def test_unparseable_braced_content_still_delegates() -> None:
    """Anything carrying a brace keeps agno's original in the loop."""
    from xpander_sdk.utils.agno_output_parsing import _patch_parse_response_model_str

    calls: List[Any] = []
    wrapped = _patch_parse_response_model_str(_counting_original(calls))
    assert wrapped('{"title": broken', Envelope) is None
    assert len(calls) == 1


def test_missing_required_field_falls_back():
    """A dict that fails validation must not short-circuit agno's remaining tiers."""
    raw = '{"title": "T", "final_result": "body"}'
    assert isinstance(lenient_structured_parse(raw), dict)
    assert _parse(raw) is None


def test_dict_parser_also_keeps_newlines():
    from agno.agent import _response as agno_response

    parsed = agno_response.parse_response_dict_str(_raw_with_literal_newlines())
    assert parsed["final_result"] == ANSWER


def test_install_is_idempotent():
    from agno.agent import _response as agno_response

    first = agno_response.parse_response_model_str
    install_agno_output_parsing_patch()
    assert agno_response.parse_response_model_str is first


def test_thinking_block_before_the_envelope():
    """A reasoning model's <think> prelude must not cost the answer its line breaks."""
    prelude = "<think>weighing {options} and more {braces}</think>\n"
    raw = prelude + _raw_with_literal_newlines()
    assert _parse(raw).final_result == ANSWER


def test_trailing_tag_fragment_after_the_envelope():
    raw = _raw_with_literal_newlines() + "</invoke>"
    assert _parse(raw).final_result == ANSWER


def test_failed_import_does_not_lock_out_a_retry(monkeypatch):
    """A transient import failure must not permanently disable the patch."""
    import importlib

    from xpander_sdk.utils import agno_output_parsing as mod

    monkeypatch.setattr(mod, "_INSTALLED", False)
    def _boom(name):
        raise ImportError(name)

    monkeypatch.setattr(importlib, "import_module", _boom)
    assert mod.install_agno_output_parsing_patch() is False
    assert mod._INSTALLED is False

    monkeypatch.undo()
    monkeypatch.setattr(mod, "_INSTALLED", False)
    assert mod.install_agno_output_parsing_patch() is True
    assert _parse(_raw_with_literal_newlines()).final_result == ANSWER
