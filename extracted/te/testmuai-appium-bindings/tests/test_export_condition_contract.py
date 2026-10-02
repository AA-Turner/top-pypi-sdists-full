"""The mobile export's branch conditions, evaluated against the real resolver.

code-export's tree_walker emits branch guards as plain Python over this
binding's var() — its test_tree_walker_mobile_if_else.py pins the emitted
strings; the strings below are copies of those emissions. Evaluating them here,
against the real var()/set_var, means a drift in var()'s template or
native-value semantics fails in the repo that changed them, instead of
silently un-taking every exported branch.
"""
import pytest

from testmu_appium._vars import clear_state, set_var, var


@pytest.fixture(autouse=True)
def _clear_vars():
    clear_state()
    yield
    clear_state()


# As emitted by _mobile_branch_condition for
# sub_checks=[{store_key: "username_visible", expected: "true", operator: "equals"}].
_GUARD = "str(var('{{username_visible}}')) == 'true'"

# As emitted for a recorded default branch behind that one checked branch.
_DEFAULT_GUARD = "not ((str(var('{{username_visible}}')) == 'true'))"


def test_the_emitted_guard_takes_the_branch_when_the_check_holds():
    set_var("username_visible", "true")
    assert eval(_GUARD, {"var": var}) is True
    assert eval(_DEFAULT_GUARD, {"var": var}) is False


def test_the_emitted_guard_skips_the_branch_when_the_check_fails():
    set_var("username_visible", "false")
    assert eval(_GUARD, {"var": var}) is False
    assert eval(_DEFAULT_GUARD, {"var": var}) is True


def test_an_unstored_variable_fails_closed():
    """var() returns the template literally when nothing is stored — the
    checked branch is not taken, and the default's negated guard is."""
    assert eval(_GUARD, {"var": var}) is False
    assert eval(_DEFAULT_GUARD, {"var": var}) is True


def test_a_native_stored_value_still_compares_as_text():
    """A whole-string template resolves NATIVELY; the emitted str() coercion
    is what lets a numeric store match its recorded text."""
    set_var("retry_count", 3)
    assert eval("str(var('{{retry_count}}')) == '3'", {"var": var}) is True
