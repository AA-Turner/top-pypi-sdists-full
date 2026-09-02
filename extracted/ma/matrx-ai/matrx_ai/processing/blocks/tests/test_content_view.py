"""The agent output contract's content view (plan §6) — scenario coverage.

Arman's scenarios, ratified 2026-08-20: plain text → one markdown instance;
text with embedded self-described JSON → interleaved instances; unnamed
structure folds back into prose with zero data loss; the simple and complex
cases are ONE shape.
"""

from __future__ import annotations

from matrx_ai.processing.blocks.content_view import content_from_text


def test_plain_text_is_one_markdown_instance() -> None:
    content = content_from_text("Just prose.\n\nTwo paragraphs of it.")
    assert len(content) == 1
    assert content[0]["__kind"] == "markdown"
    assert "Two paragraphs" in content[0]["text"]


def test_empty_text_is_empty_content() -> None:
    assert content_from_text("") == []
    assert content_from_text("   \n  ") == []


def test_self_described_json_interleaves_with_prose() -> None:
    text = (
        "Here are the ratings I found.\n\n"
        '```json\n{"__kind": "rating", "value": 4.5, "count": 10}\n```\n\n'
        "And a second one:\n\n"
        '```json\n{"__kind": "rating", "value": 3.0, "count": 2}\n```\n\n'
        "That is all."
    )
    content = content_from_text(text)
    kinds = [c["__kind"] for c in content]
    assert kinds == ["markdown", "rating", "markdown", "rating", "markdown"]
    assert content[1]["value"] == 4.5
    assert content[3]["count"] == 2


def test_anonymous_json_folds_into_prose_with_zero_loss() -> None:
    # No __kind, no envelope: it cannot be named, so it must NOT gain a fake
    # identity — it stays in the prose, re-fenced, byte content preserved.
    text = 'Intro.\n\n```json\n{"plain": "object"}\n```\n\nOutro.'
    content = content_from_text(text)
    assert [c["__kind"] for c in content] == ["markdown"]
    assert '{"plain": "object"}' in content[0]["text"]
    assert "```json" in content[0]["text"]  # re-fenced, renders as code


def test_plain_code_folds_back_refenced() -> None:
    text = "Look:\n\n```python\nprint('hi')\n```\n\nDone."
    content = content_from_text(text)
    assert len(content) == 1
    assert "```python" in content[0]["text"]
    assert "print('hi')" in content[0]["text"]


def test_six_embedded_kinds_are_six_routable_instances() -> None:
    blocks = "\n\n".join(
        f'```json\n{{"__kind": "rating", "value": {i}.0}}\n```' for i in range(6)
    )
    content = content_from_text(f"Ratings sweep:\n\n{blocks}")
    ratings = [c for c in content if c["__kind"] == "rating"]
    assert [r["value"] for r in ratings] == [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]


def test_self_described_kind_escapes_a_malformed_outer_fence() -> None:
    payload = (
        '{"__kind":"rating","value":4.5,'
        '"note":"braces } { and [arrays] inside strings stay valid"}'
    )
    text = (
        "Rules:\n[OUTPUT RULES — ABSOLUTE]\n```\n\n"
        "**Output contract:**\n\n```json\n"
        f"{payload}\n```"
    )

    content = content_from_text(text)
    assert [item["__kind"] for item in content] == ["markdown", "rating"]
    assert content[1]["value"] == 4.5
    assert "Output contract" in content[0]["text"]


def test_nested_kinds_escape_code_xml_and_anonymous_json_in_order() -> None:
    one = '{"__kind":"rating","value":1}'
    two = '{"__kind":"rating","value":2}'
    three = '{"__kind":"rating","value":3}'
    text = (
        f"```python\nbefore\n{one}\nafter\n```\n"
        f"<custom>before {two} after</custom>\n"
        f"```json\n{{\"wrapper\":{three}}}\n```"
    )

    content = content_from_text(text)
    ratings = [item for item in content if item["__kind"] == "rating"]
    assert [item["value"] for item in ratings] == [1, 2, 3]
    assert any(item["__kind"] == "markdown" for item in content)
