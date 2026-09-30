"""fence captured values spliced into a VQE vision query.

automind's vision model reads the query as prose. A multi-line or list value
substituted inline runs together with the surrounding words, and the model binds
the predicate to the LAST line instead of the whole captured block — a
confident, wrong verdict.

Port of V2 (_fence_vision_query_value).
"""
import pytest
from unittest.mock import MagicMock, patch

from testmu_selenium._helpers._vision_fence import fence_templates, fence_value
from testmu_selenium._vars import var, set_var, clear_state, _test_params

MULTILINE = "line one\nline two\nline three"


@pytest.fixture(autouse=True)
def _clean():
    clear_state()
    yield
    clear_state()


def _fence(text):
    return fence_templates(text, var)


def test_substituted_value_is_triple_quoted():
    set_var("v", MULTILINE)
    out = _fence("Does {{v}} appear?")
    assert '"""' in out and MULTILINE in out
    # The whole block sits between the fences, so the model cannot bind only to
    # "line three".
    assert out.split('"""')[1].strip() == MULTILINE


def test_surrounding_prose_stays_outside_the_fence():
    """Only the VALUE is fenced — fencing the whole string would put the
    question itself inside the quotes and change what is being asked."""
    set_var("v", "abc")
    out = _fence("Does {{v}} appear?")
    assert out.startswith("Does ")
    assert out.rstrip().endswith("appear?")


def test_whole_string_template_is_fenced():
    set_var("v", MULTILINE)
    out = _fence("{{v}}")
    assert '"""' in out and MULTILINE in out


def test_list_values_are_fenced_as_one_block():
    set_var("rows", ["a", "b", "c"])
    out = _fence("Is {{rows}} present?")
    assert out.count('"""') == 2


def test_multiple_substitutions_are_each_fenced():
    set_var("a", "one")
    set_var("b", "two")
    out = _fence("{{a}} then {{b}}")
    assert out.count('"""') == 4  # two fenced blocks


def test_dollar_params_are_fenced_too():
    _test_params["p"] = MULTILINE
    out = _fence("Check ${p}")
    assert '"""' in out and MULTILINE in out


def test_unresolved_templates_are_left_literal_not_fenced():
    # An unresolved name must stay a visible {{token}} so the failure is legible;
    # fencing it would bury the problem in quotes.
    out = _fence("Check {{missing}}")
    assert out == "Check {{missing}}"
    assert '"""' not in out


def test_plain_text_is_untouched():
    assert _fence("no templates here") == "no templates here"


def test_non_string_passes_through():
    assert fence_templates(None, var) is None
    assert fence_templates(42, var) == 42


def test_fence_value_shape():
    assert fence_value("x") == '\n"""\nx\n"""\n'


def test_ordinary_variable_reads_are_untouched():
    """The helper is vision-scoped: plain var() must not gain quote characters,
    or typed values and assertion operands would be corrupted."""
    set_var("n", 42)
    assert var("{{n}}") == 42
    assert var("value is {{n}}") == "value is 42"


def test_vision_query_requests_fencing():
    from testmu_selenium._helpers.vision_query import visionQuery

    set_var("v", MULTILINE)
    with patch("testmu_selenium._helpers.vision_query.SmartWait", return_value=MagicMock()), \
         patch("testmu_selenium._helpers.vision_query.get_driver", return_value=MagicMock()), \
         patch("testmu_selenium._helpers.vision_query.Heal") as m_heal:
        m_heal.return_value.vision_query.return_value.json.return_value = {"vision_query": True}
        visionQuery("Does {{v}} appear?", "bool")

    action = m_heal.call_args.args[0]
    sent = action["operation_intent"]
    assert '"""' in sent and MULTILINE in sent
    # automind reads queried_value; it must carry the same fenced text.
    assert action["sub_instruction_obj"]["operation_dict"]["queried_value"] == sent
