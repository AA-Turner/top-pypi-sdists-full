"""Conditional sections (Mustache) in the one variable rule — config/template_substitution.py.

``{{#name}}..{{/name}}`` stays only when declared ``name`` is filled; ``{{^name}}..{{/name}}`` only
when it is empty. Declared names only. Expected strings are exact.
"""

from __future__ import annotations

import pytest

from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.config.unified_content import TextContent


def render(text: str, variables: dict) -> str:
    block = TextContent(text=text)
    block.replace_variables(variables)
    return block.text


BLOCK = "Intro\n{{#extra}}\n## Additional Requirements:\n{{extra}}\nBe careful.\n{{/extra}}\nOutro"


def test_a_filled_section_stays_and_its_tag_lines_vanish() -> None:
    assert render(BLOCK, {"extra": "Use metric."}) == (
        "Intro\n## Additional Requirements:\nUse metric.\nBe careful.\nOutro"
    )


@pytest.mark.parametrize("empty", ["", "   ", " \n\t ", None])
def test_an_empty_section_leaves_no_residue(empty) -> None:
    assert render(BLOCK, {"extra": "" if empty is None else empty}) == "Intro\nOutro"


def test_a_declared_variable_given_no_value_removes_the_section() -> None:
    assert render(BLOCK, {"extra": ""}) == "Intro\nOutro"


def test_the_inverse_section_stays_only_when_empty() -> None:
    text = "Start\n{{^extra}}\nNo extras.\n{{/extra}}\nEnd"
    assert render(text, {"extra": ""}) == "Start\nNo extras.\nEnd"
    assert render(text, {"extra": "x"}) == "Start\nEnd"


def test_inline_sections_keep_the_line() -> None:
    text = "Hi{{#name}}, {{name}}{{/name}}{{^name}} there{{/name}}!"
    assert render(text, {"name": "Ada"}) == "Hi, Ada!"
    assert render(text, {"name": ""}) == "Hi there!"


def test_nested_sections() -> None:
    text = "{{#a}}\nA\n{{#b}}\nB\n{{/b}}\n{{^b}}\nnoB\n{{/b}}\n{{/a}}\nend"
    assert render(text, {"a": "1", "b": "1"}) == "A\nB\nend"
    assert render(text, {"a": "1", "b": ""}) == "A\nnoB\nend"
    assert render(text, {"a": "", "b": "1"}) == "end"


def test_an_undeclared_name_is_left_exactly_as_written() -> None:
    text = "{{#ghost}}\nkeep\n{{/ghost}}\n{{^ghost}}x{{/ghost}} {{ghost}}"
    assert render(text, {"other": "1"}) == text
    assert render(text, {}) == text


def test_a_declared_and_an_undeclared_section_mix() -> None:
    text = "{{#a}}A{{/a}}|{{#ghost}}G{{/ghost}}"
    assert render(text, {"a": "1"}) == "A|{{#ghost}}G{{/ghost}}"


def test_braces_a_value_brings_in_are_data() -> None:
    assert render("Q: {{q}}", {"q": "{{#q}}x{{/q}} {{^q}}y{{/q}}"}) == "Q: {{#q}}x{{/q}} {{^q}}y{{/q}}"
    assert render("{{#q}}Q: {{q}}{{/q}}", {"q": "{{#q}}"}) == "Q: {{#q}}"


def test_a_value_that_is_only_a_section_still_counts_as_filled() -> None:
    assert render("{{#q}}yes{{/q}}", {"q": "{{/q}}"}) == "yes"


def test_an_unclosed_tag_renders_literally_and_never_crashes() -> None:
    assert render("a {{#x}} b", {"x": "1"}) == "a {{#x}} b"
    assert render("a {{/x}} b", {"x": "1"}) == "a {{/x}} b"
    assert render("{{#x}}\nopen\n", {"x": ""}) == "{{#x}}\nopen\n"


def test_an_unclosed_inner_tag_does_not_break_the_outer_section() -> None:
    assert render("{{#a}}x {{#b}} y{{/a}}", {"a": "1", "b": "1"}) == "x {{#b}} y"


