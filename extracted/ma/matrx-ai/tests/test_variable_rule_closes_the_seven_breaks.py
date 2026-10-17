"""THE VARIABLE RULE: the seven breaks an adversarial review proved (2026-10-16).

Each test is the reviewer's own input, typed as a literal, and names the break it catches.
One implementation: ``matrx_ai/config/template_substitution.py``.
"""

from __future__ import annotations

from matrx_ai.agents.variables import AgentVariable, compose_variable_values
from matrx_ai.config.decision_input_config import DecisionQuestionsContent
from matrx_ai.config.prompt_values import prompt_safe_value
from matrx_ai.config.speech_script_config import SpeechScriptContent
from matrx_ai.config.template_substitution import substitute_authored
from matrx_ai.config.unified_config import UnifiedConfig


def _defs(*specs: dict) -> dict:
    return AgentVariable.from_list([dict(s) for s in specs])


# 1. Undeclared values never fill the author's text.
def test_an_undeclared_client_value_never_fills_authored_text() -> None:
    values = compose_variable_values(_defs({"name": "city", "defaultValue": "Paris"}), {"secret": "LEAK"})
    assert "secret" not in values
    cfg = UnifiedConfig.from_dict({"model": "m", "messages": [
        {"role": "system", "content": "City {{city}}; literal {{secret}}"},
        {"role": "user", "content": "Ask about {{secret}}"}]})
    cfg.replace_variables(values)
    assert cfg.system_instruction.base_instruction == "City Paris; literal {{secret}}"
    assert cfg.messages[0].content[0].text == "Ask about {{secret}}"


def test_platform_keys_pass_through_but_never_fill_unless_declared() -> None:
    values = compose_variable_values(
        _defs({"name": "city", "defaultValue": "Paris"}),
        {"vsc_git_branch": "main", "__agent_user_input__": "typed"},
    )
    assert values["vsc_git_branch"] == "main" and values["__agent_user_input__"] == "typed"
    t = "{{city}} {{vsc_git_branch}} {{__agent_user_input__}}"
    assert substitute_authored(t, t, values, prompt_safe_value, unescape=True) == (
        "Paris {{vsc_git_branch}} {{__agent_user_input__}}"
    )
    declared = compose_variable_values(
        _defs({"name": "vsc_git_branch"}), {"vsc_git_branch": "main"}
    )
    assert substitute_authored("{{vsc_git_branch}}", "{{vsc_git_branch}}", declared, str) == "main"


def test_no_definitions_at_all_keeps_the_client_dict_as_the_declaration() -> None:
    values = compose_variable_values(None, {"topic": "tea"})
    assert substitute_authored("{{topic}}", "{{topic}}", values, str) == "tea"


def test_a_stored_agent_that_declares_nothing_fills_nothing() -> None:
    values = compose_variable_values({}, {"secret": "LEAK"}, declared_only=True)
    assert substitute_authored("{{secret}}", "{{secret}}", values, str) == "{{secret}}"


# 2. Decision-question and speech-script parts get the escape and the sections.
def test_decision_question_part_runs_the_escape_and_sections() -> None:
    part = DecisionQuestionsContent(questions=[{
        "name": "q", "type": "choice",
        "instructions": "Pick {{!city}} for {{city}}{{#vip}} as VIP{{/vip}}",
        "criteria": {"a": "A {{city}}"},
    }])
    part.replace_variables({"city": "Rome", "vip": ""})
    assert part.questions[0]["instructions"] == "Pick {{city}} for Rome"
    assert part.questions[0]["criteria"] == {"a": "A Rome"}


def test_speech_script_part_runs_the_escape_and_sections_even_with_no_values() -> None:
    part = SpeechScriptContent(turns=[{"speaker": "Host", "text": "Say {{!x}}{{#x}} X{{/x}}"}])
    part.replace_variables({"x": "on"})
    assert part.turns[0]["text"] == "Say {{x}} X"
    bare = SpeechScriptContent(turns=[{"speaker": "Host", "text": "Say {{!name}} {{!todo}}"}])
    bare.replace_variables({"name": ""})
    assert bare.turns[0]["text"] == "Say {{name}} {{!todo}}"


# 3. Every authored field of a structured system instruction is filled.
def test_structured_system_instruction_fills_every_authored_field() -> None:
    cfg = UnifiedConfig.from_dict({"model": "m", "messages": [{"role": "user", "content": "hi"}],
        "system_instruction": {"content": "Base {{city}}", "intro": "Intro {{city}}",
                               "outro": "Outro {{!city}}", "prepend_sections": ["Pre {{city}}"],
                               "append_sections": ["App {{city}} {{other}}"], "include_date": False}})
    cfg.replace_variables({"city": "Oslo"})
    si = cfg.system_instruction
    assert (si.base_instruction, si.intro, si.outro) == ("Base Oslo", "Intro Oslo", "Outro {{city}}")
    assert si.prepend_sections == ["Pre Oslo"]
    assert si.append_sections == ["App Oslo {{other}}"]


# 4. The escape is exactly {{!NAME}} (and #/^/'/'/<NAME>) for a DECLARED name; nothing else.
def test_the_escape_is_only_a_name() -> None:
    t = "{{! a comment }} and {{!-- x --}} and {{!}}"
    assert substitute_authored(t, t, {}, str, unescape=True) == t
    t2 = "{{!name}} {{!#a}}{{!/a}} {{!^b}} {{!<blk>}}"
    assert substitute_authored(t2, t2, {}, str, unescape=True) == t2
    declared = {"name": "", "a": "", "b": ""}
    out = substitute_authored(t2, t2, declared, str, unescape=True, blocks={"blk": ""})
    assert out == "{{name}} {{#a}}{{/a}} {{^b}} {{<blk>}}"


# 5. A second system message is never dropped.
def test_every_system_message_is_lifted_in_order() -> None:
    cfg = UnifiedConfig.from_dict({"model": "m", "messages": [
        {"role": "system", "content": "First"},
        {"role": "user", "content": "hello"},
        {"role": "developer", "content": "SECOND rule"}]})
    assert cfg.system_instruction.base_instruction == "First\n\nSECOND rule"


# 6. Whitespace-only text from the client is a cleared value, never the default.
def test_whitespace_only_value_is_cleared() -> None:
    d = _defs({"name": "tone", "defaultValue": "formal"})
    assert compose_variable_values(d, {"tone": "   "})["tone"] == ""
    assert compose_variable_values(d, {"tone": None})["tone"] == "formal"
    assert compose_variable_values(d, {})["tone"] == "formal"
