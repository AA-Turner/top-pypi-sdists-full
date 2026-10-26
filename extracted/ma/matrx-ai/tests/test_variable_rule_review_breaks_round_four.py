"""Round-4 review probes on THE VARIABLE RULE (each was red before its fix).

R1 — an explicit ``template_message_count`` of 0 authors no message: a leading history system
     message is never lifted into the system instruction or filled. Only a missing count (an
     older client) lifts the leading system prompt.
R2 — the escape strips ``{{!`` for ANY space-free name (Arman, 2026-10-25); ``{{! comment }}`` and ``{{!}}`` stay.
R3 — a second ``replace_variables`` restarts from the authored template: never fills braces a value brought in.
R4 — a boolean renders as ``true`` / ``false`` (JSON), never Python's ``True`` / ``False``.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.config.prompt_values import prompt_safe_value
from matrx_ai.config.template_substitution import (
    OffValue,
    authored_template_messages,
    substitute_authored,
)
from matrx_ai.config.unified_config import UnifiedConfig

WIRE = [
    {"role": "system", "content": "HISTORY NOTE {{x}}"},
    {"role": "user", "content": "hello"},
    {"role": "assistant", "content": "hi"},
    {"role": "user", "content": "again"},
]


def _texts(config: UnifiedConfig) -> list[str]:
    return ["".join(getattr(c, "text", "") for c in m.content or []) for m in config.messages]


def _door(count: Any) -> UnifiedConfig:
    config = UnifiedConfig.from_dict(
        {"model": "m", "messages": [dict(m) for m in WIRE], "system_instruction": "SI {{x}}"},
        authored_message_count=count,
    )
    config.replace_variables(
        {"x": "FILLED"}, template_messages=authored_template_messages(WIRE, count, config.messages)
    )
    return config


def test_r1_a_count_of_zero_never_lifts_or_fills_a_history_system_message() -> None:
    config = _door(0)
    assert config.system_instruction.base_instruction == "SI FILLED"
    assert _texts(config)[0] == "HISTORY NOTE {{x}}"


def test_r1_a_missing_count_lifts_the_older_clients_leading_system_prompt() -> None:
    config = _door(None)
    assert config.system_instruction.base_instruction == "SI FILLED\n\nHISTORY NOTE FILLED"
    assert _texts(config) == ["hello", "hi", "again"]


def test_r1_a_stored_definition_still_lifts_every_system_message() -> None:
    config = UnifiedConfig.from_dict(
        {"model": "m", "messages": [*WIRE, {"role": "system", "content": "LATE"}]}
    )
    assert config.system_instruction.base_instruction == "HISTORY NOTE {{x}}\n\nLATE"


@pytest.mark.parametrize(
    ("escaped", "token"),
    [("{{!todo}}", "{{todo}}"), ("{{!#todo}}", "{{#todo}}"), ("{{!/todo}}", "{{/todo}}"), ("{{!^todo}}", "{{^todo}}"), ("{{!<todo>}}", "{{<todo>}}")],
)
def test_r2_an_undeclared_escape_becomes_its_token(escaped: str, token: str) -> None:
    # Rule 6 (Arman, 2026-10-25): any name, declared or not.
    template = f"keep {escaped} and {{{{!x}}}} {{{{x}}}}"
    out = substitute_authored(template, template, {"x": "V"}, prompt_safe_value, unescape=True)
    assert out == f"keep {token} and {{{{x}}}} V"


@pytest.mark.parametrize("literal", ["{{! comment }}", "{{!}}", "{{!-- note --}}", "{{!--note--}}", "{{!first name}}"])
def test_r2_what_is_not_an_escape_is_left_as_written(literal: str) -> None:
    template = f"keep {literal} and {{{{!x}}}} {{{{x}}}}"
    out = substitute_authored(template, template, {"x": "V"}, prompt_safe_value, unescape=True)
    assert out == f"keep {literal} and {{{{x}}}} V"


def test_r2_a_declared_block_name_is_escaped() -> None:
    template = "{{!<rules>}} {{!todo}}"
    out = substitute_authored(template, template, {}, prompt_safe_value, unescape=True, blocks={"rules": "R"})
    assert out == "{{<rules>}} {{todo}}"


def test_r3_a_second_fill_restarts_from_the_template() -> None:
    config = UnifiedConfig.from_dict(
        {
            "model": "m",
            "messages": [
                {"role": "system", "content": "S {{x}} {{y}}"},
                {"role": "user", "content": "U {{x}} {{y}}"},
            ],
        }
    )
    config.replace_variables({"x": "{{y}}", "y": "Y1"})
    first = (config.system_instruction.base_instruction, _texts(config))
    assert first == ("S {{y}} Y1", ["U {{y}} Y1"])
    config.replace_variables({"x": "{{y}}", "y": "Y2"})
    # The template is filled exactly once again: the new value lands, the value's braces don't.
    assert (config.system_instruction.base_instruction, _texts(config)) == ("S {{y}} Y2", ["U {{y}} Y2"])
    assert "_variables_filled" not in config.to_dict()


@pytest.mark.parametrize(("value", "text"), [(True, "true"), (False, "false")])
def test_r4_a_boolean_renders_as_json(value: bool, text: str) -> None:
    assert prompt_safe_value(value) == text
    out = substitute_authored("flag: {{f}}", "flag: {{f}}", {"f": value}, prompt_safe_value, unescape=True)
    assert out == f"flag: {text}"


def test_r4_a_toggle_still_renders_its_label() -> None:
    assert prompt_safe_value(OffValue("No")) == "No"
    assert prompt_safe_value("Yes") == "Yes"