def test_the_section_escape_is_a_literal_tag() -> None:
    assert render("{{!#x}}k{{!/x}} {{x}}", {"x": "1"}) == "{{#x}}k{{/x}} 1"


def test_a_system_prompt_gets_sections_too() -> None:
    config = UnifiedConfig(
        model="claude-opus-5-5",
        system_instruction="You help.\n{{#style}}\nStyle: {{style}}\n{{/style}}\nDone.",
        messages=[],
    )
    config.replace_variables({"style": "formal"})
    assert config.system_instruction.base_instruction == "You help.\nStyle: formal\nDone."
    empty = UnifiedConfig(
        model="claude-opus-5-5",
        system_instruction="You help.\n{{#style}}\nStyle: {{style}}\n{{/style}}\nDone.",
        messages=[],
    )
    empty.replace_variables({"style": ""})
    assert empty.system_instruction.base_instruction == "You help.\nDone."


def test_crlf_lines_are_standalone_too() -> None:
    assert render("a\r\n{{#x}}\r\nb\r\n{{/x}}\r\nc", {"x": "1"}) == "a\r\nb\r\nc"
    assert render("a\r\n{{#x}}\r\nb\r\n{{/x}}\r\nc", {"x": ""}) == "a\r\nc"


PARAGRAPHS = "Intro.\n\n{{#extra}}\n\n## Extra\n\n{{extra}}\n\n{{/extra}}\n\nEnd."


def test_paragraph_separated_text_loses_the_section_without_extra_blank_lines() -> None:
    assert render(PARAGRAPHS, {"extra": ""}) == "Intro.\n\nEnd."
    assert render(PARAGRAPHS, {"extra": "  "}) == "Intro.\n\nEnd."


def test_paragraph_separated_text_keeps_the_section_with_exact_separators() -> None:
    assert render(PARAGRAPHS, {"extra": "V"}) == "Intro.\n\n## Extra\n\nV\n\nEnd."


def test_paragraph_separated_inverse_section() -> None:
    text = "Intro.\n\n{{^extra}}\n\nNone given.\n\n{{/extra}}\n\nEnd."
    assert render(text, {"extra": ""}) == "Intro.\n\nNone given.\n\nEnd."
    assert render(text, {"extra": "V"}) == "Intro.\n\nEnd."


def test_single_newline_form_is_unchanged() -> None:
    text = "Intro.\n{{#extra}}\n## Extra\n{{extra}}\n{{/extra}}\nEnd."
    assert render(text, {"extra": ""}) == "Intro.\nEnd."
    assert render(text, {"extra": "V"}) == "Intro.\n## Extra\nV\nEnd."


def test_nested_paragraph_sections() -> None:
    text = "A\n\n{{#a}}\n\nB\n\n{{#b}}\n\nC\n\n{{/b}}\n\nD\n\n{{/a}}\n\nE"
    assert render(text, {"a": "1", "b": ""}) == "A\n\nB\n\nD\n\nE"
    assert render(text, {"a": "1", "b": "1"}) == "A\n\nB\n\nC\n\nD\n\nE"
    assert render(text, {"a": "", "b": "1"}) == "A\n\nE"


def test_a_removed_one_line_section_takes_its_line_and_leaves_one_gap() -> None:
    text = "Intro.\n\n{{#extra}}Only this line.{{/extra}}\n\nEnd."
    assert render(text, {"extra": ""}) == "Intro.\n\nEnd."
    assert render(text, {"extra": "V"}) == "Intro.\n\nOnly this line.\n\nEnd."
    single = "Intro.\n{{#extra}}Only this line.{{/extra}}\nEnd."
    assert render(single, {"extra": ""}) == "Intro.\nEnd."


def test_a_removed_inline_section_in_a_sentence_keeps_the_sentence() -> None:
    assert render("Hi{{#x}}, there{{/x}}!", {"x": ""}) == "Hi!"
    assert render("Intro.\n\nSay{{#x}} more{{/x}}.\n\nEnd.", {"x": ""}) == "Intro.\n\nSay.\n\nEnd."
