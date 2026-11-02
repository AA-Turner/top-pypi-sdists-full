from agentic_devtools.cli.checks.pre_push_budget import _eligible_signal_handlers


def test_non_posix_scope_has_no_eligible_handlers():
    assert _eligible_signal_handlers(lambda: False, lambda: True, lambda _: None) == []
