"""THE ONE VARIABLE RULE (Arman, 2026-10-10) — config/template_substitution.py.

Only declared variables are filled, once. A declared variable with no value becomes "".
Every other {{...}} is left exactly as written; nothing is added to the prompt.
The one escape: {{!name}} in the author's text becomes {{name}}.
"""

from __future__ import annotations

import pytest

from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.config.unified_content import TextContent

PROMPT = "This is {{my}} little {{fake}} prompt and /{{my}} example"


@pytest.mark.parametrize(
    ("variables", "expected"),
    [
        ({"fake": "VALUE"}, "This is {{my}} little VALUE prompt and /{{my}} example"),
        ({"fake": ""}, "This is {{my}} little  prompt and /{{my}} example"),
        ({"fake": None}, "This is {{my}} little  prompt and /{{my}} example"),
        ({"fake": "VALUE", "my": "ARMAN"}, "This is ARMAN little VALUE prompt and /ARMAN example"),
        ({}, PROMPT),
    ],
)
def test_the_owners_example_in_a_message(variables: dict, expected: str) -> None:
    block = TextContent(text=PROMPT)
    block.replace_variables({k: ("" if v is None else v) for k, v in variables.items()})
    assert block.text == expected


@pytest.mark.parametrize(
    ("variables", "expected"),
    [
        ({"fake": "VALUE"}, "This is {{my}} little VALUE prompt and /{{my}} example"),
        ({"fake": ""}, "This is {{my}} little  prompt and /{{my}} example"),
        ({"fake": "VALUE", "my": "ARMAN"}, "This is ARMAN little VALUE prompt and /ARMAN example"),
    ],
)
def test_the_owners_example_in_a_system_prompt_adds_nothing(variables: dict, expected: str) -> None:
    config = UnifiedConfig(model="claude-opus-5-5", system_instruction=PROMPT, messages=[])
    config.replace_variables(variables)
    assert config.system_instruction.base_instruction == expected


def test_a_value_is_never_filled_by_another_variable() -> None:
    block = TextContent(text="{{transcript}} for {{region}}")
    block.replace_variables({"transcript": "stores in {{region}}", "region": "Arizona"})
    assert block.text == "stores in {{region}} for Arizona"


def test_the_escape_becomes_plain_braces_and_is_never_filled() -> None:
    block = TextContent(text="Write {{!name}} literally; hello {{name}}.")
    block.replace_variables({"name": "Ada"})
    assert block.text == "Write {{name}} literally; hello Ada."


def test_the_escape_is_removed_even_with_no_value() -> None:
    config = UnifiedConfig(model="claude-opus-5-5", system_instruction="Use {{!slot}} in templates.", messages=[])
    config.replace_variables({"slot": None})
    assert config.system_instruction.base_instruction == "Use {{slot}} in templates."


def test_a_values_escape_is_data() -> None:
    block = TextContent(text="Quote: {{quote}}")
    block.replace_variables({"quote": "say {{!x}}"})
    assert block.text == "Quote: say {{!x}}"


def test_backslashes_and_spaces_mean_nothing() -> None:
    block = TextContent(text=r"a \{{fake}} b {{ fake }} c")
    block.replace_variables({"fake": "V"})
    assert block.text == r"a \V b {{ fake }} c"
