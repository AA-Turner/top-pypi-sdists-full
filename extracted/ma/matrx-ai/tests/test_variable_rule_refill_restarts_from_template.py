"""A second fill restarts every authored part from its template — or refuses loudly.

Round 4 made a config's second ``replace_variables`` a silent no-op, so
``apply_variables(force=True)``, ``clone().with_variables(...)`` after an apply, and an authored
message appended to an applied config were all ignored. The rule is "fill the authored template
exactly once": a refill starts again from each part's authored template (so a value's own braces
and the escape's result are never filled), and a part that cannot be restarted raises.
"""

from __future__ import annotations

import pytest

from matrx_ai.agents.definition import Agent
from matrx_ai.agents.variables import AgentVariable
from matrx_ai.config import MessageList, TextContent, UnifiedMessage
from matrx_ai.config.decision_input_config import DecisionQuestionsContent
from matrx_ai.config.media_config import ImageContent
from matrx_ai.config.speech_script_config import SpeechScriptContent
from matrx_ai.config.template_substitution import VariableRefillError
from matrx_ai.config.unified_config import UnifiedConfig


def _texts(config: UnifiedConfig) -> list[str]:
    return [getattr(b, "text", "") for m in config.messages for b in (m.content or [])]


def _agent() -> Agent:
    config = UnifiedConfig.from_dict(
        {
            "model": "m",
            "messages": [
                {"role": "system", "content": "S {{topic}} {{!topic}}"},
                {"role": "user", "content": "Topic: {{topic}} {{!topic}}"},
            ],
        }
    )
    return Agent(
        config=config,
        variable_defaults=AgentVariable.from_list([{"name": "topic", "defaultValue": "tea"}]),
    )


def test_force_reapply_fills_the_new_value_from_the_template() -> None:
    agent = _agent().apply_variables()
    assert agent.config.system_instruction.base_instruction == "S tea {{topic}}"
    agent.set_variable("topic", "coffee").apply_variables(force=True)
    assert agent.config.system_instruction.base_instruction == "S coffee {{topic}}"
    assert _texts(agent.config) == ["Topic: coffee {{topic}}"]


def test_clone_after_apply_fills_its_own_values() -> None:
    base = _agent().apply_variables()
    clone = base.clone().with_variables(topic="coffee")
    assert clone.config.system_instruction.base_instruction == "S coffee {{topic}}"
    assert _texts(clone.config) == ["Topic: coffee {{topic}}"]
    # The original is untouched.
    assert base.config.system_instruction.base_instruction == "S tea {{topic}}"
    assert _texts(base.config) == ["Topic: tea {{topic}}"]


def test_a_refill_never_fills_a_values_braces() -> None:
    config = UnifiedConfig.from_dict(
        {"model": "m", "messages": [{"role": "system", "content": "S {{x}} {{y}}"}, {"role": "user", "content": "U {{x}} {{y}}"}]}
    )
    config.replace_variables({"x": "{{y}}", "y": "Y1"})
    config.replace_variables({"x": "{{y}}", "y": "Y2"})
    assert config.system_instruction.base_instruction == "S {{y}} Y2"
    assert _texts(config) == ["U {{y}} Y2"]


def test_authored_text_appended_after_a_fill_is_filled() -> None:
    config = UnifiedConfig.from_dict({"model": "m", "messages": [{"role": "user", "content": "A {{topic}}"}]})
    config.replace_variables({"topic": "tea"})
    config.messages.append(UnifiedMessage(role="user", content=[TextContent(text="B {{topic}}")]))
    config.replace_variables({"topic": "tea"})
    assert _texts(config) == ["A tea", "B tea"]


def test_a_part_changed_after_its_fill_refuses_the_refill() -> None:
    config = UnifiedConfig.from_dict({"model": "m", "messages": [{"role": "user", "content": "A {{topic}}"}]})
    config.replace_variables({"topic": "tea"})
    config.messages[0].content[0].text += " edited"
    with pytest.raises(VariableRefillError):
        config.replace_variables({"topic": "coffee"})


def test_a_system_instruction_changed_after_its_fill_refuses_the_refill() -> None:
    config = UnifiedConfig.from_dict({"model": "m", "messages": [{"role": "system", "content": "S {{topic}}"}]})
    config.replace_variables({"topic": "tea"})
    config.system_instruction.base_instruction += " edited"
    with pytest.raises(VariableRefillError):
        config.replace_variables({"topic": "coffee"})


def test_a_dropped_part_refuses_the_refill() -> None:
    block = TextContent(text="{{neg}}", metadata={"role": "negative_prompt"})
    messages = MessageList(_messages=[UnifiedMessage(role="user", content=[block, TextContent(text="P")])])
    messages.replace_variables({"neg": ""})
    assert len(messages[0].content) == 1
    with pytest.raises(VariableRefillError):
        messages.replace_variables({"neg": "blurry"})


def test_glued_typed_tail_survives_a_restart() -> None:
    block = TextContent(text="Hello {{topic}}")
    messages = MessageList(_messages=[UnifiedMessage(role="user", content=[block])])
    messages.replace_variables({"topic": "tea"})
    messages.append_or_extend_user_input("typed {{topic}}")
    messages.replace_variables({"topic": "coffee"})
    assert block.text == "Hello coffee\ntyped {{topic}}"


def test_media_slot_restarts_and_renders_a_boolean_like_text() -> None:
    image = ImageContent(url="https://cdn.example.com/{{flag}}/{{name}}.png")
    assert image.replace_variables({"flag": True, "name": "a"}) is False
    assert image.url == "https://cdn.example.com/true/a.png"
    image.replace_variables({"flag": False, "name": "b"})
    assert image.url == "https://cdn.example.com/false/b.png"


def test_decision_and_speech_parts_restart_from_their_templates() -> None:
    q = DecisionQuestionsContent(questions=[{"name": "pick", "type": "choice", "instructions": "For {{city}}", "criteria": {"a": "A"}}])
    q.replace_variables({"city": "Rome"})
    q.replace_variables({"city": "Oslo"})
    assert q.questions[0]["instructions"] == "For Oslo"
    s = SpeechScriptContent(turns=[{"speaker": "Host", "text": "Say {{x}}"}])
    s.replace_variables({"x": "one"})
    s.replace_variables({"x": "two"})
    assert s.turns[0]["text"] == "Say two"
