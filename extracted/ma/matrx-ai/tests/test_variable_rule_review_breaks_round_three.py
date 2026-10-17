"""Round-3 review probes on THE VARIABLE RULE (each was red before its fix).

P3 — the escape accepts exactly the names the fill accepts: any DECLARED name, verbatim
     (spaces, accents, colons), plus the ``NAME_PATTERN`` shape.
P4 — the person's typed input is data the moment it is set: a forced re-apply refills the
     authored template with the new value and never fills her text, whether it is its own block
     or text glued onto an authored block.
"""

from __future__ import annotations

import pytest

from matrx_ai.agents.definition import Agent
from matrx_ai.agents.variables import AgentVariable, compose_variable_values
from matrx_ai.config.prompt_values import prompt_safe_value
from matrx_ai.config.template_substitution import substitute_authored
from matrx_ai.config.unified_config import UnifiedConfig


def _texts(config: UnifiedConfig) -> list[str]:
    return [getattr(b, "text", "") for m in config.messages for b in (m.content or [])]


@pytest.mark.parametrize("name", ["first name", "société", "1st", "x:y", "名前"])
def test_p3_every_fillable_name_can_be_escaped(name: str) -> None:
    values = compose_variable_values(AgentVariable.from_list([{"name": name, "defaultValue": "V"}]), {})
    template = "fill {{" + name + "}} esc {{!" + name + "}} sec {{!#" + name + "}}"
    out = substitute_authored(template, template, values, prompt_safe_value, unescape=True)
    assert out == "fill V esc {{" + name + "}} sec {{#" + name + "}}"


def test_p3_undeclared_odd_name_is_not_an_escape() -> None:
    template = "keep {{!first name}} and {{! a comment }}"
    out = substitute_authored(template, template, {}, prompt_safe_value, unescape=True)
    assert out == template


def _agent(user_template: str) -> Agent:
    config = UnifiedConfig.from_dict(
        {
            "model": "m",
            "messages": [
                {"role": "system", "content": "S {{topic}}"},
                {"role": "user", "content": user_template},
            ],
        }
    )
    return Agent(config=config, variable_defaults=AgentVariable.from_list([{"name": "topic", "defaultValue": "tea"}]))


def test_p4_typed_block_is_never_filled_on_a_forced_reapply() -> None:
    agent = _agent("Topic: {{topic}}")
    agent.set_user_input("person typed {{topic}} and {{!topic}}")
    # The forced re-apply really refills the authored template with the new value ...
    agent.set_variable("topic", "coffee").apply_variables(force=True)
    texts = _texts(agent.config)
    assert agent.config.system_instruction.base_instruction == "S coffee"
    assert any(t.startswith("Topic: coffee") for t in texts)
    # ... and her typed words stay exactly as she wrote them.
    assert any(t.endswith("person typed {{topic}} and {{!topic}}") for t in texts)
    assert not any("person typed tea" in t or "person typed coffee" in t for t in texts)


def test_p4_typed_text_glued_onto_an_authored_block_is_never_filled() -> None:
    agent = _agent("Write about {{topic}}:")  # filled seed glued with her words (or own block)
    agent.set_user_input([{"type": "text", "text": "mine {{topic}} {{!topic}}"}])
    agent.set_variable("topic", "coffee").apply_variables(force=True)
    joined = "\n".join(_texts(agent.config))
    assert "Write about coffee:" in joined  # the authored head really refilled
    assert "Write about tea:" not in joined
    assert "mine {{topic}} {{!topic}}" in joined
    assert "mine tea" not in joined and "mine coffee" not in joined


def test_p4_glued_tail_keeps_the_authored_head_filled() -> None:
    from matrx_ai.config import MessageList, TextContent, UnifiedMessage

    block = TextContent(text="Hello {{topic}}")
    messages = MessageList(_messages=[UnifiedMessage(role="user", content=[block])])
    messages.append_or_extend_user_input("typed {{topic}}")
    messages.replace_variables({"topic": "tea"})
    assert block.text == "Hello tea\ntyped {{topic}}"
    messages.replace_variables({"topic": "tea"})
    assert block.text == "Hello tea\ntyped {{topic}}"
